"""
Top-level driver for ``script/sdk-sync``.

Pipeline executed per run:

1. Discover the set of stub files that have been modified vs ``HEAD`` (or
   accept an explicit ``--stub`` list).
2. For each stub, extract the IR of both the HEAD revision (via
   ``git show HEAD:<path>``) and the working-tree revision.
3. Run the :mod:`~script.sdk_sync.differ` over the two IRs to produce
   :class:`~script.sdk_sync.differ.ChangeRecord` objects.
4. Hand each record to the :mod:`~script.sdk_sync.matcher` to find its SDK
   counterpart, then dispatch via :mod:`~script.sdk_sync.dispatcher`.
5. Persist any pending in-memory rewrites (unless ``--dry-run``).
6. Save the (possibly updated) alias cache and write
   ``sync_report.md`` with the per-change outcomes.

Exit code is ``0`` when no record produced a ``punted_*`` outcome and
``1`` otherwise -- convenient for wiring into CI even though the current
default is to invoke the tool manually via ``script/sdk-sync`` or
``make sync-stubs``.
"""

from __future__ import annotations

import argparse
import fnmatch
import glob
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING

from . import aliases as _aliases
from . import dispatcher as _dispatcher
from .differ import ChangeRecord, diff_irs
from .ir import extract, extract_from_text

if TYPE_CHECKING:
    from .matcher import Match

# Repo root is three levels above this file.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# The per-run markdown report lives at the repo root and is gitignored.
_REPORT_PATH = _REPO_ROOT / 'sync_report.md'

# Stub-file discovery is always restricted to this subtree. `--stub` basenames
# and globs without a directory part are resolved beneath it.
_STUB_ROOT = 'open_api/generated'


def main(argv: list[str] | None = None) -> int:
    """Run the full sync pipeline.

    Side effects: writes :data:`_REPORT_PATH`, updates ``aliases.json``, and
    (unless ``--dry-run``) rewrites SDK files.

    :param argv: Optional argv override for tests. ``None`` reads from
        :data:`sys.argv` as usual.
    :return: Exit status — ``0`` on full success, ``1`` if at least one
        record ended in a ``punted_*`` state.
    """
    parser = argparse.ArgumentParser(
        prog='sdk-sync',
        description=__doc__.strip() if __doc__ else None,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Do not modify any files; write the report only.',
    )
    parser.add_argument(
        '--no-llm',
        action='store_true',
        help='Skip the LLM step; only apply deterministic patches.',
    )
    parser.add_argument(
        '--stub',
        action='append',
        default=None,
        help=(
            'Restrict the run to specific stubs (repeat for multiple). Each value may be a '
            'repo-relative path, a bare basename (resolved as `open_api/generated/**/<name>`), '
            'or a glob. Default: all stubs modified vs HEAD.'
        ),
    )
    parser.add_argument(
        '--only',
        action='append',
        default=None,
        help=(
            'After discovery, keep only stubs whose repo-relative path or basename matches one '
            'of these glob patterns (repeat for multiple). Intersects with both default discovery '
            'and --stub.'
        ),
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Print one line per LLM dispatch and per LLM CLI call (start, elapsed, outcome).',
    )
    parser.add_argument(
        '--print-prompts',
        action='store_true',
        help='Print full LLM prompts to stdout before invoking the model; requires -v/--verbose.',
    )
    parser.add_argument(
        '--llm-timeout',
        type=float,
        default=240.0,
        help='Maximum seconds to wait for each LLM CLI invocation. Default: 240.',
    )
    args = parser.parse_args(argv)
    if args.print_prompts and not args.verbose:
        parser.error('--print-prompts requires -v/--verbose')
    if args.llm_timeout <= 0:
        parser.error('--llm-timeout must be greater than zero')

    config = _dispatcher.DispatchConfig(
        dry_run=args.dry_run,
        use_llm=not args.no_llm,
        verbose=args.verbose,
        print_prompts=args.print_prompts,
        llm_timeout=args.llm_timeout,
    )

    # `--stub` overrides the default git-derived scope. Useful for replays or
    # targeted reruns once aliases have been hand-curated.
    if args.stub:
        stubs: list[str] = []
        seen: set[str] = set()
        for value in args.stub:
            resolved = _resolve_stub_arg(value)
            if not resolved:
                parser.error(f'--stub {value!r} did not match any file under {_STUB_ROOT}/')
            for resolved_path in resolved:
                if resolved_path not in seen:
                    seen.add(resolved_path)
                    stubs.append(resolved_path)
    else:
        stubs = _git_diff_name_only('HEAD', f'{_STUB_ROOT}/')

    if args.only:
        stubs = [
            s for s in stubs if any(fnmatch.fnmatch(s, pat) or fnmatch.fnmatch(Path(s).name, pat) for pat in args.only)
        ]

    if not stubs:
        print('No stub changes to sync.')
        return 0

    store = _aliases.load()
    # Always start with a fresh `unmatched` list — entries from prior runs
    # would otherwise accumulate. The matcher repopulates it as it goes.
    store.unmatched = []

    # Pending in-memory rewrites shared across the dispatcher's per-record
    # calls. Persisted to disk at the end of the run unless `--dry-run`.
    pending_writes: dict[Path, str] = {}
    outcomes: list[_dispatcher.Outcome] = []
    skipped: list[tuple[str, str]] = []

    for stub in stubs:
        stub_rel = stub if Path(stub).is_absolute() is False else str(Path(stub).relative_to(_REPO_ROOT))
        try:
            old_text = _git_show(stub_rel)
        except subprocess.CalledProcessError:
            old_text = ''
        new_path = _REPO_ROOT / stub_rel
        if not new_path.exists():
            skipped.append((stub_rel, 'file does not exist in working tree'))
            continue
        if not old_text.strip():
            # New (untracked) stub file: no `git show HEAD:<path>` output, so
            # nothing to diff against. Skip with a note in the report.
            skipped.append((stub_rel, 'new file with no HEAD revision (no diff to compute)'))
            continue
        try:
            old_ir = extract_from_text(old_text, stub_rel)
            new_ir = extract(new_path)
        except SyntaxError as exc:
            # Don't take the whole run down because one stub failed to parse.
            skipped.append((stub_rel, f'syntax error: {exc}'))
            continue
        # Imported lazily here to avoid a circular import at module-load
        # time (matcher imports `aliases`, which the driver also uses).
        from .matcher import match as match_record

        # Materialize all (record, match) pairs first so we can detect
        # stub-side renames: when a method_removed and a method_added in the
        # same stub both resolve to the same SDK target, the SDK already
        # implements both — the stub just renamed itself.
        matched: list[tuple[ChangeRecord, Match | None]] = [
            (record, match_record(record, new_ir, store)) for record in diff_irs(old_ir, new_ir)
        ]
        renamed_targets = _detect_rename_targets(matched)
        for record, m in matched:
            rename_detail = _rename_supersedes(record, m, renamed_targets)
            if rename_detail is not None:
                outcomes.append(_dispatcher.Outcome(record, m, 'already_in_sync', detail=rename_detail))
                continue
            outcome = _dispatcher.dispatch(record, m, config, pending_writes=pending_writes)
            outcomes.append(outcome)

    # Flush pending in-memory rewrites to disk. In dry-run mode we skip
    # the flush so the working tree is untouched.
    if not args.dry_run:
        for path, text in pending_writes.items():
            path.write_text(text)

    _aliases.save(store)
    _write_report(outcomes, skipped, args)

    # Console summary mirrors the per-status section of the report.
    counts = Counter(o.status for o in outcomes)
    print(f'sdk_sync done. {sum(counts.values())} change records processed; report at {_REPORT_PATH}')
    for status, n in sorted(counts.items()):
        print(f'  {status:30s}  {n}')
    if skipped:
        print(f'  skipped stubs: {len(skipped)}')

    failures = sum(n for s, n in counts.items() if s.startswith('punted'))
    return 0 if failures == 0 else 1


# ---------------------------------------------------------------------------
# Stub-rename detection
#
# The OpenAPI generator periodically renames its method names (e.g.,
# ``delete_a_supervisor`` → ``delete_call_queue_supervisor``). The differ
# sees these as a paired ``method_removed`` + ``method_added``. When both
# resolve to the same SDK target, the SDK already implements both names'
# semantics — the disappearance carries no SDK-side action.
# ---------------------------------------------------------------------------

# Confidence floor for treating a paired (removed, added) as a rename. Both
# sides must independently clear this bar; lower-confidence matches may
# point at the wrong SDK method, and silently swallowing a method_removed
# based on a guess is the dangerous failure mode.
_RENAME_CONFIDENCE_FLOOR = 1.0


def _detect_rename_targets(
    matched: list[tuple[ChangeRecord, Match | None]],
) -> set[tuple[Path, str, str | None, str]]:
    """Return SDK targets covered by a high-confidence ``method_added``.

    Each target is the tuple ``(sdk_path, sdk_class, sdk_member, stub_module)``
    where ``stub_module`` keeps the pairing scoped to a single auto-stub file
    so a removal in one stub can't mask an addition in another.

    Only matches with ``confidence >= _RENAME_CONFIDENCE_FLOOR`` participate.

    :param matched: Per-stub list of ``(record, match)`` pairs from one
        ``diff_irs`` run.
    :return: Set of tuples used by :func:`_rename_supersedes` to look up a
        candidate ``method_removed``.
    """
    targets: set[tuple[Path, str, str | None, str]] = set()
    for record, m in matched:
        if record.kind != 'method_added' or m is None:
            continue
        if m.confidence < _RENAME_CONFIDENCE_FLOOR:
            continue
        targets.add((m.sdk_path, m.sdk_class, m.sdk_member, _stub_module_of(record)))
    return targets


def _rename_supersedes(
    record: ChangeRecord,
    match: Match | None,
    renamed_targets: set[tuple[Path, str, str | None, str]],
) -> str | None:
    """Decide whether a ``method_removed`` is superseded by a paired add.

    :param record: The change record under consideration.
    :param match: The matcher's resolution for ``record``, or ``None``.
    :param renamed_targets: Output of :func:`_detect_rename_targets`.
    :return: A human-readable detail string for the resulting
        ``already_in_sync`` outcome, or ``None`` when the record should
        flow through the normal dispatcher.
    """
    if record.kind != 'method_removed' or match is None:
        return None
    if match.confidence < _RENAME_CONFIDENCE_FLOOR:
        return None
    key = (match.sdk_path, match.sdk_class, match.sdk_member, _stub_module_of(record))
    if key not in renamed_targets:
        return None
    return f'rename detected; {match.sdk_class}.{match.sdk_member} now reached via a renamed stub method'


def _stub_module_of(record: ChangeRecord) -> str:
    """Best-effort extraction of the stub module for a record.

    Records emitted by :mod:`script.sdk_sync.differ` don't carry the stub
    path directly, but ``ChangeRecord.qualname`` always starts with the
    stub class name, which is unique per stub module. Using the class name
    as the scoping key is sufficient: rename pairing is meaningful only
    inside the same auto-stub class.

    :param record: A change record produced by :mod:`script.sdk_sync.differ`.
    :return: The stub class name (e.g. ``'FeaturesCallQueueApi'``).
    """
    return record.qualname.split('.', 1)[0]


def _resolve_stub_arg(value: str) -> list[str]:
    """Expand a single ``--stub`` argument into repo-relative stub paths.

    Resolution order:

    1. Literal path (relative to the repo root) that exists on disk → returned as-is.
    2. Value containing ``*`` or ``?`` → ``glob.glob`` rooted at the repo, then
       filtered to entries under ``open_api/generated/``.
    3. Bare token (no path separator and no wildcard) → resolved as
       ``open_api/generated/**/<value>`` so basenames like
       ``call-controls-members_auto.py`` work.

    :param value: The raw ``--stub`` value as typed by the user.
    :return: List of repo-relative paths (possibly empty if no match found).
    """
    candidate = _REPO_ROOT / value
    if candidate.is_file():
        return [value]
    has_wildcard = any(ch in value for ch in '*?[')
    has_sep = '/' in value or '\\' in value
    if not has_wildcard and not has_sep:
        pattern = f'{_STUB_ROOT}/**/{value}'
    elif has_wildcard:
        pattern = value
    else:
        # Path-like value that didn't exist on disk and has no wildcard;
        # no useful glob expansion to try.
        return []
    matches = glob.glob(pattern, root_dir=str(_REPO_ROOT), recursive=True)
    return sorted(m for m in matches if m.startswith(f'{_STUB_ROOT}/'))


def _git_show(path: str) -> str:
    """Return ``git show HEAD:<path>`` output as a string.

    :param path: Repo-relative path.
    :return: File contents at ``HEAD``.
    :raises subprocess.CalledProcessError: If git fails (e.g. path not in
        the HEAD tree); the caller treats that as "new file".
    """
    proc = subprocess.run(
        ['git', 'show', f'HEAD:{path}'],
        cwd=_REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout


def _git_diff_name_only(rev: str, scope: str) -> list[str]:
    """List files modified between ``rev`` and the working tree, scoped to a path.

    :param rev: Git revision to compare against (typically ``'HEAD'``).
    :param scope: Pathspec passed after ``--``; we restrict to
        ``open_api/generated/`` so this never accidentally picks up SDK files.
    :return: List of repo-relative paths, in git's output order.
    """
    proc = subprocess.run(
        ['git', 'diff', '--name-only', rev, '--', scope],
        cwd=_REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [ln for ln in proc.stdout.splitlines() if ln.strip()]


def _write_report(
    outcomes: list[_dispatcher.Outcome],
    skipped: list[tuple[str, str]],
    args: argparse.Namespace,
) -> None:
    """Render the markdown report and write it to :data:`_REPORT_PATH`.

    The report has three sections:

    - Run metadata (dry-run, llm, scoped stubs).
    - Per-status counts.
    - One section per status, listing every outcome with the matched SDK
      target, optional detail string, and (for LLM outcomes) the diff.

    :param outcomes: All :class:`Outcome` objects produced during the run.
    :param skipped: Tuples of ``(stub_path, reason)`` for stubs the driver
        skipped before the differ even ran.
    :param args: The parsed :class:`argparse.Namespace`; used for the
        metadata header.
    :return: Nothing. The file is written as a side effect.
    """
    lines: list[str] = []
    lines.append('# sdk_sync report')
    lines.append('')
    lines.append(f'- dry_run: `{args.dry_run}`')
    lines.append(f'- use_llm: `{not args.no_llm}`')
    lines.append(f'- verbose: `{args.verbose}`')
    lines.append(f'- stubs scoped: `{args.stub or "<all changed>"}`')
    lines.append(f'- only: `{args.only or "<none>"}`')
    lines.append('')
    counts = Counter(o.status for o in outcomes)
    lines.append('## Summary')
    lines.append('')
    for status, n in sorted(counts.items()):
        lines.append(f'- `{status}`: {n}')
    lines.append('')
    if skipped:
        lines.append('## Skipped stubs')
        lines.append('')
        for path, reason in skipped:
            lines.append(f'- `{path}` — {reason}')
        lines.append('')
    # Group by status so reviewers can jump to e.g. `punted_diff_rejected` directly.
    # Use a separate name (`status_key`) for this loop's variable — the earlier
    # `for status, n in sorted(counts.items())` loop typed `status` as Literal
    # because Counter[Literal] iterates as Literal, and reusing the name here
    # would conflict with the dict[str, ...] key type.
    by_status: dict[str, list[_dispatcher.Outcome]] = {}
    for o in outcomes:
        by_status.setdefault(o.status, []).append(o)
    for status_key in sorted(by_status):
        lines.append(f'## {status_key} ({len(by_status[status_key])})')
        lines.append('')
        for o in by_status[status_key]:
            target = ''
            if o.match is not None:
                target = (
                    f'  → `{_rel(o.match.sdk_path)}::{o.match.sdk_class}.{o.match.sdk_member or ""}` '
                    f'(via {o.match.matched_by}, conf={o.match.confidence:.2f})'
                )
            lines.append(f'- `{o.record.kind}` **{o.record.qualname}**{target}')
            if o.detail:
                lines.append(f'  - detail: {o.detail}')
            if o.diff:
                lines.append('  - diff:')
                lines.append('    ```diff')
                for dl in o.diff.splitlines():
                    lines.append(f'    {dl}')
                lines.append('    ```')
        lines.append('')
    _REPORT_PATH.write_text('\n'.join(lines))


def _rel(path: Path) -> str:
    """Express ``path`` relative to the repo root.

    :param path: Any absolute path; SDK file paths in practice.
    :return: Repo-root-relative string, or ``str(path)`` if the path is
        outside the repo root.
    """
    try:
        return str(path.relative_to(_REPO_ROOT))
    except ValueError:
        return str(path)


if __name__ == '__main__':
    sys.exit(main())

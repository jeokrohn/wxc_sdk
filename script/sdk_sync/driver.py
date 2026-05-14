"""
Top-level driver for ``python -m script.sdk_sync``.

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
``1`` otherwise — convenient for wiring into CI even though the current
default is to invoke the tool manually via ``make sync-stubs``.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter
from pathlib import Path

from . import aliases as _aliases
from . import dispatcher as _dispatcher
from .differ import diff_irs
from .ir import extract, extract_from_text

# Repo root is three levels above this file.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# The per-run markdown report lives at the repo root and is gitignored.
_REPORT_PATH = _REPO_ROOT / 'sync_report.md'


def main(argv: list[str] | None = None) -> int:
    """Run the full sync pipeline.

    Side effects: writes :data:`_REPORT_PATH`, updates ``aliases.json``, and
    (unless ``--dry-run``) rewrites SDK files.

    :param argv: Optional argv override for tests. ``None`` reads from
        :data:`sys.argv` as usual.
    :return: Exit status — ``0`` on full success, ``1`` if at least one
        record ended in a ``punted_*`` state.
    """
    parser = argparse.ArgumentParser(prog='sdk_sync', description=__doc__)
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
        help='Restrict the run to specific stub paths (repeat for multiple). Default: all stubs modified vs HEAD.',
    )
    args = parser.parse_args(argv)

    config = _dispatcher.DispatchConfig(dry_run=args.dry_run, use_llm=not args.no_llm)

    # `--stub` overrides the default git-derived scope. Useful for replays or
    # targeted reruns once aliases have been hand-curated.
    stubs = args.stub if args.stub else _git_diff_name_only('HEAD', 'open_api/generated/')
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
        for record in diff_irs(old_ir, new_ir):
            # Imported lazily here to avoid a circular import at module-load
            # time (matcher imports `aliases`, which the driver also uses).
            from .matcher import match as match_record

            m = match_record(record, new_ir, store)
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
    lines.append(f'- stubs scoped: `{args.stub or "<all changed>"}`')
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

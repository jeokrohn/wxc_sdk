"""
Routes :class:`~script.sdk_sync.differ.ChangeRecord` objects to the patcher or
the LLM step.

For each record:

1. If ``record.severity == 'trivial'``, try the deterministic patcher
   (:mod:`~script.sdk_sync.patcher`). On success the SDK file is rewritten —
   in-memory in dry-run mode (via the ``pending_writes`` accumulator) or to
   disk when the driver flushes at the end of the run.
2. Otherwise — or if the patcher returns :class:`Punt` for a reason other
   than the idempotent-skip sentinel — invoke the LLM step
   (:mod:`~script.sdk_sync.llm`). The returned unified diff is validated
   with ``git apply --check`` before being applied.
3. On any failure the change becomes a ``punted_*`` :class:`Outcome` with
   detail (and, for rejected LLM diffs, the diff text). The driver renders
   all outcomes into ``sync_report.md``.

Dry-run discipline: the dispatcher never writes to disk directly. It mutates
the ``pending_writes`` dict the driver hands it, and the driver decides
whether to flush. LLM-driven patches are an exception: ``git apply`` is the
only practical way to validate the diff, so in dry-run mode the diff is
captured under ``dry_run_pending`` and not applied.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from . import llm as _llm
from . import patcher as _patcher
from .differ import ChangeRecord
from .matcher import Match

# Repo root is three levels above this file: script/sdk_sync/dispatcher.py
# → script/sdk_sync → script → repo root.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent


#: The set of possible per-record outcomes. Exhaustive — the driver groups
#: the report by these values.
OutcomeStatus = Literal[
    'applied_trivial',  # deterministic patcher succeeded
    'applied_llm',  # LLM diff applied
    'already_in_sync',  # idempotent skip — change already reflected in SDK
    'punted_no_match',
    'punted_patcher_refused',
    'punted_llm_unavailable',
    'punted_diff_rejected',
    'dry_run_pending',
]


@dataclass
class Outcome:
    """The result of dispatching a single :class:`ChangeRecord`.

    :param record: The originating change.
    :param match: The resolved SDK target, or ``None`` for ``punted_no_match``.
    :param status: One of :data:`OutcomeStatus`.
    :param detail: Free-form human-readable explanation; shown in the report.
    :param diff: Unified diff text for LLM-derived outcomes (applied,
        rejected, or pending). Empty for trivial outcomes.
    """

    record: ChangeRecord
    match: Match | None
    status: OutcomeStatus
    detail: str = ''
    diff: str = ''


@dataclass
class DispatchConfig:
    """Behaviour switches for a single dispatch pass.

    :param dry_run: When ``True``, in-memory rewrites accumulate in
        ``pending_writes`` but are never persisted to disk, and LLM-derived
        diffs are captured under ``dry_run_pending`` instead of being applied.
    :param use_llm: When ``False``, changes that the deterministic patcher
        refuses become ``punted_patcher_refused`` outcomes; the LLM step is
        not consulted at all.
    :param verbose: When ``True``, the dispatcher prints one ``[llm-dispatch]``
        line per LLM-bound record and one ``[llm] ...`` line per LLM CLI
        call (including elapsed time and outcome). Default keeps the script
        silent until the end-of-run summary.
    :param print_prompts: When ``True`` and ``verbose`` is also ``True``, print
        the full prompt before each LLM CLI invocation.
    :param llm_timeout: Maximum seconds to wait for each individual LLM CLI
        invocation.
    """

    dry_run: bool = False
    use_llm: bool = True
    verbose: bool = False
    print_prompts: bool = False
    llm_timeout: float = 240.0


def dispatch(
    record: ChangeRecord,
    match: Match | None,
    config: DispatchConfig,
    pending_writes: dict[Path, str] | None = None,
) -> Outcome:
    """Route one change record through the patcher / LLM pipeline.

    Flow:

    1. ``match is None`` → ``punted_no_match``.
    2. If a previous change in this run has already rewritten the target SDK
       file, refresh the match's IR from the pending text so subsequent
       patches see the up-to-date view.
    3. For trivial records, try the deterministic patcher. Success →
       ``applied_trivial``. ``idempotent skip`` punt → ``already_in_sync``.
       Other punt → fall through to the LLM step if enabled.
    4. For review-severity records (and trivial fall-throughs), invoke the
       LLM via :func:`_try_llm`. The diff is validated and applied via
       ``git apply``.

    :param record: The change to dispatch.
    :param match: The matcher's resolution result, or ``None`` on a miss.
    :param config: Dispatch behaviour flags.
    :param pending_writes: Mutable map of ``sdk_path → new_text`` shared
        across all calls in a single run. The driver creates it; the
        dispatcher writes to it. ``None`` is accepted only for callers
        that don't care about ordering between patches.
    :return: An :class:`Outcome` describing what happened.
    """
    if match is None:
        return Outcome(record, None, 'punted_no_match', detail='no SDK counterpart')

    if pending_writes is not None and match.sdk_path in pending_writes:
        # A previous patch in this run already mutated the SDK file. Re-parse
        # so subsequent patches see the updated source text and line numbers.
        match = _refresh_match(match, pending_writes[match.sdk_path])

    if record.severity == 'trivial':
        result = _patcher.apply(record, match)
        if isinstance(result, _patcher.PatchResult):
            if pending_writes is not None:
                pending_writes[match.sdk_path] = result.new_text
            return Outcome(record, match, 'applied_trivial', detail=result.summary)
        if 'idempotent skip' in result.reason:
            # The change is already reflected in the SDK — count it as
            # success, but distinguish it from an actual edit in the report.
            return Outcome(record, match, 'already_in_sync', detail=result.reason)
        # Patcher refused for some other reason — fall through to LLM if enabled.
        if not config.use_llm:
            return Outcome(record, match, 'punted_patcher_refused', detail=result.reason)
        if config.verbose:
            _print_dispatch(record, match, fallback_reason=result.reason)
        return _try_llm(record, match, config, pending_writes, fallback_reason=result.reason)

    if not config.use_llm:
        return Outcome(record, match, 'punted_patcher_refused', detail='requires LLM but disabled')
    if config.verbose:
        _print_dispatch(record, match)
    return _try_llm(record, match, config, pending_writes)


def _try_llm(
    record: ChangeRecord,
    match: Match,
    config: DispatchConfig,
    pending_writes: dict[Path, str] | None,
    fallback_reason: str = '',
) -> Outcome:
    """Invoke the LLM step and apply its diff (or record why we didn't).

    The function always runs ``git apply --check`` before committing to a
    real ``git apply``. In dry-run mode it stops at the check stage and
    returns the diff under ``dry_run_pending``.

    :param record: The change being applied.
    :param match: The resolved SDK target.
    :param config: Dispatch behaviour flags (used to gate ``dry_run``).
    :param pending_writes: Same accumulator passed to :func:`dispatch`;
        invalidated for ``match.sdk_path`` after a successful apply because
        ``git apply`` has already written the file.
    :param fallback_reason: When the LLM is being invoked as a fallback
        from a refused deterministic patch, this is the patcher's punt
        reason; embedded in the resulting :class:`Outcome.detail` for the
        report.
    :return: An :class:`Outcome`; the diff (if any) is preserved on the
        outcome so the report can show it.
    """
    sdk_text = (
        pending_writes[match.sdk_path]
        if pending_writes and match.sdk_path in pending_writes
        else match.sdk_path.read_text()
    )
    try:
        diff = _llm.propose_diff(
            record,
            match,
            sdk_text,
            timeout=config.llm_timeout,
            verbose=config.verbose,
            print_prompts=config.print_prompts,
        )
    except _llm.LLMError as exc:
        outcome = Outcome(record, match, 'punted_llm_unavailable', detail=f'{fallback_reason} | LLM: {exc}')
        if config.verbose:
            print(f'[llm] error: {exc}')
        return outcome
    # An empty (or hunk-less) response means the LLM judged the SDK already
    # in sync — e.g. for `docstring_changed` where the SDK's docstring
    # already reflects the new stub state. Surface that as `already_in_sync`
    # so the report doesn't conflate it with a malformed diff. We require a
    # full minimal-diff shape (file headers + at least one `@@` hunk + at
    # least one `+`/`-` change line) so we don't dispatch obviously-empty
    # patches to `git apply` only to have it bounce them with "No valid
    # patches in input".
    if not _looks_like_diff(diff):
        semantic_err = _semantic_validation_error(record, match, sdk_text)
        if semantic_err:
            retry_outcome = _retry_llm_diff(
                record, match, sdk_text, config, pending_writes, fallback_reason, diff, semantic_err
            )
            if retry_outcome is not None:
                return retry_outcome
        if config.verbose:
            print('[llm] no diff returned — SDK already in sync per LLM')
        return Outcome(record, match, 'already_in_sync', detail='LLM judged SDK already in sync')
    try:
        diff = _normalize_diff_paths(diff, match)
    except ValueError as exc:
        err_one_line = _flatten_git_err(str(exc))
        _dump_rejected(record, match, diff, str(exc))
        if config.verbose:
            print(f'[llm] diff rejected before `git apply --check`: {err_one_line}')
        detail = f'{fallback_reason} | diff path: {err_one_line}' if fallback_reason else f'diff path: {err_one_line}'
        return Outcome(record, match, 'punted_diff_rejected', detail=detail, diff=diff)
    diff_lines = len(diff.splitlines())
    ok, err = _git_apply_check(diff)
    if not ok:
        if _should_retry_llm_diff(err):
            retry_outcome = _retry_llm_diff(record, match, sdk_text, config, pending_writes, fallback_reason, diff, err)
            if retry_outcome is not None:
                return retry_outcome
        err_one_line = _flatten_git_err(err)
        _dump_rejected(record, match, diff, err)
        if config.verbose:
            print(f'[llm] diff rejected by `git apply --check` ({diff_lines} lines): {err_one_line}')
        detail = f'{fallback_reason} | git apply: {err_one_line}' if fallback_reason else f'git apply: {err_one_line}'
        return Outcome(record, match, 'punted_diff_rejected', detail=detail, diff=diff)
    semantic_err = _semantic_validation_error_for_diff(record, match, sdk_text, diff)
    if semantic_err:
        if config.verbose:
            print(f'[llm] diff rejected by semantic validation: {_flatten_git_err(semantic_err)}')
        retry_outcome = _retry_llm_diff(
            record, match, sdk_text, config, pending_writes, fallback_reason, diff, semantic_err
        )
        if retry_outcome is not None:
            return retry_outcome
    if config.dry_run:
        if config.verbose:
            print(f'[llm] dry-run, diff captured ({diff_lines} lines)')
        return Outcome(record, match, 'dry_run_pending', detail=fallback_reason, diff=diff)
    ok, err = _git_apply(diff)
    if not ok:
        err_one_line = _flatten_git_err(err)
        _dump_rejected(record, match, diff, err)
        if config.verbose:
            print(f'[llm] apply failed after passing --check ({diff_lines} lines): {err_one_line}')
        return Outcome(
            record,
            match,
            'punted_diff_rejected',
            detail=f'applied check passed but apply failed | git apply: {err_one_line}',
            diff=diff,
        )
    # After a successful git apply, the on-disk file is now the source of
    # truth — drop any stale entry in pending_writes so a later trivial
    # patch on the same file re-reads the freshly applied text.
    if pending_writes is not None and match.sdk_path in pending_writes:
        del pending_writes[match.sdk_path]
    if config.verbose:
        print(f'[llm] applied ({diff_lines} diff lines)')
    return Outcome(record, match, 'applied_llm', detail='LLM patch applied', diff=diff)


def _retry_llm_diff(
    record: ChangeRecord,
    match: Match,
    sdk_text: str,
    config: DispatchConfig,
    pending_writes: dict[Path, str] | None,
    fallback_reason: str,
    rejected_diff: str,
    git_error: str,
) -> Outcome | None:
    """Ask the LLM for one fresh diff after a stale-context rejection.

    Returns an :class:`Outcome` for any terminal retry result, or ``None`` if
    the caller should keep handling the original failed diff.
    """
    if config.verbose:
        print(f'[llm] retrying after `git apply --check` failed: {_flatten_git_err(git_error)}')
    try:
        retry_diff = _llm.propose_diff(
            record,
            match,
            sdk_text,
            timeout=config.llm_timeout,
            verbose=config.verbose,
            print_prompts=config.print_prompts,
            rejected_diff=rejected_diff,
            git_error=git_error,
        )
    except _llm.LLMError as exc:
        detail = f'{fallback_reason} | ' if fallback_reason else ''
        detail += f'git apply: {_flatten_git_err(git_error)} | retry LLM: {exc}'
        if config.verbose:
            print(f'[llm] retry error: {exc}')
        return Outcome(record, match, 'punted_diff_rejected', detail=detail, diff=rejected_diff)
    if not _looks_like_diff(retry_diff):
        semantic_err = _semantic_validation_error(record, match, sdk_text)
        if semantic_err:
            detail = f'{fallback_reason} | ' if fallback_reason else ''
            detail += f'retry returned no diff but semantic validation failed: {_flatten_git_err(semantic_err)}'
            if config.verbose:
                print(f'[llm] retry returned no diff but semantic validation failed: {_flatten_git_err(semantic_err)}')
            return Outcome(record, match, 'punted_diff_rejected', detail=detail, diff=retry_diff)
        if config.verbose:
            print('[llm] retry returned no diff — SDK already in sync per LLM')
        return Outcome(record, match, 'already_in_sync', detail='LLM retry judged SDK already in sync')
    try:
        retry_diff = _normalize_diff_paths(retry_diff, match)
    except ValueError as exc:
        err_one_line = _flatten_git_err(str(exc))
        _dump_rejected(record, match, retry_diff, str(exc))
        if config.verbose:
            print(f'[llm] retry diff rejected before `git apply --check`: {err_one_line}')
        detail = (
            f'{fallback_reason} | retry diff path: {err_one_line}'
            if fallback_reason
            else (f'retry diff path: {err_one_line}')
        )
        return Outcome(record, match, 'punted_diff_rejected', detail=detail, diff=retry_diff)
    ok, err = _git_apply_check(retry_diff)
    if not ok:
        err_one_line = _flatten_git_err(err)
        _dump_rejected(record, match, retry_diff, err)
        if config.verbose:
            retry_diff_lines = len(retry_diff.splitlines())
            print(f'[llm] retry diff rejected by `git apply --check` ({retry_diff_lines} lines): {err_one_line}')
        detail = (
            f'{fallback_reason} | retry git apply: {err_one_line}'
            if fallback_reason
            else (f'retry git apply: {err_one_line}')
        )
        return Outcome(record, match, 'punted_diff_rejected', detail=detail, diff=retry_diff)
    semantic_err = _semantic_validation_error_for_diff(record, match, sdk_text, retry_diff)
    if semantic_err:
        err_one_line = _flatten_git_err(semantic_err)
        _dump_rejected(record, match, retry_diff, semantic_err)
        if config.verbose:
            retry_diff_lines = len(retry_diff.splitlines())
            print(f'[llm] retry diff rejected by semantic validation ({retry_diff_lines} lines): {err_one_line}')
        detail = (
            f'{fallback_reason} | retry semantic validation: {err_one_line}'
            if fallback_reason
            else (f'retry semantic validation: {err_one_line}')
        )
        return Outcome(record, match, 'punted_diff_rejected', detail=detail, diff=retry_diff)
    diff_lines = len(retry_diff.splitlines())
    if config.dry_run:
        if config.verbose:
            print(f'[llm] retry dry-run, diff captured ({diff_lines} lines)')
        return Outcome(record, match, 'dry_run_pending', detail=fallback_reason, diff=retry_diff)
    ok, err = _git_apply(retry_diff)
    if not ok:
        err_one_line = _flatten_git_err(err)
        _dump_rejected(record, match, retry_diff, err)
        if config.verbose:
            print(f'[llm] retry apply failed after passing --check ({diff_lines} lines): {err_one_line}')
        return Outcome(
            record,
            match,
            'punted_diff_rejected',
            detail=f'retry check passed but apply failed | git apply: {err_one_line}',
            diff=retry_diff,
        )
    if pending_writes is not None and match.sdk_path in pending_writes:
        del pending_writes[match.sdk_path]
    if config.verbose:
        print(f'[llm] retry applied ({diff_lines} diff lines)')
    return Outcome(record, match, 'applied_llm', detail='LLM patch applied after retry', diff=retry_diff)


def _print_dispatch(record: ChangeRecord, match: Match, fallback_reason: str = '') -> None:
    """Print a single ``[llm-dispatch]`` line announcing an LLM-bound record.

    Called from :func:`dispatch` only when ``config.verbose`` is set.
    Mirrors the style of the per-record line in ``sync_report.md`` so the
    console output and report stay legibly correlated.
    """
    try:
        rel = str(match.sdk_path.relative_to(_REPO_ROOT))
    except ValueError:
        rel = str(match.sdk_path)
    target = f'{rel}::{match.sdk_class}.{match.sdk_member or ""}'
    suffix = f' (fallback: {fallback_reason})' if fallback_reason else ''
    print(f'[llm-dispatch] {record.kind} {record.qualname} → {target}{suffix}')


def _refresh_match(match: Match, new_text: str) -> Match:
    """Re-extract the SDK IR from in-memory text and return an updated match.

    Used when an earlier patch in the same run has mutated the SDK file:
    the next patch needs the post-edit line numbers and member list, so we
    rebuild the :class:`ModuleIR` from the pending text and stitch it into
    the existing match.

    :param match: The previous match, whose ``sdk_module_ir`` is stale.
    :param new_text: The post-patch SDK source text.
    :return: A new :class:`Match` carrying the freshly extracted IR.
    """
    # Imported lazily to keep this module's import time low and avoid an
    # apparent circular dependency through the matcher.
    from .ir import extract_from_text

    # is_sdk=True so the refreshed IR uses the same live-replay endpoint
    # resolution as the cached SDK index in matcher._SDKIndex.
    new_ir = extract_from_text(new_text, str(match.sdk_path), is_sdk=True)
    return Match(
        sdk_path=match.sdk_path,
        kind=match.kind,
        sdk_class=match.sdk_class,
        sdk_member=match.sdk_member,
        sdk_module_ir=new_ir,
        confidence=match.confidence,
        matched_by=match.matched_by,
    )


def _semantic_validation_error_for_diff(record: ChangeRecord, match: Match, base_text: str, diff: str) -> str:
    """Return a semantic validation error for a candidate diff, or ``''``."""
    if not _needs_semantic_validation(record):
        return ''
    ok, patched_or_err = _apply_diff_to_temp_text(diff, match, base_text)
    if not ok:
        return f'semantic validation could not apply diff to temporary target: {patched_or_err}'
    return _semantic_validation_error(record, match, patched_or_err)


def _semantic_validation_error(record: ChangeRecord, match: Match, sdk_text: str) -> str:
    """Return a semantic validation error for SDK source text, or ``''``."""
    if record.kind == 'method_param_added':
        return _method_param_order_error(record, match, sdk_text)
    return ''


def _needs_semantic_validation(record: ChangeRecord) -> bool:
    """Return whether a record needs post-diff semantic validation."""
    return record.kind == 'method_param_added'


def _apply_diff_to_temp_text(diff: str, match: Match, base_text: str) -> tuple[bool, str]:
    """Apply ``diff`` to a temporary copy of the target file and return its text."""
    target = Path(_relative_target_path(match.sdk_path))
    if target.is_absolute():
        return False, f'cannot validate non-repo-relative target path {target.as_posix()!r}'
    with tempfile.TemporaryDirectory(prefix='sdk-sync-validate-') as tmp:
        tmp_root = Path(tmp)
        target_path = tmp_root / target
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(base_text)
        try:
            proc = subprocess.run(
                ['git', 'apply', '--recount', '--unidiff-zero', '-C0', '-'],
                input=diff,
                text=True,
                capture_output=True,
                cwd=tmp_root,
                check=False,
            )
        except FileNotFoundError:
            return False, 'git executable not found'
        if proc.returncode != 0:
            return False, proc.stderr or '(no stderr)'
        try:
            return True, target_path.read_text()
        except FileNotFoundError:
            return False, f'target {target.as_posix()!r} disappeared while applying diff'


def _method_param_order_error(record: ChangeRecord, match: Match, sdk_text: str) -> str:
    """Return a method-parameter order validation error, or ``''``."""
    if match.kind != 'method' or match.sdk_member is None:
        return 'semantic parameter order validation requires a matched SDK method'
    payload = record.new or {}
    param = payload.get('param') or {}
    name = param.get('name') if isinstance(param, dict) else None
    params = payload.get('params') or []
    stub_order = [p.get('name') for p in params if isinstance(p, dict) and isinstance(p.get('name'), str)]
    if not isinstance(name, str) or not stub_order:
        return ''
    try:
        from .ir import extract_from_text

        ir = extract_from_text(sdk_text, str(match.sdk_path), is_sdk=False)
    except SyntaxError as exc:
        return f'semantic parameter order validation could not parse patched SDK file: {exc}'
    if ir.api_class is None or ir.api_class.name != match.sdk_class:
        return f'semantic parameter order validation could not find SDK class {match.sdk_class}'
    method = next((m for m in ir.api_class.methods if m.name == match.sdk_member), None)
    if method is None:
        return f'semantic parameter order validation could not find SDK method {match.sdk_member}'
    sdk_order = [p.name for p in method.params]
    if name not in sdk_order:
        return f'semantic parameter order validation did not find added parameter {name!r} in SDK signature'
    stub_names = set(stub_order)
    expected = [p for p in stub_order if p in sdk_order]
    actual = [p for p in sdk_order if p in stub_names]
    if actual != expected:
        return (
            f'semantic parameter order validation failed for {match.sdk_class}.{match.sdk_member}: '
            f'expected shared stub order {expected}, got {actual}'
        )
    return ''


def _looks_like_diff(diff: str) -> bool:
    """Cheap structural sanity check for a unified diff.

    ``git apply --check`` rejects empty or header-only payloads with a noisy
    ``No valid patches in input`` error. The dispatcher already treats a
    truly-empty LLM reply as "already in sync"; this predicate extends the
    same handling to the in-between case where the LLM returned a couple of
    lines that happen to contain ``---`` but no actual hunk, sparing us a
    pointless ``git apply`` round-trip and a misleading rejection log line.

    A minimal valid unified diff requires:

    1. ``--- `` and ``+++ `` file headers (anywhere — `git apply` tolerates
       leading text);
    2. at least one ``@@`` hunk header;
    3. at least one body line starting with ``+`` or ``-`` that is *not*
       another file header.

    :param diff: Cleaned LLM diff text (post-fence-strip).
    :return: ``True`` only if all three structural elements are present.
    """
    if not diff.strip():
        return False
    if '\n--- ' not in '\n' + diff or '\n+++ ' not in '\n' + diff:
        return False
    if '\n@@' not in '\n' + diff:
        return False
    for line in diff.splitlines():
        if line.startswith(('+++', '---')):
            continue
        if line.startswith(('+', '-')):
            return True
    return False


def _normalize_diff_paths(diff: str, match: Match) -> str:
    """Canonicalize unified-diff file headers to ``a/<target>`` / ``b/<target>``.

    LLMs often emit ``--- wxc_sdk/...`` headers. ``git apply`` strips one
    path component by default, so those otherwise valid repo-root paths become
    ``telephony/...`` and fail. This normalizes all accepted spellings to the
    canonical ``a/``/``b/`` form and rejects patches that touch any other file.
    """
    target = _relative_target_path(match.sdk_path)
    raw_lines = diff.splitlines()
    lines: list[str] = []
    i = 0
    while i < len(raw_lines):
        old_header = re.match(r'^(---) ([^\t ]+)(.*)$', raw_lines[i])
        new_header = re.match(r'^(\+\+\+) ([^\t ]+)(.*)$', raw_lines[i + 1]) if i + 1 < len(raw_lines) else None
        has_hunk_after_headers = i + 2 < len(raw_lines) and raw_lines[i + 2].startswith('@@')
        if old_header is None or new_header is None or not has_hunk_after_headers:
            lines.append(raw_lines[i])
            i += 1
            continue
        lines.append(_normalize_diff_header(old_header, target))
        lines.append(_normalize_diff_header(new_header, target))
        i += 2
    normalized = '\n'.join(lines)
    if diff.endswith('\n'):
        normalized += '\n'
    return normalized


def _normalize_diff_header(match: re.Match[str], target: str) -> str:
    """Normalize one file-header line from a paired unified-diff header."""
    prefix, raw_path, suffix = match.groups()
    if raw_path == '/dev/null':
        return f'{prefix} {raw_path}{suffix}'
    if not _diff_path_matches_target(raw_path, target):
        raise ValueError(f'diff touches unexpected path {raw_path!r}; expected {target!r}')
    side = 'a' if prefix == '---' else 'b'
    return f'{prefix} {side}/{target}{suffix}'


def _relative_target_path(path: Path) -> str:
    """Return a repo-root relative path for diff-header validation."""
    try:
        return path.resolve().relative_to(_REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _diff_path_matches_target(raw_path: str, target: str) -> bool:
    """Return whether a model-produced diff path unambiguously names target."""
    path = raw_path
    if path.startswith(('a/', 'b/')):
        path = path[2:]
    if path == target:
        return True
    # Accept package-relative paths such as ``telephony/forwarding.py`` for
    # target ``wxc_sdk/telephony/forwarding.py``. Require a slash so bare
    # basenames don't accidentally match multiple SDK modules.
    return '/' in path and target.endswith(f'/{path}')


def _should_retry_llm_diff(err: str) -> bool:
    """Return ``True`` for git diagnostics that a fresh-context retry may fix."""
    return 'patch does not apply' in err or 'patch failed:' in err


def _git_apply_check(diff: str) -> tuple[bool, str]:
    """Run ``git apply --check`` against a diff string.

    ``--recount`` is on because LLMs routinely emit hunk headers with wrong
    line totals (e.g. ``@@ -141,7 +141,8 @@`` when the hunk actually contains
    5/6 lines). ``--recount`` ignores the header counts and infers them from
    the hunk body. ``--unidiff-zero`` keeps zero-context diffs valid. Combined
    with git's built-in fuzzy line-number matching, this absorbs the most
    common LLM diff quirks without sacrificing the content-correctness check.

    :param diff: Unified diff text.
    :return: ``(ok, stderr)``. ``ok`` is ``True`` only if git considers the
        diff applicable cleanly. ``stderr`` carries git's diagnostic for
        rejected diffs so callers can surface the real reason; for an empty
        diff it is ``'empty diff'``.
    """
    if not diff.strip():
        return False, 'empty diff'
    return _run_git_apply(['git', 'apply', '--check', '--recount', '--unidiff-zero', '-C0', '-'], diff)


def _git_apply(diff: str) -> tuple[bool, str]:
    """Run ``git apply`` against a diff string and modify the working tree.

    Uses the same ``--recount --unidiff-zero`` combination as
    :func:`_git_apply_check` so what passes the check also applies.

    :param diff: Unified diff text (presumed already validated via
        :func:`_git_apply_check`).
    :return: ``(ok, stderr)`` — same convention as :func:`_git_apply_check`.
    """
    return _run_git_apply(['git', 'apply', '--recount', '--unidiff-zero', '-C0', '-'], diff)


def _run_git_apply(cmd: list[str], diff: str) -> tuple[bool, str]:
    """Invoke a ``git apply`` (or ``--check``) subprocess.

    :param cmd: The full argv to run, ending in ``'-'`` so the diff is read
        from stdin.
    :param diff: Diff text fed to stdin.
    :return: ``(ok, stderr)``. ``ok`` is ``True`` iff the command exits 0.
        ``stderr`` is git's diagnostic output (or ``'git executable not
        found'`` when the binary is missing).
    """
    try:
        proc = subprocess.run(cmd, input=diff, text=True, capture_output=True, cwd=_REPO_ROOT, check=False)
    except FileNotFoundError:
        return False, 'git executable not found'
    return proc.returncode == 0, proc.stderr


#: Directory where rejected LLM diffs are dumped for post-mortem inspection.
#: Sits beside the dispatcher module so the path is stable regardless of the
#: caller's working directory. Excluded via the repo-root ``.gitignore``.
_REJECTED_DIR = Path(__file__).resolve().parent / '.rejected'


def _flatten_git_err(err: str) -> str:
    """Collapse git's multi-line stderr to a single readable line.

    The end-of-run ``sync_report.md`` renders ``Outcome.detail`` on one bullet
    line, and the verbose console log line is also single-line. Newlines
    become ``\\n``, runs of whitespace are squeezed, and the result is
    truncated so a chatty error doesn't dominate the report.

    :param err: Raw stderr text from a ``git apply`` invocation.
    :return: A single-line, length-bounded representation.
    """
    flat = re.sub(r'\s+', ' ', err.replace('\n', '\\n')).strip()
    if len(flat) > 400:
        flat = flat[:397] + '...'
    return flat or '(no stderr)'


def _dump_rejected(record: ChangeRecord, match: Match, diff: str, err: str) -> None:
    """Write the rejected diff plus git's error to ``.rejected/`` for later inspection.

    Failures are intentionally swallowed (with a single warning line) so that
    a transient I/O problem in this debug aid never aborts the sync run.

    :param record: The change record whose diff was rejected.
    :param match: The resolved SDK target the diff was meant to patch.
    :param diff: The rejected unified-diff text.
    :param err: Stderr from ``git apply --check`` (or ``git apply``).
    """
    try:
        _REJECTED_DIR.mkdir(parents=True, exist_ok=True)
        try:
            rel_target = str(match.sdk_path.relative_to(_REPO_ROOT))
        except ValueError:
            rel_target = str(match.sdk_path)
        target_full = f'{rel_target}::{match.sdk_class}.{match.sdk_member or ""}'
        timestamp = time.strftime('%Y%m%dT%H%M%S')
        safe_qual = re.sub(r'[^A-Za-z0-9_]+', '_', record.qualname)
        safe_target = re.sub(r'[^A-Za-z0-9_]+', '_', target_full)
        filename = f'{timestamp}__{record.kind}__{safe_qual}__{safe_target}.diff'
        # Keep filenames within typical filesystem limits.
        if len(filename) > 240:
            filename = filename[:240] + '.diff'
        path = _REJECTED_DIR / filename
        indented_err = '\n'.join(f'#           {line}' for line in err.splitlines() or ['(no stderr)'])
        header = (
            f'# record:   {record.kind} {record.qualname}\n'
            f'# target:   {target_full}\n'
            f'# git err:\n{indented_err}\n'
            f'# ---\n'
        )
        path.write_text(header + diff)
    except OSError as exc:
        print(f'[llm] could not dump rejected diff: {exc}')

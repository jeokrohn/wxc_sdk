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

import subprocess
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
    """

    dry_run: bool = False
    use_llm: bool = True


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
        return _try_llm(record, match, config, pending_writes, fallback_reason=result.reason)

    if not config.use_llm:
        return Outcome(record, match, 'punted_patcher_refused', detail='requires LLM but disabled')
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
        diff = _llm.propose_diff(record, match, sdk_text)
    except _llm.LLMError as exc:
        return Outcome(record, match, 'punted_llm_unavailable', detail=f'{fallback_reason} | LLM: {exc}')
    if not _git_apply_check(diff):
        return Outcome(record, match, 'punted_diff_rejected', detail=fallback_reason, diff=diff)
    if config.dry_run:
        return Outcome(record, match, 'dry_run_pending', detail=fallback_reason, diff=diff)
    if not _git_apply(diff):
        return Outcome(record, match, 'punted_diff_rejected', detail='applied check passed but apply failed', diff=diff)
    # After a successful git apply, the on-disk file is now the source of
    # truth — drop any stale entry in pending_writes so a later trivial
    # patch on the same file re-reads the freshly applied text.
    if pending_writes is not None and match.sdk_path in pending_writes:
        del pending_writes[match.sdk_path]
    return Outcome(record, match, 'applied_llm', detail='LLM patch applied', diff=diff)


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

    new_ir = extract_from_text(new_text, str(match.sdk_path))
    return Match(
        sdk_path=match.sdk_path,
        kind=match.kind,
        sdk_class=match.sdk_class,
        sdk_member=match.sdk_member,
        sdk_module_ir=new_ir,
        confidence=match.confidence,
        matched_by=match.matched_by,
    )


def _git_apply_check(diff: str) -> bool:
    """Run ``git apply --check`` against a diff string.

    :param diff: Unified diff text.
    :return: ``True`` if git considers the diff applicable cleanly; ``False``
        for empty diffs and any non-zero exit from git.
    """
    if not diff.strip():
        return False
    return _run_git_apply(['git', 'apply', '--check', '--unidiff-zero', '-'], diff)


def _git_apply(diff: str) -> bool:
    """Run ``git apply`` against a diff string and modify the working tree.

    :param diff: Unified diff text (presumed already validated via
        :func:`_git_apply_check`).
    :return: ``True`` on a clean apply, ``False`` otherwise.
    """
    return _run_git_apply(['git', 'apply', '--unidiff-zero', '-'], diff)


def _run_git_apply(cmd: list[str], diff: str) -> bool:
    """Invoke a ``git apply`` (or ``--check``) subprocess.

    :param cmd: The full argv to run, ending in ``'-'`` so the diff is read
        from stdin.
    :param diff: Diff text fed to stdin.
    :return: ``True`` if the command exits 0. Returns ``False`` if git is
        missing (``FileNotFoundError``) — the caller still wants to know.
    """
    try:
        proc = subprocess.run(cmd, input=diff, text=True, capture_output=True, cwd=_REPO_ROOT, check=False)
    except FileNotFoundError:
        return False
    return proc.returncode == 0

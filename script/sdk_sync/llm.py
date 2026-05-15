"""
LLM step: shell out to a local coding-agent CLI to propose a unified diff.

The contract with the CLI is intentionally strict:

- **Input** — a structured prompt describing the stub change plus the
  matched SDK file's current contents.
- **Output** — a single unified diff (``--- a/<path>``/``+++ b/<path>``)
  applicable from the repo root via ``git apply``. No prose, no fences.

Why subprocess the CLI rather than calling a model SDK directly:

- The maintainer's existing CLI session handles auth and billing.
  Contributors should not need to set API-key environment variables just to
  run ``make sync-stubs``.
- A subprocess boundary is trivial to mock in tests by monkeypatching
  :func:`subprocess.run`.
- The rest of the pipeline stays independent of the selected CLI backend.

The dispatcher catches :class:`LLMError` and records a punt; the patch is
never blindly applied — the dispatcher first runs ``git apply --check`` so a
bad diff cannot land.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from .differ import ChangeRecord
from .matcher import Match

# Repo root is three levels above this file: script/sdk_sync/llm.py
# → script/sdk_sync → script → repo root.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# System prompt passed to every CLI invocation. Pins the output
# contract (unified diff only, no prose) and forbids edits that would break
# SDK-side invariants (validator blocks, single-quote style, 120-char lines).
_SYSTEM_CONSTRAINTS = (
    'You are applying a single change from an auto-generated OpenAPI stub into a '
    'hand-maintained Python SDK. Output ONLY a unified diff with `---`/`+++` headers '
    'relative to the repo root. No prose, no code fences. Preserve `#:` doc-comments. '
    'Do not modify `@field_validator` or `@model_validator` blocks. Use single quotes. '
    'Respect a 120-character line limit. Make the smallest change required.'
)


class LLMError(RuntimeError):
    """Raised when the selected LLM CLI is unavailable, fails, or returns garbage.

    The dispatcher catches this and records a ``punted_llm_unavailable``
    outcome so the rest of the run can continue.
    """


@dataclass
class LLMRequest:
    """Bundle of inputs assembled before invoking the LLM.

    Currently exposed mainly for testability; the public API
    (:func:`propose_diff`) is the function callers normally use.

    :param prompt: The fully rendered prompt string.
    :param record: The originating :class:`ChangeRecord`.
    :param match: The resolved SDK target.
    """

    prompt: str
    record: ChangeRecord
    match: Match


def render_prompt(record: ChangeRecord, match: Match, sdk_text: str) -> str:
    """Build the prompt that will be piped to the selected CLI.

    Sections:

    - Headers identifying the change (kind, qualname, notes).
    - Headers identifying the SDK target (file, class, member).
    - ``OLD`` / ``NEW`` JSON blobs of the change payload.
    - The current SDK file content as a Python code fence.
    - A trailing instruction reiterating the unified-diff contract.

    :param record: The change record to apply.
    :param match: The resolved SDK target.
    :param sdk_text: Current contents of the SDK file.
    :return: A single prompt string ready to feed via stdin to the CLI.
    """
    rel_path = _relative_sdk_path(match.sdk_path)
    parts = [
        f'STUB CHANGE: {record.kind}',
        f'STUB QUALNAME: {record.qualname}',
        f'STUB NOTES: {", ".join(record.notes) if record.notes else "(none)"}',
        '',
        f'TARGET SDK FILE: {rel_path}',
        f'TARGET CLASS: {match.sdk_class}',
        f'TARGET MEMBER: {match.sdk_member or "(class-level)"}',
        '',
        'OLD (stub side, before regeneration):',
        '```json',
        json.dumps(record.old, indent=2, default=str) if record.old else '(null)',
        '```',
        '',
        'NEW (stub side, after regeneration):',
        '```json',
        json.dumps(record.new, indent=2, default=str) if record.new else '(null)',
        '```',
        '',
        f'CURRENT SDK FILE CONTENT ({rel_path}):',
        '```python',
        sdk_text,
        '```',
        '',
        'Produce a unified diff that updates the SDK file to reflect the stub change.',
        'The diff MUST apply cleanly from the repo root via `git apply`.',
    ]
    return '\n'.join(parts)


def propose_diff(
    record: ChangeRecord,
    match: Match,
    sdk_text: str,
    *,
    timeout: float = 240.0,
    verbose: bool = False,
    print_prompts: bool = False,
) -> str:
    """Invoke a local LLM CLI and return the extracted unified diff.

    Codex CLI is preferred when available; otherwise we fall back to the
    legacy Claude CLI path. The selected runner returns assistant text, and
    this function strips any accidental code fences to leave a raw diff. The
    dispatcher applies ``git apply --check`` to the returned string before
    trusting it.

    :param record: The change record to apply.
    :param match: The resolved SDK target.
    :param sdk_text: Current contents of the SDK file.
    :param timeout: Maximum seconds to wait for the CLI to finish; raises
        :class:`LLMError` on timeout.
    :param verbose: When ``True``, print ``[llm] calling <backend> (...)``
        before invoking the CLI and ``[llm] <backend> returned in Xs (...)``
        once it returns. Default keeps the call silent.
    :param print_prompts: When ``True`` and ``verbose`` is also ``True``, print
        the full backend prompt before invoking the CLI.
    :return: Unified diff text, guaranteed to end with a newline.
    :raises LLMError: If the CLI is missing, returns a non-zero exit code,
        times out, or emits non-JSON output.
    """
    prompt = render_prompt(record, match, sdk_text)
    backend = _select_backend()
    runner = _run_codex if backend == 'codex' else _run_claude
    result = runner(prompt, match, timeout=timeout, verbose=verbose, print_prompts=print_prompts)
    return _extract_unified_diff(result)


def _select_backend() -> str:
    """Return the preferred available CLI backend name.

    Codex is preferred because it is the current target CLI for this sync
    helper. Claude remains supported as a compatibility fallback for
    environments that have not migrated yet.
    """
    if shutil.which('codex') is not None:
        return 'codex'
    if shutil.which('claude') is not None:
        return 'claude'
    raise LLMError('neither `codex` nor `claude` CLI is on PATH; install Codex CLI to enable LLM-driven sync')


def _run_codex(prompt: str, match: Match, *, timeout: float, verbose: bool, print_prompts: bool) -> str:
    """Invoke ``codex exec`` and return the final assistant message.

    ``codex exec`` may print event/progress output to stdout. The
    ``--output-last-message`` file gives us a stable, prose-free place to read
    the model's final answer from before running the shared diff extraction.
    """
    full_prompt = f'{_SYSTEM_CONSTRAINTS}\n\n{prompt}'
    target = _relative_sdk_path(match.sdk_path)
    if verbose:
        print(f'[llm] calling codex (prompt: {len(full_prompt)} chars, target: {target})')
    if verbose and print_prompts:
        _print_prompt('codex', target, full_prompt)
    t0 = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='sdk-sync-codex-') as tmp:
        output_path = Path(tmp) / 'last-message.txt'
        try:
            proc = subprocess.run(
                [
                    'codex',
                    'exec',
                    '--cd',
                    str(_REPO_ROOT),
                    '--sandbox',
                    'read-only',
                    '--ephemeral',
                    '--color',
                    'never',
                    '--output-last-message',
                    str(output_path),
                    '-',
                ],
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True,
                cwd=_REPO_ROOT,
            )
        except subprocess.CalledProcessError as exc:
            raise LLMError(f'codex CLI failed (rc={exc.returncode}): {exc.stderr[:400]}') from exc
        except subprocess.TimeoutExpired as exc:
            raise LLMError(f'codex CLI timed out after {timeout}s') from exc
        if verbose:
            elapsed = time.monotonic() - t0
            print(f'[llm] codex returned in {elapsed:.1f}s (stdout: {len(proc.stdout)} bytes)')
        try:
            return output_path.read_text()
        except FileNotFoundError as exc:
            raise LLMError('codex CLI did not write the final message file') from exc


def _run_claude(prompt: str, match: Match, *, timeout: float, verbose: bool, print_prompts: bool) -> str:
    """Invoke ``claude -p`` and return the assistant text from its JSON output."""
    target = _relative_sdk_path(match.sdk_path)
    if verbose:
        print(f'[llm] calling claude (prompt: {len(prompt)} chars, target: {target})')
    if verbose and print_prompts:
        _print_prompt('claude', target, f'SYSTEM:\n{_SYSTEM_CONSTRAINTS}\n\nSTDIN:\n{prompt}')
    t0 = time.monotonic()
    try:
        proc = subprocess.run(
            ['claude', '-p', '--output-format', 'json', '--append-system-prompt', _SYSTEM_CONSTRAINTS],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise LLMError(f'claude CLI failed (rc={exc.returncode}): {exc.stderr[:400]}') from exc
    except subprocess.TimeoutExpired as exc:
        raise LLMError(f'claude CLI timed out after {timeout}s') from exc
    if verbose:
        elapsed = time.monotonic() - t0
        print(f'[llm] claude returned in {elapsed:.1f}s (stdout: {len(proc.stdout)} bytes)')
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise LLMError(f'claude CLI did not return valid JSON: {proc.stdout[:400]}') from exc
    return payload.get('result') or payload.get('text') or ''


def _print_prompt(backend: str, target: str, prompt: str) -> None:
    """Print a backend prompt with clear delimiters for verbose debugging."""
    print(f'[llm-prompt] begin {backend} target={target}')
    print(prompt)
    print(f'[llm-prompt] end {backend} target={target}')


def _extract_unified_diff(text: str) -> str:
    """Locate the unified diff block within the CLI's text payload.

    Some models occasionally wrap the diff in a ``​```diff` fence despite the
    system prompt forbidding it. We strip such fences, then trim any leading
    text before the first ``---`` header, and ensure a trailing newline so
    ``git apply`` is happy.

    :param text: Raw assistant-produced text.
    :return: A clean unified-diff string. Returns an empty-ish string if no
        ``---`` header is present (which the dispatcher will reject via
        ``git apply --check``).
    """
    fenced = re.search(r'```(?:diff|patch)?\n(.*?)```', text, re.DOTALL)
    body = fenced.group(1) if fenced else text
    body = body.strip()
    if not body.startswith('---'):
        m = re.search(r'^---.*', body, re.MULTILINE)
        if m:
            body = body[m.start() :]
    if not body.endswith('\n'):
        body += '\n'
    return body


def _relative_sdk_path(path: Path) -> str:
    """Express ``path`` relative to the repo root for prompt readability.

    :param path: Absolute SDK file path.
    :return: A repo-root-relative string (``"wxc_sdk/devices/__init__.py"``).
        Falls back to ``str(path)`` if the path isn't under the repo root.
    """
    try:
        return str(path.relative_to(_REPO_ROOT))
    except ValueError:
        return str(path)

"""
LLM step: shell out to the ``claude`` CLI to propose a unified diff.

The contract with the CLI is intentionally strict:

- **Input** — a structured prompt describing the stub change plus the
  matched SDK file's current contents.
- **Output** — a single unified diff (``--- a/<path>``/``+++ b/<path>``)
  applicable from the repo root via ``git apply``. No prose, no fences.

Why subprocess the CLI rather than calling the Anthropic SDK directly:

- The maintainer's existing ``claude`` CLI session handles auth and billing.
  Contributors should not need to set ``ANTHROPIC_API_KEY`` just to run
  ``make sync-stubs``.
- A subprocess boundary is trivial to mock in tests by monkeypatching
  :func:`subprocess.run`.
- We can swap the implementation later without touching the rest of the
  pipeline.

The dispatcher catches :class:`LLMError` and records a punt; the patch is
never blindly applied — the dispatcher first runs ``git apply --check`` so a
bad diff cannot land.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .differ import ChangeRecord
from .matcher import Match

# System prompt appended to every `claude -p` invocation. Pins the output
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
    """Raised when the ``claude`` CLI is unavailable, fails, or returns garbage.

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
    """Build the prompt that will be piped to ``claude -p``.

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


def propose_diff(record: ChangeRecord, match: Match, sdk_text: str, *, timeout: float = 180.0) -> str:
    """Invoke ``claude -p`` and return the extracted unified diff.

    The CLI is required to be on ``PATH``. The function reads its JSON output,
    extracts the ``result`` field (the assistant's text), and strips any
    accidental code fences to leave a raw diff. The dispatcher applies
    ``git apply --check`` to the returned string before trusting it.

    :param record: The change record to apply.
    :param match: The resolved SDK target.
    :param sdk_text: Current contents of the SDK file.
    :param timeout: Maximum seconds to wait for the CLI to finish; raises
        :class:`LLMError` on timeout.
    :return: Unified diff text, guaranteed to end with a newline.
    :raises LLMError: If the CLI is missing, returns a non-zero exit code,
        times out, or emits non-JSON output.
    """
    if shutil.which('claude') is None:
        raise LLMError('the `claude` CLI is not on PATH; install Claude Code to enable LLM-driven sync')
    prompt = render_prompt(record, match, sdk_text)
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
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise LLMError(f'claude CLI did not return valid JSON: {proc.stdout[:400]}') from exc
    result = payload.get('result') or payload.get('text') or ''
    return _extract_unified_diff(result)


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
        repo_root = Path(__file__).resolve().parent.parent.parent
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)

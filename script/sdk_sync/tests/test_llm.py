# mypy: disable-error-code="attr-defined"
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, cast

import pytest

from script.sdk_sync import llm
from script.sdk_sync.differ import ChangeRecord
from script.sdk_sync.matcher import Match


def _record() -> ChangeRecord:
    return ChangeRecord(
        kind='type_changed',
        qualname='Demo.value',
        old={'annotation': 'str'},
        new={'annotation': 'int'},
        severity='review',
        notes=('field annotation changed',),
    )


def _match(tmp_path: Path) -> Match:
    return Match(
        sdk_path=tmp_path / 'wxc_sdk' / 'demo.py',
        kind='model_field',
        sdk_class='Demo',
        sdk_member='value',
        sdk_module_ir=cast(Any, None),
        confidence=1.0,
        matched_by='exact',
    )


def _diff(path: str = 'wxc_sdk/demo.py') -> str:
    return f'--- a/{path}\n+++ b/{path}\n@@ -1,2 +1,2 @@\n class Demo:\n-    value: str\n+    value: int\n'


def test_propose_diff_prefers_codex_when_available(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    calls: list[dict[str, Any]] = []

    def fake_which(name: str) -> str | None:
        return f'/usr/bin/{name}' if name in {'codex', 'claude'} else None

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append({'cmd': cmd, 'kwargs': kwargs})
        output_path = Path(cmd[cmd.index('--output-last-message') + 1])
        output_path.write_text(_diff())
        return subprocess.CompletedProcess(cmd, 0, stdout='ignore this stdout', stderr='')

    monkeypatch.setattr(llm.shutil, 'which', fake_which)
    monkeypatch.setattr(llm.subprocess, 'run', fake_run)

    diff = llm.propose_diff(_record(), _match(tmp_path), 'class Demo:\n    value: str\n')

    assert diff == _diff()
    assert len(calls) == 1
    cmd = calls[0]['cmd']
    assert cmd[:2] == ['codex', 'exec']
    assert cmd[-1] == '-'
    assert cmd[cmd.index('--sandbox') + 1] == 'read-only'
    assert '--ask-for-approval' not in cmd
    assert '--ephemeral' in cmd
    assert calls[0]['kwargs']['input'].startswith(llm._SYSTEM_CONSTRAINTS)
    assert 'STUB CHANGE: type_changed' in calls[0]['kwargs']['input']


def test_propose_diff_falls_back_to_claude_when_codex_missing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    calls: list[dict[str, Any]] = []

    def fake_which(name: str) -> str | None:
        return '/usr/bin/claude' if name == 'claude' else None

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append({'cmd': cmd, 'kwargs': kwargs})
        stdout = json.dumps({'result': _diff()})
        return subprocess.CompletedProcess(cmd, 0, stdout=stdout, stderr='')

    monkeypatch.setattr(llm.shutil, 'which', fake_which)
    monkeypatch.setattr(llm.subprocess, 'run', fake_run)

    diff = llm.propose_diff(_record(), _match(tmp_path), 'class Demo:\n    value: str\n')

    assert diff == _diff()
    assert len(calls) == 1
    cmd = calls[0]['cmd']
    assert cmd[:2] == ['claude', '-p']
    assert cmd[cmd.index('--append-system-prompt') + 1] == llm._SYSTEM_CONSTRAINTS


def test_propose_diff_errors_when_no_cli_available(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(llm.shutil, 'which', lambda name: None)

    with pytest.raises(llm.LLMError, match='neither `codex` nor `claude` CLI is on PATH'):
        llm.propose_diff(_record(), _match(tmp_path), 'class Demo:\n    value: str\n')


def test_codex_failure_mentions_selected_backend(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        raise subprocess.CalledProcessError(2, cmd, stderr='not logged in')

    monkeypatch.setattr(llm.shutil, 'which', lambda name: '/usr/bin/codex' if name == 'codex' else None)
    monkeypatch.setattr(llm.subprocess, 'run', fake_run)

    with pytest.raises(llm.LLMError, match='codex CLI failed'):
        llm.propose_diff(_record(), _match(tmp_path), 'class Demo:\n    value: str\n')


def test_codex_prints_prompt_only_when_verbose_and_requested(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        output_path = Path(cmd[cmd.index('--output-last-message') + 1])
        output_path.write_text(_diff())
        return subprocess.CompletedProcess(cmd, 0, stdout='', stderr='')

    monkeypatch.setattr(llm.shutil, 'which', lambda name: '/usr/bin/codex' if name == 'codex' else None)
    monkeypatch.setattr(llm.subprocess, 'run', fake_run)

    llm.propose_diff(
        _record(),
        _match(tmp_path),
        'class Demo:\n    value: str\n',
        verbose=False,
        print_prompts=True,
    )
    assert '[llm-prompt]' not in capsys.readouterr().out

    llm.propose_diff(
        _record(),
        _match(tmp_path),
        'class Demo:\n    value: str\n',
        verbose=True,
        print_prompts=True,
    )
    out = capsys.readouterr().out
    assert '[llm-prompt] begin codex target=' in out
    assert llm._SYSTEM_CONSTRAINTS in out
    assert 'STUB CHANGE: type_changed' in out
    assert '[llm-prompt] end codex target=' in out


def test_claude_prints_system_and_stdin_prompts(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps({'result': _diff()}), stderr='')

    monkeypatch.setattr(llm.shutil, 'which', lambda name: '/usr/bin/claude' if name == 'claude' else None)
    monkeypatch.setattr(llm.subprocess, 'run', fake_run)

    llm.propose_diff(
        _record(),
        _match(tmp_path),
        'class Demo:\n    value: str\n',
        verbose=True,
        print_prompts=True,
    )

    out = capsys.readouterr().out
    assert '[llm-prompt] begin claude target=' in out
    assert f'SYSTEM:\n{llm._SYSTEM_CONSTRAINTS}' in out
    assert 'STDIN:\nSTUB CHANGE: type_changed' in out
    assert '[llm-prompt] end claude target=' in out


def test_extract_unified_diff_strips_fence_and_leading_prose() -> None:
    assert llm._extract_unified_diff(f'Here is the patch:\n```diff\n{_diff()}```') == _diff()

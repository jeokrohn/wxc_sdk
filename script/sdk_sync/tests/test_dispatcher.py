# mypy: disable-error-code="attr-defined"
from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import pytest

from script.sdk_sync import dispatcher
from script.sdk_sync.differ import ChangeRecord
from script.sdk_sync.matcher import Match


def _record() -> ChangeRecord:
    return ChangeRecord(
        kind='type_changed',
        qualname='Demo.value',
        old={'annotation': 'str'},
        new={'annotation': 'int'},
        severity='review',
    )


def _match(path: Path) -> Match:
    return Match(
        sdk_path=path,
        kind='model_field',
        sdk_class='Demo',
        sdk_member='value',
        sdk_module_ir=cast(Any, None),
        confidence=1.0,
        matched_by='exact',
    )


def _diff(path: str) -> str:
    return f'--- {path}\n+++ {path}\n@@ -1,2 +1,2 @@\n class Demo:\n-    value: str\n+    value: int\n'


def test_normalize_diff_paths_adds_git_prefixes_for_repo_root_path() -> None:
    match = _match(dispatcher._REPO_ROOT / 'wxc_sdk' / 'demo.py')

    diff = dispatcher._normalize_diff_paths(_diff('wxc_sdk/demo.py'), match)

    assert diff.startswith('--- a/wxc_sdk/demo.py\n+++ b/wxc_sdk/demo.py\n')


def test_normalize_diff_paths_accepts_package_relative_path() -> None:
    match = _match(dispatcher._REPO_ROOT / 'wxc_sdk' / 'telephony' / 'forwarding.py')

    diff = dispatcher._normalize_diff_paths(_diff('telephony/forwarding.py'), match)

    assert diff.startswith('--- a/wxc_sdk/telephony/forwarding.py\n+++ b/wxc_sdk/telephony/forwarding.py\n')


def test_normalize_diff_paths_rejects_unexpected_file() -> None:
    match = _match(dispatcher._REPO_ROOT / 'wxc_sdk' / 'demo.py')

    with pytest.raises(ValueError, match='unexpected path'):
        dispatcher._normalize_diff_paths(_diff('wxc_sdk/other.py'), match)


def test_normalize_diff_paths_leaves_header_like_hunk_content_alone() -> None:
    match = _match(dispatcher._REPO_ROOT / 'wxc_sdk' / 'demo.py')
    diff = (
        '--- wxc_sdk/demo.py\n'
        '+++ wxc_sdk/demo.py\n'
        '@@ -1,3 +1,3 @@\n'
        ' class Demo:\n'
        '--- not a file header\n'
        '+++ also not a file header\n'
    )

    normalized = dispatcher._normalize_diff_paths(diff, match)

    assert '--- not a file header\n+++ also not a file header\n' in normalized


def test_try_llm_retries_patch_that_does_not_apply(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    sdk_path = tmp_path / 'demo.py'
    sdk_path.write_text('class Demo:\n    value: str\n')
    match = _match(sdk_path)
    proposed = iter(['bad diff', 'good diff'])
    calls: list[dict[str, Any]] = []

    def fake_propose_diff(*args: Any, **kwargs: Any) -> str:
        calls.append(kwargs)
        return next(proposed)

    checks = iter(
        [
            (False, 'error: patch failed: demo.py:1\nerror: demo.py: patch does not apply\n'),
            (True, ''),
        ]
    )

    monkeypatch.setattr(dispatcher._llm, 'propose_diff', fake_propose_diff)
    monkeypatch.setattr(dispatcher, '_looks_like_diff', lambda diff: True)
    monkeypatch.setattr(dispatcher, '_normalize_diff_paths', lambda diff, match: diff)
    monkeypatch.setattr(dispatcher, '_git_apply_check', lambda diff: next(checks))

    outcome = dispatcher._try_llm(
        _record(),
        match,
        dispatcher.DispatchConfig(dry_run=True, llm_timeout=12.5),
        pending_writes={},
    )

    assert outcome.status == 'dry_run_pending'
    assert outcome.diff == 'good diff'
    assert len(calls) == 2
    assert calls[0]['timeout'] == 12.5
    assert calls[1]['rejected_diff'] == 'bad diff'
    assert 'patch does not apply' in calls[1]['git_error']


def test_git_apply_check_allows_reduced_context(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_run_git_apply(cmd: list[str], diff: str) -> tuple[bool, str]:
        captured['cmd'] = cmd
        captured['diff'] = diff
        return True, ''

    monkeypatch.setattr(dispatcher, '_run_git_apply', fake_run_git_apply)

    ok, err = dispatcher._git_apply_check('diff text')

    assert ok
    assert err == ''
    assert captured['cmd'] == ['git', 'apply', '--check', '--recount', '--unidiff-zero', '-C0', '-']

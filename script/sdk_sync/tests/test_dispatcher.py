# mypy: disable-error-code="attr-defined"
from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any, cast

import pytest

from script.sdk_sync import dispatcher
from script.sdk_sync.differ import ChangeRecord
from script.sdk_sync.ir import extract_from_text
from script.sdk_sync.matcher import Match


def _record() -> ChangeRecord:
    return ChangeRecord(
        kind='type_changed',
        qualname='Demo.value',
        old={'annotation': 'str'},
        new={'annotation': 'int'},
        severity='review',
    )


def _param_added_record() -> ChangeRecord:
    return ChangeRecord(
        kind='method_param_added',
        qualname='DemoApi.call',
        old=None,
        new={
            'param': {'name': 'b', 'annotation': 'str', 'default': 'None', 'kind': 'positional'},
            'params': [
                {'name': 'a', 'annotation': 'str', 'default': 'None', 'kind': 'positional'},
                {'name': 'b', 'annotation': 'str', 'default': 'None', 'kind': 'positional'},
                {'name': 'c', 'annotation': 'str', 'default': 'None', 'kind': 'positional'},
            ],
            'insert_after': 'a',
            'insert_before': 'c',
        },
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


def _method_match() -> Match:
    return Match(
        sdk_path=dispatcher._REPO_ROOT / 'wxc_sdk' / 'demo.py',
        kind='method',
        sdk_class='DemoApi',
        sdk_member='call',
        sdk_module_ir=cast(Any, None),
        confidence=1.0,
        matched_by='exact',
    )


def _diff(path: str) -> str:
    return f'--- {path}\n+++ {path}\n@@ -1,2 +1,2 @@\n class Demo:\n-    value: str\n+    value: int\n'


def _bad_param_order_diff() -> str:
    return (
        '--- a/wxc_sdk/demo.py\n'
        '+++ b/wxc_sdk/demo.py\n'
        '@@ -1,4 +1,4 @@\n'
        ' from wxc_sdk.api_child import ApiChild\n'
        " class DemoApi(ApiChild, base='x'):\n"
        '-    def call(self, a: str = None, c: str = None):\n'
        '+    def call(self, a: str = None, c: str = None, b: str = None):\n'
        '         pass\n'
    )


def _demo_api_source() -> str:
    return (
        'from wxc_sdk.api_child import ApiChild\n'
        "class DemoApi(ApiChild, base='x'):\n"
        '    def call(self, a: str = None, c: str = None):\n'
        '        pass\n'
    )


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


def test_try_llm_rejects_method_param_added_with_wrong_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict[str, Any]] = []

    def fake_propose_diff(*args: Any, **kwargs: Any) -> str:
        calls.append(kwargs)
        return _bad_param_order_diff()

    monkeypatch.setattr(dispatcher._llm, 'propose_diff', fake_propose_diff)
    monkeypatch.setattr(dispatcher, '_git_apply_check', lambda diff: (True, ''))

    match = _method_match()
    outcome = dispatcher._try_llm(
        _param_added_record(),
        match,
        dispatcher.DispatchConfig(dry_run=True),
        pending_writes={match.sdk_path: _demo_api_source()},
    )

    assert outcome.status == 'punted_diff_rejected'
    assert 'retry semantic validation' in outcome.detail
    assert 'expected shared stub order' in outcome.detail
    assert len(calls) == 2
    assert 'semantic parameter order validation failed' in calls[1]['git_error']


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


def test_dispatch_doc_comment_divergence_punts_when_llm_disabled(tmp_path: Path) -> None:
    """Do not deterministically overwrite a hand-diverged SDK doc-comment.

    :param tmp_path: Temporary directory used for the synthetic SDK file.
    :type tmp_path: pathlib.Path
    :return: Nothing.
    :rtype: None
    """
    sdk_text = textwrap.dedent("""\
    from wxc_sdk.base import SafeEnum as Enum


    class OwnerType(str, Enum):
        #: Hand-authored owner text.
        call_queue = 'CALL_QUEUE'
    """)
    sdk_path = tmp_path / 'common.py'
    sdk_path.write_text(sdk_text)
    record = ChangeRecord(
        kind='docstring_changed',
        qualname='NumberOwnerType.call_queue',
        old={'doc_comment': 'Old owner text.'},
        new={'doc_comment': 'New owner text.'},
        severity='trivial',
    )
    match = Match(
        sdk_path=sdk_path,
        kind='enum_value',
        sdk_class='OwnerType',
        sdk_member='call_queue',
        sdk_module_ir=extract_from_text(sdk_text, str(sdk_path)),
        confidence=0.95,
        matched_by='structural-enum',
    )

    outcome = dispatcher.dispatch(
        record,
        match,
        dispatcher.DispatchConfig(dry_run=True, use_llm=False),
        pending_writes={},
    )

    assert outcome.status == 'punted_patcher_refused'
    assert 'diverged from old stub' in outcome.detail

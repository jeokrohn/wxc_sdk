"""Smoke tests for driver-side scoping helpers and main() flag wiring."""
# mypy: disable-error-code="attr-defined"

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest

from script.sdk_sync import dispatcher as _dispatcher
from script.sdk_sync import driver as _driver
from script.sdk_sync.differ import ChangeRecord
from script.sdk_sync.ir import ApiClassIR, ModuleIR
from script.sdk_sync.matcher import Match


def _make_match(sdk_class: str, sdk_member: str, confidence: float = 1.0) -> Match:
    """Build a minimal :class:`Match` for rename-detection unit tests."""
    empty_ir = ModuleIR(
        path='<test>',
        models=(),
        enums=(),
        api_class=ApiClassIR(name=sdk_class, base='', methods=(), lineno=1, end_lineno=1),
        source_sha='',
        source_text='',
    )
    return Match(
        sdk_path=Path('wxc_sdk/test_target.py'),
        kind='method',
        sdk_class=sdk_class,
        sdk_member=sdk_member,
        sdk_module_ir=empty_ir,
        confidence=confidence,
        matched_by='alias',
    )


def _make_record(kind: str, stub_class: str, stub_method: str) -> ChangeRecord:
    """Build a minimal :class:`ChangeRecord` matching the differ's qualname shape."""
    return ChangeRecord(
        kind=kind,
        qualname=f'{stub_class}.{stub_method}',
        old=None if kind == 'method_added' else {'name': stub_method},
        new=None if kind == 'method_removed' else {'name': stub_method},
        severity='review',
    )


def test_rename_detection_pairs_removed_with_added() -> None:
    target = _make_match('SupervisorApi', 'delete')
    matched: list[tuple[ChangeRecord, Match | None]] = [
        (_make_record('method_removed', 'FeaturesCallQueueApi', 'delete_a_supervisor'), target),
        (_make_record('method_added', 'FeaturesCallQueueApi', 'delete_call_queue_supervisor'), target),
    ]
    targets = _driver._detect_rename_targets(matched)
    detail = _driver._rename_supersedes(matched[0][0], matched[0][1], targets)
    assert detail is not None
    assert 'rename detected' in detail
    assert 'SupervisorApi.delete' in detail


def test_rename_detection_requires_same_stub_class() -> None:
    target = _make_match('SupervisorApi', 'delete')
    # method_removed in stub class A, method_added in stub class B → not a rename.
    matched: list[tuple[ChangeRecord, Match | None]] = [
        (_make_record('method_removed', 'FeaturesCallQueueApi', 'delete_a_supervisor'), target),
        (_make_record('method_added', 'FeaturesHuntGroupApi', 'delete_hunt_group_supervisor'), target),
    ]
    targets = _driver._detect_rename_targets(matched)
    assert _driver._rename_supersedes(matched[0][0], matched[0][1], targets) is None


def test_rename_detection_requires_full_confidence_on_both_sides() -> None:
    target_low = _make_match('SupervisorApi', 'delete', confidence=0.85)
    target_full = _make_match('SupervisorApi', 'delete', confidence=1.0)
    # Heuristic match on the added side: not eligible to suppress a removal.
    matched: list[tuple[ChangeRecord, Match | None]] = [
        (_make_record('method_removed', 'FeaturesCallQueueApi', 'delete_a_supervisor'), target_full),
        (_make_record('method_added', 'FeaturesCallQueueApi', 'delete_call_queue_supervisor'), target_low),
    ]
    targets = _driver._detect_rename_targets(matched)
    assert _driver._rename_supersedes(matched[0][0], matched[0][1], targets) is None
    # Symmetric: heuristic on the removed side also disqualifies.
    matched2: list[tuple[ChangeRecord, Match | None]] = [
        (_make_record('method_removed', 'FeaturesCallQueueApi', 'delete_a_supervisor'), target_low),
        (_make_record('method_added', 'FeaturesCallQueueApi', 'delete_call_queue_supervisor'), target_full),
    ]
    targets2 = _driver._detect_rename_targets(matched2)
    assert _driver._rename_supersedes(matched2[0][0], matched2[0][1], targets2) is None


def test_rename_detection_only_applies_to_method_removed() -> None:
    target = _make_match('SupervisorApi', 'delete')
    # method_added paired with method_added — never a rename pair, even if same target.
    record = _make_record('method_added', 'FeaturesCallQueueApi', 'delete_call_queue_supervisor')
    matched: list[tuple[ChangeRecord, Match | None]] = [(record, target)]
    targets = _driver._detect_rename_targets(matched)
    assert _driver._rename_supersedes(record, target, targets) is None


def test_rename_detection_skips_unmatched_removal() -> None:
    target = _make_match('SupervisorApi', 'delete')
    matched: list[tuple[ChangeRecord, Match | None]] = [
        (_make_record('method_removed', 'FeaturesCallQueueApi', 'delete_a_supervisor'), None),
        (_make_record('method_added', 'FeaturesCallQueueApi', 'delete_call_queue_supervisor'), target),
    ]
    targets = _driver._detect_rename_targets(matched)
    assert _driver._rename_supersedes(matched[0][0], matched[0][1], targets) is None


def test_resolve_stub_arg_literal_path() -> None:
    # A real file we already know exists in the working tree from CLAUDE.md.
    rel = 'open_api/generated/Webex-Suite/Webex-Calling/Webex-Cloud-Calling/All-APIs/call-controls-members_auto.py'
    assert _driver._resolve_stub_arg(rel) == [rel]


def test_resolve_stub_arg_bare_basename() -> None:
    resolved = _driver._resolve_stub_arg('call-controls-members_auto.py')
    assert len(resolved) == 1
    assert resolved[0].endswith('/call-controls-members_auto.py')
    assert resolved[0].startswith('open_api/generated/')


def test_resolve_stub_arg_glob() -> None:
    resolved = _driver._resolve_stub_arg('open_api/generated/**/call-controls-members_auto.py')
    assert len(resolved) == 1
    assert resolved[0].endswith('/call-controls-members_auto.py')


def test_resolve_stub_arg_missing_returns_empty() -> None:
    assert _driver._resolve_stub_arg('definitely-not-a-real-stub_auto.py') == []
    assert _driver._resolve_stub_arg('open_api/generated/**/__no_such_file__.py') == []


def test_main_unknown_stub_exits(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        _driver.main(['--dry-run', '--no-llm', '--stub', 'no_such_stub_auto.py'])
    assert exc.value.code != 0
    err = capsys.readouterr().err
    assert 'no_such_stub_auto.py' in err


def test_print_prompts_requires_verbose(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        _driver.main(['--dry-run', '--no-llm', '--print-prompts'])
    assert exc.value.code != 0
    assert '--print-prompts requires -v/--verbose' in capsys.readouterr().err


def test_print_prompts_reaches_dispatch_config(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_config(**kwargs: Any) -> object:
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(_driver._dispatcher, 'DispatchConfig', fake_config)
    monkeypatch.setattr(_driver, '_git_diff_name_only', lambda rev, scope: [])

    rc = _driver.main(['--dry-run', '--no-llm', '-v', '--print-prompts'])

    assert rc == 0
    assert captured == {
        'dry_run': True,
        'use_llm': False,
        'verbose': True,
        'print_prompts': True,
        'llm_timeout': 240.0,
    }


def test_llm_timeout_reaches_dispatch_config(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_config(**kwargs: Any) -> object:
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(_driver._dispatcher, 'DispatchConfig', fake_config)
    monkeypatch.setattr(_driver, '_git_diff_name_only', lambda rev, scope: [])

    rc = _driver.main(['--dry-run', '--no-llm', '--llm-timeout', '600'])

    assert rc == 0
    assert captured['llm_timeout'] == 600.0


def test_llm_timeout_must_be_positive(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        _driver.main(['--dry-run', '--no-llm', '--llm-timeout', '0'])
    assert exc.value.code != 0
    assert '--llm-timeout must be greater than zero' in capsys.readouterr().err


def test_main_only_filter_drops_everything(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Force discovery to return one known stub, then have --only filter it out.
    monkeypatch.setattr(
        _driver,
        '_git_diff_name_only',
        lambda rev, scope: ['open_api/generated/Shared/webhooks_auto.py'],
    )
    rc = _driver.main(['--dry-run', '--no-llm', '--only', '*__nope__*'])
    assert rc == 0
    assert 'No stub changes to sync.' in capsys.readouterr().out


def test_main_processes_new_stub_without_head_revision(monkeypatch: pytest.MonkeyPatch) -> None:
    existing_stub = (
        'open_api/generated/Webex-Suite/Webex-Calling/Webex-Cloud-Calling/All-APIs/call-controls-members_auto.py'
    )
    missing_stub = 'open_api/generated/__missing_new_stub_auto.py'
    old_ir = ModuleIR(path=existing_stub, models=(), enums=(), api_class=None, source_sha='', source_text='')
    new_ir = ModuleIR(
        path=existing_stub,
        models=(),
        enums=(),
        api_class=ApiClassIR(name='NewStubApi', base='', methods=(), lineno=1, end_lineno=1),
        source_sha='',
        source_text='',
    )
    record = ChangeRecord(
        kind='method_added',
        qualname='NewStubApi.list_new_stub_items',
        old=None,
        new={'name': 'list_new_stub_items'},
        severity='review',
    )
    captured: dict[str, Any] = {}

    def fake_git_show(path: str) -> str:
        raise subprocess.CalledProcessError(128, ['git', 'show', f'HEAD:{path}'])

    def fake_extract_from_text(source: str, path: str) -> ModuleIR:
        assert source == ''
        assert path == existing_stub
        return old_ir

    def fake_dispatch(
        rec: ChangeRecord,
        match: Match | None,
        config: _dispatcher.DispatchConfig,
        pending_writes: dict[Path, str] | None = None,
    ) -> _dispatcher.Outcome:
        captured.setdefault('dispatched', []).append((rec, match, pending_writes))
        return _dispatcher.Outcome(rec, match, 'already_in_sync', detail='processed new stub')

    def fake_write_report(
        outcomes: list[_dispatcher.Outcome],
        skipped: list[tuple[str, str]],
        args: Any,
    ) -> None:
        captured['outcomes'] = outcomes
        captured['skipped'] = skipped

    monkeypatch.setattr(_driver, '_git_diff_name_only', lambda rev, scope: [existing_stub, missing_stub])
    monkeypatch.setattr(_driver, '_git_show', fake_git_show)
    monkeypatch.setattr(_driver, 'extract_from_text', fake_extract_from_text)
    monkeypatch.setattr(_driver, 'extract', lambda path: new_ir)
    monkeypatch.setattr(_driver, 'diff_irs', lambda old, new: [record])
    monkeypatch.setattr('script.sdk_sync.matcher.match', lambda rec, ir, store: None)
    monkeypatch.setattr(_driver._dispatcher, 'dispatch', fake_dispatch)
    monkeypatch.setattr(_driver._aliases, 'load', lambda: _driver._aliases.AliasStore())
    monkeypatch.setattr(_driver._aliases, 'save', lambda store: None)
    monkeypatch.setattr(_driver, '_write_report', fake_write_report)

    rc = _driver.main(['--dry-run', '--no-llm'])

    assert rc == 0
    assert [item[0] for item in captured['dispatched']] == [record]
    assert captured['outcomes'][0].record == record
    assert captured['skipped'] == [(missing_stub, 'file does not exist in working tree')]

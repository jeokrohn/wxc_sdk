"""Smoke tests for driver-side scoping helpers and main() flag wiring."""

from __future__ import annotations

import pytest

from script.sdk_sync import driver as _driver


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

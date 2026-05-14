"""Fixture-driven tests for the deterministic patcher.

Each fixture directory under `fixtures/` contains:
- `before.py`        — SDK pre-state
- `change.json`      — serialized ChangeRecord
- `match.json`       — minimal match metadata (kind, sdk_class, sdk_member, matched_by)
- `after.py`         — expected SDK post-state, OR
- `expected_punt.txt` — substring of the expected Punt.reason
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from script.sdk_sync import patcher
from script.sdk_sync.differ import ChangeRecord
from script.sdk_sync.ir import extract_from_text
from script.sdk_sync.matcher import Match

_FIXTURES = Path(__file__).with_name('fixtures')


def _load_record(d: Path) -> ChangeRecord:
    data = json.loads((d / 'change.json').read_text())
    return ChangeRecord(
        kind=data['kind'],
        qualname=data['qualname'],
        old=data.get('old'),
        new=data.get('new'),
        severity=data['severity'],
        notes=tuple(data.get('notes') or ()),
    )


def _load_match(d: Path, before_text: str) -> Match:
    data = json.loads((d / 'match.json').read_text())
    ir = extract_from_text(before_text, str(d / 'before.py'))
    return Match(
        sdk_path=d / 'before.py',
        kind=data['kind'],
        sdk_class=data['sdk_class'],
        sdk_member=data.get('sdk_member'),
        sdk_module_ir=ir,
        confidence=1.0,
        matched_by=data['matched_by'],
    )


def _fixture_dirs() -> list[Path]:
    return sorted([d for d in _FIXTURES.iterdir() if d.is_dir() and (d / 'change.json').exists()])


@pytest.mark.parametrize('fixture', _fixture_dirs(), ids=lambda d: d.name)
def test_patcher_roundtrip(fixture: Path) -> None:
    before_text = (fixture / 'before.py').read_text()
    record = _load_record(fixture)
    match = _load_match(fixture, before_text)
    result = patcher.apply(record, match)

    after_path = fixture / 'after.py'
    punt_path = fixture / 'expected_punt.txt'
    if punt_path.exists():
        assert isinstance(result, patcher.Punt), (
            f'expected punt, got: {result.summary if isinstance(result, patcher.PatchResult) else result}'
        )
        expected_substr = punt_path.read_text().strip()
        assert expected_substr in result.reason, f'punt reason {result.reason!r} does not contain {expected_substr!r}'
        return
    assert after_path.exists(), f'fixture {fixture.name} has neither after.py nor expected_punt.txt'
    assert isinstance(result, patcher.PatchResult), f'expected PatchResult, got Punt: {result.reason}'
    expected = after_path.read_text()
    assert result.new_text == expected, _format_diff(result.new_text, expected, fixture.name)


def _format_diff(actual: str, expected: str, name: str) -> str:
    import difflib

    diff = ''.join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile=f'{name}/after.py',
            tofile='actual',
        )
    )
    return f'patcher output diverges from expected:\n{diff}'

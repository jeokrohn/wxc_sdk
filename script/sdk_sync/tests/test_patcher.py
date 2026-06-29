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
import textwrap
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


def test_doc_comment_update_uses_matched_enum_member() -> None:
    """Update an enum value doc-comment after alias or structural matching.

    :return: Nothing.
    :rtype: None
    """
    before_text = textwrap.dedent("""\
    from wxc_sdk.base import SafeEnum as Enum


    class OwnerType(str, Enum):
        #: Old owner text.
        call_queue = 'CALL_QUEUE'
    """)
    record = ChangeRecord(
        kind='docstring_changed',
        qualname='NumberOwnerType.call_queue',
        old={'doc_comment': 'Old owner text.'},
        new={'doc_comment': 'New owner text.'},
        severity='trivial',
    )
    match = Match(
        sdk_path=Path('wxc_sdk/common.py'),
        kind='enum_value',
        sdk_class='OwnerType',
        sdk_member='call_queue',
        sdk_module_ir=extract_from_text(before_text, 'wxc_sdk/common.py'),
        confidence=0.95,
        matched_by='structural-enum',
    )

    result = patcher.apply(record, match)

    assert isinstance(result, patcher.PatchResult)
    assert '#: New owner text.' in result.new_text
    assert '#: Old owner text.' not in result.new_text


def test_doc_comment_update_uses_matched_sdk_field_name() -> None:
    """Update a field doc-comment when the SDK field name differs from the stub.

    :return: Nothing.
    :rtype: None
    """
    before_text = textwrap.dedent("""\
    from typing import Optional
    from pydantic import Field
    from wxc_sdk.base import ApiModel


    class NumberOwner(ApiModel):
        #: Old type text.
        owner_type: Optional[str] = Field(alias='type', default=None)
    """)
    record = ChangeRecord(
        kind='docstring_changed',
        qualname='AutoAttendantCallForwardAvailableNumberObjectOwner.type',
        old={'doc_comment': 'Old type text.'},
        new={'doc_comment': 'New type text.'},
        severity='trivial',
    )
    match = Match(
        sdk_path=Path('wxc_sdk/common.py'),
        kind='model_field',
        sdk_class='NumberOwner',
        sdk_member='owner_type',
        sdk_module_ir=extract_from_text(before_text, 'wxc_sdk/common.py'),
        confidence=0.95,
        matched_by='structural-model',
    )

    result = patcher.apply(record, match)

    assert isinstance(result, patcher.PatchResult)
    assert '#: New type text.' in result.new_text
    assert '#: Old type text.' not in result.new_text


def test_doc_comment_changed_already_in_sync_is_idempotent_skip() -> None:
    """Treat an SDK comment that already matches the new stub as success.

    :return: Nothing.
    :rtype: None
    """
    before_text = textwrap.dedent("""\
    from wxc_sdk.base import SafeEnum as Enum


    class OwnerType(str, Enum):
        #: New owner text.
        call_queue = 'CALL_QUEUE'
    """)
    record = ChangeRecord(
        kind='docstring_changed',
        qualname='NumberOwnerType.call_queue',
        old={'doc_comment': 'Old owner text.'},
        new={'doc_comment': 'New owner text.'},
        severity='trivial',
    )
    match = Match(
        sdk_path=Path('wxc_sdk/common.py'),
        kind='enum_value',
        sdk_class='OwnerType',
        sdk_member='call_queue',
        sdk_module_ir=extract_from_text(before_text, 'wxc_sdk/common.py'),
        confidence=0.95,
        matched_by='structural-enum',
    )

    result = patcher.apply(record, match)

    assert isinstance(result, patcher.Punt)
    assert 'idempotent skip' in result.reason

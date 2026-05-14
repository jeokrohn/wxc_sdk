"""Smoke tests for the differ."""

from __future__ import annotations

import textwrap

from script.sdk_sync.differ import diff_irs
from script.sdk_sync.ir import extract_from_text


def test_enum_value_added_is_trivial() -> None:
    old = textwrap.dedent("""\
    from wxc_sdk.base import SafeEnum as Enum
    class Color(str, Enum):
        red = 'red'
        blue = 'blue'
    """)
    new = textwrap.dedent("""\
    from wxc_sdk.base import SafeEnum as Enum
    class Color(str, Enum):
        red = 'red'
        green = 'green'
        blue = 'blue'
    """)
    records = diff_irs(extract_from_text(old, 'a'), extract_from_text(new, 'b'))
    assert len(records) == 1
    r = records[0]
    assert r.kind == 'enum_value_added'
    assert r.qualname == 'Color.green'
    assert r.severity == 'trivial'


def test_model_field_added_is_trivial() -> None:
    old = textwrap.dedent("""\
    from typing import Optional
    from wxc_sdk.base import ApiModel
    class W(ApiModel):
        #: a.
        a: Optional[str] = None
    """)
    new = textwrap.dedent("""\
    from typing import Optional
    from wxc_sdk.base import ApiModel
    class W(ApiModel):
        #: a.
        a: Optional[str] = None
        #: b.
        b: Optional[int] = None
    """)
    records = diff_irs(extract_from_text(old, 'a'), extract_from_text(new, 'b'))
    assert any(r.kind == 'model_field_added' and r.qualname == 'W.b' and r.severity == 'trivial' for r in records)


def test_method_param_added_is_review() -> None:
    old = textwrap.dedent("""\
    from wxc_sdk.api_child import ApiChild
    class A(ApiChild, base='x'):
        def do(self):
            url = self.ep()
            return super().get(url)
    """)
    new = textwrap.dedent("""\
    from wxc_sdk.api_child import ApiChild
    class A(ApiChild, base='x'):
        def do(self, q: str = None):
            url = self.ep()
            return super().get(url)
    """)
    records = diff_irs(extract_from_text(old, 'a'), extract_from_text(new, 'b'))
    assert any(r.kind == 'method_param_added' and r.severity == 'review' for r in records)

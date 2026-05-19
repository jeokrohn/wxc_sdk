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


def test_new_api_class_emits_concrete_method_additions() -> None:
    new = textwrap.dedent("""\
    from wxc_sdk.api_child import ApiChild
    class A(ApiChild, base='x'):
        def first(self):
            url = self.ep('first')
            return super().get(url)

        def second(self):
            url = self.ep('second')
            return super().post(url)
    """)
    records = diff_irs(extract_from_text('', 'a'), extract_from_text(new, 'b'))

    assert [(r.kind, r.qualname) for r in records] == [
        ('method_added', 'A.first'),
        ('method_added', 'A.second'),
    ]
    assert all(r.new is not None and r.new['name'] in {'first', 'second'} for r in records)
    assert all(r.qualname != 'A.*' for r in records)


def test_method_param_additions_preserve_stub_order_and_anchors() -> None:
    old = textwrap.dedent("""\
    from wxc_sdk.api_child import ApiChild
    class A(ApiChild, base='x'):
        def do(self, a: str = None, d: str = None):
            url = self.ep()
            return super().get(url)
    """)
    new = textwrap.dedent("""\
    from wxc_sdk.api_child import ApiChild
    class A(ApiChild, base='x'):
        def do(self, a: str = None, b: str = None, c: str = None, d: str = None):
            url = self.ep()
            return super().get(url)
    """)
    records = [
        r for r in diff_irs(extract_from_text(old, 'a'), extract_from_text(new, 'b')) if r.kind == 'method_param_added'
    ]

    assert [r.new['param']['name'] for r in records if r.new is not None] == ['b', 'c']
    assert [r.new['insert_after'] for r in records if r.new is not None] == ['a', 'b']
    assert [r.new['insert_before'] for r in records if r.new is not None] == ['d', 'd']
    first_new = records[0].new
    assert first_new is not None
    assert [p['name'] for p in first_new['params']] == ['a', 'b', 'c', 'd']

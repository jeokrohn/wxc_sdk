"""Smoke tests for the IR extractor."""

from __future__ import annotations

import textwrap
from pathlib import Path

from script.sdk_sync.ir import extract, extract_from_text

_REPO_ROOT = Path(__file__).resolve().parents[3]


def test_enum_with_doc_comments() -> None:
    src = textwrap.dedent("""\
    from wxc_sdk.base import SafeEnum as Enum


    class Color(str, Enum):
        #: A primary color.
        red = 'red'
        green = 'green'
        #: Like the sky.
        blue = 'blue'
    """)
    ir = extract_from_text(src, '<test>')
    assert len(ir.enums) == 1
    e = ir.enums[0]
    assert e.name == 'Color'
    assert [v.name for v in e.values] == ['red', 'green', 'blue']
    assert e.values[0].doc_comment == 'A primary color.'
    assert e.values[1].doc_comment is None
    assert e.values[2].doc_comment == 'Like the sky.'


def test_model_validators_and_refs() -> None:
    src = textwrap.dedent("""\
    from typing import Optional
    from pydantic import field_validator, model_validator
    from wxc_sdk.base import ApiModel


    class Device(ApiModel):
        #: id.
        id: Optional[str] = None
        mac: Optional[str] = None

        @field_validator('mac')
        @classmethod
        def strip_colons(cls, v):
            return v

        @model_validator(mode='before')
        @classmethod
        def pop_place_id(cls, values):
            return values
    """)
    ir = extract_from_text(src, '<test>')
    m = ir.model_by_name('Device')
    assert m is not None
    assert m.has_custom_validators is True
    assert m.validator_field_refs == frozenset({'mac'})
    assert m.last_field_end_lineno == 9


def test_api_method_endpoint_canonicalization() -> None:
    src = textwrap.dedent("""\
    from typing import Any
    from wxc_sdk.api_child import ApiChild


    class FooApi(ApiChild, base='foo/bar'):
        def get_item(self, item_id: str) -> Any:
            url = self.ep(f'{item_id}/details')
            return super().get(url)

        def list_items(self, **params: Any):
            url = self.ep()
            return super().get(url, params=params)

        def create(self) -> Any:
            url = self.ep('new')
            return super().post(url)
    """)
    ir = extract_from_text(src, '<test>')
    assert ir.api_class is not None
    methods = {m.name: m for m in ir.api_class.methods}
    assert methods['get_item'].verb == 'get'
    # Placeholder identifiers are erased to bare `{}` so the same URL spelled
    # with different parameter names on the stub and SDK side canonicalizes
    # to the same key.
    assert methods['get_item'].ep_template == 'foo/bar/{}/details'
    assert methods['list_items'].verb == 'get'
    assert methods['list_items'].ep_template == 'foo/bar'
    assert methods['create'].verb == 'post'
    assert methods['create'].ep_template == 'foo/bar/new'


def test_api_child_helper_bases_are_api_classes() -> None:
    plain_src = textwrap.dedent("""\
    from wxc_sdk.person_settings.common import PersonSettingsApiChild


    class PlainHelperApi(PersonSettingsApiChild):
        pass
    """)
    dotted_src = textwrap.dedent("""\
    from wxc_sdk.person_settings import common


    class DottedHelperApi(common.PersonSettingsApiChild):
        pass
    """)
    plain_ir = extract_from_text(plain_src, '<plain>')
    dotted_ir = extract_from_text(dotted_src, '<dotted>')

    assert plain_ir.api_class is not None
    assert plain_ir.api_class.name == 'PlainHelperApi'
    assert dotted_ir.api_class is not None
    assert dotted_ir.api_class.name == 'DottedHelperApi'


def test_ecbn_api_live_replay_includes_person_workspace_and_virtual_line_urls() -> None:
    ir = extract(_REPO_ROOT / 'wxc_sdk/person_settings/ecbn.py', is_sdk=True)

    assert ir.api_class is not None
    assert ir.api_class.name == 'ECBNApi'
    read_templates = {m.ep_template for m in ir.api_class.methods if m.name == 'read'}
    assert {
        'telephony/config/people/{}/emergencyCallbackNumber',
        'telephony/config/workspaces/{}/emergencyCallbackNumber',
        'telephony/config/virtualLines/{}/emergencyCallbackNumber',
    } <= read_templates

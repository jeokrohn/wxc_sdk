"""
Tests for parsing and generating OpenAPI ``anyOf`` schemas.
"""

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from open_api.open_api_code_generator import OACodeGenerator  # type: ignore[import-untyped]
from open_api.open_api_model import OASchemaProperty  # type: ignore[import-untyped]
from open_api.open_api_sources import OpenApiSpecInfo  # type: ignore[import-untyped]


def _base_spec(schemas: dict[str, Any]) -> dict[str, Any]:
    """
    Build a minimal OpenAPI document for ``anyOf`` generation tests.

    :param schemas: Component schemas to include in the document.
    :type schemas: dict[str, Any]
    :return: Minimal OpenAPI document using the supplied schemas.
    :rtype: dict[str, Any]
    """
    return {
        'openapi': '3.0.3',
        'info': {
            'title': 'AnyOf Test',
            'version': 'v1',
            'description': 'Spec used to verify anyOf parsing and generation.',
        },
        'servers': [{'url': 'https://example.test/v1'}],
        'paths': {
            '/combined': {
                'get': {
                    'summary': 'Get combined response',
                    'operationId': 'getCombinedResponse',
                    'description': 'Return all anyOf test shapes.',
                    'responses': {
                        '200': {
                            'description': 'OK',
                            'content': {
                                'application/json': {
                                    'schema': {'$ref': '#/components/schemas/CombinedResponse'},
                                },
                            },
                        },
                    },
                },
            },
        },
        'components': {'schemas': schemas},
    }


def _any_of_schemas() -> dict[str, Any]:
    """
    Return schemas covering referenced, inline, nested, and primitive ``anyOf`` shapes.

    :return: Component schemas used by the generation tests.
    :rtype: dict[str, Any]
    """
    return {
        'AvailableSegment': {
            'type': 'object',
            'required': ['available'],
            'properties': {'available': {'type': 'boolean'}},
        },
        'UnavailableSegment': {
            'type': 'object',
            'required': ['reason'],
            'properties': {'reason': {'type': 'string'}},
        },
        'CombinedResponse': {
            'type': 'object',
            'properties': {
                'segments': {
                    'type': 'array',
                    'items': {
                        'anyOf': [
                            {'$ref': '#/components/schemas/AvailableSegment'},
                            {'$ref': '#/components/schemas/UnavailableSegment'},
                            {'$ref': '#/components/schemas/AvailableSegment'},
                        ],
                    },
                },
                'payload': {
                    'anyOf': [
                        {
                            'type': 'object',
                            'required': ['plainText'],
                            'properties': {'plainText': {'type': 'string'}},
                        },
                        {
                            'type': 'object',
                            'required': ['attachmentId'],
                            'properties': {'attachmentId': {'type': 'string'}},
                        },
                    ],
                },
                'choice': {
                    'anyOf': [
                        {
                            'anyOf': [
                                {'type': 'string'},
                                {'type': 'integer'},
                            ],
                        },
                        {'type': 'boolean'},
                    ],
                },
                'status': {
                    'anyOf': [
                        {'type': 'string', 'enum': ['available']},
                        {'type': 'string', 'enum': ['unavailable']},
                    ],
                },
            },
        },
    }


def _build_generator(spec_data: dict[str, Any], temp_dir: Path) -> OACodeGenerator:
    """
    Build and normalize a generator for a temporary OpenAPI document.

    :param spec_data: OpenAPI document to load.
    :type spec_data: dict[str, Any]
    :param temp_dir: Temporary directory in which to write the input specification.
    :type temp_dir: pathlib.Path
    :return: Normalized OpenAPI code generator.
    :rtype: OACodeGenerator
    """
    spec_path = temp_dir / 'spec.json'
    spec_path.write_text(json.dumps(spec_data))
    code_gen = OACodeGenerator()
    code_gen.add_open_api_spec(
        OpenApiSpecInfo(api_name='any-of-test', base_path=str(temp_dir), spec_path=str(spec_path), version='v1')
    )
    code_gen.cleanup()
    return code_gen


def _generate_source(spec_data: dict[str, Any], temp_dir: Path) -> str:
    """
    Generate Python source for a temporary OpenAPI document.

    :param spec_data: OpenAPI document to generate.
    :type spec_data: dict[str, Any]
    :param temp_dir: Temporary directory in which to write the input specification.
    :type temp_dir: pathlib.Path
    :return: Generated Python source.
    :rtype: str
    """
    return cast(str, _build_generator(spec_data, temp_dir).source(with_example=False))


def _import_generated_source(source: str, temp_dir: Path) -> ModuleType:
    """
    Import generated source as a temporary Python module.

    :param source: Generated Python source to import.
    :type source: str
    :param temp_dir: Temporary directory in which to write the generated module.
    :type temp_dir: pathlib.Path
    :return: Imported generated module.
    :rtype: types.ModuleType
    :raises RuntimeError: If Python cannot create an import specification for the module.
    """
    module_name = 'generated_any_of_test'
    source_path = temp_dir / f'{module_name}.py'
    source_path.write_text(source)
    module_spec = importlib.util.spec_from_file_location(module_name, source_path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f'Could not create an import specification for {source_path}')
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_name] = module
    try:
        module_spec.loader.exec_module(module)
    finally:
        sys.modules.pop(module_name, None)
    return module


def test_parser_accepts_nested_any_of_alternatives() -> None:
    """
    Verify complete nested Schema Objects are retained when parsing ``anyOf``.

    :return: None.
    """
    prop = OASchemaProperty.model_validate(
        {
            'anyOf': [
                {'$ref': '#/components/schemas/AvailableSegment'},
                {
                    'type': 'array',
                    'items': {
                        'anyOf': [
                            {'type': 'string'},
                            {'type': 'integer'},
                        ],
                    },
                },
            ],
        }
    )

    assert prop.any_of is not None
    assert prop.any_of[0].ref == '#/components/schemas/AvailableSegment'
    assert prop.any_of[1].items is not None
    assert prop.any_of[1].items.any_of is not None
    assert [option.type for option in prop.any_of[1].items.any_of] == ['string', 'integer']


def test_generator_emits_nested_unions_and_tracks_references(tmp_path: Path) -> None:
    """
    Verify referenced and recursively nested ``anyOf`` schemas generate stable unions.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    code_gen = _build_generator(_base_spec(_any_of_schemas()), tmp_path)
    source = code_gen.source(with_example=False)
    combined_response = code_gen.class_registry.get('CombinedResponse')
    assert combined_response is not None
    assert combined_response.attributes is not None
    attributes = {attribute.name: attribute for attribute in combined_response.attributes}

    assert 'segments: Optional[list[Union[AvailableSegment, UnavailableSegment]]] = None' in source
    assert 'payload: Optional[Union[CombinedResponsePayloadAnyOf1, CombinedResponsePayloadAnyOf2]] = None' in source
    assert 'choice: Optional[Union[Union[str, int], bool]] = None' in source
    assert 'status: Optional[str] = None' in source
    assert attributes['segments'].class_references == ('AvailableSegment', 'UnavailableSegment')
    assert attributes['payload'].class_references == (
        'CombinedResponsePayloadAnyOf1',
        'CombinedResponsePayloadAnyOf2',
    )


def test_inline_object_alternatives_have_deterministic_names(tmp_path: Path) -> None:
    """
    Verify inline ``anyOf`` objects receive stable owner-and-property-based names.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    source = _generate_source(_base_spec(_any_of_schemas()), tmp_path)

    assert 'class CombinedResponsePayloadAnyOf1(ApiModel):' in source
    assert 'class CombinedResponsePayloadAnyOf2(ApiModel):' in source


def test_generated_union_validates_referenced_and_inline_alternatives(tmp_path: Path) -> None:
    """
    Verify generated Pydantic models accept referenced and inline ``anyOf`` alternatives.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    source = _generate_source(_base_spec(_any_of_schemas()), tmp_path)
    generated = _import_generated_source(source, tmp_path)

    response = generated.CombinedResponse.model_validate(
        {
            'segments': [{'available': True}, {'reason': 'maintenance'}],
            'payload': {'attachmentId': 'attachment-1'},
            'choice': 42,
            'status': 'available',
        }
    )

    assert isinstance(response.segments[0], generated.AvailableSegment)
    assert isinstance(response.segments[1], generated.UnavailableSegment)
    assert isinstance(response.payload, generated.CombinedResponsePayloadAnyOf2)
    assert response.choice == 42
    assert response.status == 'available'


def test_same_primitive_any_of_retains_primitive_annotation(tmp_path: Path) -> None:
    """
    Verify same-type primitive alternatives preserve the legacy primitive annotation.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    source = _generate_source(_base_spec(_any_of_schemas()), tmp_path)

    assert 'status: Optional[str] = None' in source
    assert 'CombinedResponseStatusAnyOf' not in source


def test_empty_any_of_has_contextual_error(tmp_path: Path) -> None:
    """
    Verify an empty ``anyOf`` identifies its containing property.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    schemas = {
        'CombinedResponse': {
            'type': 'object',
            'properties': {'segments': {'anyOf': []}},
        },
    }

    with pytest.raises(ValueError, match=r'CombinedResponse\.segments.*anyOf.*at least one alternative'):
        _generate_source(_base_spec(schemas), tmp_path)


def test_any_of_rejects_schema_defining_siblings(tmp_path: Path) -> None:
    """
    Verify schema-defining siblings cannot silently override ``anyOf`` alternatives.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    schemas = {
        'CombinedResponse': {
            'type': 'object',
            'properties': {
                'segments': {
                    'type': 'string',
                    'anyOf': [
                        {'type': 'string'},
                        {'type': 'integer'},
                    ],
                },
            },
        },
    }

    with pytest.raises(ValueError, match=r'CombinedResponse\.segments.*anyOf.*schema-defining fields: type'):
        _generate_source(_base_spec(schemas), tmp_path)

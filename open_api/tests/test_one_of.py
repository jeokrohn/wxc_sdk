"""
Tests for parsing and generating OpenAPI ``oneOf`` schemas.
"""

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from open_api.open_api_code_generator import OACodeGenerator  # type: ignore[import-untyped]
from open_api.open_api_model import OASchemaProperty, OASpec  # type: ignore[import-untyped]
from open_api.open_api_sources import OpenApiSpecInfo  # type: ignore[import-untyped]


def _base_spec(schemas: dict[str, Any], response_schema: str = 'CombinedResponse') -> dict[str, Any]:
    """
    Build a minimal OpenAPI document for code-generation tests.

    :param schemas: Component schemas to include in the document.
    :type schemas: dict[str, Any]
    :param response_schema: Component schema returned by the test endpoint.
    :type response_schema: str
    :return: Minimal OpenAPI document using the supplied schemas.
    :rtype: dict[str, Any]
    """
    return {
        'openapi': '3.0.3',
        'info': {
            'title': 'OneOf Test',
            'version': 'v1',
            'description': 'Spec used to verify oneOf parsing and generation.',
        },
        'servers': [{'url': 'https://example.test/v1'}],
        'paths': {
            '/combined': {
                'get': {
                    'summary': 'Get combined response',
                    'operationId': 'getCombinedResponse',
                    'description': 'Return all oneOf test shapes.',
                    'responses': {
                        '200': {
                            'description': 'OK',
                            'content': {
                                'application/json': {
                                    'schema': {'$ref': f'#/components/schemas/{response_schema}'},
                                },
                            },
                        },
                    },
                },
            },
        },
        'components': {'schemas': schemas},
    }


def _one_of_schemas() -> dict[str, Any]:
    """
    Return component schemas covering every supported nested ``oneOf`` shape.

    :return: Schemas containing inline, referenced, and array-item alternatives.
    :rtype: dict[str, Any]
    """
    return {
        'MessageText': {
            'type': 'object',
            'properties': {'text': {'type': 'string'}},
        },
        'TranscriptObject': {
            'type': 'object',
            'properties': {
                'message': {
                    'oneOf': [
                        {'type': 'string', 'description': 'Human utterance.'},
                        {
                            'type': 'array',
                            'items': {'$ref': '#/components/schemas/MessageText'},
                            'description': 'Bot response.',
                        },
                    ],
                },
            },
        },
        'TextMessage': {
            'type': 'object',
            'properties': {'plainText': {'type': 'string'}},
        },
        'TextWithAttachment': {
            'type': 'object',
            'properties': {'attachments': {'type': 'array', 'items': {'type': 'string'}}},
        },
        'ScheduleSlot': {
            'type': 'object',
            'properties': {'startTime': {'type': 'string'}},
        },
        'AdvancedScheduleDay': {
            'type': 'object',
            'properties': {'day': {'type': 'string'}},
        },
        'CombinedResponse': {
            'type': 'object',
            'properties': {
                'transcript': {'$ref': '#/components/schemas/TranscriptObject'},
                'message': {
                    'oneOf': [
                        {'$ref': '#/components/schemas/TextMessage'},
                        {'$ref': '#/components/schemas/TextWithAttachment'},
                        {'$ref': '#/components/schemas/TextMessage'},
                    ],
                },
                'schedule': {
                    'type': 'array',
                    'items': {
                        'oneOf': [
                            {'$ref': '#/components/schemas/ScheduleSlot'},
                            {'$ref': '#/components/schemas/AdvancedScheduleDay'},
                        ],
                    },
                },
            },
        },
    }


def _build_generator(spec_data: dict[str, Any], temp_dir: Path) -> OACodeGenerator:
    """
    Build and normalize a generator for an in-memory OpenAPI document.

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
        OpenApiSpecInfo(api_name='one-of-test', base_path=str(temp_dir), spec_path=str(spec_path), version='v1')
    )
    code_gen.cleanup()
    return code_gen


def _generate_source(spec_data: dict[str, Any], temp_dir: Path) -> str:
    """
    Generate Python source for an in-memory OpenAPI document.

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
    Import generated source from a temporary Python module.

    :param source: Generated Python source to import.
    :type source: str
    :param temp_dir: Temporary directory in which to write the generated module.
    :type temp_dir: pathlib.Path
    :return: Imported generated module.
    :rtype: types.ModuleType
    :raises RuntimeError: If Python cannot create an import specification for the module.
    """
    module_name = 'generated_one_of_test'
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


def test_parser_accepts_inline_one_of_alternatives() -> None:
    """
    Verify inline Schema Objects are retained when parsing ``oneOf``.

    :return: None.
    """
    prop = OASchemaProperty.model_validate(
        {
            'description': 'Human or bot message.',
            'oneOf': [
                {'type': 'string', 'description': 'Human utterance.'},
                {
                    'type': 'array',
                    'items': {'$ref': '#/components/schemas/MessageText'},
                    'description': 'Bot response.',
                },
            ],
        }
    )

    assert prop.one_of is not None
    assert prop.one_of[0].type == 'string'
    assert prop.one_of[0].description == 'Human utterance.'
    assert prop.one_of[1].type == 'array'
    assert prop.one_of[1].items is not None
    assert prop.one_of[1].items.ref == '#/components/schemas/MessageText'


def test_parser_retains_union_discriminator_and_object_limits() -> None:
    """
    Verify valid metadata used by current production union schemas is retained.

    :return: None.
    """
    prop = OASchemaProperty.model_validate(
        {
            'oneOf': [
                {'$ref': '#/components/schemas/TextMessage'},
                {'$ref': '#/components/schemas/TextWithAttachment'},
            ],
            'discriminator': {
                'propertyName': 'type',
                'mapping': {
                    'text': '#/components/schemas/TextMessage',
                    'attachment': '#/components/schemas/TextWithAttachment',
                },
            },
            'maxProperties': 50,
        }
    )

    assert prop.max_properties == 50
    assert prop.discriminator is not None
    assert prop.discriminator.mapping == {
        'text': '#/components/schemas/TextMessage',
        'attachment': '#/components/schemas/TextWithAttachment',
    }


def test_generator_emits_nested_unions_and_tracks_all_references(tmp_path: Path) -> None:
    """
    Verify nested unions generate stable annotations and retain every model.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    code_gen = _build_generator(_base_spec(_one_of_schemas()), tmp_path)
    source = code_gen.source(with_example=False)
    combined_response = code_gen.class_registry.get('CombinedResponse')
    assert combined_response is not None
    assert combined_response.attributes is not None
    attributes = {attribute.name: attribute for attribute in combined_response.attributes}

    assert 'message: Optional[Union[str, list[MessageText]]] = None' in source
    assert 'message: Optional[Union[TextMessage, TextWithAttachment]] = None' in source
    assert 'schedule: Optional[list[Union[ScheduleSlot, AdvancedScheduleDay]]] = None' in source
    assert attributes['message'].class_references == ('TextMessage', 'TextWithAttachment')
    assert attributes['schedule'].class_references == ('ScheduleSlot', 'AdvancedScheduleDay')
    for class_name in {
        'AdvancedScheduleDay',
        'MessageText',
        'ScheduleSlot',
        'TextMessage',
        'TextWithAttachment',
        'TranscriptObject',
    }:
        assert f"'{class_name}'" in source


def test_inline_object_alternatives_have_deterministic_names(tmp_path: Path) -> None:
    """
    Verify inline object alternatives receive stable owner-and-property-based names.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    schemas = {
        'CombinedResponse': {
            'type': 'object',
            'properties': {
                'status': {'type': 'string'},
                'payload': {
                    'oneOf': [
                        {
                            'type': 'object',
                            'properties': {'plainText': {'type': 'string'}},
                        },
                        {
                            'type': 'object',
                            'properties': {'attachmentId': {'type': 'string'}},
                        },
                    ],
                },
            },
        },
    }

    source = _generate_source(_base_spec(schemas), tmp_path)

    assert 'payload: Optional[Union[CombinedResponsePayloadOneOf1, CombinedResponsePayloadOneOf2]] = None' in source
    assert 'class CombinedResponsePayloadOneOf1(ApiModel):' in source
    assert 'class CombinedResponsePayloadOneOf2(ApiModel):' in source


def test_generated_inline_union_validates_both_payload_shapes(tmp_path: Path) -> None:
    """
    Verify generated Pydantic models accept both AI Receptionist message shapes.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    source = _generate_source(_base_spec(_one_of_schemas()), tmp_path)
    generated = _import_generated_source(source, tmp_path)

    human = generated.CombinedResponse.model_validate({'transcript': {'message': 'hello'}})
    bot = generated.CombinedResponse.model_validate({'transcript': {'message': [{'text': 'hello'}]}})

    assert human.transcript.message == 'hello'
    assert isinstance(bot.transcript.message, list)
    assert isinstance(bot.transcript.message[0], generated.MessageText)
    assert bot.transcript.message[0].text == 'hello'


def test_endpoint_result_union_tracks_every_reference(tmp_path: Path) -> None:
    """
    Verify a response-level union retains all referenced result classes.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    schemas = {
        'TextMessage': {'type': 'object', 'properties': {'plainText': {'type': 'string'}}},
        'TextWithAttachment': {
            'type': 'object',
            'properties': {'attachments': {'type': 'array', 'items': {'type': 'string'}}},
        },
    }
    spec_data = _base_spec(schemas, response_schema='TextMessage')
    response_schema = spec_data['paths']['/combined']['get']['responses']['200']['content']['application/json']
    response_schema['schema'] = {
        'oneOf': [
            {'$ref': '#/components/schemas/TextMessage'},
            {'$ref': '#/components/schemas/TextWithAttachment'},
        ]
    }

    code_gen = _build_generator(spec_data, tmp_path)
    source = code_gen.source(with_example=False)
    generated = _import_generated_source(source, tmp_path)
    endpoint = next(endpoint for _, endpoint in code_gen.all_endpoints())
    validator = endpoint.body_validator(generated)

    assert endpoint.result_class_references == ('TextMessage', 'TextWithAttachment')
    assert 'def get_combined_response(self) -> Union[TextMessage, TextWithAttachment]:' in source
    assert 'r = TypeAdapter(Union[TextMessage, TextWithAttachment]).validate_python(data)' in source
    assert "'TextMessage'" in source
    assert "'TextWithAttachment'" in source
    assert isinstance(validator({'plainText': 'hello'}), generated.TextMessage)
    assert isinstance(validator({'attachments': ['abc']}), generated.TextWithAttachment)


def test_body_parameter_union_serializes_through_type_adapter(tmp_path: Path) -> None:
    """
    Verify body-argument unions retain all models and use Pydantic serialization.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    schemas = {
        'TextMessage': {'type': 'object', 'properties': {'plainText': {'type': 'string'}}},
        'TextWithAttachment': {
            'type': 'object',
            'properties': {'attachments': {'type': 'array', 'items': {'type': 'string'}}},
        },
    }
    spec_data = _base_spec(schemas, response_schema='TextMessage')
    spec_data['paths']['/combined'] = {
        'put': {
            'summary': 'Update combined response',
            'operationId': 'updateCombinedResponse',
            'description': 'Update a union-typed message.',
            'requestBody': {
                'required': True,
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'required': ['message'],
                            'properties': {
                                'message': {
                                    'oneOf': [
                                        {'$ref': '#/components/schemas/TextMessage'},
                                        {'$ref': '#/components/schemas/TextWithAttachment'},
                                    ],
                                },
                            },
                        },
                    },
                },
            },
            'responses': {'204': {'description': 'No Content'}},
        },
    }

    source = _generate_source(spec_data, tmp_path)

    assert 'def update_combined_response(self, message: Union[TextMessage, TextWithAttachment]) -> None:' in source
    assert (
        "body['message'] = TypeAdapter(Union[TextMessage, TextWithAttachment]).dump_python("
        "message, mode='json', by_alias=True, exclude_none=True)"
    ) in source
    assert "'TextMessage'" in source
    assert "'TextWithAttachment'" in source


def test_top_level_referenced_object_union_is_still_flattened() -> None:
    """
    Verify existing top-level object-union normalization remains unchanged.

    :return: None.
    """
    schemas = {
        'First': {
            'type': 'object',
            'required': ['shared', 'first'],
            'properties': {'shared': {'type': 'string'}, 'first': {'type': 'string'}},
        },
        'Second': {
            'type': 'object',
            'required': ['shared', 'second'],
            'properties': {'shared': {'type': 'string'}, 'second': {'type': 'string'}},
        },
        'CombinedResponse': {
            'type': 'object',
            'discriminator': {'propertyName': 'kind'},
            'oneOf': [
                {'$ref': '#/components/schemas/First'},
                {'$ref': '#/components/schemas/Second'},
            ],
        },
    }
    spec = OASpec.model_validate(_base_spec(schemas))

    spec.unify_one_of_schemas()

    combined = spec.components.schemas['CombinedResponse']
    assert combined.one_of is None
    assert combined.type == 'object'
    assert list(combined.properties or {}) == ['shared', 'first', 'second']
    assert combined.required == ['shared']


def test_flattened_union_resolves_schema_free_object_references(tmp_path: Path) -> None:
    """
    Verify flattened object unions can reference schema-free map components.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    schemas = {
        'Settings': {
            'type': 'object',
            'additionalProperties': {'type': 'string'},
        },
        'First': {
            'type': 'object',
            'properties': {'kind': {'type': 'string'}, 'settings': {'$ref': '#/components/schemas/Settings'}},
        },
        'Second': {
            'type': 'object',
            'properties': {'kind': {'type': 'string'}, 'settings': {'$ref': '#/components/schemas/Settings'}},
        },
        'CombinedResponse': {
            'oneOf': [
                {'$ref': '#/components/schemas/First'},
                {'$ref': '#/components/schemas/Second'},
            ],
        },
    }

    source = _generate_source(_base_spec(schemas), tmp_path)

    assert 'settings: Optional[dict] = None' in source


def test_schema_free_object_alias_reaches_body_parameters(tmp_path: Path) -> None:
    """
    Verify schema-free object aliases are resolved in endpoint body parameters.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    schemas = {
        'Settings': {
            'type': 'object',
            'additionalProperties': {'type': 'string'},
        },
        'CombinedResponse': {
            'type': 'object',
            'properties': {'status': {'type': 'string'}},
        },
    }
    spec_data = _base_spec(schemas)
    spec_data['paths']['/combined'] = {
        'put': {
            'summary': 'Update combined response',
            'operationId': 'updateCombinedResponse',
            'description': 'Update schema-free settings.',
            'requestBody': {
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'settings': {'$ref': '#/components/schemas/Settings'},
                            },
                        },
                    },
                },
            },
            'responses': {'204': {'description': 'No Content'}},
        },
    }

    source = _generate_source(spec_data, tmp_path)

    assert 'def update_combined_response(self, settings: dict = None) -> None:' in source


def test_top_level_inline_union_has_contextual_error() -> None:
    """
    Verify unsupported top-level inline unions fail with the schema name.

    :return: None.
    """
    schemas = {
        'CombinedResponse': {
            'oneOf': [
                {'type': 'string'},
                {'type': 'integer'},
            ],
        },
    }
    spec = OASpec.model_validate(_base_spec(schemas))

    with pytest.raises(
        ValueError,
        match=r"Schema 'CombinedResponse': top-level oneOf alternatives must all be object schemas",
    ):
        spec.unify_one_of_schemas()


def test_empty_nested_union_has_contextual_error(tmp_path: Path) -> None:
    """
    Verify an empty nested union identifies its containing property.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    schemas = {
        'CombinedResponse': {
            'type': 'object',
            'properties': {'message': {'oneOf': []}},
        },
    }

    with pytest.raises(ValueError, match=r'CombinedResponse\.message.*at least one alternative'):
        _generate_source(_base_spec(schemas), tmp_path)


def test_nested_union_rejects_schema_defining_siblings(tmp_path: Path) -> None:
    """
    Verify schema-defining siblings cannot silently override a nested union.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: pathlib.Path
    :return: None.
    """
    schemas = {
        'CombinedResponse': {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string',
                    'oneOf': [
                        {'type': 'string'},
                        {'type': 'integer'},
                    ],
                },
            },
        },
    }

    with pytest.raises(ValueError, match=r'CombinedResponse\.message.*schema-defining fields: type'):
        _generate_source(_base_spec(schemas), tmp_path)

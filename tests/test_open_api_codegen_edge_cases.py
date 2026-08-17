"""Regression tests for OpenAPI constructs used by the previously failing specifications."""

import importlib.util
import json
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
from pydantic import ValidationError

from open_api.open_api_code_generator import OACodeGenerator
from open_api.open_api_model import OASchemaProperty, OASpec
from open_api.open_api_sources import OpenApiSpecInfo


def _minimal_spec(
    schemas: dict[str, dict[str, Any]],
    paths: dict[str, dict[str, dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """Build a minimal OpenAPI document for code-generation tests.

    :param schemas: Component schemas to include in the document.
    :param paths: Optional path and operation definitions.
    :return: Minimal OpenAPI document accepted by the generator.
    """
    return {
        'openapi': '3.1.0',
        'info': {
            'title': 'OpenAPI edge-case test',
            'version': '1.0.0',
            'description': 'Synthetic document covering code-generation edge cases.',
        },
        'servers': [{'url': 'https://example.test'}],
        'paths': paths or {},
        'components': {'schemas': schemas},
    }


def _operation(
    operation_id: str,
    *,
    request_body: dict[str, Any] | None = None,
    response_schema: dict[str, Any] | None = None,
    method_summary: str = 'Exercise an edge case',
    extensions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one synthetic OpenAPI operation.

    :param operation_id: Operation identifier used for the generated method.
    :param request_body: Optional request body object.
    :param response_schema: Optional successful response schema.
    :param method_summary: Summary used by the generated method docstring.
    :param extensions: Optional vendor extensions to add to the operation.
    :return: OpenAPI operation dictionary.
    """
    if response_schema is None:
        responses: dict[str, Any] = {'204': {'description': 'No Content'}}
    else:
        responses = {
            '200': {
                'description': 'Success',
                'content': {'application/json': {'schema': response_schema}},
            }
        }
    operation: dict[str, Any] = {
        'summary': method_summary,
        'operationId': operation_id,
        'description': f'Synthetic operation for {operation_id}.',
        'responses': responses,
    }
    if request_body is not None:
        operation['requestBody'] = request_body
    operation.update(extensions or {})
    return operation


def _generate(tmp_path: Path, spec: dict[str, Any]) -> tuple[OACodeGenerator, str]:
    """Generate and normalize Python source for a synthetic OpenAPI document.

    :param tmp_path: Pytest-provided temporary directory.
    :param spec: OpenAPI document to generate.
    :return: Generator instance and complete generated source.
    """
    spec_path = tmp_path / 'spec.json'
    spec_path.write_text(json.dumps(spec), encoding='utf-8')
    generator = OACodeGenerator()
    generator.add_open_api_spec(
        OpenApiSpecInfo(
            api_name='edge-case-test',
            base_path=str(tmp_path),
            spec_path=str(spec_path),
            version='v1',
        )
    )
    generator.cleanup()
    return generator, generator.source(with_example=False)


def _import_generated_source(source: str, tmp_path: Path, module_name: str) -> ModuleType:
    """Import generated source from a temporary Python module.

    :param source: Generated Python source to import.
    :param tmp_path: Directory in which to write the temporary module.
    :param module_name: Unique module name to register during import.
    :return: Imported module, retained in ``sys.modules`` for forward-reference resolution.
    :raises RuntimeError: If Python cannot create a module loader.
    """
    source_path = tmp_path / f'{module_name}.py'
    source_path.write_text(source, encoding='utf-8')
    module_spec = importlib.util.spec_from_file_location(module_name, source_path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f'Could not create an import specification for {source_path}')
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_name] = module
    module_spec.loader.exec_module(module)
    return module


def test_parser_accepts_examples_not_and_vendor_extensions() -> None:
    """Accept supported metadata while retaining strict ordinary-field validation.

    :return: None.
    """
    operation = _operation(
        'updateThing',
        request_body={
            'required': True,
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/Selector'},
                }
            },
        },
        extensions={
            'x-codegen-request-body-name': 'selector',
            'x-unrelated-generator-setting': True,
        },
    )
    operation['parameters'] = [
        {
            'name': 'filter',
            'in': 'query',
            'schema': {'type': 'string'},
            'examples': {'sample': {'value': 'active'}},
            'x-parameter-note': 'ignored vendor metadata',
        }
    ]
    spec = OASpec.model_validate(
        _minimal_spec(
            {
                'Selector': {
                    'type': 'object',
                    'examples': [{'id': 'announcement-id'}],
                    'oneOf': [
                        {
                            'type': 'object',
                            'required': ['id'],
                            'properties': {'id': {'type': 'string'}},
                        },
                        {
                            'type': 'object',
                            'required': ['fileName'],
                            'not': {'required': ['id']},
                            'properties': {'fileName': {'type': 'string'}},
                        },
                    ],
                }
            },
            {'/things': {'put': operation}},
        )
    )

    parsed_operation = spec.paths['/things']['put']
    assert parsed_operation.request_body_name == 'selector'
    assert parsed_operation.parameters[0].examples == {'sample': {'value': 'active'}}
    selector = spec.components.schemas['Selector']
    assert selector.examples == [{'id': 'announcement-id'}]
    assert selector.one_of is not None
    assert selector.one_of[1].not_ is not None

    with pytest.raises(ValidationError, match='extra_forbidden'):
        OASchemaProperty.model_validate({'type': 'string', 'ordinaryTypo': True})


def test_annotation_only_schema_generates_any(tmp_path: Path) -> None:
    """Map a schema carrying only annotations to ``Any`` without losing its documentation.

    :param tmp_path: Pytest-provided temporary directory.
    """
    spec = _minimal_spec(
        {
            'Envelope': {
                'type': 'object',
                'properties': {
                    'kind': {'type': 'string'},
                    'value': {
                        'description': 'Value whose runtime type is intentionally unconstrained.',
                        'example': '94043',
                    },
                },
            }
        },
        {'/things': {'get': _operation('getThing', response_schema={'$ref': '#/components/schemas/Envelope'})}},
    )

    _, source = _generate(tmp_path, spec)

    assert 'value: Optional[Any] = None' in source
    assert 'Value whose runtime type is intentionally unconstrained.' in source


def test_primitive_component_alias_resolves_response(tmp_path: Path) -> None:
    """Resolve a response reference to a primitive component alias.

    :param tmp_path: Pytest-provided temporary directory.
    """
    spec = _minimal_spec(
        {'Acknowledgement': {'type': 'string', 'description': 'Returns OK.', 'example': 'OK'}},
        {
            '/lock': {
                'post': _operation(
                    'lockThing',
                    response_schema={'$ref': '#/components/schemas/Acknowledgement'},
                )
            }
        },
    )

    generator, source = _generate(tmp_path, spec)
    endpoint = next(endpoint for _, endpoint in generator.all_endpoints())

    assert endpoint.result == 'str'
    assert endpoint.result_referenced_class is None
    assert 'def lock_thing(self) -> str:' in source


def test_recursive_schema_generates_importable_model(tmp_path: Path) -> None:
    """Generate, import, and validate a self-referential component schema.

    :param tmp_path: Pytest-provided temporary directory.
    """
    spec = _minimal_spec(
        {
            'ActivityInput': {
                'type': 'object',
                'required': ['name', 'children'],
                'properties': {
                    'name': {'type': 'string'},
                    'children': {
                        'type': 'array',
                        'items': {'$ref': '#/components/schemas/ActivityInput'},
                    },
                },
            }
        },
        {
            '/inputs': {
                'get': _operation(
                    'getInput',
                    response_schema={'$ref': '#/components/schemas/ActivityInput'},
                )
            }
        },
    )

    _, source = _generate(tmp_path, spec)
    module_name = 'generated_recursive_openapi_test'
    generated = _import_generated_source(source, tmp_path, module_name)
    try:
        result = generated.ActivityInput.model_validate(
            {'name': 'parent', 'children': [{'name': 'child', 'children': []}]}
        )
        assert result.children[0].name == 'child'
    finally:
        sys.modules.pop(module_name, None)


def test_component_all_of_merges_inline_and_referenced_objects(tmp_path: Path) -> None:
    """Merge required fields and properties from inline and referenced ``allOf`` members.

    :param tmp_path: Pytest-provided temporary directory.
    """
    spec = _minimal_spec(
        {
            'BaseRequest': {
                'type': 'object',
                'required': ['name'],
                'properties': {'name': {'type': 'string'}},
            },
            'UpdateRequest': {
                'allOf': [
                    {
                        'type': 'object',
                        'required': ['id'],
                        'properties': {
                            'id': {'type': 'string'},
                            'name': {'type': 'string'},
                        },
                    },
                    {'$ref': '#/components/schemas/BaseRequest'},
                ]
            },
        },
        {
            '/things': {
                'get': _operation(
                    'getUpdateRequest',
                    response_schema={'$ref': '#/components/schemas/UpdateRequest'},
                )
            }
        },
    )

    parsed = OASpec.model_validate(spec)
    parsed.unify_all_of_schemas()
    assert parsed.components.schemas['UpdateRequest'].required == ['id', 'name']

    _, source = _generate(tmp_path, spec)

    assert 'class UpdateRequest(ApiModel):' in source
    assert 'id: Optional[str] = None' in source
    assert 'name: Optional[str] = None' in source


@pytest.mark.parametrize(
    ('schemas', 'message'),
    [
        (
            {
                'Conflicting': {
                    'allOf': [
                        {'type': 'object', 'properties': {'value': {'type': 'string'}}},
                        {'type': 'object', 'properties': {'value': {'type': 'integer'}}},
                    ]
                }
            },
            "Schema 'Conflicting': conflicting allOf definitions for property 'value'",
        ),
        (
            {
                'First': {'allOf': [{'$ref': '#/components/schemas/Second'}]},
                'Second': {'allOf': [{'$ref': '#/components/schemas/First'}]},
            },
            'allOf composition cycle detected: First -> Second -> First',
        ),
    ],
)
def test_component_all_of_rejects_conflicts_and_cycles(schemas: dict[str, dict[str, Any]], message: str) -> None:
    """Raise contextual errors for unsafe ``allOf`` normalization.

    :param schemas: Component definitions containing the invalid composition.
    :param message: Diagnostic fragment expected from normalization.
    :return: None.
    """
    spec = OASpec.model_validate(_minimal_spec(schemas))

    with pytest.raises(ValueError, match=re.escape(message)):
        spec.unify_all_of_schemas()


def test_component_inline_one_of_flattens_object_alternatives(tmp_path: Path) -> None:
    """Flatten inline object alternatives using existing component ``oneOf`` semantics.

    :param tmp_path: Pytest-provided temporary directory.
    """
    spec = _minimal_spec(
        {
            'AnnouncementSelector': {
                'type': 'object',
                'nullable': True,
                'description': 'Select an announcement by ID or file metadata.',
                'oneOf': [
                    {
                        'type': 'object',
                        'required': ['id'],
                        'properties': {'id': {'type': 'string'}},
                    },
                    {
                        'type': 'object',
                        'required': ['fileName'],
                        'not': {'required': ['id']},
                        'properties': {'fileName': {'type': 'string'}},
                    },
                ],
            }
        },
        {
            '/announcement': {
                'get': _operation(
                    'getAnnouncement',
                    response_schema={'$ref': '#/components/schemas/AnnouncementSelector'},
                )
            }
        },
    )

    parsed = OASpec.model_validate(spec)
    parsed.unify_one_of_schemas()
    assert parsed.components.schemas['AnnouncementSelector'].required == []

    _, source = _generate(tmp_path, spec)

    assert 'class AnnouncementSelector(ApiModel):' in source
    assert 'id: Optional[str] = None' in source
    assert 'file_name: Optional[str] = None' in source


def test_equivalent_request_media_types_prefer_json(tmp_path: Path) -> None:
    """Choose JSON deterministically when multiple content types have equivalent shapes.

    :param tmp_path: Pytest-provided temporary directory.
    """
    body_schema = {
        'type': 'object',
        'required': ['name'],
        'properties': {'name': {'type': 'string'}},
    }
    request_body = {
        'required': True,
        'content': {
            'multipart/form-data': {'schema': body_schema},
            'application/json': {'schema': body_schema},
        },
    }
    spec = _minimal_spec(
        {},
        {'/things': {'post': _operation('createThing', request_body=request_body)}},
    )

    generator, source = _generate(tmp_path, spec)
    endpoint = next(endpoint for _, endpoint in generator.all_endpoints())

    assert endpoint.request_media_type == 'application/json'
    assert endpoint.body_is_raw is False
    assert [parameter.name for parameter in endpoint.body_parameter] == ['name']
    assert 'super().post(url, json=body)' in source


def test_divergent_request_media_types_are_rejected(tmp_path: Path) -> None:
    """Reject multiple request media types whose generated body shapes differ.

    :param tmp_path: Pytest-provided temporary directory.
    """
    request_body = {
        'required': True,
        'content': {
            'application/json': {'schema': {'type': 'object', 'properties': {'name': {'type': 'string'}}}},
            'multipart/form-data': {
                'schema': {'type': 'object', 'properties': {'file': {'type': 'string', 'format': 'binary'}}}
            },
        },
    }
    spec = _minimal_spec(
        {},
        {'/things': {'post': _operation('createThing', request_body=request_body)}},
    )

    with pytest.raises(ValueError, match='different schemas or encodings'):
        _generate(tmp_path, spec)


def test_raw_inline_and_referenced_array_bodies_are_typed(tmp_path: Path) -> None:
    """Generate one typed argument for inline and referenced array request bodies.

    :param tmp_path: Pytest-provided temporary directory.
    """
    inline_body = {
        'description': 'List of identities.',
        'required': True,
        'content': {
            'application/json-patch+json': {
                'schema': {'type': 'array', 'items': {'type': 'string'}},
            }
        },
    }
    referenced_body = {
        'description': 'JSON Patch operations.',
        'required': True,
        'content': {
            'application/json-patch+json': {
                'schema': {'$ref': '#/components/schemas/PatchRequest'},
            }
        },
    }
    spec = _minimal_spec(
        {
            'PatchDocument': {
                'type': 'object',
                'required': ['op'],
                'properties': {'op': {'type': 'string'}},
            },
            'PatchRequest': {
                'type': 'array',
                'items': {'$ref': '#/components/schemas/PatchDocument'},
            },
        },
        {
            '/identities': {'patch': _operation('removeIdentities', request_body=inline_body)},
            '/patches': {
                'patch': _operation(
                    'applyPatches',
                    request_body=referenced_body,
                    extensions={'x-codegen-request-body-name': 'documents'},
                )
            },
            '/patches/default-name': {'patch': _operation('applyDefaultPatches', request_body=referenced_body)},
        },
    )

    generator, source = _generate(tmp_path, spec)
    endpoints = {endpoint.name: endpoint for _, endpoint in generator.all_endpoints()}
    inline_endpoint = endpoints['remove_identities']
    referenced_endpoint = endpoints['apply_patches']
    default_name_endpoint = endpoints['apply_default_patches']

    assert inline_endpoint.body_is_raw is True
    assert inline_endpoint.request_media_type == 'application/json-patch+json'
    assert [(parameter.name, parameter.python_type) for parameter in inline_endpoint.body_parameter] == [
        ('body', 'list[str]')
    ]
    assert referenced_endpoint.body_is_raw is True
    assert [(parameter.name, parameter.python_type) for parameter in referenced_endpoint.body_parameter] == [
        ('documents', 'list[PatchDocument]')
    ]
    assert [(parameter.name, parameter.python_type) for parameter in default_name_endpoint.body_parameter] == [
        ('PatchRequest', 'list[PatchDocument]')
    ]
    assert "super().patch(url, json=body, content_type='application/json-patch+json')" in source
    assert 'body = TypeAdapter(list[PatchDocument]).dump_python(documents,' in source


def test_generated_identifiers_handle_argument_collisions_and_keywords(tmp_path: Path) -> None:
    """Keep generated source valid for duplicate wire names and Python-keyword enum values.

    :param tmp_path: Pytest-provided temporary directory.
    """
    operation = _operation(
        'updateThing',
        request_body={
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'required': ['name'],
                        'properties': {
                            'id': {'type': 'string'},
                            'name': {'type': 'string'},
                        },
                    }
                }
            },
        },
        response_schema={'$ref': '#/components/schemas/Action'},
    )
    operation['parameters'] = [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'schema': {'type': 'string'},
        }
    ]
    spec = _minimal_spec(
        {'Action': {'type': 'string', 'enum': ['CONTINUE', 'TRANSFER']}},
        {'/things/{id}': {'put': operation}},
    )

    _, source = _generate(tmp_path, spec)

    compile(source, '<generated-identifiers>', 'exec')
    assert "continue_ = 'CONTINUE'" in source
    assert 'body_id: str = None' in source
    assert "body['id'] = body_id" in source

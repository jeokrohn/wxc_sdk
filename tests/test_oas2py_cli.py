"""Integration tests for the OpenAPI-to-Python command-line interface."""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[1]
OAS2PY = REPO_ROOT / 'script' / 'oas2py.py'


def _write_api(
    openapi_root: Path,
    api_name: str,
    api_type: str,
    spec: dict[str, object],
) -> Path:
    """Write a synthetic API metadata file and specification.

    :param openapi_root: Root of the synthetic OpenAPI repository.
    :param api_name: Name of the synthetic API.
    :param api_type: API type stored in ``api.json``.
    :param spec: JSON specification payload.
    :return: Path to the created ``spec.json``.
    """
    api_dir = openapi_root / 'production' / 'Test' / api_name
    spec_dir = api_dir / 'v1'
    spec_dir.mkdir(parents=True)
    (api_dir / 'api.json').write_text(
        json.dumps(
            {
                'apiId': api_name,
                'owners': ['owner@example.com'],
                'apiType': api_type,
                'versions': [{'version': 'v1', 'featureToggles': []}],
            }
        )
    )
    spec_path = spec_dir / 'spec.json'
    spec_path.write_text(json.dumps(spec))
    return spec_path


def _minimal_openapi_spec() -> dict[str, object]:
    """Return a minimal valid OpenAPI document.

    :return: OpenAPI document with no paths or schemas.
    """
    return {
        'openapi': '3.0.3',
        'info': {
            'title': 'Synthetic REST API',
            'description': 'REST fixture for CLI generation.',
            'version': '1.0.0',
        },
        'servers': [{'url': 'https://example.com'}],
        'paths': {},
        'components': {'schemas': {}},
    }


def _extended_openapi_spec() -> dict[str, object]:
    """Return one document combining the newly supported OpenAPI constructs.

    :return: OpenAPI document covering composition, recursion, extensions, and raw bodies.
    """
    body_schema = {
        'type': 'object',
        'required': ['name'],
        'properties': {'name': {'type': 'string'}},
    }
    return {
        'openapi': '3.1.0',
        'info': {
            'title': 'Extended REST API',
            'description': 'Regression fixture for previously unsupported constructs.',
            'version': '1.0.0',
        },
        'servers': [{'url': 'https://example.com'}],
        'paths': {
            '/nodes': {
                'post': {
                    'summary': 'Create a node',
                    'operationId': 'createNode',
                    'x-codegen-request-body-name': 'node',
                    'x-unrelated-extension': True,
                    'parameters': [
                        {
                            'name': 'traceId',
                            'in': 'query',
                            'schema': {'type': 'string'},
                            'examples': {'sample': {'value': 'trace-1'}},
                        }
                    ],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'multipart/form-data': {'schema': body_schema},
                            'application/json': {'schema': body_schema},
                        },
                    },
                    'responses': {
                        '200': {
                            'description': 'Success',
                            'content': {
                                'application/json': {
                                    'schema': {'$ref': '#/components/schemas/Acknowledgement'},
                                }
                            },
                        }
                    },
                },
            },
            '/patches': {
                'patch': {
                    'summary': 'Apply patches',
                    'operationId': 'applyPatches',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json-patch+json': {
                                'schema': {'$ref': '#/components/schemas/PatchRequest'},
                            }
                        },
                    },
                    'responses': {
                        '200': {
                            'description': 'Success',
                            'content': {
                                'application/json': {
                                    'schema': {'$ref': '#/components/schemas/RecursiveNode'},
                                }
                            },
                        }
                    },
                }
            },
        },
        'components': {
            'schemas': {
                'BaseNode': {
                    'type': 'object',
                    'required': ['name'],
                    'properties': {'name': {'type': 'string'}},
                },
                'RecursiveNode': {
                    'allOf': [
                        {'$ref': '#/components/schemas/BaseNode'},
                        {
                            'type': 'object',
                            'properties': {
                                'children': {
                                    'type': 'array',
                                    'items': {'$ref': '#/components/schemas/RecursiveNode'},
                                },
                                'metadata': {
                                    'description': 'Intentionally unconstrained metadata.',
                                    'example': {'source': 'test'},
                                },
                            },
                        },
                    ],
                },
                'PatchRequest': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'examples': [['replace /name']],
                },
                'Selector': {
                    'type': 'object',
                    'nullable': True,
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
                },
                'Acknowledgement': {'type': 'string', 'example': 'OK'},
            }
        },
    }


def _run_oas2py(openapi_root: Path, output_path: Path) -> subprocess.CompletedProcess[str]:
    """Run the CLI against all synthetic specifications.

    :param openapi_root: Root of the synthetic OpenAPI repository.
    :param output_path: Destination for generated Python source.
    :return: Completed subprocess result with captured output.
    """
    return subprocess.run(
        [
            sys.executable,
            str(OAS2PY),
            '--oas',
            str(openapi_root / '**'),
            '--pysrc',
            str(output_path),
            '--body-style',
            'args',
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_cli_skips_grpc_and_generates_supported_spec(tmp_path: Path) -> None:
    """Generate supported input while reporting and skipping gRPC.

    :param tmp_path: Pytest-provided temporary directory.
    """
    openapi_root = tmp_path / 'openapi'
    rest_path = _write_api(openapi_root, 'rest-api', 'rest', _minimal_openapi_spec())
    grpc_path = _write_api(openapi_root, 'grpc-api', 'grpc', {'files': [{'name': 'service.proto'}]})
    output_path = tmp_path / 'generated.py'

    result = _run_oas2py(openapi_root, output_path)

    assert result.returncode == 0, result.stderr
    assert f'Conversion of "{rest_path}"' in result.stdout
    assert f'Skipping "{grpc_path}" (apiType: grpc)' in result.stdout
    assert output_path.is_file()


def test_cli_with_only_grpc_input_succeeds_without_output(tmp_path: Path) -> None:
    """Treat a gRPC-only selection as a successful no-op.

    :param tmp_path: Pytest-provided temporary directory.
    """
    openapi_root = tmp_path / 'openapi'
    grpc_path = _write_api(openapi_root, 'grpc-api', 'grpc', {'files': [{'name': 'service.proto'}]})
    output_path = tmp_path / 'generated.py'

    result = _run_oas2py(openapi_root, output_path)

    assert result.returncode == 0, result.stderr
    assert f'Skipping "{grpc_path}" (apiType: grpc)' in result.stdout
    assert not output_path.exists()


def test_cli_still_reports_malformed_rest_spec(tmp_path: Path) -> None:
    """Keep malformed supported specifications in the failure path.

    :param tmp_path: Pytest-provided temporary directory.
    """
    openapi_root = tmp_path / 'openapi'
    malformed_path = _write_api(openapi_root, 'malformed-rest-api', 'rest', {})
    output_path = tmp_path / 'generated.py'

    result = _run_oas2py(openapi_root, output_path)

    assert result.returncode == 1
    assert f'Conversion of "{malformed_path}" failed:' in result.stderr
    assert 'validation errors for OASpec' in result.stderr
    assert f'{malformed_path}: ValidationError:' in result.stderr
    assert not output_path.exists()


def test_cli_generates_extended_openapi_constructs(tmp_path: Path) -> None:
    """Generate one corpus-style fixture containing all newly supported constructs.

    :param tmp_path: Pytest-provided temporary directory.
    """
    openapi_root = tmp_path / 'openapi'
    spec_path = _write_api(openapi_root, 'extended-rest-api', 'rest', _extended_openapi_spec())
    output_path = tmp_path / 'generated.py'

    result = _run_oas2py(openapi_root, output_path)

    assert result.returncode == 0, result.stderr
    assert f'Conversion of "{spec_path}"' in result.stdout
    assert 'OAS files failed' not in result.stderr
    source = output_path.read_text(encoding='utf-8')
    compile(source, str(output_path), 'exec')

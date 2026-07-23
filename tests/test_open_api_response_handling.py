"""
Regression tests for OpenAPI endpoint response handling.
"""

import json
import logging
from pathlib import Path
from typing import Any

import pytest

from apib.python_class import Endpoint
from open_api.open_api_code_generator import OACodeGenerator
from open_api.open_api_sources import OpenApiSpecInfo

REGISTRY_LOGGER = 'open_api.open_api_class_registry'
DELETE_FALLBACK_WARNING = 'No 2xx response defined for DELETE endpoint delete_thing; assuming 204 No Content'


def _minimal_spec(method: str, responses: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """
    Build a minimal OpenAPI document with one endpoint.

    :param method: HTTP method to use for the endpoint.
    :type method: str
    :param responses: Response objects keyed by HTTP status code.
    :type responses: dict[str, dict[str, Any]]
    :return: Minimal OpenAPI document suitable for code generation.
    :rtype: dict[str, Any]
    """
    operation_id = f'{method.lower()}Thing'
    return {
        'openapi': '3.0.3',
        'info': {
            'title': 'Response Handling Test',
            'version': '1.0.0',
            'description': 'Minimal OpenAPI document for response-handling regression coverage.',
        },
        'servers': [{'url': 'https://example.test'}],
        'paths': {
            '/things': {
                method.lower(): {
                    'summary': f'{method.title()} thing',
                    'operationId': operation_id,
                    'description': f'{method.title()} a thing.',
                    'responses': responses,
                }
            }
        },
        'components': {'schemas': {}},
    }


def _generate_endpoint(tmp_path: Path, method: str, responses: dict[str, dict[str, Any]]) -> tuple[Endpoint, str]:
    """
    Generate endpoint metadata and Python source from a minimal specification.

    :param tmp_path: Temporary directory in which to store the input specification.
    :type tmp_path: Path
    :param method: HTTP method to use for the endpoint.
    :type method: str
    :param responses: Response objects keyed by HTTP status code.
    :type responses: dict[str, dict[str, Any]]
    :return: Generated endpoint metadata and complete Python module source.
    :rtype: tuple[Endpoint, str]
    :raises ValueError: If the response configuration cannot be converted into an endpoint.

    The helper writes a temporary ``spec.json`` file below ``tmp_path``.
    """
    spec_path = tmp_path / 'spec.json'
    spec_path.write_text(json.dumps(_minimal_spec(method, responses)), encoding='utf-8')

    code_gen = OACodeGenerator()
    code_gen.add_open_api_spec(
        OpenApiSpecInfo(
            api_name='response-handling-test',
            base_path=str(tmp_path),
            spec_path=str(spec_path),
            version='v1',
        )
    )
    code_gen.cleanup()
    endpoint = next(endpoint for _, endpoint in code_gen.all_endpoints())
    return endpoint, code_gen.source(with_example=False)


def test_delete_without_success_response_assumes_empty_204(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """
    Generate an empty-result DELETE endpoint when the spec documents only errors.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: Path
    :param caplog: Pytest log capture fixture.
    :type caplog: pytest.LogCaptureFixture
    :return: None.
    :rtype: None
    """
    with caplog.at_level(logging.WARNING, logger=REGISTRY_LOGGER):
        endpoint, source = _generate_endpoint(
            tmp_path,
            'delete',
            {'404': {'description': 'Not Found'}},
        )

    assert endpoint.result is None
    assert endpoint.response_body is None
    assert 'def delete_thing(self) -> None:' in source
    assert 'super().delete(url)' in source
    assert DELETE_FALLBACK_WARNING in caplog.messages


def test_delete_with_explicit_204_does_not_use_fallback(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """
    Preserve an explicitly documented DELETE ``204`` response without warning.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: Path
    :param caplog: Pytest log capture fixture.
    :type caplog: pytest.LogCaptureFixture
    :return: None.
    :rtype: None
    """
    with caplog.at_level(logging.WARNING, logger=REGISTRY_LOGGER):
        endpoint, source = _generate_endpoint(
            tmp_path,
            'delete',
            {'204': {'description': 'No Content'}},
        )

    assert endpoint.result is None
    assert endpoint.response_body is None
    assert 'def delete_thing(self) -> None:' in source
    assert 'super().delete(url)' in source
    assert DELETE_FALLBACK_WARNING not in caplog.messages


def test_non_delete_without_success_response_still_fails(tmp_path: Path) -> None:
    """
    Reject a non-DELETE operation that has no documented successful response.

    :param tmp_path: Pytest-provided temporary directory.
    :type tmp_path: Path
    :return: None.
    :rtype: None
    """
    with pytest.raises(ValueError, match=r'unexpected response code None for get_thing'):
        _generate_endpoint(
            tmp_path,
            'get',
            {'404': {'description': 'Not Found'}},
        )

"""Tests for OpenAPI source discovery and code-generation eligibility."""

import json
from pathlib import Path

import pytest

from open_api import open_api_sources
from open_api.open_api_sources import APIConfig, OpenApiSpecInfo


def _api_config(api_type: str) -> APIConfig:
    """Create API metadata for a synthetic specification.

    :param api_type: API type stored in the synthetic ``api.json`` metadata.
    :return: Validated API configuration.
    """
    return APIConfig.model_validate(
        {
            'apiId': f'{api_type}-api',
            'owners': ['owner@example.com'],
            'apiType': api_type,
            'versions': [{'version': 'v1', 'featureToggles': []}],
        }
    )


def _write_spec(root: Path, api_name: str, api_type: str | None) -> Path:
    """Write a synthetic specification and optional API metadata.

    :param root: Temporary OpenAPI repository root.
    :param api_name: Name of the synthetic API.
    :param api_type: API type to write, or ``None`` to omit ``api.json``.
    :return: Path to the created ``spec.json`` file.
    """
    api_dir = root / 'production' / 'Test' / api_name
    spec_dir = api_dir / 'v1'
    spec_dir.mkdir(parents=True)
    spec_path = spec_dir / 'spec.json'
    spec_path.write_text('{}')
    if api_type is not None:
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
    return spec_path


@pytest.mark.parametrize(
    ('api_type', 'expected'),
    [
        ('rest', True),
        ('graphql', True),
        ('grpc', False),
        ('future-api-type', True),
    ],
)
def test_supports_oas_codegen_uses_api_type_metadata(api_type: str, expected: bool) -> None:
    """Classify only explicitly declared gRPC APIs as unsupported.

    :param api_type: API type under test.
    :param expected: Expected code-generation eligibility.
    """
    spec_info = OpenApiSpecInfo(
        api_name='example',
        base_path='/tmp/openapi',
        spec_path='/tmp/openapi/example/v1/spec.json',
        version='v1',
        api_config=_api_config(api_type),
    )

    assert spec_info.supports_oas_codegen is expected


def test_supports_oas_codegen_for_public_spec(tmp_path: Path) -> None:
    """Keep public specifications without ``api.json`` metadata eligible.

    :param tmp_path: Pytest-provided temporary directory.
    """
    public_spec_dir = tmp_path / 'public-spec'
    public_spec_dir.mkdir()
    spec_path = public_spec_dir / 'example.json'
    spec_path.write_text('{}')

    spec_info = OpenApiSpecInfo.from_spec_json_path(str(spec_path))

    assert spec_info.api_config is None
    assert spec_info.supports_oas_codegen is True


def test_open_api_specs_excludes_grpc_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Yield supported specifications while excluding gRPC descriptors.

    :param tmp_path: Pytest-provided temporary directory.
    :param monkeypatch: Pytest helper used to point discovery at the fixture.
    """
    workspace_dir = tmp_path / 'open-api-specs'
    openapi_root = workspace_dir / 'openapi'
    expected_paths = {
        _write_spec(openapi_root, 'rest-api', 'rest'),
        _write_spec(openapi_root, 'graphql-api', 'graphql'),
        _write_spec(openapi_root, 'metadata-free-api', None),
    }
    grpc_path = _write_spec(openapi_root, 'grpc-api', 'grpc')
    monkeypatch.setattr(open_api_sources, 'WORKSPACE_BASE', str(tmp_path))
    monkeypatch.setattr(open_api_sources, 'WORKSPACE_DIR', workspace_dir.name)

    discovered_paths = {Path(spec.spec_path) for spec in open_api_sources.open_api_specs()}

    assert discovered_paths == expected_paths
    assert grpc_path not in discovered_paths

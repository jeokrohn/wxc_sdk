"""
access OpenAPI sources
"""
import glob
import json
import os
import re
from collections.abc import Generator
from dataclasses import dataclass

__all__ = ['OpenApiSpecInfo', 'open_api_specs']

from typing import List, Optional

from pydantic import BaseModel, Field

WORKSPACE_DIR = 'open-api-specs'  # directory where OpenAPI specs are stored under the workspace
WORKSPACE_BASE = os.path.expanduser(os.path.join('~', 'Documents', 'workspace'))


class PublishItem(BaseModel):
    api_group: str = Field(..., alias='apiGroup')


class VisibilityItem(BaseModel):
    access_level: int = Field(..., alias='accessLevel')

class FeatureToggle(BaseModel):
    method: str
    path: str
    toggle_name: str = Field(..., alias='toggleName')

class APIVersion(BaseModel):
    version: str
    feature_toggles: List[FeatureToggle] = Field(..., alias='featureToggles')

class APIConfig(BaseModel):
    api_id: str = Field(..., alias='apiId')
    owners: list[str]
    api_type: str = Field(..., alias='apiType')
    versions: list[APIVersion]
    publish_to: List[str] = Field(..., alias='publishTo')


@dataclass
class OpenApiSpecInfo:
    """
    Information of one OpenAPI spec
    """
    api_name: str
    base_path: str
    spec_path: str
    version: str

    api_config: Optional[APIConfig] = None

    @property
    def rel_spec_path(self)->str:
        path = self.spec_path[len(self.base_path):]
        m = re.match(r'^/(.+)/v\d', path)
        path = m.group(1)
        return path

    @classmethod
    def from_spec_json_path(cls, path: str) -> 'OpenApiSpecInfo':
        """
        Create OpenApiSpecInfo from path to spec.json
        """
        path_match = re.match(r'^(.+/openapi)/(.+)/(v\d)/spec.json$', path)
        if path_match is None:
            raise ValueError(f"Invalid path: {path}")
        base_path = path_match.group(1)
        spec_path = path_match.group(2)
        version = path_match.group(3)
        api_name = spec_path.split('/')[-1]

        api_json_path = os.path.join(base_path, spec_path, 'api.json')
        try:
            with open(api_json_path) as f:
                data = json.load(f)
                api_config = APIConfig.model_validate(data)
        except FileNotFoundError:
            api_config = None
        return cls(base_path=base_path, spec_path=path, api_config=api_config, version=version, api_name=api_name)

def open_api_specs() -> Generator[OpenApiSpecInfo, None, None]:
    """
    Generator of OpenAPI specs
    """
    base_dir = os.path.expanduser(os.path.join(WORKSPACE_BASE, WORKSPACE_DIR, 'openapi'))
    assert os.path.exists(base_dir), f"Directory {base_dir} does not exist"
    search_spec = os.path.join(base_dir, '**', 'spec.json')
    specs = glob.glob(search_spec, recursive=True)
    for spec in specs:
        yield OpenApiSpecInfo.from_spec_json_path(spec)

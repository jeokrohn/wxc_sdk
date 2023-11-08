from collections.abc import Generator
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['DeveloperRegistrationGetResponse', 'DeveloperRegistrationUpdateRequest', 'SkillCreateRequest',
            'SkillCreateRequestLanguages', 'SkillCreateResponse']


class SkillCreateRequestLanguages(str, Enum):
    en = 'en'
    es = 'es'
    fr = 'fr'


class SkillCreateRequest(ApiModel):
    languages: Optional[list[SkillCreateRequestLanguages]] = None
    url: Optional[str] = None
    name: Optional[str] = None
    contact_email: Optional[str] = Field(alias='contact_email', default=None)
    secret: Optional[str] = None
    public_key: Optional[str] = Field(alias='public_key', default=None)
    #: example: ['[]']
    suggested_invocation_names: Optional[list[str]] = Field(alias='suggested_invocation_names', default=None)


class SkillCreateResponse(ApiModel):
    skill_id: Optional[str] = Field(alias='skill_id', default=None)
    developer_id: Optional[str] = Field(alias='developer_id', default=None)
    url: Optional[str] = None
    name: Optional[str] = None
    contact_email: Optional[str] = Field(alias='contact_email', default=None)
    public: Optional[bool] = None
    deleted: Optional[bool] = None
    created_at: Optional[str] = Field(alias='created_at', default=None)
    deleted_at: Optional[str] = Field(alias='deleted_at', default=None)
    modified_at: Optional[str] = Field(alias='modified_at', default=None)
    #: example: ['[]']
    suggested_invocation_names: Optional[list[str]] = Field(alias='suggested_invocation_names', default=None)
    languages: Optional[list[str]] = None


class DeveloperRegistrationGetResponse(ApiModel):
    registration_id: Optional[str] = Field(alias='registration_id', default=None)
    skill_id: Optional[str] = Field(alias='skill_id', default=None)
    enabled: Optional[bool] = None
    languages: Optional[list[str]] = None
    invocation_names: Optional[list[str]] = Field(alias='invocation_names', default=None)
    created_at: Optional[str] = Field(alias='created_at', default=None)
    modified_at: Optional[str] = Field(alias='modified_at', default=None)
    developer_id: Optional[str] = Field(alias='developer_id', default=None)


class DeveloperRegistrationUpdateRequest(ApiModel):
    invocation_names: Optional[list[str]] = Field(alias='invocation_names', default=None)


class AssistantSkillsServiceAPIApi(ApiChild, base=''):
    """
    Assistant Skills Service API
    
    Develop custom skills to use with the Webex Assistant.
    
    ## Authentication
    
    Uses OAuth v2 Bearer Token / Personal Access Token for its authentication.
    """
    ...
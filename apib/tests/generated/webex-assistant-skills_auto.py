from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['DeveloperRegistrationGetResponse', 'DeveloperRegistrationUpdateRequest', 'SkillCreateRequest', 'SkillCreateRequestLanguages', 'SkillCreateResponse']


class SkillCreateRequestLanguages(str, Enum):
    en = 'en'
    es = 'es'
    fr = 'fr'


class SkillCreateRequest(ApiModel):
    languages: Optional[list[SkillCreateRequestLanguages]] = None
    url: Optional[str] = None
    name: Optional[str] = None
    contact_email: Optional[str] = None
    secret: Optional[str] = None
    public_key: Optional[str] = None
    #: example: ['[]']
    suggested_invocation_names: Optional[list[str]] = None


class SkillCreateResponse(ApiModel):
    skill_id: Optional[str] = None
    developer_id: Optional[str] = None
    url: Optional[str] = None
    name: Optional[str] = None
    contact_email: Optional[str] = None
    public: Optional[bool] = None
    deleted: Optional[bool] = None
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    modified_at: Optional[str] = None
    #: example: ['[]']
    suggested_invocation_names: Optional[list[str]] = None
    languages: Optional[list[str]] = None


class DeveloperRegistrationGetResponse(ApiModel):
    registration_id: Optional[str] = None
    skill_id: Optional[str] = None
    enabled: Optional[bool] = None
    languages: Optional[list[str]] = None
    invocation_names: Optional[list[str]] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    developer_id: Optional[str] = None


class DeveloperRegistrationUpdateRequest(ApiModel):
    invocation_names: Optional[list[str]] = None

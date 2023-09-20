from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Template', 'ValidationRules', 'ValidationRulesCollection']


class ValidationRules(ApiModel):
    #: Field on which validation rule is applied
    #: example: templateId
    field: Optional[str] = None
    #: Whether the above field is required
    #: example: yes
    required: Optional[str] = None


class ValidationRulesCollection(ApiModel):
    #: An array of validation rules
    validations: Optional[list[ValidationRules]] = None


class Template(ApiModel):
    #: Unique identifier representing a report.
    #: example: 130
    id: Optional[datetime] = None
    #: Name of the template.
    #: example: Client Version
    title: Optional[str] = None
    #: The service to which the report belongs.
    #: example: Teams
    service: Optional[str] = None
    #: Maximum date range for reports belonging to this template.
    #: example: 31.0
    maxDays: Optional[int] = None
    #: Generated reports belong to which field.
    #: example: orgWithoutDate
    identifier: Optional[str] = None
    validations: Optional[ValidationRulesCollection] = None

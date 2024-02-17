from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ReportTemplatesApi', 'Template', 'ValidationRules', 'ValidationRulesCollection']


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
    id: Optional[str] = None
    #: Name of the template.
    #: example: Client Version
    title: Optional[str] = None
    #: The service to which the report belongs.
    #: example: Teams
    service: Optional[str] = None
    #: Maximum date range for reports belonging to this template.
    #: example: 31
    max_days: Optional[int] = None
    #: Generated reports belong to which field.
    #: example: orgWithoutDate
    identifier: Optional[str] = None
    validations: Optional[ValidationRulesCollection] = None


class ReportTemplatesApi(ApiChild, base='report/templates'):
    """
    Report Templates
    
    Report templates are available for use with the `Reports API
    <https://developer.webex.com/docs/api/v1/reports>`_.
    
    To access this endpoint, you must use an administrator token with the `analytics:read_all` `scope
    <https://developer.webex.com/docs/integrations#scopes>`_. The authenticated
    user must be a read-only or full administrator of the organization to which the report belongs.
    
    To use this endpoint the organization needs to be licensed for `Pro Pack for Control Hub
    <https://help.webex.com/article/np3c1rm/Pro-Pack-For-Control-Hub>`_.
    
    For more information about Report Templates, see the `Admin API
    <https://developer.webex.com/docs/admin#reports-api>`_ guide.
    """

    def list_report_templates(self) -> list[Template]:
        """
        List Report Templates

        List all the available report templates that can be generated.

        CSV (comma separated value) reports for Webex services are only supported for organizations based in the North
        American region. Organizations based in other regions will return blank CSV files for any Webex reports.

        :rtype: list[Template]
        """
        url = self.ep()
        data = super().get(url)
        r = TypeAdapter(list[Template]).validate_python(data)
        return r

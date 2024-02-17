from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['OrganizationLicenseTemplatesApi', 'Template', 'TemplateTemplateType']


class TemplateTemplateType(str, Enum):
    org = 'ORG'
    group = 'GROUP'


class Template(ApiModel):
    #: A unique identifier for a license template
    #: example: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: Name of the org level template
    #: example: Default
    template_name: Optional[str] = None
    #: An array of license strings
    #: example: ['Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh', 'Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi']
    licenses: Optional[list[str]] = None
    #: Specify the template type to be created ORG or GROUP
    template_type: Optional[TemplateTemplateType] = None
    #: An array of group ids associated with template
    #: example: ['Y2lzY29zcGFyazovL45zL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh', 'Y2lzY29zcGFyazovL3VzL0xOU0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh']
    groups: Optional[list[str]] = None


class OrganizationLicenseTemplatesApi(ApiChild, base='organization'):
    """
    Organization License Templates
    
    These APIs allow a Webex organization administrator to list, create, update, and delete license templates for their
    groups. Admins can create org- and group-level templates. If a user is part of a group, they are assigned the
    group-level templates. Users who are not part of a group will default to org-level templates.
    
    To list templates at the organization level you need an admin auth token with a scope of
    `spark-admin:licenses_read` to view templates at the org level. Adding, updating, and removing templates requires
    an admin auth token with the `spark-admin:licenses_write` scope.
    """

    def list_organization_license_templates(self, org_id: str) -> list[Template]:
        """
        List Organization License Templates

        Get org level license templates

        :param org_id: A unique identifier for an org
        :type org_id: str
        :rtype: list[Template]
        """
        url = self.ep(f'licenseTemplates?orgId={org_id}')
        data = super().get(url)
        r = TypeAdapter(list[Template]).validate_python(data['items'])
        return r

    def create_an_organization_license_template(self, org_id: str, template_name: str = None,
                                                licenses: list[str] = None, groups: list[str] = None,
                                                template_type: TemplateTemplateType = None) -> Template:
        """
        Create an Organization License Template

        Create an org/group level license template which could be assigned to users as part of user onboarding.
        Only group level templates can be associated with groups

        :param org_id: A unique identifier for an org
        :type org_id: str
        :param template_name: Name of the org level template
        :type template_name: str
        :param licenses: An array of license strings
        :type licenses: list[str]
        :param groups: An array of groups
        :type groups: list[str]
        :param template_type: Specify the template type to be created
        :type template_type: TemplateTemplateType
        :rtype: :class:`Template`
        """
        body = dict()
        if template_name is not None:
            body['templateName'] = template_name
        if licenses is not None:
            body['licenses'] = licenses
        if groups is not None:
            body['groups'] = groups
        if template_type is not None:
            body['templateType'] = enum_str(template_type)
        body['orgId'] = org_id
        url = self.ep('licenseTemplates')
        data = super().post(url, json=body)
        r = Template.model_validate(data)
        return r

    def update_an_organization_license_template(self, license_template_id: str, org_id: str, template_name: str = None,
                                                licenses: list[str] = None, groups: list[str] = None) -> Template:
        """
        Update an Organization License Template

        Update org/group license template

        Specify the templateId in the `licenseTemplateId` parameter in the URI

        :param license_template_id: A unique identifier of a template
        :type license_template_id: str
        :param org_id: A unique identifier for an org
        :type org_id: str
        :param template_name: Name of the org level template
        :type template_name: str
        :param licenses: An array of license strings
        :type licenses: list[str]
        :param groups: An array of groups
        :type groups: list[str]
        :rtype: :class:`Template`
        """
        body = dict()
        if template_name is not None:
            body['templateName'] = template_name
        if licenses is not None:
            body['licenses'] = licenses
        if groups is not None:
            body['groups'] = groups
        body['orgId'] = org_id
        url = self.ep(f'licenseTemplates/{license_template_id}')
        data = super().put(url, json=body)
        r = Template.model_validate(data)
        return r

    def delete_an_organization_license_template(self, license_template_id: str):
        """
        Delete an Organization License Template

        Delete an org/group level template

        Specify the templateId in the `licenseTemplateId` parameter in the URI

        :param license_template_id: A unique identifier of a template
        :type license_template_id: str
        :rtype: None
        """
        url = self.ep(f'licenseTemplates/{license_template_id}')
        super().delete(url)

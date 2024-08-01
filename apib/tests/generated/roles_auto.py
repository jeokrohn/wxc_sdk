from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Role', 'RolesApi']


class Role(ApiModel):
    #: A unique identifier for the role.
    #: example: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh
    id: Optional[str] = None
    #: The name of the role.
    #: example: Full Administrator
    name: Optional[str] = None


class RolesApi(ApiChild, base='roles'):
    """
    Roles
    
    A persona for an authenticated user, corresponding to a set of privileges within an organization.
    """

    def list_roles(self) -> list[Role]:
        """
        List Roles

        List all roles. Must be called by an admin user.

        :rtype: list[Role]
        """
        url = self.ep()
        data = super().get(url)
        r = TypeAdapter(list[Role]).validate_python(data['items'])
        return r

    def get_role_details(self, role_id: str) -> Role:
        """
        Get Role Details

        Shows details for a role, by ID.

        Specify the role ID in the `roleId` parameter in the URI.

        :param role_id: The unique identifier for the role.
        :type role_id: str
        :rtype: :class:`Role`
        """
        url = self.ep(f'{role_id}')
        data = super().get(url)
        r = Role.model_validate(data)
        return r

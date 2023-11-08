from collections.abc import Generator
from datetime import datetime
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetPersonOrWorkspaceDetailsObject', 'GetPersonOrWorkspaceDetailsObjectDepartment',
            'PutPersonOrWorkspaceDetailsObject', 'PutPersonOrWorkspaceDetailsObjectDepartment']


class GetPersonOrWorkspaceDetailsObjectDepartment(ApiModel):
    #: Unique identifier of the department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None
    #: Name of the department.
    #: example: HR
    name: Optional[str] = None


class GetPersonOrWorkspaceDetailsObject(ApiModel):
    #: Specifies the department information.
    department: Optional[GetPersonOrWorkspaceDetailsObjectDepartment] = None


class PutPersonOrWorkspaceDetailsObjectDepartment(ApiModel):
    #: Unique identifier of the department.  Set to null to remove entity from department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None


class PutPersonOrWorkspaceDetailsObject(ApiModel):
    #: Specifies the department information.
    department: Optional[PutPersonOrWorkspaceDetailsObjectDepartment] = None


class BetaUserCallSettingsWithDepartmentFeaturesApi(ApiChild, base='telephony/config/people/{personId}'):
    """
    Beta User Call Settings with Department Features
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Person Call Settings supports modifying Webex Calling settings for a specific person.
    
    Viewing People requires a full, user, or read-only administrator auth token with a scope of
    `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by a
    person to read their own settings.
    
    Configuring People settings requires a full or user administrator auth token with the `spark-admin:people_write`
    scope or, for select APIs, a user auth token with `spark:people_write` scope can be used by a person to update
    their own settings.
    """

    def read_department_of_a_person(self, person_id: str,
                                    org_id: str = None) -> GetPersonOrWorkspaceDetailsObjectDepartment:
        """
        Read Department of a Person

        Retrieve a person's department membership.
        
        An admin can organize people, workspaces, and features by placing them into departments. Departments can span
        locations.
        
        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Retrieve department membership of this person.
        :type person_id: str
        :param org_id: Person is in this organization.
        :type org_id: str
        :rtype: GetPersonOrWorkspaceDetailsObjectDepartment
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'')
        ...


    def update_department_of_a_person(self, person_id: str, department: PutPersonOrWorkspaceDetailsObjectDepartment,
                                      org_id: str = None):
        """
        Update Department of a Person

        Modify a person's department membership.
        
        An admin can organize people, workspaces, and features by placing them into departments. Departments can span
        locations.
        
        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Modify department membership of this person.
        :type person_id: str
        :param department: Specifies the department information.
        :type department: PutPersonOrWorkspaceDetailsObjectDepartment
        :param org_id: Person is in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'')
        ...

    ...
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
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
    ...
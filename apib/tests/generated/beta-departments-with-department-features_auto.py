from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['DepartmentCollectionRequest', 'DepartmentCollectionResponse', 'DepartmentResponse',
            'DepartmentResponseDepartment', 'DepartmentResponseWithId']


class DepartmentCollectionRequest(ApiModel):
    #: Name of the department.
    #: example: HR
    name: Optional[str] = None


class DepartmentResponseDepartment(ApiModel):
    #: Unique identifier of the department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None
    #: Name of the department.
    #: example: HR
    name: Optional[str] = None
    #: Number of members in this department.
    #: example: 2.0
    member_count: Optional[int] = None


class DepartmentResponse(ApiModel):
    #: Specifies the department information.
    department: Optional[DepartmentResponseDepartment] = None


class DepartmentCollectionResponse(ApiModel):
    #: List of departments.
    departments: Optional[list[DepartmentResponse]] = None


class DepartmentResponseWithId(ApiModel):
    #: Unique identifier of the department.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvZjA2ZWRiOGMtMjMxNC00ZTcxLWIzNzgtZTdiMmQwNjk3OTliOjk2YWJjMmFhLTNkY2MtMTFlNS1hMTUyLWZlMzQ4MTljZGM5YQ
    id: Optional[str] = None


class BetaDepartmentsWithDepartmentFeaturesApi(ApiChild, base='telephony/config/departments'):
    """
    Beta Departments with Department Features
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Webex Calling Organization Settings support reading and writing of Webex Calling settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `OrgId`
    query parameter.
    
    Only organization settings with department-related fields are listed.  For department membership, please refer to
    `Get Group Members API
    <https://developer.webex.com/docs/api/v1/groups/get-group-members>`_ to retrieve members of a department group.
    
    The use of the `/groups` API for departments is supported in a read-only
    manner only. Modification of a department via the `/groups` API is
    unsupported.
    
    """
    ...
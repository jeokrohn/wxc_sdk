from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['DepartmentCollectionRequest', 'DepartmentCollectionResponse', 'DepartmentResponse', 'DepartmentResponseDepartment', 'DepartmentResponseWithId']


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
    memberCount: Optional[int] = None


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

from collections.abc import Generator
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

    def get_a_list_of_departments(self, org_id: str = None, start: int = None, max_: int = None, name: str = None,
                                  id: str = None, **params) -> Generator[DepartmentResponse, None, None]:
        """
        Get a List of Departments

        Retrieve a list of departments.
        
        Admin can organize people, workspaces, and features by placing them into departments. Departments can span
        locations.
        
        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Retrieve list of departments for this organization.
        :type org_id: str
        :param start: Specifies the offset from the first result that you want to fetch.
        :type start: int
        :param max_: Specifies the maximum number of records that you want to fetch.
        :type max_: int
        :param name: Specifies the case insensitive substring to be matched against the department names.
        :type name: str
        :param id: Specifies the department ID you want to fetch.
        :type id: str
        :return: Generator yielding :class:`DepartmentResponse` instances
        """
        ...


    def create_a_department(self, name: str, org_id: str = None) -> str:
        """
        Create a Department

        This API is used to create a department in an organization.
        
        An admin can organize people, workspaces, and features by placing them into departments. Departments can span
        locations.
        
        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param name: Name of the department.
        :type name: str
        :param org_id: Create a department for this organization.
        :type org_id: str
        :rtype: str
        """
        ...


    def delete_a_department(self, department_id: str, org_id: str = None):
        """
        Delete a Department

        This API is used to delete a department by its department id.
        
        An admin can organize people, workspaces, and features by placing them into departments. Departments can span
        locations.
        
        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.
        
        <br/>
        
        <strong> NOTE </strong>: Before deleting a department, please be sure to unassign the resources (such as call
        queues, paging groups, etc.) that are associated with it.
        Unassigning resources from a department happens asynchronously and can take upto 20 seconds to take effect.

        :param department_id: Unique identifier for the department.
        :type department_id: str
        :param org_id: Delete a department from this organization.
        :type org_id: str
        :rtype: None
        """
        ...


    def get_details_of_a_department(self, department_id: str, org_id: str = None) -> DepartmentResponseDepartment:
        """
        Get Details of a Department

        Retrieve details of a department.
        
        An admin can organize people, workspaces, and features by placing them into departments. Departments can span
        locations.
        
        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param department_id: Unique identifier for the department.
        :type department_id: str
        :param org_id: Retrieve details for a department in this organization.
        :type org_id: str
        :rtype: DepartmentResponseDepartment
        """
        ...


    def modify_a_department(self, department_id: str, name: str, org_id: str = None):
        """
        Modify a Department

        This API is used to modify a department in an organization.
        
        An admin can organize people, workspaces, and features by placing them into departments. Departments can span
        locations.
        
        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param department_id: Unique identifier for the department.
        :type department_id: str
        :param name: Name of the department.
        :type name: str
        :param org_id: Modify a department for this organization.
        :type org_id: str
        :rtype: None
        """
        ...

    ...
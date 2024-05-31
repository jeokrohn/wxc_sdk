from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BulkManageSCIM2UsersAndGroupsApi', 'BulkUser', 'BulkUserOperations', 'BulkUserOperationsMethod']


class BulkUserOperationsMethod(str, Enum):
    post = 'POST'
    patch = 'PATCH'
    delete = 'DELETE'


class BulkUserOperations(ApiModel):
    #: The HTTP method of the current operation.
    #: example: PATCH
    method: Optional[BulkUserOperationsMethod] = None
    #: The resource's relative path. If the method is POST, the value must specify a resource type endpoint, for
    #: example `/Users` or `/Groups`. All other method values must specify the path to a specific resource.
    #: example: /Users/2819c223-7f76-453a-919d-413861904646
    path: Optional[str] = None
    #: The Resource JSON data as it appears for a single POST or PATCH resource operation.
    #: example: JSON text
    data: Optional[str] = None
    #: The transient identifier of a newly created resource, unique within a bulk request and created by the client.
    #: example: ytrewq
    bulk_id: Optional[str] = None


class BulkUser(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:api:messages:2.0:BulkRequest']
    schemas: Optional[list[str]] = None
    #: An integer specifying the maximum number of errors that the service provider will accept before the operation is
    #: terminated and an error response is returned.
    #: example: 99
    fail_on_errors: Optional[int] = None
    #: Contains a list of bulk operations for POST/PATCH/DELETE operations.
    operations: Optional[list[BulkUserOperations]] = None


class BulkManageSCIM2UsersAndGroupsApi(ApiChild, base='identity/scim'):
    """
    Bulk Manage SCIM 2 Users and Groups
    
    The bulk API allows you to create, update, and remove multiple users and groups in Webex.  The number of Bulk
    operations in a single request is limited to 100.
    
    Bulk deletion of Users is irreversible. Please test in a test org or sandbox
    before running the command in your production system.
    
    """

    def user_bulk_api(self, org_id: str, schemas: list[str], fail_on_errors: int,
                      operations: list[BulkUserOperations]) -> BulkUser:
        """
        User bulk API

        <br/>

        **Authorization**

        OAuth token rendered by Identity Broker.

        <br/>

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        <br/>

        **Usage**:

        1. The input JSON must conform to the following schema: 'urn:ietf:params:scim:api:messages:2.0:BulkRequest'.

        1. The request must be accompanied with a body in JSON format according to the standard SCIM schema definition.
        The maximum number of operations in a request is 100; an error is thrown if the limit is exceeded.

        1. `failOnErrors` parameter

        An integer specifies the number of errors that the service provider will accept before the operation is
        terminated and an error response is returned.
        It is OPTIONAL in a request.
        Maximum number of operations allowed to fail before the server stops processing the request. The value must be
        between 1 and 100.

        1. `operations` parameter

        Contains a list of bulk operations for POST/PATCH/DELETE operations. (REQUIRED)
        + `operations.method`

        The HTTP method of the current operation. Possible values are POST, PATCH or DELETE.
        + `operations.path`

        The Resource's relative path. If the method is POST the value must specify a Resource type endpoint;
        e.g., /Users or /Groups whereas all other method values must specify the path to a specific Resource;
        e.g., /Users/2819c223-7f76-453a-919d-413861904646.
        + `operations.data`

        The Resource data as it would appear for a single POST or PATCH Resource operation.
        It is REQUIRED in a request when method is POST and PATCH.
        Refer to corresponding wiki for SCIM 2.0 POST, PATCH and DELETE API.
        + `operations.bulkId`

        The transient identifier of a newly created resource, unique within a bulk request and created by the client.
        The bulkId serves as a surrogate resource id enabling clients to uniquely identify newly created resources in
        the response and cross-reference new resources in and across operations within a bulk request.
        It is REQUIRED when "method" is "POST".

        :param org_id: Webex Identity assigned organization identifier for user's organization.
        :type org_id: str
        :param schemas: Input JSON schemas.
        :type schemas: list[str]
        :param fail_on_errors: An integer specifying the maximum number of errors that the service provider will accept
            before the operation is terminated and an error response is returned.
        :type fail_on_errors: int
        :param operations: Contains a list of bulk operations for POST/PATCH/DELETE operations.
        :type operations: list[BulkUserOperations]
        :rtype: :class:`BulkUser`
        """
        body = dict()
        body['schemas'] = schemas
        body['failOnErrors'] = fail_on_errors
        body['operations'] = TypeAdapter(list[BulkUserOperations]).dump_python(operations, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{org_id}/v2/Bulk')
        data = super().post(url, json=body)
        r = BulkUser.model_validate(data)
        return r

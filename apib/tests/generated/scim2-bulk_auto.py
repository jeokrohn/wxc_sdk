from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['BulkUser', 'BulkUserOperations', 'BulkUserOperationsMethod']


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
    #: example: 99.0
    fail_on_errors: Optional[int] = None
    #: Contains a list of bulk operations for POST/PATCH/DELETE operations.
    operations: Optional[list[BulkUserOperations]] = None


class BulkManageSCIM2UsersAndGroupsApi(ApiChild, base='identity/scim/{orgId}/v2/Bulk'):
    """
    Bulk Manage SCIM 2 Users and Groups
    
    The bulk API allows you to create, update, and remove multiple users and groups in Webex.  The number of Bulk
    operations in a single request is limited to 100.
    """
    ...
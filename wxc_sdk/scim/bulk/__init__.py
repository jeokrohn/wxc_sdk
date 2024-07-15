import re
from typing import Optional

from pydantic import TypeAdapter, Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['BulkMethod', 'BulkOperation', 'ResponseError', 'BulkErrorResponse', 'BulkResponseOperation',
           'BulkResponse', 'SCIM2BulkApi']

from wxc_sdk.scim.child import ScimApiChild


class BulkMethod(str, Enum):
    post = 'POST'
    patch = 'PATCH'
    delete = 'DELETE'


class BulkOperation(ApiModel):
    #: The HTTP method of the current operation.
    method: Optional[BulkMethod] = None
    #: The resource's relative path. If the method is POST, the value must specify a resource type endpoint, for
    #: example `/Users` or `/Groups`. All other method values must specify the path to a specific resource.
    path: Optional[str] = None
    #: The Resource JSON data as it appears for a single POST or PATCH resource operation.
    data: Optional[dict] = None
    #: The transient identifier of a newly created resource, unique within a bulk request and created by the client.
    bulk_id: Optional[str] = None


class ResponseError(ApiModel):
    tracking_id: Optional[str] = None
    error_code: Optional[int] = None
    details: Optional[str] = None


class BulkErrorResponse(ApiModel):
    schemas: Optional[list[str]] = None
    status: Optional[int] = None
    error: Optional[ResponseError] = Field(
        alias='urn:scim:schemas:extension:cisco:webexidentity:api:messages:2.0:Error', default=None)


class BulkResponseOperation(ApiModel):
    location: Optional[str] = None
    method: Optional[str] = None
    bulk_id: Optional[str] = None
    version: Optional[str] = None
    status: Optional[int] = None
    response: Optional[BulkErrorResponse] = None

    @property
    def user_id(self) -> Optional[str]:
        if not self.location:
            return None
        m = re.match(r'.+/identity/scim/.+/v2/Users/(\S+)', self.location)
        return m and m.group(1)


class BulkResponse(ApiModel):
    schemas: Optional[list[str]] = None
    operations: Optional[list[BulkResponseOperation]] = None


class SCIM2BulkApi(ScimApiChild, base='identity/scim'):
    """
    Bulk Manage SCIM 2 Users and Groups

    The bulk API allows you to create, update, and remove multiple users and groups in Webex.  The number of Bulk
    operations in a single request is limited to 100.

    Bulk deletion of Users is irreversible. Please test in a test org or sandbox
    before running the command in your production system.

    """

    def bulk_request(self, org_id: str, fail_on_errors: int,
                     operations: list[BulkOperation]) -> BulkResponse:
        """
        User bulk API

        **Authorization**

        OAuth token rendered by Identity Broker.

        One of the following OAuth scopes is required:

        - `identity:people_rw`

        **Usage**:

        1. The input JSON must conform to the following schema: 'urn:ietf:params:scim:api:messages:2.0:BulkRequest'.

        2. The request must be accompanied with a body in JSON format according to the standard SCIM schema definition.
           The maximum number of operations in a request is 100; an error is thrown if the limit is exceeded.

        3. `failOnErrors` parameter

           An integer specifies the number of errors that the service provider will accept before the operation is
           terminated and an error response is returned.
           It is OPTIONAL in a request.
           Maximum number of operations allowed to fail before the server stops processing the request. The value must
           be between 1 and 100.

        4. `operations` parameter

           Contains a list of bulk operations for POST/PATCH/DELETE operations. (REQUIRED)

           + `operations.method`

             The HTTP method of the current operation. Possible values are POST, PATCH or DELETE.
           + `operations.path

             The Resource's relative path. If the method is POST the value must specify a Resource type endpoint;
             e.g., /Users or /Groups whereas all other method values must specify the path to a specific Resource;
             e.g., /Users/2819c223-7f76-453a-919d-413861904646.
           + `operations.data`

             The Resource data as it would appear for a single POST or PATCH Resource operation.
             It is REQUIRED in a request when method is POST and PATCH.
             Refer to corresponding wiki for SCIM 2.0 POST, PATCH and DELETE API.
           + `operations.bulkId`

             The transient identifier of a newly created resource, unique within a bulk request and created by the
             client.
             The bulkId serves as a surrogate resource id enabling clients to uniquely identify newly created
             resources in
             the response and cross-reference new resources in and across operations within a bulk request.
             It is REQUIRED when "method" is "POST".

        :param org_id: Webex Identity assigned organization identifier for user's organization.
        :type org_id: str
        :param fail_on_errors: An integer specifying the maximum number of errors that the service provider will accept
            before the operation is terminated and an error response is returned.
        :type fail_on_errors: int
        :param operations: Contains a list of bulk operations for POST/PATCH/DELETE operations.
        :type operations: list[BulkOperation]
        :rtype: :class:`BulkResponse`

        Example:

            .. code-block:: python

                # bulk operations to create a bunch of users from a list of ScimUser instances
                new_scim_users: list[ScimUser]
                operations = [BulkOperation(method=BulkMethod.post, path='/Users',
                                            bulk_id=str(uuid.uuid4()),
                                            data=scim_user.create_update())
                              for scim_user in new_scim_users]
                bulk_response = self.api.scim.bulk.bulk_request(org_id=org_id, fail_on_errors=1,
                                                                operations=operations)
        """
        body = dict()
        body['schemas'] = ['urn:ietf:params:scim:api:messages:2.0:BulkRequest']
        body['failOnErrors'] = fail_on_errors
        body['operations'] = TypeAdapter(list[BulkOperation]).dump_python(
            operations, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{org_id}/v2/Bulk')
        data = super().post(url, json=body)
        r = BulkResponse.model_validate(data)
        return r

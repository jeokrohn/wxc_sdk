from dataclasses import dataclass

from wxc_sdk.rest import RestSession
from wxc_sdk.api_child import ApiChild
from wxc_sdk.scim.bulk import SCIM2BulkApi
from wxc_sdk.scim.groups import SCIM2GroupsApi
from wxc_sdk.scim.users import SCIM2UsersApi

__all__ = ['ScimV2Api']


@dataclass(init=False)
class ScimV2Api(ApiChild, base=''):
    users: SCIM2UsersApi
    bulk: SCIM2BulkApi
    groups: SCIM2GroupsApi

    def __init__(self, *, session: RestSession):
        super().__init__(session=session)
        self.users = SCIM2UsersApi(session=session)
        self.bulk = SCIM2BulkApi(session=session)
        self.groups = SCIM2GroupsApi(session=session)

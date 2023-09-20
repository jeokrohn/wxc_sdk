from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Authorization', 'AuthorizationType', 'AuthorizationsCollectionResponse']


class AuthorizationType(str, Enum):
    #: refresh authorization used to create `access` tokens
    refresh = 'refresh'
    #: `access` token authorization
    access = 'access'


class Authorization(ApiModel):
    #: The unique authorization identifier.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVEhPUklaQVRJT04vZjI3MDM0ZTMtMDA5ZS00ODA4LTk5MDQtNTNkMDQ0OGJlNDVk
    id: Optional[str] = None
    #: The unique identifier for the application.
    #: example: Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OL0NmMzkyNWU5NDFmMzhhYTc0M2Y0MmFiNzcwZmZhZjFhNTIyMjcxZDI5OTQ4NDhjNjk2YWMwYTEwN2Q2YTg5MjI3
    applicationId: Optional[str] = None
    #: The name of the Integration.
    #: example: Developer Portal
    applicationName: Optional[str] = None
    #: The unique oAuth client id.
    #: example: C80fb9c7096bd8474627317ee1d7a817eff372ca9c9cee3ce43c3ea3e8d1511ec
    clientId: Optional[str] = None
    #: The date and time the authorization was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None
    #: The type of token associated with the authorization.
    #: example: refresh
    type: Optional[AuthorizationType] = None


class AuthorizationsCollectionResponse(ApiModel):
    items: Optional[list[Authorization]] = None

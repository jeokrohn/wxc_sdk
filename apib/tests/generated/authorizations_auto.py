from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
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
    application_id: Optional[str] = None
    #: The name of the Integration.
    #: example: Developer Portal
    application_name: Optional[str] = None
    #: The unique oAuth client id.
    #: example: C80fb9c7096bd8474627317ee1d7a817eff372ca9c9cee3ce43c3ea3e8d1511ec
    client_id: Optional[str] = None
    #: The date and time the authorization was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None
    #: The type of token associated with the authorization.
    #: example: refresh
    type: Optional[AuthorizationType] = None


class AuthorizationsCollectionResponse(ApiModel):
    items: Optional[list[Authorization]] = None


class AuthorizationsApi(ApiChild, base='authorizations'):
    """
    Authorizations
    
    Admin API. You need full or user level admin privileges to call this API.
    
    
    
    Authorizations are user grants to applications to act on the user's behalf. Authorizations are how `Integrations
    <https://developer.webex.com/docs/integrations>`_ get
    authorized with specific `access scopes
    <https://developer.webex.com/docs/integrations#scopes>`_ in the oAuth client life-cycle. Integrations and some of the Webex service
    portals, like `developer.webex.com
    <https://developer.webex.com/>`_, are all oAuth clients, each with their unique `clientId`.
    
    Your application receives an API `access token
    <https://developer.webex.com/docs/integrations#getting-an-access-token>`_ and a `refresh token
    used to call Webex APIs for which the user authorized the scopes. Access tokens expire fairly frequently, while
    refresh tokens (when being regularly used) will be refreshed to last forever (see `Using the Refresh Token
    <https://developer.webex.com/docs/integrations#using-the-refresh-token>`_ for
    details).
    
    In this API an authorization is synonymous with an `API access token
    <https://developer.webex.com/docs/integrations#getting-an-access-token>`_.
    
    To provide admins with fine-grained token management control, you use the `/authorizations
    <https://developer.webex.com/docs/api/v1/authorizations>`_ API with
    the `DELETE` HTTP method to revoke access and refresh tokens.
    
    Deleting a refresh token will revoke all associated access tokens as well. Deleting an access token will revoke the
    developers ability to call the APIs with it.
    Webex subsystems may cache the validity of the token for a short while longer after the authorization was deleted.
    
    Admins can revoke user authorizations for users in their organization. When an admin deletes their own token, the
    `clientId` used to auhtorize the request must match the `clientId` used to generate the token.
    
    To use the authorizations API in an Integration the scopes must include:
    `identity:tokens_write`,`identity:tokens_read`.
    """
    ...
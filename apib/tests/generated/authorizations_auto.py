from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Authorization', 'AuthorizationType', 'AuthorizationsApi']


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
    #: The person Id of the user. Can be used in the /people API.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9lYjIyYjNiZC03NGNiLTRjMjktYjA3Zi1lYWQwMmU1NjgyZDI
    person_id: Optional[str] = None
    #: The unique oAuth client id.
    #: example: C80fb9c7096bd8474627317ee1d7a817eff372ca9c9cee3ce43c3ea3e8d1511ec
    client_id: Optional[str] = None
    #: The date and time the authorization was created.
    #: example: 2015-10-18T14:26:16+00:00
    created: Optional[datetime] = None
    #: The type of token associated with the authorization.
    #: example: refresh
    type: Optional[AuthorizationType] = None


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

    def list_authorizations_for_a_user(self, person_id: str, person_email: str) -> list[Authorization]:
        """
        List authorizations for a user

        Lists all authorizations for a user. Either `personId` or `personEmail` must be provided. This API does not
        support pagination.

        :param person_id: List authorizations for this user id.
        :type person_id: str
        :param person_email: List authorizations for this user email.
        :type person_email: str
        :rtype: list[Authorization]
        """
        params = {}
        params['personId'] = person_id
        params['personEmail'] = person_email
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[Authorization]).validate_python(data['items'])
        return r

    def delete_authorization(self, authorization_id: str):
        """
        Delete authorization

        Deletes an authorization, by authorization ID.

        Specify the authorization Id in the `authorizationId` parameter in the URI which was listed in the list
        resource.

        :param authorization_id: The unique identifier for the message.
        :type authorization_id: str
        :rtype: None
        """
        url = self.ep(f'{authorization_id}')
        super().delete(url)

    def delete_authorization_of_org_and_client_id(self, client_id: str, org_id: str = None):
        """
        Delete authorization of org and client ID

        Deletes an authorization, by org ID and client ID.

        :param client_id: The unique oAuth client id.
        :type client_id: str
        :param org_id: The ID of the organization to which this person belongs.  If no orgId is specified, use orgId
            from the OAuth token.
        :type org_id: str
        :rtype: None
        """
        params = {}
        params['clientId'] = client_id
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        super().delete(url, params=params)

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
    id: Optional[str] = None
    #: The unique identifier for the application.
    application_id: Optional[str] = None
    #: The name of the Integration.
    application_name: Optional[str] = None
    #: The person Id of the user. Can be used in the /people API.
    person_id: Optional[str] = None
    #: The unique oAuth client id.
    client_id: Optional[str] = None
    #: The date and time the authorization was created.
    created: Optional[datetime] = None
    #: The type of token associated with the authorization.
    type: Optional[AuthorizationType] = None


class AuthorizationsApi(ApiChild, base='authorizations'):
    """
    Authorizations
    
    This is an admin API. As a partner admin revoking tokens for your customer
    users, you must be a `Full Admin.` As an admin in your own org revoking tokens
    for your home org users, you must have either of the following roles: `Full
    Admin,` `Device Admin,` `Or user Admin.` Read-only admins are not supported.
    
    
    
    Regular users can manage their tokens via the following
    `GUI
    <https://idbroker.webex.com/idb/profile#/tokens>`_
    
    
    
    Authorizations are user grants to applications to act on the user's behalf. Authorizations are how `Integrations
    <https://developer.webex.com/docs/integrations>`_ get
    authorized with specific `access scopes
    <https://developer.webex.com/docs/integrations#scopes>`_ in the oAuth client life-cycle. Integrations and some of the Webex service
    portals, like `developer.webex.com
    <https://developer.webex.com/>`_, are all oAuth clients, each with their unique `clientId.`
    
    Your application receives an API `access token
    <https://developer.webex.com/docs/integrations#getting-an-access-token>`_ and a `refresh token
    used to call Webex APIs for which the user authorized the scopes. Access tokens expire reasonably frequently,
    while refresh tokens (when being regularly used) will be refreshed to last forever (see `Using the Refresh Token
    <https://developer.webex.com/docs/integrations#using-the-refresh-token>`_
    for details).
    
    In this API an authorization is synonymous with an `API access token
    <https://developer.webex.com/docs/integrations#getting-an-access-token>`_.
    
    To provide admins with fine-grained token management control, you use the `/authorizations
    <https://developer.webex.com/docs/api/v1/authorizations>`_ API with the `DELETE`
    HTTP method to revoke access and refresh tokens.
    
    Deleting a refresh token will revoke all associated access tokens as well. Deleting an access token will revoke the
    developer's ability to call the APIs with it.
    Webex subsystems may cache the token's validity briefly after the authorization is deleted.
    
    Admins can revoke user authorizations for users in their organization. When an admin deletes their own token, the
    `clientId` used to authorize the request must match the `clientId` used to generate the token.
    
    To use the authorizations API in an Integration the scopes must include: `identity:tokens_write,`
    `identity:tokens_read.`
    """

    def delete_authorization_of_org_and_client_id(self, client_id: str, org_id: str = None):
        """
        Delete authorization of org and client ID

        Deletes an authorization by org ID and client ID.

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

    def list_authorizations_for_user(self, person_id: str = None, person_email: str = None) -> list[Authorization]:
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
        if person_id is not None:
            params['personId'] = person_id
        if person_email is not None:
            params['personEmail'] = person_email
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[Authorization]).validate_python(data['items'])
        return r

    def delete_authorization(self, authorization_id: str):
        """
        Delete authorization

        Deletes an authorization by authorization ID.

        Specify the authorization Id in the `authorizationId` parameter in the URI, which was listed in the list
        resource.

        :param authorization_id: The unique identifier for the message.
        :type authorization_id: str
        :rtype: None
        """
        url = self.ep(f'{authorization_id}')
        super().delete(url)

from datetime import datetime
from typing import Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, to_camel, SafeEnum

__all__ = ['Authorization', 'AuthorizationType', 'AuthorizationsApi']


class AuthorizationType(str, SafeEnum):
    """
    The type of token associated with the authorization.
    """
    #: refresh authorization used to create access tokens
    refresh = 'refresh'
    #: access token authorization
    access = 'access'


class Authorization(ApiModel):
    #: The unique authorization identifier.
    id: Optional[str]
    #: The unique identifier for the application.
    application_id: Optional[str]
    #: The name of the Integration.
    application_name: Optional[str]
    #: The unique oAuth client id.
    client_id: Optional[str]
    #: The date and time the authorization was created.
    created: Optional[datetime]
    #: The type of token associated with the authorization.
    type: Optional[AuthorizationType]
    # TODO: undocumented
    person_id: Optional[str]


class AuthorizationsApi(ApiChild, base='authorizations'):
    """
    Authorizations are user grants to applications to act on the user's behalf. Authorizations are how Integrations get
    authorized with specific access scopes in the oAuth client life-cycle. Integrations and some of the Webex service
    portals, like developer.webex.com, are all oAuth clients, each with their unique clientId.

    Your application receives an API access token and a refresh token through the oAuth process. The access token is
    used to call Webex APIs for which the user authorized the scopes. Access tokens expire fairly frequently,
    while refresh tokens (when being regularly used) will be refreshed to last forever (see Using the Refresh Token
    for details).

    In this API an authorization is synonymous with an API access token.

    To provide admins with fine-grained token management control, you use the /authorizations API with the DELETE HTTP
    method to revoke access and refresh tokens.

    Deleting a refresh token will revoke all associated access tokens as well. Deleting an access token will revoke the
    developers ability to call the APIs with it. Webex subsystems may cache the validity of the token for a short while
    longer after the authorization was deleted.

    Admins can revoke user authorizations for users in their organization. When an admin deletes their own token,
    the clientId used to authorize the request must match the clientId used to generate the token.

    To use the authorizations API in an Integration the scopes must
    include: identity:tokens_write, identity:tokens_read.
    """

    def list(self, person_id: str = None, person_email: str = None) -> list[Authorization]:
        """
        Lists all authorizations for a user. Either personId or personEmail must be provided. This API does not support
        pagination.

        :param person_id: List authorizations for this user id.
        :param person_email: List authorizations for this user email.
        :return: List of Authorizations
        """
        params = {to_camel(k): v
                  for k, v in locals().items()
                  if k not in {'self'} and v is not None}
        if frozenset(params) not in {frozenset({'personId'}),
                                     frozenset({'personEmail'})}:
            raise ValueError(
                'Invalid parameter combination: exactly one of person_id or person_email has to be present.')
        url = self.ep()
        data = self.get(url, params=params)
        return TypeAdapter(list[Authorization]).validate_python(data['items'])

    def delete(self, authorization_id: str = None, client_id: str = None, org_id: str = None):
        """
        Deletes an authorization, by authorization ID or client ID and org ID.

        Specify the authorization Id in the authorizationId parameter in the URI which was listed in the list
        resource. The client_id parameter can be combined with org_id.

        :param authorization_id: The unique identifier for the authorization
        :type authorization_id: str
        :param client_id: The unique oAuth client id.
        :type client_id: str
        :param org_id: The ID of the organization. If no orgId is specified, use orgId from the OAuth token.
        :type org_id: str
        """
        if authorization_id:
            if client_id or org_id:
                raise ValueError(
                    'Invalid parameter combination: authorization_id cannot be combined with client_id or org_id.')
            url = self.ep(authorization_id)
            params = None
        else:
            if not client_id:
                raise ValueError(
                    'Invalid parameter combination: client_id is required when authorization_id is not specified.')
            url = self.ep()
            params = client_id and {'clientId': client_id} or dict()
            if org_id:
                params['orgId'] = org_id
        super().delete(url, params=params)

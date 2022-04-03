"""
An OAuth integration
"""
import logging
import urllib.parse
from dataclasses import dataclass
from typing import Union

import requests

from ..rest import dump_response
from ..tokens import Tokens

log = logging.getLogger(__name__)

__all__ = ['Integration']


@dataclass
class Integration:
    """
    An OAuth integration
    """
    #: integration's client id, obtained from developer.webex.com
    client_id: str

    #: integration's client secret, obtained from developer.webex.com
    client_secret: str

    #: OAuth scopes of the integration.
    scopes: list[str]

    #: redirect URL of the integration
    redirect_url: str

    #: URL of the authorization service; used as part of the URL to start an OAuth flow
    auth_service: str

    #: base URL of the access token service
    token_service: str

    def __init__(self, *, client_id: str, client_secret: str, scopes: Union[str, list[str]],
                 redirect_url: str,
                 auth_service: str = None,
                 token_service: str = None):
        """

        :param client_id: integration's client id, obtained from developer.webex.com
        :param client_secret: integration's client secret, obtained from developer.webex.com
        :param scopes: integration's scopes. Can be a list of strings or a string containing a list of space
            separated scopes
        :param redirect_url: integration's redirect URL
        :param auth_service: authorization service to be used in the authorization URL.
            Default: 'https://webexapis.com/v1/authorize'
        :param token_service: URL of token service to use to obrtain tokens from.
            Default: 'https://webexapis.com/v1/access_token'
        """
        self.client_id = client_id
        self.client_secret = client_secret
        if isinstance(scopes, list):
            self.scopes = scopes
        else:
            scopes: str
            self.scopes = scopes.split()
        self.redirect_url = redirect_url
        self.auth_service = auth_service or 'https://webexapis.com/v1/authorize'
        self.token_service = token_service or 'https://webexapis.com/v1/access_token'

    def auth_url(self, *, state: str) -> str:
        """
        Get the URL to start an OAuth flow for the integration

        :param state: state in redirect URL
        :type state: str
        :return: URL to start the OAuth flow
        :rtype: str
        """
        scopes = self.scopes
        if isinstance(scopes, list):
            scopes = ' '.join(scopes)
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_url,
            'scope': scopes,
            'state': state
        }
        full_url = f'{self.auth_service}?{urllib.parse.urlencode(params)}'
        return full_url

    def tokens_from_code(self, *, code: str) -> Tokens:
        """
        Get a new set of tokens from code at end of OAuth flow

        :param code: code obtained at end of SAML 2.0 OAuth flow
        :type code: str
        :return: new tokens
        :rtype: Tokens
        """
        url = self.token_service
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_url
        }
        with requests.Session() as session:
            response = session.post(url=url, data=data)
            dump_response(response, dump_log=log)

        response.raise_for_status()
        json_data = response.json()
        tokens = Tokens.parse_obj(json_data)
        tokens.set_expiration()
        return tokens

    def refresh(self, *, tokens: Tokens):
        """
        Try to get a new access token using the refresh token.

        :param tokens: Tokens. Access token and expirations get updated in place.
        :raise:
            :class:`requests.HTTPError`: if request to obtain new access token fails
        """
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': tokens.refresh_token
        }
        try:
            url = self.token_service
            with requests.Session() as session:
                with session.post(url=url, data=data) as response:
                    dump_response(response=response, dump_log=log)
                    response.raise_for_status()
                    json_data = response.json()
        except requests.HTTPError:
            tokens.access_token = None
            raise
        else:
            new_tokens = Tokens.parse_obj(json_data)
            new_tokens: Tokens
            new_tokens.set_expiration()
            tokens.update(new_tokens)

    def validate_tokens(self, *, tokens: Tokens, min_lifetime_seconds: int = 300) -> bool:
        """
        Validate tokens

        If remaining life time is to small then try to get a new access token
        using the existing refresh token.
        If no new access token can be obtained using the refresh token then the access token is set to None
        and True is returned

        :param tokens: current OAuth tokens. Get updated if new tokens are created
        :type tokens: Tokens
        :param min_lifetime_seconds: minimal remaining lifetime in seconds. Default: 300 seconds
        :type min_lifetime_seconds: int
        :return: True -> min lifetime reached and tried to get new access token.
        :rtype: bool
        """
        if tokens.remaining >= min_lifetime_seconds:
            return False
        log.debug(f'Getting new access token, valid until {tokens.expires_at}, remaining {tokens.remaining}')
        try:
            self.refresh(tokens=tokens)
        except requests.HTTPError:
            # ignore HTTPErrors
            pass
        return True

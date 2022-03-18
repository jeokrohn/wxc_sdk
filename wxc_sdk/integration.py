"""
An OAuth integration
"""
import logging
import os
import urllib.parse
from dataclasses import dataclass

import requests

from .tokens import Tokens
from .rest import dump_response

log = logging.getLogger(__name__)

__all__ = ['Integration']


@dataclass
class Integration:
    """
    an OAuth integration
    """
    client_id: str  #: integration's client id, obtained from developer.webex.com
    client_secret: str  #: integration's client id, obtained from developer.webex.com

    #: OAuth scopes of the integration
    scopes: str

    #: URL of the authorization service; used as part of the URL to start an OAuth flow
    auth_service = 'https://webexapis.com/v1/authorize'

    #: base URL of the access token service
    token_service = 'https://webexapis.com/v1/access_token'

    @property
    def redirect_url(self) -> str:
        """
        Obtain redirect URI. Either on Heroku or localhost:6001

        """
        # redirect URL is either local or to heroku
        heroku_name = os.getenv('HEROKU_NAME')
        if heroku_name:
            return f'https://{heroku_name}.herokuapp.com/redirect'
        return 'http://localhost:6001/redirect'

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
        return tokens

    def validate_tokens(self, tokens: Tokens) -> bool:
        """
        Validate tokens if remaining life time is to small then try to get a new access token
        using the existing refresh token.
        If no new access token can be obtained using the refresh token then the access token is set to None
        and True is returned

        :param tokens: current OAuth tokens. Get updated if new tokens are created
        :type tokens: Tokens
        :return: Indicate if tokens have been changed
        :rtype: bool
        """
        if tokens.needs_refresh:
            log.debug(f'Getting new access token, valid until {tokens.expires_at}, remaining {tokens.remaining}')
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
            else:
                new_tokens = Tokens.parse_obj(json_data)
                new_tokens: Tokens
                new_tokens.set_expiration()
                tokens.update(new_tokens)
                return True
        return False

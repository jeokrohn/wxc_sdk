"""
An OAuth integration
"""
import concurrent.futures
import http.server
import logging
import socketserver
import threading
import urllib.parse
import uuid
import webbrowser
from collections.abc import Callable
from dataclasses import dataclass
from typing import Union, Optional

import requests

from ..rest import dump_response
from ..tokens import Tokens

log = logging.getLogger(__name__)

__all__ = ['Integration']


@dataclass(init=False)
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

    def get_tokens_from_oauth_flow(self) -> Optional[Tokens]:
        """
        Initiate an OAuth flow to obtain new tokens.

        start a local webserver on port 6001 o serve the last step in the OAuth flow

        :param self: Integration to use for the flow
        :type: :class:`wxc_sdk.integration.Integration`
        :return: set of new tokens if successful, else None
        :rtype: :class:`wxc_sdk.tokens.Tokens``
        """

        def serve_redirect():
            """
            Temporarily start a web server to serve the redirect URI at http://localhost:6001/redirect'
            :return: parses query of the GET on the redirect URI
            """

            # mutable to hold the query result
            oauth_response = dict()

            class RedirectRequestHandler(http.server.BaseHTTPRequestHandler):
                # handle the GET request on the redirect URI

                # noinspection PyPep8Naming
                def do_GET(self):
                    # serve exactly one GET on the redirect URI and then we are done

                    parsed = urllib.parse.urlparse(self.path)
                    if parsed.path == '/redirect':
                        log.debug('serve_redirect: got GET on /redirect')
                        query = urllib.parse.parse_qs(parsed.query)
                        oauth_response['query'] = query
                        # we are done
                        self.shutdown(self.server)
                    self.send_response(200)
                    self.flush_headers()

                @staticmethod
                def shutdown(server: socketserver.BaseServer):
                    log.debug('serve_redirect: shutdown of local web server requested')
                    threading.Thread(target=server.shutdown, daemon=True).start()

            httpd = http.server.HTTPServer(server_address=('', 6001),
                                           RequestHandlerClass=RedirectRequestHandler)
            log.debug('serve_redirect: starting local web server for redirect URI')
            httpd.serve_forever()
            httpd.server_close()
            log.debug(f'serve_redirect: server terminated, result {oauth_response["query"]}')
            return oauth_response['query']

        state = str(uuid.uuid4())
        auth_url = self.auth_url(state=state)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # start web server
            fut = executor.submit(serve_redirect)

            # open authentication URL in local webbrowser
            webbrowser.open(auth_url)
            # wait for GET on redirect URI and get the result (parsed query of redirect URI)
            try:
                result = fut.result(timeout=120)
            except concurrent.futures.TimeoutError:
                try:
                    # post a dummy response to the redirect URI to stop the server
                    with requests.Session() as session:
                        session.get(self.redirect_url, params={'code': 'foo'})
                except Exception:
                    pass
                log.warning('Authorization did not finish in time (60 seconds)')
                return

        code = result['code'][0]
        response_state = result['state'][0]
        assert response_state == state

        # get access tokens
        new_tokens = self.tokens_from_code(code=code)
        if new_tokens is None:
            log.error('Failed to obtain tokens')
            return None
        return new_tokens

    def get_cached_tokens(self, *, read_from_cache: Callable[[], Optional[Tokens]],
                          write_to_cache: Callable[[Tokens], None]) -> Optional[Tokens]:
        """
        Get tokens.

        Tokens are read from cache and then verified. If needed an OAuth flow is initiated to get a new
        set of tokens. For this the redirect URL http://localhost:6001/redirect is expected.

        :param read_from_cache: callback to read tokens from cache. Called without parameters and is expected to return
            a :class:`wxc_sdk.tokens.Tokens` instance with the cached tokens. If cached tokens cannot be provided then
            None should be returned.
        :param write_to_cache: callback to write updated tokens back to cache. The callback is called with a
            :class:`wxc_sdk.tokens.Tokens` instance as only argument.
        :return: set of tokens or None
        :rtype: :class:`wxc_sdk.tokens.Tokens`
        """
        # read tokens from cache
        tokens = read_from_cache()
        if tokens:
            # validate tokens
            changed = self.validate_tokens(tokens=tokens)
            if not tokens.access_token:
                tokens = None
            elif changed:
                write_to_cache(tokens)
        if not tokens:
            # get new tokens via integration if needed
            tokens = self.get_tokens_from_oauth_flow()
            if tokens:
                tokens.set_expiration()
                write_to_cache(tokens)
        return tokens

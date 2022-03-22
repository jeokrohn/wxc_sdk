#!/usr/bin/env python
"""
Example script
read tokens from file or interactively obtain token by starting a local web server and open the authorization URL in
the local web browser
"""
import concurrent.futures
import http.server
import json
import logging
import os
import socketserver
import threading
import urllib.parse
import uuid
import webbrowser
from typing import Optional

import requests
from dotenv import load_dotenv
from yaml import safe_load, safe_dump

from wxc_sdk import WebexSimpleApi
from wxc_sdk.integration import Integration
from wxc_sdk.tokens import Tokens

log = logging.getLogger(__name__)


def env_path() -> str:
    """
    determine path for .env to load environment variables from

    :return: .env file path
    """
    return os.path.join(os.getcwd(), f'{os.path.splitext(os.path.basename(__file__))[0]}.env')


def yml_path() -> str:
    """
    determine path of YML file to persists tokens
    :return: path to YML file
    :rtype: str
    """
    return os.path.join(os.getcwd(), f'{os.path.splitext(os.path.basename(__file__))[0]}.yml')


def build_integration() -> Integration:
    """
    read integration parameters from environment variables and create an integration
    :return: :class:`wxc_sdk.integration.Integration` instance
    """
    client_id = os.getenv('TOKEN_INTEGRATION_CLIENT_ID')
    client_secret = os.getenv('TOKEN_INTEGRATION_CLIENT_SECRET')
    scopes = os.getenv('TOKEN_INTEGRATION_CLIENT_SCOPES')
    redirect_url = 'http://localhost:6001/redirect'
    if not all((client_id, client_secret, scopes)):
        raise ValueError('failed to get integration parameters from environment')
    return Integration(client_id=client_id, client_secret=client_secret, scopes=scopes,
                       redirect_url=redirect_url)


def get_tokens_from_oauth_flow(integration: Integration) -> Optional[Tokens]:
    """
    Initiate an OAuth flow to obtain new tokens.

    start a local webserver on port 6001 o serve the last step in the OAuth flow

    :param integration: Integration to use for the flow
    :type: :class:`wxc_sdk.integration.Integration`
    :return: set of new tokens if successful, else None
    :rtype: :class:`wxc_sdk.tokens.Tokens`
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
    auth_url = integration.auth_url(state=state)
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
                    session.get(integration.redirect_url, params={'code': 'foo'})
            except Exception:
                pass
            log.warning('Authorization did not finish in time (60 seconds)')
            return

    code = result['code'][0]
    response_state = result['state'][0]
    assert response_state == state

    # get access tokens
    new_tokens = integration.tokens_from_code(code=code)
    if new_tokens is None:
        log.error('Failed to obtain tokens')
        return None
    return new_tokens


def get_tokens() -> Optional[Tokens]:
    """

    Tokens are read from a YML file. If needed an OAuth flow is initiated.

    :return: tokens
    :rtype: :class:`wxc_sdk.tokens.Tokens`
    """

    def write_tokens(*, tokens: Tokens):
        with open(yml_path(), mode='w') as f:
            safe_dump(json.loads(tokens.json()), f)
        return

    # read tokens from file
    integration = build_integration()
    try:
        with open(yml_path(), mode='r') as f:
            data = safe_load(f)
            tokens = Tokens.parse_obj(data)
    except Exception as e:
        log.info(f'failed to read tokens from file: {e}')
        tokens = None
    if tokens:
        # validate tokens
        tokens: Tokens
        changed = integration.validate_tokens(tokens=tokens)
        if not tokens.access_token:
            tokens = None
        elif changed:
            write_tokens(tokens=tokens)
    if not tokens:
        # get new tokens via integration if needed
        tokens = get_tokens_from_oauth_flow(integration=integration)
        if tokens:
            tokens.set_expiration()
            write_tokens(tokens=tokens)
    return tokens


logging.basicConfig(level=logging.DEBUG)

# load environment variables from .env
path = env_path()
log.info(f'reading {path}')
load_dotenv(env_path())

tokens = get_tokens()

# use the tokens to get identity of authenticated user
api = WebexSimpleApi(tokens=tokens)
me = api.people.me()
print(f'authenticated as {me.display_name} ({me.emails[0]}) ')

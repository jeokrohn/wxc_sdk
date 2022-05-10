#!/usr/bin/env python
"""
Example script
read tokens from file or interactively obtain token by starting a local web server and open the authorization URL in
the local web browser
"""
import json
import logging
import os
from typing import Optional

from dotenv import load_dotenv
from yaml import safe_load, safe_dump

from wxc_sdk import WebexSimpleApi
from wxc_sdk.integration import Integration
from wxc_sdk.scopes import parse_scopes
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
    scopes = parse_scopes(os.getenv('TOKEN_INTEGRATION_CLIENT_SCOPES'))
    redirect_url = 'http://localhost:6001/redirect'
    if not all((client_id, client_secret, scopes)):
        raise ValueError('failed to get integration parameters from environment')
    return Integration(client_id=client_id, client_secret=client_secret, scopes=scopes,
                       redirect_url=redirect_url)


def get_tokens() -> Optional[Tokens]:
    """

    Tokens are read from a YML file. If needed an OAuth flow is initiated.

    :return: tokens
    :rtype: :class:`wxc_sdk.tokens.Tokens`
    """

    def write_tokens(tokens_to_cache: Tokens):
        with open(yml_path(), mode='w') as f:
            safe_dump(json.loads(tokens_to_cache.json()), f)
        return

    def read_tokens() -> Optional[Tokens]:
        try:
            with open(yml_path(), mode='r') as f:
                data = safe_load(f)
                tokens_read = Tokens.parse_obj(data)
        except Exception as e:
            log.info(f'failed to read tokens from file: {e}')
            tokens_read = None
        return tokens_read

    integration = build_integration()
    tokens = integration.get_cached_tokens(read_from_cache=read_tokens,
                                           write_to_cache=write_tokens)
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

#!/usr/bin/env python
"""
Demo for Webex service app: using service APP tokens to access a API endpoints
"""
import logging
import sys
from json import dumps, loads
from os import getenv
from os.path import basename, splitext, isfile
from typing import Optional

from dotenv import load_dotenv
from yaml import safe_load, safe_dump

from wxc_sdk import WebexSimpleApi
from wxc_sdk.integration import Integration
from wxc_sdk.tokens import Tokens


def yml_path() -> str:
    """
    Get filename for YML file to cache access and refresh token
    """
    return f'{splitext(basename(__file__))[0]}.yml'


def env_path() -> str:
    """
    Get path to .env file to read service app settings from
    :return:
    """
    return f'{splitext(basename(__file__))[0]}.env'


def read_tokens_from_file() -> Optional[Tokens]:
    """
    Get service app tokens from cache file, return None if cache does not exist
    """
    path = yml_path()
    if not isfile(path):
        return None
    try:
        with open(path, mode='r') as f:
            data = safe_load(f)
        tokens = Tokens.model_validate(data)
    except Exception:
        return None
    return tokens


def write_tokens_to_file(tokens: Tokens):
    """
    Write tokens to cache
    """
    with open(yml_path(), mode='w') as f:
        safe_dump(tokens.model_dump(exclude_none=True), f)


def get_access_token() -> Tokens:
    """
    Get a new access token using refresh token, service app client id, service app client secret
    """
    tokens = Tokens(refresh_token=getenv('SERVICE_APP_REFRESH_TOKEN'))
    integration = Integration(client_id=getenv('SERVICE_APP_CLIENT_ID'),
                              client_secret=getenv('SERVICE_APP_CLIENT_SECRET'),
                              scopes=[], redirect_url=None)
    integration.refresh(tokens=tokens)
    write_tokens_to_file(tokens)
    return tokens


def get_tokens() -> Optional[Tokens]:
    """
    Get tokens from cache or create new access token using service app credentials
    """
    # try to read from file
    tokens = read_tokens_from_file()
    # .. or create new access token using refresh token
    if tokens is None:
        tokens = get_access_token()
    if tokens.remaining < 24 * 60 * 60:
        tokens = get_access_token()
    return tokens


def service_app():
    """
    Use service app access token to call Webex Calling API endpoints
    :return:
    """
    load_dotenv(env_path())
    # assert that all required environment variable are set
    if not all(getenv(s) for s in ('SERVICE_APP_REFRESH_TOKEN', 'SERVICE_APP_CLIENT_ID', 'SERVICE_APP_CLIENT_SECRET')):
        print(
            f'SERVICE_APP_REFRESH_TOKEN, SERVICE_APP_CLIENT_ID, and SERVICE_APP_CLIENT_SECRET need to be defined in '
            f'environment or in "{env_path()}"',
            file=sys.stderr)
        exit(1)

    # get tokens and dump to console
    tokens = get_tokens()
    print(dumps(loads(tokens.json()), indent=2))
    print()
    print('scopes:')
    print('\n'.join(f' * {s}' for s in sorted(tokens.scope.split())))

    # use tokens to access APIs
    api = WebexSimpleApi(tokens=tokens)

    users = list(api.people.list())
    print(f'{len(users)} users')

    queues = list(api.telephony.callqueue.list())
    print(f'{len(queues)} call queues')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    service_app()

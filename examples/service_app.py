#!/usr/bin/env python
"""
Demo for Webex service app: using service APP tokens to access a API endpoints
"""
import inspect
import logging
import os
import sys
from json import dumps, loads
from os import getenv
from typing import Optional

import yaml
from dotenv import load_dotenv

from wxc_sdk import WebexSimpleApi
from wxc_sdk.integration import Integration
from wxc_sdk.tokens import Tokens

SERVICE_APP_ENVS = ('SERVICE_APP_REFRESH_TOKEN', 'SERVICE_APP_CLIENT_ID', 'SERVICE_APP_CLIENT_SECRET')


def yml_path(*, client_id: str) -> str:
    """
    Get filename for YML file to cache access and refresh token
    """
    return f'tokens_{client_id}.yml'


def env_path() -> str:
    """
    Get path to .env file to read service app settings from
    """
    # get the file name of the calling script to determine the name of the .env file
    frame = inspect.currentframe().f_back
    file_name = inspect.getframeinfo(frame).filename
    env_name = f'{os.path.splitext(os.path.basename(file_name))[0]}.env'
    return env_name


def read_tokens_from_file(*, client_id: str) -> Optional[Tokens]:
    """
    Get service app tokens from cache file, return None if cache does not exist or read fails
    """
    path = yml_path(client_id=client_id)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, mode='r') as f:
            data = yaml.safe_load(f)
        tokens = Tokens.model_validate(data)
    except Exception:
        return None
    return tokens


def write_tokens_to_file(*, client_id: str, tokens: Tokens):
    """
    Write tokens to cache
    """
    with open(yml_path(client_id=client_id), mode='w') as f:
        yaml.safe_dump(tokens.model_dump(exclude_none=True), f)


def get_access_token(*, client_id: str, client_secret: str, refresh: str) -> Tokens:
    """
    Get a new access token using refresh token, service app client id, service app client secret
    """
    tokens = Tokens(refresh_token=refresh)
    integration = Integration(client_id=client_id,
                              client_secret=client_secret,
                              scopes=[], redirect_url=None)
    integration.refresh(tokens=tokens)
    write_tokens_to_file(client_id=client_id, tokens=tokens)
    return tokens


def get_tokens() -> Optional[Tokens]:
    """
    Get tokens from environment variable, cache or create new access token using service app credentials
    """
    refresh, client_id, client_secret = (os.getenv(env) for env in SERVICE_APP_ENVS)
    if not all((refresh, client_id, client_secret)):
        token = os.getenv('WEBEX_ACCESS_TOKEN')
        if token is None:
            return None
        tokens = Tokens(access_token=token)
    else:
        # try to read from file
        tokens = read_tokens_from_file(client_id=client_id)
        # .. or create new access token using refresh token
        if tokens is None:
            tokens = get_access_token(client_id=client_id, client_secret=client_secret, refresh=refresh)
        if tokens.expires_in is not None and tokens.remaining < 24 * 60 * 60:
            tokens = get_access_token(client_id=client_id, client_secret=client_secret, refresh=refresh)
    return tokens


def service_app():
    """
    Use service app access token to call Webex Calling API endpoints
    :return:
    """
    load_dotenv(env_path())
    # assert that all required environment variable are set
    if not all(getenv(s) for s in SERVICE_APP_ENVS):
        print(
            f'{", ".join(SERVICE_APP_ENVS)} environment variables need to be defined in '
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

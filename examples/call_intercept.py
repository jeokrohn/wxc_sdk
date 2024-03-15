#!/usr/bin/env python
"""
Script to read/update call intercept settings of a calling user.

The script uses the access token passed via the CLI, reads one from the WEBEX_ACCESS_TOKEN environment variable or
obtains tokens via an OAuth flow.

    usage: call_intercept.py [-h] [--token TOKEN] user_email [{on,off}]

    positional arguments:
      user_email     email address of user
      {on,off}       operation to apply

    options:
      -h, --help     show this help message and exit
      --token TOKEN  admin access token to use
"""
import argparse
import logging
import os
import re
import sys
from json import loads
from typing import Optional

from dotenv import load_dotenv
from wxc_sdk import WebexSimpleApi
from wxc_sdk.integration import Integration
from wxc_sdk.person_settings.call_intercept import InterceptSetting
from wxc_sdk.rest import RestError
from wxc_sdk.scopes import parse_scopes
from wxc_sdk.tokens import Tokens
from yaml import safe_dump, safe_load

log = logging.getLogger(__name__)


def env_path() -> str:
    """
    determine path for .env to load environment variables from

    :return: .env file path
    """
    return os.path.join(os.getcwd(), f'{os.path.splitext(os.path.basename(__file__))[0]}.env')


def yml_path() -> str:
    """
    determine path of YML file to persist tokens

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
    if scopes:
        scopes = parse_scopes(scopes)
    if not all((client_id, client_secret, scopes)):
        raise ValueError('failed to get integration parameters from environment')
    redirect_url = 'http://localhost:6001/redirect'
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
            safe_dump(loads(tokens_to_cache.json()), f)
        return

    def read_tokens() -> Optional[Tokens]:
        try:
            with open(yml_path(), mode='r') as f:
                data = safe_load(f)
                tokens_read = Tokens.model_validate(data)
        except Exception as e:
            log.info(f'failed to read tokens from file: {e}')
            tokens_read = None
        return tokens_read

    integration = build_integration()
    tokens = integration.get_cached_tokens(read_from_cache=read_tokens,
                                           write_to_cache=write_tokens)
    return tokens


RE_EMAIL = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def email_type(value):
    if not RE_EMAIL.match(value):
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid email")
    return value


def main():
    """
    where the magic happens
    """
    # read .env file with the settings for the integration to be used to obtain tokens
    load_dotenv(env_path())

    parser = argparse.ArgumentParser()
    parser.add_argument('user_email', type=email_type, help='email address of user')
    parser.add_argument('on_off', choices=['on', 'off'], nargs='?', help='operation to apply')
    parser.add_argument('--token', type=str, required=False, help='admin access token to use')
    args = parser.parse_args()

    if args.token:
        tokens = args.token
    elif (tokens := os.getenv('WEBEX_ACCESS_TOKEN')) is None:
        tokens = get_tokens()

    if not tokens:
        print('Failed to get tokens', file=sys.stderr)
        exit(1)

    # set level to DEBUG to see debug of REST requests
    logging.basicConfig(level=(gt := getattr(sys, 'gettrace', None)) and gt() and logging.DEBUG or logging.INFO)

    with WebexSimpleApi(tokens=tokens) as api:
        # get user
        email = args.user_email.lower()
        user = next((user
                     for user in api.people.list(email=email)
                     if user.emails[0] == email), None)
        if user is None:
            print(f'User "{email}" not found', file=sys.stderr)
            exit(1)

        # display call intercept status
        try:
            intercept = api.person_settings.call_intercept.read(user.person_id)
        except RestError as e:
            print(f'Failed to read call intercept settings: {e.response.status_code}, {e.description}')
            exit(1)

        print('on' if intercept.enabled else 'off')
        if args.on_off:
            # action: turn on/off
            intercept = InterceptSetting.default()
            intercept.enabled = args.on_off == 'on'
            try:
                api.person_settings.call_intercept.configure(user.person_id,
                                                             intercept=intercept)
            except RestError as e:
                print(f'Failed to update call intercept settings: {e.response.status_code}, {e.description}')
                exit(1)

            # read call intercept again
            try:
                intercept = api.person_settings.call_intercept.read(user.person_id)
            except RestError as e:
                print(f'Failed to read call intercept settings: {e.response.status_code}, {e.description}')
                exit(1)

            # display state after update
            print(f"set to {'on' if intercept.enabled else 'off'}")

    exit(0)


if __name__ == '__main__':
    main()

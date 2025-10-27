#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "email-validator",
#     "python-dotenv",
#     "typer",
#     "wxc-sdk",
# ]
# ///
"""
Script to read/update call intercept settings of a calling user.

 Usage: call_intercept.py [OPTIONS] USER_EMAIL [ON_OFF]:[on|off]

 read/update call intercept settings of a calling user.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────╮
│ *    user_email      EMAIL_TYPE         email address of user [required]                   │
│      on_off          [ON_OFF]:[on|off]  operation to apply.                                │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────╮
│ --token                     TEXT  Access token can be provided using --token argument, set │
│                                   in WEBEX_ACCESS_TOKEN environment variable or can be a   │
│                                   service app token. For the latter set environment        │
│                                   variables ('SERVICE_APP_REFRESH_TOKEN',                  │
│                                   'SERVICE_APP_CLIENT_ID', 'SERVICE_APP_CLIENT_SECRET').   │
│                                   Environment variables can also be set in service_app.env │
│ --install-completion              Install completion for the current shell.                │
│ --show-completion                 Show completion for the current shell, to copy it or     │
│                                   customize the installation.                              │
│ --help                            Show this message and exit.                              │
╰────────────────────────────────────────────────────────────────────────────────────────────╯

 Example: ./call_intercept.py bob@example.com on
"""
import logging
import os
import sys
from enum import Enum
from typing import Optional

import typer
from dotenv import load_dotenv
from email_validator import validate_email

from service_app import SERVICE_APP_ENVS, env_path, get_tokens
from wxc_sdk import WebexSimpleApi
from wxc_sdk.person_settings.call_intercept import InterceptSetting
from wxc_sdk.rest import RestError
from wxc_sdk.tokens import Tokens

log = logging.getLogger(__name__)


def email_type(value: str):
    """
    Validate email address
    """
    validated = validate_email(value, check_deliverability=False)
    return validated.normalized


class OnOff(str, Enum):
    ON = 'on'
    OFF = 'off'


app = typer.Typer()


@app.command(name=os.path.basename(__file__),
             help='read/update call intercept settings of a calling user.',
             epilog=f'Example: {sys.argv[0]} bob@example.com on')
def main(user_email: str = typer.Argument(...,
                                          help='email address of user',
                                          parser=email_type),
         on_off: Optional[OnOff] = typer.Argument(None,
                                                  help='operation to apply.'),
         token: Optional[str] = typer.Option(None, '--token',
                                             help=f'Access token can be provided using --token argument, '
                                                  f'set in WEBEX_ACCESS_TOKEN environment variable or '
                                                  f'can be a service app token. For the latter set '
                                                  f'environment variables {SERVICE_APP_ENVS}. '
                                                  f'Environment variables can also be set in '
                                                  f'{env_path()}')):
    """
    where the magic happens
    """
    # get tokens
    load_dotenv(env_path())

    tokens = get_tokens() if token is None else Tokens(access_token=token)
    if tokens is None:
        print(f'Access token can be provided using --token argument, set in WEBEX_ACCESS_TOKEN environment variable or '
              f'can be a service app token. For the latter set environment variables {SERVICE_APP_ENVS}. Environment '
              f'variables can '
              f'also be set in {env_path()}', file=sys.stderr)

    # set level to DEBUG to see debug of REST requests
    logging.basicConfig(level=(gt := getattr(sys, 'gettrace', None)) and gt() and logging.DEBUG or logging.INFO)

    with WebexSimpleApi(tokens=tokens) as api:
        # get user
        email = user_email.lower()
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
        if on_off:
            # action: turn on/off
            intercept = InterceptSetting.default()
            intercept.enabled = on_off == OnOff.ON
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
    app()

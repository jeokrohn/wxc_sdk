#!/usr/bin/env python
"""
Read all messages from given space
usage: archive_space.py [-h] [--email EMAIL] space

read contents of a space

positional arguments:
  space                 space name

optional arguments:
  -h, --help            show this help message and exit
  --email EMAIL, -e EMAIL
                        email address of user

"""

import os
import re
import sys
from argparse import ArgumentParser, ArgumentTypeError

from dotenv import load_dotenv

from wxc_sdk import WebexSimpleApi
from wxc_sdk.integration import Integration
from wxc_sdk.scopes import parse_scopes

RE_EMAIL = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def email_type(value):
    if not RE_EMAIL.match(value):
        raise ArgumentTypeError(f"'{value}' is not a valid email")
    return value


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


def main():
    # parse arguments
    #   * email
    #   * space name
    parser = ArgumentParser(description='read contents of a space')
    parser.add_argument('--email', '-e', type=email_type, required=False, help='email address of user')
    parser.add_argument('space', type=str, help='space name')
    parser.add_argument('--token', type=str, required=False, help='admin access token to use')

    args = parser.parse_args()

    # get tokens
    tokens = args.token
    load_dotenv(os.path.join(os.getcwd(),
                             f'{os.path.splitext(os.path.basename(__file__))[0]}.env'))

    # try to get token from file .. or in the 2nd round force new tokens if the token is for a different email address
    for force_new in (False, True):
        if not tokens:
            integration = build_integration()
            tokens = integration.get_cached_tokens_from_yml(
                yml_path=os.path.join(os.getcwd(),
                                      f'{os.path.splitext(os.path.basename(__file__))[0]}.yml'),
                force_new=force_new)

        if not tokens:
            print('failed to get valid access token', file=sys.stderr)
            exit(1)
        with WebexSimpleApi(tokens=tokens) as api:
            # verify that token matches email address (if given)
            me = api.people.me()
            print(f'access token issued for {me.display_name}({me.emails[0]})')
            if args.email and args.email != me.emails[0]:
                print(f'token does not match provided email address {args.email}', file=sys.stderr)
                if force_new:
                    # we already tried to force new tokens --> we are done here
                    exit(1)
                else:
                    # try again with new tokens
                    if not args.token:
                        continue
                    else:
                        break
                # if
            # if
            # find space
            # ... the complicated way to avoid to have to paginate through the whole thing if the target happened to
            # be in the 1st "few" spaces
            target = next((space for space in api.rooms.list(max=500)
                           if space.title == args.space), None)
            if target is None:
                print(f'space "{args.space}" not found', file=sys.stderr)
                exit(1)

            # iterate through all messages
            for message in api.messages.list(room_id=target.id, max=1000):
                print(message)
                # .. here you can now add code to for example write messages to a file
            # for
        # with
        # break the loop: we are done here, we had valid tokens.
        break
    # for
    return


if __name__ == '__main__':
    main()

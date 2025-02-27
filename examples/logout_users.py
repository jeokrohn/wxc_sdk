#!/usr/bin/env python
"""
    usage: logout_users.py [-h] [--appname APPNAME] [--test] email

    CLI tool to logout users by revoking user authorizations

    positional arguments:
      email              single email or path to file w/ email addresses (one email address per line). "all" can be
                         used to print authorizations for all users. "all" cannot be combined with other parameters
                         and no authorizations will be revoked in this case."

    optional arguments:
      -h, --help         show this help message and exit
      --appname APPNAME  regular expression matching authorization application names. When missing authorizations for
                         all client ids defined in the script are revoked
      --test             test run only
"""
import asyncio
import logging
import re
import sys
import time
from argparse import ArgumentParser
from itertools import chain
from operator import attrgetter
from os import getcwd, getenv
from os.path import join, splitext, basename, isfile
from typing import Optional

from dotenv import load_dotenv
from yaml import safe_dump, safe_load

from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.authorizations import Authorization, AuthorizationType
from wxc_sdk.integration import Integration
from wxc_sdk.people import Person
from wxc_sdk.tokens import Tokens

# list of client ids to revoke authorizations for
# add more client ids as needed
CLIENT_IDS = {
    # Webex Web Client
    'C64ab04639eefee4798f58e7bc3fe01d47161be0d97ff0d31e040a6ffe66d7f0a',
    # Webex Teams Desktop Client for Mac
    'Ccb2581f071a0714c8ab7d4777f70ebed26f1ef5f3261597f00afbb3a53c1ad88',
    # add more client ids as required, call the script with "all" parameter to identify more client ids
}


def yml_path() -> str:
    """
    Get filename for YML file to cache access and refresh token
    """
    return f'{splitext(basename(__file__))[0]}.yml'


def env_path() -> str:
    """
    Get path to .env file to read service app settings from
    """
    return f'{splitext(basename(__file__))[0]}.env'


def read_tokens_from_file() -> Optional[Tokens]:
    """
    Get service app tokens from cache file, return None if cache does not exist or read fails
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


def auth_str(auth: Authorization) -> str:
    return f'{auth.type:7}, {auth.client_id} - {auth.application_name}'


async def main() -> int:
    parser = ArgumentParser(prog=basename(__file__),
                            description='CLI tool to logout users by revoking user authorizations')
    parser.add_argument('email',
                        help='single email or path to file w/ email addresses (one email address per line). "all" can '
                             'be used to print authorizations for all users. "all" cannot be combined with other '
                             'parameters and no authorizations will be revoked in this case."')
    parser.add_argument('--appname',
                        type=str,
                        help='regular expression matching authorization application names. '
                             'When missing authorizations for all client ids defined in the '
                             'script are revoked')
    parser.add_argument('--test', action='store_true', help='test run only')
    args = parser.parse_args()
    email = args.email
    test_run = args.test
    appname = args.appname

    if appname:
        try:
            appname_re = re.compile(appname)
        except re.error as e:
            print(f'invalid regular expression for --appname: {e}')
            return 1

    async def work_on_one_email(api: AsWebexSimpleApi, user_email: str) -> int:
        """
        Work on authorizations for one email
        """
        print(f'Getting authorizations for {user_email}')
        auths = await api.authorizations.list(person_email=user_email)

        auths.sort(key=lambda a: f'{a.application_name}{a.type}')

        # determine set of authorization ids to revoke
        if appname:
            auths_to_delete = set(a.id for a in auths
                                  if appname_re.match(a.application_name))
        else:
            auths_to_delete = set(a.id for a in auths
                                  if a.client_id in CLIENT_IDS)
        if auths:
            # show all authorizations and indicate which will be revoked
            print('\n'.join(f'{user_email}: {auth_str(auth)} '
                            f'{"--> revoke" if auth.id in auths_to_delete else ""}'
                            for auth in auths))

        if not auths:
            print(f'{user_email}: no auths found')
            return 0
        if not auths_to_delete:
            print(f'{user_email}: no auths to revoke')
            return 0
        if test_run:
            print(f'{user_email}: testrun, not revoking any auths')
            return 0
        results = await asyncio.gather(*[api.authorizations.delete(authorization_id=a_id)
                                         for a_id in auths_to_delete],
                                       return_exceptions=True)
        err = False
        for r, auth_id in zip(results, auths_to_delete):
            if not isinstance(r, Exception):
                continue
            auth = next((a for a in auths if a.id == auth_id))
            if auth.type == AuthorizationType.refresh:
                # ignore errors on revoking access tokens (race condition)
                continue
            print(f'{user_email}: {auth_str(auth)}, error revoking auth: {r}')
            err = True
        if err:
            return 1
        return 0

    # get tokens; as an alternative you can just get a developer token from developer.webex.com and use:
    #   tokens = '<developer token from developer.webex.com>'
    load_dotenv(dotenv_path=env_path())
    err = ''
    tokens = None
    try:
        tokens = get_tokens()
    except Exception as e:
        err = f'{e}'
    if not tokens:
        print(f'failed to obtain access tokens: {err}', file=sys.stderr)
        return 1

    async with AsWebexSimpleApi(tokens=tokens) as api:
        if email == 'all':
            print('Getting users...')
            users = await api.people.list()
            print(f'Getting authorizations for {len(users)} users...')
            auth_lists = await asyncio.gather(*[api.authorizations.list(person_id=user.person_id)
                                                for user in users],
                                              return_exceptions=True)
            err = False
            for user, error in zip(users, auth_lists):
                user: Person
                if isinstance(error, Exception):
                    print(f'{user.emails}: failed to get authorizations: {error}')
                    err = True
            if err:
                return 1
            auth_dict: dict[str, list[Authorization]] = {person.person_id: auth_list
                                                         for person, auth_list in zip(users, auth_lists)
                                                         if auth_list}
            print('\n'.join(chain.from_iterable((f'{user.emails[0]}: {auth_str(auth)}'
                                                 for auth in auth_dict.get(user.person_id, []))
                                                for user in sorted(users, key=attrgetter('display_name')))))

            clients = set(auth_str(auth) for auth in chain.from_iterable(auth_lists))
            print()
            print('tokens and clients:')
            print('\n'.join(sorted(clients)))
            return 0
        elif isfile(email):
            # read email addresses from file, one email address per line
            with open(email, mode='r') as f:
                emails = list(sorted(set(s_line for line in f if (s_line := line.strip()))))
        else:
            emails = [email]

        if not emails:
            print('Nothing to do')
            return 0

        # act on all emails concurrently
        results = await asyncio.gather(*[work_on_one_email(api, e)
                                         for e in emails],
                                       return_exceptions=True)
    err = next((r for r in results if isinstance(r, Exception)), None)
    if err:
        raise err
    return max(results)


if __name__ == '__main__':
    root_logger = logging.getLogger()
    h = logging.StreamHandler(stream=sys.stderr)
    h.setLevel(logging.INFO)
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(h)

    # log REST API interactions to file
    file_fmt = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s')
    file_fmt.converter = time.gmtime

    rest_log_name = join(getcwd(), f'{splitext(basename(__file__))[0]}.log')
    rest_log_handler = logging.FileHandler(rest_log_name, mode='w')
    rest_log_handler.setLevel(logging.DEBUG)
    rest_log_handler.setFormatter(file_fmt)
    rest_logger = logging.getLogger('wxc_sdk.as_rest')
    rest_logger.setLevel(logging.DEBUG)
    rest_logger.addHandler(rest_log_handler)

    exit(asyncio.run(main()))

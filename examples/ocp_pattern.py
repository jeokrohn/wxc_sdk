#!/usr/bin/env python3
"""
Provision OCP patterns for one or all locations

usage: ocp_pattern.py [-h] [--token TOKEN] [--dry-run] [--verbose] [--log-file LOG_FILE]
                      location patterns

Provision OCP patterns for one or all locations

positional arguments:
  location             Location to provision OCP patterns for. Use "all" to provision for
                       all locations
  patterns             File with patterns to provision. File has one pattern per line. Use
                       "remove" to remove all patterns previously provisioned by the
                       script

optional arguments:
  -h, --help           show this help message and exit
  --token TOKEN        Access token can be provided using --token argument, set in
                       WEBEX_ACCESS_TOKEN environment variable or can be a service app
                       token. For the latter set environment variables
                       ('SERVICE_APP_REFRESH_TOKEN', 'SERVICE_APP_CLIENT_ID',
                       'SERVICE_APP_CLIENT_SECRET'). Environment variables can also be set
                       in ocp_pattern.env
  --dry-run            Dry run, do not provision anything
  --verbose            Print debug information
  --log-file LOG_FILE  Log file. If extension is .har, log in HAR format

Example: ocp_pattern.py all ocp_pattern.txt --log-file ocp_pattern.har --dry-run
"""
import argparse
import asyncio
import logging
import os
import sys
from contextlib import contextmanager
from typing import Optional

import yaml
from dotenv import load_dotenv

from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.as_rest import AsRestError
from wxc_sdk.har_writer import HarWriter
from wxc_sdk.integration import Integration
from wxc_sdk.person_settings.permissions_out import DigitPattern, Action
from wxc_sdk.telephony.location import TelephonyLocation
from wxc_sdk.tokens import Tokens

SERVICE_APP_ENVS = ('SERVICE_APP_REFRESH_TOKEN', 'SERVICE_APP_CLIENT_ID', 'SERVICE_APP_CLIENT_SECRET')


def yml_path() -> str:
    """
    Get filename for YML file to cache access and refresh token
    """
    return f'{os.path.splitext(os.path.basename(__file__))[0]}.yml'


def env_path() -> str:
    """
    Get path to .env file to read service app settings from
    """
    return f'{os.path.splitext(os.path.basename(__file__))[0]}.env'


def read_tokens_from_file() -> Optional[Tokens]:
    """
    Get service app tokens from cache file, return None if cache does not exist or read fails
    """
    path = yml_path()
    if not os.path.isfile(path):
        return None
    try:
        with open(path, mode='r') as f:
            data = yaml.safe_load(f)
        tokens = Tokens.model_validate(data)
    except Exception:
        return None
    return tokens


def write_tokens_to_file(tokens: Tokens):
    """
    Write tokens to cache
    """
    with open(yml_path(), mode='w') as f:
        yaml.safe_dump(tokens.model_dump(exclude_none=True), f)


def get_access_token() -> Tokens:
    """
    Get a new access token using refresh token, service app client id, service app client secret
    """
    load_dotenv(env_path())
    refresh, client_id, client_secret = (os.getenv(env) for env in SERVICE_APP_ENVS)
    if not all((refresh, client_id, client_secret)):
        token = os.getenv('WEBEX_ACCESS_TOKEN')
        if token is None:
            print(
                f'Access token can be provided using --token argument, set in WEBEX_ACCESS_TOKEN environment variable '
                f'or '
                f'can be a service app token. For the latter set environment variables {SERVICE_APP_ENVS}. Environment '
                f'variables can '
                f'also be set in {env_path()}', file=sys.stderr)
            exit(1)
        tokens = Tokens(access_token=token)
    else:
        tokens = Tokens(refresh_token=refresh)
        integration = Integration(client_id=client_id,
                                  client_secret=client_secret,
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
    if tokens.expires_in is not None and tokens.remaining < 24 * 60 * 60:
        tokens = get_access_token()
    return tokens


async def work_on_one_location(api: AsWebexSimpleApi, location: TelephonyLocation, pattern_list: list[str],
                               dry_run: bool):
    """
    Work on one location, create, update or remove patterns
    """
    async def create(pattern: str):
        try:
            await dapi.create(location.location_id,
                              DigitPattern(pattern=pattern,
                                           name=f'ocp-{pattern}',
                                           action=Action.allow,
                                           transfer_enabled=True))
            print(f'{location.name}: created pattern {pattern}')
        except AsRestError as e:
            print(f'{location.name}: failed to create pattern {pattern}, error: {e}')
            raise

    async def remove(pattern: DigitPattern):
        try:
            await dapi.delete(location.location_id, pattern.id)
            print(f'{location.name}: removed pattern {pattern.pattern}')
        except AsRestError as e:
            print(f'{location.name}: failed to remove pattern {pattern.pattern}, error: {e}')
            raise


    async def update(pattern: DigitPattern):
        try:
            await dapi.update(location.location_id,
                              DigitPattern(pattern=pattern.pattern,
                                           name=f'ocp-{pattern.pattern}',
                                           action=Action.allow,
                                           transfer_enabled=True))
            print(f'{location.name}: updated pattern {pattern.pattern}')
        except AsRestError as e:
            print(f'{location.name}: failed to update pattern {pattern.pattern}, error: {e}')
            raise

    pattern_set = set(pattern_list)
    dapi = api.telephony.permissions_out.digit_patterns

    # get ocp patterns for location
    location_digit_patterns = await dapi.get_digit_patterns(location.location_id)

    existing_patterns = [pattern for pattern in location_digit_patterns.digit_patterns
                         if pattern.pattern in pattern_set]
    missing_patterns = [pattern
                        for pattern in pattern_list
                        if pattern not in set(map(lambda p: p.pattern, location_digit_patterns.digit_patterns))]
    to_be_removed = [pattern for pattern in location_digit_patterns.digit_patterns
                     if pattern.name.startswith('ocp-') and pattern.pattern not in pattern_set]
    tasks = []

    # remove patterns
    for remove_pattern in to_be_removed:
        # remove pattern
        print(f'{location.name}: remove pattern {remove_pattern.pattern}')
        if not dry_run:
            tasks.append(remove(remove_pattern))

    # add missing patterns
    for pattern in missing_patterns:
        # add pattern
        print(f'{location.name}: add pattern {pattern}')
        if not dry_run:
            tasks.append(create(pattern))

    # check existing patterns and update if action is not "allow"
    for existing in existing_patterns:
        if existing.action == Action.allow and existing.transfer_enabled:
            # pattern already exists and is allowed
            continue
        # update existing pattern
        print(f'{location.name}: update pattern {existing.pattern}')
        if not dry_run:
            tasks.append(update(existing))
    if tasks:
        # run tasks
        await asyncio.gather(*tasks)
    return

@contextmanager
def setup_logging(args: argparse.Namespace, api: AsWebexSimpleApi):
    """
    Set up logging
    """

    @contextmanager
    def file_handler(log_file: str):
        if not log_file:
            yield
        else:
            # log to file or to HAR
            if os.path.splitext(log_file)[-1].lower() == '.har':
                with HarWriter(api=api, path=log_file):
                    yield
            else:
                f_handler = logging.FileHandler(args.log_file)
                f_handler.setLevel(logging.DEBUG)
                f_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
                logging.getLogger().addHandler(f_handler)
                yield
        return

    logging.getLogger().setLevel(logging.DEBUG)
    # create a console logging handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(console_handler)
    with file_handler(args.log_file):
        yield

async def main():
    parser = argparse.ArgumentParser(
        description="Provision OCP patterns for one or all locations",
        epilog='Example: %(prog)s all ocp_pattern.txt --log-file ocp_pattern.har --dry-run')
    parser.add_argument('location', type=str, help='Location to provision OCP patterns for. Use "all" to '
                                                   'provision for all locations')
    parser.add_argument('patterns', type=str, help='File with patterns to provision. File has one pattern '
                                                   'per line. Use "remove" to remove all patterns previously '
                                                   'provisioned '
                                                   'by the script')
    parser.add_argument('--token',
                        help=f'Access token can be provided using --token argument, set in '
                             f'WEBEX_ACCESS_TOKEN environment variable or can be a service app token. For '
                             f'the latter set environment variables {SERVICE_APP_ENVS}. Environment '
                             f'variables can also be set in {env_path()}')
    parser.add_argument('--dry-run', action='store_true', help='Dry run, do not provision anything')
    parser.add_argument('--verbose', action='store_true', help='Print debug information')
    parser.add_argument('--log-file', help='Log file. If extension is .har, log in HAR format')

    args = parser.parse_args()
    location_name = args.location
    pattern_file = args.patterns
    dry_run = args.dry_run

    # get tokens
    # if token is provided use that token, else try to read from file
    tokens = get_tokens() if args.token is None else Tokens(access_token=args.token)
    async with AsWebexSimpleApi(tokens=tokens, concurrent_requests=100) as api:
        with setup_logging(args, api):
            # validate location
            if location_name.lower() == 'all':
                # all locations
                location_list = await api.telephony.locations.list()
                location_list.sort(key=lambda loc: loc.name)
            else:
                # single location
                location_list = [loc
                                 for loc in await api.telephony.locations.list(name=location_name)
                                 if loc.name == location_name]
                if not location_list:
                    print(f'Location {location_name} not found', file=sys.stderr)
                    exit(1)

            # read patterns from given file
            if pattern_file.lower() == 'remove':
                # remove all patterns
                pattern_list = []
            else:
                try:
                    with open(pattern_file, mode='r') as f:
                        pattern_list = [ps for p in f.readlines()
                                        if (ps := p.strip()) and not p.startswith('#')]
                except FileNotFoundError:
                    print(f'File {pattern_file} not found', file=sys.stderr)
                    exit(1)

            # apply changes to all locations
            print(f'Working on {len(location_list)} location(s), {len(pattern_list)} patterns')
            await asyncio.gather(*[work_on_one_location(api, loc, pattern_list, dry_run)
                                   for loc in location_list])
    return

if __name__ == '__main__':
    asyncio.run(main())

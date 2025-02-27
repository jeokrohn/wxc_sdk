#!/usr/bin/env python
"""
Add TNs to a locations.
usage: add_numbers.py [-h] [--dry-run] [--verbose] [--log-file LOG_FILE] [--token TOKEN]
                      [--inactive]
                      file

Add TNs to Webex Calling locations

positional arguments:
  file                 CSV file with location names and TNs

optional arguments:
  -h, --help           show this help message and exit
  --dry-run            Do not make any changes
  --verbose            Print debug information
  --log-file LOG_FILE  Log file. If extension is .har, log in HAR format
  --token TOKEN        Access token can be provided using --token argument, set in
                       WEBEX_ACCESS_TOKEN environment variable or can be a service app token. For
                       the latter set environment variables ('SERVICE_APP_REFRESH_TOKEN',
                       'SERVICE_APP_CLIENT_ID', 'SERVICE_APP_CLIENT_SECRET'). Environment variables
                       can also be set in add_numbers.env
  --inactive           Add TNs as inactive

Example: add_numbers.py add_numbers.csv --log-file add_numbers.har --dry-run

"""
import argparse
import asyncio
import csv
import logging
import os
import sys
from argparse import Namespace
from collections import defaultdict, Counter
from contextlib import contextmanager
from itertools import chain
from typing import Optional

import yaml
from dotenv import load_dotenv

from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import NumberState
from wxc_sdk.har_writer import HarWriter
from wxc_sdk.integration import Integration
from wxc_sdk.tokens import Tokens

BATCH_SIZE = 10
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
        print(f'Access token can be provided using --token argument, set in WEBEX_ACCESS_TOKEN environment variable or '
              f'can be a service app token. For the latter set environment variables {SERVICE_APP_ENVS}. Environment '
              f'variables can '
              f'also be set in {env_path()}', file=sys.stderr)
        exit(1)

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
    if tokens.remaining < 24 * 60 * 60:
        tokens = get_access_token()
    return tokens


@contextmanager
def setup_logging(args: Namespace, api: AsWebexSimpleApi):
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
    # console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(console_handler)
    with file_handler(args.log_file):
        yield


def read_csv(file: str) -> dict[str, list[str]]:
    """
    Read CSV file with location names and TNs
    """
    if not os.path.isfile(file):
        logging.error(f'File {file} does not exist')
        exit(1)
    err = False
    locations_and_tns: dict[str, list[str]] = defaultdict(list)
    with open(file, mode='r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            if len(row) != 2:
                logging.error(f'Invalid row: {row}')
                err = True
                continue
            location, tn = row
            logging.debug(f'Location: {location}, TN: {tn}')
            locations_and_tns[location].append(tn)
    if err:
        logging.error('Errors in the CSV file')
        exit(1)
    return locations_and_tns


async def verify_location(api: AsWebexSimpleApi, location_name: str) -> Optional[str]:
    """
    Verify that a location exists and return location id
    """
    try:
        location = next((l
                         for l in await api.telephony.locations.list(name=location_name)
                         if l.name == location_name),
                        None)
        return location and location.location_id
    except Exception as e:
        logging.error(f'Failed to get location {location_name}: {e}')
        return None


async def validate_tns(api: AsWebexSimpleApi, tns: list[str]) -> bool:
    """
    Validate TNs and return validity
    """
    tn_counter = Counter(tns)
    err = False
    for tn, count in tn_counter.items():
        if count > 1:
            err = True
            logging.error(f'TN {tn} is duplicated')
    if err:
        return False

    # validate numbers in batches
    try:
        validations = await asyncio.gather(*[api.telephony.validate_phone_numbers(tns[i:i + BATCH_SIZE])
                                             for i in range(0, len(tns), BATCH_SIZE)])
    except Exception as e:
        logging.error(f'Failed to validate TNs: {e}')
        return False

    ok_tns = []
    err = False
    for status in chain.from_iterable(v.phone_numbers for v in validations):
        if status.ok:
            ok_tns.append(status.phone_number)
        else:
            err = True
            logging.error(f'TN {status.phone_number}: {status.state} ')
    return not err


async def add_tns(api: AsWebexSimpleApi, location_id: str, tns: list[str], inactive: bool):
    """
    Add TNs to a location
    """
    number_state = NumberState.inactive if inactive else NumberState.active
    try:
        # add TNs in batches
        await asyncio.gather(*[api.telephony.location.number.add(location_id=location_id,
                                                                 phone_numbers=tns[i:i + BATCH_SIZE],
                                                                 state=number_state)
                               for i in range(0, len(tns), BATCH_SIZE)])
    except Exception as e:
        logging.error(f'Failed to add TNs: {e}')
        return False
    return True


async def add_numbers():
    """
    Add TNs to Webex Calling locations
    """
    # get commandline arguments
    parser = argparse.ArgumentParser(description='Add TNs to Webex Calling locations',
                                     epilog='Example: %(prog)s add_numbers.csv --log-file add_numbers.har --dry-run')
    parser.add_argument('file', help='CSV file with location names and TNs')
    parser.add_argument('--dry-run', action='store_true', help='Do not make any changes')
    parser.add_argument('--verbose', action='store_true', help='Print debug information')
    parser.add_argument('--log-file', help='Log file. If extension is .har, log in HAR format')
    parser.add_argument('--token', help=f'Access token can be provided using --token argument, set in '
                                        f'WEBEX_ACCESS_TOKEN environment variable or can be a service app token. For '
                                        f'the latter set environment variables {SERVICE_APP_ENVS}. Environment '
                                        f'variables can also be set in {env_path()}')
    parser.add_argument('--inactive', action='store_true', help='Add TNs as inactive')
    args = parser.parse_args()
    token = args.token or os.getenv('WEBEX_ACCESS_TOKEN') or get_tokens().access_token
    async with AsWebexSimpleApi(tokens=token) as api:
        with setup_logging(args, api):
            # validate the access token
            try:
                await api.people.me()
            except Exception as e:
                logging.error(f'Failed to get identity: {e}')
                logging.error('Token might be invalid')
                exit(1)
            # read location names and TNs from a CSV file
            logging.info(f'Reading file {args.file}')
            locations_and_tns = read_csv(args.file)

            # validate the location names
            logging.info('Validating location names...')
            location_ids = await asyncio.gather(*[verify_location(api, location)
                                                  for location in locations_and_tns.keys()])
            if not all(location_ids):
                for location_name, location_id in zip(locations_and_tns.keys(), location_ids):
                    if not location_id:
                        logging.error(f'Location {location_name} does not exist')
                exit(1)

            # validate the TNs
            logging.info('Validating TNs...')
            tn_list = list(chain.from_iterable(locations_and_tns.values()))
            validation = await validate_tns(api, tn_list)
            if not validation:
                exit(1)

            # add TNs to the locations
            if not args.dry_run:
                logging.info('Adding TNs...')
                results = await asyncio.gather(*[add_tns(api, location_id, tns, args.inactive)
                                                 for location_id, tns in zip(location_ids,
                                                                             locations_and_tns.values())])
                if not all(results):
                    exit(1)
            #
            logging.info('Done')
        # end of logging context
    # end of API context
    return


if __name__ == '__main__':
    asyncio.run(add_numbers())

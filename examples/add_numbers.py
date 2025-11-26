#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "python-dotenv",
#     "typer",
#     "wxc-sdk",
# ]
# ///
"""
Add TNs to a locations.

 Usage: add_numbers.py [OPTIONS] FILE

 Add TNs to Webex Calling locations

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────╮
│ *    file      PATH  CSV file with location names and TNs [required]                       │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────╮
│ --dry-run                         Do not make any changes                                  │
│ --verbose                         Print debug information                                  │
│ --log-file                  PATH  Log file. If extension is .har, log in HAR format        │
│ --token                     TEXT  Access token can be provided using --token argument, set │
│                                   in WEBEX_ACCESS_TOKEN environment variable or can be a   │
│                                   service app token. For the latter set environment        │
│                                   variables ('SERVICE_APP_REFRESH_TOKEN',                  │
│                                   'SERVICE_APP_CLIENT_ID', 'SERVICE_APP_CLIENT_SECRET').   │
│                                   Environment variables can also be set in add_numbers.env │
│ --inactive                        Add TNs as inactive                                      │
│ --install-completion              Install completion for the current shell.                │
│ --show-completion                 Show completion for the current shell, to copy it or     │
│                                   customize the installation.                              │
│ --help                            Show this message and exit.                              │
╰────────────────────────────────────────────────────────────────────────────────────────────╯

 Example: ./add_numbers.py add_numbers.csv --log-file add_numbers.har --dry-run

"""
import asyncio
import csv
import logging
import os
import sys
from collections import defaultdict, Counter
from contextlib import contextmanager
from functools import wraps
from itertools import chain
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv

from service_app import SERVICE_APP_ENVS, env_path, get_tokens
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import NumberState
from wxc_sdk.har_writer import HarWriter
from wxc_sdk.tokens import Tokens

BATCH_SIZE = 10


@contextmanager
def setup_logging(*, api: AsWebexSimpleApi, verbose: bool, log_file: Optional[Path]):
    """
    Set up logging
    """

    @contextmanager
    def file_handler():
        if not log_file:
            yield
        else:
            # log to file or to HAR
            log_file_str = str(log_file)
            if os.path.splitext(log_file_str)[-1].lower() == '.har':
                with HarWriter(api=api, path=log_file_str):
                    yield
            else:
                f_handler = logging.FileHandler(log_file_str)
                f_handler.setLevel(logging.DEBUG)
                f_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
                logging.getLogger().addHandler(f_handler)
                yield
        return

    logging.getLogger().setLevel(logging.DEBUG)
    # create a console logging handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    # console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(console_handler)
    with file_handler():
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


def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


app = typer.Typer()


@app.command(epilog=f'Example: {sys.argv[0]} add_numbers.csv --log-file add_numbers.har --dry-run',
             help='Add TNs to Webex Calling locations')
@async_command
async def add_numbers(file: Path = typer.Argument(exists=True,
                                                  help='CSV file with location names and TNs'),
                      dry_run: bool = typer.Option(False, '--dry-run',
                                                   help='Do not make any changes'),
                      verbose: bool = typer.Option(False, '--verbose',
                                                   help='Print debug information'),
                      log_file: Optional[Path] = typer.Option(None, '--log-file',
                                                              help='Log file. If extension is .har, log in HAR format'),
                      token: Optional[str] = typer.Option(None, '--token',
                                                          help=f'Access token can be provided using --token argument, '
                                                               f'set in WEBEX_ACCESS_TOKEN environment variable or '
                                                               f'can be a service app token. For the latter set '
                                                               f'environment variables {SERVICE_APP_ENVS}. '
                                                               f'Environment variables can also be set in '
                                                               f'{env_path()}'),
                      inactive: bool = typer.Option(False, '--inactive',
                                                    help='Add TNs as inactive')

                      ):
    """
    Add TNs to Webex Calling locations
    """
    load_dotenv(env_path(), override=True)
    tokens = get_tokens() if token is None else Tokens(access_token=token)
    if tokens is None:
        print(f'Access token can be provided using --token argument, set in WEBEX_ACCESS_TOKEN environment variable or '
              f'can be a service app token. For the latter set environment variables {SERVICE_APP_ENVS}. Environment '
              f'variables can '
              f'also be set in {env_path()}', file=sys.stderr)
        exit(1)

    async with AsWebexSimpleApi(tokens=tokens) as api:
        with setup_logging(api=api, verbose=verbose, log_file=log_file):
            # validate the access token
            try:
                await api.people.me()
            except Exception as e:
                logging.error(f'Failed to get identity: {e}')
                logging.error('Token might be invalid')
                exit(1)
            # read location names and TNs from a CSV file
            logging.info(f'Reading file {file}')
            locations_and_tns = read_csv(file)

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
            if not dry_run:
                logging.info('Adding TNs...')
                results = await asyncio.gather(*[add_tns(api, location_id, tns, inactive)
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
    app()

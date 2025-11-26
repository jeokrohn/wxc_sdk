#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "typer",
#     "wxc-sdk",
#     "python-dotenv",
# ]
# ///
"""
Provision location level access codes from a CSV file
the CSV file should have the following columns:
- location: location name
- code: the access code
- description: a description of the access code
- operation: one of 'add', 'delete'

Usage: access_codes.py [OPTIONS] CSV_FILE

 Provision location level access codes from a CSV file

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────╮
│ *    csv_file      PATH  CSV file with access codes [required]                             │
╰────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────╮
│ --dry-run                         Do not make any changes                                  │
│ --token                     TEXT  Access token can be provided using --token argument, set │
│                                   in WEBEX_ACCESS_TOKEN environment variable or can be a   │
│                                   service app token. For the latter set environment        │
│                                   variables ('SERVICE_APP_REFRESH_TOKEN',                  │
│                                   'SERVICE_APP_CLIENT_ID', 'SERVICE_APP_CLIENT_SECRET').   │
│                                   Environment variables can also be set in                 │
│                                   access_codes.env                                         │
│ --install-completion              Install completion for the current shell.                │
│ --show-completion                 Show completion for the current shell, to copy it or     │
│                                   customize the installation.                              │
│ --help                            Show this message and exit.                              │
╰────────────────────────────────────────────────────────────────────────────────────────────╯

"""
import asyncio
import csv
import logging
import sys
from collections import defaultdict
from functools import reduce
from os.path import basename
from pathlib import Path
from typing import Literal, Optional

import typer
from dotenv import load_dotenv
from pydantic import BaseModel, TypeAdapter

from service_app import SERVICE_APP_ENVS, env_path, get_tokens
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import AuthCode
from wxc_sdk.telephony.location import TelephonyLocation
from wxc_sdk.tokens import Tokens


class CSVOperation(BaseModel):
    """
    row in CSV file: Operation to be performed on an access code
    """
    location: str
    code: str
    description: str
    operation: Literal['add', 'delete']


async def process_operations(*, operations: list[CSVOperation], token: str, dry_run:bool):
    """
    Process the operations from the CSV file in parallel
    """

    # noinspection PyShadowingNames
    async def process_one_location(*, location: str, operations: list[CSVOperation]):
        """
        process operations for one location
        """
        # find the location
        loc = locations.get(location)
        if loc is None:
            print(f'Location {location} not found', sys.stderr)
            return

        # get existing codes in location
        ac_codes: dict[str, AuthCode] = {ac.code: ac
                                         for ac in await api.telephony.access_codes.read(location_id=loc.location_id)}

        tasks = []
        delete_operations = [operation
                             for operation in operations
                             if operation.operation == 'delete']
        non_existing = [op
                        for op in delete_operations
                        if op.code not in ac_codes]
        if non_existing:
            print(f'Location {location}: access codes not found: {", ".join(op.code for op in non_existing)}',
                  file=sys.stderr)
        to_delete = [ac
                     for ac in delete_operations
                     if ac.code in ac_codes]
        print(f'Location {location}: deleting access codes: {", ".join(op.code for op in to_delete)}')
        if to_delete:
            tasks.append(api.telephony.access_codes.delete_codes(location_id=loc.location_id,
                                                                 access_codes=[op.code for op in to_delete]))

        add_operations = [operation
                          for operation in operations
                          if operation.operation == 'add']
        existing = [op for op in add_operations if op.code in ac_codes]
        if existing:
            print(f'Location {location}: access codes already exist: {", ".join(op.code for op in existing)}',
                  file=sys.stderr)
        to_add = [ac for ac in add_operations if ac.code not in ac_codes]
        print(f'Location {location}: adding access codes: {", ".join(op.code for op in to_add)}')
        if to_add:
            tasks.append(api.telephony.access_codes.create(location_id=loc.location_id,
                                                           access_codes=[AuthCode(code=op.code,
                                                                                  description=op.description)
                                                                         for op in to_add]))
        if tasks and not dry_run:
            await asyncio.gather(*tasks)

    async with AsWebexSimpleApi(tokens=token) as api:
        # get locations
        locations: dict[str, TelephonyLocation] = {loc.name: loc for loc in await api.telephony.locations.list()}

        # group operations by location
        operations_by_location: dict[str, list[CSVOperation]] = reduce(
            lambda acc, op: acc[op.location].append(op) or acc,
            operations,
            defaultdict(list))

        # process all locations in parallel
        await asyncio.gather(*[process_one_location(location=loc, operations=ops)
                               for loc, ops in operations_by_location.items()])
    return


app = typer.Typer()


@app.command(name=basename(__file__),
             help='Provision location level access codes from a CSV file')
def main(csv_file: Path = typer.Argument(exists=True,
                                         help='CSV file with access codes'),
         dry_run: bool = typer.Option(False, '--dry-run',
                                      help='Do not make any changes'),

         token: Optional[str] = typer.Option(None, '--token',
                                             help=f'Access token can be provided using --token argument, '
                                                  f'set in WEBEX_ACCESS_TOKEN environment variable or '
                                                  f'can be a service app token. For the latter set '
                                                  f'environment variables {SERVICE_APP_ENVS}. '
                                                  f'Environment variables can also be set in '
                                                  f'{env_path()}')):
    # get access token
    load_dotenv(env_path(), override=True)
    tokens = get_tokens() if token is None else Tokens(access_token=token)
    if tokens is None:
        print(f'Access token can be provided using --token argument, set in WEBEX_ACCESS_TOKEN environment variable or '
              f'can be a service app token. For the latter set environment variables {SERVICE_APP_ENVS}. Environment '
              f'variables can '
              f'also be set in {env_path()}', file=sys.stderr)
        exit(1)

    csv_file = str(csv_file)
    # read CSV file
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # validate the data from the CSV file
    csv_operations = TypeAdapter(list[CSVOperation]).validate_python(data)

    asyncio.run(process_operations(operations=csv_operations,
                                   token=tokens,
                                   dry_run=dry_run))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app()

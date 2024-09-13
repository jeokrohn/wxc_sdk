#!/usr/bin/env python
"""
Provision location level access codes from a CSV file
the CSV file should have the following columns:
- location: location name
- code: the access code
- description: a description of the access code
- operation: one of 'add', 'delete', 'update'

usage: access_codes.py [-h] [--token TOKEN] csv_file

Provision location level access codes from a CSV file

positional arguments:
  csv_file       CSV file with access codes

options:
  -h, --help     show this help message and exit
  --token TOKEN  API token


"""
import asyncio
import csv
import logging
import sys
from argparse import ArgumentParser
from collections import defaultdict
from functools import reduce
from os.path import basename, isfile
from typing import Literal

from pydantic import BaseModel, TypeAdapter

from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import AuthCode
from wxc_sdk.telephony.location import TelephonyLocation


class CSVOperation(BaseModel):
    location: str
    code: str
    description: str
    operation: Literal['add', 'delete']


async def process_operations(operations: list[CSVOperation], token: str):
    """
    Process the operations from the CSV file in parallel
    """
    async def process_one_location(location: str, operations: list[CSVOperation]):
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
        if to_add:
            tasks.append(api.telephony.access_codes.create(location_id=loc.location_id,
                                                           access_codes=[AuthCode(code=op.code,
                                                                                  description=op.description)
                                                                         for op in to_add]))
        if tasks:
            await asyncio.gather(*tasks)

    async with AsWebexSimpleApi(tokens=token) as api:
        # get locations
        locations: dict[str, TelephonyLocation] = {loc.name: loc for loc in await api.telephony.locations.list()}

        # group operations by location
        operations_by_location: dict[str, list[CSVOperation]] = reduce(
            lambda acc, op: acc[op.location].append(op) or acc, operations,
            defaultdict(list))

        # process all locations in parallel
        await asyncio.gather(*[process_one_location(loc, ops) for loc, ops in operations_by_location.items()])


def main():
    parser = ArgumentParser(prog=basename(__file__),
                            description='Provision location level access codes from a CSV file')
    parser.add_argument('csv_file', help='CSV file with access codes')
    parser.add_argument('--token', help='API token')
    args = parser.parse_args()
    csv_file = args.csv_file
    if not isfile(csv_file):
        parser.error(f'File {csv_file} not found')
    # read CSV file
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # validate the date from the CSV file
    csv_operations = TypeAdapter(list[CSVOperation]).validate_python(data)

    asyncio.run(process_operations(csv_operations, args.token))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()

#!/usr/bin/env python
"""
Create workspaces with 3rd party devices.
From a CSV read:
    * workspace name: if workspace doesn't exist a new workspace will be created
    * location name: must be an existing location
    * extension (optional); if missing a new extension will be generated starting at 2000
    * MAC address; if empty a new (dummy) MAC address will be generated as DEAD-DEAD-XXXX
    * password (optional); if missing a new (random password will be generated
The output is a CSV file with the following columns:
    * workspace name
    * location name
    * extension
    * MAC address
    * password
    * outbound proxy
    * SIP user name
    * line/port

usage: workspace_w_3rd_party.py [-h] [--token TOKEN] [--dry-run]
                                [--log-file LOG_FILE]
                                csv [output]

Provision workspaces with 3rd party devices.

positional arguments:
  csv                  CSV with workspaces to provision. CSV has the
                       following columns: * workspace name: the workspace
                       will be created * location name: must be an
                       existing location * extension (optional); if
                       missing a new extension will be generated starting
                       at 2000 * MAC address; if empty a new (dummy) MAC
                       address will be generated as DEAD-DEAD-XXXX *
                       password (optional); if missing a new (random
                       password will be generated
  output               Output CSV with the provisioning results. Not
                       required in dry-run mode

optional arguments:
  -h, --help           show this help message and exit
  --token TOKEN        Access token can be provided using --token
                       argument, set in WEBEX_ACCESS_TOKEN environment
                       variable or can be a service app token. For the
                       latter set environment variables
                       ('SERVICE_APP_REFRESH_TOKEN',
                       'SERVICE_APP_CLIENT_ID',
                       'SERVICE_APP_CLIENT_SECRET'). Environment variables
                       can also be set in workspace_w_3rd_party.env
  --dry-run            Dry run, do not provision anything
  --log-file LOG_FILE  Log file. If extension is .har, log in HAR format

Example: workspace_w_3rd_party.py input.csv output.csv --log-file log.har
"""
import argparse
import asyncio
import csv
import logging
import os
import sys
from collections import defaultdict
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass, field
from itertools import zip_longest, chain

from dotenv import load_dotenv

from examples.service_app import SERVICE_APP_ENVS, env_path, get_tokens
from open_api.generated.Shared.workspaces_auto import WorkspaceType
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import DevicePlatform
from wxc_sdk.har_writer import HarWriter
from wxc_sdk.licenses import License
from wxc_sdk.telephony.devices import MACState, MACValidationResponse
from wxc_sdk.telephony.location import TelephonyLocation
from wxc_sdk.tokens import Tokens
from wxc_sdk.workspaces import Workspace, WorkspaceSupportedDevices, WorkspaceCalling, CallingType, \
    WorkspaceWebexCalling

MAC_VALIDATION_BATCH_SIZE = 100


@dataclass
class CSVRow:
    """
    CSV row with workspace and location name
    """
    workspace_name: str
    location_name: str
    extension: str
    mac_address: str
    password: str
    workspace: Workspace = field(default=None, init=False)
    calling_license_id: str = field(default=None, init=False)
    location: TelephonyLocation = field(default=None, init=False)
    outbound_proxy: str = field(default=None, init=False)
    sip_user_name: str = field(default=None, init=False)
    line_port: str = field(default=None, init=False)

    def __post_init__(self):
        # clean up some data
        self.workspace_name = self.workspace_name.strip()
        self.location_name = self.location_name.strip()
        self.extension = self.extension.strip() or None
        self.mac_address = self.mac_address.strip().lower() or None
        self.password = self.password.strip() or None

    @classmethod
    def from_csv(cls, csv_path: str) -> Generator['CSVRow', None, None]:
        """
        Yield CSVRow instances from CSV file
        """
        err = False
        with open(csv_path, newline='') as csv_file:
            reader = csv.reader(csv_file)
            for row_number, row in enumerate(reader, 1):
                try:
                    yield cls(*row)
                except TypeError as te:
                    err = True
                    print(f'Failed to parse row {row_number}: {te}', file=sys.stderr)
                    continue
        if err:
            print(f'Failed to parse {csv_path}', file=sys.stderr)
            exit(1)
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
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(console_handler)
    with file_handler(args.log_file):
        yield


# list of validation errors
ValidationResult = list[tuple[int, str]]


async def validate_extensions(*, api: AsWebexSimpleApi, location: TelephonyLocation,
                              indexed_rows: list[tuple[int, CSVRow]]) -> ValidationResult:
    """
    Make sure that extensions are unique; if no extension is provided, generate a new one
    """
    extensions_in_location = {number.extension for number in
                              await api.telephony.phone_numbers(location_id=location.location_id)
                              if number.extension is not None}
    errors = []
    for row_index, csv_row in indexed_rows:
        if csv_row.extension:
            if csv_row.extension in extensions_in_location:
                errors.append((row_index, f'Duplicate extension "{csv_row.extension}" in location "{location.name}"'))
        else:
            # generate new extension
            csv_row.extension = next((str(ext) for ext in range(2000, 10000)
                                      if str(ext) not in extensions_in_location))
            print(f'Row {row_index}: Generated new extension "{csv_row.extension}"')
        extensions_in_location.add(csv_row.extension)

    return errors


async def generate_passwords(*, api: AsWebexSimpleApi, location: TelephonyLocation,
                             indexed_rows: list[tuple[int, CSVRow]]) -> ValidationResult:
    """
    Generate random passwords for rows without a password
    """
    new_passwords = await asyncio.gather(*[api.telephony.location.generate_password(location_id=location.location_id)
                                           for _, csv_row in indexed_rows
                                           if not csv_row.password])

    for row_index, csv_row in indexed_rows:
        if not csv_row.password:
            # generate new password
            csv_row.password = new_passwords.pop(0)
            print(f'Row {row_index}: Generated new password "{csv_row.password}"')
    return []


async def validate_locations_and_extensions(*, api: AsWebexSimpleApi, csv_rows: list[CSVRow],
                                            cleanup: bool) -> ValidationResult:
    """
    Locations must exist and extensions must be unique
    """
    if cleanup:
        return []
    locations = {location.name: location
                 for location in await api.telephony.locations.list()}
    errors = []
    for row_index, csv_row in enumerate(csv_rows, 1):
        location = locations.get(csv_row.location_name)
        if not location:
            errors.append((row_index, f'Location "{csv_row.location_name}" does not exist'))
        csv_row.location = location

    # for all existing locations validate extensions
    csv_rows_by_location: dict[str, list[tuple[int, CSVRow]]] = defaultdict(list)
    for row_index, csv_row in enumerate(csv_rows, 1):
        if csv_row.location_name in locations:
            csv_rows_by_location[csv_row.location_name].append((row_index, csv_row))
    tasks = [validate_extensions(api=api, location=locations[l_name],
                                 indexed_rows=indexed_rows)
             for l_name, indexed_rows in csv_rows_by_location.items()]
    # also generate passwords for rows without a password
    tasks.extend(generate_passwords(api=api, location=locations[l_name], indexed_rows=indexed_rows)
                 for l_name, indexed_rows in csv_rows_by_location.items())
    location_results = await asyncio.gather(*tasks)
    errors.extend(chain.from_iterable(location_results))
    return errors


async def assign_new_mac_addresses(*, api: AsWebexSimpleApi, csv_rows: list[CSVRow]) -> ValidationResult:
    """
    Get new MAC addresses for rows where no MAC address is provided
    """
    number_of_missing_mac_addresses = sum(1
                                          for csv_row in csv_rows
                                          if not csv_row.mac_address)

    if not number_of_missing_mac_addresses:
        return []
    mac_prefix = 'DEADDEAD'
    mac_addresses_in_csv = {csv_row.mac_address
                            for csv_row in csv_rows
                            if csv_row.mac_address}

    def mac_candidates() -> Generator[str, None, None]:
        for v in range(0, 65536):
            candidate = f'{mac_prefix}{hex(v)[2:].zfill(4).upper()}'
            if candidate in mac_addresses_in_csv:
                # skip mac addresses that are already in the csv
                continue
            yield f'{mac_prefix}{hex(v)[2:].zfill(4).upper()}'

    new_mac_addresses = []

    # test macs in batches
    batch_args = [mac_candidates()] * MAC_VALIDATION_BATCH_SIZE

    # noinspection PyArgumentList
    batches = zip_longest(*batch_args)
    for batch in batches:
        validation_result = await api.telephony.devices.validate_macs(macs=list(batch))
        errored_macs = set(ms.mac
                           for ms in (validation_result.mac_status or [])
                           if ms.state != MACState.available)
        new_mac_addresses.extend((mac for mac in batch if mac not in errored_macs))
        if len(new_mac_addresses) >= number_of_missing_mac_addresses:
            break
    for row_index, csv_row in enumerate(csv_rows, 1):
        if not csv_row.mac_address:
            # generate new MAC address
            csv_row.mac_address = new_mac_addresses.pop(0)
            print(f'Row {row_index}: Generated new MAC address "{csv_row.mac_address}"')
    return []


async def mac_addresses_available(*, api: AsWebexSimpleApi, csv_rows: list[CSVRow]) -> ValidationResult:
    """
    Check if MAC addresses provided in CSV are available
    """
    errors = []
    mac_addresses = list(set(csv_row.mac_address for csv_row in csv_rows if csv_row.mac_address))
    if not mac_addresses:
        return []

    # validate in batches
    batches = [mac_addresses[i:i + MAC_VALIDATION_BATCH_SIZE]
               for i in range(0, len(mac_addresses), MAC_VALIDATION_BATCH_SIZE)]
    results = await asyncio.gather(*[api.telephony.devices.validate_macs(macs=batch)
                                     for batch in batches])
    results: list[MACValidationResponse]

    errored_macs: dict[str, str] = dict()
    for result in results:
        errored_macs.update((ms.mac, f'{ms.state}, {ms.message}')
                            for ms in (result.mac_status or [])
                            if ms.state != MACState.available)

    if not errored_macs:
        return []
    for row_index, csv_row in enumerate(csv_rows, 1):
        if csv_row.mac_address and csv_row.mac_address in errored_macs:
            errors.append((row_index, f'MAC address "{csv_row.mac_address}": {errored_macs[csv_row.mac_address]}'))
    return errors


async def validate_mac_addresses(*, api: AsWebexSimpleApi, csv_rows: list[CSVRow],
                                 cleanup: bool) -> ValidationResult:
    """
    mac addresses must be unique and available
    """
    if cleanup:
        return []
    mac_addresses = set()
    errors = []
    # check if provided MAC addresses are unique
    for row_index, csv_row in enumerate(csv_rows, 1):
        if csv_row.mac_address:
            if csv_row.mac_address in mac_addresses:
                errors.append((row_index, f'Duplicate MAC address "{csv_row.mac_address}"'))
            mac_addresses.add(csv_row.mac_address)

    results = await asyncio.gather(assign_new_mac_addresses(api=api, csv_rows=csv_rows),
                                   mac_addresses_available(api=api, csv_rows=csv_rows))
    errors.extend(chain.from_iterable(results))
    return errors


async def validate_workspaces_and_licenses(*, api: AsWebexSimpleApi, csv_rows: list[CSVRow],
                                           cleanup: bool) -> ValidationResult:
    """
    Workspaces should not exist, also get license for new workspaces
    """
    tasks = [api.workspaces.list()]
    if not cleanup:
        tasks.append(api.licenses.list())
    results = await asyncio.gather(*tasks)
    workspace_list = results[0]
    if cleanup:
        licenses = []
    else:
        licenses = results[1]
    workspace_list: list[Workspace]
    licenses: list[License]
    workspaces = {ws.display_name: ws
                  for ws in workspace_list}

    def calling_license_id() -> Generator[str, None, None]:
        """
        calling license id for license with available entitlement
        """
        candidate_licenses = [lic for lic in licenses
                              if lic.webex_calling_workspaces or lic.webex_calling_professional]
        # make sure to consume workspace licenses first
        candidate_licenses.sort(key=lambda x: x.name, reverse=True)
        for lic in candidate_licenses:
            while lic.consumed_units < lic.total_units:
                lic.consumed_units += 1
                yield lic.license_id
        return

    errors = []
    license_id_gen = calling_license_id()
    for row_index, csv_row in enumerate(csv_rows, 1):
        # check if workspace exists
        ws = workspaces.get(csv_row.workspace_name)
        csv_row.workspace = ws
        if cleanup:
            if not ws:
                errors.append((row_index, f'Workspace "{csv_row.workspace_name}" does not exist'))
            continue
        if ws:
            errors.append((row_index, f'Workspace "{csv_row.workspace_name}" already exists'))
        # get a license for the workspace
        try:
            license_id = next(license_id_gen)
        except StopIteration:
            errors.append((row_index, f'No more licenses available for "{csv_row.workspace_name}"'))
            continue
        csv_row.calling_license_id = license_id
    return errors


async def validate_and_prepare(*, api: AsWebexSimpleApi, csv_rows: list[CSVRow], cleanup: bool) -> None:
    """
    validate csv and prepare for provisioning
        * location exists
        * extensions are unique (if provided)
        * MAC addresses are unique (if provided)
        * workspace names are unique
        * no devices in the workspace
    """
    results = await asyncio.gather(validate_locations_and_extensions(api=api, csv_rows=csv_rows, cleanup=cleanup),
                                   validate_mac_addresses(api=api, csv_rows=csv_rows, cleanup=cleanup),
                                   validate_workspaces_and_licenses(api=api, csv_rows=csv_rows, cleanup=cleanup))
    errors = list(chain.from_iterable(results))
    errors: ValidationResult
    errors.sort(key=lambda x: x[0])
    if errors:
        print('Validation errors:', file=sys.stderr)
        for row_index, error in errors:
            print(f'Row {row_index}: {error}', file=sys.stderr)
        exit(1)
    return


async def delete_workspaces(*, api: AsWebexSimpleApi, csv_rows: list[CSVRow], dry_run: bool) -> None:
    """
    cleanup: delete workspaces
    """

    async def delete_one_workspace(workspace: Workspace) -> None:
        if dry_run:
            print(f'Delete workspace "{workspace.display_name}"')
        else:
            await api.workspaces.delete_workspace(workspace_id=workspace.workspace_id)
            print(f'Deleted workspace "{workspace.display_name}"')
        return

    await asyncio.gather(*[delete_one_workspace(csv_row.workspace)
                           for csv_row in csv_rows
                           if csv_row.workspace])


async def provision_row(*, api: AsWebexSimpleApi, csv_row: CSVRow) -> None:
    """
    Provision a single row
    """
    # create workspace
    settings = Workspace(location_id=csv_row.location.location_id,
                         display_name=csv_row.workspace_name,
                         type=WorkspaceType.desk,
                         capacity=1,
                         supported_devices=WorkspaceSupportedDevices.phones,
                         device_platform=DevicePlatform.cisco,
                         calling=WorkspaceCalling(type=CallingType.webex,
                                                  webex_calling=WorkspaceWebexCalling(
                                                      licenses=[csv_row.calling_license_id],
                                                      extension=csv_row.extension,
                                                      location_id=csv_row.location.location_id)))
    workspace = await api.workspaces.create(settings=settings)
    print(f'Provisioned workspace "{workspace.display_name}"')

    # create device
    device = await api.devices.create_by_mac_address(mac=csv_row.mac_address,
                                                     workspace_id=workspace.workspace_id,
                                                     model='Generic IPPhone Customer Managed',
                                                     password=csv_row.password)

    details = await api.telephony.devices.details(device_id=device.device_id)
    print(f'Provisioned device in workspace "{workspace.display_name}"')
    csv_row.sip_user_name = details.owner.sip_user_name
    csv_row.line_port = details.owner.line_port
    csv_row.outbound_proxy = details.proxy.outbound_proxy

    return


def main():
    async def as_main():
        # read CSV file
        csv_rows = list(CSVRow.from_csv(csv_file))
        async with AsWebexSimpleApi(tokens=tokens) as api:
            with setup_logging(args, api):
                # validation and preparation for provisioning
                await validate_and_prepare(api=api, csv_rows=csv_rows, cleanup=args.cleanup)
                if args.dry_run:
                    print('Dry run, not provisioning anything')
                    return
                if args.cleanup:
                    await delete_workspaces(api=api, csv_rows=csv_rows, dry_run=args.dry_run)
                else:
                    await asyncio.gather(*[provision_row(api=api, csv_row=csv_row)
                                           for csv_row in csv_rows])
                # write output
                if args.output:
                    with open(args.output, 'w', newline='') as output:
                        writer = csv.writer(output)
                        writer.writerow(['workspace_name', 'location_name', 'extension', 'mac_address',
                                         'password', 'outbound_proxy', 'sip_user_name', 'line_port'])
                        for csv_row in csv_rows:
                            writer.writerow([csv_row.workspace_name, csv_row.location_name,
                                             csv_row.extension, csv_row.mac_address,
                                             csv_row.password, csv_row.outbound_proxy,
                                             csv_row.sip_user_name, csv_row.line_port])
                    # for
                # with open
            # with setup_logging
        # async with AsWebexSimpleApi
        return

    # parse arguments
    parser = argparse.ArgumentParser(
        description="Provision workspaces with 3rd party devices.",
        epilog='Example: %(prog)s input.csv output.csv --log-file log.har')
    parser.add_argument('csv', type=str, help="""CSV with workspaces to provision. CSV has the following columns:
    * workspace name: the workspace will be created
    * location name: must be an existing location
    * extension (optional); if missing a new extension will be generated starting at 2000
    * MAC address; if empty a new (dummy) MAC address will be generated as DEAD-DEAD-XXXX
    * password (optional); if missing a new (random password will be generated""")
    parser.add_argument('output', nargs='?', type=str,
                        help='Output CSV with the provisioning results. Not required in dry-run mode')
    parser.add_argument('--token',
                        help=f'Access token can be provided using --token argument, set in '
                             f'WEBEX_ACCESS_TOKEN environment variable or can be a service app token. For '
                             f'the latter set environment variables {SERVICE_APP_ENVS}. Environment '
                             f'variables can also be set in {env_path()}')
    parser.add_argument('--dry-run', action='store_true', help='Dry run, do not provision anything')
    parser.add_argument('--log-file', help='Log file. If extension is .har, log in HAR format')
    parser.add_argument('--cleanup', action='store_true', help='remove workspaces')
    args = parser.parse_args()
    if not any((args.output, args.dry_run, args.cleanup)):
        parser.error('Output file is required if not dry-run cleanup mode')
    csv_file = args.csv
    if not os.path.isfile(csv_file):
        print(f'File {csv_file} does not exist', file=sys.stderr)
        exit(1)

    # read tokens
    load_dotenv(env_path())
    tokens = get_tokens() if args.token is None else Tokens(access_token=args.token)
    if tokens is None:
        print(
            f'Access token can be provided using --token argument, set in WEBEX_ACCESS_TOKEN environment variable '
            f'or can be a service app token. For the latter set environment variables {SERVICE_APP_ENVS}. Environment '
            f'variables can also be set in {env_path()}', file=sys.stderr)
        exit(1)

    asyncio.run(as_main())


if __name__ == '__main__':
    main()

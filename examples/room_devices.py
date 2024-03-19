#!/usr/bin/env python
"""
    usage: room_devices.py [-h] [--location LOCATION] [--wsnames WSNAMES] [--test] {show,clear}

    CLI tool to manage room device calling entitlements

    positional arguments:
      {show,clear}         show: show all room devices with their calling settings, clear: remove calling
                           license from devices

    optional arguments:
      -h, --help           show this help message and exit
      --location LOCATION  work on devices in given location
      --wsnames WSNAMES    file name of a file with workspace names to operate on; one name per line
      --test               test run only

    The tool reads environment variables from room_devices.env:
        SERVICE_APP_CLIENT_ID=<clients id of a service app created on developer.webex.com>
        SERVICE_APP_CLIENT_SECRET=<clients secret of a service app created on developer.webex.com>
        SERVICE_APP_REFRESH_TOKEN=<refresh token of the service app obtained after the service app has been
                                        authorized for an org>

    This information is used to obtain an access token required to authorize API access

    This is a super-set of the scopes the service app needs:
        * spark-admin:workspaces_write
        * Identity:one_time_password
        * identity:placeonetimepassword_create
        * spark:people_read
        * spark-admin:workspace_locations_read
        * spark-admin:workspaces_read
        * spark:devices_write
        * spark:devices_read
        * spark:kms
        * spark-admin:devices_read
        * spark-admin:workspace_locations_write
        * spark-admin:licenses_read
        * spark-admin:telephony_config_read
        * spark-admin:telephony_config_write
        * spark-admin:devices_write
        * spark-admin:people_read

    More service app details: https://developer.webex.com/docs/service-apps

    Tokens get persisted in room_devices.yml.
"""
import asyncio
import logging
import sys
import time
from argparse import ArgumentParser
from collections import defaultdict
from functools import reduce
from itertools import chain
from os import getenv, getcwd
from os.path import splitext, basename, isfile, join
from typing import Optional

from dotenv import load_dotenv
from yaml import safe_load, safe_dump

from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.common import OwnerType
from wxc_sdk.devices import Device
from wxc_sdk.integration import Integration
from wxc_sdk.locations import Location
from wxc_sdk.telephony import NumberListPhoneNumber
from wxc_sdk.tokens import Tokens
from wxc_sdk.workspace_locations import WorkspaceLocation
from wxc_sdk.workspaces import Workspace, WorkspaceSupportedDevices, CallingType, WorkspaceCalling


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


def main() -> int:
    """
    Main code
    """
    # parse args
    parser = ArgumentParser(prog=basename(__file__), description='CLI tool to manage room device calling entitlements')
    parser.add_argument('operation', choices=['show', 'clear'], help='show: show all room devices with their calling '
                                                                     'settings, clear: remove calling license from '
                                                                     'devices')
    parser.add_argument('--location', type=str, help='work on devices in given location')
    parser.add_argument('--wsnames', type=str, help='file name of a file with workspace names to operate on; '
                                                    'one name per line')
    parser.add_argument('--test', action='store_true', help='test run only')
    args = parser.parse_args()
    operation = args.operation
    test_run = args.test
    location = args.location
    ws_names = args.wsnames

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

    async def as_main() -> int:
        """
        Async main to be able to use concurrency
        """

        async def downgrade_workspace(ws: Workspace):
            """
            Downgrade one workspace to free calling
            """

            def log(s: str, file=sys.stdout):
                print(f'downgrade workspace "{ws.display_name:{ws_name_len}}": {s}', file=file)

            if ws.calling.type != CallingType.webex:
                raise ValueError(f'calling type is "{ws.calling.type}", not "{CallingType.webex.value}"')
            if test_run:
                log('skipping update, test run only')
            else:
                log('updating calling settings')
                update = ws.model_copy(deep=True)
                update.calling = WorkspaceCalling(type=CallingType.free)
                update.workspace_location_id = None
                update.location_id = None
                await api.workspaces.update(workspace_id=ws.workspace_id, settings=update)
            log('done')

        async with AsWebexSimpleApi(tokens=tokens) as api:

            # get list of locations and workspace locations
            ws_location_list, location_list = await asyncio.gather(
                api.workspace_locations.list(display_name=location),
                api.locations.list(name=location))
            location_list: list[Location]
            ws_location_list: list[WorkspaceLocation]

            # validate location argument
            if location:
                target_location = next((loc for loc in location_list if loc.name == location), None)
                target_ws_location = next((loc for loc in ws_location_list if loc.display_name == location), None)
                if not all((target_ws_location, target_location)):
                    print(f'location "{location}" not found', file=sys.stderr)
                    return 1
            else:
                target_location = None
                target_ws_location = None

            # get workspaces, numbers, and devices (in target location)
            workspaces, numbers, devices = await asyncio.gather(
                api.workspaces.list(workspace_location_id=target_ws_location and target_ws_location.id),
                api.telephony.phone_numbers(location_id=target_location and target_location.location_id,
                                            owner_type=OwnerType.place),
                api.devices.list(workspace_location_id=target_ws_location and target_ws_location.id,
                                 product_type='roomdesk')
            )
            workspaces: list[Workspace]
            numbers: list[NumberListPhoneNumber]
            devices: list[Device]

            # only workspaces supporting desk devices
            workspaces = [ws for ws in workspaces
                          if ws.supported_devices == WorkspaceSupportedDevices.collaboration_devices]

            # if a path to a file with workspace names was given, then filter based on the file contents
            if ws_names:
                with open(ws_names, mode='r') as f:
                    workspace_names = set(s_line for line in f if (s_line := line.strip()))
                workspaces = [ws for ws in workspaces
                              if ws.display_name in workspace_names]
            if not workspaces:
                print('No workspaces', file=sys.stderr)
                return 1

            # only devices in workspaces (no personal devices)
            devices = [d for d in devices if d.workspace_id is not None]

            # prepare some lookups
            workspace_locations_by_id: dict[str, WorkspaceLocation] = {wsl.id: wsl for wsl in ws_location_list}
            numbers_by_workspace_uuid: dict[str, list[NumberListPhoneNumber]] = reduce(
                lambda r, el: r[webex_id_to_uuid(el.owner.owner_id)].append(el) or r,
                numbers,
                defaultdict(list))
            devices_by_workspace_id: dict[str, list[Device]] = reduce(
                lambda r, el: r[el.workspace_id].append(el) or r,
                devices,
                defaultdict(list))

            # sort workspaces by workspace location name and workspace name; workspace location can be unset
            workspaces.sort(key=lambda ws: ('' if not ws.workspace_location_id else
                                            workspace_locations_by_id[ws.workspace_location_id].display_name,
                                            ws.display_name))
            # some field lengths for nicer output
            wsl_name_len = max(len(wsl.display_name) for wsl in ws_location_list)
            ws_name_len = max(len(ws.display_name) for ws in workspaces)

            # ... chain([1], ...) to avoid max() on empty sequence
            pn_len = max(chain([1], (len(n.phone_number) for n in numbers if n.phone_number)))
            ext_len = max(chain([1], (len(n.extension) for n in numbers if n.extension)))

            # print workspaces with workspace locations, numbers, and devices
            for workspace in workspaces:
                if not workspace.workspace_location_id:
                    wsl_name = ''
                else:
                    wsl_name = workspace_locations_by_id[workspace.workspace_location_id].display_name
                print(f'workspace location "{wsl_name:{wsl_name_len}}", '
                      f'workspace "{workspace.display_name:{ws_name_len}}"')

                # are there any numbers in that workspace?
                numbers = numbers_by_workspace_uuid.get(webex_id_to_uuid(workspace.workspace_id))
                if numbers:
                    for number in numbers:
                        print(f'  number: {number.phone_number or "-" * pn_len:{pn_len}}/'
                              f'{number.extension or "-" * ext_len:{ext_len}}')
                devices = devices_by_workspace_id.get(workspace.workspace_id)
                if devices:
                    for device in devices:
                        print(f'  device: {device.display_name}')

            if operation == 'show':
                # we are done here
                return 0

            # now we want to downgrade (disable calling) on all workspaces
            print()
            print('Starting downgrade')
            results = await asyncio.gather(*[downgrade_workspace(ws) for ws in workspaces], return_exceptions=True)

            # print errors ... if any
            for ws, result in zip(workspaces, results):
                ws: Workspace
                if isinstance(result, Exception):
                    print(f'Failed to downgrade "{ws.display_name:{ws_name_len}}": {result}', file=sys.stderr)

            if any(isinstance(r, Exception) for r in results):
                return 1
            return 0

    return asyncio.run(as_main())


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

    exit(main())

#!/usr/bin/env python
"""
Get calling users without devices
"""
import asyncio
import logging
import os
from itertools import chain
from typing import Optional

from dotenv import load_dotenv

from wxc_sdk import Tokens
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import UserType
from wxc_sdk.integration import Integration
from wxc_sdk.person_settings import DeviceList
from wxc_sdk.scopes import parse_scopes


def env_path() -> str:
    """
    determine path for .env to load environment variables from; based on name of this file
    :return: .env file path
    """
    return os.path.join(os.getcwd(), f'{os.path.splitext(os.path.basename(__file__))[0]}.env')


def yml_path() -> str:
    """
    determine path of YML file to persist tokens
    :return: path to YML file
    :rtype: str
    """
    return os.path.join(os.getcwd(), f'{os.path.splitext(os.path.basename(__file__))[0]}.yml')


def build_integration() -> Integration:
    """
    read integration parameters from environment variables and create an integration
    :return: :class:`wxc_sdk.integration.Integration` instance
    """
    client_id = os.getenv('INTEGRATION_CLIENT_ID')
    client_secret = os.getenv('INTEGRATION_CLIENT_SECRET')
    scopes = parse_scopes(os.getenv('INTEGRATION_SCOPES'))
    redirect_url = 'http://localhost:6001/redirect'
    if not all((client_id, client_secret, scopes)):
        raise ValueError('failed to get integration parameters from environment')
    return Integration(client_id=client_id, client_secret=client_secret, scopes=scopes,
                       redirect_url=redirect_url)


def get_tokens() -> Optional[Tokens]:
    """
    Tokens are read from a YML file. If needed an OAuth flow is initiated.

    :return: tokens
    :rtype: :class:`wxc_sdk.tokens.Tokens`
    """

    integration = build_integration()
    tokens = integration.get_cached_tokens_from_yml(yml_path=yml_path())
    return tokens


async def main():
    # get environment variables from .env; required for integration parameters
    load_dotenv(env_path())

    # get tokens from cache or create a new set of tokens using the integration defined in .env
    tokens = get_tokens()

    async with AsWebexSimpleApi(tokens=tokens) as api:
        # get calling users
        calling_users = [user for user in await api.people.list(calling_data=True)
                         if user.location_id]

        # get device info for all users
        user_device_infos = await asyncio.gather(*[api.person_settings.devices(person_id=user.person_id)
                                                   for user in calling_users])
        user_device_infos: list[DeviceList]
        users_wo_devices = [user for user, device_info in zip(calling_users, user_device_infos)
                            if not device_info.devices]

        # alternatively we can collect all device owners
        device_owner_ids = set(owner.owner_id
                               for device in chain.from_iterable(udi.devices for udi in user_device_infos)
                               if (owner := device.owner) and owner.owner_type == UserType.people)

        # ... and collect all other users (the ones not owning a device)
        users_not_owning_a_device = [user for user in calling_users
                                     if user.person_id not in device_owner_ids]

    users_wo_devices.sort(key=lambda u: u.display_name)
    print(f'{len(users_wo_devices)} users w/o devices:')
    print('\n'.join(f'{user.display_name} ({user.emails[0]})'
                    for user in users_wo_devices))

    print()
    users_not_owning_a_device.sort(key=lambda u: u.display_name)
    print(f'{len(users_not_owning_a_device)} users not owning a device:')
    print('\n'.join(f'{user.display_name} ({user.emails[0]})'
                    for user in users_not_owning_a_device))


if __name__ == '__main__':
    # enable DEBUG logging to a file; REST log shows all requests
    logging.basicConfig(filename=os.path.join(os.getcwd(), f'{os.path.splitext(os.path.basename(__file__))[0]}.log'),
                        filemode='w', level=logging.DEBUG, format='%(asctime)s %(threadName)s %(message)s')
    asyncio.run(main())

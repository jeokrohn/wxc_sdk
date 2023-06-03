#!/usr/bin/env python
"""
This script looks for unassigned TNs and assigns them to HGs that are forwarded to the locations main number.
The idea is to catch all incoming calls to unassigned TNs and handle them accordingly

    usage: catch_tns.py [-h] [--test] [--location LOCATION] [--token TOKEN]
                        [--cleanup]

    optional arguments:
      -h, --help           show this help message and exit
      --test               test only; don't actually apply any config
      --location LOCATION  Location to work on
      --token TOKEN        admin access token to use.
      --cleanup            remove all pooling HGs
"""
import asyncio
import logging
import os
import sys
from argparse import ArgumentParser, Namespace
from collections import defaultdict
from operator import attrgetter
from typing import Optional, Union

from dotenv import load_dotenv

from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import IdAndName, AlternateNumber, RingPattern
from wxc_sdk.integration import Integration
from wxc_sdk.scopes import parse_scopes
from wxc_sdk.telephony import NumberListPhoneNumber
from wxc_sdk.telephony.forwarding import CallForwarding
from wxc_sdk.telephony.huntgroup import HuntGroup
from wxc_sdk.tokens import Tokens

POOL_HG_NAME = 'POOL_'


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


async def location_id_from_args(api: AsWebexSimpleApi, args: Namespace) -> Optional[str]:
    """
    Get location id for --location parameter
    """
    if not args.location:
        return None
    location = next((loc
                     for loc in await api.locations.list(name=args.location)
                     if loc.name == args.location),
                    None)
    return location and location.location_id


async def cleanup(api: AsWebexSimpleApi, args: Namespace):
    """
    clean up (delete) pooling HGs
    """
    location_id = await location_id_from_args(api, args)
    existing_hg_list = [hg for hg in await api.telephony.huntgroup.list(location_id=location_id)
                        if hg.name.startswith(POOL_HG_NAME)]

    async def delete_one(hg: HuntGroup):
        if not args.test:
            await api.telephony.huntgroup.delete_huntgroup(location_id=hg.location_id,
                                                           huntgroup_id=hg.id)
        print(f'Deleted HG "{hg.name}" in location "{hg.location_name}"')

    await asyncio.gather(*[delete_one(hg)
                           for hg in existing_hg_list])


async def pool_tns_location(api: AsWebexSimpleApi, args: Namespace, location: IdAndName,
                            tns: list[NumberListPhoneNumber]):
    """
    Pool unassigned TNs for a given location
    """

    async def add_to_hg(hg: Union[HuntGroup, str],
                        tns: list[NumberListPhoneNumber]):
        """
        Add a bunch of TNs to given HG
        :param hg: can be an existing HG or a name of a HG to be created
        :param tns: list of TNs to be added to the HG
        """
        if isinstance(hg, str):
            # create new HG
            print(f'Creating HG "{hg}" in location "{location.name}" for: '
                  f'{", ".join(tn.phone_number for tn in tns)}')
            if args.test:
                return
            settings = HuntGroup.create(name=hg,
                                        phone_number=tns[0].phone_number)
            new_id = await api.telephony.huntgroup.create(location_id=location.id,
                                                          settings=settings)
            # Get details of new HG and also the forwarding settings
            # * details are needed for the recursive call to add_to_hg .. in case we have more than one TN to add
            # * ... and forwarding settings are needed b/c we want to set CFwdAll to location's main number
            details, forwarding = await asyncio.gather(
                api.telephony.huntgroup.details(location_id=location.id, huntgroup_id=new_id),
                api.telephony.huntgroup.forwarding.settings(location_id=location.id, feature_id=new_id))
            forwarding: CallForwarding
            details: HuntGroup

            # set call forwarding
            print(f'HG "{hg}" in location "{location.name}": set CFwdAll to {main_number}')
            forwarding.always.enabled = True
            forwarding.always.destination = main_number
            await api.telephony.huntgroup.forwarding.update(location_id=location.id, feature_id=new_id,
                                                            forwarding=forwarding)
            if len(tns) > 1:
                # add the remaining as alternate numbers
                await add_to_hg(hg=details, tns=tns[1:])
            return

        # add tns as alternate numbers
        print(f'HG "{hg.name}" in location "{location.name}", adding: '
              f'{", ".join(tn.phone_number for tn in tns)}')
        if args.test:
            return
        # weirdly on GET alternate numbers are returned in alternate_number_settings ...
        alternate_numbers = hg.alternate_number_settings.alternate_numbers
        alternate_numbers.extend(AlternateNumber(phone_number=tn.phone_number,
                                                 ring_pattern=RingPattern.normal)
                                 for tn in tns)
        # ... while for an update Wx expects the alternate numbers in an alternate_number attribute
        update = HuntGroup(alternate_numbers=alternate_numbers)
        await api.telephony.huntgroup.update(location_id=location.id,
                                             huntgroup_id=hg.id,
                                             update=update)

        return

    # if the list of available TNs includes the main number then something is wonky. The main number should be owned
    # by something
    main_number = next((tn for tn in tns if tn.main_number), None)
    if main_number is not None:
        print(f'Error: main number {main_number.phone_number} in location "{location.name}" is not assigned to '
              f'anything!', file=sys.stderr)
        return

    # get main number of location
    main_number = (await api.telephony.location.details(location_id=location.id)).calling_line_id.phone_number

    # get list if "pool" HGs in location
    existing_hg_list = [hg for hg in await api.telephony.huntgroup.list(location_id=location.id)
                        if hg.name.startswith(POOL_HG_NAME)]

    # we need the details for all HGs: list() response is missing the alternate number list
    # get all HG details in parallel
    existing_hg_list = await asyncio.gather(*[api.telephony.huntgroup.details(location_id=location.id,
                                                                              huntgroup_id=hg.id)
                                              for hg in existing_hg_list])
    existing_hg_list: list[HuntGroup]

    # start with an empty list of tasks
    tasks = []

    # assign TNs to existing "pool" HGs

    # these are the HGs we can still assign some TNs to
    hgs_with_open_slots = (hg
                           for hg in existing_hg_list
                           if len(hg.alternate_number_settings.alternate_numbers) < 10)
    tns.sort(key=attrgetter('phone_number'))
    while tns:
        hg_with_open_slots = next(hgs_with_open_slots, None)
        if hg_with_open_slots is None:
            # no more HGs we can assign TNs to --> we are done here
            break

        # add some tns to this hg; hg can have max 10 alternate numbers
        tns_to_add = 10 - len(hg_with_open_slots.alternate_number_settings.alternate_numbers)
        tasks.append(add_to_hg(hg=hg_with_open_slots, tns=tns[:tns_to_add]))

        # continue w/ remaining TNs
        tns = tns[tns_to_add:]

    # assign remaining TNs to new "pool" HGs
    # .. in batches of 11
    existing_names = set(hg.name for hg in existing_hg_list)
    new_hg_names = (name
                    for i in range(1, 1000)
                    if (name := f'{POOL_HG_NAME}{i:03d}') not in existing_names)
    while tns:
        tasks.append(add_to_hg(hg=next(new_hg_names), tns=tns[:11]))
        tns = tns[11:]

    # Now run all tasks
    await asyncio.gather(*tasks)
    return


async def pool_tns(api: AsWebexSimpleApi, args: Namespace):
    """
    Assign unassigned numbers to pool HGs
    """
    location_id = await location_id_from_args(api, args)

    # get available TNs. If a location argument was present then limit to that location
    numbers = await api.telephony.phone_numbers(available=True, location_id=location_id)

    # we need to work on TNs by location ...
    tns_by_location: dict[str, list[NumberListPhoneNumber]] = defaultdict(list)
    # ... and we want to collect location information (specifically the name)
    locations: dict[str, IdAndName] = dict()
    for tn in numbers:
        locations[tn.location.id] = tn.location
        tns_by_location[tn.location.id].append(tn)

    # work on all locations in parallel
    await asyncio.gather(*[pool_tns_location(api=api, args=args,
                                             location=locations[location_id], tns=tns)
                           for location_id, tns in tns_by_location.items()])


async def catch_tns():
    """
    Main async logic
    """
    parser = ArgumentParser()
    parser.add_argument('--test', required=False, help='test only; don\'t actually apply any config',
                        action='store_true')
    parser.add_argument('--location', required=False, help='Location to work on', type=str)
    parser.add_argument('--token', type=str, required=False, help='admin access token to use.')
    parser.add_argument('--cleanup', required=False, help='remove all pooling HGs', action='store_true')
    args = parser.parse_args()

    load_dotenv(env_path())

    tokens = args.token or None

    if tokens is None:
        # get tokens from cache or create a new set of tokens using the integration defined in .env
        tokens = get_tokens()
    async with AsWebexSimpleApi(tokens=tokens) as api:
        if args.cleanup:
            await cleanup(api, args)
        else:
            await pool_tns(api, args)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(catch_tns())

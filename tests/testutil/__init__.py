"""
Generic helper for test cases
"""
import asyncio
import os
import random
from collections import defaultdict
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import date
from functools import reduce
from itertools import zip_longest, chain
from operator import attrgetter
from random import randint
from typing import Generator, Optional, Union, Literal

from test_helper.digittree import DigitTree
from test_helper.randomlocation import RandomLocation, Address
from test_helper.randomuser import User
from test_helper.randomuserutil import RandomUserUtil

from examples.calendarific import CalendarifiyApi
from wxc_sdk import WebexSimpleApi
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import NumberState
from wxc_sdk.common.schedules import ScheduleType, Schedule, Event
from wxc_sdk.licenses import LicenseRequest, LicenseProperties, License
from wxc_sdk.locations import Location
from wxc_sdk.people import Person
from wxc_sdk.rest import RestError
from wxc_sdk.telephony import NumberType, NumberListPhoneNumber

__all__ = ['as_available_tns', 'available_tns', 'available_extensions', 'LocationInfo', 'us_location_info',
           'calling_users', 'available_numbers', 'available_extensions_gen', 'get_or_create_holiday_schedule',
           'get_or_create_business_schedule', 'random_users', 'create_call_park_extension',
           'as_available_extensions_gen', 'create_random_wsl', 'available_mac_address', 'new_workspace_names',
           'TEST_WORKSPACES_PREFIX', 'create_workspace_with_webex_calling', 'get_calling_license',
           'create_calling_user', 'create_random_calling_user']

from wxc_sdk.telephony.devices import MACState
from wxc_sdk.telephony.location import TelephonyLocation

from wxc_sdk.workspace_locations import WorkspaceLocation
from wxc_sdk.workspaces import Workspace, WorkspaceCalling, CallingType, WorkspaceWebexCalling, \
    WorkspaceSupportedDevices


def available_numbers(numbers: Iterable[str], seed: str = None) -> Generator[str, None, None]:
    """

    :param numbers:
    :param seed:
    :return:
    """
    # group numbers by len
    by_len: dict[int, list[str]] = reduce(lambda red, pn: red[len(pn)].append(pn) or red,
                                          numbers, defaultdict(list))
    if by_len:
        ext_len = max(by_len)
        numbers = by_len[ext_len]
        seed = numbers[0]
    else:
        numbers = []
        seed = seed or str(randint(1, 9) * 1000)
    tree = DigitTree.from_list(nodes=numbers)
    return tree.available(seed=seed)


async def as_available_tns(*, as_api: AsWebexSimpleApi, tn_prefix: str, tns_requested: int = 1) -> list[str]:
    """
    Get some available US TNs
    :param as_api:
    :param tn_prefix: prefix for TNs to find. Can be +E.164 or 1st few digits of 10D. If an NPA is passed as 3D or
        +1-3D then numbers in the +1 NXX 555 01XX range are searched
    :param tns_requested: number of TNs to find
    :return:
    """

    # convert prefix to +E.164 prefix
    if not tn_prefix.startswith('+'):
        tn_prefix = f'+1{tn_prefix}'
    if len(tn_prefix) == 5:
        # we only got an NPA make sure to only look at NXX 555 01XX
        tn_prefix = f'{tn_prefix}55501'
    digits_to_fill = 12 - len(tn_prefix)
    numbers_to_scan = 10 ** digits_to_fill

    # generator for numbers to scan for availability
    scan = (f'{tn_prefix}{i:0{digits_to_fill}}' for i in range(1, numbers_to_scan))
    tns = []

    # the check for availability should operate on batches of at least 5 TNs
    # last batch is filled with None at the end
    batches = zip_longest(*([scan] * max(5, tns_requested)), fillvalue=None)
    for batch in batches:
        # ignore the fill values (in the last batch)
        batch = [number for number in batch if number]
        validation = await as_api.telephony.validate_phone_numbers(phone_numbers=batch)
        if validation.ok:
            # all numbers are available
            failed = set()
        else:
            # get set of numbers which are not available for provisioning
            failed = set(result.phone_number for result in validation.phone_numbers
                         if not result.ok)
        # add available numbers in batch to list of TNs
        tns.extend(number for number in batch if number not in failed)
        if len(tns) >= tns_requested:
            # we are done
            break
    # don't return more TNs than requested
    return tns[:tns_requested]


def available_tns(*, api: WebexSimpleApi, tn_prefix: str, tns_requested: int = 1) -> list[str]:
    """
    Get some available US TNs
    :param api:
    :param tn_prefix: prefix for TNs to find. Can be +E.164 or 1st few digits of 10D. If an NPA is passed as 3D or
        +1-3D then numbers in the +1 NXX 555 01XX range are searched
    :param tns_requested: number of TNs to find
    :return:
    """

    async def as_run():
        async with AsWebexSimpleApi(tokens=api.access_token) as as_api:
            result = await as_available_tns(as_api=as_api, tn_prefix=tn_prefix, tns_requested=tns_requested)
        return result

    return asyncio.run(as_run())


def available_extensions_gen(*, api: WebexSimpleApi, location_id: str, seed: str = None) -> Generator[str, None, None]:
    extensions = [pn.extension for pn in api.telephony.phone_numbers(location_id=location_id)
                  if pn.extension]
    extensions.extend(cpe.extension for cpe in api.telephony.callpark_extension.list(location_id=location_id))
    return available_numbers(numbers=extensions, seed=seed)


async def as_available_extensions_gen(*, api: AsWebexSimpleApi,
                                      location_id: str, seed: str = None) -> Generator[str, None, None]:
    phone_numbers, cpe_list = await asyncio.gather(api.telephony.phone_numbers(location_id=location_id),
                                                   api.telephony.callpark_extension.list(location_id=location_id))
    extensions = [pn.extension for pn in phone_numbers
                  if pn.extension]
    extensions.extend(cpe.extension for cpe in cpe_list)
    return available_numbers(numbers=extensions, seed=seed)


def available_extensions(*, api: WebexSimpleApi, location_id: str, ext_requested: int = 1,
                         seed: str = None) -> list[str]:
    """
    Get some available extensions in given location
    :param api:
    :param location_id:
    :param ext_requested:
    :param seed:
    :return: list of extensions
    """
    result = [next(available_extensions_gen(api=api, location_id=location_id, seed=seed)) for _ in range(ext_requested)]
    return result


@dataclass
class LocationInfo:
    location: Location
    tel_location: TelephonyLocation
    main_number: str
    numbers: list[NumberListPhoneNumber]

    def available_tns(self, *, api: WebexSimpleApi, tns_requested: int = 1) -> list[str]:
        return available_tns(api=api, tn_prefix=self.main_number[:5], tns_requested=tns_requested)


def us_location_info(*, api: WebexSimpleApi) -> list[LocationInfo]:
    """
    Get information about US location with numbers
    :param api:
    """
    us_locations = [loc for loc in api.locations.list()
                    if loc.address.country == 'US']

    def safe_tel_location_details(location_id: str)->Optional[TelephonyLocation]:
        try:
            return api.telephony.location.details(location_id)
        except RestError:
            return None
    with ThreadPoolExecutor() as pool:
        tel_locations = list(pool.map(safe_tel_location_details, (loc.location_id for loc in us_locations)))

    # only consider locations with telephony
    us_locations, tel_locations = zip(*((loc, tel_loc) for loc, tel_loc in zip(us_locations, tel_locations)
                                        if tel_loc))
    numbers = list(api.telephony.phone_numbers(number_type=NumberType.number))
    # group numbers by location id
    numbers_by_location: dict[str, list[NumberListPhoneNumber]] = defaultdict(list)
    for number in numbers:
        numbers_by_location[number.location.id].append(number)
    # collect results
    result = []
    for loc, tel_loc in zip(us_locations, tel_locations):
        # get numbers for this location; maybe there are none
        loc_numbers = numbers_by_location.get(loc.location_id)
        if loc_numbers is None:
            # skip locations w/o numbers
            continue

        # determine main number of location
        main_number = next((n for n in loc_numbers
                            if n.main_number), None)
        if not main_number:
            # skip locations w/o main number
            continue
        result.append(LocationInfo(location=loc, tel_location=tel_loc, main_number=main_number.phone_number,
                                   numbers=loc_numbers))
    return result


def calling_users(*, api: WebexSimpleApi) -> list[Person]:
    """
    Get a list of all calling users
    :param api:
    :return: list of users
    """

    calling_license_ids = set(lic.license_id for lic in api.licenses.list()
                              if lic.webex_calling)
    # user is a calling user if any of the user's licenses is a calling license
    users = [user for user in api.people.list()
             if any(license_id in calling_license_ids for license_id in user.licenses)]
    return users


def get_calling_license(*, api: WebexSimpleApi, prefer_basic: bool = True) -> Optional[str]:
    """
    Get id of available calling license
    """
    licenses = [lic for lic in api.licenses.list() if lic.webex_calling and not lic.webex_calling_workspaces]
    licenses.sort(key=attrgetter('webex_calling_professional'), reverse=not prefer_basic)
    licence = next((lic for lic in licenses
                    if lic.consumed_units < lic.total_units), None)
    return licence and licence.license_id


def get_or_create_holiday_schedule(*, api: WebexSimpleApi, location_id: str) -> Schedule:
    """
    Create a holiday schedule in given location
    :param api:
    :param location_id:
    :return:
    """
    schedules = list(api.telephony.schedules.list(obj_id=location_id, schedule_type=ScheduleType.holidays))
    if schedules:
        return random.choice(schedules)
    # create a new schedule
    this_year = date.today().year

    events = []
    for year in (this_year, this_year + 1):
        # get national holidays for specified year
        holidays = CalendarifiyApi().holidays(country='US', year=year, holiday_type='national')
        today = date.today()
        events.extend((Event(name=f'{holiday.name} {holiday.date.year}',
                             start_date=holiday.date,
                             end_date=holiday.date,
                             all_day_enabled=True)
                       for holiday in holidays
                       if holiday.date >= today and holiday.date.weekday() != 6))
    schedule = Schedule(name='National Holidays',
                        schedule_type=ScheduleType.holidays,
                        events=events)
    schedule_id = api.telephony.schedules.create(obj_id=location_id, schedule=schedule)
    return api.telephony.schedules.details(obj_id=location_id, schedule_type=ScheduleType.holidays,
                                           schedule_id=schedule_id)


def get_or_create_business_schedule(*, api: WebexSimpleApi, location_id: str) -> Schedule:
    """
    Create a business schedule in given location
    :param api:
    :param location_id:
    :return:
    """
    schedules = list(api.telephony.schedules.list(obj_id=location_id, schedule_type=ScheduleType.business_hours))
    if schedules:
        return random.choice(schedules)
    # create a new schedule
    schedule = Schedule.business(name='Business hours')
    schedule_id = api.telephony.schedules.create(obj_id=location_id, schedule=schedule)
    return api.telephony.schedules.details(obj_id=location_id, schedule_type=ScheduleType.business_hours,
                                           schedule_id=schedule_id)


Inc = Literal[
    'gender', 'name', 'location', 'email', 'login', 'registered', 'dob', 'phone', 'cell', 'id', 'picture', 'nat']


async def random_users(api: AsWebexSimpleApi, user_count: int = 1, inc: Union[Inc, list[Inc]] = 'name') -> list[User]:
    """
    Get a bunch of random new users
    :param api:
    :param user_count:
    :param inc:
    :return:
    """
    email = os.getenv('BASE_EMAIL')
    if email is None:
        raise KeyError('BASE_EMAIL needs to be defined')
    util = RandomUserUtil(api=api, gmail_address=email)
    new_users = await util.get_new_users(number_of_users=user_count, inc=inc)
    return new_users


def create_call_park_extension(*, api: WebexSimpleApi, location_id: str) -> str:
    """
    Create a new call park extension in given location
    :param api:
    :param location_id:
    :return: if of call park extension
    """
    cp = api.telephony.callpark_extension

    # get name for new CPE
    cpes = list(cp.list(location_id=location_id))
    new_names = (name for i in range(1000)
                 if (name := f'CPE {i:03d}') not in set(cpe.name for cpe in cpes))
    new_name = next(new_names)

    # we need an available extension in that location
    extension = next(available_extensions_gen(api=api, location_id=location_id))

    cpe_id = cp.create(location_id=location_id, name=new_name, extension=extension)
    return cpe_id


def create_random_wsl(api: WebexSimpleApi) -> WorkspaceLocation:
    """
    create a random workspace location
    """

    def random_address() -> Address:
        """
        Get a random address in the US
        """

        async def as_random_address() -> Address:
            """
            Get a random address in the US
            """
            async with RandomLocation() as rl:
                return await rl.random_address()

        return asyncio.run(as_random_address())

    # we should not create workspace locations anymore
    raise NotImplementedError()
    address = random_address()

    # get a unique display name
    display_name_prefix = f'{address.city}, {address.address1}'
    wsl_list = api.workspace_locations.list()
    display_names = set(wsl.display_name for wsl in wsl_list)
    display_name = next(dpn
                        for suffix in chain([''],
                                            (f'_{i:02}'
                                             for i in range(1, 99)))
                        if (dpn := f'{display_name_prefix}{suffix}') not in display_names)

    wsl = api.workspace_locations.create(display_name=display_name, address=str(address),
                                         country_code='US', longitude=address.geo_location.lon,
                                         latitude=address.geo_location.lat, city_name=address.city)
    return wsl


def available_mac_address(*, api: WebexSimpleApi) -> Generator[str, None, None]:
    mac_prefix = 'DEADDEAD'

    def mac_candidates() -> Generator[str, None, None]:
        for v in range(10, 65536):
            yield f'{mac_prefix}{hex(v)[2:].zfill(4).upper()}'

    # test macs in batches of 10
    batch_args = [mac_candidates()] * 10
    batches = zip_longest(*batch_args)
    for batch in batches:
        validation_result = api.telephony.devices.validate_macs(macs=list(batch))
        errored_macs = set(ms.mac
                           for ms in (validation_result.mac_status or [])
                           if ms.state != MACState.available)
        yield from (mac for mac in batch if mac not in errored_macs)


TEST_WORKSPACES_PREFIX = 'workspace test '


def new_workspace_names(api: WebexSimpleApi) -> Generator[str, None, None]:
    ws_list = list(api.workspaces.list())
    ws_names = set(w.display_name for w in ws_list)
    new_gen = (name for i in range(1000)
               if (name := f'{TEST_WORKSPACES_PREFIX}{i:03}') not in ws_names)
    return new_gen


def create_workspace_with_webex_calling(api: WebexSimpleApi, target_location: Location,
                                        supported_devices: WorkspaceSupportedDevices,
                                        license: License = None,
                                        **kwargs) -> Workspace:
    """
    create a workspace with webex calling in given location
    """
    # get an extension in location
    extension = next(available_extensions_gen(api=api,
                                              location_id=target_location.location_id))

    # get a name for new workspace
    name = next(new_workspace_names(api=api))

    # create workspace with that extension
    webex_calling = WorkspaceWebexCalling(
        extension=extension,
        location_id=target_location.location_id)
    if license is not None:
        webex_calling.licenses = [license.license_id]
    new_workspace = Workspace(
        display_name=name,
        calling=WorkspaceCalling(
            type=CallingType.webex,
            webex_calling=webex_calling),
        supported_devices=supported_devices, **kwargs)
    workspace = api.workspaces.create(settings=new_workspace)
    return workspace


def create_calling_user(api: WebexSimpleApi, user: User, location_id: str, calling_license_id: str,
                        extension: str = None, phone_number: str = None) -> Person:
    """
    Create a calling enabled user

    :param api:
    :param user:
    :param location_id:
    :param extension:
    :param phone_number:
    :param calling_license_id:
    :return:
    """
    if not any((extension, phone_number)):
        raise ValueError('extension or phone_number required')
    # create user
    new_user = api.people.create(
        settings=Person(emails=[user.email],
                        display_name=user.display_name,
                        first_name=user.name.first,
                        last_name=user.name.last))

    api.licenses.assign_licenses_to_users(
        person_id=new_user.person_id,
        licenses=[LicenseRequest(id=calling_license_id,
                                 properties=LicenseProperties(location_id=location_id,
                                                              extension=extension,
                                                              phone_number=phone_number))])
    new_user = api.people.details(person_id=new_user.person_id, calling_data=True)
    return new_user


def create_random_calling_user(api: WebexSimpleApi, location_id: str, calling_license_id: str = None,
                               with_tn: bool = False) -> Person:
    """
    create a random calling users in given location
    :param api:
    :param location_id:
    :param calling_license_id:
    :param with_tn:
    :return:
    """

    async def get_random_user() -> User:
        async with AsWebexSimpleApi(tokens=api.access_token) as as_api:
            users = await random_users(api=as_api)
        return users[0]
    random_user = asyncio.run(get_random_user())

    if with_tn:
        # figure out the NPA for phone numbers in target location
        existing_tns = api.telephony.phone_numbers(location_id=location_id,
                                                   number_type=NumberType.number)

        # take the NPA from the 1st phone number
        npa = next((n.phone_number[2:5] for n in existing_tns), None)
        if npa is None:
            raise ValueError('Could not determine NPA for given location)')

        phone_number = (available_tns(api=api, tn_prefix=npa))[0]
        # add phone number to location
        api.telephony.location.number.add(location_id=location_id,
                                          phone_numbers=[phone_number],
                                          state=NumberState.active)
    else:
        phone_number = None
    extension = available_extensions(api=api, location_id=location_id)[0]
    if calling_license_id is None:
        calling_licenses = [lic for lic in api.licenses.list() if
                            lic.webex_calling_basic or lic.webex_calling_professional]
        calling_licenses.sort(key=attrgetter('name'), reverse=True)

        calling_license = next((lic for lic in calling_licenses
                                if lic.consumed_units < lic.total_units), None)
        calling_license_id = calling_license.license_id
    return create_calling_user(api=api, user=random_user, location_id=location_id,
                               calling_license_id=calling_license_id, extension=extension,
                               phone_number=phone_number)

import asyncio
from base64 import b64decode
from contextlib import asynccontextmanager
from dataclasses import dataclass
from itertools import chain
from json import dumps, loads
from random import choice
from typing import ClassVar
from unittest import skip

from randomlocation import RandomLocation, NpaInfo, Address

from wxc_sdk.as_rest import AsRestError
from wxc_sdk.common import RouteType, RouteIdentity
from wxc_sdk.locations import Location, LocationAddress
from wxc_sdk.telephony import NumberType, NumberListPhoneNumber
from wxc_sdk.telephony.location import TelephonyLocation, PSTNConnection, CallingLineId
from wxc_sdk.telephony.location.internal_dialing import InternalDialing
from wxc_sdk.telephony.prem_pstn.route_group import RouteGroup
from wxc_sdk.telephony.prem_pstn.trunk import Trunk
from .base import TestCaseWithLog, async_test
from .testutil import as_available_tns


class TestLocation(TestCaseWithLog):

    def test_001_list_all(self):
        """
        list all locations
        """
        location_list = list(self.api.locations.list())
        print(f'Got {len(location_list)} locations')

    @async_test
    async def test_002_details(self):
        """
        get details for all locations
        """
        locations = await self.async_api.locations.list()
        # get location details and telephony details for each location
        details, telephony_details = await asyncio.gather(
            asyncio.gather(*[self.async_api.locations.details(location_id=location.location_id)
                             for location in locations]),
            asyncio.gather(*[self.async_api.telephony.location.details(location_id=loc.location_id)
                             for loc in locations]))
        print(f'Got details for {len(locations)} locations')

    @async_test
    async def test_003_create_location(self):
        """
        create a location with
        * premises PSTN
        * main number (inactive)
        * ...
        """

        async with RandomLocation() as random_location:
            # get
            # * locations
            # * phone numbers in org
            # * list of trunks
            # * list of route groups
            # * list of NPAs
            with self.no_log():
                locations, phone_numbers, trunks, route_groups, npa_data = await asyncio.gather(
                    self.async_api.locations.list(),
                    self.async_api.telephony.phone_numbers(number_type=NumberType.number),
                    self.async_api.telephony.prem_pstn.trunk.list(),
                    self.async_api.telephony.prem_pstn.route_group.list(),
                    random_location.load_npa_data())
                locations: list[Location]
                phone_numbers: list[NumberListPhoneNumber]
                trunks: list[Trunk]
                route_groups: list[RouteGroup]
                npa_data: list[NpaInfo]

                # determine routing prefixes
                # noinspection PyTypeChecker
                location_details = await asyncio.gather(
                    *[self.async_api.telephony.location.details(location_id=loc.location_id)
                      for loc in locations])
                location_details: list[TelephonyLocation]
                routing_prefixes = set(ld.routing_prefix for ld in location_details
                                       if ld.routing_prefix)

            # active NPAs in US
            us_npa_list = [npa.npa for npa in npa_data
                           if npa.country == 'US' and npa.in_service]

            # NPAs used in existing phone numbers
            used_npa_list = set(number.phone_number[2:5] for number in phone_numbers
                                if number.phone_number.startswith('+1'))

            # active NPAs not currently in use
            available_npa_list = [npa for npa in us_npa_list
                                  if npa not in used_npa_list]

            # pick a random NPA and get an address and an available number in that NPA
            with self.no_log():
                address = None
                while address is None:
                    npa = choice(available_npa_list)
                    address, tn_list = await asyncio.gather(random_location.npa_random_address(npa=npa),
                                                            as_available_tns(as_api=self.async_api, tn_prefix=npa))
            address: Address
            tn_list: list[str]
            tn = tn_list[0]

        # get name for location
        location_names = set(loc.name for loc in locations)
        # name like {city} {npa}-dd (suffix only present if there is already a location with that name
        location_name = next(name for suffix in chain([''], (f'-{i:02}' for i in range(1, 100)))
                             if (name := f'{address.city} {npa}{suffix}') not in location_names)
        print(f'Creating location: {npa=}, {npa=}, {address=}')

        location_id = await self.async_api.locations.create(name=location_name,
                                                            time_zone='America/Los_Angeles',
                                                            announcement_language='en_us',
                                                            preferred_language='en_us',
                                                            address1=address.address1,
                                                            city=address.city,
                                                            state=address.state_or_province_abbr,
                                                            postal_code=address.zip_or_postal_code,
                                                            country='US')
        print(f'New location id: {location_id}/{b64decode(location_id + "==").decode()}')

        # add trunk
        trunk_name = next(name for suffix in chain([''], (f'-{i:02}'
                                                          for i in range(1, 100)))
                          if (name := f'{address.city}{suffix}') not in set(trunk.name for trunk in trunks))
        password = await self.async_api.telephony.location.generate_password(location_id=location_id)
        print(f'Creating trunk "{trunk_name}" in location "{location_name}"')
        trunk_id = await self.async_api.telephony.prem_pstn.trunk.create(name=trunk_name,
                                                                         location_id=location_id,
                                                                         password=password)

        # set PSTN choice for location to trunk
        print(f'Setting new trunk "{trunk_name}" as PSTN choice for location "{location_name}"')
        await self.async_api.telephony.location.update(location_id=location_id,
                                                       settings=TelephonyLocation(
                                                           connection=PSTNConnection(type=RouteType.trunk,
                                                                                     id=trunk_id)))

        # add number to location
        await self.async_api.telephony.location.number.add(location_id=location_id, phone_numbers=[tn])

        # finally set that number as main number and set site code
        # also enable unknown extension dialing to the trunk we just defined
        routing_prefix = next(prefix for i in chain([int(npa)], range(1, 1000))
                              if (prefix := f'8{i:03}') not in routing_prefixes)
        await asyncio.gather(
            self.async_api.telephony.location.update(location_id=location_id,
                                                     settings=TelephonyLocation(
                                                         calling_line_id=CallingLineId(
                                                             phone_number=tn),
                                                         routing_prefix=routing_prefix,
                                                         outside_dial_digit='9',
                                                         external_caller_id_name=address.city)),
            self.async_api.telephony.location.internal_dialing.update(
                location_id=location_id,
                update=InternalDialing(
                    enable_unknown_extension_route_policy=True,
                    unknown_extension_route_identity=RouteIdentity(
                        route_id=trunk_id,
                        route_type=RouteType.trunk))))

        # get location details
        location_details, telephony_details = await asyncio.gather(
            self.async_api.locations.details(location_id=location_id),
            self.async_api.telephony.location.details(location_id=location_id)
        )
        location_details: Location
        telephony_details: TelephonyLocation
        print('--------------- Location details ---------------')
        print(dumps(loads(location_details.json()), indent=2))
        print('--------------- Location telephony details ---------------')
        print(dumps(loads(telephony_details.json()), indent=2))


@dataclass(init=False)
class TestUpdate(TestCaseWithLog):
    """
    Tests updating locations
    """
    locations: ClassVar[list[Location]] = None

    @asynccontextmanager
    async def target_location(self) -> Location:
        if self.locations is None:
            with self.no_log():
                locations = await self.async_api.locations.list()
                self.__class__.locations = locations
        target = choice(self.locations)
        details = await self.async_api.locations.details(location_id=target.location_id)
        try:
            yield target.copy(deep=True)
        finally:
            await self.async_api.locations.update(location_id=target.location_id,
                                                  settings=target)
            restored = await self.async_api.locations.details(location_id=target.location_id)
            self.assertEqual(details, restored)

    async def update_and_verify(self, *, target: Location, update: Location, expected: Location):
        """
        Apply an update to a location and verify expected result
        :param target:
        :param update:
        :param expected:
        """
        await self.async_api.locations.update(location_id=target.location_id, settings=update)
        after = await self.async_api.locations.details(location_id=target.location_id)
        self.assertEqual(expected, after)

    @async_test
    async def test_001_update_name(self):
        async with self.target_location() as target:
            target: Location
            new_name = f'{target.name}XYZ'
            update = Location(name=new_name)
            expected = target.copy(deep=True)
            expected.name = new_name
            await self.update_and_verify(target=target, update=update, expected=expected)

    @async_test
    async def test_002_update_timezone(self):
        async with self.target_location() as target:
            target: Location
            new_zone = 'America/New_York' if target.time_zone == 'America/Los_Angeles' else 'America/Los_Angeles'
            update = Location(time_zone=new_zone)
            expected = target.copy(deep=True)
            expected.time_zone = new_zone
            await self.update_and_verify(target=target, update=update, expected=expected)

    @async_test
    async def test_003_update_address2(self):
        """
        Change address line 2
        """
        async with self.target_location() as target:
            target: Location
            address2 = 'whatever'
            update = Location(address=LocationAddress(address1=target.address.address1,
                                                      city=target.address.city,
                                                      address2=address2,
                                                      postal_code=target.address.postal_code,
                                                      state=target.address.state))
            expected = target.copy(deep=True)
            expected.address.address2 = address2
            await self.update_and_verify(target=target, update=update, expected=expected)

    @async_test
    async def test_004_clear_whatever(self):
        """
        Clean up location that have a left-over in address2
        """
        with self.no_log():
            locations = await self.async_api.locations.list()

        locations: list[Location]
        targets = [loc for loc in locations
                   if loc.address.address2 == 'whatever']
        if not targets:
            return
        await asyncio.gather(*[self.async_api.locations.update(location_id=loc.location_id,
                                                               settings=Location(
                                                                   address=LocationAddress(
                                                                       address1=loc.address.address1,
                                                                       address2=None,
                                                                       city=loc.address.city,
                                                                       state=loc.address.state,
                                                                       postal_code=loc.address.postal_code)))
                               for loc in targets])


@skip('Not an actual test')
class ClearAddress2(TestCaseWithLog):
    @async_test
    async def test_clear_address2(self):
        targets = [loc for loc in await self.async_api.locations.list()
                   if loc.address.address2 is not None]

        async def clear_address2(location: Location):
            address = location.address.copy(deep=True)
            address.address2 = None
            await self.async_api.locations.update(location_id=location.location_id,
                                                  settings=Location(address=address))

        await asyncio.gather(*[clear_address2(loc) for loc in targets])


@dataclass(init=False)
class TestUpdateTelephony(TestCaseWithLog):
    """
    Tests updating location telephony settings
    """
    locations: ClassVar[list[TelephonyLocation]] = None

    @asynccontextmanager
    async def target_location(self) -> TelephonyLocation:
        """
        Get a target location for tests
        """
        if self.locations is None:
            with self.no_log():
                locations = await self.async_api.locations.list()
                us_locations = [loc for loc in locations
                                if loc.address.country == 'US']
                if not us_locations:
                    self.skipTest('Need some US locations to run test')
                details = await asyncio.gather(*[self.async_api.telephony.location.details(location_id=loc.location_id)
                                                 for loc in us_locations])
                self.__class__.locations = details
        target = choice(self.locations)
        details = await self.async_api.telephony.location.details(location_id=target.location_id)
        try:
            yield details.copy(deep=True)
        finally:
            # restore old settings.
            # but don't try to update the PSTN settings again
            restore = details.copy(deep=True)
            restore.connection = None
            await self.async_api.telephony.location.update(location_id=target.location_id,
                                                           settings=restore)
            restored = await self.async_api.telephony.location.details(location_id=target.location_id)
            self.assertEqual(details, restored)

    async def update_and_verify(self, *, target: TelephonyLocation, update: TelephonyLocation,
                                expected: TelephonyLocation):
        """
        Apply an update to a location and verify expected result
        :param target:
        :param update:
        :param expected:
        """
        await self.async_api.telephony.location.update(location_id=target.location_id, settings=update)
        after = await self.async_api.telephony.location.details(location_id=target.location_id)
        self.assertEqual(expected, after)

    @async_test
    async def test_001_site_prefix(self):
        """
        update site prefix
        """
        async with self.target_location() as target:
            target: TelephonyLocation
            prefix = '8999'
            update = TelephonyLocation(routing_prefix=prefix)
            expected = target.copy(deep=True)
            expected.routing_prefix = prefix
            await self.update_and_verify(target=target, update=update, expected=expected)

    @async_test
    async def test_002_duplicate_site_prefix(self):
        """
        Try to assign a duplicate site prefix
        """
        async with self.target_location() as target:
            target: TelephonyLocation
            prefixes = [loc.routing_prefix for loc in self.locations
                        if loc.routing_prefix and loc.routing_prefix != target.routing_prefix]
            if not prefixes:
                self.skipTest('Need another location with routing prefix to run test')
            prefix = choice(prefixes)
            update = TelephonyLocation(routing_prefix=prefix)
            expected = target.copy(deep=True)
            expected.routing_prefix = prefix
            with self.assertRaises(AsRestError) as exc:
                await self.update_and_verify(target=target, update=update, expected=expected)
            rest_error: AsRestError = exc.exception
            self.assertEqual(502, rest_error.status)

    @async_test
    async def test_003_oac(self):
        """
        update OAC
        """
        async with self.target_location() as target:
            target: TelephonyLocation
            oac = '0' if target.outside_dial_digit == '9' else '9'
            update = TelephonyLocation(outside_dial_digit=oac)
            expected = target.copy(deep=True)
            expected.outside_dial_digit = oac
            await self.update_and_verify(target=target, update=update, expected=expected)

    @async_test
    async def test_004_external_caller_id_name(self):
        """
        update external caller id name
        """
        async with self.target_location() as target:
            target: TelephonyLocation
            name = f'{target.external_caller_id_name}xyz'
            update = TelephonyLocation(external_caller_id_name=name)
            expected = target.copy(deep=True)
            expected.external_caller_id_name = name
            await self.update_and_verify(target=target, update=update, expected=expected)

    @async_test
    async def test_005_main_number(self):
        """
        update OAC
        """
        tn = None
        try:
            async with self.target_location() as target:
                target: TelephonyLocation

                numbers = await self.async_api.telephony.phone_numbers(location_id=target.location_id,
                                                                       number_type=NumberType.number)
                main_number = next((n for n in numbers if n.main_number), None)
                if main_number is None:
                    self.skipTest(f'Location "{target.name}" has no main number set')
                # get a new number in the same range
                tn_list = await as_available_tns(as_api=self.async_api, tn_prefix=main_number.phone_number[:5])
                # add that number to location
                await self.async_api.telephony.location.number.add(location_id=target.location_id,
                                                                   phone_numbers=[tn_list[0]])
                tn = tn_list[0]
                # set calling line id to new number
                update = TelephonyLocation(calling_line_id=CallingLineId(phone_number=tn))
                expected = target.copy(deep=True)
                expected.calling_line_id.phone_number = tn
                await self.update_and_verify(target=target, update=update, expected=expected)
        finally:
            # remove TN from location again
            if tn:
                await self.async_api.telephony.location.number.remove(location_id=target.location_id,
                                                                      phone_numbers=[tn])

    @async_test
    async def test_006_calling_line_id_name(self):
        """
        update external caller id name
        """
        async with self.target_location() as target:
            target: TelephonyLocation
            name = f'{target.calling_line_id.name or ""}xyz'
            update = TelephonyLocation(calling_line_id=CallingLineId(name=name,
                                                                     phone_number=target.calling_line_id.phone_number))
            expected = target.copy(deep=True)
            expected.calling_line_id.name = name
            await self.update_and_verify(target=target, update=update, expected=expected)

    @async_test
    async def test_007_set_pstn(self):
        """
        Create a new location and try to set PSTN choice on that location once
        """
        # TODO: implement test

    @async_test
    async def test_008_change_pstn(self):
        """
        create a test location with some trunk, then set the PSTN choice to that trunk and finally try to change the
        PSTN choice to a different trunk
        """
        # TODO: implement test

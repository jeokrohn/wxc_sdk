import asyncio
import base64
import re
from base64 import b64decode
from contextlib import asynccontextmanager
from dataclasses import dataclass
from itertools import chain
from json import dumps, loads
from random import choice
from typing import ClassVar
from unittest import skip

from test_helper.randomlocation import RandomLocation, NpaInfo, Address

from wxc_sdk.as_rest import AsRestError
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.common import RouteType, RouteIdentity
from wxc_sdk.locations import Location, LocationAddress
from wxc_sdk.people import Person
from wxc_sdk.telephony import NumberType, NumberListPhoneNumber
from wxc_sdk.telephony.location import TelephonyLocation, PSTNConnection, CallingLineId
from wxc_sdk.telephony.location.internal_dialing import InternalDialing
from wxc_sdk.telephony.prem_pstn.route_group import RouteGroup
from wxc_sdk.telephony.prem_pstn.trunk import Trunk
from wxc_sdk.workspace_locations import WorkspaceLocation
from tests.base import TestCaseWithLog, async_test, TestWithLocations
from tests.testutil import as_available_tns, create_random_wsl


class TestLocation(TestWithLocations):

    @async_test
    async def test_001_list_all(self):
        """
        list all locations
        """
        # list locations and telephony locations
        location_list, telephony_location_list = await asyncio.gather(
            self.async_api.locations.list(),
            self.async_api.telephony.location.list(),
            return_exceptions=True
        )
        self.assertTrue(all(not isinstance(l, Exception)
                            for l in (location_list, telephony_location_list)))
        print(f'Got {len(location_list)} locations')
        print(f'Got {len(telephony_location_list)} telephony locations')

    @async_test
    async def test_002_details(self):
        """
        get details for all locations
        """
        locations = self.locations
        # get location details and telephony details for each location
        details, telephony_details = await asyncio.gather(
            asyncio.gather(*[self.async_api.locations.details(location_id=location.location_id)
                             for location in locations], return_exceptions=True),
            asyncio.gather(*[self.async_api.telephony.location.details(location_id=loc.location_id)
                             for loc in locations], return_exceptions=True))
        exception = next((e for e in chain(details, telephony_details) if isinstance(e, Exception)), None)
        if exception:
            raise exception
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
                phone_numbers, trunks, route_groups, npa_data = await asyncio.gather(
                    self.async_api.telephony.phone_numbers(number_type=NumberType.number),
                    self.async_api.telephony.prem_pstn.trunk.list(),
                    self.async_api.telephony.prem_pstn.route_group.list(),
                    random_location.load_npa_data())
                locations = self.locations
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
        # enable location for webex calling
        location = Location(location_id=location_id,
                            name=location_name,
                            time_zone='America/Los_Angeles',
                            announcement_language='en_us',
                            preferred_language='en_us',
                            address=LocationAddress(address1=address.address1,
                                                    city=address.city,
                                                    state=address.state_or_province_abbr,
                                                    postal_code=address.zip_or_postal_code,
                                                    country='US'))
        tel_location_id = self.api.telephony.location.enable_for_calling(location=location)
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


class TestUnifiedLocations(TestCaseWithLog):
    """
    Tests related to "unified" locations
    """

    @async_test
    async def test_001_list_and_understand_ids(self):
        """
        list locations and workspace locations and correlate
        apparently the last part of a base64 decoded workspace location id look like this:
            36818b6f-ef07-43d1-b76f-ced79ab2e3e7#1a4a4644-1b39-4357-bde7-be7bf29ad58b
        .. where the part before the "#" is the UUID org id
        .. and the last part is the actual id
        which can be used to correlate workspace location ids with location ids

        """

        def id_prefix(id: str):
            s = base64.b64decode(f'{id}==').decode()
            return '/'.join(s.split('/')[2:4])

        locations, workspace_locations, me = await asyncio.gather(
            self.async_api.locations.list(),
            self.async_api.workspace_locations.list(),
            self.async_api.people.me())
        locations: list[Location]
        workspace_locations: list[WorkspaceLocation]
        me: Person

        org_id = webex_id_to_uuid(me.org_id)

        decoded_wsl_id_prefixes = set(id_prefix(wsl.id) for wsl in workspace_locations)
        self.assertEqual(1, len(decoded_wsl_id_prefixes))
        decoded_wsl_id_prefix = next(iter(decoded_wsl_id_prefixes))
        decoded_location_id_prefixes = set(id_prefix(loc.location_id) for loc in locations)
        self.assertEqual(1, len(decoded_wsl_id_prefixes))
        decoded_location_id_prefix = next(iter(decoded_location_id_prefixes))

        wsl_ids = set((webex_id_to_uuid(wsl.id).split('#')[-1] for wsl in workspace_locations))
        wsl_id_1st_part = set(webex_id_to_uuid(wsl.id).split('#')[0] for wsl in workspace_locations)
        location_ids = set((webex_id_to_uuid(loc.location_id) for loc in locations))
        # location ids and the part of the WSL id after the "#" really identical?
        location_by_uuid = {webex_id_to_uuid(location.location_id): location for location in locations}
        err = False
        for wsl in workspace_locations:
            location_uuid = webex_id_to_uuid(wsl.id).split("#")[-1]
            location = location_by_uuid.get(location_uuid)
            if location is None:
                print(f'Workspace location "{wsl.display_name}" with id {webex_id_to_uuid(wsl.id)}: '
                      f'couldn\'t find location with uuid {location_uuid}')
                err = True
        self.assertFalse(err)

        # we also assume that we get the same number of responses from both APIs
        self.assertEqual(len(locations), len(workspace_locations))

        # also the 1st part of the WSL id (before the "#" is the org id)
        self.assertEqual(1, len(wsl_id_1st_part))
        self.assertEqual({org_id}, wsl_id_1st_part)

        print(f'base64 decoded workspace location ids use prefix: {decoded_wsl_id_prefix}')
        print(f'base64 decoded location ids use prefix: {decoded_location_id_prefix}')

    @async_test
    async def test_002_determine_calling(self):
        """
        list all locations and determine calling locations by trying to get calling details
        :return:
        """
        locations = await self.async_api.locations.list()
        calling_details = await asyncio.gather(
            *[self.async_api.telephony.location.details(location_id=loc.location_id) for loc in
              locations], return_exceptions=True)
        # we either get calling details or the call leads to 404 AsRestError
        name_len = max(map(len, (loc.name for loc in locations)))
        err = False
        for location, details in zip(locations, calling_details):
            print(f'{location.name:{name_len}}: ', end='')
            if isinstance(details, TelephonyLocation):
                print('telephony location')
            elif isinstance(details, AsRestError) and details.status == 404:
                print(f'not a calling location, got a 404')
            else:
                err = True
                print(f'unexpected result: {details}')
        self.assertFalse(err)

    def test_003_create_wsl_and_check_in_locations(self):
        """
        create a workspace location and verify that it shows up in location list
        .. then clean up and check that this also affects both, workspace and location list
        """
        new_wsl = create_random_wsl(api=self.api)
        err = []
        new_location = None
        try:
            locations = list(self.api.locations.list())
            new_location = next((loc for loc in locations
                                 if loc.location_id_uuid == new_wsl.id_uuid), None)
            if new_location is None:
                err.append('New WSL not found in locations')
        finally:
            self.api.workspace_locations.delete(location_id=new_wsl.id)
            # now the location should be gone both in the WSK and location list
            wsl_list = list(self.api.workspace_locations.list())
            locations = list(self.api.locations.list())
            err = []
            if next((wsl for wsl in wsl_list if wsl.id == new_wsl.id), None) is not None:
                err.append('Workspace location not deleted')
            if new_location and next((loc for loc in locations if loc.location_id == new_location.location_id),
                                     None) is not None:
                err.append('Location not deleted')
        self.assertTrue(not err, '\n'.join(err))

    @async_test
    async def test_004_cleanup_workspace_locations(self):
        """
        Find workspace locations for which we don't have a location
        .. and delete them
        :return:
        """
        locations, workspace_locations = await asyncio.gather(
            self.async_api.locations.list(),
            self.async_api.workspace_locations.list())
        locations: list[Location]
        workspace_locations: list[WorkspaceLocation]
        location_uuid_list = set(loc.location_id_uuid for loc in locations)
        workspace_locations_wo_location = [wsl for wsl in workspace_locations
                                           if wsl.id_uuid not in location_uuid_list]
        if not workspace_locations_wo_location:
            self.skipTest('No workspace locations w/o location')

        # delete them
        delete_results = await asyncio.gather(
            *[self.async_api.workspace_locations.delete(location_id=wsl.id)
              for wsl in workspace_locations_wo_location], return_exceptions=True)

        # any issues deleting?
        for wsl, result in zip(workspace_locations_wo_location, delete_results):
            if isinstance(result, Exception):
                print(f'{wsl.display_name}: {result}')
        self.assertFalse(any(map(lambda r: isinstance(r, Exception), delete_results)))

    def test_003_create_workspace_location_and_upgrade_to_calling(self):
        """
        Create a workspace location and upgrade to calling
        """
        new_wsl = create_random_wsl(api=self.api)
        print(f'Created WSL: {new_wsl.display_name}')
        new_location = next((loc for loc in self.api.locations.list()
                             if loc.location_id_uuid == new_wsl.id_uuid), None)
        self.assertIsNotNone(new_location, 'WSL created, but no location found')

        # postal_code and state are missing
        # WSL address looks like: 7133 Woodside Road, Pensacola, FL 32526 USA
        m = re.search(r'\b(\w{2})\b (\d+) USA', new_wsl.address)
        self.assertIsNotNone(m, f'Failed to get state, postalcode from "{new_wsl.display_name}"')
        new_location.address.postal_code = m.group(2)
        new_location.address.state = m.group(1)

        # also some more attributes need to be set
        new_location.announcement_language = 'en_us'
        new_location.preferred_language = 'en_us'
        new_location.time_zone = 'America/Los_Angeles'

        # enable location for calling
        self.api.telephony.location.enable_for_calling(location=new_location)


class TestUpdate(TestWithLocations):
    """
    Tests updating locations
    """

    @asynccontextmanager
    async def target_location(self) -> Location:
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
                                                 for loc in us_locations], return_exceptions=True)
                details = [d for d in details
                           if not isinstance(d, Exception)]
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
            if not restore.outside_dial_digit:
                restore.outside_dial_digit = ''
            if not restore.routing_prefix:
                restore.routing_prefix = ''
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
                expected.calling_line_id.name = None
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

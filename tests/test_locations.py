import asyncio
import base64
import re
from base64 import b64decode
from collections import defaultdict
from collections.abc import Callable, Generator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from functools import partial
from itertools import chain
from json import dumps, loads
from operator import attrgetter
from random import choice
from typing import ClassVar, NamedTuple, Any
from unittest import skip

from pydantic import TypeAdapter
from test_helper.randomlocation import RandomLocation, NpaInfo, Address

from tests.base import TestCaseWithLog, async_test, TestWithLocations
from tests.testutil import as_available_tns, create_random_wsl
from wxc_sdk.as_rest import AsRestError
from wxc_sdk.base import webex_id_to_uuid, ApiModel
from wxc_sdk.common import RouteType, RouteIdentity
from wxc_sdk.devices import ProductType
from wxc_sdk.locations import Location, LocationAddress
from wxc_sdk.people import Person
from wxc_sdk.rest import RestError
from wxc_sdk.telephony import NumberType, NumberListPhoneNumber, OwnerType
from wxc_sdk.telephony.autoattendant import AutoAttendant
from wxc_sdk.telephony.callqueue import CallQueue
from wxc_sdk.telephony.huntgroup import HuntGroup
from wxc_sdk.telephony.location import TelephonyLocation, PSTNConnection, CallingLineId
from wxc_sdk.telephony.location.internal_dialing import InternalDialing
from wxc_sdk.telephony.paging import Paging
from wxc_sdk.telephony.prem_pstn.route_group import RouteGroup
from wxc_sdk.telephony.prem_pstn.trunk import Trunk
from wxc_sdk.telephony.virtual_line import VirtualLine
from wxc_sdk.telephony.voicemail_groups import VoicemailGroup
from wxc_sdk.workspace_locations import WorkspaceLocation
from wxc_sdk.workspaces import Workspace


# TODO: add test cases for floors etc. (see WorksspaceLocations test cases)


class TestLocationSimple(TestCaseWithLog):

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
        with self.no_log():
            locations = list(self.api.locations.list())
        # get location details and telephony details for each location
        details, telephony_details = await asyncio.gather(
            asyncio.gather(*[self.async_api.locations.details(location_id=location.location_id)
                             for location in locations], return_exceptions=True),
            asyncio.gather(*[self.async_api.telephony.location.details(location_id=loc.location_id)
                             for loc in locations], return_exceptions=True))
        exception = None
        for location, detail, telephony_detail in zip(locations, details, telephony_details):
            print(f'{location.name}')
            if isinstance(detail, Exception):
                print(f'  error getting location details: {detail}')
                exception = exception or detail
            if isinstance(telephony_detail, Exception):
                print(f'  error getting telephony location details: {telephony_detail}')
        if exception:
            raise exception
        print(f'Got details for {len(locations)} locations')


class TestLocation(TestWithLocations):

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

        # TODO: looks like announcement_language and time_zone can't be set here?
        location_id = self.api.locations.create(name=location_name,
                                                time_zone='America/Chicago',
                                                announcement_language=None,
                                                preferred_language='de_de',
                                                address1=address.address1,
                                                city=address.city,
                                                state=address.state_or_province_abbr,
                                                postal_code=address.zip_or_postal_code,
                                                country='US')

        created_location = await self.async_api.locations.details(location_id=location_id)
        # enable location for webex calling
        location = Location(location_id=location_id,
                            name=location_name,
                            time_zone='America/Chicago',
                            announcement_language='de_de',
                            preferred_language='de_de',
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
        password = self.api.telephony.location.generate_password(location_id=location_id)
        print(f'Creating trunk "{trunk_name}" in location "{location_name}"')
        trunk_id = self.api.telephony.prem_pstn.trunk.create(name=trunk_name,
                                                             location_id=location_id,
                                                             password=password)

        # set PSTN choice for location to trunk
        print(f'Setting new trunk "{trunk_name}" as PSTN choice for location "{location_name}"')
        self.api.telephony.location.update(location_id=location_id,
                                           settings=TelephonyLocation(
                                               connection=PSTNConnection(type=RouteType.trunk,
                                                                         id=trunk_id)))

        # add number to location
        self.api.telephony.location.number.add(location_id=location_id, phone_numbers=[tn])

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
        print(dumps(loads(location_details.model_dump_json()), indent=2))
        print('--------------- Location telephony details ---------------')
        print(dumps(loads(telephony_details.model_dump_json()), indent=2))

    @skip('avoid too many dummy locations')
    def test_004_create_and_validate_settings(self):
        """
        Apparently time zone and announcement language are not set when creating a location?
        """
        l_names = set(l.name for l in self.api.locations.list('TEST'))
        location_name = next((name for i in range(100) if (name := f'TEST_{i:03}') not in l_names), None)
        print(f'Creating location "{location_name}"')
        location_id = self.api.locations.create(name=location_name,
                                                time_zone='Europe/Berlin',
                                                announcement_language='de_de',
                                                preferred_language='de_de',
                                                address1='strasse 1',
                                                city='Darmstadt',
                                                state=None,
                                                postal_code='64291',
                                                country='DE')
        details = self.api.locations.details(location_id=location_id)
        self.assertEqual('de_de', details.preferred_language)
        self.assertEqual('Europe/Berlin', details.time_zone)

    @async_test
    async def test_005_create_and_update_location(self):
        """
        Create a test location (no calling)
        """
        async with RandomLocation() as random_location:
            address = await random_location.random_address()
            address1 = await random_location.random_address()
        # determine a name for the new randon location
        location_names = set(loc.name for loc in self.api.locations.list())
        new_location_name = next((name
                                  for i in range(1, 100)
                                  if (name := f'{address.city} {i:02d}') not in location_names))
        new_location_id = self.api.locations.create(name=new_location_name,
                                                    time_zone='America/Chicago',
                                                    preferred_language='en_us',
                                                    announcement_language='en_us',
                                                    address1=address.address1,
                                                    city=address.city,
                                                    state=address.state_or_province_abbr,
                                                    postal_code=address.zip_or_postal_code,
                                                    country='US',
                                                    address2=address.address2,
                                                    latitude=address.geo_location.lat,
                                                    longitude=address.geo_location.lon,
                                                    notes='auto generated')
        location_details = self.api.locations.details(location_id=new_location_id)
        # try to update the location
        update = location_details.model_copy(deep=True)
        new_address = LocationAddress(address1=address1.address1, address2=address1.address2, city=address1.city,
                                      state=address1.state_or_province_abbr, postal_code=address1.zip_or_postal_code,
                                      country='US')
        update.address = new_address
        update.longitude = address1.geo_location.lon
        update.latitude = address1.geo_location.lat
        update.notes = 'updated notes'
        self.api.locations.update(location_id=new_location_id, settings=update)
        after_update = self.api.locations.details(location_id=new_location_id)
        self.assertEqual(update, after_update)


class CodeAndName(ApiModel):
    code: str
    name: str


class CPAPICountryDetail(ApiModel):
    url: str
    state_required: bool
    zip_code_required: bool
    states: list[CodeAndName]
    time_zones: list[str]


class TestCountries(TestCaseWithLog):
    def test_001_list_countries(self):
        """
        Try to list countries using CPAPI
        """
        me = self.api.people.me()
        org_id_uuid = webex_id_to_uuid(me.org_id)
        url = f'https://cpapi-r.wbx2.com/api/v1/customers/{org_id_uuid}/countries'
        data = self.api.session.rest_get(url)
        countries = TypeAdapter(list[CodeAndName]).validate_python(data['countries'])
        countries.sort(key=attrgetter('name'))
        print('\n'.join(f'{c.code}: {c.name}' for c in countries))

    def test_002_details_belgium(self):
        """
        Get details for Belgium
        """
        me = self.api.people.me()
        org_id_uuid = webex_id_to_uuid(me.org_id)
        country_code = 'BE'
        url = f'https://cpapi-r.wbx2.com/api/v1/customers/{org_id_uuid}/countries/{country_code}'
        data = self.api.session.rest_get(url)
        result = CPAPICountryDetail.model_validate(data)
        print(dumps(loads(result.model_dump_json()), indent=2))


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
            elif isinstance(details, AsRestError) and details.status in {404, 400}:
                print(f'not a calling location, got a {details.status}')
            else:
                err = True
                print(f'unexpected result: {details}')
        self.assertFalse(err)

    @skip('workspace locations deprecated')
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

    @skip('workspace locations deprecated')
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
            yield target.model_copy(deep=True)
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
            expected = target.model_copy(deep=True)
            expected.name = new_name
            await self.update_and_verify(target=target, update=expected, expected=expected)

    @async_test
    async def test_002_update_timezone(self):
        async with self.target_location() as target:
            target: Location
            new_zone = 'America/New_York' if target.time_zone == 'America/Los_Angeles' else 'America/Los_Angeles'
            expected = target.model_copy(deep=True)
            expected.time_zone = new_zone
            await self.update_and_verify(target=target, update=expected, expected=expected)

    @async_test
    async def test_003_update_address2(self):
        """
        Change address line 2
        """
        async with self.target_location() as target:
            target: Location
            address2 = 'whatever'
            expected = target.model_copy(deep=True)
            expected.address.address2 = address2
            await self.update_and_verify(target=target, update=expected, expected=expected)

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

        def location_update(location: Location) -> Location:
            update = location.model_copy(deep=True)
            update.address.address2 = None
            return update

        await asyncio.gather(*[self.async_api.locations.update(location_id=loc.location_id,
                                                               settings=location_update(loc))
                               for loc in targets])


@skip('Not an actual test')
class ClearAddress2(TestCaseWithLog):
    @async_test
    async def test_clear_address2(self):
        targets = [loc for loc in await self.async_api.locations.list()
                   if loc.address.address2 is not None]

        async def clear_address2(location: Location):
            address = location.address.model_copy(deep=True)
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

    async def update_and_wait_for_job(self, location_id: str, settings: Location):
        batch_job_id = await self.async_api.telephony.location.update(location_id=location_id,
                                                                      settings=settings)
        if batch_job_id:
            # wait for job to complete
            while True:
                job = await self.async_api.telephony.jobs.update_routing_prefix.status(job_id=batch_job_id)
                if job.latest_execution_status == 'COMPLETED':
                    break
                await asyncio.sleep(5)
        return

    @asynccontextmanager
    async def target_location(self) -> TelephonyLocation:
        """
        Get a target location for tests
        """
        if self.locations is None:
            with self.no_log():
                locations = await self.async_api.locations.list()
                # some location are getting created as workspace locations. These locations don't have preferred
                # language and we ignore them as candidates for these tests
                us_locations = [loc for loc in locations
                                if loc.address.country == 'US' and loc.preferred_language]
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
            yield details.model_copy(deep=True)
        finally:
            # restore old settings.
            # but don't try to update the PSTN settings again
            restore = details.model_copy(deep=True)
            restore.connection = None
            if not restore.outside_dial_digit:
                restore.outside_dial_digit = None
            if not restore.routing_prefix:
                restore.routing_prefix = None
            await self.update_and_wait_for_job(location_id=target.location_id, settings=restore)
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
        await self.update_and_wait_for_job(location_id=target.location_id, settings=update)
        after = await self.async_api.telephony.location.details(location_id=target.location_id)
        # ignore calling line id name in compare
        expected.calling_line_id.name = after.calling_line_id.name
        self.assertEqual(expected, after)

    @async_test
    async def test_001_site_prefix(self):
        """
        update site prefix
        """
        async with self.target_location() as target:
            target: TelephonyLocation
            prefixes = set(loc.routing_prefix for loc in self.locations)
            prefix = next(p for i in range(1, 1000) if (p := f'8{i:03}') not in prefixes)
            update = TelephonyLocation(routing_prefix=prefix)
            expected = target.model_copy(deep=True)
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
            expected = target.model_copy(deep=True)
            expected.routing_prefix = prefix
            with self.assertRaises(AsRestError) as exc:
                await self.update_and_verify(target=target, update=update, expected=expected)
            rest_error: AsRestError = exc.exception
            self.assertEqual(400, rest_error.status)
            self.assertEqual(5600, rest_error.detail.code)

    @async_test
    async def test_003_oac(self):
        """
        update OAC
        """
        async with self.target_location() as target:
            target: TelephonyLocation
            oac = '0' if target.outside_dial_digit == '9' else '9'
            update = TelephonyLocation(outside_dial_digit=oac)
            expected = target.model_copy(deep=True)
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
            expected = target.model_copy(deep=True)
            expected.external_caller_id_name = name
            await self.update_and_verify(target=target, update=update, expected=expected)

    @async_test
    async def test_005_main_number(self):
        """
        update main number
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
                expected = target.model_copy(deep=True)
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
            expected = target.model_copy(deep=True)
            expected.calling_line_id.name = name
            await self.update_and_verify(target=target, update=update, expected=expected)

    @async_test
    async def test_set_oac_and_validate_oac_enforcement(self):
        """
        Try to change OAC and verify that OAC enforcement policy doesn't get changed
        """
        async with self.target_location() as target:
            target: TelephonyLocation
            # enable OAC enforcement
            settings = TelephonyLocation(enforce_outside_dial_digit=True)
            lapi = self.api.telephony.location
            lapi.update(location_id=target.location_id, settings=settings)

            # validate
            after = lapi.details(location_id=target.location_id)
            self.assertTrue(after.enforce_outside_dial_digit)

            # update OAC
            old_oac = target.outside_dial_digit
            settings = TelephonyLocation(outside_dial_digit='6')
            lapi.update(location_id=target.location_id, settings=settings)

            # validate OAC enforcement
            after = lapi.details(location_id=target.location_id)
            self.assertTrue(after.enforce_outside_dial_digit)
            self.assertEqual('6', after.outside_dial_digit)

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


@dataclass
class LocationInfo:
    location: Location = field(default=None)
    workspace: WorkspaceLocation = field(default=None)
    calling: TelephonyLocation = field(default=None)

    @property
    def ok(self) -> bool:
        location_uuid = self.location and webex_id_to_uuid(self.location.location_id)
        return self.location is not None and self.workspace is not None and \
            location_uuid == webex_id_to_uuid(self.workspace.id).split('#')[-1] and \
            (self.calling is None or location_uuid == webex_id_to_uuid(self.calling.location_id))


class TestLocationConsistency(TestCaseWithLog):
    """
    Tests around location consistency
    """

    def get_location_info(self) -> dict[str, LocationInfo]:
        locations = list(self.api.locations.list())
        workspace_locations = list(self.api.workspace_locations.list())
        calling_locations = list(self.api.telephony.location.list())

        location_info: dict[str, LocationInfo] = defaultdict(LocationInfo)
        for loc in locations:
            location_info[loc.name].location = loc
        for ws in workspace_locations:
            location_info[ws.display_name].workspace = ws
        for cl in calling_locations:
            location_info[cl.name].calling = cl
        return location_info

    def test_001_check_consistency(self):
        """
        Get locations, calling location details, workspace locations and compare...
        """
        location_info = self.get_location_info()
        location_id_set = set(li.location.location_id for li in location_info.values()
                              if li.location)

        for name in sorted(location_info):
            info = location_info[name]
            if info.ok:
                # print(f'"{name}": ok')
                print(f'{name}')
                print(f'            location id: {webex_id_to_uuid(info.location.location_id)}')
                print(
                    f'         ws location id: {webex_id_to_uuid(info.workspace.id)} '
                    f'{base64.b64decode(info.workspace.id + "==").decode()}')
                print(f'  telephony location id: {info.calling and webex_id_to_uuid(info.calling.location_id)}')
                continue
            print(f'!!!!!!!!! {name} with issues:')
            if info.location is not None:
                print(f'                              location id: {webex_id_to_uuid(info.location.location_id)}')
            if info.workspace is not None:
                print(f'                             workspace id: {webex_id_to_uuid(info.workspace.id)}')
            if info.calling is not None:
                print(f'  location id in calling location details: {webex_id_to_uuid(info.calling.location_id)}')
                print(f'    location id {webex_id_to_uuid(info.calling.location_id)} '
                      f'does{"" if info.calling.location_id in location_id_set else " not"} exist in location list ')
        self.assertTrue(all(li.ok for li in location_info.values()))

    def test_002_users_no_calling(self):
        """
        try to find users w/o calling
        """
        users_wo_calling = [user for user in self.api.people.list(callingData=True)
                            if user.location_id is None]
        print('\n'.join(sorted(u.display_name for u in users_wo_calling)))

    def test_003_users_by_location(self):
        """
        For each location show the users belonging to that location
        """
        users_by_location_id: dict[str, list[Person]] = defaultdict(list)
        for user in self.api.people.list(callingData=True):
            users_by_location_id[user.location_id].append(user)
        covered = set()
        for location in self.api.locations.list():
            covered.add(location.location_id)
            users = users_by_location_id.get(location.location_id, list())
            print(f'"{location.name}" ({len(users)} users)')
            if not users:
                print('  - no users- ')
            else:
                print('\n'.join(sorted(f'  - {user.display_name}' for user in users)))
        err = False
        for location_id, users in users_by_location_id.items():
            if location_id in covered:
                continue
            for user in users:
                err = err or (location_id is not None)
                print(f'user not in known location: {location_id or ""} {user.display_name}({user.emails[0]})')
        self.assertFalse(err, 'User inconsistencies')

    def test_004_numbers_and_locations(self):
        """
        check for numbers and location consistency
        """
        locations = list(self.api.locations.list())
        numbers = list(self.api.telephony.phone_numbers())
        numbers_by_location: dict[str, list[NumberListPhoneNumber]] = defaultdict(list)
        for number in numbers:
            numbers_by_location[number.location.id].append(number)
        covered = set()
        for location in locations:
            covered.add(location.location_id)
            numbers = numbers_by_location.get(location.location_id)
            print(location.name)
            if numbers is None:
                print('  - no numbers- ')
            else:
                for number in numbers:
                    print(f'  {number.phone_number or "":12} {number.extension or ""}')

        numbers_in_unknown_location = list(chain.from_iterable(numbers
                                                               for location_id, numbers in numbers_by_location.items()
                                                               if location_id not in covered))
        if not numbers_in_unknown_location:
            return

        # what is the longest location name in any number in an unknown location?
        loc_len = max(len(n.location.name)
                      for n in numbers_in_unknown_location)

        for number in numbers_in_unknown_location:
            print(
                f'number in unknown location "{number.location.name:{loc_len}}"('
                f'{webex_id_to_uuid(number.location.id)}): '
                f'{number.phone_number or "":12} {number.extension or ""}')
        self.assertTrue(not numbers_in_unknown_location, 'Found numbers in unknown locations')

    def test_005_trunks_and_locations(self):
        """
        check for trunks and location consistency
        """
        locations = list(self.api.locations.list())
        trunks = list(self.api.telephony.prem_pstn.trunk.list())
        trunks_by_location: dict[str, list[Trunk]] = defaultdict(list)
        for trunk in trunks:
            trunks_by_location[trunk.location.id].append(trunk)
        covered = set()
        for location in locations:
            covered.add(location.location_id)
            trunks = trunks_by_location.get(location.location_id)
            print(location.name)
            if trunks is None:
                print('  - no trunks - ')
            else:
                for trunk in trunks:
                    print(f'  {trunk.name}')

        trunks_in_unknown_location = list(chain.from_iterable(trunks
                                                              for location_id, trunks in trunks_by_location.items()
                                                              if location_id not in covered))
        if not trunks_in_unknown_location:
            return

        loc_len = max(len(trunk.location.name) for trunk in trunks_in_unknown_location)
        t_len = max(len(trunk.name) for trunk in trunks_in_unknown_location)

        err = False
        for location_id, trunks in trunks_by_location.items():
            if location_id in covered:
                continue
            err = True
            for trunk in trunks:
                print(f'trunk in unknown location: location "{trunk.location.name:{loc_len}}" '
                      f'({webex_id_to_uuid(trunk.location.id)}), trunk "{trunk.name:{t_len}}" '
                      f'({webex_id_to_uuid(trunk.trunk_id)})')
        self.assertFalse(err, 'Found trunks in unknown locations')

    def test_006_number_ownership(self):
        """
        check consistency of number ownerships
        """

        def check_exists(number_key: NumberListPhoneNumber, cache: dict[str, Any],
                         list_call: Callable[[], Generator[Any, None, None]],
                         key_attr: Callable[[Any], str], entity: str):
            owner_webex_id = number_key.owner.owner_id
            decoded_owner_webex_id = base64.b64decode(owner_webex_id + '==').decode()
            # we use the UUID for the lookup
            owner_uuid = webex_id_to_uuid(owner_webex_id)
            if not cache:
                # fill the cache
                entities = list_call()
                # assert that dict has at least one entry .. even if the list call doesn't return anything
                cache[''] = ''
                # add entities to dict
                for en in entities:
                    cache[webex_id_to_uuid(key_attr(en))] = en
            if (en := cache.get(owner_uuid)) is None:
                return f'{entity} not found'
            en_webex_id = key_attr(en)
            decoded_en_webex_id = base64.b64decode(en_webex_id + '==').decode()
            if decoded_owner_webex_id != decoded_en_webex_id:
                # looks like we found an entry using the UUID as index, but the actual IDs are different
                return f'{entity}: id mismatch, from owner: {decoded_owner_webex_id}, entity id: {decoded_en_webex_id}'
            return ''

        def vm_exists(number_key: NumberListPhoneNumber) -> str:
            """
            Validator for VM portal number
            :param number_key:
            :return:
            """
            # get VM portal settings for location
            try:
                vm_settings = self.api.telephony.voiceportal.read(location_id=number_key.location.id)
            except RestError:
                vm_settings = None
            if vm_settings is None:
                return f'failed to get voiceportal settings for location "{number_key.location.name}" ' \
                       f'{webex_id_to_uuid(number_key.location.id)}'
            if number_key.extension and number_key.extension != vm_settings.extension or number_key.phone_number and \
                    number_key.phone_number != vm_settings.phone_number:
                return f'voiceportal setting mismatch for location "{number_key.location.name}" ' \
                       f'{webex_id_to_uuid(number_key.location.id)}: ' \
                       f'extension {number_key.extension or ""}/{vm_settings.extension or ""} ' \
                       f'phone number {number_key.phone_number or ""}/{vm_settings.phone_number or ""}'
            return ''

        # noinspection PyShadowingNames
        def check_devices_and_owners(numbers: list[NumberListPhoneNumber]) -> bool:
            """
            For each device that belongs to a user or workspace we want to find a number with the respective owner id
            """
            err = False
            devices = list(self.api.devices.list())
            for device in devices:
                owner_id = device.person_id or device.workspace_id
                if not owner_id:
                    continue
                decoded_owner_id = base64.b64decode(owner_id + '==').decode()

                # try to find a number with this owner_id
                number = next((number for number in numbers
                               if number.owner and number.owner.owner_id == owner_id),
                              None)
                if number:
                    continue
                err = True
                print(f'device "{device.display_name}" no owner found for '
                      f'{"workspace" if device.workspace_id else "person"}_id: '
                      f'{owner_id}, {decoded_owner_id}'
                      f'{", might be a room device w/o calling" if device.product_type == ProductType.roomdesk else ""}')
            return err

        class ValidatorCache(NamedTuple):
            users: dict[str, Person]
            auto_attendants: dict[str, AutoAttendant]
            virtual_lines: dict[str, VirtualLine]
            call_queues: dict[str, CallQueue]
            places: dict[str, Workspace]
            hunt_groups: dict[str, HuntGroup]
            vm_groups: dict[str, VoicemailGroup]
            group_paging: dict[str, Paging]

        validator_cache = ValidatorCache(users=dict(),
                                         auto_attendants=dict(),
                                         virtual_lines=dict(),
                                         call_queues=dict(),
                                         places=dict(),
                                         hunt_groups=dict(),
                                         vm_groups=dict(),
                                         group_paging=dict())

        # dict of validators for each owner type
        validators = {
            OwnerType.people: partial(check_exists, cache=validator_cache.users,
                                      list_call=partial(self.api.people.list, callingData=True),
                                      key_attr=attrgetter('person_id'), entity='user'),
            OwnerType.auto_attendant: partial(check_exists, cache=validator_cache.auto_attendants,
                                              list_call=self.api.telephony.auto_attendant.list,
                                              key_attr=attrgetter('auto_attendant_id'), entity='auto attendant'),
            OwnerType.virtual_line: partial(check_exists, cache=validator_cache.virtual_lines,
                                            list_call=self.api.telephony.virtual_lines.list,
                                            key_attr=attrgetter('id'), entity='virtual line'),
            OwnerType.call_queue: partial(check_exists, cache=validator_cache.call_queues,
                                          list_call=self.api.telephony.callqueue.list,
                                          key_attr=attrgetter('id'), entity='call queue'),
            OwnerType.place: partial(check_exists, cache=validator_cache.places,
                                     list_call=self.api.workspaces.list,
                                     key_attr=attrgetter('workspace_id'), entity='workspace'),
            OwnerType.hunt_group: partial(check_exists, cache=validator_cache.hunt_groups,
                                          list_call=self.api.telephony.huntgroup.list,
                                          key_attr=attrgetter('id'), entity='huntgroup'),
            OwnerType.voice_messaging: vm_exists,
            OwnerType.voicemail_group: partial(check_exists, cache=validator_cache.vm_groups,
                                               list_call=self.api.telephony.voicemail_groups.list,
                                               key_attr=attrgetter('group_id'), entity='voicemail group'),
            OwnerType.group_paging: partial(check_exists, cache=validator_cache.group_paging,
                                            list_call=self.api.telephony.paging.list,
                                            key_attr=attrgetter('paging_id'), entity='paging group')
        }

        numbers = list(self.api.telephony.phone_numbers())
        err = False
        for number in numbers:
            if not number.owner:
                continue
            owner_type = number.owner.owner_type

            validator = validators.get(owner_type)
            if validator is None:
                result = 'no validator'
            else:
                result = validator(number)
            if not result:
                continue
            err = True
            print(f'tn:{number.phone_number or "":12}/ext:{number.extension or "":4} '
                  f'in "{number.location.name}"({webex_id_to_uuid(number.location.id)})'
                  f'{", main number " if number.main_number else " "}'
                  f'{number.owner.owner_type} '
                  f'"{number.owner.first_name}"/"{number.owner.last_name}"'
                  f'({webex_id_to_uuid(number.owner.owner_id)}): {result}')

        # also there seems to be an issue with owner IDs for workspaces in the numbers response
        numbers_in_workspaces = [n for n in numbers if n.owner and n.owner.owner_type == OwnerType.place]
        if numbers_in_workspaces:
            # key: workstation display name
            # value: owner UUID
            owner_name_and_id: dict[str, str] = dict()
            for number in numbers_in_workspaces:
                owner_display_name = f'{number.owner.first_name} {number.owner.last_name.strip(".")}'.strip()
                owner_name_and_id[owner_display_name] = base64.b64decode(number.owner.owner_id + '==').decode()

            # create an equivalent dict based on list of workstations
            ws_name_and_id = dict()
            for ws in validator_cache.places.values():
                if not ws:
                    # skip sentinel
                    continue
                ws_name_and_id[ws.display_name] = base64.b64decode(ws.workspace_id + '==').decode()

            # now see if the IDs are equivalent for each given display name
            for name in sorted(owner_name_and_id):
                owner_id = owner_name_and_id[name]
                ws_id = ws_name_and_id.get(name, 'not found')
                if owner_id != ws_id:
                    print(f'{name} owner id {owner_id} workspace id {ws_id}')
                    err = True

        if check_devices_and_owners(numbers):
            err = True

        self.assertFalse(err, 'Some issues with numbers')

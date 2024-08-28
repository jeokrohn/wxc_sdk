"""
Testing DECT devices
"""
import asyncio
import json
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from itertools import chain
from operator import attrgetter
from typing import NamedTuple

from pydantic import TypeAdapter

from tests.base import TestWithLocations, async_test
from wxc_sdk.common import UserType
from wxc_sdk.locations import Location
from wxc_sdk.rest import RestError
from wxc_sdk.telephony.dect_devices import DECTNetworkModel, DECTNetworkDetail, BaseStationResponse, \
    BaseStationsResponse, DECTHandsetItem, DectDevice
from wxc_sdk.telephony.devices import AvailableMember
from wxc_sdk.telephony.virtual_line import VirtualLine


class TestDECTNetwork(NamedTuple):
    target_location: Location
    dect_network_id: str


class TestDectDevices(TestWithLocations):

    def test_device_types(self):
        """
        Read the DECT device type list
        """
        api = self.api.telephony.dect_devices
        device_types = api.device_type_list()
        print(f'found {len(device_types)} DECT device types')
        print(json.dumps(TypeAdapter(list[DectDevice]).dump_python(device_types,
                                                                   mode='json', by_alias=True), indent=2))

    @contextmanager
    def create_test_dect_network(self, keep: bool = False) -> TestDECTNetwork:
        """
        Create a test dect network in given location
        :return: test DECT network context
        """
        target_location = random.choice(self.locations)
        target_location: Location
        api = self.api.telephony.dect_devices
        with self.no_log():
            networks = api.list_dect_networks(location_id=target_location.location_id)
        names = set(n.name for n in networks)
        new_names = (name for i in range(1, 1000) if (name := f'test_{i:03}') not in names)
        new_name = next(new_names)
        access_code = f'1{new_name[-3:]}'
        network_id = api.create_dect_network(location_id=target_location.location_id,
                                             name=new_name,
                                             display_name=f'd{new_name}',
                                             model=DECTNetworkModel.dms_cisco_dbs210,
                                             default_access_code_enabled=True,
                                             default_access_code=access_code)
        print(f'DECT network "{new_name}" in location "{target_location.name}"')
        try:
            yield TestDECTNetwork(target_location, network_id)
        finally:
            if not keep:
                api.delete_dect_network(location_id=target_location.location_id, dect_network_id=network_id)
        return

    def test_001_create_network(self):
        """
        Test to create a DECT network
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network(keep=True) as ctx:
            ctx: TestDECTNetwork
            details = api.dect_network_details(location_id=ctx.target_location.location_id,
                                               dect_network_id=ctx.dect_network_id)
        print(json.dumps(details.model_dump(), indent=2))

    def test_list_networks(self):
        """
        List networks
        """
        dect_networks = self.api.telephony.dect_devices.list_dect_networks()
        print(f'found {len(dect_networks)} DECT networks')

    @async_test
    async def test_list_networks_by_location(self):
        """
        list networks by location and make sure that location IDs are ok
        """
        network_lists = await asyncio.gather(
            *[self.async_api.telephony.dect_devices.list_dect_networks(location_id=loc.location_id) for loc in
              self.locations],
            return_exceptions=True)
        err = None
        for location, network_list in zip(self.locations, network_lists):
            location: Location
            if isinstance(network_list, Exception):
                err = err or network_list
                print(f'{location.name}: failed to get network list, {network_list}')
                continue
            network_list: list[DECTNetworkDetail]
            print(f'location: {location.name}, {len(network_list)} DECT networks: '
                  f'{", ".join(n.name for n in network_list)}')
            try:
                self.assertTrue(all(network.location.id == location.location_id for network in network_list))
            except AssertionError as e:
                print(f'{location.name}: assertion error, {e}')
                err = err or e

        if err is not None:
            raise err

    @async_test
    async def test_dect_network_details(self):
        """
        get list of DECT networks and then details for each network
        """
        networks = self.api.telephony.dect_devices.list_dect_networks()
        network_details = await asyncio.gather(
            *[self.async_api.telephony.dect_devices.dect_network_details(location_id=n.location.id,
                                                                         dect_network_id=n.id)
              for n in networks],
            return_exceptions=True)
        err = None
        for network, details in zip(networks, network_details):
            network: DECTNetworkDetail
            if isinstance(details, Exception):
                err = err or details
                print(f'{network.name} in {network.location.name}: failed to get details, {details}')
                continue
            details: DECTNetworkDetail
        if err is not None:
            raise err

    def test_update_dect_network(self):
        """
        create DECT network and update the DECT network name
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork
            before = api.dect_network_details(location_id=ctx.target_location.location_id,
                                              dect_network_id=ctx.dect_network_id)
            new_name = f'{before.name}changed'
            new_display_name = f'{before.display_name}changed'
            new_display_name = new_display_name[:11]
            new_default_access_code = f'9{before.default_access_code[-3:]}'
            api.update_dect_network(location_id=ctx.target_location.location_id,
                                    dect_network_id=ctx.dect_network_id,
                                    name=new_name,
                                    display_name=new_display_name,
                                    default_access_code_enabled=True,
                                    default_access_code=new_default_access_code)
            after = api.dect_network_details(location_id=ctx.target_location.location_id,
                                             dect_network_id=ctx.dect_network_id)
            self.assertEqual(new_name, after.name)
            self.assertEqual(new_default_access_code, after.default_access_code)
            self.assertTrue(after.default_access_code_enabled)
            self.assertEqual(new_display_name, after.display_name)

    def test_update_dect_network_settings(self):
        """
        create DECT network and update the DECT network name
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork
            before = api.dect_network_details(location_id=ctx.target_location.location_id,
                                              dect_network_id=ctx.dect_network_id)
            new_name = f'{before.name}changed'
            new_display_name = f'{before.display_name}changed'
            new_display_name = new_display_name[:11]
            new_default_access_code = f'9{before.default_access_code[-3:]}'
            # copy current values and update
            settings = before.model_copy(deep=True)
            settings.name = new_name
            settings.display_name = new_display_name
            settings.default_access_code = new_default_access_code
            settings.default_access_code_enabled = True
            api.update_dect_network_settings(settings)
            after = api.dect_network_details(location_id=ctx.target_location.location_id,
                                             dect_network_id=ctx.dect_network_id)
            self.assertEqual(new_name, after.name)
            self.assertEqual(new_default_access_code, after.default_access_code)
            self.assertTrue(after.default_access_code_enabled)
            self.assertEqual(new_display_name, after.display_name)

    def test_delete_dect_network(self):
        """
        Create DECT network, delete it and verify that it's gone
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network(keep=True) as ctx:
            ctx: TestDECTNetwork
            details = api.dect_network_details(location_id=ctx.target_location.location_id,
                                               dect_network_id=ctx.dect_network_id)
            api.delete_dect_network(location_id=details.location.id,
                                    dect_network_id=details.id)
            # getting details is expected to fail
            with self.assertRaises(RestError) as err:
                api.dect_network_details(location_id=ctx.target_location.location_id,
                                         dect_network_id=ctx.dect_network_id)
            rest_error: RestError = err.exception
            self.assertEqual(404, rest_error.response.status_code)
            self.assertEqual(27455, rest_error.code)

            # also the network should not be part of the network list any more
            networks = api.list_dect_networks()
            found = next((n for n in networks if n.id == ctx.dect_network_id), None)
            self.assertIsNone(found)

    def create_base_stations(self, ctx: TestDECTNetwork) -> list[BaseStationResponse]:
        """
        Create a bunch of base stations for test DECT network
        """
        api = self.api.telephony.dect_devices
        dummy_macs = (f'AFFEAFFE{4096 + i:04x}'.upper() for i in range(1, 1000))
        bs_macs = [next(dummy_macs) for _ in range(50)]
        response = api.create_base_stations(location_id=ctx.target_location.location_id,
                                            dect_id=ctx.dect_network_id,
                                            base_station_macs=bs_macs)
        # we should have a response for each mac address
        result_macs = set(r.mac for r in response)
        self.assertTrue(all(mac in result_macs for mac in bs_macs),
                        'not all requested MACs are present in response')

        # all should be successful
        self.assertTrue(all(r.result.status == 201 for r in response),
                        'Not all stations were created')
        return response

    @async_test
    async def test_create_base_stations(self):
        """
        Create a bunch of base stations under a test network
        Then list all base stations and verify existence.
        Finally get details for all created base stations
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork
            response = self.create_base_stations(ctx=ctx)

            # when listing base stations, we should be able to find the ones we just created
            bs_list = api.list_base_stations(location_id=ctx.target_location.location_id,
                                             dect_network_id=ctx.dect_network_id)
            # macs of all generated base stations should be there
            for r in response:
                mac = r.mac
                listed = next((bs for bs in bs_list if bs.mac == mac), None)
                self.assertIsNotNone(listed, f'Missing MAC in list: {mac}')
                self.assertEqual(r.result.id, listed.id, f'inconsistent ID: {r.result.id}-{listed.id}')
            # and finally, we want t be able to get details for all base stations
            as_api = self.async_api.telephony.dect_devices
            all_details = await asyncio.gather(
                *[as_api.base_station_details(location_id=ctx.target_location.location_id,
                                              dect_network_id=ctx.dect_network_id,
                                              base_station_id=r.result.id)
                  for r in response],
                return_exceptions=True)
            self.assertFalse(any(isinstance(details, Exception) for details in all_details),
                             'Failed to get some base station details')

    def test_bulk_delete_base_stations(self):
        """
        Create test network with a bunch of base stations and try to bulk delete all of them
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork
            response = self.create_base_stations(ctx=ctx)
            # get list of base stations
            bs_list = api.list_base_stations(location_id=ctx.target_location.location_id,
                                             dect_network_id=ctx.dect_network_id)
            self.assertEqual(len(response), len(bs_list))
            # bulk delete
            api.delete_bulk_base_stations(location_id=ctx.target_location.location_id,
                                          dect_network_id=ctx.dect_network_id)
            # get list again and verify that all are gone
            bs_list = api.list_base_stations(location_id=ctx.target_location.location_id,
                                             dect_network_id=ctx.dect_network_id)
            self.assertEqual(0, len(bs_list))

    def test_delete_base_station(self):
        """
        Create test network with a bunch of base stations. Then try to delete one of the base stations and verify that
        it's gone
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork
            response = self.create_base_stations(ctx=ctx)
            # get list of base stations
            bs_list = api.list_base_stations(location_id=ctx.target_location.location_id,
                                             dect_network_id=ctx.dect_network_id)
            self.assertEqual(len(response), len(bs_list))
            # delete on base station
            target_bs = random.choice(bs_list)
            target_bs: BaseStationsResponse
            api.delete_base_station(location_id=ctx.target_location.location_id,
                                    dect_network_id=ctx.dect_network_id,
                                    base_station_id=target_bs.id)
            # get list again and verify that target is gone
            bs_list = api.list_base_stations(location_id=ctx.target_location.location_id,
                                             dect_network_id=ctx.dect_network_id)
            self.assertEqual(len(response) - 1, len(bs_list))
            self.assertIsNone(next((bs for bs in bs_list if bs.id == target_bs.id), None))

    def test_add_handset(self):
        """
        Add a handset with a single line
        - list handsets
        - get details of handset just created
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork
            members = list(api.available_members())
            users = [m for m in members if m.member_type == UserType.people]
            user_for_1st_line = random.choice(users)
            user_for_1st_line: AvailableMember
            dect = {'location_id': ctx.target_location.location_id,
                    'dect_network_id': ctx.dect_network_id}
            api.add_a_handset(**dect,
                              line1_member_id=user_for_1st_line.member_id,
                              custom_display_name=user_for_1st_line.last_name)
            handsets = api.list_handsets(**dect)
            self.assertEqual(1, len(handsets.handsets))
            self.assertEqual(1, handsets.number_of_handsets_assigned)
            self.assertEqual(1, handsets.number_of_lines_assigned)
            handset = handsets.handsets[0]
            self.assertEqual(1, len(handset.lines))
            hs_details = api.handset_details(**dect, handset_id=handset.id)
            foo = 1

    def test_add_handset_two_members(self):
        """
        Add a handset with two lines
        - list handsets
        - get details of handset just created
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork
            members = list(api.available_members())
            users = [m for m in members if m.member_type == UserType.people]
            random.shuffle(users)
            user_for_1st_line, user_for_2nd_line = users[:2]
            user_for_1st_line: AvailableMember
            user_for_2nd_line: AvailableMember
            dect = {'location_id': ctx.target_location.location_id,
                    'dect_network_id': ctx.dect_network_id}
            with self.assertRaises(RestError) as exc:
                api.add_a_handset(**dect,
                                  line1_member_id=user_for_1st_line.member_id,
                                  line2_member_id=user_for_2nd_line.member_id,
                                  custom_display_name=user_for_1st_line.last_name)
            err: RestError = exc.exception
            if err.response.status_code == 400 and err.code == 5302:
                # com.broadsoft.components.nssynch.NSSynchronizationException
                # --> Try to create with one member and add 2nd member later
                api.add_a_handset(**dect,
                                  line1_member_id=user_for_1st_line.member_id,
                                  custom_display_name=user_for_1st_line.last_name)
                new_handset = next(hs
                                   for hs in api.list_handsets(**dect,
                                                               member_id=user_for_1st_line.member_id).handsets
                                   if hs.lines[0].member_id == user_for_1st_line.member_id)
                api.update_handset(**dect, handset_id=new_handset.id,
                                   line1_member_id=user_for_1st_line.member_id,
                                   line2_member_id=user_for_2nd_line.member_id,
                                   custom_display_name=user_for_1st_line.last_name)
                print('Creating handset with two members failed but creating handset with one member and then '
                      'adding 2nd member worked')
            handsets = api.list_handsets(**dect)
            self.assertEqual(1, len(handsets.handsets))
            self.assertEqual(1, handsets.number_of_handsets_assigned)
            self.assertEqual(2, handsets.number_of_lines_assigned)
            handset = handsets.handsets[0]
            self.assertEqual(2, len(handset.lines))
            hs_details = api.handset_details(**dect, handset_id=handset.id)
            # raise error for now; can be removed if we don't run in to an exception anymore when creating handset
            # with two members
            raise err

    def test_handset_details(self):
        ...

    def test_update_handset(self):
        ...

    def test_add_and_remove_2nd_line_to_from_handset(self):
        """
        Create a handset with a single line
        - verify created handset
        - add 2nd line and verify
        - remove 2nd line and verify
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork
            members = list(api.available_members())
            users = [m for m in members if m.member_type == UserType.people]
            random.shuffle(users)
            user_for_1st_line, user_for_2nd_line = users[:2]
            user_for_1st_line: AvailableMember
            user_for_2nd_line: AvailableMember
            dect = {'location_id': ctx.target_location.location_id,
                    'dect_network_id': ctx.dect_network_id}
            api.add_a_handset(**dect,
                              line1_member_id=user_for_1st_line.member_id,
                              custom_display_name=user_for_1st_line.last_name)
            handsets = api.list_handsets(**dect)
            self.assertEqual(1, len(handsets.handsets))
            self.assertEqual(1, handsets.number_of_handsets_assigned)
            self.assertEqual(1, handsets.number_of_lines_assigned)
            handset = handsets.handsets[0]
            self.assertEqual(1, len(handset.lines))
            # add 2nd line and verify
            api.update_handset(**dect, handset_id=handset.id, line1_member_id=user_for_1st_line.member_id,
                               line2_member_id=user_for_2nd_line.member_id,
                               custom_display_name=handset.custom_display_name)
            hs_details = api.handset_details(**dect, handset_id=handset.id)
            self.assertEqual(2, len(hs_details.lines))

            # remove 2nd line and verify
            api.update_handset(**dect, handset_id=handset.id, line1_member_id=user_for_1st_line.member_id,
                               custom_display_name=handset.custom_display_name)
            hs_details = api.handset_details(**dect, handset_id=handset.id)
            self.assertEqual(1, len(hs_details.lines))

    def create_handsets(self, ctx: TestDECTNetwork, hs_count: int,
                        member_type: UserType = UserType.people) -> list[DECTHandsetItem]:
        """
        Create a bunch of hansets and return the list of handsets
        """
        api = self.api.telephony.dect_devices
        members = api.available_members()
        target_members = [m for m in members if m.member_type == member_type]
        if hs_count > len(target_members):
            self.skipTest(f"Not enough {member_type} targets")
        random.shuffle(target_members)

        dect = {'location_id': ctx.target_location.location_id,
                'dect_network_id': ctx.dect_network_id}

        def create_hs(m: AvailableMember):
            api.add_a_handset(**dect, line1_member_id=m.member_id,
                              custom_display_name=m.last_name)

        with ThreadPoolExecutor() as pool:
            list(pool.map(create_hs, target_members[:hs_count]))
        handsets = api.list_handsets(**dect)
        return handsets.handsets

    def test_delete_handset(self):
        """
        Create some handsets, delete a random handset and verify that the handset is gone
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork

            # create some handsets
            handsets = self.create_handsets(ctx=ctx, hs_count=5)

            # pick one and delete it
            target_handset = random.choice(handsets)
            target_handset: DECTHandsetItem
            dect = {'location_id': ctx.target_location.location_id,
                    'dect_network_id': ctx.dect_network_id}
            api.delete_handset(**dect, handset_id=target_handset.id)

            # verify that the handset is gone
            handsets_after = api.list_handsets(**dect)
            self.assertEqual(len(handsets) - 1, len(handsets_after.handsets))
            self.assertIsNone(next((hs
                                    for hs in handsets_after.handsets
                                    if hs.id == target_handset.id),
                                   None))

    def test_delete_handsets(self):
        """
        Create some handsets and delete a subset
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork

            # create some handsets
            handsets = self.create_handsets(ctx=ctx, hs_count=5)
            random.shuffle(handsets)

            # pick three handsets to delete
            handsets_to_delete = handsets[:3]
            dect = {'location_id': ctx.target_location.location_id,
                    'dect_network_id': ctx.dect_network_id}

            ids_to_delete = list(map(attrgetter('id'), handsets_to_delete))
            api.delete_handsets(**dect, handset_ids=ids_to_delete, delete_all=False)

            # verify that the handsets are gone
            handsets_after = api.list_handsets(**dect)
            self.assertEqual(len(handsets) - 3, len(handsets_after.handsets))
            self.assertFalse(set(ids_to_delete) & set(map(attrgetter('id'), handsets_after.handsets)),
                             'Not all handsets are gone')

    def test_delete_handsets_all(self):
        """
        Create some handsets and delete aall
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork

            # create some handsets
            handsets = self.create_handsets(ctx=ctx, hs_count=5)
            random.shuffle(handsets)

            dect = {'location_id': ctx.target_location.location_id,
                    'dect_network_id': ctx.dect_network_id}
            api.delete_handsets(**dect, handset_ids=[], delete_all=True)

            # verify that the handsets are gone
            handsets_after = api.list_handsets(**dect)
            self.assertEqual(0, len(handsets_after.handsets))

    def test_networks_associated_with_person(self):
        """
        Create some handsets and see if we can find the associated nwtwork for persons assigned to lines on the handsets
        """
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork

            # create some handsets
            handsets = self.create_handsets(ctx=ctx, hs_count=5)
            random.shuffle(handsets)

            person_ids = list(chain.from_iterable((l.member_id for l in hs.lines) for hs in handsets))
            with ThreadPoolExecutor() as pool:
                networks = list(pool.map(api.dect_networks_associated_with_person, person_ids))
            networks: list[list[DECTNetworkDetail]]
            # for each user "our" network needs to be in the list of networks
            self.assertTrue(all(ctx.dect_network_id in set(nw.id for nw in network_list)
                                for network_list in networks))

    def test_networks_associated_with_workspace(self):
        raise NotImplementedError()

    def test_networks_associated_with_virtual_line(self):
        """
        Create one handset with virtual line and see if we can find the associated network for virtual_line assigned
        to line on the handset
        """
        # verify DECT network list for virtual line
        api = self.api.telephony.dect_devices
        with self.create_test_dect_network() as ctx:
            ctx: TestDECTNetwork

            # create handset with user as primary line
            handsets = self.create_handsets(ctx=ctx, hs_count=1)

            handset = handsets[0]
            vl_list = list(self.api.telephony.virtual_lines.list())
            target_vl: VirtualLine = random.choice(vl_list)

            # assign virtual line as secondary line
            dect = {'location_id': ctx.target_location.location_id,
                    'dect_network_id': ctx.dect_network_id}
            api.update_handset(**dect, handset_id=handset.id, line1_member_id=handset.lines[0].member_id,
                               custom_display_name=handset.custom_display_name,
                               line2_member_id=target_vl.id)
            details_after = api.handset_details(**dect, handset_id=handset.id)
            self.assertEqual(2, len(details_after.lines))
            self.assertEqual(target_vl.id, details_after.lines[1].member_id)

            vl_network_list = api.dect_networks_associated_with_virtual_line(virtual_line_id=target_vl.id)
            self.assertTrue(ctx.dect_network_id in set(n.id for n in vl_network_list))

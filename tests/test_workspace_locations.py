import asyncio
import base64
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from itertools import chain

from randomlocation import RandomLocation, Address

from tests.base import TestCaseWithLog
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.rest import RestError
from wxc_sdk.workspace_locations import WorkspaceLocation


class TestWorkspaceLocations(TestCaseWithLog):

    @staticmethod
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

    def create_random_wsl(self) -> WorkspaceLocation:
        """
        create a random workspace location
        """
        address = self.random_address()

        # get a unique display name
        display_name_prefix = f'{address.city}, {address.address1}'
        wsl_list = self.api.workspace_locations.list()
        display_names = set(wsl.display_name for wsl in wsl_list)
        display_name = next(dpn
                            for suffix in chain([''],
                                                (f'_{i:02}'
                                                 for i in range(1, 99)))
                            if (dpn := f'{display_name_prefix}{suffix}') not in display_names)

        wsl = self.api.workspace_locations.create(display_name=display_name, address=str(address),
                                                  country_code='US', longitude=address.geo_location.lon,
                                                  latitude=address.geo_location.lat, city_name=address.city)
        return wsl

    def test_001_list(self):
        """
        list workspace locations
        """
        wsl = list(self.api.workspace_locations.list())
        print(f'Got {len(wsl)} workspace locations')

    def test_002_list_w_org_id(self):
        """
        list workspace locations
        """
        with self.no_log():
            me = self.api.people.me()
        print(f'Org id: {webex_id_to_uuid(me.org_id)}')
        wsl = list(self.api.workspace_locations.list(org_id=me.org_id))
        print(f'Got {len(wsl)} workspace locations')
        print('Base64 decoded IDs:')
        print('\n'.join(base64.b64decode(f'{w.id}').decode() for w in wsl))

    def test_003_list_wrong_org_id(self):
        """
        list workspace locations for random org id
        """
        with self.no_log():
            me = self.api.people.me()
        org_id = base64.b64decode(me.org_id + '==').decode()
        fake_org_id = '/'.join(org_id.split('/')[:-1])
        fake_org_id = f'{fake_org_id}/{uuid.uuid4()}'
        fake_org_id = base64.b64encode(fake_org_id.encode()).decode().strip('=')
        with self.assertRaises(RestError) as raised:
            list(self.api.workspace_locations.list(org_id=fake_org_id))
        rest_error: RestError = raised.exception
        self.assertEqual(403, rest_error.response.status_code)

    def test_004_create(self):
        """
        test creation
        """
        wsl = self.create_random_wsl()
        print(f'Created new workplace location: {wsl}')

    def test_005_details(self):
        """
        Get details for all workspace locations
        """
        wsl_list = list(self.api.workspace_locations.list())
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda wsl: self.api.workspace_locations.details(location_id=wsl.id),
                                    wsl_list))
        print(f'Got details for {len(wsl_list)} workspace locations')

    def test_006_update(self):
        """
        Try to update a workspace location
        """
        wsl = self.create_random_wsl()
        try:
            update = wsl.copy(deep=True)
            notes = f'Random text {uuid.uuid4()}'
            update.notes = notes
            update_result = self.api.workspace_locations.update(location_id=wsl.id, settings=update)
            after = self.api.workspace_locations.details(location_id=wsl.id)
            self.assertEqual(update_result, after)
            self.assertEqual(notes, update_result.notes)
            after.notes = wsl.notes
            self.assertEqual(wsl, after)
        finally:
            # delete the workspace location again
            self.api.workspace_locations.delete(location_id=wsl.id)

    def test_007_clear_notes(self):
        """
        Try to update a workspace location and clear the notes
        """
        wsl = self.create_random_wsl()
        try:
            notes = f'Random text {uuid.uuid4()}'
            wsl.notes = notes
            with_notes = self.api.workspace_locations.update(location_id=wsl.id, settings=wsl)
            self.assertEqual(notes, with_notes.notes)
            # now try to clear notes
            update = with_notes.copy(deep=True)
            update.notes = None
            after = self.api.workspace_locations.update(location_id=wsl.id, settings=update)
            self.assertIsNone(after.notes)
        finally:
            # delete the workspace location again
            self.api.workspace_locations.delete(location_id=wsl.id)

    @contextmanager
    def temp_location(self):
        with self.no_log():
            wsl = self.create_random_wsl()
        try:
            yield wsl
        finally:
            with self.no_log():
                self.api.workspace_locations.delete(location_id=wsl.id)

    def test_008_list_floors_new_location(self):
        """
        List floors of new location
        """
        with self.temp_location() as wsl:
            wsl: WorkspaceLocation
            floors = list(self.api.workspace_locations.floors.list(location_id=wsl.id))
            self.assertEqual(list(), floors)

    def test_008_create_some_floors(self):
        """
        create some floors in a location
        """
        with self.temp_location() as wsl:
            wsl: WorkspaceLocation
            for i in range(1, 11):
                self.api.workspace_locations.floors.create(
                    location_id=wsl.id,
                    floor_number=i,
                    display_name=f'{i}. floor')
            listed_floors = list(self.api.workspace_locations.floors.list(location_id=wsl.id))
            self.assertEqual(10, len(listed_floors))

    def test_009_update_floor(self):
        """
        update a floor
        """
        with self.temp_location() as wsl:
            wsl: WorkspaceLocation
            floor = self.api.workspace_locations.floors.create(location_id=wsl.id,
                                                               floor_number=1,
                                                               display_name='1st floor')
            try:
                new_dn = 'foo'
                update = floor.copy(deep=True)
                update.display_name = new_dn
                updated = self.api.workspace_locations.floors.update(location_id=wsl.id,
                                                                     floor_id=floor.id,
                                                                     settings=update)
                self.assertEqual(new_dn, updated.display_name)
            finally:
                self.api.workspace_locations.floors.delete(location_id=wsl.id,
                                                           floor_id=floor.id)
                floors = list(self.api.workspace_locations.floors.list(location_id=wsl.id))
                self.assertEqual(list(), floors)

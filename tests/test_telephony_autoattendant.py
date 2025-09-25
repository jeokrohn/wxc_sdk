"""
Tests for auto attendants
"""
import asyncio
import json
# TODO: additional tests
import random
from contextlib import contextmanager
from itertools import chain

from tests.base import TestCaseWithLog, TestWithLocations, async_test
from tests.testutil import available_extensions_gen, new_aa_names
from wxc_sdk.all_types import AutoAttendant, ScheduleType
from wxc_sdk.common import AnnouncementLevel
from wxc_sdk.common.schedules import Schedule
from wxc_sdk.locations import Location
from wxc_sdk.telephony.announcements_repo import RepoAnnouncement
from wxc_sdk.telephony.autoattendant import AutoAttendantMenu, AutoAttendantKeyConfiguration, MenuKey, \
    AutoAttendantAction
from wxc_sdk.telephony.location import TelephonyLocation


class TestAutoAttendant(TestCaseWithLog):
    """
    List all auto attendants
    """

    def test_001_list(self):
        """
        List all auto attendants
        """
        aa_list = list(self.api.telephony.auto_attendant.list())
        print(f'got {len(aa_list)} auto attendants')
        print('\n'.join(f'{aa}' for aa in aa_list))

    @async_test
    async def test_002_details(self):
        """
        Get details of all auto attendants
        """
        aa_list = await self.async_api.telephony.auto_attendant.list()
        if not aa_list:
            self.skipTest('No existing auto attendants')
        ata = self.async_api.telephony.auto_attendant
        details = await asyncio.gather(*[ata.details(location_id=aa.location_id,
                                                     auto_attendant_id=aa.auto_attendant_id)
                                         for aa in aa_list])
        print(f'got details for {len(aa_list)} auto attendants')
        print('\n'.join(f'{aa}' for aa in details))


class TestCreate(TestWithLocations):

    @contextmanager
    def get_schedule(self, location: Location) -> Schedule:
        """
        Get or create schedule
        :return:
        """
        schedules = list(self.api.telephony.schedules.list(obj_id=location.location_id,
                                                           schedule_type=ScheduleType.business_hours))
        if schedules:
            # we prefer schedule "workday"
            target_schedule = next((schedule for schedule in schedules
                                    if schedule.name == 'workday'), None)

            # .. but are ok with any other scheduled if that doesn't exist
            target_schedule = target_schedule or schedules[0]
            yield target_schedule
        else:
            schedule_id = self.api.telephony.schedules.create(obj_id=location.location_id,
                                                              schedule=Schedule.business(name='business'))
            target_schedule = self.api.telephony.schedules.details(obj_id=location.location_id,
                                                                   schedule_type=ScheduleType.business_hours,
                                                                   schedule_id=schedule_id)
            try:
                yield target_schedule
            finally:
                self.api.telephony.schedules.delete_schedule(obj_id=location.location_id,
                                                             schedule_type=ScheduleType.business_hours,
                                                             schedule_id=schedule_id)

    @contextmanager
    def create_aa(self):
        """
        Create a new auto attendant in a random location
        """
        target_location = random.choice(self.telephony_locations)
        with self.get_schedule(location=target_location) as target_schedule:
            target_schedule: Schedule

            # shortcut
            ata = self.api.telephony.auto_attendant

            # get an available name and extension for the new auto attendant
            with self.no_log():
                new_name = next(new_aa_names(api=self.api))
                extension = next(available_extensions_gen(api=self.api, location_id=target_location.location_id))

            print(f'creating AA "{new_name}" ({extension}) with schedule "{target_schedule.name}" '
                  f'in location "{target_location.name}"...')
            aa_settings = AutoAttendant.create(name=new_name,
                                               business_schedule=target_schedule.name,
                                               extension=extension)
            aa_id = ata.create(location_id=target_location.location_id,
                               settings=aa_settings)
            details = ata.details(location_id=target_location.location_id, auto_attendant_id=aa_id)
            try:
                yield target_location.location_id, details
            finally:
                # clean up, remove AA again
                ata.delete_auto_attendant(location_id=target_location.location_id,
                                          auto_attendant_id=aa_id)
            return

    def test_001_create(self):
        """
        Create a simple AA in a random location
        """
        with self.create_aa() as (location_id, details):
            print(json.dumps(json.loads(details.model_dump_json()), indent=2))
            print(f'Created AA: {details.location_id}')


class TestUpdate(TestCreate):
    def test_update_menu(self):
        """
        Add a menu key to an existing auto attendant and then remove it again
        """
        ata = self.api.telephony.auto_attendant
        with self.create_aa() as (location_id, details):
            location_id: str
            details: AutoAttendant
            print(f'Adding menu key to AA "{details.name}" ({details.auto_attendant_id})')

            # create a new menu with a key configuration
            new_menu = details.business_hours_menu.model_copy(deep=True)
            new_menu: AutoAttendantMenu
            new_menu.key_configurations = [
                AutoAttendantKeyConfiguration(key=MenuKey.zero, action=AutoAttendantAction.repeat_menu,
                                              description='Repeat menu'),
                AutoAttendantKeyConfiguration(key=MenuKey.one,
                                              action=AutoAttendantAction.exit,
                                              description='Exit')]
            new_settings = details.model_copy(deep=True)
            new_settings.business_hours_menu = new_menu
            ata.update(location_id=location_id, auto_attendant_id=details.auto_attendant_id, settings=new_settings)
            after = ata.details(location_id=location_id, auto_attendant_id=details.auto_attendant_id)
            self.assertEqual(new_menu, after.business_hours_menu)

            # go back to the original menu
            ata.update(location_id=location_id, auto_attendant_id=details.auto_attendant_id, settings=details)
            after = ata.details(location_id=location_id, auto_attendant_id=details.auto_attendant_id)
            self.assertEqual(details.business_hours_menu, after.business_hours_menu)

        return


class TestDelete(TestCaseWithLog):

    def test_001_delete(self):
        """
        Delete a random "aa_*" auto attendant
        :return:
        """
        ata = self.api.telephony.auto_attendant
        aa_list = list(ata.list(name='aa_'))
        if not aa_list:
            self.skipTest('No existing auto attendant "aa_*"')
        target_aa = random.choice(aa_list)
        print(f'Deleting aa "{target_aa.name}" in location "{target_aa.location_name}"')
        ata.delete_auto_attendant(location_id=target_aa.location_id, auto_attendant_id=target_aa.auto_attendant_id)


class TestAnnouncementFiles(TestCaseWithLog):
    """
    List announcement files
    """

    @async_test
    async def test_001_list_ann_files(self):
        """
        List announcement files for all existing auto attendants
        """
        aa_list = list(self.api.telephony.auto_attendant.list())
        if not aa_list:
            self.skipTest('No existing auto attendants')

        location_ids_set = sorted({aa.location_id for aa in aa_list})
        locations: dict[str, TelephonyLocation] = {loc.location_id: loc for loc in self.api.telephony.location.list()}

        # get global and location announcements (only for locations with auto attendants)
        global_announcements, loc_announcements_list = await asyncio.gather(
            self.async_api.telephony.announcements_repo.list(),
            asyncio.gather(*[self.async_api.telephony.announcements_repo.list(
                location_id=location_id)
                for location_id in location_ids_set]))
        global_announcements: list[RepoAnnouncement]
        loc_announcements_list: list[list[RepoAnnouncement]]

        announcements_for_location: dict[str, list[RepoAnnouncement]] = {loc_id: loc_anns
                                                                         for loc_id, loc_anns in zip(location_ids_set,
                                                                                                     loc_announcements_list)}

        aa_files_list = await asyncio.gather(*[self.async_api.telephony.auto_attendant.list_announcement_files(
            location_id=aa.location_id, auto_attendant_id=aa.auto_attendant_id) for aa in aa_list])
        aa_files_list: list[list[RepoAnnouncement]]
        aa_file_id_set = {af.id for af in chain.from_iterable(aa_files_list)}

        print(f'Unique announcement files: {len(aa_file_id_set)}')
        err = None
        loc_len = max(len(locations[loc_id].name) for loc_id in location_ids_set)
        aa_len = max(len(aa.name) for aa in aa_list)
        for aa, af_files in zip(aa_list, aa_files_list):
            location = locations[aa.location_id]
            loc_announcements = announcements_for_location[aa.location_id]
            af_files_org = [af for af in af_files if af.level == AnnouncementLevel.organization.value]
            af_files_loc = [af for af in af_files if af.level == AnnouncementLevel.location.value]

            print(
                f'{aa.name:{aa_len}} in {location.name:{loc_len}}: {len(af_files)} files ({len(af_files_org)} org, '
                f'{len(af_files_loc)} loc) {len(loc_announcements)} existing location announcements')
            try:
                # number of available announcements must be equal to the number of org + location announcements
                self.assertEqual(len(af_files), len(af_files_org) + len(af_files_loc))
            except AssertionError as e:
                err = err or e
        if err:
            raise err

"""
Tests for auto attendants
"""
import asyncio
import json
# TODO: additional tests
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from wxc_sdk.all_types import AutoAttendant, ScheduleType
from wxc_sdk.common.schedules import Schedule
from wxc_sdk.locations import Location
from tests.base import TestCaseWithLog, TestWithLocations, async_test
from tests.testutil import available_extensions_gen


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

    def test_001_create(self):
        """
        Create a simple AA in a random location
        """
        target_location = random.choice(self.locations)
        with self.get_schedule(location=target_location) as target_schedule:
            target_schedule: Schedule

            # shortcut
            ata = self.api.telephony.auto_attendant

            # get an available name for the new auto attendant
            existing_aa = list(ata.list(location_id=target_location.location_id))
            names = set(aa.name for aa in existing_aa)
            new_name = next(name for i in range(1000)
                            if (name := f'aa_{i:03}') not in names)

            extension = next(available_extensions_gen(api=self.api, location_id=target_location.location_id))

            print(f'creating AA "{new_name}" ({extension}) with schedule "{target_schedule.name}" '
                  f'in location "{target_location.name}"...')
            aa_settings = AutoAttendant.create(name=new_name,
                                               business_schedule=target_schedule.name,
                                               extension=extension)
            aa_id = ata.create(location_id=target_location.location_id,
                               settings=aa_settings)
            details = ata.details(location_id=target_location.location_id, auto_attendant_id=aa_id)
            print(json.dumps(json.loads(details.model_dump_json()), indent=2))
            print(f'Created AA: {aa_id}')

            # clean up, remove AA again
            ata.delete_auto_attendant(location_id=target_location.location_id,
                                      auto_attendant_id=aa_id)


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


class TestForwarding(TestCaseWithLog):

    def test_001_get_all_forwarding_settings(self):
        """
        get forwarding settings for all auto attendants
        """
        ata = self.api.telephony.auto_attendant
        aa_list = list(ata.list(name='aa_'))
        with ThreadPoolExecutor() as pool:
            forwarding_settings = list(pool.map(
                lambda aa: ata.forwarding.settings(location_id=aa.location_id, feature_id=aa.auto_attendant_id),
                aa_list))
        print(f'Got forwarding settings for {len(forwarding_settings)} auto attendants.')

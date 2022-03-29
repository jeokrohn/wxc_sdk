"""
Tests for auto attendants
"""
import json
# TODO: additional tests
import random
from concurrent.futures import ThreadPoolExecutor

from wxc_sdk.telephony.autoattendant import AutoAttendant
from wxc_sdk.telephony.schedules import ScheduleType
from .base import TestCaseWithLog, TestWithLocations


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

    def test_002_details(self):
        """
        Get details of all auto attendants
        """
        aa_list = list(self.api.telephony.auto_attendant.list())
        if not aa_list:
            self.skipTest('No existing auto attendants')
        ata = self.api.telephony.auto_attendant
        with ThreadPoolExecutor() as pool:
            aa = aa_list[0]
            ata.details(location_id=aa.location_id, auto_attendant_id=aa.auto_attendant_id)
            details = list(pool.map(
                lambda aa: ata.details(location_id=aa.location_id, auto_attendant_id=aa.auto_attendant_id),
                aa_list))
        print(f'got details for {len(aa_list)} auto attendants')
        print('\n'.join(f'{aa}' for aa in details))


class TestCreate(TestWithLocations):

    def test_001_create(self):
        """
        Create a simple AA in a random location
        """
        target_location = random.choice(self.locations)
        schedules = list(self.api.telephony.schedules.list(location_id=target_location.location_id,
                                                           schedule_type=ScheduleType.business_hours))
        if not schedules:
            self.skipTest(f'No business hours schedule in location "{target_location.name}"')
        # we prefer schedule "workday"
        target_schedule = next((schedule for schedule in schedules
                                if schedule.name == 'workday'), None)

        # .. but are ok with any other scheduled if that doesn't exist
        target_schedule = target_schedule or schedules[0]

        # shortcut
        ata = self.api.telephony.auto_attendant

        # get an available name for the new auto attendant
        existing_aa = list(ata.list(location_id=target_location.location_id))
        names = set(aa.name for aa in existing_aa)
        new_name = next(name for i in range(1000)
                        if (name := f'aa_{i:03}') not in names)

        # for simplicity we just assume that auto attendants can use extension 9XXX
        extension = str(9000 + int(new_name[-3:]))

        print(f'creating AA "{new_name}" ({extension}) witch scheduled "{target_schedule.name}" '
              f'in location "{target_location.name}"...')
        aa_settings = AutoAttendant.create(name=new_name,
                                           business_schedule=target_schedule.name,
                                           extension=extension)
        aa_id = ata.create(location_id=target_location.location_id,
                           settings=aa_settings)
        details = ata.details(location_id=target_location.location_id, auto_attendant_id=aa_id)
        print(json.dumps(json.loads(details.json()), indent=2))
        print(f'Created AA: {aa_id}')


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

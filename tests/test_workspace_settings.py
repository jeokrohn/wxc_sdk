"""
Webex Calling Workspace settings
"""
import asyncio
import random
from contextlib import contextmanager
from dataclasses import dataclass
from typing import ClassVar

from tests.base import TestCaseWithLog, async_test, TestWithLocations
from tests.testutil import create_workspace_with_webex_calling
from wxc_sdk.common.schedules import ScheduleType, Schedule
from wxc_sdk.licenses import License
from wxc_sdk.locations import Location
from wxc_sdk.person_settings import TelephonyDevice
from wxc_sdk.person_settings.sequential_ring import SequentialRing, SequentialRingNumber, SequentialRingCriteria, \
    Source, SequentialRingCallsFrom, RingCriteriaScheduleLevel
from wxc_sdk.workspace_settings.numbers import WorkspaceNumbers
from wxc_sdk.workspaces import Workspace, CallingType, WorkspaceSupportedDevices


class TestWorkspaceSettings(TestCaseWithLog):

    @async_test
    async def test_001_list_devices(self):
        """
        Get list of devices in all workspaces
        """
        workspaces = list(self.api.workspaces.list())
        workspaces = [ws for ws in workspaces if ws.calling and ws.calling.type == CallingType.webex]
        if not workspaces:
            self.skipTest('No workspaces with calling type webex')
        device_lists = await asyncio.gather(*[self.async_api.workspace_settings.devices.list(ws.workspace_id)
                                              for ws in workspaces],
                                            return_exceptions=True)
        for ws, devices in zip(workspaces, device_lists):
            ws: Workspace
            print(f'workspace "{ws.display_name}", calling type: {ws.calling.type}')
            if isinstance(devices, Exception):
                print(f'  failed to get device list: {devices}')
                continue
            devices: list[TelephonyDevice]
            if not devices:
                print('  no devices')
                continue
            for device in devices:
                print(f'  - {device.model} {device.activation_state} {device.mac or "no MAC"} '
                      f'{device.ip_address or "no ip address"}')
        self.assertFalse(any(isinstance(dl, Exception) for dl in device_lists))

    @async_test
    async def test_002_numbers(self):
        """
        Get numbers for all workspaces
        """
        workspaces = list(self.api.workspaces.list())
        workspaces = [ws for ws in workspaces if ws.calling and ws.calling.type == CallingType.webex]
        if not workspaces:
            self.skipTest('No workspaces with calling type webex')
        number_lists = await asyncio.gather(*[self.async_api.workspace_settings.numbers.read(ws.workspace_id)
                                              for ws in workspaces],
                                            return_exceptions=True)

        for ws, numbers in zip(workspaces, number_lists):
            ws: Workspace
            print(f'workspace "{ws.display_name}"')
            if isinstance(numbers, Exception):
                print(f'  failed to get number list: {numbers}')
                continue
            numbers: WorkspaceNumbers
            if not numbers.phone_numbers:
                print('  no phone numbers')
                continue
            for pn in numbers.phone_numbers:
                print(f'  - {pn.extension or "no extension"} {pn.external or "no TN"}')
        self.assertFalse(any(isinstance(nl, Exception) for nl in number_lists))


@dataclass(init=False)
class TestWithProfessionalWorkspace(TestWithLocations):
    """
    Tests for workspace settings using a temporary professional workspace
    """
    # temporary workspace with professional license
    workspace: ClassVar[Workspace] = None
    location: ClassVar[Location] = None

    @classmethod
    def create_temp_workspace(cls):
        """
        Create a temporary workspace with professional license
        """
        # get pro license
        pro_license = next((lic
                            for lic in cls.api.licenses.list()
                            if lic.webex_calling_professional and lic.consumed_units < lic.total_units),
                           None)
        if pro_license:
            pro_license: License
            # create WS in random location
            location = random.choice(cls.locations)
            cls.location = location
            workspace = create_workspace_with_webex_calling(api=cls.api,
                                                            target_location=location,
                                                            # workspace_location_id=wsl.id,
                                                            supported_devices=WorkspaceSupportedDevices.phones,
                                                            notes=f'temp location for professional workspace tests, '
                                                                  f'location "{location.name}"',
                                                            license=pro_license)
            cls.workspace = workspace

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.create_temp_workspace()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if cls.workspace:
            cls.api.workspaces.delete_workspace(cls.workspace.workspace_id)

    def setUp(self) -> None:
        super().setUp()
        self.assertIsNotNone(self.workspace, 'No professional workspace created')

    def test_read_anon_calls(self):
        api = self.api.workspace_settings.anon_calls
        api.read(self.workspace.workspace_id)

    def test_configure_anon_calls(self):
        api = self.api.workspace_settings.anon_calls
        r = api.read(self.workspace.workspace_id)
        api.configure(self.workspace.workspace_id, not r)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(not r, after)

    def test_read_dnd(self):
        api = self.api.workspace_settings.dnd
        api.read(self.workspace.workspace_id)

    def test_configure_dnd(self):
        api = self.api.workspace_settings.dnd
        r = api.read(self.workspace.workspace_id)
        update = r.model_copy(deep=True)
        update.enabled = not r.enabled
        api.configure(self.workspace.workspace_id, update)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(update, after)

    def test_read_call_bridge(self):
        api = self.api.workspace_settings.call_bridge
        api.read(self.workspace.workspace_id)

    def test_configure_call_bridge(self):
        api = self.api.workspace_settings.call_bridge
        r = api.read(self.workspace.workspace_id)
        update = r.model_copy(deep=True)
        update.warning_tone_enabled = not r.warning_tone_enabled
        api.configure(self.workspace.workspace_id, update)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(update, after)

    def test_read_ptt(self):
        api = self.api.workspace_settings.push_to_talk
        api.read(self.workspace.workspace_id)

    def test_configure_ptt(self):
        api = self.api.workspace_settings.push_to_talk
        r = api.read(self.workspace.workspace_id)
        update = r.model_copy(deep=True)
        update.allow_auto_answer = not r.allow_auto_answer
        api.configure(self.workspace.workspace_id, update)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(update, after)

    def test_read_voicemail(self):
        api = self.api.workspace_settings.voicemail
        api.read(self.workspace.workspace_id)

    def test_configure_voicemail(self):
        api = self.api.workspace_settings.voicemail
        r = api.read(self.workspace.workspace_id)
        update = r.model_copy(deep=True)
        update.enabled = not r.enabled
        api.configure(self.workspace.workspace_id, update)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(update, after)

    def test_sequential_ring_criteria_create(self):
        """
        create criteria
        """
        api = self.api.workspace_settings.sequential_ring
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        criteria = SequentialRingCriteria(calls_from=SequentialRingCallsFrom.any_phone_number, ring_enabled=True)
        criteria_id = api.create_criteria(self.workspace.workspace_id, criteria)
        try:
            details = api.read_criteria(self.workspace.workspace_id, criteria_id)
            self.assertEqual(criteria.calls_from, details.calls_from)
            self.assertEqual(criteria.ring_enabled, details.ring_enabled)

            # also there should be one criteria in the details
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(1, len(after.criteria))
        finally:
            # clean up: delete criteria again
            api.delete_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(after.criteria))

    def test_sequential_ring_criteria_create_with_phone_number(self):
        """
        create criteria with phone numbers
        """
        api = self.api.workspace_settings.sequential_ring
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SequentialRingCriteria(calls_from=SequentialRingCallsFrom.select_phone_numbers, ring_enabled=True,
                                          phone_numbers=phone_numbers,
                                          anonymous_callers_enabled=False,
                                          unavailable_callers_enabled=False)
        criteria_id = api.create_criteria(self.workspace.workspace_id, criteria)
        try:
            details = api.read_criteria(self.workspace.workspace_id, criteria_id)
            details_with_cleaned_phone_number = details.model_copy(deep=True)
            details_with_cleaned_phone_number.phone_numbers = \
                [pn.replace('-', '')
                 for pn in details_with_cleaned_phone_number.phone_numbers]
            criteria.id = details.id
            self.assertEqual(criteria, details_with_cleaned_phone_number)

            # also there should be one criteria in the details
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(1, len(after.criteria))

            # ... and the numbers are somewhat screwed up
            self.assertTrue(all(pn == pn_after
                                for pn, pn_after in zip(phone_numbers,
                                                        details.phone_numbers)),
                            f'phone numbers in criteria and details are not equal: '
                            f'{", ".join(details.phone_numbers)}')

        finally:
            # clean up: delete criteria again
            api.delete_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(after.criteria))

    def test_sequential_ring_criteria_add_phone_number(self):
        """
        create criteria and add phone number
        """
        api = self.api.workspace_settings.sequential_ring
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SequentialRingCriteria(calls_from=SequentialRingCallsFrom.select_phone_numbers, ring_enabled=True,
                                          phone_numbers=phone_numbers,
                                          anonymous_callers_enabled=False,
                                          unavailable_callers_enabled=False)
        criteria_id = api.create_criteria(self.workspace.workspace_id, criteria)
        try:
            details = api.read_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            criteria.id = details.id
            self.assertEqual(2, len(details.phone_numbers))
            # also there should be one criteria in the details
            self.assertEqual(1, len(after.criteria))

            # now, let's try to add a phone numbers
            phone_numbers.append('+4961007739767')
            update = details.model_copy(deep=True)
            update.phone_numbers = phone_numbers
            api.configure_criteria(self.workspace.workspace_id, criteria_id, update)
            criteria_after = api.read_criteria(self.workspace.workspace_id, criteria_id)
            self.assertEqual(3, len(criteria_after.phone_numbers))

        finally:
            # clean up: delete criteria again
            api.delete_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(after.criteria))

    def test_sequential_ring_criteria_remove_phone_number(self):
        """
        create criteria and renove phone number
        """
        api = self.api.workspace_settings.sequential_ring
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SequentialRingCriteria(calls_from=SequentialRingCallsFrom.select_phone_numbers, ring_enabled=True,
                                          phone_numbers=phone_numbers,
                                          anonymous_callers_enabled=False,
                                          unavailable_callers_enabled=False)
        criteria_id = api.create_criteria(self.workspace.workspace_id, criteria)
        try:
            details = api.read_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            criteria.id = details.id
            self.assertEqual(2, len(details.phone_numbers))
            # also there should be one criteria in the details
            self.assertEqual(1, len(after.criteria))

            # now, let's try to remove a phone numbers
            update = details.model_copy(deep=True)
            update.phone_numbers = phone_numbers[:-1]
            api.configure_criteria(self.workspace.workspace_id, criteria_id, update)
            criteria_after = api.read_criteria(self.workspace.workspace_id, criteria_id)
            self.assertEqual(1, len(criteria_after.phone_numbers))

        finally:
            # clean up: delete criteria again
            api.delete_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(after.criteria))

    def test_sequential_ring_criteria_create_with_schedule(self):
        """
        create criteria with actual schedule
        """
        api = self.api.workspace_settings.sequential_ring

        @contextmanager
        def with_schedule() -> Schedule:
            """
            get or create a schedule for the test
            """
            with self.no_log():
                schedules = list(self.api.telephony.schedules.list(self.workspace.location_id))
            if False and schedules:
                temp_schedule: Schedule = random.choice(schedules)
                yield temp_schedule
            else:
                # create a temporary schedule for the test
                print('creating temporary schedule for the test')
                temp_schedule = Schedule.business('test schedule')
                with self.no_log():
                    schedule_id = self.api.telephony.schedules.create(self.workspace.location_id, temp_schedule)
                try:
                    yield temp_schedule
                finally:
                    with self.no_log():
                        print('deleting temporary schedule')
                        self.api.telephony.schedules.delete_schedule(self.workspace.location_id,
                                                                     schedule_type=ScheduleType.business_hours,
                                                                     schedule_id=schedule_id)
            return

        with with_schedule() as schedule:
            schedule: Schedule
            before = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(before.criteria))
            criteria = SequentialRingCriteria(calls_from=SequentialRingCallsFrom.any_phone_number,
                                              ring_enabled=True,
                                              schedule_name=schedule.name,
                                              schedule_type=schedule.schedule_type,
                                              schedule_level=RingCriteriaScheduleLevel.group)
            criteria_id = api.create_criteria(self.workspace.workspace_id, criteria)
            try:
                details = api.read_criteria(self.workspace.workspace_id, criteria_id)
                after = api.read(self.workspace.workspace_id)
                self.assertEqual(1, len(after.criteria))
            finally:
                # clean up: delete criteria again
                api.delete_criteria(self.workspace.workspace_id, criteria_id)
                after = api.read(self.workspace.workspace_id)
                self.assertEqual(0, len(after.criteria))

    def test_sequential_ring_read(self):
        """
        read sequential ring settings
        """
        api = self.api.workspace_settings.sequential_ring
        api.read(self.workspace.workspace_id)

    def test_sequential_ring_configure(self):
        """
        configure sequential ring settings
        """

        @contextmanager
        def create_criteria() -> SequentialRingCriteria:
            """
            Create two sequential ring criteria on workspace
            """
            criteria = SequentialRingCriteria(schedule_name='', schedule_level='GLOBAL',
                                              calls_from=SequentialRingCallsFrom.any_phone_number, ring_enabled=True)
            cid1 = api.create_criteria(self.workspace.workspace_id, criteria)
            criteria = SequentialRingCriteria(schedule_name='', schedule_level='GLOBAL',
                                              calls_from=SequentialRingCallsFrom.select_phone_numbers, ring_enabled=False,
                                              phone_numbers=['+4961007739765', '+4961007739766'],
                                              anonymous_callers_enabled=False, unavailable_callers_enabled=False)
            cid2 = api.create_criteria(self.workspace.workspace_id, criteria)
            try:
                yield
            finally:
                api.delete_criteria(self.workspace.workspace_id, cid1)
                api.delete_criteria(self.workspace.workspace_id, cid2)
            return

        api = self.api.workspace_settings.sequential_ring
        with create_criteria():
            update = SequentialRing(enabled=True,
                                    ring_base_location_first_enabled=True,
                                    base_location_number_of_rings=3,
                                    continue_if_base_location_is_busy_enabled=True,
                                    calls_to_voicemail_enabled=False,
                                    phone_numbers=[SequentialRingNumber(phone_number='+4961009764',
                                                                        answer_confirmation_required_enabled=True,
                                                                        number_of_rings=3)])
            api.configure(self.workspace.workspace_id, update)
            after = api.read(self.workspace.workspace_id)

            # apparently the phone numbers are returned in a weird format: +49-61007739764
            # to check the update we want to ignore that
            after_with_cleaned_phone_number = after.model_copy(deep=True)
            for pn in after_with_cleaned_phone_number.phone_numbers:
                if pn.phone_number is None:
                    continue
                pn.phone_number = pn.phone_number.replace('-', '')

            # also, sequential ring settings always are returned with five phone numbers; for the test we are going to
            # ignore the ones that are not set
            after_with_cleaned_phone_number.phone_numbers = [pn for pn in after_with_cleaned_phone_number.phone_numbers
                                                             if pn.phone_number]

            # as the update doesn't have criteria, we also want to ignore differences in criteria
            update.criteria = after.criteria
            self.assertEqual(update, after_with_cleaned_phone_number)

            # we created two criteria, so there should be two criteria in the details
            self.assertEqual(2, len(after.criteria))

            # finally, raise an error if the phone numbers are not equal
            self.assertTrue(all(pn == pn_after
                                for pn, pn_after in zip(update.phone_numbers,
                                                        after.phone_numbers)),
                            f'phone numbers in update and after are not equal: '
                            f'{", ".join(str(pn.phone_number) for pn in after.phone_numbers if pn.phone_number)}')

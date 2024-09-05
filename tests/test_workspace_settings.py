"""
Webex Calling Workspace settings
"""
import asyncio
import random
from contextlib import contextmanager
from dataclasses import dataclass
from typing import ClassVar

from tests.base import TestCaseWithLog, async_test, TestWithProfessionalWorkspace
from wxc_sdk.common.schedules import Schedule
from wxc_sdk.common.selective import SelectiveFrom, SelectiveScheduleLevel
from wxc_sdk.person_settings import TelephonyDevice
from wxc_sdk.person_settings.call_policy import PrivacyOnRedirectedCalls
from wxc_sdk.person_settings.priority_alert import PriorityAlertApi, PriorityAlertCriteria, PriorityAlert
from wxc_sdk.person_settings.selective_accept import SelectiveAcceptApi, SelectiveAcceptCriteria, SelectiveAccept
from wxc_sdk.person_settings.selective_forward import SelectiveForwardApi, SelectiveForwardCriteria, SelectiveForward
from wxc_sdk.person_settings.selective_reject import SelectiveRejectApi, SelectiveRejectCriteria, SelectiveReject
from wxc_sdk.person_settings.sequential_ring import SequentialRing, SequentialRingNumber, SequentialRingCriteria, \
    SequentialRingApi
from wxc_sdk.person_settings.sim_ring import SimRingCriteria, SimRing, SimRingNumber, SimRingApi
from wxc_sdk.telephony import NumberType
from wxc_sdk.workspace_settings.numbers import WorkspaceNumbers
from wxc_sdk.workspaces import Workspace, CallingType


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


class TestWorkspaceSettingsWithProWorkspace(TestWithProfessionalWorkspace):
    def test_anon_calls_read(self):
        api = self.api.workspace_settings.anon_calls
        api.read(self.workspace.workspace_id)

    def test_anon_calls_configure(self):
        api = self.api.workspace_settings.anon_calls
        r = api.read(self.workspace.workspace_id)
        api.configure(self.workspace.workspace_id, not r)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(not r, after)

    def test_dnd_read(self):
        api = self.api.workspace_settings.dnd
        api.read(self.workspace.workspace_id)

    def test_dnd_configure(self):
        api = self.api.workspace_settings.dnd
        r = api.read(self.workspace.workspace_id)
        update = r.model_copy(deep=True)
        update.enabled = not r.enabled
        api.configure(self.workspace.workspace_id, update)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(update, after)

    def test_call_bridge_read(self):
        api = self.api.workspace_settings.call_bridge
        api.read(self.workspace.workspace_id)

    def test_call_bridge_configure(self):
        api = self.api.workspace_settings.call_bridge
        r = api.read(self.workspace.workspace_id)
        update = r.model_copy(deep=True)
        update.warning_tone_enabled = not r.warning_tone_enabled
        api.configure(self.workspace.workspace_id, update)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(update, after)

    def test_ptt_read(self):
        api = self.api.workspace_settings.push_to_talk
        api.read(self.workspace.workspace_id)

    def test_ptt_configure(self):
        api = self.api.workspace_settings.push_to_talk
        r = api.read(self.workspace.workspace_id)
        update = r.model_copy(deep=True)
        update.allow_auto_answer = not r.allow_auto_answer
        api.configure(self.workspace.workspace_id, update)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(update, after)

    def test_voicemail_read(self):
        api = self.api.workspace_settings.voicemail
        api.read(self.workspace.workspace_id)

    def test_voicemail_configure(self):
        api = self.api.workspace_settings.voicemail
        r = api.read(self.workspace.workspace_id)
        update = r.model_copy(deep=True)
        update.enabled = not r.enabled
        api.configure(self.workspace.workspace_id, update)
        after = api.read(self.workspace.workspace_id)
        self.assertEqual(update, after)

    def test_call_policy_read(self):
        """
        read call policy settings
        """
        api = self.api.workspace_settings.call_policy
        api.read(self.workspace.workspace_id)

    def test_call_policy_configure(self):
        """
        configure call policy settings
        """
        api = self.api.workspace_settings.call_policy
        before = api.read(self.workspace.workspace_id)
        try:
            for i in PrivacyOnRedirectedCalls:
                api.configure(self.workspace.workspace_id, i)
                r = api.read(self.workspace.workspace_id)
                self.assertEqual(i, r)
        finally:
            # restore original settings
            api.configure(self.workspace.workspace_id, before)
        return


@dataclass(init=False)
class SeqRingTest(TestWithProfessionalWorkspace):
    tapi: ClassVar[SequentialRingApi]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tapi = cls.api.workspace_settings.sequential_ring

    def test_criteria_create(self):
        """
        create criteria
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        criteria = SequentialRingCriteria(calls_from=SelectiveFrom.any_phone_number, enabled=True)
        criteria_id = api.create_criteria(self.workspace.workspace_id, criteria)
        try:
            details = api.read_criteria(self.workspace.workspace_id, criteria_id)
            self.assertEqual(criteria.calls_from, details.calls_from)
            self.assertEqual(criteria.enabled, details.enabled)

            # also there should be one criteria in the details
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(1, len(after.criteria))
        finally:
            # clean up: delete criteria again
            api.delete_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(after.criteria))

    def test_criteria_create_with_phone_number(self):
        """
        create criteria with phone numbers
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766', '+14085550123']
        criteria = SequentialRingCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_add_phone_number(self):
        """
        create criteria and add phone number
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SequentialRingCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_remove_phone_number(self):
        """
        create criteria and remove phone number
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SequentialRingCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_create_with_schedule(self):
        """
        create criteria with actual schedule
        """
        api = self.tapi

        with self.with_schedule() as schedule:
            schedule: Schedule
            before = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(before.criteria))
            criteria = SequentialRingCriteria(calls_from=SelectiveFrom.any_phone_number,
                                              enabled=True,
                                              schedule_name=schedule.name,
                                              schedule_type=schedule.schedule_type,
                                              schedule_level=SelectiveScheduleLevel.group)
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

    def test_read(self):
        """
        read sequential ring settings
        """
        api = self.tapi
        api.read(self.workspace.workspace_id)

    def test_configure(self):
        """
        configure sequential ring settings
        """
        api = self.tapi

        @contextmanager
        def create_criteria():
            """
            Create two sequential ring criteria on workspace
            """
            criteria = SequentialRingCriteria(schedule_name='', schedule_level='GLOBAL',
                                              calls_from=SelectiveFrom.any_phone_number, enabled=True)
            cid1 = api.create_criteria(self.workspace.workspace_id, criteria)
            criteria = SequentialRingCriteria(schedule_name='', schedule_level='GLOBAL',
                                              calls_from=SelectiveFrom.select_phone_numbers,
                                              enabled=False,
                                              phone_numbers=['+4961007739765', '+4961007739766'],
                                              anonymous_callers_enabled=False, unavailable_callers_enabled=False)
            cid2 = api.create_criteria(self.workspace.workspace_id, criteria)
            try:
                yield
            finally:
                api.delete_criteria(self.workspace.workspace_id, cid1)
                api.delete_criteria(self.workspace.workspace_id, cid2)
            return

        with create_criteria():
            update = SequentialRing(enabled=True,
                                    ring_base_location_first_enabled=True,
                                    base_location_number_of_rings=3,
                                    continue_if_base_location_is_busy_enabled=True,
                                    calls_to_voicemail_enabled=False,
                                    phone_numbers=[SequentialRingNumber(phone_number='+4961009764',
                                                                        answer_confirmation_required_enabled=True,
                                                                        number_of_rings=3),
                                                   SequentialRingNumber(phone_number='+14085550123',
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


@dataclass(init=False)
class SimRingTest(TestWithProfessionalWorkspace):
    tapi: ClassVar[SimRingApi]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tapi = cls.api.workspace_settings.sim_ring

    def test_criteria_create(self):
        """
        create criteria
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        criteria = SimRingCriteria(calls_from=SelectiveFrom.any_phone_number, enabled=True)
        criteria_id = api.create_criteria(self.workspace.workspace_id, criteria)
        try:
            details = api.read_criteria(self.workspace.workspace_id, criteria_id)
            self.assertEqual(criteria.calls_from, details.calls_from)
            self.assertEqual(criteria.enabled, details.enabled)

            # also there should be one criteria in the details
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(1, len(after.criteria))
        finally:
            # clean up: delete criteria again
            api.delete_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(after.criteria))

    def test_criteria_create_with_phone_number(self):
        """
        create criteria with phone numbers
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SimRingCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_add_phone_number(self):
        """
        create criteria and add phone number
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SimRingCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_remove_phone_number(self):
        """
        create criteria and remove phone number
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SimRingCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_create_with_schedule(self):
        """
        create criteria with actual schedule
        """
        api = self.tapi

        with self.with_schedule() as schedule:
            schedule: Schedule
            before = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(before.criteria))
            criteria = SimRingCriteria(calls_from=SelectiveFrom.any_phone_number,
                                       enabled=True,
                                       schedule_name=schedule.name,
                                       schedule_type=schedule.schedule_type,
                                       schedule_level=SelectiveScheduleLevel.group)
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

    def test_read(self):
        """
        read sim ring settings
        """
        api = self.tapi
        api.read(self.workspace.workspace_id)

    def test_configure(self):
        """
        configure sim ring settings
        """
        api = self.tapi

        @contextmanager
        def create_criteria():
            """
            Create two sim ring criteria on workspace
            """
            criteria = SimRingCriteria(schedule_name='', schedule_level='GLOBAL',
                                       calls_from=SelectiveFrom.any_phone_number, enabled=True)
            cid1 = api.create_criteria(self.workspace.workspace_id, criteria)
            criteria = SimRingCriteria(schedule_name='', schedule_level='GLOBAL',
                                       calls_from=SelectiveFrom.select_phone_numbers,
                                       enabled=False,
                                       phone_numbers=['+4961007739765', '+4961007739766'],
                                       anonymous_callers_enabled=False, unavailable_callers_enabled=False)
            cid2 = api.create_criteria(self.workspace.workspace_id, criteria)
            try:
                yield
            finally:
                api.delete_criteria(self.workspace.workspace_id, cid1)
                api.delete_criteria(self.workspace.workspace_id, cid2)
            return

        with create_criteria():
            update = SimRing(enabled=True,
                             do_not_ring_if_on_call_enabled=True,
                             criterias_enabled=True,
                             phone_numbers=[SimRingNumber(phone_number='+4961009764',
                                                          answer_confirmation_required_enabled=True)])
            api.configure(self.workspace.workspace_id, update)
            after = api.read(self.workspace.workspace_id)

            # apparently the phone numbers are returned in a weird format: +49-61007739764
            # to check the update we want to ignore that
            after_with_cleaned_phone_number = after.model_copy(deep=True)
            for pn in after_with_cleaned_phone_number.phone_numbers:
                if pn.phone_number is None:
                    continue
                pn.phone_number = pn.phone_number.replace('-', '')

            # also, sim ring settings always are returned with five phone numbers; for the test we are going to
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


@dataclass(init=False)
class SelectiveRejectTest(TestWithProfessionalWorkspace):
    tapi: ClassVar[SelectiveRejectApi]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tapi = cls.api.workspace_settings.selective_reject

    def test_criteria_create(self):
        """
        create criteria
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        criteria = SelectiveRejectCriteria(calls_from=SelectiveFrom.any_phone_number, enabled=True)
        criteria_id = api.create_criteria(self.workspace.workspace_id, criteria)
        try:
            details = api.read_criteria(self.workspace.workspace_id, criteria_id)
            self.assertEqual(criteria.calls_from, details.calls_from)
            self.assertEqual(criteria.enabled, details.enabled)

            # also there should be one criteria in the details
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(1, len(after.criteria))
        finally:
            # clean up: delete criteria again
            api.delete_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(after.criteria))

    def test_criteria_create_with_phone_number(self):
        """
        create criteria with phone numbers
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SelectiveRejectCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_add_phone_number(self):
        """
        create criteria and add phone number
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SelectiveRejectCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_remove_phone_number(self):
        """
        create criteria and remove phone number
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SelectiveRejectCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_create_with_schedule(self):
        """
        create criteria with actual schedule
        """
        api = self.tapi

        with self.with_schedule() as schedule:
            schedule: Schedule
            before = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(before.criteria))
            criteria = SelectiveRejectCriteria(calls_from=SelectiveFrom.any_phone_number,
                                               enabled=True,
                                               schedule_name=schedule.name,
                                               schedule_type=schedule.schedule_type,
                                               schedule_level=SelectiveScheduleLevel.group)
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

    def test_read(self):
        """
        read selective reject settings
        """
        api = self.tapi
        api.read(self.workspace.workspace_id)

    def test_configure(self):
        """
        configure selective reject settings
        """
        api = self.tapi

        @contextmanager
        def create_criteria():
            """
            Create two sim ring criteria on workspace
            """
            criteria = SelectiveRejectCriteria(schedule_name='', schedule_level='GLOBAL',
                                               calls_from=SelectiveFrom.any_phone_number, enabled=True)
            cid1 = api.create_criteria(self.workspace.workspace_id, criteria)
            criteria = SelectiveRejectCriteria(schedule_name='', schedule_level='GLOBAL',
                                               calls_from=SelectiveFrom.select_phone_numbers,
                                               enabled=False,
                                               phone_numbers=['+4961007739765', '+4961007739766'],
                                               anonymous_callers_enabled=False, unavailable_callers_enabled=False)
            cid2 = api.create_criteria(self.workspace.workspace_id, criteria)
            try:
                yield
            finally:
                api.delete_criteria(self.workspace.workspace_id, cid1)
                api.delete_criteria(self.workspace.workspace_id, cid2)
            return

        with create_criteria():
            update = SelectiveReject(enabled=True)
            api.configure(self.workspace.workspace_id, update)
            after = api.read(self.workspace.workspace_id)

            # as the update doesn't have criteria, we also want to ignore differences in criteria
            update.criteria = after.criteria
            self.assertEqual(update, after)

            # we created two criteria, so there should be two criteria in the details
            self.assertEqual(2, len(after.criteria))


@dataclass(init=False)
class SelectiveAcceptTest(TestWithProfessionalWorkspace):
    tapi: ClassVar[SelectiveAcceptApi]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tapi = cls.api.workspace_settings.selective_accept

    def test_criteria_create(self):
        """
        create criteria
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        criteria = SelectiveAcceptCriteria(calls_from=SelectiveFrom.any_phone_number, enabled=True)
        criteria_id = api.create_criteria(self.workspace.workspace_id, criteria)
        try:
            details = api.read_criteria(self.workspace.workspace_id, criteria_id)
            self.assertEqual(criteria.calls_from, details.calls_from)
            self.assertEqual(criteria.enabled, details.enabled)

            # also there should be one criteria in the details
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(1, len(after.criteria))
        finally:
            # clean up: delete criteria again
            api.delete_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(after.criteria))

    def test_criteria_create_with_phone_number(self):
        """
        create criteria with phone numbers
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SelectiveAcceptCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_add_phone_number(self):
        """
        create criteria and add phone number
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SelectiveAcceptCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_remove_phone_number(self):
        """
        create criteria and remove phone number
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SelectiveAcceptCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_create_with_schedule(self):
        """
        create criteria with actual schedule
        """
        api = self.tapi

        with self.with_schedule() as schedule:
            schedule: Schedule
            before = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(before.criteria))
            criteria = SelectiveAcceptCriteria(calls_from=SelectiveFrom.any_phone_number,
                                               enabled=True,
                                               schedule_name=schedule.name,
                                               schedule_type=schedule.schedule_type,
                                               schedule_level=SelectiveScheduleLevel.group)
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

    def test_read(self):
        """
        read selective accept settings
        """
        api = self.tapi
        api.read(self.workspace.workspace_id)

    def test_configure(self):
        """
        configure selective accept settings
        """
        api = self.tapi

        @contextmanager
        def create_criteria():
            """
            Create two sim ring criteria on workspace
            """
            criteria = SelectiveAcceptCriteria(schedule_name='', schedule_level='GLOBAL',
                                               calls_from=SelectiveFrom.any_phone_number, enabled=True)
            cid1 = api.create_criteria(self.workspace.workspace_id, criteria)
            criteria = SelectiveAcceptCriteria(schedule_name='', schedule_level='GLOBAL',
                                               calls_from=SelectiveFrom.select_phone_numbers,
                                               enabled=False,
                                               phone_numbers=['+4961007739765', '+4961007739766'],
                                               anonymous_callers_enabled=False, unavailable_callers_enabled=False)
            cid2 = api.create_criteria(self.workspace.workspace_id, criteria)
            try:
                yield
            finally:
                api.delete_criteria(self.workspace.workspace_id, cid1)
                api.delete_criteria(self.workspace.workspace_id, cid2)
            return

        with create_criteria():
            update = SelectiveAccept(enabled=True)
            api.configure(self.workspace.workspace_id, update)
            after = api.read(self.workspace.workspace_id)

            # as the update doesn't have criteria, we also want to ignore differences in criteria
            update.criteria = after.criteria
            self.assertEqual(update, after)

            # we created two criteria, so there should be two criteria in the details
            self.assertEqual(2, len(after.criteria))


@dataclass(init=False)
class PriorityAlertTest(TestWithProfessionalWorkspace):
    tapi: ClassVar[PriorityAlertApi]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tapi = cls.api.workspace_settings.priority_alert

    def test_criteria_create(self):
        """
        create criteria
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        criteria = PriorityAlertCriteria(calls_from=SelectiveFrom.any_phone_number, enabled=True)
        criteria_id = api.create_criteria(self.workspace.workspace_id, criteria)
        try:
            details = api.read_criteria(self.workspace.workspace_id, criteria_id)
            self.assertEqual(criteria.calls_from, details.calls_from)
            self.assertEqual(criteria.enabled, details.enabled)

            # also there should be one criteria in the details
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(1, len(after.criteria))
        finally:
            # clean up: delete criteria again
            api.delete_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(after.criteria))

    def test_criteria_create_with_phone_number(self):
        """
        create criteria with phone numbers
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = PriorityAlertCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_add_phone_number(self):
        """
        create criteria and add phone number
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = PriorityAlertCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_remove_phone_number(self):
        """
        create criteria and remove phone number
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = PriorityAlertCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
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

    def test_criteria_create_with_schedule(self):
        """
        create criteria with actual schedule
        """
        api = self.tapi

        with self.with_schedule() as schedule:
            schedule: Schedule
            before = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(before.criteria))
            criteria = PriorityAlertCriteria(calls_from=SelectiveFrom.any_phone_number,
                                             enabled=True,
                                             schedule_name=schedule.name,
                                             schedule_type=schedule.schedule_type,
                                             schedule_level=SelectiveScheduleLevel.group)
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

    def test_read(self):
        """
        read priority alert settings
        """
        api = self.tapi
        api.read(self.workspace.workspace_id)

    def test_configure(self):
        """
        configure priority alert settings
        """
        api = self.tapi

        @contextmanager
        def create_criteria():
            """
            Create two sim ring criteria on workspace
            """
            criteria = PriorityAlertCriteria(schedule_name='', schedule_level='GLOBAL',
                                             calls_from=SelectiveFrom.any_phone_number, enabled=True)
            cid1 = api.create_criteria(self.workspace.workspace_id, criteria)
            criteria = PriorityAlertCriteria(schedule_name='', schedule_level='GLOBAL',
                                             calls_from=SelectiveFrom.select_phone_numbers,
                                             enabled=False,
                                             phone_numbers=['+4961007739765', '+4961007739766'],
                                             anonymous_callers_enabled=False, unavailable_callers_enabled=False)
            cid2 = api.create_criteria(self.workspace.workspace_id, criteria)
            try:
                yield
            finally:
                api.delete_criteria(self.workspace.workspace_id, cid1)
                api.delete_criteria(self.workspace.workspace_id, cid2)
            return

        with create_criteria():
            update = PriorityAlert(enabled=True)
            api.configure(self.workspace.workspace_id, update)
            after = api.read(self.workspace.workspace_id)

            # as the update doesn't have criteria, we also want to ignore differences in criteria
            update.criteria = after.criteria
            self.assertEqual(update, after)

            # we created two criteria, so there should be two criteria in the details
            self.assertEqual(2, len(after.criteria))


@dataclass(init=False)
class SelectiveForwardTest(TestWithProfessionalWorkspace):
    tapi: ClassVar[SelectiveForwardApi]
    forward_to_phone_number: ClassVar[str]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tapi = cls.api.workspace_settings.selective_forward
        numbers = list(
            cls.api.telephony.phone_numbers(location_id=cls.location.location_id, number_type=NumberType.number))
        if numbers:
            cls.forward_to_phone_number = random.choice(numbers).phone_number
        else:
            cls.forward_to_phone_number = None

    def setUp(self) -> None:
        super().setUp()
        if self.forward_to_phone_number is None:
            self.fail('No phone numbers available')

    def test_criteria_create(self):
        """
        create criteria
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        criteria = SelectiveForwardCriteria(calls_from=SelectiveFrom.any_phone_number, enabled=True,
                                            forward_to_phone_number=self.forward_to_phone_number,
                                            send_to_voicemail_enabled=True)
        criteria_id = api.create_criteria(self.workspace.workspace_id, criteria)
        try:
            details = api.read_criteria(self.workspace.workspace_id, criteria_id)
            self.assertEqual(criteria.calls_from, details.calls_from)
            self.assertEqual(criteria.enabled, details.enabled)
            self.assertEqual(criteria.send_to_voicemail_enabled, details.send_to_voicemail_enabled)
            # apparently the phone numbers are returned in a weird format: +49-6100135393
            self.assertEqual(criteria.forward_to_phone_number,
                             details.forward_to_phone_number.replace('-', ''))

            # also there should be one criteria in the details
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(1, len(after.criteria))
            self.assertEqual(criteria.forward_to_phone_number, details.forward_to_phone_number)
        finally:
            # clean up: delete criteria again
            api.delete_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(after.criteria))

    def test_criteria_create_with_phone_number(self):
        """
        create criteria with phone numbers
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SelectiveForwardCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
                                            phone_numbers=phone_numbers,
                                            anonymous_callers_enabled=False,
                                            unavailable_callers_enabled=False,
                                            forward_to_phone_number=self.forward_to_phone_number,
                                            send_to_voicemail_enabled=True)
        criteria_id = api.create_criteria(self.workspace.workspace_id, criteria)
        try:
            details = api.read_criteria(self.workspace.workspace_id, criteria_id)
            details_with_cleaned_phone_number = details.model_copy(deep=True)
            details_with_cleaned_phone_number.phone_numbers = \
                [pn.replace('-', '')
                 for pn in details_with_cleaned_phone_number.phone_numbers]
            criteria.id = details.id
            details_with_cleaned_phone_number.forward_to_phone_number = (
                details.forward_to_phone_number.replace('-', ''))
            self.assertEqual(criteria, details_with_cleaned_phone_number)

            # also there should be one criteria in the details
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(1, len(after.criteria))

            # ... and the numbers are somewhat screwed up
            err = False
            if not all(pn == pn_after
                       for pn, pn_after in zip(phone_numbers,
                                               details.phone_numbers)):
                print(f'phone numbers in criteria and details are not equal: '
                      f'{", ".join(details.phone_numbers)}')
                err = True
            if criteria.forward_to_phone_number != details.forward_to_phone_number:
                print(f'forward_to_phone_number in criteria and details are not equal: '
                      f'{criteria.forward_to_phone_number} != {details.forward_to_phone_number}')
                err = True
            self.assertFalse(err, 'Some number issues; check output')

        finally:
            # clean up: delete criteria again
            api.delete_criteria(self.workspace.workspace_id, criteria_id)
            after = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(after.criteria))

    def test_criteria_add_phone_number(self):
        """
        create criteria and add phone number
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SelectiveForwardCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
                                            phone_numbers=phone_numbers,
                                            anonymous_callers_enabled=False,
                                            unavailable_callers_enabled=False,
                                            forward_to_phone_number=self.forward_to_phone_number)
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

    def test_criteria_remove_phone_number(self):
        """
        create criteria and remove phone number
        """
        api = self.tapi
        before = api.read(self.workspace.workspace_id)
        self.assertEqual(0, len(before.criteria))
        phone_numbers = ['+4961007739765', '+4961007739766']
        criteria = SelectiveForwardCriteria(calls_from=SelectiveFrom.select_phone_numbers, enabled=True,
                                            phone_numbers=phone_numbers,
                                            anonymous_callers_enabled=False,
                                            unavailable_callers_enabled=False,
                                            forward_to_phone_number=self.forward_to_phone_number)
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

    def test_criteria_create_with_schedule(self):
        """
        create criteria with actual schedule
        """
        api = self.tapi

        with self.with_schedule() as schedule:
            schedule: Schedule
            before = api.read(self.workspace.workspace_id)
            self.assertEqual(0, len(before.criteria))
            criteria = SelectiveForwardCriteria(calls_from=SelectiveFrom.any_phone_number,
                                                enabled=True,
                                                schedule_name=schedule.name,
                                                schedule_type=schedule.schedule_type,
                                                schedule_level=SelectiveScheduleLevel.group,
                                                forward_to_phone_number=self.forward_to_phone_number)
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

    def test_read(self):
        """
        read selective forward settings
        """
        api = self.tapi
        api.read(self.workspace.workspace_id)

    def test_configure(self):
        """
        configure selective forward settings
        """
        api = self.tapi

        @contextmanager
        def create_criteria():
            """
            Create two sim ring criteria on workspace
            """
            criteria = SelectiveForwardCriteria(schedule_name='', schedule_level='GLOBAL',
                                                calls_from=SelectiveFrom.any_phone_number, enabled=True,
                                                forward_to_phone_number=self.forward_to_phone_number)
            cid1 = api.create_criteria(self.workspace.workspace_id, criteria)
            criteria = SelectiveForwardCriteria(schedule_name='', schedule_level='GLOBAL',
                                                calls_from=SelectiveFrom.select_phone_numbers,
                                                enabled=False,
                                                phone_numbers=['+4961007739765', '+4961007739766'],
                                                anonymous_callers_enabled=False, unavailable_callers_enabled=False,
                                                forward_to_phone_number=self.forward_to_phone_number)
            cid2 = api.create_criteria(self.workspace.workspace_id, criteria)
            try:
                yield
            finally:
                api.delete_criteria(self.workspace.workspace_id, cid1)
                api.delete_criteria(self.workspace.workspace_id, cid2)
            return

        with create_criteria():
            update = SelectiveForward(enabled=True, default_phone_number_to_forward=self.forward_to_phone_number,
                                      ring_reminder_enabled=True, destination_voicemail_enabled=True)
            api.configure(self.workspace.workspace_id, update)
            after = api.read(self.workspace.workspace_id)

            # as the update doesn't have criteria, we also want to ignore differences in criteria
            update.criteria = after.criteria
            self.assertEqual(update, after)

            # we created two criteria, so there should be two criteria in the details
            self.assertEqual(2, len(after.criteria))

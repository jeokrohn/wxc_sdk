from contextlib import suppress
from uuid import uuid4

from tests.base import TestWithTwoTempCallingUsers
from wxc_sdk.common.schedules import Schedule, ScheduleType
from wxc_sdk.common.selective import SelectiveFrom
from wxc_sdk.person_settings.executive import (
    ExecCallFiltering,
    ExecCallFilteringCriteria,
    ExecCallFilteringScheduleLevel,
    ExecCallFilterType,
)
from wxc_sdk.rest import RestError

# mypy: disable-error-code="list-item"


class TestPersonExecutive(TestWithTwoTempCallingUsers):
    """
    Stateful tests for person executive settings.
    """

    def assigned_assistants_or_empty(self):
        """
        Return assigned assistants, treating an unassigned Executive service as an empty baseline.
        """
        api = self.api.person_settings.executive
        try:
            return api.assigned_assistants(person_id=self.user.person_id)
        except RestError as e:
            if e.code == 4410:
                return []
            raise

    def assigned_assistants_or_skip(self):
        """
        Return assigned assistants, or skip when the org cannot expose Executive service for the temp user.
        """
        api = self.api.person_settings.executive
        try:
            return api.assigned_assistants(person_id=self.user.person_id)
        except RestError as e:
            if e.code == 4410:
                self.skipTest('Executive service is not assigned to the temporary user')
            raise

    def update_assigned_assistants_or_skip(self, assistant_ids: list[str]):
        """
        Update assigned assistants, or skip when the temp user cannot use Executive service.
        """
        api = self.api.person_settings.executive
        try:
            api.update_assigned_assistants(person_id=self.user.person_id, assistant_ids=assistant_ids)
        except RestError as e:
            if e.code == 4410:
                self.skipTest('Executive service cannot be assigned to the temporary user')
            raise

    def test_assigned_assistants_add_list_delete_restore(self):
        """
        Add, list, delete, and restore an executive assistant assignment using two disposable users.
        """
        api = self.api.person_settings.executive

        # Snapshot existing assigned assistants, treating a missing Executive service as empty.
        before = self.assigned_assistants_or_empty()
        try:
            # Assign the second temp user as assistant and verify it appears in the assigned list.
            self.update_assigned_assistants_or_skip(assistant_ids=[self.second_user.person_id])
            after_add = self.assigned_assistants_or_skip()
            self.assertIn(self.second_user.person_id, {assistant.id for assistant in after_add})

            # Remove all assigned assistants and verify the temporary assistant is gone.
            self.update_assigned_assistants_or_skip(assistant_ids=[])
            after_delete = self.assigned_assistants_or_skip()
            self.assertNotIn(self.second_user.person_id, {assistant.id for assistant in after_delete})
        finally:
            # Restore the original assigned assistant list if the endpoint remains available.
            with suppress(RestError):
                api.update_assigned_assistants(
                    person_id=self.user.person_id,
                    assistant_ids=[assistant.id for assistant in before if assistant.id],
                )

    def test_alert_and_screening_update_restore(self):
        """
        Update executive alert and screening settings, then restore their original values.
        """
        api = self.api.person_settings.executive

        # Snapshot current assistant assignments and prepare restore sentinels.
        assigned_before = self.assigned_assistants_or_empty()
        alert_before = None
        screening_before = None
        try:
            # Assign an assistant first because Executive subsettings require the service to be active.
            self.update_assigned_assistants_or_skip(assistant_ids=[self.second_user.person_id])
            try:
                alert_before = api.alert_settings(person_id=self.user.person_id)
                screening_before = api.screening_settings(person_id=self.user.person_id)
            except RestError as e:
                if e.code == 4410:
                    self.skipTest('Executive service is not assigned to the temporary user')
                raise

            # Toggle alert rollover and verify the alert read endpoint reflects the update.
            alert_update = alert_before.model_copy(deep=True)
            alert_update.rollover_enabled = not bool(alert_update.rollover_enabled)
            api.update_alert_settings(person_id=self.user.person_id, settings=alert_update)
            alert_after = api.alert_settings(person_id=self.user.person_id)
            self.assertEqual(alert_update.rollover_enabled, alert_after.rollover_enabled)

            # Toggle screening enablement and verify the screening read endpoint reflects the update.
            screening_update = screening_before.model_copy(deep=True)
            screening_update.enabled = not bool(screening_update.enabled)
            api.update_screening_settings(person_id=self.user.person_id, settings=screening_update)
            screening_after = api.screening_settings(person_id=self.user.person_id)
            self.assertEqual(screening_update.enabled, screening_after.enabled)
        finally:
            # Restore alert and screening settings if they were successfully read.
            if alert_before is not None:
                api.update_alert_settings(person_id=self.user.person_id, settings=alert_before)
            if screening_before is not None:
                api.update_screening_settings(person_id=self.user.person_id, settings=screening_before)

            # Restore assistant assignments regardless of the update path outcome.
            with suppress(RestError):
                api.update_assigned_assistants(
                    person_id=self.user.person_id,
                    assistant_ids=[assistant.id for assistant in assigned_before if assistant.id],
                )

    def test_assistant_settings_update_restore(self):
        """
        Update assistant-side executive settings for the assigned assistant and restore them.
        """
        api = self.api.person_settings.executive

        # Snapshot current executive assignments and prepare a restore sentinel for assistant settings.
        assigned_before = self.assigned_assistants_or_empty()
        assistant_after_assign = None
        try:
            # Assign the second temp user as assistant, then read that user's assistant settings.
            self.update_assigned_assistants_or_skip(assistant_ids=[self.second_user.person_id])
            assistant_after_assign = api.executive_assistant_settings(person_id=self.second_user.person_id)

            # Toggle the assistant's opt-in state for the temporary executive.
            update = assistant_after_assign.model_copy(deep=True)
            executive = next((exec_ for exec_ in update.executives or [] if exec_.id == self.user.person_id), None)
            self.assertIsNotNone(executive)
            executive.opt_in_enabled = not bool(executive.opt_in_enabled)

            # Update assistant settings and verify the opt-in change is visible.
            api.update_executive_assistant_settings(person_id=self.second_user.person_id, settings=update)
            after = api.executive_assistant_settings(person_id=self.second_user.person_id)
            after_executive = next((exec_ for exec_ in after.executives or [] if exec_.id == self.user.person_id), None)
            self.assertIsNotNone(after_executive)
            self.assertEqual(executive.opt_in_enabled, after_executive.opt_in_enabled)
        finally:
            # Restore assistant settings if they were read after assignment.
            if assistant_after_assign is not None:
                with suppress(RestError):
                    api.update_executive_assistant_settings(
                        person_id=self.second_user.person_id,
                        settings=assistant_after_assign,
                    )

            # Restore the original assistant assignment list.
            with suppress(RestError):
                api.update_assigned_assistants(
                    person_id=self.user.person_id,
                    assistant_ids=[assistant.id for assistant in assigned_before if assistant.id],
                )

    def test_call_filtering_criteria_create_read_update_delete_restore(self):
        """
        Create, read, update, delete, and restore executive call filtering criteria.
        """
        executive_api = self.api.person_settings.executive
        schedules_api = self.api.person_settings.schedules

        # Snapshot assignment and filtering state before enabling custom criteria.
        assigned_before = self.assigned_assistants_or_empty()
        filtering_before = None

        # Prepare a person-level holiday schedule used only by this criterion.
        schedule_name = f'test_executive_filtering_{uuid4().hex[:8]}'
        schedule_type = ScheduleType.holidays
        schedule = Schedule(name=schedule_name, type=schedule_type)
        schedule_id = None
        criteria_id = None
        try:
            # Assign the assistant and read call filtering settings after Executive service activation.
            self.update_assigned_assistants_or_skip(assistant_ids=[self.second_user.person_id])
            try:
                filtering_before = executive_api.executive_call_filtering_settings(person_id=self.user.person_id)
            except RestError as e:
                if e.code == 4410:
                    self.skipTest('Executive service is not assigned to the temporary user')
                raise

            # Enable custom call filters so criteria can be created and evaluated.
            executive_api.update_executive_call_filtering_settings(
                person_id=self.user.person_id,
                settings=ExecCallFiltering(enabled=True, filter_type=ExecCallFilterType.custom_call_filters),
            )

            # Create the temporary schedule and associated filtering criterion.
            schedule_id = schedules_api.create(obj_id=self.user.person_id, schedule=schedule)
            criteria = ExecCallFilteringCriteria(
                filter_name='test_filter',
                schedule_name=schedule.name,
                schedule_type=schedule_type,
                schedule_level=ExecCallFilteringScheduleLevel.people,
                calls_from=SelectiveFrom.any_phone_number,
                filter_enabled=True,
            )
            criteria_id = executive_api.create_call_filtering_criteria(person_id=self.user.person_id, settings=criteria)

            # Read criterion details and verify the created values.
            details = executive_api.get_filtering_criteria(person_id=self.user.person_id, id=criteria_id)
            self.assertEqual(criteria.filter_name, details.filter_name)
            self.assertEqual(criteria.calls_from, details.calls_from)

            # Toggle criterion behavior and verify the update through the detail endpoint.
            details.filter_enabled = not bool(details.filter_enabled)
            executive_api.update_call_filtering_criteria(
                person_id=self.user.person_id, id=criteria_id, settings=details
            )
            after_update = executive_api.get_filtering_criteria(person_id=self.user.person_id, id=criteria_id)
            self.assertEqual(details.filter_enabled, after_update.filter_enabled)

            # Delete the criterion and verify the settings list no longer contains it.
            executive_api.delete_call_filtering_criteria(person_id=self.user.person_id, id=criteria_id)
            criteria_id = None
            after_delete = executive_api.executive_call_filtering_settings(person_id=self.user.person_id)
            self.assertNotIn(details.id, {criterion.id for criterion in after_delete.criteria or []})
        finally:
            # Remove the criterion if the test exits before the explicit delete.
            if criteria_id is not None:
                with suppress(RestError):
                    executive_api.delete_call_filtering_criteria(person_id=self.user.person_id, id=criteria_id)

            # Delete the temporary schedule artifact created for the criterion.
            if schedule_id is not None:
                with suppress(RestError):
                    schedules_api.delete_schedule(
                        obj_id=self.user.person_id,
                        schedule_type=schedule_type,
                        schedule_id=schedule_id,
                    )

            # Restore call filtering and assistant assignments to their original states.
            if filtering_before is not None:
                executive_api.update_executive_call_filtering_settings(
                    person_id=self.user.person_id,
                    settings=filtering_before,
                )
            with suppress(RestError):
                executive_api.update_assigned_assistants(
                    person_id=self.user.person_id,
                    assistant_ids=[assistant.id for assistant in assigned_before if assistant.id],
                )

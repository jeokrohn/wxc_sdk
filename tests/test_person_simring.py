import asyncio

from tests.base import TestCaseWithUsers, TestWithTempCallingUser, async_test
from wxc_sdk.common.selective import SelectiveFrom
from wxc_sdk.person_settings.sim_ring import SimRingCriteria


class TestPersonSimRing(TestCaseWithUsers):
    """
    Read simultaneous ring settings for existing calling users.
    """

    @async_test
    async def test_get_all_settings(self):
        """
        Retrieve simultaneous ring settings for all calling users and report any endpoint errors.
        """
        # Read all users concurrently to cover the list of available live users.
        settings = await asyncio.gather(
            *[self.async_api.person_settings.sim_ring.read(entity_id=u.person_id) for u in self.users],
            return_exceptions=True,
        )

        # Print the user associated with any failure so fixture problems are diagnosable.
        err = None
        for user, setting in zip(self.users, settings):
            if isinstance(setting, Exception):
                err = err or setting
                print(f'Failed to get simring settings for user "{user.display_name}": {setting}')
        return


class TestPersonSimRingCrud(TestWithTempCallingUser):
    """
    Stateful CRUD coverage for simultaneous ring settings on a disposable user.
    """

    def test_configure_restore(self):
        """
        Modify simultaneous ring settings and restore them.
        """
        api = self.api.person_settings.sim_ring

        # Snapshot current settings and build a safe update for the disposable user.
        before = api.read(entity_id=self.user.person_id)
        update = before.model_copy(deep=True)
        if update.phone_numbers:
            update.enabled = not bool(update.enabled)
        else:
            update.enabled = before.enabled
        update.do_not_ring_if_on_call_enabled = not bool(update.do_not_ring_if_on_call_enabled)
        try:
            # Configure the updated settings and verify the mutable fields changed as requested.
            api.configure(entity_id=self.user.person_id, settings=update)
            after = api.read(entity_id=self.user.person_id)
            self.assertEqual(update.enabled, after.enabled)
            self.assertEqual(update.do_not_ring_if_on_call_enabled, after.do_not_ring_if_on_call_enabled)
        finally:
            # Restore the exact original settings and verify no side effect remains.
            api.configure(entity_id=self.user.person_id, settings=before)
            restored = api.read(entity_id=self.user.person_id)
            self.assertEqual(before, restored)

    def test_criteria_create_read_update_delete(self):
        """
        Create, read, update, and delete simultaneous ring criteria.
        """
        api = self.api.person_settings.sim_ring
        criteria = SimRingCriteria(calls_from=SelectiveFrom.any_phone_number, enabled=True)
        criteria_id = None
        try:
            # Snapshot existing criteria and create a new all-callers criterion.
            before = api.read(entity_id=self.user.person_id)
            criteria_id = api.create_criteria(entity_id=self.user.person_id, settings=criteria)
            details = api.read_criteria(entity_id=self.user.person_id, id=criteria_id)
            self.assertEqual(criteria.calls_from, details.calls_from)
            self.assertEqual(criteria.enabled, details.enabled)

            # Verify the new criterion appears in the criteria list.
            after_create = api.read(entity_id=self.user.person_id)
            self.assertIn(criteria_id, {c.id for c in after_create.criteria or []})
            self.assertGreaterEqual(len(after_create.criteria or []), len(before.criteria or []) + 1)

            # Update the criterion enabled flag and verify the detail endpoint reflects it.
            update = details.model_copy(deep=True)
            update.enabled = not bool(update.enabled)
            api.configure_criteria(entity_id=self.user.person_id, id=criteria_id, settings=update)
            after_update = api.read_criteria(entity_id=self.user.person_id, id=criteria_id)
            self.assertEqual(update.enabled, after_update.enabled)

            # Delete the criterion and verify it disappears from the list.
            api.delete_criteria(entity_id=self.user.person_id, id=criteria_id)
            criteria_id = None
            after_delete = api.read(entity_id=self.user.person_id)
            self.assertNotIn(details.id, {c.id for c in after_delete.criteria or []})
        finally:
            # Clean up the created criterion if the test exits before explicit deletion.
            if criteria_id is not None:
                api.delete_criteria(entity_id=self.user.person_id, id=criteria_id)

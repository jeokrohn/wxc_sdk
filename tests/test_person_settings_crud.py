from tests.base import TestWithTempCallingUser


class TestPersonSettingsSimpleCrud(TestWithTempCallingUser):
    """
    Restore-safe read/modify coverage for person settings without separate child artifacts.
    """

    def test_top_level_get_modify_and_calling_services(self):
        """
        Read top-level person settings, call the no-op modify path, and verify settings are unchanged.
        """
        api = self.api.person_settings

        # Snapshot settings and read the service list for the disposable calling user.
        before = api.get(person_id=self.user.person_id)
        services = api.get_calling_services(person_id=self.user.person_id)
        self.assertIsInstance(services, list)
        if before.announcement_language is None and before.time_zone is None:
            self.skipTest('Temporary user has no timezone or announcement language to send in a no-op modify')

        # Send an idempotent modify request using the current language and timezone.
        api.modify(
            person_id=self.user.person_id,
            announcement_language=before.announcement_language,
            time_zone=before.time_zone,
        )

        # Read back the settings and verify the no-op modify left them unchanged.
        after = api.get(person_id=self.user.person_id)
        self.assertEqual(before, after)

    def test_anon_calls_toggle_restore(self):
        """
        Toggle anonymous call rejection for a disposable user and restore the original value.
        """
        api = self.api.person_settings.anon_calls

        # Snapshot the current anonymous-calls setting.
        before = api.read(entity_id=self.user.person_id)
        try:
            # Toggle the setting and verify the read endpoint reflects the change.
            api.configure(entity_id=self.user.person_id, enabled=not before)
            after = api.read(entity_id=self.user.person_id)
            self.assertEqual(not before, after)
        finally:
            # Restore the original setting and verify no side effect remains.
            api.configure(entity_id=self.user.person_id, enabled=before)
            restored = api.read(entity_id=self.user.person_id)
            self.assertEqual(before, restored)

    def test_hoteling_toggle_restore(self):
        """
        Toggle hoteling for a disposable user and restore the original value.
        """
        api = self.api.person_settings.hoteling

        # Snapshot the current hoteling setting.
        before = api.read(person_id=self.user.person_id)
        try:
            # Toggle the setting and verify the read endpoint reflects the change.
            api.configure(person_id=self.user.person_id, enabled=not before)
            after = api.read(person_id=self.user.person_id)
            self.assertEqual(not before, after)
        finally:
            # Restore the original setting and verify no side effect remains.
            api.configure(person_id=self.user.person_id, enabled=before)
            restored = api.read(person_id=self.user.person_id)
            self.assertEqual(before, restored)

    def test_call_waiting_toggle_restore(self):
        """
        Toggle call waiting for a disposable user and restore the original value.
        """
        api = self.api.person_settings.call_waiting

        # Snapshot the current call waiting setting.
        before = api.read(entity_id=self.user.person_id)
        try:
            # Toggle the setting and verify the read endpoint reflects the change.
            api.configure(entity_id=self.user.person_id, enabled=not before)
            after = api.read(entity_id=self.user.person_id)
            self.assertEqual(not before, after)
        finally:
            # Restore the original setting and verify no side effect remains.
            api.configure(entity_id=self.user.person_id, enabled=before)
            restored = api.read(entity_id=self.user.person_id)
            self.assertEqual(before, restored)

    def test_dnd_toggle_restore(self):
        """
        Toggle do-not-disturb for a disposable user and restore the original model.
        """
        api = self.api.person_settings.dnd

        # Snapshot the full DND settings model and prepare an updated copy.
        before = api.read(entity_id=self.user.person_id)
        update = before.model_copy(deep=True)
        update.enabled = not bool(update.enabled)
        try:
            # Configure the updated model and verify the enabled flag changed.
            api.configure(entity_id=self.user.person_id, dnd_settings=update)
            after = api.read(entity_id=self.user.person_id)
            self.assertEqual(update.enabled, after.enabled)
        finally:
            # Restore the original model and verify no side effect remains.
            api.configure(entity_id=self.user.person_id, dnd_settings=before)
            restored = api.read(entity_id=self.user.person_id)
            self.assertEqual(before, restored)

    def test_call_bridge_toggle_restore(self):
        """
        Toggle call bridge warning tone for a disposable user and restore the original model.
        """
        api = self.api.person_settings.call_bridge

        # Snapshot the full call bridge settings model and prepare an updated copy.
        before = api.read(entity_id=self.user.person_id)
        update = before.model_copy(deep=True)
        update.warning_tone_enabled = not update.warning_tone_enabled
        try:
            # Configure the updated model and verify the entire returned model matches.
            api.configure(entity_id=self.user.person_id, setting=update)
            after = api.read(entity_id=self.user.person_id)
            self.assertEqual(update, after)
        finally:
            # Restore the original model and verify no side effect remains.
            api.configure(entity_id=self.user.person_id, setting=before)
            restored = api.read(entity_id=self.user.person_id)
            self.assertEqual(before, restored)

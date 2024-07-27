"""
Unit test for voicemail settings
"""
import random
from concurrent.futures import ThreadPoolExecutor

from tests.base import TestCaseWithUsers


class VoicemailTests(TestCaseWithUsers):
    """
    Test cases for voicemail settings
    """

    # TODO: more tests

    def test_001_read_all(self):
        """
        read voicemail settings for all users
        """
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(
                lambda user: self.api.person_settings.voicemail.read(user.person_id),
                self.users))
        print(f'Got details for {len(details)} users')

    def test_002_configure(self):
        """
        Try to update VM settings of a random user with unchanged settings.
        """
        # random user
        target_user = random.choice(self.users)
        apv = self.api.person_settings.voicemail

        # current settings
        settings = apv.read(target_user.person_id)

        # update with current settings (check that some fields a are not send in update)
        apv.configure(entity_id=target_user.person_id, settings=settings)

        # get (updated) settings
        settings_after = apv.read(target_user.person_id)

        # there should be no difference
        self.assertEqual(settings, settings_after)

    def test_003_reset_vm_pin(self):
        """
        reset voicemail pin of random user
        """
        # random user
        target_user = random.choice(self.users)
        apv = self.api.person_settings.voicemail
        apv.reset_pin(target_user.person_id)

"""
Test for exec assistant settings
"""
import random
from concurrent.futures import ThreadPoolExecutor

from wxc_sdk.all_types import ExecAssistantType
from tests.base import TestCaseWithUsers


class TestRead(TestCaseWithUsers):

    def test_001_read_all(self):
        """
        Read exec assistant settings of all users
        """
        ea = self.api.person_settings.exec_assistant

        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda user: ea.read(person_id=user.person_id),
                                     self.users))
        print(f'Got exec assistant settings for {len(self.users)} users')
        max_len = max(len(user.display_name) for user in self.users)
        print('\n'.join(f'{user.display_name:{max_len}}: {s}' for user, s in zip(self.users, settings)))

    def test_002_update(self):
        """
        update exec assistant settings for a user
        """
        target = random.choice(self.users)
        ea = self.api.person_settings.exec_assistant
        setting = ea.read(person_id=target.person_id)
        try:
            # cycle through all possible values
            for new_setting in ExecAssistantType:
                if new_setting == setting:
                    continue
                ea.configure(person_id=target.person_id, setting=new_setting)
                after = ea.read(person_id=target.person_id)
                self.assertEqual(new_setting, after)
        finally:
            # restore old settings
            ea.configure(person_id=target.person_id, setting=setting)
            restored = ea.read(person_id=target.person_id)
            self.assertEqual(setting, restored)

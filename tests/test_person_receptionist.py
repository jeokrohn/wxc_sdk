"""
Test for receptionist client settings
"""
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from itertools import chain

from wxc_sdk.types import Person, ReceptionistSettings
from .base import TestCaseWithUsers


class TestRead(TestCaseWithUsers):

    def test_001_read_all(self):
        """
        Read settings of all users
        """
        rc = self.api.person_settings.receptionist

        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda user: rc.read(person_id=user.person_id),
                                     self.users))
        print(f'Got receptionist client settings for {len(self.users)} users')
        print('\n'.join(s.json() for s in settings))
        for user, setting in zip(self.users, settings):
            if not setting.enabled:
                continue
            print(f'{user.display_name}')
            for me in setting.monitored_members or []:
                print(f'  {me.display_name}')
                for n in me.numbers or []:
                    print(f'    {n.extension or "None":10} {n.external or "None":10}')

    @contextmanager
    def target_user(self):
        """
        Get target user
        """
        user = random.choice(self.users)
        print(f'target user: {user.display_name}')
        settings = self.api.person_settings.receptionist.read(person_id=user.person_id)
        try:
            yield user
        finally:
            # restore old settings
            self.api.person_settings.receptionist.configure(person_id=user.person_id, settings=settings)
            restored = self.api.person_settings.receptionist.read(person_id=user.person_id)
            self.assertEqual(settings, restored)

    def test_001_toggle_enabled(self):
        """
        Toggle enabled
        """
        with self.target_user() as user:
            rc = self.api.person_settings.receptionist
            user: Person
            before = rc.read(person_id=user.person_id)
            settings = ReceptionistSettings(enabled=not before.enabled)
            rc.configure(person_id=user.person_id, settings=settings)
            after = rc.read(person_id=user.person_id)
        self.assertEqual(settings.enabled, after.enabled)
        after.enabled = before.enabled
        if not before.monitored_members and not after.monitored_members:
            # None and [] are equivalent
            after.monitored_members = before.monitored_members
        self.assertEqual(before, after)

    def test_002_disable_all(self):
        """
        Disable receptionist client for all users
        """
        settings = ReceptionistSettings(enabled=False)
        rc = self.api.person_settings.receptionist
        with ThreadPoolExecutor() as pool:
            list(pool.map(lambda user: rc.configure(person_id=user.person_id, settings=settings),
                          self.users))

    def test_002_add_user_by_id(self):
        """
        Add some users by ID
        """
        with self.target_user() as user:
            # API shortcut
            rc = self.api.person_settings.receptionist
            # get current settings
            before = rc.read(person_id=user.person_id)
            present_ids = [m.member_id for m in before.monitored_members or []]
            user_candidates = [user for user in self.users
                               if user.person_id not in present_ids]
            to_add = random.sample(user_candidates, 3)

            # ths is what we want to add
            new_monitoring = [user.person_id
                              for user in to_add]
            settings = before.copy(deep=True)
            settings.enabled = True
            settings.monitored_members = (settings.monitored_members or []) + new_monitoring

            # update
            rc.configure(person_id=user.person_id, settings=settings)

            # how does it look like after the update?
            after = rc.read(person_id=user.person_id)

            # all new user ids need to be present now
            after_member_ids = set(member.member_id for member in after.monitored_members)
            new_user_ids = set(user.person_id for user in to_add)
            self.assertEqual(new_user_ids, after_member_ids & new_user_ids)
            self.assertTrue(after.enabled)

    def test_003_extension_format(self):
        """
        Verify extension format

        # TODO: defect, wrong extension format. Some extensions are returned as ESN with hyphen before the extension,
            # CALL-68675
        """
        with self.target_user() as user:
            # API shortcut
            rc = self.api.person_settings.receptionist
            # get current settings
            before = rc.read(person_id=user.person_id)
            present_ids = [m.member_id for m in before.monitored_members or []]
            user_candidates = [user for user in self.users
                               if user.person_id not in present_ids]
            to_add = random.sample(user_candidates, 3)
            print('Adding:')
            for u in to_add:
                print(f'  {u.display_name}: {u.phone_numbers}')

            # ths is what we want to add
            new_monitoring = [u.person_id
                              for u in to_add]
            settings = before.copy(deep=True)
            settings.enabled = True
            settings.monitored_members = (settings.monitored_members or []) + new_monitoring

            # update
            rc.configure(person_id=user.person_id, settings=settings)

            # how does it look like after the update?
            after = rc.read(person_id=user.person_id)

            max_disp = max(len(m.display_name) for m in after.monitored_members)
            for member in after.monitored_members:
                print(f'{member.display_name:{max_disp}}: '
                      f'{", ".join(n.extension for n in member.numbers if n.extension)}')
            extensions = list(chain.from_iterable((n.extension
                                                   for n in m.numbers if n.extension)
                                                  for m in after.monitored_members))
            # a hyphen in an extension is an indicator of an issue
            self.assertTrue(not any('-' in e for e in extensions), 'At least one extension has the wrong format')

"""
Test for receptionist client settings
"""
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from unittest import skip

from wxc_sdk.all_types import Person, ReceptionistSettings
from wxc_sdk.rest import RestError
from tests.base import TestCaseWithUsers


@skip('Receptionist client is not available anymore')
class TestRead(TestCaseWithUsers):

    # noinspection DuplicatedCode,PyShadowingNames
    def test_001_read_all(self):
        """
        Read settings of all users
        """
        rc = self.api.person_settings.receptionist

        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda user: rc.read(person_id=user.person_id),
                                     self.users))
        print(f'Got receptionist client settings for {len(self.users)} users')
        print('\n'.join(s.model_dump_json() for s in settings))
        for user, setting in zip(self.users, settings):
            if not setting.enabled:
                continue
            print(f'{user.display_name}')
            for me in setting.monitored_members or []:
                print(f'  {me.display_name}')
                for n in me.numbers or []:
                    print(f'    {n.extension or "None":10} {n.external or "None":10}')

    # noinspection DuplicatedCode
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

    # noinspection DuplicatedCode
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
            settings = before.model_copy(deep=True)
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
        Apparently extensions returned for members can have different formats:
            * ESN (site code - extension): the member is in a different location than the user
            * extension: the member is in the same location as the user
        """
        with self.target_user() as target_user:
            target_user: Person
            # get user details with calling data for all users
            with self.no_log():
                target_user = self.api.people.details(person_id=target_user.person_id, calling_data=True)
                with ThreadPoolExecutor() as pool:
                    users = list(pool.map(lambda u: self.api.people.details(person_id=u.person_id, calling_data=True),
                                          self.users))
            # API shortcut
            rc = self.api.person_settings.receptionist
            # get current settings
            before = rc.read(person_id=target_user.person_id)
            present_ids = [m.member_id for m in before.monitored_members or []]
            user_candidates = [user_candidate for user_candidate in users
                               if user_candidate.person_id not in present_ids and
                               target_user.person_id != user_candidate.person_id]
            if True:
                # add all users...
                to_add = user_candidates
            else:
                to_add = random.sample(user_candidates, 3)
            print('Adding:')
            for u in to_add:
                print(f'  {u.display_name}: {u.phone_numbers}')

            # ths is what we want to add
            new_monitoring = [u.person_id
                              for u in to_add]
            settings = before.model_copy(deep=True)
            settings.enabled = True
            settings.monitored_members = (settings.monitored_members or []) + new_monitoring

            # update
            try:
                rc.configure(person_id=target_user.person_id, settings=settings)
            except RestError as e:
                if e.code == 4470 and e.response.status_code == 400:
                    # apparently at least one of the users could not get added
                    # now try ot add them one by one and see which ones fail
                    print('Adding all users all at once failed. Now try to add them one by one...')
                    users_failed_to_add = []
                    monitored_members = before.monitored_members or []
                    for user_id in new_monitoring:
                        user_to_add = next(u for u in users if u.person_id == user_id)
                        settings.monitored_members = monitored_members + [user_id]
                        try:
                            rc.configure(person_id=target_user.person_id, settings=settings)
                        except RestError as ie:
                            if ie.code == 4470:
                                users_failed_to_add.append(user_id)
                        else:
                            monitored_members.append(user_id)
                    print('failed users: ', end='')
                    print(', '.join((failed_user := next(u for u in users if u.person_id == user_id)).display_name
                                    for user_id in users_failed_to_add))
                    raise e
                else:
                    raise

            # how does it look like after the update?
            after = rc.read(person_id=target_user.person_id)

            max_disp = max(len(m.display_name) for m in after.monitored_members)
            after.monitored_members.sort(key=lambda m: m.display_name)
            print('Members:')
            err = False
            for member in after.monitored_members:
                member_user = next(u for u in users if u.person_id == member.member_id)

                def user_number(n):
                    numbers = [ee for ee in (n.extension, n.external) if ee]
                    if len(numbers) > 1:
                        return f'({"/".join(numbers)})'
                    return numbers[0]

                print(f'  {member.display_name:{max_disp}}: '
                      f'{", ".join(user_number(n) for n in member.numbers)}'
                      f'{"" if member_user.location_id == target_user.location_id else " not"} '
                      f'in same location as target user')
                if any(n.extension and '-' in n.extension
                       for n in member.numbers) != (member_user.location_id != target_user.location_id):
                    err = True
            # a hyphen in an extension is an indicator of an issue
            self.assertFalse(err, 'At least one extension has the wrong format')

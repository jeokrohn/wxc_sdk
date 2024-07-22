"""
Test for person PTT settings
"""
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass

from wxc_sdk.all_types import *
from tests.base import TestCaseWithUsers


class TestRead(TestCaseWithUsers):

    def test_001_read_all(self):
        """
        Read PTT settings of all users
        """
        ptt = self.api.person_settings.push_to_talk

        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda user: ptt.read(entity_id=user.person_id),
                                     self.users))
        print(f'Got PTT settings for {len(self.users)} users')
        print('\n'.join(s.model_dump_json() for s in settings))


@dataclass(init=False)
class TestUpdate(TestCaseWithUsers):

    @contextmanager
    def target_user(self):
        """
        Get target user
        """
        user = random.choice(self.users)
        ptt = self.api.person_settings.push_to_talk
        settings = ptt.read(entity_id=user.person_id)
        try:
            yield user
        finally:
            # restore old settings
            ptt.configure(entity_id=user.person_id, settings=settings)
            restored = ptt.read(entity_id=user.person_id)
            self.assertEqual(settings, restored)

    def test_001_toggle_allow_auto_answer(self):
        """
        Toggle allow_auto_answer on random user
        """
        with self.target_user() as user:
            ptt = self.api.person_settings.push_to_talk
            user: Person
            before = ptt.read(entity_id=user.person_id)
            settings = PushToTalkSettings(allow_auto_answer=not before.allow_auto_answer)
            ptt.configure(entity_id=user.person_id, settings=settings)
            after = ptt.read(entity_id=user.person_id)
            self.assertEqual(settings.allow_auto_answer,
                             after.allow_auto_answer)
            after.allow_auto_answer = before.allow_auto_answer
            self.assertEqual(before, after)

    def test_002_toggle_connection_type(self):
        """
        Toggle connection_type on random user
        """
        with self.target_user() as user:
            ptt = self.api.person_settings.push_to_talk
            user: Person
            before = ptt.read(entity_id=user.person_id)
            settings = PushToTalkSettings(connection_type=next(ct for ct in PTTConnectionType
                                                               if ct != before.connection_type))
            ptt.configure(entity_id=user.person_id, settings=settings)
            after = ptt.read(entity_id=user.person_id)
            self.assertEqual(settings.connection_type,
                             after.connection_type)
            after.connection_type = before.connection_type
            self.assertEqual(before, after)

    def test_003_toggle_access_type(self):
        """
        Toggle access_type on random user
        """
        with self.target_user() as user:
            ptt = self.api.person_settings.push_to_talk
            user: Person
            before = ptt.read(entity_id=user.person_id)
            settings = PushToTalkSettings(access_type=next(at for at in PushToTalkAccessType
                                                           if at != before.access_type))
            ptt.configure(entity_id=user.person_id, settings=settings)
            after = ptt.read(entity_id=user.person_id)
            self.assertEqual(settings.access_type,
                             after.access_type)
            after.access_type = before.access_type
            self.assertEqual(before, after)

    def test_004_add_members(self):
        """
        Toggle access_type on random user
        """
        with self.target_user() as user:
            ptt = self.api.person_settings.push_to_talk
            user: Person
            before = ptt.read(entity_id=user.person_id)
            members_before = before.members or []
            members_before_ids = set(m.member_id for m in members_before)

            candidates = [user for user in self.users if user.person_id not in members_before_ids]
            if len(candidates) < 5:
                self.skipTest('Need at least 5 users to add')
            to_add = random.sample(candidates, 5)
            settings = PushToTalkSettings(members=[MonitoredMember(member_id=u.person_id) for u in to_add])
            ptt.configure(entity_id=user.person_id, settings=settings)
            after = ptt.read(entity_id=user.person_id)
            self.assertEqual(len(to_add), len(after.members))
            to_add_set = set(m.person_id for m in to_add)
            members_set_after = set(m.member_id for m in after.members)
            self.assertEqual(to_add_set, members_set_after)
            after.members = before.members
            self.assertEqual(before, after)

    def test_005_add_members_by_id(self):
        """
        Toggle access_type on random user
        """
        with self.target_user() as user:
            ptt = self.api.person_settings.push_to_talk
            user: Person
            before = ptt.read(entity_id=user.person_id)
            members_before = before.members or []
            members_before_ids = set(m.member_id for m in members_before)

            candidates = [user for user in self.users if user.person_id not in members_before_ids]
            if len(candidates) < 5:
                self.skipTest('Need at least 5 users to add')
            to_add = random.sample(candidates, 5)
            settings = PushToTalkSettings(members=[u.person_id for u in to_add])
            ptt.configure(entity_id=user.person_id, settings=settings)
            after = ptt.read(entity_id=user.person_id)
            self.assertEqual(len(to_add), len(after.members))
            to_add_set = set(m.person_id for m in to_add)
            members_set_after = set(m.member_id for m in after.members)
            self.assertEqual(to_add_set, members_set_after)
            after.members = before.members
            self.assertEqual(before, after)

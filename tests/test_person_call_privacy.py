"""
Test for privacy settings
"""
import asyncio
import base64
import random
from contextlib import contextmanager
from dataclasses import dataclass

from tests.base import TestCaseWithUsers, async_test
from wxc_sdk.all_types import Person, Privacy


class TestRead(TestCaseWithUsers):

    @async_test
    async def test_001_read_all(self):
        """
        Read privacy setting of all users
        """
        ps = self.async_api.person_settings.privacy

        await asyncio.gather(*[ps.read(user.person_id) for user in self.users])

        print(f'Got privacy settings for {len(self.users)} users')


@dataclass(init=False)
class TestUpdate(TestCaseWithUsers):

    @contextmanager
    def target_user(self):
        """
        Get target user
        """
        user = random.choice(self.users)
        settings = self.api.person_settings.privacy.read(user.person_id)
        try:
            yield user
        finally:
            # restore old settings
            # makes sure to clear list of monitored elements
            settings.monitoring_agents = settings.monitoring_agents or []
            self.api.person_settings.privacy.configure(user.person_id, settings=settings)
            settings.monitoring_agents = settings.monitoring_agents or None
            restored = self.api.person_settings.privacy.read(user.person_id)
            self.assertEqual(settings, restored)

    def test_001_toggle_aa_extension_dialing_enabled(self):
        """
        Toggle aa_extension_dialing_enabled on random user
        """
        with self.target_user() as user:
            priv = self.api.person_settings.privacy
            user: Person
            before = priv.read(user.person_id)
            settings = Privacy(aa_extension_dialing_enabled=not before.aa_extension_dialing_enabled)
            priv.configure(user.person_id, settings=settings)
            after = priv.read(user.person_id)
        self.assertEqual(settings.aa_extension_dialing_enabled, after.aa_extension_dialing_enabled)
        after.aa_extension_dialing_enabled = before.aa_extension_dialing_enabled
        self.assertEqual(before, after)

    def test_002_toggle_enable_phone_status_directory_privacy(self):
        """
        Toggle enable_phone_status_directory_privacy on random user
        """
        with self.target_user() as user:
            priv = self.api.person_settings.privacy
            user: Person
            before = priv.read(user.person_id)
            settings = Privacy(enable_phone_status_directory_privacy=not before.enable_phone_status_directory_privacy)
            priv.configure(user.person_id, settings=settings)
            after = priv.read(user.person_id)
        self.assertEqual(settings.enable_phone_status_directory_privacy, after.enable_phone_status_directory_privacy)
        after.enable_phone_status_directory_privacy = before.enable_phone_status_directory_privacy
        self.assertEqual(before, after)

    def test_003_add_user_by_id(self):
        """
        Add some users by ID
        """
        with self.target_user() as user:
            # API shortcut
            priv = self.api.person_settings.privacy
            # get current settings
            before = priv.read(user.person_id)
            present_ids = [agent.agent_id for agent in before.monitoring_agents or []]
            user_candidates = [user for user in self.users
                               if user.person_id not in present_ids]
            to_add = random.sample(user_candidates, 3)

            # ths is what we want to add
            new_agents = [user.person_id
                          for user in to_add]
            settings = Privacy(
                monitoring_agents=(before.monitoring_agents or []) + new_agents)

            # update
            priv.configure(user.person_id, settings=settings)

            # how does it look like after the update?
            after = priv.read(user.person_id)

        # all new user ids need to be present now
        after_agent_ids = set(agent.agent_id for agent in after.monitoring_agents)
        new_user_ids = set(user.person_id for user in to_add)
        try:
            self.assertEqual(new_user_ids, after_agent_ids & new_user_ids)
        except AssertionError as e:
            new_ids_missing = new_user_ids - after_agent_ids
            for new_id in new_ids_missing:
                print(f'New ID missing: {new_id}, {base64.b64decode(new_id + "==").decode()}')
            unexpected_ids = after_agent_ids - set(agent.agent_id for agent in before.monitoring_agents or []) - \
                new_user_ids
            for unexpected_id in unexpected_ids:
                print(f'Unexpected ID: {unexpected_id}, {base64.b64decode(unexpected_id + "==").decode()}')
            raise

        # other than that nothing should've changed
        after.monitoring_agents = before.monitoring_agents
        self.assertEqual(before, after)

    def test_004_verify_agent_id_format(self):
        """
        verify format of agent IDs
        # TODO: defect, wrong agent id format; broadcloud ID instead of UUID, CALL-68642
        """
        with self.target_user() as target_user:
            # API shortcut
            priv = self.api.person_settings.privacy

            # get current settings
            before = priv.read(target_user.person_id)
            present_ids = [agent.agent_id for agent in before.monitoring_agents or []]
            user_candidates = [user for user in self.users
                               if user.person_id not in present_ids and user.person_id != target_user.person_id]
            to_add = random.sample(user_candidates, 3)

            # ths is what we want to add
            new_agents = [user.person_id
                          for user in to_add]
            settings = Privacy(
                monitoring_agents=(before.monitoring_agents or []) + new_agents)

            # update
            priv.configure(target_user.person_id, settings=settings)

            # how does it look like after the update?
            after = priv.read(target_user.person_id)

        decoded_agent_ids = list(map(lambda agent: base64.b64decode(agent.agent_id + '==').decode(),
                                     after.monitoring_agents))
        for agent, decoded in zip(after.monitoring_agents, decoded_agent_ids):
            print(f'id: {agent.agent_id} -> {decoded}')
        # an "@" in the decoded agent IDs is an indicator that broadcloud IDs are returned instead of proper user IDs
        self.assertTrue(not any('@' in d for d in decoded_agent_ids), "wrong format for agent IDs")

"""
Test for call monitoring settings
"""
import asyncio
import base64
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass
from typing import ClassVar, Optional

from wxc_sdk import WebexSimpleApi
from wxc_sdk.all_types import *
from wxc_sdk.as_api import AsWebexSimpleApi
from tests.base import TestCaseWithUsers


def print_monitoring(*, user: Person, monitoring: Monitoring):
    print(f'user: {user.display_name}')
    print(f'  call park notifications enabled: {monitoring.call_park_notification_enabled}')
    for me in monitoring.monitored_elements or []:
        if me.member:
            print(f'    {me.member.display_name} ({me.member.member_type}) in {me.member.location_name}')
        else:
            print(f'    {me.cpe.name} (CPE) in {me.cpe.location_name}')


class TestRead(TestCaseWithUsers):

    def test_001_read_all(self):
        """
        Read monitoring setting of all users
        """
        ps = self.api.person_settings

        with ThreadPoolExecutor() as pool:
            monitoring_settings = list(pool.map(lambda user: ps.monitoring.read(entity_id=user.person_id),
                                                self.users))
        print(f'Got monitoring details for {len(self.users)} users')
        with_elements = [(user, ms) for user, ms in zip(self.users, monitoring_settings)
                         if ms.monitored_elements]
        for user, ms in with_elements:
            print_monitoring(user=user, monitoring=ms)


@dataclass(init=False)
class TempCPE:
    api: WebexSimpleApi
    generated_cpe_ids: list[str]
    location_id: str

    def __init__(self, api: WebexSimpleApi):
        self.api = api

    async def cleanup(self):
        async with AsWebexSimpleApi(tokens=self.api.access_token) as api:
            tasks = [api.telephony.callpark_extension.delete(location_id=self.location_id, cpe_id=cpe_id)
                     for cpe_id in self.generated_cpe_ids]
            self.generated_cpe_ids = []
            await asyncio.gather(*tasks)

    @contextmanager
    def generate_cpes(self, cpes_present: list[CallParkExtension], cpe_count: int = 1) -> list[str]:
        """
        get a number of CPEs to add as monitored elements to given monitoring settings
        create new CPEs if needed using CPAPI
        """

        async def get_cpes() -> list[str]:
            async with AsWebexSimpleApi(tokens=self.api.access_token) as api:
                existing_cpes = await api.telephony.callpark_extension.list()

                # CPE ids currently used as member
                ids_cpes_present = set(cpe.cpe_id for cpe in cpes_present)

                # ids of CPEs which can be added: all cpes not currently used
                available_ci_cpe_ids = [cpe.cpe_id
                                        for cpe in existing_cpes
                                        if cpe.cpe_id not in ids_cpes_present]

                # are we missing any to be able to fulfill the request?
                missing = max(cpe_count - len(available_ci_cpe_ids), 0)
                if missing:
                    # we need to create a bunch of CPEs
                    # pick a random location
                    locations = await api.locations.list()

                    location_id = random.choice(locations).location_id
                    self.location_id = location_id
                    cpe_names = set(cpe.name for cpe in existing_cpes
                                    if cpe.location_id == location_id)
                    new_names = (name for i in range(1000)
                                 if (name := f'cpe_{i:03}') not in cpe_names)

                    # assumption: we can assign new extensions to CPEs in ascending order
                    extensions = [int(cpe.extension)
                                  for cpe in existing_cpes
                                  if cpe.location_id == location_id]
                    extensions = extensions or [1100]
                    max_cpe_extension = max(extensions)

                    tasks = [api.telephony.callpark_extension.create(location_id=location_id,
                                                                     name=next(new_names),
                                                                     extension=str(max_cpe_extension + i + 1))
                             for i in range(missing)]
                    self.generated_cpe_ids = await asyncio.gather(*tasks)
                    available_ci_cpe_ids.extend(self.generated_cpe_ids)

            result = random.sample(available_ci_cpe_ids, cpe_count)
            return result

        self.generated_cpe_ids = []
        cpe_list = asyncio.run(get_cpes())

        try:
            yield cpe_list
        finally:
            # remove creates CPEs
            if self.generated_cpe_ids:
                asyncio.run(self.cleanup())


@dataclass(init=False)
class TestUpdate(TestCaseWithUsers):
    callpark_extensions: ClassVar[Optional[list[CallParkExtension]]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.callpark_extensions = list(cls.api.telephony.callpark_extension.list())

    @contextmanager
    def target_user(self):
        """
        Get target user
        """
        user = random.choice(self.users)
        settings = self.api.person_settings.monitoring.read(entity_id=user.person_id)
        print('Before')
        print_monitoring(user=user, monitoring=settings)
        try:
            yield user
        finally:
            # restore old settings
            # makes sure to clear list of monitored elements
            settings.monitored_elements = settings.monitored_elements or []
            self.api.person_settings.monitoring.configure(entity_id=user.person_id, settings=settings)
            settings.monitored_elements = settings.monitored_elements or None
            restored = self.api.person_settings.monitoring.read(entity_id=user.person_id)
            self.assertEqual(settings, restored)

    def test_001_toggle_notifications(self):
        """
        Toggle call_park_notification_enabled on random user
        """
        with self.target_user() as user:
            mon = self.api.person_settings.monitoring
            user: Person
            before = mon.read(entity_id=user.person_id)
            settings = Monitoring(call_park_notification_enabled=not before.call_park_notification_enabled)
            mon.configure(entity_id=user.person_id, settings=settings)
            after = mon.read(entity_id=user.person_id)
            print_monitoring(user=user, monitoring=after)
        self.assertEqual(settings.call_park_notification_enabled, after.call_park_notification_enabled)
        after.call_park_notification_enabled = before.call_park_notification_enabled
        self.assertEqual(before, after)

    def test_002_add_cpe_by_id(self):
        """
        Add some CPEs by ID
        """
        with self.target_user() as user:
            # API shortcut
            mon = self.api.person_settings.monitoring
            # get current settings
            before = mon.read(entity_id=user.person_id)
            # get some CPE ids to add
            temp_cpe = TempCPE(api=self.api)
            with temp_cpe.generate_cpes(cpes_present=before.monitored_cpes, cpe_count=8) as new_cpe_ids:
                # ths is what we want to add
                new_monitoring_elements = [cpe_id
                                           for cpe_id in new_cpe_ids]
                settings = Monitoring(
                    monitored_elements=(before.monitored_elements or []) + new_monitoring_elements)

                # update
                mon.configure(entity_id=user.person_id, settings=settings)

                # how does it look like after the update?
                after = mon.read(entity_id=user.person_id)
                print_monitoring(user=user, monitoring=after)
            # with
        # with

        # all new CPE ids need to be present now
        after_cpe_ids = set(cpe.cpe_id for cpe in after.monitored_cpes)
        new_cpe_ids = set(new_cpe_ids)
        self.assertEqual(new_cpe_ids, after_cpe_ids & new_cpe_ids)

        # other than that nothing should've changed
        after.monitored_elements = before.monitored_elements
        self.assertEqual(before, after)

    def test_003_add_user_by_id(self):
        """
        Add some users by ID
        """
        with self.target_user() as user:
            # API shortcut

            mon = self.api.person_settings.monitoring
            # get current settings
            before = mon.read(entity_id=user.person_id)
            present_ids = [m.member_id for m in before.monitored_members]
            user_candidates = [uc for uc in self.users
                               if uc.person_id not in present_ids and uc.person_id != user.person_id]
            to_add = random.sample(user_candidates, 3)
            to_add: list[Person]
            print(f'Trying to add monitoring for: {", ".join(u.display_name for u in to_add)}')

            # ths is what we want to add
            new_monitoring_elements = [user.person_id
                                       for user in to_add]
            settings = Monitoring(
                monitored_elements=(before.monitored_elements or []) + new_monitoring_elements)

            # update
            mon.configure(entity_id=user.person_id, settings=settings)

            # how does it look like after the update?
            after = mon.read(entity_id=user.person_id)
            print_monitoring(user=user, monitoring=after)

        # all new user ids need to be present now
        after_member_ids = set(member.member_id for member in after.monitored_members)
        new_user_ids = set(user.person_id for user in to_add)
        self.assertEqual(new_user_ids, after_member_ids & new_user_ids)

        # other than that nothing should've changed
        after.monitored_elements = before.monitored_elements
        self.assertEqual(before, after)

    def test_004_verify_user_id_format(self):
        """
        Verify user ID format
        """
        with self.target_user() as user:
            # API shortcut
            mon = self.api.person_settings.monitoring
            # get current settings
            before = mon.read(entity_id=user.person_id)
            present_ids = [m.member_id for m in before.monitored_members]
            user_candidates = [user for user in self.users
                               if user.person_id not in present_ids]
            to_add = random.sample(user_candidates, 3)
            print(f'Trying to add monitoring for: {", ".join(u.display_name for u in to_add)}')

            # ths is what we want to add
            new_monitoring_elements = [user.person_id
                                       for user in to_add]
            settings = Monitoring(
                monitored_elements=(before.monitored_elements or []) + new_monitoring_elements)

            # update
            mon.configure(entity_id=user.person_id, settings=settings)

            # how does it look like after the update?
            after = mon.read(entity_id=user.person_id)
            print_monitoring(user=user, monitoring=after)

        decoded_user_ids = list(map(lambda member: base64.b64decode(member.member_id + '==').decode(),
                                    after.monitored_members))
        for member, decoded in zip(after.monitored_members, decoded_user_ids):
            print(f'id: {member.member_id} -> {decoded}')
        self.assertTrue(not any('@' in d for d in decoded_user_ids), "wrong format for member IDs")

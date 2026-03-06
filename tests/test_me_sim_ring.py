import asyncio
import json
import random
from typing import List, Tuple, Union

from tests.base import TestWithRandomUserApi, async_test
from wxc_sdk.all_types import *
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.as_rest import AsRestError


class TestMeSimRing(TestWithRandomUserApi):
    # proxy = True

    @async_test
    async def test_get_settings(self):
        """
        Get sim ring settings for all users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.sim_ring.get()
                    except AsRestError as e:
                        raise e
            # end of get_settings
            return

        users = [user
                 for user in self.users
                 if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error sim ring settings for {user.display_name}: {result}")
            elif result is not None:
                result: MeSimRing
                print(f"sim ring settings for {user.display_name}: ")

                print(json.dumps(result.model_dump(mode='json', exclude_unset=True,
                                                   exclude_none=True),
                                 indent=2))
        if err:
            raise err

    @async_test
    async def test_get_settings_and_criteria(self):
        """
        Get sim ring settings and criteria for all users
        """

        R_TYPE = Tuple[MeSimRing, List[Union[Exception, SimRingCriteria]]]

        async def get_settings(user: Person) -> R_TYPE:
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    sr_api = as_api.me.sim_ring
                    try:
                        settings = await sr_api.get()
                        criteria_list = await asyncio.gather(*[sr_api.criteria_get(criteria_id=c.id)
                                                               for c in settings.criteria],
                                                             return_exceptions=True)
                        return settings, criteria_list
                    except AsRestError as e:
                        raise e
            # end of get_settings
            return

        users = [user
                 for user in self.users
                 if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error sim ring settings for {user.display_name}: {result}")
                continue
            result: R_TYPE
            settings, criteria_list = result
            print(f'Sim ring settings for {user.display_name}')
            print(json.dumps(settings.model_dump(mode='json', exclude_none=True, by_alias=True),
                             indent=2))
            if criteria_list:
                print(f'Sim ring criteria for {user.display_name}')
                for criteria in criteria_list:
                    if isinstance(criteria, Exception):
                        err = err or criteria
                        print(f'Error: {criteria}')
                        continue
                    print(json.dumps(criteria.model_dump(mode='json', exclude_none=True, by_alias=True),
                                     indent=2))
                #
            print()
            #
        if err:
            raise err

    @async_test
    async def test_enable_sim_ring(self):
        """
        enable sim ring for a user
        """
        # get sim ring settings for all users
        users = [user
                 for user in self.users
                 if not user.display_name.startswith('admin@')]

        async def get_settings(user: Person) -> MeSimRing:
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    sr_api = as_api.me.sim_ring
                    return await sr_api.get()
            # end of get_settings
            return

        settings = await asyncio.gather(*[get_settings(user) for user in users])
        settings: List[MeSimRing]

        # pick random user that doesn't have sim ring enabled
        user, setting = random.choice([(user, setting)
                                       for user, setting in zip(users, settings)
                                       if not setting.enabled and not setting.criteria and not setting.phone_numbers])
        user: Person
        setting: MeSimRing

        print(f'Testing with {user.display_name}')
        with self.user_api(user) as api:
            sr_api = api.me.sim_ring
            # update setting
            new_setting = MeSimRing(enabled=True,
                                    phone_numbers=[MeSimRingNumber(phone_number='1234',
                                                                   answer_confirmation_enabled=True)])
            sr_api.update(new_setting)
            try:
                # get settings
                settings_after = sr_api.get()
                expected = setting.model_copy(deep=True)
                expected.enabled = new_setting.enabled
                expected.phone_numbers = new_setting.phone_numbers
                self.assertEqual(settings_after, expected)

                # create criteria
                phone_numbers = [f'+496100773976{i}' for i in range(1, 10)]
                new_criteria = SimRingCriteria(calls_from=SelectiveFrom.select_phone_numbers,
                                               phone_numbers=phone_numbers,
                                               anonymous_callers_enabled=True,
                                               unavailable_callers_enabled=True,
                                               enabled=True)

                criteria_id = sr_api.criteria_create(new_criteria)
                try:
                    settings_after = sr_api.get()
                    self.assertEqual(1, len(settings_after.criteria))
                    self.assertTrue(settings_after.criterias_enabled)
                    self.assertEqual(criteria_id, settings_after.criteria[0].id)

                    # read criteria
                    criteria_read = sr_api.criteria_get(criteria_id=criteria_id)
                    self.assertEqual(phone_numbers, criteria_read.phone_numbers)

                finally:
                    # delete criteria again
                    sr_api.criteria_delete(criteria_id)
            finally:
                # reset sim ring settings
                setting.phone_numbers = []
                sr_api.update(setting)
        return

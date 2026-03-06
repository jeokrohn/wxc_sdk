import asyncio
import json
import random
from typing import List, Tuple

from pydantic import TypeAdapter
from tests.base import TestWithRandomUserApi, async_test
from wxc_sdk.all_types import *
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.as_rest import AsRestError
from wxc_sdk.me.call_notify import CallNotifyCriteria


class TestMePriorityAlert(TestWithRandomUserApi):
    # proxy = True

    @async_test
    async def test_settings(self):
        """
        get priority alert settings for all users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.priority_alert.get()
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
                print(f"Error priority alert settings for {user.display_name}: {result}")
            elif result is not None:
                result: PriorityAlert
                print(f"Call priority alert for {user.display_name}: ")

                print(json.dumps(
                    TypeAdapter(PriorityAlert).dump_python(result, mode='json', exclude_unset=True,
                                                            exclude_none=True),
                    indent=2))
        if err:
            raise err

    @async_test
    async def test_call_notify_criteria(self):
        """
        Get call notify settings and criteria for all users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    cn_api = as_api.me.call_notify
                    try:
                        cn_settings = await cn_api.get()
                        tasks = []
                        for crit in cn_settings.criteria:
                            tasks.append(cn_api.criteria_get(id=crit.id))
                        if tasks:
                            criteria = await asyncio.gather(*tasks, return_exceptions=True)
                        else:
                            criteria = []
                        return cn_settings, criteria
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
                print(f"Call notify settings for {user.display_name}: {result}")
            elif result is not None:
                result: Tuple[CallNotify, List[CallNotifyCriteria]]
                cn_settings, criteria = result
                print(f"Call notify settings for {user.display_name}: ")
                print(json.dumps(cn_settings.model_dump(mode='json', by_alias=True, exclude_none=True), indent=2))
                if criteria:
                    print()
                    print(json.dumps(
                        TypeAdapter(List[CallNotifyCriteria]).dump_python(criteria, mode='json', exclude_unset=True,
                                                                exclude_none=True),
                        indent=2))
        if err:
            raise err

    def test_create_criteria(self):
        """
        Create a new call notifycriteria for a user
        """
        # pick random users
        users = [user
                 for user in self.users
                 if not user.display_name.startswith('admin@')]
        user = random.choice(users)
        print(f'Creating call notify criteria for "{user.display_name}"')

        with (self.user_api(user) as api):
            cn_api = api.me.call_notify
            cn_settings = cn_api.get()

            # pick a schedule not yet used
            schedules_used = set(c.schedule_name for c in cn_settings.criteria)
            unused_schedules = [s for s in api.me.schedules.list() if s.name not in schedules_used]
            if not unused_schedules:
                self.skipTest("No schedules available")
            schedule = random.choice(unused_schedules)

            new_criteria = CallNotifyCriteria(calls_from=SelectiveFrom.any_phone_number, enabled=True)
            crit_id = cn_api.criteria_create(new_criteria)
            try:
                cn_settings_after = cn_api.get()
            finally:
                cn_api.criteria_delete(crit_id)
        return

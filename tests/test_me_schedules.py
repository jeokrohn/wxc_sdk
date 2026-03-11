import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import List

from pydantic import TypeAdapter

from tests.base import TestWithRandomUserApi, async_test
from wxc_sdk.all_types import *
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.as_rest import AsRestError


class TestMeSchedules(TestWithRandomUserApi):
    # proxy = True

    @async_test
    async def test_list(self):
        """
        List schedules for all users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.schedules.list()
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
                print(f"Error schedules for {user.display_name}: {result}")
            elif result is not None:
                result: List[Schedule]
                print(f"Schedules for {user.display_name}: ")

                print(json.dumps(
                    TypeAdapter(List[Schedule]).dump_python(result, mode='json', exclude_unset=True,
                                                            exclude_none=True),
                    indent=2))
        if err:
            raise err

    @async_test
    async def test_schedule_details(self):
        """
        List schedules for all users and get details for all schedules
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        schedules = await as_api.me.schedules.list()
                        tasks = []
                        for schedule in schedules:
                            if schedule.level == ScheduleLevel.people:
                                tasks.append(as_api.me.schedules.get_user_schedule(
                                    schedule_type=schedule.schedule_type,
                                    schedule_id=schedule.schedule_id))
                            else:
                                tasks.append(as_api.me.schedules.get_location_schedule(
                                    schedule_type=schedule.schedule_type,
                                    schedule_id=schedule.schedule_id))
                        if tasks:
                            details = await asyncio.gather(*tasks, return_exceptions=True)
                            return details
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
                print(f"Error schedules for {user.display_name}: {result}")
            elif result is not None:
                result: List[Schedule]
                print(f"Schedules for {user.display_name}: ")

                print(json.dumps(
                    TypeAdapter(List[Schedule]).dump_python(result, mode='json', exclude_unset=True,
                                                            exclude_none=True),
                    indent=2))
        if err:
            raise err

    def test_create_schedule(self):
        """
        Create a new schedule for a random user
        """
        # pick random users
        users = [user
                 for user in self.users
                 if not user.display_name.startswith('admin@')]
        user = random.choice(users)
        print(f'Creating schedule for "{user.display_name}"')

        with (self.user_api(user) as api):
            sapi = api.me.schedules
            # list all schedules
            schedules = sapi.list()

            # pick a new schedule name
            names = set(s.name for s in schedules)
            new_name = next((s_name for i in range(1, 100) if (s_name := f'test {i:02}') not in names))
            # create schedule
            today = datetime.today()
            tomorrow = today + timedelta(days=1)
            new_schedule = Schedule(
                name=new_name, schedule_type=ScheduleType.holidays,
                events=[Event(
                    name='bday', start_date=tomorrow.date(), end_date=tomorrow.date(), all_day_enabled=True,
                    recurrence=Recurrence(
                        recur_end_occurrence=10,
                        recur_weekly=RecurWeekly.single_day(tomorrow, recur_interval=1)))])
            sched_id = sapi.create(new_schedule)
            try:
                # get details of new schedule
                schedule = sapi.get_user_schedule(schedule_type=ScheduleType.holidays, schedule_id=sched_id)
                self.assertEqual(schedule.create_update(), new_schedule.create_update())
            finally:
                # delete schedule again
                sapi.delete(schedule_type=ScheduleType.holidays, schedule_id=sched_id)
        return

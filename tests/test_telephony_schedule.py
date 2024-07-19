"""
Unit test for Schedules
"""
import asyncio
# TODO: testcase for event update
# TODO test case for event delete
# TODO test case for schedule delete
import datetime
import random
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from itertools import chain
from typing import ClassVar

from tests.base import TestWithLocations, async_test
from wxc_sdk.all_types import *


class TestScheduleList(TestWithLocations):
    """
    Test cases for schedules
    """

    def all_schedules(self) -> list[Schedule]:
        """
        Get all existing schedules in all locations
        :return: list of schedules
        """
        with ThreadPoolExecutor() as pool:
            lists = pool.map(lambda loc: list(self.api.telephony.schedules.list(obj_id=loc.location_id)),
                             self.locations)
            schedules = list(chain.from_iterable(lists))
        return schedules

    def test_001_list(self):
        """
        Try to list all existing schedules in all locations
        """
        schedules = self.all_schedules()
        print(f'got {len(schedules)} schedules')
        print('\n'.join(f'{s}' for s in schedules))

    def test_002_list_name(self):
        """
        Try to list by name
        """
        with ThreadPoolExecutor() as pool:
            lists = pool.map(lambda loc: self.api.telephony.schedules.list(obj_id=loc.location_id,
                                                                           name='Germany 2'),
                             self.locations)
            schedules = list(chain.from_iterable(lists))
            schedules: list[Schedule]
            print(f'got {len(schedules)} schedules')
            print('\n'.join(f'{s}' for s in schedules))
            self.assertTrue(all(schedule.name.startswith('Germany 2') for schedule in schedules),
                            'Not all schedule names start with the expected string')

    def test_003_list_business_hours(self):
        """
        List all business hours schedules in all locations
        """
        with ThreadPoolExecutor() as pool:
            lists = pool.map(
                lambda loc: list(self.api.telephony.schedules.list(obj_id=loc.location_id,
                                                                   schedule_type=ScheduleType.business_hours)),
                self.locations)
            schedules = list(chain.from_iterable(lists))
        schedules: list[Schedule]
        print(f'got {len(schedules)} schedules')
        print('\n'.join(f'{s}' for s in schedules))
        self.assertTrue(all(schedule.schedule_type == ScheduleType.business_hours for schedule in schedules),
                        'Schedule type mismatch')

    def test_004_all_detail(self):
        """
        Get details of all schedules
        """
        schedules = self.all_schedules()
        with ThreadPoolExecutor() as pool:
            details = pool.map(
                lambda schedule: self.api.telephony.schedules.details(obj_id=schedule.location_id,
                                                                      schedule_type=schedule.schedule_type,
                                                                      schedule_id=schedule.schedule_id),
                schedules)
            details = list(details)
        print(f'Got details for {len(details)} schedules')

    def test_005_all_event_details(self):
        """
        Get all event details of all schedules
        """
        schedules = self.all_schedules()

        def schedule_event_details(schedule: Schedule):
            """
            get details of all events in given schedule
            :param schedule: schedule
            :type schedule: Schedule
            :return: list of schedules
            """
            details = self.api.telephony.schedules.details(
                obj_id=schedule.location_id,
                schedule_type=schedule.schedule_type,
                schedule_id=schedule.schedule_id)
            details: Schedule
            if not details.events:
                return list()
            with ThreadPoolExecutor() as pool:
                event_details = pool.map(
                    lambda event: self.api.telephony.schedules.event_details(obj_id=schedule.location_id,
                                                                             schedule_type=schedule.schedule_type,
                                                                             schedule_id=schedule.schedule_id,
                                                                             event_id=event.event_id),
                    details.events)
                event_details = list(event_details)
            return event_details

        with ThreadPoolExecutor() as pool:
            event_details = pool.map(lambda schedule: schedule_event_details(schedule),
                                     schedules)
            event_details = list(chain.from_iterable(event_details))
        print(f'Got details of {len(event_details)} events in {len(schedules)} schedules.')


@dataclass(init=False)
class TestWithTestSchedules(TestWithLocations):
    """
    Base class for tests with test schedules (test_xxx)
    """
    test_schedules: ClassVar[list[Schedule]]

    @classmethod
    def setUpClass(cls) -> None:
        """
        get all test_xxx schedules in all locations
        :return:
        """
        super().setUpClass()
        if not cls.locations:
            cls.test_schedules = None
            return

        with ThreadPoolExecutor() as pool:
            tasks = pool.map(lambda loc: list(cls.api.telephony.schedules.list(obj_id=loc.location_id,
                                                                               name='test_')),
                             cls.locations)
            cls.test_schedules = list(chain.from_iterable(tasks))
        cls.test_schedules: list[Schedule]
        cls.test_schedules = [schedule
                              for schedule in cls.test_schedules
                              if re.match(r'test_\d{3}', schedule.name)]


class TestCreate(TestWithTestSchedules):
    """
    Test cases for schedule creation
    """

    def test_001_create_business(self):
        """
        create a business schedule in a random location
        """
        # select a random location
        target_location = random.choice(self.locations)
        print(f'Target location: "{target_location.name}"')

        schedules = list(self.api.telephony.schedules.list(obj_id=target_location.location_id))
        schedule_names = set(sched.name for sched in schedules)
        schedule_name = next((name for i in range(1000)
                              if (name := f'test_{i:03d}') not in schedule_names))
        schedule = Schedule.business(name=schedule_name)
        schedule_id = self.api.telephony.schedules.create(obj_id=target_location.location_id, schedule=schedule)
        details = self.api.telephony.schedules.details(obj_id=target_location.location_id,
                                                       schedule_type=schedule.schedule_type,
                                                       schedule_id=schedule_id)
        print(f'created schedule: {target_location.name}/{schedule_name}/{schedule_id}')
        self.assertEqual(len(schedule.events), len(details.events))
        self.assertEqual(schedule.name, details.name)

    def test_002_create_event(self):
        """
        create an event
        """
        if not self.test_schedules:
            self.skipTest('Need at least one test schedule (test_xxx)')

        target_schedule = random.choice(self.test_schedules)
        details = self.api.telephony.schedules.details(obj_id=target_schedule.location_id,
                                                       schedule_type=target_schedule.schedule_type,
                                                       schedule_id=target_schedule.schedule_id)
        # add an event
        event_names = set(event.name for event in details.events)
        event_name = next(name for i in range(1000)
                          if (name := f'today_{i:03d}') not in event_names)
        event = Event(name=event_name,
                      all_day_enabled=True,
                      start_date=datetime.date.today(),
                      end_date=datetime.date.today(),
                      recurrence=Recurrence(recur_for_ever=True,
                                            recur_yearly_by_date=RecurYearlyByDate.from_date(datetime.date.today())))
        event_id = self.api.telephony.schedules.event_create(obj_id=target_schedule.location_id,
                                                             schedule_type=target_schedule.schedule_type,
                                                             schedule_id=target_schedule.schedule_id,
                                                             event=event)
        details_after = self.api.telephony.schedules.details(obj_id=target_schedule.location_id,
                                                             schedule_type=target_schedule.schedule_type,
                                                             schedule_id=target_schedule.schedule_id)
        self.assertEqual(len(details.events) + 1, len(details_after.events))
        self.assertEqual(event_name, details_after.events[-1].name)
        self.assertEqual(event_id, details_after.events[-1].event_id)


class TestUpdateSchedule(TestWithTestSchedules):
    """
    Test cases for updating schedules
    """

    def setUp(self) -> None:
        super().setUp()
        if not self.test_schedules:
            self.skipTest('Need at least one test schedule (test_xxx)')

    def test_001_update_schedule_name(self):
        """
        test to update a schedule name
        """
        target_schedule = random.choice(self.test_schedules)
        details = self.api.telephony.schedules.details(obj_id=target_schedule.location_id,
                                                       schedule_type=target_schedule.schedule_type,
                                                       schedule_id=target_schedule.schedule_id)
        schedule_names = set(schedule.name
                             for schedule in self.test_schedules
                             if schedule.location_id == target_schedule.location_id)
        old_name = target_schedule.name
        new_name = next(name for i in range(1000)
                        if (name := f'test_{i:03d}') not in schedule_names)
        details.name = new_name

        new_id = self.api.telephony.schedules.update(schedule=details,
                                                     obj_id=target_schedule.location_id,
                                                     schedule_type=target_schedule.schedule_type,
                                                     schedule_id=target_schedule.schedule_id)
        after = self.api.telephony.schedules.details(obj_id=target_schedule.location_id,
                                                     schedule_type=target_schedule.schedule_type,
                                                     schedule_id=new_id)
        # restore old name
        details.name = old_name
        self.api.telephony.schedules.update(schedule=details,
                                            obj_id=target_schedule.location_id,
                                            schedule_type=target_schedule.schedule_type,
                                            schedule_id=new_id)

        self.assertEqual(new_name, after.name)
        self.assertEqual(details.events, after.events)

    def test_002_update_event_names(self):
        """
        test to update event names
        """
        target_schedule = random.choice(self.test_schedules)
        # get details; we need the eventy
        details = self.api.telephony.schedules.details(obj_id=target_schedule.location_id,
                                                       schedule_type=target_schedule.schedule_type,
                                                       schedule_id=target_schedule.schedule_id)

        # change all event names: add a leading 'U'
        update = details.model_copy(deep=True)
        for event in update.events:
            event.new_name = f'U{event.name}'
        new_id = self.api.telephony.schedules.update(schedule=update,
                                                     obj_id=target_schedule.location_id,
                                                     schedule_type=target_schedule.schedule_type,
                                                     schedule_id=target_schedule.schedule_id)
        after = self.api.telephony.schedules.details(obj_id=target_schedule.location_id,
                                                     schedule_type=target_schedule.schedule_type,
                                                     schedule_id=new_id)

        # restore old settings
        restore = update.model_copy(deep=True)
        # update names back to original: swap new name and name for each event
        for event in restore.events:
            event.name, event.new_name = event.new_name, event.name
        self.api.telephony.schedules.update(schedule=restore,
                                            obj_id=target_schedule.location_id,
                                            schedule_type=target_schedule.schedule_type,
                                            schedule_id=new_id)
        # number of events should not have changed
        self.assertEqual(len(details.events), len(after.events))

        # schedule should not have changed with the exception of events
        self.assertEqual(details.model_dump_json(exclude={'events'}), after.model_dump_json(exclude={'events'}))

        # for each event
        #   * name should have changed
        #   * everything else should be unchanged
        for event, after_event in zip(details.events, after.events):
            self.assertEqual(f'U{event.name}', after_event.name)
            # all event settings with the exception of event_id and name should be identical
            event_json = event.model_dump_json(exclude={'event_id', 'name'})
            after_event_json = after_event.model_dump_json(exclude={'event_id', 'name'})
            self.assertEqual(event_json, after_event_json)


class TestAllDetails(TestWithLocations):
    """
    list all schedules of all locations
    """

    @async_test
    async def test_all_details(self):
        sapi = self.async_api.telephony.schedules
        schedule_lists = await asyncio.gather(*[sapi.list(obj_id=loc.location_id)
                                                for loc in self.locations])
        schedule_lists: list[list[Schedule]]
        # get details for all schedules
        sched_list: list[Schedule]
        schedule_lists = await asyncio.gather(*[asyncio.gather(*[sapi.details(loc.location_id,
                                                                              schedule_type=sched.schedule_type,
                                                                              schedule_id=sched.schedule_id)
                                                                 for sched in sched_list])
                                                for loc, sched_list in zip(self.locations, schedule_lists)])
        for location, schedule_list in zip(self.locations, schedule_lists):
            print(f'{location.name}: {len(schedule_list)} schedules')
            print(' ', end='')
            print(', '.join(f'{sched.name}' for sched in schedule_list))
            for schedule in schedule_list:
                print(f'  {schedule.name}: {len(schedule.events)} events')
                for event in schedule.events:
                    data = event.model_dump(exclude={'event_id', 'new_name'}, mode='json', by_alias=True)
                    print(f'    {data}')

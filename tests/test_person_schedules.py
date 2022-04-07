"""
Unit test for person schedules
"""
# TODO: testcase for event update
# TODO test case for event delete
# TODO test case for schedule delete
import base64
import datetime
import random
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from itertools import chain

from wxc_sdk.rest import RestError
from wxc_sdk.types import *
from .base import TestCaseWithUsers

# prefix for test schedule names
SCHEDULE_NAME_PREFIX = 'test_'


def unique_schedules(schedules: Iterable[Schedule]) -> list[Schedule]:
    """
    list of unique schedules

    :meta private:
    """
    unique_schedules = {(schedule.schedule_id, schedule.schedule_type): schedule for schedule in schedules}
    return list(unique_schedules.values())


def debug_schedule_id(schedule_id: str) -> str:
    """
    debug output for schedule id

    :meta private:
    """
    decoded = base64.b64decode(f"{schedule_id}==").decode()
    decoded_id = base64.b64decode(f'{decoded.split("/")[-1]}').decode()

    return f'{schedule_id}, {decoded}, {decoded_id}'


class TestScheduleList(TestCaseWithUsers):
    """
    Test cases for schedules
    """

    def test_001_list(self):
        """
        Try to list all existing schedules for all users
        """
        with ThreadPoolExecutor() as pool:
            schedules = list(pool.map(lambda user: list(self.api.person_settings.schedules.list(obj_id=user.person_id)),
                                      self.users))
        all_schedules = list(chain.from_iterable(schedules))
        schedule_ids = set((schedule.name, schedule.schedule_id, schedule.schedule_type) for schedule in all_schedules)
        print(f'got {len(all_schedules)} schedules ({len(schedule_ids)} unique) for {len(self.users)}')

        if schedule_ids:
            name_len = max(map(len, (s[0] for s in schedule_ids)))
            type_len = max(map(len, (s[2].name for s in schedule_ids)))
            decoded_ids = map(lambda s: f'{s[0]:{name_len}}({s[2].name:{type_len}}): {debug_schedule_id(s[1])}',
                              schedule_ids)
            print('\n'.join(decoded_ids))


class TestCreateOrUpdate(TestCaseWithUsers):
    """
    Test cases for schedule creation or updates
    * is it possible to create a user schedule with the name of an existing location schedule
        * if yes, which one shows up in a user level list
    * update a user schedule, daes it change the locatuon schedule?
    """

    def test_001_create(self):
        """
        create a user schedule, does it show up at location level
        """
        ps = self.api.person_settings.schedules
        ls = self.api.telephony.schedules

        # pick random user
        target_user = random.choice(self.users)
        print(f'target user: {target_user.display_name}')

        # list user and location schedules
        user_schedules = list(ps.list(obj_id=target_user.person_id))
        location_schedules = list(ls.list(obj_id=target_user.location_id))
        print(f'    user schedules: {", ".join(f"{s.name}({s.schedule_type.name})" for s in user_schedules)}')
        print(f'location schedules: {", ".join(f"{s.name}({s.schedule_type.name})" for s in location_schedules)}')

        # get available name (not present at location nor user level)
        names = set(chain((s.name for s in user_schedules),
                          (s.name for s in location_schedules)))
        new_names = (name for i in range(1000)
                     if (name := f'{SCHEDULE_NAME_PREFIX}user_{i:03}') not in names)
        new_name = next(new_names)
        print(f'new schedule name: {new_name}')

        # create user schedule: holidays
        new_schedule = Schedule(name=new_name, schedule_type=ScheduleType.holidays)
        new_schedule_id = ps.create(obj_id=target_user.person_id,
                                    schedule=new_schedule)

        # get details and verify
        details = ps.details(obj_id=target_user.person_id,
                             schedule_type=new_schedule.schedule_type,
                             schedule_id=new_schedule_id)
        self.assertEqual(new_name, details.name)
        self.assertEqual(details.schedule_type, new_schedule.schedule_type)
        self.assertTrue(not details.events)

        # list user and location schedules. Where does it show up?
        user_schedules_after = list(ps.list(obj_id=target_user.person_id))
        location_schedules_after = list(ls.list(obj_id=target_user.location_id))
        print(f'    user schedules (after): '
              f'{", ".join(f"{s.name}({s.schedule_type.name})" for s in user_schedules_after)}')
        print(f'location schedules (after): '
              f'{", ".join(f"{s.name}({s.schedule_type.name})" for s in location_schedules_after)}')

        # the new schedule shoult not change the location schedule list
        self.assertEqual(location_schedules, location_schedules_after)

        # new schedule has to be in user schedule list
        in_list = next((schedule for schedule in user_schedules_after
                        if new_schedule_id == new_schedule_id), None)
        self.assertTrue(in_list is not None)

    def test_002_create_name_conflict(self):
        """
        it is not possible to create a user schedule with the name and type of an existing location schedule
        """
        ps = self.api.person_settings.schedules
        ls = self.api.telephony.schedules

        # pick random user
        target_user = random.choice(self.users)
        print(f'target user: {target_user.display_name}')

        # list user and location schedules
        user_schedules = list(ps.list(obj_id=target_user.person_id))
        location_schedules = list(ls.list(obj_id=target_user.location_id))
        print(f'    user schedules: {", ".join(f"{s.name}({s.schedule_type.name})" for s in user_schedules)}')
        print(f'location schedules: {", ".join(f"{s.name}({s.schedule_type.name})" for s in location_schedules)}')

        # determine target location schedule
        user_schedule_names = set(s.name for s in user_schedules)
        location_schedule_names = set(s.name for s in location_schedules)

        target_schedule_name = next((name for i in range(1000)
                                     if (name := f'{SCHEDULE_NAME_PREFIX}{i:03}') not in user_schedule_names))

        # create a new location schedule if no location schedule with the target name exists
        if target_schedule_name in location_schedule_names:
            target_location_schedule = next(s for s in location_schedules
                                            if s.name == target_schedule_name)
            print(f'Existing location schedule: {target_location_schedule.name}')
        else:
            # we need to create a location schedule
            new_location_schedule = Schedule(
                name=target_schedule_name,
                schedule_type=ScheduleType.holidays)
            target_location_schedule_id = ls.create(
                obj_id=target_user.location_id,
                schedule=new_location_schedule)
            target_location_schedule = ls.details(obj_id=target_user.location_id,
                                                  schedule_type=new_location_schedule.schedule_type,
                                                  schedule_id=target_location_schedule_id)
            print(f'New location schedule: {target_location_schedule.name}')

        # create a user schedule with the same name and type as the location schedule
        # this should fail with a RestError, duplicate name
        with self.assertRaises(RestError) as exc:
            new_schedule = Schedule(
                name=target_location_schedule.name,
                schedule_type=target_location_schedule.schedule_type)
            ps.create(obj_id=target_user.person_id, schedule=new_schedule)
        self.assertEqual(25030, exc.exception.code)

    def test_003_location_schedule_shows_in_user_schedule_list(self):
        """
        location schedules show in user schedules
        """
        ps = self.api.person_settings.schedules
        ls = self.api.telephony.schedules

        # pick random user
        target_user = random.choice(self.users)
        print(f'target user: {target_user.display_name}')

        # location schedules
        user_schedules = {(s.schedule_type, s.name): s for s in ps.list(obj_id=target_user.person_id)}
        location_schedules = {(s.schedule_type, s.name): s for s in ls.list(obj_id=target_user.location_id)}
        print(f'    user schedules:'
              f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in user_schedules)}')
        print(f'location schedules:'
              f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in location_schedules)}')

        # available names for new schedules
        schedule_names = set(chain((s.name for s in user_schedules.values()),
                                   (s.name for s in location_schedules.values())))
        new_names = (name for i in range(1000)
                     if (name := f'{SCHEDULE_NAME_PREFIX}{i:03}') not in schedule_names)

        # we need at least one location schedule to prove our point
        if not location_schedules:
            # new location schedule
            location_schedule_name = next(new_names)
            ls.create(obj_id=target_user.location_id,
                      schedule=Schedule(name=location_schedule_name, schedule_type=ScheduleType.holidays))
            print(f'new location holiday schedule: {location_schedule_name}')

        # validate user and location schedule list
        user_schedules_after = {(s.schedule_type, s.name): s for s in ps.list(obj_id=target_user.person_id,
                                                                              schedule_type=ScheduleType.holidays)}
        location_schedules_after = {(s.schedule_type, s.name): s for s in ls.list(obj_id=target_user.location_id,
                                                                                  schedule_type=ScheduleType.holidays)}
        self.assertTrue(all(key in user_schedules_after for key in location_schedules_after),
                        'Not all location schedules show up in user schedules')

    def test_004_user_schedules_dont_show_in_location_schedules(self):
        """
        user schedules don't show up in location schedules
        """
        ps = self.api.person_settings.schedules
        ls = self.api.telephony.schedules

        # pick random user
        target_user = random.choice(self.users)
        print(f'target user: {target_user.display_name}')

        # list user and location schedules
        user_schedules = {(s.schedule_type, s.name): s for s in ps.list(obj_id=target_user.person_id,
                                                                        schedule_type=ScheduleType.holidays)}
        location_schedules = {(s.schedule_type, s.name): s for s in ls.list(obj_id=target_user.location_id,
                                                                            schedule_type=ScheduleType.holidays)}
        print(f'    user schedules:'
              f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in user_schedules)}')
        print(f'location schedules:'
              f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in location_schedules)}')

        # available names for new schedules
        schedule_names = set(chain((s.name for s in user_schedules.values()),
                                   (s.name for s in location_schedules.values())))
        new_names = (name for i in range(1000)
                     if (name := f'{SCHEDULE_NAME_PREFIX}{i:03}') not in schedule_names)

        # we create a new user schedule
        # new user schedule
        user_schedule_name = next(new_names)
        ps.create(obj_id=target_user.person_id,
                  schedule=Schedule(name=user_schedule_name, schedule_type=ScheduleType.holidays))
        print(f'new user holiday schedule: {user_schedule_name}')

        # validate user and location schedule list
        user_schedules_after = {(s.schedule_type, s.name): s for s in ps.list(obj_id=target_user.person_id,
                                                                              schedule_type=ScheduleType.holidays)}
        location_schedules_after = {(s.schedule_type, s.name): s for s in ls.list(obj_id=target_user.location_id,
                                                                                  schedule_type=ScheduleType.holidays)}
        print(f'    user schedules after:'
              f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in user_schedules_after)}')
        print(f'location schedules after:'
              f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in location_schedules_after)}')

        # new user schedule is in user list
        key = (ScheduleType.holidays, user_schedule_name)
        self.assertTrue(key in user_schedules_after)
        # .. but not in location schedule list
        self.assertTrue(key not in location_schedules_after)

    def test_005_get_user_schedule_details(self):
        """
        try to get details for all user schedules returned by list
        * getting user schedule details for schedules that are actually location schedules fails
        """
        ps = self.api.person_settings.schedules
        ls = self.api.telephony.schedules

        # pick random user
        target_user = random.choice(self.users)
        print(f'target user: {target_user.display_name}')

        # list user and location schedules
        user_schedules = {(s.schedule_type, s.name): s for s in ps.list(obj_id=target_user.person_id,
                                                                        schedule_type=ScheduleType.holidays)}
        location_schedules = {(s.schedule_type, s.name): s for s in ls.list(obj_id=target_user.location_id,
                                                                            schedule_type=ScheduleType.holidays)}
        print(f'    user schedules:'
              f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in user_schedules)}')
        print(f'location schedules:'
              f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in location_schedules)}')

        # available names for new schedules
        schedule_names = set(chain((s.name for s in user_schedules.values()),
                                   (s.name for s in location_schedules.values())))
        new_names = (name for i in range(1000)
                     if (name := f'{SCHEDULE_NAME_PREFIX}{i:03}') not in schedule_names)

        # we need at least one location schedule to prove our point
        if not location_schedules:
            # new location schedule
            location_schedule_name = next(new_names)
            ls.create(obj_id=target_user.location_id,
                      schedule=Schedule(name=location_schedule_name, schedule_type=ScheduleType.holidays))
            print(f'new location holiday schedule: {location_schedule_name}')

        # we also at least need one real(!) user schedule to prove our point
        if next((key for key in user_schedules
                 if key not in location_schedules), None) is None:
            # new user schedule
            user_schedule_name = next(new_names)
            ps.create(obj_id=target_user.person_id,
                      schedule=Schedule(name=user_schedule_name, schedule_type=ScheduleType.holidays))
            print(f'new user holiday schedule: {user_schedule_name}')

        # validate user and location schedule list
        user_schedules_after = {(s.schedule_type, s.name): s for s in ps.list(obj_id=target_user.person_id,
                                                                              schedule_type=ScheduleType.holidays)}
        location_schedules_after = {(s.schedule_type, s.name): s for s in ls.list(obj_id=target_user.location_id,
                                                                                  schedule_type=ScheduleType.holidays)}
        print(f'    user schedules after:'
              f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in user_schedules_after)}')
        print(f'location schedules after:'
              f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in location_schedules_after)}')

        # hypothesis: we can only get user schedule details for schedules in the user list which are not actually
        # location schedules.
        name_len = max(map(len, (s.name for s in user_schedules_after.values())))
        for schedule in user_schedules_after.values():
            schedule: Schedule
            print(f'Getting user schedule details for {schedule.name}({schedule.schedule_type.name})')
            if (schedule.schedule_type, schedule.name) in location_schedules_after:
                # this is actually a location schedule and we expect the user details call to fail
                with self.assertRaises(RestError):
                    ps.details(obj_id=target_user.person_id, schedule_type=schedule.schedule_type,
                               schedule_id=schedule.schedule_id)
                print(f'Getting user schedule details for {schedule.name:{name_len}} '
                      f'   failed as expected (is a location schedule)')
            else:
                # for schedules which aren't actually location schedules the details call should work
                ps.details(obj_id=target_user.person_id, schedule_type=schedule.schedule_type,
                           schedule_id=schedule.schedule_id)
                print(f'Getting user schedule details for {schedule.name:{name_len}} '
                      f'succeeded as expected (is a person schedule)')

    def test_006_update_name(self):
        """
        try to change the name of a person schedule
        """
        ps = self.api.person_settings.schedules
        ls = self.api.telephony.schedules

        # pick random user
        target_user = random.choice(self.users)
        print(f'target user: {target_user.display_name}')

        # list user and location schedules
        user_schedules = {(s.schedule_type, s.name): s for s in ps.list(obj_id=target_user.person_id,
                                                                        schedule_type=ScheduleType.holidays)}
        location_schedules = {(s.schedule_type, s.name): s for s in ls.list(obj_id=target_user.location_id,
                                                                            schedule_type=ScheduleType.holidays)}
        print(f'    user schedules:'
              f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in user_schedules)}')
        print(f'location schedules:'
              f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in location_schedules)}')

        # available names for new schedules
        schedule_names = set(chain((s.name for s in user_schedules.values()),
                                   (s.name for s in location_schedules.values())))
        new_names = (name for i in range(1000)
                     if (name := f'{SCHEDULE_NAME_PREFIX}{i:03}') not in schedule_names)

        # we also at least need one real(!) user schedule for the test
        if (target_schedule_id := next((schedule.schedule_id
                                        for key, schedule in user_schedules.items()
                                        if key not in location_schedules), None)) is None:
            # new user schedule
            user_schedule_name = next(new_names)
            target_schedule_id = ps.create(obj_id=target_user.person_id,
                                           schedule=Schedule(name=user_schedule_name,
                                                             schedule_type=ScheduleType.holidays))
            print(f'new user holiday schedule: {user_schedule_name}')
        # get details with events
        target_schedule = ps.details(obj_id=target_user.person_id,
                                     schedule_type=ScheduleType.holidays,
                                     schedule_id=target_schedule_id)

        # we want to test with a schedule that has at least one event
        # .. so that we can verify that an update w/o events leaves the existing events unchanged
        if not target_schedule.events:
            new_start_date = datetime.date.today()
            new_event = Event(name=f'{new_start_date.month:02}{new_start_date.day:02}',
                              start_date=new_start_date,
                              end_date=new_start_date,
                              all_day_enabled=True)
            print(f'adding new event to schedule: {new_event.name}')
            ps.event_create(obj_id=target_user.person_id,
                            schedule_type=target_schedule.schedule_type,
                            schedule_id=target_schedule.schedule_id,
                            event=new_event)
            target_schedule = ps.details(obj_id=target_user.person_id,
                                         schedule_type=target_schedule.schedule_type,
                                         schedule_id=target_schedule.schedule_id)
            # verify that the event actually got added
            self.assertEqual(1, len(target_schedule.events))
        print(f'target schedule: {target_schedule.name}({target_schedule.schedule_type.name})')

        new_name = next(new_names)
        print(f'Changing name to {new_name}')
        settings = Schedule(name=new_name,
                            schedule_type=target_schedule.schedule_type)
        updated_id = ps.update(obj_id=target_user.person_id,
                               schedule=settings)

        print(f'updated id: {debug_schedule_id(updated_id)}')

        # get details after update
        updated_schedule = ps.details(obj_id=target_user.person_id,
                                      schedule_type=target_schedule.schedule_type,
                                      schedule_id=updated_id)

        # name should be the new name
        self.assertEqual(new_name, updated_schedule.name)

        # everything other than name and id should be the same
        updated_schedule.name = target_schedule.name
        updated_schedule.schedule_id = target_schedule.schedule_id
        self.assertEqual(target_schedule, updated_schedule)

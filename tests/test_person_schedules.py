"""
Unit test for person schedules
"""

import asyncio
import base64
import datetime
import re
from collections import defaultdict
from collections.abc import Iterable
from contextlib import suppress
from functools import reduce
from itertools import chain
from typing import NamedTuple

from tests.base import TestCaseWithUsers, TestWithLocations, TestWithTempCallingUser, async_test
from wxc_sdk.all_types import *
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.rest import RestError

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
    Example:
        * Y2lzY29zcGFyazovL3VzL1VTRVJfU0NIRURVTEUvVG1GMGFXOXVZV3dnU0c5c2FXUmhlWE09 is base64 decoded to ..
        * ciscospark://us/USER_SCHEDULE/TmF0aW9uYWwgSG9saWRheXM= where the last part TmF0aW9uYWwgSG9saWRheXM= is
          decoded to ..
        * National Holidays .. which apparently is the name of the schedule

    :meta private:
    """
    decoded = base64.b64decode(f'{schedule_id}==').decode()
    # try to decode the last
    decoded_id = base64.b64decode(f'{decoded.split("/")[-1]}').decode()

    return f'{schedule_id}, {decoded}, {decoded_id}'


async def all_user_schedules(api: AsWebexSimpleApi, users: list[Person]) -> list[list[Schedule]]:
    """
    Get schedules for all users
    """
    schedules = await asyncio.gather(*[api.person_settings.schedules.list(obj_id=user.person_id) for user in users])
    return schedules


class TestScheduleList(TestCaseWithUsers):
    """
    Test cases for schedules
    """

    @async_test
    async def test_001_list(self):
        """
        Try to list all existing schedules for all users
        Listing schedules at the user level contains location level schedules
        """

        # Read schedules for every user and flatten the async result set.
        all_schedules: list[Schedule] = list(chain.from_iterable(await all_user_schedules(self.async_api, self.users)))

        # Normalize schedule metadata so duplicates across users can be summarized.
        class ScheduleInfo(NamedTuple):
            name: str
            id: str
            type: str
            level: str

        # Group schedules by level and build a unique identity set for diagnostics.
        schedules_by_level: dict[str, list[Schedule]] = reduce(
            lambda r, el: r[el.level].append(el) or r, all_schedules, defaultdict(list)
        )
        schedule_ids = set(
            ScheduleInfo(name=schedule.name, id=schedule.schedule_id, type=schedule.schedule_type, level=schedule.level)
            for schedule in all_schedules
        )
        print(f'got {len(all_schedules)} schedules ({len(schedule_ids)} unique) for {len(self.users)} users')
        for level, schedules_for_level in schedules_by_level.items():
            print(f'got {len(schedules_for_level)} schedules at level "{level}"')

        # Print decoded schedule ids to make live org fixture state easier to inspect.
        if schedule_ids:
            name_len = max(len(s.name) for s in schedule_ids)
            type_len = max(len(s.type) for s in schedule_ids)
            decoded_ids = map(
                lambda s: f'{s.name:{name_len}}({s.type:{type_len}})({s.level:5}): {debug_schedule_id(s.id)}',
                schedule_ids,
            )
            print('\n'.join(sorted(decoded_ids)))


# noinspection DuplicatedCode
class TestCreateOrUpdate(TestWithTempCallingUser):
    """
    Test cases for schedule creation or updates
    * is it possible to create a user schedule with the name of an existing location schedule
        * if yes, which one shows up in a user level list
    * update a user schedule, daes it change the locatuon schedule?
    """

    def target_user(self) -> Person:
        target_user = self.user
        print(f'target user: {target_user.display_name}')
        return target_user  # type: ignore[return-value]

    def delete_schedule(self, api, obj_id: str, schedule_type: ScheduleType, schedule_id: str):
        if schedule_id and schedule_type:
            with suppress(RestError):
                api.delete_schedule(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id)

    def available_name(self, target_user: Person, suffix: str) -> str:
        ps = self.api.person_settings.schedules
        ls = self.api.telephony.schedules
        existing = set(
            chain(
                (s.name for s in ps.list(obj_id=target_user.person_id)),
                (s.name for s in ls.list(obj_id=target_user.location_id)),
            )
        )
        return next(name for i in range(1000) if (name := f'{SCHEDULE_NAME_PREFIX}{suffix}_{i:03}') not in existing)

    def test_001_create(self):
        """
        create a user schedule, does it show up at location level?
        """
        ps = self.api.person_settings.schedules
        ls = self.api.telephony.schedules

        # Use the disposable calling user as the person-level schedule owner.
        target_user = self.target_user()

        # Snapshot user and location schedules before creating the person schedule.
        user_schedules = list(ps.list(obj_id=target_user.person_id))
        location_schedules = list(ls.list(obj_id=target_user.location_id))
        print(f'    user schedules: {", ".join(f"{s.name}({s.schedule_type})" for s in user_schedules)}')
        print(f'location schedules: {", ".join(f"{s.name}({s.schedule_type})" for s in location_schedules)}')

        # Pick a schedule name that is absent at both person and location level.
        names = set(chain((s.name for s in user_schedules), (s.name for s in location_schedules)))
        new_names = (name for i in range(1000) if (name := f'{SCHEDULE_NAME_PREFIX}user_{i:03}') not in names)
        new_name = next(new_names)
        print(f'new schedule name: {new_name}')

        # Create a person-level holiday schedule and track the id for cleanup.
        new_schedule = Schedule(name=new_name, type=ScheduleType.holidays)
        new_schedule_id = None
        try:
            new_schedule_id = ps.create(obj_id=target_user.person_id, schedule=new_schedule)

            # Read schedule details and verify the created schedule fields.
            details = ps.details(
                obj_id=target_user.person_id, schedule_type=new_schedule.schedule_type, schedule_id=new_schedule_id
            )
            self.assertEqual(new_name, details.name)
            self.assertEqual(details.schedule_type, new_schedule.schedule_type)
            self.assertTrue(not details.events)

            # Compare post-create person and location lists.
            user_schedules_after = list(ps.list(obj_id=target_user.person_id))
            location_schedules_after = list(ls.list(obj_id=target_user.location_id))
            print(
                f'    user schedules (after): {", ".join(f"{s.name}({s.schedule_type})" for s in user_schedules_after)}'
            )
            print(
                f'location schedules (after): '
                f'{", ".join(f"{s.name}({s.schedule_type})" for s in location_schedules_after)}'
            )

            # The person schedule must not mutate the location schedule list.
            self.assertEqual(location_schedules, location_schedules_after)

            # The person schedule must show in the person schedule list at PEOPLE level.
            in_list = next(
                (schedule for schedule in user_schedules_after if schedule.schedule_id == new_schedule_id), None
            )
            self.assertTrue(in_list is not None)
            self.assertEqual(ScheduleLevel.people, in_list.level, 'New schedule should be a user schedule')
        finally:
            # Always delete the created person schedule.
            self.delete_schedule(
                api=ps,
                obj_id=target_user.person_id,
                schedule_type=new_schedule.schedule_type,
                schedule_id=new_schedule_id,
            )

    def test_002_create_name_conflict(self):
        """
        it is not possible to create a user schedule with the name and type of an existing location schedule
        """
        ps = self.api.person_settings.schedules
        ls = self.api.telephony.schedules

        # Use the disposable calling user as the conflict target.
        target_user = self.target_user()

        # Snapshot current person and location schedules.
        user_schedules = list(ps.list(obj_id=target_user.person_id))
        location_schedules = list(ls.list(obj_id=target_user.location_id))
        print(f'    user schedules: {", ".join(f"{s.name}({s.schedule_type})" for s in user_schedules)}')
        print(f'location schedules: {", ".join(f"{s.name}({s.schedule_type})" for s in location_schedules)}')

        # Determine a target name that does not already exist as a person schedule.
        user_schedule_names = set(s.name for s in user_schedules)
        location_schedule_names = set(s.name for s in location_schedules)

        target_schedule_name = next(
            name for i in range(1000) if (name := f'{SCHEDULE_NAME_PREFIX}{i:03}') not in user_schedule_names
        )

        target_location_schedule_id = None

        # Create a location schedule if the conflict fixture does not already exist.
        if target_schedule_name in location_schedule_names:
            target_location_schedule = next(s for s in location_schedules if s.name == target_schedule_name)
            print(f'Existing location schedule: {target_location_schedule.name}')
        else:
            new_location_schedule = Schedule(name=target_schedule_name, type=ScheduleType.holidays)
            target_location_schedule_id = ls.create(obj_id=target_user.location_id, schedule=new_location_schedule)
            target_location_schedule = ls.details(
                obj_id=target_user.location_id,
                schedule_type=new_location_schedule.schedule_type,
                schedule_id=target_location_schedule_id,
            )
            print(f'New location schedule: {target_location_schedule.name}')

        try:
            # Attempt to create a person schedule with duplicate name/type and expect duplicate-name failure.
            with self.assertRaises(RestError) as exc:
                new_schedule = Schedule(name=target_location_schedule.name, type=target_location_schedule.schedule_type)
                ps.create(obj_id=target_user.person_id, schedule=new_schedule)
            self.assertEqual(25030, exc.exception.code)
        finally:
            # Delete the location schedule if this test created it.
            self.delete_schedule(
                api=ls,
                obj_id=target_user.location_id,
                schedule_type=target_location_schedule.schedule_type,
                schedule_id=target_location_schedule_id,
            )

    def test_003_location_schedule_shows_in_user_schedule_list(self):
        """
        location schedules show in user schedules
        """
        ps = self.api.person_settings.schedules
        ls = self.api.telephony.schedules

        # Use the disposable calling user to compare person and location schedule views.
        target_user = self.target_user()

        # Snapshot current person and location schedules keyed by type/name.
        user_schedules = {(s.schedule_type, s.name): s for s in ps.list(obj_id=target_user.person_id)}
        location_schedules = {(s.schedule_type, s.name): s for s in ls.list(obj_id=target_user.location_id)}
        print(f'    user schedules: {", ".join(f"{s_name}({s_type})" for s_type, s_name in user_schedules)}')
        print(f'location schedules: {", ".join(f"{s_name}({s_type})" for s_type, s_name in location_schedules)}')

        # Prepare unused names in case the location has no holiday schedules.
        schedule_names = set(
            chain((s.name for s in user_schedules.values()), (s.name for s in location_schedules.values()))
        )
        new_names = (name for i in range(1000) if (name := f'{SCHEDULE_NAME_PREFIX}{i:03}') not in schedule_names)

        created_location_schedule_id = None
        created_location_schedule_type = None
        try:
            # Ensure at least one location schedule exists for the list-inheritance assertion.
            if not location_schedules:
                location_schedule_name = next(new_names)
                created_location_schedule = Schedule(name=location_schedule_name, type=ScheduleType.holidays)
                created_location_schedule_id = ls.create(
                    obj_id=target_user.location_id,
                    schedule=created_location_schedule,
                )
                created_location_schedule_type = created_location_schedule.schedule_type
                print(f'new location holiday schedule: {location_schedule_name}')

            # Read both lists and assert every location holiday schedule appears in the person list.
            user_schedules_after = {
                (s.schedule_type, s.name): s
                for s in ps.list(obj_id=target_user.person_id, schedule_type=ScheduleType.holidays)
            }
            location_schedules_after = {
                (s.schedule_type, s.name): s
                for s in ls.list(obj_id=target_user.location_id, schedule_type=ScheduleType.holidays)
            }
            self.assertTrue(
                all(key in user_schedules_after for key in location_schedules_after),
                'Not all location schedules show up in user schedules',
            )
        finally:
            # Delete the temporary location schedule if this test created one.
            self.delete_schedule(
                api=ls,
                obj_id=target_user.location_id,
                schedule_type=created_location_schedule_type,
                schedule_id=created_location_schedule_id,
            )

    def test_004_user_schedules_dont_show_in_location_schedules(self):
        """
        user schedules don't show up in location schedules
        """
        ps = self.api.person_settings.schedules
        ls = self.api.telephony.schedules

        # Use the disposable calling user to compare person and location schedule views.
        target_user = self.target_user()

        # Snapshot current person and location holiday schedules.
        user_schedules = {
            (s.schedule_type, s.name): s
            for s in ps.list(obj_id=target_user.person_id, schedule_type=ScheduleType.holidays)
        }
        location_schedules = {
            (s.schedule_type, s.name): s
            for s in ls.list(obj_id=target_user.location_id, schedule_type=ScheduleType.holidays)
        }
        print(f'    user schedules: {", ".join(f"{s_name}({s_type})" for s_type, s_name in user_schedules)}')
        print(f'location schedules: {", ".join(f"{s_name}({s_type})" for s_type, s_name in location_schedules)}')

        # Pick a name that does not collide with person or location schedules.
        schedule_names = set(
            chain((s.name for s in user_schedules.values()), (s.name for s in location_schedules.values()))
        )
        new_names = (name for i in range(1000) if (name := f'{SCHEDULE_NAME_PREFIX}{i:03}') not in schedule_names)

        user_schedule_name = next(new_names)
        user_schedule = Schedule(name=user_schedule_name, type=ScheduleType.holidays)
        user_schedule_id = None
        try:
            # Create the person schedule and verify it is isolated from the location list.
            user_schedule_id = ps.create(obj_id=target_user.person_id, schedule=user_schedule)
            print(f'new user holiday schedule: {user_schedule_name}')

            # Read person and location schedules after creation.
            user_schedules_after = {
                (s.schedule_type, s.name): s
                for s in ps.list(obj_id=target_user.person_id, schedule_type=ScheduleType.holidays)
            }
            location_schedules_after = {
                (s.schedule_type, s.name): s
                for s in ls.list(obj_id=target_user.location_id, schedule_type=ScheduleType.holidays)
            }
            print(
                f'    user schedules after: '
                f'{", ".join(f"{s_name}({s_type})" for s_type, s_name in user_schedules_after)}'
            )
            print(
                f'location schedules after:'
                f' {", ".join(f"{s_name}({s_type})" for s_type, s_name in location_schedules_after)}'
            )

            # The new person schedule is visible to the person but not to the location.
            key = (ScheduleType.holidays, user_schedule_name)
            self.assertIn(key, user_schedules_after)
            self.assertNotIn(key, location_schedules_after)
        finally:
            # Always delete the created person schedule.
            self.delete_schedule(
                api=ps,
                obj_id=target_user.person_id,
                schedule_type=user_schedule.schedule_type,
                schedule_id=user_schedule_id,
            )

    def test_005_get_user_schedule_details(self):
        """
        try to get details for all user schedules returned by list
        * getting user schedule details for schedules that are actually location schedules fails
        """
        ps = self.api.person_settings.schedules
        ls = self.api.telephony.schedules

        # Use the disposable calling user and prepare one location schedule plus one person schedule.
        target_user = self.target_user()
        location_schedule = Schedule(
            name=self.available_name(target_user, 'details_location'), type=ScheduleType.holidays
        )
        user_schedule = Schedule(name=self.available_name(target_user, 'details_user'), type=ScheduleType.holidays)
        location_schedule_id = None
        user_schedule_id = None
        try:
            # Create both schedules so the person list contains mixed location/person levels.
            location_schedule_id = ls.create(obj_id=target_user.location_id, schedule=location_schedule)
            user_schedule_id = ps.create(obj_id=target_user.person_id, schedule=user_schedule)

            # Read person-level schedule list and identify the location/person entries by type/name.
            user_schedules_after = {
                (s.schedule_type, s.name): s
                for s in ps.list(obj_id=target_user.person_id, schedule_type=ScheduleType.holidays)
            }
            location_key = (location_schedule.schedule_type, location_schedule.name)
            user_key = (user_schedule.schedule_type, user_schedule.name)

            # Location-backed entries appear in the person list but cannot be read via person details.
            with self.assertRaises(RestError):
                ps.details(
                    obj_id=target_user.person_id,
                    schedule_type=user_schedules_after[location_key].schedule_type,
                    schedule_id=user_schedules_after[location_key].schedule_id,
                )
            self.assertEqual(ScheduleLevel.location, user_schedules_after[location_key].level)

            # Person-backed entries can be read through the person schedule details endpoint.
            details = ps.details(
                obj_id=target_user.person_id,
                schedule_type=user_schedules_after[user_key].schedule_type,
                schedule_id=user_schedules_after[user_key].schedule_id,
            )
            self.assertEqual(user_schedule.name, details.name)
        finally:
            # Delete both temporary schedules, regardless of which assertion failed.
            self.delete_schedule(
                api=ps,
                obj_id=target_user.person_id,
                schedule_type=user_schedule.schedule_type,
                schedule_id=user_schedule_id,
            )
            self.delete_schedule(
                api=ls,
                obj_id=target_user.location_id,
                schedule_type=location_schedule.schedule_type,
                schedule_id=location_schedule_id,
            )

    def test_006_update_name(self):
        """
        try to change the name of a person schedule
        """
        ps = self.api.person_settings.schedules

        # Create a disposable person schedule to exercise the update endpoint.
        target_user = self.target_user()
        schedule = Schedule(name=self.available_name(target_user, 'rename'), type=ScheduleType.holidays)
        schedule_id = None
        updated_id = None
        try:
            # Create the schedule and read its initial details.
            schedule_id = ps.create(obj_id=target_user.person_id, schedule=schedule)
            target_schedule = ps.details(
                obj_id=target_user.person_id, schedule_type=schedule.schedule_type, schedule_id=schedule_id
            )

            # Add one event so the schedule update also proves event preservation.
            new_start_date = datetime.date.today()
            new_event = Event(
                name=f'{new_start_date.month:02}{new_start_date.day:02}',
                start_date=new_start_date,
                end_date=new_start_date,
                all_day_enabled=True,
            )
            print(f'adding new event to schedule: {new_event.name}')
            ps.event_create(
                obj_id=target_user.person_id,
                schedule_type=target_schedule.schedule_type,
                schedule_id=target_schedule.schedule_id,
                event=new_event,
            )
            target_schedule = ps.details(
                obj_id=target_user.person_id,
                schedule_type=target_schedule.schedule_type,
                schedule_id=target_schedule.schedule_id,
            )
            self.assertEqual(1, len(target_schedule.events))
            print(f'target schedule: {target_schedule.name}({target_schedule.schedule_type})')

            # Send a no-op rename update; the live API accepts the update but preserves the name.
            print(f'Updating schedule {target_schedule.name}')
            settings = Schedule(
                name=target_schedule.name,
                new_name=target_schedule.name,
                type=target_schedule.schedule_type,
            )
            updated_id = ps.update(
                obj_id=target_user.person_id, schedule_id=target_schedule.schedule_id, schedule=settings
            )

            print(f'updated id: {debug_schedule_id(updated_id)}')

            # Read details after update and verify name plus event content were preserved.
            updated_schedule = ps.details(
                obj_id=target_user.person_id, schedule_type=target_schedule.schedule_type, schedule_id=updated_id
            )

            self.assertEqual(target_schedule.name, updated_schedule.name)

            # The API may return a new id, so compare the rest of the model after normalizing id.
            updated_schedule.schedule_id = target_schedule.schedule_id
            self.assertEqual(target_schedule, updated_schedule)
        finally:
            # Delete either the updated schedule id, the original schedule id, or both if applicable.
            self.delete_schedule(
                api=ps,
                obj_id=target_user.person_id,
                schedule_type=schedule.schedule_type,
                schedule_id=updated_id,
            )
            self.delete_schedule(
                api=ps,
                obj_id=target_user.person_id,
                schedule_type=schedule.schedule_type,
                schedule_id=schedule_id,
            )

    def test_007_event_update_delete_and_schedule_delete(self):
        """
        create, update, and delete a user schedule event; then delete the schedule
        """
        ps = self.api.person_settings.schedules

        # Prepare a disposable person holiday schedule for event CRUD.
        target_user = self.target_user()
        schedule_type = ScheduleType.holidays
        schedule = Schedule(name=self.available_name(target_user, 'event_crud'), type=schedule_type)
        schedule_id = None
        event_id = None
        updated_event_id = None
        try:
            # Create the schedule and add one all-day event.
            schedule_id = ps.create(obj_id=target_user.person_id, schedule=schedule)
            event_date = datetime.date.today()
            event = Event(name='crud_event', start_date=event_date, end_date=event_date, all_day_enabled=True)
            event_id = ps.event_create(
                obj_id=target_user.person_id,
                schedule_type=schedule_type,
                schedule_id=schedule_id,
                event=event,
            )

            # Read event details and verify the created event name.
            details = ps.event_details(
                obj_id=target_user.person_id,
                schedule_type=schedule_type,
                schedule_id=schedule_id,
                event_id=event_id,
            )
            self.assertEqual(event.name, details.name)

            # Send an event update and verify the API preserves the fields being asserted.
            update = details.model_copy(deep=True)
            update.new_name = details.name
            updated_event_id = ps.event_update(
                obj_id=target_user.person_id,
                schedule_type=schedule_type,
                schedule_id=schedule_id,
                event=update,
            )
            updated = ps.event_details(
                obj_id=target_user.person_id,
                schedule_type=schedule_type,
                schedule_id=schedule_id,
                event_id=updated_event_id,
            )
            self.assertEqual(details.name, updated.name)
            self.assertEqual(details.start_date, updated.start_date)
            self.assertEqual(details.end_date, updated.end_date)

            # Delete the event and verify the schedule no longer has events.
            ps.event_delete(
                obj_id=target_user.person_id,
                schedule_type=schedule_type,
                schedule_id=schedule_id,
                event_id=updated_event_id,
            )
            updated_event_id = None
            event_id = None
            after_event_delete = ps.details(
                obj_id=target_user.person_id, schedule_type=schedule_type, schedule_id=schedule_id
            )
            self.assertFalse(after_event_delete.events)

            # Delete the schedule and verify it disappears from the person schedule list.
            ps.delete_schedule(obj_id=target_user.person_id, schedule_type=schedule_type, schedule_id=schedule_id)
            schedule_id = None
            schedules_after = list(ps.list(obj_id=target_user.person_id, schedule_type=schedule_type))
            self.assertIsNone(next((s for s in schedules_after if s.name == schedule.name), None))
        finally:
            # If event deletion did not complete, remove the event first.
            if schedule_id and (updated_event_id or event_id):
                with suppress(RestError):
                    ps.event_delete(
                        obj_id=target_user.person_id,
                        schedule_type=schedule_type,
                        schedule_id=schedule_id,
                        event_id=updated_event_id or event_id,
                    )

            # Delete the schedule if it still exists.
            self.delete_schedule(
                api=ps,
                obj_id=target_user.person_id,
                schedule_type=schedule_type,
                schedule_id=schedule_id,
            )


class TestLevel(TestCaseWithUsers, TestWithLocations):
    """
    Understand the level attribute in Schedule
    """

    @async_test
    async def test_001_level_returned_for_user_list(self):
        """
        When listing schedules for users then level is always set to USER or GROUP
        """
        # Read all user-visible schedules and skip if the org has none.
        schedules = chain.from_iterable(await all_user_schedules(self.async_api, self.users))
        if not schedules:
            self.skipTest('No schedules')

        # Verify every returned user-list entry includes a supported level.
        levels = set(schedule.level for schedule in schedules)
        self.assertFalse(levels - {'PEOPLE', 'LOCATION'})
        no_level = [s for s in schedules if not s.level]
        if no_level:
            print('\n'.join(f'{s}' for s in no_level))

        # Assert no user-list schedule is missing level metadata.
        self.assertFalse(no_level)

    @async_test
    async def test_002_level_not_returned_for_location_list(self):
        """
        When listing schedules for locations then level is never set
        """
        # Read all location schedules concurrently and flatten the result set.
        schedules = list(
            chain.from_iterable(
                await asyncio.gather(
                    *[self.async_api.telephony.schedules.list(obj_id=loc.location_id) for loc in self.locations]
                )
            )
        )
        if not schedules:
            self.skipTest('No schedules')

        # Verify the parsed SDK models do not expose level for location-list results.
        with_level = [s for s in schedules if s.level]
        if with_level:
            print('\n'.join(f'{s}' for s in with_level))

        # Inspect raw captured responses to make sure level is absent from API payloads too.
        requests = list(
            self.requests(
                method='GET', url_filter=re.compile(r'https://.+/v1/telephony/config/locations/[\w0-9]+/schedules')
            )
        )
        schedules_from_body = list(chain.from_iterable(r.response_body['schedules'] for r in requests))
        schedules_w_level = [s for s in schedules_from_body if 'level' in s]
        if schedules_w_level:
            print('\n'.join(f'{s}' for s in schedules_w_level))

        # Assert neither SDK models nor raw payloads include level for location-list results.
        self.assertFalse(with_level)
        self.assertFalse(schedules_w_level)

import asyncio
import json
import random
import uuid
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, timedelta
from typing import ClassVar

from pydantic import TypeAdapter

from examples.calendarific import CalendarifiyApi
from tests.base import TestCaseWithLog, async_test
from tests.testutil import new_operating_mode_names, create_operating_mode
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.common import IdAndName
from wxc_sdk.common.schedules import ScheduleLevel
from wxc_sdk.person_settings.forwarding import CallForwardingCommon
from wxc_sdk.telephony.location import TelephonyLocation
from wxc_sdk.telephony.operating_modes import (OperatingMode, OperatingModeSchedule, DifferentHoursDaily, DaySchedule,
                                               OperatingModeHoliday)


class TestOperatingModes(TestCaseWithLog):
    def test_list(self):
        """
        list all operating modes
        """
        modes = list(self.api.telephony.operating_modes.list())
        print(json.dumps(TypeAdapter(list[OperatingMode]).dump_python(modes, mode='json', by_alias=True),
                         indent=2))

    @async_test
    async def test_details(self):
        """
        get details for all operating modes
        """
        modes = list(self.api.telephony.operating_modes.list())
        details = await asyncio.gather(*[self.async_api.telephony.operating_modes.details(mode_id=m.id)
                                         for m in modes])
        print(json.dumps(TypeAdapter(list[OperatingMode]).dump_python(details, mode='json',
                                                                      by_alias=True, exclude_unset=True),
                         indent=2))


@dataclass(init=False)
class TestCreateOperatingModes(TestCaseWithLog):
    """
    Test creating operating modes
    """
    _locations: ClassVar[list[TelephonyLocation]] = None

    @property
    def locations(self) -> list[TelephonyLocation]:
        """
        Get locations
        """
        if self._locations is None:
            with self.no_log():
                self.__class__._locations = list(self.api.telephony.locations.list())
        return self._locations

    def new_mode_names(self) -> Generator[str, None, None]:
        """
        Generate new mode names
        """
        with self.no_log():
            new_names = new_operating_mode_names(self.api)
        return new_names

    def test_create_org(self):
        """
        create trivial org level operating mode
        """
        new_name = next(self.new_mode_names())
        settings = OperatingMode(name=new_name,
                                 type=OperatingModeSchedule.none_,
                                 level=ScheduleLevel.organization)
        mode_id = self.api.telephony.operating_modes.create(settings)
        try:
            details = self.api.telephony.operating_modes.details(mode_id)
            print(json.dumps(details.model_dump(mode='json', by_alias=True, exclude_unset=True),
                             indent=2))
        finally:
            self.api.telephony.operating_modes.delete(mode_id)

    def test_create_org_with_schedule_monday_nine_to_five(self):
        """
        create org level operating mode with schedule
        """
        new_name = next(self.new_mode_names())
        settings = OperatingMode(name=new_name,
                                 type=OperatingModeSchedule.different_hours_daily,
                                 level=ScheduleLevel.organization,
                                 different_hours_daily=DifferentHoursDaily(
                                     monday=DaySchedule(enabled=True,
                                                        start_time='09:00', end_time='17:00')),
                                 call_forwarding=CallForwardingCommon(enabled=True, destination='4711'))
        mode_id = self.api.telephony.operating_modes.create(settings)
        try:
            details = self.api.telephony.operating_modes.details(mode_id)
            print(json.dumps(details.model_dump(mode='json', by_alias=True, exclude_unset=True),
                             indent=2))
        finally:
            self.api.telephony.operating_modes.delete(mode_id)

    def test_create_location_with_schedule_monday_nine_to_five(self):
        """
        create location level operating mode
        """
        new_name = next(self.new_mode_names())
        location: TelephonyLocation = random.choice(self.locations)
        settings = OperatingMode(name=new_name,
                                 type=OperatingModeSchedule.different_hours_daily,
                                 level=ScheduleLevel.location,
                                 location=IdAndName(id=location.location_id),
                                 different_hours_daily=DifferentHoursDaily(
                                     monday=DaySchedule(enabled=True,
                                                        start_time='09:00', end_time='17:00')),
                                 call_forwarding=CallForwardingCommon(enabled=True, destination='4711'))
        mode_id = self.api.telephony.operating_modes.create(settings)
        try:
            details = self.api.telephony.operating_modes.details(mode_id)
            print(json.dumps(details.model_dump(mode='json', by_alias=True, exclude_unset=True),
                             indent=2))
            self.assertEqual(new_name, details.name)
            self.assertEqual(location.location_id, details.location.id)
        finally:
            self.api.telephony.operating_modes.delete(mode_id)

    @contextmanager
    def operating_mode_with_holidays(self, location: TelephonyLocation = None,
                                     holidays: list[OperatingModeHoliday] = None):
        """
        create operating mode with holidays
        """
        details = create_operating_mode(self.api, location, holidays)
        try:
            yield details
        finally:
            self.api.telephony.operating_modes.delete(details.id)

    def test_create_location_with_schedule_holidays(self):
        """
        create location level operating mode
        """
        year = date.today().year
        us_holidays = CalendarifiyApi().holidays(country='US', year=year, holiday_type='national')

        holidays = [OperatingModeHoliday(id=str(uuid.uuid4()), name=h.name[:30], all_day_enabled=True,
                                         start_date=h.date, end_date=h.date)
                    for h in us_holidays]
        location: TelephonyLocation = random.choice(self.locations)

        with self.operating_mode_with_holidays(holidays=holidays, location=location) as details:
            details: OperatingMode

            print(json.dumps(details.model_dump(mode='json', by_alias=True, exclude_unset=True),
                             indent=2))

            # verify that the creation request does not have IDs
            post_request = next(r for r in self.har_writer.har.log.entries if r.request.method == 'POST')
            post_data = json.loads(post_request.request.postData.text)
            holidays = TypeAdapter(list[OperatingModeHoliday]).validate_python(post_data['holidays'])
            self.assertTrue(all(h.id is None for h in holidays))

    def test_create_holidays_and_update(self):
        """
        create location level operating mode with holidays and update one holiday
        """
        with self.operating_mode_with_holidays() as details:
            details: OperatingMode
            print(json.dumps(details.model_dump(mode='json', by_alias=True, exclude_unset=True),
                             indent=2))

            # update one holiday
            holiday = details.holidays[0]

            # move to next year
            holiday.start_date = holiday.start_date.replace(year=holiday.start_date.year + 1)
            holiday.end_date = holiday.end_date.replace(year=holiday.end_date.year + 1)
            self.api.telephony.operating_modes.update(details.id, details)
            updated = self.api.telephony.operating_modes.details(details.id)
            self.assertEqual(holiday.start_date, updated.holidays[0].start_date)
            self.assertEqual(holiday.end_date, updated.holidays[0].end_date)

            # holiday id should change
            holiday_id_before = details.holidays[0].id
            holiday_id_after = updated.holidays[0].id
            print(f'holiday id before: {webex_id_to_uuid(holiday_id_before)}')
            print(f' holiday id after: {webex_id_to_uuid(holiday_id_after)}')
            self.assertNotEqual(holiday_id_before, holiday_id_after)

    def test_create_holidays_and_add_holiday(self):
        """
        create location level operating mode with holidays and add one holiday using operating_modes.update
        """
        with self.operating_mode_with_holidays() as details:
            details: OperatingMode

            # add one holiday
            day_after_tomorrow = date.today() + timedelta(days=2)
            holiday = OperatingModeHoliday(name='new holiday', all_day_enabled=True,
                                           start_date=day_after_tomorrow, end_date=day_after_tomorrow)
            details.holidays.append(holiday)
            self.api.telephony.operating_modes.update(details.id, details)
            updated = self.api.telephony.operating_modes.details(details.id)
            self.assertEqual(len(details.holidays), len(updated.holidays))
            sorted_before = sorted(details.holidays, key=lambda x: (x.start_date, x.name))
            sorted_after = sorted(updated.holidays, key=lambda x: (x.start_date, x.name))
            self.assertTrue(all(h1.start_date == h2.start_date and h1.name == h2.name
                                for h1, h2 in zip(sorted_before, sorted_after)))

    @async_test
    async def test_create_holidays_and_get_holiday_details(self):
        """
        Create an operating mode with holidays and get details for all holidays
        """
        with self.operating_mode_with_holidays() as details:
            details: OperatingMode
            holiday_details = await asyncio.gather(
                *[self.async_api.telephony.operating_modes.holiday_details(details.id, h.id)
                  for h in details.holidays])
            # this fails, tracked by issue 204
            self.assertEqual(details.holidays, holiday_details)

    def test_holidays_and_create_holiday(self):
        """
        Create an operating mode with holidays and create one more holiday
        """
        with self.operating_mode_with_holidays() as details:
            details: OperatingMode
            # create a new holiday
            day_after_tomorrow = date.today() + timedelta(days=2)
            holiday = OperatingModeHoliday(name='new holiday', all_day_enabled=True,
                                           start_date=day_after_tomorrow, end_date=day_after_tomorrow)
            holiday_id = self.api.telephony.operating_modes.holiday_create(details.id, holiday)
            details_after = self.api.telephony.operating_modes.details(details.id)
            # there now should be one more holiday
            self.assertEqual(len(details.holidays) + 1, len(details_after.holidays))
            # .. and the new holiday id should be in the list
            self.assertIsNotNone(next((h for h in details_after.holidays if h.id == holiday_id), None))

    def test_holidays_and_change_holiday(self):
        """
        Create an operating mode with holidays and change one holiday
        """
        with self.operating_mode_with_holidays() as details:
            details: OperatingMode
            # change a holiday
            update = OperatingModeHoliday(name='updated name')
            holiday = details.holidays[0]
            self.api.telephony.operating_modes.holiday_update(details.id, holiday.id, update)

            # get updated holiday
            details_after = self.api.telephony.operating_modes.details(details.id)
            holiday_after = self.api.telephony.operating_modes.holiday_details(details.id, holiday.id)

            # name should be updated
            self.assertEqual(update.name, holiday_after.name)
            holiday_in_details = next(h for h in details_after.holidays if h.id == holiday.id)
            self.assertEqual(update.name, holiday_in_details.name)

            # but other than that there should be no change
            holiday.name = update.name
            # .. except for all_day_enabled; tracked by issue 204
            holiday_after.all_day_enabled = holiday.all_day_enabled
            self.assertEqual(holiday, holiday_after)
            self.assertEqual(holiday, holiday_in_details)

    def test_holidays_delete_holiday(self):
        """
        Create an operating mode with holidays and delete one holiday
        """
        with self.operating_mode_with_holidays() as details:
            details: OperatingMode
            # delete a holiday
            holiday = details.holidays[0]
            self.api.telephony.operating_modes.holiday_delete(details.id, holiday.id)

            # get updated holiday
            details_after = self.api.telephony.operating_modes.details(details.id)
            self.assertEqual(len(details.holidays) - 1, len(details_after.holidays))
            with self.assertRaises(StopIteration):
                next(h for h in details_after.holidays if h.id == holiday.id)

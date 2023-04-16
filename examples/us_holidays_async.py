#!/usr/bin/env python
"""
Example script
Create a holiday schedule for all US locations with all national holidays

Using the asyc SDK variant
"""
import asyncio
import functools
import logging
from collections import defaultdict
from datetime import date
from typing import List

from dotenv import load_dotenv

from calendarific import CalendarifiyApi, Holiday
from wxc_sdk.all_types import ScheduleType, Event, Schedule
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.locations import Location

log = logging.getLogger(__name__)

# a lock per location to protect observe_in_location()
location_locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

# Use parallel tasks for provisioning?
USE_TASKS = True

# True: delete holiday schedule instead of creating one
CLEAN_UP = False

# first and last year for which to create public holiday events
FIRST_YEAR = 2022
LAST_YEAR = 2024

LAST_YEAR = not CLEAN_UP and LAST_YEAR or FIRST_YEAR


async def observe_in_location(*, api: AsWebexSimpleApi, location: Location, holidays: List[Holiday]):
    """
    create/update a "National Holiday" schedule in one location

    :param api: Webex api
    :type api: WebexSimpleApi
    :param location: location to work on
    :type location: Location
    :param holidays: list of holidays to observe
    :type holidays: List[Holiday]
    """
    # there should always only one thread messing with the holiday schedule of a location
    async with location_locks[location.location_id]:
        year = holidays[0].date.year
        schedule_name = 'National Holidays'

        # shortcut
        ats = api.telephony.schedules

        # existing "National Holiday" schedule or None
        schedule = next((schedule
                         for schedule in await ats.list(obj_id=location.location_id,
                                                        schedule_type=ScheduleType.holidays,
                                                        name=schedule_name)
                         if schedule.name == schedule_name),
                        None)
        if CLEAN_UP:
            if schedule:
                log.info(f'Delete schedule {schedule.name} in location {schedule.location_name}')
                await ats.delete_schedule(obj_id=location.location_id,
                                          schedule_type=ScheduleType.holidays,
                                          schedule_id=schedule.schedule_id)
            return
        if schedule:
            # we need the details: list response doesn't have events
            schedule = await ats.details(obj_id=location.location_id,
                                         schedule_type=ScheduleType.holidays,
                                         schedule_id=schedule.schedule_id)
        # create list of desired schedule entries
        #   * one per holiday
        #   * only future holidays
        #   * not on a Sunday
        today = date.today()
        events = [Event(name=f'{holiday.name} {holiday.date.year}',
                        start_date=holiday.date,
                        end_date=holiday.date,
                        all_day_enabled=True)
                  for holiday in holidays
                  if holiday.date >= today and holiday.date.weekday() != 6]

        if not schedule:
            # create new schedule
            log.debug(f'observe_in_location({location.name}, {year}): no existing schedule')
            if not events:
                log.info(f'observe_in_location({location.name}, {year}): no existing schedule, no events, done')
                return
            schedule = Schedule(name=schedule_name,
                                schedule_type=ScheduleType.holidays,
                                events=events)
            log.debug(
                f'observe_in_location({location.name}, {year}): creating schedule "{schedule_name}" with {len(events)} '
                f'events')
            schedule_id = await ats.create(obj_id=location.location_id, schedule=schedule)
            log.info(f'observe_in_location({location.name}, {year}): new schedule id: {schedule_id}, done')
            return

        # update existing schedule
        # delete existing events in the past
        to_delete = [event
                     for event in schedule.events
                     if event.start_date < today]
        if to_delete:
            log.debug(f'observe_in_location({location.name}, {year}): deleting {len(to_delete)} outdated events')
            if USE_TASKS:
                await asyncio.gather(*[ats.event_delete(obj_id=location.location_id,
                                                        schedule_type=ScheduleType.holidays,
                                                        schedule_id=schedule.schedule_id,
                                                        event_id=event.event_id)
                                       for event in to_delete])
            else:
                for event in to_delete:
                    await ats.event_delete(obj_id=location.location_id,
                                           schedule_type=ScheduleType.holidays,
                                           schedule_id=schedule.schedule_id,
                                           event_id=event.event_id)

        # add events which don't exist yet
        existing_dates = set(event.start_date
                             for event in schedule.events)
        to_add = [event
                  for event in events
                  if event.start_date not in existing_dates]
        if not to_add:
            log.info(f'observe_in_location({location.name}, {year}): no events to add, done.')
            return
        log.debug(f'observe_in_location({location.name}, {year}): creating {len(to_add)} new events.')
        if USE_TASKS:
            await asyncio.gather(*[ats.event_create(obj_id=location.location_id,
                                                    schedule_type=ScheduleType.holidays,
                                                    schedule_id=schedule.schedule_id,
                                                    event=event)
                                   for event in to_add])
        else:
            for event in to_add:
                await ats.event_create(obj_id=location.location_id,
                                       schedule_type=ScheduleType.holidays,
                                       schedule_id=schedule.schedule_id,
                                       event=event)
        log.info(f'observe_in_location({location.name}, {year}): done.')
    return


async def observe_national_holidays(*, api: AsWebexSimpleApi, locations: List[Location],
                                    year: int = None):
    """
    US national holidays for given locations

    :param api: Webex api
    :type api: WebexSimpleApi
    :param locations: list of locations in which US national holidays should be observed
    :type locations: List[Location]
    :param year: year for national holidays. Default: current year
    :type year: int
    """
    # default: this year
    year = year or date.today().year

    # get national holidays for specified year
    loop = asyncio.get_running_loop()
    # avoid sync all:
    # holidays = CalendarifiyApi().holidays(country='US', year=year, holiday_type='national')
    holidays = await loop.run_in_executor(None, functools.partial(CalendarifiyApi().holidays,
                                                                  country='US', year=year, holiday_type='national'))

    # update holiday schedule for each location
    if USE_TASKS:
        await asyncio.gather(*[observe_in_location(api=api, location=location, holidays=holidays)
                               for location in locations])
    else:
        for location in locations:
            await observe_in_location(api=api, location=location, holidays=holidays)
    return


if __name__ == '__main__':
    # read dotenv which has some environment variables like Webex API token and Calendarify
    # API key.
    load_dotenv()

    # enable logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(threadName)s %(name)s: %(message)s')
    logging.getLogger('urllib3').setLevel(logging.INFO)
    logging.getLogger('wxc_sdk.as_rest').setLevel(logging.INFO)

    # the actual action
    async def do_provision():

        async with AsWebexSimpleApi(concurrent_requests=5) as wx_api:
            # get all US locations
            log.info('Getting locations...')
            us_locations = [location
                            for location in await wx_api.locations.list()
                            if location.address.country == 'US']

            # set up location locks
            # location_locks is a defaultdict -> accessing with all potential keys creates the locks
            list(location_locks[loc.location_id] for loc in us_locations)

            # create national holiday schedule for given year(s) and locations
            if USE_TASKS:
                await asyncio.gather(*[observe_national_holidays(api=wx_api, year=year, locations=us_locations)
                                       for year in range(FIRST_YEAR, LAST_YEAR + 1)])
            else:
                for year in range(FIRST_YEAR, LAST_YEAR + 1):
                    await observe_national_holidays(api=wx_api, year=year, locations=us_locations)

    asyncio.run(do_provision())

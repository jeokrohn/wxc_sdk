"""
Webex Calling Organization Settings with Location Scheduling
Webex Calling Organization Settings support reading and writing of Webex Calling settings for a specific organization.

Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
spark-admin:telephony_config_read, as the current set of APIs is designed to provide supplemental information for
administrators utilizing People Webex Calling APIs.

A partner administrator can retrieve or change settings in a customer's organization using the optional OrgId query
parameter.
"""
import datetime
from enum import Enum
from typing import Optional, List, Union
import json
from pydantic import Field
from collections.abc import Generator

from ..api_child import ApiChild
from ..base import ApiModel
from requests import Session

__all__ = ['ScheduleAPI', 'ScheduleType', 'ScheduleMonth', 'ScheduleDay', 'ScheduleWeek', 'RecurWeekly',
           'RecurYearlyByDate', 'RecurYearlyByDay', 'Recurrence', 'Event', 'Schedule']

ScheduleTypeOrStr = Union[str, 'ScheduleType']


class ScheduleType(str, Enum):
    business_hours = 'businessHours'
    holidays = 'holidays'

    @staticmethod
    def type_or_str(v: ScheduleTypeOrStr) -> 'ScheduleType':
        if isinstance(v, ScheduleType):
            return v
        return ScheduleType(v)


class ScheduleMonth(str, Enum):
    """
    Month used in yearly recurrences
    """
    jan = 'JANUARY'
    feb = 'FEBRUARY'
    mar = 'MARCH'
    apr = 'APRIL'
    may = 'MAY'
    jun = 'JUNE'
    jul = 'JULY'
    aug = 'AUGUST'
    sep = 'SEPTEMBER'
    oct = 'OCTOBER'
    nov = 'NOVEMBER'
    dec = 'DECEMBER'


class ScheduleDay(str, Enum):
    monday = 'MONDAY'
    tuesday = 'TUESDAY'
    wednesday = 'WEDNESDAY'
    thursday = 'THURSDAY'
    friday = 'FRIDAY'
    saturday = 'SATURDAY'
    sunday = 'SUNDAY'

    @staticmethod
    def mon_to_fri():
        return [ScheduleDay.monday, ScheduleDay.tuesday, ScheduleDay.wednesday, ScheduleDay.thursday,
                ScheduleDay.friday]


class ScheduleWeek(str, Enum):
    """
    Week used in monthly recurrence
    """
    first = 'FIRST'
    second = 'SECOND'
    third = 'THIRD'
    fourth = 'FOURTH'


class RecurWeekly(ApiModel):
    sunday: bool = Field(default=False)
    monday: bool = Field(default=False)
    tuesday: bool = Field(default=False)
    wednesday: bool = Field(default=False)
    thursday: bool = Field(default=False)
    friday: bool = Field(default=False)
    saturday: bool = Field(default=False)

    def enable_day(self, day: Union[ScheduleDay, datetime.date]):
        """
        set recurrence to True on one day
        :param day:
        """
        if isinstance(day, datetime.date):
            day_name = day.strftime('%A').lower()
            setattr(self, day_name, True)
        else:
            setattr(self, day.name, True)

    @staticmethod
    def single_day(day: Union[ScheduleDay, datetime.date]) -> 'RecurWeekly':
        """
        Weekly recurrence for a single day
        :param day:
        :return:
        """
        r = RecurWeekly()
        r.enable_day(day=day)
        return r


class RecurYearlyByDate(ApiModel):
    day_of_month: int
    month: ScheduleMonth

    @staticmethod
    def from_date(date: datetime.date) -> 'RecurYearlyByDate':
        return RecurYearlyByDate(day_of_month=date.day, month=date.strftime('%B').upper())


class RecurYearlyByDay(ApiModel):
    day: ScheduleDay
    week: ScheduleWeek
    month: ScheduleMonth


class Recurrence(ApiModel):
    recur_for_ever: bool
    recur_end_date: Optional[datetime.date]
    recur_weekly: Optional[RecurWeekly]
    recur_yearly_by_date: Optional[RecurYearlyByDate]
    recur_yearly_by_day: Optional[RecurYearlyByDay]

    @staticmethod
    def every_week(day: Union[ScheduleDay, datetime.date]) -> 'Recurrence':
        """
        Recurrence for a single day, forever
        :param day:
        :return:
        """
        return Recurrence(recur_for_ever=True,
                          recur_weekly=RecurWeekly.single_day(day=day))


class Event(ApiModel):
    event_id: Optional[str] = Field(alias='id')
    name: str
    new_name: Optional[str]  # only used in updates
    start_date: datetime.date
    end_date: datetime.date
    start_time: Optional[datetime.time]
    end_time: Optional[datetime.time]
    all_day_enabled: bool
    recurrence: Optional[Recurrence]

    class Config:
        json_encoders = {
            datetime.time: lambda v: v.strftime('%H:%M')
        }

    @staticmethod
    def day_start_end(name: str,
                      day: datetime.date,
                      start_time: Union[int, datetime.time],
                      end_time: Union[int, datetime.time]) -> 'Event':
        """
        Event on a given day with specified start and end time and weekly recurrence
        :param name:
        :param day:
        :param start_time:
        :param end_time:
        :return:
        """
        if isinstance(start_time, int):
            start_time = datetime.time(start_time)
        if isinstance(end_time, int):
            end_time = datetime.time(end_time)
        return Event(name=name,
                     start_date=day, end_date=day,
                     start_time=start_time,
                     end_time=end_time,
                     all_day_enabled=False,
                     recurrence=Recurrence.every_week(day=day))


class Schedule(ApiModel):
    name: str
    schedule_id: Optional[str] = Field(alias='id')
    location_name: Optional[str]  # not returned by details()
    location_id: Optional[str]  # not returned by details()
    schedule_type: ScheduleType = Field(alias='type')
    events: List[Event] = Field(default_factory=list)

    class Config:
        json_encoders = {
            # datetime objects are encoded as HH:MM
            datetime.time: lambda v: v.strftime('%H:%M')
        }

    @property
    def selector(self) -> dict:
        """
        A selector for this schedule. Can be used as parameters for details() call
        """
        return {'location_id': self.location_id,
                'schedule_type': self.schedule_type,
                'schedule_id': self.schedule_id}

    @staticmethod
    def business(name: str,
                 day_start: Union[int, datetime.time] = 9,
                 day_end: Union[int, datetime.time] = 17,
                 break_start: Union[int, datetime.time] = 12,
                 break_end: Union[int, datetime.time] = 13) -> 'Schedule':
        """
        Business schedule with the given times Mon-Fri
        :param name:
        :param day_start:
        :param day_end:
        :param break_start:
        :param break_end:
        :return:
        """
        dt_day = datetime.date.today()
        weekday = dt_day.weekday()
        # we want to start on a monday
        if weekday:
            dt_day = dt_day + datetime.timedelta(days=7 - weekday)

        schedule = Schedule(name=name, schedule_type=ScheduleType.business_hours)
        for day in ScheduleDay.mon_to_fri():
            # Two events
            # * from start to break
            # * from break end to end of day
            schedule.events.append(Event.day_start_end(name=f'{day.value} 1',
                                                       day=dt_day,
                                                       start_time=day_start,
                                                       end_time=break_start))
            schedule.events.append(Event.day_start_end(name=f'{day.value} 2',
                                                       day=dt_day,
                                                       start_time=break_end,
                                                       end_time=day_end))
            dt_day = dt_day + datetime.timedelta(days=1)
        return schedule


class ScheduleAPI(ApiChild, base='telephony/config/locations'):

    def _endpoint(self, *, location_id: str, schedule_type: ScheduleTypeOrStr = None, schedule_id: str = None,
                  event_id: str = None):
        """
        location specific feature endpoint like v1/telephony/config/locations/{location_id}/schedules/....

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param schedule_type: type of schedule
        :type schedule_type: ScheduleType
        :param schedule_id: schedule id
        :type schedule_id: str
        :return: full endpoint
        :rtype: str
        """
        ep = super().ep(path=f'{location_id}/schedules')
        if schedule_type is not None:
            schedule_type = ScheduleType.type_or_str(schedule_type)
            ep = f'{ep}/{schedule_type.value}/{schedule_id}'
            if event_id is not None:
                event_id = event_id and f'/{event_id}' or ''
                ep = f'{ep}/events{event_id}'
        return ep

    def list(self, *, location_id: str, org_id: str = None, schedule_type: ScheduleType = None,
             name: str = None) -> Generator[Schedule, None, None]:
        """
        Read the List of Schedules
        List all Schedules for the given location of the organization.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Return the list of schedules for this location.
        :type location_id: str
        :param org_id: List schedules for this organization.
        :type org_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :param name: Only return schedules with the matching name.
        :return: yields schedules
        """
        url = self._endpoint(location_id=location_id)
        params = dict()
        if schedule_type is not None:
            params['type'] = schedule_type.value
        if name is not None:
            params['name'] = name
        if org_id is not None:
            params['orgId'] = org_id

        # with Session() as session:
        #     r = session.get(url=url, headers={'authorization': f'Bearer {self.session._tokens.access_token}'})
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Schedule, params=params or None)

    def details(self, *, location_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                org_id: str = None) -> Schedule:
        """
        Get Details for a Schedule
        Retrieve Schedule details.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Retrieving schedule details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve schedule details in this location.
        :type location_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Retrieve the schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Retrieve schedule details from this organization.
        :type org_id: str
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, schedule_type=schedule_type, schedule_id=schedule_id)
        data = self.get(url, params=params)
        result = Schedule.parse_obj(data)
        return result

    def create(self, *, location_id: str, schedule: Schedule, org_id: str = None) -> str:
        """
        Create a Schedule
        Create new Schedule for the given location.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Creating a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Create the schedule for this location.
        :type location_id: str
        :param schedule: Schedule to be created
        :type schedule: Schedule
        :param org_id: Create the schedule for this organization.
        :type org_id: str
        :return: ID of the newly created schedule.
        :rtype: str
        """
        schedule_data = schedule.json(exclude={'schedule_id'})
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        data = self.post(url, data=schedule_data, params=params)
        result = data['id']
        return result

    def update(self, *, schedule: Schedule, location_id: str = None, schedule_type: ScheduleTypeOrStr = None,
               schedule_id: str = None, org_id: str = None) -> str:
        """
        Update a Schedule
        Update the designated Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Updating a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        NOTE: The Schedule ID will change upon modification of the Schedule name

        :param schedule: data for the update
        :type schedule: Schedule
        :param location_id: Location in which this schedule exists. Default: location_id from schedule
        :type location_id: str
        :param schedule_type: Type of the schedule. Default: schedule_type from schedule
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Update schedule with the matching ID. Default: schedule_id from schedule
        :type schedule_id: str
        :param org_id: Update schedule from this organization.
        :type org_id: str
        :return: schedule id
        """
        location_id = location_id or schedule.location_id
        schedule_type = schedule_type or schedule.schedule_type
        schedule_id = schedule_id or schedule.schedule_id
        # update only uses name and events
        schedule_data = json.loads(schedule.json(include={'name', 'events'}))
        for event in schedule_data['events']:
            # mo id in updates
            event.pop('id', None)
            # new_name uses name as default
            event['newName'] = event.get('newName', None) or event['name']
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, schedule_type=schedule_type, schedule_id=schedule_id)
        data = self.put(url, json=schedule_data, params=params)
        return data['id']

        pass

    def delete_schedule(self, *, location_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                        org_id: str = None):
        """
        Delete a Schedule
        Delete the designated Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Deleting a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a schedule.
        :type location_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Delete the schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Retrieve schedule details from this organization.
        :type org_id: str
        :return:
        """
        url = self._endpoint(location_id=location_id, schedule_type=schedule_type, schedule_id=schedule_id)
        params = org_id and {'orgId': org_id} or None
        self.delete(url, params=params)

    def event_details(self, *, location_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                      event_id: str, org_id: str = None) -> Event:
        """
        Get Details for a Schedule Event
        Retrieve Schedule Event details.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Retrieving schedule event details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve schedule event details in this location.
        :type location_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Retrieve schedule event details in this location.
        :type schedule_id: str
        :param event_id: Retrieve the schedule event with the matching schedule event ID.
        :type event_id: str
        :param org_id: Retrieve schedule event details from this organization.
        :type org_id: str
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id=event_id)
        data = self.get(url, params=params)
        result = Event.parse_obj(data)
        return result

    def event_create(self, *, location_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                     event: Event, org_id: str = None) -> str:
        """
        Create a Schedule Event
        Create new Event for the given location Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Creating a schedule event requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the schedule for this location.
        :type location_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Create event for a given schedule ID.
        :type schedule_id: str
        :param event: event data
        :type event: Event
        :param org_id: Retrieve schedule event details from this organization.
        :type org_id: str
        :return: event id
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id='')
        data = event.json(exclude={'event_id'})
        data = self.post(url, data=data, params=params)
        return data['id']

    def event_update(self, *, location_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                     event: Event, event_id: str = None, org_id: str = None) -> str:
        """
        Update a Schedule Event
        Update the designated Schedule Event.
        
        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for 
        example auto attendants, can perform a specific action.
        
        Updating a schedule event requires a full administrator auth token with a scope of 
        spark-admin:telephony_config_write.
        
        NOTE: The Schedule Event ID will change upon modification of the Schedule event name.

        :param location_id: Location in which this schedule event exists.
        :type location_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Update schedule event with the matching schedule ID.
        :type schedule_id: str
        :param event: update settings
        :type event: Event
        :param event_id: Update the schedule event with the matching schedule event ID. Default: event id from event
        :type event_id: str
        :param org_id: Update schedule from this organization.
        :type org_id: str
        :return: event id; changed if name changed
        """
        event_id = event_id or event.event_id
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id=event_id)
        event_data = event.json(exclude={'event_id'})
        data = self.put(url, data=event_data, params=params)
        return data['id']

    def event_delete(self, *, location_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                     event_id: str, org_id: str = None):
        """
        # TODO: update documentation

        :param location_id: Location from which to delete a schedule.
        :type location_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Delete schedule event with the matching schedule ID.
        :type schedule_id: str
        :param event_id: Delete the schedule event with the matching schedule event ID. Default: event id from event
        :type event_id: str
        :param org_id: Delete schedule from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id=event_id)
        self.delete(url, params=params)

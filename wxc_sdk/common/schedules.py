"""
Schedules for locations or users
"""
import datetime
from collections.abc import Generator
from enum import Enum
from typing import Optional, Union

from pydantic import Field

from ..api_child import ApiChild
from ..base import ApiModel
from ..rest import RestSession

__all__ = ['ScheduleApi', 'ScheduleType', 'ScheduleMonth', 'ScheduleDay', 'ScheduleWeek', 'RecurWeekly',
           'RecurYearlyByDate', 'RecurYearlyByDay', 'Recurrence', 'Event', 'Schedule', 'ScheduleApiBase',
           'ScheduleTypeOrStr']

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
    """
    Specifies the event recur weekly on the designated days of the week
    """
    #: Specifies the number of weeks between the start of each recurrence.
    recur_interval: Optional[int]
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

        :param day: can either be a :class:`ScheduleDay` or a :class:`datetime.date`
        """
        if isinstance(day, datetime.date):
            # determine name of day in lower case
            day_name = day.strftime('%A').lower()
            setattr(self, day_name, True)
        else:
            setattr(self, day.name, True)

    @staticmethod
    def single_day(day: Union[ScheduleDay, datetime.date], recur_interval: int = 1) -> 'RecurWeekly':
        """
        Weekly recurrence for a single day

        :param day: can either be a :class:`ScheduleDay` or a :class:`datetime.date`
        :param recur_interval: Specifies the number of weeks between the start of each recurrence.
        :return: weekly recurrence
        :rtype: class:`RecurWeekly`
        """
        r = RecurWeekly(recur_interval=recur_interval)
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


class RecurDaily(ApiModel):
    """
    Specifies the number of days between the start of each recurrence and is not allowed with recurWeekly.
    """
    #: Recurring interval in Daily. The Number of days after the start when an event will repeat.
    #: Repetitions cannot overlap.
    recur_interval: int


class Recurrence(ApiModel):
    """
    Recurrence scheme for an event.
    Location schedules support:  recur_weekly, recur_yearly_by_date, recur_yearly_by_day
    User schedules support: recur_daily, recur_weekly
    """
    #: True if the event repeats forever. Requires either recurDaily or recurWeekly to be specified.
    #: user and location schedules
    recur_for_ever: Optional[bool]
    #: End date for the recurring event in the format of YYYY-MM-DD. Requires either recur_daily or recur_weekly to
    #: be specified. User and location schedules
    recur_end_date: Optional[datetime.date]
    #: End recurrence after the event has repeated the specified number of times. Requires either
    #: recur_daily or recur_weekly to be specified. User schedules only.
    recur_end_of_occurrence: Optional[int]
    #: Specifies the number of days between the start of each recurrence and is not allowed with recurWeekly.
    #: Only allowed for user schedules
    recur_daily: Optional[RecurDaily]
    #: Specifies the event recur weekly on the designated days of the week and is not allowed with recur_daily.
    #: allowed for user and location schedules
    recur_weekly: Optional[RecurWeekly]
    #: only allowed for location schedules
    recur_yearly_by_date: Optional[RecurYearlyByDate]
    #: only allowed for location schedules
    recur_yearly_by_day: Optional[RecurYearlyByDay]

    @staticmethod
    def every_week(day: Union[ScheduleDay, datetime.date]) -> 'Recurrence':
        """
        weekly recurrence for a single day, forever

        :param day: can either be a :class:`ScheduleDay` or a :class:`datetime.date`
        :return: weekly recurrence
        :rtype: :class:`Recurrence`
        """
        return Recurrence(recur_for_ever=True,
                          recur_weekly=RecurWeekly.single_day(day=day))


class Event(ApiModel):
    #: unique id of the event
    event_id: Optional[str] = Field(alias='id')
    #: Name for the event.
    name: str
    #: new name for the event, only used in updates
    new_name: Optional[str]
    #: Start date of the event, or first occurrence if repeating. This field is required
    #: if all_day_enabled field is present.
    start_date: Optional[datetime.date]
    #: End date of the event, or first occurrence if repeating, in the format of YYYY-MM-DD. This field is required
    #: if all_day_enabled field is present.
    end_date: Optional[datetime.date]
    #: Start time of the event. This field is required if all_day_enabled
    #: field is false or omitted.
    start_time: Optional[datetime.time]
    #: End time of the event. This field is required if all_day_enabled field
    #: is false or omitted.
    end_time: Optional[datetime.time]
    #: True if it is all-day event.
    all_day_enabled: Optional[bool]
    #: Recurrence scheme for an event.
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

        :param name: name of the event
        :param day: start date
        :param start_time: start time, can be hour or :class:`datetime.time`
        :param end_time: end time, can be hour or :class:`datetime.time`
        :return: event
        :rtype: :class:`Event`
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
    #: Name for the schedule.
    name: Optional[str]
    #: new name for the schedule. Only used in update()
    new_name: Optional[str]
    #: Identifier for a schedule.
    schedule_id: Optional[str] = Field(alias='id')
    #: location name, only returned by list() for location schedules
    location_name: Optional[str]
    #: location id, only returned by list() for location schedules
    location_id: Optional[str]
    #: Indicates the schedule type whether businessHours or holidays
    schedule_type: ScheduleType = Field(alias='type')
    #: Indicates a list of events.
    events: Optional[list[Event]]

    class Config:
        json_encoders = {
            # datetime objects are encoded as HH:MM
            datetime.time: lambda v: v.strftime('%H:%M')
        }

    @staticmethod
    def business(name: str,
                 day_start: Union[int, datetime.time] = 9,
                 day_end: Union[int, datetime.time] = 17,
                 break_start: Union[int, datetime.time] = 12,
                 break_end: Union[int, datetime.time] = 13) -> 'Schedule':
        """
        Business schedule with the given times Mon-Fri

        :param name: schedule name
        :param day_start: daily start time, default: 9
        :type day_start: int
        :param day_end: daily end time, default: 17
        :type day_end: int
        :param break_start: start of break, default: 12
        :type break_start: int
        :param break_end: end of break, default: 13
        :type break_end: int
        :return: business hours schedule
        :rtype: :class:`Schedule`
        """
        dt_day = datetime.date.today()
        weekday = dt_day.weekday()
        # we want to start on a monday
        if weekday:
            dt_day = dt_day + datetime.timedelta(days=7 - weekday)

        schedule = Schedule(name=name, schedule_type=ScheduleType.business_hours)
        schedule.events = []
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

    def create_update(self, *, update: bool = False) -> str:
        """
        JSON for create or update

        :meta private:
        """
        working_copy = self.copy(deep=True)
        if update:
            for event in working_copy.events or []:
                event.new_name = event.new_name or event.name
        return working_copy.json(exclude={'schedule_id': True,
                                          'location_name': True,
                                          'location_id': True,
                                          'events': {'__all__': {'event_id': True}}})


class ScheduleApiBase(str, Enum):
    """
    possible base URLs for schedule api: locations or users
    """
    locations = 'telephony/config/locations'
    people = 'people'


class ScheduleApi(ApiChild, base='telephony/config/locations'):
    """
    Schedules API
    """

    def __init__(self, *, session: RestSession, base: ScheduleApiBase):
        super().__init__(session=session, base=base.value)
        if base == ScheduleApiBase.people:
            self.after_id = '/features/schedules'
        elif base == ScheduleApiBase.locations:
            self.after_id = '/schedules'
        else:
            raise ValueError('unexpected value for base')

    def _endpoint(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr = None, schedule_id: str = None,
                  event_id: str = None):
        """
        location specific feature endpoint like v1/telephony/config/locations/{obj_id}/schedules/.... or
        v1/people/{obj_id}/features/schedules/....

        :meta private:
        :param obj_id: Unique identifier for the location or user
        :type obj_id: str
        :param schedule_type: type of schedule
        :type schedule_type: ScheduleType
        :param schedule_id: schedule id
        :type schedule_id: str
        :return: full endpoint
        :rtype: str
        """
        ep = self.ep(path=f'{obj_id}{self.after_id}')
        if schedule_type is not None:
            schedule_type = ScheduleType.type_or_str(schedule_type)
            ep = f'{ep}/{schedule_type.value}/{schedule_id}'
            if event_id is not None:
                event_id = event_id and f'/{event_id}' or ''
                ep = f'{ep}/events{event_id}'
        return ep

    def list(self, *, obj_id: str, org_id: str = None, schedule_type: ScheduleType = None,
             name: str = None, **params) -> Generator[Schedule, None, None]:
        """
        List of Schedules for a Person or location

        List schedules for a person or location in an organization.

        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week
        by defining one or more events. holidays schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param obj_id: Return the list of schedules for this location or user
        :type obj_id: str
        :param org_id: List schedules for this organization.
        :type org_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :param name: Only return schedules with the matching name.
        :return: yields schedules
        """
        url = self._endpoint(obj_id=obj_id)
        if schedule_type is not None:
            params['type'] = schedule_type.value
        if name is not None:
            params['name'] = name
        if org_id is not None:
            params['orgId'] = org_id

        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Schedule, params=params or None)

    def details(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                org_id: str = None) -> Schedule:
        """
        Get Details for a Schedule

        Retrieve Schedule details.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Retrieving schedule details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param obj_id: Retrieve schedule details in this location or user
        :type obj_id: str
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
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id)
        data = self.get(url, params=params)
        result = Schedule.parse_obj(data)
        return result

    def create(self, *, obj_id: str, schedule: Schedule, org_id: str = None) -> str:
        """
        Create a Schedule

        Create new Schedule for the given location.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Creating a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param obj_id: Create the schedule for this location or user
        :type obj_id: str
        :param schedule: Schedule to be created
        :type schedule: Schedule
        :param org_id: Create the schedule for this organization.
        :type org_id: str
        :return: ID of the newly created schedule.
        :rtype: str
        """
        schedule_data = schedule.create_update()
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id)
        data = self.post(url, data=schedule_data, params=params)
        result = data['id']
        return result

    def update(self, *, obj_id: str, schedule: Schedule, schedule_type: ScheduleTypeOrStr = None,
               schedule_id: str = None, org_id: str = None) -> str:
        """
        Update a Schedule

        Update the designated Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Updating a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        NOTE: The Schedule ID will change upon modification of the Schedule name

        :param obj_id: Location or user for  which this schedule exists
        :type obj_id: str
        :param schedule: data for the update
        :type schedule: Schedule
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
        schedule_type = schedule_type or schedule.schedule_type
        schedule_id = schedule_id or schedule.schedule_id
        schedule_data = schedule.create_update(update=True)
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id)
        data = self.put(url, data=schedule_data, params=params)
        return data['id']

    def delete_schedule(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                        org_id: str = None):
        """
        Delete a Schedule

        Delete the designated Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Deleting a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param obj_id: Location or user from which to delete a schedule.
        :type obj_id: str
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
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id)
        params = org_id and {'orgId': org_id} or None
        self.delete(url, params=params)

    def event_details(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                      event_id: str, org_id: str = None) -> Event:
        """
        Get Details for a Schedule Event

        Retrieve Schedule Event details.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Retrieving schedule event details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param obj_id: Retrieve schedule event details for this location or user
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Retrieve schedule event details for schedule with the matching ID.
        :type schedule_id: str
        :param event_id: Retrieve the schedule event with the matching schedule event ID.
        :type event_id: str
        :param org_id: Retrieve schedule event details from this organization.
        :type org_id: str
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id=event_id)
        data = self.get(url, params=params)
        result = Event.parse_obj(data)
        return result

    def event_create(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                     event: Event, org_id: str = None) -> str:
        """
        Create a Schedule Event

        Create new Event for the given location or user Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Creating a schedule event requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param obj_id: Create the schedule for this location.
        :type obj_id: str
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
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id='')
        data = event.json(exclude={'event_id'})
        data = self.post(url, data=data, params=params)
        return data['id']

    def event_update(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                     event: Event, event_id: str = None, org_id: str = None) -> str:
        """
        Update a Schedule Event

        Update the designated Schedule Event.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Updating a schedule event requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        NOTE: The Schedule Event ID will change upon modification of the Schedule event name.

        :param obj_id: Location or user for which this schedule event exists.
        :type obj_id: str
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
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id=event_id)
        event_data = event.json(exclude={'event_id'})
        data = self.put(url, data=event_data, params=params)
        return data['id']

    def event_delete(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                     event_id: str, org_id: str = None):
        """
        Delete a Schedule Event

        Delete the designated Schedule Event.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Deleting a schedule event requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param obj_id: Location or user from which to delete a schedule.
        :type obj_id: str
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
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id=event_id)
        self.delete(url, params=params)

from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['GetScheduleEventObject', 'GetScheduleObject', 'GetScheduleObjectType', 'ListScheduleObject',
           'LocationCallSettingsSchedulesApi', 'ModifyScheduleEventListObject', 'ModifyScheduleEventObject',
           'RecurWeeklyObject', 'RecurYearlyByDateObject', 'RecurYearlyByDateObjectMonth', 'RecurYearlyByDayObject',
           'RecurYearlyByDayObjectDay', 'RecurYearlyByDayObjectWeek', 'RecurrenceObject']


class RecurWeeklyObject(ApiModel):
    #: Frequency of occurrence in weeks and select the day - Sunday.
    sunday: Optional[bool] = None
    #: Frequency of occurrence in weeks and select the day - Monday.
    monday: Optional[bool] = None
    #: Frequency of occurrence in weeks and select the day - Tuesday.
    tuesday: Optional[bool] = None
    #: Frequency of occurrence in weeks and select the day - Wednesday.
    wednesday: Optional[bool] = None
    #: Frequency of occurrence in weeks and select the day - Thursday.
    thursday: Optional[bool] = None
    #: Frequency of occurrence in weeks and select the day - Friday.
    friday: Optional[bool] = None
    #: Frequency of occurrence in weeks and select the day - Saturday.
    saturday: Optional[bool] = None


class RecurYearlyByDateObjectMonth(str, Enum):
    january = 'JANUARY'
    february = 'FEBRUARY'
    march = 'MARCH'
    april = 'APRIL'
    may = 'MAY'
    june = 'JUNE'
    july = 'JULY'
    august = 'AUGUST'
    september = 'SEPTEMBER'
    october = 'OCTOBER'
    november = 'NOVEMBER'
    december = 'DECEMBER'


class RecurYearlyByDateObject(ApiModel):
    #: Schedule the event on a specific day of the month.
    day_of_month: Optional[int] = None
    #: Schedule the event on a specific month of the year.
    month: Optional[RecurYearlyByDateObjectMonth] = None


class RecurYearlyByDayObjectDay(str, Enum):
    sunday = 'SUNDAY'
    monday = 'MONDAY'
    tuesday = 'TUESDAY'
    wednesday = 'WEDNESDAY'
    thursday = 'THURSDAY'
    friday = 'FRIDAY'
    saturday = 'SATURDAY'


class RecurYearlyByDayObjectWeek(str, Enum):
    first = 'FIRST'
    second = 'SECOND'
    third = 'THIRD'
    fourth = 'FOURTH'
    last = 'LAST'


class RecurYearlyByDayObject(ApiModel):
    #: Schedule the event on a specific day.
    day: Optional[RecurYearlyByDayObjectDay] = None
    #: Schedule the event on a specific week.
    week: Optional[RecurYearlyByDayObjectWeek] = None
    #: Schedule the event on a specific month.
    month: Optional[RecurYearlyByDateObjectMonth] = None


class RecurrenceObject(ApiModel):
    #: Flag to indicate if event will recur forever.
    recur_for_ever: Optional[bool] = None
    #: End date of recurrence.
    recur_end_date: Optional[datetime] = None
    #: Weekly recurrence definition.
    recur_weekly: Optional[RecurWeeklyObject] = None
    #: Recurrence definition yearly by date.
    recur_yearly_by_date: Optional[RecurYearlyByDateObject] = None
    #: Recurrence definition yearly by day.
    recur_yearly_by_day: Optional[RecurYearlyByDayObject] = None


class GetScheduleEventObject(ApiModel):
    #: A unique identifier for the schedule event.
    id: Optional[str] = None
    #: Name for the event.
    name: Optional[str] = None
    #: Start Date of Event.
    start_date: Optional[datetime] = None
    #: End Date of Event.
    end_date: Optional[datetime] = None
    #: Start time of event.
    start_time: Optional[str] = None
    #: End time of event.
    end_time: Optional[str] = None
    #: An indication of whether given event is an all-day event or not.
    all_day_enabled: Optional[bool] = None
    #: Recurrence definition.
    recurrence: Optional[RecurrenceObject] = None


class GetScheduleObjectType(str, Enum):
    #: Business hours schedule type.
    business_hours = 'businessHours'
    #: Holidays schedule type.
    holidays = 'holidays'


class GetScheduleObject(ApiModel):
    #: A unique identifier for the schedule.
    id: Optional[str] = None
    #: Unique name for the schedule.
    name: Optional[str] = None
    #: Type of the schedule.
    type: Optional[GetScheduleObjectType] = None
    #: List of schedule events.
    events: Optional[list[GetScheduleEventObject]] = None


class ListScheduleObject(ApiModel):
    #: A unique identifier for the schedule.
    id: Optional[str] = None
    #: Unique name for the schedule.
    name: Optional[str] = None
    #: Type of the schedule.
    type: Optional[GetScheduleObjectType] = None
    #: Name of location for schedule.
    location_name: Optional[str] = None
    #: ID of the location for the schedule.
    location_id: Optional[str] = None


class ModifyScheduleEventListObject(ApiModel):
    #: Current name for the event.
    name: Optional[str] = None
    #: New name for the event.
    new_name: Optional[str] = None
    #: Start date of event.
    start_date: Optional[datetime] = None
    #: End date of event.
    end_date: Optional[datetime] = None
    #: Start time of event. Mandatory if the event is not all day.
    start_time: Optional[str] = None
    #: End time of event. Mandatory if the event is not all day.
    end_time: Optional[str] = None
    #: An indication of whether given event is an all-day event or not. Mandatory if the `startTime` and `endTime` are
    #: not defined.
    all_day_enabled: Optional[bool] = None
    #: Recurrence definition.
    recurrence: Optional[RecurrenceObject] = None


class ModifyScheduleEventObject(ApiModel):
    #: Name for the event.
    name: Optional[str] = None
    #: Start date of event.
    start_date: Optional[datetime] = None
    #: End date of event.
    end_date: Optional[datetime] = None
    #: Start time of event. Mandatory if the event is not all day.
    start_time: Optional[str] = None
    #: End time of event. Mandatory if the event is not all day.
    end_time: Optional[str] = None
    #: An indication of whether given event is an all-day event or not. Mandatory if the `startTime` and `endTime` are
    #: not defined.
    all_day_enabled: Optional[bool] = None
    #: Recurrence definition.
    recurrence: Optional[RecurrenceObject] = None


class LocationCallSettingsSchedulesApi(ApiChild, base='telephony/config/locations'):
    """
    Location Call Settings:  Schedules
    
    Location Call Settings: Schedules supports reading and writing of Webex
    Calling Location Schedule and Event settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_schedules(self, location_id: str, name: str = None, type: GetScheduleObjectType = None,
                                   org_id: str = None, **params) -> Generator[ListScheduleObject, None, None]:
        """
        Read the List of Schedules

        List all schedules for the given location of the organization.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the list of schedules for this location.
        :type location_id: str
        :param name: Only return schedules with the matching name.
        :type name: str
        :param type: Type of the schedule.
        :type type: GetScheduleObjectType
        :param org_id: List schedules for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListScheduleObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if name is not None:
            params['name'] = name
        if type is not None:
            params['type'] = enum_str(type)
        url = self.ep(f'{location_id}/schedules')
        return self.session.follow_pagination(url=url, model=ListScheduleObject, item_key='schedules', params=params)

    def create_a_schedule(self, location_id: str, type: GetScheduleObjectType, name: str,
                          events: list[ModifyScheduleEventObject] = None, org_id: str = None) -> str:
        """
        Create a Schedule

        Create new Schedule for the given location.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Creating a schedule requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Create the schedule for this location.
        :type location_id: str
        :param type: Type of the schedule.
        :type type: GetScheduleObjectType
        :param name: Unique name for the schedule.
        :type name: str
        :param events: List of schedule events.
        :type events: list[ModifyScheduleEventObject]
        :param org_id: Create the schedule for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['type'] = enum_str(type)
        body['name'] = name
        if events is not None:
            body['events'] = TypeAdapter(list[ModifyScheduleEventObject]).dump_python(events, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{location_id}/schedules')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_schedule(self, location_id: str, type: GetScheduleObjectType, schedule_id: str, org_id: str = None):
        """
        Delete a Schedule

        Delete the designated Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Deleting a schedule requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Location from which to delete a schedule.
        :type location_id: str
        :param type: Type of the schedule.
        :type type: GetScheduleObjectType
        :param schedule_id: Delete the schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Delete the schedule from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/schedules/{type}/{schedule_id}')
        super().delete(url, params=params)

    def get_details_for_a_schedule(self, location_id: str, type: GetScheduleObjectType, schedule_id: str,
                                   org_id: str = None) -> GetScheduleObject:
        """
        Get Details for a Schedule

        Retrieve Schedule details.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Retrieving schedule details requires a full or read-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve schedule details in this location.
        :type location_id: str
        :param type: Type of the schedule.
        :type type: GetScheduleObjectType
        :param schedule_id: Retrieve the schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Retrieve schedule details from this organization.
        :type org_id: str
        :rtype: :class:`GetScheduleObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/schedules/{type}/{schedule_id}')
        data = super().get(url, params=params)
        r = GetScheduleObject.model_validate(data)
        return r

    def update_a_schedule(self, location_id: str, type: GetScheduleObjectType, schedule_id: str, name: str,
                          events: list[ModifyScheduleEventListObject] = None, org_id: str = None) -> str:
        """
        Update a Schedule

        Update the designated schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Updating a schedule requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **NOTE**: The Schedule ID will change upon modification of the Schedule name.

        :param location_id: Location in which this schedule exists.
        :type location_id: str
        :param type: Type of schedule.
        :type type: GetScheduleObjectType
        :param schedule_id: Update schedule with the matching ID.
        :type schedule_id: str
        :param name: Unique name for the schedule.
        :type name: str
        :param events: List of schedule events.
        :type events: list[ModifyScheduleEventListObject]
        :param org_id: Update schedule from this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        if events is not None:
            body['events'] = TypeAdapter(list[ModifyScheduleEventListObject]).dump_python(events, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{location_id}/schedules/{type}/{schedule_id}')
        data = super().put(url, params=params, json=body)
        r = data['id']
        return r

    def create_a_schedule_event(self, location_id: str, type: GetScheduleObjectType, schedule_id: str, name: str,
                                start_date: Union[str, datetime], end_date: Union[str, datetime],
                                start_time: str = None, end_time: str = None, all_day_enabled: bool = None,
                                recurrence: RecurrenceObject = None, org_id: str = None) -> str:
        """
        Create a Schedule Event

        Create new Event for the given location Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Creating a schedule event requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Create the schedule for this location.
        :type location_id: str
        :param type: Type of schedule.
        :type type: GetScheduleObjectType
        :param schedule_id: Create event for a given schedule ID.
        :type schedule_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start Date of Event.
        :type start_date: Union[str, datetime]
        :param end_date: End Date of Event.
        :type end_date: Union[str, datetime]
        :param start_time: Start time of event. Mandatory if the event is not all day.
        :type start_time: str
        :param end_time: End time of event. Mandatory if the event is not all day.
        :type end_time: str
        :param all_day_enabled: An indication of whether given event is an all-day event or not. Mandatory if the
            `startTime` and `endTime` are not defined.
        :type all_day_enabled: bool
        :param recurrence: Recurrence definition.
        :type recurrence: RecurrenceObject
        :param org_id: Create the schedule for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['startDate'] = start_date
        body['endDate'] = end_date
        if start_time is not None:
            body['startTime'] = start_time
        if end_time is not None:
            body['endTime'] = end_time
        if all_day_enabled is not None:
            body['allDayEnabled'] = all_day_enabled
        if recurrence is not None:
            body['recurrence'] = recurrence.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{location_id}/schedules/{type}/{schedule_id}/events')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_schedule_event(self, location_id: str, type: GetScheduleObjectType, schedule_id: str, event_id: str,
                                org_id: str = None):
        """
        Delete a Schedule Event

        Delete the designated Schedule Event.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Deleting a schedule event requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Location from which to delete a schedule.
        :type location_id: str
        :param type: Type of schedule.
        :type type: GetScheduleObjectType
        :param schedule_id: Delete the schedule with the matching ID.
        :type schedule_id: str
        :param event_id: Delete the schedule event with the matching schedule event ID.
        :type event_id: str
        :param org_id: Delete the schedule from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/schedules/{type}/{schedule_id}/events/{event_id}')
        super().delete(url, params=params)

    def get_details_for_a_schedule_event(self, location_id: str, type: GetScheduleObjectType, schedule_id: str,
                                         event_id: str, org_id: str = None) -> GetScheduleEventObject:
        """
        Get Details for a Schedule Event

        Retrieve Schedule Event details.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Retrieving a schedule event's details requires a full or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve schedule event details in this location.
        :type location_id: str
        :param type: Type of schedule.
        :type type: GetScheduleObjectType
        :param schedule_id: Retrieve the schedule event with the matching schedule ID.
        :type schedule_id: str
        :param event_id: Retrieve the schedule event with the matching schedule event ID.
        :type event_id: str
        :param org_id: Retrieve schedule event details from this organization.
        :type org_id: str
        :rtype: :class:`GetScheduleEventObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/schedules/{type}/{schedule_id}/events/{event_id}')
        data = super().get(url, params=params)
        r = GetScheduleEventObject.model_validate(data)
        return r

    def update_a_schedule_event(self, location_id: str, type: str, schedule_id: str, event_id: str, name: str,
                                start_date: Union[str, datetime], end_date: Union[str, datetime],
                                start_time: str = None, end_time: str = None, all_day_enabled: bool = None,
                                recurrence: RecurrenceObject = None, org_id: str = None) -> str:
        """
        Update a Schedule Event

        Update the designated Schedule Event.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Updating a schedule event requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **NOTE**: The schedule event ID will change upon modification of the schedule event name.

        :param location_id: Location in which this schedule event exists.
        :type location_id: str
        :param type: Type of schedule.

        + `businessHours` - Business hours schedule type.

        + `holidays` - Holidays schedule type.
        :type type: str
        :param schedule_id: Update schedule event with the matching schedule ID.
        :type schedule_id: str
        :param event_id: Update the schedule event with the matching schedule event ID.
        :type event_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start date of event.
        :type start_date: Union[str, datetime]
        :param end_date: End date of event.
        :type end_date: Union[str, datetime]
        :param start_time: Start time of event. Mandatory if the event is not all day.
        :type start_time: str
        :param end_time: End time of event. Mandatory if the event is not all day.
        :type end_time: str
        :param all_day_enabled: An indication of whether given event is an all-day event or not. Mandatory if the
            `startTime` and `endTime` are not defined.
        :type all_day_enabled: bool
        :param recurrence: Recurrence definition.
        :type recurrence: RecurrenceObject
        :param org_id: Update schedule from this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['startDate'] = start_date
        body['endDate'] = end_date
        if start_time is not None:
            body['startTime'] = start_time
        if end_time is not None:
            body['endTime'] = end_time
        if all_day_enabled is not None:
            body['allDayEnabled'] = all_day_enabled
        if recurrence is not None:
            body['recurrence'] = recurrence.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{location_id}/schedules/{type}/{schedule_id}/events/{event_id}')
        data = super().put(url, params=params, json=body)
        r = data['id']
        return r

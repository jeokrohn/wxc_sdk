from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetScheduleEventObject', 'GetScheduleObject', 'GetScheduleObjectType', 'ListScheduleObject', 'ModifyScheduleEventListObject', 'ModifyScheduleEventObject', 'ModifyScheduleObject', 'PostScheduleObject', 'RecurWeeklyObject', 'RecurYearlyByDateObject', 'RecurYearlyByDateObjectMonth', 'RecurYearlyByDayObject', 'RecurYearlyByDayObjectDay', 'RecurYearlyByDayObjectWeek', 'RecurrenceObject']


class RecurWeeklyObject(ApiModel):
    #: Frequency of occurrence in weeks and select the day - Sunday.
    #: example: True
    sunday: Optional[bool] = None
    #: Frequency of occurrence in weeks and select the day - Monday.
    #: example: True
    monday: Optional[bool] = None
    #: Frequency of occurrence in weeks and select the day - Tuesday.
    #: example: True
    tuesday: Optional[bool] = None
    #: Frequency of occurrence in weeks and select the day - Wednesday.
    #: example: True
    wednesday: Optional[bool] = None
    #: Frequency of occurrence in weeks and select the day - Thursday.
    #: example: True
    thursday: Optional[bool] = None
    #: Frequency of occurrence in weeks and select the day - Friday.
    #: example: True
    friday: Optional[bool] = None
    #: Frequency of occurrence in weeks and select the day - Saturday.
    #: example: True
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
    #: example: 1.0
    dayOfMonth: Optional[int] = None
    #: Schedule the event on a specific month of the year.
    #: example: JANUARY
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
    #: example: SUNDAY
    day: Optional[RecurYearlyByDayObjectDay] = None
    #: Schedule the event on a specific week.
    #: example: SECOND
    week: Optional[RecurYearlyByDayObjectWeek] = None
    #: Schedule the event on a specific month.
    #: example: JANUARY
    month: Optional[RecurYearlyByDateObjectMonth] = None


class RecurrenceObject(ApiModel):
    #: Flag to indicate if event will recur forever.
    recurForEver: Optional[bool] = None
    #: End date of recurrence.
    #: example: 2021-11-30
    recurEndDate: Optional[datetime] = None
    #: Weekly recurrence definition.
    recurWeekly: Optional[RecurWeeklyObject] = None
    #: Recurrence definition yearly by date.
    recurYearlyByDate: Optional[RecurYearlyByDateObject] = None
    #: Recurrence definition yearly by day.
    recurYearlyByDay: Optional[RecurYearlyByDayObject] = None


class GetScheduleEventObject(ApiModel):
    #: A unique identifier for the schedule event.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSEVEVUxFX0VWRU5UL1RXOXVaR0Y1VTJOb1pXUjFiR1U
    id: Optional[str] = None
    #: Name for the event.
    #: example: MondaySchedule
    name: Optional[str] = None
    #: Start Date of Event.
    #: example: 2021-11-01
    startDate: Optional[datetime] = None
    #: End Date of Event.
    #: example: 2021-11-30
    endDate: Optional[datetime] = None
    #: Start time of event.
    #: example: 12:20
    startTime: Optional[datetime] = None
    #: End time of event.
    #: example: 14:20
    endTime: Optional[datetime] = None
    #: An indication of whether given event is an all-day event or not.
    allDayEnabled: Optional[bool] = None
    #: Recurrence definition.
    recurrence: Optional[RecurrenceObject] = None


class GetScheduleObjectType(str, Enum):
    #: Business hours schedule type.
    businesshours = 'businessHours'
    #: Holidays schedule type.
    holidays = 'holidays'


class GetScheduleObject(ApiModel):
    #: A unique identifier for the schedule.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSEVEVUxFL1FWVlVUMEZVVkVWT1JFRk9WQzFDVlZOSlRrVlRVeTFJVDFWU1V3
    id: Optional[str] = None
    #: Unique name for the schedule.
    #: example: AUTOATTENDANT-BUSINESS-HOURS
    name: Optional[str] = None
    #: Type of the schedule.
    #: example: businessHours
    type: Optional[GetScheduleObjectType] = None
    #: List of schedule events.
    events: Optional[list[GetScheduleEventObject]] = None


class ListScheduleObject(ApiModel):
    #: A unique identifier for the schedule.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSEVEVUxFL1FWVlVUMEZVVkVWT1JFRk9WQzFDVlZOSlRrVlRVeTFJVDFWU1V3
    id: Optional[str] = None
    #: Unique name for the schedule.
    #: example: AUTOATTENDANT-BUSINESS-HOURS
    name: Optional[str] = None
    #: Type of the schedule.
    #: example: businessHours
    type: Optional[GetScheduleObjectType] = None
    #: Name of location for schedule.
    #: example: Alaska
    locationName: Optional[str] = None
    #: ID of the location for the schedule.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    locationId: Optional[str] = None


class ModifyScheduleEventListObject(ApiModel):
    #: Current name for the event.
    #: example: Schedule
    name: Optional[str] = None
    #: New name for the event.
    #: example: MondaySchedule
    newName: Optional[str] = None
    #: Start date of event.
    #: example: 2021-11-01
    startDate: Optional[datetime] = None
    #: End date of event.
    #: example: 2021-11-30
    endDate: Optional[datetime] = None
    #: Start time of event. Mandatory if the event is not all day.
    #: example: 12:20
    startTime: Optional[datetime] = None
    #: End time of event. Mandatory if the event is not all day.
    #: example: 14:20
    endTime: Optional[datetime] = None
    #: An indication of whether given event is an all-day event or not. Mandatory if the `startTime` and `endTime` are not defined.
    allDayEnabled: Optional[bool] = None
    #: Recurrence definition.
    recurrence: Optional[RecurrenceObject] = None


class ModifyScheduleEventObject(ApiModel):
    #: Name for the event.
    #: example: MondaySchedule
    name: Optional[str] = None
    #: Start date of event.
    #: example: 2021-11-01
    startDate: Optional[datetime] = None
    #: End date of event.
    #: example: 2021-11-30
    endDate: Optional[datetime] = None
    #: Start time of event. Mandatory if the event is not all day.
    #: example: 12:20
    startTime: Optional[datetime] = None
    #: End time of event. Mandatory if the event is not all day.
    #: example: 14:20
    endTime: Optional[datetime] = None
    #: An indication of whether given event is an all-day event or not. Mandatory if the `startTime` and `endTime` are not defined.
    allDayEnabled: Optional[bool] = None
    #: Recurrence definition.
    recurrence: Optional[RecurrenceObject] = None


class ModifyScheduleObject(ApiModel):
    #: Unique name for the schedule.
    #: example: AUTOATTENDANT-BUSINESS-HOURS
    name: Optional[str] = None
    #: List of schedule events.
    events: Optional[list[ModifyScheduleEventListObject]] = None


class PostScheduleObject(ApiModel):
    #: Type of the schedule.
    #: example: businessHours
    type: Optional[GetScheduleObjectType] = None
    #: Unique name for the schedule.
    #: example: AUTOATTENDANT-BUSINESS-HOURS
    name: Optional[str] = None
    #: List of schedule events.
    events: Optional[list[ModifyScheduleEventObject]] = None

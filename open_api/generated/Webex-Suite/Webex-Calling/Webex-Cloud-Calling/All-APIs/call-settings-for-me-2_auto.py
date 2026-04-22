import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AvailableHotelingHost', 'BlockContiguousSequences', 'BlockPreviousPasscodes', 'BlockRepeatedDigits',
           'CallNotifyGet', 'CallSettingsForMe22Api', 'GuestCallingNumber', 'HotelingGuestSettings',
           'LocationAssignedNumber', 'LocationAssignedNumberOwner', 'LocationAssignedNumberPhoneNumberType',
           'LocationAssignedNumberState', 'ModeManagementFeatureResponse', 'ModeManagementFeatureResponseModesItem',
           'ModeManagementFeatureResponseModesItemForwardTo',
           'ModeManagementFeatureResponseModesItemForwardToSelection', 'ModeManagementFeatureResponseModesItemLevel',
           'ModeManagementFeatureResponseModesItemType', 'ModeManagementFeaturesResponseFeaturesItem',
           'ModeManagementFeaturesResponseFeaturesItemExceptionType',
           'ModeManagementFeaturesResponseFeaturesItemLocation', 'ModeManagementFeaturesResponseFeaturesItemType',
           'NumberOwnerType', 'OperatingModeResponse', 'OperatingModeResponseDifferentHoursDaily',
           'OperatingModeResponseForwardTo', 'OperatingModeResponseHolidaysItem',
           'OperatingModeResponseHolidaysItemRecurrence', 'OperatingModeResponseSameHoursDaily',
           'OperatingModeResponseSameHoursDailyMondayToFriday', 'PasscodeLength', 'PersonalAssistantSettings',
           'PersonalAssistantSettingsAlerting', 'PersonalAssistantSettingsPresence', 'PriorityAlertCriteriaGet',
           'PriorityAlertCriteriaGetCallsFrom', 'PriorityAlertGet', 'PriorityAlertGetCriteriaObject',
           'PriorityAlertGetCriteriaObjectSource', 'RecurWeeklyObject', 'RecurYearlyByDateObject',
           'RecurYearlyByDateObjectMonth', 'RecurYearlyByDayObject', 'RecurYearlyByDayObjectDay',
           'RecurYearlyByDayObjectWeek', 'RecurrenceObject', 'ScheduleEventObject', 'ScheduleEventObjectRecurrence',
           'ScheduleEventObjectRecurrenceRecurWeekly', 'SelectiveAcceptCallCriteria',
           'SelectiveAcceptCallCriteriaGet', 'SelectiveAcceptCallSettingsGet', 'SelectiveCallForwardCriteriaGet',
           'SelectiveCallForwardCriteriaPatchCallsFrom', 'SelectiveForwardCallCriteria',
           'SelectiveForwardCallCriteriaSource', 'SelectiveForwardCallSettingsGet', 'SelectiveRejectCallCriteria',
           'SelectiveRejectCallCriteriaGet', 'SelectiveRejectCallCriteriaPostCallsFrom',
           'SelectiveRejectCallCriteriaSource', 'SelectiveRejectCallSettingsGet', 'SequentialRingCriteriaGet',
           'SequentialRingCriteriaSummary', 'SequentialRingNumber', 'SequentialRingSettingsGet',
           'SimultaneousRingCriteriaSummary', 'SimultaneousRingGet', 'SimultaneousRingNumber',
           'UserLocationScheduleEvent', 'UserLocationScheduleGetResponse', 'UserSchedule', 'UserScheduleEvent',
           'UserScheduleEventPatch', 'UserScheduleGetResponse', 'UserScheduleLevel', 'UserScheduleRecurrenceObject',
           'UserScheduleRecurrenceObjectRecurDaily', 'UserScheduleType', 'VoicemailRules']


class UserScheduleType(str, Enum):
    #: The schedule is for business hours.
    business_hours = 'businessHours'
    #: The schedule is for holidays.
    holidays = 'holidays'


class UserScheduleLevel(str, Enum):
    #: The schedule is at the user level.
    people = 'PEOPLE'
    #: The schedule is at the location level.
    location = 'LOCATION'


class UserSchedule(ApiModel):
    #: Unique identifier for the schedule.
    id: Optional[str] = None
    #: Name of the schedule.
    name: Optional[str] = None
    type: Optional[UserScheduleType] = None
    level: Optional[UserScheduleLevel] = None


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
    recur_weekly: Optional[RecurWeeklyObject] = None
    recur_yearly_by_date: Optional[RecurYearlyByDateObject] = None
    recur_yearly_by_day: Optional[RecurYearlyByDayObject] = None


class UserLocationScheduleEvent(ApiModel):
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
    recurrence: Optional[RecurrenceObject] = None


class UserLocationScheduleGetResponse(ApiModel):
    #: Unique identifier for the schedule.
    id: Optional[str] = None
    #: Name of the schedule.
    name: Optional[str] = None
    type: Optional[UserScheduleType] = None
    #: List of events in the schedule.
    events: Optional[list[UserLocationScheduleEvent]] = None


class UserScheduleRecurrenceObjectRecurDaily(ApiModel):
    #: Recurring interval in days. The number of days after the start when an event will repeat.  Repetitions cannot
    #: overlap.
    recur_interval: Optional[int] = None


class UserScheduleRecurrenceObject(ApiModel):
    #: Flag to indicate if event will recur forever.
    recur_for_ever: Optional[bool] = None
    #: End date of recurrence.
    recur_end_date: Optional[datetime] = None
    #: Number of occurrences after which the event will stop recurring.
    recur_end_occurrence: Optional[int] = None
    #: Specifies the number of days between the start of each recurrence and is not allowed with `recurWeekly`.
    recur_daily: Optional[UserScheduleRecurrenceObjectRecurDaily] = None
    recur_weekly: Optional[RecurWeeklyObject] = None


class UserScheduleEvent(ApiModel):
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
    recurrence: Optional[UserScheduleRecurrenceObject] = None


class UserScheduleGetResponse(ApiModel):
    #: Unique identifier for the schedule.
    id: Optional[str] = None
    #: Name of the schedule.
    name: Optional[str] = None
    type: Optional[UserScheduleType] = None
    #: List of events in the schedule.
    events: Optional[list[UserScheduleEvent]] = None


class UserScheduleEventPatch(ApiModel):
    #: Name for the event.
    name: Optional[str] = None
    #: New Name for the event.
    new_name: Optional[str] = None
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
    recurrence: Optional[UserScheduleRecurrenceObject] = None


class ScheduleEventObjectRecurrenceRecurWeekly(ApiModel):
    #: Specifies the number of weeks between the start of each recurrence.
    recur_interval: Optional[int] = None
    #: The Event occurs weekly on Sunday.
    sunday: Optional[bool] = None
    #: The Event occurs weekly on Monday.
    monday: Optional[bool] = None
    #: The Event occurs weekly on Tuesday.
    tuesday: Optional[bool] = None
    #: The Event occurs weekly on Wednesday.
    wednesday: Optional[bool] = None
    #: The Event occurs weekly on Thursday.
    thursday: Optional[bool] = None
    #: The Event occurs weekly on Friday.
    friday: Optional[bool] = None
    #: The Event occurs weekly on Saturday.
    saturday: Optional[bool] = None


class ScheduleEventObjectRecurrence(ApiModel):
    #: True if the event repeats forever. Requires either `recurDaily` or `recurWeekly` to be specified.
    recur_for_ever: Optional[bool] = None
    #: End date for the recurring event in the format of `YYYY-MM-DD`. Requires either `recurDaily` or `recurWeekly` to
    #: be specified.
    recur_end_date: Optional[datetime] = None
    #: End recurrence after the event has repeated the specified number of times. Requires either `recurDaily` or
    #: `recurWeekly` to be specified.
    recur_end_occurrence: Optional[int] = None
    #: Specifies the number of days between the start of each recurrence. Not allowed with `recurWeekly`.
    recur_daily: Optional[UserScheduleRecurrenceObjectRecurDaily] = None
    #: Specifies the event recur weekly on the designated days of the week. Not allowed with `recurDaily`.
    recur_weekly: Optional[ScheduleEventObjectRecurrenceRecurWeekly] = None


class ScheduleEventObject(ApiModel):
    #: Name for the event.
    name: Optional[str] = None
    #: Start date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is
    #: required if the `allDayEnabled` field is present.
    start_date: Optional[datetime] = None
    #: End date of the event, or first occurrence if repeating, in the format of `YYYY-MM-DD`.  This field is required
    #: if the `allDayEnabled` field is present.
    end_date: Optional[datetime] = None
    #: Start time of the event in the format of `HH:MM` (24 hours format).  This field is required if the
    #: `allDayEnabled` field is false or omitted.
    start_time: Optional[str] = None
    #: End time of the event in the format of `HH:MM` (24 hours format).  This field is required if the `allDayEnabled`
    #: field is false or omitted.
    end_time: Optional[str] = None
    #: An indication of whether given event is an all-day event or not. Mandatory if the `startTime` and `endTime` are
    #: not defined.
    all_day_enabled: Optional[bool] = None
    #: Recurrence scheme for an event.
    recurrence: Optional[ScheduleEventObjectRecurrence] = None


class PriorityAlertGetCriteriaObjectSource(str, Enum):
    #: User wants to be notified for calls from Any Phone Number.
    all_numbers = 'ALL_NUMBERS'
    #: User wants to be notified for calls from Select Phone Numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'


class PriorityAlertGetCriteriaObject(ApiModel):
    #: Unique identifier for the priority alert criterion.
    id: Optional[str] = None
    #: Name of the schedule associated with the criteria.
    schedule_name: Optional[str] = None
    #: Determines whether priority alerting is applied for calls matching this criteria. If `true`, priority alerting
    #: is applied. If `false`, this criteria acts as a 'Don't Alert' rule, preventing priority alerting. Criteria with
    #: `notificationEnabled` set to `false` (Don't Alert) take precedence over criteria with `notificationEnabled` set
    #: to `true` (Alert).
    notification_enabled: Optional[bool] = None
    #: Type of the source.
    source: Optional[PriorityAlertGetCriteriaObjectSource] = None


class PriorityAlertGet(ApiModel):
    #: Indicates whether the priority alert feature is enabled for the user.
    enabled: Optional[bool] = None
    #: List of Priority Alert Criteria configured by the user.
    criteria: Optional[list[PriorityAlertGetCriteriaObject]] = None


class PriorityAlertCriteriaGetCallsFrom(str, Enum):
    #: The criteria applies to any phone number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: The criteria applies to selected phone numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'


class PriorityAlertCriteriaGet(ApiModel):
    #: Unique identifier for the priority alert criteria.
    id: Optional[str] = None
    #: Name of the schedule associated with the criteria.
    schedule_name: Optional[str] = None
    #: Type of the schedule.
    schedule_type: Optional[UserScheduleType] = None
    schedule_level: Optional[UserScheduleLevel] = None
    #: Specifies the type of callsFrom, categorizing incoming data based on callsFrom types or numbers that match the
    #: current criteria.
    calls_from: Optional[PriorityAlertCriteriaGetCallsFrom] = None
    #: Indicates whether anonymous callers are included in this criteria.
    anonymous_callers_enabled: Optional[bool] = None
    #: Indicates whether unavailable callers are included in this criteria.
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers that this criteria applies to.
    phone_numbers: Optional[list[str]] = None
    #: Determines whether priority alerting is applied for calls matching this criteria. If `true`, priority alerting
    #: is applied. If `false`, this criteria acts as a 'Don't Alert' rule, preventing priority alerting. Criteria with
    #: `notificationEnabled` set to `false` (Don't Alert) take precedence over criteria with `notificationEnabled` set
    #: to `true` (Alert).
    notification_enabled: Optional[bool] = None


class CallNotifyGet(ApiModel):
    #: Indicates whether the call notify feature is enabled for the user.
    enabled: Optional[bool] = None
    #: Email Address to which call notifications to be received.
    email_address: Optional[str] = None
    #: List of Call Notify Criteria configured by the user.
    criteria: Optional[list[PriorityAlertGetCriteriaObject]] = None


class SelectiveAcceptCallCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective accept is in effect.
    schedule_name: Optional[str] = None
    #: Type of the schedule.
    schedule_type: Optional[UserScheduleType] = None
    schedule_level: Optional[UserScheduleLevel] = None
    #: Specifies the type of callsFrom, categorizing incoming data based on callsFrom types or numbers that match the
    #: current criteria.
    calls_from: Optional[PriorityAlertCriteriaGetCallsFrom] = None
    #: When `true`, enables selective accept to calls from anonymous callers.
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, enables selective accept to calls if the callers are unavailable.
    unavailable_callers_enabled: Optional[bool] = None
    #: the list of phone numbers that will checked against incoming calls for a match.
    phone_numbers: Optional[list[str]] = None
    #: Determines whether selective call accept is applied for calls matching this criteria. If `true`, selective call
    #: accept is applied. If `false`, this criteria acts as a 'Don't Accept' rule, preventing call acceptance.
    #: Criteria with `notificationEnabled` set to `false` (Don't Accept) take precedence over criteria with
    #: `acceptEnabled` set to `true` (Accept).
    accept_enabled: Optional[bool] = None


class SelectiveAcceptCallCriteria(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective call accept is in effect.
    schedule_name: Optional[str] = None
    #: Type of the source.
    source: Optional[PriorityAlertGetCriteriaObjectSource] = None
    #: Determines whether selective call accept is applied for calls matching this criteria. If `true`, selective call
    #: accept is applied. If `false`, this criteria acts as a 'Don't Accept' rule, preventing call acceptance.
    #: Criteria with `notificationEnabled` set to `false` (Don't Accept) take precedence over criteria with
    #: `acceptEnabled` set to `true` (Accept).
    accept_enabled: Optional[bool] = None


class SelectiveAcceptCallSettingsGet(ApiModel):
    #: `true` if the Selective Accept feature is enabled.
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective accept is in effect.
    criteria: Optional[list[SelectiveAcceptCallCriteria]] = None


class LocationAssignedNumberState(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class LocationAssignedNumberPhoneNumberType(str, Enum):
    #: A direct phone number.
    primary = 'PRIMARY'
    #: An alternate phone number.
    alternate = 'ALTERNATE'
    #: A FAX number.
    fax = 'FAX'


class NumberOwnerType(str, Enum):
    #: phone number/extension owner is a workspace.
    place = 'PLACE'
    #: phone number/extension owner is a person.
    people = 'PEOPLE'
    #: phone number/extension owner is a Virtual Profile.
    virtual_line = 'VIRTUAL_LINE'
    #: phone number/extension owner is an auto-attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: phone number/extension owner is a call queue.
    call_queue = 'CALL_QUEUE'
    #: phone number/extension owner is a group paging.
    group_paging = 'GROUP_PAGING'
    #: phone number/extension owner is a hunt group.
    hunt_group = 'HUNT_GROUP'
    #: phone number/extension owner is a voice messaging.
    voice_messaging = 'VOICE_MESSAGING'
    #: phone number/extension owner is a Single Number Reach.
    office_anywhere = 'OFFICE_ANYWHERE'
    #: phone number/extension owner is a Contact Center link.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: phone number/extension owner is a Contact Center adapter.
    contact_center_adapter = 'CONTACT_CENTER_ADAPTER'
    #: phone number/extension owner is a route list.
    route_list = 'ROUTE_LIST'
    #: phone number/extension owner is a voicemail group.
    voicemail_group = 'VOICEMAIL_GROUP'
    collaborate_bridge = 'COLLABORATE_BRIDGE'


class LocationAssignedNumberOwner(ApiModel):
    type: Optional[NumberOwnerType] = None
    #: First name of the phone number/extension owner. This field is present only for type `PEOPLE` and `VIRTUAL_LINE`.
    first_name: Optional[str] = None
    #: Last name of the phone number/extension owner. This field is present only for type `PEOPLE` and `VIRTUAL_LINE`.
    last_name: Optional[str] = None
    #: Display Name of the phone number/extension owner.
    display_name: Optional[str] = None


class LocationAssignedNumber(ApiModel):
    #: The phone number in E.164 format.
    phone_number: Optional[str] = None
    #: The extension.
    extension: Optional[str] = None
    state: Optional[LocationAssignedNumberState] = None
    phone_number_type: Optional[LocationAssignedNumberPhoneNumberType] = None
    #: Indicate if the number is toll free.
    toll_free_number: Optional[bool] = None
    #: The owner details.
    owner: Optional[LocationAssignedNumberOwner] = None


class SelectiveCallForwardCriteriaPatchCallsFrom(str, Enum):
    #: The criteria applies to any phone number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: The criteria applies to selected phone numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: The criteria applies to any internal number.
    any_internal = 'ANY_INTERNAL'
    #: The criteria applies to any external number.
    any_external = 'ANY_EXTERNAL'


class SelectiveCallForwardCriteriaGet(ApiModel):
    #: Unique identifier for the priority alert criteria.
    id: Optional[str] = None
    #: The phone number to which calls are forwarded when the criteria conditions are met.
    forward_to_phone_number: Optional[str] = None
    #: Indicates whether calls that meet the criteria are forwarded to the destination phone number's voicemail.
    destination_voicemail_enabled: Optional[bool] = None
    #: Name of the schedule associated with the criteria.
    schedule_name: Optional[str] = None
    #: Type of the schedule.
    schedule_type: Optional[UserScheduleType] = None
    schedule_level: Optional[UserScheduleLevel] = None
    #: Specifies the type of callsFrom, categorizing incoming data based on callsFrom types or numbers that match the
    #: current criteria.
    calls_from: Optional[SelectiveCallForwardCriteriaPatchCallsFrom] = None
    #: Indicates whether anonymous callers are included in this criteria.
    anonymous_callers_enabled: Optional[bool] = None
    #: Indicates whether unavailable callers are included in this criteria.
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers that this criteria applies to.
    phone_numbers: Optional[list[str]] = None
    #: Determines whether selective call forwarding is applied for calls matching this criteria. If `true`, the
    #: selective forwarding is applied. If `false`, this criteria acts as a 'Don't Forward' rule, preventing
    #: selectively forwarding of the calls. Criteria with `forwardEnabled` set to `false` (Don't Forward) take
    #: precedence over criteria with `forwardEnabled` set to `true` (Forward).
    forward_enabled: Optional[bool] = None


class SelectiveForwardCallCriteriaSource(str, Enum):
    #: Select to forward calls from Any Phone Number.
    all_numbers = 'ALL_NUMBERS'
    #: Select to forward calls from Select Phone Numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'
    #: Select to forward calls from Any Internal Number.
    any_internal = 'ANY_INTERNAL'
    #: Select to forward calls from Any External Number.
    any_external = 'ANY_EXTERNAL'


class SelectiveForwardCallCriteria(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the selective call forward is in effect.
    schedule_name: Optional[str] = None
    #: Specifies the type of source, categorizing incoming data based on source types or numbers that match the current
    #: criteria.
    source: Optional[SelectiveForwardCallCriteriaSource] = None
    #: Determines whether selective call forwarding is applied for calls matching this criteria. If `true`, the
    #: selective forwarding is applied. If `false`, this criteria acts as a 'Don't Forward' rule, preventing
    #: selectively forwarding of the calls. Criteria with `forwardEnabled` set to `false` (Don't Forward) take
    #: precedence over criteria with `forwardEnabled` set to `true` (Forward).
    forward_enabled: Optional[bool] = None


class SelectiveForwardCallSettingsGet(ApiModel):
    #: `true` if the Selective Forward feature is enabled.
    enabled: Optional[bool] = None
    #: The phone number to which calls are forwarded by default when the criteria conditions are met.
    default_phone_number_to_forward: Optional[str] = None
    #: If `true`, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Indicates whether calls that meet the criteria are forwarded to the destination phone number's voicemail.
    destination_voicemail_enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective accept is in effect.
    criteria: Optional[list[SelectiveForwardCallCriteria]] = None


class SelectiveRejectCallCriteriaPostCallsFrom(str, Enum):
    #: The criteria applies to any phone number.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: The criteria applies to selected phone numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'
    #: The criteria applies to calls that have been forwarded.
    forwarded = 'FORWARDED'


class SelectiveRejectCallCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the schedule associated with the criteria.
    schedule_name: Optional[str] = None
    #: Type of the schedule.
    schedule_type: Optional[UserScheduleType] = None
    schedule_level: Optional[UserScheduleLevel] = None
    #: Specifies the type of calling numbers the criteria applies to, categorizing incoming data based on callsFrom
    #: types or numbers that match the current criteria.
    calls_from: Optional[SelectiveRejectCallCriteriaPostCallsFrom] = None
    #: When `true`, means this criteria applies for anonymous callers.
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, means this criteria applies for unavailable callers.
    unavailable_callers_enabled: Optional[bool] = None
    #: The list of phone numbers that will be checked against incoming calls for a match.
    phone_numbers: Optional[list[str]] = None
    #: Determines whether selective call reject is applied for calls matching this criteria. If `true`, selective call
    #: reject is applied. Criteria with rejectEnabled set to false have precedence over criteria with rejectEnabled
    #: set to true.
    reject_enabled: Optional[bool] = None


class SelectiveRejectCallCriteriaSource(str, Enum):
    #: Select to reject calls from Any Phone Number.
    all_numbers = 'ALL_NUMBERS'
    #: Select to reject calls from Select Phone Numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'
    #: Select to reject calls that have been forwarded.
    forwarded = 'FORWARDED'


class SelectiveRejectCallCriteria(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the schedule associated with the criteria.
    schedule_name: Optional[str] = None
    #: Type of the source.
    source: Optional[SelectiveRejectCallCriteriaSource] = None
    #: Determines whether selective call reject is applied for calls matching this criteria. If `true`, selective call
    #: reject is applied. If `false`, this criteria acts as a 'Don't Reject' rule, preventing call rejections.
    #: Criteria with rejectEnabled set to false have precedence over criteria with rejectEnabled set to true.
    reject_enabled: Optional[bool] = None


class SelectiveRejectCallSettingsGet(ApiModel):
    #: `true` if the selective reject feature is enabled.
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective reject is in effect.
    criteria: Optional[list[SelectiveRejectCallCriteria]] = None


class SequentialRingNumber(ApiModel):
    #: Phone number to ring sequentially.
    phone_number: Optional[str] = None
    #: When `true`, the person answering must press any key to accept the call.
    answer_confirmation_required_enabled: Optional[bool] = None
    #: Number of rings for this phone number. Minimum: 2, Maximum: 20.
    number_of_rings: Optional[int] = None


class SequentialRingCriteriaSummary(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the schedule which determines when sequential ring is in effect.
    schedule_name: Optional[str] = None
    #: Type of the source.
    source: Optional[PriorityAlertGetCriteriaObjectSource] = None
    #: Determines whether sequential ring is applied for calls matching this criteria. If `true`, sequential ring is
    #: applied. If `false`, this criteria acts as a 'Don't Ring' rule. Criteria with ringEnabled set to false have
    #: precedence over criteria with ringEnabled set to true.
    ring_enabled: Optional[bool] = None


class SequentialRingSettingsGet(ApiModel):
    #: `true` if the sequential ring feature is enabled.
    enabled: Optional[bool] = None
    #: When `true`, the user's own devices ring before sequential ring numbers.
    ring_base_location_first_enabled: Optional[bool] = None
    #: Number of rings for the user's own devices. Minimum: 2, Maximum: 20.
    base_location_number_of_rings: Optional[int] = None
    #: When `true`, sequential ring continues even when the user is unavailable. It controls if we allow trying the
    #: sequential ring numbers when either a service for the user such as Do Not Disturb or Call Waiting sends the
    #: call to busy processing, or ringBaseLocationFirstEnabled is true but all the user's devices are unreachable.
    continue_if_base_location_is_busy_enabled: Optional[bool] = None
    #: When `true`, the caller is provided the option to press the # key to end the sequential ring service and send
    #: the call to no answer handling such as voicemail.
    calls_to_voicemail_enabled: Optional[bool] = None
    #: List of phone numbers to ring sequentially.
    phone_numbers: Optional[list[SequentialRingNumber]] = None
    #: List of criteria specifying conditions when sequential ring is in effect.
    criteria: Optional[list[SequentialRingCriteriaSummary]] = None


class SequentialRingCriteriaGet(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the schedule which determines when sequential ring is in effect.
    schedule_name: Optional[str] = None
    #: Type of the schedule.
    schedule_type: Optional[UserScheduleType] = None
    schedule_level: Optional[UserScheduleLevel] = None
    #: Specifies the type of calling numbers the criteria applies to.
    calls_from: Optional[PriorityAlertCriteriaGetCallsFrom] = None
    #: When `true`, means this criteria applies for anonymous callers. If SELECT_PHONE_NUMBERS has been selected.
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true`, means this criteria applies for unavailable callers.
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers that will be checked against incoming calls for a match. Only when SELECT_PHONE_NUMBERS
    #: has been chosen for the criteria.
    phone_numbers: Optional[list[str]] = None
    #: Determines whether sequential ring is applied for calls matching this criteria. If `true`, sequential ring is
    #: applied. If `false`, this criteria acts as a 'Don't Ring' rule. Criteria with ringEnabled set to false have
    #: precedence over criteria with ringEnabled set to true.
    ring_enabled: Optional[bool] = None


class ModeManagementFeaturesResponseFeaturesItemType(str, Enum):
    #: Auto Attendant feature.
    auto_attendant = 'AUTO_ATTENDANT'
    #: Call Queue feature (includes customer assist queues).
    call_queue = 'CALL_QUEUE'
    #: Hunt Group feature.
    hunt_group = 'HUNT_GROUP'


class ModeManagementFeaturesResponseFeaturesItemLocation(ApiModel):
    #: Unique identifier for the location.
    id: Optional[str] = None
    #: Display name of the location.
    name: Optional[str] = None


class ModeManagementFeaturesResponseFeaturesItemExceptionType(str, Enum):
    #: Automatic switchback with early start.
    automatic_switch_back_early_start = 'AUTOMATIC_SWITCH_BACK_EARLY_START'
    #: Automatic switchback with extension.
    automatic_switch_back_extension = 'AUTOMATIC_SWITCH_BACK_EXTENSION'
    #: Manual switchback required.
    manual_switch_back = 'MANUAL_SWITCH_BACK'
    #: Standard automatic switchback.
    automatic_switch_back_standard = 'AUTOMATIC_SWITCH_BACK_STANDARD'


class ModeManagementFeaturesResponseFeaturesItem(ApiModel):
    #: Unique identifier for the auto attendant, call queue, or hunt group.
    id: Optional[str] = None
    #: Display name of the auto attendant, call queue, or hunt group.
    name: Optional[str] = None
    type: Optional[ModeManagementFeaturesResponseFeaturesItemType] = None
    #: Phone number of the feature
    phone_number: Optional[str] = None
    #: Extension of the feature
    extension: Optional[str] = None
    #: Whether mode based forwarding is enabled for the feature
    mode_based_forwarding_enabled: Optional[bool] = None
    #: Location information for the feature
    location: Optional[ModeManagementFeaturesResponseFeaturesItemLocation] = None
    #: Current forward destination
    forward_destination: Optional[str] = None
    #: Name of the current operating mode
    current_operating_mode_name: Optional[str] = None
    #: ID of the current operating mode
    current_operating_mode_id: Optional[str] = None
    #: Type of exception indicating how the feature will switch back from the current mode. This field is not present
    #: when the feature is in normal operation.
    exception_type: Optional[ModeManagementFeaturesResponseFeaturesItemExceptionType] = None


class ModeManagementFeatureResponseModesItemType(str, Enum):
    #: No schedule defined.
    none_ = 'NONE'
    #: Same hours for weekdays and weekends.
    same_hours_daily = 'SAME_HOURS_DAILY'
    #: Different hours for each day.
    different_hours_daily = 'DIFFERENT_HOURS_DAILY'
    #: Holiday-based schedule.
    holiday = 'HOLIDAY'


class ModeManagementFeatureResponseModesItemLevel(str, Enum):
    #: Organization level mode.
    organization = 'ORGANIZATION'
    #: Location level mode.
    location = 'LOCATION'


class ModeManagementFeatureResponseModesItemForwardToSelection(str, Enum):
    #: Do not forward calls.
    do_not_forward = 'DO_NOT_FORWARD'
    #: Forward to a specified number.
    forward_to_specified_number = 'FORWARD_TO_SPECIFIED_NUMBER'
    #: Use the mode's default forwarding setting (which may be to forward or not forward).
    forward_to_default_number = 'FORWARD_TO_DEFAULT_NUMBER'


class ModeManagementFeatureResponseModesItemForwardTo(ApiModel):
    selection: Optional[ModeManagementFeatureResponseModesItemForwardToSelection] = None
    #: Phone number to forward to when selection is FORWARD_TO_SPECIFIED_NUMBER.
    phone_number: Optional[str] = None
    #: Whether to send to voicemail when selection is FORWARD_TO_SPECIFIED_NUMBER.
    send_to_voicemail_enabled: Optional[bool] = None
    #: Default phone number when selection is FORWARD_TO_DEFAULT_NUMBER. This field is not present if the mode's
    #: default is to not forward.
    default_phone_number: Optional[str] = None
    #: Whether default is to send to voicemail
    default_send_to_voicemail_enabled: Optional[bool] = None


class ModeManagementFeatureResponseModesItem(ApiModel):
    #: Unique identifier for the operating mode.
    id: Optional[str] = None
    #: Display name of the operating mode.
    name: Optional[str] = None
    type: Optional[ModeManagementFeatureResponseModesItemType] = None
    level: Optional[ModeManagementFeatureResponseModesItemLevel] = None
    #: Whether this mode is enabled for normal operation.
    normal_operation_enabled: Optional[bool] = None
    #: Forwarding configuration for this mode
    forward_to: Optional[ModeManagementFeatureResponseModesItemForwardTo] = None


class ModeManagementFeatureResponse(ApiModel):
    #: Whether mode based forwarding is enabled for the feature
    mode_based_forwarding_enabled: Optional[bool] = None
    #: Timezone for the feature
    timezone: Optional[str] = None
    #: Phone number of the feature
    phone_number: Optional[str] = None
    #: Extension of the feature
    extension: Optional[str] = None
    #: Unique identifier for the current operating mode.
    current_operating_mode_id: Optional[str] = None
    #: The current operating mode's end time in 12-hour format showing hour and minute only (no date information). This
    #: field's presence and meaning depends on the operational state:
    #: * Present during normal operation with the time at which the next mode change will occur.
    #: * Not present for Manual Switch Back exceptions.
    #: * For Automatic Switch Back (Early Start) exceptions it is when the exception ends and the feature automatically
    #: reverts to normal operation which is the mode's configured start time.
    #: * For Automatic Switch Back (Extension) exceptions it is when the exception ends and the feature automatically
    #: reverts to normal operation which is the mode's configured end time when the exception started plus the
    #: extension time.
    #: * For Automatic Switch Back (Standard) exceptions it is when the exception ends and the feature automatically
    #: reverts to normal operation which is the mode's configured end time.
    current_operating_mode_end_time: Optional[str] = None
    #: Forward destination for current operating mode
    current_operating_mode_forward_destination: Optional[str] = None
    #: Type of exception indicating how the feature will switch back from the current mode. This field is not present
    #: when the feature is in normal operation.
    exception_type: Optional[ModeManagementFeaturesResponseFeaturesItemExceptionType] = None
    #: Array of operating modes configured for this feature
    modes: Optional[list[ModeManagementFeatureResponseModesItem]] = None


class OperatingModeResponseSameHoursDailyMondayToFriday(ApiModel):
    #: Whether schedule is enabled for Monday to Friday
    enabled: Optional[bool] = None
    #: Whether all day is enabled
    all_day_enabled: Optional[bool] = None
    #: Start time in HH:mm format. This field is not present when allDayEnabled is true.
    start_time: Optional[str] = None
    #: End time in HH:mm format. This field is not present when allDayEnabled is true.
    end_time: Optional[str] = None


class OperatingModeResponseSameHoursDaily(ApiModel):
    monday_to_friday: Optional[OperatingModeResponseSameHoursDailyMondayToFriday] = None
    saturday_to_sunday: Optional[OperatingModeResponseSameHoursDailyMondayToFriday] = None


class OperatingModeResponseDifferentHoursDaily(ApiModel):
    sunday: Optional[OperatingModeResponseSameHoursDailyMondayToFriday] = None
    monday: Optional[OperatingModeResponseSameHoursDailyMondayToFriday] = None
    tuesday: Optional[OperatingModeResponseSameHoursDailyMondayToFriday] = None
    wednesday: Optional[OperatingModeResponseSameHoursDailyMondayToFriday] = None
    thursday: Optional[OperatingModeResponseSameHoursDailyMondayToFriday] = None
    friday: Optional[OperatingModeResponseSameHoursDailyMondayToFriday] = None
    saturday: Optional[OperatingModeResponseSameHoursDailyMondayToFriday] = None


class OperatingModeResponseHolidaysItemRecurrence(ApiModel):
    #: Recur yearly by day of week in month
    recur_yearly_by_day: Optional[RecurYearlyByDayObject] = None
    #: Recur yearly by specific date
    recur_yearly_by_date: Optional[RecurYearlyByDateObject] = None


class OperatingModeResponseHolidaysItem(ApiModel):
    #: Unique identifier for the holiday schedule event.
    id: Optional[str] = None
    #: Holiday event name
    name: Optional[str] = None
    #: Whether holiday is all day
    all_day_enabled: Optional[bool] = None
    #: Start date in YYYY-MM-DD format.
    start_date: Optional[datetime] = None
    #: End date in YYYY-MM-DD format.
    end_date: Optional[datetime] = None
    #: Start time in HH:mm format. This field is not present when allDayEnabled is true.
    start_time: Optional[str] = None
    #: End time in HH:mm format. This field is not present when allDayEnabled is true.
    end_time: Optional[str] = None
    #: Recurrence pattern for the holiday. This field is only present for recurring holidays.
    recurrence: Optional[OperatingModeResponseHolidaysItemRecurrence] = None


class OperatingModeResponseForwardTo(ApiModel):
    #: Whether call forwarding is enabled
    enabled: Optional[bool] = None
    #: Forwarding destination phone number
    destination: Optional[str] = None
    #: Whether to send to voicemail
    send_to_voicemail_enabled: Optional[bool] = None


class OperatingModeResponse(ApiModel):
    #: Unique identifier for the operating mode.
    operating_mode_id: Optional[str] = None
    #: Display name of the operating mode.
    name: Optional[str] = None
    type: Optional[ModeManagementFeatureResponseModesItemType] = None
    level: Optional[ModeManagementFeatureResponseModesItemLevel] = None
    #: Location name
    location_name: Optional[str] = None
    #: Schedule configuration when same hours apply for weekdays and weekends
    same_hours_daily: Optional[OperatingModeResponseSameHoursDaily] = None
    #: Schedule configuration when different hours apply for each day
    different_hours_daily: Optional[OperatingModeResponseDifferentHoursDaily] = None
    #: Array of holiday schedule events
    holidays: Optional[list[OperatingModeResponseHolidaysItem]] = None
    #: Call forwarding configuration for this operating mode
    forward_to: Optional[OperatingModeResponseForwardTo] = None


class SimultaneousRingNumber(ApiModel):
    #: Phone number set for simultaneous ring.
    phone_number: Optional[str] = None
    #: When set to `true`, the called party is required to press any key on the keypad to confirm answer for the call.
    answer_confirmation_enabled: Optional[bool] = None


class SimultaneousRingCriteriaSummary(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the schedule which determines when the simultaneous ring is in effect.
    schedule_name: Optional[str] = None
    source: Optional[PriorityAlertCriteriaGetCallsFrom] = None
    #: When set to `true` simultaneous ringing is enabled for calls that meet this criteria. Criteria with
    #: `ringEnabled` set to `false` take priority.
    ring_enabled: Optional[bool] = None


class SimultaneousRingGet(ApiModel):
    #: Simultaneous Ring is enabled or not.
    enabled: Optional[bool] = None
    #: When set to `true`, the configured phone numbers won't ring when you are on a call.
    do_not_ring_if_on_call_enabled: Optional[bool] = None
    #: Enter up to 10 phone numbers to ring simultaneously when you receive an incoming call.
    phone_numbers: Optional[list[SimultaneousRingNumber]] = None
    #: A list of criteria specifying conditions when simultaneous ring is in effect.
    criteria: Optional[list[SimultaneousRingCriteriaSummary]] = None
    #: Controls whether the criteria for simultaneous ring are enabled.
    criterias_enabled: Optional[bool] = None


class GuestCallingNumber(ApiModel):
    #: Phone number available for guest calling.
    phone_number: Optional[str] = None
    state: Optional[LocationAssignedNumberState] = None
    #: Indicates whether this is the location's main number.
    is_main_number: Optional[bool] = None


class BlockPreviousPasscodes(ApiModel):
    #: If enabled, set how many of the previous passcodes are not allowed to be re-used.
    enabled: Optional[bool] = None
    #: Number of previous passcodes. The minimum value is 1. The maximum value is 10.
    number_of_passcodes: Optional[int] = None


class BlockRepeatedDigits(ApiModel):
    #: If enabled, checks for sequence of the same digit being repeated.
    enabled: Optional[bool] = None
    #: Maximum number of repeated digit sequence allowed. The minimum value is 1. The maximum value is 6.
    max_: Optional[int] = None


class BlockContiguousSequences(ApiModel):
    #: If enabled, passcode should not contain a numerical sequence.
    enabled: Optional[bool] = None
    #: Specifies the maximum length of an ascending numerical sequence allowed. The minimum value is 2. The maximum
    #: value is 5. Example: If this value is set to 3, then 123856 is allowed, but 123485 is not allowed (since the
    #: ascending sequence 1234 exceeds 3 digits).
    number_of_ascending_digits: Optional[int] = None
    #: Specifies the maximum length of a descending numerical sequence allowed. The minimum value is 2. The maximum
    #: value is 5. Example: If this value is set to 3, then 321856 is allowed, but 432185 is not allowed (since the
    #: descending sequence 4321 exceeds 3 digits).
    number_of_descending_digits: Optional[int] = None


class PasscodeLength(ApiModel):
    #: The minimum value is 2. The maximum value is 15.
    min: Optional[int] = None
    #: The minimum value is 3. The maximum value is 30.
    max_: Optional[int] = None


class VoicemailRules(ApiModel):
    #: If enabled, the passcode cannot contain repeated patterns. For example, 121212 and 123123.
    block_repeated_patterns_enabled: Optional[bool] = None
    #: If enabled, the passcode must not match the user's own phone number.
    block_user_number_enabled: Optional[bool] = None
    #: If enabled, the passcode must not match the user's phone number in reverse.
    block_reversed_user_number_enabled: Optional[bool] = None
    block_previous_passcodes: Optional[BlockPreviousPasscodes] = None
    #: If enabled, the passcode must not match the user's old passcodes in reverse.
    block_reversed_old_passcode_enabled: Optional[bool] = None
    block_repeated_digits: Optional[BlockRepeatedDigits] = None
    block_contiguous_sequences: Optional[BlockContiguousSequences] = None
    length: Optional[PasscodeLength] = None


class HotelingGuestSettings(ApiModel):
    #: Enable/Disable hoteling guest functionality for the person. When enabled, the person can associate themselves
    #: with a hoteling host device.
    enabled: Optional[bool] = None
    #: When enabled, the person's hoteling guest association will be automatically removed after the specified time
    #: period.
    association_limit_enabled: Optional[bool] = None
    #: Time limit in hours for the hoteling guest association (1-999). Applicable when associationLimitEnabled is true.
    association_limit_hours: Optional[int] = None
    #: Time limit in hours configured by the host for guest associations.
    host_association_limit_hours: Optional[int] = None
    #: Indicates whether the host has enforced an association time limit.
    host_enforced_association_limit_enabled: Optional[bool] = None
    #: First name of the hoteling host.
    host_first_name: Optional[str] = None
    #: Last name of the hoteling host.
    host_last_name: Optional[str] = None
    #: Unique identifier of the hoteling host person or workspace.
    host_id: Optional[str] = None
    #: Phone number of the hoteling host.
    host_phone_number: Optional[str] = None
    #: Extension of the hoteling host.
    host_extension: Optional[str] = None
    host_location: Optional[ModeManagementFeaturesResponseFeaturesItemLocation] = None


class AvailableHotelingHost(ApiModel):
    #: Unique identifier for the person or workspace.
    host_id: Optional[str] = None
    #: First name of the hoteling host.
    first_name: Optional[str] = None
    #: Last name of the hoteling host.
    last_name: Optional[str] = None
    #: Phone number of the hoteling host.
    phone_number: Optional[str] = None
    #: Extension of the hoteling host.
    extension: Optional[str] = None
    #: Maximum allowed association duration in hours for this host.
    allowed_association_duration: Optional[int] = None


class PersonalAssistantSettingsPresence(str, Enum):
    business_trip = 'BUSINESS_TRIP'
    gone_for_the_day = 'GONE_FOR_THE_DAY'
    lunch = 'LUNCH'
    meeting = 'MEETING'
    out_of_office = 'OUT_OF_OFFICE'
    temporarily_out = 'TEMPORARILY_OUT'
    training = 'TRAINING'
    unavailable = 'UNAVAILABLE'
    vacation = 'VACATION'


class PersonalAssistantSettingsAlerting(str, Enum):
    alert_me_first = 'ALERT_ME_FIRST'
    play_ring_reminder = 'PLAY_RING_REMINDER'
    none_ = 'NONE'


class PersonalAssistantSettings(ApiModel):
    #: Enable/Disable the personal assistant feature.
    enabled: Optional[bool] = None
    #: Presence status that triggers the personal assistant.
    presence: Optional[PersonalAssistantSettingsPresence] = None
    #: Date and time until which the personal assistant is active (ISO 8601 format).
    until_date_time: Optional[datetime] = None
    #: Enable/Disable call transfer when personal assistant is active.
    transfer_enabled: Optional[bool] = None
    #: Phone number to transfer calls to when transfer is enabled.
    transfer_number: Optional[str] = None
    #: Alerting behavior for incoming calls when personal assistant is active. Possible values: ALERT_ME_FIRST - Ring
    #: the user's phone first before the personal assistant takes over. PLAY_RING_REMINDER - Play a ring reminder to
    #: the user. NONE - No alerting.
    alerting: Optional[PersonalAssistantSettingsAlerting] = None
    #: Number of rings before transferring the call when alerting is set to ALERT_ME_FIRST.
    alert_me_first_number_of_rings: Optional[int] = None


class CallSettingsForMe22Api(ApiChild, base='telephony/config/people/me'):
    """
    Call Settings For Me (2/2)
    
    Call settings for me APIs allow a person to read or modify their settings.
    
    Viewing settings requires a user auth token with a scope of `spark:telephony_config_read`.
    
    Configuring settings requires a user auth token with a scope of `spark:telephony_config_write`.
    """

    def get_available_numbers_for_my_location(self, name: str = None, phone_number: str = None, extension: str = None,
                                              order: str = None,
                                              **params: Any) -> Generator[LocationAssignedNumber, None, None]:
        """
        Get Available Numbers for User's Location.

        Fetch all the numbers available in User's location.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param name: List numbers whose owner name contains this string.
        :type name: str
        :param phone_number: List numbers whose phoneNumber contains this string.
        :type phone_number: str
        :param extension: List numbers whose extension contains this string.
        :type extension: str
        :param order: Sort the list of numbers based on `lastName`, `dn`, `extension` either asc or desc.
        :type order: str
        :return: Generator yielding :class:`LocationAssignedNumber` instances
        """
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        if order is not None:
            params['order'] = order
        url = self.ep('location/assignedNumbers')
        return self.session.follow_pagination(url=url, model=LocationAssignedNumber, item_key='phoneNumbers', params=params)

    def get_my_location_schedule(self, schedule_type: UserScheduleType,
                                 schedule_id: str) -> UserLocationScheduleGetResponse:
        """
        Get User's Location Level Schedule

        Get Location Schedule for Call Settings of the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param schedule_type: Type of the schedule.
        * `businessHours` - Business hours schedule type.
        * `holidays` - Holidays schedule type.
        :type schedule_type: UserScheduleType
        :param schedule_id: Retrieve the schedule with the matching ID.
        :type schedule_id: str
        :rtype: :class:`UserLocationScheduleGetResponse`
        """
        url = self.ep(f'locations/schedules/{enum_str(schedule_type)}/{schedule_id}')
        data = super().get(url)
        r = UserLocationScheduleGetResponse.model_validate(data)
        return r

    def get_my_schedules(self) -> builtins.list[UserSchedule]:
        """
        Get User (and Location) Schedules

        Get Schedules for Call Settings for the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[UserSchedule]
        """
        url = self.ep('schedules')
        data = super().get(url)
        r = TypeAdapter(list[UserSchedule]).validate_python(data['schedules'])
        return r

    def create_my_schedule(self, type: UserScheduleType, name: str, events: list[ScheduleEventObject] = None) -> str:
        """
        Add a User level Schedule for Call Settings

        Create a new Schedule for the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param type: Type of the schedule.
        :type type: UserScheduleType
        :param name: Unique name for the schedule.
        :type name: str
        :param events: List of schedule events.
        :type events: list[ScheduleEventObject]
        :rtype: str
        """
        body: dict[str, Any] = dict()
        body['type'] = enum_str(type)
        body['name'] = name
        if events is not None:
            body['events'] = TypeAdapter(list[ScheduleEventObject]).dump_python(events, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('schedules')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_my_user_schedule(self, schedule_type: UserScheduleType, schedule_id: str) -> None:
        """
        Delete a User Schedule

        Delete a specific schedule for the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule_type: Type of the schedule.
        * `businessHours` - Business hours schedule type.
        * `holidays` - Holidays schedule type.
        :type schedule_type: UserScheduleType
        :param schedule_id: Delete the schedule with the matching ID.
        :type schedule_id: str
        :rtype: None
        """
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}')
        super().delete(url)

    def get_my_schedule(self, schedule_type: UserScheduleType, schedule_id: str) -> UserScheduleGetResponse:
        """
        Get User Schedule

        Get a Schedule details for Call Settings of the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param schedule_type: Type of the schedule.
        * `businessHours` - Business hours schedule type.
        * `holidays` - Holidays schedule type.
        :type schedule_type: UserScheduleType
        :param schedule_id: Retrieve the schedule with the matching ID.
        :type schedule_id: str
        :rtype: :class:`UserScheduleGetResponse`
        """
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}')
        data = super().get(url)
        r = UserScheduleGetResponse.model_validate(data)
        return r

    def update_my_schedule(self, schedule_type: UserScheduleType, schedule_id: str, name: str,
                           events: list[UserScheduleEventPatch] = None) -> None:
        """
        Modify User Schedule

        Modify a Schedule details for Call Settings of the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param schedule_type: Type of the schedule.
        * `businessHours` - Business hours schedule type.
        * `holidays` - Holidays schedule type.
        :type schedule_type: UserScheduleType
        :param schedule_id: Update the schedule with the matching ID.
        :type schedule_id: str
        :param name: Name of the schedule.
        :type name: str
        :param events: List of events in the schedule.
        :type events: list[UserScheduleEventPatch]
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['name'] = name
        if events is not None:
            body['events'] = TypeAdapter(list[UserScheduleEventPatch]).dump_python(events, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}')
        super().put(url, json=body)

    def create_my_schedule_event(self, schedule_type: UserScheduleType, schedule_id: str, name: str,
                                 start_date: Union[str, datetime], end_date: Union[str, datetime],
                                 all_day_enabled: bool, start_time: str = None, end_time: str = None,
                                 recurrence: UserScheduleRecurrenceObject = None) -> str:
        """
        Add an event for a User Schedule

        Create a new Event for for the authenticated user's specified schedule.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule_type: Type of the schedule.
        * `businessHours` - Business hours schedule type.
        * `holidays` - Holidays schedule type.
        :type schedule_type: UserScheduleType
        :param schedule_id: add an event for the specified schedule ID.
        :type schedule_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start Date of Event.
        :type start_date: Union[str, datetime]
        :param end_date: End Date of Event.
        :type end_date: Union[str, datetime]
        :param all_day_enabled: An indication of whether given event is an all-day event or not.
        :type all_day_enabled: bool
        :param start_time: Start time of event.
        :type start_time: str
        :param end_time: End time of event.
        :type end_time: str
        :param recurrence: -
        :type recurrence: UserScheduleRecurrenceObject
        :rtype: str
        """
        body: dict[str, Any] = dict()
        body['name'] = name
        body['startDate'] = start_date
        body['endDate'] = end_date
        if start_time is not None:
            body['startTime'] = start_time
        if end_time is not None:
            body['endTime'] = end_time
        body['allDayEnabled'] = all_day_enabled
        if recurrence is not None:
            body['recurrence'] = recurrence.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}/events')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_my_user_schedule_event(self, schedule_type: UserScheduleType, schedule_id: str, event_id: str) -> None:
        """
        Delete User a Schedule Event

        Delete a specific schedule event for the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule_type: Type of the schedule.
        * `businessHours` - Business hours schedule type.
        * `holidays` - Holidays schedule type.
        :type schedule_type: UserScheduleType
        :param schedule_id: Delete an event for the specified schedule ID.
        :type schedule_id: str
        :param event_id: Delete the event with the matching ID.
        :type event_id: str
        :rtype: None
        """
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}/events/{event_id}')
        super().delete(url)

    def get_my_schedule_event(self, schedule_type: UserScheduleType, schedule_id: str,
                              event_id: str) -> UserScheduleEvent:
        """
        Get User Schedule Event

        Get a Schedule Event details for Call Settings of the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param schedule_type: Type of the schedule.
        * `businessHours` - Business hours schedule type.
        * `holidays` - Holidays schedule type.
        :type schedule_type: UserScheduleType
        :param schedule_id: Retrieve the schedule with the matching ID.
        :type schedule_id: str
        :param event_id: Retrieve the event with the matching ID.
        :type event_id: str
        :rtype: :class:`UserScheduleEvent`
        """
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}/events/{event_id}')
        data = super().get(url)
        r = UserScheduleEvent.model_validate(data)
        return r

    def update_my_schedule_event(self, schedule_type: UserScheduleType, schedule_id: str, event_id: str, name: str,
                                 start_date: Union[str, datetime], end_date: Union[str, datetime],
                                 all_day_enabled: bool, new_name: str = None, start_time: str = None,
                                 end_time: str = None, recurrence: UserScheduleRecurrenceObject = None) -> None:
        """
        Modify User Schedule Event

        Modify a Schedule event details for Call Settings of the authenticated user.

        Schedules are used to define specific time periods which can be applied to various Call Settings, such as
        Sequential Ring, or Priority Alert. These call settings perform the defined actions based on the time frame in
        the schedule, making it more convenient for users to manage their calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param schedule_type: Type of the schedule.
        * `businessHours` - Business hours schedule type.
        * `holidays` - Holidays schedule type.
        :type schedule_type: UserScheduleType
        :param schedule_id: Update an event for the specified schedule ID.
        :type schedule_id: str
        :param event_id: Update the event with the matching ID.
        :type event_id: str
        :param name: Name for the event.
        :type name: str
        :param start_date: Start Date of Event.
        :type start_date: Union[str, datetime]
        :param end_date: End Date of Event.
        :type end_date: Union[str, datetime]
        :param all_day_enabled: An indication of whether given event is an all-day event or not.
        :type all_day_enabled: bool
        :param new_name: New Name for the event.
        :type new_name: str
        :param start_time: Start time of event.
        :type start_time: str
        :param end_time: End time of event.
        :type end_time: str
        :param recurrence: -
        :type recurrence: UserScheduleRecurrenceObject
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['name'] = name
        if new_name is not None:
            body['newName'] = new_name
        body['startDate'] = start_date
        body['endDate'] = end_date
        if start_time is not None:
            body['startTime'] = start_time
        if end_time is not None:
            body['endTime'] = end_time
        body['allDayEnabled'] = all_day_enabled
        if recurrence is not None:
            body['recurrence'] = recurrence.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'schedules/{enum_str(schedule_type)}/{schedule_id}/events/{event_id}')
        super().put(url, json=body)

    def get_my_anonymous_call_reject_settings(self) -> bool:
        """
        Get Anonymous Call Rejection Settings for User

        Get Anonymous Call Rejection Settings for the authenticated user.

        Anonymous Call Rejection allows you to reject calls from anonymous callers.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: bool
        """
        url = self.ep('settings/anonymousCallReject')
        data = super().get(url)
        r = data['enabled']
        return r

    def update_my_anonymous_call_reject_settings(self, enabled: bool) -> None:
        """
        Modify Anonymous Call Rejection Settings for User

        Update Anonymous Call Rejection Settings for the authenticated user.

        Anonymous Call Rejection allows you to reject calls from anonymous callers.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Indicates whether Anonymous Call Rejection is enabled or not.
        :type enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        url = self.ep('settings/anonymousCallReject')
        super().put(url, json=body)

    def get_my_call_notify_settings(self) -> CallNotifyGet:
        """
        Get Call Notify Settings for User

        Get Call Notify Settings for the authenticated user.

        Call Notify allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the user
        wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`CallNotifyGet`
        """
        url = self.ep('settings/callNotify')
        data = super().get(url)
        r = CallNotifyGet.model_validate(data)
        return r

    def update_my_call_notify_settings(self, enabled: bool, email_address: str = None) -> None:
        """
        Modify Call Notify Settings for User

        Update Call Notify Settings for the authenticated user.

        Call Notify allows you to set up a unique ringtone based on predefined criteria. This API allows modifying
        attributes such as name, phoneNumbers etc for a particular criteria.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Indicates whether the call notify feature should be enabled or disabled for the user.
        :type enabled: bool
        :param email_address: Email Address to which call notifications to be received.
        :type email_address: str
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        if email_address is not None:
            body['emailAddress'] = email_address
        url = self.ep('settings/callNotify')
        super().put(url, json=body)

    def create_my_call_notify_criteria(self, schedule_name: str = None, schedule_type: UserScheduleType = None,
                                       schedule_level: UserScheduleLevel = None,
                                       calls_from: PriorityAlertCriteriaGetCallsFrom = None,
                                       anonymous_callers_enabled: bool = None,
                                       unavailable_callers_enabled: bool = None, phone_numbers: list[str] = None,
                                       notification_enabled: bool = None) -> str:
        """
        Add a Call Notify Criteria

        Create a Call Notify Criteria for the authenticated user.

        Call Notify allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the user
        wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule_name: Name of the schedule to be associated with the criteria.
        :type schedule_name: str
        :param schedule_type: Type of the schedule.
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: Specifies the type of callsFrom, categorizing incoming data based on callsFrom types or
            numbers that match the current criteria.
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param anonymous_callers_enabled: Indicates whether anonymous callers are included in this criteria. Required
            if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Indicates whether unavailable callers are included in this criteria.
            Required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers to update for this criteria. Required if `callsFrom` is
            `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param notification_enabled: Determines whether call notification is applied for calls matching this criteria.
            If `true`, call notify is applied. If `false`, this criteria acts as a 'Don't Notify Me' rule, preventing
            call notification. Criteria with `notificationEnabled` set to `false` (Don't Notify Me) take precedence
            over criteria with `notificationEnabled` set to `true` (Notify).
        :type notification_enabled: bool
        :rtype: str
        """
        body: dict[str, Any] = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if notification_enabled is not None:
            body['notificationEnabled'] = notification_enabled
        url = self.ep('settings/callNotify/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_my_call_notify_criteria(self, id: str) -> None:
        """
        Delete a Call Notify Criteria

        Delete a Call Notify criteria for the authenticated user.

        Call Notify allows you to set up a unique ringtone based on predefined criteria. This API removes a specific
        criteria rule by its unique identifier.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the call notify criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'settings/callNotify/criteria/{id}')
        super().delete(url)

    def get_my_call_notify_criteria_settings(self, id: str) -> PriorityAlertCriteriaGet:
        """
        Get Call Notify Criteria Settings

        Get Call Notify Criteria Settings for the authenticated user.

        Call Notify allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the user
        wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param id: The `id` parameter specifies the unique identifier for the call notify criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :rtype: :class:`PriorityAlertCriteriaGet`
        """
        url = self.ep(f'settings/callNotify/criteria/{id}')
        data = super().get(url)
        r = PriorityAlertCriteriaGet.model_validate(data)
        return r

    def update_my_call_notify_criteria_settings(self, id: str, schedule_name: str = None,
                                                schedule_type: UserScheduleType = None,
                                                schedule_level: UserScheduleLevel = None,
                                                calls_from: PriorityAlertCriteriaGetCallsFrom = None,
                                                anonymous_callers_enabled: bool = None,
                                                unavailable_callers_enabled: bool = None,
                                                phone_numbers: list[str] = None,
                                                notification_enabled: bool = None) -> None:
        """
        Modify a Call Notify Criteria

        Modify Call Notify Criteria Settings for the authenticated user.

        Call Notify allows you to set up a unique ringtone based on predefined criteria. This API allows modifying
        attributes such as name, phoneNumbers etc for a particular criteria.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the call notify criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :param schedule_name: Name of the schedule to be associated with the criteria.
        :type schedule_name: str
        :param schedule_type: Type of the schedule.
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: Specifies the type of callsFrom, categorizing incoming data based on callsFrom types or
            numbers that match the current criteria.
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param anonymous_callers_enabled: Indicates whether anonymous callers are included in this criteria. Required
            if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Indicates whether unavailable callers are included in this criteria.
            Required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers to update for this criteria. Required if `callsFrom` is
            `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param notification_enabled: Determines whether call notification is applied for calls matching this criteria.
            If `true`, call notify is applied. If `false`, this criteria acts as a 'Don't Notify Me' rule, preventing
            call notification. Criteria with `notificationEnabled` set to `false` (Don't Notify Me) take precedence
            over criteria with `notificationEnabled` set to `true` (Notify).
        :type notification_enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if notification_enabled is not None:
            body['notificationEnabled'] = notification_enabled
        url = self.ep(f'settings/callNotify/criteria/{id}')
        super().put(url, json=body)

    def get_my_call_waiting_settings(self) -> bool:
        """
        Get Call Waiting Settings for User

        Get Call Waiting Settings for the authenticated user.

        Call Waiting allows a user to receive multiple calls simultaneously. When the user is on an active call, they
        can receive an incoming call and switch between the two calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: bool
        """
        url = self.ep('settings/callWaiting')
        data = super().get(url)
        r = data['enabled']
        return r

    def update_my_call_waiting_settings(self, enabled: bool) -> None:
        """
        Modify Call Waiting Settings for User

        Update Call Waiting Settings for the authenticated user.

        Call Waiting allows a user to receive multiple calls simultaneously. When the user is on an active call, they
        can receive an incoming call and switch between the two calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Enable or disable Call Waiting for the user.
        :type enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        url = self.ep('settings/callWaiting')
        super().put(url, json=body)

    def get_my_guest_calling_numbers(self) -> builtins.list[GuestCallingNumber]:
        """
        Retrieve My Guest Calling Numbers

        Retrieve available guest calling numbers for the authenticated user.

        This API returns a list of phone numbers that can be used for guest calling purposes.

        Retrieving guest calling numbers requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[GuestCallingNumber]
        """
        url = self.ep('settings/guestCalling/numbers')
        data = super().get(url)
        r = TypeAdapter(list[GuestCallingNumber]).validate_python(data['phoneNumbers'])
        return r

    def get_available_hoteling_hosts(self, name: str = None, phone_number: str = None,
                                     **params: Any) -> Generator[AvailableHotelingHost, None, None]:
        """
        Get Available Hoteling Hosts

        Retrieve a list of available hoteling hosts that a person can associate with as a guest. Returns hosts that
        have hoteling enabled on their devices and are available for guest associations. The list can be filtered by
        name or phone number and supports pagination.

        Hoteling is a feature of Webex Calling that enables flexible workspace solutions by allowing users to log into
        shared devices.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param name: Filter hosts by name (first name or last name). Partial match is supported.
        :type name: str
        :param phone_number: Filter hosts by phone number. Partial match is supported.
        :type phone_number: str
        :return: Generator yielding :class:`AvailableHotelingHost` instances
        """
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('settings/hoteling/availableHosts')
        return self.session.follow_pagination(url=url, model=AvailableHotelingHost, item_key='hosts', params=params)

    def get_hoteling_guest_settings(self) -> HotelingGuestSettings:
        """
        Get Hoteling Guest Settings

        Retrieve hoteling guest settings for a person. Hoteling allows a person to temporarily use a device as a guest,
        associating their extension and configuration with that device for a limited time. This API returns the
        current hoteling guest configuration including any active host association details.

        Hoteling is a feature of Webex Calling that enables flexible workspace solutions by allowing users to log into
        shared devices.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`HotelingGuestSettings`
        """
        url = self.ep('settings/hoteling/guest')
        data = super().get(url)
        r = HotelingGuestSettings.model_validate(data)
        return r

    def update_hoteling_guest_settings(self, enabled: bool, association_limit_enabled: bool = None,
                                       association_limit_hours: int = None, host_id: str = None) -> None:
        """
        Update Hoteling Guest Settings

        Update hoteling guest settings for a person. Allows enabling or disabling the ability to use hoteling as a
        guest, configuring whether an association will be removed automatically after a specified time period, and
        associating with a hoteling host.

        Hoteling is a feature of Webex Calling that enables flexible workspace solutions by allowing users to log into
        shared devices.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Enable/Disable hoteling guest functionality for the person. When enabled, the person can
            associate themselves with a hoteling host device.
        :type enabled: bool
        :param association_limit_enabled: When enabled, the person's hoteling guest association will be automatically
            removed after the specified time period.
        :type association_limit_enabled: bool
        :param association_limit_hours: Time limit in hours for the hoteling guest association (1-999). Applicable when
            associationLimitEnabled is true.
        :type association_limit_hours: int
        :param host_id: Unique identifier of the hoteling host person or workspace to associate with. Required when
            enabling hoteling guest functionality.
        :type host_id: str
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        if association_limit_enabled is not None:
            body['associationLimitEnabled'] = association_limit_enabled
        if association_limit_hours is not None:
            body['associationLimitHours'] = association_limit_hours
        if host_id is not None:
            body['hostId'] = host_id
        url = self.ep('settings/hoteling/guest')
        super().put(url, json=body)

    def get_mode_management_features(self) -> builtins.list[ModeManagementFeaturesResponseFeaturesItem]:
        """
        Get Mode Management Features

        Retrieves a list of all mode management features (Auto Attendants, Call Queues, and Hunt Groups) for which the
        authenticated user has been designated as a mode manager. This API returns basic information about each
        feature including its ID, name, and type.

        Mode Management allows designated managers to switch features between different operational configurations
        based on time schedules or manual triggers. This is useful for managing business hours, holidays, and
        emergency scenarios.

        This API requires a user auth token with the `spark:telephony_config_read` scope. The authenticated user must
        be configured as a mode manager for at least one feature to receive results.

        :rtype: list[ModeManagementFeaturesResponseFeaturesItem]
        """
        url = self.ep('settings/modeManagement/features')
        data = super().get(url)
        r = TypeAdapter(list[ModeManagementFeaturesResponseFeaturesItem]).validate_python(data['features'])
        return r

    def switch_mode_multiple_features(self, feature_ids: list[str], operating_mode_name: str) -> None:
        """
        Switch Mode for Multiple Features

        Switches the operating mode for multiple features simultaneously by specifying a common mode name. This API
        accepts a list of feature IDs and sets all of them to the specified operating mode, provided that mode exists
        for all features.

        This bulk operation is particularly useful for coordinating operational changes across an organization, such as
        activating holiday modes, emergency procedures, or after-hours configurations across multiple Auto Attendants,
        Call Queues, and Hunt Groups at once.

        This API requires a user auth token with the `spark:telephony_config_write` scope. The authenticated user must
        be a mode manager for all specified features.

        :param feature_ids: List of feature IDs to switch mode
        :type feature_ids: list[str]
        :param operating_mode_name: Name of the common operating mode to be set as current operating mode
        :type operating_mode_name: str
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['featureIds'] = feature_ids
        body['operatingModeName'] = operating_mode_name
        url = self.ep('settings/modeManagement/features/actions/switchMode/invoke')
        super().post(url, json=body)

    def get_common_modes(self, feature_ids: list[str]) -> builtins.list[str]:
        """
        Get Common Modes

        Retrieves a list of common operating mode names that are shared across multiple specified features. This API
        accepts a list of feature IDs and returns only the mode names that exist in all of the specified features,
        allowing managers to switch multiple features to the same mode simultaneously.

        Common modes are useful when you need to coordinate operational changes across multiple features. For example,
        switching an entire office to "Holiday" mode across all Auto Attendants and Call Queues at once.

        This API requires a user auth token with the `spark:telephony_config_read` scope. The authenticated user must
        be a mode manager for the specified features.

        :param feature_ids: List of feature IDs (comma-separated) for auto attendants, call queues, or hunt groups
        :type feature_ids: list[str]
        :rtype: list[str]
        """
        params: dict[str, Any] = dict()
        params['featureIds'] = ','.join(feature_ids)
        url = self.ep('settings/modeManagement/features/commonModes')
        data = super().get(url, params=params)
        r = data['commonModeNames']
        return r

    def get_mode_management_feature(self, feature_id: str) -> ModeManagementFeatureResponse:
        """
        Get Mode Management Feature

        Retrieves detailed information about a specific mode management feature including its current operating mode
        and exception status. This API provides the feature's ID, name, type, current operating mode ID, and whether
        it is currently in an exception mode.

        Exception mode indicates that the feature has been manually switched to a different mode than what its schedule
        dictates. This information is critical for mode managers to understand the current state of their features.

        This API requires a user auth token with the `spark:telephony_config_read` scope. The authenticated user must
        be a mode manager for the specified feature.

        :param feature_id: Unique identifier for the feature.
        :type feature_id: str
        :rtype: :class:`ModeManagementFeatureResponse`
        """
        url = self.ep(f'settings/modeManagement/features/{feature_id}')
        data = super().get(url)
        r = ModeManagementFeatureResponse.model_validate(data)
        return r

    def extend_mode(self, feature_id: str, operating_mode_id: str, extension_time: int = None) -> None:
        """
        Extend Current Operating Mode Duration

        Extends the duration of the current operating mode by adding additional time before it expires or reverts to
        scheduled operation. This API allows managers to prolong a temporary mode change without having to switch
        modes again.

        Extension time can be specified in 30-minute increments up to 720 minutes (12 hours). If no extension time is
        provided, the mode is extended with a manual switchback exception, meaning it will remain active until
        manually changed.

        This API requires a user auth token with the `spark:telephony_config_write` scope. The authenticated user must
        be a mode manager for the specified feature.

        :param feature_id: Unique identifier for the feature.
        :type feature_id: str
        :param operating_mode_id: Unique identifier for the operating mode for which the extension is being configured.
        :type operating_mode_id: str
        :param extension_time: Extension time in minutes (must be multiple of 30). If not sent, mode is extended with
            manual switch back exception
        :type extension_time: int
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['operatingModeId'] = operating_mode_id
        if extension_time is not None:
            body['extensionTime'] = extension_time
        url = self.ep(f'settings/modeManagement/features/{feature_id}/actions/extendMode/invoke')
        super().post(url, json=body)

    def switch_mode_for_feature(self, feature_id: str, operating_mode_id: str,
                                is_manual_switchback_enabled: bool = None) -> None:
        """
        Switch Mode for Single Feature

        Switches the operating mode for a single feature to a specified mode, either temporarily or with manual
        switchback. This API creates an exception to the feature's normal scheduled operation, allowing managers to
        manually control the feature's behavior.

        You can configure whether the mode switch is temporary (automatically reverts based on schedule) or requires
        manual switchback. This is useful for handling unexpected situations like emergency closures, special events,
        or unscheduled breaks.

        This API requires a user auth token with the `spark:telephony_config_write` scope. The authenticated user must
        be a mode manager for the specified feature.

        :param feature_id: Unique identifier for the feature.
        :type feature_id: str
        :param operating_mode_id: Operating mode ID to switch to
        :type operating_mode_id: str
        :param is_manual_switchback_enabled: Determines if switch back will be manual (if true) or automatic (if false
            or omitted from request)
        :type is_manual_switchback_enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['operatingModeId'] = operating_mode_id
        if is_manual_switchback_enabled is not None:
            body['isManualSwitchbackEnabled'] = is_manual_switchback_enabled
        url = self.ep(f'settings/modeManagement/features/{feature_id}/actions/switchMode/invoke')
        super().post(url, json=body)

    def switch_to_normal_operation(self, feature_id: str) -> None:
        """
        Switch to Normal Operation

        Switches the feature back to its normal scheduled operation mode, removing any manual exceptions or overrides
        that may be active. This returns the feature to operating according to its configured time schedules.

        This operation is useful when a temporary manual mode change (exception) is no longer needed and you want to
        restore automatic schedule-based operation. It effectively cancels any active manual mode switches.

        This API requires a user auth token with the `spark:telephony_config_write` scope. The authenticated user must
        be a mode manager for the specified feature.

        :param feature_id: Unique identifier for the feature.
        :type feature_id: str
        :rtype: None
        """
        url = self.ep(f'settings/modeManagement/features/{feature_id}/actions/switchToNormalOperation/invoke')
        super().post(url)

    def get_operating_mode(self, feature_id: str, mode_id: str) -> OperatingModeResponse:
        """
        Get Operating Mode

        Retrieves detailed information about a specific operating mode for a feature, including the mode's ID and name.
        This API allows managers to get the details of any operating mode configured for a feature.

        Operating modes define different configurations for how a feature behaves (e.g., business hours routing vs.
        after-hours routing). Each mode has a unique ID and a descriptive name that helps managers identify its
        purpose.

        This API requires a user auth token with the `spark:telephony_config_read` scope. The authenticated user must
        be a mode manager for the specified feature.

        :param feature_id: Unique identifier for the feature.
        :type feature_id: str
        :param mode_id: Unique identifier for the operating mode.
        :type mode_id: str
        :rtype: :class:`OperatingModeResponse`
        """
        url = self.ep(f'settings/modeManagement/features/{feature_id}/modes/{mode_id}')
        data = super().get(url)
        r = OperatingModeResponse.model_validate(data)
        return r

    def get_normal_operation_mode(self, feature_id: str) -> str:
        """
        Get Normal Operation Mode

        Retrieves the current normal operating mode that the feature is scheduled to be in based on its time schedules.
        This represents the mode the feature would be in if no manual exceptions or overrides were active.

        The normal operation mode is determined by the feature's configured schedules and may differ from the actual
        current operating mode if a manual exception has been applied. This API helps managers understand what the
        scheduled behavior is versus the actual current state.

        This API requires a user auth token with the `spark:telephony_config_read` scope. The authenticated user must
        be a mode manager for the specified feature.

        :param feature_id: Unique identifier for the feature.
        :type feature_id: str
        :rtype: str
        """
        url = self.ep(f'settings/modeManagement/features/{feature_id}/normalOperationMode')
        data = super().get(url)
        r = data['operatingModeId']
        return r

    def get_personal_assistant_settings(self) -> PersonalAssistantSettings:
        """
        Get Personal Assistant Settings

        Retrieve personal assistant settings for a person. The personal assistant feature allows users to configure an
        automated attendant that can handle incoming calls when they are unavailable, including presence-based routing
        and call transfer options.

        Personal Assistant is a feature of Webex Calling that helps manage incoming calls based on the user's
        availability status.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`PersonalAssistantSettings`
        """
        url = self.ep('settings/personalAssistant')
        data = super().get(url)
        r = PersonalAssistantSettings.model_validate(data)
        return r

    def update_personal_assistant_settings(self, enabled: bool, presence: PersonalAssistantSettingsPresence = None,
                                           until_date_time: Union[str, datetime] = None,
                                           transfer_enabled: bool = None, transfer_number: str = None,
                                           alerting: PersonalAssistantSettingsAlerting = None,
                                           alert_me_first_number_of_rings: int = None) -> None:
        """
        Update Personal Assistant Settings

        Update personal assistant settings for a person. Allows configuring the personal assistant feature including
        enabling/disabling it, setting presence status, configuring call transfer options, and alerting preferences.

        Personal Assistant is a feature of Webex Calling that helps manage incoming calls based on the user's
        availability status.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Enable/Disable the personal assistant feature.
        :type enabled: bool
        :param presence: Presence status that triggers the personal assistant.
        :type presence: PersonalAssistantSettingsPresence
        :param until_date_time: Date and time until which the personal assistant is active (ISO 8601 format).
        :type until_date_time: Union[str, datetime]
        :param transfer_enabled: Enable/Disable call transfer when personal assistant is active.
        :type transfer_enabled: bool
        :param transfer_number: Phone number to transfer calls to when transfer is enabled.
        :type transfer_number: str
        :param alerting: Alerting behavior for incoming calls when personal assistant is active. Possible values:
            ALERT_ME_FIRST - Ring the user's phone first before the personal assistant takes over. PLAY_RING_REMINDER
            - Play a ring reminder to the user. NONE - No alerting.
        :type alerting: PersonalAssistantSettingsAlerting
        :param alert_me_first_number_of_rings: Number of rings before transferring the call when alerting is set to
            ALERT_ME_FIRST.
        :type alert_me_first_number_of_rings: int
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        if presence is not None:
            body['presence'] = enum_str(presence)
        if until_date_time is not None:
            body['untilDateTime'] = until_date_time
        if transfer_enabled is not None:
            body['transferEnabled'] = transfer_enabled
        if transfer_number is not None:
            body['transferNumber'] = transfer_number
        if alerting is not None:
            body['alerting'] = enum_str(alerting)
        if alert_me_first_number_of_rings is not None:
            body['alertMeFirstNumberOfRings'] = alert_me_first_number_of_rings
        url = self.ep('settings/personalAssistant')
        super().put(url, json=body)

    def get_my_priority_alert_settings(self) -> PriorityAlertGet:
        """
        Get Priority Alert Settings

        Get Priority Alert Settings for the authenticated user.

        Priority alert allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the
        user wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`PriorityAlertGet`
        """
        url = self.ep('settings/priorityAlert')
        data = super().get(url)
        r = PriorityAlertGet.model_validate(data)
        return r

    def update_my_priority_alert_settings(self, enabled: bool) -> None:
        """
        Modify Priority Alert Settings for User

        Update Priority Alert Settings for the authenticated user.

        Priority alert allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the
        user wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Indicates whether the priority alert feature should be enabled or disabled for the user.
        :type enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        url = self.ep('settings/priorityAlert')
        super().put(url, json=body)

    def create_my_priority_alert_criteria(self, schedule_name: str = None, schedule_type: UserScheduleType = None,
                                          schedule_level: UserScheduleLevel = None,
                                          calls_from: PriorityAlertCriteriaGetCallsFrom = None,
                                          anonymous_callers_enabled: bool = None,
                                          unavailable_callers_enabled: bool = None, phone_numbers: list[str] = None,
                                          notification_enabled: bool = None) -> str:
        """
        Add a Priority Alert Criteria

        Create a Priority Alert Criteria for the authenticated user.

        Priority alert allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the
        user wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule_name: Name of the schedule to be associated with the criteria.
        :type schedule_name: str
        :param schedule_type: Type of the schedule.
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: Specifies the type of callsFrom, categorizing incoming data based on callsFrom types or
            numbers that match the current criteria.
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param anonymous_callers_enabled: Indicates whether anonymous callers are included in this criteria. Required
            if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Indicates whether unavailable callers are included in this criteria.
            Required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers to update for this criteria. Required if `callsFrom` is
            `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param notification_enabled: Determines whether priority alerting is applied for calls matching this criteria.
            If `true`, priority alerting is applied. If `false`, this criteria acts as a 'Don't Alert' rule,
            preventing priority alerting. Criteria with `notificationEnabled` set to `false` (Don't Alert) take
            precedence over criteria with `notificationEnabled` set to `true` (Alert).
        :type notification_enabled: bool
        :rtype: str
        """
        body: dict[str, Any] = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if notification_enabled is not None:
            body['notificationEnabled'] = notification_enabled
        url = self.ep('settings/priorityAlert/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_my_priority_alert_criteria(self, id: str) -> None:
        """
        Delete a Priority Alert Criteria

        Delete a Priority Alert criteria for the authenticated user.

        Priority alert allows you to set up a unique ringtone based on predefined criteria. This API removes a specific
        criteria rule by its unique identifier.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the priority alert criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'settings/priorityAlert/criteria/{id}')
        super().delete(url)

    def get_my_priority_alert_criteria_settings(self, id: str) -> PriorityAlertCriteriaGet:
        """
        Get Priority Alert Criteria Settings

        Get Priority Alert Criteria Settings for the authenticated user.

        Priority alert allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the
        user wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param id: The `id` parameter specifies the unique identifier for the priority alert criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :rtype: :class:`PriorityAlertCriteriaGet`
        """
        url = self.ep(f'settings/priorityAlert/criteria/{id}')
        data = super().get(url)
        r = PriorityAlertCriteriaGet.model_validate(data)
        return r

    def update_my_priority_alert_criteria_settings(self, id: str, schedule_name: str = None,
                                                   schedule_type: UserScheduleType = None,
                                                   schedule_level: UserScheduleLevel = None,
                                                   calls_from: PriorityAlertCriteriaGetCallsFrom = None,
                                                   anonymous_callers_enabled: bool = None,
                                                   unavailable_callers_enabled: bool = None,
                                                   phone_numbers: list[str] = None,
                                                   notification_enabled: bool = None) -> None:
        """
        Modify Settings for a Priority Alert Criteria

        Modify Priority Alert Criteria Settings for the authenticated user.

        Priority alert allows you to set up a unique ringtone based on predefined criteria. This API allows modifying
        attributes such as name, phoneNumbers etc for a particular criteria.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the priority alert criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :param schedule_name: Name of the schedule to be associated with the criteria.
        :type schedule_name: str
        :param schedule_type: Type of the schedule.
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: Specifies the type of callsFrom, categorizing incoming data based on callsFrom types or
            numbers that match the current criteria.
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param anonymous_callers_enabled: Indicates whether anonymous callers are included in this criteria. Required
            if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Indicates whether unavailable callers are included in this criteria.
            Required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers to update for this criteria. Required if `callsFrom` is
            `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param notification_enabled: Determines whether priority alerting is applied for calls matching this criteria.
            If `true`, priority alerting is applied. If `false`, this criteria acts as a 'Don't Alert' rule,
            preventing priority alerting. Criteria with `notificationEnabled` set to `false` (Don't Alert) take
            precedence over criteria with `notificationEnabled` set to `true` (Alert).
        :type notification_enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if notification_enabled is not None:
            body['notificationEnabled'] = notification_enabled
        url = self.ep(f'settings/priorityAlert/criteria/{id}')
        super().put(url, json=body)

    def get_my_selective_accept_settings(self) -> SelectiveAcceptCallSettingsGet:
        """
        Get Selective Call Accept Settings for User

        Get Selective Call Accept Settings for the authenticated user.

        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`SelectiveAcceptCallSettingsGet`
        """
        url = self.ep('settings/selectiveAccept')
        data = super().get(url)
        r = SelectiveAcceptCallSettingsGet.model_validate(data)
        return r

    def update_my_selective_accept_settings(self, enabled: bool) -> None:
        """
        Modify Selective Call Accept Settings for User

        Update Selective Call Accept Settings for the authenticated user.

        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: indicates whether selective accept is enabled or not.
        :type enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        url = self.ep('settings/selectiveAccept')
        super().put(url, json=body)

    def create_my_selective_accept_criteria(self, schedule_name: str, schedule_type: UserScheduleType,
                                            schedule_level: UserScheduleLevel,
                                            calls_from: PriorityAlertCriteriaGetCallsFrom, accept_enabled: bool,
                                            anonymous_callers_enabled: bool = None,
                                            unavailable_callers_enabled: bool = None,
                                            phone_numbers: list[str] = None) -> str:
        """
        Add User Selective Call Accept Criteria

        Create a new Selective Call Accept Criteria for the authenticated user.

        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule_name: Name of the location's schedule which determines when the selective accept is in effect.
        :type schedule_name: str
        :param schedule_type: -
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: Specifies the type of callsFrom, categorizing incoming data based on callsFrom types or
            numbers that match the current criteria.
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param accept_enabled: Determines whether selective call accept is applied for calls matching this criteria. If
            `true`, selective call accept is applied. If `false`, this criteria acts as a 'Don't Accept' rule,
            preventing call acceptance. Criteria with `notificationEnabled` set to `false` (Don't Accept) take
            precedence over criteria with `acceptEnabled` set to `true` (Accept).
        :type accept_enabled: bool
        :param anonymous_callers_enabled: When `true`, enables calls from anonymous callers. Value for this attribute
            is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, enables calls even if callers are unavailable. Value for this
            attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: the list of phone numbers that will checked against incoming calls for a match. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :rtype: str
        """
        body: dict[str, Any] = dict()
        body['scheduleName'] = schedule_name
        body['scheduleType'] = enum_str(schedule_type)
        body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['acceptEnabled'] = accept_enabled
        url = self.ep('settings/selectiveAccept/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_my_selective_call_accept_criteria(self, id: str) -> None:
        """
        Delete a Selective Call Accept Criteria

        Delete a Selective Call Accept Criteria for the authenticated user.



        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the selective call accept criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'settings/selectiveAccept/criteria/{id}')
        super().delete(url)

    def get_my_selective_accept_criteria_settings(self, id: str) -> SelectiveAcceptCallCriteriaGet:
        """
        Get Selective Call Accept Criteria Settings for User

        Get Selective Call Accept Criteria Settings for the authenticated user.

        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param id: The `id` parameter specifies the unique identifier for the selective call accept criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :rtype: :class:`SelectiveAcceptCallCriteriaGet`
        """
        url = self.ep(f'settings/selectiveAccept/criteria/{id}')
        data = super().get(url)
        r = SelectiveAcceptCallCriteriaGet.model_validate(data)
        return r

    def update_my_selective_call_accept_criteria_settings(self, id: str, schedule_name: str = None,
                                                          schedule_type: UserScheduleType = None,
                                                          schedule_level: UserScheduleLevel = None,
                                                          calls_from: PriorityAlertCriteriaGetCallsFrom = None,
                                                          anonymous_callers_enabled: bool = None,
                                                          unavailable_callers_enabled: bool = None,
                                                          phone_numbers: list[str] = None,
                                                          accept_enabled: bool = None) -> None:
        """
        Modify a Selective Call Accept Criteria

        Modify Selective Call Accept Criteria Settings for the authenticated user.



        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the selective call accept. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :param schedule_name: Name of the schedule to be associated with the criteria.
        :type schedule_name: str
        :param schedule_type: Type of the schedule.
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: Specifies the type of callsFrom, categorizing incoming data based on callsFrom types or
            numbers that match the current criteria.
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param anonymous_callers_enabled: Indicates whether anonymous callers are included in this criteria. Required
            if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Indicates whether unavailable callers are included in this criteria.
            Required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers to update for this criteria. Required if `callsFrom` is
            `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param accept_enabled: Determines whether selective call accept is applied for calls matching this criteria. If
            `true`, selective call accept is applied. If `false`, this criteria acts as a 'Don't Accept' rule,
            preventing call acceptance. Criteria with `notificationEnabled` set to `false` (Don't Accept) take
            precedence over criteria with `acceptEnabled` set to `true` (Accept).
        :type accept_enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if accept_enabled is not None:
            body['acceptEnabled'] = accept_enabled
        url = self.ep(f'settings/selectiveAccept/criteria/{id}')
        super().put(url, json=body)

    def get_my_selective_forward_settings(self) -> SelectiveForwardCallSettingsGet:
        """
        Get Selective Call Forward Settings for User

        Get Selective Call Forward Settings for the authenticated user.

        Selective Call Forward allows you to create customized rules to forward specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`SelectiveForwardCallSettingsGet`
        """
        url = self.ep('settings/selectiveForward')
        data = super().get(url)
        r = SelectiveForwardCallSettingsGet.model_validate(data)
        return r

    def update_my_selective_forward_settings(self, enabled: bool, default_phone_number_to_forward: str = None,
                                             ring_reminder_enabled: bool = None,
                                             destination_voicemail_enabled: bool = None) -> None:
        """
        Modify Selective Call Forward Settings for User

        Update the Selective Call Forward Settings for the authenticated user.

        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number, identity, and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: indicates whether selective forward is enabled or not.
        :type enabled: bool
        :param default_phone_number_to_forward: The phone number to which calls are forwarded by default when the
            criteria conditions are met.
        :type default_phone_number_to_forward: str
        :param ring_reminder_enabled: If `true`, a brief tone will be played on the person's phone when a call has been
            forwarded.
        :type ring_reminder_enabled: bool
        :param destination_voicemail_enabled: Indicates whether calls that meet the criteria are forwarded to the
            destination phone number's voicemail.
        :type destination_voicemail_enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        if default_phone_number_to_forward is not None:
            body['defaultPhoneNumberToForward'] = default_phone_number_to_forward
        if ring_reminder_enabled is not None:
            body['ringReminderEnabled'] = ring_reminder_enabled
        if destination_voicemail_enabled is not None:
            body['destinationVoicemailEnabled'] = destination_voicemail_enabled
        url = self.ep('settings/selectiveForward')
        super().put(url, json=body)

    def create_my_selective_call_forward_criteria(self, forward_to_phone_number: str = None,
                                                  destination_voicemail_enabled: bool = None,
                                                  schedule_name: str = None, schedule_type: UserScheduleType = None,
                                                  schedule_level: UserScheduleLevel = None,
                                                  calls_from: PriorityAlertCriteriaGetCallsFrom = None,
                                                  anonymous_callers_enabled: bool = None,
                                                  unavailable_callers_enabled: bool = None,
                                                  phone_numbers: list[str] = None,
                                                  forward_enabled: bool = None) -> str:
        """
        Add a Selective Call Forwarding Criteria

        Create a Selective Call Forwarding Criteria for the authenticated user.

        Selective Call Forward allows you to define rules that automatically forward incoming calls based on specific
        criteria, such as the caller’s phone number, caller identity, and the time and day the call is received.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param forward_to_phone_number: The phone number to which calls are forwarded when the criteria conditions are
            met.
        :type forward_to_phone_number: str
        :param destination_voicemail_enabled: Indicates whether calls that meet the criteria are forwarded to the
            destination phone number's voicemail.
        :type destination_voicemail_enabled: bool
        :param schedule_name: Name of the schedule to be associated with the criteria.
        :type schedule_name: str
        :param schedule_type: Type of the schedule.
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: Specifies the type of callsFrom, categorizing incoming data based on callsFrom types or
            numbers that match the current criteria.
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param anonymous_callers_enabled: Indicates whether anonymous callers are included in this criteria. Required
            if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Indicates whether unavailable callers are included in this criteria.
            Required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers to update for this criteria. Required if `callsFrom` is
            `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param forward_enabled: Determines whether selective call forwarding is applied for calls matching this
            criteria. If `true`, the selective forwarding is applied. If `false`, this criteria acts as a 'Don't
            Forward' rule, preventing selectively forwarding of the calls. Criteria with `forwardEnabled` set to
            `false` (Don't Forward) take precedence over criteria with `forwardEnabled` set to `true` (Forward).
        :type forward_enabled: bool
        :rtype: str
        """
        body: dict[str, Any] = dict()
        if forward_to_phone_number is not None:
            body['forwardToPhoneNumber'] = forward_to_phone_number
        if destination_voicemail_enabled is not None:
            body['destinationVoicemailEnabled'] = destination_voicemail_enabled
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if forward_enabled is not None:
            body['forwardEnabled'] = forward_enabled
        url = self.ep('settings/selectiveForward/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_my_selective_call_forwarding_criteria(self, id: str) -> None:
        """
        Delete a Selective Call Forwarding Criteria

        Delete a Selective Call Forwarding Criteria for the authenticated user.

        Selective call forwarding allows you to define rules that automatically forward incoming calls based on
        specific criteria. This API removes a specific criteria rule by its unique identifier.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the selective call forwarding criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'settings/selectiveForward/criteria/{id}')
        super().delete(url)

    def get_my_selective_call_forward_criteria(self, id: str) -> SelectiveCallForwardCriteriaGet:
        """
        Get Settings for a Selective Call Forwarding Criteria

        Get settings for a Selective Call Forwarding Criteria for the authenticated user.

        Selective Call Forward allows you to define rules that automatically forward incoming calls based on specific
        criteria, such as the caller’s phone number, caller identity, and the time and day the call is received.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param id: The `id` parameter specifies the unique identifier for the selective call forwarding criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :rtype: :class:`SelectiveCallForwardCriteriaGet`
        """
        url = self.ep(f'settings/selectiveForward/criteria/{id}')
        data = super().get(url)
        r = SelectiveCallForwardCriteriaGet.model_validate(data)
        return r

    def update_my_selective_call_forwarding_criteria_settings(self, id: str, forward_to_phone_number: str = None,
                                                              destination_voicemail_enabled: bool = None,
                                                              schedule_name: str = None,
                                                              schedule_type: UserScheduleType = None,
                                                              schedule_level: UserScheduleLevel = None,
                                                              calls_from: PriorityAlertCriteriaGetCallsFrom = None,
                                                              anonymous_callers_enabled: bool = None,
                                                              unavailable_callers_enabled: bool = None,
                                                              phone_numbers: list[str] = None,
                                                              forward_enabled: bool = None) -> None:
        """
        Modify Settings for a Selective Call Forwarding Criteria

        Modify settings for a Selective Call Forwarding Criteria for the authenticated user.

        Selective Call Forward allows you to define rules that automatically forward incoming calls based on specific
        criteria, such as the caller’s phone number, caller identity, and the time and day the call is received.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the selective call forwarding criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :param forward_to_phone_number: The phone number to which calls are forwarded when the criteria conditions are
            met.
        :type forward_to_phone_number: str
        :param destination_voicemail_enabled: Indicates whether calls that meet the criteria are forwarded to the
            destination phone number's voicemail.
        :type destination_voicemail_enabled: bool
        :param schedule_name: Name of the schedule to be associated with the criteria.
        :type schedule_name: str
        :param schedule_type: Type of the schedule.
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: Specifies the type of callsFrom, categorizing incoming data based on callsFrom types or
            numbers that match the current criteria.
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param anonymous_callers_enabled: Indicates whether anonymous callers are included in this criteria. Required
            if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: Indicates whether unavailable callers are included in this criteria.
            Required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers to update for this criteria. Required if `callsFrom` is
            `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param forward_enabled: Determines whether selective call forwarding is applied for calls matching this
            criteria. If `true`, the selective forwarding is applied. If `false`, this criteria acts as a 'Don't
            Forward' rule, preventing selectively forwarding of the calls. Criteria with `forwardEnabled` set to
            `false` (Don't Forward) take precedence over criteria with `forwardEnabled` set to `true` (Forward).
        :type forward_enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        if forward_to_phone_number is not None:
            body['forwardToPhoneNumber'] = forward_to_phone_number
        if destination_voicemail_enabled is not None:
            body['destinationVoicemailEnabled'] = destination_voicemail_enabled
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if forward_enabled is not None:
            body['forwardEnabled'] = forward_enabled
        url = self.ep(f'settings/selectiveForward/criteria/{id}')
        super().put(url, json=body)

    def get_my_selective_reject_settings(self) -> SelectiveRejectCallSettingsGet:
        """
        Get Selective Call Reject Settings for User

        Get Selective Call Reject Settings for the authenticated user.

        Selective Call Reject allows you to create customized rules to reject specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`SelectiveRejectCallSettingsGet`
        """
        url = self.ep('settings/selectiveReject')
        data = super().get(url)
        r = SelectiveRejectCallSettingsGet.model_validate(data)
        return r

    def update_my_selective_reject_settings(self, enabled: bool) -> None:
        """
        Modify Selective Call Reject Settings for User

        Update Selective Call Reject Settings for the authenticated user.

        Selective Call Reject allows you to create customized rules to reject specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Indicates whether selective reject is enabled.
        :type enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        url = self.ep('settings/selectiveReject')
        super().put(url, json=body)

    def create_my_selective_reject_criteria(self, schedule_name: str, schedule_type: UserScheduleType,
                                            schedule_level: UserScheduleLevel,
                                            calls_from: PriorityAlertCriteriaGetCallsFrom, reject_enabled: bool,
                                            anonymous_callers_enabled: bool = None,
                                            unavailable_callers_enabled: bool = None,
                                            phone_numbers: list[str] = None) -> str:
        """
        Add User Selective Call Reject Criteria

        Create a new Selective Call Reject Criteria for the authenticated user.

        Selective Call Reject allows you to create customized rules to reject specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule_name: Name of the schedule associated with the criteria.
        :type schedule_name: str
        :param schedule_type: -
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: Specifies the type of calling numbers the criteria applies to, categorizing incoming data
            based on callsFrom types or numbers that match the current criteria.
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param reject_enabled: Determines whether selective call reject is applied for calls matching this criteria. If
            `true`, selective call reject is applied. Criteria with rejectEnabled set to false have precedence over
            criteria with rejectEnabled set to true.
        :type reject_enabled: bool
        :param anonymous_callers_enabled: When `true`, means this criteria applies for anonymous callers. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, means this criteria applies for unavailable callers. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: The list of phone numbers that will be checked against incoming calls for a match. Value
            for this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :rtype: str
        """
        body: dict[str, Any] = dict()
        body['scheduleName'] = schedule_name
        body['scheduleType'] = enum_str(schedule_type)
        body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['rejectEnabled'] = reject_enabled
        url = self.ep('settings/selectiveReject/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_my_selective_call_reject_criteria(self, id: str) -> None:
        """
        Delete a Selective Call Reject Criteria

        Delete a Selective Call Reject Criteria for the authenticated user.



        Selective Call Reject allows you to create customized rules to reject specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the selective call reject criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'settings/selectiveReject/criteria/{id}')
        super().delete(url)

    def get_my_selective_reject_criteria_settings(self, id: str) -> SelectiveRejectCallCriteriaGet:
        """
        Get Selective Call Reject Criteria Settings for User

        Get Selective Call Reject Criteria Settings for the authenticated user.

        Selective Call Reject allows you to create customized rules to reject specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param id: The `id` parameter specifies the unique identifier for the selective call reject criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :rtype: :class:`SelectiveRejectCallCriteriaGet`
        """
        url = self.ep(f'settings/selectiveReject/criteria/{id}')
        data = super().get(url)
        r = SelectiveRejectCallCriteriaGet.model_validate(data)
        return r

    def update_my_selective_call_reject_criteria_settings(self, id: str, schedule_name: str = None,
                                                          schedule_type: UserScheduleType = None,
                                                          schedule_level: UserScheduleLevel = None,
                                                          calls_from: PriorityAlertCriteriaGetCallsFrom = None,
                                                          anonymous_callers_enabled: bool = None,
                                                          unavailable_callers_enabled: bool = None,
                                                          phone_numbers: list[str] = None,
                                                          reject_enabled: bool = None) -> None:
        """
        Modify a Selective Call Reject Criteria

        Modify Selective Call Reject Criteria Settings for the authenticated user.



        Selective Call Reject allows you to create customized rules to reject specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the selective call reject. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :param schedule_name: Name of the schedule to be associated with the criteria.
        :type schedule_name: str
        :param schedule_type: Type of the schedule.
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: Specifies the type of calling numbers the criteria applies to, categorizing incoming data
            based on callsFrom types or numbers that match the current criteria.
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param anonymous_callers_enabled: When `true`, means this criteria applies for anonymous callers. Required if
            `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, means this criteria applies for unavailable callers. Required
            if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers to update for this criteria. Required if `callsFrom` is
            `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param reject_enabled: Determines whether selective call reject is applied for calls matching this criteria. If
            `true`, selective call reject is applied. Criteria with rejectEnabled set to false have precedence over
            criteria with rejectEnabled set to true.
        :type reject_enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if reject_enabled is not None:
            body['rejectEnabled'] = reject_enabled
        url = self.ep(f'settings/selectiveReject/criteria/{id}')
        super().put(url, json=body)

    def get_my_sequential_ring_settings(self) -> SequentialRingSettingsGet:
        """
        Get Sequential Ring Settings for User

        Get Sequential Ring Settings for the authenticated user.

        Sequential Ring allows calls to ring additional phone numbers in sequence if the initial call is not answered.
        This can be configured to ring up to five phone numbers with customizable ring patterns.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`SequentialRingSettingsGet`
        """
        url = self.ep('settings/sequentialRing')
        data = super().get(url)
        r = SequentialRingSettingsGet.model_validate(data)
        return r

    def update_my_sequential_ring_settings(self, enabled: bool, ring_base_location_first_enabled: bool = None,
                                           base_location_number_of_rings: int = None,
                                           continue_if_base_location_is_busy_enabled: bool = None,
                                           calls_to_voicemail_enabled: bool = None,
                                           phone_numbers: list[SequentialRingNumber] = None) -> None:
        """
        Modify Sequential Ring Settings for User

        Update Sequential Ring Settings for the authenticated user.

        Sequential Ring allows calls to ring additional phone numbers in sequence if the initial call is not answered.
        This can be configured to ring up to five phone numbers with customizable ring patterns.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Enable or disable sequential ring for the user.
        :type enabled: bool
        :param ring_base_location_first_enabled: When `true`, the user's own devices ring before sequential ring
            numbers.
        :type ring_base_location_first_enabled: bool
        :param base_location_number_of_rings: Number of rings for the user's own devices. Minimum: 2, Maximum: 20.
        :type base_location_number_of_rings: int
        :param continue_if_base_location_is_busy_enabled: When `true`, sequential ring continues even when the user is
            unavailable. It controls if we allow trying the sequential ring numbers when either a service for the user
            such as Do Not Disturb or Call Waiting sends the call to busy processing, or ringBaseLocationFirstEnabled
            is true but all the user's devices are unreachable.
        :type continue_if_base_location_is_busy_enabled: bool
        :param calls_to_voicemail_enabled: When `true`, the caller is provided the option to press the # key to end the
            sequential ring service and send the call to no answer handling such as voicemail.
        :type calls_to_voicemail_enabled: bool
        :param phone_numbers: List of phone numbers to ring sequentially. Maximum 5 phone numbers.
        :type phone_numbers: list[SequentialRingNumber]
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        if ring_base_location_first_enabled is not None:
            body['ringBaseLocationFirstEnabled'] = ring_base_location_first_enabled
        if base_location_number_of_rings is not None:
            body['baseLocationNumberOfRings'] = base_location_number_of_rings
        if continue_if_base_location_is_busy_enabled is not None:
            body['continueIfBaseLocationIsBusyEnabled'] = continue_if_base_location_is_busy_enabled
        if calls_to_voicemail_enabled is not None:
            body['callsToVoicemailEnabled'] = calls_to_voicemail_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = TypeAdapter(list[SequentialRingNumber]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('settings/sequentialRing')
        super().put(url, json=body)

    def create_my_sequential_ring_criteria(self, schedule_name: str, schedule_type: UserScheduleType,
                                           schedule_level: UserScheduleLevel,
                                           calls_from: PriorityAlertCriteriaGetCallsFrom, ring_enabled: bool,
                                           anonymous_callers_enabled: bool = None,
                                           unavailable_callers_enabled: bool = None,
                                           phone_numbers: list[str] = None) -> str:
        """
        Add User Sequential Ring Criteria

        Create a new Sequential Ring Criteria for the authenticated user.

        Sequential Ring criteria defines rules for when sequential ring should activate based on the caller and
        schedule.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule_name: Name of the schedule which determines when sequential ring is in effect.
        :type schedule_name: str
        :param schedule_type: -
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: Specifies the type of calling numbers the criteria applies to.
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param ring_enabled: Determines whether sequential ring is applied for calls matching this criteria. If `true`,
            sequential ring is applied. Criteria with ringEnabled set to false have precedence over criteria with
            ringEnabled set to true.
        :type ring_enabled: bool
        :param anonymous_callers_enabled: When `true`, means this criteria applies for anonymous callers. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, means this criteria applies for unavailable callers. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers that will be checked against incoming calls for a match. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :rtype: str
        """
        body: dict[str, Any] = dict()
        body['scheduleName'] = schedule_name
        body['scheduleType'] = enum_str(schedule_type)
        body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['ringEnabled'] = ring_enabled
        url = self.ep('settings/sequentialRing/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_my_sequential_ring_criteria(self, id: str) -> None:
        """
        Delete Sequential Ring Criteria

        Delete a Sequential Ring Criteria for the authenticated user.

        Sequential Ring criteria defines rules for when sequential ring should activate based on the caller and
        schedule.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the sequential ring criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'settings/sequentialRing/criteria/{id}')
        super().delete(url)

    def get_my_sequential_ring_criteria_settings(self, id: str) -> SequentialRingCriteriaGet:
        """
        Get Sequential Ring Criteria Settings for User

        Get Sequential Ring Criteria Settings for the authenticated user.

        Sequential Ring criteria defines rules for when sequential ring should activate based on the caller and
        schedule.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param id: The `id` parameter specifies the unique identifier for the sequential ring criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :rtype: :class:`SequentialRingCriteriaGet`
        """
        url = self.ep(f'settings/sequentialRing/criteria/{id}')
        data = super().get(url)
        r = SequentialRingCriteriaGet.model_validate(data)
        return r

    def update_my_sequential_ring_criteria_settings(self, id: str, schedule_name: str = None,
                                                    schedule_type: UserScheduleType = None,
                                                    schedule_level: UserScheduleLevel = None,
                                                    calls_from: PriorityAlertCriteriaGetCallsFrom = None,
                                                    anonymous_callers_enabled: bool = None,
                                                    unavailable_callers_enabled: bool = None,
                                                    phone_numbers: list[str] = None,
                                                    ring_enabled: bool = None) -> None:
        """
        Modify Sequential Ring Criteria Settings for User

        Update Sequential Ring Criteria Settings for the authenticated user.

        Sequential Ring criteria defines rules for when sequential ring should activate based on the caller and
        schedule.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the sequential ring criteria. Example:
            `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type id: str
        :param schedule_name: Name of the schedule to be associated with the criteria.
        :type schedule_name: str
        :param schedule_type: Type of the schedule.
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: Specifies the type of calling numbers the criteria applies to.
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param anonymous_callers_enabled: When `true`, means this criteria applies for anonymous callers. Required if
            `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, means this criteria applies for unavailable callers. Required
            if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: List of phone numbers to update for this criteria. Required if `callsFrom` is
            `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param ring_enabled: Determines whether sequential ring is applied for calls matching this criteria. If `true`,
            sequential ring is applied. Criteria with ringEnabled set to false have precedence over criteria with
            ringEnabled set to true.
        :type ring_enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if ring_enabled is not None:
            body['ringEnabled'] = ring_enabled
        url = self.ep(f'settings/sequentialRing/criteria/{id}')
        super().put(url, json=body)

    def get_my_simultaneous_ring_settings(self) -> SimultaneousRingGet:
        """
        Retrieve My Simultaneous Ring Settings

        Retrieve simultaneous ring settings for the authenticated user.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Schedules can also be set up to ring these phones during certain times of the day or days of
        the week.

        Retrieving settings requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`SimultaneousRingGet`
        """
        url = self.ep('settings/simultaneousRing')
        data = super().get(url)
        r = SimultaneousRingGet.model_validate(data)
        return r

    def update_my_simultaneous_ring_settings(self, enabled: bool = None, do_not_ring_if_on_call_enabled: bool = None,
                                             phone_numbers: list[SimultaneousRingNumber] = None,
                                             criterias_enabled: bool = None) -> None:
        """
        Modify My Simultaneous Ring Settings

        Modify simultaneous ring settings for the authenticated user.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Schedules can also be set up to ring these phones during certain times of the day or days of
        the week.

        Modifying settings requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Simultaneous Ring is enabled or not.
        :type enabled: bool
        :param do_not_ring_if_on_call_enabled: When set to `true`, the configured phone numbers won't ring when you are
            on a call.
        :type do_not_ring_if_on_call_enabled: bool
        :param phone_numbers: Enter up to 10 phone numbers to ring simultaneously when you receive an incoming call.
        :type phone_numbers: list[SimultaneousRingNumber]
        :param criterias_enabled: Controls whether the criteria for simultaneous ring are enabled.
        :type criterias_enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if do_not_ring_if_on_call_enabled is not None:
            body['doNotRingIfOnCallEnabled'] = do_not_ring_if_on_call_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = TypeAdapter(list[SimultaneousRingNumber]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        if criterias_enabled is not None:
            body['criteriasEnabled'] = criterias_enabled
        url = self.ep('settings/simultaneousRing')
        super().put(url, json=body)

    def create_my_simultaneous_ring_criteria(self, schedule_name: str, schedule_type: UserScheduleType,
                                             schedule_level: UserScheduleLevel,
                                             calls_from: PriorityAlertCriteriaGetCallsFrom, ring_enabled: bool,
                                             anonymous_callers_enabled: bool = None,
                                             unavailable_callers_enabled: bool = None,
                                             phone_numbers: list[str] = None) -> str:
        """
        Create My Simultaneous Ring Criteria

        Create simultaneous ring criteria settings for the authenticated user.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain
        times of the day or days of the week.

        Creating criteria requires a user auth token with a scope of `spark:telephony_config_write`.

        :param schedule_name: Name of the schedule which determines when the simultaneous ring is in effect.
        :type schedule_name: str
        :param schedule_type: -
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: -
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param ring_enabled: When set to `true` simultaneous ringing is enabled for calls that meet this criteria.
            Criteria with `ringEnabled` set to `false` take priority.
        :type ring_enabled: bool
        :param anonymous_callers_enabled: When `true`, the criteria applies to calls from anonymous callers. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, the criteria applies to calls from unavailable callers. Value
            for this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: The list of phone numbers that will checked against incoming calls for a match. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :rtype: str
        """
        body: dict[str, Any] = dict()
        body['scheduleName'] = schedule_name
        body['scheduleType'] = enum_str(schedule_type)
        body['scheduleLevel'] = enum_str(schedule_level)
        body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        body['ringEnabled'] = ring_enabled
        url = self.ep('settings/simultaneousRing/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_my_simultaneous_ring_criteria(self, id: str) -> None:
        """
        Delete My Simultaneous Ring Criteria

        Delete simultaneous ring criteria settings for the authenticated user.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain
        times of the day or days of the week.

        Deleting criteria requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: Unique identifier for the criteria.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'settings/simultaneousRing/criteria/{id}')
        super().delete(url)

    def get_my_simultaneous_ring_criteria(self, id: str) -> SequentialRingCriteriaGet:
        """
        Retrieve My Simultaneous Ring Criteria

        Retrieve simultaneous ring criteria settings for the authenticated user.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain
        times of the day or days of the week.

        Retrieving criteria requires a user auth token with a scope of `spark:telephony_config_read`.

        :param id: Unique identifier for the criteria.
        :type id: str
        :rtype: :class:`SequentialRingCriteriaGet`
        """
        url = self.ep(f'settings/simultaneousRing/criteria/{id}')
        data = super().get(url)
        r = SequentialRingCriteriaGet.model_validate(data)
        return r

    def update_my_simultaneous_ring_criteria(self, id: str, schedule_name: str = None,
                                             schedule_type: UserScheduleType = None,
                                             schedule_level: UserScheduleLevel = None,
                                             calls_from: PriorityAlertCriteriaGetCallsFrom = None,
                                             anonymous_callers_enabled: bool = None,
                                             unavailable_callers_enabled: bool = None,
                                             phone_numbers: list[str] = None, ring_enabled: bool = None) -> None:
        """
        Modify My Simultaneous Ring Criteria

        Modify simultaneous ring criteria settings for the authenticated user.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain
        times of the day or days of the week.

        Modifying criteria requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: Unique identifier for the criteria.
        :type id: str
        :param schedule_name: Name of the schedule which determines when the simultaneous ring is in effect.
        :type schedule_name: str
        :param schedule_type: -
        :type schedule_type: UserScheduleType
        :param schedule_level: -
        :type schedule_level: UserScheduleLevel
        :param calls_from: -
        :type calls_from: PriorityAlertCriteriaGetCallsFrom
        :param anonymous_callers_enabled: When `true`, the criteria applies to calls from anonymous callers. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type anonymous_callers_enabled: bool
        :param unavailable_callers_enabled: When `true`, the criteria applies to calls from unavailable callers. Value
            for this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type unavailable_callers_enabled: bool
        :param phone_numbers: The list of phone numbers that will checked against incoming calls for a match. Value for
            this attribute is required if `callsFrom` is `SELECT_PHONE_NUMBERS`.
        :type phone_numbers: list[str]
        :param ring_enabled: When set to `true` simultaneous ringing is enabled for calls that meet this criteria.
            Criteria with `ringEnabled` set to `false` take priority.
        :type ring_enabled: bool
        :rtype: None
        """
        body: dict[str, Any] = dict()
        if schedule_name is not None:
            body['scheduleName'] = schedule_name
        if schedule_type is not None:
            body['scheduleType'] = enum_str(schedule_type)
        if schedule_level is not None:
            body['scheduleLevel'] = enum_str(schedule_level)
        if calls_from is not None:
            body['callsFrom'] = enum_str(calls_from)
        if anonymous_callers_enabled is not None:
            body['anonymousCallersEnabled'] = anonymous_callers_enabled
        if unavailable_callers_enabled is not None:
            body['unavailableCallersEnabled'] = unavailable_callers_enabled
        if phone_numbers is not None:
            body['phoneNumbers'] = phone_numbers
        if ring_enabled is not None:
            body['ringEnabled'] = ring_enabled
        url = self.ep(f'settings/simultaneousRing/criteria/{id}')
        super().put(url, json=body)

    def upload_voicemail_busy_greeting(self, file: str) -> None:
        """
        Upload Voicemail Busy Greeting

        Uploads a new busy greeting audio file for the authenticated user's voicemail.

        This endpoint is part of the voicemail greeting management capabilities provided by the Webex Calling platform
        and is available when the `wxc-csg-hydra-call-184017-phase4` feature is enabled. The greeting must be in WAV
        format and not exceed 5000 kilobytes.

        Requires a user auth token with the `spark:telephony_config_write` scope. Only the authenticated user may
        upload greetings for their own voicemail.

        :param file: Greeting audio file in WAV format. Maximum file size is 5000 kilobytes.
        :type file: str
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['file'] = file
        url = self.ep('settings/voicemail/actions/busyGreetingUpload/invoke')
        super().post(url, json=body)

    def upload_voicemail_no_answer_greeting(self, file: str) -> None:
        """
        Upload Voicemail No Answer Greeting

        Uploads a new no answer greeting audio file for the authenticated user's voicemail.

        This endpoint is part of the voicemail greeting management capabilities provided by the Webex Calling platform
        and is available when the `wxc-csg-hydra-call-184017-phase4` feature is enabled. The greeting must be in WAV
        format and not exceed 5000 kilobytes.

        Requires a user auth token with the `spark:telephony_config_write` scope. Only the authenticated user may
        upload greetings for their own voicemail.

        :param file: Greeting audio file in WAV format. Maximum file size is 5000 kilobytes.
        :type file: str
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['file'] = file
        url = self.ep('settings/voicemail/actions/noAnswerGreetingUpload/invoke')
        super().post(url, json=body)

    def update_voicemail_pin(self, passcode: str) -> None:
        """
        Update Voicemail PIN

        Set the voicemail PIN for a person. Updates the PIN used to access voicemail messages. The PIN must comply with
        the passcode rules defined for the organization.

        The voicemail feature is part of Webex Calling, allowing users to secure their voicemail access with a PIN. The
        PIN is required to retrieve voice messages via phone.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param passcode: Person voicemail PIN. The PIN must comply with the passcode rules defined for the
            organization.
        :type passcode: str
        :rtype: None
        """
        body: dict[str, Any] = dict()
        body['passcode'] = passcode
        url = self.ep('voicemail/pin')
        super().put(url, json=body)

    def get_user_voicemail_rules(self) -> VoicemailRules:
        """
        Get Person's Voicemail Rules

        Get person's voicemail passcode rules. Voicemail rules specify the default passcode requirements. They are
        provided for informational purposes only and cannot be modified.

        The voicemail feature allows users to manage their voicemail settings as part of Webex Calling. Voicemail rules
        help ensure secure access to voice messages by defining passcode complexity requirements.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`VoicemailRules`
        """
        url = self.ep('voicemail/rules')
        data = super().get(url)
        r = VoicemailRules.model_validate(data)
        return r

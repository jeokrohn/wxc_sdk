from collections.abc import Generator
from datetime import time, date
from typing import Optional, List, Annotated

from pydantic import TypeAdapter, PlainSerializer

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.common import IdAndName
from wxc_sdk.common.schedules import ScheduleLevel
from wxc_sdk.person_settings.forwarding import CallForwardingCommon

__all__ = ['OperatingModesApi', 'Month',
           'DaySchedule',
           'DifferentHoursDaily', 'OperatingMode',
           'OperatingModeHoliday',
           'OperatingModeRecurrence', 'SameHoursDaily',
           'OperatingModeSchedule', 'OperatingModeRecurYearlyByDate',
           'OperatingModeRecurYearlyByDay', 'Day', 'Week']


class OperatingModeSchedule(str, Enum):
    #: Specifies the `operating mode` is active during the same hours daily (i.e., same schedule for Monday to Friday,
    #: and Saturday to Sunday).
    same_hours_daily = 'SAME_HOURS_DAILY'
    #: Specifies the `operating mode` is active during different hours for different days of the week.
    different_hours_daily = 'DIFFERENT_HOURS_DAILY'
    #: Specifies the `operating mode` is active during holidays with their own days, and recurrence.
    holiday = 'HOLIDAY'
    #: Specifies the `operating mode` doesn't have any schedules defined.
    none_ = 'NONE'


TimeHHMM = Annotated[time, PlainSerializer(lambda v: v.strftime('%H:%M') if v else None, return_type=str)]
DateYYYYMMDD = Annotated[date, PlainSerializer(lambda v: v.strftime('%Y-%m-%d') if v else None, return_type=str)]


class DaySchedule(ApiModel):
    #: Specifies if the `operating mode` schedule for the specified weekday(s) is enabled, or not. `False` if the flag
    #: is not set.
    enabled: Optional[bool] = None
    #: Specifies if the `operating mode` is enabled for the entire day. `False` if the flag is not set.
    all_day_enabled: Optional[bool] = None
    #: Start time for the `operating mode`.
    start_time: Optional[TimeHHMM] = None
    #: End time for the `operating mode`.
    end_time: Optional[TimeHHMM] = None


class SameHoursDaily(ApiModel):
    #: `Operating mode` schedule for Monday to Friday.
    monday_to_friday: Optional[DaySchedule] = None
    #: `Operating mode` schedule for Saturday to Sunday.
    saturday_to_sunday: Optional[DaySchedule] = None


class DifferentHoursDaily(ApiModel):
    #: `Operating mode` schedule for Sunday.
    sunday: Optional[DaySchedule] = None
    #: `Operating mode` schedule for Monday.
    monday: Optional[DaySchedule] = None
    #: `Operating mode` schedule for Tuesday.
    tuesday: Optional[DaySchedule] = None
    #: `Operating mode` schedule for Wednesday.
    wednesday: Optional[DaySchedule] = None
    #: `Operating mode` schedule for Thursday.
    thursday: Optional[DaySchedule] = None
    #: `Operating mode` schedule for Friday.
    friday: Optional[DaySchedule] = None
    #: `Operating mode` schedule for Saturday.
    saturday: Optional[DaySchedule] = None


class Month(str, Enum):
    #: Schedule the event in January.
    january = 'JANUARY'
    #: Schedule the event in February.
    february = 'FEBRUARY'
    #: Schedule the event in March.
    march = 'MARCH'
    #: Schedule the event in April.
    april = 'APRIL'
    #: Schedule the event in May.
    may = 'MAY'
    #: Schedule the event in June.
    june = 'JUNE'
    #: Schedule the event in July.
    july = 'JULY'
    #: Schedule the event in August.
    august = 'AUGUST'
    #: Schedule the event in September.
    september = 'SEPTEMBER'
    #: Schedule the event in October.
    october = 'OCTOBER'
    #: Schedule the event in November.
    november = 'NOVEMBER'
    #: Schedule the event in December.
    december = 'DECEMBER'

    @classmethod
    def from_index(cls, i: int) -> 'Week':
        return list(cls)[i]

    @classmethod
    def from_date(cls, d: date) -> 'Month':
        return cls.from_month(d.month)

    @classmethod
    def from_month(cls, m: int) -> 'Month':
        return cls.from_index(m - 1)


class OperatingModeRecurYearlyByDate(ApiModel):
    #: Schedule the event on a specific day of the month.
    day_of_month: Optional[int] = None
    #: Schedule the event on a specific month of the year.
    month: Optional[Month] = None


class Day(str, Enum):
    #: Schedule the event on Sunday.
    sunday = 'SUNDAY'
    #: Schedule the event on Monday.
    monday = 'MONDAY'
    #: Schedule the event on Tuesday.
    tuesday = 'TUESDAY'
    #: Schedule the event on Wednesday.
    wednesday = 'WEDNESDAY'
    #: Schedule the event on Thursday.
    thursday = 'THURSDAY'
    #: Schedule the event on Friday.
    friday = 'FRIDAY'
    #: Schedule the event on Saturday.
    saturday = 'SATURDAY'

    @classmethod
    def from_index(cls, i: int) -> 'Week':
        return list(cls)[i]


class Week(str, Enum):
    #: Schedule the event on the first week of the month.
    first = 'FIRST'
    #: Schedule the event on the second week of the month.
    second = 'SECOND'
    #: Schedule the event on the third week of the month.
    third = 'THIRD'
    #: Schedule the event on the fourth week of the month.
    fourth = 'FOURTH'
    #: Schedule the event on the last week of the month.
    last = 'LAST'

    @classmethod
    def from_index(cls, i: int) -> 'Week':
        return list(cls)[i]


class OperatingModeRecurYearlyByDay(ApiModel):
    #: Schedule the event on a specific day.
    day: Optional[Day] = None
    #: Schedule the event on a specific week.
    week: Optional[Week] = None
    #: Schedule the event on a specific month.
    month: Optional[Month] = None


class OperatingModeRecurrence(ApiModel):
    #: Recurrence definition yearly by date.
    recur_yearly_by_date: Optional[OperatingModeRecurYearlyByDate] = None
    #: Recurrence definition yearly by day.
    recur_yearly_by_day: Optional[OperatingModeRecurYearlyByDay] = None


class OperatingModeHoliday(ApiModel):
    #: A unique identifier for the holiday.
    id: Optional[str] = None
    #: Name of the holiday.
    name: Optional[str] = None
    #: Specifies if the `operating mode holiday` schedule event is enabled for the entire day. `False` if the flag is
    #: not set.
    all_day_enabled: Optional[bool] = None
    #: Start date of the `operating mode holiday`.
    start_date: Optional[DateYYYYMMDD] = None
    #: End date of the `operating mode holiday`.
    end_date: Optional[DateYYYYMMDD] = None
    #: Start time for the `operating mode holiday`. Mandatory if `allDayEnabled` is false.
    start_time: Optional[TimeHHMM] = None
    #: End time for the `operating mode holiday`. Mandatory if `allDayEnabled` is false.
    end_time: Optional[TimeHHMM] = None
    #: Recurrence configuration for the `operating mode holiday`.
    recurrence: Optional[OperatingModeRecurrence] = None

    def create_update(self) -> dict:
        """
        Data for create and update calls

        :meta private:
        """
        data = self.model_dump(mode='json', by_alias=True, exclude_unset=True)
        return data


class OperatingMode(ApiModel):
    #: A unique identifier for the `operating mode`.
    id: Optional[str] = None
    #: Unique name for the `operating mode`.
    name: Optional[str] = None
    #: Defines the scheduling of the `operating mode`.
    type: Optional[OperatingModeSchedule] = None
    #: Level at which the `operating mode` would be defined.
    level: Optional[ScheduleLevel] = None
    #: Location object having a unique identifier for the location, and its name. Mandatory if level is `LOCATION`.
    location: Optional[IdAndName] = None
    #: `Operating mode` schedule for same hours daily. Present if type is `SAME_HOURS_DAILY`.
    same_hours_daily: Optional[SameHoursDaily] = None
    #: `Operating mode` schedule for different hours daily. Present if type is `DIFFERENT_HOURS_DAILY`.
    different_hours_daily: Optional[DifferentHoursDaily] = None
    #: `Operating mode` schedule for holidays. Present if type is `HOLIDAY`.
    holidays: Optional[list[OperatingModeHoliday]] = None
    #: Call forwarding settings for an `operating mode`.
    call_forwarding: Optional[CallForwardingCommon] = None

    def create(self) -> dict:
        """
        Data for create calls

        :meta private:
        """
        data = self.model_dump(mode='json', by_alias=True, exclude_unset=True,
                               exclude={'id': True,
                                        'location': True,
                                        'holidays': {'__all__': {'id': True}}})
        if self.location:
            data['locationId'] = self.location.id
        return data

    def update(self) -> dict:
        """
        Data for update calls

        :meta private:
        """
        data = self.model_dump(mode='json', by_alias=True, exclude_unset=True,
                               exclude={'id': True,
                                        'location': True,
                                        'holidays': {'__all__': {'id': True}},
                                        'type': True,
                                        'level': True})
        return data


class OperatingModesApi(ApiChild, base='telephony/config'):
    """
    Schedule Based Routing with Operating Modes

    Features: `Operating modes` help manage calls more efficiently by routing them based on predefined settings.
    Authorized users can adjust these modes to reduce wait times for clients.
    `Operating modes` are used by mode-based forwarding for the `Auto Attendant`, `Call Queue`, and `Hunt Group`
    features.

    Viewing these read-only organization settings requires a full, read-only, or location administrator auth token with
    a scope of `spark-admin:telephony_config_read`.

    Modifying these organization settings requires a full, or location administrator auth token with a scope of
    `spark-admin:telephony_config_write`.

    A partner administrator can retrieve, or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def list(self, limit_to_location_id: str = None, name: str = None,
             limit_to_org_level_enabled: bool = None, order: str = None,
             org_id: str = None,
             **params) -> Generator[OperatingMode, None, None]:
        """
        Read the List of Operating Modes.

        Retrieve `Operating Modes` list defined at location, or organization level. Use query parameters to filter the
        result set by location or level. The list returned is sorted in ascending order by operating mode name. Long
        result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        `Operating modes` help manage calls more efficiently by routing them based on predefined settings.

        Retrieving this list requires a full, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param limit_to_location_id: Location query parameter to filter the `operating modes` from that location only.
        :type limit_to_location_id: str
        :param name: List `operating modes` whose name contains this string.
        :type name: str
        :param limit_to_org_level_enabled: If true, only return `operating modes` defined at the organization level.
        :type limit_to_org_level_enabled: bool
        :param order: Sort the list of `operating modes` based on `name`, either asc, or desc.
        :type order: str
        :param org_id: Retrieve `operating modes` list from this organization.
        :type org_id: str
        :return: Generator yielding :class:`OperatingMode` instances
        """
        if name is not None:
            params['name'] = name
        if limit_to_location_id is not None:
            params['limitToLocationId'] = limit_to_location_id
        if limit_to_org_level_enabled is not None:
            params['limitToOrgLevelEnabled'] = str(limit_to_org_level_enabled).lower()
        if order is not None:
            params['order'] = order
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('operatingModes')
        return self.session.follow_pagination(url=url, model=OperatingMode, item_key='operatingModes',
                                              params=params)

    def details(self, mode_id: str, org_id: str = None) -> OperatingMode:
        """
        Get Details for an Operating Mode.

        Retrieve an `Operating Mode` by `Operating Mode ID`.

        `Operating modes` can be used to define call routing rules for different scenarios like business hours, after
        hours, holidays, etc.

        Retrieving an `operating mode` requires a full, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param mode_id: Get the `operating mode` with the matching ID.
        :type mode_id: str
        :param org_id: Get the `operating mode` from this organization.
        :type org_id: str
        :rtype: :class:`OperatingMode`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'operatingModes/{mode_id}')
        data = super().get(url, params=params)
        r = OperatingMode.model_validate(data)
        return r

    def create(self, settings: OperatingMode, org_id: str = None) -> str:
        """
        Create an Operating Mode.

        Create an `Operating Mode` at an organization, or a location level.

        `Operating modes` can be used to define call routing rules for different scenarios like business hours, after
        hours, holidays, etc.

        Creating an `Operating Mode` requires a full, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param settings: Create the `operating mode` with these settings. At least name, type and level must be set.
        :type settings: OperatingMode
        :param org_id: Create the `operating mode` for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {'orgId': org_id} if org_id else None
        body = settings.create()
        url = self.ep('operatingModes')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def update(self, mode_id: str, settings: OperatingMode, org_id: str = None):
        """
        Modify an Operating Mode.

        Modify the designated `Operating Mode's` configuration.

        `Operating modes` can be used to define call routing rules for different scenarios like business hours, after
        hours, holidays, etc.

        Modifying an `Operating Mode` requires a full, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param mode_id: Modify the `operating mode` with the matching ID.
        :type mode_id: str
        :param settings: Modify the `operating mode` with these settings.
        :type settings: OperatingMode
        :param org_id: Modify the `operating mode` from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {'orgId': org_id} if org_id else None
        body = settings.update()
        mode_id = mode_id or settings.id
        url = self.ep(f'operatingModes/{mode_id}')
        super().put(url, params=params, json=body)

    def delete(self, mode_id: str, org_id: str = None):
        """
        Delete an Operating Mode.

        Delete the designated `Operating Mode`.

        Deleting an `Operating Mode` requires a full, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param mode_id: Delete the `operating mode` with the matching ID.
        :type mode_id: str
        :param org_id: Delete the `operating mode` from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'operatingModes/{mode_id}')
        super().delete(url, params=params)

    def holiday_details(self, mode_id: str, holiday_id: str,
                        org_id: str = None) -> OperatingModeHoliday:
        """
        Get details for an Operating Mode Holiday.

        Retrieve an `Operating Mode Holiday` by ID.

        Holidays define a recurring schedule for the `Operating Modes`.

        Retrieving an `Operating Mode Holiday` requires a full, read-only, or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param mode_id: Get the holiday from this `operating mode` matching ID.
        :type mode_id: str
        :param holiday_id: Get the `operating mode Holiday` with the matching ID.
        :type holiday_id: str
        :param org_id: Get the `operating mode` from this organization.
        :type org_id: str
        :rtype: :class:`OperatingModeHoliday`
        """
        params = {'orgId': org_id} if org_id else None
        url = self.ep(f'operatingModes/{mode_id}/holidays/{holiday_id}')
        data = super().get(url, params=params)
        r = OperatingModeHoliday.model_validate(data)
        return r

    def holiday_create(self, mode_id: str, settings: OperatingModeHoliday, org_id: str = None) -> str:
        """
        Create an Operating Mode Holiday.

        Create a holiday schedule event for the designated `Operating Mode`.

        Holidays define a recurring schedule for the `Operating Modes`. An `Operating Mode` can have a max of 150
        holidays.

        Creating an `Operating Mode Holiday` requires a full, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param mode_id: Create the holiday for this `operating mode`.
        :type mode_id: str
        :param settings: Create the `operating mode holiday` with these settings.
        :type settings: OperatingModeHoliday
        :param org_id: Create the `operating mode holiday` for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {'orgId': org_id} if org_id else None
        body = settings.create_update()
        url = self.ep(f'operatingModes/{mode_id}/holidays')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def holiday_update(self, mode_id: str, holiday_id: str, settings: OperatingModeHoliday, org_id: str = None):
        """
        Modify an Operating Mode Holiday.

        Modify the designated `Operating Mode Holiday's` configuration.

        Modifying an `Operating Mode Holiday` requires a full, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param mode_id: Modify the holiday from this `operating mode` matching ID.
        :type mode_id: str
        :param holiday_id: Modify the `Holiday` with the matching ID.
        :type holiday_id: str
        :param settings: Modify the `operating mode holiday` with these settings.
        :type settings: OperatingModeHoliday
        :param org_id: Modify the `operating mode` from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {'orgId': org_id} if org_id else None
        holiday_id = holiday_id or settings.id
        body = settings.create_update()
        url = self.ep(f'operatingModes/{mode_id}/holidays/{holiday_id}')
        super().put(url, params=params, json=body)

    def holiday_delete(self, mode_id: str, holiday_id: str = None, org_id: str = None):
        """
        Delete an Operating Mode Holiday.

        Delete the designated `Operating Mode Holiday`.

        Deleting an `Operating Mode Holiday` requires a full, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param mode_id: Delete the holiday from this `operating mode` matching ID.
        :type mode_id: str
        :param holiday_id: Delete the holiday with the matching ID.
        :type holiday_id: str
        :param org_id: Delete the `operating mode` from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'operatingModes/{mode_id}/holidays/{holiday_id}')
        super().delete(url, params=params)

    def available_operating_modes(self, location_id: str,
                                  org_id: str = None) -> List[IdAndName]:
        """
        Retrieve the List of Available Operating Modes in a Location.

        Retrieve list of `Operating Modes` which are available to be assigned to a location level feature (`Auto
        Attendant`, `Call Queue`, or `Hunt Group`). Since each location and an org can have a max of 100 `Operating
        Modes` defined. The max number of `operating modes` that can be returned is 200.

        `Operating modes` can be used to define call routing rules for different scenarios like business hours, after
        hours, holidays, etc. for the `Auto Attendant`, `Call Queue`, and `Hunt Group` features.

        Retrieving this list requires a full, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Retrieve `operating modes` list from this location.
        :type location_id: str
        :param org_id: Retrieve `operating modes` list from this organization.
        :type org_id: str
        :rtype: list[IdAndName]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/operatingModes/availableOperatingModes')
        data = super().get(url, params=params)
        r = TypeAdapter(list[IdAndName]).validate_python(data['operatingModes'])
        return r

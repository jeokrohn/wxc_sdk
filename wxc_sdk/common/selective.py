from typing import Optional, ClassVar, Any

from pydantic import model_validator

from wxc_sdk.base import SafeEnum as Enum, ApiModel
from wxc_sdk.common.schedules import ScheduleType

__all__ = ['SelectiveScheduleLevel', 'SelectiveFrom', 'SelectiveCriteria', 'SelectiveSource', 'SelectiveCrit']


class SelectiveScheduleLevel(str, Enum):
    #: Indicates schedule specified is of `GROUP` level.
    group = 'GROUP'
    global_ = 'GLOBAL'


class SelectiveFrom(str, Enum):
    #: Criteria applies to all incoming numbers.
    any_phone_number = 'ANY_PHONE_NUMBER'
    #: Criteria applies only for specific incoming numbers.
    select_phone_numbers = 'SELECT_PHONE_NUMBERS'


class SelectiveCriteria(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the sequential ring is in effect. Creating criteria
    #: without schedule_name nor schedule_type creates a criteria for all hours all days
    schedule_name: Optional[str] = None
    #: This indicates the type of schedule. Creating criteria without schedule_name nor schedule_type creates a
    #: criteria for all hours all days
    schedule_type: Optional[ScheduleType] = None
    #: This indicates the level of the schedule specified by `scheduleName`.
    schedule_level: Optional[SelectiveScheduleLevel] = None
    #: This indicates if criteria are applicable for calls from any phone number or selected phone numbers.
    calls_from: Optional[SelectiveFrom] = None
    #: When `true` incoming calls from private numbers are allowed. This is only applicable when `callsFrom` is set to
    #: `SELECT_PHONE_NUMBERS`.
    anonymous_callers_enabled: Optional[bool] = None
    #: When `true` incoming calls from unavailable numbers are allowed. This is only applicable when `callsFrom` is set
    #: to `SELECT_PHONE_NUMBERS`.
    unavailable_callers_enabled: Optional[bool] = None
    #: When callsFrom is set to `SELECT_PHONE_NUMBERS`, indicates a list of incoming phone numbers for which the
    #: criteria apply.
    phone_numbers: Optional[list[str]] = None
    #: When set to `true` selective treatment enabled for calls that meet the current criteria. Criteria with
    #: `enabled` set to `false` take priority.
    enabled: Optional[bool] = None

    # attribute for enabled
    _enabled_attr: ClassVar[str] = None
    # attribute for phone number list
    _phone_numbers: ClassVar[str] = None

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        """
        Verify that the class has the required attributes
        """
        super().__pydantic_init_subclass__(**kwargs)
        if cls._enabled_attr is None:
            raise TypeError('_enabled_attr has to be defined')
        if cls._phone_numbers is None:
            raise TypeError('_phone_numbers has to be defined')

    @model_validator(mode='before')
    @classmethod
    def val_enabled(cls, data: dict) -> dict:
        """
        this class is used for multiple selective cases where there are different *_enabled fields.
            * ring_enabled
            * accept_enabled
            * forward_enabled
        also the attribute phone_numbers in one case is called numbers.

        This is to "normalize the data before validation"

        :meta private:
        """
        if cls == SelectiveCriteria:
            raise TypeError(f'{cls.__name__} is not meant to be used directly. You can only instantiate subclasses.')
        if cls._enabled_attr in data:
            data['enabled'] = data.pop(cls._enabled_attr)
        if cls._phone_numbers in data:
            data['phoneNumbers'] = data.pop(cls._phone_numbers)
        return data

    def update(self) -> dict:
        """
        data for update

        :meta private:
        """
        data = self.model_dump(mode='json', by_alias=True, exclude_none=True,
                               exclude={'id'})
        if 'enabled' in data:
            data[self._enabled_attr] = data.pop('enabled')
        if 'phoneNumbers' in data:
            data[self._phone_numbers] = data.pop('phoneNumbers')
        return data


class SelectiveSource(str, Enum):
    #: Criteria applies to all incoming numbers.
    all_numbers = 'ALL_NUMBERS'
    #: Criteria applies only for specific incoming numbers.
    specific_numbers = 'SPECIFIC_NUMBERS'


class SelectiveCrit(ApiModel):
    #: Unique identifier for criteria.
    id: Optional[str] = None
    #: Name of the location's schedule which determines when the sequential ring is in effect.
    schedule_name: Optional[str] = None
    #: Indicates if criteria are applicable for calls from any phone number or specific phone number.
    source: Optional[SelectiveSource] = None
    #: When set to `true` selective treatment is enabled for calls that meet the current criteria. Criteria with
    #: `enabled` set to `false` take priority.
    enabled: Optional[bool] = None

    @model_validator(mode='before')
    @classmethod
    def val_enabled(cls, data: dict) -> dict:
        """
        'enabled' is actually something like *_enabled.

        This is to "normalize the data before validation"

        :meta private:
        """
        enabled_attr = next(enabled_attr for enabled_attr in data if enabled_attr.endswith('Enabled'))
        data['enabled'] = data.pop(enabled_attr)
        return data

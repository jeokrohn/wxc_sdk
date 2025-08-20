from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CallSettingsForMeApi', 'PersonalAssistantGet', 'PersonalAssistantGetAlerting',
           'PersonalAssistantGetPresence']


class PersonalAssistantGetPresence(str, Enum):
    #: User is available.
    none_ = 'NONE'
    #: User is gone for a business trip.
    business_trip = 'BUSINESS_TRIP'
    #: User is gone for the day.
    gone_for_the_day = 'GONE_FOR_THE_DAY'
    #: User is gone for lunch.
    lunch = 'LUNCH'
    #: User is gone for a meeting.
    meeting = 'MEETING'
    #: User is out of office.
    out_of_office = 'OUT_OF_OFFICE'
    #: User is temporarily out.
    temporarily_out = 'TEMPORARILY_OUT'
    #: User is gone for training.
    training = 'TRAINING'
    #: User is unavailable.
    unavailable = 'UNAVAILABLE'
    #: User is gone for vacation.
    vacation = 'VACATION'


class PersonalAssistantGetAlerting(str, Enum):
    #: Ring the recipient first.
    alert_me_first = 'ALERT_ME_FIRST'
    #: Reminder ring the recipient.
    play_ring_reminder = 'PLAY_RING_REMINDER'
    #: No alert.
    none_ = 'NONE'


class PersonalAssistantGet(ApiModel):
    #: Toggles feature.
    enabled: Optional[bool] = None
    #: Person's availability.
    presence: Optional[PersonalAssistantGetPresence] = None
    #: The date until which personal assistant is active.
    until_date_time: Optional[datetime] = None
    #: Toggle the option to transfer to another number.
    transfer_enabled: Optional[bool] = None
    #: Number to transfer to.
    transfer_number: Optional[str] = None
    #: Alert type.
    alerting: Optional[PersonalAssistantGetAlerting] = None
    #: Number of rings for alert type: `ALERT_ME_FIRST`; available range is 2-20
    alert_me_first_number_of_rings: Optional[int] = None


class CallSettingsForMeApi(ApiChild, base='telephony/config/people/me/settings'):
    """
    Call Settings For Me
    
    Call settings for me APIs allow a person to read or modify their settings.
    
    Viewing settings requires a user auth token with a scope of `spark:telephony_config_read`.
    
    Configuring settings requires a user auth token with a scope of `spark:telephony_config_write`.
    """

    def get_my_personal_assistant(self) -> PersonalAssistantGet:
        """
        Get My Personal Assistant

        Retrieve user's own Personal Assistant details.

        Personal Assistant is used to manage a user's incoming calls when they are away.

        Retrieving Personal Assistant details requires a user auth token with `spark:telephony_config_read`.

        :rtype: :class:`PersonalAssistantGet`
        """
        url = self.ep('personalAssistant')
        data = super().get(url)
        r = PersonalAssistantGet.model_validate(data)
        return r

    def update_my_personal_assistant(self, enabled: bool = None, presence: PersonalAssistantGetPresence = None,
                                     until_date_time: Union[str, datetime] = None, transfer_enabled: bool = None,
                                     transfer_number: str = None, alerting: PersonalAssistantGetAlerting = None,
                                     alert_me_first_number_of_rings: int = None):
        """
        Update My Personal Assistant

        Update user's own Personal Assistant details.

        Personal Assistant is used to manage a user's incoming calls when they are away.

        Updating Personal Assistant details requires a auth token with the `spark:telephony_config_write`.

        :param enabled: Toggles feature.
        :type enabled: bool
        :param presence: Person's availability.
        :type presence: PersonalAssistantGetPresence
        :param until_date_time: The date until which the personal assistant is active.
        :type until_date_time: Union[str, datetime]
        :param transfer_enabled: Toggle the option to transfer to another number.
        :type transfer_enabled: bool
        :param transfer_number: Number to transfer to.
        :type transfer_number: str
        :param alerting: Alert type.
        :type alerting: PersonalAssistantGetAlerting
        :param alert_me_first_number_of_rings: Number of rings for alert type: ALERT_ME_FIRST; available range is 2-20.
        :type alert_me_first_number_of_rings: int
        :rtype: None
        """
        body = dict()
        if enabled is not None:
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
        url = self.ep('personalAssistant')
        super().put(url, json=body)

    def get_my_webex_go_override_settings(self) -> bool:
        """
        Get My WebexGoOverride Settings

        Retrieve "Mobile User Aware" override setting for Do Not Disturb feature.

        When enabled, a mobile device will still ring even if Do Not Disturb, Quiet Hours, or Presenting Status are
        enabled.

        When disabled, a mobile device will return busy for all incoming calls if Do Not Disturb, Quiet Hours, or
        Presenting Status are enabled.

        It requires a user auth token with `spark:telephony_config_read` scope.

        :rtype: bool
        """
        url = self.ep('webexGoOverride')
        data = super().get(url)
        r = data['enabled']
        return r

    def update_my_webex_go_override_settings(self, enabled: bool = None):
        """
        Update My WebexGoOverride Settings

        Update "Mobile User Aware" override setting for Do Not Disturb feature.

        When enabled, a mobile device will still ring even if Do Not Disturb, Quiet Hours, or Presenting Status are
        enabled.

        When disabled, a mobile device will return busy for all incoming calls if Do Not Disturb, Quiet Hours, or
        Presenting Status are enabled.

        It requires a user auth token with the `spark:telephony_config_write` scope.

        :param enabled: True if the "Mobile User Aware" override setting for Do Not Disturb feature is enabled.
        :type enabled: bool
        :rtype: None
        """
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        url = self.ep('webexGoOverride')
        super().put(url, json=body)

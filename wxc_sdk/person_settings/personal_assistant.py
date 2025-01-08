from datetime import datetime
from typing import Optional, Union

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import SafeEnum as Enum, ApiModel, enum_str

__all__ = ['PersonalAssistantPresence', 'PersonalAssistantAlerting', 'PersonalAssistant', 'PersonalAssistantApi']

class PersonalAssistantPresence(str, Enum):
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


class PersonalAssistantAlerting(str, Enum):
    #: Ring the recipient first.
    alert_me_first = 'ALERT_ME_FIRST'
    #: Reminder ring the recipient.
    play_ring_reminder = 'PLAY_RING_REMINDER'
    #: No alert.
    none_ = 'NONE'


class PersonalAssistant(ApiModel):
    #: Toggles feature.
    enabled: Optional[bool] = None
    #: Person's availability.
    presence: Optional[PersonalAssistantPresence] = None
    #: The date until which personal assistant is active.
    until_date_time: Optional[datetime] = None
    #: Toggle the option to transfer to another number.
    transfer_enabled: Optional[bool] = None
    #: Number to transfer to.
    transfer_number: Optional[str] = None
    #: Alert type.
    alerting: Optional[PersonalAssistantAlerting] = None
    #: Number of rings for alert type: `ALERT_ME_FIRST`; available range is 0-20
    alert_me_first_number_of_rings: Optional[int] = None


class PersonalAssistantApi(ApiChild, base=''):
    """
    API for personal assistant settings

    """

    def get(self, person_id: str, org_id: str = None) -> PersonalAssistant:
        """
        Get Personal Assistant

        Retrieve Personal Assistant details for a specific user.

        Personal Assistant is used to manage a user's incoming calls when they are away.

        Retrieving Personal Assistant details requires a full, user, or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Get Personal Assistant details for the organization.
        :type org_id: str
        :rtype: :class:`PersonalAssistant`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/people/{person_id}/features/personalAssistant')
        data = super().get(url, params=params)
        r = PersonalAssistant.model_validate(data)
        return r

    def update(self, person_id: str, enabled: bool = None,
               presence: PersonalAssistantPresence = None,
               until_date_time: Union[str, datetime] = None, transfer_enabled: bool = None, transfer_number: str = None,
               alerting: PersonalAssistantAlerting = None,
               alert_me_first_number_of_rings: int = None, org_id: str = None):
        """
        Update Personal Assistant

        Update Personal Assistant details for a specific user.

        Personal Assistant is used to manage a user's incoming calls when they are away.

        Updating Personal Assistant details requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: Toggles feature.
        :type enabled: bool
        :param presence: Person's availability.
        :type presence: PersonalAssistantPresence
        :param until_date_time: The date until which the personal assistant is active.
        :type until_date_time: Union[str, datetime]
        :param transfer_enabled: Toggle the option to transfer to another number.
        :type transfer_enabled: bool
        :param transfer_number: Number to transfer to.
        :type transfer_number: str
        :param alerting: Alert type.
        :type alerting: PersonalAssistantAlerting
        :param alert_me_first_number_of_rings: Number of rings for alert type: ALERT_ME_FIRST; available range is 0-20.
        :type alert_me_first_number_of_rings: int
        :param org_id: Update Personal Assistant details for the organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
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
        url = self.ep(f'telephony/config/people/{person_id}/features/personalAssistant')
        super().put(url, params=params, json=body)

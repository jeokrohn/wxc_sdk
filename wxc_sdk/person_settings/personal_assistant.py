from datetime import datetime
from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum

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
    #: Ring the user's phone first before the personal assistant takes over.
    alert_me_first = 'ALERT_ME_FIRST'
    #: Play a ring reminder to the user.
    play_ring_reminder = 'PLAY_RING_REMINDER'
    #: No alerting..
    none_ = 'NONE'


class PersonalAssistant(ApiModel):
    #: Enable/Disable the personal assistant feature.
    enabled: Optional[bool] = None
    #: Presence status that triggers the personal assistant..
    presence: Optional[PersonalAssistantPresence] = None
    #: Date and time until which the personal assistant is active (ISO 8601 format).
    until_date_time: Optional[datetime] = None
    #: Enable/Disable call transfer when personal assistant is active.
    transfer_enabled: Optional[bool] = None
    #: Phone number to transfer calls to when transfer is enabled.
    transfer_number: Optional[str] = None
    #: Alerting behavior for incoming calls when personal assistant is active. Possible values:
    #: ALERT_ME_FIRST - Ring
    #: the user's phone first before the personal assistant takes over. PLAY_RING_REMINDER - Play a ring reminder to
    #: the user. NONE - No alerting..
    alerting: Optional[PersonalAssistantAlerting] = None
    #: Number of rings before transferring the call when alerting is set to ALERT_ME_FIRST.
    alert_me_first_number_of_rings: Optional[int] = None


class PersonalAssistantApi(ApiChild, base=''):
    """
    API for personal assistant settings

    """

    def get(self, person_id: str, org_id: str = None) -> PersonalAssistant:  # type: ignore[override]
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

    def update(self, person_id: str, settings: PersonalAssistant, org_id: str = None):
        """
        Update Personal Assistant

        Update Personal Assistant details for a specific user.

        Personal Assistant is used to manage a user's incoming calls when they are away.

        Updating Personal Assistant details requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: Personal Assistant settings.
        :type settings: PersonalAssistant
        :param org_id: Update Personal Assistant details for the organization.
        :type org_id: str
        :rtype: None
        """
        params = {'orgId': org_id} if org_id is not None else None
        body = settings.model_dump(mode='json', exclude_unset=True, by_alias=True)
        url = self.ep(f'telephony/config/people/{person_id}/features/personalAssistant')
        super().put(url, params=params, json=body)

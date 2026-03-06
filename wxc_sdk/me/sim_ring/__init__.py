from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, E164Number
from wxc_sdk.common.selective import SelectiveCrit

__all__ = ['MeSimRingApi', 'MeSimRingNumber', 'MeSimRing']

from wxc_sdk.person_settings.sim_ring import SimRingCriteria


class MeSimRingNumber(ApiModel):
    #: Phone number set for simultaneous ring.
    phone_number: Optional[E164Number] = None
    #: When set to `true`, the called party is required to press any key on the keypad to confirm answer for the call.
    answer_confirmation_enabled: Optional[bool] = None


class MeSimRing(ApiModel):
    #: Simultaneous Ring is enabled or not.
    enabled: Optional[bool] = None
    #: When set to `true`, the configured phone numbers won't ring when on a call.
    do_not_ring_if_on_call_enabled: Optional[bool] = None
    #: Enter up to 10 phone numbers to ring simultaneously when workspace phone receives an incoming call.
    phone_numbers: Optional[list[MeSimRingNumber]] = None
    #: A list of criteria specifying conditions when simultaneous ring is in effect.
    criteria: Optional[list[SelectiveCrit]] = None
    #: When `true`, enables the selected schedule for simultaneous ring.
    criterias_enabled: Optional[bool] = None

    def update(self) -> dict:
        """
        Data for update

        :meta private
        """
        return self.model_dump(mode='json', by_alias=True, exclude_none=True,
                               exclude={'criteria'})


class MeSimRingApi(ApiChild, base='telephony/config/people/me'):
    def get(self) -> MeSimRing:
        """
        Retrieve My Simultaneous Ring Settings

        Retrieve simultaneous ring settings for the authenticated user.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously. Schedules can also be set up to ring these phones during certain times of the day or days of
        the week.

        Retrieving settings requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`MeSimRing`
        """
        url = self.ep('settings/simultaneousRing')
        data = super().get(url)
        r = MeSimRing.model_validate(data)
        return r

    def update(self, settings: MeSimRing) -> None:
        """
        Modify My Simultaneous Ring Settings

        Modify simultaneous ring settings for the authenticated user.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your
        choice to ring
        simultaneously. Schedules can also be set up to ring these phones during certain times of the
        day or days of
        the week.

        Modifying settings requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: new sim ring settings
        :rtype: None
        """
        body = settings.update()
        url = self.ep('settings/simultaneousRing')
        super().put(url, json=body)

    def criteria_create(self, criteria: SimRingCriteria) -> str:
       """
       Create My Simultaneous Ring Criteria

       Create simultaneous ring criteria settings for the authenticated user.

       The Simultaneous Ring feature allows you to configure your office phone and other phones of your
       choice to ring
       simultaneously. Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones
       during certain
       times of the day or days of the week.

       Creating criteria requires a user auth token with a scope of `spark:telephony_config_write`.

       :param criteria: new sim ring criteria
       :type criteria: :class:`MeSimRingCriteria`
       :rtype: str
       """
       body = criteria.update()
       url = self.ep('settings/simultaneousRing/criteria')
       data = super().post(url, json=body)
       r = data['id']
       return r

    def criteria_delete(self, criteria_id: str):
       """
       Delete My Simultaneous Ring Criteria

       Delete simultaneous ring criteria settings for the authenticated user.

       The Simultaneous Ring feature allows you to configure your office phone and other phones of your
       choice to ring simultaneously. Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones
       during certain times of the day or days of the week.

       Deleting criteria requires a user auth token with a scope of `spark:telephony_config_write`.

       :param criteria_id: Unique identifier for the criteria.
       :type criteria_id: str
       :rtype: None
       """
       url = self.ep(f'settings/simultaneousRing/criteria/{criteria_id}')
       super().delete(url)

    def criteria_get(self, criteria_id: str) -> SimRingCriteria:
       """
       Retrieve My Simultaneous Ring Criteria

       Retrieve simultaneous ring criteria settings for the authenticated user.

       The Simultaneous Ring feature allows you to configure your office phone and other phones of your
       choice to ring simultaneously. Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones
       during certain times of the day or days of the week.

       Retrieving criteria requires a user auth token with a scope of `spark:telephony_config_read`.

       :param criteria_id: Unique identifier for the criteria.
       :type criteria_id: str
       :rtype: :class:`SimRingCriteria`
       """
       url = self.ep(f'settings/simultaneousRing/criteria/{criteria_id}')
       data = super().get(url)
       r = SimRingCriteria.model_validate(data)
       return r

    def criteria_update(self, criteria: SimRingCriteria, criteria_id: str=None):
        """
        Modify My Simultaneous Ring Criteria

        Modify simultaneous ring criteria settings for the authenticated user.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your
        choice to ring
        simultaneously. Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones
        during certain
        times of the day or days of the week.

        Modifying criteria requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria: new settings
        :type criteria: :class:`SimRingCriteria`
        :param criteria_id: Unique identifier for the criteria. Default: id from criteria
        :type criteria_id: str
        :rtype: None
        """
        criteria_id = criteria_id or criteria.id
        body = criteria.update()
        url = self.ep(f'settings/simultaneousRing/criteria/{criteria_id}')
        super().put(url, json=body)

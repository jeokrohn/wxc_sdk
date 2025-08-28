from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.person_settings.single_number_reach import SingleNumberReachNumber

__all__ = ['MeSNRApi', 'MeSNRSettings']


class MeSNRSettings(ApiModel):
    #: If `true`, the Single Number Reach feature is enabled.
    enabled: Optional[bool] = None
    #: If `true`, all locations will be alerted for click-to-dial calls.
    alert_all_locations_for_click_to_dial_calls_enabled: Optional[bool] = None
    #: If `true`, all locations will be alerted for group paging calls.
    alert_all_locations_for_group_paging_calls_enabled: Optional[bool] = None
    #: List of numbers configured for Single Number Reach.
    numbers: Optional[list[SingleNumberReachNumber]] = None


class MeSNRApi(ApiChild, base='telephony/config/people/me'):

    def settings(self) -> MeSNRSettings:
        """
        Get User's Single Number Reach Settings

        Retrieves all single number reach settings configured for the authenticated user.

        The "Single Number Reach" feature in Webex allows users to access their business phone capabilities from any
        device, making it easy to make and receive calls as if at their office. This is especially useful for remote
        or mobile workers needing flexibility.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`MeSNRSettings`
        """
        url = self.ep('settings/singleNumberReach')
        data = super().get(url)
        r = MeSNRSettings.model_validate(data)
        return r

    def update(self, alert_all_locations_for_click_to_dial_calls_enabled: bool = None):
        """
        Update User's Single Number Reach Settings

        Updates single number reach settings associated with the authenticated user.

        The "Single Number Reach" feature in Webex allows users to access their business phone capabilities from any
        device, making it easy to make and receive calls as if at their office. This is especially useful for remote
        or mobile workers needing flexibility.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param alert_all_locations_for_click_to_dial_calls_enabled: If `true`, all locations will be alerted for
            click-to-dial calls.
        :type alert_all_locations_for_click_to_dial_calls_enabled: bool
        :rtype: None
        """
        body = dict()
        if alert_all_locations_for_click_to_dial_calls_enabled is not None:
            body['alertAllLocationsForClickToDialCallsEnabled'] = alert_all_locations_for_click_to_dial_calls_enabled
        url = self.ep('settings/singleNumberReach')
        super().put(url, json=body)

    def create_snr(self, settings: SingleNumberReachNumber) -> str:
        """
        Add phone number as User's Single Number Reach

        Add a phone number as a single number reach for the authenticated user.

        The "Single Number Reach" feature in Webex allows users to access their business phone capabilities from any
        device, making it easy to make and receive calls as if at their office. This is especially useful for remote
        or mobile workers needing flexibility.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: User's Single Number Reach Settings
        :type settings: :class:`SingleNumberReachNumber`
        :return: Unique identifier of the phone number.
        :rtype: str
        """
        body = settings.create_update()
        url = self.ep('settings/singleNumberReach/numbers')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_snr(self, phone_number_id: str):
        """
        Delete User's Single Number Reach Contact Settings

        Delete contact settings associated with the authenticated user.

        The "Single Number Reach" feature in Webex allows users to access their business phone capabilities from any
        device, making it easy to make and receive calls as if at their office. This is especially useful for remote
        or mobile workers needing flexibility.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param phone_number_id: Unique identifier of the phone number.
        :type phone_number_id: str
        :rtype: None
        """
        url = self.ep(f'settings/singleNumberReach/numbers/{phone_number_id}')
        super().delete(url)

    def update_snr(self, phone_number_id: str, settings: SingleNumberReachNumber):
        """
        Modify User's Single Number Reach Contact Settings

        Update the contact settings of single number reach for the authenticated user.

        The "Single Number Reach" feature in Webex allows users to access their business phone capabilities from any
        device, making it easy to make and receive calls as if at their office. This is especially useful for remote
        or mobile workers needing flexibility.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param phone_number_id: Unique identifier of the phone number.
        :type phone_number_id: str
        :param settings: User's Single Number Reach Settings
        :type settings: :class:`SingleNumberReachNumber`
        """
        body = settings.create_update()
        url = self.ep(f'settings/singleNumberReach/numbers/{phone_number_id}')
        super().put(url, json=body)

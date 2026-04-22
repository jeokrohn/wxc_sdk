from collections.abc import Generator
from typing import Any, Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['MeHotelingApi', 'AvailableHotelingHost', 'HotelingGuestSettings']

from wxc_sdk.common import IdAndName


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
    host_location: Optional[IdAndName] = None

    def update(self) -> dict[str, Any]:
        """
        data for update()

        :meta private:
        """
        return self.model_dump(
            mode='json',
            by_alias=True,
            exclude_none=True,
            include={'enabled', 'association_limit_enabled', 'association_limit_hours', 'host_id'},
        )


class MeHotelingApi(ApiChild, base='telephony/config/people/me'):
    def get_available_hosts(
        self, name: str = None, phone_number: str = None, **params: Any
    ) -> Generator[AvailableHotelingHost, None, None]:
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

    def get_guest_settings(self) -> HotelingGuestSettings:
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

    def update_guest_settings(self, settings: HotelingGuestSettings) -> None:
        """
        Update Hoteling Guest Settings

        Update hoteling guest settings for a person. Allows enabling or disabling the ability to use hoteling as a
        guest, configuring whether an association will be removed automatically after a specified time period, and
        associating with a hoteling host.

        Hoteling is a feature of Webex Calling that enables flexible workspace solutions by allowing users to log into
        shared devices.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: Hoteling settings to update
        :type settings: :class:`HotelingGuestSettings`
        :rtype: None
        """
        body = settings.update()
        url = self.ep('settings/hoteling/guest')
        super().put(url, json=body)

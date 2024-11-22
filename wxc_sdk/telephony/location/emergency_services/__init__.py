from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['LocationEmergencyServicesApi', 'LocationEmergencyCallNotification', 'LocationCallNotificationOrganization']


class LocationCallNotificationOrganization(ApiModel):
    #: When true sends an email to the specified email address when a call is made from this location to emergency
    #: services.
    emergency_call_notification_enabled: Optional[bool] = None
    #: Send an emergency call notification email for all locations.
    allow_email_notification_all_location_enabled: Optional[bool] = None
    #: When `emergencyCallNotificationEnabled` is true, the emergency notification email is sent to the specified email
    #: address.
    email_address: Optional[str] = None


class LocationEmergencyCallNotification(ApiModel):
    #: When true sends an email to the specified email address when a call is made from this location to emergency
    #: services.
    emergency_call_notification_enabled: Optional[bool] = None
    #: When `emergencyCallNotificationEnabled` is true, the emergency notification email is sent to the specified email
    #: address.
    email_address: Optional[str] = None
    #: All locations at organization level
    organization: Optional[LocationCallNotificationOrganization] = None

    def update(self) -> dict:
        """
        Date for update

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_unset=True, exclude={'customer'})


class LocationEmergencyServicesApi(ApiChild, base='telephony/config/locations'):
    """
    Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
    receive email notifications when an emergency call is made. Once activated at the organization level, individual
    locations can configure this setting to direct notifications to specific email addresses. To comply with U.S.
    Public Law 115-127, also known as Kari’s Law, any call that's made from within your organization to emergency
    services must generate an email notification.

    Viewing these organization settings requires a full or read-only administrator auth token with a scope
    of `spark-admin:telephony_config_read`. Modifying these organization settings requires a full administrator auth
    token with a scope of `spark-admin:telephony_config_write`.
    """

    def read_emergency_call_notification(self, location_id: str,
                                         org_id: str = None) -> LocationEmergencyCallNotification:
        """
        Get a Location Emergency Call Notification

        Get location emergency call notification.

        Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
        receive email notifications when an emergency call is made. Once activated at the organization level,
        individual locations can configure this setting to direct notifications to specific email addresses. To comply
        with U.S. Public Law 115-127, also known as Kari’s Law, any call that's made from within your organization to
        emergency services must generate an email notification.

        To retrieve location call notifications requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve Emergency Call Notification attributes for this location.
        :type location_id: str
        :param org_id: Retrieve Emergency Call Notification attributes for the location in this organization.
        :type org_id: str
        :rtype: :class:`LocationEmergencyCallNotification`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/emergencyCallNotification')
        data = super().get(url, params=params)
        r = LocationEmergencyCallNotification.model_validate(data)
        return r

    def update_emergency_call_notification(self, location_id: str, setting: LocationEmergencyCallNotification,
                                           org_id: str = None):
        """
        Update a location emergency call notification.

        Once settings enabled at the organization level, the configured email address will receive emergency call
        notifications for all locations; for specific location customization, users can navigate to Management >
        Locations, select the Calling tab, and update the Emergency Call Notification settings.

        Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
        receive email notifications when an emergency call is made. Once activated at the organization level,
        individual locations can configure this setting to direct notifications to specific email addresses. To comply
        with U.S. Public Law 115-127, also known as Kari’s Law, any call that's made from within your organization to
        emergency services must generate an email notification.

        To update location call notification requires a full, user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Update Emergency Call Notification attributes for this location.
        :type location_id: str
        :param setting: new settings
        :type setting: LocationEmergencyCallNotification
        :param org_id: Update Emergency Call Notification attributes for a location in this organization.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        body = setting.update()
        url = self.ep(f'{location_id}/emergencyCallNotification')
        super().put(url, params=params, json=body)

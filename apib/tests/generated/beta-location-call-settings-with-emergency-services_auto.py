from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaLocationCallSettingsWithEmergencyServicesApi', 'GetLocationCallNotificationObject',
           'GetLocationCallNotificationObjectOrganization']


class GetLocationCallNotificationObjectOrganization(ApiModel):
    #: When true sends an email to the specified email address when a call is made from this location to emergency
    #: services.
    #: example: True
    emergency_call_notification_enabled: Optional[bool] = None
    #: Send an emergency call notification email for all locations.
    #: example: True
    allow_email_notification_all_location_enabled: Optional[bool] = None
    #: When `emergencyCallNotificationEnabled` is true, the emergency notification email is sent to the specified email
    #: address.
    #: example: test@gmail.com
    email_address: Optional[str] = None


class GetLocationCallNotificationObject(ApiModel):
    #: When true sends an email to the specified email address when a call is made from this location to emergency
    #: services.
    #: example: True
    emergency_call_notification_enabled: Optional[bool] = None
    #: When `emergencyCallNotificationEnabled` is true, the emergency notification email is sent to the specified email
    #: address.
    #: example: callback@gmail.com
    email_address: Optional[str] = None
    #: All locations at organization level
    organization: Optional[GetLocationCallNotificationObjectOrganization] = None


class BetaLocationCallSettingsWithEmergencyServicesApi(ApiChild, base='telephony/config/locations'):
    """
    Beta Location Call Settings with Emergency Services
    
    Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
    receive email notifications when an emergency call is made. Once activated at the organization level, individual
    locations can configure this setting to direct notifications to specific email addresses. To comply with U.S.
    Public Law 115-127, also known as Kari’s Law, any call that's made from within your organization to emergency
    services must generate an email notification.
    
    Viewing these organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`. Modifying these organization settings requires a full administrator auth
    token with a scope of `spark-admin:telephony_config_write`.
    """

    def get_a_location_emergency_call_notification(self, location_id: str,
                                                   org_id: str = None) -> GetLocationCallNotificationObject:
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
        :rtype: :class:`GetLocationCallNotificationObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/emergencyCallNotification')
        data = super().get(url, params=params)
        r = GetLocationCallNotificationObject.model_validate(data)
        return r

    def update_a_location_emergency_call_notification(self, location_id: str,
                                                      emergency_call_notification_enabled: bool = None,
                                                      email_address: str = None, org_id: str = None):
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
        :param emergency_call_notification_enabled: When true sends an email to the specified email address when a call
            is made from this location to emergency services.
        :type emergency_call_notification_enabled: bool
        :param email_address: Sends an email to this email address when a call is made from this location to emergency
            services and `emergencyCallNotificationEnabled` is true.
        :type email_address: str
        :param org_id: Update Emergency Call Notification attributes for a location in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if emergency_call_notification_enabled is not None:
            body['emergencyCallNotificationEnabled'] = emergency_call_notification_enabled
        if email_address is not None:
            body['emailAddress'] = email_address
        url = self.ep(f'{location_id}/emergencyCallNotification')
        super().put(url, params=params, json=body)

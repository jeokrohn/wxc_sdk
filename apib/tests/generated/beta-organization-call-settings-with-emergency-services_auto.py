from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaOrganizationCallSettingsWithEmergencyServicesApi', 'OrgCallNotificationObject']


class OrgCallNotificationObject(ApiModel):
    #: When true sends an email to the specified email address when a call is made to emergency services.
    #: example: True
    emergency_call_notification_enabled: Optional[bool] = None
    #: Send an emergency call notification email for all locations.
    #: example: True
    allow_email_notification_all_location_enabled: Optional[bool] = None
    #: When `emergencyCallNotificationEnabled` is true, the emergency notification email is sent to the specified email
    #: address.
    #: example: callback@gmail.com
    email_address: Optional[str] = None


class BetaOrganizationCallSettingsWithEmergencyServicesApi(ApiChild, base='telephony/config/emergencyCallNotification'):
    """
    Beta Organization Call Settings with Emergency Services
    
    Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
    receive email notifications when an emergency call is made. To comply with U.S. Public Law 115-127, also known as
    Kari’s Law, any call that's made from within your organization to emergency services must generate an email
    notification.
    
    Viewing these organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`. Modifying these organization settings requires a full administrator auth
    token with a scope of `spark-admin:telephony_config_write`.
    """

    def get_an_organization_emergency_call_notification(self, org_id: str = None) -> OrgCallNotificationObject:
        """
        Get an Organization Emergency Call Notification

        Get organization emergency call notification.

        Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
        receive email notifications when an emergency call is made. To comply with U.S. Public Law 115-127, also known
        as Kari’s Law, any call that's made from within your organization to emergency services must generate an email
        notification.

        To retrieve organization call notifications requires a full, user or read-only administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve Emergency Call Notification attributes for the organization.
        :type org_id: str
        :rtype: :class:`OrgCallNotificationObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = OrgCallNotificationObject.model_validate(data)
        return r

    def update_an_organization_emergency_call_notification(self, emergency_call_notification_enabled: bool = None,
                                                           allow_email_notification_all_location_enabled: bool = None,
                                                           email_address: str = None, org_id: str = None):
        """
        Update an organization emergency call notification.

        Once settings are enabled at the organization level, the configured email address will receive emergency call
        notifications for all locations.

        Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
        receive email notifications when an emergency call is made. To comply with U.S. Public Law 115-127, also known
        as Kari’s Law, any call that's made from within your organization to emergency services must generate an email
        notification.

        To update organization call notification requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param emergency_call_notification_enabled: When true sends an email to the specified email address when a call
            is made to emergency services.
        :type emergency_call_notification_enabled: bool
        :param allow_email_notification_all_location_enabled: Send an emergency call notification email for all
            locations.
        :type allow_email_notification_all_location_enabled: bool
        :param email_address: When `emergencyCallNotificationEnabled` is true, the emergency notification email is sent
            to the specified email address.
        :type email_address: str
        :param org_id: Update Emergency Call Notification attributes for the organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if emergency_call_notification_enabled is not None:
            body['emergencyCallNotificationEnabled'] = emergency_call_notification_enabled
        if allow_email_notification_all_location_enabled is not None:
            body['allowEmailNotificationAllLocationEnabled'] = allow_email_notification_all_location_enabled
        if email_address is not None:
            body['emailAddress'] = email_address
        url = self.ep()
        super().put(url, params=params, json=body)

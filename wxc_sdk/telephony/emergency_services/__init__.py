from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['OrgEmergencyServicesApi', 'OrgEmergencyCallNotification']


class OrgEmergencyCallNotification(ApiModel):
    #: When true sends an email to the specified email address when a call is made to emergency services.
    emergency_call_notification_enabled: Optional[bool] = None
    #: Send an emergency call notification email for all locations.
    allow_email_notification_all_location_enabled: Optional[bool] = None
    #: When `emergencyCallNotificationEnabled` is true, the emergency notification email is sent to the specified email
    #: address.
    email_address: Optional[str] = None

    def update(self) -> dict:
        """

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True)


class OrgEmergencyServicesApi(ApiChild, base='telephony/config/emergencyCallNotification'):
    """
    Organization Call Settings with Emergency Services

    Emergency Call Notifications can be enabled at the organization level, allowing specified email addresses to
    receive email notifications when an emergency call is made. To comply with U.S. Public Law 115-127, also known as
    Kari’s Law, any call that's made from within your organization to emergency services must generate an email
    notification.

    Viewing these organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`. Modifying these organization settings requires a full administrator auth
    token with a scope of `spark-admin:telephony_config_write`.
    """

    def read_emergency_call_notification(self, org_id: str = None) -> OrgEmergencyCallNotification:
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
        :rtype: :class:`OrgEmergencyCallNotification`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = OrgEmergencyCallNotification.model_validate(data)
        return r

    def update_emergency_call_notification(self, setting: OrgEmergencyCallNotification, org_id: str = None):
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

        :param setting: updated settings
        :type setting: OrgEmergencyCallNotification
        :param org_id: Update Emergency Call Notification attributes for the organization.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        body = setting.update()
        url = self.ep()
        super().put(url, params=params, json=body)

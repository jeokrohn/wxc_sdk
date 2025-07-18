from collections.abc import Generator
from datetime import datetime
from typing import Optional, Union, Any

from dateutil.parser import isoparse

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str

__all__ = ['AdminAuditEventsApi', 'AuditEvent', 'AuditEventData']


class AuditEventData(ApiModel):
    class Config:
        extra = 'allow'

    #: The display name of the organization.
    actor_org_name: Optional[str] = None
    #: The name of the resource being acted upon.
    target_name: Optional[str] = None
    #: A description for the event.
    event_description: Optional[str] = None
    #: The name of the person who performed the action.
    actor_name: Optional[str] = None
    #: The email of the person who performed the action.
    actor_email: Optional[str] = None
    #: Admin roles for the person.
    admin_roles: Optional[list[str]] = None
    #: A tracking identifier for the event.
    tracking_id: Optional[str] = None
    #: The type of resource changed by the event.
    target_type: Optional[str] = None
    #: The identifier for the resource changed by the event.
    target_id: Optional[str] = None
    #: The category of resource changed by the event.
    event_category: Optional[str] = None
    #: The browser user agent of the person who performed the action.
    # Chrome/71.0.3578.98 Safari/537.36
    actor_user_agent: Optional[str] = None
    #: The IP address of the person who performed the action.
    actor_ip: Optional[str] = None
    #: The `orgId` of the organization.
    target_org_id: Optional[str] = None
    #: A more detailed description of the change made by the person.
    action_text: Optional[str] = None
    #: The name of the organization being acted upon.
    target_org_name: Optional[str] = None

    account_name: Optional[Any] = None
    action_client_id: Optional[Any] = None
    action_client_name: Optional[Any] = None
    action: Optional[Any] = None
    activated_numbers: Optional[Any] = None
    actor_client_id: Optional[Any] = None
    actor_client_name: Optional[Any] = None
    added_pattern: Optional[Any] = None
    attributes: Optional[Any] = None
    authorized_status: Optional[Any] = None
    api_version: Optional[Any] = None
    business_text_status: Optional[Any] = None
    capacity: Optional[Any] = None
    category: Optional[Any] = None
    change_detail_id: Optional[Any] = None
    change_set: Optional[Any] = None
    changed_attributes: Optional[Any] = None
    changed_group_members: Optional[Any] = None
    client_id: Optional[Any] = None
    client_type: Optional[Any] = None
    command_key: Optional[Any] = None
    config_key: Optional[Any] = None
    config_value: Optional[Any] = None
    contact_info: Optional[Any] = None
    contact_type: Optional[Any] = None
    current_location_name: Optional[Any] = None
    dect_network_name: Optional[Any] = None
    deleted_auth_code: Optional[Any] = None
    deleted_pattern_name: Optional[Any] = None
    deleted_pattern: Optional[Any] = None
    deleted_settings: Optional[Any] = None
    details: Optional[Any] = None
    device_id: Optional[Any] = None
    domain_name: Optional[Any] = None
    domain_state: Optional[Any] = None
    email_address_count: Optional[Any] = None
    email_type: Optional[Any] = None
    end_date: Optional[Any] = None
    enrollment_status: Optional[Any] = None
    entitlements: Optional[Any] = None
    entity_id: Optional[Any] = None
    entity_type: Optional[Any] = None
    event_status: Optional[Any] = None
    extension_time: Optional[Any] = None
    external_admin_email: Optional[Any] = None
    external_admin_org_name: Optional[Any] = None
    failed_reason: Optional[Any] = None
    feature_type: Optional[Any] = None
    file_name: Optional[Any] = None
    group_name: Optional[Any] = None
    is_manual_switchback_enabled: Optional[Any] = None
    job_name: Optional[Any] = None
    locale: Optional[Any] = None
    location_id: Optional[Any] = None
    location_name: Optional[Any] = None
    location: Optional[Any] = None
    mac_address: Optional[Any] = None
    name: Optional[Any] = None
    new_org_default_enabled: Optional[Any] = None
    new_vendor_name: Optional[Any] = None
    numbers_updated: Optional[Any] = None
    numbers: Optional[Any] = None
    offer_map: Optional[Any] = None
    old_org_default_enabled: Optional[Any] = None
    old_vendor_name: Optional[Any] = None
    operating_mode_level: Optional[Any] = None
    operating_mode_name: Optional[Any] = None
    operation_type: Optional[Any] = None
    operation: Optional[Any] = None
    org_id: Optional[Any] = None
    owner_id: Optional[Any] = None
    owner_type: Optional[Any] = None
    portability_numbers: Optional[Any] = None
    previous_group_id: Optional[Any] = None
    previous_value: Optional[Any] = None
    report_id: Optional[Any] = None
    reserved_numbers: Optional[Any] = None
    result: Optional[Any] = None
    role_added: Optional[Any] = None
    role_removed: Optional[Any] = None
    rule_name: Optional[Any] = None
    rule_title: Optional[Any] = None
    service_app_scopes: Optional[Any] = None
    services: Optional[Any] = None
    setting_key: Optional[Any] = None
    setting_name: Optional[Any] = None
    setting_value: Optional[Any] = None
    site_admin_roles: Optional[Any] = None
    start_date: Optional[Any] = None
    sub_type: Optional[Any] = None
    success: Optional[Any] = None
    tags: Optional[Any] = None
    target_email: Optional[Any] = None
    target_location_name: Optional[Any] = None
    template_name: Optional[Any] = None
    template_type: Optional[Any] = None
    token_id: Optional[Any] = None
    trial_expiration_dtm: Optional[Any] = None
    trial_id: Optional[Any] = None
    trial_period_days: Optional[Any] = None
    trial_start_dtm: Optional[Any] = None
    type: Optional[Any] = None
    updated_fields: Optional[Any] = None
    updated_settings: Optional[Any] = None
    user_name: Optional[Any] = None
    user_roles: Optional[Any] = None
    vendor_name: Optional[Any] = None


class AuditEvent(ApiModel):
    data: Optional[AuditEventData] = None
    #: The date and time the event took place.
    created: Optional[datetime] = None
    #: The `orgId` of the person who made the change.
    actor_org_id: Optional[str] = None
    #: A unique identifier for the event.
    id: Optional[str] = None
    #: The `personId` of the person who made the change.
    actor_id: Optional[str] = None


class AdminAuditEventsApi(ApiChild, base='adminAudit'):
    """
    Admin Audit Events

    Admin Audit Events are available to full administrators for `certain events
    <https://help.webex.com/en-us/article/nqzomav/Control-Hub-audit-events-reference>`_ performed in Webex Control Hub.

    Administrators with accounts created before 2019 who have never logged into `Webex Control Hub
    <https://admin.webex.com>`_ will need to log into
    Webex Control Hub at least once to enable access to this API.

    An administrator account with the `audit:events_read` scope is required to use this API.
    """

    def list_events(self, org_id: str, from_: Union[str, datetime], to_: Union[str, datetime],
                    actor_id: str = None, event_categories: list[str] = None,
                    **params) -> Generator[AuditEvent, None, None]:
        """
        List Admin Audit Events

        List admin audit events in your organization. Several query parameters are available to filter the response.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        **NOTE**: A maximum of one year of audit events can be returned per request.

        :param org_id: List events in this organization, by ID.
        :type org_id: str
        :param from_: List events which occurred after a specific date and time.
        :type from_: Union[str, datetime]
        :param to_: List events which occurred before a specific date and time.
        :type to_: Union[str, datetime]
        :param actor_id: List events performed by this person, by ID.
        :type actor_id: str
        :param event_categories: List events, by event categories.
        :type event_categories: list[str]
        :return: Generator yielding :class:`AuditEvent` instances
        """
        params['orgId'] = org_id
        if isinstance(from_, str):
            from_ = isoparse(from_)
        from_ = dt_iso_str(from_)
        params['from'] = from_
        if isinstance(to_, str):
            to_ = isoparse(to_)
        to_ = dt_iso_str(to_)
        params['to'] = to_
        if actor_id is not None:
            params['actorId'] = actor_id
        if event_categories is not None:
            params['eventCategories'] = ','.join(event_categories)
        url = self.ep('events')
        return self.session.follow_pagination(url=url, model=AuditEvent, item_key='items', params=params)

    def list_event_categories(self) -> list[str]:
        """
        List Admin Audit Event Categories

        Get the list of all admin event categories.

        :rtype: list[str]
        """
        url = self.ep('eventCategories')
        data = super().get(url)
        r = data['eventCategories']
        return r

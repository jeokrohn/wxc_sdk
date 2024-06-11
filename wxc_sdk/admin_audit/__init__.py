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
    #: example: Acme Inc.
    actor_org_name: Optional[str] = None
    #: The name of the resource being acted upon.
    #: example: Acme Inc.
    target_name: Optional[str] = None
    #: A description for the event.
    #: example: An Admin logged in
    event_description: Optional[str] = None
    #: The name of the person who performed the action.
    #: example: Joe Smith
    actor_name: Optional[str] = None
    #: The email of the person who performed the action.
    #: example: joe@example.com
    actor_email: Optional[str] = None
    #: Admin roles for the person.
    #: example: ['User', 'Full_Admin', 'id_full_admin']
    admin_roles: Optional[list[str]] = None
    #: A tracking identifier for the event.
    #: example: ATLAS_6f23a878-bcd4-c204-a4db-e701b42b0e5c_0
    tracking_id: Optional[str] = None
    #: The type of resource changed by the event.
    #: example: TargetResourceType.ORG
    target_type: Optional[str] = None
    #: The identifier for the resource changed by the event.
    #: example: NWIzZTBiZDgtZjg4Ni00MjViLWIzMTgtYWNlYjliN2EwZGFj
    target_id: Optional[str] = None
    #: The category of resource changed by the event.
    #: example: EventCategory.LOGINS
    event_category: Optional[str] = None
    #: The browser user agent of the person who performed the action.
    #: example: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko)
    # Chrome/71.0.3578.98 Safari/537.36
    actor_user_agent: Optional[str] = None
    #: The IP address of the person who performed the action.
    #: example: 128.107.241.191
    actor_ip: Optional[str] = None
    #: The `orgId` of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    target_org_id: Optional[str] = None
    #: A more detailed description of the change made by the person.
    #: example: Joe Smith logged into organization Acme Inc.
    action_text: Optional[str] = None
    #: The name of the organization being acted upon.
    #: example: Acme Inc.
    target_org_name: Optional[str] = None

    action_client_id: Optional[Any] = None
    action_client_name: Optional[Any] = None
    actor_client_id: Optional[Any] = None
    actor_client_name: Optional[Any] = None
    added_pattern: Optional[Any] = None
    attributes: Optional[Any] = None
    authorized_status: Optional[Any] = None
    capacity: Optional[Any] = None
    change_detail_id: Optional[Any] = None
    changed_attributes: Optional[Any] = None
    changed_group_members: Optional[Any] = None
    client_id: Optional[Any] = None
    command_key: Optional[Any] = None
    config_key: Optional[Any] = None
    config_value: Optional[Any] = None
    current_location_name: Optional[Any] = None
    dect_network_name: Optional[Any] = None
    deleted_auth_code: Optional[Any] = None
    deleted_pattern_name: Optional[Any] = None
    deleted_pattern: Optional[Any] = None
    device_id: Optional[Any] = None
    email_type: Optional[Any] = None
    enrollment_status: Optional[Any] = None
    entitlements: Optional[Any] = None
    entity_type: Optional[Any] = None
    event_status: Optional[Any] = None
    external_admin_email: Optional[Any] = None
    external_admin_org_name: Optional[Any] = None
    failed_reason: Optional[Any] = None
    job_name: Optional[Any] = None
    locale: Optional[Any] = None
    location_id: Optional[Any] = None
    location_name: Optional[Any] = None
    location: Optional[Any] = None
    mac_address: Optional[Any] = None
    name: Optional[Any] = None
    new_org_default_enabled: Optional[Any] = None
    new_vendor_name: Optional[Any] = None
    numbers: Optional[Any] = None
    offer_map: Optional[Any] = None
    old_org_default_enabled: Optional[Any] = None
    old_vendor_name: Optional[Any] = None
    operation_type: Optional[Any] = None
    operation: Optional[Any] = None
    org_id: Optional[Any] = None
    owner_id: Optional[Any] = None
    owner_type: Optional[Any] = None
    previous_value: Optional[Any] = None
    result: Optional[Any] = None
    role_added: Optional[Any] = None
    role_removed: Optional[Any] = None
    rule_name: Optional[Any] = None
    service_app_scopes: Optional[Any] = None
    services: Optional[Any] = None
    setting_key: Optional[Any] = None
    setting_name: Optional[Any] = None
    setting_value: Optional[Any] = None
    tags: Optional[Any] = None
    target_email: Optional[Any] = None
    target_location_name: Optional[Any] = None
    token_id: Optional[Any] = None
    trial_expiration_dtm: Optional[Any] = None
    trial_id: Optional[Any] = None
    trial_period_days: Optional[Any] = None
    trial_start_dtm: Optional[Any] = None
    type: Optional[Any] = None
    updated_fields: Optional[Any] = None
    updated_settings: Optional[Any] = None
    user_name: Optional[Any] = None
    vendor_name: Optional[Any] = None


class AuditEvent(ApiModel):
    data: Optional[AuditEventData] = None
    #: The date and time the event took place.
    #: example: 2019-01-02T16:58:36.845Z
    created: Optional[datetime] = None
    #: The `orgId` of the person who made the change.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    actor_org_id: Optional[str] = None
    #: A unique identifier for the event.
    #: example: MjQ0ODhiZTYtY2FiMS00ZGRkLTk0NWQtZDFlYjkzOGQ4NGUy
    id: Optional[str] = None
    #: The `personId` of the person who made the change.
    #: example: MjQ4Njg2OTYtYWMwZC00ODY4LWJkMjEtZGUxZDc4MzhjOTdm
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

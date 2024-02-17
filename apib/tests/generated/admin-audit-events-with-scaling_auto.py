from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AdminAuditEventsWithScalingApi', 'AuditEvent', 'AuditEventData']


class AuditEventData(ApiModel):
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
    #: example: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
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
    #: User operation failure message.
    #: example: WXC-25058 Extension cannot be less than 2 or greater than 6 characters
    error_message: Optional[str] = None
    #: User operation failure code.
    #: example: WXC-25058
    error_code: Optional[str] = None


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


class AdminAuditEventsWithScalingApi(ApiChild, base='adminAudit'):
    """
    Admin Audit Events with Scaling
    
    Admin Audit Events are available to full administrators for `certain events
    <https://help.webex.com/n3b0w6x/>`_ performed in Webex Control Hub.
    
    Administrators with accounts created before 2019 who have never logged into `Webex Control Hub
    <https://admin.webex.com>`_ will need to log into
    Webex Control Hub at least once to enable access to this API.
    
    An administrator account with the `audit:events_read` scope is required to use this API.
    """

    def list_admin_audit_events(self, org_id: str, from_: Union[str, datetime], to_: Union[str, datetime],
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

    def list_admin_audit_event_categories(self) -> list[str]:
        """
        List Admin Audit Event Categories

        Get the list of all admin event categories.

        :rtype: list[str]
        """
        url = self.ep('eventCategories')
        data = super().get(url)
        r = data['eventCategories']
        return r

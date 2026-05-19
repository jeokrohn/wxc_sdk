import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AdminAuditEventsApi', 'AdminRolesEnum', 'AuditEvent', 'AuditEventData']


class AdminRolesEnum(str, Enum):
    user = 'User'
    full_admin = 'Full_Admin'
    id_full_admin = 'id_full_admin'


class AuditEventData(ApiModel):
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
    admin_roles: Optional[list[AdminRolesEnum]] = None
    #: A tracking identifier for the event.
    tracking_id: Optional[str] = None
    #: The type of resource changed by the event.
    target_type: Optional[str] = None
    #: The identifier for the resource changed by the event.
    target_id: Optional[str] = None
    #: The category of resource changed by the event.
    event_category: Optional[str] = None
    #: The browser user agent of the person who performed the action.
    actor_user_agent: Optional[str] = None
    #: The IP address of the person who performed the action.
    actor_ip: Optional[str] = None
    #: The `orgId` of the organization.
    target_org_id: Optional[str] = None
    #: A more detailed description of the change made by the person.
    action_text: Optional[str] = None
    #: The name of the organization being acted upon.
    target_org_name: Optional[str] = None


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

    def list_admin_audit_event_categories(self) -> builtins.list[str]:
        """
        List Admin Audit Event Categories

        Get the list of all admin event categories.

        :rtype: list[str]
        """
        url = self.ep('eventCategories')
        data = super().get(url)
        r = data['eventCategories']
        return r

    def list_admin_audit_events(self, org_id: str, from_: Union[str, datetime], to_: Union[str, datetime],
                                actor_id: str = None, event_categories: list[str] = None,
                                **params: Any) -> Generator[AuditEvent, None, None]:
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

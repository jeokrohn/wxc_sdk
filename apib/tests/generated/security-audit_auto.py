from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['SecurityAuditEvent', 'SecurityAuditEventData', 'SecurityAuditEventsApi']


class SecurityAuditEventData(ApiModel):
    #: The display name of the organization.
    #: example: Acme Inc.
    actor_org_name: Optional[str] = None
    #: A description for the event.
    #: example: An Admin logged in
    event_description: Optional[str] = None
    #: The name of the person who performed the action.
    #: example: Joe Smith
    actor_name: Optional[str] = None
    #: The email of the person who performed the action.
    #: example: joe@example.com
    actor_email: Optional[str] = None
    #: The browser user agent of the person who performed the action.
    #: example: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
    actor_user_agent: Optional[str] = None
    #: A tracking identifier for the event.
    #: example: ATLAS_6f23a878-bcd4-c204-a4db-e701b42b0e5c_0
    tracking_id: Optional[str] = None
    #: The category of resource changed by the event.
    #: example: LOGINS
    event_category: Optional[str] = None
    #: The IP address of the person who performed the action.
    #: example: 128.107.241.191
    actor_ip: Optional[str] = None
    #: A more detailed description of the change made by the person.
    #: example: Joe Smith logged into organization Acme Inc.
    action_text: Optional[str] = None


class SecurityAuditEvent(ApiModel):
    data: Optional[SecurityAuditEventData] = None
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
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82ZWVmOGE4ZS1lNzg3LTQzMWUtOWM3ZC1hOGVjZmU1MjM5Nzc
    actor_id: Optional[str] = None


class SecurityAuditEventsApi(ApiChild, base='admin/securityAudit/events'):
    """
    Security Audit Events
    
    """

    def list_security_audit_events(self, org_id: str, start_time: Union[str, datetime], end_time: Union[str, datetime],
                                   actor_id: str = None, event_categories: list[str] = None,
                                   **params) -> Generator[SecurityAuditEvent, None, None]:
        """
        List Security Audit Events

        List Security Audit Events. This API currently returns user sign-in and sign-out data.
        To call this API the `audit:events_read` scope must be selected for the Integration or Service App and
        auhtorized by a Full Admin.

        Several query parameters are available to filter the response.

        Long result sets will be split into multiple `pages
        <https://developer.webex.com/docs/basics#pagination>`_

        **NOTE**: A maximum of one year of audit events can be returned per request.

        :param org_id: List events in this organization, by ID.
        :type org_id: str
        :param start_time: List events which occurred after a specific date and time.
        :type start_time: Union[str, datetime]
        :param end_time: List events which occurred before a specific date and time.
        :type end_time: Union[str, datetime]
        :param actor_id: List events performed by this person, by ID.
        :type actor_id: str
        :param event_categories: List events, by event categories.
        :type event_categories: list[str]
        :return: Generator yielding :class:`SecurityAuditEvent` instances
        """
        params['orgId'] = org_id
        if isinstance(start_time, str):
            start_time = isoparse(start_time)
        start_time = dt_iso_str(start_time)
        params['startTime'] = start_time
        if isinstance(end_time, str):
            end_time = isoparse(end_time)
        end_time = dt_iso_str(end_time)
        params['endTime'] = end_time
        if actor_id is not None:
            params['actorId'] = actor_id
        if event_categories is not None:
            params['eventCategories'] = ','.join(event_categories)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=SecurityAuditEvent, item_key='items', params=params)

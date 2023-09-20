from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AuditEvent', 'AuditEventCategoryCollectionResponse', 'AuditEventCollectionResponse', 'AuditEventData']


class AuditEventData(ApiModel):
    #: The display name of the organization.
    #: example: Acme Inc.
    actorOrgName: Optional[str] = None
    #: The name of the resource being acted upon.
    #: example: Acme Inc.
    targetName: Optional[str] = None
    #: A description for the event.
    #: example: An Admin logged in
    eventDescription: Optional[str] = None
    #: The name of the person who performed the action.
    #: example: Joe Smith
    actorName: Optional[str] = None
    #: The email of the person who performed the action.
    #: example: joe@example.com
    actorEmail: Optional[str] = None
    #: Admin roles for the person.
    #: example: ['User', 'Full_Admin', 'id_full_admin']
    adminRoles: Optional[list[str]] = None
    #: A tracking identifier for the event.
    #: example: ATLAS_6f23a878-bcd4-c204-a4db-e701b42b0e5c_0
    trackingId: Optional[str] = None
    #: The type of resource changed by the event.
    #: example: TargetResourceType.ORG
    targetType: Optional[str] = None
    #: The identifier for the resource changed by the event.
    #: example: NWIzZTBiZDgtZjg4Ni00MjViLWIzMTgtYWNlYjliN2EwZGFj
    targetId: Optional[str] = None
    #: The category of resource changed by the event.
    #: example: EventCategory.LOGINS
    eventCategory: Optional[str] = None
    #: The browser user agent of the person who performed the action.
    #: example: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
    actorUserAgent: Optional[str] = None
    #: The IP address of the person who performed the action.
    #: example: 128.107.241.191
    actorIp: Optional[str] = None
    #: The `orgId` of the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    targetOrgId: Optional[str] = None
    #: A more detailed description of the change made by the person.
    #: example: Joe Smith logged into organization Acme Inc.
    actionText: Optional[str] = None
    #: The name of the organization being acted upon.
    #: example: Acme Inc.
    targetOrgName: Optional[str] = None


class AuditEvent(ApiModel):
    data: Optional[AuditEventData] = None
    #: The date and time the event took place.
    #: example: 2019-01-02T16:58:36.845Z
    created: Optional[datetime] = None
    #: The `orgId` of the person who made the change.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    actorOrgId: Optional[str] = None
    #: A unique identifier for the event.
    #: example: MjQ0ODhiZTYtY2FiMS00ZGRkLTk0NWQtZDFlYjkzOGQ4NGUy
    id: Optional[str] = None
    #: The `personId` of the person who made the change.
    #: example: MjQ4Njg2OTYtYWMwZC00ODY4LWJkMjEtZGUxZDc4MzhjOTdm
    actorId: Optional[str] = None


class AuditEventCollectionResponse(ApiModel):
    #: An array of audit event objects. See [this article](https://help.webex.com/n3b0w6x/) for details about each event type.
    items: Optional[list[AuditEvent]] = None


class AuditEventCategoryCollectionResponse(ApiModel):
    #: An array of audit event categories.
    eventCategories: Optional[list[str]] = None

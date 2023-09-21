from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Issue', 'IssueStatus', 'IssueType', 'IssuesCollectionResponse']


class IssueType(str, Enum):
    #: Issue type for general comments.
    comment = 'COMMENT'
    #: Issue type for reporting defects.
    defect = 'DEFECT'
    #: Issue type for feature requests.
    feature = 'FEATURE'
    #: Issue type for reporting new problems. (default)
    problem = 'PROBLEM'
    #: Issue type for questions that need answers.
    question = 'QUESTION'


class IssueStatus(str, Enum):
    #: Status for issues sssigned to a support person.
    assigned = 'ASSIGNED'
    #: Status for issues that were closed without resolving.
    closed = 'CLOSED'
    #: Status for issues that were escalated to another support team.
    escalated = 'ESCALATED'
    #: Status for open issues. (default)
    new = 'NEW'
    #: Status for issues that were fixed and resolved.
    resolved = 'RESOLVED'


class Issue(ApiModel):
    #: A unique identifier for the issue.
    #: example: Y2lzY29zcGFyazovL3VzL0lTU1VFLzIyNWE0YWY0LTIxYTctNDY2OC05NjhhLWI5NWU2MjlhMjBlNg
    id: Optional[str] = None
    #: A shorter identifier for the issue, unique only to the organization it belongs to.
    #: example: 123.0
    short_key: Optional[int] = None
    #: The subject summary for the issue.
    #: example: No audio during meeting from Webex client.
    subject: Optional[str] = None
    #: The full description of the issue.
    #: example: I could not hear any audio during a Webex Meeting I joined from my Webex for Android client.
    description: Optional[str] = None
    #: The person ID of user the issue was created for.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    created_for: Optional[str] = None
    #: The organization the issue belongs to.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: The type for the issue, such as `PROBLEM` or `DEFECT`.
    #: example: PROBLEM
    type: Optional[IssueType] = None
    #: The status for the issue, such as `NEW` or `CLOSED`.
    #: example: NEW
    status: Optional[IssueStatus] = None
    #: The person ID of user assigned to resolve the issue.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    assignee: Optional[str] = None
    #: A description of how the issue was resolved.
    #: example: The end user's Bluetooth headset was not paired successfully with her Android phone. Re-paring fixed the issue.
    resolution: Optional[str] = None
    #: Date and time issue was created.
    #: example: 2019-06-01T00:00:00.000Z
    created: Optional[datetime] = None
    #: Date and time issue was last modified.
    #: example: 2019-06-01T00:00:00.000Z
    last_modified: Optional[datetime] = None
    #: The person ID of user that last modified the issue.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    last_modified_by: Optional[str] = None
    #: The log ID submitted by webex clients when a user triggers feedback.
    #: example: 99e71be2-25a6-4628-9b77-37002fe40f47
    log_id: Optional[str] = None
    #: The meeting ID related to the issue.
    #: example: dfb45ece33264639a7bc3dd9535d53f7_20200516T230000Z
    meeting_id: Optional[str] = None
    #: The space ID created to collaborate on the issue.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    space_id: Optional[str] = None
    #: Any custom identifier associated with the issue, such as from an external ticketing system.
    #: example: TICKET-12345
    external_key: Optional[str] = None


class IssuesCollectionResponse(ApiModel):
    #: An array of issue objects.
    items: Optional[list[Issue]] = None

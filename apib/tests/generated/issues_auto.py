from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Issue', 'IssueStatus', 'IssueType', 'IssuesAPIApi']


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
    #: example: 123
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


class IssuesAPIApi(ApiChild, base='issues'):
    """
    Issues API
    
    Issues are support feedback entries from users of Webex clients and portals.
    
    Adding, searching, and viewing Issues requires an auth token with a scope of `support:issues_read`.
    
    Updating an issue by a user is also supported, but limited to the `subject` and `description`
    attributes.
    
    Viewing the list of all Issues in the Organization(s) managed by the admin user requires an
    auth token with scope of `support:org_issues_read`.
    
    Updating an Issue's `status` requires an auth token with the `support:org_issues_write` scope.
    
    An Issue cannot be deleted, but the `status` can be updated to `CLOSED`.
    """

    def list_issues(self, created_for: str = None, from_: Union[str, datetime] = None, to_: Union[str,
                    datetime] = None, after_issue: str = None, org_id: str = None,
                    **params) -> Generator[Issue, None, None]:
        """
        List Issues

        List issues in your organization.

        Admin users can list all issues for all organizations they manage.
        Admin users can also use the `createdFor` parameter to list issues for a specific person ID, or use the
        `orgId` to list issues for a specific organization.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param created_for:
        List issues created for this person ID.
        :type created_for: str
        :param from_:
        List events which occurred after a specific date and time.
        :type from_: Union[str, datetime]
        :param to_:
        List events which occurred before a specific date and time.
        :type to_: Union[str, datetime]
        :param after_issue:
        List issues created or modified after a specific issue, by ID.
        :type after_issue: str
        :param org_id:
        List issues in this organization. Admins of another organization such as partners might use this parameter.
        :type org_id: str
        :return: Generator yielding :class:`Issue` instances
        """
        if created_for is not None:
            params['createdFor'] = created_for
        if org_id is not None:
            params['orgId'] = org_id
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        if after_issue is not None:
            params['afterIssue'] = after_issue
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Issue, item_key='items', params=params)

    def create_an_issue(self, subject: str, description: str, type: IssueType = None, log_id: str = None,
                        meeting_id: str = None, external_key: str = None) -> Issue:
        """
        Create an Issue

        Create a new issue.

        Users can create issues for themselves and
        admins can create issues for both themselves and on behalf of other users.

        :param subject: The subject title for the issue.
        :type subject: str
        :param description: The full description of the issue.
        :type description: str
        :param type: The initial type for the issue.
        :type type: IssueType
        :type log_id: str
        :param meeting_id: The meeting ID related to the issue.
        :type meeting_id: str
        :param external_key: Any custom identifier associated with the issue, such as from an external ticketing
            system.
        :type external_key: str
        :rtype: :class:`Issue`
        """
        body = dict()
        body['subject'] = subject
        body['description'] = description
        if type is not None:
            body['type'] = enum_str(type)
        if log_id is not None:
            body['logId'] = log_id
        if meeting_id is not None:
            body['meetingId'] = meeting_id
        if external_key is not None:
            body['externalKey'] = external_key
        url = self.ep()
        data = super().post(url, json=body)
        r = Issue.model_validate(data)
        return r

    def get_issue_details(self, id: str) -> Issue:
        """
        Get Issue Details

        Show details for an issue, by ID.

        Specify the issue ID in the `id` parameter in the URI.

        :param id: A unique identifier for the issue.
        :type id: str
        :rtype: :class:`Issue`
        """
        url = self.ep(f'{id}')
        data = super().get(url)
        r = Issue.model_validate(data)
        return r

    def update_an_issue(self, id: str, subject: str = None, description: str = None, type: IssueType = None,
                        status: IssueStatus = None, assignee: str = None, resolution: str = None, log_id: str = None,
                        meeting_id: str = None, external_key: str = None) -> Issue:
        """
        Update an Issue

        Update details for an issue, by ID.

        Specify the issue ID in the `id` parameter in the URI.
        Users may update only the `subject` and `description` attributes.
        Admin users can update the `subject`, `description`, `type`, and `status` attributes.

        Include all details for the issue. This action expects all issue details to be present in the
        request. A common approach is to first `GET the issue's details
        <https://developer.webex.com/docs/api/v1/issues/get-issue-details>`_,
        make changes, then PUT both the changed and unchanged values.

        :param id: A unique identifier for the issue.
        :type id: str
        :param subject: The subject title for the issue.
        :type subject: str
        :param description: The full description of the issue.
        :type description: str
        :param type: The type for the issue.
        :type type: IssueType
        :param status: The status of the issue.
        :type status: IssueStatus
        :param assignee: The person ID of user assigned to resolve the issue.
        :type assignee: str
        :param resolution: A description of how the issue was resolved.
        :type resolution: str
        :type log_id: str
        :param meeting_id: The meeting ID related to the issue.
        :type meeting_id: str
        :param external_key: Any custom identifier associated with the issue, such as from an external ticketing
            system.
        :type external_key: str
        :rtype: :class:`Issue`
        """
        body = dict()
        if subject is not None:
            body['subject'] = subject
        if description is not None:
            body['description'] = description
        if type is not None:
            body['type'] = enum_str(type)
        if status is not None:
            body['status'] = enum_str(status)
        if assignee is not None:
            body['assignee'] = assignee
        if resolution is not None:
            body['resolution'] = resolution
        if log_id is not None:
            body['logId'] = log_id
        if meeting_id is not None:
            body['meetingId'] = meeting_id
        if external_key is not None:
            body['externalKey'] = external_key
        url = self.ep(f'{id}')
        data = super().put(url, json=body)
        r = Issue.model_validate(data)
        return r

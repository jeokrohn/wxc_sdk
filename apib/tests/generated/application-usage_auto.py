from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ApplicationUsage', 'ApplicationUsageApi', 'ApplicationUsagePolicyAction', 'ListApplicationUsageOrderBy']


class ApplicationUsagePolicyAction(str, Enum):
    allow = 'allow'
    deny = 'deny'


class ApplicationUsage(ApiModel):
    #: A unique identifier for the application.
    #: example: Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OLzEyMzQ1Njc4LTkwYWItY2RlZi0xMjM0LTU2Nzg5MGFiY2RlZg
    id: Optional[str] = None
    #: The ID of the organization to which this application belongs.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: The ID of the policy which permits usage of this application.
    #: example: ``
    policy_id: Optional[str] = None
    #: A unique identifier for the application.
    #: example: Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OLzEyMzQ1Njc4LTkwYWItY2RlZi0xMjM0LTU2Nzg5MGFiY2RlZg
    app_id: Optional[str] = None
    #: A descriptive name for the application.
    #: example: My Great App
    app_name: Optional[str] = None
    #: The application's Oauth client ID.
    #: example: C1234567890ABCDEF
    app_client_id: Optional[str] = None
    #: URL for the application's privacy policy.
    #: example: https://www.example.com/privacy-policy
    app_privacy_url: Optional[str] = None
    #: URL for the application's support information.
    #: example: https://help.example.com/
    app_support_url: Optional[str] = None
    #: URL for the application's maintainer.
    #: example: https://www.example.com
    app_company_url: Optional[str] = None
    #: Contact name for the application.
    #: example: John Andersen
    app_contact_name: Optional[str] = None
    #: Contact email for the application.
    #: example: info@example.com
    app_contact_email: Optional[str] = None
    #: How many users use the application.
    #: example: 5
    app_user_adoption: Optional[int] = None
    #: Whether or not the application is allowed by policy.
    #: example: allow
    policy_action: Optional[ApplicationUsagePolicyAction] = None
    #: The date and time the application was created.
    #: example: 2017-10-01T07:00:00.000Z
    app_created: Optional[datetime] = None
    #: The date and time this application's usage was last updated.
    #: example: 2018-10-01T07:00:00.000Z
    last_updated: Optional[datetime] = None


class ListApplicationUsageOrderBy(str, Enum):
    is_featured = 'isFeatured'
    last_submission_date = 'lastSubmissionDate'
    policy = 'policy'
    app_name = 'appName'
    name = 'name'


class ApplicationUsageApi(ApiChild, base='application/usage'):
    """
    Application Usage
    
    """

    def list_application_usage(self, app_name: str = None, app_id: str = None,
                               order_by: ListApplicationUsageOrderBy = None, cursor: str = None, org_id: str = None,
                               **params) -> Generator[ApplicationUsage, None, None]:
        """
        List Application Usage

        Lists all applications, optionally filtered by organization ID, application name, or application ID.

        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param app_name: List application usage information for applications with this name.
        :type app_name: str
        :param app_id: List application usage for an application, by ID.
        :type app_id: str
        :param order_by: Sort results.
        :type order_by: ListApplicationUsageOrderBy
        :param cursor: The current cursor when `paging
            <https://developer.webex.com/docs/basics#pagination>`_ through long result sets.
        :type cursor: str
        :param org_id: List application usage for applications owned by this organization, by ID.
        :type org_id: str
        :return: Generator yielding :class:`ApplicationUsage` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if app_name is not None:
            params['appName'] = app_name
        if app_id is not None:
            params['appId'] = app_id
        if order_by is not None:
            params['orderBy'] = enum_str(order_by)
        if cursor is not None:
            params['cursor'] = cursor
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ApplicationUsage, item_key='items', params=params)

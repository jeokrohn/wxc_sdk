"""
Organizations
A set of people in Webex. Organizations may manage other organizations or be managed themselves. This organizations
resource can be accessed only by an admin.

Applications can delete an Organization only after they have been authorized by a user with the Full Administrator
Role which may be a user in the customer org or a user in a managing partner organization to which the role has been
granted. The authorizing admin must grant the spark-admin:organizations-write scope.
"""

__all__ = ['Organization', 'OrganizationApi']

import datetime

from pydantic import parse_obj_as, Field

from ..api_child import ApiChild
from ..base import ApiModel


class Organization(ApiModel):
    #: A unique identifier for the organization.
    org_id: str = Field(alias='id')
    #: Full name of the organization.
    display_name: str
    #: The date and time the organization was created.
    created: datetime.datetime


class OrganizationApi(ApiChild, base='organizations'):
    def list(self) -> list[Organization]:
        """
        List all organizations visible by your account. The results will not be paginated.

        :return: list of Organizations
        """
        data = self.get(url=self.ep())
        return parse_obj_as(list[Organization], data['items'])

    def details(self, org_id: str) -> Organization:
        """
        Get Organization Details

        Shows details for an organization, by ID.

        :param org_id: The unique identifier for the organization.
        :type org_id: str
        :return: org details
        :rtype: :class:`Organization`
        """
        url = self.ep(org_id)
        data = self.get(url=url)
        return Organization.parse_obj(data)

    def delete(self, org_id: str):
        """
        Delete Organization

        Deletes an organization, by ID. It may take up to 10 minutes for the organization to be deleted after the
        response is returned.

        :param org_id: The unique identifier for the organization.
        :type org_id: str
        """
        url = self.ep(org_id)
        super().delete(url=url)

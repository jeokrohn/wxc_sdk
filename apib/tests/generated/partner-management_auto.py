from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['IdentityManagedOrg', 'PartnerAdminUser', 'PartnerAdministratorsApi']


class IdentityManagedOrg(ApiModel):
    #: The org ID of the managed org.
    #: example: Y2LZY29ZCGFYAZOVL3VZL1BFT1BMRS9MNWIZNJE4NY1JOGRKLTQ3MJCTOGIYZI1MOWM0NDDMMJKWNDY
    org_id: Optional[str] = None
    #: role ID of the user to this org.
    #: example: YXRSYXMTCG9YDGFSLNBHCNRUZXIUC2FSZXNMDWXSYWRTAW4=
    role: Optional[str] = None


class PartnerAdminUser(ApiModel):
    #: The user ID of the partner admin.
    #: example: Y2LZY29ZCGFYAZOVL3VZL1BFT1BMRS9JOTYWOTZIYI1KYTRHLTQ3NZETYTC2ZI1KNDEZODQWZWVM1TQ
    id: Optional[str] = None
    #: The display name of the partner admin.
    #: example: display name
    display_name: Optional[str] = None
    #: The first name of the partner admin.
    #: example: John
    first_name: Optional[str] = None
    #: The last name of the partner admin.
    #: example: Doe
    last_name: Optional[str] = None
    #: List of emails for the partner admin.
    #: example: ['johndoe@example.com']
    emails: Optional[list[str]] = None
    #: The role of this partner admin in the given customer org.
    #: example: id_full_admin
    role_in_customer_org: Optional[str] = None


class PartnerAdministratorsApi(ApiChild, base='partner/organizations'):
    """
    Partner Administrators
    
    Partner organizations that manage their customers through Webex Partner Hub can leverage this API to assign or
    unassign partner administrator roles to their users, as well as assign or unassign customer organizations to
    specific partner administrators.
    Managing other partner administrators in an organization requires the partner full administrator role. The users
    being acted upon also exist in the partners own organization. To create a user, see `People API
    <https://developer.webex.com/docs/api/v1/people>`_. The authorizing
    admin must grant the spark-admin:organizations-read scope for read operations and spark-admin:organizations-write
    scope for write operations.
    """

    def get_all_customers_managed_by_a_partner_admin(self, managed_by: str) -> list[IdentityManagedOrg]:
        """
        Get all customers managed by a partner admin

        Get all customers managed by given partner admin, in the `managedBy` request parameter.

        This API can be used by partner full admin and partner readonly admin.

        Specify the `personId` in the `managedBy` parameter in the URI.

        :param managed_by: List customer orgs associated with this person ID.
        :type managed_by: str
        :rtype: list[IdentityManagedOrg]
        """
        params = {}
        params['managedBy'] = managed_by
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[IdentityManagedOrg]).validate_python(data['items'])
        return r

    def get_all_partner_admins_assigned_to_a_customer(self, org_id: str) -> list[PartnerAdminUser]:
        """
        Get all partner admins assigned to a customer

        For a given customer, get all the partner admins with their role details.

        This API can be used by partner full admin.

        Specify the `orgId` in the path parameter.

        :param org_id: List partner admins associated with this customer org ID.
        :type org_id: str
        :rtype: list[PartnerAdminUser]
        """
        url = self.ep(f'{org_id}/partnerAdmins')
        data = super().get(url)
        r = TypeAdapter(list[PartnerAdminUser]).validate_python(data['items'])
        return r

    def assign_partner_admin_to_a_customer(self, org_id: str, person_id: str):
        """
        Assign partner admin to a customer

        Assign a specific partner admin to a customer organization. The partner admin is a user that has the partner
        administrator role.
        Other partner roles, such as partner full administrator are not applicable for this API, since this role
        manages all customer organizations.

        This API can be used by partner full admin.

        Specify the `orgId` and the `personId` in the path param.

        :param org_id: The ID of the customer organization.
        :type org_id: str
        :param person_id: User ID of the partner admin in the partners org.
        :type person_id: str
        :rtype: None
        """
        url = self.ep(f'{org_id}/partnerAdmin/{person_id}/assign')
        super().post(url)

    def unassign_partner_admin_from_a_customer(self, org_id: str, person_id: str):
        """
        Unassign partner admin from a customer

        Unassign a specific partner admin from a customer organization. The partner admin is a user that has the
        partner administrator role.
        Unassigning a customer organization from a partner admin does not remove the role from the user.

        This API can be used by partner full admin.

        Specify the `orgId` and the `personId` in the path param.

        :param org_id: The ID of the customer organization.
        :type org_id: str
        :param person_id: User ID of the partner admin in the partners org.
        :type person_id: str
        :rtype: None
        """
        url = self.ep(f'{org_id}/partnerAdmin/{person_id}/unassign')
        super().delete(url)

    def revoke_all_partner_admin_roles_for_a_given_person_id(self, person_id: str):
        """
        Revoke all partner admin roles for a given person ID

        Revoke all partner administrator roles from a user, thereby revoking access to Partner Hub and all managed
        customer organizations.
        This action does not grant or revoke Control Hub administrator roles (e.g. full administrator, user and device
        administrator, etc.).

        This API can be used by partner full admin.

        Specify the `personId` in the path param.

        :param person_id: ID of the user whose partner roles needs to be revoked.
        :type person_id: str
        :rtype: None
        """
        url = self.ep(f'partnerAdmin/{person_id}')
        super().delete(url)

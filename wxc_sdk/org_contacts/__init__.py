from collections.abc import Generator
from datetime import datetime
from typing import Optional, List

from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.people import SipType
from wxc_sdk.scim.users import ScimPhoneNumberType

__all__ = ['ContactPhoneNumber', 'Contact', 'Meta', 'OrganizationContactsApi',
           'ContactEmail', 'EmailType', 'ContactIm',
           'ContactImType', 'UpdateContactPhoneNumbers',
           'PrimaryContactMethod', 'ContactSipAddress', 'ContactAddress']


class PrimaryContactMethod(str, Enum):
    sipaddress = 'SIPADDRESS'
    email = 'EMAIL'
    phone = 'PHONE'
    ims = 'IMS'


class EmailType(str, Enum):
    work = 'WORK'
    home = 'HOME'
    room = 'ROOM'
    other = 'OTHER'


class ContactEmail(ApiModel):
    #: The email address.
    value: Optional[str] = None
    #: The type of the email.
    type: Optional[EmailType] = None
    #: A Boolean value indicating the email status.
    primary: Optional[bool] = None


class ContactSipAddress(ApiModel):
    #: The sipAddress value.
    value: Optional[str] = None
    #: The type of the sipAddress.
    type: Optional[SipType] = None
    #: Designate the primary sipAddress.
    primary: Optional[bool] = None


class ContactImType(str, Enum):
    aim = 'aim'
    cucm_jid = 'cucm-jid'
    gtalk = 'gtalk'
    icq = 'icq'
    msn = 'msn'
    qq = 'qq'
    skype = 'skype'
    webex_messenger_jid = 'webex-messenger-jid'
    webex_squared_jid = 'webex-squared-jid'
    xmpp = 'xmpp'
    yahoo = 'yahoo'
    microsoft_sip_uri = 'microsoft-sip-uri'
    xmpp_fed_jid = 'xmpp-fed-jid'


class ContactIm(ApiModel):
    #: The IMS account value.
    value: Optional[str] = None
    #: The type of the IMS.
    type: Optional[ContactImType] = None
    #: A Boolean value indicating the IMS account status.
    primary: Optional[bool] = None


class ContactPhoneNumber(ApiModel):
    #: The phone number.
    value: Optional[str] = None
    #: The types of the phone numbers.
    type: Optional[ScimPhoneNumberType] = None
    #: A Boolean value indicating the phone number's primary status.
    primary: Optional[bool] = None


class UpdateContactPhoneNumbers(ContactPhoneNumber):
    #: - A String value on the operation, only `delete` is supported now.
    operation: Optional[str] = None


class Meta(ApiModel):
    #: The date and time the contact was created.
    created: Optional[datetime] = None
    #: The date and time the contact was last changed.
    last_modified: Optional[datetime] = None


class ContactAddress(ApiModel):
    city: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    street: Optional[str] = None
    zip_code: Optional[str] = None


class Contact(ApiModel):
    #: Use this to update an existing contact.
    contact_id: Optional[str] = None
    #: "urn:cisco:codev:identity:contact:core:1.0".
    schemas: str = Field(default='urn:cisco:codev:identity:contact:core:1.0')
    #: Response metadata.
    meta: Optional[Meta] = None
    #: The full name of the contact.
    display_name: Optional[str] = None
    #: The first name of the contact.
    first_name: Optional[str] = None
    #: The last name of the contact.
    last_name: Optional[str] = None
    #: The company the contact is working for.
    company_name: Optional[str] = None
    #: The contact's title.
    title: Optional[str] = None
    #: Contact's address
    address: Optional[str] = None
    #: Contact's address details
    address_info: Optional[ContactAddress] = None
    #: The URL to the person's avatar in PNG format.
    avatar_url: Optional[str] = Field(alias='avatarURL', default=None)
    #: The contact's primary contact method.
    primary_contact_method: Optional[PrimaryContactMethod] = None
    #: Where the data come from.
    source: Optional[str] = None
    is_migration: Optional[bool] = None
    org_id: Optional[str] = None
    #: A list of the user's email addresses with an indicator of the user's primary email address.
    emails: Optional[list[ContactEmail]] = None
    #: A list of user's phone numbers with an indicator of primary to specify the user's main number.
    phone_numbers: Optional[list[ContactPhoneNumber]] = None
    #: The sipAddress values for the user.
    sip_addresses: Optional[list[ContactSipAddress]] = None
    #: Instant messaging addresses for the user.
    ims: Optional[list[ContactIm]] = None
    #: Groups associated with the contact.
    group_ids: Optional[list[str]] = None

    def create(self) -> dict:
        """

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_unset=True)


class BulkFailed(ApiModel):
    #: Bulk ID of the contact object that failed creation.
    id: Optional[str] = None
    #: Error message for the contact creation failure.
    error_message: Optional[str] = None
    #: HTTP Response code for the contact creation failure.
    error_code: Optional[str] = None
    status_code: Optional[int]


class BulkResponse(ApiModel):
    #: Array of contact successfully created.
    contacts: list[Optional[Contact]]
    #: Array of contacts that failed creation.
    failed_contacts: list[BulkFailed]
    #: Organization ID in which the contacts were created.
    org_id: str


class OrganizationContactsApi(ApiChild, base='contacts/organizations'):
    """
    Organization Contacts

    Organizational contacts are entities that can be created, imported, or synchronized with Webex. Searching and
    viewing contacts require an auth token with a `scope
    <https://developer.webex.com/docs/integrations#scopes>`_ of `Identity:contact` or `Identity:SCIM`, while adding,
    updating, and removing contacts in your Organization requires an administrator auth token with the
    `Identity:contact` or `Identity:SCIM` scope. An admin can only operate on the contacts list for his org or a
    managed org.

    **Note**:

    * `broadworks-connector` entitled callers are limited to org contacts with either source=`CH` or
      source=`Webex4Broadworks`, while non-entitled callers are limited to source=`CH`.

    * The `orgId` used in the path for this API are the org UUIDs. They follow a xxxx-xxxx-xxxx-xxxx pattern. If you
      have an orgId in base64 encoded format (starting with Y2.....) you need to base64 decode the id and extract the
      UUID from the slug, before you use it in your API call.
    """

    def create(self, org_id: str, contact: Contact) -> Contact:
        """
        Create a Contact

        Creating a new contact for a given organization requires an org admin role.

        At least one of the following body parameters: `phoneNumbers`, `emails`, `sipAddresses` is required to create a
        new contact for source "CH",
        `displayName` is required to create a new contact for source "Webex4Broadworks".

        Use the optional `groupIds` field to add group IDs in an array within the organisation contact. This will
        become a group contact.

        :param org_id: Webex Identity assigned organization identifier for the user's organization or the organization
            he manages.
        :type org_id: str
        :param contact: The contact to create.
        :type contact: Contact
        :rtype: None
        """
        body = contact.create()
        body['schemas'] = 'urn:cisco:codev:identity:contact:core:1.0'
        url = self.ep(f'{org_id}/contacts')
        data = super().post(url, json=body)
        return Contact.model_validate(data)

    def get(self, org_id: str, contact_id: str) -> Contact:
        """
        Get a Contact

        Shows details for an organization contact by ID.
        Specify the organization ID in the `orgId` parameter in the URI, and specify the contact ID in the `contactId`
        parameter in the URI.

        **NOTE**:
        The `orgId` used in the path for this API are the org UUIDs. They follow a xxxx-xxxx-xxxx-xxxx pattern. If you
        have an orgId in base64 encoded format (starting with Y2.....) you need to base64 decode the id and extract
        the UUID from the slug, before you use it in your API call.

        :param org_id: Webex Identity assigned organization identifier for the user's organization or the organization
            he manages.
        :type org_id: str
        :param contact_id: The contact ID.
        :type contact_id: str
        :rtype: :class:`Contact`
        """
        url = self.ep(f'{org_id}/contacts/{contact_id}')
        data = super().get(url)
        r = Contact.model_validate(data)
        return r

    def update(self, org_id: str, contact_id: str, update: Contact):
        """
        Update a Contact

        Update details for contact by ID. Only an admin can update a contact.
        Specify the organization ID in the `orgId` parameter in the URI, and specify the contact ID in the `contactId`
        parameter in the URI.

        Use the optional `groupIds` field to update the group IDs by changing the existing array. You can add or remove
        one or all groups. To remove all associated groups, pass an empty array in the `groupIds` field.

        :param org_id: Webex Identity assigned organization identifier for the user's organization or the organization
            he manages.
        :type org_id: str
        :param contact_id: The contact ID.
        :type contact_id: str
        :param update: the update
        :type update: Contact
        :rtype: None
        """
        body = update.create()
        url = self.ep(f'{org_id}/contacts/{contact_id}')
        super().patch(url, json=body)

    def delete(self, org_id: str, contact_id: str):
        """
        Delete a Contact

        Remove a contact from the organization. Only an admin can remove a contact.

        Specify the organization ID in the `orgId` parameter in the URI, and specify the contact ID in the `contactId`
        parameter in the URI.

        :param org_id: Webex Identity assigned organization identifier for the user's organization or the organization
            he manages.
        :type org_id: str
        :param contact_id: The contact ID.
        :type contact_id: str
        :rtype: None
        """
        url = self.ep(f'{org_id}/contacts/{contact_id}')
        super().delete(url)

    def list(self, org_id: str, keyword: str = None, source: str = None, limit: int = None,
             group_ids: list[str] = None) -> Generator[Contact, None, None]:
        """
        List Contacts

        List contacts in the organization. The default limit is `100`.

        `keyword` can be the value of "displayName", "firstName", "lastName", "email". An empty string of `keyword`
        means get all contacts.

        `groupIds` is a comma separated list group IDs. Results are filtered based on those group IDs.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param org_id: The organization ID.
        :type org_id: str
        :param keyword: List contacts with a keyword.
        :type keyword: str
        :param source: List contacts with source.
        :type source: str
        :param limit: Limit the maximum number of contact in the response.
        + Default: 100
        :type limit: int
        :param group_ids: Filter contacts based on groups.
        :type group_ids: list[str]
        """
        params = {}
        if keyword is not None:
            params['keyword'] = keyword
        if source is not None:
            params['source'] = source
        if limit is not None:
            params['limit'] = limit
        if group_ids is not None:
            params['groupIds'] = ','.join(group_ids)
        url = self.ep(f'{org_id}/contacts/search')
        return self.session.follow_pagination(url, params=params, item_key='result', model=Contact)

    def bulk_create_or_update(self, org_id: str, contacts: List[Contact]) -> BulkResponse:
        """
        Bulk Create or Update Contacts

        Create or update contacts in bulk. Update an existing contact by specifying the contact ID in the `contactId`
        parameter in the request body.

        :param org_id: Webex Identity assigned organization identifier for the user's organization or the organization
            he manages.
        :type org_id: str
        :param contacts: Contains a list of contacts to be created/updated.
        :type contacts: list[BulkCreateContact]
        :rtype: None
        """
        body = dict()
        body['schemas'] = 'urn:cisco:codev:identity:contact:core:1.0'
        body['contacts'] = TypeAdapter(list[Contact]).dump_python(contacts, mode='json', by_alias=True,
                                                                  exclude_unset=True)
        url = self.ep(f'{org_id}/contacts/bulk')
        data = super().post(url, json=body)
        return BulkResponse.model_validate(data)

    def bulk_delete(self, org_id: str, object_ids: List[str]):
        """
        Bulk Delete Contacts

        Delete contacts in bulk.

        :param org_id: Webex Identity assigned organization identifier for the user's organization or the organization
            he manages.
        :type org_id: str
        :param object_ids: List of UUIDs for the contacts.
        :type object_ids: list[str]
        :rtype: None
        """
        body = dict()
        body['schemas'] = 'urn:cisco:codev:identity:contact:core:1.0'
        body['objectIds'] = object_ids
        url = self.ep(f'{org_id}/contacts/bulk/delete')
        super().post(url, json=body)

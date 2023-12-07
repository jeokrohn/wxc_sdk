from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['BulkCreateContacts', 'ContactEmails', 'ContactEmailsType', 'ContactIms', 'ContactImsType',
            'ContactPhoneNumbers', 'ContactPhoneNumbersType', 'ContactPrimaryContactMethod', 'ContactResponse',
            'ContactSipAddresses', 'ContactSipAddressesType', 'ContactSource', 'Meta', 'OrganizationContactsApi',
            'SearchResponse']


class ContactPrimaryContactMethod(str, Enum):
    sipaddress = 'SIPADDRESS'
    email = 'EMAIL'
    phone = 'PHONE'
    ims = 'IMS'


class ContactSource(str, Enum):
    ch = 'CH'
    webex4_broadworks = 'Webex4Broadworks'


class ContactEmailsType(str, Enum):
    work = 'work'
    home = 'home'
    room = 'room'
    other = 'other'


class ContactEmails(ApiModel):
    #: The email address.
    #: example: user1@example.home.com
    value: Optional[str] = None
    #: The type of the email.
    #: example: home
    type: Optional[ContactEmailsType] = None
    #: A Boolean value indicating the email status.
    primary: Optional[bool] = None


class ContactPhoneNumbersType(str, Enum):
    work = 'work'
    home = 'home'
    mobile = 'mobile'
    work_extension = 'work_extension'
    fax = 'fax'
    pager = 'pager'
    other = 'other'


class ContactPhoneNumbers(ApiModel):
    #: The phone number.
    #: example: 400 123 1234
    value: Optional[str] = None
    #: The types of the phone numbers.
    #: example: work
    type: Optional[ContactPhoneNumbersType] = None
    #: A Boolean value indicating the phone number's primary status.
    #: example: True
    primary: Optional[bool] = None
    #: - A String value on the operation, only `delete` is supported now.
    #: example: delete
    operation: Optional[str] = None


class ContactSipAddressesType(str, Enum):
    enterprise = 'enterprise'
    cloud_calling = 'cloud-calling'
    personal_room = 'personal-room'


class ContactSipAddresses(ApiModel):
    #: The sipAddress value.
    #: example: sipAddress value1
    value: Optional[str] = None
    #: The type of the sipAddress.
    #: example: enterprise
    type: Optional[ContactSipAddressesType] = None
    #: Designate the primary sipAddress.
    #: example: True
    primary: Optional[bool] = None


class ContactImsType(str, Enum):
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


class ContactIms(ApiModel):
    #: The IMS account value.
    #: example: aim_account_ID
    value: Optional[str] = None
    #: The type of the IMS.
    #: example: aim
    type: Optional[ContactImsType] = None
    #: A Boolean value indicating the IMS account status.
    #: example: True
    primary: Optional[bool] = None


class BulkCreateContacts(ApiModel):
    #: The full name of the contact.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: The first name of the contact.
    #: example: John
    first_name: Optional[str] = None
    #: The last name of the contact.
    #: example: Andersen
    last_name: Optional[str] = None
    #: The company the contact is working for.
    #: example: Cisco Systems
    company_name: Optional[str] = None
    #: The contact's title.
    #: example: GM
    title: Optional[str] = None
    #: Contact's address.
    #: example: {\"city\" : \"Milpitas\", \"country\" : \"US\", \"street\" : \"1099 Bird Ave.\", \"zipCode\" : \"99212\"}
    address: Optional[str] = None
    #: The URL to the person's avatar in PNG format.
    #: example: https://avatar-prod-us-east-2.webexcontent.com/default_avatar~1600
    avatar_url: Optional[str] = Field(alias='avatarURL', default=None)
    #: The contact's primary contact method.
    #: example: SIPADDRESS
    primary_contact_method: Optional[ContactPrimaryContactMethod] = None
    #: Where the data come from.
    #: example: Webex4Broadworks
    source: Optional[ContactSource] = None
    #: A list of the user's email addresses with an indicator of the user's primary email address.
    emails: Optional[list[ContactEmails]] = None
    #: A list of user's phone numbers with an indicator of primary to specify the user's main number.
    phone_numbers: Optional[list[ContactPhoneNumbers]] = None
    #: The sipAddress values for the user.
    sip_addresses: Optional[list[ContactSipAddresses]] = None
    #: Instant messaging addresses for the user.
    ims: Optional[list[ContactIms]] = None


class Meta(ApiModel):
    #: The date and time the contact was created.
    #: example: 2022-04-29T13:06:26.831Z
    created: Optional[datetime] = None
    #: The date and time the contact was last changed.
    #: example: 2022-05-29T13:06:26.831Z
    last_modified: Optional[datetime] = None


class ContactResponse(ApiModel):
    #: "urn:cisco:codev:identity:contact:core:1.0".
    #: example: urn:cisco:codev:identity:contact:core:1.0
    schemas: Optional[str] = None
    #: Response metadata.
    meta: Optional[Meta] = None
    #: The full name of the contact.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: The first name of the contact.
    #: example: John
    first_name: Optional[str] = None
    #: The last name of the contact.
    #: example: Andersen
    last_name: Optional[str] = None
    #: The company the contact is working for.
    #: example: Cisco Systems
    company_name: Optional[str] = None
    #: The contact's title.
    #: example: GM
    title: Optional[str] = None
    #: Contact's address.
    #: example: {\"city\" : \"Milpitas\", \"country\" : \"US\", \"street\" : \"1099 Bird Ave.\", \"zipCode\" : \"99212\"}
    address: Optional[str] = None
    #: The URL to the person's avatar in PNG format.
    #: example: https://avatar-prod-us-east-2.webexcontent.com/default_avatar~1600
    avatar_url: Optional[str] = Field(alias='avatarURL', default=None)
    #: The contact's primary contact method.
    #: example: SIPADDRESS
    primary_contact_method: Optional[ContactPrimaryContactMethod] = None
    #: Where the data come from.
    #: example: Webex4Broadworks
    source: Optional[ContactSource] = None
    #: A list of the user's email addresses with an indicator of the user's primary email address.
    emails: Optional[list[ContactEmails]] = None
    #: A list of user's phone numbers with an indicator of primary to specify the user's main number.
    phone_numbers: Optional[list[ContactPhoneNumbers]] = None
    #: The sipAddress values for the user.
    sip_addresses: Optional[list[ContactSipAddresses]] = None
    #: Instant messaging addresses for the user.
    ims: Optional[list[ContactIms]] = None


class SearchResponse(ApiModel):
    #: An array of contact objects.
    result: Optional[list[ContactResponse]] = None
    #: Start at the zero-based offset in the list of matching contacts.
    start: Optional[int] = None
    #: Limit the number of contacts returned to this maximum count.
    #: example: 1000
    limit: Optional[int] = None
    #: Total number of contacts returned in search results.
    #: example: 1
    total: Optional[int] = None


class OrganizationContactsApi(ApiChild, base='contacts/organizations/{orgId}/contacts'):
    """
    Organization Contacts
    
    Organizational contacts are entities that can be created, imported, or synchronized with Webex. Searching and
    viewing contacts require an auth token with a `scope
    <https://developer.webex.com/docs/integrations#scopes>`_ of `Identity:contact` or `Identity:SCIM`, while adding,
    updating, and removing contacts in your Organization requires an administrator auth token with the
    `Identity:contact` or `Identity:SCIM` scope. An admin can only operate on the contacts list for his org or a
    managed org.
    
    Note: `broadworks-connector` entitled callers are limited to org contacts with either source=`CH` or
    source=`Webex4Broadworks`, while non-entitled callers are limited to source=`CH`.
    """

    def create_a_contact(self, org_id: str, schemas: str, display_name: str, first_name: str, last_name: str,
                         company_name: str, title: str, address: str, avatar_url: str,
                         primary_contact_method: ContactPrimaryContactMethod, source: ContactSource,
                         emails: list[ContactEmails], phone_numbers: list[ContactPhoneNumbers],
                         sip_addresses: list[ContactSipAddresses], ims: list[ContactIms]):
        """
        Create a Contact

        Creating a new contact for a given organization requires an org admin role.

        At least one of the following body parameters: `phoneNumbers`, `emails`, `sipAddresses` is required to create a
        new contact for source "CH",
        `displayName` is required to create a new contact for source "Webex4Broadworks".

        :param org_id: Webex Identity assigned organization identifier for the user's organization or the organization
            he manages.
        :type org_id: str
        :param schemas: "urn:cisco:codev:identity:contact:core:1.0".
        :type schemas: str
        :param display_name: The full name of the contact.
        :type display_name: str
        :param first_name: The first name of the contact.
        :type first_name: str
        :param last_name: The last name of the contact.
        :type last_name: str
        :param company_name: The company the contact is working for.
        :type company_name: str
        :param title: The contact's title.
        :type title: str
        :param address: Contact's address.
        :type address: str
        :param avatar_url: The URL to the person's avatar in PNG format.
        :type avatar_url: str
        :param primary_contact_method: The contact's primary contact method.
        :type primary_contact_method: ContactPrimaryContactMethod
        :param source: Where the data come from.
        :type source: ContactSource
        :param emails: A list of the user's email addresses with an indicator of the user's primary email address.
        :type emails: list[ContactEmails]
        :param phone_numbers: A list of user's phone numbers with an indicator of primary to specify the user's main
            number.
        :type phone_numbers: list[ContactPhoneNumbers]
        :param sip_addresses: The sipAddress values for the user.
        :type sip_addresses: list[ContactSipAddresses]
        :param ims: Instant messaging addresses for the user.
        :type ims: list[ContactIms]
        :rtype: None
        """
        body = dict()
        body['schemas'] = schemas
        body['displayName'] = display_name
        body['firstName'] = first_name
        body['lastName'] = last_name
        body['companyName'] = company_name
        body['title'] = title
        body['address'] = address
        body['avatarURL'] = avatar_url
        body['primaryContactMethod'] = enum_str(primary_contact_method)
        body['source'] = enum_str(source)
        body['emails'] = loads(TypeAdapter(list[ContactEmails]).dump_json(emails, by_alias=True, exclude_none=True))
        body['phoneNumbers'] = loads(TypeAdapter(list[ContactPhoneNumbers]).dump_json(phone_numbers, by_alias=True, exclude_none=True))
        body['sipAddresses'] = loads(TypeAdapter(list[ContactSipAddresses]).dump_json(sip_addresses, by_alias=True, exclude_none=True))
        body['ims'] = loads(TypeAdapter(list[ContactIms]).dump_json(ims, by_alias=True, exclude_none=True))
        url = self.ep(f'')
        super().post(url, json=body)

    def get_a_contact(self, org_id: str, contact_id: str) -> ContactResponse:
        """
        Get a Contact

        Shows details for an organization contact by ID.
        Specify the organization ID in the `orgId` parameter in the URI, and specify the contact ID in the `contactId`
        parameter in the URI.

        :param org_id: Webex Identity assigned organization identifier for the user's organization or the organization
            he manages.
        :type org_id: str
        :param contact_id: The contact ID.
        :type contact_id: str
        :rtype: :class:`ContactResponse`
        """
        url = self.ep(f'{contact_id}')
        data = super().get(url)
        r = ContactResponse.model_validate(data)
        return r

    def update_a_contact(self, org_id: str, contact_id: str, schemas: str, display_name: str, first_name: str,
                         last_name: str, company_name: str, title: str, address: str, avatar_url: str,
                         primary_contact_method: ContactPrimaryContactMethod, source: ContactSource,
                         emails: list[ContactEmails], phone_numbers: list[ContactPhoneNumbers],
                         sip_addresses: list[ContactSipAddresses], ims: list[ContactIms]):
        """
        Update a Contact

        Update details for contact by ID. Only an admin can update a contact.
        Specify the organization ID in the `orgId` parameter in the URI, and specify the contact ID in the `contactId`
        parameter in the URI.

        :param org_id: Webex Identity assigned organization identifier for the user's organization or the organization
            he manages.
        :type org_id: str
        :param contact_id: The contact ID.
        :type contact_id: str
        :param schemas: "urn:cisco:codev:identity:contact:core:1.0".
        :type schemas: str
        :param display_name: The full name of the contact.
        :type display_name: str
        :param first_name: The first name of the contact.
        :type first_name: str
        :param last_name: The last name of the contact.
        :type last_name: str
        :param company_name: The company the contact is working for.
        :type company_name: str
        :param title: The contact's title.
        :type title: str
        :param address: Contact's address.
        :type address: str
        :param avatar_url: The URL to the person's avatar in PNG format.
        :type avatar_url: str
        :param primary_contact_method: The contact's primary contact method.
        :type primary_contact_method: ContactPrimaryContactMethod
        :param source: Where the data come from.
        :type source: ContactSource
        :param emails: A list of the user's email addresses with an indicator of the user's primary email address.
        :type emails: list[ContactEmails]
        :param phone_numbers: A list of user's phone numbers with an indicator of primary to specify the user's main
            number.
        :type phone_numbers: list[ContactPhoneNumbers]
        :param sip_addresses: The sipAddress values for the user.
        :type sip_addresses: list[ContactSipAddresses]
        :param ims: Instant messaging addresses for the user.
        :type ims: list[ContactIms]
        :rtype: None
        """
        body = dict()
        body['schemas'] = schemas
        body['displayName'] = display_name
        body['firstName'] = first_name
        body['lastName'] = last_name
        body['companyName'] = company_name
        body['title'] = title
        body['address'] = address
        body['avatarURL'] = avatar_url
        body['primaryContactMethod'] = enum_str(primary_contact_method)
        body['source'] = enum_str(source)
        body['emails'] = loads(TypeAdapter(list[ContactEmails]).dump_json(emails, by_alias=True, exclude_none=True))
        body['phoneNumbers'] = loads(TypeAdapter(list[ContactPhoneNumbers]).dump_json(phone_numbers, by_alias=True, exclude_none=True))
        body['sipAddresses'] = loads(TypeAdapter(list[ContactSipAddresses]).dump_json(sip_addresses, by_alias=True, exclude_none=True))
        body['ims'] = loads(TypeAdapter(list[ContactIms]).dump_json(ims, by_alias=True, exclude_none=True))
        url = self.ep(f'{contact_id}')
        super().patch(url, json=body)

    def delete_a_contact(self, org_id: str, contact_id: str):
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
        url = self.ep(f'{contact_id}')
        super().delete(url)

    def list_contacts(self, org_id: str, keyword: str = None, limit: int = None, source: str = None) -> SearchResponse:
        """
        List Contacts

        List contacts in the organization. The default limit is `1000`.

        `keyword` can be the value of "displayName", "firstName", "lastName", "email". An empty string of `keyword`
        means get all contacts.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param org_id: The organization ID.
        :type org_id: str
        :param keyword: List contacts with a keyword.
        :type keyword: str
        :param limit: Limit the maximum number of contact in the response.
        + Default: 1000
        :type limit: int
        :param source: List contacts with source.
        :type source: str
        :rtype: :class:`SearchResponse`
        """
        params = {}
        if keyword is not None:
            params['keyword'] = keyword
        if limit is not None:
            params['limit'] = limit
        if source is not None:
            params['source'] = source
        url = self.ep(f'search')
        data = super().get(url, params=params)
        r = SearchResponse.model_validate(data)
        return r

    def bulk_create_or_update_contacts(self, org_id: str, schemas: str, contacts: list[BulkCreateContacts]):
        """
        Bulk Create or Update Contacts

        Create or update contacts in bulk.

        :param org_id: Webex Identity assigned organization identifier for the user's organization or the organization
            he manages.
        :type org_id: str
        :param schemas: "urn:cisco:codev:identity:contact:core:1.0".
        :type schemas: str
        :param contacts: Contains a list of contacts to be created/updated.
        :type contacts: list[BulkCreateContacts]
        :rtype: None
        """
        body = dict()
        body['schemas'] = schemas
        body['contacts'] = loads(TypeAdapter(list[BulkCreateContacts]).dump_json(contacts, by_alias=True, exclude_none=True))
        url = self.ep(f'bulk')
        super().post(url, json=body)

    def bulk_delete_contacts(self, org_id: str, schemas: str, object_ids: list[str]):
        """
        Bulk Delete Contacts

        Delete contacts in bulk.

        :param org_id: Webex Identity assigned organization identifier for the user's organization or the organization
            he manages.
        :type org_id: str
        :param schemas: "urn:cisco:codev:identity:contact:core:1.0".
        :type schemas: str
        :param object_ids: List of UUIDs for the contacts.
        :type object_ids: list[str]
        :rtype: None
        """
        body = dict()
        body['schemas'] = schemas
        body['objectIds'] = object_ids
        url = self.ep(f'bulk/delete')
        super().post(url, json=body)

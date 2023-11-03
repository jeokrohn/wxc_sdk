from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['BulkCreate', 'BulkCreateContacts', 'BulkDelete', 'Contact', 'ContactEmails', 'ContactEmailsType',
            'ContactIms', 'ContactImsType', 'ContactPhoneNumbers', 'ContactPhoneNumbersType',
            'ContactPrimaryContactMethod', 'ContactResponse', 'ContactSipAddresses', 'ContactSipAddressesType',
            'ContactSource', 'Meta', 'SearchResponse']


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


class Contact(ApiModel):
    #: "urn:cisco:codev:identity:contact:core:1.0".
    #: example: urn:cisco:codev:identity:contact:core:1.0
    schemas: Optional[str] = None
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


class BulkCreate(ApiModel):
    #: "urn:cisco:codev:identity:contact:core:1.0".
    #: example: urn:cisco:codev:identity:contact:core:1.0
    schemas: Optional[str] = None
    #: Contains a list of contacts to be created/updated.
    contacts: Optional[list[BulkCreateContacts]] = None


class BulkDelete(ApiModel):
    #: "urn:cisco:codev:identity:contact:core:1.0".
    #: example: urn:cisco:codev:identity:contact:core:1.0
    schemas: Optional[str] = None
    #: List of UUIDs for the contacts.
    #: example: ['8a5fac49-2c5f-4773-aec7-02db0e3a9d72']
    object_ids: Optional[list[str]] = None


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
    #: example: 1000.0
    limit: Optional[int] = None
    #: Total number of contacts returned in search results.
    #: example: 1.0
    total: Optional[int] = None

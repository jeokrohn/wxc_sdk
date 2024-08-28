from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CreateAPersonPhoneNumbers', 'CreateAPersonPhoneNumbersType', 'PeopleApi', 'Person', 'PersonAddresses',
           'PersonPhoneNumbers', 'PersonPhoneNumbersType', 'PersonSipAddresses', 'PersonSipAddressesType',
           'PersonStatus', 'PersonType']


class PersonPhoneNumbersType(str, Enum):
    #: Work phone number of the person.
    work = 'work'
    #: Work extension of the person. For the Webex Calling person, the value will have a routing prefix along with the
    #: extension.
    work_extension = 'work_extension'
    #: Mobile number of the person.
    mobile = 'mobile'
    #: FAX number of the person.
    fax = 'fax'


class PersonPhoneNumbers(ApiModel):
    #: The type of phone number.
    #: example: work
    type: Optional[PersonPhoneNumbersType] = None
    #: The phone number.
    #: example: +1 408 526 7209
    value: Optional[str] = None
    #: Primary number for the person.
    #: example: True
    primary: Optional[bool] = None


class PersonAddresses(ApiModel):
    #: The type of address.
    #: example: work
    type: Optional[str] = None
    #: The user's country.
    #: example: US
    country: Optional[str] = None
    #: The user's locality, often city.
    #: example: Milpitas
    locality: Optional[str] = None
    #: The user's region, often state.
    #: example: California
    region: Optional[str] = None
    #: The user's street.
    #: example: 1099 Bird Ave.
    street_address: Optional[str] = None
    #: The user's postal or zip code.
    #: example: 99212
    postal_code: Optional[str] = None


class PersonSipAddressesType(str, Enum):
    #: Personal room address.
    personal_room = 'personal-room'
    #: Enterprise address.
    enterprise = 'enterprise'
    #: Cloud calling address.
    cloud_calling = 'cloud-calling'


class PersonSipAddresses(ApiModel):
    #: The type of SIP address.
    #: example: personal-room
    type: Optional[PersonSipAddressesType] = None
    #: The SIP address.
    #: example: testuser5@mycompany.webex.com
    value: Optional[str] = None
    #: Primary SIP address of the person.
    primary: Optional[bool] = None


class PersonStatus(str, Enum):
    #: Active within the last 10 minutes.
    active = 'active'
    #: The user is in a call.
    call = 'call'
    #: The user has manually set their status to "Do Not Disturb".
    do_not_disturb = 'DoNotDisturb'
    #: Last activity occurred more than 10 minutes ago.
    inactive = 'inactive'
    #: The user is in a meeting.
    meeting = 'meeting'
    #: The user or a Hybrid Calendar service has indicated that they are "Out of Office".
    out_of_office = 'OutOfOffice'
    #: The user has never logged in; a status cannot be determined.
    pending = 'pending'
    #: The user is sharing content.
    presenting = 'presenting'
    #: The user’s status could not be determined.
    unknown = 'unknown'


class PersonType(str, Enum):
    #: Account belongs to a person.
    person = 'person'
    #: Account is a bot user.
    bot = 'bot'
    #: Account is a `guest user
    #: <https://developer.webex.com/docs/guest-issuer>`_.
    appuser = 'appuser'


class Person(ApiModel):
    #: A unique identifier for the person.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    id: Optional[str] = None
    #: The email addresses of the person.
    #: example: ['john.andersen@example.com']
    emails: Optional[list[str]] = None
    #: Phone numbers for the person.
    phone_numbers: Optional[list[PersonPhoneNumbers]] = None
    #: The Webex Calling extension for the person. Only applies to a person with a Webex Calling license.
    #: example: 133
    extension: Optional[str] = None
    #: The ID of the location for this person retrieved from BroadCloud.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzYzNzE1
    location_id: Optional[str] = None
    #: The full name of the person.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: The nickname of the person if configured. If no nickname is configured for the person, this field will not be
    #: present.
    #: example: John
    nick_name: Optional[str] = None
    #: The first name of the person.
    #: example: John
    first_name: Optional[str] = None
    #: The last name of the person.
    #: example: Andersen
    last_name: Optional[str] = None
    #: The URL to the person's avatar in PNG format.
    #: example: https://1efa7a94ed21783e352-c62266528714497a17239ececf39e9e2.ssl.cf1.rackcdn.com/V1~54c844c89e678e5a7b16a306bc2897b9~wx29yGtlTpilEFlYzqPKag==~1600
    avatar: Optional[str] = None
    #: The ID of the organization to which this person belongs.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: An array of role strings representing the roles to which this admin user belongs.
    #: example: ['Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh', 'Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi']
    roles: Optional[list[str]] = None
    #: An array of license strings allocated to this person.
    #: example: ['Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh', 'Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi']
    licenses: Optional[list[str]] = None
    #: The business department the user belongs to.
    #: example: Sales
    department: Optional[str] = None
    #: A manager identifier.
    #: example: John Duarte
    manager: Optional[str] = None
    #: Person ID of the manager.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80ZGEzYTI0OC05YjBhLTQxMDgtODU0NC1iNTQwMzEyZTU2M2E
    manager_id: Optional[str] = None
    #: The person's title.
    #: example: GM
    title: Optional[str] = None
    #: A person's addresses.
    addresses: Optional[list[PersonAddresses]] = None
    #: The date and time the person was created.
    #: example: 2015-10-18T14:26:16.000Z
    created: Optional[datetime] = None
    #: The date and time the person was last changed.
    #: example: 2015-10-18T14:26:16.000Z
    last_modified: Optional[datetime] = None
    #: The time zone of the person if configured. If no timezone is configured on the account, this field will not be
    #: present.
    #: example: America/Denver
    timezone: Optional[str] = None
    #: The date and time of the person's last activity within Webex. This will only be returned for people within your
    #: organization or an organization you manage. Presence information will not be shown if the authenticated user
    #: has `disabled status sharing
    #: <https://help.webex.com/nkzs6wl/>`_.
    #: example: 2015-10-18T14:26:16.028Z
    last_activity: Optional[datetime] = None
    #: One or several site names where this user has a role (host or attendee).
    #: example: ['mysite.webex.com#attendee']
    site_urls: Optional[list[str]] = None
    #: The user's SIP addresses. Read-only.
    sip_addresses: Optional[list[PersonSipAddresses]] = None
    #: Identifier for intra-domain federation with other XMPP based messenger systems.
    #: example: user@example.com
    xmpp_federation_jid: Optional[str] = None
    #: The current presence status of the person. This will only be returned for people within your organization or an
    #: organization you manage. Presence information will not be shown if the authenticated user has
    #: `disabled status sharing
    #: <https://help.webex.com/nkzs6wl/>`_. Presence status is different from Control Hub's "Last Service Access Time" which
    #: indicates the last time an oAuth token was issued for this user.
    #: example: active
    status: Optional[PersonStatus] = None
    #: Whether or not an invite is pending for the user to complete account activation. This property is only returned
    #: if the authenticated user is an admin user for the person's organization.
    invite_pending: Optional[bool] = None
    #: Whether or not the user is allowed to use Webex. This property is only returned if the authenticated user is an
    #: admin user for the person's organization.
    #: example: True
    login_enabled: Optional[bool] = None
    #: The type of person account, such as person or bot.
    #: example: person
    type: Optional[PersonType] = None


class CreateAPersonPhoneNumbersType(str, Enum):
    work = 'work'


class CreateAPersonPhoneNumbers(ApiModel):
    #: The type of phone number.
    #: example: work
    type: Optional[CreateAPersonPhoneNumbersType] = None
    #: The phone number.
    #: example: 408 526 7209
    value: Optional[str] = None


class PeopleApi(ApiChild, base='people'):
    """
    People
    
    As of January 2024, the Webex APIs have been fully upgraded to support the
    industry-standard [SCIM
    2.0](https://developer.webex.com/docs/api/v1/scim2-user) protocol, which is
    used for user and group management, provisioning, and maintenance. Developers
    are advised to use this API instead of the people API, due to its higher
    performance and readily available connectors. Users created via SCIM should be
    licensed using the /licenses API, even in large quantities, using the new
    [PATCH method](https://developer.webex.com/docs/api/v1/licenses/assign-
    licenses-to-users).
    
    
    
    People are registered users of Webex. Searching and viewing People requires an auth token with a `scope
    <https://developer.webex.com/docs/integrations#scopes>`_ of
    `spark:people_read`. Viewing the list of all People in your organization requires an administrator auth token with
    `spark-admin:people_read` scope. Adding, updating, and removing People requires an administrator auth token with
    the `spark-admin:people_write` and `spark-admin:people_read` scope.
    
    A person's call settings are for `Webex Calling` and necessitate Webex Calling licenses.
    
    To learn more about managing people in a room see the `Memberships API
    <https://developer.webex.com/docs/api/v1/memberships>`_. For information about how to allocate Hybrid
    Services licenses to people, see the `Managing Hybrid Services
    <https://developer.webex.com/docs/api/guides/managing-hybrid-services-licenses>`_ guide.
    """

    def list_people(self, email: str = None, display_name: str = None, id: str = None, roles: str = None,
                    calling_data: bool = None, location_id: str = None, org_id: str = None,
                    **params) -> Generator[Person, None, None]:
        """
        List People

        List people in your organization. For most users, either the `email` or `displayName` parameter is required.
        Admin users can omit these fields and list all users in their organization.

        Response properties associated with a user's presence status, such as `status` or `lastActivity`, will only be
        returned for people within your organization or an organization you manage. Presence information will not be
        returned if the authenticated user has `disabled status sharing
        <https://help.webex.com/nkzs6wl/>`_. Calling /people frequently to poll `status`
        information for a large set of users will quickly lead to `429` errros and throttling of such requests and is
        therefore discouraged.

        Admin users can include `Webex Calling` (BroadCloud) user details in the response by specifying `callingData`
        parameter as `true`. Admin users can list all users in a location or with a specific phone number. Admin users
        will receive an enriched payload with additional administrative fields like `licenses`,`roles`, `locations`
        etc. These fields are shown when accessing a user via GET /people/{id}, not when doing a GET /people?id=

        Lookup by `email` is only supported for people within the same org or where a partner admin relationship is in
        place.

        Lookup by `roles` is only supported for Admin users for the people within the same org.

        Long result sets will be split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        :param email: List people with this email address. For non-admin requests, either this or `displayName` are
            required. With the exception of partner admins and a managed org relationship, people lookup by email is
            only available for users in the same org.
        :type email: str
        :param display_name: List people whose name starts with this string. For non-admin requests, either this or
            email are required.
        :type display_name: str
        :param id: List people by ID. Accepts up to 85 person IDs separated by commas. If this parameter is provided
            then presence information (such as the `lastActivity` or `status` properties) will not be included in the
            response.
        :type id: str
        :param roles: List of roleIds separated by commas.
        :type roles: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param location_id: List people present in this location.
        :type location_id: str
        :param org_id: List people in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :return: Generator yielding :class:`Person` instances
        """
        if email is not None:
            params['email'] = email
        if display_name is not None:
            params['displayName'] = display_name
        if id is not None:
            params['id'] = id
        if org_id is not None:
            params['orgId'] = org_id
        if roles is not None:
            params['roles'] = roles
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        if location_id is not None:
            params['locationId'] = location_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Person, item_key='items', params=params)

    def create_a_person(self, emails: list[str], calling_data: bool = None, min_response: bool = None,
                        phone_numbers: list[CreateAPersonPhoneNumbers] = None, extension: str = None,
                        location_id: str = None, display_name: str = None, first_name: str = None,
                        last_name: str = None, avatar: str = None, roles: list[str] = None,
                        licenses: list[str] = None, department: str = None, manager: str = None,
                        manager_id: str = None, title: str = None, addresses: list[PersonAddresses] = None,
                        site_urls: list[str] = None, org_id: str = None) -> Person:
        """
        Create a Person

        Create a new user account for a given organization. Only an admin can create a new user account.

        At least one of the following body parameters is required to create a new user: `displayName`, `firstName`,
        `lastName`.

        Currently, users may have only one email address associated with their account. The `emails` parameter is an
        array, which accepts multiple values to allow for future expansion, but currently only one email address will
        be used for the new user.

        Admin users can include `Webex calling` (BroadCloud) user details in the response by specifying `callingData`
        parameter as true. It may happen that the POST request with calling data returns a 400 status, but the person
        was created still. One way to get into this state is if an invalid phone number is assigned to a user. The
        people API aggregates calls to several other microservices, and one may have failed. A best practice is to
        check if the user exists before retrying. This can be done with the user's email address and a GET /people.

        When doing attendee management, append `#attendee` to the `siteUrl` parameter (e.g.
        `mysite.webex.com#attendee`) to make the new user an attendee for a site.

        **NOTES**:

        * For creating a `Webex Calling` user, you must provide `phoneNumbers` or `extension`, `locationId`, and
        `licenses` string in the same request.

        * `SipAddresses` are asigned via an asynchronous process. This means that the POST response may not show the
        SIPAddresses immediately. Instead you can verify them with a separate GET to /people, after they were newly
        configured.

        :param emails: The email addresses of the person. Only one email address is allowed per person.
        :type emails: list[str]
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param min_response: Set to `true` to improve performance by omitting person details and returning only the ID
            in the response when successful. If unsuccessful the response will have optional error details.
        :type min_response: bool
        :param phone_numbers: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling
            license.
        :type phone_numbers: list[CreateAPersonPhoneNumbers]
        :param extension: Webex Calling extension of the person. This is only settable for a person with a Webex
            Calling license.
        :type extension: str
        :param location_id: The ID of the location for this person.
        :type location_id: str
        :param display_name: The full name of the person.
        :type display_name: str
        :param first_name: The first name of the person.
        :type first_name: str
        :param last_name: The last name of the person.
        :type last_name: str
        :param avatar: The URL to the person's avatar in PNG format.
        :type avatar: str
        :param roles: An array of role strings representing the roles to which this admin user belongs.
        :type roles: list[str]
        :param licenses: An array of license strings allocated to this person.
        :type licenses: list[str]
        :param department: The business department the user belongs to.
        :type department: str
        :param manager: A manager identifier.
        :type manager: str
        :param manager_id: Person ID of the manager.
        :type manager_id: str
        :param title: The person's title.
        :type title: str
        :param addresses: A person's addresses.
        :type addresses: list[PersonAddresses]
        :param site_urls: One or several site names where this user has an attendee role. Append `#attendee` to the
            sitename (e.g.: `mysite.webex.com#attendee`).
        :type site_urls: list[str]
        :param org_id: The ID of the organization to which this person belongs.
        :type org_id: str
        :rtype: :class:`Person`
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        if min_response is not None:
            params['minResponse'] = str(min_response).lower()
        body = dict()
        body['emails'] = emails
        if phone_numbers is not None:
            body['phoneNumbers'] = TypeAdapter(list[CreateAPersonPhoneNumbers]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        if extension is not None:
            body['extension'] = extension
        if location_id is not None:
            body['locationId'] = location_id
        if display_name is not None:
            body['displayName'] = display_name
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if avatar is not None:
            body['avatar'] = avatar
        if org_id is not None:
            body['orgId'] = org_id
        if roles is not None:
            body['roles'] = roles
        if licenses is not None:
            body['licenses'] = licenses
        if department is not None:
            body['department'] = department
        if manager is not None:
            body['manager'] = manager
        if manager_id is not None:
            body['managerId'] = manager_id
        if title is not None:
            body['title'] = title
        if addresses is not None:
            body['addresses'] = TypeAdapter(list[PersonAddresses]).dump_python(addresses, mode='json', by_alias=True, exclude_none=True)
        if site_urls is not None:
            body['siteUrls'] = site_urls
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = Person.model_validate(data)
        return r

    def get_person_details(self, person_id: str, calling_data: bool = None) -> Person:
        """
        Get Person Details

        Shows details for a person, by ID.

        Response properties associated with a user's presence status, such as `status` or `lastActivity`, will only be
        displayed for people within your organization or an organization you manage. Presence information will not be
        shown if the authenticated user has `disabled status sharing
        <https://help.webex.com/nkzs6wl/>`_.

        Admin users can include `Webex Calling` (BroadCloud) user details in the response by specifying `callingData`
        parameter as `true`.

        Specify the person ID in the `personId` parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :rtype: :class:`Person`
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        url = self.ep(f'{person_id}')
        data = super().get(url, params=params)
        r = Person.model_validate(data)
        return r

    def update_a_person(self, person_id: str, display_name: str, calling_data: bool = None,
                        show_all_types: bool = None, min_response: bool = None, emails: list[str] = None,
                        phone_numbers: list[CreateAPersonPhoneNumbers] = None, extension: str = None,
                        location_id: str = None, first_name: str = None, last_name: str = None, nick_name: str = None,
                        avatar: str = None, roles: list[str] = None, licenses: list[str] = None,
                        department: str = None, manager: str = None, manager_id: str = None, title: str = None,
                        addresses: list[PersonAddresses] = None, site_urls: list[str] = None,
                        login_enabled: bool = None, org_id: str = None) -> Person:
        """
        Update a Person

        Update details for a person, by ID.

        Specify the person ID in the `personId` parameter in the URI. Only an admin can update a person details.

        Include all details for the person. This action expects all user details to be present in the request. A common
        approach is to first `GET the person's details
        <https://developer.webex.com/docs/api/v1/people/get-person-details>`_, make changes, then PUT both the changed and unchanged values.

        Admin users can include `Webex Calling` (BroadCloud) user details in the response by specifying `callingData`
        parameter as true.

        When doing attendee management, to update a user from host role to an attendee for a site append `#attendee` to
        the respective `siteUrl` and remove the meeting host license for this site from the license array.
        To update a person from an attendee role to a host for a site, add the meeting license for this site in the
        meeting array, and remove that site from the `siteurl` parameter.

        To remove the attendee privilege for a user on a meeting site, remove the `sitename#attendee` from the
        `siteUrl`s array. The `showAllTypes` parameter must be set to `true`.

        **NOTE**:

        * The `locationId` can only be set when assigning a calling license to a user. It cannot be changed if a user
        is already an existing calling user.

        * The `extension` field should be used to update the Webex Calling extension for a person. The extension value
        should not include the location routing prefix. The `work_extension` type in the `phoneNumbers` object as seen
        in the response payload of `List People
        <https://developer.webex.com/docs/api/v1/people/list-people>`_ or `Get Person Details
        extension for a person.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param display_name: The full name of the person.
        :type display_name: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param show_all_types: Include additional user data like `#attendee` role.
        :type show_all_types: bool
        :param min_response: Set to `true` to improve performance by omitting person details in the response. If
            unsuccessful the response will have optional error details.
        :type min_response: bool
        :param emails: The email addresses of the person. Only one email address is allowed per person.
        :type emails: list[str]
        :param phone_numbers: Phone numbers for the person. Can only be set for Webex Calling. Needs a Webex Calling
            license.
        :type phone_numbers: list[CreateAPersonPhoneNumbers]
        :param extension: Webex Calling extension of the person. This is only settable for a person with a Webex
            Calling license.
        :type extension: str
        :param location_id: The ID of the location for this person.
        :type location_id: str
        :param first_name: The first name of the person.
        :type first_name: str
        :param last_name: The last name of the person.
        :type last_name: str
        :param nick_name: The nickname of the person if configured. This cannot be overwritten and instead will be set
            to the firstName automatically in update requests.
        :type nick_name: str
        :param avatar: The URL to the person's avatar in PNG format.
        :type avatar: str
        :param roles: An array of role strings representing the roles to which this admin user belongs.
        :type roles: list[str]
        :param licenses: An array of license strings allocated to this person.
        :type licenses: list[str]
        :param department: The business department the user belongs to.
        :type department: str
        :param manager: A manager identifier.
        :type manager: str
        :param manager_id: Person ID of the manager.
        :type manager_id: str
        :param title: The person's title.
        :type title: str
        :param addresses: A person's addresses.
        :type addresses: list[PersonAddresses]
        :param site_urls: One or several site names where this user has a role (host or attendee). Append `#attendee`
            to the site name to designate the attendee role on that site.
        :type site_urls: list[str]
        :param login_enabled: Whether or not the user is allowed to use Webex. This property is only accessible if the
            authenticated user is an admin user for the person's organization.
        :type login_enabled: bool
        :param org_id: The ID of the organization to which this person belongs.
        :type org_id: str
        :rtype: :class:`Person`
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        if show_all_types is not None:
            params['showAllTypes'] = str(show_all_types).lower()
        if min_response is not None:
            params['minResponse'] = str(min_response).lower()
        body = dict()
        if emails is not None:
            body['emails'] = emails
        if phone_numbers is not None:
            body['phoneNumbers'] = TypeAdapter(list[CreateAPersonPhoneNumbers]).dump_python(phone_numbers, mode='json', by_alias=True, exclude_none=True)
        if extension is not None:
            body['extension'] = extension
        if location_id is not None:
            body['locationId'] = location_id
        body['displayName'] = display_name
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if nick_name is not None:
            body['nickName'] = nick_name
        if avatar is not None:
            body['avatar'] = avatar
        if org_id is not None:
            body['orgId'] = org_id
        if roles is not None:
            body['roles'] = roles
        if licenses is not None:
            body['licenses'] = licenses
        if department is not None:
            body['department'] = department
        if manager is not None:
            body['manager'] = manager
        if manager_id is not None:
            body['managerId'] = manager_id
        if title is not None:
            body['title'] = title
        if addresses is not None:
            body['addresses'] = TypeAdapter(list[PersonAddresses]).dump_python(addresses, mode='json', by_alias=True, exclude_none=True)
        if site_urls is not None:
            body['siteUrls'] = site_urls
        if login_enabled is not None:
            body['loginEnabled'] = login_enabled
        url = self.ep(f'{person_id}')
        data = super().put(url, params=params, json=body)
        r = Person.model_validate(data)
        return r

    def delete_a_person(self, person_id: str):
        """
        Delete a Person

        Remove a person from the system. Only an admin can remove a person.

        Specify the person ID in the `personId` parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :rtype: None
        """
        url = self.ep(f'{person_id}')
        super().delete(url)

    def get_my_own_details(self, calling_data: bool = None) -> Person:
        """
        Get My Own Details

        Get profile details for the authenticated user. This is the same as GET `/people/{personId}` using the Person
        ID associated with your Auth token.

        Admin users can include `Webex Calling` (BroadCloud) user details in the response by specifying `callingData`
        parameter as true.

        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :rtype: :class:`Person`
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        url = self.ep('me')
        data = super().get(url, params=params)
        r = Person.model_validate(data)
        return r

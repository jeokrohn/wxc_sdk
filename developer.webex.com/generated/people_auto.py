from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Addresses', 'CreatePersonBody', 'ListPeopleResponse', 'PeopleApi', 'Person', 'PhoneNumbers',
           'SipAddressesType', 'Status', 'Type']


class PhoneNumbers(ApiModel):
    #: The type of phone number.
    #: Possible values: work, mobile, fax
    type: Optional[str]
    #: The phone number.
    #: Possible values: +1 408 526 7209
    value: Optional[str]


class SipAddressesType(PhoneNumbers):
    primary: Optional[bool]


class Status(str, Enum):
    #: Active within the last 10 minutes
    active = 'active'
    #: The user is in a call
    call = 'call'
    #: The user has manually set their status to "Do Not Disturb"
    do_not_disturb = 'DoNotDisturb'
    #: Last activity occurred more than 10 minutes ago
    inactive = 'inactive'
    #: The user is in a meeting
    meeting = 'meeting'
    #: The user or a Hybrid Calendar service has indicated that they are "Out of Office"
    out_of_office = 'OutOfOffice'
    #: The user has never logged in; a status cannot be determined
    pending = 'pending'
    #: The user is sharing content
    presenting = 'presenting'
    #: The user’s status could not be determined
    unknown = 'unknown'


class Type(str, Enum):
    #: Account belongs to a person
    person = 'person'
    #: Account is a bot user
    bot = 'bot'
    #: Account is a guest user
    appuser = 'appuser'


class Addresses(ApiModel):
    #: The type of address
    #: Possible values: work
    type: Optional[str]
    #: The user's country
    #: Possible values: US
    country: Optional[str]
    #: the user's locality, often city
    #: Possible values: Milpitas
    locality: Optional[str]
    #: the user's region, often state
    #: Possible values: California
    region: Optional[str]
    #: the user's street
    #: Possible values: 1099 Bird Ave.
    street_address: Optional[str]
    #: the user's postal or zip code
    #: Possible values: 99212
    postal_code: Optional[str]


class CreatePersonBody(ApiModel):
    #: The email addresses of the person. Only one email address is allowed per person.
    #: Possible values: john.andersen@example.com
    emails: Optional[list[str]]
    #: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling license.
    phone_numbers: Optional[list[PhoneNumbers]]
    #: Webex Calling extension of the person. This is only settable for a person with a Webex Calling license.
    extension: Optional[str]
    #: The ID of the location for this person.
    location_id: Optional[str]
    #: The full name of the person.
    display_name: Optional[str]
    #: The first name of the person.
    first_name: Optional[str]
    #: The last name of the person.
    last_name: Optional[str]
    #: The URL to the person's avatar in PNG format.
    avatar: Optional[str]
    #: The ID of the organization to which this person belongs.
    org_id: Optional[str]
    #: An array of role strings representing the roles to which this admin user belongs.
    #: Possible values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
    #: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
    roles: Optional[list[str]]
    #: An array of license strings allocated to this person.
    #: Possible values: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
    #: Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
    licenses: Optional[list[str]]
    #: The business department the user belongs to.
    department: Optional[str]
    #: A manager identifier.
    manager: Optional[str]
    #: Person Id of the manager
    manager_id: Optional[str]
    #: the person's title
    title: Optional[str]
    #: Person's address
    addresses: Optional[list[Addresses]]
    #: One or several site names where this user has an attendee role. Append #attendee to the sitename (eg:
    #: mysite.webex.com#attendee)
    #: Possible values: mysite.webex.com#attendee
    site_urls: Optional[list[str]]


class Person(CreatePersonBody):
    #: A unique identifier for the person.
    id: Optional[str]
    #: The nickname of the person if configured. If no nickname is configured for the person, this field will not be
    #: present.
    nick_name: Optional[str]
    #: The date and time the person was created.
    created: Optional[str]
    #: The date and time the person was last changed.
    last_modified: Optional[str]
    #: The time zone of the person if configured. If no timezone is configured on the account, this field will not be
    #: present
    timezone: Optional[str]
    #: The date and time of the person's last activity within Webex. This will only be returned for people within your
    #: organization or an organization you manage. Presence information will not be shown if the authenticated user has
    #: disabled status sharing.
    last_activity: Optional[str]
    #: The users sip addresses. Read-only.
    sip_addresses: Optional[list[SipAddressesType]]
    #: The current presence status of the person. This will only be returned for people within your organization or an
    #: organization you manage. Presence information will not be shown if the authenticated user has disabled status
    #: sharing.
    status: Optional[Status]
    #: Whether or not an invite is pending for the user to complete account activation. This property is only returned
    #: if the authenticated user is an admin user for the person's organization.
    invite_pending: Optional[bool]
    #: Whether or not the user is allowed to use Webex. This property is only returned if the authenticated user is an
    #: admin user for the person's organization.
    login_enabled: Optional[bool]
    #: The type of person account, such as person or bot.
    type: Optional[Type]


class ListPeopleResponse(ApiModel):
    #: An array of person objects.
    items: Optional[list[Person]]
    #: An array of person IDs that could not be found.
    not_found_ids: Optional[list[str]]


class UpdatePersonBody(CreatePersonBody):
    #: The nickname of the person if configured. Set to the firstName automatically in update request.
    nick_name: Optional[str]
    #: Whether or not the user is allowed to use Webex. This property is only accessible if the authenticated user is
    #: an admin user for the person's organization.
    login_enabled: Optional[bool]


class PeopleApi(ApiChild, base='people'):
    """
    People are registered users of Webex. Searching and viewing People requires an auth token with a scope of
    spark:people_read. Viewing the list of all People in your Organization requires an administrator auth token with
    spark-admin:people_read scope. Adding, updating, and removing People requires an administrator auth token with the
    spark-admin:people_write and spark-admin:people_read scope.
    A person's call settings are for Webex Calling and necessitate Webex Calling licenses.
    To learn more about managing people in a room see the Memberships API. For information about how to allocate Hybrid
    Services licenses to people, see the Managing Hybrid Services guide.
    """

    def list_people(self, email: str = None, display_name: str = None, id: str = None, org_id: str = None, roles: str = None, calling_data: bool = None, location_id: str = None, **params) -> Generator[Person, None, None]:
        """
        List people in your organization. For most users, either the email or displayName parameter is required. Admin
        users can omit these fields and list all users in their organization.
        Response properties associated with a user's presence status, such as status or lastActivity, will only be
        returned for people within your organization or an organization you manage. Presence information will not be
        returned if the authenticated user has disabled status sharing.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true. Admin users can list all users in a location or with a specific phone number. Admin users
        will receive an enriched payload with additional administrative fields like liceneses,roles etc. These fields
        are shown when accessing a user via GET /people/{id}, not when doing a GET /people?id=
        Lookup by email is only supported for people within the same org or where a partner admin relationship is in
        place.
        Lookup by roles is only supported for Admin users for the people within the same org.
        Long result sets will be split into pages.

        :param email: List people with this email address. For non-admin requests, either this or displayName are
            required. With the exception of partner admins and a managed org relationship, people lookup by email is
            only available for users in the same org.
        :type email: str
        :param display_name: List people whose name starts with this string. For non-admin requests, either this or
            email are required.
        :type display_name: str
        :param id: List people by ID. Accepts up to 85 person IDs separated by commas. If this parameter is provided
            then presence information (such as the lastActivity or status properties) will not be included in the
            response.
        :type id: str
        :param org_id: List people in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param roles: List of roleIds separated by commas.
        :type roles: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param location_id: List people present in this location.
        :type location_id: str

        documentation: https://developer.webex.com/docs/api/v1/people/list-people
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
        return self.session.follow_pagination(url=url, model=Person, params=params)

    def create(self, emails: List[str], calling_data: bool = None, phone_numbers: PhoneNumbers = None, extension: str = None, location_id: str = None, display_name: str = None, first_name: str = None, last_name: str = None, avatar: str = None, org_id: str = None, roles: List[str] = None, licenses: List[str] = None, department: str = None, manager: str = None, manager_id: str = None, title: str = None, addresses: Addresses = None, site_urls: List[str] = None) -> Person:
        """
        Create a new user account for a given organization. Only an admin can create a new user account.
        At least one of the following body parameters is required to create a new user: displayName, firstName,
        lastName.
        Currently, users may have only one email address associated with their account. The emails parameter is an
        array, which accepts multiple values to allow for future expansion, but currently only one email address will
        be used for the new user.
        Admin users can include Webex calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.
        When doing attendee management, append #attendee to the siteUrl parameter (e.g. mysite.webex.com#attendee) to
        make the new user an attendee for a site.

        :param emails: The email addresses of the person. Only one email address is allowed per person. Possible
            values: john.andersen@example.com
        :type emails: List[str]
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param phone_numbers: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling
            license.
        :type phone_numbers: PhoneNumbers
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
        :param org_id: The ID of the organization to which this person belongs.
        :type org_id: str
        :param roles: An array of role strings representing the roles to which this admin user belongs. Possible
            values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type roles: List[str]
        :param licenses: An array of license strings allocated to this person. Possible values:
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type licenses: List[str]
        :param department: The business department the user belongs to.
        :type department: str
        :param manager: A manager identifier.
        :type manager: str
        :param manager_id: Person Id of the manager
        :type manager_id: str
        :param title: the person's title
        :type title: str
        :param addresses: Person's address
        :type addresses: Addresses
        :param site_urls: One or several site names where this user has an attendee role. Append #attendee to the
            sitename (eg: mysite.webex.com#attendee) Possible values: mysite.webex.com#attendee
        :type site_urls: List[str]

        documentation: https://developer.webex.com/docs/api/v1/people/create-a-person
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        body = CreatePersonBody()
        if emails is not None:
            body.emails = emails
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        if extension is not None:
            body.extension = extension
        if location_id is not None:
            body.location_id = location_id
        if display_name is not None:
            body.display_name = display_name
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if avatar is not None:
            body.avatar = avatar
        if org_id is not None:
            body.org_id = org_id
        if roles is not None:
            body.roles = roles
        if licenses is not None:
            body.licenses = licenses
        if department is not None:
            body.department = department
        if manager is not None:
            body.manager = manager
        if manager_id is not None:
            body.manager_id = manager_id
        if title is not None:
            body.title = title
        if addresses is not None:
            body.addresses = addresses
        if site_urls is not None:
            body.site_urls = site_urls
        url = self.ep()
        data = super().post(url=url, params=params, data=body.json())
        return Person.parse_obj(data)

    def details(self, person_id: str, calling_data: bool = None) -> Person:
        """
        Shows details for a person, by ID.
        Response properties associated with a user's presence status, such as status or lastActivity, will only be
        displayed for people within your organization or an organization you manage. Presence information will not be
        shown if the authenticated user has disabled status sharing.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.
        Specify the person ID in the personId parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool

        documentation: https://developer.webex.com/docs/api/v1/people/get-person-details
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        url = self.ep(f'{person_id}')
        data = super().get(url=url, params=params)
        return Person.parse_obj(data)

    def update(self, person_id: str, emails: List[str], calling_data: bool = None, show_all_types: bool = None, phone_numbers: PhoneNumbers = None, extension: str = None, location_id: str = None, display_name: str = None, first_name: str = None, last_name: str = None, avatar: str = None, org_id: str = None, roles: List[str] = None, licenses: List[str] = None, department: str = None, manager: str = None, manager_id: str = None, title: str = None, addresses: Addresses = None, site_urls: List[str] = None, nick_name: str = None, login_enabled: bool = None) -> Person:
        """
        Update details for a person, by ID.
        Specify the person ID in the personId parameter in the URI. Only an admin can update a person details.
        Include all details for the person. This action expects all user details to be present in the request. A common
        approach is to first GET the person's details, make changes, then PUT both the changed and unchanged values.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.
        Note: The locationId can only be set when adding a calling license to a user. It cannot be changed if a user is
        already an existing calling user.
        When doing attendee management, to update a user from host role to an attendee for a site append #attendee to
        the respective siteUrl and remove the meeting host license for this site from the license array.
        To update a person from an attendee role to a host for a site, add the meeting license for this site in the
        meeting array, and remove that site from the siteurl parameter.
        To remove the attendee privilege for a user on a meeting site, remove the sitename#attendee from the siteUrls
        array. The showAllTypes parameter must be set to true.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param emails: The email addresses of the person. Only one email address is allowed per person. Possible
            values: john.andersen@example.com
        :type emails: List[str]
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param show_all_types: Include additional user data like #attendee role
        :type show_all_types: bool
        :param phone_numbers: Phone numbers for the person. Only settable for Webex Calling. Requires a Webex Calling
            license.
        :type phone_numbers: PhoneNumbers
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
        :param org_id: The ID of the organization to which this person belongs.
        :type org_id: str
        :param roles: An array of role strings representing the roles to which this admin user belongs. Possible
            values: Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type roles: List[str]
        :param licenses: An array of license strings allocated to this person. Possible values:
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh,
            Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi
        :type licenses: List[str]
        :param department: The business department the user belongs to.
        :type department: str
        :param manager: A manager identifier.
        :type manager: str
        :param manager_id: Person Id of the manager
        :type manager_id: str
        :param title: the person's title
        :type title: str
        :param addresses: Person's address
        :type addresses: Addresses
        :param site_urls: One or several site names where this user has an attendee role. Append #attendee to the
            sitename (eg: mysite.webex.com#attendee) Possible values: mysite.webex.com#attendee
        :type site_urls: List[str]
        :param nick_name: The nickname of the person if configured. Set to the firstName automatically in update
            request.
        :type nick_name: str
        :param login_enabled: Whether or not the user is allowed to use Webex. This property is only accessible if the
            authenticated user is an admin user for the person's organization.
        :type login_enabled: bool

        documentation: https://developer.webex.com/docs/api/v1/people/update-a-person
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        if show_all_types is not None:
            params['showAllTypes'] = str(show_all_types).lower()
        body = UpdatePersonBody()
        if emails is not None:
            body.emails = emails
        if phone_numbers is not None:
            body.phone_numbers = phone_numbers
        if extension is not None:
            body.extension = extension
        if location_id is not None:
            body.location_id = location_id
        if display_name is not None:
            body.display_name = display_name
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if avatar is not None:
            body.avatar = avatar
        if org_id is not None:
            body.org_id = org_id
        if roles is not None:
            body.roles = roles
        if licenses is not None:
            body.licenses = licenses
        if department is not None:
            body.department = department
        if manager is not None:
            body.manager = manager
        if manager_id is not None:
            body.manager_id = manager_id
        if title is not None:
            body.title = title
        if addresses is not None:
            body.addresses = addresses
        if site_urls is not None:
            body.site_urls = site_urls
        if nick_name is not None:
            body.nick_name = nick_name
        if login_enabled is not None:
            body.login_enabled = login_enabled
        url = self.ep(f'{person_id}')
        data = super().put(url=url, params=params, data=body.json())
        return Person.parse_obj(data)

    def delete(self, person_id: str):
        """
        Remove a person from the system. Only an admin can remove a person.
        Specify the person ID in the personId parameter in the URI.

        :param person_id: A unique identifier for the person.
        :type person_id: str

        documentation: https://developer.webex.com/docs/api/v1/people/delete-a-person
        """
        url = self.ep(f'{person_id}')
        super().delete(url=url)
        return

    def my_own_details(self, calling_data: bool = None) -> Person:
        """
        Get profile details for the authenticated user. This is the same as GET /people/{personId} using the Person ID
        associated with your Auth token.
        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.

        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool

        documentation: https://developer.webex.com/docs/api/v1/people/get-my-own-details
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        url = self.ep('me')
        data = super().get(url=url, params=params)
        return Person.parse_obj(data)

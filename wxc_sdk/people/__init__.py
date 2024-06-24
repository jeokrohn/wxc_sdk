"""
People types and API

    **As of January 2024, the Webex APIs have been fully upgraded to support the
    industry-standard** :class:`SCIM2.0 <wxc_sdk.scim.ScimV2Api>`
    **protocol, which is
    used for user and group management, provisioning, and maintenance. Developers
    are advised to use this API instead of the people API, due to its higher
    performance and readily available connectors. Users created via SCIM can be
    licensed using the /licenses API, even in large quantities, using
    the new** :meth:`PATCH method <wxc_sdk.licenses.LicensesApi.assign_licenses_to_users>`.

People are registered users of Webex. Searching and viewing People requires an auth token with a
`scope <https://developer.webex.com/docs/integrations#scopes>`_
of `spark:people_read`. Viewing the list of all People in your organization requires an administrator auth token
with `spark-admin:people_read` scope. Adding, updating, and removing People requires an administrator auth token
with the `spark-admin:people_write` and `spark-admin:people_read` scope.

A person's call settings are for `Webex Calling` and necessitate Webex Calling licenses.

To learn more about managing people in a room see the :class:`Memberships API
<wxc_sdk.memberships.MembershipApi>`. For information about how to allocate Hybrid
Services licenses to people, see the `Managing Hybrid Services
<https://developer.webex.com/docs/api/guides/managing-hybrid-services-licenses>`_ guide.
"""

import datetime
from collections.abc import Generator
from typing import Optional

from pydantic import Field

from ..api_child import ApiChild
from ..base import ApiModel, to_camel, webex_id_to_uuid, ApiModelWithErrors
from ..base import SafeEnum as Enum

__all__ = ['PhoneNumberType', 'PhoneNumber', 'SipType', 'SipAddress', 'PeopleStatus', 'PersonType', 'PersonAddress',
           'Person', 'PeopleApi']

# there seems to be a problem with getting too many users with calling data at the same time
# this is the maximum number the SDK enforces
MAX_USERS_WITH_CALLING_DATA = 10
CALLING_DATA_TIMEOUT_PROTECTION = False


class PhoneNumberType(str, Enum):
    """
    Webex phone number type
    """
    work = 'work'
    mobile = 'mobile'
    fax = 'fax'
    work_extension = 'work_extension'
    enterprise = 'enterprise'
    alternate1 = 'alternate1'
    alternate2 = 'alternate2'


class PhoneNumber(ApiModel):
    """
    Webex phone number: type and Value
    """
    number_type: PhoneNumberType = Field(alias='type')
    value: str
    primary: Optional[bool] = None


class SipType(str, Enum):
    """
    SIP address type
    """
    enterprise = 'enterprise'
    cloudCalling = 'cloud-calling'
    personalRoom = 'personal-room'
    unknown = 'unknown'


class SipAddress(ApiModel):
    """
    SIP address: type, value and primary indication
    """
    sip_type: SipType = Field(alias='type')
    value: str
    primary: bool


class PeopleStatus(str, Enum):
    active = 'active'  #: active within the last 10 minutes
    call = 'call'  #: the user is in a call
    do_not_disturb = 'DoNotDisturb'  #: the user has manually set their status to "Do Not Disturb"
    inactive = 'inactive'  #: last activity occurred more than 10 minutes ago
    meeting = 'meeting'  #: last activity occurred more than 10 minutes ago
    out_of_office = 'OutOfOffice'  #: the user or a Hybrid Calendar service has indicated that they are "Out of Office"
    pending = 'pending'  #: the user has never logged in; a status cannot be determined
    presenting = 'presenting'  #: the user is sharing content
    unknown = 'unknown'  #: the user’s status could not be determined


class PersonType(str, Enum):
    #: account belongs to a person
    person = 'person'
    #: account is a bot user
    bot = 'bot'
    #: account is a guest user
    app_user = 'appuser'


class PersonAddress(ApiModel):
    #: The type of address
    #: Possible values: work
    type: Optional[str] = None
    #: The user's country
    #: Possible values: US
    country: Optional[str] = None
    #: the user's locality, often city
    #: Possible values: Milpitas
    locality: Optional[str] = None
    #: the user's region, often state
    #: Possible values: California
    region: Optional[str] = None
    #: the user's street
    #: Possible values: 1099 Bird Ave.
    street_address: Optional[str] = None
    #: the user's postal or zip code
    #: Possible values: 99212
    postal_code: Optional[str] = None


class Person(ApiModelWithErrors):
    """
    Webex person
    """
    #: A unique identifier for the person.
    person_id: Optional[str] = Field(alias='id', default=None)
    #: The email addresses of the person.
    emails: Optional[list[str]] = None
    #: Phone numbers for the person.
    phone_numbers: Optional[list[PhoneNumber]] = None
    #: The Webex Calling extension for the person. Only applies to a person with a Webex Calling license
    extension: Optional[str] = None
    #: The ID of the location for this person retrieved from BroadCloud.
    location_id: Optional[str] = None
    #: The full name of the person.
    display_name: Optional[str] = None
    #: The nickname of the person if configured. If no nickname is configured for the person, this field will not
    #: be present.
    nick_name: Optional[str] = None
    #: first_name: Optional[str]
    first_name: Optional[str] = None
    #: The last name of the person.
    last_name: Optional[str] = None
    #: The URL to the person's avatar in PNG format
    avatar: Optional[str] = None
    #: The ID of the organization to which this person belongs.
    org_id: Optional[str] = None
    #: An array of role strings representing the roles to which this person belongs.
    roles: Optional[list[str]] = None
    #: An array of license strings allocated to this person.
    licenses: Optional[list[str]] = None
    #: The business department the user belongs to.
    department: Optional[str] = None
    #: A manager identifier.
    manager: Optional[str] = None
    #: Person Id of the manager
    manager_id: Optional[str] = None
    #: the person's title
    title: Optional[str] = None
    #: Person's address
    addresses: Optional[list[PersonAddress]] = None
    #: One or several site names where this user has an attendee role. Append #attendee to the sitename (eg:
    # mysite.webex.com#attendee)
    #: Possible values: mysite.webex.com#attendee
    site_urls: Optional[list[str]] = None
    #: The date and time the person was created.
    created: Optional[datetime.datetime] = None
    #: The date and time the person was last changed.
    last_modified: Optional[datetime.datetime] = None
    #: The time zone of the person if configured. If no timezone is configured on the account, this field will not be
    #: present
    timezone: Optional[str] = None
    #: The date and time of the person's last activity within Webex. This will only be returned for people within
    #: your organization or an organization you manage. Presence information will not be shown if the authenticated
    #: user has disabled status sharing.
    last_activity: Optional[str] = None
    #: The users sip addresses. Read-only.
    sip_addresses: Optional[list[SipAddress]] = None
    #: The current presence status of the person. This will only be returned for people within your organization or an
    #: organization you manage. Presence information will not be shown if the authenticated user has disabled status
    #: sharing.
    status: Optional[PeopleStatus] = None
    #: Whether or not an invite is pending for the user to complete account activation. This property is only returned
    #: if the authenticated user is an admin user for the person's organization.
    invite_pending: Optional[bool] = None
    #: Whether or not the user is allowed to use Webex. This property is only returned if the authenticated user is an
    #: admin user for the person's organization.
    login_enabled: Optional[bool] = None
    #: The type of person account, such as person or bot.
    person_type: Optional[PersonType] = Field(alias='type', default=None)
    user_name: Optional[str] = None

    @property
    def person_id_uuid(self) -> str:
        """
        person id in uuid format
        """
        return webex_id_to_uuid(self.person_id)

    @property
    def plus_e164(self) -> list[PhoneNumber]:
        """
        List of +E.164 phone numbers of the user
        :return:
        """
        return self.phone_numbers and [number for number in self.phone_numbers
                                       if number.value.startswith('+')] or []

    @property
    def tn(self) -> Optional[PhoneNumber]:
        """
        user's TN (first +E.164 number if any)
        :return:
        """
        if not self.phone_numbers:
            return None
        return next((number for number in self.phone_numbers
                     if number.value.startswith('+')), None)

    def create_update(self)->dict:
        """
        Date for create() and udpate()

        :meta private:
        """
        return self.model_dump(mode='json', exclude_none=True, by_alias=True,
                               exclude={'person_id': True,
                                        'created': True,
                                        'last_modified': True,
                                        'timezone': True,
                                        'last_activity': True,
                                        'sip_addresses': True,
                                        'status': True,
                                        'invite_pending': True,
                                        'login_enabled': True,
                                        'person_type': True}
                               )


class PeopleApi(ApiChild, base='people'):
    """
    People

        **As of January 2024, the Webex APIs have been fully upgraded to support the
        industry-standard** :class:`SCIM2.0 <wxc_sdk.scim.ScimV2Api>`
        **protocol, which is
        used for user and group management, provisioning, and maintenance. Developers
        are advised to use this API instead of the people API, due to its higher
        performance and readily available connectors. Users created via SCIM can be
        licensed using the /licenses API, even in large quantities, using
        the new** :meth:`PATCH method <wxc_sdk.licenses.LicensesApi.assign_licenses_to_users>`.

    People are registered users of Webex. Searching and viewing People requires an auth token with a
    `scope <https://developer.webex.com/docs/integrations#scopes>`_
    of `spark:people_read`. Viewing the list of all People in your organization requires an administrator auth token
    with `spark-admin:people_read` scope. Adding, updating, and removing People requires an administrator auth token
    with the `spark-admin:people_write` and `spark-admin:people_read` scope.

    A person's call settings are for `Webex Calling` and necessitate Webex Calling licenses.

    To learn more about managing people in a room see the :class:`Memberships API
    <wxc_sdk.memberships.MembershipApi>`. For information about how to allocate Hybrid
    Services licenses to people, see the `Managing Hybrid Services
    <https://developer.webex.com/docs/api/guides/managing-hybrid-services-licenses>`_ guide.
    """

    def list(self, email: str = None, display_name: str = None, id_list: list[str] = None, org_id: str = None,
             roles: str = None, calling_data: bool = None, location_id: str = None,
             **params) -> Generator[Person, None, None]:
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

        :param email: List people with this email address. For non-admin requests, either this or displayName are
            required.
        :type email: str
        :param display_name: List people whose name starts with this string. For non-admin requests, either this or
            email are required.
        :type display_name: str
        :param id_list: List people by ID. Accepts up to 85 person IDs. If this parameter is provided then presence
            information (such as the last_activity or status properties) will not be included in the response.
        :type id_list: list[str]
        :param org_id: List people in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param roles: List of roleIds separated by commas.
        :type roles: str
        :param calling_data: Include Webex Calling user details in the response. Default: False
        :type calling_data: bool
        :param location_id: List people present in this location.
        :type location_id: str
        :return: yield :class:`Person` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        if calling_data:
            params['callingData'] = 'true'
            # apparently there is a performance problem with getting too many users w/ calling data at the same time
            if CALLING_DATA_TIMEOUT_PROTECTION:
                params['max'] = params.get('max', MAX_USERS_WITH_CALLING_DATA)
        id_list = params.pop('idList', None)
        if id_list:
            params['id'] = ','.join(id_list)
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Person, params=params)

    def create(self, settings: Person, calling_data: bool = False, min_response: bool = None) -> Person:
        """
        Create a Person

        Create a new user account for a given organization. Only an admin can create a new user account.

        At least one of the following body parameters is required to create a new user: displayName, firstName,
        lastName.

        Currently, users may have only one email address associated with their account. The emails parameter is an
        array, which accepts multiple values to allow for future expansion, but currently only one email address will
        be used for the new user.

        Admin users can include `Webex calling` (BroadCloud) user details in the response by specifying `callingData`
        parameter as true. It may happen that the POST request with calling data returns a 400 status, but the person
        was created still. One way to get into this state is if an invalid phone number is assigned to a user. The
        people API aggregates calls to several other microservices, and one may have failed. A best practice is to
        check if the user exists before retrying. This can be done with the user's email address and a GET /people.

        When doing attendee management, to make the new user an attendee for a site: append #attendee to the siteUrl
        parameter (eg: mysite.webex.com#attendee).

        **NOTES**:

        * For creating a `Webex Calling` user, you must provide `phoneNumbers` or `extension`, `locationId`, and
          `licenses` string in the same request.

        * `SipAddresses` are assigned via an asynchronous process. This means that the POST response may not show the
          SIPAddresses immediately. Instead, you can verify them with a separate GET to /people, after they were newly
          configured.

        :param settings: settings for new user
        :type settings: Person
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :param min_response: Set to `true` to improve performance by omitting person details and returning only the ID
            in the response when successful. If unsuccessful the response will have optional error details.
        :type min_response: bool
        :return: new user
        :rtype: Person
        """
        params = {}
        if calling_data is not None:
            params['callingData'] = str(calling_data).lower()
        if min_response is not None:
            params['minResponse'] = str(min_response).lower()
        url = self.ep()
        data = settings.create_update()
        return Person.model_validate(self.post(url, json=data, params=params))

    def details(self, person_id: str, calling_data: bool = False) -> Person:
        """
        Shows details for a person, by ID.

        Response properties associated with a user's presence status, such as status or last_activity, will only be
        displayed for people within your organization or an organization you manage. Presence information will not be
        shown if the authenticated user has disabled status sharing.

        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying calling_data
        parameter as True.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calling_data: Include Webex Calling user details in the response. Default: false
        :type calling_data: bool
        :return: person details
        :rtype: Person
        """
        ep = self.ep(path=person_id)
        params = calling_data and {'callingData': 'true'} or None
        return Person.model_validate(self.get(ep, params=params))

    def delete_person(self, person_id: str):
        """
        Remove a person from the system. Only an admin can remove a person.

        :param person_id: A unique identifier for the person.
        :return:
        """
        ep = self.ep(path=person_id)
        self.delete(ep)

    def update(self, person: Person, calling_data: bool = False, show_all_types: bool = False,
               min_response: bool = None) -> Person:
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

        :param person: The person to update
        :type person: Person
        :param calling_data: Include Webex Calling user details in the response. Default: False
        :type calling_data: bool
        :param show_all_types: Include additional user data like #attendee role
        :type show_all_types: bool
        :param min_response: Set to `true` to improve performance by omitting person details in the response. If
            unsuccessful the response will have optional error details.
        :type min_response: bool
        :return: Person details
        :rtype: Person
        """
        params = {}
        if calling_data:
            params['callingData'] = 'true'
        if show_all_types:
            params['showAllTypes'] = 'true'
        if min_response:
            params['minResponse'] = 'true'

        # some attributes should not be included in update
        data = person.create_update()
        ep = self.ep(path=person.person_id)
        return Person.model_validate(self.put(url=ep, json=data, params=params))

    def me(self, calling_data: bool = False) -> Person:
        """
        Show the profile for the authenticated user. This is the same as GET /people/{personId} using the Person ID
        associated with your Auth token.

        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.

        :param calling_data: True -> return calling data
        :type calling_data: bool
        :rtype: Person
        :return: profile of authenticated user
        """
        ep = self.ep('me')
        params = calling_data and {'callingData': 'true'} or None
        data = self.get(ep, params=params)
        result = Person.model_validate(data)
        return result

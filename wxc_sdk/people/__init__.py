"""
People types and API

People are registered users of Webex. Searching and viewing People requires an auth token with a scope
of spark:people_read. Viewing the list of all People in your Organization requires an administrator auth token
with spark-admin:people_read scope. Adding, updating, and removing People requires an administrator auth token
with the spark-admin:people_write and spark-admin:people_read scope.

A person's call settings are for Webex Calling and necessitate Webex Calling licenses.

To learn more about managing people in a room see the Memberships API.
"""

import datetime
import json
from collections.abc import Generator
from enum import Enum
from typing import Optional

from pydantic import Field

from ..api_child import ApiChild
from ..base import ApiModel, to_camel, webex_id_to_uuid

__all__ = ['PhoneNumberType', 'PhoneNumber', 'SipType', 'SipAddress', 'PeopleStatus', 'PersonType', 'Person',
           'PeopleApi']


class PhoneNumberType(str, Enum):
    """
    Webex phone number type
    """
    work = 'work'
    mobile = 'mobile'
    fax = 'fax'
    work_extension = 'work_extension'


class PhoneNumber(ApiModel):
    """
    Webex phone number: type and Value
    """
    number_type: PhoneNumberType = Field(alias='type')
    value: str


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
    person = 'person'  #: account belongs to a person
    bot = 'bot'  #: account is a bot user
    app_user = 'appuser'  #: account is a guest user


class Person(ApiModel):
    """
    Webex person
    """
    #: A unique identifier for the person.
    person_id: str = Field(alias='id')
    #: The email addresses of the person.
    emails: list[str]
    #: Phone numbers for the person.
    phone_numbers: Optional[list[PhoneNumber]]
    #: The Webex Calling extension for the person. Only applies to a person with a Webex Calling license
    extension: Optional[str]
    #: The ID of the location for this person retrieved from BroadCloud.
    location_id: Optional[str]
    #: The full name of the person.
    display_name: Optional[str]
    #: The nickname of the person if configured. If no nickname is configured for the person, this field will not
    #: be present.
    nick_name: Optional[str]
    #: first_name: Optional[str]
    first_name: Optional[str]
    #: The last name of the person.
    last_name: Optional[str]
    #: The URL to the person's avatar in PNG format
    avatar: Optional[str]
    #: The ID of the organization to which this person belongs.
    org_id: str
    #: An array of role strings representing the roles to which this person belongs.
    roles: Optional[list[str]]
    #: An array of license strings allocated to this person.
    licenses: Optional[list[str]]
    #: The date and time the person was created.
    created: datetime.datetime
    #: The date and time the person was last changed.
    last_modified: str
    #: The time zone of the person if configured. If no timezone is configured on the account, this field will not be
    #: present
    timezone: Optional[str]
    #: The date and time of the person's last activity within Webex. This will only be returned for people within
    #: your organization or an organization you manage. Presence information will not be shown if the authenticated
    #: user has disabled status sharing.
    last_activity: Optional[str]
    #: One or several site names where this user has a role (host or attendee)
    site_urls: Optional[list[str]]
    #: The users sip addresses
    sip_addresses: Optional[list[SipAddress]]
    #: The current presence status of the person. This will only be returned for people within your organization or
    #: an organization you manage. Presence information will not be shown if the authenticated user has disabled
    #: status sharing.
    status: Optional[PeopleStatus]
    #: Whether or not an invite is pending for the user to complete account activation. This property is only
    #: returned if the authenticated user is an admin user for the person's organization.
    #: True: the person has been invited to Webex but has not created an account
    #:
    #: False: the person has been invited to Webex but has not created an account
    invite_pending: Optional[bool]
    #: Whether or not the user is allowed to use Webex. This property is only returned if the authenticated user is an
    #: admin user for the person's organization.
    #: True: the person can log into Webex
    #:
    #: False: the person cannot log into Webex
    login_enabled: Optional[bool]
    #: The type of person account, such as person or bot.
    person_type: PersonType = Field(alias='type')

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


class PeopleApi(ApiChild, base='people'):
    """
    People API
    """

    def list(self, email: str = None, display_name: str = None, id_list: list[str] = None, org_id: str = None,
             calling_data: bool = None, location_id: str = None, **params) -> Generator[Person, None, None]:
        """
        List people in your organization. For most users, either the email or display_name parameter is required. Admin
        users can omit these fields and list all users in their organization.

        Response properties associated with a user's presence status, such as status or last_activity, will only be
        displayed for people within your organization or an organization you manage. Presence information will not be
        shown if the authenticated user has disabled status sharing.

        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying calling_data
        parameter as True. Admin users can list all users in a location or with a specific phone number.

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
        id_list = params.pop('idList', None)
        if id_list:
            params['id'] = ','.join(id_list)
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Person, params=params)

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
        return Person.parse_obj(self.get(ep, params=params))

    def delete_person(self, person_id: str):
        """
        Remove a person from the system. Only an admin can remove a person.

        :param person_id: A unique identifier for the person.
        :return:
        """
        ep = self.ep(path=person_id)
        self.delete(ep)

    def update(self, person: Person, calling_data: bool = False, show_all_types: bool = False) -> Person:
        """
        Update details for a person, by ID.

        Only an admin can update a person details.

        Include all details for the person. This action expects all user details to be present in the request. A
        common approach is to first GET the person's details, make changes, then PUT both the changed and unchanged
        values.

        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying calling_data
        parameter as True.

        Note: The location_id can only be set when adding a calling license to a user. It cannot be changed if a user
        is already an existing calling user.

        When doing attendee management, to update a user “from host to attendee” for a site append #attendee to the
        respective site_url and remove the meeting host license for this site from the license array. To update a
        person “from attendee to host” for a site, add the meeting license for this site in the meeting array and
        remove that site from the site_url parameter.

        Removing the attendee privilege for a user on a meeting site is done by removing that sitename#attendee from
        the siteUrls array. The show_all_types parameter must be set to True.

        :param person: The person to update
        :type person: Person
        :param calling_data: Include Webex Calling user details in the response. Default: False
        :type calling_data: bool
        :param show_all_types: Include Webex Calling user details in the response. Default: False
        :type show_all_types: bool
        :return: Person details
        :rtype: Person
        """
        params = {}
        if calling_data:
            params['callingData'] = 'true'
        if show_all_types:
            params['showAllTypes'] = 'true'

        # set of attributes that can be updated and should be included in body of PUT
        can_update = {'emails', 'phoneNumbers', 'extension', 'locationId', 'displayName', 'firstName', 'lastName',
                      'nickName', 'avatar', 'orgId', 'roles', 'licenses', 'siteUrls', 'loginEnabled'}
        data = {k: v for k, v in json.loads(person.json()).items()
                if k in can_update}
        ep = self.ep(path=person.person_id)
        return Person.parse_obj(self.put(url=ep, json=data))

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
        result = Person.parse_obj(data)
        return result

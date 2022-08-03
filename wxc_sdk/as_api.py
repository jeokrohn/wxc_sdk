# auto-generated. DO NOT EDIT
import json
import logging
import os
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from enum import Enum
from io import BufferedReader
from typing import Union, Dict, Optional, Literal, List

from aiohttp import MultipartWriter
from pydantic import parse_obj_as

from wxc_sdk.all_types import *
from wxc_sdk.as_rest import AsRestSession
from wxc_sdk.base import to_camel, StrOrDict

log = logging.getLogger(__name__)


class MultipartEncoder(MultipartWriter):
    """
    Compatibility class for requests toolbelt MultipartEncoder
    """

    def __init__(self, *, fields: dict):
        super().__init__('form_data')
        for field_name, (file_name, content, content_type) in fields.items():
            # noinspection PyTypeChecker
            part = self.append(content, {'Content-Type': content_type})
            part.set_content_disposition('form-data', name=field_name, filename=file_name)


# there seems to be a problem with getting too many users with calling data at the same time
# this is the maximum number the SDK enforces
MAX_USERS_WITH_CALLING_DATA = 10


__all__ = ['AsAccessCodesApi', 'AsAnnouncementApi', 'AsApiChild', 'AsAppServicesApi', 'AsAuthCodesApi',
           'AsAutoAttendantApi', 'AsBargeApi', 'AsCallInterceptApi', 'AsCallParkApi', 'AsCallPickupApi',
           'AsCallQueueApi', 'AsCallRecordingApi', 'AsCallWaitingApi', 'AsCallerIdApi', 'AsCallingBehaviorApi',
           'AsCallparkExtensionApi', 'AsCallsApi', 'AsDialPlanApi', 'AsDndApi', 'AsExecAssistantApi',
           'AsForwardingApi', 'AsGroupsApi', 'AsHotelingApi', 'AsHuntGroupApi', 'AsIncomingPermissionsApi',
           'AsInternalDialingApi', 'AsLicensesApi', 'AsLocationInterceptApi', 'AsLocationMoHApi',
           'AsLocationNumbersApi', 'AsLocationVoicemailSettingsApi', 'AsLocationsApi', 'AsMonitoringApi',
           'AsNumbersApi', 'AsOrganisationVoicemailSettingsAPI', 'AsOutgoingPermissionsApi', 'AsPagingApi',
           'AsPeopleApi', 'AsPersonForwardingApi', 'AsPersonSettingsApi', 'AsPersonSettingsApiChild',
           'AsPremisePstnApi', 'AsPrivacyApi', 'AsPrivateNetworkConnectApi', 'AsPushToTalkApi', 'AsReceptionistApi',
           'AsRestSession', 'AsRouteGroupApi', 'AsRouteListApi', 'AsScheduleApi', 'AsTelephonyApi',
           'AsTelephonyLocationApi', 'AsTransferNumbersApi', 'AsTrunkApi', 'AsVoicePortalApi', 'AsVoicemailApi',
           'AsVoicemailGroupsApi', 'AsVoicemailRulesApi', 'AsWebexSimpleApi', 'AsWebhookApi',
           'AsWorkspaceSettingsApi', 'AsWorkspacesApi']


@dataclass(init=False)
class AsApiChild:
    """
    Base class for child APIs of :class:`WebexSimpleApi`
    """
    session: AsRestSession

    def __init__(self, *, session: AsRestSession, base: str = None):
        #: REST session
        self.session = session
        if base:
            self.base = base

    def __init_subclass__(cls, base: str):
        """
        Subclass registration hook. Each APIChild has a specific endpoint prefix which we gather at subclass
        registration time-

        :param base: APIChild specific URL path
        """
        super().__init_subclass__()
        # save endpoint prefix
        cls.base = base

    def ep(self, path: str = None):
        """
        endpoint URL for given path

        :param path: path after APIChild subclass specific endpoint URI prefix
        :type path: str
        :return: endpoint URL
        :rtype: str
        """
        path = path and f'/{path}' or ''
        return self.session.ep(f'{self.base}{path}')

    async def get(self, *args, **kwargs) -> StrOrDict:
        """
        GET request

        :param args:
        :param kwargs:
        :return:
        """
        return await self.session.rest_get(*args, **kwargs)

    async def post(self, *args, **kwargs) -> StrOrDict:
        """
        POST request

        :param args:
        :param kwargs:
        :return:
        """
        return await self.session.rest_post(*args, **kwargs)

    async def put(self, *args, **kwargs) -> StrOrDict:
        """
        PUT request

        :param args:
        :param kwargs:
        :return:
        """
        return await self.session.rest_put(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> None:
        """
        DELETE request

        :param args:
        :param kwargs:
        """
        await self.session.rest_delete(*args, **kwargs)

    async def patch(self, *args, **kwargs) -> StrOrDict:
        """
        PATCH request

        :param args:
        :param kwargs:
        """
        return await self.session.rest_patch(*args, **kwargs)


class AsGroupsApi(AsApiChild, base='groups'):

    def list_gen(self, *, include_members: bool = None, attributes: str = None, sort_by: str = None,
             sort_order: str = None, list_filter: str = None, org_id: str = None,
             **params) -> AsyncGenerator[Group, None, None]:
        """
        List groups

        :param include_members: Include members in list response
        :type include_members: bool
        :param attributes: comma separated list of attributes to return
        :type attributes: str
        :param sort_by: attribute to sort by
        :type sort_by: str
        :param sort_order: sort order, ascending or descending
        :type sort_order: str
        :param org_id: organisation ID
        :type org_id: str
        :param list_filter: filter expression. Example: displayName eq "test"
        :type list_filter: str
        :param params:
        :return: generator of :class:`Group` objects
        """
        params.update((to_camel(k), v) for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        for k, v in params.items():
            if isinstance(v, bool):
                params[k] = 'true' if v else 'false'
        if lf := params.pop('listFilter', None):
            params['filter'] = lf
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Group, item_key='groups', params=params)

    async def list(self, *, include_members: bool = None, attributes: str = None, sort_by: str = None,
             sort_order: str = None, list_filter: str = None, org_id: str = None,
             **params) -> List[Group]:
        """
        List groups

        :param include_members: Include members in list response
        :type include_members: bool
        :param attributes: comma separated list of attributes to return
        :type attributes: str
        :param sort_by: attribute to sort by
        :type sort_by: str
        :param sort_order: sort order, ascending or descending
        :type sort_order: str
        :param org_id: organisation ID
        :type org_id: str
        :param list_filter: filter expression. Example: displayName eq "test"
        :type list_filter: str
        :param params:
        :return: generator of :class:`Group` objects
        """
        params.update((to_camel(k), v) for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        for k, v in params.items():
            if isinstance(v, bool):
                params[k] = 'true' if v else 'false'
        if lf := params.pop('listFilter', None):
            params['filter'] = lf
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=Group, item_key='groups', params=params)]

    async def create(self, *, settings: Group) -> Group:
        """
        Create a new group using the provided settings. Only display_name is mandatory

        :param settings: settings for new group
        :type settings: Group
        :return: new group
        :rtype: :class:`Group`
        """
        url = self.ep()
        body = settings.json(exclude={'group_id': True,
                                      'members': {'__all__': {'member_type': True,
                                                              'display_name': True,
                                                              'operation': True}},
                                      'created': True,
                                      'last_modified': True})
        data = await self.post(url, data=body)
        return Group.parse_obj(data)

    async def details(self, group_id: str, include_members: bool = None) -> Group:
        """
        Get group details

        :param group_id: group id
        :type group_id: str
        :param include_members: return members in response
        :type include_members: bool
        :return: group details
        :rtype: Group
        """
        url = self.ep(group_id)
        params = dict()
        if include_members is not None:
            params['includeMembers'] = 'true' if include_members else 'false'
        data = await self.get(url, params=params)
        return Group.parse_obj(data)

    def members_gen(self, *, group_id: str, **params) -> AsyncGenerator[GroupMember, None, None]:
        """
        Query members of a group

        :param group_id: group id
        :type group_id: str
        :param params:
        :return: generator of :class:`GroupMember` instances
        """
        url = self.ep(f'{group_id}/Members')
        return self.session.follow_pagination(url=url, model=GroupMember, params=params, item_key='members')

    async def members(self, *, group_id: str, **params) -> List[GroupMember]:
        """
        Query members of a group

        :param group_id: group id
        :type group_id: str
        :param params:
        :return: generator of :class:`GroupMember` instances
        """
        url = self.ep(f'{group_id}/Members')
        return [o async for o in self.session.follow_pagination(url=url, model=GroupMember, params=params, item_key='members')]

    async def update(self, *, group_id: str, settings: Group = None, remove_all: bool = None) -> Group:
        """
        update group information.

        Options: change displayName, add new members, remove some or all members, replace all members

        :param group_id:
        :param settings:
        :param remove_all:
        :return:
        """
        if not any((settings, remove_all)):
            raise ValueError('settings or remove_all have to be present')
        url = self.ep(group_id)
        if settings:
            body = settings.json(exclude={'group_id': True,
                                          'members': {'__all__': {'member_type': True,
                                                                  'display_name': True}},
                                          'created': True,
                                          'last_modified': True})
        else:
            body = 'purgeAllValues:{"attributes":["members"]}'
        data = await self.patch(url, data=body)
        return Group.parse_obj(data)

    async def delete_group(self, group_id: str):
        """
        Delete a group

        :param group_id: group id
        :type group_id: str
        """
        url = self.ep(group_id)
        await self.delete(url)


class AsLicensesApi(AsApiChild, base='licenses'):
    """
    Licenses

    An allowance for features and services that are provided to users on a Webex services subscription. Cisco and its
    partners manage the amount of licenses provided to administrators and users. This license resource can be accessed
    only by an admin.
    """

    def list_gen(self, org_id: str = None) -> AsyncGenerator[License, None, None]:
        """
        List all licenses for a given organization. If no org_id is specified, the default is the organization of
        the authenticated user.

        Response properties that are not applicable to the license will not be present in the response.

        :param org_id: List licenses for this organization.
        :type org_id: str
        :return: yields :class:`License` instances
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=License, params=params)

    async def list(self, org_id: str = None) -> List[License]:
        """
        List all licenses for a given organization. If no org_id is specified, the default is the organization of
        the authenticated user.

        Response properties that are not applicable to the license will not be present in the response.

        :param org_id: List licenses for this organization.
        :type org_id: str
        :return: yields :class:`License` instances
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=License, params=params)]

    async def details(self, license_id) -> License:
        """
        Shows details for a license, by ID.

        Response properties that are not applicable to the license will not be present in the response.

        :param license_id: The unique identifier for the license.
        :type license_id: str
        :return: license details
        :rtype: License
        """
        ep = self.ep(license_id)
        return License.parse_obj(await self.get(ep))


class AsLocationsApi(AsApiChild, base='locations'):
    """
    Location API

    Locations are used to organize Webex Calling (BroadCloud) features within physical locations. Webex Control Hub
    may be used to define new locations.

    Searching and viewing locations in your organization requires an administrator auth token with the
    spark-admin:people_read and spark-admin:people_write or spark-admin:device_read AND spark-admin:device_write
    scope combinations.
    """

    def list_gen(self, name: str = None, location_id: str = None, org_id: str = None,
             **params) -> AsyncGenerator[Location, None, None]:
        """
        List locations for an organization.

        :param name: List locations whose name contains this string (case-insensitive).
        :type name: str
        :param location_id: List locations by ID.
        :type location_id: str
        :param org_id: List locations in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: generator of :class:`Location` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        if location_id is not None:
            params.pop('locationId')
            params['id'] = location_id
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Location, params=params)

    async def list(self, name: str = None, location_id: str = None, org_id: str = None,
             **params) -> List[Location]:
        """
        List locations for an organization.

        :param name: List locations whose name contains this string (case-insensitive).
        :type name: str
        :param location_id: List locations by ID.
        :type location_id: str
        :param org_id: List locations in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: generator of :class:`Location` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        if location_id is not None:
            params.pop('locationId')
            params['id'] = location_id
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=Location, params=params)]

    async def by_name(self, name: str, org_id: str = None) -> Optional[Location]:
        """
        Get a location by name

        :param name: name of the location to search
        :type name: str
        :param org_id: search in list of locations  in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: locations
        :rtype: Location
        """
        return next((location for location in await self.list(name=name, org_id=org_id)
                     if location.name == name), None)

    async def details(self, location_id) -> Location:
        """
        Shows details for a location, by ID.

        This API only works for Customer administrators and for Partner administrators to query their own organization.
        Partner administrators looking to query customer organizations should use the List Locations endpoint to
        retrieve information about locations.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :return: location details
        :rtype: Location
        """
        ep = self.ep(location_id)
        return Location.parse_obj(await self.get(ep))


class AsPeopleApi(AsApiChild, base='people'):
    """
    People API
    """

    def list_gen(self, email: str = None, display_name: str = None, id_list: list[str] = None, org_id: str = None,
             calling_data: bool = None, location_id: str = None, **params) -> AsyncGenerator[Person, None, None]:
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
            # apparently there is a performance problem with getting too many users w/ calling data at the same time
            params['max'] = params.get('max', MAX_USERS_WITH_CALLING_DATA)
        id_list = params.pop('idList', None)
        if id_list:
            params['id'] = ','.join(id_list)
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Person, params=params)

    async def list(self, email: str = None, display_name: str = None, id_list: list[str] = None, org_id: str = None,
             calling_data: bool = None, location_id: str = None, **params) -> List[Person]:
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
            # apparently there is a performance problem with getting too many users w/ calling data at the same time
            params['max'] = params.get('max', MAX_USERS_WITH_CALLING_DATA)
        id_list = params.pop('idList', None)
        if id_list:
            params['id'] = ','.join(id_list)
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=Person, params=params)]

    async def create(self, settings: Person, calling_data: bool = False) -> Person:
        """
        Create a Person

        Create a new user account for a given organization. Only an admin can create a new user account.

        At least one of the following body parameters is required to create a new user: displayName, firstName,
        lastName.

        Currently, users may have only one email address associated with their account. The emails parameter is an
        array, which accepts multiple values to allow for future expansion, but currently only one email address will
        be used for the new user.

        Admin users can include Webex calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.

        When doing attendee management, to make the new user an attendee for a site: append #attendee to the siteUrl
        parameter (eg: mysite.webex.com#attendee).

        :param settings: settings for new user
        :type settings: Person
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :return: new user
        :rtype: Person
        """
        params = calling_data and {'callingData': 'true'} or None
        url = self.ep()
        data = settings.json(exclude={'person_id': True,
                                      'created': True,
                                      'last_modified': True,
                                      'timezone': True,
                                      'last_activity': True,
                                      'sip_addresses': True,
                                      'status': True,
                                      'invite_pending': True,
                                      'login_enabled': True,
                                      'person_type': True})
        return Person.parse_obj(await self.post(url, data=data, params=params))

    async def details(self, person_id: str, calling_data: bool = False) -> Person:
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
        return Person.parse_obj(await self.get(ep, params=params))

    async def delete_person(self, person_id: str):
        """
        Remove a person from the system. Only an admin can remove a person.

        :param person_id: A unique identifier for the person.
        :return:
        """
        ep = self.ep(path=person_id)
        await self.delete(ep)

    async def update(self, person: Person, calling_data: bool = False, show_all_types: bool = False) -> Person:
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
        params = calling_data and {'callingData': 'true'} or None

        if not all(v is not None
                   for v in (person.display_name, person.first_name, person.last_name)):
            raise ValueError('display_name, first_name, and last_name are required')

        # some attributes should not be included in update
        data = person.json(exclude={'created': True,
                                    'last_modified': True,
                                    'timezone': True,
                                    'last_activity': True,
                                    'sip_addresses': True,
                                    'status': True,
                                    'invite_pending': True,
                                    'login_enabled': True,
                                    'person_type': True})
        ep = self.ep(path=person.person_id)
        return Person.parse_obj(await self.put(url=ep, data=data, params=params))

    async def me(self, calling_data: bool = False) -> Person:
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
        data = await self.get(ep, params=params)
        result = Person.parse_obj(data)
        return result


class AsPersonSettingsApiChild(AsApiChild, base=''):
    """
    Base class for all classes implementing person settings APIs
    """

    feature = None

    def __init__(self, *, session: AsRestSession,
                 workspaces: bool = False, locations: bool = False):
        self.feature_prefix = '/features/'
        if workspaces:
            self.selector = 'workspaces'
        elif locations:
            self.selector = 'telephony/config/locations'
            self.feature_prefix = '/'
        else:
            self.selector = 'people'
        super().__init__(session=session, base=self.selector)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(base='')
        if cls.feature is None:
            raise TypeError('feature has to be defined')

    def f_ep(self, *, person_id: str, path: str = None) -> str:
        """
        person specific feature endpoint like v1/people/{uid}/features/....

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param path: path in the endpoint after the feature base URL
        :type path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        return self.session.ep(f'{self.selector}/{person_id}{self.feature_prefix}{self.feature}{path}')


class AsAppServicesApi(AsPersonSettingsApiChild):
    """
    API for person's app services settings
    """

    feature = 'applications'

    async def read(self, *, person_id: str, org_id: str = None) -> AppServicesSettings:
        """
        Retrieve a Person's Application Services Settings

        Application services let you determine the ringing behavior for calls made to people in certain scenarios.
        You can also specify which devices can download the Webex Calling app.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: privacy settings
        :rtype: :class:`Privacy`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return AppServicesSettings.parse_obj(data)

    async def configure(self, *, person_id: str, settings: AppServicesSettings, org_id: str = None):
        """
        Modify a Person's Application Services Settings

        Application services let you determine the ringing behavior for calls made to users in certain scenarios. You
        can also specify which devices users can download the Webex Calling app on.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: settings for update
        :type settings: :class:`AppServicesSettings`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = settings.json(exclude={'available_line_count': True})
        await self.put(ep, params=params, data=data)


class AsBargeApi(AsPersonSettingsApiChild):
    """
    API for person's barge settings
    """

    feature = 'bargeIn'

    async def read(self, *, person_id: str, org_id: str = None) -> BargeSettings:
        """
        Retrieve a Person's Barge In Settings

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: barge settings for specific user
        :rtype: BargeSettings
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return BargeSettings.parse_obj(await self.get(ep, params=params))

    async def configure(self, *, person_id: str, barge_settings: BargeSettings, org_id: str = None):
        """
        Configure a Person's Barge In Settings

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param barge_settings: new setting to be applied
        :type barge_settings: BargeSettings
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        await self.put(ep, params=params, data=barge_settings.json())


class AsCallInterceptApi(AsPersonSettingsApiChild):
    """
    API for person's call intercept settings
    """

    feature = 'intercept'

    async def read(self, *, person_id: str, org_id: str = None) -> InterceptSetting:
        """
        Read Call Intercept Settings for a Person

        Retrieves Person's Call Intercept Settings

        The intercept feature gracefully takes a person’s phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none,
        some, or all incoming calls to the specified person are intercepted. Also depending on the service
        configuration, outgoing calls are intercepted or rerouted to another location.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: user's call intercept settings
        :rtype: InterceptSetting
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return InterceptSetting.parse_obj(await self.get(ep, params=params))

    async def configure(self, *, person_id: str, intercept: InterceptSetting, org_id: str = None):
        """
        Configure Call Intercept Settings for a Person

        Configures a Person's Call Intercept Settings

        The intercept feature gracefully takes a person’s phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified person are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param intercept: new intercept settings
        :type intercept: InterceptSetting
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.loads(intercept.json())
        try:
            # remove attribute not present in update
            data['incoming']['announcements'].pop('fileName', None)
        except KeyError:
            pass
        await self.put(ep, params=params, json=data)

    async def greeting(self, person_id: str, content: Union[BufferedReader, str],
                 upload_as: str = None, org_id: str = None):
        """
        Configure Call Intercept Greeting for a Person

        Configure a Person's Call Intercept Greeting by uploading a Waveform Audio File Format, .wav, encoded audio
        file.

        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        if isinstance(content, str):
            upload_as = os.path.basename(content)
            content = open(content, mode='rb')
            must_close = True
            pass
        else:
            must_close = False
            # an existing reader
            if not upload_as:
                raise ValueError('upload_as is required')
        encoder = MultipartEncoder(fields={'file': (upload_as, content, 'audio/wav')})
        ep = self.f_ep(person_id=person_id, path='actions/announcementUpload/invoke')
        params = org_id and {'orgId': org_id} or None
        try:
            await self.post(ep, data=encoder, headers={'Content-Type': encoder.content_type},
                      params=params)
        finally:
            if must_close:
                content.close()
        return


class AsCallRecordingApi(AsPersonSettingsApiChild):
    """
    API for person's call recording settings
    """

    feature = 'callRecording'

    async def read(self, *, person_id: str, org_id: str = None) -> CallRecordingSetting:
        """
        Read Call Recording Settings for a Person

        Retrieve a Person's Call Recording Settings

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return CallRecordingSetting.parse_obj(await self.get(ep, params=params))

    async def configure(self, *, person_id: str, recording: CallRecordingSetting, org_id: str = None):
        """
        Configure Call Recording Settings for a Person

        Configure a Person's Call Recording Settings

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param recording: the new recording settings
        :type recording: CallRecordingSetting
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.loads(recording.json())
        for key in ['serviceProvider', 'externalGroup', 'externalIdentifier']:
            # remove attribute not present in update
            data.pop(key, None)
        await self.put(ep, params=params, json=data)


class AsCallWaitingApi(AsPersonSettingsApiChild):
    """
    API for person's call waiting settings
    """

    feature = 'callWaiting'

    async def read(self, *, person_id: str, org_id: str = None) -> bool:
        """
        Read Call Waiting Settings for a Person

        Retrieve a Person's Call Waiting Settings

        With this feature, a person can place an active call on hold and answer an incoming call. When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or
        ignore the call.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: call waiting setting
        :rtype: bool
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return data['enabled']

    async def configure(self, *, person_id: str, enabled: bool, org_id: str = None):
        """
        Configure Call Waiting Settings for a Person

        Configure a Person's Call Waiting Settings

        With this feature, a person can place an active call on hold and answer an incoming call. When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore
        the call.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: true if the Call Waiting feature is enabled.
        :type enabled: bool
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.dumps({'enabled': enabled})
        await self.put(ep, params=params, json=data)


class AsCallerIdApi(AsPersonSettingsApiChild):
    """
    API for person's caller id settings
    """

    feature = 'callerId'

    async def read(self, *, person_id: str, org_id: str = None) -> CallerId:
        """
        Retrieve a Person's Caller ID Settings

        Caller ID settings control how a person’s information is displayed when making outgoing calls.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return CallerId.parse_obj(await self.get(ep, params=params))

    async def configure(self, *, person_id: str, org_id: str = None,
                  selected: CallerIdSelectedType = None,
                  custom_number: str = None,
                  first_name: str = None,
                  last_name: str = None,
                  external_caller_id_name_policy: ExternalCallerIdNamePolicy = None,
                  custom_external_caller_id_name: str = None):
        """
        Configure a Person's Caller ID Settings

        Caller ID settings control how a person’s information is displayed when making outgoing calls.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param selected: Which type of outgoing Caller ID will be used.
        :type selected: CallerIdSelectedType
        :param custom_number: This value must be an assigned number from the person\'s location.
        :type custom_number: str
        :param first_name: Person\'s Caller ID first name. Characters of %, +, \`, \" and Unicode characters are not
            allowed.

        :type first_name: str
        :param last_name: Person\'s Caller ID last name. Characters of %, +, \`, \" and Unicode characters are not
            allowed.
        :type last_name: str
        :param external_caller_id_name_policy: Designates which type of External Caller Id Name policy is used.
            Default is DIRECT_LINE.
        :type external_caller_id_name_policy: ExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Custom External Caller Name, which will be shown if External Caller Id
            Name is OTHER.
        :type custom_external_caller_id_name: str

        """
        data = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                if i > 2 and v is not None}
        params = org_id and {'orgId': org_id} or None
        ep = self.f_ep(person_id=person_id)
        await self.put(ep, params=params, json=data)


class AsCallingBehaviorApi(AsPersonSettingsApiChild):
    """
    API for person's calling behavior settings
    """

    feature = 'callingBehavior'

    async def read(self, *, person_id: str, org_id: str = None) -> CallingBehavior:
        """
        Read Person's Calling Behavior

        Retrieves the calling behavior and UC Manager Profile settings for the person which includes overall calling
        behavior and calling UC Manager Profile ID.

        Webex Calling Behavior controls which Webex telephony application is to be used.

        An organization has an organization-wide default Calling Behavior that may be overridden for individual persons.

        In addition, UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or
        Calling in Webex Teams (Unified CM).

        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: calling behavior setting
        :rtype: CallingBehavior
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return CallingBehavior.parse_obj(data)

    async def configure(self, *, person_id: str, settings: CallingBehavior,
                  org_id: str = None):
        """
        Configure a Person's Calling Behavior

        Modifies the calling behavior settings for the person which includes overall calling behavior and UC Manager
        Profile ID.

        Webex Calling Behavior controls which Webex telephony application is to be used.

        An organization has an organization-wide default Calling Behavior that may be overridden for individual persons.

        In addition, UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or
        Calling in Webex Teams (Unified CM).

        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: new settings
        :type settings: CallingBehavior
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = settings.json(exclude_none=False, exclude={'effective_behavior_type'}, exclude_unset=True)
        await self.put(ep, params=params, data=data)


class AsDndApi(AsPersonSettingsApiChild):
    """
    API for person's DND settings
    """

    feature = 'doNotDisturb'

    async def read(self, *, person_id: str, org_id: str = None) -> DND:
        """
        Read Do Not Disturb Settings for a Person
        Retrieve a Person's Do Not Disturb Settings

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.
        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners) may
        use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return:
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return DND.parse_obj(await self.get(ep, params=params))

    async def configure(self, *, person_id: str, dnd_settings: DND, org_id: str = None):
        """
        Configure Do Not Disturb Settings for a Person
        Configure a Person's Do Not Disturb Settings

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param dnd_settings: new setting to be applied
        :type dnd_settings: DND
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        await self.put(ep, params=params, data=dnd_settings.json())


class AsExecAssistantApi(AsPersonSettingsApiChild):
    """
    API for person's exec assistant settings
    """

    feature = 'executiveAssistant'

    async def read(self, *, person_id: str, org_id: str = None) -> ExecAssistantType:
        """
        Retrieve Executive Assistant Settings for a Person

        Retrieve the executive assistant settings for the specified personId.

        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set
        the call forward destination and join or leave an executive's pool.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: exec assistant setting
        :rtype: :class:`ExecAssistantType`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        h: _Helper = _Helper.parse_obj(data)
        return h.exec_type

    async def configure(self, *, person_id: str, setting: ExecAssistantType, org_id: str = None):
        """
        Modify Executive Assistant Settings for a Person

        Modify the executive assistant settings for the specified personId.

        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set
        the call forward destination and join or leave an executive's pool.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param setting: New exex assistant settings
        :type setting: :class:`ExecAssistantType`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        h = _Helper(exec_type=setting)
        params = org_id and {'orgId': org_id} or None
        data = h.json()
        await self.put(ep, params=params, data=data)


class AsHotelingApi(AsPersonSettingsApiChild):
    """
    API for person's hoteling settings
    """

    feature = 'hoteling'

    async def read(self, *, person_id: str, org_id: str = None) -> bool:
        """
        Read Hoteling Settings for a Person

        Retrieve a person's hoteling settings.

        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features,
        and calling plan) is temporarily loaded onto a shared (host) phone.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: hoteling setting
        :rtype: bool
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return data['enabled']

    async def configure(self, *, person_id: str, enabled: bool, org_id: str = None):
        """
        Configure Hoteling Settings for a Person

        Configure a person's hoteling settings.

        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features,
        and calling plan) is temporarily loaded onto a shared (host) phone.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: When true, allow this person to connect to a Hoteling host device.
        :type enabled: bool
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.dumps({'enabled': enabled})
        await self.put(ep, params=params, json=data)


class AsIncomingPermissionsApi(AsPersonSettingsApiChild):
    """
    API for person's incoming permissions settings
    """

    feature = 'incomingPermission'

    async def read(self, *, person_id: str, org_id: str = None) -> IncomingPermissions:
        """
        Read Incoming Permission Settings for a Person

        Retrieve a Person's Incoming Permission Settings

        You can change the incoming calling permissions for a person if you want them to be different from your
        organization's default.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: incoming permission settings for specific user
        :rtype: :class:`IncomingPermissions`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return IncomingPermissions.parse_obj(await self.get(ep, params=params))

    async def configure(self, *, person_id: str, settings: IncomingPermissions, org_id: str = None):
        """
        Configure a Person's Barge In Settings

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: new setting to be applied
        :type settings: :class:`IncomingPermissions`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        await self.put(ep, params=params, data=settings.json())


class AsMonitoringApi(AsPersonSettingsApiChild):
    """
    API for person's call monitoring settings
    """

    feature = 'monitoring'

    async def read(self, *, person_id: str, org_id: str = None) -> Monitoring:
        """
        Retrieve a Person's Monitoring Settings

        Retrieves the monitoring settings of the person, which shows specified people, places or, call park
        extensions under monitoring. Monitors the line status which indicates if a person or place is on a call and
        if  a call has been parked on that extension.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: monitoring settings
        :rtype: :class:`Monitoring`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return Monitoring.parse_obj(data)

    async def configure(self, *, person_id: str, settings: Monitoring, org_id: str = None):
        """
        Configure Call Waiting Settings for a Person

        Configure a Person's Call Waiting Settings

        With this feature, a person can place an active call on hold and answer an incoming call. When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore
        the call.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: settings for update
        :type settings: :class:`Monitoring`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = {}
        if settings.call_park_notification_enabled is not None:
            data['enableCallParkNotification'] = settings.call_park_notification_enabled
        if settings.monitored_elements is not None:
            id_list = []
            for me in settings.monitored_elements:
                if isinstance(me, str):
                    id_list.append(me)
                else:
                    id_list.append(me.member and me.member.member_id or me.cpe and me.cpe.cpe_id)
            data['monitoredElements'] = id_list
        await self.put(ep, params=params, json=data)


class AsNumbersApi(AsPersonSettingsApiChild):
    """
    API for person's numbers
    """

    feature = 'numbers'

    # TODO: documentation defect:
    #  https://developer.webex.com/docs/api/v1/webex-calling-person-settings-with-additional-settings/get-a-list-of
    #  -phone-numbers-for-a-person
    #  says the URL is /v1/people/{personId}/numbers
    #  while it actually is /v1/people/{personId}/features/numbers

    async def read(self, *, person_id: str, org_id: str = None) -> PersonNumbers:
        """
        Read Do Not Disturb Settings for a Person
        Retrieve a Person's Do Not Disturb Settings

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.
        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners) may
        use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return:
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return PersonNumbers.parse_obj(await self.get(ep, params=params))

    async def update(self, *, person_id: str, update: UpdatePersonNumbers, org_id: str = None):
        """
        Assign or unassign alternate phone numbers to a person.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone
        numbers must follow E.164 format for all countries, except for the United States, which can also follow the
        National format. Active phone numbers are in service.

        Assigning or Unassigning an alternate phone number to a person requires a full administrator auth token with
        a scope of spark-admin:telephony_config_write.

        :param person_id: Unique identifier of the person.
        :type person_id: str
        :param update: Update to apply
        :type update: :class:`UpdatePersonNumbers`
        :param org_id: organization to work on
        :type org_id: str
        """
        url = self.session.ep(f'telephony/config/people/{person_id}/numbers')
        params = org_id and {'orgId': org_id} or None
        body = update.json()
        await self.put(url=url, params=params, data=body)


class AsAuthCodesApi(AsPersonSettingsApiChild):
    """
    API for person's outgoing permission authorization codes
    """
    feature = 'outgoingPermission/authorizationCodes'

    async def read(self, person_id: str, org_id: str = None) -> list[AuthCode]:
        """
        Retrieve Authorization codes for a Workspace.

        Authorization codes are used to bypass permissions.

        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or
        a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param person_id: Unique identifier for the workspace.
        :type person_id: str
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: list of authorization codes
        :rtype: list of :class:`AuthCode`
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url, params=params)
        return parse_obj_as(list[AuthCode], data['authorizationCodes'])

    async def delete_codes(self, person_id: str, access_codes: list[Union[str, AuthCode]], org_id: str = None):
        """
        Modify Authorization codes for a workspace.

        Authorization codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a
        user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param person_id: Unique identifier for the workspace.
        :type person_id: str
        :param access_codes: authorization codes to remove
        :type access_codes: list[str]
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        body = {'deleteCodes': [ac.code if isinstance(ac, AuthCode) else ac
                                for ac in access_codes]}
        await self.put(url, params=params, json=body)

    async def create(self, person_id: str, code: str, description: str, org_id: str = None):
        """
        Modify Authorization codes for a workspace.

        Authorization codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a
        user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param person_id: Unique identifier for the workspace.
        :type person_id: str
        :param code: Indicates an authorization code.
        :type code: str
        :param description: Indicates the description of the authorization code.
        :type description: str
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        body = {'code': code,
                'description': description}
        await self.post(url, params=params, json=body)


@dataclass(init=False)


class AsTransferNumbersApi(AsPersonSettingsApiChild):
    """
    API for outgoing permission auto transfer numbers
    """
    feature = 'outgoingPermission/autoTransferNumbers'

    async def read(self, person_id: str, org_id: str = None) -> AutoTransferNumbers:
        """
        Retrieve Transfer Numbers Settings for a Workspace.

        When calling a specific call type, this workspace will be automatically transferred to another number. The
        person assigned the Auto Transfer Number can then approve the call and send it through or reject the call
        type. You can add up to 3 numbers.

        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or
        a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param person_id: Unique identifier for the workspace.
        :type person_id: str
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: auto transfer numbers
        :rtype: :class:`AutoTransferNumbers`
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url, params=params)
        return AutoTransferNumbers.parse_obj(data)

    async def configure(self, person_id: str, settings: AutoTransferNumbers, org_id: str = None):
        """
        Modify Transfer Numbers Settings for a Place.

        When calling a specific call type, this workspace will be automatically transferred to another number.
        The person assigned the Auto Transfer Number can then approve the call and send it through or reject the
        call type. You can add up to 3 numbers.

        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a
        user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param person_id: Unique identifier for the workspace.
        :type person_id: str
        :param settings: new auto transfer numbers
        :type settings: AutoTransferNumbers
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        body = settings.json()
        await self.put(url, params=params, data=body)


class AsOutgoingPermissionsApi(AsPersonSettingsApiChild):
    """
    API for person's outgoing permissions settings

    also used for workspace and location outgoing permissions
    """
    #: Only available for workspaces
    transfer_numbers: AsTransferNumbersApi
    #: Only available for workspaces
    auth_codes: AsAuthCodesApi

    feature = 'outgoingPermission'

    def __init__(self, *, session: AsRestSession,
                 workspaces: bool = False, locations: bool = False):
        super().__init__(session=session, workspaces=workspaces, locations=locations)
        if workspaces:
            # auto transfer numbers API seems to only exist for workspaces
            self.transfer_numbers = AsTransferNumbersApi(session=session,
                                                       workspaces=True)
            self.auth_codes = AsAuthCodesApi(session=session, workspaces=True)
        elif locations:
            self.transfer_numbers = AsTransferNumbersApi(session=session,
                                                       locations=True)
            self.auth_codes = None
        else:
            self.transfer_numbers = None
            self.auth_codes = None

    async def read(self, *, person_id: str, org_id: str = None) -> OutgoingPermissions:
        """
        Retrieve a Person's Outgoing Calling Permissions Settings

        You can change the outgoing calling permissions for a person if you want them to be different from your
        organization's default.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: outgoing permission settings for specific user
        :rtype: :class:`OutgoingPermissions`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return OutgoingPermissions.parse_obj(await self.get(ep, params=params))

    async def configure(self, *, person_id: str, settings: OutgoingPermissions, org_id: str = None):
        """
        Configure a Person's Outgoing Calling Permissions Settings

        Turn on outgoing call settings for this person to override the calling settings from the location that are
        used by default.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: new setting to be applied
        :type settings: :class:`OutgoingPermissions`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        await self.put(ep, params=params, data=settings.json())


class AsPersonForwardingApi(AsPersonSettingsApiChild):
    """
    API for person's call forwarding settings
    """

    feature = 'callForwarding'

    async def read(self, *, person_id: str, org_id: str = None) -> PersonForwardingSetting:
        """
        Retrieve a Person's Call Forwarding Settings

        Three types of call forwarding are supported:

        * Always – forwards all incoming calls to the destination you choose.

        * When busy – forwards all incoming calls to the destination you chose while the phone is in use or the person
          is busy.

        * When no answer – forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as power outage, failed Internet connection, or wiring problem

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: user's forwarding settings
        :rtype: PersonForwardingSetting
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return PersonForwardingSetting.parse_obj(await self.get(ep, params=params))

    async def configure(self, *, person_id: str, forwarding: PersonForwardingSetting, org_id: str = None):
        """
        Configure a Person's Call Forwarding Settings

        Three types of call forwarding are supported:

        * Always – forwards all incoming calls to the destination you choose.

        * When busy – forwards all incoming calls to the destination you chose while the phone is in use or the person
          is busy.

        * When no answer – forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as power outage, failed Internet connection, or wiring problem

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param forwarding: new forwarding settings
        :type forwarding: PersonForwardingSetting
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        # system_max_number_of_ring cannot be used in update
        data = forwarding.json(
            exclude={'call_forwarding':
                         {'no_answer':
                              {'system_max_number_of_rings': True}}})
        await self.put(ep, params=params, data=data)


class AsPrivacyApi(AsPersonSettingsApiChild):
    """
    API for person's call monitoring settings
    """

    feature = 'privacy'

    async def read(self, *, person_id: str, org_id: str = None) -> Privacy:
        """
        Get a person's Privacy Settings

        Get a person's privacy settings for the specified person id.

        The privacy feature enables the person's line to be monitored by others and determine if they can be reached
        by Auto Attendant services.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: privacy settings
        :rtype: :class:`Privacy`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return Privacy.parse_obj(data)

    async def configure(self, *, person_id: str, settings: Privacy, org_id: str = None):
        """
        Configure Call Waiting Settings for a Person

        Configure a Person's Call Waiting Settings

        With this feature, a person can place an active call on hold and answer an incoming call. When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore
        the call.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: settings for update
        :type settings: :class:`Monitoring`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.loads(settings.json())
        if settings.monitoring_agents is not None:
            id_list = []
            for ma in settings.monitoring_agents:
                if isinstance(ma, str):
                    id_list.append(ma)
                else:
                    id_list.append(ma.agent_id)
            data['monitoringAgents'] = id_list
        await self.put(ep, params=params, json=data)


class AsPushToTalkApi(AsPersonSettingsApiChild):
    """
    API for person's PTT settings
    """

    feature = 'pushToTalk'

    async def read(self, *, person_id: str, org_id: str = None) -> PushToTalkSettings:
        """
        Read Push-to-Talk Settings for a Person
        Retrieve a Person's Push-to-Talk Settings

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: PTT settings for specific user
        :rtype: PushToTalkSettings
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return PushToTalkSettings.parse_obj(await self.get(ep, params=params))

    async def configure(self, *, person_id: str, settings: PushToTalkSettings, org_id: str = None):
        """
        Configure Push-to-Talk Settings for a Person

        Configure a Person's Push-to-Talk Settings

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: new setting to be applied. For members only the ID needs to be set
        :type settings: PushToTalkSettings
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        if settings.members:
            # for an update member is just a list of IDs
            body_settings = settings.copy(deep=True)
            members = [m.member_id if isinstance(m, MonitoredMember) else m
                       for m in settings.members]
            body_settings.members = members
        else:
            body_settings = settings
        body = body_settings.json(exclude_none=False,
                                  exclude_unset=True)
        await self.put(ep, params=params, data=body)


class AsReceptionistApi(AsPersonSettingsApiChild):
    """
    API for person's receptionist client settings
    """

    feature = 'reception'

    async def read(self, *, person_id: str, org_id: str = None) -> ReceptionistSettings:
        """
        Read Receptionist Client Settings for a Person

        Retrieve a Person's Receptionist Client Settings

        To help support the needs of your front-office personnel, you can set up people or workspaces as telephone
        attendants so that they can screen all incoming calls to certain numbers within your organization.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: receptionist client settings
        :rtype: :class:`ReceptionistSettings`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return ReceptionistSettings.parse_obj(data)

    async def configure(self, *, person_id: str, settings: ReceptionistSettings, org_id: str = None):
        """
        Modify Executive Assistant Settings for a Person

        Modify the executive assistant settings for the specified personId.

        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set
        the call forward destination and join or leave an executive's pool.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: New receptionist client settings
        :type settings: :class:`ReceptionistSettings`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        if settings.enabled is None:
            raise ValueError('enabled is a mandatory parameter for updates')
        if settings.monitored_members and not settings.enabled:
            raise ValueError('when setting members enabled has to be True')
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.loads(settings.json())
        if settings.monitored_members is not None:
            id_list = []
            for me in settings.monitored_members:
                if isinstance(me, str):
                    id_list.append(me)
                else:
                    id_list.append(me.member_id)
            data['monitoredMembers'] = id_list
        await self.put(ep, params=params, json=data)


class AsScheduleApi(AsApiChild, base='telephony/config/locations'):
    """
    Schedules API
    """

    def __init__(self, *, session: AsRestSession, base: ScheduleApiBase):
        super().__init__(session=session, base=base.value)
        if base == ScheduleApiBase.people:
            self.after_id = '/features/schedules'
        elif base == ScheduleApiBase.locations:
            self.after_id = '/schedules'
        else:
            raise ValueError('unexpected value for base')

    def _endpoint(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr = None, schedule_id: str = None,
                  event_id: str = None):
        """
        location specific feature endpoint like v1/telephony/config/locations/{obj_id}/schedules/.... or
        v1/people/{obj_id}/features/schedules/....

        :meta private:
        :param obj_id: Unique identifier for the location or user
        :type obj_id: str
        :param schedule_type: type of schedule
        :type schedule_type: ScheduleType
        :param schedule_id: schedule id
        :type schedule_id: str
        :return: full endpoint
        :rtype: str
        """
        ep = self.ep(path=f'{obj_id}{self.after_id}')
        if schedule_type is not None:
            schedule_type = ScheduleType.type_or_str(schedule_type)
            ep = f'{ep}/{schedule_type.value}/{schedule_id}'
            if event_id is not None:
                event_id = event_id and f'/{event_id}' or ''
                ep = f'{ep}/events{event_id}'
        return ep

    def list_gen(self, *, obj_id: str, org_id: str = None, schedule_type: ScheduleType = None,
             name: str = None, **params) -> AsyncGenerator[Schedule, None, None]:
        """
        List of Schedules for a Person or location

        List schedules for a person or location in an organization.

        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week
        by defining one or more events. holidays schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param obj_id: Return the list of schedules for this location or user
        :type obj_id: str
        :param org_id: List schedules for this organization.
        :type org_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :param name: Only return schedules with the matching name.
        :return: yields schedules
        """
        url = self._endpoint(obj_id=obj_id)
        if schedule_type is not None:
            params['type'] = schedule_type.value
        if name is not None:
            params['name'] = name
        if org_id is not None:
            params['orgId'] = org_id

        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Schedule, params=params or None)

    async def list(self, *, obj_id: str, org_id: str = None, schedule_type: ScheduleType = None,
             name: str = None, **params) -> List[Schedule]:
        """
        List of Schedules for a Person or location

        List schedules for a person or location in an organization.

        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week
        by defining one or more events. holidays schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param obj_id: Return the list of schedules for this location or user
        :type obj_id: str
        :param org_id: List schedules for this organization.
        :type org_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :param name: Only return schedules with the matching name.
        :return: yields schedules
        """
        url = self._endpoint(obj_id=obj_id)
        if schedule_type is not None:
            params['type'] = schedule_type.value
        if name is not None:
            params['name'] = name
        if org_id is not None:
            params['orgId'] = org_id

        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=Schedule, params=params or None)]

    async def details(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                org_id: str = None) -> Schedule:
        """
        Get Details for a Schedule

        Retrieve Schedule details.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Retrieving schedule details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param obj_id: Retrieve schedule details in this location or user
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Retrieve the schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Retrieve schedule details from this organization.
        :type org_id: str
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id)
        data = await self.get(url, params=params)
        result = Schedule.parse_obj(data)
        return result

    async def create(self, *, obj_id: str, schedule: Schedule, org_id: str = None) -> str:
        """
        Create a Schedule

        Create new Schedule for the given location.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Creating a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param obj_id: Create the schedule for this location or user
        :type obj_id: str
        :param schedule: Schedule to be created
        :type schedule: Schedule
        :param org_id: Create the schedule for this organization.
        :type org_id: str
        :return: ID of the newly created schedule.
        :rtype: str
        """
        schedule_data = schedule.create_update()
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id)
        data = await self.post(url, data=schedule_data, params=params)
        result = data['id']
        return result

    async def update(self, *, obj_id: str, schedule: Schedule, schedule_type: ScheduleTypeOrStr = None,
               schedule_id: str = None, org_id: str = None) -> str:
        """
        Update a Schedule

        Update the designated Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Updating a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        NOTE: The Schedule ID will change upon modification of the Schedule name

        :param obj_id: Location or user for  which this schedule exists
        :type obj_id: str
        :param schedule: data for the update
        :type schedule: Schedule
        :param schedule_type: Type of the schedule. Default: schedule_type from schedule
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Update schedule with the matching ID. Default: schedule_id from schedule
        :type schedule_id: str
        :param org_id: Update schedule from this organization.
        :type org_id: str
        :return: schedule id
        """
        schedule_type = schedule_type or schedule.schedule_type
        schedule_id = schedule_id or schedule.schedule_id
        schedule_data = schedule.create_update(update=True)
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id)
        data = await self.put(url, data=schedule_data, params=params)
        return data['id']

    async def delete_schedule(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                        org_id: str = None):
        """
        Delete a Schedule

        Delete the designated Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Deleting a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param obj_id: Location or user from which to delete a schedule.
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Delete the schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Retrieve schedule details from this organization.
        :type org_id: str
        :return:
        """
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id)
        params = org_id and {'orgId': org_id} or None
        await self.delete(url, params=params)

    async def event_details(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                      event_id: str, org_id: str = None) -> Event:
        """
        Get Details for a Schedule Event

        Retrieve Schedule Event details.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Retrieving schedule event details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param obj_id: Retrieve schedule event details for this location or user
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Retrieve schedule event details for schedule with the matching ID.
        :type schedule_id: str
        :param event_id: Retrieve the schedule event with the matching schedule event ID.
        :type event_id: str
        :param org_id: Retrieve schedule event details from this organization.
        :type org_id: str
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id=event_id)
        data = await self.get(url, params=params)
        result = Event.parse_obj(data)
        return result

    async def event_create(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                     event: Event, org_id: str = None) -> str:
        """
        Create a Schedule Event

        Create new Event for the given location or user Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Creating a schedule event requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param obj_id: Create the schedule for this location.
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Create event for a given schedule ID.
        :type schedule_id: str
        :param event: event data
        :type event: Event
        :param org_id: Retrieve schedule event details from this organization.
        :type org_id: str
        :return: event id
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id='')
        data = event.json(exclude={'event_id'})
        data = await self.post(url, data=data, params=params)
        return data['id']

    async def event_update(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                     event: Event, event_id: str = None, org_id: str = None) -> str:
        """
        Update a Schedule Event

        Update the designated Schedule Event.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Updating a schedule event requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        NOTE: The Schedule Event ID will change upon modification of the Schedule event name.

        :param obj_id: Location or user for which this schedule event exists.
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Update schedule event with the matching schedule ID.
        :type schedule_id: str
        :param event: update settings
        :type event: Event
        :param event_id: Update the schedule event with the matching schedule event ID. Default: event id from event
        :type event_id: str
        :param org_id: Update schedule from this organization.
        :type org_id: str
        :return: event id; changed if name changed
        """
        event_id = event_id or event.event_id
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id=event_id)
        event_data = event.json(exclude={'event_id'})
        data = await self.put(url, data=event_data, params=params)
        return data['id']

    async def event_delete(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                     event_id: str, org_id: str = None):
        """
        Delete a Schedule Event

        Delete the designated Schedule Event.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Deleting a schedule event requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param obj_id: Location or user from which to delete a schedule.
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Delete schedule event with the matching schedule ID.
        :type schedule_id: str
        :param event_id: Delete the schedule event with the matching schedule event ID. Default: event id from event
        :type event_id: str
        :param org_id: Delete schedule from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id=event_id)
        await self.delete(url, params=params)


class AsVoicemailApi(AsPersonSettingsApiChild):
    """
    API for person's call voicemail settings
    """

    feature = 'voicemail'

    async def read(self, *, person_id: str, org_id: str = None) -> VoicemailSettings:
        """
        Read Voicemail Settings for a Person
        Retrieve a Person's Voicemail Settings

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, .wav, format.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: user's voicemail settings
        :rtype: VoicemailSettings
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return VoicemailSettings.parse_obj(await self.get(url, params=params))

    async def configure(self, *, person_id: str, settings: VoicemailSettings, org_id: str = None):
        """
        Configure Voicemail Settings for a Person
        Configure a person's Voicemail Settings

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, .wav, format.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not
        include the voicemail files.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.
        :return:
        """
        # some settings can't be part of an update
        data = settings.json(exclude={'send_busy_calls': {'greeting_uploaded': True},
                                      'send_unanswered_calls': {'system_max_number_of_rings': True,
                                                                'greeting_uploaded': True},
                                      'voice_message_forwarding_enabled': True
                                      })
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        await self.put(url, data=data, params=params)

    async def _configure_greeting(self, *, person_id: str, content: Union[BufferedReader, str],
                            upload_as: str = None, org_id: str = None,
                            greeting_key: str):
        """
        handled greeting configuration

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param greeting_key: 'uploadBusyGreeting' or 'uploadNoAnswerGreeting'
        """
        if isinstance(content, str):
            upload_as = os.path.basename(content)
            content = open(content, mode='rb')
            must_close = True
        else:
            must_close = False
            # an existing reader
            if not upload_as:
                raise ValueError('upload_as is required')
        encoder = MultipartEncoder(fields={'file': (upload_as, content, 'audio/wav')})
        ep = self.f_ep(person_id=person_id, path=f'actions/{greeting_key}/invoke')
        params = org_id and {'orgId': org_id} or None
        try:
            await self.post(ep, data=encoder, headers={'Content-Type': encoder.content_type},
                      params=params)
        finally:
            if must_close:
                content.close()

    def configure_busy_greeting(self, *, person_id: str, content: Union[BufferedReader, str],
                                upload_as: str = None, org_id: str = None):
        """
        Configure Busy Voicemail Greeting for a Person
        Configure a Person's Busy Voicemail Greeting by uploading a Waveform Audio File Format, .wav, encoded audio
        file.

        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        self._configure_greeting(person_id=person_id, content=content, upload_as=upload_as, org_id=org_id,
                                 greeting_key='uploadBusyGreeting')

    def configure_no_answer_greeting(self, person_id: str, content: Union[BufferedReader, str],
                                     upload_as: str = None, org_id: str = None):
        """
        Configure No Answer Voicemail Greeting for a Person
        Configure a Person's No Answer Voicemail Greeting by uploading a Waveform Audio File Format, .wav, encoded
        audio file.

        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        self._configure_greeting(person_id=person_id, content=content, upload_as=upload_as, org_id=org_id,
                                 greeting_key='uploadNoAnswerGreeting')


@dataclass(init=False)
class AsPersonSettingsApi(AsApiChild, base='people'):
    """
    API for all user level settings
    """

    #: Person's Application Services Settings
    appservices: AsAppServicesApi
    #: Barge In Settings for a Person
    barge: AsBargeApi
    #: Do Not Disturb Settings for a Person
    dnd: AsDndApi
    #: Call Intercept Settings for a Person
    call_intercept: AsCallInterceptApi
    #: Call Recording Settings for a Person
    call_recording: AsCallRecordingApi
    #: Call Waiting Settings for a Person
    call_waiting: AsCallWaitingApi
    #: Caller ID Settings for a Person
    caller_id: AsCallerIdApi
    #: Person's Calling Behavior
    calling_behavior: AsCallingBehaviorApi
    #: Executive Assistant Settings for a Person
    exec_assistant: AsExecAssistantApi
    #: Forwarding Settings for a Person
    forwarding: AsPersonForwardingApi
    #: Hoteling Settings for a Person
    hoteling: AsHotelingApi
    #: Person's Monitoring Settings
    monitoring: AsMonitoringApi
    #: Phone Numbers for a Person
    numbers: AsNumbersApi
    #: Incoming Permission Settings for a Person
    permissions_in: AsIncomingPermissionsApi
    #: Person's Outgoing Calling Permissions Settings
    permissions_out: AsOutgoingPermissionsApi
    #: Person's Privacy Settings
    privacy: AsPrivacyApi
    #: Push-to-Talk Settings for a Person
    push_to_talk: AsPushToTalkApi
    #: Receptionist Client Settings for a Person
    receptionist: AsReceptionistApi
    #: Schedules for a Person
    schedules: AsScheduleApi
    #: Voicemail Settings for a Person
    voicemail: AsVoicemailApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.appservices = AsAppServicesApi(session=session)
        self.barge = AsBargeApi(session=session)
        self.dnd = AsDndApi(session=session)
        self.call_intercept = AsCallInterceptApi(session=session)
        self.call_recording = AsCallRecordingApi(session=session)
        self.call_waiting = AsCallWaitingApi(session=session)
        self.calling_behavior = AsCallingBehaviorApi(session=session)
        self.caller_id = AsCallerIdApi(session=session)
        self.exec_assistant = AsExecAssistantApi(session=session)
        self.forwarding = AsPersonForwardingApi(session=session)
        self.hoteling = AsHotelingApi(session=session)
        self.monitoring = AsMonitoringApi(session=session)
        self.numbers = AsNumbersApi(session=session)
        self.permissions_in = AsIncomingPermissionsApi(session=session)
        self.permissions_out = AsOutgoingPermissionsApi(session=session)
        self.privacy = AsPrivacyApi(session=session)
        self.push_to_talk = AsPushToTalkApi(session=session)
        self.receptionist = AsReceptionistApi(session=session)
        self.schedules = AsScheduleApi(session=session, base=ScheduleApiBase.people)
        self.voicemail = AsVoicemailApi(session=session)

    async def reset_vm_pin(self, person_id: str, org_id: str = None):
        """
        Reset Voicemail PIN

        Reset a voicemail PIN for a person.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. A voicemail PIN is used to retrieve your voicemail messages.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners) may
            use this parameter as the default is the same organization as the token used to access API.
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{person_id}/features/voicemail/actions/resetPin/invoke')
        await self.post(url, params=params)


class AsAccessCodesApi(AsApiChild, base='telephony/config/locations'):
    """
    Access codes API
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific feature endpoint like
        /v1/telephony/config/locations/{locationId}/outgoingPermission/accessCodes}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/outgoingPermission/accessCodes{path}')
        return ep

    async def read(self, *, location_id: str, org_id: str = None) -> list[AuthCode]:
        """
        Get Location Access Code

        Retrieve access codes details for a customer location.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Retrieving access codes details requires a full, user or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.


        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        :return: list of :class:`wxc_sdk.common.CallPark`
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        data = await self.get(url, params=params)
        return parse_obj_as(list[AuthCode], data['accessCodes'])

    async def create(self, *, location_id: str, access_codes: list[AuthCode], org_id: str = None) -> list[AuthCode]:
        """
        Create access code in location

        :param location_id: Add new access code for this location.
        :type location_id: str
        :param access_codes: Access code details
        :type access_codes: list of :class:`wxc_sdk.common.AuthCode`
        :param org_id: Add new access code for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = {'accessCodes': [json.loads(ac.json()) for ac in access_codes]}
        await self.post(url, json=body, params=params)

    async def delete_codes(self, *, location_id: str, access_codes: list[Union[str, AuthCode]],
                     org_id: str = None) -> list[AuthCode]:
        """
        Delete Access Code Location

        Deletes the access code details for a particular location for a customer.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Modifying the access code location details requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Deletes the access code details for this location.
        :type location_id: str
        :param access_codes: access codes to delete
        :type access_codes: list of :class:`wxc_sdk.common.AuthCode` or str
        :param org_id: Delete access codes from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = {'deleteCodes': [ac.code if isinstance(ac, AuthCode) else ac
                                for ac in access_codes]}
        await self.put(url, json=body, params=params)


class AsForwardingApi:
    """
    API for forwarding settings on call queues, hunt groups, and auto attendants
    """

    def __init__(self, session: AsRestSession, feature_selector: FeatureSelector):
        self._session = session
        self._feature = feature_selector

    def _endpoint(self, location_id: str, feature_id: str, path: str = None):
        """

        :meta private:
        :param location_id:
        :param feature_id:
        :param path:
        :return:
        """
        path = path and f'/{path}' or ''
        ep = self._session.ep(path=f'telephony/config/locations/{location_id}/{self._feature.value}/'
                                   f'{feature_id}/callForwarding{path}')
        return ep

    async def settings(self, location_id: str, feature_id: str, org_id: str = None) -> CallForwarding:
        """
        Retrieve Call Forwarding settings for the designated feature including the list of call
        forwarding rules.

        :param location_id: Location in which this feature exists.
        :type location_id: str
        :param feature_id: Retrieve the call forwarding settings for this entity
        :type feature_id: str
        :param org_id: Retrieve call forwarding settings from this organization.
        :type org_id: str
        :return: call forwarding settings
        :rtype: class:`CallForwarding`
        """
        params = org_id and {'orgId': org_id} or {}
        url = self._endpoint(location_id=location_id, feature_id=feature_id)
        data = await self._session.rest_get(url=url, params=params)
        result = CallForwarding.parse_obj(data['callForwarding'])
        return result

    async def update(self, location_id: str, feature_id: str,
               forwarding: CallForwarding, org_id: str = None):
        """
        Update Call Forwarding Settings for a feature

        Update Call Forwarding settings for the designated feature.

        Updating call forwarding settings for a feature requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this feature exists.
        :type location_id: str
        :param feature_id: Update call forwarding settings for this feature.
        :type feature_id: str
        :param forwarding: Forwarding settings
        :type forwarding: :class:`CallForwarding`
        :param org_id: Update feature forwarding settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or {}
        url = self._endpoint(location_id=location_id, feature_id=feature_id)
        body = forwarding.dict()

        # update only has 'id' and 'enabled' in rules
        # determine names of ForwardingRule fields to remove
        to_pop = [field
                  for field in ForwardingRule.__fields__
                  if field not in {'id', 'enabled'}]
        for rule in body['rules']:
            rule: Dict
            for field in to_pop:
                rule.pop(field, None)
        body = {'callForwarding': body}
        await self._session.rest_put(url=url, json=body, params=params)

    async def create_call_forwarding_rule(self, location_id: str, feature_id: str,
                                    forwarding_rule: ForwardingRuleDetails, org_id: str = None) -> str:
        """
        Create a Selective Call Forwarding Rule feature

        A selective call forwarding rule for feature to be forwarded or not
        forwarded to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available feature's call
        forwarding settings.
        :param location_id: Location in which the call queue exists.
        :type location_id: str
        :param feature_id: Create the rule for this feature
        :type feature_id: str
        :param forwarding_rule: details of rule to be created
        :type forwarding_rule: :class:`ForwardingRuleDetails`
        :param org_id: Create the feature forwarding rule for this organization.
        :type org_id: str
        :return: forwarding rule id
        :rtype; str
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path='selectiveRules')
        body = forwarding_rule.dict()
        params = org_id and {'orgId': org_id} or None
        data = await self._session.rest_post(url=url, json=body, params=params)
        return data['id']

    async def call_forwarding_rule(self, location_id: str, feature_id: str, rule_id: str,
                             org_id: str = None) -> ForwardingRuleDetails:
        """
        Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue.

        A selective call forwarding rule for feature allows calls to be forwarded or not forwarded
        to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the feature's call
        forwarding settings.
        :param location_id: Location in which the feature exists.
        :type location_id: stre
        :param feature_id: Retrieve setting for a rule for this feature.
        :type feature_id: str
        :param rule_id: feature rule you are retrieving settings for.
        :type rule_id: str
        :param org_id: Retrieve feature forwarding settings from this organization.
        :type org_id: str
        :return: call forwarding rule details
        :rtype: :class:`ForwardingRuleDetails`
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules/{rule_id}')
        params = org_id and {'orgId': org_id} or None
        data = await self._session.rest_get(url=url, params=params)
        result = ForwardingRuleDetails.parse_obj(data)
        return result

    async def update_call_forwarding_rule(self, location_id: str, feature_id: str, rule_id: str,
                                    forwarding_rule: ForwardingRuleDetails, org_id: str = None) -> str:
        """
        Update a Selective Call Forwarding Rule's settings for the designated feature.

        A selective call forwarding rule for feature allows calls to be forwarded or not forwarded
        to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the feature's call
        forwarding settings.

        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which the feature exists.
        :type location_id: str
        :param feature_id: Update settings for a rule for this feature.
        :type feature_id: str
        :param rule_id: feature you are updating settings for.
        :type rule_id: str
        :param forwarding_rule: forwarding rule details for update
        :type forwarding_rule: :class:`ForwardingRuleDetails`
        :param org_id: Update feature rule settings for this organization.
        :type org_id: str
        :return: new call forwarding rule id
        :rtype: str
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules/{rule_id}')
        params = org_id and {'orgId': org_id} or None
        body = forwarding_rule.dict()
        data = await self._session.rest_put(url=url, params=params, json=body)
        return data['id']

    async def delete_call_forwarding_rule(self, location_id: str, feature_id: str, rule_id: str, org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for the designated feature.

        A selective call forwarding rule for a feature allows calls to be forwarded or not forwarded
        to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the feature's call
        forwarding
        settings.
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules/{rule_id}')
        params = org_id and {'orgId': org_id} or None
        await self._session.delete(url=url, params=params)


class AsAutoAttendantApi(AsApiChild, base='telephony/config/autoAttendants'):
    """
    Auto attendant API
    """
    forwarding: AsForwardingApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.forwarding = AsForwardingApi(session=session, feature_selector=FeatureSelector.auto_attendants)

    def _endpoint(self, *, location_id: str = None, auto_attendant_id: str = None) -> str:
        """
        auto attendant specific feature endpoint like /v1/telephony/config/locations/{locationId}/autoAttendants/{
        auto_attendant_id}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param auto_attendant_id: auto attendant id
        :type auto_attendant_id: str
        :return: full endpoint
        :rtype: str
        """
        if location_id is None:
            return self.session.ep('telephony/config/autoAttendants')
        else:
            ep = self.session.ep(f'telephony/config/locations/{location_id}/autoAttendants')
            if auto_attendant_id:
                ep = f'{ep}/{auto_attendant_id}'
            return ep

    def list_gen(self, *, org_id: str = None, location_id: str = None, name: str = None,
             phone_number: str = None, **params) -> AsyncGenerator[AutoAttendant, None, None]:
        """
        Read the List of Auto Attendants
        List all Auto Attendants for the organization.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List auto attendants for this organization.
        :type org_id: str
        :param location_id: Return the list of auto attendants for this location.
        :type location_id: str
        :param name: Only return auto attendants with the matching name.
        :type name: str
        :param phone_number: Only return auto attendants with the matching phone number.
        :type phone_number: str
        :return: yields :class:`AutoAttendant` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=AutoAttendant, params=params, item_key='autoAttendants')

    async def list(self, *, org_id: str = None, location_id: str = None, name: str = None,
             phone_number: str = None, **params) -> List[AutoAttendant]:
        """
        Read the List of Auto Attendants
        List all Auto Attendants for the organization.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List auto attendants for this organization.
        :type org_id: str
        :param location_id: Return the list of auto attendants for this location.
        :type location_id: str
        :param name: Only return auto attendants with the matching name.
        :type name: str
        :param phone_number: Only return auto attendants with the matching phone number.
        :type phone_number: str
        :return: yields :class:`AutoAttendant` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=AutoAttendant, params=params, item_key='autoAttendants')]

    async def by_name(self, *, name: str, location_id: str = None, org_id: str = None) -> Optional[AutoAttendant]:
        """
        Get auto attendant info by name

        :param location_id:
        :param name:
        :param org_id:
        :return:
        """
        return next((hg for hg in await self.list(name=name, location_id=location_id, org_id=org_id)
                     if hg.name == name), None)

    async def details(self, *, location_id: str, auto_attendant_id: str, org_id: str = None) -> AutoAttendant:
        """
        Get Details for an Auto Attendant
        Retrieve an Auto Attendant details.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Retrieving an auto attendant details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve an auto attendant details in this location.
        :type location_id: str
        :param auto_attendant_id: Retrieve the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Retrieve auto attendant details from this organization.
        :type org_id: str
        :return: auto attendant details
        :rtype: :class:`AutoAttendant`
        """
        url = self._endpoint(location_id=location_id, auto_attendant_id=auto_attendant_id)
        params = org_id and {'orgId': org_id} or None
        return AutoAttendant.parse_obj(await self.get(url, params=params))

    async def create(self, *, location_id: str, settings: AutoAttendant, org_id: str = None) -> str:
        """
        Create an Auto Attendant
        Create new Auto Attendant for the given location.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Creating an auto attendant requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Create the auto attendant for this location.
        :type location_id: str
        :param settings: auto attendant settings for new auto attendant
        :type settings: :class:`AutoAttendant`
        :param org_id: Create the auto attendant for this organization.
        :type org_id: str
        :return: ID of the newly created auto attendant.
        :rtype: str
        """
        data = settings.create_or_update()
        url = self._endpoint(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.post(url, data=data, params=params)
        return data['id']

    async def update(self, *, location_id: str, auto_attendant_id: str, settings: AutoAttendant, org_id: str = None):
        """
        Update an Auto Attendant
        Update the designated Auto Attendant.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Updating an auto attendant requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update an auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param settings: auto attendant settings for the update
        :type settings: :class:`AutoAttendant`
        :param org_id: Create the auto attendant for this organization.
        :type org_id: str
        """
        data = settings.create_or_update()
        url = self._endpoint(location_id=location_id, auto_attendant_id=auto_attendant_id)
        params = org_id and {'orgId': org_id} or None
        await self.put(url, data=data, params=params)

    async def delete_auto_attendant(self, *, location_id: str, auto_attendant_id: str, org_id: str = None):
        """
        elete the designated Auto Attendant.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Deleting an auto attendant requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete an auto attendant.
        :type location_id: str
        :param auto_attendant_id: Delete the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Delete the auto attendant from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, auto_attendant_id=auto_attendant_id)
        params = org_id and {'orgId': org_id} or None
        await self.delete(url, params=params)


class AsCallParkApi(AsApiChild, base='telephony/config/callParks'):
    """
    Call Park API
    """

    def _endpoint(self, *, location_id: str, callpark_id: str = None, path: str = None) -> str:
        """
        call park specific feature endpoint like /v1/telephony/config/locations/{locationId}/callParks/{callpark_id}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param callpark_id: call park id
        :type callpark_id: str
        :param path: addtl. path
        :type path: str
        :return: full endpoint
        :rtype: str
        """
        call_park_id = callpark_id and f'/{callpark_id}' or ''
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/callParks{call_park_id}{path}')
        return ep

    def list_gen(self, location_id: str, order: Literal['ASC', 'DSC'] = None, name: str = None,
             org_id: str = None, **params) -> AsyncGenerator[CallPark, None, None]:
        """
        Read the List of Call Parks

        List all Call Parks for the organization.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Return the list of call parks for this location.
        :type location_id: str
        :param order: Sort the list of call parks by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call parks that contains the given name. The maximum length is 80.
        :type name: str
        :param org_id: List call parks for this organization.
        :type org_id: str
        :return: yields :class:`CallPark` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i > 1 and v is not None and k != 'params')
        url = self._endpoint(location_id=location_id)
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CallPark, params=params, item_key='callParks')

    async def list(self, location_id: str, order: Literal['ASC', 'DSC'] = None, name: str = None,
             org_id: str = None, **params) -> List[CallPark]:
        """
        Read the List of Call Parks

        List all Call Parks for the organization.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Return the list of call parks for this location.
        :type location_id: str
        :param order: Sort the list of call parks by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call parks that contains the given name. The maximum length is 80.
        :type name: str
        :param org_id: List call parks for this organization.
        :type org_id: str
        :return: yields :class:`CallPark` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i > 1 and v is not None and k != 'params')
        url = self._endpoint(location_id=location_id)
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=CallPark, params=params, item_key='callParks')]

    async def create(self, location_id: str, settings: CallPark, org_id: str = None) -> str:
        """
        Create a Call Park

        Create new Call Parks for the given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Creating a call park requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Create the call park for this location.
        :type location_id: str
        :param settings: settings for new call park
        :type settings: :class:`CallPark`
        :param org_id: Create the call park for this organization.
        :return: ID of the newly created call park.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = settings.create_or_update()
        data = await self.post(url, data=body, params=params)
        return data['id']

    async def delete_callpark(self, location_id: str, callpark_id: str, org_id: str = None):
        """
        Delete a Call Park

        Delete the designated Call Park.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Deleting a call park requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Location from which to delete a call park.
        :type location_id: str
        :param callpark_id: Delete the call park with the matching ID.
        :type callpark_id: str
        :param org_id: Delete the call park from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, callpark_id=callpark_id)
        params = org_id and {'orgId': org_id} or None
        await self.delete(url, params=params)

    async def details(self, location_id: str, callpark_id: str, org_id: str = None) -> CallPark:
        """
        Get Details for a Call Park

        Retrieve Call Park details.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving call park details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Retrieve settings for a call park in this location.
        :type location_id: str
        :param callpark_id: Retrieve settings for a call park with the matching ID.
        :type callpark_id: str
        :param org_id: Retrieve call park settings from this organization.
        :type org_id: str
        :return: call park info
        :rtype: :class:`CallPark`
        """
        url = self._endpoint(location_id=location_id, callpark_id=callpark_id)
        params = org_id and {'orgId': org_id} or None
        return CallPark.parse_obj(await self.get(url, params=params))

    async def update(self, location_id: str, callpark_id: str, settings: CallPark, org_id: str = None) -> str:
        """
        Update a Call Park

        Update the designated Call Park.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Updating a call park requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: RLocation in which this call park exists.
        :type location_id: str
        :param callpark_id: Update settings for a call park with the matching ID.
        :type callpark_id: str
        :param settings: updates
        :type settings: :class:`CallPark`
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, callpark_id=callpark_id)
        body = settings.create_or_update()
        data = await self.put(url, data=body, params=params)
        return data['id']

    def available_agents_gen(self, location_id: str, call_park_name: str = None, name: str = None, phone_number: str = None,
                         order: str = None, org_id: str = None) -> AsyncGenerator[PersonPlaceAgent, None, None]:
        """
        Get available agents from Call Parks
        Retrieve available agents from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available agents from call parks requires a full or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_park_name: Only return available agents from call parks with the matching name.
        :type call_park_name: str
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, number and extension.
            The maximum supported sort order value is 3.
        :type order: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :return: yields :class:`PersonPlaceCallPark` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableUsers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=PersonPlaceAgent, params=params, item_key='agents')

    async def available_agents(self, location_id: str, call_park_name: str = None, name: str = None, phone_number: str = None,
                         order: str = None, org_id: str = None) -> List[PersonPlaceAgent]:
        """
        Get available agents from Call Parks
        Retrieve available agents from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available agents from call parks requires a full or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_park_name: Only return available agents from call parks with the matching name.
        :type call_park_name: str
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, number and extension.
            The maximum supported sort order value is 3.
        :type order: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :return: yields :class:`PersonPlaceCallPark` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableUsers')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=PersonPlaceAgent, params=params, item_key='agents')]

    def available_recalls_gen(self, location_id: str, name: str = None, order: str = None,
                          org_id: str = None) -> AsyncGenerator[AvailableRecallHuntGroup, None, None]:
        """
        Get available recall hunt groups from Call Parks

        Retrieve available recall hunt groups from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available recall hunt groups from call parks requires a full or read-only administrator auth
        token with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available recall hunt groups for this location.
        :type location_id: str
        :param name: Only return available recall hunt groups with the matching name.
        :type name: str
        :param order: Order the available recall hunt groups according to the designated fields. Available sort
            fields: lname.
        :param order: str
        :param org_id: Return the available recall hunt groups for this organization.
        :type org_id: str
        :return: yields :class:`AvailableRecallHuntGroup` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableRecallHuntGroups')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=AvailableRecallHuntGroup,
                                              params=params, item_key='huntGroups')

    async def available_recalls(self, location_id: str, name: str = None, order: str = None,
                          org_id: str = None) -> List[AvailableRecallHuntGroup]:
        """
        Get available recall hunt groups from Call Parks

        Retrieve available recall hunt groups from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available recall hunt groups from call parks requires a full or read-only administrator auth
        token with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available recall hunt groups for this location.
        :type location_id: str
        :param name: Only return available recall hunt groups with the matching name.
        :type name: str
        :param order: Order the available recall hunt groups according to the designated fields. Available sort
            fields: lname.
        :param order: str
        :param org_id: Return the available recall hunt groups for this organization.
        :type org_id: str
        :return: yields :class:`AvailableRecallHuntGroup` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableRecallHuntGroups')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=AvailableRecallHuntGroup,
                                              params=params, item_key='huntGroups')]

    async def call_park_settings(self, location_id: str, org_id: str = None) -> LocationCallParkSettings:
        """
        Get Call Park Settings

        Retrieve Call Park Settings from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving settings from call parks requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Return the call park settings for this location.
        :type location_id: str
        :param org_id: Return the call park settings for this organization.
        :type org_id: str
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, path='settings')
        return LocationCallParkSettings.parse_obj(await self.get(url, params=params))

    async def update_call_park_settings(self, location_id: str, settings: LocationCallParkSettings, org_id: str = None):
        """
        Update Call Park settings

        Update Call Park settings for the designated location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Updating call park settings requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location for which call park settings will be updated.
        :type location_id: str
        :param settings: update settings
        :type settings: :class:`LocationCallParkSettings`
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, path='settings')
        body = settings.update()
        await self.put(url, params=params, data=body)


class AsCallPickupApi(AsApiChild, base='telephony/config/callPickups'):
    """
    Call Pickup API
    """

    def _endpoint(self, *, location_id: str, pickup_id: str = None, path: str = None) -> str:
        """
        call park specific feature endpoint like /v1/telephony/config/locations/{locationId}/callPickups/{pickup_id}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param pickup_id: call pickup id
        :type pickup_id: str
        :param path: addtl. path
        :type path: str
        :return: full endpoint
        :rtype: str
        """
        pickup_id = pickup_id and f'/{pickup_id}' or ''
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/callPickups{pickup_id}{path}')
        return ep

    def list_gen(self, location_id: str, order: Literal['ASC', 'DSC'] = None, name: str = None,
             org_id: str = None, **params) -> AsyncGenerator[CallPickup, None, None]:
        """
        Read the List of Call Pickups

        List all Call Pickups for the organization.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving this list requires a full, user, or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Return the list of call pickups for this location.
        :type location_id: str
        :param order: Sort the list of call pickups by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call pickups that contains the given name. The maximum length is 80.
        :type name: str
        :param org_id: List call pickups for this organization.
        :type org_id: str
        :return: yields :class:`CallPickup` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i > 1 and v is not None and k != 'params')
        url = self._endpoint(location_id=location_id)
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CallPickup, params=params, item_key='callPickups')

    async def list(self, location_id: str, order: Literal['ASC', 'DSC'] = None, name: str = None,
             org_id: str = None, **params) -> List[CallPickup]:
        """
        Read the List of Call Pickups

        List all Call Pickups for the organization.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving this list requires a full, user, or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Return the list of call pickups for this location.
        :type location_id: str
        :param order: Sort the list of call pickups by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call pickups that contains the given name. The maximum length is 80.
        :type name: str
        :param org_id: List call pickups for this organization.
        :type org_id: str
        :return: yields :class:`CallPickup` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i > 1 and v is not None and k != 'params')
        url = self._endpoint(location_id=location_id)
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=CallPickup, params=params, item_key='callPickups')]

    async def create(self, location_id: str, settings: CallPickup, org_id: str = None) -> str:
        """
        Create a Call Pickup

        Create new Call Pickups for the given location.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Creating a call pickup requires a full or user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Create the call pickup for this location.
        :type location_id: str
        :param settings: settings for new call pickup
        :type settings: :class:`CallPickup`
        :param org_id: Create the call pickup for this organization.
        :return: ID of the newly created call pickup.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = settings.create_or_update()
        data = await self.post(url, data=body, params=params)
        return data['id']

    async def delete_pickup(self, location_id: str, pickup_id: str, org_id: str = None):
        """
        Delete a Call Pickup

        Delete the designated Call Pickup.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Deleting a call pickup requires a full or user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location from which to delete a call pickup.
        :type location_id: str
        :param pickup_id: Delete the call pickup with the matching ID.
        :type pickup_id: str
        :param org_id: Delete the call pickup from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, pickup_id=pickup_id)
        params = org_id and {'orgId': org_id} or None
        await self.delete(url, params=params)

    async def details(self, location_id: str, pickup_id: str, org_id: str = None) -> CallPickup:
        """
        Get Details for a Call Pickup

        Retrieve Call Pickup details.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving call pickup details requires a full, user, or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Retrieve settings for a call pickup in this location.
        :type location_id: str
        :param pickup_id: Retrieve settings for a call pickup with the matching ID.
        :type pickup_id: str
        :param org_id: Retrieve call pickup settings from this organization.
        :type org_id: str
        :return: call pickup info
        :rtype: :class:`CallPickup`
        """
        url = self._endpoint(location_id=location_id, pickup_id=pickup_id)
        params = org_id and {'orgId': org_id} or None
        return CallPickup.parse_obj(await self.get(url, params=params))

    async def update(self, location_id: str, pickup_id: str, settings: CallPickup, org_id: str = None) -> str:
        """
        Update a Call Pickup

        Update the designated Call Pickup.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Updating a call pickup requires a full or user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location in which this call pickup exists.
        :type location_id: str
        :param pickup_id: Update settings for a call pickup with the matching ID.
        :type pickup_id: str
        :param settings: updates
        :type settings: :class:`CallPickup`
        :param org_id: Update call pickup settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, pickup_id=pickup_id)
        body = settings.create_or_update()
        data = await self.put(url, data=body, params=params)
        return data['id']

    def available_agents_gen(self, location_id: str, call_pickup_name: str = None, name: str = None,
                         phone_number: str = None, order: str = None,
                         org_id: str = None) -> AsyncGenerator[PersonPlaceAgent, None, None]:
        """
        Get available agents from Call Pickups
        Retrieve available agents from call pickups for a given location.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving available agents from call pickups requires a full, user, or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_pickup_name: Only return available agents from call pickups with the matching name.
        :type call_pickup_name: str
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, number and extension.
            The maximum supported sort order value is 3.
        :type order: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :return: yields :class:`PersonPlaceCallPark` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableUsers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=PersonPlaceAgent, params=params, item_key='agents')

    async def available_agents(self, location_id: str, call_pickup_name: str = None, name: str = None,
                         phone_number: str = None, order: str = None,
                         org_id: str = None) -> List[PersonPlaceAgent]:
        """
        Get available agents from Call Pickups
        Retrieve available agents from call pickups for a given location.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving available agents from call pickups requires a full, user, or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_pickup_name: Only return available agents from call pickups with the matching name.
        :type call_pickup_name: str
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, number and extension.
            The maximum supported sort order value is 3.
        :type order: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :return: yields :class:`PersonPlaceCallPark` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableUsers')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=PersonPlaceAgent, params=params, item_key='agents')]


class AsAnnouncementApi:
    """
    API for call queue Announcements
    """

    def __init__(self, *, session: AsRestSession):
        self._session = session

    def _endpoint(self, location_id: str, queue_id: str, path: str = None):
        """

        :meta private:
        :param location_id:
        :param queue_id:
        :param path:
        :return:
        """
        path = path and f'/{path}' or ''
        ep = self._session.ep(path=f'telephony/config/locations/{location_id}/queues/{queue_id}/announcements{path}')
        return ep

    def list_gen(self, *, location_id: str, queue_id: str, org_id: str = None) -> AsyncGenerator[Announcement]:
        """

        :param location_id:
        :param queue_id:
        :param org_id:
        :return:
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = org_id and {'orgId': org_id} or dict()
        # noinspection PyTypeChecker
        return self._session.follow_pagination(url=url, model=Announcement, params=params)

    async def list(self, *, location_id: str, queue_id: str, org_id: str = None) -> List[Announcement]:
        """

        :param location_id:
        :param queue_id:
        :param org_id:
        :return:
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = org_id and {'orgId': org_id} or dict()
        # noinspection PyTypeChecker
        return [o async for o in self._session.follow_pagination(url=url, model=Announcement, params=params)]

    async def delete_announcement(self, *, location_id: str, queue_id: str, file_name: str, org_id: str = None):
        """

        :param location_id:
        :type location_id: str
        :param queue_id:
        :type queue_id: str
        :param file_name:
        :type file_name: str
        :param org_id:
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id, path=file_name)
        params = org_id and {'orgId': org_id} or None
        await self._session.delete(url=url, params=params)


class AsCallQueueApi:
    """
    Call Queue APÍ
    """
    forwarding: AsForwardingApi
    announcement: AsAnnouncementApi

    def __init__(self, session: AsRestSession):
        self._session = session
        self.forwarding = AsForwardingApi(session=session, feature_selector=FeatureSelector.queues)
        self.announcement = AsAnnouncementApi(session=session)

    def _endpoint(self, *, location_id: str = None, queue_id: str = None):
        """
        Helper to get URL for API endpoints

        :meta private:
        :param location_id:
        :param queue_id:
        :return:
        """
        if location_id is None:
            return self._session.ep('telephony/config/queues')
        else:
            ep = self._session.ep(f'telephony/config/locations/{location_id}/queues')
            if queue_id:
                ep = f'{ep}/{queue_id}'
            return ep

    @staticmethod
    def update_or_create(*, queue: CallQueue) -> str:
        """
        Get JSON for update or create

        :param queue:
        :return:
        :meta private:
        """
        return queue.json(
            exclude={'id': True,
                     'location_name': True,
                     'location_id': True,
                     'toll_free_number': True,
                     'language': True,
                     'agents':
                         {'__all__':
                              {'first_name': True,
                               'last_name': True,
                               'user_type': True,
                               'extension': True,
                               'phone_number': True}},
                     'alternate_number_settings':
                         {'alternate_numbers':
                              {'__all__':
                                   {'toll_free_number': True}}},
                     'queue_settings':
                         {'overflow':
                              {'is_transfer_number_set': True}}})

    def list_gen(self, *, location_id: str = None, name: str = None,
             org_id: str = None, **params) -> AsyncGenerator[CallQueue, None, None]:
        """
        Read the List of Call Queues
        List all Call Queues for the organization.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Only return call queues with matching location ID.
        :type location_id: str
        :param name: Only return call queues with the matching name.
        :type name: str
        :param org_id: List call queues for this organization
        :type org_id: str
        :param params: dict of additional parameters passed directly to endpoint
        :type params: dict
        :return: yields :class:`CallQueue` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self._session.follow_pagination(url=url, model=CallQueue, params=params)

    async def list(self, *, location_id: str = None, name: str = None,
             org_id: str = None, **params) -> List[CallQueue]:
        """
        Read the List of Call Queues
        List all Call Queues for the organization.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Only return call queues with matching location ID.
        :type location_id: str
        :param name: Only return call queues with the matching name.
        :type name: str
        :param org_id: List call queues for this organization
        :type org_id: str
        :param params: dict of additional parameters passed directly to endpoint
        :type params: dict
        :return: yields :class:`CallQueue` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return [o async for o in self._session.follow_pagination(url=url, model=CallQueue, params=params)]

    async def by_name(self, *, name: str, location_id: str = None, org_id: str = None) -> Optional[CallQueue]:
        """
        Get queue info by name

        :param location_id:
        :param name:
        :param org_id:
        :return:
        """
        return next((cq for cq in await self.list(location_id=location_id, org_id=org_id, name=name)
                     if cq.name == name), None)

    async def create(self, *, location_id: str, settings: CallQueue, org_id: str = None) -> str:
        """
        Create a Call Queue
        Create new Call Queues for the given location.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Creating a call queue requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Create the call queue for this location.
        :type location_id: str
        :param settings: parameters for queue creation.
        :type settings: :class:`CallQueue`
        :param org_id: Create the call queue for this organization.
        :type org_id: str
        :return: queue id
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or {}
        cq_data = settings.create_or_update()
        url = self._endpoint(location_id=location_id)
        data = await self._session.rest_post(url, data=cq_data, params=params)
        return data['id']

    async def delete_queue(self, *, location_id: str, queue_id: str, org_id: str = None):
        """
        Delete a Call Queue
        Delete the designated Call Queue.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Deleting a call queue requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a call queue.
        :type location_id: str
        :param queue_id: Delete the call queue with the matching ID.
        :type queue_id: str
        :param org_id: Delete the call queue from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = org_id and {'orgId': org_id} or None
        await self._session.rest_delete(url=url, params=params)

    async def details(self, *, location_id: str, queue_id: str, org_id: str = None) -> CallQueue:
        """
        Get Details for a Call Queue
        Retrieve Call Queue details.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned anvinternal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Retrieving call queue details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str
        :return: call queue details
        :rtype: :class:`CallQueue`
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = {'orgId': org_id} if org_id is not None else {}
        data = await self._session.rest_get(url, params=params)
        result = CallQueue.parse_obj(data)
        # noinspection PyTypeChecker
        return result

    async def update(self, *, location_id: str, queue_id: str, update: CallQueue, org_id: str = None):
        """
        Update a Call Queue

        Update the designated Call Queue.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Updating a call queue requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        Examples:

        .. code-block::

            api = WebexSimpleApi()

            # shortcut
            cq = api.telephony.callqueue

            # disable a call queue
            update = CallQueue(enabled=False)
            cq.update(location_id=...,
                      queue_id=...,
                      update=update)

            # set the call routing policy to SIMULTANEOUS
            update = CallQueue(call_policies=CallPolicies(policy=Policy.simultaneous))
            cq.update(location_id=...,
                      queue_id=...,
                      update=update)
            # don't bounce calls after the set number of rings.
            update = CallQueue(
                call_policies=CallPolicies(
                    call_bounce=CallBounce(
                        enabled=False)))
            cq.update(location_id=...,
                      queue_id=...,
                      update=update)

        Alternatively you can also read call queue details, update them in place and then call update().

        .. code-block::

            details = cq.details(location_id=...,
                                 queue_id=...)
            details.call_policies.call_bounce.agent_unavailable_enabled=False
            details.call_policies.call_bounce.on_hold_enabled=False
            cq.update(location_id=...,
                      queue_id=...,
                      update=details)

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param update: updates
        :type update: :class:`CallQueue`
        :param org_id: Update call queue settings from this organization.
        """
        params = org_id and {'orgId': org_id} or None
        cq_data = update.create_or_update()
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        await self._session.rest_put(url=url, data=cq_data, params=params)


class AsCallparkExtensionApi(AsApiChild, base='telephony/config/huntGroups'):
    """
    Call Park Extension API
    """

    def _endpoint(self, *, location_id: str = None, cpe_id: str = None) -> str:
        """
        call park extension specific feature endpoint like
        /v1/telephony/config/locations/{locationId}/callParkExtensions/{cpe_id}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param cpe_id: call park extension id
        :type cpe_id: str
        :return: full endpoint
        :rtype: str
        """
        if location_id is None:
            return self.session.ep('telephony/config/callParkExtensions')
        else:
            ep = self.session.ep(f'telephony/config/locations/{location_id}/callParkExtensions')
            if cpe_id:
                ep = f'{ep}/{cpe_id}'
            return ep

    def list_gen(self, org_id: str = None, extension: str = None, name: str = None, location_id: str = None,
             location_name: str = None,
             order: str = None, **params) -> AsyncGenerator[CallParkExtension, None, None]:
        """
        Read the List of Call Park Extensions

        List all Call Park Extensions for the organization.

        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call
        Park service for holding parked calls.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List call park extensions for this organization.
        :type org_id: str
        :param extension: Only return call park extensions with the matching extension.
        :type extension: str
        :param name: Only return call park extensions with the matching name.
        :type name: str
        :param location_id: Only return call park extensions with matching location ID.
        :type location_id: str
        :param location_name: Only return call park extensions with matching location name.
        :type location_name: str
        :param order: Order the available agents according to the designated fields. Available sort fields: groupName,
            callParkExtension, callParkExtensionName, callParkExtensionExternalId.
        :type order: str
        :param params: additional parameters
        :return: yields :class:`wxc_sdk.common.CallParkExtension` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CallParkExtension, params=params)

    async def list(self, org_id: str = None, extension: str = None, name: str = None, location_id: str = None,
             location_name: str = None,
             order: str = None, **params) -> List[CallParkExtension]:
        """
        Read the List of Call Park Extensions

        List all Call Park Extensions for the organization.

        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call
        Park service for holding parked calls.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List call park extensions for this organization.
        :type org_id: str
        :param extension: Only return call park extensions with the matching extension.
        :type extension: str
        :param name: Only return call park extensions with the matching name.
        :type name: str
        :param location_id: Only return call park extensions with matching location ID.
        :type location_id: str
        :param location_name: Only return call park extensions with matching location name.
        :type location_name: str
        :param order: Order the available agents according to the designated fields. Available sort fields: groupName,
            callParkExtension, callParkExtensionName, callParkExtensionExternalId.
        :type order: str
        :param params: additional parameters
        :return: yields :class:`wxc_sdk.common.CallParkExtension` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=CallParkExtension, params=params)]

    async def details(self, location_id: str, cpe_id: str, org_id: str = None) -> CallParkExtension:
        """
        Get Details for a Call Park Extension

        Retrieve Call Park Extension details.

        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call
        Park service for holding parked calls.

        Retrieving call park extension details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve details for a call park extension in this location.
        :type location_id: str
        :param cpe_id: Retrieve details for a call park extension with the matching ID.
        :type cpe_id: str
        :param org_id: Retrieve call park extension details from this organization
        :type org_id: str
        :return: call park extension details
        :rtype: :class:`wxc_sdk.common.CallParkExtension` instance (only name and extension are set)
        """
        url = self._endpoint(location_id=location_id, cpe_id=cpe_id)
        params = org_id and {'orgId': org_id} or {}
        data = await self.get(url, params=params)
        return CallParkExtension.parse_obj(data)


class AsCallsApi(AsApiChild, base='telephony/calls'):

    async def dial(self, destination: str) -> DialResponse:
        """
        Initiate an outbound call to a specified destination. This is also commonly referred to as Click to Call or
        Click to Dial. Alerts on all the devices belonging to the user. When the user answers on one of these alerting
        devices, an outbound call is placed from that device to the destination.

        :param destination: The destination to be dialed. The destination can be digits or a URI. Some examples for
            destination include: 1234, 2223334444, +12223334444, \*73, tel:+12223334444, user@company.domain,
            sip:user@company.domain
        :type destination: str
        :return: Call id and call session id
        """
        ep = self.ep('dial')
        data = await self.post(ep, json={'destination': destination})
        return DialResponse.parse_obj(data)

    async def answer(self, call_id: str):
        """
        Answer an incoming call on the user's primary device.

        :param call_id: The call identifier of the call to be answered.
        :type call_id: str
        """
        ep = self.ep('answer')
        await self.post(ep, json={'callId': call_id})

    async def reject(self, call_id: str, action: RejectAction = None):
        """
        Reject an unanswered incoming call.

        :param call_id: The call identifier of the call to be rejected.
        :type call_id: str
        :param action: The rejection action to apply to the call. The busy action is applied if no specific action is
            provided.
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('reject')
        await self.post(ep, json=data)

    async def hangup(self, call_id: str):
        """
        Hangup a call. If used on an unanswered incoming call, the call is rejected and sent to busy.

        :param call_id: The call identifier of the call to hangup.
        :type call_id: str
        """
        ep = self.ep('hangup')
        await self.post(ep, json={'callId': call_id})

    async def hold(self, call_id: str):
        """
        Hold a connected call.

        :param call_id: The call identifier of the call to hold.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('hold')
        await self.post(ep, json=data)

    async def resume(self, call_id: str):
        """
        Resume a held call.

        :param call_id: The call identifier of the call to resume.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('resume')
        await self.post(ep, json=data)

    async def divert(self, call_id: str, destination: str = None, to_voicemail: bool = None):
        """
        Divert a call to a destination or a user's voicemail. This is also commonly referred to as Blind Transfer

        :param call_id: The call identifier of the call to divert.
        :type call_id: str
        :param destination: The destination to divert the call to. If toVoicemail is false, destination is required.
            The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444,
            +12223334444, \*73, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type destination: str
        :param to_voicemail: If set to true, the call is diverted to voicemail. If no destination is specified, the
            call is diverted to the user's own voicemail. If a destination is specified, the call is diverted to the
            specified user's voicemail.
        :type to_voicemail: bool
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('divert')
        await self.post(ep, json=data)

    async def transfer(self, call_id1: str = None, call_id2: str = None, destination: str = None):
        """
        Transfer two calls together. Unanswered incoming calls cannot be transferred but can be diverted using the
        divert API. If the user has only two calls and wants to transfer them together, the callId1 and callId2
        parameters are optional and when not provided the calls are automatically selected and transferred. If the
        user has more than two calls and wants to transfer two of them together, the callId1 and callId2 parameters
        are mandatory to specify which calls are being transferred. These are also commonly referred to as Attended
        Transfer, Consultative Transfer, or Supervised Transfer and will return a 204 response. If the user wants to
        transfer one call to a new destination but only when the destination responds, the callId1 and destination
        parameters are mandatory to specify the call being transferred and the destination. This is referred to as a
        Mute Transfer and is similar to the divert API with the difference of waiting for the destination to respond
        prior to transferring the call. If the destination does not respond, the call is not transferred. This will
        return a 201 response.

        :param call_id1: The call identifier of the first call to transfer. This parameter is mandatory if either
            call_id2 or destination is provided.
        :type call_id1: str
        :param call_id2: The call identifier of the first call to transfer. This parameter is mandatory if either
            callId2 or destination is provided.
        :type call_id1: str
        :param destination: The destination to be transferred to. The destination can be digits or a URI. Some
            examples for destination include: 1234, 2223334444,
            +12223334444, \*73, tel:+12223334444, user@company.domain, sip:user@company.domain.
            This parameter is mandatory if call_id1 is provided and call_id2 is not provided.
        :type destination: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('transfer')
        await self.post(ep, json=data)

    async def park(self, call_id: str, destination: str = None, is_group_park: bool = None) -> ParkedAgainst:
        """
        Park a connected call. The number field in the response can be used as the destination for the retrieve
        command to retrieve the parked call.

        :param call_id: The call identifier of the call to park.
        :type call_id: str
        :param destination: Identifies where the call is to be parked. If not provided, the call is parked against the
            parking user.
            The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444,
            +12223334444, \*73, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type destination: str
        :param is_group_park: If set to true, the call is parked against an automatically selected member of the
            user's call park group and the destination parameter is ignored.
        :type is_group_park: bool
        :return: The details of where the call has been parked.
        :rtype: :class:`ParkedAgainst`
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('park')
        data = await self.post(ep, json=data)
        return ParkedAgainst.parse_obj(data)

    async def retrieve(self, destination: str) -> CallInfo:
        """
        :param destination: Identifies where the call is parked. The number field from the park command response can
            be used as the destination for the retrieve command. If not provided, the call parked against the
            retrieving user is retrieved. The destination can be digits or a URI. Some examples for destination
            include: 1234, 2223334444, +12223334444, \*73, tel:+12223334444, user@company.domain,
            sip:user@company.domain
        :return: call id and call session id of retreived call
        :rtype: :class:`CallInfo`
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('retrieve')
        data = await self.post(ep, json=data)
        return CallInfo.parse_obj(data)

    async def start_recording(self, call_id: str):
        """
        Start recording a call. Use of this API is only valid when the user's call recording mode is set to "On Demand".

        :param call_id: The call identifier of the call to start recording.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('startRecording')
        await self.post(ep, json=data)

    async def stop_recording(self, call_id: str):
        """
        Stop recording a call. Use of this API is only valid when a call is being recorded and the user's call
        recording mode is set to "On Demand".

        :param call_id: The call identifier of the call to stop recording.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('stopRecording')
        await self.post(ep, json=data)

    async def pause_recording(self, call_id: str):
        """
        Pause recording on a call. Use of this API is only valid when a call is being recorded and the user's call
        recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param call_id: The call identifier of the call to pause recording.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('pauseRecording')
        await self.post(ep, json=data)

    async def resume_recording(self, call_id: str):
        """
        Resume recording a call. Use of this API is only valid when a call's recording is paused and the user's call
        recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param call_id: The call identifier of the call to resume recording.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('resumeRecording')
        await self.post(ep, json=data)

    async def transmit_dtmf(self, call_id: str, dtmf: str):
        """
        Transmit DTMF digits to a call.

        :param call_id: The call identifier of the call to hold.
        :type call_id: str
        :param dtmf: The DTMF digits to transmit. Each digit must be part of the following set: [0, 1, 2, 3, 4, 5, 6,
            7, 8, 9, \*, #, A, B, C, D]. A comma "," may be included to indicate a pause between digits. For the value
            “1,234”, the DTMF 1 digit is initially sent. After a pause, the DTMF 2, 3, and 4 digits are sent
            successively.
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('transmitDtmf')
        await self.post(ep, json=data)

    async def push(self, call_id: str):
        """
        Pushes a call from the assistant to the executive the call is associated with. Use of this API is only valid
        when the assistant’s call is associated with an executive.

        :param call_id: The call identifier of the call to push.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('push')
        await self.post(ep, json=data)

    async def pickup(self, target: str) -> CallInfo:
        """
        Picks up an incoming call to another user. A new call is initiated to perform the pickup in a similar manner
        to the dial command. When target is not present, the API pickups up a call from the user’s call pickup group.
        When target is present, the API pickups an incoming call from the specified target user.

        :param target: Identifies the user to pickup an incoming call from. If not provided, an incoming call to the
            user’s call pickup group is picked up. The target can be digits or a URI. Some examples for target
            include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type target: str
        :return: call info of picked up call
        :rtype: :class:`CallInfo`
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('pickup')
        data = await self.post(ep, json=data)
        return CallInfo.parse_obj(data)

    async def barge_in(self, target: str):
        """
        Barge-in on another user’s answered call. A new call is initiated to perform the barge-in in a similar manner
        to the dial command.

        :param target: Identifies the user to barge-in on. The target can be digits or a URI. Some examples for target
            include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type target: str
        :return: call info of picked up call
        :rtype: :class:`CallInfo`
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('bargeIn')
        data = await self.post(ep, json=data)
        return CallInfo.parse_obj(data)

    def list_calls_gen(self) -> AsyncGenerator[TelephonyCall, None, None]:
        """
        Get the list of details for all active calls associated with the user.

        :return: yield :class:`TelephonyCall`
        """
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=TelephonyCall)

    async def list_calls(self) -> List[TelephonyCall]:
        """
        Get the list of details for all active calls associated with the user.

        :return: yield :class:`TelephonyCall`
        """
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=TelephonyCall)]

    async def call_details(self, call_id: str) -> TelephonyCall:
        """
        Get the details of the specified active call for the user.

        :param call_id: The call identifier of the call.
        :type call_id: str
        :return: call details
        :rtype: :class:`TelephonyCall`
        """
        ep = self.ep(call_id)
        data = await self.get(ep)
        return TelephonyCall.parse_obj(data)

    def call_history_gen(self, history_type: Union[str, HistoryType] = None) -> AsyncGenerator[CallHistoryRecord, None, None]:
        """
        List Call History
        Get the list of call history records for the user. A maximum of 20 call history records per type (placed,
        missed, received) are returned.

        :param history_type: The type of call history records to retrieve. If not specified, then all call history
            records are retrieved.
            Possible values: placed, missed, received
        :type history_type: HistoryType or str
        :return: yields :class:`CallHistoryRecord` objects
        """
        history_type = history_type and HistoryType.history_type_or_str(history_type)
        params = history_type and {'type': history_type.value} or None
        url = self.ep('history')
        return self.session.follow_pagination(url=url, model=CallHistoryRecord, params=params)

    async def call_history(self, history_type: Union[str, HistoryType] = None) -> List[CallHistoryRecord]:
        """
        List Call History
        Get the list of call history records for the user. A maximum of 20 call history records per type (placed,
        missed, received) are returned.

        :param history_type: The type of call history records to retrieve. If not specified, then all call history
            records are retrieved.
            Possible values: placed, missed, received
        :type history_type: HistoryType or str
        :return: yields :class:`CallHistoryRecord` objects
        """
        history_type = history_type and HistoryType.history_type_or_str(history_type)
        params = history_type and {'type': history_type.value} or None
        url = self.ep('history')
        return [o async for o in self.session.follow_pagination(url=url, model=CallHistoryRecord, params=params)]


class AsHuntGroupApi(AsApiChild, base='telephony/config/huntGroups'):
    """
    Hunt Group API
    """
    forwarding: AsForwardingApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.forwarding = AsForwardingApi(session=session, feature_selector=FeatureSelector.huntgroups)

    def _endpoint(self, *, location_id: str = None, huntgroup_id: str = None) -> str:
        """
        hunt group specific feature endpoint like /v1/telephony/config/locations/{locationId}/huntGroups/{huntGroupId}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param huntgroup_id: schedule id
        :type huntgroup_id: str
        :return: full endpoint
        :rtype: str
        """
        if location_id is None:
            return self.session.ep('telephony/config/huntGroups')
        else:
            ep = self.session.ep(f'telephony/config/locations/{location_id}/huntGroups')
            if huntgroup_id:
                ep = f'{ep}/{huntgroup_id}'
            return ep

    def list_gen(self, org_id: str = None, location_id: str = None, name: str = None,
             phone_number: str = None, **params) -> AsyncGenerator[HuntGroup, None, None]:
        """
        Read the List of Hunt Groups

        List all calling Hunt Groups for the organization.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List hunt groups for this organization.
        :param location_id: Only return hunt groups with matching location ID.
        :param name: Only return hunt groups with the matching name.
        :param phone_number: Only return hunt groups with the matching primary phone number or extension.
        :return: yields :class:`HuntGroup` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=HuntGroup, params=params)

    async def list(self, org_id: str = None, location_id: str = None, name: str = None,
             phone_number: str = None, **params) -> List[HuntGroup]:
        """
        Read the List of Hunt Groups

        List all calling Hunt Groups for the organization.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List hunt groups for this organization.
        :param location_id: Only return hunt groups with matching location ID.
        :param name: Only return hunt groups with the matching name.
        :param phone_number: Only return hunt groups with the matching primary phone number or extension.
        :return: yields :class:`HuntGroup` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=HuntGroup, params=params)]

    async def by_name(self, name: str, location_id: str = None, org_id: str = None) -> Optional[HuntGroup]:
        """
        Get hunt group info by name
        :param location_id:
        :param name:
        :param org_id:
        :return:
        """
        return next((hg for hg in await self.list(name=name, location_id=location_id, org_id=org_id)
                     if hg.name == name), None)

    async def create(self, location_id: str, settings: HuntGroup, org_id: str = None) -> str:
        """
        Create a Hunt Group

        Create new Hunt Groups for the given location.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Creating a hunt group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the hunt group for the given location.
        :type location_id: str
        :param settings: hunt group details
        :type settings: :class:`HuntGroup`
        :param org_id: Create the hunt group for this organization.
        :type org_id: str
        :return: ID of the newly created hunt group.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or {}
        settings.call_policies = settings.call_policies or HGCallPolicies().default()
        data = settings.create_or_update()
        url = self._endpoint(location_id=location_id)
        data = await self.post(url, data=data, params=params)
        return data['id']

    async def delete_huntgroup(self, location_id: str, huntgroup_id: str, org_id: str = None):
        """
        Delete a Hunt Group

        Delete the designated Hunt Group.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Deleting a hunt group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a hunt group.
        :type location_id: str
        :param huntgroup_id: Delete the hunt group with the matching ID.
        :type huntgroup_id: str
        :param org_id: Delete the hunt group with the matching ID.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, huntgroup_id=huntgroup_id)
        await self.delete(url, params=params)

    async def details(self, location_id: str, huntgroup_id: str, org_id: str = None) -> HuntGroup:
        """
        Get Details for a Hunt Group

        Retrieve Hunt Group details.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Retrieving hunt group details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a hunt group in this location.
        :type location_id: str
        :param huntgroup_id: Retrieve settings for the hunt group with this identifier.
        :type huntgroup_id: str
        :param org_id: Retrieve hunt group settings from this organization.
        :type org_id: str
        :return: hunt group details
        """
        url = self._endpoint(location_id=location_id, huntgroup_id=huntgroup_id)
        params = org_id and {'orgId': org_id} or {}
        data = await self.get(url, params=params)
        result = HuntGroup.parse_obj(data)
        return result

    async def update(self, location_id: str, huntgroup_id: str, update: HuntGroup,
               org_id: str = None):
        """
        Update a Hunt Group

        Update the designated Hunt Group.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Updating a hunt group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Update the hunt group for this location.
        :type location_id: str
        :param huntgroup_id: Update setting for the hunt group with the matching ID.
        :type huntgroup_id: str
        :param update: hunt group settings
        :type update: :class:`HuntGroup`
        :param org_id: Update hunt group settings from this organization.
        """
        params = org_id and {'orgId': org_id} or None
        data = update.create_or_update()
        url = self._endpoint(location_id=location_id, huntgroup_id=huntgroup_id)
        await self.put(url, data=data, params=params)


class AsOrganisationVoicemailSettingsAPI(AsApiChild, base='telephony/config/voicemail/settings'):
    """
    API for Organisation voicemail settings
    """

    async def read(self, *, org_id: str = None) -> OrganisationVoicemailSettings:
        """
        Get Voicemail Settings

        Retrieve the organization's voicemail settings.

        Organizational voicemail settings determines what voicemail features a person can configure and automatic
        message expiration.

        Retrieving organization's voicemail settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param org_id: Retrieve voicemail settings for this organization.
        :type org_id: str
        :return: VM settings
        :rtype: OrganisationVoicemailSettings
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        return OrganisationVoicemailSettings.parse_obj(await self.get(url, params=params))

    async def update(self, *, settings: OrganisationVoicemailSettings, org_id: str = None):
        """
        Update the organization's voicemail settings.

        Organizational voicemail settings determines what voicemail features a person can configure and automatic
        message expiration.

        Updating organization's voicemail settings requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param settings: new settings
        :type settings: OrganisationVoicemailSettings
        :param org_id: Update voicemail settings for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = settings.json()
        await self.put(url, data=data, params=params)


class AsPagingApi(AsApiChild, base='telephony/config'):

    def _endpoint(self, *, location_id: str = None, paging_id: str = None) -> str:
        """
        endpoint for paging group operation

        :meta private:
        :param location_id:
        :type location_id: str
        :param paging_id:
        :type paging_id: str
        """
        if location_id is None:
            return super().ep('paging')
        paging_id = paging_id and f'/{paging_id}' or ''
        return super().ep(f'locations/{location_id}/paging{paging_id}')

    def list_gen(self, *, location_id: str = None, name: str = None, phone_number: str = None,
             org_id: str = None, **params) -> AsyncGenerator[Paging, None, None]:
        """
        Read the List of Paging Groups
        List all Paging Groups for the organization.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return only paging groups with matching location ID. Default is all locations
        :type location_id: str
        :param name: Return only paging groups with the matching name.
        :type name: str
        :param phone_number: Return only paging groups with matching primary phone number or extension.
        :type phone_number: str
        :param org_id: List paging groups for this organization.
        :type org_id: str
        :return: generator of class:`Paging` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Paging, params=params, item_key='locationPaging')
        pass

    async def list(self, *, location_id: str = None, name: str = None, phone_number: str = None,
             org_id: str = None, **params) -> List[Paging]:
        """
        Read the List of Paging Groups
        List all Paging Groups for the organization.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return only paging groups with matching location ID. Default is all locations
        :type location_id: str
        :param name: Return only paging groups with the matching name.
        :type name: str
        :param phone_number: Return only paging groups with matching primary phone number or extension.
        :type phone_number: str
        :param org_id: List paging groups for this organization.
        :type org_id: str
        :return: generator of class:`Paging` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=Paging, params=params, item_key='locationPaging')]
        pass

    async def create(self, *, location_id: str, settings: Paging, org_id: str = None) -> str:
        """
        Create a new Paging Group
        Create a new Paging Group for the given location.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Creating a paging group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the paging group for this location.
        :type location_id: str
        :param settings: new paging group
        :type settings: Paging
        :param org_id: Create the paging group for this organization.
        :type org_id: str
        :return: ID of the newly created paging group.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        if settings.originators and settings.originator_caller_id_enabled is None:
            raise TypeError('originator_caller_id_enabled required if originators are provided')
        url = self._endpoint(location_id=location_id)
        data = settings.create_or_update()
        data = await self.post(url, data=data, params=params)
        return data['id']

    async def delete_paging(self, *, location_id: str, paging_id: str, org_id: str = None):
        """
        Delete a Paging Group
        Delete the designated Paging Group.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Deleting a paging group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a paging group.
        :type location_id: str
        :param paging_id: Delete the paging group with the matching ID.
        :param org_id: Delete the paging group from this organization.
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, paging_id=paging_id)
        await self.delete(url, params=params)

    async def details(self, *, location_id: str, paging_id: str, org_id: str = None) -> Paging:
        """
        Get Details for a Paging Group
        Retrieve Paging Group details.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Retrieving paging group details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.
        :param location_id: Retrieve settings for a paging group in this location.
        :param paging_id: Retrieve settings for the paging group with this identifier.
        :param org_id: Retrieve paging group settings from this organization.
        :return: :class:`Paging` object
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, paging_id=paging_id)
        return Paging.parse_obj(await self.get(url, params=params))

    async def update(self, *, location_id: str, update: Paging, paging_id: str, org_id: str = None):
        """
        Update the designated Paging Group.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Updating a paging group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Update settings for a paging group in this location.
        :type location_id: str
        :param update: update parameters
        :type update: Paging
        :param paging_id: Update settings for the paging group with this identifier.
        :type paging_id: str
        :param org_id: Update paging group settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, paging_id=paging_id)
        data = update.create_or_update()
        await self.put(url, data=data, params=params)


class AsDialPlanApi(AsApiChild, base='telephony/config/premisePstn/dialPlans'):

    def list_gen(self, *, dial_plan_name: str = None, route_group_name: str = None, trunk_name: str = None,
             order: str = None, org_id: str = None, **params) -> AsyncGenerator[DialPlan, None, None]:
        """
        List all Dial Plans for the organization.

        Dial plans route calls to on-premises destinations by use of the trunks or route groups with which the dial
        plan is associated. Multiple dial patterns can be defined as part of your dial plan. Dial plans are configured
        globally for an enterprise and apply to all users, regardless of location.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_name: Return the list of dial plans matching the dial plan name.
        :type dial_plan_name: str
        :param route_group_name: Return the list of dial plans matching the route group name.
        :type route_group_name: str
        :param trunk_name: Return the list of dial plans matching the trunk name.
        :type trunk_name: str
        :param order: Order the dial plans according to the designated fields. Available sort fields: name, routeName,
            routeType. Sort order is ascending by default
        :type order: str
        :param org_id: List dial plans for this organization.
        :type org_id: str
        :return:
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i and v is not None and p != 'params')
        url = self.ep()
        return self.session.follow_pagination(url=url, model=DialPlan, params=params, item_key='dialPlans')

    async def list(self, *, dial_plan_name: str = None, route_group_name: str = None, trunk_name: str = None,
             order: str = None, org_id: str = None, **params) -> List[DialPlan]:
        """
        List all Dial Plans for the organization.

        Dial plans route calls to on-premises destinations by use of the trunks or route groups with which the dial
        plan is associated. Multiple dial patterns can be defined as part of your dial plan. Dial plans are configured
        globally for an enterprise and apply to all users, regardless of location.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_name: Return the list of dial plans matching the dial plan name.
        :type dial_plan_name: str
        :param route_group_name: Return the list of dial plans matching the route group name.
        :type route_group_name: str
        :param trunk_name: Return the list of dial plans matching the trunk name.
        :type trunk_name: str
        :param order: Order the dial plans according to the designated fields. Available sort fields: name, routeName,
            routeType. Sort order is ascending by default
        :type order: str
        :param org_id: List dial plans for this organization.
        :type org_id: str
        :return:
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i and v is not None and p != 'params')
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=DialPlan, params=params, item_key='dialPlans')]

    async def create(self, *, name: str, route_id: str, route_type: RouteType, dial_patterns: List[str] = None,
               org_id: str = None) -> CreateResponse:
        """
        Create a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Creating a dial plan requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param name: A unique name for the dial plan.
        :type name: str
        :param route_id: ID of route type associated with the dial plan.
        :type route_id: str
        :param route_type: Route Type associated with the dial plan.
        :type route_type: :class:`wxc_sdk.common.RouteType`
        :param dial_patterns: An Array of dial patterns
        :type dial_patterns: list[str]
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :return: result of dial plan creation
        :rtype: :class:`CreateResponse`
        """
        url = self.ep()
        params = org_id and {'orgId': org_id} or None
        body = {
            'name': name,
            'routeId': route_id,
            'routeType': route_type.value if isinstance(route_type, RouteType) else route_type,
            'dialPatterns': dial_patterns or []
        }
        data = await self.post(url=url, params=params, json=body)
        return CreateResponse.parse_obj(data)

    async def details(self, *, dial_plan_id: str, org_id: str = None) -> DialPlan:
        """
        Get a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Retrieving a dial plan requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_id: Id of the dial plan.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :return: dial plan details
        :rtype: :class:`DialPlan`
        """
        url = self.ep(dial_plan_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url=url, params=params)
        return DialPlan.parse_obj(data)

    async def update(self, *, update: DialPlan, org_id: str = None):
        """
        Modify a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Modifying a dial plan requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param update: DialPlan objects with updated settings. Only name, route_id and route_type are considered. All
            three need to be set
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        url = self.ep(update.dial_plan_id)
        params = org_id and {'orgId': org_id} or None
        body = update.json(include={'name', 'route_id', 'route_type'})
        await self.put(url=url, params=params, data=body)

    async def delete_dial_plan(self, *, dial_plan_id: str, org_id: str = None):
        """
        Delete a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Deleting a dial plan requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param dial_plan_id: Id of the dial plan.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        url = self.ep(dial_plan_id)
        params = org_id and {'orgId': org_id} or None
        await self.delete(url=url, params=params)

    def patterns_gen(self, *, dial_plan_id: str, org_id: str = None,
                 dial_pattern: str = None, **params) -> AsyncGenerator[str, None, None]:
        """
        List all Dial Patterns for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_id: Id of the dial plan.
        :type dial_plan_id: str
        :param org_id: List dial patterns associated with a dial plan.
        :type org_id: str
        :param dial_pattern: An enterprise dial pattern is represented by a sequence of digits (1-9), followed by
            optional wildcard characters. Valid wildcard characters are ! (matches any sequence of digits) and
            X (matches a single digit, 0-9).
            The ! wildcard can only occur once at the end and only in an E.164 pattern
        :return: list of patterns
        :rtype: list[str]
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i > 1 and v is not None and p != 'params')
        url = self.ep(f'{dial_plan_id}/dialPatterns')

        return self.session.follow_pagination(url=url, params=params, item_key='dialPatterns')

    async def patterns(self, *, dial_plan_id: str, org_id: str = None,
                 dial_pattern: str = None, **params) -> List[str]:
        """
        List all Dial Patterns for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_id: Id of the dial plan.
        :type dial_plan_id: str
        :param org_id: List dial patterns associated with a dial plan.
        :type org_id: str
        :param dial_pattern: An enterprise dial pattern is represented by a sequence of digits (1-9), followed by
            optional wildcard characters. Valid wildcard characters are ! (matches any sequence of digits) and
            X (matches a single digit, 0-9).
            The ! wildcard can only occur once at the end and only in an E.164 pattern
        :return: list of patterns
        :rtype: list[str]
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i > 1 and v is not None and p != 'params')
        url = self.ep(f'{dial_plan_id}/dialPatterns')

        return [o async for o in self.session.follow_pagination(url=url, params=params, item_key='dialPatterns')]

    async def modify_patterns(self, *, dial_plan_id: str, dial_patterns: List[PatternAndAction], org_id: str = None):
        """
        Modify dial patterns for the Dial Plan.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Modifying a dial pattern requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param dial_plan_id: Id of the dial plan being modified.
        :type dial_plan_id: str
        :param dial_patterns: Array of dial patterns to add or delete. Dial Pattern that is not present in the
            request is not modified.
        :type dial_patterns: :class:`PatternAndAction`
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        url = self.ep(f'{dial_plan_id}/dialPatterns')
        params = org_id and {'orgId': org_id} or None

        class Body(ApiModel):
            dial_patterns: list[PatternAndAction]

        body = Body(dial_patterns=dial_patterns).json()
        await self.put(url=url, params=params, data=body)

    async def delete_all_patterns(self, *, dial_plan_id: str, org_id: str = None):
        """
        Delete all dial patterns from the Dial Plan.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Deleting dial pattern requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param dial_plan_id: Id of the dial plan being modified.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        url = self.ep(f'{dial_plan_id}/dialPatterns')
        params = org_id and {'orgId': org_id} or None
        body = {'deleteAllDialPatterns': True}
        await self.put(url=url, params=params, json=body)


class AsRouteGroupApi(AsApiChild, base='telephony/config/premisePstn/routeGroups'):
    """
    API for everything route groups
    """

    def list_gen(self, *, name: str = None, order: str = None,
             org_id: str = None, **params) -> AsyncGenerator[RouteGroup, None, None]:
        """
        List all Route Groups for an organization. A Route Group is a group of trunks that allows further scale and
        redundancy with the connection to the premises.

        Retrieving this route group list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of route groups matching the route group name.
        :type name: st
        :param order: Order the route groups according to designated fields. Available sort orders: asc, desc.
        :type order: str
        :param org_id: List route groups for this organization.
        :type org_id: str
        :return: generator of :class:`RouteGroup` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params, model=RouteGroup)

    async def list(self, *, name: str = None, order: str = None,
             org_id: str = None, **params) -> List[RouteGroup]:
        """
        List all Route Groups for an organization. A Route Group is a group of trunks that allows further scale and
        redundancy with the connection to the premises.

        Retrieving this route group list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of route groups matching the route group name.
        :type name: st
        :param order: Order the route groups according to designated fields. Available sort orders: asc, desc.
        :type order: str
        :param org_id: List route groups for this organization.
        :type org_id: str
        :return: generator of :class:`RouteGroup` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, params=params, model=RouteGroup)]

    async def create(self, *, route_group: RouteGroup, org_id: str = None) -> str:
        """
        Creates a Route Group for the organization.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Creating a Route Group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param route_group: settings for new route group. name and local_gateways need to be set. For each LGW
            id and priority need to be set.
            Example:

            .. code-block:: python

                rg = RouteGroup(name=rg_name,
                        local_gateways=[RGTrunk(trunk_id=trunk.trunk_id,
                                                priority=1)])
                rg_id = api.telephony.prem_pstn.route_group.create(route_group=rg)
        :type route_group: :class:`RouteGroup`
        :param org_id:
        :type org_id: str
        :return: id of new route group
        :rtype: str
        """
        # TODO: doc defect. wrong URL at https://developer.webex.com/docs/api/v1/webex-calling-organization-settings
        #  /create-route-group-for-a-organization
        params = org_id and {'orgId': org_id} or None
        body = route_group.json(include={'name': True,
                                         'local_gateways': {'__all__': {'trunk_id', 'priority'}}})
        url = self.ep()
        data = await self.post(url=url, params=params, data=body)
        return data['id']

    async def details(self, *, rg_id: str, org_id: str = None) -> RouteGroup:
        """
        Reads a Route Group for the organization based on id.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Reading a Route Group requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route Group for which details are being requested.
        :type rg_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :return: route group details
        :rtype: :class:`RouteGroup`
        """
        # TODO: wrong data structure at
        #  https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-a-route-group-for-a
        #  -organization
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rg_id)
        data = await self.get(url=url, params=params)
        return RouteGroup.parse_obj(data)

    async def update(self, *, rg_id: str, update: RouteGroup, org_id: str = None):
        """
        Modifies an existing Route Group for an organization based on id.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Modifying a Route Group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rg_id: route group to be modified
        :type rg_id: str
        :param update: new settings
        :type update: :class:`RouteGroup`
        :param org_id: Organization of the Route Group.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        body = update.json(include={'name': True,
                                    'local_gateways': {'__all__': {'trunk_id', 'priority'}}})
        url = self.ep(rg_id)
        data = await self.post(url=url, params=params, data=body)
        await self.put(url=url, params=params, data=data)

    async def delete_route_group(self, *, rg_id: str, org_id: str = None):
        """
        Remove a Route Group from an Organization based on id.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Removing a Route Group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rg_id: Route Group to be deleted
        :type rg_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        """
        # TODO: doc defect. wrong URL
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rg_id)
        await self.delete(url=url, params=params)

    async def usage(self, *, rg_id: str, org_id: str = None) -> RouteGroupUsage:
        """
        List the number of "Call to" on-premises Extensions, Dial Plans, PSTN Connections, and Route Lists used by a
        specific Route Group. Users within Call to Extension locations are registered to a PBX which allows you to
        route unknown extensions (calling number length of 2-6 digits) to the PBX using an existing Trunk or Route
        Group. PSTN Connections may be cisco PSTN, cloud-connected PSTN, or premises-based PSTN (local gateway).
        Dial Plans allow you to route calls to on-premises extensions via your trunk or route group. Route Lists are
        a list of numbers that can be reached via a route group. It can be used to provide cloud PSTN connectivity to
        Webex Calling Dedicated Instance.

        Retrieving usage information requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :type rg_id: str
        :param org_id: Organization associated with specific route group
        :type org_id: str
        :return: usage information
        :rtype: :class:`RouteGroupUsage`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{rg_id}/usage')
        data = await self.get(url=url, params=params)
        return RouteGroupUsage.parse_obj(data)

    def usage_call_to_extension_gen(self, rg_id: str, org_id: str = None, **params) -> AsyncGenerator[IdAndName, None, None]:
        """
        List "Call to" on-premises Extension Locations for a specific route group. Users within these locations are
        registered to a PBX which allows you to route unknown extensions (calling number length of 2-6 digits) to
        the PBX using an existing trunk or route group.

        Retrieving this location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageCallToExtension')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    async def usage_call_to_extension(self, rg_id: str, org_id: str = None, **params) -> List[IdAndName]:
        """
        List "Call to" on-premises Extension Locations for a specific route group. Users within these locations are
        registered to a PBX which allows you to route unknown extensions (calling number length of 2-6 digits) to
        the PBX using an existing trunk or route group.

        Retrieving this location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageCallToExtension')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params)]

    def usage_dial_plan_gen(self, rg_id: str, org_id: str = None, **params) -> AsyncGenerator[IdAndName, None, None]:
        """
        List Dial Plan Locations for a specific route group.

        Dial Plans allow you to route calls to on-premises destinations by use of trunks or route groups. They are
        configured globally for an enterprise and apply to all users, regardless of location. A Dial Plan also
        specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Retrieving this location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageDialPlan')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    async def usage_dial_plan(self, rg_id: str, org_id: str = None, **params) -> List[IdAndName]:
        """
        List Dial Plan Locations for a specific route group.

        Dial Plans allow you to route calls to on-premises destinations by use of trunks or route groups. They are
        configured globally for an enterprise and apply to all users, regardless of location. A Dial Plan also
        specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Retrieving this location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageDialPlan')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params)]

    def usage_location_pstn_gen(self, rg_id: str, org_id: str = None, **params) -> AsyncGenerator[IdAndName, None, None]:
        """
        List PSTN Connection Locations for a specific route group. This solution lets you configure users to use Cloud
        PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this Location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usagePstnConnection')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    async def usage_location_pstn(self, rg_id: str, org_id: str = None, **params) -> List[IdAndName]:
        """
        List PSTN Connection Locations for a specific route group. This solution lets you configure users to use Cloud
        PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this Location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usagePstnConnection')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params)]

    def usage_route_lists_gen(self, rg_id: str, org_id: str = None, **params) -> AsyncGenerator[UsageRouteLists, None, None]:
        """
        List Route Lists for a specific route group. Route Lists are a list of numbers that can be reached via a
        Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.

        Retrieving this list of Route Lists requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageRouteList')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=UsageRouteLists, params=params)

    async def usage_route_lists(self, rg_id: str, org_id: str = None, **params) -> List[UsageRouteLists]:
        """
        List Route Lists for a specific route group. Route Lists are a list of numbers that can be reached via a
        Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.

        Retrieving this list of Route Lists requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageRouteList')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=UsageRouteLists, params=params)]


class AsRouteListApi(AsApiChild, base='telephony/config/premisePstn/routeLists'):
    """
    API for everything route lists
    """

    def list_gen(self, *, name: list[str] = None, location_id: list[str] = None, order: str = None,
             org_id: str = None, **params) -> AsyncGenerator[RouteList, None, None]:
        """
        List all Route Lists for the organization.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving the Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of Route List matching the route list name.
        :type name: str
        :param location_id: Return the list of Route Lists matching the location id.
        :type location_id: str
        :param order: Order the Route List according to the designated fields.Available sort fields: name, locationId.
            Sort order is ascending by default
        :type order: str
        :param org_id: List all Route List for this organization.
        :type org_id: str
        :return: generator yielding :class:`RouteList` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params, model=RouteList)

    async def list(self, *, name: list[str] = None, location_id: list[str] = None, order: str = None,
             org_id: str = None, **params) -> List[RouteList]:
        """
        List all Route Lists for the organization.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving the Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of Route List matching the route list name.
        :type name: str
        :param location_id: Return the list of Route Lists matching the location id.
        :type location_id: str
        :param order: Order the Route List according to the designated fields.Available sort fields: name, locationId.
            Sort order is ascending by default
        :type order: str
        :param org_id: List all Route List for this organization.
        :type org_id: str
        :return: generator yielding :class:`RouteList` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, params=params, model=RouteList)]

    async def create(self, *, name: str, location_id: str, rg_id: str, org_id: str = None) -> str:
        """
        Create a Route List for the organization.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Creating a Route List requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param name: Name of the Route List
        :type name: str
        :param location_id: Location associated with the Route List.
        :type location_id: str
        :param rg_id: UUID of the route group associated with Route List.
        :type rg_id: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: ID of the newly route list created.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        body = {'name': name,
                'locationId': location_id,
                'routeGroupId': rg_id}
        url = self.ep()
        data = await self.post(url=url, params=params, json=body)
        return data['id']

    async def details(self, *, rl_id: str, org_id: str = None) -> RouteListDetail:
        """
        Get Route List Details.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rl_id: Id of the Route List.
        :type rl_id: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: route list details
        :rtype: :class:`RouteListDetail`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rl_id)
        data = await self.get(url=url, params=params)
        return RouteListDetail.parse_obj(data)

    async def update(self, *, rl_id: str, name: str, rg_id: str, org_id: str = None):
        """
        Modify the details for a Route List.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: Id of the Route List.
        :type rl_id: str
        :param name: Route List new name.
        :type name: str
        :param rg_id: New route group id.
        :type rg_id: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        body = {'name': name,
                'routeGroupId': rg_id}
        url = self.ep(rl_id)
        await self.put(url=url, params=params, json=body)

    async def delete_route_list(self, *, rl_id: str, org_id: str = None):
        """
        Delete Route List for a Customer

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Deleting a Route List requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: Id of the Route List.
        :type rl_id: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rl_id)
        await self.delete(url=url, params=params)

    def numbers_gen(self, *, rl_id: str, order: str = None, number: str = None,
                org_id: str = None, **params) -> AsyncGenerator[str, None, None]:
        """
        Get numbers assigned to a Route List

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: Id of the Route List.
        :type rl_id: str
        :param order: Order the Route Lists according to number.
        :type order: str
        :param number: Number assigned to the route list.
        :type number: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: generator yielding str
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params', 'rl_id'})
        url = self.ep(f'{rl_id}/numbers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params)

    async def numbers(self, *, rl_id: str, order: str = None, number: str = None,
                org_id: str = None, **params) -> List[str]:
        """
        Get numbers assigned to a Route List

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: Id of the Route List.
        :type rl_id: str
        :param order: Order the Route Lists according to number.
        :type order: str
        :param number: Number assigned to the route list.
        :type number: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: generator yielding str
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params', 'rl_id'})
        url = self.ep(f'{rl_id}/numbers')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, params=params)]

    async def update_numbers(self, *, rl_id: str, numbers: List[NumberAndAction],
                       org_id: str = None) -> List[UpdateNumbersResponse]:
        """
        Modify numbers for a specific Route List of a Customer.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: Id of the Route List.
        :type rl_id: str
        :param numbers: Array of the numbers to be deleted/added.
        :type numbers: list[:class:`NumberAndAction`]
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: list of update number status
        :rtype: list[:class:`UpdateNumbersResponse`]
        """
        url = self.ep(f'{rl_id}/numbers')
        params = org_id and {'orgId': org_id} or None

        class Body(ApiModel):
            numbers: list[NumberAndAction]

        body = Body(numbers=numbers).json()
        data = await self.put(url=url, params=params, data=body)
        if data:
            return parse_obj_as(list[UpdateNumbersResponse], data['numberStatus'])
        else:
            return []

    async def delete_all_numbers(self, *, rl_id: str, org_id: str = None):
        url = self.ep(f'{rl_id}/numbers')
        params = org_id and {'orgId': org_id} or None
        body = {'deleteAllNumbers': True}
        await self.put(url=url, params=params, json=body)


class AsTrunkApi(AsApiChild, base='telephony/config/premisePstn/trunks'):
    """
    API for everything trunks
    """

    def list_gen(self, *, name: str = None, location_name: str = None, trunk_type: str = None, order: str = None,
             org_id: str = None, **params) -> AsyncGenerator[Trunk, None, None]:
        """
        List all Trunks for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        ebex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of trunks matching the local gateway names.
        :type name: str
        :param location_name: Return the list of trunks matching the location names.
        :type location_name: str
        :param trunk_type: Return the list of trunks matching the trunk type.
        :type trunk_type: str
        :param order: Order the trunks according to the designated fields. Available sort fields: name, locationName.
            Sort order is ascending by default
        :type order: str
        :param org_id:
        :type org_id: str
        :return: generator of Trunk instances
        :rtype: :class:`Trunk`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params, model=Trunk, item_key='trunks')

    async def list(self, *, name: str = None, location_name: str = None, trunk_type: str = None, order: str = None,
             org_id: str = None, **params) -> List[Trunk]:
        """
        List all Trunks for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        ebex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of trunks matching the local gateway names.
        :type name: str
        :param location_name: Return the list of trunks matching the location names.
        :type location_name: str
        :param trunk_type: Return the list of trunks matching the trunk type.
        :type trunk_type: str
        :param order: Order the trunks according to the designated fields. Available sort fields: name, locationName.
            Sort order is ascending by default
        :type order: str
        :param org_id:
        :type org_id: str
        :return: generator of Trunk instances
        :rtype: :class:`Trunk`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, params=params, model=Trunk, item_key='trunks')]

    async def create(self, *, name: str, location_id: str, password: str, trunk_type: TrunkType,
               dual_identity_support_enabled: bool = None, device_type: TrunkDeviceType = None, address: str = None,
               domain: str = None, port: int = None, max_concurrent_calls: int = None, org_id: str = None) -> str:
        """
        Create a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Creating a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param name: A unique name for the trunk.
        :type name: str
        :param location_id: ID of location associated with the trunk.
        :type location_id: str
        :param password: A password to use on the trunk.
        :type password: str
        :param trunk_type: Trunk Type associated with the trunk.
        :type trunk_type: :class:`TrunkType`
        :param dual_identity_support_enabled: Dual Identity Support setting impacts the handling of the From header
            and P-Asserted-Identity header when sending an initial SIP INVITE to the trunk for an outbound call.
        :type dual_identity_support_enabled: bool
        :param device_type: Device type associated with trunk.
        :type device_type: :class:`TrunkDeviceType`
        :param address: FQDN or SRV address. Required to create a static certificate-based trunk.
        :type address: str
        :param domain: Domain name. Required to create a static certificate based trunk.
        :type domain: str
        :param port: FQDN port. Required to create a static certificate-based trunk.
        :type port: int
        :param max_concurrent_calls: Max Concurrent call. Required to create a static certificate based trunk.
        :type max_concurrent_calls: int
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id of new trunk
        :rtype: str
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'org_id'} and v is not None}
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = await self.post(url=url, params=params, json=body)
        return data['id']

    async def details(self, *, trunk_id: str, org_id: str = None) -> TrunkDetail:
        """
        Get a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving a trunk requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: trunk details
        :rtype: :class:`TrunkDetail`
        """
        url = self.ep(trunk_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url=url, params=params)
        return TrunkDetail.parse_obj(data)

    async def update(self, *, trunk_id: str, name: str, location_id: str, password: str, trunk_type: TrunkType,
               dual_identity_support_enabled: bool = None, max_concurrent_calls: int = None, org_id: str = None):
        """
        Modify a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Modifying a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param trunk_id:
        :type name: str
        :param location_id: ID of location associated with the trunk.
        :type location_id: str
        :param password: A password to use on the trunk.
        :type password: str
        :param trunk_type: Trunk Type associated with the trunk.
        :type trunk_type: :class:`TrunkType`
        :param dual_identity_support_enabled: Dual Identity Support setting impacts the handling of the From header
            and P-Asserted-Identity header when sending an initial SIP INVITE to the trunk for an outbound call.
        :type dual_identity_support_enabled: bool
        :param max_concurrent_calls: Max Concurrent call. Required to create a static certificate based trunk.
        :type max_concurrent_calls: int
        :param org_id: Organization to which trunk belongs.
        :type org_id: str:return:
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'org_id'} and v is not None}
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        await self.put(url=url, params=params, json=body)

    async def delete_trunk(self, *, trunk_id: str, org_id: str = None):
        """
        Delete a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Deleting a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        """
        url = self.ep(trunk_id)
        params = org_id and {'orgId': org_id} or None
        await self.delete(url=url, params=params)

    async def trunk_types(self, org_id: str = None) -> List[TrunkTypeWithDeviceType]:
        """
        List all TrunkTypes with DeviceTypes for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy. Trunk Types are Registering
        or Certificate Based and are configured in CallManager.

        Retrieving trunk types requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id:
        :return: trunk types
        :rtype: list[:class:`TrunkTypeWithDeviceType`]
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep('trunkTypes')
        data = await self.get(url=ep, params=params)
        return parse_obj_as(list[TrunkTypeWithDeviceType], data['trunkTypes'])

    async def usage(self, *, trunk_id: str, org_id: str = None) -> TrunkUsage:
        """
        Get Local Gateway Usage Count

        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: usage counts
        :rtype: :class:`TrunkUsage`
        """
        url = self.ep(f'{trunk_id}/usage')
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url=url, params=params)
        return TrunkUsage.parse_obj(data)

    def usage_dial_plan_gen(self, *, trunk_id: str, org_id: str = None) -> AsyncGenerator[IdAndName, None, None]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usageDialPlan')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    async def usage_dial_plan(self, *, trunk_id: str, org_id: str = None) -> List[IdAndName]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usageDialPlan')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params)]

    def usage_location_pstn_gen(self, *, trunk_id: str, org_id: str = None) -> AsyncGenerator[IdAndName, None, None]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with
        a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks
        that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usagePstnConnection')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    async def usage_location_pstn(self, *, trunk_id: str, org_id: str = None) -> List[IdAndName]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with
        a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks
        that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usagePstnConnection')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params)]

    def usage_route_group_gen(self, *, trunk_id: str, org_id: str = None) -> AsyncGenerator[IdAndName, None, None]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usageRouteGroup')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    async def usage_route_group(self, *, trunk_id: str, org_id: str = None) -> List[IdAndName]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: Id of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usageRouteGroup')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params)]

    def validate_fqdn_and_domain(self):
        # TODO: implement
        ...

    # TODO: are we missing a usage for trunks used for calls to unknown extensions??
    # TODO: are we missing a usage for route lists??


class AsPremisePstnApi(AsApiChild, base='telephony/config/premisePstn'):
    """
    Premises PSTN API
    """
    #: dial plan configuration
    dial_plan: AsDialPlanApi
    #: trunk configuration
    trunk: AsTrunkApi
    #: route group configuration
    route_group: AsRouteGroupApi
    #: route list configuration
    route_list: AsRouteListApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.dial_plan = AsDialPlanApi(session=session)
        self.trunk = AsTrunkApi(session=session)
        self.route_group = AsRouteGroupApi(session=session)
        self.route_list = AsRouteListApi(session=session)

    async def validate_pattern(self, dial_patterns: Union[str, List[str]], org_id: str = None) -> DialPatternValidationResult:
        """
        Validate a Dial Pattern.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Validating a dial pattern requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param dial_patterns: Array of dial patterns.
        :type dial_patterns: list[str] or str
        :param org_id: Organization to which dial plan belongs.
        :return: validation result
        :rtype: :class:`DialPatternValidationResult`
        """
        if isinstance(dial_patterns, str):
            dial_patterns = [dial_patterns]

        url = self.ep('actions/validateDialPatterns/invoke')
        params = org_id and {'orgId': org_id} or None
        body = {'dialPatterns': dial_patterns}
        data = await self.post(url=url, params=params, json=body)
        return DialPatternValidationResult.parse_obj(data)


class AsPrivateNetworkConnectApi(AsApiChild, base='telephony/config/locations'):
    """
    API for location private network connect API settings
    """

    async def read(self, *, location_id: str, org_id: str = None) -> NetworkConnectionType:
        """
        Get Private Network Connect

        Retrieve the location's network connection type.

        Network Connection Type determines if the location's network connection is public or private.

        Retrieving location's network connection type requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve network connection type for this location.
        :type location_id: str
        :param org_id: Retrieve network connection type for this organization.
        :type org_id: str
        :return: location PNC settings
        :rtype: NetworkConnectionType
        """
        params = org_id and {'orgId': org_id} or None
        url = self.session.ep(f'telephony/config/locations/{location_id}/privateNetworkConnect')
        data = await self.get(url, params=params)
        return parse_obj_as(NetworkConnectionType, data['networkConnectionType'])

    async def update(self, *, location_id: str, connection_type: NetworkConnectionType, org_id: str = None):
        """
        Get Private Network Connect

        Retrieve the location's network connection type.

        Network Connection Type determines if the location's network connection is public or private.

        Retrieving location's network connection type requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Update network connection type for this location.
        :type location_id: str
        :param connection_type: Network Connection Type for the location.
        :type connection_type: NetworkConnectionType
        :param org_id: Update network connection type for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.session.ep(f'telephony/config/locations/{location_id}/privateNetworkConnect')
        body = {'networkConnectionType': connection_type.value}
        await self.put(url, json=body, params=params)


class AsInternalDialingApi(AsApiChild, base='telephony/config/locations'):
    """
    Internal dialing settings for location
    """

    def url(self, *, location_id: str) -> str:
        return super().ep(f'{location_id}/internalDialing')

    async def read(self, *, location_id: str, org_id: str = None) -> InternalDialing:
        """
        Get current configuration for routing unknown extensions to the Premises as internal calls

        If some users in a location are registered to a PBX, retrieve the setting to route unknown extensions (digits
        that match the extension length) to the PBX.

        Retrieving the internal dialing configuration requires a full or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: location for which internal calling configuration is being requested
        :type location_id: str
        :param org_id:
        :type org_id: str
        :return: settings
        :rtype: :class:`InternalDialing`
        """
        url = self.url(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url=url, params=params)
        return InternalDialing.parse_obj(data)

    async def update(self, *, location_id: str, update: InternalDialing, org_id: str = None):
        """
        Modify current configuration for routing unknown extensions to the Premises as internal calls

        If some users in a location are registered to a PBX, enable the setting to route unknown extensions (digits
        that match the extension length) to the PBX.

        Editing the internal dialing configuration requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: location for which internal calling configuration is being requested
        :type location_id: str
        :param update: new settings
        :type update: :class:`InternalDialing`
        :param org_id:
        :type org_id: str
        """
        url = self.url(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = update.json(exclude_none=False)
        await self.put(url=url, params=params, data=data)


class AsLocationInterceptApi(AsApiChild, base='telephony/config/locations'):
    """
    API for location's call intercept settings
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific
        telephony/config/locations/{locationId}/intercept

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/intercept{path}')
        return ep

    async def read(self, *, location_id: str, org_id: str = None) -> InterceptSetting:
        """
        Get Location Intercept

        Retrieve intercept location details for a customer location.

        Intercept incoming or outgoing calls for persons in your organization. If this is enabled, calls are either
        routed to a designated number the person chooses, or to the person's voicemail.

        Retrieving intercept location details requires a full, user or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve intercept details for this location.
        :type location_id: str
        :param org_id: Retrieve intercept location details for a customer location.
        :type org_id: str
        :return: user's call intercept settings
        :rtype: :class:`wxc_sdk.person_settings.call_intercept.InterceptSetting`
        """
        ep = self._endpoint(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        return InterceptSetting.parse_obj(await self.get(ep, params=params))

    async def configure(self, *, location_id: str, settings: InterceptSetting, org_id: str = None):
        """
        Put Location Intercept

        Modifies the intercept location details for a customer location.

        Intercept incoming or outgoing calls for users in your organization. If this is enabled, calls are either
        routed to a designated number the user chooses, or to the user's voicemail.

        Modifying the intercept location details requires a full, user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Unique identifier for the person.
        :type location_id: str
        :param settings: new intercept settings
        :type settings: InterceptSetting
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self._endpoint(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = settings.json()
        await self.put(ep, params=params, data=data)


class AsLocationMoHApi(AsApiChild, base='telephony/config/locations'):
    """
    Access codes API
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific feature endpoint like
        /v1/telephony/config/locations/{locationId}/musicOnHold

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/musicOnHold{path}')
        return ep

    async def read(self, *, location_id: str, org_id: str = None) -> LocationMoHSetting:
        """
        Get Music On Hold

        Retrieve the location's music on hold settings.

        Location's music on hold settings allows you to play music when a call is placed on hold or parked.

        Retrieving location's music on hold settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        :return: MoH settings
        :rtype: :class:`LocationMoHSetting`
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        data = await self.get(url, params=params)
        return LocationMoHSetting.parse_obj(data)

    async def update(self, *, location_id: str, settings: LocationMoHSetting, org_id: str = None) -> LocationMoHSetting:
        """
        Get Music On Hold

        Retrieve the location's music on hold settings.

        Location's music on hold settings allows you to play music when a call is placed on hold or parked.

        Retrieving location's music on hold settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param settings: new settings
        :type settings: :class:`LocationMoHSetting`
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        :return: list of :class:`wxc_sdk.common.CallPark`
        """
        params = org_id and {'orgId': org_id} or None
        data = settings.json()
        url = self._endpoint(location_id=location_id)
        await self.put(url, params=params, data=data)

    async def create(self, *, location_id: str, access_codes: list[AuthCode], org_id: str = None) -> list[AuthCode]:
        """

        :param location_id: Add new access code for this location.
        :type location_id: str
        :param access_codes: Access code details
        :type access_codes: list of :class:`wxc_sdk.common.AuthCode`
        :param org_id: Add new access code for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = {'accessCodes': [json.loads(ac.json()) for ac in access_codes]}
        await self.post(url, json=body, params=params)

    async def delete_codes(self, *, location_id: str, access_codes: list[Union[str, AuthCode]],
                     org_id: str = None) -> list[AuthCode]:
        """
        Delete Access Code Location

        Deletes the access code details for a particular location for a customer.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Modifying the access code location details requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Deletes the access code details for this location.
        :type location_id: str
        :param access_codes: access codes to delete
        :type access_codes: list of :class:`wxc_sdk.common.AuthCode` or str
        :param org_id: Delete access codes from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = {'deleteCodes': [ac.code if isinstance(ac, AuthCode) else ac
                                for ac in access_codes]}
        await self.put(url, json=body, params=params)


class AsLocationNumbersApi(AsApiChild, base='telephony/config/locations'):
    def _url(self, location_id: str, path: str = None):
        path = path and f'/{path}' or ''
        return self.ep(f'{location_id}/numbers{path}')

    async def add(self, *, location_id: str, phone_numbers: list[str], state: NumberState = NumberState.inactive,
            org_id: str = None):
        """
        Adds specified set of phone numbers to a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Adding a phone number to a location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: list[str]
        :param state: State of the phone numbers.
        :type state: :class:`wxc_sdk.common.NumberState`
        :param org_id: Organization to manage
        :type org_id: str
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = {'phoneNumbers': phone_numbers,
                'state': state}
        await self.post(url=url, params=params, json=body)

    async def activate(self, *, location_id: str, phone_numbers: list[str], org_id: str = None):
        """
        Activate the specified set of phone numbers in a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features.
        Phone numbers must follow E.164 format for all countries, except for the United States, which can also
        follow the National format. Active phone numbers are in service.

        Activating a phone number in a location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: LocationId in which numbers should be activated.
        :type location_id: str
        :param phone_numbers: List of phone numbers to be activated.
        :type phone_numbers: list[str]
        :param org_id: Organization to manage
        :type org_id: str
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = {'phoneNumbers': phone_numbers}
        await self.put(url=url, params=params, json=body)

    async def remove(self, *, location_id: str, phone_numbers: list[str], org_id: str = None):
        """
        Remove the specified set of phone numbers from a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Removing a phone number from a location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: LocationId from which numbers should be removed.
        :type location_id: str
        :param phone_numbers: List of phone numbers to be removed.
        :type phone_numbers: list[str]
        :param org_id: Organization to manage
        :type org_id: str
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = {'phoneNumbers': phone_numbers}
        await self.delete(url=url, params=params, json=body)


class AsLocationVoicemailSettingsApi(AsApiChild, base='telephony/config/locations'):
    """
    location voicemail settings API, for now only enable/disable Vm transcription
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific
        telephony/config/locations/{locationId}/voicemail

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/voicemail{path}')
        return ep

    async def read(self, *, location_id: str, org_id: str = None) -> LocationVoiceMailSettings:
        """
        Get Location Voicemail

        Retrieve voicemail settings for a specific location.

        Location's voicemail settings allows you to enable voicemail transcription for a specific location.

        Retrieving location's voicemail settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.


        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        :return: location voicemail settings
        :rtype: :class:`LocationVoiceMailSettings`
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        data = await self.get(url, params=params)
        return LocationVoiceMailSettings.parse_obj(data)

    async def update(self, *, location_id: str, settings: LocationVoiceMailSettings, org_id: str = None):
        """
        Get Location Voicemail

        Retrieve voicemail settings for a specific location.

        Location's voicemail settings allows you to enable voicemail transcription for a specific location.

        Retrieving location's voicemail settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.


        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param settings: new settings
        :type settings: :class:`LocationVoiceMailSettings`
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = settings.json()
        await self.put(url, params=params, data=body)


@dataclass(init=False)
class AsTelephonyLocationApi(AsApiChild, base='telephony/config/locations'):
    #: call intercept settings
    intercept: AsLocationInterceptApi
    #: internal dialing settings
    internal_dialing: AsInternalDialingApi
    #: moh settings
    moh: AsLocationMoHApi
    #: number settings
    number: AsLocationNumbersApi
    #: Location VM settings (only enable/disable transcription for now)
    voicemail: AsLocationVoicemailSettingsApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.intercept = AsLocationInterceptApi(session=session)
        self.moh = AsLocationMoHApi(session=session)
        self.number = AsLocationNumbersApi(session=session)
        self.voicemail = AsLocationVoicemailSettingsApi(session=session)
        self.internal_dialing = AsInternalDialingApi(session=session)

    async def generate_password(self, *, location_id: str, generate: list[str] = None, org_id: str = None):
        """
        Generates an example password using the effective password settings for the location. If you don't specify
        anything in the generate field or don't provide a request body, then you will receive a SIP password by default.

        It's used while creating a trunk and shouldn't be used anywhere else.

        Generating an example password requires a full or write-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location for which example password has to be generated.
        :type location_id: str
        :param generate: password settings array.
        :type generate: list[str]
        :param org_id: Organization to which location belongs.
        :type org_id: str
        :return: new password
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        body = generate and {'generate': generate} or {}
        url = self.ep(f'{location_id}/actions/generatePassword/invoke')
        data = await self.post(url=url, params=params, json=body)
        return data['exampleSipPassword']

    async def validate_extensions(self, location_id: str, extensions: list[str],
                            org_id: str = None) -> ValidateExtensionsResponse:
        """
        Validate extensions for a specific location.

        Validating extensions requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Validate extensions for this location.
        :type location_id: str
        :param extensions: Array of extensions that will be validated.
        :type extensions: list[str]
        :param org_id: Validate extensions for this organization.
        :type org_id: str
        :return: Validation result
        :rtype: :class:`wxc_sdk.common.ValidateExtensionsResponse`
        """
        url = self.ep(f'{location_id}/actions/validateExtensions/invoke')
        body = {'extensions': extensions}
        params = org_id and {'orgId': org_id} or None
        data = await self.post(url=url, params=params, json=body)
        return ValidateExtensionsResponse.parse_obj(data)


class AsVoicePortalApi(AsApiChild, base='telephony/config/locations'):
    """
    location voice portal API
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific
        telephony/config/locations/{locationId}/voicePortal

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/voicePortal{path}')
        return ep

    async def read(self, *, location_id: str, org_id: str = None) -> VoicePortalSettings:
        """

        :param location_id: Location to which the voice portal belongs.
        :type location_id: str
        :param org_id: Organization to which the voice portal belongs.
        :type org_id: str
        :return: location voice portal settings
        :rtype: VoicePortalSettings
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        return VoicePortalSettings.parse_obj(await self.get(url, params=params))

    async def update(self, *, location_id: str, settings: VoicePortalSettings, passcode: str = None, org_id: str = None):
        """
        Update VoicePortal

        Update Voice portal information for the location.

        Voice portals provide an interactive voice response (IVR) system so administrators can manage auto attendant
        announcements.

        Updating voice portal information for organization and/or rules requires a full administrator auth token with
        a scope of spark-admin:telephony_config_write.

        :param location_id: Location to which the voice portal belongs.
        :type location_id: str
        :param settings: new settings
        :type settings: VoicePortalSettings
        :param passcode: new passcode
        :type passcode: str
        :param org_id: Organization to which the voice portal belongs.
        :type org_id: str
        """
        data = json.loads(settings.json(exclude={'portal_id': True,
                                                 'language': True}))
        if passcode is not None:
            data['passcode'] = {'newPasscode': passcode,
                                'confirmPasscode': passcode}
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        await self.put(url, params=params, json=data)

    async def passcode_rules(self, *, location_id: str, org_id: str = None) -> PasscodeRules:
        """
        Get VoicePortal Passcode Rule

        Retrieve the voice portal passcode rule for a location.

        Voice portals provide an interactive voice response (IVR) system so administrators can manage auto attendant
        announcements

        Retrieving the voice portal passcode rule requires a full read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve voice portal passcode rules for this location.
        :type location_id: str
        :param org_id: Retrieve voice portal passcode rules for this organization.
        :type org_id: str
        :return: passcode rules
        :rtype: PasscodeRules
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, path='passcodeRules')
        return PasscodeRules.parse_obj(await self.get(url, params=params))


class AsVoicemailGroupsApi(AsApiChild, base='telephony/config/voicemailGroups'):
    """
    API for location private network connect API settings
    """

    def list(self, *, location_id: str = None, name: str = None, phone_number: str = None, org_id: str = None):
        params = {to_camel(p): v for p, v in locals().items() if p != 'self' and v is not None}
        url = self.ep()
        return self.session.follow_pagination(url=url, model=VoicemailGroup, params=params, item_key='voicemailGroups')


class AsVoicemailRulesApi(AsApiChild, base='telephony/config/voicemail/rules'):
    """
    API for voicemail rules settings
    """

    async def read(self, *, org_id: str = None) -> VoiceMailRules:
        """
        Get Voicemail Rules

        Retrieve the organization's voicemail rules.

        Organizational voicemail rules specify the default passcode requirements.

        Retrieving the organization's voicemail rules requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param org_id: Retrieve voicemail settings for this organization.
        :type org_id: str
        :return: VM settings
        :rtype: OrganisationVoicemailSettings
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        return VoiceMailRules.parse_obj(await self.get(url, params=params))

    async def update(self, *, settings: VoiceMailRules, org_id: str = None):
        """
        Update Voicemail Rules

        Update the organization's default voicemail passcode and/or rules.

        Organizational voicemail rules specify the default passcode requirements.

        If you choose to set default passcode for new people added to your organization, communicate to your people
        what that passcode is, and that it must be reset before they can access their voicemail. If this feature is
        not turned on, each new person must initially set their own passcode.

        Updating organization's voicemail passcode and/or rules requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param settings: new settings
        :type settings: VoiceMailRules
        :param org_id: Update voicemail rules for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = settings.json(exclude={'default_voicemail_pin_rules': True})
        await self.put(url, params=params, data=data)


class AsTelephonyApi(AsApiChild, base='telephony'):
    """
    The telephony settings (features) API.
    """
    #: access or authentication codes
    access_codes: AsAccessCodesApi
    auto_attendant: AsAutoAttendantApi
    calls: AsCallsApi
    callpark: AsCallParkApi
    callpark_extension: AsCallparkExtensionApi
    callqueue: AsCallQueueApi
    huntgroup: AsHuntGroupApi
    #: location specific settings
    location: AsTelephonyLocationApi
    #: organisation voicemail settings
    organisation_voicemail: AsOrganisationVoicemailSettingsAPI
    paging: AsPagingApi
    permissions_out: AsOutgoingPermissionsApi
    pickup: AsCallPickupApi
    prem_pstn: AsPremisePstnApi
    pnc: AsPrivateNetworkConnectApi
    schedules: AsScheduleApi
    voicemail_groups: AsVoicemailGroupsApi
    voicemail_rules: AsVoicemailRulesApi
    voiceportal: AsVoicePortalApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.access_codes = AsAccessCodesApi(session=session)
        self.auto_attendant = AsAutoAttendantApi(session=session)
        self.calls = AsCallsApi(session=session)
        self.callpark = AsCallParkApi(session=session)
        self.callpark_extension = AsCallparkExtensionApi(session=session)
        self.callqueue = AsCallQueueApi(session=session)
        self.huntgroup = AsHuntGroupApi(session=session)
        self.location = AsTelephonyLocationApi(session=session)
        self.organisation_voicemail = AsOrganisationVoicemailSettingsAPI(session=session)
        self.paging = AsPagingApi(session=session)
        self.permissions_out = AsOutgoingPermissionsApi(session=session, locations=True)
        self.pickup = AsCallPickupApi(session=session)
        self.pnc = AsPrivateNetworkConnectApi(session=session)
        self.prem_pstn = AsPremisePstnApi(session=session)
        self.schedules = AsScheduleApi(session=session, base=ScheduleApiBase.locations)
        self.voicemail_groups = AsVoicemailGroupsApi(session=session)
        self.voicemail_rules = AsVoicemailRulesApi(session=session)
        self.voiceportal = AsVoicePortalApi(session=session)

    def phone_numbers_gen(self, *, location_id: str = None, phone_number: str = None, available: bool = None,
                      order: str = None,
                      owner_name: str = None, owner_id: str = None, owner_type: OwnerType = None,
                      extension: str = None, number_type: NumberType = None,
                      phone_number_type: NumberListPhoneNumberType = None,
                      state: NumberState = None, toll_free_numbers: bool = None,
                      org_id: str = None, **params) -> AsyncGenerator[NumberListPhoneNumber, None, None]:
        """
        Get Phone Numbers for an Organization with given criteria.

        List all the phone numbers for the given organization along with the status and owner (if any).

        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return the list of phone numbers for this location within the given organization.
        :type location_id: str
        :param phone_number: Search for this phone number.
        :type phone_number: str
        :param available: Search among the available phone numbers. This parameter cannot be used along with owner_type
            parameter when set to true.
        :type available: bool
        :param order: Sort the list of phone numbers based on the following:lastName,dn,extension. Default sort will
            be based on number and extension in an Ascending order
        :type order: str
        :param owner_name: Return the list of phone numbers that is owned by given owner name. Maximum length is 255.
        :type owner_name: str
        :param owner_id: Returns only the matched number/extension entries assigned to the feature with specified
            uuid/broadsoftId.
        :type owner_id: str
        :param owner_type: Returns the list of phone numbers that are of given owner_type.
        :type owner_type: OwnerType
        :param extension: Returns the list of PSTN phone numbers with given extension.
        :type extension: str
        :param number_type: Returns the filtered list of PSTN phone numbers that contains given type of numbers.
            This parameter cannot be used along with available or state.
        :type number_type: NumberType
        :param phone_number_type: Returns the filtered list of PSTN phone numbers that are of given phoneNumberType.
        :type phone_number_type: NumberListPhoneNumberType
        :param state: Returns the list of PSTN phone numbers with matching state.
        :type state: NumberState
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: yields :class:`NumberListPhoneNumber` instances
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i and v is not None and p != 'params')
        for param, value in params.items():
            if isinstance(value, bool):
                value = 'true' if value else 'false'
                params[param] = value
            elif isinstance(value, Enum):
                value = value.value
                params[param] = value
        url = self.ep(path='config/numbers')
        return self.session.follow_pagination(url=url, model=NumberListPhoneNumber, params=params,
                                              item_key='phoneNumbers')

    async def phone_numbers(self, *, location_id: str = None, phone_number: str = None, available: bool = None,
                      order: str = None,
                      owner_name: str = None, owner_id: str = None, owner_type: OwnerType = None,
                      extension: str = None, number_type: NumberType = None,
                      phone_number_type: NumberListPhoneNumberType = None,
                      state: NumberState = None, toll_free_numbers: bool = None,
                      org_id: str = None, **params) -> List[NumberListPhoneNumber]:
        """
        Get Phone Numbers for an Organization with given criteria.

        List all the phone numbers for the given organization along with the status and owner (if any).

        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return the list of phone numbers for this location within the given organization.
        :type location_id: str
        :param phone_number: Search for this phone number.
        :type phone_number: str
        :param available: Search among the available phone numbers. This parameter cannot be used along with owner_type
            parameter when set to true.
        :type available: bool
        :param order: Sort the list of phone numbers based on the following:lastName,dn,extension. Default sort will
            be based on number and extension in an Ascending order
        :type order: str
        :param owner_name: Return the list of phone numbers that is owned by given owner name. Maximum length is 255.
        :type owner_name: str
        :param owner_id: Returns only the matched number/extension entries assigned to the feature with specified
            uuid/broadsoftId.
        :type owner_id: str
        :param owner_type: Returns the list of phone numbers that are of given owner_type.
        :type owner_type: OwnerType
        :param extension: Returns the list of PSTN phone numbers with given extension.
        :type extension: str
        :param number_type: Returns the filtered list of PSTN phone numbers that contains given type of numbers.
            This parameter cannot be used along with available or state.
        :type number_type: NumberType
        :param phone_number_type: Returns the filtered list of PSTN phone numbers that are of given phoneNumberType.
        :type phone_number_type: NumberListPhoneNumberType
        :param state: Returns the list of PSTN phone numbers with matching state.
        :type state: NumberState
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: yields :class:`NumberListPhoneNumber` instances
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i and v is not None and p != 'params')
        for param, value in params.items():
            if isinstance(value, bool):
                value = 'true' if value else 'false'
                params[param] = value
            elif isinstance(value, Enum):
                value = value.value
                params[param] = value
        url = self.ep(path='config/numbers')
        return [o async for o in self.session.follow_pagination(url=url, model=NumberListPhoneNumber, params=params,
                                              item_key='phoneNumbers')]

    async def phone_number_details(self, *, org_id: str = None) -> NumberDetails:
        """
        get summary (counts) of phone numbers

        :param org_id: detaild for numbers in this organization.
        :type org_id: str
        :return: phone number details
        :rtype: :class:`NumberDetails`
        """
        params = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                  if i and v is not None}
        params['details'] = 'true'
        params['max'] = 1
        url = self.ep(path='config/numbers')
        data = await self.get(url, params=params)
        return NumberDetails.parse_obj(data['count'])

    async def validate_extensions(self, *, extensions: list[str]) -> ValidateExtensionsResponse:
        """
        Validate the List of Extensions

        Validate the List of Extensions. Retrieving this list requires a full or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param extensions: Array of Strings of ID of Extensions.
        :type extensions: list[str]
        :return: validation response
        :rtype: :class:`wxc_sdk.common.ValidateExtensionsResponse`
        """
        url = self.ep(path='config/actions/validateExtensions/invoke')
        data = await self.post(url, json={'extensions': extensions})
        return ValidateExtensionsResponse.parse_obj(data)

    async def validate_phone_numbers(self, phone_numbers: list[str], org_id: str = None) -> ValidatePhoneNumbersResponse:
        """
        Validate the list of phone numbers in an organization. Each phone number's availability is indicated in the
        response.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Validating a phone number in an organization requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param phone_numbers: List of phone numbers to be validated.
        :type phone_numbers: list[str]
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :return: validation result
        :rtype: :class:`wxc_sdk.common.ValidatePhoneNumbersResponse`
        """
        url = self.ep('config/actions/validateNumbers/invoke')
        body = {'phoneNumbers': phone_numbers}
        params = org_id and {'orgId': org_id} or None
        data = await self.post(url=url, params=params, json=body)
        return ValidatePhoneNumbersResponse.parse_obj(data)

    async def ucm_profiles(self, *, org_id: str = None) -> list[UCMProfile]:
        """
        Read the List of UC Manager Profiles

        List all calling UC Manager Profiles for the organization.

        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in
        Webex Teams (Unified CM).

        The UC Manager Profile has an organization-wide default and may be overridden for individual persons, although
        currently only setting at a user level is supported by Webex APIs.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:people_read as this API is designed to be used in conjunction with calling behavior at the
        user level.

        :param org_id: List manager profiles in this organization.
        :type org_id: str
        :return: list of :class:`UCMProfile`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(path='config/callingProfiles')
        data = await self.get(url, params=params)
        return parse_obj_as(list[UCMProfile], data['callingProfiles'])

    async def change_announcement_language(self, *, location_id: str, language_code: str, agent_enabled: bool = None,
                                     service_enabled: bool = None, org_id: str = None):
        """
        Change Announcement Language

        Change announcement language for the given location.

        Change announcement language for current people/workspaces and/or existing feature configurations. This does
        not change the default announcement language which is applied to new users/workspaces and new feature
        configurations.

        Changing announcement language for the given location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Change announcement language for this location.
        :type location_id: str
        :param language_code: Language code.
        :type language_code: str
        :param agent_enabled: Set to true to change announcement language for existing people and workspaces.
        :type agent_enabled: bool
        :param service_enabled: Set to true to change announcement language for existing feature configurations.
        :type service_enabled: bool
        :param org_id: Change announcement language for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        body = {'announcementLanguageCode': language_code}
        if agent_enabled is not None:
            body['agentEnabled'] = agent_enabled
        if service_enabled is not None:
            body['serviceEnabled'] = service_enabled
        url = self.session.ep(f'telephony/config/locations/{location_id}/actions/modifyAnnouncementLanguage/invoke')
        await self.put(url, json=body, params=params)

    def route_choices_gen(self, route_group_name: str = None, trunk_name: str = None, order: str = None,
                      org_id: str = None) -> AsyncGenerator[RouteIdentity, None, None]:
        """
        List all Routes for the organization.

        Trunk and Route Group qualify as Route. Trunks and Route Groups provide you the ability to configure Webex
        Calling to manage calls between Webex Calling hosted users and premises PBX(s) users. This solution lets you
        configure users to use Cloud PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param route_group_name: Return the list of route identities matching the route group name.
        :param trunk_name: Return the list of route identities matching the trunk name.
        :param order: Order the route identities according to the designated fields.
            Available sort fields: routeName, routeType.
        :param org_id: List route identities for this organization.
        :return:
        """
        params = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                  if i and v is not None}
        url = self.ep('config/routeChoices')
        return self.session.follow_pagination(url=url, model=RouteIdentity, params=params, item_key='routeIdentities')

    async def route_choices(self, route_group_name: str = None, trunk_name: str = None, order: str = None,
                      org_id: str = None) -> List[RouteIdentity]:
        """
        List all Routes for the organization.

        Trunk and Route Group qualify as Route. Trunks and Route Groups provide you the ability to configure Webex
        Calling to manage calls between Webex Calling hosted users and premises PBX(s) users. This solution lets you
        configure users to use Cloud PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param route_group_name: Return the list of route identities matching the route group name.
        :param trunk_name: Return the list of route identities matching the trunk name.
        :param order: Order the route identities according to the designated fields.
            Available sort fields: routeName, routeType.
        :param org_id: List route identities for this organization.
        :return:
        """
        params = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                  if i and v is not None}
        url = self.ep('config/routeChoices')
        return [o async for o in self.session.follow_pagination(url=url, model=RouteIdentity, params=params, item_key='routeIdentities')]

    async def test_call_routing(self, *, originator_id: str, originator_type: OriginatorType, destination: str,
                          originator_number: str = None, org_id: str = None) -> TestCallRoutingResult:
        """
        Validates that an incoming call can be routed.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Test call routing requires a full or write-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param originator_id: This element is used to identify the originating party. It can be user UUID or trunk UUID.
        :type originator_id: str
        :param originator_type:
        :type originator_type: :class:`OriginatorType`
        :param destination: This element specifies called party. It can be any dialable string, for example, an
            ESN number, E.164 number, hosted user DN, extension, extension with location code, URL, FAC code.
        :type destination: str
        :param originator_number: Only used when originatorType is TRUNK. This element could be a phone number or URI.
        :type originator_number: str
        :param org_id: Organization in which we are validating a call routing.
        :type org_id: str
        :return: call routing test result
        :rtype: :class:`TestCallRoutingResult`
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'org_id'} and v is not None}
        params = org_id and {'orgId': org_id} or None
        url = self.ep('config/actions/testCallRouting/invoke')
        data = await self.post(url=url, params=params, json=body)
        return TestCallRoutingResult.parse_obj(data)


class AsWebhookApi(AsApiChild, base='webhooks'):
    """
    API for webhook management
    """

    def list_gen(self) -> AsyncGenerator[WebHook, None, None]:
        """
        List all of your webhooks.

        :return: yields webhooks
        """
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=WebHook)

    async def list(self) -> List[WebHook]:
        """
        List all of your webhooks.

        :return: yields webhooks
        """
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=WebHook)]

    async def create(self, *, name: str, target_url: str, resource: WebHookResource, event: WebHookEvent, filter: str = None,
               secret: str = None,
               owned_by: str = None) -> WebHook:
        """
        Creates a webhook.

        :param name: A user-friendly name for the webhook.
        :param target_url: The URL that receives POST requests for each event.
        :param resource: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource
            the webhook is for.
        :param event: The event type for the webhook.
        :param filter: The filter that defines the webhook scope.
        :param secret: The secret used to generate payload signature.
        :param owned_by: Specified when creating an org/admin level webhook. Supported for meetings, recordings and
            meetingParticipants resources for now.

        :return: the new webhook
        """
        params = {to_camel(param): value for i, (param, value) in enumerate(locals().items())
                  if i and value is not None}
        body = json.loads(WebHookCreate(**params).json())
        ep = self.ep()
        data = await self.post(ep, json=body)
        result = WebHook.parse_obj(data)
        return result

    async def details(self, *, webhook_id: str) -> WebHook:
        """
        Get Webhook Details
        Shows details for a webhook, by ID.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :return: Webhook details
        """
        url = self.ep(webhook_id)
        return WebHook.parse_obj(await self.get(url))

    async def update(self, *, webhook_id: str, update: WebHook) -> WebHook:
        """
        Updates a webhook, by ID. You cannot use this call to deactivate a webhook, only to activate a webhook that
        was auto deactivated. The fields that can be updated are name, targetURL, secret and status. All other fields,
        if supplied, are ignored.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :param update: The webhook update
        :type update: WebHook
        :return: updated :class:`WebHook` object
        """
        url = self.ep(webhook_id)
        webhook_data = update.json(include={'name', 'target_url', 'secret', 'owned_by', 'status'})
        return WebHook.parse_obj(await self.put(url, data=webhook_data))

    async def webhook_delete(self, *, webhook_id: str):
        """
        Deletes a webhook, by ID.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :return: None
        """
        ep = self.ep(f'{webhook_id}')
        await self.delete(ep)


@dataclass(init=False)
class AsWorkspaceSettingsApi(AsApiChild, base='workspaces'):
    """
    API for all workspace settings.

    Most of the workspace settings are equivalent to corresponding user settings. For these settings the attributes of
    this class are instances of the respective user settings APIs. When calling endpoints of these APIs workspace IDs
    need to be passed to the ``person_id`` parameter of the called function.
    """
    call_intercept: AsCallInterceptApi
    call_waiting: AsCallWaitingApi
    caller_id: AsCallerIdApi
    forwarding: AsPersonForwardingApi
    monitoring: AsMonitoringApi
    numbers: AsNumbersApi
    permissions_in: AsIncomingPermissionsApi
    permissions_out: AsOutgoingPermissionsApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.call_intercept = AsCallInterceptApi(session=session, workspaces=True)
        self.call_waiting = AsCallWaitingApi(session=session, workspaces=True)
        self.caller_id = AsCallerIdApi(session=session, workspaces=True)
        self.forwarding = AsPersonForwardingApi(session=session, workspaces=True)
        self.monitoring = AsMonitoringApi(session=session, workspaces=True)
        self.numbers = AsNumbersApi(session=session, workspaces=True)
        self.permissions_in = AsIncomingPermissionsApi(session=session, workspaces=True)
        self.permissions_out = AsOutgoingPermissionsApi(session=session, workspaces=True)


class AsWorkspacesApi(AsApiChild, base='workspaces'):
    """
    Workspaces API

    Workspaces represent where people work, such as conference rooms, meeting spaces, lobbies, and lunch rooms. Devices
    may be associated with workspaces.

    Viewing the list of workspaces in an organization requires an administrator auth token with
    the spark-admin:workspaces_read scope. Adding, updating, or deleting workspaces in an organization requires an
    administrator auth token with the spark-admin:workspaces_write scope.

    The Workspaces API can also be used by partner administrators acting as administrators of a different organization
    than their own. In those cases an orgId value must be supplied, as indicated in the reference documentation for
    the relevant endpoints.
    """

    def list_gen(self, *, workspace_location_id: str = None, floor_id: str = None, display_name: str = None,
             capacity: int = None,
             workspace_type: WorkSpaceType = None, calling: CallingType = None, calendar: CalendarType = None,
             org_id: str = None, **params) -> AsyncGenerator[Workspace, None, None]:
        """
        List Workspaces

        List workspaces. Use query parameters to filter the response. The orgId parameter can only be used by admin
        users of another organization (such as partners). The workspaceLocationId, floorId, capacity and type fields
        will only be present for workspaces that have a value set for them. The special values notSet (for filtering
        on category) and -1 (for filtering on capacity) can be used to filter for workspaces without a type and/or
        capacity.

        :param workspace_location_id: Location associated with the workspace
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param display_name: List workspaces by display name.
        :type display_name: str
        :param capacity: List workspaces with the given capacity. Must be -1 or higher. A value of -1 lists workspaces
            with no capacity set.
        :type capacity: int
        :param workspace_type: List workspaces by type.
        :type workspace_type: :class:`WorkSpaceType`
        :param calling: List workspaces by calling type.
        :type calling: :class:`CallingType`
        :param calendar: List workspaces by calendar type.
        :type calendar: :class:`CalendarType`
        :param org_id: List workspaces in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: generator of :class:`Workspace` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        if workspace_type is not None:
            params.pop('workspaceType')
            params['type'] = workspace_type
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Workspace, params=params)

    async def list(self, *, workspace_location_id: str = None, floor_id: str = None, display_name: str = None,
             capacity: int = None,
             workspace_type: WorkSpaceType = None, calling: CallingType = None, calendar: CalendarType = None,
             org_id: str = None, **params) -> List[Workspace]:
        """
        List Workspaces

        List workspaces. Use query parameters to filter the response. The orgId parameter can only be used by admin
        users of another organization (such as partners). The workspaceLocationId, floorId, capacity and type fields
        will only be present for workspaces that have a value set for them. The special values notSet (for filtering
        on category) and -1 (for filtering on capacity) can be used to filter for workspaces without a type and/or
        capacity.

        :param workspace_location_id: Location associated with the workspace
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param display_name: List workspaces by display name.
        :type display_name: str
        :param capacity: List workspaces with the given capacity. Must be -1 or higher. A value of -1 lists workspaces
            with no capacity set.
        :type capacity: int
        :param workspace_type: List workspaces by type.
        :type workspace_type: :class:`WorkSpaceType`
        :param calling: List workspaces by calling type.
        :type calling: :class:`CallingType`
        :param calendar: List workspaces by calendar type.
        :type calendar: :class:`CalendarType`
        :param org_id: List workspaces in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: generator of :class:`Workspace` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        if workspace_type is not None:
            params.pop('workspaceType')
            params['type'] = workspace_type
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=Workspace, params=params)]

    async def create(self, *, settings: Workspace, org_id: str = None):
        """
        Create a Workspace

        Create a workspace. The workspaceLocationId, floorId, capacity, type and notes parameters are optional, and
        omitting them will result in the creation of a workspace without these values set, or set to their default.
        A workspaceLocationId must be provided when the floorId is set. Calendar and calling can also be set for a
        new workspace. Omitting them will default to free calling and no calendaring. The orgId parameter can only be
        used by admin users of another organization (such as partners).

        :param settings: settings for new Workspace
        :type settings: :class:`Workspace`
        :param org_id: OrgId associated with the workspace. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: new workspace
        :rtype: :class:`Workspace`
        """
        if org_id:
            settings.org_id = org_id
        data = settings.update_or_create()
        url = self.ep()
        data = await self.post(url, data=data)
        return Workspace.parse_obj(data)

    async def details(self, workspace_id) -> Workspace:
        """
        Get Workspace Details

        Shows details for a workspace, by ID. The workspaceLocationId, floorId, capacity, type and notes fields will
        only be present if they have been set for the workspace.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :return: workspace details
        :rtype: :class:`Workspace`
        """
        url = self.ep(workspace_id)
        return Workspace.parse_obj(await self.get(url))

    async def update(self, *, workspace_id, settings: Workspace) -> Workspace:
        """
        Update a Workspace

        Updates details for a workspace, by ID. Specify the workspace ID in the workspaceId parameter in the URI.
        Include all details for the workspace that are present in a GET request for the workspace details. Not
        including the optional capacity, type or notes fields will result in the fields no longer being defined
        for the workspace. A workspaceLocationId must be provided when the floorId is set. The workspaceLocationId,
        floorId, calendar and calling fields do not change when omitted from the update request. Updating the
        calling parameter is not supported.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :param settings: new workspace settings
        :type settings: :class:`Workspace`
        :return: updated workspace
        :rtype: :class:`Workspace`
        """
        url = self.ep(workspace_id)
        j_data = settings.update_or_create(for_update=True)
        data = await self.put(url, data=j_data)
        return Workspace.parse_obj(data)

    async def delete_workspace(self, workspace_id):
        """
        Delete a Workspace

        Deletes a workspace, by ID. Will also delete all devices associated with the workspace. Any deleted devices
        will need to be reactivated.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        """
        url = self.ep(workspace_id)
        await self.delete(url)


@dataclass(init=False)
class AsWebexSimpleApi:
    """
    The main API object
    """

    #: groups API :class:`AsGroupsApi`
    groups: AsGroupsApi
    #: Licenses API :class:`AsLicensesApi`
    licenses: AsLicensesApi
    #: Location API :class:`AsLocationsApi`
    locations: AsLocationsApi
    #: Person settings API :class:`AsPersonSettingsApi`
    person_settings: AsPersonSettingsApi
    #: People API :class:`AsPeopleApi`
    people: AsPeopleApi
    #: Telephony (features) API :class:`AsTelephonyApi`
    telephony: AsTelephonyApi
    #: Webhooks API :class:`AsWebhookApi`
    webhook: AsWebhookApi
    #: Workspaces API :class:`AsWorkspacesApi`
    workspaces: AsWorkspacesApi
    #: Workspace setting API :class:`AsWorkspaceSettingsApi`
    workspace_settings: AsWorkspaceSettingsApi
    #: :class:`AsRestSession` used for all API requests
    session: AsRestSession

    def __init__(self, *, tokens: Union[str, Tokens] = None, concurrent_requests: int = 10):
        """

        :param tokens: token to be used by the API. Can be a :class:`tokens.Tokens` instance, a string or None. If
            None then an access token is expected in the WEBEX_ACCESS_TOKEN environment variable.
        :param concurrent_requests: number of concurrent requests when using multi-threading
        :type concurrent_requests: int
        """
        if isinstance(tokens, str):
            tokens = Tokens(access_token=tokens)
        elif tokens is None:
            tokens = os.getenv('WEBEX_ACCESS_TOKEN')
            if tokens is None:
                raise ValueError('if no access token is passed, then a valid access token has to be present in '
                                 'WEBEX_ACCESS_TOKEN environment variable')
            tokens = Tokens(access_token=tokens)

        session = AsRestSession(tokens=tokens, concurrent_requests=concurrent_requests)
        self.groups = AsGroupsApi(session=session)
        self.licenses = AsLicensesApi(session=session)
        self.locations = AsLocationsApi(session=session)
        self.person_settings = AsPersonSettingsApi(session=session)
        self.people = AsPeopleApi(session=session)
        self.telephony = AsTelephonyApi(session=session)
        self.webhook = AsWebhookApi(session=session)
        self.workspaces = AsWorkspacesApi(session=session)
        self.workspace_settings = AsWorkspaceSettingsApi(session=session)
        self.session = session

    @property
    def access_token(self) -> str:
        """
        access token used for all requests

        :return: access token
        :rtype: str
        """
        return self.session.access_token

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
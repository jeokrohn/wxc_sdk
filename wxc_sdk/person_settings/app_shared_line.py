from collections.abc import Generator
from typing import Union

from wxc_sdk.api_child import ApiChild
from wxc_sdk.telephony.devices import AvailableMember, DeviceMembersResponse, DeviceMember

__all__ = ['AppSharedLineApi']


class AppSharedLineApi(ApiChild, base='telephony/config/people'):
    """
    Webex app shared line API
    """

    def f_ep(self, person_id: str, application_id: str, path: str) -> str:
        """

        :meta private:
        """
        return super().ep(f'{person_id}/applications/{application_id}/{path}')

    def search_members(self, person_id: str, order: str = None, location: str = None,
                       name: str = None, phone_number: str = None, extension: str = None,
                       **params) -> Generator[AvailableMember, None, None]:
        """
        Search Shared-Line Appearance Members

        Get members available for shared-line assignment to a Webex Calling Apps.

        Like most hardware devices, applications support assigning additional shared lines which can monitored and
        utilized by the application.

        This API requires a full, user, or location administrator auth token with the
        `spark-admin:telephony_config_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param order: Order the Route Lists according to number, ascending or descending.
        :type order: str
        :param location: Location ID for the user.
        :type location: str
        :param name: Search for users with names that match the query.
        :type name: str
        :param phone_number: Search for users with numbers that match the query.
        :type phone_number: str
        :param extension: Search for users with extensions that match the query.
        :type extension: str
        :return: Generator yielding :class:`AvailableSharedLineMember` instances
        """
        if order is not None:
            params['order'] = order
        if location is not None:
            params['location'] = location
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'{person_id}/applications/availableMembers')
        return self.session.follow_pagination(url=url, model=AvailableMember,
                                              item_key='members', params=params)

    def search_members_old(self, person_id: str, application_id: str, max_: str = None,
                           start: str = None, location: str = None, name: str = None,
                           number: str = None, order: str = None,
                           extension: str = None, **params) -> Generator[AvailableMember, None, None]:
        """
        Search Shared-Line Appearance Members

        Get members available for shared-line assignment to a Webex Calling Apps Desktop device.

        Deprecated: This operation has been marked as deprecated, which means it could be removed at some point in the
        future.

        This API requires a full or user administrator or location administrator auth token with
        the `spark-admin:people_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :param max_: Number of records per page.
        :type max_: str
        :param start: Page number.
        :type start: str
        :param location: Location ID for the user.
        :type location: str
        :param name: Search for users with names that match the query.
        :type name: str
        :param number: Search for users with numbers that match the query.
        :type number: str
        :param order: Sort by first name (`fname`) or last name (`lname`).
        :type order: str
        :param extension: Search for users with extensions that match the query.
        :type extension: str
        :return: Generator yielding :class:`AvailableMember` instances
        """
        if max_ is not None:
            params['max'] = max_
        if start is not None:
            params['start'] = start
        if location is not None:
            params['location'] = location
        if name is not None:
            params['name'] = name
        if number is not None:
            params['number'] = number
        if order is not None:
            params['order'] = order
        if extension is not None:
            params['extension'] = extension
        url = self.f_ep(person_id=person_id, application_id=application_id, path='availableMembers')
        return self.session.follow_pagination(url, model=AvailableMember, params=params, item_key='members')

    def get_members(self, person_id: str) -> DeviceMembersResponse:
        """
        Get Shared-Line Appearance Members

        Get primary and secondary members assigned to a shared line on a Webex Calling Apps.

        Like most hardware devices, applications support assigning additional shared lines which can monitored and
        utilized by the application.

        This API requires a full, user, or location administrator auth token with the
        `spark-admin:telephony_config_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :rtype: :class:`DeviceMembersResponse`
        """
        url = self.ep(f'{person_id}/applications/members')
        data = super().get(url)
        r = DeviceMembersResponse.model_validate(data)
        return r

    def update_members(self, person_id: str,
                       members: list[Union[DeviceMember, AvailableMember]] = None):
        """
        Put Shared-Line Appearance Members New

        Add or modify primary and secondary users assigned to shared-lines on a Webex Calling Apps.

        Like most hardware devices, applications support assigning additional shared lines which can monitored and
        utilized by the application.

        This API requires a full, user, or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param members: List of members to be added or modified for shared-line assignment to a Webex Calling Apps.
        :type members: list[Union[DeviceMember, AvailableMember]]
        :rtype: None
        """
        members_for_update = []
        for member in members or []:
            if isinstance(member, AvailableMember):
                member = DeviceMember.from_available(member)
            else:
                member = member.model_copy(deep=True)
            members_for_update.append(member)

        if members_for_update:
            # now assign port indices
            port = 1
            for member in members_for_update:
                member.port = port
                port += member.line_weight

        # create body
        if members_for_update:
            members = [m.model_dump(mode='json', exclude_none=True, by_alias=True,
                                    include={'member_id', 'port',
                                             'primary_owner', 'line_type', 'line_weight', 'line_label',
                                             'allow_call_decline_enabled'})
                       for m in members_for_update]
            body = {'members': members}
        else:
            body = None

        url = self.ep(f'{person_id}/applications/members')
        super().put(url, json=body)

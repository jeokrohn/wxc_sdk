from collections.abc import Generator

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.telephony.devices import MemberCommon, DeviceMembersResponse, DeviceMember


class AppSharedLineApi(ApiChild, base='telephony/config/people'):
    """
    Webex app shared line API
    """

    def f_ep(self, person_id: str, application_id: str, path: str) -> str:
        """

        :meta private:
        """
        return super().ep(f'{person_id}/applications/{application_id}/{path}')

    def search_members(self, person_id: str, application_id: str, max_: str = None,
                       start: str = None, location: str = None, name: str = None,
                       number: str = None, order: str = None,
                       extension: str = None, **params) -> Generator[MemberCommon, None, None]:
        """
        Search Shared-Line Appearance Members

        Get members available for shared-line assignment to a Webex Calling Apps Desktop device.

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
        :return: Generator yielding :class:`MemberCommon` instances
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
        return self.session.follow_pagination(url, model=MemberCommon, params=params, item_key='members')

    def get_members(self, person_id: str, application_id: str) -> DeviceMembersResponse:
        """
        Get Shared-Line Appearance Members

        Get primary and secondary members assigned to a shared line on a Webex Calling Apps Desktop device.

        This API requires a full or user administrator or location administrator auth token with
        the `spark-admin:people_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :rtype: :class:`GetSharedLineMemberList`
        """
        url = self.f_ep(person_id=person_id, application_id=application_id, path='members')
        data = super().get(url)
        r = DeviceMembersResponse.model_validate(data)
        return r

    def update_members(self, person_id: str, application_id: str,
                       members: list[DeviceMember] = None):
        """
        Put Shared-Line Appearance Members

        Add or modify primary and secondary users assigned to shared-lines on a Webex Calling Apps Desktop device.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :type members: list[DeviceMember]
        :rtype: None
        """
        body = dict()
        if members is not None:
            body['members'] = TypeAdapter(list[DeviceMember]).dump_python(members, mode='json', by_alias=True,
                                                                          exclude_none=True)
        url = self.f_ep(person_id=person_id, application_id=application_id, path='members')
        super().put(url, json=body)

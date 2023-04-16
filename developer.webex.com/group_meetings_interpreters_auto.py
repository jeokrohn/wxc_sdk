from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Api', 'CreateMeetingInterpreterBody', 'CreateMeetingInterpreterResponse',
           'ListMeetingInterpretersResponse']


class CreateMeetingInterpreterResponse(ApiModel):
    #: Unique identifier for meeting interpreter.
    id: Optional[str]
    #: The pair of languageCode1 and languageCode2 form a bi-directional simultaneous interpretation language channel.
    #: The language codes conform with ISO 639-1.
    language_code1: Optional[str]
    #: The pair of languageCode1 and languageCode2 form a bi-directional simultaneous interpretation language channel.
    #: The language codes conform with ISO 639-1.
    language_code2: Optional[str]
    #: Email address of meeting interpreter.
    email: Optional[str]
    #: Display name of meeting interpreter.
    display_name: Optional[str]


class CreateMeetingInterpreterBody(ApiModel):
    #: The pair of languageCode1 and languageCode2 form a bi-directional simultaneous interpretation language channel.
    #: The language codes conform with ISO 639-1.
    language_code1: Optional[str]
    #: The pair of languageCode1 and languageCode2 form a bi-directional simultaneous interpretation language channel.
    #: The language codes conform with ISO 639-1.
    language_code2: Optional[str]
    #: Email address of meeting interpreter. If not specified, an empty interpreter will be created for this
    #: bi-directional language channel, and a specific email can be assigned to this empty interpreter by Update a
    #: Meeting Interpreter API later. Please note that multiple interpreters with different emails can be assigned to
    #: the same bi-directional language channel, but the same email cannot be assigned to more than one interpreter.
    email: Optional[str]
    #: Display name of meeting interpreter. If the interpreter is already an invitee of the meeting and it has a
    #: different display name, that invitee's display name will be overwritten by this attribute.
    display_name: Optional[str]
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage to
    #: be the meeting host.
    host_email: Optional[str]
    #: If true, send email to the interpreter.
    send_email: Optional[bool]


class ListMeetingInterpretersResponse(ApiModel):
    #: Array of meeting interpreters.
    items: Optional[list[CreateMeetingInterpreterResponse]]


class Api(ApiChild, base='meetings/'):
    """

    """

    def create_interpreter(self, meeting_id: str, language_code1: str, language_code2: str, email: str = None, display_name: str = None, host_email: str = None, send_email: bool = None) -> CreateMeetingInterpreterResponse:
        """
        Assign an interpreter to a bi-directional simultaneous interpretation language channel for a meeting.

        :param meeting_id: Unique identifier for the meeting to which the interpreter is to be assigned.
        :type meeting_id: str
        :param language_code1: The pair of languageCode1 and languageCode2 form a bi-directional simultaneous
            interpretation language channel. The language codes conform with ISO 639-1.
        :type language_code1: str
        :param language_code2: The pair of languageCode1 and languageCode2 form a bi-directional simultaneous
            interpretation language channel. The language codes conform with ISO 639-1.
        :type language_code2: str
        :param email: Email address of meeting interpreter. If not specified, an empty interpreter will be created for
            this bi-directional language channel, and a specific email can be assigned to this empty interpreter by
            Update a Meeting Interpreter API later. Please note that multiple interpreters with different emails can be
            assigned to the same bi-directional language channel, but the same email cannot be assigned to more than
            one interpreter.
        :type email: str
        :param display_name: Display name of meeting interpreter. If the interpreter is already an invitee of the
            meeting and it has a different display name, that invitee's display name will be overwritten by this
            attribute.
        :type display_name: str
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param send_email: If true, send email to the interpreter.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/create-a-meeting-interpreter
        """
        body = CreateMeetingInterpreterBody()
        if language_code1 is not None:
            body.language_code1 = language_code1
        if language_code2 is not None:
            body.language_code2 = language_code2
        if email is not None:
            body.email = email
        if display_name is not None:
            body.display_name = display_name
        if host_email is not None:
            body.host_email = host_email
        if send_email is not None:
            body.send_email = send_email
        url = self.ep(f'{meeting_id}/interpreters')
        data = super().post(url=url, data=body.json())
        return CreateMeetingInterpreterResponse.parse_obj(data)

    def interpreter(self, meeting_id: str, interpreter_id: str, host_email: str = None) -> CreateMeetingInterpreterResponse:
        """
        Retrieves details for a meeting interpreter identified by meetingId and interpreterId in the URI.

        :param meeting_id: Unique identifier for the meeting to which the interpreter has been assigned.
        :type meeting_id: str
        :param interpreter_id: Unique identifier for the interpreter whose details are being requested.
        :type interpreter_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return details for an interpreter of the meeting that is hosted by that
            user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-interpreter
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}/interpreters/{interpreter_id}')
        data = super().get(url=url, params=params)
        return CreateMeetingInterpreterResponse.parse_obj(data)

    def list_interpreters(self, meeting_id: str, host_email: str = None) -> list[CreateMeetingInterpreterResponse]:
        """
        Lists meeting interpreters for a meeting with a specified meetingId.
        This operation can be used for meeting series, scheduled meeting and ended or ongoing meeting instance objects.
        If the specified meetingId is for a meeting series, the interpreters for the series will be listed; if the
        meetingId is for a scheduled meeting, the interpreters for the particular scheduled meeting will be listed; if
        the meetingId is for an ended or ongoing meeting instance, the interpreters for the particular meeting instance
        will be listed. See the Webex Meetings guide for more information about the types of meetings.
        The list returned is sorted in descending order by when interpreters were created.

        :param meeting_id: Unique identifier for the meeting for which interpreters are being requested. The meeting
            can be meeting series, scheduled meeting or meeting instance which has ended or is ongoing. Please note
            that currently meeting ID of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return interpreters of the meeting that is hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-interpreters
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}/interpreters')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[CreateMeetingInterpreterResponse], data["items"])

    def update_interpreter(self, meeting_id: str, interpreter_id: str, language_code1: str, language_code2: str, email: str = None, display_name: str = None, host_email: str = None, send_email: bool = None) -> CreateMeetingInterpreterResponse:
        """
        Updates details for a meeting interpreter identified by meetingId and interpreterId in the URI.

        :param meeting_id: Unique identifier for the meeting whose interpreters were belong to.
        :type meeting_id: str
        :param interpreter_id: Unique identifier for the interpreter whose details are being requested.
        :type interpreter_id: str
        :param language_code1: The pair of languageCode1 and languageCode2 form a bi-directional simultaneous
            interpretation language channel. The language codes conform with ISO 639-1.
        :type language_code1: str
        :param language_code2: The pair of languageCode1 and languageCode2 form a bi-directional simultaneous
            interpretation language channel. The language codes conform with ISO 639-1.
        :type language_code2: str
        :param email: Email address of meeting interpreter. If not specified, an empty interpreter will be created for
            this bi-directional language channel, and a specific email can be assigned to this empty interpreter by
            Update a Meeting Interpreter API later. Please note that multiple interpreters with different emails can be
            assigned to the same bi-directional language channel, but the same email cannot be assigned to more than
            one interpreter.
        :type email: str
        :param display_name: Display name of meeting interpreter. If the interpreter is already an invitee of the
            meeting and it has a different display name, that invitee's display name will be overwritten by this
            attribute.
        :type display_name: str
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param send_email: If true, send email to the interpreter.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-a-meeting-interpreter
        """
        body = CreateMeetingInterpreterBody()
        if language_code1 is not None:
            body.language_code1 = language_code1
        if language_code2 is not None:
            body.language_code2 = language_code2
        if email is not None:
            body.email = email
        if display_name is not None:
            body.display_name = display_name
        if host_email is not None:
            body.host_email = host_email
        if send_email is not None:
            body.send_email = send_email
        url = self.ep(f'{meeting_id}/interpreters/{interpreter_id}')
        data = super().put(url=url, data=body.json())
        return CreateMeetingInterpreterResponse.parse_obj(data)

    def delete_interpreter(self, meeting_id: str, interpreter_id: str, host_email: str = None, send_email: bool = None):
        """
        Removes a meeting interpreter identified by meetingId and interpreterId in the URI. The deleted meeting
        interpreter cannot be recovered.

        :param meeting_id: Unique identifier for the meeting whose interpreters were belong to.
        :type meeting_id: str
        :param interpreter_id: Unique identifier for the interpreter to be removed.
        :type interpreter_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will delete an interpreter of the meeting that is hosted by that user.
        :type host_email: str
        :param send_email: If true, send email to the interpreter.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-a-meeting-interpreter
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if send_email is not None:
            params['sendEmail'] = str(send_email).lower()
        url = self.ep(f'{meeting_id}/interpreters/{interpreter_id}')
        super().delete(url=url, params=params)
        return


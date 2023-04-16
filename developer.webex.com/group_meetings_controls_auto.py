from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Api', 'GetMeetingControlStatusResponse']


class GetMeetingControlStatusResponse(ApiModel):
    #: Whether the meeting is locked or not.
    locked: Optional[bool]
    #: The value can be true or false, it indicates the meeting recording started or not.
    recording_started: Optional[bool]
    #: The value can be true or false, it indicates the meeting recording paused or not.
    recording_paused: Optional[bool]


class Api(ApiChild, base='meetings/controls'):
    """

    """

    def control_status(self, meeting_id: str) -> GetMeetingControlStatusResponse:
        """
        Get the meeting control of a live meeting, which is consisted of meeting control status on "locked" and
        "recording" to reflect whether the meeting is currently locked and there is recording in progress.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-meeting-control-status
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep()
        data = super().get(url=url, params=params)
        return GetMeetingControlStatusResponse.parse_obj(data)

    def update_control_status(self, meeting_id: str, locked: bool = None, recording_started: bool = None, recording_paused: bool = None) -> GetMeetingControlStatusResponse:
        """
        To start, pause, resume, or stop a meeting recording; To lock or unlock an on-going meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param locked: Whether the meeting is locked or not.
        :type locked: bool
        :param recording_started: The value can be true or false, it indicates the meeting recording started or not.
        :type recording_started: bool
        :param recording_paused: The value can be true or false, it indicates the meeting recording paused or not.
        :type recording_paused: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-meeting-control-status
        """
        params = {}
        params['meetingId'] = meeting_id
        body = GetMeetingControlStatusResponse()
        if locked is not None:
            body.locked = locked
        if recording_started is not None:
            body.recording_started = recording_started
        if recording_paused is not None:
            body.recording_paused = recording_paused
        url = self.ep()
        data = super().put(url=url, params=params, data=body.json())
        return GetMeetingControlStatusResponse.parse_obj(data)


from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CallMembership', 'CallMembershipAudio', 'CallMembershipCollectionResponse', 'CallMembershipStatus']


class CallMembershipStatus(str, Enum):
    notified = 'notified'
    joined = 'joined'
    declined = 'declined'
    left = 'left'
    waiting = 'waiting'


class CallMembershipAudio(str, Enum):
    on = 'on'
    off = 'off'


class CallMembership(ApiModel):
    #: A unique identifier for the call membership.
    #: example: Y2lzY29zcGFyazovL3VzL01FTUJFUlNISVAvMGQwYzkxYjYtY2U2MC00NzI1LWI2ZDAtMzQ1NWQ1ZDExZWYzOmNkZTFkZDQwLTJmMGQtMTFlNS1iYTljLTdiNjU1NmQyMjA3Yg
    id: Optional[str] = None
    #: The status of the call membership.
    #: example: joined
    status: Optional[CallMembershipStatus] = None
    #: The call ID.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExTLzU0MUFFMzBFLUUyQzUtNERENi04NTM4LTgzOTRDODYzM0I3MQo
    callId: Optional[str] = None
    #: Whether or not the person referenced by this membership hosted the call.
    #: example: True
    isHost: Optional[bool] = None
    #: The fully qualified SIP address of the participant, if not a known Webex user.
    #: example: sip:john.andersen@example.com
    sipUrl: Optional[str] = None
    #: The E.164 PSTN address of the participant, if not a known Webex user.
    #: example: +14155551212
    phoneNumber: Optional[str] = None
    #: The room ID of the call.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    roomId: Optional[str] = None
    #: List of device IDs associated to the participant.
    #: example: ['22ecb593-8408-4fe5-81bb-0d92d568f93f', '2345aea8-7a8b-4861-982a-26c792e21c17']
    deviceIds: Optional[list[str]] = None
    #: Whether or not the participant is in the same organization.
    isGuest: Optional[bool] = None
    #: The organization ID of the participant if they are a guest.
    #: example: ``
    orgId: Optional[str] = None
    #: The total amount of time, in seconds, that the membership was in a "joined" state.
    #: example: 180.0
    joinedDuration: Optional[int] = None
    #: The current status of the audio stream.
    #: example: on
    audio: Optional[CallMembershipAudio] = None
    #: The current status of the video stream.
    #: example: on
    video: Optional[CallMembershipAudio] = None
    #: The current status of the whiteboard stream.
    #: example: off
    slide: Optional[CallMembershipAudio] = None
    #: The date and time when the call membership was created.
    #: example: 2015-10-18T14:26:16.203Z
    created: Optional[datetime] = None


class CallMembershipCollectionResponse(ApiModel):
    items: Optional[list[CallMembership]] = None

from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CallForwardingPut', 'CallForwardingPutCallForwarding', 'CallForwardingPutCallForwardingAlways', 'CallForwardingPutCallForwardingBusy', 'CallForwardingPutCallForwardingNoAnswer']


class CallForwardingPutCallForwardingAlways(ApiModel):
    #: "Always" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "Always" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingPutCallForwardingBusy(ApiModel):
    #: "Busy" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "Busy" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Indicates the enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingPutCallForwardingNoAnswer(ApiModel):
    #: "No Answer" call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
    #: example: 3.0
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    #: example: 15.0
    system_max_number_of_rings: Optional[int] = None
    #: Indicates the enabled or disabled state of sending incoming calls to destination number's voicemail if the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingPutCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardingPutCallForwardingAlways] = None
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the person is busy.
    busy: Optional[CallForwardingPutCallForwardingBusy] = None
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[CallForwardingPutCallForwardingNoAnswer] = None


class CallForwardingPut(ApiModel):
    #: Settings related to "Always", "Busy", and "No Answer" call forwarding.
    call_forwarding: Optional[CallForwardingPutCallForwarding] = None
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[CallForwardingPutCallForwardingBusy] = None

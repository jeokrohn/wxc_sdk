from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetComplianceAnnouncementObject', 'GetOrgComplianceAnnouncementObject']


class GetComplianceAnnouncementObject(ApiModel):
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an inbound caller.
    #: example: True
    inboundPSTNCallsEnabled: Optional[bool] = None
    #: Flag to indicate whether to use the customer level compliance announcement default settings.
    #: example: True
    useOrgSettingsEnabled: Optional[bool] = None
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an outbound caller.
    outboundPSTNCallsEnabled: Optional[bool] = None
    #: Flag to indicate whether compliance announcement is played after a specified delay in seconds.
    outboundPSTNCallsDelayEnabled: Optional[bool] = None
    #: Number of seconds to wait before playing the compliance announcement.
    #: example: 10.0
    delayInSeconds: Optional[int] = None


class GetOrgComplianceAnnouncementObject(ApiModel):
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an inbound caller.
    #: example: True
    inboundPSTNCallsEnabled: Optional[bool] = None
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an outbound caller.
    outboundPSTNCallsEnabled: Optional[bool] = None
    #: Flag to indicate whether compliance announcement is played after a specified delay in seconds.
    outboundPSTNCallsDelayEnabled: Optional[bool] = None
    #: Number of seconds to wait before playing the compliance announcement.
    #: example: 10.0
    delayInSeconds: Optional[int] = None

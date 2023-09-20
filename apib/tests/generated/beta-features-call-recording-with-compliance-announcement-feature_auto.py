from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetComplianceAnnouncementObject']


class GetComplianceAnnouncementObject(ApiModel):
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an internal caller.
    #: example: True
    inboundPSTNCallsEnabled: Optional[bool] = None

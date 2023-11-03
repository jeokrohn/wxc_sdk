from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CallBridgeInfo']


class CallBridgeInfo(ApiModel):
    #: Indicates that a stutter dial tone will be played to all the participants when a person is bridged on the active
    #: shared line call.
    warning_tone_enabled: Optional[bool] = None

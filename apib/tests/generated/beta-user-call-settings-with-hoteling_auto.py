from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['HotelingRequest', 'UserHotelingRequestPatch']


class HotelingRequest(ApiModel):
    #: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can log into this host(workspace device) and use this device
    #: as if it were their own. This is useful for employees who travel to remote offices and need to make and receive calls using their office phone number and access features that are normally available on their office phone.
    enabled: Optional[bool] = None
    #: Enable limiting the time a guest can use the device. The time limit is configured via `guestHoursLimit`.
    limit_guest_use: Optional[bool] = None
    #: Time limit, in hours, until the hoteling reservation expires.
    guest_hours_limit: Optional[int] = None


class UserHotelingRequestPatch(ApiModel):
    #: Modify person Device Hoteling Setting.
    hoteling: Optional[HotelingRequest] = None

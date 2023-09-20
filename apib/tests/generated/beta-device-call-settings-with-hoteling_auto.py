from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ActivationStates', 'DeviceList', 'DeviceOwner', 'Devices', 'HotelingRequest', 'LineType', 'MemberType']


class ActivationStates(str, Enum):
    #: Indicates a device is activating.
    activating = 'ACTIVATING'
    #: Indicates a device is activated.
    activated = 'ACTIVATED'
    #: Indicates a device is deactivated.
    deactivated = 'DEACTIVATED'


class HotelingRequest(ApiModel):
    #: Enable/Disable hoteling Host. Enabling the device for hoteling means that a guest(end user) can log into this host(workspace device) and use this device
    #: as if it were their own. This is useful for employees who travel to remote offices and need to make and receive calls using their office phone number and access features that are normally available on their office phone.
    enabled: Optional[bool] = None
    #: Enable limiting the time a guest can use the device. The time limit is configured via `guestHoursLimit`.
    limitGuestUse: Optional[bool] = None
    #: Time limit, in hours, until the hoteling reservation expires.
    guestHoursLimit: Optional[int] = None


class LineType(str, Enum):
    #: Primary line for the member.
    primary = 'PRIMARY'
    #: Shared line for the member. A shared line allows a person to receive and place calls to and from another user's extension, using their own device.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'


class MemberType(str, Enum):
    #: Indicates the associated member is a person.
    people = 'PEOPLE'
    #: Indicates the associated member is a workspace.
    place = 'PLACE'


class DeviceOwner(ApiModel):
    #: Unique identifier of a person or a workspace.
    id: Optional[str] = None
    #: Enumeration that indicates if the member is of type `PEOPLE` or `PLACE`.
    type: Optional[MemberType] = None
    #: First name of device owner.
    firstName: Optional[str] = None
    #: Last name of device owner.
    lastName: Optional[str] = None


class Devices(ApiModel):
    #: Unique identifier for a device.
    id: Optional[str] = None
    #: Comma separated array of tags used to describe device.
    description: Optional[list[str]] = None
    #: Identifier for device model.
    model: Optional[str] = None
    #: MAC address of device.
    mac: Optional[str] = None
    #: IP address of device.
    ipAddress: Optional[str] = None
    #: Indicates whether the person or the workspace is the owner of the device, and points to a primary Line/Port of the device.
    primaryOwner: Optional[bool] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    type: Optional[LineType] = None
    #: Hoteling settings, which are available when the device is the user's primary device and device type is PRIMARY
    hoteling: Optional[HotelingRequest] = None
    #: Owner of device.
    owner: Optional[DeviceOwner] = None
    #: Activation state of device.
    activationState: Optional[ActivationStates] = None


class DeviceList(ApiModel):
    #: Array of devices available to person.
    devices: Optional[list[Devices]] = None
    #: Maximum number of devices a person can be assigned to.
    maxDeviceCount: Optional[int] = None

from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetMemberResponse', 'LineType', 'Location', 'MemberObject', 'MemberType', 'SearchMemberObject',
            'SearchMemberResponse']


class LineType(str, Enum):
    #: Indicates a Primary line for the member.
    primary = 'PRIMARY'
    #: Indicates a Shared line for the member. Shared line appearance allows users to receive and place calls to and
    #: from another user's extension, using their device.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'


class MemberType(str, Enum):
    #: Indicates the associated member is a person.
    people = 'PEOPLE'
    #: Indicates the associated member is a workspace.
    place = 'PLACE'


class Location(ApiModel):
    #: Location identifier associated with the members.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzJiNDkyZmZkLTRjNGItNGVmNS04YzAzLWE1MDYyYzM4NDA5Mw
    id: Optional[str] = None
    #: Location name associated with the member.
    #: example: MainOffice
    name: Optional[str] = None


class MemberObject(ApiModel):
    #: Unique identifier for the member.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: First name of a person or workspace.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of a person or workspace.
    #: example: Smith
    last_name: Optional[str] = None
    #: Phone Number of a person or workspace. In some regions phone numbers are not returned in E.164 format. This will
    #: be supported in a future update.
    #: example: 2055552221
    phone_number: Optional[str] = None
    #: Extension of a person or workspace.
    #: example: 000
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 1234000
    esn: Optional[str] = None
    #: This field indicates whether the person or the workspace is the owner of the device, and points to a primary
    #: Line/Port of the device.
    #: example: True
    primary_owner: Optional[bool] = None
    #: Port number assigned to person or workspace.
    #: example: 1
    port: Optional[int] = None
    #: T.38 Fax Compression setting and is available only for ATA Devices. Choose T.38 fax compression if the device
    #: requires this option. This will override user level compression options.
    t38_fax_compression_enabled: Optional[bool] = None
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    #: example: 1
    line_weight: Optional[int] = None
    #: Registration Host IP address for the line port.
    #: example: 10.0.0.45
    host_ip: Optional[str] = Field(alias='hostIP', default=None)
    #: Registration Remote IP address for the line port.
    #: example: 192.102.12.84
    remote_ip: Optional[str] = Field(alias='remoteIP', default=None)
    #: Enable Hotline. Configure this line to automatically call a predefined number whenever taken off-hook. Once
    #: enabled, the line can only make calls to the predefined number set in hotlineDestination.
    #: example: True
    hotline_enabled: Optional[bool] = None
    #: The preconfigured number for Hotline. Required only if `hotlineEnabled` is set to true.
    #: example: +12055552222
    hotline_destination: Optional[str] = None
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended
    #: to all the endpoints on the device. When set to false, a call decline request only declines the current
    #: endpoint.
    #: example: True
    allow_call_decline_enabled: Optional[bool] = None
    #: Device line label.
    #: example: share line label
    line_label: Optional[str] = None
    #: Indicates if the member is of type `PEOPLE` or `PLACE`.
    member_type: Optional[MemberType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


class GetMemberResponse(ApiModel):
    #: Model type of the device.
    #: example: DMS Cisco 192
    model: Optional[str] = None
    #: List of members that appear on the device.
    members: Optional[list[MemberObject]] = None
    #: Maximum number of lines available for the device.
    #: example: 10
    max_line_count: Optional[int] = None


class SearchMemberObject(ApiModel):
    #: Unique identifier for the member.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: First name of a person or workspace.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of a person or workspace.
    #: example: Smith
    last_name: Optional[str] = None
    #: Phone Number of a person or workspace.
    #: example: +12055552221
    phone_number: Optional[str] = None
    #: T.38 Fax Compression setting and available only for ATA Devices. Choose T.38 fax compression if the device
    #: requires this option. this will override user level compression options.
    t38_fax_compression_enabled: Optional[bool] = None
    #: Line type is used to differentiate Primary and SCA, at which endpoint it is assigned.
    line_type: Optional[LineType] = None
    #: Set how a person's device behaves when a call is declined. When set to true, a call decline request is extended
    #: to all the endpoints on the device. When set to false, a call decline request only declines the current
    #: endpoint.
    #: example: True
    allow_call_decline_enabled: Optional[bool] = None
    #: Indicates if member is of type `PEOPLE` or `PLACE`.
    member_type: Optional[MemberType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


class SearchMemberResponse(ApiModel):
    #: List of members available for the device.
    members: Optional[list[SearchMemberObject]] = None


class BetaDeviceCallSettingsWithESNFeatureApi(ApiChild, base='telephony/config/devices/{deviceId}'):
    """
    Beta Device Call Settings with ESN Feature
    
    These APIs manages Webex Calling settings for devices with are of the Webex Calling type.
    
    Viewing these read-only device settings requires a full, device, or
    read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these device settings requires a full or device
    administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    """

    def get_device_members(self, device_id: str, org_id: str = None) -> GetMemberResponse:
        """
        Get Device Members

        Get the list of all the members of the device including primary and secondary users.

        A device member can be either a person or a workspace. An admin can access the list of member details, modify
        member details and
        search for available members on a device.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Retrieves the list of all members of the device in this organization.
        :type org_id: str
        :rtype: :class:`GetMemberResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'members')
        data = super().get(url, params=params)
        r = GetMemberResponse.model_validate(data)
        return r

    def search_members(self, device_id: str, location_id: str, org_id: str = None, start: int = None,
                       member_name: str = None, phone_number: str = None, extension: Union[str, datetime] = None,
                       **params) -> Generator[SearchMemberObject, None, None]:
        """
        Search Members

        Search members that can be assigned to the device.

        A device member can be either a person or a workspace. A admin can access the list of member details, modify
        member details and
        search for available members on a device.

        This requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param org_id: Retrieves the list of available members on the device in this organization.
        :type org_id: str
        :param start: Specifies the offset from the first result that you want to fetch.
        :type start: int
        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param extension: Search (Contains) based on extension.
        :type extension: Union[str, datetime]
        :return: Generator yielding :class:`SearchMemberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        params['locationId'] = location_id
        if start is not None:
            params['start'] = start
        if member_name is not None:
            params['memberName'] = member_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if extension is not None:
            if isinstance(extension, str):
                extension = isoparse(extension)
            extension = dt_iso_str(extension)
            params['extension'] = extension
        url = self.ep(f'availableMembers')
        return self.session.follow_pagination(url=url, model=SearchMemberObject, item_key='members', params=params)

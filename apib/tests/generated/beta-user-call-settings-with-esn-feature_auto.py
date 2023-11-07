from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AgentAvaliableCallQueueIdList', 'AgentCallQueueId', 'AvailableSharedLineMemberItem',
            'AvailableSharedLineMemberList', 'CallQueueObject', 'GetMonitoredElementsObject',
            'GetMonitoredElementsObjectCallparkextension', 'GetMonitoredElementsObjectMember', 'GetNumbers',
            'GetNumbersPhoneNumbers', 'GetNumbersPhoneNumbersRingPattern', 'GetSharedLineMemberItem',
            'GetSharedLineMemberList', 'LineType', 'Location', 'MonitoredMemberObject', 'MonitoredNumberObject',
            'MonitoringSettings', 'PeopleOrPlaceOrVirtualLineType', 'PrivacyGet', 'PushToTalkAccessType',
            'PushToTalkConnectionType', 'PushToTalkInfo', 'ReceptionInfo', 'UserType']


class CallQueueObject(ApiModel):
    #: Indicates the Call Queue's unique identifier.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvMjE3ZDU3YmEtOTMxYi00ZjczLTk1Y2EtOGY3MWFhYzc4MTE5
    id: Optional[str] = None
    #: Indicates the Call Queue's name.
    #: example: SalesQueue
    name: Optional[str] = None
    #: When not null, indicates the Call Queue's phone number.
    #: example: 4255558100
    phone_number: Optional[str] = None
    #: When not null, indicates the Call Queue's extension number.
    #: example: 8100
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12348100
    esn: Optional[str] = None


class AgentAvaliableCallQueueIdList(ApiModel):
    #: Indicates a list of Call Queues that the agent belongs and are available to be selected as the Caller ID for
    #: outgoing calls. It is empty when the agent's Call Queues have disabled the Call Queue outgoing phone number
    #: setting to be used as Caller ID. In the case where this setting is enabled the array will be populated.
    available_queues: Optional[list[CallQueueObject]] = None


class AgentCallQueueId(ApiModel):
    #: When true, indicates that this agent is using the `selectedQueue` for its Caller ID. When false, indicates that
    #: it is using the agent's configured Caller ID.
    #: example: True
    queue_caller_id_enabled: Optional[bool] = None
    #: Indicates agent's choice of using this queue's Caller ID for outgoing calls. It is empty object when
    #: `queueCallerIdEnabled` is false. When `queueCallerIdEnabled` is true this data must be populated.
    selected_queue: Optional[CallQueueObject] = None


class LineType(str, Enum):
    #: Primary line for the member.
    primary = 'PRIMARY'
    #: Shared line for the member. A shared line allows users to receive and place calls to and from another user's
    #: extension, using their own device.
    shared_call_appearance = 'SHARED_CALL_APPEARANCE'


class Location(ApiModel):
    #: Location identifier associated with the members.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzJiNDkyZmZkLTRjNGItNGVmNS04YzAzLWE1MDYyYzM4NDA5Mw
    id: Optional[str] = None
    #: Location name associated with the member.
    #: example: MainOffice
    name: Optional[str] = None


class AvailableSharedLineMemberItem(ApiModel):
    #: A unique member identifier.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85ODhiYTQyOC0zMjMyLTRmNjItYjUyNS1iZDUzZmI4Nzc0MWE
    id: Optional[str] = None
    #: First name of member.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of member.
    #: example: Doe
    last_name: Optional[str] = None
    #: Phone number of member. Currently, E.164 format is not supported.
    #: example: 1234567890
    phone_number: Optional[str] = None
    #: Phone extension of member.
    #: example: 0000
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12340000
    esn: Optional[str] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    #: example: SHARED_CALL_APPEARANCE
    line_type: Optional[LineType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


class AvailableSharedLineMemberList(ApiModel):
    members: Optional[list[AvailableSharedLineMemberItem]] = None


class UserType(str, Enum):
    #: The associated member is a person.
    people = 'PEOPLE'
    #: The associated member is a workspace.
    place = 'PLACE'


class GetSharedLineMemberItem(ApiModel):
    #: Unique identifier for the member.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85ODhiYTQyOC0zMjMyLTRmNjItYjUyNS1iZDUzZmI4Nzc0MWE
    id: Optional[str] = None
    #: First name of person or workspace.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of person or workspace.
    #: example: Doe
    last_name: Optional[str] = None
    #: Phone number of a person or workspace. Currently, E.164 format is not supported. This will be supported in the
    #: future update.
    #: example: 2056852221
    phone_number: Optional[str] = None
    #: Phone extension of a person or workspace.
    #: example: 1111
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341111
    esn: Optional[datetime] = None
    #: Device port number assigned to a person or workspace.
    #: example: 1.0
    port: Optional[int] = None
    #: T.38 Fax Compression setting. Valid only for ATA Devices. Overrides user level compression options.
    #: example: True
    t38_fax_compression_enabled: Optional[bool] = None
    #: If `true` the person or the workspace is the owner of the device. Points to primary line/port of the device.
    #: example: true
    primary_owner: Optional[str] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    #: example: SHARED_CALL_APPEARANCE
    line_type: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    #: example: 1.0
    line_weight: Optional[int] = None
    #: Registration home IP for the line port.
    #: example: 198.168.0.1
    host_ip: Optional[str] = Field(alias='hostIP', default=None)
    #: Registration remote IP for the line port.
    #: example: 198.168.0.2
    remote_ip: Optional[str] = Field(alias='remoteIP', default=None)
    #: Configure this line to automatically call a predefined number whenever taken off-hook. Once enabled, the line
    #: can only make calls to the predefined number set in hotlineDestination.
    #: example: True
    hotline_enabled: Optional[bool] = None
    #: Preconfigured number for the hotline. Required only if `hotlineEnabled` is set to `true`.
    #: example: 1234
    hotline_destination: Optional[datetime] = None
    #: Set how a device behaves when a call is declined. When set to `true`, a call decline request is extended to all
    #: the endpoints on the device. When set to `false`, a call decline request is only declined at the current
    #: endpoint.
    #: example: True
    allow_call_decline_enabled: Optional[bool] = None
    #: Device line label.
    #: example: share line label
    line_label: Optional[str] = None
    #: Indicates if the member is of type `PEOPLE` or `PLACE`.
    member_type: Optional[UserType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


class GetSharedLineMemberList(ApiModel):
    #: Model name of device.
    #: example: Business Communicator - PC
    model: Optional[str] = None
    #: List of members.
    members: Optional[list[GetSharedLineMemberItem]] = None
    #: Maximum number of device ports.
    #: example: 10.0
    max_line_count: Optional[int] = None


class PeopleOrPlaceOrVirtualLineType(str, Enum):
    #: Indicates a person or list of people.
    people = 'PEOPLE'
    #: Indicates a workspace that is not assigned to a specific person such as for a shared device in a common area.
    place = 'PLACE'
    #: Indicates a virtual line or list of virtual lines.
    virtual_line = 'VIRTUAL_LINE'


class MonitoredNumberObject(ApiModel):
    #: External phone number of the monitored person, workspace or virtual line.
    #: example: +19845551088
    external: Optional[str] = None
    #: Extension number of the monitored person, workspace or virtual line.
    #: example: 1088
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341088
    esn: Optional[str] = None
    #: Indicates whether phone number is a primary number.
    #: example: True
    primary: Optional[bool] = None


class GetMonitoredElementsObjectMember(ApiModel):
    #: The identifier of the monitored person.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS85OWNlZjRmYS03YTM5LTQ1ZDItOTNmNi1jNjA5YTRiMjgzODY
    id: Optional[str] = None
    #: The last name of the monitored person, place or virtual line.
    #: example: Nelson
    last_name: Optional[str] = None
    #: The first name of the monitored person, place or virtual line.
    #: example: John
    first_name: Optional[str] = None
    #: The display name of the monitored person, place or virtual line.
    #: example: John Nelson
    display_name: Optional[str] = None
    #: Indicates whether the type is `PEOPLE`, `PLACE` or `VIRTUAL_LINE`.
    type: Optional[PeopleOrPlaceOrVirtualLineType] = None
    #: The email address of the monitored person, place or virtual line.
    #: example: john.nelson@gmail.com
    email: Optional[str] = None
    #: The list of phone numbers of the monitored person, place or virtual line.
    numbers: Optional[list[MonitoredNumberObject]] = None
    #: The location name where the call park extension is.
    #: example: Dallas
    location: Optional[str] = None
    #: The ID for the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzZhZjk4ZGViLWVlZGItNGFmYi1hMDAzLTEzNzgyYjdjODAxYw
    location_id: Optional[str] = None


class GetMonitoredElementsObjectCallparkextension(ApiModel):
    #: The identifier of the call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUEFSS19FWFRFTlNJT04vZTdlZDdiMDEtN2E4Ni00NDEwLWFlODMtOWJmODMzZGEzNzQy
    id: Optional[str] = None
    #: The name used to describe the call park extension.
    #: example: Dallas-Test
    name: Optional[str] = None
    #: The extension number for the call park extension.
    #: example: 4001
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12344001
    esn: Optional[str] = None
    #: The location name where the call park extension is.
    #: example: Dallas
    location: Optional[str] = None
    #: The ID for the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzZhZjk4ZGViLWVlZGItNGFmYi1hMDAzLTEzNzgyYjdjODAxYw
    location_id: Optional[str] = None


class GetMonitoredElementsObject(ApiModel):
    member: Optional[GetMonitoredElementsObjectMember] = None
    callparkextension: Optional[GetMonitoredElementsObjectCallparkextension] = None


class GetNumbersPhoneNumbersRingPattern(str, Enum):
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a long ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class GetNumbersPhoneNumbers(ApiModel):
    #: Flag to indicate if the number is primary or not.
    #: example: True
    primary: Optional[bool] = None
    #: Phone number.
    #: example: 2143456789
    direct_number: Optional[str] = None
    #: Extension.
    #: example: 1234
    extension: Optional[datetime] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341234
    esn: Optional[str] = None
    #: Optional ring pattern. Applicable only for alternate numbers.
    #: example: NORMAL
    ring_pattern: Optional[GetNumbersPhoneNumbersRingPattern] = None


class GetNumbers(ApiModel):
    #: Enable/disable a distinctive ring pattern that identifies calls coming from a specific phone number.
    #: example: True
    distinctive_ring_enabled: Optional[bool] = None
    #: Information about the number.
    phone_numbers: Optional[list[GetNumbersPhoneNumbers]] = None


class MonitoredMemberObject(ApiModel):
    #: Unique identifier of the person, workspace or virtual line to be monitored.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
    id: Optional[str] = None
    #: Last name of the monitored person, workspace or virtual line.
    #: example: Little
    last_name: Optional[str] = None
    #: First name of the monitored person, workspace or virtual line.
    #: example: Alice
    first_name: Optional[str] = None
    #: Display name of the monitored person, workspace or virtual line.
    #: example: Alice Little
    display_name: Optional[str] = None
    #: Indicates whether type is person, workspace or virtual line.
    type: Optional[PeopleOrPlaceOrVirtualLineType] = None
    #: Email address of the monitored person, workspace or virtual line.
    #: example: alice@example.com
    email: Optional[str] = None
    #: List of phone numbers of the monitored person, workspace or virtual line.
    numbers: Optional[list[MonitoredNumberObject]] = None


class MonitoringSettings(ApiModel):
    #: Call park notification is enabled or disabled.
    #: example: True
    call_park_notification_enabled: Optional[bool] = None
    #: Settings of monitored elements which can be person, place, virtual line or call park extension.
    monitored_elements: Optional[list[GetMonitoredElementsObject]] = None


class PrivacyGet(ApiModel):
    #: When `true` auto attendant extension dialing will be enabled.
    #: example: True
    aa_extension_dialing_enabled: Optional[bool] = None
    #: When `true` auto attendant dailing by first or last name will be enabled.
    #: example: True
    aa_naming_dialing_enabled: Optional[bool] = None
    #: When `true` phone status directory privacy will be enabled.
    #: example: True
    enable_phone_status_directory_privacy: Optional[bool] = None
    #: List of people that are being monitored.
    monitoring_agents: Optional[list[MonitoredMemberObject]] = None


class PushToTalkAccessType(str, Enum):
    #: List of people that are allowed to use the Push-to-Talk feature to interact with the person being configured.
    allow_members = 'ALLOW_MEMBERS'
    #: List of people that are disallowed to interact using the Push-to-Talk feature with the person being configured.
    block_members = 'BLOCK_MEMBERS'


class PushToTalkConnectionType(str, Enum):
    #: Push-to-Talk initiators can chat with this person but only in one direction. The person you enable Push-to-Talk
    #: for cannot respond.
    one_way = 'ONE_WAY'
    #: Push-to-Talk initiators can chat with this person in a two-way conversation. The person you enable Push-to-Talk
    #: for can respond.
    two_way = 'TWO_WAY'


class PushToTalkInfo(ApiModel):
    #: Set to `true` to enable the Push-to-Talk feature.  When enabled, a person receives a Push-to-Talk call and
    #: answers the call automatically.
    #: example: True
    allow_auto_answer: Optional[bool] = None
    #: Specifies the connection type to be used.
    connection_type: Optional[PushToTalkConnectionType] = None
    #: Specifies the access type to be applied when evaluating the member list.
    access_type: Optional[PushToTalkAccessType] = None
    #: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
    members: Optional[list[MonitoredMemberObject]] = None


class ReceptionInfo(ApiModel):
    #: Set to `true` to enable the Receptionist Client feature.
    #: example: True
    reception_enabled: Optional[bool] = None
    #: List of people, workspaces or virtual lines to monitor.
    monitored_members: Optional[list[MonitoredMemberObject]] = None


class BetaUserCallSettingsWithESNFeatureApi(ApiChild, base=''):
    """
    Beta User Call Settings with ESN Feature
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Person Call Settings supports modifying Webex Calling settings for a specific person.
    
    Viewing People requires a full, user, or read-only administrator auth token with a scope of
    `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by a
    person to read their own settings.
    
    Configuring People settings requires a full or user administrator auth token with the `spark-admin:people_write`
    scope or, for select APIs, a user auth token with `spark:people_write` scope can be used by a person to update
    their own settings.
    """
    ...
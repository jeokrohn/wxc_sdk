from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AgentCallQueueId', 'AvailableSharedLineMemberItem', 'BetaUserCallSettingsWithESNFeatureApi',
           'CallQueueObject', 'GetMonitoredElementsObject', 'GetMonitoredElementsObjectCallparkextension',
           'GetMonitoredElementsObjectMember', 'GetNumbers', 'GetNumbersPhoneNumbers',
           'GetNumbersPhoneNumbersRingPattern', 'GetSharedLineMemberItem', 'GetSharedLineMemberList', 'LineType',
           'Location', 'MonitoredMemberObject', 'MonitoredNumberObject', 'MonitoringSettings',
           'PeopleOrPlaceOrVirtualLineType', 'PrivacyGet', 'PushToTalkAccessType', 'PushToTalkConnectionType',
           'PushToTalkInfo', 'ReceptionInfo', 'UserType']


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
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12348100
    esn: Optional[str] = None


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
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12340000
    esn: Optional[str] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    #: example: SHARED_CALL_APPEARANCE
    line_type: Optional[LineType] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None


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
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341111
    esn: Optional[str] = None
    #: Device port number assigned to a person or workspace.
    #: example: 1
    port: Optional[int] = None
    #: T.38 Fax Compression setting. Valid only for ATA Devices. Overrides user level compression options.
    #: example: True
    t38_fax_compression_enabled: Optional[bool] = None
    #: If `true` the person or the workspace is the owner of the device. Points to primary line/port of the device.
    #: example: True
    primary_owner: Optional[bool] = None
    #: Indicates if the line is acting as a primary line or a shared line for this device.
    #: example: SHARED_CALL_APPEARANCE
    line_type: Optional[LineType] = None
    #: Number of lines that have been configured for the person on the device.
    #: example: 1
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
    hotline_destination: Optional[str] = None
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
    #: example: 10
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
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
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
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
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
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
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

    def retrieve_list_of_call_queue_caller_id_information(self, person_id: str) -> list[CallQueueObject]:
        """
        Retrieve List of Call Queue Caller ID information

        Retrieve the list of the person's available call queues and the associated Caller ID information.

        If the Agent is to enable `queueCallerIdEnabled`, they must choose which queue to use as the source for
        outgoing Caller ID.  This API returns a list of Call Queues from which the person must select.  If this
        setting is disabled or the Agent does not belong to any queue, this list will be empty.

        This API requires a full admin or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :rtype: list[CallQueueObject]
        """
        url = self.ep(f'telephony/config/people/{person_id}/queues/availableCallerIds')
        data = super().get(url)
        r = TypeAdapter(list[CallQueueObject]).validate_python(data['availableQueues'])
        return r

    def retrieve_a_call_queue_agent_s_caller_id_information(self, person_id: str) -> AgentCallQueueId:
        """
        Retrieve a call queue agent's Caller ID information.

        Each agent in the Call Queue will be able to set their outgoing Caller ID as either the Call Queue's phone
        number or their own configured Caller ID. This API fetches the configured Caller ID for the agent in the
        system.

        This API requires a full admin or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :rtype: :class:`AgentCallQueueId`
        """
        url = self.ep(f'telephony/config/people/{person_id}/queues/callerId')
        data = super().get(url)
        r = AgentCallQueueId.model_validate(data)
        return r

    def retrieve_a_person_s_monitoring_settings(self, person_id: str, org_id: str = None) -> MonitoringSettings:
        """
        Retrieve a person's Monitoring Settings

        Retrieves the monitoring settings of the person, which shows specified people, places, virtual lines or call
        park extenions that are being monitored.
        Monitors the line status which indicates if a person, place or virtual line is on a call and if a call has been
        parked on that extension.

        This API requires a full, user, or read-only administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`MonitoringSettings`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/monitoring')
        data = super().get(url, params=params)
        r = MonitoringSettings.model_validate(data)
        return r

    def get_a_list_of_phone_numbers_for_a_person(self, person_id: str, org_id: str = None) -> GetNumbers:
        """
        Get a List of Phone Numbers for a Person

        Get a person's phone numbers including alternate numbers.

        A person can have one or more phone numbers and/or extensions via which they can be called.

        This API requires a full or user administrator auth token with the `spark-admin:people_read` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`GetNumbers`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/numbers')
        data = super().get(url, params=params)
        r = GetNumbers.model_validate(data)
        return r

    def get_a_person_s_privacy_settings(self, person_id: str, org_id: str = None) -> PrivacyGet:
        """
        Get a person's Privacy Settings

        Get a person's privacy settings for the specified person ID.

        The privacy feature enables the person's line to be monitored by others and determine if they can be reached by
        Auto Attendant services.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`PrivacyGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/privacy')
        data = super().get(url, params=params)
        r = PrivacyGet.model_validate(data)
        return r

    def read_push_to_talk_settings_for_a_person(self, person_id: str, org_id: str = None) -> PushToTalkInfo:
        """
        Read Push-to-Talk Settings for a Person

        Retrieve a person's Push-to-Talk settings.

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.

        This API requires a full, user, or read-only administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`PushToTalkInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/pushToTalk')
        data = super().get(url, params=params)
        r = PushToTalkInfo.model_validate(data)
        return r

    def read_receptionist_client_settings_for_a_person(self, person_id: str, org_id: str = None) -> ReceptionInfo:
        """
        Read Receptionist Client Settings for a Person

        Retrieve a person's Receptionist Client settings.

        To help support the needs of your front-office personnel, you can set up people, workspaces or virtual lines as
        telephone attendants so that they can screen all incoming calls to certain numbers within your organization.

        This API requires a full, user, or read-only administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`ReceptionInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/reception')
        data = super().get(url, params=params)
        r = ReceptionInfo.model_validate(data)
        return r

    def search_shared_line_appearance_members(self, person_id: str, application_id: str, max_: str = None,
                                              start: str = None, location: str = None, name: str = None,
                                              number: str = None, order: str = None,
                                              extension: str = None) -> list[AvailableSharedLineMemberItem]:
        """
        Search Shared-Line Appearance Members

        Get members available for shared-line assignment to a Webex Calling Apps Desktop device.

        This API requires a full or user administrator auth token with the `spark-admin:people_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :param max_: Number of records per page.
        :type max_: str
        :param start: Page number.
        :type start: str
        :param location: Location ID for the user.
        :type location: str
        :param name: Search for users with names that match the query.
        :type name: str
        :param number: Search for users with numbers that match the query.
        :type number: str
        :param order: Sort by first name (`fname`) or last name (`lname`).
        :type order: str
        :param extension: Search for users with extensions that match the query.
        :type extension: str
        :rtype: list[AvailableSharedLineMemberItem]
        """
        body = dict()
        if max_ is not None:
            body['max'] = max_
        if start is not None:
            body['start'] = start
        if location is not None:
            body['location'] = location
        if name is not None:
            body['name'] = name
        if number is not None:
            body['number'] = number
        if order is not None:
            body['order'] = order
        if extension is not None:
            body['extension'] = extension
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/availableMembers')
        data = super().get(url, json=body)
        r = TypeAdapter(list[AvailableSharedLineMemberItem]).validate_python(data['members'])
        return r

    def get_shared_line_appearance_members(self, person_id: str, application_id: str) -> GetSharedLineMemberList:
        """
        Get Shared-Line Appearance Members

        Get primary and secondary members assigned to a shared line on a Webex Calling Apps Desktop device.

        This API requires a full or user administrator auth token with the `spark-admin:people_read` scope.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param application_id: A unique identifier for the application.
        :type application_id: str
        :rtype: :class:`GetSharedLineMemberList`
        """
        url = self.ep(f'telephony/config/people/{person_id}/applications/{application_id}/members')
        data = super().get(url)
        r = GetSharedLineMemberList.model_validate(data)
        return r

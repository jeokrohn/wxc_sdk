from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ActivityList', 'ActivityListDatasetMetadata', 'Agent', 'AgentActivity', 'AgentAgentDn', 'AgentChannelType',
           'AgentCurrentState', 'AgentSession', 'AnalyzeEntitiesDocument', 'ContactCenterApi', 'Customer',
           'CustomerActivity', 'CustomerCallDirection', 'CustomerCurrentState', 'CustomerSession',
           'CustomerSessionTerminatingEnd', 'CustomerSessionTerminationType', 'Entity', 'EntityRecognition']


class AgentAgentDn(str, Enum):
    d653 = '653'


class AgentCurrentState(str, Enum):
    logged_in = 'LoggedIn'
    idle = 'Idle'
    available = 'Available'
    connected = 'Connected'
    wrapup = 'Wrapup'
    not_responding = 'NotResponding'
    ringing = 'Ringing'


class AgentChannelType(str, Enum):
    chat = 'chat'
    email = 'email'
    telephony = 'telephony'


class Agent(ApiModel):
    #: The endpoint on which the agent receives calls/chats/emails.
    #: example: 653
    agent_dn: Optional[AgentAgentDn] = None
    #: The ID identifies an agent.
    #: example: 295
    agent_id: Optional[int] = None
    #: Name of an agent, that is, a person who answers customer calls, chats or emails.
    #: example: loadAgent00001 BSFT
    agent_name: Optional[str] = None
    #: Login name with which agent logs into agent desktop.
    #: example: loadAgent00001
    agentlogin: Optional[str] = None
    #: The ID assigned to an agent's login session.
    #: example: e3db29fa-6a84-4dc3-b814-95c617b67a95
    agent_session_id: Optional[str] = None
    #: The current state of the agent.
    #: example: LoggedIn
    current_state: Optional[AgentCurrentState] = None
    #: Timestamp when the interaction started.
    #: example: 1530629440059
    cstts: Optional[int] = None
    #: Timestamp when the interaction ended.
    #: example: 1530629440059
    cetts: Optional[int] = None
    #: The ID assigned to an entry point.
    #: example: 0ba49aae-74ed-41e5-bd28-6f8524b62e04
    channel_id: Optional[str] = None
    #: The media type of the contact.
    #: example: telephony
    channel_type: Optional[AgentChannelType] = None
    #: example: 1530629440059
    realtime_update_timestamp: Optional[int] = None
    #: The ID assigned to a team.
    #: example: 125
    team_id: Optional[int] = None
    #: The name of a team, which is a group of agents at a specific site who handle a particular type of contact.
    #: example: Load_Team1
    team_name: Optional[str] = None
    #: example: AV-SuTCNizTcJ2G98gNn
    team_system_id: Optional[str] = None
    #: The ID assigned to a site, which is a call center location.
    #: example: 66
    site_id: Optional[int] = None
    #: The call center location to which a call was distributed.
    #: example: Load_Site_BLV
    site_name: Optional[str] = None
    #: example: AV-SuI65izTcJ2G98gNm
    site_system_id: Optional[str] = None


class AgentActivity(Agent):
    #: example: c4567c9858a74fd39497cddde50b1ac
    call_session_id: Optional[str] = None
    #: The amount of time between when the activity started and when the activity ended.
    #: example: 21
    duration: Optional[int] = None
    #: The ID assigned to an idle state/code.
    #: example: 95
    idle_code_id: Optional[int] = None
    #: The name of the idle code. Admin can configure possible values like Meeting, RONA, Dinner, Lunch, Busy
    #: example: Meeting
    idle_code_name: Optional[str] = None
    #: example: AV4s2V-PXI3EMNlP7oIm
    idle_code_system_id: Optional[str] = None
    #: Indicates whether this activity occurred while making an outdial call.
    outdial_flag: Optional[int] = None


class AgentSession(Agent):
    #: A string that identifies an agent.
    #: example: AV9-9J4KizTcJ2G98fzL
    agent_system_id: Optional[str] = None
    #: The number of times an agent went into Available state.
    #: example: 1
    available_count: Optional[int] = None
    #: The number of times an agent transferred without consulting first.
    #: example: 2
    blind_xfer_count: Optional[int] = None
    #: The number of times an agent went into an Idle state.
    #: example: 1
    idle_count: Optional[int] = None
    #: The amount of time an agent spent in an Available state.
    #: example: 2065
    total_available_time: Optional[int] = None


class CustomerCallDirection(str, Enum):
    inbound = 'inbound'
    outdial = 'outdial'


class CustomerCurrentState(str, Enum):
    new = 'new'
    parked = 'parked'
    connected = 'connected'
    ended = 'ended'
    consulting = 'consulting'


class Customer(ApiModel):
    #: The ANI digits delivered with a call. ANI, or Automatic Number Identification, is a service provided by the
    #: phone company that delivers the caller's phone number along with the call.
    #: example: John
    ani: Optional[str] = None
    #: Flag that indicates whether this is a current session or not. 0 or 1.
    active: Optional[int] = None
    #: Name of an agent, that is, a person who answers customer calls/chats/emails
    #: example: loadAgent00001 BSFT
    agent_name: Optional[str] = None
    #: The ID assigned to an agent's login session.
    #: example: e3db29fa-6a84-4dc3-b814-95c617b67a95
    agent_session_id: Optional[str] = None
    #: Number of times a customer contacted.
    #: example: 1
    call_count: Optional[int] = None
    #: The current direction of the call.
    #: example: inbound
    call_direction: Optional[CustomerCallDirection] = None
    #: Timestamp when the interaction started.
    #: example: 1530629440059
    cstts: Optional[int] = None
    #: The media type of the contact.
    #: example: telephony
    channel_type: Optional[AgentChannelType] = None
    #: The current state of the contact.
    #: example: ended
    current_state: Optional[CustomerCurrentState] = None
    #: The DNIS digits delivered with the call. DNIS, or Dialed Number Identification Service, is a service provided by
    #: the phone company that delivers a digit string indicating the number the caller dialed along with the call.
    #: example: 11888999
    dnis: Optional[str] = None
    #: The ID assigned to an entry point.
    #: example: 11
    entrypoint_id: Optional[str] = None
    #: The name of the entry point, which is the landing place for customer calls on the Webex Contact Center system.
    #: Calls are moved from the entry point into a queue and are then distributed to agents.
    #: example: Apple-SalesEP
    entrypoint_name: Optional[str] = None
    #: The ID assigned to an entry point.
    #: example: AV3KrA1AXI3EMNlP7m_2
    entrypoint_system_id: Optional[str] = None
    #: Flag that indicates whether this activity occurred while making an outdial call.
    is_outdial: Optional[int] = None
    #: example: 1584547145749
    realtime_update_timestamp: Optional[str] = None
    #: example: e3cf6187-cc3f-4c6f-8ba5-6014821529e3-1584547145537-new
    sid: Optional[str] = None
    #: The ID assigned to a site, which is a call center location.
    #: example: 66
    site_id: Optional[int] = None
    #: The call center location to which a call was distributed.
    #: example: Load_Site_BLV
    site_name: Optional[str] = None
    #: example: AV-SuI65izTcJ2G98gNm
    site_system_id: Optional[str] = None
    #: The ID assigned to a team.
    #: example: 125
    team_id: Optional[int] = None
    #: The name of a team, which is a group of agents at a specific site who handle a particular type of contact.
    #: example: Load_Team1
    team_name: Optional[str] = None
    #: example: AV-SuTCNizTcJ2G98gNn
    team_system_id: Optional[str] = None
    #: example: 1
    tid: Optional[int] = None


class CustomerActivity(Customer):
    #: The amount of time between when the activity started and when it was terminated.
    #: example: 154
    duration: Optional[int] = None
    #: If this isn't a current activity, this field shows the state of the following activity.
    #: example: ivr-connected
    next_state: Optional[str] = None


class CustomerSessionTerminatingEnd(str, Enum):
    caller = 'caller'
    agent = 'agent'


class CustomerSessionTerminationType(str, Enum):
    normal = 'normal'
    abandoned = 'abandoned'
    self_service = 'self_service'


class CustomerSession(Customer):
    #: Number of times the contact was in IVR state.
    #: example: 1
    ivr_count: Optional[int] = None
    #: The amount of time, in milliseconds, during which a call was in IVR state.
    #: example: 1
    ivr_duration: Optional[int] = None
    #: A string that identifies a queue.
    #: example: 20
    queue_id: Optional[str] = None
    #: The number of queues contact entered.
    #: example: 1
    queue_count: Optional[int] = None
    #: The name of the current or final queue, which is holding place for contacts while they await handling by an
    #: agent. Calls are moved from an entry point into a queue and are then distributed to agents.
    #: example: Apple-SalesQueue
    queue_name: Optional[str] = None
    #: The amount of time, in milliseconds, a contact spent in queue waiting.
    #: example: 245198
    queue_duration: Optional[int] = None
    #: Indicates which party terminated the interaction.
    #: example: caller
    terminating_end: Optional[CustomerSessionTerminatingEnd] = None
    #: Indicates how a call was terminated.
    #: example: abandoned
    termination_type: Optional[CustomerSessionTerminationType] = None


class ActivityListDatasetMetadata(ApiModel):
    last_access_timestamp: Optional[int] = None
    #: example: 3
    number_of_records_found: Optional[int] = None
    #: example: 3
    number_of_records_in_dataset: Optional[int] = None
    #: example: True
    is_complete: Optional[bool] = None


class ActivityList(ApiModel):
    dataset_metadata: Optional[ActivityListDatasetMetadata] = None
    #: An array of column IDs in the query.
    columns: Optional[list[str]] = None
    #: An array of records
    data: Optional[list[str]] = None


class Entity(ApiModel):
    #: String value of the found entity
    value: Optional[str] = None
    #: Start index of the found entity
    start_position: Optional[int] = None
    #: End index of the found entity
    end_position: Optional[int] = None
    #: Name of the entity found
    label: Optional[str] = None
    #: Confidence score of the found entity
    score: Optional[int] = None


class EntityRecognition(ApiModel):
    #: Identifier of the Organization
    org_id: Optional[str] = None
    #: Identifier of the contact.
    contact_id: Optional[str] = None
    #: Identifier of the call leg / party (caller, agent).
    party_id: Optional[str] = None
    #: Identifier of the model.
    model_id: Optional[str] = None
    #: Version of the model.
    model_version: Optional[str] = None
    #: List of found entities
    entities: Optional[list[Entity]] = None


class AnalyzeEntitiesDocument(ApiModel):
    #: The document's type.
    #: example: PLAIN_TEXT
    type: Optional[str] = None
    #: The document's content.
    #: example: My name is John Doe . I am from USA .
    content: Optional[str] = None


class ContactCenterApi(ApiChild, base='contactCenter'):
    """
    Contact Center
    
    The Webex Contact Center functionality and API endpoints described here are
    currently pre-release features which are not available to all Webex users. If
    you have any questions, or if you need help, please contact the Webex
    Developer Support team at devsupport@webex.com.
    
    
    
    This set of WxCC API endpoints allow developers to use `AI API` for entity recognition, `Analytics API` to fetch
    session and activity based records for customer and agent in WxCC and `Media API` for providing agent/customer
    interaction recordings.
    """

    def analyze_entities(self, org_id: str, contact_id: str, party_id: str,
                         document: AnalyzeEntitiesDocument) -> EntityRecognition:
        """
        Analyze Entities

        Entity Recognition allows consumers to get named entities for the input call transcript.
        It requires an auth token with the `cjp:organization` `scope
        <https://developer.webex.com/docs/integrations#scopes>`_ to use this end point.

        Note that each API request:

        - Only considers the first 3,000 characters in the input for recognition

        - Return a maximum of 100 entities per request.

        If the text is too large, it is recommended to break it up into multiple requests to get the entities.

        :param org_id: The ID of the organization.
        :type org_id: str
        :param contact_id: The ID of the contact.
        :type contact_id: str
        :param party_id: The ID of the call leg/party.
        :type party_id: str
        :param document: The document.
        :type document: AnalyzeEntitiesDocument
        :rtype: :class:`EntityRecognition`
        """
        body = dict()
        body['orgId'] = org_id
        body['contactId'] = contact_id
        body['partyId'] = party_id
        body['document'] = loads(document.model_dump_json())
        url = self.ep('document:analyzeEntities')
        data = super().post(url, json=body)
        r = EntityRecognition.model_validate(data)
        return r

    def get_agent_activity_record_list(self, org_id: str, q: str) -> ActivityList:
        """
        Get Agent Activity Record List

        Get a list of agent activity records for the specified query, `q`. The query must be an encoded JSON object.

        Listing agent activity records requires an auth token with the `cjp:config_read` `scope
        <https://developer.webex.com/docs/integrations#scopes>`_ for organizations with a
        WxCC license, or the `cjp-analyzer:read` scope for organizations with a Hybrid Analyzer license.

        :type org_id: str
        :param q: An encoded json query. Example of json query:

        ```
        {
        "anchorId":"1",
        "dateBegin": [
        1514793600000
        ],
        "dateEnd": [
        1530860400000
        ],
        "numberOfRecords": 100,
        "aggregateQueryProperties": {
        "rowSegmentSet": [
        {
        "columnName": "channelType__s",
        "name": "channelType__s"
        }
        ],
        "columnSegmentSet": []
        },
        "activityType": "AAR",
        "aggregations": [
        {
        "id": 0,
        "aggregationType": "COUNT",
        "computeColumnName": "agentSessionId__s"
        }
        ]
        }
        ```
        :type q: str
        :rtype: :class:`ActivityList`
        """
        params = {}
        params['orgId'] = org_id
        params['q'] = q
        url = self.ep('aars')
        data = super().get(url, params=params)
        r = ActivityList.model_validate(data)
        return r

    def get_agent_activity_record(self, id: str, org_id: str) -> AgentActivity:
        """
        Get Agent Activity Record

        Get details of an agent activity for the `id` specified in the URI.

        Retrieving agent activity records requires an auth token with the `cjp:config_read` `scope
        <https://developer.webex.com/docs/integrations#scopes>`_ for organizations
        with a WxCC license or the `cjp-analyzer:read` scope for organizations with a Hybrid Analyzer license.

        :param id: A unique identifier for AAR is required. Must be of the format:
            `agentSessionId-channelType-timestamp-eventName`.
        :type id: str
        :param org_id: The organization ID.
        :type org_id: str
        :rtype: :class:`AgentActivity`
        """
        params = {}
        params['orgId'] = org_id
        url = self.ep(f'aars/{id}')
        data = super().get(url, params=params)
        r = AgentActivity.model_validate(data)
        return r

    def get_agent_session_record_list(self, org_id: str, q: str) -> ActivityList:
        """
        Get Agent Session Record List

        Get a list of agent session records for the specified query, `q`. The query must be an encoded JSON object.

        Listing agent session records requires an auth token with the `cjp:config_read` `scope
        <https://developer.webex.com/docs/integrations#scopes>`_ for organizations with a
        WxCC license or the `cjp-analyzer:read` scope for organizations with a Hybrid Analyzer license.

        :type org_id: str
        :param q: An encoded JSON query. Example JSON query:

        ```
        {
        "anchorId":"1",
        "dateBegin": [
        1514793600000
        ],
        "dateEnd": [
        1530860400000
        ],
        "numberOfRecords": 100,
        "aggregateQueryProperties": {
        "rowSegmentSet": [
        {
        "columnName": "channelType__s",
        "name": "channelType__s"
        }
        ],
        "columnSegmentSet": []
        },
        "activityType": "ASR",
        "aggregations": [
        {
        "id": 0,
        "aggregationType": "VALUE",
        "computeColumnName": "agentSessionId"
        }
        ]
        }
        ```
        :type q: str
        :rtype: :class:`ActivityList`
        """
        params = {}
        params['orgId'] = org_id
        params['q'] = q
        url = self.ep('asrs')
        data = super().get(url, params=params)
        r = ActivityList.model_validate(data)
        return r

    def get_agent_session_record(self, id: str, org_id: str) -> AgentSession:
        """
        Get Agent Session Record

        Get details of an agent session record specified by `id` in the URI.

        Retrieving agent session records requires an auth token with the `cjp:config_read` `scope
        <https://developer.webex.com/docs/integrations#scopes>`_ for organizations with
        a WxCC license or the `cjp-analyzer:read` scope for organizations with a Hybrid Analyzer license.

        :param id: A unique identifier for ASR is required.
        :type id: str
        :param org_id: The organization ID.
        :type org_id: str
        :rtype: :class:`AgentSession`
        """
        params = {}
        params['orgId'] = org_id
        url = self.ep(f'asrs/{id}')
        data = super().get(url, params=params)
        r = AgentSession.model_validate(data)
        return r

    def get_customer_activity_record_list(self, org_id: str, q: str) -> ActivityList:
        """
        Get Customer Activity Record List

        Get a list of customer activity records for the specified query, `q`. The query must be an encoded JSON object.

        Listing customer activity records requires an auth token with the `cjp:config_read` `scope
        <https://developer.webex.com/docs/integrations#scopes>`_ for organizations
        with a WxCC license or the `cjp-analyzer:read` scope for organizations with a Hybrid Analyzer license.

        :type org_id: str
        :param q: An encoded JSON query. Example JSON query:

        ```
        {
        "anchorId":"1",
        "dateBegin": [
        1514793600000
        ],
        "dateEnd": [
        1530860400000
        ],
        "numberOfRecords": 100,
        "aggregateQueryProperties": {
        "rowSegmentSet": [
        {
        "columnName": "channelType__s",
        "name": "channelType__s"
        }
        ],
        "columnSegmentSet": []
        },
        "activityType": "CAR",
        "aggregations": [
        {
        "id": 0,
        "aggregationType": "COUNT",
        "computeColumnName": "callSessionId__s"
        }
        ]
        }
        ```
        :type q: str
        :rtype: :class:`ActivityList`
        """
        params = {}
        params['orgId'] = org_id
        params['q'] = q
        url = self.ep('cars')
        data = super().get(url, params=params)
        r = ActivityList.model_validate(data)
        return r

    def get_customer_activity_record(self, id: str, org_id: str) -> CustomerActivity:
        """
        Get Customer Activity Record

        Get details of a customer activity record by `id` in the URI.

        Retrieving customer activity records requires an auth token with the `cjp:config_read` `scope
        <https://developer.webex.com/docs/integrations#scopes>`_ for organizations
        with a WxCC license or the `cjp-analyzer:read` scope for organizations with a Hybrid Analyzer license.

        :param id: A unique identifier for CAR is required. Must be of the format: callSessionId-timestamp-eventName.
        :type id: str
        :param org_id: The organization ID.
        :type org_id: str
        :rtype: :class:`CustomerActivity`
        """
        params = {}
        params['orgId'] = org_id
        url = self.ep(f'cars/{id}')
        data = super().get(url, params=params)
        r = CustomerActivity.model_validate(data)
        return r

    def get_customer_session_record_list(self, org_id: str, q: str) -> ActivityList:
        """
        Get Customer Session Record List

        Get a list of customer session records for the specified query, `q`. The query must be an encoded JSON object.

        Listing customer session records requires an auth token with the `cjp:config_read` `scope
        <https://developer.webex.com/docs/integrations#scopes>`_ for organizations with
        a WxCC license or the `cjp-analyzer:read` scope for organizations with a Hybrid Analyzer license.

        :type org_id: str
        :param q: An encoded JSON query. Example JSON query:

        ```
        {
        "anchorId":"1",
        "dateBegin": [
        1514793600000
        ],
        "dateEnd": [
        1530860400000
        ],
        "numberOfRecords": 100,
        "aggregateQueryProperties": {
        "rowSegmentSet": [
        {
        "columnName": "channelType__s",
        "name": "channelType__s"
        }
        ],
        "columnSegmentSet": []
        },
        "activityType": "CSR",
        "aggregations": [
        {
        "id": 0,
        "aggregationType": "COUNT",
        "computeColumnName": "sid"
        }
        ]
        }
        ```
        :type q: str
        :rtype: :class:`ActivityList`
        """
        params = {}
        params['orgId'] = org_id
        params['q'] = q
        url = self.ep('csrs')
        data = super().get(url, params=params)
        r = ActivityList.model_validate(data)
        return r

    def get_customer_session_record(self, id: str, org_id: str) -> CustomerSession:
        """
        Get Customer Session Record

        Get details of a customer session record for the specified `id`.

        Retrieving customer session records requires an auth token with the `cjp:config_read` `scope
        <https://developer.webex.com/docs/integrations#scopes>`_ for organizations
        with a WxCC license or the `cjp-analyzer:read` scope for organizations with a Hybrid Analyzer license.

        :param id: A unique identifier for CSR is required.
        :type id: str
        :param org_id: The organization ID.
        :type org_id: str
        :rtype: :class:`CustomerSession`
        """
        params = {}
        params['orgId'] = org_id
        url = self.ep(f'csrs/{id}')
        data = super().get(url, params=params)
        r = CustomerSession.model_validate(data)
        return r

    def get_decrypted_recording(self, session_id: str, org_id: str):
        """
        Get Decrypted Recording

        Recording management endpoints allow consumers to retrieve session recordings for customer or agent. It
        requires an auth token with a `scope
        <https://developer.webex.com/docs/integrations#scopes>`_ of `cjp:config_read` for a WxCC license and `cjp-analyzer:read` for
        organizations with only a Hybrid Analyzer license.

        Get decrypted recording of a customer or agent session by ID. Specify `sessionId` in the URI.

        :param session_id: A unique identifier for session recording is required.
        :type session_id: str
        :param org_id: The organization ID.
        :type org_id: str
        :rtype: None
        """
        params = {}
        params['orgId'] = org_id
        url = self.ep(f'get-decrypted-recording/{session_id}')
        super().get(url, params=params)

    def get_encrypted_recording(self, session_id: str, key_id: int, org_id: str):
        """
        Get Encrypted Recording

        Recording management endpoints allow consumers to retrieve session recordings for customer or agent. It
        requires an auth token with a `scope
        <https://developer.webex.com/docs/integrations#scopes>`_ of `cjp:config_read` for a WxCC license and `cjp-analyzer:read` for
        organizations having only Hybrid Analyzer license.

        Get encrypted recording of a customer or agent session by ID. Specify `sessionId` and `keyId` in the URI.

        :param session_id: A unique identifier for session recording is required.
        :type session_id: str
        :param key_id: An encryption key is required.
        :type key_id: int
        :param org_id: The organization ID.
        :type org_id: str
        :rtype: None
        """
        params = {}
        params['orgId'] = org_id
        url = self.ep(f'get-encrypted-recording/{session_id}/{key_id}')
        super().get(url, params=params)

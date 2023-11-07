from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ActivityList', 'ActivityListDatasetMetadata', 'Agent', 'AgentActivity', 'AgentAgentDn',
            'AgentChannelType', 'AgentCurrentState', 'AgentSession', 'AnalyzeEntitiesDocument', 'Customer',
            'CustomerActivity', 'CustomerCallDirection', 'CustomerCurrentState', 'CustomerSession',
            'CustomerSessionTerminatingEnd', 'CustomerSessionTerminationType', 'Entity', 'EntityRecognition', 'Error',
            'ErrorDetails', 'Link']


class ErrorDetails(ApiModel):
    ...


class Link(ApiModel):
    href: Optional[str] = None
    method: Optional[str] = None
    rel: Optional[str] = None


class Error(ApiModel):
    code: Optional[int] = None
    details: Optional[ErrorDetails] = None
    internal: Optional[bool] = None
    links: Optional[list[Link]] = None


class AgentAgentDn(str, Enum):
    _653 = '653'


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
    #: example: 295.0
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
    #: example: 1530629440059.0
    cstts: Optional[int] = None
    #: Timestamp when the interaction ended.
    #: example: 1530629440059.0
    cetts: Optional[int] = None
    #: The ID assigned to an entry point.
    #: example: 0ba49aae-74ed-41e5-bd28-6f8524b62e04
    channel_id: Optional[str] = None
    #: The media type of the contact.
    #: example: telephony
    channel_type: Optional[AgentChannelType] = None
    #: example: 1530629440059.0
    realtime_update_timestamp: Optional[int] = None
    #: The ID assigned to a team.
    #: example: 125.0
    team_id: Optional[int] = None
    #: The name of a team, which is a group of agents at a specific site who handle a particular type of contact.
    #: example: Load_Team1
    team_name: Optional[str] = None
    #: example: AV-SuTCNizTcJ2G98gNn
    team_system_id: Optional[str] = None
    #: The ID assigned to a site, which is a call center location.
    #: example: 66.0
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
    #: example: 21.0
    duration: Optional[int] = None
    #: The ID assigned to an idle state/code.
    #: example: 95.0
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
    #: example: 1.0
    available_count: Optional[int] = None
    #: The number of times an agent transferred without consulting first.
    #: example: 2.0
    blind_xfer_count: Optional[int] = None
    #: The number of times an agent went into an Idle state.
    #: example: 1.0
    idle_count: Optional[int] = None
    #: The amount of time an agent spent in an Available state.
    #: example: 2065.0
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
    #: example: 1.0
    call_count: Optional[int] = None
    #: The current direction of the call.
    #: example: inbound
    call_direction: Optional[CustomerCallDirection] = None
    #: Timestamp when the interaction started.
    #: example: 1530629440059.0
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
    entrypoint_id: Optional[datetime] = None
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
    #: example: 66.0
    site_id: Optional[int] = None
    #: The call center location to which a call was distributed.
    #: example: Load_Site_BLV
    site_name: Optional[str] = None
    #: example: AV-SuI65izTcJ2G98gNm
    site_system_id: Optional[str] = None
    #: The ID assigned to a team.
    #: example: 125.0
    team_id: Optional[int] = None
    #: The name of a team, which is a group of agents at a specific site who handle a particular type of contact.
    #: example: Load_Team1
    team_name: Optional[str] = None
    #: example: AV-SuTCNizTcJ2G98gNn
    team_system_id: Optional[str] = None
    #: example: 1.0
    tid: Optional[int] = None


class CustomerActivity(Customer):
    #: The amount of time between when the activity started and when it was terminated.
    #: example: 154.0
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
    #: example: 1.0
    ivr_count: Optional[int] = None
    #: The amount of time, in milliseconds, during which a call was in IVR state.
    #: example: 1.0
    ivr_duration: Optional[int] = None
    #: A string that identifies a queue.
    #: example: 20
    queue_id: Optional[datetime] = None
    #: The number of queues contact entered.
    #: example: 1.0
    queue_count: Optional[int] = None
    #: The name of the current or final queue, which is holding place for contacts while they await handling by an
    #: agent. Calls are moved from an entry point into a queue and are then distributed to agents.
    #: example: Apple-SalesQueue
    queue_name: Optional[str] = None
    #: The amount of time, in milliseconds, a contact spent in queue waiting.
    #: example: 245198.0
    queue_duration: Optional[int] = None
    #: Indicates which party terminated the interaction.
    #: example: caller
    terminating_end: Optional[CustomerSessionTerminatingEnd] = None
    #: Indicates how a call was terminated.
    #: example: abandoned
    termination_type: Optional[CustomerSessionTerminationType] = None


class ActivityListDatasetMetadata(ApiModel):
    last_access_timestamp: Optional[int] = None
    #: example: 3.0
    number_of_records_found: Optional[int] = None
    #: example: 3.0
    number_of_records_in_dataset: Optional[int] = None
    #: example: true
    is_complete: Optional[str] = None


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
    ...
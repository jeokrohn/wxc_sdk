from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ActivityList', 'ActivityListDatasetMetadata', 'Agent', 'AgentActivity', 'AgentAgentDn', 'AgentChannelType', 'AgentCurrentState', 'AgentSession', 'Customer', 'CustomerActivity', 'CustomerCallDirection', 'CustomerCurrentState', 'CustomerSession', 'CustomerSessionTerminatingEnd', 'CustomerSessionTerminationType', 'Entity', 'EntityRecognition', 'Error', 'ErrorDetails', 'Link']


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
    loggedin = 'LoggedIn'
    idle = 'Idle'
    available = 'Available'
    connected = 'Connected'
    wrapup = 'Wrapup'
    notresponding = 'NotResponding'
    ringing = 'Ringing'


class AgentChannelType(str, Enum):
    chat = 'chat'
    email = 'email'
    telephony = 'telephony'


class Agent(ApiModel):
    #: The endpoint on which the agent receives calls/chats/emails.
    #: example: 653
    agentDn: Optional[AgentAgentDn] = None
    #: The ID identifies an agent.
    #: example: 295.0
    agentId: Optional[int] = None
    #: Name of an agent, that is, a person who answers customer calls, chats or emails.
    #: example: loadAgent00001 BSFT
    agentName: Optional[str] = None
    #: Login name with which agent logs into agent desktop.
    #: example: loadAgent00001
    agentlogin: Optional[str] = None
    #: The ID assigned to an agent's login session.
    #: example: e3db29fa-6a84-4dc3-b814-95c617b67a95
    agentSessionId: Optional[str] = None
    #: The current state of the agent.
    #: example: LoggedIn
    currentState: Optional[AgentCurrentState] = None
    #: Timestamp when the interaction started.
    #: example: 1530629440059.0
    cstts: Optional[int] = None
    #: Timestamp when the interaction ended.
    #: example: 1530629440059.0
    cetts: Optional[int] = None
    #: The ID assigned to an entry point.
    #: example: 0ba49aae-74ed-41e5-bd28-6f8524b62e04
    channelId: Optional[str] = None
    #: The media type of the contact.
    #: example: telephony
    channelType: Optional[AgentChannelType] = None
    #: example: 1530629440059.0
    realtimeUpdateTimestamp: Optional[int] = None
    #: The ID assigned to a team.
    #: example: 125.0
    teamId: Optional[int] = None
    #: The name of a team, which is a group of agents at a specific site who handle a particular type of contact.
    #: example: Load_Team1
    teamName: Optional[str] = None
    #: example: AV-SuTCNizTcJ2G98gNn
    teamSystemId: Optional[str] = None
    #: The ID assigned to a site, which is a call center location.
    #: example: 66.0
    siteId: Optional[int] = None
    #: The call center location to which a call was distributed.
    #: example: Load_Site_BLV
    siteName: Optional[str] = None
    #: example: AV-SuI65izTcJ2G98gNm
    siteSystemId: Optional[str] = None


class AgentActivity(Agent):
    #: example: c4567c9858a74fd39497cddde50b1ac
    callSessionId: Optional[str] = None
    #: The amount of time between when the activity started and when the activity ended.
    #: example: 21.0
    duration: Optional[int] = None
    #: The ID assigned to an idle state/code.
    #: example: 95.0
    idleCodeId: Optional[int] = None
    #: The name of the idle code. Admin can configure possible values like Meeting, RONA, Dinner, Lunch, Busy
    #: example: Meeting
    idleCodeName: Optional[str] = None
    #: example: AV4s2V-PXI3EMNlP7oIm
    idleCodeSystemId: Optional[str] = None
    #: Indicates whether this activity occurred while making an outdial call.
    outdialFlag: Optional[int] = None


class AgentSession(Agent):
    #: A string that identifies an agent.
    #: example: AV9-9J4KizTcJ2G98fzL
    agentSystemId: Optional[str] = None
    #: The number of times an agent went into Available state.
    #: example: 1.0
    availableCount: Optional[int] = None
    #: The number of times an agent transferred without consulting first.
    #: example: 2.0
    blindXferCount: Optional[int] = None
    #: The number of times an agent went into an Idle state.
    #: example: 1.0
    idleCount: Optional[int] = None
    #: The amount of time an agent spent in an Available state.
    #: example: 2065.0
    totalAvailableTime: Optional[int] = None


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
    #: The ANI digits delivered with a call. ANI, or Automatic Number Identification, is a service provided by the phone company that delivers the caller's phone number along with the call.
    #: example: John
    ani: Optional[str] = None
    #: Flag that indicates whether this is a current session or not. 0 or 1.
    active: Optional[int] = None
    #: Name of an agent, that is, a person who answers customer calls/chats/emails
    #: example: loadAgent00001 BSFT
    agentName: Optional[str] = None
    #: The ID assigned to an agent's login session.
    #: example: e3db29fa-6a84-4dc3-b814-95c617b67a95
    agentSessionId: Optional[str] = None
    #: Number of times a customer contacted.
    #: example: 1.0
    callCount: Optional[int] = None
    #: The current direction of the call.
    #: example: inbound
    callDirection: Optional[CustomerCallDirection] = None
    #: Timestamp when the interaction started.
    #: example: 1530629440059.0
    cstts: Optional[int] = None
    #: The media type of the contact.
    #: example: telephony
    channelType: Optional[AgentChannelType] = None
    #: The current state of the contact.
    #: example: ended
    currentState: Optional[CustomerCurrentState] = None
    #: The DNIS digits delivered with the call. DNIS, or Dialed Number Identification Service, is a service provided by the phone company that delivers a digit string indicating the number the caller dialed along with the call.
    #: example: 11888999
    dnis: Optional[str] = None
    #: The ID assigned to an entry point.
    #: example: 11
    entrypointId: Optional[datetime] = None
    #: The name of the entry point, which is the landing place for customer calls on the Webex Contact Center system. Calls are moved from the entry point into a queue and are then distributed to agents.
    #: example: Apple-SalesEP
    entrypointName: Optional[str] = None
    #: The ID assigned to an entry point.
    #: example: AV3KrA1AXI3EMNlP7m_2
    entrypointSystemId: Optional[str] = None
    #: Flag that indicates whether this activity occurred while making an outdial call.
    isOutdial: Optional[int] = None
    #: example: 1584547145749
    realtimeUpdateTimestamp: Optional[str] = None
    #: example: e3cf6187-cc3f-4c6f-8ba5-6014821529e3-1584547145537-new
    sid: Optional[str] = None
    #: The ID assigned to a site, which is a call center location.
    #: example: 66.0
    siteId: Optional[int] = None
    #: The call center location to which a call was distributed.
    #: example: Load_Site_BLV
    siteName: Optional[str] = None
    #: example: AV-SuI65izTcJ2G98gNm
    siteSystemId: Optional[str] = None
    #: The ID assigned to a team.
    #: example: 125.0
    teamId: Optional[int] = None
    #: The name of a team, which is a group of agents at a specific site who handle a particular type of contact.
    #: example: Load_Team1
    teamName: Optional[str] = None
    #: example: AV-SuTCNizTcJ2G98gNn
    teamSystemId: Optional[str] = None
    #: example: 1.0
    tid: Optional[int] = None


class CustomerActivity(Customer):
    #: The amount of time between when the activity started and when it was terminated.
    #: example: 154.0
    duration: Optional[int] = None
    #: If this isn't a current activity, this field shows the state of the following activity.
    #: example: ivr-connected
    nextState: Optional[str] = None


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
    ivrCount: Optional[int] = None
    #: The amount of time, in milliseconds, during which a call was in IVR state.
    #: example: 1.0
    ivrDuration: Optional[int] = None
    #: A string that identifies a queue.
    #: example: 20
    queueId: Optional[datetime] = None
    #: The number of queues contact entered.
    #: example: 1.0
    queueCount: Optional[int] = None
    #: The name of the current or final queue, which is holding place for contacts while they await handling by an agent. Calls are moved from an entry point into a queue and are then distributed to agents.
    #: example: Apple-SalesQueue
    queueName: Optional[str] = None
    #: The amount of time, in milliseconds, a contact spent in queue waiting.
    #: example: 245198.0
    queueDuration: Optional[int] = None
    #: Indicates which party terminated the interaction.
    #: example: caller
    terminatingEnd: Optional[CustomerSessionTerminatingEnd] = None
    #: Indicates how a call was terminated.
    #: example: abandoned
    terminationType: Optional[CustomerSessionTerminationType] = None


class ActivityListDatasetMetadata(ApiModel):
    lastAccessTimestamp: Optional[int] = None
    #: example: 3.0
    numberOfRecordsFound: Optional[int] = None
    #: example: 3.0
    numberOfRecordsInDataset: Optional[int] = None
    #: example: true
    isComplete: Optional[str] = None


class ActivityList(ApiModel):
    datasetMetadata: Optional[ActivityListDatasetMetadata] = None
    #: An array of column IDs in the query.
    columns: Optional[list[str]] = None
    #: An array of records
    data: Optional[list[str]] = None


class Entity(ApiModel):
    #: String value of the found entity
    value: Optional[str] = None
    #: Start index of the found entity
    startPosition: Optional[int] = None
    #: End index of the found entity
    endPosition: Optional[int] = None
    #: Name of the entity found
    label: Optional[str] = None
    #: Confidence score of the found entity
    score: Optional[int] = None


class EntityRecognition(ApiModel):
    #: Identifier of the Organization
    orgId: Optional[str] = None
    #: Identifier of the contact.
    contactId: Optional[str] = None
    #: Identifier of the call leg / party (caller, agent).
    partyId: Optional[str] = None
    #: Identifier of the model.
    modelId: Optional[str] = None
    #: Version of the model.
    modelVersion: Optional[str] = None
    #: List of found entities
    entities: Optional[list[Entity]] = None

"""
common base for Call Queues and Hunt Groups
"""
from base64 import b64decode
from enum import Enum
from typing import Optional, List, Dict

from pydantic import Field, validator

from ..base import ApiModel, webex_id_to_uuid
from ..rest import RestSession
from .user_base import UserBase

__all__ = ['HGandCQ', 'AlternateNumber', 'Policy', 'Agent', 'RingPattern', 'AlternateNumberSettings',
           'ForwardingAPI', 'CallForwarding', 'ForwardingRuleDetails', 'ForwardingSetting',
           'ForwardingRule', 'ForwardTo', 'ForwardCallsTo', 'ForwardToSelection', 'ForwardFromSelection',
           'CallForwardingNumber', 'CallForwardingNumberType', 'CallsFrom', 'CustomNumbers', 'FeatureSelector']


class HGandCQ(ApiModel):
    name: Optional[str]
    id: Optional[str]
    location_name: Optional[str]  # only returned by list()
    location_id: Optional[str]  # # only returned by list()
    phone_number: Optional[str]
    extension: Optional[str]
    enabled: Optional[bool]
    toll_free_number: Optional[bool]

    @property
    def cpapi_id(self):
        return webex_id_to_uuid(self.id)

    @property
    def bc_id(self) -> Optional[str]:
        bc_id = webex_id_to_uuid(self.id)
        return bc_id and b64decode(bc_id).decode()


class RingPattern(str, Enum):
    """
    Ring Pattern
    """
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a short ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class AlternateNumber(ApiModel):
    """
    Hunt group or call queue alternate number
    """
    #: Alternate phone number for the hunt group or call queue
    phone_number: str
    #: Ring pattern for when this alternate number is called. Only available when distinctiveRing is enabled for the
    #: hunt group.
    ring_pattern: RingPattern
    #: Flag: phone_number is a toll free numner
    toll_free_number: bool


class AlternateNumberSettings(ApiModel):
    """
    Alternate number settings for call queue or hunt group

    The alternate numbers feature allows you to assign multiple phone numbers or extensions to a call queue or hunt
    group. Each
    number will reach the same greeting and each menu will function identically to the main number. The alternate
    numbers option enables you to have up to ten (10) phone numbers ring into the call queue.
    """
    #: Distinctive Ringing selected for the alternate numbers in the call queue or hunt group overrides the normal
    #: ringing patterns set for Alternate Number.
    distinctive_ring_enabled: bool = Field(default=True)
    #: Specifies up to 10 numbers which can each have an overriden distinctive ring setting.
    alternate_numbers: List[AlternateNumber] = Field(default_factory=list)


class Policy(str, Enum):
    """
    Policy controlling how calls are routed to agents.
    """
    #: (Max 1,000 agents) This option cycles through all agents after the last agent that took a call. It sends calls
    #: to the next available agent.
    circular = 'CIRCULAR'
    #: (Max 1,000 agents) Send the call through the queue of agents in order, starting from the top each time.
    regular = 'REGULAR'
    #: (Max 50 agents) Sends calls to all agents at once
    simultaneous = 'SIMULTANEOUS'
    #: (Max 1,000 agents) Sends calls to the agent that has been idle the longest. If they don't answer, proceed to the
    #: next agent who has been idle the second longest, and so on until the call is answered.
    uniform = 'UNIFORM'
    #: (Max 100 agents) Sends call to idle agents based on percentages you assign to each agent (up to 100%).
    weighted = 'WEIGHTED'


class Agent(UserBase):
    extension: Optional[str]
    phone_number: Optional[str]
    weight: Optional[int]
    agent_id: str = Field(alias='id')

    @property
    def cpapi_id(self) -> str:
        return webex_id_to_uuid(self.agent_id)


def assert_plus1(number: str) -> str:
    """
    platform returns NANP numbers w/o leading + while other numbers are returned as e.g. "+49-6567...
    For every number that does not start with "+" we prepend "+1-"
    :param number:
    :return:
    """
    return number.startswith('+') and number or f'+1-{number}'


def strip_plus1(number: str) -> str:
    """
    Strip leading "+1-" if present. NANP numbers on the platform seem to be stored as 10D only
    :param number:
    :return:
    """
    return number and number.startswith('+1-') and number[3:] or number


class ForwardingRule(ApiModel):
    id: str
    name: Optional[str]
    calls_from: Optional[str]
    forward_to: Optional[str]
    calls_to: Optional[str]
    enabled: bool


class ForwardingSetting(ApiModel):
    enabled: bool
    ring_reminder_enabled: bool
    send_to_voicemail_enabled: bool
    destination: Optional[str]

    @staticmethod
    def default() -> 'ForwardingSetting':
        return ForwardingSetting(enabled=False,
                                 ring_reminder_enabled=False,
                                 send_to_voicemail_enabled=False,
                                 destination='')


class CallForwarding(ApiModel):
    always: ForwardingSetting
    selective: ForwardingSetting
    rules: List[ForwardingRule]

    @staticmethod
    def default() -> 'CallForwarding':
        return CallForwarding(always=ForwardingSetting.default(),
                              selective=ForwardingSetting.default(),
                              rules=[])


class ForwardToSelection(str, Enum):
    default_number = 'FORWARD_TO_DEFAULT_NUMBER'
    specified_number = 'FORWARD_TO_SPECIFIED_NUMBER'
    dont_forward = 'DO_NOT_FORWARD'


class ForwardTo(ApiModel):
    """
    Definition of a call forward destination
    """
    selection: ForwardToSelection = Field(default=ForwardToSelection.default_number)
    phone_number: Optional[str]


class ForwardFromSelection(str, Enum):
    any = 'ANY'
    custom = 'CUSTOM'


class CallForwardingNumberType(str, Enum):
    """
    Number type for call forwarding number
    """
    primary = 'PRIMARY'
    alternate = 'ALTERNATE'


class CallForwardingNumber(ApiModel):
    # TODO: implement test to check whether the transform between +1 and 10D is still required
    """
    single number in forwarding calls to definition
    """
    phone_number: Optional[str]
    extension: Optional[str]
    number_type: CallForwardingNumberType = Field(alias='type')

    @validator('phone_number', pre=True)
    def validate_phone_number(cls, v):
        """
        Platform returns NANP numbers w/o +
        :param v:
        :return:
        """
        return assert_plus1(v)

    def dict(self, *args, **kwargs):
        """
        When serializing remove the +1- again
        :param args:
        :param kwargs:
        :return:
        """
        number = self.phone_number
        self.phone_number = strip_plus1(number)
        r = super().dict(*args, **kwargs)
        self.phone_number = number
        return r


class ForwardCallsTo(ApiModel):
    """
    List of numbers in custom number definition
    """
    numbers: List[CallForwardingNumber] = Field(default_factory=list)


class CustomNumbers(ApiModel):
    """
    custom numbers definition in forwarding rule
    """
    private_number_enabled: bool = Field(default=False)
    unavailable_number_enabled: bool = Field(default=False)
    numbers: Optional[List[str]]

    @validator('numbers', pre=True)
    def numbers_validator(cls, numbers: List[str]):
        """
        Platform returns NANP numbers w/o +1
        :param numbers:
        :return:
        """
        return [assert_plus1(number) for number in numbers]

    def dict(self, *args, **kwargs):
        """
        When serializing remove the +1- again
        :param args:
        :param kwargs:
        :return:
        """
        numbers = self.numbers
        if numbers:
            self.numbers = [strip_plus1(number) for number in numbers]
        r = super().dict(*args, **kwargs)
        self.numbers = numbers
        return r


class CallsFrom(ApiModel):
    """
    calls_from specification in forwarding rule
    """
    selection: ForwardFromSelection = Field(default=ForwardFromSelection.any)
    custom_numbers: CustomNumbers = Field(default_factory=CustomNumbers)


class ForwardingRuleDetails(ApiModel):
    """
    Details of a call forwarding rule
    """
    name: str
    id: Optional[str]
    enabled: bool
    holiday_schedule: Optional[str]
    business_schedule: Optional[str]
    forward_to: ForwardTo
    calls_to: ForwardCallsTo
    calls_from: CallsFrom

    @staticmethod
    def default(name: str) -> 'ForwardingRuleDetails':
        return ForwardingRuleDetails(name=name,
                                     enabled=True,
                                     forward_to=ForwardTo(),
                                     calls_to=ForwardCallsTo(),
                                     calls_from=CallsFrom())


class FeatureSelector(str, Enum):
    queues = 'queues'
    huntgroups = 'huntGroups'


class ForwardingAPI:
    """
    API for forwarding settings on call queues and hunt groups
    """

    def __init__(self, session: RestSession, feature_selector: FeatureSelector):
        self._session = session
        self._feature = feature_selector

    def _endpoint(self, location_id: str, feature_id: str, path: str = None):
        """

        :meta private:
        :param location_id:
        :param feature_id:
        :param path:
        :return:
        """
        path = path and f'/path' or ''
        ep = self._session.ep(path=f'telephony/config/locations/{location_id}/{self._feature.value}/'
                                   f'{feature_id}/callForwarding{path}')
        return ep

    def settings(self, location_id: str, feature_id: str, org_id: str = None) -> CallForwarding:
        """
        Retrieve Call Forwarding settings for the designated call queue or hunt group including the list of call 
        forwarding rules.

        :param location_id: Location in which this call queue or hunt group exists.
        :param feature_id: Retrieve the call forwarding settings for this call queue or hunt groupe.
        :param org_id: Retrieve call queue or hunt group settings from this organization.
        :return:
        """
        params = org_id and {'orgId': org_id} or {}
        url = self._endpoint(location_id=location_id, feature_id=feature_id)
        data = self._session.rest_get(url=url, params=params)
        result = CallForwarding.parse_obj(data['callForwarding'])
        return result

    def update_forwarding(self, location_id: str, feature_id: str,
                          forwarding: CallForwarding, org_id: str = None):
        params = org_id and {'orgId': org_id} or {}
        url = self._endpoint(location_id=location_id, feature_id=feature_id)
        body = forwarding.dict()

        # update only has 'id' and 'enabled' in rules
        # determine names of ForwardingRule fields to remove
        to_pop = [field
                  for field in ForwardingRule.__fields__
                  if field not in {'id', 'enabled'}]
        for rule in body['rules']:
            rule: Dict
            for field in to_pop:
                rule.pop(field, None)
        body = {'callForwarding': body}
        self._session.rest_put(url=url, json=body, params=params)

    def create_call_forwarding_rule(self, location_id: str, feature_id: str,
                                    forwarding_rule: ForwardingRuleDetails, org_id: str = None) -> str:
        """
        Create a Selective Call Forwarding Rule for the designated call queue or hunt group.

        A selective call forwarding rule for a call queue or hunt group allows calls to be forwarded or not 
        forwarded to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the call queue or hunt group's call 
        forwarding settings.
        :param location_id: Location in which the call queue exists.
        :param feature_id: Create the rule for this call queue or hunt group.
        :param forwarding_rule: details of rule to be created
        :param org_id: Create the call queue or hunt group rule for this organization.
        :return:
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules')
        body = forwarding_rule.dict()
        params = org_id and {'orgId': org_id} or None
        data = self._session.rest_post(url=url, json=body, params=params)
        return data['id']

    def call_forwarding_rule(self, location_id: str, feature_id: str, rule_id: str,
                             org_id: str = None) -> ForwardingRuleDetails:
        """
        Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue.

        A selective call forwarding rule for a call queue or hunt group allows calls to be forwarded or not forwarded 
        to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the call queue or hunt group's call 
        forwarding settings.
        :param location_id: Location in which to call queue or hunt group exists.
        :param feature_id: Retrieve setting for a rule for this call queue or hunt group.
        :param rule_id: call queue or hunt group rule you are retrieving settings for.
        :param org_id: Retrieve call queue or hunt group forwarding settings from this organization.
        :return:
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules/{rule_id}')
        params = org_id and {'orgId': org_id} or None
        data = self._session.rest_get(url=url, params=params)
        result = ForwardingRuleDetails.parse_obj(data)
        return result

    def update_call_forwarding_rule(self, location_id: str, feature_id: str, rule_id: str,
                                          forwarding_rule: ForwardingRuleDetails, org_id: str = None):
        """
        Update a Selective Call Forwarding Rule's settings for the designated call queue or hunt group.

        A selective call forwarding rule for a call queue or hunt group allows calls to be forwarded or not forwarded 
        to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the call queue or hunt group's call 
        forwarding settings.

        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.
        :param location_id: Location in which to call queue or hunt group exists.
        :param feature_id: Update settings for a rule for this call queue or hunt group.
        :param rule_id: Call queue or hunt group rule you are updating settings for.
        :param forwarding_rule: forwarding rule details for update
        :param org_id: Update call queue or hunt group rule settings for this organization.
        :return:
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules/{rule_id}')
        params = org_id and {'orgId': org_id} or None
        body = forwarding_rule.dict()
        data = self._session.rest_put(url=url, params=params, json=body)
        return data['id']

    def delete_call_forwarding_rule(self, location_id: str, feature_id: str, rule_id: str, org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for the designated Call queue or hunt group.

        A selective call forwarding rule for a call queue or hunt group allows calls to be forwarded or not forwarded 
        to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the call queue or hunt group's call
        forwarding
        settings.
        :return:
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules/{rule_id}')
        params = org_id and {'orgId': org_id} or None
        self._session.delete(url=url, params=params)

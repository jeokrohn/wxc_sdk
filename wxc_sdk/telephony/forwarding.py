"""
Forwarding settings and API for call queues, hunt groups, and auto attendants
"""

from enum import Enum
from typing import Optional, Dict

from pydantic import Field, validator

from ..base import ApiModel
from ..rest import RestSession

__all__ = ['ForwardingRule', 'ForwardingSetting', 'CallForwarding', 'ForwardToSelection', 'CallForwardingNumberType',
           'CallForwardingNumber', 'ForwardCallsTo', 'CustomNumbers', 'CallsFrom', 'ForwardingRuleDetails',
           'FeatureSelector', 'ForwardingApi']


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
    rules: list[ForwardingRule]

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
    numbers: list[CallForwardingNumber] = Field(default_factory=list)


class CustomNumbers(ApiModel):
    """
    custom numbers definition in forwarding rule
    """
    private_number_enabled: bool = Field(default=False)
    unavailable_number_enabled: bool = Field(default=False)
    numbers: Optional[list[str]]

    @validator('numbers', pre=True)
    def numbers_validator(cls, numbers: list[str]):
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
    auto_attendants = 'autoAttendants'


class ForwardingApi:
    """
    API for forwarding settings on call queues, hunt groups, and auto attendants
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
        path = path and f'/{path}' or ''
        ep = self._session.ep(path=f'telephony/config/locations/{location_id}/{self._feature.value}/'
                                   f'{feature_id}/callForwarding{path}')
        return ep

    def settings(self, location_id: str, feature_id: str, org_id: str = None) -> CallForwarding:
        """
        Retrieve Call Forwarding settings for the designated feature including the list of call
        forwarding rules.

        :param location_id: Location in which this feature exists.
        :type location_id: str
        :param feature_id: Retrieve the call forwarding settings for this entity
        :type feature_id: str
        :param org_id: Retrieve call forwarding settings from this organization.
        :type org_id: str
        :return: call forwarding settings
        :rtype: class:`CallForwarding`
        """
        params = org_id and {'orgId': org_id} or {}
        url = self._endpoint(location_id=location_id, feature_id=feature_id)
        data = self._session.rest_get(url=url, params=params)
        result = CallForwarding.parse_obj(data['callForwarding'])
        return result

    def update(self, location_id: str, feature_id: str,
               forwarding: CallForwarding, org_id: str = None):
        """
        Update Call Forwarding Settings for a feature

        Update Call Forwarding settings for the designated feature.

        Updating call forwarding settings for a feature requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this feature exists.
        :type location_id: str
        :param feature_id: Update call forwarding settings for this feature.
        :type feature_id: str
        :param forwarding: Forwarding settings
        :type forwarding: :class:`CallForwarding`
        :param org_id: Update feature forwarding settings from this organization.
        :type org_id: str
        """
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
        Create a Selective Call Forwarding Rule feature

        A selective call forwarding rule for feature to be forwarded or not
        forwarded to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available feature's call
        forwarding settings.
        :param location_id: Location in which the call queue exists.
        :type location_id: str
        :param feature_id: Create the rule for this feature
        :type feature_id: str
        :param forwarding_rule: details of rule to be created
        :type forwarding_rule: :class:`ForwardingRuleDetails`
        :param org_id: Create the feature forwarding rule for this organization.
        :type org_id: str
        :return: forwarding rule id
        :rtype; str
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path='selectiveRules')
        body = forwarding_rule.dict()
        params = org_id and {'orgId': org_id} or None
        data = self._session.rest_post(url=url, json=body, params=params)
        return data['id']

    def call_forwarding_rule(self, location_id: str, feature_id: str, rule_id: str,
                             org_id: str = None) -> ForwardingRuleDetails:
        """
        Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue.

        A selective call forwarding rule for feature allows calls to be forwarded or not forwarded
        to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the feature's call
        forwarding settings.
        :param location_id: Location in which the feature exists.
        :type location_id: stre
        :param feature_id: Retrieve setting for a rule for this feature.
        :type feature_id: str
        :param rule_id: feature rule you are retrieving settings for.
        :type rule_id: str
        :param org_id: Retrieve feature forwarding settings from this organization.
        :type org_id: str
        :return: call forwarding rule details
        :rtype: :class:`ForwardingRuleDetails`
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules/{rule_id}')
        params = org_id and {'orgId': org_id} or None
        data = self._session.rest_get(url=url, params=params)
        result = ForwardingRuleDetails.parse_obj(data)
        return result

    def update_call_forwarding_rule(self, location_id: str, feature_id: str, rule_id: str,
                                    forwarding_rule: ForwardingRuleDetails, org_id: str = None) -> str:
        """
        Update a Selective Call Forwarding Rule's settings for the designated feature.

        A selective call forwarding rule for feature allows calls to be forwarded or not forwarded
        to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the feature's call
        forwarding settings.

        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which the feature exists.
        :type location_id: str
        :param feature_id: Update settings for a rule for this feature.
        :type feature_id: str
        :param rule_id: feature you are updating settings for.
        :type rule_id: str
        :param forwarding_rule: forwarding rule details for update
        :type forwarding_rule: :class:`ForwardingRuleDetails`
        :param org_id: Update feature rule settings for this organization.
        :type org_id: str
        :return: new call forwarding rule id
        :rtype: str
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules/{rule_id}')
        params = org_id and {'orgId': org_id} or None
        body = forwarding_rule.dict()
        data = self._session.rest_put(url=url, params=params, json=body)
        return data['id']

    def delete_call_forwarding_rule(self, location_id: str, feature_id: str, rule_id: str, org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for the designated feature.

        A selective call forwarding rule for a feature allows calls to be forwarded or not forwarded
        to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the feature's call
        forwarding
        settings.
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules/{rule_id}')
        params = org_id and {'orgId': org_id} or None
        self._session.delete(url=url, params=params)

"""
Forwarding settings and API for call queues, hunt groups, and auto attendants
"""
import json
from typing import Optional

from pydantic import Field, field_validator

from ..base import ApiModel
from ..base import SafeEnum as Enum
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
    name: Optional[str] = None
    calls_from: Optional[str] = None
    forward_to: Optional[str] = None
    calls_to: Optional[str] = None
    enabled: bool


class ForwardingSetting(ApiModel):
    #: `Always` call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "Always" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    destination_voice_mail_enabled: Optional[bool] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    send_to_voicemail_enabled: Optional[bool] = None

    @staticmethod
    def default() -> 'ForwardingSetting':
        return ForwardingSetting(enabled=False,
                                 ring_reminder_enabled=False,
                                 send_to_voicemail_enabled=False,
                                 destination='')


class CallForwarding(ApiModel):
    always: ForwardingSetting
    selective: ForwardingSetting
    rules: Optional[list[ForwardingRule]] = None

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
    phone_number: Optional[str] = None


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
    phone_number: Optional[str] = None
    extension: Optional[str] = None
    number_type: CallForwardingNumberType = Field(alias='type')

    @field_validator('phone_number', mode='before')
    def validate_phone_number(cls, v):
        """
        Platform returns NANP numbers w/o +
        :meta private:
        """
        return assert_plus1(v)

    def model_dump(self, *args, **kwargs):
        """
        When serializing remove the +1- again
        """
        number = self.phone_number
        self.phone_number = strip_plus1(number)
        r = super().model_dump(*args, **kwargs)
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
    numbers: Optional[list[str]] = None

    @field_validator('numbers', mode='before')
    def numbers_validator(cls, numbers: list[str]):
        """
        :meta private:
        """
        return [assert_plus1(number) for number in numbers]

    def model_dump(self, *args, **kwargs):
        """
        When serializing remove the +1- again
        :meta private:
        """
        numbers = self.numbers
        if numbers:
            self.numbers = [strip_plus1(number) for number in numbers]
        r = super().model_dump(*args, **kwargs)
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
    #: A unique identifier for the auto attendant call forward selective rule.
    id: Optional[str] = None
    #: Flag to indicate if always call forwarding selective rule criteria is active. If not set, flag will be set to
    #: false.
    enabled: bool
    #: Name of the holiday schedule which determines when this selective call forwarding rule is in effect.
    holiday_schedule: Optional[str] = None
    #: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
    business_schedule: Optional[str] = None
    #: Number to which calls will be forwarded if the rule is of type "Forward To" and the incoming call is matched.
    forward_to: ForwardTo
    #: Comma-separated list of the types of numbers being matched for incoming call destination.
    calls_to: ForwardCallsTo
    #: Comma-separated list of incoming call numbers that, when matched, will not be forwarded. A Limit of 12 numbers
    #: is allowed. Use Any private Number in the comma-separated value to indicate rules that match incoming calls from
    #: a private number. Use Any unavailable number in the comma-separated value to match incoming calls from an
    #: unavailable number.
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
        result = CallForwarding.model_validate(data['callForwarding'])
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

        body = {'callForwarding': json.loads(forwarding.model_dump_json(exclude={'rules': {'__all__': {'calls_from',
                                                                                                       'forward_to',
                                                                                                       'calls_to',
                                                                                                       'name'}}}))}
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
        params = org_id and {'orgId': org_id} or None
        body = forwarding_rule.model_dump_json()
        data = self._session.rest_post(url=url, data=body, params=params)
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
        result = ForwardingRuleDetails.model_validate(data)
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
        body = forwarding_rule.model_dump_json(exclude={'id'})
        data = self._session.rest_put(url=url, params=params, data=body)
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
        self._session.rest_delete(url=url, params=params)

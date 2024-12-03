from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CallForwardRulesGet', 'CallForwardRulesSet', 'CallForwardSettingsGetCallForwarding',
           'CallForwardSettingsGetCallForwardingAlways', 'CallForwardSettingsGetCallForwardingOperatingModes',
           'CallForwardSettingsGetCallForwardingOperatingModesExceptionType',
           'FeaturesCallQueueCallForwardingWithModeManagementApi', 'ModesGet', 'ModesGetForwardTo',
           'ModesGetForwardToDefaultForwardToSelection', 'ModesGetForwardToSelection', 'ModesGetLevel',
           'ModesGetType', 'ModesPatch', 'ModesPatchForwardTo', 'ModifyCallForwardingObjectCallForwarding']


class CallForwardSettingsGetCallForwardingAlways(ApiModel):
    #: `Always` call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for "Always" call forwarding.
    #: example: 2225551212
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardSettingsGetCallForwardingOperatingModesExceptionType(str, Enum):
    #: The mode was switched to or extended by the user for manual switch back and runs as an exception until the user
    #: manual switches the feature back to normal operation or a different mode.
    manual_switch_back = 'MANUAL_SWITCH_BACK'
    #: The mode was switched to by the user before its start time and runs as an exception until its end time is
    #: reached at which point it automatically switches the feature back to normal operation.
    automatic_switch_back_early_start = 'AUTOMATIC_SWITCH_BACK_EARLY_START'
    #: The current mode was extended by the user before its end time and runs as an exception until the extension end
    #: time (mode's end time + extension of up to 12 hours) is reached at which point it automatically switches the
    #: feature back to normal operation.
    automatic_switch_back_extension = 'AUTOMATIC_SWITCH_BACK_EXTENSION'
    #: The mode will remain the current operating mode for the feature until its normal end time is reached.
    automatic_switch_back_standard = 'AUTOMATIC_SWITCH_BACK_STANDARD'


class ModesGetType(str, Enum):
    #: The operating mode is not scheduled.
    none_ = 'NONE'
    #: Single time duration for Monday-Friday and single time duration for Saturday-Sunday.
    same_hours_daily = 'SAME_HOURS_DAILY'
    #: Individual time durations for every day of the week.
    different_hours_daily = 'DIFFERENT_HOURS_DAILY'
    #: Holidays which have date durations spanning multiple days, as well as an optional yearly recurrence by day or
    #: date.
    holiday = 'HOLIDAY'


class ModesGetLevel(str, Enum):
    #: The operating mode is at the location level.
    location = 'LOCATION'
    #: The operating mode is at the organization level.
    organization = 'ORGANIZATION'


class ModesGetForwardToSelection(str, Enum):
    #: When the rule matches,the mode's own default forwarding selection is to be applied.
    forward_to_default_number = 'FORWARD_TO_DEFAULT_NUMBER'
    #: When the rule matches, forward to the destination.
    forward_to_specified_number = 'FORWARD_TO_SPECIFIED_NUMBER'
    #: When the rule matches, do not forward to another number.
    do_not_forward = 'DO_NOT_FORWARD'


class ModesGetForwardToDefaultForwardToSelection(str, Enum):
    #: When the rule matches, forward to the destination.
    forward_to_specified_number = 'FORWARD_TO_SPECIFIED_NUMBER'
    #: When the rule matches, do not forward to another number.
    do_not_forward = 'DO_NOT_FORWARD'


class ModesGetForwardTo(ApiModel):
    #: The selection for forwarding.
    #: example: FORWARD_TO_SPECIFIED_NUMBER
    selection: Optional[ModesGetForwardToSelection] = None
    #: The destination for forwarding. Required when the selection is set to `FORWARD_TO_SPECIFIED_NUMBER`.
    #: example: +19705550006
    destination: Optional[str] = None
    #: Destination voicemail is enabled.
    destination_voicemail_enabled: Optional[bool] = None
    #: The operating mode's destination.
    #: example: 00000
    default_destination: Optional[str] = None
    #: The operating mode's destination voicemail enabled.
    default_destination_voicemail_enabled: Optional[bool] = None
    #: The operating mode's forward to selection.
    #: example: DO_NOT_FORWARD
    default_forward_to_selection: Optional[ModesGetForwardToDefaultForwardToSelection] = None


class ModesGet(ApiModel):
    #: Normal operation is enabled or disabled.
    #: example: True
    normal_operation_enabled: Optional[bool] = None
    #: The ID of the operating mode.
    #: example: Y2lzY29zcGFyazovL3VzL09QRVJBVElOR19NT0RFL2JiOTc1OTcxLTBjZWYtNDdhNi05Yzc5LTliZWFjY2IwYjg4Mg
    id: Optional[str] = None
    #: The name of the operating mode.
    #: example: Day
    name: Optional[str] = None
    #: The type of the operating mode.
    #: example: SAME_HOURS_DAILY
    type: Optional[ModesGetType] = None
    #: The level of the operating mode.
    #: example: LOCATION
    level: Optional[ModesGetLevel] = None
    #: Forward to settings.
    forward_to: Optional[ModesGetForwardTo] = None


class CallForwardSettingsGetCallForwardingOperatingModes(ApiModel):
    #: Operating modes are enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: The ID of the current operating mode.
    #: example: Y2lzY29zcGFyazovL3VzL09QRVJBVElOR19NT0RFL2JiOTc1OTcxLTBjZWYtNDdhNi05Yzc5LTliZWFjY2IwYjg4Mg
    current_operating_mode_id: Optional[str] = None
    #: The exception type.
    #: example: MANUAL_SWITCH_BACK
    exception_type: Optional[CallForwardSettingsGetCallForwardingOperatingModesExceptionType] = None
    #: Operating modes.
    modes: Optional[list[ModesGet]] = None


class CallForwardRulesGet(ApiModel):
    #: Unique ID for the rule.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfRk9SV0FSRElOR19TRUxFQ1RJVkVfUlVMRS9kR1Z6ZEZKMWJHVTA
    id: Optional[str] = None
    #: Unique name of rule.
    #: example: My Rule
    name: Optional[str] = None
    #: Comma-separated list of incoming call numbers that, when matched, will not be forwarded. A Limit of 12 numbers
    #: is allowed. Use `Any private Number` in the comma-separated value to indicate rules that match incoming calls
    #: from a private number. Use `Any unavailable number` in the comma-separated value to match incoming calls from
    #: an unavailable number.
    #: example: Any private Number,2025551212
    call_from: Optional[str] = None
    #: Comma-separated list of the types of numbers being matched for incoming call destination.
    #: example: Primary
    calls_to: Optional[str] = None
    #: Number to which calls will be forwarded if the rule is of type "Forward To" and the incoming call is matched.
    #: example: 2025557736
    forward_to: Optional[str] = None
    #: Reflects if rule is enabled.
    #: example: True
    enabled: Optional[bool] = None


class CallForwardSettingsGetCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesGet]] = None
    #: Settings related to operating modes.
    operating_modes: Optional[CallForwardSettingsGetCallForwardingOperatingModes] = None


class CallForwardRulesSet(ApiModel):
    #: Unique ID for the rule.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfRk9SV0FSRElOR19TRUxFQ1RJVkVfUlVMRS9kR1Z6ZEZKMWJHVTA
    id: Optional[str] = None
    #: Reflects if rule is enabled.
    #: example: True
    enabled: Optional[bool] = None


class ModesPatchForwardTo(ApiModel):
    #: The selection for forwarding.
    #: example: FORWARD_TO_SPECIFIED_NUMBER
    selection: Optional[ModesGetForwardToSelection] = None
    #: The destination for forwarding. Required when the selection is set to `FORWARD_TO_SPECIFIED_NUMBER`.
    #: example: +19705550006
    destination: Optional[str] = None
    #: Destination voicemail is enabled.
    destination_voicemail_enabled: Optional[bool] = None


class ModesPatch(ApiModel):
    #: Normal operation is enabled or disabled.
    #: example: True
    normal_operation_enabled: Optional[bool] = None
    #: The ID of the operating mode.
    #: example: Y2lzY29zcGFyazovL3VzL09QRVJBVElOR19NT0RFL2JiOTc1OTcxLTBjZWYtNDdhNi05Yzc5LTliZWFjY2IwYjg4Mg
    id: Optional[str] = None
    #: Forward to settings.
    forward_to: Optional[ModesPatchForwardTo] = None


class ModifyCallForwardingObjectCallForwarding(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[CallForwardSettingsGetCallForwardingAlways] = None
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesSet]] = None
    #: Configuration for forwarding via Operating modes (Schedule Based Routing).
    modes: Optional[list[ModesPatch]] = None


class FeaturesCallQueueCallForwardingWithModeManagementApi(ApiChild, base='telephony/config/locations'):
    """
    Features: Call Queue Call Forwarding with Mode Management
    
    Features: The Call Queue feature allows for both reading and writing Webex Calling Call Queue settings for a
    specific organization.
    
    Supervisors are users responsible for managing agents. Their functions include monitoring and coaching, among other
    tasks.
    
    To view  these read-only organization settings, a user needs  a full or read-only administrator or location
    administrator auth token with a scope of `spark-admin:telephony_config_read`.
    
    To modify these organization settings, a user needs a full administrator or location administrator auth token with
    a scope of `spark-admin:telephony_config_write`.
    
    Using the optional ' orgId ' query parameter, a partner administrator can retrieve or change settings in a
    customer's organization
    """

    def get_call_forwarding_settings_for_a_call_queue(self, location_id: str, queue_id: str,
                                                      org_id: str = None) -> CallForwardSettingsGetCallForwarding:
        """
        Get Call Forwarding Settings for a Call Queue

        Retrieve Call Forwarding settings for the specified Call Queue, including the list of call forwarding rules.

        The call forwarding feature allows you to direct all incoming calls based on specific criteria that you define.
        Below are the available options for configuring your call forwarding:
        1. Always forward calls to a designated number.
        2. Forward calls to a designated number based on certain criteria.
        3. Forward calls using different modes.

        Retrieving call forwarding settings for a call queue requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Retrieve the call forwarding settings for this call queue.
        :type queue_id: str
        :param org_id: Retrieve call queue forwarding settings from this organization.
        :type org_id: str
        :rtype: CallForwardSettingsGetCallForwarding
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/queues/{queue_id}/callForwarding')
        data = super().get(url, params=params)
        r = CallForwardSettingsGetCallForwarding.model_validate(data['callForwarding'])
        return r

    def update_call_forwarding_settings_for_a_call_queue(self, location_id: str, queue_id: str,
                                                         call_forwarding: ModifyCallForwardingObjectCallForwarding = None,
                                                         org_id: str = None):
        """
        Update Call Forwarding Settings for a Call Queue

        Update Call Forwarding settings for the designated Call Queue.

        The call forwarding feature allows you to direct all incoming calls based on specific criteria that you define.
        Below are the available options for configuring your call forwarding:
        1. Always forward calls to a designated number.
        2. Forward calls to a designated number based on certain criteria.
        3. Forward calls using different modes.

        Updating call forwarding settings for a call queue requires a full administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update call forwarding settings for this call queue.
        :type queue_id: str
        :param call_forwarding: Settings related to `Always`, `Busy`, and `No Answer` call forwarding.
        :type call_forwarding: ModifyCallForwardingObjectCallForwarding
        :param org_id: Update call queue forwarding settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{location_id}/queues/{queue_id}/callForwarding')
        super().put(url, params=params, json=body)

    def switch_mode_for_call_forwarding_settings_for_a_call_queue(self, location_id: str, queue_id: str,
                                                                  org_id: str = None):
        """
        Switch Mode for Call Forwarding Settings for a Call Queue

        Switches the current operating mode of the `Call Queue` to the mode as per normal operations.

        Switching operating mode for a `call queue` requires a full, or location administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param location_id: `Location` in which this `call queue` exists.
        :type location_id: str
        :param queue_id: Switch operating mode to normal operations for this `call queue`.
        :type queue_id: str
        :param org_id: Switch operating mode as per normal operations for the `call queue` from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/queues/{queue_id}/callForwarding/actions/switchMode/invoke')
        super().post(url, params=params)

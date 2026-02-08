from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ActionToBePerformedObject', 'ActionToBePerformedObjectAction', 'AlternateNumbersObject',
           'AlternateNumbersObjectRingPattern', 'AudioAnnouncementFileGetObject', 'AudioAnnouncementFileObjectLevel',
           'AudioAnnouncementFileObjectMediaFileType', 'AutoAttendantCallForwardAvailableNumberObject',
           'AutoAttendantCallForwardAvailableNumberObjectOwner', 'AutoAttendantCallForwardSettingsDetailsObject',
           'AutoAttendantCallForwardSettingsDetailsObjectOperatingModes',
           'AutoAttendantCallForwardSettingsDetailsObjectOperatingModesExceptionType',
           'AutoAttendantCallForwardSettingsModifyDetailsObject', 'AutoAttendantPrimaryAvailableNumberObject',
           'CallForwardRulesModifyObject', 'CallForwardRulesObject',
           'CallForwardSelectiveCallsFromCustomNumbersObject', 'CallForwardSelectiveCallsFromObject',
           'CallForwardSelectiveCallsFromObjectSelection', 'CallForwardSelectiveCallsToNumbersObject',
           'CallForwardSelectiveCallsToNumbersObjectType', 'CallForwardSelectiveCallsToObject',
           'CallForwardSelectiveForwardToObject', 'CallForwardSelectiveForwardToObjectSelection',
           'CallTreatmentObject', 'CallTreatmentObjectRetryAttemptForNoInput', 'DirectLineCallerIdNameObjectForPut',
           'FeaturesAutoAttendantApi', 'GetAnnouncementFileInfo', 'GetAutoAttendantCallForwardSelectiveRuleObject',
           'GetAutoAttendantObject', 'GetAutoAttendantObjectExtensionDialing', 'GetCallForwardAlwaysSettingObject',
           'HoursMenuGetObject', 'HoursMenuGetObjectGreeting', 'KeyConfigurationsGetObject',
           'KeyConfigurationsGetObjectAction', 'KeyConfigurationsGetObjectKey', 'Level', 'ListAutoAttendantObject',
           'MediaType', 'ModesGet', 'ModesGetForwardTo', 'ModesGetForwardToDefaultForwardToSelection', 'ModesGetType',
           'ModesPatch', 'ModesPatchForwardTo', 'NumberOwnerType', 'STATE', 'SelectionObject', 'TelephonyType']


class AlternateNumbersObjectRingPattern(str, Enum):
    normal = 'NORMAL'
    long_long = 'LONG_LONG'
    short_short_long = 'SHORT_SHORT_LONG'
    short_long_short = 'SHORT_LONG_SHORT'


class AlternateNumbersObject(ApiModel):
    #: Phone number defined as alternate number.
    phone_number: Optional[str] = None
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool] = None
    #: Ring pattern that will be used for the alternate number.
    ring_pattern: Optional[AlternateNumbersObjectRingPattern] = None


class AudioAnnouncementFileObjectMediaFileType(str, Enum):
    #: WAV File Extension.
    wav = 'WAV'
    #: WMA File Extension.
    wma = 'WMA'
    #: 3GP File Extension.
    d3_gp = '3GP'


class AudioAnnouncementFileObjectLevel(str, Enum):
    #: Specifies this audio file is configured across organisation.
    organization = 'ORGANIZATION'
    #: Specifies this audio file is configured across location.
    location = 'LOCATION'


class AudioAnnouncementFileGetObject(ApiModel):
    #: A unique identifier for the announcement.
    id: Optional[str] = None
    #: Audio announcement file name.
    file_name: Optional[str] = None
    #: Audio announcement file type.
    media_file_type: Optional[AudioAnnouncementFileObjectMediaFileType] = None
    #: Audio announcement file type location.
    level: Optional[AudioAnnouncementFileObjectLevel] = None


class AutoAttendantCallForwardSettingsDetailsObjectOperatingModesExceptionType(str, Enum):
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


class CallForwardSelectiveForwardToObjectSelection(str, Enum):
    #: When the rule matches, forward to the destination for the auto attendant.
    forward_to_default_number = 'FORWARD_TO_DEFAULT_NUMBER'
    #: When the rule matches, forward to the destination for this rule.
    forward_to_specified_number = 'FORWARD_TO_SPECIFIED_NUMBER'
    #: When the rule matches, do not forward to another number.
    do_not_forward = 'DO_NOT_FORWARD'


class ModesGetForwardToDefaultForwardToSelection(str, Enum):
    #: When the rule matches, forward to the destination for this rule.
    forward_to_specified_number = 'FORWARD_TO_SPECIFIED_NUMBER'
    #: When the rule matches, do not forward to another number.
    do_not_forward = 'DO_NOT_FORWARD'


class ModesGetForwardTo(ApiModel):
    #: The selection for forwarding.
    selection: Optional[CallForwardSelectiveForwardToObjectSelection] = None
    #: The destination for forwarding. Required when the selection is set to `FORWARD_TO_SPECIFIED_NUMBER`.
    destination: Optional[str] = None
    #: Sending incoming calls to voicemail is enabled/disabled when the destination is an internal phone number and
    #: that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None
    #: The operating mode's destination.
    default_destination: Optional[str] = None
    #: The operating mode's destination voicemail enabled.
    default_destination_voicemail_enabled: Optional[bool] = None
    #: The operating mode's forward to selection.
    default_forward_to_selection: Optional[ModesGetForwardToDefaultForwardToSelection] = None


class ModesGet(ApiModel):
    #: Normal operation is enabled or disabled.
    normal_operation_enabled: Optional[bool] = None
    #: The ID of the operating mode.
    id: Optional[str] = None
    #: The name of the operating mode.
    name: Optional[str] = None
    #: The type of the operating mode.
    type: Optional[ModesGetType] = None
    #: The level of the operating mode.
    level: Optional[AudioAnnouncementFileObjectLevel] = None
    #: Forward to settings.
    forward_to: Optional[ModesGetForwardTo] = None


class AutoAttendantCallForwardSettingsDetailsObjectOperatingModes(ApiModel):
    #: Operating modes are enabled or disabled.
    enabled: Optional[bool] = None
    #: The ID of the current operating mode.
    current_operating_mode_id: Optional[str] = None
    #: The exception type.
    exception_type: Optional[AutoAttendantCallForwardSettingsDetailsObjectOperatingModesExceptionType] = None
    #: Operating modes.
    modes: Optional[list[ModesGet]] = None


class GetCallForwardAlwaysSettingObject(ApiModel):
    #: `Always` call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for `Always` call forwarding. Required if field `enabled` is set to `true`.
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    send_to_voicemail_enabled: Optional[bool] = None


class CallForwardRulesObject(ApiModel):
    #: Unique ID for the rule.
    id: Optional[str] = None
    #: Unique name of rule.
    name: Optional[str] = None
    #: Comma-separated list of incoming call numbers that, when matched, will not be forwarded. A Limit of 12 numbers
    #: is allowed. Use `Any private Number` in the comma-separated value to indicate rules that match incoming calls
    #: from a private number. Use `Any unavailable number` in the comma-separated value to match incoming calls from
    #: an unavailable number.
    calls_from: Optional[str] = None
    #: Comma-separated list of the types of numbers being matched for incoming call destination.
    calls_to: Optional[str] = None
    #: Number to which calls will be forwarded if the rule is of type "Forward To" and the incoming call is matched.
    forward_to: Optional[str] = None
    #: Reflects if rule is enabled.
    enabled: Optional[bool] = None


class AutoAttendantCallForwardSettingsDetailsObject(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[GetCallForwardAlwaysSettingObject] = None
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[GetCallForwardAlwaysSettingObject] = None
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesObject]] = None
    #: Settings related to operating modes.
    operating_modes: Optional[AutoAttendantCallForwardSettingsDetailsObjectOperatingModes] = None


class CallForwardRulesModifyObject(ApiModel):
    #: A unique identifier for the auto attendant call forward selective rule.
    id: Optional[str] = None
    #: Flag to indicate if always call forwarding selective rule criteria is active. If not set, flag will be set to
    #: false.
    enabled: Optional[bool] = None


class ModesPatchForwardTo(ApiModel):
    #: The selection for forwarding.
    selection: Optional[CallForwardSelectiveForwardToObjectSelection] = None
    #: The destination for forwarding. Required when the selection is set to `FORWARD_TO_SPECIFIED_NUMBER`.
    destination: Optional[str] = None
    #: Sending incoming calls to voicemail is enabled/disabled when the destination is an internal phone number and
    #: that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class ModesPatch(ApiModel):
    #: Normal operation is enabled or disabled.
    normal_operation_enabled: Optional[bool] = None
    #: The ID of the operating mode.
    id: Optional[str] = None
    #: Forward to settings.
    forward_to: Optional[ModesPatchForwardTo] = None


class AutoAttendantCallForwardSettingsModifyDetailsObject(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[GetCallForwardAlwaysSettingObject] = None
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[GetCallForwardAlwaysSettingObject] = None
    #: Rules for selectively forwarding calls. (Rules which are omitted in the list will not be deleted.)
    rules: Optional[list[CallForwardRulesModifyObject]] = None
    #: Configuration for forwarding via Operating modes (Schedule Based Routing).
    modes: Optional[list[ModesPatch]] = None


class CallForwardSelectiveCallsFromCustomNumbersObject(ApiModel):
    #: Match if caller ID indicates the call is from a private number.
    private_number_enabled: Optional[bool] = None
    #: Match if callerID is unavailable.
    unavailable_number_enabled: Optional[bool] = None
    #: Array of number strings to be matched against incoming caller ID.
    numbers: Optional[list[str]] = None


class CallForwardSelectiveCallsFromObjectSelection(str, Enum):
    #: Rule matches for calls from any number.
    any = 'ANY'
    #: Rule matches based on the numbers and options in customNumbers.
    custom = 'CUSTOM'


class CallForwardSelectiveCallsFromObject(ApiModel):
    #: If `CUSTOM`, use `customNumbers` to specify which incoming caller ID values cause this rule to match. `ANY`
    #: means any incoming call matches assuming the rule is in effect based on the associated schedules.
    selection: Optional[CallForwardSelectiveCallsFromObjectSelection] = None
    #: Custom rules for matching incoming caller ID information. Mandatory if the selection option is set to `CUSTOM`.
    custom_numbers: Optional[CallForwardSelectiveCallsFromCustomNumbersObject] = None


class CallForwardSelectiveCallsToNumbersObjectType(str, Enum):
    #: Indicates that the given `phoneNumber` or `extension` associated with this rule's containing object is a primary
    #: number or extension.
    primary = 'PRIMARY'
    #: Indicates that the given `phoneNumber` or `extension` associated with this rule's containing object is an
    #: alternate number or extension.
    alternate = 'ALTERNATE'


class CallForwardSelectiveCallsToNumbersObject(ApiModel):
    #: AutoCalls To phone number. Either phone number or extension should be present as mandatory.
    phone_number: Optional[str] = None
    #: Calls To extension.  Either `phoneNumber` or `extension` is mandatory.
    extension: Optional[str] = None
    #: Calls to type options.
    type: Optional[CallForwardSelectiveCallsToNumbersObjectType] = None


class CallForwardSelectiveCallsToObject(ApiModel):
    #: Array of numbers to be matched against the calling destination number.
    numbers: Optional[list[CallForwardSelectiveCallsToNumbersObject]] = None


class CallForwardSelectiveForwardToObject(ApiModel):
    #: Phone number used if selection is `FORWARD_TO_SPECIFIED_NUMBER`.
    phone_number: Optional[str] = None
    #: Controls what happens when the rule matches.
    selection: Optional[CallForwardSelectiveForwardToObjectSelection] = None


class GetAutoAttendantCallForwardSelectiveRuleObject(ApiModel):
    #: Unique ID for the rule.
    id: Optional[str] = None
    #: Unique name for the selective rule in the auto attendant.
    name: Optional[str] = None
    #: Reflects if rule is enabled.
    enabled: Optional[bool] = None
    #: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
    business_schedule: Optional[str] = None
    #: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
    holiday_schedule: Optional[str] = None
    #: Controls what happens when the rule matches including the destination number for the call forwarding.
    forward_to: Optional[CallForwardSelectiveForwardToObject] = None
    #: Settings related to the rule matching based on incoming caller ID.
    calls_from: Optional[CallForwardSelectiveCallsFromObject] = None
    #: Settings related to the rule matching based on the destination number.
    calls_to: Optional[CallForwardSelectiveCallsToObject] = None


class GetAutoAttendantObjectExtensionDialing(str, Enum):
    enterprise = 'ENTERPRISE'
    group = 'GROUP'


class HoursMenuGetObjectGreeting(str, Enum):
    default = 'DEFAULT'
    custom = 'CUSTOM'


class KeyConfigurationsGetObjectKey(str, Enum):
    d0 = '0'
    d1 = '1'
    d2 = '2'
    d3 = '3'
    d4 = '4'
    d5 = '5'
    d6 = '6'
    d7 = '7'
    d8 = '8'
    d9 = '9'
    star = '*'
    hash = '#'


class KeyConfigurationsGetObjectAction(str, Enum):
    #: Plays a recorded message and then returns to the current Auto Attendant menu.
    play_announcement = 'PLAY_ANNOUNCEMENT'
    #: Transfers the call to the specified number, without playing a transfer prompt.
    transfer_with_prompt = 'TRANSFER_WITH_PROMPT'
    #: Plays the message and then transfers the call to the specified number.
    transfer_without_prompt = 'TRANSFER_WITHOUT_PROMPT'
    #: Plays the message and then transfers the call to the specified operator number.
    transfer_to_operator = 'TRANSFER_TO_OPERATOR'
    #: Prompts the user for an extension, and transfers the user to voice mailbox of the dialed extension.
    transfer_to_mailbox = 'TRANSFER_TO_MAILBOX'
    #: Brings the user into the automated name directory.
    name_dialing = 'NAME_DIALING'
    #: Prompts the user for an extension, and transfers the user.
    extension_dialing = 'EXTENSION_DIALING'
    #: Replays the Auto Attendant greeting.
    repeat_menu = 'REPEAT_MENU'
    #: Terminates the call.
    exit = 'EXIT'


class KeyConfigurationsGetObject(ApiModel):
    #: Key assigned to specific menu configuration.
    key: Optional[KeyConfigurationsGetObjectKey] = None
    #: Action assigned to specific menu key configuration.
    action: Optional[KeyConfigurationsGetObjectAction] = None
    #: The description of each menu key.
    description: Optional[str] = None
    #: Value based on actions.
    value: Optional[str] = None
    #: Pre-configured announcement audio files when PLAY_ANNOUNCEMENT is set.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject] = None


class CallTreatmentObjectRetryAttemptForNoInput(str, Enum):
    #: Announcement will not be repeated.
    no_repeat = 'NO_REPEAT'
    #: Repeat the announcement once.
    one_time = 'ONE_TIME'
    #: Repeat the announcement twice.
    two_times = 'TWO_TIMES'
    #: Repeat the announcement thrice.
    three_times = 'THREE_TIMES'


class ActionToBePerformedObjectAction(str, Enum):
    #: Plays a recorded message and then disconnects the call.
    play_message_and_disconnect = 'PLAY_MESSAGE_AND_DISCONNECT'
    #: Transfers the call to the specified number, without playing a transfer prompt.
    transfer_without_prompt = 'TRANSFER_WITHOUT_PROMPT'
    #: Plays the message and then transfers the call to the specified number.
    transfer_with_prompt = 'TRANSFER_WITH_PROMPT'
    #: Plays the message and then transfers the call to the specified operator number.
    transfer_to_operator = 'TRANSFER_TO_OPERATOR'
    #: Transfers the call to the configured mailbox, without playing a transfer prompt.
    transfer_to_mailbox = 'TRANSFER_TO_MAILBOX'
    #: Disconnect the call.
    disconnect = 'DISCONNECT'


class ActionToBePerformedObject(ApiModel):
    #: Action to perform after the retry attempt is reached.
    action: Optional[ActionToBePerformedObjectAction] = None
    #: Greeting type is defined when `action` is set to `PLAY_MESSAGE_AND_DISCONNECT`.
    greeting: Optional[HoursMenuGetObjectGreeting] = None
    #: Pre-configured announcement audio files when `action` is set to `PLAY_MESSAGE_AND_DISCONNECT` and `greeting` is
    #: set to `CUSTOM`.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject] = None
    #: Transfer call to the specified number when `action` is set to `TRANSFER_WITH_PROMPT`, `TRANSFER_WITHOUT_PROMPT`
    #: and `TRANSFER_TO_OPERATOR` and `TRANSFER_TO_MAILBOX`.
    transfer_call_to: Optional[str] = None


class CallTreatmentObject(ApiModel):
    #: Number of times to repeat the Welcome greeting when the user does not provide an input. By default, NO_REPEAT is
    #: set.
    retry_attempt_for_no_input: Optional[CallTreatmentObjectRetryAttemptForNoInput] = None
    #: Interval the Auto Attendant service waits before timing out. By default, 10 seconds. Min value is 1 and max
    #: value is 60.
    no_input_timer: Optional[str] = None
    #: Action to perform after the retry attempt is reached.
    action_to_be_performed: Optional[ActionToBePerformedObject] = None


class HoursMenuGetObject(ApiModel):
    #: Greeting type defined for the auto attendant.
    greeting: Optional[HoursMenuGetObjectGreeting] = None
    #: Flag to indicate if auto attendant extension is enabled or not.
    extension_enabled: Optional[bool] = None
    #: Announcement Audio File details.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject] = None
    #: Key configurations defined for the auto attendant.
    key_configurations: Optional[KeyConfigurationsGetObject] = None
    #: Call treatment details.
    call_treatment: Optional[CallTreatmentObject] = None


class SelectionObject(str, Enum):
    #: When this option is selected, `customName` is to be shown for this auto attendant.
    custom_name = 'CUSTOM_NAME'
    #: When this option is selected, `name` is to be shown for this auto attendant.
    display_name = 'DISPLAY_NAME'


class DirectLineCallerIdNameObjectForPut(ApiModel):
    #: The selection of the direct line caller ID name.
    selection: Optional[SelectionObject] = None
    #: Sets or clears the custom direct line caller ID name.  To clear the `customName`, the attribute must be set to
    #: null or empty string. Required if `selection` is set to `CUSTOM_NAME`.
    custom_name: Optional[str] = None


class GetAutoAttendantObject(ApiModel):
    #: A unique identifier for the auto attendant.
    id: Optional[str] = None
    #: Unique name for the auto attendant.
    name: Optional[str] = None
    #: Flag to indicate if auto attendant number is enabled or not.
    enabled: Optional[bool] = None
    #: Auto attendant phone number.  Either `phoneNumber` or `extension` is mandatory.
    phone_number: Optional[str] = None
    #: Auto attendant extension.  Either `phoneNumber` or `extension` is mandatory.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool] = None
    #: First name defined for an auto attendant. This field has been deprecated. Please use `directLineCallerIdName`
    #: and `dialByName` instead.
    first_name: Optional[str] = None
    #: Last name defined for an auto attendant. This field has been deprecated. Please use `directLineCallerIdName` and
    #: `dialByName` instead.
    last_name: Optional[str] = None
    #: Alternate numbers defined for the auto attendant.
    alternate_numbers: Optional[list[AlternateNumbersObject]] = None
    #: Language for the auto attendant.
    language: Optional[str] = None
    #: Language code for the auto attendant.
    language_code: Optional[str] = None
    #: Business hours defined for the auto attendant.
    business_schedule: Optional[str] = None
    #: Holiday defined for the auto attendant.
    holiday_schedule: Optional[str] = None
    #: Extension dialing setting. If the values are not set default will be set as `ENTERPRISE`.
    extension_dialing: Optional[GetAutoAttendantObjectExtensionDialing] = None
    #: Name dialing setting. If the values are not set default will be set as `ENTERPRISE`.
    name_dialing: Optional[GetAutoAttendantObjectExtensionDialing] = None
    #: Time zone defined for the auto attendant.
    time_zone: Optional[str] = None
    #: Business hours menu defined for the auto attendant.
    business_hours_menu: Optional[HoursMenuGetObject] = None
    #: After hours menu defined for the auto attendant.
    after_hours_menu: Optional[HoursMenuGetObject] = None
    #: Settings for the direct line caller ID name to be shown for this auto attendant.
    direct_line_caller_id_name: Optional[DirectLineCallerIdNameObjectForPut] = None
    #: The name to be used for dial by name functions.
    dial_by_name: Optional[str] = None


class ListAutoAttendantObject(ApiModel):
    #: A unique identifier for the auto attendant.
    id: Optional[str] = None
    #: Unique name for the auto attendant.
    name: Optional[str] = None
    #: Name of location for auto attendant.
    location_name: Optional[str] = None
    #: ID of location for auto attendant.
    location_id: Optional[str] = None
    #: Auto attendant phone number.  Either `phoneNumber` or `extension` is mandatory.
    phone_number: Optional[str] = None
    #: Auto attendant extension.  Either `phoneNumber` or `extension` is mandatory.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool] = None


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class AutoAttendantPrimaryAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    phone_number: Optional[str] = None
    #: Phone number's state.
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    is_service_number: Optional[bool] = None


class NumberOwnerType(str, Enum):
    #: PSTN phone number's owner is a workspace.
    place = 'PLACE'
    #: PSTN phone number's owner is a person.
    people = 'PEOPLE'
    #: PSTN phone number's owner is a Virtual Profile.
    virtual_line = 'VIRTUAL_LINE'
    #: PSTN phone number's owner is an auto-attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: PSTN phone number's owner is a call queue.
    call_queue = 'CALL_QUEUE'
    #: PSTN phone number's owner is a group paging.
    group_paging = 'GROUP_PAGING'
    #: PSTN phone number's owner is a hunt group.
    hunt_group = 'HUNT_GROUP'
    #: PSTN phone number's owner is a voice messaging.
    voice_messaging = 'VOICE_MESSAGING'
    #: PSTN phone number's owner is a Single Number Reach.
    office_anywhere = 'OFFICE_ANYWHERE'
    #: PSTN phone number's owner is a Contact Center link.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: PSTN phone number's owner is a Contact Center adapter.
    contact_center_adapter = 'CONTACT_CENTER_ADAPTER'
    #: PSTN phone number's owner is a route list.
    route_list = 'ROUTE_LIST'
    #: PSTN phone number's owner is a voicemail group.
    voicemail_group = 'VOICEMAIL_GROUP'
    #: PSTN phone number's owner is a collaborate bridge.
    collaborate_bridge = 'COLLABORATE_BRIDGE'


class AutoAttendantCallForwardAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which PSTN Phone number is assigned.
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner.
    type: Optional[NumberOwnerType] = None
    #: First name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE`
    #: or `VIRTUAL_LINE`.
    first_name: Optional[str] = None
    #: Last name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    last_name: Optional[str] = None
    #: Display name of the PSTN phone number's owner. This field will be present except when the owner `type` is
    #: `PEOPLE` or `VIRTUAL_LINE`.
    display_name: Optional[str] = None


class AutoAttendantCallForwardAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    phone_number: Optional[str] = None
    #: Extension for a PSTN phone number.
    extension: Optional[str] = None
    #: Phone number's state.
    state: Optional[STATE] = None
    #: If `true`, the phone number is used as a location CLID.
    is_main_number: Optional[bool] = None
    #: If `true`, the phone number is a toll-free number.
    toll_free_number: Optional[bool] = None
    #: The telephony type for the number.
    telephony_type: Optional[TelephonyType] = None
    #: If `true`, the phone number is a service number; otherwise, it is a standard number. Service numbers are
    #: high-utilization or high-concurrency PSTN phone numbers that are neither mobile nor toll-free.
    is_service_number: Optional[bool] = None
    owner: Optional[AutoAttendantCallForwardAvailableNumberObjectOwner] = None


class MediaType(str, Enum):
    #: WAV File Extension.
    wav = 'WAV'


class Level(str, Enum):
    #: Organization level.
    organization = 'ORGANIZATION'
    #: Location level.
    location = 'LOCATION'
    #: Entity level.
    entity = 'ENTITY'


class GetAnnouncementFileInfo(ApiModel):
    #: ID of the announcement.
    id: Optional[str] = None
    #: Name of greeting file.
    file_name: Optional[str] = None
    #: Size of greeting file in kilo-bytes.
    file_size: Optional[str] = None
    #: Media file type of the announcement.
    media_file_type: Optional[MediaType] = None
    #: Level where the announcement is created.
    level: Optional[Level] = None


class FeaturesAutoAttendantApi(ApiChild, base='telephony/config'):
    """
    Features:  Auto Attendant
    
    Features: Auto Attendant support reading and writing of Webex Calling Auto Attendant settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_auto_attendants(self, location_id: str = None, name: str = None, phone_number: str = None,
                                         org_id: str = None,
                                         **params) -> Generator[ListAutoAttendantObject, None, None]:
        """
        Read the List of Auto Attendants

        List all Auto Attendants for the organization.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param location_id: Return the list of auto attendants for this location.
        :type location_id: str
        :param name: Only return auto attendants with the matching name.
        :type name: str
        :param phone_number: Only return auto attendants with the matching phone number.
        :type phone_number: str
        :param org_id: List auto attendants for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListAutoAttendantObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if name is not None:
            params['name'] = name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        url = self.ep('autoAttendants')
        return self.session.follow_pagination(url=url, model=ListAutoAttendantObject, item_key='autoAttendants', params=params)

    def create_an_auto_attendant(self, location_id: str, name: str, business_schedule: str,
                                 business_hours_menu: HoursMenuGetObject, after_hours_menu: HoursMenuGetObject,
                                 phone_number: str = None, extension: str = None, first_name: str = None,
                                 last_name: str = None, alternate_numbers: list[AlternateNumbersObject] = None,
                                 language_code: str = None, holiday_schedule: str = None,
                                 extension_dialing: GetAutoAttendantObjectExtensionDialing = None,
                                 name_dialing: GetAutoAttendantObjectExtensionDialing = None, time_zone: str = None,
                                 direct_line_caller_id_name: DirectLineCallerIdNameObjectForPut = None,
                                 dial_by_name: str = None, org_id: str = None) -> str:
        """
        Create an Auto Attendant

        Create new Auto Attendant for the given location.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Creating an auto attendant requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.<div><Callout type="warning">The fields
        `directLineCallerIdName.selection`, `directLineCallerIdName.customName`, and `dialByName` are not supported in
        Webex for Government (FedRAMP). Instead, administrators must use the `firstName` and `lastName` fields to
        configure and view both caller ID and dial-by-name settings.</Callout></div>

        :param location_id: Create the auto attendant for this location.
        :type location_id: str
        :param name: Unique name for the auto attendant.
        :type name: str
        :param business_schedule: Business hours defined for the auto attendant.
        :type business_schedule: str
        :param business_hours_menu: Business hours menu defined for the auto attendant.
        :type business_hours_menu: HoursMenuGetObject
        :param after_hours_menu: After hours menu defined for the auto attendant.
        :type after_hours_menu: HoursMenuGetObject
        :param phone_number: Auto attendant phone number.  Either `phoneNumber` or `extension` is mandatory.
        :type phone_number: str
        :param extension: Auto attendant extension.  Either `phoneNumber` or `extension` is mandatory.
        :type extension: str
        :param first_name: First name defined for an auto attendant. This field has been deprecated. Please use
            `directLineCallerIdName` and `dialByName` instead.
        :type first_name: str
        :param last_name: Last name defined for an auto attendant. This field has been deprecated. Please use
            `directLineCallerIdName` and `dialByName` instead.
        :type last_name: str
        :param alternate_numbers: Alternate numbers defined for the auto attendant.
        :type alternate_numbers: list[AlternateNumbersObject]
        :param language_code: Announcement language code for the auto attendant.
        :type language_code: str
        :param holiday_schedule: Holiday defined for the auto attendant.
        :type holiday_schedule: str
        :param extension_dialing: Extension dialing setting. If the values are not set default will be set as
            `ENTERPRISE`.
        :type extension_dialing: GetAutoAttendantObjectExtensionDialing
        :param name_dialing: Name dialing setting. If the values are not set default will be set as `ENTERPRISE`.
        :type name_dialing: GetAutoAttendantObjectExtensionDialing
        :param time_zone: Time zone defined for the auto attendant.
        :type time_zone: str
        :param direct_line_caller_id_name: Settings for the direct line caller ID name to be shown for this auto
            attendant.
        :type direct_line_caller_id_name: DirectLineCallerIdNameObjectForPut
        :param dial_by_name: The name to be used for dial by name functions.  Characters of `%`,  `+`, `\`, `"` and
            Unicode characters are not allowed.
        :type dial_by_name: str
        :param org_id: Create the auto attendant for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if alternate_numbers is not None:
            body['alternateNumbers'] = TypeAdapter(list[AlternateNumbersObject]).dump_python(alternate_numbers, mode='json', by_alias=True, exclude_none=True)
        if language_code is not None:
            body['languageCode'] = language_code
        body['businessSchedule'] = business_schedule
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if extension_dialing is not None:
            body['extensionDialing'] = enum_str(extension_dialing)
        if name_dialing is not None:
            body['nameDialing'] = enum_str(name_dialing)
        if time_zone is not None:
            body['timeZone'] = time_zone
        body['businessHoursMenu'] = business_hours_menu.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['afterHoursMenu'] = after_hours_menu.model_dump(mode='json', by_alias=True, exclude_none=True)
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_name is not None:
            body['dialByName'] = dial_by_name
        url = self.ep(f'locations/{location_id}/autoAttendants')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def get_auto_attendant_alternate_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                             org_id: str = None,
                                                             **params) -> Generator[AutoAttendantPrimaryAvailableNumberObject, None, None]:
        """
        Get Auto Attendant Alternate Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the auto attendant's alternate
        number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AutoAttendantPrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'locations/{location_id}/autoAttendants/alternate/availableNumbers')
        return self.session.follow_pagination(url=url, model=AutoAttendantPrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_auto_attendant_primary_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                           org_id: str = None,
                                                           **params) -> Generator[AutoAttendantPrimaryAvailableNumberObject, None, None]:
        """
        Get Auto Attendant Primary Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the auto attendant's primary
        phone number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AutoAttendantPrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'locations/{location_id}/autoAttendants/availableNumbers')
        return self.session.follow_pagination(url=url, model=AutoAttendantPrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_auto_attendant_call_forward_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                                owner_name: str = None, extension: str = None,
                                                                org_id: str = None,
                                                                **params) -> Generator[AutoAttendantCallForwardAvailableNumberObject, None, None]:
        """
        Get Auto Attendant Call Forward Available Phone Numbers

        List the service and standard PSTN numbers that are available to be assigned as the auto attendant's call
        forward number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AutoAttendantCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'locations/{location_id}/autoAttendants/callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=AutoAttendantCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def delete_an_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None):
        """
        Delete an Auto Attendant

        Delete the designated Auto Attendant.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Deleting an auto attendant requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Location from which to delete an auto attendant.
        :type location_id: str
        :param auto_attendant_id: Delete the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Delete the auto attendant from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        super().delete(url, params=params)

    def get_details_for_an_auto_attendant(self, location_id: str, auto_attendant_id: str,
                                          org_id: str = None) -> GetAutoAttendantObject:
        """
        Get Details for an Auto Attendant

        Retrieve an Auto Attendant details.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Retrieving an auto attendant details requires a full or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.<div><Callout type="warning">The fields
        `directLineCallerIdName.selection`, `directLineCallerIdName.customName`, and `dialByName` are not supported in
        Webex for Government (FedRAMP). Instead, administrators must use the `firstName` and `lastName` fields to
        configure and view both caller ID and dial-by-name settings.</Callout></div>

        :param location_id: Retrieve an auto attendant details in this location.
        :type location_id: str
        :param auto_attendant_id: Retrieve the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Retrieve auto attendant details from this organization.
        :type org_id: str
        :rtype: :class:`GetAutoAttendantObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        data = super().get(url, params=params)
        r = GetAutoAttendantObject.model_validate(data)
        return r

    def update_an_auto_attendant(self, location_id: str, auto_attendant_id: str, name: str = None,
                                 phone_number: str = None, extension: str = None, first_name: str = None,
                                 last_name: str = None, alternate_numbers: list[AlternateNumbersObject] = None,
                                 language_code: str = None, business_schedule: str = None,
                                 holiday_schedule: str = None,
                                 extension_dialing: GetAutoAttendantObjectExtensionDialing = None,
                                 name_dialing: GetAutoAttendantObjectExtensionDialing = None, time_zone: str = None,
                                 business_hours_menu: HoursMenuGetObject = None,
                                 after_hours_menu: HoursMenuGetObject = None,
                                 direct_line_caller_id_name: DirectLineCallerIdNameObjectForPut = None,
                                 dial_by_name: str = None, org_id: str = None):
        """
        Update an Auto Attendant

        Update the designated Auto Attendant.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Updating an auto attendant requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.<div><Callout type="warning">The fields
        `directLineCallerIdName.selection`, `directLineCallerIdName.customName`, and `dialByName` are not supported in
        Webex for Government (FedRAMP). Instead, administrators must use the `firstName` and `lastName` fields to
        configure and view both caller ID and dial-by-name settings.</Callout></div>

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update an auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param name: Unique name for the auto attendant.
        :type name: str
        :param phone_number: Auto attendant phone number.  Either `phoneNumber` or `extension` is mandatory.
        :type phone_number: str
        :param extension: Auto attendant extension.  Either `phoneNumber` or `extension` is mandatory.
        :type extension: str
        :param first_name: First name defined for an auto attendant. This field has been deprecated. Please use
            `directLineCallerIdName` and `dialByName` instead.
        :type first_name: str
        :param last_name: Last name defined for an auto attendant. This field has been deprecated. Please use
            `directLineCallerIdName` and `dialByName` instead.
        :type last_name: str
        :param alternate_numbers: Alternate numbers defined for the auto attendant.
        :type alternate_numbers: list[AlternateNumbersObject]
        :param language_code: Announcement language code for the auto attendant.
        :type language_code: str
        :param business_schedule: Business hours defined for the auto attendant.
        :type business_schedule: str
        :param holiday_schedule: Holiday defined for the auto attendant.
        :type holiday_schedule: str
        :param extension_dialing: Extension dialing setting. If the values are not set default will be set as
            `ENTERPRISE`.
        :type extension_dialing: GetAutoAttendantObjectExtensionDialing
        :param name_dialing: Name dialing setting. If the values are not set default will be set as `ENTERPRISE`.
        :type name_dialing: GetAutoAttendantObjectExtensionDialing
        :param time_zone: Time zone defined for the auto attendant.
        :type time_zone: str
        :param business_hours_menu: Business hours menu defined for the auto attendant.
        :type business_hours_menu: HoursMenuGetObject
        :param after_hours_menu: After hours menu defined for the auto attendant.
        :type after_hours_menu: HoursMenuGetObject
        :param direct_line_caller_id_name: Settings for the direct line caller ID name to be shown for this auto
            attendant.
        :type direct_line_caller_id_name: DirectLineCallerIdNameObjectForPut
        :param dial_by_name: Sets or clears the name to be used for dial by name functions. To clear the `dialByName`,
            the attribute must be set to null or empty string. Characters of `%`,  `+`, `\`, `"` and Unicode
            characters are not allowed.
        :type dial_by_name: str
        :param org_id: Update an auto attendant from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if alternate_numbers is not None:
            body['alternateNumbers'] = TypeAdapter(list[AlternateNumbersObject]).dump_python(alternate_numbers, mode='json', by_alias=True, exclude_none=True)
        if language_code is not None:
            body['languageCode'] = language_code
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if extension_dialing is not None:
            body['extensionDialing'] = enum_str(extension_dialing)
        if name_dialing is not None:
            body['nameDialing'] = enum_str(name_dialing)
        if time_zone is not None:
            body['timeZone'] = time_zone
        if business_hours_menu is not None:
            body['businessHoursMenu'] = business_hours_menu.model_dump(mode='json', by_alias=True, exclude_none=True)
        if after_hours_menu is not None:
            body['afterHoursMenu'] = after_hours_menu.model_dump(mode='json', by_alias=True, exclude_none=True)
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_name is not None:
            body['dialByName'] = dial_by_name
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}')
        super().put(url, params=params, json=body)

    def read_the_list_of_auto_attendant_announcement_files(self, location_id: str, auto_attendant_id: str,
                                                           org_id: str = None) -> list[GetAnnouncementFileInfo]:
        """
        Read the List of Auto Attendant Announcement Files

        List file info for all auto attendant announcement files associated with this auto attendant.

        Auto attendant announcement files contain messages and music that callers hear while waiting in the queue. A
        auto attendant can be configured to play whatever subset of these announcement files is desired.

        Retrieving this list of files requires a full or read-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        Note that uploading of announcement files via API is not currently supported, but is available via Webex
        Control Hub.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Retrieve announcement files for the auto attendant with this identifier.
        :type auto_attendant_id: str
        :param org_id: Retrieve announcement files for a auto attendant from this organization.
        :type org_id: str
        :rtype: list[GetAnnouncementFileInfo]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/announcements')
        data = super().get(url, params=params)
        r = TypeAdapter(list[GetAnnouncementFileInfo]).validate_python(data['announcements'])
        return r

    def delete_a_auto_attendant_announcement_file(self, location_id: str, auto_attendant_id: str, file_name: str,
                                                  org_id: str = None):
        """
        Delete a Auto Attendant Announcement File

        Delete an announcement file for the designated auto attendant.

        Auto Attendant announcement files contain messages and music that callers hear while waiting in the queue. A
        auto attendant can be configured to play whatever subset of these announcement files is desired.

        Deleting an announcement file for a auto attendant requires a full administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Delete an announcement for a auto attendant in this location.
        :type location_id: str
        :param auto_attendant_id: Delete an announcement for the auto attendant with this identifier.
        :type auto_attendant_id: str
        :type file_name: str
        :param org_id: Delete auto attendant announcement from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/announcements/{file_name}')
        super().delete(url, params=params)

    def get_call_forwarding_settings_for_an_auto_attendant(self, location_id: str, auto_attendant_id: str,
                                                           org_id: str = None) -> AutoAttendantCallForwardSettingsDetailsObject:
        """
        Get Call Forwarding Settings for an Auto Attendant

        Retrieve Call Forwarding settings for the designated Auto Attendant including the list of call forwarding
        rules.

        The call forwarding feature allows you to direct all incoming calls based on specific criteria that you define.
        Below are the available options for configuring your call forwarding:
        1. Always forward calls to a designated number.
        2. Forward calls to a designated number based on certain criteria.
        3. Forward calls using different modes.

        Retrieving call forwarding settings for an auto attendant requires a full or read-only administrator or
        location administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Retrieve the call forwarding settings for this auto attendant.
        :type auto_attendant_id: str
        :param org_id: Retrieve auto attendant forwarding settings from this organization.
        :type org_id: str
        :rtype: AutoAttendantCallForwardSettingsDetailsObject
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding')
        data = super().get(url, params=params)
        r = AutoAttendantCallForwardSettingsDetailsObject.model_validate(data['callForwarding'])
        return r

    def update_call_forwarding_settings_for_an_auto_attendant(self, location_id: str, auto_attendant_id: str,
                                                              call_forwarding: AutoAttendantCallForwardSettingsModifyDetailsObject,
                                                              org_id: str = None):
        """
        Update Call Forwarding Settings for an Auto Attendant

        Update Call Forwarding settings for the designated Auto Attendant.

        The call forwarding feature allows you to direct all incoming calls based on specific criteria that you define.
        Below are the available options for configuring your call forwarding:
        1. Always forward calls to a designated number.
        2. Forward calls to a designated number based on certain criteria.
        3. Forward calls using different modes.

        Updating call forwarding settings for an auto attendant requires a full administrator or location administrator
        auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update call forwarding settings for this auto attendant.
        :type auto_attendant_id: str
        :param call_forwarding: Settings related to `Always`, `Busy`, and `No Answer` call forwarding.
        :type call_forwarding: AutoAttendantCallForwardSettingsModifyDetailsObject
        :param org_id: Update auto attendant forwarding settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding')
        super().put(url, params=params, json=body)

    def switch_mode_for_call_forwarding_settings_for_an_auto_attendant(self, location_id: str, auto_attendant_id: str,
                                                                       org_id: str = None):
        """
        Switch Mode for Call Forwarding Settings for an Auto Attendant

        Switches the current operating mode of the `Auto Attendant` to the mode as per normal operations.

        Switching operating mode for an `auto attendant` requires a full, or location administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param location_id: `Location` in which this `auto attendant` exists.
        :type location_id: str
        :param auto_attendant_id: Switch operating mode to normal operations for this `auto attendant`.
        :type auto_attendant_id: str
        :param org_id: Switch operating mode as per normal operations for the `auto attendant` from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/actions/switchMode/invoke')
        super().post(url, params=params)

    def create_a_selective_call_forwarding_rule_for_an_auto_attendant(self, location_id: str, auto_attendant_id: str,
                                                                      name: str,
                                                                      forward_to: CallForwardSelectiveForwardToObject,
                                                                      calls_from: CallForwardSelectiveCallsFromObject,
                                                                      enabled: bool = None,
                                                                      business_schedule: str = None,
                                                                      holiday_schedule: str = None,
                                                                      calls_to: CallForwardSelectiveCallsToObject = None,
                                                                      org_id: str = None) -> str:
        """
        Create a Selective Call Forwarding Rule for an Auto Attendant

        Create a Selective Call Forwarding Rule for the designated Auto Attendant.

        A selective call forwarding rule for an auto attendant allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the auto attendant's call forwarding
        settings.

        Creating a selective call forwarding rule for an auto attendant requires a full administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        **NOTE**: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which the auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Create the rule for this auto attendant.
        :type auto_attendant_id: str
        :param name: Unique name for the selective rule in the auto attendant.
        :type name: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call
            forwarding.
        :type forward_to: CallForwardSelectiveForwardToObject
        :param calls_from: Settings related to the rule matching based on incoming caller ID.
        :type calls_from: CallForwardSelectiveCallsFromObject
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param business_schedule: Name of the location's business schedule which determines when this selective call
            forwarding rule is in effect.
        :type business_schedule: str
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call
            forwarding rule is in effect.
        :type holiday_schedule: str
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: CallForwardSelectiveCallsToObject
        :param org_id: Create the auto attendant rule for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        if enabled is not None:
            body['enabled'] = enabled
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        body['forwardTo'] = forward_to.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['callsFrom'] = calls_from.model_dump(mode='json', by_alias=True, exclude_none=True)
        if calls_to is not None:
            body['callsTo'] = calls_to.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/selectiveRules')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_selective_call_forwarding_rule_for_an_auto_attendant(self, location_id: str, auto_attendant_id: str,
                                                                      rule_id: str, org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for an Auto Attendant

        Delete a Selective Call Forwarding Rule for the designated Auto Attendant.

        A selective call forwarding rule for an auto attendant allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the auto attendant's call forwarding
        settings.

        Deleting a selective call forwarding rule for an auto attendant requires a full administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_write`.

        **NOTE**: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Delete the rule for this auto attendant.
        :type auto_attendant_id: str
        :param rule_id: Auto attendant rule you are deleting.
        :type rule_id: str
        :param org_id: Delete auto attendant rule from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/selectiveRules/{rule_id}')
        super().delete(url, params=params)

    def get_selective_call_forwarding_rule_for_an_auto_attendant(self, location_id: str, auto_attendant_id: str,
                                                                 rule_id: str,
                                                                 org_id: str = None) -> GetAutoAttendantCallForwardSelectiveRuleObject:
        """
        Get Selective Call Forwarding Rule for an Auto Attendant

        Retrieve a Selective Call Forwarding Rule's settings for the designated Auto Attendant.

        A selective call forwarding rule for an auto attendant allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the auto attendant's call forwarding
        settings.

        Retrieving a selective call forwarding rule's settings for an auto attendant requires a full or read-only
        administrator or location administrator

        **NOTE**: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Retrieve settings for a rule for this auto attendant.
        :type auto_attendant_id: str
        :param rule_id: Auto attendant rule you are retrieving settings for.
        :type rule_id: str
        :param org_id: Retrieve auto attendant rule settings for this organization.
        :type org_id: str
        :rtype: :class:`GetAutoAttendantCallForwardSelectiveRuleObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().get(url, params=params)
        r = GetAutoAttendantCallForwardSelectiveRuleObject.model_validate(data)
        return r

    def update_selective_call_forwarding_rule_for_an_auto_attendant(self, location_id: str, auto_attendant_id: str,
                                                                    rule_id: str, name: str, enabled: bool = None,
                                                                    business_schedule: str = None,
                                                                    holiday_schedule: str = None,
                                                                    forward_to: CallForwardSelectiveForwardToObject = None,
                                                                    calls_from: CallForwardSelectiveCallsFromObject = None,
                                                                    calls_to: CallForwardSelectiveCallsToObject = None,
                                                                    org_id: str = None) -> str:
        """
        Update Selective Call Forwarding Rule for an Auto Attendant

        Update a Selective Call Forwarding Rule's settings for the designated Auto Attendant.

        A selective call forwarding rule for an auto attendant allows calls to be forwarded or not forwarded to the
        designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the auto attendant's call forwarding
        settings.

        Updating a selective call forwarding rule's settings for an auto attendant requires a full administrator or
        location administrator auth token with a scope of `spark-admin:telephony_config_write`.

        **NOTE**: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update settings for a rule for this auto attendant.
        :type auto_attendant_id: str
        :param rule_id: Auto attendant rule you are updating settings for.
        :type rule_id: str
        :param name: Unique name for the selective rule in the auto attendant.
        :type name: str
        :param enabled: Reflects if rule is enabled.
        :type enabled: bool
        :param business_schedule: Name of the location's business schedule which determines when this selective call
            forwarding rule is in effect.
        :type business_schedule: str
        :param holiday_schedule: Name of the location's holiday schedule which determines when this selective call
            forwarding rule is in effect.
        :type holiday_schedule: str
        :param forward_to: Controls what happens when the rule matches including the destination number for the call
            forwarding.
        :type forward_to: CallForwardSelectiveForwardToObject
        :param calls_from: Settings related the rule matching based on incoming caller ID.
        :type calls_from: CallForwardSelectiveCallsFromObject
        :param calls_to: Settings related to the rule matching based on the destination number.
        :type calls_to: CallForwardSelectiveCallsToObject
        :param org_id: Update auto attendant rule settings for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        if enabled is not None:
            body['enabled'] = enabled
        if business_schedule is not None:
            body['businessSchedule'] = business_schedule
        if holiday_schedule is not None:
            body['holidaySchedule'] = holiday_schedule
        if forward_to is not None:
            body['forwardTo'] = forward_to.model_dump(mode='json', by_alias=True, exclude_none=True)
        if calls_from is not None:
            body['callsFrom'] = calls_from.model_dump(mode='json', by_alias=True, exclude_none=True)
        if calls_to is not None:
            body['callsTo'] = calls_to.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/autoAttendants/{auto_attendant_id}/callForwarding/selectiveRules/{rule_id}')
        data = super().put(url, params=params, json=body)
        r = data['id']
        return r

from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AlternateNumbersObject', 'AlternateNumbersObjectRingPattern', 'AudioAnnouncementFileGetObject',
            'AudioAnnouncementFileGetObjectLevel', 'AudioAnnouncementFileObjectMediaFileType', 'AudioFileObject',
            'AutoAttendantCallForwardSettingsDetailsObject', 'AutoAttendantCallForwardSettingsModifyDetailsObject',
            'CallForwardRulesModifyObject', 'CallForwardRulesObject',
            'CallForwardSelectiveCallsFromCustomNumbersObject', 'CallForwardSelectiveCallsFromObject',
            'CallForwardSelectiveCallsFromObjectSelection', 'CallForwardSelectiveCallsToNumbersObject',
            'CallForwardSelectiveCallsToNumbersObjectType', 'CallForwardSelectiveCallsToObject',
            'CallForwardSelectiveForwardToObject', 'CallForwardSelectiveForwardToObjectSelection',
            'CreateAnAutoAttendantResponse', 'GetAutoAttendantCallForwardSelectiveRuleObject',
            'GetAutoAttendantCallForwardSettingsObject', 'GetAutoAttendantObject',
            'GetAutoAttendantObjectExtensionDialing', 'GetCallForwardAlwaysSettingObject', 'HoursMenuGetObject',
            'HoursMenuGetObjectGreeting', 'KeyConfigurationsGetObject', 'KeyConfigurationsGetObjectAction',
            'KeyConfigurationsGetObjectKey', 'ListAutoAttendantObject',
            'ModifyAutoAttendantCallForwardSelectiveRuleObject', 'ModifyAutoAttendantCallForwardSettingsObject',
            'ModifyAutoAttendantObject', 'ReadTheListOfAutoAttendantsResponse']


class AlternateNumbersObjectRingPattern(str, Enum):
    _0 = '0'
    normal = 'NORMAL'
    long_long = 'LONG_LONG'
    short_short_long = 'SHORT_SHORT_LONG'
    short_long_short = 'SHORT_LONG_SHORT'


class AlternateNumbersObject(ApiModel):
    #: Phone number defined as alternate number.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool] = None
    #: Ring pattern that will be used for the alternate number.
    #: example: 0
    ring_pattern: Optional[AlternateNumbersObjectRingPattern] = None


class AudioAnnouncementFileObjectMediaFileType(str, Enum):
    #: WAV File Extension.
    wav = 'WAV'
    #: WMA File Extension.
    wma = 'WMA'
    #: 3GP File Extension.
    _3_gp = '3GP'


class AudioAnnouncementFileGetObjectLevel(str, Enum):
    #: Specifies this audio file is configured across organisation.
    organization = 'ORGANIZATION'
    #: Specifies this audio file is configured across location.
    location = 'LOCATION'


class AudioAnnouncementFileGetObject(ApiModel):
    #: A unique identifier for the announcement.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QzVjBPWFIxWjJkM2FFQm1iR1Y0TWk1amFYTmpieTVqYjIw
    id: Optional[str] = None
    #: Audio announcement file name.
    #: example: AUDIO_FILE.wav
    file_name: Optional[str] = None
    #: Audio announcement file type.
    #: example: WAV
    media_file_type: Optional[AudioAnnouncementFileObjectMediaFileType] = None
    #: Audio announcement file type location.
    #: example: ORGANIZATION
    level: Optional[AudioAnnouncementFileGetObjectLevel] = None


class AudioFileObject(ApiModel):
    #: Announcement audio file name.
    #: example: AUDIO_FILE.wav
    name: Optional[str] = None
    #: Announcement audio file media type.
    #: example: WAV
    media_type: Optional[AudioAnnouncementFileObjectMediaFileType] = None


class GetCallForwardAlwaysSettingObject(ApiModel):
    #: `Always` call forwarding is enabled or disabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Destination for `Always` call forwarding. Required if field `enabled` is set to `true`.
    #: example: +19705550006
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Indicates enabled or disabled state of sending incoming calls to voicemail when the destination is an internal
    #: phone number and that number has the voicemail service enabled.
    send_to_voicemail_enabled: Optional[bool] = None


class CallForwardRulesObject(ApiModel):
    #: Unique ID for the rule.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfRk9SV0FSRElOR19TRUxFQ1RJVkVfUlVMRS9WR1Z6ZENCU2RXeGw
    id: Optional[str] = None
    #: Unique name of rule.
    #: example: Test Rule
    name: Optional[str] = None
    #: Comma-separated list of incoming call numbers that, when matched, will not be forwarded. A Limit of 12 numbers
    #: is allowed. Use `Any private Number` in the comma-separated value to indicate rules that match incoming calls
    #: from a private number. Use `Any unavailable number` in the comma-separated value to match incoming calls from an
    #: unavailable number.
    #: example: Any private number
    calls_from: Optional[str] = None
    #: Comma-separated list of the types of numbers being matched for incoming call destination.
    #: example: +19705550006
    calls_to: Optional[str] = None
    #: Number to which calls will be forwarded if the rule is of type "Forward To" and the incoming call is matched.
    #: example: +19705550026
    forward_to: Optional[str] = None
    #: Reflects if rule is enabled.
    #: example: True
    enabled: Optional[bool] = None


class AutoAttendantCallForwardSettingsDetailsObject(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[GetCallForwardAlwaysSettingObject] = None
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[GetCallForwardAlwaysSettingObject] = None
    #: Rules for selectively forwarding calls.
    rules: Optional[list[CallForwardRulesObject]] = None


class CallForwardRulesModifyObject(ApiModel):
    #: A unique identifier for the auto attendant call forward selective rule.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfRk9SV0FSRElOR19TRUxFQ1RJVkVfUlVMRS9WR1Z6ZENCU2RXeGw
    id: Optional[str] = None
    #: Flag to indicate if always call forwarding selective rule criteria is active. If not set, flag will be set to
    #: false.
    #: example: True
    enabled: Optional[bool] = None


class AutoAttendantCallForwardSettingsModifyDetailsObject(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[GetCallForwardAlwaysSettingObject] = None
    #: Selectively forward calls to a designated number, depending on criteria rules. You'll need to have at least one
    #: rule for forwarding applied for call forwarding to be active.
    selective: Optional[GetCallForwardAlwaysSettingObject] = None
    #: Rules for selectively forwarding calls. (Rules which are omitted in the list will not be deleted.)
    rules: Optional[list[CallForwardRulesModifyObject]] = None


class CallForwardSelectiveCallsFromCustomNumbersObject(ApiModel):
    #: Match if caller ID indicates the call is from a private number.
    #: example: True
    private_number_enabled: Optional[bool] = None
    #: Match if callerID is unavailable.
    unavailable_number_enabled: Optional[bool] = None
    #: Array of number strings to be matched against incoming caller ID.
    #: example: ['["+12147691003", "+12147691004"]']
    numbers: Optional[list[str]] = None


class CallForwardSelectiveCallsFromObjectSelection(str, Enum):
    #: Rule matches for calls from any number.
    any = 'ANY'
    #: Rule matches based on the numbers and options in customNumbers.
    custom = 'CUSTOM'


class CallForwardSelectiveCallsFromObject(ApiModel):
    #: If `CUSTOM`, use `customNumbers` to specify which incoming caller ID values cause this rule to match. `ANY`
    #: means any incoming call matches assuming the rule is in effect based on the associated schedules.
    #: example: CUSTOM
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
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Calls To extension.  Either `phoneNumber` or `extension` is mandatory.
    #: example: 1001
    extension: Optional[datetime] = None
    #: Calls to type options.
    #: example: PRIMARY
    type: Optional[CallForwardSelectiveCallsToNumbersObjectType] = None


class CallForwardSelectiveCallsToObject(ApiModel):
    #: Array of numbers to be matched against the calling destination number.
    numbers: Optional[list[CallForwardSelectiveCallsToNumbersObject]] = None


class CallForwardSelectiveForwardToObjectSelection(str, Enum):
    #: When the rule matches, forward to the destination for the auto attendant.
    forward_to_default_number = 'FORWARD_TO_DEFAULT_NUMBER'
    #: When the rule matches, forward to the destination for this rule.
    forward_to_specified_number = 'FORWARD_TO_SPECIFIED_NUMBER'
    #: When the rule matches, do not forward to another number.
    do_not_forward = 'DO_NOT_FORWARD'


class CallForwardSelectiveForwardToObject(ApiModel):
    #: Phone number used if selection is `FORWARD_TO_SPECIFIED_NUMBER`.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Controls what happens when the rule matches.
    #: example: FORWARD_TO_DEFAULT_NUMBER
    selection: Optional[CallForwardSelectiveForwardToObjectSelection] = None


class GetAutoAttendantCallForwardSelectiveRuleObject(ApiModel):
    #: Unique ID for the rule.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfRk9SV0FSRElOR19TRUxFQ1RJVkVfUlVMRS9WR1Z6ZENCU2RXeGw
    id: Optional[str] = None
    #: Unique name for the selective rule in the auto attendant.
    #: example: Test Rule
    name: Optional[str] = None
    #: Reflects if rule is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
    #: example: AUTOATTENDANT-BUSINESS-HOURS
    business_schedule: Optional[str] = None
    #: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
    #: example: AUTOATTENDANT-HOLIDAY
    holiday_schedule: Optional[str] = None
    #: Controls what happens when the rule matches including the destination number for the call forwarding.
    forward_to: Optional[CallForwardSelectiveForwardToObject] = None
    #: Settings related to the rule matching based on incoming caller ID.
    calls_from: Optional[CallForwardSelectiveCallsFromObject] = None
    #: Settings related to the rule matching based on the destination number.
    calls_to: Optional[CallForwardSelectiveCallsToObject] = None


class GetAutoAttendantCallForwardSettingsObject(ApiModel):
    #: Settings related to `Always`, `Busy`, and `No Answer` call forwarding.
    call_forwarding: Optional[AutoAttendantCallForwardSettingsDetailsObject] = None


class GetAutoAttendantObjectExtensionDialing(str, Enum):
    enterprise = 'ENTERPRISE'
    group = 'GROUP'


class HoursMenuGetObjectGreeting(str, Enum):
    default = 'DEFAULT'
    custom = 'CUSTOM'


class KeyConfigurationsGetObjectKey(str, Enum):
    _0 = '0'
    _1 = '1'
    _2 = '2'
    _3 = '3'
    _4 = '4'
    _5 = '5'
    _6 = '6'
    _7 = '7'
    _8 = '8'
    _9 = '9'
    none_ = 'none'
    _ = '#'


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
    #: Return back to the previous menu.
    return_to_previous_menu = 'RETURN_TO_PREVIOUS_MENU'


class KeyConfigurationsGetObject(ApiModel):
    #: Key assigned to specific menu configuration.
    #: example: 0
    key: Optional[KeyConfigurationsGetObjectKey] = None
    #: Action assigned to specific menu key configuration.
    #: example: EXIT
    action: Optional[KeyConfigurationsGetObjectAction] = None
    #: The description of each menu key.
    #: example: Exit the menu
    description: Optional[str] = None
    #: Value based on actions.
    #: example: +19705550006
    value: Optional[str] = None
    #: Pre-configured announcement audio files when PLAY_ANNOUNCEMENT is set.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject] = None


class HoursMenuGetObject(ApiModel):
    #: Greeting type defined for the auto attendant.
    #: example: DEFAULT
    greeting: Optional[HoursMenuGetObjectGreeting] = None
    #: Flag to indicate if auto attendant extension is enabled or not.
    #: example: True
    extension_enabled: Optional[bool] = None
    #: Announcement Audio File details.
    audio_announcement_file: Optional[AudioAnnouncementFileGetObject] = None
    #: Key configurations defined for the auto attendant.
    key_configurations: Optional[KeyConfigurationsGetObject] = None


class GetAutoAttendantObject(ApiModel):
    #: A unique identifier for the auto attendant.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QzVjBPWFIxWjJkM2FFQm1iR1Y0TWk1amFYTmpieTVqYjIw
    id: Optional[str] = None
    #: Unique name for the auto attendant.
    #: example: Main Line AA - Test
    name: Optional[str] = None
    #: Flag to indicate if auto attendant number is enabled or not.
    #: example: True
    enabled: Optional[bool] = None
    #: Auto attendant phone number.  Either `phoneNumber` or `extension` is mandatory.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Auto attendant extension.  Either `phoneNumber` or `extension` is mandatory.
    #: example: 1001
    extension: Optional[datetime] = None
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool] = None
    #: First name defined for an auto attendant.
    #: example: Main Line AA
    first_name: Optional[str] = None
    #: Last name defined for an auto attendant.
    #: example: Test
    last_name: Optional[str] = None
    #: Alternate numbers defined for the auto attendant.
    alternate_numbers: Optional[list[AlternateNumbersObject]] = None
    #: Language for the auto attendant.
    #: example: English
    language: Optional[str] = None
    #: Language code for the auto attendant.
    #: example: en_us
    language_code: Optional[str] = None
    #: Business hours defined for the auto attendant.
    #: example: AUTOATTENDANT-BUSINESS-HOURS
    business_schedule: Optional[str] = None
    #: Holiday defined for the auto attendant.
    #: example: AUTOATTENDANT-HOLIDAY
    holiday_schedule: Optional[str] = None
    #: Extension dialing setting. If the values are not set default will be set as `ENTERPRISE`.
    #: example: ENTERPRISE
    extension_dialing: Optional[GetAutoAttendantObjectExtensionDialing] = None
    #: Name dialing setting. If the values are not set default will be set as `ENTERPRISE`.
    #: example: ENTERPRISE
    name_dialing: Optional[GetAutoAttendantObjectExtensionDialing] = None
    #: Time zone defined for the auto attendant.
    #: example: America/Los_Angeles
    time_zone: Optional[str] = None
    #: Business hours menu defined for the auto attendant.
    business_hours_menu: Optional[HoursMenuGetObject] = None
    #: After hours menu defined for the auto attendant.
    after_hours_menu: Optional[HoursMenuGetObject] = None


class ListAutoAttendantObject(ApiModel):
    #: A unique identifier for the auto attendant.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QzVjBPWFIxWjJkM2FFQm1iR1Y0TWk1amFYTmpieTVqYjIw
    id: Optional[str] = None
    #: Unique name for the auto attendant.
    #: example: Main Line AA - Test
    name: Optional[str] = None
    #: Name of location for auto attendant.
    #: example: Houston
    location_name: Optional[str] = None
    #: ID of location for auto attendant.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzI2NDE1MA
    location_id: Optional[str] = None
    #: Auto attendant phone number.  Either `phoneNumber` or `extension` is mandatory.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Auto attendant extension.  Either `phoneNumber` or `extension` is mandatory.
    #: example: 1001
    extension: Optional[datetime] = None
    #: Flag to indicate if auto attendant number is toll-free number.
    toll_free_number: Optional[bool] = None


class ModifyAutoAttendantCallForwardSelectiveRuleObject(ApiModel):
    #: Unique name for the selective rule in the auto attendant.
    #: example: Test Rule New Name
    name: Optional[str] = None
    #: Reflects if rule is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Name of the location's business schedule which determines when this selective call forwarding rule is in effect.
    #: example: AUTOATTENDANT-BUSINESS-HOURS
    business_schedule: Optional[str] = None
    #: Name of the location's holiday schedule which determines when this selective call forwarding rule is in effect.
    #: example: AUTOATTENDANT-HOLIDAY
    holiday_schedule: Optional[str] = None
    #: Controls what happens when the rule matches including the destination number for the call forwarding.
    forward_to: Optional[CallForwardSelectiveForwardToObject] = None
    #: Settings related the rule matching based on incoming caller ID.
    calls_from: Optional[CallForwardSelectiveCallsFromObject] = None
    #: Settings related to the rule matching based on the destination number.
    calls_to: Optional[CallForwardSelectiveCallsToObject] = None


class ModifyAutoAttendantCallForwardSettingsObject(ApiModel):
    #: Settings related to `Always`, `Busy`, and `No Answer` call forwarding.
    call_forwarding: Optional[AutoAttendantCallForwardSettingsModifyDetailsObject] = None


class ModifyAutoAttendantObject(ApiModel):
    #: Unique name for the auto attendant.
    #: example: Main Line IA - Test
    name: Optional[str] = None
    #: Auto attendant phone number.  Either `phoneNumber` or `extension` is mandatory.
    #: example: +19705550028
    phone_number: Optional[str] = None
    #: Auto attendant extension.  Either `phoneNumber` or `extension` is mandatory.
    #: example: 1001
    extension: Optional[datetime] = None
    #: First name defined for an auto attendant.
    #: example: Main Line AA
    first_name: Optional[str] = None
    #: Last name defined for an auto attendant.
    #: example: Test
    last_name: Optional[str] = None
    #: Alternate numbers defined for the auto attendant.
    alternate_numbers: Optional[list[AlternateNumbersObject]] = None
    #: Language code for the auto attendant.
    #: example: en_us
    language_code: Optional[str] = None
    #: Business hours defined for the auto attendant.
    #: example: AUTOATTENDANT-BUSINESS-HOURS
    business_schedule: Optional[str] = None
    #: Holiday defined for the auto attendant.
    #: example: AUTOATTENDANT-HOLIDAY
    holiday_schedule: Optional[str] = None
    #: Extension dialing setting. If the values are not set default will be set as `ENTERPRISE`.
    #: example: ENTERPRISE
    extension_dialing: Optional[GetAutoAttendantObjectExtensionDialing] = None
    #: Name dialing setting. If the values are not set default will be set as `ENTERPRISE`.
    #: example: ENTERPRISE
    name_dialing: Optional[GetAutoAttendantObjectExtensionDialing] = None
    #: Time zone defined for the auto attendant.
    #: example: America/Los_Angeles
    time_zone: Optional[str] = None
    #: Business hours menu defined for the auto attendant.
    business_hours_menu: Optional[HoursMenuGetObject] = None
    #: After hours menu defined for the auto attendant.
    after_hours_menu: Optional[HoursMenuGetObject] = None


class ReadTheListOfAutoAttendantsResponse(ApiModel):
    #: Array of auto attendants.
    auto_attendants: Optional[list[ListAutoAttendantObject]] = None


class CreateAnAutoAttendantResponse(ApiModel):
    #: ID of the newly created auto attendant.
    id: Optional[str] = None

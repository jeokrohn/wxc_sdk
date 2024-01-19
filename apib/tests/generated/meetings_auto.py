from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AnswerForCustomizedQuestion', 'BatchUpdateMeetingRegistrantsStatusStatusOpType', 'BreakoutSessionObject',
            'Control', 'CreateMeetingObject', 'CreateMeetingObjectRegistration',
            'CreateMeetingObjectSimultaneousInterpretation', 'CustomizedQuestionForCreateMeeting',
            'CustomizedQuestionForCreateMeetingOptions', 'CustomizedQuestionForCreateMeetingRules',
            'CustomizedQuestionForCreateMeetingRulesCondition', 'CustomizedQuestionForCreateMeetingRulesResult',
            'CustomizedQuestionForCreateMeetingType', 'CustomizedQuestionForGetMeeting',
            'CustomizedQuestionForGetMeetingRules', 'CustomizedRegistrant', 'DetailedTemplateObject',
            'GetBreakoutSessionObject', 'InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting',
            'InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting', 'InvitationSourceCreateObject',
            'InvitationSourceObject', 'InviteeObjectForCreateMeeting', 'JoinMeetingLinkObject',
            'LinksObjectForTelephony', 'ListMeetingsOfAMeetingSeriesMeetingType', 'ListMeetingsOfAMeetingSeriesState',
            'MeetingSeriesObject', 'MeetingSeriesObjectAttendeePrivileges',
            'MeetingSeriesObjectAudioConnectionOptions',
            'MeetingSeriesObjectAudioConnectionOptionsAudioConnectionType',
            'MeetingSeriesObjectAudioConnectionOptionsEntryAndExitTone', 'MeetingSeriesObjectForListMeeting',
            'MeetingSeriesObjectMeetingOptions', 'MeetingSeriesObjectMeetingOptionsNoteType',
            'MeetingSeriesObjectMeetingType', 'MeetingSeriesObjectRegistration', 'MeetingSeriesObjectScheduledType',
            'MeetingSeriesObjectSimultaneousInterpretation', 'MeetingSeriesObjectState',
            'MeetingSeriesObjectTelephony', 'MeetingSeriesObjectTelephonyCallInNumbers',
            'MeetingSeriesObjectTelephonyCallInNumbersTollType', 'MeetingSeriesObjectUnlockedMeetingJoinSecurity',
            'MeetingSeriesObjectWithAdhoc', 'MeetingSeriesObjectWithAdhocRegistration',
            'MeetingSeriesObjectWithAdhocTelephony', 'MeetingSessionTypeObject', 'MeetingSessionTypeObjectType',
            'MeetingTrackingCodesObject', 'MeetingTrackingCodesObjectInputMode', 'MeetingTrackingCodesObjectService',
            'MeetingTrackingCodesObjectType', 'MeetingsApi', 'OptionsForTrackingCodeObject',
            'QueryRegistrantsOrderBy', 'QueryRegistrantsOrderType', 'QuestionObject', 'QuestionObjectType',
            'QuestionOptionObject', 'QuestionWithAnswersObject', 'ReassignMeetingErrorDescriptionObject',
            'ReassignMeetingResponseObject', 'Registrant', 'RegistrantCreateResponse', 'RegistrantFormObject',
            'RegistrantStatus', 'Registrants', 'Registration', 'ScheduledMeetingObject',
            'StandardRegistrationApproveRule', 'StandardRegistrationApproveRuleQuestion', 'SurveyLinkObject',
            'SurveyObject', 'SurveyResultObject', 'TemplateObject', 'TemplateObjectTemplateType',
            'TrackingCodeItemForCreateMeetingObject']


class InviteeObjectForCreateMeeting(ApiModel):
    #: Email address of meeting invitee.
    #: example: brenda.song@example.com
    email: Optional[str] = None
    #: Display name of meeting invitee. The maximum length of `displayName` is 128 characters. If not specified but the
    #: email has been registered, user's registered name for the email will be taken as `displayName`. If not
    #: specified and the email hasn't been registered, the email will be taken as `displayName`.
    #: example: Brenda Song
    display_name: Optional[str] = None
    #: Whether or not invitee is allowed to be a cohost for the meeting. `coHost` for each invitee is `true` by default
    #: if `roomId` is specified when creating a meeting, and anyone in the invitee list that is not qualified to be a
    #: cohost will be invited as a non-cohost invitee.
    co_host: Optional[bool] = None
    #: Whether or not an invitee is allowed to be a panelist. Only applies to webinars.
    panelist: Optional[bool] = None


class InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting(ApiModel):
    #: Unique identifier for meeting interpreter.
    #: example: OGQ0OGRiM2U3ZTAxNDZiMGFjYzJjMzYxNDNmNGZhN2RfZTA5MTJiZDBjNWVlNDA4YjgxMTZlMjU4Zjg2NWIzZmM
    id: Optional[str] = None
    #: Forms a set of simultaneous interpretation channels together with `languageCode2`. Standard language format from
    #: `ISO 639-1
    #: <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_ code. Read `ISO 639-1
    #: example: en
    language_code1: Optional[str] = None
    #: Forms a set of simultaneous interpretation channels together with `languageCode1`. Standard language format from
    #: `ISO 639-1
    #: <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_ code. Read `ISO 639-1
    #: example: de
    language_code2: Optional[str] = None
    #: Email address of meeting interpreter.
    #: example: marcus.hoffmann@example.com
    email: Optional[str] = None
    #: Display name of meeting interpreter.
    #: example: Hoffmann
    display_name: Optional[str] = None


class InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting(ApiModel):
    #: Forms a set of simultaneous interpretation channels together with `languageCode2`. Standard language format from
    #: `ISO 639-1
    #: <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_ code. Read `ISO 639-1
    #: example: en
    language_code1: Optional[str] = None
    #: Forms a set of simultaneous interpretation channels together with `languageCode1`. Standard language format from
    #: `ISO 639-1
    #: <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_ code. Read `ISO 639-1
    #: example: de
    language_code2: Optional[str] = None
    #: Email address of meeting interpreter.
    #: example: marcus.hoffmann@example.com
    email: Optional[str] = None
    #: Display name of meeting interpreter.
    #: example: Hoffmann
    display_name: Optional[str] = None


class MeetingSeriesObjectMeetingType(str, Enum):
    #: Primary instance of a scheduled series of meetings which consists of one or more scheduled meetings based on a
    #: `recurrence` rule. When a non-recurring meeting is scheduled with no `recurrence`, its `meetingType` is also
    #: `meetingSeries` which is a meeting series with only one occurrence in Webex meeting modeling.
    meeting_series = 'meetingSeries'
    #: Instance from a primary meeting series.
    scheduled_meeting = 'scheduledMeeting'
    #: Meeting instance that is in progress or has completed.
    meeting = 'meeting'


class MeetingSeriesObjectState(str, Enum):
    #: Only applies to a meeting series. Indicates that one or more future scheduled meetings exist for this meeting
    #: series.
    active = 'active'
    #: Only applies to scheduled meeting. Indicates that the meeting is scheduled in the future.
    scheduled = 'scheduled'
    #: Only applies to scheduled meeting. Indicates that this scheduled meeting is ready to start or join immediately.
    ready = 'ready'
    #: Only applies to meeting instances. Indicates that a locked meeting has been joined by participants, but no hosts
    #: have joined.
    lobby = 'lobby'
    #: Applies to meeting series and meeting instances. For a meeting series, indicates that an instance of this series
    #: is happening now. For a meeting instance, indicates that the meeting has been joined and unlocked.
    in_progress = 'inProgress'
    #: Applies to scheduled meetings and meeting instances. For scheduled meetings, indicates that the meeting was
    #: started and is now over. For meeting instances, indicates that the meeting instance has concluded.
    ended = 'ended'
    #: This state only applies to scheduled meetings. Indicates that the meeting was scheduled in the past but never
    #: happened.
    missed = 'missed'
    #: This state only applies to a meeting series. Indicates that all scheduled meetings of this series have passed.
    expired = 'expired'


class MeetingSeriesObjectUnlockedMeetingJoinSecurity(str, Enum):
    #: If the value of `unlockedMeetingJoinSecurity` attribute is `allowJoin`, people can join the unlocked meeting
    #: directly.
    allow_join = 'allowJoin'
    #: If the value of `unlockedMeetingJoinSecurity` attribute is `allowJoinWithLobby`, people will wait in the lobby
    #: until the host admits them.
    allow_join_with_lobby = 'allowJoinWithLobby'
    #: If the value of `unlockedMeetingJoinSecurity` attribute is `blockFromJoin`, people can't join the unlocked
    #: meeting.
    block_from_join = 'blockFromJoin'


class MeetingSeriesObjectScheduledType(str, Enum):
    #: If the value of `scheduledType` attribute is `meeting`, it is a regular meeting.
    meeting = 'meeting'
    #: If the value of `scheduledType` attribute is `webinar`, it is a webinar meeting.
    webinar = 'webinar'
    #: If the value of `scheduledType` attribute is `personalRoomMeeting`, it is a meeting scheduled in the user's
    #: `personal room
    #: <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_.
    personal_room_meeting = 'personalRoomMeeting'


class MeetingSeriesObjectTelephonyCallInNumbersTollType(str, Enum):
    toll = 'toll'
    toll_free = 'tollFree'


class MeetingSeriesObjectTelephonyCallInNumbers(ApiModel):
    #: Label for the call-in number.
    #: example: Call-in toll-free number (US/Canada)
    label: Optional[str] = None
    #: Call-in number to join the teleconference from a phone.
    #: example: 123456789
    call_in_number: Optional[str] = None
    #: Type of toll for the call-in number.
    #: example: tollFree
    toll_type: Optional[MeetingSeriesObjectTelephonyCallInNumbersTollType] = None


class LinksObjectForTelephony(ApiModel):
    #: Link relation describing how the target resource is related to the current context (conforming with `RFC5998
    #: <https://tools.ietf.org/html/rfc5988>`_).
    #: example: globalCallinNumbers
    rel: Optional[str] = None
    #: Target resource URI (conforming with `RFC5998
    #: <https://tools.ietf.org/html/rfc5988>`_).
    #: example: /api/v1/meetings/2c87cf8ece4e414a9fe5516e4a0aac76/globalCallinNumbers
    href: Optional[str] = None
    #: Target resource method (conforming with `RFC5998
    #: <https://tools.ietf.org/html/rfc5988>`_).
    #: example: GET
    method: Optional[str] = None


class MeetingSeriesObjectTelephony(ApiModel):
    #: Code for authenticating a user to join teleconference. Users join the teleconference using the call-in number or
    #: the global call-in number, followed by the value of the `accessCode`.
    #: example: 1234567890
    access_code: Optional[str] = None
    #: Array of call-in numbers for joining a teleconference from a phone.
    call_in_numbers: Optional[list[MeetingSeriesObjectTelephonyCallInNumbers]] = None
    #: `HATEOAS
    #: <https://en.wikipedia.org/wiki/HATEOAS>`_ information of global call-in numbers for joining a teleconference from a phone.
    links: Optional[list[LinksObjectForTelephony]] = None


class MeetingSeriesObjectMeetingOptionsNoteType(str, Enum):
    #: If the value of `noteType` attribute is `allowAll`, all participants can take notes.
    allow_all = 'allowAll'
    #: If the value of `noteType` attribute is `allowOne`, only a single note taker is allowed.
    allow_one = 'allowOne'


class MeetingSeriesObjectMeetingOptions(ApiModel):
    #: Whether or not to allow any attendee to chat in the meeting. Also depends on the session type.
    #: example: True
    enabled_chat: Optional[bool] = None
    #: Whether or not to allow any attendee to have video in the meeting. Also depends on the session type.
    #: example: True
    enabled_video: Optional[bool] = None
    #: Whether or not to allow any attendee to poll in the meeting. Can only be set `true` for a webinar. The value of
    #: this attribute depends on the session type for a meeting. Please contact your site admin if this attribute is
    #: not available.
    enabled_polling: Optional[bool] = None
    #: Whether or not to allow any attendee to take notes in the meeting. The value of this attribute also depends on
    #: the session type.
    #: example: True
    enabled_note: Optional[bool] = None
    #: Whether note taking is enabled. If the value of `enabledNote` is false, users can not set this attribute and get
    #: default value `allowAll`.
    #: example: allowAll
    note_type: Optional[MeetingSeriesObjectMeetingOptionsNoteType] = None
    #: Whether or not to allow any attendee to have closed captions in the meeting. The value of this attribute also
    #: depends on the session type.
    enabled_closed_captions: Optional[bool] = None
    #: Whether or not to allow any attendee to transfer files in the meeting. The value of this attribute also depends
    #: on the session type.
    enabled_file_transfer: Optional[bool] = None
    #: Whether or not to allow any attendee to share `Universal Communications Format
    #: <https://www.cisco.com/c/en/us/td/docs/collaboration/training_center/wbs30/WebEx_BK_TE1FB6C1_00_training-center-frequently-asked-questions/WebEx_BK_TE1FB6C1_00_training-center-frequently-asked-questions_chapter_0110.pdf>`_ media files in the meeting. The
    #: value of this attribute also depends on the sessionType.
    enabled_ucfrich_media: Optional[bool] = Field(alias='enabledUCFRichMedia', default=None)


class MeetingSeriesObjectAttendeePrivileges(ApiModel):
    #: Whether or not to allow any attendee to share content in the meeting.
    #: example: True
    enabled_share_content: Optional[bool] = None
    #: Whether or not to allow any attendee to save shared documents, slides, or whiteboards when they are shared as
    #: files in the content viewer instead of in a window or application.
    enabled_save_document: Optional[bool] = None
    #: Whether or not to allow any attendee to print shared documents, slides, or whiteboards when they are shared as
    #: files in the content viewer instead of in a window or application.
    enabled_print_document: Optional[bool] = None
    #: Whether or not to allow any attendee to annotate shared documents, slides, or whiteboards when they are shared
    #: as files in the content viewer instead of in a window or application.
    enabled_annotate: Optional[bool] = None
    #: Whether or not to allow any attendee to view participants.
    #: example: True
    enabled_view_participant_list: Optional[bool] = None
    #: Whether or not to allow any attendee to see a small preview image of any page of shared documents or slides when
    #: they are shared as files in the content viewer instead of in a window or application.
    enabled_view_thumbnails: Optional[bool] = None
    #: Whether or not to allow any attendee to control applications, web browsers, or desktops remotely.
    #: example: True
    enabled_remote_control: Optional[bool] = None
    #: Whether or not to allow any attendee to view any shared documents or slides when they are shared as files in the
    #: content viewer instead of in a window or application.
    enabled_view_any_document: Optional[bool] = None
    #: Whether or not to allow any attendee to scroll through any page of shared documents or slides when they are
    #: shared as files in the content viewer instead of in a window or application.
    enabled_view_any_page: Optional[bool] = None
    #: Whether or not to allow any attendee to contact the operator privately.
    enabled_contact_operator_privately: Optional[bool] = None
    #: Whether or not to allow any attendee to chat with the host in private.
    #: example: True
    enabled_chat_host: Optional[bool] = None
    #: Whether or not to allow any attendee to chat with the presenter in private.
    #: example: True
    enabled_chat_presenter: Optional[bool] = None
    #: Whether or not to allow any attendee to chat with other participants in private.
    #: example: True
    enabled_chat_other_participants: Optional[bool] = None


class CustomizedQuestionForCreateMeetingType(str, Enum):
    #: Single line text box.
    single_line_text_box = 'singleLineTextBox'
    #: Multiple line text box.
    multi_line_text_box = 'multiLineTextBox'
    #: Check box which requires `options`.
    checkbox = 'checkbox'
    #: Drop down list box which requires `options`.
    dropdown_list = 'dropdownList'
    #: Single radio button which requires `options`.
    radio_buttons = 'radioButtons'
    none_ = 'none'


class QuestionOptionObject(ApiModel):
    #: Unique identifier for the question option.
    #: example: 1
    id: Optional[int] = None
    #: Value for the question option.
    #: example: Yes
    value: Optional[str] = None


class CustomizedQuestionForCreateMeetingRulesCondition(str, Enum):
    #: The content of the answer contains the value.
    contains = 'contains'
    #: The content of the answer does not contain the value
    not_contains = 'notContains'
    #: The content of the answer begins with the value.
    begins_with = 'beginsWith'
    #: The content of the answer ends with the value.
    ends_with = 'endsWith'
    #: The content of the answer is the same as the value.
    equals = 'equals'
    #: The content of the answer is not the same as the value.
    not_equals = 'notEquals'


class CustomizedQuestionForCreateMeetingRulesResult(str, Enum):
    #: If the user's registration value meets the criteria, the registration form will be automatically approved.
    approve = 'approve'
    #: If the user's registration value meets the criteria, the registration form will be automatically rejected.
    reject = 'reject'


class CustomizedQuestionForGetMeetingRules(ApiModel):
    #: Judgment expression for approval rules.
    #: example: contains
    condition: Optional[CustomizedQuestionForCreateMeetingRulesCondition] = None
    #: The keyword for the approval rule. If the rule matches the keyword, the corresponding action will be executed.
    #: example: tom
    value: Optional[str] = None
    #: The automatic approval result for the approval rule.
    #: example: approve
    result: Optional[CustomizedQuestionForCreateMeetingRulesResult] = None
    #: Whether to check the case of values.
    #: example: True
    match_case: Optional[bool] = None
    #: The priority number of the approval rule. Approval rules for standard questions and custom questions need to be
    #: ordered together.
    #: example: 1
    order: Optional[int] = None


class CustomizedQuestionForGetMeeting(ApiModel):
    #: Unique identifier for the question.
    #: example: 330521
    id: Optional[int] = None
    #: Title of the customized question.
    #: example: How are you
    question: Optional[str] = None
    #: Whether or not the customized question is required to be answered by participants.
    #: example: True
    required: Optional[bool] = None
    #: Type of the question being asked.
    type: Optional[CustomizedQuestionForCreateMeetingType] = None
    #: The maximum length of a string that can be entered by the user, ranging from `0` to `999`. Only required by
    #: `singleLineTextBox` and `multiLineTextBox`.
    max_length: Optional[int] = None
    #: TThe content of `options`. Required if the question type is one of `checkbox`, `dropdownList`, or
    #: `radioButtons`.
    options: Optional[list[QuestionOptionObject]] = None
    #: The automatic approval rules for customized questions.
    rules: Optional[list[CustomizedQuestionForGetMeetingRules]] = None


class StandardRegistrationApproveRuleQuestion(str, Enum):
    #: If the value is `lastName`, this approval rule applies to the standard question of "Last Name".
    last_name = 'lastName'
    #: If the value is `email`, this approval rule applies to the standard question of "Email".
    email = 'email'
    #: If the value is `jobTitle`, this approval rule applies to the standard question of "Job Title".
    job_title = 'jobTitle'
    #: If the value is `companyName`, this approval rule applies to the standard question of "Company Name".
    company_name = 'companyName'
    #: If the value is `address1`, this approval rule applies to the standard question of "Address 1".
    address1 = 'address1'
    #: If the value is `address2`, this approval rule applies to the standard question of "Address 2".
    address2 = 'address2'
    #: If the value is `city`, this approval rule applies to the standard question of "City".
    city = 'city'
    #: If the value is `state`, this approval rule applies to the standard question of "State".
    state = 'state'
    #: If the value is `zipCode`, this approval rule applies to the standard question of "Zip/Post Code".
    zip_code = 'zipCode'
    #: If the value is `countryRegion`, this approval rule applies to the standard question of "Country Region".
    country_region = 'countryRegion'
    #: If the value is `workPhone`, this approval rule applies to the standard question of "Work Phone".
    work_phone = 'workPhone'
    #: If the value is `fax`, this approval rule applies to the standard question of "Fax".
    fax = 'fax'


class StandardRegistrationApproveRule(ApiModel):
    #: Name for standard question.
    #: example: state
    question: Optional[StandardRegistrationApproveRuleQuestion] = None
    #: Judgment expression for approval rules.
    #: example: contains
    condition: Optional[CustomizedQuestionForCreateMeetingRulesCondition] = None
    #: The keyword for the approval rule. If the rule matches the keyword, the corresponding action will be executed.
    #: example: tom
    value: Optional[str] = None
    #: The automatic approval result for the approval rule.
    #: example: approve
    result: Optional[CustomizedQuestionForCreateMeetingRulesResult] = None
    #: Whether to check the case of values.
    #: example: True
    match_case: Optional[bool] = None
    #: The priority number of the approval rule. Approval rules for standard questions and custom questions need to be
    #: ordered together.
    #: example: 1
    order: Optional[int] = None


class MeetingSeriesObjectRegistration(ApiModel):
    #: Whether or not meeting registration requests are accepted automatically.
    auto_accept_request: Optional[bool] = None
    #: Whether or not a registrant's first name is required for meeting registration.
    #: example: True
    require_first_name: Optional[bool] = None
    #: Whether or not a registrant's last name is required for meeting registration.
    #: example: True
    require_last_name: Optional[bool] = None
    #: Whether or not a registrant's email is required for meeting registration.
    #: example: True
    require_email: Optional[bool] = None
    #: Whether or not a registrant's job title is shown or required for meeting registration.
    require_job_title: Optional[bool] = None
    #: Whether or not a registrant's company name is shown or required for meeting registration.
    require_company_name: Optional[bool] = None
    #: Whether or not a registrant's first address field is shown or required for meeting registration.
    require_address1: Optional[bool] = None
    #: Whether or not a registrant's second address field is shown or required for meeting registration.
    require_address2: Optional[bool] = None
    #: Whether or not a registrant's city is shown or required for meeting registration.
    require_city: Optional[bool] = None
    #: Whether or not a registrant's state is shown or required for meeting registration.
    require_state: Optional[bool] = None
    #: Whether or not a registrant's postal code is shown or required for meeting registration.
    require_zip_code: Optional[bool] = None
    #: Whether or not a registrant's country or region is shown or required for meeting registration.
    require_country_region: Optional[bool] = None
    #: Whether or not a registrant's work phone number is shown or required for meeting registration.
    require_work_phone: Optional[bool] = None
    #: Whether or not a registrant's fax number is shown or required for meeting registration.
    require_fax: Optional[bool] = None
    #: Maximum number of meeting registrations. This only applies to meetings. The maximum number of participants for
    #: meetings and webinars, with the limit based on the user capacity and controlled by a toggle at the site level.
    #: The default maximum number of participants for webinars is 10000, but the actual maximum number of participants
    #: is limited by the user capacity.
    #: example: 1000
    max_register_num: Optional[int] = None
    #: Customized questions for meeting registration.
    customized_questions: Optional[list[CustomizedQuestionForGetMeeting]] = None
    #: The approval rules for standard questions.
    rules: Optional[list[StandardRegistrationApproveRule]] = None


class MeetingSeriesObjectSimultaneousInterpretation(ApiModel):
    #: Whether or not simultaneous interpretation is enabled.
    enabled: Optional[bool] = None
    #: Interpreters for meeting.
    interpreters: Optional[list[InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting]] = None


class MeetingSeriesObjectAudioConnectionOptionsAudioConnectionType(str, Enum):
    #: Provide a hybrid audio option, allowing attendees to join using their computer audio or a phone.
    webex_audio = 'webexAudio'
    #: Only restricts attendees to join the audio portion of the meeting using their computer instead of a telephone
    #: option.
    vo_ip = 'VoIP'
    #: Other teleconference services.
    other = 'other'
    #: The way of attendees join the audio portion of the meeting is the default value.
    none_ = 'none'


class MeetingSeriesObjectAudioConnectionOptionsEntryAndExitTone(str, Enum):
    #: All call-in users joining the meeting will hear the beep.
    beep = 'beep'
    #: All call-in users joining the meeting will hear their names.
    announce_name = 'announceName'
    #: Turn off beeps and name announcements.
    no_tone = 'noTone'


class MeetingSeriesObjectAudioConnectionOptions(ApiModel):
    #: Choose how meeting attendees join the audio portion of the meeting.
    #: example: webexAudio
    audio_connection_type: Optional[MeetingSeriesObjectAudioConnectionOptionsAudioConnectionType] = None
    #: Whether or not to show toll-free call-in numbers.
    #: example: True
    enabled_toll_free_call_in: Optional[bool] = None
    #: Whether or not to show global call-in numbers to attendees.
    #: example: True
    enabled_global_call_in: Optional[bool] = None
    #: Whether or not to allow attendees to receive a call-back and call-in is available. Can only be set `true` for a
    #: webinar.
    enabled_audience_call_back: Optional[bool] = None
    #: Select the sound you want users who have a phone audio connection to hear when someone enters or exits the
    #: meeting.
    #: example: beep
    entry_and_exit_tone: Optional[MeetingSeriesObjectAudioConnectionOptionsEntryAndExitTone] = None
    #: Whether or not to allow the host to unmute participants.
    allow_host_to_unmute_participants: Optional[bool] = None
    #: Whether or not to allow attendees to unmute themselves.
    #: example: True
    allow_attendee_to_unmute_self: Optional[bool] = None
    #: Whether or not to auto-mute attendees when attendees enter meetings.
    mute_attendee_upon_entry: Optional[bool] = None


class TrackingCodeItemForCreateMeetingObject(ApiModel):
    #: Name of the tracking code. The name cannot be empty and the maximum size is 120 characters.
    #: example: Department
    name: Optional[str] = None
    #: Value for the tracking code. `value` cannot be empty and the maximum size is 120 characters.
    value: Optional[str] = None


class MeetingSeriesObject(ApiModel):
    #: Unique identifier for meeting. For a meeting series, the `id` is used to identify the entire series. For
    #: scheduled meetings from a series, the `id` is used to identify that scheduled meeting. For a meeting instance
    #: that is in progress or has concluded, the `id` is used to identify that instance.
    #: example: dfb45ece33264639a7bc3dd9535d53f7_20200516T230000Z
    id: Optional[str] = None
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting
    #: instances which have ended.
    #: example: 123456789
    meeting_number: Optional[str] = None
    #: Meeting title. Can be modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: John's Meeting
    title: Optional[str] = None
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long. This attribute can be modified for a
    #: meeting series or a scheduled meeting using the  `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: John's Agenda
    agenda: Optional[str] = None
    #: Meeting password. Applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to
    #: meeting instances which have ended. Can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: BgJep@43
    password: Optional[str] = None
    #: 8-digit numeric password used to join a meeting from audio and video devices. This attribute applies to meeting
    #: series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended.
    #: example: 12345678
    phone_and_video_system_password: Optional[str] = None
    #: Meeting type.
    #: example: meetingSeries
    meeting_type: Optional[MeetingSeriesObjectMeetingType] = None
    #: Meeting state.
    #: example: active
    state: Optional[MeetingSeriesObjectState] = None
    #: `Time zone
    #: <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ of `start` and `end`, conforming with the `IANA time zone database
    #: example: UTC
    timezone: Optional[str] = None
    #: Start time for meeting in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If the meeting is a meeting series, `start` is the date and
    #: time the first meeting of the series starts. If the meeting is a meeting series and the `current` filter is
    #: true, `start` is the date and time the upcoming or ongoing meeting of the series starts. If the meeting is a
    #: scheduled meeting from a meeting series, `start` is the date and time when that scheduled meeting starts. If
    #: the meeting is a meeting instance that has happened or is happening, `start` is the date and time that the
    #: instance actually starts. Can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: 2019-03-18T11:26:30Z
    start: Optional[datetime] = None
    #: End time for a meeting in ISO 8601 compliant format. If the meeting is a meeting series, `end` is the date and
    #: time the first meeting of the series ends. If the meeting is a meeting series and the current filter is true,
    #: `end` is the date and time the upcoming or ongoing meeting of the series ends. If the meeting is a scheduled
    #: meeting from a meeting series, `end` is the date and time when that scheduled meeting ends. If the meeting is a
    #: meeting instance that has happened, `end` is the date and time that instance actually ends. If a meeting
    #: instance is in progress, `end` is not available. Can be modified for a meeting series or a scheduled meeting
    #: using the  `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: 2019-03-18T12:26:30Z
    end: Optional[datetime] = None
    #: Meeting series recurrence rule (conforming with `RFC 2445
    #: <https://www.ietf.org/rfc/rfc2445.txt>`_). Applies only to a recurring meeting series, not to a
    #: meeting series with only one scheduled meeting. Can be modified for a meeting series using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API. Multiple days or dates for monthly or yearly `recurrence` rule are not supported, only
    #: the first day or date specified is taken. For example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12"
    #: is not supported and it will be partially supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10". For a
    #: non-recurring meeting which has no `recurrence`, its `meetingType` is also `meetingSeries` which is a meeting
    #: series with only one occurrence in Webex meeting modeling.
    #: example: FREQ=DAILY;INTERVAL=1;COUNT=10
    recurrence: Optional[str] = None
    #: Unique identifier for the meeting host.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83QkFCQkU5OS1CNDNFLTREM0YtOTE0Ny1BMUU5RDQ2QzlDQTA
    host_user_id: Optional[str] = None
    #: Display name for the meeting host.
    #: example: John Andersen
    host_display_name: Optional[str] = None
    #: Email address for the meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: Key for joining the meeting as host.
    #: example: 123456
    host_key: Optional[str] = None
    #: Site URL for the meeting.
    #: example: site4-example.webex.com
    site_url: Optional[str] = None
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or
    #: join.
    #: example: https://site4-example.webex.com/site4/j.php?MTID=md41817da6a55b0925530cb88b3577b1
    web_link: Optional[str] = None
    #: SIP address for callback from a video system.
    #: example: 123456789@site4-example.webex.com
    sip_address: Optional[str] = None
    #: IP address for callback from a video system.
    #: example: 192.168.100.100
    dial_in_ip_address: Optional[str] = None
    #: Room ID of the associated Webex space. Only applies to ad-hoc meetings and space meetings.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vNDMzZjk0ZjAtOTZhNi0xMWViLWJhOTctOTU3OTNjZDhiY2Q2
    room_id: Optional[str] = None
    #: Whether or not meeting is recorded automatically. Can be modified for a meeting series or a scheduled meeting
    #: using the  `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    enabled_auto_record_meeting: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: meeting. The target site is specified by a `siteUrl` parameter when creating the meeting. If not specified,
    #: it's a user's preferred site. The `allowAnyUserToBeCoHost` attribute can be modified for a meeting series or a
    #: scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    allow_any_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The
    #: `enabledJoinBeforeHost` attribute can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    enabled_join_before_host: Optional[bool] = None
    #: Whether or not to allow any attendee to connect to audio before the host joins the meeting. Only applicable if
    #: the `enabledJoinBeforeHost` attribute is set to `true`. The `enableConnectAudioBeforeHost` attribute can be
    #: modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    enable_connect_audio_before_host: Optional[bool] = None
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. Only
    #: applicable if the `enabledJoinBeforeHost` attribute is set to true. The `joinBeforeHostMinutes` attribute can
    #: be modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API. Valid options for a
    #: meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`, `45`, and `60`. The
    #: default is `0` if not specified.
    #: example: 15
    join_before_host_minutes: Optional[int] = None
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool] = None
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool] = None
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    #: example: 10
    reminder_time: Optional[int] = None
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    #: example: allowJoin
    unlocked_meeting_join_security: Optional[MeetingSeriesObjectUnlockedMeetingJoinSecurity] = None
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar
    #: meeting. All available meeting session types enabled for the user can be retrieved using the
    #: `List Meeting Session Types
    #: <https://developer.webex.com/docs/api/v1/meetings/list-meeting-session-types>`_ API.
    #: example: 3
    session_type_id: Optional[int] = None
    #: Specifies whether the meeting is a regular meeting, a webinar, or a meeting scheduled in the user's
    #: `personal room
    #: <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_.
    #: example: meeting
    scheduled_type: Optional[MeetingSeriesObjectScheduledType] = None
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool] = None
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read
    #: `password management
    #: <https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration>`_ for details. If not specified, a random password conforming to the site's password rules
    #: will be generated automatically.
    #: example: GwLqa@78
    panelist_password: Optional[str] = None
    #: 8-digit numeric panelist password to join a webinar meeting from audio and video devices.
    #: example: 12345678
    phone_and_video_system_panelist_password: Optional[str] = None
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool] = None
    #: The number of minutes after the meeting begins, for automatically locking it.
    #: example: 10
    automatic_lock_minutes: Optional[int] = None
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a
    #: cohost. The target site is specified by the `siteUrl` parameter when creating the meeting. If not specified,
    #: it's a user's preferred site. The `allowFirstUserToBeCoHost` attribute can be modified for a meeting series or
    #: a scheduled meeting uisng the  `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting
    #: without a prompt. This attribute can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    allow_authenticated_devices: Optional[bool] = None
    #: Information for callbacks from a meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[MeetingSeriesObjectTelephony] = None
    #: Meeting Options.
    meeting_options: Optional[MeetingSeriesObjectMeetingOptions] = None
    #: Attendee Privileges. This attribute is not supported for a webinar.
    attendee_privileges: Optional[MeetingSeriesObjectAttendeePrivileges] = None
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information in order
    #: to join the meeting. Meeting invitees will receive an email with a registration link for the registration. When
    #: the registration form has been submitted and approved, an email with a real meeting link will be received. By
    #: clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not
    #: apply to a meeting when it's a recurring meeting with a `recurrence` field or no `password` or when the feature
    #: toggle `DecoupleJBHWithRegistration` is disabled the `Join Before Host` option is enabled for the meeting, See
    #: `Register for a Meeting in Cisco Webex Meetings
    #: <https://help.webex.com/en-us/nmgmeff/Register-for-a-Meeting-in-Cisco-Webex-Meetings>`_ for details.
    registration: Optional[MeetingSeriesObjectRegistration] = None
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs,
    #: Salesforce Opportunity IDs, etc.
    integration_tags: Optional[list[str]] = None
    #: Simultaneous interpretation information for a meeting.
    simultaneous_interpretation: Optional[MeetingSeriesObjectSimultaneousInterpretation] = None
    #: Whether or not breakout sessions are enabled.
    enabled_breakout_sessions: Optional[bool] = None
    #: `HATEOAS
    #: <https://en.wikipedia.org/wiki/HATEOAS>`_ Breakout Sessions information for meeting.
    links: Optional[list[LinksObjectForTelephony]] = None
    #: Tracking codes information.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]] = None
    #: Audio connection options.
    audio_connection_options: Optional[MeetingSeriesObjectAudioConnectionOptions] = None
    #: Require attendees to sign in before joining the webinar.
    require_attendee_login: Optional[bool] = None
    #: Restrict webinar to invited attendees only.
    restrict_to_invitees: Optional[bool] = None


class MeetingSeriesObjectWithAdhocTelephony(ApiModel):
    #: Code for authenticating a user to join teleconference. Users join the teleconference using the call-in number or
    #: the global call-in number, followed by the value of the `accessCode`.
    #: example: 1234567890
    access_code: Optional[str] = None
    #: Array of call-in numbers for joining a teleconference from a phone.
    call_in_numbers: Optional[list[MeetingSeriesObjectTelephonyCallInNumbers]] = None
    #: `HATEOAS
    #: <https://en.wikipedia.org/wiki/HATEOAS>`_ information of global call-in numbers for joining a teleconference from a phone.
    links: Optional[LinksObjectForTelephony] = None


class MeetingSeriesObjectWithAdhocRegistration(ApiModel):
    #: Whether or not meeting registration requests are accepted automatically.
    auto_accept_request: Optional[bool] = None
    #: Whether or not a registrant's first name is required for meeting registration.
    #: example: True
    require_first_name: Optional[bool] = None
    #: Whether or not a registrant's last name is required for meeting registration.
    #: example: True
    require_last_name: Optional[bool] = None
    #: Whether or not a registrant's email is required for meeting registration.
    #: example: True
    require_email: Optional[bool] = None
    #: Whether or not a registrant's job title is required for meeting registration.
    require_job_title: Optional[bool] = None
    #: Whether or not a registrant's company name is required for meeting registration.
    require_company_name: Optional[bool] = None
    #: Whether or not a registrant's first address field is required for meeting registration.
    require_address1: Optional[bool] = None
    #: Whether or not a registrant's second address field is required for meeting registration.
    require_address2: Optional[bool] = None
    #: Whether or not a registrant's city is required for meeting registration.
    require_city: Optional[bool] = None
    #: Whether or not a registrant's state is required for meeting registration.
    require_state: Optional[bool] = None
    #: Whether or not a registrant's postal code is required for meeting registration.
    require_zip_code: Optional[bool] = None
    #: Whether or not a registrant's country or region is required for meeting registration.
    require_country_region: Optional[bool] = None
    #: Whether or not a registrant's work phone number is required for meeting registration.
    require_work_phone: Optional[bool] = None
    #: Whether or not a registrant's fax number is required for meeting registration.
    require_fax: Optional[bool] = None
    #: Maximum number of meeting registrations. This only applies to meetings. The maximum number of participants for
    #: meetings and webinars, with the limit based on the user capacity and controlled by a toggle at the site level.
    #: The default maximum number of participants for webinars is 10000, but the actual maximum number of participants
    #: is limited by the user capacity.
    #: example: 1000
    max_register_num: Optional[int] = None


class MeetingSeriesObjectWithAdhoc(ApiModel):
    #: Unique identifier for meeting. For a meeting series, the `id` is used to identify the entire series. For
    #: scheduled meetings from a series, the `id` is used to identify that scheduled meeting. For a meeting instance
    #: that is in progress or has concluded, the `id` is used to identify that instance.
    #: example: dfb45ece33264639a7bc3dd9535d53f7_20200516T230000Z
    id: Optional[str] = None
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting
    #: instances which have ended.
    #: example: 123456789
    meeting_number: Optional[str] = None
    #: Meeting title. Can be modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: John's Meeting
    title: Optional[str] = None
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long. This attribute can be modified for a
    #: meeting series or a scheduled meeting using the  `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: John's Agenda
    agenda: Optional[str] = None
    #: Meeting password. Applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to
    #: meeting instances which have ended. Can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: BgJep@43
    password: Optional[str] = None
    #: 8-digit numeric password used to join a meeting from audio and video devices. This attribute applies to meeting
    #: series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended.
    #: example: 12345678
    phone_and_video_system_password: Optional[str] = None
    #: Meeting type.
    #: example: meetingSeries
    meeting_type: Optional[MeetingSeriesObjectMeetingType] = None
    #: Meeting state.
    #: example: active
    state: Optional[MeetingSeriesObjectState] = None
    #: If `true`, the meeting is ad-hoc.
    adhoc: Optional[bool] = None
    #: `Time zone
    #: <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ of `start` and `end`, conforming with the `IANA time zone database
    #: example: UTC
    timezone: Optional[str] = None
    #: Start time for meeting in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If the meetingType of this meeting is `meetingSeries`, and
    #: `current` is not specified or is `false`, `start` is the scheduled start time of the first occurrence of this
    #: series. If the meetingType of this meeting is `meetingSeries`, and `current` is not specified or is `false`,
    #: `start` is the scheduled start time of the first occurrence of this series. If the meetingType of this meeting
    #: is `meetingSeries`, and `current` is `true`, `start` is the scheduled start time of the ongoing or upcoming
    #: occurrence in this series. If the meetingType of this meeting is `scheduledMeeting`, `start` is the scheduled
    #: start time of this occurrence. If the meetingType of this meeting is `meeting`, `start` is the actual start
    #: time of this meeting instance. Can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: 2019-03-18T11:26:30Z
    start: Optional[datetime] = None
    #: End time for a meeting in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If the meeting is a meeting series, `end` is the date and
    #: time the first meeting of the series ends. If the meetingType of this meeting is `meetingSeries`, and `current`
    #: is not specified or is `false`, `end` is the scheduled end time of the first occurrence of this series. If the
    #: meetingType of this meeting is `meetingSeries`, and `current` is `true`, `end` is the scheduled end time of the
    #: ongoing or upcoming occurrence in this series. If the meetingType of this meeting is `scheduledMeeting`, `end`
    #: is the scheduled end time of this occurrence. If the meetingType of this meeting is `meeting`, `end` is the
    #: actual end time of this meeting instance. Can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: 2019-03-18T12:26:30Z
    end: Optional[datetime] = None
    #: Meeting series recurrence rule (conforming with `RFC 2445
    #: <https://www.ietf.org/rfc/rfc2445.txt>`_). Applies only to a recurring meeting series, not to a
    #: meeting series with only one scheduled meeting. Can be modified for a meeting series using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API. Multiple days or dates for monthly or yearly `recurrence` rule are not supported, only
    #: the first day or date specified is taken. For example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12"
    #: is not supported and it will be partially supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
    #: example: FREQ=DAILY;INTERVAL=1;COUNT=10
    recurrence: Optional[str] = None
    #: Unique identifier for the meeting host.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83QkFCQkU5OS1CNDNFLTREM0YtOTE0Ny1BMUU5RDQ2QzlDQTA
    host_user_id: Optional[str] = None
    #: Display name for the meeting host.
    #: example: John Andersen
    host_display_name: Optional[str] = None
    #: Email address for the meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: Key for joining the meeting as host.
    #: example: 123456
    host_key: Optional[str] = None
    #: Site URL for the meeting.
    #: example: site4-example.webex.com
    site_url: Optional[str] = None
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or
    #: join.
    #: example: https://site4-example.webex.com/site4/j.php?MTID=md41817da6a55b0925530cb88b3577b1
    web_link: Optional[str] = None
    #: SIP address for callback from a video system.
    #: example: 123456789@site4-example.webex.com
    sip_address: Optional[str] = None
    #: IP address for callback from a video system.
    #: example: 192.168.100.100
    dial_in_ip_address: Optional[str] = None
    #: Room ID of the associated Webex space. Only applies to ad-hoc meetings and space meetings.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vNDMzZjk0ZjAtOTZhNi0xMWViLWJhOTctOTU3OTNjZDhiY2Q2
    room_id: Optional[str] = None
    #: Whether or not meeting is recorded automatically. Can be modified for a meeting series or a scheduled meeting
    #: using the  `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    enabled_auto_record_meeting: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: meeting. The target site is specified by a `siteUrl` parameter when creating the meeting. If not specified,
    #: it's a user's preferred site. The `allowAnyUserToBeCoHost` attribute can be modified for a meeting series or a
    #: scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    allow_any_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The
    #: `enabledJoinBeforeHost` attribute can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    enabled_join_before_host: Optional[bool] = None
    #: Whether or not to allow any attendee to connect to audio before the host joins the meeting. Only applicable if
    #: the `enabledJoinBeforeHost` attribute is set to `true`. The `enableConnectAudioBeforeHost` attribute can be
    #: modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    enable_connect_audio_before_host: Optional[bool] = None
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. Only
    #: applicable if the `enabledJoinBeforeHost` attribute is set to true. The `joinBeforeHostMinutes` attribute can
    #: be modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API. Valid options for a
    #: meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`, `45`, and `60`. The
    #: default is `0` if not specified.
    #: example: 15
    join_before_host_minutes: Optional[int] = None
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool] = None
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool] = None
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    #: example: 10
    reminder_time: Optional[int] = None
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    #: example: allowJoin
    unlocked_meeting_join_security: Optional[MeetingSeriesObjectUnlockedMeetingJoinSecurity] = None
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar
    #: meeting. All available meeting session types enabled for the user can be retrieved using the
    #: `List Meeting Session Types
    #: <https://developer.webex.com/docs/api/v1/meetings/list-meeting-session-types>`_ API.
    #: example: 3
    session_type_id: Optional[int] = None
    #: Specifies whether the meeting is a regular meeting, a webinar, or a meeting scheduled in the user's
    #: `personal room
    #: <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_.
    #: example: meeting
    scheduled_type: Optional[MeetingSeriesObjectScheduledType] = None
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool] = None
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read
    #: `password management
    #: <https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration>`_ for details. If not specified, a random password conforming to the site's password rules
    #: will be generated automatically.
    #: example: GwLqa@78
    panelist_password: Optional[str] = None
    #: 8-digit numeric panelist password to join a webinar meeting from audio and video devices.
    #: example: 12345678
    phone_and_video_system_panelist_password: Optional[str] = None
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool] = None
    #: The number of minutes after the meeting begins, for automatically locking it.
    #: example: 10
    automatic_lock_minutes: Optional[int] = None
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a
    #: cohost. The target site is specified by the `siteUrl` parameter when creating the meeting. If not specified,
    #: it's a user's preferred site. The `allowFirstUserToBeCoHost` attribute can be modified for a meeting series or
    #: a scheduled meeting uisng the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting
    #: without a prompt. This attribute can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    allow_authenticated_devices: Optional[bool] = None
    #: Whether or not this meeting instance has chat.
    has_chat: Optional[bool] = None
    #: Whether or not this meeting instance has a recording.
    has_recording: Optional[bool] = None
    #: Whether or not this meeting instance has a transcription.
    has_transcription: Optional[bool] = None
    #: Whether or not this meeting instance has closed captions.
    has_closed_caption: Optional[bool] = None
    #: Whether or not this meeting instance has polls.
    has_polls: Optional[bool] = None
    #: Whether or not this meeting instance has Q&A.
    has_qa: Optional[bool] = Field(alias='hasQA', default=None)
    #: Information for callbacks from a meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[MeetingSeriesObjectWithAdhocTelephony] = None
    #: Meeting options.
    meeting_options: Optional[MeetingSeriesObjectMeetingOptions] = None
    #: Attendee Privileges. This attribute is not supported for a webinar.
    attendee_privileges: Optional[MeetingSeriesObjectAttendeePrivileges] = None
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information in order
    #: to join the meeting. Meeting invitees will receive an email with a registration link for the registration. When
    #: the registration form has been submitted and approved, an email with a real meeting link will be received. By
    #: clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not
    #: apply to a meeting when it's a recurring meeting with a `recurrence` field or no password, or the `Join Before
    #: Host` option is enabled for the meeting. See `Register for a Meeting in Cisco Webex Meetings
    #: <https://help.webex.com/en-us/nmgmeff/Register-for-a-Meeting-in-Cisco-Webex-Meetings>`_ for details.
    registration: Optional[MeetingSeriesObjectWithAdhocRegistration] = None
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs,
    #: Salesforce Opportunity IDs, etc.
    integration_tags: Optional[list[str]] = None
    #: Simultaneous interpretation information for the meeting.
    simultaneous_interpretation: Optional[MeetingSeriesObjectSimultaneousInterpretation] = None
    #: Tracking codes information.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]] = None
    #: Audio connection options.
    audio_connection_options: Optional[MeetingSeriesObjectAudioConnectionOptions] = None
    #: Require attendees to sign in before joining the webinar.
    require_attendee_login: Optional[bool] = None
    #: Restrict webinar to invited attendees only.
    restrict_to_invitees: Optional[bool] = None


class MeetingSeriesObjectForListMeeting(ApiModel):
    #: Unique identifier for meeting. For a meeting series, the `id` is used to identify the entire series. For
    #: scheduled meetings from a series, the `id` is used to identify that scheduled meeting. For a meeting instance
    #: that is in progress or has concluded, the `id` is used to identify that instance.
    #: example: dfb45ece33264639a7bc3dd9535d53f7_20200516T230000Z
    id: Optional[str] = None
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting
    #: instances which have ended.
    #: example: 123456789
    meeting_number: Optional[str] = None
    #: Meeting title. Can be modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: John's Meeting
    title: Optional[str] = None
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long. This attribute can be modified for a
    #: meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: John's Agenda
    agenda: Optional[str] = None
    #: Meeting password. Applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to
    #: meeting instances which have ended. Can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: BgJep@43
    password: Optional[str] = None
    #: 8-digit numeric password used to join a meeting from audio and video devices. This attribute applies to meeting
    #: series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended.
    #: example: 12345678
    phone_and_video_system_password: Optional[str] = None
    #: Meeting type.
    #: example: meetingSeries
    meeting_type: Optional[MeetingSeriesObjectMeetingType] = None
    #: Meeting state.
    #: example: active
    state: Optional[MeetingSeriesObjectState] = None
    #: Time zone of `start` and `end`, conforming with the `IANA time zone database
    #: <https://www.iana.org/time-zones>`_.
    #: example: UTC
    timezone: Optional[str] = None
    #: Start time for meeting in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If the meetingType of a meeting is `meetingSeries`, `start`
    #: is the scheduled start time of the first occurrence of this series. If the meeting is a meeting series and the
    #: `current` filter is true, `start` is the date and time the upcoming or ongoing meeting of the series starts. If
    #: the meetingType of a meeting is `scheduledMeeting`, `start` is the scheduled start time of this occurrence. If
    #: the meetingType of a meeting is `meeting`, `start` is the actual start time of the meeting instance. Can be
    #: modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: 2019-03-18T11:26:30Z
    start: Optional[datetime] = None
    #: End time for a meeting in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If the meetingType of a meeting is `meetingSeries`, `end`
    #: is the scheduled end time of the first occurrence of this series. If the meeting is a meeting series and the
    #: current filter is true, `end` is the date and time the upcoming or ongoing meeting of the series ends. If the
    #: meetingType of a meeting is `scheduledMeeting`, `end` is the scheduled end time of this occurrence. If the
    #: meetingType of a meeting is `meeting`, `end` is the actual end time of the meeting instance. If a meeting
    #: instance is in progress, `end` is not available. Can be modified for a meeting series or a scheduled meeting
    #: using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: 2019-03-18T12:26:30Z
    end: Optional[datetime] = None
    #: Meeting series recurrence rule (conforming with `RFC 2445
    #: <https://www.ietf.org/rfc/rfc2445.txt>`_). Applies only to a recurring meeting series, not to a
    #: meeting series with only one scheduled meeting. Can be modified for a meeting series using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_
    #: API. Multiple days or dates for monthly or yearly `recurrence` rule are not supported, only the first day or
    #: date specified is taken. For example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported
    #: and it will be partially supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
    #: example: FREQ=DAILY;INTERVAL=1;COUNT=10
    recurrence: Optional[str] = None
    #: Unique identifier for the meeting host.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83QkFCQkU5OS1CNDNFLTREM0YtOTE0Ny1BMUU5RDQ2QzlDQTA
    host_user_id: Optional[str] = None
    #: Display name for the meeting host.
    #: example: John Andersen
    host_display_name: Optional[str] = None
    #: Email address for the meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: Key for joining the meeting as host.
    #: example: 123456
    host_key: Optional[str] = None
    #: Site URL for the meeting.
    #: example: site4-example.webex.com
    site_url: Optional[str] = None
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or
    #: join.
    #: example: https://site4-example.webex.com/site4/j.php?MTID=md41817da6a55b0925530cb88b3577b1
    web_link: Optional[str] = None
    #: SIP address for callback from a video system.
    #: example: 123456789@site4-example.webex.com
    sip_address: Optional[str] = None
    #: IP address for callback from a video system.
    #: example: 192.168.100.100
    dial_in_ip_address: Optional[str] = None
    #: Room ID of the associated Webex space. Only applies to ad-hoc meetings and space meetings.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vNDMzZjk0ZjAtOTZhNi0xMWViLWJhOTctOTU3OTNjZDhiY2Q2
    room_id: Optional[str] = None
    #: Whether or not meeting is recorded automatically. Can be modified for a meeting series or a scheduled meeting
    #: using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    enabled_auto_record_meeting: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: meeting. The target site is specified by a `siteUrl` parameter when creating the meeting. If not specified,
    #: it's a user's preferred site. The `allowAnyUserToBeCoHost` attribute can be modified for a meeting series or a
    #: scheduled meeting using the  `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    allow_any_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The
    #: `enabledJoinBeforeHost` attribute can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    enabled_join_before_host: Optional[bool] = None
    #: Whether or not to allow any attendee to connect to audio before the host joins the meeting. Only applicable if
    #: the `enabledJoinBeforeHost` attribute is set to `true`. The `enableConnectAudioBeforeHost` attribute can be
    #: modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    enable_connect_audio_before_host: Optional[bool] = None
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. Only
    #: applicable if the `enabledJoinBeforeHost` attribute is set to true. The `joinBeforeHostMinutes` attribute can
    #: be modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API. Valid options for a
    #: meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`, `45`, and `60`. The
    #: default is `0` if not specified.
    #: example: 15
    join_before_host_minutes: Optional[int] = None
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool] = None
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool] = None
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    #: example: 10
    reminder_time: Optional[int] = None
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    #: example: allowJoin
    unlocked_meeting_join_security: Optional[MeetingSeriesObjectUnlockedMeetingJoinSecurity] = None
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar
    #: meeting. All available meeting session types enabled for the user can be retrieved using the
    #: `List Meeting Session Types
    #: <https://developer.webex.com/docs/api/v1/meetings/list-meeting-session-types>`_ API.
    #: example: 3
    session_type_id: Optional[int] = None
    #: Specifies whether the meeting is a regular meeting, a webinar, or a meeting scheduled in the user's
    #: `personal room
    #: <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_.
    #: example: meeting
    scheduled_type: Optional[MeetingSeriesObjectScheduledType] = None
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool] = None
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read
    #: `password management
    #: <https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration>`_ for details. If not specified, a random password conforming to the site's password rules
    #: will be generated automatically.
    #: example: GwLqa@78
    panelist_password: Optional[str] = None
    #: 8-digit numeric panelist password to join a webinar meeting from audio and video devices.
    #: example: 12345678
    phone_and_video_system_panelist_password: Optional[str] = None
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool] = None
    #: The number of minutes after the meeting begins, for automatically locking it.
    #: example: 10
    automatic_lock_minutes: Optional[int] = None
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a
    #: cohost. The target site is specified by the `siteUrl` parameter when creating the meeting. If not specified,
    #: it's a user's preferred site. The `allowFirstUserToBeCoHost` attribute can be modified for a meeting series or
    #: a scheduled meeting uisng the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting
    #: without a prompt. This attribute can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    allow_authenticated_devices: Optional[bool] = None
    #: Whether or not this meeting instance has chat.
    has_chat: Optional[bool] = None
    #: Whether or not this meeting instance has a recording.
    has_recording: Optional[bool] = None
    #: Whether or not this meeting instance has a transcription.
    has_transcription: Optional[bool] = None
    #: Whether or not this meeting instance has closed captions.
    has_closed_caption: Optional[bool] = None
    #: Whether or not this meeting instance has polls.
    has_polls: Optional[bool] = None
    #: Whether or not this meeting instance has Q&A.
    has_qa: Optional[bool] = Field(alias='hasQA', default=None)
    #: Information for callbacks from a meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[MeetingSeriesObjectWithAdhocTelephony] = None
    #: Meeting options.
    meeting_options: Optional[MeetingSeriesObjectMeetingOptions] = None
    #: Attendee Privileges. This attribute is not supported for a webinar.
    attendee_privileges: Optional[MeetingSeriesObjectAttendeePrivileges] = None
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information in order
    #: to join the meeting. Meeting invitees will receive an email with a registration link for the registration. When
    #: the registration form has been submitted and approved, an email with a real meeting link will be received. By
    #: clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not
    #: apply to a meeting when it's a recurring meeting with a `recurrence` field or no password, or the `Join Before
    #: Host` option is enabled for the meeting. See `Register for a Meeting in Cisco Webex Meetings
    #: <https://help.webex.com/en-us/nmgmeff/Register-for-a-Meeting-in-Cisco-Webex-Meetings>`_ for details.
    registration: Optional[MeetingSeriesObjectWithAdhocRegistration] = None
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs,
    #: Salesforce Opportunity IDs, etc.
    integration_tags: Optional[list[str]] = None
    #: Simultaneous interpretation information for the meeting.
    simultaneous_interpretation: Optional[MeetingSeriesObjectSimultaneousInterpretation] = None
    #: Tracking codes information.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]] = None
    #: Audio connection options.
    audio_connection_options: Optional[MeetingSeriesObjectAudioConnectionOptions] = None
    #: Require attendees to sign in before joining the webinar.
    require_attendee_login: Optional[bool] = None
    #: Restrict webinar to invited attendees only.
    restrict_to_invitees: Optional[bool] = None


class ScheduledMeetingObject(ApiModel):
    #: Unique identifier for meeting. For a meeting series, the `id` is used to identify the entire series. For
    #: scheduled meetings from a series, the `id` is used to identify that scheduled meeting. For a meeting instance
    #: that is in progress or has concluded, the `id` is used to identify that instance.
    #: example: dfb45ece33264639a7bc3dd9535d53f7_20200516T230000Z
    id: Optional[str] = None
    #: Unique identifier for meeting series. It only apples to scheduled meeting and meeting instance. If it's a
    #: scheduled meeting from a series or a meeting instance that is happening or has happened, the `meetingSeriesId`
    #: is the `id` of the primary series.
    #: example: dfb45ece33264639a7bc3dd9535d53f7
    meeting_series_id: Optional[str] = None
    #: Unique identifier for scheduled meeting which current meeting is associated with. It only apples to meeting
    #: instance which is happening or has happened. It's the `id` of the scheduled meeting this instance is associated
    #: with.
    #: example: dfb45ece33264639a7bc3dd9535d53f7
    scheduled_meeting_id: Optional[str] = None
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting
    #: instances which have ended.
    #: example: 123456789
    meeting_number: Optional[str] = None
    #: Meeting title. Can be modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: John's Meeting
    title: Optional[str] = None
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long. This attribute can be modified for a
    #: meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: John's Agenda
    agenda: Optional[str] = None
    #: Meeting password. Applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to
    #: meeting instances which have ended. Can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: BgJep@43
    password: Optional[str] = None
    #: 8-digit numeric password used to join a meeting from audio and video devices. This attribute applies to meeting
    #: series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended.
    #: example: 12345678
    phone_and_video_system_password: Optional[str] = None
    #: Meeting type.
    #: example: scheduledMeeting
    meeting_type: Optional[MeetingSeriesObjectMeetingType] = None
    #: Meeting state.
    #: example: scheduled
    state: Optional[MeetingSeriesObjectState] = None
    #: This state only applies to scheduled meeting. Flag identifying whether or not the scheduled meeting has been
    #: modified.
    is_modified: Optional[bool] = None
    #: `Time zone
    #: <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ of `start` and `end`, conforming with the `IANA time zone database
    #: example: UTC
    timezone: Optional[str] = None
    #: Start time for meeting in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If the meetingType of a meeting is `meetingSeries`, `start`
    #: is the scheduled start time of the first occurrence of this series. If the meeting is a meeting series and the
    #: `current` filter is true, `start` is the date and time the upcoming or ongoing meeting of the series starts. If
    #: the meetingType of a meeting is `scheduledMeeting`, `start` is the scheduled start time of this occurrence. If
    #: the meetingType of a meeting is `meeting`, `start` is the actual start time of the meeting instance. Can be
    #: modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: 2019-03-18T11:26:30Z
    start: Optional[datetime] = None
    #: End time for a meeting in `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If the meetingType of a meeting is `meetingSeries`, `end`
    #: is the scheduled end time of the first occurrence of this series. If the meeting is a meeting series and the
    #: current filter is true, `end` is the date and time the upcoming or ongoing meeting of the series ends. If the
    #: meetingType of a meeting is `scheduledMeeting`, `end` is the scheduled end time of this occurrence. If the
    #: meetingType of a meeting is `meeting`, `end` is the actual end time of the meeting instance. If a meeting
    #: instance is in progress, `end` is not available. Can be modified for a meeting series or a scheduled meeting
    #: using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    #: example: 2019-03-18T12:26:30Z
    end: Optional[datetime] = None
    #: Unique identifier for the meeting host.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS83QkFCQkU5OS1CNDNFLTREM0YtOTE0Ny1BMUU5RDQ2QzlDQTA
    host_user_id: Optional[str] = None
    #: Display name for the meeting host.
    #: example: John Andersen
    host_display_name: Optional[str] = None
    #: Email address for the meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: Key for joining the meeting as host.
    #: example: 123456
    host_key: Optional[str] = None
    #: Site URL for the meeting.
    #: example: site4-example.webex.com
    site_url: Optional[str] = None
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or
    #: join.
    #: example: https://site4-example.webex.com/site4/j.php?MTID=md41817da6a55b0925530cb88b3577b1
    web_link: Optional[str] = None
    #: SIP address for callback from a video system.
    #: example: 123456789@site4-example.webex.com
    sip_address: Optional[str] = None
    #: IP address for callback from a video system.
    #: example: 192.168.100.100
    dial_in_ip_address: Optional[str] = None
    #: Room ID of the associated Webex space. Only applies to ad-hoc meetings and space meetings.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vNDMzZjk0ZjAtOTZhNi0xMWViLWJhOTctOTU3OTNjZDhiY2Q2
    room_id: Optional[str] = None
    #: Whether or not meeting is recorded automatically. Can be modified for a meeting series or a scheduled meeting
    #: using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    enabled_auto_record_meeting: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: meeting. The target site is specified by a `siteUrl` parameter when creating the meeting. If not specified,
    #: it's a user's preferred site. The `allowAnyUserToBeCoHost` attribute can be modified for a meeting series or a
    #: scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    allow_any_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The
    #: `enabledJoinBeforeHost` attribute can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    enabled_join_before_host: Optional[bool] = None
    #: Whether or not to allow any attendee to connect to audio before the host joins the meeting. Only applicable if
    #: the `enabledJoinBeforeHost` attribute is set to `true`. The `enableConnectAudioBeforeHost` attribute can be
    #: modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    enable_connect_audio_before_host: Optional[bool] = None
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. Only
    #: applicable if the `enabledJoinBeforeHost` attribute is set to true. The `joinBeforeHostMinutes` attribute can
    #: be modified for a meeting series or a scheduled meeting using the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API. Valid options for a
    #: meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`, `45`, and `60`. The
    #: default is `0` if not specified.
    #: example: 15
    join_before_host_minutes: Optional[int] = None
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool] = None
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool] = None
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    #: example: 10
    reminder_time: Optional[int] = None
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    #: example: allowJoin
    unlocked_meeting_join_security: Optional[MeetingSeriesObjectUnlockedMeetingJoinSecurity] = None
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar
    #: meeting. All available meeting session types enabled for the user can be retrieved using the
    #: `List Meeting Session Types
    #: <https://developer.webex.com/docs/api/v1/meetings/list-meeting-session-types>`_ API.
    #: example: 3
    session_type_id: Optional[int] = None
    #: Specifies whether the meeting is a regular meeting, a webinar, or a meeting scheduled in the user's
    #: `personal room
    #: <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_.
    #: example: meeting
    scheduled_type: Optional[MeetingSeriesObjectScheduledType] = None
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool] = None
    #: Password for panelists of webinar meeting. Must conform to the site's password complexity settings. Read
    #: `password management
    #: <https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration>`_ for details. If not specified, a random password conforming to the site's password rules
    #: will be generated automatically.
    #: example: GwLqa@78
    panelist_password: Optional[str] = None
    #: 8-digit numeric panelist password to join webinar meeting from audio and video devices.
    #: example: 12345678
    phone_and_video_system_panelist_password: Optional[str] = None
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool] = None
    #: The number of minutes after the meeting begins, for automatically locking it.
    #: example: 10
    automatic_lock_minutes: Optional[int] = None
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a
    #: cohost. The target site is specified by the `siteUrl` parameter when creating the meeting. If not specified,
    #: it's a user's preferred site. The `allowFirstUserToBeCoHost` attribute can be modified for a meeting series or
    #: a scheduled meeting uisng the `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting
    #: without a prompt. This attribute can be modified for a meeting series or a scheduled meeting using the
    #: `Update a Meeting
    #: <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ API.
    allow_authenticated_devices: Optional[bool] = None
    #: Whether or not this meeting instance has chat.
    has_chat: Optional[bool] = None
    #: Whether or not this meeting instance has a recording.
    has_recording: Optional[bool] = None
    #: Whether or not this meeting instance has a transcription.
    has_transcription: Optional[bool] = None
    #: Whether or not this meeting instance has closed captions.
    has_closed_caption: Optional[bool] = None
    #: Whether or not this meeting instance has polls.
    has_polls: Optional[bool] = None
    #: Whether or not this meeting instance has Q&A.
    has_qa: Optional[bool] = Field(alias='hasQA', default=None)
    #: Information for callbacks from a meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[MeetingSeriesObjectTelephony] = None
    #: Meeting Options.
    meeting_options: Optional[MeetingSeriesObjectMeetingOptions] = None
    #: Attendee Privileges. This attribute is not supported for a webinar.
    attendee_privileges: Optional[MeetingSeriesObjectAttendeePrivileges] = None
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information in order
    #: to join the meeting. Meeting invitees will receive an email with a registration link for the registration. When
    #: the registration form has been submitted and approved, an email with a real meeting link will be received. By
    #: clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not
    #: apply to a meeting when it's a recurring meeting with a `recurrence` field or no `password` or when the feature
    #: toggle `DecoupleJBHWithRegistration` is disabled the `Join Before Host` option is enabled for the meeting, See
    #: `Register for a Meeting in Cisco Webex Meetings
    #: <https://help.webex.com/en-us/nmgmeff/Register-for-a-Meeting-in-Cisco-Webex-Meetings>`_ for details.
    registration: Optional[MeetingSeriesObjectWithAdhocRegistration] = None
    #: External keys created by an integration application in its domain, for example, Zendesk ticket IDs, Jira IDs,
    #: Salesforce Opportunity IDs, etc.
    integration_tags: Optional[list[str]] = None
    #: Whether or not breakout sessions are enabled.
    enabled_breakout_sessions: Optional[bool] = None
    #: `HATEOAS
    #: <https://en.wikipedia.org/wiki/HATEOAS>`_ Breakout Sessions information for meeting.
    links: Optional[list[LinksObjectForTelephony]] = None
    #: Tracking codes information.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]] = None
    #: Audio connection options.
    audio_connection_options: Optional[MeetingSeriesObjectAudioConnectionOptions] = None
    #: Require attendees to sign in before joining the webinar.
    require_attendee_login: Optional[bool] = None
    #: Restrict webinar to invited attendees only.
    restrict_to_invitees: Optional[bool] = None


class CustomizedQuestionForCreateMeetingOptions(ApiModel):
    #: The content of the option.
    #: example: green
    value: Optional[str] = None


class CustomizedQuestionForCreateMeetingRules(ApiModel):
    #: Judgment expression for approval rules.
    #: example: contains
    condition: Optional[CustomizedQuestionForCreateMeetingRulesCondition] = None
    #: The keyword for the approval rule. If the rule matches the keyword, the corresponding action will be executed.
    #: example: tom
    value: Optional[str] = None
    #: The automatic approval result for the approval rule.
    #: example: approve
    result: Optional[CustomizedQuestionForCreateMeetingRulesResult] = None
    #: Whether to check the case of values.
    #: example: True
    match_case: Optional[bool] = None


class CustomizedQuestionForCreateMeeting(ApiModel):
    #: Title of the customized question.
    #: example: How are you
    question: Optional[str] = None
    #: Whether or not the customized question is required to be answered by participants.
    #: example: True
    required: Optional[bool] = None
    #: Type of the question being asked.
    type: Optional[CustomizedQuestionForCreateMeetingType] = None
    #: The maximum length of a string that can be entered by the user, ranging from `0` to `999`. Only required by
    #: `singleLineTextBox` and `multiLineTextBox`.
    max_length: Optional[int] = None
    #: The content of `options`. Required if the question type is one of `checkbox`, `dropdownList`, or `radioButtons`.
    options: Optional[list[CustomizedQuestionForCreateMeetingOptions]] = None
    #: The automatic approval rules for customized questions.
    rules: Optional[list[CustomizedQuestionForCreateMeetingRules]] = None


class CreateMeetingObjectRegistration(ApiModel):
    #: Whether or not meeting registration request is accepted automatically.
    auto_accept_request: Optional[bool] = None
    #: Whether or not a registrant's first name is required for meeting registration. This option must always be
    #: `true`.
    #: example: True
    require_first_name: Optional[bool] = None
    #: Whether or not a registrant's last name is required for meeting registration. This option must always be `true`.
    #: example: True
    require_last_name: Optional[bool] = None
    #: Whether or not a registrant's email is required for meeting registration. This option must always be `true`.
    #: example: True
    require_email: Optional[bool] = None
    #: Whether or not a registrant's job title is shown or required for meeting registration.
    require_job_title: Optional[bool] = None
    #: Whether or not a registrant's company name is shown or required for meeting registration.
    require_company_name: Optional[bool] = None
    #: Whether or not a registrant's first address field is shown or required for meeting registration.
    require_address1: Optional[bool] = None
    #: Whether or not a registrant's second address field is shown or required for meeting registration.
    require_address2: Optional[bool] = None
    #: Whether or not a registrant's city is shown or required for meeting registration.
    require_city: Optional[bool] = None
    #: Whether or not a registrant's state is shown or required for meeting registration.
    require_state: Optional[bool] = None
    #: Whether or not a registrant's postal code is shown or required for meeting registration.
    require_zip_code: Optional[bool] = None
    #: Whether or not a registrant's country or region is shown or required for meeting registration.
    require_country_region: Optional[bool] = None
    #: Whether or not a registrant's work phone number is shown or required for meeting registration.
    require_work_phone: Optional[bool] = None
    #: Whether or not a registrant's fax number is shown or required for meeting registration.
    require_fax: Optional[bool] = None
    #: Maximum number of meeting registrations. This only applies to meetings. The maximum number of participants for
    #: meetings and webinars, with the limit based on the user capacity and controlled by a toggle at the site level.
    #: The default maximum number of participants for webinars is 10000, but the actual maximum number of participants
    #: is limited by the user capacity.
    #: example: 1000
    max_register_num: Optional[int] = None
    #: Customized questions for meeting registration.
    customized_questions: Optional[list[CustomizedQuestionForCreateMeeting]] = None
    #: The approval rules for standard questions.
    rules: Optional[list[StandardRegistrationApproveRule]] = None


class CreateMeetingObjectSimultaneousInterpretation(ApiModel):
    #: Whether or not simultaneous interpretation is enabled.
    enabled: Optional[bool] = None
    #: Interpreters for meeting.
    interpreters: Optional[list[InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting]] = None


class BreakoutSessionObject(ApiModel):
    #: Name for breakout session.
    #: example: Breakout Session Name
    name: Optional[str] = None
    #: Invitees for breakout session. Please note that one invitee cannot be assigned to more than one breakout
    #: session.
    invitees: Optional[list[str]] = None


class CreateMeetingObject(ApiModel):
    #: Whether or not to create an ad-hoc meeting for the room specified by `roomId`. When `true`, `roomId` is
    #: required.
    adhoc: Optional[bool] = None
    #: Unique identifier for the Webex space which the meeting is to be associated with. It can be retrieved by
    #: `List Rooms
    #: <https://developer.webex.com/docs/api/v1/rooms/list-rooms>`_. `roomId` is required when `adhoc` is `true`. When `roomId` is specified, the parameter `hostEmail`
    #: will be ignored.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vNDMzZjk0ZjAtOTZhNi0xMWViLWJhOTctOTU3OTNjZDhiY2Q2
    room_id: Optional[str] = None
    #: Unique identifier for meeting template. Please note that `start` and `end` are optional when `templateId` is
    #: specified. The list of meeting templates that is available for the authenticated user can be retrieved from
    #: `List Meeting Templates
    #: <https://developer.webex.com/docs/api/v1/meetings/list-meeting-templates>`_. This parameter is ignored for an ad-hoc meeting.
    #: example: N2Q3ZWE1ZjQyYjkyMWVhY2UwNTM4NmNhMjRhZDczMGU6VS0yMDA5NzItTUMtZW5fVVM
    template_id: Optional[str] = None
    #: Meeting title. The title can be a maximum of 128 characters long. The default value for an ad-hoc meeting is the
    #: user's name if not specified.
    #: example: John's Meeting
    title: Optional[str] = None
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long.
    #: example: John's Agenda
    agenda: Optional[str] = None
    #: Meeting password. Must conform to the site's password complexity settings. Read `password management
    #: <https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration>`_ for details.
    #: If not specified, a random password conforming to the site's password rules will be generated automatically.
    #: example: BgJep@43
    password: Optional[str] = None
    #: Date and time for the start of meeting in any `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `start` cannot be before current date
    #: and time or after `end`. Duration between `start` and `end` cannot be shorter than 10 minutes or longer than 23
    #: hours 59 minutes. Please note that when a meeting is being scheduled, `start` of the meeting will be accurate
    #: to minutes, not seconds or milliseconds. Therefore, if `start` is within the same minute as the current time,
    #: `start` will be adjusted to the upcoming minute; otherwise, `start` will be adjusted with seconds and
    #: milliseconds stripped off. For instance, if the current time is `2022-03-01T10:32:16.657+08:00`, `start` of
    #: `2022-03-01T10:32:28.076+08:00` or `2022-03-01T10:32:41+08:00` will be adjusted to `2022-03-01T10:33:00+08:00`,
    #: and `start` of `2022-03-01T11:32:28.076+08:00` or `2022-03-01T11:32:41+08:00` will be adjusted to
    #: `2022-03-01T11:32:00+08:00`. The default value for an ad-hoc meeting is 5 minutes after the current time and
    #: the user's input value will be ignored. An ad-hoc meeting can be started immediately even if the `start` is 5
    #: minutes after the current time.
    #: example: 2020-05-15T20:30:00-08:00
    start: Optional[datetime] = None
    #: Date and time for the end of meeting in any `ISO 8601
    #: <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `end` cannot be before current date and
    #: time or before `start`. Duration between `start` and `end` cannot be shorter than 10 minutes or longer than 23
    #: hours 59 minutes. Please note that when a meeting is being scheduled, `end` of the meeting will be accurate to
    #: minutes, not seconds or milliseconds. Therefore, `end` will be adjusted with seconds and milliseconds stripped
    #: off. For instance, `end` of `2022-03-01T11:52:28.076+08:00` or `2022-03-01T11:52:41+08:00` will be adjusted to
    #: `2022-03-01T11:52:00+08:00`. The default value for an ad-hoc meeting is 20 minutes after the current time and
    #: the user's input value will be ignored.
    #: example: 2020-05-15T21:30:00-08:00
    end: Optional[datetime] = None
    #: `Time zone
    #: <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in which the meeting was originally scheduled (conforming with the `IANA time zone database
    #: default value for an ad-hoc meeting is `UTC` and the user's input value will be ignored.
    #: example: America/Los_Angeles
    timezone: Optional[str] = None
    #: Meeting series recurrence rule (conforming with `RFC 2445
    #: <https://www.ietf.org/rfc/rfc2445.txt>`_), applying only to meeting series. It doesn't apply to
    #: a scheduled meeting or an ended or ongoing meeting instance. This parameter is ignored for an ad-hoc meeting.
    #: Multiple days or dates for monthly or yearly `recurrence` rule are not supported, only the first day or date
    #: specified is taken. For example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it
    #: will be partially supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
    #: example: FREQ=DAILY;INTERVAL=1;COUNT=20
    recurrence: Optional[str] = None
    #: Whether or not meeting is recorded automatically.
    enabled_auto_record_meeting: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: meeting. The target site is specified by `siteUrl` parameter when creating the meeting; if not specified, it's
    #: the user's preferred site. The default value for an ad-hoc meeting is `true` and the user's input value will be
    #: ignored.
    allow_any_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The default value
    #: for an ad-hoc meeting is `true` and the user's input value will be ignored.
    enabled_join_before_host: Optional[bool] = None
    #: Whether or not to allow any attendee to connect audio in the meeting before the host joins the meeting. This
    #: attribute is only applicable if the `enabledJoinBeforeHost` attribute is set to true. The default value for an
    #: ad-hoc meeting is `true` and the user's input value will be ignored.
    enable_connect_audio_before_host: Optional[bool] = None
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. This
    #: attribute is only applicable if the `enabledJoinBeforeHost` attribute is set to true. Valid options for a
    #: meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`, `45`, and `60`. The
    #: default value for an ad-hoc meeting is 0 and the user's input value will be ignored.
    #: example: 15
    join_before_host_minutes: Optional[int] = None
    #: Whether or not to exclude the meeting password from the email invitation. This parameter is ignored for an
    #: ad-hoc meeting.
    exclude_password: Optional[bool] = None
    #: Whether or not to allow the meeting to be listed on the public calendar. The default value for an ad-hoc meeting
    #: is `false` and the user's input value will be ignored.
    public_meeting: Optional[bool] = None
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host. This parameter is
    #: ignored for an ad-hoc meeting.
    #: example: 10
    reminder_time: Optional[int] = None
    #: Specifies how the people who aren't on the invite can join the unlocked meeting. The default value for an ad-hoc
    #: meeting is `allowJoinWithLobby` and the user's input value will be ignored.
    #: example: allowJoin
    unlocked_meeting_join_security: Optional[MeetingSeriesObjectUnlockedMeetingJoinSecurity] = None
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar
    #: meeting. All available meeting session types enabled for the user can be retrieved using the
    #: `List Meeting Session Types
    #: <https://developer.webex.com/docs/api/v1/meetings/list-meeting-session-types>`_ API.
    #: example: 3
    session_type_id: Optional[int] = None
    #: When set as an attribute in a POST request body, specifies whether it's a regular meeting, a webinar, or a
    #: meeting scheduled in the user's `personal room
    #: <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_. If not specified, it's a regular meeting by default. The default
    #: value for an ad-hoc meeting is `meeting` and the user's input value will be ignored.
    #: example: meeting
    scheduled_type: Optional[MeetingSeriesObjectScheduledType] = None
    #: Whether or not webcast view is enabled. This parameter is ignored for an ad-hoc meeting.
    enabled_webcast_view: Optional[bool] = None
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read
    #: `password management
    #: <https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration>`_ for details. If not specified, a random password conforming to the site's password rules
    #: will be generated automatically. This parameter is ignored for an ad-hoc meeting.
    #: example: GwLqa@78
    panelist_password: Optional[str] = None
    #: Whether or not to automatically lock the meeting after it starts. The default value for an ad-hoc meeting is
    #: `false` and the user's input value will be ignored.
    enable_automatic_lock: Optional[bool] = None
    #: The number of minutes after the meeting begins, for automatically locking it. The default value for an ad-hoc
    #: meeting is null and the user's input value will be ignored.
    #: example: 10
    automatic_lock_minutes: Optional[int] = None
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a
    #: cohost. The target site is specified by `siteUrl` parameter when creating the meeting; if not specified, it's
    #: user's preferred site. The default value for an ad-hoc meeting is `false` and the user's input value will be
    #: ignored.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting
    #: without a prompt. The default value for an ad-hoc meeting is `true` and the user's input value will be ignored.
    allow_authenticated_devices: Optional[bool] = None
    #: Invitees for meeting. The maximum size of invitees is 1000. If `roomId` is specified and `invitees` is missing,
    #: all the members in the space are invited implicitly. If both `roomId` and `invitees` are specified, only those
    #: in the `invitees` list are invited. `coHost` for each invitee is `true` by default if `roomId` is specified
    #: when creating a meeting, and anyone in the invitee list that is not qualified to be a cohost will be invited as
    #: a non-cohost invitee. The user's input value will be ignored for an ad-hoc meeting and the the members of the
    #: room specified by `roomId` except "me" will be used by default.
    invitees: Optional[list[InviteeObjectForCreateMeeting]] = None
    #: Whether or not to send emails to host and invitees. It is an optional field and default value is true. The
    #: default value for an ad-hoc meeting is `false` and the user's input value will be ignored.
    #: example: True
    send_email: Optional[bool] = None
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin-level scopes. When used, the admin may specify the email of a user in a site they manage to be
    #: the meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: URL of the Webex site which the meeting is created on. If not specified, the meeting is created on user's
    #: preferred site. All available Webex sites and preferred site of the user can be retrieved by `Get Site List`
    #: API.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: Meeting Options.
    meeting_options: Optional[MeetingSeriesObjectMeetingOptions] = None
    #: Attendee Privileges. This attribute is not supported for a webinar.
    attendee_privileges: Optional[MeetingSeriesObjectAttendeePrivileges] = None
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information in order
    #: to join the meeting. Meeting invitees will receive an email with a registration link for the registration. When
    #: the registration form has been submitted and approved, an email with a real meeting link will be received. By
    #: clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not
    #: apply to a meeting when it's a recurring meeting with a `recurrence` field or no `password` or when the feature
    #: toggle `DecoupleJBHWithRegistration` is disabled the `Join Before Host` option is enabled for the meeting, See
    #: `Register for a Meeting in Cisco Webex Meetings
    #: <https://help.webex.com/en-us/nmgmeff/Register-for-a-Meeting-in-Cisco-Webex-Meetings>`_ for details.
    registration: Optional[CreateMeetingObjectRegistration] = None
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs,
    #: Salesforce Opportunity IDs, etc. The integration application queries meetings by a key in its own domain. The
    #: maximum size of `integrationTags` is 3 and each item of `integrationTags` can be a maximum of 64 characters
    #: long. This parameter is ignored for an ad-hoc meeting.
    integration_tags: Optional[list[str]] = None
    #: Simultaneous interpretation information for a meeting.
    simultaneous_interpretation: Optional[CreateMeetingObjectSimultaneousInterpretation] = None
    #: Whether or not breakout sessions are enabled.
    enabled_breakout_sessions: Optional[bool] = None
    #: Breakout sessions are smaller groups that are split off from the main meeting or webinar. They allow a subset of
    #: participants to collaborate and share ideas over audio and video. Use breakout sessions for workshops,
    #: classrooms, or for when you need a moment to talk privately with a few participants outside of the main
    #: session. Please note that maximum number of breakout sessions in a meeting or webinar is 100. In webinars, if
    #: hosts preassign attendees to breakout sessions, the role of `attendee` will be changed to `panelist`. Breakout
    #: session is not supported for a meeting with simultaneous interpretation.
    breakout_sessions: Optional[list[BreakoutSessionObject]] = None
    #: Tracking codes information. All available tracking codes and their options for the specified site can be
    #: retrieved by `List Meeting Tracking Codes
    #: <https://developer.webex.com/docs/api/v1/meetings/list-meeting-tracking-codes>`_ API. If an optional tracking code is missing from the `trackingCodes`
    #: array and there's a default option for this tracking code, the default option is assigned automatically. If the
    #: `inputMode` of a tracking code is `select`, its value must be one of the site-level options or the user-level
    #: value. Tracking code is not supported for a personal room meeting or an ad-hoc space meeting.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]] = None
    #: Audio connection options.
    audio_connection_options: Optional[MeetingSeriesObjectAudioConnectionOptions] = None
    #: Require attendees to sign in before joining the webinar. This option works when the value of `scheduledType`
    #: attribute is `webinar`. Please note that `requireAttendeeLogin` cannot be set if someone has already registered
    #: for the webinar.
    require_attendee_login: Optional[bool] = None
    #: Restrict webinar to invited attendees only. This option works when the registration option is disabled and the
    #: value of `scheduledType` attribute is `webinar`. Please note that `restrictToInvitees` cannot be set to `true`
    #: if `requireAttendeeLogin` is `false`.
    restrict_to_invitees: Optional[bool] = None


class TemplateObjectTemplateType(str, Enum):
    #: Webex meeting.
    meeting = 'meeting'
    #: Webex webinar.
    webinar = 'webinar'


class TemplateObject(ApiModel):
    #: Unique identifier for meeting template.
    #: example: N2Q3ZWE1ZjQyYjkyMWVhY2UwNTM4NmNhMjRhZDczMGU6VS0yMDA5NzItTUMtZW5fVVM
    id: Optional[str] = None
    #: Meeting template name.
    #: example: Meeting template 1
    name: Optional[str] = None
    #: Meeting template locale.
    #: example: en_US
    locale: Optional[str] = None
    #: Site URL for the meeting template.
    #: example: site4-example.webex.com
    site_url: Optional[str] = None
    #: Meeting template type.
    #: example: meeting
    template_type: Optional[TemplateObjectTemplateType] = None
    #: Whether or not the meeting template is a default template.
    is_default: Optional[bool] = None
    #: Whether or not the meeting template is a standard template.
    is_standard: Optional[bool] = None


class DetailedTemplateObject(ApiModel):
    #: Unique identifier for meeting template.
    #: example: N2Q3ZWE1ZjQyYjkyMWVhY2UwNTM4NmNhMjRhZDczMGU6VS0yMDA5NzItTUMtZW5fVVM
    id: Optional[str] = None
    #: Meeting template name.
    #: example: Meeting template 1
    name: Optional[str] = None
    #: Meeting template locale.
    #: example: en_US
    locale: Optional[str] = None
    #: Site URL for the meeting template.
    #: example: site4-example.webex.com
    site_url: Optional[str] = None
    #: Meeting template type.
    #: example: meeting
    template_type: Optional[TemplateObjectTemplateType] = None
    #: Whether or not the meeting template is a default template.
    is_default: Optional[bool] = None
    #: Whether or not the meeting template is a standard template.
    is_standard: Optional[bool] = None
    #: Meeting object which is used to create a meeting by the meeting template. Please note that the meeting object
    #: should be used to create a meeting immediately after retrieval since the `start` and `end` may be invalid
    #: quickly after generation.
    meeting: Optional[CreateMeetingObject] = None


class Control(ApiModel):
    #: Whether the meeting is locked or not.
    locked: Optional[bool] = None
    #: The value can be true or false, it indicates the meeting recording started or not.
    #: example: True
    recording_started: Optional[bool] = None
    #: The value can be true or false, it indicates the meeting recording paused or not.
    #: example: True
    recording_paused: Optional[bool] = None


class Registration(ApiModel):
    #: Whether or not meeting registration requests are accepted automatically.
    auto_accept_request: Optional[bool] = None
    #: Whether or not a registrant's first name is required for meeting registration. This option must always be
    #: `true`.
    #: example: True
    require_first_name: Optional[bool] = None
    #: Whether or not a registrant's last name is required for meeting registration. This option must always be `true`.
    #: example: True
    require_last_name: Optional[bool] = None
    #: Whether or not a registrant's email is required for meeting registration. This option must always be `true`.
    #: example: True
    require_email: Optional[bool] = None
    #: Whether or not a registrant's job title is shown or required for meeting registration.
    require_job_title: Optional[bool] = None
    #: Whether or not a registrant's company name is shown or required for meeting registration.
    require_company_name: Optional[bool] = None
    #: Whether or not a registrant's first address field is shown or required for meeting registration.
    require_address1: Optional[bool] = None
    #: Whether or not a registrant's second address field is shown or required for meeting registration.
    require_address2: Optional[bool] = None
    #: Whether or not a registrant's city is shown or required for meeting registration.
    require_city: Optional[bool] = None
    #: Whether or not a registrant's state is shown or required for meeting registration.
    require_state: Optional[bool] = None
    #: Whether or not a registrant's postal code is shown or required for meeting registration.
    require_zip_code: Optional[bool] = None
    #: Whether or not a registrant's country or region is shown or required for meeting registration.
    require_country_region: Optional[bool] = None
    #: Whether or not a registrant's work phone number is shown or required for meeting registration.
    require_work_phone: Optional[bool] = None
    #: Whether or not a registrant's fax number is shown or required for meeting registration.
    require_fax: Optional[bool] = None
    #: Customized questions for meeting registration.
    customized_questions: Optional[list[CustomizedQuestionForGetMeeting]] = None
    #: The approval rules for standard questions.
    rules: Optional[list[StandardRegistrationApproveRule]] = None


class AnswerForCustomizedQuestion(ApiModel):
    #: Unique identifier for the option.
    #: example: 1
    option_id: Optional[int] = None
    #: The content of the answer or the option for this question.
    #: example: green
    answer: Optional[str] = None


class CustomizedRegistrant(ApiModel):
    #: Unique identifier for the customized questions retrieved from the registration form.
    #: example: 330087
    question_id: Optional[int] = None
    #: The answers for customized questions. If the question type is checkbox, more than one answer can be set.
    answers: Optional[list[AnswerForCustomizedQuestion]] = None


class RegistrantFormObject(ApiModel):
    #: The registrant's first name.
    #: example: Bob
    first_name: Optional[str] = None
    #: The registrant's last name. (Required)
    #: example: Lee
    last_name: Optional[str] = None
    #: The registrant's email.
    #: example: bob@example.com
    email: Optional[str] = None
    #: If `true` send email to the registrant. Default: `true`.
    #: example: True
    send_email: Optional[bool] = None
    #: The registrant's job title. Registration options define whether or not this is required.
    #: example: manager
    job_title: Optional[str] = None
    #: The registrant's company. Registration options define whether or not this is required.
    #: example: Cisco Systems, Inc.
    company_name: Optional[str] = None
    #: The registrant's first address line. Registration options define whether or not this is required.
    #: example: address1 string
    address1: Optional[str] = None
    #: The registrant's second address line. Registration options define whether or not this is required.
    #: example: address2 string
    address2: Optional[str] = None
    #: The registrant's city name. Registration options define whether or not this is required.
    #: example: New York
    city: Optional[str] = None
    #: The registrant's state. Registration options define whether or not this is required.
    #: example: New York
    state: Optional[str] = None
    #: The registrant's postal code. Registration options define whether or not this is required.
    #: example: 123456
    zip_code: Optional[int] = None
    #: The America is not a country or a specific region. Registration options define whether or not this is required.
    #: example: United States
    country_region: Optional[str] = None
    #: The registrant's work phone number. Registration options define whether or not this is required.
    #: example: +1 123456
    work_phone: Optional[str] = None
    #: The registrant's FAX number. Registration options define whether or not this is required.
    #: example: 123456
    fax: Optional[str] = None
    #: The registrant's answers for customized questions. Registration options define whether or not this is required.
    customized_questions: Optional[list[CustomizedRegistrant]] = None


class RegistrantStatus(str, Enum):
    #: Registrant has been approved.
    approved = 'approved'
    #: Registrant is in a pending list waiting for host or cohost approval.
    pending = 'pending'
    #: Registrant has been rejected by the host or cohost.
    rejected = 'rejected'


class Registrant(ApiModel):
    #: New registrant's ID.
    #: example: 123456
    registrant_id: Optional[str] = None
    #: New registrant's status.
    #: example: pending
    status: Optional[RegistrantStatus] = None
    #: Registrant's first name.
    #: example: bob
    first_name: Optional[str] = None
    #: Registrant's last name.
    #: example: Lee
    last_name: Optional[str] = None
    #: Registrant's email.
    #: example: bob@example.com
    email: Optional[str] = None
    #: Registrant's job title.
    #: example: manager
    job_title: Optional[str] = None
    #: Registrant's company.
    #: example: cisco
    company_name: Optional[str] = None
    #: Registrant's first address line.
    #: example: address1 string
    address1: Optional[str] = None
    #: Registrant's second address line.
    #: example: address2 string
    address2: Optional[str] = None
    #: Registrant's city name.
    #: example: New York
    city: Optional[str] = None
    #: Registrant's state.
    #: example: New York
    state: Optional[str] = None
    #: Registrant's postal code.
    #: example: 123456
    zip_code: Optional[int] = None
    #: Registrant's country or region.
    #: example: United States
    country_region: Optional[str] = None
    #: Registrant's work phone number.
    #: example: +1 123456
    work_phone: Optional[str] = None
    #: Registrant's FAX number.
    #: example: 123456
    fax: Optional[str] = None
    #: Registrant's registration time.
    #: example: 2021-09-07T09:29:13+08:00
    registration_time: Optional[datetime] = None
    #: Registrant's answers for customized questions, Registration options define whether or not this is required.
    customized_questions: Optional[list[CustomizedRegistrant]] = None
    #: Registrant's source id.The `sourceId` is from `Create Invitation Sources
    #: <https://developer.webex.com/docs/api/v1/meetings/create-invitation-sources>`_ API.
    #: example: cisco
    source_id: Optional[str] = None
    #: Registrant's registration ID. Registrants have a special number to identify a registrations if it is
    #: webinar-enabled and enabled registration ID.
    #: example: 1111
    registration_id: Optional[str] = None


class RegistrantCreateResponse(ApiModel):
    #: New registrant's ID.
    #: example: 123456
    id: Optional[str] = None
    #: New registrant's status.
    #: example: pending
    status: Optional[RegistrantStatus] = None
    #: Registrant's first name.
    #: example: bob
    first_name: Optional[str] = None
    #: Registrant's last name.
    #: example: Lee
    last_name: Optional[str] = None
    #: Registrant's email.
    #: example: bob@example.com
    email: Optional[str] = None
    #: Registrant's job title.
    #: example: manager
    job_title: Optional[str] = None
    #: Registrant's company.
    #: example: cisco
    company_name: Optional[str] = None
    #: Registrant's first address line.
    #: example: address1 string
    address1: Optional[str] = None
    #: Registrant's second address line.
    #: example: address2 string
    address2: Optional[str] = None
    #: Registrant's city name.
    #: example: New York
    city: Optional[str] = None
    #: Registrant's state.
    #: example: New York
    state: Optional[str] = None
    #: Registrant's postal code.
    #: example: 123456
    zip_code: Optional[int] = None
    #: Registrant's country or region.
    #: example: United States
    country_region: Optional[str] = None
    #: Registrant's work phone number.
    #: example: +1 123456
    work_phone: Optional[str] = None
    #: Registrant's FAX number.
    #: example: 123456
    fax: Optional[str] = None
    #: Registrant's registration time.
    #: example: 2021-09-07T09:29:13+08:00
    registration_time: Optional[datetime] = None
    #: Registrant's answers for customized questions, Registration options define whether or not this is required.
    customized_questions: Optional[list[CustomizedRegistrant]] = None


class Registrants(ApiModel):
    #: Registrant ID.
    #: example: 123456
    id: Optional[str] = None


class QueryRegistrantsOrderType(str, Enum):
    desc = 'DESC'
    asc = 'ASC'


class QueryRegistrantsOrderBy(str, Enum):
    registration_time = 'registrationTime'
    #: Registrant's first name.
    first_name = 'firstName'
    #: Registrant's last name.
    last_name = 'lastName'
    #: Registrant's status.
    status = 'status'
    #: registrant's email.
    email = 'email'


class MeetingSessionTypeObjectType(str, Enum):
    #: Meeting session type for a meeting.
    meeting = 'meeting'
    #: Meeting session type for a webinar.
    webinar = 'webinar'
    #: Meeting session type for a private meeting.
    private_meeting = 'privateMeeting'


class MeetingSessionTypeObject(ApiModel):
    #: Unique identifier for the meeting session type.
    #: example: 628
    id: Optional[str] = None
    #: Name of the meeting session type.
    #: example: Webex Meetings EC 2.0 meeting
    name: Optional[str] = None
    #: Meeting session type.
    #: example: meeting
    type: Optional[MeetingSessionTypeObjectType] = None
    #: The maximum number of attendees for the meeting session type.
    #: example: 1000
    attendees_capacity: Optional[int] = None


class GetBreakoutSessionObject(ApiModel):
    #: Unique identifier for breakout session.
    #: example: 18d2e565770c4eee918784ee333510ec
    id: Optional[str] = None
    #: Name for breakout session.
    #: example: Breakout Session Name
    name: Optional[str] = None
    #: Invitees for breakout session.
    invitees: Optional[list[str]] = None


class JoinMeetingLinkObject(ApiModel):
    #: The link is used to start a meeting as the meeting host. Only the meeting host or cohost can generate the
    #: `startLink`.
    #: example: https://example.dmz.webex.com/wbxmjs/joinservice/sites/example/meeting/download/b9dd6cac53564877b65589cc17d4233e?siteurl=example&integrationJoinToken=QUhTSwAAAIVboyqJZyO/aObaDYnIe0wkyteQTUFUGkboab2OL/M30apxnba6ZI4G37P0uvRMihtrYnt9wk+Wgj4GMTjeKJ0YuiEsi1PYJ9AfQcft60Mt/N6q6jEC+aldJ5PfmR+ic9dsgRn6Pgz9AmyjMSCr/3Zx7VOJXKPzWHZIc4q0EqOqDyUnWu5aEtJUldB/kZYKtUrbPUj4KUQKbc60e0tGt/St3uuBBVCuf7P45GmmyVk+b3xqlol2aUokcKlYtIig8It/NDIY5sCvCg+GHxtoEWHRGVj3+0lhNXiQfNe1vTRH7w==
    start_link: Optional[str] = None
    #: The link is used to join the meeting.
    #: example: https://example.webex.com/wbxmjs/joinservice/sites/example/meeting/download/cdedf9ae847b4f9993f87e62a8889dad?siteurl=example&integrationJoinToken=QUhTSwAAAIVAFMmwcApsg+NPn9DlUdF1yv2eVVq2HaXr2vu0/4Ttl9P38kCzoA3A5CKTcDnLr79X4FSvZnZUmUPlv/4F/4/iverF7eOgZaYM5rgUayI3L9ye6lNyYGNb7ZYEAL6oo4xFUDRo8oE3+H/iBeu+nzQnkKcmnTQQPjzZVJQcZVM9tQ==&principal=QUhTSwAAAIXf3TeZvJmVBoXnIhYAIpNdFJ5pfxSftfCOhmwAlckVkd1ZuyfEMosdWeWGHDsThiN+5I55up8e5By/SIu5dUkL9QPu6qVPVhH24xIxkBHfhasau2XB0VZgyIG64tCkEcwf4s0/gJO3N/2RhWkmB669
    join_link: Optional[str] = None
    #: Expiration time of `joinLink`.
    #: example: 2022-05-30T09:44:08Z
    expiration: Optional[datetime] = None


class QuestionObjectType(str, Enum):
    #: Text input.
    text = 'text'
    #: Rating.
    rating = 'rating'
    #: Check box which requires `options`.
    checkbox = 'checkbox'
    #: Drop down list box which requires `options`.
    single_dropdown = 'singleDropdown'
    #: Single radio button which requires `options`.
    single_radio = 'singleRadio'


class QuestionObject(ApiModel):
    #: Unique identifier for the question.
    #: example: 3388057
    id: Optional[int] = None
    #: Details for the question.
    #: example: Do you like cisco?
    question: Optional[str] = None
    #: Type for the question.
    #: example: text
    type: Optional[QuestionObjectType] = None
    #: The lowest score of the rating question. This attribute will be ingnored, if the value of `type` attribute is
    #: not `rating`.
    #: example: 1
    from_score: Optional[int] = None
    #: The lowest score label of the rating question. This attribute will be ingnored, if the value of `type` attribute
    #: is not `rating`.
    #: example: disagree
    from_label: Optional[str] = None
    #: The highest score of the rating question. This attribute will be ingnored, if the value of `type` attribute is
    #: not `rating`.
    #: example: 5
    to_score: Optional[int] = None
    #: The highest score label of the rating question. This attribute will be ingnored, if the value of `type`
    #: attribute is not `rating`.
    #: example: agree
    to_label: Optional[str] = None
    #: Options for the question. This attribute will be ingnored, if the value of `type` attribute is `text` or
    #: `rating`.
    options: Optional[list[QuestionOptionObject]] = None


class SurveyObject(ApiModel):
    #: Unique identifier for the survey.
    #: example: 18d2e565770c4eee918784ee333510ec
    id: Optional[str] = None
    #: Name for the survey.
    #: example: Survey name
    survey_name: Optional[str] = None
    #: Unique identifier for the meeting.
    #: example: 560d7b784f5143e3be2fc3064a5c4999
    meeting_id: Optional[str] = None
    #: Description for the survey.
    #: example: Survey name
    description: Optional[str] = None
    #: Whether the survey allows attendees to submit anonymously.
    #: example: True
    allow_anonymous_submit: Optional[bool] = None
    #: Questions for the survey.
    questions: Optional[list[QuestionObject]] = None


class QuestionWithAnswersObject(ApiModel):
    #: Unique identifier for the question.
    #: example: 3388057
    id: Optional[int] = None
    #: Details for the question.
    #: example: Do you like cisco?
    question: Optional[str] = None
    #: Type for the question.
    #: example: text
    type: Optional[QuestionObjectType] = None
    #: The user's answers for the question.
    answers: Optional[list[AnswerForCustomizedQuestion]] = None


class SurveyResultObject(ApiModel):
    #: Unique identifier for the survey result.
    #: example: 18d2e565770c4eee918784ee333510ec
    id: Optional[str] = None
    #: Name for the survey.
    #: example: Survey name
    survey_name: Optional[str] = None
    #: Unique identifier for the meeting.
    #: example: 560d7b784f5143e3be2fc3064a5c4999
    meeting_id: Optional[str] = None
    #: Email address of the user who submits the survey.
    #: example: bob@example.com
    email: Optional[str] = None
    #: Name of the user who submits the survey.
    #: example: Bob
    display_name: Optional[str] = None
    #: The time when the user submits the survey.
    #: example: 2022-07-06T14:13:06+08:00
    create_time: Optional[datetime] = None
    #: User's answers for the questions
    questions: Optional[list[QuestionWithAnswersObject]] = None


class SurveyLinkObject(ApiModel):
    #: Participant email.
    #: example: kingu1@example.com
    email: Optional[str] = None
    #: Meeting survey Link for the participant.
    #: example: https://example.webex.com/webappng/sites/example/meeting/surveyPage/fa1fc86f70d74c08bc7dc5a3b499ab98?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaXRlSWQiOjIwNjI4NDIsImJpcnRoVGltZSI6MTY4ODQzODYwODY4NCwiZW1haWwiOiJRVWhUU3dBQUFJVllnWEhTSVJLa2hzN2pIR0lCNzJxVDM3SDc5a1NLWjcwUFNBVG9aekJYeHV3KzhJenZnd3l6ZEJ5ZGFDeGc1TnZLcW9mRHV4RjlqdWpGeWhld3EyRmFsWVpNTU9Sa3drNVRNQWZZR2lTUVFRPT0iLCJtZWV0aW5nSW5zdGFuY2VJZCI6Ijc0Y2YyZTJhMjI0ZDQ3OTViM2QwMjliMDZjMGI4NWFjX0lfMjY0Mzg5MTg4NzU2OTY1MjUxIn0.SDJTSwAAAIVIzXgb0wNfEdKwDeRiGzxLWfhoSG5blNcDoCslAiserg
    survey_link: Optional[str] = None


class InvitationSourceCreateObject(ApiModel):
    #: Source ID for the invitation.
    #: example: cisco
    source_id: Optional[str] = None
    #: Email for invitation source.
    #: example: john001@example.com
    source_email: Optional[str] = None


class InvitationSourceObject(ApiModel):
    #: Unique identifier for invitation source.
    #: example: 1
    id: Optional[str] = None
    #: Source ID for invitation.
    #: example: cisco
    source_id: Optional[str] = None
    #: Email for invitation source.
    #: example: john001@example.com
    source_email: Optional[str] = None
    #: The link bound to `sourceId` can directly join the meeting. If the meeting requires registration,`joinLink` is
    #: not returned.
    #: example: https://example.webex.com/example/j.php?MTID=m6d75f1c875b3e3c5d18c7598036bdd8b
    join_link: Optional[str] = None
    #: The link bound to `sourceId` can directly register the meeting. If the meeting requires registration,
    #: `registerLink` is returned.
    #: example: https://example.webex.com/example/j.php?RGID=rb05b31307b5b820e16594da9d1cfc588
    register_link: Optional[str] = None


class MeetingTrackingCodesObjectInputMode(str, Enum):
    #: Text input.
    text = 'text'
    #: Drop down list which requires `options`.
    select = 'select'
    #: Both text input and select from list.
    editable_select = 'editableSelect'
    #: An input method which is only available for the host profile and sign-up pages.
    host_profile_select = 'hostProfileSelect'
    none_ = 'none'


class MeetingTrackingCodesObjectService(str, Enum):
    #: Tracking codes apply to all services.
    all = 'All'
    #: Users can set tracking codes when scheduling a meeting.
    meeting_center = 'MeetingCenter'
    #: Users can set tracking codes when scheduling an event.
    event_center = 'EventCenter'
    #: Users can set tracking codes when scheduling a training session.
    training_center = 'TrainingCenter'
    #: Users can set tracking codes when scheduling a support meeting.
    support_center = 'SupportCenter'
    none_ = 'none'


class MeetingTrackingCodesObjectType(str, Enum):
    #: Available to be chosen but not compulsory.
    optional = 'optional'
    #: Officially compulsory.
    required = 'required'
    #: The value is set by admin.
    admin_set = 'adminSet'
    #: The value cannot be used.
    not_used = 'notUsed'
    #: This value only applies to the service of `All`. When the type of `All` for a tracking code is `notApplicable`,
    #: there are different types for different services. For example, `required` for `MeetingCenter`, `optional` for
    #: `EventCenter` and `notUsed` for others.
    not_applicable = 'notApplicable'
    none_ = 'none'


class OptionsForTrackingCodeObject(ApiModel):
    #: The value of a tracking code option. `value` cannot be empty and the maximum size is 120 characters.
    value: Optional[str] = None
    #: Whether or not the option is the default option of a tracking code.
    default_value: Optional[bool] = None


class MeetingTrackingCodesObject(ApiModel):
    #: Unique identifier for the tracking code.
    #: example: 1
    id: Optional[str] = None
    #: Name for the tracking code.
    #: example: Department
    name: Optional[str] = None
    #: Site URL for the tracking code.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: Tracking code option list. The options here differ from those in the `site-level tracking codes
    #: <https://developer.webex.com/docs/api/v1/tracking-codes/get-a-tracking-code>`_ and the
    #: `user-level tracking codes
    #: <https://developer.webex.com/docs/api/v1/tracking-codes/get-user-tracking-codes>`_. It is the result of a selective combination of the two. If there's user-level value
    #: for a tracking code, the user-level value becomes the default option for the tracking code, and the site-level
    #: default value becomes non-default.
    options: Optional[list[OptionsForTrackingCodeObject]] = None
    #: The input mode in which the tracking code value can be assigned.
    input_mode: Optional[MeetingTrackingCodesObjectInputMode] = None
    #: Service for schedule or sign up pages
    service: Optional[MeetingTrackingCodesObjectService] = None
    #: Type for meeting scheduler or meeting start pages.
    type: Optional[MeetingTrackingCodesObjectType] = None


class ReassignMeetingErrorDescriptionObject(ApiModel):
    #: Detailed description for the host reassignment of `meetingId` if it fails.
    #: example: The meeting is not found.
    description: Optional[str] = None


class ReassignMeetingResponseObject(ApiModel):
    #: Unique identifier for the meeting to be reassigned host.
    #: example: 560d7b784f5143e3be2fc3064a5c5888
    meeting_id: Optional[str] = None
    #: HTTP status code for the meeting reassignment result.
    #: example: 404
    http_status: Optional[str] = None
    #: General message for the host reassignment of `meetingId` if it fails.
    #: example: The requested resource could not be found.
    message: Optional[str] = None
    #: Detailed descriptions for the host reassignment of `meetingId` if it fails.
    errors: Optional[list[ReassignMeetingErrorDescriptionObject]] = None


class ListMeetingsOfAMeetingSeriesMeetingType(str, Enum):
    scheduled_meeting = 'scheduledMeeting'
    meeting = 'meeting'


class ListMeetingsOfAMeetingSeriesState(str, Enum):
    scheduled = 'scheduled'
    ready = 'ready'
    lobby = 'lobby'
    in_progress = 'inProgress'
    ended = 'ended'
    missed = 'missed'


class BatchUpdateMeetingRegistrantsStatusStatusOpType(str, Enum):
    approve = 'approve'
    reject = 'reject'
    cancel = 'cancel'
    bulk_delete = 'bulkDelete'


class MeetingsApi(ApiChild, base='meetings'):
    """
    Meetings
    
    Meetings are virtual conferences where users can collaborate in real time using audio, video, content sharing,
    chat, online whiteboards, and to collaborate.
    
    This API focuses primarily on the scheduling and management of meetings. You can use the Meetings API to list,
    create, get, update, and delete meetings.
    
    Several types of meeting objects are supported by this API, such as meeting series, scheduled meeting, and ended or
    in-progress meeting instances. See the `Meetings Overview
    <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for more information about the types of meetings.
    
    Refer to the `Meetings API Scopes` section of `Meetings Overview
    <https://developer.webex.com/docs/meetings>`_ for scopes required for each API.
    """

    def create_a_meeting(self, title: str, start: Union[str, datetime], end: Union[str, datetime],
                         invitees: list[InviteeObjectForCreateMeeting],
                         breakout_sessions: list[BreakoutSessionObject], adhoc: bool = None, room_id: str = None,
                         template_id: str = None, agenda: str = None, password: str = None, timezone: str = None,
                         recurrence: str = None, enabled_auto_record_meeting: bool = None,
                         allow_any_user_to_be_co_host: bool = None, enabled_join_before_host: bool = None,
                         enable_connect_audio_before_host: bool = None, join_before_host_minutes: int = None,
                         exclude_password: bool = None, public_meeting: bool = None, reminder_time: int = None,
                         unlocked_meeting_join_security: MeetingSeriesObjectUnlockedMeetingJoinSecurity = None,
                         session_type_id: int = None, scheduled_type: MeetingSeriesObjectScheduledType = None,
                         enabled_webcast_view: bool = None, panelist_password: str = None,
                         enable_automatic_lock: bool = None, automatic_lock_minutes: int = None,
                         allow_first_user_to_be_co_host: bool = None, allow_authenticated_devices: bool = None,
                         send_email: bool = None, host_email: str = None, site_url: str = None,
                         meeting_options: MeetingSeriesObjectMeetingOptions = None,
                         attendee_privileges: MeetingSeriesObjectAttendeePrivileges = None,
                         registration: CreateMeetingObjectRegistration = None, integration_tags: list[str] = None,
                         simultaneous_interpretation: CreateMeetingObjectSimultaneousInterpretation = None,
                         enabled_breakout_sessions: bool = None,
                         tracking_codes: list[TrackingCodeItemForCreateMeetingObject] = None,
                         audio_connection_options: MeetingSeriesObjectAudioConnectionOptions = None,
                         require_attendee_login: bool = None,
                         restrict_to_invitees: bool = None) -> MeetingSeriesObjectWithAdhoc:
        """
        Create a Meeting

        Creates a new meeting. Regular users can schedule up to 100 meetings in 24 hours and admin users up to 3000
        overall or 800 for a single user. Please note that the failed requests are also counted toward the limits.

        * If the parameter `adhoc` is `true` and `roomId` is specified, an ad-hoc meeting is created for the target
        room. An ad-hoc meeting is a non-recurring instant meeting for the target room which is supposed to be started
        immediately after being created for a quick collaboration. There's only one ad-hoc meeting for a room at the
        same time. So, if there's already an ongoing ad-hoc meeting for the room, the API returns this ongoing meeting
        instead of creating a new one. If it's a `direct
        <https://developer.webex.com/docs/api/v1/rooms/get-room-details>`_ room, both members of the room can create an ad-hoc meeting
        for the room. If it's a `group
        <https://developer.webex.com/docs/api/v1/rooms/get-room-details>`_ room, only room members that are in the same `organization
        an ad-hoc meeting for the room. Please note that an ad-hoc meeting is for the purpose of an instant
        collaboration with people in a room, user should not persist the `id` and `meetingNumber` of the ad-hoc
        meeting when it's been created since this meeting may become an inactive ad-hoc meeting for the room if it's
        not been started after being created for a while or it has been started and ended. Each time a user needs an
        ad-hoc meeting for a room, they should create one instead of reusing the previous persisted one. Moreover, for
        the same reason, no email will be sent when an ad-hoc meeting is created. Ad-hoc meetings cannot be updated by
        `Update a Meeting
        <https://developer.webex.com/docs/api/v1/meetings/update-a-meeting>`_ or deleted by `Delete a Meeting
        scheduled meetings of an ad-hoc meeting cannot be listed by `List Meetings of a Meeting Series
        <https://developer.webex.com/docs/api/v1/meetings/list-meetings-of-a-meeting-series>`_, but the ended
        and ongoing instances of ad-hoc meetings can be listed by `List Meetings
        <https://developer.webex.com/docs/api/v1/meetings/list-meetings>`_ and `List Meetings of a Meeting Series

        * If the parameter `adhoc` is `true`, `roomId` is required and the others are optional or ignored.

        * The default value of `title` for an ad-hoc meeting is the user's name if not specified. The following
        parameters for an ad-hoc meeting have default values and the user's input values will be ignored:
        `scheduledType` is always `meeting`; `start` and `end` are 5 minutes after the current time and 20 minutes
        after the current time respectively; `timezone` is `UTC`; `allowAnyUserToBeCoHost`,
        `allowAuthenticatedDevices`, `enabledJoinBeforeHost`, `enableConnectAudioBeforeHost` are always `true`;
        `allowFirstUserToBeCoHost`, `enableAutomaticLock`, `publicMeeting`, `sendEmail` are always `false`; `invitees`
        is the room members except "me"; `joinBeforeHostMinutes` is 5; `automaticLockMinutes` is null;
        `unlockedMeetingJoinSecurity` is `allowJoinWithLobby`. An ad-hoc meeting can be started immediately even if
        the `start` is 5 minutes after the current time.

        * The following parameters are not supported and will be ignored for an ad-hoc meeting: `templateId`,
        `recurrence`, `excludePassword`, `reminderTime`, `registration`, `integrationTags`, `enabledWebcastView`, and
        `panelistPassword`.

        * If the value of the parameter `recurrence` is null, a non-recurring meeting is created.

        * If the parameter `recurrence` has a value, a recurring meeting is created based on the rule defined by the
        value of `recurrence`. For a non-recurring meeting which has no `recurrence` value set, its `meetingType` is
        also `meetingSeries` which is a meeting series with only one occurrence in Webex meeting modeling.

        * If the parameter `templateId` has a value, the meeting is created based on the meeting template specified by
        `templateId`. The list of meeting templates that is available for the authenticated user can be retrieved from
        `List Meeting Templates
        <https://developer.webex.com/docs/api/v1/meetings/list-meeting-templates>`_.

        * If the parameter `siteUrl` has a value, the meeting is created on the specified site. Otherwise, the meeting
        is created on the user's preferred site. All available Webex sites and preferred site of the user can be
        retrieved by `Get Site List` API.

        * If the parameter `scheduledType` equals "personalRoomMeeting", the meeting is created in the user's
        `personal room
        <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_.

        * If the parameter `roomId` has a value, the meeting is created for the Webex space specified by `roomId`. If
        `roomId` is specified but the user calling the API is not a member of the Webex space specified by `roomId`,
        the API will fail even if the user has the admin-level scopes or he is calling the API on behalf of another
        user which is specified by `hostEmail` and is a member of the Webex space.

        :param title: Meeting title. The title can be a maximum of 128 characters long. The default value for an ad-hoc
            meeting is the user's name if not specified.
        :type title: str
        :param start: Date and time for the start of meeting in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `start` cannot be before
            current date and time or after `end`. Duration between `start` and `end` cannot be shorter than 10 minutes
            or longer than 23 hours 59 minutes. Please note that when a meeting is being scheduled, `start` of the
            meeting will be accurate to minutes, not seconds or milliseconds. Therefore, if `start` is within the same
            minute as the current time, `start` will be adjusted to the upcoming minute; otherwise, `start` will be
            adjusted with seconds and milliseconds stripped off. For instance, if the current time is
            `2022-03-01T10:32:16.657+08:00`, `start` of `2022-03-01T10:32:28.076+08:00` or `2022-03-01T10:32:41+08:00`
            will be adjusted to `2022-03-01T10:33:00+08:00`, and `start` of `2022-03-01T11:32:28.076+08:00` or
            `2022-03-01T11:32:41+08:00` will be adjusted to `2022-03-01T11:32:00+08:00`. The default value for an
            ad-hoc meeting is 5 minutes after the current time and the user's input value will be ignored. An ad-hoc
            meeting can be started immediately even if the `start` is 5 minutes after the current time.
        :type start: Union[str, datetime]
        :param end: Date and time for the end of meeting in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `end` cannot be before
            current date and time or before `start`. Duration between `start` and `end` cannot be shorter than 10
            minutes or longer than 23 hours 59 minutes. Please note that when a meeting is being scheduled, `end` of
            the meeting will be accurate to minutes, not seconds or milliseconds. Therefore, `end` will be adjusted
            with seconds and milliseconds stripped off. For instance, `end` of `2022-03-01T11:52:28.076+08:00` or
            `2022-03-01T11:52:41+08:00` will be adjusted to `2022-03-01T11:52:00+08:00`. The default value for an
            ad-hoc meeting is 20 minutes after the current time and the user's input value will be ignored.
        :type end: Union[str, datetime]
        :param invitees: Invitees for meeting. The maximum size of invitees is 1000. If `roomId` is specified and
            `invitees` is missing, all the members in the space are invited implicitly. If both `roomId` and
            `invitees` are specified, only those in the `invitees` list are invited. `coHost` for each invitee is
            `true` by default if `roomId` is specified when creating a meeting, and anyone in the invitee list that is
            not qualified to be a cohost will be invited as a non-cohost invitee. The user's input value will be
            ignored for an ad-hoc meeting and the the members of the room specified by `roomId` except "me" will be
            used by default.
        :type invitees: list[InviteeObjectForCreateMeeting]
        :param breakout_sessions: Breakout sessions are smaller groups that are split off from the main meeting or
            webinar. They allow a subset of participants to collaborate and share ideas over audio and video. Use
            breakout sessions for workshops, classrooms, or for when you need a moment to talk privately with a few
            participants outside of the main session. Please note that maximum number of breakout sessions in a
            meeting or webinar is 100. In webinars, if hosts preassign attendees to breakout sessions, the role of
            `attendee` will be changed to `panelist`. Breakout session is not supported for a meeting with
            simultaneous interpretation.
        :type breakout_sessions: list[BreakoutSessionObject]
        :param adhoc: Whether or not to create an ad-hoc meeting for the room specified by `roomId`. When `true`,
            `roomId` is required.
        :type adhoc: bool
        :param room_id: Unique identifier for the Webex space which the meeting is to be associated with. It can be
            retrieved by `List Rooms
            <https://developer.webex.com/docs/api/v1/rooms/list-rooms>`_. `roomId` is required when `adhoc` is `true`. When `roomId` is specified, the
            parameter `hostEmail` will be ignored.
        :type room_id: str
        :param template_id: Unique identifier for meeting template. Please note that `start` and `end` are optional
            when `templateId` is specified. The list of meeting templates that is available for the authenticated user
            can be retrieved from `List Meeting Templates
            <https://developer.webex.com/docs/api/v1/meetings/list-meeting-templates>`_. This parameter is ignored for an ad-hoc meeting.
        :type template_id: str
        :param agenda: Meeting agenda. The agenda can be a maximum of 1300 characters long.
        :type agenda: str
        :param password: Meeting password. Must conform to the site's password complexity settings. Read
            `password management
            <https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration>`_ for details. If not specified, a random password conforming to the site's password
            rules will be generated automatically.
        :type password: str
        :param timezone: `Time zone
            <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in which the meeting was originally scheduled (conforming with the
            `IANA time zone database
            <https://www.iana.org/time-zones>`_). The default value for an ad-hoc meeting is `UTC` and the user's input value will
            be ignored.
        :type timezone: str
        :param recurrence: Meeting series recurrence rule (conforming with `RFC 2445
            <https://www.ietf.org/rfc/rfc2445.txt>`_), applying only to meeting series.
            It doesn't apply to a scheduled meeting or an ended or ongoing meeting instance. This parameter is ignored
            for an ad-hoc meeting. Multiple days or dates for monthly or yearly `recurrence` rule are not supported,
            only the first day or date specified is taken. For example,
            "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported
            as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
        :type recurrence: str
        :param enabled_auto_record_meeting: Whether or not meeting is recorded automatically.
        :type enabled_auto_record_meeting: bool
        :param allow_any_user_to_be_co_host: Whether or not to allow any attendee with a host account on the target
            site to become a cohost when joining the meeting. The target site is specified by `siteUrl` parameter when
            creating the meeting; if not specified, it's the user's preferred site. The default value for an ad-hoc
            meeting is `true` and the user's input value will be ignored.
        :type allow_any_user_to_be_co_host: bool
        :param enabled_join_before_host: Whether or not to allow any attendee to join the meeting before the host joins
            the meeting. The default value for an ad-hoc meeting is `true` and the user's input value will be ignored.
        :type enabled_join_before_host: bool
        :param enable_connect_audio_before_host: Whether or not to allow any attendee to connect audio in the meeting
            before the host joins the meeting. This attribute is only applicable if the `enabledJoinBeforeHost`
            attribute is set to true. The default value for an ad-hoc meeting is `true` and the user's input value
            will be ignored.
        :type enable_connect_audio_before_host: bool
        :param join_before_host_minutes: Number of minutes an attendee can join the meeting before the meeting start
            time and the host joins. This attribute is only applicable if the `enabledJoinBeforeHost` attribute is set
            to true. Valid options for a meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are
            `0`, `15`, `30`, `45`, and `60`. The default value for an ad-hoc meeting is 0 and the user's input value
            will be ignored.
        :type join_before_host_minutes: int
        :param exclude_password: Whether or not to exclude the meeting password from the email invitation. This
            parameter is ignored for an ad-hoc meeting.
        :type exclude_password: bool
        :param public_meeting: Whether or not to allow the meeting to be listed on the public calendar. The default
            value for an ad-hoc meeting is `false` and the user's input value will be ignored.
        :type public_meeting: bool
        :param reminder_time: The number of minutes before the meeting begins, that an email reminder is sent to the
            host. This parameter is ignored for an ad-hoc meeting.
        :type reminder_time: int
        :param unlocked_meeting_join_security: Specifies how the people who aren't on the invite can join the unlocked
            meeting. The default value for an ad-hoc meeting is `allowJoinWithLobby` and the user's input value will
            be ignored.
        :type unlocked_meeting_join_security: MeetingSeriesObjectUnlockedMeetingJoinSecurity
        :param session_type_id: Unique identifier for a meeting session type for the user. This attribute is required
            when scheduling a webinar meeting. All available meeting session types enabled for the user can be
            retrieved using the `List Meeting Session Types
            <https://developer.webex.com/docs/api/v1/meetings/list-meeting-session-types>`_ API.
        :type session_type_id: int
        :param scheduled_type: When set as an attribute in a POST request body, specifies whether it's a regular
            meeting, a webinar, or a meeting scheduled in the user's `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_. If not specified, it's a regular
            meeting by default. The default value for an ad-hoc meeting is `meeting` and the user's input value will
            be ignored.
        :type scheduled_type: MeetingSeriesObjectScheduledType
        :param enabled_webcast_view: Whether or not webcast view is enabled. This parameter is ignored for an ad-hoc
            meeting.
        :type enabled_webcast_view: bool
        :param panelist_password: Password for panelists of a webinar meeting. Must conform to the site's password
            complexity settings. Read `password management
            <https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration>`_ for details. If not specified, a random password conforming
            to the site's password rules will be generated automatically. This parameter is ignored for an ad-hoc
            meeting.
        :type panelist_password: str
        :param enable_automatic_lock: Whether or not to automatically lock the meeting after it starts. The default
            value for an ad-hoc meeting is `false` and the user's input value will be ignored.
        :type enable_automatic_lock: bool
        :param automatic_lock_minutes: The number of minutes after the meeting begins, for automatically locking it.
            The default value for an ad-hoc meeting is null and the user's input value will be ignored.
        :type automatic_lock_minutes: int
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee of the meeting with a host
            account on the target site to become a cohost. The target site is specified by `siteUrl` parameter when
            creating the meeting; if not specified, it's user's preferred site. The default value for an ad-hoc
            meeting is `false` and the user's input value will be ignored.
        :type allow_first_user_to_be_co_host: bool
        :param allow_authenticated_devices: Whether or not to allow authenticated video devices in the meeting's
            organization to start or join the meeting without a prompt. The default value for an ad-hoc meeting is
            `true` and the user's input value will be ignored.
        :type allow_authenticated_devices: bool
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true. The default value for an ad-hoc meeting is `false` and the user's input value will be
            ignored.
        :type send_email: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin-level scopes. When used, the admin may specify the email of a
            user in a site they manage to be the meeting host.
        :type host_email: str
        :param site_url: URL of the Webex site which the meeting is created on. If not specified, the meeting is
            created on user's preferred site. All available Webex sites and preferred site of the user can be
            retrieved by `Get Site List` API.
        :type site_url: str
        :param meeting_options: Meeting Options.
        :type meeting_options: MeetingSeriesObjectMeetingOptions
        :param attendee_privileges: Attendee Privileges. This attribute is not supported for a webinar.
        :type attendee_privileges: MeetingSeriesObjectAttendeePrivileges
        :param registration: Meeting registration. When this option is enabled, meeting invitees must register personal
            information in order to join the meeting. Meeting invitees will receive an email with a registration link
            for the registration. When the registration form has been submitted and approved, an email with a real
            meeting link will be received. By clicking that link the meeting invitee can join the meeting. Please note
            that meeting registration does not apply to a meeting when it's a recurring meeting with a `recurrence`
            field or no `password` or when the feature toggle `DecoupleJBHWithRegistration` is disabled the `Join
            Before Host` option is enabled for the meeting, See `Register for a Meeting in Cisco Webex Meetings
            <https://help.webex.com/en-us/nmgmeff/Register-for-a-Meeting-in-Cisco-Webex-Meetings>`_ for
            details.
        :type registration: CreateMeetingObjectRegistration
        :param integration_tags: External keys created by an integration application in its own domain, for example
            Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries
            meetings by a key in its own domain. The maximum size of `integrationTags` is 3 and each item of
            `integrationTags` can be a maximum of 64 characters long. This parameter is ignored for an ad-hoc meeting.
        :type integration_tags: list[str]
        :param simultaneous_interpretation: Simultaneous interpretation information for a meeting.
        :type simultaneous_interpretation: CreateMeetingObjectSimultaneousInterpretation
        :param enabled_breakout_sessions: Whether or not breakout sessions are enabled.
        :type enabled_breakout_sessions: bool
        :param tracking_codes: Tracking codes information. All available tracking codes and their options for the
            specified site can be retrieved by `List Meeting Tracking Codes
            <https://developer.webex.com/docs/api/v1/meetings/list-meeting-tracking-codes>`_ API. If an optional tracking code is
            missing from the `trackingCodes` array and there's a default option for this tracking code, the default
            option is assigned automatically. If the `inputMode` of a tracking code is `select`, its value must be one
            of the site-level options or the user-level value. Tracking code is not supported for a personal room
            meeting or an ad-hoc space meeting.
        :type tracking_codes: list[TrackingCodeItemForCreateMeetingObject]
        :param audio_connection_options: Audio connection options.
        :type audio_connection_options: MeetingSeriesObjectAudioConnectionOptions
        :param require_attendee_login: Require attendees to sign in before joining the webinar. This option works when
            the value of `scheduledType` attribute is `webinar`. Please note that `requireAttendeeLogin` cannot be set
            if someone has already registered for the webinar.
        :type require_attendee_login: bool
        :param restrict_to_invitees: Restrict webinar to invited attendees only. This option works when the
            registration option is disabled and the value of `scheduledType` attribute is `webinar`. Please note that
            `restrictToInvitees` cannot be set to `true` if `requireAttendeeLogin` is `false`.
        :type restrict_to_invitees: bool
        :rtype: :class:`MeetingSeriesObjectWithAdhoc`
        """
        body = dict()
        if adhoc is not None:
            body['adhoc'] = adhoc
        if room_id is not None:
            body['roomId'] = room_id
        if template_id is not None:
            body['templateId'] = template_id
        body['title'] = title
        if agenda is not None:
            body['agenda'] = agenda
        if password is not None:
            body['password'] = password
        body['start'] = start
        body['end'] = end
        if timezone is not None:
            body['timezone'] = timezone
        if recurrence is not None:
            body['recurrence'] = recurrence
        if enabled_auto_record_meeting is not None:
            body['enabledAutoRecordMeeting'] = enabled_auto_record_meeting
        if allow_any_user_to_be_co_host is not None:
            body['allowAnyUserToBeCoHost'] = allow_any_user_to_be_co_host
        if enabled_join_before_host is not None:
            body['enabledJoinBeforeHost'] = enabled_join_before_host
        if enable_connect_audio_before_host is not None:
            body['enableConnectAudioBeforeHost'] = enable_connect_audio_before_host
        if join_before_host_minutes is not None:
            body['joinBeforeHostMinutes'] = join_before_host_minutes
        if exclude_password is not None:
            body['excludePassword'] = exclude_password
        if public_meeting is not None:
            body['publicMeeting'] = public_meeting
        if reminder_time is not None:
            body['reminderTime'] = reminder_time
        if unlocked_meeting_join_security is not None:
            body['unlockedMeetingJoinSecurity'] = enum_str(unlocked_meeting_join_security)
        if session_type_id is not None:
            body['sessionTypeId'] = session_type_id
        if scheduled_type is not None:
            body['scheduledType'] = enum_str(scheduled_type)
        if enabled_webcast_view is not None:
            body['enabledWebcastView'] = enabled_webcast_view
        if panelist_password is not None:
            body['panelistPassword'] = panelist_password
        if enable_automatic_lock is not None:
            body['enableAutomaticLock'] = enable_automatic_lock
        if automatic_lock_minutes is not None:
            body['automaticLockMinutes'] = automatic_lock_minutes
        if allow_first_user_to_be_co_host is not None:
            body['allowFirstUserToBeCoHost'] = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body['allowAuthenticatedDevices'] = allow_authenticated_devices
        body['invitees'] = loads(TypeAdapter(list[InviteeObjectForCreateMeeting]).dump_json(invitees, by_alias=True, exclude_none=True))
        if send_email is not None:
            body['sendEmail'] = send_email
        if host_email is not None:
            body['hostEmail'] = host_email
        if site_url is not None:
            body['siteUrl'] = site_url
        if meeting_options is not None:
            body['meetingOptions'] = loads(meeting_options.model_dump_json())
        if attendee_privileges is not None:
            body['attendeePrivileges'] = loads(attendee_privileges.model_dump_json())
        if registration is not None:
            body['registration'] = loads(registration.model_dump_json())
        if integration_tags is not None:
            body['integrationTags'] = integration_tags
        if simultaneous_interpretation is not None:
            body['simultaneousInterpretation'] = loads(simultaneous_interpretation.model_dump_json())
        if enabled_breakout_sessions is not None:
            body['enabledBreakoutSessions'] = enabled_breakout_sessions
        body['breakoutSessions'] = loads(TypeAdapter(list[BreakoutSessionObject]).dump_json(breakout_sessions, by_alias=True, exclude_none=True))
        if tracking_codes is not None:
            body['trackingCodes'] = loads(TypeAdapter(list[TrackingCodeItemForCreateMeetingObject]).dump_json(tracking_codes, by_alias=True, exclude_none=True))
        if audio_connection_options is not None:
            body['audioConnectionOptions'] = loads(audio_connection_options.model_dump_json())
        if require_attendee_login is not None:
            body['requireAttendeeLogin'] = require_attendee_login
        if restrict_to_invitees is not None:
            body['restrictToInvitees'] = restrict_to_invitees
        url = self.ep()
        data = super().post(url, json=body)
        r = MeetingSeriesObjectWithAdhoc.model_validate(data)
        return r

    def get_a_meeting(self, meeting_id: str, current: bool = None,
                      host_email: str = None) -> MeetingSeriesObjectWithAdhoc:
        """
        Get a Meeting

        Retrieves details for a meeting with a specified meeting ID.

        * If the `meetingId` value specified is for a meeting series and `current` is `true`, the operation returns
        details for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start or
        the upcoming scheduled meeting of the meeting series.

        * If the `meetingId` value specified is for a meeting series and `current` is `false` or `current` is not
        specified, the operation returns details for the entire meeting series.

        * If the `meetingId` value specified is for a scheduled meeting from a meeting series, the operation returns
        details for that scheduled meeting.

        * If the `meetingId` value specified is for a meeting instance which is happening or has happened, the
        operation returns details for that meeting instance.

        * `trackingCodes` is not supported for ended meeting instances.

        #### Request Header

        * `password`: Meeting password. Required when the meeting is protected by a password and the current user is
        not privileged to view it if they are not a host, cohost or invitee of the meeting.

        * `timezone`: `Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ for time stamps in response body, defined in conformance with the
        `IANA time zone database
        <https://www.iana.org/time-zones>`_. The default value is `UTC` if not specified.

        :param meeting_id: Unique identifier for the meeting being requested.
        :type meeting_id: str
        :param current: Whether or not to retrieve only the current scheduled meeting of the meeting series, i.e. the
            meeting ready to join or start or the upcoming meeting of the meeting series. If it's `true`, return
            details for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start
            or the upcoming scheduled meeting of the meeting series. If it's `false` or not specified, return details
            for the entire meeting series. This parameter only applies to meeting series.
        :type current: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :rtype: :class:`MeetingSeriesObjectWithAdhoc`
        """
        params = {}
        if current is not None:
            params['current'] = str(current).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}')
        data = super().get(url, params=params)
        r = MeetingSeriesObjectWithAdhoc.model_validate(data)
        return r

    def list_meetings(self, meeting_number: str = None, web_link: str = None, room_id: str = None,
                      meeting_type: MeetingSeriesObjectMeetingType = None, state: MeetingSeriesObjectState = None,
                      scheduled_type: MeetingSeriesObjectScheduledType = None, is_modified: bool = None,
                      has_chat: bool = None, has_recording: bool = None, has_transcription: bool = None,
                      has_closed_caption: bool = None, has_polls: bool = None, has_qa: bool = None,
                      current: bool = None, from_: Union[str, datetime] = None, to_: Union[str, datetime] = None,
                      host_email: str = None, site_url: str = None, integration_tag: str = None,
                      **params) -> Generator[MeetingSeriesObjectForListMeeting, None, None]:
        """
        List Meetings

        Retrieves details for meetings with a specified meeting number, web link, meeting type, etc. Please note that
        there are various products in the `Webex Suite
        <https://www.webex.com/collaboration-suite.html>`_ such as `Meetings` and `Events`. Currently, only meetings of the
        `Meetings` product are supported by this API, meetings of others in the suite are not supported. Ad-hoc
        meetings created by `Create a Meeting
        <https://developer.webex.com/docs/api/v1/meetings/create-a-meeting>`_ with `adhoc` of `true` and a `roomId` will not be listed, but the ended
        and ongoing ad-hoc meeting instances will be listed.

        * If `meetingNumber` is specified, the operation returns an array of meeting objects specified by the
        `meetingNumber`. Each object in the array can be a scheduled meeting or a meeting series depending on whether
        the `current` parameter is `true` or `false`, and each object contains the simultaneous interpretation object.
        When `meetingNumber` is specified, parameters of `from`, `to`, `meetingType`, `state`, `isModified` and
        `siteUrl` will be ignored. Please note that `meetingNumber`, `webLink` and `roomId` are mutually exclusive and
        they cannot be specified simultaneously.

        * If `webLink` is specified, the operation returns an array of meeting objects specified by the `webLink`. Each
        object in the array is a scheduled meeting, and each object contains the simultaneous interpretation object.
        When `webLink` is specified, parameters of `current`, `from`, `to`, `meetingType`, `state`, `isModified` and
        `siteUrl` will be ignored. Please note that `meetingNumber`, `webLink` and `roomId` are mutually exclusive and
        they cannot be specified simultaneously.

        * If `roomId` is specified, the operation returns an array of meeting objects of the Webex space specified by
        the `roomId`. When `roomId` is specified, parameters of `current`, `meetingType`, `state` and `isModified`
        will be ignored. The meeting objects are queried on the user's preferred site if no `siteUrl` is specified;
        otherwise, queried on the specified site. `meetingNumber`, `webLink` and `roomId` are mutually exclusive and
        they cannot be specified simultaneously.

        * If `state` parameter is specified, the returned array only has items in the specified state. If `state` is
        not specified, return items of all states.

        * If `meetingType` equals "meetingSeries", the `scheduledType` parameter can be "meeting", "webinar" or null.
        If `scheduledType` is specified, the returned array only has items of the specified scheduled type; otherwise,
        it has items of "meeting" and "webinar".

        * If `meetingType` equals "scheduledMeeting", the `scheduledType` parameter can be "meeting", "webinar",
        "personalRoomMeeting" or null. If `scheduledType` is specified, the returned array only has items of the
        specified scheduled type; otherwise, it has items of all scheduled types.

        * If `meetingType` equals "meeting", the `scheduledType` parameter can be "meeting", "webinar" or null. If
        `scheduledType` is specified, the returned array only has items of the specified scheduled type; otherwise, it
        has items of "meeting" and "webinar". Please note that ended or in-progress meeting instances of `personal room
        <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_
        also fall into the category of "meeting" `scheduledType`.

        * If `isModified` parameter is specified, the returned array only has items which have been modified to
        exceptional meetings. This parameter only applies to scheduled meeting.

        * If any of the `hasChat`, `hasRecording`, `hasTranscription`, `hasClosedCaption`, `hasPolls ` and `hasQA`
        parameters is specified, the `meetingType` must be "meeting" and `state` must be "ended". These parameters are
        null by default.

        * The `current` parameter only applies to meeting series. If it's `false`, the `start` and `end` attributes of
        each returned meeting series object are for the first scheduled meeting of that series. If it's `true` or not
        specified, the `start` and `end` attributes are for the scheduled meeting which is ready to start or join or
        the upcoming scheduled meeting of that series.

        * If `from` and `to` are specified, the operation returns an array of meeting objects in that specified time
        range.

        * If the parameter `siteUrl` has a value, the operation lists meetings on the specified site; otherwise, lists
        meetings on the user's all sites. All available Webex sites of the user can be retrieved by `Get Site List`
        API.

        * `trackingCodes` is not supported for ended meeting instances.

        * A full admin or a content admin can list all the ended and ongoing meeting instances of the organization he
        manages with the `meeting:admin_schedule_read` scope and `meetingType=meeting` parameter.

        #### Request Header

        * `password`: Meeting password. Required when the meeting is protected by a password and the current user is
        not privileged to view it if they are not a host, cohost or invitee of the meeting.

        * `timezone`: `Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ for time stamps in response body, defined in conformance with the
        `IANA time zone database
        <https://www.iana.org/time-zones>`_. The default value is `UTC` if not specified.

        :param meeting_number: Meeting number for the meeting objects being requested. `meetingNumber`, `webLink` and
            `roomId` are mutually exclusive. If it's an exceptional meeting from a meeting series, the exceptional
            meeting instead of the primary meeting series is returned.
        :type meeting_number: str
        :param web_link: URL encoded link to information page for the meeting objects being requested. `meetingNumber`,
            `webLink` and `roomId` are mutually exclusive.
        :type web_link: str
        :param room_id: Associated Webex space ID for the meeting objects being requested. `meetingNumber`, `webLink`
            and `roomId` are mutually exclusive.
        :type room_id: str
        :param meeting_type: Meeting type for the meeting objects being requested. This parameter will be ignored if
            `meetingNumber`, `webLink` or `roomId` is specified.
        :type meeting_type: MeetingSeriesObjectMeetingType
        :param state: Meeting state for the meeting objects being requested. If not specified, return meetings of all
            states. This parameter will be ignored if `meetingNumber`, `webLink` or `roomId` is specified. Details of
            an `ended` meeting will only be available 15 minutes after the meeting has ended. `inProgress` meetings
            are not fully supported. The API will try to return details of an `inProgress` meeting 15 minutes after
            the meeting starts. However, it may take longer depending on the traffic. See the `Webex Meetings
            <https://developer.webex.com/docs/meetings#meeting-states>`_ guide for
            more information about the states of meetings.
        :type state: MeetingSeriesObjectState
        :param scheduled_type: Scheduled type for the meeting objects being requested.
        :type scheduled_type: MeetingSeriesObjectScheduledType
        :param is_modified: Flag identifying whether a meeting has been modified. Only applies to scheduled meetings.
            If `true`, only return modified scheduled meetings; if `false`, only return unmodified scheduled meetings;
            if not specified, all scheduled meetings will be returned.
        :type is_modified: bool
        :param has_chat: Flag identifying whether a meeting has a chat log. Only applies to ended meeting instances. If
            `true`, only return meeting instances which have chats; if `false`, only return meeting instances which
            have no chats; if not specified, all meeting instances will be returned.
        :type has_chat: bool
        :param has_recording: Flag identifying meetings with recordings. Only applies to ended meeting instances. If
            `true`, only return meeting instances which have recordings; if `false`, only return meeting instances
            which have no recordings; if not specified, all meeting instances will be returned.
        :type has_recording: bool
        :param has_transcription: Flag identifying meetings with transcripts. Only applies to ended meeting instances.
            If `true`, only return meeting instances which have transcripts; if `false`, only return meeting instances
            which have no transcripts; if not specified, all meeting instances will be returned.
        :type has_transcription: bool
        :param has_closed_caption: Flag identifying meetings with closed captions. Only applies to ended meeting
            instances. If `true`, only return meeting instances which have closed captions; if `false`, only return
            meeting instances which have no closed captions; if not specified, all meeting instances will be returned.
        :type has_closed_caption: bool
        :param has_polls: Flag identifying meetings with polls. Only applies to ended meeting instances. If `true`,
            only return meeting instances which have polls; if `false`, only return meeting instances which have no
            polls; if not specified, all meeting instances will be returned.
        :type has_polls: bool
        :param has_qa: Flag identifying meetings with Q&A. Only applies to ended meeting instances. If `true`, only
            return meeting instances which have Q&A; if `false`, only return meeting instances which have no Q&A; if
            not specified, all meeting instances will be returned.
        :type has_qa: bool
        :param current: Flag identifying to retrieve the current scheduled meeting of the meeting series or the entire
            meeting series. This parameter only applies to scenarios where `meetingNumber` is specified and the
            meeting is not an exceptional meeting from a meeting series. If it's `true`, return the scheduled meeting
            of the meeting series which is ready to join or start or the upcoming scheduled meeting of the meeting
            series; if it's `false`, return the entire meeting series.
        :type current: bool
        :param from_: Start date and time (inclusive) in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format for the meeting objects being
            requested. `from` cannot be after `to`. This parameter will be ignored if `meetingNumber`, `webLink` or
            `roomId` is specified.
        :type from_: Union[str, datetime]
        :param to_: End date and time (exclusive) in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format for the meeting objects being
            requested. `to` cannot be before `from`. This parameter will be ignored if `meetingNumber`, `webLink` or
            `roomId` is specified.
        :type to_: Union[str, datetime]
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API returns meetings as if the user calling the API were the user of `hostEmail`
            themself, and the meetings returned by the API include the meetings where the user of `hostEmail` is the
            meeting host and those where they are an invitee.
        :type host_email: str
        :param site_url: URL of the Webex site which the API lists meetings from. If not specified, the API lists
            meetings from user's all sites. All available Webex sites of the user can be retrieved by `Get Site List`
            API.
        :type site_url: str
        :param integration_tag: External key created by an integration application. This parameter is used by the
            integration application to query meetings by a key in its own domain such as a Zendesk ticket ID, a Jira
            ID, a Salesforce Opportunity ID, etc.
        :type integration_tag: str
        :return: Generator yielding :class:`MeetingSeriesObjectForListMeeting` instances
        """
        if meeting_number is not None:
            params['meetingNumber'] = meeting_number
        if web_link is not None:
            params['webLink'] = web_link
        if room_id is not None:
            params['roomId'] = room_id
        if meeting_type is not None:
            params['meetingType'] = meeting_type
        if state is not None:
            params['state'] = state
        if scheduled_type is not None:
            params['scheduledType'] = scheduled_type
        if is_modified is not None:
            params['isModified'] = str(is_modified).lower()
        if has_chat is not None:
            params['hasChat'] = str(has_chat).lower()
        if has_recording is not None:
            params['hasRecording'] = str(has_recording).lower()
        if has_transcription is not None:
            params['hasTranscription'] = str(has_transcription).lower()
        if has_closed_caption is not None:
            params['hasClosedCaption'] = str(has_closed_caption).lower()
        if has_polls is not None:
            params['hasPolls'] = str(has_polls).lower()
        if has_qa is not None:
            params['hasQA'] = str(has_qa).lower()
        if current is not None:
            params['current'] = str(current).lower()
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        if integration_tag is not None:
            params['integrationTag'] = integration_tag
        url = self.ep()
        return self.session.follow_pagination(url=url, model=MeetingSeriesObjectForListMeeting, item_key='items', params=params)

    def list_meetings_of_a_meeting_series(self, meeting_series_id: str, from_: Union[str, datetime] = None,
                                          to_: Union[str, datetime] = None,
                                          meeting_type: ListMeetingsOfAMeetingSeriesMeetingType = None,
                                          state: ListMeetingsOfAMeetingSeriesState = None, is_modified: bool = None,
                                          has_chat: bool = None, has_recording: bool = None,
                                          has_transcription: bool = None, has_closed_caption: bool = None,
                                          has_polls: bool = None, has_qa: bool = None, host_email: str = None,
                                          **params) -> Generator[ScheduledMeetingObject, None, None]:
        """
        List Meetings of a Meeting Series

        Lists scheduled meeting and meeting instances of a meeting series identified by `meetingSeriesId`. Scheduled
        meetings of an ad-hoc meeting created by `Create a Meeting
        <https://developer.webex.com/docs/api/v1/meetings/create-a-meeting>`_ with `adhoc` of `true` and a `roomId` will not be
        listed, but the ended and ongoing meeting instances of it will be listed.

        Each _scheduled meeting_ or _meeting_ instance of a _meeting series_ has its own `start`, `end`, etc. Thus, for
        example, when a daily meeting has been scheduled from `2019-04-01` to `2019-04-10`, there are 10 scheduled
        meeting instances in this series, one instance for each day, and each one has its own attributes. When a
        scheduled meeting has been started and ended or is happening, there are even more ended or in-progress meeting
        instances.

        Use this operation to list scheduled meeting and meeting instances of a meeting series within a specific date
        range.

        Long result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        * If any of the `hasChat`, `hasRecording`, `hasTranscription`, `hasClosedCaption`, `hasPolls ` and `hasQA`
        parameters is specified, the `meetingType` must be "meeting" and `state` must be "ended". These parameters are
        null by default.

        * `trackingCodes` is not supported for ended meeting instances.

        #### Request Header

        * `password`: Meeting password. Required when the meeting is protected by a password and the current user is
        not privileged to view it if they are not a host, cohost or invitee of the meeting.

        * `timezone`: `Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ for time stamps in response body, defined in conformance with the
        `IANA time zone database
        <https://www.iana.org/time-zones>`_. The default value is `UTC` if not specified.

        :param meeting_series_id: Unique identifier for the meeting series. Please note that currently meeting ID of a
            scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is not supported for this API.
        :type meeting_series_id: str
        :param from_: Start date and time (inclusive) for the range for which meetings are to be returned in any
            `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `from` cannot be after `to`.
        :type from_: Union[str, datetime]
        :param to_: End date and time (exclusive) for the range for which meetings are to be returned in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_
            compliant format. `to` cannot be before `from`.
        :type to_: Union[str, datetime]
        :param meeting_type: Meeting type for the meeting objects being requested. If not specified, return meetings of
            all types.
        :type meeting_type: ListMeetingsOfAMeetingSeriesMeetingType
        :param state: Meeting state for the meetings being requested. If not specified, return meetings of all states.
            Details of an `ended` meeting will only be available 15 minutes after the meeting has ended. `inProgress`
            meetings are not fully supported. The API will try to return details of an `inProgress` meeting 15 minutes
            after the meeting starts. However, it may take longer depending on the traffic. See the `Webex Meetings
            <https://developer.webex.com/docs/meetings#meeting-states>`_
            guide for more information about the states of meetings.
        :type state: ListMeetingsOfAMeetingSeriesState
        :param is_modified: Flag identifying whether a meeting has been modified. Only applies to scheduled meetings.
            If `true`, only return modified scheduled meetings; if `false`, only return unmodified scheduled meetings;
            if not specified, all scheduled meetings will be returned.
        :type is_modified: bool
        :param has_chat: Flag identifying whether a meeting has a chat log. Only applies to ended meeting instances. If
            `true`, only return meeting instances which have chats; if `false`, only return meeting instances which
            have no chats; if not specified, all meeting instances will be returned.
        :type has_chat: bool
        :param has_recording: Flag identifying meetings with recordings. Only applies to ended meeting instances. If
            `true`, only return meeting instances which have recordings; if `false`, only return meeting instances
            which have no recordings; if not specified, all meeting instances will be returned.
        :type has_recording: bool
        :param has_transcription: Flag identifying meetings with transcripts. Only applies to ended meeting instances.
            If `true`, only return meeting instances which have transcripts; if `false`, only return meeting instances
            which have no transcripts; if not specified, all meeting instances will be returned.
        :type has_transcription: bool
        :param has_closed_caption: Flag identifying meetings with closed captions. Only applies to ended meeting
            instances. If `true`, only return meeting instances which have closed captions; if `false`, only return
            meeting instances which have no closed captions; if not specified, all meeting instances will be returned.
        :type has_closed_caption: bool
        :param has_polls: Flag identifying meetings with polls. Only applies to ended meeting instances. If `true`,
            only return meeting instances which have polls; if `false`, only return meeting instances which have no
            polls; if not specified, all meeting instances will be returned.
        :type has_polls: bool
        :param has_qa: Flag identifying meetings with Q&A. Only applies to ended meeting instances. If `true`, only
            return meeting instances which have Q&A; if `false`, only return meeting instances which have no Q&A; if
            not specified, all meeting instances will be returned.
        :type has_qa: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return meetings that are hosted by that user.
        :type host_email: str
        :return: Generator yielding :class:`ScheduledMeetingObject` instances
        """
        params['meetingSeriesId'] = meeting_series_id
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        if meeting_type is not None:
            params['meetingType'] = meeting_type
        if state is not None:
            params['state'] = state
        if is_modified is not None:
            params['isModified'] = str(is_modified).lower()
        if has_chat is not None:
            params['hasChat'] = str(has_chat).lower()
        if has_recording is not None:
            params['hasRecording'] = str(has_recording).lower()
        if has_transcription is not None:
            params['hasTranscription'] = str(has_transcription).lower()
        if has_closed_caption is not None:
            params['hasClosedCaption'] = str(has_closed_caption).lower()
        if has_polls is not None:
            params['hasPolls'] = str(has_polls).lower()
        if has_qa is not None:
            params['hasQA'] = str(has_qa).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ScheduledMeetingObject, item_key='items', params=params)

    def patch_a_meeting(self, meeting_id: str, title: str = None, agenda: str = None, password: str = None,
                        start: Union[str, datetime] = None, end: Union[str, datetime] = None, timezone: str = None,
                        recurrence: str = None, enabled_auto_record_meeting: bool = None,
                        allow_any_user_to_be_co_host: bool = None, enabled_join_before_host: bool = None,
                        enable_connect_audio_before_host: bool = None, join_before_host_minutes: int = None,
                        exclude_password: bool = None, public_meeting: bool = None, reminder_time: int = None,
                        unlocked_meeting_join_security: MeetingSeriesObjectUnlockedMeetingJoinSecurity = None,
                        session_type_id: int = None, enabled_webcast_view: bool = None, panelist_password: str = None,
                        enable_automatic_lock: bool = None, automatic_lock_minutes: int = None,
                        allow_first_user_to_be_co_host: bool = None, allow_authenticated_devices: bool = None,
                        send_email: bool = None, host_email: str = None, site_url: str = None,
                        meeting_options: MeetingSeriesObjectMeetingOptions = None,
                        attendee_privileges: MeetingSeriesObjectAttendeePrivileges = None,
                        integration_tags: list[str] = None, enabled_breakout_sessions: bool = None,
                        tracking_codes: list[TrackingCodeItemForCreateMeetingObject] = None,
                        audio_connection_options: MeetingSeriesObjectAudioConnectionOptions = None,
                        require_attendee_login: bool = None,
                        restrict_to_invitees: bool = None) -> MeetingSeriesObject:
        """
        Patch a Meeting

        Updates details for a meeting with a specified meeting ID. This operation applies to meeting series and
        scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Ad-hoc meetings created by
        `Create a Meeting
        <https://developer.webex.com/docs/api/v1/meetings/create-a-meeting>`_ with `adhoc` of `true` and a `roomId` cannot be updated.

        * If the `meetingId` value specified is for a scheduled meeting, the operation updates that scheduled meeting
        without impact on other scheduled meeting of the parent meeting series.

        * If the `meetingId` value specified is for a meeting series, the operation updates the entire meeting series.
        **Note**: If the value of `start`, `end`, or `recurrence` for the meeting series is changed, any exceptional
        scheduled meeting in this series is cancelled when the meeting series is updated.

        * The `agenda`, `recurrence`, and `trackingCodes` attributes can be specified as `null` so that these
        attributes become null and hidden from the response after the patch. Note that it's the keyword `null` not the
        string "null".

        :param meeting_id: Unique identifier for the meeting to be updated. This parameter applies to meeting series
            and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Please note that
            currently meeting ID of a scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is not supported for this API.
        :type meeting_id: str
        :param title: Meeting title. The title can be a maximum of 128 characters long.
        :type title: str
        :param agenda: Meeting agenda. The agenda can be a maximum of 1300 characters long. It can be specified `null`
            so that it becomes null and hidden from the response after the patch.
        :type agenda: str
        :param password: Meeting password. Must conform to the site's password complexity settings. Read
            `password management
            <https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration>`_ for details.
        :type password: str
        :param start: Date and time for the start of meeting in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `start` cannot be before
            current date and time or after `end`. Duration between `start` and `end` cannot be shorter than 10 minutes
            or longer than 23 hours 59 minutes. Refer to the `Webex Meetings
            <https://developer.webex.com/docs/meetings#restrictions-on-updating-a-meeting>`_ guide for more information about
            restrictions on updating date and time for a meeting. Please note that when a meeting is being updated,
            `start` of the meeting will be accurate to minutes, not seconds or milliseconds. Therefore, if `start` is
            within the same minute as the current time, `start` will be adjusted to the upcoming minute; otherwise,
            `start` will be adjusted with seconds and milliseconds stripped off. For instance, if the current time is
            `2022-03-01T10:32:16.657+08:00`, `start` of `2022-03-01T10:32:28.076+08:00` or `2022-03-01T10:32:41+08:00`
            will be adjusted to `2022-03-01T10:33:00+08:00`, and `start` of `2022-03-01T11:32:28.076+08:00` or
            `2022-03-01T11:32:41+08:00` will be adjusted to `2022-03-01T11:32:00+08:00`.
        :type start: Union[str, datetime]
        :param end: Date and time for the end of meeting in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `end` cannot be before
            current date and time or before `start`. Duration between `start` and `end` cannot be shorter than 10
            minutes or longer than 23 hours 59 minutes. Refer to the `Webex Meetings
            <https://developer.webex.com/docs/meetings#restrictions-on-updating-a-meeting>`_ guide for more information about
            restrictions on updating date and time for a meeting. Please note that when a meeting is being updated,
            `end` of the meeting will be accurate to minutes, not seconds or milliseconds. Therefore, `end` will be
            adjusted with seconds and milliseconds stripped off. For instance, `end` of
            `2022-03-01T11:52:28.076+08:00` or `2022-03-01T11:52:41+08:00` will be adjusted to
            `2022-03-01T11:52:00+08:00`.
        :type end: Union[str, datetime]
        :param timezone: `Time zone
            <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in which the meeting was originally scheduled (conforming with the
            `IANA time zone database
            <https://www.iana.org/time-zones>`_).
        :type timezone: str
        :param recurrence: Meeting series recurrence rule (conforming with `RFC 2445
            <https://www.ietf.org/rfc/rfc2445.txt>`_). Applies only to a recurring
            meeting series, not to a meeting series with only one scheduled meeting. Multiple days or dates for
            monthly or yearly `recurrence` rule are not supported, only the first day or date specified is taken. For
            example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially
            supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10". It can be specified `null` so that the
            meeting becomes non-recurring and the `recurrence` attribute becomes null and hidden from the response
            after the patch.
        :type recurrence: str
        :param enabled_auto_record_meeting: Whether or not meeting is recorded automatically.
        :type enabled_auto_record_meeting: bool
        :param allow_any_user_to_be_co_host: Whether or not to allow any attendee with a host account on the target
            site to become a cohost when joining the meeting. The target site is specified by `siteUrl` parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_any_user_to_be_co_host: bool
        :param enabled_join_before_host: Whether or not to allow any attendee to join the meeting before the host joins
            the meeting.
        :type enabled_join_before_host: bool
        :param enable_connect_audio_before_host: Whether or not to allow any attendee to connect audio in the meeting
            before the host joins the meeting. This attribute is only applicable if the `enabledJoinBeforeHost`
            attribute is set to true.
        :type enable_connect_audio_before_host: bool
        :param join_before_host_minutes: Number of minutes an attendee can join the meeting before the meeting start
            time and the host joins. Only applicable if the `enabledJoinBeforeHost` attribute is set to true. Valid
            options for a meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`,
            `45`, and `60`. The default is `0` if not specified.
        :type join_before_host_minutes: int
        :param exclude_password: Whether or not to exclude the meeting password from the email invitation.
        :type exclude_password: bool
        :param public_meeting: Whether or not to allow the meeting to be listed on the public calendar.
        :type public_meeting: bool
        :param reminder_time: The number of minutes before the meeting begins, that an email reminder is sent to the
            host.
        :type reminder_time: int
        :param unlocked_meeting_join_security: Specifies how the people who aren't on the invite can join the unlocked
            meeting.
        :type unlocked_meeting_join_security: MeetingSeriesObjectUnlockedMeetingJoinSecurity
        :param session_type_id: Unique identifier for a meeting session type for the user. This attribute is required
            while scheduling webinar meeting. All available meeting session types enabled for the user can be
            retrieved by `List Meeting Session Types
            <https://developer.webex.com/docs/api/v1/meetings/list-meeting-session-types>`_ API.
        :type session_type_id: int
        :param enabled_webcast_view: Whether or not webcast view is enabled.
        :type enabled_webcast_view: bool
        :param panelist_password: Password for panelists of a webinar meeting. Must conform to the site's password
            complexity settings. Read `password management
            <https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration>`_ for details. If not specified, a random password conforming
            to the site's password rules will be generated automatically.
        :type panelist_password: str
        :param enable_automatic_lock: Whether or not to automatically lock the meeting after it starts.
        :type enable_automatic_lock: bool
        :param automatic_lock_minutes: The number of minutes after the meeting begins, for automatically locking it.
        :type automatic_lock_minutes: int
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee of the meeting with a host
            account on the target site to become a cohost. The target site is specified by `siteUrl` parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_first_user_to_be_co_host: bool
        :param allow_authenticated_devices: Whether or not to allow authenticated video devices in the meeting's
            organization to start or join the meeting without a prompt.
        :type allow_authenticated_devices: bool
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin-level scopes. When used, the admin may specify the email of a
            user in a site they manage to be the meeting host. The field is not editable and is only used to patch a
            meeting on behalf of the real meeting host. Please use the `Reassign Meetings to a New Host
            <https://developer.webex.com/docs/api/v1/meetings/reassign-meetings-to-a-new-host>`_ API if you need
            to update the meeting host.
        :type host_email: str
        :param site_url: URL of the Webex site which the meeting is updated on. If not specified, the meeting is
            created on user's preferred site. All available Webex sites and preferred site of the user can be
            retrieved by `Get Site List` API.
        :type site_url: str
        :param meeting_options: Meeting Options.
        :type meeting_options: MeetingSeriesObjectMeetingOptions
        :param attendee_privileges: Attendee Privileges. This attribute is not supported for a webinar.
        :type attendee_privileges: MeetingSeriesObjectAttendeePrivileges
        :param integration_tags: External keys created by an integration application in its own domain, for example
            Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries
            meetings by a key in its own domain. The maximum size of `integrationTags` is 3 and each item of
            `integrationTags` can be a maximum of 64 characters long. Please note that an empty or null
            `integrationTags` will delete all existing integration tags for the meeting implicitly. Developer can
            update integration tags for a `meetingSeries` but he cannot update it for a `scheduledMeeting` or a
            `meeting` instance.
        :type integration_tags: list[str]
        :param enabled_breakout_sessions: Whether or not breakout sessions are enabled. If the value of
            `enabledBreakoutSessions` is false, users can not set breakout sessions. If the value of
            `enabledBreakoutSessions` is true, users can update breakout sessions using the `Update Breakout Sessions
            <https://developer.webex.com/docs/api/v1/meetings/{meetingId}/breakoutSessions>`_
            API. Updating breakout sessions are not supported by this API.
        :type enabled_breakout_sessions: bool
        :param tracking_codes: Tracking codes information. All available tracking codes and their options for the
            specified site can be retrieved by `List Meeting Tracking Codes
            <https://developer.webex.com/docs/api/v1/meetings/list-meeting-tracking-codes>`_ API. If an optional tracking code is
            missing from the `trackingCodes` array and there's a default option for this tracking code, the default
            option is assigned automatically. If the `inputMode` of a tracking code is `select`, its value must be one
            of the site-level options or the user-level value. Tracking code is not supported for a personal room
            meeting or an ad-hoc space meeting. It can be specified `null` so that it becomes null and hidden from the
            response after the patch.
        :type tracking_codes: list[TrackingCodeItemForCreateMeetingObject]
        :param audio_connection_options: Audio connection options.
        :type audio_connection_options: MeetingSeriesObjectAudioConnectionOptions
        :param require_attendee_login: Require attendees to sign in before joining the webinar. This option works when
            the value of `scheduledType` attribute is `webinar`. Please note that `requireAttendeeLogin` cannot be set
            if someone has already registered for the webinar.
        :type require_attendee_login: bool
        :param restrict_to_invitees: Restrict webinar to invited attendees only. This option works when the
            registration option is disabled and the value of `scheduledType` attribute is `webinar`. Please note that
            `restrictToInvitees` cannot be set to `true` if `requireAttendeeLogin` is `false`.
        :type restrict_to_invitees: bool
        :rtype: :class:`MeetingSeriesObject`
        """
        body = dict()
        if title is not None:
            body['title'] = title
        if agenda is not None:
            body['agenda'] = agenda
        if password is not None:
            body['password'] = password
        if start is not None:
            body['start'] = start
        if end is not None:
            body['end'] = end
        if timezone is not None:
            body['timezone'] = timezone
        if recurrence is not None:
            body['recurrence'] = recurrence
        if enabled_auto_record_meeting is not None:
            body['enabledAutoRecordMeeting'] = enabled_auto_record_meeting
        if allow_any_user_to_be_co_host is not None:
            body['allowAnyUserToBeCoHost'] = allow_any_user_to_be_co_host
        if enabled_join_before_host is not None:
            body['enabledJoinBeforeHost'] = enabled_join_before_host
        if enable_connect_audio_before_host is not None:
            body['enableConnectAudioBeforeHost'] = enable_connect_audio_before_host
        if join_before_host_minutes is not None:
            body['joinBeforeHostMinutes'] = join_before_host_minutes
        if exclude_password is not None:
            body['excludePassword'] = exclude_password
        if public_meeting is not None:
            body['publicMeeting'] = public_meeting
        if reminder_time is not None:
            body['reminderTime'] = reminder_time
        if unlocked_meeting_join_security is not None:
            body['unlockedMeetingJoinSecurity'] = enum_str(unlocked_meeting_join_security)
        if session_type_id is not None:
            body['sessionTypeId'] = session_type_id
        if enabled_webcast_view is not None:
            body['enabledWebcastView'] = enabled_webcast_view
        if panelist_password is not None:
            body['panelistPassword'] = panelist_password
        if enable_automatic_lock is not None:
            body['enableAutomaticLock'] = enable_automatic_lock
        if automatic_lock_minutes is not None:
            body['automaticLockMinutes'] = automatic_lock_minutes
        if allow_first_user_to_be_co_host is not None:
            body['allowFirstUserToBeCoHost'] = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body['allowAuthenticatedDevices'] = allow_authenticated_devices
        if send_email is not None:
            body['sendEmail'] = send_email
        if host_email is not None:
            body['hostEmail'] = host_email
        if site_url is not None:
            body['siteUrl'] = site_url
        if meeting_options is not None:
            body['meetingOptions'] = loads(meeting_options.model_dump_json())
        if attendee_privileges is not None:
            body['attendeePrivileges'] = loads(attendee_privileges.model_dump_json())
        if integration_tags is not None:
            body['integrationTags'] = integration_tags
        if enabled_breakout_sessions is not None:
            body['enabledBreakoutSessions'] = enabled_breakout_sessions
        if tracking_codes is not None:
            body['trackingCodes'] = loads(TypeAdapter(list[TrackingCodeItemForCreateMeetingObject]).dump_json(tracking_codes, by_alias=True, exclude_none=True))
        if audio_connection_options is not None:
            body['audioConnectionOptions'] = loads(audio_connection_options.model_dump_json())
        if require_attendee_login is not None:
            body['requireAttendeeLogin'] = require_attendee_login
        if restrict_to_invitees is not None:
            body['restrictToInvitees'] = restrict_to_invitees
        url = self.ep(f'{meeting_id}')
        data = super().patch(url, json=body)
        r = MeetingSeriesObject.model_validate(data)
        return r

    def update_a_meeting(self, meeting_id: str, title: str = None, agenda: str = None, password: str = None,
                         start: Union[str, datetime] = None, end: Union[str, datetime] = None, timezone: str = None,
                         recurrence: str = None, enabled_auto_record_meeting: bool = None,
                         allow_any_user_to_be_co_host: bool = None, enabled_join_before_host: bool = None,
                         enable_connect_audio_before_host: bool = None, join_before_host_minutes: int = None,
                         exclude_password: bool = None, public_meeting: bool = None, reminder_time: int = None,
                         unlocked_meeting_join_security: MeetingSeriesObjectUnlockedMeetingJoinSecurity = None,
                         session_type_id: int = None, enabled_webcast_view: bool = None,
                         panelist_password: str = None, enable_automatic_lock: bool = None,
                         automatic_lock_minutes: int = None, allow_first_user_to_be_co_host: bool = None,
                         allow_authenticated_devices: bool = None, send_email: bool = None, host_email: str = None,
                         site_url: str = None, meeting_options: MeetingSeriesObjectMeetingOptions = None,
                         attendee_privileges: MeetingSeriesObjectAttendeePrivileges = None,
                         integration_tags: list[str] = None, enabled_breakout_sessions: bool = None,
                         tracking_codes: list[TrackingCodeItemForCreateMeetingObject] = None,
                         audio_connection_options: MeetingSeriesObjectAudioConnectionOptions = None,
                         require_attendee_login: bool = None,
                         restrict_to_invitees: bool = None) -> MeetingSeriesObject:
        """
        Update a Meeting

        <div>
        <Callout type="warning">The PUT method is still supported and behaves the same as before, will be deprecated in
        the future. Use the PATCH method instead.</Callout>
        </div>

        Updates details for a meeting with a specified meeting ID. This operation applies to meeting series and
        scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Ad-hoc meetings created by
        `Create a Meeting
        <https://developer.webex.com/docs/api/v1/meetings/create-a-meeting>`_ with `adhoc` of `true` and a `roomId` cannot be updated.

        * If the `meetingId` value specified is for a scheduled meeting, the operation updates that scheduled meeting
        without impact on other scheduled meeting of the parent meeting series.

        * If the `meetingId` value specified is for a meeting series, the operation updates the entire meeting series.
        **Note**: If the value of `start`, `end`, or `recurrence` for the meeting series is changed, any exceptional
        scheduled meeting in this series is cancelled when the meeting series is updated.

        :param meeting_id: Unique identifier for the meeting to be updated. This parameter applies to meeting series
            and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Please note that
            currently meeting ID of a scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is not supported for this API.
        :type meeting_id: str
        :param title: Meeting title. The title can be a maximum of 128 characters long.
        :type title: str
        :param agenda: Meeting agenda. The agenda can be a maximum of 1300 characters long.
        :type agenda: str
        :param password: Meeting password. Must conform to the site's password complexity settings. Read
            `password management
            <https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration>`_ for details.
        :type password: str
        :param start: Date and time for the start of meeting in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `start` cannot be before
            current date and time or after `end`. Duration between `start` and `end` cannot be shorter than 10 minutes
            or longer than 23 hours 59 minutes. Refer to the `Webex Meetings
            <https://developer.webex.com/docs/meetings#restrictions-on-updating-a-meeting>`_ guide for more information about
            restrictions on updating date and time for a meeting. Please note that when a meeting is being updated,
            `start` of the meeting will be accurate to minutes, not seconds or milliseconds. Therefore, if `start` is
            within the same minute as the current time, `start` will be adjusted to the upcoming minute; otherwise,
            `start` will be adjusted with seconds and milliseconds stripped off. For instance, if the current time is
            `2022-03-01T10:32:16.657+08:00`, `start` of `2022-03-01T10:32:28.076+08:00` or `2022-03-01T10:32:41+08:00`
            will be adjusted to `2022-03-01T10:33:00+08:00`, and `start` of `2022-03-01T11:32:28.076+08:00` or
            `2022-03-01T11:32:41+08:00` will be adjusted to `2022-03-01T11:32:00+08:00`.
        :type start: Union[str, datetime]
        :param end: Date and time for the end of meeting in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. `end` cannot be before
            current date and time or before `start`. Duration between `start` and `end` cannot be shorter than 10
            minutes or longer than 23 hours 59 minutes. Refer to the `Webex Meetings
            <https://developer.webex.com/docs/meetings#restrictions-on-updating-a-meeting>`_ guide for more information about
            restrictions on updating date and time for a meeting. Please note that when a meeting is being updated,
            `end` of the meeting will be accurate to minutes, not seconds or milliseconds. Therefore, `end` will be
            adjusted with seconds and milliseconds stripped off. For instance, `end` of
            `2022-03-01T11:52:28.076+08:00` or `2022-03-01T11:52:41+08:00` will be adjusted to
            `2022-03-01T11:52:00+08:00`.
        :type end: Union[str, datetime]
        :param timezone: `Time zone
            <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ in which the meeting was originally scheduled (conforming with the
            `IANA time zone database
            <https://www.iana.org/time-zones>`_).
        :type timezone: str
        :param recurrence: Meeting series recurrence rule (conforming with `RFC 2445
            <https://www.ietf.org/rfc/rfc2445.txt>`_). Applies only to a recurring
            meeting series, not to a meeting series with only one scheduled meeting. Multiple days or dates for
            monthly or yearly `recurrence` rule are not supported, only the first day or date specified is taken. For
            example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially
            supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
        :type recurrence: str
        :param enabled_auto_record_meeting: Whether or not meeting is recorded automatically.
        :type enabled_auto_record_meeting: bool
        :param allow_any_user_to_be_co_host: Whether or not to allow any attendee with a host account on the target
            site to become a cohost when joining the meeting. The target site is specified by `siteUrl` parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_any_user_to_be_co_host: bool
        :param enabled_join_before_host: Whether or not to allow any attendee to join the meeting before the host joins
            the meeting.
        :type enabled_join_before_host: bool
        :param enable_connect_audio_before_host: Whether or not to allow any attendee to connect audio in the meeting
            before the host joins the meeting. This attribute is only applicable if the `enabledJoinBeforeHost`
            attribute is set to true.
        :type enable_connect_audio_before_host: bool
        :param join_before_host_minutes: Number of minutes an attendee can join the meeting before the meeting start
            time and the host joins. Only applicable if the `enabledJoinBeforeHost` attribute is set to true. Valid
            options for a meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`,
            `45`, and `60`. The default is `0` if not specified.
        :type join_before_host_minutes: int
        :param exclude_password: Whether or not to exclude the meeting password from the email invitation.
        :type exclude_password: bool
        :param public_meeting: Whether or not to allow the meeting to be listed on the public calendar.
        :type public_meeting: bool
        :param reminder_time: The number of minutes before the meeting begins, that an email reminder is sent to the
            host.
        :type reminder_time: int
        :param unlocked_meeting_join_security: Specifies how the people who aren't on the invite can join the unlocked
            meeting.
        :type unlocked_meeting_join_security: MeetingSeriesObjectUnlockedMeetingJoinSecurity
        :param session_type_id: Unique identifier for a meeting session type for the user. This attribute is required
            while scheduling webinar meeting. All available meeting session types enabled for the user can be
            retrieved by `List Meeting Session Types
            <https://developer.webex.com/docs/api/v1/meetings/list-meeting-session-types>`_ API.
        :type session_type_id: int
        :param enabled_webcast_view: Whether or not webcast view is enabled.
        :type enabled_webcast_view: bool
        :param panelist_password: Password for panelists of a webinar meeting. Must conform to the site's password
            complexity settings. Read `password management
            <https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration>`_ for details. If not specified, a random password conforming
            to the site's password rules will be generated automatically.
        :type panelist_password: str
        :param enable_automatic_lock: Whether or not to automatically lock the meeting after it starts.
        :type enable_automatic_lock: bool
        :param automatic_lock_minutes: The number of minutes after the meeting begins, for automatically locking it.
        :type automatic_lock_minutes: int
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee of the meeting with a host
            account on the target site to become a cohost. The target site is specified by `siteUrl` parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_first_user_to_be_co_host: bool
        :param allow_authenticated_devices: Whether or not to allow authenticated video devices in the meeting's
            organization to start or join the meeting without a prompt.
        :type allow_authenticated_devices: bool
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin-level scopes. When used, the admin may specify the email of a
            user in a site they manage to be the meeting host. The field is not editable and is only used to update a
            meeting on behalf of the real meeting host. Please use the `Reassign Meetings to a New Host
            <https://developer.webex.com/docs/api/v1/meetings/reassign-meetings-to-a-new-host>`_ API if you need
            to update the meeting host.
        :type host_email: str
        :param site_url: URL of the Webex site which the meeting is updated on. If not specified, the meeting is
            created on user's preferred site. All available Webex sites and preferred site of the user can be
            retrieved by `Get Site List` API.
        :type site_url: str
        :param meeting_options: Meeting Options.
        :type meeting_options: MeetingSeriesObjectMeetingOptions
        :param attendee_privileges: Attendee Privileges. This attribute is not supported for a webinar.
        :type attendee_privileges: MeetingSeriesObjectAttendeePrivileges
        :param integration_tags: External keys created by an integration application in its own domain, for example
            Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries
            meetings by a key in its own domain. The maximum size of `integrationTags` is 3 and each item of
            `integrationTags` can be a maximum of 64 characters long. Please note that an empty or null
            `integrationTags` will delete all existing integration tags for the meeting implicitly. Developer can
            update integration tags for a `meetingSeries` but he cannot update it for a `scheduledMeeting` or a
            `meeting` instance.
        :type integration_tags: list[str]
        :param enabled_breakout_sessions: Whether or not breakout sessions are enabled. If the value of
            `enabledBreakoutSessions` is false, users can not set breakout sessions. If the value of
            `enabledBreakoutSessions` is true, users can update breakout sessions using the `Update Breakout Sessions
            <https://developer.webex.com/docs/api/v1/meetings/{meetingId}/breakoutSessions>`_
            API. Updating breakout sessions are not supported by this API.
        :type enabled_breakout_sessions: bool
        :param tracking_codes: Tracking codes information. All available tracking codes and their options for the
            specified site can be retrieved by `List Meeting Tracking Codes
            <https://developer.webex.com/docs/api/v1/meetings/list-meeting-tracking-codes>`_ API. If an optional tracking code is
            missing from the `trackingCodes` array and there's a default option for this tracking code, the default
            option is assigned automatically. If the `inputMode` of a tracking code is `select`, its value must be one
            of the site-level options or the user-level value. Tracking code is not supported for a personal room
            meeting or an ad-hoc space meeting.
        :type tracking_codes: list[TrackingCodeItemForCreateMeetingObject]
        :param audio_connection_options: Audio connection options.
        :type audio_connection_options: MeetingSeriesObjectAudioConnectionOptions
        :param require_attendee_login: Require attendees to sign in before joining the webinar. This option works when
            the value of `scheduledType` attribute is `webinar`. Please note that `requireAttendeeLogin` cannot be set
            if someone has already registered for the webinar.
        :type require_attendee_login: bool
        :param restrict_to_invitees: Restrict webinar to invited attendees only. This option works when the
            registration option is disabled and the value of `scheduledType` attribute is `webinar`. Please note that
            `restrictToInvitees` cannot be set to `true` if `requireAttendeeLogin` is `false`.
        :type restrict_to_invitees: bool
        :rtype: :class:`MeetingSeriesObject`
        """
        body = dict()
        if title is not None:
            body['title'] = title
        if agenda is not None:
            body['agenda'] = agenda
        if password is not None:
            body['password'] = password
        if start is not None:
            body['start'] = start
        if end is not None:
            body['end'] = end
        if timezone is not None:
            body['timezone'] = timezone
        if recurrence is not None:
            body['recurrence'] = recurrence
        if enabled_auto_record_meeting is not None:
            body['enabledAutoRecordMeeting'] = enabled_auto_record_meeting
        if allow_any_user_to_be_co_host is not None:
            body['allowAnyUserToBeCoHost'] = allow_any_user_to_be_co_host
        if enabled_join_before_host is not None:
            body['enabledJoinBeforeHost'] = enabled_join_before_host
        if enable_connect_audio_before_host is not None:
            body['enableConnectAudioBeforeHost'] = enable_connect_audio_before_host
        if join_before_host_minutes is not None:
            body['joinBeforeHostMinutes'] = join_before_host_minutes
        if exclude_password is not None:
            body['excludePassword'] = exclude_password
        if public_meeting is not None:
            body['publicMeeting'] = public_meeting
        if reminder_time is not None:
            body['reminderTime'] = reminder_time
        if unlocked_meeting_join_security is not None:
            body['unlockedMeetingJoinSecurity'] = enum_str(unlocked_meeting_join_security)
        if session_type_id is not None:
            body['sessionTypeId'] = session_type_id
        if enabled_webcast_view is not None:
            body['enabledWebcastView'] = enabled_webcast_view
        if panelist_password is not None:
            body['panelistPassword'] = panelist_password
        if enable_automatic_lock is not None:
            body['enableAutomaticLock'] = enable_automatic_lock
        if automatic_lock_minutes is not None:
            body['automaticLockMinutes'] = automatic_lock_minutes
        if allow_first_user_to_be_co_host is not None:
            body['allowFirstUserToBeCoHost'] = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body['allowAuthenticatedDevices'] = allow_authenticated_devices
        if send_email is not None:
            body['sendEmail'] = send_email
        if host_email is not None:
            body['hostEmail'] = host_email
        if site_url is not None:
            body['siteUrl'] = site_url
        if meeting_options is not None:
            body['meetingOptions'] = loads(meeting_options.model_dump_json())
        if attendee_privileges is not None:
            body['attendeePrivileges'] = loads(attendee_privileges.model_dump_json())
        if integration_tags is not None:
            body['integrationTags'] = integration_tags
        if enabled_breakout_sessions is not None:
            body['enabledBreakoutSessions'] = enabled_breakout_sessions
        if tracking_codes is not None:
            body['trackingCodes'] = loads(TypeAdapter(list[TrackingCodeItemForCreateMeetingObject]).dump_json(tracking_codes, by_alias=True, exclude_none=True))
        if audio_connection_options is not None:
            body['audioConnectionOptions'] = loads(audio_connection_options.model_dump_json())
        if require_attendee_login is not None:
            body['requireAttendeeLogin'] = require_attendee_login
        if restrict_to_invitees is not None:
            body['restrictToInvitees'] = restrict_to_invitees
        url = self.ep(f'{meeting_id}')
        data = super().put(url, json=body)
        r = MeetingSeriesObject.model_validate(data)
        return r

    def delete_a_meeting(self, meeting_id: str, host_email: str = None, send_email: bool = None):
        """
        Delete a Meeting

        Deletes a meeting with a specified meeting ID. The deleted meeting cannot be recovered. This operation applies
        to meeting series and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Ad-hoc
        meetings created by `Create a Meeting
        <https://developer.webex.com/docs/api/v1/meetings/create-a-meeting>`_ with `adhoc` of `true` and a `roomId` cannot be deleted.

        * If the `meetingId` value specified is for a scheduled meeting, the operation deletes that scheduled meeting
        without impact on other scheduled meeting of the parent meeting series.

        * If the `meetingId` value specified is for a meeting series, the operation deletes the entire meeting series.

        :param meeting_id: Unique identifier for the meeting to be deleted. This parameter applies to meeting series
            and scheduled meetings. It doesn't apply to ended or in-progress meeting instances.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will delete a meeting that is hosted by that user.
        :type host_email: str
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :rtype: None
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if send_email is not None:
            params['sendEmail'] = str(send_email).lower()
        url = self.ep(f'{meeting_id}')
        super().delete(url, params=params)

    def join_a_meeting(self, meeting_id: str = None, meeting_number: str = None, web_link: str = None,
                       join_directly: bool = None, email: str = None, display_name: str = None, password: str = None,
                       expiration_minutes: int = None, registration_id: str = None,
                       host_email: str = None) -> JoinMeetingLinkObject:
        """
        Join a Meeting

        Retrieves links for a meeting with a specified `meetingId`, `meetingNumber`, or `webLink` that allow users to
        start or join the meeting directly without logging in and entering a password.

        * Please note that `meetingId`, `meetingNumber` and `webLink` are mutually exclusive and they cannot be
        specified simultaneously.

        * If `joinDirectly` is true or not specified, the response will have HTTP response code 302 and the request
        will be redirected to `joinLink`; otherwise, the response will have HTTP response code 200 and `joinLink` will
        be returned in response body.

        * Only the meeting host or cohost can generate the `startLink`.

        * An admin user or a `Service App
        <https://developer.webex.com/docs/service-apps>`_ can generate the `startLink` and `joinLink` on behalf of another meeting host
        using the `hostEmail` parameter. When a `Service App
        <https://developer.webex.com/docs/service-apps>`_ generates the `startLink` and `joinLink`, the `hostEmail`
        parameter is required. The `hostEmail` parameter only applies to meetings, not webinars.

        * For Service Apps, `hostEmail` must be provided in the request.

        * Generating a join link or a start link before the time specified by `joinBeforeHostMinutes` for a webinar is
        not supported.

        :param meeting_id: Unique identifier for the meeting. This parameter applies to meeting series and scheduled
            meetings. It doesn't apply to ended or in-progress meeting instances. Please note that currently meeting
            ID of a scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is also supported for this API.
        :type meeting_id: str
        :param meeting_number: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but
            not to meeting instances which have ended.
        :type meeting_number: str
        :param web_link: Link to a meeting information page where the meeting client is launched if the meeting is
            ready to start or join.
        :type web_link: str
        :param join_directly: Whether or not to redirect to `joinLink`. It is an optional field and default value is
            true.
        :type join_directly: bool
        :param email: Email address of meeting participant. If `email` is specified, the link is generated for the user
            of `email`; otherwise, the API returns the link for the user calling the API. `email` is required for a
            `guest issuer
            <https://developer.webex.com/docs/guest-issuer>`_.
        :type email: str
        :param display_name: Display name of meeting participant. If `displayName` is specified, `email` must be
            specified as well. If `email` is specified and `displayName` is not, display name is the same as `email`.
            If neither `displayName` nor `email` is specified, the API returns the link for the user calling the API.
            The maximum length of `displayName` is 128 characters. `displayName` is required for a `guest issuer
            <https://developer.webex.com/docs/guest-issuer>`_.
        :type display_name: str
        :param password: Required when the meeting is protected by a password and the current user is not privileged to
            view it if they are not a host, cohost, or invitee.
        :type password: str
        :param expiration_minutes: Expiration duration of `joinLink` in minutes. Must be between 1 and 60.
        :type expiration_minutes: int
        :param registration_id: Required when the meeting is webinar-enabled and enabled registration ID.
        :type registration_id: str
        :param host_email: Email address for the meeting host. This attribute should be set if the user or application
            calling the API has the admin on-behalf-of scopes. This parameter is required for a `Service App
            <https://developer.webex.com/docs/service-apps>`_. It only
            applies to meetings, not webinars.
        :type host_email: str
        :rtype: :class:`JoinMeetingLinkObject`
        """
        body = dict()
        if meeting_id is not None:
            body['meetingId'] = meeting_id
        if meeting_number is not None:
            body['meetingNumber'] = meeting_number
        if web_link is not None:
            body['webLink'] = web_link
        if join_directly is not None:
            body['joinDirectly'] = join_directly
        if email is not None:
            body['email'] = email
        if display_name is not None:
            body['displayName'] = display_name
        if password is not None:
            body['password'] = password
        if expiration_minutes is not None:
            body['expirationMinutes'] = expiration_minutes
        if registration_id is not None:
            body['registrationId'] = registration_id
        if host_email is not None:
            body['hostEmail'] = host_email
        url = self.ep('join')
        data = super().post(url, json=body)
        r = JoinMeetingLinkObject.model_validate(data)
        return r

    def list_meeting_templates(self, template_type: TemplateObjectTemplateType = None, locale: str = None,
                               is_default: bool = None, is_standard: bool = None, host_email: str = None,
                               site_url: str = None) -> list[TemplateObject]:
        """
        List Meeting Templates

        Retrieves the list of meeting templates that is available for the authenticated user.

        There are separate lists of meeting templates for different `templateType`, `locale` and `siteUrl`.

        * If `templateType` is specified, the operation returns an array of meeting template objects specified by the
        `templateType`; otherwise, returns an array of meeting template objects of all template types.

        * If `locale` is specified, the operation returns an array of meeting template objects specified by the
        `locale`; otherwise, returns an array of meeting template objects of the default `en_US` locale. Refer to
        `Meeting Template Locales
        <https://developer.webex.com/docs/meetings#meeting-template-locales>`_ for all the locales supported by Webex.

        * If the parameter `siteUrl` has a value, the operation lists meeting templates on the specified site;
        otherwise, lists meeting templates on the user's preferred site. All available Webex sites and preferred site
        of the user can be retrieved by `Get Site List` API.

        :param template_type: Meeting template type for the meeting template objects being requested. If not specified,
            return meeting templates of all types.
        :type template_type: TemplateObjectTemplateType
        :param locale: Locale for the meeting template objects being requested. If not specified, return meeting
            templates of the default `en_US` locale. Refer to `Meeting Template Locales
            <https://developer.webex.com/docs/meetings#meeting-template-locales>`_ for all the locales supported
            by Webex.
        :type locale: str
        :param is_default: The value is `true` or `false`. If it's `true`, return the default meeting templates; if
            it's `false`, return the non-default meeting templates. If it's not specified, return both default and
            non-default meeting templates.
        :type is_default: bool
        :param is_standard: The value is `true` or `false`. If it's `true`, return the standard meeting templates; if
            it's `false`, return the non-standard meeting templates. If it's not specified, return both standard and
            non-standard meeting templates.
        :type is_standard: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return meeting templates that are available for that user.
        :type host_email: str
        :param site_url: URL of the Webex site which the API lists meeting templates from. If not specified, the API
            lists meeting templates from user's preferred site. All available Webex sites and preferred site of the
            user can be retrieved by `Get Site List` API.
        :type site_url: str
        :rtype: list[TemplateObject]
        """
        params = {}
        if template_type is not None:
            params['templateType'] = template_type
        if locale is not None:
            params['locale'] = locale
        if is_default is not None:
            params['isDefault'] = str(is_default).lower()
        if is_standard is not None:
            params['isStandard'] = str(is_standard).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('templates')
        data = super().get(url, params=params)
        r = TypeAdapter(list[TemplateObject]).validate_python(data['items'])
        return r

    def get_a_meeting_template(self, template_id: str, host_email: str = None) -> DetailedTemplateObject:
        """
        Get a Meeting Template

        Retrieves details for a meeting template with a specified meeting template ID.

        #### Request Header

        * `timezone`: `Time zone
        <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_ for time stamps in response body, defined in conformance with the
        `IANA time zone database
        <https://www.iana.org/time-zones>`_. The default value is `UTC` if not specified.

        :param template_id: Unique identifier for the meeting template being requested.
        :type template_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return the meeting template that is available for that user.
        :type host_email: str
        :rtype: :class:`DetailedTemplateObject`
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'templates/{template_id}')
        data = super().get(url, params=params)
        r = DetailedTemplateObject.model_validate(data)
        return r

    def get_meeting_control_status(self, meeting_id: str) -> Control:
        """
        Get Meeting Control Status

        Get the meeting control of a live meeting, which is consisted of meeting control status on "locked" and
        "recording" to reflect whether the meeting is currently locked and there is recording in progress.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled
            `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting.
        :type meeting_id: str
        :rtype: :class:`Control`
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep('controls')
        data = super().get(url, params=params)
        r = Control.model_validate(data)
        return r

    def update_meeting_control_status(self, meeting_id: str, recording_started: str = None,
                                      recording_paused: str = None, locked: str = None) -> Control:
        """
        Update Meeting Control Status

        To start, pause, resume, or stop a meeting recording; To lock or unlock an on-going meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled
            `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting.
        :type meeting_id: str
        :param recording_started: The value can be true or false. true means to start the recording, false to end the
            recording.
        :type recording_started: str
        :param recording_paused: The value can be true or false, will be ignored if 'recordingStarted' sets to false,
            and true to resume the recording only if the recording is paused vise versa.
        :type recording_paused: str
        :param locked: The value is true or false.
        :type locked: str
        :rtype: :class:`Control`
        """
        params = {}
        params['meetingId'] = meeting_id
        body = dict()
        if recording_started is not None:
            body['recordingStarted'] = recording_started
        if recording_paused is not None:
            body['recordingPaused'] = recording_paused
        if locked is not None:
            body['locked'] = locked
        url = self.ep('controls')
        data = super().put(url, params=params, json=body)
        r = Control.model_validate(data)
        return r

    def list_meeting_session_types(self, host_email: str = None,
                                   site_url: str = None) -> list[MeetingSessionTypeObject]:
        """
        List Meeting Session Types

        List all the meeting session types enabled for a given user.

        :param host_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they
            manage and the API will list all the meeting session types enabled for the user.
        :type host_email: str
        :param site_url: Webex site URL to query. If `siteUrl` is not specified, the users' preferred site will be
            used. If the authorization token has the admin-level scopes, the admin can set the Webex site URL on
            behalf of the user specified in the `hostEmail` parameter.
        :type site_url: str
        :rtype: list[MeetingSessionTypeObject]
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('sessionTypes')
        data = super().get(url, params=params)
        r = TypeAdapter(list[MeetingSessionTypeObject]).validate_python(data['items'])
        return r

    def get_a_meeting_session_type(self, session_type_id: int, host_email: str = None,
                                   site_url: str = None) -> MeetingSessionTypeObject:
        """
        Get a Meeting Session Type

        Retrieves details for a meeting session type with a specified session type ID.

        :param session_type_id: A unique identifier for the sessionType.
        :type session_type_id: int
        :param host_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they
            manage and the API will get a meeting session type with the specified session type ID enabled for the
            user.
        :type host_email: str
        :param site_url: Webex site URL to query. If `siteUrl` is not specified, the users' preferred site will be
            used. If the authorization token has the admin-level scopes, the admin can set the Webex site URL on
            behalf of the user specified in the `hostEmail` parameter.
        :type site_url: str
        :rtype: :class:`MeetingSessionTypeObject`
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep(f'sessionTypes/{session_type_id}')
        data = super().get(url, params=params)
        r = MeetingSessionTypeObject.model_validate(data)
        return r

    def get_registration_form_for_a_meeting(self, meeting_id: str, current: bool = None,
                                            host_email: str = None) -> Registration:
        """
        Get registration form for a meeting

        Get a meeting's registration form to understand which fields are required.

        :param meeting_id: Unique identifier for the meeting. Only the ID of the meeting series is supported for
            meetingId. IDs of scheduled meetings, meeting instances, or scheduled personal room meetings are not
            supported. See the `Meetings Overview
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for more information about meeting types.
        :type meeting_id: str
        :param current: Whether or not to retrieve only the current scheduled meeting of the meeting series, i.e. the
            meeting ready to join or start or the upcoming meeting of the meeting series. If it's `true`, return
            details for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start
            or the upcoming scheduled meeting of the meeting series. If it's `false` or not specified, return details
            for the entire meeting series. This parameter only applies to meeting series.
        :type current: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :rtype: :class:`Registration`
        """
        params = {}
        if current is not None:
            params['current'] = str(current).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}/registration')
        data = super().get(url, params=params)
        r = Registration.model_validate(data)
        return r

    def update_meeting_registration_form(self, meeting_id: str, host_email: str = None,
                                         auto_accept_request: bool = None, require_first_name: bool = None,
                                         require_last_name: bool = None, require_email: bool = None,
                                         require_job_title: bool = None, require_company_name: bool = None,
                                         require_address1: bool = None, require_address2: bool = None,
                                         require_city: bool = None, require_state: bool = None,
                                         require_zip_code: bool = None, require_country_region: bool = None,
                                         require_work_phone: bool = None, require_fax: bool = None,
                                         max_register_num: int = None,
                                         customized_questions: list[CustomizedQuestionForCreateMeeting] = None,
                                         rules: list[StandardRegistrationApproveRule] = None) -> Registration:
        """
        Update Meeting Registration Form

        Enable or update a registration form for a meeting.

        :param meeting_id: Unique identifier for the meeting. Only the ID of the meeting series is supported for
            meetingId. IDs of scheduled meetings, meeting instances, or scheduled personal room meetings are not
            supported. See the `Meetings Overview
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for more information about meeting types.
        :type meeting_id: str
        :param host_email: - Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return an update for a meeting that is hosted by that user.
        :type host_email: str
        :param auto_accept_request: Whether or not meeting registration requests are accepted automatically.
        :type auto_accept_request: bool
        :param require_first_name: Whether or not a registrant's first name is required for meeting registration. This
            option must always be `true`.
        :type require_first_name: bool
        :param require_last_name: Whether or not a registrant's last name is required for meeting registration. This
            option must always be `true`.
        :type require_last_name: bool
        :param require_email: Whether or not a registrant's email is required for meeting registration. This option
            must always be `true`.
        :type require_email: bool
        :param require_job_title: Whether or not a registrant's job title is shown or required for meeting
            registration.
        :type require_job_title: bool
        :param require_company_name: Whether or not a registrant's company name is shown or required for meeting
            registration.
        :type require_company_name: bool
        :param require_address1: Whether or not a registrant's first address field is shown or required for meeting
            registration.
        :type require_address1: bool
        :param require_address2: Whether or not a registrant's second address field is shown or required for meeting
            registration.
        :type require_address2: bool
        :param require_city: Whether or not a registrant's city is shown or required for meeting registration.
        :type require_city: bool
        :param require_state: Whether or not a registrant's state is shown or required for meeting registration.
        :type require_state: bool
        :param require_zip_code: Whether or not a registrant's postal code is shown or required for meeting
            registration.
        :type require_zip_code: bool
        :param require_country_region: Whether or not a registrant's country or region is shown or required for meeting
            registration.
        :type require_country_region: bool
        :param require_work_phone: Whether or not a registrant's work phone number is shown or required for meeting
            registration.
        :type require_work_phone: bool
        :param require_fax: Whether or not a registrant's fax number is shown or required for meeting registration.
        :type require_fax: bool
        :param max_register_num: Maximum number of meeting registrations. This only applies to meetings. The maximum
            number of participants for meetings and webinars, with the limit based on the user capacity and controlled
            by a toggle at the site level. The default maximum number of participants for webinars is 10000, but the
            actual maximum number of participants is limited by the user capacity.
        :type max_register_num: int
        :param customized_questions: Customized questions for meeting registration.
        :type customized_questions: list[CustomizedQuestionForCreateMeeting]
        :param rules: The approval rule for standard questions.
        :type rules: list[StandardRegistrationApproveRule]
        :rtype: :class:`Registration`
        """
        body = dict()
        if host_email is not None:
            body['hostEmail'] = host_email
        if auto_accept_request is not None:
            body['autoAcceptRequest'] = auto_accept_request
        if require_first_name is not None:
            body['requireFirstName'] = require_first_name
        if require_last_name is not None:
            body['requireLastName'] = require_last_name
        if require_email is not None:
            body['requireEmail'] = require_email
        if require_job_title is not None:
            body['requireJobTitle'] = require_job_title
        if require_company_name is not None:
            body['requireCompanyName'] = require_company_name
        if require_address1 is not None:
            body['requireAddress1'] = require_address1
        if require_address2 is not None:
            body['requireAddress2'] = require_address2
        if require_city is not None:
            body['requireCity'] = require_city
        if require_state is not None:
            body['requireState'] = require_state
        if require_zip_code is not None:
            body['requireZipCode'] = require_zip_code
        if require_country_region is not None:
            body['requireCountryRegion'] = require_country_region
        if require_work_phone is not None:
            body['requireWorkPhone'] = require_work_phone
        if require_fax is not None:
            body['requireFax'] = require_fax
        if max_register_num is not None:
            body['maxRegisterNum'] = max_register_num
        if customized_questions is not None:
            body['customizedQuestions'] = loads(TypeAdapter(list[CustomizedQuestionForCreateMeeting]).dump_json(customized_questions, by_alias=True, exclude_none=True))
        if rules is not None:
            body['rules'] = loads(TypeAdapter(list[StandardRegistrationApproveRule]).dump_json(rules, by_alias=True, exclude_none=True))
        url = self.ep(f'{meeting_id}/registration')
        data = super().put(url, json=body)
        r = Registration.model_validate(data)
        return r

    def delete_meeting_registration_form(self, meeting_id: str):
        """
        Delete Meeting Registration Form

        Disable the registration form for a meeting.

        :param meeting_id: Unique identifier for the meeting. Only the ID of the meeting series is supported for
            meetingId. IDs of scheduled meetings, meeting instances, or scheduled personal room meetings are not
            supported. See the `Meetings Overview
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for more information about meeting types.
        :type meeting_id: str
        :rtype: None
        """
        url = self.ep(f'{meeting_id}/registration')
        super().delete(url)

    def register_a_meeting_registrant(self, meeting_id: str, first_name: str, last_name: str, email: str,
                                      current: bool = None, host_email: str = None, send_email: bool = None,
                                      job_title: str = None, company_name: str = None, address1: str = None,
                                      address2: str = None, city: str = None, state: str = None, zip_code: int = None,
                                      country_region: str = None, work_phone: str = None, fax: str = None,
                                      customized_questions: list[CustomizedRegistrant] = None) -> RegistrantCreateResponse:
        """
        Register a Meeting Registrant

        Register a new registrant for a meeting. When a meeting or webinar is created, this API can only be used if
        Registration is checked on the page or the registration attribute is specified through the `Create a Meeting
        <https://developer.webex.com/docs/api/v1/meetings/create-a-meeting>`_
        API.

        :param meeting_id: Unique identifier for the meeting. Only the ID of the meeting series is supported for
            meetingId. IDs of scheduled meetings, meeting instances, or scheduled personal room meetings are not
            supported. See the `Meetings Overview
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for more information about meeting types.
        :type meeting_id: str
        :param first_name: The registrant's first name.
        :type first_name: str
        :param last_name: The registrant's last name. (Required)
        :type last_name: str
        :param email: The registrant's email.
        :type email: str
        :param current: Whether or not to retrieve only the current scheduled meeting of the meeting series, i.e. the
            meeting ready to join or start or the upcoming meeting of the meeting series. If it's `true`, return
            details for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start
            or the upcoming scheduled meeting of the meeting series. If it's `false` or not specified, return details
            for the entire meeting series. This parameter only applies to meeting series.
        :type current: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :param send_email: If `true` send email to the registrant. Default: `true`.
        :type send_email: bool
        :param job_title: The registrant's job title. Registration options define whether or not this is required.
        :type job_title: str
        :param company_name: The registrant's company. Registration options define whether or not this is required.
        :type company_name: str
        :param address1: The registrant's first address line. Registration options define whether or not this is
            required.
        :type address1: str
        :param address2: The registrant's second address line. Registration options define whether or not this is
            required.
        :type address2: str
        :param city: The registrant's city name. Registration options define whether or not this is required.
        :type city: str
        :param state: The registrant's state. Registration options define whether or not this is required.
        :type state: str
        :param zip_code: The registrant's postal code. Registration options define whether or not this is required.
        :type zip_code: int
        :param country_region: The America is not a country or a specific region. Registration options define whether
            or not this is required.
        :type country_region: str
        :param work_phone: The registrant's work phone number. Registration options define whether or not this is
            required.
        :type work_phone: str
        :param fax: The registrant's FAX number. Registration options define whether or not this is required.
        :type fax: str
        :param customized_questions: The registrant's answers for customized questions. Registration options define
            whether or not this is required.
        :type customized_questions: list[CustomizedRegistrant]
        :rtype: :class:`RegistrantCreateResponse`
        """
        params = {}
        if current is not None:
            params['current'] = str(current).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        body = dict()
        body['firstName'] = first_name
        body['lastName'] = last_name
        body['email'] = email
        if send_email is not None:
            body['sendEmail'] = send_email
        if job_title is not None:
            body['jobTitle'] = job_title
        if company_name is not None:
            body['companyName'] = company_name
        if address1 is not None:
            body['address1'] = address1
        if address2 is not None:
            body['address2'] = address2
        if city is not None:
            body['city'] = city
        if state is not None:
            body['state'] = state
        if zip_code is not None:
            body['zipCode'] = zip_code
        if country_region is not None:
            body['countryRegion'] = country_region
        if work_phone is not None:
            body['workPhone'] = work_phone
        if fax is not None:
            body['fax'] = fax
        if customized_questions is not None:
            body['customizedQuestions'] = loads(TypeAdapter(list[CustomizedRegistrant]).dump_json(customized_questions, by_alias=True, exclude_none=True))
        url = self.ep(f'{meeting_id}/registrants')
        data = super().post(url, params=params, json=body)
        r = RegistrantCreateResponse.model_validate(data)
        return r

    def batch_register_meeting_registrants(self, meeting_id: str, current: bool = None, host_email: str = None,
                                           items: list[RegistrantFormObject] = None) -> list[RegistrantCreateResponse]:
        """
        Batch register Meeting Registrants

        Bulk register new registrants for a meeting. When a meeting or webinar is created, this API can only be used if
        Registration is checked on the page or the registration attribute is specified through the `Create a Meeting
        <https://developer.webex.com/docs/api/v1/meetings/create-a-meeting>`_
        API.

        :param meeting_id: Unique identifier for the meeting. Only the ID of the meeting series is supported for
            meetingId. IDs of scheduled meetings, meeting instances, or scheduled personal room meetings are not
            supported. See the `Meetings Overview
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for more information about meeting types.
        :type meeting_id: str
        :param current: Whether or not to retrieve only the current scheduled meeting of the meeting series, i.e. the
            meeting ready to join or start or the upcoming meeting of the meeting series. If it's `true`, return
            details for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start
            or the upcoming scheduled meeting of the meeting series. If it's `false` or not specified, return details
            for the entire meeting series. This parameter only applies to meeting series.
        :type current: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :param items: Registrants array.
        :type items: list[RegistrantFormObject]
        :rtype: list[RegistrantCreateResponse]
        """
        params = {}
        if current is not None:
            params['current'] = str(current).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        body = dict()
        if items is not None:
            body['items'] = loads(TypeAdapter(list[RegistrantFormObject]).dump_json(items, by_alias=True, exclude_none=True))
        url = self.ep(f'{meeting_id}/registrants/bulkInsert')
        data = super().post(url, params=params, json=body)
        r = TypeAdapter(list[RegistrantCreateResponse]).validate_python(data['items'])
        return r

    def get_detailed_information_for_a_meeting_registrant(self, meeting_id: str, registrant_id: str,
                                                          current: bool = None, host_email: str = None) -> Registrant:
        """
        Get Detailed Information for a Meeting Registrant

        Retrieves details for a meeting registrant with a specified registrant Id.

        :param meeting_id: Unique identifier for the meeting. Only the ID of the meeting series is supported for
            meetingId. IDs of scheduled meetings, meeting instances, or scheduled personal room meetings are not
            supported. See the `Meetings Overview
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for more information about meeting types.
        :type meeting_id: str
        :param registrant_id: Unique identifier for the registrant
        :type registrant_id: str
        :param current: Whether or not to retrieve only the current scheduled meeting of the meeting series, i.e. the
            meeting ready to join or start or the upcoming meeting of the meeting series. If it's `true`, return
            details for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start
            or the upcoming scheduled meeting of the meeting series. If it's `false` or not specified, return details
            for the entire meeting series. This parameter only applies to meeting series.
        :type current: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :rtype: :class:`Registrant`
        """
        params = {}
        if current is not None:
            params['current'] = str(current).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}/registrants/{registrant_id}')
        data = super().get(url, params=params)
        r = Registrant.model_validate(data)
        return r

    def list_meeting_registrants(self, meeting_id: str, host_email: str = None, current: bool = None,
                                 email: str = None, registration_time_from: Union[str, datetime] = None,
                                 registration_time_to: Union[str, datetime] = None,
                                 **params) -> Generator[Registrant, None, None]:
        """
        List Meeting Registrants

        Meeting's host and cohost can retrieve the list of registrants for a meeting with a specified meeting Id.

        :param meeting_id: Unique identifier for the meeting. Only the ID of the meeting series is supported for
            meetingId. IDs of scheduled meetings, meeting instances, or scheduled personal room meetings are not
            supported. See the `Meetings Overview
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for more information about meeting types.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :param current: Whether or not to retrieve only the current scheduled meeting of the meeting series, i.e. the
            meeting ready to join or start or the upcoming meeting of the meeting series. If it's `true`, return
            details for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start
            or the upcoming scheduled meeting of the meeting series. If it's `false` or not specified, return details
            for the entire meeting series. This parameter only applies to meeting series.
        :type current: bool
        :param email: Registrant's email to filter registrants.
        :type email: str
        :param registration_time_from: The time registrants register a meeting starts from the specified date and time
            (inclusive) in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If `registrationTimeFrom` is not specified, it equals
            `registrationTimeTo` minus 7 days.
        :type registration_time_from: Union[str, datetime]
        :param registration_time_to: The time registrants register a meeting before the specified date and time
            (exclusive) in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format. If `registrationTimeTo` is not specified, it equals
            `registrationTimeFrom` plus 7 days. The interval between `registrationTimeFrom` and `registrationTimeTo`
            must be within 90 days.
        :type registration_time_to: Union[str, datetime]
        :return: Generator yielding :class:`Registrant` instances
        """
        if host_email is not None:
            params['hostEmail'] = host_email
        if current is not None:
            params['current'] = str(current).lower()
        if email is not None:
            params['email'] = email
        if registration_time_from is not None:
            if isinstance(registration_time_from, str):
                registration_time_from = isoparse(registration_time_from)
            registration_time_from = dt_iso_str(registration_time_from)
            params['registrationTimeFrom'] = registration_time_from
        if registration_time_to is not None:
            if isinstance(registration_time_to, str):
                registration_time_to = isoparse(registration_time_to)
            registration_time_to = dt_iso_str(registration_time_to)
            params['registrationTimeTo'] = registration_time_to
        url = self.ep(f'{meeting_id}/registrants')
        return self.session.follow_pagination(url=url, model=Registrant, item_key='items', params=params)

    def query_meeting_registrants(self, meeting_id: str, emails: list[str], current: bool = None,
                                  host_email: str = None, status: RegistrantStatus = None,
                                  order_type: QueryRegistrantsOrderType = None,
                                  order_by: QueryRegistrantsOrderBy = None,
                                  **params) -> Generator[Registrant, None, None]:
        """
        Query Meeting Registrants

        Meeting's host and cohost can query the list of registrants for a meeting with a specified meeting ID and
        registrants email.

        :param meeting_id: Unique identifier for the meeting. Only the ID of the meeting series is supported for
            meetingId. IDs of scheduled meetings, meeting instances, or scheduled personal room meetings are not
            supported. See the `Meetings Overview
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for more information about meeting types.
        :type meeting_id: str
        :param emails: List of registrant email addresses.
        :type emails: list[str]
        :param current: Whether or not to retrieve only the current scheduled meeting of the meeting series, i.e. the
            meeting ready to join or start or the upcoming meeting of the meeting series. If it's `true`, return
            details for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start
            or the upcoming scheduled meeting of the meeting series. If it's `false` or not specified, return details
            for the entire meeting series. This parameter only applies to meeting series.
        :type current: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :param status: Registrant's status.
        :type status: RegistrantStatus
        :param order_type: Sort order for the registrants.
        :type order_type: QueryRegistrantsOrderType
        :param order_by: Registrant ordering field. Ordered by `registrationTime` by default.
        :type order_by: QueryRegistrantsOrderBy
        :return: Generator yielding :class:`Registrant` instances
        """
        if current is not None:
            params['current'] = str(current).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        body = dict()
        if status is not None:
            body['status'] = enum_str(status)
        if order_type is not None:
            body['orderType'] = enum_str(order_type)
        if order_by is not None:
            body['orderBy'] = enum_str(order_by)
        body['emails'] = emails
        url = self.ep(f'{meeting_id}/registrants/query')
        return self.session.follow_pagination(url=url, model=Registrant, item_key='items', params=params, json=body)

    def batch_update_meeting_registrants_status(self, meeting_id: str,
                                                status_op_type: BatchUpdateMeetingRegistrantsStatusStatusOpType,
                                                current: bool = None, host_email: str = None, send_email: str = None,
                                                registrants: list[Registrants] = None):
        """
        Batch Update Meeting Registrants status

        Meeting's host or cohost can update the set of registrants for a meeting. `cancel` means the registrant(s) will
        be moved back to the registration list. `bulkDelete` means the registrant(s) will be deleted.

        :param meeting_id: Unique identifier for the meeting. Only the ID of the meeting series is supported for
            meetingId. IDs of scheduled meetings, meeting instances, or scheduled personal room meetings are not
            supported. See the `Meetings Overview
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for more information about meeting types.
        :type meeting_id: str
        :param status_op_type: Update registrant's status.
        :type status_op_type: BatchUpdateMeetingRegistrantsStatusStatusOpType
        :param current: Whether or not to retrieve only the current scheduled meeting of the meeting series, i.e. the
            meeting ready to join or start or the upcoming meeting of the meeting series. If it's `true`, return
            details for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start
            or the upcoming scheduled meeting of the meeting series. If it's `false` or not specified, return details
            for the entire meeting series. This parameter only applies to meeting series.
        + Default: `false`
        :type current: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :param send_email: If `true` send email to registrants. Default: `true`.
        :type send_email: str
        :param registrants: Registrants array.
        :type registrants: list[Registrants]
        :rtype: None
        """
        params = {}
        if current is not None:
            params['current'] = str(current).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        body = dict()
        if send_email is not None:
            body['sendEmail'] = send_email
        if registrants is not None:
            body['registrants'] = loads(TypeAdapter(list[Registrants]).dump_json(registrants, by_alias=True, exclude_none=True))
        url = self.ep(f'{meeting_id}/registrants/{status_op_type}')
        super().post(url, params=params, json=body)

    def delete_a_meeting_registrant(self, meeting_id: str, registrant_id: str, current: bool = None,
                                    host_email: str = None):
        """
        Delete a Meeting Registrant

        Meeting's host or cohost can delete a registrant with a specified registrant ID.

        :param meeting_id: Unique identifier for the meeting. Only the ID of the meeting series is supported for
            meetingId. IDs of scheduled meetings, meeting instances, or scheduled personal room meetings are not
            supported. See the `Meetings Overview
            <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for more information about meeting types.
        :type meeting_id: str
        :param registrant_id: Unique identifier for the registrant.
        :type registrant_id: str
        :param current: Whether or not to retrieve only the current scheduled meeting of the meeting series, i.e. the
            meeting ready to join or start or the upcoming meeting of the meeting series. If it's `true`, return
            details for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start
            or the upcoming scheduled meeting of the meeting series. If it's `false` or not specified, return details
            for the entire meeting series. This parameter only applies to meeting series.
        :type current: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :rtype: None
        """
        params = {}
        if current is not None:
            params['current'] = str(current).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}/registrants/{registrant_id}')
        super().delete(url, params=params)

    def update_meeting_simultaneous_interpretation(self, meeting_id: str, enabled: bool,
                                                   interpreters: list[InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting]) -> MeetingSeriesObjectSimultaneousInterpretation:
        """
        Update Meeting Simultaneous interpretation

        Updates simultaneous interpretation options of a meeting with a specified meeting ID. This operation applies to
        meeting series and scheduled meetings. It doesn't apply to ended or in-progress meeting instances.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled
            `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting.
        :type meeting_id: str
        :param enabled: Whether or not simultaneous interpretation is enabled.
        :type enabled: bool
        :param interpreters: Interpreters for meeting.
        :type interpreters: list[InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting]
        :rtype: :class:`MeetingSeriesObjectSimultaneousInterpretation`
        """
        body = dict()
        body['enabled'] = enabled
        body['interpreters'] = loads(TypeAdapter(list[InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting]).dump_json(interpreters, by_alias=True, exclude_none=True))
        url = self.ep(f'{meeting_id}/simultaneousInterpretation')
        data = super().put(url, json=body)
        r = MeetingSeriesObjectSimultaneousInterpretation.model_validate(data)
        return r

    def create_a_meeting_interpreter(self, meeting_id: str, language_code1: str, language_code2: str,
                                     email: str = None, display_name: str = None, host_email: str = None,
                                     send_email: bool = None) -> InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting:
        """
        Create a Meeting Interpreter

        Assign an interpreter to a bi-directional simultaneous interpretation language channel for a meeting.

        :param meeting_id: Unique identifier for the meeting to which the interpreter is to be assigned.
        :type meeting_id: str
        :param language_code1: The pair of `languageCode1` and `languageCode2` form a bi-directional simultaneous
            interpretation language channel. The language codes conform with `ISO 639-1
            <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_.
        :type language_code1: str
        :param language_code2: The pair of `languageCode1` and `languageCode2` form a bi-directional simultaneous
            interpretation language channel. The language codes conform with `ISO 639-1
            <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_.
        :type language_code2: str
        :param email: Email address of meeting interpreter. If not specified, an empty interpreter will be created for
            this bi-directional language channel, and a specific email can be assigned to this empty interpreter by
            `Update a Meeting Interpreter` API later. Please note that multiple interpreters with different emails can
            be assigned to the same bi-directional language channel, but the same email cannot be assigned to more
            than one interpreter.
        :type email: str
        :param display_name: Display name of meeting interpreter. If the interpreter is already an invitee of the
            meeting and it has a different display name, that invitee's display name will be overwritten by this
            attribute.
        :type display_name: str
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param send_email: If `true`, send email to the interpreter.
        :type send_email: bool
        :rtype: :class:`InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting`
        """
        body = dict()
        body['languageCode1'] = language_code1
        body['languageCode2'] = language_code2
        if email is not None:
            body['email'] = email
        if display_name is not None:
            body['displayName'] = display_name
        if host_email is not None:
            body['hostEmail'] = host_email
        if send_email is not None:
            body['sendEmail'] = send_email
        url = self.ep(f'{meeting_id}/interpreters')
        data = super().post(url, json=body)
        r = InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting.model_validate(data)
        return r

    def get_a_meeting_interpreter(self, meeting_id: str, interpreter_id: str,
                                  host_email: str = None) -> InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting:
        """
        Get a Meeting Interpreter

        Retrieves details for a meeting interpreter identified by `meetingId` and `interpreterId` in the URI.

        :param meeting_id: Unique identifier for the meeting to which the interpreter has been assigned.
        :type meeting_id: str
        :param interpreter_id: Unique identifier for the interpreter whose details are being requested.
        :type interpreter_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return details for an interpreter of the meeting that is hosted by that
            user.
        :type host_email: str
        :rtype: :class:`InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting`
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}/interpreters/{interpreter_id}')
        data = super().get(url, params=params)
        r = InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting.model_validate(data)
        return r

    def list_meeting_interpreters(self, meeting_id: str,
                                  host_email: str = None) -> list[InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting]:
        """
        List Meeting Interpreters

        Lists meeting interpreters for a meeting with a specified `meetingId`.

        This operation can be used for meeting series, scheduled meeting and ended or ongoing meeting instance objects.
        If the specified `meetingId` is for a meeting series, the interpreters for the series will be listed; if the
        `meetingId` is for a scheduled meeting, the interpreters for the particular scheduled meeting will be listed;
        if the `meetingId` is for an ended or ongoing meeting instance, the interpreters for the particular meeting
        instance will be listed. See the `Webex Meetings
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ guide for more information about the types of meetings.

        The list returned is sorted in descending order by when interpreters were created.

        :param meeting_id: Unique identifier for the meeting for which interpreters are being requested. The meeting
            can be meeting series, scheduled meeting or meeting instance which has ended or is ongoing. Please note
            that currently meeting ID of a scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return interpreters of the meeting that is hosted by that user.
        :type host_email: str
        :rtype: list[InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting]
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}/interpreters')
        data = super().get(url, params=params)
        r = TypeAdapter(list[InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting]).validate_python(data['items'])
        return r

    def update_a_meeting_interpreter(self, meeting_id: str, interpreter_id: str, language_code1: str,
                                     language_code2: str, email: str = None, display_name: str = None,
                                     host_email: str = None,
                                     send_email: bool = None) -> InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting:
        """
        Update a Meeting Interpreter

        Updates details for a meeting interpreter identified by `meetingId` and `interpreterId` in the URI.

        :param meeting_id: Unique identifier for the meeting whose interpreters were belong to.
        :type meeting_id: str
        :param interpreter_id: Unique identifier for the interpreter whose details are being requested.
        :type interpreter_id: str
        :param language_code1: The pair of `languageCode1` and `languageCode2` form a bi-directional simultaneous
            interpretation language channel. The language codes conform with `ISO 639-1
            <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_.
        :type language_code1: str
        :param language_code2: The pair of `languageCode1` and `languageCode2` form a bi-directional simultaneous
            interpretation language channel. The language codes conform with `ISO 639-1
            <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_.
        :type language_code2: str
        :param email: Email address of meeting interpreter. If not specified, it'll be an empty interpreter for the
            bi-directional language channel. Please note that multiple interpreters with different emails can be
            assigned to the same bi-directional language channel, but the same email cannot be assigned to more than
            one interpreter.
        :type email: str
        :param display_name: Display name of meeting interpreter. If the interpreter is already an invitee of the
            meeting and it has a different display name, that invitee's display name will be overwritten by this
            attribute.
        :type display_name: str
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param send_email: If `true`, send email to the interpreter.
        :type send_email: bool
        :rtype: :class:`InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting`
        """
        body = dict()
        body['languageCode1'] = language_code1
        body['languageCode2'] = language_code2
        if email is not None:
            body['email'] = email
        if display_name is not None:
            body['displayName'] = display_name
        if host_email is not None:
            body['hostEmail'] = host_email
        if send_email is not None:
            body['sendEmail'] = send_email
        url = self.ep(f'{meeting_id}/interpreters/{interpreter_id}')
        data = super().put(url, json=body)
        r = InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting.model_validate(data)
        return r

    def delete_a_meeting_interpreter(self, meeting_id: str, interpreter_id: str, host_email: str = None,
                                     send_email: bool = None):
        """
        Delete a Meeting Interpreter

        Removes a meeting interpreter identified by `meetingId` and `interpreterId` in the URI. The deleted meeting
        interpreter cannot be recovered.

        :param meeting_id: Unique identifier for the meeting whose interpreters were belong to.
        :type meeting_id: str
        :param interpreter_id: Unique identifier for the interpreter to be removed.
        :type interpreter_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will delete an interpreter of the meeting that is hosted by that user.
        :type host_email: str
        :param send_email: If `true`, send email to the interpreter.
        :type send_email: bool
        :rtype: None
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if send_email is not None:
            params['sendEmail'] = str(send_email).lower()
        url = self.ep(f'{meeting_id}/interpreters/{interpreter_id}')
        super().delete(url, params=params)

    def update_meeting_breakout_sessions(self, meeting_id: str, items: list[BreakoutSessionObject],
                                         host_email: str = None,
                                         send_email: bool = None) -> list[GetBreakoutSessionObject]:
        """
        Update Meeting Breakout Sessions

        Updates breakout sessions of a meeting with a specified meeting ID in the pre-meeting state. This operation
        applies to meeting series and scheduled meetings.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled
            `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting.
        :type meeting_id: str
        :param items: Breakout sessions are smaller groups that are split off from the main meeting or webinar. They
            allow a subset of participants to collaborate and share ideas over audio and video. Use breakout sessions
            for workshops, classrooms, or for when you need a moment to talk privately with a few participants outside
            of the main session. Please note that maximum number of breakout sessions in a meeting or webinar is 100.
            In webinars, if hosts preassign attendees to breakout sessions, the role of `attendee` will be changed to
            `panelist`. Breakout session is not supported for a meeting with simultaneous interpretation.
        :type items: list[BreakoutSessionObject]
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :rtype: list[GetBreakoutSessionObject]
        """
        body = dict()
        if host_email is not None:
            body['hostEmail'] = host_email
        if send_email is not None:
            body['sendEmail'] = send_email
        body['items'] = loads(TypeAdapter(list[BreakoutSessionObject]).dump_json(items, by_alias=True, exclude_none=True))
        url = self.ep(f'{meeting_id}/breakoutSessions')
        data = super().put(url, json=body)
        r = TypeAdapter(list[GetBreakoutSessionObject]).validate_python(data['items'])
        return r

    def list_meeting_breakout_sessions(self, meeting_id: str) -> list[GetBreakoutSessionObject]:
        """
        List Meeting Breakout Sessions

        Lists meeting breakout sessions for a meeting with a specified `meetingId`.

        This operation can be used for meeting series, scheduled meeting and ended or ongoing meeting instance objects.
        See the `Webex Meetings
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ guide for more information about the types of meetings.

        :param meeting_id: Unique identifier for the meeting. This parameter applies to meeting series, scheduled
            meeting and ended or ongoing meeting instance objects. Please note that currently meeting ID of a
            scheduled `personal room
            <https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings>`_ meeting is not supported for this API.
        :type meeting_id: str
        :rtype: list[GetBreakoutSessionObject]
        """
        url = self.ep(f'{meeting_id}/breakoutSessions')
        data = super().get(url)
        r = TypeAdapter(list[GetBreakoutSessionObject]).validate_python(data['items'])
        return r

    def delete_meeting_breakout_sessions(self, meeting_id: str, send_email: bool = None):
        """
        Delete Meeting Breakout Sessions

        Deletes breakout sessions with a specified meeting ID. The deleted breakout sessions cannot be recovered. The
        value of `enabledBreakoutSessions` attribute is set to `false` automatically.
        This operation applies to meeting series and scheduled meetings. It doesn't apply to ended or in-progress
        meeting instances.

        :param meeting_id: Unique identifier for the meeting. This parameter applies to meeting series and scheduled
            meetings. It doesn't apply to ended or in-progress meeting instances.
        :type meeting_id: str
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :rtype: None
        """
        params = {}
        if send_email is not None:
            params['sendEmail'] = str(send_email).lower()
        url = self.ep(f'{meeting_id}/breakoutSessions')
        super().delete(url, params=params)

    def get_a_meeting_survey(self, meeting_id: str) -> SurveyObject:
        """
        Get a Meeting Survey

        Retrieves details for a meeting survey identified by `meetingId`.

        #### Request Header

        * `hostEmail`: Email address for the meeting host. This parameter is only used if the user or application
        calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a site
        they manage and the API will return survey details of that user.

        :param meeting_id: Unique identifier for the meeting. Please note that only the meeting ID of a scheduled
            webinar is supported for this API.
        :type meeting_id: str
        :rtype: :class:`SurveyObject`
        """
        url = self.ep(f'{meeting_id}/survey')
        data = super().get(url)
        r = SurveyObject.model_validate(data)
        return r

    def list_meeting_survey_results(self, meeting_id: str, meeting_start_time_from: Union[str, datetime] = None,
                                    meeting_start_time_to: Union[str, datetime] = None,
                                    **params) -> Generator[SurveyResultObject, None, None]:
        """
        List Meeting Survey Results

        Retrieves results for a meeting survey identified by `meetingId`.

        #### Request Header

        * `timezone`: Time zone for time stamps in response body, defined in conformance with the
        `IANA time zone database
        <https://www.iana.org/time-zones>`_. The default value is `UTC` if not specified.

        * `hostEmail`: Email address for the meeting host. This parameter is only used if the user or application
        calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a site
        they manage and the API will return the survey results of that user.

        :param meeting_id: Unique identifier for the meeting. Please note that only the meeting ID of a scheduled
            webinar is supported for this API.
        :type meeting_id: str
        :param meeting_start_time_from: Start date and time (inclusive) in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format for the
            meeting objects being requested. `meetingStartTimeFrom` cannot be after `meetingStartTimeTo`. This
            parameter will be ignored if `meetingId` is the unique identifier for the specific meeting instance.
        When `meetingId` is not the unique identifier for the specific meeting instance, the `meetingStartTimeFrom`, if
        not specified, equals `meetingStartTimeTo` minus `1` month; if `meetingStartTimeTo` is also not specified, the
        default value for `meetingStartTimeFrom` is `1` month before the current date and time.
        :type meeting_start_time_from: Union[str, datetime]
        :param meeting_start_time_to: End date and time (exclusive) in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format for the meeting
            objects being requested. `meetingStartTimeTo` cannot be prior to `meetingStartTimeFrom`. This parameter
            will be ignored if `meetingId` is the unique identifier for the specific meeting instance.
        When `meetingId` is not the unique identifier for the specific meeting instance, if `meetingStartTimeFrom` is
        also not specified, the default value for `meetingStartTimeTo` is the current date and time;For example,if
        `meetingStartTimeFrom` is a month ago, the default value for `meetingStartTimeTo` is `1` month after
        `meetingStartTimeFrom`.Otherwise it is the current date and time.
        :type meeting_start_time_to: Union[str, datetime]
        :return: Generator yielding :class:`SurveyResultObject` instances
        """
        if meeting_start_time_from is not None:
            if isinstance(meeting_start_time_from, str):
                meeting_start_time_from = isoparse(meeting_start_time_from)
            meeting_start_time_from = dt_iso_str(meeting_start_time_from)
            params['meetingStartTimeFrom'] = meeting_start_time_from
        if meeting_start_time_to is not None:
            if isinstance(meeting_start_time_to, str):
                meeting_start_time_to = isoparse(meeting_start_time_to)
            meeting_start_time_to = dt_iso_str(meeting_start_time_to)
            params['meetingStartTimeTo'] = meeting_start_time_to
        url = self.ep(f'{meeting_id}/surveyResults')
        return self.session.follow_pagination(url=url, model=SurveyResultObject, item_key='items', params=params)

    def get_meeting_survey_links(self, meeting_id: str, emails: list[str], host_email: str = None,
                                 meeting_start_time_from: Union[str, datetime] = None,
                                 meeting_start_time_to: Union[str, datetime] = None) -> list[SurveyLinkObject]:
        """
        Get Meeting Survey Links

        Get survey links of a meeting for different users.

        #### Request Header

        * `timezone`: Time zone for the `meetingStartTimeFrom` and `meetingStartTimeTo` parameters and defined in
        conformance with the `IANA time zone database
        <https://www.iana.org/time-zones>`_. The default value is `UTC` if not specified.

        :param meeting_id: Unique identifier for the meeting. Only applies to webinars. Meetings and personal room
            meetings are not supported.
        :type meeting_id: str
        :param emails: Participants' email list. The maximum size of `emails` is 100.
        :type emails: list[str]
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. An admin can specify the email of the meeting host who
            is in a site he manages and the API returns post survey links on behalf of the meeting host.
        :type host_email: str
        :param meeting_start_time_from: Start date and time (inclusive) in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format for the
            meeting objects being requested and conforms with the `timezone` in the request header if specified.
            `meetingStartTimeFrom` cannot be after `meetingStartTimeTo`. Only applies when `meetingId` is not an
            instance ID. The API generates survey links for the last instance of `meetingId` in the time range
            specified by `meetingStartTimeFrom` and `meetingStartTimeTo`. If not specified, `meetingStartTimeFrom`
            equals `meetingStartTimeTo` minus `1` month; if `meetingStartTimeTo` is also not specified, the default
            value for `meetingStartTimeFrom` is `1` month before the current date and time.
        :type meeting_start_time_from: Union[str, datetime]
        :param meeting_start_time_to: End date and time (exclusive) in any `ISO 8601
            <https://en.wikipedia.org/wiki/ISO_8601>`_ compliant format for the meeting
            objects being requested and conforms with the `timezone` in the request header if specified.
            `meetingStartTimeTo` cannot be prior to `meetingStartTimeFrom`. Only applies when `meetingId` is not an
            instance ID. The API generates survey links for the last instance of `meetingId` in the time range
            specified by `meetingStartTimeFrom` and `meetingStartTimeTo`. If not specified, `meetingStartTimeTo`
            equals `meetingStartTimeFrom` plus `1` month; if `meetingStartTimeFrom` is also not specified, the default
            value for `meetingStartTimeTo` is the current date and time.
        :type meeting_start_time_to: Union[str, datetime]
        :rtype: list[SurveyLinkObject]
        """
        body = dict()
        if host_email is not None:
            body['hostEmail'] = host_email
        if meeting_start_time_from is not None:
            body['meetingStartTimeFrom'] = meeting_start_time_from
        if meeting_start_time_to is not None:
            body['meetingStartTimeTo'] = meeting_start_time_to
        body['emails'] = emails
        url = self.ep(f'{meeting_id}/surveyLinks')
        data = super().post(url, json=body)
        r = TypeAdapter(list[SurveyLinkObject]).validate_python(data['items'])
        return r

    def create_invitation_sources(self, meeting_id: str, host_email: str = None, person_id: str = None,
                                  items: list[InvitationSourceCreateObject] = None) -> list[InvitationSourceObject]:
        """
        Create Invitation Sources

        Creates one or more invitation sources for a meeting.

        :param meeting_id: Unique identifier for the meeting. Only the meeting ID of a scheduled webinar is supported
            for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if a user or application
            calling the API has the admin-level scopes. The admin may specify the email of a user on a site they
            manage and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :param person_id: Unique identifier for the meeting host. Should only be set if the user or application calling
            the API has the admin-level scopes. When used, the admin may specify the email of a user in a site they
            manage to be the meeting host.
        :type person_id: str
        :type items: list[InvitationSourceCreateObject]
        :rtype: list[InvitationSourceObject]
        """
        body = dict()
        if host_email is not None:
            body['hostEmail'] = host_email
        if person_id is not None:
            body['personId'] = person_id
        if items is not None:
            body['items'] = loads(TypeAdapter(list[InvitationSourceCreateObject]).dump_json(items, by_alias=True, exclude_none=True))
        url = self.ep(f'{meeting_id}/invitationSources')
        data = super().post(url, json=body)
        r = TypeAdapter(list[InvitationSourceObject]).validate_python(data['items'])
        return r

    def list_invitation_sources(self, meeting_id: str) -> list[InvitationSourceObject]:
        """
        List Invitation Sources

        Lists invitation sources for a meeting.

        #### Request Header

        * `hostEmail`: Email address for the meeting host. This parameter is only used if the user or application
        calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a site
        they manage and the API will return recording details of that user.

        * `personId`:  Unique identifier for the meeting host. This attribute should only be set if the user or
        application calling the API has the admin-level scopes. When used, the admin may specify the email of a user
        in a site they manage to be the meeting host.

        :param meeting_id: Unique identifier for the meeting. Only the meeting ID of a scheduled webinar is supported
            for this API.
        :type meeting_id: str
        :rtype: list[InvitationSourceObject]
        """
        url = self.ep(f'{meeting_id}/invitationSources')
        data = super().get(url)
        r = TypeAdapter(list[InvitationSourceObject]).validate_python(data['items'])
        return r

    def list_meeting_tracking_codes(self, service: str, site_url: str = None,
                                    host_email: str = None) -> MeetingTrackingCodesObject:
        """
        List Meeting Tracking Codes

        Lists tracking codes on a site by a meeting host. The result indicates which tracking codes and what options
        can be used to create or update a meeting on the specified site.

        * The `options` here differ from those in the `site-level tracking codes
        <https://developer.webex.com/docs/api/v1/tracking-codes/get-a-tracking-code>`_ and the `user-level tracking codes
        is the result of a selective combination of the two.

        * For a tracking code, if there is no user-level tracking code, the API returns the site-level options, and the
        `defaultValue` of the site-level default option is `true`. If there is a user-level tracking code, it is
        merged into the `options`. Meanwhile, the `defaultValue` of this user-level option is `true` and the
        site-level default option becomes non default.

        * If `siteUrl` is specified, tracking codes of the specified site will be listed; otherwise, tracking codes of
        the user's preferred site will be listed. All available Webex sites and the preferred sites of a user can be
        retrieved by `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        :param service: Service for schedule or sign-up pages.
        :type service: str
        :param site_url: URL of the Webex site which the API retrieves the tracking code from. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and preferred
            sites of a user can be retrieved by `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :param host_email: Email address for the meeting host. This parameter is only used if a user or application
            calling the API has the admin-level scopes. The admin may specify the email of a user on a site they
            manage and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :rtype: :class:`MeetingTrackingCodesObject`
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        params['service'] = service
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep('trackingCodes')
        data = super().get(url, params=params)
        r = MeetingTrackingCodesObject.model_validate(data)
        return r

    def reassign_meetings_to_a_new_host(self, host_email: str,
                                        meeting_ids: list[str]) -> list[ReassignMeetingResponseObject]:
        """
        Reassign Meetings to a New Host

        Reassigns a list of meetings to a new host by an admin user.

        All the meetings of `meetingIds` should belong to the same site, which is the `siteUrl` in the request header,
        if specified, or the admin user's preferred site, if not specified. All available Webex sites and the
        preferred sites of a user can be retrieved by `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        If the user of `hostEmail` is not qualified to be a host of the target site, the API returns an error with the
        HTTP status code `403`. If all the meetings referenced by `meetingIds` have been reassigned the new host
        successfully, the API returns an empty response with the HTTP status code `204`. Otherwise, if all the
        meetings of `meetingIds` fail or some of them fail, the API returns a "Multi-Status" response with status code
        of `207`, and individual errors for each meeting in the response body.

        Only IDs of meeting series are supported for the `meetingIds`. IDs of scheduled meetings, meeting instances, or
        scheduled personal room meetings are not supported. See the `Meetings Overview
        <https://developer.webex.com/docs/meetings#meeting-series-scheduled-meetings-and-meeting-instances>`_ for more information about the
        types of meetings.

        There are several limitations when reassigning meetings:

        * Users cannot assign an in-progress meeting.

        * Users cannot assign a meeting to a user who is not a Webex user, or an attendee who does not have host
        privilege.

        * Users cannot assign a meeting with calling/callback to a host user who does not have calling/callback
        privileges

        * Users cannot assign a meeting with session type A to a host user who does not have session type A privileges.

        * Users cannot assign an MC or Webinar to a new host who does not have an MC license or a Webinar license.

        * Users cannot assign a TC/EC1.0/SC meeting, or a meeting that is created by on-behalf to a new host.

        * Users cannot assign meetings from third-party integrations, such as meetings integrated with Outlook or
        Google.

        #### Request Header

        * `siteUrl`: Optional request header parameter. All the meetings of `meetingIds` should belong to the site
        referenced by siteUrl if specified. Otherwise, the meetings should belong to the admin user's preferred sites.
        All available Webex sites and the preferred sites of a user can be retrieved by `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        :param host_email: Email address of the new meeting host.
        :type host_email: str
        :param meeting_ids: List of meeting series IDs to be reassigned the new host. The size is between 1 and 100.
            All the meetings of `meetingIds` should belong to the same site, which is the `siteUrl` in the request
            header, if specified, or the admin user's preferred site, if not specified. All available Webex sites and
            the preferred sites of a user can be retrieved by `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type meeting_ids: list[str]
        :rtype: list[ReassignMeetingResponseObject]
        """
        body = dict()
        body['hostEmail'] = host_email
        body['meetingIds'] = meeting_ids
        url = self.ep('reassignHost')
        data = super().post(url, json=body)
        r = TypeAdapter(list[ReassignMeetingResponseObject]).validate_python(data['items'])
        return r

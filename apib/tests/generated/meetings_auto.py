from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['AnswerForCustomizedQuestion', 'BatchRegisterMeetingRegistrantsResponse', 'BatchUpdateMeetingRegistrantsStatusStatusOpType', 'BreakoutSessionObject', 'Control', 'CreateInvitationSourcesResponse', 'CreateMeetingObject', 'CreateMeetingObjectRegistration', 'CreateMeetingObjectSimultaneousInterpretation', 'CustomizedQuestionForCreateMeeting', 'CustomizedQuestionForCreateMeetingOptions', 'CustomizedQuestionForCreateMeetingRules', 'CustomizedQuestionForCreateMeetingRulesCondition', 'CustomizedQuestionForCreateMeetingRulesResult', 'CustomizedQuestionForCreateMeetingType', 'CustomizedQuestionForGetMeeting', 'CustomizedQuestionForGetMeetingRules', 'CustomizedRegistrant', 'DetailedTemplateObject', 'GetBreakoutSessionObject', 'GetBreakoutSessionsObject', 'GetMeetingSurveyLinksResponse', 'InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting', 'InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting', 'InvitationSourceCreateObject', 'InvitationSourceObject', 'InviteeObjectForCreateMeeting', 'JoinMeetingLinkObject', 'JoinMeetingObject', 'LinksObjectForTelephony', 'ListMeetingInterpretersResponse', 'ListMeetingRegistrantsResponse', 'ListMeetingSessionTypesResponse', 'ListMeetingSurveyResultsResponse', 'ListMeetingTemplatesResponse', 'ListMeetingsOfAMeetingSeriesMeetingType', 'ListMeetingsOfAMeetingSeriesResponse', 'ListMeetingsOfAMeetingSeriesState', 'ListMeetingsResponse', 'MeetingSeriesObject', 'MeetingSeriesObjectAttendeePrivileges', 'MeetingSeriesObjectAudioConnectionOptions', 'MeetingSeriesObjectAudioConnectionOptionsAudioConnectionType', 'MeetingSeriesObjectAudioConnectionOptionsEntryAndExitTone', 'MeetingSeriesObjectForListMeeting', 'MeetingSeriesObjectMeetingOptions', 'MeetingSeriesObjectMeetingOptionsNoteType', 'MeetingSeriesObjectMeetingType', 'MeetingSeriesObjectRegistration', 'MeetingSeriesObjectScheduledType', 'MeetingSeriesObjectSimultaneousInterpretation', 'MeetingSeriesObjectState', 'MeetingSeriesObjectTelephony', 'MeetingSeriesObjectTelephonyCallInNumbers', 'MeetingSeriesObjectTelephonyCallInNumbersTollType', 'MeetingSeriesObjectUnlockedMeetingJoinSecurity', 'MeetingSeriesObjectWithAdhoc', 'MeetingSeriesObjectWithAdhocRegistration', 'MeetingSeriesObjectWithAdhocTelephony', 'MeetingSessionTypeObject', 'MeetingSessionTypeObjectType', 'MeetingTrackingCodesObject', 'MeetingTrackingCodesObjectInputMode', 'MeetingTrackingCodesObjectService', 'MeetingTrackingCodesObjectType', 'OptionsForTrackingCodeObject', 'QueryRegistrants', 'QueryRegistrantsOrderBy', 'QueryRegistrantsOrderType', 'QuestionObject', 'QuestionObjectType', 'QuestionOptionObject', 'QuestionWithAnswersObject', 'ReassignMeetingErrorDescriptionObject', 'ReassignMeetingRequestObject', 'ReassignMeetingResponseObject', 'ReassignMeetingsToANewHostResponse', 'Registrant', 'RegistrantCreateResponse', 'RegistrantFormObject', 'RegistrantStatus', 'Registrants', 'Registration', 'RegistrationForUpdate', 'ScheduledMeetingObject', 'StandardRegistrationApproveRule', 'StandardRegistrationApproveRuleQuestion', 'SurveyLinkObject', 'SurveyLinkRequestObject', 'SurveyObject', 'SurveyResultObject', 'TemplateObject', 'TemplateObjectTemplateType', 'TrackingCodeItemForCreateMeetingObject', 'UpdateInterpreterObject', 'UpdateMeetingBreakoutSessionsObject', 'UpdateMeetingObject']


class InviteeObjectForCreateMeeting(ApiModel):
    #: Email address of meeting invitee.
    #: example: brenda.song@example.com
    email: Optional[str] = None
    #: Display name of meeting invitee. The maximum length of `displayName` is 128 characters. If not specified but the email has been registered, user's registered name for the email will be taken as `displayName`. If not specified and the email hasn't been registered, the email will be taken as `displayName`.
    #: example: Brenda Song
    display_name: Optional[str] = None
    #: Whether or not invitee is allowed to be a cohost for the meeting. `coHost` for each invitee is `true` by default if `roomId` is specified when creating a meeting, and anyone in the invitee list that is not qualified to be a cohost will be invited as a non-cohost invitee.
    co_host: Optional[bool] = None
    #: Whether or not an invitee is allowed to be a panelist. Only applies to webinars.
    panelist: Optional[bool] = None


class InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting(ApiModel):
    #: Unique identifier for meeting interpreter.
    #: example: OGQ0OGRiM2U3ZTAxNDZiMGFjYzJjMzYxNDNmNGZhN2RfZTA5MTJiZDBjNWVlNDA4YjgxMTZlMjU4Zjg2NWIzZmM
    id: Optional[str] = None
    #: Forms a set of simultaneous interpretation channels together with `languageCode2`. Standard language format from [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) code. Read [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for details.
    #: example: en
    language_code1: Optional[str] = None
    #: Forms a set of simultaneous interpretation channels together with `languageCode1`. Standard language format from [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) code. Read [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for details.
    #: example: de
    language_code2: Optional[str] = None
    #: Email address of meeting interpreter.
    #: example: marcus.hoffmann@example.com
    email: Optional[str] = None
    #: Display name of meeting interpreter.
    #: example: Hoffmann
    display_name: Optional[str] = None


class InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting(ApiModel):
    #: Forms a set of simultaneous interpretation channels together with `languageCode2`. Standard language format from [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) code. Read [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for details.
    #: example: en
    language_code1: Optional[str] = None
    #: Forms a set of simultaneous interpretation channels together with `languageCode1`. Standard language format from [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) code. Read [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for details.
    #: example: de
    language_code2: Optional[str] = None
    #: Email address of meeting interpreter.
    #: example: marcus.hoffmann@example.com
    email: Optional[str] = None
    #: Display name of meeting interpreter.
    #: example: Hoffmann
    display_name: Optional[str] = None


class MeetingSeriesObjectMeetingType(str, Enum):
    #: Primary instance of a scheduled series of meetings which consists of one or more scheduled meetings based on a `recurrence` rule. When a non-recurring meeting is scheduled with no `recurrence`, its `meetingType` is also `meetingSeries` which is a meeting series with only one occurrence in Webex meeting modeling.
    meeting_series = 'meetingSeries'
    #: Instance from a primary meeting series.
    scheduled_meeting = 'scheduledMeeting'
    #: Meeting instance that is in progress or has completed.
    meeting = 'meeting'


class MeetingSeriesObjectState(str, Enum):
    #: Only applies to a meeting series. Indicates that one or more future scheduled meetings exist for this meeting series.
    active = 'active'
    #: Only applies to scheduled meeting. Indicates that the meeting is scheduled in the future.
    scheduled = 'scheduled'
    #: Only applies to scheduled meeting. Indicates that this scheduled meeting is ready to start or join immediately.
    ready = 'ready'
    #: Only applies to meeting instances. Indicates that a locked meeting has been joined by participants, but no hosts have joined.
    lobby = 'lobby'
    #: Applies to meeting series and meeting instances. For a meeting series, indicates that an instance of this series is happening now. For a meeting instance, indicates that the meeting has been joined and unlocked.
    in_progress = 'inProgress'
    #: Applies to scheduled meetings and meeting instances. For scheduled meetings, indicates that the meeting was started and is now over. For meeting instances, indicates that the meeting instance has concluded.
    ended = 'ended'
    #: This state only applies to scheduled meetings. Indicates that the meeting was scheduled in the past but never happened.
    missed = 'missed'
    #: This state only applies to a meeting series. Indicates that all scheduled meetings of this series have passed.
    expired = 'expired'


class MeetingSeriesObjectUnlockedMeetingJoinSecurity(str, Enum):
    #: If the value of `unlockedMeetingJoinSecurity` attribute is `allowJoin`, people can join the unlocked meeting directly.
    allow_join = 'allowJoin'
    #: If the value of `unlockedMeetingJoinSecurity` attribute is `allowJoinWithLobby`, people will wait in the lobby until the host admits them.
    allow_join_with_lobby = 'allowJoinWithLobby'
    #: If the value of `unlockedMeetingJoinSecurity` attribute is `blockFromJoin`, people can't join the unlocked meeting.
    block_from_join = 'blockFromJoin'


class MeetingSeriesObjectScheduledType(str, Enum):
    #: If the value of `scheduledType` attribute is `meeting`, it is a regular meeting.
    meeting = 'meeting'
    #: If the value of `scheduledType` attribute is `webinar`, it is a webinar meeting.
    webinar = 'webinar'
    #: If the value of `scheduledType` attribute is `personalRoomMeeting`, it is a meeting scheduled in the user's [personal room](https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings).
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
    #: Link relation describing how the target resource is related to the current context (conforming with [RFC5998](https://tools.ietf.org/html/rfc5988)).
    #: example: globalCallinNumbers
    rel: Optional[str] = None
    #: Target resource URI (conforming with [RFC5998](https://tools.ietf.org/html/rfc5988)).
    #: example: /api/v1/meetings/2c87cf8ece4e414a9fe5516e4a0aac76/globalCallinNumbers
    href: Optional[str] = None
    #: Target resource method (conforming with [RFC5998](https://tools.ietf.org/html/rfc5988)).
    #: example: GET
    method: Optional[str] = None


class MeetingSeriesObjectTelephony(ApiModel):
    #: Code for authenticating a user to join teleconference. Users join the teleconference using the call-in number or the global call-in number, followed by the value of the `accessCode`.
    #: example: 1234567890
    access_code: Optional[str] = None
    #: Array of call-in numbers for joining a teleconference from a phone.
    call_in_numbers: Optional[list[MeetingSeriesObjectTelephonyCallInNumbers]] = None
    #: [HATEOAS](https://en.wikipedia.org/wiki/HATEOAS) information of global call-in numbers for joining a teleconference from a phone.
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
    #: Whether or not to allow any attendee to poll in the meeting. Can only be set `true` for a webinar. The value of this attribute depends on the session type for a meeting. Please contact your site admin if this attribute is not available.
    enabled_polling: Optional[bool] = None
    #: Whether or not to allow any attendee to take notes in the meeting. The value of this attribute also depends on the session type.
    #: example: True
    enabled_note: Optional[bool] = None
    #: Whether note taking is enabled. If the value of `enabledNote` is false, users can not set this attribute and get default value `allowAll`.
    #: example: allowAll
    note_type: Optional[MeetingSeriesObjectMeetingOptionsNoteType] = None
    #: Whether or not to allow any attendee to have closed captions in the meeting. The value of this attribute also depends on the session type.
    enabled_closed_captions: Optional[bool] = None
    #: Whether or not to allow any attendee to transfer files in the meeting. The value of this attribute also depends on the session type.
    enabled_file_transfer: Optional[bool] = None
    #: Whether or not to allow any attendee to share [Universal Communications Format](https://www.cisco.com/c/en/us/td/docs/collaboration/training_center/wbs30/WebEx_BK_TE1FB6C1_00_training-center-frequently-asked-questions/WebEx_BK_TE1FB6C1_00_training-center-frequently-asked-questions_chapter_0110.pdf) media files in the meeting. The value of this attribute also depends on the sessionType.
    enabled_ucfrich_media: Optional[bool] = Field(alias='enabledUCFRichMedia', default=None)


class MeetingSeriesObjectAttendeePrivileges(ApiModel):
    #: Whether or not to allow any attendee to share content in the meeting.
    #: example: True
    enabled_share_content: Optional[bool] = None
    #: Whether or not to allow any attendee to save shared documents, slides, or whiteboards when they are shared as files in the content viewer instead of in a window or application.
    enabled_save_document: Optional[bool] = None
    #: Whether or not to allow any attendee to print shared documents, slides, or whiteboards when they are shared as files in the content viewer instead of in a window or application.
    enabled_print_document: Optional[bool] = None
    #: Whether or not to allow any attendee to annotate shared documents, slides, or whiteboards when they are shared as files in the content viewer instead of in a window or application.
    enabled_annotate: Optional[bool] = None
    #: Whether or not to allow any attendee to view participants.
    #: example: True
    enabled_view_participant_list: Optional[bool] = None
    #: Whether or not to allow any attendee to see a small preview image of any page of shared documents or slides when they are shared as files in the content viewer instead of in a window or application.
    enabled_view_thumbnails: Optional[bool] = None
    #: Whether or not to allow any attendee to control applications, web browsers, or desktops remotely.
    #: example: True
    enabled_remote_control: Optional[bool] = None
    #: Whether or not to allow any attendee to view any shared documents or slides when they are shared as files in the content viewer instead of in a window or application.
    enabled_view_any_document: Optional[bool] = None
    #: Whether or not to allow any attendee to scroll through any page of shared documents or slides when they are shared as files in the content viewer instead of in a window or application.
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
    #: example: 1.0
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
    #: The priority number of the approval rule. Approval rules for standard questions and custom questions need to be ordered together.
    #: example: 1.0
    order: Optional[int] = None


class CustomizedQuestionForGetMeeting(ApiModel):
    #: Unique identifier for the question.
    #: example: 330521.0
    id: Optional[int] = None
    #: Title of the customized question.
    #: example: How are you
    question: Optional[str] = None
    #: Whether or not the customized question is required to be answered by participants.
    #: example: True
    required: Optional[bool] = None
    #: Type of the question being asked.
    type: Optional[CustomizedQuestionForCreateMeetingType] = None
    #: The maximum length of a string that can be entered by the user, ranging from `0` to `999`. Only required by `singleLineTextBox` and `multiLineTextBox`.
    max_length: Optional[int] = None
    #: TThe content of `options`. Required if the question type is one of `checkbox`, `dropdownList`, or `radioButtons`.
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
    #: The priority number of the approval rule. Approval rules for standard questions and custom questions need to be ordered together.
    #: example: 1.0
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
    #: Maximum number of meeting registrations. This only applies to meetings. The maximum number of participants for meetings and webinars, with the limit based on the user capacity and controlled by a toggle at the site level. The default maximum number of participants for webinars is 10000, but the actual maximum number of participants is limited by the user capacity.
    #: example: 1000.0
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
    #: Only restricts attendees to join the audio portion of the meeting using their computer instead of a telephone option.
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
    #: Whether or not to allow attendees to receive a call-back and call-in is available. Can only be set `true` for a webinar.
    enabled_audience_call_back: Optional[bool] = None
    #: Select the sound you want users who have a phone audio connection to hear when someone enters or exits the meeting.
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
    #: Unique identifier for meeting. For a meeting series, the `id` is used to identify the entire series. For scheduled meetings from a series, the `id` is used to identify that scheduled meeting. For a meeting instance that is in progress or has concluded, the `id` is used to identify that instance.
    #: example: dfb45ece33264639a7bc3dd9535d53f7_20200516T230000Z
    id: Optional[str] = None
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting instances which have ended.
    #: example: 123456789
    meeting_number: Optional[str] = None
    #: Meeting title. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: John's Meeting
    title: Optional[str] = None
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long. This attribute can be modified for a meeting series or a scheduled meeting using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: John's Agenda
    agenda: Optional[str] = None
    #: Meeting password. Applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: BgJep@43
    password: Optional[str] = None
    #: 8-digit numeric password used to join a meeting from audio and video devices. This attribute applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended.
    #: example: 12345678
    phone_and_video_system_password: Optional[str] = None
    #: Meeting type.
    #: example: meetingSeries
    meeting_type: Optional[MeetingSeriesObjectMeetingType] = None
    #: Meeting state.
    #: example: active
    state: Optional[MeetingSeriesObjectState] = None
    #: [Time zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) of `start` and `end`, conforming with the [IANA time zone database](https://www.iana.org/time-zones).
    #: example: UTC
    timezone: Optional[str] = None
    #: Start time for meeting in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format. If the meeting is a meeting series, `start` is the date and time the first meeting of the series starts. If the meeting is a meeting series and the `current` filter is true, `start` is the date and time the upcoming or ongoing meeting of the series starts. If the meeting is a scheduled meeting from a meeting series, `start` is the date and time when that scheduled meeting starts. If the meeting is a meeting instance that has happened or is happening, `start` is the date and time that the instance actually starts. Can be modified for a meeting series or a scheduled meeting using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: 2019-03-18T11:26:30Z
    start: Optional[datetime] = None
    #: End time for a meeting in ISO 8601 compliant format. If the meeting is a meeting series, `end` is the date and time the first meeting of the series ends. If the meeting is a meeting series and the current filter is true, `end` is the date and time the upcoming or ongoing meeting of the series ends. If the meeting is a scheduled meeting from a meeting series, `end` is the date and time when that scheduled meeting ends. If the meeting is a meeting instance that has happened, `end` is the date and time that instance actually ends. If a meeting instance is in progress, `end` is not available. Can be modified for a meeting series or a scheduled meeting using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: 2019-03-18T12:26:30Z
    end: Optional[datetime] = None
    #: Meeting series recurrence rule (conforming with [RFC 2445](https://www.ietf.org/rfc/rfc2445.txt)). Applies only to a recurring meeting series, not to a meeting series with only one scheduled meeting. Can be modified for a meeting series using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API. Multiple days or dates for monthly or yearly `recurrence` rule are not supported, only the first day or date specified is taken. For example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10". For a non-recurring meeting which has no `recurrence`, its `meetingType` is also `meetingSeries` which is a meeting series with only one occurrence in Webex meeting modeling.
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
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or join.
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
    #: Whether or not meeting is recorded automatically. Can be modified for a meeting series or a scheduled meeting using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    enabled_auto_record_meeting: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the meeting. The target site is specified by a `siteUrl` parameter when creating the meeting. If not specified, it's a user's preferred site. The `allowAnyUserToBeCoHost` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    allow_any_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The `enabledJoinBeforeHost` attribute can be modified for a meeting series or a scheduled meeting using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    enabled_join_before_host: Optional[bool] = None
    #: Whether or not to allow any attendee to connect to audio before the host joins the meeting. Only applicable if the `enabledJoinBeforeHost` attribute is set to `true`. The `enableConnectAudioBeforeHost` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    enable_connect_audio_before_host: Optional[bool] = None
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. Only applicable if the `enabledJoinBeforeHost` attribute is set to true. The `joinBeforeHostMinutes` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API. Valid options for a meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`, `45`, and `60`. The default is `0` if not specified.
    #: example: 15.0
    join_before_host_minutes: Optional[int] = None
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool] = None
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool] = None
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    #: example: 10.0
    reminder_time: Optional[int] = None
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    #: example: allowJoin
    unlocked_meeting_join_security: Optional[MeetingSeriesObjectUnlockedMeetingJoinSecurity] = None
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar meeting. All available meeting session types enabled for the user can be retrieved using the [List Meeting Session Types](/docs/api/v1/meetings/list-meeting-session-types) API.
    #: example: 3.0
    session_type_id: Optional[int] = None
    #: Specifies whether the meeting is a regular meeting, a webinar, or a meeting scheduled in the user's [personal room](https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings).
    #: example: meeting
    scheduled_type: Optional[MeetingSeriesObjectScheduledType] = None
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool] = None
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read [password management](https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration) for details. If not specified, a random password conforming to the site's password rules will be generated automatically.
    #: example: GwLqa@78
    panelist_password: Optional[str] = None
    #: 8-digit numeric panelist password to join a webinar meeting from audio and video devices.
    #: example: 12345678
    phone_and_video_system_panelist_password: Optional[str] = None
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool] = None
    #: The number of minutes after the meeting begins, for automatically locking it.
    #: example: 10.0
    automatic_lock_minutes: Optional[int] = None
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a cohost. The target site is specified by the `siteUrl` parameter when creating the meeting. If not specified, it's a user's preferred site. The `allowFirstUserToBeCoHost` attribute can be modified for a meeting series or a scheduled meeting uisng the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting without a prompt. This attribute can be modified for a meeting series or a scheduled meeting using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    allow_authenticated_devices: Optional[bool] = None
    #: Information for callbacks from a meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[MeetingSeriesObjectTelephony] = None
    #: Meeting Options.
    meeting_options: Optional[MeetingSeriesObjectMeetingOptions] = None
    #: Attendee Privileges. This attribute is not supported for a webinar.
    attendee_privileges: Optional[MeetingSeriesObjectAttendeePrivileges] = None
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information in order to join the meeting. Meeting invitees will receive an email with a registration link for the registration. When the registration form has been submitted and approved, an email with a real meeting link will be received. By clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not apply to a meeting when it's a recurring meeting with a `recurrence` field or no `password` or when the feature toggle `DecoupleJBHWithRegistration` is disabled the `Join Before Host` option is enabled for the meeting, See [Register for a Meeting in Cisco Webex Meetings](https://help.webex.com/en-us/nmgmeff/Register-for-a-Meeting-in-Cisco-Webex-Meetings) for details.
    registration: Optional[MeetingSeriesObjectRegistration] = None
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc.
    integration_tags: Optional[list[str]] = None
    #: Simultaneous interpretation information for a meeting.
    simultaneous_interpretation: Optional[MeetingSeriesObjectSimultaneousInterpretation] = None
    #: Whether or not breakout sessions are enabled.
    enabled_breakout_sessions: Optional[bool] = None
    #: [HATEOAS](https://en.wikipedia.org/wiki/HATEOAS) Breakout Sessions information for meeting.
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
    #: Code for authenticating a user to join teleconference. Users join the teleconference using the call-in number or the global call-in number, followed by the value of the `accessCode`.
    #: example: 1234567890
    access_code: Optional[str] = None
    #: Array of call-in numbers for joining a teleconference from a phone.
    call_in_numbers: Optional[list[MeetingSeriesObjectTelephonyCallInNumbers]] = None
    #: [HATEOAS](https://en.wikipedia.org/wiki/HATEOAS) information of global call-in numbers for joining a teleconference from a phone.
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
    #: Maximum number of meeting registrations. This only applies to meetings. The maximum number of participants for meetings and webinars, with the limit based on the user capacity and controlled by a toggle at the site level. The default maximum number of participants for webinars is 10000, but the actual maximum number of participants is limited by the user capacity.
    #: example: 1000.0
    max_register_num: Optional[int] = None


class MeetingSeriesObjectWithAdhoc(ApiModel):
    #: Unique identifier for meeting. For a meeting series, the `id` is used to identify the entire series. For scheduled meetings from a series, the `id` is used to identify that scheduled meeting. For a meeting instance that is in progress or has concluded, the `id` is used to identify that instance.
    #: example: dfb45ece33264639a7bc3dd9535d53f7_20200516T230000Z
    id: Optional[str] = None
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting instances which have ended.
    #: example: 123456789
    meeting_number: Optional[str] = None
    #: Meeting title. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: John's Meeting
    title: Optional[str] = None
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long. This attribute can be modified for a meeting series or a scheduled meeting using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: John's Agenda
    agenda: Optional[str] = None
    #: Meeting password. Applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: BgJep@43
    password: Optional[str] = None
    #: 8-digit numeric password used to join a meeting from audio and video devices. This attribute applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended.
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
    #: [Time zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) of `start` and `end`, conforming with the [IANA time zone database](https://www.iana.org/time-zones).
    #: example: UTC
    timezone: Optional[str] = None
    #: Start time for meeting in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format. If the meetingType of this meeting is `meetingSeries`, and `current` is not specified or is `false`, `start` is the scheduled start time of the first occurrence of this series. If the meetingType of this meeting is `meetingSeries`, and `current` is not specified or is `false`, `start` is the scheduled start time of the first occurrence of this series. If the meetingType of this meeting is `meetingSeries`, and `current` is `true`, `start` is the scheduled start time of the ongoing or upcoming occurrence in this series. If the meetingType of this meeting is `scheduledMeeting`, `start` is the scheduled start time of this occurrence. If the meetingType of this meeting is `meeting`, `start` is the actual start time of this meeting instance. Can be modified for a meeting series or a scheduled meeting using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: 2019-03-18T11:26:30Z
    start: Optional[datetime] = None
    #: End time for a meeting in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format. If the meeting is a meeting series, `end` is the date and time the first meeting of the series ends. If the meetingType of this meeting is `meetingSeries`, and `current` is not specified or is `false`, `end` is the scheduled end time of the first occurrence of this series. If the meetingType of this meeting is `meetingSeries`, and `current` is `true`, `end` is the scheduled end time of the ongoing or upcoming occurrence in this series. If the meetingType of this meeting is `scheduledMeeting`, `end` is the scheduled end time of this occurrence. If the meetingType of this meeting is `meeting`, `end` is the actual end time of this meeting instance. Can be modified for a meeting series or a scheduled meeting using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: 2019-03-18T12:26:30Z
    end: Optional[datetime] = None
    #: Meeting series recurrence rule (conforming with [RFC 2445](https://www.ietf.org/rfc/rfc2445.txt)). Applies only to a recurring meeting series, not to a meeting series with only one scheduled meeting. Can be modified for a meeting series using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API. Multiple days or dates for monthly or yearly `recurrence` rule are not supported, only the first day or date specified is taken. For example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
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
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or join.
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
    #: Whether or not meeting is recorded automatically. Can be modified for a meeting series or a scheduled meeting using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    enabled_auto_record_meeting: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the meeting. The target site is specified by a `siteUrl` parameter when creating the meeting. If not specified, it's a user's preferred site. The `allowAnyUserToBeCoHost` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    allow_any_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The `enabledJoinBeforeHost` attribute can be modified for a meeting series or a scheduled meeting using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    enabled_join_before_host: Optional[bool] = None
    #: Whether or not to allow any attendee to connect to audio before the host joins the meeting. Only applicable if the `enabledJoinBeforeHost` attribute is set to `true`. The `enableConnectAudioBeforeHost` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    enable_connect_audio_before_host: Optional[bool] = None
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. Only applicable if the `enabledJoinBeforeHost` attribute is set to true. The `joinBeforeHostMinutes` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API. Valid options for a meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`, `45`, and `60`. The default is `0` if not specified.
    #: example: 15.0
    join_before_host_minutes: Optional[int] = None
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool] = None
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool] = None
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    #: example: 10.0
    reminder_time: Optional[int] = None
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    #: example: allowJoin
    unlocked_meeting_join_security: Optional[MeetingSeriesObjectUnlockedMeetingJoinSecurity] = None
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar meeting. All available meeting session types enabled for the user can be retrieved using the [List Meeting Session Types](/docs/api/v1/meetings/list-meeting-session-types) API.
    #: example: 3.0
    session_type_id: Optional[int] = None
    #: Specifies whether the meeting is a regular meeting, a webinar, or a meeting scheduled in the user's [personal room](https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings).
    #: example: meeting
    scheduled_type: Optional[MeetingSeriesObjectScheduledType] = None
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool] = None
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read [password management](https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration) for details. If not specified, a random password conforming to the site's password rules will be generated automatically.
    #: example: GwLqa@78
    panelist_password: Optional[str] = None
    #: 8-digit numeric panelist password to join a webinar meeting from audio and video devices.
    #: example: 12345678
    phone_and_video_system_panelist_password: Optional[str] = None
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool] = None
    #: The number of minutes after the meeting begins, for automatically locking it.
    #: example: 10.0
    automatic_lock_minutes: Optional[int] = None
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a cohost. The target site is specified by the `siteUrl` parameter when creating the meeting. If not specified, it's a user's preferred site. The `allowFirstUserToBeCoHost` attribute can be modified for a meeting series or a scheduled meeting uisng the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting without a prompt. This attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
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
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information in order to join the meeting. Meeting invitees will receive an email with a registration link for the registration. When the registration form has been submitted and approved, an email with a real meeting link will be received. By clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not apply to a meeting when it's a recurring meeting with a `recurrence` field or no password, or the `Join Before Host` option is enabled for the meeting. See [Register for a Meeting in Cisco Webex Meetings](https://help.webex.com/en-us/nmgmeff/Register-for-a-Meeting-in-Cisco-Webex-Meetings) for details.
    registration: Optional[MeetingSeriesObjectWithAdhocRegistration] = None
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc.
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
    #: Unique identifier for meeting. For a meeting series, the `id` is used to identify the entire series. For scheduled meetings from a series, the `id` is used to identify that scheduled meeting. For a meeting instance that is in progress or has concluded, the `id` is used to identify that instance.
    #: example: dfb45ece33264639a7bc3dd9535d53f7_20200516T230000Z
    id: Optional[str] = None
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting instances which have ended.
    #: example: 123456789
    meeting_number: Optional[str] = None
    #: Meeting title. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: John's Meeting
    title: Optional[str] = None
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long. This attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: John's Agenda
    agenda: Optional[str] = None
    #: Meeting password. Applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: BgJep@43
    password: Optional[str] = None
    #: 8-digit numeric password used to join a meeting from audio and video devices. This attribute applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended.
    #: example: 12345678
    phone_and_video_system_password: Optional[str] = None
    #: Meeting type.
    #: example: meetingSeries
    meeting_type: Optional[MeetingSeriesObjectMeetingType] = None
    #: Meeting state.
    #: example: active
    state: Optional[MeetingSeriesObjectState] = None
    #: Time zone of `start` and `end`, conforming with the [IANA time zone database](https://www.iana.org/time-zones).
    #: example: UTC
    timezone: Optional[str] = None
    #: Start time for meeting in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format. If the meetingType of a meeting is `meetingSeries`, `start` is the scheduled start time of the first occurrence of this series. If the meeting is a meeting series and the `current` filter is true, `start` is the date and time the upcoming or ongoing meeting of the series starts. If the meetingType of a meeting is `scheduledMeeting`, `start` is the scheduled start time of this occurrence. If the meetingType of a meeting is `meeting`, `start` is the actual start time of the meeting instance. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: 2019-03-18T11:26:30Z
    start: Optional[datetime] = None
    #: End time for a meeting in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format. If the meetingType of a meeting is `meetingSeries`, `end` is the scheduled end time of the first occurrence of this series. If the meeting is a meeting series and the current filter is true, `end` is the date and time the upcoming or ongoing meeting of the series ends. If the meetingType of a meeting is `scheduledMeeting`, `end` is the scheduled end time of this occurrence. If the meetingType of a meeting is `meeting`, `end` is the actual end time of the meeting instance. If a meeting instance is in progress, `end` is not available. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: 2019-03-18T12:26:30Z
    end: Optional[datetime] = None
    #: Meeting series recurrence rule (conforming with [RFC 2445](https://www.ietf.org/rfc/rfc2445.txt)). Applies only to a recurring meeting series, not to a meeting series with only one scheduled meeting. Can be modified for a meeting series using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API. Multiple days or dates for monthly or yearly `recurrence` rule are not supported, only the first day or date specified is taken. For example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
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
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or join.
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
    #: Whether or not meeting is recorded automatically. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    enabled_auto_record_meeting: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the meeting. The target site is specified by a `siteUrl` parameter when creating the meeting. If not specified, it's a user's preferred site. The `allowAnyUserToBeCoHost` attribute can be modified for a meeting series or a scheduled meeting using the  [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    allow_any_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The `enabledJoinBeforeHost` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    enabled_join_before_host: Optional[bool] = None
    #: Whether or not to allow any attendee to connect to audio before the host joins the meeting. Only applicable if the `enabledJoinBeforeHost` attribute is set to `true`. The `enableConnectAudioBeforeHost` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    enable_connect_audio_before_host: Optional[bool] = None
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. Only applicable if the `enabledJoinBeforeHost` attribute is set to true. The `joinBeforeHostMinutes` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API. Valid options for a meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`, `45`, and `60`. The default is `0` if not specified.
    #: example: 15.0
    join_before_host_minutes: Optional[int] = None
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool] = None
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool] = None
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    #: example: 10.0
    reminder_time: Optional[int] = None
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    #: example: allowJoin
    unlocked_meeting_join_security: Optional[MeetingSeriesObjectUnlockedMeetingJoinSecurity] = None
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar meeting. All available meeting session types enabled for the user can be retrieved using the [List Meeting Session Types](/docs/api/v1/meetings/list-meeting-session-types) API.
    #: example: 3.0
    session_type_id: Optional[int] = None
    #: Specifies whether the meeting is a regular meeting, a webinar, or a meeting scheduled in the user's [personal room](https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings).
    #: example: meeting
    scheduled_type: Optional[MeetingSeriesObjectScheduledType] = None
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool] = None
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read [password management](https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration) for details. If not specified, a random password conforming to the site's password rules will be generated automatically.
    #: example: GwLqa@78
    panelist_password: Optional[str] = None
    #: 8-digit numeric panelist password to join a webinar meeting from audio and video devices.
    #: example: 12345678
    phone_and_video_system_panelist_password: Optional[str] = None
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool] = None
    #: The number of minutes after the meeting begins, for automatically locking it.
    #: example: 10.0
    automatic_lock_minutes: Optional[int] = None
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a cohost. The target site is specified by the `siteUrl` parameter when creating the meeting. If not specified, it's a user's preferred site. The `allowFirstUserToBeCoHost` attribute can be modified for a meeting series or a scheduled meeting uisng the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting without a prompt. This attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
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
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information in order to join the meeting. Meeting invitees will receive an email with a registration link for the registration. When the registration form has been submitted and approved, an email with a real meeting link will be received. By clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not apply to a meeting when it's a recurring meeting with a `recurrence` field or no password, or the `Join Before Host` option is enabled for the meeting. See [Register for a Meeting in Cisco Webex Meetings](https://help.webex.com/en-us/nmgmeff/Register-for-a-Meeting-in-Cisco-Webex-Meetings) for details.
    registration: Optional[MeetingSeriesObjectWithAdhocRegistration] = None
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc.
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
    #: Unique identifier for meeting. For a meeting series, the `id` is used to identify the entire series. For scheduled meetings from a series, the `id` is used to identify that scheduled meeting. For a meeting instance that is in progress or has concluded, the `id` is used to identify that instance.
    #: example: dfb45ece33264639a7bc3dd9535d53f7_20200516T230000Z
    id: Optional[str] = None
    #: Unique identifier for meeting series. It only apples to scheduled meeting and meeting instance. If it's a scheduled meeting from a series or a meeting instance that is happening or has happened, the `meetingSeriesId` is the `id` of the primary series.
    #: example: dfb45ece33264639a7bc3dd9535d53f7
    meeting_series_id: Optional[str] = None
    #: Unique identifier for scheduled meeting which current meeting is associated with. It only apples to meeting instance which is happening or has happened. It's the `id` of the scheduled meeting this instance is associated with.
    #: example: dfb45ece33264639a7bc3dd9535d53f7
    scheduled_meeting_id: Optional[str] = None
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting instances which have ended.
    #: example: 123456789
    meeting_number: Optional[str] = None
    #: Meeting title. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: John's Meeting
    title: Optional[str] = None
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long. This attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: John's Agenda
    agenda: Optional[str] = None
    #: Meeting password. Applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: BgJep@43
    password: Optional[str] = None
    #: 8-digit numeric password used to join a meeting from audio and video devices. This attribute applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended.
    #: example: 12345678
    phone_and_video_system_password: Optional[str] = None
    #: Meeting type.
    #: example: scheduledMeeting
    meeting_type: Optional[MeetingSeriesObjectMeetingType] = None
    #: Meeting state.
    #: example: scheduled
    state: Optional[MeetingSeriesObjectState] = None
    #: This state only applies to scheduled meeting. Flag identifying whether or not the scheduled meeting has been modified.
    is_modified: Optional[bool] = None
    #: [Time zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) of `start` and `end`, conforming with the [IANA time zone database](https://www.iana.org/time-zones).
    #: example: UTC
    timezone: Optional[str] = None
    #: Start time for meeting in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format. If the meetingType of a meeting is `meetingSeries`, `start` is the scheduled start time of the first occurrence of this series. If the meeting is a meeting series and the `current` filter is true, `start` is the date and time the upcoming or ongoing meeting of the series starts. If the meetingType of a meeting is `scheduledMeeting`, `start` is the scheduled start time of this occurrence. If the meetingType of a meeting is `meeting`, `start` is the actual start time of the meeting instance. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    #: example: 2019-03-18T11:26:30Z
    start: Optional[datetime] = None
    #: End time for a meeting in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format. If the meetingType of a meeting is `meetingSeries`, `end` is the scheduled end time of the first occurrence of this series. If the meeting is a meeting series and the current filter is true, `end` is the date and time the upcoming or ongoing meeting of the series ends. If the meetingType of a meeting is `scheduledMeeting`, `end` is the scheduled end time of this occurrence. If the meetingType of a meeting is `meeting`, `end` is the actual end time of the meeting instance. If a meeting instance is in progress, `end` is not available. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
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
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or join.
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
    #: Whether or not meeting is recorded automatically. Can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    enabled_auto_record_meeting: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the meeting. The target site is specified by a `siteUrl` parameter when creating the meeting. If not specified, it's a user's preferred site. The `allowAnyUserToBeCoHost` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    allow_any_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The `enabledJoinBeforeHost` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    enabled_join_before_host: Optional[bool] = None
    #: Whether or not to allow any attendee to connect to audio before the host joins the meeting. Only applicable if the `enabledJoinBeforeHost` attribute is set to `true`. The `enableConnectAudioBeforeHost` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    enable_connect_audio_before_host: Optional[bool] = None
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. Only applicable if the `enabledJoinBeforeHost` attribute is set to true. The `joinBeforeHostMinutes` attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API. Valid options for a meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`, `45`, and `60`. The default is `0` if not specified.
    #: example: 15.0
    join_before_host_minutes: Optional[int] = None
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool] = None
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool] = None
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    #: example: 10.0
    reminder_time: Optional[int] = None
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    #: example: allowJoin
    unlocked_meeting_join_security: Optional[MeetingSeriesObjectUnlockedMeetingJoinSecurity] = None
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar meeting. All available meeting session types enabled for the user can be retrieved using the [List Meeting Session Types](/docs/api/v1/meetings/list-meeting-session-types) API.
    #: example: 3.0
    session_type_id: Optional[int] = None
    #: Specifies whether the meeting is a regular meeting, a webinar, or a meeting scheduled in the user's [personal room](https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings).
    #: example: meeting
    scheduled_type: Optional[MeetingSeriesObjectScheduledType] = None
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool] = None
    #: Password for panelists of webinar meeting. Must conform to the site's password complexity settings. Read [password management](https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration) for details. If not specified, a random password conforming to the site's password rules will be generated automatically.
    #: example: GwLqa@78
    panelist_password: Optional[str] = None
    #: 8-digit numeric panelist password to join webinar meeting from audio and video devices.
    #: example: 12345678
    phone_and_video_system_panelist_password: Optional[str] = None
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool] = None
    #: The number of minutes after the meeting begins, for automatically locking it.
    #: example: 10.0
    automatic_lock_minutes: Optional[int] = None
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a cohost. The target site is specified by the `siteUrl` parameter when creating the meeting. If not specified, it's a user's preferred site. The `allowFirstUserToBeCoHost` attribute can be modified for a meeting series or a scheduled meeting uisng the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting without a prompt. This attribute can be modified for a meeting series or a scheduled meeting using the [Update a Meeting](/docs/api/v1/meetings/update-a-meeting) API.
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
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information in order to join the meeting. Meeting invitees will receive an email with a registration link for the registration. When the registration form has been submitted and approved, an email with a real meeting link will be received. By clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not apply to a meeting when it's a recurring meeting with a `recurrence` field or no `password` or when the feature toggle `DecoupleJBHWithRegistration` is disabled the `Join Before Host` option is enabled for the meeting, See [Register for a Meeting in Cisco Webex Meetings](https://help.webex.com/en-us/nmgmeff/Register-for-a-Meeting-in-Cisco-Webex-Meetings) for details.
    registration: Optional[MeetingSeriesObjectWithAdhocRegistration] = None
    #: External keys created by an integration application in its domain, for example, Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc.
    integration_tags: Optional[list[str]] = None
    #: Whether or not breakout sessions are enabled.
    enabled_breakout_sessions: Optional[bool] = None
    #: [HATEOAS](https://en.wikipedia.org/wiki/HATEOAS) Breakout Sessions information for meeting.
    links: Optional[list[LinksObjectForTelephony]] = None
    #: Tracking codes information.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]] = None
    #: Audio connection options.
    audio_connection_options: Optional[MeetingSeriesObjectAudioConnectionOptions] = None
    #: Require attendees to sign in before joining the webinar.
    require_attendee_login: Optional[bool] = None
    #: Restrict webinar to invited attendees only.
    restrict_to_invitees: Optional[bool] = None


class UpdateMeetingObject(ApiModel):
    #: Meeting title. The title can be a maximum of 128 characters long.
    #: example: John's Meeting
    title: Optional[str] = None
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long.
    #: example: John's Agenda
    agenda: Optional[str] = None
    #: Meeting password. Must conform to the site's password complexity settings. Read [password management](https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration) for details.
    #: example: BgJep@43
    password: Optional[str] = None
    #: Date and time for the start of meeting in any [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format. `start` cannot be before current date and time or after `end`. Duration between `start` and `end` cannot be shorter than 10 minutes or longer than 24 hours. Refer to the [Webex Meetings](/docs/meetings#restrictions-on-updating-a-meeting) guide for more information about restrictions on updating date and time for a meeting. Please note that when a meeting is being updated, `start` of the meeting will be accurate to minutes, not seconds or milliseconds. Therefore, if `start` is within the same minute as the current time, `start` will be adjusted to the upcoming minute; otherwise, `start` will be adjusted with seconds and milliseconds stripped off. For instance, if the current time is `2022-03-01T10:32:16.657+08:00`, `start` of `2022-03-01T10:32:28.076+08:00` or `2022-03-01T10:32:41+08:00` will be adjusted to `2022-03-01T10:33:00+08:00`, and `start` of `2022-03-01T11:32:28.076+08:00` or `2022-03-01T11:32:41+08:00` will be adjusted to `2022-03-01T11:32:00+08:00`.
    #: example: 2020-05-15T20:30:00-08:00
    start: Optional[datetime] = None
    #: Date and time for the end of meeting in any [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format. `end` cannot be before current date and time or before `start`. Duration between `start` and `end` cannot be shorter than 10 minutes or longer than 24 hours. Refer to the [Webex Meetings](/docs/meetings#restrictions-on-updating-a-meeting) guide for more information about restrictions on updating date and time for a meeting. Please note that when a meeting is being updated, `end` of the meeting will be accurate to minutes, not seconds or milliseconds. Therefore, `end` will be adjusted with seconds and milliseconds stripped off. For instance, `end` of `2022-03-01T11:52:28.076+08:00` or `2022-03-01T11:52:41+08:00` will be adjusted to `2022-03-01T11:52:00+08:00`.
    #: example: 2020-05-15T21:30:00-08:00
    end: Optional[datetime] = None
    #: [Time zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) in which the meeting was originally scheduled (conforming with the [IANA time zone database](https://www.iana.org/time-zones)).
    #: example: America/Los_Angeles
    timezone: Optional[str] = None
    #: Meeting series recurrence rule (conforming with [RFC 2445](https://www.ietf.org/rfc/rfc2445.txt)). Applies only to a recurring meeting series, not to a meeting series with only one scheduled meeting. Multiple days or dates for monthly or yearly `recurrence` rule are not supported, only the first day or date specified is taken. For example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
    #: example: FREQ=DAILY;INTERVAL=1;COUNT=20
    recurrence: Optional[str] = None
    #: Whether or not meeting is recorded automatically.
    enabled_auto_record_meeting: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the meeting. The target site is specified by `siteUrl` parameter when creating the meeting; if not specified, it's user's preferred site.
    allow_any_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting.
    enabled_join_before_host: Optional[bool] = None
    #: Whether or not to allow any attendee to connect audio in the meeting before the host joins the meeting. This attribute is only applicable if the `enabledJoinBeforeHost` attribute is set to true.
    enable_connect_audio_before_host: Optional[bool] = None
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. Only applicable if the `enabledJoinBeforeHost` attribute is set to true. Valid options for a meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`, `45`, and `60`. The default is `0` if not specified.
    #: example: 15.0
    join_before_host_minutes: Optional[int] = None
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool] = None
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool] = None
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    #: example: 30.0
    reminder_time: Optional[int] = None
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    #: example: allowJoin
    unlocked_meeting_join_security: Optional[MeetingSeriesObjectUnlockedMeetingJoinSecurity] = None
    #: Unique identifier for a meeting session type for the user. This attribute is required while scheduling webinar meeting. All available meeting session types enabled for the user can be retrieved by [List Meeting Session Types](/docs/api/v1/meetings/list-meeting-session-types) API.
    #: example: 3.0
    session_type_id: Optional[int] = None
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool] = None
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read [password management](https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration) for details. If not specified, a random password conforming to the site's password rules will be generated automatically.
    #: example: GwLqa@78
    panelist_password: Optional[str] = None
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool] = None
    #: The number of minutes after the meeting begins, for automatically locking it.
    #: example: 10.0
    automatic_lock_minutes: Optional[int] = None
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a cohost. The target site is specified by `siteUrl` parameter when creating the meeting; if not specified, it's user's preferred site.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting without a prompt.
    allow_authenticated_devices: Optional[bool] = None
    #: Whether or not to send emails to host and invitees. It is an optional field and default value is true.
    #: example: True
    send_email: Optional[bool] = None
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API has the admin-level scopes. When used, the admin may specify the email of a user in a site they manage to be the meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: URL of the Webex site which the meeting is updated on. If not specified, the meeting is created on user's preferred site. All available Webex sites and preferred site of the user can be retrieved by `Get Site List` API.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: Meeting Options.
    meeting_options: Optional[MeetingSeriesObjectMeetingOptions] = None
    #: Attendee Privileges. This attribute is not supported for a webinar.
    attendee_privileges: Optional[MeetingSeriesObjectAttendeePrivileges] = None
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries meetings by a key in its own domain. The maximum size of `integrationTags` is 3 and each item of `integrationTags` can be a maximum of 64 characters long. Please note that an empty or null `integrationTags` will delete all existing integration tags for the meeting implicitly. Developer can update integration tags for a `meetingSeries` but he cannot update it for a `scheduledMeeting` or a `meeting` instance.
    integration_tags: Optional[list[str]] = None
    #: Whether or not breakout sessions are enabled. If the value of `enabledBreakoutSessions` is false, users can not set breakout sessions. If the value of `enabledBreakoutSessions` is true, users can update breakout sessions using the [Update Breakout Sessions](/docs/api/v1/meetings/{meetingId}/breakoutSessions) API. Updating breakout sessions are not supported by this API.
    enabled_breakout_sessions: Optional[bool] = None
    #: Tracking codes information. All available tracking codes and their options for the specified site can be retrieved by [List Meeting Tracking Codes](/docs/api/v1/meetings/list-meeting-tracking-codes) API. If an optional tracking code is missing from the `trackingCodes` array and there's a default option for this tracking code, the default option is assigned automatically. If the `inputMode` of a tracking code is `select`, its value must be one of the site-level options or the user-level value. Tracking code is not supported for a personal room meeting or an ad-hoc space meeting.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]] = None
    #: Audio connection options.
    audio_connection_options: Optional[MeetingSeriesObjectAudioConnectionOptions] = None
    #: Require attendees to sign in before joining the webinar. This option works when the value of `scheduledType` attribute is `webinar`. Please note that `requireAttendeeLogin` cannot be set if someone has already registered for the webinar.
    require_attendee_login: Optional[bool] = None
    #: Restrict webinar to invited attendees only. This option works when the registration option is disabled and the value of `scheduledType` attribute is `webinar`. Please note that `restrictToInvitees` cannot be set to `true` if `requireAttendeeLogin` is `false`.
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
    #: The maximum length of a string that can be entered by the user, ranging from `0` to `999`. Only required by `singleLineTextBox` and `multiLineTextBox`.
    max_length: Optional[int] = None
    #: The content of `options`. Required if the question type is one of `checkbox`, `dropdownList`, or `radioButtons`.
    options: Optional[list[CustomizedQuestionForCreateMeetingOptions]] = None
    #: The automatic approval rules for customized questions.
    rules: Optional[list[CustomizedQuestionForCreateMeetingRules]] = None


class CreateMeetingObjectRegistration(ApiModel):
    #: Whether or not meeting registration request is accepted automatically.
    auto_accept_request: Optional[bool] = None
    #: Whether or not a registrant's first name is required for meeting registration. This option must always be `true`.
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
    #: Maximum number of meeting registrations. This only applies to meetings. The maximum number of participants for meetings and webinars, with the limit based on the user capacity and controlled by a toggle at the site level. The default maximum number of participants for webinars is 10000, but the actual maximum number of participants is limited by the user capacity.
    #: example: 1000.0
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
    #: Invitees for breakout session. Please note that one invitee cannot be assigned to more than one breakout session.
    invitees: Optional[list[str]] = None


class CreateMeetingObject(ApiModel):
    #: Whether or not to create an ad-hoc meeting for the room specified by `roomId`. When `true`, `roomId` is required.
    adhoc: Optional[bool] = None
    #: Unique identifier for the Webex space which the meeting is to be associated with. It can be retrieved by [List Rooms](/docs/api/v1/rooms/list-rooms). `roomId` is required when `adhoc` is `true`. When `roomId` is specified, the parameter `hostEmail` will be ignored.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vNDMzZjk0ZjAtOTZhNi0xMWViLWJhOTctOTU3OTNjZDhiY2Q2
    room_id: Optional[str] = None
    #: Unique identifier for meeting template. Please note that `start` and `end` are optional when `templateId` is specified. The list of meeting templates that is available for the authenticated user can be retrieved from [List Meeting Templates](/docs/api/v1/meetings/list-meeting-templates). This parameter is ignored for an ad-hoc meeting.
    #: example: N2Q3ZWE1ZjQyYjkyMWVhY2UwNTM4NmNhMjRhZDczMGU6VS0yMDA5NzItTUMtZW5fVVM
    template_id: Optional[str] = None
    #: Meeting title. The title can be a maximum of 128 characters long. The default value for an ad-hoc meeting is the user's name if not specified.
    #: example: John's Meeting
    title: Optional[str] = None
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long.
    #: example: John's Agenda
    agenda: Optional[str] = None
    #: Meeting password. Must conform to the site's password complexity settings. Read [password management](https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration) for details. If not specified, a random password conforming to the site's password rules will be generated automatically.
    #: example: BgJep@43
    password: Optional[str] = None
    #: Date and time for the start of meeting in any [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format. `start` cannot be before current date and time or after `end`. Duration between `start` and `end` cannot be shorter than 10 minutes or longer than 24 hours. Please note that when a meeting is being scheduled, `start` of the meeting will be accurate to minutes, not seconds or milliseconds. Therefore, if `start` is within the same minute as the current time, `start` will be adjusted to the upcoming minute; otherwise, `start` will be adjusted with seconds and milliseconds stripped off. For instance, if the current time is `2022-03-01T10:32:16.657+08:00`, `start` of `2022-03-01T10:32:28.076+08:00` or `2022-03-01T10:32:41+08:00` will be adjusted to `2022-03-01T10:33:00+08:00`, and `start` of `2022-03-01T11:32:28.076+08:00` or `2022-03-01T11:32:41+08:00` will be adjusted to `2022-03-01T11:32:00+08:00`. The default value for an ad-hoc meeting is 5 minutes after the current time and the user's input value will be ignored. An ad-hoc meeting can be started immediately even if the `start` is 5 minutes after the current time.
    #: example: 2020-05-15T20:30:00-08:00
    start: Optional[datetime] = None
    #: Date and time for the end of meeting in any [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format. `end` cannot be before current date and time or before `start`. Duration between `start` and `end` cannot be shorter than 10 minutes or longer than 24 hours. Please note that when a meeting is being scheduled, `end` of the meeting will be accurate to minutes, not seconds or milliseconds. Therefore, `end` will be adjusted with seconds and milliseconds stripped off. For instance, `end` of `2022-03-01T11:52:28.076+08:00` or `2022-03-01T11:52:41+08:00` will be adjusted to `2022-03-01T11:52:00+08:00`. The default value for an ad-hoc meeting is 20 minutes after the current time and the user's input value will be ignored.
    #: example: 2020-05-15T21:30:00-08:00
    end: Optional[datetime] = None
    #: [Time zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) in which the meeting was originally scheduled (conforming with the [IANA time zone database](https://www.iana.org/time-zones)). The default value for an ad-hoc meeting is `UTC` and the user's input value will be ignored.
    #: example: America/Los_Angeles
    timezone: Optional[str] = None
    #: Meeting series recurrence rule (conforming with [RFC 2445](https://www.ietf.org/rfc/rfc2445.txt)), applying only to meeting series. It doesn't apply to a scheduled meeting or an ended or ongoing meeting instance. This parameter is ignored for an ad-hoc meeting. Multiple days or dates for monthly or yearly `recurrence` rule are not supported, only the first day or date specified is taken. For example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
    #: example: FREQ=DAILY;INTERVAL=1;COUNT=20
    recurrence: Optional[str] = None
    #: Whether or not meeting is recorded automatically.
    enabled_auto_record_meeting: Optional[bool] = None
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the meeting. The target site is specified by `siteUrl` parameter when creating the meeting; if not specified, it's the user's preferred site. The default value for an ad-hoc meeting is `true` and the user's input value will be ignored.
    allow_any_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The default value for an ad-hoc meeting is `true` and the user's input value will be ignored.
    enabled_join_before_host: Optional[bool] = None
    #: Whether or not to allow any attendee to connect audio in the meeting before the host joins the meeting. This attribute is only applicable if the `enabledJoinBeforeHost` attribute is set to true. The default value for an ad-hoc meeting is `true` and the user's input value will be ignored.
    enable_connect_audio_before_host: Optional[bool] = None
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. This attribute is only applicable if the `enabledJoinBeforeHost` attribute is set to true. Valid options for a meeting are `0`, `5`, `10`, and `15`, and valid options for a webinar are `0`, `15`, `30`, `45`, and `60`. The default value for an ad-hoc meeting is 0 and the user's input value will be ignored.
    #: example: 15.0
    join_before_host_minutes: Optional[int] = None
    #: Whether or not to exclude the meeting password from the email invitation. This parameter is ignored for an ad-hoc meeting.
    exclude_password: Optional[bool] = None
    #: Whether or not to allow the meeting to be listed on the public calendar. The default value for an ad-hoc meeting is `false` and the user's input value will be ignored.
    public_meeting: Optional[bool] = None
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host. This parameter is ignored for an ad-hoc meeting.
    #: example: 10.0
    reminder_time: Optional[int] = None
    #: Specifies how the people who aren't on the invite can join the unlocked meeting. The default value for an ad-hoc meeting is `allowJoinWithLobby` and the user's input value will be ignored.
    #: example: allowJoin
    unlocked_meeting_join_security: Optional[MeetingSeriesObjectUnlockedMeetingJoinSecurity] = None
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar meeting. All available meeting session types enabled for the user can be retrieved using the [List Meeting Session Types](/docs/api/v1/meetings/list-meeting-session-types) API.
    #: example: 3.0
    session_type_id: Optional[int] = None
    #: When set as an attribute in a POST request body, specifies whether it's a regular meeting, a webinar, or a meeting scheduled in the user's [personal room](https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings). If not specified, it's a regular meeting by default. The default value for an ad-hoc meeting is `meeting` and the user's input value will be ignored.
    #: example: meeting
    scheduled_type: Optional[MeetingSeriesObjectScheduledType] = None
    #: Whether or not webcast view is enabled. This parameter is ignored for an ad-hoc meeting.
    enabled_webcast_view: Optional[bool] = None
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read [password management](https://help.webex.com/en-us/zrupm6/Manage-Security-Options-for-Your-Site-in-Webex-Site-Administration) for details. If not specified, a random password conforming to the site's password rules will be generated automatically. This parameter is ignored for an ad-hoc meeting.
    #: example: GwLqa@78
    panelist_password: Optional[str] = None
    #: Whether or not to automatically lock the meeting after it starts. The default value for an ad-hoc meeting is `false` and the user's input value will be ignored.
    enable_automatic_lock: Optional[bool] = None
    #: The number of minutes after the meeting begins, for automatically locking it. The default value for an ad-hoc meeting is null and the user's input value will be ignored.
    #: example: 10.0
    automatic_lock_minutes: Optional[int] = None
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a cohost. The target site is specified by `siteUrl` parameter when creating the meeting; if not specified, it's user's preferred site. The default value for an ad-hoc meeting is `false` and the user's input value will be ignored.
    allow_first_user_to_be_co_host: Optional[bool] = None
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting without a prompt. The default value for an ad-hoc meeting is `true` and the user's input value will be ignored.
    allow_authenticated_devices: Optional[bool] = None
    #: Invitees for meeting. The maximum size of invitees is 1000. If `roomId` is specified and `invitees` is missing, all the members in the space are invited implicitly. If both `roomId` and `invitees` are specified, only those in the `invitees` list are invited. `coHost` for each invitee is `true` by default if `roomId` is specified when creating a meeting, and anyone in the invitee list that is not qualified to be a cohost will be invited as a non-cohost invitee. The user's input value will be ignored for an ad-hoc meeting and the the members of the room specified by `roomId` except "me" will be used by default.
    invitees: Optional[list[InviteeObjectForCreateMeeting]] = None
    #: Whether or not to send emails to host and invitees. It is an optional field and default value is true. The default value for an ad-hoc meeting is `false` and the user's input value will be ignored.
    #: example: True
    send_email: Optional[bool] = None
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API has the admin-level scopes. When used, the admin may specify the email of a user in a site they manage to be the meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: URL of the Webex site which the meeting is created on. If not specified, the meeting is created on user's preferred site. All available Webex sites and preferred site of the user can be retrieved by `Get Site List` API.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: Meeting Options.
    meeting_options: Optional[MeetingSeriesObjectMeetingOptions] = None
    #: Attendee Privileges. This attribute is not supported for a webinar.
    attendee_privileges: Optional[MeetingSeriesObjectAttendeePrivileges] = None
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information in order to join the meeting. Meeting invitees will receive an email with a registration link for the registration. When the registration form has been submitted and approved, an email with a real meeting link will be received. By clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not apply to a meeting when it's a recurring meeting with a `recurrence` field or no `password` or when the feature toggle `DecoupleJBHWithRegistration` is disabled the `Join Before Host` option is enabled for the meeting, See [Register for a Meeting in Cisco Webex Meetings](https://help.webex.com/en-us/nmgmeff/Register-for-a-Meeting-in-Cisco-Webex-Meetings) for details.
    registration: Optional[CreateMeetingObjectRegistration] = None
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries meetings by a key in its own domain. The maximum size of `integrationTags` is 3 and each item of `integrationTags` can be a maximum of 64 characters long. This parameter is ignored for an ad-hoc meeting.
    integration_tags: Optional[list[str]] = None
    #: Simultaneous interpretation information for a meeting.
    simultaneous_interpretation: Optional[CreateMeetingObjectSimultaneousInterpretation] = None
    #: Whether or not breakout sessions are enabled.
    enabled_breakout_sessions: Optional[bool] = None
    #: Breakout sessions are smaller groups that are split off from the main meeting or webinar. They allow a subset of participants to collaborate and share ideas over audio and video. Use breakout sessions for workshops, classrooms, or for when you need a moment to talk privately with a few participants outside of the main session. Please note that maximum number of breakout sessions in a meeting or webinar is 100. In webinars, if hosts preassign attendees to breakout sessions, the role of `attendee` will be changed to `panelist`. Breakout session is not supported for a meeting with simultaneous interpretation.
    breakout_sessions: Optional[list[BreakoutSessionObject]] = None
    #: Tracking codes information. All available tracking codes and their options for the specified site can be retrieved by [List Meeting Tracking Codes](/docs/api/v1/meetings/list-meeting-tracking-codes) API. If an optional tracking code is missing from the `trackingCodes` array and there's a default option for this tracking code, the default option is assigned automatically. If the `inputMode` of a tracking code is `select`, its value must be one of the site-level options or the user-level value. Tracking code is not supported for a personal room meeting or an ad-hoc space meeting.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]] = None
    #: Audio connection options.
    audio_connection_options: Optional[MeetingSeriesObjectAudioConnectionOptions] = None
    #: Require attendees to sign in before joining the webinar. This option works when the value of `scheduledType` attribute is `webinar`. Please note that `requireAttendeeLogin` cannot be set if someone has already registered for the webinar.
    require_attendee_login: Optional[bool] = None
    #: Restrict webinar to invited attendees only. This option works when the registration option is disabled and the value of `scheduledType` attribute is `webinar`. Please note that `restrictToInvitees` cannot be set to `true` if `requireAttendeeLogin` is `false`.
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
    #: Meeting object which is used to create a meeting by the meeting template. Please note that the meeting object should be used to create a meeting immediately after retrieval since the `start` and `end` may be invalid quickly after generation.
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
    #: Whether or not a registrant's first name is required for meeting registration. This option must always be `true`.
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
    #: example: 1.0
    option_id: Optional[int] = None
    #: The content of the answer or the option for this question.
    #: example: green
    answer: Optional[str] = None


class CustomizedRegistrant(ApiModel):
    #: Unique identifier for the customized questions retrieved from the registration form.
    #: example: 330087.0
    question_id: Optional[int] = None
    #: The answers for customized questions. If the question type is checkbox, more than one answer can be set.
    answers: Optional[list[AnswerForCustomizedQuestion]] = None


class RegistrantFormObject(ApiModel):
    #: The registrant's first name.
    #: example: 'Bob'
    first_name: Optional[str] = None
    #: The registrant's last name. (Required)
    #: example: 'Lee'
    last_name: Optional[str] = None
    #: The registrant's email.
    #: example: 'bob@example.com'
    email: Optional[str] = None
    #: If `true` send email to the registrant. Default: `true`.
    #: example: True
    send_email: Optional[bool] = None
    #: The registrant's job title. Registration options define whether or not this is required.
    #: example: 'manager'
    job_title: Optional[str] = None
    #: The registrant's company. Registration options define whether or not this is required.
    #: example: 'Cisco Systems, Inc.'
    company_name: Optional[str] = None
    #: The registrant's first address line. Registration options define whether or not this is required.
    #: example: 'address1 string'
    address1: Optional[str] = None
    #: The registrant's second address line. Registration options define whether or not this is required.
    #: example: 'address2 string'
    address2: Optional[str] = None
    #: The registrant's city name. Registration options define whether or not this is required.
    #: example: 'New York'
    city: Optional[str] = None
    #: The registrant's state. Registration options define whether or not this is required.
    #: example: 'New York'
    state: Optional[str] = None
    #: The registrant's postal code. Registration options define whether or not this is required.
    #: example: 123456.0
    zip_code: Optional[int] = None
    #: The America is not a country or a specific region. Registration options define whether or not this is required.
    #: example: 'United States'
    country_region: Optional[str] = None
    #: The registrant's work phone number. Registration options define whether or not this is required.
    #: example: '+1 123456'
    work_phone: Optional[str] = None
    #: The registrant's FAX number. Registration options define whether or not this is required.
    #: example: '123456'
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
    #: example: 123456.0
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
    #: Registrant's source id.The `sourceId` is from [Create Invitation Sources](/docs/api/v1/meetings/create-invitation-sources) API.
    #: example: cisco
    source_id: Optional[str] = None
    #: Registrant's registration ID. Registrants have a special number to identify a registrations if it is webinar-enabled and enabled registration ID.
    #: example: 1111
    registration_id: Optional[datetime] = None


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
    #: example: 123456.0
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


class QueryRegistrants(ApiModel):
    #: Registrant's status.
    #: example: pending
    status: Optional[RegistrantStatus] = None
    #: Sort order for the registrants.
    #: example: DESC
    order_type: Optional[QueryRegistrantsOrderType] = None
    #: Registrant ordering field. Ordered by `registrationTime` by default.
    #: example: registrationTime
    order_by: Optional[QueryRegistrantsOrderBy] = None
    #: List of registrant email addresses.
    #: example: ['bob@example.com']
    emails: Optional[list[str]] = None


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
    id: Optional[datetime] = None
    #: Name of the meeting session type.
    #: example: Webex Meetings EC 2.0 meeting
    name: Optional[str] = None
    #: Meeting session type.
    #: example: meeting
    type: Optional[MeetingSessionTypeObjectType] = None
    #: The maximum number of attendees for the meeting session type.
    #: example: 1000.0
    attendees_capacity: Optional[int] = None


class UpdateInterpreterObject(ApiModel):
    #: The pair of `languageCode1` and `languageCode2` form a bi-directional simultaneous interpretation language channel. The language codes conform with [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).
    #: example: en
    language_code1: Optional[str] = None
    #: The pair of `languageCode1` and `languageCode2` form a bi-directional simultaneous interpretation language channel. The language codes conform with [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).
    #: example: de
    language_code2: Optional[str] = None
    #: Email address of meeting interpreter. If not specified, it'll be an empty interpreter for the bi-directional language channel. Please note that multiple interpreters with different emails can be assigned to the same bi-directional language channel, but the same email cannot be assigned to more than one interpreter.
    #: example: marcus.tuchel@example.com
    email: Optional[str] = None
    #: Display name of meeting interpreter. If the interpreter is already an invitee of the meeting and it has a different display name, that invitee's display name will be overwritten by this attribute.
    #: example: Tuchel
    display_name: Optional[str] = None
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage to be the meeting host.
    #: example: brenda.song@example.com
    host_email: Optional[str] = None
    #: If `true`, send email to the interpreter.
    #: example: True
    send_email: Optional[bool] = None


class UpdateMeetingBreakoutSessionsObject(ApiModel):
    #: Email address for the meeting host. This parameter is only used if the user or application calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage and the API will return details for a meeting that is hosted by that user.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: Whether or not to send emails to host and invitees. It is an optional field and default value is true.
    #: example: True
    send_email: Optional[bool] = None
    #: Breakout sessions are smaller groups that are split off from the main meeting or webinar. They allow a subset of participants to collaborate and share ideas over audio and video. Use breakout sessions for workshops, classrooms, or for when you need a moment to talk privately with a few participants outside of the main session. Please note that maximum number of breakout sessions in a meeting or webinar is 100. In webinars, if hosts preassign attendees to breakout sessions, the role of `attendee` will be changed to `panelist`. Breakout session is not supported for a meeting with simultaneous interpretation.
    items: Optional[list[BreakoutSessionObject]] = None


class GetBreakoutSessionObject(ApiModel):
    #: Unique identifier for breakout session.
    #: example: 18d2e565770c4eee918784ee333510ec
    id: Optional[str] = None
    #: Name for breakout session.
    #: example: Breakout Session Name
    name: Optional[str] = None
    #: Invitees for breakout session.
    invitees: Optional[list[str]] = None


class GetBreakoutSessionsObject(ApiModel):
    #: Breakout Sessions information for meeting.
    items: Optional[list[GetBreakoutSessionObject]] = None


class JoinMeetingObject(ApiModel):
    #: Unique identifier for the meeting. This parameter applies to meeting series and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Please note that currently meeting ID of a scheduled [personal room](https://help.webex.com/en-us/article/nul0wut/Webex-Personal-Rooms-in-Webex-Meetings) meeting is also supported for this API.
    #: example: 98d8c2212c9d62b162b9565932735e58_I_231409844992607809
    meeting_id: Optional[str] = None
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting instances which have ended.
    #: example: 123456789
    meeting_number: Optional[str] = None
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or join.
    #: example: https://site4-example.webex.com/site4/j.php?MTID=md41817da6a55b0925530cb88b3577b1e
    web_link: Optional[str] = None
    #: Whether or not to redirect to `joinLink`. It is an optional field and default value is true.
    join_directly: Optional[bool] = None
    #: Email address of meeting participant. If `email` is specified, the link is generated for the user of `email`; otherwise, the API returns the link for the user calling the API. `email` is required for a [guest issuer](https://developer.webex.com/docs/guest-issuer).
    #: example: brenda.song@example.com
    email: Optional[str] = None
    #: Display name of meeting participant. If `displayName` is specified, `email` must be specified as well. If `email` is specified and `displayName` is not, display name is the same as `email`. If neither `displayName` nor `email` is specified, the API returns the link for the user calling the API. The maximum length of `displayName` is 128 characters. `displayName` is required for a [guest issuer](https://developer.webex.com/docs/guest-issuer).
    #: example: Brenda Song
    display_name: Optional[str] = None
    #: Required when the meeting is protected by a password and the current user is not privileged to view it if they are not a host, cohost, or invitee.
    #: example: BgJep@43
    password: Optional[str] = None
    #: Expiration duration of `joinLink` in minutes. Must be between 1 and 60.
    #: example: 5.0
    expiration_minutes: Optional[int] = None
    #: Required when the meeting is webinar-enabled and enabled registration ID.
    #: example: 1111
    registration_id: Optional[datetime] = None


class JoinMeetingLinkObject(ApiModel):
    #: The link is used to start a meeting as the meeting host. Only the meeting host or cohost can generate the `startLink`.
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
    #: example: 3388057.0
    id: Optional[int] = None
    #: Details for the question.
    #: example: Do you like cisco?
    question: Optional[str] = None
    #: Type for the question.
    #: example: text
    type: Optional[QuestionObjectType] = None
    #: The lowest score of the rating question. This attribute will be ingnored, if the value of `type` attribute is not `rating`.
    #: example: 1.0
    from_score: Optional[int] = None
    #: The lowest score label of the rating question. This attribute will be ingnored, if the value of `type` attribute is not `rating`.
    #: example: disagree
    from_label: Optional[str] = None
    #: The highest score of the rating question. This attribute will be ingnored, if the value of `type` attribute is not `rating`.
    #: example: 5.0
    to_score: Optional[int] = None
    #: The highest score label of the rating question. This attribute will be ingnored, if the value of `type` attribute is not `rating`.
    #: example: agree
    to_label: Optional[str] = None
    #: Options for the question. This attribute will be ingnored, if the value of `type` attribute is `text` or `rating`.
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
    #: example: 3388057.0
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


class RegistrationForUpdate(ApiModel):
    #: - Email address for the meeting host. This parameter is only used if the user or application calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage and the API will return an update for a meeting that is hosted by that user.
    #: example: 'john.andersen@example.com'
    host_email: Optional[str] = None
    #: Whether or not a registrant's first name is required for meeting registration. This option must always be `true`.
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
    #: Maximum number of meeting registrations. This only applies to meetings. The maximum number of participants for meetings and webinars, with the limit based on the user capacity and controlled by a toggle at the site level. The default maximum number of participants for webinars is 10000, but the actual maximum number of participants is limited by the user capacity.
    #: example: 1000.0
    max_register_num: Optional[int] = None
    #: Customized questions for meeting registration.
    customized_questions: Optional[list[CustomizedQuestionForCreateMeeting]] = None
    #: The approval rule for standard questions.
    rules: Optional[list[StandardRegistrationApproveRule]] = None


class SurveyLinkRequestObject(ApiModel):
    #: Email address for the meeting host. This parameter is only used if the user or application calling the API has the admin on-behalf-of scopes. An admin can specify the email of the meeting host who is in a site he manages and the API returns post survey links on behalf of the meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: Start date and time (inclusive) in any [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format for the meeting objects being requested and conforms with the `timezone` in the request header if specified. `meetingStartTimeFrom` cannot be after `meetingStartTimeTo`. Only applies when `meetingId` is not an instance ID. The API generates survey links for the last instance of `meetingId` in the time range specified by `meetingStartTimeFrom` and `meetingStartTimeTo`. If not specified, `meetingStartTimeFrom` equals `meetingStartTimeTo` minus `1` month; if `meetingStartTimeTo` is also not specified, the default value for `meetingStartTimeFrom` is `1` month before the current date and time.
    #: example: 2019-03-18T09:30:00Z
    meeting_start_time_from: Optional[datetime] = None
    #: End date and time (exclusive) in any [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) compliant format for the meeting objects being requested and conforms with the `timezone` in the request header if specified. `meetingStartTimeTo` cannot be prior to `meetingStartTimeFrom`. Only applies when `meetingId` is not an instance ID. The API generates survey links for the last instance of `meetingId` in the time range specified by `meetingStartTimeFrom` and `meetingStartTimeTo`. If not specified, `meetingStartTimeTo` equals `meetingStartTimeFrom` plus `1` month; if `meetingStartTimeFrom` is also not specified, the default value for `meetingStartTimeTo` is the current date and time.
    #: example: 2019-03-25T09:30:00Z
    meeting_start_time_to: Optional[datetime] = None
    #: Participants' email list. The maximum size of `emails` is 100.
    emails: Optional[list[str]] = None


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
    id: Optional[datetime] = None
    #: Source ID for invitation.
    #: example: cisco
    source_id: Optional[str] = None
    #: Email for invitation source.
    #: example: john001@example.com
    source_email: Optional[str] = None
    #: The link bound to `sourceId` can directly join the meeting. If the meeting requires registration,`joinLink` is not returned.
    #: example: https://example.webex.com/example/j.php?MTID=m6d75f1c875b3e3c5d18c7598036bdd8b
    join_link: Optional[str] = None
    #: The link bound to `sourceId` can directly register the meeting. If the meeting requires registration, `registerLink` is returned.
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
    #: This value only applies to the service of `All`. When the type of `All` for a tracking code is `notApplicable`, there are different types for different services. For example, `required` for `MeetingCenter`, `optional` for `EventCenter` and `notUsed` for others.
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
    id: Optional[datetime] = None
    #: Name for the tracking code.
    #: example: Department
    name: Optional[str] = None
    #: Site URL for the tracking code.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: Tracking code option list. The options here differ from those in the [site-level tracking codes](/docs/api/v1/tracking-codes/get-a-tracking-code) and the [user-level tracking codes](/docs/api/v1/tracking-codes/get-user-tracking-codes). It is the result of a selective combination of the two. If there's user-level value for a tracking code, the user-level value becomes the default option for the tracking code, and the site-level default value becomes non-default.
    options: Optional[list[OptionsForTrackingCodeObject]] = None
    #: The input mode in which the tracking code value can be assigned.
    input_mode: Optional[MeetingTrackingCodesObjectInputMode] = None
    #: Service for schedule or sign up pages
    service: Optional[MeetingTrackingCodesObjectService] = None
    #: Type for meeting scheduler or meeting start pages.
    type: Optional[MeetingTrackingCodesObjectType] = None


class ReassignMeetingRequestObject(ApiModel):
    #: Email address of the new meeting host.
    #: example: john.andersen@example.com
    host_email: Optional[str] = None
    #: List of meeting series IDs to be reassigned the new host. The size is between 1 and 100. All the meetings of `meetingIds` should belong to the same site, which is the `siteUrl` in the request header, if specified, or the admin user's preferred site, if not specified. All available Webex sites and the preferred sites of a user can be retrieved by [Get Site List](/docs/api/v1/meeting-preferences/get-site-list) API.
    meeting_ids: Optional[list[str]] = None


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
    http_status: Optional[datetime] = None
    #: General message for the host reassignment of `meetingId` if it fails.
    #: example: The requested resource could not be found.
    message: Optional[str] = None
    #: Detailed descriptions for the host reassignment of `meetingId` if it fails.
    errors: Optional[list[ReassignMeetingErrorDescriptionObject]] = None


class ListMeetingsResponse(ApiModel):
    #: Meetings array.
    items: Optional[list[MeetingSeriesObjectForListMeeting]] = None


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


class ListMeetingsOfAMeetingSeriesResponse(ApiModel):
    #: Meetings array.
    items: Optional[list[ScheduledMeetingObject]] = None


class ListMeetingTemplatesResponse(ApiModel):
    #: Meeting templates array.
    items: Optional[list[TemplateObject]] = None


class ListMeetingSessionTypesResponse(ApiModel):
    #: Meeting session type array
    items: Optional[list[MeetingSessionTypeObject]] = None


class BatchRegisterMeetingRegistrantsResponse(ApiModel):
    items: Optional[list[RegistrantCreateResponse]] = None


class ListMeetingRegistrantsResponse(ApiModel):
    #: Registrants array.
    items: Optional[list[Registrant]] = None


class BatchUpdateMeetingRegistrantsStatusStatusOpType(str, Enum):
    approve = 'approve'
    reject = 'reject'
    cancel = 'cancel'
    bulk_delete = 'bulkDelete'


class ListMeetingInterpretersResponse(ApiModel):
    #: Array of meeting interpreters.
    items: Optional[list[InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting]] = None


class ListMeetingSurveyResultsResponse(ApiModel):
    #: SurveyResult array
    items: Optional[list[SurveyResultObject]] = None


class GetMeetingSurveyLinksResponse(ApiModel):
    #: Survey link array
    items: Optional[list[SurveyLinkObject]] = None


class CreateInvitationSourcesResponse(ApiModel):
    #: Invitation source array.
    items: Optional[list[InvitationSourceObject]] = None


class ReassignMeetingsToANewHostResponse(ApiModel):
    #: Array of meeting reassignment results.
    items: Optional[list[ReassignMeetingResponseObject]] = None

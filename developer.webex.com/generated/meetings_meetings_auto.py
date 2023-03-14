from collections.abc import Generator
from typing import List, Optional

from pydantic import parse_obj_as

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['AnswerForCustomizedQuestion', 'AttendeePrivileges', 'AudioConnectionOptions', 'AudioConnectionType',
           'BatchRegisterMeetingRegistrantsResponse', 'BreakoutSessionObject', 'CallInNumbers', 'AnswerCondition',
           'CreateInvitationSourcesResponse', 'CreateMeetingBody', 'CreateMeetingInterpreterBody',
           'CreateMeetingResponse', 'CustomizedQuestionForCreateMeeting', 'CustomizedQuestionForGetMeeting',
           'CustomizedRegistrant', 'EntryAndExitTone', 'GetBreakoutSessionObject', 'GetMeetingControlStatusResponse',
           'GetMeetingSurveyResponse', 'GetMeetingTemplateResponse', 'GetRegistrationFormFormeetingResponse',
           'GetmeetingRegistrantsDetailInformationResponse', 'InputMode',
           'InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting',
           'InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting', 'InvitationSourceCreateObject',
           'InvitationSourceObject', 'InviteeObjectForCreateMeeting', 'JoinMeetingResponse', 'Links',
           'ListInvitationSourcesResponse', 'ListMeetingBreakoutSessionsResponse', 'ListMeetingInterpretersResponse',
           'ListMeetingRegistrantsResponse', 'ListMeetingSessionTypesResponse', 'ListMeetingSurveyResultsResponse',
           'ListMeetingTemplatesResponse', 'ListMeetingTrackingCodesResponse', 'ListMeetingsOfMeetingSeriesResponse',
           'ListMeetingsResponse', 'MeetingOptions', 'MeetingSeriesObjectForListMeeting', 'MeetingSessionTypeObject',
           'MeetingType', 'MeetingsApi', 'NoteType', 'Options', 'OptionsForTrackingCodeObject', 'OrderBy', 'OrderType',
           'PatchMeetingBody', 'PatchMeetingResponse', 'QueryMeetingRegistrantsResponse', 'Question', 'QuestionObject',
           'QuestionWithAnswersObject', 'RegisterMeetingRegistrantBody', 'RegisterMeetingRegistrantResponse',
           'Registration', 'RegistrationResult', 'Rules', 'ScheduledMeetingObject', 'ScheduledType',
           'Service',
           'SimultaneousInterpretation', 'SimultaneousInterpretation1', 'StandardRegistrationApproveRule', 'State',
           'Status', 'SurveyResultObject', 'Telephony', 'Telephony3', 'TemplateObject', 'TemplateType',
           'TrackingCodeItemForCreateMeetingObject', 'QuestionType', 'Type11', 'Type4', 'Type9',
           'UnlockedMeetingJoinSecurity',
           'UpdateMeetingBreakoutSessionsResponse']


class TemplateType(str, Enum):
    #: Webex meeting.
    meeting = 'meeting'
    #: Webex webinar.
    webinar = 'webinar'


class ScheduledType(TemplateType):
    #: Set the value of scheduledType attribute to personalRoomMeeting for creating a meeting in the user's personal
    #: room. Please note that templateId, roomId, integrationTags, enabledWebcastView, enabledAutoRecordMeeting and
    #: registration are not supported when creating a personal room meeting.
    personal_room_meeting = 'personalRoomMeeting'


class InviteeObjectForCreateMeeting(ApiModel):
    #: Email address of meeting invitee.
    email: Optional[str]
    #: Display name of meeting invitee. The maximum length of displayName is 128 characters. If not specified but the
    #: email has been registered, user's registered name for the email will be taken as displayName. If not specified
    #: and the email hasn't been registered, the email will be taken as displayName.
    display_name: Optional[str]
    #: Whether or not invitee is allowed to be a cohost for the meeting. coHost for each invitee is true by default if
    #: roomId is specified when creating a meeting, and anyone in the invitee list that is not qualified to be a cohost
    #: will be invited as a non-cohost invitee.
    co_host: Optional[bool]
    #: Whether or not an invitee is allowed to be a panelist. Only applies to webinars.
    panelist: Optional[bool]


class QuestionType(str, Enum):
    #: Single line text box.
    single_line_text_box = 'singleLineTextBox'
    #: Multiple line text box.
    multi_line_text_box = 'multiLineTextBox'
    #: Check box which requires options.
    checkbox = 'checkbox'
    #: Drop down list box which requires options.
    dropdown_list = 'dropdownList'
    #: Single radio button which requires options.
    radio_buttons = 'radioButtons'


class AnswerCondition(str, Enum):
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


class RegistrationResult(str, Enum):
    #: If the user's registration value meets the criteria, the registration form will be automatically approved.
    approve = 'approve'
    #: If the user's registration value meets the criteria, the registration form will be automatically rejected.
    reject = 'reject'


class Rules(ApiModel):
    #: Judgment expression for approval rules.
    condition: Optional[AnswerCondition]
    #: The keyword for the approval rule. If the rule matches the keyword, the corresponding action will be executed.
    value: Optional[str]
    #: The automatic approval result for the approval rule.
    result: Optional[RegistrationResult]
    #: Whether to check the case of values.
    match_case: Optional[bool]


class CustomizedQuestionForCreateMeeting(ApiModel):
    #: Title of the customized question.
    question: Optional[str]
    #: Whether or not the customized question is required to be answered by participants.
    required: Optional[bool]
    #: Type of the question being asked.
    type: Optional[QuestionType]
    #: The maximum length of a string that can be entered by the user, ranging from 0 to 999. Only required by
    #: singleLineTextBox and multiLineTextBox.
    max_length: Optional[int]
    #: The content of options. Required if the question type is one of checkbox, dropdownList, or radioButtons.
    #: The content of the option.
    options: Optional[list[object]]
    #: The automatic approval rules for customized questions.
    rules: Optional[list[Rules]]


class Question(str, Enum):
    #: If the value is lastName, this approval rule applies to the standard question of "Last Name".
    last_name = 'lastName'
    #: If the value is email, this approval rule applies to the standard question of "Email".
    email = 'email'
    #: If the value is jobTitle, this approval rule applies to the standard question of "Job Title".
    job_title = 'jobTitle'
    #: If the value is companyName, this approval rule applies to the standard question of "Company Name".
    company_name = 'companyName'
    #: If the value is address1, this approval rule applies to the standard question of "Address 1".
    address1 = 'address1'
    #: If the value is address2, this approval rule applies to the standard question of "Address 2".
    address2 = 'address2'
    #: If the value is city, this approval rule applies to the standard question of "City".
    city = 'city'
    #: If the value is state, this approval rule applies to the standard question of "State".
    state = 'state'
    #: If the value is zipCode, this approval rule applies to the standard question of "Zip/Post Code".
    zip_code = 'zipCode'
    #: If the value is countryRegion, this approval rule applies to the standard question of "Country Region".
    country_region = 'countryRegion'
    #: If the value is workPhone, this approval rule applies to the standard question of "Work Phone".
    work_phone = 'workPhone'
    #: If the value is fax, this approval rule applies to the standard question of "Fax".
    fax = 'fax'


class StandardRegistrationApproveRule(Rules):
    #: Name for standard question.
    question: Optional[Question]
    #: The priority number of the approval rule. Approval rules for standard questions and custom questions need to be
    #: ordered together.
    order: Optional[int]


class Registration(ApiModel):
    #: Whether or not meeting registration requests are accepted automatically.
    auto_accept_request: Optional[bool]
    #: Whether or not a registrant's first name is required for meeting registration.
    require_first_name: Optional[bool]
    #: Whether or not a registrant's last name is required for meeting registration.
    require_last_name: Optional[bool]
    #: Whether or not a registrant's email is required for meeting registration.
    require_email: Optional[bool]
    #: Whether or not a registrant's job title is required for meeting registration.
    require_job_title: Optional[bool]
    #: Whether or not a registrant's company name is required for meeting registration.
    require_company_name: Optional[bool]
    #: Whether or not a registrant's first address field is required for meeting registration.
    require_address1: Optional[bool]
    #: Whether or not a registrant's second address field is required for meeting registration.
    require_address2: Optional[bool]
    #: Whether or not a registrant's city is required for meeting registration.
    require_city: Optional[bool]
    #: Whether or not a registrant's state is required for meeting registration.
    require_state: Optional[bool]
    #: Whether or not a registrant's postal code is required for meeting registration.
    require_zip_code: Optional[bool]
    #: Whether or not a registrant's country or region is required for meeting registration.
    require_country_region: Optional[bool]
    #: Whether or not a registrant's work phone number is required for meeting registration.
    require_work_phone: Optional[bool]
    #: Whether or not a registrant's fax number is required for meeting registration.
    require_fax: Optional[bool]
    #: The maximum number of meeting registrations. Only applies to meetings. Webinars use a default value of 10000. If
    #: the maximum capacity of attendees for a webinar is less than 10000, e.g. 3000, then at most 3000 registrants can
    #: join this webinar.
    max_register_num: Optional[int]
    #: Customized questions for meeting registration.
    customized_questions: Optional[list[CustomizedQuestionForCreateMeeting]]
    #: The approval rules for standard questions.
    rules: Optional[list[StandardRegistrationApproveRule]]


class InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting(ApiModel):
    #: Forms a set of simultaneous interpretation channels together with languageCode2. Standard language format from
    #: ISO 639-1 code. Read ISO 639-1 for details.
    language_code1: Optional[str]
    #: Forms a set of simultaneous interpretation channels together with languageCode1. Standard language format from
    #: ISO 639-1 code. Read ISO 639-1 for details.
    language_code2: Optional[str]
    #: Email address of meeting interpreter.
    email: Optional[str]
    #: Display name of meeting interpreter.
    display_name: Optional[str]


class SimultaneousInterpretation(ApiModel):
    #: Whether or not simultaneous interpretation is enabled.
    enabled: Optional[bool]
    #: Interpreters for meeting.
    interpreters: Optional[list[InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting]]


class BreakoutSessionObject(ApiModel):
    #: Name for breakout session.
    name: Optional[str]
    #: Invitees for breakout session. Please note that one invitee cannot be assigned to more than one breakout
    #: session.
    invitees: Optional[list[str]]


class UnlockedMeetingJoinSecurity(str, Enum):
    #: If the value of unlockedMeetingJoinSecurity attribute is allowJoin, people can join the unlocked meeting
    #: directly.
    allow_join = 'allowJoin'
    #: If the value of unlockedMeetingJoinSecurity attribute is allowJoinWithLobby, people will wait in the lobby until
    #: the host admits them.
    allow_join_with_lobby = 'allowJoinWithLobby'
    #: If the value of unlockedMeetingJoinSecurity attribute is blockFromJoin, people can't join the unlocked meeting.
    block_from_join = 'blockFromJoin'


class NoteType(str, Enum):
    #: If the value of noteType attribute is allowAll, all participants can take notes.
    allow_all = 'allowAll'
    #: If the value of noteType attribute is allowOne, only a single note taker is allowed.
    allow_one = 'allowOne'


class MeetingOptions(ApiModel):
    #: Whether or not to allow any attendee to chat in the meeting. Also depends on the session type.
    enabled_chat: Optional[bool]
    #: Whether or not to allow any attendee to have video in the meeting. Also depends on the session type.
    enabled_video: Optional[bool]
    #: Whether or not to allow any attendee to poll in the meeting. Can only be set true for a webinar. The value of
    #: this attribute depends on the session type for a meeting. Please contact your site admin if this attribute is
    #: not available.
    enabled_polling: Optional[bool]
    #: Whether or not to allow any attendee to take notes in the meeting. The value of this attribute also depends on
    #: the session type.
    enabled_note: Optional[bool]
    #: Whether note taking is enabled. If the value of enabledNote is false, users can not set this attribute and get
    #: default value allowAll.
    note_type: Optional[NoteType]
    #: Whether or not to allow any attendee to have closed captions in the meeting. The value of this attribute also
    #: depends on the session type.
    enabled_closed_captions: Optional[bool]
    #: Whether or not to allow any attendee to transfer files in the meeting. The value of this attribute also depends
    #: on the session type.
    enabled_file_transfer: Optional[bool]
    #: Whether or not to allow any attendee to share Universal Communications Format media files in the meeting. The
    #: value of this attribute also depends on the sessionType.
    enabled_ucf_rich_media: Optional[bool]


class AttendeePrivileges(ApiModel):
    #: Whether or not to allow any attendee to share content in the meeting.
    enabled_share_content: Optional[bool]
    #: Whether or not to allow any attendee to save shared documents, slides, or whiteboards when they are shared as
    #: files in the content viewer instead of in a window or application.
    enabled_save_document: Optional[bool]
    #: Whether or not to allow any attendee to print shared documents, slides, or whiteboards when they are shared as
    #: files in the content viewer instead of in a window or application.
    enabled_print_document: Optional[bool]
    #: Whether or not to allow any attendee to annotate shared documents, slides, or whiteboards when they are shared
    #: as files in the content viewer instead of in a window or application.
    enabled_annotate: Optional[bool]
    #: Whether or not to allow any attendee to view participants.
    enabled_view_participant_list: Optional[bool]
    #: Whether or not to allow any attendee to see a small preview image of any page of shared documents or slides when
    #: they are shared as files in the content viewer instead of in a window or application.
    enabled_view_thumbnails: Optional[bool]
    #: Whether or not to allow any attendee to control applications, web browsers, or desktops remotely.
    enabled_remote_control: Optional[bool]
    #: Whether or not to allow any attendee to view any shared documents or slides when they are shared as files in the
    #: content viewer instead of in a window or application.
    enabled_view_any_document: Optional[bool]
    #: Whether or not to allow any attendee to scroll through any page of shared documents or slides when they are
    #: shared as files in the content viewer instead of in a window or application.
    enabled_view_any_page: Optional[bool]
    #: Whether or not to allow any attendee to contact the operator privately.
    enabled_contact_operator_privately: Optional[bool]
    #: Whether or not to allow any attendee to chat with the host in private.
    enabled_chat_host: Optional[bool]
    #: Whether or not to allow any attendee to chat with the presenter in private.
    enabled_chat_presenter: Optional[bool]
    #: Whether or not to allow any attendee to chat with other participants in private.
    enabled_chat_other_participants: Optional[bool]


class TrackingCodeItemForCreateMeetingObject(ApiModel):
    #: Name of the tracking code. The name cannot be empty and the maximum size is 120 characters.
    name: Optional[str]
    #: Value for the tracking code. value cannot be empty and the maximum size is 120 characters.
    value: Optional[str]


class AudioConnectionType(str, Enum):
    #: Provide a hybrid audio option, allowing attendees to join using their computer audio or a phone.
    webex_audio = 'webexAudio'
    #: Only restricts attendees to join the audio portion of the meeting using their computer instead of a telephone
    #: option.
    vo_ip = 'VoIP'
    #: Other teleconference services.
    other = 'other'
    #: The way of attendees join the audio portion of the meeting is the default value.
    none = 'none'


class EntryAndExitTone(str, Enum):
    #: All call-in users joining the meeting will hear the beep.
    beep = 'beep'
    #: All call-in users joining the meeting will hear their names.
    announce_name = 'announceName'
    #: Turn off beeps and name announcements.
    no_tone = 'noTone'


class AudioConnectionOptions(ApiModel):
    #: Choose how meeting attendees join the audio portion of the meeting.
    audio_connection_type: Optional[AudioConnectionType]
    #: Whether or not to show toll-free call-in numbers.
    enabled_toll_free_call_in: Optional[bool]
    #: Whether or not to show global call-in numbers to attendees.
    enabled_global_call_in: Optional[bool]
    #: Whether or not to allow attendees to receive a call-back and call-in is available. Can only be set true for a
    #: webinar.
    enabled_audience_call_back: Optional[bool]
    #: Select the sound you want users who have a phone audio connection to hear when someone enters or exits the
    #: meeting.
    entry_and_exit_tone: Optional[EntryAndExitTone]
    #: Whether or not to allow the host to unmute participants.
    allow_host_to_unmute_participants: Optional[bool]
    #: Whether or not to allow attendees to unmute themselves.
    allow_attendee_to_unmute_self: Optional[bool]
    #: Whether or not to auto-mute attendees when attendees enter meetings.
    mute_attendee_upon_entry: Optional[bool]


class PatchMeetingBody(ApiModel):
    #: Meeting title. The title can be a maximum of 128 characters long.
    title: Optional[str]
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long.
    agenda: Optional[str]
    #: Meeting password. Must conform to the site's password complexity settings. Read password management for details.
    password: Optional[str]
    #: Date and time for the start of meeting in any ISO 8601 compliant format. start cannot be before current date and
    #: time or after end. Duration between start and end cannot be shorter than 10 minutes or longer than 24 hours.
    #: Refer to the Webex Meetings guide for more information about restrictions on updating date and time for a
    #: meeting. Please note that when a meeting is being updated, start of the meeting will be accurate to minutes, not
    #: seconds or milliseconds. Therefore, if start is within the same minute as the current time, start will be
    #: adjusted to the upcoming minute; otherwise, start will be adjusted with seconds and milliseconds stripped off.
    #: For instance, if the current time is 2022-03-01T10:32:16.657+08:00, start of 2022-03-01T10:32:28.076+08:00 or
    #: 2022-03-01T10:32:41+08:00 will be adjusted to 2022-03-01T10:33:00+08:00, and start of
    #: 2022-03-01T11:32:28.076+08:00 or 2022-03-01T11:32:41+08:00 will be adjusted to 2022-03-01T11:32:00+08:00.
    start: Optional[str]
    #: Date and time for the end of meeting in any ISO 8601 compliant format. end cannot be before current date and
    #: time or before start. Duration between start and end cannot be shorter than 10 minutes or longer than 24 hours.
    #: Refer to the Webex Meetings guide for more information about restrictions on updating date and time for a
    #: meeting. Please note that when a meeting is being updated, end of the meeting will be accurate to minutes, not
    #: seconds or milliseconds. Therefore, end will be adjusted with seconds and milliseconds stripped off. For
    #: instance, end of 2022-03-01T11:52:28.076+08:00 or 2022-03-01T11:52:41+08:00 will be adjusted to
    #: 2022-03-01T11:52:00+08:00.
    end: Optional[str]
    #: Time zone in which the meeting was originally scheduled (conforming with the IANA time zone database).
    timezone: Optional[str]
    #: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring meeting series, not to a
    #: meeting series with only one scheduled meeting. Multiple days or dates for monthly or yearly recurrence rule are
    #: not supported, only the first day or date specified is taken. For example,
    #: "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported as
    #: "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
    recurrence: Optional[str]
    #: Whether or not meeting is recorded automatically.
    enabled_auto_record_meeting: Optional[bool]
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: meeting. The target site is specified by siteUrl parameter when creating the meeting; if not specified, it's
    #: user's preferred site.
    allow_any_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting.
    enabled_join_before_host: Optional[bool]
    #: Whether or not to allow any attendee to connect audio in the meeting before the host joins the meeting. This
    #: attribute is only applicable if the enabledJoinBeforeHost attribute is set to true.
    enable_connect_audio_before_host: Optional[bool]
    #: The number of minutes an attendee can join the meeting before the meeting start time and the host joins. This
    #: attribute is only applicable if the enabledJoinBeforeHost attribute is set to true. Valid options are 0, 5, 10
    #: and 15. Default is 0 if not specified.
    join_before_host_minutes: Optional[int]
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool]
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool]
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    reminder_time: Optional[int]
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    unlocked_meeting_join_security: Optional[UnlockedMeetingJoinSecurity]
    #: Unique identifier for a meeting session type for the user. This attribute is required while scheduling webinar
    #: meeting. All available meeting session types enabled for the user can be retrieved by List Meeting Session Types
    #: API.
    session_type_id: Optional[int]
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool]
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read
    #: password management for details. If not specified, a random password conforming to the site's password rules
    #: will be generated automatically.
    panelist_password: Optional[str]
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool]
    #: The number of minutes after the meeting begins, for automatically locking it.
    automatic_lock_minutes: Optional[int]
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a
    #: cohost. The target site is specified by siteUrl parameter when creating the meeting; if not specified, it's
    #: user's preferred site.
    allow_first_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting
    #: without a prompt.
    allow_authenticated_devices: Optional[bool]
    #: Whether or not to send emails to host and invitees. It is an optional field and default value is true.
    send_email: Optional[bool]
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin-level scopes. When used, the admin may specify the email of a user in a site they manage to be the
    #: meeting host.
    host_email: Optional[str]
    #: URL of the Webex site which the meeting is updated on. If not specified, the meeting is created on user's
    #: preferred site. All available Webex sites and preferred site of the user can be retrieved by Get Site List API.
    site_url: Optional[str]
    #: Meeting Options.
    meeting_options: Optional[MeetingOptions]
    #: Attendee Privileges.
    attendee_privileges: Optional[AttendeePrivileges]
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs,
    #: Salesforce Opportunity IDs, etc. The integration application queries meetings by a key in its own domain. The
    #: maximum size of integrationTags is 3 and each item of integrationTags can be a maximum of 64 characters long.
    #: Please note that an empty or null integrationTags will delete all existing integration tags for the meeting
    #: implicitly. Developer can update integration tags for a meetingSeries but he cannot update it for a
    #: scheduledMeeting or a meeting instance.
    integration_tags: Optional[list[str]]
    #: Whether or not breakout sessions are enabled. If the value of enabledBreakoutSessions is false, users can not
    #: set breakout sessions. If the value of enabledBreakoutSessions is true, users can update breakout sessions using
    #: the Update Breakout Sessions API. Updating breakout sessions are not supported by this API.
    enabled_breakout_sessions: Optional[bool]
    #: Tracking codes information. All available tracking codes and their options for the specified site can be
    #: retrieved by List Meeting Tracking Codes API. If an optional tracking code is missing from the trackingCodes
    #: array and there's a default option for this tracking code, the default option is assigned automatically. If the
    #: inputMode of a tracking code is select, its value must be one of the site-level options or the user-level value.
    #: Tracking code is not supported for a personal room meeting or an ad-hoc space meeting.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]]
    #: Audio connection options.
    audio_connection_options: Optional[AudioConnectionOptions]


class MeetingType(str, Enum):
    #: Primary instance of a scheduled series of meetings which consists of one or more scheduled meetings based on a
    #: recurrence rule. When a non-recurring meeting is scheduled with no recurrence, its meetingType is also
    #: meetingSeries which is a meeting series with only one occurrence in Webex meeting modeling.
    meeting_series = 'meetingSeries'
    #: Instance from a primary meeting series.
    scheduled_meeting = 'scheduledMeeting'
    #: Meeting instance that is in progress or has completed.
    meeting = 'meeting'


class State(str, Enum):
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


class CallInNumbers(ApiModel):
    #: Label for the call-in number.
    #: Possible values: Call-in toll-free number (US/Canada)
    label: Optional[str]
    #: Call-in number to join the teleconference from a phone.
    #: Possible values: 123456789
    call_in_number: Optional[str]
    #: Type of toll for the call-in number.
    #: Possible values: toll, tollFree
    toll_type: Optional[str]


class Links(ApiModel):
    #: Link relation describing how the target resource is related to the current context (conforming with RFC5998).
    rel: Optional[str]
    #: Target resource URI (conforming with RFC5998).
    href: Optional[str]
    #: Target resource method (conforming with RFC5998).
    method: Optional[str]


class Telephony(ApiModel):
    #: Code for authenticating a user to join teleconference. Users join the teleconference using the call-in number or
    #: the global call-in number, followed by the value of the accessCode.
    access_code: Optional[str]
    #: Array of call-in numbers for joining a teleconference from a phone.
    call_in_numbers: Optional[list[CallInNumbers]]
    #: HATEOAS information of global call-in numbers for joining a teleconference from a phone.
    links: Optional[Links]


class InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting(
    InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting):
    #: Unique identifier for meeting interpreter.
    id: Optional[str]


class SimultaneousInterpretation1(ApiModel):
    #: Whether or not simultaneous interpretation is enabled.
    enabled: Optional[bool]
    #: Interpreters for meeting.
    interpreters: Optional[list[InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting]]


class MeetingSeriesObjectForListMeeting(ApiModel):
    #: Unique identifier for meeting. For a meeting series, the id is used to identify the entire series. For scheduled
    #: meetings from a series, the id is used to identify that scheduled meeting. For a meeting instance that is in
    #: progress or has concluded, the id is used to identify that instance.
    id: Optional[str]
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting
    #: instances which have ended.
    meeting_number: Optional[str]
    #: Meeting title. Can be modified for a meeting series or a scheduled meeting using the Update a Meeting API.
    title: Optional[str]
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long. This attribute can be modified for a
    #: meeting series or a scheduled meeting using the Update a Meeting API.
    agenda: Optional[str]
    #: Meeting password. Applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to
    #: meeting instances which have ended. Can be modified for a meeting series or a scheduled meeting using the Update
    #: a Meeting API.
    password: Optional[str]
    #: 8-digit numeric password used to join a meeting from audio and video devices. This attribute applies to meeting
    #: series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended.
    phone_and_video_system_password: Optional[str]
    #: Meeting type.
    meeting_type: Optional[MeetingType]
    #: Meeting state.
    state: Optional[State]
    #: Time zone of start and end, conforming with the IANA time zone database.
    timezone: Optional[str]
    #: Start time for meeting in ISO 8601 compliant format. If the meetingType of a meeting is meetingSeries, start is
    #: the scheduled start time of the first occurrence of this series. If the meeting is a meeting series and the
    #: current filter is true, start is the date and time the upcoming or ongoing meeting of the series starts. If the
    #: meetingType of a meeting is scheduledMeeting, start is the scheduled start time of this occurrence. If the
    #: meetingType of a meeting is meeting, start is the actual start time of the meeting instance. Can be modified for
    #: a meeting series or a scheduled meeting using the Update a Meeting API.
    start: Optional[str]
    #: End time for a meeting in ISO 8601 compliant format. If the meetingType of a meeting is meetingSeries, end is
    #: the scheduled end time of the first occurrence of this series. If the meeting is a meeting series and the
    #: current filter is true, end is the date and time the upcoming or ongoing meeting of the series ends. If the
    #: meetingType of a meeting is scheduledMeeting, end is the scheduled end time of this occurrence. If the
    #: meetingType of a meeting is meeting, end is the actual end time of the meeting instance. If a meeting instance
    #: is in progress, end is not available. Can be modified for a meeting series or a scheduled meeting using the
    #: Update a Meeting API.
    end: Optional[str]
    #: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring meeting series, not to a
    #: meeting series with only one scheduled meeting. Can be modified for a meeting series using the Update a Meeting
    #: API. Multiple days or dates for monthly or yearly recurrence rule are not supported, only the first day or date
    #: specified is taken. For example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it
    #: will be partially supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
    recurrence: Optional[str]
    #: Unique identifier for the meeting host.
    host_user_id: Optional[str]
    #: Display name for the meeting host.
    host_display_name: Optional[str]
    #: Email address for the meeting host.
    host_email: Optional[str]
    #: Key for joining the meeting as host.
    host_key: Optional[str]
    #: Site URL for the meeting.
    site_url: Optional[str]
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or
    #: join.
    web_link: Optional[str]
    #: SIP address for callback from a video system.
    sip_address: Optional[str]
    #: IP address for callback from a video system.
    dial_in_ip_address: Optional[str]
    #: Room ID of the associated Webex space. Only applies to ad-hoc meetings and space meetings.
    room_id: Optional[str]
    #: Whether or not meeting is recorded automatically. Can be modified for a meeting series or a scheduled meeting
    #: using the Update a Meeting API.
    enabled_auto_record_meeting: Optional[bool]
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: meeting. The target site is specified by a siteUrl parameter when creating the meeting. If not specified, it's a
    #: user's preferred site. The allowAnyUserToBeCoHost attribute can be modified for a meeting series or a scheduled
    #: meeting using the Update a Meeting API.
    allow_any_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The
    #: enabledJoinBeforeHost attribute can be modified for a meeting series or a scheduled meeting using the Update a
    #: Meeting API.
    enabled_join_before_host: Optional[bool]
    #: Whether or not to allow any attendee to connect to audio before the host joins the meeting. Only applicable if
    #: the enabledJoinBeforeHost attribute is set to true. The enableConnectAudioBeforeHost attribute can be modified
    #: for a meeting series or a scheduled meeting using the Update a Meeting API.
    enable_connect_audio_before_host: Optional[bool]
    #: Number of minutes an attendee can join the meeting before the meeting start time and the host joins. Only
    #: applicable if the enabledJoinBeforeHost attribute is set to true. The joinBeforeHostMinutes attribute can be
    #: modified for a meeting series or a scheduled meeting using the Update a Meeting API. Valid options are 0, 5, 10
    #: and 15. Default is 0 if not specified.
    join_before_host_minutes: Optional[int]
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool]
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool]
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    reminder_time: Optional[int]
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    unlocked_meeting_join_security: Optional[UnlockedMeetingJoinSecurity]
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar
    #: meeting. All available meeting session types enabled for the user can be retrieved using the List Meeting
    #: Session Types API.
    session_type_id: Optional[int]
    #: Specifies whether the meeting is a regular meeting, a webinar, or a meeting scheduled in the user's personal
    #: room.
    scheduled_type: Optional[ScheduledType]
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool]
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read
    #: password management for details. If not specified, a random password conforming to the site's password rules
    #: will be generated automatically.
    panelist_password: Optional[str]
    #: 8-digit numeric panelist password to join a webinar meeting from audio and video devices.
    phone_and_video_system_panelist_password: Optional[str]
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool]
    #: The number of minutes after the meeting begins, for automatically locking it.
    automatic_lock_minutes: Optional[int]
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a
    #: cohost. The target site is specified by the siteUrl parameter when creating the meeting. If not specified, it's
    #: a user's preferred site. The allowFirstUserToBeCoHost attribute can be modified for a meeting series or a
    #: scheduled meeting uisng the Update a Meeting API.
    allow_first_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting
    #: without a prompt. This attribute can be modified for a meeting series or a scheduled meeting using the Update a
    #: Meeting API.
    allow_authenticated_devices: Optional[bool]
    #: Information for callbacks from a meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[Telephony]
    #: Meeting options.
    meeting_options: Optional[MeetingOptions]
    #: Attendee Privileges.
    attendee_privileges: Optional[AttendeePrivileges]
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information in order
    #: to join the meeting. Meeting invitees will receive an email with a registration link for the registration. When
    #: the registration form has been submitted and approved, an email with a real meeting link will be received. By
    #: clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not
    #: apply to a meeting when it's a recurring meeting with a recurrence field or no password, or the Join Before Host
    #: option is enabled for the meeting. See Register for a Meeting in Cisco Webex Meetings for details.
    registration: Optional[Registration]
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs,
    #: Salesforce Opportunity IDs, etc.
    integration_tags: Optional[list[str]]
    #: Simultaneous interpretation information for the meeting.
    simultaneous_interpretation: Optional[SimultaneousInterpretation1]
    #: Tracking codes information.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]]
    #: Audio connection options.
    audio_connection_options: Optional[AudioConnectionOptions]


class CreateMeetingResponse(MeetingSeriesObjectForListMeeting):
    #: If true, the meeting is ad-hoc.
    adhoc: Optional[bool]


class Telephony3(ApiModel):
    #: Code for authenticating a user to join teleconference. Users join the teleconference using the call-in number or
    #: the global call-in number, followed by the value of the accessCode.
    access_code: Optional[str]
    #: Array of call-in numbers for joining a teleconference from a phone.
    call_in_numbers: Optional[list[CallInNumbers]]
    #: HATEOAS information of global call-in numbers for joining a teleconference from a phone.
    links: Optional[list[Links]]


class ScheduledMeetingObject(ApiModel):
    #: Unique identifier for meeting. For a meeting series, the id is used to identify the entire series. For scheduled
    #: meetings from a series, the id is used to identify that scheduled meeting. For a meeting instance that is in
    #: progress or has concluded, the id is used to identify that instance.
    id: Optional[str]
    #: Unique identifier for meeting series. It only apples to scheduled meeting and meeting instance. If it's a
    #: scheduled meeting from a series or a meeting instance that is happening or has happened, the meetingSeriesId is
    #: the id of the primary series.
    meeting_series_id: Optional[str]
    #: Unique identifier for scheduled meeting which current meeting is associated with. It only apples to meeting
    #: instance which is happening or has happened. It's the id of the scheduled meeting this instance is associated
    #: with.
    scheduled_meeting_id: Optional[str]
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting
    #: instances which have ended.
    meeting_number: Optional[str]
    #: Meeting title. Can be modified for a meeting series or a scheduled meeting using the Update a Meeting API.
    title: Optional[str]
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long. This attribute can be modified for a
    #: meeting series or a scheduled meeting using the Update a Meeting API.
    agenda: Optional[str]
    #: Meeting password. Applies to meeting series, scheduled meetings, and in-progress meeting instances, but not to
    #: meeting instances which have ended. Can be modified for a meeting series or a scheduled meeting using the Update
    #: a Meeting API.
    password: Optional[str]
    #: 8-digit numeric password used to join a meeting from audio and video devices. This attribute applies to meeting
    #: series, scheduled meetings, and in-progress meeting instances, but not to meeting instances which have ended.
    phone_and_video_system_password: Optional[str]
    #: Meeting type.
    meeting_type: Optional[MeetingType]
    #: Meeting state.
    state: Optional[State]
    #: This state only applies to scheduled meeting. Flag identifying whether or not the scheduled meeting has been
    #: modified.
    is_modified: Optional[bool]
    #: Time zone of start and end, conforming with the IANA time zone database.
    timezone: Optional[str]
    #: Start time for meeting in ISO 8601 compliant format. If the meetingType of a meeting is meetingSeries, start is
    #: the scheduled start time of the first occurrence of this series. If the meeting is a meeting series and the
    #: current filter is true, start is the date and time the upcoming or ongoing meeting of the series starts. If the
    #: meetingType of a meeting is scheduledMeeting, start is the scheduled start time of this occurrence. If the
    #: meetingType of a meeting is meeting, start is the actual start time of the meeting instance. Can be modified for
    #: a meeting series or a scheduled meeting using the Update a Meeting API.
    start: Optional[str]
    #: End time for a meeting in ISO 8601 compliant format. If the meetingType of a meeting is meetingSeries, end is
    #: the scheduled end time of the first occurrence of this series. If the meeting is a meeting series and the
    #: current filter is true, end is the date and time the upcoming or ongoing meeting of the series ends. If the
    #: meetingType of a meeting is scheduledMeeting, end is the scheduled end time of this occurrence. If the
    #: meetingType of a meeting is meeting, end is the actual end time of the meeting instance. If a meeting instance
    #: is in progress, end is not available. Can be modified for a meeting series or a scheduled meeting using the
    #: Update a Meeting API.
    end: Optional[str]
    #: Unique identifier for the meeting host.
    host_user_id: Optional[str]
    #: Display name for the meeting host.
    host_display_name: Optional[str]
    #: Email address for the meeting host.
    host_email: Optional[str]
    #: Key for joining the meeting as host.
    host_key: Optional[str]
    #: Site URL for the meeting.
    site_url: Optional[str]
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or
    #: join.
    web_link: Optional[str]
    #: SIP address for callback from a video system.
    sip_address: Optional[str]
    #: IP address for callback from a video system.
    dial_in_ip_address: Optional[str]
    #: Room ID of the associated Webex space. Only applies to ad-hoc meetings and space meetings.
    room_id: Optional[str]
    #: Whether or not meeting is recorded automatically. Can be modified for a meeting series or a scheduled meeting
    #: using the Update a Meeting API.
    enabled_auto_record_meeting: Optional[bool]
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: meeting. The target site is specified by a siteUrl parameter when creating the meeting. If not specified, it's a
    #: user's preferred site. The allowAnyUserToBeCoHost attribute can be modified for a meeting series or a scheduled
    #: meeting using the Update a Meeting API.
    allow_any_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The
    #: enabledJoinBeforeHost attribute can be modified for a meeting series or a scheduled meeting using the Update a
    #: Meeting API.
    enabled_join_before_host: Optional[bool]
    #: Whether or not to allow any attendee to connect to audio before the host joins the meeting. Only applicable if
    #: the enabledJoinBeforeHost attribute is set to true. The enableConnectAudioBeforeHost attribute can be modified
    #: for a meeting series or a scheduled meeting using the Update a Meeting API.
    enable_connect_audio_before_host: Optional[bool]
    #: The number of minutes an attendee can join the meeting before the meeting start time and the host joins. This
    #: attribute is only applicable if the enabledJoinBeforeHost attribute is set to true. The joinBeforeHostMinutes
    #: attribute can be modified for meeting series or scheduled meeting by Update a Meeting API. Valid options are 0,
    #: 5, 10 and 15. Default is 0 if not specified.
    join_before_host_minutes: Optional[int]
    #: Whether or not to exclude the meeting password from the email invitation.
    exclude_password: Optional[bool]
    #: Whether or not to allow the meeting to be listed on the public calendar.
    public_meeting: Optional[bool]
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host.
    reminder_time: Optional[int]
    #: Specifies how the people who aren't on the invite can join the unlocked meeting.
    unlocked_meeting_join_security: Optional[UnlockedMeetingJoinSecurity]
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar
    #: meeting. All available meeting session types enabled for the user can be retrieved using the List Meeting
    #: Session Types API.
    session_type_id: Optional[int]
    #: Specifies whether the meeting is a regular meeting, a webinar, or a meeting scheduled in the user's personal
    #: room.
    scheduled_type: Optional[ScheduledType]
    #: Whether or not webcast view is enabled.
    enabled_webcast_view: Optional[bool]
    #: Password for panelists of webinar meeting. Must conform to the site's password complexity settings. Read
    #: password management for details. If not specified, a random password conforming to the site's password rules
    #: will be generated automatically.
    panelist_password: Optional[str]
    #: 8-digit numeric panelist password to join webinar meeting from audio and video devices.
    phone_and_video_system_panelist_password: Optional[str]
    #: Whether or not to automatically lock the meeting after it starts.
    enable_automatic_lock: Optional[bool]
    #: The number of minutes after the meeting begins, for automatically locking it.
    automatic_lock_minutes: Optional[int]
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a
    #: cohost. The target site is specified by the siteUrl parameter when creating the meeting. If not specified, it's
    #: a user's preferred site. The allowFirstUserToBeCoHost attribute can be modified for a meeting series or a
    #: scheduled meeting uisng the Update a Meeting API.
    allow_first_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting
    #: without a prompt. This attribute can be modified for a meeting series or a scheduled meeting using the Update a
    #: Meeting API.
    allow_authenticated_devices: Optional[bool]
    #: Information for callbacks from a meeting to phone or for joining a teleconference using a phone.
    telephony: Optional[Telephony3]
    #: Meeting Options.
    meeting_options: Optional[MeetingOptions]
    #: Attendee Privileges.
    attendee_privileges: Optional[AttendeePrivileges]
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information to join
    #: the meeting. Meeting invitees will receive an email with a registration link for the registration. When the
    #: registration form has been submitted and approved, an email with a real meeting link will be received. By
    #: clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not
    #: apply to a meeting when it's a recurring meeting with a recurrence field or no password, or the Join Before Host
    #: option is enabled for the meeting. See Register for a Meeting in Cisco Webex Meetings for details. +
    #: autoAcceptRequest: false (boolean,optional) - Whether or not meeting registration requests are accepted
    #: automatically.
    registration: Optional[Registration]
    #: External keys created by an integration application in its domain, for example, Zendesk ticket IDs, Jira IDs,
    #: Salesforce Opportunity IDs, etc.
    integration_tags: Optional[list[str]]
    #: Whether or not breakout sessions are enabled.
    enabled_breakout_sessions: Optional[bool]
    #: HATEOAS Breakout Sessions information for meeting.
    links: Optional[list[Links]]
    #: Tracking codes information.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]]
    #: Audio connection options.
    audio_connection_options: Optional[AudioConnectionOptions]


class PatchMeetingResponse(MeetingSeriesObjectForListMeeting):
    #: Whether or not breakout sessions are enabled.
    enabled_breakout_sessions: Optional[bool]
    #: HATEOAS Breakout Sessions information for meeting.
    links: Optional[list[Links]]


class TemplateObject(ApiModel):
    #: Unique identifier for meeting template.
    id: Optional[str]
    #: Meeting template name.
    name: Optional[str]
    #: Meeting template locale.
    locale: Optional[str]
    #: Site URL for the meeting template.
    site_url: Optional[str]
    #: Meeting template type.
    template_type: Optional[TemplateType]
    #: Whether or not the meeting template is a default template.
    is_default: Optional[bool]
    #: Whether or not the meeting template is a standard template.
    is_standard: Optional[bool]


class CreateMeetingBody(PatchMeetingBody):
    #: Whether or not to create an ad-hoc meeting for the room specified by roomId. When true, roomId is required.
    adhoc: Optional[bool]
    #: Unique identifier for the Webex space which the meeting is to be associated with. It can be retrieved by List
    #: Rooms. roomId is required when adhoc is true. When roomId is specified, the parameter hostEmail will be ignored.
    room_id: Optional[str]
    #: Unique identifier for meeting template. Please note that start and end are optional when templateId is
    #: specified. The list of meeting templates that is available for the authenticated user can be retrieved from List
    #: Meeting Templates. This parameter is ignored for an ad-hoc meeting.
    template_id: Optional[str]
    #: When set as an attribute in a POST request body, specifies whether it's a regular meeting, a webinar, or a
    #: meeting scheduled in the user's personal room. If not specified, it's a regular meeting by default. The default
    #: value for an ad-hoc meeting is meeting and the user's input value will be ignored.
    scheduled_type: Optional[ScheduledType]
    #: Invitees for meeting. The maximum size of invitees is 1000. If roomId is specified and invitees is missing, all
    #: the members in the space are invited implicitly. If both roomId and invitees are specified, only those in the
    #: invitees list are invited. coHost for each invitee is true by default if roomId is specified when creating a
    #: meeting, and anyone in the invitee list that is not qualified to be a cohost will be invited as a non-cohost
    #: invitee. The user's input value will be ignored for an ad-hoc meeting and the the members of the room specified
    #: by roomId except "me" will be used by default.
    invitees: Optional[list[InviteeObjectForCreateMeeting]]
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information to join
    #: the meeting. Meeting invitees will receive an email with a registration link for the registration. When the
    #: registration form has been submitted and approved, an email with a real meeting link will be received. By
    #: clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not
    #: apply to a meeting when it's a recurring meeting with a recurrence field or no password, or the Join Before Host
    #: option is enabled for the meeting. See Register for a Meeting in Cisco Webex Meetings for details. This
    #: parameter is ignored for an ad-hoc meeting.
    registration: Optional[Registration]
    #: Simultaneous interpretation information for a meeting.
    simultaneous_interpretation: Optional[SimultaneousInterpretation]
    #: Breakout sessions are smaller groups that are split off from the main meeting or webinar. They allow a subset of
    #: participants to collaborate and share ideas over audio and video. Use breakout sessions for workshops,
    #: classrooms, or for when you need a moment to talk privately with a few participants outside of the main session.
    #: Please note that maximum number of breakout sessions in a meeting or webinar is 100. In webinars, if hosts
    #: preassign attendees to breakout sessions, the role of attendee will be changed to panelist. Breakout session is
    #: not supported for a meeting with simultaneous interpretation.
    breakout_sessions: Optional[list[BreakoutSessionObject]]


class GetMeetingControlStatusResponse(ApiModel):
    #: Whether the meeting is locked or not.
    locked: Optional[bool]
    #: The value can be true or false, it indicates the meeting recording started or not.
    recording_started: Optional[bool]
    #: The value can be true or false, it indicates the meeting recording paused or not.
    recording_paused: Optional[bool]


class Type4(TemplateType):
    #: Meeting session type for a private meeting.
    private_meeting = 'privateMeeting'


class MeetingSessionTypeObject(ApiModel):
    #: Unique identifier for the meeting session type.
    id: Optional[str]
    #: Name of the meeting session type.
    name: Optional[str]
    #: Meeting session type.
    type: Optional[Type4]
    #: The maximum number of attendees for the meeting session type.
    attendees_capacity: Optional[int]


class CustomizedQuestionForGetMeeting(CustomizedQuestionForCreateMeeting):
    #: Unique identifier for the question.
    id: Optional[int]


class GetRegistrationFormFormeetingResponse(ApiModel):
    #: Whether or not a registrant's first name is required for meeting registration. This option must always be true.
    require_first_name: Optional[bool]
    #: Whether or not a registrant's last name is required for meeting registration. This option must always be true.
    require_last_name: Optional[bool]
    #: Whether or not a registrant's email is required for meeting registration. This option must always be true.
    require_email: Optional[bool]
    #: Whether or not a registrant's job title is shown or required for meeting registration.
    require_job_title: Optional[bool]
    #: Whether or not a registrant's company name is shown or required for meeting registration.
    require_company_name: Optional[bool]
    #: Whether or not a registrant's first address field is shown or required for meeting registration.
    require_address1: Optional[bool]
    #: Whether or not a registrant's second address field is shown or required for meeting registration.
    require_address2: Optional[bool]
    #: Whether or not a registrant's city is shown or required for meeting registration.
    require_city: Optional[bool]
    #: Whether or not a registrant's state is shown or required for meeting registration.
    require_state: Optional[bool]
    #: Whether or not a registrant's postal code is shown or required for meeting registration.
    require_zip_code: Optional[bool]
    #: Whether or not a registrant's country or region is shown or required for meeting registration.
    require_country_region: Optional[bool]
    #: Whether or not a registrant's work phone number is shown or required for meeting registration.
    require_work_phone: Optional[bool]
    #: Whether or not a registrant's fax number is shown or required for meeting registration.
    require_fax: Optional[bool]
    #: Customized questions for meeting registration.
    customized_questions: Optional[list[CustomizedQuestionForGetMeeting]]
    #: The approval rules for standard questions.
    rules: Optional[list[StandardRegistrationApproveRule]]


class AnswerForCustomizedQuestion(ApiModel):
    #: Unique identifier for the option.
    option_id: Optional[int]
    #: The content of the answer or the option for this question.
    answer: Optional[str]


class CustomizedRegistrant(ApiModel):
    #: Unique identifier for the customized questions retrieved from the registration form.
    question_id: Optional[int]
    #: The answers for customized questions. If the question type is checkbox, more than one answer can be set.
    answers: Optional[list[AnswerForCustomizedQuestion]]


class Status(str, Enum):
    #: Registrant has been approved.
    approved = 'approved'
    #: Registrant is in a pending list waiting for host or cohost approval.
    pending = 'pending'
    #: Registrant has been rejected by the host or cohost.
    rejected = 'rejected'


class RegisterMeetingRegistrantBody(Question):
    #: The registrant's first name.
    first_name: Optional[str]
    #: If true send email to the registrant. Default: true.
    send_email: Optional[bool]
    #: The registrant's answers for customized questions. Registration options define whether or not this is required.
    customized_questions: Optional[list[CustomizedRegistrant]]


class RegisterMeetingRegistrantResponse(Question):
    #: New registrant's ID.
    id: Optional[str]
    #: New registrant's status.
    status: Optional[Status]
    #: Registrant's first name.
    first_name: Optional[str]
    #: Registrant's registration time.
    registration_time: Optional[str]
    #: Registrant's answers for customized questions, Registration options define whether or not this is required.
    customized_questions: Optional[list[CustomizedRegistrant]]


class GetmeetingRegistrantsDetailInformationResponse(Question):
    #: New registrant's ID.
    registrant_id: Optional[str]
    #: New registrant's status.
    status: Optional[Status]
    #: Registrant's first name.
    first_name: Optional[str]
    #: Registrant's registration time.
    registration_time: Optional[str]
    #: Registrant's answers for customized questions, Registration options define whether or not this is required.
    customized_questions: Optional[list[CustomizedRegistrant]]
    #: Registrant's source id.The sourceId is from Create Invitation Sources API.
    source_id: Optional[str]


class OrderType(str, Enum):
    desc = 'DESC'
    asc = 'ASC'


class OrderBy(str, Enum):
    #: Registrant's first name.
    first_name = 'firstName'
    #: Registrant's last name.
    last_name = 'lastName'
    #: Registrant's status.
    status = 'status'
    #: registrant's email.
    email = 'email'


class CreateMeetingInterpreterBody(InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting):
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin on-behalf-of scopes. When used, the admin may specify the email of a user in a site they manage to
    #: be the meeting host.
    host_email: Optional[str]
    #: If true, send email to the interpreter.
    send_email: Optional[bool]


class GetBreakoutSessionObject(BreakoutSessionObject):
    #: Unique identifier for breakout session.
    id: Optional[str]


class Type9(str, Enum):
    #: Text input.
    text = 'text'
    #: Rating.
    rating = 'rating'
    #: Check box which requires options.
    checkbox = 'checkbox'
    #: Drop down list box which requires options.
    single_dropdown = 'singleDropdown'
    #: Single radio button which requires options.
    single_radio = 'singleRadio'


class Options(ApiModel):
    #: The unique id of options.
    #: Possible values: 1
    id: Optional[int]
    #: The content of the option.
    #: Possible values: green
    value: Optional[str]


class QuestionObject(ApiModel):
    #: Unique identifier for the question.
    id: Optional[int]
    #: Details for the question.
    question: Optional[str]
    #: Type for the question.
    type: Optional[Type9]
    #: The lowest score of the rating question. This attribute will be ingnored, if the value of type attribute is not
    #: rating.
    from_score: Optional[int]
    #: The lowest score label of the rating question. This attribute will be ingnored, if the value of type attribute
    #: is not rating.
    from_label: Optional[str]
    #: The highest score of the rating question. This attribute will be ingnored, if the value of type attribute is not
    #: rating.
    to_score: Optional[int]
    #: The highest score label of the rating question. This attribute will be ingnored, if the value of type attribute
    #: is not rating.
    to_label: Optional[str]
    #: Options for the question. This attribute will be ingnored, if the value of type attribute is text or rating.
    options: Optional[list[Options]]


class QuestionWithAnswersObject(ApiModel):
    #: Unique identifier for the question.
    id: Optional[int]
    #: Details for the question.
    question: Optional[str]
    #: Type for the question.
    type: Optional[Type9]
    #: The user's answers for the question.
    answers: Optional[list[AnswerForCustomizedQuestion]]


class SurveyResultObject(ApiModel):
    #: Unique identifier for the survey result.
    id: Optional[str]
    #: Name for the survey.
    survey_name: Optional[str]
    #: Unique identifier for the meeting.
    meeting_id: Optional[str]
    #: Email address of the user who submits the survey.
    email: Optional[str]
    #: Name of the user who submits the survey.
    display_name: Optional[str]
    #: The time when the user submits the survey.
    create_time: Optional[str]
    #: User's answers for the questions
    questions: Optional[list[QuestionWithAnswersObject]]


class InvitationSourceCreateObject(ApiModel):
    #: Source ID for the invitation.
    source_id: Optional[str]
    #: Email for invitation source.
    source_email: Optional[str]


class InvitationSourceObject(InvitationSourceCreateObject):
    #: Unique identifier for invitation source.
    id: Optional[str]
    #: The link bound to sourceId can directly join the meeting.If the meeting requires registration,joinLink is not
    #: returned.
    join_link: Optional[str]
    #: The link bound to sourceId can directly register the meeting.If the meeting requires registration,registerLink
    #: is returned.
    register_link: Optional[str]


class OptionsForTrackingCodeObject(ApiModel):
    #: The value of a tracking code option. value cannot be empty and the maximum size is 120 characters.
    value: Optional[str]
    #: Whether or not the option is the default option of a tracking code.
    default_value: Optional[bool]


class InputMode(str, Enum):
    #: Text input.
    text = 'text'
    #: Drop down list which requires options.
    select = 'select'
    #: Both text input and select from list.
    editable_select = 'editableSelect'
    #: An input method which is only available for the host profile and sign-up pages.
    host_profile_select = 'hostProfileSelect'


class Service(str, Enum):
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


class Type11(str, Enum):
    #: Available to be chosen but not compulsory.
    optional = 'optional'
    #: Officially compulsory.
    required = 'required'
    #: The value is set by admin.
    admin_set = 'adminSet'
    #: The value cannot be used.
    not_used = 'notUsed'
    #: This value only applies to the service of All. When the type of All for a tracking code is notApplicable, there
    #: are different types for different services. For example, required for MeetingCenter, optional for EventCenter
    #: and notUsed for others.
    not_applicable = 'notApplicable'


class ListMeetingsResponse(ApiModel):
    #: Meetings array.
    items: Optional[list[MeetingSeriesObjectForListMeeting]]


class ListMeetingsOfMeetingSeriesResponse(ApiModel):
    #: Meetings array.
    items: Optional[list[ScheduledMeetingObject]]


class JoinMeetingBody(ApiModel):
    #: Unique identifier for the meeting. This parameter applies to meeting series and scheduled meetings. It doesn't
    #: apply to ended or in-progress meeting instances. Please note that currently meeting ID of a scheduled personal
    #: room meeting is also supported for this API.
    meeting_id: Optional[str]
    #: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but not to meeting
    #: instances which have ended.
    meeting_number: Optional[str]
    #: Link to a meeting information page where the meeting client is launched if the meeting is ready to start or
    #: join.
    web_link: Optional[str]
    #: Whether or not to redirect to joinLink. It is an optional field and default value is true.
    join_directly: Optional[bool]
    #: Email address of meeting participant. If the user is a guest issuer, email is required.
    email: Optional[str]
    #: Display name of meeting participant. The maximum length of displayName is 128 characters. If the user is a guest
    #: issuer, displayName is required.
    display_name: Optional[str]
    #: It's required when the meeting is protected by a password and the current user is not privileged to view it if
    #: they are not a host, cohost or invitee of the meeting.
    password: Optional[str]
    #: Expiration duration of joinLink in minutes. Must be between 1 and 60.
    expiration_minutes: Optional[int]


class JoinMeetingResponse(ApiModel):
    #: The link can directly join or host the meeting.
    join_link: Optional[str]
    #: Expiration time of joinLink.
    expiration: Optional[str]


class ListMeetingTemplatesResponse(ApiModel):
    #: Meeting templates array.
    items: Optional[list[TemplateObject]]


class GetMeetingTemplateResponse(TemplateObject):
    #: Meeting object which is used to create a meeting by the meeting template. Please note that the meeting object
    #: should be used to create a meeting immediately after retrieval since the start and end may be invalid quickly
    #: after generation.
    meeting: Optional[CreateMeetingBody]


class ListMeetingSessionTypesResponse(ApiModel):
    #: Meeting session type array
    items: Optional[list[MeetingSessionTypeObject]]


class UpdateMeetingRegistrationFormBody(ApiModel):
    host_email: Optional[str]
    #: Whether or not a registrant's first name is required for meeting registration. This option must always be true.
    require_first_name: Optional[bool]
    #: Whether or not a registrant's last name is required for meeting registration. This option must always be true.
    require_last_name: Optional[bool]
    #: Whether or not a registrant's email is required for meeting registration. This option must always be true.
    require_email: Optional[bool]
    #: Whether or not a registrant's job title is shown or required for meeting registration.
    require_job_title: Optional[bool]
    #: Whether or not a registrant's company name is shown or required for meeting registration.
    require_company_name: Optional[bool]
    #: Whether or not a registrant's first address field is shown or required for meeting registration.
    require_address1: Optional[bool]
    #: Whether or not a registrant's second address field is shown or required for meeting registration.
    require_address2: Optional[bool]
    #: Whether or not a registrant's city is shown or required for meeting registration.
    require_city: Optional[bool]
    #: Whether or not a registrant's state is shown or required for meeting registration.
    require_state: Optional[bool]
    #: Whether or not a registrant's postal code is shown or required for meeting registration.
    require_zip_code: Optional[bool]
    #: Whether or not a registrant's country or region is shown or required for meeting registration.
    require_country_region: Optional[bool]
    #: Whether or not a registrant's work phone number is shown or required for meeting registration.
    require_work_phone: Optional[bool]
    #: Whether or not a registrant's fax number is shown or required for meeting registration.
    require_fax: Optional[bool]
    #: The maximum number of meeting registrations. Only applies to meetings. Webinars use a default value of 10000. If
    #: the maximum capacity of attendees for a webinar is less than 10000, e.g. 3000, then at most 3000 registrants can
    #: join this webinar.
    max_register_num: Optional[int]
    #: Customized questions for meeting registration.
    customized_questions: Optional[list[CustomizedQuestionForCreateMeeting]]
    #: The approval rule for standard questions.
    rules: Optional[list[StandardRegistrationApproveRule]]


class BatchRegisterMeetingRegistrantsBody(ApiModel):
    #: Registrants array.
    items: Optional[list[RegisterMeetingRegistrantBody]]


class BatchRegisterMeetingRegistrantsResponse(ApiModel):
    items: Optional[list[RegisterMeetingRegistrantResponse]]


class ListMeetingRegistrantsResponse(ApiModel):
    #: Registrants array.
    items: Optional[list[GetmeetingRegistrantsDetailInformationResponse]]


class QueryMeetingRegistrantsBody(ApiModel):
    #: Registrant's status.
    status: Optional[Status]
    #: Sort order for the registrants.
    order_type: Optional[OrderType]
    #: Registrant ordering field. Ordered by registrationTime by default.
    order_by: Optional[OrderBy]
    #: List of registrant email addresses.
    #: Possible values: bob@example.com
    emails: Optional[list[str]]


class QueryMeetingRegistrantsResponse(ApiModel):
    #: Registrants array.
    items: Optional[list[GetmeetingRegistrantsDetailInformationResponse]]


class BatchUpdateMeetingRegistrantsStatusBody(ApiModel):
    #: If true send email to registrants. Default: true.
    send_email: Optional[bool]
    #: Registrants array.
    #: Registrant ID.
    registrants: Optional[list[str]]


class ListMeetingInterpretersResponse(ApiModel):
    #: Array of meeting interpreters.
    items: Optional[list[InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting]]


class UpdateMeetingBreakoutSessionsBody(ApiModel):
    #: Email address for the meeting host. This parameter is only used if the user or application calling the API has
    #: the admin-level scopes. If set, the admin may specify the email of a user in a site they manage and the API will
    #: return details for a meeting that is hosted by that user.
    host_email: Optional[str]
    #: Whether or not to send emails to host and invitees. It is an optional field and default value is true.
    send_email: Optional[bool]
    #: Breakout sessions are smaller groups that are split off from the main meeting or webinar. They allow a subset of
    #: participants to collaborate and share ideas over audio and video. Use breakout sessions for workshops,
    #: classrooms, or for when you need a moment to talk privately with a few participants outside of the main session.
    #: Please note that maximum number of breakout sessions in a meeting or webinar is 100. In webinars, if hosts
    #: preassign attendees to breakout sessions, the role of attendee will be changed to panelist. Breakout session is
    #: not supported for a meeting with simultaneous interpretation.
    items: Optional[list[BreakoutSessionObject]]


class UpdateMeetingBreakoutSessionsResponse(ApiModel):
    #: Breakout Sessions information for meeting.
    items: Optional[list[GetBreakoutSessionObject]]


class ListMeetingBreakoutSessionsResponse(ApiModel):
    #: Breakout Sessions information for meeting.
    items: Optional[list[GetBreakoutSessionObject]]


class GetMeetingSurveyResponse(ApiModel):
    #: Unique identifier for the survey.
    id: Optional[str]
    #: Name for the survey.
    survey_name: Optional[str]
    #: Unique identifier for the meeting.
    meeting_id: Optional[str]
    #: Description for the survey.
    description: Optional[str]
    #: Whether the survey allows attendees to submit anonymously.
    allow_anonymous_submit: Optional[bool]
    #: Questions for the survey.
    questions: Optional[list[QuestionObject]]


class ListMeetingSurveyResultsResponse(ApiModel):
    #: SurveyResult array
    items: Optional[list[SurveyResultObject]]


class CreateInvitationSourcesBody(ApiModel):
    #: Email address for the meeting host. This parameter is only used if a user or application calling the API has the
    #: admin-level scopes. The admin may specify the email of a user on a site they manage and the API will return
    #: meeting participants of the meetings that are hosted by that user.
    host_email: Optional[str]
    #: Unique identifier for the meeting host. Should only be set if the user or application calling the API has the
    #: admin-level scopes. When used, the admin may specify the email of a user in a site they manage to be the meeting
    #: host.
    person_id: Optional[str]
    items: Optional[list[InvitationSourceCreateObject]]


class CreateInvitationSourcesResponse(ApiModel):
    #: Invitation source array.
    items: Optional[list[InvitationSourceObject]]


class ListInvitationSourcesResponse(ApiModel):
    #: Invitation source array.
    items: Optional[list[InvitationSourceObject]]


class ListMeetingTrackingCodesResponse(ApiModel):
    #: Unique identifier for the tracking code.
    id: Optional[str]
    #: Name for the tracking code.
    name: Optional[str]
    #: Site URL for the tracking code.
    site_url: Optional[str]
    #: Tracking code option list. The options here differ from those in the site-level tracking codes and the
    #: user-level tracking codes. It is the result of a selective combination of the two. If there's user-level value
    #: for a tracking code, the user-level value becomes the default option for the tracking code, and the site-level
    #: default value becomes non-default.
    options: Optional[list[OptionsForTrackingCodeObject]]
    #: The input mode in which the tracking code value can be assigned.
    input_mode: Optional[InputMode]
    #: Service for schedule or sign up pages
    service: Optional[Service]
    #: Type for meeting scheduler or meeting start pages.
    type: Optional[Type11]


class MeetingsApi(ApiChild, base='meetings'):
    """
    Meetings are virtual conferences where users can collaborate in real time using audio, video, content sharing,
    chat, online whiteboards, and to collaborate.
    This API focuses primarily on the scheduling and management of meetings. You can use the Meetings API to list,
    create, get, update, and delete meetings.
    Several types of meeting objects are supported by this API, such as meeting series, scheduled meeting, and ended or
    in-progress meeting instances. See the Meetings Overview for more information about the types of meetings.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    """

    def create(self, title: str = None, agenda: str = None, password: str = None, start: str = None, end: str = None,
               timezone: str = None, recurrence: str = None, enabled_auto_record_meeting: bool = None,
               allow_any_user_to_be_co_host: bool = None, enabled_join_before_host: bool = None,
               enable_connect_audio_before_host: bool = None, join_before_host_minutes: int = None,
               exclude_password: bool = None, public_meeting: bool = None, reminder_time: int = None,
               unlocked_meeting_join_security: UnlockedMeetingJoinSecurity = None, session_type_id: int = None,
               enabled_webcast_view: bool = None, panelist_password: str = None, enable_automatic_lock: bool = None,
               automatic_lock_minutes: int = None, allow_first_user_to_be_co_host: bool = None,
               allow_authenticated_devices: bool = None, send_email: bool = None, host_email: str = None,
               site_url: str = None, meeting_options: MeetingOptions = None,
               attendee_privileges: AttendeePrivileges = None, integration_tags: List[str] = None,
               enabled_breakout_sessions: bool = None, tracking_codes: TrackingCodeItemForCreateMeetingObject = None,
               audio_connection_options: AudioConnectionOptions = None, adhoc: bool = None, room_id: str = None,
               template_id: str = None, scheduled_type: ScheduledType = None,
               invitees: InviteeObjectForCreateMeeting = None, registration: Registration = None,
               simultaneous_interpretation: SimultaneousInterpretation = None,
               breakout_sessions: BreakoutSessionObject = None) -> CreateMeetingResponse:
        """
        Creates a new meeting. Regular users can schedule up to 100 meetings in 24 hours and admin users up to 3000.

        :param title: Meeting title. The title can be a maximum of 128 characters long.
        :type title: str
        :param agenda: Meeting agenda. The agenda can be a maximum of 1300 characters long.
        :type agenda: str
        :param password: Meeting password. Must conform to the site's password complexity settings. Read password
            management for details.
        :type password: str
        :param start: Date and time for the start of meeting in any ISO 8601 compliant format. start cannot be before
            current date and time or after end. Duration between start and end cannot be shorter than 10 minutes or
            longer than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating
            date and time for a meeting. Please note that when a meeting is being updated, start of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, if start is within the same minute as the
            current time, start will be adjusted to the upcoming minute; otherwise, start will be adjusted with seconds
            and milliseconds stripped off. For instance, if the current time is 2022-03-01T10:32:16.657+08:00, start of
            2022-03-01T10:32:28.076+08:00 or 2022-03-01T10:32:41+08:00 will be adjusted to 2022-03-01T10:33:00+08:00,
            and start of 2022-03-01T11:32:28.076+08:00 or 2022-03-01T11:32:41+08:00 will be adjusted to
            2022-03-01T11:32:00+08:00.
        :type start: str
        :param end: Date and time for the end of meeting in any ISO 8601 compliant format. end cannot be before current
            date and time or before start. Duration between start and end cannot be shorter than 10 minutes or longer
            than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating date
            and time for a meeting. Please note that when a meeting is being updated, end of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, end will be adjusted with seconds and
            milliseconds stripped off. For instance, end of 2022-03-01T11:52:28.076+08:00 or 2022-03-01T11:52:41+08:00
            will be adjusted to 2022-03-01T11:52:00+08:00.
        :type end: str
        :param timezone: Time zone in which the meeting was originally scheduled (conforming with the IANA time zone
            database).
        :type timezone: str
        :param recurrence: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring
            meeting series, not to a meeting series with only one scheduled meeting. Multiple days or dates for monthly
            or yearly recurrence rule are not supported, only the first day or date specified is taken. For example,
            "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported
            as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
        :type recurrence: str
        :param enabled_auto_record_meeting: Whether or not meeting is recorded automatically.
        :type enabled_auto_record_meeting: bool
        :param allow_any_user_to_be_co_host: Whether or not to allow any attendee with a host account on the target
            site to become a cohost when joining the meeting. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_any_user_to_be_co_host: bool
        :param enabled_join_before_host: Whether or not to allow any attendee to join the meeting before the host joins
            the meeting.
        :type enabled_join_before_host: bool
        :param enable_connect_audio_before_host: Whether or not to allow any attendee to connect audio in the meeting
            before the host joins the meeting. This attribute is only applicable if the enabledJoinBeforeHost attribute
            is set to true.
        :type enable_connect_audio_before_host: bool
        :param join_before_host_minutes: The number of minutes an attendee can join the meeting before the meeting
            start time and the host joins. This attribute is only applicable if the enabledJoinBeforeHost attribute is
            set to true. Valid options are 0, 5, 10 and 15. Default is 0 if not specified.
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
        :type unlocked_meeting_join_security: UnlockedMeetingJoinSecurity
        :param session_type_id: Unique identifier for a meeting session type for the user. This attribute is required
            while scheduling webinar meeting. All available meeting session types enabled for the user can be retrieved
            by List Meeting Session Types API.
        :type session_type_id: int
        :param enabled_webcast_view: Whether or not webcast view is enabled.
        :type enabled_webcast_view: bool
        :param panelist_password: Password for panelists of a webinar meeting. Must conform to the site's password
            complexity settings. Read password management for details. If not specified, a random password conforming
            to the site's password rules will be generated automatically.
        :type panelist_password: str
        :param enable_automatic_lock: Whether or not to automatically lock the meeting after it starts.
        :type enable_automatic_lock: bool
        :param automatic_lock_minutes: The number of minutes after the meeting begins, for automatically locking it.
        :type automatic_lock_minutes: int
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee of the meeting with a host
            account on the target site to become a cohost. The target site is specified by siteUrl parameter when
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
            user in a site they manage to be the meeting host.
        :type host_email: str
        :param site_url: URL of the Webex site which the meeting is updated on. If not specified, the meeting is
            created on user's preferred site. All available Webex sites and preferred site of the user can be retrieved
            by Get Site List API.
        :type site_url: str
        :param meeting_options: Meeting Options.
        :type meeting_options: MeetingOptions
        :param attendee_privileges: Attendee Privileges.
        :type attendee_privileges: AttendeePrivileges
        :param integration_tags: External keys created by an integration application in its own domain, for example
            Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries meetings
            by a key in its own domain. The maximum size of integrationTags is 3 and each item of integrationTags can
            be a maximum of 64 characters long. Please note that an empty or null integrationTags will delete all
            existing integration tags for the meeting implicitly. Developer can update integration tags for a
            meetingSeries but he cannot update it for a scheduledMeeting or a meeting instance.
        :type integration_tags: List[str]
        :param enabled_breakout_sessions: Whether or not breakout sessions are enabled. If the value of
            enabledBreakoutSessions is false, users can not set breakout sessions. If the value of
            enabledBreakoutSessions is true, users can update breakout sessions using the Update Breakout Sessions API.
            Updating breakout sessions are not supported by this API.
        :type enabled_breakout_sessions: bool
        :param tracking_codes: Tracking codes information. All available tracking codes and their options for the
            specified site can be retrieved by List Meeting Tracking Codes API. If an optional tracking code is missing
            from the trackingCodes array and there's a default option for this tracking code, the default option is
            assigned automatically. If the inputMode of a tracking code is select, its value must be one of the
            site-level options or the user-level value. Tracking code is not supported for a personal room meeting or
            an ad-hoc space meeting.
        :type tracking_codes: TrackingCodeItemForCreateMeetingObject
        :param audio_connection_options: Audio connection options.
        :type audio_connection_options: AudioConnectionOptions
        :param adhoc: Whether or not to create an ad-hoc meeting for the room specified by roomId. When true, roomId is
            required.
        :type adhoc: bool
        :param room_id: Unique identifier for the Webex space which the meeting is to be associated with. It can be
            retrieved by List Rooms. roomId is required when adhoc is true. When roomId is specified, the parameter
            hostEmail will be ignored.
        :type room_id: str
        :param template_id: Unique identifier for meeting template. Please note that start and end are optional when
            templateId is specified. The list of meeting templates that is available for the authenticated user can be
            retrieved from List Meeting Templates. This parameter is ignored for an ad-hoc meeting.
        :type template_id: str
        :param scheduled_type: When set as an attribute in a POST request body, specifies whether it's a regular
            meeting, a webinar, or a meeting scheduled in the user's personal room. If not specified, it's a regular
            meeting by default. The default value for an ad-hoc meeting is meeting and the user's input value will be
            ignored.
        :type scheduled_type: ScheduledType
        :param invitees: Invitees for meeting. The maximum size of invitees is 1000. If roomId is specified and
            invitees is missing, all the members in the space are invited implicitly. If both roomId and invitees are
            specified, only those in the invitees list are invited. coHost for each invitee is true by default if
            roomId is specified when creating a meeting, and anyone in the invitee list that is not qualified to be a
            cohost will be invited as a non-cohost invitee. The user's input value will be ignored for an ad-hoc
            meeting and the the members of the room specified by roomId except "me" will be used by default.
        :type invitees: InviteeObjectForCreateMeeting
        :param registration: Meeting registration. When this option is enabled, meeting invitees must register personal
            information to join the meeting. Meeting invitees will receive an email with a registration link for the
            registration. When the registration form has been submitted and approved, an email with a real meeting link
            will be received. By clicking that link the meeting invitee can join the meeting. Please note that meeting
            registration does not apply to a meeting when it's a recurring meeting with a recurrence field or no
            password, or the Join Before Host option is enabled for the meeting. See Register for a Meeting in Cisco
            Webex Meetings for details. This parameter is ignored for an ad-hoc meeting.
        :type registration: Registration
        :param simultaneous_interpretation: Simultaneous interpretation information for a meeting.
        :type simultaneous_interpretation: SimultaneousInterpretation
        :param breakout_sessions: Breakout sessions are smaller groups that are split off from the main meeting or
            webinar. They allow a subset of participants to collaborate and share ideas over audio and video. Use
            breakout sessions for workshops, classrooms, or for when you need a moment to talk privately with a few
            participants outside of the main session. Please note that maximum number of breakout sessions in a meeting
            or webinar is 100. In webinars, if hosts preassign attendees to breakout sessions, the role of attendee
            will be changed to panelist. Breakout session is not supported for a meeting with simultaneous
            interpretation.
        :type breakout_sessions: BreakoutSessionObject

        documentation: https://developer.webex.com/docs/api/v1/meetings/create-a-meeting
        """
        body = CreateMeetingBody()
        if title is not None:
            body.title = title
        if agenda is not None:
            body.agenda = agenda
        if password is not None:
            body.password = password
        if start is not None:
            body.start = start
        if end is not None:
            body.end = end
        if timezone is not None:
            body.timezone = timezone
        if recurrence is not None:
            body.recurrence = recurrence
        if enabled_auto_record_meeting is not None:
            body.enabled_auto_record_meeting = enabled_auto_record_meeting
        if allow_any_user_to_be_co_host is not None:
            body.allow_any_user_to_be_co_host = allow_any_user_to_be_co_host
        if enabled_join_before_host is not None:
            body.enabled_join_before_host = enabled_join_before_host
        if enable_connect_audio_before_host is not None:
            body.enable_connect_audio_before_host = enable_connect_audio_before_host
        if join_before_host_minutes is not None:
            body.join_before_host_minutes = join_before_host_minutes
        if exclude_password is not None:
            body.exclude_password = exclude_password
        if public_meeting is not None:
            body.public_meeting = public_meeting
        if reminder_time is not None:
            body.reminder_time = reminder_time
        if unlocked_meeting_join_security is not None:
            body.unlocked_meeting_join_security = unlocked_meeting_join_security
        if session_type_id is not None:
            body.session_type_id = session_type_id
        if enabled_webcast_view is not None:
            body.enabled_webcast_view = enabled_webcast_view
        if panelist_password is not None:
            body.panelist_password = panelist_password
        if enable_automatic_lock is not None:
            body.enable_automatic_lock = enable_automatic_lock
        if automatic_lock_minutes is not None:
            body.automatic_lock_minutes = automatic_lock_minutes
        if allow_first_user_to_be_co_host is not None:
            body.allow_first_user_to_be_co_host = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body.allow_authenticated_devices = allow_authenticated_devices
        if send_email is not None:
            body.send_email = send_email
        if host_email is not None:
            body.host_email = host_email
        if site_url is not None:
            body.site_url = site_url
        if meeting_options is not None:
            body.meeting_options = meeting_options
        if attendee_privileges is not None:
            body.attendee_privileges = attendee_privileges
        if integration_tags is not None:
            body.integration_tags = integration_tags
        if enabled_breakout_sessions is not None:
            body.enabled_breakout_sessions = enabled_breakout_sessions
        if tracking_codes is not None:
            body.tracking_codes = tracking_codes
        if audio_connection_options is not None:
            body.audio_connection_options = audio_connection_options
        if adhoc is not None:
            body.adhoc = adhoc
        if room_id is not None:
            body.room_id = room_id
        if template_id is not None:
            body.template_id = template_id
        if scheduled_type is not None:
            body.scheduled_type = scheduled_type
        if invitees is not None:
            body.invitees = invitees
        if registration is not None:
            body.registration = registration
        if simultaneous_interpretation is not None:
            body.simultaneous_interpretation = simultaneous_interpretation
        if breakout_sessions is not None:
            body.breakout_sessions = breakout_sessions
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return CreateMeetingResponse.parse_obj(data)

    def details(self, meeting_id: str, current: bool = None, host_email: str = None) -> CreateMeetingResponse:
        """
        Retrieves details for a meeting with a specified meeting ID.

        :param meeting_id: Unique identifier for the meeting being requested.
        :type meeting_id: str
        :param current: Whether or not to retrieve only the current scheduled meeting of the meeting series, i.e. the
            meeting ready to join or start or the upcoming meeting of the meeting series. If it's true, return details
            for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start or the
            upcoming scheduled meeting of the meeting series. If it's false or not specified, return details for the
            entire meeting series. This parameter only applies to meeting series.
        :type current: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting
        """
        params = {}
        if current is not None:
            params['current'] = current
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}')
        data = super().get(url=url, params=params)
        return CreateMeetingResponse.parse_obj(data)

    def list(self, meeting_number: str = None, web_link: str = None, room_id: str = None, meeting_type: str = None,
             state: str = None, scheduled_type: str = None, current: bool = None, from_: str = None, to_: str = None,
             host_email: str = None, site_url: str = None, integration_tag: str = None,
             **params) -> Generator[MeetingSeriesObjectForListMeeting, None, None]:
        """
        Retrieves details for meetings with a specified meeting number, web link, meeting type, etc. Please note that
        there are various products in the Webex Suite such as Meetings and Events. Currently, only meetings of the
        Meetings product are supported by this API, meetings of others in the suite are not supported. Ad-hoc meetings
        created by Create a Meeting with adhoc of true and a roomId will not be listed, but the ended and ongoing
        ad-hoc meeting instances will be listed.

        :param meeting_number: Meeting number for the meeting objects being requested. meetingNumber, webLink and
            roomId are mutually exclusive. If it's an exceptional meeting from a meeting series, the exceptional
            meeting instead of the primary meeting series is returned.
        :type meeting_number: str
        :param web_link: URL encoded link to information page for the meeting objects being requested. meetingNumber,
            webLink and roomId are mutually exclusive.
        :type web_link: str
        :param room_id: Associated Webex space ID for the meeting objects being requested. meetingNumber, webLink and
            roomId are mutually exclusive.
        :type room_id: str
        :param meeting_type: Meeting type for the meeting objects being requested. This parameter will be ignored if
            meetingNumber, webLink or roomId is specified. Possible values: meetingSeries, scheduledMeeting, meeting
        :type meeting_type: str
        :param state: Meeting state for the meeting objects being requested. If not specified, return meetings of all
            states. This parameter will be ignored if meetingNumber, webLink or roomId is specified. Details of an
            ended meeting will only be available 15 minutes after the meeting has ended. inProgress meetings are not
            fully supported. The API will try to return details of an inProgress meeting 15 minutes after the meeting
            starts. However, it may take longer depending on the traffic. See the Webex Meetings guide for more
            information about the states of meetings. Possible values: active, scheduled, ready, lobby, inProgress,
            ended, missed, expired
        :type state: str
        :param scheduled_type: Scheduled type for the meeting objects being requested. Possible values: meeting,
            webinar, personalRoomMeeting
        :type scheduled_type: str
        :param current: Flag identifying to retrieve the current scheduled meeting of the meeting series or the entire
            meeting series. This parameter only applies to scenarios where meetingNumber is specified and the meeting
            is not an exceptional meeting from a meeting series. If it's true, return the scheduled meeting of the
            meeting series which is ready to join or start or the upcoming scheduled meeting of the meeting series; if
            it's false, return the entire meeting series.
        :type current: bool
        :param from_: Start date and time (inclusive) in any ISO 8601 compliant format for the meeting objects being
            requested. from cannot be after to. This parameter will be ignored if meetingNumber, webLink or roomId is
            specified.
        :type from_: str
        :param to_: End date and time (exclusive) in any ISO 8601 compliant format for the meeting objects being
            requested. to cannot be before from. This parameter will be ignored if meetingNumber, webLink or roomId is
            specified.
        :type to_: String
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for meetings that are hosted by that user.
        :type host_email: str
        :param site_url: URL of the Webex site which the API lists meetings from. If not specified, the API lists
            meetings from user's all sites. All available Webex sites of the user can be retrieved by Get Site List
            API.
        :type site_url: str
        :param integration_tag: External key created by an integration application. This parameter is used by the
            integration application to query meetings by a key in its own domain such as a Zendesk ticket ID, a Jira
            ID, a Salesforce Opportunity ID, etc.
        :type integration_tag: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meetings
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
        if current is not None:
            params['current'] = current
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        if integration_tag is not None:
            params['integrationTag'] = integration_tag
        url = self.ep()
        return self.session.follow_pagination(url=url, model=MeetingSeriesObjectForListMeeting, params=params)

    def list_of_series(self, meeting_series_id: str, from_: str = None, to_: str = None, meeting_type: str = None,
                       state: str = None, is_modified: bool = None, host_email: str = None, **params) -> Generator[
        ScheduledMeetingObject, None, None]:
        """
        Lists scheduled meeting and meeting instances of a meeting series identified by meetingSeriesId. Scheduled
        meetings of an ad-hoc meeting created by Create a Meeting with adhoc of true and a roomId will not be listed,
        but the ended and ongoing meeting instances of it will be listed.
        Each scheduled meeting or meeting instance of a meeting series has its own start, end, etc. Thus, for example,
        when a daily meeting has been scheduled from 2019-04-01 to 2019-04-10, there are 10 scheduled meeting instances
        in this series, one instance for each day, and each one has its own attributes. When a scheduled meeting has
        been started and ended or is happening, there are even more ended or in-progress meeting instances.
        Use this operation to list scheduled meeting and meeting instances of a meeting series within a specific date
        range.
        Long result sets are split into pages.
        trackingCodes is not supported for ended meeting instances.

        :param meeting_series_id: Unique identifier for the meeting series. Please note that currently meeting ID of a
            scheduled personal room meeting is not supported for this API.
        :type meeting_series_id: str
        :param from_: Start date and time (inclusive) for the range for which meetings are to be returned in any ISO
            8601 compliant format. from cannot be after to.
        :type from_: str
        :param to_: End date and time (exclusive) for the range for which meetings are to be returned in any ISO 8601
            compliant format. to cannot be before from.
        :type to_: String
        :param meeting_type: Meeting type for the meeting objects being requested. If not specified, return meetings of
            all types. Possible values: scheduledMeeting, meeting
        :type meeting_type: str
        :param state: Meeting state for the meetings being requested. If not specified, return meetings of all states.
            Details of an ended meeting will only be available 15 minutes after the meeting has ended. inProgress
            meetings are not fully supported. The API will try to return details of an inProgress meeting 15 minutes
            after the meeting starts. However, it may take longer depending on the traffic. See the Webex Meetings
            guide for more information about the states of meetings. Possible values: scheduled, ready, lobby,
            inProgress, ended, missed
        :type state: str
        :param is_modified: Flag identifying whether or not only to retrieve scheduled meeting instances which have
            been modified. This parameter only applies to scheduled meetings. If it's true, only return modified
            scheduled meetings; if it's false, only return unmodified scheduled meetings; if not specified, all
            scheduled meetings will be returned.
        :type is_modified: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return meetings that are hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meetings-of-a-meeting-series
        """
        params['meetingSeriesId'] = meeting_series_id
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        if meeting_type is not None:
            params['meetingType'] = meeting_type
        if state is not None:
            params['state'] = state
        if is_modified is not None:
            params['isModified'] = is_modified
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ScheduledMeetingObject, params=params)

    def patch(self, meeting_id: str, title: str = None, agenda: str = None, password: str = None, start: str = None,
              end: str = None, timezone: str = None, recurrence: str = None, enabled_auto_record_meeting: bool = None,
              allow_any_user_to_be_co_host: bool = None, enabled_join_before_host: bool = None,
              enable_connect_audio_before_host: bool = None, join_before_host_minutes: int = None,
              exclude_password: bool = None, public_meeting: bool = None, reminder_time: int = None,
              unlocked_meeting_join_security: UnlockedMeetingJoinSecurity = None, session_type_id: int = None,
              enabled_webcast_view: bool = None, panelist_password: str = None, enable_automatic_lock: bool = None,
              automatic_lock_minutes: int = None, allow_first_user_to_be_co_host: bool = None,
              allow_authenticated_devices: bool = None, send_email: bool = None, host_email: str = None,
              site_url: str = None, meeting_options: MeetingOptions = None,
              attendee_privileges: AttendeePrivileges = None, integration_tags: List[str] = None,
              enabled_breakout_sessions: bool = None, tracking_codes: TrackingCodeItemForCreateMeetingObject = None,
              audio_connection_options: AudioConnectionOptions = None) -> PatchMeetingResponse:
        """
        Updates details for a meeting with a specified meeting ID. This operation applies to meeting series and
        scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Ad-hoc meetings created by
        Create a Meeting with adhoc of true and a roomId cannot be updated.

        :param meeting_id: Unique identifier for the meeting to be updated. This parameter applies to meeting series
            and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Please note that
            currently meeting ID of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param title: Meeting title. The title can be a maximum of 128 characters long.
        :type title: str
        :param agenda: Meeting agenda. The agenda can be a maximum of 1300 characters long.
        :type agenda: str
        :param password: Meeting password. Must conform to the site's password complexity settings. Read password
            management for details.
        :type password: str
        :param start: Date and time for the start of meeting in any ISO 8601 compliant format. start cannot be before
            current date and time or after end. Duration between start and end cannot be shorter than 10 minutes or
            longer than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating
            date and time for a meeting. Please note that when a meeting is being updated, start of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, if start is within the same minute as the
            current time, start will be adjusted to the upcoming minute; otherwise, start will be adjusted with seconds
            and milliseconds stripped off. For instance, if the current time is 2022-03-01T10:32:16.657+08:00, start of
            2022-03-01T10:32:28.076+08:00 or 2022-03-01T10:32:41+08:00 will be adjusted to 2022-03-01T10:33:00+08:00,
            and start of 2022-03-01T11:32:28.076+08:00 or 2022-03-01T11:32:41+08:00 will be adjusted to
            2022-03-01T11:32:00+08:00.
        :type start: str
        :param end: Date and time for the end of meeting in any ISO 8601 compliant format. end cannot be before current
            date and time or before start. Duration between start and end cannot be shorter than 10 minutes or longer
            than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating date
            and time for a meeting. Please note that when a meeting is being updated, end of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, end will be adjusted with seconds and
            milliseconds stripped off. For instance, end of 2022-03-01T11:52:28.076+08:00 or 2022-03-01T11:52:41+08:00
            will be adjusted to 2022-03-01T11:52:00+08:00.
        :type end: str
        :param timezone: Time zone in which the meeting was originally scheduled (conforming with the IANA time zone
            database).
        :type timezone: str
        :param recurrence: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring
            meeting series, not to a meeting series with only one scheduled meeting. Multiple days or dates for monthly
            or yearly recurrence rule are not supported, only the first day or date specified is taken. For example,
            "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported
            as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
        :type recurrence: str
        :param enabled_auto_record_meeting: Whether or not meeting is recorded automatically.
        :type enabled_auto_record_meeting: bool
        :param allow_any_user_to_be_co_host: Whether or not to allow any attendee with a host account on the target
            site to become a cohost when joining the meeting. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_any_user_to_be_co_host: bool
        :param enabled_join_before_host: Whether or not to allow any attendee to join the meeting before the host joins
            the meeting.
        :type enabled_join_before_host: bool
        :param enable_connect_audio_before_host: Whether or not to allow any attendee to connect audio in the meeting
            before the host joins the meeting. This attribute is only applicable if the enabledJoinBeforeHost attribute
            is set to true.
        :type enable_connect_audio_before_host: bool
        :param join_before_host_minutes: The number of minutes an attendee can join the meeting before the meeting
            start time and the host joins. This attribute is only applicable if the enabledJoinBeforeHost attribute is
            set to true. Valid options are 0, 5, 10 and 15. Default is 0 if not specified.
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
        :type unlocked_meeting_join_security: UnlockedMeetingJoinSecurity
        :param session_type_id: Unique identifier for a meeting session type for the user. This attribute is required
            while scheduling webinar meeting. All available meeting session types enabled for the user can be retrieved
            by List Meeting Session Types API.
        :type session_type_id: int
        :param enabled_webcast_view: Whether or not webcast view is enabled.
        :type enabled_webcast_view: bool
        :param panelist_password: Password for panelists of a webinar meeting. Must conform to the site's password
            complexity settings. Read password management for details. If not specified, a random password conforming
            to the site's password rules will be generated automatically.
        :type panelist_password: str
        :param enable_automatic_lock: Whether or not to automatically lock the meeting after it starts.
        :type enable_automatic_lock: bool
        :param automatic_lock_minutes: The number of minutes after the meeting begins, for automatically locking it.
        :type automatic_lock_minutes: int
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee of the meeting with a host
            account on the target site to become a cohost. The target site is specified by siteUrl parameter when
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
            user in a site they manage to be the meeting host.
        :type host_email: str
        :param site_url: URL of the Webex site which the meeting is updated on. If not specified, the meeting is
            created on user's preferred site. All available Webex sites and preferred site of the user can be retrieved
            by Get Site List API.
        :type site_url: str
        :param meeting_options: Meeting Options.
        :type meeting_options: MeetingOptions
        :param attendee_privileges: Attendee Privileges.
        :type attendee_privileges: AttendeePrivileges
        :param integration_tags: External keys created by an integration application in its own domain, for example
            Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries meetings
            by a key in its own domain. The maximum size of integrationTags is 3 and each item of integrationTags can
            be a maximum of 64 characters long. Please note that an empty or null integrationTags will delete all
            existing integration tags for the meeting implicitly. Developer can update integration tags for a
            meetingSeries but he cannot update it for a scheduledMeeting or a meeting instance.
        :type integration_tags: List[str]
        :param enabled_breakout_sessions: Whether or not breakout sessions are enabled. If the value of
            enabledBreakoutSessions is false, users can not set breakout sessions. If the value of
            enabledBreakoutSessions is true, users can update breakout sessions using the Update Breakout Sessions API.
            Updating breakout sessions are not supported by this API.
        :type enabled_breakout_sessions: bool
        :param tracking_codes: Tracking codes information. All available tracking codes and their options for the
            specified site can be retrieved by List Meeting Tracking Codes API. If an optional tracking code is missing
            from the trackingCodes array and there's a default option for this tracking code, the default option is
            assigned automatically. If the inputMode of a tracking code is select, its value must be one of the
            site-level options or the user-level value. Tracking code is not supported for a personal room meeting or
            an ad-hoc space meeting.
        :type tracking_codes: TrackingCodeItemForCreateMeetingObject
        :param audio_connection_options: Audio connection options.
        :type audio_connection_options: AudioConnectionOptions

        documentation: https://developer.webex.com/docs/api/v1/meetings/patch-a-meeting
        """
        body = PatchMeetingBody()
        if title is not None:
            body.title = title
        if agenda is not None:
            body.agenda = agenda
        if password is not None:
            body.password = password
        if start is not None:
            body.start = start
        if end is not None:
            body.end = end
        if timezone is not None:
            body.timezone = timezone
        if recurrence is not None:
            body.recurrence = recurrence
        if enabled_auto_record_meeting is not None:
            body.enabled_auto_record_meeting = enabled_auto_record_meeting
        if allow_any_user_to_be_co_host is not None:
            body.allow_any_user_to_be_co_host = allow_any_user_to_be_co_host
        if enabled_join_before_host is not None:
            body.enabled_join_before_host = enabled_join_before_host
        if enable_connect_audio_before_host is not None:
            body.enable_connect_audio_before_host = enable_connect_audio_before_host
        if join_before_host_minutes is not None:
            body.join_before_host_minutes = join_before_host_minutes
        if exclude_password is not None:
            body.exclude_password = exclude_password
        if public_meeting is not None:
            body.public_meeting = public_meeting
        if reminder_time is not None:
            body.reminder_time = reminder_time
        if unlocked_meeting_join_security is not None:
            body.unlocked_meeting_join_security = unlocked_meeting_join_security
        if session_type_id is not None:
            body.session_type_id = session_type_id
        if enabled_webcast_view is not None:
            body.enabled_webcast_view = enabled_webcast_view
        if panelist_password is not None:
            body.panelist_password = panelist_password
        if enable_automatic_lock is not None:
            body.enable_automatic_lock = enable_automatic_lock
        if automatic_lock_minutes is not None:
            body.automatic_lock_minutes = automatic_lock_minutes
        if allow_first_user_to_be_co_host is not None:
            body.allow_first_user_to_be_co_host = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body.allow_authenticated_devices = allow_authenticated_devices
        if send_email is not None:
            body.send_email = send_email
        if host_email is not None:
            body.host_email = host_email
        if site_url is not None:
            body.site_url = site_url
        if meeting_options is not None:
            body.meeting_options = meeting_options
        if attendee_privileges is not None:
            body.attendee_privileges = attendee_privileges
        if integration_tags is not None:
            body.integration_tags = integration_tags
        if enabled_breakout_sessions is not None:
            body.enabled_breakout_sessions = enabled_breakout_sessions
        if tracking_codes is not None:
            body.tracking_codes = tracking_codes
        if audio_connection_options is not None:
            body.audio_connection_options = audio_connection_options
        url = self.ep(f'{meeting_id}')
        data = super().patch(url=url, data=body.json())
        return PatchMeetingResponse.parse_obj(data)

    def update(self, meeting_id: str, title: str = None, agenda: str = None, password: str = None, start: str = None,
               end: str = None, timezone: str = None, recurrence: str = None, enabled_auto_record_meeting: bool = None,
               allow_any_user_to_be_co_host: bool = None, enabled_join_before_host: bool = None,
               enable_connect_audio_before_host: bool = None, join_before_host_minutes: int = None,
               exclude_password: bool = None, public_meeting: bool = None, reminder_time: int = None,
               unlocked_meeting_join_security: UnlockedMeetingJoinSecurity = None, session_type_id: int = None,
               enabled_webcast_view: bool = None, panelist_password: str = None, enable_automatic_lock: bool = None,
               automatic_lock_minutes: int = None, allow_first_user_to_be_co_host: bool = None,
               allow_authenticated_devices: bool = None, send_email: bool = None, host_email: str = None,
               site_url: str = None, meeting_options: MeetingOptions = None,
               attendee_privileges: AttendeePrivileges = None, integration_tags: List[str] = None,
               enabled_breakout_sessions: bool = None, tracking_codes: TrackingCodeItemForCreateMeetingObject = None,
               audio_connection_options: AudioConnectionOptions = None) -> PatchMeetingResponse:
        """
        Updates details for a meeting with a specified meeting ID. This operation applies to meeting series and
        scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Ad-hoc meetings created by
        Create a Meeting with adhoc of true and a roomId cannot be updated.

        :param meeting_id: Unique identifier for the meeting to be updated. This parameter applies to meeting series
            and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Please note that
            currently meeting ID of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param title: Meeting title. The title can be a maximum of 128 characters long.
        :type title: str
        :param agenda: Meeting agenda. The agenda can be a maximum of 1300 characters long.
        :type agenda: str
        :param password: Meeting password. Must conform to the site's password complexity settings. Read password
            management for details.
        :type password: str
        :param start: Date and time for the start of meeting in any ISO 8601 compliant format. start cannot be before
            current date and time or after end. Duration between start and end cannot be shorter than 10 minutes or
            longer than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating
            date and time for a meeting. Please note that when a meeting is being updated, start of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, if start is within the same minute as the
            current time, start will be adjusted to the upcoming minute; otherwise, start will be adjusted with seconds
            and milliseconds stripped off. For instance, if the current time is 2022-03-01T10:32:16.657+08:00, start of
            2022-03-01T10:32:28.076+08:00 or 2022-03-01T10:32:41+08:00 will be adjusted to 2022-03-01T10:33:00+08:00,
            and start of 2022-03-01T11:32:28.076+08:00 or 2022-03-01T11:32:41+08:00 will be adjusted to
            2022-03-01T11:32:00+08:00.
        :type start: str
        :param end: Date and time for the end of meeting in any ISO 8601 compliant format. end cannot be before current
            date and time or before start. Duration between start and end cannot be shorter than 10 minutes or longer
            than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating date
            and time for a meeting. Please note that when a meeting is being updated, end of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, end will be adjusted with seconds and
            milliseconds stripped off. For instance, end of 2022-03-01T11:52:28.076+08:00 or 2022-03-01T11:52:41+08:00
            will be adjusted to 2022-03-01T11:52:00+08:00.
        :type end: str
        :param timezone: Time zone in which the meeting was originally scheduled (conforming with the IANA time zone
            database).
        :type timezone: str
        :param recurrence: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring
            meeting series, not to a meeting series with only one scheduled meeting. Multiple days or dates for monthly
            or yearly recurrence rule are not supported, only the first day or date specified is taken. For example,
            "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported
            as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
        :type recurrence: str
        :param enabled_auto_record_meeting: Whether or not meeting is recorded automatically.
        :type enabled_auto_record_meeting: bool
        :param allow_any_user_to_be_co_host: Whether or not to allow any attendee with a host account on the target
            site to become a cohost when joining the meeting. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_any_user_to_be_co_host: bool
        :param enabled_join_before_host: Whether or not to allow any attendee to join the meeting before the host joins
            the meeting.
        :type enabled_join_before_host: bool
        :param enable_connect_audio_before_host: Whether or not to allow any attendee to connect audio in the meeting
            before the host joins the meeting. This attribute is only applicable if the enabledJoinBeforeHost attribute
            is set to true.
        :type enable_connect_audio_before_host: bool
        :param join_before_host_minutes: The number of minutes an attendee can join the meeting before the meeting
            start time and the host joins. This attribute is only applicable if the enabledJoinBeforeHost attribute is
            set to true. Valid options are 0, 5, 10 and 15. Default is 0 if not specified.
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
        :type unlocked_meeting_join_security: UnlockedMeetingJoinSecurity
        :param session_type_id: Unique identifier for a meeting session type for the user. This attribute is required
            while scheduling webinar meeting. All available meeting session types enabled for the user can be retrieved
            by List Meeting Session Types API.
        :type session_type_id: int
        :param enabled_webcast_view: Whether or not webcast view is enabled.
        :type enabled_webcast_view: bool
        :param panelist_password: Password for panelists of a webinar meeting. Must conform to the site's password
            complexity settings. Read password management for details. If not specified, a random password conforming
            to the site's password rules will be generated automatically.
        :type panelist_password: str
        :param enable_automatic_lock: Whether or not to automatically lock the meeting after it starts.
        :type enable_automatic_lock: bool
        :param automatic_lock_minutes: The number of minutes after the meeting begins, for automatically locking it.
        :type automatic_lock_minutes: int
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee of the meeting with a host
            account on the target site to become a cohost. The target site is specified by siteUrl parameter when
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
            user in a site they manage to be the meeting host.
        :type host_email: str
        :param site_url: URL of the Webex site which the meeting is updated on. If not specified, the meeting is
            created on user's preferred site. All available Webex sites and preferred site of the user can be retrieved
            by Get Site List API.
        :type site_url: str
        :param meeting_options: Meeting Options.
        :type meeting_options: MeetingOptions
        :param attendee_privileges: Attendee Privileges.
        :type attendee_privileges: AttendeePrivileges
        :param integration_tags: External keys created by an integration application in its own domain, for example
            Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries meetings
            by a key in its own domain. The maximum size of integrationTags is 3 and each item of integrationTags can
            be a maximum of 64 characters long. Please note that an empty or null integrationTags will delete all
            existing integration tags for the meeting implicitly. Developer can update integration tags for a
            meetingSeries but he cannot update it for a scheduledMeeting or a meeting instance.
        :type integration_tags: List[str]
        :param enabled_breakout_sessions: Whether or not breakout sessions are enabled. If the value of
            enabledBreakoutSessions is false, users can not set breakout sessions. If the value of
            enabledBreakoutSessions is true, users can update breakout sessions using the Update Breakout Sessions API.
            Updating breakout sessions are not supported by this API.
        :type enabled_breakout_sessions: bool
        :param tracking_codes: Tracking codes information. All available tracking codes and their options for the
            specified site can be retrieved by List Meeting Tracking Codes API. If an optional tracking code is missing
            from the trackingCodes array and there's a default option for this tracking code, the default option is
            assigned automatically. If the inputMode of a tracking code is select, its value must be one of the
            site-level options or the user-level value. Tracking code is not supported for a personal room meeting or
            an ad-hoc space meeting.
        :type tracking_codes: TrackingCodeItemForCreateMeetingObject
        :param audio_connection_options: Audio connection options.
        :type audio_connection_options: AudioConnectionOptions

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-a-meeting
        """
        body = PatchMeetingBody()
        if title is not None:
            body.title = title
        if agenda is not None:
            body.agenda = agenda
        if password is not None:
            body.password = password
        if start is not None:
            body.start = start
        if end is not None:
            body.end = end
        if timezone is not None:
            body.timezone = timezone
        if recurrence is not None:
            body.recurrence = recurrence
        if enabled_auto_record_meeting is not None:
            body.enabled_auto_record_meeting = enabled_auto_record_meeting
        if allow_any_user_to_be_co_host is not None:
            body.allow_any_user_to_be_co_host = allow_any_user_to_be_co_host
        if enabled_join_before_host is not None:
            body.enabled_join_before_host = enabled_join_before_host
        if enable_connect_audio_before_host is not None:
            body.enable_connect_audio_before_host = enable_connect_audio_before_host
        if join_before_host_minutes is not None:
            body.join_before_host_minutes = join_before_host_minutes
        if exclude_password is not None:
            body.exclude_password = exclude_password
        if public_meeting is not None:
            body.public_meeting = public_meeting
        if reminder_time is not None:
            body.reminder_time = reminder_time
        if unlocked_meeting_join_security is not None:
            body.unlocked_meeting_join_security = unlocked_meeting_join_security
        if session_type_id is not None:
            body.session_type_id = session_type_id
        if enabled_webcast_view is not None:
            body.enabled_webcast_view = enabled_webcast_view
        if panelist_password is not None:
            body.panelist_password = panelist_password
        if enable_automatic_lock is not None:
            body.enable_automatic_lock = enable_automatic_lock
        if automatic_lock_minutes is not None:
            body.automatic_lock_minutes = automatic_lock_minutes
        if allow_first_user_to_be_co_host is not None:
            body.allow_first_user_to_be_co_host = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body.allow_authenticated_devices = allow_authenticated_devices
        if send_email is not None:
            body.send_email = send_email
        if host_email is not None:
            body.host_email = host_email
        if site_url is not None:
            body.site_url = site_url
        if meeting_options is not None:
            body.meeting_options = meeting_options
        if attendee_privileges is not None:
            body.attendee_privileges = attendee_privileges
        if integration_tags is not None:
            body.integration_tags = integration_tags
        if enabled_breakout_sessions is not None:
            body.enabled_breakout_sessions = enabled_breakout_sessions
        if tracking_codes is not None:
            body.tracking_codes = tracking_codes
        if audio_connection_options is not None:
            body.audio_connection_options = audio_connection_options
        url = self.ep(f'{meeting_id}')
        data = super().put(url=url, data=body.json())
        return PatchMeetingResponse.parse_obj(data)

    def delete(self, meeting_id: str, host_email: str = None, send_email: bool = None):
        """
        Deletes a meeting with a specified meeting ID. The deleted meeting cannot be recovered. This operation applies
        to meeting series and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Ad-hoc
        meetings created by Create a Meeting with adhoc of true and a roomId cannot be deleted.

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

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-a-meeting
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if send_email is not None:
            params['sendEmail'] = send_email
        url = self.ep(f'{meeting_id}')
        super().delete(url=url, params=params)
        return

    def join(self, meeting_id: str = None, meeting_number: str = None, web_link: str = None, join_directly: bool = None,
             email: str = None, display_name: str = None, password: str = None,
             expiration_minutes: int = None) -> JoinMeetingResponse:
        """
        Retrieves a meeting join link for a meeting with a specified meetingId, meetingNumber, or webLink that allows
        users to join the meeting directly without logging in and entering a password.

        :param meeting_id: Unique identifier for the meeting. This parameter applies to meeting series and scheduled
            meetings. It doesn't apply to ended or in-progress meeting instances. Please note that currently meeting ID
            of a scheduled personal room meeting is also supported for this API.
        :type meeting_id: str
        :param meeting_number: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but
            not to meeting instances which have ended.
        :type meeting_number: str
        :param web_link: Link to a meeting information page where the meeting client is launched if the meeting is
            ready to start or join.
        :type web_link: str
        :param join_directly: Whether or not to redirect to joinLink. It is an optional field and default value is
            true.
        :type join_directly: bool
        :param email: Email address of meeting participant. If the user is a guest issuer, email is required.
        :type email: str
        :param display_name: Display name of meeting participant. The maximum length of displayName is 128 characters.
            If the user is a guest issuer, displayName is required.
        :type display_name: str
        :param password: It's required when the meeting is protected by a password and the current user is not
            privileged to view it if they are not a host, cohost or invitee of the meeting.
        :type password: str
        :param expiration_minutes: Expiration duration of joinLink in minutes. Must be between 1 and 60.
        :type expiration_minutes: int

        documentation: https://developer.webex.com/docs/api/v1/meetings/join-a-meeting
        """
        body = JoinMeetingBody()
        if meeting_id is not None:
            body.meeting_id = meeting_id
        if meeting_number is not None:
            body.meeting_number = meeting_number
        if web_link is not None:
            body.web_link = web_link
        if join_directly is not None:
            body.join_directly = join_directly
        if email is not None:
            body.email = email
        if display_name is not None:
            body.display_name = display_name
        if password is not None:
            body.password = password
        if expiration_minutes is not None:
            body.expiration_minutes = expiration_minutes
        url = self.ep('join')
        data = super().post(url=url, data=body.json())
        return JoinMeetingResponse.parse_obj(data)

    def list_templates(self, template_type: str = None, locale: str = None, is_default: bool = None,
                       is_standard: bool = None, host_email: str = None, site_url: str = None) -> list[TemplateObject]:
        """
        Retrieves the list of meeting templates that is available for the authenticated user.
        There are separate lists of meeting templates for different templateType, locale and siteUrl.

        :param template_type: Meeting template type for the meeting template objects being requested. If not specified,
            return meeting templates of all types. Possible values: meeting, webinar
        :type template_type: str
        :param locale: Locale for the meeting template objects being requested. If not specified, return meeting
            templates of the default en_US locale. Refer to Meeting Template Locales for all the locales supported by
            Webex.
        :type locale: str
        :param is_default: The value is true or false. If it's true, return the default meeting templates; if it's
            false, return the non-default meeting templates. If it's not specified, return both default and non-default
            meeting templates.
        :type is_default: bool
        :param is_standard: The value is true or false. If it's true, return the standard meeting templates; if it's
            false, return the non-standard meeting templates. If it's not specified, return both standard and
            non-standard meeting templates.
        :type is_standard: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return meeting templates that are available for that user.
        :type host_email: str
        :param site_url: URL of the Webex site which the API lists meeting templates from. If not specified, the API
            lists meeting templates from user's preferred site. All available Webex sites and preferred site of the
            user can be retrieved by Get Site List API.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-templates
        """
        params = {}
        if template_type is not None:
            params['templateType'] = template_type
        if locale is not None:
            params['locale'] = locale
        if is_default is not None:
            params['isDefault'] = is_default
        if is_standard is not None:
            params['isStandard'] = is_standard
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('templates')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[TemplateObject], data["items"])

    def template(self, template_id: str, host_email: str = None) -> GetMeetingTemplateResponse:
        """
        Retrieves details for a meeting template with a specified meeting template ID.

        :param template_id: Unique identifier for the meeting template being requested.
        :type template_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return the meeting template that is available for that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-template
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'templates/{template_id}')
        data = super().get(url=url, params=params)
        return GetMeetingTemplateResponse.parse_obj(data)

    def control_status(self, meeting_id: str) -> GetMeetingControlStatusResponse:
        """
        Get the meeting control of a live meeting, which is consisted of meeting control status on "locked" and
        "recording" to reflect whether the meeting is currently locked and there is recording in progress.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-meeting-control-status
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep('controls')
        data = super().get(url=url, params=params)
        return GetMeetingControlStatusResponse.parse_obj(data)

    def update_control_status(self, meeting_id: str, locked: bool = None, recording_started: bool = None,
                              recording_paused: bool = None) -> GetMeetingControlStatusResponse:
        """
        To start, pause, resume, or stop a meeting recording; To lock or unlock an on-going meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param locked: Whether the meeting is locked or not.
        :type locked: bool
        :param recording_started: The value can be true or false, it indicates the meeting recording started or not.
        :type recording_started: bool
        :param recording_paused: The value can be true or false, it indicates the meeting recording paused or not.
        :type recording_paused: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-meeting-control-status
        """
        params = {}
        params['meetingId'] = meeting_id
        body = GetMeetingControlStatusResponse()
        if locked is not None:
            body.locked = locked
        if recording_started is not None:
            body.recording_started = recording_started
        if recording_paused is not None:
            body.recording_paused = recording_paused
        url = self.ep('controls')
        data = super().put(url=url, params=params, data=body.json())
        return GetMeetingControlStatusResponse.parse_obj(data)

    def list_session_types(self, host_email: str = None, site_url: str = None) -> list[MeetingSessionTypeObject]:
        """
        List all the meeting session types enabled for a given user.

        :param host_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will list all the meeting session types enabled for the user.
        :type host_email: str
        :param site_url: Webex site URL to query. If siteUrl is not specified, the users' preferred site will be used.
            If the authorization token has the admin-level scopes, the admin can set the Webex site URL on behalf of
            the user specified in the hostEmail parameter.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-session-types
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('sessionTypes')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[MeetingSessionTypeObject], data["items"])

    def session_type(self, session_type_id: int, host_email: str = None,
                     site_url: str = None) -> MeetingSessionTypeObject:
        """
        Retrieves details for a meeting session type with a specified session type ID.

        :param session_type_id: A unique identifier for the sessionType.
        :type session_type_id: int
        :param host_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will get a meeting session type with the specified session type ID enabled for the user.
        :type host_email: str
        :param site_url: Webex site URL to query. If siteUrl is not specified, the users' preferred site will be used.
            If the authorization token has the admin-level scopes, the admin can set the Webex site URL on behalf of
            the user specified in the hostEmail parameter.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-session-type
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep(f'sessionTypes/{session_type_id}')
        data = super().get(url=url, params=params)
        return MeetingSessionTypeObject.parse_obj(data)

    def registration_form_formeeting(self, meeting_id: str) -> GetRegistrationFormFormeetingResponse:
        """
        Get a meeting's registration form to understand which fields are required.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-registration-form-for-a-meeting
        """
        url = self.ep(f'{meeting_id}/registration')
        data = super().get(url=url)
        return GetRegistrationFormFormeetingResponse.parse_obj(data)

    def update_registration_form(self, meeting_id: str, host_email: str = None, require_first_name: bool = None,
                                 require_last_name: bool = None, require_email: bool = None,
                                 require_job_title: bool = None, require_company_name: bool = None,
                                 require_address1: bool = None, require_address2: bool = None,
                                 require_city: bool = None, require_state: bool = None, require_zip_code: bool = None,
                                 require_country_region: bool = None, require_work_phone: bool = None,
                                 require_fax: bool = None, max_register_num: int = None,
                                 customized_questions: CustomizedQuestionForCreateMeeting = None,
                                 rules: StandardRegistrationApproveRule = None) -> \
            GetRegistrationFormFormeetingResponse:
        """
        Enable or update a registration form for a meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting or an occurrence meeting.
        :type meeting_id: str
        :param host_email: 
        :type host_email: str
        :param require_first_name: Whether or not a registrant's first name is required for meeting registration. This
            option must always be true.
        :type require_first_name: bool
        :param require_last_name: Whether or not a registrant's last name is required for meeting registration. This
            option must always be true.
        :type require_last_name: bool
        :param require_email: Whether or not a registrant's email is required for meeting registration. This option
            must always be true.
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
        :param max_register_num: The maximum number of meeting registrations. Only applies to meetings. Webinars use a
            default value of 10000. If the maximum capacity of attendees for a webinar is less than 10000, e.g. 3000,
            then at most 3000 registrants can join this webinar.
        :type max_register_num: int
        :param customized_questions: Customized questions for meeting registration.
        :type customized_questions: CustomizedQuestionForCreateMeeting
        :param rules: The approval rule for standard questions.
        :type rules: StandardRegistrationApproveRule

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-meeting-registration-form
        """
        body = UpdateMeetingRegistrationFormBody()
        if host_email is not None:
            body.host_email = host_email
        if require_first_name is not None:
            body.require_first_name = require_first_name
        if require_last_name is not None:
            body.require_last_name = require_last_name
        if require_email is not None:
            body.require_email = require_email
        if require_job_title is not None:
            body.require_job_title = require_job_title
        if require_company_name is not None:
            body.require_company_name = require_company_name
        if require_address1 is not None:
            body.require_address1 = require_address1
        if require_address2 is not None:
            body.require_address2 = require_address2
        if require_city is not None:
            body.require_city = require_city
        if require_state is not None:
            body.require_state = require_state
        if require_zip_code is not None:
            body.require_zip_code = require_zip_code
        if require_country_region is not None:
            body.require_country_region = require_country_region
        if require_work_phone is not None:
            body.require_work_phone = require_work_phone
        if require_fax is not None:
            body.require_fax = require_fax
        if max_register_num is not None:
            body.max_register_num = max_register_num
        if customized_questions is not None:
            body.customized_questions = customized_questions
        if rules is not None:
            body.rules = rules
        url = self.ep(f'{meeting_id}/registration')
        data = super().put(url=url, data=body.json())
        return GetRegistrationFormFormeetingResponse.parse_obj(data)

    def delete_registration_form(self, meeting_id: str):
        """
        Disable the registration form for a meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting or an occurrence meeting.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-meeting-registration-form
        """
        url = self.ep(f'{meeting_id}/registration')
        super().delete(url=url)
        return

    def register_registrant(self, meeting_id: str, first_name: str, last_name: str = None, email: str = None,
                            job_title: str = None, company_name: str = None, address1: str = None, address2: str = None,
                            city: str = None, state: str = None, zip_code: str = None, country_region: str = None,
                            work_phone: str = None, fax: str = None, send_email: bool = None,
                            customized_questions: CustomizedRegistrant = None) -> RegisterMeetingRegistrantResponse:
        """
        Register a new registrant for a meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param first_name: The registrant's first name.
        :type first_name: str
        :param last_name: If the value is lastName, this approval rule applies to the standard question of "Last Name".
        :type last_name: str
        :param email: If the value is email, this approval rule applies to the standard question of "Email".
        :type email: str
        :param job_title: If the value is jobTitle, this approval rule applies to the standard question of "Job Title".
        :type job_title: str
        :param company_name: If the value is companyName, this approval rule applies to the standard question of
            "Company Name".
        :type company_name: str
        :param address1: If the value is address1, this approval rule applies to the standard question of "Address 1".
        :type address1: str
        :param address2: If the value is address2, this approval rule applies to the standard question of "Address 2".
        :type address2: str
        :param city: If the value is city, this approval rule applies to the standard question of "City".
        :type city: str
        :param state: If the value is state, this approval rule applies to the standard question of "State".
        :type state: str
        :param zip_code: If the value is zipCode, this approval rule applies to the standard question of "Zip/Post
            Code".
        :type zip_code: str
        :param country_region: If the value is countryRegion, this approval rule applies to the standard question of
            "Country Region".
        :type country_region: str
        :param work_phone: If the value is workPhone, this approval rule applies to the standard question of "Work
            Phone".
        :type work_phone: str
        :param fax: If the value is fax, this approval rule applies to the standard question of "Fax".
        :type fax: str
        :param send_email: If true send email to the registrant. Default: true.
        :type send_email: bool
        :param customized_questions: The registrant's answers for customized questions. Registration options define
            whether or not this is required.
        :type customized_questions: CustomizedRegistrant

        documentation: https://developer.webex.com/docs/api/v1/meetings/register-a-meeting-registrant
        """
        body = RegisterMeetingRegistrantBody()
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if email is not None:
            body.email = email
        if job_title is not None:
            body.job_title = job_title
        if company_name is not None:
            body.company_name = company_name
        if address1 is not None:
            body.address1 = address1
        if address2 is not None:
            body.address2 = address2
        if city is not None:
            body.city = city
        if state is not None:
            body.state = state
        if zip_code is not None:
            body.zip_code = zip_code
        if country_region is not None:
            body.country_region = country_region
        if work_phone is not None:
            body.work_phone = work_phone
        if fax is not None:
            body.fax = fax
        if send_email is not None:
            body.send_email = send_email
        if customized_questions is not None:
            body.customized_questions = customized_questions
        url = self.ep(f'{meeting_id}/registrants')
        data = super().post(url=url, data=body.json())
        return RegisterMeetingRegistrantResponse.parse_obj(data)

    def batch_register_registrants(self, meeting_id: str, items: RegisterMeetingRegistrantBody = None) -> list[
        RegisterMeetingRegistrantResponse]:
        """
        Bulk register new registrants for a meeting.

        :param meeting_id: Unique identifier for the meeting.
        :type meeting_id: str
        :param items: Registrants array.
        :type items: RegisterMeetingRegistrantBody

        documentation: https://developer.webex.com/docs/api/v1/meetings/batch-register-meeting-registrants
        """
        body = BatchRegisterMeetingRegistrantsBody()
        if items is not None:
            body.items = items
        url = self.ep(f'{meeting_id}/registrants/bulkInsert')
        data = super().post(url=url, data=body.json())
        return parse_obj_as(list[RegisterMeetingRegistrantResponse], data["items"])

    def getmeeting_registrants_detail_information(self, meeting_id: str,
                                                  registrant_id: str) -> GetmeetingRegistrantsDetailInformationResponse:
        """
        Retrieves details for a meeting registrant with a specified registrant Id.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param registrant_id: Unique identifier for the registrant
        :type registrant_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-registrant's-detail-information
        """
        url = self.ep(f'{meeting_id}/registrants/{registrant_id}')
        data = super().get(url=url)
        return GetmeetingRegistrantsDetailInformationResponse.parse_obj(data)

    def list_registrants(self, meeting_id: str, email: str = None, register_time_from: str = None,
                         register_time_to: str = None, **params) -> Generator[
        GetmeetingRegistrantsDetailInformationResponse, None, None]:
        """
        Meeting's host and cohost can retrieve the list of registrants for a meeting with a specified meeting Id.

        :param meeting_id: Unique identifier for the meeting.
        :type meeting_id: str
        :param email: Registrant's email to filter registrants.
        :type email: str
        :param register_time_from: The time registrants register a meeting starts from the specified date and time
            (inclusive) in any ISO 8601 compliant format. If registerTimeFrom is not specified, it equals
            registerTimeTo minus 7 days.
        :type register_time_from: str
        :param register_time_to: The time registrants register a meeting before the specified date and time (exclusive)
            in any ISO 8601 compliant format. If registerTimeTo is not specified, it equals registerTimeFrom plus 7
            days. The interval between registerTimeFrom and registerTimeTo must be within 90 days.
        :type register_time_to: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-registrants
        """
        if email is not None:
            params['email'] = email
        if register_time_from is not None:
            params['registerTimeFrom'] = register_time_from
        if register_time_to is not None:
            params['registerTimeTo'] = register_time_to
        url = self.ep(f'{meeting_id}/registrants')
        return self.session.follow_pagination(url=url, model=GetmeetingRegistrantsDetailInformationResponse,
                                              params=params)

    def query_registrants(self, meeting_id: str, emails: List[str], status: Status = None, order_type: OrderType = None,
                          order_by: OrderBy = None, **params) -> Generator[
        GetmeetingRegistrantsDetailInformationResponse, None, None]:
        """
        Meeting's host and cohost can query the list of registrants for a meeting with a specified meeting ID and
        registrants email.

        :param meeting_id: Unique identifier for the meeting.
        :type meeting_id: str
        :param emails: List of registrant email addresses. Possible values: bob@example.com
        :type emails: List[str]
        :param status: Registrant's status.
        :type status: Status
        :param order_type: Sort order for the registrants.
        :type order_type: OrderType
        :param order_by: Registrant ordering field. Ordered by registrationTime by default.
        :type order_by: OrderBy

        documentation: https://developer.webex.com/docs/api/v1/meetings/query-meeting-registrants
        """
        body = QueryMeetingRegistrantsBody()
        if emails is not None:
            body.emails = emails
        if status is not None:
            body.status = status
        if order_type is not None:
            body.order_type = order_type
        if order_by is not None:
            body.order_by = order_by
        url = self.ep(f'{meeting_id}/registrants/query')
        return self.session.follow_pagination(url=url, model=GetmeetingRegistrantsDetailInformationResponse,
                                              params=params, data=body.json())

    def batch_update_registrants_status(self, meeting_id: str, status_op_type: str, send_email: bool = None,
                                        registrants: List[str] = None):
        """
        Meeting's host or cohost can update the set of registrants for a meeting. cancel means the registrant(s) will
        be moved back to the registration list. bulkDelete means the registrant(s) will be deleted.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param status_op_type: Update registrant's status. Possible values: approve, reject, cancel, bulkDelete
        :type status_op_type: str
        :param send_email: If true send email to registrants. Default: true.
        :type send_email: bool
        :param registrants: Registrants array. Registrant ID.
        :type registrants: List[str]

        documentation: https://developer.webex.com/docs/api/v1/meetings/batch-update-meeting-registrants-status
        """
        body = BatchUpdateMeetingRegistrantsStatusBody()
        if send_email is not None:
            body.send_email = send_email
        if registrants is not None:
            body.registrants = registrants
        url = self.ep(f'{meeting_id}/registrants/{status_op_type}')
        super().post(url=url, data=body.json())
        return

    def delete_registrant(self, meeting_id: str, registrant_id: str):
        """
        Meeting's host or cohost can delete a registrant with a specified registrant ID.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param registrant_id: Unique identifier for the registrant.
        :type registrant_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-a-meeting-registrant
        """
        url = self.ep(f'{meeting_id}/registrants/{registrant_id}')
        super().delete(url=url)
        return

    def update_simultaneous_interpretation(self, meeting_id: str, enabled: bool,
                                           interpreters:
                                           InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting =
                                           None) -> SimultaneousInterpretation1:
        """
        Updates simultaneous interpretation options of a meeting with a specified meeting ID. This operation applies to
        meeting series and scheduled meetings. It doesn't apply to ended or in-progress meeting instances.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param enabled: Whether or not simultaneous interpretation is enabled.
        :type enabled: bool
        :param interpreters: Interpreters for meeting.
        :type interpreters: InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-meeting-simultaneous-interpretation
        """
        body = SimultaneousInterpretation()
        if enabled is not None:
            body.enabled = enabled
        if interpreters is not None:
            body.interpreters = interpreters
        url = self.ep(f'{meeting_id}/simultaneousInterpretation')
        data = super().put(url=url, data=body.json())
        return SimultaneousInterpretation1.parse_obj(data)

    def create_interpreter(self, meeting_id: str, language_code1: str, language_code2: str, email: str = None,
                           display_name: str = None, host_email: str = None,
                           send_email: bool = None) -> InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting:
        """
        Assign an interpreter to a bi-directional simultaneous interpretation language channel for a meeting.

        :param meeting_id: Unique identifier for the meeting to which the interpreter is to be assigned.
        :type meeting_id: str
        :param language_code1: Forms a set of simultaneous interpretation channels together with languageCode2.
            Standard language format from ISO 639-1 code. Read ISO 639-1 for details.
        :type language_code1: str
        :param language_code2: Forms a set of simultaneous interpretation channels together with languageCode1.
            Standard language format from ISO 639-1 code. Read ISO 639-1 for details.
        :type language_code2: str
        :param email: Email address of meeting interpreter.
        :type email: str
        :param display_name: Display name of meeting interpreter.
        :type display_name: str
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param send_email: If true, send email to the interpreter.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/create-a-meeting-interpreter
        """
        body = CreateMeetingInterpreterBody()
        if language_code1 is not None:
            body.language_code1 = language_code1
        if language_code2 is not None:
            body.language_code2 = language_code2
        if email is not None:
            body.email = email
        if display_name is not None:
            body.display_name = display_name
        if host_email is not None:
            body.host_email = host_email
        if send_email is not None:
            body.send_email = send_email
        url = self.ep(f'{meeting_id}/interpreters')
        data = super().post(url=url, data=body.json())
        return InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting.parse_obj(data)

    def interpreter(self, meeting_id: str, interpreter_id: str,
                    host_email: str = None) -> InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting:
        """
        Retrieves details for a meeting interpreter identified by meetingId and interpreterId in the URI.

        :param meeting_id: Unique identifier for the meeting to which the interpreter has been assigned.
        :type meeting_id: str
        :param interpreter_id: Unique identifier for the interpreter whose details are being requested.
        :type interpreter_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return details for an interpreter of the meeting that is hosted by that
            user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-interpreter
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}/interpreters/{interpreter_id}')
        data = super().get(url=url, params=params)
        return InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting.parse_obj(data)

    def list_interpreters(self, meeting_id: str, host_email: str = None) -> list[
        InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting]:
        """
        Lists meeting interpreters for a meeting with a specified meetingId.
        This operation can be used for meeting series, scheduled meeting and ended or ongoing meeting instance objects.
        If the specified meetingId is for a meeting series, the interpreters for the series will be listed; if the
        meetingId is for a scheduled meeting, the interpreters for the particular scheduled meeting will be listed; if
        the meetingId is for an ended or ongoing meeting instance, the interpreters for the particular meeting instance
        will be listed. See the Webex Meetings guide for more information about the types of meetings.
        The list returned is sorted in descending order by when interpreters were created.

        :param meeting_id: Unique identifier for the meeting for which interpreters are being requested. The meeting
            can be meeting series, scheduled meeting or meeting instance which has ended or is ongoing. Please note
            that currently meeting ID of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return interpreters of the meeting that is hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-interpreters
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}/interpreters')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting], data["items"])

    def update_interpreter(self, meeting_id: str, interpreter_id: str, language_code1: str, language_code2: str,
                           email: str = None, display_name: str = None, host_email: str = None,
                           send_email: bool = None) -> InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting:
        """
        Updates details for a meeting interpreter identified by meetingId and interpreterId in the URI.

        :param meeting_id: Unique identifier for the meeting whose interpreters were belong to.
        :type meeting_id: str
        :param interpreter_id: Unique identifier for the interpreter whose details are being requested.
        :type interpreter_id: str
        :param language_code1: Forms a set of simultaneous interpretation channels together with languageCode2.
            Standard language format from ISO 639-1 code. Read ISO 639-1 for details.
        :type language_code1: str
        :param language_code2: Forms a set of simultaneous interpretation channels together with languageCode1.
            Standard language format from ISO 639-1 code. Read ISO 639-1 for details.
        :type language_code2: str
        :param email: Email address of meeting interpreter.
        :type email: str
        :param display_name: Display name of meeting interpreter.
        :type display_name: str
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email
            of a user in a site they manage to be the meeting host.
        :type host_email: str
        :param send_email: If true, send email to the interpreter.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-a-meeting-interpreter
        """
        body = CreateMeetingInterpreterBody()
        if language_code1 is not None:
            body.language_code1 = language_code1
        if language_code2 is not None:
            body.language_code2 = language_code2
        if email is not None:
            body.email = email
        if display_name is not None:
            body.display_name = display_name
        if host_email is not None:
            body.host_email = host_email
        if send_email is not None:
            body.send_email = send_email
        url = self.ep(f'{meeting_id}/interpreters/{interpreter_id}')
        data = super().put(url=url, data=body.json())
        return InterpreterObjectForSimultaneousInterpretationOfGetOrListMeeting.parse_obj(data)

    def delete_interpreter(self, meeting_id: str, interpreter_id: str, host_email: str = None, send_email: bool = None):
        """
        Removes a meeting interpreter identified by meetingId and interpreterId in the URI. The deleted meeting
        interpreter cannot be recovered.

        :param meeting_id: Unique identifier for the meeting whose interpreters were belong to.
        :type meeting_id: str
        :param interpreter_id: Unique identifier for the interpreter to be removed.
        :type interpreter_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will delete an interpreter of the meeting that is hosted by that user.
        :type host_email: str
        :param send_email: If true, send email to the interpreter.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-a-meeting-interpreter
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if send_email is not None:
            params['sendEmail'] = send_email
        url = self.ep(f'{meeting_id}/interpreters/{interpreter_id}')
        super().delete(url=url, params=params)
        return

    def update_breakout_sessions(self, meeting_id: str, host_email: str = None, send_email: bool = None,
                                 items: BreakoutSessionObject = None) -> list[GetBreakoutSessionObject]:
        """
        Updates breakout sessions of a meeting with a specified meeting ID. This operation applies to meeting series
        and scheduled meetings.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :param items: Breakout sessions are smaller groups that are split off from the main meeting or webinar. They
            allow a subset of participants to collaborate and share ideas over audio and video. Use breakout sessions
            for workshops, classrooms, or for when you need a moment to talk privately with a few participants outside
            of the main session. Please note that maximum number of breakout sessions in a meeting or webinar is 100.
            In webinars, if hosts preassign attendees to breakout sessions, the role of attendee will be changed to
            panelist. Breakout session is not supported for a meeting with simultaneous interpretation.
        :type items: BreakoutSessionObject

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-meeting-breakout-sessions
        """
        body = UpdateMeetingBreakoutSessionsBody()
        if host_email is not None:
            body.host_email = host_email
        if send_email is not None:
            body.send_email = send_email
        if items is not None:
            body.items = items
        url = self.ep(f'{meeting_id}/breakoutSessions')
        data = super().put(url=url, data=body.json())
        return parse_obj_as(list[GetBreakoutSessionObject], data["items"])

    def list_breakout_sessions(self, meeting_id: str) -> list[GetBreakoutSessionObject]:
        """
        Lists meeting breakout sessions for a meeting with a specified meetingId.
        This operation can be used for meeting series, scheduled meeting and ended or ongoing meeting instance objects.
        See the Webex Meetings guide for more information about the types of meetings.

        :param meeting_id: Unique identifier for the meeting. This parameter applies to meeting series, scheduled
            meeting and ended or ongoing meeting instance objects. Please note that currently meeting ID of a scheduled
            personal room meeting is not supported for this API.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-breakout-sessions
        """
        url = self.ep(f'{meeting_id}/breakoutSessions')
        data = super().get(url=url)
        return parse_obj_as(list[GetBreakoutSessionObject], data["items"])

    def delete_breakout_sessions(self, meeting_id: str, send_email: bool = None):
        """
        Deletes breakout sessions with a specified meeting ID. The deleted breakout sessions cannot be recovered. The
        value of enabledBreakoutSessions attribute is set to false automatically.
        This operation applies to meeting series and scheduled meetings. It doesn't apply to ended or in-progress
        meeting instances.

        :param meeting_id: Unique identifier for the meeting. This parameter applies to meeting series and scheduled
            meetings. It doesn't apply to ended or in-progress meeting instances.
        :type meeting_id: str
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-meeting-breakout-sessions
        """
        params = {}
        if send_email is not None:
            params['sendEmail'] = send_email
        url = self.ep(f'{meeting_id}/breakoutSessions')
        super().delete(url=url, params=params)
        return

    def survey(self, meeting_id: str) -> GetMeetingSurveyResponse:
        """
        Retrieves details for a meeting survey identified by meetingId.

        :param meeting_id: Unique identifier for the meeting. Please note that only the meeting ID of a scheduled
            webinar is supported for this API.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-survey
        """
        url = self.ep(f'{meeting_id}/survey')
        data = super().get(url=url)
        return GetMeetingSurveyResponse.parse_obj(data)

    def list_survey_results(self, meeting_id: str, meeting_start_time_from: str = None,
                            meeting_start_time_to: str = None,
                            **params) -> Generator[SurveyResultObject, None, None]:
        """
        Retrieves results for a meeting survey identified by meetingId.

        :param meeting_id: Unique identifier for the meeting. Please note that only the meeting ID of a scheduled
            webinar is supported for this API.
        :type meeting_id: str
        :param meeting_start_time_from: Start date and time (inclusive) in any ISO 8601 compliant format for the
            meeting objects being requested. meetingStartTimeFrom cannot be after meetingStartTimeTo. This parameter
            will be ignored if meetingId is the unique identifier for the specific meeting instance. When meetingId is
            not the unique identifier for the specific meeting instance, the meetingStartTimeFrom, if not specified,
            equals meetingStartTimeTo minus 1 month; if meetingStartTimeTo is also not specified, the default value for
            meetingStartTimeFrom is 1 month before the current date and time.
        :type meeting_start_time_from: str
        :param meeting_start_time_to: End date and time (exclusive) in any ISO 8601 compliant format for the meeting
            objects being requested. meetingStartTimeTo cannot be prior to meetingStartTimeFrom. This parameter will be
            ignored if meetingId is the unique identifier for the specific meeting instance. When meetingId is not the
            unique identifier for the specific meeting instance, if meetingStartTimeFrom is also not specified, the
            default value for meetingStartTimeTo is the current date and time;For example,if meetingStartTimeFrom is a
            month ago, the default value for meetingStartTimeTo is 1 month after meetingStartTimeFrom.Otherwise it is
            the current date and time.
        :type meeting_start_time_to: String

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-survey-results
        """
        if meeting_start_time_from is not None:
            params['meetingStartTimeFrom'] = meeting_start_time_from
        if meeting_start_time_to is not None:
            params['meetingStartTimeTo'] = meeting_start_time_to
        url = self.ep(f'{meeting_id}/surveyResults')
        return self.session.follow_pagination(url=url, model=SurveyResultObject, params=params)

    def create_invitation_sources(self, meeting_id: str, host_email: str = None, person_id: str = None,
                                  items: InvitationSourceCreateObject = None) -> list[InvitationSourceObject]:
        """
        Creates one or more invitation sources for a meeting.

        :param meeting_id: Unique identifier for the meeting. Only the meeting ID of a scheduled webinar is supported
            for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if a user or application
            calling the API has the admin-level scopes. The admin may specify the email of a user on a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :param person_id: Unique identifier for the meeting host. Should only be set if the user or application calling
            the API has the admin-level scopes. When used, the admin may specify the email of a user in a site they
            manage to be the meeting host.
        :type person_id: str
        :param items: 
        :type items: InvitationSourceCreateObject

        documentation: https://developer.webex.com/docs/api/v1/meetings/create-invitation-sources
        """
        body = CreateInvitationSourcesBody()
        if host_email is not None:
            body.host_email = host_email
        if person_id is not None:
            body.person_id = person_id
        if items is not None:
            body.items = items
        url = self.ep(f'{meeting_id}/invitationSources')
        data = super().post(url=url, data=body.json())
        return parse_obj_as(list[InvitationSourceObject], data["items"])

    def list_invitation_sources(self, meeting_id: str) -> list[InvitationSourceObject]:
        """
        Lists invitation sources for a meeting.

        :param meeting_id: Unique identifier for the meeting. Only the meeting ID of a scheduled webinar is supported
            for this API.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-invitation-sources
        """
        url = self.ep(f'{meeting_id}/invitationSources')
        data = super().get(url=url)
        return parse_obj_as(list[InvitationSourceObject], data["items"])

    def list_tracking_codes(self, service: str, site_url: str = None,
                            host_email: str = None) -> ListMeetingTrackingCodesResponse:
        """
        Lists tracking codes on a site by a meeting host. The result indicates which tracking codes and what options
        can be used to create or update a meeting on the specified site.

        :param service: Service for schedule or sign-up pages.
        :type service: str
        :param site_url: URL of the Webex site which the API retrieves the tracking code from. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and preferred
            sites of a user can be retrieved by Get Site List API.
        :type site_url: str
        :param host_email: Email address for the meeting host. This parameter is only used if a user or application
            calling the API has the admin-level scopes. The admin may specify the email of a user on a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-tracking-codes
        """
        params = {}
        params['service'] = service
        if site_url is not None:
            params['siteUrl'] = site_url
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep('trackingCodes')
        data = super().get(url=url, params=params)
        return ListMeetingTrackingCodesResponse.parse_obj(data)

"""
Webex Meetings APIs
"""
from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional, List

from .chats import MeetingChatsApi
from .closed_captions import MeetingClosedCaptionsApi
from .invitees import MeetingInviteesApi
from .participants import MeetingParticipantsApi
from .preferences import MeetingPreferencesApi
from .qanda import MeetingQandAApi
from .qualities import MeetingQualitiesApi
from .transcripts import MeetingTranscriptsApi
from ..api_child import ApiChild
from ..base import ApiModel
from ..base import SafeEnum as Enum
from ..common import LinkRelation
from ..rest import RestSession

__all__ = ['AttendeePrivileges', 'AudioConnectionOptions', 'AudioConnectionType', 'BreakoutSession',
           'CallInNumbers', 'AnswerCondition', 'CustomizedQuestionForCreateMeeting',
           'EntryAndExitTone', 'GetMeetingSurveyResponse', 'InputMode',
           'InterpreterForSimultaneousInterpretation',
           'InviteeForCreateMeeting',
           'JoinMeetingResponse', 'TrackingCode',
           'MeetingOptions',
           'Meeting', 'MeetingType', 'NoteType', 'QuestionOption', 'TrackingCodeOption',
           'PatchMeetingBody', 'PatchMeetingResponse', 'ApprovalQuestion', 'QuestionAnswer', 'Question',
           'QuestionWithAnswers', 'Registration', 'AutoRegistrationResult', 'ApprovalRule',
           'ScheduledMeeting',
           'ScheduledType', 'MeetingService', 'SimultaneousInterpretation',
           'StandardRegistrationApproveRule', 'MeetingState', 'SurveyResult', 'MeetingTelephony',
           'TrackingCodeItem', 'Type', 'QuestionType', 'TrackingCodeType', 'UnlockedMeetingJoinSecurity',
           'MeetingsApi', 'CreateMeetingBody', 'JoinMeetingBody']


class ScheduledType(str, Enum):
    #: Set the value of scheduledType attribute to meeting for creating a regular meeting.
    meeting = 'meeting'
    #: Set the value of scheduledType attribute to webinar for creating a webinar meeting.
    webinar = 'webinar'
    #: Set the value of scheduledType attribute to personalRoomMeeting for creating a meeting in the user's personal
    #: room. Please note that templateId, roomId, integrationTags, enabledWebcastView, enabledAutoRecordMeeting and
    #: registration are not supported when creating a personal room meeting.
    personal_room_meeting = 'personalRoomMeeting'


class InviteeForCreateMeeting(ApiModel):
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


class Type(str, Enum):
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


class AutoRegistrationResult(str, Enum):
    #: If the user's registration value meets the criteria, the registration form will be automatically approved.
    approve = 'approve'
    #: If the user's registration value meets the criteria, the registration form will be automatically rejected.
    reject = 'reject'


class ApprovalRule(ApiModel):
    #: Judgment expression for approval rules.
    condition: Optional[AnswerCondition]
    #: The keyword for the approval rule. If the rule matches the keyword, the corresponding action will be executed.
    value: Optional[str]
    #: The automatic approval result for the approval rule.
    result: Optional[AutoRegistrationResult]
    #: Whether to check the case of values.
    match_case: Optional[bool]


class CustomizedQuestionForCreateMeeting(ApiModel):
    #: Title of the customized question.
    question: Optional[str]
    #: Whether or not the customized question is required to be answered by participants.
    required: Optional[bool]
    #: Type of the question being asked.
    type: Optional[Type]
    #: The maximum length of a string that can be entered by the user, ranging from 0 to 999. Only required by
    #: singleLineTextBox and multiLineTextBox.
    max_length: Optional[int]
    #: The content of options. Required if the question type is one of checkbox, dropdownList, or radioButtons.
    #: The content of the option.
    options: Optional[list[object]]
    #: The automatic approval rules for customized questions.
    rules: Optional[list[ApprovalRule]]


class ApprovalQuestion(str, Enum):
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


class StandardRegistrationApproveRule(ApprovalRule):
    #: Name for standard question.
    question: Optional[ApprovalQuestion]
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


class InterpreterForSimultaneousInterpretation(ApiModel):
    #: Unique identifier for meeting interpreter.
    id: Optional[str]
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
    interpreters: Optional[list[InterpreterForSimultaneousInterpretation]]


class BreakoutSession(ApiModel):
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


class TrackingCodeItem(ApiModel):
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
    tracking_codes: Optional[list[TrackingCodeItem]]
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


class MeetingState(str, Enum):
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


class MeetingTelephony(ApiModel):
    #: Code for authenticating a user to join teleconference. Users join the teleconference using the call-in number or
    #: the global call-in number, followed by the value of the accessCode.
    access_code: Optional[str]
    #: Array of call-in numbers for joining a teleconference from a phone.
    call_in_numbers: Optional[list[CallInNumbers]]
    #: HATEOAS information of global call-in numbers for joining a teleconference from a phone.
    links: Optional[list[LinkRelation]]


class Meeting(ApiModel):
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
    state: Optional[MeetingState]
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
    telephony: Optional[MeetingTelephony]
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
    simultaneous_interpretation: Optional[SimultaneousInterpretation]
    #: Tracking codes information.
    tracking_codes: Optional[list[TrackingCodeItem]]
    #: Audio connection options.
    audio_connection_options: Optional[AudioConnectionOptions]
    #: If true, the meeting is ad-hoc.
    adhoc: Optional[bool]


class ScheduledMeeting(ApiModel):
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
    state: Optional[MeetingState]
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
    telephony: Optional[MeetingTelephony]
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
    links: Optional[list[LinkRelation]]
    #: Tracking codes information.
    tracking_codes: Optional[list[TrackingCodeItem]]
    #: Audio connection options.
    audio_connection_options: Optional[AudioConnectionOptions]


class PatchMeetingResponse(Meeting):
    #: Whether or not breakout sessions are enabled.
    enabled_breakout_sessions: Optional[bool]
    #: HATEOAS Breakout Sessions information for meeting.
    links: Optional[list[LinkRelation]]


class QuestionType(str, Enum):
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


class QuestionOption(ApiModel):
    #: The unique id of options.
    #: Possible values: 1
    id: Optional[int]
    #: The content of the option.
    #: Possible values: green
    value: Optional[str]


class Question(ApiModel):
    #: Unique identifier for the question.
    id: Optional[int]
    #: Details for the question.
    question: Optional[str]
    #: Type for the question.
    type: Optional[QuestionType]
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
    options: Optional[list[QuestionOption]]


class QuestionAnswer(ApiModel):
    #: Unique identifier for the question option. This attribute will be ingnored, if the value of type attribute is
    #: text or rating.
    option_id: Optional[int]
    #: The user's answers for the question.
    answer: Optional[str]


class QuestionWithAnswers(ApiModel):
    #: Unique identifier for the question.
    id: Optional[int]
    #: Details for the question.
    question: Optional[str]
    #: Type for the question.
    type: Optional[QuestionType]
    #: The user's answers for the question.
    answers: Optional[list[QuestionAnswer]]


class SurveyResult(ApiModel):
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
    questions: Optional[list[QuestionWithAnswers]]


class TrackingCodeOption(ApiModel):
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


class MeetingService(str, Enum):
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


class TrackingCodeType(str, Enum):
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
    invitees: Optional[list[InviteeForCreateMeeting]]
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
    breakout_sessions: Optional[list[BreakoutSession]]


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
    questions: Optional[list[Question]]


class TrackingCode(ApiModel):
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
    options: Optional[list[TrackingCodeOption]]
    #: The input mode in which the tracking code value can be assigned.
    input_mode: Optional[InputMode]
    #: Service for schedule or sign up pages
    service: Optional[MeetingService]
    #: Type for meeting scheduler or meeting start pages.
    type: Optional[TrackingCodeType]


@dataclass(init=False)
class MeetingsApi(ApiChild, base='meetings'):
    """
    Meetings API
    """
    #: meeting chats API
    chats: MeetingChatsApi
    #: closed captions API
    closed_captions: MeetingClosedCaptionsApi
    #: meeting invitees API
    invitees: MeetingInviteesApi
    #: meeting participants API
    participants: MeetingParticipantsApi
    #: preferences API
    preferences: MeetingPreferencesApi
    #: Q and A API
    qanda: MeetingQandAApi
    #: qualities API
    qualities: MeetingQualitiesApi
    #: transcripts
    transcripts: MeetingTranscriptsApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.chats = MeetingChatsApi(session=session)
        self.closed_captions = MeetingClosedCaptionsApi(session=session)
        self.invitees = MeetingInviteesApi(session=session)
        self.participants = MeetingParticipantsApi(session=session)
        self.preferences = MeetingPreferencesApi(session=session)
        self.qanda = MeetingQandAApi(session=session)
        self.qualities = MeetingQualitiesApi(session=session)
        self.transcripts = MeetingTranscriptsApi(session=session)

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
               enabled_breakout_sessions: bool = None, tracking_codes: TrackingCodeItem = None,
               audio_connection_options: AudioConnectionOptions = None, adhoc: bool = None, room_id: str = None,
               template_id: str = None, scheduled_type: ScheduledType = None,
               invitees: InviteeForCreateMeeting = None, registration: Registration = None,
               simultaneous_interpretation: SimultaneousInterpretation = None,
               breakout_sessions: BreakoutSession = None) -> Meeting:
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
        :type tracking_codes: TrackingCodeItem
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
        :type invitees: InviteeForCreateMeeting
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
        :type breakout_sessions: BreakoutSession

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
        return Meeting.parse_obj(data)

    def get(self, meeting_id: str, current: bool = None, host_email: str = None) -> Meeting:
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
            params['current'] = str(current).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}')
        data = super().get(url=url, params=params)
        return Meeting.parse_obj(data)

    def list(self, meeting_number: str = None, web_link: str = None, room_id: str = None, meeting_type: str = None,
             state: str = None, scheduled_type: str = None, current: bool = None, from_: str = None, to_: str = None,
             host_email: str = None, site_url: str = None, integration_tag: str = None,
             **params) -> Generator[Meeting, None, None]:
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
        :type to_: str
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
        return self.session.follow_pagination(url=url, model=Meeting, params=params)

    def list_of_series(self, meeting_series_id: str, from_: str = None, to_: str = None, meeting_type: str = None,
                       state: str = None, is_modified: bool = None, host_email: str = None,
                       **params) -> Generator[ScheduledMeeting, None, None]:
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
        :type to_: str
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
        return self.session.follow_pagination(url=url, model=ScheduledMeeting, params=params)

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
              enabled_breakout_sessions: bool = None, tracking_codes: TrackingCodeItem = None,
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
        :type tracking_codes: TrackingCodeItem
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
               enabled_breakout_sessions: bool = None, tracking_codes: TrackingCodeItem = None,
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
        :type tracking_codes: TrackingCodeItem
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

    def update_simultaneous_interpretation(self, meeting_id: str, enabled: bool,
                                           interpreters:
                                           InterpreterForSimultaneousInterpretation =
                                           None) -> SimultaneousInterpretation:
        """
        Updates simultaneous interpretation options of a meeting with a specified meeting ID. This operation applies to
        meeting series and scheduled meetings. It doesn't apply to ended or in-progress meeting instances.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param enabled: Whether or not simultaneous interpretation is enabled.
        :type enabled: bool
        :param interpreters: Interpreters for meeting.
        :type interpreters: InterpreterForSimultaneousInterpretation

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-meeting-simultaneous-interpretation
        """
        body = SimultaneousInterpretation()
        if enabled is not None:
            body.enabled = enabled
        if interpreters is not None:
            body.interpreters = interpreters
        url = self.ep(f'{meeting_id}/simultaneousInterpretation')
        data = super().put(url=url, data=body.json())
        return SimultaneousInterpretation.parse_obj(data)

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
                            meeting_start_time_to: str = None, **params) -> Generator[SurveyResult, None, None]:
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
        :type meeting_start_time_to: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-survey-results
        """
        if meeting_start_time_from is not None:
            params['meetingStartTimeFrom'] = meeting_start_time_from
        if meeting_start_time_to is not None:
            params['meetingStartTimeTo'] = meeting_start_time_to
        url = self.ep(f'{meeting_id}/surveyResults')
        return self.session.follow_pagination(url=url, model=SurveyResult, params=params)

    def list_tracking_codes(self, service: str, site_url: str = None,
                            host_email: str = None) -> Generator[TrackingCode, None, None]:
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
        return self.session.follow_pagination(url=url, model=TrackingCode, params=params)

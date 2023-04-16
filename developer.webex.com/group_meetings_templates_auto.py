from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Api', 'AttendeePrivileges', 'AudioConnectionOptions', 'AudioConnectionType', 'BreakoutSessionObject',
           'Condition', 'CreateMeetingObject', 'CustomizedQuestionForCreateMeeting', 'EntryAndExitTone',
           'GetMeetingTemplateResponse', 'InterpreterObjectForSimultaneousInterpretationOfCreateOrUpdateMeeting',
           'InviteeObjectForCreateMeeting', 'ListMeetingTemplatesResponse', 'MeetingOptions', 'NoteType', 'Question',
           'Registration', 'Result', 'Rules', 'ScheduledType', 'SimultaneousInterpretation',
           'StandardRegistrationApproveRule', 'TemplateObject', 'TemplateType',
           'TrackingCodeItemForCreateMeetingObject', 'Type', 'UnlockedMeetingJoinSecurity']


class TemplateType(str, Enum):
    #: Webex meeting.
    meeting = 'meeting'
    #: Webex webinar.
    webinar = 'webinar'


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


class UnlockedMeetingJoinSecurity(str, Enum):
    #: If the value of unlockedMeetingJoinSecurity attribute is allowJoin, people can join the unlocked meeting
    #: directly.
    allow_join = 'allowJoin'
    #: If the value of unlockedMeetingJoinSecurity attribute is allowJoinWithLobby, people will wait in the lobby until
    #: the host admits them.
    allow_join_with_lobby = 'allowJoinWithLobby'
    #: If the value of unlockedMeetingJoinSecurity attribute is blockFromJoin, people can't join the unlocked meeting.
    block_from_join = 'blockFromJoin'


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


class Rules(ApiModel):
    #: Judgment expression for approval rules.
    #: Possible values: contains, notContains, beginsWith, endsWith, equals, notEquals
    condition: Optional[str]
    #: The keyword for the approval rule. If the rule matches the keyword, the corresponding action will be executed.
    #: Possible values: tom
    value: Optional[str]
    #: The automatic approval result for the approval rule.
    #: Possible values: approve, reject
    result: Optional[str]
    #: Whether to check the case of values.
    #: Possible values:
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
    #: Possible values: green
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


class Condition(str, Enum):
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


class Result(str, Enum):
    #: If the user's registration value meets the criteria, the registration form will be automatically approved.
    approve = 'approve'
    #: If the user's registration value meets the criteria, the registration form will be automatically rejected.
    reject = 'reject'


class StandardRegistrationApproveRule(ApiModel):
    #: Name for standard question.
    question: Optional[Question]
    #: Judgment expression for approval rules.
    condition: Optional[Condition]
    #: The keyword for the approval rule. If the rule matches the keyword, the corresponding action will be executed.
    value: Optional[str]
    #: The automatic approval result for the approval rule.
    result: Optional[Result]
    #: Whether to check the case of values.
    match_case: Optional[bool]
    #: The priority number of the approval rule. Approval rules for standard questions and custom questions need to be
    #: ordered together.
    order: Optional[int]


class Registration(ApiModel):
    #: Whether or not meeting registration request is accepted automatically.
    auto_accept_request: Optional[bool]
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


class CreateMeetingObject(ApiModel):
    #: Whether or not to create an ad-hoc meeting for the room specified by roomId. When true, roomId is required.
    adhoc: Optional[bool]
    #: Unique identifier for the Webex space which the meeting is to be associated with. It can be retrieved by List
    #: Rooms. roomId is required when adhoc is true. When roomId is specified, the parameter hostEmail will be ignored.
    room_id: Optional[str]
    #: Unique identifier for meeting template. Please note that start and end are optional when templateId is
    #: specified. The list of meeting templates that is available for the authenticated user can be retrieved from List
    #: Meeting Templates. This parameter is ignored for an ad-hoc meeting.
    template_id: Optional[str]
    #: Meeting title. The title can be a maximum of 128 characters long. The default value for an ad-hoc meeting is the
    #: user's name if not specified.
    title: Optional[str]
    #: Meeting agenda. The agenda can be a maximum of 1300 characters long.
    agenda: Optional[str]
    #: Meeting password. Must conform to the site's password complexity settings. Read password management for details.
    #: If not specified, a random password conforming to the site's password rules will be generated automatically.
    password: Optional[str]
    #: Date and time for the start of meeting in any ISO 8601 compliant format. start cannot be before current date and
    #: time or after end. Duration between start and end cannot be shorter than 10 minutes or longer than 24 hours.
    #: Please note that when a meeting is being scheduled, start of the meeting will be accurate to minutes, not
    #: seconds or milliseconds. Therefore, if start is within the same minute as the current time, start will be
    #: adjusted to the upcoming minute; otherwise, start will be adjusted with seconds and milliseconds stripped off.
    #: For instance, if the current time is 2022-03-01T10:32:16.657+08:00, start of 2022-03-01T10:32:28.076+08:00 or
    #: 2022-03-01T10:32:41+08:00 will be adjusted to 2022-03-01T10:33:00+08:00, and start of
    #: 2022-03-01T11:32:28.076+08:00 or 2022-03-01T11:32:41+08:00 will be adjusted to 2022-03-01T11:32:00+08:00. The
    #: default value for an ad-hoc meeting is 5 minutes after the current time and the user's input value will be
    #: ignored. An ad-hoc meeting can be started immediately even if the start is 5 minutes after the current time.
    start: Optional[str]
    #: Date and time for the end of meeting in any ISO 8601 compliant format. end cannot be before current date and
    #: time or before start. Duration between start and end cannot be shorter than 10 minutes or longer than 24 hours.
    #: Please note that when a meeting is being scheduled, end of the meeting will be accurate to minutes, not seconds
    #: or milliseconds. Therefore, end will be adjusted with seconds and milliseconds stripped off. For instance, end
    #: of 2022-03-01T11:52:28.076+08:00 or 2022-03-01T11:52:41+08:00 will be adjusted to 2022-03-01T11:52:00+08:00. The
    #: default value for an ad-hoc meeting is 20 minutes after the current time and the user's input value will be
    #: ignored.
    end: Optional[str]
    #: Time zone in which the meeting was originally scheduled (conforming with the IANA time zone database). The
    #: default value for an ad-hoc meeting is UTC and the user's input value will be ignored.
    timezone: Optional[str]
    #: Meeting series recurrence rule (conforming with RFC 2445), applying only to meeting series. It doesn't apply to
    #: a scheduled meeting or an ended or ongoing meeting instance. This parameter is ignored for an ad-hoc meeting.
    #: Multiple days or dates for monthly or yearly recurrence rule are not supported, only the first day or date
    #: specified is taken. For example, "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it
    #: will be partially supported as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
    recurrence: Optional[str]
    #: Whether or not meeting is recorded automatically.
    enabled_auto_record_meeting: Optional[bool]
    #: Whether or not to allow any attendee with a host account on the target site to become a cohost when joining the
    #: meeting. The target site is specified by siteUrl parameter when creating the meeting; if not specified, it's the
    #: user's preferred site. The default value for an ad-hoc meeting is true and the user's input value will be
    #: ignored.
    allow_any_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow any attendee to join the meeting before the host joins the meeting. The default value
    #: for an ad-hoc meeting is true and the user's input value will be ignored.
    enabled_join_before_host: Optional[bool]
    #: Whether or not to allow any attendee to connect audio in the meeting before the host joins the meeting. This
    #: attribute is only applicable if the enabledJoinBeforeHost attribute is set to true. The default value for an
    #: ad-hoc meeting is true and the user's input value will be ignored.
    enable_connect_audio_before_host: Optional[bool]
    #: the number of minutes an attendee can join the meeting before the meeting start time and the host joins. This
    #: attribute is only applicable if the enabledJoinBeforeHost attribute is set to true. Valid options are 0, 5, 10
    #: and 15. Default is 0 if not specified. The default value for an ad-hoc meeting is 0 and the user's input value
    #: will be ignored.
    join_before_host_minutes: Optional[int]
    #: Whether or not to exclude the meeting password from the email invitation. This parameter is ignored for an
    #: ad-hoc meeting.
    exclude_password: Optional[bool]
    #: Whether or not to allow the meeting to be listed on the public calendar. The default value for an ad-hoc meeting
    #: is false and the user's input value will be ignored.
    public_meeting: Optional[bool]
    #: The number of minutes before the meeting begins, that an email reminder is sent to the host. This parameter is
    #: ignored for an ad-hoc meeting.
    reminder_time: Optional[int]
    #: Specifies how the people who aren't on the invite can join the unlocked meeting. The default value for an ad-hoc
    #: meeting is allowJoinWithLobby and the user's input value will be ignored.
    unlocked_meeting_join_security: Optional[UnlockedMeetingJoinSecurity]
    #: Unique identifier for a meeting session type for the user. This attribute is required when scheduling a webinar
    #: meeting. All available meeting session types enabled for the user can be retrieved using the List Meeting
    #: Session Types API.
    session_type_id: Optional[int]
    #: When set as an attribute in a POST request body, specifies whether it's a regular meeting, a webinar, or a
    #: meeting scheduled in the user's personal room. If not specified, it's a regular meeting by default. The default
    #: value for an ad-hoc meeting is meeting and the user's input value will be ignored.
    scheduled_type: Optional[ScheduledType]
    #: Whether or not webcast view is enabled. This parameter is ignored for an ad-hoc meeting.
    enabled_webcast_view: Optional[bool]
    #: Password for panelists of a webinar meeting. Must conform to the site's password complexity settings. Read
    #: password management for details. If not specified, a random password conforming to the site's password rules
    #: will be generated automatically. This parameter is ignored for an ad-hoc meeting.
    panelist_password: Optional[str]
    #: Whether or not to automatically lock the meeting after it starts. The default value for an ad-hoc meeting is
    #: false and the user's input value will be ignored.
    enable_automatic_lock: Optional[bool]
    #: The number of minutes after the meeting begins, for automatically locking it. The default value for an ad-hoc
    #: meeting is null and the user's input value will be ignored.
    automatic_lock_minutes: Optional[int]
    #: Whether or not to allow the first attendee of the meeting with a host account on the target site to become a
    #: cohost. The target site is specified by siteUrl parameter when creating the meeting; if not specified, it's
    #: user's preferred site. The default value for an ad-hoc meeting is false and the user's input value will be
    #: ignored.
    allow_first_user_to_be_co_host: Optional[bool]
    #: Whether or not to allow authenticated video devices in the meeting's organization to start or join the meeting
    #: without a prompt. The default value for an ad-hoc meeting is true and the user's input value will be ignored.
    allow_authenticated_devices: Optional[bool]
    #: Invitees for meeting. The maximum size of invitees is 1000. If roomId is specified and invitees is missing, all
    #: the members in the space are invited implicitly. If both roomId and invitees are specified, only those in the
    #: invitees list are invited. coHost for each invitee is true by default if roomId is specified when creating a
    #: meeting, and anyone in the invitee list that is not qualified to be a cohost will be invited as a non-cohost
    #: invitee. The user's input value will be ignored for an ad-hoc meeting and the the members of the room specified
    #: by roomId except "me" will be used by default.
    invitees: Optional[list[InviteeObjectForCreateMeeting]]
    #: Whether or not to send emails to host and invitees. It is an optional field and default value is true. The
    #: default value for an ad-hoc meeting is false and the user's input value will be ignored.
    send_email: Optional[bool]
    #: Email address for the meeting host. This attribute should only be set if the user or application calling the API
    #: has the admin-level scopes. When used, the admin may specify the email of a user in a site they manage to be the
    #: meeting host.
    host_email: Optional[str]
    #: URL of the Webex site which the meeting is created on. If not specified, the meeting is created on user's
    #: preferred site. All available Webex sites and preferred site of the user can be retrieved by Get Site List API.
    site_url: Optional[str]
    #: Meeting Options.
    meeting_options: Optional[MeetingOptions]
    #: Attendee Privileges.
    attendee_privileges: Optional[AttendeePrivileges]
    #: Meeting registration. When this option is enabled, meeting invitees must register personal information to join
    #: the meeting. Meeting invitees will receive an email with a registration link for the registration. When the
    #: registration form has been submitted and approved, an email with a real meeting link will be received. By
    #: clicking that link the meeting invitee can join the meeting. Please note that meeting registration does not
    #: apply to a meeting when it's a recurring meeting with a recurrence field or no password, or the Join Before Host
    #: option is enabled for the meeting. See Register for a Meeting in Cisco Webex Meetings for details. This
    #: parameter is ignored for an ad-hoc meeting.
    registration: Optional[Registration]
    #: External keys created by an integration application in its own domain, for example Zendesk ticket IDs, Jira IDs,
    #: Salesforce Opportunity IDs, etc. The integration application queries meetings by a key in its own domain. The
    #: maximum size of integrationTags is 3 and each item of integrationTags can be a maximum of 64 characters long.
    #: This parameter is ignored for an ad-hoc meeting.
    integration_tags: Optional[list[str]]
    #: Simultaneous interpretation information for a meeting.
    simultaneous_interpretation: Optional[SimultaneousInterpretation]
    #: Whether or not breakout sessions are enabled.
    enabled_breakout_sessions: Optional[bool]
    #: Breakout sessions are smaller groups that are split off from the main meeting or webinar. They allow a subset of
    #: participants to collaborate and share ideas over audio and video. Use breakout sessions for workshops,
    #: classrooms, or for when you need a moment to talk privately with a few participants outside of the main session.
    #: Please note that maximum number of breakout sessions in a meeting or webinar is 100. In webinars, if hosts
    #: preassign attendees to breakout sessions, the role of attendee will be changed to panelist. Breakout session is
    #: not supported for a meeting with simultaneous interpretation.
    breakout_sessions: Optional[list[BreakoutSessionObject]]
    #: Tracking codes information. All available tracking codes and their options for the specified site can be
    #: retrieved by List Meeting Tracking Codes API. If an optional tracking code is missing from the trackingCodes
    #: array and there's a default option for this tracking code, the default option is assigned automatically. If the
    #: inputMode of a tracking code is select, its value must be one of the site-level options or the user-level value.
    #: Tracking code is not supported for a personal room meeting or an ad-hoc space meeting.
    tracking_codes: Optional[list[TrackingCodeItemForCreateMeetingObject]]
    #: Audio connection options.
    audio_connection_options: Optional[AudioConnectionOptions]


class ListMeetingTemplatesResponse(ApiModel):
    #: Meeting templates array.
    items: Optional[list[TemplateObject]]


class GetMeetingTemplateResponse(TemplateObject):
    #: Meeting object which is used to create a meeting by the meeting template. Please note that the meeting object
    #: should be used to create a meeting immediately after retrieval since the start and end may be invalid quickly
    #: after generation.
    meeting: Optional[CreateMeetingObject]


class Api(ApiChild, base='meetings/templates'):
    """

    """

    def list_templates(self, template_type: str = None, locale: str = None, is_default: bool = None, is_standard: bool = None, host_email: str = None, site_url: str = None) -> list[TemplateObject]:
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
            params['isDefault'] = str(is_default).lower()
        if is_standard is not None:
            params['isStandard'] = str(is_standard).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep()
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
        url = self.ep(f'{template_id}')
        data = super().get(url=url, params=params)
        return GetMeetingTemplateResponse.parse_obj(data)


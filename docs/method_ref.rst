
Reference of all available methods
==================================

The following table contains a reference of all methods defined in the SDK with a short description of the operation.
The second column of the table has a link to the documentation of the method.

.. list-table::
   :widths: 70 30
   :header-rows: 1

   * - Method
     - Documentation
   * - api.close
        
     - :meth:`~wxc_sdk.WebexSimpleApi.close`
   * - api.attachment_actions.action_details
        Shows details for a attachment action, by ID
     - :meth:`~wxc_sdk.attachment_actions.AttachmentActionsApi.action_details`
   * - api.cdr.get_cdr_history
        Provides Webex Calling Detailed Call History data for your organization
     - :meth:`~wxc_sdk.cdr.DetailedCDRApi.get_cdr_history`
   * - api.devices.activation_code
        Create a Device Activation Code
     - :meth:`~wxc_sdk.devices.DevicesApi.activation_code`
   * - api.devices.delete
        Delete a Device
     - :meth:`~wxc_sdk.devices.DevicesApi.delete`
   * - api.devices.details
        Get Device Details
     - :meth:`~wxc_sdk.devices.DevicesApi.details`
   * - api.devices.list
        List Devices
     - :meth:`~wxc_sdk.devices.DevicesApi.list`
   * - api.devices.modify_device_tags
        Modify Device Tags
     - :meth:`~wxc_sdk.devices.DevicesApi.modify_device_tags`
   * - api.devices.settings_jobs.change
        Change device settings across organization or locations jobs
     - :meth:`~wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.change`
   * - api.devices.settings_jobs.get_status
        Get change device settings job status
     - :meth:`~wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.get_status`
   * - api.devices.settings_jobs.job_errors
        List change device settings job errors
     - :meth:`~wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.job_errors`
   * - api.devices.settings_jobs.list
        List change device settings jobs
     - :meth:`~wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.list`
   * - api.events.details
        Shows details for an event, by event ID
     - :meth:`~wxc_sdk.events.EventsApi.details`
   * - api.events.list
        List events in your organization
     - :meth:`~wxc_sdk.events.EventsApi.list`
   * - api.groups.create
        Create a new group using the provided settings
     - :meth:`~wxc_sdk.groups.GroupsApi.create`
   * - api.groups.delete_group
        Delete a group
     - :meth:`~wxc_sdk.groups.GroupsApi.delete_group`
   * - api.groups.details
        Get group details
     - :meth:`~wxc_sdk.groups.GroupsApi.details`
   * - api.groups.list
        List groups
     - :meth:`~wxc_sdk.groups.GroupsApi.list`
   * - api.groups.members
        Query members of a group
     - :meth:`~wxc_sdk.groups.GroupsApi.members`
   * - api.groups.update
        update group information
     - :meth:`~wxc_sdk.groups.GroupsApi.update`
   * - api.licenses.details
        Shows details for a license, by ID
     - :meth:`~wxc_sdk.licenses.LicensesApi.details`
   * - api.licenses.list
        List all licenses for a given organization
     - :meth:`~wxc_sdk.licenses.LicensesApi.list`
   * - api.locations.by_name
        Get a location by name
     - :meth:`~wxc_sdk.locations.LocationsApi.by_name`
   * - api.locations.create
        Create a new Location for a given organization
     - :meth:`~wxc_sdk.locations.LocationsApi.create`
   * - api.locations.details
        Shows details for a location, by ID
     - :meth:`~wxc_sdk.locations.LocationsApi.details`
   * - api.locations.list
        List locations for an organization
     - :meth:`~wxc_sdk.locations.LocationsApi.list`
   * - api.locations.update
        Update details for a location, by ID
     - :meth:`~wxc_sdk.locations.LocationsApi.update`
   * - api.membership.create
        Add someone to a room by Person ID or email address, optionally making them a moderator
     - :meth:`~wxc_sdk.memberships.MembershipApi.create`
   * - api.membership.delete
        Deletes a membership by ID
     - :meth:`~wxc_sdk.memberships.MembershipApi.delete`
   * - api.membership.details
        Get details for a membership by ID
     - :meth:`~wxc_sdk.memberships.MembershipApi.details`
   * - api.membership.list
        Lists all room memberships
     - :meth:`~wxc_sdk.memberships.MembershipApi.list`
   * - api.membership.update
        Updates properties for a membership by ID
     - :meth:`~wxc_sdk.memberships.MembershipApi.update`
   * - api.messages.create
        Post a plain text or rich text message, and optionally, a file attachment, to a room
     - :meth:`~wxc_sdk.messages.MessagesApi.create`
   * - api.messages.delete
        Delete a message, by message ID
     - :meth:`~wxc_sdk.messages.MessagesApi.delete`
   * - api.messages.details
        Show details for a message, by message ID
     - :meth:`~wxc_sdk.messages.MessagesApi.details`
   * - api.messages.edit
        Update a message you have posted not more than 10 times
     - :meth:`~wxc_sdk.messages.MessagesApi.edit`
   * - api.messages.list
        Lists all messages in a room
     - :meth:`~wxc_sdk.messages.MessagesApi.list`
   * - api.messages.list_direct
        List all messages in a 1:1 (direct) room
     - :meth:`~wxc_sdk.messages.MessagesApi.list_direct`
   * - api.organizations.delete
        Delete Organization
     - :meth:`~wxc_sdk.organizations.OrganizationApi.delete`
   * - api.organizations.details
        Get Organization Details
     - :meth:`~wxc_sdk.organizations.OrganizationApi.details`
   * - api.organizations.list
        List all organizations visible by your account
     - :meth:`~wxc_sdk.organizations.OrganizationApi.list`
   * - api.people.create
        Create a Person
     - :meth:`~wxc_sdk.people.PeopleApi.create`
   * - api.people.delete_person
        Remove a person from the system
     - :meth:`~wxc_sdk.people.PeopleApi.delete_person`
   * - api.people.details
        Shows details for a person, by ID
     - :meth:`~wxc_sdk.people.PeopleApi.details`
   * - api.people.list
        List people in your organization
     - :meth:`~wxc_sdk.people.PeopleApi.list`
   * - api.people.me
        Show the profile for the authenticated user
     - :meth:`~wxc_sdk.people.PeopleApi.me`
   * - api.people.update
        Update details for a person, by ID
     - :meth:`~wxc_sdk.people.PeopleApi.update`
   * - api.person_settings.devices
        Get all devices for a person
     - :meth:`~wxc_sdk.person_settings.PersonSettingsApi.devices`
   * - api.person_settings.reset_vm_pin
        Reset Voicemail PIN
     - :meth:`~wxc_sdk.person_settings.PersonSettingsApi.reset_vm_pin`
   * - api.person_settings.agent_caller_id.available_queues
        Retrieve the list of the person's available call queues and the associated Caller ID information
     - :meth:`~wxc_sdk.person_settings.agent_caller_id.AgentCallerIdApi.available_queues`
   * - api.person_settings.agent_caller_id.ep
        :meta private:
     - :meth:`~wxc_sdk.person_settings.agent_caller_id.AgentCallerIdApi.ep`
   * - api.person_settings.agent_caller_id.read
        Retrieve a call queue agent's Caller ID information
     - :meth:`~wxc_sdk.person_settings.agent_caller_id.AgentCallerIdApi.read`
   * - api.person_settings.agent_caller_id.update
        Modify a call queue agent's Caller ID information
     - :meth:`~wxc_sdk.person_settings.agent_caller_id.AgentCallerIdApi.update`
   * - api.person_settings.appservices.configure
        Modify a Person's Application Services Settings
     - :meth:`~wxc_sdk.person_settings.appservices.AppServicesApi.configure`
   * - api.person_settings.appservices.read
        Retrieve a Person's Application Services Settings
     - :meth:`~wxc_sdk.person_settings.appservices.AppServicesApi.read`
   * - api.person_settings.barge.configure
        Configure a Person's Barge In Settings
     - :meth:`~wxc_sdk.person_settings.barge.BargeApi.configure`
   * - api.person_settings.barge.read
        Retrieve a Person's Barge In Settings
     - :meth:`~wxc_sdk.person_settings.barge.BargeApi.read`
   * - api.person_settings.call_intercept.configure
        Configure Call Intercept Settings for a Person
     - :meth:`~wxc_sdk.person_settings.call_intercept.CallInterceptApi.configure`
   * - api.person_settings.call_intercept.greeting
        Configure Call Intercept Greeting for a Person
     - :meth:`~wxc_sdk.person_settings.call_intercept.CallInterceptApi.greeting`
   * - api.person_settings.call_intercept.read
        Read Call Intercept Settings for a Person
     - :meth:`~wxc_sdk.person_settings.call_intercept.CallInterceptApi.read`
   * - api.person_settings.call_recording.configure
        Configure Call Recording Settings for a Person
     - :meth:`~wxc_sdk.person_settings.call_recording.CallRecordingApi.configure`
   * - api.person_settings.call_recording.read
        Read Call Recording Settings for a Person
     - :meth:`~wxc_sdk.person_settings.call_recording.CallRecordingApi.read`
   * - api.person_settings.call_waiting.configure
        Configure Call Waiting Settings for a Person
     - :meth:`~wxc_sdk.person_settings.call_waiting.CallWaitingApi.configure`
   * - api.person_settings.call_waiting.read
        Read Call Waiting Settings for a Person
     - :meth:`~wxc_sdk.person_settings.call_waiting.CallWaitingApi.read`
   * - api.person_settings.caller_id.configure
        Configure a Person's Caller ID Settings
     - :meth:`~wxc_sdk.person_settings.caller_id.CallerIdApi.configure`
   * - api.person_settings.caller_id.configure_settings
        
     - :meth:`~wxc_sdk.person_settings.caller_id.CallerIdApi.configure_settings`
   * - api.person_settings.caller_id.read
        Retrieve a Person's Caller ID Settings
     - :meth:`~wxc_sdk.person_settings.caller_id.CallerIdApi.read`
   * - api.person_settings.calling_behavior.configure
        Configure a Person's Calling Behavior
     - :meth:`~wxc_sdk.person_settings.calling_behavior.CallingBehaviorApi.configure`
   * - api.person_settings.calling_behavior.read
        Read Person's Calling Behavior
     - :meth:`~wxc_sdk.person_settings.calling_behavior.CallingBehaviorApi.read`
   * - api.person_settings.dnd.configure
        Configure Do Not Disturb Settings for a Person
     - :meth:`~wxc_sdk.person_settings.dnd.DndApi.configure`
   * - api.person_settings.dnd.read
        Read Do Not Disturb Settings for a Person
     - :meth:`~wxc_sdk.person_settings.dnd.DndApi.read`
   * - api.person_settings.exec_assistant.configure
        Modify Executive Assistant Settings for a Person
     - :meth:`~wxc_sdk.person_settings.exec_assistant.ExecAssistantApi.configure`
   * - api.person_settings.exec_assistant.read
        Retrieve Executive Assistant Settings for a Person
     - :meth:`~wxc_sdk.person_settings.exec_assistant.ExecAssistantApi.read`
   * - api.person_settings.forwarding.configure
        Configure a Person's Call Forwarding Settings
     - :meth:`~wxc_sdk.person_settings.forwarding.PersonForwardingApi.configure`
   * - api.person_settings.forwarding.read
        Retrieve a Person's Call Forwarding Settings
     - :meth:`~wxc_sdk.person_settings.forwarding.PersonForwardingApi.read`
   * - api.person_settings.hoteling.configure
        Configure Hoteling Settings for a Person
     - :meth:`~wxc_sdk.person_settings.hoteling.HotelingApi.configure`
   * - api.person_settings.hoteling.read
        Read Hoteling Settings for a Person
     - :meth:`~wxc_sdk.person_settings.hoteling.HotelingApi.read`
   * - api.person_settings.monitoring.configure
        Configure Call Waiting Settings for a Person
     - :meth:`~wxc_sdk.person_settings.monitoring.MonitoringApi.configure`
   * - api.person_settings.monitoring.read
        Retrieve a Person's Monitoring Settings
     - :meth:`~wxc_sdk.person_settings.monitoring.MonitoringApi.read`
   * - api.person_settings.numbers.read
        Get a person's phone numbers including alternate numbers
     - :meth:`~wxc_sdk.person_settings.numbers.NumbersApi.read`
   * - api.person_settings.numbers.update
        Assign or unassign alternate phone numbers to a person
     - :meth:`~wxc_sdk.person_settings.numbers.NumbersApi.update`
   * - api.person_settings.permissions_in.configure
        Configure a Person's Barge In Settings
     - :meth:`~wxc_sdk.person_settings.permissions_in.IncomingPermissionsApi.configure`
   * - api.person_settings.permissions_in.read
        Read Incoming Permission Settings for a Person
     - :meth:`~wxc_sdk.person_settings.permissions_in.IncomingPermissionsApi.read`
   * - api.person_settings.permissions_out.configure
        Configure a Person's Outgoing Calling Permissions Settings
     - :meth:`~wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.configure`
   * - api.person_settings.permissions_out.read
        Retrieve a Person's Outgoing Calling Permissions Settings
     - :meth:`~wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.read`
   * - api.person_settings.privacy.configure
        Configure Call Waiting Settings for a Person
     - :meth:`~wxc_sdk.person_settings.privacy.PrivacyApi.configure`
   * - api.person_settings.privacy.read
        Get a person's Privacy Settings
     - :meth:`~wxc_sdk.person_settings.privacy.PrivacyApi.read`
   * - api.person_settings.push_to_talk.configure
        Configure Push-to-Talk Settings for a Person
     - :meth:`~wxc_sdk.person_settings.push_to_talk.PushToTalkApi.configure`
   * - api.person_settings.push_to_talk.read
        Read Push-to-Talk Settings for a Person
     - :meth:`~wxc_sdk.person_settings.push_to_talk.PushToTalkApi.read`
   * - api.person_settings.receptionist.configure
        Modify Executive Assistant Settings for a Person
     - :meth:`~wxc_sdk.person_settings.receptionist.ReceptionistApi.configure`
   * - api.person_settings.receptionist.read
        Read Receptionist Client Settings for a Person
     - :meth:`~wxc_sdk.person_settings.receptionist.ReceptionistApi.read`
   * - api.person_settings.schedules.create
        Create a Schedule
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.create`
   * - api.person_settings.schedules.delete_schedule
        Delete a Schedule
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.delete_schedule`
   * - api.person_settings.schedules.details
        Get Details for a Schedule
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.details`
   * - api.person_settings.schedules.event_create
        Create a Schedule Event
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.event_create`
   * - api.person_settings.schedules.event_delete
        Delete a Schedule Event
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.event_delete`
   * - api.person_settings.schedules.event_details
        Get Details for a Schedule Event
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.event_details`
   * - api.person_settings.schedules.event_update
        Update a Schedule Event
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.event_update`
   * - api.person_settings.schedules.list
        List of Schedules for a Person or location
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.list`
   * - api.person_settings.schedules.update
        Update a Schedule
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.update`
   * - api.person_settings.voicemail.configure
        Configure Voicemail Settings for a Person
     - :meth:`~wxc_sdk.person_settings.voicemail.VoicemailApi.configure`
   * - api.person_settings.voicemail.configure_busy_greeting
        Configure Busy Voicemail Greeting for a Person
     - :meth:`~wxc_sdk.person_settings.voicemail.VoicemailApi.configure_busy_greeting`
   * - api.person_settings.voicemail.configure_no_answer_greeting
        Configure No Answer Voicemail Greeting for a Person
     - :meth:`~wxc_sdk.person_settings.voicemail.VoicemailApi.configure_no_answer_greeting`
   * - api.person_settings.voicemail.read
        Read Voicemail Settings for a Person
     - :meth:`~wxc_sdk.person_settings.voicemail.VoicemailApi.read`
   * - api.reports.create
        Create a new report
     - :meth:`~wxc_sdk.reports.ReportsApi.create`
   * - api.reports.delete
        Remove a report from the system
     - :meth:`~wxc_sdk.reports.ReportsApi.delete`
   * - api.reports.details
        Shows details for a report, by report ID
     - :meth:`~wxc_sdk.reports.ReportsApi.details`
   * - api.reports.download
        Download a report from the given URL and yield the rows as dicts
     - :meth:`~wxc_sdk.reports.ReportsApi.download`
   * - api.reports.list
        Lists all reports
     - :meth:`~wxc_sdk.reports.ReportsApi.list`
   * - api.reports.list_templates
        List all the available report templates that can be generated
     - :meth:`~wxc_sdk.reports.ReportsApi.list_templates`
   * - api.room_tabs.create_tab
        Add a tab with a specified URL to a room
     - :meth:`~wxc_sdk.room_tabs.RoomTabsApi.create_tab`
   * - api.room_tabs.delete_tab
        Deletes a Room Tab with the specified ID
     - :meth:`~wxc_sdk.room_tabs.RoomTabsApi.delete_tab`
   * - api.room_tabs.list_tabs
        Lists all Room Tabs of a room specified by the roomId query parameter
     - :meth:`~wxc_sdk.room_tabs.RoomTabsApi.list_tabs`
   * - api.room_tabs.tab_details
        Get details for a Room Tab with the specified room tab ID
     - :meth:`~wxc_sdk.room_tabs.RoomTabsApi.tab_details`
   * - api.room_tabs.update_tab
        Updates the content URL of the specified Room Tab ID
     - :meth:`~wxc_sdk.room_tabs.RoomTabsApi.update_tab`
   * - api.rooms.create
        Creates a room
     - :meth:`~wxc_sdk.rooms.RoomsApi.create`
   * - api.rooms.delete
        Deletes a room, by ID
     - :meth:`~wxc_sdk.rooms.RoomsApi.delete`
   * - api.rooms.details
        Shows details for a room, by ID
     - :meth:`~wxc_sdk.rooms.RoomsApi.details`
   * - api.rooms.list
        List rooms
     - :meth:`~wxc_sdk.rooms.RoomsApi.list`
   * - api.rooms.meeting_details
        Shows Webex meeting details for a room such as the SIP address, meeting URL, toll-free and toll dial-in numbers
     - :meth:`~wxc_sdk.rooms.RoomsApi.meeting_details`
   * - api.rooms.update
        Updates details for a room
     - :meth:`~wxc_sdk.rooms.RoomsApi.update`
   * - api.team_memberships.create
        Add someone to a team by Person ID or email address, optionally making them a moderator
     - :meth:`~wxc_sdk.team_memberships.TeamMembershipsApi.create`
   * - api.team_memberships.delete
        Deletes a team membership, by ID
     - :meth:`~wxc_sdk.team_memberships.TeamMembershipsApi.delete`
   * - api.team_memberships.details
        Shows details for a team membership, by ID
     - :meth:`~wxc_sdk.team_memberships.TeamMembershipsApi.details`
   * - api.team_memberships.list
        Lists all team memberships for a given team, specified by the teamId query parameter
     - :meth:`~wxc_sdk.team_memberships.TeamMembershipsApi.list`
   * - api.team_memberships.membership
        Updates a team membership, by ID
     - :meth:`~wxc_sdk.team_memberships.TeamMembershipsApi.membership`
   * - api.teams.create
        Creates a team
     - :meth:`~wxc_sdk.teams.TeamsApi.create`
   * - api.teams.delete
        Deletes a team, by ID
     - :meth:`~wxc_sdk.teams.TeamsApi.delete`
   * - api.teams.details
        Shows details for a team, by ID
     - :meth:`~wxc_sdk.teams.TeamsApi.details`
   * - api.teams.list
        Lists teams to which the authenticated user belongs
     - :meth:`~wxc_sdk.teams.TeamsApi.list`
   * - api.teams.update
        Updates details for a team, by ID
     - :meth:`~wxc_sdk.teams.TeamsApi.update`
   * - api.telephony.device_settings
        Get device override settings for an organization
     - :meth:`~wxc_sdk.telephony.TelephonyApi.device_settings`
   * - api.telephony.phone_number_details
        get summary (counts) of phone numbers
     - :meth:`~wxc_sdk.telephony.TelephonyApi.phone_number_details`
   * - api.telephony.phone_numbers
        Get Phone Numbers for an Organization with given criteria
     - :meth:`~wxc_sdk.telephony.TelephonyApi.phone_numbers`
   * - api.telephony.route_choices
        List all Routes for the organization
     - :meth:`~wxc_sdk.telephony.TelephonyApi.route_choices`
   * - api.telephony.supported_devices
        Gets the list of supported devices for an organization location
     - :meth:`~wxc_sdk.telephony.TelephonyApi.supported_devices`
   * - api.telephony.test_call_routing
        Validates that an incoming call can be routed
     - :meth:`~wxc_sdk.telephony.TelephonyApi.test_call_routing`
   * - api.telephony.ucm_profiles
        Read the List of UC Manager Profiles
     - :meth:`~wxc_sdk.telephony.TelephonyApi.ucm_profiles`
   * - api.telephony.validate_extensions
        Validate the List of Extensions
     - :meth:`~wxc_sdk.telephony.TelephonyApi.validate_extensions`
   * - api.telephony.validate_phone_numbers
        Validate the list of phone numbers in an organization
     - :meth:`~wxc_sdk.telephony.TelephonyApi.validate_phone_numbers`
   * - api.telephony.access_codes.create
        Create access code in location
     - :meth:`~wxc_sdk.telephony.access_codes.AccessCodesApi.create`
   * - api.telephony.access_codes.delete_codes
        Delete Access Code Location
     - :meth:`~wxc_sdk.telephony.access_codes.AccessCodesApi.delete_codes`
   * - api.telephony.access_codes.read
        Get Location Access Code
     - :meth:`~wxc_sdk.telephony.access_codes.AccessCodesApi.read`
   * - api.telephony.auto_attendant.by_name
        Get auto attendant info by name
     - :meth:`~wxc_sdk.telephony.autoattendant.AutoAttendantApi.by_name`
   * - api.telephony.auto_attendant.create
        Create an Auto Attendant
     - :meth:`~wxc_sdk.telephony.autoattendant.AutoAttendantApi.create`
   * - api.telephony.auto_attendant.delete_auto_attendant
        elete the designated Auto Attendant
     - :meth:`~wxc_sdk.telephony.autoattendant.AutoAttendantApi.delete_auto_attendant`
   * - api.telephony.auto_attendant.details
        Get Details for an Auto Attendant
     - :meth:`~wxc_sdk.telephony.autoattendant.AutoAttendantApi.details`
   * - api.telephony.auto_attendant.list
        Read the List of Auto Attendants
     - :meth:`~wxc_sdk.telephony.autoattendant.AutoAttendantApi.list`
   * - api.telephony.auto_attendant.update
        Update an Auto Attendant
     - :meth:`~wxc_sdk.telephony.autoattendant.AutoAttendantApi.update`
   * - api.telephony.call_intercept.configure
        Put Location Intercept
     - :meth:`~wxc_sdk.telephony.location.intercept.LocationInterceptApi.configure`
   * - api.telephony.call_intercept.read
        Get Location Intercept
     - :meth:`~wxc_sdk.telephony.location.intercept.LocationInterceptApi.read`
   * - api.telephony.callpark.available_agents
        Get available agents from Call Parks
     - :meth:`~wxc_sdk.telephony.callpark.CallParkApi.available_agents`
   * - api.telephony.callpark.available_recalls
        Get available recall hunt groups from Call Parks
     - :meth:`~wxc_sdk.telephony.callpark.CallParkApi.available_recalls`
   * - api.telephony.callpark.call_park_settings
        Get Call Park Settings
     - :meth:`~wxc_sdk.telephony.callpark.CallParkApi.call_park_settings`
   * - api.telephony.callpark.create
        Create a Call Park
     - :meth:`~wxc_sdk.telephony.callpark.CallParkApi.create`
   * - api.telephony.callpark.delete_callpark
        Delete a Call Park
     - :meth:`~wxc_sdk.telephony.callpark.CallParkApi.delete_callpark`
   * - api.telephony.callpark.details
        Get Details for a Call Park
     - :meth:`~wxc_sdk.telephony.callpark.CallParkApi.details`
   * - api.telephony.callpark.list
        Read the List of Call Parks
     - :meth:`~wxc_sdk.telephony.callpark.CallParkApi.list`
   * - api.telephony.callpark.update
        Update a Call Park
     - :meth:`~wxc_sdk.telephony.callpark.CallParkApi.update`
   * - api.telephony.callpark.update_call_park_settings
        Update Call Park settings
     - :meth:`~wxc_sdk.telephony.callpark.CallParkApi.update_call_park_settings`
   * - api.telephony.callpark_extension.create
        Create new Call Park Extensions for the given location
     - :meth:`~wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.create`
   * - api.telephony.callpark_extension.delete
        Delete the designated Call Park Extension
     - :meth:`~wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.delete`
   * - api.telephony.callpark_extension.details
        Get Details for a Call Park Extension
     - :meth:`~wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.details`
   * - api.telephony.callpark_extension.list
        Read the List of Call Park Extensions
     - :meth:`~wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.list`
   * - api.telephony.callpark_extension.update
        Update the designated Call Park Extension
     - :meth:`~wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.update`
   * - api.telephony.calls.answer
        Answer an incoming call on the user's primary device
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.answer`
   * - api.telephony.calls.barge_in
        Barge-in on another user’s answered call
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.barge_in`
   * - api.telephony.calls.call_details
        Get the details of the specified active call for the user
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.call_details`
   * - api.telephony.calls.call_history
        List Call History
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.call_history`
   * - api.telephony.calls.dial
        Initiate an outbound call to a specified destination
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.dial`
   * - api.telephony.calls.divert
        Divert a call to a destination or a user's voicemail
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.divert`
   * - api.telephony.calls.hangup
        Hangup a call
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.hangup`
   * - api.telephony.calls.hold
        Hold a connected call
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.hold`
   * - api.telephony.calls.list_calls
        Get the list of details for all active calls associated with the user
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.list_calls`
   * - api.telephony.calls.park
        Park a connected call
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.park`
   * - api.telephony.calls.pause_recording
        Pause recording on a call
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.pause_recording`
   * - api.telephony.calls.pickup
        Picks up an incoming call to another user
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.pickup`
   * - api.telephony.calls.push
        Pushes a call from the assistant to the executive the call is associated with
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.push`
   * - api.telephony.calls.reject
        Reject an unanswered incoming call
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.reject`
   * - api.telephony.calls.resume
        Resume a held call
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.resume`
   * - api.telephony.calls.resume_recording
        Resume recording a call
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.resume_recording`
   * - api.telephony.calls.retrieve
        :param destination: Identifies where the call is parked
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.retrieve`
   * - api.telephony.calls.start_recording
        Start recording a call
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.start_recording`
   * - api.telephony.calls.stop_recording
        Stop recording a call
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.stop_recording`
   * - api.telephony.calls.transfer
        Transfer two calls together
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.transfer`
   * - api.telephony.calls.transmit_dtmf
        Transmit DTMF digits to a call
     - :meth:`~wxc_sdk.telephony.calls.CallsApi.transmit_dtmf`
   * - api.telephony.devices.apply_changes
        Apply Changes for a specific device
     - :meth:`~wxc_sdk.telephony.devices.TelephonyDevicesApi.apply_changes`
   * - api.telephony.devices.available_members
        Search members that can be assigned to the device
     - :meth:`~wxc_sdk.telephony.devices.TelephonyDevicesApi.available_members`
   * - api.telephony.devices.dect_devices
        Read the DECT device type list
     - :meth:`~wxc_sdk.telephony.devices.TelephonyDevicesApi.dect_devices`
   * - api.telephony.devices.device_settings
        Get override settings for a device
     - :meth:`~wxc_sdk.telephony.devices.TelephonyDevicesApi.device_settings`
   * - api.telephony.devices.members
        Get Device Members
     - :meth:`~wxc_sdk.telephony.devices.TelephonyDevicesApi.members`
   * - api.telephony.devices.update_device_settings
        Modify override settings for a device
     - :meth:`~wxc_sdk.telephony.devices.TelephonyDevicesApi.update_device_settings`
   * - api.telephony.devices.update_members
        Modify member details on the device
     - :meth:`~wxc_sdk.telephony.devices.TelephonyDevicesApi.update_members`
   * - api.telephony.devices.validate_macs
        Validate a list of MAC addresses
     - :meth:`~wxc_sdk.telephony.devices.TelephonyDevicesApi.validate_macs`
   * - api.telephony.huntgroup.by_name
        Get hunt group info by name
     - :meth:`~wxc_sdk.telephony.huntgroup.HuntGroupApi.by_name`
   * - api.telephony.huntgroup.create
        Create a Hunt Group
     - :meth:`~wxc_sdk.telephony.huntgroup.HuntGroupApi.create`
   * - api.telephony.huntgroup.delete_huntgroup
        Delete a Hunt Group
     - :meth:`~wxc_sdk.telephony.huntgroup.HuntGroupApi.delete_huntgroup`
   * - api.telephony.huntgroup.details
        Get Details for a Hunt Group
     - :meth:`~wxc_sdk.telephony.huntgroup.HuntGroupApi.details`
   * - api.telephony.huntgroup.list
        Read the List of Hunt Groups
     - :meth:`~wxc_sdk.telephony.huntgroup.HuntGroupApi.list`
   * - api.telephony.huntgroup.update
        Update a Hunt Group
     - :meth:`~wxc_sdk.telephony.huntgroup.HuntGroupApi.update`
   * - api.telephony.jobs.device_settings.change
        Change device settings across organization or locations jobs
     - :meth:`~wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.change`
   * - api.telephony.jobs.device_settings.get_status
        Get change device settings job status
     - :meth:`~wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.get_status`
   * - api.telephony.jobs.device_settings.job_errors
        List change device settings job errors
     - :meth:`~wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.job_errors`
   * - api.telephony.jobs.device_settings.list
        List change device settings jobs
     - :meth:`~wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.list`
   * - api.telephony.jobs.manage_numbers.abandon_job
        Abandon the Manage Numbers Job
     - :meth:`~wxc_sdk.telephony.jobs.ManageNumbersJobsApi.abandon_job`
   * - api.telephony.jobs.manage_numbers.initiate_job
        Starts the numbers move from one location to another location
     - :meth:`~wxc_sdk.telephony.jobs.ManageNumbersJobsApi.initiate_job`
   * - api.telephony.jobs.manage_numbers.job_status
        Returns the status and other details of the job
     - :meth:`~wxc_sdk.telephony.jobs.ManageNumbersJobsApi.job_status`
   * - api.telephony.jobs.manage_numbers.list_job_errors
        Lists all error details of Manage Numbers job
     - :meth:`~wxc_sdk.telephony.jobs.ManageNumbersJobsApi.list_job_errors`
   * - api.telephony.jobs.manage_numbers.list_jobs
        Lists all Manage Numbers jobs for the given organization in order of most recent one to oldest one
     - :meth:`~wxc_sdk.telephony.jobs.ManageNumbersJobsApi.list_jobs`
   * - api.telephony.jobs.manage_numbers.pause_job
        Pause the running Manage Numbers Job
     - :meth:`~wxc_sdk.telephony.jobs.ManageNumbersJobsApi.pause_job`
   * - api.telephony.jobs.manage_numbers.resume_job
        Resume the paused Manage Numbers Job
     - :meth:`~wxc_sdk.telephony.jobs.ManageNumbersJobsApi.resume_job`
   * - api.telephony.location.change_announcement_language
        Change Announcement Language
     - :meth:`~wxc_sdk.telephony.location.TelephonyLocationApi.change_announcement_language`
   * - api.telephony.location.details
        Shows Webex Calling details for a location, by ID
     - :meth:`~wxc_sdk.telephony.location.TelephonyLocationApi.details`
   * - api.telephony.location.device_settings
        Get device override settings for a location
     - :meth:`~wxc_sdk.telephony.location.TelephonyLocationApi.device_settings`
   * - api.telephony.location.generate_password
        Generates an example password using the effective password settings for the location
     - :meth:`~wxc_sdk.telephony.location.TelephonyLocationApi.generate_password`
   * - api.telephony.location.update
        Update Webex Calling details for a location, by ID
     - :meth:`~wxc_sdk.telephony.location.TelephonyLocationApi.update`
   * - api.telephony.location.validate_extensions
        Validate extensions for a specific location
     - :meth:`~wxc_sdk.telephony.location.TelephonyLocationApi.validate_extensions`
   * - api.telephony.location.intercept.configure
        Put Location Intercept
     - :meth:`~wxc_sdk.telephony.location.intercept.LocationInterceptApi.configure`
   * - api.telephony.location.intercept.read
        Get Location Intercept
     - :meth:`~wxc_sdk.telephony.location.intercept.LocationInterceptApi.read`
   * - api.telephony.location.internal_dialing.read
        Get current configuration for routing unknown extensions to the Premises as internal calls
     - :meth:`~wxc_sdk.telephony.location.internal_dialing.InternalDialingApi.read`
   * - api.telephony.location.internal_dialing.update
        Modify current configuration for routing unknown extensions to the Premises as internal calls
     - :meth:`~wxc_sdk.telephony.location.internal_dialing.InternalDialingApi.update`
   * - api.telephony.location.internal_dialing.url
        
     - :meth:`~wxc_sdk.telephony.location.internal_dialing.InternalDialingApi.url`
   * - api.telephony.location.moh.create
        :param location_id: Add new access code for this location
     - :meth:`~wxc_sdk.telephony.location.moh.LocationMoHApi.create`
   * - api.telephony.location.moh.delete_codes
        Delete Access Code Location
     - :meth:`~wxc_sdk.telephony.location.moh.LocationMoHApi.delete_codes`
   * - api.telephony.location.moh.read
        Get Music On Hold
     - :meth:`~wxc_sdk.telephony.location.moh.LocationMoHApi.read`
   * - api.telephony.location.moh.update
        Get Music On Hold
     - :meth:`~wxc_sdk.telephony.location.moh.LocationMoHApi.update`
   * - api.telephony.location.number.activate
        Activate the specified set of phone numbers in a location for an organization
     - :meth:`~wxc_sdk.telephony.location.numbers.LocationNumbersApi.activate`
   * - api.telephony.location.number.add
        Adds specified set of phone numbers to a location for an organization
     - :meth:`~wxc_sdk.telephony.location.numbers.LocationNumbersApi.add`
   * - api.telephony.location.number.remove
        Remove the specified set of phone numbers from a location for an organization
     - :meth:`~wxc_sdk.telephony.location.numbers.LocationNumbersApi.remove`
   * - api.telephony.location.voicemail.read
        Get Location Voicemail
     - :meth:`~wxc_sdk.telephony.location.vm.LocationVoicemailSettingsApi.read`
   * - api.telephony.location.voicemail.update
        Get Location Voicemail
     - :meth:`~wxc_sdk.telephony.location.vm.LocationVoicemailSettingsApi.update`
   * - api.telephony.organisation_voicemail.read
        Get Voicemail Settings
     - :meth:`~wxc_sdk.telephony.organisation_vm.OrganisationVoicemailSettingsAPI.read`
   * - api.telephony.organisation_voicemail.update
        Update the organization's voicemail settings
     - :meth:`~wxc_sdk.telephony.organisation_vm.OrganisationVoicemailSettingsAPI.update`
   * - api.telephony.paging.create
        Create a new Paging Group
     - :meth:`~wxc_sdk.telephony.paging.PagingApi.create`
   * - api.telephony.paging.delete_paging
        Delete a Paging Group
     - :meth:`~wxc_sdk.telephony.paging.PagingApi.delete_paging`
   * - api.telephony.paging.details
        Get Details for a Paging Group
     - :meth:`~wxc_sdk.telephony.paging.PagingApi.details`
   * - api.telephony.paging.list
        Read the List of Paging Groups
     - :meth:`~wxc_sdk.telephony.paging.PagingApi.list`
   * - api.telephony.paging.update
        Update the designated Paging Group
     - :meth:`~wxc_sdk.telephony.paging.PagingApi.update`
   * - api.telephony.permissions_out.configure
        Configure a Person's Outgoing Calling Permissions Settings
     - :meth:`~wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.configure`
   * - api.telephony.permissions_out.read
        Retrieve a Person's Outgoing Calling Permissions Settings
     - :meth:`~wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.read`
   * - api.telephony.permissions_out.transfer_numbers.configure
        Modify Transfer Numbers Settings for a Place
     - :meth:`~wxc_sdk.person_settings.permissions_out.TransferNumbersApi.configure`
   * - api.telephony.permissions_out.transfer_numbers.read
        Retrieve Transfer Numbers Settings for a Workspace
     - :meth:`~wxc_sdk.person_settings.permissions_out.TransferNumbersApi.read`
   * - api.telephony.pickup.available_agents
        Get available agents from Call Pickups
     - :meth:`~wxc_sdk.telephony.callpickup.CallPickupApi.available_agents`
   * - api.telephony.pickup.create
        Create a Call Pickup
     - :meth:`~wxc_sdk.telephony.callpickup.CallPickupApi.create`
   * - api.telephony.pickup.delete_pickup
        Delete a Call Pickup
     - :meth:`~wxc_sdk.telephony.callpickup.CallPickupApi.delete_pickup`
   * - api.telephony.pickup.details
        Get Details for a Call Pickup
     - :meth:`~wxc_sdk.telephony.callpickup.CallPickupApi.details`
   * - api.telephony.pickup.list
        Read the List of Call Pickups
     - :meth:`~wxc_sdk.telephony.callpickup.CallPickupApi.list`
   * - api.telephony.pickup.update
        Update a Call Pickup
     - :meth:`~wxc_sdk.telephony.callpickup.CallPickupApi.update`
   * - api.telephony.pnc.read
        Get Private Network Connect
     - :meth:`~wxc_sdk.telephony.pnc.PrivateNetworkConnectApi.read`
   * - api.telephony.pnc.update
        Get Private Network Connect
     - :meth:`~wxc_sdk.telephony.pnc.PrivateNetworkConnectApi.update`
   * - api.telephony.prem_pstn.validate_pattern
        Validate a Dial Pattern
     - :meth:`~wxc_sdk.telephony.prem_pstn.PremisePstnApi.validate_pattern`
   * - api.telephony.prem_pstn.dial_plan.create
        Create a Dial Plan for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.create`
   * - api.telephony.prem_pstn.dial_plan.delete_all_patterns
        Delete all dial patterns from the Dial Plan
     - :meth:`~wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.delete_all_patterns`
   * - api.telephony.prem_pstn.dial_plan.delete_dial_plan
        Delete a Dial Plan for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.delete_dial_plan`
   * - api.telephony.prem_pstn.dial_plan.details
        Get a Dial Plan for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.details`
   * - api.telephony.prem_pstn.dial_plan.list
        List all Dial Plans for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.list`
   * - api.telephony.prem_pstn.dial_plan.modify_patterns
        Modify dial patterns for the Dial Plan
     - :meth:`~wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.modify_patterns`
   * - api.telephony.prem_pstn.dial_plan.patterns
        List all Dial Patterns for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.patterns`
   * - api.telephony.prem_pstn.dial_plan.update
        Modify a Dial Plan for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.update`
   * - api.telephony.prem_pstn.route_group.create
        Creates a Route Group for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.create`
   * - api.telephony.prem_pstn.route_group.delete_route_group
        Remove a Route Group from an Organization based on id
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.delete_route_group`
   * - api.telephony.prem_pstn.route_group.details
        Reads a Route Group for the organization based on id
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.details`
   * - api.telephony.prem_pstn.route_group.list
        List all Route Groups for an organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.list`
   * - api.telephony.prem_pstn.route_group.update
        Modifies an existing Route Group for an organization based on id
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.update`
   * - api.telephony.prem_pstn.route_group.usage
        List the number of "Call to" on-premises Extensions, Dial Plans, PSTN Connections, and Route Lists used by a
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.usage`
   * - api.telephony.prem_pstn.route_group.usage_call_to_extension
        List "Call to" on-premises Extension Locations for a specific route group
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.usage_call_to_extension`
   * - api.telephony.prem_pstn.route_group.usage_dial_plan
        List Dial Plan Locations for a specific route group
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.usage_dial_plan`
   * - api.telephony.prem_pstn.route_group.usage_location_pstn
        List PSTN Connection Locations for a specific route group
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.usage_location_pstn`
   * - api.telephony.prem_pstn.route_group.usage_route_lists
        List Route Lists for a specific route group
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.usage_route_lists`
   * - api.telephony.prem_pstn.route_list.create
        Create a Route List for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.create`
   * - api.telephony.prem_pstn.route_list.delete_all_numbers
        
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.delete_all_numbers`
   * - api.telephony.prem_pstn.route_list.delete_route_list
        Delete Route List for a Customer
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.delete_route_list`
   * - api.telephony.prem_pstn.route_list.details
        Get Route List Details
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.details`
   * - api.telephony.prem_pstn.route_list.list
        List all Route Lists for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.list`
   * - api.telephony.prem_pstn.route_list.numbers
        Get numbers assigned to a Route List
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.numbers`
   * - api.telephony.prem_pstn.route_list.update
        Modify the details for a Route List
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.update`
   * - api.telephony.prem_pstn.route_list.update_numbers
        Modify numbers for a specific Route List of a Customer
     - :meth:`~wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.update_numbers`
   * - api.telephony.prem_pstn.trunk.create
        Create a Trunk for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.create`
   * - api.telephony.prem_pstn.trunk.delete_trunk
        Delete a Trunk for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.delete_trunk`
   * - api.telephony.prem_pstn.trunk.details
        Get a Trunk for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.details`
   * - api.telephony.prem_pstn.trunk.list
        List all Trunks for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.list`
   * - api.telephony.prem_pstn.trunk.trunk_types
        List all TrunkTypes with DeviceTypes for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.trunk_types`
   * - api.telephony.prem_pstn.trunk.update
        Modify a Trunk for the organization
     - :meth:`~wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.update`
   * - api.telephony.prem_pstn.trunk.usage
        Get Local Gateway Usage Count
     - :meth:`~wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.usage`
   * - api.telephony.prem_pstn.trunk.usage_dial_plan
        Get Local Gateway Dial Plan Usage for a Trunk
     - :meth:`~wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.usage_dial_plan`
   * - api.telephony.prem_pstn.trunk.usage_location_pstn
        Get Local Gateway Dial Plan Usage for a Trunk
     - :meth:`~wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.usage_location_pstn`
   * - api.telephony.prem_pstn.trunk.usage_route_group
        Get Local Gateway Dial Plan Usage for a Trunk
     - :meth:`~wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.usage_route_group`
   * - api.telephony.prem_pstn.trunk.validate_fqdn_and_domain
        Validate Local Gateway FQDN and Domain for the organization trunks
     - :meth:`~wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.validate_fqdn_and_domain`
   * - api.telephony.schedules.create
        Create a Schedule
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.create`
   * - api.telephony.schedules.delete_schedule
        Delete a Schedule
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.delete_schedule`
   * - api.telephony.schedules.details
        Get Details for a Schedule
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.details`
   * - api.telephony.schedules.event_create
        Create a Schedule Event
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.event_create`
   * - api.telephony.schedules.event_delete
        Delete a Schedule Event
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.event_delete`
   * - api.telephony.schedules.event_details
        Get Details for a Schedule Event
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.event_details`
   * - api.telephony.schedules.event_update
        Update a Schedule Event
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.event_update`
   * - api.telephony.schedules.list
        List of Schedules for a Person or location
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.list`
   * - api.telephony.schedules.update
        Update a Schedule
     - :meth:`~wxc_sdk.common.schedules.ScheduleApi.update`
   * - api.telephony.voice_messaging.delete
        Delete a specfic voicemail message for the user
     - :meth:`~wxc_sdk.telephony.voice_messaging.VoiceMessagingApi.delete`
   * - api.telephony.voice_messaging.list
        Get the list of all voicemail messages for the user
     - :meth:`~wxc_sdk.telephony.voice_messaging.VoiceMessagingApi.list`
   * - api.telephony.voice_messaging.mark_as_read
        Update the voicemail message(s) as read for the user
     - :meth:`~wxc_sdk.telephony.voice_messaging.VoiceMessagingApi.mark_as_read`
   * - api.telephony.voice_messaging.mark_as_unread
        Update the voicemail message(s) as unread for the user
     - :meth:`~wxc_sdk.telephony.voice_messaging.VoiceMessagingApi.mark_as_unread`
   * - api.telephony.voice_messaging.summary
        Get a summary of the voicemail messages for the user
     - :meth:`~wxc_sdk.telephony.voice_messaging.VoiceMessagingApi.summary`
   * - api.telephony.voicemail_groups.create
        Create new voicemail group for the given location for a customer
     - :meth:`~wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.create`
   * - api.telephony.voicemail_groups.delete
        Delete the designated voicemail group
     - :meth:`~wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.delete`
   * - api.telephony.voicemail_groups.details
        Retrieve voicemail group details for a location
     - :meth:`~wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.details`
   * - api.telephony.voicemail_groups.ep
        :param location_id:
     - :meth:`~wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.ep`
   * - api.telephony.voicemail_groups.list
        List the voicemail group information for the organization
     - :meth:`~wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.list`
   * - api.telephony.voicemail_groups.update
        Modifies the voicemail group location details for a particular location for a customer
     - :meth:`~wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.update`
   * - api.telephony.voicemail_rules.read
        Get Voicemail Rules
     - :meth:`~wxc_sdk.telephony.vm_rules.VoicemailRulesApi.read`
   * - api.telephony.voicemail_rules.update
        Update Voicemail Rules
     - :meth:`~wxc_sdk.telephony.vm_rules.VoicemailRulesApi.update`
   * - api.telephony.voiceportal.passcode_rules
        Get VoicePortal Passcode Rule
     - :meth:`~wxc_sdk.telephony.voiceportal.VoicePortalApi.passcode_rules`
   * - api.telephony.voiceportal.read
        :param location_id: Location to which the voice portal belongs
     - :meth:`~wxc_sdk.telephony.voiceportal.VoicePortalApi.read`
   * - api.telephony.voiceportal.update
        Update VoicePortal
     - :meth:`~wxc_sdk.telephony.voiceportal.VoicePortalApi.update`
   * - api.webhook.create
        Creates a webhook
     - :meth:`~wxc_sdk.webhook.WebhookApi.create`
   * - api.webhook.details
        Get Webhook Details
     - :meth:`~wxc_sdk.webhook.WebhookApi.details`
   * - api.webhook.list
        List all of your webhooks
     - :meth:`~wxc_sdk.webhook.WebhookApi.list`
   * - api.webhook.update
        Updates a webhook, by ID
     - :meth:`~wxc_sdk.webhook.WebhookApi.update`
   * - api.webhook.webhook_delete
        Deletes a webhook, by ID
     - :meth:`~wxc_sdk.webhook.WebhookApi.webhook_delete`
   * - api.workspace_locations.create
        Create a location
     - :meth:`~wxc_sdk.workspace_locations.WorkspaceLocationApi.create`
   * - api.workspace_locations.delete
        Delete a Workspace Location
     - :meth:`~wxc_sdk.workspace_locations.WorkspaceLocationApi.delete`
   * - api.workspace_locations.details
        Get a Workspace Location Details
     - :meth:`~wxc_sdk.workspace_locations.WorkspaceLocationApi.details`
   * - api.workspace_locations.ep
        
     - :meth:`~wxc_sdk.workspace_locations.WorkspaceLocationApi.ep`
   * - api.workspace_locations.list
        List workspace locations
     - :meth:`~wxc_sdk.workspace_locations.WorkspaceLocationApi.list`
   * - api.workspace_locations.update
        Update a Workspace Location
     - :meth:`~wxc_sdk.workspace_locations.WorkspaceLocationApi.update`
   * - api.workspace_locations.floors.create
        Create a Workspace Location Floor
     - :meth:`~wxc_sdk.workspace_locations.WorkspaceLocationFloorApi.create`
   * - api.workspace_locations.floors.delete
        Delete a Workspace Location Floor
     - :meth:`~wxc_sdk.workspace_locations.WorkspaceLocationFloorApi.delete`
   * - api.workspace_locations.floors.details
        Get a Workspace Location Floor Details
     - :meth:`~wxc_sdk.workspace_locations.WorkspaceLocationFloorApi.details`
   * - api.workspace_locations.floors.ep
        
     - :meth:`~wxc_sdk.workspace_locations.WorkspaceLocationFloorApi.ep`
   * - api.workspace_locations.floors.list
        :param location_id:
     - :meth:`~wxc_sdk.workspace_locations.WorkspaceLocationFloorApi.list`
   * - api.workspace_locations.floors.update
        Updates details for a floor, by ID
     - :meth:`~wxc_sdk.workspace_locations.WorkspaceLocationFloorApi.update`
   * - api.workspace_settings.call_intercept.configure
        Configure Call Intercept Settings for a Person
     - :meth:`~wxc_sdk.person_settings.call_intercept.CallInterceptApi.configure`
   * - api.workspace_settings.call_intercept.greeting
        Configure Call Intercept Greeting for a Person
     - :meth:`~wxc_sdk.person_settings.call_intercept.CallInterceptApi.greeting`
   * - api.workspace_settings.call_intercept.read
        Read Call Intercept Settings for a Person
     - :meth:`~wxc_sdk.person_settings.call_intercept.CallInterceptApi.read`
   * - api.workspace_settings.call_waiting.configure
        Configure Call Waiting Settings for a Person
     - :meth:`~wxc_sdk.person_settings.call_waiting.CallWaitingApi.configure`
   * - api.workspace_settings.call_waiting.read
        Read Call Waiting Settings for a Person
     - :meth:`~wxc_sdk.person_settings.call_waiting.CallWaitingApi.read`
   * - api.workspace_settings.caller_id.configure
        Configure a Person's Caller ID Settings
     - :meth:`~wxc_sdk.person_settings.caller_id.CallerIdApi.configure`
   * - api.workspace_settings.caller_id.configure_settings
        
     - :meth:`~wxc_sdk.person_settings.caller_id.CallerIdApi.configure_settings`
   * - api.workspace_settings.caller_id.read
        Retrieve a Person's Caller ID Settings
     - :meth:`~wxc_sdk.person_settings.caller_id.CallerIdApi.read`
   * - api.workspace_settings.forwarding.configure
        Configure a Person's Call Forwarding Settings
     - :meth:`~wxc_sdk.person_settings.forwarding.PersonForwardingApi.configure`
   * - api.workspace_settings.forwarding.read
        Retrieve a Person's Call Forwarding Settings
     - :meth:`~wxc_sdk.person_settings.forwarding.PersonForwardingApi.read`
   * - api.workspace_settings.monitoring.configure
        Configure Call Waiting Settings for a Person
     - :meth:`~wxc_sdk.person_settings.monitoring.MonitoringApi.configure`
   * - api.workspace_settings.monitoring.read
        Retrieve a Person's Monitoring Settings
     - :meth:`~wxc_sdk.person_settings.monitoring.MonitoringApi.read`
   * - api.workspace_settings.numbers.ep
        :meta private:
     - :meth:`~wxc_sdk.workspace_settings.numbers.WorkspaceNumbersApi.ep`
   * - api.workspace_settings.numbers.read
        List the PSTN phone numbers associated with a specific workspace, by ID, within the organization
     - :meth:`~wxc_sdk.workspace_settings.numbers.WorkspaceNumbersApi.read`
   * - api.workspace_settings.permissions_in.configure
        Configure a Person's Barge In Settings
     - :meth:`~wxc_sdk.person_settings.permissions_in.IncomingPermissionsApi.configure`
   * - api.workspace_settings.permissions_in.read
        Read Incoming Permission Settings for a Person
     - :meth:`~wxc_sdk.person_settings.permissions_in.IncomingPermissionsApi.read`
   * - api.workspace_settings.permissions_out.configure
        Configure a Person's Outgoing Calling Permissions Settings
     - :meth:`~wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.configure`
   * - api.workspace_settings.permissions_out.read
        Retrieve a Person's Outgoing Calling Permissions Settings
     - :meth:`~wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.read`
   * - api.workspace_settings.permissions_out.auth_codes.create
        Modify Authorization codes for a workspace
     - :meth:`~wxc_sdk.person_settings.permissions_out.AuthCodesApi.create`
   * - api.workspace_settings.permissions_out.auth_codes.delete_codes
        Modify Authorization codes for a workspace
     - :meth:`~wxc_sdk.person_settings.permissions_out.AuthCodesApi.delete_codes`
   * - api.workspace_settings.permissions_out.auth_codes.read
        Retrieve Authorization codes for a Workspace
     - :meth:`~wxc_sdk.person_settings.permissions_out.AuthCodesApi.read`
   * - api.workspace_settings.permissions_out.transfer_numbers.configure
        Modify Transfer Numbers Settings for a Place
     - :meth:`~wxc_sdk.person_settings.permissions_out.TransferNumbersApi.configure`
   * - api.workspace_settings.permissions_out.transfer_numbers.read
        Retrieve Transfer Numbers Settings for a Workspace
     - :meth:`~wxc_sdk.person_settings.permissions_out.TransferNumbersApi.read`
   * - api.workspaces.create
        Create a Workspace
     - :meth:`~wxc_sdk.workspaces.WorkspacesApi.create`
   * - api.workspaces.delete_workspace
        Delete a Workspace
     - :meth:`~wxc_sdk.workspaces.WorkspacesApi.delete_workspace`
   * - api.workspaces.details
        Get Workspace Details
     - :meth:`~wxc_sdk.workspaces.WorkspacesApi.details`
   * - api.workspaces.list
        List Workspaces
     - :meth:`~wxc_sdk.workspaces.WorkspacesApi.list`
   * - api.workspaces.update
        Update a Workspace
     - :meth:`~wxc_sdk.workspaces.WorkspacesApi.update`
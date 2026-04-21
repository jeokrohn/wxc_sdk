
Reference of all available endpoints
====================================

The following table contains a reference of all SDK methods with their HTTP method, endpoint URL, and a short
description of the operation. The method name is a link to the method documentation.

.. list-table::
   :header-rows: 1

   * - Method
   * - :meth:`api.admin_audit.list_event_categories <wxc_sdk.admin_audit.AdminAuditEventsApi.list_event_categories>`
        | List Admin Audit Event Categories
        | ``GET /adminAudit/eventCategories``
   * - :meth:`api.admin_audit.list_events <wxc_sdk.admin_audit.AdminAuditEventsApi.list_events>`
        | List Admin Audit Events
        | ``GET /adminAudit/events``
   * - :meth:`api.attachment_actions.details <wxc_sdk.attachment_actions.AttachmentActionsApi.details>`
        | Shows details for a attachment action, by ID
        | ``GET /attachment/actions/{action_id}``
   * - :meth:`api.authorizations.delete <wxc_sdk.authorizations.AuthorizationsApi.delete>`
        | Deletes an authorization, by authorization ID or client ID and org ID
        | ``DELETE /authorizations/{authorization_id}``
   * - :meth:`api.authorizations.get_token_expiration_status <wxc_sdk.authorizations.AuthorizationsApi.get_token_expiration_status>`
        | Get expiration status for a token
        | ``GET /authorizations/tokenExpiry``
   * - :meth:`api.authorizations.list <wxc_sdk.authorizations.AuthorizationsApi.list>`
        | Lists all authorizations for a user
        | ``GET /authorizations``
   * - :meth:`api.cdr.get_cdr_history <wxc_sdk.cdr.DetailedCDRApi.get_cdr_history>`
        | Provides Webex Calling Detailed Call History data for your organization
        | ``GET https://analytics-calling.webexapis.com/v1/{cdr_stream|cdr_feed}``
   * - :meth:`api.converged_recordings.delete <wxc_sdk.converged_recordings.ConvergedRecordingsApi.delete>`
        | Delete a Recording
        | ``DELETE /convergedRecordings/{recording_id}``
   * - :meth:`api.converged_recordings.details <wxc_sdk.converged_recordings.ConvergedRecordingsApi.details>`
        | Get Recording Details
        | ``GET /convergedRecordings/{recording_id}``
   * - :meth:`api.converged_recordings.list <wxc_sdk.converged_recordings.ConvergedRecordingsApi.list>`
        | List Recordings
        | ``GET /convergedRecordings``
   * - :meth:`api.converged_recordings.list_for_admin_or_compliance_officer <wxc_sdk.converged_recordings.ConvergedRecordingsApi.list_for_admin_or_compliance_officer>`
        | List Recordings for Admin or Compliance officer
        | ``GET /admin/convergedRecordings``
   * - :meth:`api.converged_recordings.metadata <wxc_sdk.converged_recordings.ConvergedRecordingsApi.metadata>`
        | Get Recording metadata
        | ``GET /convergedRecordings/{recording_id}/metadata``
   * - :meth:`api.converged_recordings.move_recordings_into_the_recycle_bin <wxc_sdk.converged_recordings.ConvergedRecordingsApi.move_recordings_into_the_recycle_bin>`
        | Move Recordings into the Recycle Bin
        | ``POST /convergedRecordings/softDelete``
   * - :meth:`api.converged_recordings.purge_recordings_from_recycle_bin <wxc_sdk.converged_recordings.ConvergedRecordingsApi.purge_recordings_from_recycle_bin>`
        | Purge Recordings from Recycle Bin
        | ``POST /convergedRecordings/purge``
   * - :meth:`api.converged_recordings.reassign <wxc_sdk.converged_recordings.ConvergedRecordingsApi.reassign>`
        | Reassign Recordings
        | ``POST /convergedRecordings/reassign``
   * - :meth:`api.converged_recordings.restore_recordings_from_recycle_bin <wxc_sdk.converged_recordings.ConvergedRecordingsApi.restore_recordings_from_recycle_bin>`
        | Restore Recordings from Recycle Bin
        | ``POST /convergedRecordings/restore``
   * - :meth:`api.device_configurations.list <wxc_sdk.device_configurations.DeviceConfigurationsApi.list>`
        | Lists all device configurations associated with the given device ID
        | ``GET /deviceConfigurations``
   * - :meth:`api.device_configurations.update <wxc_sdk.device_configurations.DeviceConfigurationsApi.update>`
        | Update Device Configurations
        | ``PATCH /deviceConfigurations``
   * - :meth:`api.devices.activation_code <wxc_sdk.devices.DevicesApi.activation_code>`
        | Create a Device Activation Code
        | ``POST /devices/activationCode``
   * - :meth:`api.devices.create_by_mac_address <wxc_sdk.devices.DevicesApi.create_by_mac_address>`
        | Create a phone by it's MAC address in a specific workspace or for a person
        | ``POST /devices``
   * - :meth:`api.devices.delete <wxc_sdk.devices.DevicesApi.delete>`
        | Delete a Device
        | ``DELETE /devices/{device_id}``
   * - :meth:`api.devices.details <wxc_sdk.devices.DevicesApi.details>`
        | Get Device Details
        | ``GET /devices/{device_id}``
   * - :meth:`api.devices.list <wxc_sdk.devices.DevicesApi.list>`
        | List Devices
        | ``GET /devices``
   * - :meth:`api.devices.modify_device_tags <wxc_sdk.devices.DevicesApi.modify_device_tags>`
        | Modify Device Tags
        | ``PATCH /devices/{device_id}``
   * - :meth:`api.devices.settings_jobs.change <wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.change>`
        | Change device settings across organization or locations jobs
        | ``POST /telephony/config/jobs/devices/callDeviceSettings``
   * - :meth:`api.devices.settings_jobs.errors <wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.errors>`
        | List change device settings job errors
        | ``GET /telephony/config/jobs/devices/callDeviceSettings/{job_id}/errors``
   * - :meth:`api.devices.settings_jobs.list <wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.list>`
        | List change device settings jobs
        | ``GET /telephony/config/jobs/devices/callDeviceSettings``
   * - :meth:`api.devices.settings_jobs.status <wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.status>`
        | Get change device settings job status
        | ``GET /telephony/config/jobs/devices/callDeviceSettings/{job_id}``
   * - :meth:`api.events.details <wxc_sdk.events.EventsApi.details>`
        | Shows details for an event, by event ID
        | ``GET /events/{event_id}``
   * - :meth:`api.events.list <wxc_sdk.events.EventsApi.list>`
        | List events in your organization
        | ``GET /events``
   * - :meth:`api.groups.create <wxc_sdk.groups.GroupsApi.create>`
        | Create a new group using the provided settings
        | ``POST /groups``
   * - :meth:`api.groups.delete_group <wxc_sdk.groups.GroupsApi.delete_group>`
        | Delete a group
        | ``DELETE /groups/{group_id}``
   * - :meth:`api.groups.details <wxc_sdk.groups.GroupsApi.details>`
        | Get group details
        | ``GET /groups/{group_id}``
   * - :meth:`api.groups.list <wxc_sdk.groups.GroupsApi.list>`
        | List groups in your organization
        | ``GET /groups``
   * - :meth:`api.groups.members <wxc_sdk.groups.GroupsApi.members>`
        | Query members of a group
        | ``GET /groups/{group_id}/Members``
   * - :meth:`api.groups.update <wxc_sdk.groups.GroupsApi.update>`
        | update group information
        | ``PATCH /groups/{group_id}``
   * - :meth:`api.guests.create <wxc_sdk.guests.GuestManagementApi.create>`
        | Create a Guest
        | ``POST /guests/token``
   * - :meth:`api.guests.guest_count <wxc_sdk.guests.GuestManagementApi.guest_count>`
        | Get Guest Count
        | ``GET /guests/count``
   * - :meth:`api.jobs.activation_emails.errors <wxc_sdk.telephony.jobs.SendActivationEmailApi.errors>`
        | Get Bulk Activation Email Resend Job Errors
        | ``GET /identity/organizations/{org_id}/jobs/sendActivationEmails/{job_id}/errors``
   * - :meth:`api.jobs.activation_emails.start <wxc_sdk.telephony.jobs.SendActivationEmailApi.start>`
        | Initiate Bulk Activation Email Resend Job
        | ``POST /identity/organizations/{org_id}/jobs/sendActivationEmails``
   * - :meth:`api.jobs.activation_emails.status <wxc_sdk.telephony.jobs.SendActivationEmailApi.status>`
        | Get Bulk Activation Email Resend Job Status
        | ``GET /identity/organizations/{org_id}/jobs/sendActivationEmails/{job_id}/status``
   * - :meth:`api.jobs.apply_line_key_templates.apply <wxc_sdk.telephony.jobs.ApplyLineKeyTemplatesJobsApi.apply>`
        | Apply a Line key Template
        | ``POST /telephony/config/jobs/devices/applyLineKeyTemplate``
   * - :meth:`api.jobs.apply_line_key_templates.errors <wxc_sdk.telephony.jobs.ApplyLineKeyTemplatesJobsApi.errors>`
        | Get job errors for an Apply Line Key Template job
        | ``GET /telephony/config/jobs/devices/applyLineKeyTemplate/{job_id}/errors``
   * - :meth:`api.jobs.apply_line_key_templates.list <wxc_sdk.telephony.jobs.ApplyLineKeyTemplatesJobsApi.list>`
        | Get List of Apply Line Key Template jobs
        | ``GET /telephony/config/jobs/devices/applyLineKeyTemplate``
   * - :meth:`api.jobs.apply_line_key_templates.status <wxc_sdk.telephony.jobs.ApplyLineKeyTemplatesJobsApi.status>`
        | Get the job status of an Apply Line Key Template job
        | ``GET /telephony/config/jobs/devices/applyLineKeyTemplate/{job_id}``
   * - :meth:`api.jobs.call_recording.errors <wxc_sdk.telephony.jobs.CallRecordingJobsApi.errors>`
        | Get Job Errors for a Call Recording Job
        | ``GET /telephony/config/jobs/callRecording/{job_id}/errors``
   * - :meth:`api.jobs.call_recording.list <wxc_sdk.telephony.jobs.CallRecordingJobsApi.list>`
        | List Call Recording Jobs
        | ``GET /telephony/config/jobs/callRecording``
   * - :meth:`api.jobs.call_recording.status <wxc_sdk.telephony.jobs.CallRecordingJobsApi.status>`
        | Get the Job Status of a Call Recording Job
        | ``GET /telephony/config/jobs/callRecording/{job_id}``
   * - :meth:`api.jobs.device_settings.change <wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.change>`
        | Change device settings across organization or locations jobs
        | ``POST /telephony/config/jobs/devices/callDeviceSettings``
   * - :meth:`api.jobs.device_settings.errors <wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.errors>`
        | List change device settings job errors
        | ``GET /telephony/config/jobs/devices/callDeviceSettings/{job_id}/errors``
   * - :meth:`api.jobs.device_settings.list <wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.list>`
        | List change device settings jobs
        | ``GET /telephony/config/jobs/devices/callDeviceSettings``
   * - :meth:`api.jobs.device_settings.status <wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.status>`
        | Get change device settings job status
        | ``GET /telephony/config/jobs/devices/callDeviceSettings/{job_id}``
   * - :meth:`api.jobs.disable_calling_location.errors <wxc_sdk.telephony.jobs.DisableCallingLocationJobsApi.errors>`
        | Retrieve Errors for a Disable Calling Location Job
        | ``GET /telephony/config/jobs/locations/deleteCallingLocation/{job_id}/errors``
   * - :meth:`api.jobs.disable_calling_location.initiate <wxc_sdk.telephony.jobs.DisableCallingLocationJobsApi.initiate>`
        | Disable a Location for Webex Calling
        | ``POST /telephony/config/jobs/locations/deleteCallingLocation``
   * - :meth:`api.jobs.disable_calling_location.list <wxc_sdk.telephony.jobs.DisableCallingLocationJobsApi.list>`
        | Get a List of Disable Calling Location Jobs
        | ``GET /telephony/config/jobs/locations/deleteCallingLocation``
   * - :meth:`api.jobs.disable_calling_location.pause <wxc_sdk.telephony.jobs.DisableCallingLocationJobsApi.pause>`
        | Pause a Disable Calling Location Job
        | ``POST /telephony/config/jobs/locations/deleteCallingLocation/{job_id}/actions/pause/invoke``
   * - :meth:`api.jobs.disable_calling_location.resume <wxc_sdk.telephony.jobs.DisableCallingLocationJobsApi.resume>`
        | Resume a Paused Disable Calling Location Job
        | ``POST /telephony/config/jobs/locations/deleteCallingLocation/{job_id}/actions/resume/invoke``
   * - :meth:`api.jobs.disable_calling_location.status <wxc_sdk.telephony.jobs.DisableCallingLocationJobsApi.status>`
        | Get Disable Calling Location Job Status
        | ``GET /telephony/config/jobs/locations/deleteCallingLocation/{job_id}``
   * - :meth:`api.jobs.dynamic_device_settings.errors <wxc_sdk.telephony.jobs.UpdateDynamicDeviceSettingsJobsApi.errors>`
        | List Dynamic Device Settings Job Errors
        | ``GET /telephony/config/jobs/devices/dynamicDeviceSettings/{job_id}/errors``
   * - :meth:`api.jobs.dynamic_device_settings.list <wxc_sdk.telephony.jobs.UpdateDynamicDeviceSettingsJobsApi.list>`
        | List dynamic device settings jobs
        | ``GET /telephony/config/jobs/devices/dynamicDeviceSettings``
   * - :meth:`api.jobs.dynamic_device_settings.status <wxc_sdk.telephony.jobs.UpdateDynamicDeviceSettingsJobsApi.status>`
        | Get Device Dynamic Settings Job Status
        | ``GET /telephony/config/jobs/devices/dynamicDeviceSettings/{job_id}``
   * - :meth:`api.jobs.dynamic_device_settings.update_across_org_or_location <wxc_sdk.telephony.jobs.UpdateDynamicDeviceSettingsJobsApi.update_across_org_or_location>`
        | Updates dynamic Device Settings Across Organization Or Location
        | ``POST /telephony/config/jobs/devices/dynamicDeviceSettings``
   * - :meth:`api.jobs.manage_numbers.abandon <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.abandon>`
        | Abandon the Manage Numbers Job
        | ``POST /telephony/config/jobs/numbers/manageNumbers/{job_id}/actions/abandon/invoke``
   * - :meth:`api.jobs.manage_numbers.errors <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.errors>`
        | List Manage Numbers Job errors
        | ``GET /telephony/config/jobs/numbers/manageNumbers/{job_id}/errors``
   * - :meth:`api.jobs.manage_numbers.initiate_job <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.initiate_job>`
        | Initiate Number Jobs
        | ``POST /telephony/config/jobs/numbers/manageNumbers``
   * - :meth:`api.jobs.manage_numbers.list <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.list>`
        | List Manage Numbers Jobs
        | ``GET /telephony/config/jobs/numbers/manageNumbers``
   * - :meth:`api.jobs.manage_numbers.pause <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.pause>`
        | Pause the Manage Numbers Job
        | ``POST /telephony/config/jobs/numbers/manageNumbers/{job_id}/actions/pause/invoke``
   * - :meth:`api.jobs.manage_numbers.resume <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.resume>`
        | Resume the Manage Numbers Job
        | ``POST /telephony/config/jobs/numbers/manageNumbers/{job_id}/actions/resume/invoke``
   * - :meth:`api.jobs.manage_numbers.status <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.status>`
        | Get Manage Numbers Job Status
        | ``GET /telephony/config/jobs/numbers/manageNumbers/{job_id}``
   * - :meth:`api.jobs.move_users.abandon <wxc_sdk.telephony.jobs.MoveUsersJobsApi.abandon>`
        | Abandon the Move Users Job
        | ``POST /telephony/config/jobs/person/moveLocation/{job_id}/actions/abandon/invoke``
   * - :meth:`api.jobs.move_users.errors <wxc_sdk.telephony.jobs.MoveUsersJobsApi.errors>`
        | List Move Users Job errors
        | ``GET /telephony/config/jobs/person/moveLocation/{job_id}/errors``
   * - :meth:`api.jobs.move_users.list <wxc_sdk.telephony.jobs.MoveUsersJobsApi.list>`
        | List Move Users Jobs
        | ``GET /telephony/config/jobs/person/moveLocation``
   * - :meth:`api.jobs.move_users.pause <wxc_sdk.telephony.jobs.MoveUsersJobsApi.pause>`
        | Pause the Move Users Job
        | ``POST /telephony/config/jobs/person/moveLocation/{job_id}/actions/pause/invoke``
   * - :meth:`api.jobs.move_users.resume <wxc_sdk.telephony.jobs.MoveUsersJobsApi.resume>`
        | Resume the Move Users Job
        | ``POST /telephony/config/jobs/person/moveLocation/{job_id}/actions/resume/invoke``
   * - :meth:`api.jobs.move_users.status <wxc_sdk.telephony.jobs.MoveUsersJobsApi.status>`
        | Get Move Users Job Status
        | ``GET /telephony/config/jobs/person/moveLocation/{job_id}``
   * - :meth:`api.jobs.move_users.validate_or_initiate <wxc_sdk.telephony.jobs.MoveUsersJobsApi.validate_or_initiate>`
        | Validate or Initiate Move Users Job
        | ``POST /telephony/config/jobs/person/moveLocation``
   * - :meth:`api.jobs.rebuild_phones.errors <wxc_sdk.telephony.jobs.RebuildPhonesJobsApi.errors>`
        | Get Job Errors for a Rebuild Phones Job
        | ``GET /telephony/config/jobs/devices/rebuildPhones/{job_id}/errors``
   * - :meth:`api.jobs.rebuild_phones.list <wxc_sdk.telephony.jobs.RebuildPhonesJobsApi.list>`
        | List Rebuild Phones Jobs
        | ``GET /telephony/config/jobs/devices/rebuildPhones``
   * - :meth:`api.jobs.rebuild_phones.rebuild_phones_configuration <wxc_sdk.telephony.jobs.RebuildPhonesJobsApi.rebuild_phones_configuration>`
        | Rebuild Phones Configuration
        | ``POST /telephony/config/jobs/devices/rebuildPhones``
   * - :meth:`api.jobs.rebuild_phones.status <wxc_sdk.telephony.jobs.RebuildPhonesJobsApi.status>`
        | Get the Job Status of a Rebuild Phones Job
        | ``GET /telephony/config/jobs/devices/rebuildPhones/{job_id}``
   * - :meth:`api.jobs.update_routing_prefix.errors <wxc_sdk.telephony.jobs.UpdateRoutingPrefixJobsApi.errors>`
        | Get job errors for update routing prefix job
        | ``GET /telephony/config/jobs/updateRoutingPrefix/{job_id}/errors``
   * - :meth:`api.jobs.update_routing_prefix.list <wxc_sdk.telephony.jobs.UpdateRoutingPrefixJobsApi.list>`
        | Get a List of Update Routing Prefix jobs
        | ``GET /telephony/config/jobs/updateRoutingPrefix``
   * - :meth:`api.jobs.update_routing_prefix.status <wxc_sdk.telephony.jobs.UpdateRoutingPrefixJobsApi.status>`
        | Get the job status of Update Routing Prefix job
        | ``GET /telephony/config/jobs/updateRoutingPrefix/{job_id}``
   * - :meth:`api.licenses.assign_licenses_to_users <wxc_sdk.licenses.LicensesApi.assign_licenses_to_users>`
        | Assign Licenses to Users
        | ``PATCH /licenses/users``
   * - :meth:`api.licenses.assigned_users <wxc_sdk.licenses.LicensesApi.assigned_users>`
        | Get users license is assigned to, by license ID
        | ``GET /licenses/{license_id}``
   * - :meth:`api.licenses.details <wxc_sdk.licenses.LicensesApi.details>`
        | Shows details for a license, by ID
        | ``GET /licenses/{license_id}``
   * - :meth:`api.licenses.list <wxc_sdk.licenses.LicensesApi.list>`
        | List all licenses for a given organization
        | ``GET /licenses``
   * - :meth:`api.locations.create <wxc_sdk.locations.LocationsApi.create>`
        | Create a Location
        | ``POST /locations``
   * - :meth:`api.locations.create_floor <wxc_sdk.locations.LocationsApi.create_floor>`
        | Create a Location Floor
        | ``POST /locations/{location_id}/floors``
   * - :meth:`api.locations.delete <wxc_sdk.locations.LocationsApi.delete>`
        | Delete Location
        | ``DELETE /locations/{location_id}``
   * - :meth:`api.locations.delete_floor <wxc_sdk.locations.LocationsApi.delete_floor>`
        | Delete a Location Floor
        | ``DELETE /locations/{location_id}/floors/{floor_id}``
   * - :meth:`api.locations.details <wxc_sdk.locations.LocationsApi.details>`
        | Get Location Details
        | ``GET /locations/{location_id}``
   * - :meth:`api.locations.floor_details <wxc_sdk.locations.LocationsApi.floor_details>`
        | Get Location Floor Details
        | ``GET /locations/{location_id}/floors/{floor_id}``
   * - :meth:`api.locations.list <wxc_sdk.locations.LocationsApi.list>`
        | List Locations
        | ``GET /locations``
   * - :meth:`api.locations.list_floors <wxc_sdk.locations.LocationsApi.list_floors>`
        | List Location Floors
        | ``GET /locations/{location_id}/floors``
   * - :meth:`api.locations.update <wxc_sdk.locations.LocationsApi.update>`
        | Update details for a location, by ID
        | ``PUT /locations/{location_id}``
   * - :meth:`api.locations.update_floor <wxc_sdk.locations.LocationsApi.update_floor>`
        | Update a Location Floor
        | ``PUT /locations/{location_id}/floors/{id}``
   * - :meth:`api.me.announcement_languages <wxc_sdk.me.MeSettingsApi.announcement_languages>`
        | Retrieve announcement languages for the authenticated user
        | ``GET /telephony/config/people/me/announcementLanguages``
   * - :meth:`api.me.anon_calls.get <wxc_sdk.me.anon_calls.MeAnonCallsApi.get>`
        | Get Anonymous Call Rejection Settings for User
        | ``GET /telephony/config/people/me/settings/anonymousCallReject``
   * - :meth:`api.me.anon_calls.modify <wxc_sdk.me.anon_calls.MeAnonCallsApi.modify>`
        | Modify Anonymous Call Rejection Settings for User
        | ``PUT /telephony/config/people/me/settings/anonymousCallReject``
   * - :meth:`api.me.available_numbers_for_location <wxc_sdk.me.MeSettingsApi.available_numbers_for_location>`
        | Get Available Numbers for User's Location
        | ``GET /telephony/config/people/me/location/assignedNumbers``
   * - :meth:`api.me.barge.configure <wxc_sdk.me.barge.MeBargeApi.configure>`
        | Configure Barge-In Settings
        | ``PUT /telephony/config/people/me/settings/bargeIn``
   * - :meth:`api.me.barge.get <wxc_sdk.me.barge.MeBargeApi.get>`
        | Retrieve Barge-In Settings
        | ``GET /telephony/config/people/me/settings/bargeIn``
   * - :meth:`api.me.call_block.add_number <wxc_sdk.me.callblock.MeCallBlockApi.add_number>`
        | Add a phone number to user's Call Block List
        | ``POST /telephony/config/people/me/settings/callBlock/numbers``
   * - :meth:`api.me.call_block.delete_number <wxc_sdk.me.callblock.MeCallBlockApi.delete_number>`
        | Delete User Call Block Number
        | ``DELETE /telephony/config/people/me/settings/callBlock/numbers/{phone_number_id}``
   * - :meth:`api.me.call_block.settings <wxc_sdk.me.callblock.MeCallBlockApi.settings>`
        | Get My Call Block Settings
        | ``GET /telephony/config/people/me/settings/callBlock``
   * - :meth:`api.me.call_block.state_for_number <wxc_sdk.me.callblock.MeCallBlockApi.state_for_number>`
        | Get My Call Block State For Specific Number
        | ``GET /telephony/config/people/me/settings/callBlock/numbers/{phone_number_id}``
   * - :meth:`api.me.call_captions_settings <wxc_sdk.me.MeSettingsApi.call_captions_settings>`
        | Get my call captions settings
        | ``GET /telephony/config/people/me/settings/callCaptions``
   * - :meth:`api.me.call_center.modify <wxc_sdk.me.callcenter.MeCallCenterApi.modify>`
        | Modify My Call Center Settings
        | ``PUT /telephony/config/people/me/settings/queues``
   * - :meth:`api.me.call_center.settings <wxc_sdk.me.callcenter.MeCallCenterApi.settings>`
        | Get My Call Center Settings
        | ``GET /telephony/config/people/me/settings/queues``
   * - :meth:`api.me.call_notify.criteria_create <wxc_sdk.me.call_notify.MeCallNotifyApi.criteria_create>`
        | Add a Call Notify Criteria
        | ``POST /telephony/config/people/me/settings/callNotify/criteria``
   * - :meth:`api.me.call_notify.criteria_delete <wxc_sdk.me.call_notify.MeCallNotifyApi.criteria_delete>`
        | Delete a Call Notify Criteria
        | ``DELETE /telephony/config/people/me/settings/callNotify/criteria/{criteria_id}``
   * - :meth:`api.me.call_notify.criteria_get <wxc_sdk.me.call_notify.MeCallNotifyApi.criteria_get>`
        | Get Call Notify Criteria Settings
        | ``GET /telephony/config/people/me/settings/callNotify/criteria/{criteria_id}``
   * - :meth:`api.me.call_notify.criteria_update <wxc_sdk.me.call_notify.MeCallNotifyApi.criteria_update>`
        | Modify a Call Notify Criteria
        | ``PUT /telephony/config/people/me/settings/callNotify/criteria/{criteria_id}``
   * - :meth:`api.me.call_notify.get <wxc_sdk.me.call_notify.MeCallNotifyApi.get>`
        | Get Call Notify Settings for User
        | ``GET /telephony/config/people/me/settings/callNotify``
   * - :meth:`api.me.call_notify.update <wxc_sdk.me.call_notify.MeCallNotifyApi.update>`
        | Modify Call Notify Settings for User
        | ``PUT /telephony/config/people/me/settings/callNotify``
   * - :meth:`api.me.call_park.settings <wxc_sdk.me.callpark.MeCallParkApi.settings>`
        | Get My Call Park Settings
        | ``GET /telephony/config/people/me/settings/callPark``
   * - :meth:`api.me.call_pickup.settings <wxc_sdk.me.callpickup.MeCallPickupApi.settings>`
        | Get My Call Pickup Group Settings
        | ``GET /telephony/config/people/me/settings/callPickupGroup``
   * - :meth:`api.me.call_policies.settings <wxc_sdk.me.callpolicy.MeCallPoliciesApi.settings>`
        | Get Call Policies Settings for User
        | ``GET /telephony/config/people/me/settings/callPolicies``
   * - :meth:`api.me.call_policies.update <wxc_sdk.me.callpolicy.MeCallPoliciesApi.update>`
        | Modify Call Policies Settings for User
        | ``PUT /telephony/config/people/me/settings/callPolicies``
   * - :meth:`api.me.call_waiting.get <wxc_sdk.me.call_waiting.MeCallWaitingApi.get>`
        | Get Call Waiting Settings for User
        | ``GET /telephony/config/people/me/settings/callWaiting``
   * - :meth:`api.me.call_waiting.update <wxc_sdk.me.call_waiting.MeCallWaitingApi.update>`
        | Modify Call Waiting Settings for User
        | ``PUT /telephony/config/people/me/settings/callWaiting``
   * - :meth:`api.me.caller_id.available_caller_id_list <wxc_sdk.me.callerid.MeCallerIdApi.available_caller_id_list>`
        | Get My Available Caller ID List
        | ``GET /telephony/config/people/me/settings/availableCallerIds``
   * - :meth:`api.me.caller_id.get_selected_caller_id_settings <wxc_sdk.me.callerid.MeCallerIdApi.get_selected_caller_id_settings>`
        | Read My Selected Caller ID Settings
        | ``GET /telephony/config/people/me/settings/selectedCallerId``
   * - :meth:`api.me.caller_id.modify_selected_caller_id_settings <wxc_sdk.me.callerid.MeCallerIdApi.modify_selected_caller_id_settings>`
        | Configure My Selected Caller ID Settings
        | ``PUT /telephony/config/people/me/settings/selectedCallerId``
   * - :meth:`api.me.caller_id.settings <wxc_sdk.me.callerid.MeCallerIdApi.settings>`
        | Get My Caller ID Settings
        | ``GET /telephony/config/people/me/settings/callerId``
   * - :meth:`api.me.caller_id.update <wxc_sdk.me.callerid.MeCallerIdApi.update>`
        | Modify My Caller ID Settings
        | ``PUT /telephony/config/people/me/settings/callerId``
   * - :meth:`api.me.calling_services_list <wxc_sdk.me.MeSettingsApi.calling_services_list>`
        | Get My Calling Services List
        | ``GET /telephony/config/people/me/settings/services``
   * - :meth:`api.me.contact_center_extensions <wxc_sdk.me.MeSettingsApi.contact_center_extensions>`
        | Read the Contact Center Extensions
        | ``GET /telephony/config/people/me``
   * - :meth:`api.me.country_telephony_config_requirements <wxc_sdk.me.MeSettingsApi.country_telephony_config_requirements>`
        | Retrieve country-specific telephony configuration requirements
        | ``GET /telephony/config/people/me/countries/{country_code}``
   * - :meth:`api.me.details <wxc_sdk.me.MeSettingsApi.details>`
        | Get My Own Details
        | ``GET /telephony/config/people/me``
   * - :meth:`api.me.dnd.configure <wxc_sdk.me.dnd.MeDNDApi.configure>`
        | Update Do Not Disturb Settings for User
        | ``PUT /telephony/config/people/me/settings/doNotDisturb``
   * - :meth:`api.me.dnd.settings <wxc_sdk.me.dnd.MeDNDApi.settings>`
        | Get Do Not Disturb Settings for User
        | ``GET /telephony/config/people/me/settings/doNotDisturb``
   * - :meth:`api.me.endpoints.available_preferred_answer_endpoints <wxc_sdk.me.endpoints.MeEndpointsApi.available_preferred_answer_endpoints>`
        | Get List Available Preferred Answer Endpoints
        | ``GET /telephony/config/people/me/settings/availablePreferredAnswerEndpoints``
   * - :meth:`api.me.endpoints.details <wxc_sdk.me.endpoints.MeEndpointsApi.details>`
        | Get My Endpoints Details
        | ``GET /telephony/config/people/me/endpoints/{endpoint_id}``
   * - :meth:`api.me.endpoints.get_preferred_answer_endpoint <wxc_sdk.me.endpoints.MeEndpointsApi.get_preferred_answer_endpoint>`
        | Get Preferred Answer Endpoint
        | ``GET /telephony/config/people/me/settings/preferredAnswerEndpoint``
   * - :meth:`api.me.endpoints.list <wxc_sdk.me.endpoints.MeEndpointsApi.list>`
        | Read the List of My Endpoints
        | ``GET /telephony/config/people/me/endpoints``
   * - :meth:`api.me.endpoints.modify_preferred_answer_endpoint <wxc_sdk.me.endpoints.MeEndpointsApi.modify_preferred_answer_endpoint>`
        | Modify Preferred Answer Endpoint
        | ``PUT /telephony/config/people/me/settings/preferredAnswerEndpoint``
   * - :meth:`api.me.endpoints.update <wxc_sdk.me.endpoints.MeEndpointsApi.update>`
        | Modify My Endpoints Details
        | ``PUT /telephony/config/people/me/endpoints/{endpoint_id}``
   * - :meth:`api.me.executive.alert_settings <wxc_sdk.me.executive.MeExecutiveApi.alert_settings>`
        | Get User Executive Alert Settings
        | ``GET /telephony/config/people/me/settings/executive/alert``
   * - :meth:`api.me.executive.assigned_assistants <wxc_sdk.me.executive.MeExecutiveApi.assigned_assistants>`
        | Get My Executive Assigned Assistants
        | ``GET /telephony/config/people/me/settings/executive/assignedAssistants``
   * - :meth:`api.me.executive.call_filtering_criteria <wxc_sdk.me.executive.MeExecutiveApi.call_filtering_criteria>`
        | Get User Executive Call Filtering Criteria Settings
        | ``GET /telephony/config/people/me/settings/executive/callFiltering/criteria/{id}``
   * - :meth:`api.me.executive.create_call_filtering_criteria <wxc_sdk.me.executive.MeExecutiveApi.create_call_filtering_criteria>`
        | Add User Executive Call Filtering Criteria
        | ``POST /telephony/config/people/me/settings/executive/callFiltering/criteria``
   * - :meth:`api.me.executive.delete_call_filtering_criteria <wxc_sdk.me.executive.MeExecutiveApi.delete_call_filtering_criteria>`
        | Delete User Executive Call Filtering Criteria
        | ``DELETE /telephony/config/people/me/settings/executive/callFiltering/criteria/{id}``
   * - :meth:`api.me.executive.executive_assistant_settings <wxc_sdk.me.executive.MeExecutiveApi.executive_assistant_settings>`
        | Get My Executive Assistant Settings
        | ``GET /telephony/config/people/me/settings/executive/assistant``
   * - :meth:`api.me.executive.executive_available_assistants <wxc_sdk.me.executive.MeExecutiveApi.executive_available_assistants>`
        | Get My Executive Available Assistants
        | ``GET /telephony/config/people/me/settings/executive/availableAssistants``
   * - :meth:`api.me.executive.executive_call_filtering_settings <wxc_sdk.me.executive.MeExecutiveApi.executive_call_filtering_settings>`
        | Get User Executive Call Filtering Settings
        | ``GET /telephony/config/people/me/settings/executive/callFiltering``
   * - :meth:`api.me.executive.screening_settings <wxc_sdk.me.executive.MeExecutiveApi.screening_settings>`
        | Get User Executive Screening Settings
        | ``GET /telephony/config/people/me/settings/executive/screening``
   * - :meth:`api.me.executive.update_alert_settings <wxc_sdk.me.executive.MeExecutiveApi.update_alert_settings>`
        | Modify User Executive Alert Settings
        | ``PUT /telephony/config/people/me/settings/executive/alert``
   * - :meth:`api.me.executive.update_assigned_assistants <wxc_sdk.me.executive.MeExecutiveApi.update_assigned_assistants>`
        | Modify My Executive Assigned Assistants
        | ``PUT /telephony/config/people/me/settings/executive/assignedAssistants``
   * - :meth:`api.me.executive.update_call_filtering_criteria <wxc_sdk.me.executive.MeExecutiveApi.update_call_filtering_criteria>`
        | Update User Executive Call Filtering Criteria Settings
        | ``PUT /telephony/config/people/me/settings/executive/callFiltering/criteria/{id}``
   * - :meth:`api.me.executive.update_executive_assistant_settings <wxc_sdk.me.executive.MeExecutiveApi.update_executive_assistant_settings>`
        | Modify My Executive Assistant Settings
        | ``PUT /telephony/config/people/me/settings/executive/assistant``
   * - :meth:`api.me.executive.update_executive_call_filtering_settings <wxc_sdk.me.executive.MeExecutiveApi.update_executive_call_filtering_settings>`
        | Update User Executive Call Filtering Settings
        | ``PUT /telephony/config/people/me/settings/executive/callFiltering``
   * - :meth:`api.me.executive.update_screening_settings <wxc_sdk.me.executive.MeExecutiveApi.update_screening_settings>`
        | Modify User Executive Screening Settings
        | ``PUT /telephony/config/people/me/settings/executive/screening``
   * - :meth:`api.me.feature_access_codes <wxc_sdk.me.MeSettingsApi.feature_access_codes>`
        | Get My Feature Access Codes
        | ``GET /telephony/config/people/me/settings/featureAccessCode``
   * - :meth:`api.me.forwarding.configure <wxc_sdk.me.forwarding.MeForwardingApi.configure>`
        | Configure My Call Forwarding Settings
        | ``PUT /telephony/config/people/me/settings/callForwarding``
   * - :meth:`api.me.forwarding.settings <wxc_sdk.me.forwarding.MeForwardingApi.settings>`
        | Read My Call Forwarding Settings
        | ``GET /telephony/config/people/me/settings/callForwarding``
   * - :meth:`api.me.go_override.get <wxc_sdk.me.go_override.GoOverrideApi.get>`
        | Get My WebexGoOverride Settings
        | ``GET /telephony/config/people/me/settings/webexGoOverride``
   * - :meth:`api.me.go_override.update <wxc_sdk.me.go_override.GoOverrideApi.update>`
        | Modify My WebexGoOverride Settings
        | ``PUT /telephony/config/people/me/settings/webexGoOverride``
   * - :meth:`api.me.guest_calling_numbers <wxc_sdk.me.MeSettingsApi.guest_calling_numbers>`
        | Retrieve My Guest Calling Numbers
        | ``GET /telephony/config/people/me/settings/guestCalling/numbers``
   * - :meth:`api.me.mode_management.extend_mode <wxc_sdk.me.mode_management.MeModeManagementApi.extend_mode>`
        | Extend Current Operating Mode Duration
        | ``POST /telephony/config/people/me/settings/modeManagement/features/{feature_id}/actions/extendMode/invoke``
   * - :meth:`api.me.mode_management.feature_get <wxc_sdk.me.mode_management.MeModeManagementApi.feature_get>`
        | Get Mode Management Feature
        | ``GET /telephony/config/people/me/settings/modeManagement/features/{feature_id}``
   * - :meth:`api.me.mode_management.get_common_modes <wxc_sdk.me.mode_management.MeModeManagementApi.get_common_modes>`
        | Get Common Modes
        | ``GET /telephony/config/people/me/settings/modeManagement/features/commonModes``
   * - :meth:`api.me.mode_management.get_features <wxc_sdk.me.mode_management.MeModeManagementApi.get_features>`
        | Get Mode Management Features
        | ``GET /telephony/config/people/me/settings/modeManagement/features``
   * - :meth:`api.me.mode_management.get_normal_operation_mode <wxc_sdk.me.mode_management.MeModeManagementApi.get_normal_operation_mode>`
        | Get Normal Operation Mode
        | ``GET /telephony/config/people/me/settings/modeManagement/features/{feature_id}/normalOperationMode``
   * - :meth:`api.me.mode_management.get_operating_mode <wxc_sdk.me.mode_management.MeModeManagementApi.get_operating_mode>`
        | Get Operating Mode
        | ``GET /telephony/config/people/me/settings/modeManagement/features/{feature_id}/modes/{mode_id}``
   * - :meth:`api.me.mode_management.switch_mode_for_feature <wxc_sdk.me.mode_management.MeModeManagementApi.switch_mode_for_feature>`
        | Switch Mode for Single Feature
        | ``POST /telephony/config/people/me/settings/modeManagement/features/{feature_id}/actions/switchMode/invoke``
   * - :meth:`api.me.mode_management.switch_mode_multiple_features <wxc_sdk.me.mode_management.MeModeManagementApi.switch_mode_multiple_features>`
        | Switch Mode for Multiple Features
        | ``POST /telephony/config/people/me/settings/modeManagement/features/actions/switchMode/invoke``
   * - :meth:`api.me.mode_management.switch_to_normal_operation <wxc_sdk.me.mode_management.MeModeManagementApi.switch_to_normal_operation>`
        | Switch to Normal Operation
        | ``POST /telephony/config/people/me/settings/modeManagement/features/{feature_id}/actions/switchToNormalOperation/invoke``
   * - :meth:`api.me.monitoring_settings <wxc_sdk.me.MeSettingsApi.monitoring_settings>`
        | Get My Monitoring Settings
        | ``GET /telephony/config/people/me/settings/monitoring``
   * - :meth:`api.me.personal_assistant.get <wxc_sdk.me.personal_assistant.MePersonalAssistantApi.get>`
        | Get My Personal Assistant
        | ``GET /telephony/config/people/me/settings/personalAssistant``
   * - :meth:`api.me.personal_assistant.update <wxc_sdk.me.personal_assistant.MePersonalAssistantApi.update>`
        | Modify My Personal Assistant
        | ``PUT /telephony/config/people/me/settings/personalAssistant``
   * - :meth:`api.me.priority_alert.criteria_create <wxc_sdk.me.priority_alert.MePriorityAlertApi.criteria_create>`
        | Add a Priority Alert Criteria
        | ``POST /telephony/config/people/me/settings/priorityAlert/criteria``
   * - :meth:`api.me.priority_alert.criteria_delete <wxc_sdk.me.priority_alert.MePriorityAlertApi.criteria_delete>`
        | Delete a Priority Alert Criteria
        | ``DELETE /telephony/config/people/me/settings/priorityAlert/criteria/{criteria_id}``
   * - :meth:`api.me.priority_alert.criteria_get <wxc_sdk.me.priority_alert.MePriorityAlertApi.criteria_get>`
        | Get Priority Alert Criteria Settings
        | ``GET /telephony/config/people/me/settings/priorityAlert/criteria/{criteria_id}``
   * - :meth:`api.me.priority_alert.criteria_update <wxc_sdk.me.priority_alert.MePriorityAlertApi.criteria_update>`
        | Modify Settings for a Priority Alert Criteria
        | ``PUT /telephony/config/people/me/settings/priorityAlert/criteria/{criteria_id}``
   * - :meth:`api.me.priority_alert.get <wxc_sdk.me.priority_alert.MePriorityAlertApi.get>`
        | Get Priority Alert Settings
        | ``GET /telephony/config/people/me/settings/priorityAlert``
   * - :meth:`api.me.priority_alert.update <wxc_sdk.me.priority_alert.MePriorityAlertApi.update>`
        | Modify Priority Alert Settings for User
        | ``PUT /telephony/config/people/me/settings/priorityAlert``
   * - :meth:`api.me.recording.settings <wxc_sdk.me.recording.MeRecordingApi.settings>`
        | Get My Call Recording Settings
        | ``GET /telephony/config/people/me/settings/callRecording``
   * - :meth:`api.me.schedules.create <wxc_sdk.me.schedules.MeSchedulesApi.create>`
        | Add a User level Schedule for Call Settings
        | ``POST /telephony/config/people/me/schedules``
   * - :meth:`api.me.schedules.delete <wxc_sdk.me.schedules.MeSchedulesApi.delete>`
        | Delete a User Schedule
        | ``DELETE /telephony/config/people/me/schedules/{schedule_type}/{schedule_id}``
   * - :meth:`api.me.schedules.event_create <wxc_sdk.me.schedules.MeSchedulesApi.event_create>`
        | Add an event for a User Schedule
        | ``POST /telephony/config/people/me/schedules/{schedule_type}/{schedule_id}/events``
   * - :meth:`api.me.schedules.event_delete <wxc_sdk.me.schedules.MeSchedulesApi.event_delete>`
        | Delete User a Schedule Event
        | ``DELETE /telephony/config/people/me/schedules/{schedule_type}/{schedule_id}/events/{event_id}``
   * - :meth:`api.me.schedules.event_get <wxc_sdk.me.schedules.MeSchedulesApi.event_get>`
        | Get User Schedule Event
        | ``GET /telephony/config/people/me/schedules/{schedule_type}/{schedule_id}/events/{event_id}``
   * - :meth:`api.me.schedules.event_update <wxc_sdk.me.schedules.MeSchedulesApi.event_update>`
        | Modify User Schedule Event
        | ``PUT /telephony/config/people/me/schedules/{schedule_type}/{schedule_id}/events/{event_id}``
   * - :meth:`api.me.schedules.get_location_schedule <wxc_sdk.me.schedules.MeSchedulesApi.get_location_schedule>`
        | Get User's Location Level Schedule
        | ``GET /telephony/config/people/me/locations/schedules/{schedule_type}/{schedule_id}``
   * - :meth:`api.me.schedules.get_user_schedule <wxc_sdk.me.schedules.MeSchedulesApi.get_user_schedule>`
        | Get User Schedule
        | ``GET /telephony/config/people/me/schedules/{schedule_type}/{schedule_id}``
   * - :meth:`api.me.schedules.list <wxc_sdk.me.schedules.MeSchedulesApi.list>`
        | Get User (and Location) Schedules
        | ``GET /telephony/config/people/me/schedules``
   * - :meth:`api.me.schedules.update <wxc_sdk.me.schedules.MeSchedulesApi.update>`
        | Modify User Schedule
        | ``PUT /telephony/config/people/me/schedules/{schedule_type}/{schedule_id}``
   * - :meth:`api.me.selective_accept.criteria_create <wxc_sdk.me.selective_accept.MeSelectiveAcceptApi.criteria_create>`
        | Add User Selective Call Accept Criteria
        | ``POST /telephony/config/people/me/settings/selectiveAccept/criteria``
   * - :meth:`api.me.selective_accept.criteria_delete <wxc_sdk.me.selective_accept.MeSelectiveAcceptApi.criteria_delete>`
        | Delete a Selective Call Accept Criteria
        | ``DELETE /telephony/config/people/me/settings/selectiveAccept/criteria/{criteria_id}``
   * - :meth:`api.me.selective_accept.criteria_get <wxc_sdk.me.selective_accept.MeSelectiveAcceptApi.criteria_get>`
        | Get Selective Call Accept Criteria Settings for User
        | ``GET /telephony/config/people/me/settings/selectiveAccept/criteria/{criteria_id}``
   * - :meth:`api.me.selective_accept.criteria_update <wxc_sdk.me.selective_accept.MeSelectiveAcceptApi.criteria_update>`
        | Modify a Selective Call Accept Criteria
        | ``PUT /telephony/config/people/me/settings/selectiveAccept/criteria/{criteria_id}``
   * - :meth:`api.me.selective_accept.get <wxc_sdk.me.selective_accept.MeSelectiveAcceptApi.get>`
        | Get Selective Call Accept Settings for User
        | ``GET /telephony/config/people/me/settings/selectiveAccept``
   * - :meth:`api.me.selective_accept.update <wxc_sdk.me.selective_accept.MeSelectiveAcceptApi.update>`
        | Modify Selective Call Accept Settings for User
        | ``PUT /telephony/config/people/me/settings/selectiveAccept``
   * - :meth:`api.me.selective_forward.criteria_create <wxc_sdk.me.selective_forward.MeSelectiveForwardApi.criteria_create>`
        | Add a Selective Call Forwarding Criteria
        | ``POST /telephony/config/people/me/settings/selectiveForward/criteria``
   * - :meth:`api.me.selective_forward.criteria_delete <wxc_sdk.me.selective_forward.MeSelectiveForwardApi.criteria_delete>`
        | Delete a Selective Call Forwarding Criteria
        | ``DELETE /telephony/config/people/me/settings/selectiveForward/criteria/{criteria_id}``
   * - :meth:`api.me.selective_forward.criteria_get <wxc_sdk.me.selective_forward.MeSelectiveForwardApi.criteria_get>`
        | Get Settings for a Selective Call Forwarding Criteria
        | ``GET /telephony/config/people/me/settings/selectiveForward/criteria/{criteria_id}``
   * - :meth:`api.me.selective_forward.criteria_update <wxc_sdk.me.selective_forward.MeSelectiveForwardApi.criteria_update>`
        | Modify Settings for a Selective Call Forwarding Criteria
        | ``PUT /telephony/config/people/me/settings/selectiveForward/criteria/{criteria_id}``
   * - :meth:`api.me.selective_forward.get <wxc_sdk.me.selective_forward.MeSelectiveForwardApi.get>`
        | Get Selective Call Forward Settings for User
        | ``GET /telephony/config/people/me/settings/selectiveForward``
   * - :meth:`api.me.selective_forward.update <wxc_sdk.me.selective_forward.MeSelectiveForwardApi.update>`
        | Modify Selective Call Forward Settings for User
        | ``PUT /telephony/config/people/me/settings/selectiveForward``
   * - :meth:`api.me.selective_reject.criteria_create <wxc_sdk.me.selective_reject.MeSelectiveRejectApi.criteria_create>`
        | Add User Selective Call Reject Criteria
        | ``POST /telephony/config/people/me/settings/selectiveReject/criteria``
   * - :meth:`api.me.selective_reject.criteria_delete <wxc_sdk.me.selective_reject.MeSelectiveRejectApi.criteria_delete>`
        | Delete a Selective Call Reject Criteria
        | ``DELETE /telephony/config/people/me/settings/selectiveReject/criteria/{criteria_id}``
   * - :meth:`api.me.selective_reject.criteria_get <wxc_sdk.me.selective_reject.MeSelectiveRejectApi.criteria_get>`
        | Get Selective Call Reject Criteria Settings for User
        | ``GET /telephony/config/people/me/settings/selectiveReject/criteria/{criteria_id}``
   * - :meth:`api.me.selective_reject.criteria_update <wxc_sdk.me.selective_reject.MeSelectiveRejectApi.criteria_update>`
        | Modify a Selective Call Reject Criteria
        | ``PUT /telephony/config/people/me/settings/selectiveReject/criteria/{criteria_id}``
   * - :meth:`api.me.selective_reject.get <wxc_sdk.me.selective_reject.MeSelectiveRejectApi.get>`
        | Get Selective Call Reject Settings for User
        | ``GET /telephony/config/people/me/settings/selectiveReject``
   * - :meth:`api.me.selective_reject.update <wxc_sdk.me.selective_reject.MeSelectiveRejectApi.update>`
        | Modify Selective Call Reject Settings for User
        | ``PUT /telephony/config/people/me/settings/selectiveReject``
   * - :meth:`api.me.sequential_ring.criteria_create <wxc_sdk.me.sequential_ring.MeSequentialRingApi.criteria_create>`
        | Add User Sequential Ring Criteria
        | ``POST /telephony/config/people/me/settings/sequentialRing/criteria``
   * - :meth:`api.me.sequential_ring.criteria_delete <wxc_sdk.me.sequential_ring.MeSequentialRingApi.criteria_delete>`
        | Delete Sequential Ring Criteria
        | ``DELETE /telephony/config/people/me/settings/sequentialRing/criteria/{criteria_id}``
   * - :meth:`api.me.sequential_ring.criteria_get <wxc_sdk.me.sequential_ring.MeSequentialRingApi.criteria_get>`
        | Get Sequential Ring Criteria Settings for User
        | ``GET /telephony/config/people/me/settings/sequentialRing/criteria/{criteria_id}``
   * - :meth:`api.me.sequential_ring.criteria_update <wxc_sdk.me.sequential_ring.MeSequentialRingApi.criteria_update>`
        | Modify Sequential Ring Criteria Settings for User
        | ``PUT /telephony/config/people/me/settings/sequentialRing/criteria/{criteria_id}``
   * - :meth:`api.me.sequential_ring.get <wxc_sdk.me.sequential_ring.MeSequentialRingApi.get>`
        | Get Sequential Ring Settings for User
        | ``GET /telephony/config/people/me/settings/sequentialRing``
   * - :meth:`api.me.sequential_ring.update <wxc_sdk.me.sequential_ring.MeSequentialRingApi.update>`
        | Modify Sequential Ring Settings for User
        | ``PUT /telephony/config/people/me/settings/sequentialRing``
   * - :meth:`api.me.sim_ring.criteria_create <wxc_sdk.me.sim_ring.MeSimRingApi.criteria_create>`
        | Create My Simultaneous Ring Criteria
        | ``POST /telephony/config/people/me/settings/simultaneousRing/criteria``
   * - :meth:`api.me.sim_ring.criteria_delete <wxc_sdk.me.sim_ring.MeSimRingApi.criteria_delete>`
        | Delete My Simultaneous Ring Criteria
        | ``DELETE /telephony/config/people/me/settings/simultaneousRing/criteria/{criteria_id}``
   * - :meth:`api.me.sim_ring.criteria_get <wxc_sdk.me.sim_ring.MeSimRingApi.criteria_get>`
        | Retrieve My Simultaneous Ring Criteria
        | ``GET /telephony/config/people/me/settings/simultaneousRing/criteria/{criteria_id}``
   * - :meth:`api.me.sim_ring.criteria_update <wxc_sdk.me.sim_ring.MeSimRingApi.criteria_update>`
        | Modify My Simultaneous Ring Criteria
        | ``PUT /telephony/config/people/me/settings/simultaneousRing/criteria/{criteria_id}``
   * - :meth:`api.me.sim_ring.get <wxc_sdk.me.sim_ring.MeSimRingApi.get>`
        | Retrieve My Simultaneous Ring Settings
        | ``GET /telephony/config/people/me/settings/simultaneousRing``
   * - :meth:`api.me.sim_ring.update <wxc_sdk.me.sim_ring.MeSimRingApi.update>`
        | Modify My Simultaneous Ring Settings
        | ``PUT /telephony/config/people/me/settings/simultaneousRing``
   * - :meth:`api.me.snr.create_snr <wxc_sdk.me.snr.MeSNRApi.create_snr>`
        | Add phone number as User's Single Number Reach
        | ``POST /telephony/config/people/me/settings/singleNumberReach/numbers``
   * - :meth:`api.me.snr.delete_snr <wxc_sdk.me.snr.MeSNRApi.delete_snr>`
        | Delete User's Single Number Reach Contact Settings
        | ``DELETE /telephony/config/people/me/settings/singleNumberReach/numbers/{phone_number_id}``
   * - :meth:`api.me.snr.settings <wxc_sdk.me.snr.MeSNRApi.settings>`
        | Get User's Single Number Reach Settings
        | ``GET /telephony/config/people/me/settings/singleNumberReach``
   * - :meth:`api.me.snr.update <wxc_sdk.me.snr.MeSNRApi.update>`
        | Update User's Single Number Reach Settings
        | ``PUT /telephony/config/people/me/settings/singleNumberReach``
   * - :meth:`api.me.snr.update_snr <wxc_sdk.me.snr.MeSNRApi.update_snr>`
        | Modify User's Single Number Reach Contact Settings
        | ``PUT /telephony/config/people/me/settings/singleNumberReach/numbers/{phone_number_id}``
   * - :meth:`api.me.voicemail.configure <wxc_sdk.me.voicemail.MeVoicemailApi.configure>`
        | Configure Voicemail Settings for a Person
        | ``PUT /telephony/config/people/me/settings/voicemail``
   * - :meth:`api.me.voicemail.settings <wxc_sdk.me.voicemail.MeVoicemailApi.settings>`
        | Read Voicemail Settings for a Person
        | ``GET /telephony/config/people/me/settings/voicemail``
   * - :meth:`api.meetings.chats.delete <wxc_sdk.meetings.chats.MeetingChatsApi.delete>`
        | Deletes the meeting chats of a finished meeting instance specified by meetingId
        | ``DELETE /meetings/postMeetingChats``
   * - :meth:`api.meetings.chats.list <wxc_sdk.meetings.chats.MeetingChatsApi.list>`
        | Lists the meeting chats of a finished meeting instance specified by meetingId
        | ``GET /meetings/postMeetingChats``
   * - :meth:`api.meetings.closed_captions.download_snippets <wxc_sdk.meetings.closed_captions.MeetingClosedCaptionsApi.download_snippets>`
        | Download meeting closed caption snippets from the meeting closed caption specified by closedCaptionId formatted
        | ``GET /meetingClosedCaptions/{closed_caption_id}/download``
   * - :meth:`api.meetings.closed_captions.list <wxc_sdk.meetings.closed_captions.MeetingClosedCaptionsApi.list>`
        | Lists closed captions of a finished meeting instance specified by meetingId
        | ``GET /meetingClosedCaptions``
   * - :meth:`api.meetings.closed_captions.list_snippets <wxc_sdk.meetings.closed_captions.MeetingClosedCaptionsApi.list_snippets>`
        | Lists snippets of a meeting closed caption specified by closedCaptionId
        | ``GET /meetingClosedCaptions/{closed_caption_id}/snippets``
   * - :meth:`api.meetings.create <wxc_sdk.meetings.MeetingsApi.create>`
        | Creates a new meeting
        | ``POST /meetings``
   * - :meth:`api.meetings.delete <wxc_sdk.meetings.MeetingsApi.delete>`
        | Deletes a meeting with a specified meeting ID
        | ``DELETE /meetings/{meeting_id}``
   * - :meth:`api.meetings.get <wxc_sdk.meetings.MeetingsApi.get>`
        | Retrieves details for a meeting with a specified meeting ID
        | ``GET /meetings/{meeting_id}``
   * - :meth:`api.meetings.invitees.create_invitee <wxc_sdk.meetings.invitees.MeetingInviteesApi.create_invitee>`
        | Invite a person to attend a meeting
        | ``POST /meetingInvitees``
   * - :meth:`api.meetings.invitees.create_invitees <wxc_sdk.meetings.invitees.MeetingInviteesApi.create_invitees>`
        | Invite people to attend a meeting in bulk
        | ``POST /meetingInvitees/bulkInsert``
   * - :meth:`api.meetings.invitees.delete <wxc_sdk.meetings.invitees.MeetingInviteesApi.delete>`
        | Removes a meeting invitee identified by a meetingInviteeId specified in the URI
        | ``DELETE /meetingInvitees/{meeting_invitee_id}``
   * - :meth:`api.meetings.invitees.invitee_details <wxc_sdk.meetings.invitees.MeetingInviteesApi.invitee_details>`
        | Retrieve details for a meeting invitee identified by a meetingInviteeId in the URI
        | ``GET /meetingInvitees/{meeting_invitee_id}``
   * - :meth:`api.meetings.invitees.list <wxc_sdk.meetings.invitees.MeetingInviteesApi.list>`
        | Lists meeting invitees for a meeting with a specified meetingId
        | ``GET /meetingInvitees``
   * - :meth:`api.meetings.invitees.update <wxc_sdk.meetings.invitees.MeetingInviteesApi.update>`
        | Update details for a meeting invitee identified by a meetingInviteeId in the URI
        | ``PUT /meetingInvitees/{meeting_invitee_id}``
   * - :meth:`api.meetings.join <wxc_sdk.meetings.MeetingsApi.join>`
        | Retrieves a meeting join link for a meeting with a specified meetingId, meetingNumber, or webLink that allows
        | ``POST /meetings/join``
   * - :meth:`api.meetings.list <wxc_sdk.meetings.MeetingsApi.list>`
        | Retrieves details for meetings with a specified meeting number, web link, meeting type, etc
        | ``GET /meetings``
   * - :meth:`api.meetings.list_of_series <wxc_sdk.meetings.MeetingsApi.list_of_series>`
        | Lists scheduled meeting and meeting instances of a meeting series identified by meetingSeriesId
        | ``GET /meetings``
   * - :meth:`api.meetings.list_survey_results <wxc_sdk.meetings.MeetingsApi.list_survey_results>`
        | Retrieves results for a meeting survey identified by meetingId
        | ``GET /meetings/{meeting_id}/surveyResults``
   * - :meth:`api.meetings.list_tracking_codes <wxc_sdk.meetings.MeetingsApi.list_tracking_codes>`
        | Lists tracking codes on a site by a meeting host
        | ``GET /meetings/trackingCodes``
   * - :meth:`api.meetings.participants.admit_participants <wxc_sdk.meetings.participants.MeetingParticipantsApi.admit_participants>`
        | To admit participants into a live meeting in bulk
        | ``POST /meetingParticipants/admit``
   * - :meth:`api.meetings.participants.list_participants <wxc_sdk.meetings.participants.MeetingParticipantsApi.list_participants>`
        | List all participants in a live or post meeting
        | ``GET /meetingParticipants``
   * - :meth:`api.meetings.participants.participant_details <wxc_sdk.meetings.participants.MeetingParticipantsApi.participant_details>`
        | Get a meeting participant details of a live or post meeting
        | ``GET /meetingParticipants/{participant_id}``
   * - :meth:`api.meetings.participants.query_participants_with_email <wxc_sdk.meetings.participants.MeetingParticipantsApi.query_participants_with_email>`
        | Query participants in a live meeting, or after the meeting, using participant's email
        | ``POST /meetingParticipants/query``
   * - :meth:`api.meetings.participants.update_participant <wxc_sdk.meetings.participants.MeetingParticipantsApi.update_participant>`
        | To mute, un-mute, expel, or admit a participant in a live meeting
        | ``PUT /meetingParticipants/{participant_id}``
   * - :meth:`api.meetings.patch <wxc_sdk.meetings.MeetingsApi.patch>`
        | Updates details for a meeting with a specified meeting ID
        | ``PATCH /meetings/{meeting_id}``
   * - :meth:`api.meetings.preferences.audio_options <wxc_sdk.meetings.preferences.MeetingPreferencesApi.audio_options>`
        | Retrieves audio options for the authenticated user
        | ``GET /meetingPreferences/audio``
   * - :meth:`api.meetings.preferences.details <wxc_sdk.meetings.preferences.MeetingPreferencesApi.details>`
        | Retrieves meeting preferences for the authenticated user
        | ``GET /meetingPreferences``
   * - :meth:`api.meetings.preferences.personal_meeting_room_options <wxc_sdk.meetings.preferences.MeetingPreferencesApi.personal_meeting_room_options>`
        | Retrieves the Personal Meeting Room options for the authenticated user
        | ``GET /meetingPreferences/personalMeetingRoom``
   * - :meth:`api.meetings.preferences.scheduling_options <wxc_sdk.meetings.preferences.MeetingPreferencesApi.scheduling_options>`
        | Retrieves scheduling options for the authenticated user
        | ``GET /meetingPreferences/schedulingOptions``
   * - :meth:`api.meetings.preferences.site_list <wxc_sdk.meetings.preferences.MeetingPreferencesApi.site_list>`
        | Retrieves the list of Webex sites that the authenticated user is set up to use
        | ``GET /meetingPreferences/sites``
   * - :meth:`api.meetings.preferences.update_audio_options <wxc_sdk.meetings.preferences.MeetingPreferencesApi.update_audio_options>`
        | Updates audio options for the authenticated user
        | ``PUT /meetingPreferences/audio``
   * - :meth:`api.meetings.preferences.update_default_site <wxc_sdk.meetings.preferences.MeetingPreferencesApi.update_default_site>`
        | Updates the default site for the authenticated user
        | ``PUT /meetingPreferences/sites``
   * - :meth:`api.meetings.preferences.update_personal_meeting_room_options <wxc_sdk.meetings.preferences.MeetingPreferencesApi.update_personal_meeting_room_options>`
        | Update a single meeting
        | ``PUT /meetingPreferences/personalMeetingRoom``
   * - :meth:`api.meetings.preferences.update_scheduling_options <wxc_sdk.meetings.preferences.MeetingPreferencesApi.update_scheduling_options>`
        | Updates scheduling options for the authenticated user
        | ``PUT /meetingPreferences/schedulingOptions``
   * - :meth:`api.meetings.preferences.update_video_options <wxc_sdk.meetings.preferences.MeetingPreferencesApi.update_video_options>`
        | Updates video options for the authenticated user
        | ``PUT /meetingPreferences/video``
   * - :meth:`api.meetings.preferences.video_options <wxc_sdk.meetings.preferences.MeetingPreferencesApi.video_options>`
        | Retrieves video options for the authenticated user
        | ``GET /meetingPreferences/video``
   * - :meth:`api.meetings.qanda.list <wxc_sdk.meetings.qanda.MeetingQandAApi.list>`
        | Lists questions and answers from a meeting, when ready
        | ``GET /meetings/q_and_a``
   * - :meth:`api.meetings.qanda.list_answers <wxc_sdk.meetings.qanda.MeetingQandAApi.list_answers>`
        | Lists the answers to a specific question asked in a meeting
        | ``GET /meetings/q_and_a/{question_id}/answers``
   * - :meth:`api.meetings.qualities.meeting_qualities <wxc_sdk.meetings.qualities.MeetingQualitiesApi.meeting_qualities>`
        | Get quality data for a meeting, by meetingId
        | ``GET https://analytics.webexapis.com/v1/meeting/qualities``
   * - :meth:`api.meetings.recordings.delete_a_recording <wxc_sdk.meetings.recordings.RecordingsApi.delete_a_recording>`
        | Delete a Recording
        | ``DELETE /recordings/{recording_id}``
   * - :meth:`api.meetings.recordings.get_recording_details <wxc_sdk.meetings.recordings.RecordingsApi.get_recording_details>`
        | Get Recording Details
        | ``GET /recordings/{recording_id}``
   * - :meth:`api.meetings.recordings.list_recordings <wxc_sdk.meetings.recordings.RecordingsApi.list_recordings>`
        | List Recordings
        | ``GET /recordings``
   * - :meth:`api.meetings.recordings.list_recordings_for_an_admin_or_compliance_officer <wxc_sdk.meetings.recordings.RecordingsApi.list_recordings_for_an_admin_or_compliance_officer>`
        | List Recordings For an Admin or Compliance Officer
        | ``GET /admin/recordings``
   * - :meth:`api.meetings.recordings.move_recordings_into_the_recycle_bin <wxc_sdk.meetings.recordings.RecordingsApi.move_recordings_into_the_recycle_bin>`
        | Move Recordings into the Recycle Bin
        | ``POST /recordings/softDelete``
   * - :meth:`api.meetings.recordings.purge_recordings_from_recycle_bin <wxc_sdk.meetings.recordings.RecordingsApi.purge_recordings_from_recycle_bin>`
        | Purge Recordings from Recycle Bin
        | ``POST /recordings/purge``
   * - :meth:`api.meetings.recordings.restore_recordings_from_recycle_bin <wxc_sdk.meetings.recordings.RecordingsApi.restore_recordings_from_recycle_bin>`
        | Restore Recordings from Recycle Bin
        | ``POST /recordings/restore``
   * - :meth:`api.meetings.survey <wxc_sdk.meetings.MeetingsApi.survey>`
        | Retrieves details for a meeting survey identified by meetingId
        | ``GET /meetings/{meeting_id}/survey``
   * - :meth:`api.meetings.transcripts.delete <wxc_sdk.meetings.transcripts.MeetingTranscriptsApi.delete>`
        | Removes a transcript with a specified transcript ID
        | ``DELETE /meetingTranscripts/{transcript_id}``
   * - :meth:`api.meetings.transcripts.download <wxc_sdk.meetings.transcripts.MeetingTranscriptsApi.download>`
        | Download a meeting transcript from the meeting transcript specified by transcriptId
        | ``GET /meetingTranscripts/{transcript_id}/download``
   * - :meth:`api.meetings.transcripts.list <wxc_sdk.meetings.transcripts.MeetingTranscriptsApi.list>`
        | Lists available transcripts of an ended meeting instance
        | ``GET /meetingTranscripts``
   * - :meth:`api.meetings.transcripts.list_compliance_officer <wxc_sdk.meetings.transcripts.MeetingTranscriptsApi.list_compliance_officer>`
        | Lists available or deleted transcripts of an ended meeting instance for a specific site
        | ``GET /admin/meetingTranscripts``
   * - :meth:`api.meetings.transcripts.list_snippets <wxc_sdk.meetings.transcripts.MeetingTranscriptsApi.list_snippets>`
        | Lists snippets of a meeting transcript specified by transcriptId
        | ``GET /meetingTranscripts/{transcript_id}/snippets``
   * - :meth:`api.meetings.transcripts.snippet_detail <wxc_sdk.meetings.transcripts.MeetingTranscriptsApi.snippet_detail>`
        | Retrieves details for a transcript snippet specified by snippetId from the meeting transcript specified by
        | ``GET /meetingTranscripts/{transcript_id}/snippets/{snippet_id}``
   * - :meth:`api.meetings.transcripts.update_snippet <wxc_sdk.meetings.transcripts.MeetingTranscriptsApi.update_snippet>`
        | Updates details for a transcript snippet specified by snippetId from the meeting transcript specified by
        | ``PUT /meetingTranscripts/{transcript_id}/snippets/{snippet_id}``
   * - :meth:`api.meetings.update <wxc_sdk.meetings.MeetingsApi.update>`
        | Updates details for a meeting with a specified meeting ID
        | ``PUT /meetings/{meeting_id}``
   * - :meth:`api.meetings.update_simultaneous_interpretation <wxc_sdk.meetings.MeetingsApi.update_simultaneous_interpretation>`
        | Updates simultaneous interpretation options of a meeting with a specified meeting ID
        | ``PUT /meetings/{meeting_id}/simultaneousInterpretation``
   * - :meth:`api.membership.create <wxc_sdk.memberships.MembershipApi.create>`
        | Add someone to a room by Person ID or email address, optionally making them a moderator
        | ``POST /memberships``
   * - :meth:`api.membership.delete <wxc_sdk.memberships.MembershipApi.delete>`
        | Deletes a membership by ID
        | ``DELETE /memberships/{membership_id}``
   * - :meth:`api.membership.details <wxc_sdk.memberships.MembershipApi.details>`
        | Get details for a membership by ID
        | ``GET /memberships/{membership_id}``
   * - :meth:`api.membership.list <wxc_sdk.memberships.MembershipApi.list>`
        | Lists all room memberships
        | ``GET /memberships``
   * - :meth:`api.membership.update <wxc_sdk.memberships.MembershipApi.update>`
        | Updates properties for a membership by ID
        | ``PUT /memberships/{id}``
   * - :meth:`api.messages.create <wxc_sdk.messages.MessagesApi.create>`
        | Post a plain text, rich text or html message, and optionally, a file attachment, to a room
        | ``POST /messages``
   * - :meth:`api.messages.delete <wxc_sdk.messages.MessagesApi.delete>`
        | Delete a message, by message ID
        | ``DELETE /messages/{message_id}``
   * - :meth:`api.messages.details <wxc_sdk.messages.MessagesApi.details>`
        | Show details for a message, by message ID
        | ``GET /messages/{message_id}``
   * - :meth:`api.messages.edit <wxc_sdk.messages.MessagesApi.edit>`
        | Update a message you have posted not more than 10 times
        | ``PUT /messages/{id}``
   * - :meth:`api.messages.list <wxc_sdk.messages.MessagesApi.list>`
        | Lists all messages in a room
        | ``GET /messages``
   * - :meth:`api.messages.list_direct <wxc_sdk.messages.MessagesApi.list_direct>`
        | List all messages in a 1:1 (direct) room
        | ``GET /messages/direct``
   * - :meth:`api.org_contacts.bulk_create_or_update <wxc_sdk.org_contacts.OrganizationContactsApi.bulk_create_or_update>`
        | Bulk Create or Update Contacts
        | ``POST /contacts/organizations/{org_id}/contacts/bulk``
   * - :meth:`api.org_contacts.bulk_delete <wxc_sdk.org_contacts.OrganizationContactsApi.bulk_delete>`
        | Bulk Delete Contacts
        | ``POST /contacts/organizations/{org_id}/contacts/bulk/delete``
   * - :meth:`api.org_contacts.create <wxc_sdk.org_contacts.OrganizationContactsApi.create>`
        | Create a Contact
        | ``POST /contacts/organizations/{org_id}/contacts``
   * - :meth:`api.org_contacts.delete <wxc_sdk.org_contacts.OrganizationContactsApi.delete>`
        | Delete a Contact
        | ``DELETE /contacts/organizations/{org_id}/contacts/{contact_id}``
   * - :meth:`api.org_contacts.get <wxc_sdk.org_contacts.OrganizationContactsApi.get>`
        | Get a Contact
        | ``GET /contacts/organizations/{org_id}/contacts/{contact_id}``
   * - :meth:`api.org_contacts.list <wxc_sdk.org_contacts.OrganizationContactsApi.list>`
        | List Contacts
        | ``GET /contacts/organizations/{org_id}/contacts/search``
   * - :meth:`api.org_contacts.update <wxc_sdk.org_contacts.OrganizationContactsApi.update>`
        | Update a Contact
        | ``PATCH /contacts/organizations/{org_id}/contacts/{contact_id}``
   * - :meth:`api.organizations.delete <wxc_sdk.organizations.OrganizationApi.delete>`
        | Delete Organization
        | ``DELETE /organizations/{org_id}``
   * - :meth:`api.organizations.details <wxc_sdk.organizations.OrganizationApi.details>`
        | Get Organization Details
        | ``GET /organizations/{org_id}``
   * - :meth:`api.organizations.list <wxc_sdk.organizations.OrganizationApi.list>`
        | List all organizations visible by your account
        | ``GET /organizations``
   * - :meth:`api.people.create <wxc_sdk.people.PeopleApi.create>`
        | Create a Person
        | ``POST /people``
   * - :meth:`api.people.delete_person <wxc_sdk.people.PeopleApi.delete_person>`
        | Delete a Person
        | ``DELETE /people/{person_id}``
   * - :meth:`api.people.details <wxc_sdk.people.PeopleApi.details>`
        | Get Person Details
        | ``GET /people/{person_id}``
   * - :meth:`api.people.list <wxc_sdk.people.PeopleApi.list>`
        | List people in your organization
        | ``GET /people``
   * - :meth:`api.people.me <wxc_sdk.people.PeopleApi.me>`
        | Show the profile for the authenticated user
        | ``GET /people/me``
   * - :meth:`api.people.update <wxc_sdk.people.PeopleApi.update>`
        | Update a Person
        | ``PUT /people/{person_id}``
   * - :meth:`api.person_settings.agent_caller_id.available_caller_ids <wxc_sdk.person_settings.agent_caller_id.AgentCallerIdApi.available_caller_ids>`
        | Retrieve Agent's List of Available Caller IDs
        | ``GET /telephony/config/people/{entity_id}/agent/availableCallerIds``
   * - :meth:`api.person_settings.agent_caller_id.configure <wxc_sdk.person_settings.agent_caller_id.AgentCallerIdApi.configure>`
        | Modify Agent's Caller ID Information
        | ``PUT /telephony/config/people/{entity_id}/agent/callerId``
   * - :meth:`api.person_settings.agent_caller_id.read <wxc_sdk.person_settings.agent_caller_id.AgentCallerIdApi.read>`
        | Retrieve Agent's Caller ID Information
        | ``GET /telephony/config/people/{entity_id}/agent/callerId``
   * - :meth:`api.person_settings.app_shared_line.get_members <wxc_sdk.person_settings.app_shared_line.AppSharedLineApi.get_members>`
        | Get Shared-Line Appearance Members
        | ``GET /telephony/config/people/{person_id}/applications/members``
   * - :meth:`api.person_settings.app_shared_line.members_count <wxc_sdk.person_settings.app_shared_line.AppSharedLineApi.members_count>`
        | Get Count of Shared-Line Appearance Members
        | ``GET /telephony/config/people/{person_id}/applications/availableMembers/count``
   * - :meth:`api.person_settings.app_shared_line.search_members <wxc_sdk.person_settings.app_shared_line.AppSharedLineApi.search_members>`
        | Search Shared-Line Appearance Members
        | ``GET /telephony/config/people/{person_id}/applications/availableMembers``
   * - :meth:`api.person_settings.app_shared_line.update_members <wxc_sdk.person_settings.app_shared_line.AppSharedLineApi.update_members>`
        | Put Shared-Line Appearance Members New
        | ``PUT /telephony/config/people/{person_id}/applications/members``
   * - :meth:`api.person_settings.appservices.configure <wxc_sdk.person_settings.appservices.AppServicesApi.configure>`
        | Modify a person's Application Services Settings
        | ``PUT /people/{person_id}/features/applications``
   * - :meth:`api.person_settings.appservices.read <wxc_sdk.person_settings.appservices.AppServicesApi.read>`
        | Retrieve a person's Application Services Settings New
        | ``GET /people/{person_id}/features/applications``
   * - :meth:`api.person_settings.appservices.shared_line.get_members <wxc_sdk.person_settings.app_shared_line.AppSharedLineApi.get_members>`
        | Get Shared-Line Appearance Members
        | ``GET /telephony/config/people/{person_id}/applications/members``
   * - :meth:`api.person_settings.appservices.shared_line.members_count <wxc_sdk.person_settings.app_shared_line.AppSharedLineApi.members_count>`
        | Get Count of Shared-Line Appearance Members
        | ``GET /telephony/config/people/{person_id}/applications/availableMembers/count``
   * - :meth:`api.person_settings.appservices.shared_line.search_members <wxc_sdk.person_settings.app_shared_line.AppSharedLineApi.search_members>`
        | Search Shared-Line Appearance Members
        | ``GET /telephony/config/people/{person_id}/applications/availableMembers``
   * - :meth:`api.person_settings.appservices.shared_line.update_members <wxc_sdk.person_settings.app_shared_line.AppSharedLineApi.update_members>`
        | Put Shared-Line Appearance Members New
        | ``PUT /telephony/config/people/{person_id}/applications/members``
   * - :meth:`api.person_settings.available_numbers.available <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.available>`
        | Get Available Phone Numbers
        | ``GET /``
   * - :meth:`api.person_settings.available_numbers.call_forward <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.call_forward>`
        | Get Call Forward Available Phone Numbers
        | ``GET /telephony/config/people/{entity_id}/callForwarding/availableNumbers``
   * - :meth:`api.person_settings.available_numbers.call_intercept <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.call_intercept>`
        | Get Call Intercept Available Phone Numbers
        | ``GET /telephony/config/people/{entity_id}/callIntercept/availableNumbers``
   * - :meth:`api.person_settings.available_numbers.ecbn <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.ecbn>`
        | Get ECBN Available Phone Numbers
        | ``GET /telephony/config/people/{entity_id}/emergencyCallbackNumber/availableNumbers``
   * - :meth:`api.person_settings.available_numbers.fax_message <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.fax_message>`
        | Get Fax Message Available Phone Numbers
        | ``GET /telephony/config/people/{entity_id}/faxMessage/availableNumbers``
   * - :meth:`api.person_settings.available_numbers.primary <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.primary>`
        | Get Person Primary Available Phone Numbers
        | ``GET /telephony/config/people/primary/availableNumbers``
   * - :meth:`api.person_settings.available_numbers.secondary <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.secondary>`
        | Get Person Secondary Available Phone Numbers
        | ``GET /telephony/config/people/{entity_id}/secondary/availableNumbers``
   * - :meth:`api.person_settings.barge.configure <wxc_sdk.person_settings.barge.BargeApi.configure>`
        | Configure Barge In Settings
        | ``PUT /people/{entity_id}/features/bargeIn``
   * - :meth:`api.person_settings.barge.read <wxc_sdk.person_settings.barge.BargeApi.read>`
        | Retrieve Barge In Settings
        | ``GET /people/{entity_id}/features/bargeIn``
   * - :meth:`api.person_settings.call_bridge.configure <wxc_sdk.person_settings.callbridge.CallBridgeApi.configure>`
        | Configure Call Bridge Settings
        | ``PUT /telephony/config/people/{entity_id}/features/callBridge``
   * - :meth:`api.person_settings.call_bridge.read <wxc_sdk.person_settings.callbridge.CallBridgeApi.read>`
        | Read Call Bridge Settings
        | ``GET /telephony/config/people/{entity_id}/features/callBridge``
   * - :meth:`api.person_settings.call_intercept.configure <wxc_sdk.person_settings.call_intercept.CallInterceptApi.configure>`
        | Configure Call Intercept Settings
        | ``PUT /people/{entity_id}/features/intercept``
   * - :meth:`api.person_settings.call_intercept.greeting <wxc_sdk.person_settings.call_intercept.CallInterceptApi.greeting>`
        | Configure Call Intercept Greeting
        | ``POST /people/{entity_id}/features/intercept/actions/announcementUpload/invoke``
   * - :meth:`api.person_settings.call_intercept.read <wxc_sdk.person_settings.call_intercept.CallInterceptApi.read>`
        | Read Call Intercept Settings
        | ``GET /people/{entity_id}/features/intercept``
   * - :meth:`api.person_settings.call_recording.configure <wxc_sdk.person_settings.call_recording.CallRecordingApi.configure>`
        | Configure Call Recording Settings for a entity
        | ``PUT /people/{entity_id}/features/callRecording``
   * - :meth:`api.person_settings.call_recording.read <wxc_sdk.person_settings.call_recording.CallRecordingApi.read>`
        | Read Call Recording Settings
        | ``GET /people/{entity_id}/features/callRecording``
   * - :meth:`api.person_settings.call_waiting.configure <wxc_sdk.person_settings.call_waiting.CallWaitingApi.configure>`
        | Configure Call Waiting Settings
        | ``PUT /people/{entity_id}/features/callWaiting``
   * - :meth:`api.person_settings.call_waiting.read <wxc_sdk.person_settings.call_waiting.CallWaitingApi.read>`
        | Read Call Waiting Settings for
        | ``GET /people/{entity_id}/features/callWaiting``
   * - :meth:`api.person_settings.caller_id.configure <wxc_sdk.person_settings.caller_id.CallerIdApi.configure>`
        | Configure a Caller ID Settings
        | ``PUT /people/{entity_id}/features/callerId``
   * - :meth:`api.person_settings.caller_id.configure_settings <wxc_sdk.person_settings.caller_id.CallerIdApi.configure_settings>`
        | Configure a Caller ID Settings
        | ``PUT /people/{entity_id}/features/callerId``
   * - :meth:`api.person_settings.caller_id.read <wxc_sdk.person_settings.caller_id.CallerIdApi.read>`
        | Retrieve Caller ID Settings
        | ``GET /people/{entity_id}/features/callerId``
   * - :meth:`api.person_settings.calling_behavior.configure <wxc_sdk.person_settings.calling_behavior.CallingBehaviorApi.configure>`
        | Configure a Person's Calling Behavior
        | ``PUT /people/{person_id}/features/callingBehavior``
   * - :meth:`api.person_settings.calling_behavior.read <wxc_sdk.person_settings.calling_behavior.CallingBehaviorApi.read>`
        | Read Person's Calling Behavior
        | ``GET /people/{person_id}/features/callingBehavior``
   * - :meth:`api.person_settings.devices <wxc_sdk.person_settings.PersonSettingsApi.devices>`
        | Get all devices for a person
        | ``GET /telephony/config/people/{person_id}/devices``
   * - :meth:`api.person_settings.dnd.configure <wxc_sdk.person_settings.dnd.DndApi.configure>`
        | Configure Do Not Disturb Settings for an entity
        | ``PUT /people/{entity_id}/features/doNotDisturb``
   * - :meth:`api.person_settings.dnd.read <wxc_sdk.person_settings.dnd.DndApi.read>`
        | Read Do Not Disturb Settings for an entity
        | ``GET /people/{entity_id}/features/doNotDisturb``
   * - :meth:`api.person_settings.ecbn.configure <wxc_sdk.person_settings.ecbn.ECBNApi.configure>`
        | Update an entity's Emergency Callback Number
        | ``PUT /telephony/config/people/{entity_id}/emergencyCallbackNumber``
   * - :meth:`api.person_settings.ecbn.dependencies <wxc_sdk.person_settings.ecbn.ECBNApi.dependencies>`
        | Retrieve an entity's Emergency Callback Number Dependencies
        | ``GET /telephony/config/people/{entity_id}/emergencyCallbackNumber/dependencies``
   * - :meth:`api.person_settings.ecbn.read <wxc_sdk.person_settings.ecbn.ECBNApi.read>`
        | Get an entity's Emergency Callback Number
        | ``GET /telephony/config/people/{entity_id}/emergencyCallbackNumber``
   * - :meth:`api.person_settings.exec_assistant.configure <wxc_sdk.person_settings.exec_assistant.ExecAssistantApi.configure>`
        | Modify Executive Assistant Settings for a Person
        | ``PUT /people/{person_id}/features/executiveAssistant``
   * - :meth:`api.person_settings.exec_assistant.read <wxc_sdk.person_settings.exec_assistant.ExecAssistantApi.read>`
        | Retrieve Executive Assistant Settings for a Person
        | ``GET /people/{person_id}/features/executiveAssistant``
   * - :meth:`api.person_settings.executive.alert_settings <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.alert_settings>`
        | Get Person Executive Alert Settings
        | ``GET /telephony/config/people/{person_id}/executive/alert``
   * - :meth:`api.person_settings.executive.assigned_assistants <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.assigned_assistants>`
        | Get Person Executive Assigned Assistants
        | ``GET /telephony/config/people/{person_id}/executive/assignedAssistants``
   * - :meth:`api.person_settings.executive.create_call_filtering_criteria <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.create_call_filtering_criteria>`
        | Add Person Executive Call Filtering Criteria
        | ``POST /telephony/config/people/{person_id}/executive/callFiltering/criteria``
   * - :meth:`api.person_settings.executive.delete_call_filtering_criteria <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.delete_call_filtering_criteria>`
        | Delete Person Executive Call Filtering Criteria
        | ``DELETE /telephony/config/people/{person_id}/executive/callFiltering/criteria/{id}``
   * - :meth:`api.person_settings.executive.executive_assistant_settings <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.executive_assistant_settings>`
        | Get Person Executive Assistant Settings
        | ``GET /telephony/config/people/{person_id}/executive/assistant``
   * - :meth:`api.person_settings.executive.executive_available_assistants <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.executive_available_assistants>`
        | Get Person Executive Available Assistants
        | ``GET /telephony/config/people/{person_id}/executive/availableAssistants``
   * - :meth:`api.person_settings.executive.executive_call_filtering_settings <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.executive_call_filtering_settings>`
        | Get Person Executive Call Filtering Settings
        | ``GET /telephony/config/people/{person_id}/executive/callFiltering``
   * - :meth:`api.person_settings.executive.get_filtering_criteria <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.get_filtering_criteria>`
        | Get Person Executive Call Filtering Criteria Settings
        | ``GET /telephony/config/people/{person_id}/executive/callFiltering/criteria/{id}``
   * - :meth:`api.person_settings.executive.screening_settings <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.screening_settings>`
        | Get Person Executive Screening Settings
        | ``GET /telephony/config/people/{person_id}/executive/screening``
   * - :meth:`api.person_settings.executive.update_alert_settings <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.update_alert_settings>`
        | Modify Person Executive Alert Settings
        | ``PUT /telephony/config/people/{person_id}/executive/alert``
   * - :meth:`api.person_settings.executive.update_assigned_assistants <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.update_assigned_assistants>`
        | Modify Person Executive Assigned Assistants
        | ``PUT /telephony/config/people/{person_id}/executive/assignedAssistants``
   * - :meth:`api.person_settings.executive.update_call_filtering_criteria <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.update_call_filtering_criteria>`
        | Modify Person Executive Call Filtering Criteria Settings
        | ``PUT /telephony/config/people/{person_id}/executive/callFiltering/criteria/{id}``
   * - :meth:`api.person_settings.executive.update_executive_assistant_settings <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.update_executive_assistant_settings>`
        | Modify Person Executive Assistant Settings
        | ``PUT /telephony/config/people/{person_id}/executive/assistant``
   * - :meth:`api.person_settings.executive.update_executive_call_filtering_settings <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.update_executive_call_filtering_settings>`
        | Modify Person Executive Call Filtering Settings
        | ``PUT /telephony/config/people/{person_id}/executive/callFiltering``
   * - :meth:`api.person_settings.executive.update_screening_settings <wxc_sdk.person_settings.executive.ExecutiveSettingsApi.update_screening_settings>`
        | Modify Person Executive Screening Settings
        | ``PUT /telephony/config/people/{person_id}/executive/screening``
   * - :meth:`api.person_settings.feature_access.read <wxc_sdk.person_settings.feature_access.FeatureAccessApi.read>`
        | Read Feature Access Settings for a Person
        | ``GET /telephony/config/people/{person_id}/settings/permissions``
   * - :meth:`api.person_settings.feature_access.read_default <wxc_sdk.person_settings.feature_access.FeatureAccessApi.read_default>`
        | Read Default Feature Access Settings for Person
        | ``GET /telephony/config/people/settings/permissions``
   * - :meth:`api.person_settings.feature_access.reset <wxc_sdk.person_settings.feature_access.FeatureAccessApi.reset>`
        | Reset a Person’s Feature Access Configuration to the Organization’s Default Settings
        | ``POST /telephony/config/people/{person_id}/settings/permissions/actions/reset/invoke``
   * - :meth:`api.person_settings.feature_access.update <wxc_sdk.person_settings.feature_access.FeatureAccessApi.update>`
        | Update a Person’s Feature Access Configuration
        | ``PUT /telephony/config/people/{person_id}/settings/permissions``
   * - :meth:`api.person_settings.feature_access.update_default <wxc_sdk.person_settings.feature_access.FeatureAccessApi.update_default>`
        | Update Default Person Feature Access Configuration
        | ``PUT /telephony/config/people/settings/permissions``
   * - :meth:`api.person_settings.forwarding.configure <wxc_sdk.person_settings.forwarding.PersonForwardingApi.configure>`
        | Configure an Entity's Call Forwarding Settings
        | ``PUT /people/{entity_id}/features/callForwarding``
   * - :meth:`api.person_settings.forwarding.read <wxc_sdk.person_settings.forwarding.PersonForwardingApi.read>`
        | Retrieve an entity's Call Forwarding Settings
        | ``GET /people/{entity_id}/features/callForwarding``
   * - :meth:`api.person_settings.get_call_captions_settings <wxc_sdk.person_settings.PersonSettingsApi.get_call_captions_settings>`
        | Get the user call captions settings
        | ``GET /telephony/config/people/{person_id}/callCaptions``
   * - :meth:`api.person_settings.hoteling.configure <wxc_sdk.person_settings.hoteling.HotelingApi.configure>`
        | Configure Hoteling Settings for a Person
        | ``PUT /people/{person_id}/features/hoteling``
   * - :meth:`api.person_settings.hoteling.read <wxc_sdk.person_settings.hoteling.HotelingApi.read>`
        | Read Hoteling Settings for a Person
        | ``GET /people/{person_id}/features/hoteling``
   * - :meth:`api.person_settings.mode_management.assign_features <wxc_sdk.person_settings.mode_management.ModeManagementApi.assign_features>`
        | Assign a List of Features to a User for Mode Management
        | ``PUT /telephony/config/people/{person_id}/modeManagement/features``
   * - :meth:`api.person_settings.mode_management.assigned_features <wxc_sdk.person_settings.mode_management.ModeManagementApi.assigned_features>`
        | Retrieve the List of Features Assigned to a User for Mode Management
        | ``GET /telephony/config/people/{person_id}/modeManagement/features``
   * - :meth:`api.person_settings.mode_management.available_features <wxc_sdk.person_settings.mode_management.ModeManagementApi.available_features>`
        | Retrieve the List of Available Features
        | ``GET /telephony/config/people/{person_id}/modeManagement/availableFeatures``
   * - :meth:`api.person_settings.modify_hoteling_settings_primary_devices <wxc_sdk.person_settings.PersonSettingsApi.modify_hoteling_settings_primary_devices>`
        | Modify Hoteling Settings for a Person's Primary Devices
        | ``PUT /telephony/config/people/{person_id}/devices/settings/hoteling``
   * - :meth:`api.person_settings.monitoring.configure <wxc_sdk.person_settings.monitoring.MonitoringApi.configure>`
        | Modify an entity's Monitoring Settings
        | ``PUT /people/{entity_id}/features/monitoring``
   * - :meth:`api.person_settings.monitoring.read <wxc_sdk.person_settings.monitoring.MonitoringApi.read>`
        | Retrieve an entity's Monitoring Settings
        | ``GET /people/{entity_id}/features/monitoring``
   * - :meth:`api.person_settings.ms_teams.configure <wxc_sdk.person_settings.msteams.MSTeamsSettingApi.configure>`
        | Configure a Person's MS Teams Setting
        | ``PUT /telephony/config/people/{person_id}/settings/msTeams``
   * - :meth:`api.person_settings.ms_teams.read <wxc_sdk.person_settings.msteams.MSTeamsSettingApi.read>`
        | Retrieve a Person's MS Teams Settings
        | ``GET /telephony/config/people/{person_id}/settings/msTeams``
   * - :meth:`api.person_settings.music_on_hold.configure <wxc_sdk.person_settings.moh.MusicOnHoldApi.configure>`
        | Configure Music On Hold Settings for a Personvirtual line, or workspace
        | ``PUT /telephony/config/people/{entity_id}/musicOnHold``
   * - :meth:`api.person_settings.music_on_hold.read <wxc_sdk.person_settings.moh.MusicOnHoldApi.read>`
        | Retrieve Music On Hold Settings for a Person, virtual line, or workspace
        | ``GET /telephony/config/people/{entity_id}/musicOnHold``
   * - :meth:`api.person_settings.numbers.read <wxc_sdk.person_settings.numbers.NumbersApi.read>`
        | Get a person's phone numbers including alternate numbers
        | ``GET /people/{person_id}/features/numbers``
   * - :meth:`api.person_settings.numbers.update <wxc_sdk.person_settings.numbers.NumbersApi.update>`
        | Assign or unassign alternate phone numbers to a person
        | ``PUT /telephony/config/people/{person_id}/numbers``
   * - :meth:`api.person_settings.permissions_in.configure <wxc_sdk.person_settings.permissions_in.IncomingPermissionsApi.configure>`
        | Configure incoming permissions settings
        | ``PUT /people/{entity_id}/features/incomingPermission``
   * - :meth:`api.person_settings.permissions_in.read <wxc_sdk.person_settings.permissions_in.IncomingPermissionsApi.read>`
        | Read Incoming Permission Settings
        | ``GET /people/{entity_id}/features/incomingPermission``
   * - :meth:`api.person_settings.permissions_out.access_codes.create <wxc_sdk.person_settings.permissions_out.AccessCodesApi.create>`
        | Create new Access codes
        | ``POST /telephony/config/people/{entity_id}/outgoingPermission/accessCodes``
   * - :meth:`api.person_settings.permissions_out.access_codes.delete <wxc_sdk.person_settings.permissions_out.AccessCodesApi.delete>`
        | Delete Access Code
        | ``DELETE /telephony/config/people/{entity_id}/outgoingPermission/accessCodes``
   * - :meth:`api.person_settings.permissions_out.access_codes.modify <wxc_sdk.person_settings.permissions_out.AccessCodesApi.modify>`
        | Modify Access Codes
        | ``PUT /telephony/config/people/{entity_id}/outgoingPermission/accessCodes``
   * - :meth:`api.person_settings.permissions_out.access_codes.read <wxc_sdk.person_settings.permissions_out.AccessCodesApi.read>`
        | Retrieve Access codes
        | ``GET /telephony/config/people/{entity_id}/outgoingPermission/accessCodes``
   * - :meth:`api.person_settings.permissions_out.configure <wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.configure>`
        | Configure Outgoing Calling Permissions Settings
        | ``PUT /people/{entity_id}/features/outgoingPermission``
   * - :meth:`api.person_settings.permissions_out.digit_patterns.create <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.create>`
        | Create Digit Patterns
        | ``POST /telephony/config/people/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.person_settings.permissions_out.digit_patterns.delete <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.delete>`
        | Delete a Digit Pattern
        | ``DELETE /telephony/config/people/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}``
   * - :meth:`api.person_settings.permissions_out.digit_patterns.delete_all <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.delete_all>`
        | Delete all Digit Patterns
        | ``DELETE /telephony/config/people/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.person_settings.permissions_out.digit_patterns.details <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.details>`
        | Retrieve Digit Pattern Details
        | ``GET /telephony/config/people/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}``
   * - :meth:`api.person_settings.permissions_out.digit_patterns.get_digit_patterns <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.get_digit_patterns>`
        | Retrieve Digit Patterns
        | ``GET /telephony/config/people/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.person_settings.permissions_out.digit_patterns.update <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.update>`
        | Modify Digit Patterns
        | ``PUT /telephony/config/people/{entity_id}/outgoingPermission/digitPatterns/{id}``
   * - :meth:`api.person_settings.permissions_out.digit_patterns.update_category_control_settings <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.update_category_control_settings>`
        | Modify the Digit Pattern Category Control Settings for the entity
        | ``PUT /telephony/config/people/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.person_settings.permissions_out.read <wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.read>`
        | Retrieve Outgoing Calling Permissions Settings
        | ``GET /people/{entity_id}/features/outgoingPermission``
   * - :meth:`api.person_settings.permissions_out.transfer_numbers.configure <wxc_sdk.person_settings.permissions_out.TransferNumbersApi.configure>`
        | Modify Transfer Numbers Settings for an entity
        | ``PUT /people/{entity_id}/features/outgoingPermission/autoTransferNumbers``
   * - :meth:`api.person_settings.permissions_out.transfer_numbers.read <wxc_sdk.person_settings.permissions_out.TransferNumbersApi.read>`
        | Retrieve Transfer Numbers Settings
        | ``GET /people/{entity_id}/features/outgoingPermission/autoTransferNumbers``
   * - :meth:`api.person_settings.personal_assistant.get <wxc_sdk.person_settings.personal_assistant.PersonalAssistantApi.get>`
        | Get Personal Assistant
        | ``GET /telephony/config/people/{person_id}/features/personalAssistant``
   * - :meth:`api.person_settings.personal_assistant.update <wxc_sdk.person_settings.personal_assistant.PersonalAssistantApi.update>`
        | Update Personal Assistant
        | ``PUT /telephony/config/people/{person_id}/features/personalAssistant``
   * - :meth:`api.person_settings.preferred_answer.modify <wxc_sdk.person_settings.preferred_answer.PreferredAnswerApi.modify>`
        | Modify Preferred Answer Endpoint
        | ``PUT /telephony/config/people/{person_id}/preferredAnswerEndpoint``
   * - :meth:`api.person_settings.preferred_answer.read <wxc_sdk.person_settings.preferred_answer.PreferredAnswerApi.read>`
        | Get Preferred Answer Endpoint
        | ``GET /telephony/config/people/{person_id}/preferredAnswerEndpoint``
   * - :meth:`api.person_settings.privacy.configure <wxc_sdk.person_settings.privacy.PrivacyApi.configure>`
        | Configure an entity's Privacy Settings
        | ``PUT /people/{entity_id}/features/privacy``
   * - :meth:`api.person_settings.privacy.read <wxc_sdk.person_settings.privacy.PrivacyApi.read>`
        | Get Privacy Settings for an entity
        | ``GET /people/{entity_id}/features/privacy``
   * - :meth:`api.person_settings.push_to_talk.configure <wxc_sdk.person_settings.push_to_talk.PushToTalkApi.configure>`
        | Configure Push-to-Talk Settings for an entity
        | ``PUT /people/{entity_id}/features/pushToTalk``
   * - :meth:`api.person_settings.push_to_talk.read <wxc_sdk.person_settings.push_to_talk.PushToTalkApi.read>`
        | Read Push-to-Talk Settings for an entity
        | ``GET /people/{entity_id}/features/pushToTalk``
   * - :meth:`api.person_settings.receptionist.configure <wxc_sdk.person_settings.receptionist.ReceptionistApi.configure>`
        | Modify Executive Assistant Settings for a Person
        | ``PUT /people/{person_id}/features/reception``
   * - :meth:`api.person_settings.receptionist.read <wxc_sdk.person_settings.receptionist.ReceptionistApi.read>`
        | Read Receptionist Client Settings for a Person
        | ``GET /people/{person_id}/features/reception``
   * - :meth:`api.person_settings.reset_vm_pin <wxc_sdk.person_settings.PersonSettingsApi.reset_vm_pin>`
        | Reset Voicemail PIN
        | ``POST /people/{person_id}/features/voicemail/actions/resetPin/invoke``
   * - :meth:`api.person_settings.schedules.create <wxc_sdk.common.schedules.ScheduleApi.create>`
        | Create a schedule
        | ``POST /people/{obj_id}/features/schedules``
   * - :meth:`api.person_settings.schedules.delete_schedule <wxc_sdk.common.schedules.ScheduleApi.delete_schedule>`
        | Delete a schedule
        | ``DELETE /people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}``
   * - :meth:`api.person_settings.schedules.details <wxc_sdk.common.schedules.ScheduleApi.details>`
        | Get details for a schedule
        | ``GET /people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}``
   * - :meth:`api.person_settings.schedules.event_create <wxc_sdk.common.schedules.ScheduleApi.event_create>`
        | Create a schedule event
        | ``POST /people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}/events``
   * - :meth:`api.person_settings.schedules.event_delete <wxc_sdk.common.schedules.ScheduleApi.event_delete>`
        | Delete a schedule event
        | ``DELETE /people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}``
   * - :meth:`api.person_settings.schedules.event_details <wxc_sdk.common.schedules.ScheduleApi.event_details>`
        | Get details for a schedule event
        | ``GET /people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}``
   * - :meth:`api.person_settings.schedules.event_update <wxc_sdk.common.schedules.ScheduleApi.event_update>`
        | Update a schedule event
        | ``PUT /people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}``
   * - :meth:`api.person_settings.schedules.list <wxc_sdk.common.schedules.ScheduleApi.list>`
        | List of schedules for a person or location
        | ``GET /people/{obj_id}/features/schedules``
   * - :meth:`api.person_settings.schedules.update <wxc_sdk.common.schedules.ScheduleApi.update>`
        | Update a schedule
        | ``PUT /people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}``
   * - :meth:`api.person_settings.selective_accept.configure <wxc_sdk.person_settings.selective_accept.SelectiveAcceptApi.configure>`
        | Modify Selective Accept Settings for an entity
        | ``PUT /telephony/config/people/{entity_id}/selectiveAccept``
   * - :meth:`api.person_settings.selective_accept.configure_criteria <wxc_sdk.person_settings.selective_accept.SelectiveAcceptApi.configure_criteria>`
        | Modify Selective Accept Criteria for an entity
        | ``PUT /telephony/config/people/{entity_id}/selectiveAccept/criteria/{id}``
   * - :meth:`api.person_settings.selective_accept.create_criteria <wxc_sdk.person_settings.selective_accept.SelectiveAcceptApi.create_criteria>`
        | Create Selective Accept Criteria for an entity
        | ``POST /telephony/config/people/{entity_id}/selectiveAccept/criteria``
   * - :meth:`api.person_settings.selective_accept.delete_criteria <wxc_sdk.person_settings.selective_accept.SelectiveAcceptApi.delete_criteria>`
        | Delete Selective Accept Criteria for an entity
        | ``DELETE /telephony/config/people/{entity_id}/selectiveAccept/criteria/{id}``
   * - :meth:`api.person_settings.selective_accept.read <wxc_sdk.person_settings.selective_accept.SelectiveAcceptApi.read>`
        | Retrieve Selective Accept Settings for an entity
        | ``GET /telephony/config/people/{entity_id}/selectiveAccept``
   * - :meth:`api.person_settings.selective_accept.read_criteria <wxc_sdk.person_settings.selective_accept.SelectiveAcceptApi.read_criteria>`
        | Retrieve Selective Accept Criteria for an entity
        | ``GET /telephony/config/people/{entity_id}/selectiveAccept/criteria/{id}``
   * - :meth:`api.person_settings.selective_forward.configure <wxc_sdk.person_settings.selective_forward.SelectiveForwardApi.configure>`
        | Modify Selective Forward Settings for a Workspace
        | ``PUT /telephony/config/people/{entity_id}/selectiveForward``
   * - :meth:`api.person_settings.selective_forward.configure_criteria <wxc_sdk.person_settings.selective_forward.SelectiveForwardApi.configure_criteria>`
        | Modify Selective Forward Criteria for a Workspace
        | ``PUT /telephony/config/people/{entity_id}/selectiveForward/criteria/{id}``
   * - :meth:`api.person_settings.selective_forward.create_criteria <wxc_sdk.person_settings.selective_forward.SelectiveForwardApi.create_criteria>`
        | Create Selective Forward Criteria for a Workspace
        | ``POST /telephony/config/people/{entity_id}/selectiveForward/criteria``
   * - :meth:`api.person_settings.selective_forward.delete_criteria <wxc_sdk.person_settings.selective_forward.SelectiveForwardApi.delete_criteria>`
        | Delete Selective Forward Criteria for a Workspace
        | ``DELETE /telephony/config/people/{entity_id}/selectiveForward/criteria/{id}``
   * - :meth:`api.person_settings.selective_forward.read <wxc_sdk.person_settings.selective_forward.SelectiveForwardApi.read>`
        | Retrieve Selective Forward Settings for a Workspace
        | ``GET /telephony/config/people/{entity_id}/selectiveForward``
   * - :meth:`api.person_settings.selective_forward.read_criteria <wxc_sdk.person_settings.selective_forward.SelectiveForwardApi.read_criteria>`
        | Retrieve Selective Forward Criteria for a Workspace
        | ``GET /telephony/config/people/{entity_id}/selectiveForward/criteria/{id}``
   * - :meth:`api.person_settings.selective_reject.configure <wxc_sdk.person_settings.selective_reject.SelectiveRejectApi.configure>`
        | Modify Selective Reject Settings for an entity
        | ``PUT /telephony/config/people/{entity_id}/selectiveReject``
   * - :meth:`api.person_settings.selective_reject.configure_criteria <wxc_sdk.person_settings.selective_reject.SelectiveRejectApi.configure_criteria>`
        | Modify Selective Reject Criteria for an entity
        | ``PUT /telephony/config/people/{entity_id}/selectiveReject/criteria/{id}``
   * - :meth:`api.person_settings.selective_reject.create_criteria <wxc_sdk.person_settings.selective_reject.SelectiveRejectApi.create_criteria>`
        | Create Selective Reject Criteria for an entity
        | ``POST /telephony/config/people/{entity_id}/selectiveReject/criteria``
   * - :meth:`api.person_settings.selective_reject.delete_criteria <wxc_sdk.person_settings.selective_reject.SelectiveRejectApi.delete_criteria>`
        | Delete Selective Reject Criteria for an entity
        | ``DELETE /telephony/config/people/{entity_id}/selectiveReject/criteria/{id}``
   * - :meth:`api.person_settings.selective_reject.read <wxc_sdk.person_settings.selective_reject.SelectiveRejectApi.read>`
        | Retrieve Selective Reject Settings for an entity
        | ``GET /telephony/config/people/{entity_id}/selectiveReject``
   * - :meth:`api.person_settings.selective_reject.read_criteria <wxc_sdk.person_settings.selective_reject.SelectiveRejectApi.read_criteria>`
        | Retrieve Selective Reject Criteria for an entity
        | ``GET /telephony/config/people/{entity_id}/selectiveReject/criteria/{id}``
   * - :meth:`api.person_settings.single_number_reach.available_phone_numbers <wxc_sdk.person_settings.single_number_reach.SingleNumberReachApi.available_phone_numbers>`
        | Get Single Number Reach Primary Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/singleNumberReach/availableNumbers``
   * - :meth:`api.person_settings.single_number_reach.create_snr <wxc_sdk.person_settings.single_number_reach.SingleNumberReachApi.create_snr>`
        | Create Single Number Reach For a Person
        | ``POST /telephony/config/people/{person_id}/singleNumberReach/numbers``
   * - :meth:`api.person_settings.single_number_reach.delete_snr <wxc_sdk.person_settings.single_number_reach.SingleNumberReachApi.delete_snr>`
        | Delete A Single Number Reach Number
        | ``DELETE /telephony/config/people/{person_id}/singleNumberReach/numbers/{id}``
   * - :meth:`api.person_settings.single_number_reach.read <wxc_sdk.person_settings.single_number_reach.SingleNumberReachApi.read>`
        | Get Single Number Reach Settings For A Person
        | ``GET /telephony/config/people/{person_id}/singleNumberReach``
   * - :meth:`api.person_settings.single_number_reach.update <wxc_sdk.person_settings.single_number_reach.SingleNumberReachApi.update>`
        | Update Single number reach settings for a person
        | ``PUT /telephony/config/people/{person_id}/singleNumberReach``
   * - :meth:`api.person_settings.single_number_reach.update_snr <wxc_sdk.person_settings.single_number_reach.SingleNumberReachApi.update_snr>`
        | Update Single number reach settings for a number
        | ``PUT /telephony/config/people/{person_id}/singleNumberReach/numbers/{id}``
   * - :meth:`api.person_settings.update_call_captions_settings <wxc_sdk.person_settings.PersonSettingsApi.update_call_captions_settings>`
        | Update the user call captions settings
        | ``PUT /telephony/config/people/{person_id}/callCaptions``
   * - :meth:`api.person_settings.voicemail.configure <wxc_sdk.person_settings.voicemail.VoicemailApi.configure>`
        | Configure Voicemail Settings for an entity
        | ``PUT /people/{entity_id}/features/voicemail``
   * - :meth:`api.person_settings.voicemail.modify_passcode <wxc_sdk.person_settings.voicemail.VoicemailApi.modify_passcode>`
        | Modify an entity's voicemail passcode
        | ``PUT /telephony/config/people/{entity_id}/voicemail/passcode``
   * - :meth:`api.person_settings.voicemail.read <wxc_sdk.person_settings.voicemail.VoicemailApi.read>`
        | Read Voicemail Settings for an entity
        | ``GET /people/{entity_id}/features/voicemail``
   * - :meth:`api.person_settings.voicemail.reset_pin <wxc_sdk.person_settings.voicemail.VoicemailApi.reset_pin>`
        | Reset Voicemail PIN
        | ``POST /people/{entity_id}/features/voicemail/actions/resetPin/invoke``
   * - :meth:`api.reports.create <wxc_sdk.reports.ReportsApi.create>`
        | Create a new report
        | ``POST /reports``
   * - :meth:`api.reports.delete <wxc_sdk.reports.ReportsApi.delete>`
        | Remove a report from the system
        | ``DELETE /reports/{report_id}``
   * - :meth:`api.reports.details <wxc_sdk.reports.ReportsApi.details>`
        | Shows details for a report, by report ID
        | ``GET /reports/{report_id}``
   * - :meth:`api.reports.download <wxc_sdk.reports.ReportsApi.download>`
        | Download a report from the given URL and yield the rows as dicts
        | ``GET {url}``
   * - :meth:`api.reports.list <wxc_sdk.reports.ReportsApi.list>`
        | Lists all reports
        | ``GET /reports``
   * - :meth:`api.reports.list_templates <wxc_sdk.reports.ReportsApi.list_templates>`
        | List all the available report templates that can be generated
        | ``GET /report/templates``
   * - :meth:`api.roles.details <wxc_sdk.roles.RolesApi.details>`
        | Get Role Details
        | ``GET /roles/{role_id}``
   * - :meth:`api.roles.list <wxc_sdk.roles.RolesApi.list>`
        | List Roles
        | ``GET /roles``
   * - :meth:`api.room_tabs.create_tab <wxc_sdk.room_tabs.RoomTabsApi.create_tab>`
        | Add a tab with a specified URL to a room
        | ``POST /room/tabs``
   * - :meth:`api.room_tabs.delete_tab <wxc_sdk.room_tabs.RoomTabsApi.delete_tab>`
        | Deletes a Room Tab with the specified ID
        | ``DELETE /room/tabs/{tab_id}``
   * - :meth:`api.room_tabs.list_tabs <wxc_sdk.room_tabs.RoomTabsApi.list_tabs>`
        | Lists all Room Tabs of a room specified by the roomId query parameter
        | ``GET /room/tabs``
   * - :meth:`api.room_tabs.tab_details <wxc_sdk.room_tabs.RoomTabsApi.tab_details>`
        | Get details for a Room Tab with the specified room tab ID
        | ``GET /room/tabs/{tab_id}``
   * - :meth:`api.room_tabs.update_tab <wxc_sdk.room_tabs.RoomTabsApi.update_tab>`
        | Updates the content URL of the specified Room Tab ID
        | ``PUT /room/tabs/{tab_id}``
   * - :meth:`api.rooms.create <wxc_sdk.rooms.RoomsApi.create>`
        | Creates a room
        | ``POST /rooms``
   * - :meth:`api.rooms.delete <wxc_sdk.rooms.RoomsApi.delete>`
        | Deletes a room, by ID
        | ``DELETE /rooms/{room_id}``
   * - :meth:`api.rooms.details <wxc_sdk.rooms.RoomsApi.details>`
        | Shows details for a room, by ID
        | ``GET /rooms/{room_id}``
   * - :meth:`api.rooms.list <wxc_sdk.rooms.RoomsApi.list>`
        | List rooms
        | ``GET /rooms``
   * - :meth:`api.rooms.meeting_details <wxc_sdk.rooms.RoomsApi.meeting_details>`
        | The meetingInfo API is deprecated and will be EOL on Jan 31, 2025
        | ``GET /rooms/{room_id}/meetingInfo``
   * - :meth:`api.rooms.update <wxc_sdk.rooms.RoomsApi.update>`
        | Updates details for a room, by ID
        | ``PUT /rooms/{id}``
   * - :meth:`api.scim.bulk.bulk_request <wxc_sdk.scim.bulk.SCIM2BulkApi.bulk_request>`
        | User bulk API
        | ``POST https://webexapis.com/identity/scim/{org_id}/v2/Bulk``
   * - :meth:`api.scim.groups.create <wxc_sdk.scim.groups.SCIM2GroupsApi.create>`
        | Create a group
        | ``POST https://webexapis.com/identity/scim/{org_id}/v2/Groups``
   * - :meth:`api.scim.groups.delete <wxc_sdk.scim.groups.SCIM2GroupsApi.delete>`
        | Delete a group
        | ``DELETE https://webexapis.com/identity/scim/{org_id}/v2/Groups/{group_id}``
   * - :meth:`api.scim.groups.details <wxc_sdk.scim.groups.SCIM2GroupsApi.details>`
        | Get a group
        | ``GET https://webexapis.com/identity/scim/{org_id}/v2/Groups/{group_id}``
   * - :meth:`api.scim.groups.members <wxc_sdk.scim.groups.SCIM2GroupsApi.members>`
        | Get Group Members
        | ``GET https://webexapis.com/identity/scim/{org_id}/v2/Groups/{group_id}/Members``
   * - :meth:`api.scim.groups.patch <wxc_sdk.scim.groups.SCIM2GroupsApi.patch>`
        | Update a group with PATCH
        | ``PATCH https://webexapis.com/identity/scim/{org_id}/v2/Groups/{group_id}``
   * - :meth:`api.scim.groups.search <wxc_sdk.scim.groups.SCIM2GroupsApi.search>`
        | Search groups
        | ``GET https://webexapis.com/identity/scim/{org_id}/v2/Groups``
   * - :meth:`api.scim.groups.update <wxc_sdk.scim.groups.SCIM2GroupsApi.update>`
        | Update a group with PUT
        | ``PUT https://webexapis.com/identity/scim/{org_id}/v2/Groups/{id}``
   * - :meth:`api.scim.users.create <wxc_sdk.scim.users.SCIM2UsersApi.create>`
        | Create a user
        | ``POST https://webexapis.com/identity/scim/{org_id}/v2/Users``
   * - :meth:`api.scim.users.delete <wxc_sdk.scim.users.SCIM2UsersApi.delete>`
        | Delete a user
        | ``DELETE https://webexapis.com/identity/scim/{org_id}/v2/Users/{user_id}``
   * - :meth:`api.scim.users.details <wxc_sdk.scim.users.SCIM2UsersApi.details>`
        | Get a user
        | ``GET https://webexapis.com/identity/scim/{org_id}/v2/Users/{user_id}``
   * - :meth:`api.scim.users.patch <wxc_sdk.scim.users.SCIM2UsersApi.patch>`
        | Update a user with PATCH
        | ``PATCH https://webexapis.com/identity/scim/{org_id}/v2/Users/{user_id}``
   * - :meth:`api.scim.users.search <wxc_sdk.scim.users.SCIM2UsersApi.search>`
        | Search users
        | ``GET https://webexapis.com/identity/scim/{org_id}/v2/Users``
   * - :meth:`api.scim.users.update <wxc_sdk.scim.users.SCIM2UsersApi.update>`
        | Update a user with PUT
        | ``PUT https://webexapis.com/identity/scim/{org_id}/v2/Users/{id}``
   * - :meth:`api.status.active_scheduled_maintenances <wxc_sdk.status.StatusAPI.active_scheduled_maintenances>`
        | Get a list of any active maintenances
        | ``GET https://status.webex.com/active-scheduled-maintenances.json``
   * - :meth:`api.status.all_incidents <wxc_sdk.status.StatusAPI.all_incidents>`
        | Get a list of the 50 most recent incidents
        | ``GET https://status.webex.com/all-incidents.json``
   * - :meth:`api.status.all_scheduled_maintenances <wxc_sdk.status.StatusAPI.all_scheduled_maintenances>`
        | Get a list of the 50 most recent scheduled maintenances
        | ``GET https://status.webex.com/all-scheduled-maintenances.json``
   * - :meth:`api.status.components <wxc_sdk.status.StatusAPI.components>`
        | Get the components for the status page
        | ``GET https://status.webex.com/components.json``
   * - :meth:`api.status.status <wxc_sdk.status.StatusAPI.status>`
        | Get the status rollup for the whole page
        | ``GET /status``
   * - :meth:`api.status.summary <wxc_sdk.status.StatusAPI.summary>`
        | Get a summary of the status page, including a status indicator, component statuses, unresolved incidents,
        | ``GET https://status.webex.com/index.json``
   * - :meth:`api.status.unresolved_incidents <wxc_sdk.status.StatusAPI.unresolved_incidents>`
        | Get a list of any unresolved incidents
        | ``GET https://status.webex.com/unresolved-incidents.json``
   * - :meth:`api.status.upcoming_scheduled_maintenances <wxc_sdk.status.StatusAPI.upcoming_scheduled_maintenances>`
        | Scheduled maintenances are planned outages, upgrades, or general notices that you're working on
        | ``GET https://status.webex.com/upcoming-scheduled-maintenances.json``
   * - :meth:`api.team_memberships.create <wxc_sdk.team_memberships.TeamMembershipsApi.create>`
        | Add someone to a team by Person ID or email address, optionally making them a moderator
        | ``POST /team/memberships``
   * - :meth:`api.team_memberships.delete <wxc_sdk.team_memberships.TeamMembershipsApi.delete>`
        | Deletes a team membership, by ID
        | ``DELETE /team/memberships/{membership_id}``
   * - :meth:`api.team_memberships.details <wxc_sdk.team_memberships.TeamMembershipsApi.details>`
        | Shows details for a team membership, by ID
        | ``GET /team/memberships/{membership_id}``
   * - :meth:`api.team_memberships.list <wxc_sdk.team_memberships.TeamMembershipsApi.list>`
        | Lists all team memberships for a given team, specified by the teamId query parameter
        | ``GET /team/memberships``
   * - :meth:`api.team_memberships.membership <wxc_sdk.team_memberships.TeamMembershipsApi.membership>`
        | Updates a team membership, by ID
        | ``PUT /team/memberships/{membership_id}``
   * - :meth:`api.teams.create <wxc_sdk.teams.TeamsApi.create>`
        | Creates a team
        | ``POST /teams``
   * - :meth:`api.teams.delete <wxc_sdk.teams.TeamsApi.delete>`
        | Deletes a team, by ID
        | ``DELETE /teams/{team_id}``
   * - :meth:`api.teams.details <wxc_sdk.teams.TeamsApi.details>`
        | Shows details for a team, by ID
        | ``GET /teams/{team_id}``
   * - :meth:`api.teams.list <wxc_sdk.teams.TeamsApi.list>`
        | Lists teams to which the authenticated user belongs
        | ``GET /teams``
   * - :meth:`api.teams.update <wxc_sdk.teams.TeamsApi.update>`
        | Updates details for a team, by ID
        | ``PUT /teams/{team_id}``
   * - :meth:`api.telephony.access_codes.create <wxc_sdk.telephony.access_codes.LocationAccessCodesApi.create>`
        | Create Outgoing Permission a new access code for a customer location
        | ``POST /telephony/config/locations/{location_id}/outgoingPermission/accessCodes``
   * - :meth:`api.telephony.access_codes.delete_all <wxc_sdk.telephony.access_codes.LocationAccessCodesApi.delete_all>`
        | Delete Outgoing Permission Location Access Codes
        | ``DELETE /telephony/config/locations/{location_id}/outgoingPermission/accessCodes``
   * - :meth:`api.telephony.access_codes.delete_codes <wxc_sdk.telephony.access_codes.LocationAccessCodesApi.delete_codes>`
        | Delete Access Code Location
        | ``PUT /telephony/config/locations/{location_id}/outgoingPermission/accessCodes``
   * - :meth:`api.telephony.access_codes.read <wxc_sdk.telephony.access_codes.LocationAccessCodesApi.read>`
        | Get Outgoing Permission Location Access Code
        | ``GET /telephony/config/locations/{location_id}/outgoingPermission/accessCodes``
   * - :meth:`api.telephony.announcements_repo.delete <wxc_sdk.telephony.announcements_repo.AnnouncementsRepositoryApi.delete>`
        | Delete an announcement greeting
        | ``DELETE /telephony/config/announcements/{announcement_id}``
   * - :meth:`api.telephony.announcements_repo.details <wxc_sdk.telephony.announcements_repo.AnnouncementsRepositoryApi.details>`
        | Fetch details of a binary announcement greeting at the organization or location level
        | ``GET /telephony/config/announcements/{announcement_id}``
   * - :meth:`api.telephony.announcements_repo.list <wxc_sdk.telephony.announcements_repo.AnnouncementsRepositoryApi.list>`
        | Fetch list of announcement greetings on location and organization level
        | ``GET /telephony/config/announcements``
   * - :meth:`api.telephony.announcements_repo.modify <wxc_sdk.telephony.announcements_repo.AnnouncementsRepositoryApi.modify>`
        | Modify a binary announcement greeting at organization or location level
        | ``PUT /telephony/config/announcements/{announcement_id}``
   * - :meth:`api.telephony.announcements_repo.upload_announcement <wxc_sdk.telephony.announcements_repo.AnnouncementsRepositoryApi.upload_announcement>`
        | Upload a binary announcement greeting at organization or location level
        | ``POST /telephony/config/announcements``
   * - :meth:`api.telephony.announcements_repo.usage <wxc_sdk.telephony.announcements_repo.AnnouncementsRepositoryApi.usage>`
        | Fetch repository usage for announcements for an organization or location
        | ``GET /telephony/config/announcements/usage``
   * - :meth:`api.telephony.auto_attendant.alternate_available_phone_numbers <wxc_sdk.telephony.autoattendant.AutoAttendantApi.alternate_available_phone_numbers>`
        | Get Auto Attendant Alternate Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/autoAttendants/alternate/availableNumbers``
   * - :meth:`api.telephony.auto_attendant.call_forward_available_phone_numbers <wxc_sdk.telephony.autoattendant.AutoAttendantApi.call_forward_available_phone_numbers>`
        | Get Auto Attendant Call Forward Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/autoAttendants/callForwarding/availableNumbers``
   * - :meth:`api.telephony.auto_attendant.create <wxc_sdk.telephony.autoattendant.AutoAttendantApi.create>`
        | Create an Auto Attendant
        | ``POST /telephony/config/locations/{location_id}/autoAttendants``
   * - :meth:`api.telephony.auto_attendant.delete_announcement_file <wxc_sdk.telephony.autoattendant.AutoAttendantApi.delete_announcement_file>`
        | Delete an Auto Attendant Announcement File
        | ``DELETE /telephony/config/locations/{location_id}/autoAttendants/{auto_attendant_id}/announcements/{file_name}``
   * - :meth:`api.telephony.auto_attendant.delete_auto_attendant <wxc_sdk.telephony.autoattendant.AutoAttendantApi.delete_auto_attendant>`
        | elete the designated Auto Attendant
        | ``DELETE /telephony/config/locations/{location_id}/autoAttendants/{auto_attendant_id}``
   * - :meth:`api.telephony.auto_attendant.details <wxc_sdk.telephony.autoattendant.AutoAttendantApi.details>`
        | Get Details for an Auto Attendant
        | ``GET /telephony/config/locations/{location_id}/autoAttendants/{auto_attendant_id}``
   * - :meth:`api.telephony.auto_attendant.forwarding.call_forwarding_rule <wxc_sdk.telephony.forwarding.ForwardingApi.call_forwarding_rule>`
        | Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue
        | ``GET /telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding/selectiveRules/{rule_id}``
   * - :meth:`api.telephony.auto_attendant.forwarding.create_call_forwarding_rule <wxc_sdk.telephony.forwarding.ForwardingApi.create_call_forwarding_rule>`
        | Create a Selective Call Forwarding Rule feature
        | ``POST /telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding/selectiveRules``
   * - :meth:`api.telephony.auto_attendant.forwarding.delete_call_forwarding_rule <wxc_sdk.telephony.forwarding.ForwardingApi.delete_call_forwarding_rule>`
        | Delete a Selective Call Forwarding Rule for the designated feature
        | ``DELETE /telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding/selectiveRules/{rule_id}``
   * - :meth:`api.telephony.auto_attendant.forwarding.settings <wxc_sdk.telephony.forwarding.ForwardingApi.settings>`
        | Retrieve Call Forwarding settings for the designated feature including the list of call
        | ``GET /telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding``
   * - :meth:`api.telephony.auto_attendant.forwarding.switch_mode_for_call_forwarding <wxc_sdk.telephony.forwarding.ForwardingApi.switch_mode_for_call_forwarding>`
        | Switch Mode for Call Forwarding Settings for an entity
        | ``POST /telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding/actions/switchMode/invoke``
   * - :meth:`api.telephony.auto_attendant.forwarding.update <wxc_sdk.telephony.forwarding.ForwardingApi.update>`
        | Update Call Forwarding Settings for a feature
        | ``PUT /telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding``
   * - :meth:`api.telephony.auto_attendant.forwarding.update_call_forwarding_rule <wxc_sdk.telephony.forwarding.ForwardingApi.update_call_forwarding_rule>`
        | Update a Selective Call Forwarding Rule's settings for the designated feature
        | ``PUT /telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding/selectiveRules/{rule_id}``
   * - :meth:`api.telephony.auto_attendant.list <wxc_sdk.telephony.autoattendant.AutoAttendantApi.list>`
        | Read the List of Auto Attendants
        | ``GET /telephony/config/autoAttendants``
   * - :meth:`api.telephony.auto_attendant.list_announcement_files <wxc_sdk.telephony.autoattendant.AutoAttendantApi.list_announcement_files>`
        | Read the List of Auto Attendant Announcement Files
        | ``GET /telephony/config/locations/{location_id}/autoAttendants/{auto_attendant_id}/announcements``
   * - :meth:`api.telephony.auto_attendant.primary_available_phone_numbers <wxc_sdk.telephony.autoattendant.AutoAttendantApi.primary_available_phone_numbers>`
        | Get Auto Attendant Primary Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/autoAttendants/availableNumbers``
   * - :meth:`api.telephony.auto_attendant.update <wxc_sdk.telephony.autoattendant.AutoAttendantApi.update>`
        | Update an Auto Attendant
        | ``PUT /telephony/config/locations/{location_id}/autoAttendants/{auto_attendant_id}``
   * - :meth:`api.telephony.call_controls_members.answer <wxc_sdk.telephony.call_contols_members.CallControlsMembersApi.answer>`
        | Answer by Member ID
        | ``POST /telephony/calls/members/{member_id}/answer``
   * - :meth:`api.telephony.call_controls_members.dial <wxc_sdk.telephony.call_contols_members.CallControlsMembersApi.dial>`
        | Dial by Member ID
        | ``POST /telephony/calls/members/{member_id}/dial``
   * - :meth:`api.telephony.call_controls_members.get_call_details <wxc_sdk.telephony.call_contols_members.CallControlsMembersApi.get_call_details>`
        | Get Call Details by Member ID
        | ``GET /telephony/calls/members/{member_id}/calls/{call_id}``
   * - :meth:`api.telephony.call_controls_members.hangup <wxc_sdk.telephony.call_contols_members.CallControlsMembersApi.hangup>`
        | Hangup by Member ID
        | ``POST /telephony/calls/members/{member_id}/hangup``
   * - :meth:`api.telephony.call_controls_members.list_calls <wxc_sdk.telephony.call_contols_members.CallControlsMembersApi.list_calls>`
        | List Calls by Member ID
        | ``GET /telephony/calls/members/{member_id}/calls``
   * - :meth:`api.telephony.call_intercept.configure <wxc_sdk.telephony.location.intercept.LocationInterceptApi.configure>`
        | Put Location Intercept
        | ``PUT /telephony/config/locations/{location_id}/intercept``
   * - :meth:`api.telephony.call_intercept.read <wxc_sdk.telephony.location.intercept.LocationInterceptApi.read>`
        | Get Location Intercept
        | ``GET /telephony/config/locations/{location_id}/intercept``
   * - :meth:`api.telephony.call_recording.get_call_recording_regions <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.get_call_recording_regions>`
        | Get Call Recording Regions
        | ``GET /telephony/config/callRecording/regions``
   * - :meth:`api.telephony.call_recording.get_location_vendors <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.get_location_vendors>`
        | Get Location Call Recording Vendors
        | ``GET /telephony/config/locations/{location_id}/callRecording/vendors``
   * - :meth:`api.telephony.call_recording.get_org_vendors <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.get_org_vendors>`
        | Get Organization Call Recording Vendors
        | ``GET /telephony/config/callRecording/vendors``
   * - :meth:`api.telephony.call_recording.list_location_users <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.list_location_users>`
        | Get Call Recording Vendor Users for a Location
        | ``GET /telephony/config/locations/{location_id}/callRecording/vendorUsers``
   * - :meth:`api.telephony.call_recording.list_org_users <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.list_org_users>`
        | Get Call Recording Vendor Users
        | ``GET /telephony/config/callRecording/vendorUsers``
   * - :meth:`api.telephony.call_recording.read <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.read>`
        | Get Call Recording Settings
        | ``GET /telephony/config/callRecording``
   * - :meth:`api.telephony.call_recording.read_location_compliance_announcement <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.read_location_compliance_announcement>`
        | Get details for the Location Compliance Announcement Setting
        | ``GET /telephony/config/locations/{location_id}/callRecording/complianceAnnouncement``
   * - :meth:`api.telephony.call_recording.read_org_compliance_announcement <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.read_org_compliance_announcement>`
        | Get details for the organization Compliance Announcement Setting
        | ``GET /telephony/config/callRecording/complianceAnnouncement``
   * - :meth:`api.telephony.call_recording.read_terms_of_service <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.read_terms_of_service>`
        | Get Call Recording Terms Of Service Settings
        | ``GET /telephony/config/callRecording/vendors/{vendor_id}/termsOfService``
   * - :meth:`api.telephony.call_recording.set_location_vendor <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.set_location_vendor>`
        | Set Call Recording Vendor for a Location
        | ``PUT /telephony/config/locations/{location_id}/callRecording/vendor``
   * - :meth:`api.telephony.call_recording.set_org_vendor <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.set_org_vendor>`
        | Set Organization Call Recording Vendor
        | ``PUT /telephony/config/callRecording/vendor``
   * - :meth:`api.telephony.call_recording.update <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.update>`
        | Update Call Recording Settings
        | ``PUT /telephony/config/callRecording``
   * - :meth:`api.telephony.call_recording.update_location_compliance_announcement <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.update_location_compliance_announcement>`
        | Update the location compliance announcement
        | ``PUT /telephony/config/locations/{location_id}/callRecording/complianceAnnouncement``
   * - :meth:`api.telephony.call_recording.update_org_compliance_announcement <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.update_org_compliance_announcement>`
        | Update the organization compliance announcement
        | ``PUT /telephony/config/callRecording/complianceAnnouncement``
   * - :meth:`api.telephony.call_recording.update_terms_of_service <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.update_terms_of_service>`
        | Update Call Recording Terms Of Service Settings
        | ``PUT /telephony/config/callRecording/vendors/{vendor_id}/termsOfService``
   * - :meth:`api.telephony.call_routing.tp.create <wxc_sdk.telephony.call_routing.translation_pattern.TranslationPatternsApi.create>`
        | Create a Translation Pattern
        | ``POST /telephony/config/locations/{location_id}/callRouting/translationPatterns``
   * - :meth:`api.telephony.call_routing.tp.delete <wxc_sdk.telephony.call_routing.translation_pattern.TranslationPatternsApi.delete>`
        | Delete a Translation Pattern
        | ``DELETE /telephony/config/locations/{location_id}/callRouting/translationPatterns/{translation_id}``
   * - :meth:`api.telephony.call_routing.tp.details <wxc_sdk.telephony.call_routing.translation_pattern.TranslationPatternsApi.details>`
        | Retrieve the details of a Translation Pattern
        | ``GET /telephony/config/locations/{location_id}/callRouting/translationPatterns/{translation_id}``
   * - :meth:`api.telephony.call_routing.tp.list <wxc_sdk.telephony.call_routing.translation_pattern.TranslationPatternsApi.list>`
        | Retrieve a list of Translation Patterns
        | ``GET /telephony/config/callRouting/translationPatterns``
   * - :meth:`api.telephony.call_routing.tp.update <wxc_sdk.telephony.call_routing.translation_pattern.TranslationPatternsApi.update>`
        | Modify a Translation Pattern
        | ``PUT /telephony/config/locations/{location_id}/callRouting/translationPatterns/{id}``
   * - :meth:`api.telephony.caller_reputation_provider.get <wxc_sdk.telephony.caller_reputation.CallerReputationProviderApi.get>`
        | Get Caller Reputation Provider Service Settings
        | ``GET /telephony/config/serviceSettings/callerReputationProvider``
   * - :meth:`api.telephony.caller_reputation_provider.providers <wxc_sdk.telephony.caller_reputation.CallerReputationProviderApi.providers>`
        | Get Caller Reputation Provider Providers
        | ``GET /telephony/config/serviceSettings/callerReputationProvider/providers``
   * - :meth:`api.telephony.caller_reputation_provider.status <wxc_sdk.telephony.caller_reputation.CallerReputationProviderApi.status>`
        | Get Caller Reputation Provider Status
        | ``GET /telephony/config/serviceSettings/callerReputationProvider/status``
   * - :meth:`api.telephony.caller_reputation_provider.unlock <wxc_sdk.telephony.caller_reputation.CallerReputationProviderApi.unlock>`
        | Unlock Caller Reputation Provider
        | ``POST /telephony/config/serviceSettings/callerReputationProvider/actions/unlock/invoke``
   * - :meth:`api.telephony.caller_reputation_provider.update <wxc_sdk.telephony.caller_reputation.CallerReputationProviderApi.update>`
        | Update Caller Reputation Provider Service Settings
        | ``PUT /telephony/config/serviceSettings/callerReputationProvider``
   * - :meth:`api.telephony.callpark.available_agents <wxc_sdk.telephony.callpark.CallParkApi.available_agents>`
        | Get available agents from Call Parks
        | ``GET /telephony/config/locations/{location_id}/callParks/availableUsers``
   * - :meth:`api.telephony.callpark.available_recalls <wxc_sdk.telephony.callpark.CallParkApi.available_recalls>`
        | Get available recall hunt groups from Call Parks
        | ``GET /telephony/config/locations/{location_id}/callParks/availableRecallHuntGroups``
   * - :meth:`api.telephony.callpark.call_park_settings <wxc_sdk.telephony.callpark.CallParkApi.call_park_settings>`
        | Get Call Park Settings
        | ``GET /telephony/config/locations/{location_id}/callParks/settings``
   * - :meth:`api.telephony.callpark.create <wxc_sdk.telephony.callpark.CallParkApi.create>`
        | Create a Call Park Extension
        | ``POST /telephony/config/locations/{location_id}/callParks``
   * - :meth:`api.telephony.callpark.delete_callpark <wxc_sdk.telephony.callpark.CallParkApi.delete_callpark>`
        | Delete a Call Park
        | ``DELETE /telephony/config/locations/{location_id}/callParks/{callpark_id}``
   * - :meth:`api.telephony.callpark.details <wxc_sdk.telephony.callpark.CallParkApi.details>`
        | Get Details for a Call Park
        | ``GET /telephony/config/locations/{location_id}/callParks/{callpark_id}``
   * - :meth:`api.telephony.callpark.list <wxc_sdk.telephony.callpark.CallParkApi.list>`
        | Read the List of Call Parks
        | ``GET /telephony/config/locations/{location_id}/callParks``
   * - :meth:`api.telephony.callpark.update <wxc_sdk.telephony.callpark.CallParkApi.update>`
        | Update a Call Park
        | ``PUT /telephony/config/locations/{location_id}/callParks/{callpark_id}``
   * - :meth:`api.telephony.callpark.update_call_park_settings <wxc_sdk.telephony.callpark.CallParkApi.update_call_park_settings>`
        | Update Call Park settings
        | ``PUT /telephony/config/locations/{location_id}/callParks/settings``
   * - :meth:`api.telephony.callpark_extension.create <wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.create>`
        | Create a Call Park Extension
        | ``POST /telephony/config/locations/{location_id}/callParkExtensions``
   * - :meth:`api.telephony.callpark_extension.delete <wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.delete>`
        | Delete a Call Park Extension
        | ``DELETE /telephony/config/locations/{location_id}/callParkExtensions/{cpe_id}``
   * - :meth:`api.telephony.callpark_extension.details <wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.details>`
        | Get Details for a Call Park Extension
        | ``GET /telephony/config/locations/{location_id}/callParkExtensions/{cpe_id}``
   * - :meth:`api.telephony.callpark_extension.list <wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.list>`
        | Read the List of Call Park Extensions
        | ``GET /telephony/config/callParkExtensions``
   * - :meth:`api.telephony.callpark_extension.update <wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.update>`
        | Update a Call Park Extension
        | ``PUT /telephony/config/locations/{location_id}/callParkExtensions/{cpe_id}``
   * - :meth:`api.telephony.callqueue.agents.details <wxc_sdk.telephony.callqueue.agents.CallQueueAgentsApi.details>`
        | Get Details for a Call Queue Agent
        | ``GET /telephony/config/queues/agents/{id}``
   * - :meth:`api.telephony.callqueue.agents.list <wxc_sdk.telephony.callqueue.agents.CallQueueAgentsApi.list>`
        | Read the List of Call Queue Agents
        | ``GET /telephony/config/queues/agents``
   * - :meth:`api.telephony.callqueue.agents.update_call_queue_settings <wxc_sdk.telephony.callqueue.agents.CallQueueAgentsApi.update_call_queue_settings>`
        | Update an Agent's Settings of One or More Call Queues
        | ``PUT /telephony/config/queues/agents/{id}/settings``
   * - :meth:`api.telephony.callqueue.alternate_available_phone_numbers <wxc_sdk.telephony.callqueue.CallQueueApi.alternate_available_phone_numbers>`
        | Get Call Queue Alternate Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/queues/alternate/availableNumbers``
   * - :meth:`api.telephony.callqueue.available_agents <wxc_sdk.telephony.callqueue.CallQueueApi.available_agents>`
        | Get Call Queue Available Agents
        | ``GET /telephony/config/queues/agents/availableAgents``
   * - :meth:`api.telephony.callqueue.call_forward_available_phone_numbers <wxc_sdk.telephony.callqueue.CallQueueApi.call_forward_available_phone_numbers>`
        | Get Call Queue Call Forward Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/queues/callForwarding/availableNumbers``
   * - :meth:`api.telephony.callqueue.create <wxc_sdk.telephony.callqueue.CallQueueApi.create>`
        | Create a Call Queue
        | ``POST /telephony/config/locations/{location_id}/queues``
   * - :meth:`api.telephony.callqueue.delete_queue <wxc_sdk.telephony.callqueue.CallQueueApi.delete_queue>`
        | Delete a Call Queue
        | ``DELETE /telephony/config/locations/{location_id}/queues/{queue_id}``
   * - :meth:`api.telephony.callqueue.details <wxc_sdk.telephony.callqueue.CallQueueApi.details>`
        | Get Details for a Call Queue
        | ``GET /telephony/config/locations/{location_id}/queues/{queue_id}``
   * - :meth:`api.telephony.callqueue.forwarding.call_forwarding_rule <wxc_sdk.telephony.forwarding.ForwardingApi.call_forwarding_rule>`
        | Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue
        | ``GET /telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding/selectiveRules/{rule_id}``
   * - :meth:`api.telephony.callqueue.forwarding.create_call_forwarding_rule <wxc_sdk.telephony.forwarding.ForwardingApi.create_call_forwarding_rule>`
        | Create a Selective Call Forwarding Rule feature
        | ``POST /telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding/selectiveRules``
   * - :meth:`api.telephony.callqueue.forwarding.delete_call_forwarding_rule <wxc_sdk.telephony.forwarding.ForwardingApi.delete_call_forwarding_rule>`
        | Delete a Selective Call Forwarding Rule for the designated feature
        | ``DELETE /telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding/selectiveRules/{rule_id}``
   * - :meth:`api.telephony.callqueue.forwarding.settings <wxc_sdk.telephony.forwarding.ForwardingApi.settings>`
        | Retrieve Call Forwarding settings for the designated feature including the list of call
        | ``GET /telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding``
   * - :meth:`api.telephony.callqueue.forwarding.switch_mode_for_call_forwarding <wxc_sdk.telephony.forwarding.ForwardingApi.switch_mode_for_call_forwarding>`
        | Switch Mode for Call Forwarding Settings for an entity
        | ``POST /telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding/actions/switchMode/invoke``
   * - :meth:`api.telephony.callqueue.forwarding.update <wxc_sdk.telephony.forwarding.ForwardingApi.update>`
        | Update Call Forwarding Settings for a feature
        | ``PUT /telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding``
   * - :meth:`api.telephony.callqueue.forwarding.update_call_forwarding_rule <wxc_sdk.telephony.forwarding.ForwardingApi.update_call_forwarding_rule>`
        | Update a Selective Call Forwarding Rule's settings for the designated feature
        | ``PUT /telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding/selectiveRules/{rule_id}``
   * - :meth:`api.telephony.callqueue.get_call_queue_settings <wxc_sdk.telephony.callqueue.CallQueueApi.get_call_queue_settings>`
        | Get Call Queue Settings
        | ``GET /telephony/config/queues/settings``
   * - :meth:`api.telephony.callqueue.list <wxc_sdk.telephony.callqueue.CallQueueApi.list>`
        | Read the List of Call Queues
        | ``GET /telephony/config/queues``
   * - :meth:`api.telephony.callqueue.primary_available_phone_numbers <wxc_sdk.telephony.callqueue.CallQueueApi.primary_available_phone_numbers>`
        | Get Call Queue Primary Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/queues/availableNumbers``
   * - :meth:`api.telephony.callqueue.update <wxc_sdk.telephony.callqueue.CallQueueApi.update>`
        | Update a Call Queue
        | ``PUT /telephony/config/locations/{location_id}/queues/{queue_id}``
   * - :meth:`api.telephony.callqueue.update_call_queue_settings <wxc_sdk.telephony.callqueue.CallQueueApi.update_call_queue_settings>`
        | Update Call Queue Settings
        | ``PUT /telephony/config/queues/settings``
   * - :meth:`api.telephony.calls.answer <wxc_sdk.telephony.calls.CallsApi.answer>`
        | Answer
        | ``POST /telephony/calls/answer``
   * - :meth:`api.telephony.calls.barge_in <wxc_sdk.telephony.calls.CallsApi.barge_in>`
        | Barge In
        | ``POST /telephony/calls/bargeIn``
   * - :meth:`api.telephony.calls.call_details <wxc_sdk.telephony.calls.CallsApi.call_details>`
        | Get Call Details
        | ``GET /telephony/calls/{call_id}``
   * - :meth:`api.telephony.calls.call_history <wxc_sdk.telephony.calls.CallsApi.call_history>`
        | List Call History
        | ``GET /telephony/calls/history``
   * - :meth:`api.telephony.calls.dial <wxc_sdk.telephony.calls.CallsApi.dial>`
        | Dial
        | ``POST /telephony/calls/dial``
   * - :meth:`api.telephony.calls.divert <wxc_sdk.telephony.calls.CallsApi.divert>`
        | Divert
        | ``POST /telephony/calls/divert``
   * - :meth:`api.telephony.calls.hangup <wxc_sdk.telephony.calls.CallsApi.hangup>`
        | Hangup
        | ``POST /telephony/calls/hangup``
   * - :meth:`api.telephony.calls.hold <wxc_sdk.telephony.calls.CallsApi.hold>`
        | Hold
        | ``POST /telephony/calls/hold``
   * - :meth:`api.telephony.calls.list_calls <wxc_sdk.telephony.calls.CallsApi.list_calls>`
        | List Calls
        | ``GET /telephony/calls``
   * - :meth:`api.telephony.calls.mute <wxc_sdk.telephony.calls.CallsApi.mute>`
        | Mute
        | ``POST /telephony/calls/mute``
   * - :meth:`api.telephony.calls.park <wxc_sdk.telephony.calls.CallsApi.park>`
        | Park
        | ``POST /telephony/calls/park``
   * - :meth:`api.telephony.calls.pause_recording <wxc_sdk.telephony.calls.CallsApi.pause_recording>`
        | Pause Recording
        | ``POST /telephony/calls/pauseRecording``
   * - :meth:`api.telephony.calls.pickup <wxc_sdk.telephony.calls.CallsApi.pickup>`
        | Pickup
        | ``POST /telephony/calls/pickup``
   * - :meth:`api.telephony.calls.pull <wxc_sdk.telephony.calls.CallsApi.pull>`
        | Pull
        | ``POST /telephony/calls/pull``
   * - :meth:`api.telephony.calls.push <wxc_sdk.telephony.calls.CallsApi.push>`
        | Push
        | ``POST /telephony/calls/push``
   * - :meth:`api.telephony.calls.reject <wxc_sdk.telephony.calls.CallsApi.reject>`
        | Reject
        | ``POST /telephony/calls/reject``
   * - :meth:`api.telephony.calls.resume <wxc_sdk.telephony.calls.CallsApi.resume>`
        | Resume
        | ``POST /telephony/calls/resume``
   * - :meth:`api.telephony.calls.resume_recording <wxc_sdk.telephony.calls.CallsApi.resume_recording>`
        | Resume Recording
        | ``POST /telephony/calls/resumeRecording``
   * - :meth:`api.telephony.calls.retrieve <wxc_sdk.telephony.calls.CallsApi.retrieve>`
        | Retrieve
        | ``POST /telephony/calls/retrieve``
   * - :meth:`api.telephony.calls.start_recording <wxc_sdk.telephony.calls.CallsApi.start_recording>`
        | Start Recording
        | ``POST /telephony/calls/startRecording``
   * - :meth:`api.telephony.calls.stop_recording <wxc_sdk.telephony.calls.CallsApi.stop_recording>`
        | Stop Recording
        | ``POST /telephony/calls/stopRecording``
   * - :meth:`api.telephony.calls.transfer <wxc_sdk.telephony.calls.CallsApi.transfer>`
        | Transfer
        | ``POST /telephony/calls/transfer``
   * - :meth:`api.telephony.calls.transmit_dtmf <wxc_sdk.telephony.calls.CallsApi.transmit_dtmf>`
        | Transmit DTMF
        | ``POST /telephony/calls/transmitDtmf``
   * - :meth:`api.telephony.calls.unmute <wxc_sdk.telephony.calls.CallsApi.unmute>`
        | Unmute
        | ``POST /telephony/calls/unmute``
   * - :meth:`api.telephony.calls.update_external_voicemail_mwi <wxc_sdk.telephony.calls.CallsApi.update_external_voicemail_mwi>`
        | Set or Clear Message Waiting Indicator (MWI) Status
        | ``POST /telephony/externalVoicemail/mwi``
   * - :meth:`api.telephony.conference.add_participant <wxc_sdk.telephony.conference.ConferenceControlsApi.add_participant>`
        | Add Participant
        | ``POST /telephony/conference/addParticipant``
   * - :meth:`api.telephony.conference.deafen_participant <wxc_sdk.telephony.conference.ConferenceControlsApi.deafen_participant>`
        | Deafen Participant
        | ``POST /telephony/conference/deafen``
   * - :meth:`api.telephony.conference.get_conference_details <wxc_sdk.telephony.conference.ConferenceControlsApi.get_conference_details>`
        | Get Conference Details
        | ``GET /telephony/conference``
   * - :meth:`api.telephony.conference.hold <wxc_sdk.telephony.conference.ConferenceControlsApi.hold>`
        | Hold
        | ``POST /telephony/conference/hold``
   * - :meth:`api.telephony.conference.mute <wxc_sdk.telephony.conference.ConferenceControlsApi.mute>`
        | Mute
        | ``POST /telephony/conference/mute``
   * - :meth:`api.telephony.conference.release_conference <wxc_sdk.telephony.conference.ConferenceControlsApi.release_conference>`
        | Release Conference
        | ``DELETE /telephony/conference``
   * - :meth:`api.telephony.conference.resume <wxc_sdk.telephony.conference.ConferenceControlsApi.resume>`
        | Resume
        | ``POST /telephony/conference/resume``
   * - :meth:`api.telephony.conference.start_conference <wxc_sdk.telephony.conference.ConferenceControlsApi.start_conference>`
        | Start Conference
        | ``POST /telephony/conference``
   * - :meth:`api.telephony.conference.undeafen_participant <wxc_sdk.telephony.conference.ConferenceControlsApi.undeafen_participant>`
        | Undeafen Participant
        | ``POST /telephony/conference/undeafen``
   * - :meth:`api.telephony.conference.unmute <wxc_sdk.telephony.conference.ConferenceControlsApi.unmute>`
        | Unmute
        | ``POST /telephony/conference/unmute``
   * - :meth:`api.telephony.create_a_call_token <wxc_sdk.telephony.TelephonyApi.create_a_call_token>`
        | Create a call token
        | ``POST /telephony/click2call/callToken``
   * - :meth:`api.telephony.cx_essentials.available_agents <wxc_sdk.telephony.cx_essentials.CustomerExperienceEssentialsApi.available_agents>`
        | Get List of available agents for Customer Experience Essentials
        | ``GET /telephony/config/locations/{location_id}/cxEssentials/agents/availableAgents``
   * - :meth:`api.telephony.cx_essentials.callqueue_recording.configure <wxc_sdk.telephony.cx_essentials.callqueue_recording.QueueCallRecordingSettingsApi.configure>`
        | Configure Queue Call Recording Settings for a Queue
        | ``PUT /telephony/config/locations/{location_id}/queues/{queue_id}/cxEssentials/callRecordings``
   * - :meth:`api.telephony.cx_essentials.callqueue_recording.read <wxc_sdk.telephony.cx_essentials.callqueue_recording.QueueCallRecordingSettingsApi.read>`
        | Read Queue Call Recording Settings for a Queue
        | ``GET /telephony/config/locations/{location_id}/queues/{queue_id}/cxEssentials/callRecordings``
   * - :meth:`api.telephony.cx_essentials.get_screen_pop_configuration <wxc_sdk.telephony.cx_essentials.CustomerExperienceEssentialsApi.get_screen_pop_configuration>`
        | Get Screen Pop configuration for a Call Queue in a Location
        | ``GET /telephony/config/locations/{location_id}/queues/{queue_id}/cxEssentials/screenPop``
   * - :meth:`api.telephony.cx_essentials.modify_screen_pop_configuration <wxc_sdk.telephony.cx_essentials.CustomerExperienceEssentialsApi.modify_screen_pop_configuration>`
        | Modify Screen Pop configuration for a Call Queue in a Location
        | ``PUT /telephony/config/locations/{location_id}/queues/{queue_id}/cxEssentials/screenPop``
   * - :meth:`api.telephony.cx_essentials.wrapup_reasons.available_queues <wxc_sdk.telephony.cx_essentials.wrapup_reasons.WrapupReasonApi.available_queues>`
        | Read Available Queues
        | ``GET /telephony/config/cxEssentials/wrapup/reasons/{wrapup_reason_id}/availableQueues``
   * - :meth:`api.telephony.cx_essentials.wrapup_reasons.create <wxc_sdk.telephony.cx_essentials.wrapup_reasons.WrapupReasonApi.create>`
        | Create Wrap Up Reason
        | ``POST /telephony/config/cxEssentials/wrapup/reasons``
   * - :meth:`api.telephony.cx_essentials.wrapup_reasons.delete <wxc_sdk.telephony.cx_essentials.wrapup_reasons.WrapupReasonApi.delete>`
        | Delete Wrap Up Reason
        | ``DELETE /telephony/config/cxEssentials/wrapup/reasons/{wrapup_reason_id}``
   * - :meth:`api.telephony.cx_essentials.wrapup_reasons.details <wxc_sdk.telephony.cx_essentials.wrapup_reasons.WrapupReasonApi.details>`
        | Read Wrap Up Reason
        | ``GET /telephony/config/cxEssentials/wrapup/reasons/{wrapup_reason_id}``
   * - :meth:`api.telephony.cx_essentials.wrapup_reasons.list <wxc_sdk.telephony.cx_essentials.wrapup_reasons.WrapupReasonApi.list>`
        | List Wrap Up Reasons
        | ``GET /telephony/config/cxEssentials/wrapup/reasons``
   * - :meth:`api.telephony.cx_essentials.wrapup_reasons.read_queue_settings <wxc_sdk.telephony.cx_essentials.wrapup_reasons.WrapupReasonApi.read_queue_settings>`
        | Read Wrap Up Reason Settings
        | ``GET /telephony/config/cxEssentials/locations/{location_id}/queues/{queue_id}/wrapup/settings``
   * - :meth:`api.telephony.cx_essentials.wrapup_reasons.update <wxc_sdk.telephony.cx_essentials.wrapup_reasons.WrapupReasonApi.update>`
        | Update Wrap Up Reason
        | ``PUT /telephony/config/cxEssentials/wrapup/reasons/{wrapup_reason_id}``
   * - :meth:`api.telephony.cx_essentials.wrapup_reasons.update_queue_settings <wxc_sdk.telephony.cx_essentials.wrapup_reasons.WrapupReasonApi.update_queue_settings>`
        | Update Wrap Up Reason Settings
        | ``PUT /telephony/config/cxEssentials/locations/{location_id}/queues/{queue_id}/wrapup/settings``
   * - :meth:`api.telephony.cx_essentials.wrapup_reasons.validate <wxc_sdk.telephony.cx_essentials.wrapup_reasons.WrapupReasonApi.validate>`
        | Validate Wrap Up Reason
        | ``POST /telephony/config/cxEssentials/wrapup/reasons/actions/validateName/invoke``
   * - :meth:`api.telephony.dect_devices.add_a_handset <wxc_sdk.telephony.dect_devices.DECTDevicesApi.add_a_handset>`
        | Add a Handset to a DECT Network
        | ``POST /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets``
   * - :meth:`api.telephony.dect_devices.add_list_of_handsets <wxc_sdk.telephony.dect_devices.DECTDevicesApi.add_list_of_handsets>`
        | Add a List of Handsets to a DECT Network
        | ``POST /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets/bulk``
   * - :meth:`api.telephony.dect_devices.available_members <wxc_sdk.telephony.dect_devices.DECTDevicesApi.available_members>`
        | Search Available Members
        | ``GET /telephony/config/devices/availableMembers``
   * - :meth:`api.telephony.dect_devices.base_station_details <wxc_sdk.telephony.dect_devices.DECTDevicesApi.base_station_details>`
        | Get the details of a specific DECT Network Base Station
        | ``GET /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/baseStations/{base_station_id}``
   * - :meth:`api.telephony.dect_devices.create_base_stations <wxc_sdk.telephony.dect_devices.DECTDevicesApi.create_base_stations>`
        | Create Multiple Base Stations
        | ``POST /telephony/config/locations/{location_id}/dectNetworks/{dect_id}/baseStations``
   * - :meth:`api.telephony.dect_devices.create_dect_network <wxc_sdk.telephony.dect_devices.DECTDevicesApi.create_dect_network>`
        | Create a DECT Network
        | ``POST /telephony/config/locations/{location_id}/dectNetworks``
   * - :meth:`api.telephony.dect_devices.dect_network_details <wxc_sdk.telephony.dect_devices.DECTDevicesApi.dect_network_details>`
        | Get DECT Network Details
        | ``GET /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}``
   * - :meth:`api.telephony.dect_devices.dect_networks_associated_with_person <wxc_sdk.telephony.dect_devices.DECTDevicesApi.dect_networks_associated_with_person>`
        | GET List of DECT networks associated with a Person
        | ``GET /telephony/config/people/{person_id}/dectNetworks``
   * - :meth:`api.telephony.dect_devices.dect_networks_associated_with_virtual_line <wxc_sdk.telephony.dect_devices.DECTDevicesApi.dect_networks_associated_with_virtual_line>`
        | Get List of Dect Networks Handsets for a Virtual Line
        | ``GET /telephony/config/virtualLines/{virtual_line_id}/dectNetworks``
   * - :meth:`api.telephony.dect_devices.dect_networks_associated_with_workspace <wxc_sdk.telephony.dect_devices.DECTDevicesApi.dect_networks_associated_with_workspace>`
        | GET List of DECT networks associated with a workspace
        | ``GET /telephony/config/workspaces/{workspace_id}/dectNetworks``
   * - :meth:`api.telephony.dect_devices.delete_base_station <wxc_sdk.telephony.dect_devices.DECTDevicesApi.delete_base_station>`
        | Delete a specific DECT Network Base Station
        | ``DELETE /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/baseStations/{base_station_id}``
   * - :meth:`api.telephony.dect_devices.delete_bulk_base_stations <wxc_sdk.telephony.dect_devices.DECTDevicesApi.delete_bulk_base_stations>`
        | Delete bulk DECT Network Base Stations
        | ``DELETE /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/baseStations``
   * - :meth:`api.telephony.dect_devices.delete_dect_network <wxc_sdk.telephony.dect_devices.DECTDevicesApi.delete_dect_network>`
        | Delete DECT Network
        | ``DELETE /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}``
   * - :meth:`api.telephony.dect_devices.delete_handset <wxc_sdk.telephony.dect_devices.DECTDevicesApi.delete_handset>`
        | Delete specific DECT Network Handset Details
        | ``DELETE /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets/{handset_id}``
   * - :meth:`api.telephony.dect_devices.delete_handsets <wxc_sdk.telephony.dect_devices.DECTDevicesApi.delete_handsets>`
        | Delete multiple handsets
        | ``DELETE /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets``
   * - :meth:`api.telephony.dect_devices.device_type_list <wxc_sdk.telephony.dect_devices.DECTDevicesApi.device_type_list>`
        | Read the DECT device type list
        | ``GET /telephony/config/devices/dectNetworks/supportedDevices``
   * - :meth:`api.telephony.dect_devices.generate_and_enable_dect_serviceability_password <wxc_sdk.telephony.dect_devices.DECTDevicesApi.generate_and_enable_dect_serviceability_password>`
        | Generate and Enable DECT Serviceability Password
        | ``POST /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/serviceabilityPassword/actions/generate/invoke``
   * - :meth:`api.telephony.dect_devices.get_dect_serviceability_password_status <wxc_sdk.telephony.dect_devices.DECTDevicesApi.get_dect_serviceability_password_status>`
        | Get DECT Serviceability Password status
        | ``GET /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/serviceabilityPassword``
   * - :meth:`api.telephony.dect_devices.handset_details <wxc_sdk.telephony.dect_devices.DECTDevicesApi.handset_details>`
        | Get Specific DECT Network Handset Details
        | ``GET /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets/{handset_id}``
   * - :meth:`api.telephony.dect_devices.list_base_stations <wxc_sdk.telephony.dect_devices.DECTDevicesApi.list_base_stations>`
        | Get a list of DECT Network Base Stations
        | ``GET /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/baseStations``
   * - :meth:`api.telephony.dect_devices.list_dect_networks <wxc_sdk.telephony.dect_devices.DECTDevicesApi.list_dect_networks>`
        | Get the List of DECT Networks for an organization
        | ``GET /telephony/config/dectNetworks``
   * - :meth:`api.telephony.dect_devices.list_handsets <wxc_sdk.telephony.dect_devices.DECTDevicesApi.list_handsets>`
        | Get List of Handsets for a DECT Network ID
        | ``GET /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets``
   * - :meth:`api.telephony.dect_devices.update_dect_network <wxc_sdk.telephony.dect_devices.DECTDevicesApi.update_dect_network>`
        | Update DECT Network
        | ``PUT /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}``
   * - :meth:`api.telephony.dect_devices.update_dect_network_settings <wxc_sdk.telephony.dect_devices.DECTDevicesApi.update_dect_network_settings>`
        | Update DECT Network from settings
        | ``PUT /telephony/config/locations/{id}/dectNetworks/{id}``
   * - :meth:`api.telephony.dect_devices.update_dect_serviceability_password_status <wxc_sdk.telephony.dect_devices.DECTDevicesApi.update_dect_serviceability_password_status>`
        | Update DECT Serviceability Password status
        | ``PUT /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/serviceabilityPassword``
   * - :meth:`api.telephony.dect_devices.update_handset <wxc_sdk.telephony.dect_devices.DECTDevicesApi.update_handset>`
        | Update DECT Network Handset
        | ``PUT /telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets/{handset_id}``
   * - :meth:`api.telephony.device_settings <wxc_sdk.telephony.TelephonyApi.device_settings>`
        | Get device override settings for an organization
        | ``GET /telephony/config/devices/settings``
   * - :meth:`api.telephony.devices.apply_changes <wxc_sdk.telephony.devices.TelephonyDevicesApi.apply_changes>`
        | Apply Changes for a specific device
        | ``POST /telephony/config/devices/{device_id}/actions/applyChanges/invoke``
   * - :meth:`api.telephony.devices.available_members <wxc_sdk.telephony.devices.TelephonyDevicesApi.available_members>`
        | Search members that can be assigned to the device
        | ``GET /telephony/config/devices/{device_id}/availableMembers``
   * - :meth:`api.telephony.devices.create_line_key_template <wxc_sdk.telephony.devices.TelephonyDevicesApi.create_line_key_template>`
        | Create a Line Key Template
        | ``POST /telephony/config/devices/lineKeyTemplates``
   * - :meth:`api.telephony.devices.delete_background_images <wxc_sdk.telephony.devices.TelephonyDevicesApi.delete_background_images>`
        | Delete Device Background Images
        | ``DELETE /telephony/config/devices/backgroundImages``
   * - :meth:`api.telephony.devices.delete_line_key_template <wxc_sdk.telephony.devices.TelephonyDevicesApi.delete_line_key_template>`
        | Delete a Line Key Template
        | ``DELETE /telephony/config/devices/lineKeyTemplates/{template_id}``
   * - :meth:`api.telephony.devices.details <wxc_sdk.telephony.devices.TelephonyDevicesApi.details>`
        | Get Webex Calling Device Details
        | ``GET /telephony/config/devices/{device_id}``
   * - :meth:`api.telephony.devices.device_settings <wxc_sdk.telephony.devices.TelephonyDevicesApi.device_settings>`
        | Get override settings for a device
        | ``GET /telephony/config/devices/{device_id}/settings``
   * - :meth:`api.telephony.devices.dynamic_settings.get_customer_device_settings <wxc_sdk.telephony.devices.dynamic_settings.DevicesDynamicSettingsApi.get_customer_device_settings>`
        | Get Customer Device Dynamic Settings
        | ``POST /telephony/config/lists/devices/dynamicSettings/actions/getSettings/invoke``
   * - :meth:`api.telephony.devices.dynamic_settings.get_device_settings <wxc_sdk.telephony.devices.dynamic_settings.DevicesDynamicSettingsApi.get_device_settings>`
        | Get Device Dynamic Settings
        | ``POST /telephony/config/lists/devices/{device_id}/dynamicSettings/actions/getSettings/invoke``
   * - :meth:`api.telephony.devices.dynamic_settings.get_location_device_settings <wxc_sdk.telephony.devices.dynamic_settings.DevicesDynamicSettingsApi.get_location_device_settings>`
        | Get Location Device Dynamic Settings
        | ``POST /telephony/config/lists/locations/{location_id}/devices/dynamicSettings/actions/getSettings/invoke``
   * - :meth:`api.telephony.devices.dynamic_settings.get_settings_groups <wxc_sdk.telephony.devices.dynamic_settings.DevicesDynamicSettingsApi.get_settings_groups>`
        | Get Settings Groups
        | ``GET /telephony/config/devices/dynamicSettings/settingsGroups``
   * - :meth:`api.telephony.devices.dynamic_settings.get_validation_schema <wxc_sdk.telephony.devices.dynamic_settings.DevicesDynamicSettingsApi.get_validation_schema>`
        | Get Validation Schema
        | ``GET /telephony/config/devices/dynamicSettings/validationSchema``
   * - :meth:`api.telephony.devices.dynamic_settings.update_specified_settings_for_the_device <wxc_sdk.telephony.devices.dynamic_settings.DevicesDynamicSettingsApi.update_specified_settings_for_the_device>`
        | Update specified settings for the device
        | ``PUT /telephony/config/devices/{device_id}/dynamicSettings``
   * - :meth:`api.telephony.devices.get_count_of_available_members <wxc_sdk.telephony.devices.TelephonyDevicesApi.get_count_of_available_members>`
        | Get Count of Available Members
        | ``GET /telephony/config/devices/availableMembers/count``
   * - :meth:`api.telephony.devices.get_count_of_members <wxc_sdk.telephony.devices.TelephonyDevicesApi.get_count_of_members>`
        | Get Count of Members
        | ``GET /telephony/config/devices/{device_id}/availableMembers/count``
   * - :meth:`api.telephony.devices.get_device_layout <wxc_sdk.telephony.devices.TelephonyDevicesApi.get_device_layout>`
        | Get Device Layout by Device ID
        | ``GET /telephony/config/devices/{device_id}/layout``
   * - :meth:`api.telephony.devices.get_person_device_settings <wxc_sdk.telephony.devices.TelephonyDevicesApi.get_person_device_settings>`
        | Get Device Settings for a Person
        | ``GET /telephony/config/people/{person_id}/devices/settings``
   * - :meth:`api.telephony.devices.get_workspace_device_settings <wxc_sdk.telephony.devices.TelephonyDevicesApi.get_workspace_device_settings>`
        | Get Device Settings for a Workspace
        | ``GET /telephony/config/workspaces/{workspace_id}/devices/settings``
   * - :meth:`api.telephony.devices.line_key_template_details <wxc_sdk.telephony.devices.TelephonyDevicesApi.line_key_template_details>`
        | Get details of a Line Key Template
        | ``GET /telephony/config/devices/lineKeyTemplates/{template_id}``
   * - :meth:`api.telephony.devices.list_background_images <wxc_sdk.telephony.devices.TelephonyDevicesApi.list_background_images>`
        | Read the List of Background Images
        | ``GET /telephony/config/devices/backgroundImages``
   * - :meth:`api.telephony.devices.list_line_key_templates <wxc_sdk.telephony.devices.TelephonyDevicesApi.list_line_key_templates>`
        | Read the list of Line Key Templates
        | ``GET /telephony/config/devices/lineKeyTemplates``
   * - :meth:`api.telephony.devices.members <wxc_sdk.telephony.devices.TelephonyDevicesApi.members>`
        | Get Device Members
        | ``GET /telephony/config/devices/{device_id}/members``
   * - :meth:`api.telephony.devices.modify_device_layout <wxc_sdk.telephony.devices.TelephonyDevicesApi.modify_device_layout>`
        | Modify Device Layout by Device ID
        | ``PUT /telephony/config/devices/{device_id}/layout``
   * - :meth:`api.telephony.devices.modify_line_key_template <wxc_sdk.telephony.devices.TelephonyDevicesApi.modify_line_key_template>`
        | Modify a Line Key Template
        | ``PUT /telephony/config/devices/lineKeyTemplates/{id}``
   * - :meth:`api.telephony.devices.preview_apply_line_key_template <wxc_sdk.telephony.devices.TelephonyDevicesApi.preview_apply_line_key_template>`
        | Preview Apply Line Key Template
        | ``POST /telephony/config/devices/actions/previewApplyLineKeyTemplate/invoke``
   * - :meth:`api.telephony.devices.supported_devices <wxc_sdk.telephony.devices.TelephonyDevicesApi.supported_devices>`
        | Read the List of Supported Devices
        | ``GET /telephony/config/supportedDevices``
   * - :meth:`api.telephony.devices.update_device_settings <wxc_sdk.telephony.devices.TelephonyDevicesApi.update_device_settings>`
        | Modify override settings for a device
        | ``PUT /telephony/config/devices/{device_id}/settings``
   * - :meth:`api.telephony.devices.update_members <wxc_sdk.telephony.devices.TelephonyDevicesApi.update_members>`
        | Modify member details on the device
        | ``PUT /telephony/config/devices/{device_id}/members``
   * - :meth:`api.telephony.devices.update_person_device_settings <wxc_sdk.telephony.devices.TelephonyDevicesApi.update_person_device_settings>`
        | Update Device Settings for a Person
        | ``PUT /telephony/config/people/{person_id}/devices/settings``
   * - :meth:`api.telephony.devices.update_third_party_device <wxc_sdk.telephony.devices.TelephonyDevicesApi.update_third_party_device>`
        | Update Third Party Device
        | ``PUT /telephony/config/devices/{device_id}``
   * - :meth:`api.telephony.devices.update_workspace_device_settings <wxc_sdk.telephony.devices.TelephonyDevicesApi.update_workspace_device_settings>`
        | Update Device Settings for a Workspace
        | ``PUT /telephony/config/workspaces/{workspace_id}/devices/settings``
   * - :meth:`api.telephony.devices.upload_background_image <wxc_sdk.telephony.devices.TelephonyDevicesApi.upload_background_image>`
        | Upload a Device Background Image
        | ``POST /telephony/config/devices/{device_id}/actions/backgroundImageUpload/invoke``
   * - :meth:`api.telephony.devices.user_devices_count <wxc_sdk.telephony.devices.TelephonyDevicesApi.user_devices_count>`
        | Get User Devices Count
        | ``GET /telephony/config/people/{person_id}/devices/count``
   * - :meth:`api.telephony.devices.validate_macs <wxc_sdk.telephony.devices.TelephonyDevicesApi.validate_macs>`
        | Validate a list of MAC addresses
        | ``POST /telephony/config/devices/actions/validateMacs/invoke``
   * - :meth:`api.telephony.emergency_address.add_to_location <wxc_sdk.telephony.emergency_address.EmergencyAddressApi.add_to_location>`
        | Add an Emergency Address to a Location
        | ``POST /telephony/pstn/locations/{location_id}/emergencyAddress``
   * - :meth:`api.telephony.emergency_address.lookup_for_location <wxc_sdk.telephony.emergency_address.EmergencyAddressApi.lookup_for_location>`
        | Emergency Address Lookup to Verify if Address is Valid
        | ``POST /telephony/pstn/locations/{location_id}/emergencyAddress/lookup``
   * - :meth:`api.telephony.emergency_address.update_for_location <wxc_sdk.telephony.emergency_address.EmergencyAddressApi.update_for_location>`
        | Update the Emergency Address of a Location
        | ``PUT /telephony/pstn/locations/{location_id}/emergencyAddresses/{address_id}``
   * - :meth:`api.telephony.emergency_address.update_for_phone_number <wxc_sdk.telephony.emergency_address.EmergencyAddressApi.update_for_phone_number>`
        | Update the emergency address for a phone number
        | ``PUT /telephony/pstn/numbers/{phone_number}/emergencyAddress``
   * - :meth:`api.telephony.emergency_services.create_location_address_and_alert_email <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.create_location_address_and_alert_email>`
        | Create a RedSky Building Address and Alert Email for a Location
        | ``POST /telephony/config/locations/{location_id}/redSky/building``
   * - :meth:`api.telephony.emergency_services.create_redsky_account_and_admin <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.create_redsky_account_and_admin>`
        | Create an account and admin in RedSky
        | ``POST /telephony/config/redSky``
   * - :meth:`api.telephony.emergency_services.get_location_compliance_status <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.get_location_compliance_status>`
        | Get a Location's RedSky Compliance Status
        | ``GET /telephony/config/locations/{location_id}/redSky/status``
   * - :meth:`api.telephony.emergency_services.get_location_notification <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.get_location_notification>`
        | Get a Location Emergency Call Notification
        | ``GET /telephony/config/locations/{location_id}/emergencyCallNotification``
   * - :meth:`api.telephony.emergency_services.get_location_parameters <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.get_location_parameters>`
        | Get a Location's RedSky Emergency Calling Parameters
        | ``GET /telephony/config/locations/{location_id}/redSky``
   * - :meth:`api.telephony.emergency_services.get_notification <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.get_notification>`
        | Get an Organization Emergency Call Notification
        | ``GET /telephony/config/emergencyCallNotification``
   * - :meth:`api.telephony.emergency_services.get_org_compliance <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.get_org_compliance>`
        | Get the Organization Compliance Status and the Location Status List
        | ``GET /telephony/config/redSky/complianceStatus``
   * - :meth:`api.telephony.emergency_services.get_org_compliance_status <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.get_org_compliance_status>`
        | Get the Organization Compliance Status for a RedSky Account
        | ``GET /telephony/config/redSky/status``
   * - :meth:`api.telephony.emergency_services.get_redsky_account_details <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.get_redsky_account_details>`
        | Retrieve RedSky account details for an organization
        | ``GET /telephony/config/redSky``
   * - :meth:`api.telephony.emergency_services.hunt_group_ecbn_dependencies <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.hunt_group_ecbn_dependencies>`
        | Get Dependencies for a Hunt Group Emergency Callback Number
        | ``GET /telephony/config/huntGroups/{hunt_group_id}/emergencyCallbackNumber/dependencies``
   * - :meth:`api.telephony.emergency_services.login <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.login>`
        | Login to a RedSky Admin Account
        | ``POST /telephony/config/redSky/actions/login/invoke``
   * - :meth:`api.telephony.emergency_services.update_location_address <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.update_location_address>`
        | Update a RedSky Building Address for a Location
        | ``PUT /telephony/config/locations/{location_id}/redSky/building``
   * - :meth:`api.telephony.emergency_services.update_location_compliance_status <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.update_location_compliance_status>`
        | Update a Location's RedSky Compliance Status
        | ``PUT /telephony/config/locations/{location_id}/redSky/status``
   * - :meth:`api.telephony.emergency_services.update_location_notification <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.update_location_notification>`
        | Update a location emergency call notification
        | ``PUT /telephony/config/locations/{location_id}/emergencyCallNotification``
   * - :meth:`api.telephony.emergency_services.update_notification <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.update_notification>`
        | Update an organization emergency call notification
        | ``PUT /telephony/config/emergencyCallNotification``
   * - :meth:`api.telephony.emergency_services.update_org_compliance_status <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.update_org_compliance_status>`
        | Update the Organization RedSky Account's Compliance Status
        | ``PUT /telephony/config/redSky/status``
   * - :meth:`api.telephony.emergency_services.update_service_settings <wxc_sdk.telephony.emergency_services.OrgEmergencyServicesApi.update_service_settings>`
        | Update RedSky Service Settings
        | ``PUT /telephony/config/redSky/serviceSettings``
   * - :meth:`api.telephony.get_call_captions_settings <wxc_sdk.telephony.TelephonyApi.get_call_captions_settings>`
        | Get the organization call captions settings
        | ``GET /telephony/config/callCaptions``
   * - :meth:`api.telephony.get_large_organization_status <wxc_sdk.telephony.TelephonyApi.get_large_organization_status>`
        | Get Large Organization Status
        | ``GET /telephony/config/largeOrgStatus``
   * - :meth:`api.telephony.guest_calling.available_members <wxc_sdk.telephony.guest_calling.GuestCallingApi.available_members>`
        | Read the Click-to-call Available Members
        | ``GET /telephony/config/guestCalling/availableMembers``
   * - :meth:`api.telephony.guest_calling.members <wxc_sdk.telephony.guest_calling.GuestCallingApi.members>`
        | Read the Click-to-call Members
        | ``GET /telephony/config/guestCalling/members``
   * - :meth:`api.telephony.guest_calling.read <wxc_sdk.telephony.guest_calling.GuestCallingApi.read>`
        | Read the Click-to-call Settings
        | ``GET /telephony/config/guestCalling``
   * - :meth:`api.telephony.guest_calling.update <wxc_sdk.telephony.guest_calling.GuestCallingApi.update>`
        | Update the Click-to-call Settings
        | ``PUT /telephony/config/guestCalling``
   * - :meth:`api.telephony.hotdesk.delete_session <wxc_sdk.telephony.hotdesk.HotDeskApi.delete_session>`
        | Delete Session
        | ``DELETE /hotdesk/sessions/{session_id}``
   * - :meth:`api.telephony.hotdesk.list_sessions <wxc_sdk.telephony.hotdesk.HotDeskApi.list_sessions>`
        | List Sessions
        | ``GET /hotdesk/sessions``
   * - :meth:`api.telephony.hotdesking_voiceportal.location_get <wxc_sdk.telephony.hotdesking_voiceportal.HotDeskingSigninViaVoicePortalApi.location_get>`
        | Voice Portal Hot desking sign in details for a location
        | ``GET /telephony/config/locations/{location_id}/features/hotDesking``
   * - :meth:`api.telephony.hotdesking_voiceportal.location_update <wxc_sdk.telephony.hotdesking_voiceportal.HotDeskingSigninViaVoicePortalApi.location_update>`
        | Update Voice Portal Hot desking sign in details for a location
        | ``PUT /telephony/config/locations/{location_id}/features/hotDesking``
   * - :meth:`api.telephony.hotdesking_voiceportal.user_get <wxc_sdk.telephony.hotdesking_voiceportal.HotDeskingSigninViaVoicePortalApi.user_get>`
        | Voice Portal Hot desking sign in details for a user
        | ``GET /telephony/config/people/{person_id}/features/hotDesking/guest``
   * - :meth:`api.telephony.hotdesking_voiceportal.user_update <wxc_sdk.telephony.hotdesking_voiceportal.HotDeskingSigninViaVoicePortalApi.user_update>`
        | Update Voice Portal Hot desking sign in details for a user
        | ``PUT /telephony/config/people/{person_id}/features/hotDesking/guest``
   * - :meth:`api.telephony.huntgroup.alternate_available_phone_numbers <wxc_sdk.telephony.huntgroup.HuntGroupApi.alternate_available_phone_numbers>`
        | Get Hunt Group Alternate Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/huntGroups/alternate/availableNumbers``
   * - :meth:`api.telephony.huntgroup.create <wxc_sdk.telephony.huntgroup.HuntGroupApi.create>`
        | Create a Hunt Group
        | ``POST /telephony/config/locations/{location_id}/huntGroups``
   * - :meth:`api.telephony.huntgroup.delete_huntgroup <wxc_sdk.telephony.huntgroup.HuntGroupApi.delete_huntgroup>`
        | Delete a Hunt Group
        | ``DELETE /telephony/config/locations/{location_id}/huntGroups/{huntgroup_id}``
   * - :meth:`api.telephony.huntgroup.details <wxc_sdk.telephony.huntgroup.HuntGroupApi.details>`
        | Get Details for a Hunt Group
        | ``GET /telephony/config/locations/{location_id}/huntGroups/{huntgroup_id}``
   * - :meth:`api.telephony.huntgroup.forward_available_phone_numbers <wxc_sdk.telephony.huntgroup.HuntGroupApi.forward_available_phone_numbers>`
        | Get Hunt Group Call Forward Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/huntGroups/callForwarding/availableNumbers``
   * - :meth:`api.telephony.huntgroup.forwarding.call_forwarding_rule <wxc_sdk.telephony.forwarding.ForwardingApi.call_forwarding_rule>`
        | Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue
        | ``GET /telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding/selectiveRules/{rule_id}``
   * - :meth:`api.telephony.huntgroup.forwarding.create_call_forwarding_rule <wxc_sdk.telephony.forwarding.ForwardingApi.create_call_forwarding_rule>`
        | Create a Selective Call Forwarding Rule feature
        | ``POST /telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding/selectiveRules``
   * - :meth:`api.telephony.huntgroup.forwarding.delete_call_forwarding_rule <wxc_sdk.telephony.forwarding.ForwardingApi.delete_call_forwarding_rule>`
        | Delete a Selective Call Forwarding Rule for the designated feature
        | ``DELETE /telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding/selectiveRules/{rule_id}``
   * - :meth:`api.telephony.huntgroup.forwarding.settings <wxc_sdk.telephony.forwarding.ForwardingApi.settings>`
        | Retrieve Call Forwarding settings for the designated feature including the list of call
        | ``GET /telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding``
   * - :meth:`api.telephony.huntgroup.forwarding.switch_mode_for_call_forwarding <wxc_sdk.telephony.forwarding.ForwardingApi.switch_mode_for_call_forwarding>`
        | Switch Mode for Call Forwarding Settings for an entity
        | ``POST /telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding/actions/switchMode/invoke``
   * - :meth:`api.telephony.huntgroup.forwarding.update <wxc_sdk.telephony.forwarding.ForwardingApi.update>`
        | Update Call Forwarding Settings for a feature
        | ``PUT /telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding``
   * - :meth:`api.telephony.huntgroup.forwarding.update_call_forwarding_rule <wxc_sdk.telephony.forwarding.ForwardingApi.update_call_forwarding_rule>`
        | Update a Selective Call Forwarding Rule's settings for the designated feature
        | ``PUT /telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding/selectiveRules/{rule_id}``
   * - :meth:`api.telephony.huntgroup.list <wxc_sdk.telephony.huntgroup.HuntGroupApi.list>`
        | Read the List of Hunt Groups
        | ``GET /telephony/config/huntGroups``
   * - :meth:`api.telephony.huntgroup.primary_available_phone_numbers <wxc_sdk.telephony.huntgroup.HuntGroupApi.primary_available_phone_numbers>`
        | Get Hunt Group Primary Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/huntGroups/availableNumbers``
   * - :meth:`api.telephony.huntgroup.update <wxc_sdk.telephony.huntgroup.HuntGroupApi.update>`
        | Update a Hunt Group
        | ``PUT /telephony/config/locations/{location_id}/huntGroups/{huntgroup_id}``
   * - :meth:`api.telephony.jobs.activation_emails.errors <wxc_sdk.telephony.jobs.SendActivationEmailApi.errors>`
        | Get Bulk Activation Email Resend Job Errors
        | ``GET /identity/organizations/{org_id}/jobs/sendActivationEmails/{job_id}/errors``
   * - :meth:`api.telephony.jobs.activation_emails.start <wxc_sdk.telephony.jobs.SendActivationEmailApi.start>`
        | Initiate Bulk Activation Email Resend Job
        | ``POST /identity/organizations/{org_id}/jobs/sendActivationEmails``
   * - :meth:`api.telephony.jobs.activation_emails.status <wxc_sdk.telephony.jobs.SendActivationEmailApi.status>`
        | Get Bulk Activation Email Resend Job Status
        | ``GET /identity/organizations/{org_id}/jobs/sendActivationEmails/{job_id}/status``
   * - :meth:`api.telephony.jobs.apply_line_key_templates.apply <wxc_sdk.telephony.jobs.ApplyLineKeyTemplatesJobsApi.apply>`
        | Apply a Line key Template
        | ``POST /telephony/config/jobs/devices/applyLineKeyTemplate``
   * - :meth:`api.telephony.jobs.apply_line_key_templates.errors <wxc_sdk.telephony.jobs.ApplyLineKeyTemplatesJobsApi.errors>`
        | Get job errors for an Apply Line Key Template job
        | ``GET /telephony/config/jobs/devices/applyLineKeyTemplate/{job_id}/errors``
   * - :meth:`api.telephony.jobs.apply_line_key_templates.list <wxc_sdk.telephony.jobs.ApplyLineKeyTemplatesJobsApi.list>`
        | Get List of Apply Line Key Template jobs
        | ``GET /telephony/config/jobs/devices/applyLineKeyTemplate``
   * - :meth:`api.telephony.jobs.apply_line_key_templates.status <wxc_sdk.telephony.jobs.ApplyLineKeyTemplatesJobsApi.status>`
        | Get the job status of an Apply Line Key Template job
        | ``GET /telephony/config/jobs/devices/applyLineKeyTemplate/{job_id}``
   * - :meth:`api.telephony.jobs.call_recording.errors <wxc_sdk.telephony.jobs.CallRecordingJobsApi.errors>`
        | Get Job Errors for a Call Recording Job
        | ``GET /telephony/config/jobs/callRecording/{job_id}/errors``
   * - :meth:`api.telephony.jobs.call_recording.list <wxc_sdk.telephony.jobs.CallRecordingJobsApi.list>`
        | List Call Recording Jobs
        | ``GET /telephony/config/jobs/callRecording``
   * - :meth:`api.telephony.jobs.call_recording.status <wxc_sdk.telephony.jobs.CallRecordingJobsApi.status>`
        | Get the Job Status of a Call Recording Job
        | ``GET /telephony/config/jobs/callRecording/{job_id}``
   * - :meth:`api.telephony.jobs.device_settings.change <wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.change>`
        | Change device settings across organization or locations jobs
        | ``POST /telephony/config/jobs/devices/callDeviceSettings``
   * - :meth:`api.telephony.jobs.device_settings.errors <wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.errors>`
        | List change device settings job errors
        | ``GET /telephony/config/jobs/devices/callDeviceSettings/{job_id}/errors``
   * - :meth:`api.telephony.jobs.device_settings.list <wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.list>`
        | List change device settings jobs
        | ``GET /telephony/config/jobs/devices/callDeviceSettings``
   * - :meth:`api.telephony.jobs.device_settings.status <wxc_sdk.telephony.jobs.DeviceSettingsJobsApi.status>`
        | Get change device settings job status
        | ``GET /telephony/config/jobs/devices/callDeviceSettings/{job_id}``
   * - :meth:`api.telephony.jobs.disable_calling_location.errors <wxc_sdk.telephony.jobs.DisableCallingLocationJobsApi.errors>`
        | Retrieve Errors for a Disable Calling Location Job
        | ``GET /telephony/config/jobs/locations/deleteCallingLocation/{job_id}/errors``
   * - :meth:`api.telephony.jobs.disable_calling_location.initiate <wxc_sdk.telephony.jobs.DisableCallingLocationJobsApi.initiate>`
        | Disable a Location for Webex Calling
        | ``POST /telephony/config/jobs/locations/deleteCallingLocation``
   * - :meth:`api.telephony.jobs.disable_calling_location.list <wxc_sdk.telephony.jobs.DisableCallingLocationJobsApi.list>`
        | Get a List of Disable Calling Location Jobs
        | ``GET /telephony/config/jobs/locations/deleteCallingLocation``
   * - :meth:`api.telephony.jobs.disable_calling_location.pause <wxc_sdk.telephony.jobs.DisableCallingLocationJobsApi.pause>`
        | Pause a Disable Calling Location Job
        | ``POST /telephony/config/jobs/locations/deleteCallingLocation/{job_id}/actions/pause/invoke``
   * - :meth:`api.telephony.jobs.disable_calling_location.resume <wxc_sdk.telephony.jobs.DisableCallingLocationJobsApi.resume>`
        | Resume a Paused Disable Calling Location Job
        | ``POST /telephony/config/jobs/locations/deleteCallingLocation/{job_id}/actions/resume/invoke``
   * - :meth:`api.telephony.jobs.disable_calling_location.status <wxc_sdk.telephony.jobs.DisableCallingLocationJobsApi.status>`
        | Get Disable Calling Location Job Status
        | ``GET /telephony/config/jobs/locations/deleteCallingLocation/{job_id}``
   * - :meth:`api.telephony.jobs.dynamic_device_settings.errors <wxc_sdk.telephony.jobs.UpdateDynamicDeviceSettingsJobsApi.errors>`
        | List Dynamic Device Settings Job Errors
        | ``GET /telephony/config/jobs/devices/dynamicDeviceSettings/{job_id}/errors``
   * - :meth:`api.telephony.jobs.dynamic_device_settings.list <wxc_sdk.telephony.jobs.UpdateDynamicDeviceSettingsJobsApi.list>`
        | List dynamic device settings jobs
        | ``GET /telephony/config/jobs/devices/dynamicDeviceSettings``
   * - :meth:`api.telephony.jobs.dynamic_device_settings.status <wxc_sdk.telephony.jobs.UpdateDynamicDeviceSettingsJobsApi.status>`
        | Get Device Dynamic Settings Job Status
        | ``GET /telephony/config/jobs/devices/dynamicDeviceSettings/{job_id}``
   * - :meth:`api.telephony.jobs.dynamic_device_settings.update_across_org_or_location <wxc_sdk.telephony.jobs.UpdateDynamicDeviceSettingsJobsApi.update_across_org_or_location>`
        | Updates dynamic Device Settings Across Organization Or Location
        | ``POST /telephony/config/jobs/devices/dynamicDeviceSettings``
   * - :meth:`api.telephony.jobs.manage_numbers.abandon <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.abandon>`
        | Abandon the Manage Numbers Job
        | ``POST /telephony/config/jobs/numbers/manageNumbers/{job_id}/actions/abandon/invoke``
   * - :meth:`api.telephony.jobs.manage_numbers.errors <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.errors>`
        | List Manage Numbers Job errors
        | ``GET /telephony/config/jobs/numbers/manageNumbers/{job_id}/errors``
   * - :meth:`api.telephony.jobs.manage_numbers.initiate_job <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.initiate_job>`
        | Initiate Number Jobs
        | ``POST /telephony/config/jobs/numbers/manageNumbers``
   * - :meth:`api.telephony.jobs.manage_numbers.list <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.list>`
        | List Manage Numbers Jobs
        | ``GET /telephony/config/jobs/numbers/manageNumbers``
   * - :meth:`api.telephony.jobs.manage_numbers.pause <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.pause>`
        | Pause the Manage Numbers Job
        | ``POST /telephony/config/jobs/numbers/manageNumbers/{job_id}/actions/pause/invoke``
   * - :meth:`api.telephony.jobs.manage_numbers.resume <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.resume>`
        | Resume the Manage Numbers Job
        | ``POST /telephony/config/jobs/numbers/manageNumbers/{job_id}/actions/resume/invoke``
   * - :meth:`api.telephony.jobs.manage_numbers.status <wxc_sdk.telephony.jobs.ManageNumbersJobsApi.status>`
        | Get Manage Numbers Job Status
        | ``GET /telephony/config/jobs/numbers/manageNumbers/{job_id}``
   * - :meth:`api.telephony.jobs.move_users.abandon <wxc_sdk.telephony.jobs.MoveUsersJobsApi.abandon>`
        | Abandon the Move Users Job
        | ``POST /telephony/config/jobs/person/moveLocation/{job_id}/actions/abandon/invoke``
   * - :meth:`api.telephony.jobs.move_users.errors <wxc_sdk.telephony.jobs.MoveUsersJobsApi.errors>`
        | List Move Users Job errors
        | ``GET /telephony/config/jobs/person/moveLocation/{job_id}/errors``
   * - :meth:`api.telephony.jobs.move_users.list <wxc_sdk.telephony.jobs.MoveUsersJobsApi.list>`
        | List Move Users Jobs
        | ``GET /telephony/config/jobs/person/moveLocation``
   * - :meth:`api.telephony.jobs.move_users.pause <wxc_sdk.telephony.jobs.MoveUsersJobsApi.pause>`
        | Pause the Move Users Job
        | ``POST /telephony/config/jobs/person/moveLocation/{job_id}/actions/pause/invoke``
   * - :meth:`api.telephony.jobs.move_users.resume <wxc_sdk.telephony.jobs.MoveUsersJobsApi.resume>`
        | Resume the Move Users Job
        | ``POST /telephony/config/jobs/person/moveLocation/{job_id}/actions/resume/invoke``
   * - :meth:`api.telephony.jobs.move_users.status <wxc_sdk.telephony.jobs.MoveUsersJobsApi.status>`
        | Get Move Users Job Status
        | ``GET /telephony/config/jobs/person/moveLocation/{job_id}``
   * - :meth:`api.telephony.jobs.move_users.validate_or_initiate <wxc_sdk.telephony.jobs.MoveUsersJobsApi.validate_or_initiate>`
        | Validate or Initiate Move Users Job
        | ``POST /telephony/config/jobs/person/moveLocation``
   * - :meth:`api.telephony.jobs.rebuild_phones.errors <wxc_sdk.telephony.jobs.RebuildPhonesJobsApi.errors>`
        | Get Job Errors for a Rebuild Phones Job
        | ``GET /telephony/config/jobs/devices/rebuildPhones/{job_id}/errors``
   * - :meth:`api.telephony.jobs.rebuild_phones.list <wxc_sdk.telephony.jobs.RebuildPhonesJobsApi.list>`
        | List Rebuild Phones Jobs
        | ``GET /telephony/config/jobs/devices/rebuildPhones``
   * - :meth:`api.telephony.jobs.rebuild_phones.rebuild_phones_configuration <wxc_sdk.telephony.jobs.RebuildPhonesJobsApi.rebuild_phones_configuration>`
        | Rebuild Phones Configuration
        | ``POST /telephony/config/jobs/devices/rebuildPhones``
   * - :meth:`api.telephony.jobs.rebuild_phones.status <wxc_sdk.telephony.jobs.RebuildPhonesJobsApi.status>`
        | Get the Job Status of a Rebuild Phones Job
        | ``GET /telephony/config/jobs/devices/rebuildPhones/{job_id}``
   * - :meth:`api.telephony.jobs.update_routing_prefix.errors <wxc_sdk.telephony.jobs.UpdateRoutingPrefixJobsApi.errors>`
        | Get job errors for update routing prefix job
        | ``GET /telephony/config/jobs/updateRoutingPrefix/{job_id}/errors``
   * - :meth:`api.telephony.jobs.update_routing_prefix.list <wxc_sdk.telephony.jobs.UpdateRoutingPrefixJobsApi.list>`
        | Get a List of Update Routing Prefix jobs
        | ``GET /telephony/config/jobs/updateRoutingPrefix``
   * - :meth:`api.telephony.jobs.update_routing_prefix.status <wxc_sdk.telephony.jobs.UpdateRoutingPrefixJobsApi.status>`
        | Get the job status of Update Routing Prefix job
        | ``GET /telephony/config/jobs/updateRoutingPrefix/{job_id}``
   * - :meth:`api.telephony.location.call_intercept_available_phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.call_intercept_available_phone_numbers>`
        | Get Location Call Intercept Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/callIntercept/availableNumbers``
   * - :meth:`api.telephony.location.change_announcement_language <wxc_sdk.telephony.location.TelephonyLocationApi.change_announcement_language>`
        | Change Announcement Language
        | ``PUT /{location_id}/actions/modifyAnnouncementLanguage/invoke``
   * - :meth:`api.telephony.location.charge_number_available_phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.charge_number_available_phone_numbers>`
        | Get Available Charge Numbers for a Location with Given Criteria
        | ``GET /telephony/config/locations/{location_id}/chargeNumber/availableNumbers``
   * - :meth:`api.telephony.location.create_receptionist_contact_directory <wxc_sdk.telephony.location.TelephonyLocationApi.create_receptionist_contact_directory>`
        | Create a Receptionist Contact Directory
        | ``POST /telephony/config/locations/{location_id}/receptionistContacts/directories``
   * - :meth:`api.telephony.location.delete_receptionist_contact_directory <wxc_sdk.telephony.location.TelephonyLocationApi.delete_receptionist_contact_directory>`
        | Delete a Receptionist Contact Directory
        | ``DELETE /telephony/config/locations/{location_id}/receptionistContacts/directories/{directory_id}``
   * - :meth:`api.telephony.location.details <wxc_sdk.telephony.location.TelephonyLocationApi.details>`
        | Get Location Webex Calling Details
        | ``GET /telephony/config/locations/{location_id}``
   * - :meth:`api.telephony.location.device_settings <wxc_sdk.telephony.location.TelephonyLocationApi.device_settings>`
        | Get device override settings for a location
        | ``GET /telephony/config/locations/{location_id}/devices/settings``
   * - :meth:`api.telephony.location.ecbn_available_phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.ecbn_available_phone_numbers>`
        | Get Location ECBN Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/emergencyCallbackNumber/availableNumbers``
   * - :meth:`api.telephony.location.emergency_services.read_emergency_call_notification <wxc_sdk.telephony.location.emergency_services.LocationEmergencyServicesApi.read_emergency_call_notification>`
        | Get a Location Emergency Call Notification
        | ``GET /telephony/config/locations/{location_id}/emergencyCallNotification``
   * - :meth:`api.telephony.location.emergency_services.update_emergency_call_notification <wxc_sdk.telephony.location.emergency_services.LocationEmergencyServicesApi.update_emergency_call_notification>`
        | Update a location emergency call notification
        | ``PUT /telephony/config/locations/{location_id}/emergencyCallNotification``
   * - :meth:`api.telephony.location.enable_for_calling <wxc_sdk.telephony.location.TelephonyLocationApi.enable_for_calling>`
        | Enable a Location for Webex Calling
        | ``POST /telephony/config/locations``
   * - :meth:`api.telephony.location.generate_password <wxc_sdk.telephony.location.TelephonyLocationApi.generate_password>`
        | Generate example password for Location
        | ``POST /telephony/config/locations/{location_id}/actions/generatePassword/invoke``
   * - :meth:`api.telephony.location.get_call_captions_settings <wxc_sdk.telephony.location.TelephonyLocationApi.get_call_captions_settings>`
        | Get the location call captions settings
        | ``GET /telephony/config/locations/{location_id}/callCaptions``
   * - :meth:`api.telephony.location.intercept.configure <wxc_sdk.telephony.location.intercept.LocationInterceptApi.configure>`
        | Put Location Intercept
        | ``PUT /telephony/config/locations/{location_id}/intercept``
   * - :meth:`api.telephony.location.intercept.read <wxc_sdk.telephony.location.intercept.LocationInterceptApi.read>`
        | Get Location Intercept
        | ``GET /telephony/config/locations/{location_id}/intercept``
   * - :meth:`api.telephony.location.internal_dialing.read <wxc_sdk.telephony.location.internal_dialing.InternalDialingApi.read>`
        | Read the Internal Dialing configuration for a location
        | ``GET /telephony/config/locations/{location_id}/internalDialing``
   * - :meth:`api.telephony.location.internal_dialing.update <wxc_sdk.telephony.location.internal_dialing.InternalDialingApi.update>`
        | Modify the Internal Dialing configuration for a location
        | ``PUT /telephony/config/locations/{location_id}/internalDialing``
   * - :meth:`api.telephony.location.list <wxc_sdk.telephony.location.TelephonyLocationApi.list>`
        | List Locations Webex Calling Details
        | ``GET /telephony/config/locations``
   * - :meth:`api.telephony.location.list_receptionist_contact_directories <wxc_sdk.telephony.location.TelephonyLocationApi.list_receptionist_contact_directories>`
        | Read list of Receptionist Contact Directories
        | ``GET /telephony/config/locations/{location_id}/receptionistContacts/directories``
   * - :meth:`api.telephony.location.modify_receptionist_contact_directory <wxc_sdk.telephony.location.TelephonyLocationApi.modify_receptionist_contact_directory>`
        | Modify a Receptionist Contact Directory
        | ``PUT /telephony/config/locations/{location_id}/receptionistContacts/directories/{directory_id}``
   * - :meth:`api.telephony.location.moh.read <wxc_sdk.telephony.location.moh.LocationMoHApi.read>`
        | Get Music On Hold
        | ``GET /telephony/config/locations/{location_id}/musicOnHold``
   * - :meth:`api.telephony.location.moh.update <wxc_sdk.telephony.location.moh.LocationMoHApi.update>`
        | Update Music On Hold
        | ``PUT /telephony/config/locations/{location_id}/musicOnHold``
   * - :meth:`api.telephony.location.number.add <wxc_sdk.telephony.location.numbers.LocationNumbersApi.add>`
        | Add Phone Numbers to a location
        | ``POST /telephony/config/locations/{location_id}/numbers``
   * - :meth:`api.telephony.location.number.manage_number_state <wxc_sdk.telephony.location.numbers.LocationNumbersApi.manage_number_state>`
        | Manage Number State in a location
        | ``PUT /telephony/config/locations/{location_id}/numbers``
   * - :meth:`api.telephony.location.number.remove <wxc_sdk.telephony.location.numbers.LocationNumbersApi.remove>`
        | Remove phone numbers from a location
        | ``DELETE /telephony/config/locations/{location_id}/numbers``
   * - :meth:`api.telephony.location.permissions_out.configure <wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.configure>`
        | Configure Outgoing Calling Permissions Settings
        | ``PUT /telephony/config/locations/{entity_id}/outgoingPermission``
   * - :meth:`api.telephony.location.permissions_out.digit_patterns.create <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.create>`
        | Create Digit Patterns
        | ``POST /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.location.permissions_out.digit_patterns.delete <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.delete>`
        | Delete a Digit Pattern
        | ``DELETE /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}``
   * - :meth:`api.telephony.location.permissions_out.digit_patterns.delete_all <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.delete_all>`
        | Delete all Digit Patterns
        | ``DELETE /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.location.permissions_out.digit_patterns.details <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.details>`
        | Retrieve Digit Pattern Details
        | ``GET /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}``
   * - :meth:`api.telephony.location.permissions_out.digit_patterns.get_digit_patterns <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.get_digit_patterns>`
        | Retrieve Digit Patterns
        | ``GET /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.location.permissions_out.digit_patterns.update <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.update>`
        | Modify Digit Patterns
        | ``PUT /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{id}``
   * - :meth:`api.telephony.location.permissions_out.digit_patterns.update_category_control_settings <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.update_category_control_settings>`
        | Modify the Digit Pattern Category Control Settings for the entity
        | ``PUT /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.location.permissions_out.read <wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.read>`
        | Retrieve Outgoing Calling Permissions Settings
        | ``GET /telephony/config/locations/{entity_id}/outgoingPermission``
   * - :meth:`api.telephony.location.permissions_out.transfer_numbers.configure <wxc_sdk.person_settings.permissions_out.TransferNumbersApi.configure>`
        | Modify Transfer Numbers Settings for an entity
        | ``PUT /telephony/config/locations/{entity_id}/outgoingPermission/autoTransferNumbers``
   * - :meth:`api.telephony.location.permissions_out.transfer_numbers.read <wxc_sdk.person_settings.permissions_out.TransferNumbersApi.read>`
        | Retrieve Transfer Numbers Settings
        | ``GET /telephony/config/locations/{entity_id}/outgoingPermission/autoTransferNumbers``
   * - :meth:`api.telephony.location.phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.phone_numbers>`
        | Get Available Phone Numbers for a Location with Given Criteria
        | ``GET /telephony/config/locations/{location_id}/availableNumbers``
   * - :meth:`api.telephony.location.phone_numbers_available_for_external_caller_id <wxc_sdk.telephony.location.TelephonyLocationApi.phone_numbers_available_for_external_caller_id>`
        | Get the List of Phone Numbers Available for External Caller ID
        | ``GET /telephony/config/locations/{location_id}/externalCallerId/availableNumbers``
   * - :meth:`api.telephony.location.read_ecbn <wxc_sdk.telephony.location.TelephonyLocationApi.read_ecbn>`
        | Get a Location Emergency callback number
        | ``GET /telephony/config/locations/{location_id}/features/emergencyCallbackNumber``
   * - :meth:`api.telephony.location.receptionist_contact_directory_details <wxc_sdk.telephony.location.TelephonyLocationApi.receptionist_contact_directory_details>`
        | Get details for a Receptionist Contact Directory
        | ``GET /telephony/config/locations/{location_id}/receptionistContacts/directories/{directory_id}``
   * - :meth:`api.telephony.location.receptionist_contacts_directory.create <wxc_sdk.telephony.location.receptionist_contacts.ReceptionistContactsDirectoryApi.create>`
        | Creates a new Receptionist Contact Directory for a location
        | ``POST /telephony/config/locations/{location_id}/receptionistContacts/directories``
   * - :meth:`api.telephony.location.receptionist_contacts_directory.delete <wxc_sdk.telephony.location.receptionist_contacts.ReceptionistContactsDirectoryApi.delete>`
        | Delete a Receptionist Contact Directory from a location
        | ``DELETE /telephony/config/locations/{location_id}/receptionistContacts/directories``
   * - :meth:`api.telephony.location.receptionist_contacts_directory.list <wxc_sdk.telephony.location.receptionist_contacts.ReceptionistContactsDirectoryApi.list>`
        | List all Receptionist Contact Directories for a location
        | ``GET /telephony/config/locations/{location_id}/receptionistContacts/directories``
   * - :meth:`api.telephony.location.safe_delete_check_before_disabling_calling_location <wxc_sdk.telephony.location.TelephonyLocationApi.safe_delete_check_before_disabling_calling_location>`
        | Safe Delete Check Before Disabling a Location for Webex Calling
        | ``POST /telephony/config/locations/{location_id}/actions/precheckForDeletion/invoke``
   * - :meth:`api.telephony.location.update <wxc_sdk.telephony.location.TelephonyLocationApi.update>`
        | Update Location Webex Calling Details
        | ``PUT /telephony/config/locations/{location_id}``
   * - :meth:`api.telephony.location.update_call_captions_settings <wxc_sdk.telephony.location.TelephonyLocationApi.update_call_captions_settings>`
        | Update the location call captions settings
        | ``PUT /telephony/config/locations/{location_id}/callCaptions``
   * - :meth:`api.telephony.location.update_ecbn <wxc_sdk.telephony.location.TelephonyLocationApi.update_ecbn>`
        | Update a Location Emergency callback number
        | ``PUT /telephony/config/locations/{location_id}/features/emergencyCallbackNumber``
   * - :meth:`api.telephony.location.validate_extensions <wxc_sdk.telephony.location.TelephonyLocationApi.validate_extensions>`
        | Validate Extensions
        | ``POST /telephony/config/locations/{location_id}/actions/validateExtensions/invoke``
   * - :meth:`api.telephony.location.voicemail.read <wxc_sdk.telephony.location.vm.LocationVoicemailSettingsApi.read>`
        | Get Location Voicemail
        | ``GET /telephony/config/locations/{location_id}/voicemail``
   * - :meth:`api.telephony.location.voicemail.update <wxc_sdk.telephony.location.vm.LocationVoicemailSettingsApi.update>`
        | Update Location Voicemail
        | ``PUT /telephony/config/locations/{location_id}/voicemail``
   * - :meth:`api.telephony.location.webex_go_available_phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.webex_go_available_phone_numbers>`
        | Get Webex Go Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/webexGo/availableNumbers``
   * - :meth:`api.telephony.locations.call_intercept_available_phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.call_intercept_available_phone_numbers>`
        | Get Location Call Intercept Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/callIntercept/availableNumbers``
   * - :meth:`api.telephony.locations.change_announcement_language <wxc_sdk.telephony.location.TelephonyLocationApi.change_announcement_language>`
        | Change Announcement Language
        | ``PUT /{location_id}/actions/modifyAnnouncementLanguage/invoke``
   * - :meth:`api.telephony.locations.charge_number_available_phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.charge_number_available_phone_numbers>`
        | Get Available Charge Numbers for a Location with Given Criteria
        | ``GET /telephony/config/locations/{location_id}/chargeNumber/availableNumbers``
   * - :meth:`api.telephony.locations.create_receptionist_contact_directory <wxc_sdk.telephony.location.TelephonyLocationApi.create_receptionist_contact_directory>`
        | Create a Receptionist Contact Directory
        | ``POST /telephony/config/locations/{location_id}/receptionistContacts/directories``
   * - :meth:`api.telephony.locations.delete_receptionist_contact_directory <wxc_sdk.telephony.location.TelephonyLocationApi.delete_receptionist_contact_directory>`
        | Delete a Receptionist Contact Directory
        | ``DELETE /telephony/config/locations/{location_id}/receptionistContacts/directories/{directory_id}``
   * - :meth:`api.telephony.locations.details <wxc_sdk.telephony.location.TelephonyLocationApi.details>`
        | Get Location Webex Calling Details
        | ``GET /telephony/config/locations/{location_id}``
   * - :meth:`api.telephony.locations.device_settings <wxc_sdk.telephony.location.TelephonyLocationApi.device_settings>`
        | Get device override settings for a location
        | ``GET /telephony/config/locations/{location_id}/devices/settings``
   * - :meth:`api.telephony.locations.ecbn_available_phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.ecbn_available_phone_numbers>`
        | Get Location ECBN Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/emergencyCallbackNumber/availableNumbers``
   * - :meth:`api.telephony.locations.emergency_services.read_emergency_call_notification <wxc_sdk.telephony.location.emergency_services.LocationEmergencyServicesApi.read_emergency_call_notification>`
        | Get a Location Emergency Call Notification
        | ``GET /telephony/config/locations/{location_id}/emergencyCallNotification``
   * - :meth:`api.telephony.locations.emergency_services.update_emergency_call_notification <wxc_sdk.telephony.location.emergency_services.LocationEmergencyServicesApi.update_emergency_call_notification>`
        | Update a location emergency call notification
        | ``PUT /telephony/config/locations/{location_id}/emergencyCallNotification``
   * - :meth:`api.telephony.locations.enable_for_calling <wxc_sdk.telephony.location.TelephonyLocationApi.enable_for_calling>`
        | Enable a Location for Webex Calling
        | ``POST /telephony/config/locations``
   * - :meth:`api.telephony.locations.generate_password <wxc_sdk.telephony.location.TelephonyLocationApi.generate_password>`
        | Generate example password for Location
        | ``POST /telephony/config/locations/{location_id}/actions/generatePassword/invoke``
   * - :meth:`api.telephony.locations.get_call_captions_settings <wxc_sdk.telephony.location.TelephonyLocationApi.get_call_captions_settings>`
        | Get the location call captions settings
        | ``GET /telephony/config/locations/{location_id}/callCaptions``
   * - :meth:`api.telephony.locations.intercept.configure <wxc_sdk.telephony.location.intercept.LocationInterceptApi.configure>`
        | Put Location Intercept
        | ``PUT /telephony/config/locations/{location_id}/intercept``
   * - :meth:`api.telephony.locations.intercept.read <wxc_sdk.telephony.location.intercept.LocationInterceptApi.read>`
        | Get Location Intercept
        | ``GET /telephony/config/locations/{location_id}/intercept``
   * - :meth:`api.telephony.locations.internal_dialing.read <wxc_sdk.telephony.location.internal_dialing.InternalDialingApi.read>`
        | Read the Internal Dialing configuration for a location
        | ``GET /telephony/config/locations/{location_id}/internalDialing``
   * - :meth:`api.telephony.locations.internal_dialing.update <wxc_sdk.telephony.location.internal_dialing.InternalDialingApi.update>`
        | Modify the Internal Dialing configuration for a location
        | ``PUT /telephony/config/locations/{location_id}/internalDialing``
   * - :meth:`api.telephony.locations.list <wxc_sdk.telephony.location.TelephonyLocationApi.list>`
        | List Locations Webex Calling Details
        | ``GET /telephony/config/locations``
   * - :meth:`api.telephony.locations.list_receptionist_contact_directories <wxc_sdk.telephony.location.TelephonyLocationApi.list_receptionist_contact_directories>`
        | Read list of Receptionist Contact Directories
        | ``GET /telephony/config/locations/{location_id}/receptionistContacts/directories``
   * - :meth:`api.telephony.locations.modify_receptionist_contact_directory <wxc_sdk.telephony.location.TelephonyLocationApi.modify_receptionist_contact_directory>`
        | Modify a Receptionist Contact Directory
        | ``PUT /telephony/config/locations/{location_id}/receptionistContacts/directories/{directory_id}``
   * - :meth:`api.telephony.locations.moh.read <wxc_sdk.telephony.location.moh.LocationMoHApi.read>`
        | Get Music On Hold
        | ``GET /telephony/config/locations/{location_id}/musicOnHold``
   * - :meth:`api.telephony.locations.moh.update <wxc_sdk.telephony.location.moh.LocationMoHApi.update>`
        | Update Music On Hold
        | ``PUT /telephony/config/locations/{location_id}/musicOnHold``
   * - :meth:`api.telephony.locations.number.add <wxc_sdk.telephony.location.numbers.LocationNumbersApi.add>`
        | Add Phone Numbers to a location
        | ``POST /telephony/config/locations/{location_id}/numbers``
   * - :meth:`api.telephony.locations.number.manage_number_state <wxc_sdk.telephony.location.numbers.LocationNumbersApi.manage_number_state>`
        | Manage Number State in a location
        | ``PUT /telephony/config/locations/{location_id}/numbers``
   * - :meth:`api.telephony.locations.number.remove <wxc_sdk.telephony.location.numbers.LocationNumbersApi.remove>`
        | Remove phone numbers from a location
        | ``DELETE /telephony/config/locations/{location_id}/numbers``
   * - :meth:`api.telephony.locations.permissions_out.configure <wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.configure>`
        | Configure Outgoing Calling Permissions Settings
        | ``PUT /telephony/config/locations/{entity_id}/outgoingPermission``
   * - :meth:`api.telephony.locations.permissions_out.digit_patterns.create <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.create>`
        | Create Digit Patterns
        | ``POST /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.locations.permissions_out.digit_patterns.delete <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.delete>`
        | Delete a Digit Pattern
        | ``DELETE /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}``
   * - :meth:`api.telephony.locations.permissions_out.digit_patterns.delete_all <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.delete_all>`
        | Delete all Digit Patterns
        | ``DELETE /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.locations.permissions_out.digit_patterns.details <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.details>`
        | Retrieve Digit Pattern Details
        | ``GET /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}``
   * - :meth:`api.telephony.locations.permissions_out.digit_patterns.get_digit_patterns <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.get_digit_patterns>`
        | Retrieve Digit Patterns
        | ``GET /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.locations.permissions_out.digit_patterns.update <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.update>`
        | Modify Digit Patterns
        | ``PUT /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{id}``
   * - :meth:`api.telephony.locations.permissions_out.digit_patterns.update_category_control_settings <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.update_category_control_settings>`
        | Modify the Digit Pattern Category Control Settings for the entity
        | ``PUT /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.locations.permissions_out.read <wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.read>`
        | Retrieve Outgoing Calling Permissions Settings
        | ``GET /telephony/config/locations/{entity_id}/outgoingPermission``
   * - :meth:`api.telephony.locations.permissions_out.transfer_numbers.configure <wxc_sdk.person_settings.permissions_out.TransferNumbersApi.configure>`
        | Modify Transfer Numbers Settings for an entity
        | ``PUT /telephony/config/locations/{entity_id}/outgoingPermission/autoTransferNumbers``
   * - :meth:`api.telephony.locations.permissions_out.transfer_numbers.read <wxc_sdk.person_settings.permissions_out.TransferNumbersApi.read>`
        | Retrieve Transfer Numbers Settings
        | ``GET /telephony/config/locations/{entity_id}/outgoingPermission/autoTransferNumbers``
   * - :meth:`api.telephony.locations.phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.phone_numbers>`
        | Get Available Phone Numbers for a Location with Given Criteria
        | ``GET /telephony/config/locations/{location_id}/availableNumbers``
   * - :meth:`api.telephony.locations.phone_numbers_available_for_external_caller_id <wxc_sdk.telephony.location.TelephonyLocationApi.phone_numbers_available_for_external_caller_id>`
        | Get the List of Phone Numbers Available for External Caller ID
        | ``GET /telephony/config/locations/{location_id}/externalCallerId/availableNumbers``
   * - :meth:`api.telephony.locations.read_ecbn <wxc_sdk.telephony.location.TelephonyLocationApi.read_ecbn>`
        | Get a Location Emergency callback number
        | ``GET /telephony/config/locations/{location_id}/features/emergencyCallbackNumber``
   * - :meth:`api.telephony.locations.receptionist_contact_directory_details <wxc_sdk.telephony.location.TelephonyLocationApi.receptionist_contact_directory_details>`
        | Get details for a Receptionist Contact Directory
        | ``GET /telephony/config/locations/{location_id}/receptionistContacts/directories/{directory_id}``
   * - :meth:`api.telephony.locations.receptionist_contacts_directory.create <wxc_sdk.telephony.location.receptionist_contacts.ReceptionistContactsDirectoryApi.create>`
        | Creates a new Receptionist Contact Directory for a location
        | ``POST /telephony/config/locations/{location_id}/receptionistContacts/directories``
   * - :meth:`api.telephony.locations.receptionist_contacts_directory.delete <wxc_sdk.telephony.location.receptionist_contacts.ReceptionistContactsDirectoryApi.delete>`
        | Delete a Receptionist Contact Directory from a location
        | ``DELETE /telephony/config/locations/{location_id}/receptionistContacts/directories``
   * - :meth:`api.telephony.locations.receptionist_contacts_directory.list <wxc_sdk.telephony.location.receptionist_contacts.ReceptionistContactsDirectoryApi.list>`
        | List all Receptionist Contact Directories for a location
        | ``GET /telephony/config/locations/{location_id}/receptionistContacts/directories``
   * - :meth:`api.telephony.locations.safe_delete_check_before_disabling_calling_location <wxc_sdk.telephony.location.TelephonyLocationApi.safe_delete_check_before_disabling_calling_location>`
        | Safe Delete Check Before Disabling a Location for Webex Calling
        | ``POST /telephony/config/locations/{location_id}/actions/precheckForDeletion/invoke``
   * - :meth:`api.telephony.locations.update <wxc_sdk.telephony.location.TelephonyLocationApi.update>`
        | Update Location Webex Calling Details
        | ``PUT /telephony/config/locations/{location_id}``
   * - :meth:`api.telephony.locations.update_call_captions_settings <wxc_sdk.telephony.location.TelephonyLocationApi.update_call_captions_settings>`
        | Update the location call captions settings
        | ``PUT /telephony/config/locations/{location_id}/callCaptions``
   * - :meth:`api.telephony.locations.update_ecbn <wxc_sdk.telephony.location.TelephonyLocationApi.update_ecbn>`
        | Update a Location Emergency callback number
        | ``PUT /telephony/config/locations/{location_id}/features/emergencyCallbackNumber``
   * - :meth:`api.telephony.locations.validate_extensions <wxc_sdk.telephony.location.TelephonyLocationApi.validate_extensions>`
        | Validate Extensions
        | ``POST /telephony/config/locations/{location_id}/actions/validateExtensions/invoke``
   * - :meth:`api.telephony.locations.voicemail.read <wxc_sdk.telephony.location.vm.LocationVoicemailSettingsApi.read>`
        | Get Location Voicemail
        | ``GET /telephony/config/locations/{location_id}/voicemail``
   * - :meth:`api.telephony.locations.voicemail.update <wxc_sdk.telephony.location.vm.LocationVoicemailSettingsApi.update>`
        | Update Location Voicemail
        | ``PUT /telephony/config/locations/{location_id}/voicemail``
   * - :meth:`api.telephony.locations.webex_go_available_phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.webex_go_available_phone_numbers>`
        | Get Webex Go Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/webexGo/availableNumbers``
   * - :meth:`api.telephony.ms_teams.configure <wxc_sdk.person_settings.msteams.OrgMSTeamsSettingApi.configure>`
        | Update an Organization's MS Teams Setting
        | ``PUT /telephony/config/settings/msTeams``
   * - :meth:`api.telephony.ms_teams.read <wxc_sdk.person_settings.msteams.OrgMSTeamsSettingApi.read>`
        | Get an Organization's MS Teams Settings
        | ``GET /telephony/config/settings/msTeams``
   * - :meth:`api.telephony.operating_modes.available_operating_modes <wxc_sdk.telephony.operating_modes.OperatingModesApi.available_operating_modes>`
        | Retrieve the List of Available Operating Modes in a Location
        | ``GET /telephony/config/locations/{location_id}/operatingModes/availableOperatingModes``
   * - :meth:`api.telephony.operating_modes.call_forward_available_phone_numbers <wxc_sdk.telephony.operating_modes.OperatingModesApi.call_forward_available_phone_numbers>`
        | Get Operating Mode Call Forward Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/operatingModes/callForwarding/availableNumbers``
   * - :meth:`api.telephony.operating_modes.create <wxc_sdk.telephony.operating_modes.OperatingModesApi.create>`
        | Create an Operating Mode
        | ``POST /telephony/config/operatingModes``
   * - :meth:`api.telephony.operating_modes.delete <wxc_sdk.telephony.operating_modes.OperatingModesApi.delete>`
        | Delete an Operating Mode
        | ``DELETE /telephony/config/operatingModes/{mode_id}``
   * - :meth:`api.telephony.operating_modes.details <wxc_sdk.telephony.operating_modes.OperatingModesApi.details>`
        | Get Details for an Operating Mode
        | ``GET /telephony/config/operatingModes/{mode_id}``
   * - :meth:`api.telephony.operating_modes.holiday_create <wxc_sdk.telephony.operating_modes.OperatingModesApi.holiday_create>`
        | Create an Operating Mode Holiday
        | ``POST /telephony/config/operatingModes/{mode_id}/holidays``
   * - :meth:`api.telephony.operating_modes.holiday_delete <wxc_sdk.telephony.operating_modes.OperatingModesApi.holiday_delete>`
        | Delete an Operating Mode Holiday
        | ``DELETE /telephony/config/operatingModes/{mode_id}/holidays/{holiday_id}``
   * - :meth:`api.telephony.operating_modes.holiday_details <wxc_sdk.telephony.operating_modes.OperatingModesApi.holiday_details>`
        | Get details for an Operating Mode Holiday
        | ``GET /telephony/config/operatingModes/{mode_id}/holidays/{holiday_id}``
   * - :meth:`api.telephony.operating_modes.holiday_update <wxc_sdk.telephony.operating_modes.OperatingModesApi.holiday_update>`
        | Modify an Operating Mode Holiday
        | ``PUT /telephony/config/operatingModes/{mode_id}/holidays/{holiday_id}``
   * - :meth:`api.telephony.operating_modes.list <wxc_sdk.telephony.operating_modes.OperatingModesApi.list>`
        | Read the List of Operating Modes
        | ``GET /telephony/config/operatingModes``
   * - :meth:`api.telephony.operating_modes.update <wxc_sdk.telephony.operating_modes.OperatingModesApi.update>`
        | Modify an Operating Mode
        | ``PUT /telephony/config/operatingModes/{mode_id}``
   * - :meth:`api.telephony.organisation_access_codes.create <wxc_sdk.telephony.org_access_codes.OrganisationAccessCodesApi.create>`
        | Create Access Codes for an Organisation
        | ``POST /telephony/config/outgoingPermission/accessCodes``
   * - :meth:`api.telephony.organisation_access_codes.delete <wxc_sdk.telephony.org_access_codes.OrganisationAccessCodesApi.delete>`
        | Delete Outgoing Permission Access Code for an Organisation
        | ``PUT /telephony/config/outgoingPermission/accessCodes``
   * - :meth:`api.telephony.organisation_access_codes.list <wxc_sdk.telephony.org_access_codes.OrganisationAccessCodesApi.list>`
        | Retrieve the organisation's access codes
        | ``GET /telephony/config/outgoingPermission/accessCodes``
   * - :meth:`api.telephony.organisation_voicemail.read <wxc_sdk.telephony.organisation_vm.OrganisationVoicemailSettingsAPI.read>`
        | Get Voicemail Settings
        | ``GET /telephony/config/voicemail/settings``
   * - :meth:`api.telephony.organisation_voicemail.update <wxc_sdk.telephony.organisation_vm.OrganisationVoicemailSettingsAPI.update>`
        | Update the organization's voicemail settings
        | ``PUT /telephony/config/voicemail/settings``
   * - :meth:`api.telephony.paging.create <wxc_sdk.telephony.paging.PagingApi.create>`
        | Create a new Paging Group
        | ``POST /telephony/config/locations/{location_id}/paging``
   * - :meth:`api.telephony.paging.delete_paging <wxc_sdk.telephony.paging.PagingApi.delete_paging>`
        | Delete a Paging Group
        | ``DELETE /telephony/config/locations/{location_id}/paging/{paging_id}``
   * - :meth:`api.telephony.paging.details <wxc_sdk.telephony.paging.PagingApi.details>`
        | Get Details for a Paging Group
        | ``GET /telephony/config/locations/{location_id}/paging/{paging_id}``
   * - :meth:`api.telephony.paging.list <wxc_sdk.telephony.paging.PagingApi.list>`
        | Read the List of Paging Groups
        | ``GET /telephony/config/paging``
   * - :meth:`api.telephony.paging.primary_available_phone_numbers <wxc_sdk.telephony.paging.PagingApi.primary_available_phone_numbers>`
        | Get Paging Group Primary Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/paging/availableNumbers``
   * - :meth:`api.telephony.paging.update <wxc_sdk.telephony.paging.PagingApi.update>`
        | Update a Paging Group
        | ``PUT /telephony/config/locations/{location_id}/paging/{paging_id}``
   * - :meth:`api.telephony.permissions_out.configure <wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.configure>`
        | Configure Outgoing Calling Permissions Settings
        | ``PUT /telephony/config/locations/{entity_id}/outgoingPermission``
   * - :meth:`api.telephony.permissions_out.digit_patterns.create <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.create>`
        | Create Digit Patterns
        | ``POST /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.permissions_out.digit_patterns.delete <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.delete>`
        | Delete a Digit Pattern
        | ``DELETE /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}``
   * - :meth:`api.telephony.permissions_out.digit_patterns.delete_all <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.delete_all>`
        | Delete all Digit Patterns
        | ``DELETE /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.permissions_out.digit_patterns.details <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.details>`
        | Retrieve Digit Pattern Details
        | ``GET /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}``
   * - :meth:`api.telephony.permissions_out.digit_patterns.get_digit_patterns <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.get_digit_patterns>`
        | Retrieve Digit Patterns
        | ``GET /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.permissions_out.digit_patterns.update <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.update>`
        | Modify Digit Patterns
        | ``PUT /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{id}``
   * - :meth:`api.telephony.permissions_out.digit_patterns.update_category_control_settings <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.update_category_control_settings>`
        | Modify the Digit Pattern Category Control Settings for the entity
        | ``PUT /telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.permissions_out.read <wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.read>`
        | Retrieve Outgoing Calling Permissions Settings
        | ``GET /telephony/config/locations/{entity_id}/outgoingPermission``
   * - :meth:`api.telephony.permissions_out.transfer_numbers.configure <wxc_sdk.person_settings.permissions_out.TransferNumbersApi.configure>`
        | Modify Transfer Numbers Settings for an entity
        | ``PUT /telephony/config/locations/{entity_id}/outgoingPermission/autoTransferNumbers``
   * - :meth:`api.telephony.permissions_out.transfer_numbers.read <wxc_sdk.person_settings.permissions_out.TransferNumbersApi.read>`
        | Retrieve Transfer Numbers Settings
        | ``GET /telephony/config/locations/{entity_id}/outgoingPermission/autoTransferNumbers``
   * - :meth:`api.telephony.phone_number_details <wxc_sdk.telephony.TelephonyApi.phone_number_details>`
        | get summary (counts) of phone numbers
        | ``GET /telephony/config/numbers``
   * - :meth:`api.telephony.phone_numbers <wxc_sdk.telephony.TelephonyApi.phone_numbers>`
        | Get Phone Numbers for an Organization with Given Criterias
        | ``GET /telephony/config/numbers``
   * - :meth:`api.telephony.pickup.available_agents <wxc_sdk.telephony.callpickup.CallPickupApi.available_agents>`
        | Get available agents from Call Pickups
        | ``GET /telephony/config/locations/{location_id}/callPickups/availableUsers``
   * - :meth:`api.telephony.pickup.create <wxc_sdk.telephony.callpickup.CallPickupApi.create>`
        | Create a Call Pickup
        | ``POST /telephony/config/locations/{location_id}/callPickups``
   * - :meth:`api.telephony.pickup.delete_pickup <wxc_sdk.telephony.callpickup.CallPickupApi.delete_pickup>`
        | Delete a Call Pickup
        | ``DELETE /telephony/config/locations/{location_id}/callPickups/{pickup_id}``
   * - :meth:`api.telephony.pickup.details <wxc_sdk.telephony.callpickup.CallPickupApi.details>`
        | Get Details for a Call Pickup
        | ``GET /telephony/config/locations/{location_id}/callPickups/{pickup_id}``
   * - :meth:`api.telephony.pickup.list <wxc_sdk.telephony.callpickup.CallPickupApi.list>`
        | Read the List of Call Pickups
        | ``GET /telephony/config/locations/{location_id}/callPickups``
   * - :meth:`api.telephony.pickup.update <wxc_sdk.telephony.callpickup.CallPickupApi.update>`
        | Update a Call Pickup
        | ``PUT /telephony/config/locations/{location_id}/callPickups/{pickup_id}``
   * - :meth:`api.telephony.playlist.assigned_locations <wxc_sdk.telephony.playlists.PlayListApi.assigned_locations>`
        | List Playlist Locations
        | ``GET /telephony/config/announcements/playlists/{play_list_id}/locations``
   * - :meth:`api.telephony.playlist.create <wxc_sdk.telephony.playlists.PlayListApi.create>`
        | Create announcement Playlist at organization level
        | ``POST /telephony/config/announcements/playlists``
   * - :meth:`api.telephony.playlist.delete <wxc_sdk.telephony.playlists.PlayListApi.delete>`
        | Delete Announcement Playlist
        | ``DELETE /telephony/config/announcements/playlists/{play_list_id}``
   * - :meth:`api.telephony.playlist.details <wxc_sdk.telephony.playlists.PlayListApi.details>`
        | Get Announcement Playlist
        | ``GET /telephony/config/announcements/playlists/{play_list_id}``
   * - :meth:`api.telephony.playlist.list <wxc_sdk.telephony.playlists.PlayListApi.list>`
        | List Announcement Playlists
        | ``GET /telephony/config/announcements/playlists``
   * - :meth:`api.telephony.playlist.modify <wxc_sdk.telephony.playlists.PlayListApi.modify>`
        | Update Announcement Playlist
        | ``PUT /telephony/config/announcements/playlists/{play_list_id}``
   * - :meth:`api.telephony.playlist.modify_assigned_locations <wxc_sdk.telephony.playlists.PlayListApi.modify_assigned_locations>`
        | Update Playlist Locations
        | ``PUT /telephony/config/announcements/playlists/{play_list_id}/locations``
   * - :meth:`api.telephony.playlist.usage <wxc_sdk.telephony.playlists.PlayListApi.usage>`
        | Get Playlist Usage
        | ``GET /telephony/config/announcements/playlists/{play_list_id}/usage``
   * - :meth:`api.telephony.pnc.read <wxc_sdk.telephony.pnc.PrivateNetworkConnectApi.read>`
        | Get Private Network Connect
        | ``GET /telephony/config/locations/{location_id}/privateNetworkConnect``
   * - :meth:`api.telephony.pnc.update <wxc_sdk.telephony.pnc.PrivateNetworkConnectApi.update>`
        | Get Private Network Connect
        | ``PUT /telephony/config/locations/{location_id}/privateNetworkConnect``
   * - :meth:`api.telephony.prem_pstn.dial_plan.create <wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.create>`
        | Create a Dial Plan for the organization
        | ``POST /telephony/config/premisePstn/dialPlans``
   * - :meth:`api.telephony.prem_pstn.dial_plan.delete_all_patterns <wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.delete_all_patterns>`
        | Delete all dial patterns from the Dial Plan
        | ``PUT /telephony/config/premisePstn/dialPlans/{dial_plan_id}/dialPatterns``
   * - :meth:`api.telephony.prem_pstn.dial_plan.delete_dial_plan <wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.delete_dial_plan>`
        | Delete a Dial Plan for the organization
        | ``DELETE /telephony/config/premisePstn/dialPlans/{dial_plan_id}``
   * - :meth:`api.telephony.prem_pstn.dial_plan.details <wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.details>`
        | Get a Dial Plan for the organization
        | ``GET /telephony/config/premisePstn/dialPlans/{dial_plan_id}``
   * - :meth:`api.telephony.prem_pstn.dial_plan.list <wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.list>`
        | List all Dial Plans for the organization
        | ``GET /telephony/config/premisePstn/dialPlans``
   * - :meth:`api.telephony.prem_pstn.dial_plan.modify_patterns <wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.modify_patterns>`
        | Modify dial patterns for the Dial Plan
        | ``PUT /telephony/config/premisePstn/dialPlans/{dial_plan_id}/dialPatterns``
   * - :meth:`api.telephony.prem_pstn.dial_plan.patterns <wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.patterns>`
        | Read the List of Dial Patterns
        | ``GET /telephony/config/premisePstn/dialPlans/{dial_plan_id}/dialPatterns``
   * - :meth:`api.telephony.prem_pstn.dial_plan.update <wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.update>`
        | Modify a Dial Plan for the organization
        | ``PUT /telephony/config/premisePstn/dialPlans/{dial_plan_id}``
   * - :meth:`api.telephony.prem_pstn.route_group.create <wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.create>`
        | Creates a Route Group for the organization
        | ``POST /telephony/config/premisePstn/routeGroups``
   * - :meth:`api.telephony.prem_pstn.route_group.delete_route_group <wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.delete_route_group>`
        | Remove a Route Group from an Organization based on id
        | ``DELETE /telephony/config/premisePstn/routeGroups/{rg_id}``
   * - :meth:`api.telephony.prem_pstn.route_group.details <wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.details>`
        | Reads a Route Group for the organization based on id
        | ``GET /telephony/config/premisePstn/routeGroups/{rg_id}``
   * - :meth:`api.telephony.prem_pstn.route_group.list <wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.list>`
        | List all Route Groups for an organization
        | ``GET /telephony/config/premisePstn/routeGroups``
   * - :meth:`api.telephony.prem_pstn.route_group.update <wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.update>`
        | Modifies an existing Route Group for an organization based on id
        | ``PUT /telephony/config/premisePstn/routeGroups/{rg_id}``
   * - :meth:`api.telephony.prem_pstn.route_group.usage <wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.usage>`
        | Read the Usage of a Routing Group
        | ``GET /telephony/config/premisePstn/routeGroups/{rg_id}/usage``
   * - :meth:`api.telephony.prem_pstn.route_group.usage_call_to_extension <wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.usage_call_to_extension>`
        | List "Call to" on-premises Extension Locations for a specific route group
        | ``GET /telephony/config/premisePstn/routeGroups/{rg_id}/usageCallToExtension``
   * - :meth:`api.telephony.prem_pstn.route_group.usage_dial_plan <wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.usage_dial_plan>`
        | List Dial Plan Locations for a specific route group
        | ``GET /telephony/config/premisePstn/routeGroups/{rg_id}/usageDialPlan``
   * - :meth:`api.telephony.prem_pstn.route_group.usage_location_pstn <wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.usage_location_pstn>`
        | List PSTN Connection Locations for a specific route group
        | ``GET /telephony/config/premisePstn/routeGroups/{rg_id}/usagePstnConnection``
   * - :meth:`api.telephony.prem_pstn.route_group.usage_route_lists <wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.usage_route_lists>`
        | Read the Route Lists of a Routing Group
        | ``GET /telephony/config/premisePstn/routeGroups/{rg_id}/usageRouteList``
   * - :meth:`api.telephony.prem_pstn.route_list.create <wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.create>`
        | Create a Route List for the organization
        | ``POST /telephony/config/premisePstn/routeLists``
   * - :meth:`api.telephony.prem_pstn.route_list.delete_all_numbers <wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.delete_all_numbers>`
        | 
        | ``PUT /telephony/config/premisePstn/routeLists/{rl_id}/numbers``
   * - :meth:`api.telephony.prem_pstn.route_list.delete_route_list <wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.delete_route_list>`
        | Delete Route List for a Customer
        | ``DELETE /telephony/config/premisePstn/routeLists/{rl_id}``
   * - :meth:`api.telephony.prem_pstn.route_list.details <wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.details>`
        | Get Route List Details
        | ``GET /telephony/config/premisePstn/routeLists/{rl_id}``
   * - :meth:`api.telephony.prem_pstn.route_list.list <wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.list>`
        | List all Route Lists for the organization
        | ``GET /telephony/config/premisePstn/routeLists``
   * - :meth:`api.telephony.prem_pstn.route_list.numbers <wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.numbers>`
        | Get numbers assigned to a Route List
        | ``GET /telephony/config/premisePstn/routeLists/{rl_id}/numbers``
   * - :meth:`api.telephony.prem_pstn.route_list.update <wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.update>`
        | Modify the details for a Route List
        | ``PUT /telephony/config/premisePstn/routeLists/{rl_id}``
   * - :meth:`api.telephony.prem_pstn.route_list.update_numbers <wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.update_numbers>`
        | Modify Numbers for Route List
        | ``PUT /telephony/config/premisePstn/routeLists/{rl_id}/numbers``
   * - :meth:`api.telephony.prem_pstn.trunk.create <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.create>`
        | Create a Trunk for the organization
        | ``POST /telephony/config/premisePstn/trunks``
   * - :meth:`api.telephony.prem_pstn.trunk.delete_trunk <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.delete_trunk>`
        | Delete a Trunk for the organization
        | ``DELETE /telephony/config/premisePstn/trunks/{trunk_id}``
   * - :meth:`api.telephony.prem_pstn.trunk.details <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.details>`
        | Get a Trunk for the organization
        | ``GET /telephony/config/premisePstn/trunks/{trunk_id}``
   * - :meth:`api.telephony.prem_pstn.trunk.list <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.list>`
        | List all Trunks for the organization
        | ``GET /telephony/config/premisePstn/trunks``
   * - :meth:`api.telephony.prem_pstn.trunk.trunk_types <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.trunk_types>`
        | List all TrunkTypes with DeviceTypes for the organization
        | ``GET /telephony/config/premisePstn/trunks/trunkTypes``
   * - :meth:`api.telephony.prem_pstn.trunk.update <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.update>`
        | Modify a Trunk for the organization
        | ``PUT /telephony/config/premisePstn/trunks/{trunk_id}``
   * - :meth:`api.telephony.prem_pstn.trunk.usage <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.usage>`
        | Get Local Gateway Usage Count
        | ``GET /telephony/config/premisePstn/trunks/{trunk_id}/usage``
   * - :meth:`api.telephony.prem_pstn.trunk.usage_call_to_extension <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.usage_call_to_extension>`
        | Get local gateway call to on-premises extension usage for a trunk
        | ``GET /telephony/config/premisePstn/trunks/{trunk_id}/usageCallToExtension``
   * - :meth:`api.telephony.prem_pstn.trunk.usage_dial_plan <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.usage_dial_plan>`
        | Get Local Gateway Dial Plan Usage for a Trunk
        | ``GET /telephony/config/premisePstn/trunks/{trunk_id}/usageDialPlan``
   * - :meth:`api.telephony.prem_pstn.trunk.usage_location_pstn <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.usage_location_pstn>`
        | Get Local Gateway Dial Plan Usage for a Trunk
        | ``GET /telephony/config/premisePstn/trunks/{trunk_id}/usagePstnConnection``
   * - :meth:`api.telephony.prem_pstn.trunk.usage_route_group <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.usage_route_group>`
        | Get Local Gateway Dial Plan Usage for a Trunk
        | ``GET /telephony/config/premisePstn/trunks/{trunk_id}/usageRouteGroup``
   * - :meth:`api.telephony.prem_pstn.trunk.validate_fqdn_and_domain <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.validate_fqdn_and_domain>`
        | Validate Local Gateway FQDN and Domain for the organization trunks
        | ``POST /telephony/config/premisePstn/trunks/actions/fqdnValidation/invoke``
   * - :meth:`api.telephony.prem_pstn.validate_pattern <wxc_sdk.telephony.prem_pstn.PremisePstnApi.validate_pattern>`
        | Validate a Dial Pattern
        | ``POST /telephony/config/premisePstn/actions/validateDialPatterns/invoke``
   * - :meth:`api.telephony.pstn.configure <wxc_sdk.telephony.pstn.PSTNApi.configure>`
        | Setup PSTN Connection for a Location
        | ``PUT /telephony/pstn/locations/{location_id}/connection``
   * - :meth:`api.telephony.pstn.list <wxc_sdk.telephony.pstn.PSTNApi.list>`
        | Retrieve PSTN Connection Options for a Location
        | ``GET /telephony/pstn/locations/{location_id}/connectionOptions``
   * - :meth:`api.telephony.pstn.read <wxc_sdk.telephony.pstn.PSTNApi.read>`
        | Retrieve PSTN Connection for a Location
        | ``GET /telephony/pstn/locations/{location_id}/connection``
   * - :meth:`api.telephony.read_list_of_announcement_languages <wxc_sdk.telephony.TelephonyApi.read_list_of_announcement_languages>`
        | Read the List of Announcement Languages
        | ``GET /telephony/config/announcementLanguages``
   * - :meth:`api.telephony.read_moh <wxc_sdk.telephony.TelephonyApi.read_moh>`
        | Get the organization Music on Hold configuration
        | ``GET /telephony/config/moh/settings``
   * - :meth:`api.telephony.route_choices <wxc_sdk.telephony.TelephonyApi.route_choices>`
        | Read the List of Routing Choices
        | ``GET /telephony/config/routeChoices``
   * - :meth:`api.telephony.schedules.create <wxc_sdk.common.schedules.ScheduleApi.create>`
        | Create a schedule
        | ``POST /telephony/config/locations/{obj_id}/schedules``
   * - :meth:`api.telephony.schedules.delete_schedule <wxc_sdk.common.schedules.ScheduleApi.delete_schedule>`
        | Delete a schedule
        | ``DELETE /telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}``
   * - :meth:`api.telephony.schedules.details <wxc_sdk.common.schedules.ScheduleApi.details>`
        | Get details for a schedule
        | ``GET /telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}``
   * - :meth:`api.telephony.schedules.event_create <wxc_sdk.common.schedules.ScheduleApi.event_create>`
        | Create a schedule event
        | ``POST /telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}/events``
   * - :meth:`api.telephony.schedules.event_delete <wxc_sdk.common.schedules.ScheduleApi.event_delete>`
        | Delete a schedule event
        | ``DELETE /telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}/events/{event_id}``
   * - :meth:`api.telephony.schedules.event_details <wxc_sdk.common.schedules.ScheduleApi.event_details>`
        | Get details for a schedule event
        | ``GET /telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}/events/{event_id}``
   * - :meth:`api.telephony.schedules.event_update <wxc_sdk.common.schedules.ScheduleApi.event_update>`
        | Update a schedule event
        | ``PUT /telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}/events/{event_id}``
   * - :meth:`api.telephony.schedules.list <wxc_sdk.common.schedules.ScheduleApi.list>`
        | List of schedules for a person or location
        | ``GET /telephony/config/locations/{obj_id}/schedules``
   * - :meth:`api.telephony.schedules.update <wxc_sdk.common.schedules.ScheduleApi.update>`
        | Update a schedule
        | ``PUT /telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}``
   * - :meth:`api.telephony.supervisors.assign_unassign_agents <wxc_sdk.telephony.supervisor.SupervisorApi.assign_unassign_agents>`
        | Assign or Unassign Agents to Supervisor
        | ``PUT /telephony/config/supervisors/{supervisor_id}``
   * - :meth:`api.telephony.supervisors.available_agents <wxc_sdk.telephony.supervisor.SupervisorApi.available_agents>`
        | List Available Agents
        | ``GET /telephony/config/supervisors/availableAgents``
   * - :meth:`api.telephony.supervisors.available_supervisors <wxc_sdk.telephony.supervisor.SupervisorApi.available_supervisors>`
        | List Available Supervisors
        | ``GET /telephony/config/supervisors/availableSupervisors``
   * - :meth:`api.telephony.supervisors.create <wxc_sdk.telephony.supervisor.SupervisorApi.create>`
        | Create a Supervisor
        | ``POST /telephony/config/supervisors``
   * - :meth:`api.telephony.supervisors.delete <wxc_sdk.telephony.supervisor.SupervisorApi.delete>`
        | Delete A Supervisor
        | ``DELETE /telephony/config/supervisors/{supervisor_id}``
   * - :meth:`api.telephony.supervisors.delete_bulk <wxc_sdk.telephony.supervisor.SupervisorApi.delete_bulk>`
        | Delete Bulk supervisors
        | ``DELETE /telephony/config/supervisors``
   * - :meth:`api.telephony.supervisors.details <wxc_sdk.telephony.supervisor.SupervisorApi.details>`
        | GET Supervisor Details
        | ``GET /telephony/config/supervisors/{supervisor_id}``
   * - :meth:`api.telephony.supervisors.list <wxc_sdk.telephony.supervisor.SupervisorApi.list>`
        | Get List of Supervisors
        | ``GET /telephony/config/supervisors``
   * - :meth:`api.telephony.supported_devices <wxc_sdk.telephony.TelephonyApi.supported_devices>`
        | Read the List of Supported Devices
        | ``GET /telephony/config/supportedDevices``
   * - :meth:`api.telephony.test_call_routing <wxc_sdk.telephony.TelephonyApi.test_call_routing>`
        | Test Call Routing
        | ``POST /telephony/config/actions/testCallRouting/invoke``
   * - :meth:`api.telephony.ucm_profiles <wxc_sdk.telephony.TelephonyApi.ucm_profiles>`
        | Read the List of UC Manager Profiles
        | ``GET /telephony/config/callingProfiles``
   * - :meth:`api.telephony.update_call_captions_settings <wxc_sdk.telephony.TelephonyApi.update_call_captions_settings>`
        | Update the organization call captions settings
        | ``PUT /telephony/config/callCaptions``
   * - :meth:`api.telephony.update_moh <wxc_sdk.telephony.TelephonyApi.update_moh>`
        | Update the organization Music on Hold configuration
        | ``PUT /telephony/config/moh/settings``
   * - :meth:`api.telephony.validate_extensions <wxc_sdk.telephony.TelephonyApi.validate_extensions>`
        | Validate the List of Extensions
        | ``POST /telephony/config/actions/validateExtensions/invoke``
   * - :meth:`api.telephony.validate_phone_numbers <wxc_sdk.telephony.TelephonyApi.validate_phone_numbers>`
        | Validate phone numbers
        | ``POST /telephony/config/actions/validateNumbers/invoke``
   * - :meth:`api.telephony.virtual_extensions.create_extension <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.create_extension>`
        | Create a Virtual Extension
        | ``POST /telephony/config/virtualExtensions``
   * - :meth:`api.telephony.virtual_extensions.create_range <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.create_range>`
        | Create a Virtual Extension Range
        | ``POST /telephony/config/virtualExtensionRanges``
   * - :meth:`api.telephony.virtual_extensions.delete_extension <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.delete_extension>`
        | Delete a Virtual Extension
        | ``DELETE /telephony/config/virtualExtensions/{extension_id}``
   * - :meth:`api.telephony.virtual_extensions.delete_range <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.delete_range>`
        | Delete a Virtual Extension Range
        | ``DELETE /telephony/config/virtualExtensionRanges/{extension_range_id}``
   * - :meth:`api.telephony.virtual_extensions.details_extension <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.details_extension>`
        | Get a Virtual Extension
        | ``GET /telephony/config/virtualExtensions/{extension_id}``
   * - :meth:`api.telephony.virtual_extensions.details_range <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.details_range>`
        | Get details of a Virtual Extension Range
        | ``GET /telephony/config/virtualExtensionRanges/{extension_range_id}``
   * - :meth:`api.telephony.virtual_extensions.get_extension_settings <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.get_extension_settings>`
        | Get Virtual extension settings
        | ``GET /telephony/config/virtualExtensions/settings``
   * - :meth:`api.telephony.virtual_extensions.list_extensions <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.list_extensions>`
        | Read the List of Virtual Extensions
        | ``GET /telephony/config/virtualExtensions``
   * - :meth:`api.telephony.virtual_extensions.list_range <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.list_range>`
        | Get a list of a Virtual Extension Range
        | ``GET /telephony/config/virtualExtensionRanges``
   * - :meth:`api.telephony.virtual_extensions.modify_extension_settings <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.modify_extension_settings>`
        | Modify Virtual Extension Settings
        | ``PUT /telephony/config/virtualExtensions/settings``
   * - :meth:`api.telephony.virtual_extensions.modify_range <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.modify_range>`
        | Modify Virtual Extension Range
        | ``PUT /telephony/config/virtualExtensionRanges/{extension_range_id}``
   * - :meth:`api.telephony.virtual_extensions.update_extension <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.update_extension>`
        | Update a Virtual Extension
        | ``PUT /telephony/config/virtualExtensions/{extension_id}``
   * - :meth:`api.telephony.virtual_extensions.validate_external_phone_number <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.validate_external_phone_number>`
        | Validate an external phone number
        | ``POST /telephony/config/virtualExtensions/actions/validateNumbers/invoke``
   * - :meth:`api.telephony.virtual_extensions.validate_range <wxc_sdk.telephony.virtual_extensions.VirtualExtensionsApi.validate_range>`
        | Validate the prefix and extension pattern for a Virtual Extension Range
        | ``POST /telephony/config/virtualExtensionRanges/actions/validate/invoke``
   * - :meth:`api.telephony.virtual_lines.agent_caller_id.available_caller_ids <wxc_sdk.person_settings.agent_caller_id.AgentCallerIdApi.available_caller_ids>`
        | Retrieve Agent's List of Available Caller IDs
        | ``GET /telephony/config/virtualLines/{entity_id}/agent/availableCallerIds``
   * - :meth:`api.telephony.virtual_lines.agent_caller_id.configure <wxc_sdk.person_settings.agent_caller_id.AgentCallerIdApi.configure>`
        | Modify Agent's Caller ID Information
        | ``PUT /telephony/config/virtualLines/{entity_id}/agent/callerId``
   * - :meth:`api.telephony.virtual_lines.agent_caller_id.read <wxc_sdk.person_settings.agent_caller_id.AgentCallerIdApi.read>`
        | Retrieve Agent's Caller ID Information
        | ``GET /telephony/config/virtualLines/{entity_id}/agent/callerId``
   * - :meth:`api.telephony.virtual_lines.assigned_devices <wxc_sdk.telephony.virtual_line.VirtualLinesApi.assigned_devices>`
        | Get List of Devices assigned for a Virtual Line
        | ``GET /telephony/config/virtualLines/{virtual_line_id}/devices``
   * - :meth:`api.telephony.virtual_lines.available_numbers.available <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.available>`
        | Get Available Phone Numbers
        | ``GET /telephony/config/virtualLines/availableNumbers``
   * - :meth:`api.telephony.virtual_lines.available_numbers.call_forward <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.call_forward>`
        | Get Call Forward Available Phone Numbers
        | ``GET /telephony/config/virtualLines/{entity_id}/callForwarding/availableNumbers``
   * - :meth:`api.telephony.virtual_lines.available_numbers.call_intercept <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.call_intercept>`
        | Get Call Intercept Available Phone Numbers
        | ``GET /callIntercept``
   * - :meth:`api.telephony.virtual_lines.available_numbers.ecbn <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.ecbn>`
        | Get ECBN Available Phone Numbers
        | ``GET /telephony/config/virtualLines/{entity_id}/emergencyCallbackNumber/availableNumbers``
   * - :meth:`api.telephony.virtual_lines.available_numbers.fax_message <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.fax_message>`
        | Get Fax Message Available Phone Numbers
        | ``GET /telephony/config/virtualLines/{entity_id}/faxMessage/availableNumbers``
   * - :meth:`api.telephony.virtual_lines.available_numbers.primary <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.primary>`
        | Get Person Primary Available Phone Numbers
        | ``GET /primary``
   * - :meth:`api.telephony.virtual_lines.available_numbers.secondary <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.secondary>`
        | Get Person Secondary Available Phone Numbers
        | ``GET /secondary``
   * - :meth:`api.telephony.virtual_lines.barge.configure <wxc_sdk.person_settings.barge.BargeApi.configure>`
        | Configure Barge In Settings
        | ``PUT /telephony/config/virtualLines/{entity_id}/bargeIn``
   * - :meth:`api.telephony.virtual_lines.barge.read <wxc_sdk.person_settings.barge.BargeApi.read>`
        | Retrieve Barge In Settings
        | ``GET /telephony/config/virtualLines/{entity_id}/bargeIn``
   * - :meth:`api.telephony.virtual_lines.call_bridge.configure <wxc_sdk.person_settings.callbridge.CallBridgeApi.configure>`
        | Configure Call Bridge Settings
        | ``PUT /telephony/config/virtualLines/{entity_id}/callBridge``
   * - :meth:`api.telephony.virtual_lines.call_bridge.read <wxc_sdk.person_settings.callbridge.CallBridgeApi.read>`
        | Read Call Bridge Settings
        | ``GET /telephony/config/virtualLines/{entity_id}/callBridge``
   * - :meth:`api.telephony.virtual_lines.call_intercept.configure <wxc_sdk.person_settings.call_intercept.CallInterceptApi.configure>`
        | Configure Call Intercept Settings
        | ``PUT /telephony/config/virtualLines/{entity_id}/intercept``
   * - :meth:`api.telephony.virtual_lines.call_intercept.greeting <wxc_sdk.person_settings.call_intercept.CallInterceptApi.greeting>`
        | Configure Call Intercept Greeting
        | ``POST /telephony/config/virtualLines/{entity_id}/intercept/actions/announcementUpload/invoke``
   * - :meth:`api.telephony.virtual_lines.call_intercept.read <wxc_sdk.person_settings.call_intercept.CallInterceptApi.read>`
        | Read Call Intercept Settings
        | ``GET /telephony/config/virtualLines/{entity_id}/intercept``
   * - :meth:`api.telephony.virtual_lines.call_recording.configure <wxc_sdk.person_settings.call_recording.CallRecordingApi.configure>`
        | Configure Call Recording Settings for a entity
        | ``PUT /telephony/config/virtualLines/{entity_id}/callRecording``
   * - :meth:`api.telephony.virtual_lines.call_recording.read <wxc_sdk.person_settings.call_recording.CallRecordingApi.read>`
        | Read Call Recording Settings
        | ``GET /telephony/config/virtualLines/{entity_id}/callRecording``
   * - :meth:`api.telephony.virtual_lines.call_waiting.configure <wxc_sdk.person_settings.call_waiting.CallWaitingApi.configure>`
        | Configure Call Waiting Settings
        | ``PUT /telephony/config/virtualLines/{entity_id}/callWaiting``
   * - :meth:`api.telephony.virtual_lines.call_waiting.read <wxc_sdk.person_settings.call_waiting.CallWaitingApi.read>`
        | Read Call Waiting Settings for
        | ``GET /telephony/config/virtualLines/{entity_id}/callWaiting``
   * - :meth:`api.telephony.virtual_lines.caller_id.configure <wxc_sdk.person_settings.caller_id.CallerIdApi.configure>`
        | Configure a Caller ID Settings
        | ``PUT /telephony/config/virtualLines/{entity_id}/callerId``
   * - :meth:`api.telephony.virtual_lines.caller_id.configure_settings <wxc_sdk.person_settings.caller_id.CallerIdApi.configure_settings>`
        | Configure a Caller ID Settings
        | ``PUT /telephony/config/virtualLines/{entity_id}/callerId``
   * - :meth:`api.telephony.virtual_lines.caller_id.read <wxc_sdk.person_settings.caller_id.CallerIdApi.read>`
        | Retrieve Caller ID Settings
        | ``GET /telephony/config/virtualLines/{entity_id}/callerId``
   * - :meth:`api.telephony.virtual_lines.create <wxc_sdk.telephony.virtual_line.VirtualLinesApi.create>`
        | Create a Virtual Line
        | ``POST /telephony/config/virtualLines``
   * - :meth:`api.telephony.virtual_lines.dect_networks <wxc_sdk.telephony.virtual_line.VirtualLinesApi.dect_networks>`
        | Get List of Dect Networks Handsets for a Virtual Line
        | ``GET /telephony/config/virtualLines/{virtual_line_id}/dectNetworks``
   * - :meth:`api.telephony.virtual_lines.delete <wxc_sdk.telephony.virtual_line.VirtualLinesApi.delete>`
        | Delete a Virtual Line
        | ``DELETE /telephony/config/virtualLines/{virtual_line_id}``
   * - :meth:`api.telephony.virtual_lines.details <wxc_sdk.telephony.virtual_line.VirtualLinesApi.details>`
        | Get Details for a Virtual Line
        | ``GET /telephony/config/virtualLines/{virtual_line_id}``
   * - :meth:`api.telephony.virtual_lines.dnd.configure <wxc_sdk.person_settings.dnd.DndApi.configure>`
        | Configure Do Not Disturb Settings for an entity
        | ``PUT /telephony/config/virtualLines/{entity_id}/doNotDisturb``
   * - :meth:`api.telephony.virtual_lines.dnd.read <wxc_sdk.person_settings.dnd.DndApi.read>`
        | Read Do Not Disturb Settings for an entity
        | ``GET /telephony/config/virtualLines/{entity_id}/doNotDisturb``
   * - :meth:`api.telephony.virtual_lines.ecbn.configure <wxc_sdk.person_settings.ecbn.ECBNApi.configure>`
        | Update an entity's Emergency Callback Number
        | ``PUT /telephony/config/virtualLines/{entity_id}/emergencyCallbackNumber``
   * - :meth:`api.telephony.virtual_lines.ecbn.dependencies <wxc_sdk.person_settings.ecbn.ECBNApi.dependencies>`
        | Retrieve an entity's Emergency Callback Number Dependencies
        | ``GET /telephony/config/virtualLines/{entity_id}/emergencyCallbackNumber/dependencies``
   * - :meth:`api.telephony.virtual_lines.ecbn.read <wxc_sdk.person_settings.ecbn.ECBNApi.read>`
        | Get an entity's Emergency Callback Number
        | ``GET /telephony/config/virtualLines/{entity_id}/emergencyCallbackNumber``
   * - :meth:`api.telephony.virtual_lines.forwarding.configure <wxc_sdk.person_settings.forwarding.PersonForwardingApi.configure>`
        | Configure an Entity's Call Forwarding Settings
        | ``PUT /telephony/config/virtualLines/{entity_id}/callForwarding``
   * - :meth:`api.telephony.virtual_lines.forwarding.read <wxc_sdk.person_settings.forwarding.PersonForwardingApi.read>`
        | Retrieve an entity's Call Forwarding Settings
        | ``GET /telephony/config/virtualLines/{entity_id}/callForwarding``
   * - :meth:`api.telephony.virtual_lines.get_phone_number <wxc_sdk.telephony.virtual_line.VirtualLinesApi.get_phone_number>`
        | Get Phone Number assigned for a Virtual Line
        | ``GET /telephony/config/virtualLines/{virtual_line_id}/number``
   * - :meth:`api.telephony.virtual_lines.list <wxc_sdk.telephony.virtual_line.VirtualLinesApi.list>`
        | List all Virtual Lines for the organization
        | ``GET /telephony/config/virtualLines``
   * - :meth:`api.telephony.virtual_lines.music_on_hold.configure <wxc_sdk.person_settings.moh.MusicOnHoldApi.configure>`
        | Configure Music On Hold Settings for a Personvirtual line, or workspace
        | ``PUT /telephony/config/virtualLines/{entity_id}/musicOnHold``
   * - :meth:`api.telephony.virtual_lines.music_on_hold.read <wxc_sdk.person_settings.moh.MusicOnHoldApi.read>`
        | Retrieve Music On Hold Settings for a Person, virtual line, or workspace
        | ``GET /telephony/config/virtualLines/{entity_id}/musicOnHold``
   * - :meth:`api.telephony.virtual_lines.permissions_in.configure <wxc_sdk.person_settings.permissions_in.IncomingPermissionsApi.configure>`
        | Configure incoming permissions settings
        | ``PUT /telephony/config/virtualLines/{entity_id}/incomingPermission``
   * - :meth:`api.telephony.virtual_lines.permissions_in.read <wxc_sdk.person_settings.permissions_in.IncomingPermissionsApi.read>`
        | Read Incoming Permission Settings
        | ``GET /telephony/config/virtualLines/{entity_id}/incomingPermission``
   * - :meth:`api.telephony.virtual_lines.permissions_out.access_codes.create <wxc_sdk.person_settings.permissions_out.AccessCodesApi.create>`
        | Create new Access codes
        | ``POST /telephony/config/virtualLines/{entity_id}/outgoingPermission/accessCodes``
   * - :meth:`api.telephony.virtual_lines.permissions_out.access_codes.delete <wxc_sdk.person_settings.permissions_out.AccessCodesApi.delete>`
        | Delete Access Code
        | ``DELETE /telephony/config/virtualLines/{entity_id}/outgoingPermission/accessCodes``
   * - :meth:`api.telephony.virtual_lines.permissions_out.access_codes.modify <wxc_sdk.person_settings.permissions_out.AccessCodesApi.modify>`
        | Modify Access Codes
        | ``PUT /telephony/config/virtualLines/{entity_id}/outgoingPermission/accessCodes``
   * - :meth:`api.telephony.virtual_lines.permissions_out.access_codes.read <wxc_sdk.person_settings.permissions_out.AccessCodesApi.read>`
        | Retrieve Access codes
        | ``GET /telephony/config/virtualLines/{entity_id}/outgoingPermission/accessCodes``
   * - :meth:`api.telephony.virtual_lines.permissions_out.configure <wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.configure>`
        | Configure Outgoing Calling Permissions Settings
        | ``PUT /telephony/config/virtualLines/{entity_id}/outgoingPermission``
   * - :meth:`api.telephony.virtual_lines.permissions_out.digit_patterns.create <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.create>`
        | Create Digit Patterns
        | ``POST /telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.virtual_lines.permissions_out.digit_patterns.delete <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.delete>`
        | Delete a Digit Pattern
        | ``DELETE /telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}``
   * - :meth:`api.telephony.virtual_lines.permissions_out.digit_patterns.delete_all <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.delete_all>`
        | Delete all Digit Patterns
        | ``DELETE /telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.virtual_lines.permissions_out.digit_patterns.details <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.details>`
        | Retrieve Digit Pattern Details
        | ``GET /telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}``
   * - :meth:`api.telephony.virtual_lines.permissions_out.digit_patterns.get_digit_patterns <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.get_digit_patterns>`
        | Retrieve Digit Patterns
        | ``GET /telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.virtual_lines.permissions_out.digit_patterns.update <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.update>`
        | Modify Digit Patterns
        | ``PUT /telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns/{id}``
   * - :meth:`api.telephony.virtual_lines.permissions_out.digit_patterns.update_category_control_settings <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.update_category_control_settings>`
        | Modify the Digit Pattern Category Control Settings for the entity
        | ``PUT /telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.telephony.virtual_lines.permissions_out.read <wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.read>`
        | Retrieve Outgoing Calling Permissions Settings
        | ``GET /telephony/config/virtualLines/{entity_id}/outgoingPermission``
   * - :meth:`api.telephony.virtual_lines.permissions_out.transfer_numbers.configure <wxc_sdk.person_settings.permissions_out.TransferNumbersApi.configure>`
        | Modify Transfer Numbers Settings for an entity
        | ``PUT /telephony/config/virtualLines/{entity_id}/outgoingPermission/autoTransferNumbers``
   * - :meth:`api.telephony.virtual_lines.permissions_out.transfer_numbers.read <wxc_sdk.person_settings.permissions_out.TransferNumbersApi.read>`
        | Retrieve Transfer Numbers Settings
        | ``GET /telephony/config/virtualLines/{entity_id}/outgoingPermission/autoTransferNumbers``
   * - :meth:`api.telephony.virtual_lines.privacy.configure <wxc_sdk.person_settings.privacy.PrivacyApi.configure>`
        | Configure an entity's Privacy Settings
        | ``PUT /telephony/config/virtualLines/{entity_id}/privacy``
   * - :meth:`api.telephony.virtual_lines.privacy.read <wxc_sdk.person_settings.privacy.PrivacyApi.read>`
        | Get Privacy Settings for an entity
        | ``GET /telephony/config/virtualLines/{entity_id}/privacy``
   * - :meth:`api.telephony.virtual_lines.push_to_talk.configure <wxc_sdk.person_settings.push_to_talk.PushToTalkApi.configure>`
        | Configure Push-to-Talk Settings for an entity
        | ``PUT /telephony/config/virtualLines/{entity_id}/pushToTalk``
   * - :meth:`api.telephony.virtual_lines.push_to_talk.read <wxc_sdk.person_settings.push_to_talk.PushToTalkApi.read>`
        | Read Push-to-Talk Settings for an entity
        | ``GET /telephony/config/virtualLines/{entity_id}/pushToTalk``
   * - :meth:`api.telephony.virtual_lines.update <wxc_sdk.telephony.virtual_line.VirtualLinesApi.update>`
        | Update a Virtual Line
        | ``PUT /telephony/config/virtualLines/{virtual_line_id}``
   * - :meth:`api.telephony.virtual_lines.update_directory_search <wxc_sdk.telephony.virtual_line.VirtualLinesApi.update_directory_search>`
        | Update Directory search for a Virtual Line
        | ``PUT /telephony/config/virtualLines/{virtual_line_id}/directorySearch``
   * - :meth:`api.telephony.virtual_lines.voicemail.configure <wxc_sdk.person_settings.voicemail.VoicemailApi.configure>`
        | Configure Voicemail Settings for an entity
        | ``PUT /telephony/config/virtualLines/{entity_id}/voicemail``
   * - :meth:`api.telephony.virtual_lines.voicemail.modify_passcode <wxc_sdk.person_settings.voicemail.VoicemailApi.modify_passcode>`
        | Modify an entity's voicemail passcode
        | ``PUT /telephony/config/virtualLines/{entity_id}/voicemail/passcode``
   * - :meth:`api.telephony.virtual_lines.voicemail.read <wxc_sdk.person_settings.voicemail.VoicemailApi.read>`
        | Read Voicemail Settings for an entity
        | ``GET /telephony/config/virtualLines/{entity_id}/voicemail``
   * - :meth:`api.telephony.virtual_lines.voicemail.reset_pin <wxc_sdk.person_settings.voicemail.VoicemailApi.reset_pin>`
        | Reset Voicemail PIN
        | ``POST /telephony/config/virtualLines/{entity_id}/voicemail/actions/resetPin/invoke``
   * - :meth:`api.telephony.voice_messaging.delete <wxc_sdk.telephony.voice_messaging.VoiceMessagingApi.delete>`
        | Delete a specific voicemail message for the user
        | ``DELETE /telephony/voiceMessages/{message_id}``
   * - :meth:`api.telephony.voice_messaging.list <wxc_sdk.telephony.voice_messaging.VoiceMessagingApi.list>`
        | Get the list of all voicemail messages for the user
        | ``GET /telephony/voiceMessages``
   * - :meth:`api.telephony.voice_messaging.mark_as_read <wxc_sdk.telephony.voice_messaging.VoiceMessagingApi.mark_as_read>`
        | Update the voicemail message(s) as read for the user
        | ``POST /telephony/voiceMessages/markAsRead``
   * - :meth:`api.telephony.voice_messaging.mark_as_unread <wxc_sdk.telephony.voice_messaging.VoiceMessagingApi.mark_as_unread>`
        | Update the voicemail message(s) as unread for the user
        | ``POST /telephony/voiceMessages/markAsUnread``
   * - :meth:`api.telephony.voice_messaging.summary <wxc_sdk.telephony.voice_messaging.VoiceMessagingApi.summary>`
        | Get a summary of the voicemail messages for the user
        | ``GET /telephony/voiceMessages/summary``
   * - :meth:`api.telephony.voicemail_groups.available_phone_numbers <wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.available_phone_numbers>`
        | Get Voicemail Group Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/voicemailGroups/availableNumbers``
   * - :meth:`api.telephony.voicemail_groups.create <wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.create>`
        | Create new voicemail group for the given location for a customer
        | ``POST /telephony/config/locations/{location_id}/voicemailGroups``
   * - :meth:`api.telephony.voicemail_groups.delete <wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.delete>`
        | Delete the designated voicemail group
        | ``DELETE /telephony/config/locations/{location_id}/voicemailGroups/{voicemail_group_id}``
   * - :meth:`api.telephony.voicemail_groups.details <wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.details>`
        | Retrieve voicemail group details for a location
        | ``GET /telephony/config/locations/{location_id}/voicemailGroups/{voicemail_group_id}``
   * - :meth:`api.telephony.voicemail_groups.fax_message_available_phone_numbers <wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.fax_message_available_phone_numbers>`
        | Get Voicemail Group Fax Message Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/voicemailGroups/faxMessage/availableNumbers``
   * - :meth:`api.telephony.voicemail_groups.list <wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.list>`
        | List the voicemail group information for the organization
        | ``GET /telephony/config/voicemailGroups``
   * - :meth:`api.telephony.voicemail_groups.update <wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.update>`
        | Modifies the voicemail group location details for a particular location for a customer
        | ``PUT /telephony/config/locations/{location_id}/voicemailGroups/{voicemail_group_id}``
   * - :meth:`api.telephony.voicemail_rules.read <wxc_sdk.telephony.vm_rules.VoicemailRulesApi.read>`
        | Get Voicemail Rules
        | ``GET /telephony/config/voicemail/rules``
   * - :meth:`api.telephony.voicemail_rules.update <wxc_sdk.telephony.vm_rules.VoicemailRulesApi.update>`
        | Update Voicemail Rules
        | ``PUT /telephony/config/voicemail/rules``
   * - :meth:`api.telephony.voiceportal.available_phone_numbers <wxc_sdk.telephony.voiceportal.VoicePortalApi.available_phone_numbers>`
        | Get VoicePortal Available Phone Numbers
        | ``GET /telephony/config/locations/{location_id}/voicePortal/availableNumbers``
   * - :meth:`api.telephony.voiceportal.passcode_rules <wxc_sdk.telephony.voiceportal.VoicePortalApi.passcode_rules>`
        | Get VoicePortal Passcode Rule
        | ``GET /telephony/config/locations/{location_id}/voicePortal/passcodeRules``
   * - :meth:`api.telephony.voiceportal.read <wxc_sdk.telephony.voiceportal.VoicePortalApi.read>`
        | Get VoicePortal
        | ``GET /telephony/config/locations/{location_id}/voicePortal``
   * - :meth:`api.telephony.voiceportal.update <wxc_sdk.telephony.voiceportal.VoicePortalApi.update>`
        | Update VoicePortal
        | ``PUT /telephony/config/locations/{location_id}/voicePortal``
   * - :meth:`api.webhook.create <wxc_sdk.webhook.WebhookApi.create>`
        | Creates a webhook
        | ``POST /webhooks``
   * - :meth:`api.webhook.details <wxc_sdk.webhook.WebhookApi.details>`
        | Get Webhook Details
        | ``GET /webhooks/{webhook_id}``
   * - :meth:`api.webhook.list <wxc_sdk.webhook.WebhookApi.list>`
        | List Webhooks
        | ``GET /webhooks``
   * - :meth:`api.webhook.update <wxc_sdk.webhook.WebhookApi.update>`
        | Updates a webhook, by ID
        | ``PUT /webhooks/{webhook_id}``
   * - :meth:`api.webhook.webhook_delete <wxc_sdk.webhook.WebhookApi.webhook_delete>`
        | Deletes a webhook, by ID
        | ``DELETE /webhooks/{webhook_id}``
   * - :meth:`api.workspace_locations.create <wxc_sdk.workspace_locations.WorkspaceLocationApi.create>`
        | Create a location
        | ``POST /workspaceLocations``
   * - :meth:`api.workspace_locations.delete <wxc_sdk.workspace_locations.WorkspaceLocationApi.delete>`
        | Delete a Workspace Location
        | ``DELETE /workspaceLocations/{location_id}``
   * - :meth:`api.workspace_locations.details <wxc_sdk.workspace_locations.WorkspaceLocationApi.details>`
        | Get a Workspace Location Details
        | ``GET /workspaceLocations/{location_id}``
   * - :meth:`api.workspace_locations.floors.create <wxc_sdk.workspace_locations.WorkspaceLocationFloorApi.create>`
        | Create a Workspace Location Floor
        | ``POST /workspaceLocations/{location_id}/floors``
   * - :meth:`api.workspace_locations.floors.delete <wxc_sdk.workspace_locations.WorkspaceLocationFloorApi.delete>`
        | Delete a Workspace Location Floor
        | ``DELETE /workspaceLocations/{location_id}/floors/{floor_id}``
   * - :meth:`api.workspace_locations.floors.details <wxc_sdk.workspace_locations.WorkspaceLocationFloorApi.details>`
        | Get a Workspace Location Floor Details
        | ``GET /workspaceLocations/{location_id}/floors/{floor_id}``
   * - :meth:`api.workspace_locations.floors.list <wxc_sdk.workspace_locations.WorkspaceLocationFloorApi.list>`
        | :param location_id:
        | ``GET /workspaceLocations/{location_id}/floors``
   * - :meth:`api.workspace_locations.floors.update <wxc_sdk.workspace_locations.WorkspaceLocationFloorApi.update>`
        | Updates details for a floor, by ID
        | ``PUT /workspaceLocations/{location_id}/floors/{floor_id}``
   * - :meth:`api.workspace_locations.list <wxc_sdk.workspace_locations.WorkspaceLocationApi.list>`
        | List workspace locations
        | ``GET /workspaceLocations``
   * - :meth:`api.workspace_locations.update <wxc_sdk.workspace_locations.WorkspaceLocationApi.update>`
        | Update a Workspace Location
        | ``PUT /workspaceLocations/{location_id}``
   * - :meth:`api.workspace_personalization.get_personalization_task <wxc_sdk.workspace_personalization.WorkspacePersonalizationApi.get_personalization_task>`
        | Get Personalization Task
        | ``GET /workspaces/{workspace_id}/personalizationTask``
   * - :meth:`api.workspace_personalization.personalize_a_workspace <wxc_sdk.workspace_personalization.WorkspacePersonalizationApi.personalize_a_workspace>`
        | Personalize a Workspace
        | ``POST /workspaces/{workspace_id}/personalize``
   * - :meth:`api.workspace_settings.anon_calls.configure <wxc_sdk.person_settings.anon_calls.AnonCallsApi.configure>`
        | Modify Anonymous Call Settings for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/anonymousCallReject``
   * - :meth:`api.workspace_settings.anon_calls.read <wxc_sdk.person_settings.anon_calls.AnonCallsApi.read>`
        | Retrieve Anonymous Call Settings for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/anonymousCallReject``
   * - :meth:`api.workspace_settings.available_numbers.available <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.available>`
        | Get Available Phone Numbers
        | ``GET /telephony/config/workspaces/availableNumbers``
   * - :meth:`api.workspace_settings.available_numbers.call_forward <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.call_forward>`
        | Get Call Forward Available Phone Numbers
        | ``GET /telephony/config/workspaces/{entity_id}/callForwarding/availableNumbers``
   * - :meth:`api.workspace_settings.available_numbers.call_intercept <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.call_intercept>`
        | Get Call Intercept Available Phone Numbers
        | ``GET /telephony/config/workspaces/{entity_id}/callIntercept/availableNumbers``
   * - :meth:`api.workspace_settings.available_numbers.ecbn <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.ecbn>`
        | Get ECBN Available Phone Numbers
        | ``GET /telephony/config/workspaces/{entity_id}/emergencyCallbackNumber/availableNumbers``
   * - :meth:`api.workspace_settings.available_numbers.fax_message <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.fax_message>`
        | Get Fax Message Available Phone Numbers
        | ``GET /telephony/config/workspaces/{entity_id}/faxMessage/availableNumbers``
   * - :meth:`api.workspace_settings.available_numbers.primary <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.primary>`
        | Get Person Primary Available Phone Numbers
        | ``GET /primary``
   * - :meth:`api.workspace_settings.available_numbers.secondary <wxc_sdk.person_settings.available_numbers.AvailableNumbersApi.secondary>`
        | Get Person Secondary Available Phone Numbers
        | ``GET /telephony/config/workspaces/{entity_id}/secondary/availableNumbers``
   * - :meth:`api.workspace_settings.barge.configure <wxc_sdk.person_settings.barge.BargeApi.configure>`
        | Configure Barge In Settings
        | ``PUT /telephony/config/workspaces/{entity_id}/bargeIn``
   * - :meth:`api.workspace_settings.barge.read <wxc_sdk.person_settings.barge.BargeApi.read>`
        | Retrieve Barge In Settings
        | ``GET /telephony/config/workspaces/{entity_id}/bargeIn``
   * - :meth:`api.workspace_settings.call_bridge.configure <wxc_sdk.person_settings.callbridge.CallBridgeApi.configure>`
        | Configure Call Bridge Settings
        | ``PUT /telephony/config/workspaces/{entity_id}/callBridge``
   * - :meth:`api.workspace_settings.call_bridge.read <wxc_sdk.person_settings.callbridge.CallBridgeApi.read>`
        | Read Call Bridge Settings
        | ``GET /telephony/config/workspaces/{entity_id}/callBridge``
   * - :meth:`api.workspace_settings.call_intercept.configure <wxc_sdk.person_settings.call_intercept.CallInterceptApi.configure>`
        | Configure Call Intercept Settings
        | ``PUT /workspaces/{entity_id}/features/intercept``
   * - :meth:`api.workspace_settings.call_intercept.greeting <wxc_sdk.person_settings.call_intercept.CallInterceptApi.greeting>`
        | Configure Call Intercept Greeting
        | ``POST /workspaces/{entity_id}/features/intercept/actions/announcementUpload/invoke``
   * - :meth:`api.workspace_settings.call_intercept.read <wxc_sdk.person_settings.call_intercept.CallInterceptApi.read>`
        | Read Call Intercept Settings
        | ``GET /workspaces/{entity_id}/features/intercept``
   * - :meth:`api.workspace_settings.call_policy.configure <wxc_sdk.person_settings.call_policy.CallPolicyApi.configure>`
        | Configure Call Policy Settings for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/callPolicies``
   * - :meth:`api.workspace_settings.call_policy.read <wxc_sdk.person_settings.call_policy.CallPolicyApi.read>`
        | Read Call Policy Settings for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/callPolicies``
   * - :meth:`api.workspace_settings.call_waiting.configure <wxc_sdk.person_settings.call_waiting.CallWaitingApi.configure>`
        | Configure Call Waiting Settings
        | ``PUT /workspaces/{entity_id}/features/callWaiting``
   * - :meth:`api.workspace_settings.call_waiting.read <wxc_sdk.person_settings.call_waiting.CallWaitingApi.read>`
        | Read Call Waiting Settings for
        | ``GET /workspaces/{entity_id}/features/callWaiting``
   * - :meth:`api.workspace_settings.caller_id.configure <wxc_sdk.person_settings.caller_id.CallerIdApi.configure>`
        | Configure a Caller ID Settings
        | ``PUT /workspaces/{entity_id}/features/callerId``
   * - :meth:`api.workspace_settings.caller_id.configure_settings <wxc_sdk.person_settings.caller_id.CallerIdApi.configure_settings>`
        | Configure a Caller ID Settings
        | ``PUT /workspaces/{entity_id}/features/callerId``
   * - :meth:`api.workspace_settings.caller_id.read <wxc_sdk.person_settings.caller_id.CallerIdApi.read>`
        | Retrieve Caller ID Settings
        | ``GET /workspaces/{entity_id}/features/callerId``
   * - :meth:`api.workspace_settings.devices.list <wxc_sdk.workspace_settings.devices.WorkspaceDevicesApi.list>`
        | Get all devices for a workspace
        | ``GET /telephony/config/workspaces/{workspace_id}/devices``
   * - :meth:`api.workspace_settings.devices.list_and_counts <wxc_sdk.workspace_settings.devices.WorkspaceDevicesApi.list_and_counts>`
        | Get all devices for a workspace
        | ``GET /telephony/config/workspaces/{workspace_id}/devices``
   * - :meth:`api.workspace_settings.devices.modify_hoteling <wxc_sdk.workspace_settings.devices.WorkspaceDevicesApi.modify_hoteling>`
        | Modify devices for a workspace
        | ``PUT /telephony/config/workspaces/{workspace_id}/devices``
   * - :meth:`api.workspace_settings.dnd.configure <wxc_sdk.person_settings.dnd.DndApi.configure>`
        | Configure Do Not Disturb Settings for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/doNotDisturb``
   * - :meth:`api.workspace_settings.dnd.read <wxc_sdk.person_settings.dnd.DndApi.read>`
        | Read Do Not Disturb Settings for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/doNotDisturb``
   * - :meth:`api.workspace_settings.ecbn.configure <wxc_sdk.person_settings.ecbn.ECBNApi.configure>`
        | Update an entity's Emergency Callback Number
        | ``PUT /telephony/config/workspaces/{entity_id}/emergencyCallbackNumber``
   * - :meth:`api.workspace_settings.ecbn.dependencies <wxc_sdk.person_settings.ecbn.ECBNApi.dependencies>`
        | Retrieve an entity's Emergency Callback Number Dependencies
        | ``GET /telephony/config/workspaces/{entity_id}/emergencyCallbackNumber/dependencies``
   * - :meth:`api.workspace_settings.ecbn.read <wxc_sdk.person_settings.ecbn.ECBNApi.read>`
        | Get an entity's Emergency Callback Number
        | ``GET /telephony/config/workspaces/{entity_id}/emergencyCallbackNumber``
   * - :meth:`api.workspace_settings.forwarding.configure <wxc_sdk.person_settings.forwarding.PersonForwardingApi.configure>`
        | Configure an Entity's Call Forwarding Settings
        | ``PUT /workspaces/{entity_id}/features/callForwarding``
   * - :meth:`api.workspace_settings.forwarding.read <wxc_sdk.person_settings.forwarding.PersonForwardingApi.read>`
        | Retrieve an entity's Call Forwarding Settings
        | ``GET /workspaces/{entity_id}/features/callForwarding``
   * - :meth:`api.workspace_settings.monitoring.configure <wxc_sdk.person_settings.monitoring.MonitoringApi.configure>`
        | Modify an entity's Monitoring Settings
        | ``PUT /workspaces/{entity_id}/features/monitoring``
   * - :meth:`api.workspace_settings.monitoring.read <wxc_sdk.person_settings.monitoring.MonitoringApi.read>`
        | Retrieve an entity's Monitoring Settings
        | ``GET /workspaces/{entity_id}/features/monitoring``
   * - :meth:`api.workspace_settings.music_on_hold.configure <wxc_sdk.person_settings.moh.MusicOnHoldApi.configure>`
        | Configure Music On Hold Settings for a Personvirtual line, or workspace
        | ``PUT /telephony/config/workspaces/{entity_id}/musicOnHold``
   * - :meth:`api.workspace_settings.music_on_hold.read <wxc_sdk.person_settings.moh.MusicOnHoldApi.read>`
        | Retrieve Music On Hold Settings for a Person, virtual line, or workspace
        | ``GET /telephony/config/workspaces/{entity_id}/musicOnHold``
   * - :meth:`api.workspace_settings.numbers.read <wxc_sdk.workspace_settings.numbers.WorkspaceNumbersApi.read>`
        | List the PSTN phone numbers associated with a specific workspace, by ID, within the organization
        | ``GET /workspaces/{workspace_id}/features/numbers/``
   * - :meth:`api.workspace_settings.numbers.update <wxc_sdk.workspace_settings.numbers.WorkspaceNumbersApi.update>`
        | Assign or Unassign numbers associated with a specific workspace
        | ``PUT /telephony/config/workspaces/{workspace_id}/numbers``
   * - :meth:`api.workspace_settings.permissions_in.configure <wxc_sdk.person_settings.permissions_in.IncomingPermissionsApi.configure>`
        | Configure incoming permissions settings
        | ``PUT /workspaces/{entity_id}/features/incomingPermission``
   * - :meth:`api.workspace_settings.permissions_in.read <wxc_sdk.person_settings.permissions_in.IncomingPermissionsApi.read>`
        | Read Incoming Permission Settings
        | ``GET /workspaces/{entity_id}/features/incomingPermission``
   * - :meth:`api.workspace_settings.permissions_out.access_codes.create <wxc_sdk.person_settings.permissions_out.AccessCodesApi.create>`
        | Create new Access codes
        | ``POST /workspaces/{entity_id}/features/outgoingPermission/accessCodes``
   * - :meth:`api.workspace_settings.permissions_out.access_codes.delete <wxc_sdk.person_settings.permissions_out.AccessCodesApi.delete>`
        | Delete Access Code
        | ``DELETE /workspaces/{entity_id}/features/outgoingPermission/accessCodes``
   * - :meth:`api.workspace_settings.permissions_out.access_codes.modify <wxc_sdk.person_settings.permissions_out.AccessCodesApi.modify>`
        | Modify Access Codes
        | ``PUT /workspaces/{entity_id}/features/outgoingPermission/accessCodes``
   * - :meth:`api.workspace_settings.permissions_out.access_codes.read <wxc_sdk.person_settings.permissions_out.AccessCodesApi.read>`
        | Retrieve Access codes
        | ``GET /workspaces/{entity_id}/features/outgoingPermission/accessCodes``
   * - :meth:`api.workspace_settings.permissions_out.configure <wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.configure>`
        | Configure Outgoing Calling Permissions Settings
        | ``PUT /workspaces/{entity_id}/features/outgoingPermission``
   * - :meth:`api.workspace_settings.permissions_out.digit_patterns.create <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.create>`
        | Create Digit Patterns
        | ``POST /telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.workspace_settings.permissions_out.digit_patterns.delete <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.delete>`
        | Delete a Digit Pattern
        | ``DELETE /telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}``
   * - :meth:`api.workspace_settings.permissions_out.digit_patterns.delete_all <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.delete_all>`
        | Delete all Digit Patterns
        | ``DELETE /telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.workspace_settings.permissions_out.digit_patterns.details <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.details>`
        | Retrieve Digit Pattern Details
        | ``GET /telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}``
   * - :meth:`api.workspace_settings.permissions_out.digit_patterns.get_digit_patterns <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.get_digit_patterns>`
        | Retrieve Digit Patterns
        | ``GET /telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.workspace_settings.permissions_out.digit_patterns.update <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.update>`
        | Modify Digit Patterns
        | ``PUT /telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns/{id}``
   * - :meth:`api.workspace_settings.permissions_out.digit_patterns.update_category_control_settings <wxc_sdk.person_settings.permissions_out.DigitPatternsApi.update_category_control_settings>`
        | Modify the Digit Pattern Category Control Settings for the entity
        | ``PUT /telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns``
   * - :meth:`api.workspace_settings.permissions_out.read <wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.read>`
        | Retrieve Outgoing Calling Permissions Settings
        | ``GET /workspaces/{entity_id}/features/outgoingPermission``
   * - :meth:`api.workspace_settings.permissions_out.transfer_numbers.configure <wxc_sdk.person_settings.permissions_out.TransferNumbersApi.configure>`
        | Modify Transfer Numbers Settings for an entity
        | ``PUT /workspaces/{entity_id}/features/outgoingPermission/autoTransferNumbers``
   * - :meth:`api.workspace_settings.permissions_out.transfer_numbers.read <wxc_sdk.person_settings.permissions_out.TransferNumbersApi.read>`
        | Retrieve Transfer Numbers Settings
        | ``GET /workspaces/{entity_id}/features/outgoingPermission/autoTransferNumbers``
   * - :meth:`api.workspace_settings.priority_alert.configure <wxc_sdk.person_settings.priority_alert.PriorityAlertApi.configure>`
        | Configure Priority Alert Settings for a Workspace
        | ``PUT /telephony/config/workspaces/{entity_id}/priorityAlert``
   * - :meth:`api.workspace_settings.priority_alert.configure_criteria <wxc_sdk.person_settings.priority_alert.PriorityAlertApi.configure_criteria>`
        | Modify Priority Alert Criteria for a Workspace
        | ``PUT /telephony/config/workspaces/{entity_id}/priorityAlert/criteria/{id}``
   * - :meth:`api.workspace_settings.priority_alert.create_criteria <wxc_sdk.person_settings.priority_alert.PriorityAlertApi.create_criteria>`
        | Create Priority Alert Criteria for a Workspace
        | ``POST /telephony/config/workspaces/{entity_id}/priorityAlert/criteria``
   * - :meth:`api.workspace_settings.priority_alert.delete_criteria <wxc_sdk.person_settings.priority_alert.PriorityAlertApi.delete_criteria>`
        | Delete Priority Alert Criteria for a Workspace
        | ``DELETE /telephony/config/workspaces/{entity_id}/priorityAlert/criteria/{id}``
   * - :meth:`api.workspace_settings.priority_alert.read <wxc_sdk.person_settings.priority_alert.PriorityAlertApi.read>`
        | Retrieve Priority Alert Settings for a Workspace
        | ``GET /telephony/config/workspaces/{entity_id}/priorityAlert``
   * - :meth:`api.workspace_settings.priority_alert.read_criteria <wxc_sdk.person_settings.priority_alert.PriorityAlertApi.read_criteria>`
        | Retrieve Priority Alert Criteria for a Workspace
        | ``GET /telephony/config/workspaces/{entity_id}/priorityAlert/criteria/{id}``
   * - :meth:`api.workspace_settings.privacy.configure <wxc_sdk.person_settings.privacy.PrivacyApi.configure>`
        | Configure an entity's Privacy Settings
        | ``PUT /telephony/config/workspaces/{entity_id}/privacy``
   * - :meth:`api.workspace_settings.privacy.read <wxc_sdk.person_settings.privacy.PrivacyApi.read>`
        | Get Privacy Settings for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/privacy``
   * - :meth:`api.workspace_settings.push_to_talk.configure <wxc_sdk.person_settings.push_to_talk.PushToTalkApi.configure>`
        | Configure Push-to-Talk Settings for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/pushToTalk``
   * - :meth:`api.workspace_settings.push_to_talk.read <wxc_sdk.person_settings.push_to_talk.PushToTalkApi.read>`
        | Read Push-to-Talk Settings for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/pushToTalk``
   * - :meth:`api.workspace_settings.selective_accept.configure <wxc_sdk.person_settings.selective_accept.SelectiveAcceptApi.configure>`
        | Modify Selective Accept Settings for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/selectiveAccept``
   * - :meth:`api.workspace_settings.selective_accept.configure_criteria <wxc_sdk.person_settings.selective_accept.SelectiveAcceptApi.configure_criteria>`
        | Modify Selective Accept Criteria for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/selectiveAccept/criteria/{id}``
   * - :meth:`api.workspace_settings.selective_accept.create_criteria <wxc_sdk.person_settings.selective_accept.SelectiveAcceptApi.create_criteria>`
        | Create Selective Accept Criteria for an entity
        | ``POST /telephony/config/workspaces/{entity_id}/selectiveAccept/criteria``
   * - :meth:`api.workspace_settings.selective_accept.delete_criteria <wxc_sdk.person_settings.selective_accept.SelectiveAcceptApi.delete_criteria>`
        | Delete Selective Accept Criteria for an entity
        | ``DELETE /telephony/config/workspaces/{entity_id}/selectiveAccept/criteria/{id}``
   * - :meth:`api.workspace_settings.selective_accept.read <wxc_sdk.person_settings.selective_accept.SelectiveAcceptApi.read>`
        | Retrieve Selective Accept Settings for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/selectiveAccept``
   * - :meth:`api.workspace_settings.selective_accept.read_criteria <wxc_sdk.person_settings.selective_accept.SelectiveAcceptApi.read_criteria>`
        | Retrieve Selective Accept Criteria for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/selectiveAccept/criteria/{id}``
   * - :meth:`api.workspace_settings.selective_forward.configure <wxc_sdk.person_settings.selective_forward.SelectiveForwardApi.configure>`
        | Modify Selective Forward Settings for a Workspace
        | ``PUT /telephony/config/workspaces/{entity_id}/selectiveForward``
   * - :meth:`api.workspace_settings.selective_forward.configure_criteria <wxc_sdk.person_settings.selective_forward.SelectiveForwardApi.configure_criteria>`
        | Modify Selective Forward Criteria for a Workspace
        | ``PUT /telephony/config/workspaces/{entity_id}/selectiveForward/criteria/{id}``
   * - :meth:`api.workspace_settings.selective_forward.create_criteria <wxc_sdk.person_settings.selective_forward.SelectiveForwardApi.create_criteria>`
        | Create Selective Forward Criteria for a Workspace
        | ``POST /telephony/config/workspaces/{entity_id}/selectiveForward/criteria``
   * - :meth:`api.workspace_settings.selective_forward.delete_criteria <wxc_sdk.person_settings.selective_forward.SelectiveForwardApi.delete_criteria>`
        | Delete Selective Forward Criteria for a Workspace
        | ``DELETE /telephony/config/workspaces/{entity_id}/selectiveForward/criteria/{id}``
   * - :meth:`api.workspace_settings.selective_forward.read <wxc_sdk.person_settings.selective_forward.SelectiveForwardApi.read>`
        | Retrieve Selective Forward Settings for a Workspace
        | ``GET /telephony/config/workspaces/{entity_id}/selectiveForward``
   * - :meth:`api.workspace_settings.selective_forward.read_criteria <wxc_sdk.person_settings.selective_forward.SelectiveForwardApi.read_criteria>`
        | Retrieve Selective Forward Criteria for a Workspace
        | ``GET /telephony/config/workspaces/{entity_id}/selectiveForward/criteria/{id}``
   * - :meth:`api.workspace_settings.selective_reject.configure <wxc_sdk.person_settings.selective_reject.SelectiveRejectApi.configure>`
        | Modify Selective Reject Settings for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/selectiveReject``
   * - :meth:`api.workspace_settings.selective_reject.configure_criteria <wxc_sdk.person_settings.selective_reject.SelectiveRejectApi.configure_criteria>`
        | Modify Selective Reject Criteria for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/selectiveReject/criteria/{id}``
   * - :meth:`api.workspace_settings.selective_reject.create_criteria <wxc_sdk.person_settings.selective_reject.SelectiveRejectApi.create_criteria>`
        | Create Selective Reject Criteria for an entity
        | ``POST /telephony/config/workspaces/{entity_id}/selectiveReject/criteria``
   * - :meth:`api.workspace_settings.selective_reject.delete_criteria <wxc_sdk.person_settings.selective_reject.SelectiveRejectApi.delete_criteria>`
        | Delete Selective Reject Criteria for an entity
        | ``DELETE /telephony/config/workspaces/{entity_id}/selectiveReject/criteria/{id}``
   * - :meth:`api.workspace_settings.selective_reject.read <wxc_sdk.person_settings.selective_reject.SelectiveRejectApi.read>`
        | Retrieve Selective Reject Settings for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/selectiveReject``
   * - :meth:`api.workspace_settings.selective_reject.read_criteria <wxc_sdk.person_settings.selective_reject.SelectiveRejectApi.read_criteria>`
        | Retrieve Selective Reject Criteria for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/selectiveReject/criteria/{id}``
   * - :meth:`api.workspace_settings.sequential_ring.configure <wxc_sdk.person_settings.sequential_ring.SequentialRingApi.configure>`
        | Modify sequential ring settings for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/sequentialRing``
   * - :meth:`api.workspace_settings.sequential_ring.configure_criteria <wxc_sdk.person_settings.sequential_ring.SequentialRingApi.configure_criteria>`
        | Modify sequential ring criteria for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/sequentialRing/criteria/{id}``
   * - :meth:`api.workspace_settings.sequential_ring.create_criteria <wxc_sdk.person_settings.sequential_ring.SequentialRingApi.create_criteria>`
        | Create sequential ring criteria for an entity
        | ``POST /telephony/config/workspaces/{entity_id}/sequentialRing/criteria``
   * - :meth:`api.workspace_settings.sequential_ring.delete_criteria <wxc_sdk.person_settings.sequential_ring.SequentialRingApi.delete_criteria>`
        | Delete sequential ring criteria for an entity
        | ``DELETE /telephony/config/workspaces/{entity_id}/sequentialRing/criteria/{id}``
   * - :meth:`api.workspace_settings.sequential_ring.read <wxc_sdk.person_settings.sequential_ring.SequentialRingApi.read>`
        | Retrieve sequential ring settings for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/sequentialRing``
   * - :meth:`api.workspace_settings.sequential_ring.read_criteria <wxc_sdk.person_settings.sequential_ring.SequentialRingApi.read_criteria>`
        | Retrieve sequential ring criteria for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/sequentialRing/criteria/{id}``
   * - :meth:`api.workspace_settings.sim_ring.configure <wxc_sdk.person_settings.sim_ring.SimRingApi.configure>`
        | Modify Simultaneous Ring Settings for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/simultaneousRing``
   * - :meth:`api.workspace_settings.sim_ring.configure_criteria <wxc_sdk.person_settings.sim_ring.SimRingApi.configure_criteria>`
        | Modify Simultaneous Ring Criteria for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/simultaneousRing/criteria/{id}``
   * - :meth:`api.workspace_settings.sim_ring.create_criteria <wxc_sdk.person_settings.sim_ring.SimRingApi.create_criteria>`
        | Create Simultaneous Ring Criteria for an entity
        | ``POST /telephony/config/workspaces/{entity_id}/simultaneousRing/criteria``
   * - :meth:`api.workspace_settings.sim_ring.delete_criteria <wxc_sdk.person_settings.sim_ring.SimRingApi.delete_criteria>`
        | Delete Simultaneous Ring Criteria for an entity
        | ``DELETE /telephony/config/workspaces/{entity_id}/simultaneousRing/criteria/{id}``
   * - :meth:`api.workspace_settings.sim_ring.read <wxc_sdk.person_settings.sim_ring.SimRingApi.read>`
        | Retrieve Simultaneous Ring Settings for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/simultaneousRing``
   * - :meth:`api.workspace_settings.sim_ring.read_criteria <wxc_sdk.person_settings.sim_ring.SimRingApi.read_criteria>`
        | Retrieve Simultaneous Ring Criteria for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/simultaneousRing/criteria/{id}``
   * - :meth:`api.workspace_settings.voicemail.configure <wxc_sdk.person_settings.voicemail.VoicemailApi.configure>`
        | Configure Voicemail Settings for an entity
        | ``PUT /telephony/config/workspaces/{entity_id}/voicemail``
   * - :meth:`api.workspace_settings.voicemail.modify_passcode <wxc_sdk.person_settings.voicemail.VoicemailApi.modify_passcode>`
        | Modify an entity's voicemail passcode
        | ``PUT /telephony/config/workspaces/{entity_id}/voicemail/passcode``
   * - :meth:`api.workspace_settings.voicemail.read <wxc_sdk.person_settings.voicemail.VoicemailApi.read>`
        | Read Voicemail Settings for an entity
        | ``GET /telephony/config/workspaces/{entity_id}/voicemail``
   * - :meth:`api.workspace_settings.voicemail.reset_pin <wxc_sdk.person_settings.voicemail.VoicemailApi.reset_pin>`
        | Reset Voicemail PIN
        | ``POST /telephony/config/workspaces/{entity_id}/voicemail/actions/resetPin/invoke``
   * - :meth:`api.workspaces.capabilities <wxc_sdk.workspaces.WorkspacesApi.capabilities>`
        | Shows the capabilities for a workspace by ID
        | ``GET /workspaces/{workspace_id}/capabilities``
   * - :meth:`api.workspaces.create <wxc_sdk.workspaces.WorkspacesApi.create>`
        | Create a Workspace
        | ``POST /workspaces``
   * - :meth:`api.workspaces.delete_workspace <wxc_sdk.workspaces.WorkspacesApi.delete_workspace>`
        | Delete a Workspace
        | ``DELETE /workspaces/{workspace_id}``
   * - :meth:`api.workspaces.details <wxc_sdk.workspaces.WorkspacesApi.details>`
        | Get Workspace Details
        | ``GET /workspaces/{workspace_id}``
   * - :meth:`api.workspaces.list <wxc_sdk.workspaces.WorkspacesApi.list>`
        | List Workspaces
        | ``GET /workspaces``
   * - :meth:`api.workspaces.update <wxc_sdk.workspaces.WorkspacesApi.update>`
        | Update a Workspace
        | ``PUT /workspaces/{workspace_id}``
   * - :meth:`api.xapi.execute_command <wxc_sdk.xapi.XApi.execute_command>`
        | Execute Command
        | ``POST /xapi/command/{command_name}``
   * - :meth:`api.xapi.query_status <wxc_sdk.xapi.XApi.query_status>`
        | Query Status
        | ``GET /xapi/status``

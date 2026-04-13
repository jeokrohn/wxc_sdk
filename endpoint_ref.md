# Endpoint Reference

| Endpoint | HTTP Method | Endpoint URL | Description |
| --- | --- | --- | --- |
| `api.admin_audit.list_event_categories` | `GET` | `/adminAudit/eventCategories` | List Admin Audit Event Categories |
| `api.admin_audit.list_events` | `GET` | `/adminAudit/events` | List Admin Audit Events |
| `api.attachment_actions.details` | `GET` | `/attachment/actions/{action_id}` | Shows details for a attachment action, by ID. |
| `api.authorizations.delete` | `DELETE` | `/authorizations/{authorization_id}` | Deletes an authorization, by authorization ID or client ID and org ID. |
| `api.authorizations.get_token_expiration_status` | `GET` | `/authorizations/tokenExpiry` | Get expiration status for a token |
| `api.authorizations.list` | `GET` | `/authorizations` | Lists all authorizations for a user. Either personId or personEmail must be provided. This API does not support |
| `api.cdr.get_cdr_history` | `GET` | `https://analytics-calling.webexapis.com/v1/{cdr_stream|cdr_feed}` | Provides Webex Calling Detailed Call History data for your organization. |
| `api.converged_recordings.delete` | `DELETE` | `/convergedRecordings/{recording_id}` | Delete a Recording |
| `api.converged_recordings.details` | `GET` | `/convergedRecordings/{recording_id}` | Get Recording Details |
| `api.converged_recordings.list` | `GET` | `/convergedRecordings` | List Recordings |
| `api.converged_recordings.list_for_admin_or_compliance_officer` | `GET` | `/admin/convergedRecordings` | List Recordings for Admin or Compliance officer |
| `api.converged_recordings.metadata` | `GET` | `/convergedRecordings/{recording_id}/metadata` | Get Recording metadata |
| `api.converged_recordings.move_recordings_into_the_recycle_bin` | `POST` | `/convergedRecordings/softDelete` | Move Recordings into the Recycle Bin |
| `api.converged_recordings.purge_recordings_from_recycle_bin` | `POST` | `/convergedRecordings/purge` | Purge Recordings from Recycle Bin |
| `api.converged_recordings.reassign` | `POST` | `/convergedRecordings/reassign` | Reassign Recordings |
| `api.converged_recordings.restore_recordings_from_recycle_bin` | `POST` | `/convergedRecordings/restore` | Restore Recordings from Recycle Bin |
| `api.device_configurations.list` | `GET` | `/deviceConfigurations` | Lists all device configurations associated with the given device ID. Administrators can list configurations |
| `api.device_configurations.update` | `PATCH` | `/deviceConfigurations` | Update Device Configurations |
| `api.devices.activation_code` | `POST` | `/devices/activationCode` | Create a Device Activation Code |
| `api.devices.create_by_mac_address` | `POST` | `/devices` | Create a phone by it's MAC address in a specific workspace or for a person. |
| `api.devices.delete` | `DELETE` | `/devices/{device_id}` | Delete a Device |
| `api.devices.details` | `GET` | `/devices/{device_id}` | Get Device Details |
| `api.devices.list` | `GET` | `/devices` | List Devices |
| `api.devices.modify_device_tags` | `PATCH` | `/devices/{device_id}` | Modify Device Tags |
| `api.devices.settings_jobs.change` | `POST` | `/telephony/config/jobs/devices/callDeviceSettings` | Change device settings across organization or locations jobs. |
| `api.devices.settings_jobs.errors` | `GET` | `/telephony/config/jobs/devices/callDeviceSettings/{job_id}/errors` | List change device settings job errors. |
| `api.devices.settings_jobs.list` | `GET` | `/telephony/config/jobs/devices/callDeviceSettings` | List change device settings jobs. |
| `api.devices.settings_jobs.status` | `GET` | `/telephony/config/jobs/devices/callDeviceSettings/{job_id}` | Get change device settings job status. |
| `api.events.details` | `GET` | `/events/{event_id}` | Shows details for an event, by event ID. |
| `api.events.list` | `GET` | `/events` | List events in your organization. Several query parameters are available to filter the response. |
| `api.groups.create` | `POST` | `/groups` | Create a new group using the provided settings. Only display_name is mandatory |
| `api.groups.delete_group` | `DELETE` | `/groups/{group_id}` | Delete a group |
| `api.groups.details` | `GET` | `/groups/{group_id}` | Get group details |
| `api.groups.list` | `GET` | `/groups` | List groups in your organization. |
| `api.groups.members` | `GET` | `/groups/{group_id}/Members` | Query members of a group |
| `api.groups.update` | `PATCH` | `/groups/{group_id}` | update group information. |
| `api.guests.create` | `POST` | `/guests/token` | Create a Guest |
| `api.guests.guest_count` | `GET` | `/guests/count` | Get Guest Count |
| `api.jobs.activation_emails.errors` | `GET` | `/identity/organizations/{org_id}/jobs/sendActivationEmails/{job_id}/errors` | Get Bulk Activation Email Resend Job Errors |
| `api.jobs.activation_emails.start` | `POST` | `/identity/organizations/{org_id}/jobs/sendActivationEmails` | Initiate Bulk Activation Email Resend Job |
| `api.jobs.activation_emails.status` | `GET` | `/identity/organizations/{org_id}/jobs/sendActivationEmails/{job_id}/status` | Get Bulk Activation Email Resend Job Status |
| `api.jobs.apply_line_key_templates.apply` | `POST` | `/telephony/config/jobs/devices/applyLineKeyTemplate` | Apply a Line key Template |
| `api.jobs.apply_line_key_templates.errors` | `GET` | `/telephony/config/jobs/devices/applyLineKeyTemplate/{job_id}/errors` | Get job errors for an Apply Line Key Template job |
| `api.jobs.apply_line_key_templates.list` | `GET` | `/telephony/config/jobs/devices/applyLineKeyTemplate` | Get List of Apply Line Key Template jobs |
| `api.jobs.apply_line_key_templates.status` | `GET` | `/telephony/config/jobs/devices/applyLineKeyTemplate/{job_id}` | Get the job status of an Apply Line Key Template job |
| `api.jobs.call_recording.errors` | `GET` | `/telephony/config/jobs/callRecording/{job_id}/errors` | Get Job Errors for a Call Recording Job |
| `api.jobs.call_recording.list` | `GET` | `/telephony/config/jobs/callRecording` | List Call Recording Jobs |
| `api.jobs.call_recording.status` | `GET` | `/telephony/config/jobs/callRecording/{job_id}` | Get the Job Status of a Call Recording Job |
| `api.jobs.device_settings.change` | `POST` | `/telephony/config/jobs/devices/callDeviceSettings` | Change device settings across organization or locations jobs. |
| `api.jobs.device_settings.errors` | `GET` | `/telephony/config/jobs/devices/callDeviceSettings/{job_id}/errors` | List change device settings job errors. |
| `api.jobs.device_settings.list` | `GET` | `/telephony/config/jobs/devices/callDeviceSettings` | List change device settings jobs. |
| `api.jobs.device_settings.status` | `GET` | `/telephony/config/jobs/devices/callDeviceSettings/{job_id}` | Get change device settings job status. |
| `api.jobs.disable_calling_location.errors` | `GET` | `/telephony/config/jobs/locations/deleteCallingLocation/{job_id}/errors` | Retrieve Errors for a Disable Calling Location Job |
| `api.jobs.disable_calling_location.initiate` | `POST` | `/telephony/config/jobs/locations/deleteCallingLocation` | Disable a Location for Webex Calling. |
| `api.jobs.disable_calling_location.list` | `GET` | `/telephony/config/jobs/locations/deleteCallingLocation` | Get a List of Disable Calling Location Jobs |
| `api.jobs.disable_calling_location.pause` | `POST` | `/telephony/config/jobs/locations/deleteCallingLocation/{job_id}/actions/pause/invoke` | Pause a Disable Calling Location Job |
| `api.jobs.disable_calling_location.resume` | `POST` | `/telephony/config/jobs/locations/deleteCallingLocation/{job_id}/actions/resume/invoke` | Resume a Paused Disable Calling Location Job |
| `api.jobs.disable_calling_location.status` | `GET` | `/telephony/config/jobs/locations/deleteCallingLocation/{job_id}` | Get Disable Calling Location Job Status |
| `api.jobs.dynamic_device_settings.errors` | `GET` | `/telephony/config/jobs/devices/dynamicDeviceSettings/{job_id}/errors` | List Dynamic Device Settings Job Errors |
| `api.jobs.dynamic_device_settings.list` | `GET` | `/telephony/config/jobs/devices/dynamicDeviceSettings` | List dynamic device settings jobs. |
| `api.jobs.dynamic_device_settings.status` | `GET` | `/telephony/config/jobs/devices/dynamicDeviceSettings/{job_id}` | Get Device Dynamic Settings Job Status |
| `api.jobs.dynamic_device_settings.update_across_org_or_location` | `POST` | `/telephony/config/jobs/devices/dynamicDeviceSettings` | Updates dynamic Device Settings Across Organization Or Location |
| `api.jobs.manage_numbers.abandon` | `POST` | `/telephony/config/jobs/numbers/manageNumbers/{job_id}/actions/abandon/invoke` | Abandon the Manage Numbers Job. |
| `api.jobs.manage_numbers.errors` | `GET` | `/telephony/config/jobs/numbers/manageNumbers/{job_id}/errors` | List Manage Numbers Job errors |
| `api.jobs.manage_numbers.initiate_job` | `POST` | `/telephony/config/jobs/numbers/manageNumbers` | Initiate Number Jobs |
| `api.jobs.manage_numbers.list` | `GET` | `/telephony/config/jobs/numbers/manageNumbers` | List Manage Numbers Jobs |
| `api.jobs.manage_numbers.pause` | `POST` | `/telephony/config/jobs/numbers/manageNumbers/{job_id}/actions/pause/invoke` | Pause the Manage Numbers Job |
| `api.jobs.manage_numbers.resume` | `POST` | `/telephony/config/jobs/numbers/manageNumbers/{job_id}/actions/resume/invoke` | Resume the Manage Numbers Job |
| `api.jobs.manage_numbers.status` | `GET` | `/telephony/config/jobs/numbers/manageNumbers/{job_id}` | Get Manage Numbers Job Status |
| `api.jobs.move_users.abandon` | `POST` | `/telephony/config/jobs/person/moveLocation/{job_id}/actions/abandon/invoke` | Abandon the Move Users Job. |
| `api.jobs.move_users.errors` | `GET` | `/telephony/config/jobs/person/moveLocation/{job_id}/errors` | List Move Users Job errors |
| `api.jobs.move_users.list` | `GET` | `/telephony/config/jobs/person/moveLocation` | List Move Users Jobs |
| `api.jobs.move_users.pause` | `POST` | `/telephony/config/jobs/person/moveLocation/{job_id}/actions/pause/invoke` | Pause the Move Users Job |
| `api.jobs.move_users.resume` | `POST` | `/telephony/config/jobs/person/moveLocation/{job_id}/actions/resume/invoke` | Resume the Move Users Job |
| `api.jobs.move_users.status` | `GET` | `/telephony/config/jobs/person/moveLocation/{job_id}` | Get Move Users Job Status |
| `api.jobs.move_users.validate_or_initiate` | `POST` | `/telephony/config/jobs/person/moveLocation` | Validate or Initiate Move Users Job |
| `api.jobs.rebuild_phones.errors` | `GET` | `/telephony/config/jobs/devices/rebuildPhones/{job_id}/errors` | Get Job Errors for a Rebuild Phones Job |
| `api.jobs.rebuild_phones.list` | `GET` | `/telephony/config/jobs/devices/rebuildPhones` | List Rebuild Phones Jobs |
| `api.jobs.rebuild_phones.rebuild_phones_configuration` | `POST` | `/telephony/config/jobs/devices/rebuildPhones` | Rebuild Phones Configuration |
| `api.jobs.rebuild_phones.status` | `GET` | `/telephony/config/jobs/devices/rebuildPhones/{job_id}` | Get the Job Status of a Rebuild Phones Job |
| `api.jobs.update_routing_prefix.errors` | `GET` | `/telephony/config/jobs/updateRoutingPrefix/{job_id}/errors` | Get job errors for update routing prefix job |
| `api.jobs.update_routing_prefix.list` | `GET` | `/telephony/config/jobs/updateRoutingPrefix` | Get a List of Update Routing Prefix jobs |
| `api.jobs.update_routing_prefix.status` | `GET` | `/telephony/config/jobs/updateRoutingPrefix/{job_id}` | Get the job status of Update Routing Prefix job |
| `api.licenses.assign_licenses_to_users` | `PATCH` | `/licenses/users` | Assign Licenses to Users |
| `api.licenses.assigned_users` | `GET` | `/licenses/{license_id}` | Get users license is assigned to, by license ID. |
| `api.licenses.details` | `GET` | `/licenses/{license_id}` | Shows details for a license, by ID. |
| `api.licenses.list` | `GET` | `/licenses` | List all licenses for a given organization. If no org_id is specified, the default is the organization of |
| `api.locations.create` | `POST` | `/locations` | Create a Location |
| `api.locations.create_floor` | `POST` | `/locations/{location_id}/floors` | Create a Location Floor |
| `api.locations.delete` | `DELETE` | `/locations/{location_id}` | Delete Location |
| `api.locations.delete_floor` | `DELETE` | `/locations/{location_id}/floors/{floor_id}` | Delete a Location Floor |
| `api.locations.details` | `GET` | `/locations/{location_id}` | Get Location Details |
| `api.locations.floor_details` | `GET` | `/locations/{location_id}/floors/{floor_id}` | Get Location Floor Details |
| `api.locations.list` | `GET` | `/locations` | List Locations |
| `api.locations.list_floors` | `GET` | `/locations/{location_id}/floors` | List Location Floors |
| `api.locations.update` | `PUT` | `/locations/{location_id}` | Update details for a location, by ID. |
| `api.locations.update_floor` | `PUT` | `/locations/{location_id}/floors/{id}` | Update a Location Floor |
| `api.me.announcement_languages` | `GET` | `/telephony/config/people/me/announcementLanguages` | Retrieve announcement languages for the authenticated user |
| `api.me.anon_calls.get` | `GET` | `/telephony/config/people/me/settings/anonymousCallReject` | Get Anonymous Call Rejection Settings for User |
| `api.me.anon_calls.modify` | `PUT` | `/telephony/config/people/me/settings/anonymousCallReject` | Modify Anonymous Call Rejection Settings for User |
| `api.me.available_numbers_for_location` | `GET` | `/telephony/config/people/me/location/assignedNumbers` | Get Available Numbers for User's Location. |
| `api.me.barge.configure` | `PUT` | `/telephony/config/people/me/settings/bargeIn` | Configure Barge-In Settings |
| `api.me.barge.get` | `GET` | `/telephony/config/people/me/settings/bargeIn` | Retrieve Barge-In Settings |
| `api.me.call_block.add_number` | `POST` | `/telephony/config/people/me/settings/callBlock/numbers` | Add a phone number to user's Call Block List |
| `api.me.call_block.delete_number` | `DELETE` | `/telephony/config/people/me/settings/callBlock/numbers/{phone_number_id}` | Delete User Call Block Number |
| `api.me.call_block.settings` | `GET` | `/telephony/config/people/me/settings/callBlock` | Get My Call Block Settings |
| `api.me.call_block.state_for_number` | `GET` | `/telephony/config/people/me/settings/callBlock/numbers/{phone_number_id}` | Get My Call Block State For Specific Number |
| `api.me.call_captions_settings` | `GET` | `/telephony/config/people/me/settings/callCaptions` | Get my call captions settings |
| `api.me.call_center.modify` | `PUT` | `/telephony/config/people/me/settings/queues` | Modify My Call Center Settings |
| `api.me.call_center.settings` | `GET` | `/telephony/config/people/me/settings/queues` | Get My Call Center Settings |
| `api.me.call_notify.criteria_create` | `POST` | `/telephony/config/people/me/settings/callNotify/criteria` | Add a Call Notify Criteria |
| `api.me.call_notify.criteria_delete` | `DELETE` | `/telephony/config/people/me/settings/callNotify/criteria/{criteria_id}` | Delete a Call Notify Criteria |
| `api.me.call_notify.criteria_get` | `GET` | `/telephony/config/people/me/settings/callNotify/criteria/{criteria_id}` | Get Call Notify Criteria Settings |
| `api.me.call_notify.criteria_update` | `PUT` | `/telephony/config/people/me/settings/callNotify/criteria/{criteria_id}` | Modify a Call Notify Criteria |
| `api.me.call_notify.get` | `GET` | `/telephony/config/people/me/settings/callNotify` | Get Call Notify Settings for User |
| `api.me.call_notify.update` | `PUT` | `/telephony/config/people/me/settings/callNotify` | Modify Call Notify Settings for User |
| `api.me.call_park.settings` | `GET` | `/telephony/config/people/me/settings/callPark` | Get My Call Park Settings |
| `api.me.call_pickup.settings` | `GET` | `/telephony/config/people/me/settings/callPickupGroup` | Get My Call Pickup Group Settings |
| `api.me.call_policies.settings` | `GET` | `/telephony/config/people/me/settings/callPolicies` | Get Call Policies Settings for User |
| `api.me.call_policies.update` | `PUT` | `/telephony/config/people/me/settings/callPolicies` | Modify Call Policies Settings for User |
| `api.me.call_waiting.get` | `GET` | `/telephony/config/people/me/settings/callWaiting` | Get Call Waiting Settings for User |
| `api.me.call_waiting.update` | `PUT` | `/telephony/config/people/me/settings/callWaiting` | Modify Call Waiting Settings for User |
| `api.me.caller_id.available_caller_id_list` | `GET` | `/telephony/config/people/me/settings/availableCallerIds` | Get My Available Caller ID List |
| `api.me.caller_id.get_selected_caller_id_settings` | `GET` | `/telephony/config/people/me/settings/selectedCallerId` | Read My Selected Caller ID Settings |
| `api.me.caller_id.modify_selected_caller_id_settings` | `PUT` | `/telephony/config/people/me/settings/selectedCallerId` | Configure My Selected Caller ID Settings |
| `api.me.caller_id.settings` | `GET` | `/telephony/config/people/me/settings/callerId` | Get My Caller ID Settings |
| `api.me.caller_id.update` | `PUT` | `/telephony/config/people/me/settings/callerId` | Modify My Caller ID Settings |
| `api.me.calling_services_list` | `GET` | `/telephony/config/people/me/settings/services` | Get My Calling Services List |
| `api.me.contact_center_extensions` | `GET` | `/telephony/config/people/me` | Read the Contact Center Extensions |
| `api.me.country_telephony_config_requirements` | `GET` | `/telephony/config/people/me/countries/{country_code}` | Retrieve country-specific telephony configuration requirements |
| `api.me.details` | `GET` | `/telephony/config/people/me` | Get My Own Details |
| `api.me.dnd.configure` | `PUT` | `/telephony/config/people/me/settings/doNotDisturb` | Update Do Not Disturb Settings for User |
| `api.me.dnd.settings` | `GET` | `/telephony/config/people/me/settings/doNotDisturb` | Get Do Not Disturb Settings for User |
| `api.me.endpoints.available_preferred_answer_endpoints` | `GET` | `/telephony/config/people/me/settings/availablePreferredAnswerEndpoints` | Get List Available Preferred Answer Endpoints |
| `api.me.endpoints.details` | `GET` | `/telephony/config/people/me/endpoints/{endpoint_id}` | Get My Endpoints Details |
| `api.me.endpoints.get_preferred_answer_endpoint` | `GET` | `/telephony/config/people/me/settings/preferredAnswerEndpoint` | Get Preferred Answer Endpoint |
| `api.me.endpoints.list` | `GET` | `/telephony/config/people/me/endpoints` | Read the List of My Endpoints |
| `api.me.endpoints.modify_preferred_answer_endpoint` | `PUT` | `/telephony/config/people/me/settings/preferredAnswerEndpoint` | Modify Preferred Answer Endpoint |
| `api.me.endpoints.update` | `PUT` | `/telephony/config/people/me/endpoints/{endpoint_id}` | Modify My Endpoints Details |
| `api.me.executive.alert_settings` | `GET` | `/telephony/config/people/me/settings/executive/alert` | Get User Executive Alert Settings |
| `api.me.executive.assigned_assistants` | `GET` | `/telephony/config/people/me/settings/executive/assignedAssistants` | Get My Executive Assigned Assistants |
| `api.me.executive.call_filtering_criteria` | `GET` | `/telephony/config/people/me/settings/executive/callFiltering/criteria/{id}` | Get User Executive Call Filtering Criteria Settings |
| `api.me.executive.create_call_filtering_criteria` | `POST` | `/telephony/config/people/me/settings/executive/callFiltering/criteria` | Add User Executive Call Filtering Criteria |
| `api.me.executive.delete_call_filtering_criteria` | `DELETE` | `/telephony/config/people/me/settings/executive/callFiltering/criteria/{id}` | Delete User Executive Call Filtering Criteria |
| `api.me.executive.executive_assistant_settings` | `GET` | `/telephony/config/people/me/settings/executive/assistant` | Get My Executive Assistant Settings |
| `api.me.executive.executive_available_assistants` | `GET` | `/telephony/config/people/me/settings/executive/availableAssistants` | Get My Executive Available Assistants |
| `api.me.executive.executive_call_filtering_settings` | `GET` | `/telephony/config/people/me/settings/executive/callFiltering` | Get User Executive Call Filtering Settings |
| `api.me.executive.screening_settings` | `GET` | `/telephony/config/people/me/settings/executive/screening` | Get User Executive Screening Settings |
| `api.me.executive.update_alert_settings` | `PUT` | `/telephony/config/people/me/settings/executive/alert` | Modify User Executive Alert Settings |
| `api.me.executive.update_assigned_assistants` | `PUT` | `/telephony/config/people/me/settings/executive/assignedAssistants` | Modify My Executive Assigned Assistants |
| `api.me.executive.update_call_filtering_criteria` | `PUT` | `/telephony/config/people/me/settings/executive/callFiltering/criteria/{id}` | Update User Executive Call Filtering Criteria Settings |
| `api.me.executive.update_executive_assistant_settings` | `PUT` | `/telephony/config/people/me/settings/executive/assistant` | Modify My Executive Assistant Settings |
| `api.me.executive.update_executive_call_filtering_settings` | `PUT` | `/telephony/config/people/me/settings/executive/callFiltering` | Update User Executive Call Filtering Settings |
| `api.me.executive.update_screening_settings` | `PUT` | `/telephony/config/people/me/settings/executive/screening` | Modify User Executive Screening Settings |
| `api.me.feature_access_codes` | `GET` | `/telephony/config/people/me/settings/featureAccessCode` | Get My Feature Access Codes |
| `api.me.forwarding.configure` | `PUT` | `/telephony/config/people/me/settings/callForwarding` | Configure My Call Forwarding Settings |
| `api.me.forwarding.settings` | `GET` | `/telephony/config/people/me/settings/callForwarding` | Read My Call Forwarding Settings |
| `api.me.go_override.get` | `GET` | `/telephony/config/people/me/settings/webexGoOverride` | Get My WebexGoOverride Settings |
| `api.me.go_override.update` | `PUT` | `/telephony/config/people/me/settings/webexGoOverride` | Modify My WebexGoOverride Settings |
| `api.me.guest_calling_numbers` | `GET` | `/telephony/config/people/me/settings/guestCalling/numbers` | Retrieve My Guest Calling Numbers |
| `api.me.mode_management.extend_mode` | `POST` | `/telephony/config/people/me/settings/modeManagement/features/{feature_id}/actions/extendMode/invoke` | Extend Current Operating Mode Duration |
| `api.me.mode_management.feature_get` | `GET` | `/telephony/config/people/me/settings/modeManagement/features/{feature_id}` | Get Mode Management Feature |
| `api.me.mode_management.get_common_modes` | `GET` | `/telephony/config/people/me/settings/modeManagement/features/commonModes` | Get Common Modes |
| `api.me.mode_management.get_features` | `GET` | `/telephony/config/people/me/settings/modeManagement/features` | Get Mode Management Features |
| `api.me.mode_management.get_normal_operation_mode` | `GET` | `/telephony/config/people/me/settings/modeManagement/features/{feature_id}/normalOperationMode` | Get Normal Operation Mode |
| `api.me.mode_management.get_operating_mode` | `GET` | `/telephony/config/people/me/settings/modeManagement/features/{feature_id}/modes/{mode_id}` | Get Operating Mode |
| `api.me.mode_management.switch_mode_for_feature` | `POST` | `/telephony/config/people/me/settings/modeManagement/features/{feature_id}/actions/switchMode/invoke` | Switch Mode for Single Feature |
| `api.me.mode_management.switch_mode_multiple_features` | `POST` | `/telephony/config/people/me/settings/modeManagement/features/actions/switchMode/invoke` | Switch Mode for Multiple Features |
| `api.me.mode_management.switch_to_normal_operation` | `POST` | `/telephony/config/people/me/settings/modeManagement/features/{feature_id}/actions/switchToNormalOperation/invoke` | Switch to Normal Operation |
| `api.me.monitoring_settings` | `GET` | `/telephony/config/people/me/settings/monitoring` | Get My Monitoring Settings |
| `api.me.personal_assistant.get` | `GET` | `/telephony/config/people/me/settings/personalAssistant` | Get My Personal Assistant |
| `api.me.personal_assistant.update` | `PUT` | `/telephony/config/people/me/settings/personalAssistant` | Modify My Personal Assistant |
| `api.me.priority_alert.criteria_create` | `POST` | `/telephony/config/people/me/settings/priorityAlert/criteria` | Add a Priority Alert Criteria |
| `api.me.priority_alert.criteria_delete` | `DELETE` | `/telephony/config/people/me/settings/priorityAlert/criteria/{criteria_id}` | Delete a Priority Alert Criteria |
| `api.me.priority_alert.criteria_get` | `GET` | `/telephony/config/people/me/settings/priorityAlert/criteria/{criteria_id}` | Get Priority Alert Criteria Settings |
| `api.me.priority_alert.criteria_update` | `PUT` | `/telephony/config/people/me/settings/priorityAlert/criteria/{criteria_id}` | Modify Settings for a Priority Alert Criteria |
| `api.me.priority_alert.get` | `GET` | `/telephony/config/people/me/settings/priorityAlert` | Get Priority Alert Settings |
| `api.me.priority_alert.update` | `PUT` | `/telephony/config/people/me/settings/priorityAlert` | Modify Priority Alert Settings for User |
| `api.me.recording.settings` | `GET` | `/telephony/config/people/me/settings/callRecording` | Get My Call Recording Settings |
| `api.me.schedules.create` | `POST` | `/telephony/config/people/me/schedules` | Add a User level Schedule for Call Settings |
| `api.me.schedules.delete` | `DELETE` | `/telephony/config/people/me/schedules/{schedule_type}/{schedule_id}` | Delete a User Schedule |
| `api.me.schedules.event_create` | `POST` | `/telephony/config/people/me/schedules/{schedule_type}/{schedule_id}/events` | Add an event for a User Schedule |
| `api.me.schedules.event_delete` | `DELETE` | `/telephony/config/people/me/schedules/{schedule_type}/{schedule_id}/events/{event_id}` | Delete User a Schedule Event |
| `api.me.schedules.event_get` | `GET` | `/telephony/config/people/me/schedules/{schedule_type}/{schedule_id}/events/{event_id}` | Get User Schedule Event |
| `api.me.schedules.event_update` | `PUT` | `/telephony/config/people/me/schedules/{schedule_type}/{schedule_id}/events/{event_id}` | Modify User Schedule Event |
| `api.me.schedules.get_location_schedule` | `GET` | `/telephony/config/people/me/locations/schedules/{schedule_type}/{schedule_id}` | Get User's Location Level Schedule |
| `api.me.schedules.get_user_schedule` | `GET` | `/telephony/config/people/me/schedules/{schedule_type}/{schedule_id}` | Get User Schedule |
| `api.me.schedules.list` | `GET` | `/telephony/config/people/me/schedules` | Get User (and Location) Schedules |
| `api.me.schedules.update` | `PUT` | `/telephony/config/people/me/schedules/{schedule_type}/{schedule_id}` | Modify User Schedule |
| `api.me.selective_accept.criteria_create` | `POST` | `/telephony/config/people/me/settings/selectiveAccept/criteria` | Add User Selective Call Accept Criteria |
| `api.me.selective_accept.criteria_delete` | `DELETE` | `/telephony/config/people/me/settings/selectiveAccept/criteria/{criteria_id}` | Delete a Selective Call Accept Criteria |
| `api.me.selective_accept.criteria_get` | `GET` | `/telephony/config/people/me/settings/selectiveAccept/criteria/{criteria_id}` | Get Selective Call Accept Criteria Settings for User |
| `api.me.selective_accept.criteria_update` | `PUT` | `/telephony/config/people/me/settings/selectiveAccept/criteria/{criteria_id}` | Modify a Selective Call Accept Criteria |
| `api.me.selective_accept.get` | `GET` | `/telephony/config/people/me/settings/selectiveAccept` | Get Selective Call Accept Settings for User |
| `api.me.selective_accept.update` | `PUT` | `/telephony/config/people/me/settings/selectiveAccept` | Modify Selective Call Accept Settings for User |
| `api.me.selective_forward.criteria_create` | `POST` | `/telephony/config/people/me/settings/selectiveForward/criteria` | Add a Selective Call Forwarding Criteria |
| `api.me.selective_forward.criteria_delete` | `DELETE` | `/telephony/config/people/me/settings/selectiveForward/criteria/{criteria_id}` | Delete a Selective Call Forwarding Criteria |
| `api.me.selective_forward.criteria_get` | `GET` | `/telephony/config/people/me/settings/selectiveForward/criteria/{criteria_id}` | Get Settings for a Selective Call Forwarding Criteria |
| `api.me.selective_forward.criteria_update` | `PUT` | `/telephony/config/people/me/settings/selectiveForward/criteria/{criteria_id}` | Modify Settings for a Selective Call Forwarding Criteria |
| `api.me.selective_forward.get` | `GET` | `/telephony/config/people/me/settings/selectiveForward` | Get Selective Call Forward Settings for User |
| `api.me.selective_forward.update` | `PUT` | `/telephony/config/people/me/settings/selectiveForward` | Modify Selective Call Forward Settings for User |
| `api.me.selective_reject.criteria_create` | `POST` | `/telephony/config/people/me/settings/selectiveReject/criteria` | Add User Selective Call Reject Criteria |
| `api.me.selective_reject.criteria_delete` | `DELETE` | `/telephony/config/people/me/settings/selectiveReject/criteria/{criteria_id}` | Delete a Selective Call Reject Criteria |
| `api.me.selective_reject.criteria_get` | `GET` | `/telephony/config/people/me/settings/selectiveReject/criteria/{id}` | Get Selective Call Reject Criteria Settings for User |
| `api.me.selective_reject.criteria_update` | `PUT` | `/telephony/config/people/me/settings/selectiveReject/criteria/{criteria_id}` | Modify a Selective Call Reject Criteria |
| `api.me.selective_reject.get` | `GET` | `/telephony/config/people/me/settings/selectiveReject` | Get Selective Call Reject Settings for User |
| `api.me.selective_reject.update` | `PUT` | `/telephony/config/people/me/settings/selectiveReject` | Modify Selective Call Reject Settings for User |
| `api.me.sequential_ring.criteria_create` | `POST` | `/telephony/config/people/me/settings/sequentialRing/criteria` | Add User Sequential Ring Criteria |
| `api.me.sequential_ring.criteria_delete` | `DELETE` | `/telephony/config/people/me/settings/sequentialRing/criteria/{criteria_id}` | Delete Sequential Ring Criteria |
| `api.me.sequential_ring.criteria_get` | `GET` | `/telephony/config/people/me/settings/sequentialRing/criteria/{criteria_id}` | Get Sequential Ring Criteria Settings for User |
| `api.me.sequential_ring.criteria_update` | `PUT` | `/telephony/config/people/me/settings/sequentialRing/criteria/{criteria_id}` | Modify Sequential Ring Criteria Settings for User |
| `api.me.sequential_ring.get` | `GET` | `/telephony/config/people/me/settings/sequentialRing` | Get Sequential Ring Settings for User |
| `api.me.sequential_ring.update` | `PUT` | `/telephony/config/people/me/settings/sequentialRing` | Modify Sequential Ring Settings for User |
| `api.me.sim_ring.criteria_create` | `POST` | `/telephony/config/people/me/settings/simultaneousRing/criteria` | Create My Simultaneous Ring Criteria |
| `api.me.sim_ring.criteria_delete` | `DELETE` | `/telephony/config/people/me/settings/simultaneousRing/criteria/{criteria_id}` | Delete My Simultaneous Ring Criteria |
| `api.me.sim_ring.criteria_get` | `GET` | `/telephony/config/people/me/settings/simultaneousRing/criteria/{criteria_id}` | Retrieve My Simultaneous Ring Criteria |
| `api.me.sim_ring.criteria_update` | `PUT` | `/telephony/config/people/me/settings/simultaneousRing/criteria/{criteria_id}` | Modify My Simultaneous Ring Criteria |
| `api.me.sim_ring.get` | `GET` | `/telephony/config/people/me/settings/simultaneousRing` | Retrieve My Simultaneous Ring Settings |
| `api.me.sim_ring.update` | `PUT` | `/telephony/config/people/me/settings/simultaneousRing` | Modify My Simultaneous Ring Settings |
| `api.me.snr.create_snr` | `POST` | `/telephony/config/people/me/settings/singleNumberReach/numbers` | Add phone number as User's Single Number Reach |
| `api.me.snr.delete_snr` | `DELETE` | `/telephony/config/people/me/settings/singleNumberReach/numbers/{phone_number_id}` | Delete User's Single Number Reach Contact Settings |
| `api.me.snr.settings` | `GET` | `/telephony/config/people/me/settings/singleNumberReach` | Get User's Single Number Reach Settings |
| `api.me.snr.update` | `PUT` | `/telephony/config/people/me/settings/singleNumberReach` | Update User's Single Number Reach Settings |
| `api.me.snr.update_snr` | `PUT` | `/telephony/config/people/me/settings/singleNumberReach/numbers/{phone_number_id}` | Modify User's Single Number Reach Contact Settings |
| `api.me.voicemail.configure` | `PUT` | `/telephony/config/people/me/settings/voicemail` | Configure Voicemail Settings for a Person |
| `api.me.voicemail.settings` | `GET` | `/telephony/config/people/me/settings/voicemail` | Read Voicemail Settings for a Person |
| `api.meetings.chats.delete` | `DELETE` | `/meetings/postMeetingChats` | Deletes the meeting chats of a finished meeting instance specified by meetingId. |
| `api.meetings.chats.list` | `GET` | `/meetings/postMeetingChats` | Lists the meeting chats of a finished meeting instance specified by meetingId. You can set a maximum number |
| `api.meetings.closed_captions.download_snippets` | `GET` | `/meetingClosedCaptions/{closed_caption_id}/download` | Download meeting closed caption snippets from the meeting closed caption specified by closedCaptionId formatted |
| `api.meetings.closed_captions.list` | `GET` | `/meetingClosedCaptions` | Lists closed captions of a finished meeting instance specified by meetingId. |
| `api.meetings.closed_captions.list_snippets` | `GET` | `/meetingClosedCaptions/{closed_caption_id}/snippets` | Lists snippets of a meeting closed caption specified by closedCaptionId. |
| `api.meetings.create` | `POST` | `/meetings` | Creates a new meeting. Regular users can schedule up to 100 meetings in 24 hours and admin users up to 3000. |
| `api.meetings.delete` | `DELETE` | `/meetings/{meeting_id}` | Deletes a meeting with a specified meeting ID. The deleted meeting cannot be recovered. This operation applies |
| `api.meetings.get` | `GET` | `/meetings/{meeting_id}` | Retrieves details for a meeting with a specified meeting ID. |
| `api.meetings.invitees.create_invitee` | `POST` | `/meetingInvitees` | Invite a person to attend a meeting. |
| `api.meetings.invitees.create_invitees` | `POST` | `/meetingInvitees/bulkInsert` | Invite people to attend a meeting in bulk. |
| `api.meetings.invitees.delete` | `DELETE` | `/meetingInvitees/{meeting_invitee_id}` | Removes a meeting invitee identified by a meetingInviteeId specified in the URI. The deleted meeting invitee |
| `api.meetings.invitees.invitee_details` | `GET` | `/meetingInvitees/{meeting_invitee_id}` | Retrieve details for a meeting invitee identified by a meetingInviteeId in the URI. |
| `api.meetings.invitees.list` | `GET` | `/meetingInvitees` | Lists meeting invitees for a meeting with a specified meetingId. You can set a maximum number of invitees to |
| `api.meetings.invitees.update` | `PUT` | `/meetingInvitees/{meeting_invitee_id}` | Update details for a meeting invitee identified by a meetingInviteeId in the URI. |
| `api.meetings.join` | `POST` | `/meetings/join` | Retrieves a meeting join link for a meeting with a specified meetingId, meetingNumber, or webLink that allows |
| `api.meetings.list` | `GET` | `/meetings` | Retrieves details for meetings with a specified meeting number, web link, meeting type, etc. Please note that |
| `api.meetings.list_of_series` | `GET` | `/meetings` | Lists scheduled meeting and meeting instances of a meeting series identified by meetingSeriesId. Scheduled |
| `api.meetings.list_survey_results` | `GET` | `/meetings/{meeting_id}/surveyResults` | Retrieves results for a meeting survey identified by meetingId. |
| `api.meetings.list_tracking_codes` | `GET` | `/meetings/trackingCodes` | Lists tracking codes on a site by a meeting host. The result indicates which tracking codes and what options |
| `api.meetings.participants.admit_participants` | `POST` | `/meetingParticipants/admit` | To admit participants into a live meeting in bulk. |
| `api.meetings.participants.list_participants` | `GET` | `/meetingParticipants` | List all participants in a live or post meeting. The meetingId parameter is required, which is the unique |
| `api.meetings.participants.participant_details` | `GET` | `/meetingParticipants/{participant_id}` | Get a meeting participant details of a live or post meeting. The participantId is required to identify the |
| `api.meetings.participants.query_participants_with_email` | `POST` | `/meetingParticipants/query` | Query participants in a live meeting, or after the meeting, using participant's email. The meetingId parameter |
| `api.meetings.participants.update_participant` | `PUT` | `/meetingParticipants/{participant_id}` | To mute, un-mute, expel, or admit a participant in a live meeting. The participantId is required to identify |
| `api.meetings.patch` | `PATCH` | `/meetings/{meeting_id}` | Updates details for a meeting with a specified meeting ID. This operation applies to meeting series and |
| `api.meetings.preferences.audio_options` | `GET` | `/meetingPreferences/audio` | Retrieves audio options for the authenticated user. |
| `api.meetings.preferences.details` | `GET` | `/meetingPreferences` | Retrieves meeting preferences for the authenticated user. |
| `api.meetings.preferences.personal_meeting_room_options` | `GET` | `/meetingPreferences/personalMeetingRoom` | Retrieves the Personal Meeting Room options for the authenticated user. |
| `api.meetings.preferences.scheduling_options` | `GET` | `/meetingPreferences/schedulingOptions` | Retrieves scheduling options for the authenticated user. |
| `api.meetings.preferences.site_list` | `GET` | `/meetingPreferences/sites` | Retrieves the list of Webex sites that the authenticated user is set up to use. |
| `api.meetings.preferences.update_audio_options` | `PUT` | `/meetingPreferences/audio` | Updates audio options for the authenticated user. |
| `api.meetings.preferences.update_default_site` | `PUT` | `/meetingPreferences/sites` | Updates the default site for the authenticated user. |
| `api.meetings.preferences.update_personal_meeting_room_options` | `PUT` | `/meetingPreferences/personalMeetingRoom` | Update a single meeting |
| `api.meetings.preferences.update_scheduling_options` | `PUT` | `/meetingPreferences/schedulingOptions` | Updates scheduling options for the authenticated user. |
| `api.meetings.preferences.update_video_options` | `PUT` | `/meetingPreferences/video` | Updates video options for the authenticated user. |
| `api.meetings.preferences.video_options` | `GET` | `/meetingPreferences/video` | Retrieves video options for the authenticated user. |
| `api.meetings.qanda.list` | `GET` | `/meetings/q_and_a` | Lists questions and answers from a meeting, when ready. |
| `api.meetings.qanda.list_answers` | `GET` | `/meetings/q_and_a/{question_id}/answers` | Lists the answers to a specific question asked in a meeting. |
| `api.meetings.qualities.meeting_qualities` | `GET` | `https://analytics.webexapis.com/v1/meeting/qualities` | Get quality data for a meeting, by meetingId. Only organization administrators can retrieve meeting quality |
| `api.meetings.recordings.delete_a_recording` | `DELETE` | `/recordings/{recording_id}` | Delete a Recording |
| `api.meetings.recordings.get_recording_details` | `GET` | `/recordings/{recording_id}` | Get Recording Details |
| `api.meetings.recordings.list_recordings` | `GET` | `/recordings` | List Recordings |
| `api.meetings.recordings.list_recordings_for_an_admin_or_compliance_officer` | `GET` | `/admin/recordings` | List Recordings For an Admin or Compliance Officer |
| `api.meetings.recordings.move_recordings_into_the_recycle_bin` | `POST` | `/recordings/softDelete` | Move Recordings into the Recycle Bin |
| `api.meetings.recordings.purge_recordings_from_recycle_bin` | `POST` | `/recordings/purge` | Purge Recordings from Recycle Bin |
| `api.meetings.recordings.restore_recordings_from_recycle_bin` | `POST` | `/recordings/restore` | Restore Recordings from Recycle Bin |
| `api.meetings.survey` | `GET` | `/meetings/{meeting_id}/survey` | Retrieves details for a meeting survey identified by meetingId. |
| `api.meetings.transcripts.delete` | `DELETE` | `/meetingTranscripts/{transcript_id}` | Removes a transcript with a specified transcript ID. The deleted transcript cannot be recovered. If a |
| `api.meetings.transcripts.download` | `GET` | `/meetingTranscripts/{transcript_id}/download` | Download a meeting transcript from the meeting transcript specified by transcriptId. |
| `api.meetings.transcripts.list` | `GET` | `/meetingTranscripts` | Lists available transcripts of an ended meeting instance. |
| `api.meetings.transcripts.list_compliance_officer` | `GET` | `/admin/meetingTranscripts` | Lists available or deleted transcripts of an ended meeting instance for a specific site. |
| `api.meetings.transcripts.list_snippets` | `GET` | `/meetingTranscripts/{transcript_id}/snippets` | Lists snippets of a meeting transcript specified by transcriptId. |
| `api.meetings.transcripts.snippet_detail` | `GET` | `/meetingTranscripts/{transcript_id}/snippets/{snippet_id}` | Retrieves details for a transcript snippet specified by snippetId from the meeting transcript specified by |
| `api.meetings.transcripts.update_snippet` | `PUT` | `/meetingTranscripts/{transcript_id}/snippets/{snippet_id}` | Updates details for a transcript snippet specified by snippetId from the meeting transcript specified by |
| `api.meetings.update` | `PUT` | `/meetings/{meeting_id}` | Updates details for a meeting with a specified meeting ID. This operation applies to meeting series and |
| `api.meetings.update_simultaneous_interpretation` | `PUT` | `/meetings/{meeting_id}/simultaneousInterpretation` | Updates simultaneous interpretation options of a meeting with a specified meeting ID. This operation applies to |
| `api.membership.create` | `POST` | `/memberships` | Add someone to a room by Person ID or email address, optionally making them a moderator. |
| `api.membership.delete` | `DELETE` | `/memberships/{membership_id}` | Deletes a membership by ID. |
| `api.membership.details` | `GET` | `/memberships/{membership_id}` | Get details for a membership by ID. |
| `api.membership.list` | `GET` | `/memberships` | Lists all room memberships. By default, lists memberships for rooms to which the authenticated user belongs. |
| `api.membership.update` | `PUT` | `/memberships/{id}` | Updates properties for a membership by ID |
| `api.messages.create` | `POST` | `/messages` | Post a plain text, rich text or html message, and optionally, a file attachment, to a room. |
| `api.messages.delete` | `DELETE` | `/messages/{message_id}` | Delete a message, by message ID. |
| `api.messages.details` | `GET` | `/messages/{message_id}` | Show details for a message, by message ID. |
| `api.messages.edit` | `PUT` | `/messages/{id}` | Update a message you have posted not more than 10 times. |
| `api.messages.list` | `GET` | `/messages` | Lists all messages in a room.  Each message will include content attachments if present. |
| `api.messages.list_direct` | `GET` | `/messages/direct` | List all messages in a 1:1 (direct) room. Use the personId or personEmail query parameter to specify the |
| `api.org_contacts.bulk_create_or_update` | `POST` | `/contacts/organizations/{org_id}/contacts/bulk` | Bulk Create or Update Contacts |
| `api.org_contacts.bulk_delete` | `POST` | `/contacts/organizations/{org_id}/contacts/bulk/delete` | Bulk Delete Contacts |
| `api.org_contacts.create` | `POST` | `/contacts/organizations/{org_id}/contacts` | Create a Contact |
| `api.org_contacts.delete` | `DELETE` | `/contacts/organizations/{org_id}/contacts/{contact_id}` | Delete a Contact |
| `api.org_contacts.get` | `GET` | `/contacts/organizations/{org_id}/contacts/{contact_id}` | Get a Contact |
| `api.org_contacts.list` | `GET` | `/contacts/organizations/{org_id}/contacts/search` | List Contacts |
| `api.org_contacts.update` | `PATCH` | `/contacts/organizations/{org_id}/contacts/{contact_id}` | Update a Contact |
| `api.organizations.delete` | `DELETE` | `/organizations/{org_id}` | Delete Organization |
| `api.organizations.details` | `GET` | `/organizations/{org_id}` | Get Organization Details |
| `api.organizations.list` | `GET` | `/organizations` | List all organizations visible by your account. The results will not be paginated. |
| `api.people.create` | `POST` | `/people` | Create a Person |
| `api.people.delete_person` | `DELETE` | `/people/{person_id}` | Delete a Person |
| `api.people.details` | `GET` | `/people/{person_id}` | Get Person Details |
| `api.people.list` | `GET` | `/people` | List people in your organization. For most users, either the email or displayName parameter is required. Admin |
| `api.people.me` | `GET` | `/people/me` | Show the profile for the authenticated user. This is the same as GET /people/{personId} using the Person ID |
| `api.people.update` | `PUT` | `/people/{person_id}` | Update a Person |
| `api.person_settings.agent_caller_id.available_caller_ids` | `GET` | `/telephony/config/people/{entity_id}/agent/availableCallerIds` | Retrieve Agent's List of Available Caller IDs |
| `api.person_settings.agent_caller_id.configure` | `PUT` | `/telephony/config/people/{entity_id}/agent/callerId` | Modify Agent's Caller ID Information. |
| `api.person_settings.agent_caller_id.read` | `GET` | `/telephony/config/people/{entity_id}/agent/callerId` | Retrieve Agent's Caller ID Information |
| `api.person_settings.app_shared_line.get_members` | `GET` | `/telephony/config/people/{person_id}/applications/members` | Get Shared-Line Appearance Members |
| `api.person_settings.app_shared_line.members_count` | `GET` | `/telephony/config/people/{person_id}/applications/availableMembers/count` | Get Count of Shared-Line Appearance Members |
| `api.person_settings.app_shared_line.search_members` | `GET` | `/telephony/config/people/{person_id}/applications/availableMembers` | Search Shared-Line Appearance Members |
| `api.person_settings.app_shared_line.update_members` | `PUT` | `/telephony/config/people/{person_id}/applications/members` | Put Shared-Line Appearance Members New |
| `api.person_settings.appservices.configure` | `PUT` | `/people/{person_id}/features/applications` | Modify a person's Application Services Settings |
| `api.person_settings.appservices.read` | `GET` | `/people/{person_id}/features/applications` | Retrieve a person's Application Services Settings New |
| `api.person_settings.appservices.shared_line.get_members` | `GET` | `/telephony/config/people/{person_id}/applications/members` | Get Shared-Line Appearance Members |
| `api.person_settings.appservices.shared_line.members_count` | `GET` | `/telephony/config/people/{person_id}/applications/availableMembers/count` | Get Count of Shared-Line Appearance Members |
| `api.person_settings.appservices.shared_line.search_members` | `GET` | `/telephony/config/people/{person_id}/applications/availableMembers` | Search Shared-Line Appearance Members |
| `api.person_settings.appservices.shared_line.update_members` | `PUT` | `/telephony/config/people/{person_id}/applications/members` | Put Shared-Line Appearance Members New |
| `api.person_settings.available_numbers.available` | `GET` | `/` | Get Available Phone Numbers |
| `api.person_settings.available_numbers.call_forward` | `GET` | `/telephony/config/people/{entity_id}/callForwarding/availableNumbers` | Get Call Forward Available Phone Numbers |
| `api.person_settings.available_numbers.call_intercept` | `GET` | `/telephony/config/people/{entity_id}/callIntercept/availableNumbers` | Get Call Intercept Available Phone Numbers |
| `api.person_settings.available_numbers.ecbn` | `GET` | `/telephony/config/people/{entity_id}/emergencyCallbackNumber/availableNumbers` | Get ECBN Available Phone Numbers |
| `api.person_settings.available_numbers.fax_message` | `GET` | `/telephony/config/people/{entity_id}/faxMessage/availableNumbers` | Get Fax Message Available Phone Numbers |
| `api.person_settings.available_numbers.primary` | `GET` | `/telephony/config/people/primary/availableNumbers` | Get Person Primary Available Phone Numbers |
| `api.person_settings.available_numbers.secondary` | `GET` | `/telephony/config/people/{entity_id}/secondary/availableNumbers` | Get Person Secondary Available Phone Numbers |
| `api.person_settings.barge.configure` | `PUT` | `/people/{entity_id}/features/bargeIn` | Configure Barge In Settings |
| `api.person_settings.barge.read` | `GET` | `/people/{entity_id}/features/bargeIn` | Retrieve Barge In Settings |
| `api.person_settings.call_bridge.configure` | `PUT` | `/telephony/config/people/{entity_id}/features/callBridge` | Configure Call Bridge Settings |
| `api.person_settings.call_bridge.read` | `GET` | `/telephony/config/people/{entity_id}/features/callBridge` | Read Call Bridge Settings |
| `api.person_settings.call_intercept.configure` | `PUT` | `/people/{entity_id}/features/intercept` | Configure Call Intercept Settings |
| `api.person_settings.call_intercept.greeting` | `POST` | `/people/{entity_id}/features/intercept/actions/announcementUpload/invoke` | Configure Call Intercept Greeting |
| `api.person_settings.call_intercept.read` | `GET` | `/people/{entity_id}/features/intercept` | Read Call Intercept Settings |
| `api.person_settings.call_recording.configure` | `PUT` | `/people/{entity_id}/features/callRecording` | Configure Call Recording Settings for a entity |
| `api.person_settings.call_recording.read` | `GET` | `/people/{entity_id}/features/callRecording` | Read Call Recording Settings |
| `api.person_settings.call_waiting.configure` | `PUT` | `/people/{entity_id}/features/callWaiting` | Configure Call Waiting Settings |
| `api.person_settings.call_waiting.read` | `GET` | `/people/{entity_id}/features/callWaiting` | Read Call Waiting Settings for |
| `api.person_settings.caller_id.configure` | `PUT` | `/people/{entity_id}/features/callerId` | Configure a Caller ID Settings |
| `api.person_settings.caller_id.configure_settings` | `PUT` | `/people/{entity_id}/features/callerId` | Configure a Caller ID Settings |
| `api.person_settings.caller_id.read` | `GET` | `/people/{entity_id}/features/callerId` | Retrieve Caller ID Settings |
| `api.person_settings.calling_behavior.configure` | `PUT` | `/people/{person_id}/features/callingBehavior` | Configure a Person's Calling Behavior |
| `api.person_settings.calling_behavior.read` | `GET` | `/people/{person_id}/features/callingBehavior` | Read Person's Calling Behavior |
| `api.person_settings.devices` | `GET` | `/telephony/config/people/{person_id}/devices` | Get all devices for a person. |
| `api.person_settings.dnd.configure` | `PUT` | `/people/{entity_id}/features/doNotDisturb` | Configure Do Not Disturb Settings for an entity |
| `api.person_settings.dnd.read` | `GET` | `/people/{entity_id}/features/doNotDisturb` | Read Do Not Disturb Settings for an entity |
| `api.person_settings.ecbn.configure` | `PUT` | `/telephony/config/people/{entity_id}/emergencyCallbackNumber` | Update an entity's Emergency Callback Number. |
| `api.person_settings.ecbn.dependencies` | `GET` | `/telephony/config/people/{entity_id}/emergencyCallbackNumber/dependencies` | Retrieve an entity's Emergency Callback Number Dependencies |
| `api.person_settings.ecbn.read` | `GET` | `/telephony/config/people/{entity_id}/emergencyCallbackNumber` | Get an entity's Emergency Callback Number |
| `api.person_settings.exec_assistant.configure` | `PUT` | `/people/{person_id}/features/executiveAssistant` | Modify Executive Assistant Settings for a Person |
| `api.person_settings.exec_assistant.read` | `GET` | `/people/{person_id}/features/executiveAssistant` | Retrieve Executive Assistant Settings for a Person |
| `api.person_settings.executive.alert_settings` | `GET` | `/telephony/config/people/{person_id}/executive/alert` | Get Person Executive Alert Settings |
| `api.person_settings.executive.assigned_assistants` | `GET` | `/telephony/config/people/{person_id}/executive/assignedAssistants` | Get Person Executive Assigned Assistants |
| `api.person_settings.executive.create_call_filtering_criteria` | `POST` | `/telephony/config/people/{person_id}/executive/callFiltering/criteria` | Add Person Executive Call Filtering Criteria |
| `api.person_settings.executive.delete_call_filtering_criteria` | `DELETE` | `/telephony/config/people/{person_id}/executive/callFiltering/criteria/{id}` | Delete Person Executive Call Filtering Criteria |
| `api.person_settings.executive.executive_assistant_settings` | `GET` | `/telephony/config/people/{person_id}/executive/assistant` | Get Person Executive Assistant Settings |
| `api.person_settings.executive.executive_available_assistants` | `GET` | `/telephony/config/people/{person_id}/executive/availableAssistants` | Get Person Executive Available Assistants |
| `api.person_settings.executive.executive_call_filtering_settings` | `GET` | `/telephony/config/people/{person_id}/executive/callFiltering` | Get Person Executive Call Filtering Settings |
| `api.person_settings.executive.get_filtering_criteria` | `GET` | `/telephony/config/people/{person_id}/executive/callFiltering/criteria/{id}` | Get Person Executive Call Filtering Criteria Settings |
| `api.person_settings.executive.screening_settings` | `GET` | `/telephony/config/people/{person_id}/executive/screening` | Get Person Executive Screening Settings |
| `api.person_settings.executive.update_alert_settings` | `PUT` | `/telephony/config/people/{person_id}/executive/alert` | Modify Person Executive Alert Settings |
| `api.person_settings.executive.update_assigned_assistants` | `PUT` | `/telephony/config/people/{person_id}/executive/assignedAssistants` | Modify Person Executive Assigned Assistants |
| `api.person_settings.executive.update_call_filtering_criteria` | `PUT` | `/telephony/config/people/{person_id}/executive/callFiltering/criteria/{id}` | Modify Person Executive Call Filtering Criteria Settings |
| `api.person_settings.executive.update_executive_assistant_settings` | `PUT` | `/telephony/config/people/{person_id}/executive/assistant` | Modify Person Executive Assistant Settings |
| `api.person_settings.executive.update_executive_call_filtering_settings` | `PUT` | `/telephony/config/people/{person_id}/executive/callFiltering` | Modify Person Executive Call Filtering Settings |
| `api.person_settings.executive.update_screening_settings` | `PUT` | `/telephony/config/people/{person_id}/executive/screening` | Modify Person Executive Screening Settings |
| `api.person_settings.feature_access.read` | `GET` | `/telephony/config/people/{person_id}/settings/permissions` | Read Feature Access Settings for a Person |
| `api.person_settings.feature_access.read_default` | `GET` | `/telephony/config/people/settings/permissions` | Read Default Feature Access Settings for Person |
| `api.person_settings.feature_access.reset` | `POST` | `/telephony/config/people/{person_id}/settings/permissions/actions/reset/invoke` | Reset a Person’s Feature Access Configuration to the Organization’s Default Settings |
| `api.person_settings.feature_access.update` | `PUT` | `/telephony/config/people/{person_id}/settings/permissions` | Update a Person’s Feature Access Configuration |
| `api.person_settings.feature_access.update_default` | `PUT` | `/telephony/config/people/settings/permissions` | Update Default Person Feature Access Configuration |
| `api.person_settings.forwarding.configure` | `PUT` | `/people/{entity_id}/features/callForwarding` | Configure an Entity's Call Forwarding Settings |
| `api.person_settings.forwarding.read` | `GET` | `/people/{entity_id}/features/callForwarding` | Retrieve an entity's Call Forwarding Settings |
| `api.person_settings.get_call_captions_settings` | `GET` | `/telephony/config/people/{person_id}/callCaptions` | Get the user call captions settings |
| `api.person_settings.hoteling.configure` | `PUT` | `/people/{person_id}/features/hoteling` | Configure Hoteling Settings for a Person |
| `api.person_settings.hoteling.read` | `GET` | `/people/{person_id}/features/hoteling` | Read Hoteling Settings for a Person |
| `api.person_settings.mode_management.assign_features` | `PUT` | `/telephony/config/people/{person_id}/modeManagement/features` | Assign a List of Features to a User for Mode Management. |
| `api.person_settings.mode_management.assigned_features` | `GET` | `/telephony/config/people/{person_id}/modeManagement/features` | Retrieve the List of Features Assigned to a User for Mode Management. |
| `api.person_settings.mode_management.available_features` | `GET` | `/telephony/config/people/{person_id}/modeManagement/availableFeatures` | Retrieve the List of Available Features. |
| `api.person_settings.modify_hoteling_settings_primary_devices` | `PUT` | `/telephony/config/people/{person_id}/devices/settings/hoteling` | Modify Hoteling Settings for a Person's Primary Devices |
| `api.person_settings.monitoring.configure` | `PUT` | `/people/{entity_id}/features/monitoring` | Modify an entity's Monitoring Settings |
| `api.person_settings.monitoring.read` | `GET` | `/people/{entity_id}/features/monitoring` | Retrieve an entity's Monitoring Settings |
| `api.person_settings.ms_teams.configure` | `PUT` | `/telephony/config/people/{person_id}/settings/msTeams` | Configure a Person's MS Teams Setting |
| `api.person_settings.ms_teams.read` | `GET` | `/telephony/config/people/{person_id}/settings/msTeams` | Retrieve a Person's MS Teams Settings |
| `api.person_settings.music_on_hold.configure` | `PUT` | `/telephony/config/people/{entity_id}/musicOnHold` | Configure Music On Hold Settings for a Personvirtual line, or workspace. |
| `api.person_settings.music_on_hold.read` | `GET` | `/telephony/config/people/{entity_id}/musicOnHold` | Retrieve Music On Hold Settings for a Person, virtual line, or workspace. |
| `api.person_settings.numbers.read` | `GET` | `/people/{person_id}/features/numbers` | Get a person's phone numbers including alternate numbers. |
| `api.person_settings.numbers.update` | `PUT` | `/telephony/config/people/{person_id}/numbers` | Assign or unassign alternate phone numbers to a person. |
| `api.person_settings.permissions_in.configure` | `PUT` | `/people/{entity_id}/features/incomingPermission` | Configure incoming permissions settings |
| `api.person_settings.permissions_in.read` | `GET` | `/people/{entity_id}/features/incomingPermission` | Read Incoming Permission Settings |
| `api.person_settings.permissions_out.access_codes.create` | `POST` | `/telephony/config/people/{entity_id}/outgoingPermission/accessCodes` | Create new Access codes. |
| `api.person_settings.permissions_out.access_codes.delete` | `DELETE` | `/telephony/config/people/{entity_id}/outgoingPermission/accessCodes` | Delete Access Code |
| `api.person_settings.permissions_out.access_codes.modify` | `PUT` | `/telephony/config/people/{entity_id}/outgoingPermission/accessCodes` | Modify Access Codes |
| `api.person_settings.permissions_out.access_codes.read` | `GET` | `/telephony/config/people/{entity_id}/outgoingPermission/accessCodes` | Retrieve Access codes. |
| `api.person_settings.permissions_out.configure` | `PUT` | `/people/{entity_id}/features/outgoingPermission` | Configure Outgoing Calling Permissions Settings |
| `api.person_settings.permissions_out.digit_patterns.create` | `POST` | `/telephony/config/people/{entity_id}/outgoingPermission/digitPatterns` | Create Digit Patterns |
| `api.person_settings.permissions_out.digit_patterns.delete` | `DELETE` | `/telephony/config/people/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}` | Delete a Digit Pattern |
| `api.person_settings.permissions_out.digit_patterns.delete_all` | `DELETE` | `/telephony/config/people/{entity_id}/outgoingPermission/digitPatterns` | Delete all Digit Patterns. |
| `api.person_settings.permissions_out.digit_patterns.details` | `GET` | `/telephony/config/people/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}` | Retrieve Digit Pattern Details |
| `api.person_settings.permissions_out.digit_patterns.get_digit_patterns` | `GET` | `/telephony/config/people/{entity_id}/outgoingPermission/digitPatterns` | Retrieve Digit Patterns |
| `api.person_settings.permissions_out.digit_patterns.update` | `PUT` | `/telephony/config/people/{entity_id}/outgoingPermission/digitPatterns/{id}` | Modify Digit Patterns |
| `api.person_settings.permissions_out.digit_patterns.update_category_control_settings` | `PUT` | `/telephony/config/people/{entity_id}/outgoingPermission/digitPatterns` | Modify the Digit Pattern Category Control Settings for the entity |
| `api.person_settings.permissions_out.read` | `GET` | `/people/{entity_id}/features/outgoingPermission` | Retrieve Outgoing Calling Permissions Settings |
| `api.person_settings.permissions_out.transfer_numbers.configure` | `PUT` | `/people/{entity_id}/features/outgoingPermission/autoTransferNumbers` | Modify Transfer Numbers Settings for an entity. |
| `api.person_settings.permissions_out.transfer_numbers.read` | `GET` | `/people/{entity_id}/features/outgoingPermission/autoTransferNumbers` | Retrieve Transfer Numbers Settings . |
| `api.person_settings.personal_assistant.get` | `GET` | `/telephony/config/people/{person_id}/features/personalAssistant` | Get Personal Assistant |
| `api.person_settings.personal_assistant.update` | `PUT` | `/telephony/config/people/{person_id}/features/personalAssistant` | Update Personal Assistant |
| `api.person_settings.preferred_answer.modify` | `PUT` | `/telephony/config/people/{person_id}/preferredAnswerEndpoint` | Modify Preferred Answer Endpoint |
| `api.person_settings.preferred_answer.read` | `GET` | `/telephony/config/people/{person_id}/preferredAnswerEndpoint` | Get Preferred Answer Endpoint |
| `api.person_settings.privacy.configure` | `PUT` | `/people/{entity_id}/features/privacy` | Configure an entity's Privacy Settings |
| `api.person_settings.privacy.read` | `GET` | `/people/{entity_id}/features/privacy` | Get Privacy Settings for an entity |
| `api.person_settings.push_to_talk.configure` | `PUT` | `/people/{entity_id}/features/pushToTalk` | Configure Push-to-Talk Settings for an entity |
| `api.person_settings.push_to_talk.read` | `GET` | `/people/{entity_id}/features/pushToTalk` | Read Push-to-Talk Settings for an entity |
| `api.person_settings.receptionist.configure` | `PUT` | `/people/{person_id}/features/reception` | Modify Executive Assistant Settings for a Person |
| `api.person_settings.receptionist.read` | `GET` | `/people/{person_id}/features/reception` | Read Receptionist Client Settings for a Person |
| `api.person_settings.reset_vm_pin` | `POST` | `/people/{person_id}/features/voicemail/actions/resetPin/invoke` | Reset Voicemail PIN |
| `api.person_settings.schedules.create` | `POST` | `/people/{obj_id}/features/schedules` | Create a schedule |
| `api.person_settings.schedules.delete_schedule` | `DELETE` | `/people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}` | Delete a schedule |
| `api.person_settings.schedules.details` | `GET` | `/people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}` | Get details for a schedule |
| `api.person_settings.schedules.event_create` | `POST` | `/people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}/events` | Create a schedule event |
| `api.person_settings.schedules.event_delete` | `DELETE` | `/people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}` | Delete a schedule event |
| `api.person_settings.schedules.event_details` | `GET` | `/people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}` | Get details for a schedule event |
| `api.person_settings.schedules.event_update` | `PUT` | `/people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}/events/{event_id}` | Update a schedule event |
| `api.person_settings.schedules.list` | `GET` | `/people/{obj_id}/features/schedules` | List of schedules for a person or location |
| `api.person_settings.schedules.update` | `PUT` | `/people/{obj_id}/features/schedules/{schedule_type}/{schedule_id}` | Update a schedule |
| `api.person_settings.selective_accept.configure` | `PUT` | `/telephony/config/people/{entity_id}/selectiveAccept` | Modify Selective Accept Settings for an entity. |
| `api.person_settings.selective_accept.configure_criteria` | `PUT` | `/telephony/config/people/{entity_id}/selectiveAccept/criteria/{id}` | Modify Selective Accept Criteria for an entity |
| `api.person_settings.selective_accept.create_criteria` | `POST` | `/telephony/config/people/{entity_id}/selectiveAccept/criteria` | Create Selective Accept Criteria for an entity |
| `api.person_settings.selective_accept.delete_criteria` | `DELETE` | `/telephony/config/people/{entity_id}/selectiveAccept/criteria/{id}` | Delete Selective Accept Criteria for an entity |
| `api.person_settings.selective_accept.read` | `GET` | `/telephony/config/people/{entity_id}/selectiveAccept` | Retrieve Selective Accept Settings for an entity. |
| `api.person_settings.selective_accept.read_criteria` | `GET` | `/telephony/config/people/{entity_id}/selectiveAccept/criteria/{id}` | Retrieve Selective Accept Criteria for an entity |
| `api.person_settings.selective_forward.configure` | `PUT` | `/telephony/config/people/{entity_id}/selectiveForward` | Modify Selective Forward Settings for a Workspace |
| `api.person_settings.selective_forward.configure_criteria` | `PUT` | `/telephony/config/people/{entity_id}/selectiveForward/criteria/{id}` | Modify Selective Forward Criteria for a Workspace |
| `api.person_settings.selective_forward.create_criteria` | `POST` | `/telephony/config/people/{entity_id}/selectiveForward/criteria` | Create Selective Forward Criteria for a Workspace |
| `api.person_settings.selective_forward.delete_criteria` | `DELETE` | `/telephony/config/people/{entity_id}/selectiveForward/criteria/{id}` | Delete Selective Forward Criteria for a Workspace |
| `api.person_settings.selective_forward.read` | `GET` | `/telephony/config/people/{entity_id}/selectiveForward` | Retrieve Selective Forward Settings for a Workspace |
| `api.person_settings.selective_forward.read_criteria` | `GET` | `/telephony/config/people/{entity_id}/selectiveForward/criteria/{id}` | Retrieve Selective Forward Criteria for a Workspace |
| `api.person_settings.selective_reject.configure` | `PUT` | `/telephony/config/people/{entity_id}/selectiveReject` | Modify Selective Reject Settings for an entity. |
| `api.person_settings.selective_reject.configure_criteria` | `PUT` | `/telephony/config/people/{entity_id}/selectiveReject/criteria/{id}` | Modify Selective Reject Criteria for an entity |
| `api.person_settings.selective_reject.create_criteria` | `POST` | `/telephony/config/people/{entity_id}/selectiveReject/criteria` | Create Selective Reject Criteria for an entity |
| `api.person_settings.selective_reject.delete_criteria` | `DELETE` | `/telephony/config/people/{entity_id}/selectiveReject/criteria/{id}` | Delete Selective Reject Criteria for an entity |
| `api.person_settings.selective_reject.read` | `GET` | `/telephony/config/people/{entity_id}/selectiveReject` | Retrieve Selective Reject Settings for an entity. |
| `api.person_settings.selective_reject.read_criteria` | `GET` | `/telephony/config/people/{entity_id}/selectiveReject/criteria/{id}` | Retrieve Selective Reject Criteria for an entity |
| `api.person_settings.single_number_reach.available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/singleNumberReach/availableNumbers` | Get Single Number Reach Primary Available Phone Numbers |
| `api.person_settings.single_number_reach.create_snr` | `POST` | `/telephony/config/people/{person_id}/singleNumberReach/numbers` | Create Single Number Reach For a Person |
| `api.person_settings.single_number_reach.delete_snr` | `DELETE` | `/telephony/config/people/{person_id}/singleNumberReach/numbers/{id}` | Delete A Single Number Reach Number |
| `api.person_settings.single_number_reach.read` | `GET` | `/telephony/config/people/{person_id}/singleNumberReach` | Get Single Number Reach Settings For A Person |
| `api.person_settings.single_number_reach.update` | `PUT` | `/telephony/config/people/{person_id}/singleNumberReach` | Update Single number reach settings for a person. |
| `api.person_settings.single_number_reach.update_snr` | `PUT` | `/telephony/config/people/{person_id}/singleNumberReach/numbers/{id}` | Update Single number reach settings for a number. |
| `api.person_settings.update_call_captions_settings` | `PUT` | `/telephony/config/people/{person_id}/callCaptions` | Update the user call captions settings |
| `api.person_settings.voicemail.configure` | `PUT` | `/people/{entity_id}/features/voicemail` | Configure Voicemail Settings for an entity |
| `api.person_settings.voicemail.modify_passcode` | `PUT` | `/telephony/config/people/{entity_id}/voicemail/passcode` | Modify an entity's voicemail passcode. |
| `api.person_settings.voicemail.read` | `GET` | `/people/{entity_id}/features/voicemail` | Read Voicemail Settings for an entity |
| `api.person_settings.voicemail.reset_pin` | `POST` | `/people/{entity_id}/features/voicemail/actions/resetPin/invoke` | Reset Voicemail PIN |
| `api.reports.create` | `POST` | `/reports` | Create a new report. For each templateId, there are a set of validation rules that need to be followed. For |
| `api.reports.delete` | `DELETE` | `/reports/{report_id}` | Remove a report from the system. |
| `api.reports.details` | `GET` | `/reports/{report_id}` | Shows details for a report, by report ID. |
| `api.reports.download` | `GET` | `{url}` | Download a report from the given URL and yield the rows as dicts |
| `api.reports.list` | `GET` | `/reports` | Lists all reports. Use query parameters to filter the response. The parameters are optional. However, `from` |
| `api.reports.list_templates` | `GET` | `/report/templates` | List all the available report templates that can be generated. |
| `api.roles.details` | `GET` | `/roles/{role_id}` | Get Role Details |
| `api.roles.list` | `GET` | `/roles` | List Roles |
| `api.room_tabs.create_tab` | `POST` | `/room/tabs` | Add a tab with a specified URL to a room. |
| `api.room_tabs.delete_tab` | `DELETE` | `/room/tabs/{tab_id}` | Deletes a Room Tab with the specified ID. |
| `api.room_tabs.list_tabs` | `GET` | `/room/tabs` | Lists all Room Tabs of a room specified by the roomId query parameter. |
| `api.room_tabs.tab_details` | `GET` | `/room/tabs/{tab_id}` | Get details for a Room Tab with the specified room tab ID. |
| `api.room_tabs.update_tab` | `PUT` | `/room/tabs/{tab_id}` | Updates the content URL of the specified Room Tab ID. |
| `api.rooms.create` | `POST` | `/rooms` | Creates a room. The authenticated user is automatically added as a member of the room. See the Memberships |
| `api.rooms.delete` | `DELETE` | `/rooms/{room_id}` | Deletes a room, by ID. Deleted rooms cannot be recovered. |
| `api.rooms.details` | `GET` | `/rooms/{room_id}` | Shows details for a room, by ID. |
| `api.rooms.list` | `GET` | `/rooms` | List rooms. |
| `api.rooms.meeting_details` | `GET` | `/rooms/{room_id}/meetingInfo` | The meetingInfo API is deprecated and will be EOL on Jan 31, 2025. Meetings in the WSMP must be scheduled and |
| `api.rooms.update` | `PUT` | `/rooms/{id}` | Updates details for a room, by ID. |
| `api.scim.bulk.bulk_request` | `POST` | `https://webexapis.com/identity/scim/{org_id}/v2/Bulk` | User bulk API |
| `api.scim.groups.create` | `POST` | `https://webexapis.com/identity/scim/{org_id}/v2/Groups` | Create a group |
| `api.scim.groups.delete` | `DELETE` | `https://webexapis.com/identity/scim/{org_id}/v2/Groups/{group_id}` | Delete a group |
| `api.scim.groups.details` | `GET` | `https://webexapis.com/identity/scim/{org_id}/v2/Groups/{group_id}` | Get a group |
| `api.scim.groups.members` | `GET` | `https://webexapis.com/identity/scim/{org_id}/v2/Groups/{group_id}/Members` | Get Group Members |
| `api.scim.groups.patch` | `PATCH` | `https://webexapis.com/identity/scim/{org_id}/v2/Groups/{group_id}` | Update a group with PATCH |
| `api.scim.groups.search` | `GET` | `https://webexapis.com/identity/scim/{org_id}/v2/Groups` | Search groups |
| `api.scim.groups.update` | `PUT` | `https://webexapis.com/identity/scim/{org_id}/v2/Groups/{id}` | Update a group with PUT |
| `api.scim.users.create` | `POST` | `https://webexapis.com/identity/scim/{org_id}/v2/Users` | Create a user |
| `api.scim.users.delete` | `DELETE` | `https://webexapis.com/identity/scim/{org_id}/v2/Users/{user_id}` | Delete a user |
| `api.scim.users.details` | `GET` | `https://webexapis.com/identity/scim/{org_id}/v2/Users/{user_id}` | Get a user |
| `api.scim.users.patch` | `PATCH` | `https://webexapis.com/identity/scim/{org_id}/v2/Users/{user_id}` | Update a user with PATCH |
| `api.scim.users.search` | `GET` | `https://webexapis.com/identity/scim/{org_id}/v2/Users` | Search users |
| `api.scim.users.update` | `PUT` | `https://webexapis.com/identity/scim/{org_id}/v2/Users/{id}` | Update a user with PUT |
| `api.status.active_scheduled_maintenances` | `GET` | `https://status.webex.com/active-scheduled-maintenances.json` | Get a list of any active maintenances. This response will only return scheduled maintenances in the In |
| `api.status.all_incidents` | `GET` | `https://status.webex.com/all-incidents.json` | Get a list of the 50 most recent incidents. This includes all unresolved incidents as described above, |
| `api.status.all_scheduled_maintenances` | `GET` | `https://status.webex.com/all-scheduled-maintenances.json` | Get a list of the 50 most recent scheduled maintenances. This includes scheduled maintenances in Scheduled , |
| `api.status.components` | `GET` | `https://status.webex.com/components.json` | Get the components for the status page. Each component is listed along with its status - one of operational, |
| `api.status.status` | `GET` | `/status` | Get the status rollup for the whole page. This response includes an indicator - one of green (operational), |
| `api.status.summary` | `GET` | `https://status.webex.com/index.json` | Get a summary of the status page, including a status indicator, component statuses, unresolved incidents, |
| `api.status.unresolved_incidents` | `GET` | `https://status.webex.com/unresolved-incidents.json` | Get a list of any unresolved incidents. This response will only return incidents in the Investigating, |
| `api.status.upcoming_scheduled_maintenances` | `GET` | `https://status.webex.com/upcoming-scheduled-maintenances.json` | Scheduled maintenances are planned outages, upgrades, or general notices that you're working on |
| `api.team_memberships.create` | `POST` | `/team/memberships` | Add someone to a team by Person ID or email address, optionally making them a moderator. |
| `api.team_memberships.delete` | `DELETE` | `/team/memberships/{membership_id}` | Deletes a team membership, by ID. |
| `api.team_memberships.details` | `GET` | `/team/memberships/{membership_id}` | Shows details for a team membership, by ID. |
| `api.team_memberships.list` | `GET` | `/team/memberships` | Lists all team memberships for a given team, specified by the teamId query parameter. |
| `api.team_memberships.membership` | `PUT` | `/team/memberships/{membership_id}` | Updates a team membership, by ID. |
| `api.teams.create` | `POST` | `/teams` | Creates a team. |
| `api.teams.delete` | `DELETE` | `/teams/{team_id}` | Deletes a team, by ID. |
| `api.teams.details` | `GET` | `/teams/{team_id}` | Shows details for a team, by ID. |
| `api.teams.list` | `GET` | `/teams` | Lists teams to which the authenticated user belongs. |
| `api.teams.update` | `PUT` | `/teams/{team_id}` | Updates details for a team, by ID. |
| `api.telephony.access_codes.create` | `POST` | `/telephony/config/locations/{location_id}/outgoingPermission/accessCodes` | Create Outgoing Permission a new access code for a customer location |
| `api.telephony.access_codes.delete_all` | `DELETE` | `/telephony/config/locations/{location_id}/outgoingPermission/accessCodes` | Delete Outgoing Permission Location Access Codes |
| `api.telephony.access_codes.delete_codes` | `PUT` | `/telephony/config/locations/{location_id}/outgoingPermission/accessCodes` | Delete Access Code Location |
| `api.telephony.access_codes.read` | `GET` | `/telephony/config/locations/{location_id}/outgoingPermission/accessCodes` | Get Outgoing Permission Location Access Code |
| `api.telephony.announcements_repo.delete` | `DELETE` | `/telephony/config/announcements/{announcement_id}` | Delete an announcement greeting. |
| `api.telephony.announcements_repo.details` | `GET` | `/telephony/config/announcements/{announcement_id}` | Fetch details of a binary announcement greeting at the organization or location level |
| `api.telephony.announcements_repo.list` | `GET` | `/telephony/config/announcements` | Fetch list of announcement greetings on location and organization level |
| `api.telephony.announcements_repo.modify` | `PUT` | `/telephony/config/announcements/{announcement_id}` | Modify a binary announcement greeting at organization or location level |
| `api.telephony.announcements_repo.upload_announcement` | `POST` | `/telephony/config/announcements` | Upload a binary announcement greeting at organization or location level |
| `api.telephony.announcements_repo.usage` | `GET` | `/telephony/config/announcements/usage` | Fetch repository usage for announcements for an organization or location |
| `api.telephony.auto_attendant.alternate_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/autoAttendants/alternate/availableNumbers` | Get Auto Attendant Alternate Available Phone Numbers |
| `api.telephony.auto_attendant.call_forward_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/autoAttendants/callForwarding/availableNumbers` | Get Auto Attendant Call Forward Available Phone Numbers |
| `api.telephony.auto_attendant.create` | `POST` | `/telephony/config/locations/{location_id}/autoAttendants` | Create an Auto Attendant |
| `api.telephony.auto_attendant.delete_announcement_file` | `DELETE` | `/telephony/config/locations/{location_id}/autoAttendants/{auto_attendant_id}/announcements/{file_name}` | Delete an Auto Attendant Announcement File |
| `api.telephony.auto_attendant.delete_auto_attendant` | `DELETE` | `/telephony/config/locations/{location_id}/autoAttendants/{auto_attendant_id}` | elete the designated Auto Attendant. |
| `api.telephony.auto_attendant.details` | `GET` | `/telephony/config/locations/{location_id}/autoAttendants/{auto_attendant_id}` | Get Details for an Auto Attendant |
| `api.telephony.auto_attendant.forwarding.call_forwarding_rule` | `GET` | `/telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding/selectiveRules/{rule_id}` | Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue. |
| `api.telephony.auto_attendant.forwarding.create_call_forwarding_rule` | `POST` | `/telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding/selectiveRules` | Create a Selective Call Forwarding Rule feature |
| `api.telephony.auto_attendant.forwarding.delete_call_forwarding_rule` | `DELETE` | `/telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding/selectiveRules/{rule_id}` | Delete a Selective Call Forwarding Rule for the designated feature. |
| `api.telephony.auto_attendant.forwarding.settings` | `GET` | `/telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding` | Retrieve Call Forwarding settings for the designated feature including the list of call |
| `api.telephony.auto_attendant.forwarding.switch_mode_for_call_forwarding` | `POST` | `/telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding/actions/switchMode/invoke` | Switch Mode for Call Forwarding Settings for an entity |
| `api.telephony.auto_attendant.forwarding.update` | `PUT` | `/telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding` | Update Call Forwarding Settings for a feature |
| `api.telephony.auto_attendant.forwarding.update_call_forwarding_rule` | `PUT` | `/telephony/config/locations/{location_id}/autoAttendants/{feature_id}/callForwarding/selectiveRules/{rule_id}` | Update a Selective Call Forwarding Rule's settings for the designated feature. |
| `api.telephony.auto_attendant.list` | `GET` | `/telephony/config/autoAttendants` | Read the List of Auto Attendants |
| `api.telephony.auto_attendant.list_announcement_files` | `GET` | `/telephony/config/locations/{location_id}/autoAttendants/{auto_attendant_id}/announcements` | Read the List of Auto Attendant Announcement Files |
| `api.telephony.auto_attendant.primary_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/autoAttendants/availableNumbers` | Get Auto Attendant Primary Available Phone Numbers |
| `api.telephony.auto_attendant.update` | `PUT` | `/telephony/config/locations/{location_id}/autoAttendants/{auto_attendant_id}` | Update an Auto Attendant |
| `api.telephony.call_controls_members.answer` | `POST` | `/telephony/calls/members/{member_id}/answer` | Answer by Member ID |
| `api.telephony.call_controls_members.dial` | `POST` | `/telephony/calls/members/{member_id}/dial` | Dial by Member ID |
| `api.telephony.call_controls_members.get_call_details` | `GET` | `/telephony/calls/members/{member_id}/calls/{call_id}` | Get Call Details by Member ID |
| `api.telephony.call_controls_members.hangup` | `POST` | `/telephony/calls/members/{member_id}/hangup` | Hangup by Member ID |
| `api.telephony.call_controls_members.list_calls` | `GET` | `/telephony/calls/members/{member_id}/calls` | List Calls by Member ID |
| `api.telephony.call_intercept.configure` | `PUT` | `/telephony/config/locations/{location_id}/intercept` | Put Location Intercept |
| `api.telephony.call_intercept.read` | `GET` | `/telephony/config/locations/{location_id}/intercept` | Get Location Intercept |
| `api.telephony.call_recording.get_call_recording_regions` | `GET` | `/telephony/config/callRecording/regions` | Get Call Recording Regions |
| `api.telephony.call_recording.get_location_vendors` | `GET` | `/telephony/config/locations/{location_id}/callRecording/vendors` | Get Location Call Recording Vendors |
| `api.telephony.call_recording.get_org_vendors` | `GET` | `/telephony/config/callRecording/vendors` | Get Organization Call Recording Vendors |
| `api.telephony.call_recording.list_location_users` | `GET` | `/telephony/config/locations/{location_id}/callRecording/vendorUsers` | Get Call Recording Vendor Users for a Location |
| `api.telephony.call_recording.list_org_users` | `GET` | `/telephony/config/callRecording/vendorUsers` | Get Call Recording Vendor Users |
| `api.telephony.call_recording.read` | `GET` | `/telephony/config/callRecording` | Get Call Recording Settings |
| `api.telephony.call_recording.read_location_compliance_announcement` | `GET` | `/telephony/config/locations/{location_id}/callRecording/complianceAnnouncement` | Get details for the Location Compliance Announcement Setting |
| `api.telephony.call_recording.read_org_compliance_announcement` | `GET` | `/telephony/config/callRecording/complianceAnnouncement` | Get details for the organization Compliance Announcement Setting |
| `api.telephony.call_recording.read_terms_of_service` | `GET` | `/telephony/config/callRecording/vendors/{vendor_id}/termsOfService` | Get Call Recording Terms Of Service Settings |
| `api.telephony.call_recording.set_location_vendor` | `PUT` | `/telephony/config/locations/{location_id}/callRecording/vendor` | Set Call Recording Vendor for a Location |
| `api.telephony.call_recording.set_org_vendor` | `PUT` | `/telephony/config/callRecording/vendor` | Set Organization Call Recording Vendor |
| `api.telephony.call_recording.update` | `PUT` | `/telephony/config/callRecording` | Update Call Recording Settings |
| `api.telephony.call_recording.update_location_compliance_announcement` | `PUT` | `/telephony/config/locations/{location_id}/callRecording/complianceAnnouncement` | Update the location compliance announcement |
| `api.telephony.call_recording.update_org_compliance_announcement` | `PUT` | `/telephony/config/callRecording/complianceAnnouncement` | Update the organization compliance announcement |
| `api.telephony.call_recording.update_terms_of_service` | `PUT` | `/telephony/config/callRecording/vendors/{vendor_id}/termsOfService` | Update Call Recording Terms Of Service Settings |
| `api.telephony.call_routing.tp.create` | `POST` | `/telephony/config/locations/{location_id}/callRouting/translationPatterns` | Create a Translation Pattern |
| `api.telephony.call_routing.tp.delete` | `DELETE` | `/telephony/config/locations/{location_id}/callRouting/translationPatterns/{translation_id}` | Delete a Translation Pattern |
| `api.telephony.call_routing.tp.details` | `GET` | `/telephony/config/locations/{location_id}/callRouting/translationPatterns/{translation_id}` | Retrieve the details of a Translation Pattern |
| `api.telephony.call_routing.tp.list` | `GET` | `/telephony/config/callRouting/translationPatterns` | Retrieve a list of Translation Patterns |
| `api.telephony.call_routing.tp.update` | `PUT` | `/telephony/config/locations/{location_id}/callRouting/translationPatterns/{id}` | Modify a Translation Pattern |
| `api.telephony.caller_reputation_provider.get` | `GET` | `/telephony/config/serviceSettings/callerReputationProvider` | Get Caller Reputation Provider Service Settings |
| `api.telephony.caller_reputation_provider.providers` | `GET` | `/telephony/config/serviceSettings/callerReputationProvider/providers` | Get Caller Reputation Provider Providers |
| `api.telephony.caller_reputation_provider.status` | `GET` | `/telephony/config/serviceSettings/callerReputationProvider/status` | Get Caller Reputation Provider Status |
| `api.telephony.caller_reputation_provider.unlock` | `POST` | `/telephony/config/serviceSettings/callerReputationProvider/actions/unlock/invoke` | Unlock Caller Reputation Provider |
| `api.telephony.caller_reputation_provider.update` | `PUT` | `/telephony/config/serviceSettings/callerReputationProvider` | Update Caller Reputation Provider Service Settings |
| `api.telephony.callpark.available_agents` | `GET` | `/telephony/config/locations/{location_id}/callParks/availableUsers` | Get available agents from Call Parks |
| `api.telephony.callpark.available_recalls` | `GET` | `/telephony/config/locations/{location_id}/callParks/availableRecallHuntGroups` | Get available recall hunt groups from Call Parks |
| `api.telephony.callpark.call_park_settings` | `GET` | `/telephony/config/locations/{location_id}/callParks/settings` | Get Call Park Settings |
| `api.telephony.callpark.create` | `POST` | `/telephony/config/locations/{location_id}/callParks` | Create a Call Park Extension |
| `api.telephony.callpark.delete_callpark` | `DELETE` | `/telephony/config/locations/{location_id}/callParks/{callpark_id}` | Delete a Call Park |
| `api.telephony.callpark.details` | `GET` | `/telephony/config/locations/{location_id}/callParks/{callpark_id}` | Get Details for a Call Park |
| `api.telephony.callpark.list` | `GET` | `/telephony/config/locations/{location_id}/callParks` | Read the List of Call Parks |
| `api.telephony.callpark.update` | `PUT` | `/telephony/config/locations/{location_id}/callParks/{callpark_id}` | Update a Call Park |
| `api.telephony.callpark.update_call_park_settings` | `PUT` | `/telephony/config/locations/{location_id}/callParks/settings` | Update Call Park settings |
| `api.telephony.callpark_extension.create` | `POST` | `/telephony/config/locations/{location_id}/callParkExtensions` | Create a Call Park Extension |
| `api.telephony.callpark_extension.delete` | `DELETE` | `/telephony/config/locations/{location_id}/callParkExtensions/{cpe_id}` | Delete a Call Park Extension |
| `api.telephony.callpark_extension.details` | `GET` | `/telephony/config/locations/{location_id}/callParkExtensions/{cpe_id}` | Get Details for a Call Park Extension |
| `api.telephony.callpark_extension.list` | `GET` | `/telephony/config/callParkExtensions` | Read the List of Call Park Extensions |
| `api.telephony.callpark_extension.update` | `PUT` | `/telephony/config/locations/{location_id}/callParkExtensions/{cpe_id}` | Update a Call Park Extension |
| `api.telephony.callqueue.agents.details` | `GET` | `/telephony/config/queues/agents/{id}` | Get Details for a Call Queue Agent |
| `api.telephony.callqueue.agents.list` | `GET` | `/telephony/config/queues/agents` | Read the List of Call Queue Agents |
| `api.telephony.callqueue.agents.update_call_queue_settings` | `PUT` | `/telephony/config/queues/agents/{id}/settings` | Update an Agent's Settings of One or More Call Queues |
| `api.telephony.callqueue.alternate_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/queues/alternate/availableNumbers` | Get Call Queue Alternate Available Phone Numbers |
| `api.telephony.callqueue.available_agents` | `GET` | `/telephony/config/queues/agents/availableAgents` | Get Call Queue Available Agents |
| `api.telephony.callqueue.call_forward_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/queues/callForwarding/availableNumbers` | Get Call Queue Call Forward Available Phone Numbers |
| `api.telephony.callqueue.create` | `POST` | `/telephony/config/locations/{location_id}/queues` | Create a Call Queue |
| `api.telephony.callqueue.delete_queue` | `DELETE` | `/telephony/config/locations/{location_id}/queues/{queue_id}` | Delete a Call Queue |
| `api.telephony.callqueue.details` | `GET` | `/telephony/config/locations/{location_id}/queues/{queue_id}` | Get Details for a Call Queue |
| `api.telephony.callqueue.forwarding.call_forwarding_rule` | `GET` | `/telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding/selectiveRules/{rule_id}` | Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue. |
| `api.telephony.callqueue.forwarding.create_call_forwarding_rule` | `POST` | `/telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding/selectiveRules` | Create a Selective Call Forwarding Rule feature |
| `api.telephony.callqueue.forwarding.delete_call_forwarding_rule` | `DELETE` | `/telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding/selectiveRules/{rule_id}` | Delete a Selective Call Forwarding Rule for the designated feature. |
| `api.telephony.callqueue.forwarding.settings` | `GET` | `/telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding` | Retrieve Call Forwarding settings for the designated feature including the list of call |
| `api.telephony.callqueue.forwarding.switch_mode_for_call_forwarding` | `POST` | `/telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding/actions/switchMode/invoke` | Switch Mode for Call Forwarding Settings for an entity |
| `api.telephony.callqueue.forwarding.update` | `PUT` | `/telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding` | Update Call Forwarding Settings for a feature |
| `api.telephony.callqueue.forwarding.update_call_forwarding_rule` | `PUT` | `/telephony/config/locations/{location_id}/queues/{feature_id}/callForwarding/selectiveRules/{rule_id}` | Update a Selective Call Forwarding Rule's settings for the designated feature. |
| `api.telephony.callqueue.get_call_queue_settings` | `GET` | `/telephony/config/queues/settings` | Get Call Queue Settings |
| `api.telephony.callqueue.list` | `GET` | `/telephony/config/queues` | Read the List of Call Queues |
| `api.telephony.callqueue.primary_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/queues/availableNumbers` | Get Call Queue Primary Available Phone Numbers |
| `api.telephony.callqueue.update` | `PUT` | `/telephony/config/locations/{location_id}/queues/{queue_id}` | Update a Call Queue |
| `api.telephony.callqueue.update_call_queue_settings` | `PUT` | `/telephony/config/queues/settings` | Update Call Queue Settings |
| `api.telephony.calls.answer` | `POST` | `/telephony/calls/answer` | Answer |
| `api.telephony.calls.barge_in` | `POST` | `/telephony/calls/bargeIn` | Barge In |
| `api.telephony.calls.call_details` | `GET` | `/telephony/calls/{call_id}` | Get Call Details |
| `api.telephony.calls.call_history` | `GET` | `/telephony/calls/history` | List Call History |
| `api.telephony.calls.dial` | `POST` | `/telephony/calls/dial` | Dial |
| `api.telephony.calls.divert` | `POST` | `/telephony/calls/divert` | Divert |
| `api.telephony.calls.hangup` | `POST` | `/telephony/calls/hangup` | Hangup |
| `api.telephony.calls.hold` | `POST` | `/telephony/calls/hold` | Hold |
| `api.telephony.calls.list_calls` | `GET` | `/telephony/calls` | List Calls |
| `api.telephony.calls.mute` | `POST` | `/telephony/calls/mute` | Mute |
| `api.telephony.calls.park` | `POST` | `/telephony/calls/park` | Park |
| `api.telephony.calls.pause_recording` | `POST` | `/telephony/calls/pauseRecording` | Pause Recording |
| `api.telephony.calls.pickup` | `POST` | `/telephony/calls/pickup` | Pickup |
| `api.telephony.calls.pull` | `POST` | `/telephony/calls/pull` | Pull |
| `api.telephony.calls.push` | `POST` | `/telephony/calls/push` | Push |
| `api.telephony.calls.reject` | `POST` | `/telephony/calls/reject` | Reject |
| `api.telephony.calls.resume` | `POST` | `/telephony/calls/resume` | Resume |
| `api.telephony.calls.resume_recording` | `POST` | `/telephony/calls/resumeRecording` | Resume Recording |
| `api.telephony.calls.retrieve` | `POST` | `/telephony/calls/retrieve` | Retrieve |
| `api.telephony.calls.start_recording` | `POST` | `/telephony/calls/startRecording` | Start Recording |
| `api.telephony.calls.stop_recording` | `POST` | `/telephony/calls/stopRecording` | Stop Recording |
| `api.telephony.calls.transfer` | `POST` | `/telephony/calls/transfer` | Transfer |
| `api.telephony.calls.transmit_dtmf` | `POST` | `/telephony/calls/transmitDtmf` | Transmit DTMF |
| `api.telephony.calls.unmute` | `POST` | `/telephony/calls/unmute` | Unmute |
| `api.telephony.calls.update_external_voicemail_mwi` | `POST` | `/telephony/externalVoicemail/mwi` | Set or Clear Message Waiting Indicator (MWI) Status |
| `api.telephony.conference.add_participant` | `POST` | `/telephony/conference/addParticipant` | Add Participant |
| `api.telephony.conference.deafen_participant` | `POST` | `/telephony/conference/deafen` | Deafen Participant |
| `api.telephony.conference.get_conference_details` | `GET` | `/telephony/conference` | Get Conference Details |
| `api.telephony.conference.hold` | `POST` | `/telephony/conference/hold` | Hold |
| `api.telephony.conference.mute` | `POST` | `/telephony/conference/mute` | Mute |
| `api.telephony.conference.release_conference` | `DELETE` | `/telephony/conference` | Release Conference |
| `api.telephony.conference.resume` | `POST` | `/telephony/conference/resume` | Resume |
| `api.telephony.conference.start_conference` | `POST` | `/telephony/conference` | Start Conference |
| `api.telephony.conference.undeafen_participant` | `POST` | `/telephony/conference/undeafen` | Undeafen Participant |
| `api.telephony.conference.unmute` | `POST` | `/telephony/conference/unmute` | Unmute |
| `api.telephony.create_a_call_token` | `POST` | `/telephony/click2call/callToken` | Create a call token |
| `api.telephony.cx_essentials.available_agents` | `GET` | `/telephony/config/locations/{location_id}/cxEssentials/agents/availableAgents` | Get List of available agents for Customer Experience Essentials |
| `api.telephony.cx_essentials.callqueue_recording.configure` | `PUT` | `/telephony/config/locations/{location_id}/queues/{queue_id}/cxEssentials/callRecordings` | Configure Queue Call Recording Settings for a Queue |
| `api.telephony.cx_essentials.callqueue_recording.read` | `GET` | `/telephony/config/locations/{location_id}/queues/{queue_id}/cxEssentials/callRecordings` | Read Queue Call Recording Settings for a Queue |
| `api.telephony.cx_essentials.get_screen_pop_configuration` | `GET` | `/telephony/config/locations/{location_id}/queues/{queue_id}/cxEssentials/screenPop` | Get Screen Pop configuration for a Call Queue in a Location |
| `api.telephony.cx_essentials.modify_screen_pop_configuration` | `PUT` | `/telephony/config/locations/{location_id}/queues/{queue_id}/cxEssentials/screenPop` | Modify Screen Pop configuration for a Call Queue in a Location |
| `api.telephony.cx_essentials.wrapup_reasons.available_queues` | `GET` | `/telephony/config/cxEssentials/wrapup/reasons/{wrapup_reason_id}/availableQueues` | Read Available Queues |
| `api.telephony.cx_essentials.wrapup_reasons.create` | `POST` | `/telephony/config/cxEssentials/wrapup/reasons` | Create Wrap Up Reason |
| `api.telephony.cx_essentials.wrapup_reasons.delete` | `DELETE` | `/telephony/config/cxEssentials/wrapup/reasons/{wrapup_reason_id}` | Delete Wrap Up Reason |
| `api.telephony.cx_essentials.wrapup_reasons.details` | `GET` | `/telephony/config/cxEssentials/wrapup/reasons/{wrapup_reason_id}` | Read Wrap Up Reason |
| `api.telephony.cx_essentials.wrapup_reasons.list` | `GET` | `/telephony/config/cxEssentials/wrapup/reasons` | List Wrap Up Reasons |
| `api.telephony.cx_essentials.wrapup_reasons.read_queue_settings` | `GET` | `/telephony/config/cxEssentials/locations/{location_id}/queues/{queue_id}/wrapup/settings` | Read Wrap Up Reason Settings |
| `api.telephony.cx_essentials.wrapup_reasons.update` | `PUT` | `/telephony/config/cxEssentials/wrapup/reasons/{wrapup_reason_id}` | Update Wrap Up Reason |
| `api.telephony.cx_essentials.wrapup_reasons.update_queue_settings` | `PUT` | `/telephony/config/cxEssentials/locations/{location_id}/queues/{queue_id}/wrapup/settings` | Update Wrap Up Reason Settings |
| `api.telephony.cx_essentials.wrapup_reasons.validate` | `POST` | `/telephony/config/cxEssentials/wrapup/reasons/actions/validateName/invoke` | Validate Wrap Up Reason |
| `api.telephony.dect_devices.add_a_handset` | `POST` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets` | Add a Handset to a DECT Network |
| `api.telephony.dect_devices.add_list_of_handsets` | `POST` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets/bulk` | Add a List of Handsets to a DECT Network |
| `api.telephony.dect_devices.available_members` | `GET` | `/telephony/config/devices/availableMembers` | Search Available Members |
| `api.telephony.dect_devices.base_station_details` | `GET` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/baseStations/{base_station_id}` | Get the details of a specific DECT Network Base Station |
| `api.telephony.dect_devices.create_base_stations` | `POST` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_id}/baseStations` | Create Multiple Base Stations |
| `api.telephony.dect_devices.create_dect_network` | `POST` | `/telephony/config/locations/{location_id}/dectNetworks` | Create a DECT Network |
| `api.telephony.dect_devices.dect_network_details` | `GET` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}` | Get DECT Network Details |
| `api.telephony.dect_devices.dect_networks_associated_with_person` | `GET` | `/telephony/config/people/{person_id}/dectNetworks` | GET List of DECT networks associated with a Person |
| `api.telephony.dect_devices.dect_networks_associated_with_virtual_line` | `GET` | `/telephony/config/virtualLines/{virtual_line_id}/dectNetworks` | Get List of Dect Networks Handsets for a Virtual Line |
| `api.telephony.dect_devices.dect_networks_associated_with_workspace` | `GET` | `/telephony/config/workspaces/{workspace_id}/dectNetworks` | GET List of DECT networks associated with a workspace |
| `api.telephony.dect_devices.delete_base_station` | `DELETE` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/baseStations/{base_station_id}` | Delete a specific DECT Network Base Station |
| `api.telephony.dect_devices.delete_bulk_base_stations` | `DELETE` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/baseStations` | Delete bulk DECT Network Base Stations |
| `api.telephony.dect_devices.delete_dect_network` | `DELETE` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}` | Delete DECT Network |
| `api.telephony.dect_devices.delete_handset` | `DELETE` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets/{handset_id}` | Delete specific DECT Network Handset Details |
| `api.telephony.dect_devices.delete_handsets` | `DELETE` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets` | Delete multiple handsets |
| `api.telephony.dect_devices.device_type_list` | `GET` | `/telephony/config/devices/dectNetworks/supportedDevices` | Read the DECT device type list |
| `api.telephony.dect_devices.generate_and_enable_dect_serviceability_password` | `POST` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/serviceabilityPassword/actions/generate/invoke` | Generate and Enable DECT Serviceability Password |
| `api.telephony.dect_devices.get_dect_serviceability_password_status` | `GET` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/serviceabilityPassword` | Get DECT Serviceability Password status |
| `api.telephony.dect_devices.handset_details` | `GET` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets/{handset_id}` | Get Specific DECT Network Handset Details |
| `api.telephony.dect_devices.list_base_stations` | `GET` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/baseStations` | Get a list of DECT Network Base Stations |
| `api.telephony.dect_devices.list_dect_networks` | `GET` | `/telephony/config/dectNetworks` | Get the List of DECT Networks for an organization |
| `api.telephony.dect_devices.list_handsets` | `GET` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets` | Get List of Handsets for a DECT Network ID |
| `api.telephony.dect_devices.update_dect_network` | `PUT` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}` | Update DECT Network |
| `api.telephony.dect_devices.update_dect_network_settings` | `PUT` | `/telephony/config/locations/{id}/dectNetworks/{id}` | Update DECT Network from settings |
| `api.telephony.dect_devices.update_dect_serviceability_password_status` | `PUT` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/serviceabilityPassword` | Update DECT Serviceability Password status |
| `api.telephony.dect_devices.update_handset` | `PUT` | `/telephony/config/locations/{location_id}/dectNetworks/{dect_network_id}/handsets/{handset_id}` | Update DECT Network Handset |
| `api.telephony.device_settings` | `GET` | `/telephony/config/devices/settings` | Get device override settings for an organization. |
| `api.telephony.devices.apply_changes` | `POST` | `/telephony/config/devices/{device_id}/actions/applyChanges/invoke` | Apply Changes for a specific device |
| `api.telephony.devices.available_members` | `GET` | `/telephony/config/devices/{device_id}/availableMembers` | Search members that can be assigned to the device. |
| `api.telephony.devices.create_line_key_template` | `POST` | `/telephony/config/devices/lineKeyTemplates` | Create a Line Key Template |
| `api.telephony.devices.delete_background_images` | `DELETE` | `/telephony/config/devices/backgroundImages` | Delete Device Background Images |
| `api.telephony.devices.delete_line_key_template` | `DELETE` | `/telephony/config/devices/lineKeyTemplates/{template_id}` | Delete a Line Key Template |
| `api.telephony.devices.details` | `GET` | `/telephony/config/devices/{device_id}` | Get Webex Calling Device Details |
| `api.telephony.devices.device_settings` | `GET` | `/telephony/config/devices/{device_id}/settings` | Get override settings for a device. |
| `api.telephony.devices.dynamic_settings.get_customer_device_settings` | `POST` | `/telephony/config/lists/devices/dynamicSettings/actions/getSettings/invoke` | Get Customer Device Dynamic Settings |
| `api.telephony.devices.dynamic_settings.get_device_settings` | `POST` | `/telephony/config/lists/devices/{device_id}/dynamicSettings/actions/getSettings/invoke` | Get Device Dynamic Settings |
| `api.telephony.devices.dynamic_settings.get_location_device_settings` | `POST` | `/telephony/config/lists/locations/{location_id}/devices/dynamicSettings/actions/getSettings/invoke` | Get Location Device Dynamic Settings |
| `api.telephony.devices.dynamic_settings.get_settings_groups` | `GET` | `/telephony/config/devices/dynamicSettings/settingsGroups` | Get Settings Groups |
| `api.telephony.devices.dynamic_settings.get_validation_schema` | `GET` | `/telephony/config/devices/dynamicSettings/validationSchema` | Get Validation Schema |
| `api.telephony.devices.dynamic_settings.update_specified_settings_for_the_device` | `PUT` | `/telephony/config/devices/{device_id}/dynamicSettings` | Update specified settings for the device. |
| `api.telephony.devices.get_count_of_available_members` | `GET` | `/telephony/config/devices/availableMembers/count` | Get Count of Available Members |
| `api.telephony.devices.get_count_of_members` | `GET` | `/telephony/config/devices/{device_id}/availableMembers/count` | Get Count of Members |
| `api.telephony.devices.get_device_layout` | `GET` | `/telephony/config/devices/{device_id}/layout` | Get Device Layout by Device ID |
| `api.telephony.devices.get_person_device_settings` | `GET` | `/telephony/config/people/{person_id}/devices/settings` | Get Device Settings for a Person |
| `api.telephony.devices.get_workspace_device_settings` | `GET` | `/telephony/config/workspaces/{workspace_id}/devices/settings` | Get Device Settings for a Workspace |
| `api.telephony.devices.line_key_template_details` | `GET` | `/telephony/config/devices/lineKeyTemplates/{template_id}` | Get details of a Line Key Template |
| `api.telephony.devices.list_background_images` | `GET` | `/telephony/config/devices/backgroundImages` | Read the List of Background Images |
| `api.telephony.devices.list_line_key_templates` | `GET` | `/telephony/config/devices/lineKeyTemplates` | Read the list of Line Key Templates |
| `api.telephony.devices.members` | `GET` | `/telephony/config/devices/{device_id}/members` | Get Device Members |
| `api.telephony.devices.modify_device_layout` | `PUT` | `/telephony/config/devices/{device_id}/layout` | Modify Device Layout by Device ID |
| `api.telephony.devices.modify_line_key_template` | `PUT` | `/telephony/config/devices/lineKeyTemplates/{id}` | Modify a Line Key Template |
| `api.telephony.devices.preview_apply_line_key_template` | `POST` | `/telephony/config/devices/actions/previewApplyLineKeyTemplate/invoke` | Preview Apply Line Key Template |
| `api.telephony.devices.supported_devices` | `GET` | `/telephony/config/supportedDevices` | Read the List of Supported Devices |
| `api.telephony.devices.update_device_settings` | `PUT` | `/telephony/config/devices/{device_id}/settings` | Modify override settings for a device. |
| `api.telephony.devices.update_members` | `PUT` | `/telephony/config/devices/{device_id}/members` | Modify member details on the device. |
| `api.telephony.devices.update_person_device_settings` | `PUT` | `/telephony/config/people/{person_id}/devices/settings` | Update Device Settings for a Person |
| `api.telephony.devices.update_third_party_device` | `PUT` | `/telephony/config/devices/{device_id}` | Update Third Party Device |
| `api.telephony.devices.update_workspace_device_settings` | `PUT` | `/telephony/config/workspaces/{workspace_id}/devices/settings` | Update Device Settings for a Workspace |
| `api.telephony.devices.upload_background_image` | `POST` | `/telephony/config/devices/{device_id}/actions/backgroundImageUpload/invoke` | Upload a Device Background Image |
| `api.telephony.devices.user_devices_count` | `GET` | `/telephony/config/people/{person_id}/devices/count` | Get User Devices Count |
| `api.telephony.devices.validate_macs` | `POST` | `/telephony/config/devices/actions/validateMacs/invoke` | Validate a list of MAC addresses. |
| `api.telephony.emergency_address.add_to_location` | `POST` | `/telephony/pstn/locations/{location_id}/emergencyAddress` | Add an Emergency Address to a Location |
| `api.telephony.emergency_address.lookup_for_location` | `POST` | `/telephony/pstn/locations/{location_id}/emergencyAddress/lookup` | Emergency Address Lookup to Verify if Address is Valid |
| `api.telephony.emergency_address.update_for_location` | `PUT` | `/telephony/pstn/locations/{location_id}/emergencyAddresses/{address_id}` | Update the Emergency Address of a Location |
| `api.telephony.emergency_address.update_for_phone_number` | `PUT` | `/telephony/pstn/numbers/{phone_number}/emergencyAddress` | Update the emergency address for a phone number. |
| `api.telephony.emergency_services.create_location_address_and_alert_email` | `POST` | `/telephony/config/locations/{location_id}/redSky/building` | Create a RedSky Building Address and Alert Email for a Location |
| `api.telephony.emergency_services.create_redsky_account_and_admin` | `POST` | `/telephony/config/redSky` | Create an account and admin in RedSky. |
| `api.telephony.emergency_services.get_location_compliance_status` | `GET` | `/telephony/config/locations/{location_id}/redSky/status` | Get a Location's RedSky Compliance Status |
| `api.telephony.emergency_services.get_location_notification` | `GET` | `/telephony/config/locations/{location_id}/emergencyCallNotification` | Get a Location Emergency Call Notification |
| `api.telephony.emergency_services.get_location_parameters` | `GET` | `/telephony/config/locations/{location_id}/redSky` | Get a Location's RedSky Emergency Calling Parameters |
| `api.telephony.emergency_services.get_notification` | `GET` | `/telephony/config/emergencyCallNotification` | Get an Organization Emergency Call Notification |
| `api.telephony.emergency_services.get_org_compliance` | `GET` | `/telephony/config/redSky/complianceStatus` | Get the Organization Compliance Status and the Location Status List |
| `api.telephony.emergency_services.get_org_compliance_status` | `GET` | `/telephony/config/redSky/status` | Get the Organization Compliance Status for a RedSky Account |
| `api.telephony.emergency_services.get_redsky_account_details` | `GET` | `/telephony/config/redSky` | Retrieve RedSky account details for an organization. |
| `api.telephony.emergency_services.hunt_group_ecbn_dependencies` | `GET` | `/telephony/config/huntGroups/{hunt_group_id}/emergencyCallbackNumber/dependencies` | Get Dependencies for a Hunt Group Emergency Callback Number |
| `api.telephony.emergency_services.login` | `POST` | `/telephony/config/redSky/actions/login/invoke` | Login to a RedSky Admin Account |
| `api.telephony.emergency_services.update_location_address` | `PUT` | `/telephony/config/locations/{location_id}/redSky/building` | Update a RedSky Building Address for a Location |
| `api.telephony.emergency_services.update_location_compliance_status` | `PUT` | `/telephony/config/locations/{location_id}/redSky/status` | Update a Location's RedSky Compliance Status |
| `api.telephony.emergency_services.update_location_notification` | `PUT` | `/telephony/config/locations/{location_id}/emergencyCallNotification` | Update a location emergency call notification. |
| `api.telephony.emergency_services.update_notification` | `PUT` | `/telephony/config/emergencyCallNotification` | Update an organization emergency call notification. |
| `api.telephony.emergency_services.update_org_compliance_status` | `PUT` | `/telephony/config/redSky/status` | Update the Organization RedSky Account's Compliance Status |
| `api.telephony.emergency_services.update_service_settings` | `PUT` | `/telephony/config/redSky/serviceSettings` | Update RedSky Service Settings |
| `api.telephony.get_call_captions_settings` | `GET` | `/telephony/config/callCaptions` | Get the organization call captions settings |
| `api.telephony.get_large_organization_status` | `GET` | `/telephony/config/largeOrgStatus` | Get Large Organization Status |
| `api.telephony.guest_calling.available_members` | `GET` | `/telephony/config/guestCalling/availableMembers` | Read the Click-to-call Available Members |
| `api.telephony.guest_calling.members` | `GET` | `/telephony/config/guestCalling/members` | Read the Click-to-call Members |
| `api.telephony.guest_calling.read` | `GET` | `/telephony/config/guestCalling` | Read the Click-to-call Settings |
| `api.telephony.guest_calling.update` | `PUT` | `/telephony/config/guestCalling` | Update the Click-to-call Settings |
| `api.telephony.hotdesk.delete_session` | `DELETE` | `/hotdesk/sessions/{session_id}` | Delete Session |
| `api.telephony.hotdesk.list_sessions` | `GET` | `/hotdesk/sessions` | List Sessions |
| `api.telephony.hotdesking_voiceportal.location_get` | `GET` | `/telephony/config/locations/{location_id}/features/hotDesking` | Voice Portal Hot desking sign in details for a location |
| `api.telephony.hotdesking_voiceportal.location_update` | `PUT` | `/telephony/config/locations/{location_id}/features/hotDesking` | Update Voice Portal Hot desking sign in details for a location |
| `api.telephony.hotdesking_voiceportal.user_get` | `GET` | `/telephony/config/people/{person_id}/features/hotDesking/guest` | Voice Portal Hot desking sign in details for a user |
| `api.telephony.hotdesking_voiceportal.user_update` | `PUT` | `/telephony/config/people/{person_id}/features/hotDesking/guest` | Update Voice Portal Hot desking sign in details for a user |
| `api.telephony.huntgroup.alternate_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/huntGroups/alternate/availableNumbers` | Get Hunt Group Alternate Available Phone Numbers |
| `api.telephony.huntgroup.create` | `POST` | `/telephony/config/locations/{location_id}/huntGroups` | Create a Hunt Group |
| `api.telephony.huntgroup.delete_huntgroup` | `DELETE` | `/telephony/config/locations/{location_id}/huntGroups/{huntgroup_id}` | Delete a Hunt Group |
| `api.telephony.huntgroup.details` | `GET` | `/telephony/config/locations/{location_id}/huntGroups/{huntgroup_id}` | Get Details for a Hunt Group |
| `api.telephony.huntgroup.forward_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/huntGroups/callForwarding/availableNumbers` | Get Hunt Group Call Forward Available Phone Numbers |
| `api.telephony.huntgroup.forwarding.call_forwarding_rule` | `GET` | `/telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding/selectiveRules/{rule_id}` | Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue. |
| `api.telephony.huntgroup.forwarding.create_call_forwarding_rule` | `POST` | `/telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding/selectiveRules` | Create a Selective Call Forwarding Rule feature |
| `api.telephony.huntgroup.forwarding.delete_call_forwarding_rule` | `DELETE` | `/telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding/selectiveRules/{rule_id}` | Delete a Selective Call Forwarding Rule for the designated feature. |
| `api.telephony.huntgroup.forwarding.settings` | `GET` | `/telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding` | Retrieve Call Forwarding settings for the designated feature including the list of call |
| `api.telephony.huntgroup.forwarding.switch_mode_for_call_forwarding` | `POST` | `/telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding/actions/switchMode/invoke` | Switch Mode for Call Forwarding Settings for an entity |
| `api.telephony.huntgroup.forwarding.update` | `PUT` | `/telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding` | Update Call Forwarding Settings for a feature |
| `api.telephony.huntgroup.forwarding.update_call_forwarding_rule` | `PUT` | `/telephony/config/locations/{location_id}/huntGroups/{feature_id}/callForwarding/selectiveRules/{rule_id}` | Update a Selective Call Forwarding Rule's settings for the designated feature. |
| `api.telephony.huntgroup.list` | `GET` | `/telephony/config/huntGroups` | Read the List of Hunt Groups |
| `api.telephony.huntgroup.primary_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/huntGroups/availableNumbers` | Get Hunt Group Primary Available Phone Numbers |
| `api.telephony.huntgroup.update` | `PUT` | `/telephony/config/locations/{location_id}/huntGroups/{huntgroup_id}` | Update a Hunt Group |
| `api.telephony.jobs.activation_emails.errors` | `GET` | `/identity/organizations/{org_id}/jobs/sendActivationEmails/{job_id}/errors` | Get Bulk Activation Email Resend Job Errors |
| `api.telephony.jobs.activation_emails.start` | `POST` | `/identity/organizations/{org_id}/jobs/sendActivationEmails` | Initiate Bulk Activation Email Resend Job |
| `api.telephony.jobs.activation_emails.status` | `GET` | `/identity/organizations/{org_id}/jobs/sendActivationEmails/{job_id}/status` | Get Bulk Activation Email Resend Job Status |
| `api.telephony.jobs.apply_line_key_templates.apply` | `POST` | `/telephony/config/jobs/devices/applyLineKeyTemplate` | Apply a Line key Template |
| `api.telephony.jobs.apply_line_key_templates.errors` | `GET` | `/telephony/config/jobs/devices/applyLineKeyTemplate/{job_id}/errors` | Get job errors for an Apply Line Key Template job |
| `api.telephony.jobs.apply_line_key_templates.list` | `GET` | `/telephony/config/jobs/devices/applyLineKeyTemplate` | Get List of Apply Line Key Template jobs |
| `api.telephony.jobs.apply_line_key_templates.status` | `GET` | `/telephony/config/jobs/devices/applyLineKeyTemplate/{job_id}` | Get the job status of an Apply Line Key Template job |
| `api.telephony.jobs.call_recording.errors` | `GET` | `/telephony/config/jobs/callRecording/{job_id}/errors` | Get Job Errors for a Call Recording Job |
| `api.telephony.jobs.call_recording.list` | `GET` | `/telephony/config/jobs/callRecording` | List Call Recording Jobs |
| `api.telephony.jobs.call_recording.status` | `GET` | `/telephony/config/jobs/callRecording/{job_id}` | Get the Job Status of a Call Recording Job |
| `api.telephony.jobs.device_settings.change` | `POST` | `/telephony/config/jobs/devices/callDeviceSettings` | Change device settings across organization or locations jobs. |
| `api.telephony.jobs.device_settings.errors` | `GET` | `/telephony/config/jobs/devices/callDeviceSettings/{job_id}/errors` | List change device settings job errors. |
| `api.telephony.jobs.device_settings.list` | `GET` | `/telephony/config/jobs/devices/callDeviceSettings` | List change device settings jobs. |
| `api.telephony.jobs.device_settings.status` | `GET` | `/telephony/config/jobs/devices/callDeviceSettings/{job_id}` | Get change device settings job status. |
| `api.telephony.jobs.disable_calling_location.errors` | `GET` | `/telephony/config/jobs/locations/deleteCallingLocation/{job_id}/errors` | Retrieve Errors for a Disable Calling Location Job |
| `api.telephony.jobs.disable_calling_location.initiate` | `POST` | `/telephony/config/jobs/locations/deleteCallingLocation` | Disable a Location for Webex Calling. |
| `api.telephony.jobs.disable_calling_location.list` | `GET` | `/telephony/config/jobs/locations/deleteCallingLocation` | Get a List of Disable Calling Location Jobs |
| `api.telephony.jobs.disable_calling_location.pause` | `POST` | `/telephony/config/jobs/locations/deleteCallingLocation/{job_id}/actions/pause/invoke` | Pause a Disable Calling Location Job |
| `api.telephony.jobs.disable_calling_location.resume` | `POST` | `/telephony/config/jobs/locations/deleteCallingLocation/{job_id}/actions/resume/invoke` | Resume a Paused Disable Calling Location Job |
| `api.telephony.jobs.disable_calling_location.status` | `GET` | `/telephony/config/jobs/locations/deleteCallingLocation/{job_id}` | Get Disable Calling Location Job Status |
| `api.telephony.jobs.dynamic_device_settings.errors` | `GET` | `/telephony/config/jobs/devices/dynamicDeviceSettings/{job_id}/errors` | List Dynamic Device Settings Job Errors |
| `api.telephony.jobs.dynamic_device_settings.list` | `GET` | `/telephony/config/jobs/devices/dynamicDeviceSettings` | List dynamic device settings jobs. |
| `api.telephony.jobs.dynamic_device_settings.status` | `GET` | `/telephony/config/jobs/devices/dynamicDeviceSettings/{job_id}` | Get Device Dynamic Settings Job Status |
| `api.telephony.jobs.dynamic_device_settings.update_across_org_or_location` | `POST` | `/telephony/config/jobs/devices/dynamicDeviceSettings` | Updates dynamic Device Settings Across Organization Or Location |
| `api.telephony.jobs.manage_numbers.abandon` | `POST` | `/telephony/config/jobs/numbers/manageNumbers/{job_id}/actions/abandon/invoke` | Abandon the Manage Numbers Job. |
| `api.telephony.jobs.manage_numbers.errors` | `GET` | `/telephony/config/jobs/numbers/manageNumbers/{job_id}/errors` | List Manage Numbers Job errors |
| `api.telephony.jobs.manage_numbers.initiate_job` | `POST` | `/telephony/config/jobs/numbers/manageNumbers` | Initiate Number Jobs |
| `api.telephony.jobs.manage_numbers.list` | `GET` | `/telephony/config/jobs/numbers/manageNumbers` | List Manage Numbers Jobs |
| `api.telephony.jobs.manage_numbers.pause` | `POST` | `/telephony/config/jobs/numbers/manageNumbers/{job_id}/actions/pause/invoke` | Pause the Manage Numbers Job |
| `api.telephony.jobs.manage_numbers.resume` | `POST` | `/telephony/config/jobs/numbers/manageNumbers/{job_id}/actions/resume/invoke` | Resume the Manage Numbers Job |
| `api.telephony.jobs.manage_numbers.status` | `GET` | `/telephony/config/jobs/numbers/manageNumbers/{job_id}` | Get Manage Numbers Job Status |
| `api.telephony.jobs.move_users.abandon` | `POST` | `/telephony/config/jobs/person/moveLocation/{job_id}/actions/abandon/invoke` | Abandon the Move Users Job. |
| `api.telephony.jobs.move_users.errors` | `GET` | `/telephony/config/jobs/person/moveLocation/{job_id}/errors` | List Move Users Job errors |
| `api.telephony.jobs.move_users.list` | `GET` | `/telephony/config/jobs/person/moveLocation` | List Move Users Jobs |
| `api.telephony.jobs.move_users.pause` | `POST` | `/telephony/config/jobs/person/moveLocation/{job_id}/actions/pause/invoke` | Pause the Move Users Job |
| `api.telephony.jobs.move_users.resume` | `POST` | `/telephony/config/jobs/person/moveLocation/{job_id}/actions/resume/invoke` | Resume the Move Users Job |
| `api.telephony.jobs.move_users.status` | `GET` | `/telephony/config/jobs/person/moveLocation/{job_id}` | Get Move Users Job Status |
| `api.telephony.jobs.move_users.validate_or_initiate` | `POST` | `/telephony/config/jobs/person/moveLocation` | Validate or Initiate Move Users Job |
| `api.telephony.jobs.rebuild_phones.errors` | `GET` | `/telephony/config/jobs/devices/rebuildPhones/{job_id}/errors` | Get Job Errors for a Rebuild Phones Job |
| `api.telephony.jobs.rebuild_phones.list` | `GET` | `/telephony/config/jobs/devices/rebuildPhones` | List Rebuild Phones Jobs |
| `api.telephony.jobs.rebuild_phones.rebuild_phones_configuration` | `POST` | `/telephony/config/jobs/devices/rebuildPhones` | Rebuild Phones Configuration |
| `api.telephony.jobs.rebuild_phones.status` | `GET` | `/telephony/config/jobs/devices/rebuildPhones/{job_id}` | Get the Job Status of a Rebuild Phones Job |
| `api.telephony.jobs.update_routing_prefix.errors` | `GET` | `/telephony/config/jobs/updateRoutingPrefix/{job_id}/errors` | Get job errors for update routing prefix job |
| `api.telephony.jobs.update_routing_prefix.list` | `GET` | `/telephony/config/jobs/updateRoutingPrefix` | Get a List of Update Routing Prefix jobs |
| `api.telephony.jobs.update_routing_prefix.status` | `GET` | `/telephony/config/jobs/updateRoutingPrefix/{job_id}` | Get the job status of Update Routing Prefix job |
| `api.telephony.location.call_intercept_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/callIntercept/availableNumbers` | Get Location Call Intercept Available Phone Numbers |
| `api.telephony.location.change_announcement_language` | `PUT` | `/{location_id}/actions/modifyAnnouncementLanguage/invoke` | Change Announcement Language |
| `api.telephony.location.charge_number_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/chargeNumber/availableNumbers` | Get Available Charge Numbers for a Location with Given Criteria |
| `api.telephony.location.create_receptionist_contact_directory` | `POST` | `/telephony/config/locations/{location_id}/receptionistContacts/directories` | Create a Receptionist Contact Directory |
| `api.telephony.location.delete_receptionist_contact_directory` | `DELETE` | `/telephony/config/locations/{location_id}/receptionistContacts/directories/{directory_id}` | Delete a Receptionist Contact Directory |
| `api.telephony.location.details` | `GET` | `/telephony/config/locations/{location_id}` | Get Location Webex Calling Details |
| `api.telephony.location.device_settings` | `GET` | `/telephony/config/locations/{location_id}/devices/settings` | Get device override settings for a location. |
| `api.telephony.location.ecbn_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/emergencyCallbackNumber/availableNumbers` | Get Location ECBN Available Phone Numbers |
| `api.telephony.location.emergency_services.read_emergency_call_notification` | `GET` | `/telephony/config/locations/{location_id}/emergencyCallNotification` | Get a Location Emergency Call Notification |
| `api.telephony.location.emergency_services.update_emergency_call_notification` | `PUT` | `/telephony/config/locations/{location_id}/emergencyCallNotification` | Update a location emergency call notification. |
| `api.telephony.location.enable_for_calling` | `POST` | `/telephony/config/locations` | Enable a Location for Webex Calling |
| `api.telephony.location.generate_password` | `POST` | `/telephony/config/locations/{location_id}/actions/generatePassword/invoke` | Generate example password for Location |
| `api.telephony.location.get_call_captions_settings` | `GET` | `/telephony/config/locations/{location_id}/callCaptions` | Get the location call captions settings |
| `api.telephony.location.intercept.configure` | `PUT` | `/telephony/config/locations/{location_id}/intercept` | Put Location Intercept |
| `api.telephony.location.intercept.read` | `GET` | `/telephony/config/locations/{location_id}/intercept` | Get Location Intercept |
| `api.telephony.location.internal_dialing.read` | `GET` | `/telephony/config/locations/{location_id}/internalDialing` | Read the Internal Dialing configuration for a location |
| `api.telephony.location.internal_dialing.update` | `PUT` | `/telephony/config/locations/{location_id}/internalDialing` | Modify the Internal Dialing configuration for a location |
| `api.telephony.location.list` | `GET` | `/telephony/config/locations` | List Locations Webex Calling Details |
| `api.telephony.location.list_receptionist_contact_directories` | `GET` | `/telephony/config/locations/{location_id}/receptionistContacts/directories` | Read list of Receptionist Contact Directories |
| `api.telephony.location.modify_receptionist_contact_directory` | `PUT` | `/telephony/config/locations/{location_id}/receptionistContacts/directories/{directory_id}` | Modify a Receptionist Contact Directory |
| `api.telephony.location.moh.read` | `GET` | `/telephony/config/locations/{location_id}/musicOnHold` | Get Music On Hold |
| `api.telephony.location.moh.update` | `PUT` | `/telephony/config/locations/{location_id}/musicOnHold` | Update Music On Hold |
| `api.telephony.location.number.add` | `POST` | `/telephony/config/locations/{location_id}/numbers` | Add Phone Numbers to a location |
| `api.telephony.location.number.manage_number_state` | `PUT` | `/telephony/config/locations/{location_id}/numbers` | Manage Number State in a location |
| `api.telephony.location.number.remove` | `DELETE` | `/telephony/config/locations/{location_id}/numbers` | Remove phone numbers from a location |
| `api.telephony.location.permissions_out.configure` | `PUT` | `/telephony/config/locations/{entity_id}/outgoingPermission` | Configure Outgoing Calling Permissions Settings |
| `api.telephony.location.permissions_out.digit_patterns.create` | `POST` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns` | Create Digit Patterns |
| `api.telephony.location.permissions_out.digit_patterns.delete` | `DELETE` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}` | Delete a Digit Pattern |
| `api.telephony.location.permissions_out.digit_patterns.delete_all` | `DELETE` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns` | Delete all Digit Patterns. |
| `api.telephony.location.permissions_out.digit_patterns.details` | `GET` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}` | Retrieve Digit Pattern Details |
| `api.telephony.location.permissions_out.digit_patterns.get_digit_patterns` | `GET` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns` | Retrieve Digit Patterns |
| `api.telephony.location.permissions_out.digit_patterns.update` | `PUT` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{id}` | Modify Digit Patterns |
| `api.telephony.location.permissions_out.digit_patterns.update_category_control_settings` | `PUT` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns` | Modify the Digit Pattern Category Control Settings for the entity |
| `api.telephony.location.permissions_out.read` | `GET` | `/telephony/config/locations/{entity_id}/outgoingPermission` | Retrieve Outgoing Calling Permissions Settings |
| `api.telephony.location.permissions_out.transfer_numbers.configure` | `PUT` | `/telephony/config/locations/{entity_id}/outgoingPermission/autoTransferNumbers` | Modify Transfer Numbers Settings for an entity. |
| `api.telephony.location.permissions_out.transfer_numbers.read` | `GET` | `/telephony/config/locations/{entity_id}/outgoingPermission/autoTransferNumbers` | Retrieve Transfer Numbers Settings . |
| `api.telephony.location.phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/availableNumbers` | Get Available Phone Numbers for a Location with Given Criteria |
| `api.telephony.location.phone_numbers_available_for_external_caller_id` | `GET` | `/telephony/config/locations/{location_id}/externalCallerId/availableNumbers` | Get the List of Phone Numbers Available for External Caller ID |
| `api.telephony.location.read_ecbn` | `GET` | `/telephony/config/locations/{location_id}/features/emergencyCallbackNumber` | Get a Location Emergency callback number |
| `api.telephony.location.receptionist_contact_directory_details` | `GET` | `/telephony/config/locations/{location_id}/receptionistContacts/directories/{directory_id}` | Get details for a Receptionist Contact Directory |
| `api.telephony.location.receptionist_contacts_directory.create` | `POST` | `/telephony/config/locations/{location_id}/receptionistContacts/directories` | Creates a new Receptionist Contact Directory for a location. |
| `api.telephony.location.receptionist_contacts_directory.delete` | `DELETE` | `/telephony/config/locations/{location_id}/receptionistContacts/directories` | Delete a Receptionist Contact Directory from a location. |
| `api.telephony.location.receptionist_contacts_directory.list` | `GET` | `/telephony/config/locations/{location_id}/receptionistContacts/directories` | List all Receptionist Contact Directories for a location. |
| `api.telephony.location.safe_delete_check_before_disabling_calling_location` | `POST` | `/telephony/config/locations/{location_id}/actions/precheckForDeletion/invoke` | Safe Delete Check Before Disabling a Location for Webex Calling |
| `api.telephony.location.update` | `PUT` | `/telephony/config/locations/{location_id}` | Update Location Webex Calling Details |
| `api.telephony.location.update_call_captions_settings` | `PUT` | `/telephony/config/locations/{location_id}/callCaptions` | Update the location call captions settings |
| `api.telephony.location.update_ecbn` | `PUT` | `/telephony/config/locations/{location_id}/features/emergencyCallbackNumber` | Update a Location Emergency callback number |
| `api.telephony.location.validate_extensions` | `POST` | `/telephony/config/locations/{location_id}/actions/validateExtensions/invoke` | Validate Extensions |
| `api.telephony.location.voicemail.read` | `GET` | `/telephony/config/locations/{location_id}/voicemail` | Get Location Voicemail |
| `api.telephony.location.voicemail.update` | `PUT` | `/telephony/config/locations/{location_id}/voicemail` | Update Location Voicemail |
| `api.telephony.location.webex_go_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/webexGo/availableNumbers` | Get Webex Go Available Phone Numbers |
| `api.telephony.locations.call_intercept_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/callIntercept/availableNumbers` | Get Location Call Intercept Available Phone Numbers |
| `api.telephony.locations.change_announcement_language` | `PUT` | `/{location_id}/actions/modifyAnnouncementLanguage/invoke` | Change Announcement Language |
| `api.telephony.locations.charge_number_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/chargeNumber/availableNumbers` | Get Available Charge Numbers for a Location with Given Criteria |
| `api.telephony.locations.create_receptionist_contact_directory` | `POST` | `/telephony/config/locations/{location_id}/receptionistContacts/directories` | Create a Receptionist Contact Directory |
| `api.telephony.locations.delete_receptionist_contact_directory` | `DELETE` | `/telephony/config/locations/{location_id}/receptionistContacts/directories/{directory_id}` | Delete a Receptionist Contact Directory |
| `api.telephony.locations.details` | `GET` | `/telephony/config/locations/{location_id}` | Get Location Webex Calling Details |
| `api.telephony.locations.device_settings` | `GET` | `/telephony/config/locations/{location_id}/devices/settings` | Get device override settings for a location. |
| `api.telephony.locations.ecbn_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/emergencyCallbackNumber/availableNumbers` | Get Location ECBN Available Phone Numbers |
| `api.telephony.locations.emergency_services.read_emergency_call_notification` | `GET` | `/telephony/config/locations/{location_id}/emergencyCallNotification` | Get a Location Emergency Call Notification |
| `api.telephony.locations.emergency_services.update_emergency_call_notification` | `PUT` | `/telephony/config/locations/{location_id}/emergencyCallNotification` | Update a location emergency call notification. |
| `api.telephony.locations.enable_for_calling` | `POST` | `/telephony/config/locations` | Enable a Location for Webex Calling |
| `api.telephony.locations.generate_password` | `POST` | `/telephony/config/locations/{location_id}/actions/generatePassword/invoke` | Generate example password for Location |
| `api.telephony.locations.get_call_captions_settings` | `GET` | `/telephony/config/locations/{location_id}/callCaptions` | Get the location call captions settings |
| `api.telephony.locations.intercept.configure` | `PUT` | `/telephony/config/locations/{location_id}/intercept` | Put Location Intercept |
| `api.telephony.locations.intercept.read` | `GET` | `/telephony/config/locations/{location_id}/intercept` | Get Location Intercept |
| `api.telephony.locations.internal_dialing.read` | `GET` | `/telephony/config/locations/{location_id}/internalDialing` | Read the Internal Dialing configuration for a location |
| `api.telephony.locations.internal_dialing.update` | `PUT` | `/telephony/config/locations/{location_id}/internalDialing` | Modify the Internal Dialing configuration for a location |
| `api.telephony.locations.list` | `GET` | `/telephony/config/locations` | List Locations Webex Calling Details |
| `api.telephony.locations.list_receptionist_contact_directories` | `GET` | `/telephony/config/locations/{location_id}/receptionistContacts/directories` | Read list of Receptionist Contact Directories |
| `api.telephony.locations.modify_receptionist_contact_directory` | `PUT` | `/telephony/config/locations/{location_id}/receptionistContacts/directories/{directory_id}` | Modify a Receptionist Contact Directory |
| `api.telephony.locations.moh.read` | `GET` | `/telephony/config/locations/{location_id}/musicOnHold` | Get Music On Hold |
| `api.telephony.locations.moh.update` | `PUT` | `/telephony/config/locations/{location_id}/musicOnHold` | Update Music On Hold |
| `api.telephony.locations.number.add` | `POST` | `/telephony/config/locations/{location_id}/numbers` | Add Phone Numbers to a location |
| `api.telephony.locations.number.manage_number_state` | `PUT` | `/telephony/config/locations/{location_id}/numbers` | Manage Number State in a location |
| `api.telephony.locations.number.remove` | `DELETE` | `/telephony/config/locations/{location_id}/numbers` | Remove phone numbers from a location |
| `api.telephony.locations.permissions_out.configure` | `PUT` | `/telephony/config/locations/{entity_id}/outgoingPermission` | Configure Outgoing Calling Permissions Settings |
| `api.telephony.locations.permissions_out.digit_patterns.create` | `POST` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns` | Create Digit Patterns |
| `api.telephony.locations.permissions_out.digit_patterns.delete` | `DELETE` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}` | Delete a Digit Pattern |
| `api.telephony.locations.permissions_out.digit_patterns.delete_all` | `DELETE` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns` | Delete all Digit Patterns. |
| `api.telephony.locations.permissions_out.digit_patterns.details` | `GET` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}` | Retrieve Digit Pattern Details |
| `api.telephony.locations.permissions_out.digit_patterns.get_digit_patterns` | `GET` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns` | Retrieve Digit Patterns |
| `api.telephony.locations.permissions_out.digit_patterns.update` | `PUT` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{id}` | Modify Digit Patterns |
| `api.telephony.locations.permissions_out.digit_patterns.update_category_control_settings` | `PUT` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns` | Modify the Digit Pattern Category Control Settings for the entity |
| `api.telephony.locations.permissions_out.read` | `GET` | `/telephony/config/locations/{entity_id}/outgoingPermission` | Retrieve Outgoing Calling Permissions Settings |
| `api.telephony.locations.permissions_out.transfer_numbers.configure` | `PUT` | `/telephony/config/locations/{entity_id}/outgoingPermission/autoTransferNumbers` | Modify Transfer Numbers Settings for an entity. |
| `api.telephony.locations.permissions_out.transfer_numbers.read` | `GET` | `/telephony/config/locations/{entity_id}/outgoingPermission/autoTransferNumbers` | Retrieve Transfer Numbers Settings . |
| `api.telephony.locations.phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/availableNumbers` | Get Available Phone Numbers for a Location with Given Criteria |
| `api.telephony.locations.phone_numbers_available_for_external_caller_id` | `GET` | `/telephony/config/locations/{location_id}/externalCallerId/availableNumbers` | Get the List of Phone Numbers Available for External Caller ID |
| `api.telephony.locations.read_ecbn` | `GET` | `/telephony/config/locations/{location_id}/features/emergencyCallbackNumber` | Get a Location Emergency callback number |
| `api.telephony.locations.receptionist_contact_directory_details` | `GET` | `/telephony/config/locations/{location_id}/receptionistContacts/directories/{directory_id}` | Get details for a Receptionist Contact Directory |
| `api.telephony.locations.receptionist_contacts_directory.create` | `POST` | `/telephony/config/locations/{location_id}/receptionistContacts/directories` | Creates a new Receptionist Contact Directory for a location. |
| `api.telephony.locations.receptionist_contacts_directory.delete` | `DELETE` | `/telephony/config/locations/{location_id}/receptionistContacts/directories` | Delete a Receptionist Contact Directory from a location. |
| `api.telephony.locations.receptionist_contacts_directory.list` | `GET` | `/telephony/config/locations/{location_id}/receptionistContacts/directories` | List all Receptionist Contact Directories for a location. |
| `api.telephony.locations.safe_delete_check_before_disabling_calling_location` | `POST` | `/telephony/config/locations/{location_id}/actions/precheckForDeletion/invoke` | Safe Delete Check Before Disabling a Location for Webex Calling |
| `api.telephony.locations.update` | `PUT` | `/telephony/config/locations/{location_id}` | Update Location Webex Calling Details |
| `api.telephony.locations.update_call_captions_settings` | `PUT` | `/telephony/config/locations/{location_id}/callCaptions` | Update the location call captions settings |
| `api.telephony.locations.update_ecbn` | `PUT` | `/telephony/config/locations/{location_id}/features/emergencyCallbackNumber` | Update a Location Emergency callback number |
| `api.telephony.locations.validate_extensions` | `POST` | `/telephony/config/locations/{location_id}/actions/validateExtensions/invoke` | Validate Extensions |
| `api.telephony.locations.voicemail.read` | `GET` | `/telephony/config/locations/{location_id}/voicemail` | Get Location Voicemail |
| `api.telephony.locations.voicemail.update` | `PUT` | `/telephony/config/locations/{location_id}/voicemail` | Update Location Voicemail |
| `api.telephony.locations.webex_go_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/webexGo/availableNumbers` | Get Webex Go Available Phone Numbers |
| `api.telephony.ms_teams.configure` | `PUT` | `/telephony/config/settings/msTeams` | Update an Organization's MS Teams Setting |
| `api.telephony.ms_teams.read` | `GET` | `/telephony/config/settings/msTeams` | Get an Organization's MS Teams Settings |
| `api.telephony.operating_modes.available_operating_modes` | `GET` | `/telephony/config/locations/{location_id}/operatingModes/availableOperatingModes` | Retrieve the List of Available Operating Modes in a Location. |
| `api.telephony.operating_modes.call_forward_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/operatingModes/callForwarding/availableNumbers` | Get Operating Mode Call Forward Available Phone Numbers |
| `api.telephony.operating_modes.create` | `POST` | `/telephony/config/operatingModes` | Create an Operating Mode. |
| `api.telephony.operating_modes.delete` | `DELETE` | `/telephony/config/operatingModes/{mode_id}` | Delete an Operating Mode. |
| `api.telephony.operating_modes.details` | `GET` | `/telephony/config/operatingModes/{mode_id}` | Get Details for an Operating Mode. |
| `api.telephony.operating_modes.holiday_create` | `POST` | `/telephony/config/operatingModes/{mode_id}/holidays` | Create an Operating Mode Holiday. |
| `api.telephony.operating_modes.holiday_delete` | `DELETE` | `/telephony/config/operatingModes/{mode_id}/holidays/{holiday_id}` | Delete an Operating Mode Holiday. |
| `api.telephony.operating_modes.holiday_details` | `GET` | `/telephony/config/operatingModes/{mode_id}/holidays/{holiday_id}` | Get details for an Operating Mode Holiday. |
| `api.telephony.operating_modes.holiday_update` | `PUT` | `/telephony/config/operatingModes/{mode_id}/holidays/{holiday_id}` | Modify an Operating Mode Holiday. |
| `api.telephony.operating_modes.list` | `GET` | `/telephony/config/operatingModes` | Read the List of Operating Modes. |
| `api.telephony.operating_modes.update` | `PUT` | `/telephony/config/operatingModes/{mode_id}` | Modify an Operating Mode. |
| `api.telephony.organisation_access_codes.create` | `POST` | `/telephony/config/outgoingPermission/accessCodes` | Create Access Codes for an Organisation |
| `api.telephony.organisation_access_codes.delete` | `PUT` | `/telephony/config/outgoingPermission/accessCodes` | Delete Outgoing Permission Access Code for an Organisation |
| `api.telephony.organisation_access_codes.list` | `GET` | `/telephony/config/outgoingPermission/accessCodes` | Retrieve the organisation's access codes. |
| `api.telephony.organisation_voicemail.read` | `GET` | `/telephony/config/voicemail/settings` | Get Voicemail Settings |
| `api.telephony.organisation_voicemail.update` | `PUT` | `/telephony/config/voicemail/settings` | Update the organization's voicemail settings. |
| `api.telephony.paging.create` | `POST` | `/telephony/config/locations/{location_id}/paging` | Create a new Paging Group |
| `api.telephony.paging.delete_paging` | `DELETE` | `/telephony/config/locations/{location_id}/paging/{paging_id}` | Delete a Paging Group |
| `api.telephony.paging.details` | `GET` | `/telephony/config/locations/{location_id}/paging/{paging_id}` | Get Details for a Paging Group |
| `api.telephony.paging.list` | `GET` | `/telephony/config/paging` | Read the List of Paging Groups |
| `api.telephony.paging.primary_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/paging/availableNumbers` | Get Paging Group Primary Available Phone Numbers |
| `api.telephony.paging.update` | `PUT` | `/telephony/config/locations/{location_id}/paging/{paging_id}` | Update a Paging Group |
| `api.telephony.permissions_out.configure` | `PUT` | `/telephony/config/locations/{entity_id}/outgoingPermission` | Configure Outgoing Calling Permissions Settings |
| `api.telephony.permissions_out.digit_patterns.create` | `POST` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns` | Create Digit Patterns |
| `api.telephony.permissions_out.digit_patterns.delete` | `DELETE` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}` | Delete a Digit Pattern |
| `api.telephony.permissions_out.digit_patterns.delete_all` | `DELETE` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns` | Delete all Digit Patterns. |
| `api.telephony.permissions_out.digit_patterns.details` | `GET` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}` | Retrieve Digit Pattern Details |
| `api.telephony.permissions_out.digit_patterns.get_digit_patterns` | `GET` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns` | Retrieve Digit Patterns |
| `api.telephony.permissions_out.digit_patterns.update` | `PUT` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns/{id}` | Modify Digit Patterns |
| `api.telephony.permissions_out.digit_patterns.update_category_control_settings` | `PUT` | `/telephony/config/locations/{entity_id}/outgoingPermission/digitPatterns` | Modify the Digit Pattern Category Control Settings for the entity |
| `api.telephony.permissions_out.read` | `GET` | `/telephony/config/locations/{entity_id}/outgoingPermission` | Retrieve Outgoing Calling Permissions Settings |
| `api.telephony.permissions_out.transfer_numbers.configure` | `PUT` | `/telephony/config/locations/{entity_id}/outgoingPermission/autoTransferNumbers` | Modify Transfer Numbers Settings for an entity. |
| `api.telephony.permissions_out.transfer_numbers.read` | `GET` | `/telephony/config/locations/{entity_id}/outgoingPermission/autoTransferNumbers` | Retrieve Transfer Numbers Settings . |
| `api.telephony.phone_number_details` | `GET` | `/telephony/config/numbers` | get summary (counts) of phone numbers |
| `api.telephony.phone_numbers` | `GET` | `/telephony/config/numbers` | Get Phone Numbers for an Organization with Given Criterias |
| `api.telephony.pickup.available_agents` | `GET` | `/telephony/config/locations/{location_id}/callPickups/availableUsers` | Get available agents from Call Pickups |
| `api.telephony.pickup.create` | `POST` | `/telephony/config/locations/{location_id}/callPickups` | Create a Call Pickup |
| `api.telephony.pickup.delete_pickup` | `DELETE` | `/telephony/config/locations/{location_id}/callPickups/{pickup_id}` | Delete a Call Pickup |
| `api.telephony.pickup.details` | `GET` | `/telephony/config/locations/{location_id}/callPickups/{pickup_id}` | Get Details for a Call Pickup |
| `api.telephony.pickup.list` | `GET` | `/telephony/config/locations/{location_id}/callPickups` | Read the List of Call Pickups |
| `api.telephony.pickup.update` | `PUT` | `/telephony/config/locations/{location_id}/callPickups/{pickup_id}` | Update a Call Pickup |
| `api.telephony.playlist.assigned_locations` | `GET` | `/telephony/config/announcements/playlists/{play_list_id}/locations` | List Playlist Locations |
| `api.telephony.playlist.create` | `POST` | `/telephony/config/announcements/playlists` | Create announcement Playlist at organization level |
| `api.telephony.playlist.delete` | `DELETE` | `/telephony/config/announcements/playlists/{play_list_id}` | Delete Announcement Playlist |
| `api.telephony.playlist.details` | `GET` | `/telephony/config/announcements/playlists/{play_list_id}` | Get Announcement Playlist |
| `api.telephony.playlist.list` | `GET` | `/telephony/config/announcements/playlists` | List Announcement Playlists |
| `api.telephony.playlist.modify` | `PUT` | `/telephony/config/announcements/playlists/{play_list_id}` | Update Announcement Playlist |
| `api.telephony.playlist.modify_assigned_locations` | `PUT` | `/telephony/config/announcements/playlists/{play_list_id}/locations` | Update Playlist Locations |
| `api.telephony.playlist.usage` | `GET` | `/telephony/config/announcements/playlists/{play_list_id}/usage` | Get Playlist Usage |
| `api.telephony.pnc.read` | `GET` | `/telephony/config/locations/{location_id}/privateNetworkConnect` | Get Private Network Connect |
| `api.telephony.pnc.update` | `PUT` | `/telephony/config/locations/{location_id}/privateNetworkConnect` | Get Private Network Connect |
| `api.telephony.prem_pstn.dial_plan.create` | `POST` | `/telephony/config/premisePstn/dialPlans` | Create a Dial Plan for the organization. |
| `api.telephony.prem_pstn.dial_plan.delete_all_patterns` | `PUT` | `/telephony/config/premisePstn/dialPlans/{dial_plan_id}/dialPatterns` | Delete all dial patterns from the Dial Plan. |
| `api.telephony.prem_pstn.dial_plan.delete_dial_plan` | `DELETE` | `/telephony/config/premisePstn/dialPlans/{dial_plan_id}` | Delete a Dial Plan for the organization. |
| `api.telephony.prem_pstn.dial_plan.details` | `GET` | `/telephony/config/premisePstn/dialPlans/{dial_plan_id}` | Get a Dial Plan for the organization. |
| `api.telephony.prem_pstn.dial_plan.list` | `GET` | `/telephony/config/premisePstn/dialPlans` | List all Dial Plans for the organization. |
| `api.telephony.prem_pstn.dial_plan.modify_patterns` | `PUT` | `/telephony/config/premisePstn/dialPlans/{dial_plan_id}/dialPatterns` | Modify dial patterns for the Dial Plan. |
| `api.telephony.prem_pstn.dial_plan.patterns` | `GET` | `/telephony/config/premisePstn/dialPlans/{dial_plan_id}/dialPatterns` | Read the List of Dial Patterns |
| `api.telephony.prem_pstn.dial_plan.update` | `PUT` | `/telephony/config/premisePstn/dialPlans/{dial_plan_id}` | Modify a Dial Plan for the organization. |
| `api.telephony.prem_pstn.route_group.create` | `POST` | `/telephony/config/premisePstn/routeGroups` | Creates a Route Group for the organization. |
| `api.telephony.prem_pstn.route_group.delete_route_group` | `DELETE` | `/telephony/config/premisePstn/routeGroups/{rg_id}` | Remove a Route Group from an Organization based on id. |
| `api.telephony.prem_pstn.route_group.details` | `GET` | `/telephony/config/premisePstn/routeGroups/{rg_id}` | Reads a Route Group for the organization based on id. |
| `api.telephony.prem_pstn.route_group.list` | `GET` | `/telephony/config/premisePstn/routeGroups` | List all Route Groups for an organization. A Route Group is a group of trunks that allows further scale and |
| `api.telephony.prem_pstn.route_group.update` | `PUT` | `/telephony/config/premisePstn/routeGroups/{rg_id}` | Modifies an existing Route Group for an organization based on id. |
| `api.telephony.prem_pstn.route_group.usage` | `GET` | `/telephony/config/premisePstn/routeGroups/{rg_id}/usage` | Read the Usage of a Routing Group |
| `api.telephony.prem_pstn.route_group.usage_call_to_extension` | `GET` | `/telephony/config/premisePstn/routeGroups/{rg_id}/usageCallToExtension` | List "Call to" on-premises Extension Locations for a specific route group. Users within these locations are |
| `api.telephony.prem_pstn.route_group.usage_dial_plan` | `GET` | `/telephony/config/premisePstn/routeGroups/{rg_id}/usageDialPlan` | List Dial Plan Locations for a specific route group. |
| `api.telephony.prem_pstn.route_group.usage_location_pstn` | `GET` | `/telephony/config/premisePstn/routeGroups/{rg_id}/usagePstnConnection` | List PSTN Connection Locations for a specific route group. This solution lets you configure users to use Cloud |
| `api.telephony.prem_pstn.route_group.usage_route_lists` | `GET` | `/telephony/config/premisePstn/routeGroups/{rg_id}/usageRouteList` | Read the Route Lists of a Routing Group |
| `api.telephony.prem_pstn.route_list.create` | `POST` | `/telephony/config/premisePstn/routeLists` | Create a Route List for the organization. |
| `api.telephony.prem_pstn.route_list.delete_all_numbers` | `PUT` | `/telephony/config/premisePstn/routeLists/{rl_id}/numbers` |  |
| `api.telephony.prem_pstn.route_list.delete_route_list` | `DELETE` | `/telephony/config/premisePstn/routeLists/{rl_id}` | Delete Route List for a Customer |
| `api.telephony.prem_pstn.route_list.details` | `GET` | `/telephony/config/premisePstn/routeLists/{rl_id}` | Get Route List Details. |
| `api.telephony.prem_pstn.route_list.list` | `GET` | `/telephony/config/premisePstn/routeLists` | List all Route Lists for the organization. |
| `api.telephony.prem_pstn.route_list.numbers` | `GET` | `/telephony/config/premisePstn/routeLists/{rl_id}/numbers` | Get numbers assigned to a Route List |
| `api.telephony.prem_pstn.route_list.update` | `PUT` | `/telephony/config/premisePstn/routeLists/{rl_id}` | Modify the details for a Route List. |
| `api.telephony.prem_pstn.route_list.update_numbers` | `PUT` | `/telephony/config/premisePstn/routeLists/{rl_id}/numbers` | Modify Numbers for Route List |
| `api.telephony.prem_pstn.trunk.create` | `POST` | `/telephony/config/premisePstn/trunks` | Create a Trunk for the organization. |
| `api.telephony.prem_pstn.trunk.delete_trunk` | `DELETE` | `/telephony/config/premisePstn/trunks/{trunk_id}` | Delete a Trunk for the organization. |
| `api.telephony.prem_pstn.trunk.details` | `GET` | `/telephony/config/premisePstn/trunks/{trunk_id}` | Get a Trunk for the organization. |
| `api.telephony.prem_pstn.trunk.list` | `GET` | `/telephony/config/premisePstn/trunks` | List all Trunks for the organization. |
| `api.telephony.prem_pstn.trunk.trunk_types` | `GET` | `/telephony/config/premisePstn/trunks/trunkTypes` | List all TrunkTypes with DeviceTypes for the organization. |
| `api.telephony.prem_pstn.trunk.update` | `PUT` | `/telephony/config/premisePstn/trunks/{trunk_id}` | Modify a Trunk for the organization. |
| `api.telephony.prem_pstn.trunk.usage` | `GET` | `/telephony/config/premisePstn/trunks/{trunk_id}/usage` | Get Local Gateway Usage Count |
| `api.telephony.prem_pstn.trunk.usage_call_to_extension` | `GET` | `/telephony/config/premisePstn/trunks/{trunk_id}/usageCallToExtension` | Get local gateway call to on-premises extension usage for a trunk. |
| `api.telephony.prem_pstn.trunk.usage_dial_plan` | `GET` | `/telephony/config/premisePstn/trunks/{trunk_id}/usageDialPlan` | Get Local Gateway Dial Plan Usage for a Trunk. |
| `api.telephony.prem_pstn.trunk.usage_location_pstn` | `GET` | `/telephony/config/premisePstn/trunks/{trunk_id}/usagePstnConnection` | Get Local Gateway Dial Plan Usage for a Trunk. |
| `api.telephony.prem_pstn.trunk.usage_route_group` | `GET` | `/telephony/config/premisePstn/trunks/{trunk_id}/usageRouteGroup` | Get Local Gateway Dial Plan Usage for a Trunk. |
| `api.telephony.prem_pstn.trunk.validate_fqdn_and_domain` | `POST` | `/telephony/config/premisePstn/trunks/actions/fqdnValidation/invoke` | Validate Local Gateway FQDN and Domain for the organization trunks. |
| `api.telephony.prem_pstn.validate_pattern` | `POST` | `/telephony/config/premisePstn/actions/validateDialPatterns/invoke` | Validate a Dial Pattern. |
| `api.telephony.pstn.configure` | `PUT` | `/telephony/pstn/locations/{location_id}/connection` | Setup PSTN Connection for a Location |
| `api.telephony.pstn.list` | `GET` | `/telephony/pstn/locations/{location_id}/connectionOptions` | Retrieve PSTN Connection Options for a Location |
| `api.telephony.pstn.read` | `GET` | `/telephony/pstn/locations/{location_id}/connection` | Retrieve PSTN Connection for a Location |
| `api.telephony.read_list_of_announcement_languages` | `GET` | `/telephony/config/announcementLanguages` | Read the List of Announcement Languages |
| `api.telephony.read_moh` | `GET` | `/telephony/config/moh/settings` | Get the organization Music on Hold configuration |
| `api.telephony.route_choices` | `GET` | `/telephony/config/routeChoices` | Read the List of Routing Choices |
| `api.telephony.schedules.create` | `POST` | `/telephony/config/locations/{obj_id}/schedules` | Create a schedule |
| `api.telephony.schedules.delete_schedule` | `DELETE` | `/telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}` | Delete a schedule |
| `api.telephony.schedules.details` | `GET` | `/telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}` | Get details for a schedule |
| `api.telephony.schedules.event_create` | `POST` | `/telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}/events` | Create a schedule event |
| `api.telephony.schedules.event_delete` | `DELETE` | `/telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}/events/{event_id}` | Delete a schedule event |
| `api.telephony.schedules.event_details` | `GET` | `/telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}/events/{event_id}` | Get details for a schedule event |
| `api.telephony.schedules.event_update` | `PUT` | `/telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}/events/{event_id}` | Update a schedule event |
| `api.telephony.schedules.list` | `GET` | `/telephony/config/locations/{obj_id}/schedules` | List of schedules for a person or location |
| `api.telephony.schedules.update` | `PUT` | `/telephony/config/locations/{obj_id}/schedules/{schedule_type}/{schedule_id}` | Update a schedule |
| `api.telephony.supervisors.assign_unassign_agents` | `PUT` | `/telephony/config/supervisors/{supervisor_id}` | Assign or Unassign Agents to Supervisor |
| `api.telephony.supervisors.available_agents` | `GET` | `/telephony/config/supervisors/availableAgents` | List Available Agents |
| `api.telephony.supervisors.available_supervisors` | `GET` | `/telephony/config/supervisors/availableSupervisors` | List Available Supervisors |
| `api.telephony.supervisors.create` | `POST` | `/telephony/config/supervisors` | Create a Supervisor |
| `api.telephony.supervisors.delete` | `DELETE` | `/telephony/config/supervisors/{supervisor_id}` | Delete A Supervisor |
| `api.telephony.supervisors.delete_bulk` | `DELETE` | `/telephony/config/supervisors` | Delete Bulk supervisors |
| `api.telephony.supervisors.details` | `GET` | `/telephony/config/supervisors/{supervisor_id}` | GET Supervisor Details |
| `api.telephony.supervisors.list` | `GET` | `/telephony/config/supervisors` | Get List of Supervisors |
| `api.telephony.supported_devices` | `GET` | `/telephony/config/supportedDevices` | Read the List of Supported Devices |
| `api.telephony.test_call_routing` | `POST` | `/telephony/config/actions/testCallRouting/invoke` | Test Call Routing |
| `api.telephony.ucm_profiles` | `GET` | `/telephony/config/callingProfiles` | Read the List of UC Manager Profiles |
| `api.telephony.update_call_captions_settings` | `PUT` | `/telephony/config/callCaptions` | Update the organization call captions settings |
| `api.telephony.update_moh` | `PUT` | `/telephony/config/moh/settings` | Update the organization Music on Hold configuration |
| `api.telephony.validate_extensions` | `POST` | `/telephony/config/actions/validateExtensions/invoke` | Validate the List of Extensions |
| `api.telephony.validate_phone_numbers` | `POST` | `/telephony/config/actions/validateNumbers/invoke` | Validate phone numbers |
| `api.telephony.virtual_extensions.create_extension` | `POST` | `/telephony/config/virtualExtensions` | Create a Virtual Extension |
| `api.telephony.virtual_extensions.create_range` | `POST` | `/telephony/config/virtualExtensionRanges` | Create a Virtual Extension Range |
| `api.telephony.virtual_extensions.delete_extension` | `DELETE` | `/telephony/config/virtualExtensions/{extension_id}` | Delete a Virtual Extension |
| `api.telephony.virtual_extensions.delete_range` | `DELETE` | `/telephony/config/virtualExtensionRanges/{extension_range_id}` | Delete a Virtual Extension Range |
| `api.telephony.virtual_extensions.details_extension` | `GET` | `/telephony/config/virtualExtensions/{extension_id}` | Get a Virtual Extension |
| `api.telephony.virtual_extensions.details_range` | `GET` | `/telephony/config/virtualExtensionRanges/{extension_range_id}` | Get details of a Virtual Extension Range |
| `api.telephony.virtual_extensions.get_extension_settings` | `GET` | `/telephony/config/virtualExtensions/settings` | Get Virtual extension settings |
| `api.telephony.virtual_extensions.list_extensions` | `GET` | `/telephony/config/virtualExtensions` | Read the List of Virtual Extensions |
| `api.telephony.virtual_extensions.list_range` | `GET` | `/telephony/config/virtualExtensionRanges` | Get a list of a Virtual Extension Range |
| `api.telephony.virtual_extensions.modify_extension_settings` | `PUT` | `/telephony/config/virtualExtensions/settings` | Modify Virtual Extension Settings |
| `api.telephony.virtual_extensions.modify_range` | `PUT` | `/telephony/config/virtualExtensionRanges/{extension_range_id}` | Modify Virtual Extension Range |
| `api.telephony.virtual_extensions.update_extension` | `PUT` | `/telephony/config/virtualExtensions/{extension_id}` | Update a Virtual Extension |
| `api.telephony.virtual_extensions.validate_external_phone_number` | `POST` | `/telephony/config/virtualExtensions/actions/validateNumbers/invoke` | Validate an external phone number |
| `api.telephony.virtual_extensions.validate_range` | `POST` | `/telephony/config/virtualExtensionRanges/actions/validate/invoke` | Validate the prefix and extension pattern for a Virtual Extension Range. |
| `api.telephony.virtual_lines.agent_caller_id.available_caller_ids` | `GET` | `/telephony/config/virtualLines/{entity_id}/agent/availableCallerIds` | Retrieve Agent's List of Available Caller IDs |
| `api.telephony.virtual_lines.agent_caller_id.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/agent/callerId` | Modify Agent's Caller ID Information. |
| `api.telephony.virtual_lines.agent_caller_id.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/agent/callerId` | Retrieve Agent's Caller ID Information |
| `api.telephony.virtual_lines.assigned_devices` | `GET` | `/telephony/config/virtualLines/{virtual_line_id}/devices` | Get List of Devices assigned for a Virtual Line |
| `api.telephony.virtual_lines.available_numbers.available` | `GET` | `/telephony/config/virtualLines/availableNumbers` | Get Available Phone Numbers |
| `api.telephony.virtual_lines.available_numbers.call_forward` | `GET` | `/telephony/config/virtualLines/{entity_id}/callForwarding/availableNumbers` | Get Call Forward Available Phone Numbers |
| `api.telephony.virtual_lines.available_numbers.call_intercept` | `GET` | `/callIntercept` | Get Call Intercept Available Phone Numbers |
| `api.telephony.virtual_lines.available_numbers.ecbn` | `GET` | `/telephony/config/virtualLines/{entity_id}/emergencyCallbackNumber/availableNumbers` | Get ECBN Available Phone Numbers |
| `api.telephony.virtual_lines.available_numbers.fax_message` | `GET` | `/telephony/config/virtualLines/{entity_id}/faxMessage/availableNumbers` | Get Fax Message Available Phone Numbers |
| `api.telephony.virtual_lines.available_numbers.primary` | `GET` | `/primary` | Get Person Primary Available Phone Numbers |
| `api.telephony.virtual_lines.available_numbers.secondary` | `GET` | `/secondary` | Get Person Secondary Available Phone Numbers |
| `api.telephony.virtual_lines.barge.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/bargeIn` | Configure Barge In Settings |
| `api.telephony.virtual_lines.barge.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/bargeIn` | Retrieve Barge In Settings |
| `api.telephony.virtual_lines.call_bridge.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/callBridge` | Configure Call Bridge Settings |
| `api.telephony.virtual_lines.call_bridge.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/callBridge` | Read Call Bridge Settings |
| `api.telephony.virtual_lines.call_intercept.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/intercept` | Configure Call Intercept Settings |
| `api.telephony.virtual_lines.call_intercept.greeting` | `POST` | `/telephony/config/virtualLines/{entity_id}/intercept/actions/announcementUpload/invoke` | Configure Call Intercept Greeting |
| `api.telephony.virtual_lines.call_intercept.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/intercept` | Read Call Intercept Settings |
| `api.telephony.virtual_lines.call_recording.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/callRecording` | Configure Call Recording Settings for a entity |
| `api.telephony.virtual_lines.call_recording.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/callRecording` | Read Call Recording Settings |
| `api.telephony.virtual_lines.call_waiting.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/callWaiting` | Configure Call Waiting Settings |
| `api.telephony.virtual_lines.call_waiting.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/callWaiting` | Read Call Waiting Settings for |
| `api.telephony.virtual_lines.caller_id.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/callerId` | Configure a Caller ID Settings |
| `api.telephony.virtual_lines.caller_id.configure_settings` | `PUT` | `/telephony/config/virtualLines/{entity_id}/callerId` | Configure a Caller ID Settings |
| `api.telephony.virtual_lines.caller_id.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/callerId` | Retrieve Caller ID Settings |
| `api.telephony.virtual_lines.create` | `POST` | `/telephony/config/virtualLines` | Create a Virtual Line |
| `api.telephony.virtual_lines.dect_networks` | `GET` | `/telephony/config/virtualLines/{virtual_line_id}/dectNetworks` | Get List of Dect Networks Handsets for a Virtual Line |
| `api.telephony.virtual_lines.delete` | `DELETE` | `/telephony/config/virtualLines/{virtual_line_id}` | Delete a Virtual Line |
| `api.telephony.virtual_lines.details` | `GET` | `/telephony/config/virtualLines/{virtual_line_id}` | Get Details for a Virtual Line |
| `api.telephony.virtual_lines.dnd.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/doNotDisturb` | Configure Do Not Disturb Settings for an entity |
| `api.telephony.virtual_lines.dnd.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/doNotDisturb` | Read Do Not Disturb Settings for an entity |
| `api.telephony.virtual_lines.ecbn.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/emergencyCallbackNumber` | Update an entity's Emergency Callback Number. |
| `api.telephony.virtual_lines.ecbn.dependencies` | `GET` | `/telephony/config/virtualLines/{entity_id}/emergencyCallbackNumber/dependencies` | Retrieve an entity's Emergency Callback Number Dependencies |
| `api.telephony.virtual_lines.ecbn.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/emergencyCallbackNumber` | Get an entity's Emergency Callback Number |
| `api.telephony.virtual_lines.forwarding.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/callForwarding` | Configure an Entity's Call Forwarding Settings |
| `api.telephony.virtual_lines.forwarding.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/callForwarding` | Retrieve an entity's Call Forwarding Settings |
| `api.telephony.virtual_lines.get_phone_number` | `GET` | `/telephony/config/virtualLines/{virtual_line_id}/number` | Get Phone Number assigned for a Virtual Line |
| `api.telephony.virtual_lines.list` | `GET` | `/telephony/config/virtualLines` | List all Virtual Lines for the organization. |
| `api.telephony.virtual_lines.music_on_hold.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/musicOnHold` | Configure Music On Hold Settings for a Personvirtual line, or workspace. |
| `api.telephony.virtual_lines.music_on_hold.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/musicOnHold` | Retrieve Music On Hold Settings for a Person, virtual line, or workspace. |
| `api.telephony.virtual_lines.permissions_in.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/incomingPermission` | Configure incoming permissions settings |
| `api.telephony.virtual_lines.permissions_in.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/incomingPermission` | Read Incoming Permission Settings |
| `api.telephony.virtual_lines.permissions_out.access_codes.create` | `POST` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/accessCodes` | Create new Access codes. |
| `api.telephony.virtual_lines.permissions_out.access_codes.delete` | `DELETE` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/accessCodes` | Delete Access Code |
| `api.telephony.virtual_lines.permissions_out.access_codes.modify` | `PUT` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/accessCodes` | Modify Access Codes |
| `api.telephony.virtual_lines.permissions_out.access_codes.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/accessCodes` | Retrieve Access codes. |
| `api.telephony.virtual_lines.permissions_out.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission` | Configure Outgoing Calling Permissions Settings |
| `api.telephony.virtual_lines.permissions_out.digit_patterns.create` | `POST` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns` | Create Digit Patterns |
| `api.telephony.virtual_lines.permissions_out.digit_patterns.delete` | `DELETE` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}` | Delete a Digit Pattern |
| `api.telephony.virtual_lines.permissions_out.digit_patterns.delete_all` | `DELETE` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns` | Delete all Digit Patterns. |
| `api.telephony.virtual_lines.permissions_out.digit_patterns.details` | `GET` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}` | Retrieve Digit Pattern Details |
| `api.telephony.virtual_lines.permissions_out.digit_patterns.get_digit_patterns` | `GET` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns` | Retrieve Digit Patterns |
| `api.telephony.virtual_lines.permissions_out.digit_patterns.update` | `PUT` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns/{id}` | Modify Digit Patterns |
| `api.telephony.virtual_lines.permissions_out.digit_patterns.update_category_control_settings` | `PUT` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/digitPatterns` | Modify the Digit Pattern Category Control Settings for the entity |
| `api.telephony.virtual_lines.permissions_out.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission` | Retrieve Outgoing Calling Permissions Settings |
| `api.telephony.virtual_lines.permissions_out.transfer_numbers.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/autoTransferNumbers` | Modify Transfer Numbers Settings for an entity. |
| `api.telephony.virtual_lines.permissions_out.transfer_numbers.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/outgoingPermission/autoTransferNumbers` | Retrieve Transfer Numbers Settings . |
| `api.telephony.virtual_lines.privacy.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/privacy` | Configure an entity's Privacy Settings |
| `api.telephony.virtual_lines.privacy.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/privacy` | Get Privacy Settings for an entity |
| `api.telephony.virtual_lines.push_to_talk.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/pushToTalk` | Configure Push-to-Talk Settings for an entity |
| `api.telephony.virtual_lines.push_to_talk.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/pushToTalk` | Read Push-to-Talk Settings for an entity |
| `api.telephony.virtual_lines.update` | `PUT` | `/telephony/config/virtualLines/{virtual_line_id}` | Update a Virtual Line |
| `api.telephony.virtual_lines.update_directory_search` | `PUT` | `/telephony/config/virtualLines/{virtual_line_id}/directorySearch` | Update Directory search for a Virtual Line |
| `api.telephony.virtual_lines.voicemail.configure` | `PUT` | `/telephony/config/virtualLines/{entity_id}/voicemail` | Configure Voicemail Settings for an entity |
| `api.telephony.virtual_lines.voicemail.modify_passcode` | `PUT` | `/telephony/config/virtualLines/{entity_id}/voicemail/passcode` | Modify an entity's voicemail passcode. |
| `api.telephony.virtual_lines.voicemail.read` | `GET` | `/telephony/config/virtualLines/{entity_id}/voicemail` | Read Voicemail Settings for an entity |
| `api.telephony.virtual_lines.voicemail.reset_pin` | `POST` | `/telephony/config/virtualLines/{entity_id}/voicemail/actions/resetPin/invoke` | Reset Voicemail PIN |
| `api.telephony.voice_messaging.delete` | `DELETE` | `/telephony/voiceMessages/{message_id}` | Delete a specific voicemail message for the user. |
| `api.telephony.voice_messaging.list` | `GET` | `/telephony/voiceMessages` | Get the list of all voicemail messages for the user. |
| `api.telephony.voice_messaging.mark_as_read` | `POST` | `/telephony/voiceMessages/markAsRead` | Update the voicemail message(s) as read for the user. |
| `api.telephony.voice_messaging.mark_as_unread` | `POST` | `/telephony/voiceMessages/markAsUnread` | Update the voicemail message(s) as unread for the user. |
| `api.telephony.voice_messaging.summary` | `GET` | `/telephony/voiceMessages/summary` | Get a summary of the voicemail messages for the user. |
| `api.telephony.voicemail_groups.available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/voicemailGroups/availableNumbers` | Get Voicemail Group Available Phone Numbers |
| `api.telephony.voicemail_groups.create` | `POST` | `/telephony/config/locations/{location_id}/voicemailGroups` | Create new voicemail group for the given location for a customer. |
| `api.telephony.voicemail_groups.delete` | `DELETE` | `/telephony/config/locations/{location_id}/voicemailGroups/{voicemail_group_id}` | Delete the designated voicemail group. |
| `api.telephony.voicemail_groups.details` | `GET` | `/telephony/config/locations/{location_id}/voicemailGroups/{voicemail_group_id}` | Retrieve voicemail group details for a location. |
| `api.telephony.voicemail_groups.fax_message_available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/voicemailGroups/faxMessage/availableNumbers` | Get Voicemail Group Fax Message Available Phone Numbers |
| `api.telephony.voicemail_groups.list` | `GET` | `/telephony/config/voicemailGroups` | List the voicemail group information for the organization. |
| `api.telephony.voicemail_groups.update` | `PUT` | `/telephony/config/locations/{location_id}/voicemailGroups/{voicemail_group_id}` | Modifies the voicemail group location details for a particular location for a customer. |
| `api.telephony.voicemail_rules.read` | `GET` | `/telephony/config/voicemail/rules` | Get Voicemail Rules |
| `api.telephony.voicemail_rules.update` | `PUT` | `/telephony/config/voicemail/rules` | Update Voicemail Rules |
| `api.telephony.voiceportal.available_phone_numbers` | `GET` | `/telephony/config/locations/{location_id}/voicePortal/availableNumbers` | Get VoicePortal Available Phone Numbers |
| `api.telephony.voiceportal.passcode_rules` | `GET` | `/telephony/config/locations/{location_id}/voicePortal/passcodeRules` | Get VoicePortal Passcode Rule |
| `api.telephony.voiceportal.read` | `GET` | `/telephony/config/locations/{location_id}/voicePortal` | Get VoicePortal |
| `api.telephony.voiceportal.update` | `PUT` | `/telephony/config/locations/{location_id}/voicePortal` | Update VoicePortal |
| `api.webhook.create` | `POST` | `/webhooks` | Creates a webhook. |
| `api.webhook.details` | `GET` | `/webhooks/{webhook_id}` | Get Webhook Details |
| `api.webhook.list` | `GET` | `/webhooks` | List Webhooks |
| `api.webhook.update` | `PUT` | `/webhooks/{webhook_id}` | Updates a webhook, by ID. You cannot use this call to deactivate a webhook, only to activate a webhook that |
| `api.webhook.webhook_delete` | `DELETE` | `/webhooks/{webhook_id}` | Deletes a webhook, by ID. |
| `api.workspace_locations.create` | `POST` | `/workspaceLocations` | Create a location. The cityName and notes parameters are optional, and omitting them will result in the |
| `api.workspace_locations.delete` | `DELETE` | `/workspaceLocations/{location_id}` | Delete a Workspace Location |
| `api.workspace_locations.details` | `GET` | `/workspaceLocations/{location_id}` | Get a Workspace Location Details |
| `api.workspace_locations.floors.create` | `POST` | `/workspaceLocations/{location_id}/floors` | Create a Workspace Location Floor |
| `api.workspace_locations.floors.delete` | `DELETE` | `/workspaceLocations/{location_id}/floors/{floor_id}` | Delete a Workspace Location Floor |
| `api.workspace_locations.floors.details` | `GET` | `/workspaceLocations/{location_id}/floors/{floor_id}` | Get a Workspace Location Floor Details |
| `api.workspace_locations.floors.list` | `GET` | `/workspaceLocations/{location_id}/floors` | :param location_id: |
| `api.workspace_locations.floors.update` | `PUT` | `/workspaceLocations/{location_id}/floors/{floor_id}` | Updates details for a floor, by ID. Specify the floor ID in the floorId parameter in the URI. Include all |
| `api.workspace_locations.list` | `GET` | `/workspaceLocations` | List workspace locations |
| `api.workspace_locations.update` | `PUT` | `/workspaceLocations/{location_id}` | Update a Workspace Location |
| `api.workspace_personalization.get_personalization_task` | `GET` | `/workspaces/{workspace_id}/personalizationTask` | Get Personalization Task |
| `api.workspace_personalization.personalize_a_workspace` | `POST` | `/workspaces/{workspace_id}/personalize` | Personalize a Workspace |
| `api.workspace_settings.anon_calls.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/anonymousCallReject` | Modify Anonymous Call Settings for an entity. |
| `api.workspace_settings.anon_calls.read` | `GET` | `/telephony/config/workspaces/{entity_id}/anonymousCallReject` | Retrieve Anonymous Call Settings for an entity. |
| `api.workspace_settings.available_numbers.available` | `GET` | `/telephony/config/workspaces/availableNumbers` | Get Available Phone Numbers |
| `api.workspace_settings.available_numbers.call_forward` | `GET` | `/telephony/config/workspaces/{entity_id}/callForwarding/availableNumbers` | Get Call Forward Available Phone Numbers |
| `api.workspace_settings.available_numbers.call_intercept` | `GET` | `/telephony/config/workspaces/{entity_id}/callIntercept/availableNumbers` | Get Call Intercept Available Phone Numbers |
| `api.workspace_settings.available_numbers.ecbn` | `GET` | `/telephony/config/workspaces/{entity_id}/emergencyCallbackNumber/availableNumbers` | Get ECBN Available Phone Numbers |
| `api.workspace_settings.available_numbers.fax_message` | `GET` | `/telephony/config/workspaces/{entity_id}/faxMessage/availableNumbers` | Get Fax Message Available Phone Numbers |
| `api.workspace_settings.available_numbers.primary` | `GET` | `/primary` | Get Person Primary Available Phone Numbers |
| `api.workspace_settings.available_numbers.secondary` | `GET` | `/telephony/config/workspaces/{entity_id}/secondary/availableNumbers` | Get Person Secondary Available Phone Numbers |
| `api.workspace_settings.barge.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/bargeIn` | Configure Barge In Settings |
| `api.workspace_settings.barge.read` | `GET` | `/telephony/config/workspaces/{entity_id}/bargeIn` | Retrieve Barge In Settings |
| `api.workspace_settings.call_bridge.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/callBridge` | Configure Call Bridge Settings |
| `api.workspace_settings.call_bridge.read` | `GET` | `/telephony/config/workspaces/{entity_id}/callBridge` | Read Call Bridge Settings |
| `api.workspace_settings.call_intercept.configure` | `PUT` | `/workspaces/{entity_id}/features/intercept` | Configure Call Intercept Settings |
| `api.workspace_settings.call_intercept.greeting` | `POST` | `/workspaces/{entity_id}/features/intercept/actions/announcementUpload/invoke` | Configure Call Intercept Greeting |
| `api.workspace_settings.call_intercept.read` | `GET` | `/workspaces/{entity_id}/features/intercept` | Read Call Intercept Settings |
| `api.workspace_settings.call_policy.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/callPolicies` | Configure Call Policy Settings for an entity |
| `api.workspace_settings.call_policy.read` | `GET` | `/telephony/config/workspaces/{entity_id}/callPolicies` | Read Call Policy Settings for an entity |
| `api.workspace_settings.call_waiting.configure` | `PUT` | `/workspaces/{entity_id}/features/callWaiting` | Configure Call Waiting Settings |
| `api.workspace_settings.call_waiting.read` | `GET` | `/workspaces/{entity_id}/features/callWaiting` | Read Call Waiting Settings for |
| `api.workspace_settings.caller_id.configure` | `PUT` | `/workspaces/{entity_id}/features/callerId` | Configure a Caller ID Settings |
| `api.workspace_settings.caller_id.configure_settings` | `PUT` | `/workspaces/{entity_id}/features/callerId` | Configure a Caller ID Settings |
| `api.workspace_settings.caller_id.read` | `GET` | `/workspaces/{entity_id}/features/callerId` | Retrieve Caller ID Settings |
| `api.workspace_settings.devices.list` | `GET` | `/telephony/config/workspaces/{workspace_id}/devices` | Get all devices for a workspace. |
| `api.workspace_settings.devices.list_and_counts` | `GET` | `/telephony/config/workspaces/{workspace_id}/devices` | Get all devices for a workspace. |
| `api.workspace_settings.devices.modify_hoteling` | `PUT` | `/telephony/config/workspaces/{workspace_id}/devices` | Modify devices for a workspace. |
| `api.workspace_settings.dnd.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/doNotDisturb` | Configure Do Not Disturb Settings for an entity |
| `api.workspace_settings.dnd.read` | `GET` | `/telephony/config/workspaces/{entity_id}/doNotDisturb` | Read Do Not Disturb Settings for an entity |
| `api.workspace_settings.ecbn.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/emergencyCallbackNumber` | Update an entity's Emergency Callback Number. |
| `api.workspace_settings.ecbn.dependencies` | `GET` | `/telephony/config/workspaces/{entity_id}/emergencyCallbackNumber/dependencies` | Retrieve an entity's Emergency Callback Number Dependencies |
| `api.workspace_settings.ecbn.read` | `GET` | `/telephony/config/workspaces/{entity_id}/emergencyCallbackNumber` | Get an entity's Emergency Callback Number |
| `api.workspace_settings.forwarding.configure` | `PUT` | `/workspaces/{entity_id}/features/callForwarding` | Configure an Entity's Call Forwarding Settings |
| `api.workspace_settings.forwarding.read` | `GET` | `/workspaces/{entity_id}/features/callForwarding` | Retrieve an entity's Call Forwarding Settings |
| `api.workspace_settings.monitoring.configure` | `PUT` | `/workspaces/{entity_id}/features/monitoring` | Modify an entity's Monitoring Settings |
| `api.workspace_settings.monitoring.read` | `GET` | `/workspaces/{entity_id}/features/monitoring` | Retrieve an entity's Monitoring Settings |
| `api.workspace_settings.music_on_hold.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/musicOnHold` | Configure Music On Hold Settings for a Personvirtual line, or workspace. |
| `api.workspace_settings.music_on_hold.read` | `GET` | `/telephony/config/workspaces/{entity_id}/musicOnHold` | Retrieve Music On Hold Settings for a Person, virtual line, or workspace. |
| `api.workspace_settings.numbers.read` | `GET` | `/workspaces/{workspace_id}/features/numbers/` | List the PSTN phone numbers associated with a specific workspace, by ID, within the organization. Also shows |
| `api.workspace_settings.numbers.update` | `PUT` | `/telephony/config/workspaces/{workspace_id}/numbers` | Assign or Unassign numbers associated with a specific workspace |
| `api.workspace_settings.permissions_in.configure` | `PUT` | `/workspaces/{entity_id}/features/incomingPermission` | Configure incoming permissions settings |
| `api.workspace_settings.permissions_in.read` | `GET` | `/workspaces/{entity_id}/features/incomingPermission` | Read Incoming Permission Settings |
| `api.workspace_settings.permissions_out.access_codes.create` | `POST` | `/workspaces/{entity_id}/features/outgoingPermission/accessCodes` | Create new Access codes. |
| `api.workspace_settings.permissions_out.access_codes.delete` | `DELETE` | `/workspaces/{entity_id}/features/outgoingPermission/accessCodes` | Delete Access Code |
| `api.workspace_settings.permissions_out.access_codes.modify` | `PUT` | `/workspaces/{entity_id}/features/outgoingPermission/accessCodes` | Modify Access Codes |
| `api.workspace_settings.permissions_out.access_codes.read` | `GET` | `/workspaces/{entity_id}/features/outgoingPermission/accessCodes` | Retrieve Access codes. |
| `api.workspace_settings.permissions_out.configure` | `PUT` | `/workspaces/{entity_id}/features/outgoingPermission` | Configure Outgoing Calling Permissions Settings |
| `api.workspace_settings.permissions_out.digit_patterns.create` | `POST` | `/telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns` | Create Digit Patterns |
| `api.workspace_settings.permissions_out.digit_patterns.delete` | `DELETE` | `/telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}` | Delete a Digit Pattern |
| `api.workspace_settings.permissions_out.digit_patterns.delete_all` | `DELETE` | `/telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns` | Delete all Digit Patterns. |
| `api.workspace_settings.permissions_out.digit_patterns.details` | `GET` | `/telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns/{digit_pattern_id}` | Retrieve Digit Pattern Details |
| `api.workspace_settings.permissions_out.digit_patterns.get_digit_patterns` | `GET` | `/telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns` | Retrieve Digit Patterns |
| `api.workspace_settings.permissions_out.digit_patterns.update` | `PUT` | `/telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns/{id}` | Modify Digit Patterns |
| `api.workspace_settings.permissions_out.digit_patterns.update_category_control_settings` | `PUT` | `/telephony/config/workspaces/{entity_id}/outgoingPermission/digitPatterns` | Modify the Digit Pattern Category Control Settings for the entity |
| `api.workspace_settings.permissions_out.read` | `GET` | `/workspaces/{entity_id}/features/outgoingPermission` | Retrieve Outgoing Calling Permissions Settings |
| `api.workspace_settings.permissions_out.transfer_numbers.configure` | `PUT` | `/workspaces/{entity_id}/features/outgoingPermission/autoTransferNumbers` | Modify Transfer Numbers Settings for an entity. |
| `api.workspace_settings.permissions_out.transfer_numbers.read` | `GET` | `/workspaces/{entity_id}/features/outgoingPermission/autoTransferNumbers` | Retrieve Transfer Numbers Settings . |
| `api.workspace_settings.priority_alert.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/priorityAlert` | Configure Priority Alert Settings for a Workspace |
| `api.workspace_settings.priority_alert.configure_criteria` | `PUT` | `/telephony/config/workspaces/{entity_id}/priorityAlert/criteria/{id}` | Modify Priority Alert Criteria for a Workspace |
| `api.workspace_settings.priority_alert.create_criteria` | `POST` | `/telephony/config/workspaces/{entity_id}/priorityAlert/criteria` | Create Priority Alert Criteria for a Workspace |
| `api.workspace_settings.priority_alert.delete_criteria` | `DELETE` | `/telephony/config/workspaces/{entity_id}/priorityAlert/criteria/{id}` | Delete Priority Alert Criteria for a Workspace |
| `api.workspace_settings.priority_alert.read` | `GET` | `/telephony/config/workspaces/{entity_id}/priorityAlert` | Retrieve Priority Alert Settings for a Workspace. |
| `api.workspace_settings.priority_alert.read_criteria` | `GET` | `/telephony/config/workspaces/{entity_id}/priorityAlert/criteria/{id}` | Retrieve Priority Alert Criteria for a Workspace |
| `api.workspace_settings.privacy.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/privacy` | Configure an entity's Privacy Settings |
| `api.workspace_settings.privacy.read` | `GET` | `/telephony/config/workspaces/{entity_id}/privacy` | Get Privacy Settings for an entity |
| `api.workspace_settings.push_to_talk.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/pushToTalk` | Configure Push-to-Talk Settings for an entity |
| `api.workspace_settings.push_to_talk.read` | `GET` | `/telephony/config/workspaces/{entity_id}/pushToTalk` | Read Push-to-Talk Settings for an entity |
| `api.workspace_settings.selective_accept.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/selectiveAccept` | Modify Selective Accept Settings for an entity. |
| `api.workspace_settings.selective_accept.configure_criteria` | `PUT` | `/telephony/config/workspaces/{entity_id}/selectiveAccept/criteria/{id}` | Modify Selective Accept Criteria for an entity |
| `api.workspace_settings.selective_accept.create_criteria` | `POST` | `/telephony/config/workspaces/{entity_id}/selectiveAccept/criteria` | Create Selective Accept Criteria for an entity |
| `api.workspace_settings.selective_accept.delete_criteria` | `DELETE` | `/telephony/config/workspaces/{entity_id}/selectiveAccept/criteria/{id}` | Delete Selective Accept Criteria for an entity |
| `api.workspace_settings.selective_accept.read` | `GET` | `/telephony/config/workspaces/{entity_id}/selectiveAccept` | Retrieve Selective Accept Settings for an entity. |
| `api.workspace_settings.selective_accept.read_criteria` | `GET` | `/telephony/config/workspaces/{entity_id}/selectiveAccept/criteria/{id}` | Retrieve Selective Accept Criteria for an entity |
| `api.workspace_settings.selective_forward.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/selectiveForward` | Modify Selective Forward Settings for a Workspace |
| `api.workspace_settings.selective_forward.configure_criteria` | `PUT` | `/telephony/config/workspaces/{entity_id}/selectiveForward/criteria/{id}` | Modify Selective Forward Criteria for a Workspace |
| `api.workspace_settings.selective_forward.create_criteria` | `POST` | `/telephony/config/workspaces/{entity_id}/selectiveForward/criteria` | Create Selective Forward Criteria for a Workspace |
| `api.workspace_settings.selective_forward.delete_criteria` | `DELETE` | `/telephony/config/workspaces/{entity_id}/selectiveForward/criteria/{id}` | Delete Selective Forward Criteria for a Workspace |
| `api.workspace_settings.selective_forward.read` | `GET` | `/telephony/config/workspaces/{entity_id}/selectiveForward` | Retrieve Selective Forward Settings for a Workspace |
| `api.workspace_settings.selective_forward.read_criteria` | `GET` | `/telephony/config/workspaces/{entity_id}/selectiveForward/criteria/{id}` | Retrieve Selective Forward Criteria for a Workspace |
| `api.workspace_settings.selective_reject.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/selectiveReject` | Modify Selective Reject Settings for an entity. |
| `api.workspace_settings.selective_reject.configure_criteria` | `PUT` | `/telephony/config/workspaces/{entity_id}/selectiveReject/criteria/{id}` | Modify Selective Reject Criteria for an entity |
| `api.workspace_settings.selective_reject.create_criteria` | `POST` | `/telephony/config/workspaces/{entity_id}/selectiveReject/criteria` | Create Selective Reject Criteria for an entity |
| `api.workspace_settings.selective_reject.delete_criteria` | `DELETE` | `/telephony/config/workspaces/{entity_id}/selectiveReject/criteria/{id}` | Delete Selective Reject Criteria for an entity |
| `api.workspace_settings.selective_reject.read` | `GET` | `/telephony/config/workspaces/{entity_id}/selectiveReject` | Retrieve Selective Reject Settings for an entity. |
| `api.workspace_settings.selective_reject.read_criteria` | `GET` | `/telephony/config/workspaces/{entity_id}/selectiveReject/criteria/{id}` | Retrieve Selective Reject Criteria for an entity |
| `api.workspace_settings.sequential_ring.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/sequentialRing` | Modify sequential ring settings for an entity. |
| `api.workspace_settings.sequential_ring.configure_criteria` | `PUT` | `/telephony/config/workspaces/{entity_id}/sequentialRing/criteria/{id}` | Modify sequential ring criteria for an entity. |
| `api.workspace_settings.sequential_ring.create_criteria` | `POST` | `/telephony/config/workspaces/{entity_id}/sequentialRing/criteria` | Create sequential ring criteria for an entity. |
| `api.workspace_settings.sequential_ring.delete_criteria` | `DELETE` | `/telephony/config/workspaces/{entity_id}/sequentialRing/criteria/{id}` | Delete sequential ring criteria for an entity. |
| `api.workspace_settings.sequential_ring.read` | `GET` | `/telephony/config/workspaces/{entity_id}/sequentialRing` | Retrieve sequential ring settings for an entity. |
| `api.workspace_settings.sequential_ring.read_criteria` | `GET` | `/telephony/config/workspaces/{entity_id}/sequentialRing/criteria/{id}` | Retrieve sequential ring criteria for an entity. |
| `api.workspace_settings.sim_ring.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/simultaneousRing` | Modify Simultaneous Ring Settings for an entity. |
| `api.workspace_settings.sim_ring.configure_criteria` | `PUT` | `/telephony/config/workspaces/{entity_id}/simultaneousRing/criteria/{id}` | Modify Simultaneous Ring Criteria for an entity |
| `api.workspace_settings.sim_ring.create_criteria` | `POST` | `/telephony/config/workspaces/{entity_id}/simultaneousRing/criteria` | Create Simultaneous Ring Criteria for an entity |
| `api.workspace_settings.sim_ring.delete_criteria` | `DELETE` | `/telephony/config/workspaces/{entity_id}/simultaneousRing/criteria/{id}` | Delete Simultaneous Ring Criteria for an entity |
| `api.workspace_settings.sim_ring.read` | `GET` | `/telephony/config/workspaces/{entity_id}/simultaneousRing` | Retrieve Simultaneous Ring Settings for an entity. |
| `api.workspace_settings.sim_ring.read_criteria` | `GET` | `/telephony/config/workspaces/{entity_id}/simultaneousRing/criteria/{id}` | Retrieve Simultaneous Ring Criteria for an entity |
| `api.workspace_settings.voicemail.configure` | `PUT` | `/telephony/config/workspaces/{entity_id}/voicemail` | Configure Voicemail Settings for an entity |
| `api.workspace_settings.voicemail.modify_passcode` | `PUT` | `/telephony/config/workspaces/{entity_id}/voicemail/passcode` | Modify an entity's voicemail passcode. |
| `api.workspace_settings.voicemail.read` | `GET` | `/telephony/config/workspaces/{entity_id}/voicemail` | Read Voicemail Settings for an entity |
| `api.workspace_settings.voicemail.reset_pin` | `POST` | `/telephony/config/workspaces/{entity_id}/voicemail/actions/resetPin/invoke` | Reset Voicemail PIN |
| `api.workspaces.capabilities` | `GET` | `/workspaces/{workspace_id}/capabilities` | Shows the capabilities for a workspace by ID. |
| `api.workspaces.create` | `POST` | `/workspaces` | Create a Workspace |
| `api.workspaces.delete_workspace` | `DELETE` | `/workspaces/{workspace_id}` | Delete a Workspace |
| `api.workspaces.details` | `GET` | `/workspaces/{workspace_id}` | Get Workspace Details |
| `api.workspaces.list` | `GET` | `/workspaces` | List Workspaces |
| `api.workspaces.update` | `PUT` | `/workspaces/{workspace_id}` | Update a Workspace |
| `api.xapi.execute_command` | `POST` | `/xapi/command/{command_name}` | Execute Command |
| `api.xapi.query_status` | `GET` | `/xapi/status` | Query Status |

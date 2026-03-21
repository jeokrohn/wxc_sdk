## 1.31.1 (2026-03-21)

### Fix

- NameError: name 'RedSkyAddress' is not defined

## 1.31.0 (2026-03-17)

### Feat

- emergency services API enhancements (RedSky) for org and locations

### Fix

- api.jobs.disable_calling_location.errors is a Generator now, more relaxed deserialization for StepExecutionStatus
- improved handling of TNs; enforce +E.164
- more permissive validation for enum SelectiveScheduleLevel
- parameter fail_on_errors is optional in api.scim.bulk.bulk_request
- new attribute ManagedGroup.org_id
- allow floats for min/max of dynamic device settings validation rules
- added new AuditEventData attributes based on unit test result
- stop following pagination if empty list is returned

## 1.30.0 (2026-03-11)

### Feat

- new api api.telephony.caller_reputation_provider
- new endpoint api.me.contact_center_extensions
- new endpoint api.telephony.playlist.usage
- new api api.telephony.call_controls_members
- new method api.person_settings.app_shared_line.members_count
- new cdr fields interaction_id, wx_cc_consult_merge_status
- new method api.telephony.get_large_organization_status
- new methods api.telephony.devices.get_count_of_available_members, api.telephony.devices.get_count_of_members

### Fix

- updated enums WorkSpaceType not_set, meeting_room; slight chance of breaking code
- changed attribute "routingPrefix" to "routing_prefix" in some places; slight chance of breaking existing code

## 1.29.1 (2026-03-06)

### Fix

- switch to local build

## 1.29.0 (2026-03-06)

### Feat

- significant enhancements for api.me

## 1.28.0 (2026-03-06)

## 1.28 (2026-02-12)

## 1.27.1 (2025-10-30)

## 1.27.0 (2025-10-07)

## 1.26.0 (2025-08-13)

## 1.25.0 (2025-05-30)

## 1.24.0 (2025-03-02)

## 1.23.0 (2024-11-25)

## 1.22.1 (2024-09-13)

## 1.22.0 (2024-08-29)

## 1.21.1 (2024-07-29)

## 1.21.0 (2024-07-27)

## 1.20.0 (2024-06-24)

## 1.19.0 (2024-05-03)

## 1.18.0 (2024-03-19)

## 1.17.1 (2023-12-07)

## 1.17.0 (2023-11-29)

## 1.16.1 (2023-09-04)

## 1.16.0 (2023-08-30)

## 1.15.0 (2023-07-28)

## 1.14.1 (2023-05-23)

## 1.14.0 (2023-05-16)

## 1.13.0 (2023-04-21)

## 1.12.0 (2023-02-18)

## 1.11.0 (2023-01-31)

### BREAKING CHANGE

- renamed classes WebHook, WebHookEvent, WebHookEventType, WebHookResource, WebHookStatus

### Feat

- new attribute browser_client_id in :class:`wxc_sdk.person_settings.appservices.AppServicesSettings`

### Fix

- consistent non-camelcase "Webhook" instead of mixed "Webhook" and "WebHook" usage

## 1.10.1 (2022-11-23)

## 1.10.0 (2022-11-23)

## 1.9.0 (2022-11-15)

## 1.8.0 (2022-11-10)

### Feat

- new option "force" for scripts/api_ref feat: finished developer.webex.com/compare.py: comparing two API specs
- scripts/api_ref feat: pull API specs w/ authentication feat: initial take on comparing API specs
- endpoint and type summary; integration into build scripts
- summarizing endpoints by common endpoint prefix
- summarizing endpoints by common endpoint prefix
- initial experiments with scraping API specs from developer.webex.com
- improved output and logging for test_telephony_voicemail_group.TestVmGroup.test_003_list_pagination

### Fix

- various issues with parsing class hierarchies.
- change 'method' to 'http_method'

## 1.7.2 (2022-10-19)

## 1.7.1 (2022-10-19)

### Feat

- cleanup.py also deletes test dial plans

### Fix

- accidentally removed support for call type NATIONAL; re-added
- listing workspace numbers only makes sense for workspaces with calling type "webex"; WXCAPIBULK-136 fix: corrected response type for :meth:`wxc_sdk.workspace_settings.numbers.WorkspaceNumbersApi.read`

## 1.7.0 (2022-10-17)

### Feat

- :class:`wxc_sdk.telephony.jobs.DeviceSettingsJobsApi` available in :class:`wxc_sdk.devices.DevicesApi`: :attr:`wxc_sdk.devices.DevicesApi.settings_jobs` fix: proper handling of show_all_types parameter in :meth:`wxc_sdk.people.PeopleApi.update` feat: :class:`wxc_sdk.person_settings.agent_caller_id.AgentCallerIdApi` available in :class:`wxc_sdk.person_settings.PersonSettingsApi`: :attr:`wxc_sdk.person_settings.PersonSettingsApi.agent_caller_id` feat: :meth:`wxc_sdk.person_settings.PersonSettingsApi.devices`: get devices of a user feat: new call queue settings: :attr:`wxc_sdk.telephony.callqueue.QueueSettings.comfort_message_bypass`, :attr:`wxc_sdk.telephony.callqueue.QueueSettings.whisper_message` feat: new call queue policy setting to support skill based routing: :attr:`wxc_sdk.telephony.callqueue.CallQueueCallPolicies.routing_type` feat: new telephony devices API: :attr:`wxc_sdk.telephony.TelephonyApi.devices` feat: new telephony jobs API: :attr:`wxc_sdk.telephony.TelephonyApi.jobs` feat: new method to get location level device settings: :meth:`wxc_sdk.telephony.location.TelephonyLocationApi.device_settings` feat: get supported devices: :meth:`wxc_sdk.telephony.TelephonyApi.supported_devices` feat: get organisation level device settings: :meth:`wxc_sdk.telephony.TelephonyApi.device_settings` feat: new API: :attr:`wxc_sdk.workspace_settings.WorkspaceSettingsApi.numbers` feat: new API to manage agent caller id settings for users: :attr:`wxc_sdk.person_settings.PersonSettingsApi.agent_caller_id` feat: new call queue agent attributes: :attr:`wxc_sdk.telephony.hg_and_cq.Agent.skill_level`, :attr:`wxc_sdk.telephony.hg_and_cq.Agent.join_enabled` fix: updated outgoing permission call types to latest call types: :class:`wxc_sdk.person_settings.permissions_out.OutgoingPermissionCallType` fix: ignore calltypes not supported in calling permissions any more: national, casual, url_dialing, unknown
- doc updates
- example call_intercept.py, enable debug output if run in debugger
- DialPlan attributes name and route_name now optional to simplify instantiation for updates
- doc string updates
- new example call_intercept.py
- new attribute :attr:`wxc_sdk.person_settings.appservices.AppServicesSettings.desktop_client_id`
- devices API, :attr:`wxc_sdk.WebexSimpleApi.devices`
- support explicit content-type for REST requests
- workspace locations (and floors) API, :attr:`wxc_sdk.WebexSimpleApi.workspace_locations`

### Fix

- remove redundant set_expiration() call in get_cached_tokens()
- matching failed for last method in class if followed by decorated class
- catch error in pagination if empty response is returned
- custom_number_info removed from ExternalCallerIdNamePolicy
- parse_scopes with None parameter raised an exception
- workaround for wrong pagination urls not required any more fix: dumping REST messages with no valid time diff caused an exception fix: exclude refresh token values from REST debug
- moving change_announcement_language to :class:`wxc_sdk.telephony.location.TelephonyLocationApi`
- added missing return type str to :meth:`wxc_sdk.locations.LocationsApi.create`

## 1.6.0 (2022-08-26)

### Feat

- organizations API
- CRUD for voicemail groups in :class:`wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi`
- better error handling, support follow_pagination w/o model (compatible to sync version)
- new helper (validator): plus1

### Fix

- typo in VoicemailSettings.default()
- workaround for pagination URL issue also for async API
- cosmetic changes
- TestDeleteTestTrunks.test_001_delete_test_trunks, actually only delete test trunks!
- :meth:`wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.details now also always returns dial plan id`
- TODO edit
- TODO edit
- :meth:`wxc_sdk.person_settings.NumbersApi.read`, doc string updates

## 1.5.2 (2022-08-03)

## v1.5.1 (2022-08-03)

## 1.5.0 (2022-08-02)

## 1.4.1 (2022-05-16)

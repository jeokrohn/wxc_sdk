Release history
===============

1.28
----
- fix: ignore status 400 for :meth:`api.telephony.location.number.add <wxc_sdk.telephony.location.numbers.LocationNumbersApi.add>`
- fix: :meth:`api.telephony.prem_pstn.dial_plan.modify_patterns <wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.modify_patterns>` had wrong body content
- feat: new api: :attr:`api.telephony.emergency_address <wxc_sdk.telephony.TelephonyApi.emergency_address>`
- feat: new endpoint :meth:`api.authorizations.get_token_expiration_status <wxc_sdk.authorizations.AuthorizationsApi.get_token_expiration_status>`
- feat: new endpoint :meth:`api.telephony.calls.update_external_voicemail_mwi <wxc_sdk.telephony.calls.CallsApi.update_external_voicemail_mwi>`
- feat: updated parameters for :meth:`api.telephony.devices.available_members <wxc_sdk.telephony.devices.TelephonyDevicesApi.available_members>`
- feat: new attributes :attr:`api.telephony.autoattendant.AutoAttendant.direct_line_caller_id_name <wxc_sdk.telephony.autoattendant.AutoAttendant.dial_by_name>`, :attr:`api.telephony.autoattendant.AutoAttendant.dial_by_name <wxc_sdk.telephony.autoattendant.AutoAttendant.dial_by_name>`
- feat: new attributes direct_line_caller_id_name and dial_by_name for HG, CQ and paging group settings
- feat: new attributes direct_line_caller_id_name and dial_by_name for voicemail group and portal, workspaces
- feat: parameter emergency_address is optional for EmergencyAddressApi.update_for_phone_number
- feat: addtl. event types for WebhookResource
- feat: addtl. CDR fields
- feat: new api :attr:`api.person_settings.executive <wxc_sdk.person_settings.PersonSettingsApi.executive>`
- feat: new api :attr:`api.telephony.virtual_lines.dnd <wxc_sdk.telephony.virtual_line.VirtualLinesApi.dnd>`
- feat: direct_line_caller_id_name, dial_by_first_name, dial_by_last_name attributes for caller id settings for users and virtual lines

1.27.1
------
- feat: new parameters host, stream for :meth:`api.cdr.get_cdr_history <wxc_sdk.cdr.DetailedCDRApi.get_cdr_history>`

1.27.0
------
- feat: support for pChargeInfoSupportPolicy on :class:`trunk details <wxc_sdk.telephony.prem_pstn.trunk.TrunkDetail>` and in :meth:`api.telephony.prem_pstn.trunk.create <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.create>` and :meth:`api.telephony.prem_pstn.trunk.update <wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.update>`
- feat: new API :attr:`api.me.go_override <wxc_sdk.me.MeSettingsApi.go_override>`
- feat: new API :attr:`api.telephony.jobs.dynamic_device_settings <wxc_sdk.telephony.jobs.JobsApi.dynamic_device_settings>`
- feat: new API :attr:`api.telephony.devices.dynamic_settings <wxc_sdk.telephony.devices.TelephonyDevicesApi.dynamic_settings>`
- feat: allow instantiation of WebexSimpleApi/AsWebexSimpleApi instances with existing session object
- feat: significant enhancements :class:`api.me.MeSettingsApi <wxc_sdk.me.MeSettingsApi>`
- feat: new endpoints :meth:`api.telephony.auto_attendant.delete_announcement_file <wxc_sdk.telephony.autoattendant.AutoAttendantApi.delete_announcement_file>`, :meth:`api.telephony.auto_attendant.list_announcement_files <wxc_sdk.telephony.autoattendant.AutoAttendantApi.list_announcement_files>`
- feat: delete locations. New endpoints :meth:`api.locations.delete <wxc_sdk.locations.LocationsApi.delete>`, :meth:`api.telephony.locations.safe_delete_check_before_disabling_calling_location <wxc_sdk.telephony.location.TelephonyLocationApi.safe_delete_check_before_disabling_calling_location>`. new api - :attr:`api.jobs.disable_calling_location <wxc_sdk.telephony.jobs.JobsApi.disable_calling_location>`
- feat: call captions settings at org, location, and user level: :meth:`api.me.call_captions_settings <wxc_sdk.me.MeSettingsApi.call_captions_settings>`, :meth:`api.person_settings.get_call_captions_settings <wxc_sdk.person_settings.PersonSettingsApi.get_call_captions_settings>`, :meth:`api.person_settings.update_call_captions_settings <wxc_sdk.person_settings.PersonSettingsApi.update_call_captions_settings>`, :meth:`api.telephony.get_call_captions_settings <wxc_sdk.telephony.TelephonyApi.get_call_captions_settings>`, :meth:`api.telephony.update_call_captions_settings <wxc_sdk.telephony.TelephonyApi.update_call_captions_settings>`, :meth:`api.telephony.location.get_call_captions_settings <wxc_sdk.telephony.location.TelephonyLocationApi.get_call_captions_settings>`, :meth:`api.telephony.location.update_call_captions_settings <wxc_sdk.telephony.location.TelephonyLocationApi.update_call_captions_settings>`
- feat: new CDR fields: original_called_party_uuid, recall_type, hold_duration, auto_attendant_key_pressed, queue_type, answered_elsewhere

1.26.0
------
- feat: new API :attr:`api.telephony.hotdesking_voiceportal <wxc_sdk.telephony.TelephonyApi.hotdesking_voiceportal>`
- feat: new API :attr:`api.telephony.cx_essentials.wrapup_reasons <wxc_sdk.telephony.cx_essentials.CustomerExperienceEssentialsApi.wrapup_reasons>`
- feat: new API :attr:`api.person_settings.single_number_reach <wxc_sdk.person_settings.PersonSettingsApi.single_number_reach>`
- feat: new API :attr:`api.telephony.hotdesk <wxc_sdk.telephony.TelephonyApi.hotdesk>`
- feat: new parameter carrier_id for :meth:`api.telephony.location.number.add <wxc_sdk.telephony.location.numbers.LocationNumbersApi.add>`
- feat: new API :attr:`api.person_settings.feature_access <wxc_sdk.person_settings.PersonSettingsApi.feature_access>`
- feat: new endpoint: :meth:`api.telephony.dect_devices.add_list_of_handsets <wxc_sdk.telephony.dect_devices.DECTDevicesApi.add_list_of_handsets>`
- feat: new endpoint: :meth:`api.telephony.location.number.manage_number_state <wxc_sdk.telephony.location.numbers.LocationNumbersApi.manage_number_state>`
- feat: new API: :attr:`api.telephony.cx_essentials.callqueue_recording <wxc_sdk.telephony.cx_essentials.CustomerExperienceEssentialsApi.callqueue_recording>`
- feat: new API: :attr:`api.telephony.jobs.activation_emails <wxc_sdk.telephony.jobs.JobsApi.activation_emails>`
- feat: also expose jobs API under :attr:`api.telephony.jobs <wxc_sdk.telephony.TelephonyApi.jobs>`
- feat: new parameter exclude_status for :meth:`api.people.list <wxc_sdk.people.PeopleApi.list>`
- fix: missing parameters max\_, start in :meth:`api.telephony.call_queues.agents.details <wxc_sdk.telephony.callqueue.agents.CallQueueAgentsApi.details>`
- feat: new parameter service_types for :meth:`api.telephony.pstn.list <wxc_sdk.telephony.pstn.PSTNApi.list>`
- break: signature of :meth:`api.person_settings.app_shared_line.update_members <wxc_sdk.person_settings.app_shared_line.AppSharedLineApi.update_members>` changed: parameter application_id removed
- break: signature of :meth:`api.person_settings.app_shared_line.get_members <wxc_sdk.person_settings.app_shared_line.AppSharedLineApi.get_members>` changed: parameter application_id removed.
- break: signature of :meth:`api.person_settings.app_shared_line.search_members <wxc_sdk.person_settings.app_shared_line.AppSharedLineApi.search_members>` changed: parameter application_id removed. For now :meth:`api.person_settings.app_shared_line.search_members_old <wxc_sdk.person_settings.app_shared_line.AppSharedLineApi.search_members_old>` can still be used while new method does not return member ids

1.25.0
------
- feat: new attributes :attr:`PSTNConnectionOption.route_type <wxc_sdk.telephony.pstn.PSTNConnectionOption.route_type>` and :attr:`.route_id <wxc_sdk.telephony.pstn.PSTNConnectionOption.route_type>`
- feat: new endpoints in :class:`CallRecordingSettingsApi <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi>` :meth:`get_call_recording_regions <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.get_call_recording_regions>`, :meth:`list_org_users <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.list_org_users>`, :meth:`set_location_vendor <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.set_location_vendor>`, :meth:`get_location_vendors <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.get_location_vendors>`, :meth:`get_location_vendor_id <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.get_location_vendor_id>`, :meth:`list_location_users <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.list_location_users>`, :meth:`get_org_vendors <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.get_org_vendors>`, :meth:`set_org_vendor <wxc_sdk.telephony.call_recording.CallRecordingSettingsApi.set_org_vendor>`
- fest: new job api: :attr:`api.telephony.jobs.call_recording <wxc_sdk.telephony.jobs.JobsApi.call_recording>`
- feat: option to include devices in :meth:`api.workspaces.details <wxc_sdk.workspaces.WorkspacesApi.details>`, :meth:`api.workspaces.list <wxc_sdk.workspaces.WorkspacesApi.list>`
- fix: updated attributes for class :class:`TelephonyLocation <wxc_sdk.telephony.location.TelephonyLocation>`: removed e911_setup_required, charge_number_usage_enabled, carrier_account_id
- feat: new attribute in :class:`DND settings <wxc_sdk.person_settings.dnd.DND>`: webex_go_override_enabled
- feat: new :class:`CDR <wxc_sdk.cdr.CDR>` fields: external_customer_id, redirecting_party_uuid, public_calling_ip_address, public_called_ip_address, caller_id_number, external_caller_id_number, device_owner_uuid, call_recording_platform_name, call_recording_result, call_recording_trigger
- feat: new API :attr:`api.telephony.virtual_extensions <wxc_sdk.telephony.TelephonyApi.virtual_extensions>`
- feat: new API :attr:`api.me.personal_assistant <wxc_sdk.me.MeSettingsApi.personal_assistant>`

1.24.0
------
- feat: new API: :attr:`api.person_settings.selective_accept <wxc_sdk.person_settings.PersonSettingsApi.selective_accept>`
- feat: new API: :attr:`api.person_settings.selective_forward <wxc_sdk.person_settings.PersonSettingsApi.selective_forward>`
- feat: new API: :attr:`api.person_settings.selective_reject <wxc_sdk.person_settings.PersonSettingsApi.selective_reject>`
- feat: new parameter `topic` in :meth:`api.converged_recordings.ConvergedRecordingsApi.list <wxc_sdk.converged_recordings.ConvergedRecordingsApi.list>`
- feat: new method :meth:`api.converged_recordings.ConvergedRecordingsApi.move_recordings_into_the_recycle_bin <wxc_sdk.converged_recordings.ConvergedRecordingsApi.move_recordings_into_the_recycle_bin>`
- feat: new method :meth:`api.converged_recordings.ConvergedRecordingsApi.restore_recordings_from_recycle_bin <wxc_sdk.converged_recordings.ConvergedRecordingsApi.restore_recordings_from_recycle_bin>`
- feat: new method :meth:`api.converged_recordings.ConvergedRecordingsApi.purge_recordings_from_recycle_bin <wxc_sdk.converged_recordings.ConvergedRecordingsApi.purge_recordings_from_recycle_bin>`
- fix: :meth:`api.devices.create_by_mac_address <wxc_sdk.devices.DevicesApi.create_by_mac_address>` returns None if device creation leads to empty response. Apparently this is the case for deskphone devices
- feat: new guest calling settings API: :attr:`api.telephony.guest_calling <wxc_sdk.telephony.TelephonyApi.guest_calling>`
- feat: new endpoint to get call token for click-to-call :meth:`api.telephony.create_a_call_token <wxc_sdk.telephony.TelephonyApi.create_a_call_token>`

- feat: person mode management settings API: :attr:`api.person_settings.mode_management <wxc_sdk.person_settings.PersonSettingsApi.mode_management>`
- feat: new endpoint to switch mode for call forwarding (AA): :meth:`api.telephony.auto_attendant.forwarding.switch_mode_for_call_forwarding <wxc_sdk.telephony.forwarding.ForwardingApi.switch_mode_for_call_forwarding>`
- feat: new endpoint to switch mode for call forwarding (CQ): :meth:`api.telephony.callqueue.forwarding.switch_mode_for_call_forwarding <wxc_sdk.telephony.forwarding.ForwardingApi.switch_mode_for_call_forwarding>`
- feat: new endpoint to switch mode for call forwarding (HG): :meth:`api.telephony.huntgroup.forwarding.switch_mode_for_call_forwarding <wxc_sdk.telephony.forwarding.ForwardingApi.switch_mode_for_call_forwarding>`
- feat: operating modes API: :attr:`api.telephony.operating_modes <wxc_sdk.telephony.TelephonyApi.operating_modes>`
- feat: personal assistant settings API: :attr:`api.person_settings.personal_assistant <wxc_sdk.person_settings.PersonSettingsApi.personal_assistant>`
- feat: new endpoints: :meth:`api.telephony.dect_devices.generate_and_enable_dect_serviceability_password <wxc_sdk.telephony.dect_devices.DECTDevicesApi.generate_and_enable_dect_serviceability_password>`, :meth:`api.telephony.dect_devices.get_dect_serviceability_password_status <wxc_sdk.telephony.dect_devices.DECTDevicesApi.get_dect_serviceability_password_status>`, :meth:`api.telephony.dect_devices.update_dect_serviceability_password_status <wxc_sdk.telephony.dect_devices.DECTDevicesApi.update_dect_serviceability_password_status>`
- feat: new endpoints: :meth:`api.telephony.location.create_receptionist_contact_directory <wxc_sdk.telephony.location.TelephonyLocationApi.create_receptionist_contact_directory>`, :meth:`api.telephony.location.delete_receptionist_contact_directory <wxc_sdk.telephony.location.TelephonyLocationApi.delete_receptionist_contact_directory>`,  :meth:`api.telephony.location.list_receptionist_contact_directories <wxc_sdk.telephony.location.TelephonyLocationApi.list_receptionist_contact_directories>`,  :meth:`api.telephony.location.modify_a_receptionist_contact_directory <wxc_sdk.telephony.location.TelephonyLocationApi.modify_a_receptionist_contact_directory>`,  :meth:`api.telephony.location.receptionist_contact_directory_details <wxc_sdk.telephony.location.TelephonyLocationApi.receptionist_contact_directory_details>`
- feat: device call settings with multi-line support
- break: changed signature for :meth:`api.person_settings.personal_assistant.update <wxc_sdk.person_settings.personal_assistant.PersonalAssistantApi.update>`
- break: AvailableAgent.numbers renamed to AvailableAgent.phone_numbers
- feat: result for meth:`api.telephony.location.number.add <wxc_sdk.telephony.location.numbers.LocationNumbersApi.add>`
- new example: add_numbers.py

1.23.0
------

- feat: new API: :attr:`api.org_contacts <wxc_sdk.WebexSimpleApi.org_contacts>`
- break: deprecated HGCallPolicies.business_continuity, use :attr:`HGCallPolicies.business_continuity_redirect <wxc_sdk.telephony.huntgroup.HGCallPolicies.business_continuity_redirect>` instead
- feat: new API: :attr:`api.xapi <wxc_sdk.WebexSimpleApi.xapi>`
- feat: support for Customer Experience Essentials.
- feat: new API: :attr:`TelephonyApi.cx_essentials <wxc_sdk.telephony.TelephonyApi.cx_essentials>`
- feat: :doc:`proxy support for the SDK <proxy>`
- feat: :doc:`HARWriter to log all requests to HAR files <har_writer>`
- feat: new API: :attr:`CallQueueApi.agents <wxc_sdk.telephony.callqueue.CallQueueApi.agents>`
- fix: enable creation of CX essentials queues: `has_cx_essentials` parameter in :meth:`api.telephony.callqueue.create <wxc_sdk.telephony.callqueue.CallQueueApi.create>`


1.22.1
------
- fix: correct handling of type\_ parameter in :meth:`api.events.list <wxc_sdk.events.EventsApi.list>`
- fix: corrected handling of password parameter in `api.devices.create_by_mac_address <wxc_sdk.devices.DevicesApi.create_by_mac_address>`
- fix: pydantic incompatibility with typing-extensions 4.12.0

1.22.0
------

- feat: new available number endpoints:

  * :meth:`api.telephony.auto_attendant.alternate_available_phone_numbers <wxc_sdk.telephony.autoattendant.AutoAttendantApi.alternate_available_phone_numbers>`
  * :meth:`api.telephony.auto_attendant.call_forward_available_phone_numbers <wxc_sdk.telephony.autoattendant.AutoAttendantApi.call_forward_available_phone_numbers>`
  * :meth:`api.telephony.auto_attendant.primary_available_phone_numbers <wxc_sdk.telephony.autoattendant.AutoAttendantApi.primary_available_phone_numbers>`
  * :meth:`api.telephony.callqueue.alternate_available_phone_numbers <wxc_sdk.telephony.callqueue.CallQueueApi.alternate_available_phone_numbers>`
  * :meth:`api.telephony.callqueue.call_forward_available_phone_numbers <wxc_sdk.telephony.callqueue.CallQueueApi.call_forward_available_phone_numbers>`
  * :meth:`api.telephony.callqueue.primary_available_phone_numbers <wxc_sdk.telephony.callqueue.CallQueueApi.primary_available_phone_numbers>`
  * :meth:`api.telephony.huntgroup.alternate_available_phone_numbers <wxc_sdk.telephony.huntgroup.HuntGroupApi.alternate_available_phone_numbers>`
  * :meth:`api.telephony.huntgroup.forward_available_phone_numbers <wxc_sdk.telephony.huntgroup.HuntGroupApi.forward_available_phone_numbers>`
  * :meth:`api.telephony.huntgroup.primary_available_phone_numbers <wxc_sdk.telephony.huntgroup.HuntGroupApi.primary_available_phone_numbers>`
  * :meth:`api.telephony.location.call_intercept_available_phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.call_intercept_available_phone_numbers>`
  * :meth:`api.telephony.location.ecbn_available_phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.ecbn_available_phone_numbers>`
  * :meth:`api.telephony.location.phone_numbers_available_for_external_caller_id <wxc_sdk.telephony.location.TelephonyLocationApi.phone_numbers_available_for_external_caller_id>`
  * :meth:`api.telephony.location.phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.phone_numbers>`
  * :meth:`api.telephony.location.webex_go_available_phone_numbers <wxc_sdk.telephony.location.TelephonyLocationApi.webex_go_available_phone_numbers>`
  * :meth:`api.telephony.paging.primary_available_phone_numbers <wxc_sdk.telephony.paging.PagingApi.primary_available_phone_numbers>`
  * :meth:`api.telephony.voicemail_groups.available_phone_numbers <wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.available_phone_numbers>`
  * :meth:`api.telephony.voicemail_groups.fax_message_available_phone_numbers <wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi.fax_message_available_phone_numbers>`
  * :meth:`api.telephony.voiceportal.available_phone_numbers <wxc_sdk.telephony.voiceportal.VoicePortalApi.available_phone_numbers>`
- new endpoint: :meth:`api.telephony.callqueue.available_agents <wxc_sdk.telephony.callqueue.CallQueueApi.available_agents>`
- new API: :attr:`api.telephony.ms_teams <wxc_sdk.telephony.TelephonyApi.ms_teams>`
- new parameter subscription_id for :meth:`api.telephony.location.number.add <wxc_sdk.telephony.location.numbers.LocationNumbersApi.add>`
- break: parameter name supervisor_id changed to supervisor_ids for :meth:`api.telephony.supervisors.delete_bulk <wxc_sdk.telephony.supervisor.SupervisorApi.delete_bulk>`
- feat: support for hunt group busy status

    New attributes:

        * :attr:`HGCallPolicies.group_busy_enabled <wxc_sdk.telephony.huntgroup.HGCallPolicies.group_busy_enabled>`
        * :attr:`HGCallPolicies.allow_members_to_control_group_busy_enabled <wxc_sdk.telephony.huntgroup.HGCallPolicies.allow_members_to_control_group_busy_enabled>`
        * :attr:`HGCallPolicies.busy_redirect <wxc_sdk.telephony.huntgroup.HGCallPolicies.busy_redirect>`
        * :attr:`HGCallPolicies.business_continuity_redirect <wxc_sdk.telephony.huntgroup.HGCallPolicies.business_continuity_redirect>`

    Deprecated:

        * :attr:`HGCallPolicies.business_continuity <wxc_sdk.telephony.huntgroup.HGCallPolicies.business_continuity>`
- feat: location PSTN settings API: :attr:`api.telephony.pstn <wxc_sdk.telephony.TelephonyApi.pstn>`
- feat: new API, organisation level emergency settings :attr:`api.telephony.emergency_services <wxc_sdk.telephony.TelephonyApi.emergency_services>`
- feat: new API, location level emergency settings :attr:`api.telephony.location.emergency_services <wxc_sdk.telephony.location.TelephonyLocationApi.emergency_services>`
- feat: new API, user ECBN settings :attr:`api.person_settings.ecbn <wxc_sdk.person_settings.PersonSettingsApi.ecbn>`
- feat: new API, virtual line ECBN settings :attr:`api.telephony.virtual_lines.ecbn <wxc_sdk.telephony.virtual_line.VirtualLinesApi.ecbn>`
- feat: new API, workspace ECBN settings :attr:`api.workspace_settings.ecbn <wxc_sdk.workspace_settings.WorkspaceSettingsApi.ecbn>`
- feat: new methods:

   * :meth:`api.telephony.locations.read_ecbn <wxc_sdk.telephony.location.TelephonyLocationApi.read_ecbn>`
   * :meth:`api.telephony.locations.update_ecbn <wxc_sdk.telephony.location.TelephonyLocationApi.update_ecbn>`
- break: parameter person_id changed to entity_id for:

   * :meth:`api.person_settings.monitoring.configure <wxc_sdk.person_settings.monitoring.MonitoringApi.configure>`
   * :meth:`api.person_settings.monitoring.read <wxc_sdk.person_settings.monitoring.MonitoringApi.read>`
   * :meth:`api.workspace_settings.monitoring.configure <wxc_sdk.person_settings.monitoring.MonitoringApi.configure>`
   * :meth:`api.workspace_settings.monitoring.read <wxc_sdk.person_settings.monitoring.MonitoringApi.read>`
- feat: new parameter service_number in :meth:`api.telephony.phone_numbers <wxc_sdk.telephony.TelephonyApi.phone_numbers>`
- feat: new method :meth:`api.workspace_settings.numbers.update <wxc_sdk.workspace_settings.numbers.WorkspaceNumbersApi.update>`
- feat: full coverage for all device call settings endpoints

    new endpoints:

       * :meth:`api.person_settings.modify_hoteling_settings_primary_devices <wxc_sdk.person_settings.PersonSettingsApi.modify_hoteling_settings_primary_devices>`
       * :meth:`api.telephony.dect_devices.device_type_list <wxc_sdk.telephony.dect_devices.DECTDevicesApi.device_type_list>`, deprecated api.telephony.devices.dect_devices
       * :meth:`api.telephony.devices.update_third_party_device <wxc_sdk.telephony.devices.TelephonyDevicesApi.update_third_party_device>`
       * :meth:`api.telephony.devices.user_devices_count <wxc_sdk.telephony.devices.TelephonyDevicesApi.user_devices_count>`

    signature change:

       * :meth:`api.telephony.devices.preview_apply_line_key_template <wxc_sdk.telephony.devices.TelephonyDevicesApi.preview_apply_line_key_template>`
- feat: organization MoH settings

   * :meth:`api.telephony.read_moh <wxc_sdk.telephony.TelephonyApi.read_moh>`
        Get the organization Music on Hold configuration
   * :meth:`api.telephony.update_moh <wxc_sdk.telephony.TelephonyApi.update_moh>`
        Update the organization Music on Hold configuration


1.21.1
------
- fix: correct endpoint URL for :meth:`api.person_settings.voicemail.reset_pin <wxc_sdk.person_settings.voicemail.VoicemailApi.reset_pin>`

1.21.0
------
- feat: manage device background images

  * :meth:`api.telephony.devices.list_background_images <wxc_sdk.telephony.devices.TelephonyDevicesApi.list_background_images>`
  * :meth:`api.telephony.devices.upload_background_image <wxc_sdk.telephony.devices.TelephonyDevicesApi.upload_background_image>`
  * :meth:`api.telephony.devices.delete_background_images <wxc_sdk.telephony.devices.TelephonyDevicesApi.delete_background_images>`

- feat: new :meth:`api.converged_recordings.reassign <wxc_sdk.converged_recordings.ConvergedRecordingsApi.reassign>`
- feat: org level call queue settings

    * :meth:`api.telephony.callqueue.get_call_queue_settings <wxc_sdk.telephony.callqueue.CallQueueApi.get_call_queue_settings>`
    * :meth:`api.telephony.callqueue.update_call_queue_settings <wxc_sdk.telephony.callqueue.CallQueueApi.update_call_queue_settings>`
- fix: call queue API missing from method reference
- feat: new API: :attr:`api.telephony.api.telephony.supervisors <wxc_sdk.telephony.TelephonyApi.supervisors>`
- break: in line with the breaking change `announced on April 2nd, 2024 <https://developer.webex.com/docs/api/changelog>`_ signature and implementation of :class:`api.person_settings.agent_caller_id <wxc_sdk.person_settings.agent_caller_id.AgentCallerIdApi>` changed.
- feat: agent caller id API for virtual lines :attr:`api.telephony.virtual_lines.agent_caller_id <wxc_sdk.telephony.virtual_line.VirtualLinesApi.agent_caller_id>`
- feat: voicemail API for virtual lines :attr:`api.telephony.virtual_lines.voicemail <wxc_sdk.telephony.virtual_line.VirtualLinesApi.voicemail>`
- feat: MoH settings API for users :attr:`api.telephony.person_settings.music_on_hold <wxc_sdk.person_settings.PersonSettingsApi.music_on_hold>`
- feat: MoH API for virtual lines :attr:`api.telephony.virtual_lines.music_on_hold <wxc_sdk.telephony.virtual_line.VirtualLinesApi.music_on_hold>`
- break: consistently use entity_id instead of person_id in privacy API
- feat: privacy API for virtual lines: :attr:`api.telephony.virtual_lines.privacy <wxc_sdk.telephony.virtual_line.VirtualLinesApi.privacy>`
- feat: privacy API for workspaces: :attr:`api.workspace_settings.privacy <wxc_sdk.workspace_settings.WorkspaceSettingsApi.privacy>`
- feat: barge API for workspaces: :attr:`api.workspace_settings.barge <wxc_sdk.workspace_settings.WorkspaceSettingsApi.barge>`
- feat: new :meth:`api.workspace_settings.devices.list_and_counts <wxc_sdk.workspace_settings.devices.WorkspaceDevicesApi.list_and_counts>`
- feat: barge API for virtual lines: :attr:`api.telephony.virtual_lines.barge <wxc_sdk.telephony.virtual_line.VirtualLinesApi.barge>`
- break: consistently use entity_id instead of person_id in push to talk API

  * :meth:`api.person_settings.push_to_talk.configure <wxc_sdk.person_settings.push_to_talk.PushToTalkApi.configure>`
  * :meth:`api.person_settings.push_to_talk.read <wxc_sdk.person_settings.push_to_talk.PushToTalkApi.read>`
- feat: push to talk API for virtual lines: :attr:`api.telephony.virtual_lines.push_to_talk <wxc_sdk.telephony.virtual_line.VirtualLinesApi.push_to_talk>`
- feat: available numbers API for users: :attr:`api.person_settings.available_numbers <wxc_sdk.person_settings.PersonSettingsApi.available_numbers>`
- feat: available numbers API for virtual lines: :attr:`api.telephony.virtual_lines.available_numbers <wxc_sdk.telephony.virtual_line.VirtualLinesApi.available_numbers>`
- feat: available numbers API for workspaces: :attr:`api.workspace_settings.available_numbers <wxc_sdk.workspace_settings.WorkspaceSettingsApi.available_numbers>`
- feat: Webex app shared line API for users: :attr:`api.person_settings.app_shared_line <wxc_sdk.person_settings.PersonSettingsApi.app_shared_line>`
- feat: MS Teams settings API for users: :attr:`api.person_settings.ms_teams <wxc_sdk.person_settings.PersonSettingsApi.ms_teams>`
- feat: move users jobs API: :attr:`api.telephony.jobs.move_users <wxc_sdk.telephony.jobs.JobsApi.move_users>`
- feat: MoH settings API for workspaces: :attr:`api.workspace_settings.music_on_hold <wxc_sdk.workspace_settings.WorkspaceSettingsApi.music_on_hold>`
- feat: anonymous calls rejection API for workspaces: :attr:`api.workspace_settings.anon_calls <wxc_sdk.workspace_settings.WorkspaceSettingsApi.anon_calls>`
- feat: do not disturb API for workspaces: :attr:`api.workspace_settings.dnd <wxc_sdk.workspace_settings.WorkspaceSettingsApi.dnd>`
- feat: push to talk API for workspaces: :attr:`api.workspace_settings.push_to_talk <wxc_sdk.workspace_settings.WorkspaceSettingsApi.push_to_talk>`
- feat: voicemail settings API for workspaces: :attr:`api.workspace_settings.voicemail <wxc_sdk.workspace_settings.WorkspaceSettingsApi.voicemail>`
- feat: sequential ring settings API for workspaces: :attr:`api.workspace_settings.sequential_ring <wxc_sdk.workspace_settings.WorkspaceSettingsApi.sequential_ring>`
- feat: call policy settings API for workspaces: :attr:`api.workspace_settings.call_policy <wxc_sdk.workspace_settings.WorkspaceSettingsApi.call_policy>`
- feat: simultaneous ring settings API for workspaces: :attr:`api.workspace_settings.sim_ring <wxc_sdk.workspace_settings.WorkspaceSettingsApi.sim_ring>`
- feat: selective reject settings API for workspaces: :attr:`api.workspace_settings.selective_reject <wxc_sdk.workspace_settings.WorkspaceSettingsApi.selective_reject>`
- feat: selective accept settings API for workspaces: :attr:`api.workspace_settings.selective_accept <wxc_sdk.workspace_settings.WorkspaceSettingsApi.selective_accept>`
- feat: priority alert settings API for workspaces: :attr:`api.workspace_settings.priority_alert <wxc_sdk.workspace_settings.WorkspaceSettingsApi.priority_alert>`
- feat: selective forward settings API for workspaces: :attr:`api.workspace_settings.selective_forward <wxc_sdk.workspace_settings.WorkspaceSettingsApi.selective_forward>`
- fix: Paging.routing_prefix instead of .routingPrefix
- feat: new attribute AutoTransferNumbers.use_custom_transfer_numbers
- feat: new attribute CallRecordingSetting.call_recording_access_settings
- fix: correct endpoint URL for :meth:`api.person_settings.voicemail.modify_passcode <wxc_sdk.person_settings.voicemail.VoicemailApi.modify_passcode>`
- feat new CDR fields :attr:`pstn_vendor_name <wxc_sdk.cdr.CDR.pstn_vendor_name>`, :attr:`pstn_legal_entity <wxc_sdk.cdr.CDR.pstn_legal_entity>`, :attr:`pstn_vendor_org_id <wxc_sdk.cdr.CDR.pstn_vendor_org_id>`, :attr:`pstn_provider_id <wxc_sdk.cdr.CDR.pstn_provider_id>`
- feat: improved CDR data handling: unset fields are now always deserialized to None values
- feat: ZIP support for :meth:`api.reports.download <wxc_sdk.reports.ReportsApi.download>`


1.20.0
------
- feat: new attribute :attr:`Privacy.enable_phone_status_pickup_barge_in_privacy  <wxc_sdk.person_settings.privacy.Privacy>`
- feat: new API :attr:`api.telephony.jobs.update_routing_prefix <wxc_sdk.telephony.jobs.JobsApi.update_routing_prefix>`
- feat: :meth:`api.telephony.locations.update <wxc_sdk.telephony.location.TelephonyLocationApi.update>` now returns job id of update routing prefix job (if present)
- feat: new API :attr:`api.scim.groups <wxc_sdk.scim.ScimV2Api.groups>`
- feat: convergedRecordings support for webhooks
- feat: new API :attr:`api.converged_recordings <wxc_sdk.WebexSimpleApi.converged_recordings>`
- feat: new API :attr:`api.telephony.organisation_access_codes <wxc_sdk.telephony.TelephonyApi.organisation_access_codes>`
- feat: new API translation patterns :attr:`api.telephony.call_routing.tp <wxc_sdk.telephony.call_routing.CallRoutingApi.tp>`
- feat: enhanced response for :meth:`api.telephony.test_call_routing <wxc_sdk.telephony.TelephonyApi.test_call_routing>` controlled by include_applied_services parameter
- feat: new endpoint :meth:`api.telephony.calls.mute <wxc_sdk.telephony.calls.CallsApi.mute>`
- feat: new endpoint :meth:`api.telephony.calls.unmute <wxc_sdk.telephony.calls.CallsApi.unmute>`
- feat: added delete_all_numbers parameter to :meth:`api.telephony.prem_pstn.route_list.update_numbers <wxc_sdk.telephony.prem_pstn.route_list.RouteListApi.update_numbers>`
- feat: new API :attr:`api.telephony.conference <wxc_sdk.telephony.TelephonyApi.conference>`
- feat: new API :attr:`api.telephony.playlist <wxc_sdk.telephony.TelephonyApi.playlist>`
- feat: support for playlist in :meth:`api.telephony.location.moh.read <wxc_sdk.telephony.location.moh.LocationMoHApi.read>` and :meth:`api.telephony.location.moh.update <wxc_sdk.telephony.location.moh.LocationMoHApi.update>`
- feat: new API :attr:`api.roles <wxc_sdk.WebexSimpleApi.roles>`

1.19.0
------
- feat: DECT devices with additional operations: :class:`wxc_sdk.telephony.dect_devices.DECTDevicesApi`

  * :meth:`list_dect_networks <wxc_sdk.telephony.dect_devices.DECTDevicesApi.list_dect_networks>`
  * :meth:`dect_network_details <wxc_sdk.telephony.dect_devices.DECTDevicesApi.dect_network_details>`
  * :meth:`update_dect_network <wxc_sdk.telephony.dect_devices.DECTDevicesApi.update_dect_network>`
  * :meth:`update_dect_network_settings <wxc_sdk.telephony.dect_devices.DECTDevicesApi.update_dect_network_settings>`
  * :meth:`delete_dect_network <wxc_sdk.telephony.dect_devices.DECTDevicesApi.delete_dect_network>`
  * :meth:`list_base_stations <wxc_sdk.telephony.dect_devices.DECTDevicesApi.list_base_stations>`
  * :meth:`base_station_details <wxc_sdk.telephony.dect_devices.DECTDevicesApi.base_station_details>`
  * :meth:`delete_bulk_base_stations <wxc_sdk.telephony.dect_devices.DECTDevicesApi.delete_bulk_base_stations>`
  * :meth:`delete_base_station <wxc_sdk.telephony.dect_devices.DECTDevicesApi.delete_base_station>`
  * :meth:`list_handsets <wxc_sdk.telephony.dect_devices.DECTDevicesApi.list_handsets>`
  * :meth:`handset_details <wxc_sdk.telephony.dect_devices.DECTDevicesApi.handset_details>`
  * :meth:`update_handset <wxc_sdk.telephony.dect_devices.DECTDevicesApi.update_handset>`
  * :meth:`delete_handset <wxc_sdk.telephony.dect_devices.DECTDevicesApi.delete_handset>`
  * :meth:`delete_handsets <wxc_sdk.telephony.dect_devices.DECTDevicesApi.delete_handsets>`
  * :meth:`dect_networks_associated_with_person <wxc_sdk.telephony.dect_devices.DECTDevicesApi.dect_networks_associated_with_person>`
  * :meth:`dect_networks_associated_with_workspace <wxc_sdk.telephony.dect_devices.DECTDevicesApi.dect_networks_associated_with_workspace>`
  * :meth:`dect_networks_associated_with_virtual_line <wxc_sdk.telephony.dect_devices.DECTDevicesApi.dect_networks_associated_with_virtual_line>`

- fix: :meth:`create_base_stations <wxc_sdk.telephony.dect_devices.DECTDevicesApi.create_base_stations>`, wrong endpoint
  and result attribute
- fix: typo in :class:`wxc_sdk.person_settings.calling_behavior.BehaviorType`. native_sip_call_zo_ucm instead of native_sip_call_to_ucm

- feat: new attribute :attr:`wxc_sdk.devices.Device.device_platform`
- feat: new :meth:`api.telephony.devices.details <wxc_sdk.telephony.devices.TelephonyDevicesApi.details>`
- feat: new :meth:`api.telephony.devices.get_device_layout <wxc_sdk.telephony.devices.TelephonyDevicesApi.get_device_layout>`
- feat: new :meth:`api.telephony.devices.get_person_device_settings <wxc_sdk.telephony.devices.TelephonyDevicesApi.get_person_device_settings>`
- feat: new :meth:`api.telephony.devices.get_workspace_device_settings <wxc_sdk.telephony.devices.TelephonyDevicesApi.get_workspace_device_settings>`
- feat: new :meth:`api.telephony.devices.modify_device_layout <wxc_sdk.telephony.devices.TelephonyDevicesApi.modify_device_layout>`
- feat: new :meth:`api.telephony.devices.update_person_device_settings <wxc_sdk.telephony.devices.TelephonyDevicesApi.update_person_device_settings>`
- feat: new :meth:`api.telephony.devices.update_workspace_device_settings <wxc_sdk.telephony.devices.TelephonyDevicesApi.update_workspace_device_settings>`
- feat: new API :attr:`api.telephony.jobs.rebuild_phones <wxc_sdk.telephony.jobs.RebuildPhonesJobsApi>`
- break: unify methods of job APIs to list(), status(), errors()
- break: different return type for :meth:`api.telephony.supported_devices <wxc_sdk.telephony.TelephonyApi.supported_devices>`
- fix: corrected enum values in :class:`wxc_sdk.telephony.ServiceType`
- feat: new event types in :class:`wxc_sdk.webhook.WebhookEventType`
- feat: new parameter number_type for :meth:`api.telephony.location.number.add <wxc_sdk.telephony.location.numbers.LocationNumbersApi.add>`
- feat: new attribute :attr:`wxc_sdk.workspaces.Workspace.indoor_navigation`
- feat: added latitude, longitude, and notes parameter to :meth:`api.locations.create <wxc_sdk.locations.LocationsApi.create>`
- feat: workspace personalization API: :attr:`api.workspace_personalization <wxc_sdk.WebexSimpleApi.workspace_personalization>`

1.18.0
------
- feat: virtual line settings: call intercept, call recording, call waiting, forwarding, incoming/outgoing call permissions, directory search, DECT networks, :class:`wxc_sdk.telephony.virtual_line.VirtualLinesApi`
- feat: call recording settings API: :class:`wxc_sdk.telephony.call_recording.CallRecordingSettingsApi`
- feat: new event type "businessTexts"
- feat: :class:`wxc_sdk.licenses.License` attributes: consumed_by_users, consumed_by_workspaces
- feat: :meth:`wxc_sdk.person_settings.voicemail.VoicemailApi.modify_passcode` to set voicemail passcode for users
- feat: guests API :attr:`wxc_sdk.WebexSimpleApi.guests`
- feat: call pickup notifications
- fix: errors when creating call pickups w/ agents
- feat: status API :attr:`wxc_sdk.WebexSimpleApi.status`
- feat: improved format for :doc:`method reference <method_ref>`
- feat: admin audit events API :attr:`wxc_sdk.WebexSimpleApi.admin_audit`
- fix: unresolved references in as_api.py
- feat: consistent implementation of outgoing calling permissions for locations, users, workspaces, and virtual lines
- feat: digit patterns APi in outgoing calling permissions for locations, users, workspaces, and virtual lines, :attr:`wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.digit_patterns`.
- feat: first (experimental, rudimentary) shot at SCIMv2 users API :attr:`wxc_sdk.scim.users.SCIM2UsersApi`, only implemented :meth:`wxc_sdk.scim.users.SCIM2UsersApi.details` and :meth:`wxc_sdk.scim.users.SCIM2UsersApi.search`
- feat: :meth:`wxc_sdk.scim.users.SCIM2UsersApi.search_all`, :meth:`wxc_sdk.scim.users.SCIM2UsersApi.update`, :meth:`wxc_sdk.scim.users.SCIM2UsersApi.patch`, :meth:`wxc_sdk.scim.users.SCIM2UsersApi.delete`
- feat: SCIMv2 bulk API :attr:`wxc_sdk.scim.bulk.SCIM2BulkApi`
- break: removing AccessCodesApi from TelephonyApi. Lives now under permissions_out
- break: consistently use entity_id instead of person_id/workspace_id in outgoing permissions API
- break: consistently use entity_id instead of person_id/workspace_id in forwarding API
- break: consistently use entity_id instead of person_id/workspace_id in caller id API
- break: consistently use entity_id instead of person_id/workspace_id in call waiting API
- break: consistently use entity_id instead of person_id/workspace_id in incoming permissions API
- break: consistently use entity_id instead of person_id/workspace_id in call intercept API
- break: consistently use entity_id instead of person_id/workspace_id in call recording API
- fix: need to bring back access codes API for locations under TelephonyAPI due to different signatures of create() method
- feat: call bridge settings for users, workspaces, virtual lines
- fix: parameter line2_member_id in :meth:`wxc_sdk.telephony.dect_devices.DECTDevicesApi.add_a_handset` has to be
  optional. To not break existing parameter order parameter custom_display_name had to be made optional as well although it actually is mandatory
- fix: :meth:`wxc_sdk.person_settings.callbridge.CallBridgeApi.read` now returns :class:`wxc_sdk.person_settings.callbridge.CallBridgeSetting` instead of bool
- fix: wrong type for :attr:`wxc_sdk.scim.users.WebexUser.user_settings`

1.17.1
------
- fix: :meth:`wxc_sdk.authorizations.AuthorizationsApi.delete`, corrected parameter handling

1.17.0
------
- feat: device configurations API :attr:`wxc_sdk.WebexSimpleApi.device_configurations`
- fix: :meth:`wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi.update`: used POST instead of PUT
- fix: :meth:`wxc_sdk.telephony.calls.CallsApi.answer` has new `endpoint_id` endpoint parameter
- fix: allow additional phone number types (enterprise, alternate1, alternate2), :class:`wxc_sdk.people.PhoneNumberType`
- Fix: added some attributes based on unittest results :attr:`wxc_sdk.common.MppCustomization.allow_monitor_lines_enabled`, :attr:`wxc_sdk.events.EventData.title_encryption_key_url`, :attr:`wxc_sdk.telephony.location.TelephonyLocation.enforce_outbound_dial_digit`
- feat: new example: room_devices.py
- feat: new parameter "mac" for ":meth:`wxc_sdk.devices.DevicesApi.list`
- feat: field_validator for :attr:`wxc_sdk.devices.Device.mac` to remove colons; enforce consistent MAC address format for mpp and roomdesk devices.
- feat: new API :attr:`wxc_sdk.WebexSimpleApi.authorizations`
- feat: new CDR fields: :attr:`wxc_sdk.cdr.CDR.ring_duration`, :attr:`wxc_sdk.cdr.CDR.release_time`, :attr:`wxc_sdk.cdr.CDR.answer_indicator`, :attr:`wxc_sdk.cdr.CDR.final_local_session_id`, :attr:`wxc_sdk.cdr.CDR.final_remote_session_id`
- feat: new :meth:`wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.usage_call_to_extension`
- fix: corrected handling of Union[datetime, str] in :meth:`wxc_sdk.cdr.DetailedCDRApi.get_cdr_history`
- feat: support for ESNs
- feat: call queue with departments
- feat: call recordings API
- fix: attribute :attr:`wxc_sdk.telephony.location.TelephonyLocation.enforce_outside_dial_digit`
- feat: new :meth:`wxc_sdk.telephony.devices.TelephonyDevicesApi.create_line_key_template`, :meth:`wxc_sdk.telephony.devices.TelephonyDevicesApi.list_line_key_templates`, :meth:`wxc_sdk.telephony.devices.TelephonyDevicesApi.line_key_template_details`, :meth:`wxc_sdk.telephony.devices.TelephonyDevicesApi.modify_line_key_template`, :meth:`wxc_sdk.telephony.devices.TelephonyDevicesApi.delete_line_key_template`, :meth:`wxc_sdk.telephony.devices.TelephonyDevicesApi.preview_apply_line_key_template`
- feat: improved :meth:wxc_sdk.devices.DevicesApi.list`, use enum parameters
- fix: :attr:`wxc_sdk.telephony.callqueue.CallQueue.department`, optional
- fix: :class:`wxc_sdk.common.OwnerType` needs to support PAGING_GROUP and GROUP_PAGING (inconsistent)
- fix: undocumented attribute :attr:`wxc_sdk.telephone.voicemail_groups.VoicemailGroupDetail.time_zone`
- feat: new API :attr:`wxc_sdk.telephony.jobs.JobsApi.apply_line_key_templates`
- feat: improved handling of floor actions in TelephonyApi
- feat: deprecation warnings for create/update on workspace locations
- feat: new :meth:`wxc_sdk.licenses.LicensesApi.assigned_users`, :meth:`wxc_sdk.licenses.LicensesApi.assign_licenses_to_users`
- feat: new :attr:`wxc_sdk.workspaces.Workspace.location_id`
- feat: call record events :class:`wxc_sdk.events.EventResource`, :class:`wxc_sdk.events.EventData`
- feat: new API: :class:`wxc_sdk.telephony.dect_devices.DECTDevicesApi`

1.16.1
------
- leftovers from pydantic v2 transition
- new type: :class:`wxc_sdk.devices.ConnectionStatus` for :attr:`wxc_sdk.devices.Device.connection_status`

1.16.0
------
- upgrading to pydantic v2, see: https://docs.pydantic.dev/latest/migration/
- feat: preferred answer device settings for calling users :attr:`wxc_sdk.person_settings.PersonSettingsApi.preferred_answer`
- fix: various updated data types
- fix: direct transformation of multi word attribute names in CDRs to snake_case to make sure that additional attributes not defined in CDR show up as snake_case
- feat: support for organizations with XSI
- feat: additional CDR attributes

1.15.0
------

- fix: missing org_id parameters in devices api
- feat: password parameter in :meth:`wxc_sdk.devices.DevicesApi.create_by_mac_address`
- feat: new methods in :class:`wxc_sdk.locations.LocationsApi`: list_floors, create_floor, floor_details, update_floor, delete_floor
- feat: support for virtual extension ranges in result of :meth:`wxc_sdk.telephony.TelephonyApi.test_call_routing`
- feat: new parameter prefer_e164_format in :meth:`wxc_sdk.person_settings_numbers.NumbersApi.read`
- fix: new :attr:`wxc_sdk.devices.Device.workspace_location_id`
- fix: changes in CDR fields based on tests
- new: :attr:`wxc_sdk.events.EventData.title`
- fix: camelCase issues for timezone when creating a location (temp fix): :meth:`wxc_sdk.locations.LocationsApi.create`
- new: :attr:`wxc_sdk.person_settings.TelephonyDevice.hoteling`. Moved :class:`wxc_sdk.person_settings.Hoteling`,
- fix: got rid of class WorkspaceDevice, use :class:`wxc_sdk.person_settings.TelephonyDevice` instead
- feat: improved details in :class:`wxc_sdk.as_rest.AsRestError`
- fix: camelCase issues for timezone when updating a location (temp fix): :meth:`wxc_sdk.locations.LocationsApi.update`
- feat: new example catch_tns.py
- feat: better handling of CDRs in :class:`wxc_sdk.cdr.CDR` to allow deserialization of addtl. fields
- feat: new parameter ´retry_429' for :class:`wxc_sdk.WebexSimpleApi` and :class:`wxc_sdk.as_api.AsWebexSimpleApi`
- fix: missing :class:`wxc_sdk.locations.CreateLocationFloorBody` in __all__
- feat: new parameter 'html' in :meth:`wxc_sdk.messages.MessagesApi.create` and :meth:`wxc_sdk.messages.MessagesApi.edit`
- fix: workspace outgoing permissions auth codes are now called access codes. Updates to
  :class:`wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi`: renamed API attribute to
  :attr:`wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.access_codes` and updated endpoint URL in
  :class:`wxc_sdk.person_settings.permissions_out.AccessCodesApi`
- fix: better handling of start_time and end_time parameters in :meth:`wxc_sdk.cdr.DetailedCDRApi.get_cdr_history`.
  Instead of datetime objects the call also accepts ISO-8601 datetime strings.
- feat: announcement repository. New API to manage announcements:
  :class:`wxc_sdk.telephony.announcements_repo.AnnouncementsRepositoryApi` available in the telephony.announcements_repo
  path of :class:`wxc_sdk.WebexSimpleApi`
- feat: announcements from repository can now be referenced for: location MoH, call queue, auto attendant menus

1.14.1
------
- update dependencies to avoid typing-extensions 4.6.0 which breaks Literals in Pydantic models

1.14.0
------
- fix: call forwarding for auto attendants, call queues, hunt groups: rules attribute optional in updates.
  Forwarding rule creation, update, and deletion was broken
- feat: unit tests for call queue forwarding and selective forwarding rule creation and deletion
- fix: missing return type for :meth:`wxc_sdk.workspace_locations.WorkspaceLocationApi.update`
- fix: make parameter location_id optional in :meth:`wxc_sdk.telephony.devices.TelephonyDevicesApi.available_members`
- fix: include line label attributes in updates: :meth:`wxc_sdk.telephony.devices.TelephonyDevicesApi.update_members`
- feat: optional org_id parameter in :meth:`wxc_sdk.devices.DevicesApi.activation_code`
- feat: optional org_id parameter in :meth:`wxc_sdk.devices.DevicesApi.create_by_mac_address`
- fix: bump requests-toolbelt version for urllib3 2.0 compatibility

1.13.0
------
- new API for virtual lines :class:`wxc_sdk.telephony.virtual_line.VirtualLinesApi`
- new API: :class:`wxc_sdk.meetings.MeetingsApi`. Experimental: not unit tested, 100% auto generated
- fix: proper enum handling for type parameter in :meth:`wxc_sdk.rooms.RoomsApi.list`
- feat: new parameter initiate_flow_callback for :class:`wxc_sdk.integration.Integration`
- fix: state and postal_code are optional in :class:`wxc_sdk.locations.LocationAddress`. They are mandatory in calling locations are not required in workspace locations which now are returned by :meth:`wxc_sdk.locations.LocationsApi.list` as well.
- feat: devices API now supports MPPs: :class:`wxc_sdk.devices.DevicesApi`
- feat: unified locations and workspace locations: :class:`wxc_sdk.workspaces.WorkspacesApi`
- feat: new :meth:`wxc_sdk.telephony.location.TelephonyLocationApi.enable_for_calling`
- feat: new :meth:`wxc_sdk.telephony.location.TelephonyLocationApi.list`
- feat: new API :class:`wxc_sdk.workspace_settings.devices.WorkspaceDevicesApi`

1.12.0
------
- feat: new attribute call_park_extension in :class:`wxc_sdk.telephony.callpark.CallPark`
- feat: new parameters details, restricted_non_geo_numbers for :meth:`wxc_sdk.telephony.TelephonyApi.phone_numbers`
- feat: new Api :class:`wxc_sdk.telephony.location.receptionist_contacts.ReceptionistContactsDirectoryApi`
- fix: correct support for enum URL params in :meth:`wxc_sdk.workspaces.WorkspacesApi.list`
- feat: new attribute :attr:`wxc_sdk.telephony.autoattendant.AutoAttendantMenu.audio_file`

1.11.0
------
- feat: new example queue_helper.py
- feat: new attributes in :class:`wxc_sdk.cdr.CDR`
- fix: additional_primary_line_appearances_enabled and basic_emergency_nomadic_enabled optional in :class:`wxc_sdk.telephony.SupportedDevice`
- feat: manage numbers jobs api :attr:`wxc_sdk.telephony.jobs.JobsApi.manage_numbers`
- fix: new attribute 'browser_client_id' in :class:`wxc_sdk.person_settings.appservices.AppServicesSettings`
- fix: :class:`wxc_sdk.telephony.jobs.ManageNumbersJobsApi`, updated method names, fixed type issues in list method
- fix: set location_id in response from :meth:`wxc_sdk.telephony.callqueue.CallQueueApi.details`
- fix: check presence of location_id and queue_id in :meth:`wxc_sdk.telephony.callqueue.CallQueueApi.update`
- feat: class to parse webhook event data :class:`wxc_sdk.webhook.WebhookEvent`, :class:`wxc_sdk.webhook.WebhookEventData`
- feat: new API :attr:`wxc_sdk.attachment_actions`
- feat: new example: firehose.py, create a "firehose" webhook (using ngrok) to dump webhook events to console
- fix: consistent non-camelcase "Webhook" instead of mixed "Webhook" and "WebHook" usage
  BREAKING CHANGE: renamed classes WebHook, WebHookEvent, WebHookEventType, WebHookResource, WebHookStatus
- feat: new enums :class:`wxc_sdk.telephony.OwnerType`: CALL_QUEUE, VIRTUAL_LINE

1.10.1
------
- fix: missing requirement: pyyaml

1.10.0
------
- fix: wxc_sdk.workspaces.Workspace.hotdesking_enabled is now :attr:`wxc_sdk.workspaces.Workspace.hotdesking_status` (on/off)
- fix: wrong url in :meth:`wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.delete`
- fix: docstring fixed for :meth:`wxc_sdk.telephony.callqueue.policies.CQPolicyApi.holiday_service_details`
- feat: new parameter force_new for :meth:`wxc_sdk.integration.Integration.get_cached_tokens`
- feat: new :meth:`wxc_sdk.integration.Integration.get_cached_tokens_from_yml`
- feat: new parameters org_public_spaces, from, to for :meth:`wxc_sdk.rooms.RoomsApi.list`
- feat: new parameters is_public, description for :meth:`wxc_sdk.rooms.RoomsApi.create`
- feat: new attributes made_public, description for :class:`wxc_sdk.rooms.Room`
- fix: fixed method names in :class:`wxc_sdk.team_memberships.TeamMembershipsApi`
- feat: new example: archive_space.py
- feat: SafeEnum instead of Enum to tolerate unknown enum values
- fix: use_enum_values = True in ApiModel so that enum values are not stored as Enum instances;
  CAUTION: might break code that uses .name and .value attributes of enums.
- feat: new API: :attr:`wxc_sdk.telephony.TelephonyApi.voice_messaging`

1.9.0
-----
- feat: new API: :attr:`wxc_sdk.WebexSimpleApi.teams`
- feat: new API: :attr:`wxc_sdk.WebexSimpleApi.team_memberships`
- feat: new API: :attr:`wxc_sdk.WebexSimpleApi.room_tabs`
- fix: proper support for :class:`wxc_sdk.messages.MessageAttachment` in :meth:`wxc_sdk.messages.MessagesApi.create`
- feat: support local files with :meth:`wxc_sdk.messages.MessagesApi.create`
- fix: :meth:`wxc_sdk.teams.TeamsApi.list`, removed undefined "param" variable
- feat: generated async API now supports file uploads; for example posting messagen
- feat: new API: :attr:`wxc_sdk.WebexSimpleApi.events`
- improved 429 handling; not using backoff module anymore
- added :meth:`wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.create`
- added :meth:`wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.delete`
- added :meth:`wxc_sdk.telephony.callpark_extension.CallparkExtensionApi.update`
- fix: :meth:`wxc_sdk.people.PeopleApi.update` with calling_data=True failed

1.8.0
-----
- feat: new APIs: :attr:`wxc_sdk.WebexSimpleApi.rooms`
- feat: new APIs: :attr:`wxc_sdk.WebexSimpleApi.messages`
- feat: new APIs: :attr:`wxc_sdk.WebexSimpleApi.membership`
- feat: new API :attr:`wxc_sdk.WebexSimpleApi.reports`
- feat: new API :attr:`wxc_sdk.WebexSimpleApi.cdr`
- feat: new API: :attr:`wxc_sdk.telephony.TelephonyApi.jobs`
- feat: :class:`wxc_sdk.person_settings.permissions_out.CallingPermissions` allows call type permissions for arbitrary
  call_types in deserialization of API responses.
- feat: :meth:`wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.configure` supports dropping of call
  types from serialization. Default: {'url_dialing', 'unknown', 'casual'}

1.7.2
-----
- fix: call type national consistently fixed

1.7.1
-----
- fix: accidentally removed support for call type NATIONAL; re-added
- fix: listing workspace numbers only makes sense for workspaces with calling type "webex"; WXCAPIBULK-136
- fix: corrected response type for :meth:`wxc_sdk.workspace_settings.numbers.WorkspaceNumbersApi.read`
- feat: cleanup.py also deletes test dial plans

1.7.0
-----
- feat: workspace locations (and floors) API, :attr:`wxc_sdk.WebexSimpleApi.workspace_locations`
- feat: devices API, :attr:`wxc_sdk.WebexSimpleApi.devices`
- feat: new API for jobs to udpate device settings at org and location level: :attr:`wxc_sdk.devices.DevicesApi.settings_jobs`
- feat: new telephony devices API: :attr:`wxc_sdk.telephony.TelephonyApi.devices`
- feat: new telephony jobs API: :attr:`wxc_sdk.telephony.TelephonyApi.jobs`
- feat: new API to get workspace numbers: :attr:`wxc_sdk.workspace_settings.WorkspaceSettingsApi.numbers`
- feat: new API to manage agent caller id settings for users: :attr:`wxc_sdk.person_settings.PersonSettingsApi.agent_caller_id`
- feat: new method to get devices of a user: :meth:`wxc_sdk.person_settings.PersonSettingsApi.devices`
- feat: new method to get location level device settings: :meth:`wxc_sdk.telephony.location.TelephonyLocationApi.device_settings`
- feat: get supported devices: :meth:`wxc_sdk.telephony.TelephonyApi.supported_devices`
- feat: get organisation level device settings: :meth:`wxc_sdk.telephony.TelephonyApi.device_settings`
- feat: new call queue settings: :attr:`wxc_sdk.telephony.callqueue.QueueSettings.comfort_message_bypass`, :attr:`wxc_sdk.telephony.callqueue.QueueSettings.whisper_message`
- feat: new call queue policy setting to support skill based routing: :attr:`wxc_sdk.telephony.callqueue.CallQueueCallPolicies.routing_type`
- feat: new call queue agent attributes: :attr:`wxc_sdk.telephony.hg_and_cq.Agent.skill_level`, :attr:`wxc_sdk.telephony.hg_and_cq.Agent.join_enabled`
- feat: new attribute :attr:`wxc_sdk.person_settings.appservices.AppServicesSettings.desktop_client_id`
- feat: support explicit content-type for REST requests
- feat: new example call_intercept.py
- feat: DialPlan attributes name and route_name now optional to simplify instantiation for updates
- feat: example call_intercept.py, enable debug output if run in debugger
- fix: added missing return type str to :meth:`wxc_sdk.locations.LocationsApi.create`
- fix: moving change_announcement_language to :class:`wxc_sdk.telephony.location.TelephonyLocationApi`
- fix: workaround for wrong pagination urls not required any more
- fix: dumping REST messages with no valid time diff caused an exception
- fix: exclude refresh token values from REST debug
- fix: parse_scopes with None parameter raised an exception
- fix: custom_number_info removed from ExternalCallerIdNamePolicy
- fix: catch error in pagination if empty response is returned
- fix: async_gen.py, matching failed for last method in class if followed by decorated class
- fix: updated outgoing permission call types to latest call types: :class:`wxc_sdk.person_settings.permissions_out.OutgoingPermissionCallType`
- fix: proper handling of show_all_types parameter in :meth:`wxc_sdk.people.PeopleApi.update`
- fix: ignore calltypes not supported in calling permissions any more: national, casual, url_dialing, unknown

1.6.0
-----
- new API: :class:`wxc_sdk.organizations.OrganizationApi`
- updated attributes in :class:`wxc_sdk.locations.Location`
- new: details() and update() in :class:`wxc_sdk.telephony.location.TelephonyLocationApi`
- new: create() and update() in :class:`wxc_sdk.locations.LocationsApi`
- new test cases
- :meth:`wxc_sdk.telephony.prem_pstn.dial_plan.DialPlanApi.details` now always returns dialplan id
- changes to data types for results of :meth:`wxc_sdk.telephony.TelephonyApi.test_call_routing` based on learnings
  from tests
- workaround for broken poagination URLs ported to async API
- consistently allow positional parameters everywhere; still recommended to use named parameters though
- async api: improved REST error handling, allow follow_pagination w/o model (compatible to sync version)
- new: CRUD for voicemail groups in :class:`wxc_sdk.telephony.voicemail_groups.VoicemailGroupsApi`
- REST logs now contain response times
- 10D numbers returned in person caller id settings get normalized to E.164



1.5.2
-----
- deprecate broken build 1.5.1

1.5.1
-----
- :meth:`wxc_sdk.telephony.location.internal_dialing.InternalDialingApi.update`: fixed a problem with removing an
  internal dialing target (trunk or route group)
- :class:`wxc_sdk.telephony.prem_pstn.route_group.RouteGroupApi`: fixed errors handling optional parameters for
  some methods.
- :class:`wxc_sdk.telephony.prem_pstn.route_list.RouteListApi`: doc strings
- :meth:`wxc_sdk.telephony.prem_pstn.trunk.TrunkApi.list`: fixed errors handling optional parameters
- Test case for location internal dialing settings
- Test case for adding/removing numbers from route lists

1.5.0
-----
- new: location API: :attr:`wxc_sdk.telephony.TelephonyApi.location`
    - moved location intercept, location moh and location voicemail settings from telephony to location API
    - new: number API: :attr:`wxc_sdk.telephony.location.TelephonyLocationApi.number`
    - new: internal dialing API: :attr:`wxc_sdk.telephony.location.TelephonyLocationApi.internal_dialing`
- new: premises PSTN API: :attr:`wxc_sdk.telephony.TelephonyApi.prem_pstn`
    - dial plans: :attr:`wxc_sdk.telephony.prem_pstn.PremisePstnApi.dial_plan`
    - trunks: :attr:`wxc_sdk.telephony.prem_pstn.PremisePstnApi.trunk`
    - route lists: :attr:`wxc_sdk.telephony.prem_pstn.PremisePstnApi.route_list`
    - route groups: :attr:`wxc_sdk.telephony.prem_pstn.PremisePstnApi.route_group`
- new: cross reference of all methods in :doc:`Reference of all available methods <method_ref>`
- new update person numbers: :meth:`wxc_sdk.person_settings.numbers.NumbersApi.update`
- workaround to catch broken pagination URLs
- new test cases

1.4.1
-----

- new: utility function to parse scopes, :func:`wxc_sdk.scopes.parse_scopes`
- new example: us_holidays_async.py

1.4.0
-----
-   new: :meth:`wxc_sdk.integration.Integration.get_cached_tokens`
-   new: :attr:`wxc_sdk.common.schedules.Schedule.new_name` for updates
-   minor changes in unit tests

1.3.0
-----
-   missing people endpoint create()
-   new: Person.errors
-   fix: people update()
-   fix: parameter error when listing phone numbers

1.2.0
-----
-   new: push to talk person settings: :attr:`wxc_sdk.person_settings.PersonSettingsApi.push_to_talk`
-   new: location features intercept, announcement language, MoH, outgoing permissions, PNC, voicemail
    rules/settings/groups, voice portal and voice portal passcode rules: :class:`wxc_sdk.telephony.TelephonyApi`

1.1.0
-----
-   new: read only call park extensions API: :attr:`wxc_sdk.telephony.TelephonyApi.callpark_extension`
-   new: groups API: :attr:`wxc_sdk.WebexSimpleApi.groups`
-   new: experimental async API: :class:`wxc_sdk.as_api.AsWebexSimpleApi`


1.0.0
-----
-   renamed ``wxc_sdk.types`` to ``wxc_sdk.all_types`` to avoid conflicts
-   calling behavior API for users: :attr:`wxc_sdk.person_settings.PersonSettingsApi.calling_behavior`
-   new method: :meth:`wxc_sdk.telephony.TelephonyApi.phone_numbers`
-   new method: :meth:`wxc_sdk.telephony.TelephonyApi.phone_number_details`
-   new method: :meth:`wxc_sdk.telephony.TelephonyApi.validate_extensions`
-   numbers API for workspaces: :attr:`wxc_sdk.workspace_settings.WorkspaceSettingsApi.numbers`


0.7.0
-----
-   new API: workspaces settings :attr:`wxc_sdk.WebexSimpleApi.workspace_settings`
    Workspace settings are very similar to person settings. Hence the
    :class:`wxc_sdk.workspace_settings.WorkspaceSettingsApi` reuses the existing person settings sub-APIs. When calling
    any of these endpoints the ``workspace_id`` of the workspace has to be passed to the ``person_id`` parameter of
    endpoint.
-   outgoing permissions API (:class:`wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi`) enhanced to
    support outgoing permission transfer numbers
    (:attr:`wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.transfer_numbers`) and authorization codes
    (:attr:`wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi.auth_codes`). For now these sub-APIs are
    only available for workspaces and not for persons. As soon as the Webex Calling APIs start to support this
    functionally for persons the SDK will follow.

0.6.1
-----
-   implemented missing call control API endpoints in :class:`wxc_sdk.telephony.calls.CallsApi`

0.6.0
-----
-   refactoring
-   new person settings :class:`wxc_sdk.person_settings.PersonSettingsApi`

    * application services: :class:`wxc_sdk.person_settings.appservices.AppServicesApi`
    * call waiting: :class:`wxc_sdk.person_settings.call_waiting.CallWaitingApi`
    * exec assistant: :class:`wxc_sdk.person_settings.exec_assistant.ExecAssistantApi`
    * hoteling: :class:`wxc_sdk.person_settings.hoteling.HotelingApi`
    * montoring: :class:`wxc_sdk.person_settings.monitoring.MonitoringApi`
    * numbers: :class:`wxc_sdk.person_settings.numbers.NumbersApi`
    * incoming permisssions: :class:`wxc_sdk.person_settings.permissions_in.IncomingPermissionsApi`
    * outgoing permissions: :class:`wxc_sdk.person_settings.permissions_out.OutgoingPermissionsApi`
    * privacy: :class:`wxc_sdk.person_settings.privacy.PrivacyApi`
    * receptionist: :class:`wxc_sdk.person_settings.receptionist.ReceptionistApi`
    * schedules: :class:`wxc_sdk.common.schedules.ScheduleApi`

-   new api: workspaces: :class:`wxc_sdk.WebexSimpleApi`. :class:`wxc_sdk.workspaces.WorkspacesApi`
-   various new test cases

0.5.3
-----
-   fixed an issue with call park updates (agents need to be pased as list of IDs)
-   fixed an issue in forwarding API: wrong URL path handling
-   additional paging group tests

0.5.2
-----
-   consistently use update() for all objects

0.5.1
-----
-   Paging group tests
-   Call park tests
-   fixed issue w/ paging group create/update

0.5.0
-----
-   Call park API (:class:`wxc_sdk.telephony.callpark.CallParkApi`)
-   Call pickup API (:class:`wxc_sdk.telephony.callpickup.CallPickupApi`)
-   refactoring data types for call queues and hunt groups
-   improved documentation of hunt group data types
-   additional tests for call queues, hunt groups

0.4.2
-----
-   Call queue API (:class:`wxc_sdk.telephony.callqueue.CallQueueApi`)
    `test cases <https://github.com/jeokrohn/wxc_sdk/blob/master/tests/test_telephony_callqueue.py>`_ and bug fixes.
-   improved documentation

0.4.1
-----
-   all datatypes defined in any of the submodules and subpackages can now be imported directly from
    ``wxc_sdk.types``.

    Instead of importing from the respective submodule/subpackage:

    .. code-block::

       from wxc_sdk.people import Person
       from wxc_sdk.person_settings.barge import BargeSettings

    ... the datatypes can simply imported like this:

    .. code-block::

       from wxc_sdk.types import Person, BargeSettings
-   documentation updates

0.4.0
-----
-   auto attendant API added :class:`wxc_sdk.telephony.autoattendant.AutoAttendantApi`.
    Example:

    .. code-block::

        from wxc_sdk import WebexSimpleApi

        api = WebexSimpleApi()
        auto_attendants = list(api.telephony.auto_attendant.list())
-   refactoring of forwarding API (:class:`wxc_sdk.telephony.forwarding.ForwardingApi`) which is used to manage
    forwarding settings for:

    - hunt groups: :class:`wxc_sdk.telephony.huntgroup.HuntGroupApi`
    - call queues: :class:`wxc_sdk.telephony.callqueue.CallQueueApi`
    - auto attendants: :class:`wxc_sdk.telephony.autoattendant.AutoAttendantApi`

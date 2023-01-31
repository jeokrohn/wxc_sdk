Release history
===============

- feat: new attribute call_park_extension in :class:`wxc_sdk.telephony.callpark.CallPark`
- feat: new parameters details, restricted_non_geo_numbers for :meth:`wxc_sdk.telephony.TelephonyApi.phone_numbers`

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
- feat: new parameters org_public_spaces, from_, to_ for :meth:`wxc_sdk.rooms.RoomsApi.list`
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
- new: cross reference of all methods in :doc:`Reference of all available methods <./method_ref>`
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

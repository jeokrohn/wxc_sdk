Release history
===============

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

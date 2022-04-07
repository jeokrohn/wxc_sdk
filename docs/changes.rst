Release history
===============

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

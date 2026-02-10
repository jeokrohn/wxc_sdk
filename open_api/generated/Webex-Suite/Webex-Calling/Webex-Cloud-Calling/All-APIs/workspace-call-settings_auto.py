from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Action', 'AuthorizationCode', 'CLIDPolicySelection', 'CallForwardingAlwaysGet', 'CallForwardingBusyGet',
           'CallForwardingNoAnswerGet', 'CallForwardingPlaceSettingGet', 'CallingPermission',
           'CallingPermissionAction', 'CallingPermissionCallType', 'DirectLineCallerIdNameObject',
           'InterceptAnnouncementsGet', 'InterceptAnnouncementsGetGreeting', 'InterceptAnnouncementsPatch',
           'InterceptGet', 'InterceptIncomingGet', 'InterceptIncomingGetType', 'InterceptIncomingPatch',
           'InterceptNumberGet', 'InterceptOutGoingGet', 'InterceptOutGoingGetType', 'ModifyCallingPermission',
           'ModifyPlaceCallForwardSettings', 'ModifyPlaceCallerIdGetExternalCallerIdNamePolicy',
           'MonitoredElementCallParkExtension', 'MonitoredElementItem', 'MonitoredElementUser',
           'MonitoredElementUserType', 'PhoneNumber', 'PlaceCallerIdGet', 'PlaceGetNumbersResponse', 'RingPattern',
           'SelectionObject', 'TransferNumberGet', 'UserInboundPermissionGet',
           'UserInboundPermissionGetExternalTransfer', 'UserMonitoringGet', 'UserNumberItem',
           'UserOutgoingPermissionGet', 'WorkspaceCallSettings12Api']


class AuthorizationCode(ApiModel):
    #: Access code.
    code: Optional[str] = None
    #: The description of the access code.
    description: Optional[str] = None


class CLIDPolicySelection(str, Enum):
    #: Outgoing caller ID will show the caller's direct line number
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID will show the main number for the location.
    location_number = 'LOCATION_NUMBER'
    #: Outgoing caller ID will show the value from the customNumber field.
    custom = 'CUSTOM'


class CallForwardingAlwaysGet(ApiModel):
    #: "Always" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "Always" call forwarding.
    destination: Optional[str] = None
    #: If `true`, a brief tone will be played on the person's phone when a call has been forwarded.
    ring_reminder_enabled: Optional[bool] = None
    #: Enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingBusyGet(ApiModel):
    #: "Busy" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "Busy" call forwarding.
    destination: Optional[str] = None
    #: Enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingNoAnswerGet(ApiModel):
    #: "No Answer" call forwarding is enabled or disabled.
    enabled: Optional[bool] = None
    #: Destination for "No Answer" call forwarding.
    destination: Optional[str] = None
    #: Number of rings before the call will be forwarded if unanswered.
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for `numberOfRings` setting.
    system_max_number_of_rings: Optional[int] = None
    #: Enables and disables sending incoming to destination number's voicemail if the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None


class CallForwardingPlaceSettingGet(ApiModel):
    #: Settings for forwarding all incoming calls to the destination you choose.
    always: Optional[CallForwardingAlwaysGet] = None
    #: Settings for forwarding all incoming calls to the destination you chose while the phone is in use or the
    #: workspace is busy.
    busy: Optional[CallForwardingBusyGet] = None
    #: Settings for forwarding which only occurs when you are away or not answering your phone.
    no_answer: Optional[CallForwardingNoAnswerGet] = None


class CallingPermissionCallType(str, Enum):
    #: Internal call type.
    internal_call = 'INTERNAL_CALL'
    #: Toll free call type.
    toll_free = 'TOLL_FREE'
    #: International call type.
    international = 'INTERNATIONAL'
    #: Operator Assisted call type.
    operator_assisted = 'OPERATOR_ASSISTED'
    #: Chargeable Directory Assisted call type.
    chargeable_directory_assisted = 'CHARGEABLE_DIRECTORY_ASSISTED'
    #: Special Services I call type.
    special_services_i = 'SPECIAL_SERVICES_I'
    #: Special Services II call type.
    special_services_ii = 'SPECIAL_SERVICES_II'
    #: Premium Services I call type.
    premium_services_i = 'PREMIUM_SERVICES_I'
    #: Premium Services II call type.
    premium_services_ii = 'PREMIUM_SERVICES_II'
    #: National call type.
    national = 'NATIONAL'


class CallingPermissionAction(str, Enum):
    #: The call type is allowed.
    allow = 'ALLOW'
    #: The call type is blocked.
    block = 'BLOCK'
    #: Access Code action for the specified call type.
    auth_code = 'AUTH_CODE'
    #: Transfer to Auto Transfer Number 1. The answering person can then approve the call and send it through or reject
    #: the call.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: Transfer to Auto Transfer Number 2. The answering person can then approve the call and send it through or reject
    #: the call.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: Transfer to Auto Transfer Number 3. The answering person can then approve the call and send it through or reject
    #: the call.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class CallingPermission(ApiModel):
    #: Type of the outgoing call.
    call_type: Optional[CallingPermissionCallType] = None
    #: Permission for call types.
    action: Optional[CallingPermissionAction] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None
    #: Indicates if the restriction is enforced by the system for the corresponding call type and cannot be changed.
    #: For example, certain call types (such as `INTERNATIONAL`) may be permanently blocked and this field will be
    #: `true` to reflect that the restriction is system-controlled and not editable.
    is_call_type_restriction_enabled: Optional[bool] = None


class InterceptAnnouncementsGetGreeting(str, Enum):
    #: A custom greeting is played when incoming calls are intercepted.
    custom = 'CUSTOM'
    #: A System default greeting is played when incoming calls are intercepted.
    default = 'DEFAULT'


class InterceptNumberGet(ApiModel):
    #: If `true`, the caller hears this new number when the call is intercepted.
    enabled: Optional[bool] = None
    #: New number the caller hears announced.
    destination: Optional[str] = None


class InterceptAnnouncementsGet(ApiModel):
    #: System default message places when incoming calls are intercepted.
    greeting: Optional[InterceptAnnouncementsGetGreeting] = None
    #: Filename of the custom greeting; this is an empty string if no custom greeting has been uploaded.
    filename: Optional[str] = None
    #: Information about the new number announcement.
    new_number: Optional[InterceptNumberGet] = None
    #: Information about how the call is handled if zero (0) is pressed.
    zero_transfer: Optional[InterceptNumberGet] = None


class InterceptAnnouncementsPatch(ApiModel):
    #: System default message is placed when incoming calls are intercepted.
    greeting: Optional[InterceptAnnouncementsGetGreeting] = None
    #: Information about the new number announcement.
    new_number: Optional[InterceptNumberGet] = None
    #: Information about how the call is handled if zero (0) is pressed.
    zero_transfer: Optional[InterceptNumberGet] = None


class InterceptIncomingGetType(str, Enum):
    #: All incoming calls are intercepted.
    intercept_all = 'INTERCEPT_ALL'
    #: Incoming calls are not intercepted.
    allow_all = 'ALLOW_ALL'


class InterceptIncomingGet(ApiModel):
    #: Incoming calls are intercepted.
    type: Optional[InterceptIncomingGetType] = None
    #: Enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    voicemail_enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[InterceptAnnouncementsGet] = None


class InterceptOutGoingGetType(str, Enum):
    #: Outgoing calls are intercepted.
    intercept_all = 'INTERCEPT_ALL'
    #: Only non-local calls are intercepted.
    allow_local_only = 'ALLOW_LOCAL_ONLY'


class InterceptOutGoingGet(ApiModel):
    #: All outgoing calls are intercepted.
    type: Optional[InterceptOutGoingGetType] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None
    #: Number to which the outbound call be transferred.
    destination: Optional[str] = None


class InterceptGet(ApiModel):
    #: `true` if call intercept is enabled.
    enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    incoming: Optional[InterceptIncomingGet] = None
    #: Settings related to how outgoing calls are handled when the intercept feature is enabled.
    outgoing: Optional[InterceptOutGoingGet] = None


class InterceptIncomingPatch(ApiModel):
    #: Incoming calls are intercepted.
    type: Optional[InterceptIncomingGetType] = None
    #: Enabled or disabled state of sending incoming calls to voicemail when the destination is an internal phone
    #: number and that number has the voicemail service enabled.
    voicemail_enabled: Optional[bool] = None
    #: Settings related to how incoming calls are handled when the intercept feature is enabled.
    announcements: Optional[InterceptAnnouncementsPatch] = None


class ModifyCallingPermission(ApiModel):
    #: Types for outgoing calls.
    call_type: Optional[CallingPermissionCallType] = None
    #: Permission for call types.
    action: Optional[CallingPermissionAction] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None


class ModifyPlaceCallForwardSettings(ApiModel):
    #: Call forwarding settings for a Workspace.
    call_forwarding: Optional[CallForwardingPlaceSettingGet] = None
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for any
    #: reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[CallForwardingBusyGet] = None


class ModifyPlaceCallerIdGetExternalCallerIdNamePolicy(str, Enum):
    #: Outgoing caller ID shows the caller's direct line name.
    direct_line = 'DIRECT_LINE'
    #: Outgoing caller ID shows the external caller ID name for the location.
    location = 'LOCATION'
    #: Outgoing caller ID shows the value from the `customExternalCallerIdName` field.
    other = 'OTHER'


class SelectionObject(str, Enum):
    #: When this option is selected, `customName` is to be shown for this workspace.
    custom_name = 'CUSTOM_NAME'
    #: When this option is selected, `displayName` is to be shown for this workspace.
    display_name = 'DISPLAY_NAME'


class DirectLineCallerIdNameObject(ApiModel):
    #: The selection of the direct line caller ID name. Defaults to `DISPLAY_NAME`.
    selection: Optional[SelectionObject] = None
    #: The custom direct line caller ID name. Required if `selection` is set to `CUSTOM_NAME`.
    custom_name: Optional[str] = None


class MonitoredElementCallParkExtension(ApiModel):
    #: ID of call park extension.
    id: Optional[str] = None
    #: Name of call park extension.
    name: Optional[str] = None
    #: Extension of call park extension.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Name of location for call park extension.
    location: Optional[str] = None
    #: ID of location for call park extension.
    location_id: Optional[str] = None


class MonitoredElementUserType(str, Enum):
    #: Object is a user.
    people = 'PEOPLE'
    #: Object is a workspace.
    place = 'PLACE'


class UserNumberItem(ApiModel):
    #: Phone number of person or workspace. Either `phoneNumber` or `extension` is mandatory.
    external: Optional[str] = None
    #: Extension of person or workspace. Either `phoneNumber` or `extension` is mandatory.
    extension: Optional[str] = None
    #: Routing prefix of location.
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    esn: Optional[str] = None
    #: Flag to indicate primary phone.
    primary: Optional[bool] = None
    #: Flag to indicate toll free number.
    toll_free_number: Optional[bool] = None


class MonitoredElementUser(ApiModel):
    #: ID of person or workspace.
    id: Optional[str] = None
    #: First name of person or workspace.
    first_name: Optional[str] = None
    #: Last name of person or workspace.
    last_name: Optional[str] = None
    #: Display name of person or workspace.
    display_name: Optional[str] = None
    #: Type of the person or workspace.
    type: Optional[MonitoredElementUserType] = None
    #: Email of the person or workspace.
    email: Optional[str] = None
    #: The list of phone numbers containing only the primary number for the monitored person, workspace.
    numbers: Optional[list[UserNumberItem]] = None
    #: Name of location for call park.
    location: Optional[str] = None
    #: ID of the location for call park.
    location_id: Optional[str] = None


class MonitoredElementItem(ApiModel):
    #: Monitored Call Park extension.
    callparkextension: Optional[MonitoredElementCallParkExtension] = None
    #: Monitored member for this workspace.
    member: Optional[MonitoredElementUser] = None


class PlaceCallerIdGet(ApiModel):
    #: Allowed types for the `selected` field. This field is read-only and cannot be modified.
    types: Optional[list[CLIDPolicySelection]] = None
    #: Which type of outgoing Caller ID will be used. This setting is for the number portion.
    selected: Optional[CLIDPolicySelection] = None
    #: Direct number which is shown if `DIRECT_LINE` is selected.
    direct_number: Optional[str] = None
    #: Location number which is shown if `LOCATION_NUMBER` is selected
    location_number: Optional[str] = None
    #: Flag to indicate if the location number is toll-free number.
    toll_free_location_number: Optional[bool] = None
    #: Custom number which is shown if CUSTOM is selected. This value must be a number from the workspace's location or
    #: from another location with the same country, PSTN provider, and zone (only applicable for India locations) as
    #: the workspace's location.
    custom_number: Optional[str] = None
    #: Workspace's caller ID display name. This field has been deprecated. Please use `directLineCallerIdName` and
    #: `dialByName` instead.
    display_name: Optional[str] = None
    #: Workspace's caller ID display details. Default is `.`. This field has been deprecated. Please use
    #: `directLineCallerIdName` and `dialByName` instead.
    display_detail: Optional[str] = None
    #: Block this workspace's identity when receiving a call.
    block_in_forward_calls_enabled: Optional[bool] = None
    #: Designates which type of External Caller ID Name policy is used. Default is `DIRECT_LINE`.
    external_caller_id_name_policy: Optional[ModifyPlaceCallerIdGetExternalCallerIdNamePolicy] = None
    #: Custom external caller ID name which is shown if external caller ID name policy is `OTHER`.
    custom_external_caller_id_name: Optional[str] = None
    #: Location's external caller ID name which is shown if external caller ID name policy is `LOCATION`.
    location_external_caller_id_name: Optional[str] = None
    #: Settings for the direct line caller ID name to be shown for this workspace.
    direct_line_caller_id_name: Optional[DirectLineCallerIdNameObject] = None
    #: The name to be used for dial by name functions.
    dial_by_name: Optional[str] = None


class TransferNumberGet(ApiModel):
    #: When `true`, use custom settings for the transfer numbers category of outbound permissions.
    use_custom_transfer_numbers: Optional[bool] = None
    #: When calling a specific call type, this workspace will be automatically transferred to another number.
    auto_transfer_number1: Optional[str] = None
    #: When calling a specific call type, this workspace will be automatically transferred to another number.
    auto_transfer_number2: Optional[str] = None
    #: When calling a specific call type, this workspace will be automatically transferred to another number.
    auto_transfer_number3: Optional[str] = None


class UserInboundPermissionGetExternalTransfer(str, Enum):
    #: All external calls are allowed.
    allow_all_external = 'ALLOW_ALL_EXTERNAL'
    #: Only externally transferred external calls are allowed.
    allow_only_transferred_external = 'ALLOW_ONLY_TRANSFERRED_EXTERNAL'
    #: All external calls are blocked.
    block_all_external = 'BLOCK_ALL_EXTERNAL'


class UserInboundPermissionGet(ApiModel):
    #: Incoming Permission state. If disabled, the default settings are used.
    use_custom_enabled: Optional[bool] = None
    #: Call transfer setting.
    external_transfer: Optional[UserInboundPermissionGetExternalTransfer] = None
    #: Flag to indicate if workspace can receive internal calls.
    internal_calls_enabled: Optional[bool] = None
    #: Flag to indicate if workspace can receive collect calls.
    collect_calls_enabled: Optional[bool] = None


class UserMonitoringGet(ApiModel):
    #: Call park notification enabled or disabled.
    call_park_notification_enabled: Optional[bool] = None
    #: Monitored element items.
    monitored_elements: Optional[MonitoredElementItem] = None


class UserOutgoingPermissionGet(ApiModel):
    #: When `true`, indicates that this workspace uses the shared control that applies to all outgoing call settings
    #: categories when placing outbound calls.
    use_custom_enabled: Optional[bool] = None
    #: When `true`, indicates that this workspace uses the specified outgoing calling permissions when placing outbound
    #: calls.
    use_custom_permissions: Optional[bool] = None
    #: Workspace's list of outgoing permissions.
    calling_permissions: Optional[list[CallingPermission]] = None


class Action(str, Enum):
    #: Add action.
    add = 'ADD'
    #: Delete action.
    delete = 'DELETE'


class RingPattern(str, Enum):
    #: Normal incoming ring pattern.
    normal = 'NORMAL'
    #: Incoming ring pattern of two long rings.
    long_long = 'LONG_LONG'
    #: Incoming ring pattern of two short rings, followed by a short ring.
    short_short_long = 'SHORT_SHORT_LONG'
    #: Incoming ring pattern of a short ring, followed by a long ring, followed by a short ring.
    short_long_short = 'SHORT_LONG_SHORT'


class PhoneNumber(ApiModel):
    #: If `true` marks the phone number as primary.
    primary: Optional[bool] = None
    #: Either 'ADD' to add phone numbers or 'DELETE' to remove phone numbers.
    action: Optional[Action] = None
    #: Phone numbers that are assigned.
    direct_number: Optional[str] = None
    #: Extension that is assigned.
    extension: Optional[str] = None
    #: Ring Pattern of this number.
    ring_pattern: Optional[RingPattern] = None


class PlaceGetNumbersResponse(ApiModel):
    #: Enables a distinctive ring pattern for the person.
    distinctive_ring_enabled: Optional[bool] = None
    #: List of phone numbers that are assigned to a person.
    phone_numbers: Optional[list[PhoneNumber]] = None


class WorkspaceCallSettings12Api(ApiChild, base='workspaces'):
    """
    Workspace Call Settings (1/2)
    
    Workspaces represent places where people work, such as conference rooms, meeting spaces, lobbies, and lunchrooms.
    Devices may be associated with workspaces.
    
    Webex Calling Workspace Settings support reading and writing of Webex Calling settings for a specific workspace
    within the organization.
    
    Viewing the list of settings in a workspace /v1/workspaces API requires an full, device, or read-only administrator
    or location administrator auth token with the `spark-admin:workspaces_read` scope.
    
    Adding, updating, or deleting settings in a workspace /v1/workspaces API requires an full or device administrator
    auth token with the `spark-admin:workspaces_write` scope.
    
    This API can also be used by partner administrators acting as administrators of a different organization than their
    own. In those cases, an `orgId` must be supplied, as indicated in the reference documentation for the relevant
    endpoints.
    
    **NOTE**: Hot Desk Only workspace does not support any calling settings.
    """

    def retrieve_call_forwarding_settings_for_a_workspace(self, workspace_id: str,
                                                          org_id: str = None) -> ModifyPlaceCallForwardSettings:
        """
        Retrieve Call Forwarding Settings for a Workspace.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy, forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer, forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`ModifyPlaceCallForwardSettings`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/callForwarding')
        data = super().get(url, params=params)
        r = ModifyPlaceCallForwardSettings.model_validate(data)
        return r

    def modify_call_forwarding_settings_for_a_workspace(self, workspace_id: str,
                                                        call_forwarding: CallForwardingPlaceSettingGet,
                                                        business_continuity: CallForwardingBusyGet,
                                                        org_id: str = None):
        """
        Modify call forwarding settings for a Workspace.

        Three types of call forwarding are supported:

        + Always - forwards all incoming calls to the destination you choose.

        + When busy, forwards all incoming calls to the destination you chose while the phone is in use or the person
        is busy.

        + When no answer, forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as a power outage, failed Internet connection, or wiring
        problem.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param call_forwarding: Call forwarding settings for a Workspace.
        :type call_forwarding: CallForwardingPlaceSettingGet
        :param business_continuity: Settings for sending calls to a destination of your choice if your phone is not
            connected to the network for any reason, such as power outage, failed Internet connection, or wiring
            problem.
        :type business_continuity: CallForwardingBusyGet
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['businessContinuity'] = business_continuity.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{workspace_id}/features/callForwarding')
        super().put(url, params=params, json=body)

    def retrieve_call_waiting_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> bool:
        """
        Retrieve Call Waiting Settings for a Workspace.

        Call Waiting allows workspaces to handle multiple simultaneous calls. Workspaces with Call Waiting enabled can
        place a call on hold to answer or initiate another call.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/callWaiting')
        data = super().get(url, params=params)
        r = data['enabled']
        return r

    def modify_call_waiting_settings_for_a_workspace(self, workspace_id: str, enabled: bool = None,
                                                     org_id: str = None):
        """
        Modify Call Waiting Settings for a Workspace.

        Call Waiting allows workspaces to handle multiple simultaneous calls. Workspaces with Call Waiting enabled can
        place a call on hold to answer or initiate another call.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: Call Waiting state.
        :type enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        url = self.ep(f'{workspace_id}/features/callWaiting')
        super().put(url, params=params, json=body)

    def read_caller_id_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> PlaceCallerIdGet:
        """
        Read Caller ID Settings for a Workspace

        Retrieve a workspace's Caller ID settings.

        Caller ID settings control how a workspace's information is displayed when making outgoing calls.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.<div><Callout type="warning">The fields `directLineCallerIdName.selection`,
        `directLineCallerIdName.customName`, and `dialByName` are not supported in Webex for Government (FedRAMP).
        Instead, administrators must use the `displayName` and `displayDetail` fields to configure and view both
        caller ID and dial-by-name settings.</Callout></div>

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`PlaceCallerIdGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/callerId')
        data = super().get(url, params=params)
        r = PlaceCallerIdGet.model_validate(data)
        return r

    def configure_caller_id_settings_for_a_workspace(self, workspace_id: str, selected: CLIDPolicySelection,
                                                     custom_number: str = None, display_name: str = None,
                                                     display_detail: str = None,
                                                     block_in_forward_calls_enabled: bool = None,
                                                     external_caller_id_name_policy: ModifyPlaceCallerIdGetExternalCallerIdNamePolicy = None,
                                                     custom_external_caller_id_name: str = None,
                                                     location_external_caller_id_name: str = None,
                                                     direct_line_caller_id_name: DirectLineCallerIdNameObject = None,
                                                     dial_by_name: str = None, org_id: str = None):
        """
        Configure Caller ID Settings for a Workspace

        Configure workspace's Caller ID settings.

        Caller ID settings control how a workspace's information is displayed when making outgoing calls.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.<div><Callout type="warning">The fields `directLineCallerIdName.selection`,
        `directLineCallerIdName.customName`, and `dialByName` are not supported in Webex for Government (FedRAMP).
        Instead, administrators must use the `displayName` and `displayDetail` fields to configure and view both
        caller ID and dial-by-name settings.</Callout></div>

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param selected: Which type of outgoing Caller ID will be used. This setting is for the number portion.
        :type selected: CLIDPolicySelection
        :param custom_number: Custom number which is shown if CUSTOM is selected. This value must be a number from the
            workspace's location or from another location with the same country, PSTN provider, and zone (only
            applicable for India locations) as the workspace's location.
        :type custom_number: str
        :param display_name: Workspace's caller ID display name. This field has been deprecated. Please use
            `directLineCallerIdName` and `dialByName` instead.
        :type display_name: str
        :param display_detail: Workspace's caller ID display details. This field has been deprecated. Please use
            `directLineCallerIdName` and `dialByName` instead.
        :type display_detail: str
        :param block_in_forward_calls_enabled: Block this workspace's identity when receiving a call.
        :type block_in_forward_calls_enabled: bool
        :param external_caller_id_name_policy: Designates which type of External Caller ID Name policy is used. Default
            is `DIRECT_LINE`.
        :type external_caller_id_name_policy: ModifyPlaceCallerIdGetExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Custom external caller ID name which is shown if external caller ID name
            policy is `OTHER`.
        :type custom_external_caller_id_name: str
        :param location_external_caller_id_name: Location's external caller ID name which is shown if external caller
            ID name policy is `LOCATION`.
        :type location_external_caller_id_name: str
        :param direct_line_caller_id_name: Settings for the direct line caller ID name to be shown for this workspace.
        :type direct_line_caller_id_name: DirectLineCallerIdNameObject
        :param dial_by_name: Sets or clears the name to be used for dial by name functions. To clear the `dialByName`,
            the attribute must be set to null or empty string. Characters of `%`,  `+`, `\`, `"` and Unicode
            characters are not allowed.
        :type dial_by_name: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['selected'] = enum_str(selected)
        if custom_number is not None:
            body['customNumber'] = custom_number
        if display_name is not None:
            body['displayName'] = display_name
        if display_detail is not None:
            body['displayDetail'] = display_detail
        if block_in_forward_calls_enabled is not None:
            body['blockInForwardCallsEnabled'] = block_in_forward_calls_enabled
        if external_caller_id_name_policy is not None:
            body['externalCallerIdNamePolicy'] = enum_str(external_caller_id_name_policy)
        if custom_external_caller_id_name is not None:
            body['customExternalCallerIdName'] = custom_external_caller_id_name
        if location_external_caller_id_name is not None:
            body['locationExternalCallerIdName'] = location_external_caller_id_name
        if direct_line_caller_id_name is not None:
            body['directLineCallerIdName'] = direct_line_caller_id_name.model_dump(mode='json', by_alias=True, exclude_none=True)
        if dial_by_name is not None:
            body['dialByName'] = dial_by_name
        url = self.ep(f'{workspace_id}/features/callerId')
        super().put(url, params=params, json=body)

    def retrieve_incoming_permission_settings_for_a_workspace(self, workspace_id: str,
                                                              org_id: str = None) -> UserInboundPermissionGet:
        """
        Retrieve Incoming Permission settings for a Workspace.

        Incoming permission settings allow modifying permissions for a workspace that can be different from the
        organization's default to manage different call types.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`UserInboundPermissionGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/incomingPermission')
        data = super().get(url, params=params)
        r = UserInboundPermissionGet.model_validate(data)
        return r

    def modify_incoming_permission_settings_for_a_workspace(self, workspace_id: str, use_custom_enabled: bool = None,
                                                            external_transfer: UserInboundPermissionGetExternalTransfer = None,
                                                            internal_calls_enabled: bool = None,
                                                            collect_calls_enabled: bool = None, org_id: str = None):
        """
        Modify Incoming Permission settings for a Workspace.

        Incoming permission settings allow modifying permissions for a workspace that can be different from the
        organization's default to manage different call types.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param use_custom_enabled: Incoming Permission state. If disabled, the default settings are used.
        :type use_custom_enabled: bool
        :param external_transfer: Call transfer setting.
        :type external_transfer: UserInboundPermissionGetExternalTransfer
        :param internal_calls_enabled: Flag to indicate if the workspace can receive internal calls.
        :type internal_calls_enabled: bool
        :param collect_calls_enabled: Flag to indicate if the workspace can receive collect calls.
        :type collect_calls_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if use_custom_enabled is not None:
            body['useCustomEnabled'] = use_custom_enabled
        if external_transfer is not None:
            body['externalTransfer'] = enum_str(external_transfer)
        if internal_calls_enabled is not None:
            body['internalCallsEnabled'] = internal_calls_enabled
        if collect_calls_enabled is not None:
            body['collectCallsEnabled'] = collect_calls_enabled
        url = self.ep(f'{workspace_id}/features/incomingPermission')
        super().put(url, params=params, json=body)

    def read_call_intercept_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> InterceptGet:
        """
        Read Call Intercept Settings for a Workspace

        Retrieves Workspace's Call Intercept Settings

        The intercept feature gracefully takes a workspace's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified workspace are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`InterceptGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/intercept')
        data = super().get(url, params=params)
        r = InterceptGet.model_validate(data)
        return r

    def configure_call_intercept_settings_for_a_workspace(self, workspace_id: str, enabled: bool = None,
                                                          incoming: InterceptIncomingPatch = None,
                                                          outgoing: InterceptOutGoingGet = None, org_id: str = None):
        """
        Configure Call Intercept Settings for a Workspace

        Configures a Workspace's Call Intercept Settings

        The intercept feature gracefully takes a workspace's phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified person are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_write` or a user auth token with `spark:workspaces_read` scope can be used by a person
        to read their settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enabled: `true` if call interception is enabled.
        :type enabled: bool
        :param incoming: Settings related to how incoming calls are handled when the intercept feature is enabled.
        :type incoming: InterceptIncomingPatch
        :param outgoing: Settings related to how outgoing calls are handled when the intercept feature is enabled.
        :type outgoing: InterceptOutGoingGet
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if incoming is not None:
            body['incoming'] = incoming.model_dump(mode='json', by_alias=True, exclude_none=True)
        if outgoing is not None:
            body['outgoing'] = outgoing.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{workspace_id}/features/intercept')
        super().put(url, params=params, json=body)

    def retrieve_monitoring_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> UserMonitoringGet:
        """
        Retrieve Monitoring Settings for a Workspace

        Retrieves Monitoring settings for a Workspace.

        Allow workspaces to monitor the line status of specified agents, workspaces, or call park extensions. The line
        status indicates if a monitored agent or a workspace is on a call, or if a call has been parked on the
        monitored call park extension.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`UserMonitoringGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/monitoring')
        data = super().get(url, params=params)
        r = UserMonitoringGet.model_validate(data)
        return r

    def modify_monitoring_settings_for_a_workspace(self, workspace_id: str, enable_call_park_notification: bool = None,
                                                   monitored_elements: list[str] = None, org_id: str = None):
        """
        Modify Monitoring settings for a Workspace.

        Allow workspaces to monitor the line status of specified agents, workspaces, or call park extensions. The line
        status indicates if a monitored agent or a workspace is on a call, or if a call has been parked on the
        monitored call park extension.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param enable_call_park_notification: Call park notification is enabled or disabled.
        :type enable_call_park_notification: bool
        :param monitored_elements: Array of ID strings of monitored elements.
        :type monitored_elements: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enable_call_park_notification is not None:
            body['enableCallParkNotification'] = enable_call_park_notification
        if monitored_elements is not None:
            body['monitoredElements'] = monitored_elements
        url = self.ep(f'{workspace_id}/features/monitoring')
        super().put(url, params=params, json=body)

    def list_numbers_associated_with_a_specific_workspace(self, workspace_id: str,
                                                          org_id: str = None) -> PlaceGetNumbersResponse:
        """
        List numbers associated with a specific workspace

        List the PSTN phone numbers associated with a specific workspace, by ID, within the organization. Also shows
        the location and organization associated with the workspace.

        Retrieving this list requires a full or read-only administrator or location administrator auth token with a
        scope of `spark-admin:workspaces_read`.

        :param workspace_id: List numbers for this workspace.
        :type workspace_id: str
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            can use this parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: :class:`PlaceGetNumbersResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/numbers')
        data = super().get(url, params=params)
        r = PlaceGetNumbersResponse.model_validate(data)
        return r

    def retrieve_outgoing_permission_settings_for_a_workspace(self, workspace_id: str,
                                                              org_id: str = None) -> UserOutgoingPermissionGet:
        """
        Retrieve Outgoing Permission settings for a Workspace.

        Turn on outgoing call settings for this workspace to override the calling settings from the location that are
        used by default.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`UserOutgoingPermissionGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/outgoingPermission')
        data = super().get(url, params=params)
        r = UserOutgoingPermissionGet.model_validate(data)
        return r

    def modify_outgoing_permission_settings_for_a_workspace(self, workspace_id: str, use_custom_enabled: bool = None,
                                                            use_custom_permissions: bool = None,
                                                            calling_permissions: list[ModifyCallingPermission] = None,
                                                            org_id: str = None):
        """
        Modify Outgoing Permission Settings for a Workspace

        Modify Outgoing Permission settings for a Place.

        Turn on outgoing call settings for this workspace to override the calling settings from the location that are
        used by default.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param use_custom_enabled: When `true`, indicates that this workspace uses the shared control that applies to
            all outgoing call settings categories when placing outbound calls.
        :type use_custom_enabled: bool
        :param use_custom_permissions: When `true`, indicates that this workspace uses the specified outgoing calling
            permissions when placing outbound calls.
        :type use_custom_permissions: bool
        :param calling_permissions: Workspace's list of outgoing permissions.
        :type calling_permissions: list[ModifyCallingPermission]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if use_custom_enabled is not None:
            body['useCustomEnabled'] = use_custom_enabled
        if use_custom_permissions is not None:
            body['useCustomPermissions'] = use_custom_permissions
        if calling_permissions is not None:
            body['callingPermissions'] = TypeAdapter(list[ModifyCallingPermission]).dump_python(calling_permissions, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{workspace_id}/features/outgoingPermission')
        super().put(url, params=params, json=body)

    def delete_all_access_codes_for_a_workspace(self, workspace_id: str, org_id: str = None):
        """
        Delete all Access Codes for a Workspace

        Deletes all Access codes for the given workspace.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/outgoingPermission/accessCodes')
        super().delete(url, params=params)

    def retrieve_access_codes_for_a_workspace(self, workspace_id: str, org_id: str = None) -> list[AuthorizationCode]:
        """
        Retrieve Access codes for a Workspace.

        Access codes are used to bypass permissions.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: list[AuthorizationCode]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/outgoingPermission/accessCodes')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AuthorizationCode]).validate_python(data['accessCodes'])
        return r

    def create_access_codes_for_a_workspace(self, workspace_id: str, code: str, description: str, org_id: str = None):
        """
        Create Access Codes for a Workspace

        Create new Access codes for the given workspace.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param code: An Access code.
        :type code: str
        :param description: The description of the access code.
        :type description: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['code'] = code
        body['description'] = description
        url = self.ep(f'{workspace_id}/features/outgoingPermission/accessCodes')
        super().post(url, params=params, json=body)

    def modify_access_codes_for_a_workspace(self, workspace_id: str, delete_codes: list[str] = None,
                                            org_id: str = None):
        """
        Modify Access codes for a workspace.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param delete_codes: Access Codes to delete.
        :type delete_codes: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if delete_codes is not None:
            body['deleteCodes'] = delete_codes
        url = self.ep(f'{workspace_id}/features/outgoingPermission/accessCodes')
        super().put(url, params=params, json=body)

    def retrieve_transfer_numbers_settings_for_a_workspace(self, workspace_id: str,
                                                           org_id: str = None) -> TransferNumberGet:
        """
        Retrieve Transfer Numbers Settings for a Workspace.

        When calling a specific call type, this workspace will be automatically transferred to another number. The
        person assigned the Auto Transfer Number can then approve the call and send it through or reject the call
        type. You can add up to 3 numbers.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with `spark:workspaces_read` scope can be used to read
        workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`TransferNumberGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/features/outgoingPermission/autoTransferNumbers')
        data = super().get(url, params=params)
        r = TransferNumberGet.model_validate(data)
        return r

    def modify_transfer_numbers_settings_for_a_workspace(self, workspace_id: str, use_custom_transfer_numbers: bool,
                                                         auto_transfer_number1: str = None,
                                                         auto_transfer_number2: str = None,
                                                         auto_transfer_number3: str = None, org_id: str = None):
        """
        Modify Transfer Numbers Settings for a Workspace

        Modify Transfer Numbers Settings for a place.

        When calling a specific call type, this workspace will be automatically transferred to another number. The
        person assigned the Auto Transfer Number can then approve the call and send it through or reject the call
        type. You can add up to 3 numbers.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param use_custom_transfer_numbers: When `true`, use custom settings for the transfer numbers category of
            outbound permissions.
        :type use_custom_transfer_numbers: bool
        :param auto_transfer_number1: When calling a specific call type, this workspace will be automatically
            transferred to another number.
        :type auto_transfer_number1: str
        :param auto_transfer_number2: When calling a specific call type, this workspace will be automatically
            transferred to another number.
        :type auto_transfer_number2: str
        :param auto_transfer_number3: When calling a specific call type, this workspace will be automatically
            transferred to another number.
        :type auto_transfer_number3: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['useCustomTransferNumbers'] = use_custom_transfer_numbers
        if auto_transfer_number1 is not None:
            body['autoTransferNumber1'] = auto_transfer_number1
        if auto_transfer_number2 is not None:
            body['autoTransferNumber2'] = auto_transfer_number2
        if auto_transfer_number3 is not None:
            body['autoTransferNumber3'] = auto_transfer_number3
        url = self.ep(f'{workspace_id}/features/outgoingPermission/autoTransferNumbers')
        super().put(url, params=params, json=body)

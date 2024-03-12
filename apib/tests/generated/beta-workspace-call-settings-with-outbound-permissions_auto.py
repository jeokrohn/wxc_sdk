from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AuthorizationCode', 'AuthorizationCodeLevel', 'BetaWorkspaceCallSettingsWithOutboundPermissionsApi',
           'CallingPermission', 'CallingPermissionAction', 'CallingPermissionCallType', 'TransferNumberGet',
           'UserPlaceAuthorizationCodeListGet', 'WorkspaceDigitPatternObject',
           'WorkspaceOutgoingPermissionDigitPatternGetListObject', 'WorkspaceOutgoingPermissionGet']


class CallingPermissionCallType(str, Enum):
    #: Indicates the internal call type.
    internal_call = 'INTERNAL_CALL'
    #: Indicates the toll free call type.
    toll_free = 'TOLL_FREE'
    #: Indicates the international call type.
    international = 'INTERNATIONAL'
    #: Indicates the operator assisted call type.
    operator_assisted = 'OPERATOR_ASSISTED'
    #: Indicates the chargeable directory assisted call type.
    chargeable_directory_assisted = 'CHARGEABLE_DIRECTORY_ASSISTED'
    #: Indicates the special services I call type.
    special_services_i = 'SPECIAL_SERVICES_I'
    #: Indicates the special services II call type.
    special_services_ii = 'SPECIAL_SERVICES_II'
    #: Indicates the premium services I call type.
    premium_services_i = 'PREMIUM_SERVICES_I'
    #: Indicates the premium services II call type.
    premium_services_ii = 'PREMIUM_SERVICES_II'
    #: Indicates the calls that are within your country of origin, both within and outside of your local area code.
    national = 'NATIONAL'


class CallingPermissionAction(str, Enum):
    #: The call type is allowed.
    allow = 'ALLOW'
    #: The call type is blocked.
    block = 'BLOCK'
    #: Indicates access code action for the specified call type.
    auth_code = 'AUTH_CODE'
    #: Indicates transfer to Auto Transfer Number 1. The answering workspace can then approve the call and send it
    #: through or reject the call.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: Indicates transfer to Auto Transfer Number 2. The answering workspace can then approve the call and send it
    #: through or reject the call.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: Indicates transfer to Auto Transfer Number 3. The answering workspace can then approve the call and send it
    #: through or reject the call.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class CallingPermission(ApiModel):
    #: Type of the outgoing call.
    #: example: INTERNAL_CALL
    call_type: Optional[CallingPermissionCallType] = None
    #: Indicates permission for call types.
    #: example: ALLOW
    action: Optional[CallingPermissionAction] = None
    #: Indicate calling permission for call type enable status.
    #: example: True
    transfer_enabled: Optional[bool] = None


class WorkspaceOutgoingPermissionGet(ApiModel):
    #: When true, indicates that this workspace uses the shared control that applies to all outgoing call settings
    #: categories when placing outbound calls.
    #: example: True
    use_custom_enabled: Optional[bool] = None
    #: When true, indicates that this workspace uses the specified outgoing calling permissions when placing outbound
    #: calls.
    #: example: True
    use_custom_permissions: Optional[bool] = None
    #: Workspace's list of outgoing permissions.
    calling_permissions: Optional[list[CallingPermission]] = None


class AuthorizationCodeLevel(str, Enum):
    #: Indicates the location level access code.
    location = 'LOCATION'
    #: Indicates the workspace level access code.
    custom = 'CUSTOM'


class AuthorizationCode(ApiModel):
    #: Indicates an access code.
    #: example: 4856
    code: Optional[str] = None
    #: Indicates the description of the access code.
    #: example: Marketing's access code
    description: Optional[str] = None
    #: Indicates the level of each access code.
    #: example: CUSTOM
    level: Optional[AuthorizationCodeLevel] = None


class UserPlaceAuthorizationCodeListGet(ApiModel):
    #: When `true`, use custom settings for the access codes category of outgoing call permissions.
    use_custom_access_codes: Optional[bool] = None
    #: Indicates the set of activation codes and description.
    access_codes: Optional[list[AuthorizationCode]] = None


class TransferNumberGet(ApiModel):
    #: When `true`, use custom settings for the transfer numbers category of outgoing call permissions.
    #: example: True
    use_custom_transfer_numbers: Optional[bool] = None
    #: When calling a specific call type, this workspace will be automatically transferred to another number.
    #: `autoTransferNumber1` will be used when the associated calling permission action is set to `TRANSFER_NUMBER_1`.
    #: example: "+1205553650"
    auto_transfer_number1: Optional[str] = None
    #: When calling a specific call type, this workspace will be automatically transferred to another number.
    #: `autoTransferNumber2` will be used when the associated calling permission action is set to `TRANSFER_NUMBER_2`.
    #: example: "+1205553651"
    auto_transfer_number2: Optional[str] = None
    #: When calling a specific call type, this workspace will be automatically transferred to another number.
    #: `autoTransferNumber3` will be used when the associated calling permission action is set to `TRANSFER_NUMBER_3`.
    #: example: "+1205553652"
    auto_transfer_number3: Optional[str] = None


class WorkspaceDigitPatternObject(ApiModel):
    #: A unique identifier for the digit pattern.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSEVEVUxFL1FWVlVUMEZVVkVWT1JFRk9WQzFDVlZOSlRrVlRVeTFJVDFWU1V3
    id: Optional[str] = None
    #: A unique name for the digit pattern.
    #: example: DigitPattern1
    name: Optional[str] = None
    #: The digit pattern to be matched with the input number.
    #: example: 1XXX
    pattern: Optional[str] = None
    #: Action to be performed on the input number that matches with the digit pattern.
    #: example: ALLOW
    action: Optional[CallingPermissionAction] = None
    #: Option to allow or disallow transfer of calls.
    #: example: True
    transfer_enabled: Optional[bool] = None


class WorkspaceOutgoingPermissionDigitPatternGetListObject(ApiModel):
    #: When `true`, use custom settings for the digit patterns category of outgoing call permissions.
    use_custom_digit_patterns: Optional[bool] = None
    #: List of digit patterns.
    digit_patterns: Optional[list[WorkspaceDigitPatternObject]] = None


class BetaWorkspaceCallSettingsWithOutboundPermissionsApi(ApiChild, base=''):
    """
    Beta Workspace Call Settings with Outbound Permissions
    
    Workspaces represent places where people work, such as conference rooms, meeting spaces, lobbies, and lunchrooms.
    Devices may be associated with workspaces.
    
    Webex Calling Workspace Settings support reading and writing of Webex Calling settings for a specific workspace
    within the organization.
    
    Viewing the list of settings in a workspace /v1/workspaces API requires a full, device, or read-only administrator
    auth token with the `spark-admin:workspaces_read` scope.
    
    Adding, updating, or deleting settings in a workspace /v1/workspaces API requires a full or device administrator
    auth token with the `spark-admin:workspaces_write` scope.
    
    This API can also be used by partner administrators acting as administrators of a different organization than their
    own. In those cases, an `orgId` must be supplied, as indicated in the reference documentation for the relevant
    endpoints.
    """

    def retrieve_outgoing_permission_settings_for_a_workspace(self, workspace_id: str,
                                                              org_id: str = None) -> WorkspaceOutgoingPermissionGet:
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
        :rtype: :class:`WorkspaceOutgoingPermissionGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission')
        data = super().get(url, params=params)
        r = WorkspaceOutgoingPermissionGet.model_validate(data)
        return r

    def modify_outgoing_permission_settings_for_a_workspace(self, workspace_id: str, use_custom_enabled: bool = None,
                                                            use_custom_permissions: bool = None,
                                                            calling_permissions: list[CallingPermission] = None,
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
        :param use_custom_enabled: When true, indicates that this workspace uses the shared control that applies to all
            outgoing call settings categories when placing outbound calls.
        :type use_custom_enabled: bool
        :param use_custom_permissions: When true, indicates that this workspace uses the specified outgoing calling
            permissions when placing outbound calls.
        :type use_custom_permissions: bool
        :param calling_permissions: Workspace's list of outgoing permissions.
        :type calling_permissions: list[CallingPermission]
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
            body['callingPermissions'] = TypeAdapter(list[CallingPermission]).dump_python(calling_permissions, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission')
        super().put(url, params=params, json=body)

    def retrieve_access_codes_for_a_workspace(self, workspace_id: str,
                                              org_id: str = None) -> UserPlaceAuthorizationCodeListGet:
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
        :rtype: :class:`UserPlaceAuthorizationCodeListGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/accessCodes')
        data = super().get(url, params=params)
        r = UserPlaceAuthorizationCodeListGet.model_validate(data)
        return r

    def modify_access_codes_for_a_workspace(self, workspace_id: str, use_custom_access_codes: bool = None,
                                            delete_codes: list[str] = None, org_id: str = None):
        """
        Modify Access codes for a workspace.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:workspaces_write` scope or a user auth token with `spark:workspaces_write` scope can be used to
        update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param use_custom_access_codes: When `true`, use custom settings for the access codes category of outgoing call
            permissions.
        :type use_custom_access_codes: bool
        :param delete_codes: Indicates access codes to delete.
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
        if use_custom_access_codes is not None:
            body['useCustomAccessCodes'] = use_custom_access_codes
        if delete_codes is not None:
            body['deleteCodes'] = delete_codes
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/accessCodes')
        super().put(url, params=params, json=body)

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
        :param code: Indicates an access code.
        :type code: str
        :param description: Indicates the description of the access code.
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
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/accessCodes')
        super().post(url, params=params, json=body)

    def delete_access_codes_for_a_workspace(self, workspace_id: str, org_id: str = None):
        """
        Delete Access Codes for a Workspace

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
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/accessCodes')
        super().delete(url, params=params)

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
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/autoTransferNumbers')
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
            outgoing call permissions.
        :type use_custom_transfer_numbers: bool
        :param auto_transfer_number1: When calling a specific call type, this workspace will be automatically
            transferred to another number. `autoTransferNumber1` will be used when the associated calling permission
            action is set to `TRANSFER_NUMBER_1`.
        :type auto_transfer_number1: str
        :param auto_transfer_number2: When calling a specific call type, this workspace will be automatically
            transferred to another number. `autoTransferNumber2` will be used when the associated calling permission
            action is set to `TRANSFER_NUMBER_2`.
        :type auto_transfer_number2: str
        :param auto_transfer_number3: When calling a specific call type, this workspace will be automatically
            transferred to another number. `autoTransferNumber3` will be used when the associated calling permission
            action is set to `TRANSFER_NUMBER_3`.
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
        url = self.ep(f'workspaces/{workspace_id}/features/outgoingPermission/autoTransferNumbers')
        super().put(url, params=params, json=body)

    def retrieve_all_digit_patterns_for_a_workspace(self, workspace_id: str,
                                                    org_id: str = None) -> WorkspaceOutgoingPermissionDigitPatternGetListObject:
        """
        Retrieve all Digit Patterns for a Workspace

        Retrieve Digit Patterns for a Workspace.

        Digit patterns are used to bypass permissions.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`WorkspaceOutgoingPermissionDigitPatternGetListObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns')
        data = super().get(url, params=params)
        r = WorkspaceOutgoingPermissionDigitPatternGetListObject.model_validate(data)
        return r

    def retrieve_a_digit_pattern_details_for_the_workspace(self, workspace_id: str, digit_pattern_id: str,
                                                           org_id: str = None) -> WorkspaceDigitPatternObject:
        """
        Retrieve a Digit Pattern details for the Workspace

        Retrieve the designated digit pattern.

        Digit patterns are used to bypass permissions.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`WorkspaceDigitPatternObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        data = super().get(url, params=params)
        r = WorkspaceDigitPatternObject.model_validate(data)
        return r

    def create_digit_pattern_for_a_workspace(self, workspace_id: str, name: str, pattern: str,
                                             action: CallingPermissionAction, transfer_enabled: bool,
                                             org_id: str = None) -> str:
        """
        Create Digit Pattern for a Workspace

        Create new Digit Pattern for the given workspace.

        Digit patterns are used to bypass permissions.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches with the digit pattern.
        :type action: CallingPermissionAction
        :param transfer_enabled: Option to allow or disallow transfer of calls.
        :type transfer_enabled: bool
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['pattern'] = pattern
        body['action'] = enum_str(action)
        body['transferEnabled'] = transfer_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_the_digit_pattern_category_control_settings_for_the_workspace(self, workspace_id: str,
                                                                             use_custom_digit_patterns: bool = None,
                                                                             org_id: str = None):
        """
        Modify the Digit Pattern Category Control Settings for the Workspace

        Modifies whether this workspace uses the specified digit patterns when placing outbound calls or not.

        Updating the digit pattern category control settings requires a full or location administrator auth token with
        a scope of `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param use_custom_digit_patterns: When `true`, use custom settings for the digit patterns category of outgoing
            call permissions.
        :type use_custom_digit_patterns: bool
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
        if use_custom_digit_patterns is not None:
            body['useCustomDigitPatterns'] = use_custom_digit_patterns
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns')
        super().put(url, params=params, json=body)

    def modify_a_digit_pattern_for_the_workspace(self, workspace_id: str, digit_pattern_id: str, name: str = None,
                                                 pattern: str = None, action: CallingPermissionAction = None,
                                                 transfer_enabled: bool = None, org_id: str = None):
        """
        Modify a Digit Pattern for the Workspace

        Modify the designated Digit Pattern.

        Digit patterns are used to bypass permissions.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches with the digit pattern.
        :type action: CallingPermissionAction
        :param transfer_enabled: Option to allow or disallow transfer of calls.
        :type transfer_enabled: bool
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
        if name is not None:
            body['name'] = name
        if pattern is not None:
            body['pattern'] = pattern
        if action is not None:
            body['action'] = enum_str(action)
        if transfer_enabled is not None:
            body['transferEnabled'] = transfer_enabled
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().put(url, params=params, json=body)

    def delete_a_digit_pattern_for_the_workspace(self, workspace_id: str, digit_pattern_id: str, org_id: str = None):
        """
        Delete a Digit Pattern for the Workspace

        Delete Digit Pattern for a Workspace.

        Digit patterns are used to bypass permissions.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().delete(url, params=params)

    def delete_all_digit_patterns_for_a_workspace(self, workspace_id: str, org_id: str = None):
        """
        Delete all Digit Patterns for a Workspace.

        Digit patterns are used to bypass permissions.

        This API requires a full or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

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
        url = self.ep(f'telephony/config/workspaces/{workspace_id}/outgoingPermission/digitPatterns')
        super().delete(url, params=params)

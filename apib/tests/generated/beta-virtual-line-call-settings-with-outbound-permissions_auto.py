from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AuthorizationCode', 'AuthorizationCodeLevel', 'BetaVirtualLineCallSettingsWithOutboundPermissionsApi',
           'TransferNumberGet', 'UserDigitPatternObject', 'UserOutgoingPermissionDigitPatternGetListObject',
           'UserOutgoingPermissionDigitPatternPostObjectAction', 'UserPlaceAuthorizationCodeListGet']


class AuthorizationCodeLevel(str, Enum):
    #: Indicates the location level access code.
    location = 'LOCATION'
    #: Indicates the user level access code.
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
    #: When `true`, use custom settings for the access codes category of outbound permissions.
    use_custom_access_codes: Optional[bool] = None
    #: Indicates the set of activation codes and description.
    access_codes: Optional[list[AuthorizationCode]] = None


class TransferNumberGet(ApiModel):
    #: When `true`, use custom settings for the transfer numbers category of outbound permissions.
    #: example: True
    use_custom_transfer_numbers: Optional[bool] = None
    #: When calling a specific call type, this virtual line will be automatically transferred to another number.
    #: `autoTransferNumber1` will be used when the associated calling permission action is set to `TRANSFER_NUMBER_1`.
    #: example: "+1205553650"
    auto_transfer_number1: Optional[str] = None
    #: When calling a specific call type, this virtual line will be automatically transferred to another number.
    #: `autoTransferNumber2` will be used when the associated calling permission action is set to `TRANSFER_NUMBER_2`.
    #: example: "+1205553651"
    auto_transfer_number2: Optional[str] = None
    #: When calling a specific call type, this virtual line will be automatically transferred to another number.
    #: `autoTransferNumber3` will be used when the associated calling permission action is set to `TRANSFER_NUMBER_3`.
    #: example: "+1205553652"
    auto_transfer_number3: Optional[str] = None


class UserOutgoingPermissionDigitPatternPostObjectAction(str, Enum):
    #: Allow the designated call type.
    allow = 'ALLOW'
    #: Block the designated call type.
    block = 'BLOCK'
    #: Allow only via Authorization Code.
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


class UserDigitPatternObject(ApiModel):
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
    action: Optional[UserOutgoingPermissionDigitPatternPostObjectAction] = None
    #: Option to allow or disallow transfer of calls.
    #: example: True
    transfer_enabled: Optional[bool] = None


class UserOutgoingPermissionDigitPatternGetListObject(ApiModel):
    #: When `true`, use custom settings for the digit patterns category of outgoing call permissions.
    use_custom_digit_patterns: Optional[bool] = None
    #: List of digit patterns.
    digit_patterns: Optional[list[UserDigitPatternObject]] = None


class BetaVirtualLineCallSettingsWithOutboundPermissionsApi(ApiChild, base='telephony/config/virtualLines'):
    """
    Beta Virtual Line Call Settings with Outbound Permissions
    
    Virtual Line Call Settings supports modifying Webex Calling settings for a Virtual Line.
    
    Viewing a virtual line requires a full, user or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read.
    """

    def retrieve_access_codes_for_a_virtual_line(self, virtual_line_id: str,
                                                 org_id: str = None) -> UserPlaceAuthorizationCodeListGet:
        """
        Retrieve Access Codes for a Virtual Line

        Retrieve the virtual line's access codes.

        Access codes are used to bypass permissions.

        This API requires a full, user or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`UserPlaceAuthorizationCodeListGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/accessCodes')
        data = super().get(url, params=params)
        r = UserPlaceAuthorizationCodeListGet.model_validate(data)
        return r

    def modify_access_codes_for_a_virtual_line(self, virtual_line_id: str, use_custom_access_codes: bool = None,
                                               delete_codes: list[str] = None, org_id: str = None):
        """
        Modify Access Codes for a Virtual Line

        Modify a virtual line's access codes.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param use_custom_access_codes: When `true`, use custom settings for the access codes category of outbound
            permissions.
        :type use_custom_access_codes: bool
        :param delete_codes: Indicates access codes to delete.
        :type delete_codes: list[str]
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
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
        url = self.ep(f'{virtual_line_id}/outgoingPermission/accessCodes')
        super().put(url, params=params, json=body)

    def create_access_codes_for_a_virtual_line(self, virtual_line_id: str, code: str, description: str,
                                               org_id: str = None):
        """
        Create Access Codes for a Virtual Line

        Create new Access codes for the virtual line.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param code: Indicates an access code.
        :type code: str
        :param description: Indicates the description of the access code.
        :type description: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
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
        url = self.ep(f'{virtual_line_id}/outgoingPermission/accessCodes')
        super().post(url, params=params, json=body)

    def delete_access_codes_for_a_virtual_line(self, virtual_line_id: str, org_id: str = None):
        """
        Delete Access Codes for a Virtual Line

        Deletes all Access codes for the virtual line.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/accessCodes')
        super().delete(url, params=params)

    def retrieve_transfer_numbers_for_a_virtual_line(self, virtual_line_id: str,
                                                     org_id: str = None) -> TransferNumberGet:
        """
        Retrieve Transfer Numbers for a Virtual Line

        Retrieve the virtual line's transfer numbers.

        When calling a specific call type, this virtual line will be automatically transferred to another number. The
        virtual line assigned to the Auto Transfer Number can then approve the call and send it through or reject the
        call type. You can add up to 3 numbers.

        This API requires a full, user or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: :class:`TransferNumberGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/autoTransferNumbers')
        data = super().get(url, params=params)
        r = TransferNumberGet.model_validate(data)
        return r

    def modify_transfer_numbers_for_a_virtual_line(self, virtual_line_id: str,
                                                   use_custom_transfer_numbers: bool = None,
                                                   auto_transfer_number1: str = None,
                                                   auto_transfer_number2: str = None,
                                                   auto_transfer_number3: str = None, org_id: str = None):
        """
        Modify Transfer Numbers for a Virtual Line

        Modify a virtual line's transfer numbers.

        When calling a specific call type, this virtual line will be automatically transferred to another number. The
        virtual line assigned the Auto Transfer Number can then approve the call and send it through or reject the
        call type. You can add up to 3 numbers.

        This API requires a full or user administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param use_custom_transfer_numbers: When `true`, use custom settings for the transfer numbers category of
            outbound permissions.
        :type use_custom_transfer_numbers: bool
        :param auto_transfer_number1: When calling a specific call type, this virtual line will be automatically
            transferred to another number. `autoTransferNumber1` will be used when the associated calling permission
            action is set to `TRANSFER_NUMBER_1`.
        :type auto_transfer_number1: str
        :param auto_transfer_number2: When calling a specific call type, this virtual line will be automatically
            transferred to another number. `autoTransferNumber2` will be used when the associated calling permission
            action is set to `TRANSFER_NUMBER_2`.
        :type auto_transfer_number2: str
        :param auto_transfer_number3: When calling a specific call type, this virtual line will be automatically
            transferred to another number. `autoTransferNumber3` will be used when the associated calling permission
            action is set to `TRANSFER_NUMBER_3`.
        :type auto_transfer_number3: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if use_custom_transfer_numbers is not None:
            body['useCustomTransferNumbers'] = use_custom_transfer_numbers
        if auto_transfer_number1 is not None:
            body['autoTransferNumber1'] = auto_transfer_number1
        if auto_transfer_number2 is not None:
            body['autoTransferNumber2'] = auto_transfer_number2
        if auto_transfer_number3 is not None:
            body['autoTransferNumber3'] = auto_transfer_number3
        url = self.ep(f'{virtual_line_id}/outgoingPermission/autoTransferNumbers')
        super().put(url, params=params, json=body)

    def retrieve_digit_patterns_for_a_virtual_profile(self, virtual_line_id: str,
                                                      org_id: str = None) -> UserOutgoingPermissionDigitPatternGetListObject:
        """
        Retrieve Digit Patterns for a Virtual Profile

        Get list of digit patterns for the virtual profile.

        Digit patterns are used to bypass permissions.

        Retrieving this list requires a full, user or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`UserOutgoingPermissionDigitPatternGetListObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns')
        data = super().get(url, params=params)
        r = UserOutgoingPermissionDigitPatternGetListObject.model_validate(data)
        return r

    def retrieve_specified_digit_pattern_details_for_a_virtual_profile(self, virtual_line_id: str,
                                                                       digit_pattern_id: str,
                                                                       org_id: str = None) -> UserDigitPatternObject:
        """
        Retrieve Specified Digit Pattern Details for a Virtual Profile

        Get the specified digit pattern for the virtual profile​.

        Digit patterns are used to bypass permissions.

        Retrieving the digit pattern details requires a full, user or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`UserDigitPatternObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        data = super().get(url, params=params)
        r = UserDigitPatternObject.model_validate(data)
        return r

    def create_digit_pattern_for_a_virtual_profile(self, virtual_line_id: str, name: str, pattern: str,
                                                   action: UserOutgoingPermissionDigitPatternPostObjectAction,
                                                   transfer_enabled: bool, org_id: str = None) -> str:
        """
        Create Digit Pattern for a Virtual Profile

        Create new digit pattern for a virtual profile.

        Digit patterns are used to bypass permissions.

        Creating the digit pattern requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches with the digit pattern.
        :type action: UserOutgoingPermissionDigitPatternPostObjectAction
        :param transfer_enabled: Option to allow or disallow transfer of calls.
        :type transfer_enabled: bool
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_the_digit_pattern_category_control_settings_for_the_virtual_profile(self, virtual_line_id: str,
                                                                                   use_custom_digit_patterns: bool = None,
                                                                                   org_id: str = None):
        """
        Modify the Digit Pattern Category Control Settings for the Virtual Profile

        Modifies whether this virtual profile uses the specified digit patterns when placing outbound calls or not.

        Updating the digit pattern category control settings requires a full or user or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param use_custom_digit_patterns: When `true`, use custom settings for the digit patterns category of outgoing
            call permissions.
        :type use_custom_digit_patterns: bool
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if use_custom_digit_patterns is not None:
            body['useCustomDigitPatterns'] = use_custom_digit_patterns
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns')
        super().put(url, params=params, json=body)

    def modify_a_digit_pattern_for_the_virtual_profile(self, virtual_line_id: str, digit_pattern_id: str,
                                                       name: str = None, pattern: str = None,
                                                       action: UserOutgoingPermissionDigitPatternPostObjectAction = None,
                                                       transfer_enabled: bool = None, org_id: str = None):
        """
        Modify a Digit Pattern for the Virtual Profile

        Modify digit patterns for a virtual profile.

        Digit patterns are used to bypass permissions.

        Updating the digit pattern requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches with the digit pattern.
        :type action: UserOutgoingPermissionDigitPatternPostObjectAction
        :param transfer_enabled: Option to allow or disallow transfer of calls.
        :type transfer_enabled: bool
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().put(url, params=params, json=body)

    def delete_a_digit_pattern_for_the_virtual_profile(self, virtual_line_id: str, digit_pattern_id: str,
                                                       org_id: str = None):
        """
        Delete a Digit Pattern for the Virtual Profile

        Delete digit pattern for a virtual profile.

        Digit patterns are used to bypass permissions.

        Deleting the digit pattern requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().delete(url, params=params)

    def delete_all_digit_patterns_for_a_virtual_profile(self, virtual_line_id: str, org_id: str = None):
        """
        Delete all digit patterns for a virtual profile.

        Digit patterns are used to bypass permissions.

        Deleting the digit patterns requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission/digitPatterns')
        super().delete(url, params=params)

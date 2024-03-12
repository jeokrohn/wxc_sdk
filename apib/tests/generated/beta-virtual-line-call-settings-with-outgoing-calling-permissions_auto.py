from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaVirtualLineCallSettingsWithOutgoingCallingPermissionsApi', 'OutgoingCallingPermissionsSettingGet',
           'OutgoingCallingPermissionsSettingGetCallingPermissions',
           'OutgoingCallingPermissionsSettingGetCallingPermissionsAction',
           'OutgoingCallingPermissionsSettingGetCallingPermissionsCallType']


class OutgoingCallingPermissionsSettingGetCallingPermissionsCallType(str, Enum):
    #: Controls calls within your own company.
    internal_call = 'INTERNAL_CALL'
    #: Controls calls to a telephone number that is billed for all arriving calls instead of incurring charges to the
    #: originating caller, usually free of charge from a landline.
    toll_free = 'TOLL_FREE'
    #: Controls calls to locations outside of the Long Distance areas that require an international calling code before
    #: the number is dialed.
    international = 'INTERNATIONAL'
    #: Controls calls requiring Operator Assistance.
    operator_assisted = 'OPERATOR_ASSISTED'
    #: Controls calls to Directory Assistant companies that require a charge to connect the call.
    chargeable_directory_assisted = 'CHARGEABLE_DIRECTORY_ASSISTED'
    #: Controls calls to carrier-specific number assignments to special services or destinations.
    special_services_i = 'SPECIAL_SERVICES_I'
    #: Controls calls to carrier-specific number assignments to special services or destinations.
    special_services_ii = 'SPECIAL_SERVICES_II'
    #: Controls calls used to provide information or entertainment for a fee charged directly to the caller.
    premium_services_i = 'PREMIUM_SERVICES_I'
    #: Controls calls used to provide information or entertainment for a fee charged directly to the caller.
    premium_services_ii = 'PREMIUM_SERVICES_II'
    #: Controls calls that are within your country of origin, both within and outside of your local area code.
    national = 'NATIONAL'


class OutgoingCallingPermissionsSettingGetCallingPermissionsAction(str, Enum):
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


class OutgoingCallingPermissionsSettingGetCallingPermissions(ApiModel):
    #: Designates the action to be taken for each call type and if transferring the call type is allowed.
    #: example: INTERNAL_CALL
    call_type: Optional[OutgoingCallingPermissionsSettingGetCallingPermissionsCallType] = None
    #: Action on the given `callType`.
    #: example: ALLOW
    action: Optional[OutgoingCallingPermissionsSettingGetCallingPermissionsAction] = None
    #: Allow the person to transfer or forward a call of the specified call type.
    transfer_enabled: Optional[bool] = None


class OutgoingCallingPermissionsSettingGet(ApiModel):
    #: When true, indicates that this user uses the shared control that applies to all outgoing call settings
    #: categories when placing outbound calls.
    #: example: True
    use_custom_enabled: Optional[bool] = None
    #: When true, indicates that this user uses the specified outgoing calling permissions when placing outbound calls.
    #: example: True
    use_custom_permissions: Optional[bool] = None
    #: Specifies the outbound calling permissions settings.
    calling_permissions: Optional[list[OutgoingCallingPermissionsSettingGetCallingPermissions]] = None


class BetaVirtualLineCallSettingsWithOutgoingCallingPermissionsApi(ApiChild, base='telephony/config/virtualLines'):
    """
    Beta Virtual Line Call Settings with Outgoing Calling Permissions
    
    Virtual Line Call Settings supports modifying Webex Calling settings for a Virtual Line.
    
    Viewing a virtual line requires a full, user, or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read.
    """

    def retrieve_outgoing_calling_permissions_settings_for_a_virtual_line(self, virtual_line_id: str,
                                                                          org_id: str = None) -> OutgoingCallingPermissionsSettingGet:
        """
        Retrieve Outgoing Calling Permissions Settings for a Virtual Line

        Retrieve the customer virtual profile's outgoing calling permissions settings.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`OutgoingCallingPermissionsSettingGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/outgoingPermission')
        data = super().get(url, params=params)
        r = OutgoingCallingPermissionsSettingGet.model_validate(data)
        return r

    def modify_outgoing_calling_permissions_settings_for_a_virtual_line(self, virtual_line_id: str,
                                                                        calling_permissions: list[OutgoingCallingPermissionsSettingGetCallingPermissions],
                                                                        use_custom_enabled: bool = None,
                                                                        use_custom_permissions: bool = None,
                                                                        org_id: str = None):
        """
        Modify Outgoing Calling Permissions Settings for a Virtual Line

        Modify a customer virtual profile's outgoing calling permissions settings.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Updating a virtual line requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param calling_permissions: Specifies the outbound calling permissions settings.
        :type calling_permissions: list[OutgoingCallingPermissionsSettingGetCallingPermissions]
        :param use_custom_enabled: When true, indicates that this user uses the shared control that applies to all
            outgoing call settings categories when placing outbound calls.
        :type use_custom_enabled: bool
        :param use_custom_permissions: When true, indicates that this user uses the specified outgoing calling
            permissions when placing outbound calls.
        :type use_custom_permissions: bool
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
        if use_custom_enabled is not None:
            body['useCustomEnabled'] = use_custom_enabled
        if use_custom_permissions is not None:
            body['useCustomPermissions'] = use_custom_permissions
        body['callingPermissions'] = TypeAdapter(list[OutgoingCallingPermissionsSettingGetCallingPermissions]).dump_python(calling_permissions, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{virtual_line_id}/outgoingPermission')
        super().put(url, params=params, json=body)

from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CallingPermissionObject', 'CallingPermissionObjectAction', 'CallingPermissionObjectCallType',
           'CallingPermissionPatchObject', 'GetAutoTransferNumberObject', 'GetLocationAccessCodeObjectAccessCodes',
           'GetLocationInterceptObject', 'GetLocationInterceptObjectIncoming',
           'GetLocationInterceptObjectIncomingAnnouncements',
           'GetLocationInterceptObjectIncomingAnnouncementsGreeting',
           'GetLocationInterceptObjectIncomingAnnouncementsNewNumber', 'GetLocationInterceptObjectIncomingType',
           'GetLocationInterceptObjectOutgoing', 'GetLocationInterceptObjectOutgoingType', 'InternalDialingGet',
           'LocationCallSettingsCallHandlingApi', 'LocationDigitPatternObject', 'PasswordGenerate', 'RouteIdentity',
           'RouteType', 'UnknownExtensionRouteIdentity']


class CallingPermissionObjectCallType(str, Enum):
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
    #: Controls calls that are National.
    national = 'NATIONAL'


class CallingPermissionObjectAction(str, Enum):
    #: Callers at this location can make these types of calls.
    allow = 'ALLOW'
    #: Callers at this location can't make these types of calls.
    block = 'BLOCK'
    #: Callers must enter the authorization code that you set before placing an outgoing call.
    auth_code = 'AUTH_CODE'
    #: Calls are transferred automatically to the configured auto transfer number `autoTransferNumber1`.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: Calls are transferred automatically to the configured auto transfer number. `autoTransferNumber2`.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: Calls are transferred automatically to the configured auto transfer number. `autoTransferNumber3`.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class CallingPermissionObject(ApiModel):
    #: Below are the call type values.
    call_type: Optional[CallingPermissionObjectCallType] = None
    #: Allows to configure settings for each call type.
    action: Optional[CallingPermissionObjectAction] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None
    #: Indicates if the restriction is enforced by the system for the corresponding call type and cannot be changed.
    #: For example, certain call types (such as `INTERNATIONAL`) may be permanently blocked and this field will be
    #: `true` to reflect that the restriction is system-controlled and not editable.
    is_call_type_restriction_enabled: Optional[bool] = None


class CallingPermissionPatchObject(ApiModel):
    #: Below are the call type values.
    call_type: Optional[CallingPermissionObjectCallType] = None
    #: Allows to configure settings for each call type.
    action: Optional[CallingPermissionObjectAction] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None


class GetAutoTransferNumberObject(ApiModel):
    #: Calls placed meeting the criteria in an outbound rule whose `action` is `TRANSFER_NUMBER_1` will be transferred
    #: to this number.
    auto_transfer_number1: Optional[str] = None
    #: Calls placed meeting the criteria in an outbound rule whose `action` is `TRANSFER_NUMBER_2` will be transferred
    #: to this number.
    auto_transfer_number2: Optional[str] = None
    #: Calls placed meeting the criteria in an outbound rule whose `action` is `TRANSFER_NUMBER_3` will be transferred
    #: to this number.
    auto_transfer_number3: Optional[str] = None


class GetLocationAccessCodeObjectAccessCodes(ApiModel):
    #: Access code number.
    code: Optional[str] = None
    #: Access code description.
    description: Optional[str] = None


class GetLocationInterceptObjectIncomingType(str, Enum):
    #: Intercept all inbound calls.
    intercept_all = 'INTERCEPT_ALL'
    #: Allow all inbound calls.
    allow_all = 'ALLOW_ALL'


class GetLocationInterceptObjectIncomingAnnouncementsGreeting(str, Enum):
    #: Play default greeting.
    default = 'DEFAULT'
    #: Play custom greeting.
    custom = 'CUSTOM'


class GetLocationInterceptObjectIncomingAnnouncementsNewNumber(ApiModel):
    #: Enable/disable to play new number announcement.
    enabled: Optional[bool] = None
    #: Incoming destination phone number to be announced.
    destination: Optional[str] = None


class GetLocationInterceptObjectIncomingAnnouncements(ApiModel):
    #: Greeting type for location intercept.
    greeting: Optional[GetLocationInterceptObjectIncomingAnnouncementsGreeting] = None
    #: If set to `CUSTOM` for greeting, filename of previously uploaded file.
    file_name: Optional[str] = None
    #: Settings for new number announcement.
    new_number: Optional[GetLocationInterceptObjectIncomingAnnouncementsNewNumber] = None
    #: Transfer number details.
    zero_transfer: Optional[GetLocationInterceptObjectIncomingAnnouncementsNewNumber] = None


class GetLocationInterceptObjectIncoming(ApiModel):
    #: Select inbound call options.
    type: Optional[GetLocationInterceptObjectIncomingType] = None
    #: Enable/disable to route voice mail.
    voicemail_enabled: Optional[bool] = None
    #: Announcements details.
    announcements: Optional[GetLocationInterceptObjectIncomingAnnouncements] = None


class GetLocationInterceptObjectOutgoingType(str, Enum):
    #: Intercept all outbound calls.
    intercept_all = 'INTERCEPT_ALL'
    #: Allow local outbound calls.
    allow_local_only = 'ALLOW_LOCAL_ONLY'


class GetLocationInterceptObjectOutgoing(ApiModel):
    #: Outbound call modes
    type: Optional[GetLocationInterceptObjectOutgoingType] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None
    #: If enabled, set outgoing destination phone number.
    destination: Optional[str] = None


class GetLocationInterceptObject(ApiModel):
    #: Enable/disable location intercept. Enable this feature to override any Location's Call Intercept settings that
    #: person configures.
    enabled: Optional[bool] = None
    #: Inbound call details.
    incoming: Optional[GetLocationInterceptObjectIncoming] = None
    #: Outbound Call details
    outgoing: Optional[GetLocationInterceptObjectOutgoing] = None


class RouteType(str, Enum):
    #: Route group must include at least one trunk with a maximum of 10 trunks per route group.
    route_group = 'ROUTE_GROUP'
    #: Connection between Webex Calling and the premises.
    trunk = 'TRUNK'


class RouteIdentity(ApiModel):
    #: ID of the route type.
    id: Optional[str] = None
    #: A unique name for the route identity.
    name: Optional[str] = None
    #: Type associated with the identity.
    type: Optional[RouteType] = None


class InternalDialingGet(ApiModel):
    #: When enabled, calls made by users at the location to an unknown extension (between 2-6 digits) are routed to the
    #: selected route group/trunk as premises calls.
    enable_unknown_extension_route_policy: Optional[bool] = None
    #: The selected route group/trunk as premises calls.
    unknown_extension_route_identity: Optional[RouteIdentity] = None


class UnknownExtensionRouteIdentity(ApiModel):
    #: ID of the route type.
    id: Optional[str] = None
    #: Type associated with the identity.
    type: Optional[RouteType] = None


class LocationDigitPatternObject(ApiModel):
    #: A unique identifier for the digit pattern.
    id: Optional[str] = None
    #: A unique name for the digit pattern.
    name: Optional[str] = None
    #: The digit pattern to be matched with the input number.
    pattern: Optional[str] = None
    #: Action to be performed on the input number that matches the digit pattern.
    action: Optional[CallingPermissionObjectAction] = None
    #: If `true`, allows transfer and forwarding for the call type.
    transfer_enabled: Optional[bool] = None


class PasswordGenerate(str, Enum):
    #: SIP password setting
    sip = 'sip'


class LocationCallSettingsCallHandlingApi(ApiChild, base='telephony/config/locations'):
    """
    Location Call Settings: Call Handling
    
    Location Call Settings: Call Handling supports reading and writing of Webex
    Calling Location settings involving permissions and intercepting of inbound and
    outbound calls for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def generate_example_password_for_location(self, location_id: str, generate: list[PasswordGenerate] = None,
                                               org_id: str = None) -> str:
        """
        Generate example password for Location

        Generates an example password using the effective password settings for the location. If you don't specify
        anything in the `generate` field or don't provide a request body, then you will receive a SIP password by
        default.

        Used while creating a trunk and shouldn't be used anywhere else.

        Generating an example password requires a full or write-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location for which example password has to be generated.
        :type location_id: str
        :param generate: password settings array.
        :type generate: list[PasswordGenerate]
        :param org_id: Organization to which the location belongs.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if generate is not None:
            body['generate'] = TypeAdapter(list[PasswordGenerate]).dump_python(generate, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{location_id}/actions/generatePassword/invoke')
        data = super().post(url, params=params, json=body)
        r = data['exampleSipPassword']
        return r

    def get_location_intercept(self, location_id: str, org_id: str = None) -> GetLocationInterceptObject:
        """
        Get Location Intercept

        Retrieve intercept location details for a customer location.

        Intercept incoming or outgoing calls for persons in your organization. If this is enabled, calls are either
        routed to a designated number the person chooses, or to the person's voicemail.

        Retrieving intercept location details requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve intercept details for this location.
        :type location_id: str
        :param org_id: Retrieve intercept location details for a customer location.
        :type org_id: str
        :rtype: :class:`GetLocationInterceptObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/intercept')
        data = super().get(url, params=params)
        r = GetLocationInterceptObject.model_validate(data)
        return r

    def put_location_intercept(self, location_id: str, enabled: bool,
                               incoming: GetLocationInterceptObjectIncoming = None,
                               outgoing: GetLocationInterceptObjectOutgoing = None, org_id: str = None):
        """
        Put Location Intercept

        Modifies the intercept location details for a customer location.

        Intercept incoming or outgoing calls for users in your organization. If this is enabled, calls are either
        routed to a designated number the user chooses, or to the user's voicemail.

        Modifying the intercept location details requires a full, user administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Modifies the intercept details for this location.
        :type location_id: str
        :param enabled: Enable/disable location intercept. Enable this feature to override any location's Call
            Intercept settings that a person configures.
        :type enabled: bool
        :param incoming: Inbound call details.
        :type incoming: GetLocationInterceptObjectIncoming
        :param outgoing: Outbound Call details
        :type outgoing: GetLocationInterceptObjectOutgoing
        :param org_id: Modifies the intercept location details for a customer location.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        if incoming is not None:
            body['incoming'] = incoming.model_dump(mode='json', by_alias=True, exclude_none=True)
        if outgoing is not None:
            body['outgoing'] = outgoing.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{location_id}/intercept')
        super().put(url, params=params, json=body)

    def read_the_internal_dialing_configuration_for_a_location(self, location_id: str,
                                                               org_id: str = None) -> InternalDialingGet:
        """
        Read the Internal Dialing configuration for a location

        Get current configuration for routing unknown extensions to the Premises as internal calls

        If some users in a location are registered to a PBX, retrieve the setting to route unknown extensions (digits
        that match the extension length) to the PBX.

        Retrieving the internal dialing configuration requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: location for which internal calling configuration is being requested
        :type location_id: str
        :param org_id: List route identities for this organization.
        :type org_id: str
        :rtype: :class:`InternalDialingGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/internalDialing')
        data = super().get(url, params=params)
        r = InternalDialingGet.model_validate(data)
        return r

    def modify_the_internal_dialing_configuration_for_a_location(self, location_id: str,
                                                                 enable_unknown_extension_route_policy: bool = None,
                                                                 unknown_extension_route_identity: UnknownExtensionRouteIdentity = None,
                                                                 org_id: str = None):
        """
        Modify the Internal Dialing configuration for a location

        Modify current configuration for routing unknown extensions to the premise as internal calls

        If some users in a location are registered to a PBX, enable the setting to route unknown extensions (digits
        that match the extension length) to the PBX.

        Editing the internal dialing configuration requires a full administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param location_id: location for which internal calling configuration is being requested
        :type location_id: str
        :param enable_unknown_extension_route_policy: When enabled, calls made by users at the location to an unknown
            extension (between 2-6 digits) are routed to the selected route group/trunk as premises calls.
        :type enable_unknown_extension_route_policy: bool
        :param unknown_extension_route_identity: Type associated with the identity.
        :type unknown_extension_route_identity: UnknownExtensionRouteIdentity
        :param org_id: List route identities for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if enable_unknown_extension_route_policy is not None:
            body['enableUnknownExtensionRoutePolicy'] = enable_unknown_extension_route_policy
        if unknown_extension_route_identity is not None:
            body['unknownExtensionRouteIdentity'] = unknown_extension_route_identity.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{location_id}/internalDialing')
        super().put(url, params=params, json=body)

    def get_location_outgoing_permission(self, location_id: str, org_id: str = None) -> list[CallingPermissionObject]:
        """
        Get Location Outgoing Permission

        Retrieve the location's outgoing call settings.

        A location's outgoing call settings allow you to determine the types of calls the people/workspaces at the
        location are allowed to make, as well as configure the default calling permission for each call type at the
        location.

        Retrieving a location's outgoing call settings requires a full, user or read-only administrator or location
        administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve outgoing call settings for this location.
        :type location_id: str
        :param org_id: Retrieve outgoing call settings for this organization.
        :type org_id: str
        :rtype: list[CallingPermissionObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission')
        data = super().get(url, params=params)
        r = TypeAdapter(list[CallingPermissionObject]).validate_python(data['callingPermissions'])
        return r

    def update_location_outgoing_permission(self, location_id: str,
                                            calling_permissions: list[CallingPermissionPatchObject] = None,
                                            org_id: str = None):
        """
        Update Location Outgoing Permission

        Update the location's outgoing call settings.

        Location's outgoing call settings allows you to determine the types of calls the people/workspaces at this
        location are allowed to make and configure the default calling permission for each call type at a location.

        Updating a location's outgoing call settings requires a full administrator or location administrator auth token
        with a scope of spark-admin:telephony_config_write.

        :param location_id: Update outgoing call settings for this location.
        :type location_id: str
        :param calling_permissions: Array specifying the subset of calling permissions to be updated.
        :type calling_permissions: list[CallingPermissionPatchObject]
        :param org_id: Update outgoing call settings for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if calling_permissions is not None:
            body['callingPermissions'] = TypeAdapter(list[CallingPermissionPatchObject]).dump_python(calling_permissions, mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{location_id}/outgoingPermission')
        super().put(url, params=params, json=body)

    def delete_all_outgoing_permission_access_code_for_a_location(self, location_id: str, org_id: str = None):
        """
        Delete all Outgoing Permission Access Code for a Location

        Deletes all the access codes for a particular location for a customer.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Deleting the access codes requires a full or user administrator or location administrator auth token with the
        `spark-admin:telephony_config_write` scope.

        :param location_id: Deletes all the access codes for this location.
        :type location_id: str
        :param org_id: Deletes the access codes for a customer location.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission/accessCodes')
        super().delete(url, params=params)

    def get_outgoing_permission_location_access_code(self, location_id: str,
                                                     org_id: str = None) -> GetLocationAccessCodeObjectAccessCodes:
        """
        Get Outgoing Permission Location Access Code

        Retrieve access codes details for a customer location.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Retrieving access codes details requires a full, user or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param org_id: Retrieve access codes details for a customer location.
        :type org_id: str
        :rtype: GetLocationAccessCodeObjectAccessCodes
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission/accessCodes')
        data = super().get(url, params=params)
        r = GetLocationAccessCodeObjectAccessCodes.model_validate(data['accessCodes'])
        return r

    def create_outgoing_permission_a_new_access_code_for_a_customer_location(self, location_id: str,
                                                                             access_codes: GetLocationAccessCodeObjectAccessCodes = None,
                                                                             org_id: str = None):
        """
        Create Outgoing Permission a new access code for a customer location

        Add a new access code for the given location for a customer.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Creating an access code for the given location requires a full or user administrator or location administrator
        auth token with a scope of spark-admin:telephony_config_write.

        :param location_id: Add new access code for this location.
        :type location_id: str
        :param access_codes: Access code details
        :type access_codes: GetLocationAccessCodeObjectAccessCodes
        :param org_id: Add new access code for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if access_codes is not None:
            body['accessCodes'] = access_codes.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'{location_id}/outgoingPermission/accessCodes')
        super().post(url, params=params, json=body)

    def delete_outgoing_permission_access_code_location(self, location_id: str, delete_codes: list[str],
                                                        org_id: str = None):
        """
        Delete Outgoing Permission Access Code Location

        Deletes the access code details for a particular location for a customer.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Modifying the access code location details requires a full administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Deletes the access code details for this location.
        :type location_id: str
        :param delete_codes: Array of string to delete access codes. For example, ["1234","2345"]
        :type delete_codes: list[str]
        :param org_id: Deletes the access code details for a customer location.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['deleteCodes'] = delete_codes
        url = self.ep(f'{location_id}/outgoingPermission/accessCodes')
        super().put(url, params=params, json=body)

    def get_outgoing_permission_auto_transfer_number(self, location_id: str,
                                                     org_id: str = None) -> GetAutoTransferNumberObject:
        """
        Get Outgoing Permission Auto Transfer Number

        Get the transfer numbers for the outbound permission in a location.

        Outbound permissions can specify which transfer number an outbound call should transfer to via the `action`
        field.

        Retrieving an auto transfer number requires a full, user or read-only administrator or location administrator
        auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve auto transfer number for this location.
        :type location_id: str
        :param org_id: Retrieve auto transfer number for this organization.
        :type org_id: str
        :rtype: :class:`GetAutoTransferNumberObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission/autoTransferNumbers')
        data = super().get(url, params=params)
        r = GetAutoTransferNumberObject.model_validate(data)
        return r

    def put_outgoing_permission_auto_transfer_number(self, location_id: str, auto_transfer_number1: str = None,
                                                     auto_transfer_number2: str = None,
                                                     auto_transfer_number3: str = None, org_id: str = None):
        """
        Put Outgoing Permission Auto Transfer Number

        Modifies the transfer numbers for the outbound permission in a location.

        Outbound permissions can specify which transfer number an outbound call should transfer to via the `action`
        field.

        Updating auto transfer number requires a full administrator or location administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param location_id: Updating auto transfer number for this location.
        :type location_id: str
        :param auto_transfer_number1: Calls placed meeting the criteria in an outbound rule whose `action` is
            `TRANSFER_NUMBER_1` will be transferred to this number.
        :type auto_transfer_number1: str
        :param auto_transfer_number2: Calls placed meeting the criteria in an outbound rule whose `action` is
            `TRANSFER_NUMBER_2` will be transferred to this number.
        :type auto_transfer_number2: str
        :param auto_transfer_number3: Calls placed meeting the criteria in an outbound rule whose `action` is
            `TRANSFER_NUMBER_3` will be transferred to this number.
        :type auto_transfer_number3: str
        :param org_id: Updating auto transfer number for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if auto_transfer_number1 is not None:
            body['autoTransferNumber1'] = auto_transfer_number1
        if auto_transfer_number2 is not None:
            body['autoTransferNumber2'] = auto_transfer_number2
        if auto_transfer_number3 is not None:
            body['autoTransferNumber3'] = auto_transfer_number3
        url = self.ep(f'{location_id}/outgoingPermission/autoTransferNumbers')
        super().put(url, params=params, json=body)

    def delete_all_outgoing_permission_digit_patterns_for_a_location(self, location_id: str, org_id: str = None):
        """
        Delete all Outgoing Permission Digit Patterns for a Location

        Deletes all the digit patterns for a particular location for a customer.

        Use Digit Patterns to bypass the set permissions for all persons/workspaces at this location.

        Deleting the digit patterns requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Delete the digit patterns for this location.
        :type location_id: str
        :param org_id: Delete the digit patterns for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission/digitPatterns')
        super().delete(url, params=params)

    def get_outgoing_permission_digit_pattern_for_a_location(self, location_id: str,
                                                             org_id: str = None) -> list[LocationDigitPatternObject]:
        """
        Get Outgoing Permission Digit Pattern for a Location

        Get the digit patterns for the outbound permission in a location.

        Use Digit Patterns to bypass the set permissions for all persons/workspaces at this location.

        Retrieving digit patterns requires a full or read-only administrator or location administrator auth token with
        a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve the digit patterns for this location.
        :type location_id: str
        :param org_id: Retrieve the digit patterns for this organization.
        :type org_id: str
        :rtype: list[LocationDigitPatternObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission/digitPatterns')
        data = super().get(url, params=params)
        r = TypeAdapter(list[LocationDigitPatternObject]).validate_python(data['digitPatterns'])
        return r

    def create_outgoing_permission_a_new_digit_pattern_for_a_location(self, location_id: str, name: str, pattern: str,
                                                                      action: CallingPermissionObjectAction,
                                                                      transfer_enabled: bool,
                                                                      org_id: str = None) -> str:
        """
        Create Outgoing Permission a new Digit Pattern for a location

        Add a new digit pattern for the given location for a customer.

        Use Digit Patterns to bypass the set permissions for all persons/workspaces at this location.

        Creating a digit pattern requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Add a new digit pattern for this location.
        :type location_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches the digit pattern.
        :type action: CallingPermissionObjectAction
        :param transfer_enabled: If `true`, allows transfer and forwarding for the call type.
        :type transfer_enabled: bool
        :param org_id: Add a new digit pattern for this organization.
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
        url = self.ep(f'{location_id}/outgoingPermission/digitPatterns')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete_a_outgoing_permission_digit_pattern_for_a_location(self, location_id: str, digit_pattern_id: str,
                                                                  org_id: str = None):
        """
        Delete a Outgoing Permission Digit Pattern for a Location

        Delete the designated digit pattern.

        Use Digit Patterns to bypass the set permissions for all persons/workspaces at this location.

        Deleting a digit pattern requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Delete the digit pattern for this location.
        :type location_id: str
        :param digit_pattern_id: Delete the digit pattern with the matching ID.
        :type digit_pattern_id: str
        :param org_id: Delete the digit pattern for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().delete(url, params=params)

    def get_details_for_a_outgoing_permission_digit_pattern_for_a_location(self, location_id: str,
                                                                           digit_pattern_id: str,
                                                                           org_id: str = None) -> LocationDigitPatternObject:
        """
        Get Details for a Outgoing Permission Digit Pattern for a Location

        Get the digit pattern details.

        Use Digit Patterns to bypass the set permissions for all persons/workspaces at this location.

        Retrieving digit pattern details requires a full or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve the digit pattern details for this location.
        :type location_id: str
        :param digit_pattern_id: Retrieve the digit pattern with the matching ID.
        :type digit_pattern_id: str
        :param org_id: Retrieve the digit pattern details for this organization.
        :type org_id: str
        :rtype: :class:`LocationDigitPatternObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        data = super().get(url, params=params)
        r = LocationDigitPatternObject.model_validate(data)
        return r

    def update_a_outgoing_permission_digit_pattern_for_a_location(self, location_id: str, digit_pattern_id: str,
                                                                  name: str = None, pattern: str = None,
                                                                  action: CallingPermissionObjectAction = None,
                                                                  transfer_enabled: bool = None, org_id: str = None):
        """
        Update a Outgoing Permission Digit Pattern for a Location

        Update the designated digit pattern.

        Use Digit Patterns to bypass the set permissions for all persons/workspaces at this location.

        Updating a digit pattern requires a full administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Update the digit pattern for this location.
        :type location_id: str
        :param digit_pattern_id: Update the digit pattern with the matching ID.
        :type digit_pattern_id: str
        :param name: A unique name for the digit pattern.
        :type name: str
        :param pattern: The digit pattern to be matched with the input number.
        :type pattern: str
        :param action: Action to be performed on the input number that matches the digit pattern.
        :type action: CallingPermissionObjectAction
        :param transfer_enabled: If `true`, allows transfer and forwarding for the call type.
        :type transfer_enabled: bool
        :param org_id: Update the digit pattern for this organization.
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
        url = self.ep(f'{location_id}/outgoingPermission/digitPatterns/{digit_pattern_id}')
        super().put(url, params=params, json=body)

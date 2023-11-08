from collections.abc import Generator
from datetime import datetime
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CallingPermissionObject', 'CallingPermissionObjectAction', 'CallingPermissionObjectCallType',
            'GeneratePasswordPostResponse', 'GetAutoTransferNumberObject', 'GetLocationAccessCodeObject',
            'GetLocationAccessCodeObjectAccessCodes', 'GetLocationInterceptObject',
            'GetLocationInterceptObjectIncoming', 'GetLocationInterceptObjectIncomingAnnouncements',
            'GetLocationInterceptObjectIncomingAnnouncementsGreeting',
            'GetLocationInterceptObjectIncomingAnnouncementsNewNumber', 'GetLocationInterceptObjectIncomingType',
            'GetLocationInterceptObjectOutgoing', 'GetLocationInterceptObjectOutgoingType',
            'GetLocationOutgoingPermissionResponse', 'InternalDialingGet', 'InternalDialingPut', 'PasswordGenerate',
            'PutAccessCodeLocationObject', 'RouteIdentity', 'RouteType', 'UnknownExtensionRouteIdentity']


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
    #: If you select this, then these types of calls are transferred automatically to the configured auto transfer
    #: number `autoTransferNumber1`.
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    #: If you select this, then these types of calls are transferred automatically to the configured auto transfer
    #: number `autoTransferNumber2`.
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    #: If you select this, then these types of calls are transferred automatically to the configured auto transfer
    #: number `autoTransferNumber3`.
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class CallingPermissionObject(ApiModel):
    #: Below are the call type values.
    #: example: INTERNAL_CALL
    call_type: Optional[CallingPermissionObjectCallType] = None
    #: Allows to configure settings for each call type.
    #: example: ALLOW
    action: Optional[CallingPermissionObjectAction] = None
    #: If enabled, allow the person to transfer or forward internal calls.
    #: example: True
    transfer_enabled: Optional[bool] = None


class GeneratePasswordPostResponse(ApiModel):
    #: Example password.
    #: example: xyz123!
    example_sip_password: Optional[str] = None


class GetAutoTransferNumberObject(ApiModel):
    #: Calls placed meeting the criteria in an outbound rule whose `action` is `TRANSFER_NUMBER_1` will be transferred
    #: to this number.
    #: example: 1234456789
    auto_transfer_number1: Optional[str] = None
    #: Calls placed meeting the criteria in an outbound rule whose `action` is `TRANSFER_NUMBER_2` will be transferred
    #: to this number.
    #: example: 2234567891
    auto_transfer_number2: Optional[str] = None
    #: Calls placed meeting the criteria in an outbound rule whose `action` is `TRANSFER_NUMBER_3` will be transferred
    #: to this number.
    #: example: 3234567891
    auto_transfer_number3: Optional[str] = None


class GetLocationAccessCodeObjectAccessCodes(ApiModel):
    #: Access code number.
    #: example: 123
    code: Optional[datetime] = None
    #: Access code description.
    #: example: Main Access Code
    description: Optional[str] = None


class GetLocationAccessCodeObject(ApiModel):
    #: Access code details
    access_codes: Optional[GetLocationAccessCodeObjectAccessCodes] = None


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
    #: example: True
    enabled: Optional[bool] = None
    #: Incoming destination phone number to be announced.
    #: example: 2147691003
    destination: Optional[str] = None


class GetLocationInterceptObjectIncomingAnnouncements(ApiModel):
    #: Greeting type for location intercept.
    #: example: DEFAULT
    greeting: Optional[GetLocationInterceptObjectIncomingAnnouncementsGreeting] = None
    #: If set to `CUSTOM` for greeting, filename of previously uploaded file.
    #: example: .wav
    file_name: Optional[str] = None
    #: Settings for new number announcement.
    new_number: Optional[GetLocationInterceptObjectIncomingAnnouncementsNewNumber] = None
    #: Transfer number details.
    zero_transfer: Optional[GetLocationInterceptObjectIncomingAnnouncementsNewNumber] = None


class GetLocationInterceptObjectIncoming(ApiModel):
    #: Select inbound call options.
    #: example: INTERCEPT_ALL
    type: Optional[GetLocationInterceptObjectIncomingType] = None
    #: Enable/disable to route voice mail.
    #: example: True
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
    #: example: INTERCEPT_ALL
    type: Optional[GetLocationInterceptObjectOutgoingType] = None
    #: Enable/disable to route all outbound calls to phone number.
    #: example: True
    transfer_enabled: Optional[bool] = None
    #: If enabled, set outgoing destination phone number.
    #: example: 2147691007
    destination: Optional[str] = None


class GetLocationInterceptObject(ApiModel):
    #: Enable/disable location intercept. Enable this feature to override any Location's Call Intercept settings that
    #: person configures.
    #: example: True
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
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    id: Optional[str] = None
    #: A unique name for the route identity.
    #: example: route_identity_name
    name: Optional[str] = None
    #: Type associated with the identity.
    type: Optional[RouteType] = None


class InternalDialingGet(ApiModel):
    #: When enabled, calls made by users at the location to an unknown extension (between 2-6 digits) are routed to the
    #: selected route group/trunk as premises calls.
    #: example: True
    enable_unknown_extension_route_policy: Optional[bool] = None
    #: The selected route group/trunk as premises calls.
    unknown_extension_route_identity: Optional[RouteIdentity] = None


class UnknownExtensionRouteIdentity(ApiModel):
    #: ID of the route type.
    #: example: Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQLzA1OWEyNzNlLWJiYjAtMTFlYy04NDIyLTAyNDJhYzEyMDAwMg
    id: Optional[str] = None
    #: Type associated with the identity.
    type: Optional[RouteType] = None


class InternalDialingPut(ApiModel):
    #: When enabled, calls made by users at the location to an unknown extension (between 2-6 digits) are routed to the
    #: selected route group/trunk as premises calls.
    #: example: True
    enable_unknown_extension_route_policy: Optional[bool] = None
    #: Type associated with the identity.
    unknown_extension_route_identity: Optional[UnknownExtensionRouteIdentity] = None


class PasswordGenerate(str, Enum):
    #: SIP password setting
    sip = 'SIP'


class PutAccessCodeLocationObject(ApiModel):
    #: Array of string to delete access codes. For example, ["1234","2345"]
    delete_codes: Optional[list[str]] = None


class GetLocationOutgoingPermissionResponse(ApiModel):
    #: Array of calling permissions.
    calling_permissions: Optional[list[CallingPermissionObject]] = None


class LocationCallSettingsCallHandlingApi(ApiChild, base='telephony/config/locations/{locationId}'):
    """
    Location Call Settings:  Call Handling
    
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

    def generate_example_password_for_location(self, location_id: str, org_id: str = None,
                                               generate: list[PasswordGenerate] = None) -> str:
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
        :param org_id: Organization to which the location belongs.
        :type org_id: str
        :param generate: password settings array.
        :type generate: list[PasswordGenerate]
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'actions/generatePassword/invoke')
        ...


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
        url = self.ep(f'internalDialing')
        ...


    def modify_the_internal_dialing_configuration_for_a_location(self, location_id: str,
                                                                 enable_unknown_extension_route_policy: bool,
                                                                 unknown_extension_route_identity: UnknownExtensionRouteIdentity,
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
        url = self.ep(f'internalDialing')
        ...


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
        url = self.ep(f'intercept')
        ...


    def put_location_intercept(self, location_id: str, enabled: bool, incoming: GetLocationInterceptObjectIncoming,
                               outgoing: GetLocationInterceptObjectOutgoing, org_id: str = None):
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
        url = self.ep(f'intercept')
        ...


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
        url = self.ep(f'outgoingPermission')
        ...


    def update_location_outgoing_permission(self, location_id: str, org_id: str = None,
                                            calling_permissions: list[CallingPermissionObject] = None):
        """
        Update Location Outgoing Permission

        Update the location's outgoing call settings.
        
        Location's outgoing call settings allows you to determine the types of calls the people/workspaces at this
        location are allowed to make and configure the default calling permission for each call type at a location.
        
        Updating a location's outgoing call settings requires a full administrator or location administrator auth token
        with a scope of spark-admin:telephony_config_write.

        :param location_id: Update outgoing call settings for this location.
        :type location_id: str
        :param org_id: Update outgoing call settings for this organization.
        :type org_id: str
        :param calling_permissions: Array specifying the subset of calling permissions to be updated.
        :type calling_permissions: list[CallingPermissionObject]
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'outgoingPermission')
        ...


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
        url = self.ep(f'outgoingPermission/autoTransferNumbers')
        ...


    def put_outgoing_permission_auto_transfer_number(self, location_id: str, auto_transfer_number1: str,
                                                     auto_transfer_number2: str, auto_transfer_number3: str,
                                                     org_id: str = None):
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
        url = self.ep(f'outgoingPermission/autoTransferNumbers')
        ...


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
        url = self.ep(f'outgoingPermission/accessCodes')
        ...


    def create_outgoing_permission_a_new_access_code_for_a_customer_location(self, location_id: str,
                                                                             access_codes: GetLocationAccessCodeObjectAccessCodes,
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
        url = self.ep(f'outgoingPermission/accessCodes')
        ...


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
        url = self.ep(f'outgoingPermission/accessCodes')
        ...

    ...
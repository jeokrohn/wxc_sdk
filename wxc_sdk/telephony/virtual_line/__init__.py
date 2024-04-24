from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional

from pydantic import TypeAdapter

from ...api_child import ApiChild
from ...base import ApiModel
from ...common import PrimaryOrShared, AssignedDectNetwork
from ...locations import LocationAddress
from ...person_settings import TelephonyDevice
from ...person_settings.callbridge import CallBridgeApi
from ...person_settings.call_intercept import CallInterceptApi
from ...person_settings.call_recording import CallRecordingApi
from ...person_settings.call_waiting import CallWaitingApi
from ...person_settings.caller_id import ExternalCallerIdNamePolicy, CallerIdApi
from ...person_settings.common import ApiSelector
from ...person_settings.forwarding import PersonForwardingApi
from ...person_settings.permissions_in import IncomingPermissionsApi
from ...person_settings.permissions_out import OutgoingPermissionsApi

__all__ = ['VirtualLine', 'VirtualLinesApi', 'VirtualLineNumber', 'VirtualLineLocation', 'VirtualLineNumberPhoneNumber',
           'VirtualLineDevices']


class VirtualLineNumber(ApiModel):
    #: Virtual Line external.  Either `external` or `extension` is mandatory.
    #: example: +15558675313
    external: Optional[str] = None
    #: Virtual Line extension.  Either `external` or `extension` is mandatory.
    #: example: 6101
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12346101
    esn: Optional[str] = None
    #: Number is Primary or Alternative Number.
    #: example: True
    primary: Optional[bool] = None


class VirtualLineLocation(ApiModel):
    #: ID of location associated with virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
    id: Optional[str] = None
    #: Name of location associated with virtual line.
    #: example: Main Location Test
    name: Optional[str] = None
    #: The address of the virtual line.
    address: Optional[LocationAddress] = None


class VirtualLine(ApiModel):
    #: A unique identifier for the virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1ZJUlRVQUxfTElORS9iMTJhNTBiMi01N2NiLTQ0MzktYjc1MS1jZDQ4M2I4MjhmNmU=
    id: Optional[str] = None
    #: Last name for virtual line.
    #: example: Shen
    last_name: Optional[str] = None
    #: First name for virtual line.
    #: example: Tom
    first_name: Optional[str] = None
    #: Display name defined for a virtual line.
    #: example: Bob Smith
    display_name: Optional[str] = None
    #: `callerIdLastName` for virtual line.
    #: example: Shen
    caller_id_last_name: Optional[str] = None
    #: `callerIdFirstName` for virtual line.
    #: example: Tom
    caller_id_first_name: Optional[str] = None
    #: `callerIdNumber` for virtual line.
    #: example: +15558675313
    caller_id_number: Optional[str] = None
    #: `externalCallerIdNamePolicy` for the virtual line.
    #: example: DIRECT_LINE
    external_caller_id_name_policy: Optional[ExternalCallerIdNamePolicy] = None
    #: `customExternalCallerIdName` for virtual line.
    #: example: Tom
    custom_external_caller_id_name: Optional[str] = None
    #: Calling details of virtual line.
    number: Optional[VirtualLineNumber] = None
    #: Location details of virtual line.
    location: Optional[VirtualLineLocation] = None
    #: Number of devices assigned to a virtual line.
    #: example: 1
    number_of_devices_assigned: Optional[int] = None
    #: Type of billing plan.
    #: example: BCOCP1
    billing_plan: Optional[str] = None
    #: Flag to indicate a directory search.
    #: example: True
    directory_search_enabled: Optional[bool] = None
    #: Virtual Line's announcement language.
    #: example: 'French'
    announcement_language: Optional[str] = None
    #: Time zone defined for the virtual line.
    #: example: Africa/Algiers
    time_zone: Optional[str] = None
    #: Calling details of virtual line.
    #: List of devices assigned to a virtual line.
    devices: Optional[list[TelephonyDevice]] = None


class VirtualLineNumberPhoneNumber(ApiModel):
    #: Phone number that is assigned to a virtual line.
    #: example: +15558675309
    direct_number: Optional[str] = None
    #: Extension that is assigned to a virtual line.
    #: example: 5309
    extension: Optional[str] = None
    #: If `true` marks the phone number as primary.
    #: example: True
    primary: Optional[bool] = None


class VirtualLineDevices(ApiModel):
    #: List of devices assigned to a virtual line.
    devices: Optional[list[TelephonyDevice]] = None
    #: Indicates to which line a device can be assigned.
    available_endpoint_type: Optional[PrimaryOrShared] = None
    #: Maximum number of devices a virtual line can be assigned to.
    #: example: 35
    max_device_count: Optional[int] = None


@dataclass(init=False)
class VirtualLinesApi(ApiChild, base='telephony/config/virtualLines'):
    #: Call bridge settings
    call_bridge: CallBridgeApi
    #: call intercept settings
    call_intercept: CallInterceptApi
    #: call recording settings
    call_recording: CallRecordingApi
    #: call waiting settings
    call_waiting: CallWaitingApi
    #: caller id settings
    caller_id: CallerIdApi
    #: forwarding settings
    forwarding: PersonForwardingApi
    #: incoming permissions
    permissions_in: IncomingPermissionsApi
    #: outgoing permissions
    permissions_out: OutgoingPermissionsApi

    def __init__(self, session):
        super().__init__(session=session)
        self.call_bridge = CallBridgeApi(session=session, selector=ApiSelector.virtual_line)
        self.call_intercept = CallInterceptApi(session=session, selector=ApiSelector.virtual_line)
        self.call_recording = CallRecordingApi(session=session, selector=ApiSelector.virtual_line)
        self.call_waiting = CallWaitingApi(session=session, selector=ApiSelector.virtual_line)
        self.caller_id = CallerIdApi(session=session, selector=ApiSelector.virtual_line)
        self.forwarding = PersonForwardingApi(session=session, selector=ApiSelector.virtual_line)
        self.permissions_in = IncomingPermissionsApi(session=session, selector=ApiSelector.virtual_line)
        self.permissions_out = OutgoingPermissionsApi(session=session, selector=ApiSelector.virtual_line)

    def create(self, first_name: str, last_name: str, location_id: str, display_name: str = None,
               phone_number: str = None, extension: str = None, caller_id_last_name: str = None,
               caller_id_first_name: str = None, caller_id_number: str = None,
               org_id: str = None) -> str:
        """
        Create a Virtual Line

        Create new Virtual Line for the given location.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Creating a virtual line requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param first_name: First name defined for a virtual line. Minimum length is 1. Maximum length is 30.
        :type first_name: str
        :param last_name: Last name defined for a virtual line. Minimum length is 1. Maximum length is 30.
        :type last_name: str
        :param location_id: ID of location for virtual line.
        :type location_id: str
        :param display_name: Display name defined for a virtual line.
        :type display_name: str
        :param phone_number: Phone number of a virtual line. Minimum length is 1. Maximum length is 23. Either
            `phoneNumber` or `extension` is mandatory.
        :type phone_number: str
        :param extension: Extension of a virtual line. Minimum length is 2. Maximum length is 10. Either `phoneNumber`
            or `extension` is mandatory.
        :type extension: str
        :param caller_id_last_name: Last name used in the Calling Line ID and for dial-by-name functions. Minimum
            length is 1. Maximum length is 30.
        :type caller_id_last_name: str
        :param caller_id_first_name: First name used in the Calling Line ID and for dial-by-name functions. Minimum
            length is 1. Maximum length is 30.
        :type caller_id_first_name: str
        :param caller_id_number: Phone number to appear as the CLID for all calls. Minimum length is 1. Maximum length
            is 23.
        :type caller_id_number: str
        :param org_id: Create the virtual line for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['firstName'] = first_name
        body['lastName'] = last_name
        if display_name is not None:
            body['displayName'] = display_name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        body['locationId'] = location_id
        if caller_id_last_name is not None:
            body['callerIdLastName'] = caller_id_last_name
        if caller_id_first_name is not None:
            body['callerIdFirstName'] = caller_id_first_name
        if caller_id_number is not None:
            body['callerIdNumber'] = caller_id_number
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def delete(self, virtual_line_id: str, org_id: str = None):
        """
        Delete a Virtual Line

        Delete the designated Virtual Line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Deleting a virtual line requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Delete the virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: Delete the virtual line from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}')
        super().delete(url, params=params)

    def details(self, virtual_line_id: str, org_id: str = None) -> VirtualLine:
        """
        Get Details for a Virtual Line

        Retrieve Virtual Line details.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Retrieving virtual line details requires a full or user or read-only administrator or location administrator
        auth token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: Retrieve virtual line settings from this organization.
        :type org_id: str
        :rtype: :class:`GetVirtualLineObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}')
        data = super().get(url, params=params)
        r = VirtualLine.model_validate(data)
        return r

    def update(self, virtual_line_id: str, first_name: str = None, last_name: str = None,
               display_name: str = None, phone_number: str = None, extension: str = None,
               announcement_language: str = None, caller_id_last_name: str = None,
               caller_id_first_name: str = None, caller_id_number: str = None, time_zone: str = None,
               org_id: str = None):
        """
        Update a Virtual Line

        Update the designated Virtual Line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Updating a virtual line requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Update settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param first_name: First name defined for a virtual line. Minimum length is 1. Maximum length is 30.
        :type first_name: str
        :param last_name: Last name defined for a virtual line. Minimum length is 1. Maximum length is 30.
        :type last_name: str
        :param display_name: Display name defined for a virtual line.
        :type display_name: str
        :param phone_number: Phone number of a virtual line. Minimum length is 1. Maximum length is 23. Either
            `phoneNumber` or `extension` is mandatory.
        :type phone_number: str
        :param extension: Extension of a virtual line. Minimum length is 2. Maximum length is 10. Either `phoneNumber`
            or `extension` is mandatory.
        :type extension: str
        :param announcement_language: Virtual Line's announcement language.
        :type announcement_language: str
        :param caller_id_last_name: Last name used in the Calling Line ID and for dial-by-name functions. Minimum
            length is 1. Maximum length is 30.
        :type caller_id_last_name: str
        :param caller_id_first_name: First name used in the Calling Line ID and for dial-by-name functions. Minimum
            length is 1. Maximum length is 30.
        :type caller_id_first_name: str
        :param caller_id_number: Phone number to appear as the CLID for all calls. Minimum length is 1. Maximum length
            is 23.
        :type caller_id_number: str
        :param time_zone: Time zone defined for the virtual line.
        :type time_zone: str
        :param org_id: Update virtual line settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if first_name is not None:
            body['firstName'] = first_name
        if last_name is not None:
            body['lastName'] = last_name
        if display_name is not None:
            body['displayName'] = display_name
        if phone_number is not None:
            body['phoneNumber'] = phone_number
        if extension is not None:
            body['extension'] = extension
        if announcement_language is not None:
            body['announcementLanguage'] = announcement_language
        if caller_id_last_name is not None:
            body['callerIdLastName'] = caller_id_last_name
        if caller_id_first_name is not None:
            body['callerIdFirstName'] = caller_id_first_name
        if caller_id_number is not None:
            body['callerIdNumber'] = caller_id_number
        if time_zone is not None:
            body['timeZone'] = time_zone
        url = self.ep(f'{virtual_line_id}')
        super().put(url, params=params, json=body)

    def get_phone_number(self, virtual_line_id: str,
                         org_id: str = None) -> VirtualLineNumberPhoneNumber:
        """
        Get Phone Number assigned for a Virtual Line

        Get details on the assigned phone number and extension for the virtual line.

        Retrieving virtual line phone number details requires a full or user or read-only administrator auth token
        with
        a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: Retrieve virtual line settings from this organization.
        :type org_id: str
        :rtype: GetVirtualLineNumberObjectPhoneNumber
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/number')
        data = super().get(url, params=params)
        r = VirtualLineNumberPhoneNumber.model_validate(data['phoneNumber'])
        return r

    def update_directory_search(self, virtual_line_id: str, enabled: bool, org_id: str = None):
        """
        Update Directory search for a Virtual Line

        Update the directory search for a designated Virtual Line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Updating Directory search for a virtual line requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Update settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param enabled: Whether or not the directory search for a virtual line is enabled.
        :type enabled: bool
        :param org_id: Update virtual line settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep(f'{virtual_line_id}/directorySearch')
        super().put(url, params=params, json=body)

    def assigned_devices(self, virtual_line_id: str, org_id: str = None) -> VirtualLineDevices:
        """
        Get List of Devices assigned for a Virtual Line

        Retrieve Device details assigned for a virtual line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Retrieving the assigned device detials for a virtual line requires a full or user or read-only administrator
        auth token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: Retrieve virtual line settings from this organization.
        :type org_id: str
        :rtype: :class:`VirtualLineDevices`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/devices')
        data = super().get(url, params=params)
        r = VirtualLineDevices.model_validate(data)
        return r

    def dect_networks(self, virtual_line_id: str, org_id: str = None) -> list[AssignedDectNetwork]:
        """
        Get List of Dect Networks Handsets for a Virtual Line

        Retrieve DECT Network details assigned for a virtual line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Retrieving the assigned device detials for a virtual line requires a full or user or read-only administrator
        auth token with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: Retrieve virtual line settings from this organization.
        :type org_id: str
        :rtype: list[AssignedDectNetwork]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/dects')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AssignedDectNetwork]).validate_python(data['dectNetworks'])
        return r

    def list(self, org_id: str = None, location_id: list[str] = None,
             id: list[str] = None, owner_name: list[str] = None, phone_number: list[str] = None,
             location_name: list[str] = None, order: list[str] = None, has_device_assigned: bool = None,
             has_extension_assigned: bool = None, has_dn_assigned: bool = None,
             **params) -> Generator[VirtualLine, None, None]:
        """
        List all Virtual Lines for the organization.
        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.
        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List virtual lines for this organization.
        :type org_id: str
        :param location_id: Return the list of virtual lines matching these location ids. Example for multiple values -
            ?locationId=locId1&locationId=locId2.
        :type location_id: List[str]
        :param id: Return the list of virtual lines matching these virtualLineIds.
        :type id: List[str]
        :param owner_name: Return the list of virtual lines matching these owner names.
        :type owner_name: List[str]
        :param phone_number: Return the list of virtual lines matching these phone numbers.
        :type phone_number: List[str]
        :param location_name: Return the list of virtual lines matching the location names.
        :type location_name: List[str]
        :param order: Return the list of virtual lines based on the order. Default sort will be in an Ascending order.
            Maximum 3 orders allowed at a time.
        :type order: List[str]
        :param has_device_assigned: If true, includes only virtual lines with devices assigned. When not explicitly
            specified, the default includes both virtual lines with devices assigned and not assigned.
        :type has_device_assigned: bool
        :param has_extension_assigned: If true, includes only virtual lines with an extension assigned. When not
            explicitly specified, the default includes both virtual lines with extension assigned and not assigned.
        :type has_extension_assigned: bool
        :param has_dn_assigned: If true, includes only virtual lines with an assigned directory number, also known as a
            Dn. When not explicitly specified, the default includes both virtual lines with a Dn assigned and not
            assigned.
        :type has_dn_assigned: bool
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if id is not None:
            params['id'] = id
        if owner_name is not None:
            params['ownerName'] = owner_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if location_name is not None:
            params['locationName'] = location_name
        if order is not None:
            params['order'] = order
        if has_device_assigned is not None:
            params['hasDeviceAssigned'] = has_device_assigned
        if has_extension_assigned is not None:
            params['hasExtensionAssigned'] = has_extension_assigned
        if has_dn_assigned is not None:
            params['hasDnAssigned'] = has_dn_assigned
        url = self.ep()
        return self.session.follow_pagination(url=url, model=VirtualLine, params=params, item_key='virtualLines')

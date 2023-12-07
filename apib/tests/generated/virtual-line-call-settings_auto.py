from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ListVirtualLineObject', 'ListVirtualLineObjectExternalCallerIdNamePolicy',
            'ListVirtualLineObjectLocation', 'ListVirtualLineObjectNumber', 'VirtualLineCallSettingsApi']


class ListVirtualLineObjectExternalCallerIdNamePolicy(str, Enum):
    #: Shows virtual lines Caller ID name.
    direct_line = 'DIRECT_LINE'
    #: Shows virtual lines location name.
    location = 'LOCATION'
    #: Allow virtual lines first/last name to be configured.
    other = 'OTHER'


class ListVirtualLineObjectNumber(ApiModel):
    #: Virtual Line external.  Either `external` or `extension` is mandatory.
    #: example: +15558675313
    external: Optional[str] = None
    #: Virtual Line extension.  Either `external` or `extension` is mandatory.
    #: example: 6101
    extension: Optional[str] = None
    #: Number is Primary or Alternative Number.
    #: example: True
    primary: Optional[bool] = None


class ListVirtualLineObjectLocation(ApiModel):
    #: ID of location associated with virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzhmZjMwMjg2LWVhMzMtNDc2Ny1iMTBmLWQ2MWIyNzFhMDVlZg
    id: Optional[str] = None
    #: Name of location associated with virtual line.
    #: example: Denver
    name: Optional[str] = None


class ListVirtualLineObject(ApiModel):
    #: A unique identifier for the virtual line.
    #: example: Y2lzY29zcGFyazovL3VzL1ZJUlRVQUxfTElORS9iMTJhNTBiMi01N2NiLTQ0MzktYjc1MS1jZDQ4M2I4MjhmNmU=
    id: Optional[str] = None
    #: Last name for virtual line.
    #: example: Shen
    last_name: Optional[str] = None
    #: First name for virtual line.
    #: example: Tom
    first_name: Optional[str] = None
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
    external_caller_id_name_policy: Optional[ListVirtualLineObjectExternalCallerIdNamePolicy] = None
    #: `customExternalCallerIdName` for virtual line.
    #: example: Tom
    custom_external_caller_id_name: Optional[str] = None
    #: Calling details of virtual line.
    number: Optional[ListVirtualLineObjectNumber] = None
    #: Location details of virtual line.
    location: Optional[ListVirtualLineObjectLocation] = None
    #: Number of devices assigned to a virtual line.
    #: example: 1
    number_of_devices_assigned: Optional[int] = None
    #: Type of billing plan.
    #: example: BCOCP1
    billing_plan: Optional[str] = None


class VirtualLineCallSettingsApi(ApiChild, base='telephony/config/virtualLines'):
    """
    Virtual Line Call Settings
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Viutual Line Settings supports listing Webex Calling virtual lines.
    
    Viewing Virtual Lines requires a full, user, or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read.
    """

    def read_the_list_of_virtual_lines(self, location_id: list[str] = None, id: list[str] = None,
                                       owner_name: list[str] = None, phone_number: list[str] = None,
                                       location_name: list[str] = None, order: list[str] = None,
                                       has_device_assigned: bool = None, has_extension_assigned: bool = None,
                                       has_dn_assigned: bool = None, org_id: str = None,
                                       **params) -> Generator[ListVirtualLineObject, None, None]:
        """
        Read the List of Virtual Lines

        List all Virtual Lines for the organization.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of virtual lines matching these location ids. Example for multiple values -
            `?locationId=locId1&locationId=locId2`.
        :type location_id: list[str]
        :param id: Return the list of virtual lines matching these virtualLineIds. Example for multiple values -
            `?id=id1&id=id2`.
        :type id: list[str]
        :param owner_name: Return the list of virtual lines matching these owner names. Example for multiple values -
            `?ownerName=name1&ownerName=name2`.
        :type owner_name: list[str]
        :param phone_number: Return the list of virtual lines matching these phone numbers. Example for multiple values
            - `?phoneNumber=number1&phoneNumber=number2`.
        :type phone_number: list[str]
        :param location_name: Return the list of virtual lines matching the location names. Example for multiple values
            - `?locationName=loc1&locationName=loc2`.
        :type location_name: list[str]
        :param order: Return the list of virtual lines based on the order. Default sort will be in an Ascending order.
            Maximum 3 orders allowed at a time. Example for multiple values - `?order=order1&order=order2`.
        :type order: list[str]
        :param has_device_assigned: If `true`, includes only virtual lines with devices assigned. When not explicitly
            specified, the default includes both virtual lines with devices assigned and not assigned.
        :type has_device_assigned: bool
        :param has_extension_assigned: If `true`, includes only virtual lines with an extension assigned. When not
            explicitly specified, the default includes both virtual lines with extension assigned and not assigned.
        :type has_extension_assigned: bool
        :param has_dn_assigned: If `true`, includes only virtual lines with an assigned directory number, also known as
            a Dn. When not explicitly specified, the default includes both virtual lines with a Dn assigned and not
            assigned.
        :type has_dn_assigned: bool
        :param org_id: List virtual lines for this organization.
        :type org_id: str
        :return: Generator yielding :class:`ListVirtualLineObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = ','.join(location_id)
        if id is not None:
            params['id'] = ','.join(id)
        if owner_name is not None:
            params['ownerName'] = ','.join(owner_name)
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if location_name is not None:
            params['locationName'] = ','.join(location_name)
        if order is not None:
            params['order'] = ','.join(order)
        if has_device_assigned is not None:
            params['hasDeviceAssigned'] = str(has_device_assigned).lower()
        if has_extension_assigned is not None:
            params['hasExtensionAssigned'] = str(has_extension_assigned).lower()
        if has_dn_assigned is not None:
            params['hasDnAssigned'] = str(has_dn_assigned).lower()
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ListVirtualLineObject, item_key='virtualLines', params=params)

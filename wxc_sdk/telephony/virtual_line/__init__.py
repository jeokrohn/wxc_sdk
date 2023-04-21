from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional

from ...api_child import ApiChild
from ...base import ApiModel
from ...common import UserNumber, IdAndName
from ...person_settings.caller_id import ExternalCallerIdNamePolicy

__all__ = ['VirtualLine', 'VirtualLinesApi']


class VirtualLine(ApiModel):
    #: A unique identifier for the virtual line.
    id: Optional[str]
    #: Last name for virtual line.
    last_name: Optional[str]
    #: First name for virtual line.
    first_name: Optional[str]
    #: callerIdLastName for virtual line.
    caller_id_last_name: Optional[str]
    #: callerIdFirstName for virtual line.
    caller_id_first_name: Optional[str]
    #: callerIdNumber for virtual line.
    caller_id_number: Optional[str]
    #: externalCallerIdNamePolicy for the virtual line.
    external_caller_id_name_policy: Optional[ExternalCallerIdNamePolicy]
    #: customExternalCallerIdName for virtual line.
    custom_external_caller_id_name: Optional[str]
    #: Calling details of virtual line.
    number: Optional[UserNumber]
    #: Location details of virtual line.
    location: Optional[IdAndName]
    #: Number of devices assigned to a virtual line.
    number_of_devices_assigned: Optional[int]
    #: Type of billing plan.
    billing_plan: Optional[str]


@dataclass(init=False)
class VirtualLinesApi(ApiChild, base='telephony/config/virtualLines'):
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

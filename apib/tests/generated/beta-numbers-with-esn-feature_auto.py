from collections.abc import Generator
from datetime import datetime
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetPhoneNumbersForAnOrganizationWithGivenCriteriasOwnerType', 'NumberListGetObject', 'NumberObject',
            'NumberObjectLocation', 'NumberObjectOwner']


class NumberObjectLocation(ApiModel):
    #: ID of location for phone number.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    id: Optional[str] = None
    #: Name of the location for phone number
    #: example: Bangalore
    name: Optional[str] = None


class NumberObjectOwner(ApiModel):
    #: ID of the owner to which PSTN Phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner
    #: example: PEOPLE
    type: Optional[str] = None
    #: First name of the PSTN phone number's owner
    #: example: Mark
    first_name: Optional[str] = None
    #: Last name of the PSTN phone number's owner
    #: example: Zand
    last_name: Optional[str] = None


class NumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Extension for a PSTN phone number.
    #: example: 000
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[datetime] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 1234000
    esn: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[str] = None
    #: Type of phone number.
    #: example: PRIMARY
    phone_number_type: Optional[str] = None
    #: Indicates if the phone number is used as location clid.
    #: example: True
    main_number: Optional[bool] = None
    #: Indicates if a phone number is a toll free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    location: Optional[NumberObjectLocation] = None
    owner: Optional[NumberObjectOwner] = None


class NumberListGetObject(ApiModel):
    #: Array of phone numbers.
    phone_numbers: Optional[list[NumberObject]] = None


class GetPhoneNumbersForAnOrganizationWithGivenCriteriasOwnerType(str, Enum):
    people = 'PEOPLE'
    place = 'PLACE'
    auto_attendant = 'AUTO_ATTENDANT'
    call_queue = 'CALL_QUEUE'
    group_paging = 'GROUP_PAGING'
    hunt_group = 'HUNT_GROUP'
    voice_messaging = 'VOICE_MESSAGING'
    broadworks_anywhere = 'BROADWORKS_ANYWHERE'
    contact_center_link = 'CONTACT_CENTER_LINK'
    route_list = 'ROUTE_LIST'
    voicemail_group = 'VOICEMAIL_GROUP'


class BetaNumbersWithESNFeatureApi(ApiChild, base='telephony/config/numbers'):
    """
    Beta Numbers with ESN Feature
    
    Numbers supports reading and writing of Webex Calling phone numbers for a
    specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def get_phone_numbers_for_an_organization_with_given_criterias(self, org_id: str = None, location_id: str = None,
                                                                   max_: int = None, start: int = None,
                                                                   phone_number: str = None, available: bool = None,
                                                                   order: str = None, owner_name: str = None,
                                                                   owner_id: str = None,
                                                                   owner_type: GetPhoneNumbersForAnOrganizationWithGivenCriteriasOwnerType = None,
                                                                   extension: str = None, number_type: str = None,
                                                                   phone_number_type: str = None, state: str = None,
                                                                   details: bool = None,
                                                                   toll_free_numbers: bool = None,
                                                                   restricted_non_geo_numbers: bool = None) -> list[NumberObject]:
        """
        Get Phone Numbers for an Organization with Given Criterias

        List all the phone numbers for the given organization along with the status and owner (if any).
        
        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.
        
        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: List numbers for this organization.
        :type org_id: str
        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param max_: Limit the number of phone numbers returned to this maximum count. Default is 2000.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching phone numbers. Default is 0.
        :type start: int
        :param phone_number: Search for this `phoneNumber`.
        :type phone_number: str
        :param available: Search among the available phone numbers. This parameter cannot be used along with
            `ownerType` parameter when set to `true`.
        :type available: bool
        :param order: Sort the list of phone numbers based on the following:`lastName`,`dn`,`extension`. Default sort
            will be based on number and extension in an ascending order
        :type order: str
        :param owner_name: Return the list of phone numbers that is owned by given `ownerName`. Maximum length is 255.
        :type owner_name: str
        :param owner_id: Returns only the matched number/extension entries assigned to the feature with specified
            uuid/broadsoftId.
        :type owner_id: str
        :param owner_type: Returns the list of phone numbers that are of given `ownerType`. Possible input values
        :type owner_type: GetPhoneNumbersForAnOrganizationWithGivenCriteriasOwnerType
        :param extension: Returns the list of PSTN phone numbers with the given extension.
        :type extension: str
        :param number_type: Returns the filtered list of PSTN phone numbers that contains given type of numbers. This
            parameter cannot be used along with `available` or `state`.
        :type number_type: str
        :param phone_number_type: Returns the filtered list of PSTN phone numbers that are of given `phoneNumberType`.
        :type phone_number_type: str
        :param state: Returns the list of PSTN phone numbers with matching state.
        :type state: str
        :param details: Returns the overall count of the PSTN phone numbers along with other details for given
            organization.
        :type details: bool
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
        :param restricted_non_geo_numbers: Returns the list of restricted non geographical numbers.
        :type restricted_non_geo_numbers: bool
        :rtype: list[NumberObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if max_ is not None:
            params['max'] = max_
        if start is not None:
            params['start'] = start
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if available is not None:
            params['available'] = str(available).lower()
        if order is not None:
            params['order'] = order
        if owner_name is not None:
            params['ownerName'] = owner_name
        if owner_id is not None:
            params['ownerId'] = owner_id
        if owner_type is not None:
            params['ownerType'] = owner_type
        if extension is not None:
            params['extension'] = extension
        if number_type is not None:
            params['numberType'] = number_type
        if phone_number_type is not None:
            params['phoneNumberType'] = phone_number_type
        if state is not None:
            params['state'] = state
        if details is not None:
            params['details'] = str(details).lower()
        if toll_free_numbers is not None:
            params['tollFreeNumbers'] = str(toll_free_numbers).lower()
        if restricted_non_geo_numbers is not None:
            params['restrictedNonGeoNumbers'] = str(restricted_non_geo_numbers).lower()
        url = self.ep()
        ...

    ...
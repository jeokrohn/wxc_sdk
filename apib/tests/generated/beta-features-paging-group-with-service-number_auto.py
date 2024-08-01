from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaFeaturesPagingGroupWithServiceNumberApi', 'PagingGroupPrimaryAvailableNumberObject', 'STATE',
           'TelephonyType']


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class PagingGroupPrimaryAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: Indicates if the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: Indicates if the phone number is a toll-free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    #: Indicates the telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: Indicates if the phone number is a service number. Service numbers are intended to be high-volume regular phone
    #: numbers (non-mobile, non toll-free numbers). If `true` the `phoneNumber` is a service number; otherwise, it is
    #: a standard number.
    #: example: True
    is_service_number: Optional[bool] = None


class BetaFeaturesPagingGroupWithServiceNumberApi(ApiChild, base='telephony/config/locations'):
    """
    Beta Features: Paging Group with Service Number
    
    Features: Paging Group supports reading and writing of Webex Calling Paging Group settings for a specific
    organization.
    
    Service numbers are intended to be high-volume regular phone numbers (non-mobile, non toll-free numbers), while
    standard numbers are PSTN numbers that do not fall under this classification.
    With the service number feature, available number APIs for location services or for features like members CLID,
    call forwarding or call intercept will now return service numbers in response.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def get_paging_group_primary_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                         org_id: str = None,
                                                         **params) -> Generator[PagingGroupPrimaryAvailableNumberObject, None, None]:
        """
        Get Paging Group Primary Available Phone Numbers

        List service and standard numbers that are available to be assigned as the paging group's primary phone number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`PagingGroupPrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'{location_id}/paging/availableNumbers')
        return self.session.follow_pagination(url=url, model=PagingGroupPrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

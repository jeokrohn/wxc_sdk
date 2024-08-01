from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaFeaturesCallQueueWithServiceNumberApi', 'CallQueueCallForwardAvailableNumberObject',
           'CallQueueCallForwardAvailableNumberObjectOwner', 'CallQueuePrimaryAvailableNumberObject',
           'NumberOwnerType', 'STATE', 'TelephonyType']


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class CallQueuePrimaryAvailableNumberObject(ApiModel):
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


class NumberOwnerType(str, Enum):
    #: PSTN phone number's owner is a workspace.
    place = 'PLACE'
    #: PSTN phone number's owner is a person.
    people = 'PEOPLE'
    #: PSTN phone number's owner is a Virtual Profile.
    virtual_line = 'VIRTUAL_LINE'
    #: PSTN phone number's owner is an auto-attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: PSTN phone number's owner is a call queue.
    call_queue = 'CALL_QUEUE'
    #: PSTN phone number's owner is a group paging.
    group_paging = 'GROUP_PAGING'
    #: PSTN phone number's owner is a hunt group.
    hunt_group = 'HUNT_GROUP'
    #: PSTN phone number's owner is a voice messaging.
    voice_messaging = 'VOICE_MESSAGING'
    #: PSTN phone number's owner is a Single Number Reach.
    office_anywhere = 'OFFICE_ANYWHERE'
    #: PSTN phone number's owner is a Contact Center link.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: PSTN phone number's owner is a Contact Center adapter.
    contact_center_adapter = 'CONTACT_CENTER_ADAPTER'
    #: PSTN phone number's owner is a route list.
    route_list = 'ROUTE_LIST'
    #: PSTN phone number's owner is a voicemail group.
    voicemail_group = 'VOICEMAIL_GROUP'
    #: PSTN phone number's owner is a collaborate bridge.
    collaborate_bridge = 'COLLABORATE_BRIDGE'


class CallQueueCallForwardAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which PSTN Phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner.
    #: example: PEOPLE
    type: Optional[NumberOwnerType] = None
    #: First name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE`
    #: or `VIRTUAL_LINE`.
    #: example: Test
    first_name: Optional[str] = None
    #: Last name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Person
    last_name: Optional[str] = None
    #: Display name of the PSTN phone number's owner. This field will be present except when the owner `type` is
    #: `PEOPLE` or `VIRTUAL_LINE`.
    #: example: TestWorkSpace
    display_name: Optional[str] = None


class CallQueueCallForwardAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Extension for a PSTN phone number.
    #: example: 1235
    extension: Optional[str] = None
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
    owner: Optional[CallQueueCallForwardAvailableNumberObjectOwner] = None


class BetaFeaturesCallQueueWithServiceNumberApi(ApiChild, base='telephony/config/locations'):
    """
    Beta Features: Call Queue with Service Number
    
    Features: Call Queue supports reading and writing of Webex Calling Call Queue settings for a specific organization.
    
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

    def get_call_queue_primary_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                       org_id: str = None,
                                                       **params) -> Generator[CallQueuePrimaryAvailableNumberObject, None, None]:
        """
        Get Call Queue Primary Available Phone Numbers

        List service and standard numbers that are available to be assigned as the call queue's primary phone number.
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
        :return: Generator yielding :class:`CallQueuePrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'{location_id}/queues/availableNumbers')
        return self.session.follow_pagination(url=url, model=CallQueuePrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_call_queue_alternate_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                         org_id: str = None,
                                                         **params) -> Generator[CallQueuePrimaryAvailableNumberObject, None, None]:
        """
        Get Call Queue Alternate Available Phone Numbers

        List service and standard numbers that are available to be assigned as the call queue's alternate phone number.
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
        :return: Generator yielding :class:`CallQueuePrimaryAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'{location_id}/queues/alternate/availableNumbers')
        return self.session.follow_pagination(url=url, model=CallQueuePrimaryAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_call_queue_call_forward_available_phone_numbers(self, location_id: str, phone_number: list[str] = None,
                                                            owner_name: str = None, extension: str = None,
                                                            org_id: str = None,
                                                            **params) -> Generator[CallQueueCallForwardAvailableNumberObject, None, None]:
        """
        Get Call Queue Call Forward Available Phone Numbers

        List service and standard numbers that are available to be assigned as the call queue's call forward number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        assigned to an owning entity.

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
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`CallQueueCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'{location_id}/queues/callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=CallQueueCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['NumberListGetObject', 'NumberListGetObjectLocation', 'NumberListGetObjectOwner', 'TelephonyType']


class NumberListGetObjectLocation(ApiModel):
    #: ID of location for phone number.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    id: Optional[str] = None
    #: Name of the location for phone number
    #: example: Banglore
    name: Optional[str] = None


class NumberListGetObjectOwner(ApiModel):
    #: ID of the owner to which PSTN Phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner
    #: example: PEOPLE
    type: Optional[str] = None
    #: First name of the PSTN phone number's owner
    #: example: Mark
    firstName: Optional[str] = None
    #: Last name of the PSTN phone number's owner
    #: example: Zand
    lastName: Optional[str] = None


class TelephonyType(str, Enum):
    #: Object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'
    #: Object is a mobile number.
    mobile_number = 'MOBILE_NUMBER'


class NumberListGetObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phoneNumber: Optional[str] = None
    #: Extension for a PSTN phone number.
    #: example: 000
    extension: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[str] = None
    #: Type of phone number.
    #: example: PRIMARY
    phoneNumberType: Optional[str] = None
    #: Indicates if the phone number is used as location clid.
    #: example: True
    mainNumber: Optional[bool] = None
    #: Indicates if a phone number is a toll free number.
    #: example: True
    tollFreeNumber: Optional[bool] = None
    #: Indicates Telephony type for the number.
    #: example: MOBILE_NUMBER
    includedTelephonyTypes: Optional[TelephonyType] = None
    #: Mobile Network for the number if number is MOBILE_NUMBER.
    #: example: mobileNetwork
    mobileNetwork: Optional[str] = None
    #: Routing Profile for the number if number is MOBILE_NUMBER.
    #: example: AttRtPf
    routingProfile: Optional[str] = None
    location: Optional[NumberListGetObjectLocation] = None
    owner: Optional[NumberListGetObjectOwner] = None

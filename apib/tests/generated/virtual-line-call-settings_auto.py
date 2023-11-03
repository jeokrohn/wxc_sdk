from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ListVirtualLineObject', 'ListVirtualLineObjectExternalCallerIdNamePolicy', 'ListVirtualLineObjectLocation', 'ListVirtualLineObjectNumber', 'ReadTheListOfVirtualLinesResponse']


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
    extension: Optional[datetime] = None
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
    #: example: 1.0
    number_of_devices_assigned: Optional[int] = None
    #: Type of billing plan.
    #: example: BCOCP1
    billing_plan: Optional[str] = None


class ReadTheListOfVirtualLinesResponse(ApiModel):
    #: Array of virtual lines.
    virtual_lines: Optional[list[ListVirtualLineObject]] = None

from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetThirdPartyDeviceObject', 'PutThirdPartyDevice']


class GetThirdPartyDeviceObject(ApiModel):
    #: Manufacturer of the device.
    #: example: THIRD_PARTY
    manufacturer: Optional[str] = None
    #: The Line/Port identifies a device endpoint in standalone mode or a SIP URI public identity in IMS mode.
    #: example: lg1_sias10_cpapi16004_LGU@64941297.int10.bcld.webex.com
    line_port: Optional[str] = None
    #: Contains the body of the HTTP response received following the request to the Console API. Not set if the response has no body.
    #: example: hs17.hosted-int.bcld.webex.com
    outbound_proxy: Optional[str] = None
    #: Device manager(s).
    #: example: CUSTOMER
    managed_by: Optional[str] = None
    #: SIP authentication user name for the owner of the device.
    #: example: 392829
    sip_user_name: Optional[str] = None


class PutThirdPartyDevice(ApiModel):
    #: Password to be updated.
    #: example: Test4Password123&
    sip_password: Optional[str] = None

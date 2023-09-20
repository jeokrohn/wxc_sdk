from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetCallRecordingObject', 'GetCallRecordingObjectOrganization', 'GetCallRecordingTermsOfServiceObject', 'GetComplianceAnnouncementObject', 'GetOrgComplianceAnnouncementObject', 'ModifyCallRecordingSettingsObject', 'ModifyCallRecordingTermsOfServiceObject']


class GetCallRecordingObjectOrganization(ApiModel):
    #: A unique identifier for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9lNTEzMTg1Zi01YTJmLTQ0OTUtYjM1Yi03MDY3YmY3Y2U0OGU
    id: Optional[str] = None
    #: A unique name for the organization.
    #: example: Alaska Cisco Organization
    name: Optional[str] = None


class GetCallRecordingObject(ApiModel):
    #: Details of the organization.
    organization: Optional[GetCallRecordingObjectOrganization] = None
    #: Whether or not the call recording is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: A unique identifier for the vendor.
    #: example: Y2lzY29zcGFyazovL3VzL1JFQ09SRElOR19WRU5ET1IvNTNkYzRjODctODQwOC00ODgyLTk1NzAtZGNhMmJjZGI5Mjgw
    vendorId: Optional[str] = None
    #: A unique name for the vendor.
    #: example: Dubber
    vendorName: Optional[str] = None
    #: Url where can be found terms of service for the vendor.
    #: example: https://www.dubber.net/terms
    termsOfServiceUrl: Optional[str] = None


class GetCallRecordingTermsOfServiceObject(ApiModel):
    #: A unique identifier for the vendor.
    #: example: Y2lzY29zcGFyazovL3VzL1JFQ09SRElOR19WRU5ET1IvNTNkYzRjODctODQwOC00ODgyLTk1NzAtZGNhMmJjZGI5Mjgw
    vendorId: Optional[str] = None
    #: A unique name for the vendor.
    #: example: Dubber
    vendorName: Optional[str] = None
    #: Whether or not the call recording terms of service are enabled.
    #: example: True
    termsOfServiceEnabled: Optional[bool] = None
    #: Url where can be found terms of service for the vendor.
    #: example: https://www.dubber.net/terms
    termsOfServiceUrl: Optional[str] = None


class GetComplianceAnnouncementObject(ApiModel):
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an inbound caller.
    #: example: True
    inboundPSTNCallsEnabled: Optional[bool] = None
    #: Flag to indicate whether to use the customer level compliance announcement default settings.
    #: example: True
    useOrgSettingsEnabled: Optional[bool] = None
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an outbound caller.
    outboundPSTNCallsEnabled: Optional[bool] = None
    #: Flag to indicate whether compliance announcement is played after a specified delay in seconds.
    outboundPSTNCallsDelayEnabled: Optional[bool] = None
    #: Number of seconds to wait before playing the compliance announcement.
    #: example: 10.0
    delayInSeconds: Optional[int] = None


class GetOrgComplianceAnnouncementObject(ApiModel):
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an inbound caller.
    #: example: True
    inboundPSTNCallsEnabled: Optional[bool] = None
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an outbound caller.
    outboundPSTNCallsEnabled: Optional[bool] = None
    #: Flag to indicate whether compliance announcement is played after a specified delay in seconds.
    outboundPSTNCallsDelayEnabled: Optional[bool] = None
    #: Number of seconds to wait before playing the compliance announcement.
    #: example: 10.0
    delayInSeconds: Optional[int] = None


class ModifyCallRecordingSettingsObject(ApiModel):
    #: Whether or not the call recording is enabled.
    #: example: True
    enabled: Optional[bool] = None


class ModifyCallRecordingTermsOfServiceObject(ApiModel):
    #: Whether or not the call recording terms of service are enabled.
    #: example: True
    termsOfServiceEnabled: Optional[bool] = None

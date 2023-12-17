from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['BetaFeaturesSupportNativeCallRecordingApi', 'GetCallRecordingObject',
            'GetCallRecordingObjectOrganization', 'GetCallRecordingTermsOfServiceObject']


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
    vendor_id: Optional[str] = None
    #: A unique name for the vendor.
    #: example: Dubber
    vendor_name: Optional[str] = None
    #: URL where can be found terms of service for the vendor.
    #: 
    #: **NOTE**: This is expected to be empty for Webex Recording Platform.
    #: example: https://www.dubber.net/terms
    terms_of_service_url: Optional[str] = None


class GetCallRecordingTermsOfServiceObject(ApiModel):
    #: A unique identifier for the vendor.
    #: example: Y2lzY29zcGFyazovL3VzL1JFQ09SRElOR19WRU5ET1IvNTNkYzRjODctODQwOC00ODgyLTk1NzAtZGNhMmJjZGI5Mjgw
    vendor_id: Optional[str] = None
    #: A unique name for the vendor.
    #: example: Dubber
    vendor_name: Optional[str] = None
    #: Whether or not the call recording terms of service are enabled.
    #: example: True
    terms_of_service_enabled: Optional[bool] = None
    #: URL where can be found terms of service for the vendor.
    #: 
    #: **NOTE**: This is expected to be empty for Webex Recording Platform.
    #: example: https://www.dubber.net/terms
    terms_of_service_url: Optional[str] = None


class BetaFeaturesSupportNativeCallRecordingApi(ApiChild, base='telephony/config/callRecording'):
    """
    Beta Features: Support Native Call Recording
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Features: Call Recording supports reading and writing of Webex Calling Call Recording settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def get_call_recording_settings(self, org_id: str = None) -> GetCallRecordingObject:
        """
        Get Call Recording Settings

        Retrieve Call Recording settings for the organization.

        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.

        Retrieving call recording settings requires a full or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve call recording settings from this organization.
        :type org_id: str
        :rtype: :class:`GetCallRecordingObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = GetCallRecordingObject.model_validate(data)
        return r

    def get_call_recording_terms_of_service_settings(self, vendor_id: str,
                                                     org_id: str = None) -> GetCallRecordingTermsOfServiceObject:
        """
        Get Call Recording Terms Of Service Settings

        Retrieve Call Recording Terms Of Service settings for the organization.

        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.

        Retrieving call recording terms of service settings requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param vendor_id: Retrieve call recording terms of service details for the given vendor.
        :type vendor_id: str
        :param org_id: Retrieve call recording terms of service details from this organization.
        :type org_id: str
        :rtype: :class:`GetCallRecordingTermsOfServiceObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'vendors/{vendor_id}/termsOfService')
        data = super().get(url, params=params)
        r = GetCallRecordingTermsOfServiceObject.model_validate(data)
        return r

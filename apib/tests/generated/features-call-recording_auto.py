from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['FeaturesCallRecordingApi', 'GetCallRecordingObject', 'GetCallRecordingObjectOrganization',
           'GetCallRecordingTermsOfServiceObject', 'GetComplianceAnnouncementObject',
           'GetOrgComplianceAnnouncementObject']


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
    #: Url where can be found terms of service for the vendor.
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
    #: Url where can be found terms of service for the vendor.
    #: 
    #: **NOTE**: This is expected to be empty for Webex Recording Platform.
    #: example: https://www.dubber.net/terms
    terms_of_service_url: Optional[str] = None


class GetComplianceAnnouncementObject(ApiModel):
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an inbound caller.
    #: example: True
    inbound_pstncalls_enabled: Optional[bool] = Field(alias='inboundPSTNCallsEnabled', default=None)
    #: Flag to indicate whether to use the customer level compliance announcement default settings.
    #: example: True
    use_org_settings_enabled: Optional[bool] = None
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an outbound caller.
    outbound_pstncalls_enabled: Optional[bool] = Field(alias='outboundPSTNCallsEnabled', default=None)
    #: Flag to indicate whether compliance announcement is played after a specified delay in seconds.
    outbound_pstncalls_delay_enabled: Optional[bool] = Field(alias='outboundPSTNCallsDelayEnabled', default=None)
    #: Number of seconds to wait before playing the compliance announcement.
    #: example: 10
    delay_in_seconds: Optional[int] = None


class GetOrgComplianceAnnouncementObject(ApiModel):
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an inbound caller.
    #: example: True
    inbound_pstncalls_enabled: Optional[bool] = Field(alias='inboundPSTNCallsEnabled', default=None)
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an outbound caller.
    outbound_pstncalls_enabled: Optional[bool] = Field(alias='outboundPSTNCallsEnabled', default=None)
    #: Flag to indicate whether compliance announcement is played after a specified delay in seconds.
    outbound_pstncalls_delay_enabled: Optional[bool] = Field(alias='outboundPSTNCallsDelayEnabled', default=None)
    #: Number of seconds to wait before playing the compliance announcement.
    #: example: 10
    delay_in_seconds: Optional[int] = None


class FeaturesCallRecordingApi(ApiChild, base='telephony/config'):
    """
    Features:  Call Recording
    
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
        url = self.ep('callRecording')
        data = super().get(url, params=params)
        r = GetCallRecordingObject.model_validate(data)
        return r

    def update_call_recording_settings(self, enabled: bool, org_id: str = None):
        """
        Update Call Recording Settings

        Update Call Recording settings for the organization.

        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.

        Updating call recording settings requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **NOTE**: This API is for Cisco partners only.

        :param enabled: Whether or not the call recording is enabled.
        :type enabled: bool
        :param org_id: Retrieve call recording settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep('callRecording')
        super().put(url, params=params, json=body)

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
        url = self.ep(f'callRecording/vendors/{vendor_id}/termsOfService')
        data = super().get(url, params=params)
        r = GetCallRecordingTermsOfServiceObject.model_validate(data)
        return r

    def update_call_recording_terms_of_service_settings(self, vendor_id: str, terms_of_service_enabled: bool,
                                                        org_id: str = None):
        """
        Update Call Recording Terms Of Service Settings

        Update Call Recording Terms Of Service settings for the given vendor.

        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.

        Updating call recording terms of service settings requires a full administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param vendor_id: Update call recording terms of service settings for the given vendor.
        :type vendor_id: str
        :param terms_of_service_enabled: Whether or not the call recording terms of service are enabled.
        :type terms_of_service_enabled: bool
        :param org_id: Update call recording terms of service settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['termsOfServiceEnabled'] = terms_of_service_enabled
        url = self.ep(f'callRecording/vendors/{vendor_id}/termsOfService')
        super().put(url, params=params, json=body)

    def get_details_for_the_organization_compliance_announcement_setting(self,
                                                                         org_id: str = None) -> GetOrgComplianceAnnouncementObject:
        """
        Get Details for the organization compliance announcement setting

        Retrieve the organization compliance announcement settings.

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Retrieving organization compliance announcement setting requires a full or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve compliance announcement setting from this organization.
        :type org_id: str
        :rtype: :class:`GetOrgComplianceAnnouncementObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording/complianceAnnouncement')
        data = super().get(url, params=params)
        r = GetOrgComplianceAnnouncementObject.model_validate(data)
        return r

    def update_the_organization_compliance_announcement(self, inbound_pstncalls_enabled: bool = None,
                                                        outbound_pstncalls_enabled: bool = None,
                                                        outbound_pstncalls_delay_enabled: bool = None,
                                                        delay_in_seconds: int = None, org_id: str = None):
        """
        Update the organization compliance announcement.

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Updating the organization compliance announcement requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param inbound_pstncalls_enabled: Flag to indicate whether the Call Recording START/STOP announcement is played
            to an inbound caller.
        :type inbound_pstncalls_enabled: bool
        :param outbound_pstncalls_enabled: Flag to indicate whether the Call Recording START/STOP announcement is
            played to an outbound caller.
        :type outbound_pstncalls_enabled: bool
        :param outbound_pstncalls_delay_enabled: Flag to indicate whether compliance announcement is played after a
            specified delay in seconds.
        :type outbound_pstncalls_delay_enabled: bool
        :param delay_in_seconds: Number of seconds to wait before playing the compliance announcement.
        :type delay_in_seconds: int
        :param org_id: Update the compliance announcement setting from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if inbound_pstncalls_enabled is not None:
            body['inboundPSTNCallsEnabled'] = inbound_pstncalls_enabled
        if outbound_pstncalls_enabled is not None:
            body['outboundPSTNCallsEnabled'] = outbound_pstncalls_enabled
        if outbound_pstncalls_delay_enabled is not None:
            body['outboundPSTNCallsDelayEnabled'] = outbound_pstncalls_delay_enabled
        if delay_in_seconds is not None:
            body['delayInSeconds'] = delay_in_seconds
        url = self.ep('callRecording/complianceAnnouncement')
        super().put(url, params=params, json=body)

    def get_details_for_the_location_compliance_announcement_setting(self, location_id: str,
                                                                     org_id: str = None) -> GetComplianceAnnouncementObject:
        """
        Get Details for the location compliance announcement setting

        Retrieve the location compliance announcement settings.

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Retrieving location compliance announcement setting requires a full or read-only administrator auth token with
        a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve compliance announcement settings for this location.
        :type location_id: str
        :param org_id: Retrieve compliance announcement setting from this organization.
        :type org_id: str
        :rtype: :class:`GetComplianceAnnouncementObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callRecording/complianceAnnouncement')
        data = super().get(url, params=params)
        r = GetComplianceAnnouncementObject.model_validate(data)
        return r

    def update_the_location_compliance_announcement(self, location_id: str, inbound_pstncalls_enabled: bool = None,
                                                    use_org_settings_enabled: bool = None,
                                                    outbound_pstncalls_enabled: bool = None,
                                                    outbound_pstncalls_delay_enabled: bool = None,
                                                    delay_in_seconds: int = None, org_id: str = None):
        """
        Update the location compliance announcement.

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Updating the location compliance announcement requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Update the compliance announcement settings for this location.
        :type location_id: str
        :param inbound_pstncalls_enabled: Flag to indicate whether the Call Recording START/STOP announcement is played
            to an inbound caller.
        :type inbound_pstncalls_enabled: bool
        :param use_org_settings_enabled: Flag to indicate whether to use the customer level compliance announcement
            default settings.
        :type use_org_settings_enabled: bool
        :param outbound_pstncalls_enabled: Flag to indicate whether the Call Recording START/STOP announcement is
            played to an outbound caller.
        :type outbound_pstncalls_enabled: bool
        :param outbound_pstncalls_delay_enabled: Flag to indicate whether compliance announcement is played after a
            specified delay in seconds.
        :type outbound_pstncalls_delay_enabled: bool
        :param delay_in_seconds: Number of seconds to wait before playing the compliance announcement.
        :type delay_in_seconds: int
        :param org_id: Update the compliance announcement setting from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if inbound_pstncalls_enabled is not None:
            body['inboundPSTNCallsEnabled'] = inbound_pstncalls_enabled
        if use_org_settings_enabled is not None:
            body['useOrgSettingsEnabled'] = use_org_settings_enabled
        if outbound_pstncalls_enabled is not None:
            body['outboundPSTNCallsEnabled'] = outbound_pstncalls_enabled
        if outbound_pstncalls_delay_enabled is not None:
            body['outboundPSTNCallsDelayEnabled'] = outbound_pstncalls_delay_enabled
        if delay_in_seconds is not None:
            body['delayInSeconds'] = delay_in_seconds
        url = self.ep(f'locations/{location_id}/callRecording/complianceAnnouncement')
        super().put(url, params=params, json=body)

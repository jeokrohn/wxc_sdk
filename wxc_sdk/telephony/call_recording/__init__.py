from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.common import IdAndName

__all__ = ['CallRecordingInfo', 'CallRecordingTermsOfService', 'OrgComplianceAnnouncement',
           'LocationComplianceAnnouncement', 'CallRecordingSettingsApi']


class CallRecordingInfo(ApiModel):
    #: Details of the organization.
    organization: Optional[IdAndName] = None
    #: Whether or not the call recording is enabled.
    enabled: Optional[bool] = None
    #: A unique identifier for the vendor.
    vendor_id: Optional[str] = None
    #: A unique name for the vendor.
    vendor_name: Optional[str] = None
    #: Url where can be found terms of service for the vendor.
    #:
    #: **NOTE**: This is expected to be empty for Webex Recording Platform.
    terms_of_service_url: Optional[str] = None


class CallRecordingTermsOfService(ApiModel):
    #: A unique identifier for the vendor.
    vendor_id: Optional[str] = None
    #: A unique name for the vendor.
    vendor_name: Optional[str] = None
    #: Whether or not the call recording terms of service are enabled.
    terms_of_service_enabled: Optional[bool] = None
    #: Url where can be found terms of service for the vendor.
    #:
    #: **NOTE**: This is expected to be empty for Webex Recording Platform.
    terms_of_service_url: Optional[str] = None


class OrgComplianceAnnouncement(ApiModel):
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an inbound caller.
    inbound_pstncalls_enabled: Optional[bool] = Field(alias='inboundPSTNCallsEnabled', default=None)
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an outbound caller.
    outbound_pstncalls_enabled: Optional[bool] = Field(alias='outboundPSTNCallsEnabled', default=None)
    #: Flag to indicate whether compliance announcement is played after a specified delay in seconds.
    outbound_pstncalls_delay_enabled: Optional[bool] = Field(alias='outboundPSTNCallsDelayEnabled', default=None)
    #: Number of seconds to wait before playing the compliance announcement.
    delay_in_seconds: Optional[int] = None


class LocationComplianceAnnouncement(OrgComplianceAnnouncement):
    #: Flag to indicate whether to use the customer level compliance announcement default settings.
    use_org_settings_enabled: Optional[bool] = None


class CallRecordingSettingsApi(ApiChild, base='telephony/config'):
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

    def read(self, org_id: str = None) -> CallRecordingInfo:
        """
        Get Call Recording Settings

        Retrieve Call Recording settings for the organization.

        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.

        Retrieving call recording settings requires a full or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve call recording settings from this organization.
        :type org_id: str
        :rtype: :class:`CallRecordingInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording')
        data = super().get(url, params=params)
        r = CallRecordingInfo.model_validate(data)
        return r

    def update(self, enabled: bool, org_id: str = None):
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

    def read_terms_of_service(self, vendor_id: str, org_id: str = None) -> CallRecordingTermsOfService:
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
        :rtype: :class:`CallRecordingTermsOfService`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'callRecording/vendors/{vendor_id}/termsOfService')
        data = super().get(url, params=params)
        r = CallRecordingTermsOfService.model_validate(data)
        return r

    def update_terms_of_service(self, vendor_id: str, enabled: bool, org_id: str = None):
        """
        Update Call Recording Terms Of Service Settings

        Update Call Recording Terms Of Service settings for the given vendor.

        Call Recording feature enables authorized agents to record any active call that Webex Contact Center manages.

        Updating call recording terms of service settings requires a full administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param vendor_id: Update call recording terms of service settings for the given vendor.
        :type vendor_id: str
        :param enabled: Whether or not the call recording terms of service are enabled.
        :type enabled: bool
        :param org_id: Update call recording terms of service settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['termsOfServiceEnabled'] = enabled
        url = self.ep(f'callRecording/vendors/{vendor_id}/termsOfService')
        super().put(url, params=params, json=body)

    def read_org_compliance_announcement(self, org_id: str = None) -> OrgComplianceAnnouncement:
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
        :rtype: :class:`OrgComplianceAnnouncement`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording/complianceAnnouncement')
        data = super().get(url, params=params)
        r = OrgComplianceAnnouncement.model_validate(data)
        return r

    def update_org_compliance_announcement(self, settings: OrgComplianceAnnouncement, org_id: str = None):
        """
        Update the organization compliance announcement

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Updating the organization compliance announcement requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param settings: new settings
        :type settings: OrgComplianceAnnouncement
        :param org_id: Update the compliance announcement setting from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('callRecording/complianceAnnouncement')
        super().put(url, params=params, json=body)

    def read_location_compliance_announcement(self, location_id: str,
                                              org_id: str = None) -> LocationComplianceAnnouncement:
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
        :rtype: :class:`LocationComplianceAnnouncement`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callRecording/complianceAnnouncement')
        data = super().get(url, params=params)
        r = LocationComplianceAnnouncement.model_validate(data)
        return r

    def update_location_compliance_announcement(self, location_id: str, settings: LocationComplianceAnnouncement,
                                                org_id: str = None):
        """
        Update the location compliance announcement

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Updating the location compliance announcement requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Update the compliance announcement settings for this location.
        :type location_id: str
        :param settings: new settings
        :type settings: LocationComplianceAnnouncement
        :param org_id: Update the compliance announcement setting from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'locations/{location_id}/callRecording/complianceAnnouncement')
        super().put(url, params=params, json=body)

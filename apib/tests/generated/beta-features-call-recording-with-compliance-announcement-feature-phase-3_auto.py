from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaFeaturesCallRecordingWithComplianceAnnouncementFeaturePhase3Api', 'GetComplianceAnnouncementObject',
           'GetOrgComplianceAnnouncementObject']


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


class BetaFeaturesCallRecordingWithComplianceAnnouncementFeaturePhase3Api(ApiChild, base='telephony/config'):
    """
    Beta Features:  Call Recording with Compliance Announcement Feature Phase 3
    
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

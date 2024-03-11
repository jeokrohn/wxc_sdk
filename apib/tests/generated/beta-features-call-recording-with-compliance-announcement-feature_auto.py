from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaFeaturesCallRecordingWithComplianceAnnouncementFeatureApi']


class BetaFeaturesCallRecordingWithComplianceAnnouncementFeatureApi(ApiChild, base='telephony/config/locations'):
    """
    Beta Features:  Call Recording with Compliance Announcement Feature
    
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

    def get_details_for_the_location_compliance_announcement_setting(self, location_id: str,
                                                                     org_id: str = None) -> bool:
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
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/callRecording/complianceAnnouncement')
        data = super().get(url, params=params)
        r = data['inboundPSTNCallsEnabled']
        return r

    def update_the_location_compliance_announcement(self, location_id: str, inbound_pstncalls_enabled: bool = None,
                                                    org_id: str = None):
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
            to an internal caller.
        :type inbound_pstncalls_enabled: bool
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
        url = self.ep(f'{location_id}/callRecording/complianceAnnouncement')
        super().put(url, params=params, json=body)

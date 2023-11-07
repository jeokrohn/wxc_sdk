from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetComplianceAnnouncementObject']


class GetComplianceAnnouncementObject(ApiModel):
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an internal caller.
    #: example: True
    inbound_pstncalls_enabled: Optional[bool] = Field(alias='inboundPSTNCallsEnabled', default=None)


class BetaFeaturesCallRecordingWithComplianceAnnouncementFeatureApi(ApiChild, base='telephony/config/locations/{locationId}/callRecording/complianceAnnouncement'):
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
    ...
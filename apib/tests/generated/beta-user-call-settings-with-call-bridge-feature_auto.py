from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CallBridgeInfo']


class CallBridgeInfo(ApiModel):
    #: Indicates that a stutter dial tone will be played to all the participants when a person is bridged on the active
    #: shared line call.
    warning_tone_enabled: Optional[bool] = None


class BetaUserCallSettingsWithCallBridgeFeatureApi(ApiChild, base='telephony/config/people/{personId}/features/callBridge'):
    """
    Beta User Call Settings with Call Bridge Feature
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    Person Call Settings supports modifying Webex Calling settings for a specific person.
    
    Viewing People requires a full, user, or read-only administrator auth token with a scope of
    `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by a
    person to read their own settings.
    
    Configuring People settings requires a full or user administrator auth token with the `spark-admin:people_write`
    scope or, for select APIs, a user auth token with `spark:people_write` scope can be used by a person to update
    their own settings.
    """
    ...
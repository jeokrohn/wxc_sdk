from collections.abc import Generator
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

    def read_call_bridge_settings_for_a_person(self, person_id: str, org_id: str = None) -> bool:
        """
        Read Call Bridge Settings for a Person

        Retrieve a person's Call Bridge settings.
        
        This API requires a full, user or read-only administrator or location administrator auth token with a scope of
        `spark-admin:people_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: bool
        """
        ...


    def configure_call_bridge_settings_for_a_person(self, person_id: str, warning_tone_enabled: bool,
                                                    org_id: str = None):
        """
        Configure Call Bridge Settings for a Person

        Configure a person's Call Bridge settings.
        
        This API requires a full or user administrator or location administrator auth token with the
        `spark-admin:people_write` scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param warning_tone_enabled: Set to enable or disable a stutter dial tone being played to all the participants
            when a person is bridged on the active shared line call.
        :type warning_tone_enabled: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        ...

    ...
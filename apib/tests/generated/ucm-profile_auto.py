from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['GetManagerProfileObject', 'UCMProfileApi']


class GetManagerProfileObject(ApiModel):
    #: A unique identifier for the calling UC Manager Profile.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExJTkdfUFJPRklMRS9iMzdmMmZiYS0yZTdjLTExZWItYTM2OC1kYmU0Yjc2NzFmZTk
    id: Optional[str] = None
    #: Unique name for the calling UC Manager Profile.
    #: example: UC Profile2
    name: Optional[str] = None


class UCMProfileApi(ApiChild, base='telephony/config/callingProfiles'):
    """
    UCM Profile
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    UCM Profiles supports reading and writing of UC Profile relatedsettings for a specific organization or person.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    Viewing people settings requires a full, user, or read-only administrator auth token with a scope of
    `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by a
    person to read their own settings.
    
    Configuring people settings requires a full or user administrator auth token with the `spark-admin:people_write`
    scope or, for select APIs, a user auth token with `spark:people_write` scope can be used by a person to update
    their own settings.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_uc_manager_profiles(self, org_id: str = None) -> list[GetManagerProfileObject]:
        """
        Read the List of UC Manager Profiles

        List all calling UC Manager Profiles for the organization.

        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in Webex
        (Unified CM).

        The UC Manager Profile has an organization-wide default and may be overridden for individual persons, although
        currently only setting at a user level is supported by Webex APIs.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:people_read` as this API is designed to be used in conjunction with calling behavior at the user
        level.

        :param org_id: List manager profiles in this organization.
        :type org_id: str
        :rtype: list[GetManagerProfileObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[GetManagerProfileObject]).validate_python(data['callingProfiles'])
        return r

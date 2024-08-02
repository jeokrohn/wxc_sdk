from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ClientCallSettingsApi', 'GetCustomerMSTeamsSettingsObject', 'GetCustomerMSTeamsSettingsObjectLevel',
           'SettingsObject', 'SettingsObjectSettingName']


class GetCustomerMSTeamsSettingsObjectLevel(str, Enum):
    #: `settingName` configured at the `GLOBAL` `level`.
    global_ = 'GLOBAL'
    #: `settingName` configured at the `ORGANIZATION` `level`.
    organization = 'ORGANIZATION'


class SettingsObjectSettingName(str, Enum):
    #: Webex will continue to run but its windows will be closed by default. Users can still access Webex from the
    #: system tray on Windows or the Menu Bar on Mac.
    hide_webex_app = 'HIDE_WEBEX_APP'
    #: Sync presence status between Microsoft Teams and Webex.
    presence_sync = 'PRESENCE_SYNC'


class SettingsObject(ApiModel):
    #: Name of the setting retrieved.
    #: example: HIDE_WEBEX_APP
    setting_name: Optional[SettingsObjectSettingName] = None
    #: Either `true` or `false` for the respective `settingName` to be retrieved.
    #: example: True
    value: Optional[bool] = None
    #: The date and time when the respective `settingName` was last updated.
    #: example: 2024-02-24T07:21:23.494198Z
    last_modified: Optional[datetime] = None


class GetCustomerMSTeamsSettingsObject(ApiModel):
    #: Level at which the `settingName` has been set.
    #: example: ORGANIZATION
    level: Optional[GetCustomerMSTeamsSettingsObjectLevel] = None
    #: Unique identifier for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi84NzU2ZjkwZS1iZDg4LTRhOTQtOGZiZC0wMzM2NzhmMDU5ZjM
    org_id: Optional[str] = None
    #: Array of `SettingsObject`.
    settings: Optional[list[SettingsObject]] = None


class ClientCallSettingsApi(ApiChild, base='telephony/config/settings/msTeams'):
    """
    Client Call Settings
    
    Client Call Settings supports reading and writing of Webex Calling client settings for a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def get_an_organization_s_ms_teams_settings(self, org_id: str = None) -> GetCustomerMSTeamsSettingsObject:
        """
        Get an Organization's MS Teams Settings

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>

        Get organization MS Teams settings.

        At an organization level, MS Teams settings allow access to viewing the `HIDE WEBEX APP` and `PRESENCE SYNC`
        settings.

        To retrieve an organization's MS Teams settings requires a full or read-only administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve MS Teams settings for the organization.
        :type org_id: str
        :rtype: :class:`GetCustomerMSTeamsSettingsObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = GetCustomerMSTeamsSettingsObject.model_validate(data)
        return r

    def update_an_organization_s_ms_teams_setting(self, setting_name: SettingsObjectSettingName, value: bool,
                                                  org_id: str = None):
        """
        Update an Organization's MS Teams Setting

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>

        Update an MS Teams setting.

        MS Teams setting can be updated at the organization level.

        Requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param setting_name: The enum value, either `HIDE_WEBEX_APP` or `PRESENCE_SYNC`, for the respective
            `settingName` to be updated.
        :type setting_name: SettingsObjectSettingName
        :param value: The boolean value, either `true` or `false`, for the respective `settingName` to be updated.
        :type value: bool
        :param org_id: Update MS Teams setting value for the organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['settingName'] = enum_str(setting_name)
        body['value'] = value
        url = self.ep()
        super().put(url, params=params, json=body)

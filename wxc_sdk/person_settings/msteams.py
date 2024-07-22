from datetime import datetime
from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['MSTeamsSettings', 'SettingsObject', 'MSTeamsSettingApi']


class SettingsObject(ApiModel):
    #: Name of the setting retrieved.
    setting_name: Optional[str] = None
    #: Level at which the `settingName` has been set.
    level: Optional[str] = None
    #: Either `true` or `false` for the respective `settingName` to be retrieved.
    value: Optional[bool] = None
    #: The date and time when the respective `settingName` was last updated.
    last_modified: Optional[datetime] = None


class MSTeamsSettings(ApiModel):
    #: Unique identifier for the person.
    person_id: Optional[str] = None
    #: Unique identifier for the organization in which the person resides.
    org_id: Optional[str] = None
    #: Array of `SettingsObject`.
    settings: Optional[list[SettingsObject]] = None


class MSTeamsSettingApi(ApiChild, base='telephony/config/people'):
    def read(self, person_id: str,
             org_id: str = None) -> MSTeamsSettings:
        """
        Retrieve a Person's MS Teams Settings

        At a person level, MS Teams settings allow access to retrieving the `HIDE WEBEX APP` and `PRESENCE SYNC`
        settings.

        To retrieve a person's MS Teams settings requires a full or read-only administrator auth token with a scope
        of `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter since the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`MSTeamsSettings`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/settings/msTeams')
        data = super().get(url, params=params)
        r = MSTeamsSettings.model_validate(data)
        return r

    def configure(self, person_id: str,
                  setting_name: str, value: bool,
                  org_id: str = None):
        """
        Configure a Person's MS Teams Setting

        MS Teams settings can be configured at the person level.

        Requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param setting_name: The enum value to be set to `HIDE_WEBEX_APP`.
        :type setting_name: str
        :param value: The boolean value to update the `HIDE_WEBEX_APP` setting, either `true` or `false`. Set to `null`
            to delete the `HIDE_WEBEX_APP` setting.
        :type value: bool
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter since the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['settingName'] = setting_name
        body['value'] = value
        url = self.ep(f'{person_id}/settings/msTeams')
        super().put(url, params=params, json=body)

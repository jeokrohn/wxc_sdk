from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel

__all__ = ['HotDeskingSigninViaVoicePortalApi', 'HotDeskingVoicePortalSetting']


class HotDeskingVoicePortalSetting(ApiModel):
    enabled: bool = Field(alias='voicePortalHotDeskSignInEnabled')


class HotDeskingSigninViaVoicePortalApi(ApiChild, base='telephony/config'):
    """
    Features: Hot Desking Sign-in via Voice Portal

    Features: Hot desking is a feature that allows users to sign in to a shared phone and make calls using their own
    phone number.

    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.

    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.

    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def location_get(self, location_id: str, org_id: str = None) -> HotDeskingVoicePortalSetting:
        """
        Voice Portal Hot desking sign in details for a location

        Get the Hot desking sign in details for a location.

        This requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Location in which the hot desking sign in resides.
        :type location_id: str
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: HotDeskingVoicePortalSetting
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/features/hotDesking')
        data = super().get(url, params=params)
        return HotDeskingVoicePortalSetting.model_validate(data)

    def location_update(self, location_id: str,
                        setting: HotDeskingVoicePortalSetting,
                        org_id: str = None):
        """
        Update Voice Portal Hot desking sign in details for a location

        Update the Hot desking sign in details for a location.

        This requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location in which the hot desking sign in resides.
        :type location_id: str
        :param setting: Hot desking sign in details for a location.
        :type setting: HotDeskingVoicePortalSetting
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = setting.model_dump(mode='json', by_alias=True, exclude_unset=True)
        url = self.ep(f'locations/{location_id}/features/hotDesking')
        super().put(url, params=params, json=body)

    def user_get(self, person_id: str, org_id: str = None) -> HotDeskingVoicePortalSetting:
        """
        Voice Portal Hot desking sign in details for a user

        Get the Hot desking sign in details for a user.

        This requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param person_id: ID of the person associated with the hot desking details.
        :type person_id: str
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: HotDeskingVoicePortalSetting
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/hotDesking/guest')
        data = super().get(url, params=params)
        return HotDeskingVoicePortalSetting.model_validate(data)

    def user_update(self, person_id: str,
                    setting: HotDeskingVoicePortalSetting,
                    org_id: str = None):
        """
        Update Voice Portal Hot desking sign in details for a user

        Update the Hot desking sign in details for a user.

        This requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: ID of the person associated with the hot desking details.
        :type person_id: str
        :param setting: Hot desking sign in details for a user.
        :type setting: HotDeskingVoicePortalSetting
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = setting.model_dump(mode='json', by_alias=True, exclude_unset=True)
        url = self.ep(f'people/{person_id}/features/hotDesking/guest')
        super().put(url, params=params, json=body)

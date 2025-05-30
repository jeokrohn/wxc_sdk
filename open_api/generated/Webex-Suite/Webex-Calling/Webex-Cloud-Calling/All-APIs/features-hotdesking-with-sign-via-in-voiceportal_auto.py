from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['FeaturesHotDeskingSigninViaVoicePortalApi']


class FeaturesHotDeskingSigninViaVoicePortalApi(ApiChild, base='telephony/config'):
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

    def voice_portal_hot_desking_sign_in_details_for_a_location(self, location_id: str, org_id: str = None) -> bool:
        """
        Voice Portal Hot desking sign in details for a location

        Get the Hot desking sign in details for a location.

        This requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Location in which the hot desking sign in resides.
        :type location_id: str
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/features/hotDesking')
        data = super().get(url, params=params)
        r = data['voicePortalHotDeskSignInEnabled']
        return r

    def update_voice_portal_hot_desking_sign_in_details_for_a_location(self, location_id: str,
                                                                       voice_portal_hot_desk_sign_in_enabled: bool = None,
                                                                       org_id: str = None):
        """
        Update Voice Portal Hot desking sign in details for a location

        Update the Hot desking sign in details for a location.

        This requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Location in which the hot desking sign in resides.
        :type location_id: str
        :param voice_portal_hot_desk_sign_in_enabled: If `true`, hot desking sign in via the Voice Portal is enabled.
        :type voice_portal_hot_desk_sign_in_enabled: bool
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if voice_portal_hot_desk_sign_in_enabled is not None:
            body['voicePortalHotDeskSignInEnabled'] = voice_portal_hot_desk_sign_in_enabled
        url = self.ep(f'locations/{location_id}/features/hotDesking')
        super().put(url, params=params, json=body)

    def voice_portal_hot_desking_sign_in_details_for_a_user(self, person_id: str, org_id: str = None) -> bool:
        """
        Voice Portal Hot desking sign in details for a user

        Get the Hot desking sign in details for a user.

        This requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param person_id: ID of the person associated with the hot desking details.
        :type person_id: str
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'people/{person_id}/features/hotDesking/guest')
        data = super().get(url, params=params)
        r = data['voicePortalHotDeskSignInEnabled']
        return r

    def update_voice_portal_hot_desking_sign_in_details_for_a_user(self, person_id: str,
                                                                   voice_portal_hot_desk_sign_in_enabled: bool = None,
                                                                   org_id: str = None):
        """
        Update Voice Portal Hot desking sign in details for a user

        Update the Hot desking sign in details for a user.

        This requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param person_id: ID of the person associated with the hot desking details.
        :type person_id: str
        :param voice_portal_hot_desk_sign_in_enabled: If `true`, hot desking sign in via the Voice Portal is enabled.
        :type voice_portal_hot_desk_sign_in_enabled: bool
        :param org_id: ID of the organization. Only admin users of another organization (such as partners) may use this
            parameter as the default is the same organization as the token used to access the API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if voice_portal_hot_desk_sign_in_enabled is not None:
            body['voicePortalHotDeskSignInEnabled'] = voice_portal_hot_desk_sign_in_enabled
        url = self.ep(f'people/{person_id}/features/hotDesking/guest')
        super().put(url, params=params, json=body)

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild

__all__ = ['MeSecondaryLineCallerIdApi']

from wxc_sdk.me.callerid import MeCallerIdSettings, MeSelectedCallerId


class MeSecondaryLineCallerIdApi(ApiChild, base='telephony/config/people/me'):

    def available_caller_id_list(self, lineowner_id: str) -> list[MeSelectedCallerId]:
        """
        Get My Secondary Line Owner's Available Caller ID List

        Get details of available caller IDs for a secondary line of the authenticated user.

        Note that an authenticated user can only retrieve information for their configured secondary lines.

        Caller ID settings control how a person's information is displayed when making outgoing calls.
        The available caller ID list shows the caller IDs that the user can choose from.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str

        :rtype: MeSelectedCallerId
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/availableCallerIds')
        data = super().get(url)
        r = TypeAdapter(list[MeSelectedCallerId]).validate_python(data['availableCallerIds'])
        return r

    def settings(self, lineowner_id: str) -> MeCallerIdSettings:
        """
        Get My Secondary Line Owner Caller ID Settings

        Get Caller ID Settings for the secondary line owner of the authenticated user.

        Note that the secondary line information is only available for the authenticated user.

        Calling Line ID Delivery Blocking in Webex prevents your name and phone number from being shown to people you
        call.
        Connected Line Identification Restriction allows you to block your name and phone number from being shown when
        receiving a call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: :class:`CallerIdSettingsGet`
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callerId')
        data = super().get(url)
        r = MeCallerIdSettings.model_validate(data)
        return r

    def update(self, lineowner_id: str, settings: MeCallerIdSettings):
        """
        Update My Secondary Line Owner Caller ID Settings

        Update Caller ID Settings for the secondary line owner of the authenticated user.

        Note that the secondary line information is only available for the authenticated user.

        Calling Line ID Delivery Blocking in Webex prevents your name and phone number from being shown to people you
        call.
        Connected Line Identification Restriction allows you to block your name and phone number from being shown when
        receiving a call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :param settings: new settings
        :type settings: :class:`MeCallerIdSettings`
        """
        body = settings.model_dump(mode='json', by_alias=True, exclude_unset=True)
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/callerId')
        super().put(url, json=body)


    def get_selected_caller_id_settings(self, lineowner_id: str) -> MeSelectedCallerId:
        """
        Get My Secondary Line Owner's Selected Caller ID Settings

        Get details of selected caller ID settings associated with a secondary line of the authenticated user.

        Note that an authenticated user can only retrieve information for their configured secondary lines.

        Caller ID settings control how a person's information is displayed when making outgoing calls.
        Selected Caller ID settings allow users to choose which configuration among available caller IDs is selected
        currently.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: MeSelectedCallerId
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/selectedCallerId')
        data = super().get(url)
        r = MeSelectedCallerId.model_validate(data['selected'])
        return r

    def modify_selected_caller_id_settings(self, lineowner_id: str, settings: MeSelectedCallerId):
        """
        Update My Secondary Line Owner's Selected Caller ID Settings

        Update selected caller ID settings associated with a secondary line owner of the authenticated user.

        Note that an authenticated user can only modify information for their configured secondary lines.

        Caller ID settings control how a person's information is displayed when making outgoing calls.
        Selected Caller ID settings allow users to choose which configuration among available caller IDs is selected
        currently.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :param settings: new settings
        :type settings: :class:`MeSelectedCallerId`
        """
        body = settings.update()
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/selectedCallerId')
        super().put(url, json=body)

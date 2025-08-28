from typing import Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['MeCallerIdApi', 'MeCallerIdSettings', 'MeSelectedCallerId']


class CallerIdType(str, Enum):
    #: Caller ID is the default configured caller ID.
    default_clid = 'DEFAULT_CLID'
    #: Caller ID is an additional number caller ID.
    additional_clid = 'ADDITIONAL_CLID'
    #: Caller ID is associated with a call queue.
    call_queue = 'CALL_QUEUE'
    #: Caller ID is associated with a hunt group.
    hunt_group = 'HUNT_GROUP'


class MeCallerIdSettings(ApiModel):
    #: If `true`, the user's name and phone number are not shown to people they call.
    calling_line_id_delivery_blocking_enabled: Optional[bool] = None
    #: If `true`, the user's name and phone number are not shown when receiving a call.
    connected_line_identification_restriction_enabled: Optional[bool] = None


class MeSelectedCallerId(ApiModel):
    type: Optional[CallerIdType] = None
    #: Unique identifier of the selected caller ID config. Set for `CALL_QUEUE` & `HUNT_GROUP` caller IDs.
    id: Optional[str] = None
    #: Name of the selected caller ID.
    name: Optional[str] = None
    #: Direct number of the selected caller ID.
    direct_number: Optional[str] = None
    #: Extension of the selected caller ID.
    extension: Optional[str] = None

    def update(self) -> dict:
        """
        Prepare the object for an update operation by converting it to a dictionary.

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_unset=True,
                               include={'type', 'id', 'direct_number'})


class MeCallerIdApi(ApiChild, base='telephony/config/people/me'):

    def settings(self) -> MeCallerIdSettings:
        """
        Get My Caller ID Settings

        Get Caller ID Settings for the authenticated user.

        Calling Line ID Delivery Blocking in Webex prevents your name and phone number from being shown to people you
        call.
        Connected Line Identification Restriction allows you to block your name and phone number from being shown when
        receiving a call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`MeCallerIdSettings`
        """
        url = self.ep('settings/callerId')
        data = super().get(url)
        r = MeCallerIdSettings.model_validate(data)
        return r

    def update(self, settings: MeCallerIdSettings):
        """
        Update My Caller ID Settings

        Update Caller ID Settings for the authenticated user.

        Calling Line ID Delivery Blocking in Webex prevents your name and phone number from being shown to people you
        call.
        Connected Line Identification Restriction allows you to block your name and phone number from being shown when
        receiving a call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: new settings
        :type settings: :class:`MeCallerIdSettings`
        """
        body = settings.model_dump(mode='json', by_alias=True, exclude_unset=True)
        url = self.ep('settings/callerId')
        super().put(url, json=body)

    def available_caller_id_list(self) -> list[MeSelectedCallerId]:
        """
        Get My Available Caller ID List

        Get details of available caller IDs of the authenticated user.

        Caller ID settings control how a person's information is displayed when making outgoing calls.
        The available caller ID list shows the caller IDs that the user can choose from.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[MeSelectedCallerId]
        """
        url = self.ep('settings/availableCallerIds')
        data = super().get(url)
        r = TypeAdapter(list[MeSelectedCallerId]).validate_python(data['availableCallerIds'])
        return r

    def get_selected_caller_id_settings(self) -> MeSelectedCallerId:
        """
        Read My Selected Caller ID Settings

        Read selected caller ID settings associated with the authenticated user.

        Caller ID settings control how a person's information is displayed when making outgoing calls.
        Selected Caller ID settings allow users to choose which configuration among available caller IDs is selected
        currently.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: MeSelectedCallerId
        """
        url = self.ep('settings/selectedCallerId')
        data = super().get(url)
        r = MeSelectedCallerId.model_validate(data['selected'])
        return r

    def modify_selected_caller_id_settings(self, settings: MeSelectedCallerId):
        """
        Configure My Selected Caller ID Settings

        Update selected caller ID settings associated with the authenticated user.

        Caller ID settings control how a person's information is displayed when making outgoing calls.
        Selected Caller ID settings allow users to choose which configuration among available caller IDs is selected
        currently.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: new settings
        :type settings: :class:`MeSelectedCallerId`
        """
        body = settings.update()
        url = self.ep('settings/selectedCallerId')
        super().put(url, json=body)

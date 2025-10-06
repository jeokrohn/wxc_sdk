import urllib.parse
from typing import Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild

__all__ = ['MeCallBlockApi', 'CallBlockNumber']

from wxc_sdk.base import ApiModel


class CallBlockNumber(ApiModel):
    #: Unique identifier of the phone number.
    id: Optional[str] = None
    #: Phone number which is blocked by user.
    phone_number: Optional[str] = None


class MeCallBlockApi(ApiChild, base='telephony/config/people/me'):
    def settings(self) -> list[CallBlockNumber]:
        """
        Get My Call Block Settings

        Get details of call block settings associated with the authenticated user.

        Call block settings allow you to get the User Call Block Number List.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[CallBlockNumber]
        """
        url = self.ep('settings/callBlock')
        data = super().get(url)
        r = TypeAdapter(list[CallBlockNumber]).validate_python(data['numbers'])
        return r

    def add_number(self, phone_number: str) -> str:
        """
        Add a phone number to user's Call Block List

        Add a phone number to the call block list for the authenticated user.

        Call block settings allow you to get the User Call Block Number List.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param phone_number: Phone number which is blocked by user.
        :type phone_number: str
        :rtype: str
        """
        body = dict()
        body['phoneNumber'] = phone_number
        url = self.ep('settings/callBlock/numbers')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_number(self, phone_number_id: str):
        """
        Delete User Call Block Number

        Delete call block number settings associated with the authenticated user.

        Call block settings allow you to delete a number from the User Call Block Number List.

        This API requires a user auth token with a scope of `spark-admin:people_write`.

        :param phone_number_id: Unique identifier of the phone number.
        :type phone_number_id: str
        :rtype: None
        """
        url = self.ep(f'settings/callBlock/numbers/{phone_number_id}')
        super().delete(url)

    def state_for_number(self, phone_number_id: str) -> bool:
        """
        Get My Call Block State For Specific Number

        Get call block state details for a specific number associated with the authenticated user.

        Call block settings allow you to get the User Call Block Number List.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param phone_number_id: Unique identifier of the phone number.
        :type phone_number_id: str
        :rtype: bool
        """
        url = self.ep(f'settings/callBlock/numbers/{urllib.parse.quote(phone_number_id)}')
        data = super().get(url)
        r = data['blockCallsEnabled']
        return r

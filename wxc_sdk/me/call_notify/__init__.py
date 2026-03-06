from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.common.selective import SelectiveCriteria, SelectiveCrit

__all__ = ['MeCallNotifyApi', 'CallNotify', 'CallNotifyCriteria']


class CallNotify(ApiModel):
    #: Indicates whether the call notify feature is enabled for the user.
    enabled: Optional[bool] = None
    #: Email Address to which call notifications to be received.
    email_address: Optional[str] = None
    #: List of Call Notify Criteria configured by the user.
    criteria: Optional[list[SelectiveCrit]] = None


class CallNotifyCriteria(SelectiveCriteria):
    _enabled_attr = 'notificationEnabled'
    _phone_numbers = 'phoneNumbers'


class MeCallNotifyApi(ApiChild, base='telephony/config/people/me'):
    def get(self) -> CallNotify:
        """
        Get Call Notify Settings for User

        Get Call Notify Settings for the authenticated user.

        Call Notify allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the user
        wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`CallNotify`
        """
        url = self.ep('settings/callNotify')
        data = super().get(url)
        r = CallNotify.model_validate(data)
        return r

    def update(self, enabled: bool, email_address: str = None):
        """
        Modify Call Notify Settings for User

        Update Call Notify Settings for the authenticated user.

        Call Notify allows you to set up a unique ringtone based on predefined criteria. This API allows modifying
        attributes such as name, phoneNumbers etc for a particular criteria.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Indicates whether the call notify feature should be enabled or disabled for the user.
        :type enabled: bool
        :param email_address: Email Address to which call notifications to be received.
        :type email_address: str
        :rtype: None
        """
        body = dict()
        body['enabled'] = enabled
        if email_address is not None:
            body['emailAddress'] = email_address
        url = self.ep('settings/callNotify')
        super().put(url, json=body)

    def criteria_create(self, criteria: CallNotifyCriteria) -> str:
        """
        Add a Call Notify Criteria

        Create a Call Notify Criteria for the authenticated user.

        Call Notify allows you to set up a unique ringtone based on predefined criteria. This is helpful,
        when the user
        wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria: Criteria to be created.
        :rtype: str
        """
        body = criteria.update()
        url = self.ep('settings/callNotify/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def criteria_delete(self, criteria_id: str):
        """
        Delete a Call Notify Criteria

        Delete a Call Notify criteria for the authenticated user.

        Call Notify allows you to set up a unique ringtone based on predefined criteria. This API removes a specific
        criteria rule by its unique identifier.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the call notify criteria.
        :type criteria_id: str
        :rtype: None
        """
        url = self.ep(f'settings/callNotify/criteria/{criteria_id}')
        super().delete(url)

    def criteria_get(self, criteria_id: str) -> CallNotifyCriteria:
        """
        Get Call Notify Criteria Settings

        Get Call Notify Criteria Settings for the authenticated user.

        Call Notify allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the user
        wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param criteria_id: The `id` parameter specifies the unique identifier for the call notify criteria.
        :type criteria_id: str
        :rtype: :class:`CallNotifyCriteria`
        """
        url = self.ep(f'settings/callNotify/criteria/{criteria_id}')
        data = super().get(url)
        r = CallNotifyCriteria.model_validate(data)
        return r

    def criteria_update(self, criteria: CallNotifyCriteria, criteria_id: str = None):
        """
        Modify a Call Notify Criteria

        Modify Call Notify Criteria Settings for the authenticated user.

        Call Notify allows you to set up a unique ringtone based on predefined criteria. This API allows modifying
        attributes such as name, phoneNumbers etc for a particular criteria.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria: Criteria to be modified.
        :type criteria: :class:`CallNotifyCriteria`
        :param criteria_id: The `id` parameter specifies the unique identifier for the call notify criteria.
            Default: id from criteria
        :type criteria_id: str
        :rtype: None
        """
        criteria_id = criteria_id or criteria.id
        body = criteria.update()
        url = self.ep(f'settings/callNotify/criteria/{criteria_id}')
        super().put(url, json=body)

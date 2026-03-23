from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import E164Number
from wxc_sdk.common.selective import SelectiveCriteria
from wxc_sdk.person_settings.selective_forward import SelectiveForward

__all__ = ['MeSelectiveForwardApi', 'MeSelectiveForwardCriteria']


class MeSelectiveForwardCriteria(SelectiveCriteria):
    _enabled_attr = 'forwardEnabled'
    _phone_numbers = 'numbers'

    #: Phone number to forward calls to during this schedule.
    forward_to_phone_number: Optional[E164Number] = None
    #: Indicates whether calls that meet the criteria are forwarded to the destination phone number's voicemail.
    destination_voicemail_enabled: Optional[bool] = None


class MeSelectiveForwardApi(ApiChild, base='telephony/config/people/me'):
    def get(self) -> SelectiveForward:
        """
        Get Selective Call Forward Settings for User

        Get Selective Call Forward Settings for the authenticated user.

        Selective Call Forward allows you to create customized rules to forward specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`SelectiveForward`
        """
        url = self.ep('settings/selectiveForward')
        data = super().get(url)
        r = SelectiveForward.model_validate(data)
        return r

    def update(self, forward: SelectiveForward) -> None:
        """
        Modify Selective Call Forward Settings for User

        Update the Selective Call Forward Settings for the authenticated user.

        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number, identity, and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param forward: Selective Call Forward Settings
        :type forward: SelectiveForward
        :rtype: None
        """
        body = forward.update()
        url = self.ep('settings/selectiveForward')
        super().put(url, json=body)

    def criteria_create(self, criteria: MeSelectiveForwardCriteria) -> str:
        """
        Add a Selective Call Forwarding Criteria

        Create a Selective Call Forwarding Criteria for the authenticated user.

        Selective Call Forward allows you to define rules that automatically forward incoming calls based on specific
        criteria, such as the caller’s phone number, caller identity, and the time and day the call is received.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria: Selective Call Forward Criteria settings
        :type criteria: MeSelectiveForwardCriteria
        :rtype: str
        """
        body = criteria.update()
        url = self.ep('settings/selectiveForward/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def criteria_delete(self, criteria_id: str):
        """
        Delete a Selective Call Forwarding Criteria

        Delete a Selective Call Forwarding Criteria for the authenticated user.

        Selective call forwarding allows you to define rules that automatically forward incoming calls based on
        specific criteria. This API removes a specific criteria rule by its unique identifier.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the selective call
            forwarding criteria.
        :type criteria_id: str
        :rtype: None
        """
        url = self.ep(f'settings/selectiveForward/criteria/{criteria_id}')
        super().delete(url)

    def criteria_get(self, criteria_id: str) -> MeSelectiveForwardCriteria:
        """
        Get Settings for a Selective Call Forwarding Criteria

        Get settings for a Selective Call Forwarding Criteria for the authenticated user.

        Selective Call Forward allows you to define rules that automatically forward incoming calls based on specific
        criteria, such as the caller’s phone number, caller identity, and the time and day the call is received.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the selective call
          forwarding criteria.
        :type criteria_id: str
        :rtype: :class:`MeSelectiveForwardCriteria`
        """
        url = self.ep(f'settings/selectiveForward/criteria/{criteria_id}')
        data = super().get(url)
        r = MeSelectiveForwardCriteria.model_validate(data)
        return r

    def criteria_update(self, criteria: MeSelectiveForwardCriteria, criteria_id: str):
        """
        Modify Settings for a Selective Call Forwarding Criteria

        Modify settings for a Selective Call Forwarding Criteria for the authenticated user.

        Selective Call Forward allows you to define rules that automatically forward incoming calls based on specific
        criteria, such as the caller’s phone number, caller identity, and the time and day the call is received.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria: Selective Call Forward Criteria settings
        :type criteria: :class:`MeSelectiveForwardCriteria`
        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the selective call
            forwarding criteria. Default: id from criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL1oxNzU0MzgzODQzNTA5NzY`.
        :type criteria_id: str
        :rtype: None
        """
        criteria_id = criteria_id or criteria.id
        body = criteria.update()
        url = self.ep(f'settings/selectiveForward/criteria/{criteria_id}')
        super().put(url, json=body)

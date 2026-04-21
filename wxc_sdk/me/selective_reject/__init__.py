from wxc_sdk.api_child import ApiChild
from wxc_sdk.person_settings.selective_reject import SelectiveReject, SelectiveRejectCriteria

__all__ = ['MeSelectiveRejectApi']


class MeSelectiveRejectApi(ApiChild, base='telephony/config/people/me'):
    def get(self) -> SelectiveReject:  # type: ignore[override]
        """
        Get Selective Call Reject Settings for User

        Get Selective Call Reject Settings for the authenticated user.

        Selective Call Reject allows you to create customized rules to reject specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`SelectiveReject`
        """
        url = self.ep('settings/selectiveReject')
        data = super().get(url)
        r = SelectiveReject.model_validate(data)
        return r

    def update(self, enabled: bool):
        """
        Modify Selective Call Reject Settings for User

        Update Selective Call Reject Settings for the authenticated user.

        Selective Call Reject allows you to create customized rules to reject specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Indicates whether selective reject is enabled.
        :type enabled: bool
        :rtype: None
        """
        body = dict()
        body['enabled'] = enabled
        url = self.ep('settings/selectiveReject')
        super().put(url, json=body)

    def criteria_create(self, criteria: SelectiveRejectCriteria) -> str:
        """
        Add User Selective Call Reject Criteria

        Create a new Selective Call Reject Criteria for the authenticated user.

        Selective Call Reject allows you to create customized rules to reject specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria: Selective Call Reject Criteria settings
        :type criteria: SelectiveRejectCriteria
        :rtype: str
        """
        body = criteria.update()
        url = self.ep('settings/selectiveReject/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def criteria_delete(self, criteria_id: str):
        """
        Delete a Selective Call Reject Criteria

        Delete a Selective Call Reject Criteria for the authenticated user.

        Selective Call Reject allows you to create customized rules to reject specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the selective call reject
            criteria.
        :type criteria_id: str
        :rtype: None
        """
        url = self.ep(f'settings/selectiveReject/criteria/{criteria_id}')
        super().delete(url)

    def criteria_get(self, criteria_id: str) -> SelectiveRejectCriteria:
        """
        Get Selective Call Reject Criteria Settings for User

        Get Selective Call Reject Criteria Settings for the authenticated user.

        Selective Call Reject allows you to create customized rules to reject specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the selective call reject
            criteria.
        :type criteria_id: str
        :rtype: :class:`SelectiveRejectCriteria`
        """
        url = self.ep(f'settings/selectiveReject/criteria/{criteria_id}')
        data = super().get(url)
        r = SelectiveRejectCriteria.model_validate(data)
        return r

    def criteria_update(self, criteria: SelectiveRejectCriteria, criteria_id: str = None):
        """
        Modify a Selective Call Reject Criteria

        Modify Selective Call Reject Criteria Settings for the authenticated user.

        Selective Call Reject allows you to create customized rules to reject specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria: Selective Call Reject Criteria settings
        :type criteria: SelectiveRejectCriteria

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the selective call
            reject. Default: id from criteria.
        :type criteria_id: str
        :rtype: None
        """
        criteria_id = criteria_id or criteria.id
        body = criteria.update()
        url = self.ep(f'settings/selectiveReject/criteria/{criteria_id}')
        super().put(url, json=body)

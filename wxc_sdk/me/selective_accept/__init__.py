from wxc_sdk.api_child import ApiChild

__all__ = ['MeSelectiveAcceptApi']

from wxc_sdk.person_settings.selective_accept import SelectiveAccept, SelectiveAcceptCriteria


class MeSelectiveAcceptApi(ApiChild, base='telephony/config/people/me'):
    def get(self) -> SelectiveAccept:
        """
        Get Selective Call Accept Settings for User

        Get Selective Call Accept Settings for the authenticated user.

        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`SelectiveAccept`
        """
        url = self.ep('settings/selectiveAccept')
        data = super().get(url)
        r = SelectiveAccept.model_validate(data)
        return r

    def update(self, enabled: bool):
        """
        Modify Selective Call Accept Settings for User

        Update Selective Call Accept Settings for the authenticated user.

        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: indicates whether selective accept is enabled or not.
        :type enabled: bool
        :rtype: None
        """
        body = dict()
        body['enabled'] = enabled
        url = self.ep('settings/selectiveAccept')
        super().put(url, json=body)

    def criteria_create(self, criteria: SelectiveAcceptCriteria) -> str:
        """
        Add User Selective Call Accept Criteria

        Create a new Selective Call Accept Criteria for the authenticated user.

        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria: Selective Call Accept Criteria settings
        :type criteria: SelectiveAcceptCriteria
        :rtype: str
        """
        body = criteria.update()
        url = self.ep('settings/selectiveAccept/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def criteria_delete(self, criteria_id: str):
        """
        Delete a Selective Call Accept Criteria

        Delete a Selective Call Accept Criteria for the authenticated user.

        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the selective call accept
            criteria.
        :type criteria_id: str
        :rtype: None
        """
        url = self.ep(f'settings/selectiveAccept/criteria/{criteria_id}')
        super().delete(url)

    def criteria_get(self, criteria_id: str) -> SelectiveAcceptCriteria:
        """
        Get Selective Call Accept Criteria Settings for User

        Get Selective Call Accept Criteria Settings for the authenticated user.

        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the selective call accept
            criteria.
        :type criteria_id: str
        :rtype: :class:`SelectiveAcceptCallCriteriaGet`
        """
        url = self.ep(f'settings/selectiveAccept/criteria/{criteria_id}')
        data = super().get(url)
        r = SelectiveAcceptCriteria.model_validate(data)
        return r

    def criteria_update(self, criteria: SelectiveAcceptCriteria, criteria_id: str = None):
        """
        Modify a Selective Call Accept Criteria

        Modify Selective Call Accept Criteria Settings for the authenticated user.

        Selective Call Accept allows you to create customized rules to accept specific calls for users based on the
        phone number,identity and the time or day of the call.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria: Selective Call Accept Criteria settings
        :type criteria: SelectiveAcceptCriteria
        :param criteria_id: Specifies the unique identifier for the selective call accept criteria.
            Default: id from criteria
        :type criteria_id: str
        :rtype: None
        """
        criteria_id = criteria_id or criteria.id
        body = criteria.update()
        url = self.ep(f'settings/selectiveAccept/criteria/{criteria_id}')
        super().put(url, json=body)

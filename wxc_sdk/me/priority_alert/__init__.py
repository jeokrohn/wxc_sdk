from wxc_sdk.api_child import ApiChild
from wxc_sdk.person_settings.priority_alert import PriorityAlert, PriorityAlertCriteria

__all__ = ['MePriorityAlertApi']


class MePriorityAlertApi(ApiChild, base='telephony/config/people/me'):
    def get(self) -> PriorityAlert:
        """
        Get Priority Alert Settings

        Get Priority Alert Settings for the authenticated user.

        Priority alert allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the
        user wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`PriorityAlert`
        """
        url = self.ep('settings/priorityAlert')
        data = super().get(url)
        r = PriorityAlert.model_validate(data)
        return r

    def update(self, enabled: bool):
        """
        Modify Priority Alert Settings for User

        Update Priority Alert Settings for the authenticated user.

        Priority alert allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the
        user wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param enabled: Indicates whether the priority alert feature should be enabled or disabled for the user.
        :type enabled: bool
        :rtype: None
        """
        body = dict()
        body['enabled'] = enabled
        url = self.ep('settings/priorityAlert')
        super().put(url, json=body)

    def criteria_create(self, criteria: PriorityAlertCriteria) -> str:
        """
        Add a Priority Alert Criteria

        Create a Priority Alert Criteria for the authenticated user.

        Priority alert allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the
        user wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria: Priority Alert Criteria
        :type criteria: :class:`PriorityAlertCriteria`
        :rtype: str
        """
        body = criteria.update()
        url = self.ep('settings/priorityAlert/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def criteria_delete(self, criteria_id: str):
        """
        Delete a Priority Alert Criteria

        Delete a Priority Alert criteria for the authenticated user.

        Priority alert allows you to set up a unique ringtone based on predefined criteria. This API removes a specific
        criteria rule by its unique identifier.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the priority alert
            criteria.
        :type criteria_id: str
        :rtype: None
        """
        url = self.ep(f'settings/priorityAlert/criteria/{criteria_id}')
        super().delete(url)

    def criteria_get(self, criteria_id: str) -> PriorityAlertCriteria:
        """
        Get Priority Alert Criteria Settings

        Get Priority Alert Criteria Settings for the authenticated user.

        Priority alert allows you to set up a unique ringtone based on predefined criteria. This is helpful, when the
        user wants to be quickly notified that a specific phone number is calling.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the priority alert criteria.
        :type criteria_id: str
        :rtype: :class:`PriorityAlertCriteria`
        """
        url = self.ep(f'settings/priorityAlert/criteria/{criteria_id}')
        data = super().get(url)
        r = PriorityAlertCriteria.model_validate(data)
        return r

    def criteria_update(self, criteria: PriorityAlertCriteria, criteria_id: str = None):
        """
        Modify Settings for a Priority Alert Criteria

        Modify Priority Alert Criteria Settings for the authenticated user.

        Priority alert allows you to set up a unique ringtone based on predefined criteria. This API allows modifying
        attributes such as name, phoneNumbers etc for a particular criteria.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the priority alert criteria.
            Default: id from criteria
        :type criteria_id: str
        :param criteria: Priority Alert Criteria
        :type criteria: :class:`PriorityAlertCriteria`
        :rtype: None
        """
        criteria_id = criteria_id or criteria.id
        body = criteria.update()
        url = self.ep(f'settings/priorityAlert/criteria/{criteria_id}')
        super().put(url, json=body)

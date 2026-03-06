from wxc_sdk.api_child import ApiChild
from wxc_sdk.person_settings.sequential_ring import SequentialRing, SequentialRingCriteria

__all__ = ['MeSequentialRingApi']


class MeSequentialRingApi(ApiChild, base='telephony/config/people/me'):
    def get(self) -> SequentialRing:
        """
        Get Sequential Ring Settings for User

        Get Sequential Ring Settings for the authenticated user.

        Sequential Ring allows calls to ring additional phone numbers in sequence if the initial call is not answered.
        This can be configured to ring up to five phone numbers with customizable ring patterns.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`SequentialRing`
        """
        url = self.ep('settings/sequentialRing')
        data = super().get(url)
        r = SequentialRing.model_validate(data)
        return r

    def update(self, settings: SequentialRing):
        """
        Modify Sequential Ring Settings for User

        Update Sequential Ring Settings for the authenticated user.

        Sequential Ring allows calls to ring additional phone numbers in sequence if the initial call is not answered.
        This can be configured to ring up to five phone numbers with customizable ring patterns.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: New sequential ring settings
        :type settings: :class:`SequentialRing`
        :rtype: None
        """
        body = settings.update()
        url = self.ep('settings/sequentialRing')
        super().put(url, json=body)

    def criteria_create(self, criteria: SequentialRingCriteria) -> str:
        """
        Add User Sequential Ring Criteria

        Create a new Sequential Ring Criteria for the authenticated user.

        Sequential Ring criteria defines rules for when sequential ring should activate based on the caller and
        schedule.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria: New sequential ring criteria settings
        :type criteria: :class:`SequentialRingCriteria`
        :rtype: str
        """
        body = criteria.update()
        url = self.ep('settings/sequentialRing/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def criteria_delete(self, criteria_id: str):
        """
        Delete Sequential Ring Criteria

        Delete a Sequential Ring Criteria for the authenticated user.

        Sequential Ring criteria defines rules for when sequential ring should activate based on the caller and
        schedule.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the sequential ring
            criteria.
        :type criteria_id: str
        :rtype: None
        """
        url = self.ep(f'settings/sequentialRing/criteria/{criteria_id}')
        super().delete(url)

    def criteria_get(self, criteria_id: str) -> SequentialRingCriteria:
        """
        Get Sequential Ring Criteria Settings for User

        Get Sequential Ring Criteria Settings for the authenticated user.

        Sequential Ring criteria defines rules for when sequential ring should activate based on the caller and
        schedule.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the sequential ring
            criteria.
        :type criteria_id: str
        :rtype: :class:`SequentialRingCriteria`
        """
        url = self.ep(f'settings/sequentialRing/criteria/{criteria_id}')
        data = super().get(url)
        r = SequentialRingCriteria.model_validate(data)
        return r

    def criteria_update(self, criteria: SequentialRingCriteria, criteria_id: str=None):
        """
        Modify Sequential Ring Criteria Settings for User

        Update Sequential Ring Criteria Settings for the authenticated user.

        Sequential Ring criteria defines rules for when sequential ring should activate based on the caller and
        schedule.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param criteria: New sequential ring criteria settings
        :type criteria: :class:`SequentialRingCriteria`
        :param criteria_id: The `criteria_id` parameter specifies the unique identifier for the sequential ring
            criteria. Default: id from criteria
        :type criteria_id: str
        :rtype: None
        """
        criteria_id = criteria_id or criteria.id
        body = criteria.update()
        url = self.ep(f'settings/sequentialRing/criteria/{criteria_id}')
        super().put(url, json=body)

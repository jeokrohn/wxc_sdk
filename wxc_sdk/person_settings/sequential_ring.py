from typing import Optional

from wxc_sdk.base import ApiModel
from wxc_sdk.common.selective import SelectiveCriteria, SelectiveCrit
from wxc_sdk.person_settings.common import PersonSettingsApiChild

__all__ = ['SequentialRingNumber', 'SequentialRing', 'SequentialRingApi', 'SequentialRingCriteria']


class SequentialRingCriteria(SelectiveCriteria):
    _enabled_attr = 'ringEnabled'
    _phone_numbers = 'phoneNumbers'


class SequentialRingNumber(ApiModel):
    #: Phone number set as the sequential number.
    phone_number: Optional[str] = None
    #: When set to `true` the called party is required to press 1 on the keypad to receive the call.
    answer_confirmation_required_enabled: Optional[bool] = None
    #: The number of rings to the specified phone number before the call advances to the subsequent number in the
    #: sequence or goes to voicemail.
    number_of_rings: Optional[int] = None


class SequentialRing(ApiModel):
    #: When set to `true` sequential ring is enabled.
    enabled: Optional[bool] = None
    #: When set to `true`, the webex calling primary line will ring first.
    ring_base_location_first_enabled: Optional[bool] = None
    #: The number of times the primary line will ring.
    base_location_number_of_rings: Optional[int] = None
    #: When set to `true` and the primary line is busy, the system redirects calls to the numbers configured for
    #: sequential ringing.
    continue_if_base_location_is_busy_enabled: Optional[bool] = None
    #: When set to `true` calls are directed to voicemail.
    calls_to_voicemail_enabled: Optional[bool] = None
    #: A list of up to five phone numbers to which calls will be directed.
    phone_numbers: Optional[list[SequentialRingNumber]] = None
    #: A list of criteria specifying conditions when sequential ringing is in effect.
    criteria: Optional[list[SelectiveCrit]] = None

    def update(self) -> dict:
        """
        data for update

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_none=True,
                               exclude={'criteria'})


class SequentialRingApi(PersonSettingsApiChild):
    """
    API for sequential ring settings

    For now only used for workspaces
    """

    feature = 'sequentialRing'

    def read_criteria(self, entity_id: str, id: str,
                      org_id: str = None) -> SequentialRingCriteria:
        """
        Retrieve sequential ring criteria for an entity.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.
        The sequential ring criteria specify settings such as schedule and incoming numbers for which to sequentially
        ring or not.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SelectiveCriteria`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id, f'criteria/{id}')
        data = super().get(url, params=params)
        r = SequentialRingCriteria.model_validate(data)
        return r

    def configure_criteria(self, entity_id: str, id: str, settings: SequentialRingCriteria,
                           org_id: str = None):
        """
        Modify sequential ring criteria for an entity.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.
        The sequential ring criteria specify settings such as schedule and incoming numbers for which to sequentially
        ring or not.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param settings: new settings to be applied.
        :type settings: SequentialRingCriteria
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.update()
        url = self.f_ep(entity_id, f'criteria/{id}')
        super().put(url, params=params, json=body)

    def delete_criteria(self, entity_id: str, id: str, org_id: str = None):
        """
        Delete sequential ring criteria for an entity.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.
        The sequential ring criteria specify settings such as schedule and incoming numbers for which to sequentially
        ring or not.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id, f'criteria/{id}')
        super().delete(url, params=params)

    def create_criteria(self, entity_id: str, settings: SequentialRingCriteria,
                        org_id: str = None) -> str:
        """
        Create sequential ring criteria for an entity.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.
        The sequential ring criteria specify settings such as schedule and incoming numbers for which to sequentially
        ring or not.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param settings: new settings to be applied.
        :type settings: SelectiveCriteria
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.update()

        url = self.f_ep(entity_id, f'criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def read(self, entity_id: str,
             org_id: str = None) -> SequentialRing:
        """
        Retrieve sequential ring settings for an entity.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the workspace
        receives incoming calls, these numbers will ring one after another.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SequentialRing`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id)
        data = super().get(url, params=params)
        r = SequentialRing.model_validate(data)
        return r

    def configure(self, entity_id: str, settings: SequentialRing,
                  org_id: str = None):
        """
        Modify sequential ring settings for an entity.

        The sequential ring feature enables you to create a list of up to five phone numbers. When the entity
        receives incoming calls, these numbers will ring one after another.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param settings: Settings for new criteria
        :type settings: SequentialRing
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.update()
        url = self.f_ep(entity_id)
        super().put(url, params=params, json=body)

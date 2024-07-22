from typing import Optional

from wxc_sdk.base import ApiModel
from wxc_sdk.common.selective import SelectiveCriteria, SelectiveCrit
from wxc_sdk.person_settings.common import PersonSettingsApiChild

__all__ = ['SelectiveRejectCriteria', 'SelectiveReject', 'SelectiveRejectApi']


class SelectiveRejectCriteria(SelectiveCriteria):
    _enabled_attr = 'rejectEnabled'
    _phone_numbers = 'phoneNumbers'


class SelectiveReject(ApiModel):
    #: `true` if the Selective Reject feature is enabled.
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective reject is in effect.
    criteria: Optional[list[SelectiveCrit]] = None

    def update(self) -> dict:
        """
        data for update

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_none=True,
                               exclude={'criteria'})


class SelectiveRejectApi(PersonSettingsApiChild):
    """
    API for selective reject settings

    For now only used for workspaces
    """

    feature = 'selectiveReject'

    def read_criteria(self, entity_id: str, id: str,
                      org_id: str = None) -> SelectiveRejectCriteria:
        """
        Retrieve Selective Reject Criteria for an entity

        Retrieve Selective Reject Criteria Settings for an entity.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SelectiveRejectCriteria`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id, f'criteria/{id}')
        data = super().get(url, params=params)
        r = SelectiveRejectCriteria.model_validate(data)
        return r

    def configure_criteria(self, entity_id: str, id: str, settings: SelectiveRejectCriteria,
                           org_id: str = None):
        """
        Modify Selective Reject Criteria for an entity

        Modify Selective Reject Criteria Settings for an entity.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param settings: new settings to be applied.
        :type settings: SelectiveRejectCriteria
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
        Delete Selective Reject Criteria for an entity

        Delete Selective Reject criteria Settings for an entity.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

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

    def create_criteria(self, entity_id: str, settings: SelectiveRejectCriteria, org_id: str = None) -> str:
        """
        Create Selective Reject Criteria for an entity

        Create Selective Reject Criteria Settings for an entity.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param settings: new settings to be applied.
        :type settings: SelectiveRejectCriteria
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
        url = self.f_ep(entity_id, 'criteria')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def read(self, entity_id: str,
             org_id: str = None) -> SelectiveReject:
        """
        Retrieve Selective Reject Settings for an entity.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SelectiveReject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id)
        data = super().get(url, params=params)
        r = SelectiveReject.model_validate(data)
        return r

    def configure(self, entity_id: str, settings: SelectiveReject, org_id: str = None):
        """
        Modify Selective Reject Settings for an entity.

        With the Selective Reject feature, you can reject calls at specific times from specific callers. This setting
        takes precedence over Selectively Accept Calls.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param settings: new settings to be applied.
        :type settings: SelectiveReject
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

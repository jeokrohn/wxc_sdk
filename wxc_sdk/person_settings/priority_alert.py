from typing import Optional

from wxc_sdk.base import ApiModel
from wxc_sdk.common.selective import SelectiveCriteria, SelectiveCrit
from wxc_sdk.person_settings.common import PersonSettingsApiChild

__all__ = ['PriorityAlertCriteria', 'PriorityAlert', 'PriorityAlertApi']


class PriorityAlertCriteria(SelectiveCriteria):
    _enabled_attr = 'notificationEnabled'
    _phone_numbers = 'phoneNumbers'


class PriorityAlert(ApiModel):
    #: `true` if the Priority Alert feature is enabled.
    enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when priority alert is in effect.
    criteria: Optional[list[SelectiveCrit]] = None

    def update(self) -> dict:
        """
        Data for update
        
        :meta private
        """
        return self.model_dump(mode='json', by_alias=True, exclude_none=True,
                               exclude={'criteria'})


class PriorityAlertApi(PersonSettingsApiChild):
    """
    API for priority alert settings

    For now only used for workspaces
    """

    feature = 'priorityAlert'

    def read_criteria(self, entity_id: str, id: str,
                      org_id: str = None) -> PriorityAlertCriteria:
        """
        Retrieve Priority Alert Criteria for a Workspace

        Retrieve Priority Alert Criteria Settings for a Workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.

        Priority Alert Criteria (Schedules) can also be set up to alert these phones during certain times of the day or
        days of the week.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PriorityAlertCriteria`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id, f'criteria/{id}')
        data = super().get(url, params=params)
        r = PriorityAlertCriteria.model_validate(data)
        return r

    def configure_criteria(self, entity_id: str, id: str, settings: PriorityAlertCriteria,
                           org_id: str = None):
        """
        Modify Priority Alert Criteria for a Workspace

        Modify Priority Alert Criteria Settings for a Workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.

        Priority Alert Criteria (Schedules) can also be set up to alert these phones during certain times of the day or
        days of the week.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param settings: new settings to be applied.
        :type settings: PriorityAlertCriteria
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
        Delete Priority Alert Criteria for a Workspace

        Delete Priority Alert criteria Settings for a workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.

        Priority Alert Criteria (Schedules) can also be set up to alert these phones during certain times of the day or
        days of the week.

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

    def create_criteria(self, entity_id: str, settings: PriorityAlertCriteria, org_id: str = None) -> str:
        """
        Create Priority Alert Criteria for a Workspace

        Create Priority Alert Criteria Settings for a Workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.

        Priority Alert Criteria (Schedules) can also be set up to alert these phones during certain times of the day or
        days of the week.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param settings: new settings to be applied.
        :type settings: PriorityAlertCriteria
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
             org_id: str = None) -> PriorityAlert:
        """
        Retrieve Priority Alert Settings for a Workspace.

        The priority alert feature enables administrators to configure priority alert settings for a professional
        workspace.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PriorityAlert`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id)
        data = super().get(url, params=params)
        r = PriorityAlert.model_validate(data)
        return r

    def configure(self, entity_id: str, settings: PriorityAlert,
                  org_id: str = None):
        """
        Configure Priority Alert Settings for a Workspace

        Configure a workspace Priority Alert Settings.

        The priority alert feature enables administrator to configure priority alert settings for a professional
        workspace.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param settings: Settings for new criteria
        :type settings: PriorityAlert
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

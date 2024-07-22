from typing import Optional

from wxc_sdk.base import ApiModel
from wxc_sdk.common.selective import SelectiveCriteria, SelectiveCrit
from wxc_sdk.person_settings.common import PersonSettingsApiChild

__all__ = ['SelectiveForwardCriteria', 'SelectiveForward', 'SelectiveForwardApi']


class SelectiveForwardCriteria(SelectiveCriteria):
    _enabled_attr = 'forwardEnabled'
    _phone_numbers = 'numbers'

    #: Phone number to forward calls to during this schedule.
    forward_to_phone_number: Optional[str] = None
    #: Enables forwarding for all calls to voicemail. This option is only available for internal phone numbers or
    #: extensions.
    send_to_voicemail_enabled: Optional[bool] = None


class SelectiveForward(ApiModel):
    #: `true` if the Selective Forward feature is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: Enter the phone number to forward calls to during this schedule.
    #: example: +1934898988
    default_phone_number_to_forward: Optional[str] = None
    #: When `true`, enables a ring reminder for such calls.
    #: example: True
    ring_reminder_enabled: Optional[bool] = None
    #: Enables forwarding for all calls to voicemail. This option is only available for internal phone numbers or
    #: extensions.
    destination_voicemail_enabled: Optional[bool] = None
    #: A list of criteria specifying conditions when selective forward feature is in effect.
    criteria: Optional[list[SelectiveCrit]] = None

    def update(self) -> dict:
        """
        data for update

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_none=True,
                               exclude={'criteria'})


class SelectiveForwardApi(PersonSettingsApiChild):
    """
    API for selective forward settings

    For now only used for workspaces
    """

    feature = 'selectiveForward'

    def read_criteria(self, entity_id: str, id: str,
                      org_id: str = None) -> SelectiveForwardCriteria:
        """
        Retrieve Selective Forward Criteria for a Workspace

        Retrieve Selective Forward Criteria Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
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
        :rtype: :class:`SelectiveCriteria`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id, f'criteria/{id}')
        data = super().get(url, params=params)
        r = SelectiveForwardCriteria.model_validate(data)
        return r

    def configure_criteria(self, entity_id: str, id: str, settings: SelectiveForwardCriteria,
                           org_id: str = None):
        """
        Modify Selective Forward Criteria for a Workspace

        Modify Selective Forward Call Criteria Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param settings: new settings to be applied.
        :type settings: SelectiveForwardCriteria
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
        Delete Selective Forward Criteria for a Workspace

        Delete Selective Forward Call criteria Settings for a workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
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

    def create_criteria(self, entity_id: str, settings: SelectiveForwardCriteria,
                        org_id: str = None) -> str:
        """
        Create Selective Forward Criteria for a Workspace

        Create Selective Forward Call Criteria Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

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
             org_id: str = None) -> SelectiveForward:
        """
        Retrieve Selective Forward Settings for a Workspace

        Retrieve Selective Forward Call Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SelectiveForward`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id)
        data = super().get(url, params=params)
        r = SelectiveForward.model_validate(data)
        return r

    def configure(self, entity_id: str, settings: SelectiveForward,
                  org_id: str = None):
        """
        Modify Selective Forward Settings for a Workspace

        Modify Selective Forward Call Settings for a Workspace.

        With the Selective Forward feature, you can forward calls at specific times from specific callers. This setting
        takes precedence over call forwarding.
        Schedules can also be set up for this feature during certain times of the day or days of the week.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param settings: Settings for new criteria
        :type settings: SelectiveForward
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

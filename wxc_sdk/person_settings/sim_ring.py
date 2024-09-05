from typing import Optional

from pydantic import model_validator

from wxc_sdk.base import ApiModel
from wxc_sdk.common.selective import SelectiveCriteria, SelectiveCrit
from wxc_sdk.person_settings.common import PersonSettingsApiChild

__all__ = ['SimRingCriteria', 'SimRingNumber', 'SimRing', 'SimRingApi']


class SimRingCriteria(SelectiveCriteria):
    _enabled_attr = 'ringEnabled'
    _phone_numbers = 'phoneNumbers'


class SimRingNumber(ApiModel):
    #: Phone number set as the sequential number.
    phone_number: Optional[str] = None
    #: When set to `true` the called party is required to press 1 on the keypad to receive the call.
    answer_confirmation_required_enabled: Optional[bool] = None

    @model_validator(mode='before')
    def remove_answer_confirmation_enabled(cls, data):
        """
        Remove answer_confirmation_enabled from data

        August 30, 2024

        Breaking Change

        For consistency with other APIs, we will be renaming the field answerConfirmationEnabled to
        answerConfirmationRequiredEnabled within the simultaneous ring settings for the Workspace API. This modification
        affects the GET and UPDATE endpoints. The change will take effect on October 11, 2024. Throughout the transition
        period, both fields will be accessible in the payload for GET and MODIFY operations.

        TODO: remove this validator after October 11, 2024

        :meta private:
        :param data:
        :return:
        """
        data.pop('answer_confirmation_enabled', None)
        data.pop('answerConfirmationEnabled', None)
        return data


class SimRing(ApiModel):
    #: Simultaneous Ring is enabled or not.
    enabled: Optional[bool] = None
    #: When set to `true`, the configured phone numbers won't ring when on a call.
    do_not_ring_if_on_call_enabled: Optional[bool] = None
    #: Enter up to 10 phone numbers to ring simultaneously when workspace phone receives an incoming call.
    phone_numbers: Optional[list[SimRingNumber]] = None
    #: A list of criteria specifying conditions when simultaneous ring is in effect.
    criteria: Optional[list[SelectiveCrit]] = None
    #: When `true`, enables the selected schedule for simultaneous ring.
    criterias_enabled: Optional[bool] = None

    def update(self) -> dict:
        """
        Data for update

        :meta private
        """
        return self.model_dump(mode='json', by_alias=True, exclude_none=True,
                               exclude={'criteria'})


class SimRingApi(PersonSettingsApiChild):
    """
    API for simultaneous ring settings

    For now only used for workspaces
    """

    feature = 'simultaneousRing'

    def read_criteria(self, entity_id: str, id: str,
                      org_id: str = None) -> SimRingCriteria:
        """
        Retrieve Simultaneous Ring Criteria for an entity

        Retrieve Simultaneous Ring Criteria Settings for an entity.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain times of the day
        or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SimRingCriteria`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id, f'criteria/{id}')
        data = super().get(url, params=params)
        r = SimRingCriteria.model_validate(data)
        return r

    def configure_criteria(self, entity_id: str, id: str, settings: SimRingCriteria,
                           org_id: str = None):
        """
        Modify Simultaneous Ring Criteria for an entity

        Modify Simultaneous Ring Criteria Settings for an entity.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain times of the day
        or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param id: Unique identifier for the criteria.
        :type id: str
        :param settings: new settings to be applied.
        :type settings: SimRingCriteria
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
        Delete Simultaneous Ring Criteria for an entity

        Delete simultaneous ring criteria Settings for an entity.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain times of the day
        or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

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

    def create_criteria(self, entity_id: str, settings: SimRingCriteria, org_id: str = None) -> str:
        """
        Create Simultaneous Ring Criteria for an entity

        Create Simultaneous Ring Criteria Settings for an entity.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Simultaneous Ring Criteria (Schedules) can also be set up to ring these phones during certain times of the day
        or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param settings: new settings to be applied.
        :type settings: SimRingCriteria
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
             org_id: str = None) -> SimRing:
        """
        Retrieve Simultaneous Ring Settings for an entity.

        The Simultaneous Ring feature allows you to configure your office phone and other phones of your choice to ring
        simultaneously.
        Schedules can also be set up to ring these phones during certain times of the day or days of the week.

        This API requires a full, read-only or location administrator auth token with a scope
        of `spark-admin:workspaces_read` or a user auth token with a scope of `spark:workspaces_read` to read workspace
        settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`SimRing`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id)
        data = super().get(url, params=params)
        r = SimRing.model_validate(data)
        return r

    def configure(self, entity_id: str, settings: SimRing,
                  org_id: str = None):
        """
        Modify Simultaneous Ring Settings for an entity.

        The Simultaneous Ring feature allows you to configure the workspace phones of your choice to ring
        simultaneously.
        Schedules can also be set up to ring these phones during certain times of the day or days of the week.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope or a user auth token with a scope of `spark:workspaces_write` to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param settings: Settings for new criteria
        :type settings: SimRing
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

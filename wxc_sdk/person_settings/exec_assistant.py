"""
exec assistant settings API
"""

from enum import Enum

from pydantic import Field

from .common import PersonSettingsApiChild
from ..common import ApiModel

__all__ = ['ExecAssistantApi', 'ExecAssistantType']


class ExecAssistantType(str, Enum):
    """
    Indicates the Executive Assistant type.
    """
    #: Indicates the feature is not enabled.
    unassigned = 'UNASSIGNED'
    #: Indicates the feature is enabled and the person is an Executive
    executive = 'EXECUTIVE'
    #: Indicates the feature is enabled and the person is an Executive Assistant.
    executive_assistant = 'EXECUTIVE_ASSISTANT'


class _Helper(ApiModel):
    exec_type: ExecAssistantType = Field(alias='type')


class ExecAssistantApi(PersonSettingsApiChild):
    """
    Api for person's exec assistant settings
    """

    feature = 'executiveAssistant'

    def read(self, *, person_id: str, org_id: str = None) -> ExecAssistantType:
        """
        Retrieve Executive Assistant Settings for a Person

        Retrieve the executive assistant settings for the specified personId.

        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set
        the call forward destination and join or leave an executive's pool.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: exec assistant setting
        :rtype: :class:`ExecAssistantType`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(ep, params=params)
        h: _Helper = _Helper.parse_obj(data)
        return h.exec_type

    def configure(self, *, person_id: str, setting: ExecAssistantType, org_id: str = None):
        """
        Modify Executive Assistant Settings for a Person

        Modify the executive assistant settings for the specified personId.

        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set
        the call forward destination and join or leave an executive's pool.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param setting: New exex assistant settings
        :type setting: :class:`ExecAssistantType`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        h = _Helper(exec_type=setting)
        params = org_id and {'orgId': org_id} or None
        data = h.json()
        self.put(ep, params=params, data=data)

"""
Receptionist client settings API
"""

import json
from typing import Optional, Union

from pydantic import Field

from .common import PersonSettingsApiChild
from ..base import ApiModel
from ..common import MonitoredMember

__all__ = ['ReceptionistApi', 'ReceptionistSettings']


class ReceptionistSettings(ApiModel):
    """
    user's receptionist client settings
    """
    #: Set to true to enable the Receptionist Client feature.
    enabled: Optional[bool] = Field(alias='receptionEnabled')
    #: List of people and/or workspaces to monitor.
    #: for updates can be a list of IDs
    monitored_members: Optional[list[Union[str, MonitoredMember]]]


class ReceptionistApi(PersonSettingsApiChild):
    """
    Api for person's receptionist client settings
    """

    feature = 'reception'

    def read(self, *, person_id: str, org_id: str = None) -> ReceptionistSettings:
        """
        Read Receptionist Client Settings for a Person

        Retrieve a Person's Receptionist Client Settings

        To help support the needs of your front-office personnel, you can set up people or workspaces as telephone
        attendants so that they can screen all incoming calls to certain numbers within your organization.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: receptionist client settings
        :rtype: :class:`ReceptionistSettings`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(ep, params=params)
        return ReceptionistSettings.parse_obj(data)

    def configure(self, *, person_id: str, settings: ReceptionistSettings, org_id: str = None):
        """
        Modify Executive Assistant Settings for a Person

        Modify the executive assistant settings for the specified personId.

        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set
        the call forward destination and join or leave an executive's pool.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: New receptionist client settings
        :type settings: :class:`ReceptionistSettings`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        if settings.enabled is None:
            raise ValueError('enabled is a mandatory parameter for updates')
        if settings.monitored_members and not settings.enabled:
            raise ValueError('when setting members enabled has to be True')
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.loads(settings.json())
        if settings.monitored_members is not None:
            id_list = []
            for me in settings.monitored_members:
                if isinstance(me, str):
                    id_list.append(me)
                else:
                    id_list.append(me.member_id)
            data['monitoredMembers'] = id_list
        self.put(ep, params=params, json=data)

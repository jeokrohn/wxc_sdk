"""
user privacy API
"""
import json
from typing import Optional, Union

from .common import PersonSettingsApiChild
from ..base import ApiModel
from ..common import PersonPlaceAgent

__all__ = ['PrivacyApi', 'Privacy']


class Privacy(ApiModel):
    """
    Person privacy settings
    """
    #: When true auto attendant extension dialing will be enabled.
    aa_extension_dialing_enabled: Optional[bool]
    #: When true auto attendant dialing by first or last name will be enabled.
    aa_naming_dialing_enabled: Optional[bool]
    #: When true phone status directory privacy will be enabled.
    enable_phone_status_directory_privacy: Optional[bool]
    # TODO: documentation defect: called "monitoredAgents" in docs
    #: List of people that are being monitored.
    #: for updates IDs can be used directly instead of :class:`wxc_sdk.common.PersonPlaceAgent` objects
    monitoring_agents: Optional[list[Union[str, PersonPlaceAgent]]]


class PrivacyApi(PersonSettingsApiChild):
    """
    API for person's call monitoring settings
    """

    feature = 'privacy'

    def read(self, *, person_id: str, org_id: str = None) -> Privacy:
        """
        Get a person's Privacy Settings

        Get a person's privacy settings for the specified person id.

        The privacy feature enables the person's line to be monitored by others and determine if they can be reached
        by Auto Attendant services.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: privacy settings
        :rtype: :class:`Privacy`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(ep, params=params)
        return Privacy.parse_obj(data)

    def configure(self, *, person_id: str, settings: Privacy, org_id: str = None):
        """
        Configure Call Waiting Settings for a Person

        Configure a Person's Call Waiting Settings

        With this feature, a person can place an active call on hold and answer an incoming call. When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore
        the call.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: settings for update
        :type settings: :class:`Monitoring`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.loads(settings.json())
        if settings.monitoring_agents is not None:
            id_list = []
            for ma in settings.monitoring_agents:
                if isinstance(ma, str):
                    id_list.append(ma)
                else:
                    id_list.append(ma.agent_id)
            data['monitoringAgents'] = id_list
        self.put(ep, params=params, json=data)

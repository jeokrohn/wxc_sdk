"""
Call waiting API
"""
import json

from .common import PersonSettingsApiChild

__all__ = ['CallWaitingApi']


class CallWaitingApi(PersonSettingsApiChild):
    """
    API for person's call waiting settings

    Also used for virtual lines, workspaces
    """

    feature = 'callWaiting'

    def read(self, entity_id: str, org_id: str = None) -> bool:
        """
        Read Call Waiting Settings for

        Retrieve Call Waiting Settings

        With this feature, an entity can place an active call on hold and answer an incoming call. When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or
        ignore the call.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: entity is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: call waiting setting
        :rtype: bool
        """
        ep = self.f_ep(person_id=entity_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(ep, params=params)
        return data['enabled']

    def configure(self, entity_id: str, enabled: bool, org_id: str = None):
        """
        Configure Call Waiting Settings

        Configure an entity's Call Waiting Settings

        With this feature, a entity can place an active call on hold and answer an incoming call. When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore
        the call.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param enabled: true if the Call Waiting feature is enabled.
        :type enabled: bool
        :param org_id: entity is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=entity_id)
        params = org_id and {'orgId': org_id} or None
        data = json.dumps({'enabled': enabled})
        self.put(ep, params=params, json=data)

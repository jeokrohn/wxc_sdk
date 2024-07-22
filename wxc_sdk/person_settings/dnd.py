"""
Person DND settings API
"""

from .common import PersonSettingsApiChild
from ..base import ApiModel

__all__ = ['DND', 'DndApi']


class DND(ApiModel):
    """
    DND settings
    """
    #: forwarding.py
    enabled: bool
    #: Enables a Ring Reminder to play a brief tone on your desktop phone when you receive incoming calls.
    ring_splash_enabled: bool


class DndApi(PersonSettingsApiChild):
    """
    API for person's DND settings. Also used for workspaces
    """

    feature = 'doNotDisturb'

    def read(self, entity_id: str, org_id: str = None) -> DND:
        """
        Read Do Not Disturb Settings for an entity
        Retrieve an entity's Do Not Disturb Settings

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: Entity is in this organization. Only admin users of another organization (such as partners) may
        use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return:
        """
        ep = self.f_ep(entity_id)
        params = org_id and {'orgId': org_id} or None
        return DND.model_validate(self.get(ep, params=params))

    def configure(self, entity_id: str, dnd_settings: DND, org_id: str = None):
        """
        Configure Do Not Disturb Settings for an entity
        Configure an entity's Do Not Disturb Settings

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by an entity to update their settings.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param dnd_settings: new setting to be applied
        :type dnd_settings: DND
        :param org_id: Entity is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(entity_id)
        params = org_id and {'orgId': org_id} or None
        self.put(ep, params=params, data=dnd_settings.model_dump_json())

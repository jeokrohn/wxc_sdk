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


class DndApi(PersonSettingsApiChild, base='people'):
    """
    Api for person's DND settings
    """

    def read(self, person_id: str, org_id: str = None) -> DND:
        """
        Read Do Not Disturb Settings for a Person
        Retrieve a Person's Do Not Disturb Settings

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.
        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners) may
        use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return:
        """
        ep = self.f_ep(person_id=person_id, path='doNotDisturb')
        params = org_id and {'orgId': org_id} or None
        return DND.parse_obj(self.get(ep, params=params))

    def configure(self, person_id: str, dnd_settings: DND, org_id: str = None):
        """
        Configure Do Not Disturb Settings for a Person
        Configure a Person's Do Not Disturb Settings

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param dnd_settings: new setting to be applied
        :type dnd_settings: DND
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id, path='doNotDisturb')
        params = org_id and {'orgId': org_id} or None
        self.put(ep, params=params, data=dnd_settings.json())

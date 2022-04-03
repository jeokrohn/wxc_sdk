"""
Person barge settings API
"""

from .common import PersonSettingsApiChild
from ..base import ApiModel

__all__ = ['BargeSettings', 'BargeApi']


class BargeSettings(ApiModel):
    """
    Barge settings
    """
    #: indicates if the Barge In feature is enabled.
    enabled: bool
    #: Indicates that a stutter dial tone will be played when a person is barging in on the active call.
    tone_enabled: bool


class BargeApi(PersonSettingsApiChild):
    """
    Api for person's barge settings
    """

    feature = 'bargeIn'

    def read(self, *, person_id: str, org_id: str = None) -> BargeSettings:
        """
        Retrieve a Person's Barge In Settings

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: barge settings for specific user
        :rtype: BargeSettings
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return BargeSettings.parse_obj(self.get(ep, params=params))

    def configure(self, *, person_id: str, barge_settings: BargeSettings, org_id: str = None):
        """
        Configure a Person's Barge In Settings

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param barge_settings: new setting to be applied
        :type barge_settings: BargeSettings
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        self.put(ep, params=params, data=barge_settings.json())

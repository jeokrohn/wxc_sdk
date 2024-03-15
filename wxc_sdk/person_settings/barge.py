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
    API for barge settings; also used for virtual lines
    """

    feature = 'bargeIn'

    def read(self, entity_id: str, org_id: str = None) -> BargeSettings:
        """
        Retrieve Barge In Settings

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by an entity to read their own settings.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: entity is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: barge settings for specific user
        :rtype: BargeSettings
        """
        ep = self.f_ep(person_id=entity_id)
        params = org_id and {'orgId': org_id} or None
        return BargeSettings.model_validate(self.get(ep, params=params))

    def configure(self, entity_id: str, barge_settings: BargeSettings, org_id: str = None):
        """
        Configure Barge In Settings

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by an entity to update their own settings.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param barge_settings: new setting to be applied
        :type barge_settings: BargeSettings
        :param org_id: entity is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=entity_id)
        params = org_id and {'orgId': org_id} or None
        self.put(ep, params=params, data=barge_settings.model_dump_json())

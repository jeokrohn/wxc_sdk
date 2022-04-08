"""
Hoteling API
"""
import json

from .common import PersonSettingsApiChild

__all__ = ['HotelingApi']


class HotelingApi(PersonSettingsApiChild):
    """
    API for person's hoteling settings
    """

    feature = 'hoteling'

    def read(self, *, person_id: str, org_id: str = None) -> bool:
        """
        Read Hoteling Settings for a Person

        Retrieve a person's hoteling settings.

        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features,
        and calling plan) is temporarily loaded onto a shared (host) phone.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: hoteling setting
        :rtype: bool
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(ep, params=params)
        return data['enabled']

    def configure(self, *, person_id: str, enabled: bool, org_id: str = None):
        """
        Configure Hoteling Settings for a Person

        Configure a person's hoteling settings.

        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features,
        and calling plan) is temporarily loaded onto a shared (host) phone.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: When true, allow this person to connect to a Hoteling host device.
        :type enabled: bool
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.dumps({'enabled': enabled})
        self.put(ep, params=params, json=data)

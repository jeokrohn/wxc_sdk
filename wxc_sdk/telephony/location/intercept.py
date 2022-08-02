"""
location intercept
"""

from ...api_child import ApiChild
from ...person_settings.call_intercept import InterceptSetting

__all__ = ['LocationInterceptApi']


class LocationInterceptApi(ApiChild, base='telephony/config/locations'):
    """
    API for location's call intercept settings
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific
        telephony/config/locations/{locationId}/intercept

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/intercept{path}')
        return ep

    def read(self, *, location_id: str, org_id: str = None) -> InterceptSetting:
        """
        Get Location Intercept

        Retrieve intercept location details for a customer location.

        Intercept incoming or outgoing calls for persons in your organization. If this is enabled, calls are either
        routed to a designated number the person chooses, or to the person's voicemail.

        Retrieving intercept location details requires a full, user or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve intercept details for this location.
        :type location_id: str
        :param org_id: Retrieve intercept location details for a customer location.
        :type org_id: str
        :return: user's call intercept settings
        :rtype: :class:`wxc_sdk.person_settings.call_intercept.InterceptSetting`
        """
        ep = self._endpoint(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        return InterceptSetting.parse_obj(self.get(ep, params=params))

    def configure(self, *, location_id: str, settings: InterceptSetting, org_id: str = None):
        """
        Put Location Intercept

        Modifies the intercept location details for a customer location.

        Intercept incoming or outgoing calls for users in your organization. If this is enabled, calls are either
        routed to a designated number the user chooses, or to the user's voicemail.

        Modifying the intercept location details requires a full, user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Unique identifier for the person.
        :type location_id: str
        :param settings: new intercept settings
        :type settings: InterceptSetting
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self._endpoint(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = settings.json()
        self.put(ep, params=params, data=data)

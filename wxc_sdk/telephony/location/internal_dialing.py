from typing import Optional

from ...api_child import ApiChild
from ...base import ApiModel
from ...common import RouteIdentity

__all__ = ['InternalDialing', 'InternalDialingApi']


class InternalDialing(ApiModel):
    #: When enabled, calls made by users at the location to an unknown extension (between 2-6 digits) are routed to
    #: the selected route group/trunk as premises calls.
    enable_unknown_extension_route_policy: bool
    #: destination for unknown extensions
    unknown_extension_route_identity: Optional[RouteIdentity]


class InternalDialingApi(ApiChild, base='telephony/config/locations'):
    """
    Internal dialing settings for location
    """

    def url(self, *, location_id: str) -> str:
        return super().ep(f'{location_id}/internalDialing')

    def read(self, *, location_id: str, org_id: str = None) -> InternalDialing:
        """
        Get current configuration for routing unknown extensions to the Premises as internal calls

        If some users in a location are registered to a PBX, retrieve the setting to route unknown extensions (digits
        that match the extension length) to the PBX.

        Retrieving the internal dialing configuration requires a full or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: location for which internal calling configuration is being requested
        :type location_id: str
        :param org_id:
        :type org_id: str
        :return: settings
        :rtype: :class:`InternalDialing`
        """
        url = self.url(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(url=url, params=params)
        return InternalDialing.parse_obj(data)

    def update(self, *, location_id: str, update: InternalDialing, org_id: str = None):
        """
        Modify current configuration for routing unknown extensions to the Premises as internal calls

        If some users in a location are registered to a PBX, enable the setting to route unknown extensions (digits
        that match the extension length) to the PBX.

        Editing the internal dialing configuration requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: location for which internal calling configuration is being requested
        :type location_id: str
        :param update: new settings
        :type update: :class:`InternalDialing`
        :param org_id:
        :type org_id: str
        """
        url = self.url(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = update.json(exclude_none=False)
        self.put(url=url, params=params, data=data)

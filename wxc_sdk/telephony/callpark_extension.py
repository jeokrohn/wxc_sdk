from collections.abc import Generator

from ..api_child import ApiChild
from ..base import to_camel
from ..common import CallParkExtension

__all__ = ['CallparkExtensionApi']


class CallparkExtensionApi(ApiChild, base='telephony'):
    """
    Call Park Extension API
    """

    def _endpoint(self, *, location_id: str = None, cpe_id: str = None) -> str:
        """
        call park extension specific feature endpoint like
        /v1/telephony/config/locations/{locationId}/callParkExtensions/{cpe_id}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param cpe_id: call park extension id
        :type cpe_id: str
        :return: full endpoint
        :rtype: str
        """
        if location_id is None:
            return self.session.ep('telephony/config/callParkExtensions')
        else:
            ep = self.session.ep(f'telephony/config/locations/{location_id}/callParkExtensions')
            if cpe_id:
                ep = f'{ep}/{cpe_id}'
            return ep

    def list(self, extension: str = None, name: str = None, location_id: str = None,
             location_name: str = None, order: str = None, org_id: str = None,
             **params) -> Generator[CallParkExtension, None, None]:
        """
        Read the List of Call Park Extensions

        List all Call Park Extensions for the organization.

        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call
        Park service for holding parked calls.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param extension: Only return call park extensions with the matching extension.
        :type extension: str
        :param name: Only return call park extensions with the matching name.
        :type name: str
        :param location_id: Only return call park extensions with matching location ID.
        :type location_id: str
        :param location_name: Only return call park extensions with matching location name.
        :type location_name: str
        :param order: Order the available agents according to the designated fields. Available sort fields: groupName,
            callParkExtension, callParkExtensionName, callParkExtensionExternalId.
        :type order: str
        :param org_id: List call park extensions for this organization.
        :type org_id: str
        :param params: additional parameters
        :return: yields :class:`wxc_sdk.common.CallParkExtension` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CallParkExtension, params=params)

    def details(self, location_id: str, cpe_id: str, org_id: str = None) -> CallParkExtension:
        """
        Get Details for a Call Park Extension

        Retrieve Call Park Extension details.

        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call
        Park service for holding parked calls.

        Retrieving call park extension details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve details for a call park extension in this location.
        :type location_id: str
        :param cpe_id: Retrieve details for a call park extension with the matching ID.
        :type cpe_id: str
        :param org_id: Retrieve call park extension details from this organization
        :type org_id: str
        :return: call park extension details
        :rtype: :class:`wxc_sdk.common.CallParkExtension` instance (only name and extension are set)
        """
        url = self._endpoint(location_id=location_id, cpe_id=cpe_id)
        params = org_id and {'orgId': org_id} or {}
        data = self.get(url, params=params)
        return CallParkExtension.parse_obj(data)

    def create(self, location_id: str, name: str, extension: str, org_id: str = None, ) -> str:
        """
        Create new Call Park Extensions for the given location.
        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.
        Creating a call park extension requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Create the call park extension for this location.
        :type location_id: str
        :param name: Name for the call park extension. The maximum length is 30.
        :type name: str
        :param extension: Unique extension which will be assigned to call park extension. The minimum length is 2,
            maximum length is 6.
        :type extension: str
        :param org_id: Create the call park extension for this organization.
        :type org_id: str
        :return: id of the new call park extension
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {'name': name, 'extension': extension}
        url = self._endpoint(location_id=location_id)
        data = super().post(url=url, params=params, json=body)
        return data["id"]

    def delete(self, location_id: str, cpe_id: str, org_id: str = None):
        """
        Delete the designated Call Park Extension.
        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.
        Deleting a call park extension requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a call park extension.
        :type location_id: str
        :param cpe_id: Delete the call park extension with the matching ID.
        :type cpe_id: str
        :param org_id: Delete the call park extension from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self._endpoint(location_id=location_id, cpe_id=cpe_id)

        super().delete(url=url, params=params)
        return

    def update(self, location_id: str, cpe_id: str, name: str = None, extension: str = None, org_id: str = None):
        """
        Update the designated Call Park Extension.
        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.
        Updating a call park extension requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this call park extension exists.
        :type location_id: str
        :param cpe_id: Update a call park extension with the matching ID.
        :type cpe_id: str
        :param name: Name for the call park extension. The maximum length is 30.
        :type name: str
        :param extension: Unique extension which will be assigned to call park extension. The minimum length is 2,
            maximum length is 6.
        :type extension: str
        :param org_id: Update a call park extension from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if extension is not None:
            body['extension'] = extension
        url = self._endpoint(location_id=location_id, cpe_id=cpe_id)
        super().put(url=url, params=params, json=body)
        return

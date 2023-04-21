"""
Location Receptionist Directories
"""

from collections.abc import Generator

from ...api_child import ApiChild
from ...common import IdAndName


class ReceptionistContactsDirectoryApi(ApiChild, base='telephony/config/locations'):
    """
    Webex Calling Location Receptionist Contacts supports creation of directories and assigning custom groups of
    users to directories for a location within an organization.

    Receptionist Contact Directories are named custom groups of users.

    Viewing these read-only directories requires a full or read-only administrator auth token with a scope of
    spark-admin:telephony_config_read, as the current set of APIs is designed to provide supplemental information for
    administrators utilizing People Webex Calling APIs.

    Modifying these directories requires a full administrator auth token with a scope
    of spark-admin:telephony_config_write.

    A partner administrator can retrieve or change settings in a customer's organization using the optional OrgId
    query parameter.

    """

    # TODO: create test cases
    # TODO: really no details call and no way to update a directory?

    def _url(self, location_id: str):
        return self.ep(f'{location_id}/receptionistContacts/directories')

    def create(self, location_id: str, name: str, contacts: list[str], org_id: str = None) -> str:
        """
        Creates a new Receptionist Contact Directory for a location.

        Receptionist Contact Directories can be used to create named directories of users.

        Adding a directory requires a full or write-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Add a Receptionist Contact Directory to this location.
        :type location_id: str
        :param name: Receptionist Contact Directory name.
        :type name: str
        :param contacts: Array of user or workspace ids assigned to this Receptionist Contact Directory
        :type contacts: list[str]
        :param org_id: Add a Receptionist Contact Directory to this organization.
        :type org_id: str
        :return: Receptionist Contact Directory ID.
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = {'name': name,
                'contacts': [{'personId': contact} for contact in contacts]}
        data = self.post(url=url, params=params, json=body)
        return data['id']

    def list(self, location_id: str, org_id: str = None) -> Generator[IdAndName, None, None]:
        """
        List all Receptionist Contact Directories for a location.

        Receptionist Contact Directories can be used to create named directories of users.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: List Receptionist Contact Directories for this location.
        :type location_id: str
        :param org_id: List Receptionist Contact Directories for this organization.
        :type org_id: str
        :return: Yields IdAndName instances
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        return self.session.follow_pagination(url=url, model=IdAndName, params=params, item_key='directories')

    def delete(self, location_id: str, directory_id: str, org_id: str = None):
        """
        Delete a Receptionist Contact Directory from a location.

        Receptionist Contact Directories can be used to create named directories of users.

        Deleting a directory requires a full or write-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Delete a Receptionist Contact Directory from this location.
        :param directory_id: ID of directory to delete.
        :param org_id: Delete a Receptionist Contact Directory from this organization.
        """
        url = f'{self._url(location_id)}/{directory_id}'
        params = org_id and {'orgId': org_id} or None
        super().delete(url=url, params=params)

"""
Call queue announcement files API
"""

from collections.abc import Generator

from pydantic import Field

from ...base import ApiModel
from ...rest import RestSession

__all__ = ['AnnouncementApi', 'Announcement']


class Announcement(ApiModel):
    """
    Announcement file information
    """
    name: str = Field(alias='fileName')
    size: int = Field(alias='fileSize')


class AnnouncementApi:
    """
    API for call queue Announcements
    """

    def __init__(self, *, session: RestSession):
        self._session = session

    def _endpoint(self, location_id: str, queue_id: str, path: str = None):
        """

        :meta private:
        :param location_id:
        :param queue_id:
        :param path:
        :return:
        """
        path = path and f'/{path}' or ''
        ep = self._session.ep(path=f'telephony/config/locations/{location_id}/queues/{queue_id}/announcements{path}')
        return ep

    def list(self, location_id: str, queue_id: str, org_id: str = None) -> Generator[Announcement]:
        """
        Read the List of Call Queue Announcement Files

        List file info for all Call Queue announcement files associated with this Call Queue.

        Call Queue announcement files contain messages and music that callers hear while waiting in the queue. A call
        queue can be configured to play whatever subset of these announcement files is desired.

        Retrieving this list of files requires a full or read-only administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        Note that uploading of announcement files via API is not currently supported, but is available via Webex
        Control Hub.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Retrieve announcement files for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve announcement files for a call queue from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = org_id and {'orgId': org_id} or dict()
        # noinspection PyTypeChecker
        return self._session.follow_pagination(url=url, model=Announcement, params=params)

    def delete_announcement(self, location_id: str, queue_id: str, file_name: str, org_id: str = None):
        """
        Delete a Call Queue Announcement File

        Delete an announcement file for the designated Call Queue.

        Call Queue announcement files contain messages and music that callers hear while waiting in the queue. A call
        queue can be configured to play whatever subset of these announcement files is desired.

        Deleting an announcement file for a call queue requires a full administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Delete an announcement for a call queue in this location.
        :type location_id: str
        :param queue_id: Delete an announcement for the call queue with this identifier.
        :type queue_id: str
        :type file_name: str
        :param org_id: Delete call queue announcement from this organization.
        :type org_id: str
        :rtype: None
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id, path=file_name)
        params = org_id and {'orgId': org_id} or None
        self._session.delete(url=url, params=params)

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

    def list(self, *, location_id: str, queue_id: str, org_id: str = None) -> Generator[Announcement]:
        """

        :param location_id:
        :param queue_id:
        :param org_id:
        :return:
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = org_id and {'orgId': org_id} or dict()
        # noinspection PyTypeChecker
        return self._session.follow_pagination(url=url, model=Announcement, params=params)

    def delete_announcement(self, *, location_id: str, queue_id: str, file_name: str, org_id: str = None):
        """

        :param location_id:
        :type location_id: str
        :param queue_id:
        :type queue_id: str
        :param file_name:
        :type file_name: str
        :param org_id:
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id, path=file_name)
        params = org_id and {'orgId': org_id} or None
        self._session.delete(url=url, params=params)

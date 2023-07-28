"""
Not supported for Webex for Government (FedRAMP)
Features: Announcement Repository support reading and writing of Webex Calling Announcement Repository settings for
a specific organization.
"""
import os
from collections.abc import Generator
from datetime import datetime
from io import BufferedReader
from typing import Optional, Union

from pydantic import Field
from requests_toolbelt import MultipartEncoder

from ...api_child import ApiChild
from ...base import ApiModel
from ...common import IdAndName, MediaFileType, AnnouncementLevel

__all__ = ['RepoAnnouncement', 'AnnouncementsRepositoryApi', 'RepositoryUsage', 'FeatureReference']


class FeatureReference(ApiModel):
    #: Unique identifier of the call feature referenced. The call Feature can be Auto Attendant, Call Queue or Music
    #: On hold.
    id: Optional[str]
    #: Name of the call feature referenced.
    name: Optional[str]
    #: Resource Type of the call feature.
    type: Optional[str]
    #: Unique identifier of the location.
    location_id: Optional[str]
    #: Location name of the announcement file.
    location_name: Optional[str]


class RepoAnnouncement(IdAndName):
    #: File name of the uploaded binary announcement greeting.
    file_name: Optional[str]
    #: Size of the file in kilobytes.
    file_size: Optional[int]
    #: Media file type of the announcement file.
    media_file_type: Optional[MediaFileType]
    #: LastUpdated timestamp (in UTC format) of the announcement.
    last_updated: Optional[datetime]
    #: The level at which this announcement exists.
    level: Optional[AnnouncementLevel]
    #: The details of location at which this announcement exists.
    location: Optional[IdAndName]
    #: The below is not returned by list(), only by details()
    #: Reference count of the call features this announcement is assigned to.
    feature_reference_count: Optional[int]
    #: Call features referenced by this announcement.
    feature_references: Optional[list[FeatureReference]]


class RepositoryUsage(ApiModel):
    #: Total file size used by announcements in this repository in kilobytes.
    total_file_size_used_kb: Optional[int] = Field(alias='totalFileSizeUsedKB')
    #: Maximum audio file size allowed to upload in kilobytes.
    max_audio_file_size_allowed_kb: Optional[int] = Field(alias='maxAudioFileSizeAllowedKB')
    #: Maximum video file size allowed to upload in kilobytes.
    max_video_file_size_allowed_kb: Optional[int] = Field(alias='maxVideoFileSizeAllowedKB')
    #: Total file size limit for the repository in megabytes.
    total_file_size_limit_mb: Optional[int] = Field(alias='totalFileSizeLimitMB')


class AnnouncementsRepositoryApi(ApiChild, base='telephony/config'):
    """
    Not supported for Webex for Government (FedRAMP)

    Features: Announcement Repository support reading and writing of Webex Calling Announcement Repository settings for
    a specific organization.

    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    spark-admin:telephony_config_read.
    Modifying these organization settings requires a full administrator auth token with a scope
    of spark-admin:telephony_config_write.

    A partner administrator can retrieve or change settings in a customer's organization using the optional orgId query
    parameter.
    """

    def list(self, location_id: str = None, order: str = None, file_name: str = None, file_type: str = None,
             media_file_type: str = None, name: str = None, org_id: str = None,
             **params) -> Generator[RepoAnnouncement, None, None]:
        """
        Fetch a list of binary announcement greetings at an organization as well as location level.
        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return the list of enterprise or Location announcement files. Without this parameter, the
            Enterprise level announcements are returned. Possible values: all, locations,
            Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
        :type location_id: str
        :param order: Sort the list according to fileName or fileSize. The default sort will be in Ascending order.
        :type order: str
        :param file_name: Return the list of announcements with the given fileName.
        :type file_name: str
        :param file_type: Return the list of announcement files for this fileType.
        :type file_type: str
        :param media_file_type: Return the list of announcement files for this mediaFileType.
        :type media_file_type: str
        :param name: Return the list of announcement files for this announcement label.
        :type name: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str
        :return: yields :class:`RepoAnnouncement` objects

        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if order is not None:
            params['order'] = order
        if file_name is not None:
            params['fileName'] = file_name
        if file_type is not None:
            params['fileType'] = file_type
        if media_file_type is not None:
            params['mediaFileType'] = media_file_type
        if name is not None:
            params['name'] = name
        url = self.ep('announcements')
        return self.session.follow_pagination(url=url, model=RepoAnnouncement, item_key='announcements',
                                              params=params)

    def _upload_or_modify(self, *, url, name, file, upload_as, params, is_upload) -> dict:
        """

        :meta private:
        """
        if isinstance(file, str):
            upload_as = upload_as or os.path.basename(file)
            file = open(file, mode='rb')
            must_close = True
        else:
            must_close = False
            # an existing reader
            if not upload_as:
                raise ValueError('upload_as is required')
        encoder = MultipartEncoder({'name': name, 'file': (upload_as, file, 'audio/wav')})
        if is_upload:
            meth = super().post
        else:
            meth = super().put
        try:
            data = meth(url, data=encoder, headers={'Content-Type': encoder.content_type},
                        params=params)
        finally:
            if must_close:
                file.close()
        return data

    def upload_announcement(self, name: str, file: Union[BufferedReader, str], upload_as: str = None,
                            location_id: str = None,
                            org_id: str = None) -> str:
        """
        Upload a binary file to the announcement repository at organization or location level.
        An admin can upload a file at an organization or location level. This file will be uploaded to the
        announcement repository.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write .

        :param name: Announcement name
        :type name: str
        :param file: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type file: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param location_id: Unique identifier of a location where an announcement is being created.
        :type location_id: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str
        :return: id of announcement
        :rtype: str

        Examples:

            .. code-block:: python

                # upload a local file as announcement at the org level
                r = api.telephony.announcements_repo.upload_announcement(name='Sample', file='sample.wav')

                # upload an announcement from an open file
                # any files-like object can be used as input.
                # note: the upload_as parameter is required to set the file name for the upload
                with open('sample.wav', mode='rb') as wav_file:
                    r = api.telephony.announcements_repo.upload_announcement(name='Sample', file=wav_file,
                                                                             upload_as='sample.wav')

                # upload an announcement from content in a string
                with open('sample.wav', mode='rb') as wav_file:
                    data = wav_file.read()

                # data now is a bytes object with the file content. As we can use files-like objects as input
                # it's also possible to use a BytesIO as input for upload_announcement()
                binary_file = io.BytesIO(data)
                r = self.api.telephony.announcements_repo.upload_announcement(name='Sample', file=binary_file,
                                                                              upload_as='from_string.wav')

        """
        params = org_id and {'orgId': org_id} or None
        if location_id is None:
            url = self.ep('announcements')
        else:
            url = self.ep(f'locations/{location_id}/announcements')
        data = self._upload_or_modify(url=url, name=name, file=file, upload_as=upload_as, params=params,
                                      is_upload=True)
        return data["id"]

    def usage(self, location_id: str = None, org_id: str = None) -> RepositoryUsage:
        """
        Retrieves repository usage for announcements for an organization.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Unique identifier of a location
        :type location_id: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str

        """
        params = org_id and {'orgId': org_id} or None
        if location_id is None:
            url = self.ep('announcements/usage')
        else:
            url = self.ep(f'locations/{location_id}/announcements/usage')
        data = super().get(url=url, params=params)
        return RepositoryUsage.parse_obj(data)

    def details(self, announcement_id: str, location_id: str = None, org_id: str = None) -> RepoAnnouncement:
        """
        Fetch details of a binary announcement greeting by its ID at an organization level.
        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Unique identifier of a location
        :type location_id: str
        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Get details of an announcement in this organization.
        :type org_id: str

        """
        params = org_id and {'orgId': org_id} or None
        if location_id is None:
            url = self.ep(f'announcements/{announcement_id}')
        else:
            url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        data = super().get(url=url, params=params)
        return RepoAnnouncement.parse_obj(data)

    def delete(self, announcement_id: str, location_id: str = None, org_id: str = None):
        """
        Delete an announcement greeting.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param location_id: Unique identifier of a location where announcement is being deleted.
        :type location_id: str
        :param org_id: Delete an announcement in this organization.
        :type org_id: str

        """
        params = org_id and {'orgId': org_id} or None

        if location_id is None:
            url = self.ep(f'announcements/{announcement_id}')
        else:
            url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        super().delete(url=url, params=params)

    def modify(self, announcement_id: str, name: str, file: Union[BufferedReader, str],
               upload_as: str = None, location_id: str = None, org_id: str = None):
        """
        Modify an existing announcement greeting
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param name: Announcement name
        :type name: str
        :param file: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type file: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param location_id: Unique identifier of a location where announcement is being deleted.
        :type location_id: str
        :param org_id: Modify an announcement in this organization.
        :type org_id: str

        """
        params = org_id and {'orgId': org_id} or None
        if location_id is None:
            url = self.ep(f'announcements/{announcement_id}')
        else:
            url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        data = self._upload_or_modify(url=url, name=name, file=file, upload_as=upload_as, params=params,
                                      is_upload=False)
        return data["id"]

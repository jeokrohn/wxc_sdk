from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AnnouncementObject', 'AnnouncementPlayListGetResponse', 'AnnouncementPlayListResponse',
           'FeaturesBetaAnnouncementPlayListApi', 'LocationObject', 'PlayListAssignedLocationResponse',
           'PlayListObject', 'PlayListObjectLevel']


class PlayListObjectLevel(str, Enum):
    organization = 'ORGANIZATION'


class PlayListObject(ApiModel):
    #: Unique identifier of the playlist.
    #: example: Y2lzY29zcGFyazovL3VzL0FOTk9VTkNFTUVOVC9iYzZjOTYwYi01ZDJjLTRiM2QtYjRlZC0wNWY1ZmFhMTJjZjA
    id: Optional[str] = None
    #: Unique name for the announcement playlist.
    #: example: testingAnnouncementPlaylist
    name: Optional[str] = None
    #: Count of the announcements associated with playlist.
    #: example: 1
    file_count: Optional[int] = None
    #: Indicates if the playlist has been used or not.
    #: example: True
    is_in_use: Optional[bool] = None
    #: Last updated timestamp (in UTC format) of the playlist.
    #: example: 2023-06-13T18:39:53.651Z
    last_updated: Optional[datetime] = None
    #: The level at which this playlist exists.
    #: example: ORGANIZATION
    level: Optional[PlayListObjectLevel] = None
    #: Count of the location this playlist is assigned to.
    #: example: 2
    location_count: Optional[int] = None


class AnnouncementPlayListResponse(ApiModel):
    #: Array of playlist available for a given organization.
    playlists: Optional[list[PlayListObject]] = None


class AnnouncementObject(ApiModel):
    #: Unique identifier of the announcement.
    #: example: Y2lzY29zcGFyazovL3VzL0FOTk9VTkNFTUVOVC8zMjAxNjRmNC1lNWEzLTQxZmYtYTMyNi02N2MwOThlNDFkMWQ
    id: Optional[str] = None
    #: Name of the announcement.
    #: example: Public_Announcement
    name: Optional[str] = None
    #: File name of the uploaded binary announcement greeting.
    #: example: Sample_Greetings_file.wav
    file_name: Optional[str] = None
    #: Size of the file in kilobytes.
    #: example: 356
    file_size: Optional[str] = None
    #: Media file type of the announcement file.
    #: example: WAV
    media_file_type: Optional[str] = None
    #: Last updated timestamp (in UTC format) of the announcement.
    #: example: 2023-06-13T18:39:53.651Z
    last_updated: Optional[datetime] = None
    #: The level at which this playlist exists.
    #: example: ORGANIZATION
    level: Optional[PlayListObjectLevel] = None


class AnnouncementPlayListGetResponse(ApiModel):
    #: Unique identifier of the playlist.
    #: example: Y2lzY29zcGFyazovL3VzL0FOTk9VTkNFTUVOVC9iYzZjOTYwYi01ZDJjLTRiM2QtYjRlZC0wNWY1ZmFhMTJjZjA
    id: Optional[str] = None
    #: Unique name of the playlist.
    #: example: testingAnnouncementPlaylist
    name: Optional[str] = None
    #: Last updated timestamp (in UTC format) of the playlist.
    #: example: 2024-03-06T07:06:36.396Z
    last_updated: Optional[datetime] = None
    #: Size of the files in kilobytes.
    #: example: 356
    file_size: Optional[str] = None
    #: Number of files in the playlist.
    #: example: 3
    file_count: Optional[str] = None
    #: List of announcement details associated with playlist.
    announcements: Optional[list[AnnouncementObject]] = None


class LocationObject(ApiModel):
    #: Unique identifier of the location.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi81ZTk3MzFlNy1iOWQ0LTRmMWQtYjYyMi05NDgwMDhhMjkzMzM
    id: Optional[str] = None
    #: Name of the location.
    #: example: RCDN
    name: Optional[str] = None


class PlayListAssignedLocationResponse(ApiModel):
    #: Unique identifier of the playlist.
    #: example: Y2lzY29zcGFyazovL3VzL0FOTk9VTkNFTUVOVC9iYzZjOTYwYi01ZDJjLTRiM2QtYjRlZC0wNWY1ZmFhMTJjZjA
    id: Optional[str] = None
    #: Array of locations with which the playlist is associated.
    locations: Optional[list[LocationObject]] = None


class FeaturesBetaAnnouncementPlayListApi(ApiChild, base='telephony/config/announcements/playlists'):
    """
    Features:  Beta Announcement PlayList
    
    Features: Announcement PlayList support reading and writing of Webex Calling Announcement PlayList settings for a
    specific organization. The playlist has multiple announcement files which will be played where the announcement
    playlist is selected.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def fetch_list_of_announcement_playlist_on_organization_level(self,
                                                                  org_id: str = None) -> list[AnnouncementPlayListResponse]:
        """
        Fetch list of announcement playlist on organization level

        Fetch a list of announcement playlist at an organization.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Get announcements playlist in this organization.
        :type org_id: str
        :rtype: list[AnnouncementPlayListResponse]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[AnnouncementPlayListResponse]).validate_python(data['playlists'])
        return r

    def create_announcement_playlist_at_organization_level(self, name: str, announcement_ids: list[str],
                                                           org_id: str = None) -> str:
        """
        Create announcement Playlist at organization level

        Create announcement Playlist at an organization level. A maximum of 25 announcement files can be included in a
        single playlist.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param name: Unique name for the announcement playlist.
        :type name: str
        :param announcement_ids: Array of `announcementIds` associated with the playlist.
        :type announcement_ids: list[str]
        :param org_id: Create an announcement playlist in this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['announcementIds'] = announcement_ids
        url = self.ep()
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def fetch_details_of_announcement_playlist_at_the_organization_level(self, play_list_id: str,
                                                                         org_id: str = None) -> AnnouncementPlayListGetResponse:
        """
        Fetch details of announcement playlist at the organization level

        Fetch details of announcement playlist by its ID at an organization level.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param play_list_id: Unique identifier of an announcement playlist.
        :type play_list_id: str
        :param org_id: Get an announcement playlist in this organization.
        :type org_id: str
        :rtype: :class:`AnnouncementPlayListGetResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{play_list_id}')
        data = super().get(url, params=params)
        r = AnnouncementPlayListGetResponse.model_validate(data)
        return r

    def modify_announcement_playlist_at_organization_level(self, play_list_id: str, name: str = None,
                                                           announcement_ids: list[str] = None, org_id: str = None):
        """
        Modify announcement playlist at organization level

        Modify an existing announcement playlist at an organization level.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param play_list_id: Unique identifier of an announcement playlist.
        :type play_list_id: str
        :param name: Unique name for the announcement playlist.
        :type name: str
        :param announcement_ids: Array of `announcementIds` associated with the playlist.
        :type announcement_ids: list[str]
        :param org_id: Modify an announcement playlist in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if announcement_ids is not None:
            body['announcementIds'] = announcement_ids
        url = self.ep(f'{play_list_id}')
        super().put(url, params=params, json=body)

    def delete_an_announcement_playlist_of_the_organization(self, play_list_id: str, org_id: str = None):
        """
        Delete an announcement playlist of the organization

        Delete an announcement playlist for an organization.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param play_list_id: Unique identifier of an announcement playlist.
        :type play_list_id: str
        :param org_id: Delete an announcement playlist in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{play_list_id}')
        super().delete(url, params=params)

    def fetch_list_of_locations_which_are_assigned_to_the_announcement_playlist(self, play_list_id: str,
                                                                                org_id: str = None) -> PlayListAssignedLocationResponse:
        """
        Fetch list of locations which are assigned to the announcement playlist

        Fetch list of locations which are assigned to the given announcement playlist

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param play_list_id: Unique identifier of playlist.
        :type play_list_id: str
        :param org_id: Get location associated to a playlist in this organization.
        :type org_id: str
        :rtype: :class:`PlayListAssignedLocationResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{play_list_id}/locations')
        data = super().get(url, params=params)
        r = PlayListAssignedLocationResponse.model_validate(data)
        return r

    def modify_list_of_assigned_locations_to_the_announcement_playlist(self, play_list_id: str,
                                                                       location_ids: list[str], org_id: str = None):
        """
        Modify list of assigned locations to the announcement playlist

        Modify list of assigned locations or add new locations to the announcement playlist. This will assing the
        playlist to the location's music on hold.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param play_list_id: Unique identifier of an announcement playlist.
        :type play_list_id: str
        :param location_ids: Array of location IDs with which the playlist is associated.
        :type location_ids: list[str]
        :param org_id: Modify an assign location for announcement playlist for organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['locationIds'] = location_ids
        url = self.ep(f'{play_list_id}/locations')
        super().put(url, params=params, json=body)

from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AnnouncementObject', 'AnnouncementPlaylistGetResponse', 'AnnouncementPlaylistResponse',
           'FeaturesAnnouncementPlaylistApi', 'LocationObject', 'PlaylistAssignedLocationResponse', 'PlaylistObject',
           'PlaylistObjectLevel']


class PlaylistObjectLevel(str, Enum):
    organization = 'ORGANIZATION'


class PlaylistObject(ApiModel):
    #: Unique identifier of the playlist.
    id: Optional[str] = None
    #: Unique name for the announcement playlist.
    name: Optional[str] = None
    #: Count of the announcements associated with playlist.
    file_count: Optional[int] = None
    #: Indicates if the playlist has been used or not.
    is_in_use: Optional[bool] = None
    #: Last updated timestamp (in UTC format) of the playlist.
    last_updated: Optional[datetime] = None
    #: The level at which this playlist exists.
    level: Optional[PlaylistObjectLevel] = None
    #: Count of the location this playlist is assigned to.
    location_count: Optional[int] = None


class AnnouncementPlaylistResponse(ApiModel):
    #: Array of playlist available for a given organization.
    playlists: Optional[list[PlaylistObject]] = None


class AnnouncementObject(ApiModel):
    #: Unique identifier of the announcement.
    id: Optional[str] = None
    #: Name of the announcement.
    name: Optional[str] = None
    #: File name of the uploaded binary announcement greeting.
    file_name: Optional[str] = None
    #: Size of the file in kilobytes.
    file_size: Optional[str] = None
    #: Media file type of the announcement file.
    media_file_type: Optional[str] = None
    #: Last updated timestamp (in UTC format) of the announcement.
    last_updated: Optional[datetime] = None
    #: The level at which this playlist exists.
    level: Optional[PlaylistObjectLevel] = None


class AnnouncementPlaylistGetResponse(ApiModel):
    #: Unique identifier of the playlist.
    id: Optional[str] = None
    #: Unique name of the playlist.
    name: Optional[str] = None
    #: Last updated timestamp (in UTC format) of the playlist.
    last_updated: Optional[datetime] = None
    #: Size of the files in kilobytes.
    file_size: Optional[str] = None
    #: Number of files in the playlist.
    file_count: Optional[str] = None
    #: List of announcement details associated with playlist.
    announcements: Optional[list[AnnouncementObject]] = None


class LocationObject(ApiModel):
    #: Unique identifier of the location.
    id: Optional[str] = None
    #: Name of the location.
    name: Optional[str] = None


class PlaylistAssignedLocationResponse(ApiModel):
    #: Unique identifier of the playlist.
    id: Optional[str] = None
    #: Array of locations with which the playlist is associated.
    locations: Optional[list[LocationObject]] = None


class FeaturesAnnouncementPlaylistApi(ApiChild, base='telephony/config/announcements/playlists'):
    """
    Features: Announcement Playlist
    
    Features: Announcement Playlist support reading and writing of Webex Calling Announcement Playlist settings for a
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
                                                                  org_id: str = None) -> list[AnnouncementPlaylistResponse]:
        """
        Fetch list of announcement playlist on organization level

        Fetch a list of announcement playlist at an organization.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Get announcements playlist in this organization.
        :type org_id: str
        :rtype: list[AnnouncementPlaylistResponse]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[AnnouncementPlaylistResponse]).validate_python(data['playlists'])
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

    def delete_an_announcement_playlist_of_the_organization(self, playlist_id: str, org_id: str = None):
        """
        Delete an announcement playlist of the organization

        Delete an announcement playlist for an organization.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param playlist_id: Unique identifier of an announcement playlist.
        :type playlist_id: str
        :param org_id: Delete an announcement playlist in this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{playlist_id}')
        super().delete(url, params=params)

    def fetch_details_of_announcement_playlist_at_the_organization_level(self, playlist_id: str,
                                                                         org_id: str = None) -> AnnouncementPlaylistGetResponse:
        """
        Fetch details of announcement playlist at the organization level

        Fetch details of announcement playlist by its ID at an organization level.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param playlist_id: Unique identifier of an announcement playlist.
        :type playlist_id: str
        :param org_id: Get an announcement playlist in this organization.
        :type org_id: str
        :rtype: :class:`AnnouncementPlaylistGetResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{playlist_id}')
        data = super().get(url, params=params)
        r = AnnouncementPlaylistGetResponse.model_validate(data)
        return r

    def modify_announcement_playlist_at_organization_level(self, playlist_id: str, name: str = None,
                                                           announcement_ids: list[str] = None, org_id: str = None):
        """
        Modify announcement playlist at organization level

        Modify an existing announcement playlist at an organization level.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param playlist_id: Unique identifier of an announcement playlist.
        :type playlist_id: str
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
        url = self.ep(f'{playlist_id}')
        super().put(url, params=params, json=body)

    def fetch_list_of_locations_which_are_assigned_to_the_announcement_playlist(self, playlist_id: str,
                                                                                org_id: str = None) -> PlaylistAssignedLocationResponse:
        """
        Fetch list of locations which are assigned to the announcement playlist

        Fetch list of locations which are assigned to the given announcement playlist

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param playlist_id: Unique identifier of playlist.
        :type playlist_id: str
        :param org_id: Get location associated to a playlist in this organization.
        :type org_id: str
        :rtype: :class:`PlaylistAssignedLocationResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{playlist_id}/locations')
        data = super().get(url, params=params)
        r = PlaylistAssignedLocationResponse.model_validate(data)
        return r

    def modify_list_of_assigned_locations_to_the_announcement_playlist(self, playlist_id: str, location_ids: list[str],
                                                                       org_id: str = None):
        """
        Modify list of assigned locations to the announcement playlist

        Modify list of assigned locations or add new locations to the announcement playlist. This will assing the
        playlist to the location's music on hold.

        This API requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param playlist_id: Unique identifier of an announcement playlist.
        :type playlist_id: str
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
        url = self.ep(f'{playlist_id}/locations')
        super().put(url, params=params, json=body)

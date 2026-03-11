import builtins
from datetime import datetime
from typing import Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.common import IdAndName

__all__ = ['PlaylistAnnouncement', 'PlayListApi', 'PlayList', 'PlaylistUsageType', 'PlaylistUsageLocation',
           'PlaylistUsageLocationFeatureRef', 'PlaylistUsage']


class PlaylistAnnouncement(ApiModel):
    #: Unique identifier of the announcement.
    id: Optional[str] = None
    #: Name of the announcement.
    name: Optional[str] = None
    #: File name of the uploaded binary announcement greeting.
    file_name: Optional[str] = None
    #: Size of the file in kilobytes.
    file_size: Optional[int] = None
    #: Media file type of the announcement file.
    media_file_type: Optional[str] = None
    #: Last updated timestamp (in UTC format) of the announcement.
    last_updated: Optional[datetime] = None
    #: The level at which this playlist exists.
    level: Optional[str] = None


class PlayList(ApiModel):
    #: Unique identifier of the playlist.
    id: Optional[str] = None
    #: Unique name for the announcement playlist.
    name: Optional[str] = None
    #: Size of the files in kilobytes.
    file_size: Optional[int] = None
    #: Count of the announcements associated with playlist.
    file_count: Optional[int] = None
    #: Indicates if the playlist has been used or not.
    is_in_use: Optional[bool] = None
    #: Last updated timestamp (in UTC format) of the playlist.
    last_updated: Optional[datetime] = None
    #: The level at which this playlist exists.
    level: Optional[str] = None
    #: Count of the location this playlist is assigned to.
    location_count: Optional[int] = None
    #: List of announcement details associated with playlist.
    announcements: Optional[list[PlaylistAnnouncement]] = None


class PlaylistUsageLocationFeatureRef(ApiModel):
    #: Feature identifier.
    id: Optional[str] = None
    #: Feature name.
    name: Optional[str] = None
    #: Feature type.
    type: Optional[str] = None


class PlaylistUsageLocation(ApiModel):
    #: Location identifier.
    id: Optional[str] = None
    #: Location name.
    name: Optional[str] = None
    #: Feature referencing the playlist.
    feature_reference: Optional[PlaylistUsageLocationFeatureRef] = None


class PlaylistUsage(ApiModel):
    #: Identifier of the playlist.
    id: Optional[str] = None
    #: List of locations using this playlist.
    locations: Optional[list[PlaylistUsageLocation]] = None


class PlaylistUsageType(str, Enum):
    feature = 'feature'
    location = 'location'


class PlayListApi(ApiChild, base='telephony/config/announcements/playlists'):
    """
    Features:  Announcement PlayList

    Features: Announcement PlayList support reading and writing of Webex Calling Announcement PlayList settings for a
    specific organization. The playlist has multiple announcement files which will be played where the announcement
    playlist is selected.

    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope
    of `spark-admin:telephony_config_read`.

    Modifying these organization settings requires a full administrator auth token with a scope
    of `spark-admin:telephony_config_write`.

    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def list(self, org_id: str = None) -> list[PlayList]:
        """
        List Announcement Playlists

        Fetch a list of announcement playlist at an organization.

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param org_id: Get announcements playlist in this organization.
        :type org_id: str
        :rtype: list[:class:`PlayList`]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[PlayList]).validate_python(data['playlists'])
        return r

    def create(self, name: str, announcement_ids: builtins.list[str], org_id: str = None) -> str:
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

    def usage(self, play_list_id: str, playlist_usage_type: PlaylistUsageType = None) -> PlaylistUsage:
        """
        Get Playlist Usage

        :param play_list_id: Unique identifier of the playlist.
        :type play_list_id: str
        :param playlist_usage_type: Filter usage by type.
        :type playlist_usage_type: PlaylistUsageType
        :rtype: :class:`PlaylistUsage`
        """
        params = {}
        if playlist_usage_type is not None:
            params['playlistUsageType'] = enum_str(playlist_usage_type)
        url = self.ep(f'{play_list_id}/usage')
        data = super().get(url, params=params)
        r = PlaylistUsage.model_validate(data)
        return r

    def delete(self, play_list_id: str, org_id: str = None):
        """
        Delete Announcement Playlist

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

    def details(self, play_list_id: str, org_id: str = None) -> PlayList:
        """
        Get Announcement Playlist

        Fetch details of announcement playlist by its ID at an organization level.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param play_list_id: Unique identifier of an announcement playlist.
        :type play_list_id: str
        :param org_id: Get an announcement playlist in this organization.
        :type org_id: str
        :rtype: :class:`PlayList`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{play_list_id}')
        data = super().get(url, params=params)
        r = PlayList.model_validate(data)
        return r

    def modify(self, play_list_id: str, name: str = None, announcement_ids: builtins.list[str] = None,
               org_id: str = None):
        """
        Update Announcement Playlist

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

    def assigned_locations(self, play_list_id: str, org_id: str = None) -> builtins.list[IdAndName]:
        """
        List Playlist Locations

        Fetch list of locations which are assigned to the given announcement playlist

        This API requires a full or read-only administrator or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param play_list_id: Unique identifier of playlist.
        :type play_list_id: str
        :param org_id: Get location associated to a playlist in this organization.
        :type org_id: str
        :rtype: :class:`PlayListAssignedLocations`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{play_list_id}/locations')
        data = super().get(url, params=params)
        r = TypeAdapter(list[IdAndName]).validate_python(data['locations'])
        return r

    def modify_assigned_locations(self, play_list_id: str, location_ids: builtins.list[str], org_id: str = None):
        """
        Update Playlist Locations

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

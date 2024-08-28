from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AudioAnnouncementFileGetObject', 'AudioAnnouncementFileGetObjectLevel',
           'AudioAnnouncementFileGetObjectMediaFileType', 'BetaFeaturesLocationCallSettingsWithPlaylistApi',
           'GetMusicOnHoldObject', 'GetMusicOnHoldObjectGreeting', 'PlayListObject']


class GetMusicOnHoldObjectGreeting(str, Enum):
    #: Play default music when call is placed on hold or parked. The system plays music to fill the silence and lets
    #: the customer know they are still connected.
    system = 'SYSTEM'
    #: Play previously uploaded custom music when call is placed on hold or parked.
    custom = 'CUSTOM'


class AudioAnnouncementFileGetObjectMediaFileType(str, Enum):
    #: WAV File Extension.
    wav = 'WAV'
    #: WMA File Extension.
    wma = 'WMA'
    #: 3GP File Extension.
    d3_gp = '3GP'


class AudioAnnouncementFileGetObjectLevel(str, Enum):
    #: Specifies this audio file is configured across organisation.
    organization = 'ORGANIZATION'
    #: Specifies this audio file is configured across location.
    location = 'LOCATION'


class AudioAnnouncementFileGetObject(ApiModel):
    #: A unique identifier for the announcement.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QzVjBPWFIxWjJkM2FFQm1iR1Y0TWk1amFYTmpieTVqYjIw
    id: Optional[str] = None
    #: Audio announcement file name.
    #: example: AUDIO_FILE.wav
    file_name: Optional[str] = None
    #: Audio announcement file type.
    #: example: WAV
    media_file_type: Optional[AudioAnnouncementFileGetObjectMediaFileType] = None
    #: Audio announcement file type location.
    #: example: ORGANIZATION
    level: Optional[AudioAnnouncementFileGetObjectLevel] = None


class PlayListObject(ApiModel):
    #: A unique identifier for the playlist.
    #: example: Y2lzY29zcGFyazovL3VzL0FOTk9VTkNFTUVOVC9iYzZjOTYwYi01ZDJjLTRiM2QtYjRlZC0wNWY1ZmFhMTJjZjA
    id: Optional[str] = None
    #: Unique name for the playlist.
    #: example: testingAnnouncementPlaylist
    name: Optional[str] = None


class GetMusicOnHoldObject(ApiModel):
    #: If enabled, music will be played when call is placed on hold.
    #: example: True
    call_hold_enabled: Optional[bool] = None
    #: If enabled, music will be played when call is parked.
    #: example: True
    call_park_enabled: Optional[bool] = None
    #: Greeting type for the location.
    #: example: SYSTEM
    greeting: Optional[GetMusicOnHoldObjectGreeting] = None
    #: Announcement Audio File details when greeting is selected to be `CUSTOM`.
    audio_file: Optional[AudioAnnouncementFileGetObject] = None
    #: Playlist details when greeting is selected to be `CUSTOM`.
    playlist: Optional[PlayListObject] = None


class BetaFeaturesLocationCallSettingsWithPlaylistApi(ApiChild, base='telephony/config/locations'):
    """
    Beta Features: Location Call Settings with Playlist
    
    Location Call Settings  supports reading and writing of Webex Calling Location settings for a specific
    organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def update_music_on_hold(self, location_id: str, greeting: GetMusicOnHoldObjectGreeting,
                             call_hold_enabled: bool = None, call_park_enabled: bool = None,
                             audio_file: AudioAnnouncementFileGetObject = None, playlist_id: str = None,
                             org_id: str = None):
        """
        Update Music On Hold

        Update the location's music on hold settings.

        Location music on hold settings allows you to play music when a call is placed on hold or parked.

        Updating a location's music on hold settings requires a full administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Update music on hold settings for this location.
        :type location_id: str
        :param greeting: Greeting type for the location.
        :type greeting: GetMusicOnHoldObjectGreeting
        :param call_hold_enabled: If enabled, music will be played when call is placed on hold.
        :type call_hold_enabled: bool
        :param call_park_enabled: If enabled, music will be played when call is parked.
        :type call_park_enabled: bool
        :param audio_file: Announcement Audio File details when greeting is selected to be `CUSTOM`.
        :type audio_file: AudioAnnouncementFileGetObject
        :param playlist_id: A unique identifier for the playlist.
        :type playlist_id: str
        :param org_id: Update music on hold settings for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if call_hold_enabled is not None:
            body['callHoldEnabled'] = call_hold_enabled
        if call_park_enabled is not None:
            body['callParkEnabled'] = call_park_enabled
        body['greeting'] = enum_str(greeting)
        if audio_file is not None:
            body['audioFile'] = audio_file.model_dump(mode='json', by_alias=True, exclude_none=True)
        if playlist_id is not None:
            body['playlistId'] = playlist_id
        url = self.ep(f'{location_id}/musicOnHold')
        super().put(url, params=params, json=body)

    def get_music_on_hold(self, location_id: str, org_id: str = None) -> GetMusicOnHoldObject:
        """
        Get Music On Hold

        Retrieve the location's music on hold settings.

        Location music on hold settings allows you to play music when a call is placed on hold or parked.

        Retrieving a location's music on hold settings requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve music on hold settings for this location.
        :type location_id: str
        :param org_id: Retrieve music on hold settings for this organization.
        :type org_id: str
        :rtype: :class:`GetMusicOnHoldObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{location_id}/musicOnHold')
        data = super().get(url, params=params)
        r = GetMusicOnHoldObject.model_validate(data)
        return r

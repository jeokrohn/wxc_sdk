from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['AnnouncementResponse', 'BetaFeaturesAnnouncementRepositoryWithPlayListApi', 'FeatureReferenceObject',
           'PlayListObject']


class FeatureReferenceObject(ApiModel):
    #: Unique identifier of the call feature referenced. The call Feature can be Auto Attendant, Call Queue or Music On
    #: hold.
    #: example: Y2lzY29zcGFyazovL3VzL0FVVE9fQVRURU5EQU5UL2QzVjBPWFIxWjJkM2FFQm1iR1Y0TWk1amFYTmpieTVqYjIw
    id: Optional[str] = None
    #: Name of the call feature referenced.
    #: example: Main Line AA - Test
    name: Optional[str] = None
    #: Resource Type of the call feature.
    #: example: Auto Attendant
    type: Optional[str] = None
    #: Unique identifier of the location.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi81ZTk3MzFlNy1iOWQ0LTRmMWQtYjYyMi05NDgwMDhhMjkzMzM
    location_id: Optional[str] = None
    #: Location name of the announcement file.
    #: example: RCDN
    location_name: Optional[str] = None


class PlayListObject(ApiModel):
    #: A unique identifier for the playlist.
    #: example: Y2lzY29zcGFyazovL3VzL0FOTk9VTkNFTUVOVC9iYzZjOTYwYi01ZDJjLTRiM2QtYjRlZC0wNWY1ZmFhMTJjZjA
    id: Optional[str] = None
    #: Unique name for the playlist.
    #: example: testingAnnouncementPlaylist
    name: Optional[str] = None


class AnnouncementResponse(ApiModel):
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
    #: Reference count of the call features this announcement is assigned to.
    #: example: 1
    feature_reference_count: Optional[int] = None
    #: Call features referenced by this announcement.
    feature_references: Optional[list[FeatureReferenceObject]] = None
    #: List of playlist available for selection.
    playlists: Optional[list[PlayListObject]] = None


class BetaFeaturesAnnouncementRepositoryWithPlayListApi(ApiChild, base='telephony/config/announcements'):
    """
    Beta Features: Announcement Repository with PlayList
    
    Features: Announcement Repository support reading and writing of Webex Calling Announcement Repository settings for
    a specific organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator or location administrator
    auth token with a scope of `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def fetch_details_of_a_binary_announcement_greeting_at_the_organization_level(self, announcement_id: str,
                                                                                  org_id: str = None) -> AnnouncementResponse:
        """
        Fetch details of a binary announcement greeting at the organization level

        Fetch details of a binary announcement greeting by its ID at an organization level.

        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.

        This API requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Get an announcement in this organization.
        :type org_id: str
        :rtype: :class:`AnnouncementResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{announcement_id}')
        data = super().get(url, params=params)
        r = AnnouncementResponse.model_validate(data)
        return r

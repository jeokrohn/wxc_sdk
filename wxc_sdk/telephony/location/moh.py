"""
MoH API for locations

"""
from typing import Optional

from ...api_child import ApiChild
from ...base import ApiModel
from ...base import SafeEnum as Enum
from ...common import AnnAudioFile, IdAndName

__all__ = ['LocationMoHGreetingType', 'LocationMoHSetting', 'LocationMoHApi']


class LocationMoHGreetingType(str, Enum):
    """
    Greeting type for the location.
    """
    #: Play default music when call is placed on hold or parked. The system plays music to fill the silence and lets
    #: the customer know they are still connected.
    system = 'SYSTEM'
    #: Play custom music when call is placed on hold or parked. An audio file must already have been successfully
    #: uploaded to specify this option.
    custom = 'CUSTOM'


class LocationMoHSetting(ApiModel):
    """
    location's music on hold settings.
    """
    #: If enabled, music will be played when call is placed on hold.
    call_hold_enabled: Optional[bool] = None
    #: If enabled, music will be played when call is parked.
    call_park_enabled: Optional[bool] = None
    #: Greeting type for the location.
    greeting: Optional[LocationMoHGreetingType] = None
    #: Announcement Audio File details when greeting is selected to be `CUSTOM`.
    audio_file: Optional[AnnAudioFile] = None
    #: Playlist details when greeting is selected to be `CUSTOM`.
    playlist: Optional[IdAndName] = None

    def update(self) -> dict:
        """
        date for update

        :meta private:
        """
        r = self.model_dump(mode='json', by_alias=True, exclude_none=True, exclude={'playlist'})
        if self.playlist:
            r['playlistId'] = self.playlist.id
        return r


class LocationMoHApi(ApiChild, base='telephony/config/locations'):
    """
    Location Music on Hold API
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific feature endpoint like
        /v1/telephony/config/locations/{locationId}/musicOnHold

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/musicOnHold{path}')
        return ep

    def read(self, location_id: str, org_id: str = None) -> LocationMoHSetting:
        """
        Get Music On Hold

        Retrieve the location's music on hold settings.

        Location's music on hold settings allows you to play music when a call is placed on hold or parked.

        Retrieving location's music on hold settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        :return: MoH settings
        :rtype: :class:`LocationMoHSetting`
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        data = self.get(url, params=params)
        return LocationMoHSetting.model_validate(data)

    def update(self, location_id: str, settings: LocationMoHSetting, org_id: str = None):
        """
        Update Music On Hold

        Update the location's music on hold settings.

        Location music on hold settings allows you to play music when a call is placed on hold or parked.

        Updating a location's music on hold settings requires a full administrator or location administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Update music on hold settings for this location.
        :type location_id: str
        :param settings: new settings
        :type settings: :class:`LocationMoHSetting`
        :param org_id: Update music on hold settings for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        self.put(url, params=params, json=settings.update())

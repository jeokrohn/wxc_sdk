"""
API for location voicemail settings
"""
from typing import Optional

from ...api_child import ApiChild
from ...base import ApiModel

__all__ = ['LocationVoiceMailSettings', 'LocationVoicemailSettingsApi']


class LocationVoiceMailSettings(ApiModel):
    """
    voicemail settings for a specific location
    """
    #: Set to true to enable voicemail transcription.
    voicemail_transcription_enabled: Optional[bool]


class LocationVoicemailSettingsApi(ApiChild, base='telephony/config/locations'):
    """
    location voicemail settings API, for now only enable/disable Vm transcription
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific
        telephony/config/locations/{locationId}/voicemail

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/voicemail{path}')
        return ep

    def read(self, *, location_id: str, org_id: str = None) -> LocationVoiceMailSettings:
        """
        Get Location Voicemail

        Retrieve voicemail settings for a specific location.

        Location's voicemail settings allows you to enable voicemail transcription for a specific location.

        Retrieving location's voicemail settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.


        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        :return: location voicemail settings
        :rtype: :class:`LocationVoiceMailSettings`
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        data = self.get(url, params=params)
        return LocationVoiceMailSettings.parse_obj(data)

    def update(self, *, location_id: str, settings: LocationVoiceMailSettings, org_id: str = None):
        """
        Get Location Voicemail

        Retrieve voicemail settings for a specific location.

        Location's voicemail settings allows you to enable voicemail transcription for a specific location.

        Retrieving location's voicemail settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.


        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param settings: new settings
        :type settings: :class:`LocationVoiceMailSettings`
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = settings.json()
        self.put(url, params=params, data=body)

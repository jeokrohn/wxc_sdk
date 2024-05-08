from typing import Optional

from wxc_sdk.base import enum_str, ApiModel
from wxc_sdk.common import Greeting, AnnAudioFile
from wxc_sdk.person_settings.common import PersonSettingsApiChild

__all__ = ['MusicOnHold', 'MusicOnHoldApi']


class MusicOnHold(ApiModel):
    #: Music on hold enabled or disabled for the entity.
    moh_enabled: Optional[bool] = None
    #: Music on hold enabled or disabled for the location. The music on hold setting returned in the response is used
    #: only when music on hold is enabled at the location level. When `mohLocationEnabled` is false and `mohEnabled`
    #: is true, music on hold is disabled for the user. When `mohLocationEnabled` is true and `mohEnabled` is false,
    #: music on hold is turned off for the user. In both cases, music on hold will not be played.
    moh_location_enabled: Optional[bool] = None
    #: Greeting type for the person.
    #: example: DEFAULT
    greeting: Optional[Greeting] = None
    #: Announcement Audio File details when greeting is selected to be `CUSTOM`.
    audio_announcement_file: Optional[AnnAudioFile] = None

    def update(self)->dict:
        """
        Data for update

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True,
                               exclude_unset=True, exclude_none=False,
                               exclude={'moh_location_enabled'})


class MusicOnHoldApi(PersonSettingsApiChild):

    feature = 'musicOnHold'

    def read(self, entity_id: str, org_id: str = None) -> MusicOnHold:
        """
        Retrieve Music On Hold Settings for a Person, virtual line, or workspace.

        Retrieve the music on hold settings.

        Music on hold is played when a caller is put on hold, or the call is parked.

        Retrieving a person's music on hold settings requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for the person, virtual line, or workspace.
        :type entity_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`GetMusicOnHoldObject`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.f_ep(entity_id)
        data = super().get(url, params=params)
        r = MusicOnHold.model_validate(data)
        return r

    def configure(self, entity_id: str, settings: MusicOnHold,
                  org_id: str = None):
        """
        Configure Music On Hold Settings for a Personvirtual line, or workspace.

        Configure music on hold settings.

        Music on hold is played when a caller is put on hold, or the call is parked.

        To configure music on hold settings for a person, music on hold setting must be enabled for this location.

        Updating a person's music on hold settings requires a full or user administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param entity_id: Unique identifier for the person, virtual line, or workspace.
        :type entity_id: str
        :param settings: new MOH settings
        :type settings: MusicOnHold
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        body = settings.update()
        url = self.f_ep(entity_id)
        super().put(url, params=params, json=body)
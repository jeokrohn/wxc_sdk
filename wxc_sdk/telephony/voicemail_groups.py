"""
Voicemail groups API
"""
from typing import Optional

from pydantic import Field

from ..api_child import ApiChild

__all__ = ['VoicemailGroup', 'VoicemailGroupsApi']

from ..base import to_camel, ApiModel


class VoicemailGroup(ApiModel):
    #: Voicemail Group Id.
    group_id: str = Field(alias='id')
    #: Voicemail Group Name.
    name: str
    #: Location Name.
    location_name: str
    #: location id
    location_id: str
    #: Extension of the voicemail group.
    extension: Optional[str]
    #: Phone number of the voicemail group.
    phone_number: Optional[str]
    #: If enabled, incoming calls are sent to voicemail.
    enabled: bool
    #: Flag to indicate if the number is toll free.
    toll_free_number: Optional[bool]


class VoicemailGroupsApi(ApiChild, base='telephony/config/voicemailGroups'):
    """
    API for location private network connect API settings
    """

    def list(self, *, location_id: str = None, name: str = None, phone_number: str = None, org_id: str = None):
        params = {to_camel(p): v for p, v in locals().items() if p != 'self' and v is not None}
        url = self.ep()
        return self.session.follow_pagination(url=url, model=VoicemailGroup, params=params, item_key='voicemailGroups')

"""
Person PTT settings API
"""
from enum import Enum
from typing import Optional, Union

from .common import PersonSettingsApiChild
from ..base import ApiModel

__all__ = ['PTTConnectionType', 'PushToTalkAccessType', 'PushToTalkSettings', 'PushToTalkApi']

from ..common import MonitoredMember


class PTTConnectionType(str, Enum):
    #: Push-to-Talk initiators can chat with this person but only in one direction. The person you enable Push-to-Talk
    #: for cannot respond.
    one_way = 'ONE_WAY'
    #: Push-to-Talk initiators can chat with this person in a two-way conversation. The person you enable
    #: Push-to-Talk for can respond.
    two_way = 'TWO_WAY'


class PushToTalkAccessType(str, Enum):
    #: List of people that are allowed to use the Push-to-Talk feature to interact with the person being configured.
    allow_members = 'ALLOW_MEMBERS'
    #: List of people that are disallowed to interact using the Push-to-Talk feature with the person being configured.
    block_members = 'BLOCK_MEMBERS'


class PushToTalkSettings(ApiModel):
    """
    Push To Talk settings
    """
    #: Set to true to enable the Push-to-Talk feature. When enabled, a person receives a Push-to-Talk call and
    #: answers the call automatically.
    allow_auto_answer: Optional[bool]
    #: Specifies the connection type to be used.
    connection_type: Optional[PTTConnectionType]
    #: Specifies the access type to be applied when evaluating the member list.
    access_type: Optional[PushToTalkAccessType]
    #: List of people that are allowed or disallowed to interact using the Push-to-Talk feature.
    #: can be just a member id for a configure() call
    members: Optional[list[Union[str, MonitoredMember]]]


class PushToTalkApi(PersonSettingsApiChild):
    """
    API for person's PTT settings
    """

    feature = 'pushToTalk'

    def read(self, *, person_id: str, org_id: str = None) -> PushToTalkSettings:
        """
        Read Push-to-Talk Settings for a Person
        Retrieve a Person's Push-to-Talk Settings

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: PTT settings for specific user
        :rtype: PushToTalkSettings
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return PushToTalkSettings.parse_obj(self.get(ep, params=params))

    def configure(self, *, person_id: str, settings: PushToTalkSettings, org_id: str = None):
        """
        Configure Push-to-Talk Settings for a Person

        Configure a Person's Push-to-Talk Settings

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: new setting to be applied. For members only the ID needs to be set
        :type settings: PushToTalkSettings
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        if settings.members:
            # for an update member is just a list of IDs
            body_settings = settings.copy(deep=True)
            members = [m.member_id if isinstance(m, MonitoredMember) else m
                       for m in settings.members]
            body_settings.members = members
        else:
            body_settings = settings
        body = body_settings.json(exclude_none=False,
                                  exclude_unset=True)
        self.put(ep, params=params, data=body)

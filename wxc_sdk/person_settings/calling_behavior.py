"""
Calling behavior API
"""
from enum import Enum
from typing import Optional

from .common import PersonSettingsApiChild
from ..base import ApiModel

__all__ = ['BehaviorType', 'CallingBehavior', 'CallingBehaviorApi']


class BehaviorType(str, Enum):
    """
    The Calling Behavior setting for the person
    """
    #: Calling in Webex Teams(formerly Spark Call), or Hybrid Calling.
    native = 'NATIVE_WEBEX_TEAMS_CALLING'
    #: Cisco Jabber app
    cisco_tel = 'CALL_WITH_APP_REGISTERED_FOR_CISCOTEL'
    #: Third-Party app
    third_party = 'CALL_WITH_APP_REGISTERED_FOR_TEL'
    #: Webex Calling app
    webex_calling = 'CALL_WITH_APP_REGISTERED_FOR_WEBEXCALLTEL'
    #: Calling in Webex Teams (Unified CM)
    native_sip_call_zo_ucm = 'NATIVE_SIP_CALL_TO_UCM'


class CallingBehavior(ApiModel):
    #: The current Calling Behavior setting for the person. If null, the effective Calling Behavior will be the
    #: Organization's current default.
    behavior_type: Optional[BehaviorType]
    #: The effective Calling Behavior setting for the person, will be the organization's default Calling Behavior if
    #: the user's behaviorType is set to null.
    effective_behavior_type: Optional[BehaviorType]
    #: The UC Manager Profile ID.
    profile_id: Optional[str]


class CallingBehaviorApi(PersonSettingsApiChild):
    """
    API for person's calling behavior settings
    """

    feature = 'callingBehavior'

    def read(self, *, person_id: str, org_id: str = None) -> CallingBehavior:
        """
        Read Person's Calling Behavior

        Retrieves the calling behavior and UC Manager Profile settings for the person which includes overall calling
        behavior and calling UC Manager Profile ID.

        Webex Calling Behavior controls which Webex telephony application is to be used.

        An organization has an organization-wide default Calling Behavior that may be overridden for individual persons.

        In addition, UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or
        Calling in Webex Teams (Unified CM).

        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: calling behavior setting
        :rtype: CallingBehavior
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(ep, params=params)
        return CallingBehavior.parse_obj(data)

    def configure(self, *, person_id: str, settings: CallingBehavior,
                  org_id: str = None):
        """
        Configure a Person's Calling Behavior

        Modifies the calling behavior settings for the person which includes overall calling behavior and UC Manager
        Profile ID.

        Webex Calling Behavior controls which Webex telephony application is to be used.

        An organization has an organization-wide default Calling Behavior that may be overridden for individual persons.

        In addition, UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or
        Calling in Webex Teams (Unified CM).

        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: new settings
        :type settings: CallingBehavior
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = settings.json(exclude_none=False, exclude={'effective_behavior_type'}, exclude_unset=True)
        self.put(ep, params=params, data=data)

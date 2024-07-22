from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaUserCallSettingsWithPickupAndBargeInPrivacyApi', 'MonitoredPersonObject',
           'PeopleOrPlaceOrVirtualLineType', 'PrivacyGet', 'PushToTalkNumberObject']


class PeopleOrPlaceOrVirtualLineType(str, Enum):
    #: Indicates a person or list of people.
    people = 'PEOPLE'
    #: Indicates a workspace that is not assigned to a specific person such as for a shared device in a common area.
    place = 'PLACE'
    #: Indicates a virtual line or list of virtual lines.
    virtual_line = 'VIRTUAL_LINE'


class PushToTalkNumberObject(ApiModel):
    #: External phone number of the person.
    #: example: +19845551088
    external: Optional[str] = None
    #: Extension number of the person.
    #: example: 1088
    extension: Optional[str] = None
    #: Indicates whether the phone number is the primary number.
    #: example: True
    primary: Optional[bool] = None


class MonitoredPersonObject(ApiModel):
    #: Unique identifier of the person.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MWU3MDlkNy1hM2IxLTQ2MDctOTBiOC04NmE5MDgxYWFkNmE
    id: Optional[str] = None
    #: Last name of the person.
    #: example: Little
    last_name: Optional[str] = None
    #: First name of the person.
    #: example: Alice
    first_name: Optional[str] = None
    #: Display name of the person.
    #: example: Alice Little
    display_name: Optional[str] = None
    #: Type usually indicates `PEOPLE`, `PLACE` or `VIRTUAL_LINE`. Push-to-Talk and Privacy features only support
    #: `PEOPLE`.
    type: Optional[PeopleOrPlaceOrVirtualLineType] = None
    #: Email address of the person.
    #: example: alice@example.com
    email: Optional[str] = None
    #: List of phone numbers of the person.
    numbers: Optional[list[PushToTalkNumberObject]] = None


class PrivacyGet(ApiModel):
    #: When `true` auto attendant extension dialing will be enabled.
    #: example: True
    aa_extension_dialing_enabled: Optional[bool] = None
    #: When `true` auto attendant dialing by first or last name will be enabled.
    #: example: True
    aa_naming_dialing_enabled: Optional[bool] = None
    #: When `true` phone status directory privacy will be enabled.
    #: example: True
    enable_phone_status_directory_privacy: Optional[bool] = None
    #: When `true` privacy is enforced for call pickup and barge-in. Only people specified by `monitoringAgents` can
    #: pick up the call or barge in by dialing the extension.
    #: example: True
    enable_phone_status_pickup_barge_in_privacy: Optional[bool] = None
    #: List of people that are being monitored.
    monitoring_agents: Optional[list[MonitoredPersonObject]] = None


class BetaUserCallSettingsWithPickupAndBargeInPrivacyApi(ApiChild, base='people'):
    """
    Beta User Call Settings with Pickup and Barge In Privacy
    
    Person Call Settings supports modifying Webex Calling settings for a specific person.
    
    The call pickup and barge-in privacy feature enables the admin to control people who can pick up the call or
    barge-in by dialing the extension.
    
    Viewing People requires a full, user, or read-only administrator or location administrator auth token with a scope
    of `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by
    a person to read their settings.
    
    Configuring People settings requires a full or user administrator or location administrator auth token with the
    `spark-admin:people_write` scope or, for select APIs, a user auth token with `spark:people_write` scope can be
    used by a person to update their settings.
    """

    def get_a_person_s_privacy_settings(self, person_id: str, org_id: str = None) -> PrivacyGet:
        """
        Get a person's Privacy Settings

        Get a person's privacy settings for the specified person ID.

        The privacy feature enables the person's line to be monitored by others and determine if they can be reached by
        Auto Attendant services.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope of
        spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`PrivacyGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/features/privacy')
        data = super().get(url, params=params)
        r = PrivacyGet.model_validate(data)
        return r

    def configure_a_person_s_privacy_settings(self, person_id: str, aa_extension_dialing_enabled: str = None,
                                              aa_naming_dialing_enabled: str = None,
                                              enable_phone_status_directory_privacy: str = None,
                                              enable_phone_status_pickup_barge_in_privacy: str = None,
                                              monitoring_agents: list[str] = None, org_id: str = None):
        """
        Configure a person's Privacy Settings

        Configure a person's privacy settings for the specified person ID.

        The privacy feature enables the person's line to be monitored by others and determine if they can be reached by
        Auto Attendant services.

        This API requires a full or user administrator or location administrator auth token with the
        spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param aa_extension_dialing_enabled: When `true` auto attendant extension dialing is enabled.
        :type aa_extension_dialing_enabled: str
        :param aa_naming_dialing_enabled: When `true` auto attendant dialing by first or last name is enabled.
        :type aa_naming_dialing_enabled: str
        :param enable_phone_status_directory_privacy: When `true` phone status directory privacy is enabled.
        :type enable_phone_status_directory_privacy: str
        :param enable_phone_status_pickup_barge_in_privacy: When `true` privacy is enforced for call pickup and
            barge-in. Only people specified by `monitoringAgents` can pick up the call or barge in by dialing the
            extension.
        :type enable_phone_status_pickup_barge_in_privacy: str
        :param monitoring_agents: List of monitoring person IDs.
        :type monitoring_agents: list[str]
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if aa_extension_dialing_enabled is not None:
            body['aaExtensionDialingEnabled'] = aa_extension_dialing_enabled
        if aa_naming_dialing_enabled is not None:
            body['aaNamingDialingEnabled'] = aa_naming_dialing_enabled
        if enable_phone_status_directory_privacy is not None:
            body['enablePhoneStatusDirectoryPrivacy'] = enable_phone_status_directory_privacy
        if enable_phone_status_pickup_barge_in_privacy is not None:
            body['enablePhoneStatusPickupBargeInPrivacy'] = enable_phone_status_pickup_barge_in_privacy
        if monitoring_agents is not None:
            body['monitoringAgents'] = monitoring_agents
        url = self.ep(f'{person_id}/features/privacy')
        super().put(url, params=params, json=body)

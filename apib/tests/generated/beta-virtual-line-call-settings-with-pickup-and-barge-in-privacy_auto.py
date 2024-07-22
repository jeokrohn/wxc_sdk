from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaVirtualLineCallSettingsWithPickupAndBargeInPrivacyApi', 'MonitoredPersonObject',
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
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12341088
    esn: Optional[str] = None
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


class BetaVirtualLineCallSettingsWithPickupAndBargeInPrivacyApi(ApiChild, base='telephony/config/virtualLines'):
    """
    Beta Virtual Line Call Settings with Pickup and Barge In Privacy
    
    Virtual Line Settings supports listing Webex Calling virtual lines.
    
    The call pickup and barge-in privacy feature enables the admin to control people who can pick up the call or
    barge-in by dialing the extension.
    
    Viewing Virtual Lines requires a full, user, or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read.
    """

    def get_a_virtual_line_s_privacy_settings(self, virtual_line_id: str, org_id: str = None) -> PrivacyGet:
        """
        Get a Virtual Line's Privacy Settings

        Get a virtual line's privacy settings for the specified virtual line ID.

        The privacy feature enables the virtual line's line to be monitored by others and determine if they can be
        reached by Auto Attendant services.

        Retrieving the privacy settings for a virtual line requires a full, user, or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PrivacyGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/privacy')
        data = super().get(url, params=params)
        r = PrivacyGet.model_validate(data)
        return r

    def configure_a_virtual_line_s_privacy_settings(self, virtual_line_id: str,
                                                    aa_extension_dialing_enabled: str = None,
                                                    aa_naming_dialing_enabled: str = None,
                                                    enable_phone_status_directory_privacy: str = None,
                                                    enable_phone_status_pickup_barge_in_privacy: str = None,
                                                    monitoring_agents: list[str] = None, org_id: str = None):
        """
        Configure a Virtual Line's Privacy Settings

        Configure a virtual line's privacy settings for the specified virtual line ID.

        The privacy feature enables the virtual line's line to be monitored by others and determine if they can be
        reached by Auto Attendant services.

        Updating the privacy settings for a virtual line requires a full or user administrator auth token with a scope
        of `spark-admin:telephony_config_write`.

        :param virtual_line_id: Retrieve settings for a virtual line with the matching ID.
        :type virtual_line_id: str
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
        :param org_id: ID of the organization in which the virtual line resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
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
        url = self.ep(f'{virtual_line_id}/privacy')
        super().put(url, params=params, json=body)

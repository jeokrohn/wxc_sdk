from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaWorkspaceCallSettingsWithPickupAndBargeInPrivacyApi', 'MonitoredPersonObject',
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
    #: When `true` auto attendant extension dialing is enabled.
    #: example: True
    aa_extension_dialing_enabled: Optional[bool] = None
    #: When `true` auto attendant dialing by first or last name is enabled.
    #: example: True
    aa_naming_dialing_enabled: Optional[bool] = None
    #: When `true` phone status directory privacy is enabled.
    #: example: True
    enable_phone_status_directory_privacy: Optional[bool] = None
    #: When `true` privacy is enforced for call pickup and barge-in. Only people specified by `monitoringAgents` can
    #: pick up the call or barge in by dialing the extension.
    #: example: True
    enable_phone_status_pickup_barge_in_privacy: Optional[bool] = None
    #: List of people that are being monitored.
    monitoring_agents: Optional[list[MonitoredPersonObject]] = None


class BetaWorkspaceCallSettingsWithPickupAndBargeInPrivacyApi(ApiChild, base='telephony/config/workspaces'):
    """
    Beta Workspace Call Settings with Pickup and Barge In Privacy
    
    Workspaces represent places where people work, such as conference rooms, meeting spaces, lobbies, and lunchrooms.
    Devices may be associated with workspaces.
    
    Webex Calling Workspace Settings support reading and writing of Webex Calling settings for a specific workspace
    within the organization.
    
    The call pickup and barge-in privacy feature enables the admin to control people who can pick up the call or
    barge-in by dialing the extension.
    
    Viewing the list of settings in a workspace /v1/workspaces API requires a full, device, or read-only administrator
    auth token with the `spark-admin:workspaces_read` scope.
    
    Adding, updating, or deleting settings in a workspace /v1/workspaces API requires a full or device administrator
    auth token with the `spark-admin:workspaces_write` scope.
    
    This API can also be used by partner administrators acting as administrators of a different organization than their
    own. In those cases, an `orgId` must be supplied, as indicated in the reference documentation for the relevant
    endpoints.
    """

    def retrieve_privacy_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> PrivacyGet:
        """
        Retrieve Privacy Settings for a Workspace.

        The privacy feature enables the Workspaces line to be monitored by others and determine if they can be reached
        by Auto Attendant services.

        This API requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:workspaces_read` scope to read workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`PrivacyGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/privacy')
        data = super().get(url, params=params)
        r = PrivacyGet.model_validate(data)
        return r

    def modify_privacy_settings_for_a_workspace(self, workspace_id: str, aa_extension_dialing_enabled: bool = None,
                                                aa_naming_dialing_enabled: bool = None,
                                                enable_phone_status_directory_privacy: bool = None,
                                                enable_phone_status_pickup_barge_in_privacy: bool = None,
                                                monitoring_agents: list[str] = None, org_id: str = None):
        """
        Modify Privacy Settings for a Workspace.

        The privacy feature enables the Workspaces line to be monitored by others and determine if they can be reached
        by Auto Attendant services.

        This API requires a full, user or location administrator auth token with the `spark-admin:workspaces_write`
        scope to update workspace settings.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param aa_extension_dialing_enabled: When `true` auto attendant extension dialing is enabled.
        :type aa_extension_dialing_enabled: bool
        :param aa_naming_dialing_enabled: When `true` auto attendant dialing by first or last name is enabled.
        :type aa_naming_dialing_enabled: bool
        :param enable_phone_status_directory_privacy: When `true` phone status directory privacy is enabled.
        :type enable_phone_status_directory_privacy: bool
        :param enable_phone_status_pickup_barge_in_privacy: When `true` privacy is enforced for call pickup and
            barge-in. Only people specified by `monitoringAgents` can pick up the call or barge in by dialing the
            extension.
        :type enable_phone_status_pickup_barge_in_privacy: bool
        :param monitoring_agents: List of monitoring person IDs.
        :type monitoring_agents: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
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
        url = self.ep(f'{workspace_id}/privacy')
        super().put(url, params=params, json=body)

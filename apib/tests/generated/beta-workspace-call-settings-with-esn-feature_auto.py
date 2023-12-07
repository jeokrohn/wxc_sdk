from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['BetaWorkspaceCallSettingsWithESNFeatureApi', 'ListNumbersAssociatedWithASpecificWorkspaceResponse',
            'Location', 'MonitoredElementCallParkExtension', 'MonitoredElementItem', 'MonitoredElementUser',
            'MonitoredElementUserType', 'PhoneNumbers', 'UserMonitoringGet', 'UserNumberItem', 'Workspace']


class MonitoredElementCallParkExtension(ApiModel):
    #: ID of call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE2NmE
    id: Optional[str] = None
    #: Name of call park extension.
    #: example: CPE1
    name: Optional[str] = None
    #: Extension of call park extension.
    #: example: 8080
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12348080
    esn: Optional[str] = None
    #: Name of location for call park extension.
    #: example: Alaska
    location: Optional[str] = None
    #: ID of location for call park extension.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    location_id: Optional[str] = None


class MonitoredElementUserType(str, Enum):
    #: Object is a user.
    people = 'PEOPLE'
    #: Object is a workspace.
    place = 'PLACE'


class UserNumberItem(ApiModel):
    #: Phone number of person or workspace. Either `phoneNumber` or `extension` is mandatory.
    #: example: +19075552859
    external: Optional[str] = None
    #: Extension of person or workspace. Either `phoneNumber` or `extension` is mandatory.
    #: example: 8080
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 12348080
    esn: Optional[str] = None
    #: Flag to indicate primary phone.
    #: example: True
    primary: Optional[bool] = None
    #: Flag to indicate toll free number.
    #: example: True
    toll_free_number: Optional[bool] = None


class MonitoredElementUser(ApiModel):
    #: ID of person or workspace.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80NDVkMzMzMC1mNjE3LTExZWItOWQyZS01NzViODE3ZGE2NmE
    id: Optional[str] = None
    #: First name of person or workspace.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of person or workspace.
    #: example: Brown
    last_name: Optional[str] = None
    #: Display name of person or workspace.
    #: example: John Brown
    display_name: Optional[str] = None
    #: Type of the person or workspace.
    #: example: PEOPLE
    type: Optional[MonitoredElementUserType] = None
    #: Email of the person or workspace.
    #: example: john.brown@gmail.com
    email: Optional[str] = None
    #: List of phone numbers of the person or workspace.
    numbers: Optional[list[UserNumberItem]] = None
    #: Name of location for call park.
    #: example: Alaska
    location: Optional[str] = None
    #: ID of the location for call park.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzEyMzQ1
    location_id: Optional[str] = None


class MonitoredElementItem(ApiModel):
    #: Monitored Call Park extension.
    callparkextension: Optional[MonitoredElementCallParkExtension] = None
    #: Monitored member for this workspace.
    member: Optional[MonitoredElementUser] = None


class PhoneNumbers(ApiModel):
    #: PSTN phone number in E.164 format.
    #: example: +12055550001
    external: Optional[str] = None
    #: Extension for workspace.
    #: example: 123
    extension: Optional[str] = None
    #: Routing prefix of location.
    #: example: 1234
    routing_prefix: Optional[str] = None
    #: Routing prefix + extension of a person or workspace.
    #: example: 1234123
    esn: Optional[str] = None
    #: If `true`, the primary number.
    #: example: True
    primary: Optional[bool] = None


class UserMonitoringGet(ApiModel):
    #: Call park notification enabled or disabled.
    #: example: True
    call_park_notification_enabled: Optional[bool] = None
    #: Monitored element items.
    monitored_elements: Optional[MonitoredElementItem] = None


class Location(ApiModel):
    #: Location identifier associated with the workspace.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4Mjg5NzIyLTFiODAtNDFiNy05Njc4LTBlNzdhZThjMTA5OA
    id: Optional[str] = None
    #: Location name associated with the workspace.
    #: example: MainOffice
    name: Optional[str] = None


class Workspace(ApiModel):
    #: Workspace ID associated with the list of numbers.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMV9pbnQxMy9QTEFDRS8xNzdmNTNlZC1hNzY2LTRkYTAtOGQ3OC03MjE0MjhjMmFjZTQ=
    id: Optional[str] = None


class ListNumbersAssociatedWithASpecificWorkspaceResponse(ApiModel):
    #: Array of numbers (primary/alternate).
    phone_numbers: Optional[list[PhoneNumbers]] = None
    #: Workspace object having a unique identifier for the Workspace.
    workspace: Optional[Workspace] = None
    #: Location object having a unique identifier for the location and its name.
    location: Optional[Location] = None
    #: Organization object having a unique identifier for the organization and its name.
    organization: Optional[Location] = None


class BetaWorkspaceCallSettingsWithESNFeatureApi(ApiChild, base='workspaces/{workspaceId}/features'):
    """
    Beta Workspace Call Settings with ESN Feature
    
    Workspaces represent places where people work, such as conference rooms, meeting spaces, lobbies, and lunchrooms.
    Devices may be associated with workspaces.
    
    Webex Calling Workspace Settings support reading and writing of Webex Calling settings for a specific workspace
    within the organization.
    
    Viewing the list of settings in a workspace /v1/workspaces API requires an full, device, or read-only administrator
    auth token with the `spark-admin:workspaces_read` scope.
    
    Adding, updating, or deleting settings in a workspace /v1/workspaces API requires an full or device administrator
    auth token with the `spark-admin:workspaces_write` scope.
    
    This API can also be used by partner administrators acting as administrators of a different organization than their
    own. In those cases, an `orgId` must be supplied, as indicated in the reference documentation for the relevant
    endpoints.
    """

    def retrieve_monitoring_settings_for_a_workspace(self, workspace_id: str, org_id: str = None) -> UserMonitoringGet:
        """
        Retrieve Monitoring Settings for a Workspace

        Retrieves Monitoring settings for a Workspace.

        Allow workspaces to monitor the line status of specified agents, workspaces, or call park extensions. The line
        status indicates if a monitored agent or a workspace is on a call, or if a call has been parked on the
        monitored call park extension.

        This API requires a full or read-only administrator auth token with a scope of `spark-admin:workspaces_read` or
        a user auth token with `spark:workspaces_read` scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: :class:`UserMonitoringGet`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'monitoring')
        data = super().get(url, params=params)
        r = UserMonitoringGet.model_validate(data)
        return r

    def list_numbers_associated_with_a_specific_workspace(self, workspace_id: str,
                                                          org_id: str = None) -> ListNumbersAssociatedWithASpecificWorkspaceResponse:
        """
        List numbers associated with a specific workspace

        List the PSTN phone numbers associated with a specific workspace, by ID, within the organization. Also shows
        the location and organization associated with the workspace.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:workspaces_read`.

        :param workspace_id: List numbers for this workspace.
        :type workspace_id: str
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            can use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :rtype: :class:`ListNumbersAssociatedWithASpecificWorkspaceResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'numbers')
        data = super().get(url, params=params)
        r = ListNumbersAssociatedWithASpecificWorkspaceResponse.model_validate(data)
        return r

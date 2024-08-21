from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaWorkspaceCallSettingsWithEmergencyServicesApi', 'CallBackEffectiveLevel', 'CallBackMemberType',
           'CallBackQuality', 'CallBackSelected', 'CallBackSelectedPatch', 'ECBNLocationEffectiveLevel',
           'GetWorkspaceCallbackNumberDependenciesObject', 'GetWorkspaceCallbackNumberObject',
           'GetWorkspaceCallbackNumberObjectDefaultInfo', 'GetWorkspaceCallbackNumberObjectDirectLineInfo',
           'GetWorkspaceCallbackNumberObjectLocationMemberInfo']


class CallBackSelected(str, Enum):
    #: Returned calls from the Public Safety Answering Point go directly to the member. The Emergency Service Address
    #: configured by the PSTN to the member's phone is specific to the member’s location.
    direct_line = 'DIRECT_LINE'
    #: Each location can have an ECBN configured that is different from the location’s main number. Location Default
    #: ECBN is typically configured for users without dedicated telephone numbers or with only an extension.
    location_ecbn = 'LOCATION_ECBN'
    #: This lets you configure one user with another user’s telephone number as an ECBN. This option is used in place
    #: of a location’s main number when the location has multiple floors or buildings. This allows the ECBN assigned
    #: to have a more accurate Emergency Service Address associated with it.
    location_member_number = 'LOCATION_MEMBER_NUMBER'
    #: When no other option is selected.
    none_ = 'NONE'


class CallBackMemberType(str, Enum):
    #: Indicates the associated member is a person.
    people = 'PEOPLE'
    #: Indicates the associated member is a workspace.
    place = 'PLACE'
    #: Indicates the associated member is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class CallBackEffectiveLevel(str, Enum):
    #: Returned calls from the Public Safety Answering Point go directly to the member. The Emergency Service Address
    #: configured by the PSTN to the member's phone is specific to the member’s location.
    direct_line = 'DIRECT_LINE'
    #: Each location can have an ECBN configured that is different from the location’s main number. Location Default
    #: ECBN is typically configured for users without dedicated telephone numbers or with only an extension.
    location_ecbn = 'LOCATION_ECBN'
    #: A location’s main number that is suitable for when the location has a single building with a single floor.
    location_number = 'LOCATION_NUMBER'
    #: When no other option is selected.
    none_ = 'NONE'


class ECBNLocationEffectiveLevel(str, Enum):
    #: Returned calls from the Public Safety Answering Point go directly to the member. The Emergency Service Address
    #: configured by the PSTN to the member's phone is specific to the member’s location.
    direct_line = 'DIRECT_LINE'
    #: Each location can have an ECBN configured that is different from the location’s main number. Location Default
    #: ECBN is typically configured for users without dedicated telephone numbers or with only an extension.
    location_ecbn = 'LOCATION_ECBN'
    #: A location’s main number that is suitable for when the location has a single building with a single floor.
    location_number = 'LOCATION_NUMBER'
    #: This lets you configure one user with another user’s telephone number as an ECBN. This option is used in place
    #: of a location’s main number when the location has multiple floors or buildings. This allows the ECBN assigned
    #: to have a more accurate Emergency Service Address associated with it.
    location_member_number = 'LOCATION_MEMBER_NUMBER'
    #: When no other option is selected.
    none_ = 'NONE'


class CallBackQuality(str, Enum):
    #: The emergency callback number is assigned to a user or workspace or virtual line.
    recommended = 'RECOMMENDED'
    #: The emergency callback number is assigned to something that may not be an attended destination.
    not_recommended = 'NOT_RECOMMENDED'
    #: The emergency callback number is a number where call backs would never work, i.e., no available caller ID.
    invalid = 'INVALID'


class CallBackSelectedPatch(str, Enum):
    #: Returned calls from the Public Safety Answering Point go directly to the member. The Emergency Service Address
    #: configured by the PSTN to the member's phone is specific to the member’s location.
    direct_line = 'DIRECT_LINE'
    #: Each location can have an ECBN configured that is different from the location’s main number. Location Default
    #: ECBN is typically configured for users without dedicated telephone numbers or with only an extension.
    location_ecbn = 'LOCATION_ECBN'
    #: This lets you configure one user with another user’s telephone number as an ECBN. This option is used in place
    #: of a location’s main number when the location has multiple floors or buildings. This allows the ECBN assigned
    #: to have a more accurate Emergency Service Address associated with it.
    location_member_number = 'LOCATION_MEMBER_NUMBER'


class GetWorkspaceCallbackNumberObjectDirectLineInfo(ApiModel):
    #: The callback phone number that is associated with the direct line.
    #: example: 18164196065
    phone_number: Optional[str] = None
    #: First name of a user.
    #: example: backUpworkspace
    first_name: Optional[str] = None
    #: Last name of a user.
    #: example: .
    last_name: Optional[str] = None
    #: The source from which the emergency calling line ID (CLID) is selected for an actual emergency call, applying
    #: fallback rules as necessary.
    #: example: DIRECT_LINE
    effective_level: Optional[CallBackEffectiveLevel] = None
    #: The field contains the valid ECBN number at the location level, or the user's main number if valid, defaulting
    #: to the location's main number if both are unavailable.
    #: example: 18164196065
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    #: example: RECOMMENDED
    quality: Optional[CallBackQuality] = None


class GetWorkspaceCallbackNumberObjectLocationMemberInfo(ApiModel):
    #: The callback phone number that is associated with member configured for the location ECBN.
    #: example: 18164196065
    phone_number: Optional[str] = None
    #: First name of a user.
    #: example: backUpworkspace
    first_name: Optional[str] = None
    #: Last name of the user or location member or `.`.
    #: example: .
    last_name: Optional[str] = None
    #: Member ID of user/place/virtual line within the location.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMV9pbnQxMy9QTEFDRS8wY2VlYjFmYy04ZmEyLTQ5OGEtYWM3Ni02N2MyZGQ3MGQ2ZGY=
    member_id: Optional[str] = None
    #: The source from which the emergency calling line ID (CLID) is selected for an actual emergency call, applying
    #: fallback rules as necessary.
    #: example: LOCATION_MEMBER_NUMBER
    effective_level: Optional[ECBNLocationEffectiveLevel] = None
    #: The field contains the valid ECBN number at the location level, or the user's main number if valid, defaulting
    #: to the location's main number if both are unavailable.
    #: example: 18164196065
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    #: example: RECOMMENDED
    quality: Optional[CallBackQuality] = None
    #: Indicates the type of the member.
    #: example: PLACE
    member_type: Optional[CallBackMemberType] = None


class GetWorkspaceCallbackNumberObjectDefaultInfo(ApiModel):
    #: The field contains the ECBN number.
    #: example: 18164196068
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    #: example: RECOMMENDED
    quality: Optional[CallBackQuality] = None


class GetWorkspaceCallbackNumberObject(ApiModel):
    #: Selected number type to configure emergency call back.
    #: example: DIRECT_LINE
    selected: Optional[CallBackSelected] = None
    #: Data relevant to the ECBN for this user/location/virtual line.
    direct_line_info: Optional[GetWorkspaceCallbackNumberObjectDirectLineInfo] = None
    #: Data relevant to the user/place/virtual line selected for ECBN for this location.
    location_ecbninfo: Optional[GetWorkspaceCallbackNumberObjectDirectLineInfo] = Field(alias='locationECBNInfo', default=None)
    #: Data relevant to the user/place/virtual line selected for ECBN.
    location_member_info: Optional[GetWorkspaceCallbackNumberObjectLocationMemberInfo] = None
    #: Gives Emergency Callback Number effective value when none of the above is assigned or some other value is set
    #: behind the scene.
    default_info: Optional[GetWorkspaceCallbackNumberObjectDefaultInfo] = None


class GetWorkspaceCallbackNumberDependenciesObject(ApiModel):
    #: When `isLocationEcbnDefault` is true, then it is the default emergency callback number for the location.
    #: example: True
    is_location_ecbn_default: Optional[bool] = None
    #: Default emergency call-back number of the place if `true`.
    is_self_ecbn_default: Optional[bool] = None
    #: Number of members using this workspace as their emergency callback number.
    dependent_member_count: Optional[int] = None


class BetaWorkspaceCallSettingsWithEmergencyServicesApi(ApiChild, base='telephony/config/workspaces'):
    """
    Beta Workspace Call Settings with Emergency Services
    
    Emergency Call back Configurations can be enabled at the organization level, Users without individual telephone
    numbers, such as extension-only users, must be set up with accurate Emergency Call Back Numbers (ECBN) to enable
    them to make emergency calls. These users can either utilize the default ECBN for their location or be assigned
    another specific telephone number from that location for emergency purposes.
    
    Viewing these organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`. Modifying these organization settings requires a full administrator auth
    token with a scope of `spark-admin:telephony_config_write`.
    """

    def get_a_workspace_emergency_callback_number(self, workspace_id: str,
                                                  org_id: str = None) -> GetWorkspaceCallbackNumberObject:
        """
        Get a Workspace Emergency Callback Number

        Retrieve the emergency callback number setting associated with a specific workspace.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Callback Numbers (ECBN) and
        Emergency Service Addresses to enable them to make emergency calls. These users can either utilize the default
        ECBN for their location or be assigned another specific telephone number from that location for emergency
        purposes.

        To retrieve an emergency callback number, it requires a full, location, user, or read-only administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param workspace_id: Retrieve Emergency Callback Number attributes for this workspace.
        :type workspace_id: str
        :param org_id: Retrieve Emergency Callback Number attributes for this organization.
        :type org_id: str
        :rtype: :class:`GetWorkspaceCallbackNumberObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/emergencyCallbackNumber')
        data = super().get(url, params=params)
        r = GetWorkspaceCallbackNumberObject.model_validate(data)
        return r

    def update_a_workspace_emergency_callback_number(self, workspace_id: str, selected: CallBackSelectedPatch,
                                                     location_member_id: str, org_id: str = None):
        """
        Update a Workspace Emergency Callback Number

        Update the emergency callback number settings for a workspace.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Call Back Numbers (ECBN) to
        enable them to make emergency calls. These users can either utilize the default ECBN for their location or be
        assigned another specific telephone number from that location for emergency purposes.

        To update an emergency callback number requires a full, location, user, or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param workspace_id: Updating Emergency Callback Number attributes for this workspace.
        :type workspace_id: str
        :param selected: Assigned number of the user or workspace in the location.
        :type selected: CallBackSelectedPatch
        :param location_member_id: Member ID of user/place/virtual line within the location. Required if
            `LOCATION_MEMBER_NUMBER` is selected.
        :type location_member_id: str
        :param org_id: Updating Emergency Callback Number attributes for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['selected'] = enum_str(selected)
        body['locationMemberId'] = location_member_id
        url = self.ep(f'{workspace_id}/emergencyCallbackNumber')
        super().put(url, params=params, json=body)

    def retrieve_workspace_emergency_callback_number_dependencies(self, workspace_id: str,
                                                                  org_id: str = None) -> GetWorkspaceCallbackNumberDependenciesObject:
        """
        Retrieve Workspace Emergency Callback Number Dependencies

        Retrieve Emergency Callback Number dependencies for a workspace.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Call Back Numbers (ECBN) to
        enable them to make emergency calls. These users can either utilize the default ECBN for their location or be
        assigned another specific telephone number from that location for emergency purposes.

        Retrieving the dependencies requires a full, user or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param workspace_id: Retrieve Emergency Callback Number attributes for this workspace.
        :type workspace_id: str
        :param org_id: Retrieve Emergency Callback Number attributes for this organization.
        :type org_id: str
        :rtype: :class:`GetWorkspaceCallbackNumberDependenciesObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/emergencyCallbackNumber/dependencies')
        data = super().get(url, params=params)
        r = GetWorkspaceCallbackNumberDependenciesObject.model_validate(data)
        return r

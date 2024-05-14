from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaVirtualLineCallSettingsWithEmergencySettingsApi', 'ECBNDirectLineEffectiveLevelType',
           'ECBNQualityType', 'ECBNSelectionType', 'LocationMemberInfoEffectiveLevelType', 'MemberType',
           'VirtualLinesECBNDependenciesObject', 'VirtualLinesECBNObject', 'VirtualLinesECBNObjectDefaultInfo',
           'VirtualLinesECBNObjectDirectLineInfo', 'VirtualLinesECBNObjectLocationMemberInfo']


class VirtualLinesECBNDependenciesObject(ApiModel):
    #: `true` if it is the default emergency call-back number for the location.
    #: example: True
    is_location_ecbn_default: Optional[bool] = None
    #: Default emergency call-back number for the virtual line if `true`.
    #: example: True
    is_self_ecbn_default: Optional[bool] = None
    #: Number of members using this virtual line as their emergency call-back number.
    #: example: 15
    dependent_member_count: Optional[int] = None


class ECBNSelectionType(str, Enum):
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
    none_ = 'None'


class ECBNDirectLineEffectiveLevelType(str, Enum):
    #: Returned calls from the Public Safety Answering Point go directly to the member. The Emergency Service Address
    #: configured by the PSTN to the member's phone is specific to the member’s location.
    direct_line = 'DIRECT_LINE'
    #: Each location can have an ECBN configured that is different from the location’s main number. Location Default
    #: ECBN is typically configured for users without dedicated telephone numbers or with only an extension.
    location_ecbn = 'LOCATION_ECBN'
    #: A location’s main number that is suitable for when the location has a single building with a single floor.
    location_number = 'LOCATION_NUMBER'
    #: There is no effective level type selected.
    none_ = 'None'


class LocationMemberInfoEffectiveLevelType(str, Enum):
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
    none_ = 'None'


class ECBNQualityType(str, Enum):
    #: The emergency callback number is assigned to a user or workspace or virtual line.
    recommended = 'RECOMMENDED'
    #: The emergency callback number is assigned to something that may not be an attended destination.
    not_recommended = 'NOT_RECOMMENDED'
    #: The emergency callback number is a number where callbacks would never work, i.e., no available caller ID.
    invalid = 'INVALID'


class MemberType(str, Enum):
    #: Indicates the associated member is a person.
    people = 'PEOPLE'
    #: Indicates the associated member is a workspace.
    place = 'PLACE'
    #: Indicates the associated member is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class VirtualLinesECBNObjectDirectLineInfo(ApiModel):
    #: The callback phone number that is associated with the direct line.
    #: example: 2056350001
    phone_number: Optional[str] = None
    #: First name of a user.
    #: example: John
    first_name: Optional[str] = None
    #: Last name of a user.
    #: example: Smith
    last_name: Optional[str] = None
    #: The source from which the emergency calling line ID (CLID) is selected for an actual emergency call, applying
    #: fallback rules as necessary.
    #: example: DIRECT_LINE
    effective_level: Optional[ECBNDirectLineEffectiveLevelType] = None
    #: The field contains the valid ECBN number at the location level, or the user's main number if valid, defaulting
    #: to the location's main number if both are unavailable.
    #: example: 9726856770
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    #: example: RECOMMENDED
    quality: Optional[ECBNQualityType] = None


class VirtualLinesECBNObjectLocationMemberInfo(ApiModel):
    #: A unique identifier for the location member's PSTN phone number.
    #: example: 9726856700
    phone_number: Optional[str] = None
    #: First name for the location member.
    #: example: James
    first_name: Optional[str] = None
    #: Last name for the location member. This field will always return "." when `effectiveLevel` is `DIRECT_LINE` or
    #: `LOCATION_MEMBER_NUMBER`, and the selected member is a place.
    #: example: Johnson
    last_name: Optional[str] = None
    #: Member ID of user/place/virtual line within the location.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS82MmQ3YTY3MS00YmVlLTQ2MDItOGVkOC1jOTFmNjU5NjcxZGI
    member_id: Optional[str] = None
    #: The source from which the emergency calling line ID (CLID) is selected for an actual emergency call, applying
    #: fallback rules as necessary.
    #: example: LOCATION_NUMBER
    effective_level: Optional[LocationMemberInfoEffectiveLevelType] = None
    #: Contains the location-level emergency callback number if valid. If not, contains the user's main number if
    #: valid.
    #: example: 9726856770
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    #: example: RECOMMENDED
    quality: Optional[ECBNQualityType] = None
    #: Indicates the type of the member.
    #: example: VIRTUAL_LINE
    member_type: Optional[MemberType] = None


class VirtualLinesECBNObjectDefaultInfo(ApiModel):
    #: The field contains ECBN number.
    #: example: 9726856770
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    #: example: RECOMMENDED
    quality: Optional[ECBNQualityType] = None


class VirtualLinesECBNObject(ApiModel):
    #: Selected number type to configure emergency call back.
    #: example: DIRECT_LINE
    selected: Optional[ECBNSelectionType] = None
    #: Data relevant to the ECBN for this user/location/virtual line.
    direct_line_info: Optional[VirtualLinesECBNObjectDirectLineInfo] = None
    #: Data relevant to the user/place/virtual line selected for ECBN for this location.
    location_ecbninfo: Optional[VirtualLinesECBNObjectDirectLineInfo] = Field(alias='locationECBNInfo', default=None)
    location_member_info: Optional[VirtualLinesECBNObjectLocationMemberInfo] = None
    #: Contains the Emergency Callback Number effective value when none of the above parameters are assigned or some
    #: other value is set.
    default_info: Optional[VirtualLinesECBNObjectDefaultInfo] = None


class BetaVirtualLineCallSettingsWithEmergencySettingsApi(ApiChild, base='telephony/config/virtualLines'):
    """
    Beta Virtual Line Call Settings with Emergency Settings
    
    A virtual line allows administrators to configure multiple lines for Webex Calling users. Virtual line settings
    support reading the dependencies for a given virtual line ID.
    
    Viewing these read-only settings requires a full, user, or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    """

    def get_dependencies_for_a_virtual_line_emergency_call_back_number(self, virtual_line_id: str,
                                                                       org_id: str = None) -> VirtualLinesECBNDependenciesObject:
        """
        Get Dependencies for a Virtual Line Emergency Call-Back Number

        Retrieves the emergency callback number dependencies for a specific virtual line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines for Webex
        Calling users.

        Retrieving the dependencies requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: List virtual lines for this organization.
        :type org_id: str
        :rtype: :class:`VirtualLinesECBNDependenciesObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/emergencyCallbackNumber/dependencies')
        data = super().get(url, params=params)
        r = VirtualLinesECBNDependenciesObject.model_validate(data)
        return r

    def get_the_virtual_line_s_emergency_call_back_settings(self, virtual_line_id: str,
                                                            org_id: str = None) -> VirtualLinesECBNObject:
        """
        Get the virtual Line's Emergency Call-back settings

        Retrieves the emergency callback number settings for a specific virtual line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines for Webex
        Calling users.

        Retrieving the dependencies requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param org_id: List virtual lines for this organization.
        :type org_id: str
        :rtype: :class:`VirtualLinesECBNObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{virtual_line_id}/emergencyCallbackNumber')
        data = super().get(url, params=params)
        r = VirtualLinesECBNObject.model_validate(data)
        return r

    def update_a_virtual_line_s_emergency_callback_settings(self, virtual_line_id: str, selected: ECBNSelectionType,
                                                            location_member_id: str, org_id: str = None):
        """
        Update a virtual Line's Emergency Callback settings

        Update the emergency callback number settings for a specific virtual line.

        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines for Webex
        Calling users.

        To update virtual line callback number requires a full or user administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param virtual_line_id: Unique identifier for the virtual line.
        :type virtual_line_id: str
        :param selected: The source from which the emergency calling line ID (CLID) is selected for an actual emergency
            call.
        :type selected: ECBNSelectionType
        :param location_member_id: Member ID of the user/place/virtual line within the location. Required if
            `LOCATION_MEMBER_NUMBER` is selected.
        :type location_member_id: str
        :param org_id: List virtual lines for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['selected'] = enum_str(selected)
        body['locationMemberId'] = location_member_id
        url = self.ep(f'{virtual_line_id}/emergencyCallbackNumber')
        super().put(url, params=params, json=body)

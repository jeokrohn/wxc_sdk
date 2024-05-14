from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaUserCallSettingsWithEmergencyServicesApi', 'CallBackMemberType', 'EmergencyCallBackNumberQuality',
           'GetPersonCallbackNumberDependenciesObject', 'GetPersonCallbackNumberObject',
           'GetPersonCallbackNumberObjectDefaultInfo', 'GetPersonCallbackNumberObjectDirectLineInfo',
           'GetPersonCallbackNumberObjectLocationMemberInfo', 'UserPlaceDirectLineGroupECBNEffectiveLevel',
           'UserPlaceECBNSelection', 'UserPlaceEmergencyCallBackNumberSelectionPatch',
           'UserPlaceLocationMemberInfoEffectiveLevel']


class UserPlaceDirectLineGroupECBNEffectiveLevel(str, Enum):
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


class EmergencyCallBackNumberQuality(str, Enum):
    #: Active number assigned to a user or workspace or virtual line.
    recommended = 'RECOMMENDED'
    #: Active number assigned to something that may not be an attended destination.
    not_recommended = 'NOT_RECOMMENDED'
    #: A number for which callbacks will not work, for instance, one without a valid caller ID.
    invalid = 'INVALID'


class GetPersonCallbackNumberObjectDirectLineInfo(ApiModel):
    #: The callback phone number that is associated with the direct line.
    #: example: 18164196065
    phone_number: Optional[str] = None
    #: First name of the user.
    #: example: User1
    first_name: Optional[str] = None
    #: Last name of the user.
    #: example: User1LastName
    last_name: Optional[str] = None
    #: The source from which the emergency calling line ID (CLID) is selected for an actual emergency call, applying
    #: fallback rules as necessary.
    #: example: DIRECT_LINE
    effective_level: Optional[UserPlaceDirectLineGroupECBNEffectiveLevel] = None
    #: The field contains the valid ECBN number at the location level, or the user's main number if valid, defaulting
    #: to the location's main number if both are unavailable.
    #: example: 18164196065
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    #: example: RECOMMENDED
    quality: Optional[EmergencyCallBackNumberQuality] = None


class CallBackMemberType(str, Enum):
    #: Indicates the associated member is a person.
    people = 'PEOPLE'
    #: Indicates the associated member is a workspace.
    place = 'PLACE'
    #: Indicates the associated member is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class UserPlaceLocationMemberInfoEffectiveLevel(str, Enum):
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


class GetPersonCallbackNumberObjectLocationMemberInfo(ApiModel):
    #: The callback phone number that is associated with member configured for the location ECBN.
    #: example: 18164196067
    phone_number: Optional[str] = None
    #: First name of the user.
    #: example: workspace1
    first_name: Optional[str] = None
    #: Last name of the user or `.`.
    #: example: .
    last_name: Optional[str] = None
    #: Member ID of user/place/virtual line within the location
    #: example: Y2lzY29zcGFyazovL3VzL1BMQUNFLzExYTNmOTkwLWE2ODktNDc3ZC1iZTZiLTcxMjAwMjVkOGFiYg
    member_id: Optional[str] = None
    #: Indicates the type of the member.
    #: example: PLACE
    member_type: Optional[CallBackMemberType] = None
    #: The source from which the emergency calling line ID (CLID) is selected for an actual emergency call, applying
    #: fallback rules as necessary.
    #: example: LOCATION_MEMBER_NUMBER
    effective_level: Optional[UserPlaceLocationMemberInfoEffectiveLevel] = None
    #: The field contains the valid ECBN number at the location level, or the user's main number if valid, defaulting
    #: to the location's main number if both are unavailable.
    #: example: 18164196067
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    #: example: RECOMMENDED
    quality: Optional[EmergencyCallBackNumberQuality] = None


class GetPersonCallbackNumberObjectDefaultInfo(ApiModel):
    #: The field contains the ECBN number.
    #: example: 18164196068
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    #: example: RECOMMENDED
    quality: Optional[EmergencyCallBackNumberQuality] = None


class UserPlaceECBNSelection(str, Enum):
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


class GetPersonCallbackNumberObject(ApiModel):
    #: Selected number type to configure emergency callback.
    #: example: DIRECT_LINE
    selected: Optional[UserPlaceECBNSelection] = None
    #: Data relevant to the ECBN for this user/location/virtual line.
    direct_line_info: Optional[GetPersonCallbackNumberObjectDirectLineInfo] = None
    #: Data relevant to the ECBN for this user/location/virtual line.
    location_ecbninfo: Optional[GetPersonCallbackNumberObjectDirectLineInfo] = Field(alias='locationECBNInfo', default=None)
    #: Data relevant to the ECBN for this user/location/virtual line.
    location_member_info: Optional[GetPersonCallbackNumberObjectLocationMemberInfo] = None
    #: Gives Emergency Callback Number effective value when none of the above is assigned or some other value is set
    #: behind the scene.
    default_info: Optional[GetPersonCallbackNumberObjectDefaultInfo] = None


class UserPlaceEmergencyCallBackNumberSelectionPatch(str, Enum):
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


class GetPersonCallbackNumberDependenciesObject(ApiModel):
    #: The default emergency callback number for the location when `isLocationEcbnDefault` is true.
    #: example: True
    is_location_ecbn_default: Optional[bool] = None
    #: The default emergency callback number for the person when `isSelfEcbnDefault` is true.
    is_self_ecbn_default: Optional[bool] = None
    #: Number of members using this person as their emergency callback number.
    dependent_member_count: Optional[int] = None


class BetaUserCallSettingsWithEmergencyServicesApi(ApiChild, base='telephony/config/people'):
    """
    Beta User Call Settings with Emergency Services
    
    Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
    numbers, such as extension-only users, must be set up with accurate Emergency Callback Numbers (ECBN) to enable
    them to make emergency calls. These users can either utilize the default ECBN for their location or be assigned
    another specific telephone number from that location for emergency purposes.
    
    Viewing these settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`. Modifying these settings requires a full administrator auth token with a
    scope of `spark-admin:telephony_config_write`.
    """

    def get_a_person_s_emergency_callback_number(self, person_id: str,
                                                 org_id: str = None) -> GetPersonCallbackNumberObject:
        """
        Get a Person's Emergency Callback Number

        Retrieve a person's emergency callback number settings.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Callback Numbers (ECBN) and
        Emergency Service Addresses to enable them to make emergency calls. These users can either utilize the default
        ECBN for their location or be assigned another specific telephone number from that location for emergency
        purposes.

        To retrieve a person's callback number requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: ID of the organization within which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`GetPersonCallbackNumberObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/emergencyCallbackNumber')
        data = super().get(url, params=params)
        r = GetPersonCallbackNumberObject.model_validate(data)
        return r

    def update_a_person_s_emergency_callback_number(self, person_id: str,
                                                    selected: UserPlaceEmergencyCallBackNumberSelectionPatch,
                                                    location_member_id: str, org_id: str = None):
        """
        Update a Person's Emergency Callback Number

        Update a person's emergency callback number settings.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Callback Numbers (ECBN) to
        enable them to make emergency calls. These users can either utilize the default ECBN for their location or be
        assigned another specific telephone number from that location for emergency purposes.

        To update an emergency callback number requires a full, location, user, or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param selected: The source from which the emergency calling line ID (CLID) is selected for an actual emergency
            call.
        :type selected: UserPlaceEmergencyCallBackNumberSelectionPatch
        :param location_member_id: Member ID of person/workspace/virtual line within the location.
        :type location_member_id: str
        :param org_id: ID of the organization within which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['selected'] = enum_str(selected)
        body['locationMemberId'] = location_member_id
        url = self.ep(f'{person_id}/emergencyCallbackNumber')
        super().put(url, params=params, json=body)

    def retrieve_a_person_s_emergency_callback_number_dependencies(self, person_id: str,
                                                                   org_id: str = None) -> GetPersonCallbackNumberDependenciesObject:
        """
        Retrieve A Person's Emergency Callback Number Dependencies

        Retrieve Emergency Callback Number dependencies for a person.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Call Back Numbers (ECBN) to
        enable them to make emergency calls. These users can either utilize the default ECBN for their location or be
        assigned another specific telephone number from that location for emergency purposes.

        Retrieving the dependencies requires a full, user or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Retrieve Emergency Callback Number attributes for this organization.
        :type org_id: str
        :rtype: :class:`GetPersonCallbackNumberDependenciesObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{person_id}/emergencyCallbackNumber/dependencies')
        data = super().get(url, params=params)
        r = GetPersonCallbackNumberDependenciesObject.model_validate(data)
        return r

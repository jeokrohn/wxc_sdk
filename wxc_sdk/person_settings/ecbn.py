from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum

__all__ = ['ECBNApi', 'ECBNQuality',
           'ECBNDependencies', 'PersonECBN',
           'ECBNDefault', 'PersonECBNDirectLine',
           'ECBNLocationMember', 'ECBNEffectiveLevel',
           'ECBNSelection', 'SelectedECBN',
           'ECBNLocationEffectiveLevel']

from wxc_sdk.common import UserType

from wxc_sdk.person_settings.common import PersonSettingsApiChild


class ECBNEffectiveLevel(str, Enum):
    #: Returned calls from the Public Safety Answering Point go directly to the member. The Emergency Service Address
    #: configured by the PSTN to the member's phone is specific to the member’s location.
    direct_line = 'DIRECT_LINE'
    #: Each location can have an ECBN configured that is different from the location’s main number. Location Default
    #: ECBN is typically configured for users without dedicated telephone numbers or with only an extension.
    location_ecbn = 'LOCATION_ECBN'
    #: A location’s main number that is suitable for when the location has a single building with a single floor.
    location_number = 'LOCATION_NUMBER'
    #: Assigned number of a user or workspace in the location.
    location_member_number = 'LOCATION_MEMBER_NUMBER'
    #: When no other option is selected.
    none_ = 'NONE'


class ECBNQuality(str, Enum):
    #: Active number assigned to a user or workspace or virtual line.
    recommended = 'RECOMMENDED'
    #: Active number assigned to something that may not be an attended destination.
    not_recommended = 'NOT_RECOMMENDED'
    #: A number for which callbacks will not work, for instance, one without a valid caller ID.
    invalid = 'INVALID'


class PersonECBNDirectLine(ApiModel):
    #: The callback phone number that is associated with the direct line.
    phone_number: Optional[str] = None
    #: First name of the user.
    first_name: Optional[str] = None
    #: Last name of the user.
    last_name: Optional[str] = None
    #: The source from which the emergency calling line ID (CLID) is selected for an actual emergency call, applying
    #: fallback rules as necessary.
    effective_level: Optional[ECBNEffectiveLevel] = None
    #: The field contains the valid ECBN number at the location level, or the user's main number if valid, defaulting
    #: to the location's main number if both are unavailable.
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    quality: Optional[ECBNQuality] = None


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


class ECBNLocationMember(ApiModel):
    #: The callback phone number that is associated with member configured for the location ECBN.
    phone_number: Optional[str] = None
    #: First name of the user.
    first_name: Optional[str] = None
    #: Last name of the user or `.`.
    last_name: Optional[str] = None
    #: Member ID of user/place/virtual line within the location
    member_id: Optional[str] = None
    #: Indicates the type of the member.
    member_type: Optional[UserType] = None
    #: The source from which the emergency calling line ID (CLID) is selected for an actual emergency call, applying
    #: fallback rules as necessary.
    effective_level: Optional[ECBNLocationEffectiveLevel] = None
    #: The field contains the valid ECBN number at the location level, or the user's main number if valid, defaulting
    #: to the location's main number if both are unavailable.
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    quality: Optional[ECBNQuality] = None


class ECBNDefault(ApiModel):
    #: The field contains the ECBN number.
    effective_value: Optional[str] = None
    #: Used to represent whether a number is a recommended ECBN.
    quality: Optional[ECBNQuality] = None


class ECBNSelection(str, Enum):
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


class PersonECBN(ApiModel):
    #: Selected number type to configure emergency callback.
    selected: Optional[ECBNSelection] = None
    #: Data relevant to the ECBN for this user/location/virtual line.
    direct_line_info: Optional[PersonECBNDirectLine] = None
    #: Data relevant to the ECBN for this user/location/virtual line.
    location_ecbn_info: Optional[PersonECBNDirectLine] = Field(alias='locationECBNInfo',
                                                               default=None)
    #: Data relevant to the ECBN for this user/location/virtual line.
    location_member_info: Optional[ECBNLocationMember] = None
    #: Gives Emergency Callback Number effective value when none of the above is assigned or some other value is set
    #: behind the scene.
    default_info: Optional[ECBNDefault] = None


class SelectedECBN(str, Enum):
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


class ECBNDependencies(ApiModel):
    #: The default emergency callback number for the location when `isLocationEcbnDefault` is true.
    is_location_ecbn_default: Optional[bool] = None
    #: The default emergency callback number for the person when `isSelfEcbnDefault` is true.
    is_self_ecbn_default: Optional[bool] = None
    #: Number of members using this person as their emergency callback number.
    dependent_member_count: Optional[int] = None


class ECBNApi(PersonSettingsApiChild):
    """
    Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
    numbers, such as extension-only users, must be set up with accurate Emergency Callback Numbers (ECBN) to enable
    them to make emergency calls. These users can either utilize the default ECBN for their location or be assigned
    another specific telephone number from that location for emergency purposes.

    Viewing these settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`. Modifying these settings requires a full administrator auth token with a
    scope of `spark-admin:telephony_config_write`.
    """

    feature = 'emergencyCallbackNumber'

    def read(self, entity_id: str,
             org_id: str = None) -> PersonECBN:
        """
        Get an entity's Emergency Callback Number

        Retrieve an entity's emergency callback number settings. Also applies to workspaces and virtual lines.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Callback Numbers (ECBN) and
        Emergency Service Addresses to enable them to make emergency calls. These users can either utilize the default
        ECBN for their location or be assigned another specific telephone number from that location for emergency
        purposes.

        To retrieve an entity's callback number requires a full, user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for the entity, virtual line, or workspace
        :type entity_id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:`PersonECBN`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id)
        data = super().get(url, params=params)
        r = PersonECBN.model_validate(data)
        return r

    def configure(self, entity_id: str,
                  selected: SelectedECBN,
                  location_member_id: str = None, org_id: str = None):
        """
        Update an entity's Emergency Callback Number.

        Update an entity's emergency callback number settings. Also applies to workspaces and virtual lines.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Callback Numbers (ECBN) to
        enable them to make emergency calls. These users can either utilize the default ECBN for their location or be
        assigned another specific telephone number from that location for emergency purposes.

        To update an emergency callback number requires a full, location, user, or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_write`.

        :param entity_id: Unique identifier for the entity, virtual line, or workspace.
        :type entity_id: str
        :param selected: The source from which the emergency calling line ID (CLID) is selected for an actual emergency
            call.
        :type selected: SelectedECBN
        :param location_member_id: Member ID of person/workspace/virtual line within the location.
        :type location_member_id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another organization
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
        if location_member_id is not None:
            body['locationMemberId'] = location_member_id
        url = self.f_ep(entity_id)
        super().put(url, params=params, json=body)

    def dependencies(self, entity_id: str,
                     org_id: str = None) -> ECBNDependencies:
        """
        Retrieve an entity's Emergency Callback Number Dependencies

        Retrieve Emergency Callback Number dependencies for an entity. Also applies to workspaces and virtual lines.

        Emergency Callback Configurations can be enabled at the organization level, Users without individual telephone
        numbers, such as extension-only users, must be set up with accurate Emergency Call Back Numbers (ECBN) to
        enable them to make emergency calls. These users can either utilize the default ECBN for their location or be
        assigned another specific telephone number from that location for emergency purposes.

        Retrieving the dependencies requires a full, user or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for the person, virtual line, or workspace
        :type entity_id: str
        :param org_id: Retrieve Emergency Callback Number attributes for this organization.
        :type org_id: str
        :rtype: :class:`ECBNDependencies`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id, 'dependencies')
        data = super().get(url, params=params)
        r = ECBNDependencies.model_validate(data)
        return r

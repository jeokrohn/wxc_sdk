"""
Outgoing permissions API and datatypes

API is used in:
    * person settings
    * location settings
    * workspace settings
    * virtual line settings
"""
import json
from dataclasses import dataclass
from typing import Optional, Union

from pydantic import field_validator, TypeAdapter, model_validator

from .common import PersonSettingsApiChild, ApiSelector
from ..base import ApiModel
from ..base import SafeEnum as Enum
from ..common import AuthCode
from ..rest import RestSession

__all__ = ['OutgoingPermissionCallType', 'Action', 'CallTypePermission', 'CallingPermissions',
           'OutgoingPermissions', 'AutoTransferNumbers', 'DigitPattern', 'DigitPatterns', 'DigitPatternsApi',
           'TransferNumbersApi', 'AccessCodesApi', 'OutgoingPermissionsApi']


class OutgoingPermissionCallType(str, Enum):
    """
    call types for outgoing permissions
    """
    internal_call = 'INTERNAL_CALL'
    local = 'LOCAL'
    toll_free = 'TOLL_FREE'
    toll = 'TOLL'
    national = 'NATIONAL'
    international = 'INTERNATIONAL'
    operator_assisted = 'OPERATOR_ASSISTED'
    chargeable_directory_assisted = 'CHARGEABLE_DIRECTORY_ASSISTED'
    special_services_i = 'SPECIAL_SERVICES_I'
    special_services_ii = 'SPECIAL_SERVICES_II'
    premium_services_i = 'PREMIUM_SERVICES_I'
    premium_services_ii = 'PREMIUM_SERVICES_II'


class Action(str, Enum):
    """
    Action on a specific call type
    """
    allow = 'ALLOW'
    block = 'BLOCK'
    auth_code = 'AUTH_CODE'
    transfer_number_1 = 'TRANSFER_NUMBER_1'
    transfer_number_2 = 'TRANSFER_NUMBER_2'
    transfer_number_3 = 'TRANSFER_NUMBER_3'


class CallTypePermission(ApiModel):
    """
    Permission for a specific call type
    """
    #: Action on the given call_type.
    action: Action
    #: Allow the person to transfer or forward a call of the specified call type.
    transfer_enabled: bool

    @staticmethod
    def default() -> 'CallTypePermission':
        return CallTypePermission(action=Action.allow, transfer_enabled=True)


class CallingPermissions(ApiModel):
    """
    Calling permissions for all call types
    """

    class Config:
        # allow undefined attributes (new call types)
        extra = 'allow'
        ...

    @model_validator(mode='before')
    def rv(cls, v):
        """

        :meta private:

        Make sure that values for unknown call types are also parsed into CallTypePermission instances
        """
        for call_type in v:
            if call_type not in cls.model_fields:
                # try to parse unknown call type into CallTypePermission instance
                v[call_type] = CallTypePermission.model_validate(v[call_type])
        return v

    internal_call: Optional[CallTypePermission] = None
    local: Optional[CallTypePermission] = None
    toll_free: Optional[CallTypePermission] = None
    toll: Optional[CallTypePermission] = None
    national: Optional[CallTypePermission] = None
    international: Optional[CallTypePermission] = None
    operator_assisted: Optional[CallTypePermission] = None
    chargeable_directory_assisted: Optional[CallTypePermission] = None
    special_services_i: Optional[CallTypePermission] = None
    special_services_ii: Optional[CallTypePermission] = None
    premium_services_i: Optional[CallTypePermission] = None
    premium_services_ii: Optional[CallTypePermission] = None

    def for_call_type(self, call_type: OutgoingPermissionCallType) -> Optional[CallTypePermission]:
        """
        get call type setting for a specific call type

        :param call_type: call type
        :type call_type: :class:`OutgoingPermissionCallType`
        :return: permissions
        :rtype: :class:`CallTypePermission`
        """
        try:
            # if parameter is an actual Enum we want to use the name for attribute access
            call_type = call_type.name
        except AttributeError:
            # ignore AttributeError; call_type most probably was a string already -> use lower case as attribute name
            call_type = call_type.lower()
        try:
            return getattr(self, call_type)
        except AttributeError:
            return None

    def permissions_dict(self) -> dict[str, CallTypePermission]:
        """
        Get a dictionary of all permissions. Key is the call type and the value is the permission for this call type

        :return: dict of all permissions
        """
        return {ct: ctp for ct, ctp in self}

    @staticmethod
    def allow_all() -> 'CallingPermissions':
        """
        most permissive permissions

        :return: :class:`CallingPermissions` instance allowing all call types
        :rtype: CallingPermissions
        """
        init_dict = {call_type: CallTypePermission(action=Action.allow, transfer_enabled=True)
                     for call_type in CallingPermissions.model_fields}
        return CallingPermissions(**init_dict)

    @staticmethod
    def default() -> 'CallingPermissions':
        """
        default settings

        :return: :class:`CallingPermissions`
        :rtype: CallingPermissions
        """
        # allow all call types except for a few
        r = CallingPermissions.allow_all()
        for call_type in (OutgoingPermissionCallType.international, OutgoingPermissionCallType.premium_services_i,
                          OutgoingPermissionCallType.premium_services_ii):
            ctp = r.for_call_type(call_type)
            ctp.transfer_enabled = False
            ctp.action = Action.block
        return r


class OutgoingPermissions(ApiModel):
    """
    Person's Outgoing Permission Settings
    """
    #: When true, indicates that this user uses the specified calling permissions when placing outbound calls.
    use_custom_enabled: Optional[bool] = None
    #: Specifies the outbound calling permissions settings.
    calling_permissions: Optional[CallingPermissions] = None

    @field_validator('calling_permissions', mode='before')
    def transform_calling_permissions(cls, v):
        """
        calling permissions are returned by the API as a list of triples:
            "callingPermissions": [
              {
                "action": "ALLOW",
                "transferEnabled": true,
                "callType": "INTERNAL_CALL"
              },
              {
                "action": "ALLOW",
                "transferEnabled": true,
                "callType": "LOCAL"
              }, ...
        The validator transforms this to a dict
        that can be deserialized to a :class:`CallingPermissions` instance:
            "callingPermissions": {
                "internal_call": {
                    "action": "ALLOW",
                    "transferEnabled": true
                },
                "local": {
                    "action": "ALLOW",
                    "transferEnabled": true
                }
            }

        :meta private:
        """
        if not isinstance(v, list):
            return v
        r = {}
        for entry in v:
            call_type = entry['callType']
            r[call_type.lower()] = {k: v for k, v in entry.items() if k != 'callType'}
        return r

    # noinspection PyMethodOverriding
    def model_dump(self, drop_call_types: set[str] = None) -> dict:
        """

        :meta private:
        calling permissions are converted back to a list of objects.
        drop_call_types can be a set of call types to be excluded from callingPermissions
        """
        if drop_call_types is None:
            # default call types to be excluded from updates
            drop_call_types = {'url_dialing', 'unknown', 'casual'}
        # dump w/o calling_permissions; we build that extra
        data = super().model_dump(exclude={'calling_permissions'}, by_alias=True)
        if self.calling_permissions is not None:
            permissions = []
            for call_type, call_type_permission in self.calling_permissions:
                call_type_permission: CallTypePermission
                if not call_type_permission or (call_type in drop_call_types):
                    continue
                ct_dict = call_type_permission.model_dump(by_alias=True)
                ct_dict['callType'] = call_type.upper()
                permissions.append(ct_dict)
            data['callingPermissions'] = permissions
        return data

    def model_dump_json(self, drop_call_types: set[str] = None) -> str:
        """

        :meta private:
        calling permissions are converted back to a list of objects.
        drop_call_types can be a set of call types to be excluded from callingPermissions
        """
        return json.dumps(self.model_dump(drop_call_types))


class AutoTransferNumbers(ApiModel):
    """
    Outgoing permission auto transfer numbers
    """
    #: Calls placed meeting the criteria in an outbound rule whose action is TRANSFER_NUMBER_1 will be transferred to
    #: this number
    auto_transfer_number1: Optional[str] = None
    #: Calls placed meeting the criteria in an outbound rule whose action is TRANSFER_NUMBER_2 will be transferred to
    #: this number
    auto_transfer_number2: Optional[str] = None
    #: Calls placed meeting the criteria in an outbound rule whose action is TRANSFER_NUMBER_3 will be transferred to
    #: this number
    auto_transfer_number3: Optional[str] = None

    @property
    def configure_unset_numbers(self) -> 'AutoTransferNumbers':
        """
        Unset numbers are returned by the API as null (None). To set a number back to unset an empty strings has to
        be set. This property returns an :class:`AutoTransferNumbers` instance where the numbers are set to an empty
        string instead of None

        :return: auto transfer numbers with empty strings instead of None
        :rtype: :class:`AutoTransferNumbers`
        """
        data = self.model_dump()
        for k in data:
            data[k] = data[k] or ''
        return AutoTransferNumbers.model_validate(data)


class DigitPattern(ApiModel):
    #: A unique identifier for the digit pattern.
    id: Optional[str] = None
    #: A unique name for the digit pattern.
    name: Optional[str] = None
    #: The digit pattern to be matched with the input number.
    pattern: Optional[str] = None
    #: Action to be performed on the input number that matches with the digit pattern.
    action: Optional[Action] = None
    #: Option to allow or disallow transfer of calls.
    transfer_enabled: Optional[bool] = None

    def create_or_update(self) -> dict:
        """
        data for create or update

        :meta private:
        """
        return self.model_dump(mode='json', exclude_none=True, exclude={'id'}, by_alias=True)


class DigitPatterns(ApiModel):
    #: When `true`, use custom settings for the digit patterns category of outgoing call permissions.
    use_custom_digit_patterns: Optional[bool] = None
    #: List of digit patterns.
    digit_patterns: Optional[list[DigitPattern]] = None


class TransferNumbersApi(PersonSettingsApiChild):
    """
    API for outgoing permission auto transfer numbers
    """
    feature = 'outgoingPermission/autoTransferNumbers'

    def read(self, person_id: str, org_id: str = None) -> AutoTransferNumbers:
        """
        Retrieve Transfer Numbers Settings for a Workspace.

        When calling a specific call type, this workspace will be automatically transferred to another number. The
        person assigned the Auto Transfer Number can then approve the call and send it through or reject the call
        type. You can add up to 3 numbers.

        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or
        a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param person_id: Unique identifier for the workspace.
        :type person_id: str
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: auto transfer numbers
        :rtype: :class:`AutoTransferNumbers`
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(url, params=params)
        return AutoTransferNumbers.model_validate(data)

    def configure(self, person_id: str, settings: AutoTransferNumbers, org_id: str = None):
        """
        Modify Transfer Numbers Settings for a Place.

        When calling a specific call type, this workspace will be automatically transferred to another number.
        The person assigned the Auto Transfer Number can then approve the call and send it through or reject the
        call type. You can add up to 3 numbers.

        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a
        user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param person_id: Unique identifier for the workspace.
        :type person_id: str
        :param settings: new auto transfer numbers
        :type settings: :class:`AutoTransferNumbers`
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        body = settings.model_dump_json()
        self.put(url, params=params, data=body)


class AccessCodesApi(PersonSettingsApiChild):
    """
    API for outgoing permission access codes: locations, persons, workspaces, virtual lines
    """
    feature = 'outgoingPermission/accessCodes'

    def read(self, workspace_id: str, org_id: str = None) -> list[AuthCode]:
        """
        Retrieve Access codes for a Workspace.

        Access codes are used to bypass permissions.

        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or
        a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :return: list of access codes
        :rtype: list of :class:`AuthCode`
        """
        url = self.f_ep(person_id=workspace_id)
        params = org_id and {'orgId': org_id} or None
        data = self.get(url, params=params)
        return TypeAdapter(list[AuthCode]).validate_python(data['accessCodes'])

    def delete_codes(self, workspace_id: str, access_codes: list[Union[str, AuthCode]], org_id: str = None):
        """
        Modify Access codes for a workspace.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a
        user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param access_codes: authorization codes to remove
        :type access_codes: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        """
        url = self.f_ep(person_id=workspace_id)
        params = org_id and {'orgId': org_id} or None
        body = {'deleteCodes': [ac.code if isinstance(ac, AuthCode) else ac
                                for ac in access_codes]}
        self.put(url, params=params, json=body)

    def create(self, workspace_id: str, code: str, description: str, org_id: str = None):
        """
        Create new Access codes for the given workspace.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a
        user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param code: Indicates an access code.
        :type code: str
        :param description: Indicates the description of the access code.
        :type description: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        """
        url = self.f_ep(person_id=workspace_id)
        params = org_id and {'orgId': org_id} or None
        body = {'code': code,
                'description': description}
        self.post(url, params=params, json=body)


class DigitPatternsApi(PersonSettingsApiChild):
    feature = 'outgoingPermission/digitPatterns'

    def get_digit_patterns(self, entity_id: str,
                           org_id: str = None) -> DigitPatterns:
        """
        Retrieve Digit Patterns

        Retrieve the person's digit patterns.

        Digit patterns are used to bypass permissions.

        Retrieving digit patterns requires a full or user or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for location, person, workspace, or virtual line.
        :type entity_id: str
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`UserOutgoingPermissionDigitPatternGetListObject`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.f_ep(person_id=entity_id)
        data = super().get(url, params=params)
        r = DigitPatterns.model_validate(data)
        return r

    def details(self, entity_id: str, digit_pattern_id: str,
                org_id: str = None) -> DigitPattern:
        """
        Retrieve Digit Pattern Details for a Person

        Retrieve the digit pattern details for a person.

        Digit patterns are used to bypass permissions.

        Retrieving the digit pattern details requires a full or user or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for location, person, workspace, or virtual line.
        :type entity_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: :class:`UserDigitPatternObject`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.f_ep(person_id=entity_id, path=digit_pattern_id)
        data = super().get(url, params=params)
        r = DigitPattern.model_validate(data)
        return r

    def create(self, entity_id: str, pattern: DigitPattern, org_id: str = None) -> str:
        """
        Create Digit Patterns for a Person

        Create new digit pattern for the given person.

        Digit patterns are used to bypass permissions.

        Creating the digit pattern requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param entity_id: Unique identifier for location, person, workspace, or virtual line.
        :type entity_id: str
        :param pattern: new digit pattern
        :type pattern: :class:`DigitPattern`
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        body = pattern.create_or_update()
        url = self.f_ep(person_id=entity_id)
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def update_category_control_settings(self, entity_id: str,
                                         use_custom_digit_patterns: bool = None,
                                         org_id: str = None):
        """
        Modify the Digit Pattern Category Control Settings for the Entity

        Modifies whether this user uses the specified digit patterns when placing outbound calls or not.

        Updating the digit pattern category control settings requires a full or user or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param entity_id: Unique identifier for location, person, workspace, or virtual line.
        :type entity_id: str
        :param use_custom_digit_patterns: When `true`, use custom settings for the digit patterns category of outgoing
            call permissions.
        :type use_custom_digit_patterns: bool
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        body = dict()
        if use_custom_digit_patterns is not None:
            body['useCustomDigitPatterns'] = use_custom_digit_patterns
        url = self.f_ep(person_id=entity_id)
        super().put(url, params=params, json=body)

    def update(self, entity_id: str, settings: DigitPattern, org_id: str = None):
        """
        Modify a Digit Pattern for the Entity

        Modify Digit Patterns for a Entity.

        Digit patterns are used to bypass permissions.

        Updating the digit pattern requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param entity_id: Unique identifier for location, person, workspace, or virtual line.
        :type entity_id: str
        :param settings: new digit pattern settings
        :type settings: :class:`DigitPattern`
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        body = settings.create_or_update()
        url = self.f_ep(person_id=entity_id, path=settings.id)
        super().put(url, params=params, json=body)

    def delete(self, entity_id: str, digit_pattern_id: str, org_id: str = None):
        """
        Delete a Digit Pattern for the Entity

        Delete Digit Pattern for a Entity.

        Digit patterns are used to bypass permissions.

        Deleting the digit pattern requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param entity_id: Unique identifier for location, person, workspace, or virtual line.
        :type entity_id: str
        :param digit_pattern_id: Unique identifier for the digit pattern.
        :type digit_pattern_id: str
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        url = self.f_ep(person_id=entity_id, path=digit_pattern_id)
        super().delete(url, params=params)

    def delete_all(self, entity_id: str, org_id: str = None):
        """
        Delete all Digit Patterns for a Entity.

        Digit patterns are used to bypass permissions.

        Deleting the digit patterns requires a full or user or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param entity_id: Unique identifier for location, person, workspace, or virtual line.
        :type entity_id: str
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access the API.
        :type org_id: str
        :rtype: None
        """
        params = org_id and {'orgId': org_id} or None
        url = self.f_ep(person_id=entity_id)
        super().delete(url, params=params)


@dataclass(init=False)
class OutgoingPermissionsApi(PersonSettingsApiChild):
    """
    API for person's outgoing permissions settings

    Also used for workspace, location, and virtual line outgoing permissions
    """
    transfer_numbers: TransferNumbersApi
    access_codes: AccessCodesApi
    digit_patterns: DigitPatternsApi

    feature = 'outgoingPermission'

    def __init__(self, *, session: RestSession,
                 selector: ApiSelector = 'person'):
        super().__init__(session=session, selector=selector)
        if selector == ApiSelector.virtual_line:
            # Virtual Lines for now don't have any of the additional features
            return
        self.transfer_numbers = TransferNumbersApi(session=session, selector=selector)
        self.access_codes = AccessCodesApi(session=session, selector=selector)
        self.digit_patterns = DigitPatternsApi(session=session, selector=selector)

    def read(self, person_id: str, org_id: str = None) -> OutgoingPermissions:
        """
        Retrieve a Person's Outgoing Calling Permissions Settings

        You can change the outgoing calling permissions for a person if you want them to be different from your
        organization's default.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the entity.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: outgoing permission settings for specific user
        :rtype: :class:`OutgoingPermissions`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return OutgoingPermissions.model_validate(self.get(ep, params=params))

    def configure(self, person_id: str, settings: OutgoingPermissions, drop_call_types: set[str] = None,
                  org_id: str = None):
        """
        Configure a Person's Outgoing Calling Permissions Settings

        Turn on outgoing call settings for this person to override the calling settings from the location that are
        used by default.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the entity.
        :type person_id: str
        :param settings: new setting to be applied
        :type settings: :class:`OutgoingPermissions`
        :param drop_call_types: set of call type names to be excluded from updates. Default is the set of call_types
            known to be not supported for updates
        :type drop_call_types: set[str]
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        self.put(ep, params=params, data=settings.model_dump_json(drop_call_types=drop_call_types))

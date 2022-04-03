"""
Person outgoing permissions API
"""
import json
from enum import Enum

from pydantic import validator

from .common import PersonSettingsApiChild
from ..base import ApiModel

__all__ = ['OutgoingPermissionCallType', 'Action', 'CallTypePermission', 'CallingPermissions',
           'OutgoingPermissions', 'OutgoingPermissionsApi']


class OutgoingPermissionCallType(str, Enum):
    """
    call types for outgoing permissions
    """
    internal_call = 'INTERNAL_CALL'
    local = 'LOCAL'
    toll_free = 'TOLL_FREE'
    toll = 'TOLL'
    international = 'INTERNATIONAL'
    operator_assisted = 'OPERATOR_ASSISTED'
    chargeable_directory_assisted = 'CHARGEABLE_DIRECTORY_ASSISTED'
    special_services_i = 'SPECIAL_SERVICES_I'
    special_services_ii = 'SPECIAL_SERVICES_II'
    premium_services_i = 'PREMIUM_SERVICES_I'
    premium_services_ii = 'PREMIUM_SERVICES_II'
    casual = 'CASUAL'
    # TODO: file documentation defect. documented as URI_DIALING
    url_dialing = 'URL_DIALING'
    unknown = 'UNKNOWN'


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


class CallingPermissions(ApiModel):
    """
    Calling permissions for all call types
    """
    internal_call: CallTypePermission
    local: CallTypePermission
    toll_free: CallTypePermission
    toll: CallTypePermission
    international: CallTypePermission
    operator_assisted: CallTypePermission
    chargeable_directory_assisted: CallTypePermission
    special_services_i: CallTypePermission
    special_services_ii: CallTypePermission
    premium_services_i: CallTypePermission
    premium_services_ii: CallTypePermission
    casual: CallTypePermission
    url_dialing: CallTypePermission
    unknown: CallTypePermission

    def for_call_type(self, call_type: OutgoingPermissionCallType) -> CallTypePermission:
        """
        get call type seting for a specific call type

        :param call_type: call type
        :type call_type: :class:`OutgoingPermissionCallType`
        :return: permissions
        :rtype: :class:`CallTypePermission`
        """
        call_type_name = call_type.name
        return self.__dict__[call_type_name]

    @staticmethod
    def allow_all() -> 'CallingPermissions':
        """
        most permissive permissions

        :return: :class:`CallingPermissions`
        """
        init_dict = {call_type.name: CallTypePermission(action=Action.allow, transfer_enabled=True)
                     for call_type in OutgoingPermissionCallType}
        return CallingPermissions(**init_dict)

    @staticmethod
    def default() -> 'CallingPermissions':
        """
        default settings

        :return: :class:`CallingPermissions`
        """
        r = CallingPermissions.allow_all()
        for call_type in (OutgoingPermissionCallType.international, OutgoingPermissionCallType.premium_services_i,
                          OutgoingPermissionCallType.premium_services_ii, OutgoingPermissionCallType.casual):
            ctp = r.for_call_type(call_type)
            ctp.transfer_enabled = False
            ctp.action = Action.block
        return r


class OutgoingPermissions(ApiModel):
    """
    Person's Outgoing Permission Settings
    """
    #: When true, indicates that this user uses the specified calling permissions when placing outbound calls.
    use_custom_enabled: bool
    #: Specifies the outbound calling permissions settings.
    calling_permissions: CallingPermissions

    @validator('calling_permissions', pre=True)
    def transform_calling_permissions(cls, v):
        """
        calling permissions are returned by the API as a list of triples. The validator transforms this to a dict
        that can be deserialized to a :class:`CallingPermissions` instance

        :meta private:
        """
        r = {}
        for entry in v:
            call_type = entry.pop('callType')
            r[call_type.lower()] = entry
        return r

    def json(self, *args, exclude_none=True, by_alias=True, **kwargs) -> str:
        # convert calling_permissions back to a list
        j_data = json.loads(super().json(*args, exclude_none=exclude_none, by_alias=by_alias, **kwargs))
        c_perms = []
        for call_type, setting in j_data['callingPermissions'].items():
            setting['callType'] = call_type.upper()
            c_perms.append(setting)
        j_data['callingPermissions'] = c_perms
        return json.dumps(j_data)


class OutgoingPermissionsApi(PersonSettingsApiChild):
    """
    Api for person's outgoing permissions settings
    """

    feature = 'outgoingPermission'

    def read(self, *, person_id: str, org_id: str = None) -> OutgoingPermissions:
        """
        Retrieve a Person's Outgoing Calling Permissions Settings

        Retrieve a Person's Outgoing Calling Permissions Settings

        You can change the outgoing calling permissions for a person if you want them to be different from your
        organization's default.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: outgoing permission settings for specific user
        :rtype: :class:`OutgoingPermissions`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return OutgoingPermissions.parse_obj(self.get(ep, params=params))

    def configure(self, *, person_id: str, settings: OutgoingPermissions, org_id: str = None):
        """
        Configure a Person's Barge In Settings

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: new setting to be applied
        :type settings: :class:`OutgoingPermissions`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        self.put(ep, params=params, data=settings.json())

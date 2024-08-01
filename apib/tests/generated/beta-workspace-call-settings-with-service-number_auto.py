from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaWorkspaceCallSettingsWithServiceNumberApi', 'NumberOwnerObject', 'NumberOwnerType', 'STATE',
           'TelephonyType', 'WorkspaceAvailableNumberObject', 'WorkspaceCallForwardAvailableNumberObject',
           'WorkspaceECBNAvailableNumberObject', 'WorkspaceECBNAvailableNumberObjectOwner',
           'WorkspaceECBNAvailableNumberObjectOwnerType']


class STATE(str, Enum):
    #: Phone number is in the active state.
    active = 'ACTIVE'
    #: Phone number is in the inactive state.
    inactive = 'INACTIVE'


class TelephonyType(str, Enum):
    #: The object is a PSTN number.
    pstn_number = 'PSTN_NUMBER'


class WorkspaceAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: Indicates if the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: Indicates the telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: Indicates if the phone number is a service number. Service numbers are intended to be high-volume regular phone
    #: numbers (non-mobile, non toll-free numbers). If `true` the `phoneNumber` is a service number; otherwise, it is
    #: a standard number.
    #: example: True
    is_service_number: Optional[bool] = None


class WorkspaceECBNAvailableNumberObjectOwnerType(str, Enum):
    #: Phone number's owner is a workspace.
    place = 'PLACE'
    #: Phone number's owner is a person.
    people = 'PEOPLE'
    #: Phone number's owner is a Virtual Profile.
    virtual_line = 'VIRTUAL_LINE'


class WorkspaceECBNAvailableNumberObjectOwner(ApiModel):
    #: Unique identifier of the owner to which the PSTN Phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the phone number's owner.
    #: example: PEOPLE
    type: Optional[WorkspaceECBNAvailableNumberObjectOwnerType] = None
    #: First name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Test
    first_name: Optional[str] = None
    #: Last name of the phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Person
    last_name: Optional[str] = None
    #: Display name of the phone number's owner. This field will be present only when the owner `type` is `PLACE`.
    #: example: TestWorkSpace
    display_name: Optional[str] = None


class WorkspaceECBNAvailableNumberObject(ApiModel):
    #: A unique identifier for the phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: Indicates if the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: Indicates if the phone number is a toll-free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    #: Indicates the telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: Indicates if the phone number is a service number. Service numbers are intended to be high-volume regular phone
    #: numbers (non-mobile, non toll-free numbers). If `true` the `phoneNumber` is a service number; otherwise, it is
    #: a standard number.
    #: example: True
    is_service_number: Optional[bool] = None
    owner: Optional[WorkspaceECBNAvailableNumberObjectOwner] = None


class NumberOwnerType(str, Enum):
    #: PSTN phone number's owner is a workspace.
    place = 'PLACE'
    #: PSTN phone number's owner is a person.
    people = 'PEOPLE'
    #: PSTN phone number's owner is a Virtual Profile.
    virtual_line = 'VIRTUAL_LINE'
    #: PSTN phone number's owner is an auto-attendant.
    auto_attendant = 'AUTO_ATTENDANT'
    #: PSTN phone number's owner is a call queue.
    call_queue = 'CALL_QUEUE'
    #: PSTN phone number's owner is a group paging.
    group_paging = 'GROUP_PAGING'
    #: PSTN phone number's owner is a hunt group.
    hunt_group = 'HUNT_GROUP'
    #: PSTN phone number's owner is a voice messaging.
    voice_messaging = 'VOICE_MESSAGING'
    #: PSTN phone number's owner is a Single Number Reach.
    office_anywhere = 'OFFICE_ANYWHERE'
    #: PSTN phone number's owner is a Contact Center link.
    contact_center_link = 'CONTACT_CENTER_LINK'
    #: PSTN phone number's owner is a Contact Center adapter.
    contact_center_adapter = 'CONTACT_CENTER_ADAPTER'
    #: PSTN phone number's owner is a route list.
    route_list = 'ROUTE_LIST'
    #: PSTN phone number's owner is a voicemail group.
    voicemail_group = 'VOICEMAIL_GROUP'
    #: PSTN phone number's owner is a collaborate bridge.
    collaborate_bridge = 'COLLABORATE_BRIDGE'


class NumberOwnerObject(ApiModel):
    #: Unique identifier of the owner to which the PSTN Phone number is assigned.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODhiZGIwNC1jZjU5LTRjMjMtODQ4OC00NTNhOTE3ZDFlMjk
    id: Optional[str] = None
    #: Type of the PSTN phone number's owner.
    #: example: PEOPLE
    type: Optional[NumberOwnerType] = None
    #: First name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE`
    #: or `VIRTUAL_LINE`.
    #: example: Test
    first_name: Optional[str] = None
    #: Last name of the PSTN phone number's owner. This field will be present only when the owner `type` is `PEOPLE` or
    #: `VIRTUAL_LINE`.
    #: example: Person
    last_name: Optional[str] = None
    #: Display name of the PSTN phone number's owner. This field will be present except when the owner `type` is
    #: `PEOPLE` or `VIRTUAL_LINE`.
    #: example: TestWorkSpace
    display_name: Optional[str] = None


class WorkspaceCallForwardAvailableNumberObject(ApiModel):
    #: A unique identifier for the PSTN phone number.
    #: example: +12056350001
    phone_number: Optional[str] = None
    #: Extension for the PSTN phone number.
    #: example: 1235
    extension: Optional[str] = None
    #: Phone number's state.
    #: example: ACTIVE
    state: Optional[STATE] = None
    #: Indicates if the phone number is used as a location CLID.
    #: example: True
    is_main_number: Optional[bool] = None
    #: Indicates if the phone number is a toll-free number.
    #: example: True
    toll_free_number: Optional[bool] = None
    #: Indicates the telephony type for the number.
    #: example: PSTN_NUMBER
    telephony_type: Optional[TelephonyType] = None
    #: Indicates if the phone number is a service number. Service numbers are intended to be high-volume regular phone
    #: numbers (non-mobile, non toll-free numbers). If `true` the `phoneNumber` is a service number; otherwise, it is
    #: a standard number.
    #: example: True
    is_service_number: Optional[bool] = None
    #: Owner details for the phone number.
    owner: Optional[NumberOwnerObject] = None


class BetaWorkspaceCallSettingsWithServiceNumberApi(ApiChild, base='telephony/config/workspaces'):
    """
    Beta Workspace Call Settings with Service Number
    
    Workspaces represent places where people work, such as conference rooms, meeting spaces, lobbies, and lunchrooms.
    Devices may be associated with workspaces.
    
    Webex Calling Workspace Settings supports reading and writing of Webex Calling settings for a specific workspace
    within the organization.
    
    Service numbers are intended to be high-volume regular phone numbers (non-mobile, non toll-free numbers), while
    standard numbers are PSTN numbers that do not fall under this classification.
    With the service number feature, available number APIs for location services or for features like members CLID,
    call forwarding or call intercept will now return service numbers in response.
    
    Viewing the list of settings in a workspace /v1/workspaces API requires a full, device, or read-only administrator
    auth token with the `spark-admin:workspaces_read` scope.
    
    Adding, updating, or deleting settings in a workspace /v1/workspaces API requires a full or device administrator
    auth token with the `spark-admin:workspaces_write` scope.
    
    This API can also be used by partner administrators acting as administrators of a different organization than their
    own. In those cases, an `orgId` must be supplied, as indicated in the reference documentation for the relevant
    endpoints.
    """

    def get_workspace_available_phone_numbers(self, location_id: str = None, phone_number: list[str] = None,
                                              org_id: str = None,
                                              **params) -> Generator[WorkspaceAvailableNumberObject, None, None]:
        """
        Get Workspace Available Phone Numbers

        List standard numbers that are available to be assigned as a workspace's phone number.
        By default, this API returns numbers from all locations that are unassigned. To select the suitable number for
        assignment, ensure the workspace's location ID is provided as the `locationId` request parameter.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep('availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_workspace_ecbn_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                   owner_name: str = None, org_id: str = None,
                                                   **params) -> Generator[WorkspaceECBNAvailableNumberObject, None, None]:
        """
        Get Workspace ECBN Available Phone Numbers

        List standard numbers that are available to be assigned as a workspace's emergency callback number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceECBNAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        url = self.ep(f'{workspace_id}/emergencyCallbackNumber/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceECBNAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_workspace_call_forward_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                           owner_name: str = None, extension: str = None,
                                                           org_id: str = None,
                                                           **params) -> Generator[WorkspaceCallForwardAvailableNumberObject, None, None]:
        """
        Get Workspace Call Forward Available Phone Numbers

        List service and standard numbers that are available to be assigned as a workspace's call forward number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'{workspace_id}/callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_workspace_call_intercept_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                             owner_name: str = None, extension: str = None,
                                                             org_id: str = None,
                                                             **params) -> Generator[WorkspaceCallForwardAvailableNumberObject, None, None]:
        """
        Get Workspace Call Intercept Available Phone Numbers

        List service and standard numbers that are available to be assigned as a workspace's call intercept number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceCallForwardAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self.ep(f'{workspace_id}/callIntercept/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceCallForwardAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_workspace_fax_message_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                          org_id: str = None,
                                                          **params) -> Generator[WorkspaceAvailableNumberObject, None, None]:
        """
        Get Workspace Fax Message Available Phone Numbers

        List standard numbers that are available to be assigned as a workspace's FAX message number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        <div><Callout type="info">Only available for workspaces with the professional license
        entitlement.</Callout></div>

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'{workspace_id}/faxMessage/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceAvailableNumberObject, item_key='phoneNumbers', params=params)

    def get_workspace_secondary_available_phone_numbers(self, workspace_id: str, phone_number: list[str] = None,
                                                        org_id: str = None,
                                                        **params) -> Generator[WorkspaceAvailableNumberObject, None, None]:
        """
        Get Workspace Secondary Available Phone Numbers

        List standard numbers that are available to be assigned as a workspace's secondary number.
        These numbers are associated with the location of the workspace specified in the request URL, can be active or
        inactive, and are unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        <div><Callout type="info">Only available for workspaces with the professional license
        entitlement.</Callout></div>

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`WorkspaceAvailableNumberObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self.ep(f'{workspace_id}/secondary/availableNumbers')
        return self.session.follow_pagination(url=url, model=WorkspaceAvailableNumberObject, item_key='phoneNumbers', params=params)

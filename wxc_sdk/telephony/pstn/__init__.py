import builtins
from typing import Any, Optional

from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.common import NumberState, RouteType, TelephonyType

__all__ = [
    'PSTNServiceType',
    'PSTNConnectionOption',
    'PSTNType',
    'PSTNApi',
    'ModifyNumberAction',
    'ModifyNumbersActionOrderStatus',
    'ModifiableNumber',
    'ModifyNumbersActionError',
    'ModifyNumbersActionOrder',
    'ModifyNumbersActionOrderNumber',
    'ModifyNumbersActionOrderNumberStatus',
    'ModifyNumbersActionOrderNumberUsage',
]


class PSTNServiceType(str, Enum):
    #: PSTN service type for geographic numbers.
    geographic_numbers = 'GEOGRAPHIC_NUMBERS'
    #: PSTN service type for toll-free numbers.
    tollfree_numbers = 'TOLLFREE_NUMBERS'
    #: PSTN service type for business texting.
    business_texting = 'BUSINESS_TEXTING'
    #: PSTN service type for contact center services.
    contact_center = 'CONTACT_CENTER'
    #: PSTN service type for service numbers.
    service_numbers = 'SERVICE_NUMBERS'
    #: PSTN service type for non-geographic numbers.
    non_geographic_numbers = 'NON_GEOGRAPHIC_NUMBERS'
    #: PSTN service type for mobile numbers.
    mobile_numbers = 'MOBILE_NUMBERS'


class PSTNType(str, Enum):
    #: PSTN connection type for a premises-based connection.
    local_gateway = 'LOCAL_GATEWAY'
    #: PSTN connection type for a Non-Integrated Cloud Connected PSTN connection.
    non_integrated_ccp = 'NON_INTEGRATED_CCP'
    #: PSTN connection type for an Integrated Cloud Connected PSTN connection. Updating the location with this
    #: connection type is currently not supported using the API.
    integrated_ccp = 'INTEGRATED_CCP'
    #: PSTN connection type for a Cisco PSTN connection. Updating the location with this connection type is currently
    #: not supported using the API.
    cisco_pstn = 'CISCO_PSTN'


class PSTNConnectionOption(ApiModel):
    #: A unique identifier for the connection.
    id: Optional[str] = None
    #: The display name of the PSTN connection.
    display_name: Optional[str] = None
    #: The PSTN services available for this connection.
    pstn_services: Optional[list[PSTNServiceType]] = None
    #: The PSTN connection type set for the location.
    pstn_connection_type: Optional[PSTNType] = None
    #: Premise route type. This is required if connection type is LOCAL_GATEWAY.
    route_type: Optional[RouteType] = None
    #: Premise route ID. This refers to either a Trunk ID or a Route Group ID. This field is optional but required if
    #: the connection type is LOCAL_GATEWAY.
    route_id: Optional[str] = None


class ModifyNumberAction(str, Enum):
    modify_elin = 'modifyElin'
    modify_standard = 'modifyStandard'
    modify_service = 'modifyService'


class ModifyNumbersActionOrderStatus(str, Enum):
    pending = 'PENDING'
    partial = 'PARTIAL'
    complete = 'COMPLETE'
    provisioned = 'PROVISIONED'
    error = 'ERROR'


class ModifyNumbersActionOrderNumberStatus(str, Enum):
    success = 'SUCCESS'
    failed = 'FAILED'
    pending = 'PENDING'


class ModifyNumbersActionOrderNumberUsage(str, Enum):
    none_ = 'NONE'
    service = 'SERVICE'
    elin = 'ELIN'


class ModifyNumbersActionError(ApiModel):
    #: Phone number associated with the error.
    number: Optional[str] = None
    #: Category of the error, such as `VERIFICATION` or `FAILED`.
    error_type: Optional[str] = None
    #: Stable machine-readable error code, such as `ERR.V.TRM.TMN60045`.
    error_code: Optional[str] = None
    #: Stable symbolic title associated with the error code, such as `NUMBER_HAS_BUSINESS_TEXTING`.
    error_title: Optional[str] = None
    #: Human-readable explanation of the error. Defaults to the message associated with `errorCode` and may contain
    #: more specific runtime detail.
    error_message: Optional[str] = None


class ModifyNumbersActionOrderNumber(ApiModel):
    #: Phone number.
    number: Optional[str] = None
    #: Number-level action status.
    #:
    #: - `SUCCESS` — The action completed successfully for the number.
    #: - `FAILED` — The action failed for the number.
    #: - `PENDING` — The action is still being processed for the number.
    status: Optional[ModifyNumbersActionOrderNumberStatus] = None
    #: Final number usage type.
    #:
    #: - `NONE` — Standard number usage.
    #: - `SERVICE` — Service number usage.
    #: - `ELIN` — Emergency Location Identification Number usage.
    usage: Optional[ModifyNumbersActionOrderNumberUsage] = None
    #: Validation or execution errors for this number.
    errors: Optional[list[ModifyNumbersActionError]] = None


class ModifyNumbersActionOrder(ApiModel):
    #: Order identifier in Webex format.
    order_id: Optional[str] = None
    #: Order status.
    #:
    #: - `PENDING` — The order is waiting to be processed.
    #: - `PARTIAL` — The order completed with only some number actions succeeding.
    #: - `COMPLETE` — The order completed successfully.
    #: - `PROVISIONED` — The requested number changes were successfully provisioned.
    #: - `ERROR` — The order failed.
    status: Optional[ModifyNumbersActionOrderStatus] = None
    #: Results for the phone numbers included in the order.
    numbers: Optional[list[ModifyNumbersActionOrderNumber]] = None
    #: Validation or provisioning errors associated with the order.
    errors: Optional[list[ModifyNumbersActionError]] = None


class ModifiableNumber(ApiModel):
    #: Phone number in E.164 format.
    phone_number: Optional[str] = None
    #: Phone number state.
    #:
    #: - `ACTIVE` — The phone number is active.
    #: - `INACTIVE` — The phone number is inactive.
    state: Optional[NumberState] = None
    #: Indicates whether this is a service number.
    is_service_number: Optional[bool] = None
    #: Indicates whether this is a toll-free number.
    toll_free_number: Optional[bool] = None
    #: Indicates whether this is the location main number.
    main_number: Optional[bool] = None
    #: Indicates whether this number is currently an ELIN.
    is_elin: Optional[bool] = Field(alias='isELIN', default=None)
    #: Indicates whether this is a reserved number.
    is_reserved_number: Optional[bool] = None
    #: Telephony type.
    #:
    #: - `PSTN_NUMBER` — A standard PSTN number.
    #: - `MOBILE_NUMBER` — A mobile telephone number.
    telephony_type: Optional[TelephonyType] = None


class PSTNApi(ApiChild, base='telephony/pstn'):
    """
    PSTN

    PSTN Location Connection Settings supports PSTN selection when creating a location or changing a PSTN type for a
    location. This is only supported for Local Gateway and Non-integrated CCP.

    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_pstn_read`.

    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_pstn_write`.

    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def list(
        self, location_id: str, service_types: builtins.list[PSTNServiceType] = None, org_id: str = None
    ) -> list[PSTNConnectionOption]:
        """
        Retrieve PSTN Connection Options for a Location

        Retrieve the list of PSTN connection options available for a location.

        PSTN location connection settings enables the admin to configure or change the PSTN provider for a location.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        `spark-admin:telephony_pstn_read`.

        :param location_id: Return the list of List PSTN location connection options for this location.
        :type location_id: str
        :param service_types: Use the `serviceTypes` parameter to fetch connections for the following services

            * `MOBILE_NUMBERS`
        :type service_types: list[PSTNServiceType]
        :param org_id: List PSTN location connection options for this organization.
        :type org_id: str
        :rtype: list[PSTNConnectionOption]
        """
        params: dict[str, Any] = {}
        if org_id is not None:
            params['orgId'] = org_id
        if service_types is not None:
            params['serviceTypes'] = [enum_str(st) for st in service_types]
        url = self.ep(f'locations/{location_id}/connectionOptions')
        data = super().get(url, params=params)
        r = TypeAdapter(list[PSTNConnectionOption]).validate_python(data['items'])
        return r

    def configure(
        self,
        location_id: str,
        id: str = None,
        premise_route_type: str = None,
        premise_route_id: str = None,
        org_id: str = None,
    ):
        """
        Setup PSTN Connection for a Location

        Set up or update the PSTN connection details for a location.

        PSTN location connection settings enables the admin to configure or change the PSTN provider for a location.

        Setting up PSTN connection on a location requires a full administrator auth token with a scope of
        `spark-admin:telephony_pstn_write`.

        :param location_id: Setup PSTN location connection options for this location.
        :type location_id: str
        :param id: A unique identifier for the connection. This is required for non-integrated CCP.
        :type id: str
        :param premise_route_type: Premise route type. The possible types are TRUNK and ROUTE_GROUP. This is required
            for the local gateway.
        :type premise_route_type: str
        :param premise_route_id: Premise route ID. This refers to either a Trunk ID or a Route Group ID and is required
            for the local gateway.
        :type premise_route_id: str
        :param org_id: Setup PSTN location connection for this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if id is not None:
            body['id'] = id
        if premise_route_type is not None:
            body['premiseRouteType'] = premise_route_type
        if premise_route_id is not None:
            body['premiseRouteId'] = premise_route_id
        url = self.ep(f'locations/{location_id}/connection')
        super().put(url, params=params, json=body)

    def read(self, location_id: str, org_id: str = None) -> PSTNConnectionOption:
        """
        Retrieve PSTN Connection for a Location

        Retrieves the current configured PSTN connection details for a location.

        PSTN location connection settings enables the admin to configure or change the PSTN provider for a location.

        Retrieving the PSTN connection details for a location requires a full or read-only administrator auth token
        with a scope of `spark-admin:telephony_pstn_read`.

        :param location_id: Retrieve PSTN location connection details for this location.
        :type location_id: str
        :param org_id: Retrieve PSTN location connection details for this organization.
        :type org_id: str
        :rtype: :class:`PSTNConnectionOption`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/connection')
        data = super().get(url, params=params)
        r = PSTNConnectionOption.model_validate(data)
        return r

    def perform_numbers_action(
        self, location_id: str, action: ModifyNumberAction, numbers: builtins.list[str], org_id: str = None
    ) -> builtins.list[ModifyNumbersActionOrder]:
        """
        Perform Numbers Action

        Perform number usage action for the specified list of numbers. The required `action` query parameter specifies
        the operation to apply to the numbers in the request body. The API supports modifying number usage between
        STANDARD/SERVICE/ELIN.

        A phone number's usage type determines how it is used within a Webex Calling location. `STANDARD` numbers
        support regular calling and can be assigned to people, workspaces, or features. `SERVICE` numbers support
        services such as Auto Attendant, Call Queue, Hunt Groups, and Webex Contact Center. `ELIN` (Emergency Location
        Identification Number) numbers provide emergency services with accurate caller information and support
        callbacks to the person or workspace that initiated the emergency call, including people with extension-only
        lines.

        Executing number actions requires an administrator auth token with a scope of
        `spark-admin:telephony_pstn_write`.

        :param location_id: Location identifier in Webex format.
        :type location_id: str
        :param action: Action to execute.
        :type action: ModifyNumberAction
        :param numbers: Phone numbers to process.
        :type numbers: list[str]
        :param org_id: Organization ID. If not specified, uses the organization from the OAuth token.
        :type org_id: str
        :rtype: list[ModifyNumbersActionOrder]
        """
        params: dict[str, Any] = dict()
        params['action'] = enum_str(action)
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['numbers'] = numbers
        url = self.ep(f'locations/{location_id}/numbers')
        data = super().post(url, params=params, json=body)
        r = TypeAdapter(list[ModifyNumbersActionOrder]).validate_python(data['orders'])
        return r

    def get_modifiable_numbers(
        self, location_id: str, action: ModifyNumberAction, org_id: str = None
    ) -> builtins.list[ModifiableNumber]:
        """
        Get Modifiable Numbers

        Retrieve modifiable numbers for a location based on action type.

        The required `action` query parameter specifies the operation used to identify eligible numbers.

        This endpoint does not support pagination. Up to a configurable server-side maximum of candidate numbers
        (default 2000) are retrieved and filtered for eligibility, and all eligible numbers within that candidate
        window are returned in a single response.

        A phone number's usage type determines how it is used within a Webex Calling location. `STANDARD` numbers
        support regular calling and can be assigned to people, workspaces, or features. `SERVICE` numbers support
        services such as Auto Attendant, Call Queue, Hunt Groups, and Webex Contact Center. `ELIN` (Emergency Location
        Identification Number) numbers provide emergency services with accurate caller information and support
        callbacks to the person or workspace that initiated the emergency call, including people with extension-only
        lines.

        Viewing number availability requires an administrator auth token with a scope of
        `spark-admin:telephony_pstn_read`.

        :param location_id: Location identifier in Webex format.
        :type location_id: str
        :param action: Action type for modifiable numbers.
        :type action: ModifyNumberAction
        :param org_id: Organization ID. If not specified, uses the organization from the OAuth token.
        :type org_id: str
        :rtype: list[ModifiableNumber]
        """
        params: dict[str, Any] = dict()
        params['action'] = enum_str(action)
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/numbers/availableNumbers')
        data = super().get(url, params=params)
        r = TypeAdapter(list[ModifiableNumber]).validate_python(data['phoneNumbers'])
        return r

"""
API for /me/endpoints
"""
from typing import Optional, List

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum

from wxc_sdk.common import UserType

__all__ = ['MeEndpointsApi', 'MeEndpoint', 'MeSecondaryLine', 'MeMobility',
           'EndpointType', 'MeHost']


class EndpointType(str, Enum):
    #: Endpoint is a calling device.
    calling_device = 'CALLING_DEVICE'
    #: Endpoint is an application.
    application = 'APPLICATION'
    #: Endpoint is a hotdesking guest.
    hotdesking_guest = 'HOTDESKING_GUEST'


class MeSecondaryLine(ApiModel):
    #: Unique identifier for the member.
    id: Optional[str] = None
    #: Type of the member.
    member_type: Optional[UserType] = None


class MeMobility(ApiModel):
    #: Phone number of the mobile device endpoint.
    phone_number: Optional[str] = None
    #: If `true`, alerting is enabled for the endpoint.
    alerting_enabled: Optional[bool] = None


class MeHost(ApiModel):
    #: Unique identifier of the endpoint.
    id: Optional[str] = None
    #: Type of the endpoint.
    type: Optional[EndpointType] = None
    #: Name of the endpoint.
    name: Optional[str] = None
    #: If `true`, the endpoint can be remotely controlled, allowing actions such as mute, hold, resume and answer.
    auto_and_forced_answer_enabled: Optional[bool] = None
    #: Unique identifier of the endpoint owner.
    owner_id: Optional[str] = None
    #: Type of the endpoint owner.
    owner_type: Optional[UserType] = None
    #: List of secondary lines. The secondary line information is not returned for the endpoint owned by an entity
    #: other than the authenticated user.
    secondary_lines: Optional[list[MeSecondaryLine]] = None


class MeEndpoint(ApiModel):
    #: Unique identifier of the endpoint.
    id: Optional[str] = None
    #: Type of the endpoint.
    type: Optional[EndpointType] = None
    #: Display name of the endpoint.
    name: Optional[str] = None
    #: If `true`, the endpoint can be remotely controlled, allowing actions such as mute, hold, resume and answer.
    auto_and_forced_answer_enabled: Optional[bool] = None
    #: Unique identifier of the endpoint owner.
    owner_id: Optional[str] = None
    #: Type of the endpoint owner.
    owner_type: Optional[UserType] = None
    #: List of secondary lines. The secondary line information is not returned for the endpoint owned by an entity
    #: other than the authenticated user.
    secondary_lines: Optional[list[MeSecondaryLine]] = None
    #: Mobility settings of the endpoint.
    mobility_settings: Optional[MeMobility] = None
    #: `HOTDESKING_GUEST` endpoints include the `host` element when the user has an active hotdesking session on a
    #: host.
    host: Optional[MeHost] = None
    #: Indicates if this endpoint has been set as the preferred answer endpoint.
    is_preferred_answer_endpoint: Optional[bool] = None


class MeEndpointsApi(ApiChild, base='telephony/config/people/me'):
    def list(self) -> list[MeEndpoint]:
        """
        Read the List of My Endpoints

        Retrieve the list of endpoints associated with the authenticated user.

        Endpoints are devices, applications, or hotdesking guest profiles. Endpoints can be owned by an authenticated
        user or have the user as a secondary line.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[MeEndpoint]
        """
        url = self.ep('endpoints')
        data = super().get(url)
        r = TypeAdapter(list[MeEndpoint]).validate_python(data['endpoints'])
        return r

    def details(self, endpoint_id: str) -> MeEndpoint:
        """
        Get My Endpoints Details

        Get details of an endpoint associated with the authenticated user.

        Endpoints are devices, applications, or hotdesking guest profiles. Endpoints can be owned by an authenticated
        user or have the user as a secondary line.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param endpoint_id: Unique identifier of the endpoint.
        :type endpoint_id: str
        :rtype: :class:`MeEndpoint`
        """
        url = self.ep(f'endpoints/{endpoint_id}')
        data = super().get(url)
        r = MeEndpoint.model_validate(data)
        return r

    def update(self, endpoint_id: str, mobility_alerting_enabled: bool):
        """
        Update My Endpoints Details

        Update alerting settings of the mobility endpoint associated with the authenticated user.

        Endpoints are devices, applications, or hotdesking guest profiles. Endpoints can be owned by an authenticated
        user or have the user as a secondary line.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param endpoint_id: Unique identifier of the endpoint.
        :type endpoint_id: str
        :param mobility_alerting_enabled: If `true`, alerting is enabled for the endpoint.
        :type mobility_alerting_enabled: bool
        :rtype: None
        """
        body = {'mobilitySettings': {'alertingEnabled': mobility_alerting_enabled}}
        url = self.ep(f'endpoints/{endpoint_id}')
        super().put(url, json=body)

    def available_preferred_answer_endpoints(self, org_id: str = None) -> List[MeEndpoint]:
        """
        Get List Available Preferred Answer Endpoints

        Get the person's preferred answer endpoint and the list of endpoints available for selection. The list of
        endpoints is empty if the person has no endpoints assigned which support the preferred answer endpoint
        functionality.

        A Webex Calling user may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices or third-party endpoints. Preferred answering endpoints
        allow users to specify which of these devices should be prioritized for answering calls, particularly when a
        person's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure that
        calls are answered on the most convenient or appropriate device for the person.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: list[Endpoints]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('settings/availablePreferredAnswerEndpoints')
        data = super().get(url, params=params)
        r = TypeAdapter(list[MeEndpoint]).validate_python(data['endpoints'])
        return r

    def get_preferred_answer_endpoint(self) -> MeEndpoint:
        """
        Get Preferred Answer Endpoint

        Retrieve the selected preferred answering endpoint for the user. If a preferred endpoint is not set for the
        person, API returns empty

        A Webex Calling user may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices or third-party endpoints. Preferred answering endpoints
        allow users to specify which of these devices should be prioritized for answering calls, particularly when a
        person's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure that
        calls are answered on the most convenient or appropriate device for the person.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`MeEndpoint`
        """

        url = self.ep('settings/preferredAnswerEndpoint')
        data = super().get(url)
        if not data:
            return None
        r = MeEndpoint.model_validate(data)
        return r

    def modify_preferred_answer_endpoint(self, id: str):
        """
        Modify Preferred Answer Endpoint

        Sets or clears the person’s preferred answer endpoint. To clear the preferred answer endpoint the `id`
        attribute must be set to null.

        A Webex Calling user may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices or third-party endpoints. Preferred answering endpoints
        allow users to specify which of these devices should be prioritized for answering calls, particularly when a
        person's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure that
        calls are answered on the most convenient or appropriate device for the person.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: Person’s preferred answer endpoint.
        :type id: str
        :type org_id: str
        :rtype: None
        """
        body = dict()
        body['id'] = id
        url = self.ep('settings/preferredAnswerEndpoint')
        super().put(url, json=body)

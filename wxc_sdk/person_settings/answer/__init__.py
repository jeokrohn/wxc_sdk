import builtins
from typing import Any, Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.common import EndpointType
from wxc_sdk.person_settings.common import ApiSelector
from wxc_sdk.rest import RestSession

__all__ = ['AnswerApi', 'AnswerSettings', 'AnswerEndpoint', 'AnswerSettingsEndpointType']


class AnswerSettingsEndpointType(str, Enum):
    #: The Webex desktop application answers the call.
    webex_app_desktop = 'WEBEX_APP_DESKTOP'
    #: The person's primary physical device answers the call.
    primary_device = 'PRIMARY_DEVICE'
    #: A physical device other than the person's primary device answers the call.
    non_primary_device = 'NON_PRIMARY_DEVICE'
    #: The device on which the person is signed in as a hot desking guest answers the call.
    hotdesk_device = 'HOTDESK_DEVICE'
    #: No preferred answer endpoint is selected.
    none_ = 'NONE'


class AnswerSettings(ApiModel):
    #: The unique identifier for the preferred answer endpoint. The companion `preferredAnswerEndpointIdType`
    #: identifies the encoded resource type as `APPLICATION`, `CALLING_DEVICE`, or `HOTDESKING_GUEST`.
    preferred_answer_endpoint_id: Optional[str] = None
    #: The preferred endpoint's behavior category.
    preferred_answer_endpoint_type: Optional[AnswerSettingsEndpointType] = None
    #: The resource type encoded by `preferredAnswerEndpointId`.
    preferred_answer_endpoint_id_type: Optional[EndpointType] = None
    #: Indicates whether the person must have a preferred answer endpoint selected in order for a call to be
    #: auto-answered.
    preferred_answer_endpoint_required: Optional[bool] = None
    #: Indicates whether auto answer is enabled for the person.
    auto_answer_enabled: Optional[bool] = None
    #: Indicates whether the person can clear the preferred endpoint setting.
    is_preferred_endpoint_clearable_by_person: Optional[bool] = None

    def update(self) -> dict[str, Any]:
        """
        Data for update

        :meta private:
        """
        return self.model_dump(
            mode='json',
            by_alias=True,
            exclude_unset=True,
            exclude={
                'preferred_answer_endpoint_type',
                'preferred_answer_endpoint_id_type',
                'preferred_answer_endpoint_required',
            },
        )


class AnswerEndpoint(ApiModel):
    #: Unique identifier for the endpoint. The companion `type` identifies the endpoint category; the opaque identifier
    #: represents a `CALLING_DEVICE`, `APPLICATION`, or `HOTDESKING_GUEST` resource.
    id: Optional[str] = None
    type: Optional[EndpointType] = None
    #: Name of the endpoint. For a device endpoint, the name can include the value of a configured `name=<value>`
    #: device tag.
    name: Optional[str] = None
    #: Indicates whether this endpoint is currently selected as the preferred answer endpoint.
    is_preferred_answer_endpoint: Optional[bool] = None


class AnswerApi(ApiChild, base=''):
    """
    API for Answer Settings. Used for person, workspace, and virtual line answer settings.
    """

    def __init__(self, *, session: RestSession, selector: ApiSelector = ApiSelector.person):
        if selector == ApiSelector.person:
            base = 'telephony/config/people'
        elif selector == ApiSelector.workspace:
            base = 'workspaces'
        elif selector == ApiSelector.virtual_line:
            base = 'telephony/config/virtualLines'
        else:
            raise ValueError(f'Invalid selector: {selector}')
        super().__init__(session=session, base=base)

    def read(self, entity_id: str, org_id: str = None) -> AnswerSettings:
        """
        Get Answer Settings for an Entity

        Get the answer settings for a specific person.

        Answer settings allow administrators to configure automatic call answering behavior for an entity, including
        preferred answer endpoint and whether auto answer is enabled.

        This API requires a full administrator, read-only administrator, delegated full administrator, user
        administrator, or location administrator auth token with the `spark-admin:telephony_config_read` scope.

        :param entity_id: The unique identifier for the person.
        :type entity_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: :class:`AnswerSettings`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{entity_id}/answerSettings')
        data = super().get(url, params=params)
        r = AnswerSettings.model_validate(data)
        return r

    def update(
        self,
        entity_id: str,
        preferred_answer_endpoint_id: str = None,
        auto_answer_enabled: bool = None,
        is_preferred_endpoint_clearable_by_person: bool = None,
        org_id: str = None,
    ) -> None:
        """
        Update Answer Settings for an Entity

        Modify the answer settings for a specific person.

        Answer settings allow administrators to configure automatic call answering behavior for an entity, including
        preferred answer endpoint and whether auto answer is enabled. To clear the preferred answer endpoint, the
        `preferredAnswerEndpointId` must be set to null.

        This API requires a full administrator, delegated full administrator, user administrator, or location
        administrator auth token with the `spark-admin:telephony_config_write` scope.

        :param entity_id: The unique identifier for the person.
        :type entity_id: str
        :param preferred_answer_endpoint_id: The unique identifier for the preferred answer endpoint. This may be a
            device, application, or hot desking guest endpoint. Set to null to clear the preferred answer endpoint;
            omit to leave unchanged.
        :type preferred_answer_endpoint_id: str
        :param auto_answer_enabled: Indicates whether auto answer is enabled for the person.
        :type auto_answer_enabled: bool
        :param is_preferred_endpoint_clearable_by_person: Indicates whether the person can clear the preferred endpoint
            setting.
        :type is_preferred_endpoint_clearable_by_person: bool
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        if preferred_answer_endpoint_id is not None:
            body['preferredAnswerEndpointId'] = preferred_answer_endpoint_id or None
        if auto_answer_enabled is not None:
            body['autoAnswerEnabled'] = auto_answer_enabled
        if is_preferred_endpoint_clearable_by_person is not None:
            body['isPreferredEndpointClearableByPerson'] = is_preferred_endpoint_clearable_by_person
        url = self.ep(f'{entity_id}/answerSettings')
        super().put(url, params=params, json=body)

    def available_preferred_answer_endpoints(self, entity_id: str, org_id: str = None) -> builtins.list[AnswerEndpoint]:
        """
        Get Available Preferred Answer Endpoints for an Entity

        Get the list of available preferred answer endpoints for a specific person. This API returns all available
        endpoints in a single response.

        A Webex Calling person may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices, or third-party endpoints. Preferred answering endpoints
        allow administrators to specify which of these devices should be prioritized for answering calls, particularly
        when an entity's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure
        that calls are answered on the most convenient or appropriate device for the person.

        This API requires a full administrator, read-only administrator, delegated full administrator, user
        administrator, or location administrator auth token with the `spark-admin:telephony_config_read` scope.

        :param entity_id: The unique identifier for the person.
        :type entity_id: str
        :param org_id: Optional target organization identifier. Defaults to token's organization if not provided.
        :type org_id: str
        :rtype: list[AnswerEndpoint]
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{entity_id}/availablePreferredAnswerEndpoints')
        data = super().get(url, params=params)
        r = TypeAdapter(list[AnswerEndpoint]).validate_python(data['endpoints'])
        return r

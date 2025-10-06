"""
API for /me/endpoints
"""

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild

__all__ = ['MeSecondaryLineEndpointsApi']

from wxc_sdk.me.endpoints import MeEndpoint


class MeSecondaryLineEndpointsApi(ApiChild, base='telephony/config/people/me'):
    def list(self, line_owner_id: str) -> list[MeEndpoint]:
        """
        Get My Secondary Line Owner's Available Preferred Answer Endpoint List

        Retrieve the list of available preferred answer endpoints for the secondary line owner of the authenticated
        person.

        A Webex Calling user may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices or third-party endpoints. Preferred answering endpoints
        allow users to specify which of these devices should be prioritized for answering calls, particularly when a
        person's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure that
        calls are answered on the most convenient or appropriate device for the person.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param line_owner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type line_owner_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: list[Endpoints]
        """
        url = self.ep(f'settings/secondaryLines/{line_owner_id}/availablePreferredAnswerEndpoints')
        data = super().get(url)
        r = TypeAdapter(list[MeEndpoint]).validate_python(data['endpoints'])
        return r

    def get_preferred_answer_endpoint(self, line_owner_id: str) -> MeEndpoint:
        """
        Get My Secondary Line Owner's Preferred Answer Endpoint

        Retrieve the selected preferred answering endpoint for the secondary line owner of the authenticated person. If
        a preferred endpoint is not set for the person, API returns empty

        A Webex Calling user may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices or third-party endpoints. Preferred answering endpoints
        allow users to specify which of these devices should be prioritized for answering calls, particularly when a
        person's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure that
        calls are answered on the most convenient or appropriate device for the person.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param line_owner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type line_owner_id: str
        :rtype: :class:`MeEndpoint`
        """

        url = self.ep(f'settings/secondaryLines/{line_owner_id}/preferredAnswerEndpoint')
        data = super().get(url)
        if not data:
            return None
        r = MeEndpoint.model_validate(data)
        return r

    def modify_preferred_answer_endpoint(self, line_owner_id: str, id: str):
        """
        Modify My Secondary Line Owner's Preferred Answer Endpoint

        Sets or clears the preferred answer endpoint for the secondary line owner of the authenticated person. To clear
        the preferred answer endpoint the `id` attribute must be set to null.

        A Webex Calling user may be associated with multiple endpoints such as Webex App (desktop or mobile), Cisco
        desk IP phone, Webex Calling-supported analog devices or third-party endpoints. Preferred answering endpoints
        allow users to specify which of these devices should be prioritized for answering calls, particularly when a
        person's extension (or a virtual line assigned to them) rings on multiple devices. This helps ensure that
        calls are answered on the most convenient or appropriate device for the person.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param line_owner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type line_owner_id: str
        :param id: Person’s preferred answer endpoint.
        :type id: str
        :type org_id: str
        :rtype: None
        """
        body = dict()
        body['id'] = id
        url = self.ep(f'settings/secondaryLines/{line_owner_id}/preferredAnswerEndpoint')
        super().put(url, json=body)

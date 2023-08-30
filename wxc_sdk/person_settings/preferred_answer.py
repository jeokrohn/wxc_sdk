"""
API for person preferred answer endpoint operatins
"""
from typing import Optional

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, SafeEnum

__all__ = ['PreferredAnswerResponse', 'PreferredAnswerApi', 'PreferredAnswerEndpointType', 'PreferredAnswerEndpoint']


class PreferredAnswerEndpointType(str, SafeEnum):
    application = 'APPLICATION'
    device = 'DEVICE'


class PreferredAnswerEndpoint(ApiModel):
    #: Unique identifier for the endpoint.
    id: str
    #: Enumeration that indicates if the endpoint is of type DEVICE or APPLICATION.
    type: PreferredAnswerEndpointType
    #: The name filed in the response is calculated using device tag. Admins have the ability to set tags for
    #: devices. If a name=<value> tag is set, for example “name=home phone“, then the <value> is included in the name
    #: field of the API response. In this example “home phone”.
    name: str


class PreferredAnswerResponse(ApiModel):
    #: Person’s preferred answer endpoint.
    preferred_answer_endpoint_id: Optional[str] = None
    #: Array of endpoints available to the person.
    endpoints: list[PreferredAnswerEndpoint]


class PreferredAnswerApi(ApiChild, base='telephony/config/people'):

    # noinspection PyMethodOverriding
    def ep(self, person_id: str) -> str:
        """
        :meta private:
        """
        return super().ep(f'{person_id}/preferredAnswerEndpoint')

    def read(self, person_id: str, org_id: str = None) -> PreferredAnswerResponse:
        """
        Get Preferred Answer Endpoint
        Get the person's preferred answer endpoint (if any) and the list of endpoints available for selection. These
        endpoints can be used by the following Call Control API's that allow the person to specify an endpointId to
        use for the call:

        /v1/telephony/calls/dial

        /v1/telephony/calls/retrieve

        /v1/telephony/calls/pickup

        /v1/telephony/calls/barge-in

        /v1/telephony/calls/answer

        This API requires spark:telephony_config_read or spark-admin:telephony_config_read scope.

        :param person_id: A unique identifier for the person.
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access
            API.
        :return: person's preferred answer endpoint settings
        :rtype: PreferredAnswerResponse
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep(person_id=person_id)
        return PreferredAnswerResponse.model_validate(self.get(ep, params=params))

    def modify(self, person_id: str, preferred_answer_endpoint_id: str, org_id: str = None):
        """
        Modify Preferred Answer Endpoint
        Sets or clears the person’s preferred answer endpoint. To clear the preferred answer endpoint the p
        preferred_answer_endpoint_id parameter must be set to None.
        This API requires spark:telephony_config_write or spark-admin:telephony_config_write scope.

        :param person_id: A unique identifier for the person.
        :param preferred_answer_endpoint_id: Person’s preferred answer endpoint.
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access
            API.
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep(person_id=person_id)
        self.put(ep, params=params, json={'preferredAnswerEndpointId': preferred_answer_endpoint_id})

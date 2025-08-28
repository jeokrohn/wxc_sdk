from dataclasses import dataclass

from pydantic import TypeAdapter

from wxc_sdk import RestSession
from wxc_sdk.api_child import ApiChild
from wxc_sdk.me import FeatureAccessCode, ServicesEnum
from wxc_sdk.me.secondary_line.callerid import MeSecondaryLineCallerIdApi
from wxc_sdk.me.secondary_line.callpark import MeSecondaryLineCallParkApi
from wxc_sdk.me.secondary_line.callpickup import MeSecondaryLineCallPickupApi
from wxc_sdk.me.secondary_line.endpoints import MeSecondaryLineEndpointsApi
from wxc_sdk.me.secondary_line.forwarding import MeSecondaryLineForwardingApi
from wxc_sdk.me.secondary_line.voicemail import MeSecondaryLineVoicemailApi


@dataclass(init=False, repr=False)
class MeSecondaryLineApi(ApiChild, base='telephony/config/people/me'):
    call_park: MeSecondaryLineCallParkApi
    call_pickup: MeSecondaryLineCallPickupApi
    caller_id: str
    endpoints: MeSecondaryLineEndpointsApi
    forwarding: MeSecondaryLineForwardingApi
    voicemail: MeSecondaryLineVoicemailApi

    def __init__(self, session: RestSession):
        """

        :meta private:
        """
        super().__init__(session=session)
        self.call_park = MeSecondaryLineCallParkApi(session=session)
        self.call_pickup = MeSecondaryLineCallPickupApi(session=session)
        self.caller_id = MeSecondaryLineCallerIdApi(session=session)
        self.endpoints = MeSecondaryLineEndpointsApi(session=session)
        self.forwarding = MeSecondaryLineForwardingApi(session=session)
        self.voicemail = MeSecondaryLineVoicemailApi(session=session)

    def feature_access_codes(self, lineowner_id: str) -> list[FeatureAccessCode]:
        """
        Get My Feature Access Codes For Secondary Line Owner

        Retrieve all Feature Access Codes configured for services that are assigned for the secondary line owner. For
        each feature access code, the name and code are returned. If an alternate code is defined, it is also
        returned.

        Feature access codes (FACs), also known as star codes, give users access to advanced calling features.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: list[FeatureAccessCode]
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/featureAccessCode')
        data = super().get(url)
        r = TypeAdapter(list[FeatureAccessCode]).validate_python(data['featureAccessCodeList'])
        return r

    def calling_services_list(self, lineowner_id: str) -> list[ServicesEnum]:
        """
        Get My Secondary Line Owner Calling Services List

        Retrieves the list of enabled calling services for the secondary line owner of the authenticated user.

        These services are designed to improve call handling and ensure that users can manage their communications
        effectively. They are commonly found in both personal and business telephony systems.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param lineowner_id: Unique identifier for the secondary line owner (applicable only for Virtual Lines).
        :type lineowner_id: str
        :rtype: list[ServicesEnum]
        """
        url = self.ep(f'settings/secondaryLines/{lineowner_id}/services')
        data = super().get(url)
        r = TypeAdapter(list[ServicesEnum]).validate_python(data['services'])
        return r

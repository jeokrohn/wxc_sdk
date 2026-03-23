from typing import Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum

__all__ = [
    'CallerReputationProviderProvider',
    'ReputationProviderRegion',
    'ReputationProviderSettings',
    'ReputationProviderStatus',
    'ReputationProviderState',
    'CallerReputationProviderApi',
]


class ReputationProviderSettings(ApiModel):
    #: Name of the reputation provider.
    name: Optional[str] = None
    #: Unique identifier for the reputation provider.
    id: Optional[str] = None
    #: Client ID used for integration with the reputation provider.
    client_id: Optional[str] = None
    #: Client secret. Cannot be read, only available for update()
    client_secret: Optional[str] = None
    #: Indicates if the caller reputation provider service is enabled.
    enabled: Optional[bool] = None
    #: Score threshold for blocking calls.
    call_block_score_threshold: Optional[str] = None
    #: Score threshold for allowing calls.
    call_allow_score_threshold: Optional[str] = None

    def update(self) -> dict:
        """
        data for update()

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_none=True)


class ReputationProviderState(str, Enum):
    #: Provider is not connected.
    not_connected = 'NOT_CONNECTED'
    #: Provider is in the process of connecting.
    connecting = 'CONNECTING'
    #: Provider is connected.
    connected = 'CONNECTED'
    #: Provider is active and operational.
    active = 'ACTIVE'
    #: Provider's session or token has expired.
    expired = 'EXPIRED'
    #: Authentication with the provider failed.
    auth_failed = 'AUTH_FAILED'
    #: Provider is disabled.
    provider_disabled = 'PROVIDER_DISABLED'


class ReputationProviderStatus(ApiModel):
    #: Unique identifier for the reputation provider.
    id: Optional[str] = None
    status: Optional[ReputationProviderState] = None


class ReputationProviderRegion(ApiModel):
    #: Unique identifier for the region.
    id: Optional[str] = None
    #: Name of the region.
    name: Optional[str] = None
    #: Type of the region (e.g., primary, secondary).
    type: Optional[str] = None
    #: Indicates if the region is visible.
    visible: Optional[bool] = None
    #: Environment type of the region (e.g., production, staging).
    environment_type: Optional[str] = None


class CallerReputationProviderProvider(ApiModel):
    #: Unique identifier for the provider.
    id: Optional[str] = None
    #: Indicates if the provider is enabled.
    enabled: Optional[bool] = None
    #: Name of the provider.
    name: Optional[str] = None
    #: List of regions for the provider.
    regions: Optional[list[ReputationProviderRegion]] = None


class CallerReputationProviderApi(ApiChild, base='telephony/config/serviceSettings/callerReputationProvider'):
    """
    Webex Calling Integration with calling reputation provider

    Webex Calling integrates with telephony Calling Reputation Providers to enhance call security and reduce unwanted
    or fraudulent calls.

    Webex Calling offers a comprehensive, secure, and reliable cloud PBX solution with several features that support
    call quality and security.
    """

    def get(self, organization_id: str = None) -> ReputationProviderSettings:
        """
        Get Caller Reputation Provider Service Settings

        Retrieves the configuration and status of the caller reputation provider service for Webex Calling.

        :param organization_id: Unique identifier for the organization.
        :type organization_id: str
        :rtype: :class:`ReputationProviderSettings`
        """
        params = {}
        if organization_id is not None:
            params['organizationId'] = organization_id
        url = self.ep()
        data = super().get(url, params=params)
        r = ReputationProviderSettings.model_validate(data)
        return r

    def update(self, settings: ReputationProviderSettings, organization_id: str = None):
        """
        Update Caller Reputation Provider Service Settings

        Updates the configuration of the caller reputation provider service for Webex Calling.

        :param settings: New settings for caller reputation provider service
        :type settings: :class:`ReputationProviderSettings`
        :param organization_id: Unique identifier for the organization.
        :type organization_id: str
        :rtype: None
        """
        params = {}
        if organization_id is not None:
            params['organizationId'] = organization_id
        body = settings.update()
        url = self.ep()
        super().put(url, params=params, json=body)

    def unlock(self, rep_id: str, organization_id: str = None):
        """
        Unlock Caller Reputation Provider

        Unlocks the caller reputation provider for Webex Calling.

        :param rep_id: Unique identifier for the reputation provider.
        :type rep_id: str
        :param organization_id: Unique identifier for the organization.
        :type organization_id: str
        :rtype: None
        """
        params = {}
        if organization_id is not None:
            params['organizationId'] = organization_id
        body = dict()
        body['id'] = rep_id
        url = self.ep('actions/unlock/invoke')
        super().post(url, params=params, json=body)

    def providers(self, organization_id: str = None) -> list[CallerReputationProviderProvider]:
        """
        Get Caller Reputation Provider Providers

        Retrieves the list of available caller reputation providers and their regions for Webex Calling.

        :param organization_id: Unique identifier for the organization.
        :type organization_id: str
        :rtype: list[CallerReputationProviderProvider]
        """
        params = {}
        if organization_id is not None:
            params['organizationId'] = organization_id
        url = self.ep('providers')
        data = super().get(url, params=params)
        r = TypeAdapter(list[CallerReputationProviderProvider]).validate_python(data['providers'])
        return r

    def status(self, organization_id: str = None) -> ReputationProviderStatus:
        """
        Get Caller Reputation Provider Status

        Retrieves the current status of the caller reputation provider integration for Webex Calling.

        :param organization_id: Unique identifier for the organization.
        :type organization_id: str
        :rtype: :class:`ReputationProviderStatus`
        """
        params = {}
        if organization_id is not None:
            params['organizationId'] = organization_id
        url = self.ep('status')
        data = super().get(url, params=params)
        r = ReputationProviderStatus.model_validate(data)
        return r

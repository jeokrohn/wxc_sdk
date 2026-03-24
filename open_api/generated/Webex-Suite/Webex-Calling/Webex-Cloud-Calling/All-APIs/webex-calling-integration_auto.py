import builtins
from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CallerReputationProviderProvider', 'CallerReputationProviderRegion', 'CallerReputationProviderSettings',
           'CallerReputationProviderStatus', 'CallerReputationProviderStatusEnum', 'WebexCallingIntegrationApi']


class CallerReputationProviderSettings(ApiModel):
    #: Name of the reputation provider.
    name: Optional[str] = None
    #: Unique identifier for the reputation provider.
    id: Optional[str] = None
    #: Client ID used for integration with the reputation provider.
    client_id: Optional[str] = None
    #: Indicates if the caller reputation provider service is enabled.
    enabled: Optional[bool] = None
    #: Score threshold for blocking calls.
    call_block_score_threshold: Optional[str] = None
    #: Score threshold for allowing calls.
    call_allow_score_threshold: Optional[str] = None


class CallerReputationProviderStatusEnum(str, Enum):
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


class CallerReputationProviderStatus(ApiModel):
    #: Unique identifier for the reputation provider.
    id: Optional[str] = None
    status: Optional[CallerReputationProviderStatusEnum] = None


class CallerReputationProviderRegion(ApiModel):
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
    regions: Optional[list[CallerReputationProviderRegion]] = None


class WebexCallingIntegrationApi(ApiChild, base='telephony/config/serviceSettings/callerReputationProvider'):
    """
    Webex Calling Integration
    
    Webex Calling integrates with telephony Calling Reputation Providers to enhance call security and reduce unwanted
    or fraudulent calls.
    
    Webex Calling offers a comprehensive, secure, and reliable cloud PBX solution with several features that support
    call quality and security.
    """

    def get_caller_reputation_provider_settings(self, organization_id: str = None) -> CallerReputationProviderSettings:
        """
        Get Caller Reputation Provider Service Settings

        Retrieves the configuration and status of the caller reputation provider service for Webex Calling.

        :param organization_id: Unique identifier for the organization.
        :type organization_id: str
        :rtype: :class:`CallerReputationProviderSettings`
        """
        params: dict[str, Any] = dict()
        if organization_id is not None:
            params['organizationId'] = organization_id
        url = self.ep()
        data = super().get(url, params=params)
        r = CallerReputationProviderSettings.model_validate(data)
        return r

    def update_caller_reputation_provider_settings(self, organization_id: str = None, enabled: bool = None,
                                                   id: str = None, name: str = None, client_id: str = None,
                                                   client_secret: str = None, call_block_score_threshold: str = None,
                                                   call_allow_score_threshold: str = None) -> None:
        """
        Update Caller Reputation Provider Service Settings

        Updates the configuration of the caller reputation provider service for Webex Calling.

        :param organization_id: Unique identifier for the organization.
        :type organization_id: str
        :param enabled: Indicates if the caller reputation provider service is enabled. when set to true, all other
            fields are required except clientSecret.
        :type enabled: bool
        :param id: Unique identifier for the reputation provider.
        :type id: str
        :param name: Name of the reputation provider.
        :type name: str
        :param client_id: Client ID used for integration with the reputation provider.
        :type client_id: str
        :param client_secret: Client secret used for integration with the reputation provider.
        :type client_secret: str
        :param call_block_score_threshold: Score threshold for blocking calls.
        :type call_block_score_threshold: str
        :param call_allow_score_threshold: Score threshold for allowing calls.
        :type call_allow_score_threshold: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if organization_id is not None:
            params['organizationId'] = organization_id
        body: dict[str, Any] = dict()
        if enabled is not None:
            body['enabled'] = enabled
        if id is not None:
            body['id'] = id
        if name is not None:
            body['name'] = name
        if client_id is not None:
            body['clientId'] = client_id
        if client_secret is not None:
            body['clientSecret'] = client_secret
        if call_block_score_threshold is not None:
            body['callBlockScoreThreshold'] = call_block_score_threshold
        if call_allow_score_threshold is not None:
            body['callAllowScoreThreshold'] = call_allow_score_threshold
        url = self.ep()
        super().put(url, params=params, json=body)

    def unlock_caller_reputation_provider(self, id: str, organization_id: str = None) -> None:
        """
        Unlock Caller Reputation Provider

        Unlocks the caller reputation provider for Webex Calling.

        :param id: Unique identifier for the reputation provider.
        :type id: str
        :param organization_id: Unique identifier for the organization.
        :type organization_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if organization_id is not None:
            params['organizationId'] = organization_id
        body: dict[str, Any] = dict()
        body['id'] = id
        url = self.ep('actions/unlock/invoke')
        super().post(url, params=params, json=body)

    def get_caller_reputation_provider_providers(self,
                                                 organization_id: str = None) -> builtins.list[CallerReputationProviderProvider]:
        """
        Get Caller Reputation Provider Providers

        Retrieves the list of available caller reputation providers and their regions for Webex Calling.

        :param organization_id: Unique identifier for the organization.
        :type organization_id: str
        :rtype: list[CallerReputationProviderProvider]
        """
        params: dict[str, Any] = dict()
        if organization_id is not None:
            params['organizationId'] = organization_id
        url = self.ep('providers')
        data = super().get(url, params=params)
        r = TypeAdapter(list[CallerReputationProviderProvider]).validate_python(data['providers'])
        return r

    def get_caller_reputation_provider_status(self, organization_id: str = None) -> CallerReputationProviderStatus:
        """
        Get Caller Reputation Provider Status

        Retrieves the current status of the caller reputation provider integration for Webex Calling.

        :param organization_id: Unique identifier for the organization.
        :type organization_id: str
        :rtype: :class:`CallerReputationProviderStatus`
        """
        params: dict[str, Any] = dict()
        if organization_id is not None:
            params['organizationId'] = organization_id
        url = self.ep('status')
        data = super().get(url, params=params)
        r = CallerReputationProviderStatus.model_validate(data)
        return r

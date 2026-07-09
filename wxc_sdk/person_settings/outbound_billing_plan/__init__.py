from typing import Any

from wxc_sdk.person_settings.common import PersonSettingsApiChild

__all__ = ['OutboundBillingPlanApi']


class OutboundBillingPlanApi(PersonSettingsApiChild):
    """
    API for OBP settings. Used for users, virtual lines and workspaces
    """

    feature = 'outboundBillingPlan'

    def read(self, entity_id: str, org_id: str = None) -> bool:
        """
        Retrieve an entity's Outbound Billing Plan

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP).</Callout></div>

        Retrieve the Cisco Calling Plan outbound billing plan setting for an entity.

        Cisco Calling Plan outbound billing identifies whether outbound calls for the entity are billed through Cisco
        Calling Plan.

        The response returns `enabled` as `true` when Cisco Calling Plan outbound billing is enabled for the entity.
        Otherwise, the response returns `enabled` as `false`.

        Retrieving an entity's outbound billing plan requires a full, user, read-only administrator, or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization,
            such as partners, may use this parameter. If not specified, the organization from the OAuth token is used.
        :type org_id: str
        :rtype: bool
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id)
        data = super().get(url, params=params)
        r = data['enabled']
        return r  # type: ignore[return-value]

    def update(self, entity_id: str, enabled: bool, org_id: str = None) -> None:
        """
        Modify a Person's Outbound Billing Plan

        <div><Callout type="warning">Not supported for Webex for Government (FedRAMP).</Callout></div>

        Modify the Cisco Calling Plan outbound billing plan setting for an entity.

        Cisco Calling Plan outbound billing identifies whether outbound calls for the entity are billed through Cisco
        Calling Plan.

        Set `enabled` to `true` to enable Cisco Calling Plan outbound billing. Setting `enabled` to `true` is supported
        only for an entity in a Cisco Calling Plan location. Set `enabled` to `false` to disable it.

        Updating an entity's outbound billing plan requires a full, user, or location administrator auth token with a
        scope of `spark-admin:telephony_config_write`.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param enabled: Set to `true` when Cisco Calling Plan outbound billing is enabled for the entity.
        :type enabled: bool
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization,
            such as partners, may use this parameter. If not specified, the organization from the OAuth token is used.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body: dict[str, Any] = dict()
        body['enabled'] = enabled
        url = self.f_ep(entity_id)
        super().put(url, params=params, json=body)

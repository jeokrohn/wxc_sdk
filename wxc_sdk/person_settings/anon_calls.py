from wxc_sdk.person_settings.common import PersonSettingsApiChild

__all__ = ['AnonCallsApi']


class AnonCallsApi(PersonSettingsApiChild):
    """
    API for anonymous call reject settings; so far only used for workspaces
    """

    feature = 'anonymousCallReject'

    def read(self, entity_id: str, org_id: str = None) -> bool:
        """
        Retrieve Anonymous Call Settings for an entity.

        Anonymous Call Rejection, when enabled, blocks all incoming calls from unidentified or blocked caller IDs.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: bool
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id)
        data = super().get(url, params=params)
        r = data['enabled']
        return r

    def configure(self, entity_id: str, enabled: bool, org_id: str = None):
        """
        Modify Anonymous Call Settings for an entity.

        Anonymous Call Rejection, when enabled, blocks all incoming calls from unidentified or blocked caller IDs.

        **NOTE**: This API is only available for professional licensed workspaces.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param enabled: `true` if the Anonymous Call Rejection feature is enabled.
        :type enabled: bool
        :param org_id: ID of the organization within which the entity resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the
            token used to access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.f_ep(entity_id)
        super().put(url, params=params, json=body)

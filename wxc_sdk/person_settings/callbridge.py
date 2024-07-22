from wxc_sdk.base import ApiModel
from wxc_sdk.person_settings.common import PersonSettingsApiChild

__all__ = ['CallBridgeApi', 'CallBridgeSetting']


class CallBridgeSetting(ApiModel):
    #: Set to enable or disable a stutter dial tone being played to all the participants
    #: when a person is bridged on the active shared line call.
    warning_tone_enabled: bool


class CallBridgeApi(PersonSettingsApiChild):
    """
    User Call Settings with Call Bridge Feature

    Also used for virtual lines

    Not supported for Webex for Government (FedRAMP)

    Person Call Settings supports modifying Webex Calling settings for a specific person.

    Viewing People requires a full, user, or read-only administrator auth token with a scope
    of `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by a
    person to read their own settings.

    Configuring People settings requires a full or user administrator auth token with the `spark-admin:people_write`
    scope or, for select APIs, a user auth token with `spark:people_write` scope can be used by a person to update
    their own settings.
    """

    feature = 'callBridge'

    def read(self, entity_id: str, org_id: str = None) -> CallBridgeSetting:
        """
        Read Call Bridge Settings

        Retrieve Bridge settings.

        This API requires a full, user or read-only administrator or location administrator auth token with a scope
        of `spark-admin:people_read`.

        :param entity_id: Unique identifier for the person.
        :type entity_id: str
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: :class:'CallBridgeSetting'
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.f_ep(entity_id)
        data = super().get(url, params=params)
        return CallBridgeSetting.model_validate(data)

    def configure(self, entity_id: str, setting: CallBridgeSetting,
                  org_id: str = None):
        """
        Configure Call Bridge Settings

        Configure Call Bridge settings.

        This API requires a full or user administrator or location administrator auth token with
        the `spark-admin:people_write` scope.

        :param entity_id: Unique identifier for the person.
        :type entity_id: str
        :param setting: new call bridge settings
        :type setting: :class:'CallBridgeSetting'
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = setting.model_dump(mode='json', exclude_none=True, by_alias=True)
        url = self.f_ep(entity_id)
        super().put(url, params=params, json=body)

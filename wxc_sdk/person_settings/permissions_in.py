"""
Person incoming permissions API
"""

from .common import PersonSettingsApiChild
from ..base import ApiModel
from ..base import SafeEnum as Enum

__all__ = ['ExternalTransfer', 'IncomingPermissions', 'IncomingPermissionsApi']


class ExternalTransfer(str, Enum):
    """
    Specifies the transfer behavior for incoming, external calls.
    """
    #: Allow transfer and forward for all external calls including those which were transferred.
    allow_all_external = 'ALLOW_ALL_EXTERNAL'
    #: Only allow transferred calls to be transferred or forwarded and disallow transfer of other external calls.
    allow_only_transferred_external = 'ALLOW_ONLY_TRANSFERRED_EXTERNAL'
    #: Block all external calls from being transferred or forwarded.
    block_all_external = 'BLOCK_ALL_EXTERNAL'


class IncomingPermissions(ApiModel):
    """
    Person's Incoming Permission Settings
    """
    #: When true, indicates that this person uses the specified calling permissions for receiving inbound calls rather
    #: than the organizational defaults.
    use_custom_enabled: bool
    #: Specifies the transfer behavior for incoming, external calls.
    external_transfer: ExternalTransfer
    #: Internal calls are allowed to be received.
    internal_calls_enabled: bool
    #: Collect calls are allowed to be received.
    collect_calls_enabled: bool

    @staticmethod
    def allow_all() -> 'IncomingPermissions':
        """
        allow everything

        :return: :class:`IncomingPermissions`
        """
        return IncomingPermissions(use_custom_enabled=True,
                                   external_transfer=ExternalTransfer.allow_all_external,
                                   internal_calls_enabled=True, collect_calls_enabled=True)

    @staticmethod
    def default() -> 'IncomingPermissions':
        """
        default settings

        :return: :class:`IncomingPermissions`
        """
        return IncomingPermissions(use_custom_enabled=False,
                                   external_transfer=ExternalTransfer.allow_all_external,
                                   internal_calls_enabled=True, collect_calls_enabled=True)


class IncomingPermissionsApi(PersonSettingsApiChild):
    """
    API for incoming permissions settings

    Also used for virtual lines, workspaces
    """

    feature = 'incomingPermission'

    def read(self, entity_id: str, org_id: str = None) -> IncomingPermissions:
        """
        Read Incoming Permission Settings

        Retrieve Incoming Permission Settings

        You can change the incoming calling permissions for an entity if you want them to be different from your
        organization's default.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param org_id: entity is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: incoming permission settings for specific user
        :rtype: :class:`IncomingPermissions`
        """
        ep = self.f_ep(person_id=entity_id)
        params = org_id and {'orgId': org_id} or None
        return IncomingPermissions.model_validate(self.get(ep, params=params))

    def configure(self, entity_id: str, settings: IncomingPermissions, org_id: str = None):
        """
        Configure incoming permissions settings

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by an entity to update their own settings.

        :param entity_id: Unique identifier for the entity.
        :type entity_id: str
        :param settings: new setting to be applied
        :type settings: :class:`IncomingPermissions`
        :param org_id: entity is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=entity_id)
        params = org_id and {'orgId': org_id} or None
        self.put(ep, params=params, data=settings.model_dump_json())

from collections.abc import Generator
from typing import Optional

from .forwarding import ForwardingApi, FeatureSelector
from .hg_and_cq import HGandCQ, Policy
from ..api_child import ApiChild
from ..base import ApiModel, to_camel
from ..common import AlternateNumber
from ..rest import RestSession

__all__ = ['NoAnswer', 'BusinessContinuity', 'HGCallPolicies', 'HuntGroup', 'HuntGroupApi']


class NoAnswer(ApiModel):
    """
    Settings for when the call into the hunt group is not answered.
    """
    #: If enabled, advance to next agent after the next_agent_rings has occurred.
    next_agent_enabled: Optional[bool]
    #: Number of rings before call will be forwarded if unanswered and nextAgentEnabled is true.
    next_agent_rings: Optional[int]
    #: If true, forwards unanswered calls to the destination after the number of rings occurs.
    forward_enabled: Optional[bool]
    #: Destination if forward_enabled is True.
    destination: Optional[str]
    #: Number of rings before forwarding calls if forward_enabled is true.
    number_of_rings: Optional[int]
    #: System-wide maximum number of rings allowed for number_of_rings setting.
    system_max_number_of_rings: Optional[int]
    #: If destination_voicemail_enabled is true, enables and disables sending incoming to destination number's
    #: voicemail if the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool]

    @staticmethod
    def default() -> 'NoAnswer':
        return NoAnswer(destination_voicemail_enabled=False,
                        forward_enabled=False,
                        next_agent_enabled=False,
                        next_agent_rings=5,
                        number_of_rings=15,
                        system_max_number_of_rings=20)


class BusinessContinuity(ApiModel):
    """
    Settings for sending calls to a destination of your choice if your phone is not connected to the network for any
    reason, such as power outage, failed Internet connection, or wiring problem
    """
    #: Divert calls when unreachable, unanswered calls divert to a defined phone number. This could apply to phone
    #: calls that aren't answered due to a network outage, or all agents of the hunt group are busy and the Advance
    #: when the busy option is also enabled. For persons only using a mobile device, calls won't be diverted, if there
    #: is a network outage.
    enabled: Optional[bool]
    #: Destination for Business Continuity.
    destination: Optional[str]
    #: Indicates enabled or disabled state of sending diverted incoming calls to the destination number's voicemail if
    #: the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool]

    @staticmethod
    def default() -> 'BusinessContinuity':
        return BusinessContinuity(enabled=False,
                                  destination_voicemail_enabled=False)


class HGCallPolicies(ApiModel):
    """
    Policy controlling how calls are routed to agents.
    """
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[Policy]
    #: If false, then the option is treated as "Advance when busy": the hunt group won’t ring agents when they’re on
    #: a call and will advance to the next agent. If a hunt group agent has call waiting enabled and the call is
    #: advanced to them, then the call will wait until that hunt group agent isn’t busy.
    waiting_enabled: Optional[bool]
    #: Settings for when the call into the hunt group is not answered.
    no_answer: Optional[NoAnswer]
    #: Settings for sending calls to a destination of your choice if your phone is not connected to the network for
    #: any reason, such as power outage, failed Internet connection, or wiring problem.
    business_continuity: Optional[BusinessContinuity]

    @staticmethod
    def default() -> 'HGCallPolicies':
        return HGCallPolicies(policy=Policy.circular,
                              waiting_enabled=False,
                              no_answer=NoAnswer.default(),
                              business_continuity=BusinessContinuity.default())


class HuntGroup(HGandCQ):
    """
    The huntgroup object
    """
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a hunt group. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the hunt group.
    alternate_numbers: Optional[list[AlternateNumber]]
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[HGCallPolicies]

    @staticmethod
    def exclude_update_or_create() -> dict:
        """
        Exclude dict for update or create calls
        :return: dict
        :meta private:
        """
        base_exclude = HGandCQ.exclude_update_or_create()
        base_exclude.update({'call_policies':
                                 {'no_answer': {'system_max_number_of_rings': True}},
                             'alternate_numbers':
                                 {'__all__':
                                      {'toll_free_number': True}}})
        return base_exclude

    @staticmethod
    def create(name: str, extension: str = None, phone_number: str = None) -> 'HuntGroup':
        """
        Get minimal hunt group settings that can be used to create a hunt group by
        calling :meth:`HuntGroupApi.create` with these settings. The hunt group will not have any agents.

        :param name: Unique name
        :type name: str
        :param extension: Extension
        :type extension: str
        :param phone_number: Primary phone number
        :type phone_number: str
        :return: :class:`HuntGroup` instance
        """
        if not any((extension, phone_number)):
            raise ValueError('at least one of phone_number or extension has to be set')
        return HuntGroup(name=name,
                         phone_number=phone_number,
                         extension=extension)


class HuntGroupApi(ApiChild, base='telephony/config/huntGroups'):
    """
    Hunt Group API

    :ivar forwarding: hunt group forwarding API :class:`wxc_sdk.telephony.forwarding.ForwardingApi`
    """

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.forwarding = ForwardingApi(session=session, feature_selector=FeatureSelector.huntgroups)

    def _endpoint(self, *, location_id: str = None, huntgroup_id: str = None) -> str:
        """
        hunt group specific feature endpoint like /v1/telephony/config/locations/{locationId}/huntGroups/{huntGroupId}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param huntgroup_id: schedule id
        :type huntgroup_id: str
        :return: full endpoint
        :rtype: str
        """
        if location_id is None:
            return self.session.ep('telephony/config/huntGroups')
        else:
            ep = self.session.ep(f'telephony/config/locations/{location_id}/huntGroups')
            if huntgroup_id:
                ep = f'{ep}/{huntgroup_id}'
            return ep

    def list(self, org_id: str = None, location_id: str = None, name: str = None,
             phone_number: str = None, **params) -> Generator[HuntGroup, None, None]:
        """
        Read the List of Hunt Groups
        List all calling Hunt Groups for the organization.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        List all calling Hunt Groups for the organization.
        :param org_id: List hunt groups for this organization.
        :param location_id: Only return hunt groups with matching location ID.
        :param name: Only return hunt groups with the matching name.
        :param phone_number: Only return hunt groups with the matching primary phone number or extension.
        :return: yields :class:`HuntGroup` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=HuntGroup, params=params)

    def by_name(self, name: str, location_id: str = None, org_id: str = None) -> Optional[HuntGroup]:
        """
        Get hunt group info by name
        :param location_id:
        :param name:
        :param org_id:
        :return:
        """
        return next((hg for hg in self.list(name=name, location_id=location_id, org_id=org_id)
                     if hg.name == name), None)

    def create(self, location_id: str, settings: HuntGroup, org_id: str = None) -> str:
        """
        Create a Hunt Group

        Create new Hunt Groups for the given location.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Creating a hunt group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the hunt group for the given location.
        :type location_id: str
        :param settings: hunt group details
        :type settings: :class:`HuntGroup`
        :param org_id: Create the hunt group for this organization.
        :type org_id: str
        :return: ID of the newly created hunt group.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or {}
        settings.call_policies = settings.call_policies or HGCallPolicies().default()
        data = settings.create_or_update()
        url = self._endpoint(location_id=location_id)
        data = self.post(url, data=data, params=params)
        return data['id']

    def delete_huntgroup(self, location_id: str, huntgroup_id: str, org_id: str = None):
        """
        Delete a Hunt Group

        Delete the designated Hunt Group.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Deleting a hunt group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a hunt group.
        :type location_id: str
        :param huntgroup_id: Delete the hunt group with the matching ID.
        :type huntgroup_id: str
        :param org_id: Delete the hunt group with the matching ID.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, huntgroup_id=huntgroup_id)
        self.delete(url, params=params)

    def details(self, location_id: str, huntgroup_id: str, org_id: str = None) -> HuntGroup:
        """
        Get Details for a Hunt Group

        Retrieve Hunt Group details.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Retrieving hunt group details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a hunt group in this location.
        :type location_id: str
        :param huntgroup_id: Retrieve settings for the hunt group with this identifier.
        :type huntgroup_id: str
        :param org_id: Retrieve hunt group settings from this organization.
        :type org_id: str
        :return: hunt group details
        """
        url = self._endpoint(location_id=location_id, huntgroup_id=huntgroup_id)
        params = org_id and {'orgId': org_id} or {}
        data = self.get(url, params=params)
        result = HuntGroup.parse_obj(data)
        return result

    def update(self, location_id: str, huntgroup_id: str, update: HuntGroup,
                         org_id: str = None):
        """
        Update a Hunt Group

        Update the designated Hunt Group.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Updating a hunt group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Update the hunt group for this location.
        :type location_id: str
        :param huntgroup_id: Update setting for the hunt group with the matching ID.
        :type huntgroup_id: str
        :param update: hunt group settings
        :type update: :class:`HuntGroup`
        :param org_id: Update hunt group settings from this organization.
        """
        params = org_id and {'orgId': org_id} or None
        # TODO: file documentation defect
        #   https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/update-a-hunt-group shows
        #   distinctiveRing and alternateNumbers as direct members while they actually are childs of
        #   alternateNumberSettings
        data = update.create_or_update()
        url = self._endpoint(location_id=location_id, huntgroup_id=huntgroup_id)
        self.put(url, data=data, params=params)

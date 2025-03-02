import logging
from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional, List

from .forwarding import ForwardingApi, FeatureSelector
from .hg_and_cq import HGandCQ, Policy
from ..api_child import ApiChild
from ..base import ApiModel, to_camel
from ..common import AlternateNumber
from ..person_settings.available_numbers import AvailableNumber
from ..rest import RestSession

__all__ = ['NoAnswer', 'BusinessContinuity', 'HGCallPolicies', 'HuntGroup', 'HuntGroupApi']

log = logging.getLogger(__name__)


class NoAnswer(ApiModel):
    """
    Settings for when the call into the hunt group is not answered.
    """
    #: If enabled, advance to next agent after the next_agent_rings has occurred.
    next_agent_enabled: Optional[bool] = None
    #: Number of rings before call will be forwarded if unanswered and nextAgentEnabled is true.
    next_agent_rings: Optional[int] = None
    #: If `true`, forwards unanswered calls to the destination after the number of rings occurs.
    forward_enabled: Optional[bool] = None
    #: Destination if forward_enabled is True.
    destination: Optional[str] = None
    #: Number of rings before forwarding calls if forward_enabled is true.
    number_of_rings: Optional[int] = None
    #: System-wide maximum number of rings allowed for number_of_rings setting.
    system_max_number_of_rings: Optional[int] = None
    #: If `forwardEnabled` is true, enables and disables sending incoming to destination number's voicemail if the
    #: destination is an internal phone number and that number has the voicemail service enabled. If
    #: `destinationVoicemailEnabled` is enabled, then *55 is added as a prefix for `destination`.
    destination_voicemail_enabled: Optional[bool] = None

    @staticmethod
    def default() -> 'NoAnswer':
        return NoAnswer(destination_voicemail_enabled=False,
                        forward_enabled=False,
                        next_agent_enabled=False,
                        next_agent_rings=5,
                        number_of_rings=15,
                        system_max_number_of_rings=20)


class BusinessContinuity(ApiModel):
    enabled: Optional[bool] = None
    #: Destination
    destination: Optional[str] = None
    #: Indicates enabled or disabled state of sending diverted incoming calls to the destination number's voicemail if
    #: the destination is an internal phone number and that number has the voicemail service enabled.
    destination_voicemail_enabled: Optional[bool] = None

    @staticmethod
    def default() -> 'BusinessContinuity':
        return BusinessContinuity(enabled=False,
                                  destination_voicemail_enabled=False)


class HGCallPolicies(ApiModel):
    """
    Policy controlling how calls are routed to agents.
    """
    #: Call routing policy to use to dispatch calls to agents.
    policy: Optional[Policy] = None
    #: If false, then the option is treated as "Advance when busy": the hunt group won’t ring agents when they’re on
    #: a call and will advance to the next agent. If a hunt group agent has call waiting enabled and the call is
    #: advanced to them, then the call will wait until that hunt group agent isn’t busy.
    waiting_enabled: Optional[bool] = None
    #: If `true`, the hunt group busy status will be set to busy. All new calls will get busy treatment. If
    #: `busyRedirect` is enabled, the calls are routed to the destination specified in `busyRedirect`.
    group_busy_enabled: Optional[bool] = None
    #: If true, agents can change the hunt group busy status.
    allow_members_to_control_group_busy_enabled: Optional[bool] = None
    #: Settings for when the call into the hunt group is not answered.
    no_answer: Optional[NoAnswer] = None
    #: Settings for sending calls to a specified destination when all agents are busy or when the hunt group busy
    #: status is set to busy.
    busy_redirect: Optional[BusinessContinuity] = None
    #: Settings for sending calls to a specified destination if the phone is not connected to the network for any
    #: reason, such as a power outage, failed internet connection, or wiring problem.
    business_continuity_redirect: Optional[BusinessContinuity] = None

    @staticmethod
    def default() -> 'HGCallPolicies':
        return HGCallPolicies(policy=Policy.circular,
                              waiting_enabled=False,
                              no_answer=NoAnswer.default(),
                              busy_redirect=BusinessContinuity.default(),
                              business_continuity_redirect=BusinessContinuity.default())


class HuntGroup(HGandCQ):
    """
    The huntgroup object
    """
    #: The alternate numbers feature allows you to assign multiple phone numbers or extensions to a hunt group. Each
    #: number will reach the same greeting and each menu will function identically to the main number. The alternate
    #: numbers option enables you to have up to ten (10) phone numbers ring into the hunt group.
    alternate_numbers: Optional[list[AlternateNumber]] = None
    #: Policy controlling how calls are routed to agents.
    call_policies: Optional[HGCallPolicies] = None
    #: Whether or not the hunt group can be used as the caller ID when the agent places outgoing calls.
    hunt_group_caller_id_for_outgoing_calls_enabled: Optional[bool] = None

    @staticmethod
    def exclude_update_or_create() -> dict:
        """
        Exclude dict for update or create calls

        :meta private:
        :return: dict
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

    def create_or_update(self) -> dict:
        """
        Get data for create or update

        :meta private:
        """
        data = super().create_or_update()
        return data


@dataclass(init=False, repr=False)
class HuntGroupApi(ApiChild, base='telephony/config/huntGroups'):
    """
    Hunt Group API
    """
    forwarding: ForwardingApi

    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.forwarding = ForwardingApi(session=session, feature_selector=FeatureSelector.huntgroups)

    def _endpoint(self, *, location_id: str = None, huntgroup_id: str = None, path: str = None) -> str:
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
            if path:
                ep = f'{ep}/{path}'
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
        data = self.post(url, json=data, params=params)
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
        result = HuntGroup.model_validate(data)
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
        data = update.create_or_update()
        url = self._endpoint(location_id=location_id, huntgroup_id=huntgroup_id)
        self.put(url, json=data, params=params)

    def primary_available_phone_numbers(self, location_id: str, phone_number: List[str] = None,
                                        org_id: str = None,
                                        **params) -> Generator[AvailableNumber, None, None]:
        """
        Get Hunt Group Primary Available Phone Numbers

        List service and standard numbers that are available to be assigned as the hunt group's primary phone number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self._endpoint(location_id=location_id, path='availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def alternate_available_phone_numbers(self, location_id: str, phone_number: List[str] = None,
                                          org_id: str = None,
                                          **params) -> Generator[AvailableNumber, None, None]:
        """
        Get Hunt Group Alternate Available Phone Numbers

        List service and standard numbers that are available to be assigned as the hunt group's alternate phone number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        unassigned.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        url = self._endpoint(location_id=location_id, path='alternate/availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

    def forward_available_phone_numbers(self, location_id: str, phone_number: List[str] = None,
                                        owner_name: str = None, extension: str = None,
                                        org_id: str = None,
                                        **params) -> Generator[AvailableNumber, None, None]:
        """
        Get Hunt Group Call Forward Available Phone Numbers

        List service and standard numbers that are available to be assigned as the hunt group's call forward number.
        These numbers are associated with the location specified in the request URL, can be active or inactive, and are
        assigned to an owning entity.

        The available numbers APIs help identify candidate numbers and their owning entities to simplify the assignment
        or association of these numbers to members or features.

        Retrieving this list requires a full, read-only or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Return the list of phone numbers for this location within the given organization. The
            maximum length is 36.
        :type location_id: str
        :param phone_number: Filter phone numbers based on the comma-separated list provided in the `phoneNumber`
            array.
        :type phone_number: list[str]
        :param owner_name: Return the list of phone numbers that are owned by the given `ownerName`. Maximum length is
            255.
        :type owner_name: str
        :param extension: Returns the list of PSTN phone numbers with the given `extension`.
        :type extension: str
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: Generator yielding :class:`AvailableNumber` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        if phone_number is not None:
            params['phoneNumber'] = ','.join(phone_number)
        if owner_name is not None:
            params['ownerName'] = owner_name
        if extension is not None:
            params['extension'] = extension
        url = self._endpoint(location_id=location_id, path='callForwarding/availableNumbers')
        return self.session.follow_pagination(url=url, model=AvailableNumber, item_key='phoneNumbers', params=params)

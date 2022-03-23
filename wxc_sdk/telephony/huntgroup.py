
from collections.abc import Generator
from typing import Optional, List

from pydantic import Field

from .hg_and_cq import HGandCQ, AlternateNumber, Policy, Agent, AlternateNumberSettings, ForwardingAPI, \
    FeatureSelector
from ..api_child import ApiChild
from ..base import ApiModel, to_camel
from ..rest import RestSession

__all__ = ['HuntGroupAPI', 'AlternateNumber', 'Policy', 'Agent', 'AlternateNumberSettings', 'HuntGroup',
           'HuntGroupDetail']


class HuntGroup(HGandCQ):
    """
    The huntgroup object
    """
    pass


class NoAnswer(ApiModel):
    next_agent_enabled: Optional[bool]
    next_agent_rings: Optional[int]
    forward_enabled: Optional[bool]
    destination: Optional[str]
    number_of_rings: Optional[int]
    system_max_number_of_rings: Optional[int]
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
    enabled: Optional[bool]
    destination: Optional[str]
    destination_voicemail_enabled: Optional[bool]

    @staticmethod
    def default() -> 'BusinessContinuity':
        return BusinessContinuity(enabled=False,
                                  destination_voicemail_enabled=False)


class CallPolicies(ApiModel):
    policy: Optional[Policy]
    waiting_enabled: Optional[bool]
    no_answer: Optional[NoAnswer]
    business_continuity: Optional[BusinessContinuity]

    @staticmethod
    def default() -> 'CallPolicies':
        return CallPolicies(policy=Policy.circular,
                            waiting_enabled=False,
                            no_answer=NoAnswer.default(),
                            business_continuity=BusinessContinuity.default())


class HuntGroupDetail(HGandCQ):
    # these two attributes are used in details and update calls
    # distinctive_ring: bool = Field(default=False)   # used in details, update only
    # alternate_numbers: List[AlternateNumber] = Field(default_factory=list)  # used in details, update only

    # in create() calls this object replaces the distinctive_ring and alternate_numbers attributes
    alternate_number_settings: Optional[AlternateNumberSettings]  # used for create() only in details

    language: Optional[str]
    language_code: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    time_zone: Optional[str]
    call_policies: Optional[CallPolicies]
    agents: List[Agent] = Field(default_factory=list)

    @staticmethod
    def create(name: str,
               agents: List[Agent],
               enabled: bool,
               phone_number: str = None,
               extension: str = None,
               language_code: str = None,
               first_name: str = None,
               last_name: str = None,
               time_zone: str = None,
               call_policies: CallPolicies = None) -> 'HuntGroupDetail':
        """
        Gwt a HuntGroupDetail instance for huntgroup creation
        :param name: Unique name for the hunt group.
        :param agents: People, including workspaces, that are eligible to receive calls. (ID and weight only)
        :param enabled: Whether or not the hunt group is enabled.
        :param phone_number: Primary phone number of the hunt group.
        :param extension: Primary phone extension of the hunt group.
        :param language_code: Language code.
        :param first_name: First name to be shown when calls are forwarded out of this hunt group. Defaults to ".".
        :param last_name: Last name to be shown when calls are forwarded out of this hunt group. Defaults to the phone
        number if set, otherwise defaults to call group name.
        :param time_zone: Time zone for the hunt group.
        :param call_policies: Policy controlling how calls are routed to agents.
        :return:
        """
        if not (phone_number or extension):
            raise ValueError('One of phone_number and extension has to be given')
        params = {k: v for k, v in locals().items()
                  if v is not None and k != 'queue_size'}
        return HuntGroupDetail(**params)


class HuntGroupAPI(ApiChild, base='telephony/config/huntGroups'):
    """

    """
    def __init__(self, session: RestSession):
        super().__init__(session=session)
        self.forwarding = ForwardingAPI(session=session, feature_selector=FeatureSelector.huntgroups)

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
             phone_number: str = None) -> Generator[HuntGroup, None, None]:
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
        :return:
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i and v is not None}
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=HuntGroup,params=params)

    def by_name(self, name: str, location_id: str = None, org_id: str = None) -> Optional[HuntGroup]:
        """
        Get hunt group info by name
        :param location_id:
        :param name:
        :param org_id:
        :return:
        """
        return next((hg for hg in self.list(name=name, location_id=location_id, org_id=org_id)
                     if hg.name==name), None)

    def create(self, location_id: str, huntgroup: HuntGroupDetail, org_id: str = None) -> str:
        """
        Create a Hunt Group
        Create new Hunt Groups for the given location.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Creating a hunt group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the hunt group for the given location.
        :type location_id: str
        :param huntgroup: hunt group details
        :type huntgroup: HuntGroup
        :param org_id: Create the hunt group for this organization.
        :type org_id: str
        :return: ID of the newly created hunt group.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or {}
        huntgroup.call_policies = huntgroup.call_policies or CallPolicies().default()
        hg_data = huntgroup.json()
        url = self._endpoint(location_id=location_id)
        data = self.post(url, data=hg_data, params=params)
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
        url = self._endpoint(location_id=location_id, huntgroup_id=huntgroup_id)
        self.delete(url)

    def details(self, location_id: str, huntgroup_id: str, org_id: str = None) -> HuntGroupDetail:
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
        result = HuntGroupDetail.parse_obj(data)
        return result

    def update_huntgroup(self, location_id: str, huntgroup_id: str, huntgroup: HuntGroupDetail,
                               org_id: str = None):
        """

        :param location_id: Update the hunt group for this location.
        :type location_id: str
        :param huntgroup_id: Update setting for the hunt group with the matching ID.
        :type huntgroup_id: str
        :param huntgroup: hunt group settings
        :type huntgroup: HuntGroupDetail
        :param org_id: Update hunt group settings from this organization.
        """
        params = org_id and {'orgId': org_id} or None
        # TODO: determine actual list of attributes to exclude/include
        hg_data = huntgroup.json(include={'enabled', 'name', 'phone_number', 'extension', 'distinctive_ring',
                                          'alternate_numbers', 'language_code', 'first_name', 'last_name',
                                          'time_zone', 'call_policies', 'agents'})
        url = self._endpoint(location_id=location_id, huntgroup_id=huntgroup_id)
        self.put(url, data=hg_data, params=params)


"""
API to manage call queue agent caller ID information
"""
import json
from typing import Optional

from pydantic import model_validator, TypeAdapter

from .common import PersonSettingsApiChild
from ..base import ApiModel
from ..base import SafeEnum as Enum

__all__ = ['AvailableCallerIdType', 'AgentCallerId', 'AgentCallerIdApi']


class AvailableCallerIdType(str, Enum):
    #: A call queue has been selected for the agent's caller ID.
    call_queue = 'CALL_QUEUE'
    #: A hunt group has been selected for the agent's caller ID.
    hunt_group = 'HUNT_GROUP'


class AgentCallerId(ApiModel):
    #: Call queue or hunt group's unique identifier.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvMjE3ZDU3YmEtOTMxYi00ZjczLTk1Y2EtOGY3MWFhYzc4MTE5
    id: Optional[str] = None
    #: Member is of type `CALL_QUEUE` or `HUNT_GROUP`
    #: example: CALL_QUEUE
    type: Optional[AvailableCallerIdType] = None
    #: Call queue or hunt group's name.
    #: example: TestCallQueue
    name: Optional[str] = None
    #: When not null, it is call queue or hunt group's phone number.
    #: example: +441234200090
    phone_number: Optional[str] = None
    #: When not null, it is call queue or hunt group's extension number.
    #: example: 6001
    extension: Optional[str] = None


class QueueCallerId(ApiModel):
    """
    call queue agent's Caller ID information
    """
    #: When true, indicates that this agent is using the selectedQueue for its Caller ID. When false, indicates that
    #: it is using the agent's configured Caller ID.
    queue_caller_id_enabled: Optional[bool] = None
    #: It is empty object when queueCallerIdEnabled is false. When queueCallerIdEnabled is true this data must be
    #: populated
    selected_queue: Optional[AgentCallerId] = None

    @model_validator(mode='before')
    def root(cls, values):
        """

        :meta private

        if no agent caller id is configured API returns a selectedQueue with id == None. In that case we pop the
        queue so that instead selectedQueue == None
        """
        if values.get('selectedQueue'):
            if 'id' in values['selectedQueue'] and values['selectedQueue']['id'] is None:
                values.pop('selectedQueue')
        return values

    def for_update(self) -> str:
        """
        JSON string for updates

        :meta private:
        """
        data = self.model_dump(include={'queue_caller_id_enabled': True,
                                        'selected_queue': {'id', 'name'}
                                        },
                               by_alias=True)
        if not self.queue_caller_id_enabled:
            # apparently selectedQueue is still mandatory even if we try to disable agent caller id
            data['selectedQueue'] = {'id': None}
        return json.dumps(data)


class AgentCallerIdApi(PersonSettingsApiChild):
    """
    API to manage agent caller id settings

    Also used for virtual lines
    """
    feature = 'agent'

    def available_caller_ids(self, entity_id: str, org_id: str = None) -> list[AgentCallerId]:
        """
        Retrieve Agent's List of Available Caller IDs

        Get the list of call queues and hunt groups available for caller ID use by this person, virtual line, or
        workspace as an agent.

        This API requires a full, user, or read-only administrator or location administrator auth token with a scope
        of `spark-admin:people_read`.

        :param entity_id: Unique identifier for the person, virtual line, or workspace.
        :type entity_id: str
        :param org_id: ID of the organization in which the entity resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access API.
        :type org_id: str
        :rtype: list[AvailableCallerIdObject]
        """
        ep = self.f_ep(entity_id, 'availableCallerIds')
        params = org_id and {'orgId': org_id} or None
        data = self.get(ep, params=params)
        return TypeAdapter(list[AgentCallerId]).validate_python(data['availableCallerIds'])

    def read(self, entity_id: str) -> AgentCallerId:
        """
        Retrieve Agent's Caller ID Information

        Retrieve the Agent's Caller ID Information.

        Each agent will be able to set their outgoing Caller ID as either the Call Queue's Caller ID, Hunt Group's
        Caller ID or their own configured Caller ID.

        This API requires a full admin or read-only administrator or location administrator auth token with a scope 
        of `spark-admin:telephony_config_read`.

        :param entity_id: Unique identifier for the person, virtual line, or workspace
        :type entity_id: str
        :rtype: AgentCallerId
        """
        url = self.f_ep(entity_id, 'callerId')
        data = super().get(url)
        r = AgentCallerId.model_validate(data['selectedCallerId'])
        return r
        
    def configure(self, entity_id: str, selected_caller_id: str = None):
        """
        Modify Agent's Caller ID Information.

        Each Agent will be able to set their outgoing Caller ID as either the designated Call Queue's Caller ID or Hunt
        Group's Caller ID or their own configured Caller ID

        This API requires a full or user administrator or location administrator auth token with
        the `spark-admin:telephony_config_write` scope.

        :param entity_id: Unique identifier for the person, virtual line, or workspace
        :type entity_id: str
        :param selected_caller_id: The unique identifier of the call queue or hunt group to use for the agent's caller
            ID. Set to null to use the agent's own caller ID.
        :type selected_caller_id: str
        :rtype: None
        """
        body = {'selectedCallerId': selected_caller_id}
        url = self.f_ep(entity_id, 'callerId')
        super().put(url, json=body)

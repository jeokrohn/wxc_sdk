"""
API to manage call queue agent caller ID information
"""
import json
from collections.abc import Generator
from typing import Optional

from pydantic import root_validator

from ..api_child import ApiChild
from ..base import ApiModel

__all__ = ['AgentQueue', 'QueueCallerId', 'AgentCallerIdApi']


class AgentQueue(ApiModel):
    """
    Available queue
    """
    #: Indicates the Call Queue's unique identifier.
    id: Optional[str]
    #: Indicates the Call Queue's name.
    name: Optional[str]
    #: When not null, indicates the Call Queue's phone number.
    phone_number: Optional[str]
    #: When not null, indicates the Call Queue's extension number.
    extension: Optional[str]


class QueueCallerId(ApiModel):
    """
    call queue agent's Caller ID information
    """
    #: When true, indicates that this agent is using the selectedQueue for its Caller ID. When false, indicates that
    #: it is using the agent's configured Caller ID.
    queue_caller_id_enabled: Optional[bool]
    #: It is empty object when queueCallerIdEnabled is false. When queueCallerIdEnabled is true this data must be
    #: populated
    selected_queue: Optional[AgentQueue]

    @root_validator(pre=True)
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
        data = self.dict(include={'queue_caller_id_enabled': True,
                                  'selected_queue': {'id', 'name'}
                                  },
                         by_alias=True)
        if not self.queue_caller_id_enabled:
            # apparently selectedQueue is still mandatory even if we try to disable agent caller id
            data['selectedQueue'] = {'id': None}
        return json.dumps(data)


class AgentCallerIdApi(ApiChild, base='telephony/config/people'):
    """
    API to manage call queue agent caller ID information
    """

    # noinspection PyMethodOverriding
    def ep(self, person_id: str, path: str):
        """
        :meta private:
        """
        return super().ep(f'{person_id}/queues/{path}')

    def available_queues(self, person_id: str, org_id: str = None) -> Generator[AgentQueue, None, None]:
        """
        Retrieve the list of the person's available call queues and the associated Caller ID information

        If the Agent is to enable queueCallerIdEnabled, they must choose which queue to use as the source for
        outgoing Caller ID. This API returns a list of Call Queues from which the person must select. If this setting
        is disabled or Agent does not belong to any queue this list will be empty.

        This API requires a full admin or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: organization id
        :type org_id: str
        :return: yields person's available call queues and the associated Caller ID information
        :rtype: Generator[AgentQueue, None, None]
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(person_id=person_id, path='availableCallerIds')
        return self.session.follow_pagination(url=url, model=AgentQueue, params=params, item_key='availableQueues')

    def read(self, person_id: str, org_id: str = None) -> QueueCallerId:
        """
        Retrieve a call queue agent's Caller ID information

        Each agent in the Call Queue will be able to set their outgoing Caller ID as either the Call Queue's phone
        number or their own configured Caller ID. This API fetches the configured Caller ID for the agent in the system.

        This API requires a full admin or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: organization id
        :type org_id: str
        :return: call queue agent's Caller ID information
        :rtype: QueueCallerId
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(person_id=person_id, path='callerId')
        data = self.get(url=url, params=params)
        return QueueCallerId.parse_obj(data)

    def update(self, person_id: str, update: QueueCallerId, org_id: str = None):
        """
        Modify a call queue agent's Caller ID information

        Each Agent in the Call Queue will be able to set their outgoing Caller ID as either the designated Call
        Queue's phone number or their own configured Caller ID. This API modifies the configured Caller ID for the
        agent in the system.

        This API requires a full or user administrator auth token with the spark-admin:telephony_config_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param update: new settings
        :type update: QueueCallerId
        :param org_id: organization id
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(person_id=person_id, path='callerId')
        body = update.for_update()
        self.put(url=url, params=params, data=body)

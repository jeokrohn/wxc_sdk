#!/usr/bin/env python
"""
Overview of users, workspaces, and virtual lines in queues
"""
import asyncio
import logging
import os
from collections import defaultdict
from functools import reduce
from itertools import chain
from typing import Optional

from dotenv import load_dotenv

from wxc_sdk.tokens import Tokens
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import UserType
from wxc_sdk.integration import Integration
from wxc_sdk.people import Person
from wxc_sdk.scopes import parse_scopes
from wxc_sdk.telephony.callqueue import CallQueue
from wxc_sdk.telephony.hg_and_cq import Agent


def env_path() -> str:
    """
    determine path for .env to load environment variables from; based on name of this file
    :return: .env file path
    """
    return os.path.join(os.getcwd(), f'{os.path.splitext(os.path.basename(__file__))[0]}.env')


def yml_path() -> str:
    """
    determine path of YML file to persist tokens
    :return: path to YML file
    :rtype: str
    """
    return os.path.join(os.getcwd(), f'{os.path.splitext(os.path.basename(__file__))[0]}.yml')


def build_integration() -> Integration:
    """
    read integration parameters from environment variables and create an integration
    :return: :class:`wxc_sdk.integration.Integration` instance
    """
    client_id = os.getenv('INTEGRATION_CLIENT_ID')
    client_secret = os.getenv('INTEGRATION_CLIENT_SECRET')
    scopes = parse_scopes(os.getenv('INTEGRATION_SCOPES'))
    redirect_url = 'http://localhost:6001/redirect'
    if not all((client_id, client_secret, scopes)):
        raise ValueError('failed to get integration parameters from environment')
    return Integration(client_id=client_id, client_secret=client_secret, scopes=scopes,
                       redirect_url=redirect_url)


def get_tokens() -> Optional[Tokens]:
    """
    Tokens are read from a YML file. If needed an OAuth flow is initiated.

    :return: tokens
    :rtype: :class:`wxc_sdk.tokens.Tokens`
    """

    integration = build_integration()
    tokens = integration.get_cached_tokens_from_yml(yml_path=yml_path())
    return tokens


async def main():
    # get environment variables from .env; required for integration parameters
    load_dotenv(env_path())

    # get tokens from cache or create a new set of tokens using the integration defined in .env
    tokens = get_tokens()

    async with AsWebexSimpleApi(tokens=tokens) as api:
        # get calling users
        calling_users = [user for user in await api.people.list(calling_data=True)
                         if user.location_id]
        users_by_id: dict[str, Person] = {user.person_id: user for user in calling_users}

        # get all call queues
        queues = await api.telephony.callqueue.list()
        queues_by_id: dict[str, CallQueue] = {q.id: q for q in queues}

        # get all details
        queue_details: list[CallQueue] = await asyncio.gather(*[api.telephony.callqueue.details(
            location_id=q.location_id,
            queue_id=q.id) for q in queues])

        # group all queue members by member type
        AgentsByType = dict[UserType, list[str]]
        agents_by_type: AgentsByType

        def agents_by_type_reduce(reduced: AgentsByType, element: Agent) -> AgentsByType:
            reduced[element.user_type].append(element.agent_id)
            return reduced

        agents_by_type = reduce(agents_by_type_reduce,
                                chain.from_iterable(qd.agents for qd in queue_details),
                                defaultdict(list))
        # get details for all agent types
        # - people: api.people details
        # - place: api.workspace.details
        # - virtual line: api.telephony.virtual_lines.list()
        # TODO: ...

        user_queues: dict[str, list[str]] = defaultdict(list)
        for qd in queue_details:
            for member in qd.agents:
                if member.user_type == UserType.people:
                    user_queues[member.agent_id].append(qd.id)

        def q_str(queue_id: str) -> str:
            queue = queues_by_id[queue_id]
            return f'{queue.name}({queue.extension})'

        user_id_list = sorted(user_queues, key=lambda uid: users_by_id[uid].display_name)
        for user_id in user_id_list:
            queue_id_list = user_queues[user_id]
            user = users_by_id[user_id]
            print(f'{user.display_name}: {", ".join(q_str(qid) for qid in queue_id_list)}')


if __name__ == '__main__':
    # enable DEBUG logging to a file; REST log shows all requests
    logging.basicConfig(filename=os.path.join(os.getcwd(), f'{os.path.splitext(os.path.basename(__file__))[0]}.log'),
                        filemode='w', level=logging.DEBUG, format='%(asctime)s %(threadName)s %(message)s')
    asyncio.run(main())

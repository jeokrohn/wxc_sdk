#!/usr/bin/env python
"""
usage: queue_helper.py [-h] [--location LOCATION [LOCATION ...]] [--queue QUEUE [QUEUE ...]]
                       [--join JOIN_AGENT [JOIN_AGENT ...]] [--unjoin UNJOIN_AGENT [UNJOIN_AGENT ...]]
                       [--remove REMOVE_USER [REMOVE_USER ...]] [--add ADD_USER [ADD_USER ...]] [--dryrun]
                       [--token TOKEN]

Modify call queue settings from the CLI

optional arguments:
  -h, --help            show this help message and exit
  --location LOCATION [LOCATION ...], -l LOCATION [LOCATION ...]
                        name of location to work on. If missing then work on all locations.
  --queue QUEUE [QUEUE ...], -q QUEUE [QUEUE ...]
                        name(s) of queue(s) to operate on. If missing then work on all queues in location.
  --join JOIN_AGENT [JOIN_AGENT ...], -j JOIN_AGENT [JOIN_AGENT ...]
                        Join given user(s) on given queue(s). Can be "all" to act on all agents.
  --unjoin UNJOIN_AGENT [UNJOIN_AGENT ...], -u UNJOIN_AGENT [UNJOIN_AGENT ...]
                        Unjoin given agent(s) from given queue(s). Can be "all" to act on all agents.
  --remove REMOVE_USER [REMOVE_USER ...], -r REMOVE_USER [REMOVE_USER ...]
                        Remove given agent from given queue(s). Can be "all" to act on all agents.
  --add ADD_USER [ADD_USER ...], -a ADD_USER [ADD_USER ...]
                        Add given users to given queue(s).
  --dryrun, -d          Dry run; don't apply any changes
  --token TOKEN         admin access token to use
"""
import asyncio
import logging
import os
import sys
from argparse import ArgumentParser
from collections.abc import AsyncGenerator
from typing import Optional

from dotenv import load_dotenv

from wxc_sdk import Tokens
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.integration import Integration
from wxc_sdk.people import Person
from wxc_sdk.scopes import parse_scopes
from wxc_sdk.telephony.callqueue import CallQueue
from wxc_sdk.telephony.hg_and_cq import Agent


def agent_name(agent: Agent) -> str:
    return f'{agent.first_name} {agent.last_name}'


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
    async def act_on_queue(queue: CallQueue):
        """
        Act on a single queue
        """
        # we need the queue details b/c the queue instance passed as parameter is from a list() call
        # ... and thus is missing all the details like agents
        details = await api.telephony.callqueue.details(location_id=queue.location_id, queue_id=queue.id)
        agent_names = set(map(agent_name, details.agents))

        def notify(message: str) -> str:
            """
            an action notification with queue information
            """
            return f'queue "{details.name:{queue_len}}" in "{queue.location_name:{location_len}}": {message}'

        def validate_agents(names: list[str], operation: str) -> list[str]:
            """
            check if all names in given list exist as agents on current queue
            """
            if 'all' in names:
                return set(agent_names)

            not_found = [name for name in names if name not in agent_names]
            if not_found:
                print('\n'.join(notify(f'{name} not found for {operation}"')
                                for name in not_found),
                      file=sys.stderr)
            return set(name for name in names if name not in set(not_found))

        # validate list of names or join, unjoin, and remove against actual list of agents
        to_join = validate_agents(join_agents, 'join')
        to_unjoin = validate_agents(unjoin_agents, 'unjoin')
        to_remove = validate_agents(remove_users, 'remove')

        # check for agents we are asked to add but which already exist as agents on the queue
        existing_agent_ids = set(agent.agent_id for agent in details.agents)
        agent_exists = [agent_name(user) for user in add_users
                        if user.person_id in existing_agent_ids]
        if agent_exists:
            print('\n'.join(notify(f'{name} already is agent')
                            for name in agent_exists),
                  file=sys.stderr)
            # reduced set of users to add
            to_add = [user for user in add_users
                      if agent_name(user) not in set(agent_exists)]
        else:
            # ...  or add all users
            to_add = add_users

        # the updated list of agents for the current queue
        new_agents = []

        # do we actually need an update?
        update_needed = False

        # create copy of each agent instance; we don't want to update the original agent objects
        # to make sure that details still holds the state before any update
        agents = [agent.copy(deep=True) for agent in details.agents]

        # iterate through the existing agents and see if we have to apply any change
        for agent in agents:
            name = agent_name(agent)
            # do we have to take action to join this agent?
            if name in to_join and not agent.join_enabled:
                print(notify(f'{name}, join'))
                update_needed = True
                agent.join_enabled = True
            # do we have to take action to unjoin this agent?
            if name in to_unjoin and agent.join_enabled:
                print(notify(f'{name}, unjoin'))
                update_needed = True
                agent.join_enabled = False
            # do we have to remove this agent?
            if name in to_remove:
                print(notify(f'{name}, remove'))
                update_needed = True
                # skip to next agent; so that we don't add this agent to the updated list of agents
                continue
            new_agents.append(agent)

        # add new agents
        new_agents.extend(Agent(agent_id=user.person_id)
                          for user in to_add)

        # update the queue
        if (update_needed or to_add) and not args.dryrun:
            # simplified update: we only messed with the agents
            update = CallQueue(agents=new_agents)
            await api.telephony.callqueue.update(location_id=queue.location_id, queue_id=queue.id,
                                                 update=update)
            print(notify('queue updated'))
            # and get details after the update
            details = await api.telephony.callqueue.details(location_id=queue.location_id, queue_id=queue.id)
            print(notify('got details after update'))

        # print summary
        print(f'queue "{queue.name:{queue_len}}" in "{queue.location_name}"')
        print(f'  phone number: {details.phone_number}')
        print(f'  extension: {details.extension}')
        print('  agents')
        if details.agents:
            name_len = max(map(len, map(agent_name, details.agents)))
            for agent in details.agents:
                print(f'    {agent_name(agent):{name_len}}: {"not " if not agent.join_enabled else ""}joined')
        return

    async def validate_users(user_names: list[str]) -> AsyncGenerator[Person, None, None]:
        """
        Validate list of names of users to be added and yield a Person instance for each one
        """
        # search for all names in parallel
        lists: list[list[Person]] = await asyncio.gather(
            *[api.people.list(display_name=name) for name in user_names], return_exceptions=True)
        for name, user_list in zip(user_names, lists):
            if isinstance(user_list, Exception):
                user = None
            else:
                user = next((u for u in user_list if name == agent_name(u)), None)
            if user is None:
                print(f'user "{name}" not found', file=sys.stderr)
                continue
            yield user
        return

    # parse command line
    parser = ArgumentParser(description='Modify call queue settings from the CLI')
    parser.add_argument('--location', '-l', type=str, required=False, nargs='+',
                        help='name of location to work on. If missing then work on all locations.')

    parser.add_argument('--queue', '-q', type=str, required=False, nargs='+',
                        help='name(s) of queue(s) to operate on. If missing then work on all queues in location.')

    parser.add_argument('--join', '-j', type=str, required=False, nargs='+', dest='join_agent',
                        help='Join given user(s) on given queue(s). Can be "all" to act on all agents.')

    parser.add_argument('--unjoin', '-u', type=str, required=False, nargs='+', dest='unjoin_agent',
                        help='Unjoin given agent(s) from given queue(s). Can be "all" to act on all agents.')

    parser.add_argument('--remove', '-r', type=str, required=False, nargs='+', dest='remove_user',
                        help='Remove given agent from given queue(s). Can be "all" to act on all agents.')

    parser.add_argument('--add', '-a', type=str, required=False, nargs='+', dest='add_user',
                        help='Add given users to given queue(s).')
    parser.add_argument('--dryrun', '-d', required=False, action='store_true',
                        help='Dry run; don\'t apply any changes')
    parser.add_argument('--token', type=str, required=False, help='admin access token to use')

    args = parser.parse_args()

    # get environment variables from .env; required for integration parameters
    load_dotenv(env_path())

    tokens = args.token or None
    if tokens is None:
        # get tokens from cache or create a new set of tokens using the integration defined in .env
        tokens = get_tokens()

    async with AsWebexSimpleApi(tokens=tokens) as api:
        # validate location parameter
        location_names = args.location or []

        # list of all locations with names matching one of the provided names
        locations = [loc for loc in await api.locations.list()
                     if not location_names or loc.name in set(location_names)]

        if not location_names:
            print(f'Considering all {len(locations)} locations')

        # set of names of matching locations
        found_location_names = set(loc.name for loc in locations)

        # Error message for each location name argument not matching an actual location
        for location_name in location_names:
            if location_name not in found_location_names:
                print(f'location "{location_name}" not found', file=sys.stderr)

        if not locations:
            print('Found no locations to work on', file=sys.stderr)
            exit(1)

        # which queues do we need to operate on?
        location_ids = set(loc.location_id for loc in locations)
        queue_names = args.queue
        all_queues = queue_names is None
        # full list of queues
        queues = await api.telephony.callqueue.list()
        # filter based on location parameter
        queues = [queue for queue in queues
                  if (all_queues or queue.name in queue_names) and queue.location_id in location_ids]

        # len of queue names for nicer output
        queue_len = max(len(queue.name) for queue in queues)

        # now we can actually go back and re-evaluate the list of locations; for the location length we only need
        # to consider locations we actually have a target queue in
        location_ids = set(queue.location_id for queue in queues)

        # max length of location names for nicely formatted output
        location_len = max(len(loc.name)
                           for loc in locations
                           if loc.location_id in location_ids)

        # get the names for join, unjoin, remove, and add
        join_agents = args.join_agent or []
        unjoin_agents = args.unjoin_agent or []
        remove_users = args.remove_user or []
        add_users = args.add_user or []

        # validate users; make sure that users exist with the provided names
        add_users = [u async for u in validate_users(user_names=add_users)]

        # apply actions to all queues
        await asyncio.gather(*[act_on_queue(queue) for queue in queues])


if __name__ == '__main__':
    # enable DEBUG logging to a file; REST log shows all requests
    logging.basicConfig(filename=os.path.join(os.getcwd(), f'{os.path.splitext(os.path.basename(__file__))[0]}.log'),
                        filemode='w', level=logging.DEBUG)
    asyncio.run(main())

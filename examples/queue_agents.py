#!/usr/bin/env python3
"""
Bulk manage agents in call queues

usage: queue_agents.py [-h] (--add | --remove) --queues QUEUES --agent AGENT [--token TOKEN]

Bulk manage agents in call queues

options:
  -h, --help       show this help message and exit
  --add            Add agent(s) to specified queues
  --remove         Remove agent(s) from specified queues
  --queues QUEUES  Text file with list of call queue names (one per line). Each line should be the a
                   location name and a queue name separated by a colon. Example: "Location1:Queue1"
  --agent AGENT    Single agent email address or text file with agent email addresses (one per line)
  --token TOKEN    admin access token to use. If no token is given then the script will try to use
                   service app tokens. The service app parameters are read from environment variables
                   SERVICE_APP_ID, SERvICE_APP_SECRET, and SERVICE_APP_REFRESH. These parameters can
                   also be defined in "queue_agents.env" file. Service app tokens are cached in
                   "queue_agents.yml". If no access token is passed and no service app is defined then
                   the script falls back to try to read an access token from environment variable
                   WEBEX_ACCESS_TOKEN.

Example: queue_agents.py --queues queues.txt --agent agents.txt --add
"""
import argparse
import asyncio
import logging
import os
import sys
from contextlib import contextmanager
from typing import List, Iterable, Optional

import yaml
from dotenv import load_dotenv

from wxc_sdk import Tokens
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.har_writer import HarWriter
from wxc_sdk.integration import Integration
from wxc_sdk.people import Person
from wxc_sdk.telephony.callqueue import CallQueue
from wxc_sdk.telephony.hg_and_cq import Agent


def yml_path() -> str:
    """
    Get filename for YML file to cache access and refresh token
    """
    return f'{os.path.splitext(os.path.basename(__file__))[0]}.yml'


def env_path() -> str:
    """
    Get path to .env file to read service app settings from
    :return:
    """
    return f'{os.path.splitext(os.path.basename(__file__))[0]}.env'


def read_tokens_from_file() -> Optional[Tokens]:
    """
    Get service app tokens from cache file, return None if cache does not exist
    """
    path = yml_path()
    if not os.path.isfile(path):
        return None
    try:
        with open(path, mode='r') as f:
            data = yaml.safe_load(f)
        tokens = Tokens.model_validate(data)
    except Exception:
        return None
    return tokens


def write_tokens_to_file(tokens: Tokens):
    """
    Write tokens to cache
    """
    with open(yml_path(), mode='w') as f:
        yaml.safe_dump(tokens.model_dump(exclude_none=True), f)


def get_access_token() -> Optional[Tokens]:
    """
    Get a new access token using refresh token, service app client id, service app client secret
    """
    env_vars = ('SERVICE_APP_ID', 'SERVICE_APP_SECRET', 'SERVICE_APP_REFRESH')
    app_id, app_secret, app_refresh = (os.getenv(var) for var in env_vars)
    if not all((app_id, app_secret, app_refresh)):
        return None
    tokens = Tokens(refresh_token=app_refresh)
    integration = Integration(client_id=app_id,
                              client_secret=app_secret,
                              scopes=[], redirect_url=None)
    integration.refresh(tokens=tokens)
    write_tokens_to_file(tokens)
    return tokens


def get_tokens() -> Optional[Tokens]:
    """
    Get tokens from cache or create new access token using service app credentials
    """
    # try to read from file
    tokens = read_tokens_from_file()
    # .. or create new access token using refresh token
    if tokens is None:
        tokens = get_access_token()
        if tokens is None:
            return None
    if tokens.remaining < 24 * 60 * 60:
        tokens = get_access_token()
    return tokens


def read_file_lines(filename: str) -> List[str]:
    """
    Read lines from a file, stripping whitespace and removing empty lines.

    Args:
        filename (str): Path to the input file

    Returns:
        List[str]: Cleaned list of lines from the file

    Raises:
        FileNotFoundError: If the specified file does not exist
        PermissionError: If there are permission issues reading the file
    """
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading file '{filename}'.", file=sys.stderr)
        sys.exit(1)


async def process_one_queue(api: AsWebexSimpleApi, queue: CallQueue, agents: list[Person], action: str):
    """
    Process adding or removing agents from a single call queue.
    """
    # get agents
    details = await api.telephony.callqueue.details(location_id=queue.location_id, queue_id=queue.id)

    agent: Agent
    agents_in_queue = set(agent.agent_id for agent in details.agents)
    agent_ids = set(person.person_id for person in agents)
    if action == 'add':
        agents_to_add = agent_ids - agents_in_queue
        if not agents_to_add:
            print(f"All agents are already in queue {queue.name} in location {queue.location_name}. Skipping.")
            return
        agent_str = ', '.join(sorted(f'{person.display_name}({person.emails[0]})'
                                     for person in agents if person.person_id in agents_to_add))
        print(f"Adding agents to queue {queue.name} in location {queue.location_name}: {agent_str}")
        details.agents.extend([Agent(agent_id=agent_id) for agent_id in agents_to_add])
    else:
        agents_to_remove = agents_in_queue & agent_ids
        if not agents_to_remove:
            print(f"No agents to remove from queue {queue.name} in location {queue.location_name}. Skipping.")
            return
        agent_str = ', '.join(sorted(f'{person.display_name}({person.emails[0]})'
                                     for person in agents if person.person_id in agents_to_remove))
        print(f"Removing agents from queue {queue.name} in location {queue.location_name}: {agent_str}")
        details.agents = [agent for agent in details.agents if agent.agent_id not in agents_to_remove]
    update = CallQueue(agents=details.agents)
    await api.telephony.callqueue.update(location_id=queue.location_id, queue_id=queue.id, update=update)


async def validate_queues(api: AsWebexSimpleApi, queues: Iterable[str]) -> list[CallQueue]:
    """
    Validate queue names and return a list of CallQueue objects
    """
    # validate queue names
    existing_queues = {f'{queue.location_name}:{queue.name}': queue
                       for queue in await api.telephony.callqueue.list()}
    validated_queues = []
    for queue in queues:
        if queue not in existing_queues:
            print(f"Queue '{queue}' does not exist. Skipping.", file=sys.stderr)
        else:
            validated_queues.append(existing_queues[queue])

    return validated_queues


async def validate_users(api: AsWebexSimpleApi, users: Iterable[str]) -> list[Person]:
    """
    Validate user emails and return a list of Person objects
    """
    existing_users = {user.emails[0].lower(): user for user in await api.people.list()}
    validated_users = []
    for user in users:
        if user.lower() not in existing_users:
            print(f"User '{user}' does not exist. Skipping.", file=sys.stderr)
        else:
            validated_users.append(existing_users[user.lower()])

    return validated_users


def main():
    """
    Main CLI script entry point for managing call queue agents.
    """
    parser = argparse.ArgumentParser(
        description='Bulk manage agents in call queues',
        epilog='Example: %(prog)s --queues queues.txt --agent agents.txt --add'
    )

    # Mutually exclusive group for add/remove actions
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--add', action='store_const', const='add', dest='action',
                              help='Add agent(s) to specified queues')
    action_group.add_argument('--remove', action='store_const', const='remove', dest='action',
                              help='Remove agent(s) from specified queues')

    # Input source arguments
    parser.add_argument('--queues', required=True,
                        help='Text file with list of call queue names (one per line). Each line should be the a '
                             'location name and a queue name separated by a colon. Example: "Location1:Queue1"')
    parser.add_argument('--agent', required=True,
                        help='Single agent email address or text file with agent email addresses (one per line)')
    parser.add_argument('--token', type=str, required=False,
                        help=f'admin access token to use. If no token is given then the script will try to use '
                             f'service app tokens. The service app parameters are read from environment variables '
                             f'SERVICE_APP_ID, SERvICE_APP_SECRET, and SERVICE_APP_REFRESH. These parameters can also '
                             f'be defined in "{os.path.splitext(os.path.basename(__file__))[0]}.env" file. Service '
                             f'app tokens are cached in "'
                             f'{os.path.splitext(os.path.basename(__file__))[0]}.yml". If no access token is passed '
                             f'and no service app '
                             f'is defined then the script falls back to try to read an access token from environment '
                             f'variable WEBEX_ACCESS_TOKEN.')

    # Debug and HAR output arguments
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--har', action='store_true', help='Enable HAR output')

    # Parse arguments
    args = parser.parse_args()

    # Get access token
    token = args.token
    load_dotenv(os.path.join(os.getcwd(),
                             f'{os.path.splitext(os.path.basename(__file__))[0]}.env'))

    token = token or (tokens := get_tokens()) and tokens.access_token

    # Read queues from file
    queues = read_file_lines(args.queues)

    # Determine if agent is a file or a single agent email
    try:
        agents = read_file_lines(args.agent) if os.path.isfile(args.agent) else [args.agent]
    except FileNotFoundError:
        agents = [args.agent]

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    async def as_main():
        """
        Async main entry point
        """
        @contextmanager
        def har_writer():
            """
            optional context manager to write HAR file
            """
            if args.har:
                with HarWriter(f'{os.path.splitext(os.path.basename(__file__))[0]}.har', api):
                    yield None
            else:
                yield None

        async with (AsWebexSimpleApi(tokens=token) as api):
            with har_writer():
                # validate queues and agents
                validated_queues, validated_agents = await asyncio.gather(
                    validate_queues(api, queues),
                    validate_users(api, agents))
                if not validated_queues:
                    print("No valid queues found. Exiting.", file=sys.stderr)
                    sys.exit(1)
                if not validated_agents:
                    print("No valid agents found. Exiting.", file=sys.stderr)
                    sys.exit(1)
                validated_queues: List[CallQueue]
                validated_agents: List[Person]

                # process all queues in parallel
                await asyncio.gather(
                    *[process_one_queue(api=api, queue=queue, agents=validated_agents, action=args.action)
                      for queue in validated_queues],
                    return_exceptions=False)
            # with
        return

    asyncio.run(as_main())

    print(f"Completed {args.action} operation for {len(agents)} agent(s) across {len(queues)} queue(s).")


if __name__ == '__main__':
    main()

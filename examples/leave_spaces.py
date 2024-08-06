#!/usr/bin/env python
import asyncio
import logging
import os
import sys
from argparse import ArgumentParser
from collections.abc import Iterable
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv

from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.as_rest import AsRestError
from wxc_sdk.common import RoomType
from wxc_sdk.messages import Message
from wxc_sdk.rooms import Room
from wxc_sdk.teams import Team


async def last_n_messages(api: AsWebexSimpleApi, space: Room, n: int = 10) -> list[Message]:
    """
    Get last n messages in a space
    """
    messages = []
    if not n:
        return messages
    async for message in api.messages.list_gen(room_id=space.id, max=min(n, 1000)):
        messages.append(message)
        n -= 1
        if not n:
            break
    return messages


async def latest_message_in_space(api: AsWebexSimpleApi, space: Room) -> Optional[Message]:
    """
    Get latest message in a space
    """
    last_messages = await last_n_messages(api, space, 1)
    if not last_messages:
        return None
    return last_messages[0]


async def verify_leave_space(api: AsWebexSimpleApi, space: Room, cutoff: datetime) -> bool:
    """
    Get latest message in a space and check if it's older than cutoff
    """
    latest = await latest_message_in_space(api, space)
    if not latest:
        return True
    return latest.created <= cutoff


async def leave_spaces(api: AsWebexSimpleApi, spaces: Iterable[Room]):
    """
    Leave some spaces
    """
    me = await api.people.me()
    person_id = me.person_id

    async def leave_space(space: Room):
        # get membership to delete
        try:
            memberships = await api.membership.list(room_id=space.id, person_id=person_id)
            if not memberships:
                print(f'No membership in space "{space.title}", skipping', file=sys.stderr)
                return
            # delete membership
            print(f'Leaving space "{space.title}"...')
            await api.membership.delete(memberships[0].id)
            print(f'Left space "{space.title}"')
        except AsRestError as e:
            print(f'Error leaving space "{space.title}": {e}', file=sys.stderr)
        return

    await asyncio.gather(*[leave_space(space) for space in spaces])


async def as_main():
    # parse args
    parser = ArgumentParser(description='leave spaces with no activity')
    parser.add_argument('--days', '-d', type=int, required=False, default=3 * 365,
                        help=f'days since last activity; default: {3 * 365}')
    parser.add_argument('--token', type=str, required=False,
                        help='Personal access token to use. If not provided script will try to read token from '
                             'WEBEX_ACCESS_TOKEN environment variable.')
    parser.add_argument('--no_test', action='store_true', required=False,
                        help='Don\'t test; actually leave the spaces')
    parser.add_argument('--no_messages', action='store_true', required=False,
                        help='Only leave spaces that have no messages')
    parser.add_argument('--keep', '-k', type=str, required=False,
                        help='file with list of spaces to keep')
    args = parser.parse_args()

    load_dotenv()
    token = args.token or os.getenv('WEBEX_ACCESS_TOKEN')
    if not token:
        print('No token provided and WEBEX_ACCESS_TOKEN not set in environment', file=sys.stderr)
        exit(1)
    cutoff = datetime.utcnow() - timedelta(days=args.days)
    cutoff = cutoff.replace(tzinfo=timezone.utc)
    if args.keep:
        try:
            with open(args.keep, mode='r') as f:
                keep = set(l.strip() for l in f if l)
        except FileNotFoundError:
            print(f'file "{args.keep}" not found', file=sys.stderr)
            exit(1)
    else:
        keep = set()
    async with AsWebexSimpleApi(tokens=token, concurrent_requests=100) as api:
        # check token
        try:
            await api.people.me()
        except AsRestError as e:
            if e.status == 401:
                print(f'Token seems to be invalid: {e}', file=sys.stderr)
                exit(1)
            raise

        print('Listing spaces and teams...')
        spaces, teams_list = await asyncio.gather(api.rooms.list(max=1000), api.teams.list())
        # we can't leave direct spaces anyway; so ignore them from the start
        spaces = [space for space in spaces if space.type != RoomType.direct]
        print(f'Found {len(spaces)} spaces')
        print(f'Found {len(teams_list)} teams')
        teams = {team.id: team for team in teams_list}

        # identify spaces to leave based on last activity
        leave = [space for space in spaces if space.last_activity and space.last_activity <= cutoff]

        # sometimes the last_activity information seems to be "off" try to get the latest message for each space to
        # verify latest activity
        print(f'Getting latest message for {len(leave)} spaces...')
        latest_messages = await asyncio.gather(*[latest_message_in_space(api, space) for space in leave])
        validated_leave: list[tuple[Room, Optional[datetime]]] = []
        for space, latest_message in zip(leave, latest_messages):
            space: Room
            latest_message: Message
            # don't leave general spaces of Teams
            # A general space is a space that has the same name as the Team it belongs to
            team: Team
            if space.team_id and (team := teams.get(space.team_id, None)) and space.title == team.name:
                print(f'Don\'t leave general space "{space.title}" of Team "{team.name}"')
                continue

            # don't leave spaces in keep file
            if space.title.strip() in keep:
                print(f'Don\'t leave space "{space.title}", found space name in keep file')
                continue

            # if only spaces with no messages should be considered and we have a message in the space then don't leave
            if args.no_messages and latest_message is not None:
                print(f'Space "{space.title}" has messages, latest is {latest_message.created:%Y.%m.%d %H:%M:%S}, '
                      f'last activity is {space.last_activity:%Y.%m.%d %H:%M:%S} - not leaving')
                continue

            # if no latest message or latest message is older than cutoff, consider leaving
            if latest_message is None or latest_message.created <= cutoff:
                latest_messages: Message
                validated_leave.append((space, latest_message and latest_message.created))
                continue
            print(f'Latest message in "{space.title}" is {latest_message.created:%Y.%m.%d %H:%M:%S}, '
                  f'last activity is {space.last_activity:%Y.%m.%d %H:%M:%S} - not leaving')
        print()
        print(f'Found {len(validated_leave)} spaces to leave:')

        # sort spaces by latest activity or latest message
        validated_leave.sort(key=lambda x: max(x[0].last_activity, x[1]) if x[1] else x[0].last_activity,
                             reverse=False)

        for space, latest in validated_leave:
            print(f'Leave "{space.title}"')
            print(f'   last activity {space.last_activity:%Y.%m.%d %H:%M:%S}, latest message '
                  f'{f"{latest:%Y.%m.%d %H:%M:%S}" if latest else "none"}')

        if args.no_test:
            # actually try to leave the spaces
            await leave_spaces(api, (space for space, _ in validated_leave))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(as_main())

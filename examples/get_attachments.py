#!/usr/bin/env python
"""
Get all attachments from one space
"""
import asyncio
import logging
import os
import re
import sys
from asyncio import Semaphore
from itertools import chain
from time import perf_counter

from dotenv import load_dotenv

from wxc_sdk import WebexSimpleApi
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.as_rest import retry_request, AsRestSession
from wxc_sdk.common import RoomType

SPACE_NAME = "Not so secret Sushi"
DOWNLOAD_PATH = '~/Downloads/sushi'


def write_to_file(path: str, content: str):
    with open(path, mode='wb') as f:
        f.write(content)


@retry_request
async def download_attachment(session: AsRestSession, semaphore: Semaphore, url: str):
    async with semaphore:
        before = perf_counter()
        async with await session.get(url=url, headers={'Authorization': f'Bearer {session.access_token}'}) as r:
            cd = r.headers.get('content-disposition')
            if cd is None:
                return
            cd_match = re.match('attachment; filename="(.+)"', cd)
            if not cd_match:
                return
            filename = os.path.join(os.path.expanduser(DOWNLOAD_PATH), cd_match.group(1))
            content = await r.read()
        after = perf_counter()
    print(f'Downloaded {cd_match.group(1)} in {(after-before)*1000:.3f} ms')

    # schedule sync i/o operation to not break asyncio
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, write_to_file, filename, content)


async def get_attachments():
    # get token from environment
    load_dotenv()
    token = os.getenv('WEBEX_ACCESS_TOKEN')

    # get target spaces, messages from that space, and attachment URLs from messages
    with WebexSimpleApi(tokens=token) as api:
        # get target spaces
        print('Getting target space...')
        target_space = next((space for space in api.rooms.list(type_=RoomType.group, sort_by='lastactivity')
                             if space.title == SPACE_NAME), None)
        if target_space is None:
            print(f'Space "{SPACE_NAME}" not found', file=sys.stderr)
            exit(1)
        print('Got target space. Getting messages...')
        # get attachment urls from messages in that space
        messages = api.messages.list(room_id=target_space.id)
        file_urls = list(chain.from_iterable(m.files for m in messages
                                             if m.files))
    print(f'Downloading {len(file_urls)} attachments')

    # schedule async tasks to download all attachments
    # abuse async API to be able to utilize 429 handling
    # limit # of concurrent requests by using a semaphore
    semaphore = Semaphore(30)
    async with AsWebexSimpleApi(tokens=token) as api:
        await asyncio.gather(*[download_attachment(api.session, semaphore, url)
                               for url in file_urls])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(get_attachments())

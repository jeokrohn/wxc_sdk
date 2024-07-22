#!/usr/bin/env python
"""
Example script
Reset call forwarding to default for all users in the org
"""
import asyncio
import logging
import time

from dotenv import load_dotenv

from wxc_sdk.all_types import PersonForwardingSetting
from wxc_sdk.as_api import AsWebexSimpleApi


async def main():
    # load environment. SDk fetches the access token from WEBEX_ACCESS_TOKEN environment variable
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    # set to DEBUG to see the actual requests
    logging.getLogger('wxc_sdk.rest').setLevel(logging.INFO)

    async with AsWebexSimpleApi() as api:

        # get all calling users
        start = time.perf_counter_ns()
        calling_users = [user for user in await api.people.list(calling_data=True)
                         if user.location_id]
        print(f'Got {len(calling_users)} calling users in '
              f'{(time.perf_counter_ns() - start) / 1e6:.3f} ms')

        # set call forwarding to default for all users
        # default call forwarding settings
        forwarding = PersonForwardingSetting.default()

        # schedule update for each user and wait for completion
        start = time.perf_counter_ns()
        await asyncio.gather(*[api.person_settings.forwarding.configure(entity_id=user.person_id,
                                                                        forwarding=forwarding)
                               for user in calling_users])
        print(f'Reset call forwarding to default for {len(calling_users)} users in '
              f'{(time.perf_counter_ns() - start) / 1e6:.3f} ms')

if __name__ == '__main__':
    asyncio.run(main())

#!/usr/bin/env python
"""
Example script
Get all calling users within the org using the (experimental) async API
"""
import asyncio
import time

from dotenv import load_dotenv

from wxc_sdk.as_api import AsWebexSimpleApi

load_dotenv()


async def calling_users():
    async with AsWebexSimpleApi(concurrent_requests=40) as api:
        # using AsPeopleApi.list_gen to iterate over persons
        # Parameter calling_data needs to be set to true to gat calling specific information
        # calling users have the attribute location_id set
        calling_users = [user async for user in api.people.list_gen(calling_data=True)
                         if user.location_id]
        print(f'{len(calling_users)} users:')
        print('\n'.join(user.display_name for user in calling_users))

        # get details for all users
        start = time.perf_counter()
        details = await asyncio.gather(*[api.people.details(person_id=user.person_id, calling_data=True)
                                         for user in calling_users])
        expired = time.perf_counter() - start
        print(f'Got details for {len(calling_users)} users in {expired * 1000:.3f} ms')


asyncio.run(calling_users())

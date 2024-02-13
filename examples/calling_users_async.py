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


async def get_calling_users():
    """
    Get details of all calling enabled users by:
    1) getting all calling users
    2) collecting all users that have a calling license
    3) getting details for all users
    """
    async with AsWebexSimpleApi(concurrent_requests=40) as api:
        print('Collecting calling licenses')
        calling_license_ids = set(lic.license_id for lic in await api.licenses.list()
                                  if lic.webex_calling)

        # get users with a calling license
        calling_users = [user async for user in api.people.list_gen()
                         if any(lic_id in calling_license_ids for lic_id in user.licenses)]
        print(f'{len(calling_users)} users:')
        print('\n'.join(user.display_name for user in calling_users))

        # get details for all users
        start = time.perf_counter()
        details = await asyncio.gather(*[api.people.details(person_id=user.person_id, calling_data=True)
                                         for user in calling_users])
        expired = time.perf_counter() - start
        print(f'Got details for {len(details)} users in {expired * 1000:.3f} ms')


if __name__ == '__main__':
    asyncio.run(get_calling_users())

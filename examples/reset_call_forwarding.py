#!/usr/bin/env python
"""
Example script
Reset call forwarding to default for all users in the org
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv

from wxc_sdk import WebexSimpleApi
from wxc_sdk.all_types import PersonForwardingSetting

load_dotenv()

logging.basicConfig(level=logging.INFO)

# set to DEBUG to see the actual requests
logging.getLogger('wxc_sdk.rest').setLevel(logging.INFO)

api = WebexSimpleApi()

# get all calling users
start = time.perf_counter_ns()
calling_users = [user for user in api.people.list(calling_data=True)
                 if user.location_id]
print(f'Got {len(calling_users)} calling users in '
      f'{(time.perf_counter_ns() - start) / 1e6:.3f} ms')

# set call forwarding to default for all users
with ThreadPoolExecutor() as pool:
    # default call forwarding settings
    forwarding = PersonForwardingSetting.default()

    # schedule update for each user and wait for completion
    start = time.perf_counter_ns()
    list(pool.map(
        lambda user: api.person_settings.forwarding.configure(person_id=user.person_id,
                                                              forwarding=forwarding),
        calling_users))
    print(f'Reset call forwarding to default for {len(calling_users)} users in '
          f'{(time.perf_counter_ns() - start) / 1e6:.3f} ms')

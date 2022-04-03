#!/usr/bin/env python
"""
Example script
Get all calling users within the org
"""

from dotenv import load_dotenv

from wxc_sdk import WebexSimpleApi

load_dotenv()

api = WebexSimpleApi()

# using wxc_sdk.people.PeopleApi.list to iterate over persons
# Parameter calling_data needs to be set to true to gat calling specific information
# calling users have the attribute location_id set
calling_users = [user for user in api.people.list(calling_data=True)
                 if user.location_id]
print(f'{len(calling_users)} users:')
print('\n'.join(user.display_name for user in calling_users))

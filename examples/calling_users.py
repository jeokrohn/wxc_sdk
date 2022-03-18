
from wxc_sdk import WebexSimpleApi

api = WebexSimpleApi()

calling_users = [user for user in api.people.list(calling_data=True)
                 if user.location_id]
print(f'{len(calling_users)} users:')
print('\n'.join(user.display_name for user in calling_users))

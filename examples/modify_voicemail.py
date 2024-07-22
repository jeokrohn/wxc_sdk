#!/usr/bin/env python
"""
Example Script
Modifying number of rings configuration in voicemail settings
Run -> python3 modify_voicemail.py modify_voicemail.csv
"""
import csv
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv

from wxc_sdk import WebexSimpleApi
from wxc_sdk.all_types import *

VOICEMAIL_SETTINGS_NUMBER_OF_RINGS = 6

# loading environment variables - use .env file for development
load_dotenv()


def update_vm_settings():
    """
    actually update VM settings for all users present in input CSV
    """
    api = WebexSimpleApi()
    final_report = []
    mail_ids = []
    # using wxc_sdk.people.PeopleApi.list to iterate over persons
    # Parameter calling_data needs to be set to true to gat calling specific information
    # calling users have the attribute location_id set
    calling_users = [user for user in api.people.list(calling_data=True)
                     if user.location_id]
    print(f'{len(calling_users)} users:')
    print('\n'.join(user.display_name for user in calling_users))

    # get CSV file name from command line
    with open(str(sys.argv[1]), 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        # read all records from CSV. Ony consider records w/o error
        for col in reader:
            if not col['ERROR']:
                # collect email address from USERNAME column for further processing
                mail_ids.append(col['USERNAME'])
            else:
                final_report.append((col['USERNAME'], 'FAILED DUE TO ERROR REASON IN INPUT FILE'))

    # work on calling users that have an email address that we read from the CSV
    filteredUsers = [d for d in calling_users if d.emails[0] in mail_ids]

    print("\nCalling Users in CI  - Count ", len(calling_users))
    print("Mail IDs from input file after removing error columns - Count ", len(mail_ids))
    print("FilteredUsers Users -  Count", len(filteredUsers))

    def set_number_of_rings(user: Person):
        """
        Read VM config for a user
        :param user: user to update
        """
        try:
            # shortcut
            vm = api.person_settings.voicemail

            # Read Current configuration
            vm_settings = vm.read(person_id=user.person_id)
            print(f'\n Existing Configuration: {vm_settings} ')

            # Modify number of rings value
            vm_settings.send_unanswered_calls.number_of_rings = VOICEMAIL_SETTINGS_NUMBER_OF_RINGS
            vm.configure(user.person_id, settings=vm_settings)
            # Read configuration after changes
            vm_settings = vm.read(user.person_id)
            print(f'\n New Configuration: {vm_settings} ')
            final_report.append((user.display_name, 'SUCCESS'))
        except Exception as e:
            final_report.append((user.display_name, 'FAILURE'))
            print("type error: " + str(e))
            print(traceback.format_exc())
        return

    # Modify settings for the filtered users
    with ThreadPoolExecutor() as pool:
        list(pool.map(lambda user: set_number_of_rings(user),
                      filteredUsers))

    print(final_report)
    with open('output.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(["USERNAME", "STATUS"])
        write.writerows(final_report)


if __name__ == '__main__':
    update_vm_settings()

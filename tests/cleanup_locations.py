"""
Delete unused locations
"""

import logging
from concurrent.futures.thread import ThreadPoolExecutor
from itertools import chain
from time import sleep

from dotenv import load_dotenv

from wxc_sdk import WebexSimpleApi
from wxc_sdk.all_types import *


def disable_calling(api: WebexSimpleApi, location: TelephonyLocation) -> list[JobErrorItem]:
    """
    Disable calling for on location
    """
    job = api.jobs.disable_calling_location.initiate(location_id=location.location_id, force_delete=True)
    # wait for job to fail or complete
    while job.latest_execution_status not in ('COMPLETED', 'FAILED'):
        print(f'Latest execution status: {job.latest_execution_status}')
        sleep(1)
        job = api.jobs.disable_calling_location.status(job.id)
    errors = api.telephony.jobs.disable_calling_location.errors(job.id)
    return errors


def delete_unused_locations(api: WebexSimpleApi):
    locations = {loc.location_id: loc for loc in api.locations.list()}
    tel_locations = {loc.location_id: loc for loc in api.telephony.location.list()}
    non_tel_locations = [loc for loc in locations.values() if loc.location_id not in tel_locations]

    # check which calling locations can be deleted
    def can_delete(location: TelephonyLocation) -> bool:
        check = api.telephony.location.safe_delete_check_before_disabling_calling_location(location.location_id)
        return check

    checks = []
    with ThreadPoolExecutor() as pool:
        checks = list(pool.map(can_delete, tel_locations.values()))
    checks: list[SafeDeleteCheckResponse]

    tel_locations_can_delete = [
        (loc, check)
        for loc, check in zip(tel_locations.values(), checks)
        if check.location_delete_status != LocationDeleteStatus.blocked
        and locations[loc.location_id].address.country == 'US'
    ]

    # delete non telephony locations
    if non_tel_locations:
        print(f'Deleting {len(non_tel_locations)} non-telephony locations')
        print('\n'.join(f'* {loc.name}' for loc in non_tel_locations))

        with ThreadPoolExecutor() as pool:
            list(pool.map(api.locations.delete, (loc.location_id for loc in non_tel_locations)))
        if tel_locations_can_delete:
            print()

    if tel_locations_can_delete:
        # delete calling locations
        print('Telephony locations that can be deleted:')
        for loc, check in tel_locations_can_delete:
            print(f'* {loc.name} - {check.location_delete_status}')

        for loc, _ in tel_locations_can_delete:
            print(f'Disable calling for "{loc.name}"')
            errors = disable_calling(api, loc)
            if errors:
                print('\n'.join(m.description for m in chain.from_iterable(item.error.message for item in errors)))
                print('... not deleting!')
            print(f'Delete "{loc.name}"')
            api.locations.delete(loc.location_id)
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    with WebexSimpleApi() as webex_api:
        delete_unused_locations(webex_api)

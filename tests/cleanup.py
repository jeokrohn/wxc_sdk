#!/usr/bin/env python
"""
Clean up test objects created by test cases
"""

import logging
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import chain

from tests.base import get_tokens
from wxc_sdk import WebexSimpleApi

TO_DELETE = re.compile(r'^(?:(?:\w{2}|many|test|test_user)_\d{3})|National Holidays$')
DRY_RUN = False


def filter(targets):
    for t in targets:
        if TO_DELETE.match(t.name):
            yield t
        else:
            print(f'Keeping {t.__class__.__name__}({t.name})')


def main():
    tokens = get_tokens()
    if not tokens:
        print('Failed to get tokens', file=sys.stderr)
        exit(1)
    api = WebexSimpleApi(tokens=tokens)
    locations = list(api.locations.list())

    log_name = f'{os.path.splitext(__file__)[0]}.log'

    fmt = logging.Formatter(fmt='%(asctime)s %(threadName)s %(message)s')
    fmt.converter = time.gmtime

    fh = logging.FileHandler(log_name, mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    rest_logger = logging.getLogger('wxc_sdk.rest')
    rest_logger.addHandler(fh)
    rest_logger.setLevel(logging.DEBUG)

    with ThreadPoolExecutor() as pool:
        # auto attendants
        ata = api.telephony.auto_attendant
        aa_list = list(filter(ata.list()))
        print(f'deleting {len(aa_list)} auto attendants: {", ".join(aa.name for aa in aa_list)}')
        if not DRY_RUN:
            list(pool.map(lambda aa: ata.delete_auto_attendant(location_id=aa.location_id,
                                                               auto_attendant_id=aa.auto_attendant_id),
                          aa_list))
        # call parks
        atc = api.telephony.callpark
        cp_list = list(filter(chain.from_iterable(
            pool.map(lambda l: atc.list(location_id=l.location_id),
                     locations))))
        print(f'deleting {len(cp_list)} call parks: {", ".join(cp.name for cp in cp_list)}')
        if not DRY_RUN:
            list(pool.map(lambda cp: atc.delete_callpark(location_id=cp.location_id, callpark_id=cp.callpark_id),
                          cp_list))

        # call pickups
        atp = api.telephony.pickup
        cpu_list = list(filter(chain.from_iterable(
            pool.map(lambda l: atp.list(location_id=l.location_id),
                     locations))))
        print(f'deleting {len(cpu_list)} call pickups: {", ".join(cp.name for cp in cpu_list)}')
        if not DRY_RUN:
            list(pool.map(lambda cp: atp.delete_pickup(location_id=cp.location_id, pickup_id=cp.pickup_id),
                          cpu_list))

        # call queues
        atq = api.telephony.callqueue
        cq_list = list(filter(chain.from_iterable(
            pool.map(lambda l: atq.list(location_id=l.location_id),
                     locations))))
        print(f'deleting {len(cq_list)} call queues: {", ".join(cq.name for cq in cq_list)}')
        if not DRY_RUN:
            list(pool.map(lambda cq: atq.delete_queue(location_id=cq.location_id, queue_id=cq.id),
                          cq_list))

        # hunt groups
        ath = api.telephony.huntgroup
        hg_list = list(filter(chain.from_iterable(
            pool.map(lambda l: ath.list(location_id=l.location_id),
                     locations))))
        print(f'deleting {len(hg_list)} hunt groups: {", ".join(hg.name for hg in hg_list)}')
        if not DRY_RUN:
            list(pool.map(lambda hg: ath.delete_huntgroup(location_id=hg.location_id, huntgroup_id=hg.id),
                          hg_list))

        # paging groups
        atpg = api.telephony.paging
        pg_list = list(filter(atpg.list()))
        print(f'deleting {len(pg_list)} paging groups: {", ".join(pg.name for pg in pg_list)}')
        if not DRY_RUN:
            list(pool.map(lambda pg: atpg.delete_paging(location_id=pg.location_id, paging_id=pg.paging_id),
                          pg_list))

        # schedules
        ats = api.telephony.schedules
        schedule_list = list(filter(chain.from_iterable(
            pool.map(lambda l: ats.list(obj_id=l.location_id),
                     locations))))
        print(f'deleting {len(schedule_list)} schedules: {", ".join(schedule.name for schedule in schedule_list)}')
        if not DRY_RUN:
            list(pool.map(lambda schedule: ats.delete_schedule(obj_id=schedule.location_id,
                                                               schedule_type=schedule.schedule_type,
                                                               schedule_id=schedule.schedule_id),
                          schedule_list))

        # person schedules
        aps = api.person_settings.schedules
        users = [user for user in api.people.list(calling_data=True)
                 if user.location_id]

        schedule_lists = list(pool.map(lambda user: list(aps.list(obj_id=user.person_id)),
                                       users))
        users_and_schedules = list(chain.from_iterable(((user, schedule)
                                                        for schedule in filter(schedules))
                                                       for user, schedules in zip(users, schedule_lists)))
        print(f'deleting {len(users_and_schedules)} user schedules:'
              f' {", ".join(f"{user.display_name}-{schedule.name}" for user, schedule in users_and_schedules)}')

        if not DRY_RUN:
            list(pool.map(
                lambda user_and_schedule: aps.delete_schedule(
                    obj_id=user_and_schedule[0].person_id,
                    schedule_type=user_and_schedule[1].schedule_type,
                    schedule_id=user_and_schedule[1].schedule_id),
                users_and_schedules))


if __name__ == '__main__':
    main()

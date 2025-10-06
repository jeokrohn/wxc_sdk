"""
Testing the managing number job API
"""
import asyncio
import datetime
from collections import defaultdict
from contextlib import asynccontextmanager
from functools import reduce
from json import dumps, loads
from random import shuffle
from time import sleep, perf_counter
from typing import NamedTuple

from dateutil import tz

from tests.base import TestCaseWithLog, TestWithLocations
from tests.testutil import as_available_tns
from wxc_sdk.common import NumberState
from wxc_sdk.telephony import NumberType, NumberListPhoneNumber
from wxc_sdk.telephony.jobs import NumberItem, NumberJob
from wxc_sdk.telephony.location import TelephonyLocation


class TestList(TestCaseWithLog):
    def test_001_list_jobs(self):
        jobs = list(self.api.telephony.jobs.manage_numbers.list())
        print(f'Got {len(jobs)} jobs')


class LocationAndNumbers(NamedTuple):
    location: TelephonyLocation
    numbers: list[NumberListPhoneNumber]


class MoveNumberContext(NamedTuple):
    source_location: LocationAndNumbers
    target_location: LocationAndNumbers
    numbers: list[str]


class TestMoveNumbers(TestWithLocations):

    async def pick_locations(self) -> tuple[LocationAndNumbers, LocationAndNumbers]:
        """
        Pick two locations that can be used for the test to move numbers.

        US locations with premises PSTN and at least one number so that we can gather the NPA
        """
        locations = [loc for loc in self.locations
                     if loc.address.country == 'US']

        # get telephony details for all locations
        details, numbers = await asyncio.gather(
            asyncio.gather(*[self.async_api.telephony.location.details(location_id=loc.location_id)
                             for loc in locations]),
            self.async_api.telephony.phone_numbers(number_type=NumberType.number))
        details: list[TelephonyLocation]
        numbers: list[NumberListPhoneNumber]
        numbers_by_location = reduce(lambda r, e: r[e.location.id].append(e) or r, numbers, defaultdict(list))
        candidates = [loc for loc in details
                      if loc.connection and numbers_by_location.get(loc.location_id)]
        if len(candidates) < 2:
            self.skipTest('Need at least two locations with numbers to run this test')
        shuffle(candidates)
        return (LocationAndNumbers(candidates[0], numbers_by_location[candidates[0].location_id]),
                LocationAndNumbers(candidates[1], numbers_by_location[candidates[1].location_id]))

    def update_pstn(self, location: TelephonyLocation):
        """
        Update PSTN of given location
        """
        self.api.telephony.pstn.configure(location_id=location.location_id, premise_route_id=location.connection.id,
                                          premise_route_type=location.connection.type)

    async def delete_numbers(self, location_id: str, numbers: list[str]):
        """
        Delete a bunch of number from location
        :param location_id:
        :param numbers:
        :return:
        """
        await asyncio.gather(*[self.async_api.telephony.location.number.remove(
            location_id=location_id,
            phone_numbers=numbers[i:i + 5]) for i in range(0, len(numbers), 5)])

    async def cleanup_numbers(self, location: TelephonyLocation, loc_ref: str, new_tns: list[str]):
        """
        Remove numbers from location and create some output
        """
        # get numbers in location
        numbers = set(n.phone_number for n in
                      self.api.telephony.phone_numbers(location_id=location.location_id,
                                                       number_type=NumberType.number))
        to_remove = [n for n in new_tns if n in numbers]
        if to_remove:
            await self.delete_numbers(location_id=location.location_id,
                                      numbers=to_remove)
            print(f'removed numbers from {loc_ref} location {location.name}: {", ".join(to_remove)}')
        return

    @asynccontextmanager
    async def move_number_context(self, number_count: int = 1,
                                  number_state: NumberState = NumberState.active,
                                  keep_log: bool = True) -> MoveNumberContext:
        with self.no_log(keep_log):
            source_location, target_location = await self.pick_locations()

            print(f'source location "{source_location.location.name}" ({source_location.numbers[0].phone_number[2:5]})')
            print(f'target location "{target_location.location.name}" ({target_location.numbers[0].phone_number[2:5]})')

            # add numbers to location
            # get available TN in the +1-XXX-555-0XXX range
            new_tns = await as_available_tns(
                as_api=self.async_api,
                tn_prefix=f'{source_location.numbers[0].phone_number[:5]}5550',
                tns_requested=number_count)
            new_tns: list[str]

        # add number(s) to source location and activate. Only activated numbers can be moved
        print(f'Adding numbers to source location: {", ".join(new_tns)}')
        self.api.telephony.location.number.add(location_id=source_location.location.location_id,
                                               phone_numbers=new_tns,
                                               state=number_state)
        try:
            # to be able to move numbers both locations have to use the same premises PSTN connection
            # we temporarily update the PSTN choice to the target location
            with self.no_log(keep_log):
                old_target_pstn_connection = target_location.location.connection
                target_location.location.connection = source_location.location.connection
                self.update_pstn(target_location.location)
                print(f'temporarily updated PSTN connection of target location "{target_location.location.name}"')

            # now yield the context
            try:
                yield MoveNumberContext(source_location=source_location,
                                        target_location=target_location,
                                        numbers=new_tns)
            finally:
                with self.no_log(keep_log):
                    # restore old PSTN connection
                    target_location.location.connection = old_target_pstn_connection
                    self.update_pstn(target_location.location)
                    print(f'restored PSTN connection of target location "{target_location.location.name}"')
        finally:
            # remove numbers from source and target location
            with self.no_log(keep_log):
                await asyncio.gather(
                    self.cleanup_numbers(location=source_location.location, loc_ref='source', new_tns=new_tns),
                    self.cleanup_numbers(location=target_location.location, loc_ref='target', new_tns=new_tns))
        return

    def monitor_job(self, job: NumberJob) -> NumberJob:
        """
        Monitor job until completion
        :param job:
        :return:
        """
        start = perf_counter()
        max_wait = 30
        while (perf_counter() < (start + max_wait)) and job.latest_execution_status not in {'COMPLETED', 'FAILED'}:
            print(f'{datetime.datetime.now(tz=tz.UTC).isoformat()}: job status: {job.latest_execution_status}')
            sleep(2)
            job = self.api.telephony.jobs.manage_numbers.status(job_id=job.id)
        return job

    def job_completed(self, job: NumberJob) -> bool:
        """
        Check whether the job completed successfully
        """
        completed = job.latest_execution_status == 'COMPLETED' and all(
            jes.exit_code == 'COMPLETED' and all(ses.status_message == 'COMPLETED'
                                                 for ses in jes.step_execution_statuses)
            for jes in job.job_execution_status)
        if not completed:
            print('Job not completed successfully:')
            print(dumps(loads(job.model_dump_json()), indent=2))
            job_errors = list(self.api.telephony.jobs.manage_numbers.errors(job_id=job.id))
            for error in job_errors:
                print(f'{error.item}: {error.error.message[0].code} ({error.error.message[0].description})')
        return completed

    async def move_number(self, number_count: int = 1,
                          number_state: NumberState = NumberState.active):
        """
        try to move one active number from one location to another
        """
        async with self.move_number_context(number_count=number_count, number_state=number_state) as context:
            source_location, target_location, new_tns = context

            job = self.api.telephony.jobs.manage_numbers.initiate_job(
                operation='MOVE',
                target_location_id=target_location.location.location_id,
                number_list=[NumberItem(location_id=source_location.location.location_id,
                                        numbers=new_tns)])
            job = self.monitor_job(job)

            self.assertTrue(self.job_completed(job), 'Job not completed successfully')

            # check whether all numbers actually have been moved
            numbers_in_target_location = set(tn.phone_number for tn in self.api.telephony.phone_numbers(
                location_id=target_location.location.location_id,
                number_type=NumberType.number))
            new_tns_not_moved = [tn for tn in new_tns
                                 if tn not in numbers_in_target_location]
            self.assertTrue(not new_tns_not_moved, f'TNs not moved: {", ".join(new_tns_not_moved)}')
        return

    @TestCaseWithLog.async_test
    async def test_001_move_number(self, number_count: int = 1,
                                   number_state: NumberState = NumberState.active):
        """
        try to move one active number from one location to another
        """
        await self.move_number()

    @TestCaseWithLog.async_test
    async def test_002_move_numbers(self):
        """
        try to move multiple active numbers from one location to another
        we expect this to fail: RESTError 412, BATCH-1017031
        """
        await self.move_number(number_count=20)

    @TestCaseWithLog.async_test
    async def test_003_move_inactive_number(self):
        """
        try to move a single inactive number
        """
        await self.move_number(number_count=1, number_state=NumberState.inactive)

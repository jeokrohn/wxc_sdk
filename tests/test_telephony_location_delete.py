"""
Testing deletion of calling locations
"""
import asyncio
import json
import random
import time

from pydantic import TypeAdapter

from tests.base import TestWithLocations, async_test
from wxc_sdk.telephony.jobs import JobErrorItem
from wxc_sdk.telephony.location import SafeDeleteCheckResponse, LocationDeleteStatus


class TestLocationDelete(TestWithLocations):
    @async_test
    async def test_safe_delete_check(self):
        """
        Safe delete check for all calling locations
        """
        pre_check_results = await asyncio.gather(*[
            self.async_api.telephony.locations.safe_delete_check_before_disabling_calling_location(loc.location_id)
            for loc in self.telephony_locations
        ], return_exceptions=True)
        err = None
        for loc, res in zip(self.locations, pre_check_results):
            print(f'Location {loc.name} safe delete check:')

            if isinstance(res, Exception):
                err = err or res
                self.fail(f'Location {loc.name} safe delete check raised exception: {res}')
            else:
                res: SafeDeleteCheckResponse
                print(json.dumps(res.model_dump(mode='json', by_alias=True, exclude_none=True), indent=2))
            print()
        if err:
            raise err

    @async_test
    async def test_delete_blocked_location(self):
        """
        Try to delete a location that is blocked
        """
        pre_check_results = await asyncio.gather(*[
            self.async_api.telephony.locations.safe_delete_check_before_disabling_calling_location(loc.location_id)
            for loc in self.telephony_locations
        ])
        pre_check_results: list[SafeDeleteCheckResponse]
        blocked_locations = [loc for loc, res in zip(self.telephony_locations, pre_check_results)
                             if res.location_delete_status == LocationDeleteStatus.blocked]
        if not blocked_locations:
            self.skipTest('No blocked locations to test deletion')
        target = random.choice(blocked_locations)

        print(f'Testing deletion of blocked location {target.name}')
        job = self.api.jobs.disable_calling_location.initiate(location_id=target.location_id, force_delete=False)
        # wait for job to fail or complete
        while job.latest_execution_status not in ('COMPLETED', 'FAILED'):
            print(f'Latest execution status: {job.latest_execution_status}')
            time.sleep(1)
            job = self.api.jobs.disable_calling_location.status(job.id)
        print(f'Final execution status: {job.latest_execution_status}')
        errors = self.api.telephony.jobs.disable_calling_location.errors(job.id)
        print(f'Errors:')
        print(json.dumps(TypeAdapter(list[JobErrorItem]).dump_python(errors, mode='json', exclude_none=True,
                                                                     by_alias=True),
                         indent=2))
        self.assertEqual('FAILED', job.latest_execution_status)
        self.assertTrue(len(errors) > 0, 'Expected errors for blocked location deletion')

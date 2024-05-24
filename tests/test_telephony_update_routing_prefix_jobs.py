from random import choice
from time import sleep
from typing import Optional

from tests.base import TestCaseWithLog
from wxc_sdk.telephony.jobs import StartJobResponse
from wxc_sdk.telephony.location import TelephonyLocation


class TestJobs(TestCaseWithLog):

    @staticmethod
    def print_job(job: StartJobResponse):
        """
        Print job details
        """
        print(f'{job.instance_id}')
        for status in job.job_execution_status:
            print(f'  created {status.created_time} start {status.start_time} end {status.end_time}')
            for step in status.step_execution_statuses:
                print(f'    start {step.start_time} end {step.end_time} {step.exit_code} {step.name}')

    def update_prefix_and_monitor(self, location: TelephonyLocation, new_prefix: str) -> Optional[StartJobResponse]:
        """
        Update routing prefix of given location and monitor job until done
        """
        # update routing prefix
        job_id = self.api.telephony.location.update(location_id=location.location_id,
                                                    settings=TelephonyLocation(routing_prefix=new_prefix))
        after = self.api.telephony.location.details(location_id=location.location_id)
        self.assertEqual(new_prefix, after.routing_prefix)
        if not job_id:
            return None

        # monitor job until done
        while True:
            job = self.api.telephony.jobs.update_routing_prefix.status(job_id=job_id)
            self.print_job(job)
            if job.latest_execution_status == 'COMPLETED':
                break
            sleep(5)
        return job

    def test_list(self):
        """
        List jobs
        """
        jobs = list(self.api.telephony.jobs.update_routing_prefix.list())
        print(f'Got {len(jobs)} update routing prefix jobs')
        if not jobs:
            self.skipTest('No existing jobs')
        for job in jobs:
            self.print_job(job)

    def test_update_routing_prefix(self):
        """
        Update routing prefix for a location and then monitor jobs
        """
        # get list of telephony locations
        telephony_locations = list(self.api.telephony.location.list())
        # get available routing prefix
        routing_prefixes = (set(loc.routing_prefix for loc in telephony_locations if loc.routing_prefix))
        routing_prefix_len = max(map(len, routing_prefixes))
        steering_digit = min(loc.routing_prefix[0] for loc in telephony_locations if loc.routing_prefix)
        available_prefix = next(prefix
                                for i in range(1, 10 ** routing_prefix_len)
                                if (prefix := f'{steering_digit}{i:0{routing_prefix_len - 1}}') not in routing_prefixes)
        # pick random location
        target_location = choice(telephony_locations)
        print(f'Target location: {target_location.name}, routing prefix: {target_location.routing_prefix}, '
              f'updating to {available_prefix}')
        self.update_prefix_and_monitor(location=target_location, new_prefix=available_prefix)

        # restore old routing prefix
        print(f'Restoring routing prefix to {target_location.routing_prefix}')
        self.update_prefix_and_monitor(location=target_location, new_prefix=target_location.routing_prefix)

    def test_clear_routing_prefix(self):
        """
        Clear routing prefix for a location and then monitor jobs
        """
        # get list of telephony locations
        telephony_locations_with_routing_prefix = [loc for loc in self.api.telephony.location.list()
                                                   if loc.routing_prefix]
        if not telephony_locations_with_routing_prefix:
            self.skipTest('No locations with routing prefix')
        # pick random location
        target_location = choice(telephony_locations_with_routing_prefix)
        print(f'Target location: {target_location.name}, routing prefix: {target_location.routing_prefix}, '
              f'clearing routing prefix')
        self.update_prefix_and_monitor(location=target_location, new_prefix=None)
        # restore old routing prefix
        print(f'Restoring routing prefix to {target_location.routing_prefix}')
        self.update_prefix_and_monitor(location=target_location, new_prefix=target_location.routing_prefix)

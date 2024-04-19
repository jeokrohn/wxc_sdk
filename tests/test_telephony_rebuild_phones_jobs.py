import json
import random
import time
from collections import defaultdict
from functools import reduce

from tests.base import TestCaseWithLog
from wxc_sdk.devices import Device
from wxc_sdk.telephony.jobs import StartJobResponse


class TestJobs(TestCaseWithLog):

    def monitor_job_execution(self, job: StartJobResponse):
        """
        monitor a job until its completion
        :return:
        """
        while True:
            print(f'{job.instance_id} {job.target} {job.location_name} '
                  f'{job.device_count} devices {job.latest_execution_status}')
            for status in job.job_execution_status:
                print(f'  created {status.created_time} start {status.start_time} end {status.end_time}')
                for step in status.step_execution_statuses:
                    print(f'    start {step.start_time} end {step.end_time} {step.exit_code} {step.name}')
            if job.latest_execution_status in {'COMPLETED', 'FAILED'}:
                break
            print('not ready; sleep for 2 seconds...')
            time.sleep(2)
            job = self.api.telephony.jobs.rebuild_phones.status(job_id=job.id)
        print(json.dumps(json.loads(job.model_dump_json()), indent=2))
        self.assertEqual('COMPLETED', job.latest_execution_status)

    def test_list(self):
        """
        List jobs
        """
        jobs = list(self.api.telephony.jobs.rebuild_phones.list())
        print(f'Got {len(jobs)} rebuild phone configuration jobs')
        if not jobs:
            self.skipTest('No existing jobs')
        for job in jobs:
            print(f'{job.instance_id} {job.target} {job.location_name} '
                  f'{job.device_count} devices')
            for status in job.job_execution_status:
                print(f'  created {status.created_time} start {status.start_time} end {status.end_time}')
                for step in status.step_execution_statuses:
                    print(f'    start {step.start_time} end {step.end_time} {step.exit_code} {step.name}')

    def test_rebuild_phones(self):
        """
        pick random location and initiate rebuild phone config job
        """
        with self.no_log():
            devices = list(self.api.devices.list())
            devices_by_location: dict[str, list[Device]] = reduce(
                lambda acc, device: acc[device.location_id].append(device) or acc,
                devices,
                defaultdict(list))
            target_location_id = random.choice(list(devices_by_location))
            target_location = self.api.locations.details(location_id=target_location_id)
        devices_in_target_location = devices_by_location[target_location_id]
        print(f'Initiating rebuild phone config job for {len(devices_in_target_location)} devices in '
              f'"{target_location.name}"')
        job = self.api.telephony.jobs.rebuild_phones.rebuild_phones_configuration(location_id=target_location_id)
        self.monitor_job_execution(job=job)
        errors = self.api.telephony.jobs.rebuild_phones.errors(job_id=job.id)

        foo = 1

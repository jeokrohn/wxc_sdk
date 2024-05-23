from tests.base import TestCaseWithLog


class TestJobs(TestCaseWithLog):

    def test_list(self):
        """
        List jobs
        """
        jobs = list(self.api.telephony.jobs.update_routing_prefix.list())
        print(f'Got {len(jobs)} update routing prefix jobs')
        if not jobs:
            self.skipTest('No existing jobs')
        for job in jobs:
            print(f'{job.instance_id}')
            for status in job.job_execution_status:
                print(f'  created {status.created_time} start {status.start_time} end {status.end_time}')
                for step in status.step_execution_statuses:
                    print(f'    start {step.start_time} end {step.end_time} {step.exit_code} {step.name}')

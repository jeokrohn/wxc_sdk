from time import sleep

from tests.base import TestCaseWithLog


class TestSendActivationEmail(TestCaseWithLog):
    def test_initiate_job(self):
        """
        initiate a bulk activation email resend job
        """
        me = self.api.people.me()
        org_id = me.org_id
        api = self.api.telephony.jobs.activation_emails
        job = api.start(org_id=org_id)
        # wait for job to complete
        while True:
            status = api.status(org_id=org_id, job_id=job.id)
            if status.latest_execution_status == 'COMPLETED':
                break
            elif status.latest_execution_status == 'FAILED':
                self.fail(f'Job failed: {status.latest_execution_status}')
            print(f'Job status: {status.latest_execution_status}')
            sleep(10)
        return

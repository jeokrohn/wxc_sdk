"""
Test Line key template operations
"""
import asyncio
import json
from time import sleep

from tests.base import TestCaseWithLog, async_test, TestWithLocations
from wxc_sdk.common import ApplyLineKeyTemplateAction, OwnerType
from wxc_sdk.devices import Device, ProductType
from wxc_sdk.telephony import NumberType, NumberListPhoneNumber, SupportedDevices
from wxc_sdk.telephony.devices import LineKeyTemplate, ProgrammableLineKey, LineKeyType


class TestLineKeyTemplate(TestCaseWithLog):
    def test_list(self):
        """
        list all line key templates
        """
        api = self.api.telephony.devices
        lkts = list(api.list_line_key_templates())
        print(f'found {len(lkts)} line key templates')

    @async_test
    async def test_details(self):
        """
        Get details for all line key templates
        """
        api = self.async_api.telephony.devices
        lkts = await api.list_line_key_templates()
        details = await asyncio.gather(*[api.line_key_template_details(template_id=lkt.id)
                                         for lkt in lkts],
                                       return_exceptions=True)
        err = next((d for d in details if isinstance(d, Exception)), None)
        if err:
            raise err
        print(f'for details for {len(lkts)} line key templates')

    @async_test
    async def test_create(self):
        """
        create a line key template
        """
        # get some information 1st
        extensions, supported, devices, lkts = await asyncio.gather(
            self.async_api.telephony.phone_numbers(number_type=NumberType.extension,
                                                   owner_type=OwnerType.people),
            self.async_api.telephony.supported_devices(),
            self.async_api.devices.list(product_type=ProductType.phone),
            self.async_api.telephony.devices.list_line_key_templates())
        extensions: list[NumberListPhoneNumber]
        supported: SupportedDevices
        devices: list[Device]
        lkts: list[LineKeyTemplate]

        model_8865 = next(d.model for d in supported.devices if '8865' in d.model)
        lkt_name = next(name
                        for i in range(1, 100)
                        if (name := f'test 8865 {i:03}') not in set(lkt.template_name
                                                                    for lkt in lkts))
        line_keys = ProgrammableLineKey.standard_plk_list(10)
        line_keys[5] = ProgrammableLineKey(line_key_index=6, line_key_type=LineKeyType.speed_dial,
                                           line_key_label='hgreen',
                                           line_key_value='7101')
        template = LineKeyTemplate(template_name=lkt_name,
                                   device_model=model_8865,
                                   user_reorder_enabled=True,
                                   line_keys=line_keys)
        new_lkt_id = self.api.telephony.devices.create_line_key_template(template=template)
        details = self.api.telephony.devices.line_key_template_details(template_id=new_lkt_id)
        print(json.dumps(json.loads(details.model_dump_json()), indent=2))


class TestPreviewApply(TestWithLocations):
    def test_preview_apply_default_template(self):
        """
        try to apply a line key template
        """
        devices = list(self.api.devices.list(product_type=ProductType.phone))
        if not devices:
            self.skipTest('No MPP devices')

        # preview apply default template
        r = self.api.telephony.devices.preview_apply_line_key_template(
            action=ApplyLineKeyTemplateAction.apply_default_templates)
        self.assertEqual(len(devices), r)


class TestJobs(TestCaseWithLog):

    @async_test
    async def test_list_jobs(self):
        """
        list apply line key template jobs
        """
        jobs = await self.async_api.telephony.jobs.apply_line_key_templates.list()
        print(f'got {len(jobs)} jobs')

    @async_test
    async def test_job_status(self):
        """
        get status of all jobs
        """
        jobs = await self.async_api.telephony.jobs.apply_line_key_templates.list()
        details = await asyncio.gather(
            *[self.async_api.telephony.jobs.apply_line_key_templates.status(job_id=job.id) for job in jobs],
            return_exceptions=True)
        err = next((d for d in details if isinstance(d, Exception)), None)
        if err:
            raise err
        print(f'got status for {len(details)} jobs')

    @async_test
    async def test_job_errors(self):
        """
        get errors of all jobs
        """
        jobs = await self.async_api.telephony.jobs.apply_line_key_templates.list()
        errors = await asyncio.gather(
            *[self.async_api.telephony.jobs.apply_line_key_templates.errors(job_id=job.id) for job in jobs],
            return_exceptions=True)
        err = next((d for d in errors if isinstance(d, Exception)), None)
        if err:
            raise err
        print(f'got errors for {len(errors)} jobs')

    def test_apply_job(self):
        """
        Apply line key template job, default like key template
        """
        api = self.api.telephony.jobs.apply_line_key_templates
        r = self.api.telephony.devices.preview_apply_line_key_template(
            action=ApplyLineKeyTemplateAction.apply_default_templates,
            exclude_devices_with_custom_layout=True)
        job = api.apply(
            action=ApplyLineKeyTemplateAction.apply_default_templates,
            exclude_devices_with_custom_layout=True)
        print(json.dumps(job.model_dump(mode='json', exclude_none=True, by_alias=True), indent=2))
        # wait for job to complete
        while True:
            status = api.status(job_id=job.id)
            print(json.dumps(status.model_dump(mode='json', exclude_none=True, by_alias=True), indent=2))
            print()
            if status.latest_execution_status == 'COMPLETED':
                break
            sleep(10)
        self.assertEqual(r, status.updated_count)

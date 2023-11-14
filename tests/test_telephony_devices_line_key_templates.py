"""
Test Line key template operations
"""
import asyncio
import json
from random import choice

from tests.base import TestCaseWithLog, async_test, TestWithLocations
from wxc_sdk.common import ApplyLineKeyTemplateAction
from wxc_sdk.devices import Device, ProductType
from wxc_sdk.telephony import NumberType, OwnerType, NumberListPhoneNumber, SupportedDevice
from wxc_sdk.telephony.devices import LineKeyTemplate, ProgrammableLineKey, LineKeyType


class TestLineKeyTemplate(TestCaseWithLog):
    def test_list(self):
        """
        list all line key templates
        """
        api = self.api.telephony.devices
        lkts = list(api.list_line_key_templates())
        foo = 1

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
        foo = 1

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
        supported: list[SupportedDevice]
        devices: list[Device]
        lkts: list[LineKeyTemplate]

        model_8865 = next(d.model for d in supported if '8865' in d.model)
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
    def test_preview_apply(self):
        """
        try to apply a line key template
        """
        lkts = list(self.api.telephony.devices.list_line_key_templates())
        if not lkts:
            self.skipTest('No line key templates')
        target_lkt = choice(lkts)
        all_location_ids = [loc.location_id for loc in self.locations]
        r = self.api.telephony.devices.preview_apply_line_key_template(
            action=ApplyLineKeyTemplateAction.apply_default_templates)
        foo = 1

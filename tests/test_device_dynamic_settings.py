import asyncio
import json
from collections import Counter, defaultdict
from random import choice
from time import sleep

from pydantic import TypeAdapter

from tests.base import TestWithLocations, async_test
from wxc_sdk.all_types import *


class TestDynamicSettings(TestWithLocations):
    def test_supported_devices(self):
        """
        Test getting supported devices and their family display names
        """
        supported_devices = self.api.telephony.supported_devices()
        devices_by_family_display_name = defaultdict(list)
        for device in supported_devices.devices:
            if not device.family_display_name:
                continue
            devices_by_family_display_name[device.family_display_name].append(device)
        for family_display_name, devices in devices_by_family_display_name.items():
            print(f'Family display name: {family_display_name}, Count: {len(devices)}')
            for device in devices:
                print(f' - {device.model} ({device.family_display_name})')

    def test_get_settings_groups(self):
        """
        Test getting dynamic settings groups
        """
        api = self.api.telephony.devices.dynamic_settings
        groups = api.get_settings_groups(include_settings_type=SettingsType.all)
        print(json.dumps(groups.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        family_or_model_display_names = set(g.family_or_model_display_name for g in groups.settings_groups)

        print(f'Found {len(groups.settings_groups)} settings groups')
        print(f'Found {len(groups.settings_tabs)} settings tabs')
        print(f'Family or model display names: {", ".join(sorted(family_or_model_display_names))}')
        self.assertGreater(len(groups.settings_groups), 0)

    def test_get_settings_groups_all(self):
        """
        Test getting all dynamic settings groups, including all types
        """
        api = self.api.telephony.devices.dynamic_settings
        groups = api.get_settings_groups()
        groups_all = api.get_settings_groups(include_settings_type=SettingsType.all)
        print(f'Found {len(groups.settings_groups)} settings groups')
        print(f'Found {len(groups_all.settings_groups)} settings groups (including all types)')

    def test_settings_per_tab(self):
        """
        Test counting settings per tab in dynamic settings groups
        """
        api = self.api.telephony.devices.dynamic_settings
        groups = api.get_settings_groups()
        counter = Counter(g.tab for g in groups.settings_groups)
        for tag, c in counter.items():
            print(f'Tab: {tag}, Count: {c}')

    def test_get_validation_schema(self):
        """
        Test getting validation schema
        """
        api = self.api.telephony.devices.dynamic_settings
        schema = api.get_validation_schema()
        print(json.dumps(TypeAdapter(list[DeviceTag]).dump_python(schema, mode='json', by_alias=True,
                                                                  exclude_unset=True), indent=2))

    @async_test
    async def test_get_location_device_dynamic_settings(self):
        """
        Test getting dynamic settings for devices in all telephony locations
        """
        api = self.async_api.telephony.devices.dynamic_settings
        groups = await api.get_settings_groups()
        family_or_model_display_names = list(set(g.family_or_model_display_name for g in groups.settings_groups))

        settings = await asyncio.gather(*[api.get_location_device_settings(loc.location_id,
                                                                           fmdn)
                                          for fmdn in family_or_model_display_names
                                          for loc in self.telephony_locations])
        print(f'Got dynamic devices settings for {len(settings)} locations')

    @async_test
    async def test_get_customer_device_dynamic_settings(self):
        """
        Test getting dynamic settings for devices across the organization
        """
        api = self.async_api.telephony.devices.dynamic_settings
        groups = await api.get_settings_groups()
        family_or_model_display_names = list(set(g.family_or_model_display_name for g in groups.settings_groups))
        settings = await asyncio.gather(*[api.get_customer_device_settings(fmdn)
                                          for fmdn in family_or_model_display_names])
        print(f'Got dynamic devices settings for {len(settings)} family or model display names')
        for fmdn, org_settings in zip(family_or_model_display_names, settings):
            print(f'Family or model display name: {fmdn}, Tags: {len(org_settings.tags)}')
            for tag in org_settings.tags:
                print(f' - {tag.tag}: {tag.value} (parent value: {tag.parent_value}, parent level: {tag.parent_level})')

    def test_each_tag_has_a_validation_rule(self):
        """
        Test that each tag has a validation rule
        """
        api = self.api.telephony.devices.dynamic_settings
        groups = api.get_settings_groups()
        validation_schema = api.get_validation_schema()
        validations: dict[str, dict[str, DeviceTag]] = defaultdict(dict)
        for device_tag in validation_schema:
            validations[device_tag.family_or_model_display_name][device_tag.tag] = device_tag

        err = None
        for group in groups.settings_groups:
            for tags in group.tags:
                for tag in tags.tag_block:
                    try:
                        validation = validations[group.family_or_model_display_name][tag]
                    except KeyError as e:
                        err = err or e
                        print(f'No validation rule for {group.family_or_model_display_name} / {tag}')
                        continue
        if err:
            raise err

    def test_updates_dynamic_device_settings_across_organization(self):
        """
        Test that updates to dynamic device settings are applied across the organization
        """
        api = self.api.telephony.devices.dynamic_settings

        # pick a family or model display name
        groups = api.get_settings_groups()
        family_or_model_display_names = list(set(g.family_or_model_display_name for g in groups.settings_groups))
        fmdn: str = choice(family_or_model_display_names)
        print(f'Family or model display name: {fmdn}')

        # get org settings
        org_settings = api.get_customer_device_settings(fmdn)

        # pick a setting
        candidates = [tag for tag in org_settings.tags if tag.value is None]
        tag: DeviceDynamicTag = choice(candidates)

        # update the setting
        japi = self.api.telephony.jobs.dynamic_device_settings
        update_tags = [DynamicSettingsUpdateJobItem(family_or_model_display_name=tag.family_or_model_display_name,
                                                    tag=tag.tag,
                                                    action=SetOrClear.set,
                                                    value=tag.parent_value)]
        print(f'Updating tag: {tag.family_or_model_display_name} / {tag.tag} to {tag.parent_value}')
        job = japi.update_across_org_or_location(update_tags)
        # monitor job to complete
        while True:
            status = japi.status(job.id)
            print(f'Job status: {status.latest_execution_status}')
            if status.latest_execution_status in ('COMPLETED', 'FAILED'):
                break
            sleep(5)
        print(f'Job completed with status: {status.latest_execution_status}')

    @async_test
    async def test_find_non_default_settings(self):
        """
        Test finding non-default settings across the organization
        """
        api = self.async_api.telephony.devices.dynamic_settings

        # for all family or model display names
        groups = await api.get_settings_groups()
        family_or_model_display_names = list(set(g.family_or_model_display_name for g in groups.settings_groups))
        settings: list[DeviceDynamicSettings] = await asyncio.gather(
            *[api.get_customer_device_settings(fmdn) for fmdn in family_or_model_display_names])

        # get org settings and find non-default tags
        for fmdn, org_settings in zip(family_or_model_display_names, settings):
            non_default_tags = [tag for tag in org_settings.tags if tag.value is not None]
            print(f'Found {len(non_default_tags)} non-default tags for {fmdn}')
            for tag in non_default_tags:
                print(f' - {tag.tag}: {tag.parent_value}')

    def test_reset_non_default_settings(self):
        """
        Test resetting non-default settings across the organization
        """

        def reset_non_default_settings(fmdn: str):
            """
            Reset non-default settings for a given family or model display name
            """
            org_settings = api.get_customer_device_settings(fmdn)

            non_default_tags = [tag for tag in org_settings.tags if tag.value is not None]
            print(f'Found {len(non_default_tags)} non-default tags for {fmdn}')
            if not non_default_tags:
                return

            # reset the tags
            update_tags = [DynamicSettingsUpdateJobItem(family_or_model_display_name=tag.family_or_model_display_name,
                                                        tag=tag.tag,
                                                        action=SetOrClear.clear)
                           for tag in non_default_tags]
            print(f'Resetting {len(update_tags)} tags for {fmdn}')
            japi = self.api.telephony.jobs.dynamic_device_settings
            job = japi.update_across_org_or_location(update_tags)
            # monitor job to complete
            while True:
                status = japi.status(job.id)
                print(f'Job status: {status.latest_execution_status}')
                if status.latest_execution_status in ('COMPLETED', 'FAILED'):
                    break
                sleep(5)
            print(f'Job completed with status: {status.latest_execution_status}')
            return

        api = self.api.telephony.devices.dynamic_settings

        # for all family or model display names
        groups = api.get_settings_groups()
        family_or_model_display_names = list(set(g.family_or_model_display_name for g in groups.settings_groups))
        for fmdn in family_or_model_display_names:
            reset_non_default_settings(fmdn)

"""
test cases for voicemail groups
"""
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from functools import reduce
from random import choice
from re import match

from wxc_sdk.rest import RestError
from wxc_sdk.telephony.voicemail_groups import VoicemailGroupDetail, VoicemailGroup

from .base import TestCaseWithLog


class TestVmGroup(TestCaseWithLog):

    @contextmanager
    def assert_vmg(self) -> VoicemailGroup:
        """
        Get a traget
        :return:
        """
        vmg = self.api.telephony.voicemail_groups
        groups = None
        for _ in range(2):
            with self.no_log():
                groups = list(g for g in vmg.list()
                              if match(r'^test_\d{3}$', g.name))
            if groups:
                break
            with self.no_log():
                self.test_003_create()
        if not groups:
            self.skipTest('No voicemail groups to mess with')
        group = choice(groups)
        try:
            yield group
        finally:
            try:
                with self.no_log():
                    vmg.delete(location_id=group.location_id,
                               voicemail_group_id=group.group_id)
            except RestError as e:
                if e.response.status_code != 404 or e.code != 4008:
                    raise

    def test_001_list(self):
        """
        list voicemail groups
        """
        with self.assert_vmg():
            vmg = self.api.telephony.voicemail_groups
            groups = list(vmg.list())
            print(f'Got {len(groups)} voicemail groups')

    def test_002_details(self):
        """
        get details for all VM groups
        """
        with self.assert_vmg():
            api = self.api.telephony.voicemail_groups
            groups = list(api.list())
            with ThreadPoolExecutor() as pool:
                details = list(pool.map(lambda g: api.details(location_id=g.location_id,
                                                              voicemail_group_id=g.group_id),
                                        groups))
            print(f'Got details for {len(groups)} voicemail groups')

    def test_003_create(self):
        """
        Create a simple voicemail group
        """
        with self.no_log():
            # pick target location
            locations = list(self.api.locations.list())
            location = choice(locations)

            # get unique name for new group
            vmg = self.api.telephony.voicemail_groups
            groups = list(vmg.list())
            vmg_name = next(name for i in range(1, 1000)
                            if (name := f'test_{i:03}') not in set(g.name for g in groups))
            # get extension within location
            extensions = set(n.extension for n in self.api.telephony.phone_numbers(location_id=location.location_id)
                             if n.extension)
            if extensions:
                first_digits: dict[str, set[str]] = reduce(lambda red, e: red[e[:1]].add(e) or red,
                                                           extensions, defaultdict(set))
                first_digit = max(first_digits, key=lambda fd: len(first_digits[fd]))
                extensions = first_digits[first_digit]
                extension = next(ext for i in range(1, 1000)
                                 if (ext := f'{first_digit}{i:03}') not in extensions)
            else:
                extension = '1000'
        # create voicemail group
        settings = VoicemailGroupDetail.create(
            name=vmg_name, extension=extension, first_name='test', last_name=vmg_name,
            passcode=740384,
            language_code='en_us')
        vmg_id = vmg.create(location_id=location.location_id,
                            settings=settings)
        print(f'Created new voicemail group "{vmg_name} in location "{location.name}" with extension {extension}')

    def test_004_update(self):
        """
        Try to update a VNG
        """
        with self.assert_vmg() as group:
            group: VoicemailGroup
            api = self.api.telephony.voicemail_groups
            details = api.details(location_id=group.location_id, voicemail_group_id=group.group_id)
            api.update(location_id=group.location_id, voicemail_group_id=group.group_id, settings=details)
            after = api.details(location_id=group.location_id, voicemail_group_id=group.group_id)
            self.assertEqual(details, after)

    def test_005_update_enabled(self):
        """
        Try to update a VNG: toggle the enabled settings
        """
        with self.assert_vmg() as group:
            group: VoicemailGroup
            api = self.api.telephony.voicemail_groups
            # get details
            details = api.details(location_id=group.location_id, voicemail_group_id=group.group_id)
            try:
                # toggle enabled
                enabled = not details.enabled
                settings = VoicemailGroupDetail(enabled=enabled)
                api.update(location_id=group.location_id, voicemail_group_id=group.group_id, settings=settings)
                # get updated info and make sure that the updated worked
                after = api.details(location_id=group.location_id, voicemail_group_id=group.group_id)
                expected = details.copy(deep=True)
                expected.enabled = enabled
                self.assertEqual(expected, after)
            finally:
                # restore old settings
                api.update(location_id=group.location_id, voicemail_group_id=group.group_id, settings=details)

    def test_006_delete(self):
        """
        Delete a voicemail group
        """
        with self.assert_vmg() as group:
            group: VoicemailGroup
            api = self.api.telephony.voicemail_groups
            print(f'Deleting voicemail group "{group.name}" in location "{group.location_name}"')
            api.delete(location_id=group.location_id, voicemail_group_id=group.group_id)

            # make sure the group is gone
            groups = list(api.list(location_id=group.location_id))
            self.assertIsNone(next((g for g in groups if g.name == group.name), None))

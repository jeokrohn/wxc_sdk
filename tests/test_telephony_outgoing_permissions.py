"""
test cases for location outgoing permission settings
"""
import json
from concurrent.futures import ThreadPoolExecutor
import random

from wxc_sdk.person_settings.permissions_out import AutoTransferNumbers, CallTypePermission, Action, \
    OutgoingPermissions, CallingPermissions, DigitPattern
from tests.base import TestWithLocations, TestCaseWithLog
from wxc_sdk.telephony import OriginatorType, ConfigurationLevel


class TestPermOut(TestWithLocations):

    def test_001_read_all(self):
        po = self.api.telephony.permissions_out
        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda loc: po.read(entity_id=loc.location_id),
                                     self.locations))
        print(f'Got outgoing permission settings for {len(settings)} locations')

    def test_002_read_transfer_numbers(self):
        po = self.api.telephony.permissions_out
        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda loc: po.transfer_numbers.read(entity_id=loc.location_id),
                                     self.locations))
        print(f'Got outgoing permission transfer numbers for {len(settings)} locations')

    def test_003_update_one_number(self):
        """
        try to update auto transfer numbers for a location
        """
        tna = self.api.telephony.permissions_out.transfer_numbers
        target_location = random.choice(self.locations)
        numbers = tna.read(entity_id=target_location.location_id)
        try:
            # change auto transfer number 1
            update = numbers.model_copy(deep=True)
            transfer = f'+496100773{random.randint(0, 9999):03}'
            update.auto_transfer_number1 = transfer
            tna.configure(entity_id=target_location.location_id, settings=update)

            # verify update
            updated = tna.read(entity_id=target_location.location_id)
            # number should be equal; ignore hyphens in number returned by API
            self.assertEqual(transfer, updated.auto_transfer_number1.replace('-', ''))
            # other than that the updated numbers should be identical to the numbers before
            updated.auto_transfer_number1 = numbers.auto_transfer_number1
            self.assertEqual(numbers, updated)
        finally:
            # restore old settings
            tna.configure(entity_id=target_location.location_id, settings=numbers.configure_unset_numbers)
            restored = tna.read(entity_id=target_location.location_id)
            self.assertEqual(numbers, restored)
        # try

    def test_002_update_one_number_no_effect_on_other_numbers(self):
        """
        try to update auto transfer numbers for a workspace. Verify that updating a single number doesn't affect the
        other numbers
        """
        tna = self.api.telephony.permissions_out.transfer_numbers
        target_location = random.choice(self.locations)
        numbers = tna.read(entity_id=target_location.location_id)
        try:
            all_numbers_set = AutoTransferNumbers(auto_transfer_number1='+4961007738001',
                                                  auto_transfer_number2='+4961007738002',
                                                  auto_transfer_number3='+4961007738003')
            tna.configure(entity_id=target_location.location_id, settings=all_numbers_set)
            all_numbers_set = tna.read(entity_id=target_location.location_id)

            # change auto transfer number 1
            transfer = f'+496100773{random.randint(0, 9999):03}'
            update = AutoTransferNumbers(auto_transfer_number1=transfer)
            tna.configure(entity_id=target_location.location_id, settings=update)

            # verify update
            updated = tna.read(entity_id=target_location.location_id)
            # number should be equal; ignore hyphens in number returned by API
            self.assertEqual(transfer, updated.auto_transfer_number1.replace('-', ''))
            # other than that the updated numbers should be identical to the numbers before
            updated.auto_transfer_number1 = all_numbers_set.auto_transfer_number1
            self.assertEqual(all_numbers_set, updated)
        finally:
            # restore old settings
            tna.configure(entity_id=target_location.location_id, settings=numbers.configure_unset_numbers)
            restored = tna.read(entity_id=target_location.location_id)
            self.assertEqual(numbers, restored)
        # try


class TestDarmstadt(TestCaseWithLog):
    def test_national_call_from_darmstadt_blocked_at_user_level(self):
        # find location
        location = next(self.api.locations.list(name='Darmstadt'))
        # make sure that national calls are allowed at the location level
        location_permissions = self.api.telephony.permissions_out.read(entity_id=location.location_id)
        self.assertEqual(Action.allow, location_permissions.calling_permissions.national.action)

        with self.no_log():
            user = self.api.people.me()
        user = self.api.people.details(calling_data=True, person_id=user.person_id)
        upa = self.api.person_settings.permissions_out

        # clear all pattern based permission setting at user level
        upa.digit_patterns.delete_all(entity_id=user.person_id)
        # block national level
        user_permissions_before = upa.read(entity_id=user.person_id)
        try:
            upa.configure(entity_id=user.person_id,
                          settings=OutgoingPermissions(
                              use_custom_permissions=True,
                              calling_permissions=CallingPermissions(
                                  national=CallTypePermission(action=Action.block,
                                                              transfer_enabled=False))))
            # validate a call to +4961967739764 (should be blocked)
            result = self.api.telephony.test_call_routing(originator_id=user.person_id,
                                                          originator_type=OriginatorType.user,
                                                          destination='+4961967739764', include_applied_services=True)
            print('Routing result:')
            print(json.dumps(result.model_dump(mode='json', exclude_unset=True, by_alias=True), indent=2))
            self.assertTrue(result.is_rejected, 'Call should be rejected')
            # there should be one applied service
            self.assertEqual(1, len(result.applied_services))
            applied_service = result.applied_services[0]
            self.assertIsNotNone(applied_service.outgoing_calling_plan_permissions_by_type)
            ocp_by_type = applied_service.outgoing_calling_plan_permissions_by_type
            self.assertEqual('NATIONAL', ocp_by_type.call_type)
            self.assertEqual(Action.block, ocp_by_type.permission)
            self.assertEqual(ConfigurationLevel.people, ocp_by_type.configuration_level)
        finally:
            upa.configure(entity_id=user.person_id,
                          settings=user_permissions_before)
        return

    def test_national_call_from_darmstadt_blocked_by_pattern_at_user_level(self):
        # find location
        location = next(self.api.locations.list(name='Darmstadt'))
        # make sure that national calls are allowed at the location level
        location_permissions = self.api.telephony.permissions_out.read(entity_id=location.location_id)
        self.assertEqual(Action.allow, location_permissions.calling_permissions.national.action)

        with self.no_log():
            user = self.api.people.me()
        user = self.api.people.details(calling_data=True, person_id=user.person_id)
        upa = self.api.person_settings.permissions_out

        # clear all pattern baed permission setting at user level
        user_category_control = upa.digit_patterns.get_digit_patterns(
            entity_id=user.person_id).use_custom_digit_patterns
        upa.digit_patterns.update_category_control_settings(entity_id=user.person_id, use_custom_digit_patterns=True)
        # make sure there is exactly one pattern
        upa.digit_patterns.delete_all(entity_id=user.person_id)
        block_pattern = DigitPattern(name='block496196', pattern='+496196!', action=Action.block,
                                     transfer_enabled=False)
        upa.digit_patterns.create(entity_id=user.person_id,
                                  pattern=block_pattern)
        upa.digit_patterns.get_digit_patterns(entity_id=user.person_id)

        # save old permission settings
        user_permissions_before = upa.read(entity_id=user.person_id)
        try:
            # set user level permissions to use location level settings
            upa.configure(entity_id=user.person_id,
                          settings=OutgoingPermissions(use_custom_permissions=False))
            user_permissions_after = upa.read(entity_id=user.person_id)
            # validate a call to +4961967739764 (should be blocked)
            result = self.api.telephony.test_call_routing(originator_id=user.person_id,
                                                          originator_type=OriginatorType.user,
                                                          destination='+4961967739764',
                                                          include_applied_services=True)
            print('Routing result:')
            print(json.dumps(result.model_dump(mode='json', exclude_unset=True, by_alias=True), indent=2))
            self.assertTrue(result.is_rejected, 'Call should be rejected')
            # there should be one applied service
            self.assertEqual(1, len(result.applied_services))
            applied_service = result.applied_services[0]
            self.assertIsNotNone(applied_service.outgoing_calling_plan_permissions_by_digit_pattern)
            ocp_by_dp = applied_service.outgoing_calling_plan_permissions_by_digit_pattern
            self.assertEqual(ConfigurationLevel.people, ocp_by_dp.configuration_level)
            self.assertEqual(Action.block, ocp_by_dp.permission)
            self.assertEqual(block_pattern.name, ocp_by_dp.name)
            self.assertEqual(block_pattern.pattern, ocp_by_dp.pattern)
        finally:
            upa.configure(entity_id=user.person_id,
                          settings=user_permissions_before)
            upa.digit_patterns.update_category_control_settings(entity_id=user.person_id,
                                                                use_custom_digit_patterns=user_category_control)
        return

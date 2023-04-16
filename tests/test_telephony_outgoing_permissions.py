"""
test cases for location outgoing permission settings
"""
from concurrent.futures import ThreadPoolExecutor
import random

from wxc_sdk.person_settings.permissions_out import AutoTransferNumbers
from tests.base import TestWithLocations


class TestPermOut(TestWithLocations):

    def test_001_read_all(self):
        po = self.api.telephony.permissions_out
        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda loc: po.read(person_id=loc.location_id),
                                     self.locations))
        print(f'Got outgoing permission settings for {len(settings)} locations')

    def test_002_read_transfer_numbers(self):
        po = self.api.telephony.permissions_out
        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda loc: po.transfer_numbers.read(person_id=loc.location_id),
                                     self.locations))
        print(f'Got outgoing permission transfer numbers for {len(settings)} locations')

    def test_003_update_one_number(self):
        """
        try to update auto transfer numbers for a location
        """
        tna = self.api.telephony.permissions_out.transfer_numbers
        target_location = random.choice(self.locations)
        numbers = tna.read(person_id=target_location.location_id)
        try:
            # change auto transfer number 1
            update = numbers.copy(deep=True)
            transfer = f'+496100773{random.randint(0, 9999):03}'
            update.auto_transfer_number1 = transfer
            tna.configure(person_id=target_location.location_id, settings=update)

            # verify update
            updated = tna.read(person_id=target_location.location_id)
            # number should be equal; ignore hyphens in number returned by API
            self.assertEqual(transfer, updated.auto_transfer_number1.replace('-', ''))
            # other than that the updated numbers should be identical to the numbers before
            updated.auto_transfer_number1 = numbers.auto_transfer_number1
            self.assertEqual(numbers, updated)
        finally:
            # restore old settings
            tna.configure(person_id=target_location.location_id, settings=numbers.configure_unset_numbers)
            restored = tna.read(person_id=target_location.location_id)
            self.assertEqual(numbers, restored)
        # try

    def test_002_update_one_number_no_effect_on_other_numbers(self):
        """
        try to update auto transfer numbers for a workspace. Verify that updating a single number doesn't affect the
        other numbers
        """
        tna = self.api.telephony.permissions_out.transfer_numbers
        target_location = random.choice(self.locations)
        numbers = tna.read(person_id=target_location.location_id)
        try:
            all_numbers_set = AutoTransferNumbers(auto_transfer_number1='+4961007738001',
                                                  auto_transfer_number2='+4961007738002',
                                                  auto_transfer_number3='+4961007738003')
            tna.configure(person_id=target_location.location_id, settings=all_numbers_set)
            all_numbers_set = tna.read(person_id=target_location.location_id)

            # change auto transfer number 1
            transfer = f'+496100773{random.randint(0, 9999):03}'
            update = AutoTransferNumbers(auto_transfer_number1=transfer)
            tna.configure(person_id=target_location.location_id, settings=update)

            # verify update
            updated = tna.read(person_id=target_location.location_id)
            # number should be equal; ignore hyphens in number returned by API
            self.assertEqual(transfer, updated.auto_transfer_number1.replace('-', ''))
            # other than that the updated numbers should be identical to the numbers before
            updated.auto_transfer_number1 = all_numbers_set.auto_transfer_number1
            self.assertEqual(all_numbers_set, updated)
        finally:
            # restore old settings
            tna.configure(person_id=target_location.location_id, settings=numbers.configure_unset_numbers)
            restored = tna.read(person_id=target_location.location_id)
            self.assertEqual(numbers, restored)
        # try

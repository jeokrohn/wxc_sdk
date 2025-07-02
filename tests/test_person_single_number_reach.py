import asyncio
import base64
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import contextmanager
from random import choice

from tests.base import TestWithLocations, async_test, TestCaseWithUsers
from wxc_sdk.people import Person
from wxc_sdk.person_settings.single_number_reach import SingleNumberReachNumber

def decoded_snr_number_id(snr_number_id: str):
    """
    decode SNR number id
    """
    decoded = base64.b64decode(snr_number_id+'==').decode()
    decoded_id = base64.b64decode(decoded.split('/')[-1]).decode()
    return f'{decoded}({decoded_id})'

class TestSingleNumberReach(TestWithLocations, TestCaseWithUsers):

    @contextmanager
    def target_user(self, keep_log: bool = True):
        """
        get a target user and restore settings after tests
        """
        target = choice(self.users)
        print(f'Target user: {target.display_name}')
        api = self.api.person_settings.single_number_reach
        with self.no_log(keep_log):
            before = api.read(target.person_id)
            if before.numbers:
                # delete existing SNR numbers
                with ThreadPoolExecutor() as pool:
                    # delete all existing numbers
                    list(pool.map(lambda n: api.delete_snr(target.person_id, n.id),
                                  before.numbers))
        try:
            yield target
        finally:
            with self.no_log(keep_log):
                after = api.read(target.person_id)
                with ThreadPoolExecutor() as pool:
                    # delete all existing numbers
                    list(pool.map(lambda n: api.delete_snr(target.person_id, n.id),
                                  after.numbers))
                    # re-create existing SNR numbers
                    list(pool.map(lambda n: api.create_snr(target.person_id, n),
                                  before.numbers))
        return

    @contextmanager
    def target_user_with_snr(self, keep_log: bool = True):
        """
        get a target user with SNR numbers and restore settings after tests
        """
        with self.target_user(keep_log) as target:
            target: Person
            # create a SNR number and enable it
            phone_number = '+4961967739764'
            snr_number = SingleNumberReachNumber(
                enabled=True,
                phone_number=phone_number,
                name='mobile'
            )
            api = self.api.person_settings.single_number_reach
            with self.no_log(keep_log):
                api.create_snr(target.person_id, snr_number)
            yield target

    @async_test
    async def test_available_phone_numbers(self):
        """
        Get available phone numbers for all telephony locations
        """
        api = self.async_api.person_settings.single_number_reach
        results = await asyncio.gather(*[api.available_phone_numbers(location_id=loc.location_id)
                                         for loc in self.telephony_locations],
                                       return_exceptions=True)
        err = None
        for location, result in zip(self.locations, results):
            if isinstance(result, Exception):
                print(f'Error getting available phone numbers for {location.name}: {result}')
                err = err or result
            else:
                print(f'Available phone numbers for {location.name}: {len(result)}')
        if err:
            raise err

    @async_test
    async def test_read_settings(self):
        """
        Read settings for all calling users
        """
        api = self.async_api.person_settings.single_number_reach
        results = await asyncio.gather(*[api.read(person_id=user.person_id)
                                         for user in self.users],
                                       return_exceptions=True)
        err = None
        for user, result in zip(self.users, results):
            if isinstance(result, Exception):
                print(f'Error reading settings for {user.display_name}: {result}')
                err = err or result
            else:
                print(f'Settings for {user.display_name}: {result}')
        if err:
            raise err
        return

    def test_enable_snr(self):
        """
        Enable SNR for a user
        """
        api = self.api.person_settings.single_number_reach
        with self.target_user() as target:
            target: Person
            # create a SNR number and enable it
            phone_number = '+4961967739764'
            snr_number = SingleNumberReachNumber(
                enabled=True,
                phone_number=phone_number,
                name='mobile'
            )
            api.create_snr(target.person_id, snr_number)
            after = api.read(target.person_id)
            self.assertIsNotNone(next((n for n in after.numbers if n.phone_number == phone_number), None),
                                 'SNR number not present')
            self.assertTrue(after.enabled)
        return

    def test_disable_snr(self):
        """
        Disable SNR for a user by disabling a number
        """
        api = self.api.person_settings.single_number_reach
        with self.target_user_with_snr() as target:
            target: Person
            before = api.read(target.person_id)
            self.assertTrue(before.enabled)
            self.assertEqual(len(before.numbers), 1)
            # disable 1st SNR number
            snr_number = before.numbers[0]
            snr_number.enabled = False
            api.update_snr(target.person_id, snr_number)
            after = api.read(target.person_id)
            self.assertFalse(after.enabled)
            self.assertEqual(len(after.numbers), 1)
            self.assertEqual(snr_number, after.numbers[0])
        return

    def test_disable_snr_partial_update(self):
        """
        Disable SNR for a user by disabling a number using a partial update
        """
        api = self.api.person_settings.single_number_reach
        with self.target_user_with_snr() as target:
            target: Person
            before = api.read(target.person_id)
            self.assertTrue(before.enabled)
            self.assertEqual(len(before.numbers), 1)
            # disable 1st SNR number
            snr_number = before.numbers[0]
            snr_number.enabled = False
            snr_update = SingleNumberReachNumber(
                **snr_number.model_dump(
                    mode='json',
                    by_alias=True,
                    exclude_unset=True,
                    exclude={'do_not_forward_calls_enabled', 'answer_confirmation_enabled',
                             'name'}))
            api.update_snr(target.person_id, snr_update)
            after = api.read(target.person_id)
            self.assertFalse(after.enabled)
            self.assertEqual(len(after.numbers), 1)
        return

    def test_change_snr_number(self):
        """
        Change SNR number
        """
        api = self.api.person_settings.single_number_reach
        with self.target_user_with_snr() as target:
            target: Person
            before = api.read(target.person_id)
            self.assertEqual(len(before.numbers), 1)
            # change 1st SNR number
            snr_number = before.numbers[0]
            snr_number.phone_number = '+4961967739765'
            new_id = api.update_snr(target.person_id, snr_number)
            after = api.read(target.person_id)
            self.assertEqual(len(after.numbers), 1)
            self.assertEqual(after.numbers[0].phone_number, snr_number.phone_number)
            self.assertEqual(after.numbers[0].id, new_id)
            # verify that the id has the encoded phone number
            self.assertEqual(decoded_snr_number_id(after.numbers[0].id).split('(')[-1].strip(')'), snr_number.phone_number)
        return

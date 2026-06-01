import asyncio
import base64
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import contextmanager

from tests.base import TestWithTempCallingUser, async_test
from wxc_sdk.people import Person
from wxc_sdk.person_settings.single_number_reach import SingleNumberReachNumber


def decoded_snr_number_id(snr_number_id: str):
    """
    decode SNR number id
    """
    decoded = base64.b64decode(snr_number_id + '==').decode()
    decoded_id = base64.b64decode(decoded.split('/')[-1]).decode()
    return f'{decoded}({decoded_id})'


class TestSingleNumberReach(TestWithTempCallingUser):
    """
    Stateful single number reach tests using a disposable calling user.
    """

    @contextmanager
    def target_user(self, keep_log: bool = True):
        """
        get a target user and restore settings after tests
        """
        # Use the disposable calling user and snapshot existing SNR numbers.
        target = self.user
        print(f'Target user: {target.display_name}')
        api = self.api.person_settings.single_number_reach
        with self.no_log(keep_log):
            before = api.read(target.person_id)
            if before.numbers:
                # Clear existing SNR numbers so the test body starts from a known state.
                with ThreadPoolExecutor() as pool:
                    list(pool.map(lambda n: api.delete_snr(target.person_id, n.id), before.numbers or []))
        try:
            yield target
        finally:
            with self.no_log(keep_log):
                # Remove any SNR numbers created by the test body.
                after = api.read(target.person_id)
                with ThreadPoolExecutor() as pool:
                    list(pool.map(lambda n: api.delete_snr(target.person_id, n.id), after.numbers or []))

                    # Re-create the original SNR numbers to leave the user unchanged.
                    list(pool.map(lambda n: api.create_snr(target.person_id, n), before.numbers or []))
        return

    @contextmanager
    def target_user_with_snr(self, keep_log: bool = True):
        """
        get a target user with SNR numbers and restore settings after tests
        """
        # Start from a clean target user and create one enabled SNR number for the test body.
        with self.target_user(keep_log) as target:
            target: Person
            phone_number = '+4961967739764'
            snr_number = SingleNumberReachNumber(enabled=True, phone_number=phone_number, name='mobile')
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

        # Query available SNR phone numbers for all telephony locations concurrently.
        results = await asyncio.gather(
            *[api.available_phone_numbers(location_id=loc.location_id) for loc in self.telephony_locations],
            return_exceptions=True,
        )

        # Print counts for successful locations and surface the first error, if any.
        err = None
        for location, result in zip(self.locations, results):
            if isinstance(result, Exception):
                print(f'Error getting available phone numbers for {location.name}: {result}')
                err = err or result
            else:
                print(f'Available phone numbers for {location.name}: {len(result)}')
        if err:
            raise err

    def test_read_settings(self):
        """
        Read settings for the temporary calling user
        """
        api = self.api.person_settings.single_number_reach

        # Read and print the disposable user's SNR settings for basic read coverage.
        result = api.read(person_id=self.user.person_id)
        print(f'Settings for {self.user.display_name}: {result}')
        return

    def test_enable_snr(self):
        """
        Enable SNR for a user
        """
        api = self.api.person_settings.single_number_reach

        # Use a clean disposable user so creating one number controls the enabled state.
        with self.target_user() as target:
            target: Person

            # Create an enabled SNR number and verify it appears in settings.
            phone_number = '+4961967739764'
            snr_number = SingleNumberReachNumber(enabled=True, phone_number=phone_number, name='mobile')
            api.create_snr(target.person_id, snr_number)
            after = api.read(target.person_id)
            self.assertIsNotNone(
                next((n for n in after.numbers if n.phone_number == phone_number), None), 'SNR number not present'
            )

            # Adding an enabled SNR number should enable the feature.
            self.assertTrue(after.enabled)
        return

    def test_disable_snr(self):
        """
        Disable SNR for a user by disabling a number
        """
        api = self.api.person_settings.single_number_reach

        # Start with exactly one enabled SNR number.
        with self.target_user_with_snr() as target:
            target: Person
            before = api.read(target.person_id)
            self.assertTrue(before.enabled)
            self.assertEqual(len(before.numbers), 1)

            # Disable that number through a full update and verify the feature disables.
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

        # Start with exactly one enabled SNR number.
        with self.target_user_with_snr() as target:
            target: Person
            before = api.read(target.person_id)
            self.assertTrue(before.enabled)
            self.assertEqual(len(before.numbers), 1)

            # Build a partial update payload that only carries update-safe fields.
            snr_number = before.numbers[0]
            snr_number.enabled = False
            snr_update = SingleNumberReachNumber(
                **snr_number.model_dump(
                    mode='json',
                    by_alias=True,
                    exclude_unset=True,
                    exclude={'do_not_forward_calls_enabled', 'answer_confirmation_enabled', 'name'},
                )
            )

            # Apply the partial update and verify the feature disables while the number remains.
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

        # Start with exactly one enabled SNR number.
        with self.target_user_with_snr() as target:
            target: Person
            before = api.read(target.person_id)
            self.assertEqual(len(before.numbers), 1)

            # Change the phone number and capture the newly returned SNR number id.
            snr_number = before.numbers[0]
            snr_number.phone_number = '+4961967739765'
            new_id = api.update_snr(target.person_id, snr_number)
            after = api.read(target.person_id)

            # Verify the list still has one number and that it reflects the update.
            self.assertEqual(len(after.numbers), 1)
            self.assertEqual(after.numbers[0].phone_number, snr_number.phone_number)
            self.assertEqual(after.numbers[0].id, new_id)

            # Verify that the returned id encodes the updated phone number.
            self.assertEqual(
                decoded_snr_number_id(after.numbers[0].id).split('(')[-1].strip(')'), snr_number.phone_number
            )
        return

    def test_delete_snr_number(self):
        """
        Delete an SNR number and verify it is gone.
        """
        api = self.api.person_settings.single_number_reach

        # Start from a clean disposable user and create one temporary SNR number.
        with self.target_user() as target:
            target: Person
            snr_number = SingleNumberReachNumber(enabled=True, phone_number='+4961967739764', name='mobile')
            number_id = api.create_snr(target.person_id, snr_number)

            # Verify the new number appears before exercising delete.
            before_delete = api.read(target.person_id)
            self.assertIsNotNone(next((n for n in before_delete.numbers if n.id == number_id), None))

            # Delete the number and verify it is no longer returned.
            api.delete_snr(target.person_id, number_id)
            after_delete = api.read(target.person_id)
            self.assertIsNone(next((n for n in after_delete.numbers if n.id == number_id), None))
        return

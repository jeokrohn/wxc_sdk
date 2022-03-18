import os.path
import random
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from typing import Callable

from .base import TestCaseWithLog, gather
from wxc_sdk.people import Person
from wxc_sdk.person_settings.barge import BargeSettings
from wxc_sdk.person_settings.call_intercept import InterceptSetting, InterceptTypeIncoming, Greeting
from wxc_sdk.person_settings.caller_id import CallerIdSelectedType


class TestCaseWithUsers(TestCaseWithLog):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        print('Getting users...')
        users = list(cls.api.people.list(calling_data=True))
        cls.users = [user for user in users if user.location_id]
        print(f'got {len(cls.users)} users')

    def setUp(self) -> None:
        super().setUp()
        self.assertFalse(not self.users, 'Need at least one user to run test')


class TestRead(TestCaseWithUsers):
    def execute_read_test(self, f: Callable):
        with ThreadPoolExecutor() as pool:
            result_map = pool.map(lambda user: f(person_id=user.person_id), self.users)
            results = list(gather(result_map, return_exceptions=True))
        return results

    def test_001_read_barge(self):
        """
        read_barge for all users
        """
        results = self.execute_read_test(self.api.person_settings.barge.read)
        for e in (r for r in results if isinstance(r, Exception)):
            print(f'{e}')
        self.assertFalse(any(isinstance(r, Exception) for r in results))

    def test_002_read_forwarding(self):
        """
        read_barge for all users
        """
        results = self.execute_read_test(self.api.person_settings.forwarding.read)
        for e in (r for r in results if isinstance(r, Exception)):
            print(f'{e}')
        self.assertFalse(any(isinstance(r, Exception) for r in results))

    def test_003_read_call_intercept(self):
        """
        read_barge for all users
        """
        results = self.execute_read_test(self.api.person_settings.call_intercept.read)
        for e in (r for r in results if isinstance(r, Exception)):
            print(f'{e}')
        self.assertFalse(any(isinstance(r, Exception) for r in results))

    def test_004_read_call_recording(self):
        """
        read call recording settings for all users
        """
        results = self.execute_read_test(self.api.person_settings.call_recording.read)
        for e in (r for r in results if isinstance(r, Exception)):
            print(f'{e}')
        self.assertFalse(any(isinstance(r, Exception) for r in results))

    def test_005_read_caller_id(self):
        """
        read caller id settings for all users
        """
        results = self.execute_read_test(self.api.person_settings.caller_id.read)
        for e in (r for r in results if isinstance(r, Exception)):
            print(f'{e}')
        self.assertFalse(any(isinstance(r, Exception) for r in results))


class TestConfigure(TestCaseWithUsers):
    """
    Testing configure (update) endpoints
    """

    @property
    def wav_path(self) -> str:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample.wav')

    def test_004_configure_barge(self):
        """
        pick random user and try to update barge settings
        """

        @contextmanager
        def user_context():
            """
            pick a random user, save barge setting and restore setting after end of test
            """
            target_user = random.choice(self.users)
            barge_settings = self.api.person_settings.barge.read(person_id=target_user.person_id)
            print(f'target user: {target_user.display_name}: enabled: {barge_settings.enabled}, tone enabled: '
                  f'{barge_settings.tone_enabled}')
            try:
                yield target_user
            finally:
                # restore barge settings
                print(f'restore enabled: {barge_settings.enabled}, tone enabled: {barge_settings.tone_enabled}')
                self.api.person_settings.barge.configure(person_id=target_user.person_id,
                                                         barge_settings=barge_settings)

        def update_and_check(barge_settings: BargeSettings):
            """
            Update and verify barge settings
            """
            print(f'Setting enabled: {barge_settings.enabled}, tone enabled: {barge_settings.tone_enabled}')
            self.api.person_settings.barge.configure(person_id=user.person_id, barge_settings=barge_settings)
            after = self.api.person_settings.barge.read(person_id=user.person_id)
            self.assertEqual(barge_settings, after)
            return

        with user_context() as user:
            # try all barge setting variations
            user: Person
            bs = BargeSettings(enabled=True, tone_enabled=True)
            update_and_check(bs)
            bs = BargeSettings(enabled=True, tone_enabled=False)
            update_and_check(bs)
            bs = BargeSettings(enabled=False, tone_enabled=True)
            update_and_check(bs)
            bs = BargeSettings(enabled=False, tone_enabled=False)
            update_and_check(bs)

    @contextmanager
    def call_intercept_user_context(self):
        """
        pick a random user, save call intercept setting and restore setting after end of test
        """
        target_user = random.choice(self.users)
        settings = self.api.person_settings.call_intercept.read(person_id=target_user.person_id)
        print(f'target user: {target_user.display_name}: {settings} ')
        try:
            yield target_user
        finally:
            # restore settings
            print(f'restore {settings}')
            self.api.person_settings.call_intercept.configure(person_id=target_user.person_id, intercept=settings)

    def call_intercept_update_and_check(self, user: Person, settings: InterceptSetting):
        """
        Update and verify call interceptsettings
        """
        print(f'setting: {settings}')
        self.api.person_settings.call_intercept.configure(person_id=user.person_id, intercept=settings)
        after = self.api.person_settings.call_intercept.read(person_id=user.person_id)
        self.assertEqual(settings, after)
        return

    def test_005_configure_call_intercept(self):
        """
        try to update call intercept settings of a user
        :return:
        """

        with self.call_intercept_user_context() as user:
            user: Person
            intercept = InterceptSetting.default()
            intercept.enabled = True
            self.call_intercept_update_and_check(user=user, settings=intercept)
            # TODO: add more tests

    def test_006_upload_intercept_greeting(self):
        """
        test to upload a custom greeting for call intercept
        :return:
        """
        with self.call_intercept_user_context() as user:
            ps = self.api.person_settings
            ps.call_intercept.greeting(person_id=user.person_id, content=self.wav_path)
            intercept = ps.call_intercept.read(person_id=user.person_id)
        self.assertEqual(os.path.basename(self.wav_path), intercept.incoming.announcements.file_name)

    def test_007_upload_intercept_greeting_from_open_file(self):
        """
        test to upload a custom greeting for call intercept from an open file
        :return:
        """
        with self.call_intercept_user_context() as user:
            with open(self.wav_path, mode='rb') as wav_file:
                upload_as = f'w{uuid.uuid4()}.wav'
                ps = self.api.person_settings
                ps.call_intercept.greeting(person_id=user.person_id, content=wav_file,
                                           upload_as=upload_as)
                intercept = ps.call_intercept.read(person_id=user.person_id)
        self.assertEqual(upload_as, intercept.incoming.announcements.file_name)

    def test_008_incoming_intercept_with_custom_greeting(self):
        """
        set tup incoming intercept w/ custom greeting
        """
        with self.call_intercept_user_context() as user:
            ps = self.api.person_settings
            intercept = ps.call_intercept.read(person_id=user.person_id)
            intercept.incoming.intercept_type = InterceptTypeIncoming.intercept_all
            intercept.incoming.announcements.greeting = Greeting.custom

            # first upload custom greeting
            with open(self.wav_path, mode='rb') as file:
                upload_as = f'w{uuid.uuid4()}.wav'
                ps.call_intercept.greeting(person_id=user.person_id, content=file,
                                           upload_as=upload_as)
            intermediate = ps.call_intercept.read(person_id=user.person_id)
            # .. and then set the greeting to custom
            ps.call_intercept.configure(person_id=user.person_id, intercept=intercept)
            updated = ps.call_intercept.read(person_id=user.person_id)

        # validation
        self.assertEqual(upload_as, intermediate.incoming.announcements.file_name)
        self.assertEqual(upload_as, updated.incoming.announcements.file_name)
        self.assertEqual(Greeting.custom, updated.incoming.announcements.greeting)


class TestCallerIdConfigure(TestCaseWithUsers):
    """
    Tests for
    """

    @contextmanager
    def user_context(self, *, users_with_tn: bool) -> Person:
        candidates = [user for user in self.users
                      if not users_with_tn or user.tn]

        if not candidates:
            self.skipTest('No candidate user for test found')

        target_user = random.choice(candidates)
        print(f'Target user: {target_user.display_name}')

        # get caller id settings
        ps = self.api.person_settings
        caller_id = ps.caller_id.read(person_id=target_user.person_id)
        try:
            yield random.choice(candidates)
        finally:
            # restore caller id settings
            restore = caller_id.configure_params()
            ps.caller_id.configure(person_id=target_user.person_id, **restore)
        return

    def test_set_direct_line(self):
        """
        Try to set the caller ID to direct line
        :return:
        """
        with self.user_context(users_with_tn=True) as user:
            ps = self.api.person_settings
            ps.caller_id.configure(person_id=user.person_id, selected=CallerIdSelectedType.direct_line)
            after = ps.caller_id.read(person_id=user.person_id)
            self.assertEqual(CallerIdSelectedType.direct_line, after.selected)

    def test_set_location_number(self):
        """
        Try to set the caller ID to location number
        :return:
        """
        with self.user_context(users_with_tn=True) as user:
            ps = self.api.person_settings
            ps.caller_id.configure(person_id=user.person_id, selected=CallerIdSelectedType.location_number)
            after = ps.caller_id.read(person_id=user.person_id)
            self.assertEqual(CallerIdSelectedType.location_number, after.selected)

    def set_custom(self):
        pass

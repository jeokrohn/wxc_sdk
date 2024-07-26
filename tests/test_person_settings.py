import asyncio
import base64
import os.path
import random
import uuid
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from functools import reduce
from itertools import chain
from operator import attrgetter
from typing import Callable

from wxc_sdk.base import to_camel
from wxc_sdk.people import Person
from wxc_sdk.person_settings.appservices import AppServicesSettings
from wxc_sdk.person_settings.barge import BargeSettings
from wxc_sdk.person_settings.call_intercept import InterceptSetting, InterceptTypeIncoming, Greeting
from wxc_sdk.person_settings.call_recording import CallRecordingSetting
from wxc_sdk.person_settings.caller_id import CallerIdSelectedType, CallerId, ExternalCallerIdNamePolicy
from wxc_sdk.person_settings.preferred_answer import PreferredAnswerResponse, PreferredAnswerEndpointType, \
    PreferredAnswerEndpoint
from wxc_sdk.telephony import NumberType, NumberListPhoneNumber, OwnerType
from tests.base import TestCaseWithUsers, gather, async_test


class TestRead(TestCaseWithUsers):
    def execute_read_test(self, f: Callable):
        with ThreadPoolExecutor() as pool:
            result_map = pool.map(lambda user: f(user.person_id), self.users)
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
        for user, result in zip(self.users, results):
            if isinstance(result, Exception):
                continue
            result: CallRecordingSetting
            if result.call_recording_access_settings:
                print(
                    f'{user.display_name} has call recording access settings: {result.call_recording_access_settings}')

        for u, e in ((u, r) for u, r in zip(self.users, results) if isinstance(r, Exception)):
            u: Person
            print(f'{u.display_name}: {e}')
        self.assertFalse(any(isinstance(r, Exception) for r in results))

    def test_005_read_caller_id(self):
        """
        read caller id settings for all users
        """
        results = self.execute_read_test(self.api.person_settings.caller_id.read)
        for e in (r for r in results if isinstance(r, Exception)):
            print(f'{e}')
        self.assertFalse(any(isinstance(r, Exception) for r in results))

    def test_006_read_all_preferred_answer_endpoints(self):
        """
        read preferred answer endpoints settings for all users
        """
        results = self.execute_read_test(self.api.person_settings.preferred_answer.read)
        for e in (r for r in results if isinstance(r, Exception)):
            print(f'{e}')
        dn_len = max(len(user.display_name) for user in self.users)
        for user, pa_setting in zip(self.users, results):
            pa_setting: PreferredAnswerResponse
            print(f'{user.display_name:{dn_len}}', end='')
            if isinstance(pa_setting, Exception):
                print(f'{pa_setting}')
            else:
                if pa_setting.preferred_answer_endpoint_id:
                    pae = next((ep for ep in pa_setting.endpoints if ep.id == pa_setting.preferred_answer_endpoint_id),
                               None)
                    if pae is None:
                        print('preferred_answer_endpoint_id set but ep not found in list')
                    else:
                        print(f'{pae.type}, {pae.name}')
                else:
                    print('preferred_answer_endpoint_id is None')
                for ep in sorted(pa_setting.endpoints, key=attrgetter('name')):
                    print(f'  {ep.type}, {ep.name}: {base64.b64decode(ep.id).decode()}')
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
            barge_settings = self.api.person_settings.barge.read(entity_id=target_user.person_id)
            print(f'target user: {target_user.display_name}: enabled: {barge_settings.enabled}, tone enabled: '
                  f'{barge_settings.tone_enabled}')
            try:
                yield target_user
            finally:
                # restore barge settings
                print(f'restore enabled: {barge_settings.enabled}, tone enabled: {barge_settings.tone_enabled}')
                self.api.person_settings.barge.configure(entity_id=target_user.person_id,
                                                         barge_settings=barge_settings)

        def update_and_check(barge_settings: BargeSettings):
            """
            Update and verify barge settings
            """
            print(f'Setting enabled: {barge_settings.enabled}, tone enabled: {barge_settings.tone_enabled}')
            self.api.person_settings.barge.configure(entity_id=user.person_id, barge_settings=barge_settings)
            after = self.api.person_settings.barge.read(entity_id=user.person_id)
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
        settings = self.api.person_settings.call_intercept.read(entity_id=target_user.person_id)
        print(f'target user: {target_user.display_name}: {settings} ')
        try:
            yield target_user
        finally:
            # restore settings
            print(f'restore {settings}')
            self.api.person_settings.call_intercept.configure(entity_id=target_user.person_id, intercept=settings)

    def call_intercept_update_and_check(self, user: Person, settings: InterceptSetting):
        """
        Update and verify call intercept settings
        """
        print(f'setting: {settings}')
        self.api.person_settings.call_intercept.configure(entity_id=user.person_id, intercept=settings)
        after = self.api.person_settings.call_intercept.read(entity_id=user.person_id)
        self.assertEqual(settings, after)
        return

    def test_005_configure_call_intercept(self):
        """
        try to update call intercept settings of a user
        """

        with self.call_intercept_user_context() as user:
            user: Person
            intercept = self.api.person_settings.call_intercept.read(entity_id=user.person_id)
            intercept.enabled = not intercept.enabled
            self.call_intercept_update_and_check(user=user, settings=intercept)

    def test_006_upload_intercept_greeting(self):
        """
        test to upload a custom greeting for call intercept
        """
        with self.call_intercept_user_context() as user:
            ps = self.api.person_settings
            ps.call_intercept.greeting(entity_id=user.person_id, content=self.wav_path)
            intercept = ps.call_intercept.read(entity_id=user.person_id)
        self.assertEqual(os.path.basename(self.wav_path), intercept.incoming.announcements.file_name)

    @async_test
    async def test_006a_async_upload_intercept_greeting(self):
        """
        test to upload a custom greeting for call intercept
        """
        with self.call_intercept_user_context() as user:
            ps = self.async_api.person_settings
            await ps.call_intercept.greeting(entity_id=user.person_id, content=self.wav_path)
            intercept = await ps.call_intercept.read(entity_id=user.person_id)
        self.assertEqual(os.path.basename(self.wav_path), intercept.incoming.announcements.file_name)

    def test_007_upload_intercept_greeting_from_open_file(self):
        """
        test to upload a custom greeting for call intercept from an open file
        """
        with self.call_intercept_user_context() as user:
            with open(self.wav_path, mode='rb') as wav_file:
                upload_as = f'w{uuid.uuid4()}.wav'
                ps = self.api.person_settings
                ps.call_intercept.greeting(entity_id=user.person_id, content=wav_file,
                                           upload_as=upload_as)
                intercept = ps.call_intercept.read(entity_id=user.person_id)
        self.assertEqual(upload_as, intercept.incoming.announcements.file_name)

    def test_008_incoming_intercept_with_custom_greeting(self):
        """
        settup incoming intercept w/ custom greeting
        """
        with self.call_intercept_user_context() as user:
            ps = self.api.person_settings
            intercept = ps.call_intercept.read(entity_id=user.person_id)
            intercept.incoming.intercept_type = InterceptTypeIncoming.intercept_all
            intercept.incoming.announcements.greeting = Greeting.custom

            # first upload custom greeting
            with open(self.wav_path, mode='rb') as file:
                upload_as = f'w{uuid.uuid4()}.wav'
                ps.call_intercept.greeting(entity_id=user.person_id, content=file,
                                           upload_as=upload_as)
            intermediate = ps.call_intercept.read(entity_id=user.person_id)
            # .. and then set the greeting to custom
            ps.call_intercept.configure(entity_id=user.person_id, intercept=intercept)
            updated = ps.call_intercept.read(entity_id=user.person_id)

        # validation
        self.assertEqual(upload_as, intermediate.incoming.announcements.file_name)
        self.assertEqual(upload_as, updated.incoming.announcements.file_name)
        self.assertEqual(Greeting.custom, updated.incoming.announcements.greeting)

    @async_test
    async def test_009_update_preferred_answer_endpoint(self):
        """
        Test updating the preferred answer endpoint for one user
        """
        api = self.async_api.person_settings.preferred_answer
        # get preferred answer settings for all users
        pa_settings = await asyncio.gather(
            *[api.read(person_id=user.person_id) for user in self.users])
        pa_settings: list[PreferredAnswerResponse]

        # pic a user where an alternative endpoint exists
        pa: PreferredAnswerResponse
        candidates = [(user, pa) for user, pa in zip(self.users, pa_settings)
                      if pa.endpoints]
        target_user, pa_setting = random.choice(candidates)
        target_user: Person
        pa_setting: PreferredAnswerResponse

        # update endpoint
        new_preferred = pa_setting.endpoints[0]
        print(f'Updating preferred answer endpoint for "{target_user.display_name}" to: '
              f'{new_preferred.type}, {new_preferred.name}')
        await api.modify(person_id=target_user.person_id,
                         preferred_answer_endpoint_id=new_preferred.id)
        try:
            # verify
            pa_after = await api.read(person_id=target_user.person_id)
            self.assertEqual(new_preferred.id, pa_after.preferred_answer_endpoint_id)
        finally:
            # restore
            await api.modify(person_id=target_user.person_id,
                             preferred_answer_endpoint_id=pa_setting.preferred_answer_endpoint_id)
            restored = await api.read(person_id=target_user.person_id)
            self.assertEqual(pa_setting, restored)

    @async_test
    async def test_010_application_in_preferred_answer_endpoints_aligns_with_user_app_setting(self):
        """
        verify that for all users the presence of an APPLICATION entry in the list of available preferred answer
        endpoints correlates with the webex desktop app being enabled on the user level.

        Also verify the ID formats
        """

        async def app_services_settings() -> list[AppServicesSettings]:
            return await asyncio.gather(
                *[self.async_api.person_settings.appservices.read(person_id=user.person_id)
                  for user in self.users])

        async def preferred_answer_settings() -> list[PreferredAnswerResponse]:
            return await asyncio.gather(
                *[self.async_api.person_settings.preferred_answer.read(person_id=user.person_id)
                  for user in self.users])

        # for all users get application settings
        # for all users get preferred answer settings
        apps, pa = await asyncio.gather(app_services_settings(), preferred_answer_settings())
        apps: list[AppServicesSettings]
        pa: list[PreferredAnswerResponse]

        # verify that 'APPLICATION' entry in preferred answer endpoints correlates with desktop app enablement
        err = False
        for user, app_setting, preferred_answer in zip(self.users, apps, pa):
            user: Person
            app_setting: AppServicesSettings
            pa: PreferredAnswerResponse
            app_available_as_pa = next((endpoint for endpoint in preferred_answer.endpoints
                                        if endpoint.type == PreferredAnswerEndpointType.application and
                                        endpoint.name == 'Webex Desktop Application'),
                                       None)
            is_app_available_as_pa = app_available_as_pa is not None
            if is_app_available_as_pa != app_setting.desktop_client_enabled:
                print(
                    f'!!! {user.display_name}: app available as preferred answer endpoint ({is_app_available_as_pa}), '
                    f'desktop client enabled ({app_setting.desktop_client_enabled})')
                err = True
            if app_available_as_pa:
                app_available_as_pa: PreferredAnswerEndpoint
                if app_available_as_pa.id != app_setting.desktop_client_id:
                    print(f'!!! {user.display_name}: desktop id (preferred answer endpoint): '
                          f'{base64.b64decode(app_available_as_pa.id + "==").decode()}, '
                          f'desktop id (user app settings): '
                          f'{base64.b64decode(app_setting.desktop_client_id + "==").decode()}')
                    err = True
            foo = 1
        self.assertFalse(err, 'check output for errors')

    def test_011_toggle_desktop_app_and_check_in_preferred_answer_endpoint(self):
        """
        for a single user try to toggle desktop availability and check the correlation with 'APPLICATION' entry in
        preferred answer endpoint list
        """
        target_user: Person = random.choice(self.users)
        ps_api = self.api.person_settings
        app_settings = ps_api.appservices.read(person_id=target_user.person_id)
        preferred_answer = ps_api.preferred_answer.read(person_id=target_user.person_id)

        def validate(apps: AppServicesSettings, preferred: PreferredAnswerResponse) -> bool:
            desktop_app = next((endpoint for endpoint in preferred.endpoints
                                if endpoint.type == PreferredAnswerEndpointType.application and
                                endpoint.name == 'Webex Desktop Application'),
                               None)
            return apps.desktop_client_enabled == (desktop_app is not None)

        try:
            self.assertTrue(validate(apps=app_settings, preferred=preferred_answer))
            # toggle desktop client availability
            app_settings_update = app_settings.model_copy(deep=True)
            app_settings_update.desktop_client_enabled = not app_settings.desktop_client_enabled
            ps_api.appservices.configure(person_id=target_user.person_id, settings=app_settings_update)
            app_settings_after = ps_api.appservices.read(person_id=target_user.person_id)
            self.assertEqual(app_settings_update.desktop_client_enabled, app_settings_after.desktop_client_enabled)

            # get preferred answer settings
            preferred_answer_after = ps_api.preferred_answer.read(person_id=target_user.person_id)

            # .. and validate
            self.assertTrue(validate(apps=app_settings_after, preferred=preferred_answer_after))
        finally:
            ps_api.appservices.configure(person_id=target_user.person_id, settings=app_settings)


class TestCallerIdConfigure(TestCaseWithUsers):
    """
    Tests for caller id settings update
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
        with self.no_log():
            caller_id = ps.caller_id.read(entity_id=target_user.person_id)
        try:
            yield target_user
        finally:
            # restore caller id settings
            with self.no_log():
                ps.caller_id.configure_settings(entity_id=target_user.person_id, settings=caller_id)
        return

    def test_001_set_direct_line(self):
        """
        Try to set the caller ID to direct line
        """
        with self.user_context(users_with_tn=True) as user:
            ps = self.api.person_settings
            ps.caller_id.configure(entity_id=user.person_id, selected=CallerIdSelectedType.direct_line)
            after = ps.caller_id.read(entity_id=user.person_id)
            self.assertEqual(CallerIdSelectedType.direct_line, after.selected)

    def test_002_set_location_number(self):
        """
        Try to set the caller ID to location number
        """
        with self.user_context(users_with_tn=True) as user:
            ps = self.api.person_settings
            ps.caller_id.configure(entity_id=user.person_id, selected=CallerIdSelectedType.location_number)
            after = ps.caller_id.read(entity_id=user.person_id)
            self.assertEqual(CallerIdSelectedType.location_number, after.selected)

    @staticmethod
    def verify_e164(body: dict) -> list[tuple[str, str]]:
        """
        verify that numbers are E.164

        :return: list od tuples (field, value) for numbers that are not E.164
        """
        fields = ['direct_number', 'location_number', 'mobile_number', 'custom_number']
        return [(field, number) for field in fields
                if (number := body.get(to_camel(field))) is not None and number[0] != '+']

    def assert_number_format_e164(self):
        """
        Check number formats in all logged get requests
        """
        requests = list(self.requests(method='GET', url_filter=r'.+people/(?P<user_id>\w+)/features/callerId'))
        e164_issue = False
        for request in requests:
            non_e164 = self.verify_e164(request.response_body)
            if non_e164:
                e164_issue = True
                print('Not E.164: ', end='')
                print(", ".join(": ".join(ne) for ne in non_e164))
        self.assertFalse(e164_issue, 'Some numbers are not E.164')

    def test_003_set_location_number_verify_number_format(self):
        """
        Try to set the caller ID to location number and check number formats
        """
        with self.user_context(users_with_tn=True) as user:
            ps = self.api.person_settings
            ps.caller_id.configure(entity_id=user.person_id, selected=CallerIdSelectedType.location_number)
            after = ps.caller_id.read(entity_id=user.person_id)

        self.assertEqual(CallerIdSelectedType.location_number, after.selected)
        self.assert_number_format_e164()

    @async_test
    async def test_004_set_custom_number(self):
        """
        Try to set number to another assigned numbers
        """
        # get phone numbers assigned to users
        numbers = await self.async_api.telephony.phone_numbers(number_type=NumberType.number,
                                                               owner_type=OwnerType.people)
        # group phone numbers by location
        numbers_by_location: dict[str, list[NumberListPhoneNumber]] = reduce(
            lambda red, r: red[r.location.id].append(r) or red,
            numbers, defaultdict(list))
        # pick random number(and user) from users within locations with at least two users
        target_number: NumberListPhoneNumber = random.choice(list(chain.from_iterable(number_list
                                                                                      for number_list in
                                                                                      numbers_by_location.values()
                                                                                      if len(number_list) > 1)))

        # pick second number and user with number in same location
        second_number: NumberListPhoneNumber = random.choice(
            [n for n in numbers_by_location[target_number.location.id]
             if n.owner.owner_id != target_number.owner.owner_id])
        # try to set the caller id of owner of 1st number
        api = self.async_api.person_settings.caller_id
        before = await api.read(entity_id=target_number.owner.owner_id)
        try:
            await api.configure(entity_id=target_number.owner.owner_id,
                                selected=CallerIdSelectedType.custom, custom_number=second_number.phone_number)
            after = await api.read(entity_id=target_number.owner.owner_id)
        finally:
            await api.configure_settings(entity_id=target_number.owner.owner_id, settings=before)
        self.assertEqual(CallerIdSelectedType.custom, after.selected)
        self.assertEqual(second_number.phone_number, after.custom_number)
        self.assert_number_format_e164()

    def test_005_set_first_name(self):
        """
        Try to update first name
        """
        with self.user_context(users_with_tn=True) as user:
            user: Person
            api = self.api.person_settings.caller_id
            before = api.read(entity_id=user.person_id)
            update = CallerId(selected=before.selected, first_name='foo')
            api.configure_settings(entity_id=user.person_id, settings=update)
            after = api.read(entity_id=user.person_id)
        expected = before.model_copy(deep=True)
        expected.first_name = update.first_name
        self.assertEqual(expected, after)

    def test_006_block_in_forward_calls_enabled(self):
        """
        Try to update block_in_forward_calls_enabled
        """
        with self.user_context(users_with_tn=True) as user:
            user: Person
            api = self.api.person_settings.caller_id
            before = api.read(entity_id=user.person_id)
            update = CallerId(selected=before.selected,
                              block_in_forward_calls_enabled=not before.block_in_forward_calls_enabled)
            api.configure_settings(entity_id=user.person_id, settings=update)
            after = api.read(entity_id=user.person_id)
        expected = before.model_copy(deep=True)
        expected.block_in_forward_calls_enabled = update.block_in_forward_calls_enabled
        self.assertEqual(expected, after)

    def test_006_custom_external_caller_id_name(self):
        """
        Try to update custom_external_caller_id_name
        """
        with self.user_context(users_with_tn=True) as user:
            user: Person
            api = self.api.person_settings.caller_id
            before = api.read(entity_id=user.person_id)
            update = CallerId(selected=before.selected,
                              external_caller_id_name_policy=ExternalCallerIdNamePolicy.other,
                              custom_external_caller_id_name='foo custom')
            api.configure_settings(entity_id=user.person_id, settings=update)
            after = api.read(entity_id=user.person_id)
        expected = before.model_copy(deep=True)
        expected.external_caller_id_name_policy = update.external_caller_id_name_policy
        expected.custom_external_caller_id_name = update.custom_external_caller_id_name
        self.assertEqual(expected, after)

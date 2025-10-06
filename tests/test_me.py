"""
tests for /me endpoint
"""
import asyncio
import base64
import json
from concurrent.futures.thread import ThreadPoolExecutor
from random import choice
from typing import Union

from pydantic import TypeAdapter

from tests.base import TestWithRandomUserApi, async_test
from wxc_sdk import WebexSimpleApi
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.as_rest import AsRestError
from wxc_sdk.me import ServicesEnum, MeProfile, UserCallCaptions
from wxc_sdk.me.endpoints import MeEndpoint
from wxc_sdk.people import Person
from wxc_sdk.person_settings.call_policy import PrivacyOnRedirectedCalls
from wxc_sdk.person_settings.dnd import DND
from wxc_sdk.person_settings.forwarding import CallForwardingAlways
from wxc_sdk.telephony import AnnouncementLanguage


class TestMe(TestWithRandomUserApi):
    # proxy = True

    def test_profile(self):
        """
        Get profile details for the authenticated user
        """
        user = self.random_user()
        with self.user_api(user) as api:
            api: WebexSimpleApi
            details = api.me.details()
        print(json.dumps(details.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))

    def test_profile_all(self) -> Union[Exception, MeProfile]:
        """
        Get profile details for all users
        """

        def get_profile(user: Person):
            with self.user_api(user) as api:
                api: WebexSimpleApi
                try:
                    details = api.me.details()
                except Exception as e:
                    return e
            return details

        candidates = [user for user in self.users if not user.emails[0].startswith('admin')]
        with ThreadPoolExecutor() as pool:
            results = list(pool.map(get_profile, candidates))
        err = None
        for user, result in zip(candidates, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting profile for {user.display_name}: {result}")
        if err:
            raise err

    def test_announcement_languages(self):
        """
        Retrieve announcement languages for the authenticated user
        """
        user = self.random_user()
        with self.user_api(user) as api:
            api: WebexSimpleApi
            languages = api.me.announcement_languages()
        print(json.dumps(TypeAdapter(list[AnnouncementLanguage]).dump_python(languages, mode='json', by_alias=True,
                                                                             exclude_unset=True),
                         indent=2))

    @async_test
    async def test_feature_access_codes(self):
        """
        Retrieve feature access codes for all calling users
        """

        async def get_fac_list(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.feature_access_codes()

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_fac_list(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting feature access codes for {user.display_name}: {result}")
        if err:
            raise err

    @async_test
    async def test_monitoring_settings(self):
        """
        Retrieve monitoring settings for all calling users
        """

        async def get_fac_list(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.monitoring_settings()

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_fac_list(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error monitoring settings for {user.display_name}: {result}")
        if err:
            raise err

    @async_test
    async def test_country_telephony_config_requirements(self):
        """
        Retrieve country telephony configuration requirements for countries of all supported announcement languages of
        the authenticated user
        """
        user = self.random_user()
        with self.user_api(user) as api:
            api: WebexSimpleApi
            unsupported_country_codes = {'RU'}
            languages = api.me.announcement_languages()
            country_codes = [cc
                             for lang in languages
                             if (cc := lang.code.split('_')[-1].upper()) not in unsupported_country_codes]
            async with self.as_webex_api(tokens=api.access_token) as as_api:
                as_api: AsWebexSimpleApi
                har_id = self.har_writer.register_as_webex_api(as_api)
                try:
                    tasks = [as_api.me.country_telephony_config_requirements(country_code) for country_code in
                             country_codes]
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                finally:
                    self.har_writer.unregister_api(har_id)
        err = None
        errored_country_codes = []
        for country_code, result in zip(country_codes, results):
            if isinstance(result, Exception):
                err = err or result
                errored_country_codes.append(country_code)
                print(f"Error getting country telephony config requirements for {country_code}: {result}")
        if err:
            print(f'Errored country codes: {", ".join(errored_country_codes)}')
            raise err

    @async_test
    async def test_available_caller_id_list(self):
        """
        Retrieve available caller ID list for all calling users
        """

        async def get_available_caller_id_list(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.caller_id.available_caller_id_list()
            # end of get_available_caller_id_list

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_available_caller_id_list(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting available caller ID list for {user.display_name}: {result}")
        if err:
            raise err

    @async_test
    async def test_calling_services_list(self):
        """
        Retrieve calling services list for all calling users
        """

        async def get_list(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.calling_services_list()
            # end of get_list

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_list(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting available calling services list for {user.display_name}: {result}")
        if err:
            # Determine calling services list by looking at responses
            services_set: set[str] = set()
            for request in self.requests(method='GET', url_filter='.*/v1/telephony/config/people/me/settings/services'):
                if request.status != 200:
                    continue
                body = request.response_body
                services = body.get('services')
                if not services:
                    continue
                services_set.update(services)
            enum_values = [v.value for v in ServicesEnum]
            services_not_in_enum = services_set - set(enum_values)
            print(f'Calling services not in ServicesEnum: {", ".join(sorted(services_not_in_enum))}')
            enum_values_not_in_services = set(enum_values) - services_set
            print(f'Calling services in ServicesEnum but not seen in responses: '
                  f'{", ".join(sorted(enum_values_not_in_services))}')
            print()
            raise err


class TestEndpoints(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    def test_list(self):
        """
        List endpoints for the authenticated user
        """
        user = self.random_user()
        with self.user_api(user) as api:
            api: WebexSimpleApi
            endpoints = api.me.endpoints.list()
        print(json.dumps(TypeAdapter(list[MeEndpoint]).dump_python(endpoints,
                                                                   mode='json', by_alias=True,
                                                                   exclude_unset=True),
                         indent=2))

    @async_test
    async def test_details(self):
        """
        Get details for all endpoints for the authenticated user
        """
        user = self.random_user()

        with self.user_api(user) as api:
            api: WebexSimpleApi
            # get endpoints synchronously
            endpoints = api.me.endpoints.list()
            # get details for all endpoints asynchronously
            async with self.as_webex_api(tokens=api.access_token) as as_api:
                as_api: AsWebexSimpleApi
                tasks = [as_api.me.endpoints.details(endpoint.id) for endpoint in endpoints]
                results = await asyncio.gather(*tasks, return_exceptions=True)
        err = None
        for endpoint, result in zip(endpoints, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting details for endpoint {endpoint.name}: {result}")
            else:
                print(f"Getting details for endpoint {endpoint.name}")
                result: MeEndpoint
                print(json.dumps(result.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        if err:
            raise err

    @async_test
    async def test_available_preferred_answer_endpoints(self):
        """
        Retrieve available preferred answer endpoints for all calling users
        """

        async def get_available_preferred_answer_endpoints(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.endpoints.available_preferred_answer_endpoints()
            # end of get_available_preferred_answer_endpoints

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_available_preferred_answer_endpoints(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting available preferred answer endpoints for {user.display_name}: {result}")
        if err:
            raise err

    @async_test
    async def test_get_preferred_answer_endpoint(self):
        """
        Get preferred answer endpoint for all calling users
        """

        async def get_endpoint(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.endpoints.get_preferred_answer_endpoint()
            # end of get_available_preferred_answer_endpoints

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_endpoint(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting preferred answer endpoint for {user.display_name}: {result}")
        if err:
            raise err

    def test_modify_preferred_answer_endpoint(self):
        """
        Modify preferred answer endpoint for a random calling user
        """
        user = self.random_user()
        with self.user_api(user) as api:
            api: WebexSimpleApi
            endpoints = api.me.endpoints.list()
            endpoints = [ep for ep in endpoints if ep.auto_and_forced_answer_enabled]
            if not endpoints:
                self.skipTest(f'User {user.display_name} has no endpoints to set as preferred answer endpoint')
            endpoint = choice(endpoints)
            # get current preferred answer endpoint
            current_pa_endpoint = api.me.endpoints.get_preferred_answer_endpoint()
            print(f'Setting preferred answer endpoint to {endpoint.name} ({endpoint.id})')
            api.me.endpoints.modify_preferred_answer_endpoint(endpoint.id)
            updated_pa_endpoint = api.me.endpoints.get_preferred_answer_endpoint()
            try:
                self.assertIsNotNone(updated_pa_endpoint)
                self.assertEqual(updated_pa_endpoint.id, endpoint.id, 'Preferred answer endpoint was not set correctly')
            finally:
                # restore to no preferred answer endpoint
                pa_id = current_pa_endpoint and current_pa_endpoint.id
                api.me.endpoints.modify_preferred_answer_endpoint(pa_id)
                restored = api.me.endpoints.get_preferred_answer_endpoint()
                self.assertEqual(restored, current_pa_endpoint)


class TestBarge(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_get(self):
        """
        Get barge settings for all calling users
        """

        async def get_barge_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.barge.get()
            # end of get_available_preferred_answer_endpoints

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_barge_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting barge settings for {user.display_name}: {result}")
        if err:
            raise err

    def test_configure(self):
        """
        Configure barge settings for a random calling user
        """
        user = self.random_user()
        with self.user_api(user) as api:
            api: WebexSimpleApi
            current_settings = api.me.barge.get()
            print(f'Current settings: {current_settings}')
            new_settings = current_settings.model_copy(deep=True)
            new_settings.enabled = not current_settings.enabled
            api.me.barge.configure(new_settings)
            updated_settings = api.me.barge.get()
            print(f'Updated settings: {updated_settings}')
            try:
                self.assertEqual(updated_settings.enabled, new_settings.enabled)
            finally:
                # restore original settings
                api.me.barge.configure(current_settings)
                # verify restoration
                restored_settings = api.me.barge.get()
                self.assertEqual(restored_settings, current_settings)


class TestCallBlock(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_settings(self):
        """
        Get call block settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.call_block.settings()
            # end of get_available_preferred_answer_endpoints

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting call block settings for {user.display_name}: {result}")
        if err:
            raise err

    def test_add_delete_number(self):
        """
        Add and delete a call block number for a random calling user
        """
        user = self.random_user()
        with self.user_api(user) as api:
            api: WebexSimpleApi
            initial_numbers = api.me.call_block.settings()
            print(f'Initial call block numbers: {initial_numbers}')
            # generate a random phone number to block
            phone_number = f'+1555555{choice(range(1000, 9999))}'
            pn_base64 = base64.b64encode(phone_number.encode()).decode()
            blocked = api.me.call_block.state_for_number(pn_base64)
            print(f'Checked that number is not already blocked: {blocked}')

            print(f'Adding call block number: {phone_number}')
            pn_id = api.me.call_block.add_number(phone_number)

            updated_numbers = api.me.call_block.settings()
            print(f'Updated call block numbers: {updated_numbers}')
            try:
                # try to find the added number in the updated list
                bn = next((n for n in updated_numbers if n.phone_number == phone_number), None)
                self.assertIsNotNone(bn, f'Added number {phone_number} not found in updated list')
                blocked = api.me.call_block.state_for_number(pn_base64)
                print(f'Verified that number {phone_number} is blocked: {blocked}')
                self.assertEqual(bn.id, pn_id, 'Returned ID does not match the ID in the updated list')
            finally:
                print(f'Deleting call block number {phone_number}')
                api.me.call_block.delete_number(bn.id)
                final_numbers = api.me.call_block.settings()
                print(f'Final call block numbers: {final_numbers}')
                self.assertEqual(final_numbers, initial_numbers)


class TestForwarding(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_read(self):
        """
        Get call forwarding settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.forwarding.settings()
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting call forwarding settings for {user.display_name}: {result}")
        if err:
            raise err

    def test_configure(self):
        """
        Configure call forwarding settings for a random calling user
        """
        user = self.random_user()
        with (self.user_api(user) as api):
            api: WebexSimpleApi
            current_settings = api.me.forwarding.settings()
            print('Current settings:')
            print(json.dumps(current_settings.model_dump(mode='json', by_alias=True, exclude_unset=True),
                             indent=2))
            destination = f'+1555555{choice(range(1000, 9999))}'
            print(f'forwarding destination {destination}')
            always = CallForwardingAlways(ring_reminder_enabled=True,
                                          enabled=True,
                                          destination=destination,
                                          destination_voicemail_enabled=False)
            update = current_settings.model_copy(deep=True)
            update.call_forwarding.always = always
            api.me.forwarding.configure(update)
            updated_settings = api.me.forwarding.settings()
            print('Updated settings:')
            print(json.dumps(updated_settings.model_dump(mode='json', by_alias=True, exclude_unset=True),
                             indent=2))
            try:
                self.assertEqual(updated_settings.call_forwarding.always, always)
            finally:
                # restore original settings
                current_always = current_settings.call_forwarding.always
                if not current_always.enabled:
                    if current_always.destination is None or current_always.destination.startswith('+1555555'):
                        # reset the destination again
                        current_always.destination = None
                api.me.forwarding.configure(current_settings)
                # verify restoration
                restored_settings = api.me.forwarding.settings()
                self.assertEqual(restored_settings, current_settings)


class TestCallPark(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_read(self):
        """
        Get call forwarding settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.call_park.settings()
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting call park settings for {user.display_name}: {result}")
        if err:
            raise err


class TestCallPickup(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_read(self):
        """
        Get call forwarding settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.call_pickup.settings()
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting call pickup settings for {user.display_name}: {result}")
        if err:
            raise err


class TestCallPolices(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_read(self):
        """
        Get call policy settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.call_policies.settings()
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting call policy settings for {user.display_name}: {result}")
        if err:
            raise err

    def test_update(self):
        """
        Update call policy settings for a random calling user
        """
        user = self.random_user()
        with (self.user_api(user) as api):
            api: WebexSimpleApi
            current = api.me.call_policies.settings()
            print(f'Current settings: {current}')
            update = PrivacyOnRedirectedCalls.privacy_for_all_calls
            print(f'Updated setting: {update}')
            api.me.call_policies.update(update)
            after = api.me.call_policies.settings()
            print(f'After: {after}')
            try:
                self.assertEqual(update, after)
            finally:
                # restore original settings
                api.me.call_policies.update(current)
                # verify restoration
                restored_setting = api.me.call_policies.settings()
                self.assertEqual(restored_setting, current)


class TestRecording(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_read(self):
        """
        Get call recording settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.recording.settings()
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting call recording settings for {user.display_name}: {result}")
        if err:
            raise err


class TestCallerId(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_read(self):
        """
        Get caller id settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.caller_id.settings()
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting caller id settings for {user.display_name}: {result}")
        if err:
            raise err


class TestDND(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_read(self):
        """
        Get DND settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    return await as_api.me.dnd.settings()
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users],
                                       return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting DND settings for {user.display_name}: {result}")
        if err:
            raise err

    def test_update(self):
        """
        Update DND settings for a random calling user
        """
        user = self.random_user()
        with (self.user_api(user) as api):
            api: WebexSimpleApi
            current = api.me.dnd.settings()
            print('Current settings:')
            print(json.dumps(current.model_dump(mode='json', by_alias=True, exclude_unset=True),
                             indent=2))
            update = DND(enabled=not current.enabled)
            print(f'Updated setting: {update}')
            api.me.dnd.configure(update)
            after = api.me.dnd.settings()
            print('After:')
            print(json.dumps(after.model_dump(mode='json', by_alias=True, exclude_unset=True),
                             indent=2))
            try:
                self.assertEqual(update.enabled, after.enabled)
            finally:
                # restore original settings
                api.me.dnd.configure(current)
                # verify restoration
                restored_setting = api.me.dnd.settings()
                self.assertEqual(restored_setting, current)


class TestExec(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_alert_settings(self):
        """
        Get exec alert settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.executive.alert_settings()
                    except AsRestError as e:
                        if e.status == 400 and e.detail.error_code == 4410:
                            return None
                        raise
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting exec alert settings for {user.display_name}: {result}")
            elif result is not None:
                print(f"Exec alert settings for {user.display_name}: ")
                print(json.dumps(result.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        if err:
            raise err

    @async_test
    async def test_assigned_assistants(self):
        """
        Get assigned assistants for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.executive.assigned_assistants()
                    except AsRestError as e:
                        if e.status == 400 and e.detail.error_code == 4410:
                            return None
                        raise
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting assigned assistants {user.display_name}: {result}")
            elif result is not None:
                print(f"Exec alert settings for {user.display_name}: ")
                print(json.dumps(result.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        if err:
            raise err

    @async_test
    async def test_exec_assistant_settings(self):
        """
        Get executive assistant settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.executive.executive_assistant_settings()
                    except AsRestError as e:
                        if e.status == 400 and e.detail.error_code == 4410:
                            return None
                        raise
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting executive assistant settings {user.display_name}: {result}")
            elif result is not None:
                print(f"executive assistant settings for {user.display_name}: ")
                print(json.dumps(result.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        if err:
            raise err

    @async_test
    async def test_executive_call_filtering_settings(self):
        """
        Get executive assistant settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.executive.executive_call_filtering_settings()
                    except AsRestError as e:
                        if e.status == 400 and e.detail.error_code == 4410:
                            return None
                        raise
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting executive call filtering settings {user.display_name}: {result}")
            elif result is not None:
                print(f"Executive call filtering settings for {user.display_name}: ")
                print(json.dumps(result.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        if err:
            raise err


class TestCallCenter(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_settings(self):
        """
        Get call center settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.call_center.settings()
                    except AsRestError as e:
                        if e.status == 400 and e.detail.error_code == 4410:
                            return None
                        raise
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error getting call center settings for {user.display_name}: {result}")
            elif result is not None:
                print(f"call center settings for {user.display_name}: ")
                print(json.dumps(result.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        if err:
            raise err


class TestSNR(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_settings(self):
        """
        Get single number reach settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.snr.settings()
                    except AsRestError as e:
                        if e.status == 400 and e.detail.error_code == 4410:
                            return None
                        raise
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error single number reach settings for {user.display_name}: {result}")
            elif result is not None:
                print(f"single number reach for {user.display_name}: ")
                print(json.dumps(result.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        if err:
            raise err


class TestVoicemail(TestWithRandomUserApi):
    # fixed_user_display_name = 'Dustin Harris'
    # proxy = True

    @async_test
    async def test_settings(self):
        """
        Get voicemail settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.voicemail.settings()
                    except AsRestError as e:
                        if e.status == 400 and e.detail.error_code == 4410:
                            return None
                        raise
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error voicemail settings for {user.display_name}: {result}")
            elif result is not None:
                print(f"voicemail settings for {user.display_name}: ")
                print(json.dumps(result.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        if err:
            raise err


class TestCallCaptions(TestWithRandomUserApi):

    @async_test
    async def test_settings(self):
        """
        Get call caption settings for all calling users
        """

        async def get_settings(user: Person):
            with self.user_api(user) as api:
                async with self.as_webex_api(tokens=api.access_token) as as_api:
                    as_api: AsWebexSimpleApi
                    try:
                        return await as_api.me.call_captions_settings()
                    except AsRestError as e:
                        raise e
            # end of get_settings

        users = [user for user in self.users if not user.display_name.startswith('admin@')]
        results = await asyncio.gather(*[get_settings(user)
                                         for user in users], return_exceptions=True)
        err = None
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                err = err or result
                print(f"Error call captions settings for {user.display_name}: {result}")
            elif result is not None:
                result: UserCallCaptions
                print(f"call caption settings for {user.display_name}: ")
                print(json.dumps(result.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
        if err:
            raise err

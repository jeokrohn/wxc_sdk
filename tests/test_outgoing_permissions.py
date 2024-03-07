"""
Tests for outgoing permissions for locations, persons, workspaces, and virtual lines
"""
import asyncio
import random

from tests.base import TestCaseWithLog, TestWithLocations, async_test
from wxc_sdk.person_settings.permissions_out import DigitPattern, Action


class TestOutgoingPermisssions(TestWithLocations):

    def test_location_read(self):
        target_location = random.choice(self.locations)
        perms = self.api.telephony.permissions_out.read(person_id=target_location.location_id)
        foo = 1

    def test_location_update(self):
        ...


class TestDigitPatterns(TestWithLocations):
    def test_location_list(self):
        target_location = next((loc for loc in self.api.locations.list(name='Frisco') if loc.name == 'Frisco'), None)
        if target_location is None:
            self.skipTest('Frisco location not found')
        api = self.api.telephony.permissions_out.digit_patterns
        patterns = api.get_digit_patterns(entity_id=target_location.location_id)
        print(f'Got {len(patterns.digit_patterns)} patterns for location {target_location.name}')

    def test_location_create(self):
        target_location = random.choice(self.locations)
        print(f'Location: {target_location.name}')
        api = self.api.telephony.permissions_out.digit_patterns
        patterns = api.get_digit_patterns(entity_id=target_location.location_id)
        existing = set(p.pattern for p in patterns.digit_patterns)
        new_patterns = (p for i in range(1000) if (p := f'9{i:03}') not in existing)
        new_pattern = next(new_patterns)
        api.create(entity_id=target_location.location_id,
                   pattern=DigitPattern(name=f'test_{new_pattern}', pattern=new_pattern, action=Action.block,
                                        transfer_enabled=False))
        after = api.get_digit_patterns(entity_id=target_location.location_id)
        print(f'Tried to create {new_pattern} in {target_location.name}')
        self.assertIn(new_pattern, (p.pattern for p in after.digit_patterns))

    @async_test
    async def test_location_create_check_500(self):
        target_location = random.choice(self.locations)
        print(f'Location: {target_location.name}')
        api = self.async_api.telephony.permissions_out.digit_patterns
        patterns = await api.get_digit_patterns(entity_id=target_location.location_id)
        existing = set(p.pattern for p in patterns.digit_patterns)
        new_patterns = (p for i in range(1000) if (p := f'9{i:03}') not in existing)

        # we want to check that we can create 500 patterns
        patterns_to_create = [next(new_patterns) for _ in range(501 - len(existing))]
        tasks = [api.create(entity_id=target_location.location_id,
                            pattern=DigitPattern(name=f'test_{pattern}', pattern=pattern, action=Action.block,
                                                 transfer_enabled=False))
                 for pattern in patterns_to_create]
        print(f'Creating {len(patterns_to_create)} patterns')
        results = await asyncio.gather(*tasks, return_exceptions=True)
        failed = [(pattern, result)
                  for pattern, result in zip(patterns_to_create, results)
                  if isinstance(result, Exception)]
        try:
            self.assertEqual(1, len(failed), f'Failed to create {len(failed)} patterns')
        finally:
            # delete patterns again
            await asyncio.gather(*[api.delete(entity_id=target_location.location_id, digit_pattern_id=dp_id)
                                   for dp_id in results
                                   if not isinstance(dp_id, Exception)])
        # fine the error response
        failed_request = next((request
                               for request in self.requests(method='POST',
                                                            url_filter='https://webexapis.com/v1/telephony/config/locations/.*/digitPatterns')
                               if request.status != 201),
                              None)
        if failed_request is not None:
            print(failed_request.record.message)
        error = failed[0][1]
        self.assertTrue(not isinstance(error.detail, str), 'invalid JSON in 502')
        after = await api.get_digit_patterns(entity_id=target_location.location_id)
        self.assertEqual(len(patterns.digit_patterns), len(after.digit_patterns), 'Number of patterns changed')

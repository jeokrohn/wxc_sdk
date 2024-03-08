"""
Tests for outgoing permissions for locations, persons, workspaces, and virtual lines
"""
import asyncio
import random
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import reduce
from itertools import chain
from typing import ClassVar

from tests.base import TestCaseWithLog, TestWithLocations, async_test
from wxc_sdk import WebexSimpleApi
from wxc_sdk.common import OwnerType, IdAndName
from wxc_sdk.people import Person
from wxc_sdk.person_settings.permissions_out import DigitPattern, Action
from wxc_sdk.telephony import NumberType, NumberListPhoneNumber, OriginatorType, DestinationType


class TestOutgoingPermissions(TestWithLocations):

    def test_location_read(self):
        target_location = random.choice(self.locations)
        self.api.telephony.permissions_out.read(person_id=target_location.location_id)

    def test_location_update(self):
        ...


class TestDigitPatterns(TestWithLocations):
    @async_test
    async def test_location_list(self):
        """
        List patterns for all locations
        """
        api = self.async_api.telephony.permissions_out.digit_patterns

        location_patterns = await asyncio.gather(*[api.get_digit_patterns(entity_id=loc.location_id)
                                                   for loc in self.locations],
                                                 return_exceptions=True)
        print(f'Got patterns for {len(location_patterns)} locations')
        errors = sum((1 for lp in location_patterns if isinstance(lp, Exception)))
        self.assertEqual(0, errors, f'Got {errors} errors')
        location_len = max(len(loc.name) for loc in self.locations)
        for location, patterns in zip(self.locations, location_patterns):
            print(f'{location.name:{location_len}}: {len(patterns.digit_patterns)} pattern(s)')

    def test_location_create(self):
        """
        Create a new pattern in a random location
        """
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

        # check whether the pattern was created
        after = api.get_digit_patterns(entity_id=target_location.location_id)
        print(f'Tried to create {new_pattern} in {target_location.name}')
        self.assertIn(new_pattern, (p.pattern for p in after.digit_patterns))

    @async_test
    async def test_location_create_check_500(self):
        """
        Try to create 501 patterns and check that we get a proper error
        """
        target_location = random.choice(self.locations)
        print(f'Location: {target_location.name}')

        api = self.async_api.telephony.permissions_out.digit_patterns
        patterns = await api.get_digit_patterns(entity_id=target_location.location_id)
        existing = set(p.pattern for p in patterns.digit_patterns)
        new_patterns = (p for i in range(1000) if (p := f'9{i:03}') not in existing)

        # we want to check that we can create 500 patterns and get an error on the 501st
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

        # find the error response
        failed_request = next((request
                               for request in self.requests(method='POST',
                                                            url_filter='.+/digitPatterns')
                               if request.status != 201),
                              None)
        self.assertIsNotNone(failed_request, 'No failed request found')

        print(failed_request.record.message)

        # error detail should be proper JSON
        error = failed[0][1]
        # noinspection PyUnresolvedReferences
        self.assertTrue(not isinstance(error.detail, str), 'invalid JSON in 502')

        # finally, the number of patterns should be the same as before
        after = await api.get_digit_patterns(entity_id=target_location.location_id)
        self.assertEqual(len(patterns.digit_patterns), len(after.digit_patterns), 'Number of patterns changed')

    @async_test
    async def test_location_delete_all(self):
        """
        create some patterns, delete them all, and check that they are gone
        """
        # pick a random location
        target_location = random.choice(self.locations)

        # get existing patterns in that location
        api = self.async_api.telephony.permissions_out.digit_patterns
        patterns = await api.get_digit_patterns(entity_id=target_location.location_id)

        # determine existing patterns
        existing = set(p.pattern for p in patterns.digit_patterns)
        available_patterns = (p for i in range(1000)
                              if (p := f'9{i:03}') not in existing)
        # available patterns
        new_patterns = [next(available_patterns) for _ in range(10)]

        # create 10 new patterns
        tasks = [api.create(entity_id=target_location.location_id,
                            pattern=DigitPattern(name=f'test_{pattern}', pattern=pattern, action=Action.block,
                                                 transfer_enabled=False))
                 for pattern in new_patterns]
        await asyncio.gather(*tasks, return_exceptions=True)
        after_creation = await api.get_digit_patterns(entity_id=target_location.location_id)
        try:
            self.assertEqual(len(patterns.digit_patterns) + len(new_patterns), len(after_creation.digit_patterns),
                             'Number of patterns after creation')
            # try to delete all patterns
            await api.delete_all(entity_id=target_location.location_id)
            after_delete = await api.get_digit_patterns(entity_id=target_location.location_id)
            self.assertEqual(0, len(after_delete.digit_patterns), 'Number of patterns after deletion')
        finally:
            # restore all patterns that existed before
            await asyncio.gather(*[api.create(entity_id=target_location.location_id, pattern=p)
                                   for p in patterns.digit_patterns], return_exceptions=True)
            after_restore = await api.get_digit_patterns(entity_id=target_location.location_id)
            self.assertEqual(len(patterns.digit_patterns), len(after_restore.digit_patterns),
                             'Number of patterns after restore')

    @async_test
    async def test_location_delete_all_test_patterns(self):
        """
        Delete all test_ patterns in all locations
        """
        # get digit patterns of all locations
        api = self.async_api.telephony.permissions_out.digit_patterns
        location_patterns = await asyncio.gather(*[api.get_digit_patterns(entity_id=loc.location_id)
                                                   for loc in self.locations],
                                                 return_exceptions=True)

        # get location id and pattern id for all patterns that start with 'test_'
        location_and_pattern = list(chain.from_iterable(
            ((location.location_id, p.id) for p in patterns.digit_patterns if p.name.startswith('test_'))
            for location, patterns in zip(self.locations, location_patterns)))
        print(f'deleting {len(location_and_pattern)} patterns')

        # delete all test patterns
        results = await asyncio.gather(*[api.delete(entity_id=loc_id, digit_pattern_id=pattern_id)
                                         for loc_id, pattern_id in location_and_pattern],
                                       return_exceptions=True)
        err = next((r for r in results if isinstance(r, Exception)), None)
        if err:
            raise err


@dataclass
class TestUser:
    """
    Helper class for test users
    """
    id: str
    extension: str
    user: Person = field(init=False)

    def set_user(self, api: WebexSimpleApi):
        self.user = api.people.details(person_id=self.id)


@dataclass
class TestBetweenUsers(TestCaseWithLog):
    location: ClassVar[IdAndName]
    user_a: ClassVar[TestUser]
    user_b: ClassVar[TestUser]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # get two calling users with extension in same location
        extensions = cls.api.telephony.phone_numbers(owner_type=OwnerType.people, number_type=NumberType.extension)

        # group by location
        extensions_by_location = reduce(lambda d, e: d.setdefault(e.location.id, []).append(e) or d, extensions, {})
        extensions_by_location: dict[str, list[NumberListPhoneNumber]]

        # pick a location with at least two extensions
        location_candidates = [loc for loc, exts in extensions_by_location.items() if len(exts) > 1]
        if not location_candidates:
            cls.location = None
            return
        target_location_id = random.choice(location_candidates)

        # pick two random extensions and users in that location
        extensions = extensions_by_location[target_location_id]
        extensions: list[NumberListPhoneNumber]
        random.shuffle(extensions)
        cls.user_a = TestUser(id=extensions[0].owner.owner_id, extension=extensions[0].extension)
        cls.user_a.set_user(cls.api)
        cls.user_b = TestUser(id=extensions[1].owner.owner_id, extension=extensions[1].extension)
        cls.user_b.set_user(cls.api)
        cls.location = extensions[0].location

        # print some info
        print(f'Location: {cls.location.name}')
        print(f'User A: {cls.user_a.user.display_name} ({cls.user_a.extension})')
        print(f'User B: {cls.user_b.user.display_name} ({cls.user_b.extension})')

    def setUp(self) -> None:
        if self.location is None:
            self.skipTest('No location with at least two extensions')
        super().setUp()

    def a_can_call_b(self):
        # verify that A can call B
        print('Verifying that A can call B')
        routing_result = self.api.telephony.test_call_routing(
            originator_id=self.user_a.id, originator_type=OriginatorType.user,
            destination=self.user_b.extension,
            originator_number=self.user_a.extension)
        self.assertFalse(routing_result.is_rejected,
                         'Call should be accepted')
        self.assertEqual(DestinationType.hosted_agent, routing_result.destination_type,
                         'Unexpected destination type')
        self.assertEqual(self.user_b.id, routing_result.hosted_user.hu_id,
                         'Wrong destination')

    def a_cant_call_b(self):
        # verify that A can no longer call B
        print('Verifying that A can no longer call B')
        routing_result = self.api.telephony.test_call_routing(
            originator_id=self.user_a.id, originator_type=OriginatorType.user,
            destination=self.user_b.extension,
            originator_number=self.user_a.extension)
        self.assertTrue(routing_result.is_rejected,
                        'Call should be rejected')

    @contextmanager
    def block_b_at_location_level(self):
        # block B's extension at the location level
        print(f'Blocking B\'s extension ({self.user_b.extension}) at the location level')
        pattern_id = self.api.telephony.permissions_out.digit_patterns.create(
            entity_id=self.location.id,
            pattern=DigitPattern(name=f'test_b_{self.user_b.extension}',
                                 pattern=self.user_b.extension,
                                 action=Action.block,
                                 transfer_enabled=False))
        try:
            yield None
        finally:
            # unblock B's extension at the location level
            print(f'Unblocking B\'s extension ({self.user_b.extension}) at the location level')
            self.api.telephony.permissions_out.digit_patterns.delete(entity_id=self.location.id,
                                                                     digit_pattern_id=pattern_id)

    @contextmanager
    def block_b_at_user_a(self, block: bool = True):
        # block B's extension at user A
        print(f'Blocking B\'s extension ({self.user_b.extension}) at user A')
        pattern_id = self.api.telephony.permissions_out.digit_patterns.create(
            entity_id=self.user_a.id,
            pattern=DigitPattern(name=f'test_b_{self.user_b.extension}',
                                 pattern=self.user_b.extension,
                                 action=Action.block if block else Action.allow,
                                 transfer_enabled=False))
        try:
            yield None
        finally:
            # unblock B's extension at the user level
            print(f'Unblocking B\'s extension ({self.user_b.extension}) at user A')
            self.api.telephony.permissions_out.digit_patterns.delete(entity_id=self.user_a.id,
                                                                     digit_pattern_id=pattern_id)


class TestCallRouting(TestBetweenUsers):
    def test_block_extension_on_location(self):
        """
        Block extension dialing between two users at the location level
        """
        self.a_can_call_b()
        with self.block_b_at_location_level():
            self.a_cant_call_b()

    def test_block_extension_on_user_level(self):
        """
        Block extension dialing between two users at the user level
        """
        self.a_can_call_b()
        with self.block_b_at_user_a():
            self.a_cant_call_b()

    def test_block_extension_at_location_level_and_allow_at_user_level(self):
        """
        Block extension dialing between two users at the location level and allow at the user level
        """
        self.a_can_call_b()
        with self.block_b_at_location_level():
            self.a_cant_call_b()
            with self.block_b_at_user_a(block=False):
                self.a_can_call_b()

"""
Tests for outgoing permissions for locations, persons, workspaces, and virtual lines
"""
import asyncio
import json
import random
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import reduce
from itertools import chain
from operator import attrgetter
from typing import ClassVar
from unittest import skip

from tests.base import TestCaseWithLog, async_test, TestLocationsUsersWorkspacesVirtualLines
from wxc_sdk import WebexSimpleApi
from wxc_sdk.as_api import AsDigitPatternsApi, AsOutgoingPermissionsApi
from wxc_sdk.as_rest import AsRestError
from wxc_sdk.common import OwnerType, IdAndName, AuthCodeLevel, AuthCode
from wxc_sdk.locations import Location
from wxc_sdk.people import Person
from wxc_sdk.person_settings.permissions_out import DigitPattern, Action, OutgoingPermissionsApi
from wxc_sdk.telephony import (NumberType, NumberListPhoneNumber, OriginatorType, DestinationType,
                               TestCallRoutingResult, ConfigurationLevel)
from wxc_sdk.telephony.virtual_line import VirtualLine
from wxc_sdk.workspaces import Workspace, CallingType


class TestOutgoingPermissions(TestLocationsUsersWorkspacesVirtualLines):
    """
    Test reading/writing outgoing permission settings for locations, users, workspaces, virtual lines
    """

    @staticmethod
    def read(entity: str, entity_id: str, api: OutgoingPermissionsApi):
        permissions = api.read(entity_id=entity_id)
        print(f'Outgoing permissions for {entity}/{entity_id}:')
        print(json.dumps(permissions.model_dump(), indent=2))

    def test_location_read(self):
        """
        Read outgoing permissions for random location
        """
        target = random.choice(self.locations)
        target: Location
        self.read(entity=f'location "{target.name}"/{target.location_id}',
                  entity_id=target.location_id,
                  api=self.api.telephony.permissions_out)

    def test_user_read(self):
        """
        Read outgoing permissions for random user
        """
        target = random.choice(self.users)
        target: Person
        self.read(entity=f'User {target.display_name}({target.emails[0]})/{target.person_id}',
                  entity_id=target.person_id,
                  api=self.api.person_settings.permissions_out)

    def test_workspace_read(self):
        """
        Read outgoing permissions for random workspace
        """
        target = random.choice(self.workspaces)
        target: Workspace
        self.read(entity=f'Workspace {target.display_name}/{target.workspace_id}',
                  entity_id=target.workspace_id,
                  api=self.api.workspace_settings.permissions_out)

    def test_virtual_line_read(self):
        """
        Read outgoing permissions for random virtual line
        """
        target = random.choice(self.virtual_lines)
        target: VirtualLine
        self.read(entity=f'Virtual Line {target.display_name}/{target.id}',
                  entity_id=target.id,
                  api=self.api.telephony.virtual_lines.permissions_out)

    def test_location_update(self):
        ...


class TestAccessCodes(TestLocationsUsersWorkspacesVirtualLines):
    """
    Tests for outgoing permissions access codes
    + read access codes
    + create access codes
    * create duplicate access codes
    * check maximum number of access codes
    * modify access codes
    * delete access codes
    * clear all test access codes
    """

    @staticmethod
    def read(entity: str, entity_id: str, api: OutgoingPermissionsApi):
        codes = api.access_codes.read(entity_id=entity_id)
        print(f'Access codes for {entity}/{entity_id}:')
        print(json.dumps(codes.model_dump(mode='json'), indent=2))

    @skip('Different access codes API for locations')
    def test_location_read(self):
        """
        Read access codes for random location
        """
        target = random.choice(self.locations)
        target: Location
        self.read(entity=f'location "{target.name}"/{target.location_id}',
                  entity_id=target.location_id,
                  api=self.api.telephony.permissions_out)

    def test_user_read(self):
        """
        Read access codes for random user
        """
        target = random.choice(self.users)
        target: Person
        self.read(entity=f'User {target.display_name}({target.emails[0]})/{target.person_id}',
                  entity_id=target.person_id,
                  api=self.api.person_settings.permissions_out)

    def test_workspace_read(self):
        """
        Read access codes for random workspace
        """
        target = random.choice(self.workspaces)
        target: Workspace
        self.read(entity=f'Workspace {target.display_name}/{target.workspace_id}',
                  entity_id=target.workspace_id,
                  api=self.api.workspace_settings.permissions_out)

    def test_virtual_line_read(self):
        """
        Read access codes for random virtual line
        """
        target = random.choice(self.virtual_lines)
        target: VirtualLine
        self.read(entity=f'Virtual Line {target.display_name}/{target.id}',
                  entity_id=target.id,
                  api=self.api.telephony.virtual_lines.permissions_out)

    def create(self, entity: str, entity_id: str, api: OutgoingPermissionsApi):
        def location_read():
            return self.api.telephony.access_codes.read(location_id=entity_id)

        def read():
            r = api.access_codes.read(entity_id=entity_id)
            return r.access_codes

        for_location = 'location' in entity.lower()
        if for_location:
            reader = location_read
        else:
            reader = read
        codes = reader()
        existing = set(ac.code for ac in codes)
        new_codes = (code for i in range(9000, 10000)
                     if (code := f'{i}') not in existing)

        # create new code
        new_code = next(new_codes)
        print(f'{entity}/{entity_id}: creating access code {new_code}')
        description = f'test_{new_code}'
        if for_location:
            self.api.telephony.access_codes.create(location_id=entity_id,
                                                   access_codes=[AuthCode(code=new_code,
                                                                          description=description,
                                                                          level=AuthCodeLevel.location)])
        else:
            api.access_codes.create(entity_id=entity_id, code=new_code,
                                    description=description)

        # verify that the code exists
        codes_after = reader()
        created_code = next((ac for ac in codes_after if ac.code == new_code), None)
        self.assertIsNotNone(created_code, 'access code not created')
        if 'location' in entity.lower():
            self.assertIsNone(created_code.level)
        else:
            self.assertEqual(AuthCodeLevel.custom, created_code.level)

        # try to remove access code again
        if for_location:
            self.api.telephony.access_codes.delete_codes(location_id=entity_id, access_codes=[new_code])
        else:
            api.access_codes.modify(entity_id=entity_id, delete_codes=[created_code])
        codes_after = reader()
        created_code = next((ac for ac in codes_after if ac.code == new_code), None)
        self.assertIsNone(created_code, 'access code still there')

    def test_location_create(self):
        """
        create access code for random location
        """
        target = random.choice(self.locations)
        target: Location
        self.create(entity=f'location "{target.name}"/{target.location_id}',
                    entity_id=target.location_id,
                    api=self.api.telephony.permissions_out)

    def test_user_create(self):
        """
        create access code for random user
        """
        target = random.choice(self.users)
        target: Person
        self.create(entity=f'User {target.display_name}({target.emails[0]})/{target.person_id}',
                    entity_id=target.person_id,
                    api=self.api.person_settings.permissions_out)

    def test_workspace_create(self):
        """
        create access code for random workspace
        """
        target = random.choice(self.workspaces)
        target: Workspace
        self.create(entity=f'Workspace {target.display_name}/{target.workspace_id}',
                    entity_id=target.workspace_id,
                    api=self.api.workspace_settings.permissions_out)

    def test_virtual_line_create(self):
        """
        create access code for random virtual line
        """
        target = random.choice(self.virtual_lines)
        target: VirtualLine
        self.create(entity=f'Virtual Line {target.display_name}/{target.id}',
                    entity_id=target.id,
                    api=self.api.telephony.virtual_lines.permissions_out)

    async def create_check_1000(self, entity: str, entity_id: str, api: AsOutgoingPermissionsApi):
        """
        Try to create 1001 access codes and check that we get a proper error
        """
        self.skipTest('Skip to protect the backend')
        print(f'target for access code creation: {entity}')

        access_codes = await api.access_codes.read(entity_id=entity_id)
        existing = set(c.code for c in access_codes.access_codes)
        new_codes = (p for i in range(8000, 10000) if (p := str(i)) not in existing)

        # we want to check that we can create 500 patterns and get an error on the 501st
        codes_to_create = [next(new_codes) for _ in range(1001 - len(existing))]
        tasks = [api.access_codes.create(entity_id=entity_id, code=code, description=f'test_{code}')
                 for code in codes_to_create]
        print(f'Creating {len(codes_to_create)} access codes')
        results = await asyncio.gather(*tasks, return_exceptions=True)
        failed = [(code, result)
                  for code, result in zip(codes_to_create, results)
                  if isinstance(result, Exception)]
        try:
            self.assertEqual(1, len(failed), f'Failed to create {len(failed)} access codes')
            # try to add the failed pattern again
            code = failed[0][0]
            with self.assertRaises(AsRestError) as exc:
                await api.access_codes.create(entity_id=entity_id, code=code, description=f'test_{code}')
            rest_error: AsRestError = exc.exception
            self.assertEqual(502, rest_error.status, 'Invalid status code')
        finally:
            # delete access codes again
            if True:
                await api.access_codes.modify(entity_id=entity_id, delete_codes=[code for code in codes_to_create])

        # find the error response
        failed_request = next((request
                               for request in self.requests(method='POST',
                                                            url_filter='.+/accessCodes')
                               if request.status != 201),
                              None)
        self.assertIsNotNone(failed_request, 'No failed request found')

        print(failed_request.record.message)

        # error detail should be proper JSON
        error = failed[0][1]
        # noinspection PyUnresolvedReferences
        self.assertTrue(not isinstance(error.detail, str), 'invalid JSON in 502')

        # finally, the number of patterns should be the same as before
        after = await api.access_codes.read(entity_id=entity_id)
        self.assertEqual(len(access_codes.access_codes), len(after.access_codes),
                         'Number of access codes changed')

    @async_test
    async def test_location_create_1000(self):
        """
        create access code for random location
        """
        target = random.choice(self.locations)
        target: Location
        await self.create_check_1000(entity=f'location "{target.name}"/{target.location_id}',
                                     entity_id=target.location_id,
                                     api=self.async_api.telephony.permissions_out)

    @async_test
    async def test_user_create_1000(self):
        """
        create access code for random user
        """
        target = random.choice(self.users)
        target: Person
        await self.create_check_1000(entity=f'User {target.display_name}({target.emails[0]})/{target.person_id}',
                                     entity_id=target.person_id,
                                     api=self.async_api.person_settings.permissions_out)

    @async_test
    async def test_workspace_create_1000(self):
        """
        create access code for random workspace
        """
        target = random.choice(self.workspaces)
        target: Workspace
        await self.create_check_1000(entity=f'Workspace {target.display_name}/{target.workspace_id}',
                                     entity_id=target.workspace_id,
                                     api=self.async_api.workspace_settings.permissions_out)

    @async_test
    async def test_virtual_line_create_1000(self):
        """
        create access code for random virtual line
        """
        target = random.choice(self.virtual_lines)
        target: VirtualLine
        await self.create_check_1000(entity=f'Virtual Line {target.display_name}/{target.id}',
                                     entity_id=target.id,
                                     api=self.async_api.telephony.virtual_lines.permissions_out)


class TestDigitPatterns(TestLocationsUsersWorkspacesVirtualLines):
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

    async def create_check_500(self, entity: str, entity_id: str, api: AsDigitPatternsApi):
        """
        Try to create 501 patterns and check that we get a proper error
        """
        print(f'target for pattern creation: {entity}')

        patterns = await api.get_digit_patterns(entity_id=entity_id)
        existing = set(p.pattern for p in patterns.digit_patterns)
        new_patterns = (p for i in range(1000) if (p := f'9{i:03}') not in existing)

        # we want to check that we can create 500 patterns and get an error on the 501st
        patterns_to_create = [next(new_patterns) for _ in range(501 - len(existing))]
        tasks = [api.create(entity_id=entity_id,
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
            # try to add the failed pattern again
            pattern = failed[0][0]
            with self.assertRaises(AsRestError) as exc:
                await api.create(entity_id=entity_id,
                                 pattern=DigitPattern(name=f'test_{pattern}', pattern=pattern, action=Action.block,
                                                      transfer_enabled=False))
            rest_error: AsRestError = exc.exception
            self.assertEqual(400, rest_error.status, 'Invalid status code')
        finally:
            # delete patterns again
            await asyncio.gather(*[api.delete(entity_id=entity_id, digit_pattern_id=dp_id)
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
        self.assertTrue(not isinstance(error.detail, str), 'invalid JSON in 400')

        # finally, the number of patterns should be the same as before
        after = await api.get_digit_patterns(entity_id=entity_id)
        self.assertEqual(len(patterns.digit_patterns), len(after.digit_patterns), 'Number of patterns changed')

    @async_test
    async def test_location_create_check_500(self):
        """
        Try to create 501 patterns in location and check that we get a proper error
        """
        target_location = random.choice(self.locations)
        entity = f'Location: {target_location.name}'
        await self.create_check_500(entity=entity, entity_id=target_location.location_id,
                                    api=self.async_api.telephony.permissions_out.digit_patterns)

    @async_test
    async def test_user_create_check_500(self):
        """
        Try to create 501 patterns for random user and check that we get a proper error
        """
        target_user = random.choice(self.users)
        target_user: Person
        entity = f'User: {target_user.display_name} ({target_user.emails[0]})'
        await self.create_check_500(entity=entity, entity_id=target_user.person_id,
                                    api=self.async_api.person_settings.permissions_out.digit_patterns)

    # @skip('Virtual lines don\'t have outgoing permissions yet')
    @async_test
    async def test_virtual_line_create_check_500(self):
        """
        Try to create 501 patterns for random virtual line and check that we get a proper error
        """
        virtual_lines = list(self.api.telephony.virtual_lines.list())
        if not virtual_lines:
            self.skipTest('No virtual lines found')
        target_vl = random.choice(virtual_lines)
        target_vl: VirtualLine
        entity = f'Virtual Line: {target_vl.display_name} in location "{target_vl.location.name}"'
        await self.create_check_500(entity=entity, entity_id=target_vl.id,
                                    api=self.async_api.telephony.virtual_lines.permissions_out.digit_patterns)

    @async_test
    async def test_workspace_create_check_500(self):
        """
        Try to create 501 patterns for random workspace and check that we get a proper error
        """
        workspaces = [ws for ws in self.api.workspaces.list()
                      if ws.calling and ws.calling.type == CallingType.webex]
        if not workspaces:
            self.skipTest('No calling workspaces found')
        target_ws = random.choice(workspaces)
        target_ws: Workspace
        entity = f'Workspace: {target_ws.display_name}"'
        await self.create_check_500(entity=entity, entity_id=target_ws.workspace_id,
                                    api=self.async_api.workspace_settings.permissions_out.digit_patterns)

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

    @skip('Keep test patterns for now')
    @async_test
    async def test_delete_all_patterns(self):
        async def delete_all_xx(*, id_list: list[str], api: AsOutgoingPermissionsApi):
            patterns_list = await asyncio.gather(*[api.digit_patterns.get_digit_patterns(id) for id in id_list])
            id_and_pattern = list(chain.from_iterable(((id, pattern.id)
                                                       for pattern in patterns.digit_patterns
                                                       if pattern.name.startswith('test_'))
                                                      for id, patterns in zip(id_list, patterns_list)))
            print(f'Delete {len(id_and_pattern)} patterns')
            await asyncio.gather(*[api.digit_patterns.delete(id, pattern_id)
                                   for id, pattern_id in id_and_pattern],
                                 return_exceptions=True)
            ...

        location_ids = list(map(attrgetter('location_id'), self.locations))
        user_ids = list(map(attrgetter('person_id'), self.users))
        vl_ids = list(map(attrgetter('id'), self.virtual_lines))
        ws_ids = list(map(attrgetter('workspace_id'), self.workspaces))
        await asyncio.gather(delete_all_xx(id_list=location_ids, api=self.async_api.telephony.permissions_out),
                             delete_all_xx(id_list=user_ids, api=self.async_api.person_settings.permissions_out),
                             delete_all_xx(id_list=vl_ids, api=self.async_api.telephony.virtual_lines.permissions_out),
                             delete_all_xx(id_list=ws_ids, api=self.async_api.workspace_settings.permissions_out))


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


@dataclass(init=False)
class TestBetweenUsers(TestCaseWithLog):
    """
    Test calls between users
    """
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

    def a_can_call_b(self)->TestCallRoutingResult:
        # verify that A can call B
        print('Verifying that A can call B')
        routing_result = self.api.telephony.test_call_routing(
            originator_id=self.user_a.id, originator_type=OriginatorType.user,
            destination=self.user_b.extension,
            originator_number=self.user_a.extension,
            include_applied_services=True)
        self.assertFalse(routing_result.is_rejected,
                         'Call should be accepted')
        self.assertEqual(DestinationType.hosted_agent, routing_result.destination_type,
                         'Unexpected destination type')
        self.assertEqual(self.user_b.id, routing_result.hosted_user.hu_id,
                         'Wrong destination')
        return routing_result

    def a_cant_call_b(self) -> TestCallRoutingResult:
        # verify that A can no longer call B
        print('Verifying that A can no longer call B')
        routing_result = self.api.telephony.test_call_routing(
            originator_id=self.user_a.id, originator_type=OriginatorType.user,
            destination=self.user_b.extension,
            originator_number=self.user_a.extension,
            include_applied_services=True)
        self.assertTrue(routing_result.is_rejected,
                        'Call should be rejected')
        # routing result has to reflect the block
        self.assertEqual(1, len(routing_result.applied_services),
                         'Number of applied services')
        service = routing_result.applied_services[0]
        ocp_by_digit_pattern = service.outgoing_calling_plan_permissions_by_digit_pattern
        self.assertIsNotNone(ocp_by_digit_pattern,
                             'Outgoing calling plan permissions by digit pattern missing')
        self.assertEqual(Action.block, ocp_by_digit_pattern.permission, 'Permission incorrect')
        self.assertEqual(self.user_b.extension, ocp_by_digit_pattern.pattern, 'Digit pattern incorrect')
        self.assertEqual(self.user_b.extension, ocp_by_digit_pattern.number, 'Number incorrect')

        return routing_result

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
        pattern_id = self.api.person_settings.permissions_out.digit_patterns.create(
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
            self.api.person_settings.permissions_out.digit_patterns.delete(entity_id=self.user_a.id,
                                                                           digit_pattern_id=pattern_id)


class TestCallRouting(TestBetweenUsers):
    def test_block_extension_on_location(self):
        """
        Block extension dialing between two users at the location level
        """
        self.a_can_call_b()
        with self.block_b_at_location_level():
            routing_result = self.a_cant_call_b()
            # routing result has to reflect the block at location level
            service = routing_result.applied_services[0]
            ocp_by_digit_pattern = service.outgoing_calling_plan_permissions_by_digit_pattern
            self.assertEqual(ConfigurationLevel.location, ocp_by_digit_pattern.configuration_level,
                             'Configuration level wrong')

    def test_block_extension_on_user_level(self):
        """
        Block extension dialing between two users at the user level
        """
        self.a_can_call_b()
        with self.block_b_at_user_a():
            routing_result = self.a_cant_call_b()
            # routing result has to reflect the block at user level
            service = routing_result.applied_services[0]
            ocp_by_digit_pattern = service.outgoing_calling_plan_permissions_by_digit_pattern
            self.assertEqual(ConfigurationLevel.people, ocp_by_digit_pattern.configuration_level,
                             'Configuration level wrong')

    def test_block_extension_at_location_level_and_allow_at_user_level(self):
        """
        Block extension dialing between two users at the location level and allow at the user level
        """
        self.a_can_call_b()
        with self.block_b_at_location_level():
            routing_result = self.a_cant_call_b()
            self.assertEqual(1, len(routing_result.applied_services))
            applied_service = routing_result.applied_services[0]
            self.assertIsNotNone(applied_service.outgoing_calling_plan_permissions_by_digit_pattern)
            ocp = applied_service.outgoing_calling_plan_permissions_by_digit_pattern
            self.assertEqual(ConfigurationLevel.location, ocp.configuration_level)
            with self.block_b_at_user_a(block=False):
                routing_result = self.a_can_call_b()
                self.assertEqual(1, len(routing_result.applied_services))
                applied_service = routing_result.applied_services[0]
                self.assertIsNotNone(applied_service.outgoing_calling_plan_permissions_by_digit_pattern)
                ocp = applied_service.outgoing_calling_plan_permissions_by_digit_pattern
                self.assertEqual(ConfigurationLevel.people, ocp.configuration_level)

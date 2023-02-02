import asyncio
import contextlib
import random
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from itertools import chain
from typing import ClassVar

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.common import DialPatternStatus, DialPatternValidate, RouteIdentity, ValidationStatus
from wxc_sdk.telephony.prem_pstn.dial_plan import DialPlan, PatternAndAction


@dataclass(init=False)
class TestCreate(TestCaseWithLog):
    dial_plans: ClassVar[list[DialPlan]]
    new_dp_names: ClassVar[Generator[str, None, None]]
    route_choices: ClassVar[list[RouteIdentity]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        dial_plans = list(cls.api.telephony.prem_pstn.dial_plan.list())
        cls.dial_plans = dial_plans
        dp_names = set(dp.name for dp in cls.api.telephony.prem_pstn.dial_plan.list())
        cls.new_dp_names = (dp_name for i in range(1, 1000) if (dp_name := f'TEST_{i:03}') not in dp_names)
        cls.route_choices = list(cls.api.telephony.route_choices())

    @contextlib.contextmanager
    def create(self) -> str:
        dp = self.api.telephony.prem_pstn.dial_plan
        dp_name = next(self.new_dp_names)
        route_choice = random.choice(self.route_choices)
        print(f'Creating dial plan "{dp_name}"')
        dp_id = dp.create(name=dp_name, route_id=route_choice.route_id,
                          route_type=route_choice.route_type).dial_plan_id
        try:
            yield dp_name, dp_id
        finally:
            print(f'Deleting dial plan "{dp_name}"')
            self.api.telephony.prem_pstn.dial_plan.delete_dial_plan(dial_plan_id=dp_id)

    def test_001_no_patterns(self):
        with self.create() as (dp_name, dp_id):
            print(f'Created dial plan {dp_name}: {dp_id}')
            dp_list = list(self.api.telephony.prem_pstn.dial_plan.list(dial_plan_name='TEST'))
            self.assertIsNotNone(next((dp for dp in dp_list
                                       if dp.name == dp_name), None),
                                 f'DP "{dp_name}" could not be found')


class TestList(TestCreate):
    # TODO: tests with different params
    def test_001_list_all(self):
        dp = self.api.telephony.prem_pstn.dial_plan
        dial_plans = list(dp.list())
        print(f'Got {len(dial_plans)} dial plans')

    def test_002_list_by_name(self):
        with contextlib.ExitStack() as st:
            new_dp_names = set()
            for _ in range(5):
                dp_name, _ = st.enter_context(self.create())
                new_dp_names.add(dp_name)
            dp_names = set(dp.name for dp in self.api.telephony.prem_pstn.dial_plan.list(dial_plan_name='TEST'))
            self.assertEqual(new_dp_names, new_dp_names & dp_names)


class TestUpdateDialPlans(TestCreate):
    """
    Tests around updating dial plans (name, rout choice)
    """

    @contextlib.contextmanager
    def assert_dial_plan(self) -> DialPlan:
        if self.dial_plans:
            target = random.choice(self.dial_plans)
            yield target
        else:
            with self.create() as (dp_name, dp_id):
                target = self.api.telephony.prem_pstn.dial_plan.details(dial_plan_id=dp_id)
                yield target

    @contextlib.contextmanager
    def pick_target(self):
        """
        Pick a target dial plan and restore the settings after the test
        """
        with self.assert_dial_plan() as target:
            target: DialPlan
            target_id = target.dial_plan_id
            dp_api = self.api.telephony.prem_pstn.dial_plan
            target = dp_api.details(dial_plan_id=target.dial_plan_id)
            target.dial_plan_id = target_id
            try:
                yield target
            finally:
                # restore previous settings and verify
                dp_api.update(update=target)
                details = dp_api.details(dial_plan_id=target.dial_plan_id)
                self.assertEqual(target.name, details.name)
                self.assertEqual(target.route_id, details.route_id)
                self.assertEqual(target.route_type, details.route_type)

    def update_and_check(self, *, target: DialPlan):
        self.api.telephony.prem_pstn.dial_plan.update(update=target)
        after = self.api.telephony.prem_pstn.dial_plan.details(dial_plan_id=target.dial_plan_id)
        self.assertEqual(target.name, after.name)
        self.assertEqual(target.route_id, after.route_id)
        self.assertEqual(target.route_type, after.route_type)

    def test_001_update_name(self):
        """
        CHange the name of a dial plan
        """
        with self.pick_target() as target:
            target: DialPlan
            new_name = next(self.new_dp_names)
            target.name = new_name
            self.update_and_check(target=target)

    def test_002_update_route_choice(self):
        """
        Update route choice of a dial plan
        """
        route_choices = list(self.api.telephony.route_choices())
        random.shuffle(route_choices)

        with self.pick_target() as target:
            target: DialPlan
            new_route_choice = next((rc for rc in route_choices
                                     if rc.route_id != target.route_id), None)
            self.assertIsNotNone(new_route_choice, 'no other route choice available')
            target.route_id = new_route_choice.route_id
            target.route_type = new_route_choice.route_type
            self.update_and_check(target=target)


class TestDetails(TestCaseWithLog):
    def test_001_all_details(self):
        dp = self.api.telephony.prem_pstn.dial_plan
        dial_plans = list(dp.list())
        with ThreadPoolExecutor() as pool:
            list(pool.map(lambda d: dp.details(dial_plan_id=d.dial_plan_id), dial_plans))
        print(f'Got details for {len(dial_plans)} dial plans')


class TestPatterns(TestCaseWithLog):
    """
    tests on dial plan patterns in dial plans
    """

    def test_001_all_patterns_all_dial_plans(self):
        dp = self.api.telephony.prem_pstn.dial_plan
        dial_plans = list(dp.list())
        with ThreadPoolExecutor() as pool:
            patterns = list(pool.map(lambda d: list(dp.patterns(dial_plan_id=d.dial_plan_id)), dial_plans))
        print(f'Got patterns for {len(dial_plans)} dial plans')
        all_patterns = list(chain.from_iterable(patterns))
        print(f'got {len(all_patterns)} patterns')


class TestPatternValidation(TestCaseWithLog):
    """
    test on dial plan pattern validation
    """

    def test_001_invalid_pattern(self):
        """
        validate an invalid pattern
        """
        result = self.api.telephony.prem_pstn.validate_pattern(dial_patterns=['+1456!!'])
        print(result)
        self.assertEqual(result.status, ValidationStatus.errors)
        self.assertEqual(1, len(result.dial_pattern_status))
        self.assertEqual(DialPatternStatus.invalid, result.dial_pattern_status[0].pattern_status)

    def test_002_invalid_pattern(self):
        """
        validate an invalid pattern
        """
        result = self.api.telephony.prem_pstn.validate_pattern(dial_patterns='+1456X234')
        print(result)
        self.assertEqual(result.status, ValidationStatus.errors)
        self.assertEqual(1, len(result.dial_pattern_status))
        self.assertEqual(DialPatternStatus.invalid, result.dial_pattern_status[0].pattern_status)

    def test_003_invalid_pattern(self):
        """
        Validate a list of invalid patterns
        """
        result = self.api.telephony.prem_pstn.validate_pattern(dial_patterns=['+1456!!',
                                                                              '845X8'])
        print(result)
        self.assertEqual(result.status, ValidationStatus.errors)
        self.assertEqual(2, len(result.dial_pattern_status))
        self.assertTrue(all(s.pattern_status == DialPatternStatus.invalid for s in result.dial_pattern_status))

    def test_004_invalid_and_duplicate_in_list(self):
        """
        Validate some invalid and some duplicate in list patterns together
        """
        invalid = ['+124!!', '456!']
        d_in_list = ['456X', '+496100!']
        patterns = invalid + d_in_list + d_in_list
        random.shuffle(patterns)
        result = self.api.telephony.prem_pstn.validate_pattern(dial_patterns=patterns)
        print(result)
        self.assertEqual(result.status, ValidationStatus.errors)

        result_by_pattern = {r.dial_pattern: r for r in result.dial_pattern_status}
        result_by_pattern: dict[str, DialPatternValidate]
        err = False
        for p in invalid:
            r = result_by_pattern.get(p)
            if not r:
                print(f'{p}: no result')
                err = True
                continue
            if r.pattern_status != DialPatternStatus.invalid:
                print(f'{p}: status {r.pattern_status}, expected INVALID')
                err = True
        for p in d_in_list:
            r = result_by_pattern.get(p)
            if not r:
                print(f'{p}: no result')
                err = True
                continue
            if r.pattern_status != DialPatternStatus.duplicate_in_list:
                print(f'{p}: status {r.pattern_status}, expected {DialPatternStatus.duplicate_in_list.value}')
                err = True
        self.assertFalse(err)

    def all_patterns(self) -> list[str]:
        """
        Get all patterns of al dial plans
        :return:
        """
        with self.no_log():
            dp = self.api.telephony.prem_pstn.dial_plan
            dial_plans = list(dp.list())
            with ThreadPoolExecutor() as pool:
                patterns = list(pool.map(lambda d: list(dp.patterns(dial_plan_id=d.dial_plan_id)), dial_plans))
        return list(chain.from_iterable(patterns))

    def test_005_duplicate_pattern(self):
        """
        Validate some patterns already in a dial plan
        :return:
        """
        existing_patterns = self.all_patterns()
        if not existing_patterns:
            self.skipTest('Need some existing dial plan patterns')
        patterns = random.sample(existing_patterns, 10)
        result = self.api.telephony.prem_pstn.validate_pattern(dial_patterns=patterns)
        print(result)
        self.assertEqual(result.status, ValidationStatus.errors)
        self.assertEqual(len(patterns), len(result.dial_pattern_status))
        self.assertTrue(all(s.pattern_status == DialPatternStatus.duplicate for s in result.dial_pattern_status))

    def test_006_duplicate_in_list(self):
        result = self.api.telephony.prem_pstn.validate_pattern(dial_patterns=['+1456!', '+1456!'])
        print(result)
        self.assertEqual(result.status, ValidationStatus.errors)
        self.assertEqual(1, len(result.dial_pattern_status))
        self.assertEqual(DialPatternStatus.duplicate_in_list, result.dial_pattern_status[0].pattern_status)


@dataclass(init=False)
class TestModifyPatterns(TestCaseWithLog):
    """
    Test cases to modify patterns in dial plan
    """
    existing_patterns: ClassVar[set[str]]
    new_e164_patterns: ClassVar[Generator[str, None, None]]
    new_ent_patterns: ClassVar[Generator[str, None, None]]
    new_class_names: ClassVar[Generator[str, None, None]]
    route_choices: ClassVar[list[RouteIdentity]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        dp = cls.api.telephony.prem_pstn.dial_plan
        dial_plans = list(dp.list())
        with ThreadPoolExecutor() as pool:
            patterns = list(pool.map(lambda d: list(dp.patterns(dial_plan_id=d.dial_plan_id)), dial_plans))
        cls.existing_patterns = set(chain.from_iterable(patterns))
        cls.new_e164_patterns = (pattern for i in range(100000)
                                 if (pattern := f'+4961007{i:05}') not in cls.existing_patterns)
        cls.new_ent_patterns = (pattern for i in range(100000)
                                if (pattern := f'849{i:05}') not in cls.existing_patterns)
        cls.new_dp_names = (name for i in range(1000)
                            if (name := f'TEST_{i:03}') not in set(d.name for d in dial_plans))
        cls.route_choices = list(cls.api.telephony.route_choices())

    def test_001_create_empty_add_patterns(self):
        """
        Create a dial plan with no patterns and add a bunch
        :return:
        """
        # create dial plan
        dp_api = self.api.telephony.prem_pstn.dial_plan
        dp_name = next(self.new_dp_names)
        route_choice = random.choice(self.route_choices)
        dp_id = dp_api.create(name=dp_name, route_id=route_choice.route_id,
                              route_type=route_choice.route_type).dial_plan_id

        try:
            # add 5 enterprise and 5 +E.164 patterns
            new_patterns = [next(self.new_e164_patterns) for _ in range(5)]
            new_patterns.extend(next(self.new_ent_patterns) for _ in range(5))
            random.shuffle(new_patterns)

            patterns_before = list(dp_api.patterns(dial_plan_id=dp_id))
            dp_api.modify_patterns(dial_plan_id=dp_id, dial_patterns=[PatternAndAction.add(p) for p in new_patterns])
            patterns_after = list(dp_api.patterns(dial_plan_id=dp_id))

            self.assertTrue(not patterns_before, 'There should be no patterns in the dial plan after creation')
            self.assertEqual(len(new_patterns), len(patterns_after), 'number of patterns after update doesn\'t match')
            self.assertTrue(all(p in set(patterns_after) for p in new_patterns), 'not all new patterns added')
        finally:
            # clean up: delete dial plan
            dp_api.delete_dial_plan(dial_plan_id=dp_id)

    # noinspection DuplicatedCode
    def test_002_create_and_modify(self):
        """
        Create a dial plan with a bunch of patterns and then modify
        :return:
        """
        dp_api = self.api.telephony.prem_pstn.dial_plan
        dp_name = next(self.new_dp_names)
        route_choice = random.choice(self.route_choices)
        initial_patterns = list(chain.from_iterable((next(self.new_e164_patterns), next(self.new_ent_patterns))
                                                    for _ in range(100)))
        random.shuffle(initial_patterns)
        dp_id = dp_api.create(name=dp_name, route_id=route_choice.route_id, route_type=route_choice.route_type,
                              dial_patterns=initial_patterns).dial_plan_id
        try:
            new_patterns = list(chain.from_iterable((next(self.new_e164_patterns), next(self.new_ent_patterns))
                                                    for _ in range(25)))
            del_patterns = random.sample(initial_patterns, 50)
            pattern_update = [PatternAndAction.add(p) for p in new_patterns]
            pattern_update.extend(PatternAndAction.delete(p) for p in del_patterns)
            random.shuffle(pattern_update)

            patterns_before = set(dp_api.patterns(dial_plan_id=dp_id))
            dp_api.modify_patterns(dial_plan_id=dp_id, dial_patterns=pattern_update)
            patterns_after = set(dp_api.patterns(dial_plan_id=dp_id))

            self.assertEqual(len(initial_patterns), len(patterns_before), 'Not all patterns added in create()')
            self.assertFalse((missing := [p for p in initial_patterns if p not in patterns_before]),
                             f'patterns not added during creation: {", ".join(missing)}')
            self.assertFalse((not_deleted := [p for p in del_patterns if p in patterns_after]),
                             f'patterns not deleted: {", ".join(not_deleted)}')
            self.assertFalse((not_added := [p for p in new_patterns if p not in patterns_after]),
                             f'patterns not added: {", ".join(not_added)}')
            self.assertEqual(len(patterns_before), len(patterns_after))

        finally:
            # clean up: delete dial plan
            dp_api.delete_dial_plan(dial_plan_id=dp_id)

    # noinspection DuplicatedCode
    def test_003_delete_all_patterns(self):
        """
        Create a dial plan with a bunch of patterns and delete all of them
        :return:
        """
        dp_api = self.api.telephony.prem_pstn.dial_plan
        dp_name = next(self.new_dp_names)
        route_choice = random.choice(self.route_choices)
        initial_patterns = list(chain.from_iterable((next(self.new_e164_patterns), next(self.new_ent_patterns))
                                                    for _ in range(100)))
        random.shuffle(initial_patterns)
        dp_id = dp_api.create(name=dp_name, route_id=route_choice.route_id, route_type=route_choice.route_type,
                              dial_patterns=initial_patterns).dial_plan_id
        try:
            patterns_before = set(dp_api.patterns(dial_plan_id=dp_id))
            dp_api.delete_all_patterns(dial_plan_id=dp_id)
            patterns_after = set(dp_api.patterns(dial_plan_id=dp_id))

            self.assertEqual(len(initial_patterns), len(patterns_before), 'Not all patterns added in create()')
            self.assertFalse((missing := [p for p in initial_patterns if p not in patterns_before]),
                             f'patterns not added during creation: {", ".join(missing)}')
            self.assertTrue(not patterns_after, 'Still some patterns present after delete_all_patterns')

        finally:
            # clean up: delete dial plan
            dp_api.delete_dial_plan(dial_plan_id=dp_id)

    def test_004_create_invalid_patterns(self):
        """
        Create a dial plan with duplicate patterns
        :return:
        """
        dp_api = self.api.telephony.prem_pstn.dial_plan
        dp_name = next(self.new_dp_names)
        route_choice = random.choice(self.route_choices)
        if not self.existing_patterns:
            self.skipTest('Need existing dial plan patterns to run this test')
        initial_patterns = random.sample(self.existing_patterns, min(10, len(self.existing_patterns)))
        random.shuffle(initial_patterns)
        result = dp_api.create(name=dp_name, route_id=route_choice.route_id, route_type=route_choice.route_type,
                               dial_patterns=initial_patterns)
        dp_id = result.dial_plan_id
        try:
            self.assertEqual(len(initial_patterns), len(result.dial_pattern_errors))
        finally:
            # clean up: delete dial plan
            dp_api.delete_dial_plan(dial_plan_id=dp_id)


class TestCreateLargeDialPlan(TestCaseWithLog):

    @async_test
    async def test_001_create_dp_6000_patterns(self):
        """
        Create a dial plan and add 6000 pattern
        """
        api = self.async_api.telephony.prem_pstn.dial_plan
        dial_plans = await api.list()
        dp_names = set(dp.name for dp in dial_plans)
        patterns = set(chain.from_iterable(await asyncio.gather(*[api.patterns(dial_plan_id=dp.dial_plan_id)
                                                                  for dp in dial_plans])))
        new_dp_names = (name for i in range(1, 1000)
                        if (name := f'test_{i:03}') not in dp_names)
        dp_name = next(new_dp_names)
        route_choices = await self.async_api.telephony.route_choices()
        route_choice = random.choice(route_choices)

        # create dp
        dp_id = (await api.create(name=dp_name,
                                  route_id=route_choice.route_id,
                                  route_type=route_choice.route_type)).dial_plan_id

        try:
            new_patterns = (pattern for i in range(1, 1000000)
                            if (pattern := f'+4961001{i:06}') not in patterns)
            # add new patterns in batches of
            batch_size = 200
            batches = int(6000 / batch_size)
            tasks = [api.modify_patterns(dial_plan_id=dp_id,
                                         dial_patterns=[PatternAndAction.add(next(new_patterns))
                                                        for _ in range(batch_size)])
                     for _ in range(batches)]
            await asyncio.gather(*tasks)
            patterns_after = await api.patterns(dial_plan_id=dp_id)
            print(f'Created dial plan "{dp_name}" with {len(patterns_after)} patterns')
            self.assertEqual(6000, len(patterns_after))

        except Exception:
            # if adding patterns fails then remove the dial plan again
            await api.delete_dial_plan(dial_plan_id=dp_id)
            raise


class TestDeleteAllTestDialPlans(TestCaseWithLog):
    def test_delete_all(self):
        api = self.api.telephony.prem_pstn.dial_plan
        dps = [dp for dp in api.list()
               if dp.name.upper().startswith('TEST_')]
        if not dps:
            self.skipTest('No Test dial plans to delete')
            return
        with ThreadPoolExecutor() as pool:
            list(pool.map(lambda dp: api.delete_dial_plan(dial_plan_id=dp.dial_plan_id), dps))

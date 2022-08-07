import base64
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import reduce
from itertools import chain
from json import dumps, loads
from random import shuffle, choice, randint
from typing import ClassVar, Optional, Generator, Union

from tests.base import TestCaseWithLog
from wxc_sdk.common import RouteType, RouteIdentity, UserType, NumberState
from wxc_sdk.common.schedules import Schedule, ScheduleType
from wxc_sdk.locations import Location
from wxc_sdk.people import Person
from wxc_sdk.rest import RestError
from wxc_sdk.telephony import OriginatorType, DestinationType, NumberType, CallSourceType, TestCallRoutingResult, \
    HostedFeatureDestination, ServiceType, HostedUserDestination, CallSourceInfo, PbxUserDestination, OwnerType, \
    NumberListPhoneNumberType
from wxc_sdk.telephony.autoattendant import AutoAttendant, AutoAttendantMenu
from wxc_sdk.telephony.huntgroup import HuntGroup
from wxc_sdk.telephony.location.internal_dialing import InternalDialing
from wxc_sdk.telephony.prem_pstn.dial_plan import DialPlan
from wxc_sdk.telephony.prem_pstn.trunk import TrunkDetail
from .testutil import calling_users, us_location_info, LocationInfo, available_extensions, available_tns


@dataclass
class DpContext:
    test: 'TestCallRouting'
    location: Location = field(init=False)
    location_users: list[Person] = field(init=False)
    trunk: TrunkDetail = field(init=False)
    dial_plan: DialPlan = field(init=False)
    prem_pattern: str = field(init=False)
    prem_numbers: list[str] = field(init=False)
    pstn_number: str = field(init=False)

    _used_numbers: set[str] = field(init=False, default_factory=set)
    _avail_generators: dict[str, Generator[str, None, None]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        """
        actually set the context
        :return:
        """
        with self.test.no_log():
            users = self.test.calling_users
            # group users by location
            users_by_location = reduce(lambda reduced, user: reduced[user.location_id].append(user) or reduced,
                                       users,
                                       defaultdict(list))
            # pick a random location
            location_id = choice(list(users_by_location))
            # get location details
            self.location = self.test.api.locations.details(location_id=location_id)
            self.location_users = users_by_location[location_id]

            # create a trunk in that location
            trunk_name = self.available_trunk_name(location_name=self.location.name)
            pwd = self.test.api.telephony.location.generate_password(location_id=location_id)
            print(f'Creating trunk "{trunk_name}" in location "{self.location.name}"')
            trunk_id = self.test.api.telephony.prem_pstn.trunk.create(name=trunk_name,
                                                                      location_id=location_id,
                                                                      password=pwd)
            self.trunk = self.test.api.telephony.prem_pstn.trunk.details(trunk_id=trunk_id)

            # create a dial plan using that trunk as destination
            dial_plans = list(self.test.api.telephony.prem_pstn.dial_plan.list())
            dp_name = next(name for i in range(1, 100)
                           if (name := f'{self.location.name} {i:02}') not in set(dp.name for dp in dial_plans))

            # we also need an E.164 number that is not part of any dial plan and not a WxC TN
            self._numbers = set(
                n.phone_number for n in self.test.api.telephony.phone_numbers(number_type=NumberType.number))
            with ThreadPoolExecutor() as pool:
                self._used_numbers.update(n for n in chain.from_iterable(
                    pool.map(lambda dp: list(self.test.api.telephony.prem_pstn.dial_plan.patterns(
                        dial_plan_id=dp.dial_plan_id)),
                             dial_plans))
                                          if n.startswith('+'))
            self.pstn_number = self.available_pstn_number(prefix='+12125550')
            self.prem_pattern = next(self.available_wildcard(prefix="+1408555", wildcard_digits=2))
            self.prem_numbers = [f'{self.prem_pattern[:10]}{i:02}' for i in range(1, 100)]

            print(f'Creating dial plan "{dp_name}" with pattern "{self.prem_pattern}"')
            dp_id = self.test.api.telephony.prem_pstn.dial_plan.create(name=dp_name,
                                                                       route_id=trunk_id,
                                                                       route_type=RouteType.trunk,
                                                                       dial_patterns=[self.prem_pattern]).dial_plan_id
            self.dial_plan = self.test.api.telephony.prem_pstn.dial_plan.details(dial_plan_id=dp_id)

    def available_trunk_name(self, location_name: str) -> str:
        """
        Get an available trunk name for a given location
        :param location_name:
        :return:
        """
        trunks_in_location = list(self.test.api.telephony.prem_pstn.trunk.list(location_name=location_name))
        trunk_names = set(t.name for t in trunks_in_location)
        trunk_name = next(name for i in range(1, 100)
                          if (name := f'{location_name} {i:02}') not in trunk_names)
        return trunk_name

    def available_pstn_number(self, prefix: str) -> str:
        open_digits = 12 - len(prefix)
        avail_gen = self._avail_generators.get(prefix)
        if avail_gen is None:
            avail_gen = (self._used_numbers.add(number) or number for i in range(1, 10 ** open_digits)
                         if (number := f'{prefix}{i:0{open_digits}}') not in self._used_numbers)
            self._avail_generators[prefix] = avail_gen
        return next(avail_gen)

    def available_wildcard(self, *, prefix: str, wildcard_digits: int):
        """
        get an available prefix
        :param prefix:
        :param wildcard_digits:
        :return:
        """
        variable_digits = 12 - len(prefix) - wildcard_digits
        if variable_digits <= 0:
            raise ValueError('Invalid parameters')
        variable_strings = [f'{i:0{variable_digits}}' for i in range(1, 10 ** variable_digits)]
        wildcarded = [f'{i:0{wildcard_digits}}' for i in range(1, 10 ** wildcard_digits)]
        for variable_string in variable_strings:
            v_prefix = f'{prefix}{variable_string}'
            numbers = set(f'{v_prefix}{wildcard_number}' for wildcard_number in wildcarded)
            if not self._used_numbers & numbers:
                self._used_numbers.update(numbers)
                yield f'{v_prefix}{"X" * wildcard_digits}'

    def cleanup(self):
        """
        delete the stuff we created
        :return:
        """
        with self.test.no_log():
            print(f'Deleting dial plan "{self.dial_plan.name}"')
            self.test.api.telephony.prem_pstn.dial_plan.delete_dial_plan(dial_plan_id=self.dial_plan.dial_plan_id)
            print(f'Deleting trunk "{self.trunk.name}"')
            self.test.api.telephony.prem_pstn.trunk.delete_trunk(trunk_id=self.trunk.trunk_id)


@dataclass(init=False)
class TestCallRouting(TestCaseWithLog):
    dp_context: ClassVar[Optional[DpContext]] = field(default=None)
    _calling_users: list[Person] = field(default=None)
    _location_infos: ClassVar[Optional[list[LocationInfo]]] = field(default=None)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.dp_context = None
        cls._location_infos = None

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.dp_context:
            cls.dp_context.cleanup()
        super().tearDownClass()

    @property
    def location_infos(self) -> list[LocationInfo]:
        if self._location_infos is None:
            with self.no_log():
                self.__class__._location_infos = us_location_info(api=self.api)
        return self._location_infos

    @property
    def locations(self) -> list[Location]:
        return [li.location for li in self.location_infos]

    @property
    def calling_users(self) -> list[Person]:
        """
        list of users which are enabled for calling
        """
        if self._calling_users is None:
            with self.no_log():
                with ThreadPoolExecutor() as pool:
                    users = list(pool.map(lambda user: self.api.people.details(person_id=user.person_id,
                                                                               calling_data=True),
                                          calling_users(api=self.api)))
                loc_ids = set(loc.location_id for loc in self.locations)
                users = [user for user in users
                         if user.location_id in loc_ids]

            self._calling_users = users
        return self._calling_users

    @contextmanager
    def assert_dial_plan_context(self) -> DpContext:
        """
        """
        if self.dp_context is None:
            self.__class__.dp_context = DpContext(test=self)
        yield self.dp_context

    @staticmethod
    def print_result(*, result: TestCallRoutingResult):
        print(dumps(loads(result.json()), indent=2))


class TestUsersAndTrunks(TestCallRouting):
    @TestCaseWithLog.async_test
    async def test_001_user_to_user_extension_same_location(self):
        """
        User A calls user B by dialing user B's extension
        """
        # only consider calling users with extensions
        users = [user for user in self.calling_users
                 if user.extension]

        # group users by location
        users_by_location: dict[str, list[Person]] = reduce(
            lambda r, user: r[user.location_id].append(user) or r, users,
            defaultdict(list))

        # pick random location from locations with at least two users
        try:
            location_id = choice([lid for lid, users in users_by_location.items()
                                  if len(users) > 1])
        except IndexError:
            location_id = None
            self.skipTest('Need at least two users with extensions in the same location to run this test')

        # pick two random users within location
        location_users = users_by_location[location_id]
        shuffle(location_users)
        calling = location_users[0]
        called = location_users[1]
        location = next(loc for loc in self.locations if loc.location_id == location_id)

        # test and verify routing
        print(f'"{calling.display_name}" ({calling.extension}) calling {called.display_name} ({called.extension})')
        test_result = await self.async_api.telephony.test_call_routing(originator_id=calling.person_id,
                                                                       originator_type=OriginatorType.user,
                                                                       destination=called.extension)
        self.print_result(result=test_result)
        expected = TestCallRoutingResult(
            destination_type=DestinationType.hosted_user,
            routing_address=called.extension,
            is_rejected=False,
            hosted_user=HostedUserDestination(
                location_name=location.name,
                location_id=location_id,
                extension=called.extension,
                phone_number=called.tn and called.tn.value,
                hu_id=called.person_id,
                hu_type=UserType.people,
                first_name=called.first_name,
                last_name=called.last_name))
        try:
            self.assertEqual(expected, test_result)
        except AssertionError:
            if called.location_id != test_result.hosted_user.location_id:
                print(f'Location id: {base64.b64decode(location_id + "==")}')
                print(f'hosted user Location id: {base64.b64decode(test_result.hosted_user.location_id + "==")}')
            test_result.hosted_user.location_id = location_id
            try:
                self.assertEqual(expected, test_result)
            except AssertionError:
                raise
            else:
                print('No other issues other than wrong location id format')
                raise

    def test_002_user_to_user_e164(self):
        """
        User calls another user dialing the user's TN
        """
        # all TNs used as primary TN
        # TODO: create active TN and temporarily add to user
        primary_tns = list(self.api.telephony.phone_numbers(owner_type=OwnerType.people,
                                                            phone_number_type=NumberListPhoneNumberType.primary,
                                                            state=NumberState.active))
        if not primary_tns:
            self.skipTest('Need at least one user with a TN')
        called_tn = choice(primary_tns)
        called = next(user for user in self.calling_users
                      if user.person_id == called_tn.owner.owner_id)
        caller = choice([user for user in self.calling_users
                         if user.person_id != called.person_id])
        result = self.api.telephony.test_call_routing(originator_id=caller.person_id,
                                                      originator_type=OriginatorType.user,
                                                      destination=called_tn.phone_number)
        self.print_result(result=result)

    def test_002_trunk_prem_to_user_extension(self):
        """
        Call from a trunk to an extension with +E.164 caller ID of a prem user is expected to work
        :return:
        """
        with self.assert_dial_plan_context() as ctx:
            ctx: DpContext
            users_w_extension = [u for u in ctx.location_users if u.extension]
            called = choice(users_w_extension)
            originator = choice(ctx.prem_numbers)
            print(f'Call from trunk "{ctx.trunk.name}" from "{originator}" to "{called.extension}"')
            print(f'trunk location: {ctx.trunk.location.name}')
            internal_dialing = self.api.telephony.location.internal_dialing.read(location_id=ctx.location.location_id)
            print(f'trunk location internal dialing: {internal_dialing}')
            test_result = self.api.telephony.test_call_routing(originator_id=ctx.trunk.trunk_id,
                                                               originator_type=OriginatorType.trunk,
                                                               destination=called.extension,
                                                               originator_number=originator)
            self.print_result(result=test_result)
            # before testing we ignore the location id in the hosted user destination
            # we alrady know that this is broken
            # TODO: monitor defect for wrong id format and remove if not needed any more
            test_result.hosted_user.location_id = called.location_id
            self.assertEqual(TestCallRoutingResult(
                call_source_info=CallSourceInfo(
                    call_source_type=CallSourceType.dial_pattern,
                    dial_plan_name=ctx.dial_plan.name,
                    dial_pattern=ctx.prem_pattern,
                    dial_plan_id=ctx.dial_plan.dial_plan_id
                ),
                destination_type=DestinationType.hosted_user,
                routing_address=called.extension,
                is_rejected=False,
                hosted_user=HostedUserDestination(
                    location_name=ctx.location.name,
                    location_id=called.location_id,
                    extension=called.extension,
                    phone_number=(ctn := called.tn) and ctn.value,
                    hu_id=called.person_id,
                    hu_type=UserType.people,
                    first_name=called.first_name,
                    last_name=called.last_name
                )
            ),
                test_result)

    def test_003_trunk_pstn_to_user_extension(self):
        """
        Call from a trunk to an extension with caller ID of a PSTN number is expected to fail
        """
        with self.assert_dial_plan_context() as ctx:
            ctx: DpContext
            users_w_extension = [u for u in ctx.location_users if u.extension]
            called = choice(users_w_extension)
            # the test is expected to fail
            with self.assertRaises(RestError) as exc:
                test_result = self.api.telephony.test_call_routing(originator_id=ctx.trunk.trunk_id,
                                                                   originator_type=OriginatorType.trunk,
                                                                   destination=called.extension,
                                                                   originator_number=ctx.pstn_number)
            rest_error: RestError = exc.exception
            self.assertEqual(111602, rest_error.code)
            self.assertEqual(f'This call is an inbound PSTN call from unknown number {ctx.pstn_number} '
                             f'in standard mode',
                             rest_error.description)

    def test_004_trunk_ext_to_user_ext_unknown_extension_routing_enabled(self):
        """
        Call from a trunk with extension as caller id to a user's extension should work
        """
        with self.assert_dial_plan_context() as ctx:
            ctx: DpContext
            users_w_extension = [u for u in ctx.location_users if u.extension]
            called = choice(users_w_extension)
            # make sure that unknown extension routing is enabled with "our" trunk as destination
            with self.no_log():
                internal_dialing_before = self.api.telephony.location.internal_dialing.read(
                    location_id=ctx.location.location_id)
                self.api.telephony.location.internal_dialing.update(
                    location_id=ctx.location.location_id,
                    update=InternalDialing(enable_unknown_extension_route_policy=True,
                                           unknown_extension_route_identity=RouteIdentity(
                                               route_id=ctx.trunk.trunk_id,
                                               route_type=RouteType.trunk)))
            try:
                test_result = self.api.telephony.test_call_routing(originator_id=ctx.trunk.trunk_id,
                                                                   originator_type=OriginatorType.trunk,
                                                                   destination=called.extension,
                                                                   originator_number='1234')
                self.print_result(result=test_result)

                self.assertIsNotNone(test_result.call_source_info)
                self.assertEqual(CallSourceType.unknown_extension, test_result.call_source_info.call_source_type)
                self.assertFalse(test_result.is_rejected)
                self.assertEqual(DestinationType.hosted_user, test_result.destination_type)
                self.assertEqual(called.person_id, test_result.hosted_user.hu_id)
            finally:
                # restore internal dialing settings
                with self.no_log():
                    self.api.telephony.location.internal_dialing.update(location_id=ctx.location.location_id,
                                                                        update=internal_dialing_before)

    def test_005_trunk_ext_to_user_ext_unknown_extension_routing_disabled(self):
        """
        Call from a trunk with extension as caller id to a user's extension should fail
        """
        with self.assert_dial_plan_context() as ctx:
            ctx: DpContext
            users_w_extension = [u for u in ctx.location_users if u.extension]
            called = choice(users_w_extension)
            # make sure that unknown extension routing is enabled with "our" trunk as destination
            with self.no_log():
                # read internal dialing settigs of location (need to restore old settings after test)
                internal_dialing_before = self.api.telephony.location.internal_dialing.read(
                    location_id=ctx.location.location_id)
                # enable unknown extension dialing; destination is the trunk we just created
                self.api.telephony.location.internal_dialing.update(
                    location_id=ctx.location.location_id,
                    update=InternalDialing(enable_unknown_extension_route_policy=False))
            try:
                with self.assertRaises(RestError) as exc:
                    test_result = self.api.telephony.test_call_routing(originator_id=ctx.trunk.trunk_id,
                                                                       originator_type=OriginatorType.trunk,
                                                                       destination=called.extension,
                                                                       originator_number='1234')
                rest_error: RestError = exc.exception
                self.assertEqual(111602, rest_error.code)
                self.assertEqual(f'This call is an inbound PSTN call from unknown number 1234 '
                                 f'in standard mode',
                                 rest_error.description)

            finally:
                # restore internal dialing settings
                with self.no_log():
                    self.api.telephony.location.internal_dialing.update(location_id=ctx.location.location_id,
                                                                        update=internal_dialing_before)

    def test_006_trunk_to_trunk_from_prem_e164(self):
        """
        Call from trunk to trunk (match on e164 pattern). Caller is E.164 based on DP match
        :return:
        """
        with self.assert_dial_plan_context() as ctx:
            ctx: DpContext
            with self.no_log():
                # pick a different location
                available_locations = [location for location in self.locations if
                                       location.location_id != ctx.location.location_id
                                       and location.address.country != 'IN']
                if not available_locations:
                    self.skipTest('Test ')
                location = choice(available_locations)
                # create a trunk in that location
                trunk_name = ctx.available_trunk_name(location_name=location.name)
                pwd = self.api.telephony.location.generate_password(
                    location_id=location.location_id)
                print(f'Creating trunk "{trunk_name}" in location "{location.name}"')
                with self.no_log():
                    trunk_id = self.api.telephony.prem_pstn.trunk.create(name=trunk_name,
                                                                         location_id=location.location_id,
                                                                         password=pwd)
                try:
                    # create a dial plan with a PSTN pattern in that location
                    prem_pattern = next(ctx.available_wildcard(prefix='+1408555', wildcard_digits=2))
                    prem_number = f'{prem_pattern[:10]}{randint(1, 99):02}'
                    dp_names = set(dp.name
                                   for dp in self.api.telephony.prem_pstn.dial_plan.list(dial_plan_name=location.name))
                    dp_name = next(name for i in range(1, 100)
                                   if (name := f'{location.name} {i:02}') not in dp_names)
                    print(f'Creating dial plan "{dp_name}" with pattern "{prem_pattern}"')
                    with self.no_log():
                        dp_id = self.api.telephony.prem_pstn.dial_plan.create(name=dp_name,
                                                                              route_id=trunk_id,
                                                                              route_type=RouteType.trunk,
                                                                              dial_patterns=[prem_pattern]).dial_plan_id
                    try:
                        originator_number = choice(ctx.prem_numbers)
                        print(f'Originator {originator_number} from trunk "{ctx.trunk.name}" calls {prem_number}'
                              f'(dp match on {prem_pattern}" in dial plan "{dp_name}" pointing to trunk "{trunk_name}"')
                        with self.with_log():
                            result = self.api.telephony.test_call_routing(originator_id=ctx.trunk.trunk_id,
                                                                          originator_type=OriginatorType.trunk,
                                                                          originator_number=originator_number,
                                                                          destination=prem_number)
                        self.print_result(result=result)
                        self.assertEqual(TestCallRoutingResult(
                            call_source_info=CallSourceInfo(
                                call_source_type=CallSourceType.dial_pattern,
                                dial_plan_name=ctx.dial_plan.name,
                                dial_pattern=ctx.prem_pattern,
                                dial_plan_id=ctx.dial_plan.dial_plan_id
                            ),
                            destination_type=DestinationType.pbx_user,
                            routing_address=prem_number,
                            is_rejected=False,
                            pbx_user=PbxUserDestination(
                                trunk_name=trunk_name,
                                trunk_id=trunk_id,
                                trunk_location_name=location.name,
                                trunk_location_id=location.location_id,
                                dial_plan_name=dp_name,
                                dial_plan_id=dp_id,
                                dial_pattern=prem_pattern,
                                premises_dial_pattern=prem_pattern
                            )),
                            result)
                    finally:
                        print(f'Deleting dial plan "{dp_name}"')
                        with self.no_log():
                            self.api.telephony.prem_pstn.dial_plan.delete_dial_plan(dial_plan_id=dp_id)
                    # test
                finally:
                    # clean: remove trunk
                    print(f'Deleting trunk "{trunk_name}"')
                    with self.no_log():
                        self.api.telephony.prem_pstn.trunk.delete_trunk(trunk_id=trunk_id)


@dataclass
class AAContext:
    """
    An auto-attendant context to be used for call routing tests with AA as destination
    """
    test: 'TestHostedFeature'
    location: Location
    aa_tn: str = field(init=False, default=None)
    sched_name: str = field(init=False, default=None)
    sched_id: str = field(init=False, default=None)
    aa_name: str = field(init=False, default=None)
    aa_id: str = field(init=False, default=None)
    auto_attendant: AutoAttendant = field(init=False, default=None)

    def __post_init__(self):
        with self.test.no_log():
            aa_list = list(self.test.api.telephony.auto_attendant.list(location_id=self.location.location_id))
            aa_names = set(aa.name for aa in aa_list)
            aa_name = next(name for i in range(1, 99)
                           if (name := f'{self.location.name} {i:02}') not in aa_names)
            self.aa_name = aa_name

            # phone number for AA
            aa_extension = available_extensions(api=self.test.api, location_id=self.location.location_id)[0]
            loc_info = next(li for li in self.test.location_infos
                            if li.location.location_id == self.location.location_id)
            aa_tn = available_tns(api=self.test.api,
                                  tn_prefix=loc_info.main_number[:9])[0]
            # add number to location
            print(f'adding TN "{aa_tn}" to location "{self.location.name}')
            try:
                self.test.api.telephony.location.number.add(location_id=self.location.location_id,
                                                            phone_numbers=[aa_tn],
                                                            state=NumberState.active)
                self.aa_tn = aa_tn

                # we also create a schedule to be used for the auto attendant
                schedules = list(self.test.api.telephony.schedules.list(obj_id=self.location.location_id))
                sched_names = set(sched.name for sched in schedules)
                sched_name = next(name for i in range(1, 99)
                                  if (name := f'{self.location.name} {i:02}') not in sched_names)
                self.sched_name = sched_name
                print(f'Creating business schedule "{sched_name}" in location "{self.location.name}')
                sched_id = self.test.api.telephony.schedules.create(obj_id=self.location.location_id,
                                                                    schedule=Schedule.business(name=sched_name))
                self.sched_id = sched_id

                # create AA
                print(f'Creating AA "{aa_name}" in location "{self.location.name}"')
                aa = AutoAttendant(name=aa_name,
                                   enabled=True,
                                   phone_number=aa_tn,
                                   extension=aa_extension,
                                   first_name='AA',
                                   last_name=aa_name,
                                   business_schedule=sched_name,
                                   business_hours_menu=AutoAttendantMenu.default(),
                                   after_hours_menu=AutoAttendantMenu.default())
                aa_id = self.test.api.telephony.auto_attendant.create(
                    location_id=self.location.location_id,
                    settings=aa)
                aa.auto_attendant_id = aa_id
                self.aa_id = aa_id
                self.auto_attendant = aa
            except:
                self.clean_up()

    def clean_up(self):
        """
        Try to remove all stuff again
        :return:
        """
        try:
            if self.aa_id:
                print(f'Deleting AA "{self.aa_name}" in location "{self.location.name}"')
                self.test.api.telephony.auto_attendant.delete_auto_attendant(
                    location_id=self.location.location_id, auto_attendant_id=self.aa_id)
        finally:
            try:
                if self.sched_id:
                    print(f'Deleting business schedule "{self.sched_name}" in location "{self.location.name}')
                    self.test.api.telephony.schedules.delete_schedule(obj_id=self.location.location_id,
                                                                      schedule_type=ScheduleType.business_hours,
                                                                      schedule_id=self.sched_id)
            finally:
                if self.aa_tn:
                    print(f'removing TN "{self.aa_tn}" from location "{self.location.name}')
                    self.test.api.telephony.location.number.remove(location_id=self.location.location_id,
                                                                   phone_numbers=[self.aa_tn])


@dataclass
class HGContext:
    """
    An hunt group context to be used for call routing tests with HG as destination
    """
    test: 'TestHostedFeature'
    location: Location
    hg_name: str = field(init=False, default=None)
    hg_tn: str = field(init=False, default=None)
    hg_id: str = field(init=False, default=None)
    hg: HuntGroup = field(init=False, default=None)

    def __post_init__(self):
        # create a new hunt group
        with self.test.no_log():
            hg_list = list(self.test.api.telephony.huntgroup.list(name=self.location.name))
            hg_names = set(hg.name for hg in hg_list)
            hg_name = next(name for i in range(1, 99)
                           if (name := f'{self.location.name} {i:02}') not in hg_names)
            self.hg_name = hg_name

            # phone number for HG
            hg_extension = available_extensions(api=self.test.api, location_id=self.location.location_id)[0]
            loc_info = next(li for li in self.test.location_infos
                            if li.location.location_id == self.location.location_id)
            hg_tn = available_tns(api=self.test.api,
                                  tn_prefix=loc_info.main_number[:9])[0]

            # add number to location
            print(f'adding TN "{hg_tn}" to location "{self.location.name}')
            try:
                self.test.api.telephony.location.number.add(location_id=self.location.location_id,
                                                            phone_numbers=[hg_tn],
                                                            state=NumberState.active)
                self.hg_tn = hg_tn

                # create huntgroup
                hg = HuntGroup.create(
                    name=hg_name,
                    extension=hg_extension,
                    phone_number=hg_tn)
                print(f'Creating hunt group "{hg_name}" in location "{self.location.name}"')
                hg_id = self.test.api.telephony.huntgroup.create(
                    location_id=self.location.location_id,
                    settings=hg)
                hg.id = hg_id
                self.hg = hg
            except:
                self.clean_up()

    def clean_up(self):
        """
        Try to remove all stuff again
        :return:
        """
        try:
            if self.hg:
                print(f'Deleting hunt group "{self.hg_name}" in location "{self.location.name}"')
                self.test.api.telephony.huntgroup.delete_huntgroup(location_id=self.location.location_id,
                                                                   huntgroup_id=self.hg.id)
        finally:
            if self.hg_tn:
                print(f'removing TN "{self.hg_tn}" from location "{self.location.name}')
                self.test.api.telephony.location.number.remove(location_id=self.location.location_id,
                                                               phone_numbers=[self.hg_tn])


@dataclass(init=False)
class TestHostedFeature(TestCallRouting):
    """
    Call routing tests for calls to hosted features
    """
    aa_context: ClassVar[AAContext] = field(default=None)
    hg_context: ClassVar[HGContext] = field(default=None)
    _target_user: ClassVar[Person] = field(default=None)

    @classmethod
    def tearDownClass(cls) -> None:
        error = None
        if cls.aa_context:
            try:
                cls.aa_context.clean_up()
            except Exception as e:
                error = error or e
        if cls.hg_context:
            try:
                cls.hg_context.clean_up()
            except Exception as e:
                error = error or e
        if error:
            raise error

    @property
    def target_user(self) -> Person:
        if self._target_user is None:
            self.__class__._target_user = choice(self.calling_users)
        return self._target_user

    def get_auto_attendant(self, *, location: Location) -> AutoAttendant:
        """
        Get an auto attendant for AA tests. AA gets created if needed.
        Clean-up happens during test Clean-Up
        """
        if not self.aa_context:
            self.__class__.aa_context = AAContext(test=self, location=location)
        return self.aa_context.auto_attendant

    def get_hunt_group(self, *, location: Location) -> HuntGroup:
        """
        Get a hunt group for HG tests. HG gets created if needed.
        Clean-up happens during test Clean-Up
        """
        if not self.hg_context:
            self.__class__.hg_context = HGContext(test=self, location=location)
        return self.hg_context.hg

    def assert_result_wrong_service_instance_id_format(self, *, expected: TestCallRoutingResult,
                                                       result: TestCallRoutingResult):
        try:
            self.assertEqual(expected, result)
        except AssertionError:
            if result.hosted_feature.service_instance_id != expected.hosted_feature.service_instance_id:
                # TODO: defect, wrong ID format. Service instance is Broadsoft id
                print('=' * 80)
                print('Wrong service instance id format (Broadsoft id)')
                expected_id = base64.b64decode(expected.hosted_feature.service_instance_id + "==").decode()
                print(f'Expected service instance id:'
                      f' {expected_id}')
                print(f'Trailing end of expected service instance id: '
                      f'{base64.b64decode(expected_id.split("/")[-1]+"==").decode()}')
                print(f'Actual service instance id:'
                      f' {base64.b64decode(result.hosted_feature.service_instance_id + "==").decode()}')

            # check whether there is anything else wrong (other than the service instance id)
            result.hosted_feature.service_instance_id = expected.hosted_feature.service_instance_id
            try:
                self.assertEqual(expected, result)
            except AssertionError:
                raise
            else:
                print('No other issues other than wrong service instance id format')
                # raise initial error
                raise

    @staticmethod
    def result_service_by_phone_numer(*, service: Union[AutoAttendant, HuntGroup],
                                      location: Location) -> TestCallRoutingResult:
        if isinstance(service, AutoAttendant):
            service_type = ServiceType.auto_attendant
            service_instance_id = service.auto_attendant_id
        elif isinstance(service, HuntGroup):
            service_type = ServiceType.hunt_group
            service_instance_id = service.id
        else:
            raise ValueError(f"Wrong service type: {service.__class__.__name__}")

        return TestCallRoutingResult(destination_type=DestinationType.hosted_feature,
                                     routing_address=service.phone_number,
                                     is_rejected=False,
                                     hosted_feature=HostedFeatureDestination(
                                         location_name=location.name,
                                         location_id=location.location_id,
                                         phone_number=service.phone_number,
                                         extension=service.extension,
                                         service_type=service_type,
                                         service_type1=service_type,
                                         service_name=service.name,
                                         name=service.name,
                                         service_instance_id=service_instance_id))

    def test_001_user_to_aa_same_location_by_extension(self):
        """
        user calls AA in same location by extension
        """
        user = self.target_user

        # get location
        location = next(loc for loc in self.locations
                        if loc.location_id == user.location_id)
        # get AA in location
        aa = self.get_auto_attendant(location=location)
        result = self.api.telephony.test_call_routing(originator_id=user.person_id,
                                                      originator_type=OriginatorType.user,
                                                      destination=aa.extension)
        self.print_result(result=result)
        # apparently the service instance ID seems to be wrong?
        expected = TestCallRoutingResult(destination_type=DestinationType.hosted_feature,
                                         routing_address=aa.extension,
                                         is_rejected=False,
                                         hosted_feature=HostedFeatureDestination(
                                             location_name=location.name,
                                             location_id=location.location_id,
                                             phone_number=aa.phone_number,
                                             extension=aa.extension,
                                             service_type=ServiceType.auto_attendant,
                                             service_type1=ServiceType.auto_attendant,
                                             service_name=aa.name,
                                             name=aa.name,
                                             service_instance_id=aa.auto_attendant_id))

        self.assert_result_wrong_service_instance_id_format(expected=expected, result=result)

    def test_002_user_to_aa_same_location_by_tn(self):
        """
        user calls AA in same location by +E.164 TN
        """
        user = self.target_user

        # get location
        location = next(loc for loc in self.locations
                        if loc.location_id == user.location_id)
        # get AA in location
        aa = self.get_auto_attendant(location=location)
        result = self.api.telephony.test_call_routing(originator_id=user.person_id,
                                                      originator_type=OriginatorType.user,
                                                      destination=aa.phone_number)
        self.print_result(result=result)
        expected = self.result_service_by_phone_numer(service=aa, location=location)
        self.assert_result_wrong_service_instance_id_format(expected=expected, result=result)

    def test_003_user_to_aa_same_location_10d(self):
        """
        user calls AA in same location by 10D
        """
        user = self.target_user

        # get location
        location = next(loc for loc in self.locations
                        if loc.location_id == user.location_id)
        # get AA in location
        aa = self.get_auto_attendant(location=location)
        result = self.api.telephony.test_call_routing(originator_id=user.person_id,
                                                      originator_type=OriginatorType.user,
                                                      destination=aa.phone_number[2:])
        self.print_result(result=result)
        expected = self.result_service_by_phone_numer(service=aa, location=location)
        self.assert_result_wrong_service_instance_id_format(expected=expected, result=result)

    def test_004_user_to_aa_same_location_9_10d(self):
        """
        user calls AA in same location by 9+10D
        """
        user = self.target_user

        # get location
        location = next(loc for loc in self.locations
                        if loc.location_id == user.location_id)
        # get AA in location
        aa = self.get_auto_attendant(location=location)
        result = self.api.telephony.test_call_routing(originator_id=user.person_id,
                                                      originator_type=OriginatorType.user,
                                                      destination=f'9{aa.phone_number[2:]}')
        self.print_result(result=result)
        expected = self.result_service_by_phone_numer(service=aa, location=location)
        self.assert_result_wrong_service_instance_id_format(expected=expected, result=result)

    def test_005_user_to_hg_same_location_by_extension(self):
        """
        user calls HG in same location by extension
        """
        user = self.target_user

        # get location
        location = next(loc for loc in self.locations
                        if loc.location_id == user.location_id)
        # get HG in location
        hg = self.get_hunt_group(location=location)
        result = self.api.telephony.test_call_routing(originator_id=user.person_id,
                                                      originator_type=OriginatorType.user,
                                                      destination=hg.extension)
        self.print_result(result=result)
        # apparently the service instance ID seems to be wrong?
        expected = TestCallRoutingResult(destination_type=DestinationType.hosted_feature,
                                         routing_address=hg.extension,
                                         is_rejected=False,
                                         hosted_feature=HostedFeatureDestination(
                                             location_name=location.name,
                                             location_id=location.location_id,
                                             phone_number=hg.phone_number,
                                             extension=hg.extension,
                                             service_type=ServiceType.hunt_group,
                                             service_type1=ServiceType.hunt_group,
                                             service_name=hg.name,
                                             name=hg.name,
                                             service_instance_id=hg.id))

        self.assert_result_wrong_service_instance_id_format(expected=expected, result=result)


    def test_005_user_to_hg_same_location_by_tn(self):
        """
        user calls HG in same location by +E.164 TN
        """
        user = self.target_user

        # get location
        location = next(loc for loc in self.locations
                        if loc.location_id == user.location_id)
        # get hg in location
        hg = self.get_hunt_group(location=location)
        result = self.api.telephony.test_call_routing(originator_id=user.person_id,
                                                      originator_type=OriginatorType.user,
                                                      destination=hg.phone_number)
        self.print_result(result=result)
        expected = self.result_service_by_phone_numer(service=hg, location=location)
        self.assert_result_wrong_service_instance_id_format(expected=expected, result=result)
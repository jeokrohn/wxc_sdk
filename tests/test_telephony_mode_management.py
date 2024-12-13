"""
Mode management tests for:
* Call Queues
* Auto Attendants
* Hunt Groups
* Personal settings
"""
import asyncio
import json
import random
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import timedelta
from itertools import chain
from typing import ClassVar, Callable
from zoneinfo import ZoneInfo

from future.backports.datetime import datetime

from tests.base import TestCaseWithLog, TestWithLocations, async_test
from tests.testutil import available_extensions_gen, create_simple_call_queue, create_operating_mode, new_aa_names, \
    new_operating_mode_names
from wxc_sdk.as_api import AsForwardingApi
from wxc_sdk.common.schedules import Schedule, ScheduleType, ScheduleLevel
from wxc_sdk.locations import Location
from wxc_sdk.person_settings.forwarding import CallForwardingCommon
from wxc_sdk.rest import RestError
from wxc_sdk.telephony.autoattendant import AutoAttendant
from wxc_sdk.telephony.callqueue import CallQueue
from wxc_sdk.telephony.forwarding import (ForwardingApi, ForwardOperatingModes, ModeForward, ModeForwardTo,
                                          ForwardToSelection, CallForwarding, ForwardingSetting)
from wxc_sdk.telephony.huntgroup import HuntGroup
from wxc_sdk.telephony.location import TelephonyLocation
from wxc_sdk.telephony.operating_modes import OperatingMode, OperatingModeSchedule, SameHoursDaily, DaySchedule


@dataclass(init=False, repr=False)
class TestModeManagement(TestCaseWithLog):
    """
    Mode Management tests for Call Queues, Auto Attendants, and Hunt Groups
    """
    fwd_api: ClassVar[ForwardingApi] = None
    target: ClassVar[CallQueue] = None
    operating_modes: ClassVar[list[OperatingMode]] = []

    @classmethod
    def tearDownClass(cls):
        for om in cls.operating_modes:
            try:
                cls.api.telephony.operating_modes.delete(om.id)
                print(f'deleted operating mode "{om.name}" in tearDownClass')
            except RestError as e:
                print(f'Error deleting operating mode {om.name}: {e}')
        super().tearDownClass()

    @property
    def target_id(self):
        return self.id_for_entity(self.target)

    @staticmethod
    def id_for_entity(entity):
        return {'location_id': entity.location_id,
                'feature_id': entity.id}

    def list(self):
        raise NotImplementedError('Abstract method')

    def setUp(self) -> None:
        if self.__class__ == TestModeManagement:
            self.skipTest('Abstract test class')
        super().setUp()

    def create_operating_mode(self) -> OperatingMode:
        """
        Create an operating mode and collect it for later deletion
        """
        om = create_operating_mode(self.api)
        self.operating_modes.append(om)
        return om

    def test_001_get_settings(self):
        """
        Get call forwarding settings
        """
        settings = self.fwd_api.settings(**self.target_id)
        print(json.dumps(json.loads(settings.model_dump_json()), indent=2))

    def test_002_switch_mode_for_call_forwarding(self):
        """
        switch mode for call forwarding
        """
        # enable target for mode based forwarding
        self.assert_target_has_operating_mode_forwarding()
        self.fwd_api.switch_mode_for_call_forwarding(**self.target_id)

    def test_003_get_all_settings(self):
        """
        get settings for all entities
        """
        entities = list(self.list())
        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda e: self.fwd_api.settings(**self.id_for_entity(e)),
                                     entities))
        for entity, setting in zip(entities, settings):
            if not (setting.operating_modes and setting.operating_modes.modes):
                continue
            print(f'{entity.name}')
            print(json.dumps(setting.model_dump(mode='json', by_alias=True, exclude_none=True),
                             indent=2))
            print()

    def assert_target_has_operating_mode_forwarding(self):
        """
        assert that the target entity has an operating mode for call forwarding
        """
        fwd_settings = self.fwd_api.settings(**self.target_id)
        if not fwd_settings.operating_modes.modes:
            om = self.create_operating_mode()
            self.fwd_api.update(forwarding=CallForwarding(operating_modes=ForwardOperatingModes(
                enabled=True,
                modes=[ModeForward(normal_operation_enabled=True,
                                   id=om.id,
                                   forward_to=ModeForwardTo(selection=ForwardToSelection.default_number))])),
                **self.target_id)
            print(f'enabled operating mode forwarding for {self.target.name}')

    def test_enable_om_forwarding(self):
        # create operating mode
        operating_mode = self.create_operating_mode()

        # assign operating mode to the queue
        fwd_settings = self.fwd_api.settings(**self.target_id)
        try:

            update = CallForwarding(operating_modes=ForwardOperatingModes(
                enabled=True,
                modes=[ModeForward(normal_operation_enabled=True,
                                   id=operating_mode.id,
                                   forward_to=ModeForwardTo(selection=ForwardToSelection.default_number))]),
                always=ForwardingSetting(enabled=False),
                selective=ForwardingSetting(enabled=False))

            self.fwd_api.update(forwarding=update, **self.target_id)
            after = self.fwd_api.settings(**self.target_id)
            self.assertIsNotNone(after.operating_modes)
            self.assertTrue(after.operating_modes and after.operating_modes.enabled,
                            'operating modes not enabled')
            self.assertEqual(1, len(after.operating_modes.modes))
            self.assertEqual(operating_mode.id, after.operating_modes.modes[0].id,
                             'mode id does not match')
        finally:
            # restore forwarding settings
            self.fwd_api.update(forwarding=fwd_settings, **self.target_id)

    @contextmanager
    def two_modes_with_schedules(self):
        """
        create two modes with schedules and return the mode ids
        :return:
        """
        timezone = self.target.time_zone
        zoneinfo = ZoneInfo(timezone)
        now: datetime = datetime.now(zoneinfo) + timedelta(minutes=5)

        # create two modes with schedules
        #  * mode 1 is active from tight after now for 3 hours
        #  * mode 2 is active for the rest of the day
        mode1_from = (now.hour + 1) % 24
        mode1_to = (mode1_from + 3) % 24
        mode1_schedule = DaySchedule(enabled=True,
                                     start_time=f'{mode1_from:02}:00',
                                     end_time=f'{mode1_to:02}:00')
        mode2_from = mode1_to
        mode2_to = mode1_from
        mode2_schedule = DaySchedule(enabled=True,
                                     start_time=f'{mode2_from:02}:00',
                                     end_time=f'{mode2_to:02}:00')
        mode_names = new_operating_mode_names(api=self.api)

        # modes to create
        modes = [OperatingMode(name=next(mode_names), type=OperatingModeSchedule.same_hours_daily,
                               level=ScheduleLevel.organization,
                               same_hours_daily=SameHoursDaily(
                                   monday_to_friday=mode1_schedule,
                                   saturday_to_sunday=mode1_schedule),
                               call_forwarding=CallForwardingCommon(enabled=False)),
                 OperatingMode(name=next(mode_names), type=OperatingModeSchedule.same_hours_daily,
                               level=ScheduleLevel.organization,
                               same_hours_daily=SameHoursDaily(
                                   monday_to_friday=mode2_schedule,
                                   saturday_to_sunday=mode2_schedule),
                               call_forwarding=CallForwardingCommon(enabled=True, destination='+4961007739764'))]

        # create the modes
        with ThreadPoolExecutor() as pool:
            mode_ids = list(pool.map(self.api.telephony.operating_modes.create, modes))
        for id, mode in zip(mode_ids, modes):
            mode.id = id
        # mark modes for cleanup in class cleanup
        self.operating_modes.extend(modes)
        try:
            yield modes
        finally:
            # no cleanup needed as the modes are marked for cleanup in class cleanup
            ...

    def test_expected_mode(self):
        """
        Add multiple modes with schedules and make sure that the expected mode is active
        """
        with self.two_modes_with_schedules() as modes:
            modes: list[OperatingMode]
            forwarding = self.fwd_api.settings(**self.target_id)
            try:
                update = CallForwarding(
                    operating_modes=ForwardOperatingModes(
                        enabled=True,
                        modes=[ModeForward(normal_operation_enabled=True, id=m.id,
                                           forward_to=ModeForwardTo(
                                               selection=ForwardToSelection.default_number))
                               for m in modes]))
                self.fwd_api.update(forwarding=update, **self.target_id)
                after = self.fwd_api.settings(**self.target_id)
                active_mode = self.api.telephony.operating_modes.details(
                    after.operating_modes.current_operating_mode_id)
                now: datetime = datetime.now(ZoneInfo(self.target.time_zone)) + timedelta(minutes=5)
                print(f'Active mode: {active_mode.name} at {now:%H:%M}')
                print(json.dumps(active_mode.model_dump(mode='json', by_alias=True, exclude_none=True), indent=2))

                # the second mode should be active
                self.assertEqual(modes[1].id, active_mode.id)
            finally:
                # restore forwarding settings
                self.fwd_api.update(forwarding=forwarding, **self.target_id)

    def test_switch_operating_mode_to_normal(self):
        """
        switch operating mode to normal
        """
        ...
        raise NotImplementedError('No way to test as there is is no way to switch to abnormal using the APIs')

    def test_disable_om_forwarding(self):
        """
        disable operating mode forwarding; how do we remove all operating modes from a feature?
        """
        # TODO: implement
        raise NotImplementedError('Not implemented')


class TestQueueModeManagement(TestModeManagement, TestWithLocations):
    """
    Mode Management tests for Call Queues
    """
    # location where we are creating the temp queue for the test
    target_location: ClassVar[Location]

    create_temp_queue: ClassVar[bool] = False

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.fwd_api = cls.api.telephony.callqueue.forwarding

    def list(self):
        return self.api.telephony.callqueue.list()

    @classmethod
    def tearDownClass(cls):
        """
        clean up after tests
        """
        # delete temp queue
        if cls.target and cls.create_temp_queue:
            print(f'Deleting queue: {cls.target.name} in location: {cls.target_location.name}')
            cls.api.telephony.callqueue.delete_queue(cls.target.location_id, cls.target.id)
        super().tearDownClass()

    def assert_target_queue(self):
        """
        create or pick a queue as target for tests
        """
        if self.target:
            return
        if self.create_temp_queue:
            with self.no_log():
                self.__class__.target = create_simple_call_queue(api=self.api,
                                                                 locations=self.telephony_locations,
                                                                 no_log=self.no_log)
            self.__class__.target_location = next(loc
                                                  for loc in self.telephony_locations
                                                  if loc.location_id == self.target.location_id)

        else:
            # pick random queue
            with self.no_log():
                queues = list(self.api.telephony.callqueue.list())
            target = next(queue for queue in queues if queue.name == 'for om tests')
            location_id = target.location_id
            target = self.api.telephony.callqueue.details(target.location_id, target.id)
            target.location_id = location_id
            self.__class__.target = target

        self.__class__.target_location = next(loc
                                              for loc in self.telephony_locations
                                              if loc.location_id == self.target.location_id)
        print(f'{"temp" if self.create_temp_queue else ""} '
              f'target queue: {self.target.name} in location: {self.target_location.name}')

    def setUp(self) -> None:
        super().setUp()
        self.assert_target_queue()


class TestAttendantModeManagement(TestModeManagement, TestWithLocations):
    target: ClassVar[AutoAttendant] = None
    target_location: ClassVar[TelephonyLocation] = None
    schedule: ClassVar[Schedule] = None
    create_temp: ClassVar[bool] = True

    @staticmethod
    def id_for_entity(entity):
        return {'location_id': entity.location_id,
                'feature_id': entity.auto_attendant_id}

    def list(self):
        return self.api.telephony.auto_attendant.list()

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.fwd_api = cls.api.telephony.auto_attendant.forwarding

    @classmethod
    def tearDownClass(cls):
        if cls.target:
            cls.api.telephony.auto_attendant.delete_auto_attendant(location_id=cls.target_location.location_id,
                                                                   auto_attendant_id=cls.target.auto_attendant_id)
            print(f'deleted auto attendant "{cls.target.name}" in location "{cls.target_location.name}"')
        if cls.schedule:
            cls.api.telephony.schedules.delete_schedule(obj_id=cls.target_location.location_id,
                                                        schedule_type=ScheduleType.business_hours,
                                                        schedule_id=cls.schedule.schedule_id)
            print(f'deleted schedule "{cls.schedule.name}" in location "{cls.target_location.name}"')
        super().tearDownClass()

    def setUp(self) -> None:
        super().setUp()
        self.assert_target()

    def assert_temp_schedule(self):
        """
        create a temp schedule to be used for the auto attendant
        """
        if self.schedule:
            return
        with self.no_log():
            names = {s.name for s in self.api.telephony.schedules.list(obj_id=self.target_location.location_id)}
            new_name = next(name for i in range(1, 1000) if (name := f'test_{i:03}') not in names)
            schedule_id = self.api.telephony.schedules.create(obj_id=self.target_location.location_id,
                                                              schedule=Schedule.business(name=new_name))
            target_schedule = self.api.telephony.schedules.details(obj_id=self.target_location.location_id,
                                                                   schedule_type=ScheduleType.business_hours,
                                                                   schedule_id=schedule_id)
            print(f'created schedule "{target_schedule.name}" in location "{self.target_location.name}"')
        self.__class__.schedule = target_schedule

    def temp_auto_attendant_target(self):
        self.__class__.target_location = random.choice(self.telephony_locations)

        # we need a schedule
        self.assert_temp_schedule()

        # get an available name and extension for the new auto attendant
        with self.no_log():
            new_name = next(new_aa_names(api=self.api))
            extension = next(available_extensions_gen(api=self.api, location_id=self.target_location.location_id))

            print(f'creating AA "{new_name}" ({extension}) with schedule "{self.schedule.name}" '
                  f'in location "{self.target_location.name}"...')
            aa_settings = AutoAttendant.create(name=new_name,
                                               business_schedule=self.schedule.name,
                                               extension=extension)
            aa_id = self.api.telephony.auto_attendant.create(location_id=self.target_location.location_id,
                                                             settings=aa_settings)
            aa = self.api.telephony.auto_attendant.details(location_id=self.target_location.location_id,
                                                           auto_attendant_id=aa_id)
            aa.location_id = self.target_location.location_id
            self.__class__.target = aa

    def assert_target(self):
        """
        create or pick an auto attendant as target for tests
        """
        if not self.target:
            if self.create_temp:
                self.temp_auto_attendant_target()
            else:
                self.__class__.target = next(q for q in self.api.telephony.auto_attendant.list(name='aa')
                                             if q.name == 'aa for om tests')
                self.__class__.target_location = next(loc for loc in self.telephony_locations
                                                      if loc.location_id == self.target.location_id)


class HuntGroupModeManagement(TestModeManagement, TestWithLocations):
    """
    Mode Management tests for Call Hunt Groups
    """
    target: ClassVar[HuntGroup] = None

    @staticmethod
    def id_for_entity(entity: HuntGroup):
        return {'location_id': entity.location_id,
                'feature_id': entity.id}

    def list(self):
        return self.api.telephony.huntgroup.list()

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.fwd_api = cls.api.telephony.huntgroup.forwarding

    @classmethod
    def tearDownClass(cls):
        if cls.target:
            cls.api.telephony.huntgroup.delete_huntgroup(location_id=cls.target.location_id,
                                                         huntgroup_id=cls.target.id)
            print(f'deleted hunt group "{cls.target.name}" in location "{cls.target.name}"')
        super().tearDownClass()

    def setUp(self) -> None:
        super().setUp()
        self.assert_target()

    def assert_target(self):
        """
        create or pick a hunt group as target for tests
        """
        if self.target:
            return
        with self.no_log():
            target_location = random.choice(self.telephony_locations)

            hapi = self.api.telephony.huntgroup
            # pick available HG name in location
            hg_names = set(hg.name for hg in hapi.list(location_id=target_location.location_id))
            new_name = next(name for i in range(1000)
                            if (name := f'hg_{i:03}') not in hg_names)
            extension = next(
                available_extensions_gen(api=self.api, location_id=target_location.location_id))

            # settings for new hunt group
            settings = HuntGroup(name=new_name,
                                 extension=extension,
                                 agents=[])

            # creat new hg
            print(f'creating hunt group "{new_name}" ({extension}) in location "{target_location.name}"...')
            new_hg_id = hapi.create(location_id=target_location.location_id,
                                    settings=settings)

            # and get details of new queue using the queue id
            details = hapi.details(location_id=target_location.location_id, huntgroup_id=new_hg_id)
            details.location_id = target_location.location_id
            self.__class__.target = details


class EnableAllFeaturesForModeManagement(TestCaseWithLog):
    """
    Enable all features for mode management with a NOP mode
    """

    @async_test
    async def test_enable_features(self):
        """
        enable all features for mode management
        """
        # create a mode that doesn't impact normal operation of a feature
        mode = OperatingMode(type=OperatingModeSchedule.none_, level=ScheduleLevel.organization,
                             call_forwarding=CallForwardingCommon(enabled=False))
        consider = {'type': True, 'level': True, 'call_forwarding': {'enabled': True}}
        mode_data = mode.model_dump(mode='json', by_alias=True, include=consider)

        # does a mode already exist?
        modes = list(self.api.telephony.operating_modes.list())
        existing = next((om for om in modes
                         if om.model_dump(mode='json', by_alias=True, include=consider) == mode_data), None)
        if existing is None:
            candidates = chain(('NOP',), (f'NOP_{i:03}' for i in range(1, 1000)))
            new_name = next(name for name in candidates if name not in {om.name for om in modes})
            mode.name = new_name
            mode_id = self.api.telephony.operating_modes.create(mode)
        else:
            mode_id = existing.id

        # enable the mode for all features

        async def enable_for_one_feature_type(*, list_method: Callable, key: Callable, fwd_api: AsForwardingApi):
            """
            Enable mode based formating for all features of a given type
            """
            # list features
            features = await list_method()
            if not features:
                return
            feature_class = features[0].__class__.__name__

            # get forwarding settings for each feature
            forwarding_settings = await asyncio.gather(
                *[fwd_api.settings(*key(f))
                  for f in features])
            forwarding_settings: list[CallForwarding]

            # if no forwarding is enabled then enable mode based formating
            features_to_enable = [f for f, fs in zip(features, forwarding_settings)
                                  if (not fs.always.enabled and not fs.selective.enabled and
                                      (not fs.operating_modes or not fs.operating_modes.modes))]
            if not features_to_enable:
                return
            update = CallForwarding(
                operating_modes=ForwardOperatingModes(
                    enabled=True,
                    modes=[ModeForward(
                        normal_operation_enabled=True,
                        id=mode_id,
                        forward_to=ModeForwardTo(
                            selection=ForwardToSelection.default_number))]))
            print(f'Enabling mode based forwarding for {len(features_to_enable)} '
                  f'{feature_class}s: {", ".join(f.name for f in features_to_enable)}')
            await asyncio.gather(*[fwd_api.update(*key(f), forwarding=update) for f in features_to_enable])

        await asyncio.gather(enable_for_one_feature_type(list_method=self.async_api.telephony.callqueue.list,
                                                         key=lambda q: (q.location_id, q.id),
                                                         fwd_api=self.async_api.telephony.callqueue.forwarding),
                             enable_for_one_feature_type(list_method=self.async_api.telephony.auto_attendant.list,
                                                         key=lambda a: (a.location_id, a.auto_attendant_id),
                                                         fwd_api=self.async_api.telephony.auto_attendant.forwarding),
                             enable_for_one_feature_type(list_method=self.async_api.telephony.huntgroup.list,
                                                         key=lambda h: (h.location_id, h.id),
                                                         fwd_api=self.async_api.telephony.huntgroup.forwarding))

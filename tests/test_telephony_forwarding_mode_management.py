"""
Mode management tests for:
* Call Queues
* Auto Attendants
* Hunt Groups
* Personal settings
"""
import json
import random
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from typing import ClassVar

from tests.base import TestCaseWithLog, TestWithLocations
from tests.testutil import available_extensions_gen, create_simple_call_queue, create_operating_mode, new_aa_names
from wxc_sdk.common.schedules import Schedule, ScheduleType
from wxc_sdk.locations import Location
from wxc_sdk.rest import RestError
from wxc_sdk.telephony.autoattendant import AutoAttendant
from wxc_sdk.telephony.callqueue import CallQueue
from wxc_sdk.telephony.forwarding import (ForwardingApi, ForwardOperatingModes, ModeForward, ModeForwardTo,
                                          ForwardToSelection, CallForwarding, ForwardingSetting)
from wxc_sdk.telephony.huntgroup import HuntGroup
from wxc_sdk.telephony.location import TelephonyLocation
from wxc_sdk.telephony.operating_modes import OperatingMode


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

    def test_disable_om_forwarding(self):
        """
        disable operating mode forwarding; how do we remove an operating mode from a feature?
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
            self.__class__.target = target

        self.__class__.target_location = next(loc
                                              for loc in self.telephony_locations
                                              if loc.location_id == self.target.location_id)
        print(f'{"temp" if self.create_temp_queue else ""} '
              f'target queue: {self.target.name} in location: {self.target_location.name}')

    def setUp(self) -> None:
        super().setUp()
        self.assert_target_queue()

    def test_001_get_settings(self):
        super().test_001_get_settings()

    def test_002_switch_mode_for_call_forwarding(self):
        super().test_002_switch_mode_for_call_forwarding()

    def test_003_get_all_settings(self):
        super().test_003_get_all_settings()

    def test_enable_om_forwarding(self):
        super().test_enable_om_forwarding()


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

    def test_002_switch_mode_for_call_forwarding(self):
        super().test_002_switch_mode_for_call_forwarding()

    def test_enable_om_forwarding(self):
        super().test_enable_om_forwarding()


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

# TODO: Personal settings mode management tests

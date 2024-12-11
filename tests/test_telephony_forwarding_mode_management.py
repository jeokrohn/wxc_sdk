"""
Mode management tests for:
* Call Queues
* Auto Attendants
* Hunt Groups
* Personal settings
"""
import json
import random
from dataclasses import dataclass
from typing import ClassVar

from tests.base import TestCaseWithLog, TestWithLocations
from tests.testutil import available_extensions_gen, create_simple_call_queue
from wxc_sdk.locations import Location
from wxc_sdk.telephony.autoattendant import AutoAttendant
from wxc_sdk.telephony.callqueue import CallQueue, CallQueueCallPolicies, QueueSettings
from wxc_sdk.telephony.forwarding import ForwardingApi
from wxc_sdk.telephony.hg_and_cq import CallingLineIdPolicy


@dataclass(init=False, repr=False)
class TestModeManagement(TestCaseWithLog):
    """
    Mode Management tests for Call Queues, Auto Attendants, and Hunt Groups
    """
    fwd_api: ClassVar[ForwardingApi] = None
    target: ClassVar[CallQueue] = None

    @property
    def target_id(self):
        return {'location_id': self.target.location_id,
                'feature_id': self.target.id}

    def setUp(self) -> None:
        if self.__class__ == TestModeManagement:
            self.skipTest('Abstract test class')
        super().setUp()

    def test_001_get_settings(self):
        """
        Get call forwarding settings
        """
        settings = self.fwd_api.settings(**self.target_id)
        print(json.dumps(json.loads(settings.model_dump_json()), indent=2))

    def test_002_switch_mode_for_call_forwarding(self):
        self.fwd_api.switch_mode_for_call_forwarding(**self.target_id)


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
            self.__class__.target = random.choice(queues)

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


class TestAttendantModeManagement(TestModeManagement):
    target: ClassVar[AutoAttendant] = None

    @property
    def target_id(self):
        return {'location_id': self.target.location_id,
                'feature_id': self.target.auto_attendant_id}

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.fwd_api = cls.api.telephony.auto_attendant.forwarding

    def setUp(self) -> None:
        super().setUp()
        self.assert_target()

    def assert_target(self):
        if not self.target:
            self.__class__.target = next(q for q in self.api.telephony.auto_attendant.list(name='aa') if q.name == 'aa')

    def test_002_switch_mode_for_call_forwarding(self):
        super().test_002_switch_mode_for_call_forwarding()

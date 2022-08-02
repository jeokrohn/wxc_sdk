from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from random import choice
from typing import ClassVar

from tests.base import TestCaseWithLog
from wxc_sdk.common import RouteIdentity, RouteType
from wxc_sdk.locations import Location
from wxc_sdk.telephony.location.internal_dialing import InternalDialing


@dataclass(init=False)
class TestInternalDialing(TestCaseWithLog):
    locations: ClassVar[list[Location]]
    _settings: list[InternalDialing] = field(default=None)
    _route_choices: list[RouteIdentity] = field(default=None)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.locations = list(cls.api.locations.list())

    def read_all_settings(self) -> dict[str, InternalDialing]:
        """
        Read settings for all locations
        """
        with ThreadPoolExecutor() as pool:
            settings = dict(
                pool.map(lambda l: (l.location_id,
                                    self.api.telephony.location.internal_dialing.read(
                                        location_id=l.location_id)),
                         self.locations))
        return settings

    @property
    def settings(self) -> dict[str, InternalDialing]:
        if self._settings is None:
            self._settings = self.read_all_settings()
        return self._settings

    @property
    def route_choices(self) -> list[RouteIdentity]:
        if self._route_choices is None:
            self._route_choices = list(self.api.telephony.route_choices())
        return self._route_choices

    def test_001_read_all(self):
        """
        read settings for all locations
        """
        with ThreadPoolExecutor() as pool:
            self.read_all_settings()
        print(f'Got internal dialing settings for {len(self.locations)} locations')

    @contextmanager
    def update_context(self, *, location: Location):
        before = self.settings[location.location_id]
        api = self.api.telephony.location.internal_dialing
        try:
            yield before
        finally:
            api.update(location_id=location.location_id,
                       update=before)
            after = api.read(location_id=location.location_id)
            self.assertEqual(before, after)

    def test_001_modify_trunk(self):
        """
        set route choice to trunk
        """
        # TODO: implement as soon as we can determine which trunks are in India
        # pick a trunk
        self.skipTest('revisit when we can avoid India trunks')
        trunks = [c for c in self.route_choices
                  if c.route_type == RouteType.trunk]
        if not trunks:
            self.skipTest('Need at least trunk to run this test')
        trunk = choice(trunks)

        # pick a location (don't pick India locations to avoid toll bypass hassle)
        locations = [l for l in self.locations if l.address.country != 'IN']
        location = choice(self.locations)
        api = self.api.telephony.location.internal_dialing
        with self.update_context(location=location):
            print(f'Location: {location.name}, trunk: {trunk.name}')
            settings = InternalDialing(enable_unknown_extension_route_policy=True,
                                       unknown_extension_route_identity=RouteIdentity(route_id=trunk.route_id,
                                                                                      route_type=RouteType.trunk))
            api.update(location_id=location.location_id, update=settings)
            after = api.read(location_id=location.location_id)
            settings.unknown_extension_route_identity.name = trunk.name
            self.assertEqual(settings, after)

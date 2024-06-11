from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from random import choice

from tests.base import TestWithLocations
from wxc_sdk.common import RouteIdentity, RouteType
from wxc_sdk.locations import Location
from wxc_sdk.telephony.location.internal_dialing import InternalDialing
from wxc_sdk.telephony.prem_pstn.trunk import TrunkDetail


@dataclass(init=False)
class TestInternalDialing(TestWithLocations):
    _settings: list[InternalDialing] = field(default=None)
    _route_choices: list[RouteIdentity] = field(default=None)

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
        set route choice for internal dialing in one location to trunk
        """
        # only look at trunk route choices
        trunks = [c for c in self.route_choices
                  if c.route_type == RouteType.trunk]

        def get_trunk_details(trunk_ids: Iterable[str]) -> list[TrunkDetail]:
            with ThreadPoolExecutor() as pool:
                return list(pool.map(lambda tid: self.api.telephony.prem_pstn.trunk.details(trunk_id=tid),
                                     trunk_ids))

        india_location_ids = set(loc.location_id for loc in self.locations
                                 if loc.address.country == 'IN')
        if india_location_ids:
            # filter out trunks in india locations
            # need to get trunk details so that we can take a look at the location id of the trunk
            trunk_details = get_trunk_details(trunk.route_id for trunk in trunks)

            detail: TrunkDetail
            trunk: RouteIdentity
            trunks = [trunk for trunk, detail in zip(trunks, trunk_details)
                      if detail.location.id not in india_location_ids]
        if not trunks:
            self.skipTest('Need at least trunk not in India to run this test')

        # pick a trunk
        trunk = choice(trunks)

        # pick a location (don't pick India locations to avoid toll bypass hassle)
        locations = [loc for loc in self.locations if loc.address.country != 'IN']
        location = choice(locations)
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

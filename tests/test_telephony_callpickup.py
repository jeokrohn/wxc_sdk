# TODO: implement further test cases
import asyncio
from itertools import chain

from tests.base import async_test, TestWithLocations
from wxc_sdk.telephony.callpickup import CallPickup


class TestDetails(TestWithLocations):
    @async_test
    async def test_all_details(self):
        """
        get details for all call pickups
        """
        locations = self.locations
        # get call pickups for all locations
        pickups = list(chain.from_iterable(
            await asyncio.gather(*[self.async_api.telephony.pickup.list(location_id=loc.location_id)
                                   for loc in locations])))
        pickups: list[CallPickup]
        if not pickups:
            self.skipTest('No existing call pickups')
        details = await asyncio.gather(*[self.async_api.telephony.pickup.details(location_id=cp.location_id,
                                                                                 pickup_id=cp.pickup_id)
                                         for cp in pickups])
        print(f'Got details for {len(details)} call pickups')

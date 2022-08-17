import asyncio

from tests.base import TestCaseWithLog, async_test
from tests.testutil import us_location_info, as_available_tns
from wxc_sdk.as_api import AsWebexSimpleApi


class TestNewTNs(TestCaseWithLog):
    """
    Try to get available TNs for each US Location
    """

    @async_test
    async def test_001_tns_for_us_locations(self):
        TNS_TO_REQUEST = 10

        us_locations = us_location_info(api=self.api)
        if not us_locations:
            self.skipTest('No US locations with main number found')
        async with AsWebexSimpleApi(tokens=self.api.access_token) as as_api:
            new_tns = await asyncio.gather(*[as_available_tns(as_api=as_api,
                                                              tn_prefix=loc.main_number[:5],
                                                              tns_requested=TNS_TO_REQUEST)
                                             for loc in us_locations])

        # check that we got the expected numbers of TNs for each location
        self.assertTrue(all(len(new_tn) == TNS_TO_REQUEST for new_tn in new_tns))

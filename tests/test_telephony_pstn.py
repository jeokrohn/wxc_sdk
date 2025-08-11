import asyncio
from dataclasses import dataclass
from typing import ClassVar

from tests.base import TestWithLocations, async_test, WithIntegrationTokens
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.telephony.pstn import PSTNServiceType


class TestPSTN(TestWithLocations):

    def check_errors(self, results):
        err = None
        for location, result in zip(self.telephony_locations, results):
            if isinstance(result, Exception):
                err = err or result
                print(f'Error for location "{location.name}": {result}')
        if err:
            raise err
        return

    @async_test
    async def test_list(self):
        """
        list PSTN options for all locations
        """
        pstn_options_list = await asyncio.gather(*[self.async_api.telephony.pstn.list(location_id=loc.location_id)
                                                   for loc in self.telephony_locations],
                                                 return_exceptions=True)
        self.check_errors(pstn_options_list)


    @async_test
    async def test_list_mobile(self):
        pstn_options_list = await asyncio.gather(*[self.async_api.telephony.pstn.list(location_id=loc.location_id,
                                                                                      service_types=[PSTNServiceType.mobile_numbers])
                                                   for loc in self.telephony_locations],
                                                 return_exceptions=True)
        self.check_errors(pstn_options_list)

    @async_test
    async def test_read(self):
        """
        Read PSTN selection for all locations
        """
        pstn_selections = await asyncio.gather(*[self.async_api.telephony.pstn.read(location_id=loc.location_id)
                                                for loc in self.telephony_locations],
                                               return_exceptions=True)
        self.check_errors(pstn_selections)

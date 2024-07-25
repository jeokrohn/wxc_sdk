import asyncio
from dataclasses import dataclass
from typing import ClassVar

from tests.base import TestWithLocations, async_test, WithIntegrationTokens
from wxc_sdk.as_api import AsWebexSimpleApi


class TestPSTN(TestWithLocations, WithIntegrationTokens):

    @async_test
    async def test_list(self):
        """
        list PSTN options for all locations
        """
        # token = 'MDljMDgxZjItZWNjYS00YTQ1LWI0YjItMWQ1ODZjYjI3YjNlYzY5YzMzZTItMDk5_P0A1_36818b6f-ef07-43d1-b76f-ced79ab2e3e7'
        token = self.integration_tokens.access_token
        async with AsWebexSimpleApi(tokens=token) as int_api:
            pstn_options_list = await asyncio.gather(*[int_api.telephony.pstn.list(location_id=loc.location_id)
                                                       for loc in self.locations], return_exceptions=True)
        foo = 1

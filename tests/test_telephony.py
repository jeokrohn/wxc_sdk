import asyncio
import json

from pydantic import TypeAdapter

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.telephony import CountryConfig


class TestTelephony(TestCaseWithLog):
    @async_test
    async def test_get_country_configuration(self):
        country_codes = ['US', 'DE', 'FR', 'NL']
        results = await asyncio.gather(
            *[self.async_api.telephony.get_country_configuration(country_code=cc) for cc in country_codes]
        )
        print(
            json.dumps(
                TypeAdapter(list[CountryConfig]).dump_python(results, mode='json', by_alias=True, exclude_none=True),
                indent=2,
            )
        )

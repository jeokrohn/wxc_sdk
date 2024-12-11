import asyncio
import json

from pydantic import TypeAdapter

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.telephony.operating_modes import OperatingMode


class TestOperatingModes(TestCaseWithLog):
    def test_list(self):
        """
        list all operating modes
        """
        modes = list(self.api.telephony.operating_modes.list())
        print(json.dumps(TypeAdapter(list[OperatingMode]).dump_python(modes, mode='json', by_alias=True),
                         indent=2))

    @async_test
    async def test_details(self):
        """
        get details for all operating modes
        """
        modes = list(self.api.telephony.operating_modes.list())
        details = await asyncio.gather(*[self.async_api.telephony.operating_modes.details(mode_id=m.id)
                                         for m in modes])
        print(json.dumps(TypeAdapter(list[OperatingMode]).dump_python(details, mode='json', by_alias=True),
                         indent=2))

    # TODO: create teste
    #   * create org level operating modes
    #   * create location level operating modes
    #   * create operating mode holiday
    #   * create operating mode schedule

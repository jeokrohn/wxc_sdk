"""
Generic helper for test cases
"""
import asyncio
from collections import defaultdict
from dataclasses import dataclass
from itertools import zip_longest

from wxc_sdk import WebexSimpleApi
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.locations import Location
from wxc_sdk.telephony import NumberType, NumberListPhoneNumber

__all__ = ['as_available_tns', 'available_tns', 'LocationInfo', 'us_location_info']


async def as_available_tns(*, as_api: AsWebexSimpleApi, tn_prefix: str, tns_requested: int = 1):
    """
    Get some available US TNs
    :param as_api:
    :param ci_org_id:
    :param tn_prefix: prefix for TNs to find. Can be +E.164 or 1st few digits of 10D. If an NPA is passed as 3D or
        +1-3D then numbers in the +1 NXX 555 01XX range are searched
    :param tns_requested: number of TNs to find
    :return:
    """

    # convert prefix to +E.164 prefix
    if not tn_prefix.startswith('+'):
        tn_prefix = f'+1{tn_prefix}'
    if len(tn_prefix) == 5:
        # we only got an NPA make sure to only look at NXX 555 01XX
        tn_prefix = f'{tn_prefix}55501'
    digits_to_fill = 12 - len(tn_prefix)
    numbers_to_scan = 10 ** digits_to_fill

    # generator for numbers to scan for availability
    scan = (f'{tn_prefix}{i:0{digits_to_fill}}' for i in range(numbers_to_scan))
    tns = []

    # the check for availability should operate on batches of at least 5 TNs
    # last batch is filled with None at the end
    batches = zip_longest(*([scan] * max(5, tns_requested)), fillvalue=None)
    for batch in batches:
        # ignore the fill values (in the last batch)
        batch = [number for number in batch if number]
        validation = await as_api.telephony.validate_phone_numbers(phone_numbers=batch)
        if validation.ok:
            # all numbers are available
            failed = set()
        else:
            # get set of numbers which are not available for provisioning
            failed = set(result.phone_number for result in validation.phone_numbers
                         if not result.ok)
        # add available numbers in batch to list of TNs
        tns.extend(number for number in batch if number not in failed)
        if len(tns) >= tns_requested:
            # we are done
            break
    # don't return more TNs than requested
    return tns[:tns_requested]


def available_tns(*, api: WebexSimpleApi, tn_prefix: str, tns_requested: int = 1) -> list[str]:
    """
    Get some available US TNs
    :param api:
    :param tn_prefix: prefix for TNs to find. Can be +E.164 or 1st few digits of 10D. If an NPA is passed as 3D or
        +1-3D then numbers in the +1 NXX 555 01XX range are searched
    :param tns_requested: number of TNs to find
    :return:
    """

    async def as_run():
        async with AsWebexSimpleApi(tokens=api.access_token) as as_api:
            result = await as_available_tns(as_api=as_api, tn_prefix=tn_prefix, tns_requested=tns_requested)
        return result

    return asyncio.run(as_run())


@dataclass
class LocationInfo:
    location: Location
    main_number: str
    numbers: list[NumberListPhoneNumber]

    def available_tns(self, *, api: WebexSimpleApi, tns_requested: int = 1) -> list[str]:
        return available_tns(api=api, tn_prefix=self.main_number[:5], tns_requested=tns_requested)


def us_location_info(*, api: WebexSimpleApi) -> list[LocationInfo]:
    """
    Get information about US location with numbers
    :param apI:
    """
    us_locations = [loc for loc in api.locations.list()
                    if loc.address.country == 'US']
    numbers = list(api.telephony.phone_numbers(number_type=NumberType.number))
    # group numbers by location id
    numbers_by_location: dict[str, list[NumberListPhoneNumber]] = defaultdict(list)
    for number in numbers:
        numbers_by_location[number.location.location_id].append(number)
    # collect results
    result = []
    for loc in us_locations:
        # ger numbers for this location; maybe there are none
        loc_numbers = numbers_by_location.get(loc.location_id)
        if loc_numbers is None:
            # skip locations w/o numbers
            continue

        # determine main number of location
        main_number = next((n for n in loc_numbers
                            if n.main_number), None)
        if not main_number:
            # skip locations w/o main number
            continue
        result.append(LocationInfo(location=loc, main_number=main_number.phone_number, numbers=loc_numbers))
    return result

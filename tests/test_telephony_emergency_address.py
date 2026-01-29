import logging
import random
from collections.abc import Set
from dataclasses import dataclass

import random_address
import requests
from lxml import etree
from pydantic import BaseModel, Field
from tests.base import TestWithLocations
from tests.testutil import available_tns
from wxc_sdk.locations import Location
from wxc_sdk.telephony.emergency_address import EmergencyAddress

log = logging.getLogger(__name__)


class RandomAddress(BaseModel):
    class Config:
        extra = 'ignore'

    address1: str
    address2: str
    city: str
    state: str
    postal_code: str = Field(alias='postalCode')


def get_npas_for_zip(zip_code: str) -> Set[str]:
    """
    Get all NPA (area codes) associated with a given ZIP code using the nalennd.com API.

    This is taken from https://www.npanxxsource.com/npa-nxx-to-zip-code-lookup.htm

    Args:
        zip_code (str): The ZIP code to lookup (e.g., "85308")

    Returns:
        Set[str]: A set of unique NPA codes (area codes) for the given ZIP code
    """

    url = f"https://www.nalennd.com/api/npanxx2zip?qsc={zip_code}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse the XML response with lxml
        root = etree.fromstring(response.content)

        # Extract all NPA values using XPath
        npas = set()
        for npa_text in root.xpath('//NPANXX/NPA/text()'):
            if npa_text:
                npas.add(npa_text.strip())

        return npas

    except requests.exceptions.RequestException as e:
        log.error(f"Error making request for ZIP {zip_code}: {e}")
        raise
    except etree.XMLSyntaxError as e:
        log.error(f"Error parsing XML response for ZIP {zip_code}: {e}")
        raise
    except Exception as e:
        log.error(f"Unexpected error for ZIP {zip_code}: {e}")
        raise


@dataclass(init=False, repr=False)
class TestEmergencyAddress(TestWithLocations):
    """
    Test Emergency address settings for location
    """
    target: Location = None

    proxy = True

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.target = random.choice([loc for loc in cls.locations if loc.address.country == 'US'])

    def test_validate_emergency_address(self):
        # create random address
        address = RandomAddress.model_validate(random_address.real_random_address())
        api = self.api.telephony.emergency_address
        em_address = EmergencyAddress(address1=address.address1,
                                      address2=address.address2,
                                      city=address.city,
                                      state=address.state,
                                      postal_code=address.postal_code,
                                      country='US')
        r = api.lookup_for_location(location_id=self.target.location_id,
                                    address=em_address)
        print(address)
        print(r)

        # get NPAs for address
        npas = get_npas_for_zip(r[0].postal_code)

        print(f'NPAs for address: {", ".join(sorted(npas))}')

        tn_list = available_tns(api=self.api, tn_prefix=f'+1{random.choice(list(npas))}', tns_requested=10)
        print('\n'.join(tn_list))
        return

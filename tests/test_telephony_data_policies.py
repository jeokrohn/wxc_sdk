"""
Endpoint tests for organization and location data-policy settings.

The read tests use the configured Webex test organization, while update tests
mock the REST session to verify request construction without changing live
data-policy settings.
"""

from unittest import TestCase
from unittest.mock import MagicMock

from tests.base import TestWithLocations
from wxc_sdk.rest import RestSession
from wxc_sdk.telephony.data_policies import (
    CustomerDataPolicies,
    DataPoliciesApi,
    DataPolicyRegion,
    LocationDataPolicies,
)


class TestDataPoliciesRead(TestWithLocations):
    """Exercise data-policy read endpoints against a configured Webex organization."""

    proxy = True

    def test_read_data_policy_settings(self) -> None:
        """
        Read and validate the organization's data-policy settings.

        :return: None.
        :rtype: None
        :raises AssertionError: If the current user has no organization or the response has the wrong model type.

        This test issues a live GET request to Webex.
        """
        org_id = self.me.org_id
        self.assertIsNotNone(org_id, 'The current user must belong to an organization')

        settings = self.api.telephony.data_policies.read_data_policy_settings(org_id=org_id)

        self.assertIsInstance(settings, CustomerDataPolicies)

    def test_get_available_data_policy_regions(self) -> None:
        """
        Read and validate the regions available for data-policy configuration.

        :return: None.
        :rtype: None
        :raises AssertionError: If the response is empty or contains an unexpected model type.

        This test issues a live GET request to Webex.
        """
        org_id = self.me.org_id
        self.assertIsNotNone(org_id, 'The current user must belong to an organization')

        regions = self.api.telephony.data_policies.get_available_data_policy_regions(org_id=org_id)

        self.assertTrue(regions, 'At least one data-policy region must be available')
        self.assertTrue(all(isinstance(region, DataPolicyRegion) for region in regions))

    def test_get_location_data_policy_settings(self) -> None:
        """
        Read and validate data-policy settings for every discovered calling location.

        :return: None.
        :rtype: None
        :raises AssertionError: If a location response has the wrong model type.

        This test issues one live GET request to Webex for each calling location.
        """
        org_id = self.me.org_id
        self.assertIsNotNone(org_id, 'The current user must belong to an organization')

        for location in self.telephony_locations:
            with self.subTest(location_id=location.location_id, location_name=location.name):
                settings = self.api.telephony.data_policies.get_location_data_policy_settings(
                    location_id=location.location_id,
                    org_id=org_id,
                )
                self.assertIsInstance(settings, LocationDataPolicies)


class TestDataPoliciesUpdateRequests(TestCase):
    """Verify data-policy update requests without sending them to Webex."""

    def test_modify_data_policy_settings(self) -> None:
        """
        Build the expected organization data-policy update request.

        :return: None.
        :rtype: None
        :raises AssertionError: If the endpoint, query parameters, body, or return value is incorrect.

        The mocked REST session prevents this test from making a network request.
        """
        session = MagicMock(spec=RestSession)
        expected_url = 'https://webexapis.com/v1/telephony/config/dataPolicies'
        session.ep.return_value = expected_url
        api = DataPoliciesApi(session=session)

        result = api.modify_data_policy_settings(org_data_region='DE', org_id='org-id')

        self.assertIsNone(result)
        session.ep.assert_called_once_with('telephony/config/dataPolicies')
        session.rest_put.assert_called_once_with(
            expected_url,
            params={'orgId': 'org-id'},
            json={'orgDataRegion': 'DE'},
        )
        session.rest_get.assert_not_called()

    def test_modify_location_data_policy_settings(self) -> None:
        """
        Build the expected location data-policy update request, preserving a false boolean value.

        :return: None.
        :rtype: None
        :raises AssertionError: If the endpoint, query parameters, body, or return value is incorrect.

        The mocked REST session prevents this test from making a network request.
        """
        session = MagicMock(spec=RestSession)
        expected_url = 'https://webexapis.com/v1/telephony/config/locations/location-id/dataPolicies'
        session.ep.return_value = expected_url
        api = DataPoliciesApi(session=session)

        result = api.modify_location_data_policy_settings(
            location_id='location-id',
            location_data_region='DE',
            use_org_data_region_enabled=False,
            org_id='org-id',
        )

        self.assertIsNone(result)
        session.ep.assert_called_once_with('telephony/config/locations/location-id/dataPolicies')
        session.rest_put.assert_called_once_with(
            expected_url,
            params={'orgId': 'org-id'},
            json={'locationDataRegion': 'DE', 'useOrgDataRegionEnabled': False},
        )
        session.rest_get.assert_not_called()

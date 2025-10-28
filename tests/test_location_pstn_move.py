"""
test to move a location from on-premises PSTN to CCPP and update the phone number of a workspace
"""
import asyncio
from dataclasses import dataclass
from time import sleep
from unittest import skip

from tests.base import TestCaseWithLog
from tests.testutil import LocationSettings, create_workspace_with_webex_calling
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import RouteType, NumberState
from wxc_sdk.locations import Location, LocationAddress
from wxc_sdk.telephony.location import TelephonyLocation, PSTNConnection, CallingLineId, LocationDeleteStatus
from wxc_sdk.workspaces import WorkspaceSupportedDevices, Workspace


@skip('Apparently changing PSTN to CCPP is not supported via Hydra')
@dataclass(init=False, repr=False)
class TestLocationPSTNMove(TestCaseWithLog):
    # proxy = True

    workspace_number: str = None
    new_workspace_number: str = None

    location_settings: LocationSettings = None
    location_id: str = None
    location: Location = None
    telephony_location: TelephonyLocation = None
    trunk_id: str = None

    workspace: Workspace = None

    @classmethod
    async def create_location(cls, *, api: AsWebexSimpleApi):
        """
        * create random location
        * enable for calling
        * create registering trunk in location
        * set PSTN to on-premises PSTN
        * add some random numbers to location
        * set main number
        """
        # get settings for new location
        ls = await LocationSettings.create(async_api=api)
        cls.location_settings = ls
        cls.workspace_number, cls.new_workspace_number = ls.tn_list[:2]

        # create random location in US
        cls.location_id = cls.api.locations.create(name=ls.name,
                                                   time_zone='America/Chicago',
                                                   announcement_language=None,
                                                   preferred_language='de_de',
                                                   address1=ls.address.address1,
                                                   city=ls.address.city,
                                                   state=ls.address.state_or_province_abbr,
                                                   postal_code=ls.address.zip_or_postal_code,
                                                   country='US')

        # enable location for webex calling
        location = Location(location_id=cls.location_id,
                            name=ls.name,
                            time_zone='America/Chicago',
                            announcement_language='de_de',
                            preferred_language='de_de',
                            address=LocationAddress(address1=ls.address.address1,
                                                    city=ls.address.city,
                                                    state=ls.address.state_or_province_abbr,
                                                    postal_code=ls.address.zip_or_postal_code,
                                                    country='US'))
        await api.telephony.location.enable_for_calling(location=location)

        # add trunk
        password = cls.api.telephony.location.generate_password(location_id=cls.location_id)
        trunk_id = cls.api.telephony.prem_pstn.trunk.create(name=ls.trunk_name,
                                                            location_id=cls.location_id,
                                                            password=password)

        # set PSTN choice for location to trunk
        cls.api.telephony.location.update(location_id=cls.location_id,
                                          settings=TelephonyLocation(
                                              connection=PSTNConnection(type=RouteType.trunk,
                                                                        id=trunk_id)))

        # add numbers to location
        cls.api.telephony.location.number.add(location_id=cls.location_id,
                                              phone_numbers=[cls.workspace_number],
                                              state=NumberState.active)

        # finally set that number as main number and set site code
        await api.telephony.location.update(location_id=cls.location_id,
                                            settings=TelephonyLocation(
                                                calling_line_id=CallingLineId(
                                                    phone_number=cls.workspace_number),
                                                routing_prefix=ls.routing_prefix,
                                                outside_dial_digit='9',
                                                external_caller_id_name=ls.address.city))
        # get location details
        cls.location, cls.telephony_location = await asyncio.gather(api.locations.details(location_id=cls.location_id),
                                                                    api.telephony.location.details(
                                                                        location_id=cls.location_id))

        return

    @classmethod
    async def create_test_environment(cls):
        async with cls.as_webex_api(tokens=cls.tokens) as api:
            # set up calling location
            await cls.create_location(api=api)

            # * create random workspace in location
            cls.workspace = create_workspace_with_webex_calling(
                api=cls.api,
                target_location=cls.location,
                supported_devices=WorkspaceSupportedDevices.collaboration_devices,
                phone_number=cls.workspace_number,
                extension='',
                license=None)

    @classmethod
    def cleanup_test_environment(cls):
        """
        clean up test environment
        * delete workspace
        * delete location
        """
        cls.api.workspaces.delete_workspace(workspace_id=cls.workspace.workspace_id)
        delete_check = cls.api.telephony.locations.safe_delete_check_before_disabling_calling_location(
            location_id=cls.location_id)
        if delete_check.location_delete_status == LocationDeleteStatus.blocked:
            raise Exception(f'Location {cls.location.name} is blocked for deletion, {delete_check}')
        force_delete = delete_check.location_delete_status == LocationDeleteStatus.force_required
        job = cls.api.jobs.disable_calling_location.initiate(location_id=cls.location_id, force_delete=force_delete)
        while True:
            sleep(5)
            status = cls.api.jobs.disable_calling_location.status(job_id=job.id)
            if status.latest_execution_status in ('COMPLETED', 'FAILED'):
                break
        if status.latest_execution_status == 'FAILED':
            raise Exception(f'Failed to disable calling location {cls.location.name}')

        # delete location
        cls.api.locations.delete(location_id=cls.location_id)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Create a test environment
        asyncio.run(cls.create_test_environment())

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            cls.cleanup_test_environment()
        finally:
            super().tearDownClass()

    def test_move(self):
        """
        Test to move a location from on-premises PSTN to CCPP
        """
        # get PSTN Choices for location
        pstn_choices = self.api.telephony.pstn.list(location_id=self.location_id)
        current_pstn = self.api.telephony.pstn.read(location_id=self.location_id)
        pure_ip = next((p for p in pstn_choices if p.display_name.startswith('Pure IP')), None)
        if not pure_ip:
            raise Exception('No Pure IP PSTN Choice found')
        if True:
            self.api.telephony.pstn.configure(location_id=self.location_id,premise_route_id=pure_ip.id, premise_route_type=RouteType.cloud_connected_pstn)
        else:
            self.api.telephony.location.update(location_id=self.location_id,
                                               settings=TelephonyLocation(
                                                   connection=PSTNConnection(type=RouteType.cloud_connected_pstn,
                                                                             id=pure_ip.id)))
        pstn_after = self.api.telephony.pstn.read(location_id=self.location_id)

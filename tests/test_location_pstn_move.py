"""
test to move a location from on-premises PSTN to CCPP and update the phone number of a workspace
"""
import asyncio
from dataclasses import dataclass
from time import sleep

from tests.base import TestCaseWithLog, async_test
from tests.testutil import LocationSettings, create_workspace_with_webex_calling
from wxc_sdk.all_types import *
from wxc_sdk.as_api import AsWebexSimpleApi


@dataclass(init=False, repr=False)
class TestLocationPSTNMove(TestCaseWithLog):
    # proxy = True

    # initial TN for workspace
    workspace_number: str = None
    # TN to be set on workspace
    new_workspace_number: str = None

    # settings for testlocation creation
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
        * set the main number
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
        location = Location(id=cls.location_id,
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

        # finally, set that number as main number and set site code
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
        return

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
        return

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Create a test environment
        asyncio.run(cls.create_test_environment())
        return

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            cls.cleanup_test_environment()
        finally:
            super().tearDownClass()
        return

    @async_test
    async def test_move(self):
        """
        Test to move a location from on-premises PSTN to CCPP
        """

        async def update_pstn_and_number():
            """
            Update PSTN and phone number
            """

            async def update_pstn():
                """
                Update PSTN
                """
                # get PSTN Choices for location and current setting
                pstn_choices, pstn_before = await asyncio.gather(
                    self.async_api.telephony.pstn.list(location_id=self.location_id),
                    self.async_api.telephony.pstn.read(location_id=self.location_id))
                pstn_choices: list[PSTNConnectionOption]
                pstn_before: [PSTNConnectionOption]

                pure_ip = next((p for p in pstn_choices if p.display_name.startswith('Pure IP')), None)
                if not pure_ip:
                    raise Exception('No Pure IP PSTN choice found')
                await self.async_api.telephony.pstn.configure(location_id=self.location_id, id=pure_ip.id)
                # read PSTN settings after
                pstn_after = await self.async_api.telephony.pstn.read(location_id=self.location_id)
                return

            async def update_number():
                # add new number
                await self.async_api.telephony.location.number.add(location_id=self.location_id,
                                                                   phone_numbers=[self.new_workspace_number],
                                                                   state=NumberState.active)
                await asyncio.gather(
                    # update number of workspace
                    self.async_api.workspaces.update(
                        workspace_id=self.workspace.workspace_id,
                        settings=Workspace(
                            calling=WorkspaceCalling(
                                type=CallingType.webex,
                                webex_calling=WorkspaceWebexCalling(
                                    phone_number=self.new_workspace_number,
                                    location_id=self.location_id)))),
                    # update main number
                    self.async_api.telephony.location.update(location_id=self.location_id,
                                                             settings=TelephonyLocation(
                                                                 calling_line_id=CallingLineId(
                                                                     phone_number=self.new_workspace_number))))
                # remove old number from location
                await self.async_api.telephony.location.number.remove(location_id=self.location_id,
                                                                      phone_numbers=[self.workspace_number])
                return

            await asyncio.gather(
                update_pstn(),
                update_number())
            return

        async def create_and_assign_floor():
            """
            Create and assign floor
            """
            # create floor
            floor = await self.async_api.locations.create_floor(location_id=self.location_id,
                                                                floor_number=1,
                                                                display_name='First floor')
            # assign floor to workspace
            await self.async_api.workspaces.update(workspace_id=self.workspace.workspace_id,
                                                   settings=Workspace(floor_id=floor.id,
                                                                      location_id=self.location_id))
            return

        await asyncio.gather(
            update_pstn_and_number(),
            create_and_assign_floor())
        return

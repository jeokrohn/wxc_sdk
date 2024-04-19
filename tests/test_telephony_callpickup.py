# TODO: implement further test cases
import asyncio
import base64
import random
from dataclasses import dataclass
from itertools import chain
from typing import ClassVar

from tests.base import async_test, TestWithLocations
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.common import PersonPlaceAgent
from wxc_sdk.locations import Location
from wxc_sdk.telephony.callpickup import CallPickup, PickupNotificationType


async def get_available_agents(api: AsWebexSimpleApi, locations: list[Location]) -> list[list[PersonPlaceAgent]]:
    """
    Get available agents for each location
    """
    return await asyncio.gather(*[api.telephony.pickup.available_agents(location_id=loc.location_id)
                                  for loc in locations])


class TestDetails(TestWithLocations):
    @async_test
    async def test_all_details(self):
        """
        get details for all call pickups
        """
        locations = self.locations
        # get call pickups for all locations
        pickups = list(chain.from_iterable(
            await asyncio.gather(*[self.async_api.telephony.pickup.list(location_id=loc.location_id)
                                   for loc in locations])))
        pickups: list[CallPickup]
        if not pickups:
            self.skipTest('No existing call pickups')
        details = await asyncio.gather(*[self.async_api.telephony.pickup.details(location_id=cp.location_id,
                                                                                 pickup_id=cp.pickup_id)
                                         for cp in pickups])
        print(f'Got details for {len(details)} call pickups')

    @async_test
    async def test_available_agents(self):
        """
        get available agents for all locations
        """
        available_agents = await get_available_agents(api=self.async_api, locations=self.locations)
        # max length of location name for all locations w/ available agents
        try:
            location_len = max(len(loc.name) for loc, agents in zip(self.locations, available_agents)
                               if agents)
            user_type_len = max(len(agent.user_type) for agent in chain.from_iterable(available_agents))
        except ValueError:
            print(f'No available agents in any location')
            return

        # print location name and available agent
        print('Available agents:')
        for location, agents in zip(self.locations, available_agents):
            location: Location
            agents: list[PersonPlaceAgent]
            for agent in agents:
                print(f'{location.name:{location_len}}: {agent.user_type:{user_type_len}} - {agent.display_name}')


@dataclass(init=False)
class TestCreateAndUpdate(TestWithLocations):
    available_agents: ClassVar[list[list[PersonPlaceAgent]]]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        async def set_available_agents():
            async with AsWebexSimpleApi(tokens=cls.tokens) as api:
                cls.available_agents = await get_available_agents(api=api, locations=cls.locations)
        asyncio.run(set_available_agents())

    def test_001_create(self):
        """
        Create a new call pickup
        """
        # pick location and available agents
        try:
            location, agents = random.choice(list((location, agents)
                                                  for location, agents in zip(self.locations, self.available_agents)
                                                  if agents))
        except IndexError:
            self.skipTest('No available agents in any location')
        # create a call pick up in that location
        api = self.api.telephony.pickup
        cp_names = set(cp.name for cp in api.list(location_id=location.location_id))
        new_cp_name = next(cp_name for i in range(1000)
                           if (cp_name := f'cp_{i:03}') not in cp_names)
        agent = random.choice(agents)
        agent: PersonPlaceAgent
        new_cp = CallPickup(name=new_cp_name, agents=[PersonPlaceAgent(id=agent.agent_id)])
        # create new call pickup
        new_cp_id = api.create(location_id=location.location_id, settings=new_cp)
        try:
            # get details of new call pickup
            new_cp_details = api.details(location_id=location.location_id,
                                         pickup_id=new_cp_id)

            # apparently the CP name is the b64 decoded last part of the webex id
            self.assertEqual(new_cp_name, base64.b64decode(webex_id_to_uuid(new_cp_details.pickup_id)).decode())
            # we expect one agent
            self.assertEqual(1, len(new_cp_details.agents))
            self.assertEqual(agent.agent_id, new_cp_details.agents[0].agent_id)
            # .. and the defaults for pickup notifications
            self.assertEqual(6, new_cp_details.notification_delay_timer_seconds)
            self.assertEqual(PickupNotificationType.none, new_cp_details.notification_type)
        finally:
            # remove the call pickup again
            api.delete_pickup(location_id=location.location_id, pickup_id=new_cp_id)

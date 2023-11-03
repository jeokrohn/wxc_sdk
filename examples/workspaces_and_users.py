"""
Simple demo to add a user as secondary line to a workspace
"""
import asyncio
import sys

from dotenv import load_dotenv

from examples.service_app import env_path, get_tokens
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.common import UserType
from wxc_sdk.people import Person
from wxc_sdk.person_settings import TelephonyDevice
from wxc_sdk.telephony.devices import DeviceMembersResponse, DeviceMember


async def update_members(api: AsWebexSimpleApi, device: TelephonyDevice, members: list[DeviceMember], user: Person):
    """
    Update members of given device so that the device has two lines:
        * workspace
        * primary line of the given user
    """
    # keep the place membership (1st line)
    new_members = [member for member in members if member.member_type == UserType.place]

    # add the user as the 2nd member
    new_members.append(DeviceMember(member_id=user.person_id))

    # update members
    await api.telephony.devices.update_members(device_id=device.device_id,
                                               members=new_members)

    # apply config
    await api.telephony.devices.apply_changes(device_id=device.device_id)


async def main():
    # api instance
    load_dotenv(env_path())
    tokens = get_tokens()
    async with AsWebexSimpleApi(tokens=tokens) as api:
        # get target workspace
        ws_list = await api.workspaces.list(display_name='Classroom')
        target_ws = next((ws for ws in ws_list
                          if ws.display_name == 'Classroom'), None)
        if target_ws is None:
            print('Failed to find workspace', file=sys.stderr)
            exit(1)

        # find devices in that workspace
        ws_devices = await api.workspace_settings.devices.list(workspace_id=target_ws.workspace_id)

        # get members for all devices
        device_members = await asyncio.gather(*[api.telephony.devices.members(device_id=device.device_id)
                                                for device in ws_devices])
        device_members: list[DeviceMembersResponse]

        # add a user as secondary line to that device
        target_users = await api.people.list(display_name='Kristen Harper')
        if not target_users:
            print('Failed to get target user', file=sys.stderr)
            exit(1)
        target_user = target_users[0]

        # update all devices in that workspace
        await asyncio.gather(*[update_members(api=api, device=device, members=dmr.members, user=target_user)
                               for device, dmr in zip(ws_devices, device_members)])


if __name__ == '__main__':
    asyncio.run(main())

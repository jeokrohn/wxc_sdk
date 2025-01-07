import json
from itertools import chain

from pydantic import TypeAdapter

from tests.base import TestCaseWithLog
from wxc_sdk.telephony.guest_calling import DestinationMember


class TestGuestCalling(TestCaseWithLog):
    def test_read_settings(self):
        settings = self.api.telephony.guest_calling.read()
        print(json.dumps(settings.model_dump(mode='json'), indent=2))

    def test_members(self):
        members = list(self.api.telephony.guest_calling.members())
        print(json.dumps(TypeAdapter(list[DestinationMember]).dump_python(members, mode='json'), indent=2))

    def test_available_members(self):
        members = list(self.api.telephony.guest_calling.available_members())
        print(json.dumps(TypeAdapter(list[DestinationMember]).dump_python(members, mode='json'), indent=2))

    def test_update_members(self):
        settings = self.api.telephony.guest_calling.read()
        members = list(self.api.telephony.guest_calling.members())
        available_members = list(self.api.telephony.guest_calling.available_members())
        destination_members = [m.id for m in chain(members, available_members)]
        self.api.telephony.guest_calling.update(enabled=settings.enabled, privacy_enabled=settings.privacy_enabled,
                                                destination_members=destination_members)
        try:
            settings_after = self.api.telephony.guest_calling.read()
            self.assertEqual(settings, settings_after, 'Settings should not have changed')
            members_after = list(self.api.telephony.guest_calling.members())
            self.assertEqual(len(members_after), len(destination_members), 'Members should have been updated')
        finally:
            self.api.telephony.guest_calling.update(enabled=settings.enabled, privacy_enabled=settings.privacy_enabled,
                                                    destination_members=[m.id for m in members])
            print('Updated members back to original')
            settings_after = self.api.telephony.guest_calling.read()
            self.assertEqual(settings, settings_after, 'Settings not updated back to original')
            members_after = list(self.api.telephony.guest_calling.members())
            self.assertEqual(members, members_after, 'Members not updated back to original')

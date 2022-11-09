"""
Tests for messages API
"""
import uuid
from random import choice

from tests.base import TestCaseWithUsersAndSpaces
from wxc_sdk.common import RoomType
from wxc_sdk.rooms import Room


class TestMessages(TestCaseWithUsersAndSpaces):

    def test_001_create_message(self):
        """
        """
        api = self.api.messages
        with self.target_space() as target:
            target: Room
            messages = list(api.list(room_id=target.id))
            new_message = api.create(room_id=target.id, text=f'Random message {uuid.uuid4()}')

    def test_002_create_direct_message(self):
        api = self.api.messages
        # pick a random user
        target_user = choice(self.users)
        new_message = api.create(to_person_id=target_user.person_id, text=f'Random message {uuid.uuid4()}')
        # now a space has to exist with that user
        self.assertEqual(RoomType.direct, new_message.room_type)
        direct_by_id = list(api.list_direct(person_id=target_user.person_id))
        direct_by_email = list(api.list_direct(person_email=target_user.emails[0]))

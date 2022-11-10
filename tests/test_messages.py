"""
Tests for messages API
"""
import uuid
from random import choice

from pydantic import parse_obj_as

from tests.base import TestCaseWithUsersAndSpaces
from wxc_sdk.common import RoomType
from wxc_sdk.messages import MessageAttachment
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

    def test_003_create_direct_message_local_file(self):
        api = self.api.messages
        # pick a random user
        target_user = choice(self.users)
        new_message = api.create(to_person_id=target_user.person_id,
                                 text=f'Random message {uuid.uuid4()} with attachment',
                                 files=[__file__])
        # now a space has to exist with that user
        self.assertEqual(RoomType.direct, new_message.room_type)

    def test_003_attachment(self):
        attachments = [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "Sample Adaptive Card",
                            "size": "large"
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "url": "http://adaptivecards.io",
                            "title": "Learn More"
                        }
                    ]
                }
            }
        ]
        atts = parse_obj_as(list[MessageAttachment], attachments)
        foo = 1

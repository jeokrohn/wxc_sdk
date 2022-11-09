"""
Tests for RoomsApi
"""
import json
import re
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from random import choice

from tests.base import TestCaseWithLog
from wxc_sdk.rooms import Room


class TestRooms(TestCaseWithLog):
    def test_001_list(self):
        rooms = list(self.api.rooms.list())
        print(f'Got {len(rooms)} rooms')

    def test_002_create(self):
        rooms = list(self.api.rooms.list())
        new_names = (name for i in range(1000)
                     if (name := f'Test Space {i:03}') not in set(r.title for r in rooms))
        title = next(new_names)
        new_room = self.api.rooms.create(title=title)
        print(f'Created space "{title}"')
        print(json.dumps(json.loads(new_room.json(by_alias=True)), indent=2))

    def test_003_details(self):
        """
        details for all spaces
        """
        rooms = list(self.api.rooms.list())
        with ThreadPoolExecutor() as pool:
            details = list(map(lambda r: self.api.rooms.details(room_id=r.id), rooms))
        print(f'got details for {len(details)} rooms')

    def test_004_details(self):
        """
        meeting details for all spaces
        """
        rooms = list(self.api.rooms.list())
        with ThreadPoolExecutor() as pool:
            details = list(map(lambda r: self.api.rooms.meeting_details(room_id=r.id), rooms))
        print(f'got meeting details for {len(details)} rooms')

    @contextmanager
    def target_space(self):
        with self.no_log():
            rooms = [r for r in self.api.rooms.list()
                     if re.match(r'Test Space \d{3}', r.title)]
        if not rooms:
            self.skipTest('No targets')
        target = choice(rooms)
        details = self.api.rooms.details(room_id=target.id)
        try:
            yield details
        finally:
            after = self.api.rooms.update(update=details)
            self.assertEqual(details, after)

    def test_005_update_title(self):
        """
        meeting details for all spaces
        """
        with self.target_space() as room:
            room: Room
            title = f'{room.title}-XXX'
            update = Room(id=room.id, title=title)
            after = self.api.rooms.update(update)
            self.assertEqual(title, after.title)
            after.title = room.title
            self.assertEqual(room, after)

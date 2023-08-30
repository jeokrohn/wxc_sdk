import json
import uuid

from tests.base import TestCaseWithLog


class TestRooms(TestCaseWithLog):
    def test_001_list_all(self):
        spaces = list(self.api.rooms.list())
        print(f'got {len(spaces)} spaces')

    def test_002_create_public_space(self):
        name = f'public {uuid.uuid4()}'
        new_space = self.api.rooms.create(title=name, is_public=True, description=f'This is space "{name}"')
        details = self.api.rooms.details(room_id=new_space.id)
        print(json.dumps(json.loads(details.model_dump_json()), indent=2))

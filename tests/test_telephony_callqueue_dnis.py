"""
Live tests for call queue DNIS settings.
"""

import json
from contextlib import suppress
from typing import ClassVar
from unittest import SkipTest

from tests.base import TestCaseWithLog
from tests.testutil import available_extensions_gen, us_location_info
from wxc_sdk.common import RingPattern
from wxc_sdk.rest import RestError
from wxc_sdk.telephony.callqueue import CallQueue
from wxc_sdk.telephony.callqueue.dnis import Dnis, DnisAnnouncements, DnisSettings
from wxc_sdk.telephony.location import TelephonyLocation


class TestCallQueueDnis(TestCaseWithLog):
    """
    Live tests for :attr:`api.telephony.callqueue.dnis`.
    """

    target_location: ClassVar[TelephonyLocation] = None
    target_queue: ClassVar[CallQueue] = None
    allocated_extensions: ClassVar[set[str]] = set()
    dnis_name_index: ClassVar[int] = 0

    @classmethod
    def setUpClass(cls) -> None:
        """
        Create one temporary call queue used by all mutating DNIS tests.
        """
        super().setUpClass()
        if cls.api is None:
            return

        cls.target_location = cls.pick_target_location()
        if cls.target_location is None:
            raise SkipTest('Need at least one calling location to run DNIS tests')

        cls.target_queue = cls.create_target_queue()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Delete the temporary call queue created for this test case.
        """
        try:
            if cls.api is not None and cls.target_location is not None and cls.target_queue is not None:
                cls.api.telephony.callqueue.delete_queue(
                    location_id=cls.target_location.location_id,
                    queue_id=cls.target_queue.id,
                )
                print(f'Deleted temporary call queue "{cls.target_queue.name}"')
        except RestError as e:
            print(f'Failed to delete temporary call queue "{cls.target_queue.name}": {e}')
        finally:
            super().tearDownClass()

    @classmethod
    def pick_target_location(cls) -> TelephonyLocation | None:
        """
        Pick a calling location, preferring one with multiple existing phone numbers.

        :return: Location to use for the temporary call queue.
        """
        location_infos = us_location_info(api=cls.api)
        location_infos.sort(key=lambda info: len(info.numbers), reverse=True)
        target_info = next((info for info in location_infos if len(info.numbers) > 1), None)
        target_info = target_info or next(iter(location_infos), None)
        if target_info is not None:
            print(f'Using location "{target_info.tel_location.name}" with {len(target_info.numbers)} phone numbers')
            return target_info.tel_location

        locations = list(cls.api.telephony.locations.list())
        target_location = next(iter(locations), None)
        if target_location is not None:
            print(f'Using fallback calling location "{target_location.name}"')
        return target_location

    @classmethod
    def create_target_queue(cls) -> CallQueue:
        """
        Create the temporary extension-only call queue.

        :return: Details of the created queue.
        """
        location_id = cls.target_location.location_id
        call_queue_api = cls.api.telephony.callqueue
        queue_names = {queue.name for queue in call_queue_api.list(location_id=location_id)}
        queue_name = next(name for i in range(1000) if (name := f'dnis_test_{i:03}') not in queue_names)
        extension = cls.next_extension()

        settings = CallQueue.create(name=queue_name, agents=[], queue_size=5, extension=extension)
        queue_id = call_queue_api.create(location_id=location_id, settings=settings)
        details = call_queue_api.details(location_id=location_id, queue_id=queue_id)
        print(f'Created temporary call queue "{details.name}" ({details.extension}) in "{cls.target_location.name}"')
        return details

    @classmethod
    def next_extension(cls) -> str:
        """
        Get the next extension not already allocated by this test case.

        :return: Available extension candidate.
        """
        extensions = available_extensions_gen(api=cls.api, location_id=cls.target_location.location_id)
        for _ in range(1000):
            extension = next(extensions)
            if extension in cls.allocated_extensions:
                continue
            cls.allocated_extensions.add(extension)
            return extension
        raise SkipTest('Could not find an available extension')

    @classmethod
    def next_dnis_name(cls, prefix: str = 'dnis') -> str:
        """
        Get a unique DNIS name for the temporary queue.

        :param prefix: Name prefix.
        :return: DNIS name.
        """
        cls.dnis_name_index += 1
        return f'{prefix}_{cls.dnis_name_index:03}'

    def setUp(self) -> None:
        """
        Skip tests if class setup could not create a target queue.
        """
        super().setUp()
        if self.target_queue is None:
            self.skipTest('Need a temporary call queue to run DNIS tests')

    @property
    def target_ids(self) -> dict[str, str]:
        """
        Common location and queue IDs for DNIS API calls.

        :return: Keyword arguments for DNIS methods.
        """
        return {
            'location_id': self.target_location.location_id,  # type: ignore[dict-item]
            'queue_id': self.target_queue.id,  # type: ignore[dict-item]
        }

    def create_dnis(self, *, name: str = None, ring_pattern: RingPattern = RingPattern.normal) -> tuple[str, str, str]:
        """
        Create a DNIS entry on the temporary queue.

        :param name: DNIS name. A unique name is generated if omitted.
        :param ring_pattern: Ring pattern to assign.
        :return: DNIS ID, name, and extension.
        """
        api = self.api
        name = name or self.next_dnis_name()
        extension = self.next_extension()
        dnis_id = api.telephony.callqueue.dnis.create(
            **self.target_ids,
            name=name,
            extension=extension,
            ring_pattern=ring_pattern,
        )
        return dnis_id, name, extension

    def delete_dnis(self, dnis_id: str) -> None:
        """
        Delete one DNIS entry, ignoring already-deleted entries.

        :param dnis_id: DNIS ID to delete.
        """
        api = self.api
        with suppress(RestError):
            api.telephony.callqueue.dnis.delete(**self.target_ids, dnis_id=dnis_id)

    def test_001_available_phone_numbers(self):
        """
        Get available phone numbers for DNIS.
        """
        api = self.api
        numbers = list(
            api.telephony.callqueue.dnis.available_phone_numbers(location_id=self.target_location.location_id)
        )
        print(f'Got {len(numbers)} available DNIS phone numbers')

        target_number = next((number.phone_number for number in numbers if number.phone_number), None)
        if target_number is not None:
            filtered = list(
                api.telephony.callqueue.dnis.available_phone_numbers(
                    location_id=self.target_location.location_id,
                    phone_number=target_number,
                )
            )
            self.assertTrue(any(number.phone_number == target_number for number in filtered))

    def test_002_settings(self):
        """
        Get, modify, verify, and restore DNIS settings.
        """
        api = self.api
        original = api.telephony.callqueue.dnis.get_settings(**self.target_ids)
        print(json.dumps(json.loads(original.model_dump_json()), indent=2))

        update = DnisSettings(
            distinctive_ringing_enabled=not original.distinctive_ringing_enabled,
            display_dnis_name_and_number_enabled=not original.display_dnis_name_and_number_enabled,
        )
        try:
            api.telephony.callqueue.dnis.modify_settings(**self.target_ids, settings=update)
            updated = api.telephony.callqueue.dnis.get_settings(**self.target_ids)
            self.assertEqual(update.distinctive_ringing_enabled, updated.distinctive_ringing_enabled)
            self.assertEqual(
                update.display_dnis_name_and_number_enabled,
                updated.display_dnis_name_and_number_enabled,
            )
        finally:
            api.telephony.callqueue.dnis.modify_settings(**self.target_ids, settings=original)

    def test_003_create_list_details_modify_delete(self):
        """
        Create, list, read, modify, and delete one DNIS entry.
        """
        api = self.api
        dnis_id, name, extension = self.create_dnis()
        try:
            dnis_list = api.telephony.callqueue.dnis.list(**self.target_ids)
            self.assertIn(dnis_id, {dnis.id for dnis in dnis_list})

            details = api.telephony.callqueue.dnis.details(**self.target_ids, dnis_id=dnis_id)
            self.assertEqual(name, details.name)
            self.assertEqual(extension, details.extension)
            self.assertEqual(RingPattern.normal, details.ring_pattern)

            new_name = self.next_dnis_name(prefix='modified_dnis')
            api.telephony.callqueue.dnis.modify(
                **self.target_ids,
                dnis_id=dnis_id,
                settings=Dnis(name=new_name, extension=extension, ring_pattern=RingPattern.long_long),
            )
            modified = api.telephony.callqueue.dnis.details(**self.target_ids, dnis_id=dnis_id)
            self.assertEqual(new_name, modified.name)
            self.assertEqual(extension, modified.extension)
            self.assertEqual(RingPattern.long_long, modified.ring_pattern)

            api.telephony.callqueue.dnis.delete(**self.target_ids, dnis_id=dnis_id)
            dnis_id = None
            remaining_ids = {dnis.id for dnis in api.telephony.callqueue.dnis.list(**self.target_ids)}
            self.assertNotIn(details.id, remaining_ids)
        finally:
            if dnis_id is not None:
                self.delete_dnis(dnis_id)

    def test_004_announcements(self):
        """
        Get and modify DNIS announcements.
        """
        api = self.api
        dnis_id, _, _ = self.create_dnis(ring_pattern=RingPattern.short_long_short)
        try:
            announcements = api.telephony.callqueue.dnis.get_announcements(**self.target_ids, dnis_id=dnis_id)
            print(json.dumps(json.loads(announcements.model_dump_json()), indent=2))
            self.assertIsInstance(announcements, DnisAnnouncements)

            custom_enabled = bool(announcements.custom_dnis_announcement_settings_enabled)
            update = DnisAnnouncements(custom_dnis_announcement_settings_enabled=custom_enabled)
            api.telephony.callqueue.dnis.modify_announcements(
                **self.target_ids,
                dnis_id=dnis_id,
                settings=update,
            )
            updated = api.telephony.callqueue.dnis.get_announcements(**self.target_ids, dnis_id=dnis_id)
            self.assertIsInstance(updated, DnisAnnouncements)
            self.assertEqual(custom_enabled, bool(updated.custom_dnis_announcement_settings_enabled))
        finally:
            self.delete_dnis(dnis_id)

    def test_005_bulk_delete(self):
        """
        Bulk delete DNIS entries.
        """
        api = self.api
        created_ids: list[str] = []
        try:
            for ring_pattern in (RingPattern.normal, RingPattern.short_long_short):
                dnis_id, _, _ = self.create_dnis(ring_pattern=ring_pattern)
                created_ids.append(dnis_id)

            api.telephony.callqueue.dnis.bulk_delete(**self.target_ids, items=created_ids)
            remaining_ids = {dnis.id for dnis in api.telephony.callqueue.dnis.list(**self.target_ids)}
            self.assertFalse(set(created_ids) & remaining_ids)
            created_ids.clear()
        finally:
            for dnis_id in created_ids:
                self.delete_dnis(dnis_id)

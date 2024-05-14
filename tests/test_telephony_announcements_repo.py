"""
Tests around announcement repositories
"""
import asyncio
import base64
import io
import random
from collections.abc import Generator
from contextlib import contextmanager
from itertools import chain
from unittest import skip

from tests.base import async_test, TestWithLocations
from wxc_sdk.as_rest import AsRestError
from wxc_sdk.common import AnnAudioFile, Greeting, AnnouncementLevel
from wxc_sdk.locations import Location
from wxc_sdk.telephony.announcements_repo import RepoAnnouncement
from wxc_sdk.telephony.autoattendant import AutoAttendant
from wxc_sdk.telephony.callqueue import CallQueue
from wxc_sdk.telephony.location.moh import LocationMoHSetting, LocationMoHGreetingType


@skip('Asked to stop testing by Bob Russel')
class Repo(TestWithLocations):

    def new_ann_names(self, location_id: str = None) -> Generator[str, None, None]:
        """
        Get a generator of available announcement names at org/location level
        """
        api = self.api.telephony.announcements_repo
        with self.no_log():
            anns = list(api.list(location_id=location_id))
        new_names = (name
                     for i in range(1, 1000)
                     if (name := f'test_ann_{i:03}') not in set(ann.name for ann in anns))
        return new_names

    def test_001_list_all(self):
        api = self.api.telephony.announcements_repo
        anns = list(api.list())
        if not anns:
            self.skipTest('No announcements')
        print(f'got {len(anns)} announcements')

    def test_002_upload_org(self):
        new_name = next(self.new_ann_names())
        r = self.api.telephony.announcements_repo.upload_announcement(name=new_name, file='sample.wav',
                                                                      upload_as=f'sample_{new_name[-3:]}.wav')
        print(f'Uploaded new announcement: {new_name} id: {r}')

    @async_test
    async def test_003_modify_org(self):
        """
        modify an existing repo.
        Change:
            * name
            * file name
        :return:
        """
        api = self.api.telephony.announcements_repo
        with self.no_log():
            anns = list(api.list())
            # # try to only use announcements as targets for which we can also get details
            # details = await asyncio.gather(
            #     *[self.async_api.telephony.announcements_repo.details(announcement_id=ann.id)
            #       for ann in anns], return_exceptions=True)
            #
            # w_exception = [ann for ann, det in zip(anns, details) if isinstance(det, Exception)]
            # if w_exception:
            #     print(f'!!!!!!!!!!!!: failed to get details for {len(w_exception)} announcements')
            #
            # anns = [ann for ann, detail in zip(anns, details)
            #         if not isinstance(detail, Exception)]
        if not anns:
            self.skipTest('No org level announcements')
        target: RepoAnnouncement = random.choice(anns)
        new_name = next(self.new_ann_names())
        upload_as = f'from_modify_{new_name[-3:]}.wav'

        print(f'Trying to rename: "{target.name}" to "{new_name}", new file: {upload_as}')
        details_before = api.details(announcement_id=target.id)
        api.modify(announcement_id=target.id,
                   name=target.name,
                   file='sample.wav',
                   upload_as=upload_as)

        details_after = api.details(announcement_id=target.id)
        foo = 1
        self.assertTrue(False, 'Why can\'t we modify?')

    def test_004_upload_org_from_file(self):
        new_name = next(self.new_ann_names())
        with open('sample.wav', mode='rb') as wav_file:
            r = self.api.telephony.announcements_repo.upload_announcement(name=new_name, file=wav_file,
                                                                          upload_as=f'sample_{new_name[-3:]}.wav')
        print(f'Uploaded new announcement: {new_name} id: {r}')

    def test_005_upload_org_from_string(self):
        new_name = next(self.new_ann_names())
        with open('sample.wav', mode='rb') as wav_file:
            data = wav_file.read()
        binary_file = io.BytesIO(data)
        r = self.api.telephony.announcements_repo.upload_announcement(name=new_name, file=binary_file,
                                                                      upload_as=f'sample_{new_name[-3:]}.wav')
        print(f'Uploaded new announcement: {new_name} id: {r}')

    @async_test
    async def test_006_upload_org_async(self):
        api = self.async_api.telephony.announcements_repo
        new_name = next(self.new_ann_names())
        r = await api.upload_announcement(name=new_name, file='sample.wav', upload_as=f'sample_{new_name[-3:]}.wav')
        print(f'Uploaded new announcement: {new_name} id: {r}')

    def test_007_upload_location(self):
        api = self.api.telephony.announcements_repo
        locations = self.locations
        target_location = random.choice(locations)
        target_location: Location
        print(f'Target location: "{target_location.name}"')
        new_name = next(self.new_ann_names(location_id=target_location.location_id))
        r = api.upload_announcement(name=new_name, file='sample.wav', upload_as=f'sample_{new_name[-3:]}.wav',
                                    location_id=target_location.location_id)
        print(f'Uploaded new announcement in location: {new_name} id: {r}')

    def test_008_org_repository_usage(self):
        api = self.api.telephony.announcements_repo
        usage = api.usage()
        print(usage)

    @async_test
    async def test_009_location_repository_usage(self):
        locations = self.locations
        usages = await asyncio.gather(*[self.async_api.telephony.announcements_repo.usage(location_id=loc.location_id)
                                        for loc in locations], return_exceptions=True)
        loc_len = max(len(loc.name) for loc in locations)
        for location, usage in zip(locations, usages):
            print(f'{location.name:{loc_len}}: {usage}')

    @async_test
    async def test_010_details_org(self):
        api = self.async_api.telephony.announcements_repo
        anns = await api.list()
        if not anns:
            self.skipTest('No announcements at org level')
        details = await asyncio.gather(*[api.details(announcement_id=ann.id)
                                         for ann in anns], return_exceptions=True)
        err = next((detail for detail in details if isinstance(detail, Exception)), None)
        if err:
            for ann, detail in zip(anns, details):
                print(f'{ann.name}: ', end='')
                if isinstance(detail, Exception):
                    print(f'{detail}')
                else:
                    print(f'no issues')
            raise err
        print(f'Got details for {len(details)} announcements')

    @async_test
    async def test_011_details_location(self):
        """
        Get details for all announcements in all locations
        """
        locations = self.locations
        anns = await asyncio.gather(*[self.async_api.telephony.announcements_repo.list(location_id=loc.location_id)
                                      for loc in locations])
        anns: list[list[RepoAnnouncement]]
        # get details for all announcements in all locations
        details = await asyncio.gather(
            *[asyncio.gather(*[
                self.async_api.telephony.announcements_repo.details(announcement_id=ann.id,
                                                                    location_id=loc.location_id)
                for ann in loc_anns])
              for loc, loc_anns in zip(locations, anns)
              if loc_anns])
        print(f'got details for {sum(len(det) for det in details)} announcements')

    @async_test
    async def test_012_delete_ann_with_reference(self):
        api = self.async_api.telephony.announcements_repo
        anns = await api.list()
        if not anns:
            self.skipTest('No org announcements')
        # get details so we see feature references
        anns = await asyncio.gather(*[api.details(announcement_id=ann.id)
                                      for ann in anns])
        anns = [ann for ann in anns if ann.feature_references]
        if not anns:
            self.skipTest('No org announcement with references')
        target: RepoAnnouncement = random.choice(anns)
        with self.assertRaises(AsRestError) as exc:
            await api.delete(announcement_id=target.id)
        rest_error: AsRestError = exc.exception
        self.assertEqual(400, rest_error.status)
        self.assertEqual(6675, rest_error.detail.error_code)

    @async_test
    async def test_013_delete_org_ann_wo_reference(self):
        api = self.async_api.telephony.announcements_repo
        anns = await api.list()
        if not anns:
            self.skipTest('No org announcements')
        # get details so we see feature references
        anns = await asyncio.gather(*[api.details(announcement_id=ann.id)
                                      for ann in anns])
        anns = [ann for ann in anns if not ann.feature_references]
        if not anns:
            self.skipTest('No org announcement w/o references')
        target: RepoAnnouncement = random.choice(anns)
        await api.delete(announcement_id=target.id)
        print(f'deleted org announcement {target.name}, {target.file_name}')
        anns = await api.list()
        self.assertTrue(all(ann.name != target.name for ann in anns))

    @async_test
    async def test_014_delete_loc_ann_wo_reference(self):
        api = self.async_api
        locations = self.locations
        anns = list(chain.from_iterable(
            await asyncio.gather(*[api.telephony.announcements_repo.list(location_id=loc.location_id)
                                   for loc in locations])))

        if not anns:
            self.skipTest('No location announcements')

        anns: list[RepoAnnouncement]
        details = await asyncio.gather(*[api.telephony.announcements_repo.details(announcement_id=ann.id,
                                                                                  location_id=ann.location.id)
                                         for ann in anns])
        anns = [ann for ann, detail in zip(anns, details) if not detail.feature_references]
        if not anns:
            self.skipTest('No location announcement w/o references')
        target: RepoAnnouncement = random.choice(anns)
        await api.telephony.announcements_repo.delete(announcement_id=target.id, location_id=target.location.id)
        print(f'deleted location announcement {target.name}, {target.file_name} in location "{target.location.name}"')
        anns = await api.telephony.announcements_repo.list(location_id=target.location.id)
        self.assertTrue(all(ann.name != target.name for ann in anns))

    @async_test
    async def test_015_delete_org_ann_with_invalid_id(self):
        api = self.async_api
        with self.assertRaises(AsRestError) as exc:
            await api.telephony.announcements_repo.delete(announcement_id='jhgfdghj')


class RepoUsage(TestWithLocations):
    """
    Tests with references to announcements
    """

    @contextmanager
    def moh_context(self, location_id: str):
        moh_settings = self.api.telephony.location.moh.read(location_id=location_id)
        try:
            yield moh_settings
        finally:
            self.api.telephony.location.moh.update(location_id=location_id, settings=moh_settings)

    def test_001_moh_org_by_id(self):
        """
        Try to update MoH for a location to use an org_level announcement
        """
        target_location: Location = random.choice(self.locations)
        print(f'Updating MoH settings in location "{target_location.name}"')

        # find an org level announcement file
        anns = list(self.api.telephony.announcements_repo.list())
        if not anns:
            self.skipTest('No org level announcements')
        target_ann: RepoAnnouncement = random.choice(anns)
        print(f'.. to use custom greeting {target_ann.name}/{target_ann.file_name}')

        # get MoH settings (context)
        with self.moh_context(location_id=target_location.location_id) as moh_settings:
            moh_settings: LocationMoHSetting
            # set to custom file
            moh_settings.audio_file = AnnAudioFile(id=target_ann.id)
            moh_settings.greeting = LocationMoHGreetingType.custom
            self.api.telephony.location.moh.update(location_id=target_location.location_id, settings=moh_settings)
            updated = self.api.telephony.location.moh.read(location_id=target_location.location_id)
            target_ann_details_after = self.api.telephony.announcements_repo.details(announcement_id=target_ann.id)

            # the ann file should be in the MoH setting
            self.assertEqual(target_ann.id, updated.audio_file.id)
            self.assertEqual(LocationMoHGreetingType.custom, updated.greeting)

            # we want MoH in this location to be referenced
            reference = next((u for u in target_ann_details_after.feature_references
                              if u.location_id == target_location.location_id and u.name == 'Music On Hold'), None)
            self.assertIsNotNone(reference)

    def test_002_call_queue(self):
        """
        Take an existing call queue and try to set an announcement
        Then verify reference
        """
        api = self.api.telephony
        queues = list(api.callqueue.list())
        if not queues:
            self.skipTest('No call queues')
        target_queue: CallQueue = random.choice(queues)

        anns = list(api.announcements_repo.list())
        if not anns:
            self.skipTest('No org level announcements')
        target_ann: RepoAnnouncement = random.choice(anns)

        cq_before = api.callqueue.details(location_id=target_queue.location_id,
                                          queue_id=target_queue.id)
        ann_before = api.announcements_repo.details(announcement_id=target_ann.id)
        try:
            # set a comfort message announcement
            cq_update = cq_before.model_copy(deep=True)
            cm = cq_update.queue_settings.comfort_message
            cm.audio_announcement_files = [AnnAudioFile(id=target_ann.id)]
            cm.greeting = Greeting.custom

            api.callqueue.update(location_id=target_queue.location_id, queue_id=target_queue.id, update=cq_update)
            cq_after = api.callqueue.details(location_id=target_queue.location_id,
                                             queue_id=target_queue.id)
            ann_after = api.announcements_repo.details(announcement_id=target_ann.id)
            feature_ref = next((fr for fr in ann_after.feature_references
                                if
                                fr.type == 'Call Queue' and fr.name == cq_before.name and fr.location_id ==
                                cq_before.location_id),
                               None)
            if not feature_ref:
                print('No feature ref found in announcement details. Feature refs:')
                print('\n'.join(f'{fr}' for fr in ann_after.feature_references))
            self.assertIsNotNone(feature_ref)
            self.assertEqual(cq_before.id, feature_ref.id,
                             f'{base64.b64decode(cq_before.id + "==").decode()} != '
                             f'{base64.b64decode(feature_ref.id + "==").decode()} ')
        finally:
            # restore old settings
            api.callqueue.update(location_id=target_queue.location_id, queue_id=target_queue.id, update=cq_before)

    def test_002_auto_attendant(self):
        """
        Take an existing auto_attendant and try to set an announcement
        Then verify reference
        """
        api = self.api.telephony
        auto_attendants = list(api.auto_attendant.list())
        if not auto_attendants:
            self.skipTest('No autoattendants')
        target_aa: AutoAttendant = random.choice(auto_attendants)

        anns = list(api.announcements_repo.list())
        if not anns:
            self.skipTest('No org level announcements')
        target_ann: RepoAnnouncement = random.choice(anns)

        aa_before = api.auto_attendant.details(location_id=target_aa.location_id,
                                               auto_attendant_id=target_aa.auto_attendant_id)
        ann_before = api.announcements_repo.details(announcement_id=target_ann.id)
        try:
            # set the business hours menu greeting
            aa_update = aa_before.model_copy(deep=True)
            bhm = aa_update.business_hours_menu
            bhm.audio_announcement_file = AnnAudioFile(id=target_ann.id,
                                                       level=AnnouncementLevel.organization)
            bhm.greeting = Greeting.custom

            api.auto_attendant.update(location_id=target_aa.location_id,
                                      auto_attendant_id=target_aa.auto_attendant_id,
                                      settings=aa_update)
            aa_after = api.auto_attendant.details(location_id=target_aa.location_id,
                                                  auto_attendant_id=target_aa.auto_attendant_id)
            ann_after = api.announcements_repo.details(announcement_id=target_ann.id)
            feature_ref = next((fr for fr in ann_after.feature_references
                                if fr.type == 'Auto Attendant' and fr.name == aa_before.name and
                                fr.location_id == target_aa.location_id), None)
            if not feature_ref:
                print('No feature ref found in announcement details. Feature refs:')
                print('\n'.join(f'{fr}' for fr in ann_after.feature_references))
            self.assertIsNotNone(feature_ref)
            self.assertEqual(aa_before.auto_attendant_id, feature_ref.id,
                             f'{base64.b64decode(aa_before.auto_attendant_id + "==").decode()} != '
                             f'{base64.b64decode(feature_ref.id + "==").decode()} ')
        finally:
            # restore old settings
            api.auto_attendant.update(location_id=target_aa.location_id, auto_attendant_id=target_aa.auto_attendant_id,
                                      settings=aa_before)

import asyncio
import random

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.telephony.announcements_repo import RepoAnnouncement


class TestPlaylists(TestCaseWithLog):
    def test_list(self):
        playlists = list(self.api.telephony.playlist.list())
        print(f'{len(playlists)} playlists:')

    @async_test
    async def test_details(self):
        playlists = list(self.api.telephony.playlist.list())
        if not playlists:
            self.skip('No playlists found')
        details_list = await asyncio.gather(*[self.async_api.telephony.playlist.details(playlist.id)
                                              for playlist in playlists],
                                            return_exceptions=True)
        print(f'go details for {len(details_list)} playlists')

    @async_test
    async def test_assigned_locations(self):
        playlists = list(self.api.telephony.playlist.list())
        if not playlists:
            self.skip('No playlists found')
        plapi = self.async_api.telephony.playlist
        assigned_locations_list = await asyncio.gather(*[plapi.assigned_locations(playlist.id)
                                                         for playlist in playlists],
                                                       return_exceptions=True)
        print(f'Go assigned locations for {len(assigned_locations_list)} playlists')

    @async_test
    async def test_create(self):
        """
        Try to create a playlist
        """
        playlists = list(self.api.telephony.playlist.list())
        pl_names = set(pl.name for pl in playlists)
        new_names = (pl_name for i in range(1, 1000) if (pl_name := f'test_{i:03}') not in pl_names)
        pl_name = next(new_names)

        ann_files = list(self.api.telephony.announcements_repo.list())
        if not ann_files:
            self.skip('No announcement files found')
        targets: list[RepoAnnouncement] = random.sample(ann_files, min(3, len(ann_files)))
        target_ids = [target.id for target in targets]
        print(f'Creating playlist {pl_name} with {len(targets)} announcements')
        print('\n'.join(f'  {target.id}: {target.name}' for target in targets))
        new_pl_id = self.api.telephony.playlist.create(name=pl_name, announcement_ids=target_ids)
        try:
            # get details for all repo announcements we used to check that the playlist is referenced
            details_list = await asyncio.gather(*[self.async_api.telephony.announcements_repo.details(target.id)
                                                  for target in targets],
                                                return_exceptions=True)
            details_list: list[RepoAnnouncement]
            # all repo announcements have to have at least one referenced playlist and our new playlist has to be one
            # of them
            self.assertTrue(all(details.playlists and next((pl for pl in details.playlists if pl.id == new_pl_id), None)
                                for details in details_list),
                            'Not all announcements have the new playlist referenced')
        finally:
            print(f'Deleting playlist {pl_name}')
            self.api.telephony.playlist.delete(new_pl_id)

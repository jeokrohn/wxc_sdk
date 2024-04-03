"""
test cases for voicemail groups
"""
import asyncio
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from functools import reduce
from itertools import chain
from random import choice
from re import match
from statistics import mean
from typing import Union

from wxc_sdk.as_rest import AsRestError
from wxc_sdk.locations import Location
from wxc_sdk.rest import RestError
from wxc_sdk.telephony import NumberListPhoneNumber
from wxc_sdk.telephony.voicemail_groups import VoicemailGroupDetail, VoicemailGroup
from tests.base import async_test, TestWithLocations
from tests.testutil import available_numbers


class TestVmGroup(TestWithLocations):

    @contextmanager
    def assert_vmg(self) -> VoicemailGroup:
        """
        Get a traget
        :return:
        """
        vmg = self.api.telephony.voicemail_groups
        groups = None
        created = False
        for _ in range(2):
            with self.no_log():
                groups = list(g for g in vmg.list()
                              if match(r'^test_\d{3}$', g.name))
            if groups:
                break
            with self.no_log():
                created = True
                self.test_003_create()
        if not groups:
            self.skipTest('No voicemail groups to mess with')
        group = choice(groups)
        try:
            yield group
        finally:
            if created:
                try:
                    with self.no_log():
                        vmg.delete(location_id=group.location_id,
                                   voicemail_group_id=group.group_id)
                except RestError as e:
                    if e.response.status_code != 404 or e.code != 4008:
                        raise

    def test_001_list(self):
        """
        list voicemail groups
        """
        with self.assert_vmg():
            vmg = self.api.telephony.voicemail_groups
            groups = list(vmg.list())
            print(f'Got {len(groups)} voicemail groups')

    @async_test
    async def test_002_list_by_location_id(self):
        """
        filter lst by location id
        """
        # get list of voicemail groups and numbers
        groups, numbers = await asyncio.gather(
            self.async_api.telephony.voicemail_groups.list(),
            self.async_api.telephony.phone_numbers()
        )
        locations = self.locations
        locations: list[Location]
        groups: list[VoicemailGroup]
        numbers: list[NumberListPhoneNumber]
        group_names_by_location_id: dict[str, list[str]] = reduce(
            lambda red, elem: red[elem.location_id].append(elem.name) or red,
            groups,
            defaultdict(list)
        )
        extensions_by_location: dict[str, list[str]] = reduce(
            lambda red, elem: red[elem.location.id].append(elem.extension) or red,
            (n for n in numbers if n.extension),
            defaultdict(list)
        )

        async def create_vmg(location: Location) -> str:
            """
            create a voicemail group in given location
            :param location:
            :return: voicemail group id
            """
            extension = next(available_numbers(
                numbers=extensions_by_location[location.location_id]))
            name = next(name for i in range(1, 1000)
                        if (name := f'test_{i:03}') not in group_names_by_location_id[location.location_id])
            settings = VoicemailGroupDetail.create(
                name=name, extension=extension, first_name='test', last_name=name,
                passcode=740384)
            new_id = await self.async_api.telephony.voicemail_groups.create(
                location_id=location.location_id,
                settings=settings)
            return new_id

        # create a new voicemail group in each location
        # noinspection PyTypeChecker
        new_vmg_ids = await asyncio.gather(*[create_vmg(loc) for loc in locations],
                                           return_exceptions=True)
        new_vmg_ids: tuple[Union[Exception, str]]

        try:
            # now list voicemail groups for each location
            # noinspection PyTypeChecker
            vmg_lists = await asyncio.gather(
                *[self.async_api.telephony.voicemail_groups.list(location_id=loc.location_id)
                  for vmg_id, loc in zip(new_vmg_ids, locations)],
                return_exceptions=True)
            vmg_lists: list[Union[Exception, tuple[VoicemailGroup]]]
            err = False
            for location, vmg_id, vmg_list in zip(locations, new_vmg_ids, vmg_lists):
                # do some validation
                print(f'Validation for location "{location.name}"')
                # check that the created voicemail group is in the list
                if isinstance(vmg_list, Exception):
                    print(f'  failed to get list of voicemail groups in location: {vmg_list}')
                    vmg_list = []
                    err = True
                if isinstance(vmg_id, Exception):
                    print(f'  failed to create voicemail group: {vmg_id}')
                    vmg_if = None
                    err = True
                # check that created voicemail group is in list
                elif next((vmg for vmg in vmg_list
                           if vmg.group_id == vmg_id), None) is None:
                    print(f'  failed to find created voicemail group in list of voicemail groups of location')
                    err = True
                # verify that only voicemail groups of the requested location are in the list
                if any(vmg for vmg in vmg_list if vmg.group_id != location.location_id):
                    print('  Found some voicemail groups not belonging to location in list of voicemail groups')
                    err = True
            self.assertFalse(err, 'Something went wrong (check output)')
        finally:
            # clean up: delete voicemail groups we created earlier
            await asyncio.gather(*[self.async_api.telephony.voicemail_groups.delete(
                location_id=location.location_id,
                voicemail_group_id=gid)
                for location, gid in zip(locations, new_vmg_ids)
                if not isinstance(gid, Exception)],
                                 return_exceptions=True)

    @async_test
    async def test_003_list_pagination(self):
        """
        Test pagination for list()
        """

        async def create_vmg(location, name, extension):
            """
            Create a voicemail group with basic settings within location
            :param location
            :param name:
            :param extension:
            :return: voicemail group id
            """
            settings = VoicemailGroupDetail.create(
                name=name, extension=extension, first_name='test', last_name=name,
                passcode=740384)
            # create with some retries
            for i in range(1, 6):
                try:
                    r = await self.async_api.telephony.voicemail_groups.create(
                        location_id=location.location_id,
                        settings=settings)
                except AsRestError:
                    print(f'Failed to create voicemail group "{name}" in location "{location.name}"')
                    if i < 5:
                        await asyncio.sleep(5)
                    else:
                        raise
                else:
                    break
            print(f'Created voicemail group "{name}" in location "{location.name}"')
            return r

        async def create_vmgs_in_location(location: Location) -> list[Union[Exception, str]]:
            """
            Create test voicemail groups in given location
            :param location:
            :return: list of voicemail group ids or exceptions
            """
            new_names = (name for i in range(1, 1000)
                         if (name := f'test_{i:03}') not in set(g.name for g in groups
                                                                if g.location_id == location.location_id))
            extensions = (n.extension for n in numbers
                          if n.extension)
            new_extensions = available_numbers(extensions)
            r = await asyncio.gather(*[create_vmg(location, next(new_names), next(new_extensions))
                                       for _ in range(number_of_groups_to_create)],
                                     return_exceptions=True)
            return r

        # start of test
        number_of_groups_to_create = 10

        with self.no_log():
            groups, numbers = await asyncio.gather(self.async_api.telephony.voicemail_groups.list(),
                                                   self.async_api.telephony.phone_numbers())
        locations = self.locations
        locations: list[Location]
        groups: list[VoicemailGroup]
        numbers: list[NumberListPhoneNumber]

        create_some = len(groups) < (len(locations) * number_of_groups_to_create * 2)
        if create_some:
            # create some voicemail groups in each location
            with self.no_log():
                vmg_ids = list(chain.from_iterable(await asyncio.gather(*[create_vmgs_in_location(loc)
                                                                          for loc in locations],
                                                                        return_exceptions=True)))

        # now list with small paging size and large paging size
        # results should be identical
        try:
            voicemail_group_list = await self.async_api.telephony.voicemail_groups.list()
            voicemail_group_list_small_page = await self.async_api.telephony.voicemail_groups.list(
                max=number_of_groups_to_create)
            # look at the paginations
            paginated_requests = [request
                                  for request in self.requests(method='GET', url_filter=r'.+config/voicemailGroups')
                                  if request.url_query.get('max')]
            pagination_link_error = False
            for i, request in enumerate(paginated_requests, 1):
                start = (start := request.url_query.get('start')) and int(start[0])
                items = len(request.response_body['voicemailGroups'])
                print(f'page {i}: start={start}, items={items}')
                link_header = request.response_headers.get('Link')
                if link_header and (link_match := match(r'<(?P<link>\S+)>;rel="(?P<rel>\w+)"', link_header)):
                    print(f'  {link_match["rel"]}: {link_match["link"]}')
                    if link_match['link'].startswith('https,'):
                        pagination_link_error = True

            vmg_ids = set(g.group_id for g in voicemail_group_list)
            vmg_ids_small_page = set(g.group_id for g in voicemail_group_list_small_page)

            # apparently some groups are duplicated in the list with small pages
            # try to collect the locations in the list per group
            group_index_lists: dict[str, list[int]] = reduce(lambda red, ig: red[ig[1].group_id].append(ig[0]) or red,
                                                             enumerate(voicemail_group_list_small_page),
                                                             defaultdict(list))
            done = set()
            for group in voicemail_group_list_small_page:
                if group.group_id in done:
                    continue
                done.add(group.group_id)
                index_list = group_index_lists[group.group_id]
                if len(index_list) > 1:
                    print(f'group "{group.name}" ({group.group_id}) in "{group.location_name}" listed multiple times '
                          f'in paginated list: '
                          f'{", ".join(str(i) for i in index_list)}')
            missing_in_small_page_set = vmg_ids - vmg_ids_small_page
            if missing_in_small_page_set:
                # determine location of missing ids in list
                for i, g in enumerate(voicemail_group_list):
                    if g.group_id in missing_in_small_page_set:
                        print(f'Small pagination list missed index {i} from long list, "{g.name}" ({g.group_id}) in'
                              f' "{g.location_name}"')

            self.assertEqual(len(voicemail_group_list), len(voicemail_group_list_small_page), 'Length differs')
            self.assertEqual(vmg_ids, vmg_ids_small_page, 'Did not get the same set of groups')

            # also we want to check fpr errors while creating the voicemail groups
            errors = [r for r in vmg_ids
                      if isinstance(r, Exception)]
            if errors:
                print('\n'.join(f'{i} - Error creating a voicemail group{e}'
                                for i, e in enumerate(errors, 1)))
                self.assertTrue(not errors)

            # finally verify that pagination links were ok
            self.assertFalse(pagination_link_error, 'wrong format in pagination links')
        finally:
            # clean up: remove voicemail groups again?
            ...

    def test_002_details(self):
        """
        get details for all VM groups
        """
        with self.assert_vmg():
            api = self.api.telephony.voicemail_groups
            groups = list(api.list())
            with ThreadPoolExecutor() as pool:
                details = list(pool.map(lambda g: api.details(location_id=g.location_id,
                                                              voicemail_group_id=g.group_id),
                                        groups))
            print(f'Got details for {len(groups)} voicemail groups')

    @async_test
    async def test_details_undocumented_time_zone(self):
        """
        Get details and check for undocumented time_zone attribute
        """
        with self.assert_vmg():
            api = self.async_api.telephony.voicemail_groups
            groups = await api.list()
            details = await asyncio.gather(*[api.details(location_id=g.location_id,
                                                         voicemail_group_id=g.group_id)
                                             for g in groups])
            details: list[VoicemailGroupDetail]
        with_time_zone = [d for d in details if d.time_zone]
        print(f'got time_zone (undocumented) for {len(with_time_zone)} voicemail groups')
        # we want to raise an exception if the undocumented attribute is gone
        self.assertTrue(with_time_zone, 'Undocumented attribute time_zone is gone?')

    def test_003_create(self):
        """
        Create a simple voicemail group
        """
        with self.no_log():
            # pick target location
            locations = self.locations
            location = choice(locations)

            # get unique name for new group
            vmg = self.api.telephony.voicemail_groups
            groups = list(vmg.list())
            vmg_name = next(name for i in range(1, 1000)
                            if (name := f'test_{i:03}') not in set(g.name for g in groups))
            # get extension within location
            extensions = set(n.extension for n in self.api.telephony.phone_numbers(location_id=location.location_id)
                             if n.extension)
            if extensions:
                first_digits: dict[str, set[str]] = reduce(lambda red, e: red[e[:1]].add(e) or red,
                                                           extensions, defaultdict(set))
                first_digit = max(first_digits, key=lambda fd: len(first_digits[fd]))
                extensions = first_digits[first_digit]
                extension = next(ext for i in range(1, 1000)
                                 if (ext := f'{first_digit}{i:03}') not in extensions)
            else:
                extension = '1000'
        # create voicemail group
        settings = VoicemailGroupDetail.create(
            name=vmg_name, extension=extension, first_name='test', last_name=vmg_name,
            passcode=740384,
            language_code='en_us')
        vmg_id = vmg.create(location_id=location.location_id,
                            settings=settings)
        print(f'Created new voicemail group "{vmg_name} in location "{location.name}" with extension {extension}')

    def test_004_update(self):
        """
        Try to update a VNG
        """
        with self.assert_vmg() as group:
            group: VoicemailGroup
            api = self.api.telephony.voicemail_groups
            details = api.details(location_id=group.location_id, voicemail_group_id=group.group_id)
            api.update(location_id=group.location_id, voicemail_group_id=group.group_id, settings=details)
            after = api.details(location_id=group.location_id, voicemail_group_id=group.group_id)
            self.assertEqual(details, after)

    def test_005_update_enabled(self):
        """
        Try to update a VNG: toggle the enabled settings
        """
        with self.assert_vmg() as group:
            group: VoicemailGroup
            api = self.api.telephony.voicemail_groups
            # get details
            details = api.details(location_id=group.location_id, voicemail_group_id=group.group_id)
            try:
                # toggle enabled
                enabled = not details.enabled
                settings = VoicemailGroupDetail(enabled=enabled)
                api.update(location_id=group.location_id, voicemail_group_id=group.group_id, settings=settings)
                # get updated info and make sure that the updated worked
                after = api.details(location_id=group.location_id, voicemail_group_id=group.group_id)
                expected = details.model_copy(deep=True)
                expected.enabled = enabled
                self.assertEqual(expected, after)
            finally:
                # restore old settings
                api.update(location_id=group.location_id, voicemail_group_id=group.group_id, settings=details)

    def test_006_delete(self):
        """
        Delete a voicemail group
        """
        with self.assert_vmg() as group:
            group: VoicemailGroup
            api = self.api.telephony.voicemail_groups
            print(f'Deleting voicemail group "{group.name}" in location "{group.location_name}"')
            api.delete(location_id=group.location_id, voicemail_group_id=group.group_id)

            # make sure the group is gone
            groups = list(api.list(location_id=group.location_id))
            after = next((g for g in groups if g.group_id == group.group_id), None)
            self.assertIsNone(after)

    async def delete_vm_groups(self, create: int = 0):
        """
        Delete a bunch of vm groups
        :param create: make sure that at least this number of vm groups exists before deleting them
        """
        groups = await self.async_api.telephony.voicemail_groups.list(name='test_')

        if len(groups) < create:
            # create a bunch of groups so that there is something to delete
            # pick target location
            locations = self.locations
            location = choice(locations)

            # get unique name for new group
            vmg = self.async_api.telephony.voicemail_groups
            groups = await vmg.list()
            vmg_names = (name for i in range(1, 1000)
                         if (name := f'test_{i:03}') not in set(g.name for g in groups))
            # get extension within location
            extensions = set(n.extension for n in self.api.telephony.phone_numbers(location_id=location.location_id)
                             if n.extension)
            extensions = extensions or {'1xxx'}
            first_digits: dict[str, set[str]] = reduce(lambda red, e: red[e[:1]].add(e) or red,
                                                       extensions, defaultdict(set))
            first_digit = max(first_digits, key=lambda fd: len(first_digits[fd]))
            extensions = first_digits[first_digit]
            new_extensions = (ext for i in range(1, 1000)
                              if (ext := f'{first_digit}{i:03}') not in extensions)
            # create a bunch of voicemail groups
            await asyncio.gather(*[vmg.create(location_id=location.location_id,
                                              settings=VoicemailGroupDetail.create(
                                                  name=(vmg_name := next(vmg_names)),
                                                  extension=next(new_extensions),
                                                  first_name='test',
                                                  last_name=vmg_name,
                                                  passcode=740384,
                                                  language_code='en_us')) for _ in range(create - len(groups))])
            groups = await self.async_api.telephony.voicemail_groups.list(name='test_')
        groups = [g for g in groups
                  if match(r'^test_\d{3}$', g.name)]

        if not groups:
            self.skipTest('No group to delete')
            return

        async def delete_one(g: VoicemailGroup):
            """
            Try to delete a voicemail group with a bunch of retries
            :param g:
            """
            tries = 5
            error = None
            for i in range(1, tries + 1):
                try:
                    await self.async_api.telephony.voicemail_groups.delete(
                        location_id=g.location_id,
                        voicemail_group_id=g.group_id)
                except AsRestError as e:
                    error = e
                    print(f'"{g.name}" in "{g.location_name}" ({i}): failed {e}')
                    if i < tries:
                        await asyncio.sleep(5)
                else:
                    print(f'"{g.name}" in "{g.location_name}" ({i}): deleted')
                    break
            if error:
                raise error
            return

        print(f'Deleting {len(groups)} voicemail groups')
        results = await asyncio.gather(*[delete_one(g)
                                         for g in groups], return_exceptions=True)
        for group, result in zip(groups, results):
            if isinstance(result, Exception):
                print(f'"{group.name}" in "{group.location_name}": error deleting {result}')

        requests = list(self.requests(method='DELETE'))
        failure_response_times = [request.time_ms for request in requests
                                  if request.status != 204]
        success_response_times = [request.time_ms for request in requests
                                  if request.status == 204]

        # avoid empty sequence for min(), max(), mean()
        failure_response_times = failure_response_times or None
        success_response_times = success_response_times or None
        if success_response_times:
            print(f'Success: min={min(success_response_times):.2f}, max={max(success_response_times):.2f}, '
                  f'mean={mean(success_response_times):.2f}')
        if failure_response_times:
            print(f'Failure: min={min(failure_response_times):.2f}, max={max(failure_response_times):.2f}, '
                  f'mean={mean(failure_response_times):.2f}')

        self.assertFalse(any(isinstance(r, Exception) for r in results))

    @async_test
    async def test_007_delete_batch(self):
        """
        Bulk delete a bunch of test voicemail groups; at least 50
        """
        await self.delete_vm_groups(create=50)

    @async_test
    async def test_008_cleanup(self):
        """
        Bulk delete all remaining test voicemail groups
        """
        await self.delete_vm_groups()

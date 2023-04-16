import asyncio
import random
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from typing import Optional

from wxc_sdk.groups import Group, GroupMember
from tests.base import TestCaseWithLog, async_test


class TestGroups(TestCaseWithLog):

    def test_001_create(self):
        """
        Create a new group without members
        """
        ga = self.api.groups
        group_list = list(ga.list())
        names = set(g.display_name for g in group_list)
        new_names = (name for i in range(1000)
                     if (name := f'test_{i:03}') not in names)
        settings = Group(display_name=next(new_names))
        new_group = ga.create(settings=settings)
        print(f'New group: {new_group}')

    def test_002_list(self):
        """
        list groups
        """
        group_list = list(self.api.groups.list(include_members=True))
        print(f'got {len(group_list)} groups')

    @async_test
    async def test_003_pagination(self):
        """
        Pagination when listing groups
        """
        ga = self.async_api.groups
        new_groups = None
        with self.no_log():
            group_list = await ga.list(include_members=True)
            # we want to have at least 30 groups to test with
            missing = max(0, 30 - len(group_list))

            if missing:
                # create missing groups to get to 30

                # existing group names
                names = set(g.display_name for g in group_list)

                # generator for new group names
                new_names = (name for i in range(1000)
                             if (name := f'test_{i:03}') not in names)

                # create them...
                # noinspection PyTypeChecker
                new_groups: list[Group] = await asyncio.gather(*[ga.create(settings=Group(display_name=next(new_names)))
                                                                 for _ in range(missing)])
        # complete list of groups after creating new groups
        group_list = await ga.list(include_members=True)

        # get list with pagination
        paginated_list = await ga.list(count=5, include_members=True)
        try:
            requests = list(self.requests(method='GET', url_filter=r'.+v1/groups\?.*count='))
            # get start index parameter, count parameter and number of returned elements in each request
            start_count_len: list[tuple[Optional[int], int, int]] = [((s := r.url_query.get('startIndex',
                                                                                            [None])[0]) and int(s),
                                                                      (c := r.url_query.get('count',
                                                                                            [None])[0]) and int(c),
                                                                      len(r.response_body['groups'])) for r in
                                                                     requests]
            for i, (s, c, l) in enumerate(start_count_len, 1):
                print(f'request {i}: start={str(s):4}, count={c}, len={l}')

            group_ids = set(group.group_id for group in group_list)
            group_ids_paginated = set(group.group_id for group in paginated_list)
            id_positions: dict[str, list[int]] = reduce(lambda red, ig: red[ig[1].group_id].append(ig[0]) or red,
                                                        enumerate(paginated_list),
                                                        defaultdict(list))
            groups_by_id = {group.group_id: group for group in group_list}
            issues = {g: p for g, p in id_positions.items() if len(p) > 1}
            for gid, positions in issues.items():
                group = groups_by_id[gid]
                print(f'group {gid}, {group.display_name} returned at positions '
                      f'{", ".join(str(p) for p in positions)}')

            self.assertTrue(all(c == l for _, c, l in start_count_len))
            self.assertTrue(not issues)
            self.assertEqual(group_ids, group_ids_paginated)
            self.assertEqual(group_list, paginated_list)
        finally:
            # clean up: remove groups we created above
            if new_groups:
                with self.no_log():
                    await asyncio.gather(*[ga.delete_group(group_id=group.group_id) for group in new_groups])

    @async_test
    async def test_004_all_details(self):
        """
        Get details for all groups
        """
        ga = self.async_api.groups
        group_list = await ga.list(include_members=True)
        details = await asyncio.gather(*[ga.details(group_id=group.group_id,
                                                    include_members=True)
                                         for group in group_list])
        print(f'Got details for {len(group_list)} groups')

    def test_005_add_users(self):
        """
        try to add users to a group
        """
        ga = self.api.groups
        group_list = list(ga.list())
        names = set(g.display_name for g in group_list)
        new_names = (name for i in range(1000)
                     if (name := f'test_{i:03}') not in names)

        # settings for new group, minimal: just a name
        settings = Group(display_name=next(new_names))
        new_group = self.api.groups.create(settings=settings)
        try:
            # pick a few users to add to group
            users = list(self.api.people.list())
            to_add = random.sample(users, 5)

            # update group
            settings = Group(members=[GroupMember(member_id=u.person_id) for u in to_add])
            updated_group = ga.update(group_id=new_group.group_id, settings=settings)

            self.assertEqual(5, len(updated_group.members))
            self.assertTrue(all(m.member_type == 'user' for m in updated_group.members))
            member_ids = set(m.member_id for m in updated_group.members)
            self.assertTrue(all(u.person_id in member_ids for u in to_add))
        finally:
            # delete group again
            self.api.groups.delete_group(group_id=new_group.group_id)

    def test_006_add_and_delete_user(self):
        """
        Try to add and delete users at the same time
        """
        ga = self.api.groups
        group_list = list(ga.list(include_members=True))
        target_groups = [g for g in group_list if g.members and len(g.members) > 2]
        if not target_groups:
            self.skipTest('Need at least one group with more than one member')
        target_group = random.choice(target_groups)
        remove_member = random.choice(target_group.members)
        members = [GroupMember(operation='delete', member_id=remove_member.member_id)]

        # determine 2 users to add
        member_ids = set(m.member_id for m in target_group.members)
        users = list(self.api.people.list())
        users = [u for u in users if u.person_id not in member_ids]
        to_add = random.sample(users, 2)
        members.extend(GroupMember(member_id=u.person_id) for u in to_add)

        # update the group
        settings = Group(members=members)
        updated_group = ga.update(group_id=target_group.group_id, settings=settings)

        # check result
        member_ids_after = set(m.member_id for m in updated_group.members)
        self.assertNotIn(remove_member.member_id, member_ids_after)
        for u in to_add:
            self.assertIn(u.person_id, member_ids_after)

    def test_007_members(self):
        """
        Get members of groups
        """
        ga = self.api.groups
        group_list = list(ga.list(include_members=True))
        target_groups = [g for g in group_list if g.members]
        if not target_groups:
            self.skipTest('Need a group with members to run this test')
        with ThreadPoolExecutor() as pool:
            list(pool.map(lambda g: list(ga.members(group_id=g.group_id)),
                          target_groups))
        print(f'Got members for {len(target_groups)} groups')

    def test_008_members_with_pagination(self):
        """
        Get members of groups with paginations
        # TODO: track defect. SPARK-322483 - Public Groups API Pagination Defect.
        """
        ga = self.api.groups
        group_list = list(ga.list(include_members=True))
        target_groups = [g for g in group_list if g.members]
        if not target_groups:
            self.skipTest('Need a group with members to run this test')
        with ThreadPoolExecutor() as pool:
            members = list(pool.map(lambda g: list(ga.members(group_id=g.group_id)),
                                    target_groups))
            members_w_pagination = list(pool.map(lambda g: list(ga.members(group_id=g.group_id, count=2)),
                                                 target_groups))
        requests = list(self.requests())
        print(f'Got members for {len(target_groups)} groups')
        self.assertEqual(members, members_w_pagination)

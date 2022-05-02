import random
from concurrent.futures import ThreadPoolExecutor

from .base import TestCaseWithLog
from wxc_sdk.groups import Group, GroupMember


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

    def test_003_pagination(self):
        """
        test pagination
        """
        ga = self.api.groups
        group_list = list(ga.list(include_members=True))
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
            with ThreadPoolExecutor() as pool:
                list(pool.map(lambda i: ga.create(settings=Group(display_name=next(new_names))),
                              range(missing)))
            # complete list of groups
            group_list = list(ga.list(include_members=True))

        # get list with pagination
        paginated_list = list(ga.list(count=5, include_members=True))
        try:
            self.assertEqual(group_list, paginated_list)
        except AssertionError:
            print(f'{group_list}')
            print(f'{paginated_list}')

    def test_004_all_details(self):
        """
        Get details for all groups
        """
        ga = self.api.groups
        group_list = list(ga.list(include_members=True))
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda group: ga.details(group_id=group.group_id, include_members=True),
                                    group_list))
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
        :return:
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
        print(f'Got members for {len(target_groups)} groups')
        self.assertEqual(members, members_w_pagination)

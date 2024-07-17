import json
from dataclasses import dataclass
from time import sleep

from tests.base import TestCaseWithUsers
from wxc_sdk.locations import Location
from wxc_sdk.people import Person
from wxc_sdk.telephony.jobs import MoveUsersList, MoveUser


@dataclass(init=False)
class TestMoveUsers(TestCaseWithUsers):
    locations: tuple[Location, Location] = None
    from_location: Location = None
    to_location: Location = None
    target_user: Person = None
    move_users: MoveUsersList = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        def get_location(name: str) -> Location:
            location = next((loc
                             for loc in cls.api.locations.list(name=name)
                             if loc.name == name),
                            None)
            return location

        cls.locations = tuple(get_location(name) for name in ('Hartford', 'Hartford New'))

    def setUp(self) -> None:
        super().setUp()
        if any(loc is None for loc in self.locations):
            self.fail('Not all locations found')
        # find Joe Garcia
        self.target_user = next(self.api.people.list(display_name='Jon Garcia',
                                                     callingData=True), None)
        if self.target_user is None:
            self.fail('User "Jon Garcia" not found')
        self.from_location = next((loc
                                   for loc in self.locations
                                   if loc.location_id == self.target_user.location_id),
                                  None)
        if self.from_location is None:
            self.fail('User "Jon Garcia" not in any of the locations')
        self.to_location = next((loc
                                 for loc in self.locations
                                 if loc.location_id != self.from_location.location_id),
                                None)
        print(f'Trying to move user "{self.target_user.display_name}" from "{self.from_location.name}" '
              f'to "{self.to_location.name}"')
        self.move_users = MoveUsersList(location_id=self.to_location.location_id,
                                        validate_only=True,
                                        users=[MoveUser(user_id=self.target_user.person_id,
                                                        extension=self.target_user.extension,
                                                        phone_number=(tn := self.target_user.tn) and tn.value)])
        return

    def test_validate_ok(self):
        """
        test to validate a user move
        """
        move_users = self.move_users.model_copy(deep=True)
        move_users.validate_only = True
        response = self.api.telephony.jobs.move_users.validate_or_initiate(users_list=move_users)
        print(json.dumps(response.model_dump(mode='json', by_alias=True), indent=2))
        self.assertTrue(response.users_list)
        self.assertIsNone(response.users_list[0].errors)
        self.assertTrue(response.users_list[0].impacts)

    def test_validate_failure(self):
        """
        test to validate a user move
        """
        to_location = next((loc for loc in self.api.locations.list()
                            if loc.location_id not in {self.from_location.location_id,
                                                       self.to_location.location_id}),
                           None)
        print(f'actually moving to {to_location.name}')
        move_users = self.move_users.model_copy(deep=True)
        move_users.location_id = to_location.location_id
        move_users.validate_only = True
        response = self.api.telephony.jobs.move_users.validate_or_initiate(users_list=move_users)
        print(json.dumps(response.model_dump(mode='json', by_alias=True), indent=2))
        self.assertTrue(response.users_list)
        self.assertTrue(response.users_list[0].errors)

    def test_move(self):
        """
        Test to actually move the user
        """
        move_users = self.move_users.model_copy(deep=True)
        move_users.validate_only = False
        api = self.api.telephony.jobs.move_users
        response = api.validate_or_initiate(users_list=move_users)
        print(json.dumps(response.model_dump(mode='json', by_alias=True), indent=2))

        # track the job until it is completed
        self.assertIsNotNone(response.job_details)
        job_id = response.job_details.id
        while True:
            status = api.status(job_id)
            print(json.dumps(status.model_dump(mode='json', by_alias=True, exclude_unset=True), indent=2))
            if status.latest_execution_status == 'COMPLETED':
                break
            print('Waiting for 10 seconds before checking again')
            sleep(10)
        print('Job completed')

        # download CSV with results
        download_url = status.csv_file_download_url
        print(f'Download the file from {download_url}')
        with api.session.get(download_url) as response:
            response.raise_for_status()
            print(response.text)

import random
from dataclasses import dataclass
from typing import ClassVar

from tests.base import TestWithTarget
from tests.test_workspace_settings import SelectiveAcceptTest, SelectiveRejectTest, SelectiveForwardTest
from tests.testutil import create_random_calling_user
from wxc_sdk.people import Person
from wxc_sdk.telephony.location import TelephonyLocation


@dataclass(init=False, repr=False)
class WithTempCallingUser(TestWithTarget):
    user: ClassVar[Person] = None

    @classmethod
    def setUpClass(cls) -> None:
        """
        create a random user and set it as target
        """
        super().setUpClass()
        location: TelephonyLocation = random.choice(cls.telephony_locations)
        cls.location_id = location.location_id
        cls.user = create_random_calling_user(api=cls.api, location_id=location.location_id)
        print(f'Created user {cls.user.display_name} in location {location.name}')
        cls.target_id = cls.user.person_id

    @classmethod
    def tearDownClass(cls):
        """
        delete the temp user again
        """
        cls.api.people.delete_person(cls.user.person_id)
        print(f'Deleted user {cls.user.display_name}')
        super().tearDownClass()


class SelectiveRejectTestUser(SelectiveRejectTest, WithTempCallingUser):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tapi = cls.api.person_settings.selective_reject


class SelectiveAcceptTestUser(SelectiveAcceptTest, WithTempCallingUser):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tapi = cls.api.person_settings.selective_accept


class SelectiveForwardTestUser(SelectiveForwardTest, WithTempCallingUser):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tapi = cls.api.person_settings.selective_forward

from tests.base import TestWithTempCallingUser
from tests.test_workspace_settings import SelectiveAcceptTest, SelectiveForwardTest, SelectiveRejectTest


class SelectiveRejectTestUser(SelectiveRejectTest, TestWithTempCallingUser):
    """
    Run the shared selective-reject CRUD tests against a disposable person.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Create the temp calling user and bind the person selective-reject API.
        """
        super().setUpClass()

        # Reuse the workspace selective test body with the person settings endpoint.
        cls.tapi = cls.api.person_settings.selective_reject


class SelectiveAcceptTestUser(SelectiveAcceptTest, TestWithTempCallingUser):
    """
    Run the shared selective-accept CRUD tests against a disposable person.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Create the temp calling user and bind the person selective-accept API.
        """
        super().setUpClass()

        # Reuse the workspace selective test body with the person settings endpoint.
        cls.tapi = cls.api.person_settings.selective_accept


class SelectiveForwardTestUser(SelectiveForwardTest, TestWithTempCallingUser):
    """
    Run the shared selective-forward CRUD tests against a disposable person.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Create the temp calling user and bind the person selective-forward API.
        """
        super().setUpClass()

        # Reuse the workspace selective test body with the person settings endpoint.
        cls.tapi = cls.api.person_settings.selective_forward

import asyncio
import os
from typing import Optional

import yaml
from dotenv import load_dotenv

from tests.base import TestCaseWithLog, async_test
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.integration import Integration
from wxc_sdk.people import Person
from wxc_sdk.scim.users import ScimUser
from wxc_sdk.tokens import Tokens


def get_tokens() -> Optional[Tokens]:
    """
    Get tokens to run a test

    Tokens are read from a YML file. If needed an OAuth flow is initiated.

    :return: tokens
    :rtype: Tokens
    """

    def env_path() -> str:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scim_service_app.env')
        return path

    def yml_path() -> str:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scim_service_app.yml')
        return path

    def read_tokens_from_file() -> Optional[Tokens]:
        """
        Get service app tokens from cache file, return None if cache does not exist
        """
        path = yml_path()
        if not os.path.isfile(path):
            return None
        try:
            with open(path, mode='r') as f:
                data = yaml.safe_load(f)
            tokens = Tokens.model_validate(data)
        except Exception:
            return None
        return tokens

    def write_tokens_to_file(tokens: Tokens):
        """
        Write tokens to cache
        """
        with open(yml_path(), mode='w') as f:
            yaml.safe_dump(tokens.model_dump(exclude_none=True), f)

    def get_access_token() -> Tokens:
        """
        Get a new access token using refresh token, service app client id, service app client secret
        """
        tokens = Tokens(refresh_token=os.getenv('SCIM_SERVICE_APP_REFRESH_TOKEN'))
        integration = Integration(client_id=os.getenv('SCIM_SERVICE_APP_CLIENT_ID'),
                                  client_secret=os.getenv('SCIM_SERVICE_APP_CLIENT_SECRET'),
                                  scopes=[], redirect_url=None)
        integration.refresh(tokens=tokens)
        write_tokens_to_file(tokens)
        return tokens

    load_dotenv(dotenv_path=env_path())
    # try to read from file
    tokens = read_tokens_from_file()
    # .. or create new access token using refresh token
    if tokens is None:
        tokens = get_access_token()
    if tokens.remaining < 24 * 60 * 60:
        tokens = get_access_token()
    return tokens


class TestWithScimToken(TestCaseWithLog):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # get service app tokens
        tokens = get_tokens()
        # replace session access token with service app access token
        cls.api.session._tokens.access_token = tokens.access_token


class TestScim(TestWithScimToken):
    def test_list(self):
        org_id = webex_id_to_uuid(self.me.org_id)
        users = self.api.scim.users.search(org_id=org_id)
        foo = 1

    @async_test
    async def test_details(self):
        org_id = webex_id_to_uuid(self.me.org_id)
        api = self.async_api.scim.users
        users = await api.search(org_id=org_id)
        details = await asyncio.gather(*[api.details(org_id=org_id, user_id=u.id)
                                         for u in users.resources], return_exceptions=True)

    @async_test
    async def test_sip_uris(self):
        """
        Verify that SCIM returns SIP URIs for users
        """
        users_with_uris = [user for user in self.api.people.list() if user.sip_addresses]
        if not users_with_uris:
            self.skipTest("No users with SIP addresses")

        # get SCIM details for all these users
        org_id = webex_id_to_uuid(self.me.org_id)
        scim_details = await asyncio.gather(
            *[self.async_api.scim.users.details(org_id=org_id, user_id=webex_id_to_uuid(u.person_id))
              for u in users_with_uris])
        scim_details: list[ScimUser]
        err = 0
        display_name_len = max(len(user.display_name) for user in users_with_uris)
        for user, scim_user in zip(users_with_uris, scim_details):
            user: Person
            scim_user: ScimUser
            if not scim_user.webex_user.sip_addresses:
                err += 1
                print(f'Webex user {user.display_name:{display_name_len}}: no SIP addresses in SCIMv2 info')

        self.assertFalse(err, f'{err}/{len(users_with_uris)} SCIMv2 users are missing SIP addresses')

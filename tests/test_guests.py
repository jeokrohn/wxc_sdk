"""
Tests for service app guests
"""
import json
import os
import uuid
from dataclasses import dataclass
from typing import ClassVar, Optional

import yaml
from pydantic import TypeAdapter, ValidationError

from tests.base import TestCaseWithLog
from wxc_sdk import WebexSimpleApi
from wxc_sdk.guests import Guest
from wxc_sdk.integration import Integration
from wxc_sdk.tokens import Tokens


def get_tokens() -> Optional[Tokens]:
    """
    Get guest token service app tokens

    Get tokens from cache or create new access token using service app credentials

    :return: tokens
    :rtype: Tokens
    """

    def yml_path() -> str:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'guest_service_token.yml')
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
        except:
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
        tokens = Tokens(refresh_token=os.getenv('GUEST_TOKEN_SERVICE_APP_REFRESH_TOKEN'))
        integration = Integration(client_id=os.getenv('GUEST_TOKEN_SERVICE_APP_CLIENT_ID'),
                                  client_secret=os.getenv('GUEST_TOKEN_SERVICE_APP_CLIENT_SECRET'),
                                  scopes=[], redirect_url=None)
        integration.refresh(tokens=tokens)
        write_tokens_to_file(tokens)
        return tokens

    # try to read from file
    tokens = read_tokens_from_file()
    # .. or create new access token using refresh token
    if tokens is None:
        tokens = get_access_token()
    if tokens.remaining < 24 * 60 * 60:
        tokens = get_access_token()
    return tokens


@dataclass(init=False)
class TestGuests(TestCaseWithLog):
    guest_service_api: ClassVar[WebexSimpleApi]
    guests: ClassVar[list[Guest]]

    @staticmethod
    def guest_list_path() -> str:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'guests.yml')
        return path

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # get tokens for guest token service app
        tokens = get_tokens()
        if tokens is None:
            cls.guest_service_api = None
        else:
            cls.guest_service_api = WebexSimpleApi(tokens=tokens)
        # read cached list of guests
        path = cls.guest_list_path()
        try:
            with open(path, mode='r') as f:
                cls.guests = TypeAdapter(list[Guest]).validate_python(yaml.safe_load(f))
        except (FileNotFoundError, ValidationError):
            cls.guests = list()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        path = cls.guest_list_path()
        with open(path, mode='w') as f:
            yaml.safe_dump(TypeAdapter(list[Guest]).dump_python(cls.guests, mode='json'), f)

    def setUp(self) -> None:
        super().setUp()
        self.assertTrue(self.guest_service_api is not None, 'No guest service app tokens')

    def test_001_create_guest(self):
        guest_id = str(uuid.uuid4())
        guest_count_before = self.guest_service_api.guests.guest_count()
        print(f'Guest count before creating guest: {guest_count_before}')
        guest = self.guest_service_api.guests.create(subject=f'subject-{guest_id}',
                                                     display_name=f'display-{guest_id}')
        self.guests.append(guest)
        guest_count_after = self.guest_service_api.guests.guest_count()
        print(f'Guest count after creating guest: {guest_count_after}')

        guest_access_token = guest.access_token
        with WebexSimpleApi(tokens=guest_access_token) as guest_api:
            guest_me = guest_api.people.me()
        print('Guest:')
        print(json.dumps(guest.model_dump(mode='json',
                                          by_alias=False,
                                          exclude_none=True,
                                          exclude_unset=True),
                         indent=2))
        print('-' * 80)
        print('Created user:')
        print(json.dumps(guest_me.model_dump(mode='json',
                                             by_alias=False,
                                             exclude_none=True,
                                             exclude_unset=True),
                         indent=2))
        self.assertEqual(guest_count_before + 1, guest_count_after, 'guest count mismatch')

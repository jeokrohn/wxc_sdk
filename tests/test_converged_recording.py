import json
import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Optional, ClassVar

import yaml
from dotenv import load_dotenv
from pydantic import TypeAdapter

from tests.base import TestCaseWithLog, WithIntegrationTokens
from wxc_sdk import WebexSimpleApi
from wxc_sdk.base import webex_id_to_uuid
from wxc_sdk.converged_recordings import ConvergedRecording, ConvergedRecordingMeta
from wxc_sdk.integration import Integration
from wxc_sdk.tokens import Tokens


@dataclass(init=False, repr=False)
class WithRecordingServiceApp(TestCaseWithLog):
    """
    Base class for tests that need to use the recording service app.
    Service app hase these scopes:
        * spark-compliance:webhooks_read
        * spark:kms
        * spark-admin:locations_read
        * spark:people_read
        * spark-compliance:webhooks_write
        * identity:people_read
        * spark-admin:telephony_config_read
        * spark-compliance:recordings_read
        * identity:people_rw
        * spark-admin:people_read
        * spark-compliance:recordings_write
    """
    test_api: ClassVar[WebexSimpleApi]
    token_identifier: ClassVar[str] = 'RECORDING_SERVICE_APP'
    recording_service_tokens: ClassVar[Tokens]
    recording_service_api: ClassVar[WebexSimpleApi]

    @staticmethod
    def get_tokens(token_identifier: str) -> Optional[Tokens]:
        """
        Get tokens to run a test

        Tokens are read from a YML file. If needed an OAuth flow is initiated.

        :return: tokens
        :rtype: Tokens
        """

        file_prefix = token_identifier.lower()
        env_var_prefix = token_identifier.upper()

        def env_path() -> str:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{file_prefix}.env')
            return path

        def yml_path() -> str:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{file_prefix}.yml')
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
            tokens = Tokens(refresh_token=os.getenv(f'{env_var_prefix}_REFRESH_TOKEN'))
            integration = Integration(client_id=os.getenv(f'{env_var_prefix}_CLIENT_ID'),
                                      client_secret=os.getenv(f'{env_var_prefix}_CLIENT_SECRET'),
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

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # get service app tokens
        cls.recording_service_tokens = cls.get_tokens(cls.token_identifier)

        # create API with standard token
        cls.recording_service_api = WebexSimpleApi(tokens=cls.recording_service_tokens.access_token)

    def setUp(self):
        super().setUp()
        self.har_writer.register_webex_api(self.recording_service_api)


    @property
    def org_id(self) -> str:
        return webex_id_to_uuid(self.me.org_id)


@dataclass(init=False, repr=False)
class TestConvergedRecording(WithRecordingServiceApp, WithIntegrationTokens):
    integration_api: ClassVar[WebexSimpleApi]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.integration_api = WebexSimpleApi(tokens=cls.integration_tokens)

    def setUp(self):
        super().setUp()
        self.har_writer.register_webex_api(self.integration_api)

    def test_list(self):
        api = self.recording_service_api
        recordings = list(api.converged_recordings.list())
        print(json.dumps(TypeAdapter(list[ConvergedRecording]).dump_python(recordings, mode='json', by_alias=True),
                         indent=2))

    def test_list_admin_or_compliance(self):
        """
        Get recordings via listfor admin or compliance office
        """
        api = self.integration_api
        recordings = list(api.converged_recordings.list_for_admin_or_compliance_officer(max=100))
        print(json.dumps(TypeAdapter(list[ConvergedRecording]).dump_python(recordings, mode='json', by_alias=True),
                         indent=2))

    def test_metadata(self):
        """
        Get metadata for all
        """
        api = self.integration_api
        recordings = list(api.converged_recordings.list_for_admin_or_compliance_officer(max=100))
        if not recordings:
            self.skipTest('No recordings found')
        # get metadata for all recordings
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(api.converged_recordings.metadata, (r.id for r in recordings)))

        print(json.dumps(TypeAdapter(list[ConvergedRecordingMeta]).dump_python(results, mode='json', by_alias=True),
                         indent=2))
        print(f'Got metadata for {len(results)} recordings')


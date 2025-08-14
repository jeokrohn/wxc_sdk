"""
base functions for unit tests
"""

import asyncio
import concurrent
import glob
import http.server
import json
import logging
import os
import random
import re
import socketserver
import threading
import time
import urllib.parse
import uuid
from collections import Counter
from collections.abc import Iterable, Generator
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from itertools import takewhile
from typing import Optional, Any, Union, ClassVar
from unittest import TestCase

import requests
import yaml
from dateutil import tz
from dotenv import load_dotenv
from pydantic import ValidationError, BaseModel, Field, model_validator, TypeAdapter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from yaml import safe_load
from yaml.scanner import ScannerError

load_dotenv()

from tests.testutil import create_workspace_with_webex_calling
from wxc_sdk import WebexSimpleApi
from wxc_sdk.all_types import Person
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.base import ApiModel
from wxc_sdk.common.schedules import Schedule, ScheduleType
from wxc_sdk.har_writer import HarWriter
from wxc_sdk.integration import Integration
from wxc_sdk.licenses import License
from wxc_sdk.locations import Location
from wxc_sdk.rooms import Room
from wxc_sdk.scopes import parse_scopes
from wxc_sdk.telephony.location import TelephonyLocation
from wxc_sdk.telephony.virtual_line import VirtualLine
from wxc_sdk.tokens import Tokens
from wxc_sdk.workspaces import Workspace, CallingType, WorkspaceSupportedDevices

log = logging.getLogger(__name__)

__all__ = ['TestCaseWithTokens', 'TestCaseWithLog', 'gather', 'TestWithLocations', 'TestCaseWithUsers', 'get_tokens',
           'async_test', 'LoggedRequest', 'TestCaseWithUsersAndSpaces', 'WithIntegrationTokens',
           'TestLocationsUsersWorkspacesVirtualLines', 'TestWithTarget', 'TestWithProfessionalWorkspace', 'UserTokens']

SKIP_TESTS_WITH_EXISTING_LOGS = False

def gather(mapping: Iterable[Any], return_exceptions: bool = False) -> Generator[Union[Any, Exception]]:
    """
    Gather results from a threading.map() call;  similar to asyncio.gather
    :param mapping: result of a threading.map() call
    :type mapping: Iterable[Any]
    :param return_exceptions: True: return exceptions; False: exceptions are raised
    :return: List of results
    """
    it = iter(mapping)
    while True:
        try:
            yield next(it)
        except StopIteration:
            break
        except Exception as e:
            if return_exceptions:
                yield e
            else:
                raise e


class AdminIntegration(Integration):
    """
    The integration we want to use to get tokens for the test cases
    """

    def __init__(self):
        """
        Integration parameters are read from environment variables
        """
        # get client id and client secret from .env in test directory
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path=dotenv_path)
        client_id = os.getenv('ADMIN_CLIENT_ID')
        client_secret = os.getenv('ADMIN_CLIENT_SECRET')
        scopes = parse_scopes(os.getenv('ADMIN_CLIENT_SCOPES'))
        if not all((client_id, client_secret, scopes)):
            raise ValueError('ADMIN_CLIENT_ID, ADMIN_CLIENT_SECRET, and ADMIN_CLIENT_SCOPES environment variables '
                             'required')
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
            redirect_url='http://localhost:6001/redirect')


def get_tokens() -> Optional[Tokens]:
    """
    Get tokens to run a test

    Tokens are read from a YML file. If needed an OAuth flow is initiated.

    :return: tokens
    :rtype: Tokens
    """

    def yml_path() -> str:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testtoken.yml')
        return path

    # noinspection PyShadowingNames
    def write_tokens(*, tokens: Tokens):
        with open(yml_path(), mode='w') as f:
            yaml.dump(json.loads(tokens.model_dump_json()), f)
        return

    # read tokens from file
    integration = AdminIntegration()
    try:
        with open(yml_path(), mode='r') as f:
            data = safe_load(f)
            tokens = Tokens.model_validate(data)
    except Exception as e:
        log.debug(f'failed to read tokens from file: {e}')
        tokens = None
    if tokens:
        # validate tokens
        tokens: Tokens
        changed = integration.validate_tokens(tokens=tokens)
        if not tokens.access_token:
            tokens = None
        elif changed:
            write_tokens(tokens=tokens)
    if not tokens:
        # get new tokens via integration if needed
        tokens = integration.get_tokens_from_oauth_flow()
        if tokens:
            tokens.set_expiration()
            write_tokens(tokens=tokens)
    return tokens


@dataclass(init=False, repr=False)
class TestCaseWithTokens(TestCase):
    """
    A test case that requires access tokens to run
    """
    api: ClassVar[WebexSimpleApi]
    me: ClassVar[Person]
    tokens: ClassVar[Tokens]
    async_api: AsWebexSimpleApi = field(default=None)

    # use proxy for all requests
    proxy: ClassVar[bool] = False
    proxy_url: ClassVar[str] = 'http://localhost:9090'

    def setup_async(self):
        """
        Anchor for pre async test actions
        """
        pass

    def shutdown_async(self):
        """
        Anchor for post async test actions
        """
        pass

    @staticmethod
    def async_test(as_test):
        """
        Decorator to run async tests
        also initializes the async_api attribute
        """

        @wraps(as_test)
        def run_async_test(test_self: TestCaseWithTokens):
            async def prepare_and_run():
                if test_self.proxy:
                    proxy = test_self.proxy_url
                else:
                    proxy = None
                async with AsWebexSimpleApi(tokens=test_self.tokens, proxy_url=proxy, ssl=False) as async_api:
                    test_self.async_api = async_api
                    test_self.setup_async()
                    await as_test(test_self)
                    test_self.shutdown_async()

            asyncio.run(prepare_and_run())

        return run_async_test

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        tokens = get_tokens()
        cls.tokens = tokens
        if tokens:
            if cls.proxy:
                proxy_url = cls.proxy_url
                verify = False
            else:
                proxy_url = None
                verify = None
            cls.api = WebexSimpleApi(tokens=tokens, proxy_url=proxy_url, verify=verify)
            cls.me = cls.api.people.me()
        else:
            cls.api = None

    def setUp(self) -> None:
        self.assertTrue(self.tokens and self.api, 'Failed to obtain tokens')
        self.assertEqual(ApiModel.Config.extra, 'forbid', 'API_MODEL_ALLOW_EXTRA must be set to "forbid"')
        random.seed()


async_test = TestCaseWithTokens.async_test


@dataclass(init=False, repr=False)
class WithIntegrationTokens(TestCase):
    integration_token_identifier: ClassVar[str] = 'TEST_INTEGRATION'
    integration_tokens: ClassVar[Tokens]

    @classmethod
    def build_integration(cls) -> Integration:
        """
        read integration parameters from environment variables and create an integration
        """
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            f'{cls.integration_token_identifier.lower()}.env')
        load_dotenv(path)

        client_id = os.getenv(f'{cls.integration_token_identifier}_CLIENT_ID')
        client_secret = os.getenv(f'{cls.integration_token_identifier}_CLIENT_SECRET')
        scopes = parse_scopes(os.getenv(f'{cls.integration_token_identifier}_CLIENT_SCOPES'))
        redirect_url = 'http://localhost:6001/redirect'
        if not all((client_id, client_secret, scopes)):
            raise ValueError('failed to get integration parameters from environment')
        return Integration(client_id=client_id, client_secret=client_secret, scopes=scopes,
                           redirect_url=redirect_url)

    @classmethod
    def get_integration_tokens(cls) -> Optional[Tokens]:
        """

        Tokens are read from a YML file. If needed an OAuth flow is initiated.

        :return: tokens
        :rtype: :class:`wxc_sdk.tokens.Tokens`
        """

        integration = cls.build_integration()
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            f'{cls.integration_token_identifier.lower()}.yml')
        tokens = integration.get_cached_tokens_from_yml(yml_path=path)
        return tokens

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # get service app tokens
        cls.integration_tokens = cls.get_integration_tokens()


# noinspection DuplicatedCode


class LoggedRequest(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    method: str
    url: str
    status: int
    response: str
    time_ms: float
    parsed_url: Optional[urllib.parse.ParseResult] = None
    url_query: dict = Field(default_factory=dict)
    url_dict: Optional[dict] = None  # groupdict() of match on url_filter if one was provided
    #: request headers
    headers: Optional[dict] = None
    #: request body
    request_body: Optional[Union[dict, str]] = None
    #: response headers
    response_headers: Optional[dict] = None
    #: response body
    response_body: Optional[Union[dict, str]] = None
    record: logging.LogRecord

    # regular expressions to match on reqeust record
    request_record: ClassVar[re.Pattern] = re.compile(r"""
        ^Request\s              # keyword at start of line
        (?P<status>\d{3})       # three digti status code
        \[(?P<response>[\w\s]+)]    # HTTP response string in squared brackets
        \s*\((?P<time_ms>\d+\.\d+)\sms\):\s     # response time in ms
        (?P<method>\w+)\s       # HTTP methods
        (?P<url>\S+)$           # url is the rest of the line""", re.VERBOSE + re.MULTILINE)
    header_line: ClassVar[re.Pattern] = re.compile(r'\s+(?P<header>.+): (?P<value>.+)$')
    response_line: ClassVar[re.Pattern] = re.compile(r'^\s+Response')
    body_line: ClassVar[re.Pattern] = re.compile(r'\s*-+\s*response body')
    end_line: ClassVar[re.Pattern] = re.compile(r'\s*-+\s*end\s*')

    @model_validator(mode='before')
    def validate_all(cls, values):
        """
        Validator to populate request, parse the message and set some additional attributes
        """
        parsed_url = urllib.parse.urlparse(values['url'])
        values['parsed_url'] = parsed_url
        if parsed_url.query:
            values['url_query'] = urllib.parse.parse_qs(parsed_url.query)
        record: logging.LogRecord = values.get('record', None)
        if record is None:
            # we are done here
            return
        lines = iter(record.message.splitlines())
        # skip 1st line (already parsed)
        next(lines)
        headers = {}
        while header := cls.header_line.match((line := next(lines))):
            headers[header['header'].capitalize()] = header['value']
        values['headers'] = headers

        # we are either at the response line or need to parse the body
        if line.strip() == '--- body ---':
            # collect everything until Response line
            ct = headers['Content-type']
            if ct.startswith('application/json'):
                body = '\n'.join(takewhile(lambda l: not cls.response_line.match(l),
                                           lines))
                values['request_body'] = json.loads(body)
            elif ct.startswith('application/x-www-form-urlencoded'):
                values['request_body'] = {header['header']: header['value']
                                          for line in takewhile(lambda l: not cls.response_line.match(l),
                                                                lines)
                                          if (header := cls.header_line.match(line))}
            else:
                values['request_body'] = '\n'.join(takewhile(lambda l: not cls.response_line.match(l),
                                                             lines))

        # now we are at the response line
        values['response_headers'] = {header['header'].capitalize(): header['value']
                                      for line in takewhile(lambda l: not cls.body_line.match(l),
                                                            lines)
                                      if (header := cls.header_line.match(line))}

        # there might be a response body
        body = '\n'.join(takewhile(lambda l: not cls.end_line.match(l),
                                   lines))
        if body:
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                pass
        values['response_body'] = body or None

        return values

    @classmethod
    def from_records(cls, records: list[logging.LogRecord], method: str = None,
                     url_filter: Union[str, re.Pattern] = None) -> Generator['LoggedRequest', None, None]:
        """
        Generate LoggedRequest objects from a list of LogRecords
        :param records:
        :param method: method filter
        :param url_filter: filter for request URLs
        :return:
        """
        records = iter(records)

        # compile if a string is provided, else keep the value provided (Pattern or None)
        url_filter = isinstance(url_filter, str) and re.compile(url_filter) or url_filter

        for record in records:
            if not (request := cls.request_record.match(record.message)) or \
                    (method and method != request['method']) or \
                    (url_filter and not (url := url_filter.match(request['url']))):
                # not a request, wrong method or url doesn't match
                continue
            # noinspection PyUnboundLocalVariable
            yield LoggedRequest(**request.groupdict(),
                                record=record,
                                url_dict=url_filter and url.groupdict())


class RecordHandler(logging.Handler):
    """
    Primitive handler to collect log records
    """

    def __init__(self, *, level: Union[int, str] = logging.NOTSET):
        super().__init__(level=level)
        self.records: list[logging.LogRecord] = list()

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)

    def requests(self, method: str = None,
                 url_filter: Union[str, re.Pattern] = None) -> Generator[LoggedRequest, None, None]:
        """
        Generator for logged requests
        :param method:
        :param url_filter:
        :return:
        """
        yield from LoggedRequest.from_records(records=self.records, method=method, url_filter=url_filter)


@dataclass(init=False, repr=False)
class TestCaseWithLog(TestCaseWithTokens):
    """
    Test case with automatic logging
    """
    log_path: str = field(default=None)
    file_log_handler: logging.Handler = field(default=None)
    record_log_handler: RecordHandler = field(default=None)

    # write HAR file as well?
    with_har: ClassVar[bool] = True
    har_writer: HarWriter = field(default=None)
    # registration id if async API was registered with HARWriter
    async_api_reg_id: Optional[str] = field(default=None)

    rest_logger_names = ['wxc_sdk.rest', 'wxc_sdk.as_rest', 'webexteamsasyncapi.rest']

    def log_name(self, prefix: str, test_case_id: str) -> str:
        """
        Get the name for the next REST logfile
        Log file format: '{prefix}_{index:03d}_{test_case_id}'

        :param prefix:
        :param test_case_id:
        :return: path of log file
        """
        # all logs are in the logs directory below the directory of this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.join(base_dir, 'logs')
        os.makedirs(base_dir, exist_ok=True)

        # get all existing files in that directory, basename only (w/o path)
        logs = glob.glob(os.path.join(base_dir, f'{prefix}_*.log'))
        logs = list(map(os.path.basename, logs))

        # sort files and only look for files matching the log filename structure
        logs_re = re.compile(r'rest_(?P<index>\d{4})_(?P<test_id>.+).log')
        logs.sort()
        # noinspection PyShadowingNames
        logs = [log
                for log in logs
                if logs_re.match(log)]

        existing_test_ids = set(logs_re.match(log).group('test_id') for log in logs)
        if SKIP_TESTS_WITH_EXISTING_LOGS and test_case_id in existing_test_ids:
            self.skipTest(f'Log file already exists for test case {test_case_id}')

        # next log file index is based on index of last log file in the list
        if not logs:
            next_log_index = 1
        else:
            m = logs_re.match(logs[-1])
            next_log_index = int(m.group('index')) + 1

        # build the log file name
        # noinspection PyShadowingNames
        log = os.path.join(base_dir,
                           f'{prefix}_{next_log_index:04d}_{test_case_id}.log')
        return log

    def setUp(self) -> None:
        super().setUp()
        print(f'{self.__class__.__name__}.setUp() in TestCaseWithLog.setUp()')
        test_case_id = self.id()

        # we always want to have REST logging into a file
        self.log_path = self.log_name(prefix='rest', test_case_id=test_case_id)
        file_handler = logging.FileHandler(filename=self.log_path)
        file_handler.setLevel(logging.DEBUG)
        file_fmt = logging.Formatter(fmt='%(asctime)s %(threadName)s %(message)s')
        file_fmt.converter = time.gmtime
        file_handler.setFormatter(file_fmt)
        self.file_log_handler = file_handler

        self.record_log_handler = RecordHandler(level=logging.DEBUG)

        # also create a HAR file?
        self.async_api_reg_id = None
        if self.with_har:
            self.har_writer = HarWriter(path=self.log_path.replace('.log', '.har'),
                                        api=self.api)

        # enable debug logging on the REST loggers
        for rest_logger_name in self.rest_logger_names:
            rest_logger = logging.getLogger(rest_logger_name)
            rest_logger.setLevel(logging.DEBUG)
            rest_logger.addHandler(file_handler)
            rest_logger.addHandler(self.record_log_handler)

    def tearDown(self) -> None:
        super().tearDown()
        print(f'{self.__class__.__name__}.tearDown() in TestCaseWithLog.teardown()')

        if self.file_log_handler is not None:
            # close REST file handler and remove from REST logger
            for rest_logger_name in self.rest_logger_names:
                rest_logger = logging.getLogger(rest_logger_name)
                rest_logger.removeHandler(self.file_log_handler)
                rest_logger.removeHandler(self.record_log_handler)

            if self.har_writer:
                self.har_writer.close()
                self.har_writer = None

            self.file_log_handler.close()
            self.file_log_handler = None
            self.record_log_handler.close()

    def setup_async(self):
        """
        when running async test also register the async API with an existing HAR writer
        """
        if self.har_writer:
            self.async_api_reg_id = self.har_writer.register_as_webex_api(self.async_api)

    def shutdown_async(self):
        """
        After running an async test unregister the async api from the HARWriter again
        """
        if self.har_writer and self.async_api_reg_id is not None:
            self.har_writer.unregister_api(self.async_api_reg_id)
            self.async_api_reg_id = None

    @contextmanager
    def no_log(self, keep: bool = False):
        """
        Context manager to temporarily disable logging
        """
        if keep:
            yield
            return

        old_level = None
        if self.file_log_handler:
            old_level = self.file_log_handler.level
            self.file_log_handler.setLevel(logging.INFO)

        if self.har_writer:
            har_active_before = self.har_writer.active
            self.har_writer.active = False
        else:
            har_active_before = None
        try:
            yield
        finally:
            if old_level:
                self.file_log_handler.setLevel(old_level)
            if har_active_before is not None:
                self.har_writer.active = har_active_before

    @contextmanager
    def with_log(self):
        """
        Context manager to temporarily (re-)enable logging
        """
        old_level = self.file_log_handler.level
        self.file_log_handler.setLevel(logging.DEBUG)

        if self.har_writer:
            har_active_before = self.har_writer.active
            self.har_writer.active = True
        else:
            har_active_before = None

        try:
            yield
        finally:
            if self.file_log_handler:
                self.file_log_handler.setLevel(old_level)
            if har_active_before is not None:
                self.har_writer.active = har_active_before

    def requests(self, method: str = None,
                 url_filter: Union[str, re.Pattern] = None) -> Generator[LoggedRequest, None, None]:
        """
        Generator for requests logged during the test
        :param method: request method, GET, POST, ...
        :param url_filter: filter for URls, can be a string or a compiled pattern
        :return: yields logged requests
        """
        return LoggedRequest.from_records(self.record_log_handler.records, method=method, url_filter=url_filter)

    def print_request_stats(self):
        """
        print some request stats
        """
        long_word = re.compile(r'/\w{20,}/?')

        def url_key(url: str) -> str:
            # remove long words (probably IDs?) from URL
            url = long_word.sub('', url)
            return url.split('?')[0]

        url_counters = Counter((url_key(request.url), request.method, request.status)
                               for request in self.requests())

        for url_and_method in sorted(url_counters, key=lambda k: url_counters[k]):
            print(f'{url_and_method}: {url_counters[url_and_method]} requests')


@dataclass(init=False, repr=False)
class TestWithLocations(TestCaseWithLog):
    """
    Test cases with existing locations
    """
    locations: ClassVar[list[Location]]
    telephony_locations: ClassVar[list[TelephonyLocation]]

    @classmethod
    def setUpClass(cls) -> None:
        """
        Get list of calling locations
        """
        super().setUpClass()

        async def get_calling_locations() -> list[Location]:
            async with AsWebexSimpleApi(tokens=cls.tokens) as api:
                locations = await api.locations.list()
                # figure out which locations are calling locations
                details = await asyncio.gather(*[api.telephony.location.details(location_id=loc.location_id)
                                                 for loc in locations], return_exceptions=True)
            validation_error = next((d for d in details if isinstance(d, ValidationError)), None)
            if validation_error is not None:
                raise validation_error

            # the calling locations are the ones for which we can actually get calling details
            result = [(loc, detail) for loc, detail in zip(locations, details)
                      if not isinstance(detail, Exception)]
            cls.locations, cls.telephony_locations = list(zip(*result))
            return

        if cls.api is None:
            cls.locations = None
            cls.telephony_locations = None
            return
        asyncio.run(get_calling_locations())

    def setUp(self) -> None:
        """
        Check if we have locations, Skip test if we don't have locations
        """
        super().setUp()
        if not self.locations:
            self.skipTest('Need at least ohe location to run test.')


class UserCache(BaseModel):
    last_access: datetime = Field(default_factory=lambda: datetime.now(tz=tz.UTC))
    users: list[Person] = Field(default_factory=list)
    licenses: list[License] = Field(default_factory=list)

    @property
    def needs_validation(self) -> bool:
        """
        cache needs validation if it has been longer than 5 minutes since we last used the cache
        """
        seconds_since_last_access = (datetime.now(tz=tz.UTC) - self.last_access).total_seconds()
        return seconds_since_last_access > 300


@dataclass(init=False, repr=False)
class TestCaseWithUsers(TestCaseWithLog):
    users: ClassVar[list[Person]]

    @staticmethod
    def user_cache_path() -> str:
        path = os.path.join(os.path.dirname(__file__), 'user_cache.yml')
        return path

    @classmethod
    def users_from_cache(cls) -> UserCache:
        try:
            with open(cls.user_cache_path(), mode='r') as f:
                cache = TypeAdapter(UserCache).validate_python(yaml.safe_load(f))
            return cache
        except (FileNotFoundError, ValidationError, ScannerError):
            return UserCache()

    @classmethod
    def dump_users(cls, cache: UserCache):
        cache.last_access = datetime.now(tz=tz.UTC)
        with open(cls.user_cache_path(), mode='w') as f:
            yaml.safe_dump(json.loads(cache.model_dump_json()), f)

    @classmethod
    def setUpClass(cls) -> None:
        """
        initialize cls.users with list of calling users. Try to read users from cache since it takes FOREVER to list
        users with calling data.
        """
        super().setUpClass()
        print('Getting users...')

        USE_CACHE = False
        if not USE_CACHE:
            users = list(cls.api.people.list(calling_data=True))
            licenses = list(cls.api.licenses.list())
            calling_license_ids = set(lic.license_id
                                      for lic in licenses
                                      if lic.webex_calling)

            # pick the calling enabled users
            cls.users = [user
                         for user in users
                         if (set(user.licenses) & calling_license_ids)]
        else:
            # read users from cache
            user_cache = cls.users_from_cache()
            if user_cache.needs_validation or not user_cache.users or not user_cache.licenses:
                # get licenses
                user_cache.licenses = list(cls.api.licenses.list())
                # getting users w/o calling data is relatively fast. Look at that list for validation
                user_dict = {user.person_id: user for user in cls.api.people.list()}
                user_dict: dict[str, Person]

                # all users from cache still exist and licenses have not changed?
                if user_cache.users and all((user := user_dict.get(cu.person_id)) and user.licenses == cu.licenses
                                            for cu in user_cache.users):
                    pass
                else:
                    # update cache
                    if False:
                        # maybe getting details for all users is faster than listing...
                        with ThreadPoolExecutor() as pool:
                            user_cache.users = list(pool.map(lambda user: cls.api.people.details(person_id=user.person_id,
                                                                                                 calling_data=True),
                                                             user_dict.values()))
                    else:
                        # bite the bullet: list users with calling data --> slooooooowww
                        user_cache.users = list(cls.api.people.list(calling_data=True))
            cls.dump_users(cache=user_cache)

            # select users with a webex calling license
            calling_license_ids = set(lic.license_id
                                      for lic in user_cache.licenses
                                      if lic.webex_calling)

            # pick the calling enabled users
            cls.users = [user
                         for user in user_cache.users
                         if any(lic_id in calling_license_ids for lic_id in user.licenses)]
        print(f'got {len(cls.users)} users')

    def setUp(self) -> None:
        super().setUp()
        if not self.users:
            self.skipTest('Need at least one calling user to run test')


@dataclass(init=False, repr=False)
class TestCaseWithUsersAndSpaces(TestCaseWithLog):
    users: ClassVar[list[Person]]
    spaces: ClassVar[list[Room]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        me = cls.api.people.me()
        cls.users = [u for u in cls.api.people.list() if u.person_id != me.person_id]
        cls.spaces = [r for r in cls.api.rooms.list()
                      if re.match(r'Test Space \d{3}', r.title)]

    def setUp(self) -> None:
        super().setUp()
        if not self.spaces:
            self.skipTest('No target spaces')

    @contextmanager
    def target_space(self) -> Room:
        target = random.choice(self.spaces)
        try:
            yield target
        finally:
            ...


@dataclass(init=False, repr=False)
class TestLocationsUsersWorkspacesVirtualLines(TestWithLocations, TestCaseWithUsers):
    """
    Base class for test cases related to outgoing permissions
    make sure we have calling locations, persons, calling workspaces, and virtual lines ready to test
    """

    workspaces: ClassVar[list[Workspace]]
    virtual_lines: ClassVar[list[VirtualLine]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        async def setup():
            async with AsWebexSimpleApi(tokens=cls.api.session.access_token) as api:
                cls.workspaces, cls.virtual_lines = await asyncio.gather(api.workspaces.list(),
                                                                         api.telephony.virtual_lines.list())
            # find calling workspaces
            cls.workspaces = [ws for ws in cls.workspaces
                              if ws.calling and ws.calling.type == CallingType.webex]

        asyncio.run(setup())

    def setUp(self) -> None:
        if not all((self.workspaces, self.virtual_lines)):
            self.skipTest('No workspaces or virtual lines')
        super().setUp()


@dataclass(init=False, repr=False)
class TestWithTarget(TestWithLocations):
    target_id: ClassVar[str] = None
    location_id: ClassVar[str] = None

    def setUp(self) -> None:
        if self.target_id is None:
            self.skipTest(f'No target_id set. {self.__class__.__name__} might be an abstract test class?')
        super().setUp()

    @classmethod
    def assert_location(cls):
        """
        make sure that location_id is set
        """
        if cls.location_id is None:
            location = random.choice(cls.locations)
            cls.location_id = location.location_id
        return

    @contextmanager
    def with_schedule(self) -> Schedule:
        """
        get or create a schedule for the test
        """
        self.assert_location()
        with self.no_log():
            schedules = list(self.api.telephony.schedules.list(self.location_id))
        if False and schedules:
            temp_schedule: Schedule = random.choice(schedules)
            yield temp_schedule
        else:
            # create a temporary schedule for the test
            print('creating temporary schedule for the test')
            temp_schedule = Schedule.business('test schedule')
            with self.no_log():
                schedule_id = self.api.telephony.schedules.create(self.location_id, temp_schedule)
            try:
                yield temp_schedule
            finally:
                with self.no_log():
                    print('deleting temporary schedule')
                    self.api.telephony.schedules.delete_schedule(self.location_id,
                                                                 schedule_type=ScheduleType.business_hours,
                                                                 schedule_id=schedule_id)
        return


@dataclass(init=False, repr=False)
class TestWithProfessionalWorkspace(TestWithTarget):
    """
    Tests for workspace settings using a temporary professional workspace
    """
    # temporary workspace with professional license
    workspace: ClassVar[Workspace] = None
    location: ClassVar[Location] = None

    @classmethod
    def create_temp_workspace(cls):
        """
        Create a temporary workspace with professional license
        """
        # get pro license
        pro_license = next((lic
                            for lic in cls.api.licenses.list()
                            if lic.webex_calling_professional and lic.consumed_units < lic.total_units),
                           None)
        if pro_license:
            pro_license: License
            # create WS in random location
            location = random.choice(cls.locations)
            cls.location_id = location.location_id
            cls.location = location
            workspace = create_workspace_with_webex_calling(api=cls.api,
                                                            target_location=location,
                                                            # workspace_location_id=wsl.id,
                                                            supported_devices=WorkspaceSupportedDevices.phones,
                                                            notes=f'temp location for professional workspace tests, '
                                                                  f'location "{location.name}"',
                                                            license=pro_license)
            cls.workspace = workspace
            cls.target_id = workspace.workspace_id

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.create_temp_workspace()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if cls.workspace:
            cls.api.workspaces.delete_workspace(cls.workspace.workspace_id)

    def setUp(self) -> None:
        super().setUp()
        self.assertIsNotNone(self.workspace, 'No professional workspace created')


TokenCache = TypeAdapter(dict[str, Tokens])


@dataclass(init=False, repr=False)
class UserTokens(TestCaseWithLog):
    """
    Base class for tests that need user tokens
    """

    # cache with tokens for each user indexed by user_id
    _token_cache: ClassVar[dict[str, Tokens]] = {}

    _cache_file: ClassVar[str] = 'user_tokens.yml'

    # prefix for environment variables _CLIENT_ID, _CLIENT_SECRET, _CLIENT_SCOPES
    _env_prefix: ClassVar[str] = 'TEST_USER_'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # read token cache from file
        cls.read_and_validate_user_cache()
        return

    def setUp(self) -> None:
        super().setUp()
        # make sure that environment variables are set
        for env_var in ('CLIENT_ID', 'CLIENT_SECRET', 'SCOPES', 'PASSWORD'):
            if not os.getenv(self._env_prefix + env_var):
                self.skipTest(f'Need environment variable {self._env_prefix + env_var} to run test')
        return

    @classmethod
    def build_integration(cls) -> Integration:
        """
        Build integration
        """
        client_id = os.getenv(cls._env_prefix + 'CLIENT_ID')
        client_secret = os.getenv(cls._env_prefix + 'CLIENT_SECRET')
        scopes = os.getenv(cls._env_prefix + 'SCOPES')

        # scopes is the full URL; we need the redirect URI
        parsed = urllib.parse.urlparse(scopes)
        query = parsed.query

        # try to parse the query and get the redirect URI
        parsed_query = urllib.parse.parse_qs(query)
        redirect_uri = parsed_query.get('redirect_uri')[0]

        # also get the scopes
        scopes = parse_scopes(scopes)
        integration = Integration(client_id=client_id, client_secret=client_secret, scopes=scopes,
                                  redirect_url=redirect_uri)
        return integration

    @classmethod
    def write_user_cache(cls):
        with open(cls._cache_file, 'w') as f:
            yaml.dump(TokenCache.dump_python(cls._token_cache, mode='json'), f)
        return

    @classmethod
    def read_and_validate_user_cache(cls):
        """
        Read token cache from file and validate tokens
        """
        try:
            with open(cls._cache_file, 'r') as f:
                data = yaml.safe_load(f)
                cls._token_cache = TokenCache.validate_python(data)
        except FileNotFoundError:
            cls._token_cache = {}

        # check remaining lifetime and refresh/regenerate tokens if needed
        integration = cls.build_integration()
        updated = False
        for user_id, tokens in cls._token_cache.items():
            if tokens.remaining < 24 * 60 * 60:
                updated = True
                # we need to refresh or try to get new tokens
                try:
                    integration.refresh(tokens)
                except requests.HTTPError:
                    tokens = cls.create_user_tokens(user_id=user_id)
                if tokens is None or not tokens.access_token:
                    # remove user from cache
                    cls._token_cache.pop(user_id)
        if updated:
            cls.write_user_cache()
        return

    @classmethod
    def get_user_tokens(cls, user_id: str) -> Tokens:
        """
        Get tokens for user:
            * from cache
            * or via OAuth flow
        """
        tokens = cls._token_cache.get(user_id)
        if not tokens:
            tokens = cls.create_user_tokens(user_id=user_id)
            cls._token_cache[user_id] = tokens
            cls.write_user_cache()
        return tokens

    @classmethod
    def create_user_tokens(cls, user_id: str) -> Optional[Tokens]:
        """
        Create tokens for user
        """

        def serve_redirect():
            """
            Temporarily start a web server to serve the redirect URI at http://localhost:6001/redirect'
            :return: parses query of the GET on the redirect URI
            """

            # mutable to hold the query result
            oauth_response = dict()

            class RedirectRequestHandler(http.server.BaseHTTPRequestHandler):
                # handle the GET request on the redirect URI

                # noinspection PyPep8Naming
                def do_GET(self):
                    # serve exactly one GET on the redirect URI and then we are done

                    parsed = urllib.parse.urlparse(self.path)
                    if parsed.path == '/redirect':
                        log.debug('serve_redirect: got GET on /redirect')
                        query = urllib.parse.parse_qs(parsed.query)
                        oauth_response['query'] = query
                        # we are done
                        self.shutdown(self.server)
                    self.send_response(200)
                    self.flush_headers()

                @staticmethod
                def shutdown(server: socketserver.BaseServer):
                    log.debug('serve_redirect: shutdown of local web server requested')
                    threading.Thread(target=server.shutdown, daemon=True).start()

            httpd = http.server.HTTPServer(server_address=('', 6001),
                                           RequestHandlerClass=RedirectRequestHandler)
            log.debug('serve_redirect: starting local web server for redirect URI')
            httpd.serve_forever()
            httpd.server_close()
            log.debug(f'serve_redirect: server terminated, result {oauth_response["query"]}')
            return oauth_response['query']

        def browser_auth_flow(url: str, cred_email: str, cred_password: str):
            """
            Drive a user auth flow in Chrome
            """
            # start OAuth flow
            web_driver = webdriver.Chrome()
            web_driver.get(url)

            email = WebDriverWait(driver=web_driver, timeout=10).until(
                method=EC.visibility_of_element_located((By.ID, 'IDToken1'))
            )
            email.send_keys(cred_email)

            # wait for "Sign In" button
            sign_in = WebDriverWait(driver=web_driver, timeout=10).until(
                method=EC.element_to_be_clickable((By.ID, 'IDButton2')))
            sign_in.click()
            password = WebDriverWait(driver=web_driver, timeout=10).until(
                method=EC.visibility_of_element_located((By.ID, 'IDToken2')))
            password.send_keys(cred_password)

            # wait for "Sign In" button
            sign_in = WebDriverWait(driver=web_driver, timeout=10).until(
                method=EC.element_to_be_clickable((By.ID, 'Button1')))
            sign_in.click()

            # unselect userGrantCheckBox
            user_grant_checkbox = WebDriverWait(driver=web_driver, timeout=10).until(
                method=EC.element_to_be_clickable((By.ID, 'userGrantCheckBox')))
            user_grant_checkbox.click()

            # click "Accept" button
            accept = WebDriverWait(driver=web_driver, timeout=10).until(
                method=EC.element_to_be_clickable((By.NAME, 'accept')))
            accept.click()
            return

        user = cls.api.people.details(user_id)
        user_email = user.emails[0]
        user_password = os.getenv(cls._env_prefix + 'PASSWORD')

        integration = cls.build_integration()

        with ThreadPoolExecutor() as executor:
            # start web server
            fut = executor.submit(serve_redirect)

            # driver auth flow in Chrome
            oauth_state = str(uuid.uuid4())
            oauth_url = integration.auth_url(state=oauth_state)
            browser_auth_flow(oauth_url, user_email, user_password)

            try:
                result = fut.result(timeout=10)
            except concurrent.futures.TimeoutError:
                # noinspection PyBroadException
                try:
                    # post a dummy response to the redirect URI to stop the server
                    with requests.Session() as session:
                        session.get(integration.redirect_url, params={'code': 'foo'})
                except Exception:
                    pass
                log.warning('Authorization did not finish in time (60 seconds)')
                return

        # get the authorization code from the response
        code = result['code'][0]
        response_state = result['state'][0]
        if response_state != oauth_state:
            log.error('Authorization code from response does not match authorization code from request')
            return

        # get access tokens
        new_tokens = integration.tokens_from_code(code=code)
        if new_tokens is None:
            log.error('Failed to obtain tokens')
            return None
        return new_tokens

"""
base functions for unit tests
"""
import asyncio
import concurrent.futures
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
import webbrowser
from collections.abc import Iterable, Generator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from typing import Optional, Any, Union, ClassVar
from unittest import TestCase

import requests
import yaml
from dotenv import load_dotenv
from pydantic import parse_obj_as, ValidationError, BaseModel, Field
from yaml import safe_load
from yaml.scanner import ScannerError

from wxc_sdk import WebexSimpleApi
from wxc_sdk.all_types import Person
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.integration import Integration
from wxc_sdk.licenses import License
from wxc_sdk.locations import Location
from wxc_sdk.scopes import parse_scopes
from wxc_sdk.tokens import Tokens

log = logging.getLogger(__name__)

__all__ = ['TestCaseWithTokens', 'TestCaseWithLog', 'gather', 'TestWithLocations', 'TestCaseWithUsers', 'get_tokens']


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


def get_tokens_from_oauth_flow(integration: Integration) -> Optional[Tokens]:
    """
    Initiate an OAuth flow to obtain new tokens.

    start a local webserver on port 6001 o serve the last step in the OAuth flow

    :param integration: Integration to use for the flow
    :type: Integration
    :return: set of new tokens if successful, else None
    :rtype: Tokens
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

    state = str(uuid.uuid4())
    auth_url = integration.auth_url(state=state)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # start web server
        fut = executor.submit(serve_redirect)

        webbrowser.open(auth_url)
        # wait for GET on redirect URI and get the result (parsed query of redirect URI)
        try:
            result = fut.result(timeout=120)
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

    code = result['code'][0]
    response_state = result['state'][0]
    assert response_state == state

    # get access tokens
    new_tokens = integration.tokens_from_code(code=code)
    if new_tokens is None:
        log.error('Failed to obtain tokens')
        return None
    return new_tokens


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

    def write_tokens(*, tokens: Tokens):
        with open(yml_path(), mode='w') as f:
            yaml.dump(json.loads(tokens.json()), f)
        return

    # read tokens from file
    integration = AdminIntegration()
    try:
        with open(yml_path(), mode='r') as f:
            data = safe_load(f)
            tokens = Tokens.parse_obj(data)
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
        tokens = get_tokens_from_oauth_flow(integration=integration)
        if tokens:
            tokens.set_expiration()
            write_tokens(tokens=tokens)
    return tokens


class TestCaseWithTokens(TestCase):
    api: Optional[WebexSimpleApi]
    me: Optional[Person]
    tokens: Optional[Tokens]
    async_api: Optional[AsWebexSimpleApi]
    """
    A test case that required access tokens to run
    """

    class wrapper:
        pass

    def async_test(async_test):
        """
        Decorator to run async tests
        also initializes the async_api attribute
        :return:
        """

        @wraps(async_test)
        def run_async_test(test_self: TestCaseWithTokens):
            async def prepare_and_run():
                async with AsWebexSimpleApi(tokens=test_self.tokens) as async_api:
                    test_self.async_api = async_api
                    await async_test(test_self)

            asyncio.run(prepare_and_run())

        return run_async_test

    @classmethod
    def setUpClass(cls) -> None:
        tokens = get_tokens()
        cls.tokens = tokens
        if tokens:
            cls.api = WebexSimpleApi(tokens=tokens)
            cls.me = cls.api.people.me()
        else:
            cls.api = None

    def setUp(self) -> None:
        self.assertTrue(self.tokens and self.api, 'Failed to obtain tokens')
        random.seed()


def log_name(prefix: str, test_case_id: str) -> str:
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
    logs_re = re.compile(r'rest_(?P<index>\d{3})_(?P<test_id>.+).log')
    logs.sort()
    logs = [log
            for log in logs
            if logs_re.match(log)]

    # next log file index is based on index of last log file in the list
    if not logs:
        next_log_index = 1
    else:
        m = logs_re.match(logs[-1])
        next_log_index = int(m.group('index')) + 1

    # build the log file name
    log = os.path.join(base_dir,
                       f'{prefix}_{next_log_index:03d}_{test_case_id}.log')
    return log


@dataclass(init=False)
class TestCaseWithLog(TestCaseWithTokens):
    """
    Test case with automatic logging
    """
    log_path: str
    file_log_handler: Optional[logging.Handler]

    rest_logger_names = ['wxc_sdk.rest', 'wxc_sdk.as_rest', 'webexteamsasyncapi.rest']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # this can be reused for other logging to the same file
        self.file_log_handler = None

    def setUp(self) -> None:
        super().setUp()
        print(f'{self.__class__.__name__}.setUp() in TestCaseWithLog.setUp()')
        test_case_id = self.id()

        # we always want to have REST logging into a file
        self.log_path = log_name(prefix='rest', test_case_id=test_case_id)
        file_handler = logging.FileHandler(filename=self.log_path)
        file_handler.setLevel(logging.DEBUG)
        file_fmt = logging.Formatter(fmt='%(asctime)s %(threadName)s %(message)s')
        file_fmt.converter = time.gmtime
        file_handler.setFormatter(file_fmt)
        self.file_log_handler = file_handler

        # enable debug logging on the REST loggers
        for rest_logger_name in self.rest_logger_names:
            rest_logger = logging.getLogger(rest_logger_name)
            rest_logger.setLevel(logging.DEBUG)
            rest_logger.addHandler(file_handler)

    def tearDown(self) -> None:
        super().tearDown()
        print(f'{self.__class__.__name__}.tearDown() in TestCaseWithLog.teardown()')

        # close REST file handler and remove from REST logger
        for rest_logger_name in self.rest_logger_names:
            rest_logger = logging.getLogger(rest_logger_name)
            rest_logger.removeHandler(self.file_log_handler)

        self.file_log_handler.close()
        self.file_log_handler = None


@dataclass(init=False)
class TestWithLocations(TestCaseWithLog):
    """
    Test cases with existing locations
    """
    locations: list[Location]

    @classmethod
    def setUpClass(cls) -> None:
        """
        Get list of locations
        """
        super().setUpClass()
        if cls.api is None:
            cls.locations = None
            return
        cls.locations = list(cls.api.locations.list())

    def setUp(self) -> None:
        """
        Check if we have locations, Skip test if we don't have locations
        """
        super().setUp()
        if not self.locations:
            self.skipTest('Need at least ohe location to run test.')


class UserCache(BaseModel):
    last_access: datetime = Field(default_factory=datetime.utcnow)
    users: list[Person] = Field(default_factory=list)
    licenses: list[License] = Field(default_factory=list)

    @property
    def needs_validation(self) -> bool:
        """
        cache needs validation if is has been longer than 5 minutes since we last used the cache
        """
        seconds_since_last_access = (datetime.utcnow() - self.last_access).total_seconds()
        return seconds_since_last_access > 300


@dataclass(init=False)
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
                cache = parse_obj_as(UserCache, yaml.safe_load(f))
            return cache
        except (FileNotFoundError, ValidationError, ScannerError):
            return UserCache()

    @classmethod
    def dump_users(cls, cache: UserCache):
        cache.last_access = datetime.utcnow()
        with open(cls.user_cache_path(), mode='w') as f:
            yaml.safe_dump(json.loads(cache.json()), f)

    @classmethod
    def setUpClass(cls) -> None:
        """
        initialize cls.users with list of calling users. Try to read users from cache since it takes FOREVER to list
        users with calling data.
        """
        super().setUpClass()
        print('Getting users...')

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

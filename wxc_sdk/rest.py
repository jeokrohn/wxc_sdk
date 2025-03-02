"""
REST session for Webex API requests
"""
import json
import logging
import time
import uuid
from collections.abc import Generator
from dataclasses import dataclass
from functools import wraps
from io import TextIOBase, StringIO
from json import JSONDecodeError
from threading import Semaphore
from typing import Tuple, Type, Optional, ClassVar, Callable, Union
from urllib.parse import parse_qsl

from pydantic import BaseModel, ValidationError, Field
from requests import HTTPError, Response, Session
from requests.adapters import HTTPAdapter
from requests.models import PreparedRequest

from .base import ApiModel, StrOrDict, RETRY_429_MAX_WAIT
from .tokens import Tokens

__all__ = ['SingleError', 'ErrorDetail', 'RestError', 'RestSession', 'dump_response']

log = logging.getLogger(__name__)


class SingleError(BaseModel):
    """
    Representation of single error in the body of an HTTP error response from Webex
    """
    description: str
    error_code: Optional[int] = Field(alias='errorCode', default=None)

    @property
    def code(self) -> Optional[int]:
        """
        Error code or None

        :return: error code
        """
        return self.error_code


class ErrorDetail(ApiModel):
    """
    Representation of error details in the body of an HTTP error response from Webex
    """
    error_code: Optional[int] = Field(alias='errorCode', default=None)
    message: str  #: error message
    errors: Optional[list[SingleError]] = None  #: list of errors; typically has a single entry
    tracking_id: str  #: tracking ID of the request

    @property
    def description(self) -> str:
        """
        error description

        """
        return self.errors and self.errors[0].description or ''

    @property
    def code(self) -> Optional[int]:
        """
        error code

        """
        return self.errors and self.errors[0].code or None


class RestError(HTTPError):
    """
    A REST error
    """
    request: PreparedRequest
    response: Response

    def __init__(self, msg: str, response: Response):
        super().__init__(msg, response=response)
        # try to parse the body of the API response
        try:
            self.detail = ErrorDetail.model_validate(json.loads(response.text))
        except (json.JSONDecodeError, ValidationError):
            self.detail = response.text

    def __str__(self):
        desc = self.description
        if desc:
            if self.code:
                desc = f', {self.code} {desc}'
            else:
                desc = f', {desc}'
        else:
            desc = ''
        return f'{super().__str__()}{desc}'

    @property
    def description(self) -> str:
        """
        error description

        """
        if isinstance(self.detail, str):
            return self.detail
        self.detail: ErrorDetail
        return self.detail and self.detail.description or ''

    @property
    def code(self) -> str:
        """
        error code

        """
        return self.detail and isinstance(self.detail, ErrorDetail) and self.detail.code or 0


def dump_response(response: Response, file: TextIOBase = None, dump_log: logging.Logger = None, diff_ns: int = None):
    """
    Dump response object to log file

    :param response: HTTP request response
    :param file: stream to dump to
    :type file: TextIOBase
    :param dump_log: logger to dump to
    :type dump_log: logging.Logger
    :param diff_ns: time the request took (in ns)
    :type diff_ns: int
    """
    if not log.isEnabledFor(logging.DEBUG):
        return
    dump_log = dump_log or log
    output = file or StringIO()

    # dump response objects in redirect history
    for h in response.history:
        dump_response(response=h, file=output)

    if diff_ns is None:
        time_str = ''
    else:
        time_str = f'({diff_ns / 1000000.0:.3f} ms)'

    print(f'Request {response.status_code}[{response.reason}]{time_str}: '
          f'{response.request.method} {response.request.url}', file=output)

    # request headers
    for k, v in response.request.headers.items():
        if k.lower() == 'authorization':
            v = 'Bearer ***'
        print(f'  {k}: {v}', file=output)

    # request body
    request_body = response.request.body
    if request_body:
        print('  --- body ---', file=output)
        ct = response.request.headers.get('Content-Type').lower()
        if ct.startswith('application/json'):
            for line in json.dumps(json.loads(request_body), indent=2).splitlines():
                print(f'  {line}', file=output)
        elif ct.startswith('application/x-www-form-urlencoded'):
            for k, v in parse_qsl(request_body):
                print(f'  {k}: {"***" if k in {"client_secret", "refresh_token"} else v}',
                      file=output)
        else:
            print(f'  {request_body}', file=output)

    print(' Response', file=output)
    # response headers
    for k in response.headers:
        print(f'  {k}: {response.headers[k]}', file=output)
    body = response.text
    # dump response body
    if body:
        print('  --- response body ---', file=output)
        try:
            body = json.loads(body)
            if isinstance(body, dict):
                # mask access and refresh tokens
                if 'access_token' in body:
                    # mask access token
                    body['access_token'] = '***'
                if 'refresh_token' in body:
                    body['refresh_token'] = '***'
            body = json.dumps(body, indent=2)
        except json.JSONDecodeError:
            pass
        for line in body.splitlines():
            print(f'  {line}', file=output)
    print(' ---- end ----', file=output)
    if file is None:
        dump_log.debug(output.getvalue())


def retry_request(func):
    """
    Decorator for the request method in the RestSession class. Used to implement backoff on 429 responses

    :param func:
    :return:
    """

    def giveup_429(e: RestError, retry_429: bool) -> bool:
        """
        callback for backoff on REST requests

        :param e: latest exception
        :param retry_429: retry on 429?
        :return: True -> break the backoff loop
        """
        response = e.response
        response: Response
        if response.status_code != 429 or not retry_429:
            # Don't retry on anything other than 429
            return True

        # determine how long we have to wait
        retry_after = int(response.headers.get('Retry-After', 5))

        # never wait more than the defined maximum
        retry_after = min(retry_after, RETRY_429_MAX_WAIT)
        time.sleep(retry_after)
        return False

    @wraps(func)
    def wrapper(session: 'RestSession', *args, **kwargs):
        with session._sem:
            while True:
                try:
                    result = func(session, *args, **kwargs)
                except RestError as e:
                    if giveup_429(e, session.retry_429):
                        raise
                else:
                    break
        return result

    return wrapper


# Callback for response logging
# callbacks get called with the response object and the time the request took
RestResponseCallBack = Callable[[Response, int], None]


def _dump_response_callback(response: Response, diff_ns: int):
    dump_response(response, diff_ns=diff_ns)


@dataclass(init=False, repr=False)
class RestSession(Session):
    """
    REST session used for API requests:
        * includes an Authorization header in reach request
        * implements retries on 429
        * loads deserializes JSON data if needed
    """
    #: base URL for all Webex API requests
    BASE: ClassVar[str] = 'https://webexapis.com/v1'

    # Bearer token(s) for this session
    _tokens: Tokens
    # semaphore for rate limiting
    _sem: Semaphore
    # retry on 429?
    retry_429: bool
    # registry of response callbacks
    _response_callback_registry: dict[str, RestResponseCallBack]

    def __init__(self, *, tokens: Tokens, concurrent_requests: int, retry_429: bool = True,
                 proxy_url: str = None, verify: Union[bool, str] = None):
        super().__init__()
        self.mount('http://', HTTPAdapter(pool_maxsize=concurrent_requests))
        self.mount('https://', HTTPAdapter(pool_maxsize=concurrent_requests))
        self._tokens = tokens
        self._sem = Semaphore(concurrent_requests)
        self.retry_429 = retry_429
        self._response_callback_registry = dict()
        self.register_response_callback(_dump_response_callback)
        if proxy_url:
            self.proxies = {'https': proxy_url}
        if verify is not None:
            self.verify = verify

    def register_response_callback(self, callback: RestResponseCallBack) -> str:
        """
        Register a response callback

        Registered response callbacks are called with the response object and the time the request took for all
        responses. This can be used for logging or other purposes.

        :param callback: callback to register
        :return: callback ID
        """
        id = str(uuid.uuid4())
        self._response_callback_registry[id] = callback
        return id

    def unregister_response_callback(self, id: str):
        """
        Unregister a response callback

        :param id: callback ID
        """
        self._response_callback_registry.pop(id, None)

    def ep(self, path: str = None):
        """
        get an API endpoint

        :meta private:
        :param path:
        :return: full endpoint
        """
        path = path and f'/{path}' or ''
        return f'{self.BASE}{path}'

    @property
    def access_token(self) -> str:
        """
        access token used for all requests

        :return: access token
        :rtype: str
        """
        return self._tokens.access_token

    @retry_request
    def _request_w_response(self, method: str, url: str, headers=None, content_type: str = None,
                            **kwargs) -> Tuple[Response, StrOrDict]:
        """
        low level API REST request with support for 429 rate limiting

        :param method: HTTP method
        :type method: str
        :param url: URL
        :type url: str
        :param headers: prepared headers for request
        :type headers: Optional[dict]
        :param content_type:
        :type content_type: str
        :param kwargs: additional keyword args
        :type kwargs: dict
        :return: Tuple of response object and body. Body can be text or dict (parsed from JSON body)
        :rtype:
        """
        request_headers = {'Authorization': f'Bearer {self._tokens.access_token}',
                           'Content-Type': 'application/json;charset=utf-8',
                           'TrackingID': f'SIMPLE_{uuid.uuid4()}'}
        if headers:
            request_headers.update((k.lower(), v) for k, v in headers.items())
        if content_type:
            request_headers['Content-Type'] = content_type
        start = time.perf_counter_ns()
        response = self.request(method, url=url, headers=request_headers, **kwargs)
        diff_ns = time.perf_counter_ns() - start
        try:
            # relay response to all registered callbacks
            for callback in self._response_callback_registry.values():
                callback(response, diff_ns)
            try:
                response.raise_for_status()
            except HTTPError as error:
                # create a RestError based on HTTP error
                error = RestError(error.args[0], response=error.response)
                raise error
            # get response body as text or dict (parsed JSON)
            ct = response.headers.get('Content-Type')
            if not ct:
                data = ''
            elif ct.startswith('application/json') and response.text:
                try:
                    data = response.json()
                except JSONDecodeError:
                    data = response.text
            else:
                data = response.text
        finally:
            response.close()
        return response, data

    def _rest_request(self, method: str, url: str, **kwargs) -> StrOrDict:
        """
        low level API request only returning the body

        :param method: HTTP method
        :type method: str
        :param url: URL
        :type url: str
        :param headers: prepared headers for request
        :type headers: Optional[dict]
        :param kwargs: additional keyward args
        :type kwargs: dict
        :return: body. Body can be text or dict (parsed from JSON body)
        :rtype: Unon
        """
        _, data = self._request_w_response(method, url=url, **kwargs)
        return data

    def rest_get(self, *args, **kwargs) -> StrOrDict:
        """
        GET request

        :param args:
        :param kwargs:
        :return: deserialized JSON content or body text
        """
        return self._rest_request('GET', *args, **kwargs)

    def rest_post(self, *args, **kwargs) -> StrOrDict:
        """
        POST request

        :param args:
        :param kwargs:
        :return: deserialized JSON content or body text
        """
        return self._rest_request('POST', *args, **kwargs)

    def rest_put(self, *args, **kwargs) -> StrOrDict:
        """
        PUT request

        :param args:
        :param kwargs:
        :return: deserialized JSON content or body text
        """
        return self._rest_request('PUT', *args, **kwargs)

    def rest_delete(self, *args, **kwargs) -> StrOrDict:
        """
        DELETE request

        :param args:
        :param kwargs:
        """
        return self._rest_request('DELETE', *args, **kwargs)

    def rest_patch(self, *args, **kwargs) -> StrOrDict:
        """
        PATCH request

        :param args:
        :param kwargs:
        """
        return self._rest_request('PATCH', *args, **kwargs)

    def follow_pagination(self, url: str, model: Type[ApiModel] = None,
                          params: dict = None, item_key: str = None, **kwargs) -> Generator[ApiModel, None, None]:
        """
        Handling RFC5988 pagination of list requests. Generator of parsed objects

        :param url: start url for 1st GET
        :type url: str
        :param model: data type to return
        :type model: ApiModel
        :param params: URL parameters, optional
        :type params: Optional[dict]
        :param item_key: key to list of values
        :type item_key: str
        :return: yields parsed objects
        """

        def noop(x):
            return x

        if model is None or not issubclass(model, ApiModel):
            model = noop
        else:
            model = model.model_validate

        while url:
            # not needed any more, WXCAPIBULK-27 has been fixed
            # if url.startswith('https,'):
            #     url = url[6:]
            log.debug(f'{self.__class__.__name__}.pagination: getting {url}')
            response, data = self._request_w_response('GET', url=url, params=params, **kwargs)
            # params only in first request. In subsequent requests we rely on the completeness of the 'next' URL
            params = None
            # try to get the next page (if present)
            try:
                url = str(response.links['next']['url'])
            except KeyError:
                url = None
            if not data:
                continue
            # return all items
            if item_key is None:
                if 'items' in data:
                    item_key = 'items'
                else:
                    # we go w/ the first return value that is a list
                    item_key = next((k for k, v in data.items()
                                     if isinstance(v, list)))
            items = data.get(item_key, [])
            for item in items:
                yield model(item)

import base64
import datetime
import json
import urllib.parse
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from io import TextIOBase
from typing import Union

from aiohttp import ClientResponse
from requests import Response

import wxc_sdk
from wxc_sdk import WebexSimpleApi
from wxc_sdk.as_api import AsWebexSimpleApi


@dataclass(init=False)
class HarWriter:
    """
    log WebexSimpleApi and AsWebexSimpleApi requests and responses to HAR files
    """
    #: flag to indicate if the writer is active
    active: bool
    #: stream to write HAR data to
    _iostream: TextIOBase
    #: flag to indicate if the stream must be closed when done
    _must_close: bool
    #: list of HAR requests to put into the HAR file
    _har_entries: list[dict]
    #: callables to unregister callbacks
    _unregister_callbacks: list[Callable]

    def __init__(self, path: Union[str, TextIOBase], api: Union[WebexSimpleApi, AsWebexSimpleApi]):
        self.active = True
        if isinstance(path, str):
            self._iostream = open(path, 'w')
            self._must_close = True
        else:
            self._iostream = path
            self._must_close = False
        self._har_entries = []
        self._unregister_callbacks = []
        # register request/response hooks
        if isinstance(api, WebexSimpleApi):
            self.register_webex_api(api)
        else:
            raise NotImplementedError('only WebexSimpleApi is supported')

    def register_webex_api(self, api: WebexSimpleApi):
        """
        Register response callback for WebexSimpleApi

        :param api:
        """
        id = api.session.register_response_callback(self._on_webex_response)
        self._unregister_callbacks.append(partial(api.session.unregister_response_callback, id))

    def register_as_webex_api(self, api: AsWebexSimpleApi):
        """
        Register response callback for WebexSimpleApi

        :param api:
        """
        id = api.session.register_response_callback(self._on_as_webex_response)
        self._unregister_callbacks.append(partial(api.session.unregister_response_callback, id))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        # unregister callbacks
        for unregister in self._unregister_callbacks:
            unregister()
        self._unregister_callbacks = []
        self._write_har()

        # close IO stream if necessary
        if self._iostream is None:
            return  # already closed

        if self._must_close:
            self._iostream.close()
        self._iostream = None

    @staticmethod
    def _query_string(url: str):
        """
        build HAR query string from URL
        """
        parsed_url = urllib.parse.urlparse(url)
        if query := parsed_url.query:
            qsl = urllib.parse.parse_qsl(query)
            query = [{'name': k, 'value': v} for k, v in qsl]
        else:
            query = []
        return query

    def _on_webex_response(self, response: Response, diff_ns: int):
        """
        Callback for WebexSimpleApi responses
        """
        if not self.active:
            # don't record this request
            return

        # build and store HAR request from response

        def content():
            if not response.content:
                return {}
            ct = response.headers.get('Content-Type')
            if ct == 'application/json':
                return {
                    'size': len(response.content),
                    "text": base64.b64encode(response.text.encode()).decode(),
                    "encoding": "base64",
                    'mimeType': ct,
                }
            raise ValueError(f'unsupported content type: {ct}')

        def post_data():
            body = response.request.body
            if not body:
                return {}
            try:
                body = body.decode()
            except AttributeError:
                pass
            return {
                'size': len(body),
                "text": body,
                'mimeType': response.headers.get('Content-Type', 'application/json'),
            }

        self._har_entries.append({
            'request': {
                'method': response.request.method,
                'url': response.request.url,
                'httpVersion': 'HTTP/1.1',
                'cookies': [],
                'headers': [{'name': k, 'value': v} for k, v in response.request.headers.items()],
                'queryString': self._query_string(response.request.url),
                'postData': post_data(),
                'headersSize': -1,
                'bodySize': response.request.body and len(response.request.body) or -1,
            },
            'response': {
                'status': response.status_code,
                'statusText': response.reason,
                'httpVersion': 'HTTP/1.1',
                'cookies': [],
                'headers': [{'name': k, 'value': v} for k, v in response.headers.items()],
                'content': content(),
                'redirectURL': '',
                'headersSize': -1,
                'bodySize': response.content and len(response.content) or -1,
            },
            'startedDateTime': f'{datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z',
            'time': diff_ns / 1_000_000,
            'cache': {},
            'timings': {
                'wait': -1,
                'blocked': -1,
                'receive': -1,
                'dns': -1,
                'connect': 1,
                'send': -1,
                'ssl': -1
            }
        })

    def _on_as_webex_response(self, response: ClientResponse, request_body: str, request_ct: str,
                              response_data: Union[str, dict], diff_ns: int):
        def post_data():
            body = request_body
            if not body:
                return {}
            try:
                body = body.decode()
            except AttributeError:
                pass
            return {
                'size': len(body),
                "text": body,
                'mimeType': request_ct,
            }

        def content():
            if not response_data:
                return {}
            ct = response.headers.get('Content-Type')
            if ct == 'application/json':
                return {
                    'size': len(response_data_str),
                    "text": base64.b64encode(response_data_str.encode()).decode(),
                    "encoding": "base64",
                    'mimeType': ct,
                }
            raise ValueError(f'unsupported content type: {ct}')

        if isinstance(response_data, dict):
            response_data_str = json.dumps(response_data)
        else:
            response_data_str = response_data

        self._har_entries.append({
            'request': {
                'method': response.request_info.method,
                'url': str(response.request_info.url),
                'httpVersion': 'HTTP/1.1',
                'cookies': [],
                'headers': [{'name': k, 'value': v} for k, v in response.request_info.headers.items()],
                'queryString': self._query_string(str(response.request_info.url)),
                'postData': post_data(),
                'headersSize': -1,
                'bodySize': request_body and len(request_body) or -1,
            },
            'response': {
                'status': response.status,
                'statusText': response.reason,
                'httpVersion': 'HTTP/1.1',
                'cookies': [],
                'headers': [{'name': k, 'value': v} for k, v in response.headers.items()],
                'content': content(),
                'redirectURL': '',
                'headersSize': -1,
                'bodySize': response_data_str and len(response_data_str) or -1,
            },
            'startedDateTime': f'{datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z',
            'time': diff_ns / 1_000_000,
            'cache': {},
            'timings': {
                'wait': -1,
                'blocked': -1,
                'receive': -1,
                'dns': -1,
                'connect': 1,
                'send': -1,
                'ssl': -1
            }
        })

    def _write_har(self):
        # write HAR file
        data = {"log": {"version": "1.2",
                        "creator": {"name": "wxc_sdk", "version": wxc_sdk.__version__},
                        "entries": self._har_entries}}
        self._iostream.write(json.dumps(data, indent=2))
        pass

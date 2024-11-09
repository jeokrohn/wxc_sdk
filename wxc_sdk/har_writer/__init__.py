import json
import logging
import urllib.parse
from collections.abc import Callable
from dataclasses import dataclass
from io import TextIOBase
from typing import Union

from aiohttp import ClientResponse
from requests import Response

import wxc_sdk
from wxc_sdk import WebexSimpleApi
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.har_writer.har import HAREntry, HARRequest, HARResponse, HARLog, HARCreator, HAR

__all__ = ['HarWriter']

log = logging.getLogger(__name__)


@dataclass(init=False)
class HarWriter:
    """
    log WebexSimpleApi and AsWebexSimpleApi requests and responses to HAR files
    """
    #: flag to indicate if the writer is active
    active: bool
    #: flag to indicate if the writer should include authorization headers
    with_authorization: bool
    #: stream to write HAR data to
    _iostream: TextIOBase
    #: flag to indicate if the stream must be closed when done
    _must_close: bool
    #: HAR log
    _har: HAR
    #: dictionary of unregister callbacks indexed by registration id
    _unregister_callbacks: dict[tuple[str, Callable]]

    def __init__(self, path: Union[str, TextIOBase], api: Union[None, WebexSimpleApi, AsWebexSimpleApi],
                 with_authorization: bool = False):
        self.active = True
        self.with_authorization = with_authorization
        if isinstance(path, str):
            self._iostream = open(path, 'w')
            self._must_close = True
        else:
            self._iostream = path
            self._must_close = False
        self._har = HAR(log=HARLog(version='1.2', creator=HARCreator(name='wxc_sdk', version=wxc_sdk.__version__)))
        self._unregister_callbacks = dict()
        # register request/response hooks
        if isinstance(api, WebexSimpleApi):
            self.register_webex_api(api)
        elif isinstance(api, AsWebexSimpleApi):
            self.register_as_webex_api(api)

    def unregister_api(self, reg_id: str):
        """
        unregister an API using an id returned by register_webex_api(), or register_as_webex_api()

        :param reg_id: registration id
        """
        unregister_callback = self._unregister_callbacks[reg_id]
        unregister_callback(reg_id)

    def register_webex_api(self, api: WebexSimpleApi) -> str:
        """
        Register response callback for WebexSimpleApi

        returns a registration id that can be used to unregister an API via unregister_api()
        :param api:
        """
        reg_id = api.session.register_response_callback(self._on_webex_response)
        self._unregister_callbacks[reg_id] = api.session.unregister_response_callback
        return reg_id

    def register_as_webex_api(self, api: AsWebexSimpleApi) -> str:
        """
        Register response callback for WebexSimpleApi

        :param api:
        """
        reg_id = api.session.register_response_callback(self._on_as_webex_response)
        self._unregister_callbacks[reg_id] = api.session.unregister_response_callback
        return reg_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        # unregister callbacks
        for reg_id, unregister in self._unregister_callbacks.items():
            unregister(reg_id)
        self._unregister_callbacks = dict()
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
        try:
            new_entry = HAREntry(request=HARRequest(method=response.request.method,
                                                    url=response.request.url,
                                                    headers=response.request.headers,
                                                    postData=response.request.body,
                                                    httpVersion=response.raw.version_string,
                                                    with_authorization=self.with_authorization),
                                 response=HARResponse(status=response.status_code,
                                                      statusText=response.reason,
                                                      httpVersion=response.raw.version_string,
                                                      headers=response.headers,
                                                      content_str=response.content.decode()),
                                 time=diff_ns / 1_000_000)
        except Exception as e:
            log.error(f'Error creating HAR entry: {e}')
        else:
            self._har.log.entries.append(new_entry)

    def _on_as_webex_response(self, response: ClientResponse, request_body: Union[str, bytes], request_ct: str,
                              response_data: Union[str, dict], diff_ns: int):
        """
        Callback for AsWebexSimpleApi responses
        """

        if not self.active:
            # don't record this request
            return

        if not response_data:
            response_data_str = ''
        elif isinstance(response_data, str):
            response_data_str = response_data
        else:
            response_data_str = json.dumps(response_data)
        http_version = f'HTTP/{response.version.major}.{response.version.minor}'
        try:
            new_entry = HAREntry(request=HARRequest(method=response.request_info.method,
                                                    url=str(response.request_info.url),
                                                    headers=response.request_info.headers,
                                                    postData=request_body,
                                                    httpVersion=http_version,
                                                    with_authorization=self.with_authorization),
                                 response=HARResponse(status=response.status,
                                                      statusText=response.reason,
                                                      httpVersion=http_version,
                                                      headers=response.headers,
                                                      content_str=response_data_str),
                                 time=diff_ns / 1_000_000)
        except Exception as e:
            log.error(f'Error creating HAR entry: {e}')
        else:
            self._har.log.entries.append(new_entry)

    def _write_har(self):
        # write HAR file
        data = self._har.model_dump()
        self._iostream.write(json.dumps(data, indent=2))

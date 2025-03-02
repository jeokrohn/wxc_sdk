import json
import logging
import re
from collections.abc import Callable
from dataclasses import dataclass
from io import TextIOBase
from typing import Union, Optional

from aiohttp import ClientResponse
from requests import Response

import wxc_sdk
from wxc_sdk import WebexSimpleApi
from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.har_writer.har import HAREntry, HARRequest, HARResponse, HARLog, HARCreator, HAR

__all__ = ['HarWriter']

log = logging.getLogger(__name__)


@dataclass(init=False, repr=False)
class HarWriter:
    """
    log WebexSimpleApi and AsWebexSimpleApi requests and responses to HAR files
    """
    #: flag to indicate if the writer is active
    active: bool
    #: flag to indicate if the writer should include authorization headers
    with_authorization: bool
    #: HAR log
    har: HAR
    #: stream to write HAR data to
    _iostream: TextIOBase
    #: flag to indicate if the stream must be closed when done
    _must_close: bool
    #: callables to unregister callbacks
    _unregister_callbacks: list[Callable]
    #: path parameter
    _path: Union[None, str, TextIOBase]
    #: dictionary of unregister callbacks indexed by registration id
    _unregister_callbacks: dict[tuple[str, Callable]]
    #: iostream to write to, only used for incremental writer
    _iostream: Optional[TextIOBase]
    #: incremental writer
    _incremental: bool
    _incremental_first_entry: bool
    _incremental_trailer: str

    def __init__(self, path: Union[None, str, TextIOBase] = None,
                 api: Union[WebexSimpleApi, AsWebexSimpleApi] = None,
                 with_authorization: bool = False,
                 incremental: bool = False):
        """
        Create a new HAR writer

        :param path: path to HAR file or stream to write HAR data to. Can be None to disable writing to a file. The
            recorded HAR data can be retrieved from the `har` attribute.
        :param api: API object to record requests and responses from. If additional API instances (for example a sync
            and an async API) need to be recorded then additional API instances can be registered using
            the :meth:`register_webex_api` and :meth:`register_as_webex_api` method.
        :param with_authorization: flag to indicate if the writer should include authorization headers
        :param incremental: write each request to HAR file incrementally instead of only when closing the HarWriter
        """
        self.active = True
        self.with_authorization = with_authorization
        self._path = path
        self._unregister_callbacks = dict()

        # register request/response hooks
        if isinstance(api, WebexSimpleApi):
            self.register_webex_api(api)
        elif isinstance(api, AsWebexSimpleApi):
            self.register_as_webex_api(api)

        har_instance = HAR(log=HARLog(version='1.2',
                                      creator=HARCreator(name='wxc_sdk',
                                                         version=wxc_sdk.__version__),
                                      entries=[]))
        self._incremental = incremental
        if self._incremental:
            # open stream if needed
            self._set_or_open_iostream()
            self.har = None
            # write start of HAR
            json_str = har_instance.model_dump_json(exclude_none=True)
            m = re.match(r'^(.+"entries":\s*\[)(].+)$', json_str, flags=re.DOTALL)
            if self._iostream is not None:
                self._iostream.write(m.group(1))
            self._incremental_trailer = m.group(2)
            self._incremental_first_entry = True
        else:
            # don't open any file, just keep HAR object so that we can keep track of entries
            self.har = har_instance
            self._iostream = None
        return

    def unregister_api(self, reg_id: str):
        """
        unregister an API using an id returned by register_webex_api(), or register_as_webex_api()

        :param reg_id: registration id
        """
        unregister_callback = self._unregister_callbacks.pop(reg_id, None)
        if unregister_callback is not None:
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

    def _set_or_open_iostream(self) -> TextIOBase:
        if isinstance(self._path, str):
            self._iostream = open(self._path, 'w')
        else:
            self._iostream = self._path

    def new_entry(self, entry: HAREntry):
        """
        Log new entry either by adding to entries of HAR object or by writing to IOStream directly
        """
        if self._incremental:
            # write json representation of entry to HAR file
            json_str = entry.model_dump_json(exclude_none=True)
            if not self._incremental_first_entry:
                json_str = f',{json_str}'
            self._incremental_first_entry = False
            self._iostream.write(json_str)
        else:
            # append entry
            self.har.log.entries.append(entry)

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
            self.new_entry(new_entry)

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
            self.new_entry(new_entry)

    def _write_har(self):
        """
        Write full HAR file or trailer for incremental HAR writer
        """
        if self._incremental:
            # write closing part of HAR
            if self._iostream is not None:
                self._iostream.write(self._incremental_trailer)
        else:
            # for non-incremental writer open HAR file at the end
            self._set_or_open_iostream()
            # write full HAR
            if self._iostream is not None:
                self._iostream.write(self.har.model_dump_json(exclude_none=True))
        if isinstance(self._path, str):
            self._iostream.close()
        self._iostream = None

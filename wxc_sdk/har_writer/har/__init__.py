"""
HAR file format models, based on the HAR 1.2 spec, http://www.softwareishard.com/blog/har-12-spec/
"""
import base64
import re
import urllib.parse
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Optional, Annotated, Union, Mapping, Literal, Any, TextIO

import requests_toolbelt
from pydantic import (BaseModel, PlainSerializer, AwareDatetime, BeforeValidator, AfterValidator, Field,
                      model_validator, TypeAdapter, PlainValidator)
from requests.structures import CaseInsensitiveDict

import wxc_sdk.as_mpe

__all__ = ['HAR', 'HARLog', 'HAREntry', 'HARRequest', 'HARResponse', 'HARCreator']


def tz_is_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None or timezone.utc.utcoffset(dt).total_seconds() != 0:
        raise ValueError(f"Expected UTC time, got {dt}")
    return dt


# UTCDateTime is a datetime that is a TZ aware datetime in UTC timezone, serialized as ISO 8601 string w/ msec precision
UTCDateTime = Annotated[
    AwareDatetime, AfterValidator(tz_is_utc), PlainSerializer(lambda x: f"{x.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z",
                                                              return_type=str)]


class HARModel(BaseModel):
    """
    Base model for all HAR models
    """

    class Config:
        extra = 'allow'


class NameValue(HARModel):
    # Entry in a NameValue list; this is how dictionaries are represented in HAR files
    name: str
    value: str

    @staticmethod
    def list_to_dict(v: Union[dict, list[dict[str, str]]]):
        """
        Convert a list of NameValue entries to a dictionary; used for deserialization
        """
        if isinstance(v, Mapping):
            v = CaseInsensitiveDict(v.items())
        else:
            l: list['NameValue'] = TypeAdapter(list['NameValue']).validate_python(v)
            v = CaseInsensitiveDict(((e.name, e.value) for e in l))
        return v

    @staticmethod
    def dict_to_list(v: dict[str, str]) -> list[dict[str, str]]:
        """
        Convert a dictionary to a list of NameValue entries; used for serialization
        """
        if isinstance(v, list):
            return v
        l = [NameValue(name=k, value=v) for k, v in v.items()]
        r = TypeAdapter(list['NameValue']).dump_python(l, mode='json')
        return r

    @staticmethod
    def plain_to_dict(v: dict[str, str]) -> CaseInsensitiveDict[str, str]:
        if isinstance(v, Mapping):
            v = CaseInsensitiveDict(v)
        return v


# a dictionary representation in a HAR file; actually a CaseInsensitiveDict
# serialized as list of name/value tuples
HARDict = Annotated[
    dict[str, str], BeforeValidator(NameValue.list_to_dict), PlainValidator(NameValue.plain_to_dict), PlainSerializer(
        NameValue.dict_to_list)]


class PostData(HARModel):
    mimeType: str
    params: Optional[HARDict] = None
    text: str


class HARRequest(HARModel):
    """
    Request data in a HAR file entry
    """
    method: str
    url: str
    httpVersion: str
    cookies: HARDict = Field(default_factory=dict)
    headers: HARDict
    queryString: Optional[HARDict] = Field(default_factory=dict)
    postData: Optional[Union[str, PostData, Any]] = Field(default=None)
    headersSize: int = Field(default=-1)
    bodySize: int = Field(default=-1)
    with_authorization: bool = Field(default=False, exclude=True)

    @model_validator(mode='after')
    def val_model(self):
        """

        :meta private:
        """
        # if no authorization should be included, remove authorization header
        if not self.with_authorization:
            # strip out the Authorization header
            if isinstance(self.headers, list):
                self.headers = NameValue.list_to_dict(self.headers)
            self.headers.pop('Authorization', None)

        # if queryString is not set, parse it from url
        if not self.queryString:
            parsed_url = urllib.parse.urlparse(self.url)
            if query := parsed_url.query:
                self.queryString = dict(urllib.parse.parse_qsl(query))
            else:
                self.queryString = {}

        if not self.headersSize or self.headersSize == -1:
            # header size is the sum of the length of the keys and values of the headers, header and value are
            # separated by ': ', each header line has a trailing '\r\n' and there is a trailing '\r\n' after the last
            # header
            self.headersSize = sum(len(k) + len(v) + 4 for k, v in self.headers.items()) + 2

        # make sure that postData is set correctly
        if pd := self.postData:
            if not isinstance(pd, PostData):
                content_type = self.headers['Content-Type'].lower()
                if content_type.startswith('application/json'):
                    # Handle application/json
                    self.postData = PostData(text=pd, mimeType=content_type)
                    self.bodySize = len(pd)
                elif content_type.startswith('multipart/form-data'):
                    if isinstance(pd, requests_toolbelt.MultipartEncoder):
                        pd: requests_toolbelt.MultipartEncoder
                        body = ''
                        boundary = pd.boundary
                        for part in pd.parts:
                            body += f'{boundary}\r\n'
                            body += part.headers.decode()
                            body += 'file data missing'
                            body += '\r\n'
                        body += f'{boundary}--\r\n'
                        newPostData = PostData(text=base64.b64encode(body.encode()).decode(), mimeType=content_type)
                        self.postData = newPostData
                        # self.bodySize = self.headers.get('Content-Length', -1)
                        self.bodySize = -1
                    elif isinstance(pd, wxc_sdk.as_mpe.MultipartEncoder):
                        pd: requests_toolbelt.MultipartEncoder
                        boundary = re.search(r'boundary=(.*)', pd.content_type).group(1)
                        body = ''
                        for values, headers, _ in pd._fields:
                            body += f'--{boundary}\r\n'
                            cd_values = "; ".join(f'{k}="{v}"' for k, v in values.items())
                            body += 'Content-Disposition: form-data; ' + cd_values + '\r\n'
                            body += "'\r\n".join(f'{k}: {v}' for k, v in headers.items())
                            body += '\r\n\r\n'
                            body += 'file data missing'
                            body += '\r\n'
                        body += f'--{boundary}--\r\n'
                        newPostData = PostData(text=base64.b64encode(body.encode()).decode(), mimeType=content_type)
                        self.postData = newPostData
                        self.bodySize = -1
                        # self.bodySize = self.headers.get('Content-Length', -1)
                    else:
                        raise NotImplementedError('Unsupported multipart/form-data postData')
                else:
                    raise NotImplementedError(f'Unsupported content type: {content_type}')
        else:
            self.postData = None
            self.bodySize = -1
        return self


class HARContent(HARModel):
    size: Optional[int] = None
    compression: Optional[int] = None
    text: Optional[str] = None
    encoding: Optional[str] = None
    mimeType: Optional[str] = None


class HARResponse(HARModel):
    """
    Response data in a HAR file entry
    """
    status: int
    statusText: str
    httpVersion: str
    cookies: Optional[HARDict] = {}
    headers: HARDict
    content: Optional[HARContent] = None
    redirectURL: Optional[str] = ''
    headersSize: Optional[int] = -1
    bodySize: Optional[int] = -1
    #: content as string.
    #: Not part of the HAR spec, but derived from content and can be used to set content
    content_str: Optional[str] = Field(default=None, exclude=None)

    @model_validator(mode='after')
    def val_model(self):
        """
        Validate the model and derive content from content_str or vice versa. Also set headersSize and bodySize if not
        set

        :meta private:
        """
        # either content or content_str must be set
        # .. and then we derive content from content_str or vice versa
        if self.content_str is None:
            # set content_str from content
            content = self.content
            if content is None:
                self.content_str = None
            else:
                content: HARContent
                if content.encoding is None:
                    self.content_str = content.text
                elif content.encoding == 'base64':
                    self.content_str = base64.b64decode(content.text).decode()
                else:
                    raise ValueError(f'Unsupported encoding: {content.encoding}')
        elif self.content is None:
            # derive content from content_str
            if self.content_str:
                self.content = HARContent(size=len(self.content_str),
                                          text=base64.b64encode(self.content_str.encode()).decode(),
                                          encoding='base64', mimeType=self.headers['Content-Type'])
            else:
                self.content = None

        if not self.headersSize or self.headersSize == -1:
            # header size is the sum of the length of the keys and values of the headers, header and value are
            # separated by ': ', each header line has a trailing '\r\n' and there is a trailing '\r\n' after the last
            # header
            self.headersSize = sum(len(k) + len(v) + 4 for k, v in self.headers.items()) + 2

        if not self.bodySize or self.bodySize == -1:
            self.bodySize = self.content_str and len(self.content_str) or -1
        return self


class HARTimings(HARModel):
    blocked: float = Field(default=-1)
    dns: float = Field(default=-1)
    connect: float = Field(default=-1)
    send: float = Field(default=-1)
    wait: float = Field(default=-1)
    receive: float = Field(default=-1)
    ssl: float = Field(default=-1)


class HAREntry(HARModel):
    request: HARRequest
    response: HARResponse
    cache: Optional[HARDict] = Field(default_factory=dict)
    startedDateTime: UTCDateTime = Field(default_factory=lambda: datetime.now(timezone.utc))
    time: float
    timings: HARTimings = Field(default_factory=HARTimings)


class HARCreator(HARModel):
    name: str
    version: str


class HARLog(HARModel):
    version: str
    creator: HARCreator
    entries: Optional[list[HAREntry]] = Field(default_factory=list)


class HAR(HARModel):
    """
    The HAR file format is a JSON format that stands for HTTP Archive.
    """
    log: HARLog

    @classmethod
    def from_file(cls, file: Union[str, TextIO]) -> 'HAR':
        """
        Load a HAR file from a path or file-like object

        :param file: path to HAr file ort file-like object to read from
        :return: HAR object read from file
        """

        @contextmanager
        def open_file():
            if isinstance(file, str):
                with open(file, 'r') as tio:
                    yield tio
            else:
                yield file

        with open_file() as f:
            return cls.model_validate_json(f.read())

    def model_dump(self, *,
                   mode: Literal['json', 'python'] | str = 'json',
                   exclude_none: bool = True,
                   by_alias: bool = True,
                   **kwargs) -> dict[str, Any]:
        """
        Dump the HAR to a dictionary

        :meta private:
        """
        return super().model_dump(mode=mode, exclude_none=exclude_none, by_alias=by_alias, **kwargs)

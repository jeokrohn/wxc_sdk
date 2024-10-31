from datetime import datetime, timezone
from typing import Optional, Annotated

from pydantic import BaseModel, NaiveDatetime, PlainSerializer, AwareDatetime, BeforeValidator, AfterValidator, Field


def tz_is_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset():
        raise ValueError(f"Expected UTC time, got {dt}")
    return dt


UTCDateTime = Annotated[
    AwareDatetime, AfterValidator(tz_is_utc), PlainSerializer(lambda x: f"{x.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z",
                                                              return_type=str)]


class HARModel(BaseModel):
    class Config:
        extra = 'allow'


class HARCreator(HARModel):
    name: str
    version: str


class NameValue(HARModel):
    name: str
    value: str
    
NameValueList = list[NameValue]


class HARRequest(HARModel):
    method: str
    url: str
    httpVersion: str
    cookies: NameValueList
    headers: NameValueList
    queryString: NameValueList
    postData: Optional[dict] = None
    headersSize: int
    bodySize: int

class HARResponse(HARModel):
    status: int
    statusText: str
    httpVersion: str
    cookies: NameValueList
    headers: NameValueList
    content: dict
    redirectURL: str
    headersSize: int
    bodySize: int
   
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
    startedDateTime: UTCDateTime = Field(default_factory=lambda : datetime.now(timezone.utc))
    time: float
    cache: dict = Field(default_factory=dict)
    timings: HARTimings = Field(default_factory=HARTimings)


class HARLog(HARModel):
    version: str
    creator: HARCreator
    entries: list[HAREntry]


class HAR(HARModel):
    log: HARLog

    @classmethod
    def from_file(cls, path: str):
        with open(path, 'r') as f:
            return cls.model_validate_json(f.read())

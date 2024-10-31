import datetime
import glob
import json
import os.path
from dataclasses import dataclass
from unittest import TestCase

from pydantic import BaseModel, Field

from tests.base import TestCaseWithLog
from wxc_sdk.har_writer.har import HAR


class HarBase(BaseModel):
    class Config:
        extra = 'forbid'


class Creator(HarBase):
    name: str
    version: str


class HarEntry(HarBase):
    class Config:
        extra = 'allow'

    request: dict
    response: dict
    comment: str
    timings: dict
    started_date_time: datetime.datetime = Field(alias='startedDateTime')
    time: float
    server_ip_address: str = Field(alias='serverIPAddress')
    pass



@dataclass(init=False)
class TestHar(TestCase):
    latest_har: str
    data: dict

    def get_latest_har(self, path)->str:
        har_files = [(f, os.path.getmtime(f)) for f in glob.glob(os.path.join(path, '*.har'))]
        if not har_files:
            raise FileNotFoundError(f'No HAR files found in {path}')
        har_files.sort(key=lambda x: x[1], reverse=True)
        return har_files[0][0]

    def setUp(self):
        # find latest HAR file in Downloads
        self.latest_har = self.get_latest_har(os.path.expanduser('~/Downloads'))
        with open(self.latest_har, mode='r') as f:
            self.data = json.load(f)

    def test_parse(self):
        har = HAR.from_file(self.latest_har)
        foo = 1
        pass

    def test_latest_test_har(self):
        latest = self.get_latest_har(os.path.expanduser('~/Documents/workspace/wxc_sdk/tests/logs'))
        har = HAR.from_file(latest)
        foo =1

    def test_remove_underscore(self):
        def no_underscore(data):
            remove_fields = {'serverIPAddress', 'comment', 'cache', 'timings'}
            if isinstance(data, dict):
                return {k: no_underscore(v) for k, v in data.items() if (not k.startswith('_')
                                                                         and k not in remove_fields)}
            elif isinstance(data, list):
                return [no_underscore(v) for v in data]
            return data

        data = no_underscore(self.data)
        with open(os.path.abspath('/Users/jkrohn/Downloads/test_no_underscore.har'), mode='w') as f:
            json.dump(data, f, indent=2)


class TestWriteHar(TestCaseWithLog):
    proxy = True
    with_har = True

    def test_list_people(self):
        list(self.api.people.list(callingData=True))

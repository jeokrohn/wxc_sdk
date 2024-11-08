import base64
import glob
import glob
import json
import os.path
from dataclasses import dataclass
from unittest import TestCase

from tests.base import TestCaseWithLog
from wxc_sdk.har_writer.har import HAR, HARLog, HARCreator


@dataclass(init=False)
class TestHar(TestCase):
    latest_har_in_downloads: str

    @staticmethod
    def get_latest_har(path) -> str:
        har_files = [(f, os.path.getmtime(f)) for f in glob.glob(os.path.join(path, '*.har'))]
        if not har_files:
            return None
        har_files.sort(key=lambda x: x[1], reverse=True)
        return har_files[0][0]

    def setUp(self):
        # find latest HAR file in Downloads
        self.latest_har_in_downloads = self.get_latest_har(os.path.expanduser('~/Downloads'))

    def test_parse_latest_in_downloads(self):
        latest = self.latest_har_in_downloads
        if self.latest_har_in_downloads is None:
            self.skipTest('No HAR files found in Downloads')

        har = HAR.from_file(latest)
        print(f'Loaded HAR file: {latest} with {len(har.log.entries)} entries')

    def test_latest_in_logs_from_path(self):
        latest = self.get_latest_har(os.path.expanduser('~/Documents/workspace/wxc_sdk/tests/logs'))
        har = HAR.from_file(latest)
        print(f'Loaded HAR file: {latest} with {len(har.log.entries)} entries')

    def test_latest_in_logs_from_file(self):
        latest = self.get_latest_har(os.path.expanduser('~/Documents/workspace/wxc_sdk/tests/logs'))
        with open(latest, 'r') as f:
            har = HAR.from_file(f)
        print(f'Loaded HAR file: {latest} with {len(har.log.entries)} entries')


class TestWriteHar(TestCaseWithLog):
    proxy = True
    with_har = True

    def test_list_people(self):
        list(self.api.people.list(callingData=True))

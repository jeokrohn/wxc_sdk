import base64
import glob
import json
import os.path
from collections import defaultdict
from dataclasses import dataclass
from io import StringIO
from itertools import chain
from typing import Optional, TextIO
from unittest import TestCase, skip

from tests.base import TestCaseWithLog, TestCaseWithTokens
from wxc_sdk.har_writer import HAREntry, HarWriter
from wxc_sdk.har_writer.har import HAR, PostData


@skip('skipping for now')
@dataclass(init=False, repr=False)
class TestHar(TestCase):
    latest_har_in_downloads: str
    all_hars_in_downloads: list[str]

    def get_all_hars(self, path: str) -> Optional[list[tuple[int, str]]]:
        har_files = [(f, os.path.getmtime(f)) for f in glob.glob(os.path.join(path, '*.har'))]
        if not har_files:
            return None
        har_files.sort(key=lambda x: x[1], reverse=True)
        return har_files

    def get_latest_har(self, path: str) -> str:
        har_files = self.get_all_hars(path)
        return har_files[0][0]

    def setUp(self):
        # find latest HAR file in Downloads
        self.latest_har_in_downloads = self.get_latest_har(os.path.expanduser('~/Downloads'))
        self.all_hars_in_downloads = [f for f, _ in self.get_all_hars(os.path.expanduser('~/Downloads'))]

    def test_parse_latest_in_downloads(self):
        latest = self.latest_har_in_downloads
        if self.latest_har_in_downloads is None:
            self.skipTest('No HAR files found in Downloads')

        har = HAR.from_file(latest)
        print(f'Loaded HAR file: {latest} with {len(har.log.entries)} entries')

    def test_parse_all_in_downloads(self):
        for har_path in self.all_hars_in_downloads:
            har = HAR.from_file(har_path)
            print(f'{har_path}: ok')

    def test_requests_with_postdata(self):
        def has_base64_encoded_text(pd: PostData) -> bool:
            text = pd.text
            assert text is not None
            try:
                text = text.encode()
            except AttributeError:
                pass
            try:
                # some string is base64 if encoding the decoded value is identity
                is_base64 = base64.b64encode(base64.b64decode(text)) == text
                return is_base64
            except (ValueError, UnicodeDecodeError):
                return False

        r: HAREntry
        paths = ['~/Downloads', '~/Documents/workspace/wxc_sdk/tests/logs']
        all_hars = sorted(har
                          for har, _ in chain.from_iterable(self.get_all_hars(os.path.expanduser(path))
                                                            for path in paths))
        requests_with_postdata = [(r.request.postData, r) for r in chain.from_iterable(HAR.from_file(hp).log.entries
                                                                                       for hp in all_hars)
                                  if r.request.postData]
        by_post_data_mime_type: dict[str, list[tuple[bool, PostData, dict, HAREntry]]] = defaultdict(list)
        for pd, har_entry in requests_with_postdata:
            by_post_data_mime_type[pd.mimeType.split(';')[0]].append(
                (has_base64_encoded_text(pd), pd, pd.model_dump(), har_entry))

        foo = 1

    def test_latest_in_logs_from_path(self):
        latest = self.get_latest_har(os.path.expanduser('~/Documents/workspace/wxc_sdk/tests/logs'))
        har = HAR.from_file(latest)
        print(f'Loaded HAR file: {latest} with {len(har.log.entries)} entries')

    def test_latest_in_logs_from_file(self):
        latest = self.get_latest_har(os.path.expanduser('~/Documents/workspace/wxc_sdk/tests/logs'))
        with open(latest, 'r') as f:
            har = HAR.from_file(f)
        print(f'Loaded HAR file: {latest} with {len(har.log.entries)} entries')

    def test_incremental(self):
        latest = self.get_latest_har(os.path.expanduser('~/Documents/workspace/wxc_sdk/tests/logs'))
        source_har = HAR.from_file(latest)

        har_json = StringIO()
        with HarWriter(har_json, incremental=True) as writer:
            for entry in source_har.log.entries:
                writer.new_entry(entry)
        json_str = har_json.getvalue()
        json_data = json.loads(json_str)
        # validate generated JSON
        har = HAR.model_validate(json_data)
        # .. and that has to get us the same HAR as the one we started with
        self.assertEqual(source_har, har)


@skip('skipping for now')
class TestWriteHar(TestCaseWithLog):
    proxy = True
    with_har = True

    def test_list_people(self):
        list(self.api.people.list(callingData=True))

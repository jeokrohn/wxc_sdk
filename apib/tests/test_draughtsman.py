from unittest import TestCase

from draughtsman import parse

from apib.tests.test_apib import ApibTest


class TestDraught(ApibTest):
    def test_001_parse_one(self):
        target_path = next((path for path in self.apib_paths
                            if path.endswith('user-call-settings.apib')), None)
        with open(target_path, mode='r') as f:
            data = f.read()
        parsed = parse(data)
        foo = 1

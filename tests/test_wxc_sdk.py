from unittest import TestCase

from wxc_sdk import __version__


class TestVersion(TestCase):
    def test_version(self):
        assert __version__ == '1.28'

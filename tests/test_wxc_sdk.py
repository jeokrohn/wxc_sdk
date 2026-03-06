from unittest import TestCase

from wxc_sdk import __version__


class TestVersion(TestCase):
    def test_version(self):
        from importlib.metadata import version as meta_version
        version = meta_version('wxc_sdk')
        print(f'{version=}')
        assert __version__ == meta_version('wxc_sdk')

from unittest import TestCase
from wxc_sdk.scopes import parse_scopes

DESIRED = 'spark:calls_write spark:kms spark:people_read spark:calls_read spark-admin:telephony_config_read'


class TestScopes(TestCase):
    """
    Verify that all supported formats are parsed correctly
    """
    def test_001(self):
        self.assertEqual(DESIRED, parse_scopes(
            'https://webexapis.com/v1/authorize?client_id'
            '=Ce42963191c22025a1149568b98749ff66094b70f0d6cf7b0d64fff976eed4835&response_type=code&redirect_uri=http%3A'
            '%2F%2Flocalhost%3A6001%2Fredirect&scope=spark%3Acalls_write%20spark%3Akms%20spark%3Apeople_read%20spark'
            '%3Acalls_read%20spark-admin%3Atelephony_config_read&state=set_state_here'))

    def test_002(self):
        self.assertEqual(DESIRED, parse_scopes(
            'scope=spark%3Acalls_write%20spark%3Akms%20spark%3Apeople_read%20spark%3Acalls_read%20spark-admin'
            '%3Atelephony_config_read&state=set_state_here'))

    def test_003(self):
        self.assertEqual(DESIRED, parse_scopes(
            'spark%3Acalls_write%20spark%3Akms%20spark%3Apeople_read%20spark%3Acalls_read%20spark-admin'
            '%3Atelephony_config_read&state=set_state_here'))

    def test_004(self):
        self.assertEqual(DESIRED, parse_scopes(
            'spark%3Acalls_write%20spark%3Akms%20spark%3Apeople_read%20spark%3Acalls_read%20spark-admin'
            '%3Atelephony_config_read'))

    def test_005(self):
        self.assertEqual(DESIRED, parse_scopes(
            'spark:calls_write spark:kms spark:people_read spark:calls_read spark-admin:telephony_config_read'))

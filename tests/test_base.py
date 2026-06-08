import json
import unittest
from unittest import skip

from tests.base import AdminIntegration


class TestTokens(unittest.TestCase):
    @skip('Enable to get integration tokens for a user')
    def test_get_new_integration_tokens(self):
        """
        Get tokens using OAuth flow
        """
        integration = AdminIntegration()
        tokens = integration.get_tokens_from_oauth_flow()
        if tokens:
            tokens.set_expiration()

        print(json.dumps(tokens.model_dump(mode='json', exclude_none=True), indent=2))

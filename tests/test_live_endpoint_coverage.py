"""
Marker-gated live smoke tests for sync SDK GET endpoints.

The scenarios live in ``tests.endpoint_coverage`` so this file can stay focused
on test execution: obtain tokens, capture REST request logs, run one scenario,
and assert that the declared endpoint was actually requested.
"""

import logging

import pytest

from tests.base import RecordHandler, get_tokens
from tests.endpoint_coverage import (
    LIVE_GET_SCENARIOS,
    LiveEndpointContext,
    LiveEndpointSkip,
    assert_endpoint_requested,
    skip_reason_for_rest_error,
)
from wxc_sdk import WebexSimpleApi
from wxc_sdk.rest import RestError

pytestmark = pytest.mark.live_endpoint


@pytest.fixture(scope='module')
def live_api():
    """
    Create one live sync API instance for the module.

    :return: Configured :class:`WebexSimpleApi` fixture.
    """
    tokens = get_tokens()
    if not tokens:
        pytest.skip('Failed to obtain Webex tokens')
    with WebexSimpleApi(tokens=tokens) as api:
        yield api


@pytest.fixture
def request_records():
    """
    Capture REST debug log records emitted during one scenario.

    The live assertions reuse the same log format as ``TestCaseWithLog`` so the
    smoke tests observe real SDK requests without adding a separate HTTP mock.

    :return: Mutable list of logging records populated while the fixture is active.
    """
    handler = RecordHandler(level=logging.DEBUG)
    loggers = [logging.getLogger(name) for name in ('wxc_sdk.rest', 'wxc_sdk.as_rest', 'webexteamsasyncapi.rest')]
    old_levels = {logger: logger.level for logger in loggers}
    for logger in loggers:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
    try:
        yield handler.records
    finally:
        for logger in loggers:
            logger.removeHandler(handler)
            logger.setLevel(old_levels[logger])
        handler.close()


@pytest.mark.parametrize('scenario', LIVE_GET_SCENARIOS, ids=lambda scenario: scenario.id)
def test_live_get_endpoint_smoke(live_api, request_records, scenario):
    """
    Execute one live GET scenario and assert that its endpoint was requested.

    :param live_api: Module-scoped live SDK fixture.
    :param request_records: Captured REST log records for this scenario.
    :param scenario: Scenario metadata and callable under test.
    """
    ctx = LiveEndpointContext(live_api)
    start = len(request_records)

    try:
        scenario.call(ctx)
    except LiveEndpointSkip as exc:
        # Missing optional tenant artifacts are expected in broad live coverage.
        pytest.skip(str(exc))
    except RestError as exc:
        # Some endpoints are unavailable without specific scopes or tenant
        # entitlements; the scenario declares which statuses count as skips.
        if reason := skip_reason_for_rest_error(exc, scenario):
            pytest.skip(reason)
        raise

    assert_endpoint_requested(scenario.method, request_records[start:])

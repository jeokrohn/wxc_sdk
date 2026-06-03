"""
Pytest configuration for endpoint-coverage tests.

The live endpoint smoke tests are intentionally present in the normal test tree
but must not run unless a maintainer explicitly opts in. This file applies that
collection-time gate based on ``RUN_LIVE_ENDPOINT_TESTS``.
"""

import os

import pytest


def _truthy_env(name: str) -> bool:
    """
    Interpret a conventional truthy environment variable.

    :param name: Environment variable name to read.
    :return: ``True`` for values such as ``1``, ``true``, ``yes``, or ``on``.
    """
    value = os.getenv(name, '')
    return value.lower() in {'1', 'true', 'yes', 'on'}


def pytest_collection_modifyitems(config, items):
    """
    Skip live endpoint tests unless their explicit opt-in flag is set.

    :param config: Pytest configuration object supplied by the hook.
    :param items: Collected test items that may need live-endpoint skip marks.
    """
    if _truthy_env('RUN_LIVE_ENDPOINT_TESTS'):
        return

    # Collection-time marking keeps the tests visible in normal runs while
    # preventing accidental live Webex calls from local or CI smoke commands.
    skip_live_endpoint = pytest.mark.skip(reason='set RUN_LIVE_ENDPOINT_TESTS=1 to run live endpoint coverage')
    for item in items:
        if 'live_endpoint' in item.keywords:
            item.add_marker(skip_live_endpoint)

"""
Offline inventory checks for live endpoint coverage.

These tests do not require Webex credentials. They make sure the endpoint
reference still resolves, the checked-in Markdown reference is current, and each
GET endpoint is either covered by tests or explicitly quarantined.
"""

from pathlib import Path

from tests.endpoint_coverage import (
    current_endpoint_markdown,
    endpoint_rows,
    explain_missing,
    invalid_endpoint_rows,
    missing_get_methods,
    unknown_live_scenarios,
)


def test_endpoint_reference_resolves_supported_sync_endpoints():
    """
    Verify that the sync SDK endpoint inventory can be resolved.

    This catches resolver regressions before live smoke tests try to map
    concrete requests back to endpoint templates.
    """
    rows = endpoint_rows()

    assert rows
    assert not invalid_endpoint_rows()


def test_endpoint_ref_markdown_is_current():
    """
    Verify that ``endpoint_ref.md`` matches the current SDK inventory.

    The coverage helper and user-facing endpoint reference intentionally share
    the same source of truth, so drift here means the generated documentation
    needs to be refreshed.
    """
    expected = current_endpoint_markdown()
    endpoint_ref_path = Path(__file__).resolve().parents[1] / 'endpoint_ref.md'
    actual = endpoint_ref_path.read_text(encoding='utf-8')

    assert actual == expected


def test_live_get_coverage_inventory_is_classified():
    """
    Verify that every GET endpoint is covered or explicitly classified.

    New GET methods should either get a live smoke scenario, be covered by an
    existing dedicated test, or receive a quarantine rule with a concrete reason.
    """
    unknown = unknown_live_scenarios()
    missing = missing_get_methods()

    assert not unknown, 'Live endpoint scenarios reference unknown SDK methods:\n' + explain_missing(unknown)
    assert not missing, 'GET endpoints need coverage or an explicit quarantine reason:\n' + explain_missing(missing)

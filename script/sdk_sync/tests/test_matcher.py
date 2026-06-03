"""Regression tests for stub-to-SDK matching."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from script.sdk_sync import aliases, matcher
from script.sdk_sync.differ import ChangeRecord
from script.sdk_sync.ir import extract_from_text


def test_method_match_finds_non_last_api_class_in_sdk_module(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Ensure endpoint matching searches every API class in an SDK module.

    The regression case is a module whose last ``ApiChild`` subclass is not the
    class that owns the matching endpoint. The matcher must still find the
    earlier class by HTTP method and endpoint template.

    :param tmp_path: Temporary project root used for a synthetic SDK module.
    :param monkeypatch: Pytest helper used to point the matcher at that module.
    """
    # Build a minimal SDK module with two API classes. The endpoint we need is
    # intentionally on the non-last class to guard against old indexing behavior.
    sdk_root = tmp_path / 'wxc_sdk'
    sdk_root.mkdir()
    sdk_file = sdk_root / 'jobs.py'
    sdk_file.write_text(
        textwrap.dedent("""\
        from wxc_sdk.api_child import ApiChild


        class ManageNumbersJobsApi(ApiChild, base='telephony/config/jobs/numbers'):
            def initiate_job(self):
                url = self.ep('manageNumbers')
                return super().post(url)


        class JobsApi(ApiChild, base='telephony/config/jobs'):
            pass
        """)
    )

    # Point the matcher at the synthetic SDK root and reset the cached index so
    # the test only observes the fixture module above.
    monkeypatch.setattr(matcher, '_SDK_ROOT', sdk_root)
    monkeypatch.setattr(matcher, '_index', matcher._SDKIndex())

    # The generated stub uses a different class and method name but the same
    # effective POST endpoint, which is the contract the matcher joins on.
    stub_ir = extract_from_text(
        textwrap.dedent("""\
        from wxc_sdk.api_child import ApiChild


        class NumbersApi(ApiChild, base='telephony/config'):
            def initiate_number_jobs(self):
                url = self.ep('jobs/numbers/manageNumbers')
                return super().post(url)
        """),
        'open_api/generated/Webex-Suite/Webex-Calling/Webex-Cloud-Calling/All-APIs/numbers_auto.py',
    )
    record = ChangeRecord(
        kind='method_param_added',
        qualname='NumbersApi.initiate_number_jobs',
        old=None,
        new={'name': 'initiate_number_jobs'},
        severity='review',
    )

    match = matcher.match(record, stub_ir, aliases.AliasStore())

    assert match is not None
    assert match.sdk_class == 'ManageNumbersJobsApi'
    assert match.sdk_member == 'initiate_job'
    assert match.matched_by == 'exact'

import json
from pathlib import Path

import pytest

from wxc_sdk.bulk_provision.data_pipeline import build_pipeline


def _write_site(tmp_path: Path) -> None:
    payload = {
        "locations": [
            {
                "location_key": "LOC1",
                "name": "Location One",
                "time_zone": "UTC",
                "preferred_language": "en_US",
                "announcement_language": "en_US",
                "address1": "Main St",
                "city": "Test",
                "state": "TS",
                "postal_code": "12345",
                "country": "US",
            }
        ],
        "profiles": {"licenses": {"LIC_CALLING_PRO": ["lic1"]}},
    }
    (tmp_path / "site.json").write_text(json.dumps(payload))


def _write_users(tmp_path: Path, rows: list[list[str]]) -> None:
    header = (
        "email,location_key,licenses,extension,phone_number_primary,phone_number_secondary,"
        "permissions_out_profile,caller_id_profile,recording_profile,forwarding_legacy_mode,"
        "forwarding_legacy_destination,groups_access,groups_features,feature_access_profile,"
        "monitoring_targets,monitoring_barge,exec_assistant_role,executive_for,assistants_for\n"
    )
    content = header + "\n".join(",".join(row) for row in rows)
    (tmp_path / "users.csv").write_text(content)


def test_pipeline_accepts_users(tmp_path: Path) -> None:
    _write_site(tmp_path)
    _write_users(
        tmp_path,
        [["ana@example.com", "LOC1", "LIC_CALLING_PRO"] + [""] * 16],
    )
    result = build_pipeline(tmp_path)
    assert len(result.users) == 1
    assert result.rejected == []


def test_pipeline_rejects_missing_required(tmp_path: Path) -> None:
    _write_site(tmp_path)
    _write_users(tmp_path, [["", "LOC1", ""] + [""] * 16])
    result = build_pipeline(tmp_path)
    assert len(result.rejected) == 1


def test_pipeline_rejects_duplicate_email(tmp_path: Path) -> None:
    _write_site(tmp_path)
    _write_users(
        tmp_path,
        [
            ["ana@example.com", "LOC1", "LIC_CALLING_PRO"] + [""] * 16,
            ["ana@example.com", "LOC1", "LIC_CALLING_PRO"] + [""] * 16,
        ],
    )
    result = build_pipeline(tmp_path)
    assert len(result.rejected) == 1


def test_pipeline_missing_users_csv(tmp_path: Path) -> None:
    _write_site(tmp_path)
    with pytest.raises(AssertionError):
        build_pipeline(tmp_path)

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from .error_handling import ReasonCode


@dataclass(frozen=True)
class SiteBundle:
    payload: dict[str, Any]
    input_hash: str
    locations: dict[str, dict[str, Any]]


@dataclass(frozen=True)
class UserRow:
    row_id: int
    entity_key: str
    location_key: str
    data: dict[str, Any]


@dataclass(frozen=True)
class WorkspaceRow:
    row_id: int
    entity_key: str
    location_key: str
    data: dict[str, Any]


@dataclass(frozen=True)
class DeviceRow:
    row_id: int
    entity_key: str
    location_key: str
    data: dict[str, Any]


@dataclass(frozen=True)
class RejectedRow:
    row_id: int
    reason_code: ReasonCode
    reason_message: str
    raw_row_minified: str


@dataclass(frozen=True)
class DataPipelineResult:
    site_bundle: SiteBundle
    users: list[UserRow]
    workspaces: list[WorkspaceRow]
    devices: list[DeviceRow]
    rejected: list[RejectedRow]


USERS_HEADER = [
    "email",
    "location_key",
    "licenses",
    "extension",
    "phone_number_primary",
    "phone_number_secondary",
    "permissions_out_profile",
    "caller_id_profile",
    "recording_profile",
    "forwarding_legacy_mode",
    "forwarding_legacy_destination",
    "groups_access",
    "groups_features",
    "feature_access_profile",
    "monitoring_targets",
    "monitoring_barge",
    "exec_assistant_role",
    "executive_for",
    "assistants_for",
]

WORKSPACES_HEADER = [
    "workspace_display_name",
    "location_key",
    "workspace_external_id",
    "licenses",
    "extension",
    "phone_number_primary",
    "phone_number_secondary",
    "permissions_out_profile",
    "caller_id_profile",
    "forwarding_legacy_mode",
    "forwarding_legacy_destination",
]

DEVICES_HEADER = [
    "device_type",
    "owner_key",
    "location_key",
    "model",
    "action",
    "notes",
]


def _normalize_value(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _load_site_bundle(input_dir: Path) -> SiteBundle:
    site_path = input_dir / "site.json"
    assert site_path.exists(), "site.json is required"
    site_bytes = site_path.read_bytes()
    payload = json.loads(site_bytes)
    locations = {item["location_key"]: item for item in payload.get("locations", [])}
    input_hash = hashlib.sha256(site_bytes).hexdigest()
    return SiteBundle(payload=payload, input_hash=input_hash, locations=locations)


def _hash_file(path: Path, current: hashlib._hashlib.HASH) -> None:
    current.update(path.read_bytes())


def _bundle_hash(paths: list[Path]) -> str:
    current = hashlib.sha256()
    for path in paths:
        _hash_file(path, current)
    return current.hexdigest()


def _load_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def build_pipeline(input_dir: Path) -> DataPipelineResult:
    site_bundle = _load_site_bundle(input_dir)
    rejected: list[RejectedRow] = []
    users: list[UserRow] = []
    workspaces: list[WorkspaceRow] = []
    devices: list[DeviceRow] = []

    users_path = input_dir / "users.csv"
    workspaces_path = input_dir / "workspaces.csv"
    devices_path = input_dir / "devices.csv"

    assert users_path.exists(), "users.csv is required"

    expected_paths = [users_path, input_dir / "site.json"]
    if workspaces_path.exists():
        expected_paths.append(workspaces_path)
    if devices_path.exists():
        expected_paths.append(devices_path)

    bundle_hash = _bundle_hash(expected_paths)
    site_bundle = SiteBundle(
        payload=site_bundle.payload,
        input_hash=bundle_hash,
        locations=site_bundle.locations,
    )

    with users_path.open("r", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != USERS_HEADER:
            raise AssertionError("users.csv header mismatch")
        seen = set()
        for row_id, row in enumerate(reader, 2):
            normalized = {k: _normalize_value(v) for k, v in row.items()}
            email = normalized.get("email")
            location_key = normalized.get("location_key")
            if not email or not location_key:
                rejected.append(
                    RejectedRow(
                        row_id=row_id,
                        reason_code=ReasonCode.invalid_input_schema,
                        reason_message="Missing required fields",
                        raw_row_minified=str({"email": email, "location_key": location_key}),
                    )
                )
                continue
            if email in seen:
                rejected.append(
                    RejectedRow(
                        row_id=row_id,
                        reason_code=ReasonCode.duplicate_key,
                        reason_message=f"Duplicate email {email}",
                        raw_row_minified=str({"email": email}),
                    )
                )
                continue
            seen.add(email)
            users.append(
                UserRow(
                    row_id=row_id,
                    entity_key=email,
                    location_key=location_key,
                    data=normalized,
                )
            )

    if workspaces_path.exists():
        with workspaces_path.open("r", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != WORKSPACES_HEADER:
                raise AssertionError("workspaces.csv header mismatch")
            seen = set()
            for row_id, row in enumerate(reader, 2):
                normalized = {k: _normalize_value(v) for k, v in row.items()}
                name = normalized.get("workspace_display_name")
                location_key = normalized.get("location_key")
                if not name or not location_key:
                    rejected.append(
                        RejectedRow(
                            row_id=row_id,
                            reason_code=ReasonCode.invalid_input_schema,
                            reason_message="Missing required fields",
                            raw_row_minified=str({"workspace_display_name": name, "location_key": location_key}),
                        )
                    )
                    continue
                if name in seen:
                    rejected.append(
                        RejectedRow(
                            row_id=row_id,
                            reason_code=ReasonCode.duplicate_key,
                            reason_message=f"Duplicate workspace {name}",
                            raw_row_minified=str({"workspace_display_name": name}),
                        )
                    )
                    continue
                seen.add(name)
                workspaces.append(
                    WorkspaceRow(
                        row_id=row_id,
                        entity_key=name,
                        location_key=location_key,
                        data=normalized,
                    )
                )

    if devices_path.exists():
        with devices_path.open("r", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != DEVICES_HEADER:
                raise AssertionError("devices.csv header mismatch")
            for row_id, row in enumerate(reader, 2):
                normalized = {k: _normalize_value(v) for k, v in row.items()}
                device_type = normalized.get("device_type")
                owner_key = normalized.get("owner_key")
                location_key = normalized.get("location_key")
                action = normalized.get("action")
                if not device_type or not owner_key or not location_key or not action:
                    rejected.append(
                        RejectedRow(
                            row_id=row_id,
                            reason_code=ReasonCode.invalid_input_schema,
                            reason_message="Missing required fields",
                            raw_row_minified=str(
                                {
                                    "device_type": device_type,
                                    "owner_key": owner_key,
                                    "location_key": location_key,
                                    "action": action,
                                }
                            ),
                        )
                    )
                    continue
                devices.append(
                    DeviceRow(
                        row_id=row_id,
                        entity_key=f"{device_type}:{owner_key}",
                        location_key=location_key,
                        data=normalized,
                    )
                )

    return DataPipelineResult(
        site_bundle=site_bundle,
        users=users,
        workspaces=workspaces,
        devices=devices,
        rejected=rejected,
    )

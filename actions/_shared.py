#!/usr/bin/env python3
"""Shared helpers for one-action-per-script remote API probes/applies."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import logging
import os
import string
from dataclasses import dataclass
from typing import Any

import requests
from requests import Response

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


@dataclass(frozen=True)
class ApiCall:
    name: str
    method: str
    path: str
    payload: dict[str, Any] | None = None
    params: dict[str, Any] | None = None
    acceptable_statuses: tuple[int, ...] = (200, 201, 204)


@dataclass(frozen=True)
class ActionSpec:
    key: str
    title: str
    objective: str
    pre_post_notes: list[str]
    probe_calls: list[ApiCall]
    apply_calls: list[ApiCall]


def _string_placeholders(value: str) -> set[str]:
    return {
        field_name
        for _, field_name, _, _ in string.Formatter().parse(value)
        if field_name
    }


def _collect_placeholders(value: Any) -> set[str]:
    if isinstance(value, str):
        return _string_placeholders(value)
    if isinstance(value, dict):
        items: set[str] = set()
        for nested_value in value.values():
            items.update(_collect_placeholders(nested_value))
        return items
    if isinstance(value, list):
        items: set[str] = set()
        for nested_value in value:
            items.update(_collect_placeholders(nested_value))
        return items
    return set()


def _required_optional_vars(spec: ActionSpec) -> tuple[list[str], list[str]]:
    probe_vars: set[str] = set()
    apply_vars: set[str] = set()
    for call in spec.probe_calls:
        probe_vars.update(_collect_placeholders(call.path))
        probe_vars.update(_collect_placeholders(call.payload))
        probe_vars.update(_collect_placeholders(call.params))
    for call in spec.apply_calls:
        apply_vars.update(_collect_placeholders(call.path))
        apply_vars.update(_collect_placeholders(call.payload))
        apply_vars.update(_collect_placeholders(call.params))
    required = sorted(apply_vars)
    optional = sorted(probe_vars - apply_vars)
    return required, optional


def _help_epilog(spec: ActionSpec) -> str:
    required_vars, optional_vars = _required_optional_vars(spec)
    required_text = ", ".join(required_vars) if required_vars else "(none)"
    optional_text = ", ".join(optional_vars) if optional_vars else "(none)"
    return (
        "Variables for --vars (JSON)\n"
        f"  Required (apply mode): {required_text}\n"
        f"  Optional (probe-only): {optional_text}\n"
        "  Example: --vars '{\"location_id\":\"...\"}'"
    )


class SimpleApiClient:
    def __init__(self, base_url: str, token: str, timeout: int, retries: int, verify: bool):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.verify = verify
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}", "Content-Type": "application/json"})

    def request(self, method: str, path: str, *, params: dict[str, Any] | None, json_payload: dict[str, Any] | None) -> Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        last_error: Exception | None = None
        for attempt in range(1, self.retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_payload,
                    timeout=self.timeout,
                    verify=self.verify,
                )
                if response.status_code == 429 or response.status_code >= 500:
                    if attempt < self.retries:
                        continue
                return response
            except requests.RequestException as err:
                last_error = err
                if attempt >= self.retries:
                    raise
        if last_error:
            raise last_error
        raise RuntimeError("Unreachable request state")


def _format_value(value: Any, variables: dict[str, Any]) -> Any:
    if isinstance(value, str):
        return value.format_map(variables)
    if isinstance(value, dict):
        return {k: _format_value(v, variables) for k, v in value.items()}
    if isinstance(value, list):
        return [_format_value(v, variables) for v in value]
    return value


def _run_calls(client: SimpleApiClient, calls: list[ApiCall], variables: dict[str, Any], logger: logging.Logger) -> int:
    failures = 0
    for call in calls:
        path = _format_value(call.path, variables)
        payload = _format_value(call.payload, variables) if call.payload else None
        params = _format_value(call.params, variables) if call.params else None
        logger.info("API call start", extra={"step": call.name, "method": call.method, "path": path})
        try:
            response = client.request(call.method, path, params=params, json_payload=payload)
            status = response.status_code
            body = response.text[:800]
            ok = status in call.acceptable_statuses
            level = logging.INFO if ok else logging.ERROR
            logger.log(level, "API call done", extra={"step": call.name, "status": status, "body": body})
            if not ok:
                failures += 1
        except Exception as err:  # pragma: no cover - runtime guard
            logger.exception("Unexpected error", extra={"step": call.name, "error": str(err)})
            failures += 1
    return failures


def _snapshot_meta(action_key: str, snapshot_dir: str | None) -> SnapshotMeta:
    base_dir = Path(snapshot_dir) if snapshot_dir else Path(tempfile.gettempdir())
    base_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    latest_name = f"lastdatetime_snapshot_action_{action_key}.json"
    timestamped_name = f"{timestamp}_{latest_name}"
    return SnapshotMeta(latest_path=base_dir / latest_name, timestamped_path=base_dir / timestamped_name)


def _save_snapshot(meta: SnapshotMeta, payload: dict[str, Any]) -> None:
    snapshot_text = json.dumps(payload, ensure_ascii=False, indent=2)
    meta.timestamped_path.write_text(snapshot_text, encoding="utf-8")
    meta.latest_path.write_text(snapshot_text, encoding="utf-8")


def _load_snapshot(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _preflight_snapshot(client: SimpleApiClient, spec: ActionSpec, variables: dict[str, Any], logger: logging.Logger) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for call in spec.probe_calls:
        path = _format_value(call.path, variables)
        params = _format_value(call.params, variables) if call.params else None
        logger.info("Preflight snapshot GET start", extra={"step": call.name, "path": path})
        try:
            response = client.request("GET", path, params=params, json_payload=None)
            json_body: dict[str, Any] | list[Any] | None
            try:
                json_body = response.json()
            except ValueError:
                json_body = None
            entries.append(
                {
                    "name": call.name,
                    "path": path,
                    "status": response.status_code,
                    "body": json_body,
                    "text": response.text[:2000],
                }
            )
            logger.info("Preflight snapshot GET done", extra={"step": call.name, "status": response.status_code})
        except Exception as err:  # pragma: no cover - runtime guard
            logger.exception("Preflight snapshot GET failed", extra={"step": call.name, "error": str(err)})
            entries.append({"name": call.name, "path": path, "error": str(err)})
    return {"action_key": spec.key, "captured_at": datetime.now().isoformat(), "entries": entries}


def _calls_from_snapshot(snapshot: dict[str, Any], logger: logging.Logger) -> list[ApiCall]:
    calls: list[ApiCall] = []
    for index, entry in enumerate(snapshot.get("entries", []), start=1):
        body = entry.get("body")
        path = entry.get("path")
        if not path or not isinstance(body, dict):
            continue
        calls.append(
            ApiCall(
                name=f"revert_{entry.get('name', index)}",
                method="PUT",
                path=path,
                payload=body,
                acceptable_statuses=(200, 201, 204, 400, 404),
            )
        )
    if not calls:
        logger.error("Snapshot has no reversible entries with JSON object body")
    return calls


def run_action_spec(spec: ActionSpec) -> int:
    parser = argparse.ArgumentParser(
        description=spec.title,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_help_epilog(spec),
    )
    parser.add_argument("--mode", choices=["probe", "apply"], default="probe")
    parser.add_argument("--base-url", default=os.getenv("WEBEX_BASE_URL", "https://webexapis.com/v1"))
    parser.add_argument("--token", default=os.getenv("WEBEX_ACCESS_TOKEN"))
    parser.add_argument("--vars", default="{}", help="JSON with ids/fields used in endpoint templates")
    parser.add_argument("--snapshot-dir", default=None, help="Directory for preflight snapshots used by --mode revert")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--insecure", action="store_true", help="Disable TLS cert validation")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    logger = logging.getLogger(spec.key)

    logger.info("Action objective: %s", spec.objective)
    for note in spec.pre_post_notes:
        logger.info("Note: %s", note)

    if not args.token:
        logger.error("Missing token. Set WEBEX_ACCESS_TOKEN or --token")
        return 2

    variables = json.loads(args.vars)
    required_vars, _ = _required_optional_vars(spec)
    missing_required = [name for name in required_vars if name not in variables]
    if missing_required and args.mode == "apply":
        logger.error("Missing required --vars for apply mode: %s", ", ".join(missing_required))
        return 2
    client = SimpleApiClient(
        base_url=args.base_url,
        token=args.token,
        timeout=args.timeout,
        retries=args.retries,
        verify=not args.insecure,
    )

    logger.info("No server-side dry-run endpoint is documented for these APIs. probe mode uses controlled invalid or read-only calls.")
    calls = spec.probe_calls if args.mode == "probe" else spec.apply_calls

    if args.mode == "apply":
        snapshot_meta = _snapshot_meta(spec.key, args.snapshot_dir)
        snapshot_payload = _preflight_snapshot(client, spec, variables, logger)
        _save_snapshot(snapshot_meta, snapshot_payload)
        logger.info("Preflight snapshot saved", extra={"latest": str(snapshot_meta.latest_path), "timestamped": str(snapshot_meta.timestamped_path)})

    if args.mode == "revert":
        snapshot_meta = _snapshot_meta(spec.key, args.snapshot_dir)
        if not snapshot_meta.latest_path.exists():
            logger.error("Snapshot for revert not found", extra={"snapshot": str(snapshot_meta.latest_path)})
            return 2
        snapshot_payload = _load_snapshot(snapshot_meta.latest_path)
        calls = _calls_from_snapshot(snapshot_payload, logger)
        if not calls:
            return 2

    failures = _run_calls(client, calls, variables, logger)
    logger.info("Completed action with %s failure(s)", failures)
    return 1 if failures else 0

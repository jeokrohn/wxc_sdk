#!/usr/bin/env python3
"""Shared helpers for one-action-per-script remote API probes/applies."""

from __future__ import annotations

import argparse
import json
import logging
import os
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


def run_action_spec(spec: ActionSpec) -> int:
    parser = argparse.ArgumentParser(description=spec.title)
    parser.add_argument("--mode", choices=["probe", "apply"], default="probe")
    parser.add_argument("--base-url", default=os.getenv("WEBEX_BASE_URL", "https://webexapis.com/v1"))
    parser.add_argument("--token", default=os.getenv("WEBEX_ACCESS_TOKEN"))
    parser.add_argument("--vars", default="{}", help="JSON with ids/fields used in endpoint templates")
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
    client = SimpleApiClient(
        base_url=args.base_url,
        token=args.token,
        timeout=args.timeout,
        retries=args.retries,
        verify=not args.insecure,
    )

    logger.info("No server-side dry-run endpoint is documented for these APIs. probe mode uses controlled invalid or read-only calls.")
    calls = spec.probe_calls if args.mode == "probe" else spec.apply_calls
    failures = _run_calls(client, calls, variables, logger)
    logger.info("Completed action with %s failure(s)", failures)
    return 1 if failures else 0

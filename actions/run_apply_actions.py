#!/usr/bin/env python3
"""Ejecuta todas las acciones en modo apply y guarda un log consolidado + reporte por API call."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import logging
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

ACTIONS: list[tuple[str, dict[str, str]]] = [
    ("action_auto_attendant.py", {"aa_name": "AA-LAB-MADRID", "extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "schedule_name": "Horario-LAB-LV"}),
    ("action_call_pickup_group.py", {"extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "pickup_name": "PG-LAB-RECEPCION"}),
    ("action_call_profiles.py", {"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA"}),
    ("action_call_queue.py", {"extension": "5101", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "queue_id": "MISSING_queue_id", "queue_name": "CQ-LAB-VENTAS"}),
    ("action_day_t_numbers_caller_id.py", {"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "primary_number": "+34915559742549"}),
    ("action_delegated_admin.py", {"principal_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "role_id": "Y2lzY29zcGFyazovL3VzL1JPTEUvaWRfdXNlcl9hZG1pbg", "scope": "organization"}),
    ("action_devices.py", {"device_model": "Cisco 8851", "workspace_id": "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1BMQUNFLzQyOGI3NzVhLWYxNTgtNDVkOC1hOTJhLTg1OTllNTVjM2UxYw==", "serial": "FTX1234LAB1"}),
    ("action_group_assignment.py", {"group_id": "MISSING_group_id", "group_name": "LAB-GROUP-VOICE", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE"}),
    ("action_hunt_group.py", {"extension": "5101", "hunt_name": "HG-LAB-SOPORTE", "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE"}),
    ("action_internal_extensions_sbc.py", {"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "route_group_id": "MISSING_route_group_id", "route_group_name": "RG-LAB-SBC", "trunk_id": "MISSING_trunk_id", "trunk_name": "TRUNK-LAB-MAIN"}),
    ("action_interplatform_dial_plan.py", {"dial_pattern": "+3491XXXXXXX", "dial_plan_name": "DP-LAB-INTERPLATFORM", "route_group_id": "MISSING_route_group_id"}),
    ("action_legacy_forwarding.py", {"forward_destination": "+34915550123", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE"}),
    ("action_location_number_removal.py", {"location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2ZjODY3OGRhLTBiOGItNDBlZS04ZWVjLTNhNzFlODFiMzc0OA", "primary_number": "+34915559742549"}),
    ("action_manager_assistant.py", {"assistant_person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS81MjYxMWNkMS1jMTJmLTQxNjgtODc1My04MDdmODJiOTYwNGQ", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE"}),
    ("action_monitoring.py", {"person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "target_person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS81MjYxMWNkMS1jMTJmLTQxNjgtODc1My04MDdmODJiOTYwNGQ"}),
    ("action_nominal_users.py", {"extension": "5101", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "primary_number": "+34915559742549"}),
    ("action_secondary_numbers.py", {"extension": "5101", "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE", "secondary_number": "+34915555861252"}),
    ("action_user_recording.py", {"person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS80OWZhZTIyMC02OGZlLTQ2NzEtYmU1My03Y2UxZDgzZTQ1ZDE"}),
    ("action_workspaces.py", {"extension": "5101", "primary_number": "+34915559742549", "workspace_id": "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1BMQUNFLzQyOGI3NzVhLWYxNTgtNDVkOC1hOTJhLTg1OTllNTVjM2UxYw=="}),
]

CALL_DONE_RE = re.compile(r"API call done \| step=(?P<step>[^ ]+) status=(?P<status>\d{3})")


def build_logger(log_file: Path) -> logging.Logger:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    handlers = [logging.StreamHandler(sys.stdout), logging.FileHandler(log_file, encoding="utf-8")]
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=handlers, force=True)
    return logging.getLogger("apply_runner")


def _load_context(context_file: Path | None) -> dict[str, Any]:
    if not context_file or not context_file.exists():
        return {}
    raw = json.loads(context_file.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}
    return raw


def _replace_missing_vars(payload: dict[str, str], context: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    resolved: dict[str, str] = {}
    unresolved: list[str] = []
    for key, value in payload.items():
        if isinstance(value, str) and value.startswith("MISSING_"):
            ctx_value = context.get(key)
            if isinstance(ctx_value, str) and ctx_value and not ctx_value.startswith("MISSING_"):
                resolved[key] = ctx_value
            else:
                resolved[key] = value
                unresolved.append(key)
            continue
        resolved[key] = value
    return resolved, unresolved


def _parse_api_calls(action_log: Path) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    if not action_log.exists():
        return calls
    for line in action_log.read_text(encoding="utf-8").splitlines():
        m = CALL_DONE_RE.search(line)
        if not m:
            continue
        calls.append({"step": m.group("step"), "status": int(m.group("status"))})
    return calls


def _resolve_token(args: argparse.Namespace) -> str | None:
    if args.token:
        return args.token
    env_token = os.getenv("WEBEX_ACCESS_TOKEN") or os.getenv("WEBEX_TOKEN")
    if env_token:
        return env_token
    if args.token_file:
        token_path = Path(args.token_file)
        if token_path.exists():
            return token_path.read_text(encoding="utf-8").strip()
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all apply actions with consolidated logging")
    parser.add_argument("--token", default=None)
    parser.add_argument("--token-file", default=None, help="Path to file containing WEBEX token")
    parser.add_argument("--continue-on-error", action="store_true", help="Do not stop at first failing action")
    parser.add_argument("--log-file", default=None, help="Custom path for consolidated log file")
    parser.add_argument("--report-file", default=None, help="Custom path for JSON report with per-action call status")
    parser.add_argument("--context-file", default="actions/lab_context.json", help="Context JSON to replace MISSING_* values")
    args = parser.parse_args()

    token = _resolve_token(args)
    if not token:
        print("[ERROR] WEBEX_ACCESS_TOKEN no esta definido (ni --token/--token-file).")
        return 2

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = Path(args.log_file) if args.log_file else Path("actions/logs") / f"apply_runner_{timestamp}.log"
    report_file = Path(args.report_file) if args.report_file else Path("actions/logs") / f"apply_runner_{timestamp}.json"
    logger = build_logger(log_file)

    context = _load_context(Path(args.context_file) if args.context_file else None)
    logger.info("Ejecutando acciones en modo apply...")
    logger.info("Log consolidado: %s", log_file)
    logger.info("Reporte JSON: %s", report_file)
    if context:
        logger.info("Context file cargado: %s", args.context_file)

    failures: list[str] = []
    results: list[dict[str, Any]] = []
    repo_root = Path(__file__).resolve().parents[1]
    action_logs_dir = repo_root / "actions" / "logs"
    action_logs_dir.mkdir(parents=True, exist_ok=True)

    for script_name, payload in ACTIONS:
        resolved_payload, unresolved_keys = _replace_missing_vars(payload, context)
        action_log = action_logs_dir / f"{timestamp}_{script_name.replace('.py', '')}.log"
        cmd = [
            sys.executable,
            str(repo_root / "actions" / script_name),
            "--mode",
            "apply",
            "--token",
            token,
            "--vars",
            json.dumps(resolved_payload, ensure_ascii=False),
            "--log-file",
            str(action_log),
        ]
        logger.info("ACTION START: %s", script_name)
        if unresolved_keys:
            logger.warning("Unresolved vars en payload (%s): %s", script_name, ", ".join(unresolved_keys))
        proc = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)
        if proc.stdout:
            logger.info("STDOUT [%s]\n%s", script_name, proc.stdout.strip())
        if proc.stderr:
            logger.info("STDERR [%s]\n%s", script_name, proc.stderr.strip())

        calls = _parse_api_calls(action_log)
        ok_calls = sum(1 for item in calls if 200 <= int(item["status"]) < 300)
        failed_calls = len(calls) - ok_calls
        result = {
            "script": script_name,
            "exit_code": proc.returncode,
            "payload": resolved_payload,
            "unresolved_vars": unresolved_keys,
            "action_log": str(action_log),
            "calls_total": len(calls),
            "calls_ok_2xx": ok_calls,
            "calls_non_2xx": failed_calls,
            "calls": calls,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
        results.append(result)

        action_failed = proc.returncode != 0 or failed_calls > 0
        if action_failed:
            failures.append(script_name)
            logger.error(
                "ACTION FAILED: %s (exit_code=%s, 2xx_calls=%s, non_2xx_calls=%s)",
                script_name,
                proc.returncode,
                ok_calls,
                failed_calls,
            )
            if not args.continue_on_error:
                logger.error("Fallo en una accion. Se detiene el runner (fail-fast).")
                #break
        else:
            logger.info("ACTION OK: %s (2xx_calls=%s)", script_name, ok_calls)

    report_payload = {
        "generated_at": datetime.now().isoformat(),
        "log_file": str(log_file),
        "context_file": args.context_file,
        "failures": failures,
        "actions": results,
    }
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if failures:
        logger.error("Runner finalizado con errores en %s accion(es): %s", len(failures), ", ".join(failures))
        logger.error("Resultado final del log consolidado: %s", log_file)
        return 1

    logger.info("Runner completado sin errores.")
    logger.info("Resultado final del log consolidado: %s", log_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

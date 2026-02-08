#!/usr/bin/env python3
"""Ejecuta todas las acciones en modo apply y guarda un log consolidado."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import logging
import os
from pathlib import Path
import subprocess
import sys

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


def build_logger(log_file: Path) -> logging.Logger:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    handlers = [logging.StreamHandler(sys.stdout), logging.FileHandler(log_file, encoding="utf-8")]
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=handlers, force=True)
    return logging.getLogger("apply_runner")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all apply actions with consolidated logging")
    parser.add_argument("--token", default=os.getenv("WEBEX_ACCESS_TOKEN"))
    parser.add_argument("--continue-on-error", action="store_true", help="Do not stop at first failing action")
    parser.add_argument("--log-file", default=None, help="Custom path for consolidated log file")
    args = parser.parse_args()

    if not args.token:
        print("[ERROR] WEBEX_ACCESS_TOKEN no esta definido.")
        return 2

    log_file = Path(args.log_file) if args.log_file else Path("actions/logs") / f"apply_runner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger = build_logger(log_file)
    logger.info("Ejecutando acciones en modo apply...")
    logger.info("Log consolidado: %s", log_file)

    failures: list[str] = []
    repo_root = Path(__file__).resolve().parents[1]
    for script_name, payload in ACTIONS:
        script_path = repo_root / "actions" / script_name
        cmd = [
            sys.executable,
            str(script_path),
            "--mode",
            "apply",
            "--token",
            args.token,
            "--vars",
            json.dumps(payload, ensure_ascii=False),
        ]
        logger.info("ACTION START: %s", script_name)
        logger.info("COMMAND: %s", " ".join(cmd))
        proc = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)
        if proc.stdout:
            logger.info("STDOUT [%s]\n%s", script_name, proc.stdout.strip())
        if proc.stderr:
            logger.info("STDERR [%s]\n%s", script_name, proc.stderr.strip())

        if proc.returncode != 0:
            failures.append(script_name)
            logger.error("ACTION FAILED: %s (exit_code=%s)", script_name, proc.returncode)
            if not args.continue_on_error:
                logger.error("Fallo en una accion. Se detiene el runner (fail-fast).")
                break
        else:
            logger.info("ACTION OK: %s", script_name)

    if failures:
        logger.error("Runner finalizado con errores en %s accion(es): %s", len(failures), ", ".join(failures))
        return 1

    logger.info("Runner completado sin errores.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Ejecuta una pasada dummy de todos los scripts action_*.py en modo probe."""

from __future__ import annotations

import glob
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _shared import _required_optional_vars  # noqa: E402

SAMPLE_VALUES: dict[str, str] = {
    "aa_name": "AA-LAB-MADRID",
    "assistant_person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9BU1NJU1RBTlQx",
    "device_model": "Cisco 8851",
    "dial_pattern": "+3491XXXXXXX",
    "dial_plan_name": "DP-LAB-INTERPLATFORM",
    "email": "dummy.user.lab@lab.example.com",
    "extension": "5101",
    "forward_destination": "+34915550123",
    "group_id": "Y2lzY29zcGFyazovL3VzL0dST1VQUy9HUk9VUDE=",
    "group_name": "LAB-GROUP-VOICE",
    "hunt_name": "HG-LAB-SOPORTE",
    "location_id": "Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OUy9NQURSSUQ=",
    "member_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9NRU1CRVIx",
    "person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9OT01JTkFMMQ==",
    "pickup_name": "PG-LAB-RECEPCION",
    "primary_number": "+34915550101",
    "principal_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9BRE1JTjE=",
    "queue_id": "Y2lzY29zcGFyazovL3VzL0NBTExfUVVFVUUvUTE=",
    "queue_name": "CQ-LAB-VENTAS",
    "role_id": "Y2lzY29zcGFyazovL3VzL1JPTEVTL1JPTEUx",
    "route_group_id": "Y2lzY29zcGFyazovL3VzL1JPVVRFX0dST1VQL1JHMQ==",
    "route_group_name": "RG-LAB-SBC",
    "schedule_name": "Horario-LAB-LV",
    "scope": "organization",
    "secondary_number": "+34915550222",
    "serial": "FTX1234LAB1",
    "target_person_id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9UQVJHRVQx",
    "trunk_id": "Y2lzY29zcGFyazovL3VzL1RSVU5LUy9UUlVOSzE=",
    "trunk_name": "TRUNK-LAB-MAIN",
    "workspace_id": "Y2lzY29zcGFyazovL3VzL1dPUktTUEFDRVMvV1Mx",
    "workspace_name": "WS-LAB-REUNIONES",
}


def load_spec(module_path: str):
    module_name = Path(module_path).stem
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module.SPEC


def vars_for_script(module_path: str) -> dict[str, str]:
    spec = load_spec(module_path)
    required, optional = _required_optional_vars(spec)
    keys = sorted(set(required + optional))
    return {key: SAMPLE_VALUES.get(key, f"sample_{key}") for key in keys}


def main() -> int:
    action_files = sorted(glob.glob("actions/action_*.py"))
    report_lines = ["# Dummy execution report", "", "Base URL: `http://127.0.0.1:9` (sin backend, espera `connection refused`).", ""]

    total_failures = 0
    for action_file in action_files:
        payload = vars_for_script(action_file)
        cmd = [
            "python",
            action_file,
            "--mode",
            "probe",
            "--base-url",
            "http://127.0.0.1:9",
            "--token",
            "DUMMY_TOKEN",
            "--timeout",
            "1",
            "--retries",
            "1",
            "--vars",
            json.dumps(payload, ensure_ascii=False),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        script_name = Path(action_file).name
        status = "OK" if proc.returncode in (0, 1) else "ERROR"
        if status == "ERROR":
            total_failures += 1
        report_lines.append(f"## {script_name}")
        report_lines.append(f"- command: `{' '.join(cmd)}`")
        report_lines.append(f"- exit_code: `{proc.returncode}` ({status})")
        stderr_tail = (proc.stderr or "").strip().splitlines()[-2:]
        stdout_tail = (proc.stdout or "").strip().splitlines()[-2:]
        if stdout_tail:
            report_lines.append("- stdout_tail:")
            for line in stdout_tail:
                report_lines.append(f"  - `{line}`")
        if stderr_tail:
            report_lines.append("- stderr_tail:")
            for line in stderr_tail:
                report_lines.append(f"  - `{line}`")
        report_lines.append("")

    report_path = Path("actions/dummy_execution_report.md")
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Reporte generado en {report_path}")
    return 1 if total_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

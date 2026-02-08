#!/usr/bin/env python3
"""Provisiona dependencias mínimas de laboratorio y genera comandos apply listos para ejecutar.

Objetivo:
- Crear usuarios dummy en servidor (opcional, modo apply).
- Descubrir IDs existentes del tenant (location, miembros, group/workspace si existen).
- Generar `actions/lab_context.json` y `actions/lab_apply_commands.sh` con `--vars` finales.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import requests

from generate_dummy_users import build_users

BASE_URL = "https://webexapis.com/v1"

DEFAULT_VALUES = {
    "aa_name": "AA-LAB-MADRID",
    "dial_pattern": "+3491XXXXXXX",
    "dial_plan_name": "DP-LAB-INTERPLATFORM",
    "forward_destination": "+34915550123",
    "group_name": "LAB-GROUP-VOICE",
    "hunt_name": "HG-LAB-SOPORTE",
    "pickup_name": "PG-LAB-RECEPCION",
    "queue_name": "CQ-LAB-VENTAS",
    "route_group_name": "RG-LAB-SBC",
    "schedule_name": "Horario-LAB-LV",
    "scope": "organization",
    "trunk_name": "TRUNK-LAB-MAIN",
    "workspace_name": "WS-LAB-REUNIONES",
    "device_model": "Cisco 8851",
}

ACTION_REQUIRED_VARS: dict[str, list[str]] = {
    "action_auto_attendant.py": ["aa_name", "extension", "location_id", "schedule_name"],
    "action_call_pickup_group.py": ["extension", "location_id", "member_id", "pickup_name"],
    "action_call_profiles.py": ["location_id"],
    "action_call_queue.py": ["extension", "location_id", "member_id", "queue_id", "queue_name"],
    "action_day_t_numbers_caller_id.py": ["location_id", "person_id", "primary_number"],
    "action_delegated_admin.py": ["principal_id", "role_id", "scope"],
    "action_devices.py": ["device_model", "workspace_id"],
    "action_group_assignment.py": ["group_id", "group_name", "member_id"],
    "action_hunt_group.py": ["extension", "hunt_name", "location_id", "member_id"],
    "action_internal_extensions_sbc.py": ["location_id", "route_group_id", "route_group_name", "trunk_id", "trunk_name"],
    "action_interplatform_dial_plan.py": ["dial_pattern", "dial_plan_name", "route_group_id"],
    "action_legacy_forwarding.py": ["forward_destination", "person_id"],
    "action_location_number_removal.py": ["location_id", "primary_number"],
    "action_manager_assistant.py": ["assistant_person_id", "person_id"],
    "action_monitoring.py": ["person_id", "target_person_id"],
    "action_nominal_users.py": ["extension", "person_id", "primary_number"],
    "action_secondary_numbers.py": ["extension", "person_id", "secondary_number"],
    "action_user_recording.py": ["person_id"],
    "action_workspaces.py": ["extension", "primary_number", "workspace_id"],
}


class Api:
    def __init__(self, token: str, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.s = requests.Session()
        self.s.headers.update({"Authorization": f"Bearer {token}", "Content-Type": "application/json"})

    def req(self, method: str, path: str, *, params: dict[str, Any] | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        r = self.s.request(method, f"{self.base_url}/{path.lstrip('/')}", params=params, json=payload, timeout=30)
        if r.status_code >= 400:
            raise RuntimeError(f"{method} {path} -> {r.status_code}: {r.text[:500]}")
        if not r.text:
            return {}
        try:
            return r.json()
        except ValueError:
            return {}


def first_item(items: list[dict[str, Any]]) -> dict[str, Any] | None:
    return items[0] if items else None


def build_context(api: Api, args: argparse.Namespace) -> dict[str, Any]:
    context: dict[str, Any] = dict(DEFAULT_VALUES)

    # location
    if args.location_id:
        context["location_id"] = args.location_id
    else:
        locations = api.req("GET", "locations").get("items", [])
        if not locations:
            raise RuntimeError("No hay locations en el tenant; crea una location y repite.")
        context["location_id"] = locations[0]["id"]

    # create or lookup users
    users = build_users(count=args.user_count, domain=args.domain, ext_start=args.ext_start, phone_prefix=args.phone_prefix)
    created: list[dict[str, Any]] = []
    for user in users:
        payload: dict[str, Any] = {
            "emails": [user.email],
            "displayName": user.display_name,
            "firstName": user.first_name,
            "lastName": user.last_name,
        }
        if args.org_id:
            payload["orgId"] = args.org_id
        if args.license_id:
            payload["licenses"] = args.license_id
        if args.location_id:
            payload["locationId"] = args.location_id
        if args.mode == "apply":
            try:
                api.req("POST", "people", payload=payload)
            except Exception as e:
                print(f"WARN create user {user.email}: {e}")
        try:
            found = api.req("GET", "people", params={"email": user.email}).get("items", [])
            if found:
                person = found[0]
                created.append({
                    "email": user.email,
                    "id": person.get("id"),
                    "extension": user.extension,
                    "primary_number": user.primary_number,
                })
        except Exception as e:
            print(f"WARN lookup user {user.email}: {e}")

    if len(created) < 2:
        raise RuntimeError("No se pudieron resolver al menos 2 usuarios (person_id/member_id) en el tenant.")

    context["users"] = created
    context["person_id"] = created[0]["id"]
    context["member_id"] = created[0]["id"]
    context["assistant_person_id"] = created[1]["id"]
    context["target_person_id"] = created[1]["id"]
    context["principal_id"] = created[0]["id"]
    context["extension"] = created[0]["extension"]
    context["primary_number"] = created[0]["primary_number"]
    context["secondary_number"] = created[1]["primary_number"]

    # optional discover dependencies
    roles = api.req("GET", "roles").get("items", [])
    if roles:
        context["role_id"] = roles[0].get("id", "")

    groups = api.req("GET", "groups").get("items", [])
    group = first_item(groups)
    if group:
        context["group_id"] = group.get("id", "")

    workspaces = api.req("GET", "workspaces").get("items", [])
    ws = first_item(workspaces)
    if ws:
        context["workspace_id"] = ws.get("id", "")

    route_groups = api.req("GET", "telephony/config/premPstn/routeGroups").get("routeGroups", [])
    rg = first_item(route_groups)
    if rg:
        context["route_group_id"] = rg.get("id", "")

    trunks = api.req("GET", "telephony/config/premPstn/trunks").get("trunks", [])
    trunk = first_item(trunks)
    if trunk:
        context["trunk_id"] = trunk.get("id", "")

    queues = api.req("GET", f"telephony/config/locations/{context['location_id']}/queues").get("queues", [])
    q = first_item(queues)
    if q:
        context["queue_id"] = q.get("id", "")

    return context


def generate_apply_commands(context: dict[str, Any]) -> str:
    lines = ["#!/usr/bin/env bash", "set -euo pipefail", "", 'export WEBEX_ACCESS_TOKEN="${WEBEX_ACCESS_TOKEN:?missing token}"', ""]
    for script_name, keys in ACTION_REQUIRED_VARS.items():
        payload = {k: context.get(k, f"MISSING_{k}") for k in keys}
        payload_json = json.dumps(payload, ensure_ascii=False)
        lines.append(f"python actions/{script_name} --mode apply --vars '{payload_json}'")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Prepara dependencias de laboratorio y genera comandos apply finales")
    p.add_argument("--mode", choices=["plan", "apply"], default="plan", help="plan=solo lookup/generación, apply=crea usuarios dummy")
    p.add_argument("--base-url", default=BASE_URL)
    p.add_argument("--token", default=None, help="WEBEX token (si no, usa env WEBEX_ACCESS_TOKEN)")
    p.add_argument("--org-id", default=None)
    p.add_argument("--location-id", default=None)
    p.add_argument("--license-id", action="append", default=[])
    p.add_argument("--user-count", type=int, default=3)
    p.add_argument("--domain", default="lab.example.com")
    p.add_argument("--ext-start", type=int, default=5101)
    p.add_argument("--phone-prefix", default="+3491555")
    p.add_argument("--context-output", default="actions/lab_context.json")
    p.add_argument("--commands-output", default="actions/lab_apply_commands.sh")
    args = p.parse_args()

    token = args.token or __import__("os").getenv("WEBEX_ACCESS_TOKEN")
    if not token:
        print("ERROR: falta token. Usa --token o WEBEX_ACCESS_TOKEN")
        return 2

    api = Api(token=token, base_url=args.base_url)
    context = build_context(api, args)

    context_path = Path(args.context_output)
    context_path.parent.mkdir(parents=True, exist_ok=True)
    context_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")

    commands = generate_apply_commands(context)
    commands_path = Path(args.commands_output)
    commands_path.write_text(commands, encoding="utf-8")
    commands_path.chmod(0o755)

    missing = sorted(k for k, v in context.items() if isinstance(v, str) and v.startswith("MISSING_"))
    print(f"Contexto generado: {context_path}")
    print(f"Comandos generados: {commands_path}")
    if missing:
        print("WARN faltan dependencias:", ", ".join(missing))
    print("Siguiente paso: revisar lab_context.json y ejecutar lab_apply_commands.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

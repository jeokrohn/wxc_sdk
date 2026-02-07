#!/usr/bin/env python3
"""Supresión de numeraciones de sede."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_location_number_removal",
    title="Supresión de numeraciones de sede",
    objective="Precheck mínimo y eliminación idempotente de números de inventario.",
    pre_post_notes=[
    "Paso previo: verificar que número no está asignado.",
    "Paso posterior: aceptar 404 como idempotente cuando aplique.",
    ],
    probe_calls=[
    ApiCall(name="probe_number_inventory", method="GET", path="telephony/config/locations/{location_id}/numbers", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="remove_numbers", method="DELETE", path="telephony/config/locations/{location_id}/numbers", payload={'phoneNumbers': ['{primary_number}']}, params=None, acceptable_statuses=(200, 204, 400, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

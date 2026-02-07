#!/usr/bin/env python3
"""Numeraciones secundarias."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_secondary_numbers",
    title="Numeraciones secundarias",
    objective="Prueba asignación/remoción de números secundarios en persona/workspace.",
    pre_post_notes=[
    "Paso previo: precheck de inventario de número.",
    "Paso posterior: verificación de asignación con GET numbers.",
    ],
    probe_calls=[
    ApiCall(name="probe_person_numbers", method="GET", path="telephony/config/people/{person_id}/numbers", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="update_person_numbers", method="PUT", path="telephony/config/people/{person_id}/numbers", payload={'extension': '{extension}', 'additionalNumbers': ['{secondary_number}']}, params=None, acceptable_statuses=(200, 204, 400, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

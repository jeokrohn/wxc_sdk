#!/usr/bin/env python3
"""Activación Día T + Caller ID."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_day_t_numbers_caller_id",
    title="Activación Día T + Caller ID",
    objective="Activa números de sede y aplica caller-id básico por entidad.",
    pre_post_notes=[
    "Paso previo: validar inventario y disponibilidad para external caller id.",
    "Paso posterior: leer caller-id final para comprobar cambio.",
    ],
    probe_calls=[
    ApiCall(name="probe_location_numbers", method="GET", path="telephony/config/locations/{location_id}/numbers", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="activate_numbers", method="POST", path="telephony/config/locations/{location_id}/numbers/actions/activate", payload={'phoneNumbers': ['{primary_number}']}, params=None, acceptable_statuses=(200, 202, 400, 404)),
    ApiCall(name="update_person_caller_id", method="PUT", path="telephony/config/people/{person_id}/callerId", payload={'selected': 'DIRECT_LINE', 'externalCallerIdNamePolicy': 'DIRECT_LINE'}, params=None, acceptable_statuses=(200, 204, 400, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

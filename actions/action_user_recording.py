#!/usr/bin/env python3
"""Servicios de grabación por usuario."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_user_recording",
    title="Servicios de grabación por usuario",
    objective="Actualiza grabación de usuario y captura errores comunes de licencia.",
    pre_post_notes=[
    "Paso previo: comprobar licencia/feature recording.",
    "Paso posterior: confirmar modo aplicado con GET.",
    ],
    probe_calls=[
    ApiCall(name="probe_recording", method="GET", path="telephony/config/people/{person_id}/callRecording", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="update_recording", method="PUT", path="telephony/config/people/{person_id}/callRecording", payload={'enabled': True, 'record': 'Always'}, params=None, acceptable_statuses=(200, 204, 400, 403, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

#!/usr/bin/env python3
"""Supervisión (BLF/monitoring)."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_monitoring",
    title="Supervisión (BLF/monitoring)",
    objective="Actualiza targets de monitoring y prueba errores de soporte/licencia.",
    pre_post_notes=[
    "Paso previo: precheck de licencia compatible.",
    "Paso posterior: validar lista completa de monitored elements.",
    ],
    probe_calls=[
    ApiCall(name="probe_monitoring", method="GET", path="telephony/config/people/{person_id}/monitoring", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="update_monitoring", method="PUT", path="telephony/config/people/{person_id}/monitoring", payload={'enableCallParkNotification': True, 'monitoredElements': [{'memberId': '{target_person_id}'}]}, params=None, acceptable_statuses=(200, 204, 400, 403, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

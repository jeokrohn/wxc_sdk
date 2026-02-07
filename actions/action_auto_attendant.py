#!/usr/bin/env python3
"""Auto Attendant."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_auto_attendant",
    title="Auto Attendant",
    objective="Orquesta prerequisitos simples (schedule/announcement) y upsert de auto attendant.",
    pre_post_notes=[
    "Paso previo: crear/usar schedule y announcement si faltan.",
    "Paso posterior: validar menús y horario en lectura final.",
    ],
    probe_calls=[
    ApiCall(name="probe_auto_attendant_list", method="GET", path="telephony/config/locations/{location_id}/autoAttendants", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="upsert_auto_attendant", method="POST", path="telephony/config/locations/{location_id}/autoAttendants", payload={'name': '{aa_name}', 'extension': '{extension}', 'businessSchedule': '{schedule_name}'}, params=None, acceptable_statuses=(200, 201, 400, 404, 409)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

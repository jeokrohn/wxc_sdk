#!/usr/bin/env python3
"""Manager-Assistant."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_manager_assistant",
    title="Manager-Assistant",
    objective="Configura relación executive/assistants usando update idempotente completo.",
    pre_post_notes=[
    "Paso previo: resolver executive/assistants por email.",
    "Paso posterior: releer configuración para verificar roles/políticas.",
    ],
    probe_calls=[
    ApiCall(name="probe_exec_assistant", method="GET", path="telephony/config/people/{person_id}/executiveAssistant", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="update_exec_assistant", method="PUT", path="telephony/config/people/{person_id}/executiveAssistant", payload={'enabled': True, 'assistants': ['{assistant_person_id}']}, params=None, acceptable_statuses=(200, 204, 400, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

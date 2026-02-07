#!/usr/bin/env python3
"""Asignación automática de grupos."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_group_assignment",
    title="Asignación automática de grupos",
    objective="Valida lookup y upsert de grupos + membresías idempotentes.",
    pre_post_notes=[
    "Paso previo: resolver group_id por nombre.",
    "Paso posterior: sincronizar miembros (add/remove) de forma idempotente.",
    ],
    probe_calls=[
    ApiCall(name="lookup_group", method="GET", path="groups", payload=None, params={'displayName': '{group_name}'}, acceptable_statuses=(200,)),
    ApiCall(name="probe_membership_add", method="POST", path="groups/{group_id}/members", payload={'members': [{'id': '{member_id}'}]}, params=None, acceptable_statuses=(200, 201, 400, 404)),
    ],
    apply_calls=[
    ApiCall(name="upsert_group", method="POST", path="groups", payload={'displayName': '{group_name}'}, params=None, acceptable_statuses=(200, 201, 400, 409)),
    ApiCall(name="add_membership", method="POST", path="groups/{group_id}/members", payload={'members': [{'id': '{member_id}'}]}, params=None, acceptable_statuses=(200, 201, 400, 404, 409)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

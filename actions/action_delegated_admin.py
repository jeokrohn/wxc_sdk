#!/usr/bin/env python3
"""Gestores delegados (out_of_scope)."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_delegated_admin",
    title="Gestores delegados (out_of_scope)",
    objective="Documenta y prueba de viabilidad mínima para delegated admin (sin contrato estable en SDK).",
    pre_post_notes=[
    "Paso previo: confirmar endpoint oficial soportado en tenant/version.",
    "Paso posterior: si no existe contrato estable => marcar out_of_scope.",
    ],
    probe_calls=[
    ApiCall(name="probe_org_roles", method="GET", path="roles", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="attempt_delegate_assignment", method="POST", path="roleAssignments", payload={'roleId': '{role_id}', 'principalId': '{principal_id}', 'scope': '{scope}'}, params=None, acceptable_statuses=(200, 201, 400, 404, 405)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

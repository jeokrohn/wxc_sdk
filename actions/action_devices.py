#!/usr/bin/env python3
"""Dispositivos (alta/asignación/activation)."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_devices",
    title="Dispositivos (alta/asignación/activation)",
    objective="Prueba alta o asignación de dispositivos con payload mínimo.",
    pre_post_notes=[
    "Paso previo: lookup por serial/MAC.",
    "Paso posterior: confirmar asignación a persona/workspace.",
    ],
    probe_calls=[
    ApiCall(name="probe_devices", method="GET", path="devices", payload=None, params={'serial': '{serial}'}, acceptable_statuses=(200,)),
    ],
    apply_calls=[
    ApiCall(name="create_or_assign_device", method="POST", path="devices", payload={'model': '{device_model}', 'workspaceId': '{workspace_id}'}, params=None, acceptable_statuses=(200, 201, 400, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

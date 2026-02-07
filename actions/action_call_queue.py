#!/usr/bin/env python3
"""Call Queue."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_call_queue",
    title="Call Queue",
    objective="Create/update de cola y actualización de agentes en segundo paso.",
    pre_post_notes=[
    "Paso previo: validar location y announcement opcional.",
    "Paso posterior: actualizar agentes de la cola.",
    ],
    probe_calls=[
    ApiCall(name="probe_queue_list", method="GET", path="telephony/config/locations/{location_id}/queues", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="upsert_queue", method="POST", path="telephony/config/locations/{location_id}/queues", payload={'name': '{queue_name}', 'extension': '{extension}', 'callPolicies': {'policy': 'SIMULTANEOUS'}}, params=None, acceptable_statuses=(200, 201, 400, 404, 409)),
    ApiCall(name="queue_agents_update", method="PUT", path="telephony/config/locations/{location_id}/queues/{queue_id}/agents", payload={'agents': [{'id': '{member_id}'}]}, params=None, acceptable_statuses=(200, 204, 400, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

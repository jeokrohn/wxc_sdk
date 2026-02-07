#!/usr/bin/env python3
"""Hunt Group."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_hunt_group",
    title="Hunt Group",
    objective="Create/update de hunt group con política de routing y miembros.",
    pre_post_notes=[
    "Paso previo: lookup del hunt group.",
    "Paso posterior: comprobar política y miembros.",
    ],
    probe_calls=[
    ApiCall(name="probe_hunt_list", method="GET", path="telephony/config/locations/{location_id}/huntGroups", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="upsert_hunt_group", method="POST", path="telephony/config/locations/{location_id}/huntGroups", payload={'name': '{hunt_name}', 'extension': '{extension}', 'callPolicies': {'policy': 'REGULAR'}, 'agents': ['{member_id}']}, params=None, acceptable_statuses=(200, 201, 400, 404, 409)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

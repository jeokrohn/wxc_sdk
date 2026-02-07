#!/usr/bin/env python3
"""Call Pickup Group."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_call_pickup_group",
    title="Call Pickup Group",
    objective="Create/update de call pickup group y sincronización de miembros.",
    pre_post_notes=[
    "Paso previo: lookup por location+name/extension.",
    "Paso posterior: releer grupo para validar miembros.",
    ],
    probe_calls=[
    ApiCall(name="probe_pickup_list", method="GET", path="telephony/config/locations/{location_id}/callPickups", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="upsert_pickup", method="POST", path="telephony/config/locations/{location_id}/callPickups", payload={'name': '{pickup_name}', 'extension': '{extension}', 'agents': ['{member_id}']}, params=None, acceptable_statuses=(200, 201, 400, 404, 409)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

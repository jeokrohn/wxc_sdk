#!/usr/bin/env python3
"""Alta/modificación de workspaces."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_workspaces",
    title="Alta/modificación de workspaces",
    objective="Lookup/create/update de workspace y update de numeración de calling.",
    pre_post_notes=[
    "Paso previo: lookup por displayName o externalId.",
    "Paso posterior: verificar settings de números del workspace.",
    ],
    probe_calls=[
    ApiCall(name="lookup_workspace", method="GET", path="workspaces", payload=None, params={'displayName': '{workspace_name}'}, acceptable_statuses=(200,)),
    ApiCall(name="probe_workspace_numbers_missing", method="PUT", path="telephony/config/workspaces/{workspace_id}/numbers", payload={'extension': '2001'}, params=None, acceptable_statuses=(200, 204, 400, 404)),
    ],
    apply_calls=[
    ApiCall(name="update_workspace_numbers", method="PUT", path="telephony/config/workspaces/{workspace_id}/numbers", payload={'extension': '{extension}', 'primaryNumber': '{primary_number}'}, params=None, acceptable_statuses=(200, 204, 400, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

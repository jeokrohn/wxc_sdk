#!/usr/bin/env python3
"""Alta/modificación de usuarios nominales post-LDAP."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_nominal_users",
    title="Alta/modificación de usuarios nominales post-LDAP",
    objective="Resuelve usuario por email y prueba updates de calling/números sin crear identidad.",
    pre_post_notes=[
    "Paso previo: lookup de person por email.",
    "Paso posterior: aplicar números/caller-id solo si user existe.",
    ],
    probe_calls=[
    ApiCall(name="lookup_user", method="GET", path="people", payload=None, params={'email': '{email}'}, acceptable_statuses=(200,)),
    ApiCall(name="probe_user_numbers_missing", method="PUT", path="telephony/config/people/{person_id}/numbers", payload={'extension': '1001'}, params=None, acceptable_statuses=(200, 204, 400, 404)),
    ],
    apply_calls=[
    ApiCall(name="update_user_numbers", method="PUT", path="telephony/config/people/{person_id}/numbers", payload={'extension': '{extension}', 'primaryNumber': '{primary_number}'}, params=None, acceptable_statuses=(200, 204, 400, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

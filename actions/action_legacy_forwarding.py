#!/usr/bin/env python3
"""Desvíos Webex → Legacy."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_legacy_forwarding",
    title="Desvíos Webex → Legacy",
    objective="Configura o desconfigura desvío a prefijo legacy (ej. 53) en persona/workspace.",
    pre_post_notes=[
    "Paso previo: comprobar que el prefijo legacy enruta en dial plan.",
    "Paso posterior: validar forwarding final en lectura de settings.",
    ],
    probe_calls=[
    ApiCall(name="probe_forwarding", method="GET", path="telephony/config/people/{person_id}/callForwarding", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="update_forwarding", method="PUT", path="telephony/config/people/{person_id}/callForwarding", payload={'enabled': True, 'destination': '{forward_destination}'}, params=None, acceptable_statuses=(200, 204, 400, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

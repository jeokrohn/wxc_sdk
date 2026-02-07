#!/usr/bin/env python3
"""Perfiles de llamada."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_call_profiles",
    title="Perfiles de llamada",
    objective="Actualiza perfiles de llamada de location/person/workspace según payload simplificado.",
    pre_post_notes=[
    "Paso previo: confirmar entidad destino y licencia.",
    "Paso posterior: releer configuración para confirmar estado final.",
    ],
    probe_calls=[
    ApiCall(name="probe_location_calling", method="GET", path="telephony/config/locations/{location_id}/callingBehavior", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="update_location_calling", method="PUT", path="telephony/config/locations/{location_id}/callingBehavior", payload={'callingLineId': {'selection': 'DIRECT_LINE'}}, params=None, acceptable_statuses=(200, 204, 400, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

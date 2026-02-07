#!/usr/bin/env python3
"""Intercomunicación Webex ↔ Legacy (Dial Plan)."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_interplatform_dial_plan",
    title="Intercomunicación Webex ↔ Legacy (Dial Plan)",
    objective="Valida y aplica reglas de dial plan contra Legacy con control básico de colisiones vía respuesta API.",
    pre_post_notes=[
    "Paso previo: validar trunk/route_group destino.",
    "Paso posterior: comprobar regla creada/actualizada con GET por id.",
    ],
    probe_calls=[
    ApiCall(name="probe_dial_plan_list", method="GET", path="telephony/config/dialPlans", payload=None, params=None, acceptable_statuses=(200,)),
    ApiCall(name="probe_invalid_target", method="POST", path="telephony/config/dialPlans", payload={'name': 'probe-invalid', 'routeType': 'ROUTE_GROUP', 'routeId': 'invalid-id', 'dialPatterns': ['53XXXX']}, params=None, acceptable_statuses=(200, 201, 400, 404)),
    ],
    apply_calls=[
    ApiCall(name="create_or_update_dial_plan", method="POST", path="telephony/config/dialPlans", payload={'name': '{dial_plan_name}', 'routeType': 'ROUTE_GROUP', 'routeId': '{route_group_id}', 'dialPatterns': ['{dial_pattern}']}, params=None, acceptable_statuses=(200, 201, 400, 409)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

#!/usr/bin/env python3
"""Enrutamiento de extensiones desconocidas a SBC."""

from _shared import ActionSpec, ApiCall, run_action_spec

SPEC = ActionSpec(
    key="action_internal_extensions_sbc",
    title="Enrutamiento de extensiones desconocidas a SBC",
    objective="Valida y ejecuta trunk + route group + internal dialing para enrutar extensiones internas desconocidas.",
    pre_post_notes=[
    "Paso previo: confirmar trunk/route_group existentes o crearlos.",
    "Paso posterior: verificar internal_dialing de la sede y PSTN asociado.",
    ],
    probe_calls=[
    ApiCall(name="probe_missing_location", method="GET", path="telephony/config/locations/{location_id}/internalDialing", payload=None, params=None, acceptable_statuses=(200, 404)),
    ApiCall(name="probe_missing_route_group", method="GET", path="telephony/config/premisePstn/routeGroups/{route_group_id}", payload=None, params=None, acceptable_statuses=(200, 404)),
    ],
    apply_calls=[
    ApiCall(name="upsert_trunk_like", method="POST", path="telephony/config/premisePstn/trunks", payload={'name': '{trunk_name}', 'dualIdentitySupportEnabled': False}, params=None, acceptable_statuses=(200, 201, 400, 409)),
    ApiCall(name="upsert_route_group_like", method="POST", path="telephony/config/premisePstn/routeGroups", payload={'name': '{route_group_name}', 'trunkIds': ['{trunk_id}']}, params=None, acceptable_statuses=(200, 201, 400, 409)),
    ApiCall(name="update_internal_dialing", method="PUT", path="telephony/config/locations/{location_id}/internalDialing", payload={'enableUnknownExtensionRoutePolicy': True, 'unknownExtensionRouteIdentity': '{route_group_id}'}, params=None, acceptable_statuses=(200, 204, 400, 404)),
    ],
)


if __name__ == "__main__":
    raise SystemExit(run_action_spec(SPEC))

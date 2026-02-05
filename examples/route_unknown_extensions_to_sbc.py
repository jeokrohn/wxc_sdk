#!/usr/bin/env python
"""
Monolithic TDD-style script for routing unknown internal extensions to an SBC.

Task A: Enrutamiento de extensiones internas desconocidas de la sede hacia SBC.
"""

from __future__ import annotations

import json
import logging
import os
from difflib import unified_diff
from typing import Any

from dotenv import load_dotenv

from wxc_sdk import WebexSimpleApi
from wxc_sdk.common import RouteIdentity, RouteType
from wxc_sdk.telephony.location import PSTNConnection, TelephonyLocation
from wxc_sdk.telephony.location.internal_dialing import InternalDialing
from wxc_sdk.telephony.prem_pstn.route_group import RGTrunk, RouteGroup
from wxc_sdk.telephony.prem_pstn.trunk import TrunkType

load_dotenv(override=True)

# Variables requeridas (campos de prueba)
ORG_ID = os.getenv("WXC_ORG_ID")
LOCATION_ID = os.getenv("WXC_LOCATION_ID")
TRUNK_NAME = os.getenv("WXC_TRUNK_NAME", "SBC-Trunk-A")
TRUNK_PASSWORD = os.getenv("WXC_TRUNK_PASSWORD")
TRUNK_TYPE = os.getenv("WXC_TRUNK_TYPE", TrunkType.registering.value)
TRUNK_ADDRESS = os.getenv("WXC_TRUNK_ADDRESS")
TRUNK_DOMAIN = os.getenv("WXC_TRUNK_DOMAIN")
TRUNK_PORT = int(os.getenv("WXC_TRUNK_PORT", "0")) or None
TRUNK_MAX_CONCURRENT_CALLS = int(os.getenv("WXC_TRUNK_MAX_CONCURRENT_CALLS", "0")) or None
ROUTE_GROUP_NAME = os.getenv("WXC_ROUTE_GROUP_NAME", "SBC-Route-Group-A")
ROUTE_GROUP_PRIORITY = int(os.getenv("WXC_ROUTE_GROUP_PRIORITY", "1"))
ROUTING_PREFIX = os.getenv("WXC_ROUTING_PREFIX")
OUTSIDE_DIAL_DIGIT = os.getenv("WXC_OUTSIDE_DIAL_DIGIT")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOGGER = logging.getLogger("route_unknown_extensions")


def log_diff_A(label: str, before: Any, after: Any) -> None:
    """Log a unified diff for JSON-serializable payloads."""
    before_json = json.dumps(before, indent=2, sort_keys=True, default=str).splitlines(keepends=True)
    after_json = json.dumps(after, indent=2, sort_keys=True, default=str).splitlines(keepends=True)
    diff = "".join(unified_diff(before_json, after_json, fromfile=f"{label}-before", tofile=f"{label}-after"))
    if diff:
        LOGGER.info("%s diff:\n%s", label, diff)
    else:
        LOGGER.info("%s diff: sin cambios", label)


def validate_env_A() -> None:
    """Validar variables mínimas requeridas para la tarea A."""
    missing = [name for name, value in {
        "WXC_LOCATION_ID": LOCATION_ID,
        "WXC_TRUNK_PASSWORD": TRUNK_PASSWORD,
    }.items() if not value]
    if TrunkType(TRUNK_TYPE) == TrunkType.certificate_base:
        missing.extend(
            name
            for name, value in {
                "WXC_TRUNK_ADDRESS": TRUNK_ADDRESS,
                "WXC_TRUNK_DOMAIN": TRUNK_DOMAIN,
                "WXC_TRUNK_PORT": TRUNK_PORT,
                "WXC_TRUNK_MAX_CONCURRENT_CALLS": TRUNK_MAX_CONCURRENT_CALLS,
            }.items()
            if not value
        )
    if missing:
        raise ValueError(f"Faltan variables requeridas: {', '.join(missing)}")


def create_trunk_A(api: WebexSimpleApi) -> str:
    """Subtarea A1: crear trunk hacia SBC y validar."""
    trunk_type = TrunkType(TRUNK_TYPE)
    LOGGER.info("Creando trunk '%s' (tipo=%s)", TRUNK_NAME, trunk_type.value)
    trunk_id = api.telephony.prem_pstn.trunk.create(
        name=TRUNK_NAME,
        location_id=LOCATION_ID,
        password=TRUNK_PASSWORD,
        trunk_type=trunk_type,
        address=TRUNK_ADDRESS,
        domain=TRUNK_DOMAIN,
        port=TRUNK_PORT,
        max_concurrent_calls=TRUNK_MAX_CONCURRENT_CALLS,
        org_id=ORG_ID,
    )

    trunk_details = api.telephony.prem_pstn.trunk.details(trunk_id=trunk_id, org_id=ORG_ID)
    log_diff_A("trunk", {}, trunk_details.model_dump(mode="json", by_alias=True))
    assert trunk_details.name == TRUNK_NAME, "Nombre de trunk no coincide"
    assert trunk_details.location.id == LOCATION_ID, "Location del trunk no coincide"
    return trunk_id


def create_route_group_A(api: WebexSimpleApi, trunk_id: str) -> str:
    """Subtarea A2: crear route group con el trunk y validar."""
    LOGGER.info("Creando route group '%s' con trunk '%s'", ROUTE_GROUP_NAME, trunk_id)
    route_group = RouteGroup(
        name=ROUTE_GROUP_NAME,
        local_gateways=[RGTrunk(trunk_id=trunk_id, priority=ROUTE_GROUP_PRIORITY)],
    )
    route_group_id = api.telephony.prem_pstn.route_group.create(route_group=route_group, org_id=ORG_ID)

    route_group_details = api.telephony.prem_pstn.route_group.details(rg_id=route_group_id, org_id=ORG_ID)
    log_diff_A("route_group", {}, route_group_details.model_dump(mode="json", by_alias=True))
    assert route_group_details.name == ROUTE_GROUP_NAME, "Nombre de route group no coincide"
    assert route_group_details.local_gateways, "Route group no tiene trunks asociados"
    return route_group_id


def update_location_pstn_A(api: WebexSimpleApi, route_group_id: str) -> None:
    """Subtarea A3: configurar PSTN de sede como ROUTE_GROUP y validar."""
    before = api.telephony.location.details(location_id=LOCATION_ID, org_id=ORG_ID)
    LOGGER.info("Actualizando PSTN en location '%s' hacia route group '%s'", LOCATION_ID, route_group_id)

    settings = TelephonyLocation(
        connection=PSTNConnection(type=RouteType.route_group, id=route_group_id),
        routing_prefix=ROUTING_PREFIX,
        outside_dial_digit=OUTSIDE_DIAL_DIGIT,
    )
    api.telephony.location.update(location_id=LOCATION_ID, settings=settings, org_id=ORG_ID)

    after = api.telephony.location.details(location_id=LOCATION_ID, org_id=ORG_ID)
    log_diff_A(
        "location_pstn",
        before.model_dump(mode="json", by_alias=True),
        after.model_dump(mode="json", by_alias=True),
    )
    assert after.connection and after.connection.type == RouteType.route_group, "PSTN no es ROUTE_GROUP"
    assert after.connection.id == route_group_id, "PSTN no apunta al route group esperado"


def update_internal_dialing_A(api: WebexSimpleApi, route_group_id: str) -> None:
    """Subtarea A4: habilitar ruta de extensiones desconocidas y validar."""
    before = api.telephony.location.internal_dialing.read(location_id=LOCATION_ID, org_id=ORG_ID)
    LOGGER.info("Habilitando route unknown extensions hacia route group '%s'", route_group_id)

    update = InternalDialing(
        enable_unknown_extension_route_policy=True,
        unknown_extension_route_identity=RouteIdentity(route_id=route_group_id, route_type=RouteType.route_group),
    )
    api.telephony.location.internal_dialing.update(location_id=LOCATION_ID, update=update, org_id=ORG_ID)

    after = api.telephony.location.internal_dialing.read(location_id=LOCATION_ID, org_id=ORG_ID)
    log_diff_A(
        "internal_dialing",
        before.model_dump(mode="json", by_alias=True),
        after.model_dump(mode="json", by_alias=True),
    )
    assert after.enable_unknown_extension_route_policy is True, "No se habilitó route unknown extensions"
    assert after.unknown_extension_route_identity, "No hay identidad de ruta configurada"
    assert after.unknown_extension_route_identity.route_id == route_group_id, "Route group no coincide"


def run_tdd_sequence_A() -> None:
    """Flujo TDD principal: crear, validar y configurar paso a paso."""
    validate_env_A()
    api = WebexSimpleApi()

    trunk_id = create_trunk_A(api)
    route_group_id = create_route_group_A(api, trunk_id=trunk_id)
    update_location_pstn_A(api, route_group_id=route_group_id)
    update_internal_dialing_A(api, route_group_id=route_group_id)

    LOGGER.info("Tarea A completada correctamente.")


if __name__ == "__main__":
    run_tdd_sequence_A()

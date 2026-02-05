from dataclasses import dataclass
from typing import Optional

from wxc_sdk.people import Person
from wxc_sdk.workspaces import Workspace


def parse_semicolon_list(value: Optional[str]) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(";") if item.strip()]


def email_display_name(email: str) -> str:
    local = email.split("@")[0]
    return local.replace(".", " ").replace("_", " ").title()


@dataclass(frozen=True)
class LocationIdentity:
    location_id: Optional[str]
    location_name: Optional[str]
    external_id: Optional[str]


def build_person(*, email: str, location_id: str, licenses: Optional[list[str]] = None) -> Person:
    return Person(
        emails=[email],
        display_name=email_display_name(email),
        location_id=location_id,
        licenses=licenses,
    )


def build_workspace(
    *,
    display_name: str,
    location_id: str,
    external_id: Optional[str],
    licenses: Optional[list[str]] = None,
) -> Workspace:
    return Workspace(
        display_name=display_name,
        location_id=location_id,
        external_id=external_id,
        licenses=licenses,
    )

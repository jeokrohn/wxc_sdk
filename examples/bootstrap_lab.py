#!/usr/bin/env python
"""
Bootstrap a small Webex Calling lab (2 locations + users + extensions).

This script is meant for sandbox use. It will:
1) Create or reuse two locations.
2) Enable each location for Webex Calling.
3) Create or reuse users with calling extensions.
4) Log counts before/after to verify remote changes.

Requirements:
* WEBEX_ACCESS_TOKEN (or a service app token) in the environment.
* CALLING_LICENSE_ID or CALLING_LICENSE_NAME for assigning a calling license to users.

Optional environment variables:
* ORG_ID: override organization to use.
* USER_EMAIL_DOMAIN: email domain for generated users (default: example.com).
"""
from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
import re
from typing import Iterable, Optional

from dotenv import load_dotenv

from wxc_sdk import WebexSimpleApi
from wxc_sdk.people import Person
from wxc_sdk.rest import RestError


@dataclass(frozen=True)
class LocationSeed:
    name: str
    time_zone: str
    preferred_language: str
    announcement_language: str
    address1: str
    city: str
    state: str
    postal_code: str
    country: str


@dataclass(frozen=True)
class UserSeed:
    email: str
    extension: str
    location_name: str


LOCATION_SEEDS = [
    LocationSeed(
        name="Lab Location A",
        time_zone="America/Los_Angeles",
        preferred_language="en_US",
        announcement_language="en_US",
        address1="100 Main St",
        city="San Jose",
        state="CA",
        postal_code="95110",
        country="US",
    ),
    LocationSeed(
        name="Lab Location B",
        time_zone="America/Los_Angeles",
        preferred_language="en_US",
        announcement_language="en_US",
        address1="200 Market St",
        city="San Jose",
        state="CA",
        postal_code="95112",
        country="US",
    ),
]


def build_user_seeds(domain: str) -> list[UserSeed]:
    return [
        UserSeed(email=f"lab.user1@{domain}", extension="3001", location_name="Lab Location A"),
        UserSeed(email=f"lab.user2@{domain}", extension="3002", location_name="Lab Location A"),
        UserSeed(email=f"lab.user3@{domain}", extension="4001", location_name="Lab Location B"),
        UserSeed(email=f"lab.user4@{domain}", extension="4002", location_name="Lab Location B"),
    ]


def email_display_name(email: str) -> str:
    local = email.split("@")[0]
    return local.replace(".", " ").replace("_", " ").title()


def resolve_org_id(api: WebexSimpleApi, override: Optional[str]) -> str:
    if override:
        return override
    orgs = api.organizations.list()
    if not orgs:
        raise RuntimeError("No organizations available for this token.")
    return orgs[0].org_id


def resolve_calling_license(api: WebexSimpleApi) -> str:
    license_id = os.getenv("CALLING_LICENSE_ID")
    if license_id:
        return license_id
    license_name = os.getenv("CALLING_LICENSE_NAME")
    licenses = api.licenses.list()
    if license_name:
        matched = next((lic for lic in licenses if lic.name == license_name), None)
        if matched:
            return matched.license_id
        available = ", ".join(sorted(lic.name for lic in licenses))
        raise RuntimeError(f'License "{license_name}" not found. Available: {available}')

    calling_license = next(
        (lic for lic in licenses if "calling" in lic.name.lower()),
        None,
    )
    if calling_license:
        print(f'Auto-selected calling license "{calling_license.name}".')
        return calling_license.license_id
    available = ", ".join(sorted(lic.name for lic in licenses))
    raise RuntimeError(
        "No calling license found. Set CALLING_LICENSE_ID or CALLING_LICENSE_NAME. "
        f"Available licenses: {available}"
    )


def ensure_locations(api: WebexSimpleApi, org_id: str, dry_run: bool) -> dict[str, str]:
    existing = {loc.name: loc for loc in api.locations.list()}
    location_ids: dict[str, str] = {}
    for seed in LOCATION_SEEDS:
        if seed.name in existing:
            location_ids[seed.name] = existing[seed.name].location_id
            continue
        if dry_run:
            print(f"[dry-run] Create location: {seed.name}")
            location_ids[seed.name] = f"dry-run:{seed.name}"
            continue
        location_id = api.locations.create(
            name=seed.name,
            time_zone=seed.time_zone,
            preferred_language=seed.preferred_language,
            announcement_language=seed.announcement_language,
            address1=seed.address1,
            city=seed.city,
            state=seed.state,
            postal_code=seed.postal_code,
            country=seed.country,
            org_id=org_id,
        )
        location_ids[seed.name] = location_id
    return location_ids


def enable_locations_for_calling(
    api: WebexSimpleApi,
    location_ids: dict[str, str],
    dry_run: bool,
) -> None:
    for name, location_id in location_ids.items():
        try:
            api.telephony.location.details(location_id=location_id)
            print(f"Calling already enabled for location: {name}")
            continue
        except RestError:
            if dry_run:
                print(f"[dry-run] Enable location for calling: {name}")
                continue
        location = api.locations.details(location_id=location_id)
        enabled_id = api.telephony.location.enable_for_calling(location=location)
        print(f"Enabled location for calling: {name} ({enabled_id})")


def prompt_confirm(message: str) -> bool:
    response = input(f"{message} [y/N]: ").strip().lower()
    return response in {"y", "yes"}


def prompt_non_empty(message: str, default: Optional[str] = None) -> str:
    while True:
        raw = input(f"{message}{' [' + default + ']' if default else ''}: ").strip()
        if not raw and default:
            return default
        if raw:
            return raw
        print("Value is required.")


def prompt_user_seeds(domain: str) -> list[UserSeed]:
    print("Enter lab users (LDAP-style email + long extension). Type 'done' to finish.")
    users: list[UserSeed] = []
    email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    ext_re = re.compile(r"^\d{4,}$")
    while True:
        email = input("User email (or 'done'): ").strip()
        if email.lower() == "done":
            break
        if not email and domain:
            print("Email is required.")
            continue
        if email and not email_re.match(email):
            print("Invalid email format.")
            continue
        extension = input("User extension (digits, >=4): ").strip()
        if not ext_re.match(extension):
            print("Invalid extension format.")
            continue
        location_name = prompt_non_empty("Location name for user")
        users.append(UserSeed(email=email, extension=extension, location_name=location_name))
    return users


def log_user_counts(api: WebexSimpleApi, users: Iterable[UserSeed], label: str) -> None:
    count = 0
    for seed in users:
        count += len(list(api.people.list(email=seed.email)))
    print(f"{label} users (by email): {count}")


def validate_person_create(person: Person) -> None:
    if not person.emails:
        raise ValueError("Person payload must include at least one email.")
    if not person.display_name:
        raise ValueError("Person payload must include display_name.")
    if not person.extension:
        raise ValueError("Person payload must include extension.")
    if not person.location_id:
        raise ValueError("Person payload must include location_id.")
    if not person.licenses:
        raise ValueError("Person payload must include licenses.")


def validate_person_response(person: Person) -> None:
    if not person.person_id:
        raise ValueError("Person response missing person_id.")
    if not person.display_name:
        raise ValueError("Person response missing display_name.")


def ensure_users(
    api: WebexSimpleApi,
    users: Iterable[UserSeed],
    location_ids: dict[str, str],
    calling_license_id: str,
    dry_run: bool,
) -> None:
    for seed in users:
        existing = list(api.people.list(email=seed.email))
        if existing:
            print(f"User exists: {seed.email}")
            continue
        location_id = location_ids.get(seed.location_name)
        if location_id is None:
            raise RuntimeError(f"Unknown location: {seed.location_name}")
        person = Person(
            emails=[seed.email],
            display_name=email_display_name(seed.email),
            extension=seed.extension,
            location_id=location_id,
            licenses=[calling_license_id],
        )
        validate_person_create(person)
        print(f"Prepared create payload for {seed.email}: {person.create_update()}")
        if dry_run:
            print(f"[dry-run] Create user: {seed.email} (ext {seed.extension})")
            continue
        created = api.people.create(person, calling_data=True)
        validate_person_response(created)
        print(f"Created user: {created.display_name} ({created.person_id})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap a small Webex Calling lab.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without applying changes.")
    parser.add_argument("--org-id", default=os.getenv("ORG_ID"), help="Override organization ID.")
    parser.add_argument(
        "--domain",
        default=os.getenv("USER_EMAIL_DOMAIN", "example.com"),
        help="Email domain for generated users.",
    )
    args = parser.parse_args()

    load_dotenv(override=True)
    api = WebexSimpleApi()
    org_id = resolve_org_id(api, args.org_id)
    calling_license_id = resolve_calling_license(api)

    location_ids = ensure_locations(api, org_id, args.dry_run)
    enable_locations_for_calling(api, location_ids, args.dry_run)

    if prompt_confirm("Use interactive user input instead of defaults?"):
        user_seeds = prompt_user_seeds(args.domain)
        if not user_seeds:
            print("No users provided; exiting.")
            return
    else:
        user_seeds = build_user_seeds(args.domain)

    log_user_counts(api, user_seeds, "Before")
    if not args.dry_run and not prompt_confirm("Proceed with user creation?"):
        print("Aborted by user.")
        return

    ensure_users(api, user_seeds, location_ids, calling_license_id, args.dry_run)
    log_user_counts(api, user_seeds, "After")


if __name__ == "__main__":
    main()

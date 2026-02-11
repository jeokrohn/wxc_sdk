#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "python-dotenv",
#     "wxc-sdk",
# ]
# ///
"""
Promote a small batch of pending lab users to Webex Calling users.

Goal (MVP):
- find users with invite pending and no calling location
- pick N users (default: 2)
- assign a calling license + location (+extension if missing)

Requirements:
- WEBEX_ACCESS_TOKEN (or service app credentials via existing SDK behavior)
- CALLING_LICENSE_ID or CALLING_LICENSE_NAME optional (auto-detect by name if not provided)
- CALLING_LOCATION_ID or CALLING_LOCATION_NAME optional (auto-detect first calling-enabled location)

Usage examples:
- python examples/promote_unverified_to_calling.py --dry-run
- python examples/promote_unverified_to_calling.py --count 2
- python examples/promote_unverified_to_calling.py --location-name "Lab Location A" --license-name "Webex Calling - Professional"
"""

from __future__ import annotations

import argparse
import os
from typing import Iterable

from dotenv import load_dotenv

from wxc_sdk import WebexSimpleApi
from wxc_sdk.people import Person
from wxc_sdk.rest import RestError


def resolve_calling_license_id(api: WebexSimpleApi,
                               *,
                               license_id: str | None,
                               license_name: str | None) -> str:
    if license_id:
        return license_id

    licenses = api.licenses.list()

    if license_name:
        matched = next((lic for lic in licenses if lic.name == license_name), None)
        if matched:
            return matched.license_id
        available = ", ".join(sorted(lic.name for lic in licenses))
        raise RuntimeError(f'License "{license_name}" not found. Available: {available}')

    matched = next((lic for lic in licenses if "calling" in (lic.name or "").lower()), None)
    if matched:
        print(f'Auto-selected calling license: {matched.name}')
        return matched.license_id

    available = ", ".join(sorted(lic.name for lic in licenses))
    raise RuntimeError(
        "No calling license found. Set CALLING_LICENSE_ID or CALLING_LICENSE_NAME. "
        f"Available licenses: {available}"
    )


def resolve_calling_location_id(api: WebexSimpleApi,
                                *,
                                location_id: str | None,
                                location_name: str | None) -> str:
    locations = list(api.locations.list())

    if location_id:
        return location_id

    if location_name:
        loc = next((loc for loc in locations if loc.name == location_name), None)
        if not loc:
            available = ", ".join(sorted(loc.name for loc in locations))
            raise RuntimeError(f'Location "{location_name}" not found. Available: {available}')
        return loc.location_id

    # auto-pick first location already enabled for calling
    for loc in locations:
        try:
            api.telephony.location.details(location_id=loc.location_id)
            print(f'Auto-selected calling-enabled location: {loc.name}')
            return loc.location_id
        except RestError:
            continue

    raise RuntimeError(
        "No calling-enabled location found. Set CALLING_LOCATION_ID or CALLING_LOCATION_NAME, "
        "or enable a location for calling first."
    )


def candidate_users(users: Iterable[Person]) -> list[Person]:
    """Pending invite + no calling location, and not admin roles."""
    result = [u for u in users
              if u.invite_pending
              and not u.location_id
              and not (u.roles or [])]
    result.sort(key=lambda u: (u.emails or [""])[0])
    return result


def next_extension(seed: int) -> str:
    return str(seed)


def main() -> None:
    parser = argparse.ArgumentParser(description="Promote pending users to Webex Calling users.")
    parser.add_argument("--count", type=int, default=2, help="How many users to promote (default: 2).")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without applying changes.")
    parser.add_argument("--license-id", default=os.getenv("CALLING_LICENSE_ID"), help="Calling license ID.")
    parser.add_argument("--license-name", default=os.getenv("CALLING_LICENSE_NAME"), help="Calling license name.")
    parser.add_argument("--location-id", default=os.getenv("CALLING_LOCATION_ID"), help="Calling location ID.")
    parser.add_argument("--location-name", default=os.getenv("CALLING_LOCATION_NAME"), help="Calling location name.")
    parser.add_argument("--extension-base", type=int, default=6100,
                        help="Base extension used when user has no extension (default: 6100).")
    args = parser.parse_args()

    load_dotenv(override=True)

    if args.count < 1:
        raise ValueError("--count must be >= 1")

    with WebexSimpleApi() as api:
        calling_license_id = resolve_calling_license_id(
            api,
            license_id=args.license_id,
            license_name=args.license_name,
        )
        calling_location_id = resolve_calling_location_id(
            api,
            location_id=args.location_id,
            location_name=args.location_name,
        )

        users = list(api.people.list(calling_data=True))
        candidates = candidate_users(users)
        if not candidates:
            print("No pending users without calling location were found.")
            return

        selected = candidates[:args.count]
        print(f"Found {len(candidates)} candidates. Processing {len(selected)} user(s).")

        for index, user in enumerate(selected, start=0):
            email = (user.emails or ["unknown"])[0]
            details = api.people.details(person_id=user.person_id, calling_data=True)

            existing_licenses = list(details.licenses or [])
            if calling_license_id not in existing_licenses:
                existing_licenses.append(calling_license_id)

            details.licenses = existing_licenses
            details.location_id = calling_location_id
            if not details.extension:
                details.extension = next_extension(args.extension_base + index)

            print(f"- {email}")
            print(f"  extension: {details.extension}")
            print(f"  location_id: {details.location_id}")
            print(f"  licenses: {len(details.licenses)} total")

            if args.dry_run:
                print("  [dry-run] skipped update")
                continue

            updated = api.people.update(details, calling_data=True)
            print(f"  updated: {updated.display_name} ({updated.person_id})")


if __name__ == "__main__":
    main()

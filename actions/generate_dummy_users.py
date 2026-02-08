#!/usr/bin/env python3
"""Genera usuarios dummy para pruebas locales de scripts de acciones."""

from __future__ import annotations

import argparse
import csv
import json
import random
import string
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


FIRST_NAMES = [
    "Ana", "Luis", "Marta", "Pablo", "Sofía", "Diego", "Lucía", "Carlos", "Elena", "Javier",
]
LAST_NAMES = [
    "García", "López", "Martín", "Sánchez", "Pérez", "Gómez", "Fernández", "Ruiz", "Díaz", "Torres",
]


@dataclass(frozen=True)
class DummyUser:
    display_name: str
    first_name: str
    last_name: str
    email: str
    extension: str
    primary_number: str


def _slug(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isascii() and ch.isalnum())


def _random_digits(size: int) -> str:
    return "".join(random.choices(string.digits, k=size))


def build_users(count: int, domain: str, ext_start: int, phone_prefix: str) -> list[DummyUser]:
    users: list[DummyUser] = []
    seed = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    for idx in range(count):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        token = _random_digits(4)
        email = f"{_slug(first)}.{_slug(last)}.{seed}.{token}@{domain}"
        extension = str(ext_start + idx)
        primary_number = f"{phone_prefix}{_random_digits(7)}"
        users.append(
            DummyUser(
                display_name=f"{first} {last}",
                first_name=first,
                last_name=last,
                email=email,
                extension=extension,
                primary_number=primary_number,
            )
        )
    return users


def _write_json(path: Path, users: Iterable[DummyUser]) -> None:
    payload = [asdict(user) for user in users]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: Path, users: Iterable[DummyUser]) -> None:
    fields = ["display_name", "first_name", "last_name", "email", "extension", "primary_number"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for user in users:
            writer.writerow(asdict(user))


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera usuarios dummy para pruebas de scripts en laboratorio")
    parser.add_argument("--count", type=int, default=10, help="Cantidad de usuarios a generar")
    parser.add_argument("--domain", default="lab.example.com", help="Dominio de email para los usuarios dummy")
    parser.add_argument("--ext-start", type=int, default=5000, help="Extensión inicial (incremental)")
    parser.add_argument("--phone-prefix", default="+3491", help="Prefijo del número principal")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Formato de salida")
    parser.add_argument("--output", default="actions/dummy_users.json", help="Ruta de salida")
    args = parser.parse_args()

    if args.count <= 0:
        parser.error("--count debe ser > 0")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    users = build_users(
        count=args.count,
        domain=args.domain,
        ext_start=args.ext_start,
        phone_prefix=args.phone_prefix,
    )

    if args.format == "json":
        _write_json(output_path, users)
    else:
        _write_csv(output_path, users)

    print(f"Generados {len(users)} usuarios dummy en: {output_path}")
    if users:
        sample = users[0]
        print(
            "Ejemplo --vars para scripts de usuario:",
            json.dumps(
                {
                    "email": sample.email,
                    "person_id": "<person_id_real_del_tenant>",
                    "extension": sample.extension,
                    "primary_number": sample.primary_number,
                },
                ensure_ascii=False,
            ),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

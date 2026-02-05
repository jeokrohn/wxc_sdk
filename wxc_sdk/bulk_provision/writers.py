import csv
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _append_row(path: Path, header: list[str], row: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists()
    with path.open("a", newline="") as handle:
        writer = csv.writer(handle)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(list(row))
        handle.flush()
        os.fsync(handle.fileno())


@dataclass(frozen=True)
class Writers:
    results_path: Path
    pending_path: Path
    rejected_path: Path

    def write_result(
        self,
        *,
        batch_id: int,
        row_id: int,
        entity_type: str,
        entity_key: str,
        step: str,
        status: str,
        http_status: Optional[int],
        message: str,
        remote_id: Optional[str],
    ) -> None:
        _append_row(
            self.results_path,
            [
                "timestamp",
                "batch_id",
                "row_id",
                "entity_type",
                "entity_key",
                "step",
                "status",
                "http_status",
                "message",
                "remote_id",
            ],
            [
                utc_timestamp(),
                batch_id,
                row_id,
                entity_type,
                entity_key,
                step,
                status,
                "" if http_status is None else http_status,
                message,
                "" if remote_id is None else remote_id,
            ],
        )

    def write_pending(
        self,
        *,
        batch_id: int,
        row_id: int,
        entity_type: str,
        entity_key: str,
        step: str,
        reason_code: str,
        reason_message: str,
        http_status: Optional[int],
        raw_row_minified: str,
    ) -> None:
        _append_row(
            self.pending_path,
            [
                "timestamp",
                "batch_id",
                "row_id",
                "entity_type",
                "entity_key",
                "step",
                "reason_code",
                "reason_message",
                "http_status",
                "raw_row_minified",
            ],
            [
                utc_timestamp(),
                batch_id,
                row_id,
                entity_type,
                entity_key,
                step,
                reason_code,
                reason_message,
                "" if http_status is None else http_status,
                raw_row_minified,
            ],
        )

    def write_rejected(
        self,
        *,
        row_id: int,
        reason_code: str,
        reason_message: str,
        raw_row_minified: str,
    ) -> None:
        _append_row(
            self.rejected_path,
            ["timestamp", "row_id", "reason_code", "reason_message", "raw_row_minified"],
            [
                utc_timestamp(),
                row_id,
                reason_code,
                reason_message,
                raw_row_minified,
            ],
        )

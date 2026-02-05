import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass
class CheckpointStore:
    path: Path

    def load(self) -> Optional[dict[str, Any]]:
        if not self.path.exists():
            return None
        with self.path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def write(self, payload: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.path.with_suffix(".tmp")
        with tmp_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.flush()
        tmp_path.replace(self.path)

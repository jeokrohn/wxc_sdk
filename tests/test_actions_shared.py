import importlib.util
import logging
from pathlib import Path
import sys


MODULE_PATH = Path(__file__).resolve().parents[1] / "actions" / "_shared.py"
SPEC = importlib.util.spec_from_file_location("actions_shared", MODULE_PATH)
assert SPEC and SPEC.loader
_shared = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = _shared
SPEC.loader.exec_module(_shared)


def test_snapshot_meta_creates_expected_names(tmp_path: Path):
    meta = _shared._snapshot_meta("action_call_queue", str(tmp_path))

    assert meta.latest_path.name == "lastdatetime_snapshot_action_action_call_queue.json"
    assert meta.timestamped_path.name.endswith(meta.latest_path.name)
    assert meta.latest_path.parent == tmp_path


def test_save_and_load_snapshot_roundtrip(tmp_path: Path):
    meta = _shared._snapshot_meta("action_call_queue", str(tmp_path))
    payload = {"entries": [{"name": "probe", "path": "x", "body": {"a": 1}}]}

    _shared._save_snapshot(meta, payload)
    loaded = _shared._load_snapshot(meta.latest_path)

    assert meta.timestamped_path.exists()
    assert meta.latest_path.exists()
    assert loaded == payload


def test_calls_from_snapshot_uses_json_objects_only():
    logger = logging.getLogger("test_actions_shared")
    snapshot = {
        "entries": [
            {"name": "ok", "path": "telephony/config/test", "body": {"enabled": True}},
            {"name": "skip_list", "path": "telephony/config/list", "body": [1, 2, 3]},
            {"name": "skip_no_path", "body": {"a": 1}},
        ]
    }

    calls = _shared._calls_from_snapshot(snapshot, logger)

    assert len(calls) == 1
    assert calls[0].method == "PUT"
    assert calls[0].path == "telephony/config/test"
    assert calls[0].payload == {"enabled": True}

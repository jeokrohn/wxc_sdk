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


def test_format_value_raises_missing_variables_error():
    try:
        _shared._format_value("devices/{serial}", {"workspace_id": "x"})
    except _shared.MissingVariablesError as err:
        assert err.missing_keys == ["serial"]
    else:
        raise AssertionError("Expected MissingVariablesError")


def test_preflight_snapshot_skips_calls_with_missing_variables():
    class DummyClient:
        def request(self, *args, **kwargs):  # pragma: no cover - should not be reached
            raise AssertionError("request() should not be called")

    spec = _shared.ActionSpec(
        key="action_devices",
        title="Devices",
        objective="Test",
        pre_post_notes=[],
        probe_calls=[
            _shared.ApiCall(
                name="probe_devices",
                method="GET",
                path="devices",
                params={"serial": "{serial}"},
            )
        ],
        apply_calls=[],
    )
    logger = logging.getLogger("test_actions_shared")

    snapshot = _shared._preflight_snapshot(DummyClient(), spec, {"workspace_id": "ws"}, logger)

    assert snapshot["entries"][0]["skipped"] is True
    assert snapshot["entries"][0]["missing_vars"] == ["serial"]


def test_run_calls_logs_full_response_body_and_headers(caplog):
    class DummyResponse:
        status_code = 200
        text = "x" * 1200
        headers = {"X-Test": "header-value"}

    class DummyClient:
        def request(self, *args, **kwargs):
            return DummyResponse()

    logger = logging.getLogger("test_actions_shared")
    call = _shared.ApiCall(name="probe", method="GET", path="devices")

    with caplog.at_level(logging.INFO, logger="test_actions_shared"):
        failures = _shared._run_calls(DummyClient(), [call], {}, logger)

    assert failures == 0
    done_records = [r for r in caplog.records if r.message.startswith("API call done | step=")]
    assert len(done_records) == 1
    assert "response_headers={'X-Test': 'header-value'}" in done_records[0].message
    assert f"response_body={'x' * 1200}" in done_records[0].message

import json
from pathlib import Path

from wxc_sdk.bulk_provision.batch_iterator import iter_batches
from wxc_sdk.bulk_provision.state_store import CheckpointStore
from wxc_sdk.bulk_provision.writers import Writers


def test_iter_batches_limits() -> None:
    items = list(range(10))
    batches = list(iter_batches(items, batch_size=4, max_rows=9, max_batches=3))
    assert len(batches) == 3
    assert sum(len(batch.items) for batch in batches) == 9


def test_checkpoint_store(tmp_path: Path) -> None:
    store = CheckpointStore(tmp_path / "checkpoint.json")
    payload = {"phase": "user", "last_item_id": 10}
    store.write(payload)
    assert store.load() == payload


def test_writers_append(tmp_path: Path) -> None:
    writers = Writers(
        results_path=tmp_path / "results.csv",
        pending_path=tmp_path / "pending.csv",
        rejected_path=tmp_path / "rejected.csv",
    )
    writers.write_result(
        batch_id=1,
        row_id=1,
        entity_type="user",
        entity_key="ana@example.com",
        step="create",
        status="success",
        http_status=200,
        message="ok",
        remote_id="id1",
    )
    writers.write_pending(
        batch_id=1,
        row_id=2,
        entity_type="user",
        entity_key="bob@example.com",
        step="create",
        reason_code="retry_exhausted",
        reason_message="timeout",
        http_status=504,
        raw_row_minified=json.dumps({"email": "bob@example.com"}),
    )
    writers.write_rejected(
        row_id=3,
        reason_code="invalid_input_schema",
        reason_message="missing",
        raw_row_minified=json.dumps({"email": ""}),
    )
    assert (tmp_path / "results.csv").read_text().count("\n") == 2
    assert (tmp_path / "pending.csv").read_text().count("\n") == 2
    assert (tmp_path / "rejected.csv").read_text().count("\n") == 2

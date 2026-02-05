from collections.abc import Generator, Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Batch:
    batch_id: int
    items: list


def iter_batches(
    items: Iterable,
    *,
    batch_size: int,
    max_rows: int,
    max_batches: int,
) -> Generator[Batch, None, None]:
    batch_id = 1
    current: list = []
    total_rows = 0
    for item in items:
        if total_rows >= max_rows:
            break
        current.append(item)
        total_rows += 1
        if len(current) >= batch_size:
            yield Batch(batch_id=batch_id, items=current)
            batch_id += 1
            if batch_id > max_batches:
                return
            current = []
    if current:
        yield Batch(batch_id=batch_id, items=current)

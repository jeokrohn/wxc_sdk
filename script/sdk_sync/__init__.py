"""
Stub → SDK drift synchronizer.

Reads OpenAPI-derived stubs under ``open_api/generated/`` against the
hand-maintained SDK in ``wxc_sdk/`` and applies the equivalent edits.

Pipeline (one direction per change record):

1. :mod:`~script.sdk_sync.ir` — extract a normalized intermediate
   representation from each Python file (stub or SDK side).
2. :mod:`~script.sdk_sync.differ` — compare the IR of a stub at ``HEAD``
   with its IR in the working tree, producing typed change records.
3. :mod:`~script.sdk_sync.matcher` — resolve each record to its SDK
   counterpart via the alias cache, exact endpoint matching, or a
   URL+docstring heuristic.
4. :mod:`~script.sdk_sync.dispatcher` — route the record to either the
   deterministic :mod:`~script.sdk_sync.patcher` or to the
   :mod:`~script.sdk_sync.llm` step (a ``claude`` CLI subprocess), with
   ``git apply --check`` gating any LLM-produced diff.
5. :mod:`~script.sdk_sync.driver` — orchestrate the run end-to-end,
   persist :mod:`~script.sdk_sync.aliases`, and render ``sync_report.md``.

Invoke via ``python -m script.sdk_sync`` or the ``make sync-stubs`` /
``make sync-stubs-dry`` / ``make sync-stubs-no-llm`` targets.
"""

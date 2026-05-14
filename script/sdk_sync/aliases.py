"""
Persistent stub↔SDK alias cache.

``aliases.json`` is checked into the repo. It records manual or auto-confirmed
mappings from stub entities to their SDK counterparts so future runs don't
re-derive the same match from scratch (or, worse, re-ask a human about the
same ambiguity).

Two kinds of mapping are persisted:

- **Method aliases** key on ``"<stub_path>::<StubClass>::<stub_method>"`` and
  point at a specific SDK class/method. They're recorded automatically by
  the matcher whenever an exact or heuristic match succeeds and consulted
  on the next run before any new matching work is done.
- **Model aliases** are simpler ``StubClassName → SDKClassName`` mappings,
  used when stub and SDK disagree on the class name (e.g. the stub's
  ``DeviceConnectionStatus`` is the SDK's ``ConnectionStatus``). These are
  typically seeded by hand because the matcher cannot infer them from
  endpoint URLs alone.

In addition we persist an ``unmatched`` list of records the matcher gave up
on, with their top heuristic candidates. This lets a reviewer see what
``aliases.json`` would need to be amended with to cover the gaps.

JSON schema (version 1):

.. code-block:: json

    {
      "version": 1,
      "method_aliases": {
        "<stub_path>::<StubClass>::<stub_method>": {
          "sdk_path": "<wxc_sdk/...>",
          "sdk_class": "<ClassName>",
          "sdk_method": "<method>",
          "confidence": 0.91,
          "matched_by": "exact|url+docstring|manual",
          "confirmed_by": "auto|user",
          "confirmed_at": "YYYY-MM-DD"
        }
      },
      "model_aliases": {
        "<StubClassName>": {"sdk_path": "...", "sdk_class": "..."}
      },
      "unmatched": [
        {"stub_key": "...", "best_score": 0.62, "candidates": [...]}
      ]
    }
"""

from __future__ import annotations

import datetime as _dt
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Path to the on-disk cache file. Resolved at import time so tests can
# override it via the `path` parameter to :func:`load` / :func:`save`.
_ALIASES_PATH = Path(__file__).with_name('aliases.json')


@dataclass
class MethodAlias:
    """A persisted stub-method → SDK-method mapping.

    :param sdk_path: SDK file path, repo-relative
        (``"wxc_sdk/devices/__init__.py"``).
    :param sdk_class: Name of the SDK class containing the method.
    :param sdk_method: Name of the SDK method.
    :param confidence: Score from the matcher; ``1.0`` for exact matches,
        the combined URL+docstring score for heuristic matches, may be
        anything for ``matched_by='manual'``.
    :param matched_by: ``'exact'`` for endpoint-key matches, ``'url+docstring'``
        for heuristic ones, ``'manual'`` for human-curated entries.
    :param confirmed_by: ``'auto'`` for entries the matcher created on its
        own, ``'user'`` for hand-edited entries.
    :param confirmed_at: ISO date of when the alias was recorded; useful
        for staleness audits.
    """

    sdk_path: str
    sdk_class: str
    sdk_method: str
    confidence: float
    matched_by: str
    confirmed_by: str = 'auto'
    confirmed_at: str = field(default_factory=lambda: _dt.date.today().isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict form.

        :return: Dict with the same keys as the dataclass fields; the
            confidence is rounded for diff-friendliness.
        """
        return {
            'sdk_path': self.sdk_path,
            'sdk_class': self.sdk_class,
            'sdk_method': self.sdk_method,
            'confidence': round(self.confidence, 4),
            'matched_by': self.matched_by,
            'confirmed_by': self.confirmed_by,
            'confirmed_at': self.confirmed_at,
        }


@dataclass
class ModelAlias:
    """A persisted stub-class → SDK-class mapping for models or enums.

    :param sdk_path: SDK file path, repo-relative.
    :param sdk_class: Name of the SDK class to use when the stub class name
        doesn't exist in the SDK.
    """

    sdk_path: str
    sdk_class: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict form.

        :return: Dict with ``sdk_path`` and ``sdk_class``.
        """
        return {'sdk_path': self.sdk_path, 'sdk_class': self.sdk_class}


@dataclass
class UnmatchedEntry:
    """One record the matcher could not resolve.

    :param stub_key: Human-readable identifier in the form
        ``"<kind>::<qualname>"``.
    :param best_score: Top heuristic score below :data:`THRESHOLD`. ``0.0``
        if no candidates were even scored.
    :param candidates: Up to five top-scoring SDK candidates as plain dicts
        with ``sdk_path``, ``sdk_class``, ``sdk_method`` and ``score``;
        empty list when no candidates survived.
    """

    stub_key: str
    best_score: float
    candidates: list[dict[str, Any]]


@dataclass
class AliasStore:
    """In-memory representation of ``aliases.json``.

    :param method_aliases: Map of stub-method-key to :class:`MethodAlias`.
    :param model_aliases: Map of stub-class-name to :class:`ModelAlias`.
    :param unmatched: List of :class:`UnmatchedEntry`; cleared at the start
        of each run and repopulated by the matcher as it punts.
    """

    method_aliases: dict[str, MethodAlias] = field(default_factory=dict)
    model_aliases: dict[str, ModelAlias] = field(default_factory=dict)
    unmatched: list[UnmatchedEntry] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the store to a plain dict matching the JSON schema.

        Method and model aliases are sorted by key so the on-disk file
        produces stable git diffs.

        :return: Dict ready to feed to :func:`json.dumps`.
        """
        return {
            'version': 1,
            'method_aliases': {k: v.to_dict() for k, v in sorted(self.method_aliases.items())},
            'model_aliases': {k: v.to_dict() for k, v in sorted(self.model_aliases.items())},
            'unmatched': [
                {'stub_key': u.stub_key, 'best_score': round(u.best_score, 4), 'candidates': u.candidates}
                for u in self.unmatched
            ],
        }


def load(path: Path = _ALIASES_PATH) -> AliasStore:
    """Read ``aliases.json`` from disk and return its in-memory form.

    :param path: Override the default cache path (used by tests).
    :return: A populated :class:`AliasStore`, or an empty one if the file
        does not exist.
    """
    if not path.exists():
        return AliasStore()
    data = json.loads(path.read_text())
    return AliasStore(
        method_aliases={k: MethodAlias(**v) for k, v in data.get('method_aliases', {}).items()},
        model_aliases={k: ModelAlias(**v) for k, v in data.get('model_aliases', {}).items()},
        unmatched=[UnmatchedEntry(**u) for u in data.get('unmatched', [])],
    )


def save(store: AliasStore, path: Path = _ALIASES_PATH) -> None:
    """Write ``store`` back to ``aliases.json`` (pretty-printed, with trailing newline).

    :param store: The store to persist.
    :param path: Override the default cache path (used by tests).
    :return: Nothing.
    """
    path.write_text(json.dumps(store.to_dict(), indent=2) + '\n')


def method_key(stub_path: str, stub_class: str, stub_method: str) -> str:
    """Build the canonical key used for method aliases.

    The key composition (``::`` separators) is human-readable and survives
    transit through JSON without escaping.

    :param stub_path: Repo-relative path of the stub file.
    :param stub_class: Name of the stub's API class.
    :param stub_method: Name of the stub's method.
    :return: A string in the form
        ``"<stub_path>::<StubClass>::<stub_method>"``.
    """
    return f'{stub_path}::{stub_class}::{stub_method}'

"""
Stub → SDK location resolver.

Given a :class:`~script.sdk_sync.differ.ChangeRecord` produced from a stub
diff, and the :class:`~script.sdk_sync.ir.ModuleIR` of the stub it came from,
the matcher returns a :class:`Match` pointing at the SDK file/class/member
that should receive the equivalent edit. Resolution order:

1. **Alias cache hit.** If the stub key is already in
   :class:`~script.sdk_sync.aliases.AliasStore.method_aliases` or
   ``.model_aliases``, return the recorded mapping. This is how the matcher
   stays cheap across runs.
2. **Exact match.** For methods, look up ``(verb, ep_template)`` against the
   SDK index — the join key is stable across stub and SDK because both
   compose URLs the same way. For models/enums/fields/enum-values, look up
   by class name (after applying any aliases).
3. **Heuristic match (methods only).** Score every plausible SDK method by
   ``0.6 * URL-token-Jaccard + 0.4 * docstring-similarity`` and accept the
   top candidate when its score clears :data:`THRESHOLD`.
4. **Punt.** Append an ``UnmatchedEntry`` to ``store.unmatched`` so the human
   reviewer can see what wasn't auto-resolved, and return ``None``.

The SDK index is built lazily on first access and cached for the process
lifetime — walking ~30 SDK modules with :mod:`ast` is ~100 ms once.
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import aliases as _aliases
from .differ import ChangeRecord
from .ir import ApiClassIR, EnumIR, MethodIR, ModelIR, ModuleIR, extract

#: Minimum combined score for the heuristic matcher to accept a match.
#: Below this we punt to the unmatched list and let a human (or the LLM with
#: a tightly scoped prompt) decide.
THRESHOLD = 0.75

# Resolve `wxc_sdk/` once at import time. Walking from
# `script/sdk_sync/matcher.py` up three levels lands at the repo root, then
# we descend into the SDK package.
_SDK_ROOT = Path(__file__).resolve().parent.parent.parent / 'wxc_sdk'

# Auto-generated files we should never propose changes to (the user
# regenerates them via `make types`/`make async`).
_SDK_SKIP_FILES = {'all_types.py', 'as_api.py', 'as_mpe.py', 'as_rest.py'}


@dataclass
class Match:
    """A resolved SDK target for one stub change.

    :param sdk_path: Absolute path to the SDK file the change applies to.
    :param kind: ``'method'``, ``'model'``, ``'enum'``, ``'enum_value'`` or
        ``'model_field'``. Selects the branch the patcher dispatches to.
    :param sdk_class: Class name on the SDK side. For aliased models/enums
        this is the *SDK* name, which may differ from the stub class name.
    :param sdk_member: Method, field or enum-value name on the SDK side.
        ``None`` for class-level matches (``model``, ``enum``).
    :param sdk_module_ir: IR of the SDK module containing the target. Carried
        on the match so the patcher and dispatcher don't re-parse it.
    :param confidence: Score in ``[0, 1]``. ``1.0`` for exact and alias hits,
        the heuristic combined score otherwise.
    :param matched_by: ``'alias'``, ``'exact'`` or ``'heuristic'`` —
        recorded in the report and in the alias cache.
    """

    sdk_path: Path
    kind: str
    sdk_class: str
    sdk_member: str | None
    sdk_module_ir: ModuleIR
    confidence: float
    matched_by: str


class _SDKIndex:
    """Lazily-built read-through index of all SDK feature modules.

    The index walks every Python file under :data:`_SDK_ROOT`, parses it with
    :func:`~script.sdk_sync.ir.extract`, and keeps the resulting IRs in
    memory. Lookups are linear in the number of modules (~30), which is fast
    enough that we don't need secondary indexes.
    """

    def __init__(self) -> None:
        self._irs: list[ModuleIR] = []
        self._loaded = False

    def _load(self) -> None:
        """Populate :attr:`_irs` if not already done.

        :return: Nothing. Subsequent calls are no-ops.
        """
        if self._loaded:
            return
        for path in sorted(_SDK_ROOT.rglob('*.py')):
            # Skip auto-generated, async wrappers, caches, and tests.
            if path.name.startswith('as_') or path.name in _SDK_SKIP_FILES:
                continue
            if '__pycache__' in path.parts:
                continue
            if path.name.startswith('test_'):
                continue
            try:
                self._irs.append(extract(path))
            except SyntaxError:
                # Skip anything that fails to parse so one broken file
                # doesn't take the whole sync run down.
                continue
        self._loaded = True

    def all(self) -> list[ModuleIR]:
        """Return every SDK module IR.

        :return: List of :class:`ModuleIR`, in path-sorted order.
        """
        self._load()
        return self._irs

    def find_model(self, name: str) -> tuple[Path, ModuleIR, ModelIR] | None:
        """Locate the SDK Pydantic model with the given class name.

        :param name: Class name to find.
        :return: ``(path, module_ir, model_ir)`` for the first match, or
            ``None`` if no module declares such a class.
        """
        for ir in self.all():
            for m in ir.models:
                if m.name == name:
                    return Path(ir.path), ir, m
        return None

    def find_enum(self, name: str) -> tuple[Path, ModuleIR, EnumIR] | None:
        """Locate the SDK enum with the given class name.

        :param name: Enum class name.
        :return: ``(path, module_ir, enum_ir)`` or ``None``.
        """
        for ir in self.all():
            for e in ir.enums:
                if e.name == name:
                    return Path(ir.path), ir, e
        return None

    def find_api_by_base(self, base: str) -> list[tuple[Path, ModuleIR, ApiClassIR]]:
        """Return every SDK module whose API class declares the given ``base=``.

        :param base: Value of the ``base=`` keyword on the stub's API class.
        :return: List of ``(path, module_ir, api_class_ir)`` triples; the list
            is usually short (0–3 entries).
        """
        out: list[tuple[Path, ModuleIR, ApiClassIR]] = []
        for ir in self.all():
            if ir.api_class is not None and ir.api_class.base == base:
                out.append((Path(ir.path), ir, ir.api_class))
        return out

    def find_api_with_endpoint(self, verb: str, ep_template: str) -> list[tuple[Path, ModuleIR, ApiClassIR, MethodIR]]:
        """Return every SDK method that exactly matches a ``(verb, ep_template)`` key.

        :param verb: HTTP verb in lowercase.
        :param ep_template: Canonical endpoint template (as produced by
            :func:`~script.sdk_sync.ir._canonical_ep_template`).
        :return: List of ``(path, module_ir, api_class_ir, method_ir)``
            quadruples; usually 0 or 1 entry.
        """
        out: list[tuple[Path, ModuleIR, ApiClassIR, MethodIR]] = []
        for ir in self.all():
            if ir.api_class is None:
                continue
            for m in ir.api_class.methods:
                if m.verb == verb and m.ep_template == ep_template:
                    out.append((Path(ir.path), ir, ir.api_class, m))
        return out


# Module-level singleton. Reset between unit tests is rarely needed; the
# index reflects on-disk SDK state, so it does not invalidate as the
# pipeline rewrites files (the dispatcher refreshes individual matches
# via `_refresh_match` instead).
_index = _SDKIndex()


def match(record: ChangeRecord, stub_ir: ModuleIR, store: _aliases.AliasStore) -> Match | None:
    """Resolve a :class:`ChangeRecord` to its SDK location.

    Dispatches to the right ``_match_*`` helper based on ``record.kind``.
    On a miss the function appends an :class:`UnmatchedEntry` to
    ``store.unmatched`` (so the report can show what wasn't resolved) and
    returns ``None``.

    :param record: The change to resolve.
    :param stub_ir: IR of the stub the change came from. Some change kinds
        (notably method-related ones) need to look up the stub method to
        retrieve its ``(verb, ep_template)``.
    :param store: Alias store; consulted for cached mappings and mutated to
        record new ones plus any unmatched cases.
    :return: A :class:`Match` if resolution succeeds, otherwise ``None``.
    """
    if record.kind in {'enum_value_added', 'enum_value_removed'}:
        return _match_enum_value(record, store)
    if record.kind in {'model_field_added', 'model_field_removed'}:
        return _match_model_field(record, store)
    if record.kind == 'model_added' or record.kind == 'model_removed':
        return _match_model_or_enum(record, store)
    if record.kind == 'docstring_changed':
        return _match_docstring(record, stub_ir, store)
    if record.kind == 'type_changed':
        return _match_type_changed(record, stub_ir, store)
    if record.kind in {
        'method_added',
        'method_removed',
        'method_param_added',
        'method_param_removed',
        'method_return_changed',
    }:
        return _match_method(record, stub_ir, store)
    return None


# ---------------------------------------------------------------------------
# Class-level / member helpers
# ---------------------------------------------------------------------------


def _split_qualname(qn: str) -> tuple[str, str | None]:
    """Split a ``ChangeRecord.qualname`` into ``(head, tail)``.

    :param qn: The qualname produced by the differ
        (``"Class"``, ``"Class.member"``, or
        ``"Class.method(param)"``).
    :return: ``(head, tail)`` — ``tail`` is ``None`` when the qualname is a
        bare class name with no dotted member.
    """
    if '.' in qn:
        cls, member = qn.split('.', 1)
        return cls, member
    return qn, None


def _resolve_class_name(stub_name: str, store: _aliases.AliasStore) -> str:
    """Apply a model alias if one is recorded for ``stub_name``.

    :param stub_name: Class name as it appears in the stub.
    :param store: Alias store consulted for renames.
    :return: The SDK class name to look up. Identical to ``stub_name`` if
        no alias exists.
    """
    a = store.model_aliases.get(stub_name)
    return a.sdk_class if a is not None else stub_name


def _match_model_or_enum(record: ChangeRecord, store: _aliases.AliasStore) -> Match | None:
    """Resolve a ``model_added`` or ``model_removed`` record.

    Looks up the SDK class first as a Pydantic model, then as an enum
    (the differ emits whole-enum changes under the ``model_*`` kinds).

    :param record: A model-or-enum-level change record.
    :param store: Alias store consulted for renames; mutated on a punt.
    :return: A :class:`Match`, or ``None`` if neither a model nor an enum
        with the (possibly aliased) name exists in the SDK index.
    """
    stub_name, _ = _split_qualname(record.qualname)
    name = _resolve_class_name(stub_name, store)
    found = _index.find_model(name)
    if found is not None:
        path, ir, _ = found
        return Match(path, 'model', name, None, ir, 1.0, 'alias' if name != stub_name else 'exact')
    found_e = _index.find_enum(name)
    if found_e is not None:
        path, ir, _ = found_e
        return Match(path, 'enum', name, None, ir, 1.0, 'alias' if name != stub_name else 'exact')
    _record_unmatched(record, store)
    return None


def _match_enum_value(record: ChangeRecord, store: _aliases.AliasStore) -> Match | None:
    """Resolve an ``enum_value_added`` / ``enum_value_removed`` record.

    :param record: A value-level enum change record. ``qualname`` is expected
        to be ``"EnumName.value_name"``.
    :param store: Alias store consulted for enum renames; mutated on a punt.
    :return: A :class:`Match` pointing at the SDK enum and its member name,
        or ``None`` if the enum class is absent from the SDK.
    """
    stub_enum, value_name = _split_qualname(record.qualname)
    if value_name is None:
        return None
    enum_name = _resolve_class_name(stub_enum, store)
    found = _index.find_enum(enum_name)
    if found is None:
        _record_unmatched(record, store)
        return None
    path, ir, _ = found
    return Match(
        path,
        'enum_value',
        enum_name,
        value_name,
        ir,
        1.0,
        'alias' if enum_name != stub_enum else 'exact',
    )


def _match_model_field(record: ChangeRecord, store: _aliases.AliasStore) -> Match | None:
    """Resolve a ``model_field_added`` / ``model_field_removed`` record.

    :param record: A field-level model change record. ``qualname`` is
        expected to be ``"ModelName.field_name"``.
    :param store: Alias store consulted for model renames; mutated on a punt.
    :return: A :class:`Match` pointing at the SDK model and its field name,
        or ``None`` if the model is absent.
    """
    stub_model, field_name = _split_qualname(record.qualname)
    if field_name is None:
        return None
    model_name = _resolve_class_name(stub_model, store)
    found = _index.find_model(model_name)
    if found is None:
        _record_unmatched(record, store)
        return None
    path, ir, _ = found
    return Match(
        path,
        'model_field',
        model_name,
        field_name,
        ir,
        1.0,
        'alias' if model_name != stub_model else 'exact',
    )


# ---------------------------------------------------------------------------
# Method-level helpers
# ---------------------------------------------------------------------------


def _stub_method_from_record(record: ChangeRecord, stub_ir: ModuleIR) -> MethodIR | None:
    """Recover the stub-side :class:`MethodIR` referenced by a change record.

    Method change records carry the qualname ``"<Class>.<method>"`` or
    ``"<Class>.<method>(param)"``. For most records the method is still in
    the *new* stub IR. For ``method_removed`` the method only exists in the
    old IR, but the record's payload preserves ``verb`` and ``ep_template``,
    so we synthesize a minimal :class:`MethodIR` for the matcher.

    :param record: The change record.
    :param stub_ir: IR of the new stub. ``api_class`` may be ``None`` for
        synthesized records.
    :return: A :class:`MethodIR` if the method or enough of its payload was
        recovered; ``None`` otherwise.
    """
    cls, method = _split_qualname(record.qualname)
    if method is None:
        return None
    method = method.split('(')[0]  # strip "(param)" suffix from type_changed records
    if stub_ir.api_class is not None:
        for m in stub_ir.api_class.methods:
            if m.name == method:
                return m
    payload = record.old or record.new or {}
    if payload.get('verb') and payload.get('ep_template'):
        return MethodIR(
            name=method,
            params=(),
            returns=payload.get('returns'),
            docstring=payload.get('docstring'),
            verb=payload.get('verb'),
            ep_template=payload.get('ep_template'),
            raw_ep_arg=None,
            lineno=0,
            end_lineno=0,
        )
    return None


def _match_method(record: ChangeRecord, stub_ir: ModuleIR, store: _aliases.AliasStore) -> Match | None:
    """Resolve a method-level change record to its SDK counterpart.

    Resolution sequence:

    1. **Alias cache** — if this exact ``(stub_path, stub_class, stub_method)``
       has been recorded, return the cached mapping immediately.
    2. **Exact endpoint match** — if exactly one SDK method has the same
       ``(verb, ep_template)``, accept it and persist the alias.
    3. **Heuristic match** — score the surviving candidates (those sharing
       the stub's ``base=``, or all same-verb methods if no class shares
       the base) by :func:`_score_method_pair` and accept the top score if
       it clears :data:`THRESHOLD`.
    4. **Punt** — record an :class:`UnmatchedEntry` with the top-scoring
       candidates for human review.

    :param record: The change record.
    :param stub_ir: IR of the stub the record came from.
    :param store: Alias store; consulted and mutated.
    :return: A :class:`Match`, or ``None`` on a punt.
    """
    if stub_ir.api_class is None:
        _record_unmatched(record, store)
        return None
    stub_cls = stub_ir.api_class.name
    cls, method_qn = _split_qualname(record.qualname)
    stub_method_name = (method_qn or '').split('(')[0]

    key = _aliases.method_key(stub_ir.path, stub_cls, stub_method_name)
    if key in store.method_aliases:
        a = store.method_aliases[key]
        sdk_path = Path(a.sdk_path)
        if not sdk_path.is_absolute():
            sdk_path = (_SDK_ROOT.parent / sdk_path).resolve()
        # Reuse the cached IR if the file is already in the index;
        # otherwise extract on demand (rare).
        try:
            sdk_ir = next(ir for ir in _index.all() if Path(ir.path) == sdk_path)
        except StopIteration:
            sdk_ir = extract(sdk_path)
        return Match(sdk_path, 'method', a.sdk_class, a.sdk_method, sdk_ir, a.confidence, 'alias')

    stub_method = _stub_method_from_record(record, stub_ir)
    if stub_method is None or stub_method.verb is None or stub_method.ep_template is None:
        _record_unmatched(record, store)
        return None

    exact = _index.find_api_with_endpoint(stub_method.verb, stub_method.ep_template)
    if len(exact) == 1:
        sdk_path, sdk_ir, sdk_cls, sdk_m = exact[0]
        store.method_aliases[key] = _aliases.MethodAlias(
            sdk_path=str(sdk_path.relative_to(_SDK_ROOT.parent)),
            sdk_class=sdk_cls.name,
            sdk_method=sdk_m.name,
            confidence=1.0,
            matched_by='exact',
            confirmed_by='auto',
        )
        return Match(sdk_path, 'method', sdk_cls.name, sdk_m.name, sdk_ir, 1.0, 'exact')

    # Heuristic: score candidates by URL-token Jaccard + docstring similarity.
    # If exact had multiple hits we score those; otherwise broaden by base= or verb.
    candidates = exact if exact else _gather_heuristic_candidates(stub_method, stub_ir.api_class.base)
    scored: list[tuple[float, Path, ModuleIR, ApiClassIR, MethodIR]] = []
    for sdk_path, sdk_ir, sdk_cls, sdk_m in candidates:
        score = _score_method_pair(stub_method, sdk_m)
        scored.append((score, sdk_path, sdk_ir, sdk_cls, sdk_m))
    scored.sort(key=lambda x: x[0], reverse=True)
    if scored and scored[0][0] >= THRESHOLD:
        score, sdk_path, sdk_ir, sdk_cls, sdk_m = scored[0]
        store.method_aliases[key] = _aliases.MethodAlias(
            sdk_path=str(sdk_path.relative_to(_SDK_ROOT.parent)),
            sdk_class=sdk_cls.name,
            sdk_method=sdk_m.name,
            confidence=score,
            matched_by='url+docstring',
            confirmed_by='auto',
        )
        return Match(sdk_path, 'method', sdk_cls.name, sdk_m.name, sdk_ir, score, 'heuristic')

    _record_unmatched(
        record,
        store,
        candidates=[
            {
                'sdk_path': str(p.relative_to(_SDK_ROOT.parent)),
                'sdk_class': c.name,
                'sdk_method': m.name,
                'score': round(s, 4),
            }
            for s, p, _ir, c, m in scored[:5]
        ],
        best_score=scored[0][0] if scored else 0.0,
    )
    return None


def _match_docstring(record: ChangeRecord, stub_ir: ModuleIR, store: _aliases.AliasStore) -> Match | None:
    """Resolve a ``docstring_changed`` record.

    Docstring changes can apply at three levels: model fields, enum values
    or methods. We disambiguate by looking at the head of the qualname:

    - ``EnumName.value`` — route to :func:`_match_enum_value`.
    - ``ModelName.field`` — route to :func:`_match_model_field`.
    - ``ClassName.method`` — route to :func:`_match_method`.

    :param record: The change record.
    :param stub_ir: IR of the stub the record came from.
    :param store: Alias store.
    :return: A :class:`Match` from the delegated resolver, or ``None``.
    """
    head, tail = _split_qualname(record.qualname)
    if tail is None:
        return None
    if _index.find_enum(head) is not None:
        return _match_enum_value(record, store)
    if _index.find_model(head) is not None:
        return _match_model_field(record, store)
    return _match_method(record, stub_ir, store)


def _match_type_changed(record: ChangeRecord, stub_ir: ModuleIR, store: _aliases.AliasStore) -> Match | None:
    """Resolve a ``type_changed`` record.

    The differ emits ``type_changed`` for both field annotation changes
    (``qualname = "Model.field"``) and method parameter retypes
    (``qualname = "Class.method(param)"``). The presence of ``(`` in the
    member portion is the disambiguator.

    :param record: The change record.
    :param stub_ir: IR of the stub the record came from.
    :param store: Alias store.
    :return: A :class:`Match`, or ``None`` on a punt.
    """
    head, tail = _split_qualname(record.qualname)
    if tail is None:
        return None
    if '(' in tail:
        return _match_method(record, stub_ir, store)
    if _index.find_enum(head) is not None:
        return _match_enum_value(record, store)
    if _index.find_model(head) is not None:
        return _match_model_field(record, store)
    _record_unmatched(record, store)
    return None


# ---------------------------------------------------------------------------
# Heuristic scoring
#
# Used only when exact `(verb, ep_template)` matching fails. The combined
# score is `0.6 * url_jaccard + 0.4 * docstring_ratio`; the weights are
# empirical and weight URLs higher because the stub generator and SDK tend
# to keep URLs literally identical while docstrings get reworded.
# ---------------------------------------------------------------------------


def _gather_heuristic_candidates(
    stub_method: MethodIR, stub_base: str
) -> list[tuple[Path, ModuleIR, ApiClassIR, MethodIR]]:
    """Collect SDK methods to score against a single stub method.

    Primary scope: every SDK class with the same ``base=`` (usually under
    20 methods total). Fallback scope: every SDK method anywhere that
    shares the stub's HTTP verb — used only when no SDK class declares the
    stub's base, e.g. when the SDK has restructured its package layout.

    :param stub_method: The method we're trying to match.
    :param stub_base: ``base=`` value of the stub's API class.
    :return: Flat list of ``(path, module_ir, api_class_ir, method_ir)``.
    """
    out: list[tuple[Path, ModuleIR, ApiClassIR, MethodIR]] = []
    for sdk_path, sdk_ir, sdk_cls in _index.find_api_by_base(stub_base):
        for sdk_m in sdk_cls.methods:
            out.append((sdk_path, sdk_ir, sdk_cls, sdk_m))
    if not out:
        # Fallback: any SDK method with the same verb. Wider but still cheap
        # at this codebase size.
        for sdk_ir in _index.all():
            if sdk_ir.api_class is None:
                continue
            for sdk_m in sdk_ir.api_class.methods:
                if sdk_m.verb == stub_method.verb:
                    out.append((Path(sdk_ir.path), sdk_ir, sdk_ir.api_class, sdk_m))
    return out


def _score_method_pair(stub: MethodIR, sdk: MethodIR) -> float:
    """Compute the combined URL+docstring similarity for two methods.

    Methods with different HTTP verbs always score 0. Otherwise the score is
    ``0.6 * url_jaccard + 0.4 * docstring_ratio``.

    :param stub: The stub-side method.
    :param sdk: The SDK-side candidate.
    :return: A score in ``[0, 1]``.
    """
    if stub.verb != sdk.verb:
        return 0.0
    url_sim = _url_jaccard(stub.ep_template or '', sdk.ep_template or '')
    doc_sim = _docstring_ratio(stub.docstring, sdk.docstring)
    return 0.6 * url_sim + 0.4 * doc_sim


def _url_jaccard(a: str, b: str) -> float:
    """Jaccard similarity of the non-placeholder URL tokens.

    Splits each URL on ``/``, drops empty parts and ``{placeholder}`` segments,
    and returns ``|A ∩ B| / |A ∪ B|``. Two URLs that share all literal
    segments score ``1.0`` regardless of how their placeholder names compare.

    :param a: First URL template.
    :param b: Second URL template.
    :return: Jaccard similarity in ``[0, 1]``. Two empty token sets score
        ``1.0``; one empty set and one non-empty score ``0.0``.
    """

    def tokens(u: str) -> set[str]:
        return {t for t in u.split('/') if t and not (t.startswith('{') and t.endswith('}'))}

    ta, tb = tokens(a), tokens(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def _docstring_ratio(a: str | None, b: str | None) -> float:
    """Similarity ratio for the leading description paragraph of two docstrings.

    We strip the Sphinx ``:param`` and ``:rtype`` blocks first because those
    are almost always derived mechanically from the signature and offer no
    information beyond what URLs already provide.

    :param a: First docstring (may be ``None``).
    :param b: Second docstring (may be ``None``).
    :return: :class:`difflib.SequenceMatcher` ratio in ``[0, 1]``.
    """

    def first_para(s: str | None) -> str:
        if not s:
            return ''
        para = s.split(':param', 1)[0].split(':rtype', 1)[0]
        return ' '.join(para.split())

    return difflib.SequenceMatcher(None, first_para(a), first_para(b)).ratio()


def _record_unmatched(
    record: ChangeRecord,
    store: _aliases.AliasStore,
    candidates: list[dict[str, Any]] | None = None,
    best_score: float = 0.0,
) -> None:
    """Append an :class:`UnmatchedEntry` to ``store.unmatched``.

    Called whenever the matcher punts. The driver writes the resulting list
    back to ``aliases.json`` at the end of each run so reviewers can inspect
    what wasn't auto-resolved.

    :param record: The unmatched change record.
    :param store: Alias store to append to.
    :param candidates: Optional list of top heuristic candidates (each a
        small dict with ``sdk_path``, ``sdk_class``, ``sdk_method``,
        ``score``); used to surface near-misses in the report.
    :param best_score: The top heuristic score that was nonetheless below
        :data:`THRESHOLD`.
    """
    store.unmatched.append(
        _aliases.UnmatchedEntry(
            stub_key=f'{record.kind}::{record.qualname}',
            best_score=best_score,
            candidates=candidates or [],
        )
    )

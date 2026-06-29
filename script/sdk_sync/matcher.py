"""
Stub → SDK location resolver.

Given a :class:`~script.sdk_sync.differ.ChangeRecord` produced from a stub
diff, and the :class:`~script.sdk_sync.ir.ModuleIR` of the stub it came from,
the matcher returns a :class:`Match` pointing at the SDK file/class/member
that should receive the equivalent edit. Resolution order:

1. **Alias cache hit.** If the stub key is already in
   :class:`~script.sdk_sync.aliases.AliasStore.method_aliases`,
   ``.model_aliases`` or ``.member_aliases``, return the recorded mapping.
   This is how the matcher stays cheap across runs.
2. **Exact match.** For methods, look up ``(verb, ep_template)`` against the
   SDK index — the join key is stable across stub and SDK because both
   compose URLs the same way. For models/enums/fields/enum-values, look up
   by class name (after applying any aliases).
3. **Heuristic match.** Score every plausible SDK method by
   ``0.6 * URL-token-Jaccard + 0.4 * docstring-similarity`` and accept the
   top candidate when its score clears :data:`THRESHOLD`. For field/enum
   doc-comments, use structural wire-shape matching when class names differ.
4. **Punt.** Append an ``UnmatchedEntry`` to ``store.unmatched`` so the human
   reviewer can see what wasn't auto-resolved, and return ``None``.

The SDK index is built lazily on first access and cached for the process
lifetime — walking ~30 SDK modules with :mod:`ast` is ~100 ms once.
"""

from __future__ import annotations

import ast
import difflib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import aliases as _aliases
from .differ import ChangeRecord
from .ir import ApiClassIR, EnumIR, EnumValueIR, FieldIR, MethodIR, ModelIR, ModuleIR, extract

#: Minimum combined score for the heuristic matcher to accept a match.
#: Below this we punt to the unmatched list and let a human (or the LLM with
#: a tightly scoped prompt) decide.
THRESHOLD = 0.75

# Minimum score for structural doc-comment matching. These are intentionally
# higher than method URL matching because a false field/enum match can rewrite
# a human-authored SDK comment.
STRUCTURAL_MODEL_THRESHOLD = 0.82
STRUCTURAL_ENUM_THRESHOLD = 0.82
STRUCTURAL_MIN_GAP = 0.05

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


@dataclass(frozen=True)
class _ModelCandidate:
    """A structural SDK model candidate for a stub model field.

    :param score: Confidence score in ``[0, 1]``.
    :type score: float
    :param sdk_path: SDK file containing the candidate.
    :type sdk_path: pathlib.Path
    :param sdk_ir: Parsed SDK module IR.
    :type sdk_ir: ModuleIR
    :param sdk_model: Candidate SDK model.
    :type sdk_model: ModelIR
    :param sdk_field: Candidate SDK field matching the stub field's wire name.
    :type sdk_field: FieldIR
    :param detail: Human-readable reason shown in unmatched reports.
    :type detail: str
    """

    score: float
    sdk_path: Path
    sdk_ir: ModuleIR
    sdk_model: ModelIR
    sdk_field: FieldIR
    detail: str


@dataclass(frozen=True)
class _EnumCandidate:
    """A structural SDK enum candidate for a stub enum value.

    :param score: Confidence score in ``[0, 1]``.
    :type score: float
    :param sdk_path: SDK file containing the candidate.
    :type sdk_path: pathlib.Path
    :param sdk_ir: Parsed SDK module IR.
    :type sdk_ir: ModuleIR
    :param sdk_enum: Candidate SDK enum.
    :type sdk_enum: EnumIR
    :param sdk_value: Candidate SDK enum value, or ``None`` when the enum
        shape matches but the specific value cannot be mapped safely.
    :type sdk_value: EnumValueIR | None
    :param detail: Human-readable reason shown in unmatched reports.
    :type detail: str
    """

    score: float
    sdk_path: Path
    sdk_ir: ModuleIR
    sdk_enum: EnumIR
    sdk_value: EnumValueIR | None
    detail: str


class _SDKIndex:
    """Lazily-built read-through index of all SDK feature modules.

    The index walks every Python file under :data:`_SDK_ROOT`, parses it with
    :func:`~script.sdk_sync.ir.extract`, and keeps the resulting IRs in
    memory. Lookups are linear in the number of modules/API classes, which is
    fast enough that we don't need secondary indexes.
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
                # is_sdk=True enables the shared endpoint_resolver's live-replay
                # path so we can recover URL templates from custom helpers
                # (e.g. CQPolicyApi._ep) that the pure-AST walker can't follow.
                self._irs.append(extract(path, is_sdk=True))
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
        """Return every SDK API class declaring the given ``base=``.

        :param base: Value of the ``base=`` keyword on the stub's API class.
        :return: List of ``(path, module_ir, api_class_ir)`` triples; the list
            is usually short (0–3 entries).
        """
        out: list[tuple[Path, ModuleIR, ApiClassIR]] = []
        for ir in self.all():
            for api_class in ir.iter_api_classes():
                if api_class.base == base:
                    out.append((Path(ir.path), ir, api_class))
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
            for api_class in ir.iter_api_classes():
                for m in api_class.methods:
                    if m.verb == verb and m.ep_template == ep_template:
                        out.append((Path(ir.path), ir, api_class, m))
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


def _relative_sdk_path(path: Path) -> str:
    """Return a stable SDK path for reports and persisted aliases.

    :param path: SDK path, absolute or relative.
    :type path: pathlib.Path
    :return: Repo-relative path when possible, otherwise the original string.
    :rtype: str
    """
    try:
        return str(path.relative_to(_SDK_ROOT.parent))
    except ValueError:
        return str(path)


def _member_alias_match(stub_class: str, stub_member: str, kind: str, store: _aliases.AliasStore) -> Match | None:
    """Return a match from a hand-confirmed member alias, if one exists.

    :param stub_class: Stub model or enum class name.
    :type stub_class: str
    :param stub_member: Stub-side field or enum value name.
    :type stub_member: str
    :param kind: Match kind to return, usually ``'model_field'`` or
        ``'enum_value'``.
    :type kind: str
    :param store: Alias store containing optional member aliases.
    :type store: script.sdk_sync.aliases.AliasStore
    :return: A :class:`Match`, or ``None`` when no alias is recorded.
    :rtype: Match | None
    """
    alias = store.member_aliases.get(_aliases.member_key(stub_class, stub_member))
    if alias is None:
        return None
    sdk_path = Path(alias.sdk_path)
    if not sdk_path.is_absolute():
        sdk_path = (_SDK_ROOT.parent / sdk_path).resolve()
    try:
        sdk_ir = next(ir for ir in _index.all() if Path(ir.path) == sdk_path)
    except StopIteration:
        sdk_ir = extract(sdk_path, is_sdk=True)
    return Match(sdk_path, kind, alias.sdk_class, alias.sdk_member, sdk_ir, 1.0, 'member-alias')


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
    member_alias = _member_alias_match(stub_enum, value_name, 'enum_value', store)
    if member_alias is not None:
        return member_alias
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
    member_alias = _member_alias_match(stub_model, field_name, 'model_field', store)
    if member_alias is not None:
        return member_alias
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
            sdk_ir = extract(sdk_path, is_sdk=True)
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
    or methods. We disambiguate by looking at the head of the qualname in
    the *stub* IR first, because the SDK class may have a different name:

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
    if stub_ir.enum_by_name(head) is not None:
        return _match_docstring_enum_value(record, stub_ir, store)
    if stub_ir.model_by_name(head) is not None:
        return _match_docstring_model_field(record, stub_ir, store)
    # Backward-compatible fallback for hand-built tests or unusual records
    # whose stub IR is incomplete.
    if _index.find_enum(head) is not None:
        return _match_enum_value(record, store)
    if _index.find_model(head) is not None:
        return _match_model_field(record, store)
    return _match_method(record, stub_ir, store)


def _match_docstring_enum_value(record: ChangeRecord, stub_ir: ModuleIR, store: _aliases.AliasStore) -> Match | None:
    """Resolve an enum-value doc-comment change, using structural fallback.

    :param record: ``docstring_changed`` record for ``Enum.member``.
    :type record: ChangeRecord
    :param stub_ir: Parsed generated stub IR.
    :type stub_ir: ModuleIR
    :param store: Alias store consulted for manual member/class aliases.
    :type store: script.sdk_sync.aliases.AliasStore
    :return: A resolved enum-value match, or ``None`` if no candidate is safe.
    :rtype: Match | None
    """
    stub_enum_name, value_name = _split_qualname(record.qualname)
    if value_name is None:
        return None
    member_alias = _member_alias_match(stub_enum_name, value_name, 'enum_value', store)
    if member_alias is not None:
        return member_alias

    enum_name = _resolve_class_name(stub_enum_name, store)
    exact = _index.find_enum(enum_name)
    if exact is not None:
        sdk_path, sdk_ir, sdk_enum = exact
        if any(v.name == value_name for v in sdk_enum.values):
            return Match(
                sdk_path,
                'enum_value',
                enum_name,
                value_name,
                sdk_ir,
                1.0,
                'alias' if enum_name != stub_enum_name else 'exact',
            )

    stub_enum = stub_ir.enum_by_name(stub_enum_name)
    if stub_enum is None:
        return None
    stub_value = next((v for v in stub_enum.values if v.name == value_name), None)
    if stub_value is None:
        _record_unmatched(record, store)
        return None

    candidates = _score_enum_candidates(stub_enum, stub_value, stub_ir)
    accepted = _accepted_enum_candidate(candidates)
    if accepted is None:
        _record_unmatched(
            record,
            store,
            candidates=[_enum_candidate_report(candidate) for candidate in candidates[:5]],
            best_score=candidates[0].score if candidates else 0.0,
        )
        return None
    assert accepted.sdk_value is not None
    return Match(
        accepted.sdk_path,
        'enum_value',
        accepted.sdk_enum.name,
        accepted.sdk_value.name,
        accepted.sdk_ir,
        accepted.score,
        'structural-enum',
    )


def _match_docstring_model_field(record: ChangeRecord, stub_ir: ModuleIR, store: _aliases.AliasStore) -> Match | None:
    """Resolve a model-field doc-comment change, using wire-shape fallback.

    :param record: ``docstring_changed`` record for ``Model.field``.
    :type record: ChangeRecord
    :param stub_ir: Parsed generated stub IR.
    :type stub_ir: ModuleIR
    :param store: Alias store consulted for manual member/class aliases.
    :type store: script.sdk_sync.aliases.AliasStore
    :return: A resolved model-field match, or ``None`` if no candidate is safe.
    :rtype: Match | None
    """
    stub_model_name, field_name = _split_qualname(record.qualname)
    if field_name is None:
        return None
    member_alias = _member_alias_match(stub_model_name, field_name, 'model_field', store)
    if member_alias is not None:
        return member_alias

    model_name = _resolve_class_name(stub_model_name, store)
    exact = _index.find_model(model_name)
    if exact is not None:
        sdk_path, sdk_ir, sdk_model = exact
        target = next((f for f in sdk_model.fields if f.name == field_name), None)
        if target is not None:
            return Match(
                sdk_path,
                'model_field',
                model_name,
                target.name,
                sdk_ir,
                1.0,
                'alias' if model_name != stub_model_name else 'exact',
            )

    stub_model = stub_ir.model_by_name(stub_model_name)
    if stub_model is None:
        return None
    stub_field = next((f for f in stub_model.fields if f.name == field_name), None)
    if stub_field is None:
        _record_unmatched(record, store)
        return None

    context_names = _method_return_context_model_names(stub_model_name, stub_ir)
    candidates = _score_model_candidates(stub_model, stub_field, context_names)
    accepted = _accepted_model_candidate(candidates)
    if accepted is None:
        _record_unmatched(
            record,
            store,
            candidates=[_model_candidate_report(candidate) for candidate in candidates[:5]],
            best_score=candidates[0].score if candidates else 0.0,
        )
        return None
    return Match(
        accepted.sdk_path,
        'model_field',
        accepted.sdk_model.name,
        accepted.sdk_field.name,
        accepted.sdk_ir,
        accepted.score,
        'structural-model',
    )


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
# Structural doc-comment matching
#
# These helpers are used only for field/enum `docstring_changed` records. They
# deliberately return ordinary Match objects so deterministic patching remains
# behind the same interface as exact and alias matches.
# ---------------------------------------------------------------------------


def _score_model_candidates(
    stub_model: ModelIR,
    stub_field: FieldIR,
    context_names: set[str] | None = None,
) -> list[_ModelCandidate]:
    """Score SDK models by wire-field shape for one stub field.

    :param stub_model: Stub-side generated model.
    :type stub_model: ModelIR
    :param stub_field: Stub-side field whose comment changed.
    :type stub_field: FieldIR
    :param context_names: SDK model names inferred from matched method returns.
    :type context_names: set[str] | None
    :return: Candidates sorted by descending score.
    :rtype: list[_ModelCandidate]
    """
    context_names = context_names or set()
    stub_wire_names = {_field_wire_name(field) for field in stub_model.fields}
    target_wire_name = _field_wire_name(stub_field)
    candidates: list[_ModelCandidate] = []
    if not stub_wire_names:
        return candidates

    for sdk_ir in _index.all():
        for sdk_model in sdk_ir.models:
            sdk_fields_by_wire = _fields_by_wire_name(sdk_model)
            sdk_wire_names = set(sdk_fields_by_wire)
            target = sdk_fields_by_wire.get(target_wire_name)
            if target is None:
                continue
            shared = stub_wire_names & sdk_wire_names
            if not shared:
                continue
            coverage = len(shared) / len(stub_wire_names)
            precision = len(shared) / len(sdk_wire_names) if sdk_wire_names else 0.0
            context = 1.0 if sdk_model.name in context_names else 0.0
            # Coverage asks "does the SDK model contain the generated model's
            # wire fields?"; precision penalizes broader shared SDK models so
            # a generic model does not beat a focused reusable one. Context is
            # deliberately small: it breaks ties when a matched endpoint
            # already proves the generated return type maps to this SDK type.
            score = (0.65 * coverage) + (0.25 * precision) + (0.10 * context)
            detail = (
                f'wire fields {len(shared)}/{len(stub_wire_names)} shared; '
                f'{len(sdk_wire_names - stub_wire_names)} SDK-only fields'
            )
            if context:
                detail += '; returned by matched endpoint'
            candidates.append(
                _ModelCandidate(
                    score=score,
                    sdk_path=Path(sdk_ir.path),
                    sdk_ir=sdk_ir,
                    sdk_model=sdk_model,
                    sdk_field=target,
                    detail=detail,
                )
            )
    candidates.sort(key=lambda c: (-c.score, _relative_sdk_path(c.sdk_path), c.sdk_model.name, c.sdk_field.name))
    return candidates


def _score_enum_candidates(stub_enum: EnumIR, stub_value: EnumValueIR, stub_ir: ModuleIR) -> list[_EnumCandidate]:
    """Score SDK enums by value/name overlap for one stub enum value.

    :param stub_enum: Stub-side generated enum.
    :type stub_enum: EnumIR
    :param stub_value: Stub-side enum value whose comment changed.
    :type stub_value: EnumValueIR
    :param stub_ir: Parsed generated stub IR, used for type-reference context.
    :type stub_ir: ModuleIR
    :return: Candidates sorted by descending score.
    :rtype: list[_EnumCandidate]
    """
    stub_names = {value.name for value in stub_enum.values}
    stub_values = {_enum_wire_value(value) for value in stub_enum.values}
    stub_values.discard(None)
    context_names = _enum_type_context_names(stub_enum.name, stub_ir)
    target_wire_value = _enum_wire_value(stub_value)
    candidates: list[_EnumCandidate] = []
    if not stub_names and not stub_values:
        return candidates

    for sdk_ir in _index.all():
        for sdk_enum in sdk_ir.enums:
            sdk_by_name = {value.name: value for value in sdk_enum.values}
            sdk_by_wire = {
                wire_value: value for value in sdk_enum.values if (wire_value := _enum_wire_value(value)) is not None
            }
            sdk_names = set(sdk_by_name)
            sdk_values = set(sdk_by_wire)
            value_overlap = len(stub_values & sdk_values) / len(stub_values) if stub_values else 0.0
            name_overlap = len(stub_names & sdk_names) / len(stub_names) if stub_names else 0.0
            same_name_target = sdk_by_name.get(stub_value.name)
            same_value_target = sdk_by_wire.get(target_wire_value) if target_wire_value is not None else None
            sdk_target = same_name_target or same_value_target
            member_match = 1.0 if sdk_target is not None else 0.0
            context = 1.0 if sdk_enum.name in context_names else 0.0
            # Value overlap is the strongest enum-class signal because wire
            # values are the public API contract. Name overlap helps with
            # generated Python spelling, member_match proves this specific
            # doc-comment has an SDK line to update, and context ties the enum
            # back to a structurally matched model field.
            score = (0.50 * value_overlap) + (0.25 * name_overlap) + (0.15 * member_match) + (0.10 * context)
            if score == 0:
                continue
            if sdk_target is None:
                detail = 'enum overlaps, but target member has no same name or wire value'
            elif same_name_target is not None and same_value_target is not None:
                detail = 'target member matches by name and wire value'
            elif same_name_target is not None:
                detail = 'target member matches by name'
            else:
                detail = 'target member matches by wire value'
            if context:
                detail += '; referenced by matched model field'
            candidates.append(
                _EnumCandidate(
                    score=score,
                    sdk_path=Path(sdk_ir.path),
                    sdk_ir=sdk_ir,
                    sdk_enum=sdk_enum,
                    sdk_value=sdk_target,
                    detail=detail,
                )
            )
    candidates.sort(
        key=lambda c: (
            -c.score,
            c.sdk_value is None,
            _relative_sdk_path(c.sdk_path),
            c.sdk_enum.name,
            c.sdk_value.name if c.sdk_value is not None else '',
        )
    )
    return candidates


def _accepted_model_candidate(candidates: list[_ModelCandidate]) -> _ModelCandidate | None:
    """Return the accepted model candidate, if one is unique enough.

    :param candidates: Sorted model candidates.
    :type candidates: list[_ModelCandidate]
    :return: The accepted candidate or ``None``.
    :rtype: _ModelCandidate | None
    """
    if not candidates or candidates[0].score < STRUCTURAL_MODEL_THRESHOLD:
        return None
    if len(candidates) > 1 and candidates[0].score - candidates[1].score < STRUCTURAL_MIN_GAP:
        return None
    return candidates[0]


def _accepted_enum_candidate(candidates: list[_EnumCandidate]) -> _EnumCandidate | None:
    """Return the accepted enum candidate, if one is unique and has a member.

    :param candidates: Sorted enum candidates.
    :type candidates: list[_EnumCandidate]
    :return: The accepted candidate or ``None``.
    :rtype: _EnumCandidate | None
    """
    if not candidates or candidates[0].score < STRUCTURAL_ENUM_THRESHOLD:
        return None
    if candidates[0].sdk_value is None:
        return None
    if len(candidates) > 1 and candidates[0].score - candidates[1].score < STRUCTURAL_MIN_GAP:
        return None
    return candidates[0]


def _model_candidate_report(candidate: _ModelCandidate) -> dict[str, Any]:
    """Render a model structural candidate for ``aliases.json``/report output.

    :param candidate: Candidate to render.
    :type candidate: _ModelCandidate
    :return: JSON-friendly candidate details.
    :rtype: dict[str, Any]
    """
    return {
        'sdk_path': _relative_sdk_path(candidate.sdk_path),
        'sdk_class': candidate.sdk_model.name,
        'sdk_member': candidate.sdk_field.name,
        'score': round(candidate.score, 4),
        'detail': candidate.detail,
    }


def _enum_candidate_report(candidate: _EnumCandidate) -> dict[str, Any]:
    """Render an enum structural candidate for ``aliases.json``/report output.

    :param candidate: Candidate to render.
    :type candidate: _EnumCandidate
    :return: JSON-friendly candidate details.
    :rtype: dict[str, Any]
    """
    return {
        'sdk_path': _relative_sdk_path(candidate.sdk_path),
        'sdk_class': candidate.sdk_enum.name,
        'sdk_member': candidate.sdk_value.name if candidate.sdk_value is not None else None,
        'score': round(candidate.score, 4),
        'detail': candidate.detail,
    }


def _field_wire_name(field: FieldIR) -> str:
    """Return the serialized JSON name for a model field.

    :param field: Field IR to inspect.
    :type field: FieldIR
    :return: Explicit ``Field(alias=...)`` when present, otherwise the SDK's
        camel-case alias generated from the Python field name.
    :rtype: str
    """
    return _field_alias(field.default) or _to_camel(field.name)


def _field_alias(default: str | None) -> str | None:
    """Extract a string alias from a Pydantic ``Field(...)`` default.

    :param default: Source text of a field default expression.
    :type default: str | None
    :return: Alias string, or ``None`` when no explicit alias exists.
    :rtype: str | None
    """
    if not default:
        return None
    try:
        expr = ast.parse(default, mode='eval').body
    except SyntaxError:
        return None
    if not isinstance(expr, ast.Call):
        return None
    func = expr.func
    if isinstance(func, ast.Name):
        func_name = func.id
    elif isinstance(func, ast.Attribute):
        func_name = func.attr
    else:
        func_name = ''
    if func_name != 'Field':
        return None
    for keyword in expr.keywords:
        if keyword.arg == 'alias' and isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
            return keyword.value.value
    return None


def _fields_by_wire_name(model: ModelIR) -> dict[str, FieldIR]:
    """Build a wire-name index for a model's fields.

    :param model: Model whose fields should be indexed.
    :type model: ModelIR
    :return: Mapping of wire field name to :class:`FieldIR`.
    :rtype: dict[str, FieldIR]
    """
    out: dict[str, FieldIR] = {}
    for field in model.fields:
        out.setdefault(_field_wire_name(field), field)
    return out


def _enum_wire_value(value: EnumValueIR) -> str | None:
    """Return the runtime string value represented by an enum assignment.

    :param value: Enum value IR.
    :type value: EnumValueIR
    :return: Literal string RHS, or ``None`` if the RHS is not a string
        literal.
    :rtype: str | None
    """
    try:
        expr = ast.parse(value.value, mode='eval').body
        literal = ast.literal_eval(expr)
    except (SyntaxError, ValueError):
        return None
    return literal if isinstance(literal, str) else None


def _to_camel(name: str) -> str:
    """Convert a snake_case Python field name to the SDK's camelCase alias.

    :param name: Python field name.
    :type name: str
    :return: Camel-case alias.
    :rtype: str
    """
    return ''.join(part.title() if index else part for index, part in enumerate(name.split('_')))


def _method_return_context_model_names(stub_model_name: str, stub_ir: ModuleIR) -> set[str]:
    """Infer SDK model names from exact-matched methods returning a stub model.

    :param stub_model_name: Stub model class being resolved.
    :type stub_model_name: str
    :param stub_ir: Parsed generated stub IR.
    :type stub_ir: ModuleIR
    :return: SDK class names found in matching SDK method return annotations.
    :rtype: set[str]
    """
    out: set[str] = set()
    for api_class in stub_ir.iter_api_classes():
        for method in api_class.methods:
            if method.returns is None or stub_model_name not in _referenced_type_names(method.returns):
                continue
            if method.verb is None or method.ep_template is None:
                continue
            exact = _index.find_api_with_endpoint(method.verb, method.ep_template)
            if len(exact) != 1:
                continue
            _sdk_path, _sdk_ir, _sdk_class, sdk_method = exact[0]
            if sdk_method.returns:
                out.update(_referenced_type_names(sdk_method.returns))
    return out


def _enum_type_context_names(stub_enum_name: str, stub_ir: ModuleIR) -> set[str]:
    """Infer SDK enum names from structurally matched models using the enum.

    :param stub_enum_name: Stub enum class being resolved.
    :type stub_enum_name: str
    :param stub_ir: Parsed generated stub IR.
    :type stub_ir: ModuleIR
    :return: SDK enum class names referenced by matching SDK model fields.
    :rtype: set[str]
    """
    out: set[str] = set()
    for stub_model in stub_ir.models:
        for stub_field in stub_model.fields:
            if stub_enum_name not in _referenced_type_names(stub_field.annotation):
                continue
            candidates = _score_model_candidates(stub_model, stub_field)
            accepted = _accepted_model_candidate(candidates)
            if accepted is None:
                continue
            out.update(_referenced_type_names(accepted.sdk_field.annotation))
    return {name for name in out if _index.find_enum(name) is not None}


def _referenced_type_names(annotation: str) -> set[str]:
    """Return likely user-defined type names from an annotation string.

    :param annotation: Source text of a Python type annotation.
    :type annotation: str
    :return: Identifier names referenced by the annotation, excluding common
        typing and primitive names.
    :rtype: set[str]
    """
    ignored = {
        'Any',
        'Optional',
        'Union',
        'Generator',
        'Iterator',
        'Iterable',
        'Sequence',
        'Mapping',
        'dict',
        'list',
        'set',
        'tuple',
        'str',
        'int',
        'float',
        'bool',
        'None',
        'NoneType',
        'builtins',
    }
    return {name for name in re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', annotation) if name not in ignored}


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
            for sdk_cls in sdk_ir.iter_api_classes():
                for sdk_m in sdk_cls.methods:
                    if sdk_m.verb == stub_method.verb:
                        out.append((Path(sdk_ir.path), sdk_ir, sdk_cls, sdk_m))
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

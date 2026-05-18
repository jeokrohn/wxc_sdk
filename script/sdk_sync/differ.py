"""
Stub-vs-stub differ.

Compares the :class:`~script.sdk_sync.ir.ModuleIR` of the *old* version of a
stub file (typically obtained via ``git show HEAD:<path>``) against the *new*
version (working tree) and emits a list of typed :class:`ChangeRecord` objects.

Each record carries:

- ``kind`` — the change category (see :data:`ChangeKindLiteral`). This is what
  the dispatcher routes on.
- ``qualname`` — a dotted path identifying the affected entity
  (``Device.mac``, ``DevicesApi.list_devices``,
  ``DeviceConnectionStatus.pending``).
- ``old`` / ``new`` — IR payloads as plain dicts, so the record is trivially
  JSON-serializable and can be embedded in fixtures and the human-readable
  report.
- ``severity`` — ``'trivial'`` if the deterministic patcher *provably* handles
  this kind of change (enum value, simple field, doc-comment), ``'review'``
  otherwise. The patcher runs its own safety re-checks; this flag is only a
  routing hint, not a guarantee that the patch is safe.

The differ is stateless: ``diff_irs(old, new)`` is a pure function. It does no
matching against the SDK — that's the matcher's job.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from .ir import EnumIR, EnumValueIR, FieldIR, MethodIR, ModelIR, ModuleIR, ParamIR

#: All the change categories the differ can emit. Kept as a closed enumeration
#: so the dispatcher's routing table can be exhaustive.
ChangeKindLiteral = Literal[
    'enum_value_added',
    'enum_value_removed',
    'model_field_added',
    'model_field_removed',
    'model_added',
    'model_removed',
    'method_added',
    'method_removed',
    'method_param_added',
    'method_param_removed',
    'method_return_changed',
    'type_changed',
    'docstring_changed',
]


@dataclass(frozen=True)
class ChangeRecord:
    """One typed difference between an old and a new IR.

    :param kind: One of the values in :data:`ChangeKindLiteral`.
    :param qualname: Dotted identifier of the affected entity. The shape
        depends on ``kind``: ``"<Class>.<field>"`` for fields/enum-values,
        ``"<ApiClass>.<method>"`` for methods, or
        ``"<ApiClass>.<method>(<param>)"`` for parameter-level type changes.
    :param old: IR-shaped dict of the entity before the change, or ``None``
        for pure additions.
    :param new: IR-shaped dict of the entity after the change, or ``None``
        for pure removals.
    :param severity: ``'trivial'`` for changes the deterministic patcher
        whitelist handles, ``'review'`` for anything that needs the LLM step
        or a human.
    :param notes: Optional free-form tags shown in the report (for example,
        ``('field annotation changed',)``).
    """

    kind: str
    qualname: str
    old: dict[str, Any] | None
    new: dict[str, Any] | None
    severity: Literal['trivial', 'review']
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Return a plain-dict representation suitable for JSON serialization.

        :return: A ``dict`` with the same keys as the dataclass fields.
        """
        return asdict(self)


def diff_irs(old: ModuleIR, new: ModuleIR) -> list[ChangeRecord]:
    """Compute the full list of change records between two module IRs.

    Order of returned records: enum changes first, then model changes, then
    API-class changes. Within each section, additions precede removals, and
    same-entity modifications come last. This ordering keeps the report
    grouped sensibly without requiring callers to sort it.

    :param old: IR of the file at the previous git revision.
    :param new: IR of the file in the current working tree.
    :return: List of :class:`ChangeRecord`, possibly empty.
    """
    records: list[ChangeRecord] = []
    records.extend(_diff_enums(old, new))
    records.extend(_diff_models(old, new))
    records.extend(_diff_api(old, new))
    return records


# ---------------------------------------------------------------------------
# Enums
#
# An enum class itself can be added or removed (reported as
# `model_added`/`model_removed` so the dispatcher uses the same routing path
# as Pydantic-model changes). For enums that exist on both sides we compare
# the value lists.
# ---------------------------------------------------------------------------


def _diff_enums(old: ModuleIR, new: ModuleIR) -> list[ChangeRecord]:
    """Compute differences between the enum sets of two modules.

    :param old: IR of the file at the previous revision.
    :param new: IR of the file in the working tree.
    :return: List of records covering enum-class adds/removes plus
        intra-enum value differences.
    """
    out: list[ChangeRecord] = []
    old_map = {e.name: e for e in old.enums}
    new_map = {e.name: e for e in new.enums}
    # Whole-enum additions and removals reuse the `model_*` kinds — the
    # dispatcher and matcher treat enum classes and model classes the same
    # way (both are "named class moves").
    for name in new_map.keys() - old_map.keys():
        out.append(
            ChangeRecord(
                kind='model_added',
                qualname=name,
                old=None,
                new=_enum_to_dict(new_map[name]),
                severity='review',
                notes=('new enum class — must be added to SDK by hand or LLM',),
            )
        )
    for name in old_map.keys() - new_map.keys():
        out.append(
            ChangeRecord(
                kind='model_removed',
                qualname=name,
                old=_enum_to_dict(old_map[name]),
                new=None,
                severity='review',
            )
        )
    for name in old_map.keys() & new_map.keys():
        out.extend(_diff_enum_values(old_map[name], new_map[name]))
    return out


def _diff_enum_values(old: EnumIR, new: EnumIR) -> list[ChangeRecord]:
    """Compute differences between two same-named enum classes.

    Emits:

    - ``enum_value_added`` / ``enum_value_removed`` for member set deltas.
    - ``type_changed`` when a member's RHS value differs (rare but possible
      if the OpenAPI spec changes a wire value).
    - ``docstring_changed`` when only the ``#:`` doc-comment text differs.

    :param old: IR of the enum class at the previous revision.
    :param new: IR of the same enum class in the working tree.
    :return: List of records, possibly empty if the enums match exactly.
    """
    out: list[ChangeRecord] = []
    old_vals = {v.name: v for v in old.values}
    new_vals = {v.name: v for v in new.values}
    for vname in new_vals.keys() - old_vals.keys():
        out.append(
            ChangeRecord(
                kind='enum_value_added',
                qualname=f'{new.name}.{vname}',
                old=None,
                new=_enum_value_to_dict(new_vals[vname]),
                severity='trivial',
            )
        )
    for vname in old_vals.keys() - new_vals.keys():
        out.append(
            ChangeRecord(
                kind='enum_value_removed',
                qualname=f'{old.name}.{vname}',
                old=_enum_value_to_dict(old_vals[vname]),
                new=None,
                severity='trivial',
            )
        )
    for vname in old_vals.keys() & new_vals.keys():
        o = old_vals[vname]
        n = new_vals[vname]
        if o.value != n.value:
            out.append(
                ChangeRecord(
                    kind='type_changed',
                    qualname=f'{new.name}.{vname}',
                    old=_enum_value_to_dict(o),
                    new=_enum_value_to_dict(n),
                    severity='review',
                    notes=('enum value RHS changed',),
                )
            )
        if (o.doc_comment or None) != (n.doc_comment or None):
            out.append(
                ChangeRecord(
                    kind='docstring_changed',
                    qualname=f'{new.name}.{vname}',
                    old={'doc_comment': o.doc_comment},
                    new={'doc_comment': n.doc_comment},
                    severity='trivial',
                )
            )
    return out


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


def _diff_models(old: ModuleIR, new: ModuleIR) -> list[ChangeRecord]:
    """Compute differences between the Pydantic model sets of two modules.

    :param old: IR of the file at the previous revision.
    :param new: IR of the file in the working tree.
    :return: Model-class adds/removes plus per-field differences for models
        that exist on both sides.
    """
    out: list[ChangeRecord] = []
    old_map = {m.name: m for m in old.models}
    new_map = {m.name: m for m in new.models}
    for name in new_map.keys() - old_map.keys():
        out.append(
            ChangeRecord(
                kind='model_added',
                qualname=name,
                old=None,
                new=_model_to_dict(new_map[name]),
                severity='review',
                notes=('new model class — must be added to SDK by hand or LLM',),
            )
        )
    for name in old_map.keys() - new_map.keys():
        out.append(
            ChangeRecord(
                kind='model_removed',
                qualname=name,
                old=_model_to_dict(old_map[name]),
                new=None,
                severity='review',
            )
        )
    for name in old_map.keys() & new_map.keys():
        out.extend(_diff_model_fields(old_map[name], new_map[name]))
    return out


def _diff_model_fields(old: ModelIR, new: ModelIR) -> list[ChangeRecord]:
    """Compute per-field differences between two same-named models.

    Emits:

    - ``model_field_added`` / ``model_field_removed`` for set deltas
      (``severity='trivial'`` — the patcher's whitelist covers these).
    - ``type_changed`` when the annotation or default differs
      (``severity='review'`` — the LLM stage handles these).
    - ``docstring_changed`` when only the ``#:`` doc-comment differs
      (``severity='trivial'`` — patcher can replace the comment in place).

    :param old: Model IR at the previous revision.
    :param new: Model IR in the working tree.
    :return: List of records describing each field-level difference.
    """
    out: list[ChangeRecord] = []
    old_fields = {f.name: f for f in old.fields}
    new_fields = {f.name: f for f in new.fields}
    for fname in new_fields.keys() - old_fields.keys():
        out.append(
            ChangeRecord(
                kind='model_field_added',
                qualname=f'{new.name}.{fname}',
                old=None,
                new=_field_to_dict(new_fields[fname]),
                severity='trivial',
            )
        )
    for fname in old_fields.keys() - new_fields.keys():
        out.append(
            ChangeRecord(
                kind='model_field_removed',
                qualname=f'{old.name}.{fname}',
                old=_field_to_dict(old_fields[fname]),
                new=None,
                severity='trivial',
            )
        )
    for fname in old_fields.keys() & new_fields.keys():
        o = old_fields[fname]
        n = new_fields[fname]
        # Annotation change wins over default change: a re-typed field's
        # default is almost always meaningless on its own.
        if o.canonical_annotation != n.canonical_annotation:
            out.append(
                ChangeRecord(
                    kind='type_changed',
                    qualname=f'{new.name}.{fname}',
                    old=_field_to_dict(o),
                    new=_field_to_dict(n),
                    severity='review',
                    notes=('field annotation changed',),
                )
            )
        elif (o.default or '') != (n.default or ''):
            out.append(
                ChangeRecord(
                    kind='type_changed',
                    qualname=f'{new.name}.{fname}',
                    old=_field_to_dict(o),
                    new=_field_to_dict(n),
                    severity='review',
                    notes=('field default changed',),
                )
            )
        if (o.doc_comment or None) != (n.doc_comment or None):
            out.append(
                ChangeRecord(
                    kind='docstring_changed',
                    qualname=f'{new.name}.{fname}',
                    old={'doc_comment': o.doc_comment},
                    new={'doc_comment': n.doc_comment},
                    severity='trivial',
                )
            )
    return out


# ---------------------------------------------------------------------------
# API methods
#
# Method identity uses the Python name because the stub generator is stable
# on operation names. Renamed operations show up as a (removed, added) pair
# and the matcher's heuristic is what unifies them across stub-and-SDK.
# ---------------------------------------------------------------------------


def _diff_api(old: ModuleIR, new: ModuleIR) -> list[ChangeRecord]:
    """Compute differences between the API classes of two modules.

    Adding or removing the API class itself is reported as a single
    coarse-grained record (``qualname='<Class>.*'``); the LLM stage is the
    only sensible handler for such a sweeping change.

    :param old: IR of the file at the previous revision.
    :param new: IR of the file in the working tree.
    :return: List of method/parameter/return/docstring difference records.
    """
    if old.api_class is None and new.api_class is None:
        return []
    if new.api_class is not None and old.api_class is None:
        cls = new.api_class
        return [
            ChangeRecord(
                kind='method_added',
                qualname=f'{cls.name}.*',
                old=None,
                new={'class': cls.name},
                severity='review',
                notes=('entire API class added/removed',),
            )
        ]
    if old.api_class is not None and new.api_class is None:
        cls = old.api_class
        return [
            ChangeRecord(
                kind='method_removed',
                qualname=f'{cls.name}.*',
                old={'class': cls.name},
                new=None,
                severity='review',
                notes=('entire API class added/removed',),
            )
        ]
    assert old.api_class is not None and new.api_class is not None  # for mypy's narrowing
    out: list[ChangeRecord] = []
    old_map = {m.name: m for m in old.api_class.methods}
    new_map = {m.name: m for m in new.api_class.methods}
    for mname in new_map.keys() - old_map.keys():
        out.append(
            ChangeRecord(
                kind='method_added',
                qualname=f'{new.api_class.name}.{mname}',
                old=None,
                new=_method_to_dict(new_map[mname]),
                severity='review',
            )
        )
    for mname in old_map.keys() - new_map.keys():
        out.append(
            ChangeRecord(
                kind='method_removed',
                qualname=f'{old.api_class.name}.{mname}',
                old=_method_to_dict(old_map[mname]),
                new=None,
                severity='review',
            )
        )
    for mname in old_map.keys() & new_map.keys():
        out.extend(_diff_method(new.api_class.name, old_map[mname], new_map[mname]))
    return out


def _diff_method(class_name: str, old: MethodIR, new: MethodIR) -> list[ChangeRecord]:
    """Compute differences within a single method that exists on both sides.

    Emits one record per change axis (params added/removed, params retyped,
    return-annotation changed, docstring changed). The patcher handles only
    docstring changes deterministically; everything else flows to the LLM.

    :param class_name: Name of the enclosing API class, used to build the
        ``qualname`` for the records.
    :param old: Method IR at the previous revision.
    :param new: Method IR in the working tree.
    :return: List of records describing each axis of drift.
    """
    out: list[ChangeRecord] = []
    qn = f'{class_name}.{new.name}'
    old_params = {p.name: p for p in old.params}
    new_params = {p.name: p for p in new.params}
    new_param_names = [p.name for p in new.params]
    added_param_names = {p.name for p in new.params if p.name not in old_params}
    for pname in new_param_names:
        if pname not in added_param_names:
            continue
        out.append(
            ChangeRecord(
                kind='method_param_added',
                qualname=qn,
                old=None,
                new=_method_param_added_payload(new.params, pname, added_param_names),
                severity='review',
            )
        )
    for pname in old_params.keys() - new_params.keys():
        out.append(
            ChangeRecord(
                kind='method_param_removed',
                qualname=qn,
                old={'param': asdict(old_params[pname])},
                new=None,
                severity='review',
            )
        )
    for pname in old_params.keys() & new_params.keys():
        o = old_params[pname]
        n = new_params[pname]
        if (o.annotation or '') != (n.annotation or '') or (o.default or '') != (n.default or ''):
            out.append(
                ChangeRecord(
                    kind='type_changed',
                    qualname=f'{qn}({pname})',
                    old={'param': asdict(o)},
                    new={'param': asdict(n)},
                    severity='review',
                )
            )
    if (old.returns or '') != (new.returns or ''):
        out.append(
            ChangeRecord(
                kind='method_return_changed',
                qualname=qn,
                old={'returns': old.returns},
                new={'returns': new.returns},
                severity='review',
            )
        )
    if (old.docstring or '') != (new.docstring or ''):
        out.append(
            ChangeRecord(
                kind='docstring_changed',
                qualname=qn,
                old={'docstring': old.docstring},
                new={'docstring': new.docstring},
                severity='trivial',
            )
        )
    return out


# ---------------------------------------------------------------------------
# IR → dict helpers
#
# Used to populate ChangeRecord.old/new. We deliberately drop the IR's
# `source_text` and line numbers from the dict form — those are only useful
# to the patcher, and including them in records would bloat the report and
# pollute test fixtures.
# ---------------------------------------------------------------------------


def _enum_to_dict(e: EnumIR) -> dict[str, Any]:
    """Project an :class:`EnumIR` to a JSON-friendly dict.

    :param e: Enum IR.
    :return: Dict containing only ``name`` and ``values``.
    """
    return {
        'name': e.name,
        'values': [_enum_value_to_dict(v) for v in e.values],
    }


def _enum_value_to_dict(v: EnumValueIR) -> dict[str, Any]:
    """Project an :class:`EnumValueIR` to a JSON-friendly dict.

    :param v: Enum value IR.
    :return: Dict containing ``name``, ``value`` (source RHS) and
        ``doc_comment``.
    """
    return {'name': v.name, 'value': v.value, 'doc_comment': v.doc_comment}


def _model_to_dict(m: ModelIR) -> dict[str, Any]:
    """Project a :class:`ModelIR` to a JSON-friendly dict.

    :param m: Model IR.
    :return: Dict containing ``name``, ``bases``, ``fields`` (each as a
        nested dict) and ``has_custom_validators``.
    """
    return {
        'name': m.name,
        'bases': list(m.bases),
        'fields': [_field_to_dict(f) for f in m.fields],
        'has_custom_validators': m.has_custom_validators,
    }


def _field_to_dict(f: FieldIR) -> dict[str, Any]:
    """Project a :class:`FieldIR` to a JSON-friendly dict.

    :param f: Field IR.
    :return: Dict containing ``name``, ``annotation``, ``default`` and
        ``doc_comment``.
    """
    return {
        'name': f.name,
        'annotation': f.annotation,
        'default': f.default,
        'doc_comment': f.doc_comment,
    }


def _method_param_added_payload(params: tuple[ParamIR, ...], name: str, added_names: set[str]) -> dict[str, Any]:
    """Build the payload for one added method parameter.

    The full stub-side parameter order is carried with each add so downstream
    LLM prompts and semantic validation can enforce where the new parameter
    belongs relative to existing SDK parameters.
    """
    param_list = [asdict(p) for p in params]
    names = [p['name'] for p in param_list]
    index = names.index(name)
    insert_before = next((candidate for candidate in names[index + 1 :] if candidate not in added_names), None)
    return {
        'param': param_list[index],
        'params': param_list,
        'insert_after': names[index - 1] if index > 0 else None,
        'insert_before': insert_before,
    }


def _method_to_dict(m: MethodIR) -> dict[str, Any]:
    """Project a :class:`MethodIR` to a JSON-friendly dict.

    Includes ``verb`` and ``ep_template`` so the matcher can resolve methods
    even when the parent IR is no longer in scope (notably for removed
    methods, which exist only in the old IR by the time the matcher runs).

    :param m: Method IR.
    :return: Dict with the method's name, endpoint key, parameters, return
        annotation, and docstring.
    """
    return {
        'name': m.name,
        'verb': m.verb,
        'ep_template': m.ep_template,
        'params': [asdict(p) for p in m.params],
        'returns': m.returns,
        'docstring': m.docstring,
    }

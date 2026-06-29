"""
Deterministic line-range splicing patcher.

The patcher handles the narrow set of changes where a literal text edit is
provably safe. Anything outside that set returns :class:`Punt` and the
dispatcher routes the change to the LLM step.

Why line-range splicing rather than :mod:`libcst` or :func:`ast.unparse`?

- ``ast.unparse`` discards comments — fatal for this codebase because the
  ``#:`` Pydantic field doc-comments are load-bearing.
- ``libcst`` would preserve comments, but it's not a project dependency and
  pinning a second parser across Python 3.9–3.13 is overkill for the small
  set of edits we need.

The chosen approach reads the source as text, uses :mod:`ast` line numbers as
anchors, and inserts/deletes whole lines. ``ruff format`` runs as a post-pass
to normalize style.

Safe edits implemented:

- ``enum_value_added`` — append a ``name = 'value'`` line (with ``#:`` doc
  comment if the stub provided one) after the last enum value.
- ``enum_value_removed`` — delete the line(s) of the named enum value.
- ``model_field_added`` — append after the last model field, only when no
  validator references the new field name and the new annotation is a
  single line.
- ``model_field_removed`` — delete the field's line(s), only when no
  validator references the field name.
- ``docstring_changed`` (field/enum doc-comment) — only when the SDK's
  current ``#:`` block is byte-identical to the *old* stub value (proof
  nobody has hand-edited it).

Method docstring rewriting is intentionally *not* implemented here; the
patcher refuses and routes those to the LLM, because SDK method docstrings
sometimes intentionally diverge from the upstream prose.

The patcher's return is :class:`PatchResult` (with the rewritten source) on
success, :class:`Punt` (with a human-readable reason) otherwise. The
dispatcher is responsible for persisting :attr:`PatchResult.new_text`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .differ import ChangeRecord
from .matcher import Match


@dataclass(frozen=True)
class Punt:
    """A signal that the deterministic patcher cannot or will not apply this change.

    :param reason: Human-readable explanation. Substrings of this reason are
        used by the dispatcher (e.g. ``'idempotent skip'``) to distinguish a
        successful no-op from a genuine refusal.
    """

    reason: str


@dataclass(frozen=True)
class PatchResult:
    """A successful in-memory rewrite.

    The caller (the dispatcher) writes :attr:`new_text` back to the file. The
    patcher does no I/O of its own.

    :param new_text: The fully rewritten SDK source. Replaces the original
        file's contents.
    :param summary: Short, one-line description of what changed; shown in the
        report (``"added enum value ConnectionStatus.pending"``).
    """

    new_text: str
    summary: str


PatchOutcome = PatchResult | Punt


def apply(record: ChangeRecord, match: Match) -> PatchOutcome:
    """Dispatch a change record to the appropriate per-kind handler.

    :param record: The change being applied.
    :param match: The resolved SDK target from :func:`script.sdk_sync.matcher.match`.
    :return: A :class:`PatchResult` on success or a :class:`Punt` if the
        change is outside the deterministic whitelist or fails one of the
        per-handler safety checks.
    """
    if record.kind == 'enum_value_added':
        return _enum_value_added(record, match)
    if record.kind == 'enum_value_removed':
        return _enum_value_removed(record, match)
    if record.kind == 'model_field_added':
        return _model_field_added(record, match)
    if record.kind == 'model_field_removed':
        return _model_field_removed(record, match)
    if record.kind == 'docstring_changed':
        return _docstring_changed(record, match)
    return Punt(f'{record.kind} is not in the deterministic-patcher whitelist')


# ---------------------------------------------------------------------------
# Enum value adds / removes
# ---------------------------------------------------------------------------


def _enum_value_added(record: ChangeRecord, match: Match) -> PatchOutcome:
    """Append a new value to an enum class.

    Safety checks: the enum must exist in the SDK, it must already have at
    least one value (so we have an insertion anchor), the change record
    must carry name + value, and the value must not already exist (an
    idempotent skip).

    :param record: A ``enum_value_added`` change record.
    :param match: A :class:`Match` of kind ``'enum_value'``.
    :return: :class:`PatchResult` with the inserted line, or :class:`Punt`.
    """
    sdk_ir = match.sdk_module_ir
    enum = sdk_ir.enum_by_name(match.sdk_class)
    if enum is None:
        return Punt(f'enum {match.sdk_class!r} not found in SDK')
    if enum.last_value_end_lineno is None:
        return Punt(f'enum {enum.name} has no values — cannot determine insertion anchor')
    new_payload = record.new or {}
    new_name = new_payload.get('name')
    new_value = new_payload.get('value')
    new_doc = new_payload.get('doc_comment')
    if not new_name or new_value is None:
        return Punt('enum_value_added record missing name/value')
    if any(v.name == new_name for v in enum.values):
        return Punt(f'enum value {enum.name}.{new_name} already present (idempotent skip)')

    indent = _detect_member_indent(sdk_ir.source_text, enum.lineno, enum.last_value_end_lineno)
    lines_to_add: list[str] = []
    if new_doc:
        for doc_line in new_doc.splitlines():
            lines_to_add.append(f'{indent}#: {doc_line}')
    lines_to_add.append(f'{indent}{new_name} = {new_value}')

    new_text = _splice_after(sdk_ir.source_text, enum.last_value_end_lineno, lines_to_add)
    return PatchResult(new_text, f'added enum value {enum.name}.{new_name}')


def _enum_value_removed(record: ChangeRecord, match: Match) -> PatchOutcome:
    """Delete an enum value (and any ``#:`` block immediately above it).

    :param record: A ``enum_value_removed`` change record.
    :param match: A :class:`Match` of kind ``'enum_value'``.
    :return: :class:`PatchResult` with the line(s) removed, or :class:`Punt`.
    """
    sdk_ir = match.sdk_module_ir
    enum = sdk_ir.enum_by_name(match.sdk_class)
    if enum is None:
        return Punt(f'enum {match.sdk_class!r} not found in SDK')
    value_name = match.sdk_member
    if value_name is None:
        return Punt('enum_value_removed match missing value name')
    target = next((v for v in enum.values if v.name == value_name), None)
    if target is None:
        return Punt(f'enum value {enum.name}.{value_name} not found in SDK')

    start_lineno = _doc_comment_start_above(sdk_ir.source_text, target.lineno)
    end_lineno = target.end_lineno
    new_text = _delete_line_range(sdk_ir.source_text, start_lineno, end_lineno)
    return PatchResult(new_text, f'removed enum value {enum.name}.{value_name}')


# ---------------------------------------------------------------------------
# Model field adds / removes
#
# Refuse with a `Punt` whenever the field is referenced by a validator.
# Validators encode hand-authored SDK invariants and silently dropping or
# adding a field they reference would invalidate that invariant.
# ---------------------------------------------------------------------------


def _model_field_added(record: ChangeRecord, match: Match) -> PatchOutcome:
    """Append a new field to a Pydantic model.

    Safety: the model must exist, must have an insertion anchor, the field
    must not already exist (idempotent skip), the field name must not appear
    inside any ``@field_validator(...)`` positional string, and the
    annotation must fit on a single line.

    :param record: A ``model_field_added`` change record.
    :param match: A :class:`Match` of kind ``'model_field'``.
    :return: :class:`PatchResult` or :class:`Punt`.
    """
    sdk_ir = match.sdk_module_ir
    model = sdk_ir.model_by_name(match.sdk_class)
    if model is None:
        return Punt(f'model {match.sdk_class!r} not found in SDK')
    if model.last_field_end_lineno is None:
        return Punt(f'model {model.name} has no field anchor — cannot insert')
    new_payload = record.new or {}
    field_name = new_payload.get('name')
    annotation = new_payload.get('annotation')
    default = new_payload.get('default')
    doc_comment = new_payload.get('doc_comment')
    if not field_name or not annotation:
        return Punt('model_field_added record missing name/annotation')
    if any(f.name == field_name for f in model.fields):
        return Punt(f'field {model.name}.{field_name} already present (idempotent skip)')
    if field_name in model.validator_field_refs:
        return Punt(f'field {field_name!r} is referenced by a validator; needs LLM review')
    if '\n' in annotation:
        return Punt('multi-line annotation; needs LLM review')

    indent = _detect_member_indent(sdk_ir.source_text, model.lineno, model.last_field_end_lineno)
    lines_to_add: list[str] = []
    if doc_comment:
        for doc_line in doc_comment.splitlines():
            lines_to_add.append(f'{indent}#: {doc_line}')
    if default is None:
        line = f'{indent}{field_name}: {annotation}'
    else:
        line = f'{indent}{field_name}: {annotation} = {default}'
    lines_to_add.append(line)

    new_text = _splice_after(sdk_ir.source_text, model.last_field_end_lineno, lines_to_add)
    return PatchResult(new_text, f'added field {model.name}.{field_name}')


def _model_field_removed(record: ChangeRecord, match: Match) -> PatchOutcome:
    """Delete a Pydantic model field.

    Safety: the model and the field must exist, and the field must not be
    referenced by a validator (same reason as :func:`_model_field_added`).

    :param record: A ``model_field_removed`` change record.
    :param match: A :class:`Match` of kind ``'model_field'``.
    :return: :class:`PatchResult` with the field's lines removed (including
        any ``#:`` block above it), or :class:`Punt`.
    """
    sdk_ir = match.sdk_module_ir
    model = sdk_ir.model_by_name(match.sdk_class)
    if model is None:
        return Punt(f'model {match.sdk_class!r} not found in SDK')
    field_name = match.sdk_member
    if field_name is None:
        return Punt('model_field_removed match missing field name')
    target = next((f for f in model.fields if f.name == field_name), None)
    if target is None:
        return Punt(f'field {model.name}.{field_name} not found in SDK')
    if field_name in model.validator_field_refs:
        return Punt(f'field {field_name!r} is referenced by a validator; needs LLM review')

    start_lineno = _doc_comment_start_above(sdk_ir.source_text, target.lineno)
    end_lineno = target.end_lineno
    new_text = _delete_line_range(sdk_ir.source_text, start_lineno, end_lineno)
    return PatchResult(new_text, f'removed field {model.name}.{field_name}')


# ---------------------------------------------------------------------------
# Docstring changes
#
# Method docstrings always punt — SDK methods often have intentionally
# rewritten descriptions and we don't want a deterministic rewrite to
# clobber that. Field/enum-value `#:` comments are handled, but only when
# the SDK's current block matches the *old* stub block byte-for-byte.
# ---------------------------------------------------------------------------


def _docstring_changed(record: ChangeRecord, match: Match) -> PatchOutcome:
    """Dispatch a ``docstring_changed`` record by the kind of target.

    :param record: A ``docstring_changed`` change record. Carries the old/new
        docstring text under either ``docstring`` (methods) or
        ``doc_comment`` (fields/enum values).
    :param match: A :class:`Match` of kind ``'method'``, ``'model_field'`` or
        ``'enum_value'``.
    :return: :class:`PatchResult` or :class:`Punt`.
    """
    old = (record.old or {}).get('docstring')
    new = (record.new or {}).get('docstring')
    old_doc_comment = (record.old or {}).get('doc_comment')
    new_doc_comment = (record.new or {}).get('doc_comment')

    if match.kind == 'method':
        return _method_docstring_changed(match, old, new)
    if match.kind in {'model_field', 'enum_value'}:
        return _doc_comment_changed(match, old_doc_comment, new_doc_comment)
    return Punt(f'docstring_changed for unexpected match kind {match.kind}')


def _method_docstring_changed(match: Match, old_stub_doc: str | None, new_stub_doc: str | None) -> PatchOutcome:
    """Always refuse method docstring rewrites — they belong to the LLM step.

    Even when the SDK docstring matches the old stub byte-for-byte, rewriting
    a method docstring deterministically risks losing intentional SDK-side
    edits we cannot detect by text alone. The LLM step gets a tighter prompt
    that can produce a more faithful rewrite.

    :param match: Resolved SDK method.
    :param old_stub_doc: Docstring as it appeared in the previous stub
        revision.
    :param new_stub_doc: Docstring as it appears in the current stub revision.
    :return: Always a :class:`Punt`.
    """
    sdk_ir = match.sdk_module_ir
    api_class = sdk_ir.api_class_by_name(match.sdk_class)
    if api_class is None or match.sdk_member is None:
        return Punt('SDK API class not located')
    method = next((m for m in api_class.methods if m.name == match.sdk_member), None)
    if method is None:
        return Punt(f'method {match.sdk_member} not in SDK class {match.sdk_class}')
    if method.docstring != old_stub_doc:
        return Punt('SDK docstring has diverged from old stub — needs LLM review')
    return Punt('method docstring rewrite via splicing not yet implemented; routing to LLM')


def _doc_comment_changed(match: Match, old: str | None, new: str | None) -> PatchOutcome:
    """Rewrite the ``#:`` doc-comment block above a field or enum value.

    Safety: refuses if the SDK's current block doesn't match the *old*
    stub block exactly — that would mean someone has hand-edited the SDK
    comment and we'd lose their text.

    :param match: A :class:`Match` of kind ``'model_field'`` or ``'enum_value'``.
    :param old: Old stub doc-comment text (concatenated ``#:`` lines, joined
        with ``\\n``). May be ``None`` if the stub had no doc-comment.
    :param new: New stub doc-comment text, same format. May be ``None`` to
        delete the existing block.
    :return: :class:`PatchResult` with the block rewritten, or :class:`Punt`.
    """
    sdk_ir = match.sdk_module_ir
    # Locate the target field or enum value to anchor the splice. The two
    # branches use distinct variable names so mypy doesn't try to unify
    # FieldIR and EnumValueIR (the only thing we actually need from either
    # is `lineno`).
    target_lineno: int | None = None
    if match.kind == 'model_field':
        model = sdk_ir.model_by_name(match.sdk_class)
        if model is not None and match.sdk_member is not None:
            field_target = next((f for f in model.fields if f.name == match.sdk_member), None)
            if field_target is not None:
                target_lineno = field_target.lineno
    else:
        enum = sdk_ir.enum_by_name(match.sdk_class)
        if enum is not None and match.sdk_member is not None:
            value_target = next((v for v in enum.values if v.name == match.sdk_member), None)
            if value_target is not None:
                target_lineno = value_target.lineno
    if target_lineno is None:
        return Punt('target line not located')

    current = _doc_comment_above_text(sdk_ir.source_text, target_lineno)
    if current == new:
        return Punt('SDK doc-comment already reflects new stub (idempotent skip)')
    if current != old:
        return Punt('SDK doc-comment has diverged from old stub — needs LLM review')

    lines = sdk_ir.source_text.splitlines(keepends=True)
    rm_start = _doc_comment_start_above(sdk_ir.source_text, target_lineno)
    indent = _line_indent(lines[target_lineno - 1])
    insert: list[str] = []
    if new:
        for line in new.splitlines():
            insert.append(f'{indent}#: {line}\n')
    rewritten = lines[: rm_start - 1] + insert + lines[target_lineno - 1 :]
    new_text = ''.join(rewritten)
    return PatchResult(new_text, f'updated doc-comment for {match.sdk_class}.{match.sdk_member}')


# ---------------------------------------------------------------------------
# Splice helpers
#
# All splicing works in source-text space using 1-based line numbers from
# the IR (which match the `ast` convention). We deliberately do not touch
# whitespace within lines — `ruff format` cleans up afterward.
# ---------------------------------------------------------------------------


_DOC_COMMENT_RE = re.compile(r'^\s*#:')


def _splice_after(source: str, after_lineno: int, new_lines: list[str]) -> str:
    """Insert lines into source text immediately after a given line.

    :param source: The full source string.
    :param after_lineno: 1-based line number; ``new_lines`` are inserted
        starting at line ``after_lineno + 1``.
    :param new_lines: Lines to insert; line-endings are appended automatically
        using the EOL detected in ``source``.
    :return: The new source with the lines spliced in.
    """
    lines = source.splitlines(keepends=True)
    insertion: list[str] = []
    eol = _detect_eol(lines)
    for line in new_lines:
        insertion.append(line + eol)
    return ''.join(lines[:after_lineno] + insertion + lines[after_lineno:])


def _delete_line_range(source: str, start_lineno: int, end_lineno: int) -> str:
    """Remove a 1-based inclusive line range from source.

    :param source: The full source string.
    :param start_lineno: First line to remove (1-based, inclusive).
    :param end_lineno: Last line to remove (1-based, inclusive).
    :return: The new source with the range gone.
    """
    lines = source.splitlines(keepends=True)
    return ''.join(lines[: start_lineno - 1] + lines[end_lineno:])


def _doc_comment_start_above(source: str, lineno: int) -> int:
    """Find the topmost line of the contiguous ``#:`` block above ``lineno``.

    :param source: The full source string.
    :param lineno: 1-based line whose preceding ``#:`` block to find.
    :return: 1-based line number of the first ``#:`` line, or ``lineno``
        itself if there is no doc-comment immediately above.
    """
    lines = source.splitlines()
    idx = lineno - 2
    while idx >= 0 and _DOC_COMMENT_RE.match(lines[idx]):
        idx -= 1
    # `idx` is now the 0-based index of the last non-`#:` line above the
    # block (or -1 if the block starts at the file top); +2 converts to the
    # 1-based index of the first `#:` line.
    return idx + 2


def _doc_comment_above_text(source: str, lineno: int) -> str | None:
    """Return the joined text content of the ``#:`` block above ``lineno``.

    Used to verify that the SDK's current doc-comment matches the stub's
    *old* doc-comment before the patcher overwrites it.

    :param source: The full source string.
    :param lineno: 1-based line number.
    :return: The doc-comment lines (without the ``#:`` prefix) joined with
        ``\\n``, or ``None`` if no ``#:`` block sits directly above.
    """
    lines = source.splitlines()
    out: list[str] = []
    idx = lineno - 2
    while idx >= 0:
        m = re.match(r'^\s*#:\s?(.*)$', lines[idx])
        if not m:
            break
        out.append(m.group(1))
        idx -= 1
    if not out:
        return None
    out.reverse()
    return '\n'.join(out)


def _detect_member_indent(source: str, class_lineno: int, anchor_lineno: int) -> str:
    """Derive the indent prefix used by members of the class at ``class_lineno``.

    Inspects the line at ``anchor_lineno`` (typically the last existing
    member of the class) and returns its leading whitespace.

    :param source: The full source string.
    :param class_lineno: 1-based line of the class header (unused at present,
        kept for symmetry with future smarter strategies).
    :param anchor_lineno: 1-based line of an existing member to copy the
        indent from.
    :return: The indent string (spaces or tabs). Falls back to ``'    '`` if
        the anchor line has no leading whitespace.
    """
    lines = source.splitlines()
    if 0 < anchor_lineno <= len(lines):
        return _line_indent(lines[anchor_lineno - 1])
    return '    '


def _line_indent(line: str) -> str:
    """Return the leading whitespace of a source line.

    :param line: A single line (without trailing newline considered).
    :return: The leading whitespace prefix, possibly empty.
    """
    m = re.match(r'^(\s*)', line)
    return m.group(1) if m else ''


def _detect_eol(lines: list[str]) -> str:
    """Detect the line-ending convention used by a source.

    :param lines: List of source lines as produced by
        :func:`str.splitlines` with ``keepends=True``.
    :return: ``'\\r\\n'`` if any line ends with CRLF, otherwise ``'\\n'``.
    """
    for ln in lines:
        if ln.endswith('\r\n'):
            return '\r\n'
        if ln.endswith('\n'):
            return '\n'
    return '\n'


# Names intended for external use. Exposed via ``__all__`` so the
# dispatcher can ``from .patcher import Punt`` without IDE warnings.
__all__ = ['apply', 'Punt', 'PatchResult', 'PatchOutcome']

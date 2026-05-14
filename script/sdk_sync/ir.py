"""
AST-based IR (intermediate representation) extractor for stub and SDK modules.

The IR is the canonical shape used by :mod:`script.sdk_sync.differ` and
:mod:`script.sdk_sync.matcher`. It captures everything we need to detect drift
between auto-generated OpenAPI stubs and the hand-maintained SDK, and to locate
the SDK counterpart of every change:

- Pydantic models with their fields, types (as source text plus a canonical
  whitespace-normalized form for equality comparison), ``#:`` doc-comments,
  and the line at which new fields can be safely inserted.
- Enums with their values and a similar insertion anchor.
- The single API class per module with its ``base=`` URL prefix and methods
  keyed by ``(verb, canonical ep_template)``.

The extractor is a pure function over source text — it never imports the module
under analysis. This means it can be run against ``git show HEAD:<path>``
output exactly as easily as against the working tree, without writing temp
files.

Python's :mod:`ast` discards comments, so the ``#:`` Pydantic field doc-comments
are recovered by scanning the source-text lines immediately above each
``AnnAssign`` node. Line numbers are preserved on every IR object so the
patcher in :mod:`script.sdk_sync.patcher` can splice text without re-parsing.
"""

from __future__ import annotations

import ast
import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

# HTTP verbs we look for in method bodies. The pagination helper
# `self.session.follow_pagination(...)` is recognised separately and treated as GET.
_HTTP_VERBS: frozenset[str] = frozenset({'get', 'post', 'put', 'delete', 'patch'})

# Matches a single Pydantic-style doc-comment line, capturing the text after the
# `#:` prefix. Used both during IR extraction and by the patcher when it
# rewrites doc-comment blocks.
_DOC_COMMENT_RE = re.compile(r'^\s*#:\s?(.*)$')


# ---------------------------------------------------------------------------
# IR dataclasses
#
# Every IR node carries `lineno`/`end_lineno` so the patcher can perform
# line-range text splicing without re-parsing the source. The classes are
# `frozen=True` so they're hashable and safe to cache.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FieldIR:
    """A single Pydantic model field.

    :param name: Python attribute name.
    :param annotation: Source text of the type annotation (for example
        ``"Optional[list[Foo]]"``).
    :param canonical_annotation: Whitespace-stripped annotation used as the
        equality key when diffing types.
    :param default: Source text of the RHS (``"None"``, ``"Field(None, ...)"``),
        or ``None`` if the field has no default.
    :param doc_comment: Concatenated content of the ``#:`` lines immediately
        above this field, joined with ``\\n``; ``None`` if no doc-comment.
    :param lineno: 1-based line where the field's ``AnnAssign`` begins.
    :param end_lineno: 1-based line where the field's ``AnnAssign`` ends
        (same as ``lineno`` for single-line annotations).
    """

    name: str
    annotation: str
    canonical_annotation: str
    default: str | None
    doc_comment: str | None
    lineno: int
    end_lineno: int


@dataclass(frozen=True)
class EnumValueIR:
    """One value declared inside an enum class.

    :param name: Python identifier of the member.
    :param value: Source text of the right-hand side (for example
        ``"'pending'"``).
    :param doc_comment: ``#:`` lines above this value joined with ``\\n``, or
        ``None`` if absent.
    :param lineno: 1-based line of the assignment.
    :param end_lineno: 1-based last line of the assignment.
    """

    name: str
    value: str
    doc_comment: str | None
    lineno: int
    end_lineno: int


@dataclass(frozen=True)
class ModelIR:
    """A Pydantic model class.

    :param name: Class name.
    :param bases: Source text of each base class expression.
    :param fields: Tuple of :class:`FieldIR` in declaration order.
    :param has_custom_validators: ``True`` if the class declares any
        ``@field_validator`` or ``@model_validator`` decorated method.
    :param validator_field_refs: Names referenced as positional string arguments
        to a validator decorator (e.g. ``@field_validator('mac')`` yields
        ``{'mac'}``). The patcher consults this set to refuse mutations that
        would invalidate a validator.
    :param last_field_end_lineno: 1-based line just below the last field; the
        anchor used when appending a new field. ``None`` if the model declared
        no fields.
    :param lineno: 1-based line where ``class Foo(...):`` starts.
    :param end_lineno: 1-based line where the class body ends.
    """

    name: str
    bases: tuple[str, ...]
    fields: tuple[FieldIR, ...]
    has_custom_validators: bool
    validator_field_refs: frozenset[str]
    last_field_end_lineno: int | None
    lineno: int
    end_lineno: int


@dataclass(frozen=True)
class EnumIR:
    """An enum class.

    :param name: Class name.
    :param values: Tuple of :class:`EnumValueIR` in declaration order.
    :param last_value_end_lineno: 1-based line of the last value declaration;
        the anchor used when appending a new value. ``None`` if the enum has
        no members.
    :param lineno: 1-based first line of the class.
    :param end_lineno: 1-based last line of the class body.
    """

    name: str
    values: tuple[EnumValueIR, ...]
    last_value_end_lineno: int | None
    lineno: int
    end_lineno: int


@dataclass(frozen=True)
class ParamIR:
    """One parameter of an API method.

    :param name: Parameter name.
    :param annotation: Source text of the annotation, or ``None`` if untyped.
    :param default: Source text of the default value, or ``None`` if required.
    :param kind: ``'positional'`` for regular positional/keyword parameters,
        ``'keyword'`` for keyword-only, ``'vararg'`` for ``*args``, ``'kwarg'``
        for ``**kwargs``.
    """

    name: str
    annotation: str | None
    default: str | None
    kind: Literal['positional', 'keyword', 'vararg', 'kwarg']


@dataclass(frozen=True)
class MethodIR:
    """A method on an API class.

    The ``(verb, ep_template)`` pair is the join key used by the matcher: the
    stub generator and the SDK both build their endpoint URLs the same way, so
    identical operations produce identical canonical templates regardless of
    how the methods are named.

    :param name: Python method name.
    :param params: Tuple of :class:`ParamIR` in signature order (``self`` is
        excluded).
    :param returns: Source text of the return annotation, or ``None``.
    :param docstring: Raw docstring text (Sphinx-style), or ``None``.
    :param verb: HTTP verb in lowercase (``'get'``, ``'post'``, ...). ``None``
        if no HTTP call was detected in the method body — for example, a
        helper method.
    :param ep_template: Canonical URL produced by joining the class ``base=``
        with the literal/f-string passed to ``self.ep(...)`` and resolving
        f-string interpolations to ``{name}`` placeholders.
    :param raw_ep_arg: Source text of the first argument to ``self.ep(...)``;
        retained for debugging and reporting.
    :param lineno: 1-based first line of the method.
    :param end_lineno: 1-based last line of the method body.
    """

    name: str
    params: tuple[ParamIR, ...]
    returns: str | None
    docstring: str | None
    verb: str | None
    ep_template: str | None
    raw_ep_arg: str | None
    lineno: int
    end_lineno: int


@dataclass(frozen=True)
class ApiClassIR:
    """The single ``ApiChild``-derived class within a stub or SDK module.

    :param name: Class name.
    :param base: Value of the ``base=`` keyword argument from the class
        signature; an empty string if the class declares no base.
    :param methods: Tuple of :class:`MethodIR` for each non-underscore,
        non-validator method in the class body.
    :param lineno: 1-based first line of the class definition.
    :param end_lineno: 1-based last line of the class body.
    """

    name: str
    base: str
    methods: tuple[MethodIR, ...]
    lineno: int
    end_lineno: int


@dataclass(frozen=True)
class ModuleIR:
    """Top-level IR for a single Python module.

    A stub or SDK module is expected to contain at most one API class; any
    number of Pydantic models and enums may sit alongside it at module scope.

    :param path: Source path the IR was extracted from (informational; may be
        a placeholder like ``'<string>'`` when extracting from text).
    :param models: All Pydantic models found at module scope.
    :param enums: All enum classes found at module scope.
    :param api_class: The API class if present, otherwise ``None``.
    :param source_sha: SHA-1 of the source text; used as a cheap identity
        check (e.g. to detect that the file has not changed since the IR was
        extracted).
    :param source_text: The full source text, retained so the patcher can
        splice without re-reading from disk. Excluded from :func:`repr` to
        keep dataclass diagnostics readable.
    """

    path: str
    models: tuple[ModelIR, ...]
    enums: tuple[EnumIR, ...]
    api_class: ApiClassIR | None
    source_sha: str
    source_text: str = field(repr=False)

    def model_by_name(self, name: str) -> ModelIR | None:
        """Find a model by class name.

        :param name: The model class name to look up.
        :return: The matching :class:`ModelIR`, or ``None`` if no model with
            that name was extracted.
        """
        for m in self.models:
            if m.name == name:
                return m
        return None

    def enum_by_name(self, name: str) -> EnumIR | None:
        """Find an enum by class name.

        :param name: The enum class name to look up.
        :return: The matching :class:`EnumIR`, or ``None``.
        """
        for e in self.enums:
            if e.name == name:
                return e
        return None

    def method_by_key(self, verb: str, ep_template: str) -> MethodIR | None:
        """Look up the API method matching a canonical endpoint key.

        :param verb: HTTP verb in lowercase.
        :param ep_template: Canonical endpoint template as produced by
            :func:`_canonical_ep_template`.
        :return: The matching :class:`MethodIR`, or ``None`` if the module has
            no API class or no method with that key.
        """
        if self.api_class is None:
            return None
        for m in self.api_class.methods:
            if m.verb == verb and m.ep_template == ep_template:
                return m
        return None


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------


def extract(path: str | Path) -> ModuleIR:
    """Read a Python source file from disk and extract its IR.

    :param path: Path to the source file. May be a string or :class:`pathlib.Path`.
    :return: A fully-populated :class:`ModuleIR`.
    :raises SyntaxError: If the file cannot be parsed.
    """
    p = Path(path)
    return extract_from_text(p.read_text(), str(p))


def extract_from_text(source: str, path: str = '<string>') -> ModuleIR:
    """Parse a source string and extract its IR.

    This is the workhorse: ``extract()`` is a thin convenience wrapper. The
    caller is expected to pass any text that is *valid* Python — typically the
    contents of a stub or SDK file, or the output of ``git show HEAD:<path>``.

    :param source: Python source text.
    :param path: Informational path string (defaults to ``'<string>'``).
    :return: A :class:`ModuleIR` with models, enums, optional API class, the
        SHA-1 of the source, and the source text retained for the patcher.
    :raises SyntaxError: If ``source`` does not parse.
    """
    tree = ast.parse(source)
    source_lines = source.splitlines(keepends=False)
    models: list[ModelIR] = []
    enums: list[EnumIR] = []
    api_class: ApiClassIR | None = None
    # Walk only top-level statements: stubs and SDK modules never nest API
    # classes or Pydantic models. Anything that isn't a class def is ignored.
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        kind = _classify_class(node)
        if kind == 'enum':
            enums.append(_extract_enum(node, source_lines))
        elif kind == 'model':
            models.append(_extract_model(node, source_lines))
        elif kind == 'api':
            api_class = _extract_api_class(node)
    return ModuleIR(
        path=path,
        models=tuple(models),
        enums=tuple(enums),
        api_class=api_class,
        source_sha=hashlib.sha1(source.encode('utf-8')).hexdigest(),
        source_text=source,
    )


# ---------------------------------------------------------------------------
# Class classification
# ---------------------------------------------------------------------------


def _base_names(node: ast.ClassDef) -> tuple[str, ...]:
    """Return the source text of each base class expression.

    :param node: A class definition node.
    :return: Tuple of base-class source strings; entries that fail to unparse
        are reported as ``'?'`` rather than raising.
    """
    names: list[str] = []
    for base in node.bases:
        try:
            names.append(ast.unparse(base))
        except Exception:
            names.append('?')
    return tuple(names)


def _classify_class(node: ast.ClassDef) -> Literal['enum', 'model', 'api', 'other']:
    """Classify a class definition into one of the four IR roles.

    The check is purely textual on the base-class expressions; we never import
    the module so we cannot resolve subclass relationships. This is good enough
    because the stub generator and SDK consistently spell the bases as
    ``Enum``/``str, Enum``, ``ApiModel`` and ``ApiChild``.

    :param node: A class definition node.
    :return: ``'enum'`` for ``SafeEnum``/``Enum`` subclasses, ``'model'`` for
        :class:`ApiModel` subclasses, ``'api'`` for :class:`ApiChild`
        subclasses (including those carrying a ``base=`` kwarg), otherwise
        ``'other'``.
    """
    bases = _base_names(node)
    if any('Enum' in b for b in bases):
        return 'enum'
    if any(b == 'ApiModel' or b.endswith('.ApiModel') for b in bases):
        return 'model'
    if any(b == 'ApiChild' or b.endswith('.ApiChild') or b.startswith('ApiChild,') for b in bases):
        return 'api'
    for base in node.bases:
        if isinstance(base, ast.Name) and base.id == 'ApiChild':
            return 'api'
    # Fallback heuristic: any class with a `base=` kwarg is treated as an
    # API class, since that pattern is unique to `ApiChild` in this codebase.
    if node.keywords and any(kw.arg == 'base' for kw in node.keywords):
        return 'api'
    return 'other'


# ---------------------------------------------------------------------------
# Doc-comment recovery
# ---------------------------------------------------------------------------


def _doc_comment_above(lineno: int, source_lines: list[str]) -> str | None:
    """Return concatenated ``#:`` doc-comment lines immediately above a line.

    Python's :mod:`ast` discards comments, so we recover them by scanning the
    raw source lines above the node. The scan stops at the first line that is
    not a ``#:`` comment (e.g. a blank line, or a different statement).

    :param lineno: 1-based line number whose preceding doc-comment block should
        be returned. Matches the ``ast`` numbering convention.
    :param source_lines: The source split into lines (no trailing newlines).
    :return: All ``#:`` text joined with ``\\n``, or ``None`` if the line
        immediately above is not a ``#:`` line.
    """
    parts: list[str] = []
    idx = lineno - 2  # zero-based index of the line above `lineno`
    while idx >= 0:
        match = _DOC_COMMENT_RE.match(source_lines[idx])
        if not match:
            break
        parts.append(match.group(1))
        idx -= 1
    if not parts:
        return None
    parts.reverse()
    return '\n'.join(parts)


def _annotation_source(node: ast.AST | None) -> str | None:
    """Return the source text of an annotation/expression node.

    :param node: AST expression node, or ``None``.
    :return: Result of :func:`ast.unparse`, or ``None`` if the input was
        ``None`` or unparsing failed.
    """
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None


def _canonical_annotation(text: str | None) -> str:
    """Whitespace-normalize an annotation for equality comparison.

    Two annotations that differ only in whitespace (``"list[Foo]"`` vs
    ``"list[ Foo ]"``) should not be reported as a ``type_changed`` event by
    the differ. Stripping all whitespace is a safe normalization for the
    annotation grammar used in stubs and the SDK.

    :param text: Annotation source text, or ``None``.
    :return: The same text with every run of whitespace removed. ``None``
        becomes the empty string.
    """
    if text is None:
        return ''
    return re.sub(r'\s+', '', text)


# ---------------------------------------------------------------------------
# Enum / model body walkers
# ---------------------------------------------------------------------------


def _extract_enum(node: ast.ClassDef, source_lines: list[str]) -> EnumIR:
    """Extract an :class:`EnumIR` from an enum class definition.

    :param node: The class definition node previously classified as ``'enum'``.
    :param source_lines: The module's source split into lines, used to recover
        ``#:`` doc-comments above each enum value.
    :return: A populated :class:`EnumIR`.
    """
    values: list[EnumValueIR] = []
    last_end: int | None = None
    for child in node.body:
        if isinstance(child, ast.Assign) and len(child.targets) == 1 and isinstance(child.targets[0], ast.Name):
            name = child.targets[0].id
            try:
                rhs = ast.unparse(child.value)
            except Exception:
                rhs = '?'
            doc = _doc_comment_above(child.lineno, source_lines)
            ln = child.lineno
            end_ln = child.end_lineno or ln
            values.append(
                EnumValueIR(
                    name=name,
                    value=rhs,
                    doc_comment=doc,
                    lineno=ln,
                    end_lineno=end_ln,
                )
            )
            last_end = end_ln
    return EnumIR(
        name=node.name,
        values=tuple(values),
        last_value_end_lineno=last_end,
        lineno=node.lineno,
        end_lineno=node.end_lineno or node.lineno,
    )


def _extract_model(node: ast.ClassDef, source_lines: list[str]) -> ModelIR:
    """Extract a :class:`ModelIR` from a Pydantic model class definition.

    Walks the class body and collects:

    - ``AnnAssign`` nodes as :class:`FieldIR` entries.
    - ``FunctionDef`` nodes carrying a validator decorator, recording both the
      presence of validators and any field names referenced as positional
      string args to those decorators (so the patcher can refuse to mutate
      validator-referenced fields).

    :param node: The class definition node previously classified as
        ``'model'``.
    :param source_lines: Module source split into lines, used by
        :func:`_doc_comment_above` to capture ``#:`` doc-comments.
    :return: A populated :class:`ModelIR`.
    """
    fields_out: list[FieldIR] = []
    last_field_end: int | None = None
    has_validators = False
    validator_refs: set[str] = set()
    for child in node.body:
        if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
            ann_src = _annotation_source(child.annotation) or ''
            default_src = _annotation_source(child.value)
            doc = _doc_comment_above(child.lineno, source_lines)
            fields_out.append(
                FieldIR(
                    name=child.target.id,
                    annotation=ann_src,
                    canonical_annotation=_canonical_annotation(ann_src),
                    default=default_src,
                    doc_comment=doc,
                    lineno=child.lineno,
                    end_lineno=child.end_lineno or child.lineno,
                )
            )
            last_field_end = child.end_lineno or child.lineno
        elif isinstance(child, ast.FunctionDef):
            if _has_validator_decorator(child):
                has_validators = True
                validator_refs.update(_find_field_string_refs(child))
    return ModelIR(
        name=node.name,
        bases=_base_names(node),
        fields=tuple(fields_out),
        has_custom_validators=has_validators,
        validator_field_refs=frozenset(validator_refs),
        last_field_end_lineno=last_field_end,
        lineno=node.lineno,
        end_lineno=node.end_lineno or node.lineno,
    )


def _has_validator_decorator(func: ast.FunctionDef) -> bool:
    """Return ``True`` if ``func`` is decorated with a Pydantic validator.

    Recognises both call form (``@field_validator('mac')``) and bare-name form
    (``@field_validator``), and both ``field_validator`` and ``model_validator``.

    :param func: A function definition node taken from a class body.
    :return: ``True`` if any decorator is a Pydantic validator.
    """
    for dec in func.decorator_list:
        if isinstance(dec, ast.Call):
            fn = dec.func
            if isinstance(fn, ast.Name) and fn.id in {'field_validator', 'model_validator'}:
                return True
        if isinstance(dec, ast.Name) and dec.id in {'field_validator', 'model_validator'}:
            return True
    return False


def _find_field_string_refs(func: ast.FunctionDef) -> set[str]:
    """Collect string-literal arguments passed to validator decorators.

    The patcher uses this set to refuse mutations on a field that a validator
    explicitly names — adding such a field without updating its validator,
    or removing a field a validator depends on, would silently break the SDK.

    Examples:

    - ``@field_validator('mac')`` → ``{'mac'}``
    - ``@field_validator('a', 'b')`` → ``{'a', 'b'}``
    - ``@model_validator(mode='before')`` → ``set()`` (no positional strings)

    :param func: A function definition node carrying validator decorators.
    :return: The set of field names referenced positionally.
    """
    out: set[str] = set()
    for dec in func.decorator_list:
        if isinstance(dec, ast.Call):
            for arg in dec.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    out.add(arg.value)
    return out


# ---------------------------------------------------------------------------
# API class / method walkers
# ---------------------------------------------------------------------------


def _extract_api_class(node: ast.ClassDef) -> ApiClassIR:
    """Extract an :class:`ApiClassIR` from an ``ApiChild``-derived class.

    Skips dunder methods, underscore-prefixed helpers, and the ``ep`` helper
    itself (which is what we're trying to *resolve*, not catalog). Methods
    carrying validator decorators are also skipped — those belong to models
    and never to ApiChild classes, but the guard is cheap and safe.

    :param node: The class definition node previously classified as ``'api'``.
    :return: A populated :class:`ApiClassIR`.
    """
    base = ''
    for kw in node.keywords:
        if kw.arg == 'base' and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
            base = kw.value.value
            break
    methods: list[MethodIR] = []
    for child in node.body:
        if isinstance(child, ast.FunctionDef) and not _has_validator_decorator(child):
            if child.name.startswith('_') or child.name == 'ep':
                continue
            methods.append(_extract_method(child, base))
    return ApiClassIR(
        name=node.name,
        base=base,
        methods=tuple(methods),
        lineno=node.lineno,
        end_lineno=node.end_lineno or node.lineno,
    )


def _extract_method(func: ast.FunctionDef, class_base: str) -> MethodIR:
    """Extract a :class:`MethodIR` from a function definition.

    Captures the signature (positional, keyword-only, ``*args``, ``**kwargs``),
    the return annotation, the docstring, and the canonical endpoint key
    derived from inspecting the method body.

    :param func: The method's ``FunctionDef`` node.
    :param class_base: The enclosing API class's ``base=`` value; combined
        with the body-resolved suffix to form the canonical ``ep_template``.
    :return: A populated :class:`MethodIR`. ``verb`` and ``ep_template`` may
        be ``None`` if the body does not contain a recognised HTTP call.
    """
    args = func.args
    params_out: list[ParamIR] = []
    # `args.defaults` covers only the trailing positional defaults — compute
    # the offset so we can pair each positional arg with its default (if any).
    pos_defaults_offset = len(args.args) - len(args.defaults)
    for i, a in enumerate(args.args):
        if a.arg == 'self':
            continue
        default = None
        d_idx = i - pos_defaults_offset
        if d_idx >= 0:
            default = _annotation_source(args.defaults[d_idx])
        params_out.append(
            ParamIR(
                name=a.arg,
                annotation=_annotation_source(a.annotation),
                default=default,
                kind='positional',
            )
        )
    for i, a in enumerate(args.kwonlyargs):
        # kw_defaults uses None to represent "no default" (unlike defaults).
        default_node = args.kw_defaults[i] if i < len(args.kw_defaults) else None
        params_out.append(
            ParamIR(
                name=a.arg,
                annotation=_annotation_source(a.annotation),
                default=_annotation_source(default_node) if default_node is not None else None,
                kind='keyword',
            )
        )
    if args.vararg is not None:
        params_out.append(
            ParamIR(
                name=args.vararg.arg,
                annotation=_annotation_source(args.vararg.annotation),
                default=None,
                kind='vararg',
            )
        )
    if args.kwarg is not None:
        params_out.append(
            ParamIR(
                name=args.kwarg.arg,
                annotation=_annotation_source(args.kwarg.annotation),
                default=None,
                kind='kwarg',
            )
        )
    verb, raw_ep_arg = _extract_verb_and_ep(func)
    ep_template = _canonical_ep_template(class_base, raw_ep_arg)
    return MethodIR(
        name=func.name,
        params=tuple(params_out),
        returns=_annotation_source(func.returns),
        docstring=ast.get_docstring(func, clean=False),
        verb=verb,
        ep_template=ep_template,
        raw_ep_arg=raw_ep_arg,
        lineno=func.lineno,
        end_lineno=func.end_lineno or func.lineno,
    )


def _extract_verb_and_ep(func: ast.FunctionDef) -> tuple[str | None, str | None]:
    """Walk a method body to extract the HTTP verb and the ``self.ep(...)`` argument.

    The function recognises three call patterns common to stubs and the SDK:

    - ``url = self.ep(...)`` / ``url = self._endpoint(...)`` — captures the
      first argument as the URL suffix.
    - ``super().<verb>(url, ...)`` / ``self.<verb>(url, ...)`` /
      ``self.session.<verb>(...)`` — captures the verb.
    - ``self.session.follow_pagination(...)`` — treated as ``GET``.
    - ``self.rest_get(...)`` etc. — verb taken from the prefix.

    :param func: A method's ``FunctionDef`` node.
    :return: A ``(verb, raw_ep_arg)`` tuple. Either element may be ``None``
        when no matching call is found; ``raw_ep_arg`` is the empty string
        when ``self.ep()`` is called with no arguments.
    """
    ep_arg: str | None = None
    verb: str | None = None
    for stmt in ast.walk(func):
        if isinstance(stmt, ast.Call):
            fn = stmt.func
            # `url = self.ep(...)` / `url = self._endpoint(...)`
            if isinstance(fn, ast.Attribute) and fn.attr in {'ep', '_endpoint'}:
                if isinstance(fn.value, ast.Name) and fn.value.id == 'self':
                    if stmt.args:
                        try:
                            ep_arg = ast.unparse(stmt.args[0])
                        except Exception:
                            ep_arg = '?'
                    else:
                        ep_arg = ''
            # `super().<verb>(url, ...)` / `self.<verb>(url, ...)` /
            # `self.session.follow_pagination(...)` / `self.rest_<verb>(...)`
            if verb is None and isinstance(fn, ast.Attribute):
                if fn.attr in _HTTP_VERBS:
                    if _is_self_or_super_call(fn.value):
                        verb = fn.attr
                elif fn.attr == 'follow_pagination':
                    verb = 'get'
                elif fn.attr in {'rest_get', 'rest_post', 'rest_put', 'rest_delete', 'rest_patch'}:
                    verb = fn.attr.removeprefix('rest_')
    return verb, ep_arg


def _is_self_or_super_call(node: ast.AST) -> bool:
    """Decide whether a call receiver is ``self``, ``super()`` or ``self.<attr>``.

    Used to reject confounding HTTP-verb method calls that aren't actually on
    the API object (for example, a ``foo.get(key)`` on a dict).

    :param node: The ``Call.func.value`` portion of an attribute call.
    :return: ``True`` for ``self``, ``super()`` and ``self.<anything>`` (the
        last covers ``self.session.get`` etc.).
    """
    if isinstance(node, ast.Name) and node.id == 'self':
        return True
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'super':
        return True
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == 'self':
        return True
    return False


# ---------------------------------------------------------------------------
# Endpoint canonicalization
#
# The matcher's join key for methods is `(verb, ep_template)`. Stubs and SDK
# code spell their URLs slightly differently — the stub's f-string parameter
# names will not always match the SDK's — so both sides go through the same
# canonicalization, which replaces every interpolated value with `{name}`.
# ---------------------------------------------------------------------------


def _canonical_ep_template(base: str, raw_ep_arg: str | None) -> str | None:
    """Combine the class ``base=`` with the ``self.ep(...)`` argument.

    The result substitutes f-string interpolations with ``{name}`` placeholders
    so stub and SDK forms compare equal even when interpolated variables are
    named differently.

    Examples:

    - ``base='devices'``, ``ep_arg=''`` → ``'devices'``
    - ``base='devices'``, ``ep_arg="'activationCode'"`` → ``'devices/activationCode'``
    - ``base='devices'``, ``ep_arg="f'{device_id}'"`` → ``'devices/{device_id}'``
    - ``base='hotdesk/sessions'``, ``ep_arg=None`` → ``'hotdesk/sessions'``

    :param base: Value of the API class's ``base=`` kwarg.
    :param raw_ep_arg: Source text of the first ``self.ep(...)`` arg, the empty
        string for ``self.ep()`` with no args, or ``None`` if the method body
        never called ``self.ep(...)``.
    :return: Canonical URL string, or ``None`` when neither a base nor an
        endpoint argument is available.
    """
    if raw_ep_arg is None:
        # No ep() call discovered; fall back to base alone (rare in stubs but
        # happens in some SDK helper methods).
        return base or None
    suffix = _resolve_ep_arg(raw_ep_arg)
    if suffix == '':
        return base
    if not base:
        return suffix
    return f'{base}/{suffix}'.replace('//', '/')


def _resolve_ep_arg(raw_ep_arg: str) -> str:
    """Parse the source text of the first ``self.ep(...)`` argument.

    :param raw_ep_arg: Source text of the argument, or the empty string for
        ``self.ep()`` with no args.
    :return: A canonical URL suffix string with f-string holes replaced by
        ``{name}`` placeholders. Returns the input verbatim if it does not
        parse as a Python expression.
    """
    if raw_ep_arg == '':
        return ''
    try:
        node = ast.parse(raw_ep_arg, mode='eval').body
    except SyntaxError:
        return raw_ep_arg
    return _resolve_node(node)


def _resolve_node(node: ast.AST) -> str:
    """Reduce a small subset of AST expression nodes to a URL string.

    Recognises:

    - String constants → the literal value.
    - JoinedStr (f-strings) → each constant chunk inlined, each ``{expr}``
      replaced with ``{name}`` produced by :func:`_placeholder_name`.
    - Name nodes (a bare variable) → ``{name}``.
    - ``Add`` BinOps → concatenation of the resolved operands.
    - Call nodes → recurse into the first positional argument; this handles
      wrappers such as ``urllib.parse.quote(person_id)`` or ``enum_str(x)``.

    Anything else falls back to :func:`ast.unparse`, and unparseable nodes
    return ``'?'``.

    :param node: An AST expression.
    :return: The canonical URL string for that expression.
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for v in node.values:
            if isinstance(v, ast.Constant):
                parts.append(str(v.value))
            elif isinstance(v, ast.FormattedValue):
                parts.append('{' + _placeholder_name(v.value) + '}')
        return ''.join(parts)
    if isinstance(node, ast.Name):
        return '{' + node.id + '}'
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _resolve_node(node.left) + _resolve_node(node.right)
    if isinstance(node, ast.Call):
        # Unwrap call wrappers: urllib.parse.quote(person_id), enum_str(x), etc.
        if node.args:
            return _resolve_node(node.args[0])
        return '?'
    try:
        return ast.unparse(node)
    except Exception:
        return '?'


def _placeholder_name(node: ast.AST) -> str:
    """Derive the placeholder name for an f-string interpolation expression.

    For a simple ``{device_id}`` we return ``"device_id"``. For attribute
    accesses (``{self.device_id}``) we use the rightmost attribute. For
    wrapping calls (``{enum_str(kind)}``) we recurse to the inner expression.

    :param node: An AST expression that appeared inside an f-string ``{}``.
    :return: A short identifier used as the placeholder text.
    """
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Call) and node.args:
        return _placeholder_name(node.args[0])
    try:
        return ast.unparse(node)
    except Exception:
        return '?'

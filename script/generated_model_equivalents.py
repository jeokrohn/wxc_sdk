#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.14"
# ///
"""
Find SDK models equivalent to models from an auto-generated OpenAPI source.

Equivalence is intentionally narrow: two models are equivalent when their
Python field-name sets are identical. Type annotations, aliases, defaults,
validators, enum definitions, and comments are ignored.

When no exact equivalent exists, the analyzer also reports SDK models whose
field-name set is a strict superset of the generated model and whose shared
primitive/container field annotations are compatible.
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from argparse import Namespace
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from script.sdk_sync.ir import ModuleIR, extract, extract_from_text

# Source scanning intentionally avoids importing SDK modules. Generated files
# and partially edited SDK modules may not be import-safe while this tool runs.
SDK_SKIP_FILES = {'all_types.py', 'as_api.py', 'as_mpe.py', 'as_rest.py'}
MODEL_ROOT_NAMES = {'ApiModel', 'ApiModelWithErrors'}
BUILTIN_TYPE_NAMES = {
    'Any',
    'bool',
    'bytes',
    'datetime',
    'dict',
    'float',
    'int',
    'list',
    'None',
    'set',
    'str',
    'tuple',
}


@dataclass(frozen=True)
class SourceClassShape:
    """AST-level class description before ApiModel inheritance is resolved."""

    name: str
    bases: tuple[str, ...]
    local_fields: tuple[str, ...]
    local_field_annotations: dict[str, str]
    path: Path
    module: str
    lineno: int


@dataclass(frozen=True)
class SourceModelInfo:
    """Resolved ApiModel-like class with inherited fields merged."""

    name: str
    field_names: frozenset[str]
    field_annotations: dict[str, str]
    path: Path
    module: str
    lineno: int

    @property
    def field_count(self) -> int:
        """Return the number of effective Python model fields.

        :return: Count of merged field names.
        :rtype: int
        """
        return len(self.field_names)

    @property
    def import_path(self) -> str:
        """Return the importable module and class reference.

        :return: Dotted import path for the model class.
        :rtype: str
        """
        return f'{self.module}.{self.name}' if self.module else self.name


@dataclass(frozen=True)
class GeneratedSupersetCandidate:
    """SDK model whose fields strictly contain a generated model's fields."""

    model: SourceModelInfo
    extra_fields: frozenset[str]


@dataclass(frozen=True)
class GeneratedModelMatch:
    """Comparison result for one generated model."""

    generated: SourceModelInfo
    candidates: tuple[SourceModelInfo, ...]
    superset_candidates: tuple[GeneratedSupersetCandidate, ...] = ()

    @property
    def status(self) -> str:
        """Return the match category for the generated model.

        :return: ``matched``, ``superset``, or ``no_match``.
        :rtype: str
        """
        if self.candidates:
            return 'matched'
        if self.superset_candidates:
            return 'superset'
        return 'no_match'


@dataclass(frozen=True)
class GeneratedAnalysisResult:
    """Full generated-file analysis result plus summary metadata."""

    generated_file: Path
    sdk_root: Path
    base_ref: str
    added_only: bool
    generated_total: int
    sdk_models_total: int
    sdk_files_scanned: int
    matches: tuple[GeneratedModelMatch, ...]

    @property
    def matched_total(self) -> int:
        """Return how many generated models have exact SDK matches.

        :return: Exact-match model count.
        :rtype: int
        """
        return sum(1 for match in self.matches if match.candidates)

    @property
    def superset_total(self) -> int:
        """Return how many generated models only have superset matches.

        :return: Superset-only model count.
        :rtype: int
        """
        return sum(1 for match in self.matches if not match.candidates and match.superset_candidates)

    @property
    def unmatched_total(self) -> int:
        """Return how many generated models have no SDK candidate.

        :return: Unmatched model count.
        :rtype: int
        """
        return sum(1 for match in self.matches if match.status == 'no_match')


def _base_names(node: ast.ClassDef) -> tuple[str, ...]:
    """Return source strings for class bases.

    :param node: Class AST node to inspect.
    :type node: ast.ClassDef
    :return: Base-class expressions as Python source snippets.
    :rtype: tuple[str, ...]
    """
    out: list[str] = []
    for base in node.bases:
        try:
            out.append(ast.unparse(base))
        except Exception:
            out.append('?')
    return tuple(out)


def _final_name(base: str) -> str:
    """Return the unqualified name from a base-class expression.

    :param base: Base-class expression such as ``module.Base``.
    :type base: str
    :return: Final dotted-name component.
    :rtype: str
    """
    return base.rsplit('.', maxsplit=1)[-1]


def _class_shapes_from_ir(module_ir: ModuleIR) -> list[SourceClassShape]:
    """Extract class shapes from a parsed module.

    :param module_ir: Intermediate representation produced by ``sdk_sync.ir``.
    :type module_ir: ModuleIR
    :return: Class shapes with local fields, annotations, bases, and location.
    :rtype: list[SourceClassShape]
    """
    source = module_ir.source_text
    tree = ast.parse(source)
    path = Path(module_ir.path)
    module = module_name_for_path(path)
    shapes: list[SourceClassShape] = []

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        fields: list[str] = []
        field_annotations: dict[str, str] = {}
        for child in node.body:
            if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                field_name = child.target.id
                fields.append(field_name)
                try:
                    field_annotations[field_name] = ast.unparse(child.annotation)
                except Exception:
                    field_annotations[field_name] = ''
        shapes.append(
            SourceClassShape(
                name=node.name,
                bases=_base_names(node),
                local_fields=tuple(fields),
                local_field_annotations=field_annotations,
                path=path,
                module=module,
                lineno=node.lineno,
            )
        )
    return shapes


def module_name_for_path(path: Path, package_root: Path | None = None) -> str:
    """Convert a Python source path to a dotted module path.

    :param path: Python file path.
    :type path: Path
    :param package_root: Directory used as the module path root.
    :type package_root: Path | None
    :return: Dotted import module name.
    :rtype: str
    """
    resolved = path.resolve()
    if package_root is None:
        package_root = REPO_ROOT
    try:
        rel = resolved.relative_to(package_root.resolve())
    except ValueError:
        try:
            rel = resolved.relative_to(package_root.resolve().parent)
        except ValueError:
            rel = path

    parts = list(rel.with_suffix('').parts)
    if parts and parts[-1] == '__init__':
        parts = parts[:-1]
    return '.'.join(parts)


def collect_models_from_module_irs(
    module_irs: list[ModuleIR],
    package_root: Path | None = None,
) -> list[SourceModelInfo]:
    """Collect resolved ApiModel-like classes from module IRs.

    :param module_irs: Module representations to inspect.
    :type module_irs: list[ModuleIR]
    :param package_root: Optional package root for import path rendering.
    :type package_root: Path | None
    :return: Resolved source models with inherited fields merged.
    :rtype: list[SourceModelInfo]
    """
    shapes: list[SourceClassShape] = []
    for ir in module_irs:
        module_shapes = _class_shapes_from_ir(ir)
        if package_root is not None:
            module_shapes = [
                SourceClassShape(
                    name=shape.name,
                    bases=shape.bases,
                    local_fields=shape.local_fields,
                    local_field_annotations=shape.local_field_annotations,
                    path=shape.path,
                    module=module_name_for_path(shape.path, package_root),
                    lineno=shape.lineno,
                )
                for shape in module_shapes
            ]
        shapes.extend(module_shapes)
    return _resolve_model_shapes(shapes)


def _resolve_model_shapes(shapes: list[SourceClassShape]) -> list[SourceModelInfo]:
    """Resolve ApiModel inheritance and effective fields for class shapes.

    :param shapes: Raw class shapes collected from source files.
    :type shapes: list[SourceClassShape]
    :return: ApiModel-derived source models.
    :rtype: list[SourceModelInfo]
    """
    by_key: dict[tuple[Path, str], SourceClassShape] = {(shape.path, shape.name): shape for shape in shapes}
    by_name: dict[str, list[SourceClassShape]] = defaultdict(list)
    for shape in shapes:
        by_name[shape.name].append(shape)

    model_cache: dict[tuple[Path, str], bool] = {}
    field_cache: dict[tuple[Path, str], frozenset[str]] = {}
    annotation_cache: dict[tuple[Path, str], dict[str, str]] = {}

    def resolve_base(shape: SourceClassShape, base: str) -> SourceClassShape | None:
        """Resolve a base-class expression to a known class shape.

        :param shape: Class shape that declares the base.
        :type shape: SourceClassShape
        :param base: Base-class expression.
        :type base: str
        :return: Matching class shape, if it can be resolved unambiguously.
        :rtype: SourceClassShape | None
        """
        base_name = _final_name(base)
        local = by_key.get((shape.path, base_name))
        if local is not None:
            return local
        candidates = by_name.get(base_name, [])
        if len(candidates) == 1:
            return candidates[0]
        return None

    def is_model(shape: SourceClassShape, visiting: frozenset[tuple[Path, str]] = frozenset()) -> bool:
        """Return whether a class shape inherits from an SDK model root.

        :param shape: Class shape to classify.
        :type shape: SourceClassShape
        :param visiting: Recursion guard for inheritance cycles.
        :type visiting: frozenset[tuple[Path, str]]
        :return: ``True`` when the shape is ApiModel-derived.
        :rtype: bool
        """
        key = (shape.path, shape.name)
        if key in model_cache:
            return model_cache[key]
        if key in visiting:
            return False
        if shape.name in MODEL_ROOT_NAMES:
            model_cache[key] = True
            return True
        for base in shape.bases:
            base_name = _final_name(base)
            if base_name in MODEL_ROOT_NAMES:
                model_cache[key] = True
                return True
            parent = resolve_base(shape, base)
            if parent is not None and is_model(parent, visiting | {key}):
                model_cache[key] = True
                return True
        model_cache[key] = False
        return False

    def effective_fields(
        shape: SourceClassShape,
        visiting: frozenset[tuple[Path, str]] = frozenset(),
    ) -> frozenset[str]:
        """Return local and inherited field names for a model shape.

        :param shape: Model class shape to resolve.
        :type shape: SourceClassShape
        :param visiting: Recursion guard for inheritance cycles.
        :type visiting: frozenset[tuple[Path, str]]
        :return: Merged field-name set.
        :rtype: frozenset[str]
        """
        key = (shape.path, shape.name)
        if key in field_cache:
            return field_cache[key]
        if key in visiting:
            return frozenset(shape.local_fields)

        fields: set[str] = set()
        for base in shape.bases:
            parent = resolve_base(shape, base)
            if parent is not None and is_model(parent):
                fields.update(effective_fields(parent, visiting | {key}))
        fields.update(shape.local_fields)
        result = frozenset(fields)
        field_cache[key] = result
        return result

    def effective_annotations(
        shape: SourceClassShape,
        visiting: frozenset[tuple[Path, str]] = frozenset(),
    ) -> dict[str, str]:
        """Return local and inherited field annotation strings.

        :param shape: Model class shape to resolve.
        :type shape: SourceClassShape
        :param visiting: Recursion guard for inheritance cycles.
        :type visiting: frozenset[tuple[Path, str]]
        :return: Mapping from effective field name to annotation source.
        :rtype: dict[str, str]
        """
        key = (shape.path, shape.name)
        if key in annotation_cache:
            return annotation_cache[key]
        if key in visiting:
            return dict(shape.local_field_annotations)

        annotations: dict[str, str] = {}
        for base in shape.bases:
            parent = resolve_base(shape, base)
            if parent is not None and is_model(parent):
                annotations.update(effective_annotations(parent, visiting | {key}))
        annotations.update(shape.local_field_annotations)
        annotation_cache[key] = annotations
        return annotations

    models: list[SourceModelInfo] = []
    for shape in shapes:
        if shape.name == 'ApiModel':
            continue
        if not is_model(shape):
            continue
        models.append(
            SourceModelInfo(
                name=shape.name,
                field_names=effective_fields(shape),
                field_annotations=effective_annotations(shape),
                path=shape.path,
                module=shape.module,
                lineno=shape.lineno,
            )
        )
    models.sort(key=lambda model: (model.path.as_posix(), model.lineno, model.name))
    return models


def should_scan_sdk_file(path: Path) -> bool:
    """Return whether an SDK source file should be included in the scan.

    :param path: Candidate Python source path.
    :type path: Path
    :return: ``True`` if the file belongs to SDK model source.
    :rtype: bool
    """
    if path.name in SDK_SKIP_FILES:
        return False
    if path.name.startswith('as_'):
        return False
    if path.name.startswith('test_'):
        return False
    if '__pycache__' in path.parts:
        return False
    if 'tests' in path.parts:
        return False
    return True


def collect_generated_models(generated_file: Path) -> list[SourceModelInfo]:
    """Collect generated ApiModel-like classes from one file.

    :param generated_file: Auto-generated Python source file.
    :type generated_file: Path
    :return: Generated models declared in the source file.
    :rtype: list[SourceModelInfo]
    """
    return collect_models_from_module_irs([extract(generated_file)], generated_file.parent)


def collect_sdk_models(sdk_root: Path) -> tuple[list[SourceModelInfo], int]:
    """Collect SDK ApiModel-like classes under an SDK package root.

    :param sdk_root: SDK package directory to scan.
    :type sdk_root: Path
    :return: Tuple of collected SDK models and scanned-file count.
    :rtype: tuple[list[SourceModelInfo], int]
    """
    module_irs: list[ModuleIR] = []
    files_scanned = 0
    for path in sorted(sdk_root.rglob('*.py')):
        if not should_scan_sdk_file(path):
            continue
        files_scanned += 1
        try:
            module_irs.append(extract(path))
        except SyntaxError:
            continue
    return collect_models_from_module_irs(module_irs, sdk_root.parent), files_scanned


def load_generated_source_at_ref(generated_file: Path, base_ref: str, repo_root: Path = REPO_ROOT) -> str | None:
    """Load a generated file's historical contents from Git.

    :param generated_file: Current generated source file.
    :type generated_file: Path
    :param base_ref: Git ref to read from.
    :type base_ref: str
    :param repo_root: Repository root for the ``git show`` invocation.
    :type repo_root: Path
    :return: File contents at the ref, or ``None`` if the blob is absent.
    :rtype: str | None
    """
    try:
        rel = generated_file.resolve().relative_to(repo_root.resolve())
        blob_path = rel.as_posix()
    except ValueError:
        blob_path = generated_file.as_posix()

    proc = subprocess.run(
        ['git', 'show', f'{base_ref}:{blob_path}'],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def filter_added_models(models: list[SourceModelInfo], generated_file: Path, base_ref: str) -> list[SourceModelInfo]:
    """Keep only models whose class names are absent from a base ref.

    :param models: Current generated models.
    :type models: list[SourceModelInfo]
    :param generated_file: Current generated source path.
    :type generated_file: Path
    :param base_ref: Git ref used as the previous version.
    :type base_ref: str
    :return: Models considered newly added.
    :rtype: list[SourceModelInfo]
    """
    old_source = load_generated_source_at_ref(generated_file, base_ref)
    if old_source is None:
        return models

    old_ir = extract_from_text(old_source, str(generated_file))
    old_models = collect_models_from_module_irs([old_ir], generated_file.parent)
    old_names = {model.name for model in old_models}
    return [model for model in models if model.name not in old_names]


def _strip_outer_optional(annotation: str) -> str:
    """Remove one outer optional wrapper from an annotation string.

    :param annotation: Annotation source string.
    :type annotation: str
    :return: Annotation without ``Optional`` or ``| None`` when present.
    :rtype: str
    """
    annotation = ''.join(annotation.split())
    if annotation.startswith('Optional[') and annotation.endswith(']'):
        return annotation[len('Optional[') : -1]
    if annotation.startswith('Union[') and annotation.endswith(']'):
        parts = [part for part in annotation[len('Union[') : -1].split(',') if part not in {'None', 'NoneType'}]
        if len(parts) == 1:
            return parts[0]
    if annotation.endswith('|None'):
        return annotation[:-5]
    if annotation.startswith('None|'):
        return annotation[5:]
    return annotation


def _strip_typing_prefixes(annotation: str) -> str:
    """Remove common module prefixes from an annotation string.

    :param annotation: Annotation source string.
    :type annotation: str
    :return: Annotation with ``typing.`` and ``builtins.`` prefixes removed.
    :rtype: str
    """
    for prefix in ('typing.', 'builtins.'):
        annotation = annotation.replace(prefix, '')
    return annotation


def _canonical_annotation(annotation: str) -> str:
    """Normalize an annotation string for lightweight comparison.

    :param annotation: Annotation source string.
    :type annotation: str
    :return: Canonical annotation string.
    :rtype: str
    """
    return _strip_typing_prefixes(_strip_outer_optional(annotation))


def _container_arg(annotation: str, container: str) -> str | None:
    """Return the single inner argument for a simple container annotation.

    :param annotation: Annotation source string.
    :type annotation: str
    :param container: Container name such as ``list``.
    :type container: str
    :return: Inner annotation string, or ``None`` if not a matching container.
    :rtype: str | None
    """
    prefix = f'{container}['
    if annotation.startswith(prefix) and annotation.endswith(']'):
        return annotation[len(prefix) : -1]
    return None


def _top_level_type_name(annotation: str) -> str:
    """Return the leading type name from an annotation string.

    :param annotation: Annotation source string.
    :type annotation: str
    :return: Top-level type name without module qualification.
    :rtype: str
    """
    for separator in ('[', '|', ','):
        annotation = annotation.split(separator, maxsplit=1)[0]
    return annotation.rsplit('.', maxsplit=1)[-1]


def annotations_compatible(generated_annotation: str, sdk_annotation: str) -> bool:
    """Return whether two annotation strings are compatible for supersets.

    This is intentionally looser than the legacy runtime type comparison. It
    blocks obvious primitive/container mismatches while allowing generated and
    hand-maintained custom model names to differ.

    :param generated_annotation: Generated model annotation string.
    :type generated_annotation: str
    :param sdk_annotation: SDK model annotation string.
    :type sdk_annotation: str
    :return: ``True`` when the annotations are compatible enough for a superset.
    :rtype: bool
    """
    generated_annotation = _canonical_annotation(generated_annotation)
    sdk_annotation = _canonical_annotation(sdk_annotation)
    if generated_annotation == sdk_annotation:
        return True

    for container in ('list', 'set', 'tuple'):
        generated_inner = _container_arg(generated_annotation, container)
        sdk_inner = _container_arg(sdk_annotation, container)
        if generated_inner is not None and sdk_inner is not None:
            return annotations_compatible(generated_inner, sdk_inner)

    generated_name = _top_level_type_name(generated_annotation)
    sdk_name = _top_level_type_name(sdk_annotation)
    if generated_name in BUILTIN_TYPE_NAMES or sdk_name in BUILTIN_TYPE_NAMES:
        return False

    # User-defined model and enum names often differ between generated files and
    # the hand-maintained SDK. Field-name superset matching is the structural
    # signal; this only blocks obvious primitive/container mismatches.
    return bool(generated_name and sdk_name)


def common_fields_are_type_compatible(generated_model: SourceModelInfo, sdk_model: SourceModelInfo) -> bool:
    """Return whether shared fields have compatible annotation strings.

    :param generated_model: Generated model being matched.
    :type generated_model: SourceModelInfo
    :param sdk_model: SDK candidate model.
    :type sdk_model: SourceModelInfo
    :return: ``True`` when all generated fields are type-compatible.
    :rtype: bool
    """
    for field_name in generated_model.field_names:
        generated_annotation = generated_model.field_annotations.get(field_name, '')
        sdk_annotation = sdk_model.field_annotations.get(field_name, '')
        if not annotations_compatible(generated_annotation, sdk_annotation):
            return False
    return True


def find_generated_equivalent_models(
    generated_models: list[SourceModelInfo],
    sdk_models: list[SourceModelInfo],
) -> tuple[GeneratedModelMatch, ...]:
    """Find exact and fallback superset candidates for generated models.

    Exact field-name matches are preferred. Superset candidates are only
    reported when no exact candidate exists.

    :param generated_models: Generated models to compare.
    :type generated_models: list[SourceModelInfo]
    :param sdk_models: SDK models to search.
    :type sdk_models: list[SourceModelInfo]
    :return: Per-generated-model match records.
    :rtype: tuple[GeneratedModelMatch, ...]
    """
    candidates_by_fields: dict[frozenset[str], list[SourceModelInfo]] = defaultdict(list)
    for sdk_model in sdk_models:
        candidates_by_fields[sdk_model.field_names].append(sdk_model)

    matches: list[GeneratedModelMatch] = []
    for generated_model in generated_models:
        candidates = tuple(
            sorted(
                candidates_by_fields.get(generated_model.field_names, []),
                key=lambda model: (model.module, model.name, model.lineno),
            )
        )
        superset_candidates: tuple[GeneratedSupersetCandidate, ...] = ()
        if not candidates:
            superset_candidates = tuple(
                sorted(
                    (
                        GeneratedSupersetCandidate(
                            model=sdk_model,
                            extra_fields=sdk_model.field_names - generated_model.field_names,
                        )
                        for sdk_model in sdk_models
                        if generated_model.field_names < sdk_model.field_names
                        and common_fields_are_type_compatible(generated_model, sdk_model)
                    ),
                    key=lambda candidate: (
                        len(candidate.extra_fields),
                        candidate.model.module,
                        candidate.model.name,
                        candidate.model.lineno,
                    ),
                )
            )
        matches.append(
            GeneratedModelMatch(
                generated=generated_model,
                candidates=candidates,
                superset_candidates=superset_candidates,
            )
        )
    return tuple(matches)


def analyse_generated_file(
    generated_file: Path,
    sdk_root: Path = Path('wxc_sdk'),
    added_only: bool = False,
    base_ref: str = 'HEAD',
) -> GeneratedAnalysisResult:
    """Analyze one generated file against SDK source models.

    :param generated_file: Auto-generated Python source to inspect.
    :type generated_file: Path
    :param sdk_root: SDK package root to scan.
    :type sdk_root: Path
    :param added_only: Whether to analyze only class names absent at ``base_ref``.
    :type added_only: bool
    :param base_ref: Git ref used for ``added_only`` filtering.
    :type base_ref: str
    :return: Complete generated-file analysis result.
    :rtype: GeneratedAnalysisResult
    """
    generated_file = generated_file.resolve()
    sdk_root = sdk_root.resolve()

    all_generated_models = collect_generated_models(generated_file)
    generated_models = (
        filter_added_models(all_generated_models, generated_file, base_ref) if added_only else all_generated_models
    )
    sdk_models, sdk_files_scanned = collect_sdk_models(sdk_root)

    return GeneratedAnalysisResult(
        generated_file=generated_file,
        sdk_root=sdk_root,
        base_ref=base_ref,
        added_only=added_only,
        generated_total=len(all_generated_models),
        sdk_models_total=len(sdk_models),
        sdk_files_scanned=sdk_files_scanned,
        matches=find_generated_equivalent_models(generated_models, sdk_models),
    )


def _path_for_output(path: Path) -> str:
    """Return a stable path string for human and JSON output.

    :param path: Path to render.
    :type path: Path
    :return: Repository-relative path when possible, otherwise original path.
    :rtype: str
    """
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _model_ref(model: SourceModelInfo) -> dict[str, object]:
    """Return the JSON-compatible reference for a source model.

    :param model: Source model to serialize.
    :type model: SourceModelInfo
    :return: JSON-compatible model reference.
    :rtype: dict[str, object]
    """
    return {
        'name': model.name,
        'module': model.module,
        'import_path': model.import_path,
        'source': _path_for_output(model.path),
        'line': model.lineno,
        'field_count': model.field_count,
        'fields': sorted(model.field_names),
    }


def render_generated_json(result: GeneratedAnalysisResult) -> str:
    """Render a generated-file analysis result as JSON.

    :param result: Analysis result to render.
    :type result: GeneratedAnalysisResult
    :return: Pretty-printed JSON report.
    :rtype: str
    """
    payload = {
        'summary': {
            'generated_file': _path_for_output(result.generated_file),
            'sdk_root': _path_for_output(result.sdk_root),
            'added_only': result.added_only,
            'base_ref': result.base_ref,
            'generated_models_total': result.generated_total,
            'generated_models_analyzed': len(result.matches),
            'sdk_models_indexed': result.sdk_models_total,
            'sdk_files_scanned': result.sdk_files_scanned,
            'matched_models': result.matched_total,
            'superset_models': result.superset_total,
            'unmatched_models': result.unmatched_total,
        },
        'models': [
            {
                **_model_ref(match.generated),
                'status': match.status,
                'matches': [_model_ref(candidate) for candidate in match.candidates],
                'superset_matches': [
                    {
                        **_model_ref(candidate.model),
                        'additional_fields': sorted(candidate.extra_fields),
                    }
                    for candidate in match.superset_candidates
                ],
            }
            for match in result.matches
        ],
    }
    return json.dumps(payload, indent=2)


def render_generated_text(result: GeneratedAnalysisResult) -> str:
    """Render a generated-file analysis result as plain text.

    :param result: Analysis result to render.
    :type result: GeneratedAnalysisResult
    :return: Human-readable report text.
    :rtype: str
    """
    lines: list[str] = []
    w = lines.append

    w('=' * 72)
    w('Generated Model Equivalence Report')
    w('=' * 72)
    w(f'Generated file          : {_path_for_output(result.generated_file)}')
    w(f'SDK root                : {_path_for_output(result.sdk_root)}')
    if result.added_only:
        w(f'Mode                    : added only since {result.base_ref}')
    else:
        w('Mode                    : all generated models')
    w(f'Generated models found  : {result.generated_total}')
    w(f'Generated models checked: {len(result.matches)}')
    w(f'SDK files scanned       : {result.sdk_files_scanned}')
    w(f'SDK models indexed      : {result.sdk_models_total}')
    w(f'Matched models          : {result.matched_total}')
    w(f'Superset-only models    : {result.superset_total}')
    w(f'Unmatched models        : {result.unmatched_total}')
    w('')

    for index, match in enumerate(result.matches, 1):
        generated = match.generated
        w('-' * 72)
        w(f'{index}. {generated.name}  line {generated.lineno}  fields={generated.field_count}')
        w(f'Fields: {", ".join(sorted(generated.field_names)) or "(none)"}')
        if not match.candidates and not match.superset_candidates:
            w('Matches: no match')
            continue
        if match.candidates:
            w('Matches:')
            for candidate in match.candidates:
                w(
                    f'  - {candidate.import_path} '
                    f'({_path_for_output(candidate.path)}:{candidate.lineno}, fields={candidate.field_count})'
                )
            continue
        w('Matches: no exact match')
        w('Superset matches:')
        for superset_candidate in match.superset_candidates:
            extra_fields = ', '.join(sorted(superset_candidate.extra_fields))
            w(
                f'  - {superset_candidate.model.import_path} '
                f'({_path_for_output(superset_candidate.model.path)}:{superset_candidate.model.lineno}, '
                f'fields={superset_candidate.model.field_count}; additional attributes: {extra_fields})'
            )

    return '\n'.join(lines)


def parse_args() -> Namespace:
    """Parse command-line arguments for standalone generated-file mode.

    :return: Parsed command-line namespace.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description='Find SDK models with the same Python field names as generated OpenAPI models.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('generated_file', help='Auto-generated Python source to analyze')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format (default: text)')
    parser.add_argument('--output', '-o', help='Write report to FILE (default: stdout)')
    parser.add_argument('--sdk-root', default='wxc_sdk', help='SDK package root to scan (default: wxc_sdk)')
    parser.add_argument('--added-only', action='store_true', help='Only analyze models added since --base-ref')
    parser.add_argument('--base-ref', default='HEAD', help='Git base ref for --added-only (default: HEAD)')
    return parser.parse_args()


def main() -> None:
    """Run the standalone generated-file CLI entry point.

    :return: ``None``.
    :rtype: None
    """
    args = parse_args()
    result = analyse_generated_file(
        generated_file=Path(args.generated_file),
        sdk_root=Path(args.sdk_root),
        added_only=args.added_only,
        base_ref=args.base_ref,
    )
    report = render_generated_json(result) if args.format == 'json' else render_generated_text(result)

    if args.output:
        Path(args.output).write_text(report)
    else:
        print(report)


if __name__ == '__main__':
    main()

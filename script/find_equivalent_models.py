#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "pydantic"
# ]
# ///
"""
find_equivalent_models.py
─────────────────────────
Scan all Pydantic models exported by wxc_sdk.all_types and identify:

  • Equivalent models  – same field names AND equivalent field types
  • Similar models     – small differences in field names / types,
                         clustered into groups via union-find
  • Inheritance        – child models that extend another __all__ model,
                         highlighting empty subclasses (no new fields)

Usage
─────
    python find_equivalent_models.py [options]

Options
───────
  --max-diff N           Max field differences for "similar" (default: 3)
  --min-fields N         Ignore models with fewer than N fields (default: 3)
  --output FILE          Write report to FILE instead of stdout
  --format {text,json}   Output format (default: text)
  --include-subclasses   Include subclass pairs in similar section too
  --no-cluster           List similar pairs flat instead of clustering them
"""

import argparse
import inspect
import json
import sys
import typing
from argparse import Namespace
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Any

import pydantic

# we need to add the parent dir into sys.path so that the import of wxc_sdk can be resolved locally
p_dir = str(Path(__file__).parent.parent)
print(f'inserting parent dir {p_dir} into sys.path')
sys.path.insert(0, p_dir)
print(sys.path)
print()

from wxc_sdk.base import ApiModel

# ══════════════════════════════════════════════════════════════════════════════
# Type canonicalisation & pretty-printing
# ══════════════════════════════════════════════════════════════════════════════


def canonical_type(ann: Any, depth: int = 0) -> object:
    """Return a hashable, comparable representation of a type annotation."""
    if depth > 10:
        return str(ann)

    origin = typing.get_origin(ann)
    args = typing.get_args(ann)

    if origin is typing.Union:
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return 'Optional', canonical_type(non_none[0], depth + 1)
        return 'Union', tuple(sorted(str(canonical_type(a, depth + 1)) for a in args))

    if origin is typing.Literal:
        return 'Literal', tuple(sorted(str(a) for a in args))

    if origin is list:
        inner = canonical_type(args[0], depth + 1) if args else 'Any'
        return 'List', inner

    if origin is dict:
        k = canonical_type(args[0], depth + 1) if args else 'Any'
        v = canonical_type(args[1], depth + 1) if len(args) > 1 else 'Any'
        return 'Dict', k, v

    if origin is tuple:
        return 'Tuple', tuple(canonical_type(a, depth + 1) for a in args)

    if origin is set:
        inner = canonical_type(args[0], depth + 1) if args else 'Any'
        return 'Set', inner

    if isinstance(ann, type):
        return ann.__name__

    return str(ann)


def pretty_type(ann: Any, depth: int = 0) -> str:
    """Human-readable type string: Optional[X], List[X], etc."""
    if depth > 10:
        return str(ann)

    origin = typing.get_origin(ann)
    args = typing.get_args(ann)

    if origin is typing.Union:
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return f'Optional[{pretty_type(non_none[0], depth + 1)}]'
        parts = ' | '.join(pretty_type(a, depth + 1) for a in args)
        return f'Union[{parts}]'

    if origin is typing.Literal:
        vals = ', '.join(repr(a) for a in args)
        return f'Literal[{vals}]'

    if origin is list:
        inner = pretty_type(args[0], depth + 1) if args else 'Any'
        return f'List[{inner}]'

    if origin is dict:
        k = pretty_type(args[0], depth + 1) if args else 'Any'
        v = pretty_type(args[1], depth + 1) if len(args) > 1 else 'Any'
        return f'Dict[{k}, {v}]'

    if origin is tuple:
        parts = ', '.join(pretty_type(a, depth + 1) for a in args)
        return f'Tuple[{parts}]'

    if origin is set:
        inner = pretty_type(args[0], depth + 1) if args else 'Any'
        return f'Set[{inner}]'

    if isinstance(ann, type):
        return ann.__name__

    return str(ann)


def types_equivalent(a: Any, b: Any) -> bool:
    return canonical_type(a) == canonical_type(b)


# ══════════════════════════════════════════════════════════════════════════════
# Model introspection
# ══════════════════════════════════════════════════════════════════════════════


@dataclass
class ModelInfo:
    name: str
    cls: type[pydantic.BaseModel]
    source_file: str
    module: str
    fields: dict[str, pydantic.fields.FieldInfo]  # name -> pydantic FieldInfo
    field_names: frozenset[str]
    canonical_sig: tuple[tuple[str, str], ...]  # sorted (field_name, canonical_type_str)

    # Filled in during inheritance analysis
    parent_model: 'ModelInfo | None' = field(default=None, compare=False, repr=False)
    child_models: list['ModelInfo'] = field(default_factory=list, compare=False, repr=False)

    def __hash__(self) -> int:
        return hash(id(self.cls))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ModelInfo) and self.cls is other.cls


def get_source_file(cls: type[pydantic.BaseModel]) -> str:
    try:
        f = inspect.getfile(cls)
        parts = Path(f).parts
        try:
            idx = next(i for i, p in enumerate(parts) if p == 'wxc_sdk')
            return str(Path(*parts[idx:]))
        except StopIteration:
            return f
    except (TypeError, OSError):
        return '<unknown>'


def collect_models(min_fields: int = 3) -> list[ModelInfo]:
    from wxc_sdk import all_types

    models: list[ModelInfo] = []
    seen_ids: set[int] = set()

    for name in all_types.__all__:
        obj = getattr(all_types, name, None)
        if obj is None:
            continue
        if not (inspect.isclass(obj) and issubclass(obj, pydantic.BaseModel)):
            continue
        if id(obj) in seen_ids:
            continue
        seen_ids.add(id(obj))

        flds = obj.model_fields
        if len(flds) < min_fields:
            continue

        sig = tuple(sorted((fname, str(canonical_type(fi.annotation))) for fname, fi in flds.items()))

        models.append(
            ModelInfo(
                name=name,
                cls=obj,
                source_file=get_source_file(obj),
                module=obj.__module__,
                fields=flds,
                field_names=frozenset(flds.keys()),
                canonical_sig=sig,
            )
        )

    return models


def build_inheritance(models: list[ModelInfo]) -> list[ModelInfo]:
    """Attach .parent_model / .child_models for non-trivial inheritance."""
    cls_to_info: dict[type, ModelInfo] = {m.cls: m for m in models}
    base_classes = {pydantic.BaseModel, ApiModel, object}

    for m in models:
        for ancestor in m.cls.__mro__[1:]:
            if ancestor in base_classes:
                continue
            if ancestor in cls_to_info:
                parent_info = cls_to_info[ancestor]
                m.parent_model = parent_info
                parent_info.child_models.append(m)
                break  # nearest meaningful ancestor only

    return models


# ══════════════════════════════════════════════════════════════════════════════
# Diffs
# ══════════════════════════════════════════════════════════════════════════════


@dataclass
class FieldDiff:
    only_in_a: list[str]
    only_in_b: list[str]
    type_differs: list[tuple[str, str, str]]  # (field_name, pretty_type_a, pretty_type_b)

    def total(self) -> int:
        return len(self.only_in_a) + len(self.only_in_b) + len(self.type_differs)


def compute_diff(a: ModelInfo, b: ModelInfo) -> FieldDiff:
    only_a = sorted(a.field_names - b.field_names)
    only_b = sorted(b.field_names - a.field_names)
    common = a.field_names & b.field_names
    type_diffs = []
    for fname in sorted(common):
        ta = a.fields[fname].annotation
        tb = b.fields[fname].annotation
        if not types_equivalent(ta, tb):
            type_diffs.append((fname, pretty_type(ta), pretty_type(tb)))
    return FieldDiff(only_a, only_b, type_diffs)


# ══════════════════════════════════════════════════════════════════════════════
# Union-Find
# ══════════════════════════════════════════════════════════════════════════════


class UnionFind:
    def __init__(self) -> None:
        self._parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self._parent.setdefault(x, x)
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def union(self, x: str, y: str) -> None:
        self._parent[self.find(x)] = self.find(y)


# ══════════════════════════════════════════════════════════════════════════════
# Result types
# ══════════════════════════════════════════════════════════════════════════════


@dataclass
class EquivalentGroup:
    models: list[ModelInfo]
    fields: frozenset[str]


@dataclass
class SimilarPair:
    a: ModelInfo
    b: ModelInfo
    diff: FieldDiff

    def total(self) -> int:
        return self.diff.total()


@dataclass
class SimilarCluster:
    members: list[ModelInfo]
    pairs: list[SimilarPair]

    def max_diff(self) -> int:
        return max((p.total() for p in self.pairs), default=0)


@dataclass
class InheritanceEntry:
    child: ModelInfo
    parent: ModelInfo
    added_fields: list[str]


# ══════════════════════════════════════════════════════════════════════════════
# Core analysis
# ══════════════════════════════════════════════════════════════════════════════


def analyse(
    models: list[ModelInfo],
    max_diff: int,
    include_subclasses: bool,
    cluster: bool,
) -> tuple[list[EquivalentGroup], list[SimilarCluster]]:

    # ── Equivalent groups ─────────────────────────────────────────────────
    sig_buckets: dict[tuple[tuple[str, str], ...], list[ModelInfo]] = defaultdict(list)
    for m in models:
        sig_buckets[m.canonical_sig].append(m)

    equivalent_groups = sorted(
        [EquivalentGroup(ms, ms[0].field_names) for ms in sig_buckets.values() if len(ms) > 1],
        key=lambda g: (-len(g.models), sorted(m.name for m in g.models)[0]),
    )

    equiv_pairs: set[frozenset[str]] = set()
    for grp in equivalent_groups:
        for ma, mb in combinations(grp.models, 2):
            equiv_pairs.add(frozenset({ma.name, mb.name}))

    subclass_pairs: set[frozenset[str]] = set()
    if not include_subclasses:
        for m in models:
            if m.parent_model is not None:
                subclass_pairs.add(frozenset({m.name, m.parent_model.name}))

    # ── Similar pairs ─────────────────────────────────────────────────────
    similar_pairs: list[SimilarPair] = []

    for ma, mb in combinations(models, 2):
        key: frozenset[str] = frozenset({ma.name, mb.name})
        if key in equiv_pairs or key in subclass_pairs:
            continue
        if abs(len(ma.field_names) - len(mb.field_names)) > max_diff:
            continue
        if len(ma.field_names ^ mb.field_names) > max_diff * 2:
            continue

        diff = compute_diff(ma, mb)
        if 0 < diff.total() <= max_diff:
            similar_pairs.append(SimilarPair(ma, mb, diff))

    similar_pairs.sort(key=lambda p: (p.total(), p.a.name, p.b.name))

    # ── Cluster ───────────────────────────────────────────────────────────
    if not cluster:
        clusters = [SimilarCluster([p.a, p.b], [p]) for p in similar_pairs]
        return equivalent_groups, clusters

    uf = UnionFind()
    for p in similar_pairs:
        uf.union(p.a.name, p.b.name)

    name_to_model: dict[str, ModelInfo] = {m.name: m for m in models}
    cluster_members: dict[str, list[ModelInfo]] = defaultdict(list)
    cluster_pairs: dict[str, list[SimilarPair]] = defaultdict(list)

    seen_names: set[str] = set()
    for p in similar_pairs:
        for name in (p.a.name, p.b.name):
            seen_names.add(name)
        root = uf.find(p.a.name)
        cluster_pairs[root].append(p)

    for name in seen_names:
        cluster_members[uf.find(name)].append(name_to_model[name])

    clusters = []
    for root, members in cluster_members.items():
        clusters.append(
            SimilarCluster(
                members=sorted(members, key=lambda m: m.name),
                pairs=sorted(cluster_pairs[root], key=lambda p: (p.total(), p.a.name)),
            )
        )

    clusters.sort(key=lambda c: (-len(c.members), c.members[0].name))
    return equivalent_groups, clusters


def collect_inheritance_entries(models: list[ModelInfo]) -> list[InheritanceEntry]:
    entries = []
    for m in models:
        if m.parent_model is None:
            continue
        added = sorted(m.field_names - m.parent_model.field_names)
        entries.append(InheritanceEntry(m, m.parent_model, added))
    entries.sort(key=lambda e: (e.parent.name, e.child.name))
    return entries


# ══════════════════════════════════════════════════════════════════════════════
# Text rendering
# ══════════════════════════════════════════════════════════════════════════════


def render_text(
    models: list[ModelInfo],
    equiv_groups: list[EquivalentGroup],
    clusters: list[SimilarCluster],
    inheritance: list[InheritanceEntry],
    max_diff: int,
    min_fields: int,
) -> str:

    lines: list[str] = []
    w = lines.append

    total_similar_models = len({m for c in clusters for m in c.members})
    total_similar_pairs = sum(len(c.pairs) for c in clusters)

    w('=' * 72)
    w('wxc_sdk – Redundant / Similar Model Report  (v2)')
    w('=' * 72)
    w(f'Models examined (≥{min_fields} fields)  : {len(models)}')
    w(f'Equivalent groups               : {len(equiv_groups)}')
    w(
        f'Similar clusters                : {len(clusters)}'
        f'  ({total_similar_pairs} pairs across {total_similar_models} models)'
    )
    w(f'Inheritance relationships        : {len(inheritance)}')
    w('')

    # ─── Section 1: Equivalent ────────────────────────────────────────────
    w('━' * 72)
    w(f'1. EQUIVALENT MODELS  ({len(equiv_groups)} groups)')
    w('━' * 72)
    w('   Models with identical field names and types — safe to consolidate.')
    w('')

    if equiv_groups:
        for i, grp in enumerate(equiv_groups, 1):
            sample = grp.models[0]
            w(f'  ┌─ Group {i}  ·  {len(grp.models)} models  ·  {len(sample.field_names)} fields')
            w(f'  │  Fields: {", ".join(sorted(sample.field_names))}')
            for m in grp.models:
                note = ''
                if m.parent_model and m.parent_model in grp.models:
                    note = f'  ← extends {m.parent_model.name}'
                w(f'  │    {m.name:<46} {m.source_file}{note}')
            w('  └─')
            w('')
    else:
        w('  (none found)')
        w('')

    # ─── Section 2: Similar clusters ─────────────────────────────────────
    w('━' * 72)
    w(f'2. SIMILAR MODEL CLUSTERS  ({len(clusters)} clusters, max-diff={max_diff})')
    w('━' * 72)
    w("   Each cluster's members are within --max-diff of ≥1 other member.")
    w('   Subclass pairs are excluded here (see section 3).')
    w('')

    if clusters:
        for i, clust in enumerate(clusters, 1):
            w(f'  ┌─ Cluster {i}  ·  {len(clust.members)} models  ·  max diff {clust.max_diff()}')
            seen_files: set[str] = set()
            for m in clust.members:
                if m.source_file not in seen_files:
                    w(f'  │    {m.name:<46} {m.source_file}')
                    seen_files.add(m.source_file)
                else:
                    w(f'  │    {m.name}')

            w('  │  Differences:')
            if len(clust.pairs) <= 10:
                for p in clust.pairs:
                    d = p.diff
                    w(f'  │    ↔ {p.a.name}  vs  {p.b.name}  ({p.total()} diff{"s" if p.total() != 1 else ""})')
                    if d.only_in_a:
                        w(f'  │        only in {p.a.name}: {", ".join(d.only_in_a)}')
                    if d.only_in_b:
                        w(f'  │        only in {p.b.name}: {", ".join(d.only_in_b)}')
                    for fname, ta, tb in d.type_differs:
                        w(f"  │        field '{fname}':")
                        w(f'  │          {p.a.name}: {ta}')
                        w(f'  │          {p.b.name}: {tb}')
            else:
                # Large cluster: show most distinguishing fields
                field_counts: dict[str, int] = defaultdict(int)
                for p in clust.pairs:
                    for fn in p.diff.only_in_a + p.diff.only_in_b:
                        field_counts[fn] += 1
                top = sorted(field_counts, key=lambda x: -field_counts[x])[:8]
                w(f'  │    ({len(clust.pairs)} edges total — top distinguishing fields:)')
                w(f'  │    {", ".join(top)}')

            w('  └─')
            w('')
    else:
        w('  (none found)')
        w('')

    # ─── Section 3: Inheritance ───────────────────────────────────────────
    w('━' * 72)
    w(f'3. INHERITANCE RELATIONSHIPS  ({len(inheritance)} entries)')
    w('━' * 72)
    w('   Child models that extend another model present in __all__.')
    w('   ⚠  marks empty subclasses (no new fields) — prime candidates for removal.')
    w('')

    if inheritance:
        by_parent: dict[str, list[InheritanceEntry]] = defaultdict(list)
        for e in inheritance:
            by_parent[e.parent.name].append(e)

        for parent_name, entries in sorted(by_parent.items()):
            parent = entries[0].parent
            w(f'  {parent_name}  [{parent.source_file}]')
            for e in entries:
                if e.added_fields:
                    added_str = f'+ {", ".join(e.added_fields)}'
                else:
                    added_str = '⚠  (no new fields)'
                w(f'    └─ {e.child.name:<44} {added_str}')
            w('')
    else:
        w('  (none found)')
        w('')

    return '\n'.join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# JSON rendering
# ══════════════════════════════════════════════════════════════════════════════


def render_json(
    models: list[ModelInfo],
    equiv_groups: list[EquivalentGroup],
    clusters: list[SimilarCluster],
    inheritance: list[InheritanceEntry],
) -> str:
    def mref(m: ModelInfo) -> dict[str, str]:
        return {'name': m.name, 'source': m.source_file}

    out = {
        'summary': {
            'total_models': len(models),
            'equivalent_groups': len(equiv_groups),
            'similar_clusters': len(clusters),
            'similar_pairs': sum(len(c.pairs) for c in clusters),
            'inheritance_relationships': len(inheritance),
        },
        'equivalent_groups': [
            {
                'fields': sorted(grp.fields),
                'members': [mref(m) for m in grp.models],
            }
            for grp in equiv_groups
        ],
        'similar_clusters': [
            {
                'members': [mref(m) for m in c.members],
                'max_diff': c.max_diff(),
                'pairs': [
                    {
                        'a': mref(p.a),
                        'b': mref(p.b),
                        'total_differences': p.total(),
                        'only_in_a': p.diff.only_in_a,
                        'only_in_b': p.diff.only_in_b,
                        'type_differences': [
                            {'field': f, 'type_a': ta, 'type_b': tb} for f, ta, tb in p.diff.type_differs
                        ],
                    }
                    for p in c.pairs
                ],
            }
            for c in clusters
        ],
        'inheritance': [
            {
                'child': mref(e.child),
                'parent': mref(e.parent),
                'fields_added_by_child': e.added_fields,
                'empty_subclass': len(e.added_fields) == 0,
            }
            for e in inheritance
        ],
    }
    return json.dumps(out, indent=2)


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════


def parse_args() -> Namespace:
    p = argparse.ArgumentParser(
        description='Find equivalent and similar Pydantic models in wxc_sdk',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument('--max-diff', type=int, default=3, help="Max field differences for 'similar' (default: 3)")
    p.add_argument('--min-fields', type=int, default=3, help='Ignore models with fewer than N fields (default: 3)')
    p.add_argument('--output', '-o', help='Write report to FILE (default: stdout)')
    p.add_argument('--format', choices=['text', 'json'], default='text', help='Output format (default: text)')
    p.add_argument('--include-subclasses', action='store_true', help='Include subclass pairs in similar section')
    p.add_argument('--no-cluster', action='store_true', help='List pairs flat instead of clustering')
    return p.parse_args()


def main() -> None:
    args = parse_args()

    print('Collecting models…', file=sys.stderr)
    models = collect_models(min_fields=args.min_fields)
    print(f'  {len(models)} models (≥{args.min_fields} fields)', file=sys.stderr)

    print('Building inheritance graph…', file=sys.stderr)
    models = build_inheritance(models)
    inheritance = collect_inheritance_entries(models)
    print(f'  {len(inheritance)} parent→child relationships', file=sys.stderr)

    print('Analysing…', file=sys.stderr)
    equiv_groups, clusters = analyse(
        models,
        max_diff=args.max_diff,
        include_subclasses=args.include_subclasses,
        cluster=not args.no_cluster,
    )
    total_pairs = sum(len(c.pairs) for c in clusters)
    print(f'  {len(equiv_groups)} equivalent groups', file=sys.stderr)
    print(f'  {len(clusters)} similar clusters ({total_pairs} pairs)', file=sys.stderr)

    if args.format == 'json':
        report = render_json(models, equiv_groups, clusters, inheritance)
    else:
        report = render_text(models, equiv_groups, clusters, inheritance, args.max_diff, args.min_fields)

    if args.output:
        Path(args.output).write_text(report)
        print(f'Report written to {args.output}', file=sys.stderr)
    else:
        print(report)


if __name__ == '__main__':
    main()

# mypy: disable-error-code="arg-type,no-untyped-def,union-attr"
"""
Python class registry for OpenAPI schema; derived from PythonClassRegistry; used for code creation
"""

import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from typing import Any, Optional

import dateutil.parser

from apib.class_registry import PythonClassRegistry
from apib.python_class import Attribute, Endpoint, Parameter, PythonAPI, PythonClass
from apib.tools import sanitize_class_name, snake_case
from open_api.open_api_model import (
    OAContent,
    OAOperation,
    OAParameter,
    OARequestBody,
    OAResponse,
    OASchemaProperty,
    OASpec,
)
from open_api.open_api_sources import OpenApiSpecInfo

log = logging.getLogger(__name__)

# Verb prefixes that appear at the start of operation-specific model names
_MODEL_VERB_PREFIXES = ('Post', 'Put', 'Patch', 'Get', 'List', 'Modify', 'Create', 'Update', 'Delete', 'Add', 'Set')


@dataclass(frozen=True)
class _ResolvedPythonType:
    """
    Python type expression and the generated classes needed by that expression.

    ``referenced_classes`` preserves discovery order so generated unions remain stable.

    :param python_type: Complete generated Python type expression.
    :type python_type: str
    :param referenced_classes: Generated class names used by the type expression.
    :type referenced_classes: tuple[str, ...]
    """

    python_type: str
    referenced_classes: tuple[str, ...] = ()

    @property
    def primary_reference(self) -> Optional[str]:
        """
        Return the first class reference for legacy single-reference consumers.

        :return: First referenced class, or ``None`` for a primitive-only type.
        :rtype: Optional[str]
        """
        return self.referenced_classes[0] if self.referenced_classes else None


def _strip_model_name(qualified: str) -> str:
    """
    Return a cleaner class name for a consolidated canonical model by:
      1. Stripping a leading verb prefix (e.g. Get, Post, Modify)
      2. Stripping a trailing 'Object' suffix
      3. Stripping a trailing verb suffix (e.g. SomethingGet → Something)

    Only the *unqualified* part (after the last '%') is modified; the context prefix is kept.
    Returns the original string unchanged if no transformation applies.
    """
    context, sep, name = qualified.rpartition('%')
    # Strip leading verb prefix followed immediately by an upper-case letter
    for verb in _MODEL_VERB_PREFIXES:
        rest = name[len(verb) :]
        if name.startswith(verb) and rest and rest[0].isupper():
            name = rest
            break
    # Strip trailing 'Object'
    if name.endswith('Object') and len(name) > 6:
        name = name[:-6]
    # Strip trailing verb suffix (e.g. SomethingGet → Something)
    for verb in _MODEL_VERB_PREFIXES:
        if name.endswith(verb) and len(name) > len(verb):
            name = name[: -len(verb)]
            break
    return f'{context}{sep}{name}'


def class_name_from_schema_name(schema_name: str) -> str:
    """
    Convert schema name to class name
    """
    return sanitize_class_name(schema_name)


def class_name_from_ref(ref: str) -> str:
    """
    Convert reference to class name
    """
    ref_match = re.match(r'#/components/schemas/(.*)', ref)
    if not ref_match:
        raise ValueError(f'Invalid ref {ref}')
    return class_name_from_schema_name(ref_match.group(1))


def is_datetime(value: str) -> bool:
    """
    Check if value is a datetime
    """
    if not isinstance(value, str):
        return False
    value = value.strip("'").strip('"')

    # value has to have some minimum  length to qualify as a date
    if len(value) < 10:
        return False
    try:
        dateutil.parser.parse(value)
    except (OverflowError, dateutil.parser.ParserError, TypeError):
        # probably a string
        return False
    except Exception as e:
        raise NotImplementedError(f'Unexpected error when trying to parse a string: {e}') from e

    # only assume datetime if sample doesn't parse as number
    try:
        float(value)
    except ValueError:
        return True
    return False


class OpenApiPythonClassRegistry(PythonClassRegistry):
    """
    Registry of classes generated from OpenAPI schema
    """

    body_style: str
    consolidate_models: bool

    def __init__(self, body_style: str = 'args', consolidate_models: bool = False) -> None:
        super().__init__()  # type: ignore[no-untyped-call]
        self.body_style = body_style
        self.consolidate_models = consolidate_models

    def normalize(self) -> None:
        """Consolidate operation-specific models then run standard normalization."""
        if self.body_style != 'args' or self.consolidate_models:
            # for body_style args we don't consolidate (backward compatibility) unless enforced
            self.consolidate_resource_models()
            self._strip_verb_affixes_from_all_models()
            self._merge_include_sets_before_redundancy_elimination()
        super().normalize()

    def _merge_include_sets_before_redundancy_elimination(self) -> None:
        """
        Run eliminate_redundancies() early so we can detect which classes will be made redundant,
        then transfer their post/put include-sets to the canonical class they point to.

        Without this, a body model that shares all fields with a GET-result model gets made
        redundant by eliminate_redundancies(), and the endpoint ends up pointing to the canonical
        (the GET-result model) which never had include-sets registered on it.

        super().normalize() will call eliminate_redundancies() again, which is a no-op since all
        redundancies are already resolved.
        """
        self.eliminate_redundancies()  # type: ignore[no-untyped-call]
        for pc in self._classes.values():
            if not (pc.baseclass and not pc.attributes):
                continue
            # follow the baseclass chain to the ultimate canonical
            canonical_name, canonical = self._dereferenced_class(pc.baseclass)
            if canonical is None:
                continue
            for include_set in pc.post_include_sets:
                if include_set not in canonical.post_include_sets:
                    canonical.post_include_sets.append(include_set)
            for include_set in pc.put_include_sets:
                if include_set not in canonical.put_include_sets:
                    canonical.put_include_sets.append(include_set)
            canonical.post_nested_include.update(pc.post_nested_include)
            canonical.put_nested_include.update(pc.put_nested_include)

    def _apply_class_rename(self, old_name: str, new_name: str) -> None:
        """
        Rename a class and every singular or compound reference to it.

        :param old_name: Current qualified generated class name.
        :type old_name: str
        :param new_name: Replacement qualified generated class name.
        :type new_name: str
        :return: None.
        :raises KeyError: If ``old_name`` is not registered.
        """
        pc = self._classes.pop(old_name)
        pc.name = new_name
        self._classes[new_name] = pc

        for other_pc in self._classes.values():
            for attr in other_pc.attributes or []:
                if old_name in attr.class_references:
                    attr.replace_class_reference(old_name, new_name, (new_name,))
            if other_pc.alias and old_name in other_pc.alias.class_references:
                other_pc.alias.replace_class_reference(old_name, new_name, (new_name,))

        for _, endpoint in self.endpoints():
            if endpoint.body_class_name == old_name:
                endpoint.body_class_name = new_name
            if old_name in endpoint.result_class_references:
                endpoint.replace_result_class_reference(old_name, new_name, (new_name,))
            for param in chain(endpoint.body_parameter, endpoint.href_parameter):
                if old_name in param.class_references:
                    param.replace_class_reference(old_name, new_name, (new_name,))

    def _rename_with_cascade(self, old_name: str, new_name: str) -> None:
        """
        Rename *old_name* to *new_name* and cascade the rename to all classes whose
        unqualified name starts with the old unqualified name (e.g. renaming FooGet → Foo
        also renames FooGetBar → FooBar).
        """
        old_class = old_name.split('%')[-1]
        new_class = new_name.split('%')[-1]
        self._apply_class_rename(old_name, new_name)
        for sub_old in sorted(self._classes):
            sub_class = sub_old.split('%')[-1]
            if not sub_class.startswith(old_class):
                continue
            sub_suffix = sub_class[len(old_class) :]
            sub_new_class = f'{new_class}{sub_suffix}'
            context, sep, _ = sub_old.rpartition('%')
            sub_new = f'{context}{sep}{sub_new_class}'
            if sub_new in self._classes:
                continue
            self._apply_class_rename(sub_old, sub_new)

    def _strip_verb_affixes_from_all_models(self) -> None:
        """
        Apply _strip_model_name to every class in the registry, repeating until stable.

        Multiple passes are needed because a cascade rename can produce new names that
        themselves benefit from stripping (e.g. FooGetCriteriaObject → FooGetCriteria after
        cascade, then → FooCriteria on the next pass once FooGet → Foo is processed).
        """
        changed = True
        while changed:
            changed = False
            for old_name in sorted(self._classes):
                if old_name not in self._classes:
                    continue  # was renamed by a cascade in this pass
                new_name = _strip_model_name(old_name)
                if new_name == old_name or new_name in self._classes:
                    continue
                old_class = old_name.split('%')[-1]
                new_class = new_name.split('%')[-1]
                log.info(f'strip_verb_affixes: {old_class} → {new_class}')
                self._rename_with_cascade(old_name, new_name)
                changed = True

    def consolidate_resource_models(self) -> None:
        """
        URL-based resource model consolidation.

        Groups endpoints by their resource base URL (stripping the trailing /{param} segment),
        then within each group merges operation-specific body models (e.g. PostFooObject,
        ModifyFooObject) into the canonical model for the group (preferring the single-item GET
        response model, falling back to the model with the most attributes).

        Body models do NOT need to be strict subsets of the canonical — any fields missing from
        the canonical are added to it (union expansion). A 20 % field-overlap threshold is used
        as a safety check to avoid merging unrelated models.

        The merged models' field sets are registered as post_include_sets / put_include_sets on
        the canonical so that post() / put() methods are emitted with correct include filters.
        Endpoints are remapped to the canonical and the now-redundant models are removed.

        Safety constraint: a model is only consolidated if it is never used as a *result* type
        (response) in the group — remapping result types would break response deserialisation.

        Must run before normalize() while class names are still qualified.
        """

        def resource_base(url: str) -> str:
            """Strip trailing /{param} to get the collection/resource URL."""
            normalised = re.sub(r'\{[^}]+\}', '{}', url)
            return re.sub(r'/\{\}$', '', normalised)

        # --- group endpoints by resource base URL ---
        resource_groups: dict[str, list[Endpoint]] = defaultdict(list)
        for _, endpoint in self.endpoints():
            resource_groups[resource_base(endpoint.url)].append(endpoint)

        # Build a global set of result classes across ALL groups before any consolidation.
        # A model used as a response type anywhere must never be removed — the per-group
        # result_classes check is not enough because the same model may be a body type in
        # a different group that is processed first.
        global_result_classes: set[str] = set()
        for ep_list in resource_groups.values():
            for ep in ep_list:
                global_result_classes.update(
                    reference for reference in ep.result_class_references if reference in self._classes
                )

        classes_to_remove: set[str] = set()
        consolidated_canonicals: set[str] = set()  # canonicals that absorbed at least one model
        body_to_canonical: dict[str, str] = {}  # removed body class → its canonical (for cross-group fixup)

        for group_eps in resource_groups.values():
            # collect model names referenced in this group, split by role
            body_class_endpoints: dict[str, list[Endpoint]] = defaultdict(list)
            result_classes: set[str] = set()
            single_item_get_result: Optional[str] = None  # preferred canonical

            for ep in group_eps:
                if ep.body_class_name and ep.body_class_name in self._classes:
                    body_class_endpoints[ep.body_class_name].append(ep)
                result_classes.update(
                    reference for reference in ep.result_class_references if reference in self._classes
                )
                if (
                    len(ep.result_class_references) == 1
                    and ep.result == ep.result_referenced_class
                    and ep.result_referenced_class in self._classes
                ):
                    # Single-item GET: method GET and URL ends with /{param}
                    if ep.method.upper() == 'GET' and re.search(r'/\{[^}]+\}$', ep.url):
                        rc = self._classes.get(ep.result_referenced_class)
                        if rc and not rc.is_enum and not rc.alias and rc.attributes:
                            single_item_get_result = ep.result_referenced_class

            all_model_names = set(body_class_endpoints) | result_classes
            if len(all_model_names) < 2:
                continue

            # filter to concrete (non-enum, non-alias) models with attributes
            candidates = {
                name: self._classes[name]
                for name in all_model_names
                if name in self._classes
                and not self._classes[name].is_enum
                and not self._classes[name].alias
                and self._classes[name].attributes
            }
            if len(candidates) < 2:
                continue

            # Prefer single-item GET result as canonical; fall back to largest by field count
            if single_item_get_result and single_item_get_result in candidates:
                canonical_name = single_item_get_result
            else:
                canonical_name = max(candidates, key=lambda n: len(candidates[n].attributes))
            canonical = candidates[canonical_name]
            canonical_fields = frozenset(a.name for a in canonical.attributes)

            for small_name, small_model in candidates.items():
                if small_name == canonical_name:
                    continue
                # never consolidate a model that is used as a result type anywhere in the spec
                if small_name in global_result_classes:
                    continue
                small_fields = frozenset(a.name for a in small_model.attributes)

                # Safety: require at least 20% field overlap between the body model and canonical
                overlap = len(small_fields & canonical_fields)
                if overlap == 0:
                    continue
                overlap_ratio = overlap / max(len(small_fields), len(canonical_fields))
                if overlap_ratio < 0.2:
                    continue

                # Union expansion: copy fields from body model that are missing from canonical
                missing_fields = small_fields - canonical_fields
                if missing_fields:
                    missing_attrs = [a for a in small_model.attributes if a.name in missing_fields]
                    canonical.attributes = list(canonical.attributes) + missing_attrs
                    canonical_fields = frozenset(a.name for a in canonical.attributes)

                # register include sets and carry over any nested include constraints
                for ep in body_class_endpoints.get(small_name, []):
                    verb = ep.method.upper()
                    if verb == 'POST':
                        if small_fields not in canonical.post_include_sets:
                            canonical.post_include_sets.append(small_fields)
                        for fn, nested in small_model.post_nested_include.items():
                            canonical.post_nested_include.setdefault(fn, nested)
                    elif verb == 'PUT':
                        if small_fields not in canonical.put_include_sets:
                            canonical.put_include_sets.append(small_fields)
                        for fn, nested in small_model.put_nested_include.items():
                            canonical.put_nested_include.setdefault(fn, nested)
                    ep.body_class_name = canonical_name
                    ep.body_method_name = 'post' if verb == 'POST' else 'put'

                classes_to_remove.add(small_name)
                consolidated_canonicals.add(canonical_name)
                body_to_canonical[small_name] = canonical_name

        for name in classes_to_remove:
            self._classes.pop(name, None)
        if classes_to_remove:
            log.info(
                f'consolidate_resource_models: removed {len(classes_to_remove)} redundant models: '
                f'{", ".join(sorted(n.split("%")[-1] for n in classes_to_remove))}'
            )

        # Fix up ALL stale references to removed classes. These go stale when the same body
        # model is used across multiple resource groups — only the first group's endpoints get
        # updated inline; all other references need this second pass.
        # Covers: body_class_name and parameter referenced_class on endpoints, and
        # referenced_class on model attributes.
        if body_to_canonical:
            for _, endpoint in self.endpoints():
                if endpoint.body_class_name and endpoint.body_class_name in body_to_canonical:
                    endpoint.body_class_name = body_to_canonical[endpoint.body_class_name]
                for param in chain(endpoint.body_parameter, endpoint.href_parameter):
                    for referenced_class in param.class_references:
                        if referenced_class not in body_to_canonical:
                            continue
                        new_ref = body_to_canonical[referenced_class]
                        param.replace_class_reference(referenced_class, new_ref, (new_ref,))
            for pc in self._classes.values():
                for attr in pc.attributes or []:
                    for referenced_class in attr.class_references:
                        if referenced_class not in body_to_canonical:
                            continue
                        new_ref = body_to_canonical[referenced_class]
                        attr.replace_class_reference(referenced_class, new_ref, (new_ref,))
                if pc.alias:
                    for referenced_class in pc.alias.class_references:
                        if referenced_class not in body_to_canonical:
                            continue
                        new_ref = body_to_canonical[referenced_class]
                        pc.alias.replace_class_reference(referenced_class, new_ref, (new_ref,))

        # Rename consolidated canonicals: strip leading verb prefix, trailing 'Object', and
        # trailing verb suffix.  Cascade to sub-models whose unqualified name shares the prefix.
        for old_name in sorted(consolidated_canonicals):
            new_name = _strip_model_name(old_name)
            if new_name == old_name or new_name in self._classes:
                continue
            old_class = old_name.split('%')[-1]
            new_class = new_name.split('%')[-1]
            log.info(f'consolidate_resource_models: renaming {old_class} → {new_class}')
            self._rename_with_cascade(old_name, new_name)

    @staticmethod
    def _attributes_from_enum(prop: OASchemaProperty) -> list[Attribute]:
        """
        Create attributes from enum values
        """
        enum_values = prop.enum
        if enum_values is None:
            raise ValueError('enum values cannot be None')
        enum_details = dict(prop.enum_details or [])
        attrs = [
            Attribute(
                name=str(enum_value),
                python_type='str',
                docstring=enum_details.get(str(enum_value)),
                sample=None,
                referenced_class=None,
            )
            for enum_value in enum_values
        ]
        return attrs

    def _add_or_get_type_for_property(
        self, prop: OASchemaProperty, name: str, prop_name: str = '', parent_example: Any = None
    ) -> _ResolvedPythonType:
        """
        Resolve an OpenAPI property to a generated Python type.

        :param prop: OpenAPI schema property to resolve.
        :type prop: OASchemaProperty
        :param name: Owning generated class name.
        :type name: str
        :param prop_name: Property name within the owning class.
        :type prop_name: str
        :param parent_example: Example inherited from a containing parameter.
        :type parent_example: Any
        :return: Python type expression and all generated class references it requires.
        :rtype: _ResolvedPythonType
        :raises ValueError: If a ``oneOf`` or ``anyOf`` is empty or combined with unsupported
            schema-defining fields.
        :raises NotImplementedError: If the property uses another unsupported OpenAPI schema shape.
        """
        if prop.one_of is not None:
            # Resolve oneOf first so schema-defining siblings cannot silently take precedence.
            return self._resolve_one_of_property(prop=prop, name=name, prop_name=prop_name)
        if prop.any_of is not None:
            # anyOf has the same Python acceptance type as oneOf: an ordered Union of alternatives.
            return self._resolve_any_of_property(prop=prop, name=name, prop_name=prop_name)

        try:
            ref = None
            if ref := prop.ref or prop.object_ref:
                # reference to a different schema that (hopefully) will be added to the registry as PythonClass later
                class_name = class_name_from_ref(ref)
                referenced_class_name = self.qualified_class_name(class_name_from_schema_name(class_name))
                # if we have no docstring for the property, we can try to get it from the allOf schema
                if not prop.docstring and prop.all_of:
                    desc_prop = next((p for p in prop.all_of if p.description), None)
                    if desc_prop:
                        prop.description = desc_prop.description
                return _ResolvedPythonType(referenced_class_name, (referenced_class_name,))
        except AttributeError:
            raise

        if prop.enum:
            # create an enum class
            # with the enum values as attributes
            # and use that as the type
            enum_class_name = self.qualified_class_name(sanitize_class_name(f'{name}{sanitize_class_name(prop_name)}'))
            attrs = self._attributes_from_enum(prop)
            python_class = PythonClass(
                name=enum_class_name, attributes=attrs, description=prop.enum_description, is_enum=True, baseclass=None
            )
            # add to registry
            self._add_class(python_class)
            return _ResolvedPythonType(enum_class_name, (enum_class_name,))
        elif prop.type == 'array':
            # array type
            # we need to create a class for the array
            # and use that as the type
            # create class for array
            array_class_name = sanitize_class_name(f'{name}{sanitize_class_name(prop_name)}')
            if not prop.items:
                # fall back to array[string]
                item_type = _ResolvedPythonType('str')
                log.warning(f'No items in array property {prop_name} in {name}. Falling back to array[string]')
            else:
                item_type = self._add_or_get_type_for_property(prop.items, array_class_name, 'item')
            return _ResolvedPythonType(
                python_type=f'list[{item_type.python_type}]',
                referenced_classes=item_type.referenced_classes,
            )
        elif self._is_simple_type(prop_type := prop.type):
            example = prop.example or parent_example
            if prop_type == 'number' and isinstance(example, int):
                # 'number' actually should be 'integer' if the example is an integer
                msg = (
                    f'Changing type "number" to "integer" for {name.split("%")[-1]}.{prop_name} '
                    f'based on example "{example}"'
                )
                log.info(msg)
                prop_type = 'integer'
            elif prop_type == 'string' and isinstance(example, str) and is_datetime(example):
                msg = (
                    f'Changing type "string" to "datetime" for {name.split("%")[-1]}.{prop_name} '
                    f'based on example "{example}"'
                )
                log.info(msg)
                prop_type = 'datetime'
            return _ResolvedPythonType(self._schema_type_to_python_type(prop_type))
        elif prop.type == 'object':
            # create class for object
            if not prop.properties:
                # empty object
                return _ResolvedPythonType('dict')
            object_class_name = sanitize_class_name(f'{name}{sanitize_class_name(prop_name)}')
            object_class_name = self.qualified_class_name(object_class_name)  # type: ignore[assignment]
            self._add_object_schema(object_class_name, prop)
            return _ResolvedPythonType(object_class_name, (object_class_name,))
        elif not prop.model_fields_set:
            # This is an empty property
            # for code generation we will use 'Any' as the type
            log.warning(f'Empty property {prop_name} in {name}')
            return _ResolvedPythonType('Any')
        else:
            raise NotImplementedError(f'Need to handle property {prop_name} in {name}: {prop}')

    def _resolve_one_of_property(self, *, prop: OASchemaProperty, name: str, prop_name: str) -> _ResolvedPythonType:
        """
        Resolve a nested ``oneOf`` property to an ordered Python ``Union``.

        :param prop: Property carrying the ``oneOf`` alternatives.
        :type prop: OASchemaProperty
        :param name: Owning generated class name.
        :type name: str
        :param prop_name: Property name within the owning class.
        :type prop_name: str
        :return: Ordered union type and all generated class references used by its alternatives.
        :rtype: _ResolvedPythonType
        :raises ValueError: If the union is empty or has schema-defining siblings that cannot be combined safely.
        """
        return self._resolve_union_property(
            prop=prop,
            alternatives=prop.one_of,
            name=name,
            prop_name=prop_name,
            composition_name='oneOf',
            composition_field='one_of',
            option_suffix='OneOf',
        )

    def _resolve_any_of_property(self, *, prop: OASchemaProperty, name: str, prop_name: str) -> _ResolvedPythonType:
        """
        Resolve a nested ``anyOf`` property to an ordered Python ``Union``.

        Alternatives with the same primitive schema type retain the historical single-type
        annotation instead of introducing enum classes or a redundant union.

        :param prop: Property carrying the ``anyOf`` alternatives.
        :type prop: OASchemaProperty
        :param name: Owning generated class name.
        :type name: str
        :param prop_name: Property name within the owning class.
        :type prop_name: str
        :return: Ordered union type and all generated class references used by its alternatives.
        :rtype: _ResolvedPythonType
        :raises ValueError: If the union is empty or has schema-defining siblings that cannot be combined safely.
        """
        return self._resolve_union_property(
            prop=prop,
            alternatives=prop.any_of,
            name=name,
            prop_name=prop_name,
            composition_name='anyOf',
            composition_field='any_of',
            option_suffix='AnyOf',
            collapse_same_simple_type=True,
        )

    def _resolve_union_property(
        self,
        *,
        prop: OASchemaProperty,
        alternatives: Optional[list[OASchemaProperty]],
        name: str,
        prop_name: str,
        composition_name: str,
        composition_field: str,
        option_suffix: str,
        collapse_same_simple_type: bool = False,
    ) -> _ResolvedPythonType:
        """
        Resolve an OpenAPI composition keyword to an ordered Python ``Union``.

        :param prop: Property carrying the composition alternatives and metadata.
        :type prop: OASchemaProperty
        :param alternatives: Ordered Schema Objects declared by the composition keyword.
        :type alternatives: Optional[list[OASchemaProperty]]
        :param name: Owning generated class name.
        :type name: str
        :param prop_name: Property name within the owning class.
        :type prop_name: str
        :param composition_name: OpenAPI keyword used in diagnostics, such as ``oneOf``.
        :type composition_name: str
        :param composition_field: Pydantic model field corresponding to the OpenAPI keyword.
        :type composition_field: str
        :param option_suffix: Stable suffix used to name inline object alternatives.
        :type option_suffix: str
        :param collapse_same_simple_type: Whether identical primitive alternatives collapse to one type.
        :type collapse_same_simple_type: bool
        :return: Ordered union type and all generated class references used by its alternatives.
        :rtype: _ResolvedPythonType
        :raises ValueError: If the union is empty or has schema-defining siblings that cannot be combined safely.
        """
        context = '.'.join(part for part in (name.split('%')[-1], prop_name) if part)
        if not alternatives:
            raise ValueError(f'{context}: {composition_name} must contain at least one alternative')

        # Metadata may accompany a composition keyword, but another schema-defining keyword would mean an
        # intersection that cannot be represented by a plain Python Union.
        metadata_fields = {
            composition_field,
            'description',
            'title',
            'nullable',
            'deprecated',
            'discriminator',
            'example',
            'default',
            'read_only',
        }
        unsupported_fields = sorted(prop.model_fields_set - metadata_fields)
        if unsupported_fields:
            raise ValueError(
                f'{context}: {composition_name} cannot be combined with schema-defining fields: '
                f'{", ".join(unsupported_fields)}'
            )

        if collapse_same_simple_type:
            schema_type = alternatives[0].type
            if (
                isinstance(schema_type, str)
                and self._is_simple_type(schema_type)
                and all(option.type == schema_type for option in alternatives)
            ):
                return _ResolvedPythonType(self._schema_type_to_python_type(schema_type))

        option_types: list[str] = []
        referenced_classes: list[str] = []
        for index, option in enumerate(alternatives, start=1):
            # The suffix gives inline object alternatives stable, collision-free generated names.
            option_prop_name = f'{prop_name}{option_suffix}{index}' if prop_name else f'{option_suffix}{index}'
            resolved_option = self._add_or_get_type_for_property(option, name, option_prop_name)
            if resolved_option.python_type not in option_types:
                option_types.append(resolved_option.python_type)
            for referenced_class in resolved_option.referenced_classes:
                if referenced_class not in referenced_classes:
                    referenced_classes.append(referenced_class)

        python_type = option_types[0] if len(option_types) == 1 else f'Union[{", ".join(option_types)}]'
        return _ResolvedPythonType(python_type=python_type, referenced_classes=tuple(referenced_classes))

    @staticmethod
    def _schema_type_to_python_type(schema_type: str) -> str:
        mapping = {'string': 'str', 'integer': 'int', 'number': 'int', 'boolean': 'bool', 'datetime': 'datetime'}
        python_type = mapping.get(schema_type)
        return python_type or schema_type

    @staticmethod
    def _is_simple_type(schema_type: str) -> bool:
        return schema_type in ['string', 'integer', 'number', 'boolean']

    def _add_object_schema(self, schema_name: str, schema: OASchemaProperty) -> None:
        """
        Add an object schema to the registry as a generated Python class.

        :param schema_name: Name to use for the generated class.
        :type schema_name: str
        :param schema: OpenAPI object schema to convert.
        :type schema: OASchemaProperty
        :return: None.
        """
        name = self.qualified_class_name(class_name_from_schema_name(schema_name))
        schema_description = schema.description
        attrs = []
        for prop_name, prop in schema.properties.items():
            # prop_name might be something like 't38FaxCompressionEnabled `true`'
            # we only want to consider the part before the space
            actual_prop_name = prop_name
            if '`' in prop_name:
                m = re.match(r"""[^`]+""", prop_name)
                actual_prop_name = m.group(0).strip()
            if actual_prop_name != prop_name:
                log.warning(f'Property name {prop_name} in {name} contains value, using {actual_prop_name} instead')
                prop_name = actual_prop_name
            resolved_type = self._add_or_get_type_for_property(prop, name, prop_name)
            attr = Attribute(
                name=prop_name,
                python_type=resolved_type.python_type,
                docstring=prop.docstring,
                sample=None,
                referenced_class=resolved_type.primary_reference,
                referenced_classes=resolved_type.referenced_classes,
            )
            attrs.append(attr)
        python_class = PythonClass(
            name=name, attributes=attrs, description=schema_description, is_enum=False, baseclass=None
        )
        # add to registry
        self._add_class(python_class)

    def _add_schema(self, schema_name: str, schema: OASchemaProperty) -> None:
        """
        Add a component schema and any required top-level alias to the registry.

        :param schema_name: Component schema name.
        :type schema_name: str
        :param schema: OpenAPI schema to add.
        :type schema: OASchemaProperty
        :return: None.
        """
        resolved_type = self._add_or_get_type_for_property(schema, sanitize_class_name(schema_name))
        """
            For a schema like:
                "LocationListResponse": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "required": [
                        "id",
                        "name"
                      ]
            _add_schema returns:
                * 'list[None%LocationListResponseItem]'
                * 'None%LocationListResponseItem'

            we probably need to create a dummy for LocationListResponse
        """
        referenced_class = resolved_type.primary_reference
        if (
            referenced_class
            and (unqualified_ref := referenced_class.split('%')[-1]) != schema_name
            and unqualified_ref.endswith('Item')
        ):
            # this is a list of items, we need to create a dummy class for the list
            # so that we can use it as a type
            alias_attribute = Attribute(
                name='alias',
                python_type=resolved_type.python_type,
                referenced_class=referenced_class,
                referenced_classes=resolved_type.referenced_classes,
            )
            dummy_class_name = self.qualified_class_name(snake_case(schema_name))
            dummy_class = PythonClass(name=dummy_class_name, alias=alias_attribute)
            self._add_class(dummy_class)
        elif schema.type == 'object' and not schema.properties:
            # References to schema-free object components still name the component. Register
            # a private alias so normalization can replace those references with ``dict``.
            alias_attribute = Attribute(name='alias', python_type=resolved_type.python_type)
            dummy_class_name = self.qualified_class_name(snake_case(schema_name))
            dummy_class = PythonClass(name=dummy_class_name, alias=alias_attribute)
            self._add_class(dummy_class)
        return

    def _parameter_from_schema_property(
        self,
        *,
        prop_name: str,
        prop: OASchemaProperty,
        param_required: Optional[set[str]] = None,
        url_parameter: bool = False,
    ) -> Parameter:
        """
        Create an endpoint parameter from an OpenAPI schema property.

        :param prop_name: Parameter/property name.
        :type prop_name: str
        :param prop: OpenAPI schema property describing the parameter.
        :type prop: OASchemaProperty
        :param param_required: Names required by the containing object schema.
        :type param_required: Optional[set[str]]
        :param url_parameter: Whether the value is interpolated into the URL.
        :type url_parameter: bool
        :return: Generated endpoint parameter with complete class-reference metadata.
        :rtype: Parameter
        """
        param_required = param_required or prop.required and set(prop.required) or {}  # type: ignore[assignment]
        required = param_required and prop_name in param_required
        resolved_type = self._add_or_get_type_for_property(prop, prop_name)
        return Parameter(
            name=prop_name,
            python_type=resolved_type.python_type,
            referenced_class=resolved_type.primary_reference,
            docstring=prop.docstring,
            sample=prop.example,
            optional=not required,
            url_parameter=url_parameter,
            registry=self,
            referenced_classes=resolved_type.referenced_classes,
        )

    def _parameter_from_oa_parameter(self, param: OAParameter) -> Parameter:
        """
        Create a generated endpoint parameter from an OpenAPI Parameter Object.

        :param param: OpenAPI parameter to convert.
        :type param: OAParameter
        :return: Generated endpoint parameter with complete class-reference metadata.
        :rtype: Parameter
        """
        resolved_type = self._add_or_get_type_for_property(param.schema_, param.name, parent_example=param.example)
        return Parameter(
            name=param.name,
            python_type=resolved_type.python_type,
            referenced_class=resolved_type.primary_reference,
            docstring=param.description,
            sample=param.example,
            optional=not param.required,
            url_parameter=param.in_ == 'path',
            registry=self,
            referenced_classes=resolved_type.referenced_classes,
        )

    def _dereference_request_body(self, spec: OASpec, request_body: Optional[OARequestBody]) -> Optional[OARequestBody]:
        """
        Resolve a component request body reference before request body code generation.

        :param spec: OpenAPI specification that owns the referenced request body component.
        :type spec: OASpec
        :param request_body: Operation request body selected for body parameter generation.
        :type request_body: Optional[OARequestBody]
        :return: Concrete request body object, or ``None`` when the operation has no request body.
        :rtype: Optional[OARequestBody]
        :raises ValueError: If the reference does not resolve to a request body component.
        """
        if request_body is None or not request_body.ref:
            return request_body
        dereferenced = spec.deref(request_body.ref)
        if not isinstance(dereferenced, OARequestBody):
            raise ValueError(f'Request body reference {request_body.ref} did not resolve to a request body')
        return dereferenced

    def _raw_body_properties(self, spec: OASpec, operation: OAOperation) -> Optional[dict[str, 'OASchemaProperty']]:
        """
        Return the raw OAS property dict for the request body schema, or None if there is no body.

        Used to inspect nested schema structures without going through Parameter conversion.

        :param spec: OpenAPI specification that owns the operation and any request body references.
        :type spec: OASpec
        :param operation: Operation whose request body should be inspected.
        :type operation: OAOperation
        :return: Raw schema properties from the request body, or ``None`` if no body schema is available.
        :rtype: Optional[dict[str, OASchemaProperty]]
        :raises ValueError: If the operation's request body reference does not resolve to a request body.
        """
        if not (req_body := self._dereference_request_body(spec, operation.request_body)):
            return None
        if not (content := req_body.content):
            return None
        content_type = next(iter(content))
        body_content = content[content_type]
        if not (body_schema := body_content.schema_):
            return None
        if ref := body_schema.ref or body_schema.object_ref:
            class_spec = spec.get_schema(ref)
            return class_spec.properties if class_spec else None
        return body_schema.properties

    def _body_parameter_from_operation(self, spec: OASpec, operation: OAOperation) -> list[Parameter]:
        """
        Create request body parameters from an OpenAPI operation.

        :param spec: OpenAPI specification that owns the operation and any referenced request body schemas.
        :type spec: OASpec
        :param operation: Operation whose request body should be converted to SDK method parameters.
        :type operation: OAOperation
        :return: SDK method parameters derived from the operation request body.
        :rtype: list[Parameter]
        :raises ValueError: If the request body has multiple content types, lacks a schema, or references an unknown
            schema or request body component.
        """
        if not (req_body := self._dereference_request_body(spec, operation.request_body)):
            return []
        if not (content := req_body.content):
            return []
        if len(content) > 1:
            raise ValueError('Only one content type supported')
        content_type = next(iter(content))
        body_content = content[content_type]
        if not (body_schema := body_content.schema_):
            raise ValueError('No schema in request body')
        if ref := body_schema.ref or body_schema.object_ref:
            # reference to a different schema that (hopefully) will be added to the registry as PythonClass later
            class_name = class_name_from_ref(ref)
            # find the schema in the registry
            class_spec = spec.get_schema(ref)
            if not class_spec:
                raise ValueError(f'Referenced schema {class_name}/{ref} not found')
            # now we can create the parameter list from the referenced schema
            param_properties = class_spec.properties
            param_required: set[str] = class_spec.required and set(class_spec.required) or {}  # type: ignore[assignment]
        else:
            # create parameter list from schema properties
            param_properties = body_schema.properties
            param_required = body_schema.required and set(body_schema.required) or {}  # type: ignore[assignment]
        # create parameter list
        parameters = [
            self._parameter_from_schema_property(prop_name=prop_name, prop=prop, param_required=param_required)
            for prop_name, prop in param_properties.items()
        ]
        return parameters

    def _dereference_response(self, spec: OASpec, response: Optional[OAResponse]) -> Optional[OAResponse]:
        """
        Resolve a component response reference before endpoint return type generation.

        :param spec: OpenAPI specification that owns the referenced response component.
        :type spec: OASpec
        :param response: Operation response selected for return type generation.
        :type response: Optional[OAResponse]
        :return: Concrete response object, or ``None`` when no response was selected.
        :rtype: Optional[OAResponse]
        :raises ValueError: If the reference does not resolve to a response component.
        """
        if response is None or not response.ref:
            return response
        dereferenced = spec.deref(response.ref)
        if not isinstance(dereferenced, OAResponse):
            raise ValueError(f'Response reference {response.ref} did not resolve to a response')
        return dereferenced

    def _endpoint_from_operation(
        self, spec: OASpec, operation: OAOperation, host: str, path: str, method: str
    ) -> Endpoint:
        """
        Create an SDK endpoint from an OpenAPI operation.

        DELETE operations without a documented successful response are treated as returning an empty
        ``204 No Content`` response. This fallback leaves the parsed OpenAPI document unchanged and emits a warning.

        :param spec: OpenAPI specification containing the operation and referenced components.
        :type spec: OASpec
        :param operation: Operation to convert into an SDK endpoint.
        :type operation: OAOperation
        :param host: Base URL for the generated endpoint.
        :type host: str
        :param path: URL path for the generated endpoint.
        :type path: str
        :param method: HTTP method for the generated endpoint.
        :type method: str
        :return: Generated endpoint metadata.
        :rtype: Endpoint
        :raises ValueError: If request or response metadata is unsupported, including a non-DELETE operation without
            a successful response.

        This method may register generated request or response model classes in the registry.
        """
        endpoint_name = snake_case(operation.operation_id)
        method = method
        host = host
        url = path
        title = operation.summary
        docstring = operation.description

        href_parameter = [self._parameter_from_oa_parameter(qp) for qp in operation.parameters if not qp.is_auth]

        body_parameter = self._body_parameter_from_operation(spec, operation)

        body_class_name = None
        body_class_include = None
        body_method_name = 'post'
        registry = self

        # For POST and PUT endpoints: check whether the body parameters are a subset of a registered model.
        # If so, use the model as the single body argument (instead of individual parameters).
        # POST → model.post()   PUT → model.put()
        # Skipped entirely when body_style is 'args'.
        if self.body_style != 'args' and method.upper() in ('POST', 'PUT') and len(body_parameter) > 1:
            body_field_names = frozenset(p.name for p in body_parameter)
            matched_model: Optional[str] = None
            for class_name, python_class in self._classes.items():
                if python_class.is_enum or python_class.alias or not python_class.attributes:
                    continue
                model_field_names = frozenset(a.name for a in python_class.attributes)
                if body_field_names <= model_field_names:
                    matched_model = class_name
                    break

            if matched_model:
                model_class = self._classes[matched_model]
                include_set = body_field_names
                if method.upper() == 'POST':
                    body_method_name = 'post'
                    if include_set not in model_class.post_include_sets:
                        model_class.post_include_sets.append(include_set)
                else:  # PUT
                    body_method_name = 'put'
                    if include_set not in model_class.put_include_sets:
                        model_class.put_include_sets.append(include_set)
                body_class_name = matched_model
                body_class_include = include_set
                if self.body_style != 'hybrid':
                    # in hybrid mode body_parameter is kept so it can serve as fallback kwargs
                    body_parameter = []
                else:
                    # in hybrid mode all body params are optional (settings takes priority when provided)
                    for p in body_parameter:
                        p.optional = True

                # Check nested models: if the body schema defines fewer fields for a list/object
                # attribute than the registered model, register a nested include constraint.
                raw_props = self._raw_body_properties(spec, operation)
                if raw_props:
                    nested_include: dict[str, frozenset[str]] = {}
                    attr_by_oas_name = {a.name: a for a in model_class.attributes}
                    for field_name in include_set:
                        body_prop = raw_props.get(field_name)
                        if body_prop is None:
                            continue
                        attr = attr_by_oas_name.get(field_name)
                        if attr is None or len(attr.class_references) != 1:
                            continue
                        # Resolve the referenced class name (strip qualification prefix)
                        ref_class_name = attr.class_references[0]
                        nested_model = self._classes.get(ref_class_name)
                        if nested_model is None or nested_model.is_enum or not nested_model.attributes:
                            continue
                        nested_model_fields = frozenset(a.name for a in nested_model.attributes)
                        # Determine which fields the body schema provides for this nested type
                        if body_prop.type == 'array' and body_prop.items:
                            items = body_prop.items
                            if items.ref or items.object_ref:
                                # $ref to the same model — all fields; no restriction needed
                                body_nested_fields = nested_model_fields
                            elif items.properties:
                                body_nested_fields = frozenset(items.properties.keys())
                            else:
                                body_nested_fields = nested_model_fields
                        elif body_prop.type == 'object' and body_prop.properties:
                            body_nested_fields = frozenset(body_prop.properties.keys())
                        else:
                            body_nested_fields = nested_model_fields
                        # Only register if the body defines a strict subset of the model's fields
                        if body_nested_fields < nested_model_fields:
                            nested_include[field_name] = body_nested_fields

                    if nested_include:
                        target = (
                            model_class.post_nested_include
                            if method.upper() == 'POST'
                            else model_class.put_nested_include
                        )
                        target.update(nested_include)

        response_code, response = next(
            ((rc, content) for rc, content in operation.responses.items() if rc.startswith('2')), (None, None)
        )
        if response_code is None and method.upper() == 'DELETE':
            # Some upstream DELETE specs document only error responses even though the endpoint succeeds without a body.
            log.warning(f'No 2xx response defined for DELETE endpoint {endpoint_name}; assuming 204 No Content')
            response_code = '204'
        response = self._dereference_response(spec, response)

        response_ct, response_content = next(iter(response.content.items()), (None, None)) if response else (None, None)
        if not (response_ct and response_content):
            if response_code == '200':
                log.warning(f'No content in 200 response for {endpoint_name}')
            response_body = None
            result = None
            result_referenced_class = None
            result_referenced_classes: tuple[str, ...] = ()
            if response_code not in {'204', '201', '202', '200'}:
                raise ValueError(f'unexpected response code {response_code} for {endpoint_name}')
        else:
            response_content: OAContent  # type: ignore[no-redef]
            # response body is an example
            response_body = response_content.example
            response_schema = response_content.schema_
            if response_schema is None:
                # if no schema is provided, we can't do much. For now we just issue a warning
                log.warning(f'No schema in response for {endpoint_name}')
                result = None
                result_referenced_class = None
                result_referenced_classes = ()
            else:
                resolved_result = self._add_or_get_type_for_property(
                    response_schema, endpoint_name, prop_name='Response'
                )
                result = resolved_result.python_type
                result_referenced_class = resolved_result.primary_reference
                result_referenced_classes = resolved_result.referenced_classes

        endpoint = Endpoint(
            name=endpoint_name,
            method=method,
            host=host,
            url=url,
            title=title,
            docstring=docstring,
            href_parameter=href_parameter,
            body_parameter=body_parameter,
            body_class_name=body_class_name,
            body_class_include=body_class_include,
            body_method_name=body_method_name,
            body_style=self.body_style if body_class_name else 'args',
            response_body=response_body,
            result=result,
            result_referenced_class=result_referenced_class,
            result_referenced_classes=result_referenced_classes,
            registry=registry,
        )
        return endpoint

    def add_open_api(self, spec_info: OpenApiSpecInfo):
        """
        Add classes from given OpenApiSpecInfo
        """
        with open(spec_info.spec_path) as f:
            data = json.load(f)
        open_api_spec = OASpec.model_validate(data)
        # dereference all parameters defined as $ref
        open_api_spec.deref_parameters()
        # clean up schemas with one_of definition
        open_api_spec.unify_one_of_schemas()

        # add PythonAPI instance
        host = open_api_spec.servers and open_api_spec.servers[0].url
        if not host:
            log.warning(f'OpenAPI spec {spec_info.spec_path} has no host')
            host = 'http://host/'

        python_api = PythonAPI(title=open_api_spec.info.title, docstring=open_api_spec.info.description, host=host)
        self._add_api(python_api=python_api)

        # add data structures : PythonClass instances
        # data structures are in components.schemas
        for schema_name, schema in open_api_spec.components.schemas.items():
            self._add_schema(schema_name, schema)
        # add endpoints
        for path, method, operation in open_api_spec.operations():
            endpoint = self._endpoint_from_operation(open_api_spec, operation, host, path, method)
            python_api.add_endpoint(endpoint)
        return

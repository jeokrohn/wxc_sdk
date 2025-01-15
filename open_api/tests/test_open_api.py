"""
Tests for OpenAPI specs
"""
import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import reduce
from itertools import chain
from typing import ClassVar, Iterable
from unittest import TestCase

import yaml
from docutils.nodes import description

from open_api.open_api_class_registry import OpenApiPythonClassRegistry
from open_api.open_api_model import OpenAPISpec, OpenApiSpecSchemaProperty
from open_api.open_api_sources import open_api_specs, OpenApiSpecInfo


def read_one_spec_from_file(spec: OpenApiSpecInfo) -> OpenAPISpec:
    """
    Read one OpenAPI spec from file
    """
    with open(spec.spec_path) as f:
        data = json.load(f)
    parsed_spec = OpenAPISpec.model_validate(data)
    return parsed_spec


class TestOpenApiSpecs(TestCase):
    def test_all_api_specs(self):
        """
        print some info about all OpenAPI specs
        """
        print()
        for spec in sorted(open_api_specs(), key=lambda s: (s.api_name, s.version)):
            print(f'{spec.api_name}, {spec.version}, {spec.spec_path=}')


class TestParseOpenApi(TestCase):
    """
    Test parsing OpenAPI specs
    """

    def test_read_all(self):
        parsed_open_api_specs = list(map(read_one_spec_from_file, open_api_specs()))
        print()
        print(f'Parsed {len(parsed_open_api_specs)} OpenAPI specs')
        parsed_open_api_specs.sort(key=lambda spec: spec.info.title)
        print('\n'.join(spec.info.title for spec in parsed_open_api_specs))


@dataclass(init=False, repr=False)
class WithOpenApiSpecInfos(TestCase):
    spec_infos: ClassVar[list[OpenApiSpecInfo]]

    @classmethod
    def setUpClass(cls):
        """
        Read all OpenAPI spec infos
        """
        super().setUpClass()
        cls.spec_infos = list(open_api_specs())


@dataclass(init=False, repr=False)
class WithParsedOpenApiSpecs(WithOpenApiSpecInfos):
    parsed_specs: ClassVar[list[OpenAPISpec]]

    @classmethod
    def setUpClass(cls):
        """
        Read all OpenAPI specs
        """
        super().setUpClass()
        cls.parsed_specs = list(map(read_one_spec_from_file, cls.spec_infos))


class TestCreateYAML(WithOpenApiSpecInfos):
    """
    Create a YAML for all OpenAPI spec JSON files
    """

    def test_001_create_all_yml(self):
        for spec in self.spec_infos:
            yml_path = spec.spec_path.replace('.json', '.yml')
            with open(spec.spec_path) as f:
                data = json.load(f)
            with open(yml_path, 'w') as f:
                yaml.safe_dump(data, f)

    def test_002_delete_all_yml(self):
        for spec in self.spec_infos:
            yml_path = spec.spec_path.replace('.json', '.yml')
            if os.path.exists(yml_path):
                os.remove(yml_path)


class TestParsedOpenApiSpecs(WithParsedOpenApiSpecs):
    """
    Test assumptions about parsed OpenAPI specs
    """

    def all_schemas(self) -> Iterable[tuple[OpenApiSpecInfo, str, OpenApiSpecSchemaProperty]]:
        """
        Generator of all schemas with api_name and name
        """
        return chain.from_iterable(((spec_info, name, schema)
                                    for name, schema in spec.components.schemas.items())
                                   for spec_info, spec in zip(self.spec_infos, self.parsed_specs)
                                   if spec.components and spec.components.schemas)

    # noinspection GrazieInspection
    def test_scheme_component_types(self):
        """
        Collect types of components.schemas
        """
        type_counter = Counter(schema.type
                               for _, _, schema in self.all_schemas())
        print()
        for type_, count in sorted(type_counter.items(), key=lambda item: item[1], reverse=True):
            print(f'{type_}: {count}')

    def test_schema_component_type_none(self):
        """
        Understand schema types that are None
        """
        none_schemas = [(api_spec_info, name, schema)
                        for api_spec_info, name, schema in self.all_schemas()
                        if schema.type is None]
        print()
        print(f'None schemas: {len(none_schemas)}')
        for api_spec_info, name, schema in none_schemas:
            api_name = api_spec_info.api_name
            print(f'{api_name=} {name=} {schema=}')

    def test_schema_component_type_string_are_all_enums(self):
        """
        Understand schema types that are "string"; they should be enums
        """
        string_schemas = [(api_spec_info, name, schema)
                          for api_spec_info, name, schema in self.all_schemas()
                          if schema.type == 'string']
        print()
        print(f'"string" schemas: {len(string_schemas)}')
        for api_spec_info, name, schema in string_schemas:
            api_name = api_spec_info.api_name
            print(f'{api_name=} {name=} {schema=}')

        print()
        string_schemas_not_enum = [(api_spec_info, name, schema)
                                   for api_spec_info, name, schema in string_schemas
                                   if schema.enum is None]
        print(f'Not enum: {len(string_schemas_not_enum)}')
        for api_spec_info, name, schema in string_schemas:
            api_name = api_spec_info.api_name
            print(f'{api_name=} {name=} {schema=}')
        self.assertTrue(not string_schemas_not_enum, 'Some "string" schemas are not enums')

    def test_schema_component_type_array(self):
        """
        Understand schema types that are "array"
        """
        array_schemas = [(api_spec_info, name, schema)
                         for api_spec_info, name, schema in self.all_schemas()
                         if schema.type == 'array']
        print()
        print(f'"array" schemas: {len(array_schemas)}')
        for api_spec_info, name, schema in array_schemas:
            api_name = api_spec_info.api_name
            print(f'{api_name=} {name=} {schema=}')

    def test_find_descriptions_with_something_like_properties(self):
        """
        wrong formatting in APIB can lead to properties ending up in descriptions
        """

        # go through all endpoints and schemas and look for "fishy" descriptions
        def check_schema_property(*, property: OpenApiSpecSchemaProperty, path: str):
            if property.description and re.search(r'\s*\+ \S+:', property.description, re.MULTILINE):
                print()
                print(f'{path}: ')
                print(f'{property.description}')
                print('-' * 130)
            if property.items:
                check_schema_property(property=property.items, path=f'{path}.items')
            if property.properties:
                for name, prop in property.properties.items():
                    check_schema_property(property=prop, path=f'{path}.{name}')

        for api_spec_info, name, schema in self.all_schemas():
            check_schema_property(property=schema, path=f'{api_spec_info.rel_spec_path}.{name}')

    def test_object_schema_property_types(self):
        """
        Understand types of properties in object schemas
        """
        object_schemas = [(api_spec_info, name, schema)
                          for api_spec_info, name, schema in self.all_schemas()
                          if schema.type == 'object']
        # group all properties by type
        properties_by_type = reduce(lambda acc, x: acc[x[0]].append(x[1:]) or acc,
                                    ((prop.type, api_spec_info, schema_name, schema, prop_name, prop)
                                     for api_spec_info, schema_name, schema in object_schemas
                                     for prop_name, prop in schema.properties.items()),
                                    defaultdict(list))
        properties_by_type: dict[
            str, list[tuple[OpenApiSpecInfo, str, OpenApiSpecSchemaProperty, str, OpenApiSpecSchemaProperty]]]
        for type_ in sorted(properties_by_type, key=lambda key: len(properties_by_type[key]), reverse=True):
            print()
            print(f'{type_}: {len(properties_by_type[type_])}')
            if type_ == 'array':
                for api_spec_info, schema_name, schema, prop_name, prop in properties_by_type[type_]:
                    items = prop.items
                    api_name = api_spec_info.api_name
                    # items can
                    # - be a reference to another schema
                    # - be an object
                    # - have any_of --> need to understand this better
                    if not items.ref and not (items.type and items.type in {'string', 'object', 'integer'}):
                        if items.any_of:
                            print(f'  {api_name=} {schema_name=} {prop_name} array of any_of:')
                            for item in items.any_of:
                                print(f'    {item}')
                        else:
                            print(f'  {api_name=} {schema_name=} {prop_name} array of {items}')
            elif type_ is None:
                for api_spec_info, schema_name, schema, prop_name, prop in properties_by_type[type_]:
                    api_name = api_spec_info.api_name
                    # property could
                    # - be a reference to another schema
                    # - have an all_of list
                    # - has an example from which we can infer a type
                    if prop.ref or prop.all_of or prop.example:
                        continue
                    print(f'  {api_name=} {schema_name=} {prop_name} {prop}')
            elif type_ == 'object':
                for api_spec_info, schema_name, schema, prop_name, prop in properties_by_type[type_]:
                    api_name = api_spec_info.api_name
                    if prop.properties:
                        continue
                    print(f'  {api_name=} {schema_name=} {prop_name} {prop}')
            elif type_ in {'number', 'integer', 'string', 'boolean'}:
                continue
            else:
                raise ValueError(f'Unknown type {type_}')


class TestPythonClassRegistry(TestCase):
    """
    Test OpenApiPythonClassRegistry used for code generation
    """

    def test_add_classes_from_open_api_spec_info(self):
        registry = OpenApiPythonClassRegistry()
        # test with the call-routing spec
        for spec in open_api_specs():
            if spec.api_name != 'call-routing':
                continue
            registry.add_open_api(spec)
            break

    foo = 1

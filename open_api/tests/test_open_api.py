"""
Tests for OpenAPI specs
"""
import json
from collections import Counter
from dataclasses import dataclass
from itertools import chain
from typing import ClassVar, Iterable
from unittest import TestCase

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
class WithParsedOpenApiSpecs(TestCase):
    spec_infos: ClassVar[list[OpenApiSpecInfo]]
    parsed_specs: ClassVar[list[OpenAPISpec]]

    @classmethod
    def setUpClass(cls):
        """
        Read all OpenAPI specs
        """
        super().setUpClass()
        cls.spec_infos = list(open_api_specs())
        cls.parsed_specs = list(map(read_one_spec_from_file, cls.spec_infos))


class TestParsedOpenApiSpecs(WithParsedOpenApiSpecs):
    """
    Test assumptions about parsed OpenAPI specs
    """
    def all_schemas(self)->Iterable[tuple[str, str, OpenApiSpecSchemaProperty]]:
        """
        Generator of all schemas with api_name and name
        """
        return chain.from_iterable(((spec_info.api_name, name, schema)
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
        none_schemas = [(api_name, name, schema)
                        for api_name, name, schema in self.all_schemas()
                        if schema.type is None]
        print()
        print(f'None schemas: {len(none_schemas)}')
        for api_name, name, schema in none_schemas:
            print(f'{api_name=} {name=} {schema=}')

    def test_schema_component_type_string_are_all_enums(self):
        """
        Understand schema types that are "string"; they should be enums
        """
        string_schemas = [(api_name, name, schema)
                          for api_name, name, schema in self.all_schemas()
                          if schema.type=='string']
        print()
        print(f'"string" schemas: {len(string_schemas)}')
        for api_name, name, schema in string_schemas:
            print(f'{api_name=} {name=} {schema=}')

        print()
        string_schemas_not_enum = [(api_name, name, schema)
                                   for api_name, name, schema in string_schemas
                                   if schema.enum is None]
        print(f'Not enum: {len(string_schemas_not_enum)}')
        for api_name, name, schema in string_schemas:
            print(f'{api_name=} {name=} {schema=}')
        self.assertTrue(not string_schemas_not_enum, 'Some "string" schemas are not enums')

    def test_schema_component_type_array(self):
        """
        Understand schema types that are "array"
        """
        array_schemas = [(api_name, name, schema)
                         for api_name, name, schema in self.all_schemas()
                         if schema.type=='array']
        print()
        print(f'"array" schemas: {len(array_schemas)}')
        for api_name, name, schema in array_schemas:
            print(f'{api_name=} {name=} {schema=}')


class TestPythonClassRegistry(TestCase):
    def test_add_classes_from_open_api_spec_info(self):
        registry = OpenApiPythonClassRegistry()
        for spec in open_api_specs():
            if spec.api_name != 'call-routing':
                continue
            registry.add_classes_from_open_api_spec_info(spec)
            break
    foo = 1

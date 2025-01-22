"""
Tests for OpenAPI specs
"""
import json
import logging
import os
import re
from collections import Counter, defaultdict
from collections.abc import Generator, Callable
from dataclasses import dataclass
from functools import reduce
from typing import ClassVar, Union
from unittest import TestCase

import yaml
from pydantic import ValidationError

from open_api.open_api_class_registry import OpenApiPythonClassRegistry
from open_api.open_api_code_generator import OACodeGenerator
from open_api.open_api_model import OASpec, OASchemaProperty, OAOperation, OAParameter
from open_api.open_api_sources import open_api_specs, OpenApiSpecInfo


def read_one_spec_from_file(spec: OpenApiSpecInfo) -> OASpec:
    """
    Read one OpenAPI spec from file
    """
    with open(spec.spec_path) as f:
        data = json.load(f)
    parsed_spec = OASpec.model_validate(data)
    return parsed_spec


def descend_into_property(*, spec: OASpec, prop: OASchemaProperty, path: str,
                          call_back: Callable[[OASchemaProperty, str], bool] = None,
                          deref: bool = True) -> bool:
    """
    Descend into a property and call callback for each property
    """
    r = call_back(prop, path)

    def descend_into_ref(ref: str) -> bool:
        # check reference and descend in referenced schema
        ref_match = re.match(r'^#/components/schemas/(.+)$', ref)
        if ref_match is None:
            raise ValueError(f'Invalid reference {ref}')
        ref_name = ref_match.group(1)
        ref_schema = spec.components.schemas.get(ref_name)
        if ref_schema is None:
            raise ValueError(f'Unknown reference {ref}')
        if deref:
            return descend_into_property(spec=spec, prop=ref_schema, path=f'{path}(ref {ref})', call_back=call_back,
                                         deref=deref)
        return False

    if prop.ref:
        r = r or descend_into_ref(prop.ref)
    if object_ref := prop.object_ref:
        r = r or descend_into_ref(object_ref)
    if prop.any_of:
        for item in prop.any_of:
            r = r or descend_into_property(spec=spec, prop=item, path=f'{path}.any_of', call_back=call_back,
                                           deref=deref)
    if prop.items:
        # this is an array
        assert prop.type == 'array'
        r = r or descend_into_property(spec=spec, prop=prop.items, path=f'{path}[]', call_back=call_back, deref=deref)
    if prop.properties:
        for name, prop_prop in prop.properties.items():
            r = r or descend_into_property(spec=spec, prop=prop_prop, path=f'{path}.{name}', call_back=call_back,
                                           deref=deref)
    return r


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
        parsed_open_api_specs = []
        err = False
        for spec_info in open_api_specs():
            with open(spec_info.spec_path) as f:
                data = json.load(f)
            print(f'Parsing {spec_info.api_name} {spec_info.version} {spec_info.spec_path}')
            try:
                parsed_spec = OASpec.model_validate(data)
            except ValidationError as e:
                err = True
                print(f'Error parsing {spec_info.api_name} {spec_info.version} {spec_info.spec_path}')
                print(e)
                continue
            parsed_open_api_specs.append(parsed_spec)
            print(f'{spec_info.api_name} {parsed_spec.info.title}')
        print()
        print(f'Parsed {len(parsed_open_api_specs)} OpenAPI specs')
        parsed_open_api_specs.sort(key=lambda spec: spec.info.title)
        print('\n'.join(spec.info.title for spec in parsed_open_api_specs))
        self.assertFalse(err, 'Some OpenAPI specs could not be parsed')


@dataclass(init=False, repr=False)
class WithOpenApiSpecInfos(TestCase):
    spec_infos: ClassVar[list[OpenApiSpecInfo]]

    @classmethod
    def setUpClass(cls):
        """
        Read all OpenAPI spec infos
        """
        super().setUpClass()
        cls.spec_infos = list(sorted(open_api_specs(), key=lambda s: (s.spec_path, s.api_name, s.version)))


@dataclass(init=False, repr=False)
class WithParsedOpenApiSpecs(WithOpenApiSpecInfos):
    parsed_specs: ClassVar[list[OASpec]]

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

    def all_schemas(self) -> Generator[tuple[OpenApiSpecInfo, OASpec, str, OASchemaProperty], None, None]:
        """
        Generator of all schemas with api_name and name
        """
        for spec_info, spec in zip(self.spec_infos, self.parsed_specs):
            if spec.components and spec.components.schemas:
                for name, schema in spec.components.schemas.items():
                    yield spec_info, spec, name, schema

    def all_operations(self) -> Generator[tuple[OpenApiSpecInfo, OASpec, str, str, OAOperation], None, None]:
        for spec_info, spec in zip(self.spec_infos, self.parsed_specs):
            for path, method, operation in spec.operations():
                yield spec_info, spec, path, method, operation

    # noinspection GrazieInspection
    def test_scheme_component_types(self):
        """
        Collect types of components.schemas
        """
        type_counter = Counter(schema.type
                               for _, _, _, schema in self.all_schemas())
        print()
        for type_, count in sorted(type_counter.items(), key=lambda item: item[1], reverse=True):
            print(f'{type_}: {count}')

    def test_schema_component_type_none(self):
        """
        Understand schema types that are None
        """
        errs = []

        def check_none(prop: OASchemaProperty, path: str):
            if prop.any_type is None and not prop.properties and not prop.any_ref and not prop.any_of:
                if prop.example:
                    # if no explicit type is given, we can infer the type from the example
                    example_type = type(prop.example)
                    if example_type in {str, int, float, bool}:  # these are not None
                        return
                errs.append((path, prop))
            return

        for api_spec_info, spec, name, schema in self.all_schemas():
            descend_into_property(spec=spec, prop=schema, path=f'{api_spec_info.rel_spec_path}.{name}',
                                  call_back=check_none, deref=False)
        if errs:
            print('"None" schemas:')
            print('\n'.join(f'{path}: {prop}' for path, prop in errs))

    def test_schema_component_type_string_are_all_enums(self):
        """
        Understand schema types that are "string"; they should be enums
        """
        string_schemas = [(api_spec_info, name, schema)
                          for api_spec_info, _, name, schema in self.all_schemas()
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
                         for api_spec_info, _, name, schema in self.all_schemas()
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

        def check_property(prop: OASchemaProperty, path: str):
            if prop.description and re.search(r'\s*\+ \S+:', prop.description, re.MULTILINE):
                print()
                print(f'{path}: ')
                print(f'{prop.description}')
                print('-' * 130)

        for api_spec_info, spec, name, schema in self.all_schemas():
            descend_into_property(spec=spec, prop=schema, path=f'{api_spec_info.rel_spec_path}.{name}',
                                  call_back=check_property)

    def test_valid_schemas(self):
        """
        Check schema validity
        """
        print()
        errors = []

        def err(si: OpenApiSpecInfo, name: str, schema: OASchemaProperty, msg: str):
            errors.append((si, name, schema))
            print(f'{si.api_name} {name} {msg} {si.rel_spec_path} {schema}')

        for api_spec_info, spec, name, schema in self.all_schemas():
            if schema.type == 'array':
                if not schema.items:
                    errors.append((api_spec_info, name, schema))
                    err(api_spec_info, name, schema, 'array has no items')
                continue
            if schema.type in {'string', 'number', 'integer', 'boolean'}:
                # simple types are ok
                continue
            if schema.ref or schema.object_ref:
                # reference to another schema
                continue
            if schema.type == 'object':
                if not schema.properties:
                    err(api_spec_info, name, schema, 'object has no properties')
                continue
            if schema.properties:
                continue
            err(api_spec_info, name, schema, 'unknown error')
        self.assertTrue(not errors, 'Some schemas have no properties')
        return

    def test_find_broken_responses(self):
        """
        Some responses don't have properties
        """

        errors: list[tuple[str, str]] = []

        def check_empty_property(prop: OASchemaProperty, prop_path: str) -> bool:
            err = None
            if not prop.model_fields_set:
                err = 'Empty property'
            if err:
                errors.append((prop_path, err))
                print(f'{prop_path}: {err}')
                return True
            return False

        print()
        previous_spec_info = None
        err_in_spec = False
        for api_spec_info, parsed_spec, path, method, operation in self.all_operations():
            if previous_spec_info != api_spec_info and err_in_spec:
                print()
                err_in_spec = False
            previous_spec_info = api_spec_info
            for code, response in operation.responses.items():
                if response.content:
                    for content_type, content in response.content.items():
                        ct_path = f'{api_spec_info.rel_spec_path}: {path} {method.upper()}->{code}'
                        if content.schema_:
                            err_in_spec = err_in_spec or descend_into_property(spec=parsed_spec,
                                                                               prop=content.schema_, path=ct_path,
                                                                               call_back=check_empty_property)
                        else:
                            err_str = f'no schema, {content=}'
                            print(f'{ct_path}: {err_str}')
                            errors.append((ct_path, err_str))
                            err_in_spec = True
                        # if
                    # for
                # if
            # for
        # for

        self.assertTrue(not errors, 'Some responses have empty properties')
        return

    def test_object_schema_property_types(self):
        """
        Understand types of properties in object schemas
        """
        object_schemas = [(api_spec_info, name, schema)
                          for api_spec_info, _, name, schema in self.all_schemas()
                          if schema.type == 'object']
        # group all properties by type
        properties_by_type = reduce(lambda acc, x: acc[x[0]].append(x[1:]) or acc,
                                    ((prop.type, api_spec_info, schema_name, schema, prop_name, prop)
                                     for api_spec_info, schema_name, schema in object_schemas
                                     for prop_name, prop in schema.properties.items()),
                                    defaultdict(list))
        properties_by_type: dict[
            Union[str, None], list[tuple[OpenApiSpecInfo, str, OASchemaProperty, str, OASchemaProperty]]]
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

        return

    def test_operation_parameters(self):
        """
        Understand operation parameters
        """
        parameters_in: dict[
            str, list[tuple[OAParameter, OpenApiSpecInfo, OASpec, str, str, OAOperation]]] = defaultdict(list)
        for api_spec_info, parsed_spec, path, method, operation in self.all_operations():
            for param in operation.parameters:
                parameters_in[param.in_].append((param, api_spec_info, parsed_spec, path, method, operation))
        print(f'Possible values for in: {sorted(parameters_in)}')

        return

    def test_operation_request_content_types(self):
        """
        Understand operations request content types
        """
        content_types = defaultdict(list)
        for api_spec_info, parsed_spec, path, method, operation in self.all_operations():
            if not operation.request_body:
                continue
            for content_type, content in operation.request_body.content.items():
                content_types[content_type].append((content, api_spec_info, parsed_spec, path, method, operation))
        foo = 1
        return

    def test_operation_request_body_content(self):
        """
        Understand operations request body content
        """
        err = False
        for api_spec_info, parsed_spec, path, method, operation in self.all_operations():
            if not operation.request_body:
                continue
            for content_type, content in operation.request_body.content.items():
                content_schema = content.schema_
                self.assertIsNotNone(content_schema, 'Missing schema')
                # schema has a ref or a type
                if not content_schema.ref and not content_schema.object_ref and not content_schema.type:
                    print(f'{api_spec_info.rel_spec_path}: {path} {method.upper()} has no type or ref')
                    err = True
                    continue
        self.assertFalse(err)
        return


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
        registry.normalize()


class TestCodeGenerator(TestCase):
    """
    Test CodeGenerator
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('open_api').setLevel(logging.DEBUG)

    def test_read_spec_and_create_source(self):
        code_gen = OACodeGenerator()
        # test with the call-routing spec
        for spec in open_api_specs():
            if spec.api_name != 'call-routing':
                continue
            code_gen.add_open_api_spec(spec)
            break
        code_gen.cleanup()
        source = code_gen.source()
        print(source)

    def test_create_all_sources(self):
        """
        Try to create source for all OpenAPI specs
        """
        print()
        err = None
        for spec in open_api_specs():
            # if spec.api_name != 'dial-number':
            #     continue
            try:
                code_gen = OACodeGenerator()
                code_gen.add_open_api_spec(spec)
                code_gen.cleanup()
                code_gen.source()
            except Exception as e:
                print(f'Error creating source for {spec.api_name} {spec.version} {spec.spec_path}')
                print(f'    {e}')
                err = err or e
        if err:
            raise err

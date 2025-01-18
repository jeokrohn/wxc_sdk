"""
Python class registry for OpenAPI schema; derived from PythonClassRegistry; used for code creation
"""
import json
import re

from apib.python_class import PythonClassRegistry, PythonAPI, PythonClass, Attribute
from apib.tools import sanitize_class_name
from open_api.open_api_model import OpenAPISpec, OpenApiSpecSchemaProperty
from open_api.open_api_sources import OpenApiSpecInfo


def class_name_from_schema_name(schema_name: str) -> str:
    """
    Convert schema name to class name
    """
    return sanitize_class_name(schema_name)


class OpenApiPythonClassRegistry(PythonClassRegistry):
    """
    Registry of classes generated from OpenAPI schema
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def _attributes_from_enum(prop: OpenApiSpecSchemaProperty) -> list[Attribute]:
        """
        Create attributes from enum values
        """
        attrs = [Attribute(name=enum_value, python_type='str', docstring=None, sample=None,
                           referenced_class=None)
                 for enum_value in prop.enum]
        return attrs

    def _add_object_schema(self, schema_name: str, schema: OpenApiSpecSchemaProperty):
        """
        Add "object" schema to registry as Python class
        """
        name = class_name_from_schema_name(schema_name)
        schema_description = schema.description
        attrs = []
        for prop_name, prop in schema.properties.items():
            # create attribute
            if prop.ref:
                # reference to a different schema that (hopefully) will be added to the registry as PythonClass later
                ref_match = re.match(r'#/components/schemas/(.*)', prop.ref)
                if not ref_match:
                    raise ValueError(f'Invalid ref {prop.ref} for property {prop_name} in schema {schema_name}')
                referenced_class_name = class_name_from_schema_name(ref_match.group(1))
                attr = Attribute(name=prop_name,
                                 docstring=prop.description,
                                 python_type=referenced_class_name,
                                 referenced_class=referenced_class_name, sample=None)
                attrs.append(attr)
                continue

            if prop.enum:
                attr = Attribute(name=prop_name, python_type='str', docstring=prop.description, sample=None,
                                 referenced_class=None)
            elif prop.type == 'array':
                # array type
                # we need to create a class for the array
                # and use that as the type
                # create class for array
                array_class_name = f'{name}_{prop_name}'
                array_class = PythonClass(name=array_class_name, attributes=[], description=None, is_enum=False,
                                          baseclass=None)
                self._add_class(array_class)
                attr = Attribute(name=prop_name, python_type=array_class_name, docstring=prop.description,
                                 sample=None,
                                 referenced_class=None)
            else:
                attr = Attribute(name=prop_name, python_type=prop.type, docstring=prop.description, sample=None,
                                 referenced_class=None)
            attrs.append(attr)
        python_class = PythonClass(name=name,
                                   attributes=attrs,
                                   description=schema_description, is_enum=False,
                                   baseclass=None)
        # add to registry
        self._add_class(python_class)

    def _add_schema(self, schema_name: str, schema: OpenApiSpecSchemaProperty):
        """
        Add schema to registry
        """
        # create PythonClass instance
        # we need
        # * name
        # * attributes
        # * description
        # * is_enum
        # * baseclass (None)
        name = class_name_from_schema_name(schema_name)
        if schema.type == 'string':
            if not schema.enum:
                raise ValueError(f'String schema {schema_name} has no enum values')
            is_enum = True
            attrs = self._attributes_from_enum(schema)
            python_class = PythonClass(name=name,
                                       attributes=attrs,
                                       description=schema.description,
                                       is_enum=is_enum,
                                       baseclass=None)
            # add to registry
            self._add_class(python_class)
        elif schema.type == 'object':
            self._add_object_schema(schema_name, schema)
        elif schema.type == 'array':
            raise NotImplementedError(f'Array schema {schema_name} not implemented')
        elif schema.type is None:
            raise NotImplementedError(f'None schema {schema_name} not implemented')
        else:
            raise ValueError(f'Unknown schema type {schema.type} for schema {schema_name}')

    def add_open_api(self, spec_info: OpenApiSpecInfo):
        """
        Add classes from given OpenApiSpecInfo
        """
        with open(spec_info.spec_path) as f:
            data = json.load(f)
        open_api_spec = OpenAPISpec.model_validate(data)

        # add PythonAPI instance
        host = open_api_spec.servers and open_api_spec.servers[0].url
        if not host:
            raise ValueError(f'OpenAPI spec {spec_info.spec_path} has no host')

        python_api = PythonAPI(title=open_api_spec.info.title, docstring=open_api_spec.info.description, host=host)
        self._add_api(python_api=python_api)

        # add data structures : PythonClass instances
        # data structures are in components.schemas
        for schema_name, schema in open_api_spec.components.schemas.items():
            self._add_schema(schema_name, schema)
        # add endpoints
        raise NotImplementedError()

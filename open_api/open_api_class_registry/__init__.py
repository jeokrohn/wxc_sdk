"""
Python class registry for OpenAPI schema; derived from PythonClassRegistry; used for code creation
"""
import json
import re
from typing import Optional

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

    def _add_or_get_type_for_property(self, prop: OpenApiSpecSchemaProperty, name: str, prop_name: str = '') -> tuple[
        str, str]:
        """
        Add or get type for property
        :return: python_type and referenced_class
        """
        if (ref := prop.ref or prop.object_ref):
            # reference to a different schema that (hopefully) will be added to the registry as PythonClass later
            ref_match = re.match(r'#/components/schemas/(.*)', ref)
            if not ref_match:
                raise ValueError(f'Invalid ref {prop.ref} for {name}')
            referenced_class_name = self.qualified_class_name(class_name_from_schema_name(ref_match.group(1)))
            return referenced_class_name, referenced_class_name

        if prop.enum:
            # create an enum class
            # with the enum values as attributes
            # and use that as the type
            enum_class_name = self.qualified_class_name(sanitize_class_name(f'{name}{sanitize_class_name(prop_name)}'))
            attrs = self._attributes_from_enum(prop)
            python_class = PythonClass(name=enum_class_name, attributes=attrs, description=prop.description,
                                       is_enum=True, baseclass=None)
            # add to registry
            self._add_class(python_class)
            return enum_class_name, enum_class_name
        elif prop.type == 'array':
            # array type
            # we need to create a class for the array
            # and use that as the type
            # create class for array
            array_class_name = sanitize_class_name(f'{name}{sanitize_class_name(prop_name)}')
            schema_type, referenced_class = self._add_or_get_type_for_property(prop.items, array_class_name)
            python_type = f'list[{self._schema_type_to_python_type(schema_type)}]'
            referenced_class = self._class_reference(referenced_class)
            return python_type, referenced_class
        elif self._is_simple_type(prop.type):
            return self._schema_type_to_python_type(prop.type), None
        elif prop.type == 'object':
            # create class for object
            if not prop.properties:
                # empty object
                return 'dict', None
            object_class_name = sanitize_class_name(f'{name}{sanitize_class_name(prop_name)}')
            self._add_object_schema(object_class_name, prop)
            return object_class_name, object_class_name
        else:
            raise NotImplementedError

    def _class_reference(self, schema_type: str) -> Optional[str]:
        if self._is_simple_type(schema_type):
            return None
        return schema_type

    @staticmethod
    def _schema_type_to_python_type(schema_type: str) -> str:
        mapping = {'string': 'str', 'integer': 'int', 'number': 'float', 'boolean': 'bool'}
        python_type = mapping.get(schema_type)
        return python_type or schema_type

    @staticmethod
    def _is_simple_type(schema_type: str) -> bool:
        return schema_type in ['string', 'integer', 'number', 'boolean']

    def _add_object_schema(self, schema_name: str, schema: OpenApiSpecSchemaProperty):
        """
        Add "object" schema to registry as Python class
        """
        name = self.qualified_class_name(class_name_from_schema_name(schema_name))
        schema_description = schema.description
        attrs = []
        for prop_name, prop in schema.properties.items():
            python_type, referenced_class = self._add_or_get_type_for_property(prop, name, prop_name)
            attr = Attribute(name=prop_name, python_type=python_type, docstring=prop.description, sample=None,
                             referenced_class=referenced_class)
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
        self._add_or_get_type_for_property(schema, sanitize_class_name(schema_name))

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
        self.normalize()
        for name, v in self._classes.items():
            s = v.source()
            if s is None:
                print(f'Class {name} has no source: baseclass={v.baseclass}')
            else:
                print(s)
            print()
            print()
        # add endpoints
        raise NotImplementedError()

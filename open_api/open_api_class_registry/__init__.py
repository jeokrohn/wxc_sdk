"""
Python class registry for OpenAPI schema; derived from PythonClassRegistry; used for code creation
"""
import json
import re
from typing import Optional

from apib.python_class import PythonAPI, PythonClass, Attribute, Endpoint, Parameter
from apib.class_registry import PythonClassRegistry
from apib.tools import sanitize_class_name, snake_case
from open_api.open_api_model import OASpec, OASchemaProperty, OAOperation, OAContent
from open_api.open_api_sources import OpenApiSpecInfo


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


class OpenApiPythonClassRegistry(PythonClassRegistry):
    """
    Registry of classes generated from OpenAPI schema
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def _attributes_from_enum(prop: OASchemaProperty) -> list[Attribute]:
        """
        Create attributes from enum values
        """
        attrs = [Attribute(name=enum_value, python_type='str', docstring=None, sample=None,
                           referenced_class=None)
                 for enum_value in prop.enum]
        return attrs

    def _add_or_get_type_for_property(self, prop: OASchemaProperty,
                                      name: str,
                                      prop_name: str = '') -> tuple[str, Optional[str]]:
        """
        Add or get type for property
        :return: python_type and referenced_class
        """
        if (ref := prop.ref or prop.object_ref):
            # reference to a different schema that (hopefully) will be added to the registry as PythonClass later
            class_name = class_name_from_ref(ref)
            referenced_class_name = self.qualified_class_name(class_name_from_schema_name(class_name))
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
            if referenced_class:
                referenced_class = self.qualified_class_name(referenced_class)
            return python_type, referenced_class
        elif self._is_simple_type(prop.type):
            return self._schema_type_to_python_type(prop.type), None
        elif prop.type == 'object':
            # create class for object
            if not prop.properties:
                # empty object
                return 'dict', None
            object_class_name = sanitize_class_name(f'{name}{sanitize_class_name(prop_name)}')
            object_class_name = self.qualified_class_name(object_class_name)
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

    def _add_object_schema(self, schema_name: str, schema: OASchemaProperty):
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

    def _add_schema(self, schema_name: str, schema: OASchemaProperty):
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

    def _parameter_from_schema_property(self, spec: OASpec, prop_name: str, prop: OASchemaProperty) -> Parameter:
        """
        Create parameter from schema property
        """
        python_type, referenced_class = self._add_or_get_type_for_property(prop, prop_name)
        return Parameter(name=prop_name, python_type=python_type, referenced_class=referenced_class,
                         docstring=prop.description, sample=prop.example, optional=prop.required is False,
                         registry=self)

    def _body_parameter_from_operation(self, spec: OASpec, operation: OAOperation) -> list[Parameter]:
        """
        Create parameter list from operation
        """
        if not (req_body := operation.request_body):
            return []
        if not (content := req_body.content):
            return []
        if len(content) > 1:
            raise ValueError('Only one content type supported')
        content_type = next(iter(content))
        body_content = content[content_type]
        if not (body_schema := body_content.schema_):
            raise ValueError('No schema in request body')
        if (ref := body_schema.ref or body_schema.object_ref):
            # reference to a different schema that (hopefully) will be added to the registry as PythonClass later
            class_name = class_name_from_ref(ref)
            # find the schema in the registry
            class_spec = spec.components.schemas.get(class_name)
            if not class_spec:
                raise ValueError(f'Referenced schema {class_name} not found')
            # now we can create the parameter list from the referenced schema
            paraam_properties = class_spec.properties
        else:
            # create parameter list from schema properties
            paraam_properties = body_schema.properties
        # create parameter list
        parameters = [self._parameter_from_schema_property(spec, prop_name, prop)
                      for prop_name, prop in paraam_properties.items()]
        return parameters

    def _endpoint_from_operation(self, spec: OASpec, operation: OAOperation,
                                 host: str, path: str, method: str):
        """
        Add operation to api
        """
        endpoint_name = snake_case(operation.operation_id)
        method = method
        host = host
        url = path
        title = operation.summary
        docstring = operation.description

        href_parameter = [Parameter(name=qp.name, python_type=self._schema_type_to_python_type(qp.schema_.type),
                                    referenced_class=None, docstring=qp.description, sample=qp.example,
                                    optional=qp.required is False, registry=self)
                          for qp in operation.query_parameters]

        # url parameters are also part of href parameters
        href_parameter.extend((Parameter(name=qp.name,
                                         python_type=self._schema_type_to_python_type(qp.schema_.type),
                                         referenced_class=None, docstring=qp.description, optional=False,
                                         sample=qp.example, registry=self, url_parameter=True)
                               for qp in operation.path_parameters))

        body_parameter = self._body_parameter_from_operation(spec, operation)

        body_class_name = None
        registry = self

        response_code, response = next(((rc, content) for rc, content in operation.responses.items()
                                        if rc.startswith('2')), (None, None))

        response_ct, response_content = next(iter(response.content.items()), (None, None))
        if not (response_ct and response_content):
            response_body = None
            result = None
            result_referenced_class = None
            if response_code != '204':
                raise ValueError(f'unexpected response code {response_code}')
        else:
            response_content: OAContent
            # response body is an example
            response_body = response_content.example
            response_schema = response_content.schema_
            result, result_referenced_class = self._add_or_get_type_for_property(response_schema, 'Response',
                                                                                 prop_name=endpoint_name)
            print(f'endpoint {endpoint_name} referenced {result_referenced_class}')

        endpoint = Endpoint(name=endpoint_name, method=method, host=host, url=url,
                            title=title, docstring=docstring, href_parameter=href_parameter,
                            body_parameter=body_parameter, body_class_name=body_class_name,
                            response_body=response_body, result=result,
                            result_referenced_class=result_referenced_class, registry=registry)
        return endpoint

    def add_open_api(self, spec_info: OpenApiSpecInfo):
        """
        Add classes from given OpenApiSpecInfo
        """
        with open(spec_info.spec_path) as f:
            data = json.load(f)
        open_api_spec = OASpec.model_validate(data)

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
        for path, method, operation in open_api_spec.operations():
            endpoint = self._endpoint_from_operation(open_api_spec, operation, host, path, method)
            python_api.add_endpoint(endpoint)
        return

"""
Python class registry for OpenAPI schema; derived from PythonClassRegistry; used for code creation
"""
import json
import logging
import re
from typing import Optional

import dateutil.parser

from apib.python_class import PythonAPI, PythonClass, Attribute, Endpoint, Parameter
from apib.class_registry import PythonClassRegistry
from apib.tools import sanitize_class_name, snake_case
from open_api.open_api_model import OASpec, OASchemaProperty, OAOperation, OAContent, OAParameter
from open_api.open_api_sources import OpenApiSpecInfo

log = logging.getLogger(__name__)


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
    value=value.strip("'").strip('"')

    # value has to have some minimum  length to qualify as a date
    if len(value) < 10:
        return False
    try:
        dateutil.parser.parse(value)
    except (OverflowError, dateutil.parser.ParserError, TypeError):
        # probably a string
        return False
    except Exception as e:
        raise NotImplementedError(f'Unexpected error when trying to parse a string: {e}')

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

    def __init__(self):
        super().__init__()

    @staticmethod
    def _attributes_from_enum(prop: OASchemaProperty) -> list[Attribute]:
        """
        Create attributes from enum values
        """
        enum_values = prop.enum
        enum_details = dict(prop.enum_details or [])
        attrs = [Attribute(name=enum_value, python_type='str', docstring=enum_details.get(enum_value), sample=None,
                           referenced_class=None)
                 for enum_value in enum_values]
        return attrs

    def _add_or_get_type_for_property(self, prop: OASchemaProperty,
                                      name: str,
                                      prop_name: str = '',
                                      parent_example=None) -> tuple[str, Optional[str]]:
        """
        Add or get type for property

        :return: python_type and referenced_class
        """
        try:
            if (ref := prop.ref or prop.object_ref):
                # reference to a different schema that (hopefully) will be added to the registry as PythonClass later
                class_name = class_name_from_ref(ref)
                referenced_class_name = self.qualified_class_name(class_name_from_schema_name(class_name))
                return referenced_class_name, referenced_class_name
        except AttributeError:
            raise

        if prop.enum:
            # create an enum class
            # with the enum values as attributes
            # and use that as the type
            enum_class_name = self.qualified_class_name(sanitize_class_name(f'{name}{sanitize_class_name(prop_name)}'))
            attrs = self._attributes_from_enum(prop)
            python_class = PythonClass(name=enum_class_name, attributes=attrs, description=prop.enum_description,
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
            if not prop.items:
                # fall back to array[string]
                schema_type = 'string'
                referenced_class = None
                log.warning(f'No items in array property {prop_name} in {name}. Falling back to array[string]')
            else:
                schema_type, referenced_class = self._add_or_get_type_for_property(prop.items, array_class_name, 'item')
                referenced_class = self._class_reference(referenced_class)
            python_type = f'list[{self._schema_type_to_python_type(schema_type)}]'
            if referenced_class:
                referenced_class = self.qualified_class_name(referenced_class)
            return python_type, referenced_class
        elif self._is_simple_type(prop_type:=prop.type):
            example = prop.example or parent_example
            if prop_type == 'number' and isinstance(example, int):
                # 'number' actually should be 'integer' if the example is an integer
                msg = (f'Changing type "number" to "integer" for {name.split("%")[-1]}.{prop_name} '
                         f'based on example "{example}"')
                log.info(msg)
                prop_type = 'integer'
            elif prop_type == 'string' and isinstance(example, str) and is_datetime(example):
                msg = (f'Changing type "string" to "datetime" for {name.split("%")[-1]}.{prop_name} '
                       f'based on example "{example}"')
                log.info(msg)
                prop_type = 'datetime'
            return self._schema_type_to_python_type(prop_type), None
        elif prop.type == 'object':
            # create class for object
            if not prop.properties:
                # empty object
                return 'dict', None
            object_class_name = sanitize_class_name(f'{name}{sanitize_class_name(prop_name)}')
            object_class_name = self.qualified_class_name(object_class_name)
            self._add_object_schema(object_class_name, prop)
            return object_class_name, object_class_name
        elif any_type := prop.any_type:
            """
            property has any_of and types of all options are identical
            """
            if self._is_simple_type(any_type):
                any_type = self._schema_type_to_python_type(any_type)
                return any_type, None
            else:
                raise NotImplementedError(f'any_type {any_type}, need to figure out how to handle non-simple types')
        elif not prop.model_fields_set:
            # This is an empty property
            # for code generation we will use 'Any' as the type
            log.warning(f'Empty property {prop_name} in {name}')
            return 'Any', None
        else:
            raise NotImplementedError(f'Need to handle property {prop_name} in {name}: {prop}')

    def _class_reference(self, schema_type: str) -> Optional[str]:
        if self._is_simple_type(schema_type):
            return None
        return schema_type

    @staticmethod
    def _schema_type_to_python_type(schema_type: str) -> str:
        mapping = {'string': 'str', 'integer': 'int', 'number': 'float', 'boolean': 'bool', 'datetime': 'datetime'}
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
            attr = Attribute(name=prop_name, python_type=python_type, docstring=prop.docstring, sample=None,
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

    def _parameter_from_schema_property(self, *, prop_name: str, prop: OASchemaProperty,
                                        param_required: Optional[set[str]] = None,
                                        url_parameter:bool=False) -> Parameter:
        """
        Create parameter from schema property
        """
        param_required = param_required or prop.required and set(prop.required) or {}
        required = (param_required and prop_name in param_required)
        python_type, referenced_class = self._add_or_get_type_for_property(prop, prop_name)
        return Parameter(name=prop_name, python_type=python_type, referenced_class=referenced_class,
                         docstring=prop.docstring, sample=prop.example, optional=not required,
                         url_parameter=url_parameter,
                         registry=self)

    def _parameter_from_oa_parameter(self, param: OAParameter) -> Parameter:
        """
        Create parameter from OAParameter
        """
        python_type, referenced_class = self._add_or_get_type_for_property(param.schema_, param.name,
                                                                           parent_example=param.example)
        return Parameter(name=param.name, python_type=python_type, referenced_class=referenced_class,
                         docstring=param.description, sample=param.example, optional=not param.required,
                         url_parameter=param.in_ == 'path',
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
        if ref := body_schema.ref or body_schema.object_ref:
            # reference to a different schema that (hopefully) will be added to the registry as PythonClass later
            class_name = class_name_from_ref(ref)
            # find the schema in the registry
            class_spec = spec.get_schema(ref)
            if not class_spec:
                raise ValueError(f'Referenced schema {class_name}/{ref} not found')
            # now we can create the parameter list from the referenced schema
            param_properties = class_spec.properties
            param_required = class_spec.required and set(class_spec.required) or {}
        else:
            # create parameter list from schema properties
            param_properties = body_schema.properties
            param_required = body_schema.required and set(body_schema.required) or {}
        # create parameter list
        parameters = [self._parameter_from_schema_property(prop_name=prop_name, prop=prop,
                                                           param_required=param_required)
                      for prop_name, prop in param_properties.items()]
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

        href_parameter = [self._parameter_from_oa_parameter(qp)
                          for qp in operation.parameters if not qp.is_auth]

        body_parameter = self._body_parameter_from_operation(spec, operation)

        body_class_name = None
        registry = self

        response_code, response = next(((rc, content) for rc, content in operation.responses.items()
                                        if rc.startswith('2')), (None, None))

        response_ct, response_content = next(iter(response.content.items()), (None, None))
        if not (response_ct and response_content):
            if response_code == '200':
                log.warning(f'No content in 200 response for {endpoint_name}')
            response_body = None
            result = None
            result_referenced_class = None
            if response_code not in {'204', '201', '202', '200'}:
                raise ValueError(f'unexpected response code {response_code} for {endpoint_name}')
        else:
            response_content: OAContent
            # response body is an example
            response_body = response_content.example
            response_schema = response_content.schema_
            if response_schema is None:
                # if no schema is provided, we can't do much. For now we just issue a warning
                log.warning(f'No schema in response for {endpoint_name}')
                result = None
                result_referenced_class = None
            else:
                result, result_referenced_class = self._add_or_get_type_for_property(response_schema, endpoint_name,
                                                                                     prop_name='Response')

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

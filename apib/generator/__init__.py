import os
import re
from collections import defaultdict
from collections.abc import Generator
from dataclasses import dataclass
from itertools import chain
from typing import NamedTuple, Union
from urllib.parse import urljoin

import dateutil.parser

from apib.apib import read_api_blueprint, ApibParseResult
from apib.apib.classes import ApibElement, ApibEnum, ApibDatastructure, ApibObject, ApibString, \
    ApibBool, ApibNumber, ApibArray, ApibSelect, ApibMember
from apib.python_class import PythonClassRegistry, Endpoint, Parameter, PythonClass, Attribute, \
    simple_python_type

PREAMBLE = """
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum"""


class PythonTypeFromHintAndSampleResult(NamedTuple):
    sample: str
    python_type: str


@dataclass(repr=False, init=False)
class CodeGenerator:
    class_registry: PythonClassRegistry
    #: Dictionary of parsed APIB files. Indexed by basename of APIB file w/o suffix
    parsed_blueprints: dict[str, ApibParseResult]
    #: Dictionary of list of endpoints of an APIB file. Indexed by basename of APIB file w/o suffix
    endpoints: dict[str, list[Endpoint]]

    def __init__(self):
        self.class_registry = PythonClassRegistry()
        self.parsed_blueprints = dict()
        self.endpoints = defaultdict(list)

    def read_blueprint(self, apib_path: str):
        # read api bluepring file
        data = read_api_blueprint(apib_path)

        # parse data
        apib_key = os.path.splitext(os.path.basename(apib_path))[0]
        parse_result = ApibParseResult.model_validate(data)
        self.parsed_blueprints[apib_key] = parse_result

        # use APIB filename to disambiguate class names
        self.class_registry.set_context(apib_key)

        # register all classes from parsed result
        self.class_registry.add_classes_from_parse_result(parse_result)
        self._register_endpoints(apib_key=apib_key, parsed_blueprint=parse_result)

    def cleanup(self):
        self.class_registry.normalize()
        # TODO: update normalized class names in endpoints
        raise NotImplementedError()

    def all_endpoints(self) -> Generator[tuple[str, Endpoint], None, None]:
        """
        Generator of endpoints defined in the APIB
        """
        return chain.from_iterable(((apib_key, ep)
                                    for ep in endpoints)
                                   for apib_key, endpoints in self.endpoints.items())

    def source(self) -> str:
        """
        Generate Python source for the APIB read
        """
        class_names = []
        class_sources = [class_names.append(c.name) or s for c in self.class_registry.classes() if (s := c.source())]
        auto_src = f"""__auto__ = [{", ".join(f"'{c}'" for c in sorted(class_names))}]"""
        source = '\n\n\n'.join(chain.from_iterable(((PREAMBLE, auto_src), class_sources)))
        source = source.strip() + '\n'
        return source

    def _register_endpoints(self, apib_key: str, parsed_blueprint: ApibParseResult):
        """
        Determine endpoints defined in parsed blueprint and register the endpoints. Python classes are registered on
        the fly as needed
        """
        # host is defined at tha API level
        # something like 'https://webexapis.com/v1/'
        host = parsed_blueprint.api.host
        for transition in parsed_blueprint.api.transitions():
            # come up with a name for the method
            # 'List Admin Audit Events' --> 'list_admin_audit_events'
            name = '_'.join(transition.title.split()).lower()

            # href is something like '/adminAudit/events{?orgId,from,to,actorId,max,offset,eventCategories}'
            href = transition.href
            # extract the href parameter names from the part between the brackets
            if m := re.search(r'\{\?(.+)}', href):
                href_param_names = m.group(1).split(',')
            else:
                href_param_names = []

            # the actual URL is the part before the bracket ... if there is one
            url = href.split('{')[0].strip('/')
            # full url based on host and endpoint url
            full_url = urljoin(host, url)

            # gather info from the HTTP transaction
            http_transaction = transition.http_transaction
            request = http_transaction.request
            response = http_transaction.response

            method = request.method
            response_datastructure = response.datastructure
            href_parameters = []
            for href_variable in transition.href_variables:
                param = self._param_from_member_or_select(endpoint_name=name, member=href_variable)
                href_parameters.append(param)

            body_parameters = []
            if body := request.find_content_by_element('dataStructure'):
                body: ApibDatastructure
                body_content = body.content
                if isinstance(body_content, ApibObject):
                    # The object should have all attributes
                    body_content: ApibObject
                    # ApibObject has a list of members
                    body_parameters = [self._param_from_member_or_select(endpoint_name=name, member=member)
                                      for member in body_content.content]
                elif isinstance(body_content, ApibElement) and not any((body_content.content,
                                                                        body_content.meta)):
                    # this might be a class name
                    class_name = body_content.element.replace(' ', '')
                    class_name = self.class_registry.qualified_class_name(class_name)

                    # type attributes is the only acceptable attribute
                    optional = False
                    if body_content.attributes:
                        if set(body_content.attributes) != {'typeAttributes'}:
                            raise KeyError(f'Only typeAttributes are acceptable, got: '
                                           f'{", ".join(sorted(body_content.attributes))}')
                        type_attributes = set(ta.content for ta in body_content.attributes['typeAttributes'].content)
                        optional = 'required' not in type_attributes
                    # .. and that class should exist
                    if python_class := self.class_registry.get(class_name):
                        # attributes of the class -> parameters
                        if python_class.attributes:
                            body_parameters = [Parameter(name=attr.name, python_type=attr.python_type,
                                                        docstring=attr.docstring, sample=attr.sample,
                                                        optional=optional, referenced_class=attr.referenced_class)
                                              for attr in python_class.attributes]
                        else:
                            raise NotImplementedError('No attributes')
                else:
                    raise NotImplementedError(f'http request body datastructure '
                                              f'with unexpected content: {body_content.element}')

            result = None
            referenced_class = None
            if not response_datastructure:
                raise NotImplementedError()
            else:
                # we have as response datastructure
                # a response datastructure should always have content
                response_ds_content = response_datastructure.content
                if not response_ds_content:
                    raise ValueError('response datastructure w/o content')
                else:
                    # the datastructure content can have content...
                    if response_ds_content.content:
                        # ... and then the element is either 'array' or 'object'
                        if response_ds_content.element == 'object':
                            response_class = self.class_registry.add_classes_from_data_structure(ds=response_datastructure,
                                                                                                 class_name=f'{name} Response')
                            result = response_class.name
                        elif response_ds_content.element == 'array':
                            array_content_class_name = response_ds_content.content[0].element
                            array_content_class_name = self.class_registry.qualified_class_name(array_content_class_name)
                            result = f'list[{array_content_class_name}]'
                            referenced_class = array_content_class_name
                        else:
                            raise ValueError(f'Unexpected response datastructure content element: '
                                             f'{response_ds_content.element}')

                    else:
                        # .. or the datastructure content doesn't have content
                        # and in this case the element is a reference to a class
                        result = response_datastructure.content.element
                        result = self.class_registry.qualified_class_name(result)
                        # .. and the class has to exist
                        if not self.class_registry.get(class_name=result):
                            raise KeyError(f'class {result} not found')
            referenced_class = referenced_class or result
            self.endpoints[apib_key].append(Endpoint(name=name, method=method, url=full_url,
                                                     href_parameter=href_parameters,
                                                     body_parameter=body_parameters,
                                                     result=result,
                                                     result_referenced_class=referenced_class))
        return

    def _param_from_member_or_select(self, endpoint_name: str, member: Union[ApibMember, ApibSelect]) -> Parameter:

        if not (isinstance(member, ApibMember) or isinstance(member, ApibSelect)):
            raise TypeError(f'unexpected parameter type: {member.__class__.__name__}')

        if isinstance(member, ApibSelect):
            member: ApibSelect
            name = member.option_key
            docstring = member.description
            # collect all types
            types = [simple_python_type(option.content.value.element, option.content.value.content)
                     for option in member.content]
            python_type = f'Union[{", ".join(sorted(set(types)))}]'
            text_of_options = '\n'.join(f'{option.content.value.content} ({t})'
                                        for option, t in zip(member.content, types))
            docstring = '\n'.join(l for l in chain((docstring, 'One of:'),
                                                   (f'  * {tl}' for tl in text_of_options.splitlines()))
                                  if l is not None)

            parameter = Parameter(name=name, python_type=python_type, docstring=docstring, referenced_class=None,
                                  optional=False, sample=None)
            return parameter

        # determine parameter name,
        name = member.key

        docstring = member.description
        sample = member.value
        if member.meta is None:
            type_hint = None
        else:
            type_hint = member.meta.title
        optional = 'required' not in member.type_attributes

        # now try to determine the actual Python type and sample value
        type_hint_lower = type_hint and type_hint.lower()
        python_type = ''
        referenced_class = None

        if isinstance(sample, ApibString):
            sample = sample.content
        elif isinstance(sample, ApibBool):
            sample = sample.content
        elif isinstance(sample, ApibNumber):
            sample = sample.content

        if isinstance(sample, ApibElement):
            if isinstance(sample, ApibEnum):
                sample: ApibEnum
                # create an enum on the fly
                # name of the enum is based on the method name and the attribute
                enum_name = ''.join(map(str.capitalize, endpoint_name.split('_')))
                enum_name = f'{enum_name}{name[0].upper()}{name[1:]}'
                enum_attributes = list(Attribute.from_enum(sample))
                enum_class = PythonClass(name=enum_name, description=docstring, is_enum=True,
                                         attributes=enum_attributes)
                # and register that
                self.class_registry.add(enum_class)
                enum_name = enum_class.name
                if sample.default:
                    sample = sample.default.content
                else:
                    # try the 1st enum value
                    sample = sample.enum_values[0]
                python_type = enum_name
                referenced_class = enum_name
            elif isinstance(sample, ApibObject):
                # create a class on the fly
                class_name = ''.join(map(str.capitalize, endpoint_name.split('_')))
                class_name = f'{class_name}{name[0].upper()}{name[1:]}'
                class_attributes = []
                for sample_member in sample.content:
                    attribute = self.class_registry.attribute_from_member(class_name=class_name,
                                                                          member=sample_member)
                    class_attributes.append(attribute)
                new_class = PythonClass(name=class_name, description=docstring, is_enum=False,
                                        attributes=class_attributes)
                # and register that
                self.class_registry.add(new_class)
                sample = ''
                python_type = new_class.name
                referenced_class = new_class.name
            elif isinstance(sample, ApibArray):
                try:
                    python_type = simple_python_type(sample.content[0].element)
                except ValueError:
                    python_type = None
                if python_type:
                    # simple type
                    python_type = f'list[{python_type}]'
                    sample = ", ".join(f"'{e.content}'" for e in sample.content)
                    sample = f'[{sample}]'
                else:
                    # hopefully we can figure out the type of the array elements. For this we expect the
                    # sample content to have exactly one ApibElement entry
                    if len(sample.content) != 1:
                        raise NotImplementedError(f'Unexpected sample: {sample}')
                    arr_element = sample.content[0]
                    if not isinstance(arr_element, ApibElement):
                        raise NotImplementedError(f'Unexpected sample: {sample}')
                    if isinstance(arr_element, ApibObject):
                        # create a class on the fly
                        class_name = ''.join(map(str.capitalize, endpoint_name.split('_')))
                        class_name = f'{class_name}{name[0].upper()}{name[1:]}'
                        class_attributes = []
                        for sample_member in arr_element.content:
                            attribute = self.class_registry.attribute_from_member(class_name=class_name,
                                                                                  member=sample_member)
                            class_attributes.append(attribute)
                        new_class = PythonClass(name=class_name, description=docstring, is_enum=False,
                                                attributes=class_attributes)
                        # and register that
                        self.class_registry.add(new_class)
                        class_name = new_class.name
                        referenced_class = new_class.name
                        sample = ''
                        python_type = f'list[{new_class.name}]'
                    else:
                        # this is an array of a class instance and the arr_element has the class name
                        class_name = arr_element.element
                        class_name = self.class_registry.qualified_class_name(class_name)
                        # this class has to exist
                        if pc := self.class_registry.get(class_name):
                            python_type = f'list[{pc.name}]'
                            referenced_class = pc.name
                            sample = ''
                        else:
                            raise KeyError(f'Unknown class: {class_name}')
            elif isinstance(sample, ApibElement):
                # in this case the element is a class name
                class_name = sample.element
                class_name = self.class_registry.qualified_class_name(class_name)

                # this class should exist
                if not self.class_registry.get(class_name):
                    raise KeyError(f'Unknown class: {class_name}')
                else:
                    python_type = class_name
                    referenced_class = class_name
                    if sample.meta:
                        raise NotImplementedError()
                    if (sample.attributes and
                            (unexpected_attributes := set(sample.attributes) - {'typeAttributes', 'default',
                                                                                'enumerations'})):
                        raise NotImplementedError(f'Unexpected sample attributes: '
                                                  f'{", ".join(sorted(unexpected_attributes))}')
                    if sample.content:
                        sample = sample.content.content
                    else:
                        sample = ''
            else:
                raise NotImplementedError(f'unhandled sample: {sample}')
        elif type_hint_lower == 'string' or type_hint_lower is None:
            # could be a datetime
            if sample is None:
                python_type = 'str'
            else:
                try:
                    dateutil.parser.parse(sample)
                    python_type = 'datetime'
                except (OverflowError, dateutil.parser.ParserError, TypeError):
                    # probably a string
                    python_type = 'str'
                except Exception as e:
                    raise NotImplementedError(f'Unexpected error when trying to parse a string: {e}')
        elif type_hint_lower == 'number':
            # can be int or float
            if sample is None:
                python_type = 'int'
            else:
                try:
                    sample = int(sample)
                    python_type = 'int'
                except ValueError:
                    python_type = 'float'
                    try:
                        sample = float(sample)
                    except ValueError:
                        pass
        elif type_hint_lower in {'integer', 'long', 'int'}:
            python_type = 'int'
            try:
                sample = int(sample)
            except ValueError:
                pass
        elif type_hint_lower == 'boolean':
            python_type = 'bool'
        elif type_hint_lower in {'list', 'array'}:
            python_type = 'list[str]'
        elif type_hint_lower.startswith('array['):
            # let's see whether the type spec is a known class
            m = re.match(r'array\[(.+)]', type_hint)
            array_element_class = m.group(1)
            pc = self.class_registry.get(self.class_registry.qualified_class_name(array_element_class))
            if pc:
                # reference to known class name
                python_type = f'list[{pc.name}]'
                referenced_class = pc.name
            else:
                python_type = f'list[{simple_python_type(array_element_class)}]'
        elif type_hint_lower == 'string array':
            python_type = 'list[str]'
        else:
            # check whether the type hint is a known PythonClass
            if pc := self.class_registry.get(type_hint):
                if pc.is_enum:
                    python_type = type_hint
                else:
                    NotImplementedError('No idea how to hande a non-enum class in href parameters')
            else:
                raise NotImplementedError(f'unexpected type hint: "{type_hint_lower}"')
        if not python_type:
            raise ValueError('Well, that\'s embarrassing!')

        parameter = Parameter(name=name, python_type=python_type, docstring=docstring, sample=sample,
                              optional=optional, referenced_class=referenced_class)
        return parameter

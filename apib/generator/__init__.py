import re
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
    classes_and_attribute_from_member, simple_python_type

PREAMBLE = """
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum"""

RESERVED_PARAM_NAMES = {'from', 'to'}


class PythonTypeFromHintAndSampleResult(NamedTuple):
    sample: str
    python_type: str


@dataclass(repr=False, init=False)
class CodeGenerator:
    class_registry: PythonClassRegistry
    parsed_blueprint: ApibParseResult

    def __init__(self):
        self.class_registry = PythonClassRegistry()
        self.parsed_blueprint = None

    def read_blueprint(self, apib_path):
        # read api bluepring file
        data = read_api_blueprint(apib_path)

        # parse data
        self.parsed_blueprint = ApibParseResult.model_validate(data)

        # register all classes from parsed result
        # TODO: allow to register multiple APIB files with identical class names
        #   in that case a new classname is created for the 2nd class and the references in the data from the APIB
        #   file are updated
        list(map(self.class_registry.add, PythonClass.from_parse_result(self.parsed_blueprint)))
        self.class_registry.eliminate_redundancies()

    def source(self) -> str:
        class_names = []
        class_sources = [class_names.append(c.name) or s for c in self.class_registry.classes() if (s := c.source())]
        auto_src = f"""__auto__ = [{", ".join(f"'{c}'" for c in sorted(class_names))}]"""
        source = '\n\n\n'.join(chain.from_iterable(((PREAMBLE, auto_src), class_sources)))
        source = source.strip() + '\n'
        return source

    def param_from_member_or_select(self, endpoint_name: str, member: Union[ApibMember, ApibSelect]) -> Parameter:

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

            parameter = Parameter(name=name, python_type=python_type, docstring=docstring,
                                  optional=False, sample=None)
            return parameter

        # determine parameter name, ... and avoid reserved names
        name = member.key
        if name in RESERVED_PARAM_NAMES:
            name = f'{name}_'

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
                if sample.default:
                    sample = sample.default.content
                else:
                    # try the 1st enum value
                    sample = sample.enum_values[0]
                python_type = enum_name
            elif isinstance(sample, ApibObject):
                # create a class on the fly
                class_name = ''.join(map(str.capitalize, endpoint_name.split('_')))
                class_name = f'{class_name}{name[0].upper()}{name[1:]}'
                class_attributes = []
                for sample_member in sample.content:
                    classes, attribute = classes_and_attribute_from_member(class_name=class_name,
                                                                           member=sample_member)
                    # register classes
                    list(map(self.class_registry.add, classes))
                    class_attributes.append(attribute)
                new_class = PythonClass(name=class_name, description=docstring, is_enum=False,
                                        attributes=class_attributes)
                # and register that
                self.class_registry.add(new_class)
                sample = ''
                python_type = class_name
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
                            classes, attribute = classes_and_attribute_from_member(class_name=class_name,
                                                                                   member=sample_member)
                            # register classes
                            list(map(self.class_registry.add, classes))
                            class_attributes.append(attribute)
                        new_class = PythonClass(name=class_name, description=docstring, is_enum=False,
                                                attributes=class_attributes)
                        # and register that
                        self.class_registry.add(new_class)
                        sample = ''
                        python_type = f'list[{class_name}]'
                    else:
                        # this is an array of a class instance and the arr_element has the class name
                        class_name = arr_element.element.replace(' ', '')
                        # this class has to exist
                        if pc := self.class_registry.get(class_name):
                            python_type = f'list[{pc.name}]'
                            sample = ''
                        else:
                            raise KeyError(f'Unknown class: {class_name}')
            elif isinstance(sample, ApibElement):
                # in this case the element is a class name
                class_name = sample.element.replace(' ', '')
                # this class should exist
                if not self.class_registry.get(class_name):
                    raise KeyError(f'Unknown class: {class_name}')
                else:
                    python_type = class_name
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
            # TODO: this is probably an oversimplification
            #   probably need to get python type for array members instead
            #   this might lead to dynamic class creation. Should we move this code to a method of the class registry?
            python_type = type_hint.replace('array[', 'list[')
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

        return Parameter(name=name, python_type=python_type, docstring=docstring, sample=sample, optional=optional)

    def endpoints(self) -> Generator[Endpoint, None, None]:
        # host is defined at tha API level
        # something like 'https://webexapis.com/v1/'
        host = self.parsed_blueprint.api.host
        for transition in self.parsed_blueprint.api.transitions():
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
            # full url based based on host and endpoint url
            full_url = urljoin(host, url)

            # gather info from the HTTP transaction
            http_transaction = transition.http_transaction
            request = http_transaction.request
            response = http_transaction.response

            method = request.method
            response_datastructure = response.datastructure
            href_parameter = []
            for href_variable in transition.href_variables:
                param = self.param_from_member_or_select(endpoint_name=name, member=href_variable)
                href_parameter.append(param)

            # TODO: body parameter, from request
            body_parameter = []
            if (body := request.find_content_by_element('dataStructure')):
                body: ApibDatastructure
                body_content = body.content
                if isinstance(body_content, ApibObject):
                    # The object should have all attributes
                    body_content: ApibObject
                    # ApibObject has a list of members
                    body_parameter = [self.param_from_member_or_select(endpoint_name=name, member=member)
                                      for member in body_content.content]
                elif isinstance(body_content, ApibElement) and not any((body_content.content,
                                                                        body_content.meta)):
                    # this might be a class name
                    class_name = body_content.element.replace(' ', '')

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
                            body_parameter = [Parameter(name=attr.name, python_type=attr.python_type,
                                                        docstring=attr.docstring, sample=attr.sample,
                                                        optional=optional)
                                              for attr in python_class.attributes]
                        else:
                            raise NotImplementedError('No attributes')
                else:
                    raise NotImplementedError(f'http request body datastructure '
                                              f'with unexpected content: {body_content.element}')

            yield Endpoint(name=name, method=method, url=full_url, href_parameter=href_parameter,
                           body_parameter=body_parameter, result=response_datastructure)

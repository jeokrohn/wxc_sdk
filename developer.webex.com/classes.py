#!/usr/bin/env python
"""
generate class definitions from API specs

usage: classes.py [-h] [-o OUTPUT_PATH] [-l LOG_PATH] api_spec

positional arguments:
  api_spec

options:
  -h, --help            show this help message and exit
  -o OUTPUT_PATH, --output OUTPUT_PATH
                        Write output to given file.
  -l LOG_PATH, --logfile LOG_PATH
                        Write detailed logs to this file.
"""
# TODO: check/fix private_network_connect
# TODO: enums in url parameters need to be converted to string values
import argparse
import json
import logging
import re
from collections import Counter
from collections.abc import Generator, Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from io import StringIO
from itertools import chain
from json import JSONDecodeError
from sys import stderr, stdout
from typing import TextIO, Optional, NamedTuple

from inflection import underscore

from scraper import DocMethodDetails, Parameter, Class, MethodDetails, python_type, break_lines
from wxc_sdk.base import to_camel

collected_types = list()

log = logging.getLogger()

PY_HEADER = """
from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, TypeAdapter
"""


def setup_logging(console_level: int = logging.INFO,
                  log_path: Optional[str] = None):
    """
    Setup logging

    :param console_level: logging level for console (stderr)
    :param log_path: path to log file
    """

    # enable debugging
    logging.getLogger('urllib3').setLevel(logging.INFO)
    logging.getLogger('selenium').setLevel(logging.INFO)

    # log to console level INFO
    # log to file level DEBUG
    logger = logging.getLogger()
    if log_path:
        fmt = logging.Formatter(fmt='%(levelname)5s:%(name)s:%(message)s')

        file_handler = logging.FileHandler(filename=log_path, mode='w')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(console_level)
    logger.addHandler(stream_handler)

    logger.setLevel(logging.DEBUG)


@dataclass
class APIMethod:
    name: str
    methods_details: MethodDetails
    body_class: Optional[Class] = None
    response_class: Optional[Class] = None

    METHOD = '''
    def {method_name}(self{param_list}){return_type}:
        """
{method_doc}

        documentation: {doc_url}
        """
{code}
'''

    EP_URL = '''        url = self.ep({url_path})'''
    PARAM_DOC = '''
        :param {p_name}: {p_doc}
        :type {p_name}: {p_type}'''
    PARAM_INIT = '''
        if {p_name} is not None:
            params['{p_name_camel}'] = {p_value}'''
    PARAM_INIT_REQUIRED = '''
        params['{p_name_camel}'] = {p_value}'''

    BODY_INIT = '''
        if {p_name} is not None:
            body.{p_name} = {p_name}'''

    @property
    def is_paginated(self) -> bool:
        return self.methods_details.is_paginated

    def source(self, common_prefix: str, transform_name: Callable[[str], str]) -> Generator[str, None, None]:
        """
        source for one method
        :return:
        """
        param_list = []
        param_docs = []
        param_code = []
        body_params = []

        def add_param(param: Parameter, is_query: bool = False, is_body: bool = False):
            """
            add a method parameter, prepare code to be generated for the parameter
            """
            p_name = param.python_name
            if param.param_class:
                # type of parameter is actually a class we generated
                p_type = python_type(param.param_class.name)
            else:
                p_type = python_type(param.type)
            for_param_list = f'{p_name}: {p_type}'
            if not param.required:
                for_param_list = f'{for_param_list} = None'
            # in paginated methods we want to get rid of "max" and "start"
            if not self.is_paginated or p_name not in {'start', 'max'}:
                param_list.append(for_param_list)
                p_doc = '\n'.join(break_lines(param.doc,
                                              # 2nd line and following start with three indentations
                                              line_start=' ' * 12,
                                              # 1str line starts with this string, consider this for line breaks of
                                              # 1st line
                                              first_line_prefix=f'        :param {p_name}: '))
                param_docs.append(self.PARAM_DOC.format(p_name=p_name,
                                                        p_type=p_type,
                                                        p_doc=p_doc).strip('\n'))
                if is_query:
                    # query parameters need special treatment
                    # * bools need to be transformed to true/false
                    # TODO: enums need to be conditionally transformed to strings
                    p_value = p_name
                    if p_type == 'bool':
                        p_value = f"str({p_name}).lower()"
                    if param.required:
                        param_code.append(self.PARAM_INIT_REQUIRED.format(p_name=p_name, p_value=p_value,
                                                                          p_name_camel=param.name))
                    else:
                        param_code.append(self.PARAM_INIT.format(p_name=p_name, p_value=p_value,
                                                                 p_name_camel=param.name))
            if is_body:
                body_params.append(self.BODY_INIT.format(p_name=p_name))

        name = underscore(self.name)
        uri_parameters = self.methods_details.parameters_and_response.get('URI Parameters')
        if uri_parameters:
            for param in uri_parameters:
                add_param(param)

        # collect parameters, differentiate between mandatory and optional parameters
        # 1st collect query parameters and then body parameters
        class ParameterInfo(NamedTuple):
            p: Parameter
            is_query: bool
            is_body: bool

        mandatory: list[ParameterInfo] = list()
        optional: list[ParameterInfo] = list()

        # add query parameters (mandatory 1st)
        query_parameters = self.methods_details.parameters_and_response.get('Query Parameters')
        if query_parameters:
            mandatory.extend(ParameterInfo(p=p, is_query=True, is_body=False) for p in query_parameters if p.required)
            optional.extend(
                ParameterInfo(p=p, is_query=True, is_body=False) for p in query_parameters if not p.required)

        # ... finally we need the request body
        if self.body_class:
            body_parameters = list(self.body_class.all_attributes())
            mandatory.extend(ParameterInfo(p=p, is_query=False, is_body=True) for p in body_parameters if p.required)
            optional.extend(ParameterInfo(p=p, is_query=False, is_body=True) for p in body_parameters if not p.required)

        # ... now we can actually add the parameters to the code, mandatory 1st
        for param in mandatory:
            add_param(param.p, is_query=param.is_query, is_body=param.is_body)
        for param in optional:
            add_param(param.p, is_query=param.is_query, is_body=param.is_body)

        method_doc = '\n'.join(chain.from_iterable(
            break_lines(line=line, line_start=' ' * 8) for line in self.methods_details.doc.splitlines()))
        if method_doc:
            method_doc = method_doc + '\n'
        if param_docs:
            param_docs = '\n'.join((p for pd in param_docs if (p := pd.strip('\n'))))
            method_doc = '\n'.join((method_doc, param_docs))
        method_doc = method_doc.strip('\n')

        # in paginated methods we want to add "**params" to allow additional parameters
        if self.is_paginated:
            param_list.append('**params')
            kwargs = True
        else:
            kwargs = False

        if param_list:
            param_list = f', {", ".join(param_list)}'
        else:
            param_list = ''

        method_body = StringIO()

        # add initialization of param dict
        if param_code:
            if not kwargs:
                print('        params = {}', file=method_body)
            print('\n'.join(p.strip('\n') for p in param_code), file=method_body)

        # initialization of JSON body
        if body_params:
            print(f'        body = {python_type(self.body_class.name)}()', file=method_body)
            print('\n'.join(p.strip('\n') for p in body_params), file=method_body)
            json_param = ', data=body.json()'
        else:
            json_param = ''

        # first create line to get EP
        url = self.methods_details.documentation.endpoint
        if common_prefix:
            url = url[len(common_prefix):].strip('/')
        if uri_parameters:
            url_path = f"f'{url}'"
            # find parameters in url and replace with snail_case names
            url_path, _ = re.subn('\{(\w+)}',
                                  lambda m: f'{{{underscore(m.group(1))}}}',
                                  url_path)
        else:
            url_path = url and f"'{url}'"
        print(self.EP_URL.format(url_path=url_path), file=method_body)

        # the REST call
        http_method = self.methods_details.documentation.http_method.lower()
        rest_call = f'super().{http_method}'
        if kwargs or param_code:
            kwargs = ', params=params'
        else:
            kwargs = ''
        rest_call = f'{rest_call}(url=url{kwargs}{json_param})'
        if self.response_class:
            rest_call = f'data = {rest_call}'

        if self.is_paginated:
            item_key, result_type = python_type(self.response_class.name, for_list=True)
            return_type = f' -> Generator[{result_type}, None, None]'
            if item_key == 'items':
                item_key = ''
            else:
                item_key = f"item_key='{item_key}', "
            result = f'return self.session.follow_pagination(url=url, model={result_type}, {item_key}' \
                     f'params=params{json_param})'
            rest_call = ''
        elif self.response_class:
            # if only a single attribute is returned then we might have a list of something
            # if the single attribute is not a list then we might as well just return that thing
            if not self.response_class.base and len(self.response_class.attributes) == 1:
                if m := re.match(r'^array\[(.+)]$', self.response_class.attributes[0].type):
                    # the only return attribute is a list
                    if self.response_class.attributes[0].param_class:
                        base_type = self.response_class.attributes[0].param_class.name
                        # we need to deserialize a list fo something
                        return_type = python_type(base_type)
                        result = f'return TypeAdapter(list[{return_type}].validate_python(data["' \
                                 f'{to_camel(self.response_class.attributes[0].name)}"])'
                        return_type = f'list[{return_type}]'
                    else:
                        return_type = python_type(self.response_class.attributes[0].type)
                        result = f'return data["{to_camel(self.response_class.attributes[0].name)}"]'
                else:
                    # the result has only one attribute
                    # this is either a trivial type or needs to be parsed as object
                    attr = self.response_class.attributes[0]
                    if attr.param_class:
                        # we need to deserialize a single object
                        return_type = python_type(attr.param_class.name)
                        result = f'return {return_type}.model_validate(data["{to_camel(attr.name)}"])'
                    else:
                        return_type = python_type(attr.type)
                        result = f'return data["{to_camel(attr.name)}"]'
            else:
                # the result has multiple attributes -> needs to be parsed as object
                result_type = python_type(self.response_class.name)
                return_type = f'{result_type}'
                result = f'return {result_type}.model_validate(data)'
            return_type = f' -> {return_type}'
        else:
            if http_method == 'get':
                # that is weird. a GET method w/o any return?
                # force a syntax error
                result = f'return $!$!$!   # this is weird. ' \
                         f'Check the spec at {self.methods_details.documentation.doc_link}'
            else:
                result = 'return'
            return_type = ''

        if rest_call:
            # no REST call if we return a Generator
            print(f'        {rest_call}', file=method_body)
        print(f'        {result}', file=method_body)

        # return something
        yield self.METHOD.format(method_name=transform_name(name), param_list=param_list, return_type=return_type,
                                 method_doc=method_doc,
                                 doc_url=self.methods_details.documentation.doc_link,
                                 code=method_body.getvalue()).strip('\n')
        return


@dataclass
class API:
    """
    Representation of an APi object
    """
    section: str
    doc: Optional[str] = None
    methods: list[APIMethod] = field(default_factory=list)

    @staticmethod
    def base_type(type_str: str) -> str:
        """
        get base type from type string

        "array[foo]" --> "foo"

        :param type_str:
        :return:
        """
        type_str = type_str.strip()
        if type_str.startswith('array['):
            type_str = type_str[6:-1]
        type_str = "".join(type_str.split())
        return type_str

    @staticmethod
    def class_name(parameter: Parameter):
        """
        Determine class name for a given parameter
        :param parameter:
        :return:
        """
        type_str = API.base_type(parameter.type)

        if type_str == 'enum' or type_str == 'object' or type_str == 'string':
            # class name based on attribute name
            class_name = parameter.name
            class_name = f'{class_name[0].upper()}{class_name[1:]}'
        else:
            # class name is in type_str
            class_name = type_str

        return class_name

    @staticmethod
    def method_name_from_header(header: str) -> str:
        """
        Derive a method name from a doc header

        Example: Create a Person --> Create Person

        :param header:
        :return:
        """

        def cap(s: str) -> str:
            return s[0].upper() + s[1:]

        header = header.replace(' a ', '')
        header = header.replace(' an ', '')
        header = header.replace(' the ', '')
        header = header.replace("'", '')

        result = "".join(map(cap, header.split()))
        # print(f'{header} -> {result}')
        return result

    def create_class(self, class_name: str, attributes: list[Parameter], as_enum: bool = False) -> Class:
        """
        Create a class with the given name and attributes

        :param class_name:
        :param attributes:
        :param as_enum:
        :return:
        """

        # catch a situation where a class is to be created with only attributes that are quoted strings
        # there is at least one occurrence on developer.webex.com where this schema is used to define an enum
        quoted_string = re.compile(r"^'(\w+)'$")
        if all(quoted_string.match(a.name) and a.type == 'string' and not a.param_attrs and not a.param_object
               for a in attributes):
            as_enum = True
            # update names (remove quotes)
            for attr in attributes:
                attr.name = quoted_string.match(attr.name).group(1)
        for attribute in attributes:
            if as_enum and any((attribute.param_attrs, attribute.param_attrs)):
                log.error(f'Enum cannot have childs: {class_name} {attributes}')
                continue
            # an attribute with just "true" and "false" as childs is a bool
            attr_names = set(a.name for a in chain(attribute.param_attrs, attribute.param_object))
            if attr_names == {'true', 'false'}:
                log.debug(f'{class_name}.{attribute.name}: type set to "boolean" b/c the only childs are "true" '
                          f'and "false"')
                # TODO: move doc string from child attributes up to this attribute
                attribute.type = 'boolean'
                attribute.param_object = list()
                attribute.param_attrs = list()
                continue

            # if the type has something like this then try to convert to attributes:
            # array[{"type": "personal-room","value": "testuser5@mycompany.webex.com","primary": false}]
            if not any((attribute.param_attrs, attribute.param_object)):
                base_type = self.base_type(attribute.type)
                try:
                    data = json.loads(base_type)
                except JSONDecodeError:
                    pass
                else:
                    attrs = []
                    for k, v in data.items():
                        if isinstance(v, str):
                            type_str = 'string'
                        elif isinstance(v, bool):
                            type_str = 'boolean'
                        elif isinstance(v, int):
                            type_str = 'number'
                        else:
                            type_str = 'any'
                        attrs.append(Parameter(name=k, type=type_str, doc=''))
                    log.debug(f'complex base type: "{base_type}", created parameters ad hoc: {attrs}')
                    attribute.param_attrs = attrs

                    # we also need a new type for the attribute
                    type_str = f'{attribute.name}Type'
                    type_str = f'{type_str[0].upper()}{type_str[1:]}'
                    if attribute.type.startswith('array['):
                        type_str = f'array[{type_str}]'
                    attribute.type = type_str

            is_enum = attribute.type == 'enum'
            # if name ends in "Enum" and all attributes are simple strings then we also treat this as an enum
            if attribute.type.endswith('Enum') and all(a.type == 'string' and not any((a.param_object, a.param_attrs))
                                                       for a in chain(attribute.param_attrs, attribute.param_object)):
                is_enum = True
            if is_enum and not attr_names:
                # an enum without childs is just a string
                log.debug(f'{class_name}.{attribute.name}: type set to "string" instead of "enum" b/c there are no '
                          f'child attributes')
                attribute.type = 'string'

            if attribute.param_attrs:
                new_class = self.create_class(class_name=self.class_name(attribute), attributes=attribute.param_attrs,
                                              as_enum=is_enum)
                attribute.param_class = new_class
            if attribute.param_object:
                new_class = self.create_class(class_name=self.class_name(attribute), attributes=attribute.param_object,
                                              as_enum=is_enum)
                attribute.param_class = new_class
            # if
        # for

        # if the class name has multiple words then make camel case
        class_name = ''.join(f'{w[0].upper()}{w[1:]}' for w in class_name.split())
        # strip illegal characters from class names
        class_name = re.sub(r'\W', '', class_name)

        new_class = Class(name=class_name, attributes=attributes, is_enum=as_enum)
        log.debug(
            f'create class: {new_class.name} - {", ".join(f"{attr.name}({attr.type})" for attr in attributes)}')
        return new_class

    def add_method(self, method_details: MethodDetails):
        """
        Add one method to the API
        """
        method_name = self.method_name_from_header(method_details.header)
        body_class = None
        response_class = None
        # look at "Body Parameters" and "Response Properties"
        if body := method_details.parameters_and_response.get('Body Parameters'):
            body_class = self.create_class(class_name=f'{method_name}Body', attributes=body)
        if response := method_details.parameters_and_response.get('Response Properties'):
            response_class = self.create_class(class_name=f'{method_name}Response', attributes=response)
        self.methods.append(APIMethod(name=method_name,
                                      methods_details=method_details,
                                      body_class=body_class,
                                      response_class=response_class))
        return

    @property
    def api_class_name(self) -> str:
        """
        Name of the API class for this API
        """
        return f'{self.section.replace(" ", "")}Api'

    API_HEADER = '''
class {class_name}(ApiChild, base='{base}'):
    """
{class_name_doc}
    """
'''

    def source(self) -> Generator[str, None, None]:
        """
        Source for API class
        """
        class_name = self.api_class_name
        # determine common base of all methods in this API
        endpoints = [m.methods_details.documentation.endpoint for m in self.methods]
        # look for the 1st index where the set of letters is larger than one or a URL parameter starts
        common_index = next((i for i, letters in enumerate(zip(*endpoints))
                             if len(ls := set(letters)) > 1 or ls == {'{'}),
                            min(map(len, endpoints)))
        common_prefix = endpoints[0][:common_index]
        webex_prefix = 'https://webexapis.com/v1/'
        if common_prefix.startswith(webex_prefix):
            base = common_prefix[len(webex_prefix):]
        else:
            base = ''
            common_prefix = ''
        if self.doc:
            doc = '\n'.join(chain.from_iterable(break_lines(line=line, line_start='    ')
                                                for line in self.doc.splitlines()))
        else:
            doc = ''
        yield self.API_HEADER.format(class_name=class_name, base=base, class_name_doc=doc).strip('\n')

        # for methods like list_rooms, create_room, update_room, ... we want to get rid of "room"
        # let's look for the most common word in all methods names
        word_counts = Counter(chain.from_iterable(underscore(method.name).split('_') for method in self.methods))
        word, word_count = max(word_counts.items(), key=lambda t: t[1])
        if word == 'options' or word_count == 1:
            # let's not transform any: set word to something that is never going to be matching anything
            word = 'zzzzzzzzzzzzzz'
        method_matcher = re.compile(f'_{word}s?')

        def transform_method_name(name: str) -> str:
            name = method_matcher.sub('', name)
            if name.startswith('get_'):
                name = name[4:]
            return name

        for method in self.methods:
            yield from method.source(common_prefix=common_prefix, transform_name=transform_method_name)

    def sources(self) -> Generator[str, None, None]:
        """
        Generator for sources for this API
        """
        # yield sources for all classes
        # all body and response classes at the end ... we might want to delete them anyway
        for only_childs in (True, False):
            for method in self.methods:
                if method.body_class:
                    yield from method.body_class.sources(only_childs=only_childs)
                if method.response_class:
                    yield from method.response_class.sources(only_childs=only_childs)

        # now prepare and yield source for APIClass
        yield from self.source()


@dataclass
class ClassGenerator:
    output: TextIO
    api_list: list[API] = field(default_factory=list)

    @staticmethod
    def parameters_from_url(url: str) -> list[str]:
        """
        get list of URL parameters from URL

        Parameters in URL are strings like "{locationId}". Parameters are returned in CamelCase

        :param url:
        :return:
        """
        url_parameter = re.compile(r'\{([a-zA-Z_]+)}')
        return url_parameter.findall(url)

    @staticmethod
    def method_from_url(url: str) -> str:
        """
        Extract last part of URL that is not a URL parameter

        Result is in camel case with 1st letter capitalized

        :param url:
        :return:
        """
        parts = url.split('/')
        parts.reverse()
        return next((p for p in parts if not p.startswith('{'))).capitalize()

    def from_methods(self, section: str, doc: str, method_list: list[MethodDetails]):
        Class.registry.clear()
        api = API(section=section, doc=doc)
        self.api_list.append(api)
        for method_details in method_list:
            api.add_method(method_details)
        Class.optimize()

    def from_doc_method_details(self, api_spec: DocMethodDetails, only_section: str = None):
        """
        Read API spec and identify classes for objects in the API spec. Optionally limited to only one section
        """

        Class.registry.clear()
        # go through all methods

        # for each method look at request and response body parameters

        # each response body is a class be definition?
        # * maybe not for simple lists
        # * .. other exceptions?

        # else every parameter with attributes is a class
        # * param_attrs only for enums
        # * param_object is a class
        for section in api_spec.docs:
            if only_section and only_section != section:
                continue
            section_details = api_spec.docs[section]
            methods = section_details.methods
            if not methods:
                # nothing to do here
                continue
            api = API(section=section, doc=section_details.doc)
            self.api_list.append(api)
            for method_details in methods:
                api.add_method(method_details)

        Class.optimize()

    def sources(self) -> Generator[str, None, None]:
        """
        Generator for sources of all APIs
        """
        for api in self.api_list:
            yield from api.sources()

    def dunder_all(self) -> str:
        """
        get __all__ = [...]
        :return:
        """

        def class_names(from_class: Class, attrs_only: bool = False) -> Generator[str, None, None]:
            if from_class.base:
                base_class = Class.registry[from_class.base]
                yield from class_names(base_class)

            for attr in from_class.attributes:
                if attr.param_class:
                    yield from class_names(attr.param_class)
            if not attrs_only and from_class.attributes:
                yield from_class.name
            return

        # collect names of classes
        names = set()
        for api in self.api_list:
            names.add(api.api_class_name)
            for method in api.methods:
                if method.response_class:
                    names.update(class_names(method.response_class))
                if method.body_class:
                    names.update(class_names(method.body_class, attrs_only=True))
        names = sorted(names)
        first_line_prefix = '__all__ = ['
        line = f"""{', '.join(f"'{n}'" for n in names)}]"""
        line = '\n'.join(break_lines(line=line,
                                     line_start=' ' * len(first_line_prefix),
                                     first_line_prefix=first_line_prefix))
        return f'{first_line_prefix}{line}'

    def run(self):
        """
        Generate all sources and write to output
        """
        print(PY_HEADER.strip('\n'), file=self.output)
        print('\n', file=self.output)
        print(self.dunder_all(), file=self.output)
        print('\n', file=self.output)
        print('\n\n'.join(self.sources()), file=self.output)


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()

    parser.add_argument('api_spec')
    parser.add_argument('-o', '--output', dest='output_path', action='store', required=False, type=str,
                        help='Write output to given file.')
    # enable debug output to stderr
    parser.add_argument('-d', '--debug', action='store_true', help='show debugs on console')

    # write detailed logs (debug level) to a file
    parser.add_argument('-l', '--logfile', dest='log_path', action='store', required=False, type=str,
                        help='Write detailed logs to this file.')

    # limit output to a single section
    parser.add_argument('--section', type=str,
                        help='Limit output to a single section. Example --section "Meeting chats"')

    args = parser.parse_args()

    setup_logging(console_level=logging.DEBUG if args.debug else logging.INFO,
                  log_path=args.log_path)

    @contextmanager
    def output_file():
        if args.output_path:
            with open(args.output_path, mode='w') as f:
                print(f'writing to {args.output_path}', file=stderr)
                yield f
        else:
            yield stdout

    with output_file() as output:
        print(f'reading API spec from {args.api_spec}', file=stderr)
        api_spec = DocMethodDetails.from_yml(args.api_spec)

        class_generator = ClassGenerator(output=output)
        class_generator.from_doc_method_details(api_spec, only_section=args.section)
        class_generator.run()

    # with
    return


if __name__ == '__main__':
    main()
    exit(0)

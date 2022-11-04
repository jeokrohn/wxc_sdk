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
import argparse
import json
import logging
import re
from collections import Counter
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import chain
from json import JSONDecodeError
from sys import stderr, stdout
from typing import TextIO, Optional

from scraper import DocMethodDetails, Parameter, Class

collected_types = list()

log = logging.getLogger()


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
class ClassGenerator:
    output: TextIO

    @staticmethod
    def parameters_from_url(url: str) -> list[str]:
        """
        get list of URL parameters from URL

        Paraméters in URL are strings like "{locationId}". Parameters are returned in CamelCase

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
        type_str = ClassGenerator.base_type(parameter.type)

        if type_str == 'enum' or type_str == 'object' or type_str == 'string':
            # class name based on attribute name
            class_name = parameter.name
            class_name = f'{class_name[0].upper()}{class_name[1:]}'
        else:
            # class name is in type_str
            class_name = type_str

        return class_name

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

        # if the class name has multiple word then make camel case
        class_name = ''.join(f'{w[0].upper()}{w[1:]}' for w in class_name.split())
        # strip illegal characters from class names
        class_name = re.sub(r'\W', '', class_name)

        new_class = Class(name=class_name, attributes=attributes, is_enum=as_enum)
        log.debug(
            f'create class: {new_class.name} - {", ".join(f"{attr.name}({attr.type})" for attr in attributes)}')
        return new_class

    def classes_from_doc_method_details(self, api_spec: DocMethodDetails):
        """
        Read API spec and identify classes for objects in the API spec

        :param api_spec:
        :return:
        """

        # go through all methods

        # for each method look at request and response body parameters

        # each response body is a class be definition?
        # * maybe not for simple lists
        # * .. other exceptions?

        # else every parameter with attributes is a class
        # * param_attrs only for enums
        # * param_object is a class
        for method in api_spec.methods():
            # look at "Body Parameters" and "Response Properties"
            method_name = self.method_name_from_header(method.method_details.header)
            if body := method.method_details.parameters_and_response.get('Body Parameters'):
                self.create_class(class_name=f'{method_name}Body', attributes=body)
            if response := method.method_details.parameters_and_response.get('Response Properties'):
                self.create_class(class_name=f'{method_name}Response', attributes=response)
        Class.optimize()

    @staticmethod
    def sources() -> Generator[str, None, None]:
        """
        Generator for sources of all classes
        """
        yield from Class.all_sources()


def validate_parameters(api_spec: DocMethodDetails):
    """
    Some validation of parameters
    :param api_spec:
    :return:
    """
    types_with_attrs = Counter(ClassGenerator.class_name(attr.parameter) for attr in api_spec.attributes()
                               if attr.parameter.param_attrs)
    types_with_object = Counter(ClassGenerator.class_name(attr.parameter) for attr in api_spec.attributes()
                                if attr.parameter.param_object)
    parameters_and_response_keys = set(chain.from_iterable(m.method_details.parameters_and_response
                                                           for m in api_spec.methods()))
    requests = [
        f'{ClassGenerator.method_name_from_header(m.method_details.header)}/' \
        f'{ClassGenerator.method_from_url(m.method_details.documentation.endpoint)}'
        for m in api_spec.methods()]

    foo = 1


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()

    parser.add_argument('api_spec')
    parser.add_argument('-o', '--output', dest='output_path', action='store', required=False, type=str,
                        help=f'Write output to given file.')
    # enable debug output to stderr
    parser.add_argument('-d', '--debug', action='store_true', help='show debugs on console')

    # write detailed logs (debug level) to a file
    parser.add_argument('-l', '--logfile', dest='log_path', action='store', required=False, type=str,
                        help=f'Write detailed logs to this file.')


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

        validate_parameters(api_spec)

        class_generator = ClassGenerator(output=output)
        class_generator.classes_from_doc_method_details(api_spec)
        print('from wxc_sdk.base import ApiModel', file=output)
        print('from enum import Enum', file=output)
        print('from typing import Optional', file=output)
        print('from pydantic import Field', file=output)
        print('\n', file=output)
        print('\n\n'.join(class_generator.sources()), file=output)

    # with
    return


if __name__ == '__main__':
    main()
    exit(0)

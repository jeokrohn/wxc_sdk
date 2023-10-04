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

    def cleanup(self):
        self.class_registry.normalize()

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



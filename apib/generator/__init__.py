import os
from collections.abc import Generator
from dataclasses import dataclass
from itertools import chain
from typing import NamedTuple

from apib.apib import read_api_blueprint, ApibParseResult
from apib.python_class import PythonClassRegistry, Endpoint
from apib.tools import break_line

PREAMBLE = """from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum"""


class PythonTypeFromHintAndSampleResult(NamedTuple):
    sample: str
    python_type: str


@dataclass(repr=False, init=False)
class CodeGenerator:
    # True -> include sources for unreferenced classes
    with_unreferenced_classes: bool

    class_registry: PythonClassRegistry

    #: Dictionary of parsed APIB files. Indexed by basename of APIB file w/o suffix
    parsed_blueprints: dict[str, ApibParseResult]

    def __init__(self, with_unreferenced_classes: bool = False):
        self.class_registry = PythonClassRegistry()
        self.parsed_blueprints = dict()
        self.with_unreferenced_classes = with_unreferenced_classes

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
        return self.class_registry.endpoints()

    def source(self, with_example: bool = True) -> str:
        """
        Generate Python source for the APIB files read
            * dataclasses
            * API classes
        """
        apis = [api for _, api in self.class_registry.apis()]

        # set of names of classes referenced by endpoints
        referenced_classes: set[str] = set()
        api_sources = [api.source(class_names=referenced_classes) for api in apis]

        # also add classes to referenced classes that are referenced by attributes of referenced classes
        class_names_to_check = list(referenced_classes)
        while class_names_to_check:
            class_name_to_check = class_names_to_check.pop()
            class_to_check = self.class_registry.get(class_name_to_check)
            if class_to_check is None:
                # class not in class registry; this can happen for the name of the API class
                continue

            if (bc := class_to_check.baseclass) and bc not in referenced_classes:
                # class has a baseclass that we need to keep track of
                referenced_classes.add(bc)
                class_names_to_check.append(bc)

            if not class_to_check.attributes:
                # if a class doesn't have attributes then we can ignore the reference
                referenced_classes.remove(class_to_check.name)

            # check for referenced classes in all attributes
            for attr in class_to_check.attributes:
                if (rc := attr.referenced_class) and rc not in referenced_classes:
                    # attribute references a class we are not yet aware off
                    referenced_classes.add(rc)
                    class_names_to_check.append(rc)
                # if
            # for
        # while

        class_sources: list[str] = list()
        for python_class in self.class_registry.classes():
            if not self.with_unreferenced_classes and python_class.name not in referenced_classes:
                continue
            class_source = python_class.source(with_example=with_example)
            if class_source:
                referenced_classes.add(python_class.name)
                class_sources.append(class_source)

        # __all__ with all class names
        auto_src = f"""__all__ = [{", ".join(f"'{c}'" for c in sorted(referenced_classes))}]"""
        auto_src = '\n'.join(break_line(auto_src, width=120, prefix=' ' * 11, prefix_first_line=''))

        source = '\n\n\n'.join(chain.from_iterable(((PREAMBLE, auto_src), class_sources)))
        source = source.strip()
        nl = '\n'
        # source = f'{source}{nl}'
        source = f'{source}{nl * 3}{(nl * 2).join(f"{api_source}" for api_source in api_sources)}'

        return source

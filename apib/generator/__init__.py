import os
from collections import defaultdict
from collections.abc import Generator
from dataclasses import dataclass
from functools import reduce
from itertools import chain
from typing import NamedTuple

from apib.apib import read_api_blueprint, ApibParseResult
from apib.python_class import PythonClassRegistry, Endpoint
from apib.tools import break_line

PREAMBLE = """from collections.abc import Generator
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
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

    def __init__(self):
        self.class_registry = PythonClassRegistry()
        self.parsed_blueprints = dict()

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

    def source(self) -> str:
        """
        Generate Python source for the APIB files read
            * dataclasses
            * API classes
        """
        apis = [api for _, api in self.class_registry.apis()]
        api_sources = [api.source() for api in apis]

        class_names = []
        class_sources = []

        for python_class in self.class_registry.classes():
            source = python_class.source()
            if not source:
                continue
            class_names.append(python_class.name)
            class_sources.append(source)
        # __auto__ with all class names
        auto_src = f"""__auto__ = [{", ".join(f"'{c}'" for c in sorted(class_names))}]"""
        auto_src = '\n'.join(break_line(auto_src, width=120, prefix=' ' * 12, prefix_first_line=''))
        source = '\n\n\n'.join(chain.from_iterable(((PREAMBLE, auto_src), class_sources)))
        source = source.strip()
        nl = '\n'
        # source = f'{source}{nl}'
        source = f'{source}{nl * 3}{(nl * 2).join(f"{api_source}{nl}    ..." for api_source in api_sources)}'

        return source

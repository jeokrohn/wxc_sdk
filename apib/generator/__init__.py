from dataclasses import dataclass
from itertools import chain

from apib.apib import read_api_blueprint, ApibParseResult
from apib.python_class import PythonClassRegistry

PREAMBLE = """
from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum"""

@dataclass(repr=False, init=False)
class CodeGenerator:
    class_registry: PythonClassRegistry

    def __init__(self):
        self.class_registry = PythonClassRegistry()

    def read_blueprint(self, apib_path):
        # read api bluepring file
        data = read_api_blueprint(apib_path)

        # parse data
        parsed = ApibParseResult.model_validate(data)

        # register all classes from parsed result
        # TODO: allow to register multiple APIB files with identical class names
        #   in that case a new classname is created for the 2nd class and the references in the data from the APIB
        #   file are updated
        list(map(self.class_registry.add, parsed.python_classes()))

    def optimize(self):
        self.class_registry.eliminate_redundancies()
        ...

    def source(self)->str:
        class_names = []
        class_sources = [class_names.append(c.name) or s for c in self.class_registry.classes() if (s := c.source())]
        auto_src = f"""__auto__ = [{", ".join(f"'{c}'" for c in sorted(class_names))}]"""
        source = '\n\n\n'.join(chain.from_iterable(((PREAMBLE, auto_src), class_sources)))
        source = source.strip()+'\n'
        return source

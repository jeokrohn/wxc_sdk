"""
Code generator
"""
from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional

from apib.api_blueprint import ParseResult

__all__ = ['Endpoint', 'CodeGenerator']


@dataclass
class Endpoint:
    host: str
    href: str


@dataclass
class CodeGenerator:
    parse_result: ParseResult

    def __post_init__(self):
        if self.parse_result.api is None:
            raise ValueError('Got no API info')

    @property
    def api_docstring(self) -> Optional[str]:
        return self.parse_result.api.doc_string

    def endpoints(self) -> Generator[Endpoint, None, None]:
        for transition in self.parse_result.api.transitions():
            foo = 1
        foo = 1
        ...

#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "aenum",
#     "aiohttp",
#     "pydantic",
#     "python-dateutil",
#     "pytz",
#     "PyYAML",
#     "requests",
#     "requests-toolbelt"
# ]
# ///

"""
Create a Markdown reference of SDK methods and their endpoint URLs.

Endpoint and HTTP-method resolution lives in :mod:`script.sdk_sync._endpoint_resolver`
so :mod:`script.sdk_sync.ir` can share the same logic when extracting SDK URL
templates from helper-method-driven classes.
"""

from __future__ import annotations

import argparse
import inspect
import os
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, parent_dir)

from script.sdk_sync._endpoint_resolver import (
    Placeholder,
    child_apis,
    default_value,
    endpoint_calls,
    env_value,
    eval_expr,
    function_ast,
    normalize_endpoint,
    request_calls,
    resolve_call,
    resolve_endpoint,
    resolve_http_method,
)
from wxc_sdk import WebexSimpleApi

__all__ = [
    'EndpointReference',
    'IGNORE_METHODS',
    'Placeholder',
    'RST_PREFIX',
    'child_apis',
    'default_value',
    'endpoint_calls',
    'endpoint_reference',
    'env_value',
    'eval_expr',
    'function_ast',
    'is_base_attr',
    'main',
    'markdown_table',
    'md_cell',
    'method_class_path',
    'method_description',
    'mod_path',
    'normalize_endpoint',
    'obj_methods',
    'parse_args',
    'request_calls',
    'resolve_call',
    'resolve_endpoint',
    'resolve_http_method',
    'rst_description',
    'rst_description_text',
    'rst_row',
    'rst_table',
]

IGNORE_METHODS = {'ep', 'f_ep', 'url'}
RST_PREFIX = """
Reference of all available endpoints
====================================

The following table contains a reference of all SDK methods with their HTTP method, endpoint URL, and a short
description of the operation. The method name is a link to the method documentation.

.. list-table::
   :header-rows: 1

   * - Method"""


@dataclass
class EndpointReference:
    """
    One row in the generated endpoint reference.

    :param method: Fully-qualified SDK method name, for example ``api.people.list``.
    :param http_method: HTTP verb used by the SDK method, for example ``GET``.
    :param endpoint: Relative or absolute endpoint URL, for example ``/people`` or
        ``https://analytics.webexapis.com/v1/meeting/qualities``.
    :param description: First non-empty line of the method docstring.
    :param class_path: Fully-qualified Python path used for the Sphinx ``:meth:`` link.
    """

    method: str
    http_method: str
    endpoint: str
    description: str
    class_path: str


def is_base_attr(*, base: type[Any], name: str, attr: Any) -> bool:
    """
    Check whether ``name`` resolves to the same attribute on a base class.

    This is used to filter inherited methods from the exported reference so only
    methods introduced by the concrete API class are listed.

    :param base: Base class to inspect.
    :param name: Attribute name to look up.
    :param attr: Attribute object taken from the concrete child class.
    :return: ``True`` if the base class exposes the same attribute object.
    """
    try:
        base_attr = getattr(base, name)
    except AttributeError:
        return False
    return bool(base_attr == attr)


def obj_methods(obj: Any) -> Iterator[str]:
    """
    Get names of all methods defined in the object class and not inherited from a base class.

    The SDK API tree contains many helper methods inherited from :class:`ApiChild`.
    Those helpers are intentionally excluded so the output focuses on user-facing SDK
    calls.

    :param obj: API object to inspect.
    :return: Iterator of method names such as ``list`` or ``details``.
    """
    bases = obj.__class__.__bases__
    obj_class = obj.__class__
    for name in dir(obj_class):
        if name.startswith('_'):
            continue
        if name in IGNORE_METHODS:
            continue
        attr = getattr(obj_class, name)
        if not callable(attr):
            continue
        if any(is_base_attr(base=base, name=name, attr=attr) for base in bases):
            continue
        yield name


def mod_path(path: str) -> str:
    """
    Convert a filesystem path to a dotted Python module path.

    This mirrors the helper in ``script/method_ref.py`` so the generated RST can link
    to the exact same method documentation targets.

    :param path: Filesystem path ending in ``.py``.
    :return: Dotted module path without the trailing ``.__init__`` part.

    Example:
        ``wxc_sdk/people/__init__.py`` becomes ``wxc_sdk.people``.
    """

    def splitall(current: str) -> Iterator[str]:
        split = os.path.split(current)
        if split[0]:
            yield from splitall(split[0])
        yield split[1]

    path = path[:-3]
    parts = list(splitall(path))
    if parts[-1] == '__init__':
        parts = parts[:-1]
    return '.'.join(parts)


def method_class_path(obj: Any, method_name: str) -> str:
    """
    Build the Sphinx cross-reference target for a method.

    :param obj: Live API object the method belongs to.
    :param method_name: Name of the method on ``obj``.
    :return: Cross-reference target such as
        ``wxc_sdk.people.PeopleApi.list``.
    """
    class_file = inspect.getfile(obj.__class__)
    common_prefix = os.path.commonpath([class_file, __file__])
    rel_path = os.path.relpath(class_file, common_prefix)
    module_path = mod_path(rel_path)
    return f'{module_path}.{obj.__class__.__name__}.{method_name}'


def method_description(obj: Any, method_name: str) -> str:
    """
    Return the first non-empty line of a method's docstring.

    The generated table is intentionally compact, so we only keep the first meaningful
    docstring line rather than the full block.

    :param obj: Live API object the method belongs to.
    :param method_name: Name of the method on ``obj``.
    :return: First non-empty docstring line, or an empty string if no docstring exists.
    """
    bound_method = getattr(obj, method_name)
    doc = inspect.getdoc(bound_method) or ''
    for line in doc.splitlines():
        line = line.strip()
        if line:
            return line
    return ''


def rst_description(obj: Any, method_name: str) -> str:
    """
    Return the short description style used by ``method_ref.rst``.

    The existing method reference keeps the first sentence of the first non-empty line,
    so the RST output of this generator follows the same convention for consistency.

    :param obj: Live API object the method belongs to.
    :param method_name: Name of the method on ``obj``.
    :return: Short one-line description without a trailing period when possible.
    """
    doc = method_description(obj, method_name)
    if not doc:
        return ''
    return doc.split('.')[0].strip()


def md_cell(text: str) -> str:
    """
    Escape Markdown table cell content.

    :param text: Raw cell text.
    :return: Escaped text safe to embed between ``|`` separators.
    """
    return text.replace('|', '\\|')


def endpoint_reference(name: str, obj: Any) -> Iterator[EndpointReference]:
    """
    Walk the API tree recursively and yield reference rows.

    :param name: Dotted prefix representing the current API object in the exported
        hierarchy, for example ``api.people``.
    :param obj: Current API object to inspect.
    :return: Iterator of :class:`EndpointReference` rows.

    Example:
        Starting with ``("api", WebexSimpleApi(...))`` yields rows such as
        ``EndpointReference(method="api.people.list", http_method="GET",
        endpoint="/people", description="List people in your organization...")``.
    """
    methods = sorted(obj_methods(obj))
    for method in methods:
        endpoint = resolve_endpoint(obj, method)
        http_method = resolve_http_method(obj, method)
        if endpoint and http_method:
            yield EndpointReference(
                method=f'{name}.{method}',
                http_method=http_method,
                endpoint=endpoint,
                description=method_description(obj, method),
                class_path=method_class_path(obj, method),
            )

    for child_name, child in child_apis(obj):
        yield from endpoint_reference(f'{name}.{child_name}', child)


def markdown_table(rows: list[EndpointReference]) -> str:
    """
    Render endpoint reference rows as a Markdown table.

    :param rows: Resolved endpoint reference rows.
    :return: Markdown document content.
    """
    lines = [
        '# Endpoint Reference',
        '',
        '| Endpoint | HTTP Method | Endpoint URL | Description |',
        '| --- | --- | --- | --- |',
    ]
    for row in rows:
        lines.append(f'| `{row.method}` | `{row.http_method}` | `{row.endpoint}` | {md_cell(row.description)} |')
    lines.append('')
    return '\n'.join(lines)


def rst_row(row: EndpointReference) -> str:
    """
    Render one endpoint reference row in the list-table format used by Sphinx.

    The table keeps a single visible column like ``method_ref.rst``. The description,
    HTTP method, and URL are emitted as separate indented lines below the method link
    so the document stays readable in narrower layouts.

    :param row: Endpoint reference row to render.
    :return: RST snippet for a single ``.. list-table::`` item.
    """
    description = rst_description_text(row.description)
    return (
        f'\n   * - :meth:`{row.method} <{row.class_path}>`\n'
        f'        | {description}\n'
        f'        | ``{row.http_method} {row.endpoint}``'
    )


def rst_description_text(description: str) -> str:
    """
    Normalize the description line used in the RST table.

    :param description: Raw description stored on the row.
    :return: Shortened description compatible with ``method_ref.rst`` style.
    """
    if not description:
        return ''
    return description.split('.')[0].strip()


def rst_table(rows: list[EndpointReference]) -> str:
    """
    Render endpoint reference rows as an RST list-table document.

    :param rows: Resolved endpoint reference rows.
    :return: RST document content suitable for ``docs/user``.
    """
    content = [RST_PREFIX]
    for row in rows:
        content.append(rst_row(row))
    content.append('\n')
    return ''.join(content)


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    :return: Parsed CLI namespace with ``format`` and ``output_path`` attributes.

    Example:
        ``script/endpoint_ref.py docs/user/endpoint_ref.rst --format rst`` writes the
        RST reference to ``docs/user/endpoint_ref.rst``.
    """
    parser = argparse.ArgumentParser(description='Generate an SDK endpoint reference in Markdown or RST format.')
    parser.add_argument(
        'output_path',
        help='output file path, or "-" to write to stdout',
    )
    parser.add_argument(
        '--format',
        choices=('md', 'rst'),
        default='md',
        help='output format to generate (default: md)',
    )
    return parser.parse_args()


def main() -> None:
    """
    Generate endpoint reference from the current SDK source tree.

    The script instantiates :class:`WebexSimpleApi` with a dummy token because endpoint
    discovery only needs the in-memory API object graph, not real network access.
    The caller must provide the output destination as a positional argument. Use ``-``
    to write the generated document to stdout.
    """
    args = parse_args()
    api = WebexSimpleApi(tokens='dummy')
    rows = sorted(endpoint_reference('api', api), key=lambda row: row.method)
    rendered = markdown_table(rows) if args.format == 'md' else rst_table(rows)
    path = args.output_path

    if path == '-':
        sys.stdout.write(rendered)
        return

    with open(path, mode='w', encoding='utf-8') as f:
        f.write(rendered)

    print(f'wrote {len(rows)} endpoint references to {path}')


if __name__ == '__main__':
    main()

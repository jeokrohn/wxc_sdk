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
"""

from __future__ import annotations

import argparse
import ast
import inspect
import os
import sys
import textwrap
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, parent_dir)

from wxc_sdk import WebexSimpleApi
from wxc_sdk.api_child import ApiChild
from wxc_sdk.rest import RestSession

IGNORE_METHODS = {'ep', 'f_ep', 'url'}
HTTP_METHOD_NAMES = {'get', 'post', 'put', 'delete', 'patch'}
REST_HTTP_METHOD_NAMES = {'rest_get', 'rest_post', 'rest_put', 'rest_delete', 'rest_patch'}
RST_PREFIX = """
Reference of all available endpoints
====================================

The following table contains a reference of all SDK methods with their HTTP method, endpoint URL, and a short
description of the operation. The method name is a link to the method documentation.

.. list-table::
   :header-rows: 1

   * - Method"""


class Placeholder(str):
    """
    Placeholder value for endpoint parameters.

    The generator never executes real API calls. Instead it substitutes values such as
    ``person_id`` with placeholders like ``{person_id}`` so helper methods can still
    build human-readable endpoint paths.

    Example:
        ``Placeholder("person_id")`` renders as ``"{person_id}"``.
    """

    name: str

    def __new__(cls, name: str) -> Placeholder:
        obj = super().__new__(cls, f'{{{name}}}')
        obj.name = name
        return obj


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


def child_apis(obj: Any) -> Iterator[tuple[str, ApiChild]]:
    """
    Yield child API objects attached to ``obj``.

    The generator walks the SDK tree recursively starting at ``WebexSimpleApi``.
    Child APIs are stored as instance attributes whose values are ``ApiChild``
    instances.

    :param obj: API object whose attributes should be inspected.
    :return: Iterator of ``(attribute_name, child_api)`` tuples sorted by name.
    """
    names = [name for name, value in obj.__dict__.items() if isinstance(value, ApiChild)]
    names.sort()
    for name in names:
        yield name, getattr(obj, name)


def default_value(name: str) -> Any:
    """
    Create a placeholder for a function argument.

    :param name: Parameter name from a method signature.
    :return: A :class:`Placeholder` instance such as ``{location_id}``.
    """
    return Placeholder(name)


def env_value(parameter: inspect.Parameter) -> Any:
    """
    Choose the synthetic runtime value used while evaluating AST expressions.

    Literal defaults such as ``"analytics-calling.webexapis.com"`` are preserved
    because they often materially affect the resolved URL. Boolean defaults are *not*
    preserved: when a method chooses between two endpoint paths based on a boolean
    flag, we prefer to keep both possibilities visible in the generated reference.
    All other values are replaced with named placeholders.

    :param parameter: Function parameter from :func:`inspect.signature`.
    :return: Either the literal default value or a placeholder string.
    """
    if parameter.default is not inspect.Parameter.empty and (
        isinstance(parameter.default, str)
        or (isinstance(parameter.default, (int, float)) and not isinstance(parameter.default, bool))
    ):
        return parameter.default
    return default_value(parameter.name)


def eval_expr(node: ast.AST, env: dict[str, Any]) -> Any:
    """
    Evaluate a limited subset of Python AST nodes into placeholder-friendly values.

    This is the core of the generator. Rather than executing SDK methods, we inspect
    their source and reduce only the expression types that are commonly used to build
    URLs. That keeps the evaluation deterministic and safe while still understanding
    patterns such as:

    - ``self.ep(f"{person_id}/features/voicemail")``
    - ``self.session.ep("reports")``
    - ``urllib.parse.quote(phone_number_id)``
    - ``enum_str(schedule_type)``

    Unsupported node types intentionally raise ``ValueError`` so callers can fall back
    to other heuristics instead of silently inventing endpoints.

    :param node: AST node to evaluate.
    :param env: Synthetic evaluation environment mapping parameter names to literal
        defaults or placeholders.
    :return: A Python value, usually a string suitable for endpoint construction.

    Example:
        Evaluating the f-string AST for ``f"people/{person_id}"`` returns
        ``"people/{person_id}"``.
    """
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return env.get(node.id, default_value(node.id))
    if isinstance(node, ast.Attribute):
        value = eval_expr(node.value, env)
        if isinstance(value, Placeholder):
            return Placeholder(node.attr)
        return Placeholder(node.attr)
    if isinstance(node, ast.JoinedStr):
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                parts.append(str(value.value))
            elif isinstance(value, ast.FormattedValue):
                parts.append(str(eval_expr(value.value, env)))
        return ''.join(parts)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return f'{eval_expr(node.left, env)}{eval_expr(node.right, env)}'
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -eval_expr(node.operand, env)
    if isinstance(node, ast.List):
        return [eval_expr(elt, env) for elt in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(eval_expr(elt, env) for elt in node.elts)
    if isinstance(node, ast.Dict):
        return {eval_expr(k, env): eval_expr(v, env) for k, v in zip(node.keys, node.values) if k is not None}
    if isinstance(node, ast.IfExp):
        test_value = eval_expr(node.test, env)
        if isinstance(test_value, bool):
            return eval_expr(node.body if test_value else node.orelse, env)
        body_value = eval_expr(node.body, env)
        orelse_value = eval_expr(node.orelse, env)
        if body_value == orelse_value:
            return body_value
        return f'{{{body_value}|{orelse_value}}}'
    if isinstance(node, ast.Call):
        func = node.func
        if isinstance(func, ast.Name):
            if func.id in {'str', 'repr', 'enum_str'} and node.args:
                return eval_expr(node.args[0], env)
        if isinstance(func, ast.Attribute):
            if func.attr == 'quote' and node.args:
                return eval_expr(node.args[0], env)
        if node.args:
            return eval_expr(node.args[0], env)
    raise ValueError(f'Unsupported AST node for endpoint resolution: {ast.dump(node, include_attributes=False)}')


def function_ast(func: Any) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    """
    Parse a function object into its top-level AST node.

    :param func: Function or bound method implementation.
    :return: Parsed ``FunctionDef``/``AsyncFunctionDef`` node, or ``None`` when the
        source does not parse into a function body.
    """
    source = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(source)
    function = tree.body[0]
    if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return None
    return function


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


def endpoint_calls(func: Any) -> list[ast.Call]:
    """
    Return endpoint-building calls in source order.

    We deliberately collect more than just direct ``self.ep(...)`` calls because the
    SDK uses several recurring helper styles:

    - ``self.ep(...)`` and ``self.f_ep(...)``
    - helper wrappers such as ``self._endpoint(...)`` or ``self._url(...)``
    - ``self.session.ep(...)`` / ``self._session.ep(...)``
    - ``super().ep(...)`` in helper implementations

    These calls are later replayed with placeholder arguments to recover the endpoint.

    :param func: Function or bound method implementation.
    :return: Ordered list of candidate AST call nodes.

    Example:
        For a method containing ``url = self._endpoint(location_id=location_id)``, the
        returned list contains the ``self._endpoint(...)`` call node.
    """
    function = function_ast(func)
    if function is None:
        return []

    calls = []

    class Visitor(ast.NodeVisitor):
        """
        Collect only URL-construction calls that are useful for endpoint recovery.
        """

        def visit_Call(self, node: ast.Call) -> None:
            func_node = node.func
            if isinstance(func_node, ast.Attribute):
                if (
                    isinstance(func_node.value, ast.Name)
                    and func_node.value.id == 'self'
                    and (func_node.attr in {'ep', 'f_ep'} or 'endpoint' in func_node.attr or 'url' in func_node.attr)
                ):
                    calls.append(node)
                elif (
                    isinstance(func_node.value, ast.Attribute)
                    and isinstance(func_node.value.value, ast.Name)
                    and func_node.value.value.id == 'self'
                    and func_node.value.attr in {'session', '_session'}
                    and func_node.attr == 'ep'
                ):
                    calls.append(node)
                elif (
                    func_node.attr == 'ep'
                    and isinstance(func_node.value, ast.Call)
                    and isinstance(func_node.value.func, ast.Name)
                    and func_node.value.func.id == 'super'
                ):
                    calls.append(node)
            self.generic_visit(node)

    Visitor().visit(function)
    return calls


def request_calls(func: Any) -> list[ast.Call]:
    """
    Return request-executing calls in source order.

    Endpoint resolution and HTTP verb resolution are intentionally separate. This
    function only identifies the call that actually performs the request, such as
    ``self.get(...)`` or ``self.session.follow_pagination(...)``.

    :param func: Function or bound method implementation.
    :return: Ordered list of request-like AST call nodes.

    Example:
        ``return self.session.follow_pagination(url=url, ...)`` produces a single call
        that later maps to ``GET``.
    """
    source = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(source)
    function = tree.body[0]
    if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return []

    calls = []

    class Visitor(ast.NodeVisitor):
        """
        Collect request execution calls while ignoring ordinary helper invocations.
        """

        def visit_Call(self, node: ast.Call) -> None:
            func_node = node.func
            if isinstance(func_node, ast.Attribute):
                if func_node.attr in HTTP_METHOD_NAMES | REST_HTTP_METHOD_NAMES | {'_upload_or_modify'}:
                    calls.append(node)
                elif (
                    isinstance(func_node.value, ast.Attribute)
                    and isinstance(func_node.value.value, ast.Name)
                    and func_node.value.value.id == 'self'
                    and func_node.value.attr in {'session', '_session'}
                    and func_node.attr == 'follow_pagination'
                ):
                    calls.append(node)
            elif isinstance(func_node, ast.Name) and func_node.id == 'meth':
                calls.append(node)
            self.generic_visit(node)

    Visitor().visit(function)
    return calls


def normalize_endpoint(url: str, base: str | None = None) -> str:
    """
    Normalize an endpoint into the user-facing form written to the Markdown table.

    The SDK mixes several styles:

    - full ``https://webexapis.com/v1/...`` URLs
    - relative API paths such as ``people`` or ``telephony/config/...``
    - absolute non-Webex URLs such as the status and analytics endpoints
    - placeholder-only values such as ``{url}`` for downloader helpers

    This function strips the normal Webex base URL, preserves non-Webex absolute URLs,
    ensures relative paths start with ``/``, and removes duplicated base prefixes that
    can appear when a helper passes a suffix already covered by ``ApiChild.base``.

    :param url: Raw URL/path recovered from the SDK source.
    :param base: ``ApiChild.base`` value of the current API object, if any.
    :return: Normalized endpoint string ready for the Markdown table.

    Example:
        ``https://webexapis.com/v1/people`` becomes ``/people``.
    """
    if url.startswith(RestSession.BASE):
        url = url[len(RestSession.BASE) :]
    elif '://' in url:
        return url
    elif url.startswith('{') and url.endswith('}'):
        return url
    if not url.startswith('/'):
        url = f'/{url}'
    if base:
        repeated_prefix = f'/{base}/{base}/'
        if url.startswith(repeated_prefix):
            url = f'/{base}/{url[len(repeated_prefix) :]}'
    return url


def resolve_call(obj: Any, call: ast.Call, env: dict[str, Any]) -> str | None:
    """
    Resolve one endpoint-building AST call against a live API object.

    The AST traversal only identifies *which* helper call looks relevant. This function
    evaluates its arguments, replays the helper against the instantiated SDK object, and
    normalizes the resulting endpoint.

    The ``if/elif`` structure mirrors the distinct helper families used in the SDK:

    1. ``self.<helper>(...)``:
       This is the most common case and covers direct calls such as ``self.ep(...)``,
       ``self.f_ep(...)``, ``self._endpoint(...)``, and ``self.url(...)``.
    2. ``self.session.ep(...)`` / ``self._session.ep(...)``:
       Some APIs bypass ``ApiChild.ep()`` and ask the REST session to build a URL
       directly.
    3. ``super().ep(...)``:
       A few helper methods call the ``ApiChild`` implementation explicitly.

    The branches are kept separate because each family needs slightly different
    treatment. In particular, ``self.ep(...)`` can accidentally duplicate the class
    base or wrap an already-absolute URL, while ``self.session.ep(...)`` always starts
    from the raw session base URL.

    :param obj: Live API object the method belongs to.
    :param call: AST call node returned by :func:`endpoint_calls`.
    :param env: Synthetic evaluation environment used for placeholders.
    :return: Resolved endpoint string, or ``None`` if this call shape is unsupported.

    Example:
        Replaying ``self.f_ep(person_id=person_id)`` with
        ``person_id -> {person_id}`` may return
        ``/telephony/config/people/{person_id}/voicemail``.

        Replaying ``self.session.ep("reports")`` returns ``/reports``.
    """
    func_node = call.func
    args = [eval_expr(arg, env) for arg in call.args]
    kwargs = {kw.arg: eval_expr(kw.value, env) for kw in call.keywords if kw.arg}
    base = getattr(obj, 'base', None)

    if isinstance(func_node, ast.Attribute):
        if isinstance(func_node.value, ast.Name) and func_node.value.id == 'self':
            # Branch 1: helper invoked on the API object itself.
            # Some SDK methods pass a full absolute URL into self.ep(...). In that
            # case we must keep the value as-is rather than letting ApiChild.ep()
            # prefix it with the regular Webex API base.
            if func_node.attr == 'ep' and args and isinstance(args[0], str) and '://' in args[0]:
                return normalize_endpoint(args[0], base)
            if func_node.attr == 'ep' and base and args:
                ep_arg = args[0]
                if isinstance(ep_arg, str):
                    # Guard against helpers calling self.ep("jobs/callRecording")
                    # when the class base already is "telephony/config/jobs/callRecording".
                    stripped = ep_arg.strip('/')
                    if stripped and (base == stripped or base.endswith(f'/{stripped}')):
                        return normalize_endpoint(f'/{base}', base)
            target = getattr(obj, func_node.attr, None)
            if callable(target):
                return normalize_endpoint(target(*args, **kwargs), base)
        elif (
            isinstance(func_node.value, ast.Attribute)
            and isinstance(func_node.value.value, ast.Name)
            and func_node.value.value.id == 'self'
            and func_node.value.attr in {'session', '_session'}
            and func_node.attr == 'ep'
        ):
            # Branch 2: endpoint built directly via the attached REST session.
            session = getattr(obj, func_node.value.attr, None)
            if session is not None:
                return normalize_endpoint(session.ep(*args, **kwargs), base)
        elif (
            func_node.attr == 'ep'
            and isinstance(func_node.value, ast.Call)
            and isinstance(func_node.value.func, ast.Name)
            and func_node.value.func.id == 'super'
        ):
            # Branch 3: helper explicitly delegated to the ApiChild base class.
            return normalize_endpoint(super(obj.__class__, obj).ep(*args, **kwargs), base)
    return None


def resolve_endpoint(obj: Any, method_name: str) -> str | None:
    """
    Resolve the endpoint used by a bound SDK method.

    Resolution happens in two passes:

    1. Find and replay explicit endpoint helper calls such as ``self.ep(...)`` or
       ``self._endpoint(...)``.
    2. Fall back to simple literal assignments like ``url = f"https://.../cdr_feed"``
       when the method builds the URL inline instead of via a helper.

    The fallback deliberately skips assigned call expressions because those are already
    handled by the structured helper replay above and are too easy to misinterpret if
    reduced only to a string.

    The nested ``if``/``elif`` handling in the second pass exists for three reasons:

    - ``if isinstance(node, ast.Assign)`` limits the fallback to top-level statements
      in execution order, which lets us build up a simple local environment.
    - ``if isinstance(target, ast.Name)`` ensures we only track plain local variables
      such as ``endpoint`` or ``url``. Tuple unpacking and other assignment shapes are
      ignored on purpose.
    - ``if target.id in {'url', 'ep'}`` restricts final endpoint extraction to the
      conventional variable names used throughout the SDK. This keeps the fallback from
      accidentally treating arbitrary intermediate strings as endpoint URLs.

    In practice, this fallback is what makes manually assembled endpoints like the CDR
    analytics URL work, while still leaving more complicated helper calls to the first
    pass.

    :param obj: Live API object the method belongs to.
    :param method_name: Name of the method on ``obj``.
    :return: Normalized endpoint string, or ``None`` if no safe resolution strategy
        succeeded.

    Example:
        ``api.people.list`` resolves to ``/people``.
    """
    bound_method = getattr(obj, method_name)
    func = getattr(bound_method, '__func__', bound_method)
    signature = inspect.signature(func)
    env = {
        name: env_value(parameter)
        for name, parameter in signature.parameters.items()
        if name != 'self' and parameter.kind not in {inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD}
    }

    for call in endpoint_calls(func):
        try:
            endpoint = resolve_call(obj, call, env)
        except Exception:
            # Some candidate helper calls are intentionally optimistic. If one of them
            # cannot be evaluated safely, we ignore it and continue with the next
            # candidate instead of failing the whole method.
            continue
        if endpoint:
            return endpoint

    function = function_ast(func)
    if function is None:
        return None
    for node in function.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    try:
                        # Track simple local values in source order so later
                        # assignments such as ``url = f".../{endpoint}"`` can resolve
                        # previously assigned names like ``endpoint``.
                        env[target.id] = eval_expr(node.value, env)
                    except Exception:
                        pass
                if isinstance(target, ast.Name) and target.id in {'url', 'ep'}:
                    if isinstance(node.value, ast.Call):
                        # Calls are already handled by the explicit helper replay in
                        # the first pass. Treating them as raw strings here would lose
                        # too much information.
                        continue
                    try:
                        endpoint = normalize_endpoint(str(eval_expr(node.value, env)), getattr(obj, 'base', None))
                    except Exception:
                        continue
                    return endpoint
    if 'url' in env:
        return normalize_endpoint(str(env['url']), getattr(obj, 'base', None))
    return None


def resolve_http_method(obj: Any, method_name: str) -> str | None:
    """
    Resolve the HTTP method used by a bound method.

    The first request-like call in the method body is treated as authoritative. This
    matches the SDK style where one public SDK method typically wraps exactly one REST
    endpoint. The resolver understands:

    - ``self.get/post/put/delete/patch(...)``
    - ``self.session.rest_get/...(...)``
    - ``self.session.follow_pagination(...)`` -> ``GET``
    - announcement upload wrappers that route through ``_upload_or_modify`` or a local
      ``meth`` variable chosen from ``super().post`` / ``super().put``

    The branch order matters:

    1. ``if isinstance(func_node, ast.Name) and func_node.id == 'meth'``:
       Handles the special upload helper pattern where the method is first stored in a
       local variable named ``meth`` and only later invoked.
    2. ``elif isinstance(func_node, ast.Attribute)``:
       Handles the normal SDK request styles.
       Inside this block:
       - ``_upload_or_modify`` is inspected first because it hides whether the
         operation is ``POST`` or ``PUT`` behind an ``is_upload`` flag.
       - ``follow_pagination`` is treated as ``GET`` because it performs paginated
         retrieval.
       - direct ``get/post/put/delete/patch`` methods are then mapped one-to-one.
       - ``rest_get/rest_post/...`` names are finally normalized by stripping the
         ``rest_`` prefix.

    :param obj: Live API object the method belongs to.
    :param method_name: Name of the method on ``obj``.
    :return: HTTP verb such as ``GET`` or ``POST``, or ``None`` if no request call
        could be identified.

    Example:
        A method containing ``return self.session.follow_pagination(...)`` resolves to
        ``GET``.
    """
    bound_method = getattr(obj, method_name)
    func = getattr(bound_method, '__func__', bound_method)
    for call in request_calls(func):
        func_node = call.func
        if isinstance(func_node, ast.Name) and func_node.id == 'meth':
            # Upload helpers sometimes choose between ``super().post`` and
            # ``super().put`` first and only invoke the chosen callable later as
            # ``meth(...)``. The ``is_upload`` flag tells us which verb to report.
            is_upload = next(
                (
                    kw.value.value
                    for kw in call.keywords
                    if kw.arg == 'is_upload' and isinstance(kw.value, ast.Constant)
                ),
                None,
            )
            if is_upload is True:
                return 'POST'
            if is_upload is False:
                return 'PUT'
        elif isinstance(func_node, ast.Attribute):
            if func_node.attr == '_upload_or_modify':
                # Same upload pattern as above, but here the wrapper method is invoked
                # directly instead of through the local ``meth`` variable.
                is_upload = next(
                    (
                        kw.value.value
                        for kw in call.keywords
                        if kw.arg == 'is_upload' and isinstance(kw.value, ast.Constant)
                    ),
                    None,
                )
                if is_upload is True:
                    return 'POST'
                if is_upload is False:
                    return 'PUT'
            if func_node.attr == 'follow_pagination':
                # Pagination helpers always fetch data and therefore correspond to GET.
                return 'GET'
            if func_node.attr in HTTP_METHOD_NAMES:
                return func_node.attr.upper()
            if func_node.attr in REST_HTTP_METHOD_NAMES:
                # rest_get -> GET, rest_post -> POST, ...
                return func_node.attr.split('_', 1)[1].upper()
    return None


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

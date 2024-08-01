#!/usr/bin/env python
"""
Create a reference of all methods available in the SDK
"""

import os

from wxc_sdk import WebexSimpleApi
from wxc_sdk.api_child import ApiChild
import inspect

RST_FILE = 'method_ref.rst'

PREFIX = """
Reference of all available methods
==================================

The following table contains a reference of all methods defined in the SDK with a short description of the operation.
The method name is a link to the method documentation.

.. list-table::
   :header-rows: 1

   * - Method"""

ROW_TEMPLATE = """
   * - :meth:`{method} <{class_path}>`
        {doc}"""

IGNORE_METHODS = {'ep', 'f_ep'}


def is_base_attr(*, base, name, attr):
    """
    Check whether an attribute is defined in the given base class
    :param base: base class
    :param name: name of attribute
    :param attr: attribute value in child class
    """
    try:
        base_attr = getattr(base, name)
    except AttributeError:
        return False
    return base_attr == attr


def obj_methods(obj):
    """
    Get names of all methods defined in the obj and not inherited from a base class
    :param obj:
    :return:
    """
    bases = obj.__class__.__bases__
    obj_class = obj.__class__
    for name in dir(obj_class):
        # ignore all private and dunder methods
        if name.startswith('_'):
            continue
        # ignore some special names
        if name in IGNORE_METHODS:
            continue
        # ignore all non-callables
        attr = getattr(obj_class, name)
        if not callable(attr):
            continue
        # ignore if the same attribute exists in any of the base classes
        if any(is_base_attr(base=base, name=name, attr=attr) for base in bases):
            continue
        yield name


def mod_path(path):
    """
    create a module path based on file path
    :param path:
    :return:
    """

    def splitall(path):
        split = os.path.split(path)
        if split[0]:
            yield from splitall(split[0])
        yield split[1]

    # remove ".py"
    path = path[:-3]
    path = list(splitall(path))
    if path[-1] == '__init__':
        path = path[:-1]
    return '.'.join(path)


def method_reference(name, obj):
    """
    Recursively climb down the attribute hierarchy and yield cross reference information for all methods
    :param name:
    :param obj:
    :return:
    """
    # collect all methods
    methods = list(obj_methods(obj))
    class_path = inspect.getfile(obj.__class__)
    path = __file__
    common = next(i for i, (s1, s2) in enumerate(zip(class_path, path))
                  if s1 != s2)
    class_path = mod_path(class_path[common:])
    class_path = f'{class_path}.{obj.__class__.__name__}'
    for method in methods:
        attr = getattr(obj, method)
        doc = attr.__doc__ or ''
        if doc:
            # get 1st sentence
            doc = doc.strip().split('\n')[0].split('.')[0].strip()
        yield f'{name}.{method}', f'{class_path}.{method}', f'{doc}'

    child_apis = [name for name, value in obj.__dict__.items()
                  if isinstance(value, ApiChild)]
    child_apis.sort()
    for child_name in child_apis:
        yield from method_reference(f'{name}.{child_name}', getattr(obj, child_name))


def main():
    api = WebexSimpleApi(tokens='foo')
    method_list = list(method_reference('api', api))
    print(len(method_list))
    print('\n'.join('/'.join(m) for m in method_list))

    rst_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', RST_FILE))

    with open(rst_path, mode='w') as f:
        f.write(PREFIX)
        for method, class_path, doc in method_list:
            f.write(ROW_TEMPLATE.format(method=method, class_path=class_path, doc=doc))


if __name__ == '__main__':
    main()

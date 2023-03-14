#!/usr/bin/env python
"""
Read API spec and try to group endpoints based on common endpoint parts
"""
import re
from collections.abc import Callable, Generator
from dataclasses import dataclass, field
from io import StringIO
from typing import List, Optional
from urllib.parse import urlparse

from scraper import DocMethodDetails, MethodDetails, Parameter
from classes import ClassGenerator


# TODO: common URL for ApiChild base cannot contain URL parameters
def paginated_method(method: MethodDetails) -> bool:
    """
    determine whether the method requires pagination

    requires pagination if:
        * only returns an array of something
        * has "max" query parameters
    """
    response_attributes = method.parameters_and_response.get('Response Properties')
    if not response_attributes or len(response_attributes) > 1:
        return False
    if not response_attributes[0].type.startswith('array['):
        return False
    p_names = set(p.name
                  for p in method.parameters_and_response.get('Query Parameters', []))
    return 'max' in p_names


@dataclass
class UrlTree:
    node: str = field(default='')
    path: str = field(default='')
    childs: dict[str, 'UrlTree'] = field(init=False, default_factory=dict)
    method_details: Optional[list[MethodDetails]] = field(default_factory=list)

    def insert_path(self, path: str, md: MethodDetails):
        if not path:
            self.method_details.append(md)
            return
        # get first component
        parts = path.split('/')
        first = parts[0]
        if len(parts) == 1 and first.startswith('{'):
            # if only one URL part is left and that is a URL parameter then we are done here
            # .. and add this method to this node
            self.method_details.append(md)
            return
        # ... else climb down the tree and add below
        remaining = '/'.join(parts[1:])
        if not (child := self.childs.get(first)):
            child = UrlTree(node=first, path=self.path and f'{self.path}/{first}' or first)
            self.childs[first] = child
        child.insert_path(remaining, md=md)

    def insert_url(self, url: str, md: MethodDetails):
        if self.node:
            raise ValueError('insert_url() should only be called on root')
        url = url.replace('https:// ', 'https://')
        parsed = urlparse(url)
        if parsed.hostname != 'webexapis.com':
            # we only want to insert
            return
        self.insert_path(path=parsed.path[1:], md=md)

    def descend(self) -> Generator['UrlTree', None, None]:
        yield self
        for child_key in sorted(self.childs):
            yield from self.childs[child_key].descend()

    def cleanup(self):
        """
        find node with only one method. If such a node exists then move that single method one layer up
        """
        # 1st cleanup all childs
        for child in self.childs.values():
            child.cleanup()
        child_keys = list(self.childs)
        for child_key in child_keys:
            child = self.childs[child_key]
            # then check all childs nodes whether they are terminal and only have on methods
            if not child.childs and len(child.method_details) == 1:
                # move that one method one level up
                self.method_details.append(child.method_details[0])
                # .. and get rid of that child node
                self.childs.pop(child_key)
                continue
            # also if there is a child that represents a url parameter then move all methods one up
            if child_key.startswith('{'):
                self.method_details.extend(child.method_details)
                child.method_details = []
                if not child.childs:
                    # if there are no further childs on this child then we can get rid of this child
                    self.childs.pop(child_key)
        return


def main():
    api_spec = DocMethodDetails.from_yml('generated/meetings.yml')

    # start with all endpoints
    tree = UrlTree()
    for m in api_spec.methods():
        if m.section != 'Meetings':
            continue
        tree.insert_url(m.method_details.documentation.endpoint, m.method_details)
    tree.cleanup()
    for node in tree.descend():
        if node.method_details:
            meth_len = max(map(len, (md.documentation.http_method for md in node.method_details)))
            print(node.path)
            for md in node.method_details:
                print(f'  {md.documentation.http_method:{meth_len}} {md.documentation.endpoint}: {md.header}')

    for node in tree.descend():
        if node.method_details:
            # create an API for this set of methods
            with StringIO() as code:
                api = ClassGenerator(output=code)
                api.from_methods(section='', doc='', method_list=node.method_details)
                api.run()
                source = code.getvalue()
            path = node.path
            if path.startswith('v1/'):
                path = path[3:]
            parts = path.split('/')
            parts = [part for part in parts if not part.startswith('{')]
            source_path = f'group_{"_".join(parts)}_auto.py'
            with open(source_path, mode='w') as file:
                print(source, file=file)

    def print_methods(filter_func: Callable[[MethodDetails, list[Parameter], list[Parameter]], bool]):
        ...
        # regex to match array params
        array_re = re.compile(r'^array\[(.+)]$')

        for section, method in api_spec.methods():
            method: MethodDetails
            section: str
            response = method.parameters_and_response.get('Response Properties')
            if response is None:
                # print(f'{section}/{method.header}: no response')
                continue
            array_params = [param for param in response
                            if array_re.match(param.type)]
            non_array_params = [param for param in response
                                if not array_re.match(param.type)]
            if not array_params:
                # print(f'{section}/{method.header}: no array in response')
                continue
            if filter_func(method, array_params, non_array_params):
                print(f'{section}/{method.header}: list(s): {", ".join(p.type for p in array_params)} other: '
                      f'{", ".join(p.type for p in non_array_params)}')
                print(f'  {method.documentation.doc_link}')
        return

    # 'list' calls with not only an array as response
    def filter_list_with_not_only_array(method: MethodDetails,
                                        arrays: list[Parameter],
                                        non_arrays: list[Parameter]) -> bool:
        return method.header.lower().startswith('list') and non_arrays

    def filter_array_only_but_but_not_list(method: MethodDetails,
                                           arrays: list[Parameter],
                                           non_arrays: list[Parameter]) -> bool:
        return arrays and not non_arrays and not method.header.lower().startswith('list')

    print('"List" methods with not only array returns:')
    print_methods(filter_list_with_not_only_array)
    print()
    print('non "List" methods with only array returns:')
    print_methods(filter_array_only_but_but_not_list)
    print()
    print('paginated methods:')
    print_methods(lambda m, x, y: paginated_method(m) and not m.header.lower().startswith('list'))


...

if __name__ == '__main__':
    main()

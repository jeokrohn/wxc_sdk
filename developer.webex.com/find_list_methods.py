#!/usr/bin/env python
"""
Read API spec and find all methods that return a list of items
Then do some consistency checks

Code used to better understand list methods as foundation to improving code generation
"""
import re
from collections.abc import Callable

from scraper import DocMethodDetails, MethodDetails, Parameter


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


def main():
    api_spec = DocMethodDetails.from_yml('generated/api_spec.yml')

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

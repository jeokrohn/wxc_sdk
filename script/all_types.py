#!/usr/bin/env python

"""
find all .py files in ../wxc_sdk
for each source file
    import
    get __all__
    add each item to union __all__
    check that the names are unique
"""

import os.path
import sys
from importlib import import_module
from io import StringIO
from pathlib import Path


def module_name_from_path(path):
    """
    Create a module name from a path
    :param path:
    :return:
    """
    p_split = str(path).split('/')
    wxc_sdk_base = next(i for i in range(100)
                        if p_split[-i] == 'wxc_sdk')
    p_split = p_split[-wxc_sdk_base:]
    p_split[-1] = os.path.splitext(p_split[-1])[0]
    if p_split[-1] == '__init__':
        p_split = p_split[:-1]
    mod_name = '.'.join(p_split)
    return mod_name


def main():
    # all Python sources
    wxc_sdk = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'wxc_sdk'))
    py_files = list(Path(wxc_sdk).rglob('*.py'))
    py_files.sort()
    # module names from paths
    module_names = list(map(module_name_from_path, py_files))

    # a set to collect all identifiers
    combined_all = set()

    # print to a string
    source = StringIO()

    # exclude some sources
    to_skip = ['wxc_sdk',
               'wxc_sdk.api_child',
               'wxc_sdk.integration',
               'wxc_sdk.rest',
               'wxc_sdk.as_rest',
               'wxc_sdk.as_api',
               'wxc_sdk.all_types']
    err = False
    for module_name in module_names:
        if module_name in to_skip:
            continue
        module = import_module(module_name)
        module_all = module.__dict__.get('__all__')
        if module_all is None:
            continue
        names_in_module = []
        for name in module_all:
            if name.endswith('Api'):
                # Apis not needed
                continue
            if name in combined_all:
                print(f'duplicate name {module_name}.{name}', file=sys.stderr)
                err = True
            else:
                combined_all.add(name)
                names_in_module.append(name)
        # import statement for module
        if names_in_module:
            names_in_module.sort()
            line = f'from {module_name} import '
            max_line = 116
            pending_line = ''
            for name in names_in_module:
                entry = f"{name}, "
                if len(line) + len(entry) >= max_line:
                    if pending_line:
                        print(f'{pending_line.rstrip()} \\', file=source)
                    pending_line = line.rstrip()
                    # next line is indented by 4 spaces
                    line = ' ' * 4
                line = f'{line}{entry}'
            if pending_line:
                if line.strip():
                    print(f'{pending_line.rstrip()} \\', file=source)
                    print(f'{line.rstrip(" ,")}', file=source)
                else:
                    print(f'{pending_line.rstrip(" ,")} \\', file=source)
            else:
                print(f'{line.rstrip(" ,")}', file=source)
    if err:
        raise NameError('Duplicate names')

    # create __all__
    print(file=source)
    line = '__all__ = ['
    combined_all = sorted(combined_all)
    max_line = 120
    for name in combined_all:
        entry = f"'{name}', "
        if len(line) + len(entry) >= max_line:
            print(line.rstrip(), file=source)
            line = ' ' * 11

        line = f'{line}{entry}'
    print(f'{line.rstrip(" ,")}]', file=source)
    with open(os.path.join(wxc_sdk, 'all_types.py'), mode='w') as f:
        f.write(source.getvalue())

    print(source.getvalue())
    return


if __name__ == '__main__':
    main()

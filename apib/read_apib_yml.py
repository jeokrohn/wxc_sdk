#!/usr/bin/env/python

"""
Read/play with YML file created from apib by "drafter"
Blueprint files are hosted here: https://sqbu-github.cisco.com/S4D/api-specs
"""
import logging
from glob import glob
from operator import attrgetter
from os.path import splitext

import yaml

from private.api_blueprint import read_api_blueprint, ParseResult


def analyze_content(data: dict, level=0, pre: str = ''):
    """
    look for all 'element' keys in dict (recursive) and dump some info
    """

    def lp(m: str):
        print(f'{" " * (level * 2 + 1)}{pre}{m}')

    element = data.get('element')
    if element:
        content = data.get('content')
        if content:
            lp(f'{element}: {type(content)}')
        else:
            lp(f'{element}: no content')

    # climb down
    for k, v in data.items():
        if isinstance(v, dict):
            lp(k)
            analyze_content(v, level=level + 1)
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            lp(k)
            list(map(lambda e: analyze_content(e, level=level + 1, pre='- '), v))
            print()


def print_metas(data: dict):
    if meta := data.get('meta'):
        print(meta)
    for k, v in data.items():
        if isinstance(v, list):
            list(map(print_metas, v))
        elif isinstance(v, dict):
            print_metas(v)


def parse_one(path: str):
    data = read_api_blueprint(path)
    # dump a YAML file for debugging purposes
    yml_path = f'{splitext(path)[0]}.yml'
    with open(yml_path, mode='w') as f:
        yaml.safe_dump(data, f)
    try:
        parsed = ParseResult.model_validate(data)
    except Exception as e:
        print(f'{path} failed: {e}')
        parsed = None
        raise
    return parsed


def validate_parse_result(parsed: ParseResult):
    # print enums
    for enum_def in sorted(parsed.api.data_structures.enums, key=attrgetter('id')):
        print(f'{enum_def.id}: {", ".join(enum_el.normalized_value for enum_el in enum_def.enumerations)}')
    # print data structures
    # print methods
    for resource in parsed.api.resource:
        for methods_def in resource.methods:
            foo = 1
    ...


def parse_all():
    blueprint_files = glob('api-specs-master/blueprint/webexapis.com/v1/*.apib')
    for path in blueprint_files:
        parsed = parse_one(path)
        if parsed:
            validate_parse_result(parsed)

    # list(map(parse_one, blueprint_files))


def main():
    data = read_api_blueprint('api-specs-master/blueprint/webexapis.com/v1/meetings.apib')
    # data = read_api_blueprint('api-specs-master/blueprint/webexapis.com/v1/webex-calling-organization-settings.apib')
    # data = read_api_blueprint('api-specs-master/blueprint/webexapis.com/v1/devices-with-wxc-devices-displayed.apib')
    # print_metas(data)
    analyze_content(data)
    parsed = ParseResult.model_validate(data)
    validate_parse_result(parsed)

    foo = 1
    ...


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # parse_all()
    main()

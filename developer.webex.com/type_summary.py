#!/usr/bin/env python
"""
Read API specs from YML file and print type summary
"""
import argparse
import os
from collections import defaultdict
from collections.abc import Iterable
from contextlib import contextmanager
from dataclasses import dataclass
from functools import reduce
from sys import stdout

from scraper import DocMethodDetails, MethodDetails, AttributeInfo


@dataclass(init=False)
class EndPointGrouper:
    keys: set[str]

    def key(self, url: str, init: bool = False):
        start = 'https://webexapis.com/v1'
        if url.startswith(start):
            url = url[len(start):]
            if not init and url in self.keys:
                return url

            parts = url.split('/')
            url = '/'.join(parts[:-1])
        return url

    def __init__(self, methods: Iterable[MethodDetails]):
        self.keys = set(self.key(m.documentation.endpoint, init=True) for m in methods)


def main():
    parser = argparse.ArgumentParser()
    default_output = f'{os.path.splitext(os.path.basename(__file__))[0]}.txt'
    default_input = 'read_api_spec.yml'

    # specify file a file to write the summary to
    parser.add_argument('-o', '--output', dest='output_path', action='store', required=False, type=str, nargs='?',
                        const=f'{default_output}', help=f'Write output to file. Default: {default_output}')
    parser.add_argument('input', action='store', type=str,
                        help=f'read API spec from file. Default: {default_input}')

    args = parser.parse_args()

    @contextmanager
    def output_file():
        if args.output_path:
            with open(args.output_path, mode='w') as f:
                yield f
        else:
            yield stdout

    # read API documentation details from file
    doc_details = DocMethodDetails.from_yml(args.input)

    with output_file() as output:
        attributes = list(doc_details.attributes())
        print('\n'.join(f'{a.path} - {a.parameter.type}{f" ({a.parameter.type_spec})" if a.parameter.type_spec else ""}'
                        for a in attributes), file=output)

        types_and_paths: dict[str, list[AttributeInfo]]
        types_and_paths = reduce(lambda s, e: s[e.parameter.type].append(e) or s, attributes, defaultdict(list))
        # regenerate with sorted keys
        types_and_paths = {k: types_and_paths[k] for k in sorted(types_and_paths, key=lambda k: k.lower())}
        print(file=output)
        print('\n'.join(f'{k}: {len(types_and_paths[k])}' for k in types_and_paths), file=output)


if __name__ == '__main__':
    main()
    exit(0)

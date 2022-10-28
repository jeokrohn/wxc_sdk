#!/usr/bin/env python
"""
compare two API spec filed
* endpoints existing in both files
    * same parameters?
        * recursive to also catch changed objects/attributes
* new endpoints
* endpoints removed
"""
import argparse
import os
from collections import defaultdict
from collections.abc import Generator
from contextlib import contextmanager
from functools import reduce
from itertools import chain
from sys import stderr, stdout
from typing import NamedTuple

from scraper import DocMethodDetails, MethodDetails, SectionAndMethodDetails


class Endpoint(NamedTuple):
    url: str
    http_method: str

    def __lt__(self, other: 'Endpoint'):
        return self.url < other.url or self.url == other.url and self.http_method < other.http_method


class PathAndMethod(NamedTuple):
    path: str
    endpoint: Endpoint
    method: SectionAndMethodDetails


class PathAndDocMethodDetails(NamedTuple):
    path: str
    doc_method_details: DocMethodDetails

    def methods(self) -> Generator[PathAndMethod, None, None]:
        for m in self.doc_method_details.methods():
            yield PathAndMethod(path=self.path, endpoint=Endpoint(http_method=m.method_details.documentation.http_method,
                                                                  url=m.method_details.documentation.endpoint),
                                method=m)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('api_spec', nargs=2)
    parser.add_argument('-o', '--output', dest='output_path', action='store', required=False, type=str,
                        help=f'Write output to given file.')

    args = parser.parse_args()
    # names need to be unique
    if len(set(args.api_spec)) != len(args.api_spec):
        print('API specs need to be unique', file=stderr)
        exit(1)

    @contextmanager
    def output_file():
        if args.output_path:
            with open(args.output_path, mode='w') as f:
                print(f'writing to {args.output_path}', file=stderr)
                yield f
        else:
            try:
                yield stdout
            finally:
                ...

    with output_file() as output:
        # read all API specs
        api_specs: dict[str, PathAndDocMethodDetails] = {}
        for spec_path in args.api_spec:
            print(f'Reading API spec from {spec_path}', file=stderr)
            api_specs[spec_path] = PathAndDocMethodDetails(path=spec_path,
                                                           doc_method_details=DocMethodDetails.from_yml(spec_path))

        # group methods in all spec paths
        endpoints: dict[Endpoint, list[PathAndMethod]] = reduce(
            lambda r, el: r[el.endpoint].append(el) or r,
            chain.from_iterable(v.methods() for v in api_specs.values()),
            defaultdict(list))

        # First look at endpoints that only exist in one API spec
        only_one = [ep for ep in endpoints if
                    len(endpoints[ep]) == 1]
        # in which paths did they exist?
        singular_methods: dict[str, list[SectionAndMethodDetails]] = defaultdict(list)
        for singular_method in only_one:
            sm = endpoints.pop(singular_method)[0]
            singular_methods[sm.path].append(sm.method)
        for spec_path in args.api_spec:
            methods = singular_methods.get(spec_path)
            if not methods:
                continue
            print(f'Methods only present in {spec_path}:', file=output)
            for method in sorted(methods):
                print(f'  {method.section}, {method.method_details.documentation.http_method} '
                      f'{method.method_details.documentation.endpoint} --- {method.method_details.documentation.doc}',
                      file=output)
            print(file=output)

        # now let's look at endpoints that exist in multiple specs --- and check for differences
        for endpoint in sorted(endpoints):
            # group by path
            pm: PathAndMethod
            p_and_ms = endpoints[endpoint]
            by_path: dict[str, list[SectionAndMethodDetails]] = reduce(
                lambda s, el: s[el.path].append(el.http_method) or s,
                p_and_ms, defaultdict(list))
            eq = p_and_ms[0].method.method_details == p_and_ms[1].method.method_details
        raise NotImplementedError


if __name__ == '__main__':
    main()
    exit(0)

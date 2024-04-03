#!/usr/bin/env python
"""
Read API specs from YML file and print summary of endpoints

usage: endpoint_summary.py [-h] [-f [OUTPUT_PATH]]

optional arguments:
  -h, --help            show this help message and exit
  -f [OUTPUT_PATH], --file [OUTPUT_PATH]
                        Write output to file. Default: endpoint_summary.txt
"""
import argparse
import os
from collections import defaultdict
from collections.abc import Iterable
from contextlib import contextmanager
from dataclasses import dataclass
from functools import reduce
from sys import stdout, stderr

from scraper import DocMethodDetails, MethodDetails, SectionAndMethodDetails


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

    def __init__(self, methods: Iterable[SectionAndMethodDetails]):
        methods = list(methods)
        self.keys = set(self.key(m.method_details.documentation.endpoint, init=True) for m in methods)


def main():
    parser = argparse.ArgumentParser()
    default_output = f'{os.path.splitext(os.path.basename(__file__))[0]}.txt'
    default_input = 'api_spec.yml'

    # specify file a file to write the endpoint summary to
    parser.add_argument('-o', '--output', dest='output_path', action='store', required=False, type=str, nargs='?',
                        const=f'{default_output}', help=f'Write output to file. Default: {default_output}')
    parser.add_argument('input', action='store', type=str,
                        help=f'read API spec from file. Default: {default_input}')

    args = parser.parse_args()

    @contextmanager
    def output_file():
        if args.output_path:
            with open(args.output_path, mode='w') as f:
                print(f'writing to {args.output_path}', file=stderr)
                yield f
        else:
            yield stdout

    # read API documentation details from file
    doc_details = DocMethodDetails.from_yml(args.input)

    csv_output = args.output_path.lower().endswith('.csv')
    # group endpoints by key (common start of endpoint URL)
    epg = EndPointGrouper(doc_details.methods())
    summary: dict[str, list[MethodDetails]]

    if csv_output:
        # for csv output simply group by section
        summary = reduce(lambda s, el: s[el.section].append(el.method_details) or s,
                         doc_details.methods(), defaultdict(list))
    else:
        summary = reduce(lambda s, el: (s[epg.key(el.method_details.documentation.endpoint)].append(el.method_details)
                                        or s),
                         doc_details.methods(),
                         defaultdict(list))

    with output_file() as output:
        if csv_output:
            print('section,method,url,doc,doc_url', file=output)
        for prefix in sorted(summary):
            if csv_output:
                methods_detail_list = summary[prefix]
                for md in methods_detail_list:
                    print(f'{prefix},{md.documentation.http_method},{md.documentation.endpoint},{md.documentation.doc},'
                          f'{md.documentation.doc_link}',
                          file=output)
            else:
                print(f'{prefix.strip("/")}', file=output)
                print('\n'.join(f'  {m.documentation.http_method:6} {m.documentation.endpoint} --- {m.documentation.doc}'
                                for m in sorted(summary[prefix], key=lambda m: m.documentation.endpoint)),
                      file=output)

    rl_delete = next((m for m in doc_details.methods()
                      if m.section == 'Delete a Route List'), None)
    if rl_delete and 'trunks' in rl_delete.documentation.method:
        # TODO: track resolution of WXCAPIBULK-219
        print('Wrong endpoint URL for "Delete a Route List", WXCAPIBULK-219', file=stderr)


if __name__ == '__main__':
    main()
    exit(0)

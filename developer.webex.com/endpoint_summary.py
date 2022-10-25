#!/usr/bin/env python
"""
Read API specs from developer.webex.com using Selenium and write as YML
"""
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from functools import reduce

from scraper import DocMethodDetails, MethodDetails


@dataclass(init=False)
class EndPointGrouper:
    keys: set[str]

    def key(self, url: str, init: bool = False):
        start = 'https://webexapis.com/v1'
        assert url.startswith(start)
        url = url[len(start):]
        if not init and url in self.keys:
            return url

        parts = url.split('/')
        url = '/'.join(parts[:-1])
        return url

    def __init__(self, methods: Iterable[MethodDetails]):
        self.keys = set(self.key(m.documentation.endpoint, init=True) for m in methods)


def main():
    # read API documentation details from file
    doc_details = DocMethodDetails.from_yml('read_api_spec.yml')

    # group endpoints by key (common start of endpoint URL)
    epg = EndPointGrouper(doc_details.methods())
    summary: dict[str, list[MethodDetails]]
    summary = reduce(lambda s, el: s[epg.key(el.documentation.endpoint)].append(el) or s,
                     doc_details.methods(),
                     defaultdict(list))

    for prefix in sorted(summary):
        print(prefix)
        print('\n'.join(f'  {m.documentation.method:6} {m.documentation.endpoint} --> {m.documentation.doc}'
                        for m in sorted(summary[prefix], key=lambda m: m.documentation.endpoint)))


if __name__ == '__main__':
    main()
    exit(0)

#!/usr/bin/env python
"""
compare two API spec files

usage: compare.py [-h] [-o OUTPUT_PATH] api_spec api_spec

positional arguments:
  api_spec

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_PATH, --output OUTPUT_PATH
                        Write output to given file.
"""
import argparse
import logging
import os.path
from collections import defaultdict
from collections.abc import Generator, Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import reduce
from itertools import chain
from sys import stderr, stdout
from typing import NamedTuple, ClassVar

from scraper import DocMethodDetails, SectionAndMethodDetails, Parameter

log = logging.getLogger(__name__)


class Method(NamedTuple):
    url: str
    http_method: str

    def __str__(self) -> str:
        return f'{self.http_method} {self.url}'

    def __lt__(self, other: 'Method'):
        return self.url < other.url or self.url == other.url and self.http_method < other.http_method


class PathAndMethod(NamedTuple):
    path: str
    method: Method
    details: SectionAndMethodDetails


class PathAndDocMethodDetails(NamedTuple):
    path: str
    doc_method_details: DocMethodDetails

    def methods(self) -> Generator[PathAndMethod, None, None]:
        for m in self.doc_method_details.methods():
            yield PathAndMethod(path=self.path, method=Method(http_method=m.method_details.documentation.http_method,
                                                              url=m.method_details.documentation.endpoint),
                                details=m)


ParametersAndResponse = dict[str, list[Parameter]]


@dataclass
class Diff:
    """
    Base class for all differences
    """
    issue_with: PathAndMethod

    name_len: ClassVar[int] = 0

    def __str__(self):
        return f'{self.__class__.__name__:{self.name_len}}: {self.issue_with.path}/{self.issue_with.details.section}/' \
               f'{self.issue_with.method}'

    def __init_subclass__(cls, **kwargs):
        Diff.name_len = max(cls.name_len, len(cls.__name__) + 1)


@dataclass
class MissingSection(Diff):
    """
    one section is missing from parameters and responses
    """
    section: str

    def __str__(self):
        return f'{super().__str__()}: missing section "{self.section}"'


@dataclass
class MissingParameter(Diff):
    """
    One parameter is missing
    """
    path: str

    def __str__(self):
        return f'{super().__str__()}: missing parameter "{self.path}"'


@dataclass
class TypeMismatch(Diff):
    """
    Type mismatch between two parameters
    """
    path: str
    type1: str
    type2: str

    def __str__(self):
        return f'{super().__str__()}/{self.path}: type mismatch "{self.type1}" != "{self.type2}"'


@dataclass
class ParamListMissing(Diff):
    """
    List of parameters is missing
    """
    path: str
    text: str

    def __str__(self):
        return f'{super().__str__()}/{self.path}: parameter list missing from {self.text}'


@dataclass
class ComparePathAndMethod:
    """
    Helper class to compare :class:`PathAndMethod` instances
    """
    p_and_m1: PathAndMethod
    p_and_m2: PathAndMethod

    @staticmethod
    def consider_all(diff: Diff):
        """
        Default diff callback

        Logs diff to debug and doesn't ignore any differences
        """
        log.debug(f'{diff}')
        return True

    diff_callback: Callable[[Diff], bool] = field(default=consider_all)

    def compare(self) -> bool:
        """
        Actually compare the two :class:`PathAndMethod` instances
        :return:
        """
        # we are actually only interested in the parameters and responses
        return self.compare_parameters_and_response(self.p_and_m1.details.method_details.parameters_and_response,
                                                    self.p_and_m2.details.method_details.parameters_and_response)

    def compare_parameters_and_response(self, p_and_r1: ParametersAndResponse, p_and_r2: ParametersAndResponse) -> bool:
        """
        Compare parameters and response sections of two methods
        """
        # 1st check for missing sections
        result = False
        covered = set()
        for key in p_and_r1:
            if key not in p_and_r2:
                diff = MissingSection(issue_with=self.p_and_m2, section=key)
                result = self.diff_callback(diff) or result
            covered.add(key)
        for key in (k for k in p_and_r2 if k not in covered):
            if key not in p_and_r1:
                diff = MissingSection(issue_with=self.p_and_m1, section=key)
                result = self.diff_callback(diff) or result

        # now we have to take a look at the parameters in each section
        for key in set(chain(p_and_r1, p_and_r2)):
            params_1 = p_and_r1.get(key, [])
            params_2 = p_and_r2.get(key, [])
            if not params_1:
                result = self.diff_callback(MissingSection(issue_with=self.p_and_m1,
                                                           section=key)) or result
            if not params_2:
                result = self.diff_callback(MissingSection(issue_with=self.p_and_m2,
                                                           section=key)) or result
            result = self.compare_param_list(key, params_1, params_2) or result
        return result

    def compare_param_list(self, path: str, p_list1: list[Parameter], p_list2: list[Parameter]) -> bool:
        """
        Compare two lists of parameters
        :param path:
        :param p_list1:
        :param p_list2:
        :return:
        """

        # check for missing parameters in either side
        # noinspection PyShadowingNames
        def not_in(l1: list[Parameter], l2: list[Parameter], blame: PathAndMethod) -> bool:
            result = False
            l2_names = set(p.name for p in l2)
            for p_name in (p.name for p in l1):
                if p_name not in l2_names:
                    result = self.diff_callback(MissingParameter(blame, f'{path}/{p_name}')) or result
            return result

        result = not_in(p_list1, p_list2, blame=self.p_and_m2)
        result = not_in(p_list2, p_list1, blame=self.p_and_m1) or result

        # check parameter definition
        for p1 in p_list1:
            p2 = next((p for p in p_list2 if p.name == p1.name), None)
            if p2 is None:
                continue
            result = self.compare_parameter(path, p1, p2) or result
        return result

    def compare_parameter(self, path: str, p1: Parameter, p2: Parameter) -> bool:
        """
        Compare two parameters
        :param path:
        :param p1:
        :param p2:
        :return:
        """
        result = False
        # compare parameter definition
        path = f'{path}/{p1.name}'
        t1 = f'{p1.type}/{p1.type_spec}'
        t2 = f'{p2.type}/{p2.type_spec}'
        if t1 != t2:
            result = self.diff_callback(TypeMismatch(issue_with=self.p_and_m2,
                                                     path=path,
                                                     type1=t1,
                                                     type2=t2)) or result

        # noinspection PyShadowingNames
        def comp_lists(path, l1, l2) -> bool:
            result = False
            if l1 and not l2:
                result = self.diff_callback(ParamListMissing(self.p_and_m2, path=path, text='second object')) or result
            elif l2 and not l1:
                result = self.diff_callback(ParamListMissing(self.p_and_m1, path=path, text='first object')) or result
            elif l1 and l2:
                result = self.compare_param_list(path, p_list1=l1, p_list2=l2) or result
            return result

        # step down into object hierarchy
        result = comp_lists(f'{path}-attrs', p1.param_attrs, p2.param_attrs) or result
        result = comp_lists(f'{path}-obj', p1.param_object, p2.param_object) or result
        return result


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('api_spec', nargs=2)
    parser.add_argument('-o', '--output', dest='output_path', action='store', required=False, type=str,
                        help='Write output to given file.')

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
        truncate = os.path.basename(args.api_spec[0]) != os.path.basename(args.api_spec[1])
        if truncate:
            p_len = max(map(len, map(os.path.basename, args.api_spec)))
        else:
            p_len = max(map(len, args.api_spec))
        for spec_path in args.api_spec:
            print(f'Reading API spec from {spec_path}', file=stderr)
            if truncate:
                truncated_path = os.path.basename(spec_path)
            else:
                truncated_path = spec_path
            truncated_path = f'{truncated_path:{p_len}}'
            api_specs[truncated_path] = PathAndDocMethodDetails(
                path=truncated_path,
                doc_method_details=DocMethodDetails.from_yml(spec_path))

        # group methods in all spec paths
        methods: dict[Method, list[PathAndMethod]] = reduce(
            lambda r, el: r[el.method].append(el) or r,
            chain.from_iterable(v.methods() for v in api_specs.values()),
            defaultdict(list))

        # First look at methods that only exist once
        only_one = [m for m in methods if
                    len(methods[m]) == 1]
        # in which paths did they exist?
        singular_methods: dict[str, list[SectionAndMethodDetails]] = defaultdict(list)
        for singular_method in only_one:
            sm = methods.pop(singular_method)[0]
            singular_methods[sm.path].append(sm.details)
        for spec_path in args.api_spec:
            methods_in_spec = singular_methods.get(spec_path)
            if not methods_in_spec:
                continue
            print(f'Methods only present in {spec_path}:', file=output)
            for method in sorted(methods_in_spec):
                print(f'  {method.section}, {method.method_details.documentation.http_method} '
                      f'{method.method_details.documentation.endpoint} --- {method.method_details.documentation.doc}',
                      file=output)
            print(file=output)

        def diff_logger(diff: Diff) -> bool:
            print(f'{diff}', file=output)
            return True

        # now let's look at endpoints that exist multiple times --- and check for differences
        for method in sorted(methods):
            path_and_method_gen = (p_and_m for p_and_m in methods[method])
            p_and_m1 = next(path_and_method_gen)
            for p_and_m2 in path_and_method_gen:
                cmp = ComparePathAndMethod(p_and_m1, p_and_m2, diff_logger)
                cmp.compare()
    return


if __name__ == '__main__':
    main()
    exit(0)

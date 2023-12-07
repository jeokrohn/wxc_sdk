"""
Understand opportunities to optimize auto class creation and usage
"""
import json
import logging
import os
import re
from collections import defaultdict
from collections.abc import Generator, Iterable
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from itertools import chain
from os.path import commonprefix
from typing import NamedTuple

from apib.generator import CodeGenerator
from apib.python_class import PythonClass, PythonClassRegistry, Endpoint
from apib.tests.test_generator import GeneratorTest
from apib.tools import snake_case

log = logging.getLogger(__name__)


def rev_str(s: str) -> str:
    return ''.join(reversed(s))


def combined_class_name(n1: str, n2: str) -> str:
    """
    Combined class name based on names of two classes
    :param n1:
    :param n2:
    :return:
    """
    word_in_class_name = re.compile(r'[A-Z]+[a-z0-9]+')
    n1_words = list(reversed(word_in_class_name.findall(n1)))
    n2_words = list(reversed(word_in_class_name.findall(n2)))
    common_words = commonprefix((n1_words, n2_words))
    if common_words:
        common_suffix = ''.join(reversed(common_words))
        r = f'{n1[:-len(common_suffix)]}{n2}'
    else:
        if len(n1) < len(n2):
            r = f'{n1}{n2}'
        else:
            r = f'{n2}{n1}'
    log.debug(f'combined_class_name: {n1}, {n2} -> {r}')
    return r


def class_union(cr: PythonClassRegistry, c1: PythonClass, c2: PythonClass, depth: int = 0) -> PythonClass:
    """
    Union of two Python classes

    Superset of attributes of both classes
    """
    r = PythonClass(name=combined_class_name(c1.name, c2.name), attributes=list(), description=c1.description,
                    is_enum=c1.is_enum)
    if depth:
        prefix = ' ' * (depth * 2)
    else:
        prefix = ''
    log.debug(f'{prefix}class_union: {c1.name}, {c2.name} as {r.name}')
    processed_attributes: set[str] = set()
    for a1 in c1.attributes:
        processed_attributes.add(a1.name)
        log.debug(f'{prefix}working on {c1.name}.{a1.name}: {a1.python_type}')
        a2 = next((a for a in c2.attributes if a.name == a1.name), None)
        if a2 is None:
            log.debug(f'{prefix} attribute not found in {c2.name}, adding attribute to result')
            r.attributes.append(deepcopy(a1))
            continue
        log.debug(f'{prefix} found {c2.name}.{a2.name}: {a2.python_type}')
        if a1.python_type == a2.python_type:
            log.debug(f'{prefix} attribute types in both classes identical, adding attribute to result')
            r.attributes.append(deepcopy(a1))
            continue
        if a1.referenced_class and a2.referenced_class:
            # are they "compatible"?
            if a1.python_type.replace(a1.referenced_class, a2.referenced_class) != a2.python_type:
                raise ValueError(f'{a1.python_type} and {a2.python_type} not compatible')
            new_attr = deepcopy(a1)
            new_attr_class = class_union(cr, cr.get(a1.referenced_class), cr.get(a2.referenced_class),
                                         depth=depth + 1)
            new_attr.python_type = a1.python_type.replace(a1.referenced_class, new_attr_class.name)
            new_attr.referenced_class = new_attr_class.name
            r.attributes.append(new_attr)
        else:
            raise NotImplementedError()
    # add attributes from c2 which are not covered yet
    for a2 in c2.attributes:
        if a2.name in processed_attributes:
            continue
        log.debug(f'{prefix}adding remaining attribute: {c2.name}.{a2.name}: {a2.python_type}')
        r.attributes.append(deepcopy(a2))
    cr._add_class(r)
    return r


def class_exclude(cr: PythonClassRegistry, c1: PythonClass, c2: PythonClass, depth: int = 0) -> dict:
    """
    get exclude dict for two classes where c1 is the super-set
    """
    if depth:
        prefix = ' ' * (depth * 2)
    else:
        prefix = ''
    r = dict()
    attr_names1 = set(a.name for a in c1.attributes)
    attr_names2 = set(a.name for a in c2.attributes)
    if attr_names2 - attr_names1:
        raise ValueError(f'attributes in {c2.name} not in {c1.name}: {", ".join(sorted(attr_names2 - attr_names1))}')

    for a1 in c1.attributes:
        a2 = next((a for a in c2.attributes if a.name == a1.name), None)
        if a2 is None:
            # attribute not present in c2
            r[snake_case(a1.name)] = True
            continue
        if a1.python_type == a2.python_type:
            continue
        if not a1.referenced_class or not a2.referenced_class:
            raise ValueError(f'Incompatible types {c1.name}.{a1.name}: {a1.python_type} and '
                             f'{c2.name}.{a2.name}: {a2.python_type}')
        attr_diff = class_exclude(cr, cr.get(a1.referenced_class), cr.get(a2.referenced_class), depth=depth + 1)
        if not attr_diff:
            continue
        if a1.python_type.startswith('list['):
            attr_diff = {'__all__': attr_diff}
        r[snake_case(a1.name)] = attr_diff
    return r


class EndpointInfo(NamedTuple):
    apib_path: str
    endpoint: Endpoint


class EndpointType(str, Enum):
    create = 'create'
    read = 'read'
    update = 'update'
    delete_ = 'delete'
    unknown = 'unknown'
    list_ = 'list'
    modify = 'modify'


@dataclass(init=False)
class EndpointGroup:
    """
    Group of endpoints with a common URL prefix
    """
    # common URL prefix for all endpoints
    url_prefix: str
    # endpoints grouped by apib path
    apib_buckets: dict[str, list[Endpoint]]

    def __init__(self, url_prefix: str, endpoint_infos: Iterable[EndpointInfo]):
        self.url_prefix = url_prefix
        self.apib_buckets = defaultdict(list)
        for ep_info in endpoint_infos:
            self.apib_buckets[ep_info.apib_path].append(ep_info.endpoint)

    @property
    def group_identity(self) -> str:
        # determine identity of objects endpoints in this endpoint group work on
        # url_prefix 'telephony/config/queues' --> 'Queues'
        r = self.url_prefix.split('/')[-1]
        r = f'{r[0].upper()}{r[1:]}'
        return r

    @property
    def apib_paths(self) -> list[str]:
        return list(self.apib_buckets)

    def endpoints(self) -> Generator[Endpoint, None, None]:
        return chain.from_iterable(self.apib_buckets.values())

    def endpoint_type(self, ep: Endpoint) -> EndpointType:
        """
        Get endpoint type for endpoint of this group
        """
        if ep.method.upper() == 'GET':
            if ep.url == self.url_prefix:
                # can be list or read
                # read is typically complemented by an UPDATE with the same URL
                if next((upd for upd in self.endpoints() if ep.url == upd.url and upd.method == 'PUT'), None) is None:
                    # no update
                    return EndpointType.list_
            return EndpointType.read
        elif ep.method.upper() == 'POST':
            return EndpointType.create
        elif ep.method.upper() == 'PUT':
            return EndpointType.update
        elif ep.method.upper() == 'DELETE':
            return EndpointType.delete_
        elif ep.method.upper() == 'PATCH':
            return EndpointType.modify
        else:
            raise ValueError(f'unknown method: {ep.method}')


@dataclass(init=False)
class EndpointCollection():
    # all end points grouped by URL prefix
    # URL prefix is url w/o the last URL parameter
    groups_by_url: dict[str, EndpointGroup]

    def __init__(self, endpoints: Iterable[EndpointInfo]):
        groups_by_url: dict[str, list[EndpointInfo]] = defaultdict(list)
        for ep_info in endpoints:
            ep = ep_info.endpoint
            url = ep.url
            group_url = re.sub(r'/\{[^}]+}$', '', url)
            groups_by_url[group_url].append(ep_info)
        self.groups_by_url = {prefix: EndpointGroup(prefix, epi_list) for prefix, epi_list in groups_by_url.items()}


class TestClassOptimization(GeneratorTest):

    def test_queue_create_and_update(self):
        code_gen = CodeGenerator()

        for apib_path in self.apib_paths:
            apib_path_base = os.path.basename(apib_path)
            if apib_path_base != 'features-call-queue.apib':
                continue
            code_gen.read_blueprint(apib_path)
        code_gen.cleanup()
        endpoints = list(code_gen.all_endpoints())
        create = next(ep for _, ep in endpoints if ep.name == 'create_a_call_queue')
        get_details = next(ep for _, ep in endpoints if ep.name == 'get_details_for_a_call_queue')
        update_details = next(ep for _, ep in endpoints if ep.name == 'update_a_call_queue')
        cq_details_class = code_gen.class_registry.get(get_details.result_referenced_class)
        cq_update_class = code_gen.class_registry.get(update_details.body_class_name)
        cq_create_class = code_gen.class_registry.get(create.body_class_name)
        foo = 1
        union_details_create = class_union(code_gen.class_registry, cq_details_class, cq_create_class)
        exclude_create = class_exclude(code_gen.class_registry, union_details_create, cq_create_class)
        exclude_details = class_exclude(code_gen.class_registry, union_details_create, cq_details_class)
        foo = 1

    def test_group_endpoints_by_uri(self):
        """
        Read (all) APIB files and group URLs
        """
        logging.getLogger().setLevel(logging.INFO)
        code_gen = CodeGenerator()
        skip_apib = {'device-configurations.apib'}
        for apib_path in self.apib_paths:
            apib_path_base = os.path.basename(apib_path)
            if apib_path_base in skip_apib:
                continue
            if False and apib_path_base != 'features-call-queue.apib':
                continue
            code_gen.read_blueprint(apib_path)
        code_gen.cleanup()
        [ep.returns_list for _, ep in code_gen.all_endpoints()]
        endpoint_collection = EndpointCollection(EndpointInfo(*e)
                                                 for e in code_gen.all_endpoints())
        print('found these URL prefixes:')
        url_prefix_len = max(map(len, endpoint_collection.groups_by_url))
        for url_prefix, endpoint_group in endpoint_collection.groups_by_url.items():
            print(f'{url_prefix:{url_prefix_len}} methods: '
                  f'{", ".join(sorted(set(ep.name for ep in endpoint_group.endpoints())))}')
            ep_types = set(map(endpoint_group.endpoint_type, endpoint_group.endpoints()))
            print(f'{" " * (url_prefix_len + 10)}{", ".join(sorted(ept.value for ept in ep_types))}')
            print(f'{" " * url_prefix_len} Group identity: {endpoint_group.group_identity}')
        foo = 1

    def test_group_endpoints_by_uri_all_apib(self):
        """
        Read all APIB files and group all endpoints by URL
        """
        logging.getLogger().setLevel(logging.INFO)
        code_gen = CodeGenerator()
        for apib_path in self.apib_paths:
            apib_path_base = os.path.basename(apib_path)
            ignore = {'device-configurations.apib'}
            if apib_path_base in ignore:
                continue
            try:
                code_gen.read_blueprint(apib_path)
            except:
                pass

        code_gen.cleanup()
        logging.getLogger().setLevel(logging.INFO)
        endpoints = [ep for _, ep in code_gen.all_endpoints()]
        groups_by_url: dict[str, list[Endpoint]] = defaultdict(list)
        ep_names = set()

        def keep_ep(ep: Endpoint) -> bool:
            # don't keep list methods
            if ep.method == 'GET' and not ep.url.endswith('}'):
                print(f'drop {ep.name}')
                return False
            return True

        for ep in endpoints:
            if ep.name in ep_names:
                continue
            if not keep_ep(ep):
                continue
            ep_names.add(ep.name)
            url = ep.url
            group_url = re.sub(r'/\{[^}]+}$', '', url)
            groups_by_url[group_url].append(ep)

        single_ep = [k for k, ep_list in groups_by_url.items() if len(ep_list) < 2]
        list(map(groups_by_url.pop, single_ep))
        single_http_method = [k for k, ep_list in groups_by_url.items()
                              if len(set(ep.method for ep in ep_list)) == 1]
        list(map(groups_by_url.pop, single_http_method))
        groups_by_url = {url: groups_by_url[url] for url in sorted(groups_by_url)}

        def ep_class_names(ep: Endpoint) -> Generator[str, None, None]:
            if ep.body_class_name:
                yield ep.body_class_name
            if ep.result_referenced_class:
                yield ep.result_referenced_class

        def print_ep(ep: Endpoint):
            print(f'  {ep.title}, {ep.name}')
            print(f'    {ep.method} {ep.url}')
            if ep.body_class_name:
                print(f'      body class: {ep.body_class_name}')
            if ep.result:
                print(f'          result: {ep.result}')
            if ep.result_referenced_class:
                print(f'    result class: {ep.result_referenced_class}')

        for url, endpoints in groups_by_url.items():
            # try to extract item name from url
            # 'admin/meeting/config/trackingCodes' -> TrackingCodes
            item_name = url.split('/')[-1].capitalize()
            print('=' * 90)
            print(f'Item name: {item_name}')
            print(f'url: {url}')
            print('endpoints:')
            for ep in endpoints:
                print_ep(ep)
            class_names = set(chain.from_iterable(ep_class_names(ep) for ep in endpoints))
            if class_names:
                print(f'{len(class_names)} classes: {", ".join(sorted(class_names))}')
            if len(class_names) < 2:
                continue
            classes = list(map(code_gen.class_registry.get, class_names))
            try:
                classes_union = class_union(code_gen.class_registry, classes[0], classes[1])
                for c in classes[2:]:
                    classes_union = class_union(code_gen.class_registry, classes_union, c)
            except (ValueError, NotImplementedError) as e:
                print(f'---- failed to get union: {e}')
            else:
                for c in classes:
                    print(f'{c.name}')
                    print('\n'.join(f'  {l}'
                                    for l in json.dumps(class_exclude(code_gen.class_registry,
                                                                      classes_union, c),
                                                        indent=2).splitlines()))
        foo = 1

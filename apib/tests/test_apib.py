"""
Test reading apib files
"""
import glob
import logging
import os.path
import re
import sys
from collections import Counter, defaultdict
from collections.abc import Generator, Callable
from dataclasses import dataclass
from typing import ClassVar, Any, NamedTuple
from unittest import TestCase, skip

from pydantic import ValidationError, parse_obj_as, BaseModel, model_validator, TypeAdapter

from apib.apib import *


@dataclass(init=False)
class ApibTest(TestCase):
    apib_paths: ClassVar[list[str]]
    apib_data: ClassVar[dict[str, dict]]
    stream_handler: logging.StreamHandler
    log_level: int

    @classmethod
    def setUpClass(cls) -> None:
        api_apecs = os.path.dirname(__file__)
        api_specs = os.path.join(api_apecs, *(['..'] * 3), 'api-specs')
        api_specs = os.path.abspath(api_specs)
        cls.apib_paths = sorted(glob.glob(os.path.join(api_specs,
                                                       'blueprint',
                                                       'webexapis.com',
                                                       'v1',
                                                       '*.apib')))
        cls.apib_data = dict()

    def setUp(self) -> None:
        super().setUp()
        logger = logging.getLogger()
        self.log_level = logger.level
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(funcName)s %(message)s')
        stream_handler.setFormatter(fmt)
        logger.addHandler(stream_handler)
        self.stream_handler = stream_handler
        print()

    def tearDown(self) -> None:
        logging.getLogger().removeHandler(self.stream_handler)
        logging.getLogger().setLevel(self.log_level)

    def get_apib_data(self, apib_path: str) -> dict:
        if (data := self.apib_data.get(apib_path)) is None:
            data = read_api_blueprint(apib_path)
            self.apib_data[apib_path] = data
        return data

    def apib_path_and_data(self) -> Generator[tuple[str, dict]]:
        for path in self.apib_paths:
            data = self.get_apib_data(path)
            yield path, data

    def for_all_apib(self, tests: Callable[[str, dict], None]):
        """
        run tests for all apib files
        """
        err = None
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            try:
                tests(path, data)
            except AssertionError as e:
                print(f'{path}: {e}')
                err = err or e
        if err:
            raise err


class AttrInfo(NamedTuple):
    path: str
    attr_name: str
    attr_value: Any
    data_path: list[dict]

    def elem_path(self) -> str:
        return '.'.join(e['element'] for e in self.data_path if is_element(e))


def all_attrs(data: Any, path: str = None, data_path: list[dict] = None) -> Generator[AttrInfo, None, None]:
    path = path or '/'
    data_path = data_path or list()
    if not isinstance(data, dict):
        return
    data: dict
    yield AttrInfo(path=path, attr_name='', attr_value=data, data_path=data_path)
    for k, v in data.items():
        yield AttrInfo(path=path, attr_name=k, attr_value=v, data_path=data_path)
        # descend down into list element and child dicts
        if isinstance(v, list):
            # look at all list elements
            for i, child in enumerate(v):
                yield from all_attrs(data=child, path=f'{path}.{k}[{i}]', data_path=data_path + [data] + [v])
        elif isinstance(v, dict):
            # look at all dict values
            for a, child in v.items():
                yield from all_attrs(data=child, path=f'{path}.{k}.{a}', data_path=data_path + [data] + [v])


def is_key_value(v) -> bool:
    if not isinstance(v, dict):
        return False
    v: dict
    if set(v.keys()) != {'key', 'value'}:
        return False
    # key always has 'element' and 'content' while 'value' is more flexible
    return {'element', 'content'} == set(v['key']) and is_element(v['value'])


class ReadAPIB(ApibTest):

    def test_001_read_all(self):
        """
        Try reading API blueprint files
        """
        for api_path in self.apib_paths:
            try:
                api_dict = self.get_apib_data(api_path)
            except Exception as e:
                print(f'{api_path}: {e}')
                raise
            else:
                print(f'{os.path.basename(api_path)}: ok')

    def test_002_parse_result(self):
        """
        Verify root node "parseResult"
        """
        for api_path in self.apib_paths:
            api_dict = self.get_apib_data(api_path)
            api_path = os.path.basename(api_path)
            try:
                # parseResult should only have 'element' and 'content'
                self.assertEqual({'element', 'content'}, set(api_dict.keys()))

                # 'element' should indicate -> parseResult
                self.assertEqual('parseResult', api_dict['element'])

                # ... and 'content' should be a list
                content = api_dict['content']
                self.assertTrue(isinstance(content, list))
            except AssertionError:
                print(f'{api_path}')
                raise

    def test_003_parse_result_content(self):
        """
        Verify content of parseResult
        """
        error = None
        for api_path in self.apib_paths:
            api_dict = self.get_apib_data(api_path)
            api_path = os.path.basename(api_path)
            try:
                content = api_dict['content']
                element_type_counter = Counter(c['element'] for c in content)
                # we expect exactly one 'category'
                self.assertTrue('category' in element_type_counter)
                self.assertEqual(1, element_type_counter['category'])
                # and potentially some 'annotation' elements
                self.assertFalse(set(element_type_counter.keys()) - {'category', 'annotation'})
            except AssertionError as e:
                error = (api_dict, e)
                print(f'{api_path}: {e}')
        if error:
            raise error[1]

    def test_004_meta_attributes(self):
        """
        look for all "meta" attributes and assert that they only have these attributes:
        * classes
        * title
        * description
        """

        error = None
        all_meta_key_sets = set()
        class_item_elements = set()
        for api_path in self.apib_paths:
            api_dict = self.get_apib_data(api_path)
            api_path = os.path.basename(api_path)
            for attr_info in all_attrs(data=api_dict):
                if attr_info.attr_name == 'meta':
                    meta = attr_info.attr_value
                    try:
                        # 'meta' has to be a dict
                        self.assertTrue(isinstance(meta, dict))
                        key_set = set(meta.keys())
                        all_meta_key_sets.add(', '.join(sorted(key_set)))
                        # 'meta' only has: classes, title, description
                        self.assertFalse(key_set - {'classes', 'title', 'description'})
                        classes = meta.get('classes')
                        if classes:
                            # 'classes' has to be a dict
                            self.assertTrue(isinstance(classes, dict))
                            classes: dict
                            # 'classes' always only has: content, element
                            self.assertEqual({'content', 'element'}, set(classes.keys()))
                            # 'classes'.'element' always is 'array'
                            self.assertEqual('array', classes['element'])
                            for class_item in classes['content']:
                                # all content entries are dicts ..
                                self.assertTrue(isinstance(class_item, dict))
                                class_item: dict
                                # .. and only have: content, element
                                self.assertEqual({'content', 'element'}, set(class_item.keys()))
                                # .. and element is 'string'
                                self.assertEqual('string', class_item['element'])
                                class_item_elements.add(class_item['element'])
                    except AssertionError:
                        print(f'{api_path}:{attr_info.path}')
                        raise
                # if
            # for
        # for
        print('Existing attribute sets:')
        print('\n'.join(sorted(all_meta_key_sets)))
        print(f'Class item elements: {", ".join(sorted(class_item_elements))}')

    def test_005_feature_toggle(self):
        """
        look for 'feature-toggle' in APIB files
        There is either one or none
        """

        for api_path in self.apib_paths:
            api_dict = self.get_apib_data(api_path)
            api_path = os.path.basename(api_path)
            for attr_info in all_attrs(data=api_dict):
                if isinstance(attr_info.attr_value, str) and 'feature-toggle' in attr_info.attr_value:
                    self.assertEqual('/.content[0].content[0]', attr_info.path)
                    self.assertEqual('content', attr_info.attr_name)
                    # look for stuff like:
                    #   <!-- feature-toggle-name:contact-center-api-docs-v1 -->
                    r = re.findall(r'<!-- feature-toggle-name:(.+?) ?-->', attr_info.attr_value)
                    self.assertEqual(1, len(r))
                    print(f'{api_path}: {r[0]}')

    def test_006_content_is_simple_value_or_list_of_element(self):
        """
        Verify options for 'content' attribute

        'content' can be:
            * int
            * str
            * list ('element')
            * key/value
            * 'element'
            * None
        """
        error = None
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                if attr_info.attr_name != 'content':
                    continue
                try:
                    content = attr_info.attr_value
                    if isinstance(content, list):
                        self.assertTrue(all(is_element(c) for c in content))
                    else:
                        # content is:
                        #   * key/value
                        #   * element
                        #   * str
                        #   * int
                        self.assertTrue(is_key_value(content) or is_element(content) or
                                        isinstance(content, str) or isinstance(content, int),
                                        f'{content} is not key/value, content, str nor int: {type(content)}')
                except AssertionError as e:
                    print(f'{path}: {e}')
                    error = e
        if error:
            raise error

    def test_category_element(self):
        """
        Validation of 'category' element as child of 'parseResult'
            * has meta, attributes, and content
            * meta has classes and title
            * meta classes is an array with a single string element with value 'api'
            * has one 'copy' element in the content
        ... and else
            * ...
        """
        error = None
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                value = attr_info.attr_value
                if not (is_element(value) and value['element'] == 'category'):
                    continue

                try:
                    if is_element(parent := attr_info.data_path[-2]) and parent['element'] == 'parseResult':
                        # validation as child of parseResult

                        # has meta, attributes, and content
                        self.assertEqual({'meta', 'attributes', 'content', 'element'}, set(value), 'A')

                        # meta has classes and title
                        meta = value['meta']
                        self.assertEqual({'classes', 'title'}, set(meta), 'B')

                        # meta classes is an array with a single string element with value 'api'
                        meta_classes = meta['classes']
                        self.assertTrue(is_element(meta_classes), 'C')
                        self.assertEqual(meta_classes['element'], 'array', 'D')
                        meta_classes_1st_element = meta_classes['content'][0]
                        self.assertTrue(is_element(meta_classes_1st_element), 'E')
                        self.assertEqual('string', meta_classes_1st_element['element'], 'F')
                        self.assertEqual('api', meta_classes_1st_element['content'], 'G')
                    else:
                        # validation for other category elements
                        ...
                except AssertionError as e:
                    print(f'{path}: {e}')
                    error = e
        if error:
            raise error

    @skip
    def test_datastructure_element(self):
        """
        Validation of 'dataStructure'
            * always only has 'content' attribute
            * content is either a reference to a data structure
            ... or
            * is an object
        """
        error = None
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                value = attr_info.attr_value
                if not (is_element(value) and value['element'] == 'dataStructure'):
                    continue
                try:
                    self.assertEqual({'element', 'content'}, set(value), 'A')
                    content = value['content']
                    # content can be a simple reference to a datatype like:
                    #   {'element': 'Audit Event Collection Response'}
                    # and then there is nothing to validate
                    if content['element'] not in {'enum', 'object', 'array'}:
                        # in this case only 'element' and 'attributes' are allowed
                        self.assertFalse(set(content) - {'element', 'attributes'}, 'B')
                        continue

                    # else content can be an enum or an object
                    self.assertTrue(is_element(content) and content['element'] in {'enum', 'object', 'array'}, 'C')
                    foo = 1
                    # # dataStructure can be as trivial as:
                    # # {'content': {'element': 'Audit Event Collection Response'}, 'element': 'dataStructure'}
                    # if set(value) == {'element', 'content'}:
                    #     self.assertTrue(isinstance(value['content'], dict), 'A')
                    #     self.assertEqual({'element'}, set(value['content']), 'B')
                    # else:
                    #     foo = 1
                except AssertionError as e:
                    print(f'{path}: {e}')
                    error = e
        if error:
            raise error

    def test_attributes(self):
        """
        Which elements have 'attributes' and what attributes live in those 'attributes'?
        """
        attr_attributes_in_element: dict[str, set] = defaultdict(set)
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)

            for attr_info in all_attrs(data):
                if not isinstance(attr_info.attr_value, dict) or not (attributes := attr_info.attr_value.get(
                        'attributes')):
                    continue
                attr_attributes_in_element[attr_info.attr_value['element']].update(attributes)
        print('\n'.join(f'{el}: {", ".join(sorted(attr_attributes_in_element[el]))}'
                        for el in sorted(attr_attributes_in_element)))
        return

    def test_where_do_we_see_copy_elements(self):
        """
        Where do we have 'copy' elements?
        """

        def elem_path(data_path) -> str:
            return '.'.join(e['element'] for e in data_path if is_element(e))

        parents: set[str] = set()
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)

            for attr_info in all_attrs(data):
                value = attr_info.attr_value
                if not is_element(value) or value['element'] != 'copy':
                    continue
                key = attr_info.elem_path()
                parents.add(key)
        print('Copy elements exist in these paths:')
        print('\n'.join(sorted(parents)))

    def test_where_do_we_see_category_elements(self):
        """
        Where do we have 'category' elements?
        """
        parents: set[str] = set()
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)

            for attr_info in all_attrs(data):
                value = attr_info.attr_value
                if not is_element(value) or value['element'] != 'category':
                    continue
                key = attr_info.elem_path()
                parents.add(key)
        print('Copy elements exist in these paths:')
        print('\n'.join(sorted(parents)))

    def test_members(self):
        """
        * where do 'member' objects show up?
        * what do they have as content?
        """
        parents = set()
        member_attrs = set()
        parent_member_attrs: dict[str, set] = defaultdict(set)
        content_attrs = set()
        member_content_value_attrs = set()
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                try:
                    if attr_info.attr_value['element'] != 'member':
                        continue
                except (TypeError, KeyError):
                    continue
                m = re.match(r'^.+?\.(\w+)\.\w+\[\d+]$', attr_info.path)
                self.assertIsNotNone(m)
                parent = m.group(1)
                parents.add(parent)
                member_attrs.update(attr_info.attr_value)
                parent_member_attrs[parent].update(attr_info.attr_value)
                content_attrs.update(attr_info.attr_value['content'])
                member_content_value_attrs.update(attr_info.attr_value['content']['value'])
        print(f'parents: {", ".join(sorted(parents))}')
        print(f'member element attributes: {", ".join(sorted(member_attrs))}')
        print('\n'.join(f'member element attributes for {p}: {", ".join(sorted(parent_member_attrs[p]))}' for p in
                        sorted(parent_member_attrs)))
        print(f'member content attributes: {", ".join(sorted(content_attrs))}')
        print(f'member content value attributes: {", ".join(sorted(member_content_value_attrs))}')

    def test_type_attributes(self):
        """
        Are 'type_attributes' really always an 'array' with string elements only?
        """
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                if attr_info.attr_name != 'typeAttributes':
                    continue
                values = attr_info.attr_value
                self.assertEqual('array', values['element'])
                self.assertIsNone(values.get('meta'))
                self.assertIsNone(values.get('attributes'))
                content = values['content']
                self.assertTrue(isinstance(content, list))
                for item in content:
                    self.assertEqual('string', item['element'])
                    self.assertIsNone(item.get('meta'))
                    self.assertIsNone(item.get('attributes'))
                    self.assertTrue(isinstance(item['content'], str))
        return

    def test_string_w_non_string_content(self):
        """
        Find 'string' elements with non-string content
        """
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                try:
                    if attr_info.attr_value['element'] != 'string':
                        continue
                except (TypeError, KeyError) as e:
                    continue
                try:
                    content = attr_info.attr_value['content']
                except KeyError:
                    continue
                if not isinstance(content, str):
                    foo = 1

    def test_string_element_wo_content(self):
        """
        Locate string elements wo content
        """
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                a_data = attr_info.attr_value
                try:
                    if a_data['element'] != 'string':
                        continue
                except (TypeError, KeyError):
                    continue
                if 'content' not in a_data:
                    print(f'{path}: {attr_info.path}')

    def test_transition_wo_href(self):
        error = False
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                try:
                    if attr_info.attr_value['element'] != 'transition':
                        continue
                except (TypeError, KeyError):
                    continue
                attributes = attr_info.attr_value.get('attributes')
                if attributes is None:
                    print(f'No attributes: {path}, {attr_info.path}')
                    error = True
                    continue
                if attributes.get('href') is None:
                    print(f'No href: {path}, {attr_info.path}')
                    error = True
                    continue
        self.assertFalse(error)

    def test_content_w_data(self):
        error = False
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                try:
                    element = attr_info.attr_value.get('element')
                    if attr_info.attr_value.get('data'):
                        print(f'{path}, {attr_info.path}({element}) has "data"')
                        error = True
                except AttributeError:
                    pass
        self.assertFalse(error)

    def test_http_headers(self):
        """
        Verify that 'httpHeader' content is a list of key/value pairs with string values
        """
        err = None
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                try:
                    element = attr_info.attr_value.get('element')
                    if element != 'httpHeaders':
                        continue
                except AttributeError:
                    continue
                for http_header in attr_info.attr_value['content']:
                    try:
                        self.assertEqual('member', http_header['element'])
                        content = http_header['content']
                        self.assertEqual({'key', 'value'}, set(content))
                        for k, v in content.items():
                            str_val = ApibString.model_validate(v)
                            self.assertIsNone(str_val.meta)
                            self.assertIsNone(str_val.attributes)
                            self.assertTrue(isinstance(str_val.content, str))
                    except AssertionError as e:
                        print(f'{path}: {e}')
                        err = err or e
        if err:
            raise err

    def test_enums(self):
        """
        Understand 'enum' elements
        """
        content_str = set()
        enumeration_element_types = set()
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                try:
                    element = attr_info.attr_value.get('element')
                    if element != 'enum':
                        continue
                except AttributeError:
                    continue
                values = attr_info.attr_value
                # content is optional ..
                content = values.get('content')
                if content is not None:
                    # .. and if it's there then it's a 'string
                    # content should be a string (the enum name?)
                    content = ApibString.model_validate(values['content'])
                    content_str.add(content.content)
                # attributes are optional ..
                type_attributes = values.get('attributes')
                if type_attributes is not None:
                    # 'enumerations' and 'default' are the only attributes
                    self.assertFalse(set(type_attributes) - {'enumerations', 'default'})
                    # 'enumerations" are mandatory
                    enumerations = type_attributes.get('enumerations')
                    self.assertIsNotNone(enumerations)
                    default = type_attributes.get('default')

                    # enumerations are an array
                    enumerations_array = ApibArray.model_validate(enumerations)
                    enumeration_element_types.update(c.element for c in enumerations_array.content)

                    # .. string seems to be the only enumeration element type
                    wrong_element_type = next((e for e in enumerations_array.content if e.element != 'string'), None)
                    self.assertIsNone(wrong_element_type)

                    enums_w_attrs_or_meta = [en for en in enumerations_array.content if en.attributes or en.meta]
                    if enums_w_attrs_or_meta:
                        # not all of them have typeAttributes?
                        # self.assertEqual(len(enumerations_array.content), len(enums_w_attrs_or_meta))
                        # none of them have meta
                        self.assertTrue(all(en for en in enums_w_attrs_or_meta if en.meta is None))
                        for enum_el in enums_w_attrs_or_meta:
                            enum_el: ApibString
                            self.assertEqual('string', enum_el.element)
                            # typeAttributes is the only attribute
                            self.assertEqual({'typeAttributes'}, set(enum_el.attributes))
                            type_attributes = enum_el.attributes['typeAttributes']
                            self.assertTrue(isinstance(type_attributes, ApibArray))

                            # typeAttributes are a list of strings
                            self.assertIsNone(type_attributes.meta)
                            self.assertIsNone(type_attributes.attributes)

                            # meta and attributes is None for all attributes
                            self.assertTrue(
                                all(a.meta is None and a.attributes is None for a in type_attributes.content))

                            # 'fixed' is always present
                            attribute_set = set(a.content for a in type_attributes.content)
                            self.assertTrue('fixed' in attribute_set)
                        foo = 1
                if default is not None:
                    # default is someting like:
                    #   {'content': {'content': 'name', 'element': 'string'}, 'element': 'enum'}
                    self.assertEqual('enum', default['element'])
                    default_content = ApibString.model_validate(default['content'])

        print('content str values:')
        print("\n".join(f'  * {cs}' for cs in sorted(content_str)))
        print(f'enum element types: {", ".join(sorted(enumeration_element_types))}')

    def test_data_structures(self):
        """
        understand data structures
        """
        self.stream_handler.setLevel(logging.INFO)
        ds_child_elements = set()
        for apib_path, apib_data in self.apib_path_and_data():
            apib_path = os.path.basename(apib_path)
            parsed = ApibParseResult.model_validate(apib_data)
            for el_info in parsed.elements_with_path():
                element, path, element_path = el_info
                if element.element != 'dataStructure':
                    continue
                try:
                    self.assertTrue(isinstance(element, ApibDatastucture))
                    content = element.content
                    # if isinstance(content, ApibElement):
                    #     if content.element not in {'object', 'enum', 'array'}:
                    #         ds_child_elements.add(content.element)
                    #         if any((content.content, content.attributes, content.meta)):
                    #             print(f'{apib_path}, {el_info.elem_path_extended} unexpected content, attributes, '
                    #                   f'or meta: '
                    #                   f'{", ".join(f"{s}" for s in (content.content, content.attributes,
                    #                   content.meta) if s)}')
                    #             # self.assertTrue(False,
                    #             #                 "unexpected content, attributes, or meta")
                    #     continue
                    # datastructures only exist in lists
                    if isinstance(element_path[-1], list):
                        parent = element_path[-2]
                        parent: ApibElement
                        self.assertTrue(parent.element in {'httpRequest', 'httpResponse', 'category'})
                        if parent.element == 'category':
                            # content should be an object
                            self.assertTrue(True or isinstance(element.content, ApibElement) and
                                            element.content.element == 'object',
                                            'child should be "object"')
                            foo = 1
                            ...
                        else:
                            self.assertTrue(True or not any((content.content, content.attributes, content.meta)),
                                            "unexpected content, attributes, or meta")
                            ...
                    elif isinstance(element_path[-1], ApibTransition):
                        self.assertTrue(True or
                                        isinstance(element.content,
                                                   ApibElement) and element.content.element == 'object')

                        ...
                    else:
                        self.assertTrue(False)
                except AssertionError as e:
                    raise e
        print(', '.join(sorted(ds_child_elements)))

    def test_007_find_key_value(self):
        """
        Where do key/value elements show up?
        :return:
        """
        kv_parents = set()
        value_keys = set()
        err = False
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                if attr_info.attr_name != 'content':
                    continue
                content = attr_info.attr_value
                if is_key_value(content):
                    # key/value should only exist in list
                    m = re.match(r'.+((:?\.\w+){2})\.content\[\d+]$', attr_info.path)
                    self.assertIsNotNone(m, f'key value not part of list: {path}')
                    path_match = m.group(1)
                    if not path_match.startswith('.attributes'):
                        err = True
                        print(f'{path}: {path_match}, {attr_info.attr_value}')
                        # should still be part of a list
                        self.assertTrue(isinstance(attr_info.data_path[-1], list))
                        self.assertTrue(is_element(attr_info.data_path[-2]))
                        self.assertTrue(is_element(attr_info.data_path[-3]))
                        self.assertEqual('enum', attr_info.data_path[-3]['element'])
                        meta = attr_info.data_path[-3].get('meta')
                        self.assertIsNotNone(meta)
                        meta_id = meta.get('id')
                        self.assertIsNotNone(meta_id)
                        meta_id_content = meta_id.get('content')
                        print(f'   {meta_id_content}')
                    self.assertTrue(True or path_match.startswith('.attributes'))
                    kv_parents.add(m.group(1))
                    value = content['value']

                    value_keys.add(', '.join(sorted(value)))
        print(', '.join(sorted(kv_parents)))
        print('Keys of value attributes:')
        print('\n'.join(sorted(value_keys)))
        self.assertFalse(err)

    def test_008_element_content_variants(self):
        """
        Validate all 'content' types of 'elements'
        'content' can be:
            * int
            * str
            * list ('element')
            * key/value
            * 'element'
            * None
        """
        elements = set()
        addtl_attrs = set()
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            for attr_info in all_attrs(data):
                try:
                    element_info = attr_info.attr_value['element']
                except (TypeError, KeyError):
                    continue
                content = attr_info.attr_value.get('content')
                if isinstance(content, list):
                    element_info = f'{element_info}, list, len: {len(content)}'
                    self.assertTrue(all(is_element(c) for c in content))
                elif isinstance(content, str):
                    element_info = f'{element_info}, str'
                elif isinstance(content, int):
                    element_info = f'{element_info}, int'
                elif is_key_value(content):
                    element_info = f'{element_info}, key/value'
                elif is_element(content):
                    element_info = f'{element_info}, element ({content["element"]})'
                elif content is None:
                    element_info = f'{element_info}, None'
                else:
                    raise ValueError
                addtl = {k: v for k, v in attr_info.attr_value.items() if k not in {'element', 'content'}}
                if addtl:
                    element_info = f'{element_info} ... {", ".join(sorted(addtl))}'
                    addtl_attrs.add(', '.join(sorted(addtl)))
                elements.add(element_info)
        print('\n'.join(sorted(elements)))

        print('Addtl. attributes of element items:')
        print('\n'.join(sorted(addtl_attrs)))

    def test_009_parse_obj(self):
        """
        Parse all APIBs
        """
        err = None
        logging.getLogger().setLevel(logging.DEBUG)
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            try:
                parsed = ApibParseResult.model_validate(data)
            except ValidationError as e:
                print(f'{path}: {e}')
                raise
                err = err or e
                continue
        if err:
            raise err

    def test_010_parse_obj_and_check_copy(self):
        """
        looks like only these element types have 'copy' elements in their content:
            * category
            * httpRequest
            * httpResponse
            * transition
        .. and there is always only one 'copy' element
        """
        # which elements hava copy elements?
        element_types_w_copy_content = defaultdict(int)
        for path, data in self.apib_path_and_data():
            parsed = ApibParseResult.model_validate(data)
            for element in parsed.elements():
                copy_elements_in_content = list(element.content_elements_by_type(content_element_type='copy'))
                if copy_elements_in_content:
                    element_types_w_copy_content[element.element] = max(element_types_w_copy_content[element.element],
                                                                        len(copy_elements_in_content))

        print('\n'.join(f'{et}: {element_types_w_copy_content[et]}' for et in sorted(element_types_w_copy_content)))

    def test_011_parse_obj_and_dump_category_docstring(self):
        """
        """
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            print(f'{path}:')
            print('-' * 80)
            print(parsed.api.doc_string)
            print('\n' * 3)

    def test_012_blueprints_wo_category_docstring(self):
        """
        """
        err = False
        # suppress debug messages
        self.stream_handler.setLevel(logging.INFO)
        no_docstring = []
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            if not parsed.api.doc_string:
                no_docstring.append(path)
                err = True
        print('no docstrings:')
        print('\n'.join(sorted(no_docstring)))
        self.assertFalse(err)

    def test_parsed_categories_wo_doctring(self):
        """
        look for 'category' elements w/o docstring
        """
        self.stream_handler.setLevel(logging.INFO)
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el, path, elem_path in parsed.elements_with_path():
                el: ApibCategory
                if el.element != 'category' or el.copy_content:
                    continue
                self.assertTrue(False)

    def test_parsed_boolean_is_always_child_of_member(self):
        self.stream_handler.setLevel(logging.INFO)
        err = False
        bool_content = set()
        ancestor_set = set()
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in parsed.elements_with_path():
                if el_info.element.element != 'boolean':
                    continue
                try:
                    # these elements should be parsed as ApibBool
                    bool_element = el_info.element
                    self.assertTrue(isinstance(bool_element, ApibBool), f'Should be an ApibBool, '
                                                                        f'is {bool_element.__class__.__name__}')

                    # .. should always be child of member
                    elem_path = el_info.elem_path
                    self.assertTrue(elem_path.endswith('.member'), f'Should be child of member, '
                                                                   f'is {elem_path.split(".")[-1]}')

                    # .. let's look at all ancestors
                    ancestors = '.'.join(elem_path.split('.')[-3:])
                    ancestor_set.add(ancestors)
                    parent = el_info.data_path[-1]
                    parent: ApibMember
                    content = el_info.element.content
                    if content is not None:
                        bool_content.add(content)
                except ValidationError as e:
                    print(f'{path}, {el_info.elem_path_extended}: {e}')
                    err = True
        print(f'Values: {", ".join(f"{s}" for s in sorted(bool_content))}')
        print('Ancestors')
        print('\n'.join(sorted(ancestor_set)))
        self.assertFalse(err)

    def test_parsed_number(self):
        """
        look at parsed "number" elements
        """
        self.stream_handler.setLevel(logging.INFO)
        err = None
        number_class_counter = defaultdict(int)
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in parsed.elements_with_path():
                if el_info.element.element != 'number':
                    continue
                try:
                    # these elements should be parsed as ApibNumber
                    number_element = el_info.element
                    number_element: ApibNumber
                    number_class_counter[number_element.__class__.__name__] += 1
                    self.assertTrue(isinstance(number_element, ApibNumber), f'Should be an ApibNumber, '
                                                                            f'is {number_element.__class__.__name__}')
                    self.assertIsNone(number_element.meta, 'Unexpected meta')
                    self.assertTrue(number_element.content is None or isinstance(number_element.content, float),
                                    f'Unexpected instance: {number_element.content.__class__.__name__}')

                    if attributes := number_element.attributes:
                        self.assertEqual({'default'}, set(attributes))
                    foo = 1
                except ValidationError as e:
                    print(f'{path}, {el_info.elem_path_extended}: {e}')
                    err = err or e
        print('\n'.join(f'{k}: {v}' for k,v in number_class_counter.items()))
        if err:
            raise err

    def test_parsed_where_do_transition_elements_live(self):
        """
        Look for 'transition' elements and check where they live
        """
        expected_paths = {'parseResult.category.resource', 'parseResult.category.category.resource'}
        transition_paths = set()
        self.stream_handler.setLevel(logging.INFO)
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in parsed.elements_with_path():
                if el_info.element.element != 'transition':
                    continue
                elem_path = el_info.elem_path
                transition_paths.add(elem_path)
                if elem_path not in expected_paths:
                    print(f'{path}: unexpected path for "transition" element: {elem_path}')
        print('\n'.join(sorted(transition_paths)))
        self.assertEqual(expected_paths, transition_paths)

    def test_parsed_transition_has_title(self):
        self.stream_handler.setLevel(logging.INFO)
        err = False
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in parsed.elements_with_path():
                transition = el_info.element
                if transition.element != 'transition':
                    continue
                transition: ApibTransition
                if not transition.title:
                    print(f'{path}, {el_info.elem_path_extended}: no title')
                    err = True
        self.assertFalse(err)

    def test_parsed_transition_has_href(self):
        self.stream_handler.setLevel(logging.INFO)
        err = False
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in parsed.elements_with_path():
                transition = el_info.element
                if transition.element != 'transition':
                    continue
                transition: ApibTransition
                if not transition.href:
                    print(f'{path}, {el_info.elem_path_extended}.{transition.title}: no href')
                    # then the href might be in a parent
                    parent_with_href = next((el for el in reversed(el_info.data_path)))
                    err = True
        self.assertFalse(err)

    def test_parsed_http_transaction_has_request_and_response(self):
        self.stream_handler.setLevel(logging.INFO)
        err = False
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in parsed.elements_with_path():
                http_transaction = el_info.element
                if http_transaction.element != 'httpTransaction':
                    continue
                http_transaction: ApibHttpTransaction
                issues = []
                if not http_transaction.request:
                    issues.append('no request')
                if not http_transaction.request:
                    issues.append('no response')
                if issues:
                    err = True
                    print(f'{path}, {el_info.elem_path_extended}: {", ".join(issues)}')
        self.assertFalse(err)

    def test_parsed_object_only_has_member_as_child(self):
        self.stream_handler.setLevel(logging.INFO)
        err = None
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in parsed.elements_with_path():
                object_element = el_info.element
                if object_element.element != 'object':
                    continue
                object_element: ApibElement
                # content should always be a list
                content = object_element.content

                try:
                    # if an object has no content then meta.id has to exist and is a class name
                    if content is None:
                        self.assertTrue(object_element.meta and object_element.meta.id,
                                        f'content is None and there is no meta.id')
                    else:
                        self.assertTrue(isinstance(content, list), f'Should be list, is {content.__class__.__name__}')
                except AssertionError as e:
                    print(f'{path}, {el_info.elem_path_extended}: {e}')
                    err = err or e

        if err:
            raise err

    def test_parsed_understand_http_responses(self):
        self.stream_handler.setLevel(logging.INFO)
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in parsed.elements_with_path():
                http_response = el_info.element
                if http_response.element != 'httpResponse':
                    continue
                http_response: ApibHttpResponse
                if http_response.status_code == 204 and not any((http_response.headers, http_response.datastructure,
                                                                 http_response.message_body,
                                                                 http_response.message_body_schema)):
                    continue
                issues = []
                if not http_response.headers:
                    issues.append('no headers')
                if any((http_response.message_body, http_response.message_body_schema, http_response.datastructure)):
                    if not http_response.message_body:
                        issues.append('no message body')
                    if not http_response.message_body_schema:
                        issues.append('no message body schema')
                    if not http_response.datastructure:
                        issues.append('no datastructure')
                if issues:
                    print(f'{path}, {el_info.elem_path_extended}: {", ".join(issues)}')

    def test_parsed_annotation(self):
        """
        check parsed 'annotation' elements
        """
        self.stream_handler.setLevel(logging.INFO)
        err = None
        meta_classes = set()
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in parsed.elements_with_path():
                annotation = el_info.element
                if annotation.element.lower() != 'annotation':
                    continue
                annotation: ApibAnnotation
                try:
                    self.assertIsNone(annotation.attributes)
                    meta = annotation.meta
                    self.assertIsNotNone(meta)
                    self.assertIsNone(meta.id)
                    self.assertIsNone(meta.description)
                    self.assertIsNone(meta.title)
                    self.assertIsNotNone(meta.classes)
                    meta_classes.update(meta.classes)
                    self.assertIsNotNone(annotation.code)
                except AssertionError as e:
                    print(f'{path}, {el_info.elem_path_extended}: {e}')
                    err = err or e
        print(f'meta classes: {", ".join(sorted(meta_classes))}')
        if err:
            raise err

    def test_parsed_asset(self):
        """
        check parsed 'asset' elements
        """
        self.stream_handler.setLevel(logging.INFO)
        err = None
        meta_classes = set()
        parents = set()
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in parsed.elements_with_path():
                asset = el_info.element
                if asset.element.lower() != 'asset':
                    continue
                try:
                    self.assertTrue(isinstance(asset.content, str))
                    attributes = asset.attributes
                    meta = asset.meta
                    # asset always has meta
                    # Attributes are optional
                    self.assertTrue(meta)
                    self.assertTrue(not any((meta.description, meta.id, meta.title)))

                    # collect meta classes
                    self.assertTrue(meta.meta_class)
                    meta_classes.add(meta.meta_class)

                    # collect parents
                    parent = el_info.elem_path.split('.')[-1]
                    parents.add(parent)
                except AssertionError as e:
                    print(f'{path}, {el_info.elem_path_extended}: {e}')
                    err = err or e
        print(f'meta classes: {", ".join(sorted(meta_classes))}')
        print(f'parents: {", ".join(sorted(parents))}')

        if err:
            raise err

    def test_parsed_object(self):
        """
        check parsed 'object' elements
        """
        self.stream_handler.setLevel(logging.INFO)
        err = None
        meta_classes = set()
        parents = set()
        content_types = set()
        content_list_members = set()
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in parsed.elements_with_path():
                object_element = el_info.element
                if object_element.element.lower() != 'object':
                    continue
                try:
                    content = object_element.content
                    # content is always a list
                    if content:
                        content_types.add(content.__class__.__name__)
                        self.assertEqual('list', content.__class__.__name__)
                        content_list_members.update(c.element for c in content)

                    # only attribute is 'typeAttributes'
                    attributes = object_element.attributes
                    if attributes:
                        self.assertFalse(set(attributes)-{'typeAttributes'})
                    # self.assertIsNone(attributes)
                    foo = 1

                    # collect parents
                    parent = el_info.elem_path.split('.')[-1]
                    parents.add(parent)
                except AssertionError as e:
                    print(f'{path}, {el_info.elem_path_extended}: {e}')
                    err = err or e
        print(f'content types: {", ".join(sorted(content_types))}')
        print(f'content list members: {", ".join(sorted(content_list_members))}')
        print(f'parents: {", ".join(sorted(parents))}')

        if err:
            raise err

    def test_parsed_select(self):
        """
        check parsed 'select' elements
        """
        self.stream_handler.setLevel(logging.INFO)
        err = None
        parents = set()
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in parsed.elements_with_path():
                select_element = el_info.element
                if select_element.element.lower() != 'select':
                    continue
                try:
                    content = select_element.content
                    # content is always a list
                    self.assertEqual('list', content.__class__.__name__)
                    # there are no attributes
                    self.assertIsNone(select_element.attributes)
                    # no meta
                    self.assertIsNone(select_element.meta)

                    # collect parents
                    parent = el_info.elem_path.split('.')[-1]
                    parents.add(parent)

                    # childs are 'option' elements
                    self.assertTrue(all(c.element == 'option' for c in content))

                    for option_element in content:
                        self.assertTrue(isinstance(option_element.content, list))
                        self.assertEqual(1, len(option_element.content))
                        member = option_element.content[0]
                        self.assertEqual('member', member.element)
                        member: ApibMember
                        self.assertIsNone(member.attributes)
                        self.assertIsNone(member.content)
                        member_meta = member.meta
                        # meta can exist
                        if member_meta:
                            # .. and only has a description
                            self.assertIsNone(member_meta.classes)
                            self.assertIsNone(member_meta.id)
                            self.assertIsNone(member_meta.title)
                            self.assertIsNotNone(member_meta.description)
                        self.assertIsNotNone(member.key)

                except AssertionError as e:
                    print(f'{path}, {el_info.elem_path_extended}: {e}')
                    err = err or e
        print(f'parents: {", ".join(sorted(parents))}')

        if err:
            raise err

    def test_013_blueprint_category_meta(self):
        """
        """
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            self.assertTrue(parsed.api.meta.title)
            print(f'{path}: title "{parsed.api.meta.title}"')
            error_member = next((member for member in parsed.api.metadata
                                 if not member.key or member.value.element != 'string' or not member.value.content),
                                None)
            self.assertIsNone(error_member, f'member error: {error_member}')
            for member in parsed.api.metadata:
                print(f'  {member.key} = {member.value.content}')
            print(f'  host = {parsed.api.host}')
            foo = 1

    def test_014_transition_elements(self):
        """
        Understand 'transition' elements
        """
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for element in (e for e in parsed.elements() if isinstance(e, ApibTransition)):
                self.assertIsNotNone(element.meta)
                self.assertIsNotNone(element.meta.title)
                foo = 1

    def test_015_transition_w_data(self):
        """
        Some transition elenents have "data". Understand the content
        """
        logging.getLogger().setLevel(logging.WARNING)
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for element in (e for e in parsed.elements() if isinstance(e, ApibTransition) and e.data):
                element: ApibTransition
                print(f'{path}, "{element.title}" has data: element={element.data.element}')

    def test_016_href_variables_wo_value(self):
        """
        Some transitions have href varibles w/o value
        """
        logging.getLogger().setLevel(logging.WARNING)
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.model_validate(data)
            for element in (e for e in parsed.elements() if isinstance(e, ApibTransition)):
                element: ApibTransition
                href_vars_wo_value = [hm for hm in element.href_variables if not hm.value]
                if href_vars_wo_value:
                    print(f'{path}, "{element.title}" has hrefVariables w/o value: '
                          f'{", ".join(hv.key for hv in href_vars_wo_value)}')

    def test_017_ApibEnumElement_with_extra_attribute(self):
        """
        # TODO: still not really clear when empty elements occur. Also see ApibEnum.val_root_enum()
        """
        err = False
        logging.getLogger().setLevel(logging.WARNING)
        for apib_path, data in self.apib_path_and_data():
            apib_path = os.path.basename(apib_path)
            parsed = ApibParseResult.model_validate(data)
            for el_info in (eli
                            for eli in parsed.elements_with_path()
                            if isinstance(eli.element, ApibEnumElement)):
                element, path, elem_path = el_info
                element: ApibEnumElement

                member = next((el for el in reversed(elem_path)
                               if isinstance(el, ApibMember) and el.key),
                              None)
                member_key = member and member.key or '???'
                ds_object = next((el for el in reversed(elem_path)
                                  if isinstance(el, ApibElement) and el.element == 'object'),
                                 None)
                ds_id = ds_object and ds_object.meta and ds_object.meta.id or '???'

                if not element.content:
                    print(f'{apib_path}, {ds_id}.{member_key}: no content')
                    # '*' in an enum apparently is parsed as
                    err = True
                if (addtl_attr := set(element.__dict__) - {'attributes', 'content', 'element', 'meta',
                                                           'type_attributes'}):
                    print(f'{apib_path}, {ds_id}.{member_key}: '
                          f'addtl. attributes: {", ".join(sorted(addtl_attr))}')

                    err = True
        self.assertFalse(err, 'Some errors, check output')

    def test_root_validators_and_subclasses(self):
        class Base(BaseModel):
            a: str

            @model_validator(mode='before')
            def vaL_root_base(cls, v):
                print(f'val_root_base: {v}')
                return v

        class Sub(Base):
            b: str

            @model_validator(mode='wrap')
            def val_root_sub(cls, v, handler):
                v = handler(v)
                print(f'val_root_sub: {v}')
                return v

        sub = Sub.model_validate({'a': 'a', 'b': 'b'})
        print(sub)

    def test_validate_sourcemap(self):
        data = [{'element': 'array', 'content': [{'element': 'number', 'attributes': {'line': {'element': 'number', 'content': 204}, 'column': {'element': 'number', 'content': 7}}, 'content': 8988}, {'element': 'number', 'attributes': {'line': {'element': 'number', 'content': 204}, 'column': {'element': 'number', 'content': 11}}, 'content': 5}]}, {'element': 'array', 'content': [{'element': 'number', 'attributes': {'line': {'element': 'number', 'content': 205}, 'column': {'element': 'number', 'content': 9}}, 'content': 9001}, {'element': 'number', 'attributes': {'line': {'element': 'number', 'content': 205}, 'column': {'element': 'number', 'content': 10}}, 'content': 2}]}, {'element': 'array', 'content': [{'element': 'number', 'attributes': {'line': {'element': 'number', 'content': 206}, 'column': {'element': 'number', 'content': 9}}, 'content': 9011}, {'element': 'number', 'attributes': {'line': {'element': 'number', 'content': 206}, 'column': {'element': 'number', 'content': 110}}, 'content': 102}]}, {'element': 'array', 'content': [{'element': 'number', 'attributes': {'line': {'element': 'number', 'content': 207}, 'column': {'element': 'number', 'content': 9}}, 'content': 9121}, {'element': 'number', 'attributes': {'line': {'element': 'number', 'content': 207}, 'column': {'element': 'number', 'content': 38}}, 'content': 30}]}, {'element': 'array', 'content': [{'element': 'number', 'attributes': {'line': {'element': 'number', 'content': 208}, 'column': {'element': 'number', 'content': 9}}, 'content': 9159}, {'element': 'number', 'attributes': {'line': {'element': 'number', 'content': 208}, 'column': {'element': 'number', 'content': 10}}, 'content': 2}]}]
        parsed_content = TypeAdapter(list[AbibSourceMapNumberArray]).validate_python(data)
        print(parsed_content)
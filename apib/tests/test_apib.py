"""
Test reading apib files
"""
import glob
import logging
import os.path
import re
import sys
from collections import Counter, defaultdict
from collections.abc import Generator
from dataclasses import dataclass
from typing import ClassVar, Any, NamedTuple
from unittest import TestCase

from pydantic import ValidationError, parse_obj_as

from private.apib.apib import read_api_blueprint, is_element, ApibParseResult, ApibCopy, ApibWithCopy, ApibTransition, \
    ApibString, ApibArray, ApibEnumElement, ApibEnum, ApibMember, ApibElement, ApibDatastucture


@dataclass(init=False)
class ApibTest(TestCase):
    apib_paths: ClassVar[list[str]]
    apib_data: ClassVar[dict[str, dict]]
    stream_handler: logging.StreamHandler
    log_level: int

    @classmethod
    def setUpClass(cls) -> None:
        api_apecs = os.path.dirname(__file__)
        api_specs = os.path.join(api_apecs, *(['..'] * 4), 'api-specs')
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
        logger.addHandler(stream_handler)
        self.stream_handler = stream_handler

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


class AttrInfo(NamedTuple):
    path: str
    attr_name: str
    attr_value: Any


def all_attrs(data: Any, path: str = None) -> Generator[AttrInfo, None, None]:
    path = path or '/'
    if not isinstance(data, dict):
        return
    data: dict
    yield AttrInfo(path=path, attr_name='', attr_value=data)
    for k, v in data.items():
        yield AttrInfo(path=path, attr_name=k, attr_value=v)
        # descend down into list element and child dicts
        if isinstance(v, list):
            # look at all list elements
            for i, child in enumerate(v):
                yield from all_attrs(data=child, path=f'{path}.{k}[{i}]')
        elif isinstance(v, dict):
            # look at all dict values
            for a, child in v.items():
                yield from all_attrs(data=child, path=f'{path}.{k}.{a}')


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
                    r = re.findall(r'<!-- feature-toggle.+? -->', attr_info.attr_value)
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

    def test_attributes(self):
        """
        Which elements have 'attributes' and what attributes life in those 'attributes'?
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
                            str_val = ApibString.parse_obj(v)
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
                    # .. and if it's there tben it's a 'string
                    # content should be a string (the enum name?)
                    content = ApibString.parse_obj(values['content'])
                    content_str.add(content.content)
                # attributes are optional ..
                attributes = values.get('attributes')
                if attributes is not None:
                    # 'enumerations' and 'default' are the only attributes
                    self.assertFalse(set(attributes) - {'enumerations', 'default'})
                    # 'enumerations" are mandatory
                    enumerations = attributes.get('enumerations')
                    self.assertIsNotNone(enumerations)
                    default = attributes.get('default')

                    # enumerations are an array
                    enumerations_array = ApibArray.parse_obj(enumerations)
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
                            # typeAttributes are a list of strings
                            attributes = ApibArray.parse_obj(type_attributes, element='string')
                            # can have more than one attribute
                            # self.assertEqual(1, len(attributes.content))
                            self.assertIsNone(attributes.meta)
                            self.assertIsNone(attributes.attributes)
                            # meta and attributes is None for all attributes
                            self.assertTrue(all(a.meta is None and a.attributes is None for a in attributes.content))
                            # 'fixed' is always present
                            attribute_set = set(a.content for a in attributes.content)
                            self.assertTrue('fixed' in attribute_set)
                        foo = 1
                if default is not None:
                    # default is someting like:
                    #   {'content': {'content': 'name', 'element': 'string'}, 'element': 'enum'}
                    self.assertEqual('enum', default['element'])
                    default_content = ApibString.parse_obj(default['content'])

        print('content str values:')
        print("\n".join(f'  * {cs}' for cs in sorted(content_str)))
        print(f'enum element types: {", ".join(sorted(enumeration_element_types))}')

    def test_data_structures(self):
        """
        understand data structures
        """
        ds_child_elements = set()
        for apib_path, apib_data in self.apib_path_and_data():
            apib_path = os.path.basename(apib_path)
            parsed = ApibParseResult.parse_obj(apib_data)
            for element, path, element_path in parsed.elements_with_path():
                if element.element != 'dataStructure':
                    continue
                try:
                    self.assertTrue(isinstance(element, ApibDatastucture))
                    content = element.content
                    if isinstance(content, ApibElement):
                        if content.element not in  {'object', 'enum', 'array'}:
                            ds_child_elements.add(content.element)
                            self.assertTrue(not any ((content.content, content.attributes, content.meta)),
                                            "unexpected content, attributes, or meta")
                    continue
                    # datastructures only exist in lists
                    if isinstance(element_path[-1], list):
                        parent = element_path[-2]
                        parent: ApibElement
                        self.assertTrue(parent.element in {'httpRequest', 'httpResponse', 'category'})
                        if parent.element == 'category':
                            # content should ne an object
                            self.assertTrue(isinstance(element.content, ApibElement) and
                                            element.content.element=='object',
                                            'child should be "object"')
                            foo = 1
                            ...
                        else:
                            self.assertTrue(not any ((content.content, content.attributes, content.meta)),
                                            "unexpected content, attributes, or meta")
                        foo = 1
                        ...
                    elif isinstance(element_path[-1], ApibTransition):
                        self.assertTrue(isinstance(element.content, ApibElement) and element.content.element=='object')
                        foo = 1
                        ...
                    else:
                        self.assertTrue(False)
                except AssertionError as e:
                    raise e
        print(', '.join(sorted(ds_child_elements)))

    def test_007_find_key_value(self):
        kv_parents = set()
        value_keys = set()
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
                    self.assertTrue(m.group(1).startswith('.attributes'))
                    kv_parents.add(m.group(1))
                    value = content['value']

                    value_keys.add(', '.join(sorted(value)))
        print(', '.join(sorted(kv_parents)))
        print('Keys of value attributes:')
        print('\n'.join(sorted(value_keys)))

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
        :return:
        """
        err = None
        logging.getLogger().setLevel(logging.DEBUG)
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            try:
                parsed = ApibParseResult.parse_obj(data)
            except ValidationError as e:
                print(f'{path}: {e}')
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
            parsed = ApibParseResult.parse_obj(data)
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
            parsed = ApibParseResult.parse_obj(data)
            print(f'{path}:')
            print('-' * 80)
            print(parsed.category.doc_string)
            print('\n' * 3)

    def test_012_blueprints_wo_category_docstring(self):
        """
        """
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.parse_obj(data)
            if not parsed.category.doc_string:
                print(f'{path}: has no docstring')

    def test_013_blueprint_category_meta(self):
        """
        """
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.parse_obj(data)
            self.assertTrue(parsed.category.meta.title)
            print(f'{path}: title "{parsed.category.meta.title}"')
            error_member = next((member for member in parsed.category.metadata
                                 if not member.key or member.value.element != 'string' or not member.value.content),
                                None)
            self.assertIsNone(error_member, f'member error: {error_member}')
            for member in parsed.category.metadata:
                print(f'  {member.key} = {member.value.content}')
            print(f'  host = {parsed.category.host}')
            foo = 1

    def test_014_transition_elements(self):
        """
        Understand 'transition' elements
        """
        for path, data in self.apib_path_and_data():
            path = os.path.basename(path)
            parsed = ApibParseResult.parse_obj(data)
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
            parsed = ApibParseResult.parse_obj(data)
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
            parsed = ApibParseResult.parse_obj(data)
            for element in (e for e in parsed.elements() if isinstance(e, ApibTransition)):
                element: ApibTransition
                href_vars_wo_value = [hm for hm in element.href_variables if not hm.value]
                if href_vars_wo_value:
                    print(f'{path}, "{element.title}" has hrefVariables w/o value: '
                          f'{", ".join(hv.key for hv in href_vars_wo_value)}')

    def test_017_ApibEnumElement_with_extra_attribute(self):
        """
        # TODO: still not really clear when empty elements occur. Also see val_root_enum()
        """
        err = False
        logging.getLogger().setLevel(logging.WARNING)
        for apib_path, data in self.apib_path_and_data():
            apib_path = os.path.basename(apib_path)
            parsed = ApibParseResult.parse_obj(data)
            for element, path, elem_path in ((e, p, ep)
                                             for e, p, ep in parsed.elements_with_path()
                                             if isinstance(e, ApibEnumElement)):
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
                    err = True
                if (addtl_attr := set(element.__dict__) - {'attributes', 'content', 'element', 'meta',
                                                           'type_attributes'}):
                    print(f'{apib_path}, {ds_id}.{member_key}: '
                          f'addtl. attributes: {", ".join(sorted(addtl_attr))}')

                    err = True
        self.assertFalse(err, 'Some errors, check output')

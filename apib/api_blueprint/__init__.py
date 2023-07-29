"""
Helper to read apib files
"""
import json
import logging
import re
import subprocess
import sys
import typing
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Any, ClassVar

from pydantic import BaseModel, root_validator, Extra, Field, ValidationError

node_log = logging.getLogger(f'{__name__}.Node')


def simple_value(v):
    """
    Simplify a value:
        {'element': 'array', 'content': [....]} --- simplified to --> [....]
        {'element': 'string', 'content': 'fixed'} --- simplified to --> 'fixed'
        {'element': 'number', 'content': 10} --- simplified to --> 10
    :param v:
    :return: simplification or None
    """
    if not isinstance(v, dict):
        return v
    if len(v) != 2:
        return v
    try:
        element = v['element']
        content = v['content']
    except KeyError:
        return v
    if element == 'array':
        arr = [simple_value(c) for c in content]
        return arr
    elif element in {'string', 'number', 'boolean'}:
        return content
    return v


def is_list(ann):
    try:
        return ann.__origin__ == list or any(map(is_list, ann.__args__))
    except AttributeError:
        return False


def is_str(ann) -> bool:
    try:
        return ann == str or any(map(is_str, ann.__args__))
    except AttributeError:
        return False

    if ann == str:
        return True
    try:
        return ann.__origin__ == typing.Union and str in ann.__args__
    except AttributeError:
        pass
    return False


@dataclass(init=False)
class Node(BaseModel):
    class Config:
        extra = Extra.allow

    _element: ClassVar[str]
    _node_class: ClassVar[str]

    # noinspection PyMethodOverriding
    def __init_subclass__(cls, element: str = '', node_class: str = ''):
        """
        record expected "element" value
        """
        super().__init_subclass__()
        cls._element = element
        cls._node_class = node_class
        return

    @root_validator(pre=False)
    def node_post(cls, values):
        """
        Post validator, check node class (optional)
        :param values:
        :return:
        """
        if cls._node_class:
            classes = values.get('classes')
            if not classes or cls._node_class not in classes:
                raise ValueError(f'Wrong class: {classes}, expected: {cls._node_class}')
        return values

    @root_validator(pre=True)
    def node(cls, values):
        """
        Pre validator
        """
        node_log.debug(f'node({cls.__name__})<: {str(values):.500}')
        if cls._element:
            element = values.pop('element', None)
            assert 'element' not in values

            if cls._element != element:
                raise ValueError(f'Expected element="{cls._element}"')
            node_log.debug(f'node({cls.__name__}) : element attribute "{cls._element}" validated')

        else:
            node_log.debug(f'node({cls.__name__}) : no class var "element"')

        class_fields = cls.__fields__

        # move 'attributes' up if no field 'attributes' is explicitly defined
        if 'attributes' not in class_fields and (attrs := values.pop('attributes', None)):
            node_log.debug(f'node({cls.__name__}) : pulling attributes up: {", ".join(attrs)}')
            # values.update(attrs)
            for attr, value in attrs.items():
                s_value = simple_value(value)
                node_log.debug(f'node({cls.__name__}) : attribute {attr} value: {value} simplified value: {s_value}')
                values[attr] = s_value

        # move 'meta' up if no field 'meta' is explicitly defined
        if 'meta' not in class_fields and (meta := values.pop('meta', None)):
            node_log.debug(f'node({cls.__name__}) : pulling meta up, {", ".join(meta):.500}')
            # values.update(meta)
            for attr, value in meta.items():
                values[attr] = simple_value(value)
                # values[attr] = simple_value(value['content']) or value['content']

        # all elements in content need to be moved one level up (if they are models)
        if 'content' in class_fields:
            # if the model actually defines an attribute "content" then we leave the data as is
            node_log.debug(f'node({cls.__name__})> (content field present): {str(values):.500}')
            return values

        # generate list by element key
        updates = defaultdict(list)
        content_list = values.get('content', [])
        if not isinstance(content_list, list):
            content_list = [content_list]
        for content_element in content_list:
            try:
                content_element_key = content_element['element']
                updates[content_element_key].append(simple_value(content_element))
            except KeyError:
                # could be something like this:
                # {'key': {'element': 'string', 'content': '...'}, 'value': {'element': 'string', 'content': '...'}}
                for k, v in content_element.items():
                    v = simple_value(v)
                    values[k] = v
                pass

        # fields can be lists or single entities. For all fields not defined as list we try to convert the list in the
        # update to a single entity
        for field in class_fields.values():
            try:
                if is_list(field.annotation):
                    # leave lists unchanged
                    continue

            except AttributeError:
                # ignore AttributeError: the field annotation is no Generic
                pass

            # this field is not supposed to be a list
            list_elements = updates.get(field.alias)

            # only convert single element list to make sure validation fails if more than one value was provided
            if list_elements and len(list_elements) == 1:
                updates[field.alias] = list_elements[0]
                # if the desired type is a string, and we only have element/content with content being a str then
                # simplify
                if is_str(field.annotation) and isinstance(le := list_elements[0], dict) and \
                        set(le) == {'element', 'content'} and isinstance(v := le['content'], str):
                    updates[field.alias] = v

        # now remove the 'content' attribute
        values.pop('content', None)
        # ... and apply the updates
        node_log.debug(f'node({cls.__name__}) : updates for: {", ".join(updates):.500}')

        values.update(updates)

        updates = {k: simple
                   for k, v in values.items()
                   if (simple := simple_value(v)) != v}
        if updates:
            node_log.debug(f'node({cls.__name__}) : update simple values {", ".join(updates):.500}')
            values.update(updates)

        node_log.debug(f'node({cls.__name__})>: {str(values):.500}')
        return values

    @classmethod
    def parse_obj(cls: typing.Type['Model'], obj: Any) -> 'Model':
        try:
            return super().parse_obj(obj)
        except ValidationError as e:
            foo = 1
            raise


class SourceMapNumber(Node, element='number'):
    content: int
    line: int
    column: int

    @root_validator(pre=True)
    def source_map_number(cls, values: dict) -> dict:
        if not isinstance(values['line'], int) or not isinstance(values['column'], int):
            foo = 1
        return values


class SourceMap(Node, element='sourceMap'):
    lines: list[list[SourceMapNumber]] = Field(alias='array')

    @root_validator(pre=True)
    def source_map(cls, values: dict) -> dict:
        return values


class Annotation(Node, element='annotation'):
    content: str
    classes: list[str]
    code: int
    source_map: list[SourceMap] = Field(alias='sourceMap')

    @root_validator(pre=True)
    def annotation(cls, values: dict) -> dict:
        return values


class Meta(BaseModel):
    classes: list[str]
    title: Optional[str]


class Member(Node, element='member', node_class='user'):
    classes: list[str]
    key: str
    value: str

    @root_validator(pre=True)
    def member(cls, values: dict) -> dict:
        return values


class Copy(Node, element='copy'):
    content: str


class MemberNode(Node, element='member'):
    """
    a dataclass member
    """
    type_attributes: Optional[list[str]] = Field(alias='typeAttributes')
    description: Optional[str]
    key: str
    value: typing.Union[str, int, bool, 'ObjectNode', Any]

    @root_validator(pre=True)
    def member_node(cls, values):
        cls.update_forward_refs()
        return values

    @root_validator
    def member_node_post(cls, values):
        return values


class DataStructureNode(Node):
    # {'element': 'object', 'meta': {'id': 'Device'}, ...
    # we want to move the id meta.id element up
    id: Optional[str]

    @root_validator(pre=True)
    def id_from_meta(cls, values: dict) -> dict:
        meta = values.get('meta')
        if meta:
            id = meta.pop('id', None)
            if id:
                values['id'] = id
            # if id was only attribute then remove "meta"
            if not meta:
                values.pop('meta')
        return values


class ObjectNode(DataStructureNode, element='object'):
    members: Optional[list[MemberNode]] = Field(alias='member')

    @root_validator(pre=True)
    def object_node(cls, values):
        node_log.debug(f'{cls.__name__}.object_node: {values}')
        if (member := values.get('member')) is not None and not isinstance(member, list):
            node_log.error(f'{cls.__name__}: "member" is not a list: {member}')
        return values

    @root_validator
    def object_node_post(cls, values):
        return values


class Enumeration(BaseModel):
    # something like: {'element': 'string', 'attributes': {'typeAttributes': ['fixed']}, 'content': 'connected'}
    type: str = Field(alias='element')
    value: Optional[str] = Field(alias='content')
    attributes: Optional[list[str]]

    @root_validator(pre=True)
    def enumeration(cls, values: dict) -> dict:
        """
        pull typeAttributes up
        :param values:
        :return:
        """
        if 'attributes' not in values:
            return values
        attributes = values['attributes']
        type_attributes = attributes.pop('typeAttributes', [])
        values['attributes'] = simple_value(type_attributes)
        # also keep the other attributes
        values.update(attributes)
        return values

    @property
    def normalized_value(self) -> str:
        """
        Remove quotes from Enumerations like 'INACTIVE'
        """
        if m := re.match(r"^'(.+)'$", self.value):
            return m.group(1)
        return self.value


class EnumNode(DataStructureNode, element='enum'):
    enumerations: list[Enumeration]

    @root_validator(pre=True)
    def enum_node(cls, values: dict) -> dict:
        return values

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'


class DataStructure(Node, element='category'):
    objects: Optional[list[ObjectNode]] = Field(alias='object', default_factory=list)
    enums: Optional[list[EnumNode]] = Field(alias='enum', default_factory=list)

    @root_validator(pre=True)
    def data_structure(cls, values: dict) -> dict:
        # data has a bunch of "dataStructure" nodes. Each dataStructure node has single element content: object or euzm
        # we want to get rid of the datsStructure nodes and instead want list of nodes by element type under
        # dataStructure
        data_structure_sub_nodes = defaultdict(list)
        for data_structure_node in values.get('dataStructure', []):
            sub_node = data_structure_node['content']
            data_structure_sub_nodes[sub_node['element']].append(sub_node)
        values.pop('dataStructure', None)
        values.update(data_structure_sub_nodes)
        return values


class HrefVariable(Node, element='member'):
    description: Optional[str]
    title: Optional[str]
    type_attributes: list[str] = Field(alias='typeAttributes')
    key: str
    value: Any  # TODO: need to figure out what is possible here

    @root_validator(pre=True)
    def href_variable(cls, values):
        node_log.debug(f'{cls.__name__} pre: values: {values}')
        return values


class HttpRequest(Node, element='httpRequest'):
    method: str


class HttpResponse(Node, element='httpResponse'):
    status_code: Optional[int] = Field(alias='statusCode')
    data_structure: Optional[str] = Field(alias='dataStructure')

    @root_validator(pre=True)
    def http_response(cls, values):
        node_log.debug(f'{cls.__name__} pre: value: {values}')
        # 'dataStructure' can be the name of a dataStructure
        # 'dataStructure': {'element': 'dataStructure', 'content': {'element': 'Device Configuration Collection Response'}}
        data_structure = values.pop('dataStructure', None)
        if data_structure is not None:
            if set(data_structure) != {'element', 'content'}:
                raise ValueError(f'unexpected dataStructure(1): {data_structure}')
            content = data_structure['content']
            if set(content) != {'element'}:
                raise ValueError(f'unexpected dataStructure(2): {data_structure}')
            values['dataStructure'] = content['element']
        return values

    @root_validator(pre=False)
    def http_response_post(cls, values):
        node_log.debug(f'{cls.__name__} post: values: {values}')
        return values

    ...

class HttpTransaction(Node, element='httpTransaction'):

    http_request: HttpRequest = Field(alias='httpRequest')
    http_response: HttpResponse = Field(alias='httpResponse')

    @root_validator(pre=True)
    def http_transaction(cls, values):
        node_log.debug(f'{cls.__name__}: value: {values}')
        return values

    @root_validator(pre=False)
    def http_transaction_post(cls, values):
        node_log.debug(f'{cls.__name__}: value: {values}')
        return values


class Method(Node, element='transition'):
    href: Optional[str]
    title: str
    docstring: Optional[str] = Field(alias='copy')
    href_variables: Optional[list[HrefVariable]] = Field(alias='hrefVariables')
    http_transaction: HttpTransaction = Field(alias='httpTransaction')

    @root_validator(pre=True)
    def method(cls, values):
        try:
            values['hrefVariables'] = values['hrefVariables']['content']
        except KeyError:
            pass
        return values

    def __repr__(self):
        return f'{self.__class__.__name__}({self.title})'

    ...


class Resource(Node, element='resource'):
    href: str
    title: str
    methods: list[Method] = Field(alias='transition')
    ...


class MetaInfo(Node):
    classes: list[str]

    @root_validator(pre=True)
    def meta_info(cls, values):
        return values


class ResourceGroup(Node, element='category'):
    classes: list[str]
    title: Optional[str]
    resources: list[Resource] = Field(alias='resource')

    @root_validator(pre=True)
    def resource_group(cls, values: dict) -> dict:
        return values


class ApiSpec(Node, element='category', node_class='api'):
    docstring: Optional[str] = Field(alias='copy')
    data_structures: Optional[DataStructure] = Field(alias='dataStructures')
    resource_groups: Optional[list[ResourceGroup]] = Field(alias='resourceGroup')
    resource: Optional[list[Resource]]
    metadata: Optional[list[Member]]

    @root_validator(pre=True)
    def api_spec(cls, values: dict) -> dict:
        # each "category" entry has a class definition in the meta attribute like this:
        # {'element': 'category', 'meta': {'classes': {'element': 'array', 'content': [{'element': 'string',
        # 'content': 'resourceGroup'}]},
        categories = values.pop('category', [])
        categories_by_class = defaultdict(list)
        for category in categories:
            meta: MetaInfo = MetaInfo.parse_obj(category['meta'])
            category_class = meta.classes and len(meta.classes) == 1 and meta.classes[0]
            category_class = category_class or 'no_class'
            categories_by_class[category_class].append(category)
        ds = categories_by_class.get('dataStructures')
        if ds and len(ds) == 1:
            categories_by_class['dataStructures'] = ds[0]
        values.update(categories_by_class)
        return values


class ParseResult(Node, element='parseResult'):
    """
    The root parse results object
    """
    api: ApiSpec = Field(alias='category')
    annotation: Optional[list[Annotation]]



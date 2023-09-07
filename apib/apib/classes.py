import logging

from collections import defaultdict
from dataclasses import dataclass, field
from itertools import chain
from typing import Literal, Any, Optional, Union, ClassVar, Generator, NamedTuple

import dateutil.parser
from pydantic import BaseModel, Extra, validator, model_validator, Field, parse_obj_as, field_validator, TypeAdapter, \
    ValidationError

from apib.apib import is_element

__all__ = ['ApibParseResult', 'ApibElement', 'ApibCopy', 'ApibResource', 'ApibModel', 'ApibDatastucture',
           'ApibCategory', 'ApibAnnotation', 'ApibKeyValue', 'ApibWithCopy', 'ApibTransition', 'ApibMember',
           'ApibMeta', 'ApibArray', 'ApibString', 'ApibEnum', 'ApibEnumElement', 'ApibHttpHeaders',
           'ApibWithHeaders', 'ApibHrefMember', 'ApibHttpResponse', 'ApibHttpTransaction', 'ApibHttpRequest',
           'ApibBool', 'ApibApi', 'ApibHrefVariables', 'ApibNumber', 'ApibSourceMap', 'ApibSourceMapNumber',
           'AbibSourceMapNumberArray', 'ApibObject']

log = logging.getLogger(__name__)


def words_to_camel(s: str) -> str:
    return ''.join(w.lower().capitalize() for w in s.split())


def simple_python_type(t: str) -> str:
    if t == 'string':
        return 'str'
    elif t == 'number':
        return 'int'
    else:
        raise ValueError(f'unexpected simple type: {t}')


class ApibModel(BaseModel):
    class Config:
        extra = Extra.forbid


ApibKeyValue = Any


class ApibMeta(ApibModel):
    classes: Optional[list[str]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    id: Optional[str] = None

    @model_validator(mode='before')
    def val_root_meta(cls, data):
        log.debug(f'{data}')
        try:
            data = data.copy()
            if classes := data.get('classes'):
                # parse as 'array' of 'string' objects
                array = ApibArray.model_validate(classes, element='string')
                # .. and extract the values
                data['classes'] = [e.content for e in array.content]
                if len(data['classes']) != 1:
                    raise ValueError('foo')
            for str_field in ('title', 'description', 'id'):
                if str_value := data.get(str_field):
                    data[str_field] = ApibString.model_validate(str_value).content
        except Exception as e:
            log.error(f'val_root_meta: failed, {e}')
            raise
        return data

    @property
    def meta_class(self) -> Optional[str]:
        return (self.classes and (len(self.classes) == 1) and self.classes[0]) or None


class ElementInfo(NamedTuple):
    element: 'ApibElement'
    path: str
    data_path: list[Union['ApibElement', list['ApibElement']]]

    @property
    def elem_path(self) -> str:
        return '.'.join(e.element for e in self.data_path if not isinstance(e, list))

    @property
    def elem_path_extended(self) -> str:
        def components() -> Generator[str, None, None]:
            for e in self.data_path:
                if isinstance(e, list):
                    continue
                e: ApibElement
                to_yield = e.element
                if meta := e.meta:
                    addtl = '/'.join(s for s in (meta.id, meta.meta_class, meta.title) if s)
                    if addtl:
                        to_yield = f'{to_yield}({addtl})'
                yield to_yield

        return '.'.join(components())


class ApibElement(ApibModel):
    element: str
    content: Optional[Union[int, str, ApibKeyValue, 'ApibElement', list['ApibElement']]] = None
    attributes: Optional[dict[str, 'ApibElement']] = None
    meta: Optional[ApibMeta] = None

    #: if set to true then attributes are moved "up" and will show up as attributes of model
    has_attributes: ClassVar[bool] = False

    # registry for all subclasses which have a fixed element value (Literal)
    _element_registry: ClassVar[dict[str, dict[str, ApibModel]]] = defaultdict(dict)
    _allowed_content: ClassVar[set[str]] = None

    @classmethod
    def element_literal_value(cls) -> Optional[str]:
        """
        determine the Literal restriction value of the 'element' field .. if any
        """
        field_element = cls.model_fields['element']
        element_type = field_element.annotation
        # element_type = field_element.type_
        try:
            element_origin = element_type.__origin__
        except AttributeError:
            return None
        if element_origin is Literal:
            element_value = element_type.__args__[0]
            return element_value
        return None

    def __init_subclass__(cls, allowed_content: set[str] = None, override_element_type_for: str = None):
        super().__init_subclass__()
        return

    @classmethod
    def __pydantic_init_subclass__(cls, allowed_content: set[str] = None, override_element_type_for: str = None):
        """
        We want to keep track of all subclasses that have a fixed element value (Literal).
        This registry is used when deserializing 'element' objects to determine the class of childs in the 'content'
        attribute of that object.

        :param allowed_content: set of 'element' types which are allowed as 'content' items in this class
        :param override_element_type_for: some element types are used in multiple context. If a class with a given
        'element' type should override the standard class for an element type then this parameter is the 'element'
        type of the parent for which the override should be considered
        """
        cls._allowed_content = allowed_content
        # register this class
        # * either globally -> element type = '*'
        # * or as factory within a given context
        override_element_type_for = override_element_type_for or '*'
        element_value = cls.element_literal_value()
        if element_value is None:
            return
        # register this class
        # * either globally -> element type = '*'
        # * or as factory within a given context
        log.debug(f'{override_element_type_for}/{element_value}: {cls.__name__}')
        cls._element_registry[override_element_type_for][element_value] = cls
        return

    @classmethod
    def deserialize_element(cls, v: dict) -> Union[dict, 'ApibElement']:
        """
        Try to deserialize an object based on the value of 'element' as registered class or ApibEleemnt
        """
        if isinstance(v, dict) and (element := v.get('element')):
            if cls._allowed_content and element not in cls._allowed_content:
                raise ValueError(f"'{element}' not allowed as content for class {cls.__name__}")
            parent_element = cls.element_literal_value()
            element_cls = cls._element_registry[parent_element].get(element)
            if element_cls is None:
                element_cls = cls._element_registry['*'].get(element)
            if element_cls is None:
                log.debug(f'content element with unregistered "element": {element}')
                parsed = ApibElement.model_validate(v)
            else:
                parsed = element_cls.model_validate(v)
            return parsed
        return v

    @model_validator(mode='before')
    def val_root_element(cls, data):
        try:
            if cls.has_attributes:
                data = cls.move_attributes_up(data)
        except Exception as e:
            log.error(f'val_root_element failed: {e}')
            raise
        return data

    @field_validator('content', mode='before')
    def val_content_element(cls, content):
        """
        Content can be (among other options):
            * element
            * list of elements

        In these cases we try to deserialize based on the 'element' key that possibly identifies a specific
        ApibElement subclass
        """
        if is_element(content):
            content = cls.deserialize_element(content)
        elif isinstance(content, list):
            content = [cls.deserialize_element(item) for item in content]
        return content

    @field_validator('attributes', mode='before')
    def val_attributes(cls, attributes):
        """
        Validate as dict[str, 'ApibElement'] and try to deserialize values
        """
        if attributes:
            attributes = {k: cls.deserialize_element(v) for k, v in attributes.items()}
        return attributes

    @classmethod
    def move_attributes_up(cls, data: dict) -> dict:
        if not isinstance(data, dict) or data.get('attributes') is None:
            return data
        data = data.copy()
        data.update(data.pop('attributes'))
        return data

    def elements(self) -> Generator['ApibElement', None, None]:
        """
        All elememts
        """
        for e, _, _ in self.elements_with_path():
            yield e

    def elements_with_path(self, path: str = None,
                           elem_path: list['ApibElement'] = None) -> \
            Generator[ElementInfo, None, None]:
        """
        All elements
        """
        path = path or ''
        path = f'{path}({self.element})'
        elem_path = elem_path or list()
        yield ElementInfo(self, path, elem_path)
        # if isinstance(self.content, ApibElement):
        #     yield from self.content.elements()
        # elif isinstance(self.content, list):
        #     for element in self.content:
        #         yield from element.elements()
        elp_len = len(elem_path)
        elem_path.append(self)
        for k, v in self.__dict__.items():
            if isinstance(v, ApibElement):
                yield from v.elements_with_path(f'{path}.{k}', elem_path)
            if isinstance(v, list):
                elem_path.append(v)
                for i, e in enumerate(v):
                    if isinstance(e, ApibElement):
                        yield from e.elements_with_path(f'{path}.{k}[{i}]', elem_path)
                    else:
                        log.warning(f'content list member is not an ApibElement: {path}.{k}[{i}]: '
                                    f'{e.__class__.__name__} ')
                elem_path.pop()
        elem_path.pop()

        return

    def content_elements_by_type(self, content_element_type: str) -> Generator['ApibElement', None, None]:
        """
        Generator for all content elements of a given 'element' value
        """
        if isinstance(self.content, list):
            return (c for c in self.content
                    if isinstance(c, ApibElement) and c.element == content_element_type)
        return ()

    def find_content_by_element(self, content_element_type) -> Optional['ApibElement']:
        return next(self.content_elements_by_type(content_element_type), None)

    @property
    def description(self) -> Optional[str]:
        return self.meta and self.meta.description


class ApibString(ApibElement):
    element: Literal['string']
    content: Optional[str] = None

    @field_validator('content', mode='after')
    def content_string_val(cls, v):
        if isinstance(v, int):
            v = f'{v}'
        if not isinstance(v, str):
            raise ValueError('content has to be string.')
        return v


class ApibBool(ApibElement):
    element: Literal['boolean']
    content: Optional[bool] = None

    @field_validator('content', mode='after')
    def content_bool(cls, v):
        if v is not None:
            if not isinstance(v, int):
                raise ValueError('content has to be an int')
            v = (v == 1)
        return v


class ApibNumber(ApibElement):
    element: Literal['number']

    content: Optional[float] = None
    default: Optional[float] = None

    @model_validator(mode='before')
    def val_root_number(cls, v):
        """
        Root validator to parse default from attributes if present
        """
        if isinstance(v, dict) and (attrs := v.get('attributes')) and (default := attrs.get('default')):
            attrs = attrs.copy()
            attrs.pop('default')
            v = v.copy()
            if attrs:
                v['attributes'] = attrs
            else:
                v.pop('attributes')
            number = ApibNumber.model_validate(default)
            if any((number.attributes, number.meta, number.default)):
                raise ValueError(f'Unexpected attributes, meta, or default: {number}')
            v['default'] = number.content
        return v


class ApibSourceMapNumber(ApibNumber, override_element_type_for='sourceMapXYC'):
    has_attributes = True
    element: Literal['number']

    line: Optional[int] = None
    column: Optional[int] = None

    @field_validator('line', 'column', mode='before')
    def val_line_column(cls, v):
        v = ApibNumber.model_validate(v).content
        return v


class AbibSourceMapNumberArray(ApibElement, override_element_type_for='sourceMap'):
    element: Literal['array']
    content: list[ApibSourceMapNumber]

    @model_validator(mode='before')
    def val_root_sourcemap_number_array(cls, v):
        v = v.copy()
        v['content'] = TypeAdapter(list[ApibSourceMapNumber]).validate_python(v['content'])
        return v


class ApibSourceMapEntry(ApibModel):
    start: ApibSourceMapNumber
    end: ApibSourceMapNumber

    # @model_validator(mode='before')
    # def val_root_source_map_entry(cls, v):
    #     return v


class ApibSourceMap(ApibElement):
    element: Literal['sourceMap']
    content: list[ApibSourceMapEntry]

    @model_validator(mode='before')
    def val_root_sourcemap(cls, v):
        parsed_content = TypeAdapter(list[AbibSourceMapNumberArray]).validate_python(v['content'])
        v = v.copy()
        v['content'] = [{'start': pc.content[0], 'end': pc.content[1]} for pc in parsed_content]
        return v


class WithTypeAttributes(ApibElement):
    """
    Mixin to support 'typeAttributes' attribute
    """
    has_attributes = True
    type_attributes: set[str] = Field(alias='typeAttributes', default_factory=set)

    @field_validator('type_attributes', mode='before')
    def val_type_attributes(cls, v):
        """
        Type attributes are something like:
            {'content': [{'content': 'required', 'element': 'string'}], 'element': 'array'}
        :param v:
        :return:
        """
        v = ApibArray.model_validate(v, element='string')
        if any(s.meta or s.attributes for s in v.content):
            raise ValueError(f'Can\'t create set from list with non trivial strings: {v}')
        v = set(s.content for s in v.content)
        return v


class ApibEnumElement(ApibString, WithTypeAttributes, override_element_type_for='enum_elem'):
    """
    enumerations in 'enum' are 'strings' with typeAttributes
    """

    class Config:
        extra = Extra.allow
        # TODO: check for extra fields?? 'samples' seems to be a candidate

    @model_validator(mode='before')
    def val_root_enum(cls, data):
        # apparently a "*" in an enum is parsed as:
        #   {
        #     "element": "string",
        #     "attributes": {
        #       "samples": {
        #         "element": "array",
        #         "content": [
        #           {
        #             "element": "string"
        #           }
        #         ]
        #       }
        #     }
        #   }
        #
        # In that case we want to instead parse:
        #     {
        #     "element": "string",
        #     "attributes": {
        #       "typeAttributes": {
        #         "element": "array",
        #         "content": [
        #           {
        #             "element": "string",
        #             "content": "fixed"
        #           }
        #         ]
        #       }
        #     },
        #     "content": "*"
        #     },
        if not data.get('content'):
            if data.get('samples'):
                data = {
                    "element": "string",
                    "attributes": {
                        "typeAttributes": {
                            "element": "array",
                            "content": [
                                {
                                    "element": "string",
                                    "content": "fixed"
                                }
                            ]
                        }
                    },
                    "content": "*"
                }
            else:
                # apparently 'none' is parsed as None
                data = data.copy()
                data['content'] = 'none'

        return data


class ApibArray(ApibElement):
    element: Literal['array']

    @classmethod
    def model_validate(cls, data: Any, element: str = None) -> 'ApibArray':
        parsed = super().model_validate(data)
        parsed.content = parsed.content or list()
        if e := next((c for c in parsed.content if element and element != c.element), None):
            raise ValueError(f"Unexpected element '{e.element}', expected: {element}")
        return parsed


class ApibCopy(ApibElement):
    element: Literal['copy']
    content: str


class ApibMember(ApibElement):
    element: Literal['member']
    key: str
    value: ApibElement

    @property
    def as_dict(self) -> dict:
        return {self.key: self.value.content}

    @model_validator(mode='before')
    def val_root_member(cls, values):
        try:
            values = values.copy()
            values['key'] = ApibString.model_validate(values['content']['key']).content
            value = ApibElement.deserialize_element(values['content']['value'])
            values['value'] = value
            values.pop('content')
        except Exception as e:
            log.error(f'val_root_member failed: {e}')
            raise
        return values


class ApibHrefVariables(ApibElement):
    element: Literal['hrefVariables']
    content: list['ApibMember']


class ApibResource(ApibElement):
    element: Literal['resource']
    has_attributes = True
    href: Optional[str] = None
    href_variables: Optional[ApibHrefVariables] = Field(alias='hrefVariables', default=None)

    @field_validator('href', mode='before')
    def vaL_href(cls, v):
        v = ApibString.model_validate(v)
        return v.content


class ApibWithCopy(ApibElement):
    @field_validator('content', mode='after')
    def max_one_copy_in_content(cls, content):
        if isinstance(content, list):
            copy_elements = sum(isinstance(c, ApibCopy) for c in content)
            if copy_elements > 1:
                raise ValueError(f"Max one 'copy' element expected as content in {cls.__name__} ")
        return content

    @property
    def copy_content(self) -> Optional[str]:
        cc = next(self.content_elements_by_type(content_element_type='copy'), None)
        return (cc and cc.content) or None


class ApibCategory(ApibWithCopy,
                   allowed_content={'content', 'copy', 'resource', 'category', 'dataStructure'}):
    element: Literal['category']
    metadata: Optional[list[ApibMember]] = None
    content: list[ApibElement]

    has_attributes = True

    @field_validator('metadata', mode='before')
    def val_metadata(cls, data):
        # parse as Array ..
        data = ApibArray.model_validate(data, element='member')
        # .. and then actually return the parsed array
        return data.content


class Attribute(NamedTuple):
    """
    one datastructure attribute
    """
    name: str
    python_type: str
    docstring: str
    sample: Any
    referenced_class: str

    @classmethod
    def classes_and_attribute_from_member(cls, class_name: str, member: ApibMember) \
            -> tuple[list['PythonClass'], 'Attribute']:
        if member.element != 'member':
            log.warning(f'Not implemented, member element: {member.element}')
            return [], None
            # TODO: implement this case
        classes = []
        name = member.key
        value = member.value
        docstring = member.meta and member.meta.description
        referenced_class = None
        if value.element == 'string':
            sample = value.content
            # could be a datetime
            if sample is None:
                python_type = 'str'
            else:
                try:
                    dateutil.parser.parse(sample)
                    python_type = 'datetime'
                except (OverflowError, dateutil.parser.ParserError):
                    # probably a string
                    python_type = 'str'
        elif value.element == 'array':
            sample = None
            if not isinstance(value.content, list):
                raise ValueError('unexpected content for list')
            if not value.content:
                array_element_type = 'string'
            else:
                array_element_type = value.content[0].element
            if array_element_type == 'string':
                python_type = 'list[str]'
                sample = ", ".join(f"'{c.content}'" for c in value.content if c.content is not None)
                sample = sample and f'[{sample}]'
            else:
                # array of some type
                # references class is that type
                referenced_class = words_to_camel(array_element_type)
                # .. and the Python type is a list of that type
                python_type = f'list[{referenced_class}]'
        elif value.element == 'object':
            # we need a class with these attributes
            python_type = f'{class_name}{name[0].upper()}{name[1:]}'
            sample = None
            referenced_class = python_type
            new_classes, class_attributes = python_class_attributes(basename=referenced_class, members=value.content)
            classes.extend(new_classes)
            classes.append(PythonClass(name=referenced_class, attributes=class_attributes,
                                       description=value.description, is_enum=False, baseclass=None))
        elif value.element == 'number':
            # can be int or float
            if value.content is None:
                python_type = 'int'
            else:
                try:
                    int(value.content)
                    python_type = 'int'
                except ValueError:
                    python_type = 'float'
            sample = value.content
        elif value.element == 'enum':
            value: ApibEnum
            # we need an implicit enum class
            python_type = f'{class_name}{name[0].upper()}{name[1:]}'
            sample = value.content and value.content.content
            referenced_class = python_type
            class_attributes = [Attribute(name=e.content,python_type=simple_python_type(e.element),
                                           docstring=e.description,sample=None,referenced_class=None)
                                 for e in value.enumerations]
            classes.append(PythonClass(name=referenced_class, attributes=class_attributes,
                                       description=value.description, is_enum=True, baseclass=None))
        elif value.element == 'boolean':
            python_type = 'bool'
            sample = value.content
        else:
            # this might be a reference to a class
            python_type = words_to_camel(value.element)
            referenced_class = python_type
            try:
                sample = value.content and value.content.content
            except AttributeError:
                sample = None
        return classes, Attribute(name=name, python_type=python_type, docstring=docstring, sample=sample,
                                  referenced_class=referenced_class)


@dataclass
class PythonClass:
    """
    Information about a Python class
    """
    name: str
    attributes: list[Attribute] = field(default_factory=list)
    description: str = field(default=None)
    is_enum: bool = field(default=None)
    baseclass: str = field(default=None)


def python_class_attributes(basename: str, members: list['ApibMember']) -> tuple[list[PythonClass], list[Attribute]]:
    classes = []
    attributes = []
    if not members:
        return classes, attributes
    for member in members:
        new_classes, attribute = Attribute.classes_and_attribute_from_member(basename, member)
        classes.extend(new_classes)
        if attribute:
            attributes.append(attribute)
    return classes, attributes


class ApibDatastucture(ApibElement):
    element: Literal['dataStructure']

    content: ApibElement

    """
    A datastructure can have these childs
        * ApibEnum
        * ApibObject
        * ApibElement - the element value is the name of the super-class in this case, the content attribute of the 
                        child then has the list of addtl. attributes
    """

    @property
    def python_name(self) -> Optional[str]:
        if self.content and self.content.meta:
            return self.content.meta.id and words_to_camel(self.content.meta.id)
        return None

    @property
    def is_enum(self) -> bool:
        return self.content.element == 'enum'

    @property
    def is_class(self) -> bool:
        return not self.is_enum

    @property
    def baseclass(self) -> Optional[str]:
        el = self.content.element
        if el in {'object', 'enum'}:
            return None
        return words_to_camel(el)

    @property
    def referenced_classes(self) -> list[str]:
        if self.content.element == 'object':
            refs = self.content.meta and self.content.meta.id
            refs = refs and [words_to_camel(refs)] or list()
        else:
            refs = list()
        refs.append(a.referenced_class for a in self.class_attributes if a.referenced_class)
        return refs

    def python_classes(self) -> Generator[PythonClass, None, None]:
        """
        :return:
        """
        # content can be 'object' or 'enum'
        content = self.content
        content_element = content and content.element
        python_name = self.python_name
        baseclass = self.baseclass
        if not content_element:
            raise ValueError('content element should not be None')
        elif content_element == 'object':
            content: ApibObject
            # get attributes from object content
            classes, attributes = python_class_attributes(basename=self.python_name,
                                                          members=content.content)
            yield from classes
            yield PythonClass(name=python_name, attributes=attributes, description=None, is_enum=False,
                              baseclass=baseclass)

        elif content_element == 'enum':
            content: ApibEnum
            attributes = [Attribute(name=e.content, python_type=simple_python_type(e.element),
                                    docstring=e.description, sample=None, referenced_class=None)
                          for e in content.enumerations]
            yield PythonClass(name=python_name, attributes=attributes, is_enum=True)
        else:
            classes, attributes = python_class_attributes(basename=self.python_name,
                                                          members=content.content)
            yield from classes
            yield PythonClass(name=python_name, attributes=attributes, description=None, is_enum=False,
                              baseclass=baseclass)

    @property
    def class_attributes(self) -> list[Attribute]:
        if not self.is_class:
            return
        if self.superclass:
            members = self.content.content
        else:
            members = self.content.content
        r = list()
        if not members:
            return r
        for member in members:
            r.append(Attribute.from_member(self.python_name, member))
        return r


class ApibHrefMember(ApibElement, override_element_type_for='transition'):
    element: Literal['member']
    type_attributes: set[str] = Field(alias='typeAttributes')

    key: str
    value: Optional[Union[str, ApibElement]] = None

    has_attributes = True

    @model_validator(mode='before')
    def val_root_member(cls, data):
        try:
            data = data.copy()
            content = data.get('content')
            if content is None:
                raise ValueError(f'missing content in {cls.__name__}')
            # content should be a dict with key, value
            if set(content) != {'key', 'value'}:
                raise ValueError(f'Unexpected keys in content for {cls.__name__}: {sorted(set(content))}')

            key = ApibString.model_validate(content['key']).content
            if not isinstance(key, str):
                raise ValueError(f'key is not a string: {type(key)}')
            data['key'] = key
            value = ApibElement.deserialize_element(content['value'])
            if isinstance(value, ApibString):
                value = value.content
            if value is not None:
                data['value'] = value
            data.pop('content')
        except Exception as e:
            log.error(f'val_root_member failed: {e}')
            raise

        return data

    @field_validator('type_attributes', mode='before')
    def val_type_attributes(cls, v):
        """
        Type attributes are something like:
            {'content': [{'content': 'required', 'element': 'string'}], 'element': 'array'}
        :param v:
        :return:
        """
        v = ApibArray.model_validate(v, element='string')
        if any(s.meta or s.attributes for s in v.content):
            raise ValueError(f'Can\'t create set from list with non trivial strings: {v}')
        v = set(s.content for s in v.content)
        return v


class ApibObject(WithTypeAttributes):
    element: Literal['object']

    @model_validator(mode='after')
    def val_root_object(cls, o: 'ApibObject'):
        if o.type_attributes and o.type_attributes != {'fixedType'}:
            raise ValidationError(f'unexpected type attributes: {o.type_attributes}')
        return o


class ApibTransition(ApibElement, allowed_content={'copy', 'httpTransaction'}):
    element: Literal['transition']
    href: Optional[str] = None
    href_variables: list[ApibHrefMember] = Field(alias='hrefVariables', default_factory=list)
    data: Optional[ApibDatastucture] = None

    has_attributes = True

    @field_validator('href', mode='before')
    def val_href(cls, v):
        """
        href is an ApibString
        :param v:
        :return:
        """
        v = ApibString.model_validate(v)
        return v.content

    @field_validator('href_variables', mode='before')
    def val_href_variables(cls, v):
        if (element := v.get('element')) != 'hrefVariables':
            raise ValueError(f"unexpected 'element' value for hrefVariables: '{element}'")
        v = TypeAdapter(list[ApibHrefMember]).validate_python(v['content'])
        return v

    @property
    def title(self) -> Optional[str]:
        return (self.meta and self.meta.title) or None


class ApibApi(ApibCategory, override_element_type_for='parseResult'):
    meta: ApibMeta

    @property
    def host(self) -> Optional[str]:
        if not self.metadata:
            return None
        member = next((m for m in self.metadata
                       if m.key == 'HOST'), None)
        return member and member.value.content or None

    @property
    def doc_string(self) -> Optional[str]:
        """
        String that can be used as docstring
        """
        return self.copy_content

    def data_structures(self) -> Generator[ApibDatastucture, None, None]:
        """
        All datastructures defined in this API
        """
        # data structures live in a category element in the content
        return chain.from_iterable(c.content for c in self.content if isinstance(c, ApibCategory)
                                   and c.meta.meta_class == 'dataStructures')

    def transitions(self) -> Generator[ApibTransition, None, None]:
        return chain.from_iterable(c.content for c in self.content if isinstance(c, ApibResource))

    @model_validator(mode='after')
    def val_is_api(cls, api: 'ApibApi'):
        # verify that this really an api definition by looking for 'api' in meta.classes
        if api.meta.meta_class != 'api':
            raise ValueError('not an api')
        return api


class ApibAnnotation(ApibElement):
    has_attributes = True
    element: Literal['annotation']

    content: str
    code: int
    source_map: list[ApibSourceMap] = Field(alias='sourceMap')

    @field_validator('code', mode='before')
    def val_code(cls, v):
        parsed = ApibNumber.model_validate(v)
        if parsed.attributes or parsed.meta:
            raise ValueError(f'unexpected attributes or meta for {cls.__name__}.code')
        return parsed.content

    @field_validator('source_map', mode='before')
    def val_source_map(cls, v):
        parsed = ApibArray.model_validate(v)
        return parsed.content


class ApibHttpHeaders(ApibElement, allowed_content={'member'}):
    element: Literal['httpHeaders']
    content: list[ApibMember]


class ApibWithHeaders(ApibElement):
    has_attributes = True
    headers: Optional[dict[str, str]] = None

    @field_validator('headers', mode='before')
    def val_headers(cls, data):
        """
        This is a 'httpHeaders' element. Content of which is a list of "member" items with key/value content
        :param data:
        :return:
        """
        parsed = ApibHttpHeaders.model_validate(data)
        parsed: ApibHttpHeaders
        e = next((member for member in parsed.content
                  if not isinstance(member, ApibMember) or not member.key or \
                  not isinstance(member.value, ApibString)),
                 None)
        if e:
            raise ValueError(f'Unexpected member for http header: {e}')
        result = {member.key: member.value.content for member in parsed.content}
        return result


class ApibHttpRequest(ApibWithHeaders):
    element: Literal['httpRequest']

    method: str

    @model_validator(mode='before')
    def val_root_http_request(cls, data):
        try:
            data = cls.move_attributes_up(data)
            data = data.copy()
            data['method'] = ApibString.model_validate(data['method']).content
        except Exception as e:
            log.error(f'val_root_http_request failed: {e}')
            raise
        return data


class ApibHttpResponse(ApibWithHeaders):
    element: Literal['httpResponse']
    has_attributes = True

    status_code: Optional[int] = Field(alias='statusCode', default=None)

    @model_validator(mode='before')
    def val_root_http_response(cls, data):
        try:
            data = cls.move_attributes_up(data)
            status_code = data.get('statusCode')
            if status_code is not None:
                data = data.copy()
                data['statusCode'] = int(ApibString.model_validate(status_code).content)
        except Exception as e:
            log.error(f'val_root_http_response failed: {e}')
            raise
        return data

    @property
    def message_body_schema(self) -> Optional[str]:
        message_body_schema_element = next((el for el in self.content_elements_by_type('asset')
                                            if el.meta and el.meta.meta_class == 'messageBodySchema'), None)
        return message_body_schema_element and message_body_schema_element.content

    @property
    def message_body(self) -> Optional[str]:
        message_body_element = next((el for el in self.content_elements_by_type('asset')
                                     if el.meta and el.meta.meta_class == 'messageBody'),
                                    None)
        return message_body_element and message_body_element.content

    @property
    def datastructure(self) -> Optional[ApibDatastucture]:
        return next((el for el in self.content if isinstance(el, ApibDatastucture)), None)


class ApibHttpTransaction(ApibElement):
    element: Literal['httpTransaction']

    @property
    def request(self) -> Optional[ApibHttpRequest]:
        return self.find_content_by_element('httpRequest')

    @property
    def response(self) -> Optional[ApibHttpRequest]:
        return self.find_content_by_element('httpResponse')


class ApibEnum(ApibElement):
    has_attributes = True
    element: Literal['enum']
    content: Optional[ApibString] = None

    # Some enumerations have type attributes?
    enumerations: Optional[list[ApibEnumElement]] = None
    default: Optional[ApibString] = None

    @property
    def enum_values(self) -> list[str]:
        return [e.content for e in self.enumerations]

    @model_validator(mode='before')
    def val_root_enum(cls, data):
        try:
            data = cls.move_attributes_up(data)
            default = data.get('default')
            enumerations = data.get('enumerations')
            if default or enumerations:
                data = data.copy()
            if default:
                parsed_default = ApibElement.model_validate(default)
                if parsed_default.element != 'enum':
                    raise ValueError(f'"enum" element expected for default; got {parsed_default.element}')
                if not isinstance(parsed_default.content, ApibString):
                    raise ValueError(f'Did not get "string" element for default: {default}')
                data['default'] = parsed_default.content
            if enumerations:
                parsed_list = TypeAdapter(list[ApibEnumElement]).validate_python(enumerations['content'])
                if parsed_list and not (le := parsed_list[-1]).content:
                    if le.attributes or le.meta:
                        raise ValueError()
                    fields = set(le.__dict__)
                    unexpected_fields = fields - {'attributes', 'content', 'element', 'meta', 'type_attributes'}
                    if unexpected_fields:
                        raise ValueError()
                    # remove the empty final element
                    parsed_list = parsed_list[:-1]
                data['enumerations'] = parsed_list
        except Exception as e:
            log.error(f'val_root_enum failed: {e}')
            raise

        return data

    @model_validator(mode='after')
    def val_root_enum_post(cls, data):
        return data


class ApibParseResult(ApibElement, allowed_content={'category', 'annotation'}):
    element: Literal['parseResult']

    @property
    def api(self) -> ApibApi:
        return next(c for c in self.content if isinstance(c, ApibApi))

    @model_validator(mode='after')
    def val_root_parse_result(cls, parse_result: 'ApibParseResult'):
        # make sure we have exactly one 'category' element
        try:
            content = parse_result.content
            if content:
                content: list[ApibElement]
                if sum(v.element == 'category' for v in content) != 1:
                    raise ValueError('Exactly one \'category\' element expected')
        except Exception as e:
            log.error(f'val_root_parse_result failed: {e}')
            raise
        return parse_result

    @classmethod
    def model_validate(cls, *args, **kwargs) -> 'ApibParseResult':
        return super().model_validate(*args, **kwargs)

    def python_classes(self) -> Generator[PythonClass, None, None]:
        """
        All Python classes (implicit and explict)
        """
        for ds in self.api.data_structures():
            yield from ds.python_classes()
            ...

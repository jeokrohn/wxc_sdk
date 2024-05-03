import logging
from collections import defaultdict
from itertools import chain
from typing import Literal, Any, Optional, Union, ClassVar, Generator, NamedTuple

from pydantic import BaseModel, Extra, model_validator, Field, field_validator, TypeAdapter, \
    ValidationError

from apib.apib import is_element

__all__ = ['ApibParseResult', 'ApibElement', 'ApibCopy', 'ApibResource', 'ApibModel', 'ApibDatastructure',
           'ApibCategory', 'ApibAnnotation', 'ApibKeyValue', 'ApibWithCopy', 'ApibTransition', 'ApibMember',
           'ApibMeta', 'ApibArray', 'ApibString', 'ApibEnum', 'ApibEnumElement', 'ApibHttpHeaders',
           'ApibWithHeaders', 'ApibHttpResponse', 'ApibHttpTransaction', 'ApibHttpRequest',
           'ApibBool', 'ApibApi', 'ApibHrefVariables', 'ApibNumber', 'ApibSourceMap', 'ApibSourceMapNumber',
           'AbibSourceMapNumberArray', 'ApibObject', 'ApibSourceMapEntry', 'ApibOption',
           'ApibSelect']

from apib.tools import words_to_camel

log = logging.getLogger(__name__)


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
                    addtl = '/'.join(s for s in (meta.id, meta.meta_class, meta.title, meta.description) if s)
                    if addtl:
                        to_yield = f'{to_yield}({addtl})'
                yield to_yield

        return '.'.join(components())


class ApibElement(ApibModel):
    element: str
    content: Optional[Union[int, str, bool, float, ApibKeyValue, 'ApibElement', list['ApibElement']]] = None
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
            try:
                if element_cls is None:
                    log.debug(f'content element with unregistered "element": {element}')
                    parsed = ApibElement.model_validate(v)
                else:
                    parsed = element_cls.model_validate(v)
            except ValidationError as e:
                log.error(f'validation error cls {cls.__new__()}, {element_cls.__name__}: {e}')
                raise e
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

    def find_content_by_element(self, content_element_type: str) -> Optional['ApibElement']:
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
    type_attributes: set[str] = Field(alias='typeAttributes', default_factory=set)

    @model_validator(mode='before')
    def val_root_type_attributes(cls, values):
        if values is None:
            return None
        values = values.copy()
        # try to pull typeAttributes
        if (attributes := values.get('attributes')) and (typeAttributes := attributes.pop('typeAttributes', None)):
            values['typeAttributes'] = typeAttributes
            if not attributes:
                values.pop('attributes')
            else:
                log.warning(f'{cls.__name__} with unconsumed attributes: {", ".join(attributes)}')
        return values

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
        if 'content' not in data:
            foo = 1
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


class ApibMember(WithTypeAttributes):
    element: Literal['member']
    key: str
    value: Optional[Union[str, ApibElement]] = None

    @property
    def as_dict(self) -> dict:
        return {self.key: self.value.content}

    @model_validator(mode='before')
    def val_root_member(cls, data):
        if not isinstance(data, dict):
            return
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
            # if isinstance(value, ApibString):
            #     value = value.content
            if value is not None:
                data['value'] = value
            data.pop('content')

        except Exception as e:
            log.error(f'val_root_member failed: {e}')
            raise

        return data


class ApibOption(ApibElement):
    element: Literal['option']
    content: ApibMember

    @model_validator(mode='before')
    def root_val_option(cls, values):
        # content should be a single element list
        if not (content := values.get('content')) or not isinstance(content, list) or len(content) != 1:
            raise ValueError(f'content should be single element list: {content}')
        values = values.copy()
        values['content'] = content[0]
        return values

    @property
    def option_text(self) -> Optional[str]:
        return self.content.meta and self.content.meta.description

    @property
    def value(self) -> Union[Any]:
        return self.content.value.content


class ApibSelect(ApibElement):
    element: Literal['select']
    content: list[ApibOption]

    @model_validator(mode='after')
    def val_root_select(cls, data: 'ApibSelect'):
        option_keys = set(option.content.key for option in data.content)
        if len(option_keys) != 1:
            raise ValueError(f'only expected one value in all options. Got: {", ".join(sorted(option_keys))}')
        return data

    @property
    def option_key(self) -> str:
        return self.content[0].content.key


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


class ApibDatastructure(ApibElement):
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
    def class_name(self) -> Optional[str]:
        """
        DS name to be used for class registry. No transformation is applied. The name is used as is for PythonClass
        instantiation. The normalization to proper Python names (and de-duplication) only happens later
        """
        if self.content and self.content.meta and (name := self.content.meta.id):
            return name
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
        return el

    @property
    def referenced_classes(self) -> list[str]:
        if self.content.element == 'object':
            refs = self.content.meta and self.content.meta.id
            refs = refs and [words_to_camel(refs)] or list()
        else:
            refs = list()
        refs.append(a.referenced_class for a in self.class_attributes if a.referenced_class)
        return refs


class ApibObject(WithTypeAttributes):
    element: Literal['object']

    # TODO: Why is this union needed? Looks likes sometimes there is a 'select' child element?
    content: list[Union[ApibMember, ApibSelect]] = Field(default_factory=list)

    @model_validator(mode='after')
    def val_root_object(cls, o: 'ApibObject'):
        if o.type_attributes and o.type_attributes != {'fixedType'}:
            raise ValidationError(f'unexpected type attributes: {o.type_attributes}')
        return o


class ApibTransition(ApibElement, allowed_content={'copy', 'httpTransaction'}):
    element: Literal['transition']
    href: Optional[str] = None
    href_variables: list[ApibMember] = Field(alias='hrefVariables', default_factory=list)
    data: Optional[ApibDatastructure] = None

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
        v = TypeAdapter(list[ApibMember]).validate_python(v['content'])
        return v

    @property
    def title(self) -> Optional[str]:
        return (self.meta and self.meta.title) or None

    @property
    def docstring(self) -> Optional[str]:
        copy_element = self.find_content_by_element('copy')
        return copy_element and copy_element.content

    @property
    def http_transaction(self) -> 'ApibHttpTransaction':
        return self.find_content_by_element('httpTransaction')


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

    def data_structures(self) -> Generator[ApibDatastructure, None, None]:
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
    def datastructure(self) -> Optional[ApibDatastructure]:
        return next((el for el in self.content if isinstance(el, ApibDatastructure)), None)


class ApibHttpTransaction(ApibElement):
    element: Literal['httpTransaction']

    @property
    def request(self) -> Optional[ApibHttpRequest]:
        return self.find_content_by_element('httpRequest')

    @property
    def response(self) -> Optional[ApibHttpResponse]:
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
                """ drafter seems to sometimes create a superfluous empty element at the end of an enumeration
                    "element": "enum",
                    "attributes": {
                      "enumerations": {
                        "element": "array",
                        "content": [
                          {
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
                            "content": "none"
                          },
                          {
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
                            "content": "submitted"
                          },
                          ...
                          {
                            "element": "string"
                          }
                        ]
                      }
                    }
                In that case we throw away the last element
                """
                enumerations_content = enumerations['content']
                if enumerations_content[-1] == {'element': 'string'}:
                    enumerations_content = enumerations_content[:-1]
                parsed_list = TypeAdapter(list[ApibEnumElement]).validate_python(enumerations_content)
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

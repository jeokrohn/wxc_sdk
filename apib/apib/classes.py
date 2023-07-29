import logging
from collections import defaultdict
from typing import Literal, Any, Optional, Union, ClassVar, Generator

from pydantic import BaseModel, Extra, validator, root_validator, Field, parse_obj_as

from private.apib.apib import is_element

__all__ = ['ApibParseResult', 'ApibElement', 'ApibCopy', 'ApibResource', 'ApibModel', 'ApibDatastucture',
           'ApibCategory', 'ApibAnnotation', 'ApibKeyValue', 'ApibWithCopy', 'ApibTransition', 'ApibMember',
           'ApibMeta', 'ApibArray', 'ApibString', 'ApibEnum', 'ApibEnumElement', 'ApibHttpHeaders',
           'ApibWithHeaders', 'ApibHrefMember', 'ApibHttpResponse', 'ApibHttpTransaction', 'ApibHttpRequest']

log = logging.getLogger(__name__)


class ApibModel(BaseModel):
    class Config:
        extra = Extra.forbid


ApibKeyValue = Any


class ApibMeta(ApibModel):
    classes: Optional[list[str]]
    title: Optional[str]
    description: Optional[str]
    id: Optional[str]

    @root_validator(pre=True)
    def val_root_meta(cls, data):
        try:
            data = data.copy()
            if classes := data.get('classes'):
                # parse as 'array' of 'string' objects
                array = ApibArray.parse_obj(classes, element='string')
                # .. and extract the values
                data['classes'] = [e.content for e in array.content]
                if len(data['classes']) != 1:
                    raise ValueError('foo')
            for str_field in ('title', 'description', 'id'):
                if str_value := data.get(str_field):
                    data[str_field] = ApibString.parse_obj(str_value).content
        except Exception as e:
            log.error(f'val_root_meta: failed, {e}')
            raise
        return data

    @property
    def meta_class(self) -> Optional[str]:
        return (self.classes and (len(self.classes) == 1) and self.classes[0]) or None


class ApibElement(ApibModel):
    element: str
    content: Optional[Union[int, str, ApibKeyValue, 'ApibElement', list['ApibElement']]]
    attributes: Optional[dict]
    meta: Optional[ApibMeta]

    has_attributes: ClassVar[bool] = False

    # registry for all subclasses which have a fixed element value (Literal)
    _element_registry: ClassVar[dict[str, dict[str, ApibModel]]] = defaultdict(dict)
    _allowed_content: ClassVar[set[str]] = None

    @classmethod
    def element_literal_value(cls) -> Optional[str]:
        """
        determine the Literal restriction value of the 'element' field .. if any
        """
        field_element = cls.__fields__['element']
        element_type = field_element.type_
        try:
            element_origin = element_type.__origin__
        except AttributeError:
            return None
        if element_origin is Literal:
            element_value = element_type.__args__[0]
            return element_value
        return None

    @classmethod
    def __init_subclass__(cls, allowed_content: set[str] = None, override_element_type_for: str = None):
        """
        We want to keep track of all subclasses that have a fixed element value (Literal).
        This registry is used when deserializing 'element' objects to determine the class of childs in the 'content'
        attribute of that object.

        :param allowed_content: set of 'element' types which are allowed as 'content' items in this class
        :param override_element_type_for: some element types are used in multiple context. If a class with a given
        'element' type should overrides the standard class for an element type then this parameter is the 'element'
        type of the parent for which the override should be considered
        """
        cls._allowed_content = allowed_content
        element_value = cls.element_literal_value()
        if element_value is None:
            return
        # register this class
        # * either globally -> element type = '*'
        # * or as factory within a given context
        override_element_type_for = override_element_type_for or '*'
        cls._element_registry[override_element_type_for][element_value] = cls
        return

    @classmethod
    def deserialize_element(cls, v: dict) -> Union[dict, 'ApibElement']:
        """
        Try to deserialize an object based on the value of 'element' as registered class or ApibEleemnt
        """
        if element := v.get('element'):
            if cls._allowed_content and element not in cls._allowed_content:
                raise ValueError(f"'{element}' not allowed as content for class {cls.__name__}")
            parent_element = cls.element_literal_value()
            element_cls = cls._element_registry[parent_element].get(element)
            if element_cls is None:
                element_cls = cls._element_registry['*'].get(element)
            if element_cls is None:
                log.debug(f'content element with unregistered "element": {element}')
                parsed = ApibElement.parse_obj(v)
            else:
                parsed = element_cls.parse_obj(v)
            return parsed
        return v

    @root_validator(pre=True)
    def vaL_root_element(cls, data):
        try:
            if cls.has_attributes:
                data = cls.move_attributes_up(data)
        except Exception as e:
            log.error(f'vaL_root_element failed: {e}')
            raise
        return data

    @validator('content', pre=True)
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

    @classmethod
    def move_attributes_up(cls, data: dict) -> dict:
        if (attributes := data.get('attributes')) is None:
            return data
        data = data.copy()
        data.pop('attributes')
        for k, v in attributes.items():
            data[k] = v
        return data

    def elements(self) -> Generator['ApibElement', None, None]:
        """
        All elememts
        """
        for e, _, _ in self.elements_with_path():
            yield e

    def elements_with_path(self, path:str=None,
                           elem_path: list['ApibElement'] = None) -> Generator[
        tuple['ApibElement', str, list['ApibElement']], None, None]:
        """
        All elememts
        """
        path = path or ''
        path = f'{path}({self.element})'
        elem_path = elem_path or list()
        yield self, path, elem_path
        # if isinstance(self.content, ApibElement):
        #     yield from self.content.elements()
        # elif isinstance(self.content, list):
        #     for element in self.content:
        #         yield from element.elements()
        elp_len = len(elem_path)
        elem_path.append(self)
        for k,v in self.__dict__.items():
            if isinstance(v, ApibElement):
                yield from v.elements_with_path(f'{path}.{k}', elem_path)
            if isinstance(v, list):
                elem_path.append(v)
                for i, e in enumerate(v):
                    if isinstance(e, ApibElement):
                        yield from e.elements_with_path(f'{path}.{k}[{i}]', elem_path)
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


class ApibString(ApibElement):
    element: Literal['string']

    @validator('content', pre=False)
    def content_string_val(cls, v):
        if isinstance(v, int):
            v = f'{v}'
        if not isinstance(v, str):
            raise ValueError('content has to be string.')
        return v
class WithTypeAttributes(ApibElement):
    """
    Mixin to support 'typeAttributes' attribute
    """
    has_attributes = True
    type_attributes: set[str] = Field(alias='typeAttributes', default_factory=set)

    @validator('type_attributes', pre=True)
    def val_type_attributes(cls, v):
        """
        Type attributes are something like:
            {'content': [{'content': 'required', 'element': 'string'}], 'element': 'array'}
        :param v:
        :return:
        """
        v = ApibArray.parse_obj(v, element='string')
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
class ApibArray(ApibElement):
    element: Literal['array']

    @classmethod
    def parse_obj(cls, data: Any, element: str = None) -> 'ApibArray':
        parsed = super().parse_obj(data)
        parsed.content = parsed.content or list()
        if e := next((c for c in parsed.content if element and element != c.element), None):
            raise ValueError(f"Unexpected element '{e.element}', expected: {element}")
        return parsed


class ApibCopy(ApibElement):
    element: Literal['copy']


class ApibResource(ApibElement):
    element: Literal['resource']


class ApibWithCopy(ApibElement):
    @validator('content', pre=False)
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


class ApibMember(ApibElement):
    element: Literal['member']
    key: str
    value: ApibElement

    @root_validator(pre=True)
    def vaL_root_member(cls, values):
        try:
            values = values.copy()
            values['key'] = ApibString.parse_obj(values['content']['key']).content
            value = ApibElement.deserialize_element(values['content']['value'])
            values['value'] = value
            values.pop('content')
        except Exception as e:
            log.error(f'vaL_root_member failed: {e}')
            raise
        return values


class ApibCategory(ApibWithCopy,
                   allowed_content={'content', 'copy', 'resource', 'category', 'dataStructure'}):
    element: Literal['category']
    metadata: Optional[list[ApibMember]]

    has_attributes = True

    @validator('metadata', pre=True)
    def val_metadata(cls, data):
        # parse as Array ..
        data = ApibArray.parse_obj(data, element='member')
        # .. and then actually return the parsed array
        return data.content

    @property
    def doc_string(self) -> Optional[str]:
        """
        String that can be used as docstring 
        """
        return self.copy_content

    @property
    def host(self) -> Optional[str]:
        if not self.metadata:
            return None
        member = next((m for m in self.metadata
                       if m.key == 'HOST'), None)
        return member and member.value.content or None


class ApibAnnotation(ApibElement):
    element: Literal['annotation']


class ApibHrefMember(ApibElement, override_element_type_for='transition'):
    element: Literal['member']
    type_attributes: set[str] = Field(alias='typeAttributes')

    key: str
    value: Optional[Union[str, ApibElement]]

    has_attributes = True

    @root_validator(pre=True)
    def val_root_member(cls, data):
        try:
            content = data.get('content')
            if content is None:
                raise ValueError(f'missing content in {cls.__name__}')
            # content should be a dict with key, value
            if set(content) != {'key', 'value'}:
                raise ValueError(f'Unexpected keys in content for {cls.__name__}: {sorted(set(content))}')

            key = ApibString.parse_obj(content['key']).content
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

    @validator('type_attributes', pre=True)
    def val_type_attributes(cls, v):
        """
        Type attributes are something like:
            {'content': [{'content': 'required', 'element': 'string'}], 'element': 'array'}
        :param v:
        :return:
        """
        v = ApibArray.parse_obj(v, element='string')
        if any(s.meta or s.attributes for s in v.content):
            raise ValueError(f'Can\'t create set from list with non trivial strings: {v}')
        v = set(s.content for s in v.content)
        return v


class ApibDatastucture(ApibElement):
    element: Literal['dataStructure']
    @property
    def ds_id(self)->Optional[str]:
        return (self.content and self.content.meta and self.content.meta.id) or None


class ApibTransition(ApibElement, allowed_content={'copy', 'httpTransaction'}):
    element: Literal['transition']
    href: Optional[str]
    href_variables: list[ApibHrefMember] = Field(alias='hrefVariables', default_factory=list)
    data: Optional[ApibDatastucture]

    has_attributes = True

    @validator('href', pre=True)
    def val_href(cls, v):
        """
        href is an ApibString
        :param v:
        :return:
        """
        v = ApibString.parse_obj(v)
        return v.content

    @validator('href_variables', pre=True)
    def val_href_variables(cls, v):
        if (element := v.get('element')) != 'hrefVariables':
            raise ValueError(f"unexpected 'element' value for hrefVariables: '{element}'")
        v = parse_obj_as(list[ApibHrefMember], v['content'])
        return v

    @property
    def title(self) -> Optional[str]:
        return (self.meta and self.meta.title) or None


class ApibHttpHeaders(ApibElement, allowed_content={'member'}):
    element: Literal['httpHeaders']
    content: list[ApibMember]


class ApibWithHeaders(ApibElement):
    has_attributes = True
    headers: Optional[dict[str, str]]

    @validator('headers', pre=True)
    def vaL_headers(cls, data):
        """
        This is a 'httpHeaders' element. Content of which is a list of "memeber" items with key/value content
        :param data:
        :return:
        """
        parsed = ApibHttpHeaders.parse_obj(data)
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

    @root_validator(pre=True)
    def val_root_http_request(cls, data):
        try:
            data = data.copy()
            data['method'] = ApibString.parse_obj(data['method']).content
        except Exception as e:
            log.error(f'val_root_http_request failed: {e}')
            raise
        return data


class ApibHttpResponse(ApibWithHeaders):
    element: Literal['httpResponse']
    has_attributes = True

    status_code: Optional[int] = Field(alias='statusCode')

    @root_validator(pre=True)
    def val_root_http_response(cls, data):
        try:
            status_code = data.get('statusCode')
            if status_code is not None:
                data = data.copy()
                data['statusCode'] = int(ApibString.parse_obj(status_code).content)
        except Exception as e:
            log.error(f'val_root_http_response failed: {e}')
            raise
        return data


class ApibHttpTransaction(ApibElement):
    element: Literal['httpTransaction']


class ApibEnum(ApibElement):
    has_attributes = True
    element: Literal['enum']
    content: Optional[ApibString]

    # Some enumerations have type attributes?
    enumerations: list[ApibEnumElement]
    default: Optional[ApibString]

    @property
    def enum_values(self)->list[str]:
        return [e.content for e in self.enumerations.content]

    @root_validator(pre=True)
    def val_root_enum(cls, data):
        try:
            default = data.get('default')
            enumerations = data.get('enumerations')
            if default or enumerations:
                data.copy()
            if default:
                parsed_default = ApibElement.parse_obj(default)
                if parsed_default.element != 'enum':
                    raise ValueError(f'"enum" element expected for default; got {parsed_default.element}')
                if not isinstance(parsed_default.content, ApibString):
                    raise ValueError(f'Did not get "string" element for default: {default}')
                data['default'] = parsed_default.content
            if enumerations:
                parsed_list = parse_obj_as(list[ApibEnumElement], enumerations['content'])
                if parsed_list and not (le:=parsed_list[-1]).content:
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

    @root_validator(pre=False)
    def val_root_enum_post(cls, data):
        return data
class ApibParseResult(ApibElement, allowed_content={'category', 'annotation'}):
    element: Literal['parseResult']

    @property
    def category(self) -> ApibCategory:
        return next(c for c in self.content if isinstance(c, ApibCategory))

    @property
    def annotations(self) -> list[ApibAnnotation, None, None]:
        return [c for c in self.content if isinstance(c, ApibAnnotation)]

    @root_validator(pre=False)
    def val_root_parse_result(cls, values):
        # make sure we have exactly one 'category' element
        try:
            content = values.get('content')
            if content:
                content: list[ApibElement]
                if sum(v.element == 'category' for v in content) != 1:
                    raise ValueError('Exactly one \'category\' element expected')
        except Exception as e:
            log.error(f'val_root_parse_result failed: {e}')
            raise
        return values


def test_root_validator():
    class Root(BaseModel):
        content: Any

        @root_validator(pre=True)
        def val_root(cls, data):
            print(f'{cls.__name__}.Root.val_root: {data}')
            return data

        @validator('content', pre=False)
        def val_content_root(cls, v):
            print(f'{cls.__name__}.Root.val_content_root: {v}')
            return v

    class Derived(Root):
        @root_validator(pre=True)
        def val_root_derived(cls, data):
            # data = super().val_root(data)
            print(f'{cls.__name__}.Derived.val_root_d: {data}')
            return data

        @validator('content', pre=False)
        def val_content_derived(cls, v):
            print(f'{cls.__name__}.Derived.val_content_derived: {v}')
            return v

    data = {'content': 'fghjk'}
    parsed = Derived.parse_obj(data)
    print(parsed)


if __name__ == '__main__':
    test_root_validator()

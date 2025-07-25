import logging
import re
from collections import Counter
from collections.abc import Generator, Iterable, Callable
from dataclasses import dataclass, field
from io import StringIO
from itertools import chain
from os.path import commonprefix
from re import subn, sub
from typing import Any, Optional, Union, Type
from urllib.parse import urljoin

import dateutil.parser
from pydantic import TypeAdapter

from apib.apib import ApibEnum
from apib.apib.classes import ApibApi
from apib.tools import break_line, snake_case, words_to_camel, \
    remove_html_comments, remove_div, lines_for_docstring, simple_python_type
from wxc_sdk.base import to_camel, ApiModel

__all__ = ['PythonClass', 'Attribute', 'Endpoint', 'Parameter', 'PythonAPI']

log = logging.getLogger(__name__)

# add description to class sources?
CLASSES_WITH_DESCRIPTION = False

# some Python names are not allowed as parameter names
RESERVED_PARAM_NAMES = {'from', 'to', 'max', 'format', 'global', 'none', 'in'}

CLASS_TEMPLATE = """
class {class_name}{baseclass}:
{desc}{attributes}
"""

DESC_TEMPLATE = '''    """
{docstring}
    """
'''


@dataclass
class Parameter:
    """
    One Parameter
    """
    name: str
    python_type: str
    referenced_class: Optional[str]
    docstring: str
    sample: Any
    optional: bool
    # true -> parameter is parameter in URL
    url_parameter: bool = field(default=False)
    registry: 'PythonClassRegistry' = field(default=None)

    @property
    def python_name(self) -> str:
        """
        A Python compatible name. Reserved Python names are suffixed with an underscore
            from -> from_
        """
        if self.name in RESERVED_PARAM_NAMES:
            return f'{self.name}_'
        return snake_case(self.name)

    @property
    def is_enum(self) -> bool:
        """
        Is the parameter an enum?
        Parameter is an enum if the class type is an enum class
        """
        if not self.referenced_class or self.referenced_class != self.python_type:
            return False
        python_class = self.registry.get(self.python_type)
        return python_class.is_enum

    def source_for_arg_list(self, class_names: set[str]) -> str:
        """
        representation of parameter in argument list in def

        :param class_names: set of names of referenced classes
        """
        python_type = self.python_type
        if python_type == 'datetime':
            python_type = 'Union[str, datetime]'
        arg = f'{self.python_name}:&{python_type}'
        if self.optional:
            arg = f'{arg}&=&None'
        if self.referenced_class:
            class_names.add(self.referenced_class)
        return arg

    def source_for_docstring(self) -> Generator[str, None, None]:
        """
        Lines for docstring something like:
            :param person_id: List authorizations for this user id.
            :type person_id: str
        """
        source = StringIO()
        # param lines:
        ' * 1st line has ":param <xyc>: '
        ' * following lines just have docstring lines'
        yield from lines_for_docstring(docstring=self.docstring,
                                       text_prefix_for_1st_line=f':param {self.python_name}: ',
                                       indent=4,
                                       indent_first_line=0,
                                       width=112)
        # for datetime: str or datetime
        python_type = self.python_type
        if python_type == 'datetime':
            python_type = 'Union[str, datetime]'
        yield f':type {self.python_name}: {python_type}'

    def source_for_param_init(self) -> Iterable[str]:
        """
        Python code for initialization of 'param' variable
        """
        lines = []
        # something like
        #   params['<name>'] = <python_name>
        # for datetime and bool some special treatment is required
        if self.python_type == 'bool':
            # str(<python
            python_val = f'str({self.python_name}).lower()'
        elif self.python_type == 'list[str]':
            python_val = f"','.join({self.python_name})"
        elif self.is_enum:
            # body['{name}'] = enum_str({python_name})
            python_val = f"enum_str({self.python_name})"
        else:
            if self.python_type == 'datetime':
                # datetime parameters in URLs are something like:
                #   2018-01-01T13:12:11.789Z
                lines.append(f"""if isinstance({self.python_name}, str):""")
                lines.append(f"""    {self.python_name} = isoparse({self.python_name})""")
                lines.append(f"""{self.python_name} = dt_iso_str({self.python_name})""")
            python_val = f'{self.python_name}'
        lines.append(f"params['{self.name}'] = {python_val}")
        if self.optional:
            lines = chain([f'if {self.python_name} is not None:'],
                          (f'    {l}' for l in lines))
        return lines

    def source_for_body_init(self) -> Generator[str, None, None]:
        """
        Python code for body init
        """
        if self.optional:
            yield f'if {self.python_name} is not None:'
            indent = ' ' * 4
        else:
            indent = ''
        # most simple form:
        if not self.referenced_class:
            # most simple form
            # body['{name}'] = {python_name}
            yield f"{indent}body['{self.name}'] = {self.python_name}"
            return
        if self.is_enum:
            # body['{name}'] = enum_str({python_name})
            yield f"{indent}body['{self.name}'] = enum_str({self.python_name})"
            return
        if self.python_type == self.referenced_class:
            # body['{name}'] = {python_name}.model_dump(mode='json', by_alias=True, exclude_none=True)
            yield (f"{indent}body['{self.name}'] = {self.python_name}.model_dump(mode='json', "
                   f"by_alias=True, exclude_none=True)")
            return
        yield (f"{indent}body['{self.name}'] = TypeAdapter({self.python_type}).dump_python({self.python_name}, "
               f"mode='json', by_alias=True, exclude_none=True)")


class SourceIO(StringIO):
    def __init__(self):
        self.prefix = ' ' * 8
        super().__init__()

    def print(self, l: str = None):
        if l:
            print(f'{self.prefix}{l}', file=self)
        else:
            print(file=self)


@dataclass
class Endpoint:
    # python name for the method
    name: str
    # title for docstring
    title: str
    # text for docstring
    docstring: str = field(repr=False)
    # HTTP method
    method: str = field(default=None)
    # the host. Something like 'https://webexapis.com/v1/'
    host: str = field(default=None)
    # the url. Something like 'people/{personId}/features/bargeIn'
    url: str = field(default=None)
    # list of parameters, each can be a URL parameter or a query parameter
    href_parameter: list[Parameter] = field(default_factory=list, repr=False)
    # class name for body content if present ...
    body_class_name: str = field(default=None, repr=False)
    # ... or list of parameters to be sent in the body
    body_parameter: list[Parameter] = field(default_factory=list, repr=False)
    # python type for result
    result: str = field(default=None, repr=False)
    # references class if python result type is a class or references a class, e.g. list[SomeObject]
    result_referenced_class: str = field(default=None, repr=False)
    # example response body
    response_body: str = field(default=None)
    registry: 'PythonClassRegistry' = field(default=None, repr=False)

    @property
    def full_url(self) -> str:
        return urljoin(self.host, self.url)

    @property
    def paginated(self) -> Optional['Attribute']:
        """
        determine whether the method requires pagination. Returns body list attribute or None

        requires pagination if:
          * 1st attribute returned is an array of something
          * has "max" query parameters
        """
        pag_parameters = {'max'}
        pagination_parameters = set(p.name
                                    for p in self.href_parameter
                                    if p.name in pag_parameters)
        if pagination_parameters != pag_parameters:
            return None
        if self.result_referenced_class and self.result == self.result_referenced_class:
            # paginated methods have something like 'EnterpriseListResponse' as result
            result_class = self.registry.get(self.result_referenced_class)
            # 1st attribute should be a list
            result_attribute = result_class.attributes[0]
            if result_attribute.python_type.startswith('list['):
                return result_attribute
            log.warning(f'endpoint "{self.name}" has "max" parameter, but 1st result attribute is not a list')
        return None

    @property
    def returns_list(self) -> Optional[str]:
        """
        if endpoint is a 'list' endpoint return the base datatype of the list
        """
        if self.method != 'GET':
            return None

        def attribute_list_base(a: Attribute) -> Optional[str]:
            if a.referenced_class:
                return a.referenced_class
            m = re.match(r'list\[(\S+)]', a.python_type)
            return m and m.group(1)

        if pa := self.paginated:
            return attribute_list_base(pa)

        if sa := self.single_result_attribute:
            return attribute_list_base(sa)

        if self.result and self.result.startswith('list['):
            if self.result_referenced_class:
                return self.result_referenced_class
            m = re.match(r'list\[(\S+)]', self.result)
            return m and m.group(1)
        return None

    def href_parameters_filtered(self) -> Iterable[Parameter]:
        """
        Href parameter, filtered for paginated methods if needed
        """
        if self.paginated:
            # remove max, offset, and start if "max" is there
            if next((p for p in self.href_parameter if p.name == 'max'), None):
                p_filter = {'max', 'offset', 'start'}
            else:
                p_filter = set()
        else:
            p_filter = set()
        return (p for p in self.href_parameter if p.name not in p_filter)

    def parameters_for_args(self) -> Generator[Parameter, None, None]:
        """
        Generator for parameters in order required for method arguments
        """
        # order
        #   * mandatory parameters; href before body
        #   * optional parameters; href before body w/o orgId
        #   * orgId if present
        yield from (p for p in chain(self.href_parameters_filtered(),
                                     self.body_parameter)
                    if not p.optional)
        org_id = None
        for p in chain(self.href_parameters_filtered(),
                       self.body_parameter):
            if not p.optional:
                # skip mandatory parameters; already covered
                continue
            if p.name == 'orgId':
                # skip orgId parameter ... for now
                org_id = p
                continue
            yield p
        # out orgId parameter to the end
        if org_id:
            yield org_id

    @property
    def params_required(self) -> bool:
        # do we need to pass 'params'?
        return self.paginated or any((not p.url_parameter for p in self.href_parameters_filtered()))

    @property
    def single_result_attribute(self) -> Optional['Attribute']:
        """
        Check if the result is an object with only one attribute. Then we take that attribute as the result
        """
        if self.result_referenced_class and self.result_referenced_class == self.result:
            result_class = self.registry.get(self.result)
            if len(result_class.attributes) == 1:
                return result_class.attributes[0]
        return None

    def source_def_line(self, source: SourceIO, class_names: set[str]):
        """
        Write Python source for def line to source

        :param source: generated source code
        :param class_names: set of names of referenced classes
        """
        # generate def line
        # in the prepared def line use "&" instead of " " for spaces where we don't want to break the line
        def_line = f'def {self.name}('

        # this is by how much we need to indent parameters starting with the 2nd line
        def_lines_prefix = ' ' * (4 + len(def_line))

        # comma separated list of all parameters
        param_line = ', '.join(chain(['self'],
                                     (parameter.source_for_arg_list(class_names=class_names)
                                      for parameter in self.parameters_for_args())))

        # for methods with pagination we want to add a **params parameter
        if paginated := self.paginated:
            # this is something like 'list[AuditEvent]'
            result_type = paginated.python_type
            m = re.match(r'^list\[(\w+)]$', result_type)
            if m is None:
                raise ValueError(f'Can\'t extract paginated result from "{result_type}"')
            result_type = m.group(1)
            if paginated.referenced_class:
                class_names.add(paginated.referenced_class)
            param_line = f'{param_line}, **params)&->&Generator[{result_type},&None,&None]'
        else:
            param_line = f'{param_line})'
            if self.result:
                if sra := self.single_result_attribute:
                    r_type = sra.python_type
                    if sra.referenced_class:
                        class_names.add(sra.referenced_class)
                else:
                    r_type = self.result
                    if self.result_referenced_class:
                        class_names.add(self.result_referenced_class)
                param_line = f'{param_line}&->&{r_type}'

        # now write def with parameters to string
        def_line = f'{def_line}{param_line}:'

        # add lines to source and remove the "&" placeholders
        for line in break_line(def_line, prefix=def_lines_prefix, prefix_first_line=' ' * 4):
            print(line.replace('&', ' '),
                  file=source)

    def source_docstring(self, source: SourceIO):
        """
        Write Python source for the docstring after the def line
        """
        # now to the docstring
        source.print(f'"""')
        if self.title:
            # suppress title if title is repeated in 1st line of docstring.
            skip_title = False
            first_docstring_line = self.docstring and next(l for l in self.docstring.splitlines())
            if first_docstring_line:
                first_docstring_line = first_docstring_line.strip('.')
                if self.title.lower() == first_docstring_line.lower():
                    skip_title = True
            if not skip_title:
                source.print(f'{self.title}')
                print(file=source)
        if self.docstring:
            for line in lines_for_docstring(docstring=self.docstring,
                                            width=112):
                source.print(line)
            source.print()
        # parameter docstrings
        for parameter in self.parameters_for_args():
            # print all docstring lines for parameter
            list(map(source.print, parameter.source_for_docstring()))
        # also add a return: line
        if paginated := self.paginated:
            if not paginated.referenced_class:
                list(map(source.print, lines_for_docstring(docstring=paginated.docstring,
                                                           text_prefix_for_1st_line=':return: ',
                                                           indent=4,
                                                           indent_first_line=0,
                                                           width=112)))
            else:
                source.print(f':return: Generator yielding :class:`{paginated.referenced_class}` instances')
        else:
            if sra := self.single_result_attribute:
                source.print(f':rtype: {sra.python_type}')
            elif self.result_referenced_class and self.result_referenced_class == self.result:
                source.print(f':rtype: :class:`{self.result_referenced_class}`')
            else:
                source.print(f':rtype: {self.result}')
        source.print(f'"""')

    def body_validator(self, module) -> Callable[[dict], Any]:
        """
        Get a callable that can validate the body of the response
        """

        def get_module_class(class_name: str) -> Type[ApiModel]:
            model = getattr(module, class_name, None)
            if model is None:
                raise ValueError(f'Failed to find class "{class_name}" in module')
            return model

        def validate(data: dict) -> Any:
            return validator(getter(data))

        getter = lambda x: x
        if pa := self.paginated:
            model = get_module_class(pa.referenced_class)
            model = TypeAdapter(list[model])
            getter = lambda x: x[pa.name]
            validator = model.validate_python
            return validate
        if self.result != self.result_referenced_class:
            # complex return type -> need to use TypeAdapter
            for_ta = self.result.replace(self.result_referenced_class,
                                         f"module.{self.result_referenced_class}")
            ta = eval(f'TypeAdapter({for_ta})')
            validator = ta.validate_python
        else:
            # simple return type
            if not (sra := self.single_result_attribute):
                # not a single result attribute -> need to deserialize for result
                model = get_module_class(self.result)
                validator = model.model_validate
            else:
                # single result attribute->instead of deserializing the result type we take the value of the
                # attribute and deserialize that .. if needed
                getter = lambda x: x[sra.name]
                if not sra.referenced_class:
                    # no need to parse anything, just pick the return value from the data
                    validator = lambda x: x
                else:
                    # single result attribute is not a simple Python type -> we need deserialization
                    if sra.referenced_class == sra.python_type:
                        model = get_module_class(sra.python_type)
                        if not issubclass(model, ApiModel):
                            validator = model
                        else:
                            validator = model.model_validate
                    else:
                        python_type = sra.python_type.replace(sra.referenced_class,
                                                              f"module.{sra.referenced_class}")
                        try:
                            ta = eval(f"TypeAdapter({python_type})")
                        except NameError as e:
                            raise ValueError(f'Failed to find class "{sra.referenced_class}" in module') from e
                        validator = ta.validate_python
                    # if .. else ..
                # if .. else ..
            # if .. else ..
        # if .. else ..

        return validate

    def source_call_and_return(self, source: SourceIO):
        """
        Python source for calling the method and returning the result
        """
        if pa := self.paginated:
            # return self.session.follow_pagination(url=ep, model=Person, params=params)
            call_line = f"return self.session.follow_pagination(url=url, model={pa.referenced_class}, item_key='" \
                        f"{pa.name}'"
            if self.params_required:
                call_line = f'{call_line}, params=params'
            if self.body_parameter:
                call_line = f'{call_line}, json=body'
            call_line = f'{call_line})'
            source.print(call_line)
        else:
            if self.result:
                call_line = 'data = '
            else:
                call_line = ''
            # need to call a method and parse a result
            call_line = f'{call_line}super().{self.method.lower()}(url'
            if self.params_required:
                call_line = f'{call_line}, params=params'
            if self.body_parameter:
                call_line = f'{call_line}, json=body'
            call_line = f'{call_line})'
            source.print(call_line)

            # parse result
            if self.result:
                if self.result != self.result_referenced_class:
                    # complex return type -> need to use TypeAdapter
                    source.print(f'r = TypeAdapter({self.result}).validate_python(data)')
                else:
                    # simple return type
                    if not (sra := self.single_result_attribute):
                        # not a single result attribute -> need to deserialize for result
                        source.print(f'r = {self.result}.model_validate(data)')
                    else:
                        # single result attribute->instead of deserializing the result type we take the value of the
                        # attribute and deserialize that .. if needed
                        if not sra.referenced_class:
                            # no need to parse anything, just pick the return value from the data
                            source.print(f"r = data['{sra.name}']")
                        else:
                            # single result attribute is not a simple Python type -> we need deserialization
                            if sra.referenced_class == sra.python_type:
                                source.print(f"r = {sra.python_type}.model_validate(data['{sra.name}'])")
                            else:
                                source.print(f"r = TypeAdapter({sra.python_type}).validate_python(data['{sra.name}'])")
                source.print(f'return r')

    def source(self, base: str, class_names: set[str]) -> str:
        """
        Create Python source for endpoint under some class

        :param base: base URL, common URL for all endpoints
        :param class_names: set of names of referenced classes
        """
        source = SourceIO()
        self.source_def_line(source, class_names=class_names)

        self.source_docstring(source)

        # code to prepare params (only href params which are not URL params
        if self.params_required:
            if not self.paginated:
                # methods with pagination have a **params argument
                source.print('params = {}')
            for p in self.href_parameters_filtered():
                if p.url_parameter:
                    continue
                # add all lines for param initialization to source
                list(map(source.print, p.source_for_param_init()))

        # prepare body
        if self.body_parameter:
            source.print('body = dict()')
            for p in self.body_parameter:
                list(map(source.print, p.source_for_body_init()))

        # code to determine URL (make sure to set URL parameters)
        # we only need the part of the endpoint URL after the common base URL
        url = self.url[len(base):].strip('/')
        if any(p.url_parameter for p in self.href_parameter):
            # generate Python code that uses an f-string to determine the URL
            # for that we have to replace href parameter names in URL with python names
            # 'locations/{locationId}/dectNetworks'  --> url = self.ep(f'locations/{location_id}/dectNetworks')
            for p in self.href_parameter:
                if not p.url_parameter:
                    continue
                url = url.replace(f'{{{p.name}}}', f'{{{p.python_name}}}')
            url = f"f'{url}'"
        else:
            if url:
                url = f"'{url}'"
        url_line = f"url = self.ep({url})"
        source.print(url_line)

        # call the method
        self.source_call_and_return(source)

        # return the final code
        full_code = source.getvalue()
        return full_code


@dataclass
class Attribute:
    """
    one datastructure attribute
    """
    name: str
    python_type: str
    docstring: Optional[str] = None
    sample: Optional[Any] = None
    referenced_class: Optional[str] = None
    optional: bool = field(default=False)

    def __post_init__(self):
        if (self.sample and isinstance(self.sample, str) and self.sample.lower() in {'true', 'false'} and
                self.python_type != 'bool'):
            log.warning(f'attribute "{self.name}" has sample value `{self.sample}` but is a {self.python_type} '
                        f'instead of a bool')
            self.sample = self.sample == 'true'
            self.python_type = 'bool'
            self.referenced_class = None
            log.warning(f'attribute "{self.name}" has been converted to a bool')

    @classmethod
    def from_enum(cls, enum_element: ApibEnum) -> Generator['Attribute', None, None]:
        """
        Generator for attributes from an ApibEnum
        """
        for e in enum_element.enumerations:
            yield Attribute(name=e.content, python_type=simple_python_type(e.element),
                            docstring=e.description, sample=None, referenced_class=None)

    @property
    def name_for_source(self)->str:
        name_map = {'*': 'star',
                    '#': 'hash'}

        attr_name = self.name.strip('"')
        attr_name = attr_name.strip("'")

        if mapped_name := name_map.get(attr_name):
            # replace special characters with a Python compatible name
            attr_name = mapped_name
        attr_name = snake_case(attr_name)

        # reserved Python names are not allowed as attribute names
        if attr_name in RESERVED_PARAM_NAMES:
            attr_name = f'{attr_name}_'
        return attr_name

    def source(self, for_enum: bool, with_example: bool = True) -> str:
        """
        Python source for one class attribute
        """
        # docstring before attribute looks something like this and is indented by 4 spaces
        #   #: The display name of the organization.
        if self.docstring:
            # break docstring lines to 80 characters
            lines = [f'#: {line}' for line in lines_for_docstring(self.docstring, width=113)]
        else:
            lines = []
        if for_enum:
            # something like:
            #   wav = 'WAV'
            if self.name is not None:
                name = self.name_for_source

                if name != 'none' or True:
                    # skip creation of 'none' attribute for enums; this is most probably meant to refer to the actual Null
                    # value
                    # replace all non-alphanumeric characters with '_'
                    name, _ = subn(r'[^a-z0-9]', '_', name)
                    # if the name starts with a digit then prefix it with 'd'
                    name = sub('^([0-9])', 'd\\1', name)
                    value = self.name
                    value = value.replace("'", '')
                    lines.append(f"{name} = '{value}'")
                # if
        else:
            # something like:
            #   actor_org_name: Optional[str] = None
            attr_name = self.name_for_source

            if with_example and self.sample:
                lines.append(f'#: example: {self.sample}')

            # something like
            #   target_name: Optional[str]
            line = f'{attr_name}: Optional[{self.python_type}]'

            if to_camel(attr_name) == self.name:
                # something like:
                #   target_name: Optional[str] = None
                line = f'{line} = None'
            else:
                # something like:
                #   users_in_ci: Optional[int] = Field(alias='usersInCI', default=None)
                line = f"{line} = Field(alias='{self.name}', default=None)"
            lines.append(line)
        return '\n'.join(lines)


@dataclass
class PythonClass:
    """
    Information about a Python class
    """
    name: str
    attributes: Optional[list[Attribute]] = field(default_factory=list)
    description: Optional[str] = None
    is_enum: bool = field(default=None)
    baseclass: Optional[str] = None
    # used for the case where a class is basically something like list[SomeOtherClass]
    alias: Optional[Attribute] = None

    def __post_init__(self):
        if not self.attributes and not self.alias:
            raise ValueError(f'class {self.name} has no attributes nor alias')
        if not self.attributes:
            return
        # attribute names need to be unique
        names = Counter(attr.name for attr in self.attributes)

        not_unique = [name for name, c in names.items() if c > 1]
        if not_unique:
            raise KeyError(f'class {self.name} has duplicate attributes: {", ".join(not_unique)}')

    def source(self, with_example: bool = True) -> Optional[str]:
        """
        Source code for this class or None
        """
        if self.baseclass and not self.attributes:
            return None
        if self.alias:
            return None
        if self.is_enum:
            baseclass = 'str, Enum'
        else:
            baseclass = self.baseclass or 'ApiModel'
        baseclass = baseclass and f'({baseclass})'
        if not self.attributes:
            attribute_sources = ('...',)
        else:
            attribute_sources = chain.from_iterable(map(str.splitlines,
                                                        (f'{a.source(self.is_enum, with_example)}'
                                                         for a in self.attributes)))
        if not (self.description and CLASSES_WITH_DESCRIPTION):
            desc_source = ''
        else:
            # break description into lines
            desc_source = '\n'.join(chain.from_iterable(break_line(line, prefix=' ' * 4)
                                                        for line in self.description.splitlines()))
            desc_source = DESC_TEMPLATE.format(docstring=desc_source)
        result = CLASS_TEMPLATE.format(class_name=self.name,
                                       baseclass=baseclass,
                                       desc=desc_source,
                                       attributes='\n'.join(f'    {line}' for line in attribute_sources)).strip()
        return result


@dataclass
class PythonAPI:
    """
    One API with multiple Endpoints
    """
    title: str
    docstring: str
    host: str

    class_template = '''class {class_name}(ApiChild, base='{base}'):
    """
{docstring}
    """
'''

    endpoints: list[Endpoint] = field(repr=False, default_factory=list)

    def add_endpoint(self, ep: Endpoint):
        self.endpoints.append(ep)

    def __post_init__(self):
        # clean up docstring
        # docstring = remove_links(self.docstring)
        # docstring = html2text(docstring)
        self.docstring = self.docstring and self.docstring.strip()

    @classmethod
    def from_apib_api(cls, apib_api: ApibApi) -> 'PythonAPI':
        docstring = apib_api.doc_string
        title = apib_api.meta.title
        host = apib_api.host
        return PythonAPI(docstring=docstring, title=title, host=host)

    @property
    def cleaned_doc_string(self) -> str:
        """
        docstring w/o stuff like:
            <!-- feature-toggle-name:wxc-cpapi-receptionist-72075 -->

            <div><Callout type="warning">Not supported for Webex for Government (FedRAMP)</Callout></div>
        """
        return self.docstring and remove_div(remove_html_comments(self.docstring)) or ''

    def source(self, *, class_name: str = None, class_names: set[str]) -> str:
        """
        Generate API source for given class name. If class name is not given, then class name is derived from API
        title.
        While generating sources collect name sof classes actually referenced by endpoints
        """
        class_name = class_name or f'{words_to_camel(self.title)}Api'
        # add API class name to referenced classes
        class_names.add(class_name)

        base = commonprefix([f'{ep.url}/' for ep in self.endpoints])
        # base cannot have url parameters
        # --> cut base if there is a url parameter in there
        match_before_parameter = re.match(r'(.+?/)\{', base)
        if match_before_parameter:
            base = match_before_parameter.group(1)
        # remove everything after the last '/'
        base = re.sub(r'/\w*$', '', base)
        doc_lines = chain([self.title, ''], self.cleaned_doc_string.splitlines())
        docstring = '\n'.join(chain.from_iterable(break_line(line, prefix=' ' * 4) for line in doc_lines))
        class_head = self.class_template.format(class_name=class_name,
                                                base=base.lstrip('/'),
                                                docstring=docstring)

        # full API source is head followed by source for each endpoint
        full_api_source = '\n'.join(s
                                    for s in chain([class_head],
                                                   (ep.source(base=base, class_names=class_names)
                                                    for ep in self.endpoints))
                                    if s)
        return full_api_source


def guess_datetime_or_int(sample: Optional[str], type_hint: Optional[str]) -> tuple[Optional[Union[str, int]], str]:
    """
    Guess type of sample and return tuple:
        * sample value
        * Python type: datetime, str, or int

    Only assume datetime if the sample doesn't parse as int
    """
    if sample is None:
        return sample, 'str'

    # is it a datetime?
    try:
        dateutil.parser.parse(sample)
        python_type = 'datetime'
    except (OverflowError, dateutil.parser.ParserError, TypeError):
        # probably a string
        return sample, 'str'
    except Exception as e:
        raise NotImplementedError(f'Unexpected error when trying to parse a string: {e}')

    # only assume datetime if sample doesn't parse as int
    try:
        sample = int(sample)
    except ValueError:
        pass
    else:
        if type_hint == 'string':
            return str(sample), 'str'
        return sample, 'int'
    return sample, python_type



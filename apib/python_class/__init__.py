import logging
import re
from collections import defaultdict
from collections.abc import Generator, Iterable
from dataclasses import dataclass, field
from functools import partial
from io import StringIO
from itertools import chain
from operator import attrgetter
from os.path import commonprefix
from re import subn, sub
from typing import Any, Optional, Union
from urllib.parse import urljoin

import dateutil.parser

from apib.apib import ApibDatastructure, ApibObject, ApibEnum, ApibParseResult, ApibMember
from apib.apib.classes import ApibElement, ApibSelect, ApibString, ApibBool, ApibNumber, ApibArray, ApibApi
from apib.tools import break_line, sanitize_class_name, snake_case, words_to_camel, \
    remove_html_comments, remove_div, lines_for_docstring
from wxc_sdk.base import to_camel

__all__ = ['PythonClass', 'PythonClassRegistry', 'Attribute', 'Endpoint', 'Parameter', 'simple_python_type']

log = logging.getLogger(__name__)

# some Python names are not allowed as parameter names
RESERVED_PARAM_NAMES = {'from', 'to', 'max'}

CLASS_TEMPLATE = """
class {class_name}{baseclass}:
{attributes}
"""


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

    def for_arg_list(self) -> str:
        """
        representation of parameter in argument list in def
        """
        python_type = self.python_type
        if python_type == 'datetime':
            python_type = 'Union[str, datetime]'
        arg = f'{self.python_name}:&{python_type}'
        if self.optional:
            arg = f'{arg}&=&None'
        return arg

    def for_docstring(self) -> Generator[str, None, None]:
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

    def for_param_init(self) -> Iterable[str]:
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

    def for_body_init(self) -> str:
        """
        Python code for body init
        """
        # most simple form:
        if not self.referenced_class:
            # most simple form
            # body['{name}'] = {python_name}
            return f"body['{self.name}'] = {self.python_name}"
        if self.is_enum:
            # body['{name}'] = enum_str({python_name})
            return f"body['{self.name}'] = enum_str({self.python_name})"
        if self.python_type == self.referenced_class:
            return f"body['{self.name}'] = loads({self.python_name}.model_dump_json())"
        return f"body['{self.name}'] = loads(TypeAdapter({self.python_type}).dump_json({self.python_name}))"


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

    def href_parameters_filtered(self) -> Iterable[Parameter]:
        """
        Href parameter, filtered for paginated methods if needed
        """
        if self.paginated:
            p_filter = {'max', 'offset'}
        else:
            p_filter = set()
        return (p for p in self.href_parameter if p.name not in p_filter)

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

    def source_def_line(self, source: SourceIO):
        """
        Write Python source for def line to source
        """
        # generate def line
        # in the prepared def line use "&" instead of " " for spaces where we don't want to break the line
        def_line = f'def {self.name}('

        # this is by how much we need to indent parameters starting with the 2nd line
        def_lines_prefix = ' ' * (4 + len(def_line))

        # comma separated list of all parameters
        param_line = ', '.join(chain(['self'],
                                     # optional parameters, href 1st
                                     (parameter.for_arg_list()
                                      for parameter in chain(self.href_parameters_filtered(),
                                                             self.body_parameter)
                                      if not parameter.optional),
                                     # mandatory parameters, href 1st
                                     (parameter.for_arg_list()
                                      for parameter in chain(self.href_parameters_filtered(),
                                                             self.body_parameter)
                                      if parameter.optional)))

        # for methods with pagination we want to add a **params parameter
        if paginated := self.paginated:
            # this is something like 'list[AuditEvent]'
            result_type = paginated.python_type
            m = re.match(r'^list\[(\w+)]$', result_type)
            if m is None:
                raise ValueError(f'Can\'t extract paginated result from "{result_type}"')
            result_type = m.group(1)
            param_line = f'{param_line}, **params)&->&Generator[{result_type},&None,&None]'
        else:
            param_line = f'{param_line})'
            if self.result:
                if sra := self.single_result_attribute:
                    r_type = sra.python_type
                else:
                    r_type = self.result
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
            source.print(f'{self.title}')
            print(file=source)
        if self.docstring:
            for line in lines_for_docstring(docstring=self.docstring,
                                            width=112):
                source.print(line)
            source.print()
        # parameter docstrings
        for parameter in chain((p for p in chain(self.href_parameters_filtered(),
                                                 self.body_parameter)
                                if not p.optional),
                               (p for p in chain(self.href_parameters_filtered(),
                                                 self.body_parameter)
                                if p.optional)):
            # print all docstring lines for parameter
            list(map(source.print, parameter.for_docstring()))
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

    def source(self, base: str) -> str:
        """
        Create Python source for endpoint under some class
        """
        source = SourceIO()

        self.source_def_line(source)

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
                list(map(source.print, p.for_param_init()))

        # prepare body
        if self.body_parameter:
            source.print('body = dict()')
            for p in self.body_parameter:
                source.print(p.for_body_init())

        # code to determine URL (make sure to set URL parameters)
        url = self.url[len(base):].strip('/')
        if any(p.url_parameter for p in self.href_parameter):
            # massage url parameters in url
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
    docstring: str
    sample: Any
    referenced_class: str

    @classmethod
    def from_enum(cls, enum_element: ApibEnum) -> Generator['Attribute', None, None]:
        """
        Generator for attributes from an ApibEnum
        """
        for e in enum_element.enumerations:
            yield Attribute(name=e.content, python_type=simple_python_type(e.element),
                            docstring=e.description, sample=None, referenced_class=None)

    def source(self, for_enum: bool) -> str:
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
            name = snake_case(self.name)
            if name == 'none':
                name = 'none_'
            name, _ = subn(r'[^a-z0-9]', '_', name)
            name = sub('^([0-9])', '_\\1', name)
            value = self.name
            value = value.replace("'", '')
            lines.append(f"{name} = '{value}'")
        else:
            # something like:
            #   actor_org_name: Optional[str] = None
            attr_name = snake_case(self.name)
            if attr_name in RESERVED_PARAM_NAMES:
                attr_name = f'{attr_name}_'

            if self.sample:
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
    attributes: Optional[list[Attribute]] = field(default=None)
    description: str = field(default=None)
    is_enum: bool = field(default=None)
    baseclass: str = field(default=None)

    def source(self) -> Optional[str]:
        """
        Source code for this class or None
        """
        if self.baseclass and not self.attributes:
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
                                                        (f'{a.source(self.is_enum)}' for a in self.attributes)))

        result = CLASS_TEMPLATE.format(class_name=self.name,
                                       baseclass=baseclass,
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

    def source(self, class_name: str = None) -> str:
        """
        Generate API source for given class name. If class name is not given, then class name is derived from API title
        """
        class_name = class_name or f'{words_to_camel(self.title)}Api'
        base = commonprefix([f'{ep.url}/' for ep in self.endpoints])
        # remove everything after the last '/'
        base = re.sub('/\w*$', '', base)
        doc_lines = chain([self.title, ''], self.cleaned_doc_string.splitlines())
        docstring = '\n'.join(chain.from_iterable(break_line(line, prefix=' ' * 4) for line in doc_lines))
        class_head = self.class_template.format(class_name=class_name,
                                                base=base,
                                                docstring=docstring)

        # full API source is head followed by source for each endpoint
        full_api_source = '\n'.join(s
                                    for s in chain([class_head],
                                                   (ep.source(base=base)
                                                    for ep in self.endpoints))
                                    if s)
        return full_api_source


@dataclass(init=False)
class PythonClassRegistry:
    # TODO: to disambiguate names:
    #   + a global context can be set (name of the APIB currently processed)
    #       * set_context(context: str)
    #   + the context is used to create qualified identifiers for class names
    #       * qualified_class_name(class_name: str)->str
    #   + qualident: <prefix>%<class name>
    #   + class names are not converted to camel case during creation of PythonClass instances from APIB
    #   + python_types and referenced_classes in Attribute instances use qualified class names
    #       * use get_qualident() to validate reference and get qualified name
    #   + "proper" Python class names are created after all PythonClasses have been created --> normalization before
    #       code creation
    #   + the normalization makes sure that unique Python class names are used
    #       + mapper from qualified class name to "normalized" Python class name
    #       + remove qualifier
    #       + convert class names to camel case
    #       + make class names unique
    #       + after creating unique unqualified class names the resulting mapping is used to update references to
    #           class names
    #       + normalization updates
    #           + python_type in Attribute
    #           + referenced_class in Attribute
    #           + python_type in PythonClass
    #           * ... in Endpoint
    #   + after normalization updated PythonClass and Attribute instances can be used for code creation
    #

    # context used to disambiguate class names in the registry
    _context: str = field(repr=False)

    # registered classes
    _classes: dict[str, PythonClass] = field(repr=False)

    #: Dictionary of APIs indexed by basename of APIB file w/o suffix
    _apis: dict[str, PythonAPI] = field(repr=False)

    def __init__(self):
        self._context = None
        self._classes = dict()
        self._apis = dict()

    def set_context(self, context: str):
        if self._context == '-':
            raise ValueError('context cannot be set after eliminate_redundancies()')
        self._context = context

    def qualified_class_name(self, class_name: Optional[str]) -> Optional[str]:
        """
        Get qualified identified for given class name
        """
        if class_name is None:
            return None
        if self._context == '-' or '%' in class_name:
            return class_name
        return f'{self._context}%{sanitize_class_name(class_name)}'

    def _add_api(self, apib_key: str, python_api: PythonAPI):
        if apib_key in self._apis:
            raise KeyError(f'"{apib_key}" already has an API registered')
        self._apis[apib_key] = python_api

    def apis(self) -> Iterable[tuple[str, PythonAPI]]:
        return self._apis.items()

    def _add_class(self, pc: PythonClass):
        """
        Add a python class to the registry. When adding the class name to the registry pc.name gets updated to a
        qualident.
        pc.name has to be unique; this is ensured her
        """
        qualident = self.qualified_class_name(sanitize_class_name(pc.name))
        if qualident in self._classes:
            log.warning(f'python class name "{pc.name}" already registered')
            qualident = next((name
                              for i in range(1, 10)
                              if (name := f'{qualident}{i}') not in self._classes))
            log.warning(f'class name "{pc.name}" not unique using qualident "{qualident}" instead')
        pc.name = qualident
        self._classes[pc.name] = pc

    def get(self, class_name: str) -> Optional[PythonClass]:
        """
        Get a python class from the registry for a given (potentially unqualified) class name
        """
        class_name = self.qualified_class_name(class_name)
        if pc := self._classes.get(class_name):
            _, pc = self._dereferenced_class(pc.name)
        return pc

    def classes(self) -> Generator[PythonClass, None, None]:
        """
        Generator for all registered classes
        :return:
        """
        visited = set()

        def yield_from_classname(class_name: Optional[str]) -> Generator[PythonClass, None, None]:
            if class_name is None:
                return

            # descend down into baseclasses if there are no attributes
            _, c = self._dereferenced_class(class_name)
            if c is None:
                return

            yield from yield_classes(c)
            return

        def yield_classes(p_class: PythonClass) -> Generator[PythonClass, None, None]:
            yield from yield_from_classname(p_class.baseclass)
            for attr in p_class.attributes:
                yield from yield_from_classname(attr.referenced_class)

            if p_class.name not in visited:
                visited.add(p_class.name)
                yield p_class

        for pc_name in self._classes:
            yield from yield_from_classname(pc_name)

    def endpoints(self) -> Iterable[tuple[str, Endpoint]]:
        """
        Generator of endpoints defined in the APIB
        yields tuples of APIB key and Endpoint instance
        """
        return chain.from_iterable(((apib_key, ep)
                                    for ep in api.endpoints)
                                   for apib_key, api in self.apis())

    def _python_class_attributes(self, basename: str, members: list[ApibMember]) -> list[Attribute]:
        attributes = []
        if not members:
            return attributes
        for member in members:
            attribute = self._attribute_from_member(basename, member)
            if attribute:
                attributes.append(attribute)
        return attributes

    def _attribute_from_member(self, class_name: str, member: ApibMember) -> Attribute:
        """
        derive Attribute from APIB member. Create and register classes on the fly as needed
        """
        if member.element != 'member':
            log.warning(f'Not implemented, member element: {member.element}')
            # TODO: implement this case
            raise NotImplementedError
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
            elif array_element_type == 'number':
                content = value.content[0]
                python_type = f'list[{content.content.__class__.__name__}]'
                sample = f'[{", ".join(f"{c.content}" for c in value.content)}]'
            elif array_element_type == 'object':
                # array of some object
                if not isinstance(value.content, list) or len(value.content) != 1:
                    raise ValueError(f'Well, this is unexpected: {value.content}')
                content: ApibObject = value.content[0]
                referenced_class = f'{class_name}{name[0].upper()}{name[1:]}'
                class_attributes = self._python_class_attributes(basename=referenced_class,
                                                                 members=content.content)
                new_class = PythonClass(name=referenced_class, attributes=class_attributes,
                                        description=value.description, is_enum=False, baseclass=None)

                self._add_class(new_class)
                python_type = f'list[{new_class.name}]'
            elif array_element_type == 'enum':
                # array of enum
                if not isinstance(value.content, list) or len(value.content) != 1:
                    raise ValueError(f'Well, this is unexpected: {value.content}')
                # create enum on the fly
                content: ApibEnum = value.content[0]
                referenced_class = f'{class_name}{name[0].upper()}{name[1:]}'
                class_attributes = list(Attribute.from_enum(content))
                new_class = PythonClass(name=referenced_class, attributes=class_attributes,
                                        description=value.description, is_enum=True, baseclass=None)
                self._add_class(new_class)
                python_type = f'list[{new_class.name}]'
            else:
                # array of some type
                # references class is that type
                referenced_class = array_element_type
                referenced_class = self.qualified_class_name(sanitize_class_name(referenced_class))
                # .. and the Python type is a list of that type
                python_type = f'list[{referenced_class}]'
        elif value.element == 'object':
            # we need a class with these attributes
            python_type = f'{class_name}{name[0].upper()}{name[1:]}'
            python_type, _ = re.subn(r'[^\w_]', '', python_type)
            sample = None
            python_type = sanitize_class_name(python_type)
            referenced_class = python_type
            class_attributes = self._python_class_attributes(basename=referenced_class, members=value.content)
            new_class = PythonClass(name=referenced_class, attributes=class_attributes,
                                    description=value.description, is_enum=False, baseclass=None)
            self._add_class(new_class)
            python_type = new_class.name
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
            python_type = sanitize_class_name(python_type)
            sample = value.content and value.content.content
            referenced_class = python_type
            class_attributes = list(Attribute.from_enum(value))
            new_class = PythonClass(name=referenced_class, attributes=class_attributes,
                                    description=value.description, is_enum=True, baseclass=None)
            self._add_class(new_class)
            python_type = new_class.name
            referenced_class = new_class.name
        elif value.element == 'boolean':
            python_type = 'bool'
            sample = value.content
        else:
            # this might be a reference to a class
            python_type = value.element
            python_type = self.qualified_class_name(sanitize_class_name(python_type))
            referenced_class = python_type
            try:
                sample = value.content and value.content.content
            except AttributeError:
                sample = None
        if referenced_class:
            referenced_class = self.qualified_class_name(referenced_class)
        return Attribute(name=name, python_type=python_type, docstring=docstring, sample=sample,
                         referenced_class=referenced_class)

    def _add_classes_from_data_structure(self, ds: ApibDatastructure, class_name: str = None) -> PythonClass:
        """
        Add classes defined in a given APIB datastructure
        """
        # content can be 'object' or 'enum'
        content = ds.content
        content_element = content and content.element
        class_name = class_name or ds.class_name
        if not class_name:
            raise ValueError('Undefined class name')
        class_name = sanitize_class_name(class_name)
        baseclass = sanitize_class_name(ds.baseclass)
        if not content_element:
            raise ValueError('content element should not be None')
        elif content_element == 'object':
            content: ApibObject
            # get attributes from object content
            attributes = self._python_class_attributes(basename=class_name,
                                                       members=content.content)
            pc = PythonClass(name=class_name, attributes=attributes, description=None, is_enum=False,
                             baseclass=baseclass)

        elif content_element == 'enum':
            content: ApibEnum
            attributes = list(Attribute.from_enum(content))
            pc = PythonClass(name=class_name, attributes=attributes, is_enum=True)
        else:
            attributes = self._python_class_attributes(basename=class_name,
                                                       members=content.content)
            baseclass = self.qualified_class_name(baseclass)
            pc = PythonClass(name=class_name, attributes=attributes, description=None, is_enum=False,
                             baseclass=baseclass)
        self._add_class(pc)
        return pc

    def add_classes_from_parse_result(self, parse_result: ApibParseResult) -> Generator['PythonClass', None, None]:
        """
        All Python classes (implicit and explict and classes used in results of endpoint calls)
        """
        for ds in parse_result.api.data_structures():
            self._add_classes_from_data_structure(ds)

        # also go through transitions and look at response datastructures
        # TODO: isn't this redundant w/ _register_endpoints?
        # for transition in parse_result.api.transitions():
        #     response = transition.http_transaction.response
        #     ds = response and response.datastructure
        #     if not ds:
        #         continue
        #
        #     # skip datastructures w/o attributes
        #     if not ds.attributes:
        #         continue
        #     self.add_classes_from_data_structure(ds)
        self._register_endpoints(parsed_blueprint=parse_result)

    def _dereferenced_class(self, class_name) -> tuple[str, Optional[PythonClass]]:
        while True:
            pc = self._classes.get(class_name)
            if not pc:
                log.error(f'class "{class_name}" not found')
                return class_name, None
            if pc.baseclass and not pc.attributes:
                class_name = pc.baseclass
                continue
            return class_name, pc

    def _dereferenced_class_name(self, class_name) -> str:
        class_name, _ = self._dereferenced_class(class_name)
        return class_name

    def _attribute_python_type(self, attribute: Attribute) -> str:
        if not attribute.referenced_class:
            return attribute.python_type
        class_name = self._dereferenced_class_name(attribute.referenced_class)
        if class_name != attribute.referenced_class:
            # clean up the python type and referenced class on the fly
            new_python_type = attribute.python_type.replace(attribute.referenced_class, class_name)
            log.debug(f'update attribute {attribute.name}: '
                      f'python_type "{attribute.python_type}" -> "{new_python_type}"')
            attribute.referenced_class = class_name
            attribute.python_type = new_python_type
        return attribute.python_type

    def eliminate_redundancies(self):
        """
        Find classes that are equivalent and then remove the redundant definitions
        """

        def attribute_key(pc: PythonClass) -> str:
            # concatenation of sorted attribute names ...
            key = '/'.join(sorted(attr.name for attr in pc.attributes))
            # ... with leading enum indication
            return f'{pc.is_enum}/{key}'

        def classes_equivalent(pc1: PythonClass, pc2: PythonClass) -> bool:
            # two classes are equivalent if
            #   * they have the same attribute names
            #   * attribute classes are identical
            #   * ... or attribute classes are equivalent
            if pc1.baseclass and not pc1.attributes:
                return False
            if pc2.baseclass and not pc2.attributes:
                return False
            if pc1.is_enum != pc2.is_enum:
                return False
            if attribute_key(pc1) != attribute_key(pc2):
                return False
            if pc1.name == pc2.name:
                if pc1 == pc2:
                    # if both classes are the same then they are equivalent and no further optimization is needed
                    return True
                raise ValueError('equal class names should imply class equality!')
            if not pc1.is_enum:
                # if these are not enums then we actually have to compare the attributes
                for attr1, attr2 in zip(sorted(pc1.attributes, key=attrgetter('name')),
                                        sorted(pc2.attributes, key=attrgetter('name'))):
                    attr1: Attribute
                    attr2: Attribute
                    attr1_type = self._attribute_python_type(attr1)
                    attr2_type = self._attribute_python_type(attr2)
                    if attr1_type == attr2_type:
                        # attributes are identical
                        continue

                    # maybe both attributes reference equivalent classes?
                    if not all((attr1.referenced_class, attr2.referenced_class)):
                        return False
                    class1, ref1 = self._dereferenced_class(attr1.referenced_class)
                    class2, ref2 = self._dereferenced_class(attr2.referenced_class)
                    if not all((ref1, ref2)) or not classes_equivalent(ref1, ref2):
                        return False

                    # check the python types of both attributes again
                    attr1_type = self._attribute_python_type(attr1)
                    attr2_type = self._attribute_python_type(attr2)
                    if attr1_type != attr2_type:
                        return False
                    # if
                # for
            # if
            # make pc2 redundant
            log.debug(f'"{pc1.name}" and "{pc2.name}" are equivalent. Making "{pc2.name}" redundant')
            pc2.baseclass = pc1.name
            pc2.attributes = None
            return True

        # start by grouping all Python classes by their attribute_key
        class_groups: dict[str, list[PythonClass]] = defaultdict(list)
        for pc in self._classes.values():
            # only consider classes that haven't been eliminated yet
            if pc.baseclass and not pc.attributes:
                continue
            class_groups[attribute_key(pc)].append(pc)

        # now work though the groups sorted by number of classes in each group
        for attr_key in sorted(class_groups, key=lambda k: len(class_groups[k]), reverse=True):
            candidates = class_groups[attr_key]
            # we don't need to look at classes that are already optimized
            candidates = [c for c in candidates if not c.baseclass or c.attributes]
            if len(candidates) == 1:
                continue

            # pairwise check of all candidates
            # check all candidates but the last ...
            for i, candidate1 in enumerate(candidates[:-1]):
                # ... against all candidates further down the line for equivalency
                list(map(partial(classes_equivalent, candidate1), candidates[i + 1:]))
                if candidate1.is_enum:
                    # in this case the 1st iteration should already have covered everything
                    # ... b/c for enums only the attribute_key matters and all candidates have the same
                    # attribute_key
                    break
                # if
            # for
        # now go through all attributes and update the types
        for pc in self.classes():
            if pc.is_enum or not pc.attributes:
                continue
            list(map(self._attribute_python_type, pc.attributes))
        return
        # TODO: might need some logic to work with super-classes
        #   instead of creating child classes it might actually be better to always use the class with the superset
        #   of attributes and only use proper exclude= parameters when serializing to json. For further investigation
        # now we can still try to find classes hat have common attributes
        common_attributes: dict[int, dict[str, dict[str, PythonClass]]] = defaultdict(lambda: defaultdict(dict))
        p_classes = list(self._classes.values())
        for i, class1 in enumerate(p_classes[:-1]):
            if class1.baseclass and not class1.attributes:
                continue
            attr1 = set(a.name for a in class1.attributes)
            for class2 in p_classes[i + 1:]:
                if class2.baseclass and not class2.attributes:
                    continue
                attr2 = set(a.name for a in class2.attributes)
                common_attr = attr1 & attr2
                # for now we only want to consider full subclasses; one class doesn't have more than the common
                # attributes
                if len(class1.attributes) != len(common_attr) and len(class2.attributes) != len(common_attr):
                    continue
                # we only want to look at cases where we have at least 2 common attributes
                if len(common_attr) < 3:
                    continue
                if common_attr:
                    common_key = "/".join(sorted(common_attr))
                    class_dict = common_attributes[len(common_attr)][common_key]
                    class_dict[class1.name] = class1
                    class_dict[class2.name] = class2
                # if
            # for
        # for

    def normalize(self):
        """
        Eliminate redundancies and then transform all class names to Python class names
            * the normalization makes sure that unique Python class names are used
              * mapper from qualified class name to "normalized" Python class name
              * remove qualifier
              * convert class names to camel case
              * make class names unique
              * after creating unique unqualified class names the resulting mapping is used to update references to
                  class names
              * normalization updates
                  * python_type in Attribute
                  * referenced_class in Attribute
                  * python_type in PythonClass
                  * ... in Endpoint
            * after normalization updated PythonClass and Attribute instances can be used for code creation
        """
        self.eliminate_redundancies()

        # mapping qualidents to Python class names
        qualident_to_python_name: dict[str, str] = dict()
        python_names = set()

        # create the mappings
        for qualident, pc in self._classes.items():
            python_name = words_to_camel(pc.name.split('%')[-1])
            # disambiguate class names by appending an index
            python_name = next((pn for suffix in chain([''], (str(i) for i in range(1, 100)))
                                if (pn := f'{python_name}{suffix}') not in python_names))
            # keep record of the Python class name
            python_names.add(python_name)
            qualident_to_python_name[qualident] = python_name

        # now go through all classes and clean up references from qualidents to Python names
        for qualident, python_name in qualident_to_python_name.items():
            pc = self._classes.pop(qualident)
            pc.name = python_name
            pc.baseclass = pc.baseclass and qualident_to_python_name[pc.baseclass]
            if pc.attributes:
                for attr in pc.attributes:
                    if attr.referenced_class:
                        new_class_name = qualident_to_python_name[attr.referenced_class]
                        attr.python_type = attr.python_type.replace(attr.referenced_class, new_class_name)
                        attr.referenced_class = new_class_name
            self._classes[python_name] = pc

        # now go through all classes and attributes again and updated to dereferences classes
        for pc in self._classes.values():
            if pc.attributes:
                for attr in pc.attributes:
                    if attr.referenced_class:
                        new_class_name = self._dereferenced_class_name(attr.referenced_class)
                        if new_class_name != attr.referenced_class:
                            attr.python_type = attr.python_type.replace(attr.referenced_class, new_class_name)
                            attr.referenced_class = new_class_name

        # update class references in endpoints
        for key, endpoint in self.endpoints():
            # parameter
            for param in chain(endpoint.body_parameter, endpoint.href_parameter):
                if param.referenced_class:
                    python_name = qualident_to_python_name[param.referenced_class]
                    python_name, _ = self._dereferenced_class(python_name)
                    param.python_type = param.python_type.replace(param.referenced_class, python_name)
                    param.referenced_class = python_name

            # result class
            if endpoint.result_referenced_class:
                python_name = qualident_to_python_name[endpoint.result_referenced_class]
                python_name, _ = self._dereferenced_class(python_name)
                endpoint.result = endpoint.result.replace(endpoint.result_referenced_class,
                                                          python_name)
                endpoint.result_referenced_class = python_name
        self._context = '-'

    def baseclasses_for_common_attribute_sets(self):
        """
        Try to find classes that have sets of common attributes.
        If A and B have common attributes a1, a2, ..., aI then create base class C with attributes a1, a2, ..., an
        """
        # for each class
        #   for each other class
        #       * determine the set of common attributes
        #       * record class, # of common attributes, common attributes
        #       * group candidates together by common attribute names
        # pick the class with the largest overlap of attributes
        # generate new base class if common attributes are not covering everything
        # TODO: implement
        ...

    def _register_endpoints(self, parsed_blueprint: ApibParseResult):
        """
        Determine endpoints defined in parsed blueprint and register the endpoints. Python classes are registered on
        the fly as needed
        """
        apib_key = self._context
        # host is defined at tha API level
        # something like 'https://webexapis.com/v1/'
        host = parsed_blueprint.api.host

        # register API
        python_api = PythonAPI.from_apib_api(parsed_blueprint.api)
        self._add_api(apib_key=apib_key, python_api=python_api)

        for transition in parsed_blueprint.api.transitions():
            # come up with a name for the method
            # 'List Admin Audit Events' --> 'list_admin_audit_events'
            name = snake_case(transition.title)
            # name = '_'.join(transition.title.split()).lower()

            # href is something like '/adminAudit/events{?orgId,from,to,actorId,max,offset,eventCategories}'
            href = transition.href
            # extract the href parameter names from the part between the brackets
            if m := re.search(r'\{\?(.+)}', href):
                href_param_names = m.group(1).split(',')
            else:
                href_param_names = []

            # url can contain url parameters in brackets: {}, but we want to get rid of the
            # trailing stuff like {?orgId,locationId,max,start,name,phoneNumber}
            url = re.sub(r'\{\?.+}\s*$', '', href)
            url = url.strip('/')

            # gather info from the HTTP transaction
            http_transaction = transition.http_transaction
            request = http_transaction.request
            response = http_transaction.response

            method = request.method
            response_datastructure = response.datastructure
            href_parameters = []
            for href_variable in transition.href_variables:
                param = self._param_from_member_or_select(endpoint_name=name, member=href_variable)
                if f'{{{param.name}}}' in url:
                    param.url_parameter = True
                href_parameters.append(param)

            body_parameters = []
            body_class_name = None
            if body := request.find_content_by_element('dataStructure'):
                body: ApibDatastructure
                body_content = body.content
                if isinstance(body_content, ApibObject):
                    # The object should have all attributes
                    body_content: ApibObject
                    # ApibObject has a list of members
                    body_parameters = [self._param_from_member_or_select(endpoint_name=name, member=member)
                                       for member in body_content.content]
                elif isinstance(body_content, ApibElement) and not any((body_content.content,
                                                                        body_content.meta)):
                    # this might be a class name
                    class_name_base = sanitize_class_name(body_content.element)
                    class_name = self.qualified_class_name(class_name_base)
                    body_class_name = class_name

                    # type attributes is the only acceptable attribute
                    optional = False
                    if body_content.attributes:
                        if set(body_content.attributes) != {'typeAttributes'}:
                            raise KeyError(f'Only typeAttributes are acceptable, got: '
                                           f'{", ".join(sorted(body_content.attributes))}')
                        type_attributes = set(ta.content for ta in body_content.attributes['typeAttributes'].content)
                        optional = 'required' not in type_attributes
                    # .. and that class should exist
                    if python_class := self.get(class_name):
                        # attributes of the class -> parameters
                        if python_class.attributes:
                            body_parameters = [Parameter(name=attr.name, python_type=attr.python_type,
                                                         docstring=attr.docstring, sample=attr.sample,
                                                         optional=optional, referenced_class=attr.referenced_class,
                                                         registry=self)
                                               for attr in python_class.attributes]
                        else:
                            raise NotImplementedError('No attributes')
                    else:
                        raise ValueError(f'Unknown body class name "{class_name_base}" for "{name}()"')
                else:
                    raise NotImplementedError(f'http request body datastructure '
                                              f'with unexpected content: "{body_content.element}"')

            result = None
            referenced_class = None
            if response_datastructure:
                # we have as response datastructure
                # a response datastructure should always have content
                response_ds_content = response_datastructure.content
                if not response_ds_content:
                    raise ValueError('response datastructure w/o content')
                else:
                    # the datastructure content can have content...
                    if response_ds_content.content:
                        # ... and then the element is either 'array' or 'object'
                        if response_ds_content.element == 'object':
                            # create a new response class
                            response_class = self._add_classes_from_data_structure(
                                ds=response_datastructure,
                                class_name=f'{" ".join(map(str.capitalize, name.split("_")))} Response')
                            result = response_class.name
                        elif response_ds_content.element == 'array':
                            array_content_class_name = sanitize_class_name(response_ds_content.content[0].element)
                            array_content_class_name = self.qualified_class_name(array_content_class_name)
                            result = f'list[{array_content_class_name}]'
                            referenced_class = array_content_class_name
                        else:
                            raise ValueError(f'Unexpected response datastructure content element: '
                                             f'"{response_ds_content.element}"')

                    else:
                        # .. or the datastructure content doesn't have content
                        # and in this case the element is a reference to a class
                        result = response_datastructure.content.element
                        result = self.qualified_class_name(sanitize_class_name(result))
                        # .. and the class has to exist
                        if not self.get(class_name=result):
                            raise KeyError(f'class "{result}" not found')
            referenced_class = referenced_class or result
            endpoint = Endpoint(name=name, method=method, host=host, url=url,
                                title=transition.title,
                                docstring=transition.docstring,
                                href_parameter=href_parameters,
                                body_parameter=body_parameters,
                                body_class_name=body_class_name,
                                result=result,
                                result_referenced_class=referenced_class,
                                registry=self)
            # register endpoint on API
            python_api.add_endpoint(endpoint)
        return

    def _param_from_member_or_select(self, endpoint_name: str, member: Union[ApibMember, ApibSelect]) -> Parameter:

        if not (isinstance(member, ApibMember) or isinstance(member, ApibSelect)):
            raise TypeError(f'unexpected parameter type: {member.__class__.__name__}')

        if isinstance(member, ApibSelect):
            member: ApibSelect
            name = member.option_key
            docstring = member.description
            # collect all types
            types = [simple_python_type(option.content.value.element, option.content.value.content)
                     for option in member.content]
            python_type = f'Union[{", ".join(sorted(set(types)))}]'
            text_of_options = '\n'.join(f'{option.content.value.content} ({t})'
                                        for option, t in zip(member.content, types))
            docstring = '\n'.join(l for l in chain((docstring, 'One of:'),
                                                   (f'  * {tl}' for tl in text_of_options.splitlines()))
                                  if l is not None)

            parameter = Parameter(name=name, python_type=python_type, docstring=docstring, referenced_class=None,
                                  optional=False, sample=None, registry=self)
            return parameter

        # determine parameter name,
        name = member.key

        docstring = member.description
        sample = member.value
        if member.meta is None:
            type_hint = None
        else:
            type_hint = member.meta.title
        optional = 'required' not in member.type_attributes

        # now try to determine the actual Python type and sample value
        type_hint_lower = type_hint and type_hint.lower()
        python_type = ''
        referenced_class = None

        if isinstance(sample, ApibString):
            sample = sample.content
        elif isinstance(sample, ApibBool):
            sample = sample.content
        elif isinstance(sample, ApibNumber):
            sample = sample.content

        if isinstance(sample, ApibElement):
            if isinstance(sample, ApibEnum):
                sample: ApibEnum
                # create an enum on the fly
                # name of the enum is based on the method name and the attribute
                enum_name = ''.join(map(str.capitalize, endpoint_name.split('_')))
                enum_name = f'{enum_name}{name[0].upper()}{name[1:]}'
                enum_attributes = list(Attribute.from_enum(sample))
                enum_class = PythonClass(name=enum_name, description=docstring, is_enum=True,
                                         attributes=enum_attributes)
                # and register that
                self._add_class(enum_class)
                enum_name = enum_class.name
                if sample.default:
                    sample = sample.default.content
                else:
                    # try the 1st enum value
                    sample = sample.enum_values[0]
                python_type = enum_name
                referenced_class = enum_name
            elif isinstance(sample, ApibObject):
                # create a class on the fly
                class_name = ''.join(map(str.capitalize, endpoint_name.split('_')))
                class_name = f'{class_name}{name[0].upper()}{name[1:]}'
                class_attributes = []
                for sample_member in sample.content:
                    attribute = self._attribute_from_member(class_name=class_name,
                                                            member=sample_member)
                    class_attributes.append(attribute)
                new_class = PythonClass(name=class_name, description=docstring, is_enum=False,
                                        attributes=class_attributes)
                # and register that
                self._add_class(new_class)
                sample = ''
                python_type = new_class.name
                referenced_class = new_class.name
            elif isinstance(sample, ApibArray):
                try:
                    python_type = simple_python_type(sample.content[0].element)
                except ValueError:
                    python_type = None
                if python_type:
                    # simple type
                    python_type = f'list[{python_type}]'
                    sample = ", ".join(f"'{e.content}'" for e in sample.content)
                    sample = f'[{sample}]'
                else:
                    # hopefully we can figure out the type of the array elements. For this we expect the
                    # sample content to have exactly one ApibElement entry
                    if len(sample.content) != 1:
                        raise NotImplementedError(f'Unexpected sample: {sample}')
                    arr_element = sample.content[0]
                    if not isinstance(arr_element, ApibElement):
                        raise NotImplementedError(f'Unexpected sample: {sample}')
                    if isinstance(arr_element, ApibObject):
                        # create a class on the fly
                        class_name = ''.join(map(str.capitalize, endpoint_name.split('_')))
                        class_name = f'{class_name}{name[0].upper()}{name[1:]}'
                        class_attributes = []
                        for sample_member in arr_element.content:
                            attribute = self._attribute_from_member(class_name=class_name,
                                                                    member=sample_member)
                            class_attributes.append(attribute)
                        new_class = PythonClass(name=class_name, description=docstring, is_enum=False,
                                                attributes=class_attributes)
                        # and register that
                        self._add_class(new_class)
                        class_name = new_class.name
                        referenced_class = new_class.name
                        sample = ''
                        python_type = f'list[{new_class.name}]'
                    else:
                        # this is an array of a class instance and the arr_element has the class name
                        class_name = sanitize_class_name(arr_element.element)
                        class_name = self.qualified_class_name(class_name)
                        # this class has to exist
                        if pc := self.get(class_name):
                            python_type = f'list[{pc.name}]'
                            referenced_class = pc.name
                            sample = ''
                        else:
                            raise KeyError(f'Unknown class: {class_name}')
            elif isinstance(sample, ApibElement):
                # in this case the element is a class name
                class_name = sanitize_class_name(sample.element)
                class_name = self.qualified_class_name(class_name)

                # this class should exist
                if not self.get(class_name):
                    raise KeyError(f'Unknown class: {class_name}')
                else:
                    python_type = class_name
                    referenced_class = class_name
                    if sample.meta:
                        raise NotImplementedError()
                    if (sample.attributes and
                            (unexpected_attributes := set(sample.attributes) - {'typeAttributes', 'default',
                                                                                'enumerations'})):
                        raise NotImplementedError(f'Unexpected sample attributes: '
                                                  f'{", ".join(sorted(unexpected_attributes))}')
                    if sample.content:
                        sample = sample.content.content
                    else:
                        sample = ''
            else:
                raise NotImplementedError(f'unhandled sample: {sample}')
        elif type_hint_lower == 'string' or type_hint_lower is None:
            # could be a datetime
            if sample is None:
                python_type = 'str'
            else:
                try:
                    dateutil.parser.parse(sample)
                    python_type = 'datetime'
                except (OverflowError, dateutil.parser.ParserError, TypeError):
                    # probably a string
                    python_type = 'str'
                except Exception as e:
                    raise NotImplementedError(f'Unexpected error when trying to parse a string: {e}')
        elif type_hint_lower == 'number':
            # can be int or float
            if sample is None:
                python_type = 'int'
            else:
                try:
                    sample = int(sample)
                    python_type = 'int'
                except ValueError:
                    python_type = 'float'
                    try:
                        sample = float(sample)
                    except ValueError:
                        pass
        elif type_hint_lower in {'integer', 'long', 'int'}:
            python_type = 'int'
            try:
                sample = int(sample)
            except ValueError:
                pass
        elif type_hint_lower == 'boolean':
            python_type = 'bool'
        elif type_hint_lower in {'list', 'array'}:
            python_type = 'list[str]'
        elif type_hint_lower.startswith('array['):
            # let's see whether the type spec is a known class
            m = re.match(r'array\[(.+)]', type_hint)
            array_element_class = m.group(1)
            pc = self.get(self.qualified_class_name(sanitize_class_name(array_element_class)))
            if pc:
                # reference to known class name
                python_type = f'list[{pc.name}]'
                referenced_class = pc.name
            else:
                python_type = f'list[{simple_python_type(array_element_class)}]'
        elif type_hint_lower == 'string array':
            python_type = 'list[str]'
        else:
            # check whether the type hint is a known PythonClass
            if pc := self.get(type_hint):
                if pc.is_enum:
                    python_type = type_hint
                else:
                    NotImplementedError('No idea how to hande a non-enum class in href parameters')
            else:
                raise NotImplementedError(f'unexpected type hint: "{type_hint_lower}"')
        if not python_type:
            raise ValueError('Well, that\'s embarrassing!')

        parameter = Parameter(name=name, python_type=python_type, docstring=docstring, sample=sample,
                              optional=optional, referenced_class=referenced_class, registry=self)
        return parameter


def simple_python_type(type_hint: str, value: Any = None) -> str:
    if type_hint == 'string':
        return 'str'
    elif type_hint == 'number':
        # could be float or int
        if value is not None:
            try:
                float(value)
            except ValueError:
                return 'int'
            return 'float'
        return 'int'
    elif type_hint == 'boolean':
        return 'bool'
    else:
        raise ValueError(f'unexpected simple type: {type_hint}')

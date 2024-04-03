import logging
import re
import sys
from collections import defaultdict
from collections.abc import Generator, Iterable
from dataclasses import dataclass, field
from io import StringIO
from itertools import chain
from typing import Union, Optional, NamedTuple, ClassVar, overload

from bs4 import BeautifulSoup, ResultSet, Tag
from inflection import underscore
from pydantic import BaseModel, Field, model_validator, field_validator
from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from yaml import safe_load, safe_dump

__all__ = ['MethodDoc', 'SectionDoc', 'AttributeInfo', 'Parameter', 'MethodDetails', 'DocMethodDetails',
           'DevWebexComScraper', 'Credentials', 'SectionAndMethodDetails', 'Class', 'python_type', 'SectionDetails',
           'break_lines']

# "Standard" menu titles we want to ignore when pull method details from submenus on the left
IGNORE_MENUS = {
    'BroadWorks Billing Reports',
    'BroadWorks Device Provisioning',
    'BroadWorks Enterprises',
    'BroadWorks Subscribers',
    'Recording Report',
    'Video Mesh',
    'Wholesale Billing Reports',
    'Wholesale Customers',
    'Wholesale Subscribers'
}

# set this to limit scraping to a subset of menus; mainly for debugging
RELEVANT_MENUS = {
    'Call Controls'
}

log = logging.getLogger(__name__)


def debugger() -> bool:
    """
    Check if executed in debugger
    """
    return (gt := getattr(sys, 'gettrace', None)) and gt()


def div_repr(d) -> str:
    """
    Simple text representation of a div
    """
    if d is None:
        return 'None'
    assert d.name == 'div'
    classes = d.attrs.get('class', None)
    if classes:
        class_str = f" class={' '.join(classes)}"
    else:
        class_str = ''
    return f'<div{class_str}>'


@overload
def python_type(type_str: str) -> str:
    ...


@overload
def python_type(type_str: str, for_list: bool) -> tuple[str, str]:
    ...


def python_type(type_str: str, for_list: bool = False) -> Union[str, tuple[str, str]]:
    """
    Transform a type description from developer.cisco.com to a type that can be used in Python code

    :param type_str:
    :param for_list:
    :return:
    """
    # transform "Some Class" to "SomeClass"
    type_str, _ = re.subn(r'\s([A-Z])', '\g<1>', type_str)
    if type_str == 'number':
        return 'int'
    elif type_str == 'boolean':
        return 'bool'
    elif type_str.lower() == 'string':
        # sometimes apparently "String" is used
        return 'str'
    elif m := re.match(r'array\[(\w+)]', type_str):
        return f'List[{python_type(m.group(1))}]'
    elif type_str == 'array' or type_str == 'string array':
        return 'List[str]'
    if (referenced_class := Class.registry.get(type_str)) and referenced_class.base and \
            not referenced_class.attributes:
        # if the referenced class has a base class and no attributes then use the name of the base class instead
        return python_type(referenced_class.base)
    if for_list:
        # need to find an attribute that is a list
        assert referenced_class
        list_attr = next((a
                          for a in referenced_class.attributes
                          if (m := re.match(r'array\[(.+)]', a.type))), None)
        if list_attr:
            if list_attr.param_class:
                # if we have a class then the name of the class
                array_base_type_name = list_attr.param_class.name
            else:
                # ... else whatever (basic) type was provided
                array_base_type_name = m.group(1)
            return list_attr.name, python_type(array_base_type_name)
        else:
            raise KeyError(f'Oops, no "array" attribute, but we are supposed to get a type_name for a list: {type_str}')

    return type_str


class Credentials(NamedTuple):
    user: str
    password: str


class MethodDoc(BaseModel):
    #: HTTP method
    http_method: str
    #: API endpoint URL
    endpoint: str
    #: link to documentation page
    doc_link: str
    #: Documentation
    doc: str


class SectionDoc(BaseModel):
    """
    Available documentation for one section on developer.webex.com

    For example for Calling/Reference/Locations
    """
    #: menu text from the menu at the left under Reference linking to the page with the list of methods
    menu_text: str
    #: header from the section page on the right
    header: Optional[str] = None
    #: documentation from section page on the right
    doc: Optional[str] = None
    #: list of methods parsed from the page
    methods: list[MethodDoc]


@dataclass
class AttributeInfo:
    path: str
    parameter: 'Parameter'


class Parameter(BaseModel):
    name: str
    type: str
    type_spec: Optional[str] = None
    doc: str
    # parsed from params-type-non-object: probably an enum
    param_attrs: Optional[list['Parameter']] = Field(default_factory=list)
    # parsed from params-type-object: child object
    param_object: Optional[list['Parameter']] = Field(default_factory=list)
    # reference to Class object; us set during class generation. Not part of (de-)serialization
    param_class: 'Class' = Field(default=None)

    @property
    def required(self):
        return self.type_spec and self.type_spec.lower() == 'required'

    @property
    def python_name(self):
        name = underscore(self.name)
        if name in {'from', 'to', 'type'}:
            return f'{name}_'
        return name

    @field_validator('param_attrs', 'param_object', mode='after')
    def attrs_and_object(cls, v):
        if not v:
            return list()
        return v

    def attributes(self, *, path: str) -> Generator[AttributeInfo, None, None]:
        yield AttributeInfo(parameter=self, path=f'{path}/{self.name}')
        for p in self.param_attrs or list():
            yield from p.attributes(path=f'{path}/{self.name}/attrs')
        for p in self.param_object or list():
            yield from p.attributes(path=f'{path}/{self.name}/object')

    def model_dump(self, exclude=None, **kwargs):
        return super().model_dump(exclude={'param_class'}, **kwargs)

    def model_dump_json(self, exclude=None, **kwargs):
        return super().model_dump_json(exclude={'param_class'}, **kwargs)


def break_lines(line: str, line_start: str, first_line_prefix: str = None) -> Generator[str, None, None]:
    """
    Break line in multiple lines (max 120 chars) if needed
    """
    max_len = 120
    current_line = ''
    # indentation for lines starting with "*"
    star_line = line.strip().startswith('*')
    if star_line:
        line = line.strip()
        star_indent = '  '
    else:
        star_indent = ''

    if first_line_prefix:
        # consider the first_line_prefix for determination of line breaks for the 1st row
        line_prefix = first_line_prefix
        # first line returned as is. Prefixed as needed by caller
        start_of_line = ''
    else:
        # no special treatment for 1st line
        line_prefix = line_start
        start_of_line = line_start
    for word in line.split():
        if len(current_line) + len(line_prefix) + len(star_indent) + len(word) + 1 >= max_len:
            yield f'{start_of_line}{star_indent}{current_line}'
            current_line = ''
            # every line starting with the 2nd line always gets prefixed with line_start
            start_of_line = line_start
            if star_line:
                # increased indent of enumerations (star lines) starting with 2nd line
                star_indent = f'    '
            # ... and the line_start is considered for line break determination
            line_prefix = line_start
        # append word to current line
        current_line = f'{current_line} {word}'.strip()
    if current_line:
        yield f'{start_of_line}{star_indent}{current_line}'


@dataclass
class Class:
    #: registry of Class instances by name
    registry: ClassVar[dict[str, 'Class']] = dict()

    #: logger
    log: ClassVar[logging.Logger] = logging.getLogger(f'{__name__}.Class')

    #: class name
    name: str
    _name: str = field(init=False, repr=False, default=None)

    #: attribute list
    attributes: list[Parameter] = field(default_factory=list)

    is_enum: bool = field(default=False)

    base: str = field(default=None)

    source_generated: bool = field(default=False)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        if isinstance(new_name, property):
            raise TypeError('missing mandatory parameter: ''name''')
        if self._name is not None:
            # unregister old name
            self.registry.pop(self._name, None)
        self._name = new_name
        # register new name
        self.register()

    def register(self):
        """
        register instance
        """
        # we want to make sure that Class names are unique
        if self.registry.get(self._name) is not None:
            # suffix an index and pick the 1st name not taken
            new_name = next(name for i in range(1, 100)
                            if self.registry.get(name := f'{self._name}{i}') is None)
            self._name = new_name
        self.registry[self._name] = self

    def all_attributes(self) -> Generator[Parameter, None, None]:
        """
        all attributes: base attributes and attributes at the class level
        """
        if self.base:
            yield from self.registry[self.base].all_attributes()
        yield from self.attributes

    def equivalent(self, other: 'Class'):
        """
        check if both have the same attributes

        :param other:
        :return:
        """
        if other.base == self._name:
            return True
        if self.base == other._name:
            return True
        if len(self.attributes) != len(other.attributes):
            return False
        other_attrs = {a.name: a for a in other.attributes}
        for a1 in self.attributes:
            a2 = other_attrs.get(a1.name)
            if a2 is None:
                return False
            if a1.type != a2.type:
                return False
            if (not not a1.param_class) != (not not a2.param_class):
                return False
            if a1.param_class and not a1.param_class.equivalent(a2.param_class):
                return False
        return self.base == other.base

    def sources(self, only_childs: bool = False) -> Generator[str, None, None]:
        """
        Source for class
        :return:
        """

        def type_for_source(a: Parameter) -> str:
            """
            type string for Python source for given parameter
            """
            if a.param_class:
                if a.type.startswith('array'):
                    return f'list[{python_type(a.param_class._name)}]'
                return python_type(a.param_class._name)
            if a.type.startswith('array'):
                base_type = python_type(a.type[6:-1])
                return f'list[{base_type}]'
            else:
                return python_type(a.type)

        def enum_name(a: str) -> str:
            a = re.sub(r'[^\w0-9]', '_', a)
            if '_' in a:
                a = a.lower()
            else:
                a = underscore(a)
            return a

        def handle_starting_digit(name: str) -> str:
            if name[0] in '0123456789':
                digit_name = {'0': 'zero',
                              '1': 'one',
                              '2': 'two',
                              '3': 'three',
                              '4': 'four',
                              '5': 'five',
                              '6': 'six',
                              '7': 'seven',
                              '8': 'eight',
                              '9': 'nine'}[name[0]]
                name = f'{digit_name}_{name[1:].strip("_")}'
            return name

        if self.source_generated:
            # we are done here; source already generated
            return

        if not self.attributes and not self.base:
            # empty classes don't need to be generated
            return

        # 1st generate sources for all classes of any attributes
        child_classes = (attr.param_class for attr in self.attributes
                         if attr.param_class)
        for child_class in child_classes:
            yield from child_class.sources()

        # look at base
        if self.base:
            yield from self.registry[self.base].sources()

        if only_childs or not self.attributes:
            # don't need to actually create a source for this class if
            # * we only were asked to create child classes
            # * or this is a class w/o attributes --> this class is redundant and is represented by its base
            return

        # then yield source for this class
        source = StringIO()

        if self.base:
            bases = self.base
        elif self.is_enum:
            bases = 'str, Enum'
        else:
            bases = 'ApiModel'
        print(f'class {self._name}({bases}):', file=source)
        for attr in self.attributes:
            for line in attr.doc.strip('\n').splitlines():
                print('\n'.join(break_lines(line, '    #: ')), file=source)
            if self.is_enum:
                print(f'    {handle_starting_digit(enum_name(attr.name))} = \'{attr.name}\'', file=source)
            else:
                # determine whether we need an alias
                if re.search(r'\s', attr.name):
                    # if the attribute name has spaces then we need an alias
                    alias = f" = Field(alias='{attr.name}')"
                    attr_name = attr.name.replace(' ', '_')
                else:
                    attr_name = attr.name
                    alias = ''
                print(f'    {handle_starting_digit(underscore(attr_name))}: Optional[{type_for_source(attr)}]{alias}',
                      file=source)
        self.source_generated = True
        yield source.getvalue()
        return

    @classmethod
    def all_sources(cls) -> Generator[str, None, None]:
        """
        Generator for all class sources

        recurse through tree of all classes and yield class sources in correct order
        :return:
        """
        yield from chain.from_iterable(map(lambda c: c.sources(), cls.registry.values()))

    def common_attributes(self, other: 'Class') -> list[Parameter]:
        """
        Get list of common attributes
        :param other:
        :return:
        """

        def eq_type(type_a: str, type_b: str):
            # for comparing types 'number' and 'string' are considered equivalent
            a = type_a.replace('number', 'string')
            b = type_b.replace('number', 'string')
            return a == b

        other_attrs = {a.name: a for a in other.attributes}
        common = list()
        for attr in self.attributes:
            if (other_attr := other_attrs.get(attr.name)) is None:
                continue
            other_attr: Parameter
            if not eq_type(attr.type, other_attr.type):
                continue
            common.append(attr)
        return common

    @classmethod
    def optimize(cls):
        """
        find redundant classes
            * classes/enums with identical attribute lists
            * find classes which are subclasses of others
        :return:
        """

        def log_(msg: str, level: int = logging.DEBUG):
            log.log(msg=f'optimize: {msg}', level=level)

        # for all pairs or classes
        # * determine set of common (same name and type) attributes
        # * create new base classes as required
        for class_a in reversed(cls.registry.values()):
            if not class_a.attributes:
                # log_(f'{class_a._name}, skipping, no attributes')
                continue
            # for now ignore multiple tiers of hierarchy
            # if this class already has a base then don't check whether this class is subclass of another
            if class_a.base:
                # log_(f'{class_a._name}, skipping, base {class_a.base}')
                continue

            class ClassCommon(NamedTuple):
                class_: Class
                common: list[Parameter]

            # collect all candidate base classes: classes with common attributes and group them by number of common
            # attributes
            candidates: dict[int, list[ClassCommon]] = defaultdict(list)

            # look at all other classes
            for class_b in reversed(cls.registry.values()):
                if class_b._name == class_a._name:
                    continue
                # if class_b already has a base then skip
                if class_b.base:
                    # log_(f'{class_a._name}/{class_b._name}, skipping, {class_b._name} has base {class_b.base}')
                    continue

                # determine common attributes
                common = class_a.common_attributes(class_b)
                if len(common) == len(class_b.attributes) and len(common) > 1:
                    # all attributes of class_b also exist in our class_a -> candidate base class for class_a
                    log_(f'{class_a._name}/{class_b._name}, common attributes: {", ".join(a.name for a in common)}')
                    candidates[len(common)].append(ClassCommon(class_=class_b, common=common))
                # if
            # for
            # now pick the candidate base class with the largest overlap
            if candidates:
                cand_list = candidates[max(candidates)]
                class_b, common = cand_list[-1]

                # class_b is base for class_a
                class_a.base = class_b._name
                # ... and we can remove all common attributes from class_a
                names = {a.name for a in common}
                class_a.attributes = [a for a in class_a.attributes
                                      if a.name not in names]
            # if
        # for
        return


class MethodDetails(BaseModel):
    header: str
    doc: str
    parameters_and_response: dict[str, list[Parameter]]
    documentation: MethodDoc

    def attributes(self, *, path: str) -> Generator[AttributeInfo, None, None]:
        for pr_key in self.parameters_and_response:
            for p in self.parameters_and_response[pr_key]:
                yield from p.attributes(path=f'{path}/{self.header}/{pr_key}')

    @property
    def is_paginated(self) -> bool:
        """
        determine whether the method requires pagination

        requires pagination if:
            * 1st attribute returned is an array of something
            * has "max" query parameters
        """
        response_attributes = self.parameters_and_response.get('Response Properties')
        if not response_attributes:
            return False
        if not response_attributes[0].type.startswith('array['):
            return False
        p_names = set(p.name
                      for p in self.parameters_and_response.get('Query Parameters', []))
        return 'max' in p_names


class SectionAndMethodDetails(NamedTuple):
    section: str
    method_details: MethodDetails

    def __lt__(self, other: 'SectionAndMethodDetails'):
        return self.section < other.section or self.section == other.section and (
                self.method_details.documentation.endpoint < other.method_details.documentation.endpoint or
                self.method_details.documentation.endpoint == other.method_details.documentation.endpoint and
                self.method_details.documentation.http_method < other.method_details.documentation.http_method)


class SectionDetails(BaseModel):
    """
    Details for a section: header, doc and list of methods
    """
    header: Optional[str]
    doc: Optional[str]
    methods: list[MethodDetails]


class DocMethodDetails(BaseModel):
    """
    Container for all information; interface to YML file
    """
    info: Optional[str]
    #: dictionary indexed by menu text with list of methods in that section
    docs: dict[str, SectionDetails] = Field(default_factory=dict)

    @model_validator(mode='before')
    def backward_compatibility(cls, values):
        """
        docs used to be a dict of list of methods.
        When reading an "old" YML file then convert accordingly to that dict can be parsed as TabDetails
        :param values:
        :return:
        """
        docs = values.get('docs')
        if docs is None or not isinstance(docs, dict):
            return values
        for section in docs:
            content = docs[section]
            if isinstance(content, list):
                docs[section] = {'methods': content}
        return values

    @staticmethod
    def from_yml(path: str):
        with open(path, mode='r') as f:
            return DocMethodDetails.model_validate(safe_load(f))

    def to_yml(self, path: Optional[str] = None) -> Optional[str]:
        data = self.model_dump()
        if path:
            with open(path, mode='w') as f:
                if self.info:
                    line = '# ' + f'{self.info}' + '\n'
                    f.write(line)
                safe_dump(data, f)
            return None
        else:
            return safe_dump(data)

    def methods(self) -> Generator[SectionAndMethodDetails, None, None]:
        for section, method_details in self.docs.items():
            for m in method_details.methods:
                yield SectionAndMethodDetails(section=section, method_details=m)

    def attributes(self) -> Generator[AttributeInfo, None, None]:
        for method_details_key in self.docs:
            method_details = self.docs[method_details_key]
            for md in method_details.methods:
                yield from md.attributes(path=f'{method_details_key}')

    def model_dump(self, exclude=None, **kwargs):
        return super().model_dump(exclude={'info'}, by_alias=True, **kwargs)


# noinspection PyShadowingNames
@dataclass
class DevWebexComScraper:
    driver: ChromiumDriver
    logger: logging.Logger
    credentials: Credentials
    baseline: Optional[DocMethodDetails]
    new_only: bool
    section: str
    tabs: Union[str, list[str]]
    # ignore sections not part of the "core": the ones listed in IGNORE_MENUS
    ignore_non_core: bool

    def __init__(self, credentials: Credentials = None, baseline: DocMethodDetails = None,
                 new_only: bool = True, section: str = None, tabs: Union[str, list[str]] = None,
                 ignore_non_core: bool = True):
        self.driver = webdriver.Chrome()
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self.credentials = credentials
        self.baseline = baseline
        self.new_only = new_only
        self.section = section or 'Calling'
        self.tabs = tabs or 'all'
        self.ignore_non_core = ignore_non_core

    def close(self):
        self.log('close()')
        if self.driver:
            self.driver.quit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log('__exit__()')
        self.close()

    def __enter__(self):
        return self

    def log(self, msg: str, level: int = logging.DEBUG):
        self.logger.log(level=level, msg=msg)

    @staticmethod
    def by_class_and_text(find_in: Union[ChromiumDriver, WebElement], class_name: str, text: str) -> WebElement:
        """
        Find a WebElement by class name and text

        :param find_in: root to search in
        :param class_name: class name
        :param text: text
        :return: WebElement
        :raises:
            StopIteration: if no element can be found
        """
        return next((element for element in find_in.find_elements(by=By.CLASS_NAME, value=class_name)
                     if element.text == text))

    def login(self):
        """
        Log in
        :return:
        """
        if not self.credentials:
            return

        # look for: <a href="/login" id="header-login-link"><span>Log in</span></a>
        login = self.driver.find_element(by=By.ID, value='header-login-link')
        login.click()

        # wait for field to enter email address
        email = WebDriverWait(driver=self.driver, timeout=10).until(
            method=EC.visibility_of_element_located((By.ID, 'IDToken1'))
        )
        # email = self.driver.find_element(by=By.ID, value='IDToken1')
        email.send_keys(self.credentials.user)

        # wait for "Sign In" button
        sign_in = WebDriverWait(driver=self.driver, timeout=10).until(
            method=EC.element_to_be_clickable((By.ID, 'IDButton2')))
        sign_in.click()
        password = WebDriverWait(driver=self.driver, timeout=10).until(
            method=EC.visibility_of_element_located((By.ID, 'IDToken2')))
        password.send_keys(self.credentials.password)

        # wait for "Sign In" button
        sign_in = WebDriverWait(driver=self.driver, timeout=10).until(
            method=EC.element_to_be_clickable((By.ID, 'Button1')))
        sign_in.click()

        return

    @staticmethod
    def obj_class(tag: Tag) -> set[str]:
        """
        Check if a tag has one of the classes that designate an object

        :param tag:
        :return: set of tag classes designating an object
        """
        classes = set(tag.attrs.get('class', []))
        return classes & {'params-type-non-object', 'params-type-object'}

    def methods_from_api_reference_container(self, container: BeautifulSoup,
                                             header: str) -> Generator[MethodDoc, None, None]:
        """
        Yield method documentation instances for each method parsed from an API reference container on the right

        Container looks like:
            <div class="api_reference_entry__container">
                <div class="columns large-9">
                    <div class="XZCMfprZP3RvdJJ_CfTH"><h3>Locations</h3>
                        <p>Locations are used to organize Webex Calling (BroadCloud) features within physical
                        locations. Y .... .</p></div>
                    <div>
                        <div class="clearfix dVWBljZUFIGiEgkvpTg5"><h5 class="columns
                        small-9"><span>Method</span></h5><h5
                                class="columns small-3"><span>Description</span></h5></div>
                        <div class="UuvKF2Qey4J1ajkvpmiN">
                            <div class="B_af0kjJ65j92iCwAiw1">
                                <div class="columns small-9"><span
                                        class="md-badge md-badge--green E38yq9G_nWIm8SdrG1GU">GET</span><span
                                        class="X9_XSxV8TI6eNf98ElQU"><a
                                        href="/docs/api/v1/locations/list-locations">https://webexapis.com/v1
                                        /locations</a></span>
                                </div>
                                <div class="columns small-3 sn1OrZrRvd9GVOvUv4WK">List Locations</div>
                            </div>
                            <div class="cg3iKW8BWwV8ooZrsjQi">
                                <div class="X9_XSxV8TI6eNf98ElQU"><a
                                href="/docs/api/v1/locations/list-locations">https://webexapis.com/v1/locations</a>
                                </div>
                                <span class="md-badge md-badge--green E38yq9G_nWIm8SdrG1GU">GET</span><span
                                    class="sn1OrZrRvd9GVOvUv4WK">List Locations</span></div>
                        </div>

        :param container: API reference container
        :param header: header these methods belong under; for logging
        """

        def log(text: str, level: int = logging.DEBUG):
            self.log(f'    methods_from_api_reference_container("{header}"): {text}',
                     level=level)

        log('start')
        rows = container.div.div.find_all('div', recursive=False)[1].find_all('div', recursive=False)
        """
            Rows look like this:
                <div class="B_af0kjJ65j92iCwAiw1">
                    <div class="columns small-9"><span class="md-badge md-badge--green
                    E38yq9G_nWIm8SdrG1GU">GET</span><span
                            class="X9_XSxV8TI6eNf98ElQU"><a
                            href="/docs/api/v1/broadworks-billing-reports/list-broadworks-billing-reports">https
                            ://webexapis.com/v1/broadworks/billing/reports</a></span>
                    </div>
                    <div class="columns small-3 sn1OrZrRvd9GVOvUv4WK">List BroadWorks Billing Reports</div>
                </div>
                <div class="cg3iKW8BWwV8ooZrsjQi">
                    <div class="X9_XSxV8TI6eNf98ElQU"><a
                    href="/docs/api/v1/broadworks-billing-reports/list-broadworks-billing-reports">https://webexapis
                    .com/v1/broadworks/billing/reports</a>
                    </div>
                    <span class="md-badge md-badge--green E38yq9G_nWIm8SdrG1GU">GET</span><span
                    class="sn1OrZrRvd9GVOvUv4WK">List BroadWorks Billing Reports</span>
                </div>
        """
        for soup_row in rows[1:]:
            method = soup_row.div.div.span.text
            endpoint = soup_row.div.div.a.text
            doc_link = f"https://developer.webex.com{soup_row.div.div.a.get('href')}"
            doc = soup_row.div.find_all('div')[1].text

            log(f'{doc}', level=logging.INFO)
            log(f'yield: {method} {endpoint}: {doc}, {doc_link}', level=logging.DEBUG)
            yield MethodDoc(http_method=method, endpoint=endpoint, doc_link=doc_link, doc=doc)
        log('end')

    def docs_from_submenu_items(self, submenus: list[WebElement]) -> Generator[SectionDoc, None, None]:
        """
        Yield section information for each submenu on the left
        :param submenus:
        :return:
        """

        def log(text: str, level: int = logging.DEBUG):
            self.log(f'  endpoints_from_submenu_items({submenu.text}): {text}',
                     level=level)

        prev_container_header = None

        def wait_for_new_api_reference_container():
            """
            Wait until the page on teh right has been updated with new content after clicking on a new section on the
            left
            """

            def log(text: str):
                self.log(f'  wait_for_new_api_reference_container: {text}')

            def _predicate(driver):
                """
                Look for API reference container and check if the container header has changed
                """
                target = driver.find_element(By.CLASS_NAME, 'api_reference_entry__container')
                log('Container found' if target else 'Container not found')
                target = EC.visibility_of(target)(driver)
                log(f'Visibility: {not not target}')
                if target:
                    target: WebElement
                    # header selector: div.api_reference_entry__container > div > div:nth-of-type(1) > h3
                    container_header = target.find_element(
                        by=By.CSS_SELECTOR,
                        value='div > div:nth-of-type(1) > h3')

                    header_text = container_header.text
                    log(f'prev container header: {prev_container_header}, header: {header_text}')
                    if header_text != prev_container_header:
                        return target, header_text
                return False

            return _predicate

        for submenu in submenus:
            # decide whether we need to work on the sub menu
            submenu_text = submenu.text
            ignore = False
            if self.baseline:
                if self.new_only:
                    # only work on menus not present in the diff
                    if submenu_text in self.baseline.docs:
                        ignore = True
                else:
                    # skip if the baseline has the menu, but no methods. This is one of the groups we want to ignore
                    if (submenu_text in self.baseline.docs) and not self.baseline.docs[submenu_text]:
                        ignore = True
            else:
                if isinstance(self.tabs, list) and submenu_text not in self.tabs:
                    ignore = True
                elif submenu_text in IGNORE_MENUS and self.ignore_non_core:
                    # .. skip all non-"standard" menus
                    ignore = True
                if False and debugger() and submenu_text not in RELEVANT_MENUS:
                    ignore = True
            if ignore:
                # .. skip
                log('skipping', level=logging.INFO)
                # .. but yield an empty list, so that we at least have a marker for that section
                yield SectionDoc(menu_text=submenu_text,
                                 methods=list())
                continue

            log(f'Extracting methods from "{submenu_text}" menu', level=logging.INFO)

            log('start')
            log('click()')

            # click on the submenu on the left
            submenu.click()

            # after clicking on the submenu we need to wait for a new api reference container to show up
            try:
                for i in range(3):
                    try:
                        api_reference_container, header = WebDriverWait(driver=self.driver, timeout=10).until(
                            method=wait_for_new_api_reference_container())
                    except StaleElementReferenceException:
                        if i < 2:
                            continue
                        raise
                    else:
                        break
            except TimeoutException:
                api_reference_container = None
                log('!!!!! Timeout waiting for documentation window to show up !!!!!', level=logging.ERROR)
                continue
            api_reference_container: WebElement
            header: str

            # set the new header (needed when waiting for the next container)
            # noinspection PyUnboundLocalVariable
            prev_container_header = header

            # noinspection PyUnboundLocalVariable
            soup = BeautifulSoup(api_reference_container.get_attribute('outerHTML'), 'html.parser')
            header = soup.div.div.h3.text
            doc = '\n'.join(p.text for p in soup.div.div.find_all('p'))
            yield SectionDoc(menu_text=submenu.text,
                             header=header,
                             doc=doc,
                             methods=list(self.methods_from_api_reference_container(
                                 container=soup,
                                 header=submenu.text)))
            log('end')
        return

    def get_section_docs(self) -> list[SectionDoc]:
        """
        Read developer.webex.com and get doc information for all endpoints under requested section "Calling"
        """
        url = 'https://developer.webex.com/docs'

        def log(text: str, level: int = logging.DEBUG):
            self.log(level=level, msg=f'navigate_to_calling_reference: {text}')

        log(f'opening "{url}"')
        self.driver.get(url)

        # wait max 10 seconds for accept cookies button to show up and be steady

        log('waiting for button to accept cookies')

        def steady(locator):
            """
            Wait for a web element to be:
                * visible
                * enabled
                * steady: same position at two consecutive polls
            :param locator:
            :return: False or web element
            """
            #: mutable to cache postion of element
            mutable = {'pos': dict()}

            def log(text: str):
                self.log(f'steady: {text}')

            def _predicate(driver):
                target = driver.find_element(*locator)
                target = EC.visibility_of(target)(driver)
                if target and target.is_enabled():
                    target: WebElement
                    pos = target.location
                    log(f'prev pos: {mutable["pos"]}, pos: {pos}')
                    if mutable['pos'] == pos:
                        return target
                    mutable['pos'] = pos
                else:
                    log('not visible or not enabled')
                return False

            return _predicate

        try:
            # wait for button to accept cookies to be steady
            accept_cookies = WebDriverWait(driver=self.driver, timeout=10).until(
                method=steady((By.ID, 'onetrust-consent-sdk')))
        except TimeoutException:
            # if there is no accept cookies button after 10 seconds then we are probably ok
            log('No popup to accept cookies', level=logging.WARNING)
        else:
            accept_cookies: WebElement
            # there is a button in there that we need to click
            # button = accept_cookies.find_element(by=By.TAG_NAME, value='button')
            button = None
            try:
                button = accept_cookies.find_element(by=By.ID, value='onetrust-accept-btn-handler')
            except NoSuchElementException:
                pass
            if button is None:
                try:
                    button = accept_cookies.find_element(by=By.XPATH,
                                                         value='//*[@id="onetrust-close-btn-container"]/button')
                except NoSuchElementException:
                    pass
            if button is not None:
                log('accept cookies')
                button.click()

        # try:
        #     # wait for button to accept cookies to be steady
        #     accept_cookies = WebDriverWait(driver=self.driver, timeout=10).until(
        #         method=steady((By.ID, 'onetrust-accept-btn-handler')))
        # except TimeoutException:
        #     # if there is no accept cookies button after 10 seconds then we are probably ok
        #     log('No popup to accept cookies', level=logging.WARNING)
        # else:
        #     accept_cookies: WebElement
        #     # there is a button in there that we need to click
        #     button = accept_cookies
        #     # button = accept_cookies.find_element(by=By.TAG_NAME, value='button')
        #     log('accept cookies')
        #     button.click()

        if self.credentials:
            self.login()

        log(f'looking for "{self.section}"')
        section = self.by_class_and_text(find_in=self.driver,
                                         class_name='md-list-item__center',
                                         text=self.section)
        log(f'clicking on "{self.section}"')
        section.click()

        if self.section == 'Full API Reference':
            # wait for a sidebar group to be present
            reference_nav_group = WebDriverWait(driver=self.driver, timeout=10).until(
                method=EC.presence_of_element_located((By.CLASS_NAME, 'md-sidebar-nav__group--expanded')))
        else:
            # after clicking on section an expanded nav group exists
            log('looking for expanded sidebar nav group')
            section_nav_group = WebDriverWait(driver=self.driver, timeout=10).until(
                method=EC.presence_of_element_located((By.CLASS_NAME, 'md-sidebar-nav__group--expanded')))

            # in that nav group we want to click on "Reference"
            log('looking for "Reference" in expanded sidebar group')
            reference = self.by_class_and_text(find_in=section_nav_group,
                                               class_name='md-list-item__center',
                                               text='Reference')
            log('clicking on "Reference"')
            reference.click()

            # After clicking on "Reference" a new expanded nav group should exist
            log('Looking for expanded sidebar nav group under "Calling"')
            reference_nav_group = next(iter(section_nav_group.find_elements(by=By.CLASS_NAME,
                                                                            value='md-sidebar-nav__group--expanded')))
        log('Collecting menu items in "Reference" sidebar group')
        reference_items = reference_nav_group.find_elements(by=By.CLASS_NAME, value='md-submenu__item')
        log(f"""menu items in "Reference" sidebar group: {', '.join(f'"{smi.text}"' for smi in reference_items)}""")

        docs = list(self.docs_from_submenu_items(reference_items))
        return docs

    def param_parser(self, divs: Iterable[Tag], level: int = 0, path: str = '') -> Generator[Parameter, None, None]:
        """
        Parse parameters from divs
        :param divs:
        :param level:
        :param path:
        :return:
        """

        param_div = None
        name = None

        def log(msg: str, div: Tag = None, log_level: int = logging.DEBUG):
            div = div or param_div
            name_str = name and f'"{name}", ' or ""
            self.log(f'      {" " * level}param_parser({path}{div_repr(div)}): {name_str}{msg}',
                     level=log_level)

        def div_generator(div_list: list[Tag]) -> Generator[Tag, None, None]:
            """
            Generator for divs to consider in parser

            The generator takes care of climbing down div hierarchies and trying to hide other "anomalies" from the
            parser
            :param div_list:
            :return:
            """
            for tag in div_list:
                div = tag
                yield_div = True
                while True:
                    if div.attrs.get('class', None) is None:
                        log('div_generator: classless div->yield immediately')
                        break

                    # also yield divs indicating an object
                    if classes := self.obj_class(div):
                        log(f'div_generator: div indicating an object({next(iter(classes))})->yield immediately')
                        break

                    # if this div only has one div child then go one down
                    # for a parameter we expect two child divs
                    if len(div.find_all('div', recursive=False)) == 1:
                        div = div.div
                        log('div_generator: div with single div child. moved one down')
                        continue
                    # if there is a button then go one down
                    if div.find('button', recursive=False):
                        div = div.div
                        log('div_generator: found a button, went one down')
                        continue
                    """
                    if we have a list of classless divs as childs then yield the childs
                    example:
                        <div class="emjDUw5LqTp3QCCg4hNp">
                            <div class="bfIcOqrr0LEmWxjEID2z">
                                <div class="Sj3x8PGVKM_DQu1MaOpF">
                                    <div>
                                        <div class="bfIcOqrr0LEmWxjEID2z">
                                            <div class="ETdjpkOd18yDmr_Pomer">
                                                <div class="AzemgtvlBWwLVUYkRkbg">id</div>
                                                <div class="Xjm2mpYxY4YHNn4XsTBg"><span>string</span><span
                                                class="buEuRUqtw7z8xim5DxxA">required</span>
                                                </div>
                                            </div>
                                            <div class="Sj3x8PGVKM_DQu1MaOpF"><p>Unique ID for the rule.</p></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div class="bfIcOqrr0LEmWxjEID2z">
                                            <div class="ETdjpkOd18yDmr_Pomer">
                                                <div class="AzemgtvlBWwLVUYkRkbg">enabled</div>
                                                <div class="Xjm2mpYxY4YHNn4XsTBg"><span>boolean</span></div>
                                            </div>
                                            <div class="Sj3x8PGVKM_DQu1MaOpF"><p>Reflects if rule is enabled.</p></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    """
                    if (childs := div.find_all('div', recursive=False)) and all(child.attrs.get('class', None) is None
                                                                                for child in childs):
                        log('div_generator: list of classless child divs -> yield divs from childs')
                        for child in childs:
                            child: Tag
                            yield from child.find_all('div', recursive=False)
                        yield_div = False
                    break
                if yield_div:
                    yield div
            return

        log(f'start: divs({len(divs)}): {", ".join(map(div_repr, divs))}')
        div_iter = div_generator(divs)
        param_div = next(div_iter, None)
        while param_div:
            name = None
            # a classless div is a wrapper for a list of attributes
            if param_div.attrs.get('class', None) is None:
                # yield members of classless div
                all_divs = param_div.find_all('div', recursive=False)
                yield from self.param_parser(all_divs,
                                             level=level)
                # and then continue with the next
                param_div = next(div_iter, None)
                continue

            # special case: a div w/o child divs and just two spans
            if not param_div.find_all('div', recursive=False):
                spans = param_div.find_all('span', recursive=False)
                if len(spans) == 2:
                    yield Parameter(name=spans[0].text,
                                    type='',
                                    doc=f'{spans[0].text}{spans[1].text}')
                param_div = next(div_iter, None)
                continue

            param_attrs = None
            param_object = None

            # the div should have two child divs:
            #   * attribute name and type
            #   * attribute doc string
            child_divs = param_div.find_all('div', recursive=False)
            log(f'child divs({len(child_divs)}): {", ".join(map(div_repr, child_divs))}')

            if len(child_divs) == 2:
                """
                Parse something like this
                    <div class="bfIcOqrr0LEmWxjEID2z">
                        <div class="ETdjpkOd18yDmr_Pomer">
                            <div class="AzemgtvlBWwLVUYkRkbg">personId</div>
                            <div class="Xjm2mpYxY4YHNn4XsTBg"><span>string</span><span
                            class="buEuRUqtw7z8xim5DxxA">required</span></div>
                        </div>
                        <div class="Sj3x8PGVKM_DQu1MaOpF"><p>Unique identifier for the person.</p></div>
                    </div>
                """
                param_div, p_spec_div = child_divs

                # get attribute name and type
                child_divs = param_div.find_all('div', recursive=False)
                log(f'param child divs({len(child_divs)}): {", ".join(map(div_repr, child_divs))}')
                assert len(child_divs) == 2
                name_div, type_div = child_divs
                name = name_div.text

                # type information has type and addtl. spec in spans
                spans = type_div.find_all('span', recursive=False)
                log(f'# of spans in type spec: {len(spans)}')
                assert len(spans) and len(spans) <= 2
                param_type = spans[0].text
                log(f'parameter type: {param_type}')
                if len(spans) == 2:
                    type_spec = spans[1].text
                else:
                    type_spec = None

                # catch "callOfferToneEnabled `true`"
                if param_type == 'boolean' and len(name.split()) > 1:
                    name = name.split()[0]

                # doc is in the second div
                # get all <p> and <ul> tags and build doc from that
                # * each <p> is a line
                # * each <p> in each <li> of each <ul> is a line prefixed by "* "
                # stop as soon as a any other tag is hit
                def doc_lines_from_p_spec():
                    for child in p_spec_div.children:
                        child: Tag
                        if child.name == 'p':
                            yield child.text
                            ...
                        elif child.name == 'ul':
                            for ul_child in child.children:
                                ul_child: Tag
                                if ul_child.name != 'li':
                                    raise KeyError(f'Unexpected child of <ul>: {ul_child.name}')
                                yield f"* {' '.join(ul_child.strings)}"
                        else:
                            break
                    return

                new_doc = '\n'.join(doc_lines_from_p_spec())

                doc_paragraphs = p_spec_div.find_all('p', recursive=False)
                doc = '\n'.join(map(lambda p: p.text, doc_paragraphs))

                assert new_doc.startswith(doc)
                doc = new_doc
                # for an enum the second div can have a list of enum values
                child_divs = p_spec_div.find_all('div', recursive=False)
                if child_divs:
                    log(f'divs in second div of parameter parsed ({len(child_divs)}): '
                        f'{", ".join(map(div_repr, child_divs))}')
                    param_attrs = list(self.param_parser(child_divs, level=level + 1)) or None
                    if param_attrs and len(param_attrs) == 1 and not any(
                            (param_attrs[0].param_attrs, param_attrs[0].param_object)):
                        # a single child attribute without childs doesn't make any sense
                        # instead add something to the doc string
                        doc_line = param_attrs[0].doc.strip()
                        log(f'single child attribute doesn\'t make sense. Adding line to documentation: "{doc_line}"')
                        doc = '\n'.join((doc.strip(), doc_line))
                        param_attrs = None
            elif len(child_divs) < 3:
                # to short: not idea what we can do here....
                log(f'to few divs: {len(child_divs)}: skipping')
                param_div = next(div_iter, None)
                continue
            else:
                """
                Special case:
                    <div class="emjDUw5LqTp3QCCg4hNp">
                        <div class="AzemgtvlBWwLVUYkRkbg">primary</div>
                        <div class="Xjm2mpYxY4YHNn4XsTBg"><span>boolean</span></div>
                        <div class="Sj3x8PGVKM_DQu1MaOpF"><p>Flag to indicate if the number is primary or
                        not.</p></div>
                        <div class="Mo4RauPOboRxtDGO9VvT"><span>Possible values: </span><span></span></div>
                    </div>
                """
                childs = iter(child_divs)

                # get name of attribute from 1st div
                # <div class="AzemgtvlBWwLVUYkRkbg">primary</div>
                name = next(childs).text
                log(f'got name "{name}"')
                log('flat sequence of divs')

                # next div has a list of spans ...
                # <div class="Xjm2mpYxY4YHNn4XsTBg"><span>boolean</span></div>
                spans = iter(next(childs).find_all('span', recursive=False))

                # .. and the 1st span has the type
                param_type = next(spans).text
                log(f'got parameter type "{param_type}"')

                # ... if there is still one span then that's the type spec
                span = next(spans, None)
                type_spec = span and span.text
                log(f'got type spec "{type_spec}"')

                # the next div has a list of paragraphs with the documentation
                # <div class="Sj3x8PGVKM_DQu1MaOpF"><p>Flag to indicate if the number is primary or not.</p></div>
                doc = '\n'.join(p.text
                                for p in next(childs).find_all('p', recursive=False))
                log(f'got doc "{doc[:30]}..."')

                # there might be one more div
                # <div class="Mo4RauPOboRxtDGO9VvT"><span>Possible values: </span><span></span></div>
                div = next(childs, None)
                if div:
                    # if this div is of the same class as the parameter div then we take this div and all following
                    # divs of the same class as attributes of this param
                    param_div_classes = set(param_div.attrs.get('class'))
                    assert param_div_classes
                    div_classes = set(div.attrs.get('class'))
                    common_classes = div_classes & param_div_classes
                    if common_classes:
                        attr_divs = [div] + list(childs)
                        log(f'parsing remaining {len(attr_divs)} child divs as parameter attributes: '
                            f'{",".join(map(div_repr, attr_divs))}')
                        param_attrs = list(self.param_parser(attr_divs,
                                                             level=level + 1)) or None
                    elif spans := div.find_all('span', recursive=False):
                        # ... with a list of spans; add the text in these spans to the doc
                        spans = iter(spans)
                        try:
                            doc_line = f'{next(spans).text}{", ".join(t for s in spans if (t := s.text))}'
                        except StopIteration:
                            pass
                        log(f'enhancing doc string: "{doc_line}"')
                        doc = '\n'.join((doc, doc_line))
                    else:
                        raise NotImplementedError('No idea what to do with this div')
                # now all childs should be consumed
                unconsumed_childs = list(childs)
                if unconsumed_childs:
                    raise NotImplementedError('Not all child divs consumed')
            # if

            # look ahead to next div
            param_div = next(div_iter, None)
            if param_div:
                # check if class is one of the param classes
                if classes := self.obj_class(param_div):
                    log(f'parsing next div ({next(iter(classes))}) as part of this parameter')
                    # this enhances the current parameter
                    obj_attributes = list(self.param_parser(param_div.find_all('div', recursive=False),
                                                            level=level + 1)) or None
                    if 'params-type-non-object' in classes:
                        assert param_attrs is None
                        param_attrs = obj_attributes
                    else:
                        param_object = obj_attributes
                    # move to next div
                    param_div = next(div_iter, None)
                # if
            # if

            # ignore string parameters with invalid names
            # we can keep spaces and slashes. These will be transformed to correct names when creating the classes
            if not re.match(r'^[^0-9#][\w\s/]*$', name):
                if name == '#':
                    name = 'hash'
                elif name in '0123456789':
                    name = f'digit_{name}'
                elif len(name.split()) > 1:
                    log(f'ignoring parameter name "{name}"', log_level=logging.WARNING)
                    continue

            if param_type == 'enum' and not param_attrs and not param_object:
                log('type "enum" without attributes transformed to "string"')
                param_type = 'string'

            log(f'yield type={param_type}, type_spec={type_spec}, '
                f'param_attrs={param_attrs and len(param_attrs) or 0}, '
                f'param_object={param_object and len(param_object) or 0}')
            yield Parameter(name=name,
                            type=param_type,
                            type_spec=type_spec,
                            doc=doc,
                            param_attrs=param_attrs,
                            param_object=param_object)
        # while
        return

    def params_and_response_from_divs(self, divs: ResultSet) -> dict[str, list[Parameter]]:
        """
        Extract params and response properties from child divs of api-reference__description
        :param divs:
        :return:
        """

        def log(msg: str):
            self.log(f'    params_and_response_from_divs: {msg}')

        log('start')
        result: dict[str, list[Parameter]] = {}
        for div in divs:
            # each div has one or more h6 headers and the same number of divs of class vertical-up with the parameter
            # information
            if div.attrs.get('class', None) is None:
                # navigate one level down if encapsulated in an empty div: this is the case for "Response Properties"
                div = div.div
                log(f'navigating one level down from <div> to {div_repr(div)}')
                if div is None:
                    # apparently this was an empty div; we are done here
                    continue
            headers = div.find_all(name='h6', recursive=False)
            parameter_groups = div.find_all(class_='vertical-up', recursive=False)
            assert len(headers) == len(parameter_groups)
            log(f"""{div_repr(div)}: headers({len(headers)}): {", ".join(map(lambda h: f'"{h.text}"', headers))}""")

            for header, parameters in zip(headers, parameter_groups):
                if False and debugger() and header.text != 'Body Parameters':
                    continue
                # each parameter spec is in one child div
                child_divs = parameters.find_all(name='div', recursive=False)
                log(f'{div_repr(div)}, header("{header.text}"). child divs({len(child_divs)}): '
                    f'{", ".join(map(div_repr, child_divs))}')
                # parsed_params = list(map(self.parse_param, child_divs))
                parsed_params = list(self.param_parser(child_divs))
                result[header.text] = parsed_params
        log('end')
        return result

    def get_method_details(self, method_doc: MethodDoc) -> Optional[MethodDetails]:
        """
        Get details for one method

        :param method_doc:
        :return:
        """

        def log(msg: str, level: int = logging.DEBUG):
            self.log(f'  get_method_details("{method_doc.doc}"): {msg}',
                     level=level)

        if False and debugger() and method_doc.doc != "Retrieve a person's Outgoing Calling Permissions Settings":
            # skip
            return

        log('', level=logging.INFO)

        doc_link = method_doc.doc_link

        # sometimes links have a superfluous trailing dot
        # we try the original URL 1st and retry w/p trailing dots
        while True:
            # navigate to doc url of method
            log(f'GET {doc_link}')
            self.driver.get(doc_link)

            # we don't need to click on anything. Hence we can just extract from static page using BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            api_ref_descr = soup.find(class_='api-reference__description')
            """ API reference description is something like:
                    <div class="columns u_6eoYxPfVMJxwlI0Wcb large-6 xlarge-6 api-reference__description
                    XdQBFUuam5J29sqNCtir">
                        <div class="K_M3cdOQTnTLnPOWhtqe"><h4>Read Person's Calling Behavior</h4>
                            <div><p>Retrieves the calling behavior and UC Manager Profile settings for the person which
                            includes overall
                                calling behavior and calling UC Manager Profile ID.</p>
                                <p>Webex Calling Behavior controls which Webex telephony application and which UC
                                Manager
                                Profile is to be
                                    used for a person.</p>
                                </div>
            """
            if not api_ref_descr:
                if doc_link.endswith('.'):
                    log(f'GET {doc_link} failed. Retry w/o trailing "."',
                        level=logging.WARNING)
                    doc_link = doc_link.strip('.')
                    continue
                log('GET failed? API reference description not found on page', level=logging.ERROR)
                return None
            break
        # while

        try:
            header = api_ref_descr.div.h4.text
        except AttributeError:
            log('Failed o parse header from api spec',
                level=logging.ERROR)
            return None

        log(f'header from API reference description: "{header}"')

        # long doc string can have multiple paragraphs
        doc_paragraphs = api_ref_descr.div.div.find_all(name='p', recursive=False)
        assert doc_paragraphs
        long_doc_string = '\n'.join(dp.text for dp in doc_paragraphs)

        # parameters and response values are in the divs following the 1st one. The last div has response codes
        # hence to get parameters and response codes we can skip the 1st and last div
        divs = api_ref_descr.find_all(name='div', recursive=False)

        divs = divs[1:-1]

        log(f'child divs for parameters and response: {", ".join(map(div_repr, divs))}')
        params_and_response = self.params_and_response_from_divs(divs)
        result = MethodDetails(header=header,
                               doc=long_doc_string,
                               parameters_and_response=params_and_response,
                               documentation=method_doc)
        log('end')
        return result

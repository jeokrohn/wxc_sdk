import logging
from collections import defaultdict
from collections.abc import Generator
from dataclasses import dataclass, field
from functools import partial
from itertools import chain
from operator import attrgetter
from re import subn, sub
from typing import Any, Optional

__all__ = ['PythonClass', 'PythonClassRegistry', 'Attribute', 'Endpoint', 'Parameter']

import dateutil.parser

from apib.apib import ApibDatastructure, ApibObject, ApibEnum, ApibParseResult, ApibMember, words_to_camel
from apib.apib.classes import snake_case
from wxc_sdk.base import to_camel

log = logging.getLogger(__name__)

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
    docstring: str
    sample: Any
    optional: bool


@dataclass
class Endpoint:
    name: str
    method: str = field(default=None)
    url: str = field(default=None)
    href_parameter: list[Parameter] = field(default_factory=list)
    body_parameter: list[Parameter] = field(default_factory=list)
    result: str = field(default=None)


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

    # TODO: is this still needed?
    # @classmethod
    # def data_structure_class_attributes(cls, ds: ApibDatastucture) -> Generator['Attribute', None, None]:
    #     if not ds.is_class:
    #         return
    #     if ds.superclass:
    #         members = ds.content.content
    #     else:
    #         members = ds.content.content
    #     if not members:
    #         return
    #     for member in members:
    #         yield Attribute.from_member(ds.python_name, member)

    @classmethod
    def from_enum(cls, enum_element: ApibEnum) -> Generator['Attribute', None, None]:
        """
        Generator for attributes from an ApibEnum
        """
        for e in enum_element.enumerations:
            yield Attribute(name=e.content, python_type=simple_python_type(e.element),
                            docstring=e.description, sample=None, referenced_class=None)

    def source(self, for_enum: bool) -> str:
        if self.docstring:
            lines = [f'#: {ls}' for line in self.docstring.strip().splitlines()
                     if (ls := line.strip())]
        else:
            lines = []
        if for_enum:
            name = snake_case(self.name)
            if name == 'none':
                name = 'none_'
            name, _ = subn(r'[^a-z0-9]', '_', name)
            name = sub('^([0-9])', '_\\1', name)
            value = self.name
            value = value.replace("'", '')
            lines.append(f"{name} = '{value}'")
            foo = 1
        else:
            attr_name = snake_case(self.name)
            if attr_name in {'from'}:
                attr_name = f'{attr_name}_'
            if self.sample:
                lines.append(f'#: example: {self.sample}')
            line = f'{attr_name}: Optional[{self.python_type}]'
            if to_camel(attr_name) == self.name:
                line = f'{line} = None'
            else:
                line = f"{line} = Field(alias='{self.name}', default=None)"
            lines.append(line)
        return '\n'.join(lines)


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

    def source(self) -> Optional[str]:
        """
        Source code for this class or None
        """
        if self.baseclass and not self.attributes:
            return None
        baseclass = ''
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

    @classmethod
    def from_data_structure(cls, ds: ApibDatastructure) -> Generator['PythonClass', None, None]:
        """
        :return:
        """
        # content can be 'object' or 'enum'
        content = ds.content
        content_element = content and content.element
        python_name = ds.python_name
        baseclass = ds.baseclass
        if not content_element:
            raise ValueError('content element should not be None')
        elif content_element == 'object':
            content: ApibObject
            # get attributes from object content
            classes, attributes = python_class_attributes(basename=ds.python_name,
                                                          members=content.content)
            yield from classes
            yield PythonClass(name=python_name, attributes=attributes, description=None, is_enum=False,
                              baseclass=baseclass)

        elif content_element == 'enum':
            content: ApibEnum
            attributes = list(Attribute.from_enum(content))
            yield PythonClass(name=python_name, attributes=attributes, is_enum=True)
        else:
            classes, attributes = python_class_attributes(basename=ds.python_name,
                                                          members=content.content)
            yield from classes
            yield PythonClass(name=python_name, attributes=attributes, description=None, is_enum=False,
                              baseclass=baseclass)

    @classmethod
    def from_parse_result(cls, parse_result: ApibParseResult) -> Generator['PythonClass', None, None]:
        """
        All Python classes (implicit and explict and classes used in results of endpoint calls)
        """
        for ds in parse_result.api.data_structures():
            yield from PythonClass.from_data_structure(ds)

        # also go through transitions and look at response datastructures
        for transition in parse_result.api.transitions():
            response = transition.http_transaction.response
            ds = response and response.datastructure
            if ds:
                yield from PythonClass.from_data_structure(ds)


@dataclass
class PythonClassRegistry:
    _classes: dict[str, PythonClass] = field(default_factory=dict, repr=False)

    def add(self, pc: PythonClass):
        self._classes[pc.name] = pc

    def get(self, class_name: str)->Optional[PythonClass]:
        if pc := self._classes.get(class_name):
            _, pc = self.dereferenced_class(pc.name)
        return pc

    def classes(self) -> Generator[PythonClass, None, None]:
        visited = set()

        def yield_from_classname(class_name: Optional[str]) -> Generator[PythonClass, None, None]:
            if class_name is None:
                return

            # descend down into baseclasses if there are no attributes
            _, c = self.dereferenced_class(class_name)
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

    def dereferenced_class(self, class_name) -> tuple[str, Optional[PythonClass]]:
        while True:
            pc = self._classes.get(class_name)
            if not pc:
                log.error(f'class "{class_name}" not found')
                return class_name, None
            if pc.baseclass and not pc.attributes:
                class_name = pc.baseclass
                continue
            return class_name, pc

    def dereferenced_class_name(self, class_name) -> str:
        class_name, _ = self.dereferenced_class(class_name)
        return class_name

    def attribute_python_type(self, attribute: Attribute):
        if not attribute.referenced_class:
            return attribute.python_type
        class_name = self.dereferenced_class_name(attribute.referenced_class)
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
                    attr1_type = self.attribute_python_type(attr1)
                    attr2_type = self.attribute_python_type(attr2)
                    if attr1_type == attr2_type:
                        # attributes are identical
                        continue

                    # maybe both attributes reference equivalent classes?
                    if not all((attr1.referenced_class, attr2.referenced_class)):
                        return False
                    class1, ref1 = self.dereferenced_class(attr1.referenced_class)
                    class2, ref2 = self.dereferenced_class(attr2.referenced_class)
                    if not all((ref1, ref2)) or not classes_equivalent(ref1, ref2):
                        return False

                    # check the python types of both attributes again
                    attr1_type = self.attribute_python_type(attr1)
                    attr2_type = self.attribute_python_type(attr2)
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
            list(map(self.attribute_python_type, pc.attributes))
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


def simple_python_type(type_hint: str, value: Any=None) -> str:
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


def classes_and_attribute_from_member(class_name: str, member: ApibMember) \
        -> tuple[list['PythonClass'], Attribute]:
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
        elif array_element_type == 'number':
            content = value.content[0]
            python_type = f'list[{content.content.__class__.__name__}]'
            sample = f'[{", ".join(f"{c.content}" for c in value.content)}]'
        elif array_element_type == 'object':
            # array of some object
            if not isinstance(value.content, list) or len(value.content) != 1:
                raise ValueError(f'Well, this is unwxpdected: {value.content}')
            content: ApibObject = value.content[0]
            referenced_class = f'{class_name}{name[0].upper()}{name[1:]}'
            python_type = f'list[{referenced_class}]'
            new_classes, class_attributes = python_class_attributes(basename=referenced_class,
                                                                    members=content.content)
            classes.extend(new_classes)
            classes.append(PythonClass(name=referenced_class, attributes=class_attributes,
                                       description=value.description, is_enum=False, baseclass=None))
        elif array_element_type == 'enum':
            # array of enum
            if not isinstance(value.content, list) or len(value.content) != 1:
                raise ValueError(f'Well, this is unexpected: {value.content}')
            # create enum on the fly
            content: ApibEnum = value.content[0]
            referenced_class = f'{class_name}{name[0].upper()}{name[1:]}'
            python_type = f'list[{referenced_class}]'
            class_attributes = list(Attribute.from_enum(content))
            classes.append(PythonClass(name=referenced_class, attributes=class_attributes,
                                       description=value.description, is_enum=True, baseclass=None))
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
        class_attributes = list(Attribute.from_enum(value))
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


def python_class_attributes(basename: str, members: list[ApibMember]) -> tuple[list[PythonClass], list[Attribute]]:
    classes = []
    attributes = []
    if not members:
        return classes, attributes
    for member in members:
        new_classes, attribute = classes_and_attribute_from_member(basename, member)
        classes.extend(new_classes)
        if attribute:
            attributes.append(attribute)
    return classes, attributes

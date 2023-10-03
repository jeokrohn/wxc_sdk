import logging
import re
from collections import defaultdict
from collections.abc import Generator
from dataclasses import dataclass, field
from functools import partial
from itertools import chain
from operator import attrgetter
from re import subn, sub
from typing import Any, Optional

__all__ = ['PythonClass', 'PythonClassRegistry', 'Attribute', 'Endpoint', 'Parameter', 'simple_python_type']

import dateutil.parser

from apib.apib import ApibDatastructure, ApibObject, ApibEnum, ApibParseResult, ApibMember, words_to_camel
from apib.apib.classes import snake_case
from wxc_sdk.base import to_camel

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

    @property
    def python_name(self) -> str:
        """
        A Python compatible name. Reserved Python names are suffixed with an underscore
            from -> from_
        """
        if self.name in RESERVED_PARAM_NAMES:
            return f'{self.name}_'
        return self.name


@dataclass
class Endpoint:
    name: str
    method: str = field(default=None)
    url: str = field(default=None)
    href_parameter: list[Parameter] = field(default_factory=list)
    body_parameter: list[Parameter] = field(default_factory=list)
    result: str = field(default=None)
    result_referenced_class: str = field(default=None)


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
    _context: str = field(default='', repr=False)

    # registered classes
    _classes: dict[str, PythonClass] = field(default_factory=dict, repr=False)

    def __init__(self):
        self._context = None
        self._classes = dict()

    def set_context(self, context: str):
        self._context = context

    def qualified_class_name(self, class_name: str)->str:
        """
        Get qualified identified for given class name
        """
        if '%' in class_name:
            return class_name
        return f'{self._context}%{class_name}'

    def add(self, pc: PythonClass):
        """
        Add a python class to the registry. When adding the class name to the registry pc.name gets updated to a
        qualident.
        pc.name has to be unique
        """
        qualident = self.qualified_class_name(pc.name)
        if qualident in self._classes:
            raise KeyError(f'python class name "{pc.name}" already registered')

        pc.name = qualident
        self._classes[pc.name] = pc

    def get(self, class_name: str) -> Optional[PythonClass]:
        if pc := self._classes.get(class_name):
            _, pc = self._dereferenced_class(pc.name)
        return pc

    def _python_class_attributes(self, basename: str, members: list[ApibMember]) -> list[Attribute]:
        attributes = []
        if not members:
            return attributes
        for member in members:
            attribute = self.attribute_from_member(basename, member)
            if attribute:
                attributes.append(attribute)
        return attributes

    def attribute_from_member(self, class_name: str, member: ApibMember) -> Attribute:
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

                self.add(new_class)
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
                self.add(new_class)
                python_type = f'list[{new_class.name}]'
            else:
                # array of some type
                # references class is that type
                referenced_class = array_element_type
                # .. and the Python type is a list of that type
                python_type = f'list[{referenced_class}]'
        elif value.element == 'object':
            # we need a class with these attributes
            python_type = f'{class_name}{name[0].upper()}{name[1:]}'
            python_type, _ = re.subn(r'[^\w_]', '', python_type)
            sample = None
            referenced_class = python_type
            class_attributes = self._python_class_attributes(basename=referenced_class, members=value.content)
            new_class = PythonClass(name=referenced_class, attributes=class_attributes,
                                    description=value.description, is_enum=False, baseclass=None)
            self.add(new_class)
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
            python_type, _ = re.subn(r'[^\w_]', '', python_type)
            sample = value.content and value.content.content
            referenced_class = python_type
            class_attributes = list(Attribute.from_enum(value))
            new_class = PythonClass(name=referenced_class, attributes=class_attributes,
                                    description=value.description, is_enum=True, baseclass=None)
            self.add(new_class)
            python_type = new_class.name
        elif value.element == 'boolean':
            python_type = 'bool'
            sample = value.content
        else:
            # this might be a reference to a class
            python_type = value.element
            referenced_class = python_type
            try:
                sample = value.content and value.content.content
            except AttributeError:
                sample = None
        if referenced_class:
            referenced_class = self.qualified_class_name(referenced_class)
        return Attribute(name=name, python_type=python_type, docstring=docstring, sample=sample,
                         referenced_class=referenced_class)

    def add_classes_from_data_structure(self, ds: ApibDatastructure, class_name: str = None) -> PythonClass:
        """
        Add classes defined in a given APIB datastructure
        """
        # content can be 'object' or 'enum'
        content = ds.content
        content_element = content and content.element
        class_name = class_name or ds.class_name
        if not class_name:
            raise ValueError('Undefined class name')
        baseclass = ds.baseclass
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
            baseclass = baseclass and self.qualified_class_name(baseclass)
            pc = PythonClass(name=class_name, attributes=attributes, description=None, is_enum=False,
                                 baseclass=baseclass)
        self.add(pc)
        return pc

    def add_classes_from_parse_result(self, parse_result: ApibParseResult) -> Generator['PythonClass', None, None]:
        """
        All Python classes (implicit and explict and classes used in results of endpoint calls)
        """
        for ds in parse_result.api.data_structures():
            self.add_classes_from_data_structure(ds)

        # also go through transitions and look at response datastructures
        for transition in parse_result.api.transitions():
            response = transition.http_transaction.response
            ds = response and response.datastructure
            if not ds:
                continue

            # skip datastructures w/o attributes
            if not ds.attributes:
                continue
            self.add_classes_from_data_structure(ds)

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
            python_class_name = words_to_camel(pc.name.split('%')[-1])
            # disambiguate class names by appending an index
            python_class_name = next((pn for suffix in chain([''], (str(i) for i in range(1, 100)))
                                      if (pn:=f'{python_class_name}{suffix}') not in python_names))
            # keep record of the Python class name
            python_names.add(python_class_name)
            qualident_to_python_name[qualident] = python_class_name

        # now go through all classes and clean up references from qualidents to Python names
        for qualident, python_class_name in qualident_to_python_name.items():
            pc = self._classes.pop(qualident)
            pc.name = python_class_name
            pc.baseclass = pc.baseclass and qualident_to_python_name[pc.baseclass]
            if pc.attributes:
                for attr in pc.attributes:
                    if attr.referenced_class:
                        new_class_name = qualident_to_python_name[attr.referenced_class]
                        attr.python_type = attr.python_type.replace(attr.referenced_class, new_class_name)
                        attr.referenced_class = new_class_name
            self._classes[python_class_name] = pc

        # TODO: how do we update endpoints?

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

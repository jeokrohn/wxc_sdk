"""
Class Python class registry for code generation
"""
import re
from _operator import attrgetter
from collections import defaultdict
from dataclasses import dataclass, field
from functools import partial
from itertools import chain
from typing import Optional, Iterable, Generator, Union

from apib.apib import ApibMember, ApibOption, ApibObject, ApibEnum, ApibDatastructure, ApibParseResult, ApibElement, \
    ApibSelect, ApibString, ApibBool, ApibNumber, ApibArray
from apib.python_class import PythonClass, PythonAPI, log, Endpoint, Attribute, guess_datetime_or_int, Parameter
from apib.tools import sanitize_class_name, words_to_camel, snake_case, simple_python_type


@dataclass(init=False, repr=False)
class PythonClassRegistry:
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

    def _add_api(self, *, python_api: PythonAPI, apib_key: str=None):
        if apib_key is None:
            apib_key = self._context
        if apib_key in self._apis:
            raise KeyError(f'"{apib_key}" already has an API registered')
        self._apis[apib_key] = python_api

    def apis(self) -> Iterable[tuple[str, PythonAPI]]:
        return self._apis.items()

    def _add_class(self, pc: PythonClass):
        """
        Add a python class to the registry. When adding the class name to the registry pc.name gets updated to a
        qualident.
        pc.name has to be unique; this is ensured here
        """
        qualident = self.qualified_class_name(sanitize_class_name(pc.name))
        if qualident in self._classes:
            log.warning(f'python class name "{pc.name}" already registered')
            qualident = next((name
                              for i in range(1, 100)
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
        if member.element == 'select':
            sample = None
            options: list[ApibOption] = [option for option in member.content]
            python_types = [simple_python_type(option.content.value.element, option.content.value.content) for option in
                            options]
            python_type = f'Union[{", ".join(python_types)}]'
            docstring = None
            referenced_class = None
            optional = False
            name = options[0].content.key
        elif member.element != 'member':
            log.warning(f'Not implemented, member element: {member.element}')
            # TODO: implement this case
            raise NotImplementedError
        else:
            name = member.key
            value = member.value
            docstring = member.meta and member.meta.description
            referenced_class = None
            optional = 'optional' in member.type_attributes
            if value.element == 'string':
                sample = value.content
                # could be a datetime
                sample, python_type = guess_datetime_or_int(sample, 'string')
            elif value.element == 'array':
                sample = None
                if not isinstance(value.content, list):
                    raise ValueError('unexpected content for list')
                if not value.content:
                    array_element_type = 'string'
                else:
                    array_element_type = value.content[0].element
                    el_content = value.content[0].content
                    if (array_element_type == 'string' and el_content and isinstance(el_content, str) and
                            re.match(r'^\w+: ', el_content)):
                        raise ValueError(
                            f'{class_name}.{name}: is this really an array of strings or are we missing an (object) '
                            f'definition?')
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
                if class_attributes:
                    new_class = PythonClass(name=referenced_class, attributes=class_attributes,
                                            description=value.description, is_enum=False, baseclass=None)
                    self._add_class(new_class)
                    python_type = new_class.name
                else:
                    # attribute type is a generic "object"
                    python_type = 'Any'
                    referenced_class = None
            elif value.element == 'number':
                sample = value.content
                # can be int or float
                if value.content is None:
                    python_type = 'int'
                else:
                    try:
                        sample = int(value.content)
                        python_type = 'int'
                    except ValueError:
                        python_type = 'float'
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
                         referenced_class=referenced_class, optional=optional)

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
            try:
                key = '/'.join(sorted(str(attr.name) for attr in pc.attributes))
            except TypeError:
                raise
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
                try:
                    python_name = qualident_to_python_name[endpoint.result_referenced_class]
                except KeyError:
                    err_txt = (f'"{endpoint.result_referenced_class}" not found in qualident_to_python_name '
                              f'endpoint: {endpoint.name}')
                    log.error(err_txt)
                    raise KeyError(err_txt)

                python_name, _ = self._dereferenced_class(python_name)
                endpoint.result = endpoint.result.replace(endpoint.result_referenced_class,
                                                          python_name)
                endpoint.result_referenced_class = python_name

            if endpoint.body_class_name:
                python_name = qualident_to_python_name[endpoint.body_class_name]
                python_name, _ = self._dereferenced_class(python_name)
                endpoint.body_class_name = python_name

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
                                                         optional=attr.optional, referenced_class=attr.referenced_class,
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
            response_body = response and response.message_body
            endpoint = Endpoint(name=name, method=method, host=host, url=url,
                                title=transition.title,
                                docstring=transition.docstring,
                                href_parameter=href_parameters,
                                body_parameter=body_parameters,
                                body_class_name=body_class_name,
                                response_body=response_body,
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
            if type_hint is None and member.value and member.value.element.lower() in {'string', 'boolean'}:
                # use value as fallback
                type_hint = member.value.element
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
            sample, python_type = guess_datetime_or_int(sample, type_hint_lower)
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

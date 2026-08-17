"""
Pydantic models to deserialize OpenAPI specs
"""

import logging
import re
from collections.abc import Generator
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from wxc_sdk.base import to_camel

log = logging.getLogger(__name__)


class OABaseModel(BaseModel):
    """Base class for strict OpenAPI models with vendor-extension support."""

    model_config = ConfigDict(alias_generator=to_camel, extra='forbid')

    @model_validator(mode='before')
    @classmethod
    def discard_unknown_vendor_extensions(cls, value: Any) -> Any:
        """Discard undeclared ``x-*`` keys while retaining declared extensions.

        :param value: Raw value passed to Pydantic for model validation.
        :return: A shallow copy without unknown vendor extensions, or the original non-mapping value.

        OpenAPI permits vendor extensions on every object. Ordinary unknown fields remain
        forbidden so misspelled standard fields continue to fail validation.
        """
        if not isinstance(value, dict):
            return value
        declared_aliases = {field.alias for field in cls.model_fields.values() if field.alias}
        return {
            key: item
            for key, item in value.items()
            if not (isinstance(key, str) and key.startswith('x-') and key not in declared_aliases)
        }


class OANameAndUrl(OABaseModel):
    name: Optional[str] = None
    url: Optional[str] = None


class OACContact(OANameAndUrl):
    email: Optional[str] = None


class OAInfo(OABaseModel):
    title: str
    version: str
    description: str
    terms_of_service: Optional[str] = None
    license: Optional[OANameAndUrl] = None
    contact: Optional[OACContact] = None


class OAServer(OABaseModel):
    description: Optional[str] = None
    url: str


class OAParameter(OABaseModel):
    ref: Optional[str] = Field(None, alias='$ref')
    name: Optional[str] = None
    in_: Optional[str] = Field(None, alias='in')
    description: Optional[str] = None
    required: bool = False
    example: Optional[Any] = None
    examples: Optional[Any] = None
    schema_: Optional['OASchemaProperty'] = Field(None, alias='schema')
    style: Optional[str] = None
    explode: Optional[bool] = None
    allow_reserved: Optional[bool] = None
    content: Optional[dict[str, 'OAContent']] = None

    @property
    def is_auth(self) -> bool:
        """
        Check if this is an auth parameter
        """
        return self.name == 'Authorization' and self.in_ == 'header'


class OARequestBody(OABaseModel):
    description: Optional[str] = None
    ref: Optional[str] = Field(alias='$ref', default=None)
    content: Optional[dict[str, 'OAContent']] = None
    required: Optional[bool] = None


class OASchemaPropertyItemsRef(OABaseModel):
    ref: str = Field(alias='$ref')


class OADiscriminator(OABaseModel):
    """
    OpenAPI discriminator metadata for a polymorphic schema.

    :param property_name: Property whose value selects the concrete schema.
    :type property_name: str
    :param mapping: Optional discriminator-value to schema-reference mapping.
    :type mapping: Optional[dict[str, str]]
    """

    property_name: str
    mapping: Optional[dict[str, str]] = None


class OASchemaRef(OABaseModel):
    ref: str = Field(alias='$ref')


class OASchemaProperty(OABaseModel):
    """
    OpenAPI Schema Object used for components, properties, and nested alternatives.

    Nested ``anyOf``, ``allOf``, and ``oneOf`` alternatives recursively retain complete
    Schema Objects, including inline types, items, properties, and references.
    """

    title: Optional[str] = None
    type: Optional[str | OASchemaPropertyItemsRef] = None
    deprecated: bool = Field(default=False)
    # if no type, then this is a reference to another schema
    ref: Optional[str] = Field(alias='$ref', default=None)
    description: Optional[str] = None
    example: Optional[Any] = None
    examples: Optional[Any] = None
    # ref for array items if type == 'array'
    items: Optional['OASchemaProperty'] = None
    # enum values if type == 'string'
    enum: Optional[list[Optional[str | int]]] = None
    # properties if type == 'object'
    properties: Optional[dict[str, 'OASchemaProperty']] = None
    required: Optional[list[str]] = Field(default_factory=list)
    nullable: Optional[bool] = None
    # list of possible types
    any_of: Optional[list['OASchemaProperty']] = None
    all_of: Optional[list['OASchemaProperty']] = None
    one_of: Optional[list['OASchemaProperty']] = None
    not_: Optional['OASchemaProperty'] = Field(alias='not', default=None)
    format: Optional[str] = None
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    pattern: Optional[str] = None
    unique_items: Optional[bool] = None
    read_only: Optional[bool] = None
    additional_properties: Optional[Any] = None
    min_properties: Optional[int] = None
    max_properties: Optional[int] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    # OpenAPI allows integer and fractional divisors for numeric schemas.
    multiple_of: Optional[int | float] = None
    min_items: Optional[int] = None
    max_items: Optional[int] = None
    discriminator: Optional[OADiscriminator] = None
    default: Optional[Any] = None
    definitions: Optional[Any] = None

    # noinspection PyMethodParameters
    @field_validator('enum', mode='before')
    @classmethod
    def validate_enum(cls, v: Any, validation: ValidationInfo) -> Any:
        """
        Validate enum. Only valid for type 'string' and 'integer'
        """
        data = validation.data
        if data['type'] not in {'string', 'integer'}:
            raise ValueError("enum is only valid for type 'string' and 'integer")
        return v

    @model_validator(mode='after')
    def cleanup_after(self: 'OASchemaProperty') -> 'OASchemaProperty':
        """
        remove None from enum values. None represents the null value and is not a valid enum value.
        """
        if self.enum and any(enum_value is None for enum_value in self.enum):
            log.warning(f'Remove None from Enum values: {", ".join(map(str, self.enum))}')
            self.enum = [enum_value for enum_value in self.enum if enum_value is not None]
        return self

    @property
    def enum_details(self) -> Optional[list[tuple[str, str]]]:
        """
        Documentation of enum values is pushed into the description

        Example:
            The type of room.
                * `direct` - 1:1 room
                * `group` - group room
        This function returns a list of tuples with the enum value and its description.
        """

        if self.enum is None:
            return None
        if self.description is None:
            return None
        # we want to look for the enum values in the description and need a regex that matches the enum values
        # the regex looks for lines that start with * `enum_value` - description
        # and captures the enum value and description
        # the regex is multiline, so we need to use re.MULTILINE
        try:
            match_enum_values = '|'.join(
                f'(?:{re.escape(str(enum_value))})' for enum_value in self.enum if enum_value is not None
            )
            match_descriptions = f'^\\s*\\* `({match_enum_values})`\\s*-\\s*'
        except:
            raise
        matches = list(re.finditer(match_descriptions, self.description, re.MULTILINE + re.DOTALL))
        details = dict()
        for i, match in enumerate(matches):
            if i == len(matches) - 1:
                desc_end = len(self.description)
            else:
                desc_end = matches[i + 1].start() - 1
            desc_start = match.end()
            desc = self.description[desc_start:desc_end]
            enum_value = match.group(1)
            details[enum_value] = desc.strip()
        return [(str(enum_value), d if (d := details.get(enum_value)) else '') for enum_value in self.enum]

    @property
    def enum_description(self) -> Optional[str]:
        """
        Get the enum description. Since enum value documentation is pushed into the description, we need a way to get
        the description without the enum value documentation.
        """
        if self.enum is None:
            return None
        if self.description is None:
            return None

        # look for first enum value description
        # look for the 1st line starting with "* "
        pattern = re.compile(r'(.*?)^\s*\* ', re.MULTILINE + re.DOTALL)
        m = pattern.match(self.description)
        if m:
            description = m.group(1) or ''
            return description.strip()
        return self.description

    @property
    def docstring(self) -> str:
        """
        either the full description or the description without the enum value documentation
        """
        if self.enum:
            return self.enum_description or ''
        return self.description or ''

    @staticmethod
    def _obj_ref(plist: Optional[list['OASchemaProperty']]) -> Optional[str]:
        """
        Get the referenced object schema.
        """
        if plist is None:
            return None
        object_item = next((item for item in plist if item.type == 'object'), None)
        # if there is an object item, it must not have properties
        if object_item and object_item.properties:
            raise ValueError(f'Object schema {object_item} has properties, cannot return a reference')
        ref_item = next((item for item in plist if item.ref is not None), None)
        return ref_item and ref_item.ref  # type: ignore[return-value]

    @property
    def object_ref(self) -> Optional[str]:
        """
        Get the referenced object schema.
        Example:
                "allOf": [
                  {
                    "$ref": "#/components/schemas/AgentCallerIdType"
                  },
                  {
                    "type": "object",
                    "properties": {}
                  }
                ],

        """
        return self._obj_ref(self.all_of)

    @property
    def any_ref(self) -> Optional[str]:
        """
        Any reference
        """
        return self.ref or self._obj_ref(self.all_of) or self._obj_ref(self.any_of)

    @property
    def any_type(self) -> Optional[str]:
        """
        Any type
        """
        if self.type:
            return self.type  # type: ignore[return-value]
        if not self.any_of:
            return None
        any_types = set(item.type for item in self.any_of)
        if len(any_types) > 1:
            return None
        return any_types.pop()  # type: ignore[return-value]


class OAContent(OABaseModel):
    schema_: Optional[OASchemaProperty] = None
    example: Optional[Any] = None
    examples: Optional[Any] = None
    encoding: Optional[Any] = None


class OAResponse(OABaseModel):
    description: Optional[str] = None
    headers: Optional[dict[Any, Any]] = None
    content: Optional[dict[str, OAContent]] = Field(default_factory=dict)
    ref: Optional[str] = Field(alias='$ref', default=None)


class ExternalDocs(OABaseModel):
    description: Optional[str] = None
    url: Optional[str] = None


class OAOperation(OABaseModel):
    summary: str
    operation_id: Optional[str] = None
    description: Optional[str] = ''
    parameters: Optional[list[OAParameter]] = Field(default_factory=list)
    request_body: Optional[OARequestBody] = None
    security: Optional[Any] = None
    responses: dict[str, OAResponse]
    tags: Optional[list[str]] = Field(default_factory=list)
    deprecated: Optional[bool] = None
    external_docs: Optional[ExternalDocs] = None
    request_body_name: Optional[str] = Field(alias='x-codegen-request-body-name', default=None)

    @property
    def path_parameters(self) -> list[OAParameter]:
        return [param for param in self.parameters if param.in_ == 'path']  # type: ignore[union-attr]

    @property
    def query_parameters(self) -> list[OAParameter]:
        return [param for param in self.parameters if param.in_ == 'query']  # type: ignore[union-attr]


class OASpecSchema(OABaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    required: Optional[list[str]] = Field(default_factory=list)
    properties: dict[str, OASchemaProperty] = Field(default_factory=dict)
    # all_of can exist on its own
    all_of: Optional[list[Any]] = None
    # if schema is an enum, then these are the possible values
    enum: Optional[list[Optional[str]]] = None


class OAComponents(OABaseModel):
    parameters: Optional[dict[str, OAParameter]] = Field(default_factory=dict)
    schemas: dict[str, OASchemaProperty] = Field(default_factory=dict)
    request_bodies: Optional[dict[str, OARequestBody]] = None
    security_schemes: Optional[dict[str, Any]] = None
    responses: Optional[dict[str, OAResponse]] = None


class NameAndDescription(OABaseModel):
    name: str
    description: Optional[str] = None


Tag = str | NameAndDescription


class OASpec(OABaseModel):
    openapi: str
    info: OAInfo
    servers: Optional[list[OAServer]] = None
    paths: dict[str, dict[str, OAOperation]]
    components: OAComponents
    tags: Optional[list[Tag]] = None
    security: Optional[list[Any]] = None
    external_docs: Optional[ExternalDocs] = None

    def operations(self) -> Generator[tuple[str, str, OAOperation], None, None]:
        """
        Generator of operations defined in this API spec
        """
        for path in sorted(self.paths):
            path_item = self.paths[path]
            for method in sorted(path_item):
                operation = path_item[method]
                yield path, method, operation

    def get_schema(self, schema_ref: str) -> OASchemaProperty:
        """
        Get schema by reference
        """
        ref_match = re.match(r'^#/components/schemas/(.+)$', schema_ref)
        schema_ref = ref_match and ref_match.group(1) or schema_ref
        return self.components.schemas[schema_ref]

    def deref(self, ref: str) -> OARequestBody | OAResponse | OASchemaProperty | OAParameter | None:
        """
        Dereference a component reference.

        :param ref: OpenAPI component reference such as ``#/components/responses/BadRequestError``.
        :type ref: str
        :return: Referenced component object, or ``None`` when the reference does not target ``#/components``.
        :rtype: OARequestBody | OAResponse | OASchemaProperty | OAParameter | None
        :raises ValueError: If the component type is not supported by the generator.
        """
        ref_match = re.match(r'^#/components/(.+?)/(.+)$', ref)
        if not ref_match:
            return None
        component_type: str = ref_match.group(1)
        component_name: str = ref_match.group(2)
        if component_type == 'schemas':
            return self.components.schemas[component_name]
        elif component_type == 'responses':
            return self.components.responses[component_name]  # type: ignore[index]
        elif component_type == 'parameters':
            return self.components.parameters[component_name]  # type: ignore[index]
        elif component_type == 'requestBodies':
            return self.components.request_bodies[component_name]  # type: ignore[index]
        else:
            raise ValueError(f'Unknown component type: {component_type}')

    def deref_parameters(self) -> None:
        """
        Deref all parameters defined with $ref in this API spec
        """
        for _, _, op in self.operations():
            if not op.parameters:
                continue
            op.parameters = [self.deref(p.ref) if p.ref else p for p in op.parameters]  # type: ignore[misc]
        return

    def unify_all_of_schemas(self) -> None:
        """Flatten object ``allOf`` compositions in ``components/schemas`` in-place.

        Referenced component compositions and nested inline compositions are resolved recursively.
        Properties are merged and required fields are unioned. Identical duplicate properties are
        accepted because several upstream specifications repeat a base definition for documentation.

        :return: None.
        :raises ValueError: If a reference cannot be resolved, a composition contains a non-object
            alternative, duplicate properties conflict, or component compositions form a cycle.
        """

        def component_name(ref: str, context: str) -> str:
            """Extract a component schema name from a local reference.

            :param ref: Reference to validate and parse.
            :param context: Human-readable composition context for errors.
            :return: Referenced schema component name.
            :raises ValueError: If the reference is not a local component schema reference.
            """
            ref_match = re.match(r'^#/components/schemas/(.+)$', ref)
            if not ref_match:
                raise ValueError(f'{context}: allOf reference {ref!r} is not a component schema reference')
            return ref_match.group(1)

        def merge_property(
            properties: dict[str, OASchemaProperty],
            name: str,
            prop: OASchemaProperty,
            context: str,
        ) -> None:
            """Merge one property while rejecting incompatible duplicate definitions.

            :param properties: Accumulated property definitions.
            :param name: OpenAPI property name being merged.
            :param prop: Candidate property definition.
            :param context: Human-readable composition context for errors.
            :return: None.
            :raises ValueError: If the property was already defined differently.
            """
            existing = properties.get(name)
            if existing is None:
                properties[name] = prop.model_copy(deep=True)
                return
            if existing.model_dump(by_alias=True, exclude_none=True) != prop.model_dump(
                by_alias=True, exclude_none=True
            ):
                raise ValueError(f'{context}: conflicting allOf definitions for property {name!r}')

        def flatten_object(
            schema: OASchemaProperty,
            context: str,
            component_stack: tuple[str, ...],
        ) -> tuple[dict[str, OASchemaProperty], set[str]]:
            """Return merged properties and required names for one object composition.

            :param schema: Schema or reference participating in the composition.
            :param context: Human-readable composition context for errors.
            :param component_stack: Component names currently being expanded.
            :return: Merged properties and required field names.
            :raises ValueError: If the composition is invalid or cyclic.
            """
            if schema.ref:
                name = component_name(schema.ref, context)
                if name in component_stack:
                    cycle = ' -> '.join((*component_stack, name))
                    raise ValueError(f'{context}: allOf composition cycle detected: {cycle}')
                try:
                    referenced = self.components.schemas[name]
                except KeyError as error:
                    raise ValueError(f'{context}: allOf reference {schema.ref!r} could not be resolved') from error
                return flatten_object(referenced, f'{context} -> {name}', (*component_stack, name))

            if schema.type not in {None, 'object'} or (
                schema.type is None and schema.properties is None and schema.all_of is None
            ):
                raise ValueError(f'{context}: allOf alternatives must resolve to object schemas')

            properties: dict[str, OASchemaProperty] = {}
            required = set(schema.required or [])
            for prop_name, prop in schema.properties.items() if schema.properties else ():
                merge_property(properties, prop_name, prop, context)

            for index, alternative in enumerate(schema.all_of or []):
                alternative_context = f'{context} allOf[{index}]'
                alternative_properties, alternative_required = flatten_object(
                    alternative,
                    alternative_context,
                    component_stack,
                )
                for prop_name, prop in alternative_properties.items():
                    merge_property(properties, prop_name, prop, context)
                required.update(alternative_required)
            return properties, required

        for schema_name, schema in self.components.schemas.items():
            if schema.all_of is None:
                continue
            properties, required = flatten_object(schema, f'Schema {schema_name!r}', (schema_name,))
            schema.type = 'object'
            schema.properties = properties
            schema.required = sorted(required)
            schema.all_of = None
        return

    def unify_one_of_schemas(self) -> None:
        """
        Unify ``oneOf`` schemas in ``components/schemas`` in-place.

        For every schema whose ``one_of`` field is set this method:

        1. Validates that no incompatible schema-defining fields are set. A redundant
           ``type: object`` is accepted.
        2. Dereferences component alternatives and accepts inline object alternatives.
        3. Computes the union of all properties across the alternatives.
        4. Marks a property as *required* only when it is required in **every** alternative.
        5. For enum-typed properties, merges the enum value lists across all alternatives
           that carry that property, preserving original order with duplicates removed.
        6. Replaces ``one_of`` with the unified ``type='object'`` / ``properties`` / ``required``
           representation on the schema object so that downstream codegen sees a normal object.

        Nested ``oneOf`` declarations are left intact for the type resolver. Component-level
        declarations must contain only object schemas so this compatibility normalization cannot
        silently change a primitive or array union into an object. Parsed ``not`` constraints are
        intentionally ignored because generated SDK models do not implement JSON Schema logic.

        :return: None.
        :raises ValueError: If a component-level ``oneOf`` is empty, contains a non-object
            alternative, has an unresolved reference, or is combined with other schema-defining fields.
        """

        def ref_to_schema_name(ref: str) -> str:
            ref_match = re.match(r'^#/components/schemas/(.+)$', ref)
            return ref_match.group(1) if ref_match else ref

        for schema_name, schema in self.components.schemas.items():
            if schema.one_of is None:
                continue

            # A redundant ``type: object`` is compatible with the object-only flattening.
            allowed_fields = {
                'default',
                'deprecated',
                'description',
                'discriminator',
                'example',
                'examples',
                'not_',
                'nullable',
                'one_of',
                'read_only',
                'title',
            }
            if schema.type == 'object':
                allowed_fields.add('type')
            disallowed_fields = sorted(schema.model_fields_set - allowed_fields)
            if disallowed_fields:
                raise ValueError(
                    f'Schema {schema_name!r}: one_of cannot be unified when other fields are set: '
                    f'{", ".join(disallowed_fields)}'
                )

            # --- 1. Resolve references and validate inline alternatives ---
            if not schema.one_of:
                raise ValueError(f'Schema {schema_name!r}: top-level oneOf must contain alternatives')
            referenced: list[OASchemaProperty] = []
            one_of_schema_names: list[str] = []
            for index, option in enumerate(schema.one_of):
                if option.ref:
                    try:
                        referenced_schema = self.get_schema(option.ref)
                    except KeyError as error:
                        raise ValueError(
                            f'Schema {schema_name!r}: oneOf reference {option.ref!r} could not be resolved'
                        ) from error
                    one_of_schema_names.append(ref_to_schema_name(option.ref))
                else:
                    referenced_schema = option
                    one_of_schema_names.append(f'<inline:{index}>')
                if referenced_schema.type != 'object':
                    raise ValueError(f'Schema {schema_name!r}: top-level oneOf alternatives must all be object schemas')
                referenced.append(referenced_schema)

            # --- 2. Collect all property names ---
            all_names: list[str] = []
            seen: set[str] = set()
            for ref_schema in referenced:
                for name in ref_schema.properties or {}:
                    if name not in seen:
                        all_names.append(name)
                        seen.add(name)

            # --- 3. Merge properties ---
            merged_properties: dict[str, OASchemaProperty] = {}
            for prop_name in all_names:
                instances: list[OASchemaProperty] = [
                    ref_schema.properties[prop_name]
                    for ref_schema in referenced
                    if ref_schema.properties and prop_name in ref_schema.properties
                ]
                if len(instances) == 1:
                    merged_properties[prop_name] = instances[0].model_copy(deep=True)
                else:
                    # Start with a deep copy of the first occurrence.
                    merged = instances[0].model_copy(deep=True)
                    # If property carries enum values, union them while preserving order.
                    if merged.enum is not None:
                        merged_enum: list[str | int] = list(merged.enum)  # type: ignore[arg-type]
                        seen_enum: set[str | int] = set(merged_enum)
                        for other in instances[1:]:
                            for ev in other.enum or []:
                                if ev not in seen_enum:
                                    merged_enum.append(ev)  # type: ignore[arg-type]
                                    seen_enum.add(ev)  # type: ignore[arg-type]
                        merged.enum = merged_enum  # type: ignore[assignment]
                    merged_properties[prop_name] = merged

            # --- 4. Required = intersection across all referenced schemas ---
            if referenced:
                required_in_all: set[str] = set(referenced[0].required or [])
                for ref_schema in referenced[1:]:
                    required_in_all &= set(ref_schema.required or [])
            else:
                required_in_all = set()

            # --- 5. Update the schema in-place ---
            log.info(
                'unify_one_of_schemas: schema_name=%s one_of_refs=%s merged_properties=%s',
                schema_name,
                sorted(one_of_schema_names),
                list(merged_properties.keys()),
            )

            schema.type = 'object'
            schema.properties = merged_properties
            schema.required = sorted(required_in_all)
            schema.one_of = None
        return

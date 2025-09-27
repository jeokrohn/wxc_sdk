"""
Pydantic models to deserialize OpenAPI specs
"""
import logging
import re
from collections.abc import Generator
from typing import List, Optional, Any, Union, Tuple

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from wxc_sdk.base import to_camel

log = logging.getLogger(__name__)


class OABaseModel(BaseModel):
    """
    Base class for OpenAPI models
    """

    class Config:
        alias_generator = to_camel
        extra = 'forbid'


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
    name: str
    in_: str = Field(..., alias='in')
    description: Optional[str] = None
    required: bool = False
    example: Optional[Any] = None
    schema_: Optional['OASchemaProperty'] = Field(alias='schema', default=None)
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
    property_name: str


class OASchemaProperty(OABaseModel):
    title: Optional[str] = None
    type: Optional[Union[str, OASchemaPropertyItemsRef]] = None
    deprecated: bool = Field(default=False)
    # if no type, then this is a reference to another schema
    ref: Optional[str] = Field(alias='$ref', default=None)
    description: Optional[str] = None
    example: Optional[Any] = None
    # ref for array items if type == 'array'
    items: Optional['OASchemaProperty'] = None
    # enum values if type == 'string'
    enum: Optional[List[Optional[str]]] = None
    # properties if type == 'object'
    properties: Optional[dict[str, 'OASchemaProperty']] = None
    required: Optional[List[str]] = Field(default_factory=list)
    nullable: Optional[bool] = None
    # list of possible types
    any_of: Optional[list['OASchemaProperty']] = None
    all_of: Optional[list['OASchemaProperty']] = None
    one_of: Optional[list[Any]] = None
    format: Optional[str] = None
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    pattern: Optional[str] = None
    unique_items: Optional[bool] = None
    read_only: Optional[bool] = None
    additional_properties: Optional[Any] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    min_items: Optional[int] = None
    max_items: Optional[int] = None
    discriminator: Optional[OADiscriminator] = None
    default: Optional[Any] = None
    definitions: Optional[Any] = None

    # noinspection PyMethodParameters
    @field_validator('enum', mode='before')
    def validate_enum(cls, v, validation: ValidationInfo):
        """
        Validate enum. Only valid for type 'string'
        """
        data = validation.data
        if data['type'] != 'string':
            raise ValueError(f"enum is only valid for type 'string'")
        return v

    @model_validator(mode='after')
    def remove_none_from_enum(cls, data: 'OASchemaProperty') -> 'OASchemaProperty':
        """
        remove None from enum values. None represents the null value and is not a valid enum value.
        """
        if data.enum and any(enum_value is None for enum_value in data.enum):
            log.warning(f"Remove None from Enum values: {', '.join(map(str, data.enum))}")
            data.enum = [enum_value for enum_value in data.enum if enum_value is not None]
        return data

    @property
    def enum_details(self) -> Optional[List[Tuple[str, str]]]:
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
        r = []
        # we want to look for the enum values in the description and need a regex that matches the enum values
        # the regex looks for lines that start with * `enum_value` - description
        # and captures the enum value and description
        # the regex is multiline, so we need to use re.MULTILINE
        try:
            match_enum_values = '|'.join(f'(?:{re.escape(enum_value)})' for enum_value in self.enum
                                         if enum_value is not None)
            match_descriptions = f'^\s*\* `({match_enum_values})` - '
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
        return [(enum_value, d if (d := details.get(enum_value)) else '')
                for enum_value in self.enum]

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
        pattern = f'(:?(.*?)\n)?^ \* `.+?` -'
        m = re.match(pattern, self.description, re.MULTILINE + re.DOTALL)
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
            raise ValueError(f"Object schema {object_item} has properties, cannot return a reference")
        ref_item = next((item for item in plist if item.ref is not None), None)
        return ref_item and ref_item.ref

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
    def any_ref(self) -> Optional['OASchemaProperty']:
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
            return self.type
        if not self.any_of:
            return None
        any_types = set(item.type for item in self.any_of)
        if len(any_types) > 1:
            return None
        return any_types.pop()


class OAContent(OABaseModel):
    schema_: Optional[OASchemaProperty] = None
    example: Optional[Any] = None
    examples: Optional[Any] = None
    encoding: Optional[Any] = None


class OAResponse(OABaseModel):
    description: Optional[str] = None
    headers: Optional[dict] = None
    content: Optional[dict[str, OAContent]] = Field(default_factory=dict)
    ref: Optional[str] = Field(alias='$ref', default=None)


class ExternalDocs(OABaseModel):
    description: Optional[str] = None
    url: Optional[str] = None


class OAOperation(OABaseModel):
    summary: str
    operation_id: Optional[str] = None
    description: str
    parameters: Optional[List[OAParameter]] = Field(default_factory=list)
    request_body: Optional[OARequestBody] = None
    security: Optional[Any] = None
    responses: dict[str, OAResponse]
    tags: Optional[List[str]] = Field(default_factory=list)
    deprecated: Optional[bool] = None
    external_docs: Optional[ExternalDocs] = None

    @property
    def path_parameters(self) -> List[OAParameter]:
        return [param for param in self.parameters if param.in_ == 'path']

    @property
    def query_parameters(self) -> List[OAParameter]:
        return [param for param in self.parameters if param.in_ == 'query']


class OASpecSchema(OABaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    required: Optional[List[str]] = Field(default_factory=list)
    properties: dict[str, OASchemaProperty] = Field(default_factory=dict)
    # all_of can exist on its own
    all_of: Optional[List[Any]] = None
    # if schema is an enum, then these are the possible values
    enum: Optional[List[Optional[str]]] = None


class OAComponents(OABaseModel):
    schemas: dict[str, OASchemaProperty] = Field(default_factory=dict)
    request_bodies: Optional[dict[str, OARequestBody]] = None
    security_schemes: Optional[dict[str, Any]] = None
    responses: Optional[dict[str, OAResponse]] = None


class NameAndDescription(OABaseModel):
    name: str
    description: Optional[str] = None


Tag = Union[str, NameAndDescription]


class OASpec(OABaseModel):
    openapi: str
    info: OAInfo
    servers: Optional[List[OAServer]] = None
    paths: dict[str, dict[str, OAOperation]]
    components: OAComponents
    tags: Optional[list[Tag]] = None
    security: Optional[List[Any]] = None
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

    def deref(self, ref: str):
        """
        Dereference a ref like '#/components/responses/BadRequestError'
        :param ref:
        :return:
        """
        ref_match = re.match(r'^#/components/(.+?)/(.+)$', ref)
        if not ref_match:
            return None
        component_type = ref_match.group(1)
        component_name = ref_match.group(2)
        if component_type == 'schemas':
            return self.components.schemas[component_name]
        elif component_type == 'responses':
            return self.components.responses[component_name]
        else:
            raise ValueError(f"Unknown component type: {component_type}")

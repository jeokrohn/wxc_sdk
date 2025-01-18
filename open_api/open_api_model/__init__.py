"""
Pydantic models to deserialize OpenAPI specs
"""
import re
from collections.abc import Generator
from typing import List, Optional, Any, Union

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from wxc_sdk.base import to_camel


class OpenApiBaseModel(BaseModel):
    """
    Base class for OpenAPI models
    """

    class Config:
        alias_generator = to_camel
        extra = 'forbid'


class NameAndUrl(OpenApiBaseModel):
    name: str
    url: Optional[str] = None


class Info(OpenApiBaseModel):
    title: str
    version: str
    description: str
    terms_of_service: Optional[str] = None
    license: Optional[NameAndUrl] = None
    contact: Optional[NameAndUrl] = None


class Server(OpenApiBaseModel):
    description: Optional[str] = None
    url: str


class Parameter(OpenApiBaseModel):
    name: str
    in_: str = Field(..., alias='in')
    description: Optional[str] = None
    required: bool = False
    example: Optional[Any] = None
    schema_: dict = Field(alias='schema')
    style: Optional[str] = None
    explode: Optional[bool] = None
    allow_reserved: Optional[bool] = None


class RequestBody(OpenApiBaseModel):
    description: Optional[str] = None
    ref: Optional[str] = Field(alias='$ref', default=None)
    content: Optional[dict] = None
    required: Optional[bool] = None


class OpenApiSpecSchemaPropertyItemsRef(OpenApiBaseModel):
    ref: str = Field(alias='$ref')


class Discriminator(OpenApiBaseModel):
    property_name: str


class OpenApiSpecSchemaProperty(OpenApiBaseModel):
    title: Optional[str] = None
    type: Optional[Union[str, OpenApiSpecSchemaPropertyItemsRef]] = None
    # if no type, then this is a reference to another schema
    ref: Optional[str] = Field(alias='$ref', default=None)
    description: Optional[str] = None
    example: Optional[Any] = None
    # ref for array items if type == 'array'
    items: Optional['OpenApiSpecSchemaProperty'] = None
    # enum values if type == 'string'
    enum: Optional[List[Optional[str]]] = None
    # properties if type == 'object'
    properties: Optional[dict[str, 'OpenApiSpecSchemaProperty']] = None
    required: Optional[List[str]] = Field(default_factory=list)
    nullable: Optional[bool] = None
    # list of possible types
    any_of: Optional[list['OpenApiSpecSchemaProperty']] = None
    all_of: Optional[list['OpenApiSpecSchemaProperty']] = None
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
    discriminator: Optional[Discriminator] = None
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

    @staticmethod
    def _obj_ref(plist: Optional[list['OpenApiSpecSchemaProperty']]) -> Optional[str]:
        """
        Get the referenced object schema.
        """
        if plist is None:
            return None
        object_item = next((item for item in plist if item.type == 'object'), None)
        if not object_item:
            return None
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
    def any_ref(self)->Optional['OpenApiSpecSchemaProperty']:
        """
        Any reference
        """
        return self.ref or self._obj_ref(self.all_of) or self._obj_ref(self.any_of)

    @property
    def any_type(self)->Optional[str]:
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


class Content(OpenApiBaseModel):
    schema_: Optional[OpenApiSpecSchemaProperty] = None
    example: Optional[Any] = None
    examples: Optional[Any] = None


class Response(OpenApiBaseModel):
    description: str
    headers: Optional[dict] = None
    content: Optional[dict[str, Content]] = Field(default_factory=dict)


class Operation(OpenApiBaseModel):
    summary: str
    operation_id: Optional[str] = None
    description: str
    parameters: Optional[List[Parameter]] = Field(default_factory=list)
    request_body: Optional[RequestBody] = None
    security: Optional[Any] = None
    responses: dict[str, Response]
    tags: List[str]
    deprecated: Optional[bool] = None


class OpenApiSpecSchema(OpenApiBaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    required: Optional[List[str]] = Field(default_factory=list)
    properties: dict[str, OpenApiSpecSchemaProperty] = Field(default_factory=dict)
    # all_of can exist on its own
    all_of: Optional[List[Any]] = None
    # if schema is an enum, then these are the possible values
    enum: Optional[List[Optional[str]]] = None


class Components(OpenApiBaseModel):
    schemas: dict[str, OpenApiSpecSchemaProperty]
    request_bodies: Optional[dict[str, RequestBody]] = None
    security_schemes: Optional[dict[str, Any]] = None


class OpenAPISpec(OpenApiBaseModel):
    openapi: str
    info: Info
    servers: Optional[List[Server]] = None
    paths: dict[str, dict[str, Operation]]
    components: Components
    tags: Optional[List[str]] = None

    def operations(self) -> Generator[tuple[str, str, Operation], None, None]:
        """
        Generator of operations defined in this API spec
        """
        for path in sorted(self.paths):
            path_item = self.paths[path]
            for method in sorted(path_item):
                operation = path_item[method]
                yield path, method, operation

    def get_schema(self, schema_ref: str) -> OpenApiSpecSchemaProperty:
        """
        Get schema by reference
        """
        ref_match = re.match(r'^#/components/schemas/(.+)$', schema_ref)
        schema_ref = ref_match and ref_match.group(1) or schema_ref
        return self.components.schemas[schema_ref]

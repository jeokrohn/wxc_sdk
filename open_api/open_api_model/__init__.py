# Pydantic models to deserialize OpenAPI specs
import json

from pydantic import BaseModel, Field, Extra, field_validator
from typing import List, Optional, Any, Union

from pydantic_core.core_schema import ValidationInfo

from wxc_sdk.base import to_camel


class OpenApiBaseModel(BaseModel):
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


class Response(OpenApiBaseModel):
    description: str
    headers: Optional[dict]
    content: Optional[dict]


class Operation(OpenApiBaseModel):
    summary: str
    operation_id: Optional[str] = None
    description: str
    parameters: Optional[List[Parameter]] = Field(default_factory=list)
    request_body: Optional[RequestBody] = None
    security: Optional[Any] = None
    responses: dict
    tags: List[str]
    deprecated: Optional[bool] = None


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
    all_of: Optional[List[Any]] = None
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

    @field_validator('enum', mode='before')
    def validate_enum(cls, v, validation: ValidationInfo):
        data = validation.data
        if data['type'] != 'string':
            raise ValueError(f"enum is only valid for type 'string'")
        return v


class OpenApiSpecSchema(OpenApiBaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    required: Optional[List[str]] = Field(default_factory=list)
    properties: dict[str, OpenApiSpecSchemaProperty] = Field(default_factory=dict)
    # all_of can exist on it's own
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


def parse_all():
    from open_api.open_api_sources import open_api_specs

    specs = list(open_api_specs())
    parsed_specs = []
    for spec in specs:
        with open(spec.spec_path, 'r') as f:
            data = json.load(f)
        parsed_spec = OpenAPISpec.model_validate(data)
        parsed_specs.append(parsed_spec)
    foo = 1


if __name__ == '__main__':
    parse_all()

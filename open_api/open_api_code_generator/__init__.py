# mypy: disable-error-code="import-untyped,no-untyped-def,misc"
from dataclasses import dataclass

from apib.generator import CodeGenerator
from open_api.open_api_class_registry import OpenApiPythonClassRegistry
from open_api.open_api_sources import OpenApiSpecInfo


@dataclass(repr=False, init=False)
class OACodeGenerator(CodeGenerator):
    """
    Code generator for OpenAPI models
    """

    class_registry = OpenApiPythonClassRegistry

    def __init__(
        self,
        with_unreferenced_classes: bool = False,
        class_registry=None,
        body_style: str = 'args',
        consolidate_models: bool = False,
    ):
        class_registry = class_registry or OpenApiPythonClassRegistry(
            body_style=body_style, consolidate_models=consolidate_models
        )
        super().__init__(with_unreferenced_classes=with_unreferenced_classes, class_registry=class_registry)

    def add_open_api_spec(self, spec_info: OpenApiSpecInfo):
        self.class_registry.add_open_api(spec_info)

    def add_open_api_spec_from_path(self, spec_path: str):
        spec_info = OpenApiSpecInfo.from_spec_json_path(spec_path)
        self.add_open_api_spec(spec_info)

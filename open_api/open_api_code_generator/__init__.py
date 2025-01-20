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

    def __init__(self, with_unreferenced_classes: bool = False, class_registry = None):
        class_registry= class_registry or OpenApiPythonClassRegistry()
        super().__init__(with_unreferenced_classes=with_unreferenced_classes, class_registry=class_registry)

    def add_open_api_spec(self, spec_info: OpenApiSpecInfo):
        self.class_registry.add_open_api(spec_info)

"""
Unittests for code generation
"""
import logging
import os.path
from contextlib import contextmanager

from apib.apib import ApibParseResult
from apib.apib.generator import *
from apib.tests.test_apib import ApibTest


class GeneratorTest(ApibTest):

    def test_001(self):
        target_path = next((path for path in self.apib_paths
                            if path.endswith('user-call-settings.apib')), None)
        self.assertIsNotNone(target_path)
        parsed = ApibParseResult.model_validate(self.get_apib_data(target_path))
        code_generator = CodeGenerator(parsed)
        foo = 1

    def test_002_docstring(self):
        """
        Check docstring fot all APIB files
        :return:
        """
        self.stream_handler.setLevel(logging.INFO)

        def test(path, data):
            code_generator = CodeGenerator(ApibParseResult.model_validate(data))
            self.assertIsNotNone(code_generator.api_docstring, 'No docstring')

        self.for_all_apib(test)

    def test_003_methods(self):
        """
        list Methods
        """
        self.stream_handler.setLevel(logging.INFO)

        def test(path, data):
            code_generator = CodeGenerator(ApibParseResult.model_validate(data))
            for endpoint in code_generator.endpoints():
                print(f'{path}: {endpoint.host}/{endpoint.href}')

        self.for_all_apib(test)

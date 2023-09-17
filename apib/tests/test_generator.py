"""
Unittests for code generation
"""
import logging
import os
from os.path import splitext, dirname

from apib.generator import CodeGenerator
from apib.tests.test_apib import ApibTest


class GeneratorTest(ApibTest):

    def test_001_generate_class_sources(self):
        """
        Generate Python sources for all classes in all APIB sources
        """
        logging.getLogger().setLevel(logging.INFO)

        for apib_path in self.apib_paths:
            code_gen = CodeGenerator()
            code_gen.read_blueprint(apib_path)
            apib_path = os.path.basename(apib_path)
            py_path = os.path.join(os.path.dirname(__file__),
                                   'generated',
                                   f'{os.path.splitext(apib_path)[0]}_auto.py')
            with open(py_path, mode='w') as f:
                f.write(code_gen.source())

    def test_002_endpoints(self):
        logging.getLogger().setLevel(logging.INFO)

        for apib_path in self.apib_paths:
            code_gen = CodeGenerator()
            code_gen.read_blueprint(apib_path)
            apib_path = os.path.basename(apib_path)
            for ep in code_gen.endpoints():
                print(ep)

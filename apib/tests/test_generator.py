"""
Unittests for code generation
"""
import logging
import os
import sys

from apib.generator import CodeGenerator
from apib.tests.test_apib import ApibTest


class GeneratorTest(ApibTest):

    def test_001_generate_class_sources(self):
        """
        Generate Python sources for all classes in all APIB sources
        """
        logging.getLogger().setLevel(logging.INFO)
        err = None
        for apib_path in self.apib_paths:
            try:
                code_gen = CodeGenerator()
                code_gen.read_blueprint(apib_path)
                code_gen.cleanup()
            except Exception as e:
                err = err or e
                print(f'{os.path.basename(apib_path)}: {e}')
            else:
                apib_path = os.path.basename(apib_path)
                py_path = os.path.join(os.path.dirname(__file__),
                                       'generated',
                                       f'{os.path.splitext(apib_path)[0]}_auto.py')
                with open(py_path, mode='w') as f:
                    f.write(code_gen.source())
        if err:
            raise err

    def test_002_endpoints(self):
        logging.getLogger().setLevel(logging.INFO)

        for apib_path in self.apib_paths:
            code_gen = CodeGenerator()
            code_gen.read_blueprint(apib_path)
            code_gen.cleanup()
            for apib_key, ep in code_gen.all_endpoints():
                print(f'{apib_key}: {ep}')

    def test_003_generate_class_sources_with_endpoints(self):
        logging.getLogger().setLevel(logging.INFO)

        err = None
        for apib_path in self.apib_paths:
            apib_path_base = os.path.basename(apib_path)
            if 'video-mesh.apib' == apib_path_base:
                continue
            code_gen = CodeGenerator()
            try:
                code_gen.read_blueprint(apib_path)
                classes_after_reading_blueprint = len(list(code_gen.class_registry.classes()))

                list(code_gen.endpoints())
                classes_after_generating_endpoints = len(list(code_gen.class_registry.classes()))

                code_gen.class_registry.eliminate_redundancies()
                classes_after_generating_endpoints_no_redundancies = len(list(code_gen.class_registry.classes()))

                print(f'{apib_path_base}: {classes_after_reading_blueprint}, {classes_after_generating_endpoints}, '
                      f'{classes_after_generating_endpoints_no_redundancies}')
                py_path = os.path.join(os.path.dirname(__file__),
                                       'generated',
                                       f'{os.path.splitext(apib_path_base)[0]}_auto.py')
                with open(py_path, mode='w') as f:
                    f.write(code_gen.source())
            except Exception as e:
                print(f'{apib_path_base}: {e}', file=sys.stderr)
                err = err or e
        if err:
            raise err

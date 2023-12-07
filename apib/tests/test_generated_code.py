"""
Tests for generated Python code
"""
import importlib.util
import inspect
import logging
import os
import sys
from inspect import getmembers, isclass
from os.path import splitext, join
from tempfile import NamedTemporaryFile, TemporaryDirectory

from apib.generator import CodeGenerator
from apib.tests.test_apib import ApibTest


class Tests(ApibTest):

    def test_import(self):
        self.stream_handler.setLevel(logging.INFO)
        # ignore these APIB files
        ignore = {'device-configurations.apib', 'convergedRecordings.apib'}

        err = None
        with TemporaryDirectory() as temp_dir:
            for apib_path in self.apib_paths:
                apib_path_base = os.path.basename(apib_path)
                if apib_path_base in ignore:
                    continue
                if apib_path_base != 'applications.apib':
                    continue
                code_gen = CodeGenerator(with_unreferenced_classes=False)
                code_gen.read_blueprint(apib_path)
                code_gen.cleanup()
                # write code to a source file in the temp dir
                # source name derived from APIB file
                python_source_name = f'{splitext(apib_path_base)[0]}.py'
                python_source_path = join(temp_dir, python_source_name)
                with open(python_source_path, mode='w') as f:
                    f.write(code_gen.source())
                try:
                    # import temp file
                    module_name = splitext(apib_path_base)[0]
                    spec = importlib.util.spec_from_file_location(module_name, python_source_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    members = inspect.getmembers(module, inspect.isclass)
                except Exception as e:
                    print(f'Failed to import "{module_name}": {e}')
        if err:
            raise err



        # for each APIB file
        # instantiate code generator for APIB file
        # generate source and write to temp file
        # import temp file and check for errors
        ...

    def test_message_body(self):
        # for each APIB file
        # instantiate code generator for APIB file
        # generate source and write to temp file
        # import temp file and check for errors
        # for each endpoint with message body
        # try to json load message body
        # try to deserialize using respective result class
        ...

    def test_all_apib(self):

        ...
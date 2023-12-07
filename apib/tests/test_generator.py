"""
Unittests for code generation
"""
import logging
import os
import sys

from apib.generator import CodeGenerator
from apib.tests.test_apib import ApibTest


class GeneratorTest(ApibTest):

    def codegen_with_all_apib(self) -> CodeGenerator:
        code_gen = CodeGenerator()
        ignore = {'device-configurations.apib'}
        for apib_path in self.apib_paths:
            apib_path_base = os.path.basename(apib_path)
            if apib_path_base in ignore:
                continue
            try:
                code_gen.read_blueprint(apib_path)
            except Exception as e:
                print(f'{apib_path_base}: {e}')
        return code_gen

    def test_001_generate_class_sources(self):
        """
        Generate Python sources for all classes in all APIB sources
        """
        logging.getLogger().setLevel(logging.INFO)
        err = None

        # ignore these APIB files
        ignore = {'device-configurations.apib', 'convergedRecordings.apib'}

        for apib_path in self.apib_paths:
            apib_path_base = os.path.basename(apib_path)
            if apib_path_base in ignore:
                continue
            # if apib_path_base != 'location-call-settings.apib':
            #     continue
            try:
                code_gen = CodeGenerator(with_unreferenced_classes=False)
                code_gen.read_blueprint(apib_path)
                code_gen.cleanup()
            except Exception as e:
                err = err or e
                print(f'{apib_path_base}: {e}')
                raise e
            else:
                apib_path = apib_path_base
                py_path = os.path.join(os.path.dirname(__file__),
                                       'generated',
                                       f'{os.path.splitext(apib_path)[0]}_auto.py')
                with open(py_path, mode='w') as f:
                    f.write(code_gen.source())
        if err:
            raise err

    def test_generate_combined_source_from_all_apib(self):
        """
        Read all APIB files and generate a combined source
        """
        logging.getLogger().setLevel(logging.INFO)
        code_gen = self.codegen_with_all_apib()
        print(f'{len(list(code_gen.class_registry.classes()))} classes before optimization')
        code_gen.cleanup()
        print(f'{len(list(code_gen.class_registry.classes()))} classes after optimization')

        apib_key_len = max(len(apib_key) for apib_key, _ in code_gen.all_endpoints())
        for apib_key, ep in code_gen.all_endpoints():
            print(f'{apib_key:{apib_key_len}}: {ep}')
        py_path = os.path.join(os.path.dirname(__file__),
                               'generated',
                               f'all_auto.py')
        with open(py_path, mode='w') as f:
            f.write(code_gen.source())

    def test_read_all_apib_endpoints_wo_body_class_but_parameters(self):
        logging.getLogger().setLevel(logging.INFO)
        code_gen = self.codegen_with_all_apib()
        apib_key_len = max(len(apib_key) for apib_key, _ in code_gen.all_endpoints())
        name_len = max(len(ep.name) for _, ep in code_gen.all_endpoints())
        print('endpoints w/o body class')
        for apib_key, ep in code_gen.all_endpoints():
            if ep.body_class_name or not ep.body_parameter:
                continue
            print(f'{apib_key:{apib_key_len}}: {ep.name:{name_len}}: {len(ep.body_parameter)} parameters')

    def test_read_all_apib_endpoints_result(self):
        logging.getLogger().setLevel(logging.INFO)
        code_gen = self.codegen_with_all_apib()
        code_gen.cleanup()
        apib_key_len = max(len(apib_key) for apib_key, _ in code_gen.all_endpoints())
        name_len = max(len(ep.name) for _, ep in code_gen.all_endpoints())
        print('endpoints w/ results')
        for apib_key, ep in code_gen.all_endpoints():
            if not any((ep.result, ep.result_referenced_class)):
                continue
            if ep.result == ep.result_referenced_class:
                continue
            print(f'{apib_key:{apib_key_len}}: {ep.name:{name_len}}: {ep.result}/{ep.result_referenced_class}')

    def test_read_all_apib_endpoints_w_body_class(self):
        logging.getLogger().setLevel(logging.INFO)
        code_gen = self.codegen_with_all_apib()
        apib_key_len = max(len(apib_key) for apib_key, _ in code_gen.all_endpoints())
        name_len = max(len(ep.name) for _, ep in code_gen.all_endpoints())
        for apib_key, ep in code_gen.all_endpoints():
            if not ep.body_class_name:
                continue
            print(f'{apib_key:{apib_key_len}}: {ep.name:{name_len}} -> {ep.body_class_name.split("%")[-1]}')

    def test_read_all_apib_endpoints_with_pagination(self):
        logging.getLogger().setLevel(logging.INFO)
        code_gen = self.codegen_with_all_apib()
        code_gen.cleanup()
        apib_key_len = max(len(apib_key) for apib_key, _ in code_gen.all_endpoints())
        name_len = max(len(ep.name) for _, ep in code_gen.all_endpoints())
        err = None
        for apib_key, ep in code_gen.all_endpoints():
            if not (pag:=ep.paginated):
                continue
            try:
                self.assertIsNotNone(ep.result_referenced_class, 'No referenced result class')
            except AssertionError as e:
                print(f'{apib_key:{apib_key_len}}: {ep.name:{name_len}} -> !!! {e}')
                err = err or e
            print(f'{apib_key:{apib_key_len}}: {ep.name:{name_len}} -> paginated: {pag.name}/{pag.python_type}')
            if ep.result_referenced_class != ep.result:
                print(f'  {" " * (apib_key_len + name_len)} -> {ep.result}/{ep.result_referenced_class}')
        if err:
            raise err

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

    def test_read_all_apib_find_list_methods_and_check_return_type(self):
        logging.getLogger().setLevel(logging.INFO)
        code_gen = self.codegen_with_all_apib()
        code_gen.cleanup()
        err = None
        for apib, ep in code_gen.all_endpoints():
            if ep.method != 'GET' or 'list' not in ep.name:
                continue
            try:
                if not ep.returns_list:
                    # is at least one of the returned attributes a list?
                    if ep.result and ep.result == ep.result_referenced_class and (rc := code_gen.class_registry.get(ep.result)):
                        list_attr = next((attr for attr in rc.attributes if attr.python_type.startswith('list[')), None)
                        self.assertIsNotNone(list_attr, 'No list attribute')
                        print(f'{apib}/{ep.name}: returns_list is None but result class "{rc.name}" has: '
                              f'{list_attr.name}: {list_attr.python_type}')
                        self.assertGreater(len(rc.attributes), 1, 'list attribute is only attribute')
                        continue
                    self.assertTrue(False, 'list method w/o result referenced class')
            except AssertionError as e:
                err = err or e
                print(f'!!! {apib}/{ep.name}: {e}')
        if err:
            raise err

import json
import os.path
import sys
import tempfile
from contextlib import contextmanager
from importlib import import_module
from os.path import basename, splitext
from unittest import TestCase

from apib.generator import CodeGenerator

# This is where all APIB files live
APIB_PATH = '/Users/jkrohn/Documents/workspace/api-specs/blueprint/webexapis.com/v1'
PY_PATH = '/Users/jkrohn/Documents/workspace/wxc_sdk/apib/tests/generated'


class TestReturnValues(TestCase):
    """
    Blueprint files can have example return values for some call. We want to try to parse these example return values
    using the pydantic models created for that endpoint

    high level process
        * read/parse APiB file
        * create source
        * import generated module
            * how do we get rid of it again?
        * identify all endpoints for which a result body is defined
        * for each of these endpoints
            * figure out the result class to parse the result
            * try to deserialize the result body
    """
    apib_file = 'user-call-settings.apib'

    @contextmanager
    def import_py_module(self, source: str):
        """
        Context manager: temporarily import given Python source as module and yield module reference
        :param source: Python source
        :return: yields imported module
        """
        # temp directory to safe the source to
        with tempfile.TemporaryDirectory() as dir:
            # temporarily add path to temp dir to Python path
            sys.path.insert(0, dir)
            try:
                module_name = splitext(basename(self.apib_file))[0]
                py_path = os.path.join(dir, f'{module_name}.py')
                # write Python source to temp dir
                with open(py_path, mode='w') as py_file:
                    py_file.write(source)
                module = import_module(module_name)
                try:
                    yield module
                finally:
                    # get rid of moduke
                    del sys.modules[module.__name__]
            finally:
                # restore original path; remove temp dir
                sys.path.pop(0)
        return

    def test_001_code_gen(self):
        # join APIB_PATH and apib_file
        apib_path = os.path.join(APIB_PATH, self.apib_file)
        code_gen = CodeGenerator(with_unreferenced_classes=False)
        code_gen.read_blueprint(apib_path)
        code_gen.cleanup()
        source = code_gen.source()
        with self.import_py_module(source) as module:
            err = None
            # iterate through all APIs in the APIB; usually there is only one
            for _, api in code_gen.class_registry.apis():
                # look at each endpoint in the API
                for endpoint in api.endpoints:
                    # endpoints w/o response body are not really interesting
                    if not endpoint.response_body:
                        # print(f'{endpoint.name}, no response body')
                        continue
                    # try to load body as json
                    try:
                        response_body = json.loads(endpoint.response_body)
                    except Exception as e:
                        print(f'{endpoint.name}, failed to read body: {e}', file=sys.stderr)
                        err = err or e
                        continue
                    # what is the result class?
                    print(f'{endpoint.name}, result: {endpoint.result}, '
                          f'result_referenced_class: {endpoint.result_referenced_class}')
                    # get an validator for the response data
                    validator = endpoint.body_validator(module)
                    # try to deserialize the body
                    try:
                        result = validator(response_body)
                    except Exception as e:
                        print(f'{endpoint.name}, ********* failed to parse body: {e}', file=sys.stderr)
                        err = err or e
                        continue
                # for
            # for
        # with
        if err:
            raise err

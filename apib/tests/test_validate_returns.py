import json
import os.path
import sys
import tempfile
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

    def test_001_code_gen(self):
        # join APIB_PATH and apib_file
        apib_path = os.path.join(APIB_PATH, self.apib_file)
        code_gen = CodeGenerator(with_unreferenced_classes=False)
        code_gen.read_blueprint(apib_path)
        code_gen.cleanup()
        source = code_gen.source()
        with tempfile.TemporaryDirectory() as dir:
            py_path = os.path.join(dir, f'{splitext(basename(self.apib_file))[0]}.py')
            # write Python source to temp dir
            with open(py_path, mode='w') as py_file:
                py_file.write(source)
            sm = sys.modules
            # import module
            # TODO: need to figure out to create module from string
            #   ... or how to import from tempdir
            module = import_module(py_path)

            err = None
            for _, api in code_gen.class_registry.apis():
                for endpoint in api.endpoints:
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
                    print(f'{endpoint.name}, result: {endpoint.result}, result_referenced_class: {endpoint.result_referenced_class}')
                    # find result class in module
                    # use <model>.model_parse() to try to deserialize the body
                    foo = 1
        if err:
            raise err

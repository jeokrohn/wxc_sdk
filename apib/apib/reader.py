"""
Helper to read on apib file as dict
"""
import json
import subprocess

__all__ = ['read_api_blueprint']

import sys
from os.path import isfile


def read_api_blueprint(path: str) -> dict:
    """
    read apib file from path and return a dict representation.

    'drafter' is used to convert the APIB to json and then the json output is read
    :param path:
    :return:
    """
    if not isfile(path):
        raise FileNotFoundError(f'not found: {path}')
    # run the external program
    process = subprocess.Popen(['drafter', '-f', 'json', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # read the output from stdout
    output, error = process.communicate()

    error = error.decode().strip()
    if error and error.splitlines()[0].strip() != 'OK.':
        print(f'error: {error}', file=sys.stderr)
        raise RuntimeError(f'error: {error}')
    # print the output
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        print('print failed to parse JSON', file=sys.stderr)
        raise
    return data

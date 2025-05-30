#!/usr/bin/env python
"""
CLI tool to generate Python source from OpenApi specs
    usage: apib2py.py [-h] [--pypath PYPATH] [--pysrc PYSRC] [--nobeta] [--exclude EXCLUDE] [--with-unref] apib

    positional arguments:
      apib               name of API file. If name is given w/o oath then default path from environment APIB_PATH
                         (if present) is used to determine the absolute path of the APIB source. Parameter value
                         is interpreted as glob wildcard.

    optional arguments:
      -h, --help         show this help message and exit
      --pypath PYPATH    dir path to store result in .. if not target with path is given. if parameter is missing
                         then path is read from environment PY_PATH (if present)
      --pysrc PYSRC      filename (w/ or w/o path) of python source to generate, "-" to print source to stdout. If
                         parameter is missing then the output name is based on the basename of given APIB name
      --nobeta           Exclude all "beta-" APIB files
      --exclude EXCLUDE  Python.re to exclude some APIB files; matches on basenames of APIB files
      --with-unref       include unreferenced classes
"""
import argparse
import glob
import logging
import os
import re
import shutil
import sys
import traceback
from contextlib import contextmanager
from os.path import basename
from pathlib import Path

from dotenv import load_dotenv

from open_api.open_api_code_generator import OACodeGenerator


def main():
    logging.basicConfig(level=logging.INFO)
    env_path = f'{os.path.splitext(__file__)[0]}.env'
    load_dotenv(env_path)

    parser = argparse.ArgumentParser(description='Convert OpenApi specs to Python source',
                                     epilog=f'Environment is read from {env_path} if present.')
    parser.add_argument('--oas', type=str,
                        help='name of OpenApi spec file. If name is given w/o path then default path from environment '
                             'OAS_SPEC_PATH (if present) is used to determine the absolute path of the APIB source. '
                             'Parameter value is interpreted as glob wildcard.')
    parser.add_argument('--pypath', type=str,
                        help='dir path to store result in .. if not target with path is given. if parameter is '
                             'missing then path is read from environment OAS_PY_PATH (if present). If the path ends '
                             'with "/" then the folder hierarchy of the OAS specs is recreated for the created Python '
                             'sources.')
    parser.add_argument('--pysrc', type=str,
                        help='filename (w/ or w/o path) of python source to generate, "-" to print source to stdout. '
                             'If parameter is missing then the output name is based on the basename of given APIB name')
    parser.add_argument('--exclude', type=str,
                        help='Python.re to exclude some OAS files; matches on basenames of OAS files')
    parser.add_argument('--with-unref', action='store_true',
                        help='include unreferenced classes')
    parser.add_argument('--with-examples', action='store_true',
                        help='include example values for attributes')
    parser.add_argument('--raise', action='store_true',
                        help='raise exception on error instead of printing to stderr',
                        dest='raise_exception')
    parser.add_argument('--cleanup', action='store_true', help='delete all .py files in the output directory.')
    args = parser.parse_args()

    oas_path = args.oas or ''
    oas_dirname, oas_basename = os.path.split(oas_path)
    if oas_basename:
        if oas_basename == '**':
            # a given basename of "**" means all files
            oas_basename = '**/spec.json'
        if not "*" in oas_basename:
            # a given basename is interpreted as the name of an API
            # and API specs are stored in dir structure like:
            # /<some hierarchy>/<name>/v1/spec.json
            oas_basename = os.path.join('**', oas_basename, '**', 'spec.json')
    else:
        oas_basename = oas_basename or '**/spec.json'
    oas_spec_path = os.getenv('OAS_SPEC_PATH')
    if not oas_dirname:
        from_env = oas_spec_path
        if from_env:
            print(f'got oas path "{from_env}" from "{env_path}"')
            oas_path = os.path.join(from_env, oas_basename)
    else:
        if os.path.isdir(oas_dirname):
            oas_path = os.path.join(oas_dirname, oas_basename)
        elif os.path.isdir(os.path.join(oas_spec_path, oas_dirname)):
            oas_path = os.path.join(oas_spec_path, oas_dirname, oas_basename)
    oas_files = glob.glob(oas_path, recursive=True)
    oas_files.sort()

    if args.exclude:
        try:
            re_exclude = re.compile(args.exclude)
        except re.error as e:
            print(f'Invalid reqex for --exclude: {e}',
                  file=sys.stderr)
            exit(1)
        oas_files = [p for p in oas_files
                     if not re_exclude.match(basename(p))]

    if not oas_files:
        print(f'No input OAS file(s)',
              file=sys.stderr)
        exit(1)

    with_examples = args.with_examples or False

    py_path = args.pypath
    if py_path is not None:
        # if the path is given then use it
        py_path_has_slash = py_path.endswith('/')
        py_path = os.path.abspath(py_path)
        if py_path_has_slash:
            py_path = f'{py_path}/'
        if not os.path.isdir(py_path):
            print(f'Path "{py_path}" does not exist',
                  file=sys.stderr)
            exit(1)

    if args.cleanup:
        cleanup_py_path = py_path or os.getenv('OAS_PY_PATH') or ''
        if not cleanup_py_path:
            print('No path given for cleanup, use --pypath to specify the path',
                  file=sys.stderr)
            exit(1)
        cleanup_py_path = Path(cleanup_py_path)
        if not cleanup_py_path.exists():
            print(f'Path "{cleanup_py_path}" does not exist',
                  file=sys.stderr)
            exit(1)
        for item in cleanup_py_path.iterdir():
            if item.is_file() or item.is_symlink():
                print(f'Removing file or symlink: {item}')
                item.unlink()  # Remove file or symlink
            elif item.is_dir():
                print(f'Removing directory and all contents: {item}')
                shutil.rmtree(item)  # Remove directory and all contents
        exit(0)

    # conversion for each OAS file
    def convert_one_oas(oas_path: str):
        """
        Convert one OAS file
        """
        code_gen = OACodeGenerator(with_unreferenced_classes=args.with_unref)
        code_gen.add_open_api_spec_from_path(oas_path)
        code_gen.cleanup()

        @contextmanager
        def output_ctx(spec_path: str):
            # determine output for Python source
            pysrc = args.pysrc
            if pysrc == '-':
                yield sys.stdout
            else:
                if not pysrc:
                    path_components = spec_path.split(os.sep)
                    if path_components[-2] == 'v1':
                        # something like "people"
                        py_basename = path_components[-3]
                    else:
                        # something like "people_v2"
                        py_basename = f'{path_components[-3]}_{path_components[-2]}'
                    py_basename = f'{py_basename}_auto.py'
                    oas_py_path = py_path or os.getenv('OAS_PY_PATH') or ''
                    if oas_spec_path and spec_path.startswith(oas_spec_path) and oas_py_path.endswith('/'):
                        # for OAS specs that are under the spec path re-create the directory structure in the target
                        # directory
                        # ignore the start of the path and the last 3 components
                        # we only want the hierarchy, not the spec name: /<some hierarchy>/<name>/v1/spec.json
                        rel_dir = spec_path[len(oas_spec_path):].strip(os.sep)
                        rel_dirs = rel_dir.split(os.sep)[:-3]
                        dirname = os.path.join(oas_py_path, *rel_dirs)
                        # make sure that the directories exist
                        if not os.path.isdir(dirname):
                            os.makedirs(dirname)
                        pysrc = os.path.join(dirname, py_basename)
                    else:
                        # if the path is not given then use the name of the OAS file
                        pysrc = os.path.join(oas_py_path, py_basename)
                    # if
                # if
                print(f'.. writing output to "{pysrc}"')
                with open(pysrc, mode='w') as f:
                    yield f
            return

        with output_ctx(oas_path) as f:
            print(code_gen.source(with_example=with_examples),
                  end='',
                  file=f)
        return

    failed_oas_files = []
    for oas_file in oas_files:
        print(f'Conversion of "{oas_file}"')
        try:
            convert_one_oas(oas_file)
        except Exception:
            if args.raise_exception:
                raise
            failed_oas_files.append(oas_file)
            print(f'Conversion of "{oas_file}" failed:',
                  file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
    if failed_oas_files:
        print('\n' * 2, file=sys.stderr)
        print(f'Conversion of {len(failed_oas_files)} OAS files failed:', file=sys.stderr)
        for failed_file in failed_oas_files:
            print(f'  {failed_file}', file=sys.stderr)
        exit(1)
    exit(0)


if __name__ == '__main__':
    main()

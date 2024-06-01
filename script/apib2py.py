#!/usr/bin/env python
"""
CLI tool to generate Python source from APIB file
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
import os
import re
import sys
import traceback
from contextlib import contextmanager
from os.path import basename, splitext

from dotenv import load_dotenv

from apib.generator import CodeGenerator


def main():
    env_path = f'{os.path.splitext(__file__)[0]}.env'
    load_dotenv(env_path)

    parser = argparse.ArgumentParser()
    parser.add_argument('apib', type=str,
                        help='name of API file. If name is given w/o path then default path from environment '
                             'APIB_PATH (if present) is used to determine the absolute path of the APIB source. '
                             'Parameter value is interpreted as glob wildcard.')
    parser.add_argument('--pypath', type=str,
                        help='dir path to store result in .. if not target with path is given. if parameter is '
                             'missing then path is read from environment PY_PATH (if present)')
    parser.add_argument('--pysrc', type=str,
                        help='filename (w/ or w/o path) of python source to generate, "-" to print source to stdout. '
                             'If parameter is missing then the output name is based on the basename of given APIB name')
    parser.add_argument('--nobeta', action='store_true',
                        help='Exclude all "beta-" APIB files')
    parser.add_argument('--exclude', type=str,
                        help='Python.re to exclude some APIB files; matches on basenames of APIB files')
    parser.add_argument('--with-unref', action='store_true',
                        help='include unreferenced classes')
    parser.add_argument('--with-examples', action='store_true',
                        help='include example values for attributes')
    args = parser.parse_args()

    apib_path = args.apib
    apib_dirname, apib_basename = os.path.split(apib_path)
    if not apib_dirname:
        from_env = os.getenv('APIB_PATH')
        if from_env:
            print(f'got apib path "{from_env}" from "{env_path}"')
            apib_path = os.path.join(from_env, apib_basename)
    apib_files = glob.glob(apib_path, recursive=False)
    apib_files.sort()

    if args.nobeta:
        apib_files = [p for p in apib_files
                      if not basename(p).startswith('beta-')]

    if args.exclude:
        try:
            re_exclude = re.compile(args.exclude)
        except re.error as e:
            print(f'Invalid reqex for --exclude: {e}',
                  file=sys.stderr)
            exit(1)
        apib_files = [p for p in apib_files
                      if not re_exclude.match(basename(p))]

    if not apib_files:
        print(f'No input APIB file(s)',
              file=sys.stderr)
        exit(1)

    with_examples = args.with_examples or False

    # conversion for each APIB files
    def convert_one_apib(apib_path: str):
        """
        Convert one APIB file
        """
        code_gen = CodeGenerator(with_unreferenced_classes=args.with_unref)
        code_gen.read_blueprint(apib_path)
        code_gen.cleanup()

        @contextmanager
        def output_ctx():
            # determine output for Python source
            pysrc = args.pysrc
            if pysrc == '-':
                yield sys.stdout
            else:
                if not pysrc:
                    # determine basename based on basename of APIB file
                    pysrc = f'{splitext(basename(apib_path))[0]}_auto.py'
                path, base = os.path.split(pysrc)
                if not path:
                    path = args.pypath or os.getenv('PY_PATH')
                    if path:
                        pysrc = os.path.join(path, base)
                print(f'.. writing output to "{pysrc}"')
                with open(pysrc, mode='w') as f:
                    yield f
            return

        with output_ctx() as f:
            print(code_gen.source(with_example=with_examples),
                  end='',
                  file=f)

    err = False
    for apib_file in apib_files:
        print(f'Conversion of "{apib_file}"')
        try:
            convert_one_apib(apib_file)
        except Exception:
            err = True
            print(f'Conversion of "{apib_file}" failed:',
                  file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
    if err:
        exit(1)
    exit(0)


if __name__ == '__main__':
    main()

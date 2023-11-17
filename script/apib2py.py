#!/usr/bin/env python
"""
CLI tool to generate Python source from APIB file
"""
import argparse
import os

from dotenv import load_dotenv

from apib.generator import CodeGenerator


def main():
    env_path = f'{os.path.splitext(__file__)[0]}.env'
    load_dotenv(env_path)

    parser = argparse.ArgumentParser()
    parser.add_argument('apib', type=str, help='path to API file')
    parser.add_argument('--pypath', type=str, help='dir path to store result in .. if not target with path is given')
    parser.add_argument('--pysrc', type=str, help='filename (w/ or w/o path) of python source to generate')
    args = parser.parse_args()

    apib_path = args.apib
    apib_dirname, apib_basename = os.path.split(apib_path)
    if not apib_dirname:
        apib_dirname = os.getenv('APIB_PATH') or ''
    apib_path = os.path.join(apib_dirname, apib_basename)

    code_gen = CodeGenerator()
    code_gen.read_blueprint(apib_path)
    code_gen.cleanup()
    print(code_gen.source())


if __name__ == '__main__':
    main()

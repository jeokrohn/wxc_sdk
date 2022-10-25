#!/usr/bin/env python
"""
Read API specs from developer.webex.com using Selenium and write as YML

usage: read_api_spec.py [-h] [-f [YML_PATH]] [-d] [-l [LOG_PATH]]

optional arguments:
  -h, --help            show this help message and exit
  -f [YML_PATH], --file [YML_PATH]
                        write YML to file. Default: read_api_spec.yml
  -d, --debug           show debugs on console
  -l [LOG_PATH], --logfile [LOG_PATH]
                        Write detailed logs to this file. Default:
                        read_api_spec.log

"""
import argparse
import logging
import os
from typing import Optional

from yaml import safe_dump

from scraper import DevWebexComScraper, DocMethodDetails


def setup_logging(console_level: int = logging.INFO,
                  log_path: Optional[str] = None):
    """
    Setup logging

    :param console_level: logging level for console (stderr)
    :param log_path: path to log file
    """

    # enable debugging
    logging.getLogger('urllib3').setLevel(logging.INFO)
    logging.getLogger('selenium').setLevel(logging.INFO)

    # log to console level INFO
    # log to file level DEBUG
    logger = logging.getLogger()
    if log_path:
        fmt = logging.Formatter(fmt='%(levelname)5s:%(name)s:%(message)s')

        file_handler = logging.FileHandler(filename=log_path, mode='w')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(console_level)
    logger.addHandler(stream_handler)

    logger.setLevel(logging.DEBUG)


def main():
    parser = argparse.ArgumentParser()
    default_name = f'{os.path.splitext(os.path.basename(__file__))[0]}'

    # specify file a file to write the YML with the API specs to
    # if not given then YML is written to stdout.
    parser.add_argument('-f', '--file', dest='yml_path', action='store', required=False, type=str, nargs='?',
                        const=f'{default_name}.yml', help=f'Write YML to file. Default: {default_name}.yml')

    # enable debug output to stderr
    parser.add_argument('-d', '--debug', action='store_true', help='show debugs on console')

    # write detailed logs (debug level) to a file
    parser.add_argument('-l', '--logfile', dest='log_path', action='store', required=False, type=str, nargs='?',
                        const=f'{default_name}.log',
                        help=f'Write detailed logs to this file. Default: {default_name}.log')
    args = parser.parse_args()

    setup_logging(console_level=logging.DEBUG if args.debug else logging.INFO,
                  log_path=args.log_path)

    doc_details = DocMethodDetails()

    with DevWebexComScraper() as site:
        # get information about existing documentation from developer.webex.com
        docs = site.get_calling_docs()

        # get method details
        for doc in docs:
            logging.info(f'"{doc.menu_text}"')
            doc_details.docs[doc.menu_text] = [md for md in map(site.get_method_details, doc.methods)
                                               if md]
    # with

    # write API spec to file or print to stdout
    if args.yml_path:
        doc_details.to_yml(args.yml_path)
    else:
        print(doc_details.to_yml())


if __name__ == '__main__':
    main()
    exit(0)

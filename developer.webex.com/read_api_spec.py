#!/usr/bin/env python
"""
Read API specs from developer.webex.com using Selenium and write as YML

usage: read_api_spec.py [-h] [-f [YML_PATH]] [-d] [-l [LOG_PATH]] [-b BASELINE] [-n] [-u USER] [-p PASSWORD] [-a AUTH]

optional arguments:
  -h, --help            show this help message and exit
  -f [YML_PATH], --file [YML_PATH]
                        Write YML to file. Default: read_api_spec.yml
  -d, --debug           show debugs on console
  -l [LOG_PATH], --logfile [LOG_PATH]
                        Write detailed logs to this file. Default: read_api_spec.log
  -b BASELINE, -base BASELINE
                        take given API spec YML as baseline
  -n, --newonly         only read new endpoints. Can only be used together with -b
  -u USER, --user USER  username for authentication
  -p PASSWORD, --password PASSWORD
                        password for authentication
  -a AUTH, --auth AUTH  filename of file with credentials in .env file format

"""
# TODO: Webex Calling Detailed Call History, Get Detailed Call History
#   https://developer.webex.com/docs/api/v1/webex-calling-detailed-call-history/get-detailed-call-history
#   * that should actually be a follow-pagination
# TODO: Call Pickups
#   generated HostedAgentType is actually an enum
import argparse
import logging
import os
import sys
from sys import stderr
from typing import Optional

from dotenv import load_dotenv

from scraper import DevWebexComScraper, DocMethodDetails, Credentials, SectionDetails


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

    parser.add_argument('-b', '-base', dest='baseline', required=False, type=str,
                        help='take given API spec YML as baseline')
    parser.add_argument('-n', '--newonly', required=False, action='store_true',
                        help='only read new endpoints. Can only be used together with -b')
    parser.add_argument('-u', '--user', required=False, type=str, help='username for authentication')
    parser.add_argument('-p', '--password', required=False, type=str, help='password for authentication')
    parser.add_argument('-a', '--auth', required=False, type=str,
                        help='filename of file with credentials in .env file format')

    parser.add_argument('-s', '--section', required=False, type=str, help='section to read. For example "Calling". '
                                                                          'Default: "Calling"',
                        nargs='?', const='Calling', default='Calling')
    parser.add_argument('-t', '--tabs', required=False, type=str, help='tab to parse. Example: "Locations". To read '
                                                                       'all tabs a value of "all" can be used.',
                        default='all', nargs='*')
    parser.add_argument('--no_ignore', help='Include all sections and don\'t skip stuff like "Wholesale Customer", ...',
                        action='store_true')

    args = parser.parse_args()

    if args.baseline and args.tabs != 'all':
        print('-b not acceptable to gether with tab spec', file=stderr)
        exit(1)

    if args.newonly and not args.baseline:
        print('-n only acceptable together with -b', file=stderr)
        exit(1)

    credentials = None
    if any((args.user, args.password)):
        if args.auth:
            print('Can\'t use auth file together with user or password')
            exit(1)
        if all((args.user, args.password)):
            credentials = Credentials(user=args.user, password=args.password)
            ...
        else:
            print('both, user and password need to be given', file=stderr)
            exit(1)

    if args.auth:
        # read env file and get credentials from file
        load_dotenv(args.auth)
        user = os.getenv('WEBEX_USER')
        password = os.getenv('WEBEX_PASSWORD')
        if not all((user, password)):
            print(f'Auth file {args.auth} needs to have values for both, WEBEX_USER and WEBEX_PASSWORD', file=stderr)
            exit(1)
        credentials = Credentials(user=user, password=password)

    setup_logging(console_level=logging.DEBUG if args.debug else logging.INFO,
                  log_path=args.log_path)

    param_strings = [f'"{s}"' if ' ' in s else s for s in sys.argv]
    doc_details = DocMethodDetails(info=f'command: {" ".join(param_strings)}')

    if args.baseline:
        logging.info(f'reading base api spec from {args.baseline}')
        baseline = DocMethodDetails.from_yml(args.baseline)
    else:
        baseline = None

    with DevWebexComScraper(credentials=credentials, baseline=baseline, new_only=args.newonly,
                            section=args.section, tabs=args.tabs, ignore_non_core=not args.no_ignore) as site:
        # get information about existing documentation from developer.webex.com
        docs = site.get_section_docs()

        # get method details
        for doc in docs:
            logging.info(f'"{doc.menu_text}"')
            method_details = [md for md in map(site.get_method_details, doc.methods)
                              if md]
            section_details = SectionDetails(header=doc.header,
                                             doc=doc.doc,
                                             methods=method_details)
            doc_details.docs[doc.menu_text] = section_details
    # with

    # write API spec to file or print to stdout
    if args.yml_path:
        logging.info(f'writing to {args.yml_path}')
        doc_details.to_yml(args.yml_path)
    else:
        print(doc_details.to_yml())


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print(f'failed to run {", ".join(sys.argv)}')
        raise
    exit(0)

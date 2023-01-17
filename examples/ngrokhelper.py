"""
Module to simplify the use of ngrok to get a public URL for our bot
"""
import logging
import os
import shutil
import subprocess

import backoff
import requests

log = logging.getLogger(__name__)

__all__ = ['get_public_url']


def poll_exception(e: Exception):
    # print(f'{e}')
    return False


@backoff.on_exception(backoff.constant,
                      (requests.ConnectionError, KeyError, StopIteration),
                      interval=2,
                      giveup=poll_exception,
                      max_time=10)
def poll_ngrok_for_url(host: str) -> str:
    """
    Poll Ngrok client API to get public https:// URL. Maximum time: 10 seconds

    :param host: Ngrok host to poll
    :return:
    """
    # noinspection HttpUrlsUsage
    url = f'http://{host}:4040/api/tunnels'
    with requests.Session() as session:
        with session.get(url) as response:
            response.raise_for_status()
            data = response.json()
    # we are looking for an HTTPS tunnel. KeyError and StopIteration indicate that no HTTPS tunnel exists ... yet
    tunnel = next(tunnel for tunnel in data['tunnels']
                  if tunnel['proto'] == 'https')
    return tunnel['public_url']


def get_public_url(local_port: int) -> str:
    """
    Get public URL for local service. If environment informs us about Ngrok host then poll that host.
    Else start a local ngrok instance and poll that instance

    :param local_port: local port the webservice runs on
    :type local_port: int
    :return:
    """
    ngrok_host = os.getenv('NGROK_HOST') or None
    log.debug(f'NGROK_HOST: {ngrok_host}')
    if ngrok_host is None:
        # start a local ngrok instance and then poll on localhost
        # where is ngrok?
        ngrok = shutil.which('ngrok')

        # commandline to start ngrok
        cmd = f'{ngrok} http {local_port}'

        # start ngrok process
        log.debug(f'NGROK_HOST not set, starting ngrok, command: {cmd}')
        subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        ngrok_host = 'localhost'
    # simply poll the running ngrok for public address
    bot_url = poll_ngrok_for_url(host=ngrok_host)
    return bot_url

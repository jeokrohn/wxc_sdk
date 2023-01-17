#!/usr/bin/env python
"""
Create a firehose webhook and dump events to stdout
"""
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from json import dumps
from typing import Optional
from uuid import uuid4

from dotenv import load_dotenv
from flask import Flask, request

from examples import ngrokhelper
from wxc_sdk import WebexSimpleApi
from wxc_sdk.tokens import Tokens
from wxc_sdk.integration import Integration
from wxc_sdk.scopes import parse_scopes
from wxc_sdk.webhook import WebhookEvent

LOCAL_APP_PORT = 6001


def env_path() -> str:
    """
    determine path for .env to load environment variables from

    :return: .env file path
    """
    return os.path.join(os.getcwd(), f'{os.path.splitext(os.path.basename(__file__))[0]}.env')


def yml_path() -> str:
    """
    determine path of YML file to persist tokens

    :return: path to YML file
    :rtype: str
    """
    return os.path.join(os.getcwd(), f'{os.path.splitext(os.path.basename(__file__))[0]}.yml')


def build_integration() -> Integration:
    """
    read integration parameters from environment variables and create an integration

    :return: :class:`wxc_sdk.integration.Integration` instance
    """
    client_id = os.getenv('TOKEN_INTEGRATION_CLIENT_ID')
    client_secret = os.getenv('TOKEN_INTEGRATION_CLIENT_SECRET')
    scopes = parse_scopes(os.getenv('TOKEN_INTEGRATION_CLIENT_SCOPES'))
    redirect_url = 'http://localhost:6001/redirect'
    if not all((client_id, client_secret, scopes)):
        raise ValueError('failed to get integration parameters from environment')
    return Integration(client_id=client_id, client_secret=client_secret, scopes=scopes,
                       redirect_url=redirect_url)


def get_tokens() -> Optional[Tokens]:
    """
    Tokens are read from a YML file. If needed an OAuth flow is initiated.

    :return: tokens
    :rtype: :class:`wxc_sdk.tokens.Tokens`
    """

    integration = build_integration()
    tokens = integration.get_cached_tokens_from_yml(yml_path=yml_path())
    return tokens


# set up logging for the app
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(process)d] %(threadName)s %(levelname)s %(name)s %('
                                                'message)s')
logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
logging.getLogger('webexteamssdk.restsession').setLevel(logging.WARNING)

# to disable logging of WXC SDK REST messages change the log level
logging.getLogger('wxc_sdk.rest').setLevel(logging.DEBUG)

log = logging.getLogger(__name__)

load_dotenv(env_path())


@dataclass(init=False)
class FireHose(Flask):
    """
    A Firehose webhook listener
    """
    api: WebexSimpleApi

    def __init__(self,
                 *,
                 api: WebexSimpleApi,
                 base_url: str):
        """
        """
        super().__init__('FireHose')
        self.api = api
        self.instance_id = f'{uuid4()}'

        # register URL for messages to webhook
        self.add_url_rule(
            f'/', "index", self.process_incoming_message, methods=["POST"]
        )

        # get list of webhooks and delete all existing webhooks
        wh_list = list(api.webhook.list())
        wh_name = self.__class__.__name__
        # delete all webhooks which smell like leftovers
        with ThreadPoolExecutor() as pool:
            list(pool.map(lambda wh: api.webhook.webhook_delete(webhook_id=wh.webhook_id),
                          (wh for wh in wh_list if wh.name.startswith(wh_name))))
        wh = api.webhook.create(name=wh_name, resource='all', event='all', target_url=base_url)
        return

    def process_incoming_message(self):
        """
        Process an incoming message, determine the command and action,
        and determine reply.
        :return:
        """
        reply = None

        # Get the webhook data
        post_data = request.json
        log.debug(dumps(post_data, indent=2))
        try:
            wh_event: WebhookEvent = WebhookEvent.parse_obj(post_data)
            log.debug(f'{wh_event}')
            log.debug(f'{wh_event.resource} parsed as {wh_event.data.__class__.__name__}')
        except Exception as e:
            log.error(f'Failed to parse: {e}')
        return ''


def create_app() -> Optional[FireHose]:
    """
    Create a FireHose instance
    """
    # get tokens
    tokens = get_tokens()
    if not tokens or not tokens.access_token:
        print('Failed to obtain tokens', file=sys.stderr)
        return None
    api = WebexSimpleApi(tokens=tokens)

    # determine public URL for Bot
    base_url = ngrokhelper.get_public_url(local_port=LOCAL_APP_PORT)
    log.debug(f'Webhook base URL: {base_url}')

    app = FireHose(api=api, base_url=base_url)
    return app


if __name__ == '__main__':
    app = create_app()
    if app is None:
        exit(1)
    app.run(host='0.0.0.0', port=LOCAL_APP_PORT)

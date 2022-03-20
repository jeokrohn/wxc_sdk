"""
Simple SDK for Webex APIs with focus on Weebx Calling specific endpoints
"""
import logging
import os
from typing import Union

from .licenses import LicensesApi
from .locations import LocationsApi
from .people import PeopleApi
from .person_settings import PersonSettingsApi
from .rest import RestSession
from .telephony import TelephonyApi
from .tokens import Tokens
from .webhook import WebhookApi

__all__ = ['WebexSimpleApi']

__version__ = '0.1.0'

log = logging.getLogger(__name__)


class WebexSimpleApi:
    """
    The main API object

    :ivar licenses: :class:`licenses.LicensesApi`
    :ivar locations: :class:`locations.LocationsApi`
    :ivar person_settings: :class:`person_settings.PersonSettingsApi`
    :ivar people: :class:`people.PeopleApi`
    :ivar telephony: :class:`telephony.TelephonyApi`
    :ivar webhook: :class:`webhook.WebhookApi`
    """
    #: Webhooks API :class:`webhook.WebhookApi`
    webhook: WebhookApi

    def __init__(self, *, tokens: Union[str, Tokens] = None, concurrent_requests: int = 10):
        """

        :param tokens: token to be used by the API. Can be a :class:`tokens.Tokens` instance, a string or None. If
            None then an access token is expected in the WEBEX_ACCESS_TOKEN environment variable.
        :param concurrent_requests: number of concurrent requests when using multi-threading
        :type concurrent_requests: int
        """
        if isinstance(tokens, str):
            tokens = Tokens(access_token=tokens)
        elif tokens is None:
            tokens = os.getenv('WEBEX_ACCESS_TOKEN')
            if tokens is None:
                raise ValueError('if no access token is passed, then a valid access token has to be present in '
                                 'WEBEX_ACCESS_TOKEN environment variable')
            tokens = Tokens(access_token=tokens)

        # :class:`rest.RestSession` used for all API requests
        self.session = RestSession(tokens=tokens, concurrent_requests=concurrent_requests)
        #: Licenses API :class:`licenses.LicensesApi`
        self.licenses = LicensesApi(session=self.session)
        #: Location API :class:`locations.LocationsApi`
        self.locations = LocationsApi(session=self.session)
        #: Person settings API :class:`person_settings.PersonSettingsApi`
        self.person_settings = PersonSettingsApi(session=self.session)
        #: People API :class:`people.PeopleApi`
        self.people = PeopleApi(session=self.session)
        #: Telephony API :class:`telephony.TelephonyApi`
        self.telephony = TelephonyApi(session=self.session)
        #: Webhooks API :class:`webhook.WebhookApi`
        self.webhook = WebhookApi(session=self.session)

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

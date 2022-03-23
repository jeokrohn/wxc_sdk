"""
Simple SDK for Webex APIs with focus on Webex Calling specific endpoints
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
from dataclasses import dataclass

__all__ = ['WebexSimpleApi']

__version__ = '0.3.1'

log = logging.getLogger(__name__)


@dataclass(init=False)
class WebexSimpleApi:
    """
    The main API object

    """

    #: Licenses API :class:`licenses.LicensesApi`
    licenses: LicensesApi
    #: Location API :class:`locations.LocationsApi`
    locations: LocationsApi
    #: Person settings API :class:`person_settings.PersonSettingsApi`
    person_settings: PersonSettingsApi
    #: People API :class:`people.PeopleApi`
    people: PeopleApi
    #: Telephony API :class:`telephony.TelephonyApi`
    telephony: TelephonyApi
    #: Webhooks API :class:`webhook.WebhookApi`
    webhook: WebhookApi
    #: :class:`rest.RestSession` used for all API requests
    session: RestSession

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

        session = RestSession(tokens=tokens, concurrent_requests=concurrent_requests)
        self.licenses = LicensesApi(session=session)
        self.locations = LocationsApi(session=session)
        self.person_settings = PersonSettingsApi(session=session)
        self.people = PeopleApi(session=session)
        self.telephony = TelephonyApi(session=session)
        self.webhook = WebhookApi(session=session)
        self.session = session

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

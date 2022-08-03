"""
Simple SDK for Webex APIs with focus on Webex Calling specific endpoints
"""
import logging
import os
from typing import Union

from .groups import GroupsApi
from .licenses import LicensesApi
from .locations import LocationsApi
from .people import PeopleApi
from .person_settings import PersonSettingsApi
from .rest import RestSession
from .telephony import TelephonyApi
from .tokens import Tokens
from .webhook import WebhookApi
from .workspaces import WorkspacesApi
from .workspace_settings import WorkspaceSettingsApi
from dataclasses import dataclass

__all__ = ['WebexSimpleApi']

__version__ = '1.5.2'

log = logging.getLogger(__name__)


# TODO: devices


@dataclass(init=False)
class WebexSimpleApi:
    """
    The main API object
    """

    #: groups API :class:`groups.GroupsApi`
    groups: GroupsApi
    #: Licenses API :class:`licenses.LicensesApi`
    licenses: LicensesApi
    #: Location API :class:`locations.LocationsApi`
    locations: LocationsApi
    #: Person settings API :class:`person_settings.PersonSettingsApi`
    person_settings: PersonSettingsApi
    #: People API :class:`people.PeopleApi`
    people: PeopleApi
    #: Telephony (features) API :class:`telephony.TelephonyApi`
    telephony: TelephonyApi
    #: Webhooks API :class:`webhook.WebhookApi`
    webhook: WebhookApi
    #: Workspaces API :class:`workspaces.WorkspacesApi`
    workspaces: WorkspacesApi
    #: Workspace setting API :class:`workspace_settings.WorkspaceSettingsApi`
    workspace_settings: WorkspaceSettingsApi
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
        self.groups = GroupsApi(session=session)
        self.licenses = LicensesApi(session=session)
        self.locations = LocationsApi(session=session)
        self.person_settings = PersonSettingsApi(session=session)
        self.people = PeopleApi(session=session)
        self.telephony = TelephonyApi(session=session)
        self.webhook = WebhookApi(session=session)
        self.workspaces = WorkspacesApi(session=session)
        self.workspace_settings = WorkspaceSettingsApi(session=session)
        self.session = session

    @property
    def access_token(self) -> str:
        """
        access token used for all requests

        :return: access token
        :rtype: str
        """
        return self.session.access_token

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

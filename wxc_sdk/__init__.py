"""
Simple SDK for Webex APIs with focus on Webex Calling specific endpoints
"""
import logging
import os
from typing import Union

from .attachment_actions import AttachmentActionsApi
from .cdr import DetailedCDRApi
from .devices import DevicesApi
from .events import EventsApi
from .groups import GroupsApi
from .licenses import LicensesApi
from .locations import LocationsApi
from .memberships import MembershipApi
from .messages import MessagesApi
from .organizations import OrganizationApi
from .people import PeopleApi
from .person_settings import PersonSettingsApi
from .reports import ReportsApi
from .rest import RestSession
from .room_tabs import RoomTabsApi
from .rooms import RoomsApi
from .team_memberships import TeamMembershipsApi
from .teams import TeamsApi
from .telephony import TelephonyApi
from .tokens import Tokens
from .webhook import WebhookApi
from .workspace_locations import WorkspaceLocationApi
from .workspaces import WorkspacesApi
from .workspace_settings import WorkspaceSettingsApi
from dataclasses import dataclass

__all__ = ['WebexSimpleApi']

__version__ = '1.11.0'

log = logging.getLogger(__name__)


# noinspection PyShadowingNames
@dataclass(init=False)
class WebexSimpleApi:
    """
    The main API object
    """

    #: Attachment actions API :class:`attachment_actions.AttachmentActionsApi`
    attachment_actions: AttachmentActionsApi
    #: CDR API :class:`cdr.DetailedCDRApi`
    cdr: DetailedCDRApi
    #: devices API :class:`devices.DevicesApi`
    devices: DevicesApi
    #: events API; :class:`events.EventsApi`
    events: EventsApi
    #: groups API :class:`groups.GroupsApi`
    groups: GroupsApi
    #: Licenses API :class:`licenses.LicensesApi`
    licenses: LicensesApi
    #: Location API :class:`locations.LocationsApi`
    locations: LocationsApi
    #: membership API :class:`memberships.MembershipApi`
    membership: MembershipApi
    #: Messages API :class:`messages.MessagesApi`
    messages: MessagesApi
    #: organization settings API
    organizations: OrganizationApi
    #: Person settings API :class:`person_settings.PersonSettingsApi`
    person_settings: PersonSettingsApi
    #: People API :class:`people.PeopleApi`
    people: PeopleApi
    #: Reports API :class:`reports.ReportsApi`
    reports: ReportsApi
    #: Rooms API :class:`rooms.RoomsApi`
    rooms: RoomsApi
    #: Room tabs API :class:`room_tabs.RoomTabsApi`
    room_tabs: RoomTabsApi
    #: Teams API :class:`teams.TeamsApi`
    teams: TeamsApi
    #: Team memberships API :class:`TeamMembershipsApi`
    team_memberships: TeamMembershipsApi
    #: Telephony (features) API :class:`telephony.TelephonyApi`
    telephony: TelephonyApi
    #: Webhooks API :class:`webhook.WebhookApi`
    webhook: WebhookApi
    #: Workspaces API :class:`workspaces.WorkspacesApi`
    workspaces: WorkspacesApi
    #: Workspace locations API; :class:`workspace_locations.WorkspaceLocationApi`
    workspace_locations: WorkspaceLocationApi
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
        self.attachment_actions = AttachmentActionsApi(session=session)
        self.cdr = DetailedCDRApi(session=session)
        self.devices = DevicesApi(session=session)
        self.events = EventsApi(session=session)
        self.groups = GroupsApi(session=session)
        self.licenses = LicensesApi(session=session)
        self.locations = LocationsApi(session=session)
        self.membership = MembershipApi(session=session)
        self.messages = MessagesApi(session=session)
        self.organizations = OrganizationApi(session=session)
        self.person_settings = PersonSettingsApi(session=session)
        self.people = PeopleApi(session=session)
        self.reports = ReportsApi(session=session)
        self.rooms = RoomsApi(session=session)
        self.room_tabs = RoomTabsApi(session=session)
        self.teams = TeamsApi(session=session)
        self.team_memberships = TeamMembershipsApi(session=session)
        self.telephony = TelephonyApi(session=session)
        self.webhook = WebhookApi(session=session)
        self.workspaces = WorkspacesApi(session=session)
        self.workspace_locations = WorkspaceLocationApi(session=session)
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

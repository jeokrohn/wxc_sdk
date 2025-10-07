"""
Simple SDK for Webex APIs with focus on Webex Calling specific endpoints
"""
import logging
import os
from dataclasses import dataclass
from typing import Union

from .admin_audit import AdminAuditEventsApi
from .attachment_actions import AttachmentActionsApi
from .authorizations import AuthorizationsApi
from .cdr import DetailedCDRApi
from .converged_recordings import ConvergedRecordingsApi
from .device_configurations import DeviceConfigurationsApi
from .devices import DevicesApi
from .events import EventsApi
from .groups import GroupsApi
from .guests import GuestManagementApi
from .licenses import LicensesApi
from .locations import LocationsApi
from .me import MeSettingsApi
from .meetings import MeetingsApi
from .memberships import MembershipApi
from .messages import MessagesApi
from .org_contacts import OrganizationContactsApi
from .organizations import OrganizationApi
from .people import PeopleApi
from .person_settings import PersonSettingsApi
from .reports import ReportsApi
from .rest import RestSession
from .roles import RolesApi
from .room_tabs import RoomTabsApi
from .rooms import RoomsApi
from .scim import ScimV2Api
from .status import StatusAPI
from .team_memberships import TeamMembershipsApi
from .teams import TeamsApi
from .telephony import TelephonyApi
from .telephony.jobs import JobsApi
from .tokens import Tokens
from .webhook import WebhookApi
from .workspace_locations import WorkspaceLocationApi
from .workspace_personalization import WorkspacePersonalizationApi
from .workspace_settings import WorkspaceSettingsApi
from .workspaces import WorkspacesApi
from .xapi import XApi

__all__ = ['WebexSimpleApi']

__version__ = '1.27.0'

log = logging.getLogger(__name__)


# noinspection PyShadowingNames
@dataclass(init=False, repr=False)
class WebexSimpleApi:
    """
    The main API object
    """

    #: Admin Audit Events API :class:`admin_audit.AdminAuditEventsApi`
    admin_audit: AdminAuditEventsApi
    #: Attachment actions API :class:`attachment_actions.AttachmentActionsApi`
    attachment_actions: AttachmentActionsApi
    #: Authorizations API :class:`authorizations.AuthorizationsApi`
    authorizations: AuthorizationsApi
    #: CDR API :class:`cdr.DetailedCDRApi`
    cdr: DetailedCDRApi
    #: converged recordings API :class:`converged_recordings.ConvergedRecordingsApi`
    converged_recordings: ConvergedRecordingsApi
    #: device configurations API :class:`device_configurations.DeviceConfigurationsApi`
    device_configurations: DeviceConfigurationsApi
    #: devices API :class:`devices.DevicesApi`
    devices: DevicesApi
    #: events API; :class:`events.EventsApi`
    events: EventsApi
    #: groups API :class:`groups.GroupsApi`
    groups: GroupsApi
    #: guests API :class:`guests.GuestManagementApi`
    guests: GuestManagementApi
    #: jobs API: :class:`telephony.jobs.JobsApi`
    jobs: JobsApi
    #: Licenses API :class:`licenses.LicensesApi`
    licenses: LicensesApi
    #: Location API :class:`locations.LocationsApi`
    locations: LocationsApi
    #: call settings for me  API :class:`me.MeSettingsApi`
    me: MeSettingsApi
    #: meetings API :class:`meetings.MeetingsApi`
    meetings: MeetingsApi
    #: membership API :class:`memberships.MembershipApi`
    membership: MembershipApi
    #: Messages API :class:`messages.MessagesApi`
    messages: MessagesApi
    #: org contacts API :class:`org_contacts.OrganizationContactsApi`
    org_contacts: OrganizationContactsApi
    #: organization settings API
    organizations: OrganizationApi
    #: Person settings API :class:`person_settings.PersonSettingsApi`
    person_settings: PersonSettingsApi
    #: People API :class:`people.PeopleApi`
    people: PeopleApi
    #: Reports API :class:`reports.ReportsApi`
    reports: ReportsApi
    #: Roles API :class:`roles.RolesApi`
    roles: RolesApi
    #: Rooms API :class:`rooms.RoomsApi`
    rooms: RoomsApi
    #: Room tabs API :class:`room_tabs.RoomTabsApi`
    room_tabs: RoomTabsApi
    #: Webex Status API :class:`status.StatusAPI`
    status: StatusAPI
    #: ScimV2 API: :class:`scimv2.ScimV2Api`
    scim: ScimV2Api
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
    #: Workspace personalization API :class:workspace_personalization.WorkspacePersonalizationApi`
    workspace_personalization: WorkspacePersonalizationApi
    #: Workspace setting API :class:`workspace_settings.WorkspaceSettingsApi`
    workspace_settings: WorkspaceSettingsApi
    #: XAPI API :class:`xapi.XApi`
    xapi: XApi
    #: :class:`rest.RestSession` used for all API requests
    session: RestSession
    #: whether the session used for all requests must be closed when :meth:`close` is called
    _must_close_session: bool

    def __init__(self, *, tokens: Union[str, Tokens] = None, concurrent_requests: int = 10, retry_429: bool = True,
                 session: RestSession = None, **kwargs):
        """

        :param tokens: token to be used by the API. Can be a :class:`tokens.Tokens` instance, a string or None. If
            None then an access token is expected in the WEBEX_ACCESS_TOKEN environment variable.
        :param concurrent_requests: number of concurrent requests when using multi-threading
        :type concurrent_requests: int
        :param retry_429: automatically retry for 429 throttling response
        :type retry_429: bool
        :param session: if given, this :class:`rest.RestSession` instance will be used for all requests instead of
            creating a new one
        :type session: RestSession
        :param kwargs: additional arguments to be passed to the constructor of the :attr:`session` object to be used
            for all requests
        """
        if isinstance(tokens, str):
            tokens = Tokens(access_token=tokens)
        elif tokens is None:
            tokens = os.getenv('WEBEX_ACCESS_TOKEN')
            if tokens is None:
                raise ValueError('if no access token is passed, then a valid access token has to be present in '
                                 'WEBEX_ACCESS_TOKEN environment variable')
            tokens = Tokens(access_token=tokens)

        if session is None:
            session = RestSession(tokens=tokens, concurrent_requests=concurrent_requests, retry_429=retry_429,
                                  **kwargs)
            self._must_close_session = True
        else:
            self._must_close_session = False
        self.session = session

        self.admin_audit = AdminAuditEventsApi(session=session)
        self.attachment_actions = AttachmentActionsApi(session=session)
        self.authorizations = AuthorizationsApi(session=session)
        self.cdr = DetailedCDRApi(session=session)
        self.converged_recordings = ConvergedRecordingsApi(session=session)
        self.device_configurations = DeviceConfigurationsApi(session=session)
        self.devices = DevicesApi(session=session)
        self.events = EventsApi(session=session)
        self.groups = GroupsApi(session=session)
        self.guests = GuestManagementApi(session=session)
        self.jobs = JobsApi(session=session)
        self.licenses = LicensesApi(session=session)
        self.locations = LocationsApi(session=session)
        self.me = MeSettingsApi(session=session)
        self.meetings = MeetingsApi(session=session)
        self.membership = MembershipApi(session=session)
        self.messages = MessagesApi(session=session)
        self.org_contacts = OrganizationContactsApi(session=session)
        self.organizations = OrganizationApi(session=session)
        self.person_settings = PersonSettingsApi(session=session)
        self.people = PeopleApi(session=session)
        self.reports = ReportsApi(session=session)
        self.roles = RolesApi(session=session)
        self.rooms = RoomsApi(session=session)
        self.room_tabs = RoomTabsApi(session=session)
        self.scim = ScimV2Api(session=session)
        self.status = StatusAPI(session=session)
        self.teams = TeamsApi(session=session)
        self.team_memberships = TeamMembershipsApi(session=session)
        self.telephony = TelephonyApi(session=session)
        self.webhook = WebhookApi(session=session)
        self.workspaces = WorkspacesApi(session=session)
        self.workspace_locations = WorkspaceLocationApi(session=session)
        self.workspace_personalization = WorkspacePersonalizationApi(session=session)
        self.workspace_settings = WorkspaceSettingsApi(session=session)
        self.xapi = XApi(session=session)

    @property
    def access_token(self) -> str:
        """
        access token used for all requests

        :return: access token
        :rtype: str
        """
        return self.session.access_token

    def close(self):
        if self._must_close_session:
            self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

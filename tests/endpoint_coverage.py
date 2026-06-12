"""
Helpers for live endpoint coverage tests.

This module keeps the broad endpoint-coverage machinery out of individual test
files. It treats ``script.endpoint_ref`` as the source of truth for the sync SDK
surface, defines a small live-smoke scenario registry, and classifies the rest
of the GET inventory as covered, skipped by tenant state, or explicitly
quarantined for later workflow-specific tests.
"""

from __future__ import annotations

import ast
import fnmatch
import re
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from functools import cache, cached_property
from pathlib import Path
from typing import Any, cast

from script.endpoint_ref import EndpointReference, endpoint_reference, markdown_table
from tests.base import LoggedRequest
from wxc_sdk import WebexSimpleApi
from wxc_sdk.rest import RestError, RestSession

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_TEST_ROOT = _PROJECT_ROOT / 'tests'
_PLACEHOLDER_RE = re.compile(r'\{([^{}]+)}')
_HTTP_METHODS = {'DELETE', 'GET', 'PATCH', 'POST', 'PUT'}


@dataclass(frozen=True)
class GetCoverageRule:
    """
    Explicit classification rule for GET endpoints that are not yet smoke-tested.

    :param pattern: ``fnmatch`` pattern matched against SDK method names.
    :param reason: Human-readable explanation shown when an endpoint is
        classified as quarantined.
    """

    pattern: str
    reason: str

    def matches(self, method: str) -> bool:
        """
        Return whether this quarantine rule applies to a method name.

        :param method: Fully-qualified SDK method name such as
            ``api.person_settings.forwarding.read``.
        :return: ``True`` when ``method`` matches this rule's pattern.
        """
        return fnmatch.fnmatchcase(method, self.pattern)


@dataclass(frozen=True)
class LiveGetScenario:
    """
    One executable live GET smoke scenario.

    :param method: Fully-qualified SDK method name covered by the scenario.
    :param call: Callable that performs the live SDK operation.
    :param description: Short reason this scenario exists.
    :param skip_statuses: HTTP statuses that indicate tenant/resource/scope
        absence rather than a harness failure.
    """

    method: str
    call: Callable[[LiveEndpointContext], Any]
    description: str
    skip_statuses: frozenset[int] = frozenset({400, 401, 403, 404})

    @property
    def id(self) -> str:
        """
        Return a compact pytest parameter ID for this scenario.

        :return: Method name without the leading ``api.`` prefix.
        """
        return self.method.removeprefix('api.')


class LiveEndpointContext:
    """
    Lazily discovers reusable live tenant resources for endpoint smoke tests.

    The cached properties centralize tenant-resource discovery so each scenario
    can stay focused on the SDK method it covers. Missing resources raise
    :class:`LiveEndpointSkip`, which lets the live suite skip cleanly for
    tenants that do not have optional artifacts such as webhooks or devices.
    """

    def __init__(self, api: WebexSimpleApi):
        """
        Store the live API object shared by one smoke scenario invocation.

        :param api: Configured sync SDK API instance backed by real test tokens.
        """
        self.api = api

    @cached_property
    def me(self):
        """
        Return the authenticated user.

        :return: Current user details from ``api.people.me``.
        """
        return self.api.people.me()

    @cached_property
    def org_id(self) -> str | None:
        """
        Return the organization ID associated with the current user.

        :return: Current user's organization ID, or ``None`` if absent.
        """
        return cast('str | None', self.me.org_id)

    @cached_property
    def first_device(self):
        """
        Return one device from the tenant.

        :return: First device returned by the Devices API.
        :raises LiveEndpointSkip: If the tenant has no devices.
        """
        return first_or_skip((d for d in self.api.devices.list() if d.device_id is not None), 'No devices available')

    @cached_property
    def first_group(self):
        """
        Return one group from the tenant.

        :return: First group returned by the Groups API.
        :raises LiveEndpointSkip: If the tenant has no groups.
        """
        return first_or_skip(self.api.groups.list(max=1), 'No groups available')

    @cached_property
    def first_license(self):
        """
        Return one license from the tenant.

        :return: First license returned by the Licenses API.
        :raises LiveEndpointSkip: If no licenses are visible.
        """
        return first_or_skip(self.api.licenses.list(), 'No licenses available')

    @cached_property
    def first_location(self):
        """
        Return one location from the tenant.

        :return: First location returned by the Locations API.
        :raises LiveEndpointSkip: If no locations are visible.
        """
        return first_or_skip(self.api.locations.list(max=1), 'No locations available')

    @cached_property
    def first_role(self):
        """
        Return one role from the tenant.

        :return: First role returned by the Roles API.
        :raises LiveEndpointSkip: If no roles are visible.
        """
        return first_or_skip(self.api.roles.list(), 'No roles available')

    @cached_property
    def first_room(self):
        """
        Return one room from the tenant.

        :return: First room returned by the Rooms API.
        :raises LiveEndpointSkip: If the token has no room access.
        """
        return first_or_skip(self.api.rooms.list(max=1), 'No rooms available')

    @cached_property
    def first_team(self):
        """
        Return one team from the tenant.

        :return: First team returned by the Teams API.
        :raises LiveEndpointSkip: If no teams are visible.
        """
        return first_or_skip(self.api.teams.list(), 'No teams available')

    @cached_property
    def first_webhook(self):
        """
        Return one webhook from the tenant.

        :return: First webhook returned by the Webhooks API.
        :raises LiveEndpointSkip: If no webhooks exist for the token.
        """
        return first_or_skip(self.api.webhook.list(), 'No webhooks available')

    @cached_property
    def first_workspace(self):
        """
        Return one workspace from the tenant.

        :return: First workspace returned by the Workspaces API.
        :raises LiveEndpointSkip: If no workspaces are visible.
        """
        return first_or_skip(self.api.workspaces.list(max=1), 'No workspaces available')


def first_or_none(values: Iterable[Any]) -> Any | None:
    """
    Return the first item from an iterable without materializing it.

    :param values: Any iterable or generator returned by an SDK list method.
    :return: First item, or ``None`` when the iterable is empty.
    """
    return next(iter(values), None)


def first_or_skip(values: Iterable[Any], reason: str) -> Any:
    """
    Return the first iterable item or raise a live-test skip sentinel.

    :param values: Iterable to inspect.
    :param reason: Skip reason to attach when the iterable is empty.
    :return: First item from ``values``.
    :raises LiveEndpointSkip: If no item exists.
    """
    value = first_or_none(values)
    if value is None:
        raise LiveEndpointSkip(reason)
    return value


class LiveEndpointSkip(Exception):
    """
    Indicates that tenant state does not contain the resource a live scenario needs.
    """


@cache
def endpoint_rows() -> tuple[EndpointReference, ...]:
    """
    Resolve the sync SDK endpoint inventory from the live object graph.

    :return: Sorted endpoint reference rows for ``WebexSimpleApi``.
    """
    # Source of truth: the same resolver that builds endpoint_ref.md.
    api = WebexSimpleApi(tokens='dummy')
    return tuple(sorted(endpoint_reference('api', api), key=lambda row: row.method))


@cache
def endpoint_by_method() -> dict[str, EndpointReference]:
    """
    Index endpoint rows by fully-qualified SDK method name.

    :return: Mapping from names such as ``api.people.me`` to reference rows.
    """
    return {row.method: row for row in endpoint_rows()}


def current_endpoint_markdown() -> str:
    """
    Render the current in-memory endpoint inventory as Markdown.

    :return: Markdown content expected in ``endpoint_ref.md``.
    """
    return markdown_table(list(endpoint_rows()))


def endpoint_template_regex(endpoint: str) -> re.Pattern[str]:
    """
    Convert an endpoint template into a regex for logged request URLs.

    ``endpoint_ref`` templates use placeholders such as ``{person_id}``.
    Request logs contain concrete IDs, optional query strings, and sometimes
    absolute non-Webex URLs, so this helper bridges those representations.

    :param endpoint: Endpoint template from :class:`EndpointReference`.
    :return: Compiled regex matching a concrete request URL.
    """
    if endpoint.startswith('http://') or endpoint.startswith('https://'):
        url_template = endpoint
    elif endpoint.startswith('{') and endpoint.endswith('}'):
        url_template = endpoint
    else:
        url_template = f'{RestSession.BASE}{endpoint}'

    # Replace every endpoint placeholder with a path-segment matcher while
    # preserving literal text and known alternatives like {cdr_stream|cdr_feed}.
    parts: list[str] = []
    pos = 0
    for match in _PLACEHOLDER_RE.finditer(url_template):
        parts.append(re.escape(url_template[pos : match.start()]))
        placeholder = match.group(1)
        choices = placeholder.split('|')
        if len(choices) > 1 and all(re.fullmatch(r'[-\w]+', choice) for choice in choices):
            parts.append('(?:' + '|'.join(re.escape(choice) for choice in choices) + ')')
        else:
            parts.append(r'[^/?#]+')
        pos = match.end()
    parts.append(re.escape(url_template[pos:]))
    return re.compile('^' + ''.join(parts) + r'(?:\?.*)?$')


def matching_requests(row: EndpointReference, records: Sequence[Any]) -> list[LoggedRequest]:
    """
    Find logged REST requests matching an endpoint reference row.

    :param row: Endpoint metadata to match.
    :param records: Logging records captured during a test.
    :return: Parsed request records matching the row's HTTP method and URL.
    """
    # The existing TestCaseWithLog parser is reused so live smoke tests check
    # the real SDK logging format instead of inventing another request tap.
    url_re = endpoint_template_regex(row.endpoint)
    return list(LoggedRequest.from_records(list(records), method=row.http_method, url_filter=url_re))


def assert_endpoint_requested(method: str, records: Sequence[Any]) -> None:
    """
    Assert that a live scenario issued the request for its declared SDK method.

    :param method: Fully-qualified SDK method name covered by the scenario.
    :param records: Request log records emitted while the scenario ran.
    """
    row = endpoint_by_method()[method]
    requests = matching_requests(row, records)
    assert requests, f'{method} did not issue {row.http_method} {row.endpoint}'


def scenario(method: str, description: str) -> Callable[[Callable[[LiveEndpointContext], Any]], LiveGetScenario]:
    """
    Decorate a function as a registered live GET smoke scenario.

    :param method: Fully-qualified SDK method name covered by the decorated
        function.
    :param description: Short scenario description for maintainers.
    :return: Decorator converting a function into :class:`LiveGetScenario`.
    """

    def decorator(func: Callable[[LiveEndpointContext], Any]) -> LiveGetScenario:
        """
        Build immutable scenario metadata around the scenario callable.

        :param func: Function that performs one live SDK request path.
        :return: Scenario object added to ``LIVE_GET_SCENARIOS``.
        """
        return LiveGetScenario(method=method, call=func, description=description)

    return decorator


@scenario('api.admin_audit.list_event_categories', 'Read stable admin-audit category metadata')
def _admin_audit_categories(ctx: LiveEndpointContext) -> None:
    """
    Cover listing admin-audit event categories.

    :param ctx: Live endpoint test context.
    """
    first_or_none(ctx.api.admin_audit.list_event_categories())


@scenario('api.admin_audit.list_events', 'Read a recent page of admin-audit events')
def _admin_audit_events(ctx: LiveEndpointContext) -> None:
    """
    Cover listing recent admin-audit events for the current organization.

    :param ctx: Live endpoint test context.
    :raises LiveEndpointSkip: If the current user has no organization ID.
    """
    if not ctx.org_id:
        raise LiveEndpointSkip('Current user has no org_id')
    to_ = datetime.now(UTC)
    from_ = to_ - timedelta(days=7)
    first_or_none(ctx.api.admin_audit.list_events(org_id=ctx.org_id, from_=from_, to_=to_))


@scenario('api.authorizations.get_token_expiration_status', 'Read token expiration metadata for current token')
def _authorization_token_expiration(ctx: LiveEndpointContext) -> None:
    """
    Cover reading token-expiration status for the active token.

    :param ctx: Live endpoint test context.
    """
    ctx.api.authorizations.get_token_expiration_status()


@scenario('api.authorizations.list', 'List authorizations for the current user')
def _authorizations_list(ctx: LiveEndpointContext) -> None:
    """
    Cover listing authorizations for the authenticated user.

    :param ctx: Live endpoint test context.
    """
    ctx.api.authorizations.list(person_id=ctx.me.person_id)


@scenario('api.devices.list', 'List a single device page')
def _devices_list(ctx: LiveEndpointContext) -> None:
    """
    Cover listing devices with a small page size.

    :param ctx: Live endpoint test context.
    """
    first_or_none(ctx.api.devices.list(max=1))


@scenario('api.devices.details', 'Read details for a discovered device')
def _devices_details(ctx: LiveEndpointContext) -> None:
    """
    Cover reading device details for a discovered tenant device.

    :param ctx: Live endpoint test context.
    """
    ctx.api.devices.details(device_id=ctx.first_device.device_id)


@scenario('api.devices.settings_jobs.list', 'List device settings jobs')
def _device_settings_jobs_list(ctx: LiveEndpointContext) -> None:
    """
    Cover listing device settings jobs.

    :param ctx: Live endpoint test context.
    """
    first_or_none(ctx.api.devices.settings_jobs.list())


@scenario('api.groups.list', 'List a single group page')
def _groups_list(ctx: LiveEndpointContext) -> None:
    """
    Cover listing identity groups with a small page size.

    :param ctx: Live endpoint test context.
    """
    first_or_none(ctx.api.groups.list(max=1))


@scenario('api.groups.details', 'Read details for a discovered group')
def _groups_details(ctx: LiveEndpointContext) -> None:
    """
    Cover reading group details for a discovered group.

    :param ctx: Live endpoint test context.
    """
    ctx.api.groups.details(group_id=ctx.first_group.group_id)


@scenario('api.groups.members', 'List members for a discovered group')
def _groups_members(ctx: LiveEndpointContext) -> None:
    """
    Cover listing members for a discovered group.

    :param ctx: Live endpoint test context.
    """
    first_or_none(ctx.api.groups.members(group_id=ctx.first_group.group_id, count=1))


@scenario('api.licenses.list', 'List licenses')
def _licenses_list(ctx: LiveEndpointContext) -> None:
    """
    Cover listing organization licenses.

    :param ctx: Live endpoint test context.
    """
    ctx.api.licenses.list()


@scenario('api.licenses.details', 'Read details for a discovered license')
def _licenses_details(ctx: LiveEndpointContext) -> None:
    """
    Cover reading details for a discovered license.

    :param ctx: Live endpoint test context.
    """
    ctx.api.licenses.details(license_id=ctx.first_license.license_id)


@scenario('api.licenses.assigned_users', 'List assigned users for a discovered license')
def _licenses_assigned_users(ctx: LiveEndpointContext) -> None:
    """
    Cover listing users assigned to a discovered license.

    :param ctx: Live endpoint test context.
    """
    first_or_none(ctx.api.licenses.assigned_users(license_id=ctx.first_license.license_id, max=1))


@scenario('api.locations.list', 'List a single location page')
def _locations_list(ctx: LiveEndpointContext) -> None:
    """
    Cover listing locations with a small page size.

    :param ctx: Live endpoint test context.
    """
    first_or_none(ctx.api.locations.list(max=1))


@scenario('api.locations.details', 'Read details for a discovered location')
def _locations_details(ctx: LiveEndpointContext) -> None:
    """
    Cover reading details for a discovered location.

    :param ctx: Live endpoint test context.
    """
    ctx.api.locations.details(location_id=ctx.first_location.location_id)


@scenario('api.locations.list_floors', 'List floors for a discovered location')
def _locations_list_floors(ctx: LiveEndpointContext) -> None:
    """
    Cover listing floors for a discovered location.

    :param ctx: Live endpoint test context.
    """
    ctx.api.locations.list_floors(location_id=ctx.first_location.location_id)


@scenario('api.people.me', 'Read current user details')
def _people_me(ctx: LiveEndpointContext) -> None:
    """
    Cover reading the authenticated user's People details.

    :param ctx: Live endpoint test context.
    """
    ctx.api.people.me()


@scenario('api.people.details', 'Read current user by person ID')
def _people_details(ctx: LiveEndpointContext) -> None:
    """
    Cover reading People details by person ID.

    :param ctx: Live endpoint test context.
    """
    ctx.api.people.details(person_id=ctx.me.person_id)


@scenario('api.people.list', 'List people by current user email')
def _people_list(ctx: LiveEndpointContext) -> None:
    """
    Cover listing people using the authenticated user's email.

    :param ctx: Live endpoint test context.
    """
    first_or_none(ctx.api.people.list(email=ctx.me.emails[0]))


@scenario('api.reports.list_templates', 'List available report templates')
def _reports_list_templates(ctx: LiveEndpointContext) -> None:
    """
    Cover listing report templates.

    :param ctx: Live endpoint test context.
    """
    ctx.api.reports.list_templates()


@scenario('api.roles.list', 'List roles')
def _roles_list(ctx: LiveEndpointContext) -> None:
    """
    Cover listing roles.

    :param ctx: Live endpoint test context.
    """
    ctx.api.roles.list()


@scenario('api.roles.details', 'Read details for a discovered role')
def _roles_details(ctx: LiveEndpointContext) -> None:
    """
    Cover reading details for a discovered role.

    :param ctx: Live endpoint test context.
    """
    ctx.api.roles.details(role_id=ctx.first_role.id)


@scenario('api.rooms.list', 'List a single room page')
def _rooms_list(ctx: LiveEndpointContext) -> None:
    """
    Cover listing rooms with a small page size.

    :param ctx: Live endpoint test context.
    """
    first_or_none(ctx.api.rooms.list(max=1))


@scenario('api.rooms.details', 'Read details for a discovered room')
def _rooms_details(ctx: LiveEndpointContext) -> None:
    """
    Cover reading details for a discovered room.

    :param ctx: Live endpoint test context.
    """
    ctx.api.rooms.details(room_id=ctx.first_room.id)


@scenario('api.status.summary', 'Read Webex status summary')
def _status_summary(ctx: LiveEndpointContext) -> None:
    """
    Cover reading the Webex status summary page.

    :param ctx: Live endpoint test context.
    """
    ctx.api.status.summary()


@scenario('api.status.components', 'Read Webex status components')
def _status_components(ctx: LiveEndpointContext) -> None:
    """
    Cover reading Webex status components.

    :param ctx: Live endpoint test context.
    """
    ctx.api.status.components()


@scenario('api.status.unresolved_incidents', 'Read unresolved Webex status incidents')
def _status_unresolved_incidents(ctx: LiveEndpointContext) -> None:
    """
    Cover reading unresolved Webex status incidents.

    :param ctx: Live endpoint test context.
    """
    ctx.api.status.unresolved_incidents()


@scenario('api.status.all_incidents', 'Read recent Webex status incidents')
def _status_all_incidents(ctx: LiveEndpointContext) -> None:
    """
    Cover reading recent Webex status incidents.

    :param ctx: Live endpoint test context.
    """
    ctx.api.status.all_incidents()


@scenario('api.status.upcoming_scheduled_maintenances', 'Read upcoming Webex status maintenances')
def _status_upcoming_scheduled_maintenances(ctx: LiveEndpointContext) -> None:
    """
    Cover reading upcoming Webex status maintenances.

    :param ctx: Live endpoint test context.
    """
    ctx.api.status.upcoming_scheduled_maintenances()


@scenario('api.status.active_scheduled_maintenances', 'Read active Webex status maintenances')
def _status_active_scheduled_maintenances(ctx: LiveEndpointContext) -> None:
    """
    Cover reading active Webex status maintenances.

    :param ctx: Live endpoint test context.
    """
    ctx.api.status.active_scheduled_maintenances()


@scenario('api.status.all_scheduled_maintenances', 'Read all Webex status maintenances')
def _status_all_scheduled_maintenances(ctx: LiveEndpointContext) -> None:
    """
    Cover reading all Webex status maintenances.

    :param ctx: Live endpoint test context.
    """
    ctx.api.status.all_scheduled_maintenances()


@scenario('api.teams.list', 'List teams')
def _teams_list(ctx: LiveEndpointContext) -> None:
    """
    Cover listing teams.

    :param ctx: Live endpoint test context.
    """
    first_or_none(ctx.api.teams.list())


@scenario('api.teams.details', 'Read details for a discovered team')
def _teams_details(ctx: LiveEndpointContext) -> None:
    """
    Cover reading details for a discovered team.

    :param ctx: Live endpoint test context.
    """
    ctx.api.teams.details(team_id=ctx.first_team.id)


@scenario('api.webhook.list', 'List webhooks')
def _webhook_list(ctx: LiveEndpointContext) -> None:
    """
    Cover listing webhooks.

    :param ctx: Live endpoint test context.
    """
    first_or_none(ctx.api.webhook.list())


@scenario('api.webhook.details', 'Read details for a discovered webhook')
def _webhook_details(ctx: LiveEndpointContext) -> None:
    """
    Cover reading details for a discovered webhook.

    :param ctx: Live endpoint test context.
    """
    ctx.api.webhook.details(webhook_id=ctx.first_webhook.id)


@scenario('api.workspaces.list', 'List a single workspace page')
def _workspaces_list(ctx: LiveEndpointContext) -> None:
    """
    Cover listing workspaces with a small page size.

    :param ctx: Live endpoint test context.
    """
    first_or_none(ctx.api.workspaces.list(max=1))


@scenario('api.workspaces.details', 'Read details for a discovered workspace')
def _workspaces_details(ctx: LiveEndpointContext) -> None:
    """
    Cover reading details for a discovered workspace.

    :param ctx: Live endpoint test context.
    """
    ctx.api.workspaces.details(workspace_id=ctx.first_workspace.workspace_id)


@scenario('api.workspaces.capabilities', 'Read capabilities for a discovered workspace')
def _workspaces_capabilities(ctx: LiveEndpointContext) -> None:
    """
    Cover reading capabilities for a discovered workspace.

    :param ctx: Live endpoint test context.
    """
    ctx.api.workspaces.capabilities(workspace_id=ctx.first_workspace.workspace_id)


# Live scenario registry: every entry executes a real SDK GET path and asserts
# that the expected HTTP request appeared in the captured REST logs.
LIVE_GET_SCENARIOS: tuple[LiveGetScenario, ...] = (
    _admin_audit_categories,
    _admin_audit_events,
    _authorization_token_expiration,
    _authorizations_list,
    _devices_list,
    _devices_details,
    _device_settings_jobs_list,
    _groups_list,
    _groups_details,
    _groups_members,
    _licenses_list,
    _licenses_details,
    _licenses_assigned_users,
    _locations_list,
    _locations_details,
    _locations_list_floors,
    _people_me,
    _people_details,
    _people_list,
    _reports_list_templates,
    _roles_list,
    _roles_details,
    _rooms_list,
    _rooms_details,
    _status_summary,
    _status_components,
    _status_unresolved_incidents,
    _status_all_incidents,
    _status_upcoming_scheduled_maintenances,
    _status_active_scheduled_maintenances,
    _status_all_scheduled_maintenances,
    _teams_list,
    _teams_details,
    _webhook_list,
    _webhook_details,
    _workspaces_list,
    _workspaces_details,
    _workspaces_capabilities,
)

# Quarantine registry: GET endpoints that are not covered by a generic smoke
# scenario must carry a concrete reason so inventory drift is visible.
GET_COVERAGE_QUARANTINE_RULES: tuple[GetCoverageRule, ...] = (
    GetCoverageRule('api.attachment_actions.*', 'Requires a real card attachment action ID from messaging activity.'),
    GetCoverageRule('api.cdr.*', 'Requires recent calling CDR data and date windows.'),
    GetCoverageRule('api.converged_recordings.*', 'Requires existing recordings and recording lifecycle state.'),
    GetCoverageRule(
        'api.device_configurations.*',
        'Requires target devices with configurable device configuration data.',
    ),
    GetCoverageRule('api.devices.settings_jobs.errors', 'Requires a live device settings job ID.'),
    GetCoverageRule('api.devices.settings_jobs.status', 'Requires a live device settings job ID.'),
    GetCoverageRule(
        'api.events.*',
        'Requires compliance scope and event history; covered by dedicated tests where enabled.',
    ),
    GetCoverageRule('api.guests.*', 'Requires service-app guest issuer token rather than the default admin token.'),
    GetCoverageRule('api.jobs.*', 'Requires live job IDs created by mutating job workflows.'),
    GetCoverageRule(
        'api.me.*',
        'Current-user calling feature endpoints depend on user entitlements and settings state.',
    ),
    GetCoverageRule('api.meetings.*', 'Requires meeting/site/invitee artifacts and host-specific state.'),
    GetCoverageRule('api.membership.*', 'Requires room membership resources.'),
    GetCoverageRule('api.messages.*', 'Requires room/message resources and message content state.'),
    GetCoverageRule('api.locations.floor_details', 'Requires a location with a floor artifact.'),
    GetCoverageRule('api.org_contacts.*', 'Requires organization contact data.'),
    GetCoverageRule('api.organizations.*', 'Requires managed organization relationships or org feature state.'),
    GetCoverageRule(
        'api.person_settings.*',
        'Requires disposable calling users and feature-specific setup/restore flows.',
    ),
    GetCoverageRule('api.reports.details', 'Requires an existing generated report ID.'),
    GetCoverageRule('api.reports.download', 'Requires a generated report download URL.'),
    GetCoverageRule('api.reports.list', 'Requires report history and can be region/template dependent.'),
    GetCoverageRule('api.room_tabs.*', 'Requires room tab resources.'),
    GetCoverageRule('api.scim.*', 'Requires SCIM-specific users/groups and filter scenarios.'),
    GetCoverageRule('api.status.status', 'Resolver currently records /status instead of the status.webex.com URL.'),
    GetCoverageRule('api.team_memberships.*', 'Requires team membership resources.'),
    GetCoverageRule('api.telephony.*', 'Requires calling tenant resources; covered by feature-specific live tests.'),
    GetCoverageRule('api.webhook.details', 'Requires at least one webhook; live smoke skips when none exist.'),
    GetCoverageRule(
        'api.workspace_locations.*',
        'Deprecated workspace-locations API; retained for legacy coverage only.',
    ),
    GetCoverageRule('api.workspace_personalization.*', 'Requires workspace personalization task state.'),
    GetCoverageRule('api.workspace_settings.*', 'Requires disposable workspace calling feature setup/restore flows.'),
    GetCoverageRule('api.xapi.*', 'Requires eligible device XAPI access.'),
)


def quarantine_reason(method: str) -> str | None:
    """
    Return the explicit quarantine reason for a method, if any.

    :param method: Fully-qualified SDK method name.
    :return: Quarantine reason or ``None`` when no rule matches.
    """
    for rule in GET_COVERAGE_QUARANTINE_RULES:
        if rule.matches(method):
            return rule.reason
    return None


def live_scenario_methods() -> set[str]:
    """
    Return the set of SDK methods covered by live smoke scenarios.

    :return: Method names declared in ``LIVE_GET_SCENARIOS``.
    """
    return {scenario.method for scenario in LIVE_GET_SCENARIOS}


def discovered_test_method_references(*, include_async: bool = False) -> set[str]:
    """
    Discover existing direct SDK method calls in test modules.

    This lightweight AST scan lets the inventory test count existing dedicated
    tests as coverage without requiring every old test to opt in to this helper.

    :param include_async: Whether ``self.async_api`` calls should count as
        sync-method coverage.
    :return: Set of fully-qualified SDK method names referenced by tests.
    """
    methods: set[str] = set()
    for path in _TEST_ROOT.glob('test*.py'):
        if path.name in {'test_endpoint_inventory.py', 'test_live_endpoint_coverage.py'}:
            continue
        try:
            tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        except SyntaxError:
            continue

        class Visitor(ast.NodeVisitor):
            """
            AST visitor that records direct SDK method invocations.
            """

            def visit_Call(self, node: ast.Call) -> None:
                """
                Record an API call expression when it resolves to the SDK tree.

                :param node: AST call node being inspected.
                """
                chain = _api_chain(node.func, include_async=include_async)
                if chain and len(chain.split('.')) >= 3:
                    methods.add(chain)
                self.generic_visit(node)

        Visitor().visit(tree)
    return methods


def _api_chain(node: ast.AST, *, include_async: bool) -> str | None:
    """
    Convert an AST attribute chain rooted at ``api`` or ``self.api`` to text.

    :param node: AST expression to inspect.
    :param include_async: Whether ``self.async_api`` should normalize to
        ``api``.
    :return: Dotted method path, or ``None`` for unrelated expressions.
    """
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value

    if isinstance(current, ast.Name) and current.id == 'api':
        parts.append('api')
    elif isinstance(current, ast.Attribute) and isinstance(current.value, ast.Name) and current.value.id == 'self':
        if current.attr == 'api' or (include_async and current.attr == 'async_api'):
            parts.append('api')
    else:
        return None

    return '.'.join(reversed(parts))


def coverage_status() -> dict[str, str]:
    """
    Classify every endpoint row as covered, deferred, quarantined, or missing.

    :return: Mapping from SDK method name to coverage classification.
    """
    covered = discovered_test_method_references() | live_scenario_methods()
    status: dict[str, str] = {}
    for row in endpoint_rows():
        if row.method in covered:
            status[row.method] = 'covered'
        elif row.http_method != 'GET':
            status[row.method] = 'deferred: mutating endpoint requires disposable-resource CRUD coverage'
        elif reason := quarantine_reason(row.method):
            status[row.method] = f'quarantined: {reason}'
        else:
            status[row.method] = 'missing'
    return status


def missing_get_methods() -> list[str]:
    """
    Return GET endpoints that are neither covered nor explicitly quarantined.

    :return: Sorted list of missing SDK method names.
    """
    status = coverage_status()
    return sorted(method for method, value in status.items() if value == 'missing')


def invalid_endpoint_rows() -> list[EndpointReference]:
    """
    Return endpoint rows with invalid HTTP method metadata.

    :return: Rows whose HTTP method or endpoint is not usable by the tests.
    """
    return [row for row in endpoint_rows() if row.http_method not in _HTTP_METHODS or not row.endpoint]


def unknown_live_scenarios() -> list[str]:
    """
    Return live scenarios that name SDK methods absent from the endpoint inventory.

    :return: Sorted list of unknown method names.
    """
    known = endpoint_by_method()
    return sorted(method for method in live_scenario_methods() if method not in known)


def scenario_by_id() -> dict[str, LiveGetScenario]:
    """
    Index live scenarios by their pytest-friendly ID.

    :return: Mapping from scenario ID to scenario metadata.
    """
    return {scenario.id: scenario for scenario in LIVE_GET_SCENARIOS}


def explain_missing(methods: Sequence[str]) -> str:
    """
    Render method names as an indented assertion message block.

    :param methods: Method names to explain.
    :return: Multi-line bullet-style text, or an empty string.
    """
    if not methods:
        return ''
    return '\n'.join(f'  - {method}' for method in methods)


def skip_reason_for_rest_error(error: RestError, scenario: LiveGetScenario) -> str | None:
    """
    Convert allowed live REST failures into pytest skip reasons.

    :param error: REST exception raised by a live SDK call.
    :param scenario: Scenario that was executing.
    :return: Skip reason for expected tenant/scope absence, otherwise ``None``.
    """
    status = error.response.status_code
    if status in scenario.skip_statuses:
        return f'{scenario.method} unavailable in this tenant or token scope: HTTP {status} {error}'
    return None

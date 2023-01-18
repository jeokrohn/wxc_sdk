# auto-generated. DO NOT EDIT
import csv
import json
import logging
import mimetypes
import os
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from dateutil import tz
from enum import Enum
from io import BufferedReader
from typing import Union, Dict, Optional, Literal, List

from aiohttp import FormData
from pydantic import parse_obj_as

from wxc_sdk.all_types import *
from wxc_sdk.as_rest import AsRestSession
from wxc_sdk.base import to_camel, StrOrDict, dt_iso_str
from wxc_sdk.base import SafeEnum as Enum

log = logging.getLogger(__name__)


class MultipartEncoder(FormData):
    """
    Compatibility class for requests toolbelt MultipartEncoder
    """

    def __init__(self, body):
        super().__init__()
        for name, value in body.items():
            if isinstance(value, str):
                self.add_field(name, value)
            elif isinstance(value, tuple):
                self.add_field(name, value=value[1], content_type=value[2], filename=value[0])
            else:
                raise NotImplementedError

    @property
    def content_type(self) -> str:
        return self._writer.content_type


# there seems to be a problem with getting too many users with calling data at the same time
# this is the maximum number the SDK enforces
MAX_USERS_WITH_CALLING_DATA = 10


__all__ = ['AsAccessCodesApi', 'AsAgentCallerIdApi', 'AsAnnouncementApi', 'AsApiChild', 'AsAppServicesApi',
           'AsAttachmentActionsApi', 'AsAuthCodesApi', 'AsAutoAttendantApi', 'AsBargeApi', 'AsCQPolicyApi',
           'AsCallInterceptApi', 'AsCallParkApi', 'AsCallPickupApi', 'AsCallQueueApi', 'AsCallRecordingApi',
           'AsCallWaitingApi', 'AsCallerIdApi', 'AsCallingBehaviorApi', 'AsCallparkExtensionApi', 'AsCallsApi',
           'AsDetailedCDRApi', 'AsDeviceSettingsJobsApi', 'AsDevicesApi', 'AsDialPlanApi', 'AsDndApi', 'AsEventsApi',
           'AsExecAssistantApi', 'AsForwardingApi', 'AsGroupsApi', 'AsHotelingApi', 'AsHuntGroupApi',
           'AsIncomingPermissionsApi', 'AsInternalDialingApi', 'AsJobsApi', 'AsLicensesApi', 'AsLocationInterceptApi',
           'AsLocationMoHApi', 'AsLocationNumbersApi', 'AsLocationVoicemailSettingsApi', 'AsLocationsApi',
           'AsManageNumbersJobsApi', 'AsMembershipApi', 'AsMessagesApi', 'AsMonitoringApi', 'AsNumbersApi',
           'AsOrganisationVoicemailSettingsAPI', 'AsOrganizationApi', 'AsOutgoingPermissionsApi', 'AsPagingApi',
           'AsPeopleApi', 'AsPersonForwardingApi', 'AsPersonSettingsApi', 'AsPersonSettingsApiChild',
           'AsPremisePstnApi', 'AsPrivacyApi', 'AsPrivateNetworkConnectApi', 'AsPushToTalkApi', 'AsReceptionistApi',
           'AsReportsApi', 'AsRestSession', 'AsRoomTabsApi', 'AsRoomsApi', 'AsRouteGroupApi', 'AsRouteListApi',
           'AsScheduleApi', 'AsTeamMembershipsApi', 'AsTeamsApi', 'AsTelephonyApi', 'AsTelephonyDevicesApi',
           'AsTelephonyLocationApi', 'AsTransferNumbersApi', 'AsTrunkApi', 'AsVoiceMessagingApi', 'AsVoicePortalApi',
           'AsVoicemailApi', 'AsVoicemailGroupsApi', 'AsVoicemailRulesApi', 'AsWebexSimpleApi', 'AsWebhookApi',
           'AsWorkspaceLocationApi', 'AsWorkspaceLocationFloorApi', 'AsWorkspaceNumbersApi', 'AsWorkspaceSettingsApi',
           'AsWorkspacesApi']


@dataclass(init=False)
class AsApiChild:
    """
    Base class for child APIs of :class:`WebexSimpleApi`
    """
    session: AsRestSession

    def __init__(self, *, session: AsRestSession, base: str = None):
        #: REST session
        self.session = session
        if base:
            self.base = base

    # noinspection PyMethodOverriding

    def __init_subclass__(cls, base: str):
        """
        Subclass registration hook. Each APIChild has a specific endpoint prefix which we gather at subclass
        registration time-

        :param base: APIChild specific URL path
        """
        super().__init_subclass__()
        # save endpoint prefix
        cls.base = base

    def ep(self, path: str = None):
        """
        endpoint URL for given path

        :param path: path after APIChild subclass specific endpoint URI prefix
        :type path: str
        :return: endpoint URL
        :rtype: str
        """
        path = path and f'/{path}' or ''
        return self.session.ep(f'{self.base}{path}')

    async def get(self, *args, **kwargs) -> StrOrDict:
        """
        GET request

        :param args:
        :param kwargs:
        :return:
        """
        return await self.session.rest_get(*args, **kwargs)

    async def post(self, *args, **kwargs) -> StrOrDict:
        """
        POST request

        :param args:
        :param kwargs:
        :return:
        """
        return await self.session.rest_post(*args, **kwargs)

    async def put(self, *args, **kwargs) -> StrOrDict:
        """
        PUT request

        :param args:
        :param kwargs:
        :return:
        """
        return await self.session.rest_put(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> None:
        """
        DELETE request

        :param args:
        :param kwargs:
        """
        await self.session.rest_delete(*args, **kwargs)

    async def patch(self, *args, **kwargs) -> StrOrDict:
        """
        PATCH request

        :param args:
        :param kwargs:
        """
        return await self.session.rest_patch(*args, **kwargs)


class AsAttachmentActionsApi(AsApiChild, base='attachment/actions'):
    """
    Users create attachment actions by interacting with message attachments such as clicking on a submit button in a
    card.
    """

    async def details(self, action_id: str) -> AttachmentAction:
        """
        Shows details for a attachment action, by ID.
        Specify the attachment action ID in the id URI parameter.

        :param action_id: A unique identifier for the attachment action.
        :type action_id: str
        """
        url = self.ep(f'{action_id}')
        data = await super().get(url=url)
        return AttachmentAction.parse_obj(data)


class AsDetailedCDRApi(AsApiChild, base='devices'):
    """
    To retrieve Detailed Call History information, you must use a token with the spark-admin:calling_cdr_read scope.
    The authenticating user must be a read-only-admin or full-admin of the organization and have the administrator
    role "Webex Calling Detailed Call History API access" enabled.

    Detailed Call History information is available 5 minutes after a call has ended and may be retrieved for up to 48
    hours. For example, if a call ends at 9:46 am, the record for that call can be collected using the API from 9:51
    am, and is available until 9:46 am two days later.

    This API is rate-limited to one call every 5 minutes for a given organization ID.
    """

    def get_cdr_history_gen(self, start_time: datetime = None, end_time: datetime = None, locations: list[str] = None,
                        **params) -> AsyncGenerator[CDR, None, None]:
        """
        Provides Webex Calling Detailed Call History data for your organization.

        Results can be filtered with the startTime, endTime and locations request parameters. The startTime and endTime
        parameters specify the start and end of the time period for the Detailed Call History reports you wish to
        collect.
        The API will return all reports that were created between startTime and endTime.

        :param start_time: Time of the first report you wish to collect. (report time is the time the call finished).
            Note: The specified time must be between 5 minutes ago and 48 hours ago.
        :param end_time: Time of the last report you wish to collect. Note: The specified time should be earlier than
            startTime and no earlier than 48 hours ago
        :param locations: Names of the location (as shown in Control Hub). Up to 10 comma-separated locations can be
            provided. Allows you to query reports by location.
        :param params: additional arguments
        :return:
        """
        url = 'https://analytics.webexapis.com/v1/cdr_feed'
        if locations:
            params['locations'] = ','.join(locations)
        if not start_time:
            start_time = datetime.now(tz=tz.tzutc()) - timedelta(hours=47, minutes=58)
        if not end_time:
            end_time = datetime.now(tz=tz.tzutc()) - timedelta(minutes=5, seconds=30)

        params['startTime'] = dt_iso_str(start_time)
        params['endTime'] = dt_iso_str(end_time)
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CDR, params=params, item_key='items')

    async def get_cdr_history(self, start_time: datetime = None, end_time: datetime = None, locations: list[str] = None,
                        **params) -> List[CDR]:
        """
        Provides Webex Calling Detailed Call History data for your organization.

        Results can be filtered with the startTime, endTime and locations request parameters. The startTime and endTime
        parameters specify the start and end of the time period for the Detailed Call History reports you wish to
        collect.
        The API will return all reports that were created between startTime and endTime.

        :param start_time: Time of the first report you wish to collect. (report time is the time the call finished).
            Note: The specified time must be between 5 minutes ago and 48 hours ago.
        :param end_time: Time of the last report you wish to collect. Note: The specified time should be earlier than
            startTime and no earlier than 48 hours ago
        :param locations: Names of the location (as shown in Control Hub). Up to 10 comma-separated locations can be
            provided. Allows you to query reports by location.
        :param params: additional arguments
        :return:
        """
        url = 'https://analytics.webexapis.com/v1/cdr_feed'
        if locations:
            params['locations'] = ','.join(locations)
        if not start_time:
            start_time = datetime.now(tz=tz.tzutc()) - timedelta(hours=47, minutes=58)
        if not end_time:
            end_time = datetime.now(tz=tz.tzutc()) - timedelta(minutes=5, seconds=30)

        params['startTime'] = dt_iso_str(start_time)
        params['endTime'] = dt_iso_str(end_time)
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=CDR, params=params, item_key='items')]


class AsDeviceSettingsJobsApi(AsApiChild, base='telephony/config/jobs/devices/callDeviceSettings'):
    """
    API for jobs to update device settings at the location and organization level

    """

    async def change(self, location_id: Optional[str], customization: DeviceCustomization,
               org_id: str = None) -> StartJobResponse:
        """
        Change device settings across organization or locations jobs.

        Performs bulk and asynchronous processing for all types of device settings initiated by organization and system
        admins in a stateful persistent manner. This job will modify the requested device settings across all the
        devices. Whenever a location ID is specified in the request, it will modify the requested device settings only
        for the devices that are part of the provided location within an organization.

        Returns a unique job ID which can then be utilized further to retrieve status and errors for the same.

        Only one job per customer can be running at any given time within the same organization. An attempt to run
        multiple jobs at the same time will result in a 409 error response.

        Running a job requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location within an organization where changes of device settings will be applied to all the
            devices within it.
        :type location_id: str
        :param customization: customization. Atttribute custom_enabled Indicates if all the devices within this
            location will be customized with new requested customizations(if set to true) or will be overridden with
            the one at organization level (if set to false or any other value). This field has no effect when the job
            is being triggered at organization level.
        :type customization: DeviceCustomization
        :param org_id: Apply change device settings for all the devices under this organization.
        :type org_id: str
        :return: information about the created job
        :rtype: StartJobResponse
        """
        url = self.ep()
        params = org_id and {'prgId': org_id} or None
        body = {}
        if location_id:
            body['locationId'] = location_id
            body['locationCustomizationsEnabled'] = customization.custom_enabled
        if customization.custom_enabled or not location_id:
            body['customizations'] = json.loads(customization.customizations.json())
        data = await self.post(url=url, params=params, json=body)
        return StartJobResponse.parse_obj(data)

    def list_gen(self, org_id: str = None, **params) -> AsyncGenerator[StartJobResponse, None, None]:
        """
        List change device settings jobs.

        Lists all the jobs for jobType calldevicesettings for the given organization in order of most recent one to
        oldest one irrespective of its status.

        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Retrieve list of 'calldevicesettings' jobs for this organization.
        :type org_id: str
        :param params: optional parameters
        :return: Generator of :class:`StartJobResponse` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=StartJobResponse, params=params)

    async def list(self, org_id: str = None, **params) -> List[StartJobResponse]:
        """
        List change device settings jobs.

        Lists all the jobs for jobType calldevicesettings for the given organization in order of most recent one to
        oldest one irrespective of its status.

        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Retrieve list of 'calldevicesettings' jobs for this organization.
        :type org_id: str
        :param params: optional parameters
        :return: Generator of :class:`StartJobResponse` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=StartJobResponse, params=params)]

    async def get_status(self, job_id: str, org_id: str = None) -> StartJobResponse:
        """
        Get change device settings job status.

        Provides details of the job with jobId of jobType calldevicesettings.

        This API requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :type job_id: str
        :param org_id: Retrieve job details for this org
        :type org_id: str
        :return: job details
        :rtype: StartJobResponse
        """
        url = self.ep(job_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url=url, params=params)
        return StartJobResponse.parse_obj(data)

    def job_errors_gen(self, job_id: str, org_id: str = None) -> AsyncGenerator[JobErrorItem, None, None]:
        """
        List change device settings job errors.

        Lists all error details of the job with jobId of jobType calldevicesettings.

        This API requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :param org_id: Retrieve list of jobs for this organization.
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{job_id}/errors')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=JobErrorItem, params=params)

    async def job_errors(self, job_id: str, org_id: str = None) -> List[JobErrorItem]:
        """
        List change device settings job errors.

        Lists all error details of the job with jobId of jobType calldevicesettings.

        This API requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :param org_id: Retrieve list of jobs for this organization.
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{job_id}/errors')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=JobErrorItem, params=params)]


class AsDevicesApi(AsApiChild, base='devices'):
    """
    Devices represent cloud-registered Webex RoomOS devices. Devices may be associated with Workspaces.

    Searching and viewing details for your devices requires an auth token with the spark:devices_read scope. Updating or
    deleting your devices requires an auth token with the spark:devices_write scope. Viewing the list of all devices in
    an organization requires an administrator auth token with the spark-admin:devices_read scope. Adding, updating,
    or deleting all devices in an organization requires an administrator auth token with the spark-admin:devices_write
    scope. Generating an activation code requires an auth token with the identity:placeonetimepassword_create scope.
    """

    #: device jobs Api
    settings_jobs: AsDeviceSettingsJobsApi

    def __init__(self, *, session: AsRestSession):
        super().__init__(session=session)
        self.settings_jobs = AsDeviceSettingsJobsApi(session=session)

    def list_gen(self, person_id: str = None, workspace_id: str = None, display_name: str = None, product: str = None,
             product_type: str = None, tag: str = None, connection_status: str = None, serial: str = None,
             software: str = None, upgrade_channel: str = None, error_code: str = None, capability: str = None,
             permission: str = None, org_id: str = None, **params) -> AsyncGenerator[Device, None, None]:
        """
        List Devices

        Lists all active Webex devices associated with the authenticated user, such as devices activated in personal
        mode. Administrators can list all devices within an organization.

        :param person_id: List devices by person ID.
        :type person_id: str
        :param workspace_id: List devices by workspace ID.
        :type workspace_id: str
        :param display_name: List devices with this display name.
        :type display_name: str
        :param product: List devices with this product name.
        :type product: str
        :param product_type: List devices with this type.
        :type product_type: str
        :param tag: List devices which have a tag. Searching for multiple tags (logical AND) can be done by comma
        :type tag: str
            separating the tag values or adding several tag parameters.
        :param connection_status: List devices with this connection statu
        :type connection_status: str
        :param serial: List devices with this serial number.
        :type serial: str
        :param software: List devices with this software version.
        :type software: str
        :param upgrade_channel: List devices with this upgrade channel.
        :type upgrade_channel: str
        :param error_code: List devices with this error code.
        :type error_code: str
        :param capability: List devices with this capability.
        :type capability: str
        :param permission: List devices with this permission.
        :type permission: str
        :param org_id: List devices in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :return: Generator yielding :class:`Device` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if p not in {'self', 'params'} and v is not None)
        pt = params.pop(product_type, None)
        if pt is not None:
            params['type'] = pt
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Device, params=params, item_key='items')

    async def list(self, person_id: str = None, workspace_id: str = None, display_name: str = None, product: str = None,
             product_type: str = None, tag: str = None, connection_status: str = None, serial: str = None,
             software: str = None, upgrade_channel: str = None, error_code: str = None, capability: str = None,
             permission: str = None, org_id: str = None, **params) -> List[Device]:
        """
        List Devices

        Lists all active Webex devices associated with the authenticated user, such as devices activated in personal
        mode. Administrators can list all devices within an organization.

        :param person_id: List devices by person ID.
        :type person_id: str
        :param workspace_id: List devices by workspace ID.
        :type workspace_id: str
        :param display_name: List devices with this display name.
        :type display_name: str
        :param product: List devices with this product name.
        :type product: str
        :param product_type: List devices with this type.
        :type product_type: str
        :param tag: List devices which have a tag. Searching for multiple tags (logical AND) can be done by comma
        :type tag: str
            separating the tag values or adding several tag parameters.
        :param connection_status: List devices with this connection statu
        :type connection_status: str
        :param serial: List devices with this serial number.
        :type serial: str
        :param software: List devices with this software version.
        :type software: str
        :param upgrade_channel: List devices with this upgrade channel.
        :type upgrade_channel: str
        :param error_code: List devices with this error code.
        :type error_code: str
        :param capability: List devices with this capability.
        :type capability: str
        :param permission: List devices with this permission.
        :type permission: str
        :param org_id: List devices in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :return: Generator yielding :class:`Device` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if p not in {'self', 'params'} and v is not None)
        pt = params.pop(product_type, None)
        if pt is not None:
            params['type'] = pt
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=Device, params=params, item_key='items')]

    async def details(self, device_id: str, org_id: str = None) -> Device:
        """
        Get Device Details
        Shows details for a device, by ID.

        Specify the device ID in the deviceId parameter in the URI.

        :param device_id: A unique identifier for the device.
        :type device_id: str
        :param org_id:
        :type org_id: str
        :return: Device details
        :rtype: Device
        """
        url = self.ep(device_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url=url, params=params)
        return Device.parse_obj(data)

    async def delete(self, device_id: str, org_id: str = None):
        """
        Delete a Device

        Deletes a device, by ID.

        Specify the device ID in the deviceId parameter in the URI.

        :param device_id: A unique identifier for the device.
        :type device_id: str
        :param org_id:
        :type org_id: str
        """
        url = self.ep(device_id)
        params = org_id and {'orgId': org_id} or None
        await super().delete(url=url, params=params)

    async def modify_device_tags(self, device_id: str, op: TagOp, value: List[str], org_id: str = None) -> Device:
        """
        Modify Device Tags

        Update requests use JSON Patch syntax.

        :param device_id: A unique identifier for the device.
        :type device_id: str
        :param op: tag operation
        :type op: TagOp
        :param value: list of tags
        :type value: list[str]
        :param org_id:
        :type org_id: str
        :return: device details
        :rtype: Device
        """
        body = {'op': op.value if isinstance(op, TagOp) else op,
                'path': 'tags',
                'value': value}
        url = self.ep(device_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.patch(url=url, json=body, params=params, content_type='application/json-patch+json')
        return Device.parse_obj(data)

    async def activation_code(self, workspace_id: str, org_id: str = None) -> ActivationCodeResponse:
        """
        Create a Device Activation Code

        Generate an activation code for a device in a specific workspace by workspaceId. Currently, activation codes
        may only be generated for shared workspaces--personal mode is not supported.

        :param workspace_id: The workspaceId of the workspace where the device will be activated.
        :param org_id:
        :return: activation code and expiry time
        :rtype: ActivationCodeResponse
        """
        url = self.ep('activationCode')
        params = org_id and {'orgId': org_id} or None
        data = await self.post(url=url, params=params, json={'workspaceId': workspace_id})
        return ActivationCodeResponse.parse_obj(data)


class AsEventsApi(AsApiChild, base='events'):
    """
    Events are generated when actions take place within Webex, such as when someone creates or deletes a message.
    The Events API can only be used by a Compliance Officer with an API access token that contains the
    spark-compliance:events_read scope. See the Compliance Guide for more information.
    """

    def list_gen(self, resource: EventResource = None, type_: EventType = None, actor_id: str = None,
             from_: datetime = None, to_: datetime = None, **params) -> AsyncGenerator[ComplianceEvent, None, None]:
        """
        List events in your organization.
        Several query parameters are available to filter the events returned in
        the response. Long result sets will be split into pages.

        :param resource: List events with a specific resource type.
        :type resource: EventResource
        :param type_: List events with a specific event type.
        :type type_: EventType
        :param actor_id: List events performed by this person, by person ID.
        :type actor_id: str
        :param from_: List events which occurred after a specific date and time.
        :type from_: str
        :param to_: List events which occurred before a specific date and time. If unspecified, or set to a time in the
            future, lists events up to the present.
        :type to_: str
        """
        if resource is not None:
            params['resource'] = resource
        if type_ is not None:
            params['type'] = type_
        if actor_id is not None:
            params['actorId'] = actor_id
        if from_ is not None:
            params['from'] = dt_iso_str(from_)
        if to_ is not None:
            params['to'] = dt_iso_str(to_)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ComplianceEvent, params=params)

    async def list(self, resource: EventResource = None, type_: EventType = None, actor_id: str = None,
             from_: datetime = None, to_: datetime = None, **params) -> List[ComplianceEvent]:
        """
        List events in your organization.
        Several query parameters are available to filter the events returned in
        the response. Long result sets will be split into pages.

        :param resource: List events with a specific resource type.
        :type resource: EventResource
        :param type_: List events with a specific event type.
        :type type_: EventType
        :param actor_id: List events performed by this person, by person ID.
        :type actor_id: str
        :param from_: List events which occurred after a specific date and time.
        :type from_: str
        :param to_: List events which occurred before a specific date and time. If unspecified, or set to a time in the
            future, lists events up to the present.
        :type to_: str
        """
        if resource is not None:
            params['resource'] = resource
        if type_ is not None:
            params['type'] = type_
        if actor_id is not None:
            params['actorId'] = actor_id
        if from_ is not None:
            params['from'] = dt_iso_str(from_)
        if to_ is not None:
            params['to'] = dt_iso_str(to_)
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=ComplianceEvent, params=params)]

    async def details(self, event_id: str) -> ComplianceEvent:
        """
        Shows details for an event, by event ID.
        Specify the event ID in the eventId parameter in the URI.

        :param event_id: The unique identifier for the event.
        :type event_id: str
        """
        url = self.ep(f'{event_id}')
        data = await super().get(url=url)
        return ComplianceEvent.parse_obj(data)


class AsGroupsApi(AsApiChild, base='groups'):

    def list_gen(self, include_members: bool = None, attributes: str = None, sort_by: str = None,
             sort_order: str = None, list_filter: str = None, org_id: str = None,
             **params) -> AsyncGenerator[Group, None, None]:
        """
        List groups

        :param include_members: Include members in list response
        :type include_members: bool
        :param attributes: comma separated list of attributes to return
        :type attributes: str
        :param sort_by: attribute to sort by
        :type sort_by: str
        :param sort_order: sort order, ascending or descending
        :type sort_order: str
        :param org_id: organisation ID
        :type org_id: str
        :param list_filter: filter expression. Example: displayName eq "test"
        :type list_filter: str
        :param params:
        :return: generator of :class:`Group` objects
        """
        params.update((to_camel(k), v) for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        for k, v in params.items():
            if isinstance(v, bool):
                params[k] = 'true' if v else 'false'
        if lf := params.pop('listFilter', None):
            params['filter'] = lf
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Group, item_key='groups', params=params)

    async def list(self, include_members: bool = None, attributes: str = None, sort_by: str = None,
             sort_order: str = None, list_filter: str = None, org_id: str = None,
             **params) -> List[Group]:
        """
        List groups

        :param include_members: Include members in list response
        :type include_members: bool
        :param attributes: comma separated list of attributes to return
        :type attributes: str
        :param sort_by: attribute to sort by
        :type sort_by: str
        :param sort_order: sort order, ascending or descending
        :type sort_order: str
        :param org_id: organisation ID
        :type org_id: str
        :param list_filter: filter expression. Example: displayName eq "test"
        :type list_filter: str
        :param params:
        :return: generator of :class:`Group` objects
        """
        params.update((to_camel(k), v) for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        for k, v in params.items():
            if isinstance(v, bool):
                params[k] = 'true' if v else 'false'
        if lf := params.pop('listFilter', None):
            params['filter'] = lf
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=Group, item_key='groups', params=params)]

    async def create(self, settings: Group) -> Group:
        """
        Create a new group using the provided settings. Only display_name is mandatory

        :param settings: settings for new group
        :type settings: Group
        :return: new group
        :rtype: :class:`Group`
        """
        url = self.ep()
        body = settings.json(exclude={'group_id': True,
                                      'members': {'__all__': {'member_type': True,
                                                              'display_name': True,
                                                              'operation': True}},
                                      'created': True,
                                      'last_modified': True})
        data = await self.post(url, data=body)
        return Group.parse_obj(data)

    async def details(self, group_id: str, include_members: bool = None) -> Group:
        """
        Get group details

        :param group_id: group id
        :type group_id: str
        :param include_members: return members in response
        :type include_members: bool
        :return: group details
        :rtype: Group
        """
        url = self.ep(group_id)
        params = dict()
        if include_members is not None:
            params['includeMembers'] = 'true' if include_members else 'false'
        data = await self.get(url, params=params)
        return Group.parse_obj(data)

    def members_gen(self, group_id: str, **params) -> AsyncGenerator[GroupMember, None, None]:
        """
        Query members of a group

        :param group_id: group id
        :type group_id: str
        :param params:
        :return: generator of :class:`GroupMember` instances
        """
        url = self.ep(f'{group_id}/Members')
        return self.session.follow_pagination(url=url, model=GroupMember, params=params, item_key='members')

    async def members(self, group_id: str, **params) -> List[GroupMember]:
        """
        Query members of a group

        :param group_id: group id
        :type group_id: str
        :param params:
        :return: generator of :class:`GroupMember` instances
        """
        url = self.ep(f'{group_id}/Members')
        return [o async for o in self.session.follow_pagination(url=url, model=GroupMember, params=params, item_key='members')]

    async def update(self, group_id: str, settings: Group = None, remove_all: bool = None) -> Group:
        """
        update group information.

        Options: change displayName, add new members, remove some or all members, replace all members

        :param group_id:
        :param settings:
        :param remove_all:
        :return:
        """
        if not any((settings, remove_all)):
            raise ValueError('settings or remove_all have to be present')
        url = self.ep(group_id)
        if settings:
            body = settings.json(exclude={'group_id': True,
                                          'members': {'__all__': {'member_type': True,
                                                                  'display_name': True}},
                                          'created': True,
                                          'last_modified': True})
        else:
            body = 'purgeAllValues:{"attributes":["members"]}'
        data = await self.patch(url, data=body)
        return Group.parse_obj(data)

    async def delete_group(self, group_id: str):
        """
        Delete a group

        :param group_id: group id
        :type group_id: str
        """
        url = self.ep(group_id)
        await self.delete(url)


class AsLicensesApi(AsApiChild, base='licenses'):
    """
    Licenses

    An allowance for features and services that are provided to users on a Webex services subscription. Cisco and its
    partners manage the amount of licenses provided to administrators and users. This license resource can be accessed
    only by an admin.
    """

    def list_gen(self, org_id: str = None) -> AsyncGenerator[License, None, None]:
        """
        List all licenses for a given organization. If no org_id is specified, the default is the organization of
        the authenticated user.

        Response properties that are not applicable to the license will not be present in the response.

        :param org_id: List licenses for this organization.
        :type org_id: str
        :return: yields :class:`License` instances
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=License, params=params)

    async def list(self, org_id: str = None) -> List[License]:
        """
        List all licenses for a given organization. If no org_id is specified, the default is the organization of
        the authenticated user.

        Response properties that are not applicable to the license will not be present in the response.

        :param org_id: List licenses for this organization.
        :type org_id: str
        :return: yields :class:`License` instances
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=License, params=params)]

    async def details(self, license_id) -> License:
        """
        Shows details for a license, by ID.

        Response properties that are not applicable to the license will not be present in the response.

        :param license_id: The unique identifier for the license.
        :type license_id: str
        :return: license details
        :rtype: License
        """
        ep = self.ep(license_id)
        return License.parse_obj(await self.get(ep))


class AsLocationsApi(AsApiChild, base='locations'):
    """
    Location API

    Locations are used to organize Webex Calling (BroadCloud) features within physical locations. Webex Control Hub
    may be used to define new locations.

    Searching and viewing locations in your organization requires an administrator auth token with the
    spark-admin:people_read and spark-admin:people_write or spark-admin:device_read AND spark-admin:device_write
    scope combinations.
    """

    def list_gen(self, name: str = None, location_id: str = None, org_id: str = None,
             **params) -> AsyncGenerator[Location, None, None]:
        """
        List locations for an organization.

        :param name: List locations whose name contains this string (case-insensitive).
        :type name: str
        :param location_id: List locations by ID.
        :type location_id: str
        :param org_id: List locations in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: generator of :class:`Location` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        if location_id is not None:
            params.pop('locationId')
            params['id'] = location_id
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Location, params=params)

    async def list(self, name: str = None, location_id: str = None, org_id: str = None,
             **params) -> List[Location]:
        """
        List locations for an organization.

        :param name: List locations whose name contains this string (case-insensitive).
        :type name: str
        :param location_id: List locations by ID.
        :type location_id: str
        :param org_id: List locations in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: generator of :class:`Location` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        if location_id is not None:
            params.pop('locationId')
            params['id'] = location_id
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=Location, params=params)]

    async def by_name(self, name: str, org_id: str = None) -> Optional[Location]:
        """
        Get a location by name

        :param name: name of the location to search
        :type name: str
        :param org_id: search in list of locations  in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: locations
        :rtype: Location
        """
        return next((location for location in await self.list(name=name, org_id=org_id)
                     if location.name == name), None)

    async def details(self, location_id) -> Location:
        """
        Shows details for a location, by ID.

        This API only works for Customer administrators and for Partner administrators to query their own organization.
        Partner administrators looking to query customer organizations should use the List Locations endpoint to
        retrieve information about locations.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :return: location details
        :rtype: :class:`Location`
        """
        ep = self.ep(location_id)
        return Location.parse_obj(await self.get(ep))

    async def create(self, name: str, time_zone: str, preferred_language: str, announcement_language: str, address1: str,
               city: str, state: str, postal_code: str, country: str, address2: str = None, org_id: str = None) -> str:
        """
        Create a new Location for a given organization. Only an admin in a Webex Calling licensed organization can
        create a new Location.

        The following body parameters are required to create a new location: name, timeZone, preferredLanguage,
        address, announcementLanguage.

        Creating a location in your organization requires an administrator auth token with
        the spark-admin:locations_write.

        :param name: The name of the location.
        :type name: str
        :param time_zone: Time zone associated with this location
        :type time_zone: str
        :param preferred_language: Default email language.
        :type preferred_language: str
        :param announcement_language: Location's phone announcement language.
        :type announcement_language: str
        :param address1: Address 1
        :type address1: str
        :param address2: Address 2
        :type address2: str
        :param city: City
        :type city: str
        :param state: State Code
        :type state: str
        :param postal_code: Postal Code
        :type postal_code: str
        :param country: ISO-3166 2-Letter Country Code.
        :type country: str
        :param org_id: Create a location common attribute for this organization.
        :type org_id: str
        :return: ID of new location
        :rtype: :class:`Location`
        """
        # TODO: unit tests
        body = {}
        address = {}
        for p, v in list(locals().items()):
            if p in {'address', 'body', 'self'} or v is None:
                continue
            p = to_camel(p)
            if p == 'address1' or address:
                address[p] = v
            else:
                body[p] = v
        body['address'] = address
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = await self.post(url=url, json=body, params=params)
        return data['id']

    async def update(self, location_id: str, settings: Location, org_id: str = None):
        """
        Update details for a location, by ID.

        Specify the location ID in the locationId parameter in the URI. Only an admin can update a location details.

        Updating a location in your organization requires an administrator auth token with
        the spark-admin:locations_write.

        :param location_id: Update location common attributes for this location.
        :type location_id: str
        :param settings: new settings for the org:
        :type settings: :class:`Location`
        :param org_id: Update location common attributes for this organization
        :type org_id: str
        """
        settings_copy = settings.copy(deep=True)
        if settings_copy.address and not settings_copy.address.address2:
            settings_copy.address.address2 = None

        data = settings_copy.json(exclude={'location_id', 'org_id'}, exclude_none=False, exclude_unset=True)
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id)
        await self.put(url=url, data=data, params=params)


class AsMembershipApi(AsApiChild, base='memberships'):
    """
    Memberships represent a person's relationship to a room. Use this API to list members of any room that you're in
    or create memberships to invite someone to a room. Compliance Officers can now also list memberships for
    personEmails where the CO is not part of the room.
    Memberships can also be updated to make someone a moderator, or deleted, to remove someone from the room.
    Just like in the Webex client, you must be a member of the room in order to list its memberships or invite people.
    """

    def list_gen(self, room_id: str = None, person_id: str = None, person_email: str = None,
             **params) -> AsyncGenerator[Membership, None, None]:
        """
        Lists all room memberships. By default, lists memberships for rooms to which the authenticated user belongs.
        Use query parameters to filter the response.
        Use roomId to list memberships for a room, by ID.
        NOTE: For moderated team spaces, the list of memberships will include only the space moderators if the user
        is a team member but not a direct participant of the space.
        Use either personId or personEmail to filter the results. The roomId parameter is required when using these
        parameters.
        Long result sets will be split into pages.

        :param room_id: List memberships associated with a room, by ID.
        :type room_id: str
        :param person_id: List memberships associated with a person, by ID. The roomId parameter is required
            when using this parameter.
        :type person_id: str
        :param person_email: List memberships associated with a person, by email address. The roomId parameter
            is required when using this parameter.
        :type person_email: str
        """
        if room_id is not None:
            params['roomId'] = room_id
        if person_id is not None:
            params['personId'] = person_id
        if person_email is not None:
            params['personEmail'] = person_email
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Membership, params=params)

    async def list(self, room_id: str = None, person_id: str = None, person_email: str = None,
             **params) -> List[Membership]:
        """
        Lists all room memberships. By default, lists memberships for rooms to which the authenticated user belongs.
        Use query parameters to filter the response.
        Use roomId to list memberships for a room, by ID.
        NOTE: For moderated team spaces, the list of memberships will include only the space moderators if the user
        is a team member but not a direct participant of the space.
        Use either personId or personEmail to filter the results. The roomId parameter is required when using these
        parameters.
        Long result sets will be split into pages.

        :param room_id: List memberships associated with a room, by ID.
        :type room_id: str
        :param person_id: List memberships associated with a person, by ID. The roomId parameter is required
            when using this parameter.
        :type person_id: str
        :param person_email: List memberships associated with a person, by email address. The roomId parameter
            is required when using this parameter.
        :type person_email: str
        """
        if room_id is not None:
            params['roomId'] = room_id
        if person_id is not None:
            params['personId'] = person_id
        if person_email is not None:
            params['personEmail'] = person_email
        url = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=Membership, params=params)]

    async def create(self, room_id: str, person_id: str = None, person_email: str = None,
               is_moderator: bool = None) -> Membership:
        """
        Add someone to a room by Person ID or email address, optionally making them a moderator.

        :param room_id: The room ID.
        :type room_id: str
        :param person_id: The person ID.
        :type person_id: str
        :param person_email: The email address of the person.
        :type person_email: str
        :param is_moderator: Whether or not the participant is a room moderator.
        :type is_moderator: bool
        """
        body = {}
        if room_id is not None:
            body['roomId'] = room_id
        if person_id is not None:
            body['personId'] = person_id
        if person_email is not None:
            body['personEmail'] = person_email
        if is_moderator is not None:
            body['isModerator'] = is_moderator
        url = self.ep()
        data = await super().post(url=url, json=body)
        return Membership.parse_obj(data)

    async def details(self, membership_id: str) -> Membership:
        """
        Get details for a membership by ID.
        Specify the membership ID in the membershipId URI parameter.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str
        """
        url = self.ep(f'{membership_id}')
        data = await super().get(url=url)
        return Membership.parse_obj(data)

    async def update(self, update: Membership) -> Membership:
        """
        Updates properties for a membership by ID

        :param update: new settings; ID has to be set in update.

            These can be updated:
                is_moderator: bool: Whether or not the participant is a room moderator.

                is_room_hidden: bool: When set to true, hides direct spaces in the teams client. Any new message will
                make the room visible again.
        :type update: Membership

        """
        data = update.json(include={'is_moderator', 'is_room_hidden'})
        if update.id is None:
            raise ValueError('ID has to be set')
        url = self.ep(f'{update.id}')
        data = await super().put(url=url, data=data)
        return Membership.parse_obj(data)

    async def delete(self, membership_id: str):
        """
        Deletes a membership by ID.
        Specify the membership ID in the membershipId URI parameter.
        The membership for the last moderator of a Team's General space may not be deleted; promote another user to
        team moderator first.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str
        """
        url = self.ep(f'{membership_id}')
        await super().delete(url=url)
        return


class AsMessagesApi(AsApiChild, base='messages'):
    """

    """

    def list_gen(self, room_id: str, parent_id: str = None, mentioned_people: List[str] = None, before: datetime = None,
             before_message: str = None, **params) -> AsyncGenerator[Message, None, None]:
        """
        Lists all messages in a room.  Each message will include content attachments if present.
        The list sorts the messages in descending order by creation date.
        Long result sets will be split into pages.

        :param room_id: List messages in a room, by ID.
        :type room_id: str
        :param parent_id: List messages with a parent, by ID.
        :type parent_id: str
        :param mentioned_people: List messages with these people mentioned, by ID. Use me as a shorthand
            for the current API user. Only me or the person ID of the current user may be specified. Bots must include
            this parameter to list messages in group rooms (spaces).
        :type mentioned_people: List[str]
        :param before: List messages sent before a date and time.
        :type before: str
        :param before_message: List messages sent before a message, by ID.
        :type before_message: str
        """
        if room_id is not None:
            params['roomId'] = room_id
        if parent_id is not None:
            params['parentId'] = parent_id
        if mentioned_people is not None:
            params['mentionedPeople'] = mentioned_people
        if before is not None:
            params['before'] = dt_iso_str(before)
        if before_message is not None:
            params['beforeMessage'] = before_message
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Message, params=params)

    async def list(self, room_id: str, parent_id: str = None, mentioned_people: List[str] = None, before: datetime = None,
             before_message: str = None, **params) -> List[Message]:
        """
        Lists all messages in a room.  Each message will include content attachments if present.
        The list sorts the messages in descending order by creation date.
        Long result sets will be split into pages.

        :param room_id: List messages in a room, by ID.
        :type room_id: str
        :param parent_id: List messages with a parent, by ID.
        :type parent_id: str
        :param mentioned_people: List messages with these people mentioned, by ID. Use me as a shorthand
            for the current API user. Only me or the person ID of the current user may be specified. Bots must include
            this parameter to list messages in group rooms (spaces).
        :type mentioned_people: List[str]
        :param before: List messages sent before a date and time.
        :type before: str
        :param before_message: List messages sent before a message, by ID.
        :type before_message: str
        """
        if room_id is not None:
            params['roomId'] = room_id
        if parent_id is not None:
            params['parentId'] = parent_id
        if mentioned_people is not None:
            params['mentionedPeople'] = mentioned_people
        if before is not None:
            params['before'] = dt_iso_str(before)
        if before_message is not None:
            params['beforeMessage'] = before_message
        url = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=Message, params=params)]

    def list_direct_gen(self, parent_id: str = None, person_id: str = None, person_email: str = None,
                    **params) -> AsyncGenerator[Message, None, None]:
        """
        List all messages in a 1:1 (direct) room. Use the personId or personEmail query parameter to specify the
        room. Each message will include content attachments if present.
        The list sorts the messages in descending order by creation date.

        :param parent_id: List messages with a parent, by ID.
        :type parent_id: str
        :param person_id: List messages in a 1:1 room, by person ID.
        :type person_id: str
        :param person_email: List messages in a 1:1 room, by person email.
        :type person_email: str
        """
        if parent_id is not None:
            params['parentId'] = parent_id
        if person_id is not None:
            params['personId'] = person_id
        if person_email is not None:
            params['personEmail'] = person_email
        url = self.ep('direct')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Message, params=params)

    async def list_direct(self, parent_id: str = None, person_id: str = None, person_email: str = None,
                    **params) -> List[Message]:
        """
        List all messages in a 1:1 (direct) room. Use the personId or personEmail query parameter to specify the
        room. Each message will include content attachments if present.
        The list sorts the messages in descending order by creation date.

        :param parent_id: List messages with a parent, by ID.
        :type parent_id: str
        :param person_id: List messages in a 1:1 room, by person ID.
        :type person_id: str
        :param person_email: List messages in a 1:1 room, by person email.
        :type person_email: str
        """
        if parent_id is not None:
            params['parentId'] = parent_id
        if person_id is not None:
            params['personId'] = person_id
        if person_email is not None:
            params['personEmail'] = person_email
        url = self.ep('direct')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=Message, params=params)]

    async def create(self, room_id: str = None, parent_id: str = None, to_person_id: str = None, to_person_email: str = None,
               text: str = None, markdown: str = None, files: List[str] = None,
               attachments: List[Union[dict, MessageAttachment]] = None) -> Message:
        """
        Post a plain text or rich text message, and optionally, a file attachment, to a room.
        The files parameter is an array, which accepts multiple values to allow for future expansion, but currently
        only one file may be included with the message. File previews are only rendered for attachments of 1MB or less.

        :param room_id: The room ID of the message.
        :type room_id: str
        :param parent_id: The parent message to reply to.
        :type parent_id: str
        :param to_person_id: The person ID of the recipient when sending a private 1:1 message.
        :type to_person_id: str
        :param to_person_email: The email address of the recipient when sending a private 1:1 message.
        :type to_person_email: str
        :param text: The message, in plain text. If markdown is specified this parameter may be optionally used
            to provide alternate text for UI clients that do not support rich text. The maximum message length is 7439
            bytes.
        :type text: str
        :param markdown: The message, in Markdown format. The maximum message length is 7439 bytes.
        :type markdown: str
        :param files: The public URL to a binary file or a path to a local file to be posted into the room.
            Only one file is allowed
            per message. Uploaded files are automatically converted into a format that all Webex clients can render. For
            the supported media types and the behavior of uploads, see the Message Attachments Guide.
        :type files: List[str]
        :param attachments: Content attachments to attach to the message. Only one card per message
            is supported. See the Cards Guide for more information.
        :type attachments: List[Attachment]
        :rtype: Message
        """
        # TODO: handle local files for attachments
        body = {}
        if room_id is not None:
            body['roomId'] = room_id
        if parent_id is not None:
            body['parentId'] = parent_id
        if to_person_id is not None:
            body['toPersonId'] = to_person_id
        if to_person_email is not None:
            body['toPersonEmail'] = to_person_email
        if text is not None:
            body['text'] = text
        if markdown is not None:
            body['markdown'] = markdown
        if attachments is not None:
            body['attachments'] = [a.dict(by_alias=True) if isinstance(a, MessageAttachment) else a
                                   for a in attachments]
        if files is not None:
            body['files'] = files

        url = self.ep()
        if files and os.path.isfile(files[0]):
            # this is a local file
            open_file = open(files[0], mode='rb')
            try:
                c_type = mimetypes.guess_type(files[0])[0] or 'text/plain'
                body['files'] = (os.path.basename(files[0]),
                                 open_file,
                                 c_type)
                multipart = MultipartEncoder(body)
                headers = {'Content-type': multipart.content_type}
                data = await super().post(url=url, headers=headers, data=multipart)
            finally:
                open_file.close()
        else:
            data = await super().post(url=url, json=body)
        return Message.parse_obj(data)

    async def edit(self, message: Message) -> Message:
        """
        Update a message you have posted not more than 10 times.
        Specify the messageId of the message you want to edit.
        Edits of messages containing files or attachments are not currently supported.
        If a user attempts to edit a message containing files or attachments a 400 Bad Request will be returned by
        the API with a message stating that the feature is currently unsupported.
        There is also a maximum number of times a user can edit a message. The maximum currently supported is 10
        edits per message.
        If a user attempts to edit a message greater that the maximum times allowed the API will return 400 Bad
        Request with a message stating the edit limit has been reached.
        While only the roomId and text or markdown attributes are required in the request body, a common pattern for
        editing message is to first call GET /messages/{id} for the message you wish to edit and to then update the
        text or markdown attribute accordingly, passing the updated message object in the request body of the PUT
        /messages/{id} request.

        :param message: the updated message, id has to be set in the message
            attributes supported for update:

                * room_id: str: The room ID of the message.
                * text: str: The message, in plain text. If markdown is specified this parameter may be optionally used
                  to provide alternate text for UI clients that do not support rich text. The maximum message length
                  is 7439 bytes.
                * markdown: str: The message, in Markdown format. If this attribute is set ensure that the request does
                  NOT contain an html attribute.
        """
        data = message.json(include={'room_id', 'text', 'markdown'})
        if not message.id:
            raise ValueError('ID has to be set')
        url = self.ep(f'{message.id}')
        data = await super().put(url=url, data=data)
        return Message.parse_obj(data)

    async def details(self, message_id: str) -> Message:
        """
        Show details for a message, by message ID.
        Specify the message ID in the messageId parameter in the URI.

        :param message_id: The unique identifier for the message.
        :type message_id: str
        """
        url = self.ep(f'{message_id}')
        data = await super().get(url=url)
        return Message.parse_obj(data)

    async def delete(self, message_id: str):
        """
        Delete a message, by message ID.
        Specify the message ID in the messageId parameter in the URI.

        :param message_id: The unique identifier for the message.
        :type message_id: str
        """
        url = self.ep(f'{message_id}')
        await super().delete(url=url)
        return


class AsOrganizationApi(AsApiChild, base='organizations'):
    async def list(self) -> list[Organization]:
        """
        List all organizations visible by your account. The results will not be paginated.

        :return: list of Organizations
        """
        data = await self.get(url=self.ep())
        return parse_obj_as(list[Organization], data['items'])

    async def details(self, org_id: str) -> Organization:
        """
        Get Organization Details

        Shows details for an organization, by ID.

        :param org_id: The unique identifier for the organization.
        :type org_id: str
        :return: org details
        :rtype: :class:`Organization`
        """
        url = self.ep(org_id)
        data = await self.get(url=url)
        return Organization.parse_obj(data)

    async def delete(self, org_id: str):
        """
        Delete Organization

        Deletes an organization, by ID. It may take up to 10 minutes for the organization to be deleted after the
        response is returned.

        :param org_id: The unique identifier for the organization.
        :type org_id: str
        """
        url = self.ep(org_id)
        await super().delete(url=url)


class AsPeopleApi(AsApiChild, base='people'):
    """
    People API
    """

    def list_gen(self, email: str = None, display_name: str = None, id_list: list[str] = None, org_id: str = None,
             calling_data: bool = None, location_id: str = None, **params) -> AsyncGenerator[Person, None, None]:
        """
        List people in your organization. For most users, either the email or displayName parameter is required. Admin
        users can omit these fields and list all users in their organization.

        Response properties associated with a user's presence status, such as status or lastActivity, will only be
        returned for people within your organization or an organization you manage. Presence information will not be
        returned if the authenticated user has disabled status sharing.

        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true. Admin users can list all users in a location or with a specific phone number. Admin users
        will receive an enriched payload with additional administrative fields like liceneses,roles etc. These fields
        are shown when accessing a user via GET /people/{id}, not when doing a GET /people?id=

        Lookup by email is only supported for people within the same org or where a partner admin relationship is in
        place.

        :param email: List people with this email address. For non-admin requests, either this or displayName are
            required.
        :type email: str
        :param display_name: List people whose name starts with this string. For non-admin requests, either this or
            email are required.
        :type display_name: str
        :param id_list: List people by ID. Accepts up to 85 person IDs. If this parameter is provided then presence
            information (such as the last_activity or status properties) will not be included in the response.
        :type id_list: list[str]
        :param org_id: List people in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param calling_data: Include Webex Calling user details in the response. Default: False
        :type calling_data: bool
        :param location_id: List people present in this location.
        :type location_id: str
        :return: yield :class:`Person` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        if calling_data:
            params['callingData'] = 'true'
            # apparently there is a performance problem with getting too many users w/ calling data at the same time
            params['max'] = params.get('max', MAX_USERS_WITH_CALLING_DATA)
        id_list = params.pop('idList', None)
        if id_list:
            params['id'] = ','.join(id_list)
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Person, params=params)

    async def list(self, email: str = None, display_name: str = None, id_list: list[str] = None, org_id: str = None,
             calling_data: bool = None, location_id: str = None, **params) -> List[Person]:
        """
        List people in your organization. For most users, either the email or displayName parameter is required. Admin
        users can omit these fields and list all users in their organization.

        Response properties associated with a user's presence status, such as status or lastActivity, will only be
        returned for people within your organization or an organization you manage. Presence information will not be
        returned if the authenticated user has disabled status sharing.

        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true. Admin users can list all users in a location or with a specific phone number. Admin users
        will receive an enriched payload with additional administrative fields like liceneses,roles etc. These fields
        are shown when accessing a user via GET /people/{id}, not when doing a GET /people?id=

        Lookup by email is only supported for people within the same org or where a partner admin relationship is in
        place.

        :param email: List people with this email address. For non-admin requests, either this or displayName are
            required.
        :type email: str
        :param display_name: List people whose name starts with this string. For non-admin requests, either this or
            email are required.
        :type display_name: str
        :param id_list: List people by ID. Accepts up to 85 person IDs. If this parameter is provided then presence
            information (such as the last_activity or status properties) will not be included in the response.
        :type id_list: list[str]
        :param org_id: List people in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param calling_data: Include Webex Calling user details in the response. Default: False
        :type calling_data: bool
        :param location_id: List people present in this location.
        :type location_id: str
        :return: yield :class:`Person` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        if calling_data:
            params['callingData'] = 'true'
            # apparently there is a performance problem with getting too many users w/ calling data at the same time
            params['max'] = params.get('max', MAX_USERS_WITH_CALLING_DATA)
        id_list = params.pop('idList', None)
        if id_list:
            params['id'] = ','.join(id_list)
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=Person, params=params)]

    async def create(self, settings: Person, calling_data: bool = False) -> Person:
        """
        Create a Person

        Create a new user account for a given organization. Only an admin can create a new user account.

        At least one of the following body parameters is required to create a new user: displayName, firstName,
        lastName.

        Currently, users may have only one email address associated with their account. The emails parameter is an
        array, which accepts multiple values to allow for future expansion, but currently only one email address will
        be used for the new user.

        Admin users can include Webex calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.

        When doing attendee management, to make the new user an attendee for a site: append #attendee to the siteUrl
        parameter (eg: mysite.webex.com#attendee).

        :param settings: settings for new user
        :type settings: Person
        :param calling_data: Include Webex Calling user details in the response.
        :type calling_data: bool
        :return: new user
        :rtype: Person
        """
        params = calling_data and {'callingData': 'true'} or None
        url = self.ep()
        data = settings.json(exclude={'person_id': True,
                                      'created': True,
                                      'last_modified': True,
                                      'timezone': True,
                                      'last_activity': True,
                                      'sip_addresses': True,
                                      'status': True,
                                      'invite_pending': True,
                                      'login_enabled': True,
                                      'person_type': True})
        return Person.parse_obj(await self.post(url, data=data, params=params))

    async def details(self, person_id: str, calling_data: bool = False) -> Person:
        """
        Shows details for a person, by ID.

        Response properties associated with a user's presence status, such as status or last_activity, will only be
        displayed for people within your organization or an organization you manage. Presence information will not be
        shown if the authenticated user has disabled status sharing.

        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying calling_data
        parameter as True.

        :param person_id: A unique identifier for the person.
        :type person_id: str
        :param calling_data: Include Webex Calling user details in the response. Default: false
        :type calling_data: bool
        :return: person details
        :rtype: Person
        """
        ep = self.ep(path=person_id)
        params = calling_data and {'callingData': 'true'} or None
        return Person.parse_obj(await self.get(ep, params=params))

    async def delete_person(self, person_id: str):
        """
        Remove a person from the system. Only an admin can remove a person.

        :param person_id: A unique identifier for the person.
        :return:
        """
        ep = self.ep(path=person_id)
        await self.delete(ep)

    async def update(self, person: Person, calling_data: bool = False, show_all_types: bool = False) -> Person:
        """
        Update details for a person, by ID.

        Specify the person ID in the personId parameter in the URI. Only an admin can update a person details.

        Include all details for the person. This action expects all user details to be present in the request. A common
        approach is to first GET the person's details, make changes, then PUT both the changed and unchanged values.

        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.

        Note: The locationId can only be set when adding a calling license to a user. It cannot be changed if a user is
        already an existing calling user.

        When doing attendee management, to update a user from host role to an attendee for a site append #attendee to
        the respective siteUrl and remove the meeting host license for this site from the license array.

        To update a person from an attendee role to a host for a site, add the meeting license for this site in the
        meeting array, and remove that site from the siteurl parameter.

        To remove the attendee privilege for a user on a meeting site, remove the sitename#attendee from the siteUrls
        array. The showAllTypes parameter must be set to true.

        :param person: The person to update
        :type person: Person
        :param calling_data: Include Webex Calling user details in the response. Default: False
        :type calling_data: bool
        :param show_all_types: Include additional user data like #attendee role
        :type show_all_types: bool
        :return: Person details
        :rtype: Person
        """
        params = {}
        if calling_data:
            params['callingData'] = 'true'
        if show_all_types:
            params['showAllTypes'] = 'true'

        if not all(v is not None
                   for v in (person.display_name, person.first_name, person.last_name)):
            raise ValueError('display_name, first_name, and last_name are required')

        # some attributes should not be included in update
        data = person.json(exclude={'created': True,
                                    'last_modified': True,
                                    'timezone': True,
                                    'last_activity': True,
                                    'sip_addresses': True,
                                    'status': True,
                                    'invite_pending': True,
                                    'login_enabled': True,
                                    'person_type': True})
        ep = self.ep(path=person.person_id)
        return Person.parse_obj(await self.put(url=ep, data=data, params=params))

    async def me(self, calling_data: bool = False) -> Person:
        """
        Show the profile for the authenticated user. This is the same as GET /people/{personId} using the Person ID
        associated with your Auth token.

        Admin users can include Webex Calling (BroadCloud) user details in the response by specifying callingData
        parameter as true.

        :param calling_data: True -> return calling data
        :type calling_data: bool
        :rtype: Person
        :return: profile of authenticated user
        """
        ep = self.ep('me')
        params = calling_data and {'callingData': 'true'} or None
        data = await self.get(ep, params=params)
        result = Person.parse_obj(data)
        return result


class AsAgentCallerIdApi(AsApiChild, base='telephony/config/people'):
    """
    API to manage call queue agent caller ID information
    """

    # noinspection PyMethodOverriding
    def ep(self, person_id: str, path: str):
        """
        :meta private:
        """
        return super().ep(f'{person_id}/queues/{path}')

    def available_queues_gen(self, person_id: str, org_id: str = None) -> AsyncGenerator[AgentQueue, None, None]:
        """
        Retrieve the list of the person's available call queues and the associated Caller ID information

        If the Agent is to enable queueCallerIdEnabled, they must choose which queue to use as the source for
        outgoing Caller ID. This API returns a list of Call Queues from which the person must select. If this setting
        is disabled or Agent does not belong to any queue this list will be empty.

        This API requires a full admin or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: organization id
        :type org_id: str
        :return: yields person's available call queues and the associated Caller ID information
        :rtype: Generator[AgentQueue, None, None]
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(person_id=person_id, path='availableCallerIds')
        return self.session.follow_pagination(url=url, model=AgentQueue, params=params, item_key='availableQueues')

    async def available_queues(self, person_id: str, org_id: str = None) -> List[AgentQueue]:
        """
        Retrieve the list of the person's available call queues and the associated Caller ID information

        If the Agent is to enable queueCallerIdEnabled, they must choose which queue to use as the source for
        outgoing Caller ID. This API returns a list of Call Queues from which the person must select. If this setting
        is disabled or Agent does not belong to any queue this list will be empty.

        This API requires a full admin or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: organization id
        :type org_id: str
        :return: yields person's available call queues and the associated Caller ID information
        :rtype: Generator[AgentQueue, None, None]
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(person_id=person_id, path='availableCallerIds')
        return [o async for o in self.session.follow_pagination(url=url, model=AgentQueue, params=params, item_key='availableQueues')]

    async def read(self, person_id: str, org_id: str = None) -> QueueCallerId:
        """
        Retrieve a call queue agent's Caller ID information

        Each agent in the Call Queue will be able to set their outgoing Caller ID as either the Call Queue's phone
        number or their own configured Caller ID. This API fetches the configured Caller ID for the agent in the system.

        This API requires a full admin or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: organization id
        :type org_id: str
        :return: call queue agent's Caller ID information
        :rtype: QueueCallerId
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(person_id=person_id, path='callerId')
        data = await self.get(url=url, params=params)
        return QueueCallerId.parse_obj(data)

    async def update(self, person_id: str, update: QueueCallerId, org_id: str = None):
        """
        Modify a call queue agent's Caller ID information

        Each Agent in the Call Queue will be able to set their outgoing Caller ID as either the designated Call
        Queue's phone number or their own configured Caller ID. This API modifies the configured Caller ID for the
        agent in the system.

        This API requires a full or user administrator auth token with the spark-admin:telephony_config_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param update: new settings
        :type update: QueueCallerId
        :param org_id: organization id
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(person_id=person_id, path='callerId')
        body = update.for_update()
        await self.put(url=url, params=params, data=body)


class AsPersonSettingsApiChild(AsApiChild, base=''):
    """
    Base class for all classes implementing person settings APIs
    """

    feature = None

    def __init__(self, *, session: AsRestSession,
                 workspaces: bool = False, locations: bool = False):
        # set parameters to get the correct URL templates
        #
        #               selector                    feature_prefix  url template
        # workspaces    workspaces                  /features/      workspaces/{person_id}/features/{feature}{path}
        # locations     telephony/config/locations  /               telephony/config/locations/{person_id}{path}
        # person        people                      /features       people/{person_id}/features/{feature}{path}
        self.feature_prefix = '/features/'
        if workspaces:
            self.selector = 'workspaces'
        elif locations:
            self.selector = 'telephony/config/locations'
            self.feature_prefix = '/'
        else:
            self.selector = 'people'
        super().__init__(session=session, base=self.selector)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(base='')
        if cls.feature is None:
            raise TypeError('feature has to be defined')

    def f_ep(self, person_id: str, path: str = None) -> str:
        """
        person specific feature endpoint like v1/people/{uid}/features/....

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param path: path in the endpoint after the feature base URL
        :type path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        # url templates:
        #
        #               selector                    feature_prefix  url template
        # workspaces    workspaces                  /features/      workspaces/{person_id}/features/{feature}{path}
        # locations     telephony/config/locations  /               telephony/config/locations/{person_id}{path}
        # person        people                      /features       people/{person_id}/features/{feature}{path}
        return self.session.ep(f'{self.selector}/{person_id}{self.feature_prefix}{self.feature}{path}')


class AsAppServicesApi(AsPersonSettingsApiChild):
    """
    API for person's app services settings
    """

    feature = 'applications'

    async def read(self, person_id: str, org_id: str = None) -> AppServicesSettings:
        """
        Retrieve a Person's Application Services Settings

        Application services let you determine the ringing behavior for calls made to people in certain scenarios.
        You can also specify which devices can download the Webex Calling app.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: privacy settings
        :rtype: :class:`Privacy`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return AppServicesSettings.parse_obj(data)

    async def configure(self, person_id: str, settings: AppServicesSettings, org_id: str = None):
        """
        Modify a Person's Application Services Settings

        Application services let you determine the ringing behavior for calls made to users in certain scenarios. You
        can also specify which devices users can download the Webex Calling app on.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: settings for update
        :type settings: :class:`AppServicesSettings`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = settings.json(exclude={'available_line_count': True})
        await self.put(ep, params=params, data=data)


class AsBargeApi(AsPersonSettingsApiChild):
    """
    API for person's barge settings
    """

    feature = 'bargeIn'

    async def read(self, person_id: str, org_id: str = None) -> BargeSettings:
        """
        Retrieve a Person's Barge In Settings

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: barge settings for specific user
        :rtype: BargeSettings
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return BargeSettings.parse_obj(await self.get(ep, params=params))

    async def configure(self, person_id: str, barge_settings: BargeSettings, org_id: str = None):
        """
        Configure a Person's Barge In Settings

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param barge_settings: new setting to be applied
        :type barge_settings: BargeSettings
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        await self.put(ep, params=params, data=barge_settings.json())


class AsCallInterceptApi(AsPersonSettingsApiChild):
    """
    API for person's call intercept settings
    """

    feature = 'intercept'

    async def read(self, person_id: str, org_id: str = None) -> InterceptSetting:
        """
        Read Call Intercept Settings for a Person

        Retrieves Person's Call Intercept Settings

        The intercept feature gracefully takes a person’s phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none,
        some, or all incoming calls to the specified person are intercepted. Also depending on the service
        configuration, outgoing calls are intercepted or rerouted to another location.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: user's call intercept settings
        :rtype: InterceptSetting
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return InterceptSetting.parse_obj(await self.get(ep, params=params))

    async def configure(self, person_id: str, intercept: InterceptSetting, org_id: str = None):
        """
        Configure Call Intercept Settings for a Person

        Configures a Person's Call Intercept Settings

        The intercept feature gracefully takes a person’s phone out of service, while providing callers with
        informative announcements and alternative routing options. Depending on the service configuration, none, some,
        or all incoming calls to the specified person are intercepted. Also depending on the service configuration,
        outgoing calls are intercepted or rerouted to another location.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param intercept: new intercept settings
        :type intercept: InterceptSetting
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.loads(intercept.json())
        try:
            # remove attribute not present in update
            data['incoming']['announcements'].pop('fileName', None)
        except KeyError:
            pass
        await self.put(ep, params=params, json=data)

    async def greeting(self, person_id: str, content: Union[BufferedReader, str],
                 upload_as: str = None, org_id: str = None):
        """
        Configure Call Intercept Greeting for a Person

        Configure a Person's Call Intercept Greeting by uploading a Waveform Audio File Format, .wav, encoded audio
        file.

        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        if isinstance(content, str):
            upload_as = os.path.basename(content)
            content = open(content, mode='rb')
            must_close = True
            pass
        else:
            must_close = False
            # an existing reader
            if not upload_as:
                raise ValueError('upload_as is required')
        encoder = MultipartEncoder(fields={'file': (upload_as, content, 'audio/wav')})
        ep = self.f_ep(person_id=person_id, path='actions/announcementUpload/invoke')
        params = org_id and {'orgId': org_id} or None
        try:
            await self.post(ep, data=encoder, headers={'Content-Type': encoder.content_type},
                      params=params)
        finally:
            if must_close:
                content.close()
        return


class AsCallRecordingApi(AsPersonSettingsApiChild):
    """
    API for person's call recording settings
    """

    feature = 'callRecording'

    async def read(self, person_id: str, org_id: str = None) -> CallRecordingSetting:
        """
        Read Call Recording Settings for a Person

        Retrieve a Person's Call Recording Settings

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return CallRecordingSetting.parse_obj(await self.get(ep, params=params))

    async def configure(self, person_id: str, recording: CallRecordingSetting, org_id: str = None):
        """
        Configure Call Recording Settings for a Person

        Configure a Person's Call Recording Settings

        The Call Recording feature provides a hosted mechanism to record the calls placed and received on the Carrier
        platform for replay and archival. This feature is helpful for quality assurance, security, training, and more.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param recording: the new recording settings
        :type recording: CallRecordingSetting
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.loads(recording.json())
        for key in ['serviceProvider', 'externalGroup', 'externalIdentifier']:
            # remove attribute not present in update
            data.pop(key, None)
        await self.put(ep, params=params, json=data)


class AsCallWaitingApi(AsPersonSettingsApiChild):
    """
    API for person's call waiting settings
    """

    feature = 'callWaiting'

    async def read(self, person_id: str, org_id: str = None) -> bool:
        """
        Read Call Waiting Settings for a Person

        Retrieve a Person's Call Waiting Settings

        With this feature, a person can place an active call on hold and answer an incoming call. When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or
        ignore the call.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: call waiting setting
        :rtype: bool
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return data['enabled']

    async def configure(self, person_id: str, enabled: bool, org_id: str = None):
        """
        Configure Call Waiting Settings for a Person

        Configure a Person's Call Waiting Settings

        With this feature, a person can place an active call on hold and answer an incoming call. When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore
        the call.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: true if the Call Waiting feature is enabled.
        :type enabled: bool
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.dumps({'enabled': enabled})
        await self.put(ep, params=params, json=data)


class AsCallerIdApi(AsPersonSettingsApiChild):
    """
    API for person's caller id settings
    """

    feature = 'callerId'

    async def read(self, person_id: str, org_id: str = None) -> CallerId:
        """
        Retrieve a Person's Caller ID Settings

        Caller ID settings control how a person’s information is displayed when making outgoing calls.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return CallerId.parse_obj(await self.get(ep, params=params))

    async def configure(self, person_id: str, org_id: str = None,
                  selected: CallerIdSelectedType = None,
                  custom_number: str = None,
                  first_name: str = None,
                  last_name: str = None,
                  external_caller_id_name_policy: ExternalCallerIdNamePolicy = None,
                  custom_external_caller_id_name: str = None):
        """
        Configure a Person's Caller ID Settings

        Caller ID settings control how a person’s information is displayed when making outgoing calls.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param selected: Which type of outgoing Caller ID will be used.
        :type selected: CallerIdSelectedType
        :param custom_number: This value must be an assigned number from the person\'s location.
        :type custom_number: str
        :param first_name: Person\'s Caller ID first name. Characters of %, +, \`, \" and Unicode characters are not
            allowed.

        :type first_name: str
        :param last_name: Person\'s Caller ID last name. Characters of %, +, \`, \" and Unicode characters are not
            allowed.
        :type last_name: str
        :param external_caller_id_name_policy: Designates which type of External Caller ID Name policy is used.
            Default is DIRECT_LINE.
        :type external_caller_id_name_policy: ExternalCallerIdNamePolicy
        :param custom_external_caller_id_name: Custom External Caller Name, which will be shown if External Caller ID
            Name is OTHER.
        :type custom_external_caller_id_name: str

        """
        data = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                if i > 2 and v is not None}
        params = org_id and {'orgId': org_id} or None
        ep = self.f_ep(person_id=person_id)
        await self.put(ep, params=params, json=data)

    async def configure_settings(self, person_id: str, settings: CallerId, org_id: str = None):
        params = org_id and {'orgId': org_id} or None
        data = settings.json(exclude_unset=True, include={'selected': True,
                                                          'custom_number': True,
                                                          'first_name': True,
                                                          'last_name': True,
                                                          'block_in_forward_calls_enabled': True,
                                                          'external_caller_id_name_policy': True,
                                                          'custom_external_caller_id_name': True,
                                                          })
        ep = self.f_ep(person_id=person_id)
        await self.put(ep, params=params, data=data)


class AsCallingBehaviorApi(AsPersonSettingsApiChild):
    """
    API for person's calling behavior settings
    """

    feature = 'callingBehavior'

    async def read(self, person_id: str, org_id: str = None) -> CallingBehavior:
        """
        Read Person's Calling Behavior

        Retrieves the calling behavior and UC Manager Profile settings for the person which includes overall calling
        behavior and calling UC Manager Profile ID.

        Webex Calling Behavior controls which Webex telephony application is to be used.

        An organization has an organization-wide default Calling Behavior that may be overridden for individual persons.

        In addition, UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or
        Calling in Webex Teams (Unified CM).

        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: calling behavior setting
        :rtype: CallingBehavior
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return CallingBehavior.parse_obj(data)

    async def configure(self, person_id: str, settings: CallingBehavior,
                  org_id: str = None):
        """
        Configure a Person's Calling Behavior

        Modifies the calling behavior settings for the person which includes overall calling behavior and UC Manager
        Profile ID.

        Webex Calling Behavior controls which Webex telephony application is to be used.

        An organization has an organization-wide default Calling Behavior that may be overridden for individual persons.

        In addition, UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or
        Calling in Webex Teams (Unified CM).

        The UC Manager Profile also has an organization-wide default and may be overridden for individual persons.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: new settings
        :type settings: CallingBehavior
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = settings.json(exclude_none=False, exclude={'effective_behavior_type'}, exclude_unset=True)
        await self.put(ep, params=params, data=data)


class AsDndApi(AsPersonSettingsApiChild):
    """
    API for person's DND settings
    """

    feature = 'doNotDisturb'

    async def read(self, person_id: str, org_id: str = None) -> DND:
        """
        Read Do Not Disturb Settings for a Person
        Retrieve a Person's Do Not Disturb Settings

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.
        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners) may
        use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return:
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return DND.parse_obj(await self.get(ep, params=params))

    async def configure(self, person_id: str, dnd_settings: DND, org_id: str = None):
        """
        Configure Do Not Disturb Settings for a Person
        Configure a Person's Do Not Disturb Settings

        When enabled, this feature will give all incoming calls the busy treatment. Optionally, you can enable a Ring
        Reminder to play a brief tone on your desktop phone when you receive incoming calls.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param dnd_settings: new setting to be applied
        :type dnd_settings: DND
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        await self.put(ep, params=params, data=dnd_settings.json())


class AsExecAssistantApi(AsPersonSettingsApiChild):
    """
    API for person's exec assistant settings
    """

    feature = 'executiveAssistant'

    async def read(self, person_id: str, org_id: str = None) -> ExecAssistantType:
        """
        Retrieve Executive Assistant Settings for a Person

        Retrieve the executive assistant settings for the specified personId.

        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set
        the call forward destination and join or leave an executive's pool.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: exec assistant setting
        :rtype: :class:`ExecAssistantType`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        h: _Helper = _Helper.parse_obj(data)
        return h.exec_type

    async def configure(self, person_id: str, setting: ExecAssistantType, org_id: str = None):
        """
        Modify Executive Assistant Settings for a Person

        Modify the executive assistant settings for the specified personId.

        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set
        the call forward destination and join or leave an executive's pool.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param setting: New exex assistant settings
        :type setting: :class:`ExecAssistantType`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        h = _Helper(exec_type=setting)
        params = org_id and {'orgId': org_id} or None
        data = h.json()
        await self.put(ep, params=params, data=data)


class AsHotelingApi(AsPersonSettingsApiChild):
    """
    API for person's hoteling settings
    """

    feature = 'hoteling'

    async def read(self, person_id: str, org_id: str = None) -> bool:
        """
        Read Hoteling Settings for a Person

        Retrieve a person's hoteling settings.

        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features,
        and calling plan) is temporarily loaded onto a shared (host) phone.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: hoteling setting
        :rtype: bool
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return data['enabled']

    async def configure(self, person_id: str, enabled: bool, org_id: str = None):
        """
        Configure Hoteling Settings for a Person

        Configure a person's hoteling settings.

        As an administrator, you can enable hoteling for people so that their phone profile (phone number, features,
        and calling plan) is temporarily loaded onto a shared (host) phone.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param enabled: When true, allow this person to connect to a Hoteling host device.
        :type enabled: bool
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.dumps({'enabled': enabled})
        await self.put(ep, params=params, json=data)


class AsIncomingPermissionsApi(AsPersonSettingsApiChild):
    """
    API for person's incoming permissions settings
    """

    feature = 'incomingPermission'

    async def read(self, person_id: str, org_id: str = None) -> IncomingPermissions:
        """
        Read Incoming Permission Settings for a Person

        Retrieve a Person's Incoming Permission Settings

        You can change the incoming calling permissions for a person if you want them to be different from your
        organization's default.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: incoming permission settings for specific user
        :rtype: :class:`IncomingPermissions`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return IncomingPermissions.parse_obj(await self.get(ep, params=params))

    async def configure(self, person_id: str, settings: IncomingPermissions, org_id: str = None):
        """
        Configure a Person's Barge In Settings

        The Barge In feature enables you to use a Feature Access Code (FAC) to answer a call that was directed to
        another subscriber, or barge-in on the call if it was already answered. Barge In can be used across locations.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: new setting to be applied
        :type settings: :class:`IncomingPermissions`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        await self.put(ep, params=params, data=settings.json())


class AsMonitoringApi(AsPersonSettingsApiChild):
    """
    API for person's call monitoring settings
    """

    feature = 'monitoring'

    async def read(self, person_id: str, org_id: str = None) -> Monitoring:
        """
        Retrieve a Person's Monitoring Settings

        Retrieves the monitoring settings of the person, which shows specified people, places or, call park
        extensions under monitoring. Monitors the line status which indicates if a person or place is on a call and
        if  a call has been parked on that extension.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: monitoring settings
        :rtype: :class:`Monitoring`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return Monitoring.parse_obj(data)

    async def configure(self, person_id: str, settings: Monitoring, org_id: str = None):
        """
        Configure Call Waiting Settings for a Person

        Configure a Person's Call Waiting Settings

        With this feature, a person can place an active call on hold and answer an incoming call. When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore
        the call.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: settings for update
        :type settings: :class:`Monitoring`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = {}
        if settings.call_park_notification_enabled is not None:
            data['enableCallParkNotification'] = settings.call_park_notification_enabled
        if settings.monitored_elements is not None:
            id_list = []
            for me in settings.monitored_elements:
                if isinstance(me, str):
                    id_list.append(me)
                else:
                    id_list.append(me.member and me.member.member_id or me.cpe and me.cpe.cpe_id)
            data['monitoredElements'] = id_list
        await self.put(ep, params=params, json=data)


class AsNumbersApi(AsPersonSettingsApiChild):
    """
    API for person's numbers
    """

    feature = 'numbers'

    async def read(self, person_id: str, org_id: str = None) -> PersonNumbers:
        """
        Get a person's phone numbers including alternate numbers.

        A person can have one or more phone numbers and/or extensions via which they can be called.

        This API requires a full or user administrator auth token with
        the spark-admin:people_read scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners) may
            use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: Alternate numbers of the user
        :rtype: :class:`PersonNumbers`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return PersonNumbers.parse_obj(await self.get(ep, params=params))

    async def update(self, person_id: str, update: UpdatePersonNumbers, org_id: str = None):
        """
        Assign or unassign alternate phone numbers to a person.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone
        numbers must follow E.164 format for all countries, except for the United States, which can also follow the
        National format. Active phone numbers are in service.

        Assigning or Unassigning an alternate phone number to a person requires a full administrator auth token with
        a scope of spark-admin:telephony_config_write.

        :param person_id: Unique identifier of the person.
        :type person_id: str
        :param update: Update to apply
        :type update: :class:`UpdatePersonNumbers`
        :param org_id: organization to work on
        :type org_id: str
        """
        url = self.session.ep(f'telephony/config/people/{person_id}/numbers')
        params = org_id and {'orgId': org_id} or None
        body = update.json()
        await self.put(url=url, params=params, data=body)


class AsAuthCodesApi(AsPersonSettingsApiChild):
    """
    API for person's outgoing permission authorization codes
    """
    feature = 'outgoingPermission/authorizationCodes'

    async def read(self, person_id: str, org_id: str = None) -> list[AuthCode]:
        """
        Retrieve Authorization codes for a Workspace.

        Authorization codes are used to bypass permissions.

        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or
        a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param person_id: Unique identifier for the workspace.
        :type person_id: str
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: list of authorization codes
        :rtype: list of :class:`AuthCode`
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url, params=params)
        return parse_obj_as(list[AuthCode], data['authorizationCodes'])

    async def delete_codes(self, person_id: str, access_codes: list[Union[str, AuthCode]], org_id: str = None):
        """
        Modify Authorization codes for a workspace.

        Authorization codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a
        user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param person_id: Unique identifier for the workspace.
        :type person_id: str
        :param access_codes: authorization codes to remove
        :type access_codes: list[str]
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        body = {'deleteCodes': [ac.code if isinstance(ac, AuthCode) else ac
                                for ac in access_codes]}
        await self.put(url, params=params, json=body)

    async def create(self, person_id: str, code: str, description: str, org_id: str = None):
        """
        Modify Authorization codes for a workspace.

        Authorization codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a
        user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param person_id: Unique identifier for the workspace.
        :type person_id: str
        :param code: Indicates an authorization code.
        :type code: str
        :param description: Indicates the description of the authorization code.
        :type description: str
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        body = {'code': code,
                'description': description}
        await self.post(url, params=params, json=body)


class AsTransferNumbersApi(AsPersonSettingsApiChild):
    """
    API for outgoing permission auto transfer numbers
    """
    feature = 'outgoingPermission/autoTransferNumbers'

    async def read(self, person_id: str, org_id: str = None) -> AutoTransferNumbers:
        """
        Retrieve Transfer Numbers Settings for a Workspace.

        When calling a specific call type, this workspace will be automatically transferred to another number. The
        person assigned the Auto Transfer Number can then approve the call and send it through or reject the call
        type. You can add up to 3 numbers.

        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or
        a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param person_id: Unique identifier for the workspace.
        :type person_id: str
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: auto transfer numbers
        :rtype: :class:`AutoTransferNumbers`
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url, params=params)
        return AutoTransferNumbers.parse_obj(data)

    async def configure(self, person_id: str, settings: AutoTransferNumbers, org_id: str = None):
        """
        Modify Transfer Numbers Settings for a Place.

        When calling a specific call type, this workspace will be automatically transferred to another number.
        The person assigned the Auto Transfer Number can then approve the call and send it through or reject the
        call type. You can add up to 3 numbers.

        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a
        user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param person_id: Unique identifier for the workspace.
        :type person_id: str
        :param settings: new auto transfer numbers
        :type settings: :class:`AutoTransferNumbers`
        :param org_id: Workspace is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        body = settings.json()
        await self.put(url, params=params, data=body)


class AsOutgoingPermissionsApi(AsPersonSettingsApiChild):
    """
    API for person's outgoing permissions settings

    also used for workspace and location outgoing permissions
    """
    #: Only available for workspaces and locations
    transfer_numbers: AsTransferNumbersApi
    #: Only available for workspaces
    auth_codes: AsAuthCodesApi

    feature = 'outgoingPermission'

    def __init__(self, *, session: AsRestSession,
                 workspaces: bool = False, locations: bool = False):
        super().__init__(session=session, workspaces=workspaces, locations=locations)
        if workspaces:
            # auto transfer numbers API seems to only exist for workspaces
            self.transfer_numbers = AsTransferNumbersApi(session=session,
                                                       workspaces=True)
            self.auth_codes = AsAuthCodesApi(session=session, workspaces=True)
        elif locations:
            self.transfer_numbers = AsTransferNumbersApi(session=session,
                                                       locations=True)
            self.auth_codes = None
        else:
            self.transfer_numbers = None
            self.auth_codes = None

    async def read(self, person_id: str, org_id: str = None) -> OutgoingPermissions:
        """
        Retrieve a Person's Outgoing Calling Permissions Settings

        You can change the outgoing calling permissions for a person if you want them to be different from your
        organization's default.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: outgoing permission settings for specific user
        :rtype: :class:`OutgoingPermissions`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return OutgoingPermissions.parse_obj(await self.get(ep, params=params))

    async def configure(self, person_id: str, settings: OutgoingPermissions, drop_call_types: set[str] = None,
                  org_id: str = None):
        """
        Configure a Person's Outgoing Calling Permissions Settings

        Turn on outgoing call settings for this person to override the calling settings from the location that are
        used by default.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: new setting to be applied
        :type settings: :class:`OutgoingPermissions`
        :param drop_call_types: set of call type names to be excluded from updates. Default is the set of call_types
            known to be not supported for updates
        :type drop_call_types: set[str]
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        await self.put(ep, params=params, data=settings.json(drop_call_types=drop_call_types))


class AsPersonForwardingApi(AsPersonSettingsApiChild):
    """
    API for person's call forwarding settings
    """

    feature = 'callForwarding'

    async def read(self, person_id: str, org_id: str = None) -> PersonForwardingSetting:
        """
        Retrieve a Person's Call Forwarding Settings

        Three types of call forwarding are supported:

        * Always – forwards all incoming calls to the destination you choose.

        * When busy – forwards all incoming calls to the destination you chose while the phone is in use or the person
          is busy.

        * When no answer – forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as power outage, failed Internet connection, or wiring problem

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their own settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: user's forwarding settings
        :rtype: PersonForwardingSetting
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return PersonForwardingSetting.parse_obj(await self.get(ep, params=params))

    async def configure(self, person_id: str, forwarding: PersonForwardingSetting, org_id: str = None):
        """
        Configure a Person's Call Forwarding Settings

        Three types of call forwarding are supported:

        * Always – forwards all incoming calls to the destination you choose.

        * When busy – forwards all incoming calls to the destination you chose while the phone is in use or the person
          is busy.

        * When no answer – forwarding only occurs when you are away or not answering your phone.

        In addition, the Business Continuity feature will send calls to a destination of your choice if your phone is
        not connected to the network for any reason, such as power outage, failed Internet connection, or wiring problem

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param forwarding: new forwarding settings
        :type forwarding: PersonForwardingSetting
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        # system_max_number_of_ring cannot be used in update
        data = forwarding.json(
            exclude={'call_forwarding':
                         {'no_answer':
                              {'system_max_number_of_rings': True}}})
        await self.put(ep, params=params, data=data)


class AsPrivacyApi(AsPersonSettingsApiChild):
    """
    API for person's call monitoring settings
    """

    feature = 'privacy'

    async def read(self, person_id: str, org_id: str = None) -> Privacy:
        """
        Get a person's Privacy Settings

        Get a person's privacy settings for the specified person id.

        The privacy feature enables the person's line to be monitored by others and determine if they can be reached
        by Auto Attendant services.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: privacy settings
        :rtype: :class:`Privacy`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return Privacy.parse_obj(data)

    async def configure(self, person_id: str, settings: Privacy, org_id: str = None):
        """
        Configure Call Waiting Settings for a Person

        Configure a Person's Call Waiting Settings

        With this feature, a person can place an active call on hold and answer an incoming call. When enabled,
        while you are on an active call, a tone alerts you of an incoming call and you can choose to answer or ignore
        the call.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: settings for update
        :type settings: :class:`Monitoring`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.loads(settings.json())
        if settings.monitoring_agents is not None:
            id_list = []
            for ma in settings.monitoring_agents:
                if isinstance(ma, str):
                    id_list.append(ma)
                else:
                    id_list.append(ma.agent_id)
            data['monitoringAgents'] = id_list
        await self.put(ep, params=params, json=data)


class AsPushToTalkApi(AsPersonSettingsApiChild):
    """
    API for person's PTT settings
    """

    feature = 'pushToTalk'

    async def read(self, person_id: str, org_id: str = None) -> PushToTalkSettings:
        """
        Read Push-to-Talk Settings for a Person
        Retrieve a Person's Push-to-Talk Settings

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: PTT settings for specific user
        :rtype: PushToTalkSettings
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return PushToTalkSettings.parse_obj(await self.get(ep, params=params))

    async def configure(self, person_id: str, settings: PushToTalkSettings, org_id: str = None):
        """
        Configure Push-to-Talk Settings for a Person

        Configure a Person's Push-to-Talk Settings

        Push-to-Talk allows the use of desk phones as either a one-way or two-way intercom that connects people in
        different parts of your organization.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: new setting to be applied. For members only the ID needs to be set
        :type settings: PushToTalkSettings
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        if settings.members:
            # for an update member is just a list of IDs
            body_settings = settings.copy(deep=True)
            members = [m.member_id if isinstance(m, MonitoredMember) else m
                       for m in settings.members]
            body_settings.members = members
        else:
            body_settings = settings
        body = body_settings.json(exclude_none=False,
                                  exclude_unset=True)
        await self.put(ep, params=params, data=body)


class AsReceptionistApi(AsPersonSettingsApiChild):
    """
    API for person's receptionist client settings
    """

    feature = 'reception'

    async def read(self, person_id: str, org_id: str = None) -> ReceptionistSettings:
        """
        Read Receptionist Client Settings for a Person

        Retrieve a Person's Receptionist Client Settings

        To help support the needs of your front-office personnel, you can set up people or workspaces as telephone
        attendants so that they can screen all incoming calls to certain numbers within your organization.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: receptionist client settings
        :rtype: :class:`ReceptionistSettings`
        """
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(ep, params=params)
        return ReceptionistSettings.parse_obj(data)

    async def configure(self, person_id: str, settings: ReceptionistSettings, org_id: str = None):
        """
        Modify Executive Assistant Settings for a Person

        Modify the executive assistant settings for the specified personId.

        People with the executive service enabled, can select from a pool of assistants who have been assigned the
        executive assistant service and who can answer or place calls on their behalf. Executive assistants can set
        the call forward destination and join or leave an executive's pool.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param settings: New receptionist client settings
        :type settings: :class:`ReceptionistSettings`
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        if settings.enabled is None:
            raise ValueError('enabled is a mandatory parameter for updates')
        if settings.monitored_members and not settings.enabled:
            raise ValueError('when setting members enabled has to be True')
        ep = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        data = json.loads(settings.json())
        if settings.monitored_members is not None:
            id_list = []
            for me in settings.monitored_members:
                if isinstance(me, str):
                    id_list.append(me)
                else:
                    id_list.append(me.member_id)
            data['monitoredMembers'] = id_list
        await self.put(ep, params=params, json=data)


class AsScheduleApi(AsApiChild, base='telephony/config/locations'):
    """
    Schedules API
    """

    def __init__(self, *, session: AsRestSession, base: ScheduleApiBase):
        super().__init__(session=session, base=base.value)
        if base == ScheduleApiBase.people:
            self.after_id = '/features/schedules'
        elif base == ScheduleApiBase.locations:
            self.after_id = '/schedules'
        else:
            raise ValueError('unexpected value for base')

    def _endpoint(self, *, obj_id: str, schedule_type: ScheduleTypeOrStr = None, schedule_id: str = None,
                  event_id: str = None):
        """
        location specific feature endpoint like v1/telephony/config/locations/{obj_id}/schedules/.... or
        v1/people/{obj_id}/features/schedules/....

        :meta private:
        :param obj_id: Unique identifier for the location or user
        :type obj_id: str
        :param schedule_type: type of schedule
        :type schedule_type: ScheduleType
        :param schedule_id: schedule id
        :type schedule_id: str
        :return: full endpoint
        :rtype: str
        """
        ep = self.ep(path=f'{obj_id}{self.after_id}')
        if schedule_type is not None:
            schedule_type = ScheduleType.type_or_str(schedule_type)
            ep = f'{ep}/{schedule_type.value}/{schedule_id}'
            if event_id is not None:
                event_id = event_id and f'/{event_id}' or ''
                ep = f'{ep}/events{event_id}'
        return ep

    def list_gen(self, obj_id: str, org_id: str = None, schedule_type: ScheduleType = None,
             name: str = None, **params) -> AsyncGenerator[Schedule, None, None]:
        """
        List of Schedules for a Person or location

        List schedules for a person or location in an organization.

        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week
        by defining one or more events. holidays schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param obj_id: Return the list of schedules for this location or user
        :type obj_id: str
        :param org_id: List schedules for this organization.
        :type org_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :param name: Only return schedules with the matching name.
        :return: yields schedules
        """
        url = self._endpoint(obj_id=obj_id)
        if schedule_type is not None:
            params['type'] = schedule_type.value
        if name is not None:
            params['name'] = name
        if org_id is not None:
            params['orgId'] = org_id

        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Schedule, params=params or None)

    async def list(self, obj_id: str, org_id: str = None, schedule_type: ScheduleType = None,
             name: str = None, **params) -> List[Schedule]:
        """
        List of Schedules for a Person or location

        List schedules for a person or location in an organization.

        Schedules are used to support calling features and can be defined at the location or person level.
        businessHours schedules allow you to apply specific call settings at different times of the day or week
        by defining one or more events. holidays schedules define exceptions to normal business hours by defining one
        or more events.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read.

        :param obj_id: Return the list of schedules for this location or user
        :type obj_id: str
        :param org_id: List schedules for this organization.
        :type org_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :param name: Only return schedules with the matching name.
        :return: yields schedules
        """
        url = self._endpoint(obj_id=obj_id)
        if schedule_type is not None:
            params['type'] = schedule_type.value
        if name is not None:
            params['name'] = name
        if org_id is not None:
            params['orgId'] = org_id

        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=Schedule, params=params or None)]

    async def details(self, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                org_id: str = None) -> Schedule:
        """
        Get Details for a Schedule

        Retrieve Schedule details.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Retrieving schedule details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param obj_id: Retrieve schedule details in this location or user
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Retrieve the schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Retrieve schedule details from this organization.
        :type org_id: str
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id)
        data = await self.get(url, params=params)
        result = Schedule.parse_obj(data)
        return result

    async def create(self, obj_id: str, schedule: Schedule, org_id: str = None) -> str:
        """
        Create a Schedule

        Create new Schedule for the given location.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Creating a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param obj_id: Create the schedule for this location or user
        :type obj_id: str
        :param schedule: Schedule to be created
        :type schedule: Schedule
        :param org_id: Create the schedule for this organization.
        :type org_id: str
        :return: ID of the newly created schedule.
        :rtype: str
        """
        schedule_data = schedule.create_update()
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id)
        data = await self.post(url, data=schedule_data, params=params)
        result = data['id']
        return result

    async def update(self, obj_id: str, schedule: Schedule, schedule_type: ScheduleTypeOrStr = None,
               schedule_id: str = None, org_id: str = None) -> str:
        """
        Update a Schedule

        Update the designated Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Updating a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        NOTE: The Schedule ID will change upon modification of the Schedule name

        :param obj_id: Location or user for  which this schedule exists
        :type obj_id: str
        :param schedule: data for the update
        :type schedule: Schedule
        :param schedule_type: Type of the schedule. Default: schedule_type from schedule
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Update schedule with the matching ID. Default: schedule_id from schedule
        :type schedule_id: str
        :param org_id: Update schedule from this organization.
        :type org_id: str
        :return: schedule id
        """
        schedule_type = schedule_type or schedule.schedule_type
        schedule_id = schedule_id or schedule.schedule_id
        schedule_data = schedule.create_update(update=True)
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id)
        data = await self.put(url, data=schedule_data, params=params)
        return data['id']

    async def delete_schedule(self, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                        org_id: str = None):
        """
        Delete a Schedule

        Delete the designated Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Deleting a schedule requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param obj_id: Location or user from which to delete a schedule.
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Delete the schedule with the matching ID.
        :type schedule_id: str
        :param org_id: Retrieve schedule details from this organization.
        :type org_id: str
        :return:
        """
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id)
        params = org_id and {'orgId': org_id} or None
        await self.delete(url, params=params)

    async def event_details(self, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                      event_id: str, org_id: str = None) -> Event:
        """
        Get Details for a Schedule Event

        Retrieve Schedule Event details.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Retrieving schedule event details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param obj_id: Retrieve schedule event details for this location or user
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Retrieve schedule event details for schedule with the matching ID.
        :type schedule_id: str
        :param event_id: Retrieve the schedule event with the matching schedule event ID.
        :type event_id: str
        :param org_id: Retrieve schedule event details from this organization.
        :type org_id: str
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id=event_id)
        data = await self.get(url, params=params)
        result = Event.parse_obj(data)
        return result

    async def event_create(self, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                     event: Event, org_id: str = None) -> str:
        """
        Create a Schedule Event

        Create new Event for the given location or user Schedule.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Creating a schedule event requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param obj_id: Create the schedule for this location.
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Create event for a given schedule ID.
        :type schedule_id: str
        :param event: event data
        :type event: Event
        :param org_id: Retrieve schedule event details from this organization.
        :type org_id: str
        :return: event id
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id='')
        data = event.json(exclude={'event_id'})
        data = await self.post(url, data=data, params=params)
        return data['id']

    async def event_update(self, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                     event: Event, event_id: str = None, org_id: str = None) -> str:
        """
        Update a Schedule Event

        Update the designated Schedule Event.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Updating a schedule event requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        NOTE: The Schedule Event ID will change upon modification of the Schedule event name.

        :param obj_id: Location or user for which this schedule event exists.
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Update schedule event with the matching schedule ID.
        :type schedule_id: str
        :param event: update settings
        :type event: Event
        :param event_id: Update the schedule event with the matching schedule event ID. Default: event id from event
        :type event_id: str
        :param org_id: Update schedule from this organization.
        :type org_id: str
        :return: event id; changed if name changed
        """
        event_id = event_id or event.event_id
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id=event_id)
        event_data = event.json(exclude={'event_id'})
        data = await self.put(url, data=event_data, params=params)
        return data['id']

    async def event_delete(self, obj_id: str, schedule_type: ScheduleTypeOrStr, schedule_id: str,
                     event_id: str, org_id: str = None):
        """
        Delete a Schedule Event

        Delete the designated Schedule Event.

        A time schedule establishes a set of times during the day or holidays in the year in which a feature, for
        example auto attendants, can perform a specific action.

        Deleting a schedule event requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param obj_id: Location or user from which to delete a schedule.
        :type obj_id: str
        :param schedule_type: Type of the schedule.
            businessHours - Business hours schedule type.
            holidays - Holidays schedule type.
        :type schedule_type: ScheduleTypeOrStr
        :param schedule_id: Delete schedule event with the matching schedule ID.
        :type schedule_id: str
        :param event_id: Delete the schedule event with the matching schedule event ID. Default: event id from event
        :type event_id: str
        :param org_id: Delete schedule from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(obj_id=obj_id, schedule_type=schedule_type, schedule_id=schedule_id,
                             event_id=event_id)
        await self.delete(url, params=params)


class AsVoicemailApi(AsPersonSettingsApiChild):
    """
    API for person's call voicemail settings
    """

    feature = 'voicemail'

    async def read(self, person_id: str, org_id: str = None) -> VoicemailSettings:
        """
        Read Voicemail Settings for a Person
        Retrieve a Person's Voicemail Settings

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, .wav, format.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not include
        the voicemail files.

        This API requires a full, user, or read-only administrator auth token with a scope of spark-admin:people_read
        or a user auth token with spark:people_read scope can be used by a person to read their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: user's voicemail settings
        :rtype: VoicemailSettings
        """
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        return VoicemailSettings.parse_obj(await self.get(url, params=params))

    async def configure(self, person_id: str, settings: VoicemailSettings, org_id: str = None):
        """
        Configure Voicemail Settings for a Person
        Configure a person's Voicemail Settings

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. Voicemail audio is sent in Waveform Audio File Format, .wav, format.

        Optionally, notifications can be sent to a mobile phone via text or email. These notifications will not
        include the voicemail files.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.
        :return:
        """
        # some settings can't be part of an update
        data = settings.json(exclude={'send_busy_calls': {'greeting_uploaded': True},
                                      'send_unanswered_calls': {'system_max_number_of_rings': True,
                                                                'greeting_uploaded': True},
                                      'voice_message_forwarding_enabled': True
                                      })
        url = self.f_ep(person_id=person_id)
        params = org_id and {'orgId': org_id} or None
        await self.put(url, data=data, params=params)

    async def _configure_greeting(self, *, person_id: str, content: Union[BufferedReader, str],
                            upload_as: str = None, org_id: str = None,
                            greeting_key: str):
        """
        handled greeting configuration

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :param greeting_key: 'uploadBusyGreeting' or 'uploadNoAnswerGreeting'
        """
        if isinstance(content, str):
            upload_as = os.path.basename(content)
            content = open(content, mode='rb')
            must_close = True
        else:
            must_close = False
            # an existing reader
            if not upload_as:
                raise ValueError('upload_as is required')
        encoder = MultipartEncoder(fields={'file': (upload_as, content, 'audio/wav')})
        ep = self.f_ep(person_id=person_id, path=f'actions/{greeting_key}/invoke')
        params = org_id and {'orgId': org_id} or None
        try:
            await self.post(ep, data=encoder, headers={'Content-Type': encoder.content_type},
                      params=params)
        finally:
            if must_close:
                content.close()

    def configure_busy_greeting(self, person_id: str, content: Union[BufferedReader, str],
                                upload_as: str = None, org_id: str = None):
        """
        Configure Busy Voicemail Greeting for a Person
        Configure a Person's Busy Voicemail Greeting by uploading a Waveform Audio File Format, .wav, encoded audio
        file.

        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        self._configure_greeting(person_id=person_id, content=content, upload_as=upload_as, org_id=org_id,
                                 greeting_key='uploadBusyGreeting')

    def configure_no_answer_greeting(self, person_id: str, content: Union[BufferedReader, str],
                                     upload_as: str = None, org_id: str = None):
        """
        Configure No Answer Voicemail Greeting for a Person
        Configure a Person's No Answer Voicemail Greeting by uploading a Waveform Audio File Format, .wav, encoded
        audio file.

        Your request will need to be a multipart/form-data request rather than JSON, using the audio/wav Content-Type.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope or a user
        auth token with spark:people_write scope can be used by a person to update their settings.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param content: the file to be uploaded, can be a path to a file or a buffered reader (opened file); if a
            reader referring to an open file is passed then make sure to open the file as binary b/c otherwise the
            content length might be calculated wrong
        :type content: Union[BufferedReader, str]
        :param upload_as: filename for the content. Only required if content is a reader; has to be a .wav file name.
        :type upload_as: str
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        self._configure_greeting(person_id=person_id, content=content, upload_as=upload_as, org_id=org_id,
                                 greeting_key='uploadNoAnswerGreeting')


class AsPersonSettingsApi(AsApiChild, base='people'):
    """
    API for all user level settings
    """

    #: agent caller id Api
    agent_caller_id: AsAgentCallerIdApi
    #: Person's Application Services Settings
    appservices: AsAppServicesApi
    #: Barge In Settings for a Person
    barge: AsBargeApi
    #: Do Not Disturb Settings for a Person
    dnd: AsDndApi
    #: Call Intercept Settings for a Person
    call_intercept: AsCallInterceptApi
    #: Call Recording Settings for a Person
    call_recording: AsCallRecordingApi
    #: Call Waiting Settings for a Person
    call_waiting: AsCallWaitingApi
    #: Caller ID Settings for a Person
    caller_id: AsCallerIdApi
    #: Person's Calling Behavior
    calling_behavior: AsCallingBehaviorApi
    #: Executive Assistant Settings for a Person
    exec_assistant: AsExecAssistantApi
    #: Forwarding Settings for a Person
    forwarding: AsPersonForwardingApi
    #: Hoteling Settings for a Person
    hoteling: AsHotelingApi
    #: Person's Monitoring Settings
    monitoring: AsMonitoringApi
    #: Phone Numbers for a Person
    numbers: AsNumbersApi
    #: Incoming Permission Settings for a Person
    permissions_in: AsIncomingPermissionsApi
    #: Person's Outgoing Calling Permissions Settings
    permissions_out: AsOutgoingPermissionsApi
    #: Person's Privacy Settings
    privacy: AsPrivacyApi
    #: Push-to-Talk Settings for a Person
    push_to_talk: AsPushToTalkApi
    #: Receptionist Client Settings for a Person
    receptionist: AsReceptionistApi
    #: Schedules for a Person
    schedules: AsScheduleApi
    #: Voicemail Settings for a Person
    voicemail: AsVoicemailApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.agent_caller_id = AsAgentCallerIdApi(session=session)
        self.appservices = AsAppServicesApi(session=session)
        self.barge = AsBargeApi(session=session)
        self.dnd = AsDndApi(session=session)
        self.call_intercept = AsCallInterceptApi(session=session)
        self.call_recording = AsCallRecordingApi(session=session)
        self.call_waiting = AsCallWaitingApi(session=session)
        self.calling_behavior = AsCallingBehaviorApi(session=session)
        self.caller_id = AsCallerIdApi(session=session)
        self.exec_assistant = AsExecAssistantApi(session=session)
        self.forwarding = AsPersonForwardingApi(session=session)
        self.hoteling = AsHotelingApi(session=session)
        self.monitoring = AsMonitoringApi(session=session)
        self.numbers = AsNumbersApi(session=session)
        self.permissions_in = AsIncomingPermissionsApi(session=session)
        self.permissions_out = AsOutgoingPermissionsApi(session=session)
        self.privacy = AsPrivacyApi(session=session)
        self.push_to_talk = AsPushToTalkApi(session=session)
        self.receptionist = AsReceptionistApi(session=session)
        self.schedules = AsScheduleApi(session=session, base=ScheduleApiBase.people)
        self.voicemail = AsVoicemailApi(session=session)

    async def reset_vm_pin(self, person_id: str, org_id: str = None):
        """
        Reset Voicemail PIN

        Reset a voicemail PIN for a person.

        The voicemail feature transfers callers to voicemail based on your settings. You can then retrieve voice
        messages via Voicemail. A voicemail PIN is used to retrieve your voicemail messages.

        This API requires a full or user administrator auth token with the spark-admin:people_write scope.

        :param person_id: Unique identifier for the person.
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners) may
            use this parameter as the default is the same organization as the token used to access API.
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{person_id}/features/voicemail/actions/resetPin/invoke')
        await self.post(url, params=params)

    async def devices(self, person_id: str, org_id: str = None) -> PersonDevicesResponse:
        """
        Get all devices for a person.

        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param person_id: Person to retrieve devices for
        :type person_id: str
        :param org_id: organization that person belongs to
        :type org_id: str
        :return: device info for user
        :rtype: PersonDevicesResponse
        """
        params = org_id and {'orgId': org_id} or None
        url = self.session.ep(f'telephony/config/people/{person_id}/devices')
        data = await self.get(url=url, params=params)
        return PersonDevicesResponse.parse_obj(data)


class AsReportsApi(AsApiChild, base='devices'):
    """
    Report templates are available for use with the Reports API.

    To access this endpoint, you must use an administrator token with the analytics:read_all scope. The authenticated
    user must be a read-only or full administrator of the organization to which the report belongs.

    To use this endpoint the organization needs to be licensed for Pro Pack for Control Hub.

    Reports available via Webex Control Hub may be generated and downloaded via the Reports API. To access this API,
    the authenticated user must be a read-only or full administrator of the organization to which the report belongs.

    """

    async def list_templates(self) -> list[ReportTemplate]:
        """
        List all the available report templates that can be generated.

        CSV (comma separated value) reports for Webex services are only supported for organizations based in the
        North American region. Organizations based in other regions will return blank CSV files for any Webex reports.

        :return: list of report templates
        :rtype: list[ReportTemplate]
        """
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "Template Attributes" is actually "items"
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "validations"/"validations" is actually "validations"
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "id" is actually "Id"
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "startDate", "endDate" not documented
        url = self.session.ep('report/templates')
        data = await self.get(url=url)
        result = parse_obj_as(list[ReportTemplate], data['items'])
        return result

    def list_gen(self, report_id: str = None, service: str = None, template_id: str = None, from_date: date = None,
             to_date: date = None) -> AsyncGenerator[Report, None, None]:
        """
        Lists all reports. Use query parameters to filter the response. The parameters are optional. However,
        from and to parameters should be provided together.

        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param report_id: List reports by ID.
        :param service: List reports which use this service.
        :param template_id: List reports with this report template ID.
        :param from_date: List reports that were created on or after this date.
        :param to_date: List reports that were created before this date.
        :return: yields :class:`Report` instances
        """
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "Report Attributes" is actually "items"
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   missing attribute: downloadDomain
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "id" is actually "Id"
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "scheduledFrom" is actually "scheduleFrom"

        params = {to_camel(k.split('_')[0] if k.endswith('date') else k): v for k, v in locals().items()
                  if k not in {'self', 'from_date', 'to_date'} and v is not None}
        if from_date:
            params['from'] = from_date.strftime('%Y-%m-%d')
        if to_date:
            params['to'] = to_date.strftime('%Y-%m-%d')

        url = self.session.ep('reports')
        return self.session.follow_pagination(url=url, params=params, model=Report, item_key='items')

    async def list(self, report_id: str = None, service: str = None, template_id: str = None, from_date: date = None,
             to_date: date = None) -> List[Report]:
        """
        Lists all reports. Use query parameters to filter the response. The parameters are optional. However,
        from and to parameters should be provided together.

        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param report_id: List reports by ID.
        :param service: List reports which use this service.
        :param template_id: List reports with this report template ID.
        :param from_date: List reports that were created on or after this date.
        :param to_date: List reports that were created before this date.
        :return: yields :class:`Report` instances
        """
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "Report Attributes" is actually "items"
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   missing attribute: downloadDomain
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "id" is actually "Id"
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "scheduledFrom" is actually "scheduleFrom"

        params = {to_camel(k.split('_')[0] if k.endswith('date') else k): v for k, v in locals().items()
                  if k not in {'self', 'from_date', 'to_date'} and v is not None}
        if from_date:
            params['from'] = from_date.strftime('%Y-%m-%d')
        if to_date:
            params['to'] = to_date.strftime('%Y-%m-%d')

        url = self.session.ep('reports')
        return [o async for o in self.session.follow_pagination(url=url, params=params, model=Report, item_key='items')]

    async def create(self, template_id: int, start_date: date = None, end_date: date = None, site_list: str = None) -> str:
        """
        Create a new report. For each templateId, there are a set of validation rules that need to be followed. For
        example, for templates belonging to Webex, the user needs to provide siteUrl. These validation rules can be
        retrieved via the Report Templates API.

        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param template_id: Unique ID representing valid report templates.
        :type template_id: int
        :param start_date: Data in the report will be from this date onwards.
        :type start_date: date
        :param end_date: Data in the report will be until this date.
        :type end_date: date
        :param site_list: Sites belonging to user's organization. This attribute is needed for site-based templates.
        :type site_list: str
        :return: The unique identifier for the report.
        :rtype: str
        """
        # TODO: https://developer.webex.com/docs/api/v1/reports/create-a-report, documentation bug
        #   result actually is something like: {'items': {'Id': 'Y2...lMg'}}
        body = {'templateId': template_id}
        if start_date:
            body['startDate'] = start_date.strftime('%Y-%m-%d')
        if end_date:
            body['endDate'] = end_date.strftime('%Y-%m-%d')
        if site_list:
            body['siteList'] = site_list
        url = self.session.ep('reports')
        data = await self.post(url=url, json=body)
        result = data['items']['Id']
        return result

    async def details(self, report_id: str) -> Report:
        """
        Shows details for a report, by report ID.

        Specify the report ID in the reportId parameter in the URI.

        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param report_id: The unique identifier for the report.
        :type report_id: str
        :return: report details
        :rtype: Report
        """
        # TODO: https://developer.webex.com/docs/api/v1/reports/create-a-report, documentation bug
        #   result actually is something like: {'items': [{'title': 'Engagement Report', 'service': 'Webex Calling',
        #   'startDate': '2021-12-14', 'endDate': '2022-01-13', 'siteList': '', 'created': '2022-01-14 11:16:59',
        #   'createdBy': 'Y2lz..GM', 'scheduleFrom': 'api', 'status': 'done', 'downloadDomain':
        #   'https://reportdownload-a.webex.com/',  'downloadURL':
        #   'https://reportdownload-a.webex.com/api?reportId=Y2lz3ZA',  'Id': 'Y23ZA'}], 'numberOfReports': 1}
        url = self.session.ep(f'reports/{report_id}')
        data = await self.get(url=url)
        result = Report.parse_obj(data['items'][0])
        return result

    async def delete(self, report_id: str):
        """
        Remove a report from the system.

        Specify the report ID in the reportId parameter in the URI

        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param report_id: The unique identifier for the report.
        :type report_id: str
        """
        url = self.session.ep(f'reports/{report_id}')
        await super().delete(url=url)

    async def download(self, url: str) -> List[dict]:
        """
        Download a report from the given URL and yield the rows as dicts

        :param url: download URL
        :type url: str
        :return: list of dicts (one per row)
        :rtype: list[dict]
        """
        headers = {'Authorization': f'Bearer {self.session.access_token}'}
        async with self.session.get(url=url, headers=headers) as r:
            r.raise_for_status()
            lines = [line.decode(encoding='utf-8-sig') async for line in r.content]
            reader = csv.DictReader(lines)
            return list(reader)

        


class AsRoomTabsApi(AsApiChild, base='room/tabs'):
    """
    A Room Tab represents a URL shortcut that is added as a persistent tab to a Webex room (space) tab row. Use this
    API to list tabs of any Webex room that you belong to. Room Tabs can also be updated to point to a different
    content URL, or deleted to remove the tab from the room.
    Just like in the Webex app, you must be a member of the room in order to list its Room Tabs.
    """

    def list_tabs_gen(self, room_id: str, **params) -> AsyncGenerator[RoomTab, None, None]:
        """
        Lists all Room Tabs of a room specified by the roomId query parameter.

        :param room_id: ID of the room for which to list room tabs.
        :type room_id: str
        """
        if room_id is not None:
            params['roomId'] = room_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=RoomTab, params=params)

    async def list_tabs(self, room_id: str, **params) -> List[RoomTab]:
        """
        Lists all Room Tabs of a room specified by the roomId query parameter.

        :param room_id: ID of the room for which to list room tabs.
        :type room_id: str
        """
        if room_id is not None:
            params['roomId'] = room_id
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=RoomTab, params=params)]

    async def create_tab(self, room_id: str, content_url: str, display_name: str) -> RoomTab:
        """
        Add a tab with a specified URL to a room.

        :param room_id: A unique identifier for the room.
        :type room_id: str
        :param content_url: URL of the Room Tab. Must use https protocol.
        :type content_url: str
        :param display_name: User-friendly name for the room tab.
        :type display_name: str
        """
        body = {}
        if room_id is not None:
            body['roomId'] = room_id
        if content_url is not None:
            body['contentUrl'] = content_url
        if display_name is not None:
            body['displayName'] = display_name
        url = self.ep()
        data = await super().post(url=url, json=body)
        return RoomTab.parse_obj(data)

    async def tab_details(self, tab_id: str) -> RoomTab:
        """
        Get details for a Room Tab with the specified room tab ID.

        :param tab_id: The unique identifier for the Room Tab.
        :type tab_id: str
        """
        url = self.ep(f'{tab_id}')
        data = await super().get(url=url)
        return RoomTab.parse_obj(data)

    async def update_tab(self, tab_id: str, room_id: str, content_url: str, display_name: str) -> RoomTab:
        """
        Updates the content URL of the specified Room Tab ID.

        :param tab_id: The unique identifier for the Room Tab.
        :type tab_id: str
        :param room_id: ID of the room that contains the room tab in question.
        :type room_id: str
        :param content_url: Content URL of the Room Tab. URL must use https protocol.
        :type content_url: str
        :param display_name: User-friendly name for the room tab.
        :type display_name: str
        """
        body = {}
        if room_id is not None:
            body['roomId'] = room_id
        if content_url is not None:
            body['contentUrl'] = content_url
        if display_name is not None:
            body['displayName'] = display_name
        url = self.ep(f'{tab_id}')
        data = await super().put(url=url, json=body)
        return RoomTab.parse_obj(data)

    async def delete_tab(self, tab_id: str):
        """
        Deletes a Room Tab with the specified ID.

        :param tab_id: The unique identifier for the Room Tab to delete.
        :type tab_id: str
        """
        url = self.ep(f'{tab_id}')
        await super().delete(url=url)
        return


class AsRoomsApi(AsApiChild, base='rooms'):
    """
    Rooms are virtual meeting places where people post messages and collaborate to get work done. This API is used to
    manage the rooms themselves. Rooms are created and deleted with this API. You can also update a room to change
    its title, for example.
    To create a team room, specify the a teamId in the POST payload. Note that once a room is added to a team,
    it cannot be moved. To learn more about managing teams, see the Teams API.
    To manage people in a room see the Memberships API.
    To post content see the Messages API.
    """

    def list_gen(self, team_id: str = None, type_: RoomType = None, org_public_spaces: bool = None,
             from_: datetime = None, to_: datetime = None, sort_by: str = None,
             **params) -> AsyncGenerator[Room, None, None]:
        """
        List rooms.
        The title of the room for 1:1 rooms will be the display name of the other person.
        By default, lists rooms to which the authenticated user belongs.
        Long result sets will be split into pages.
        Known Limitations:
        The underlying database does not support natural sorting by lastactivity and will only sort on limited set of
        results, which are pulled from the database in order of roomId. For users or bots in more than 3000 spaces
        this can result in anomalies such as spaces that have had recent activity not being returned in the results
        when sorting by lastacivity.

        :param team_id: List rooms associated with a team, by ID.
        :type team_id: str
        :param type_: List rooms by type.
            Possible values: direct, group
        :type type_: RoomType
        :param org_public_spaces: Shows the org's public spaces joined and unjoined. When set the result list is sorted
            by the madePublic timestamp.
        :type org_public_spaces: bool
        :param from_: Filters rooms, that were made public after this time. See madePublic timestamp
        :type from_: datetime
        :param to_: Filters rooms, that were made public before this time. See maePublic timestamp
        :type to_: datetime
        :param sort_by: Sort results.
            Possible values: id, lastactivity, created
        :type sort_by: str
        """
        if team_id is not None:
            params['teamId'] = team_id
        if type_ is not None:
            params['type'] = type_
        if sort_by is not None:
            params['sortBy'] = sort_by
        if org_public_spaces is not None:
            params['orgPublicSpaces'] = org_public_spaces
        if from_ is not None:
            params['from'] = dt_iso_str(from_)
        if to_ is not None:
            params['to'] = dt_iso_str(to_)
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Room, params=params)

    async def list(self, team_id: str = None, type_: RoomType = None, org_public_spaces: bool = None,
             from_: datetime = None, to_: datetime = None, sort_by: str = None,
             **params) -> List[Room]:
        """
        List rooms.
        The title of the room for 1:1 rooms will be the display name of the other person.
        By default, lists rooms to which the authenticated user belongs.
        Long result sets will be split into pages.
        Known Limitations:
        The underlying database does not support natural sorting by lastactivity and will only sort on limited set of
        results, which are pulled from the database in order of roomId. For users or bots in more than 3000 spaces
        this can result in anomalies such as spaces that have had recent activity not being returned in the results
        when sorting by lastacivity.

        :param team_id: List rooms associated with a team, by ID.
        :type team_id: str
        :param type_: List rooms by type.
            Possible values: direct, group
        :type type_: RoomType
        :param org_public_spaces: Shows the org's public spaces joined and unjoined. When set the result list is sorted
            by the madePublic timestamp.
        :type org_public_spaces: bool
        :param from_: Filters rooms, that were made public after this time. See madePublic timestamp
        :type from_: datetime
        :param to_: Filters rooms, that were made public before this time. See maePublic timestamp
        :type to_: datetime
        :param sort_by: Sort results.
            Possible values: id, lastactivity, created
        :type sort_by: str
        """
        if team_id is not None:
            params['teamId'] = team_id
        if type_ is not None:
            params['type'] = type_
        if sort_by is not None:
            params['sortBy'] = sort_by
        if org_public_spaces is not None:
            params['orgPublicSpaces'] = org_public_spaces
        if from_ is not None:
            params['from'] = dt_iso_str(from_)
        if to_ is not None:
            params['to'] = dt_iso_str(to_)
        url = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=Room, params=params)]

    async def create(self, title: str, team_id: str = None, classification_id: str = None, is_locked: bool = None,
               is_public: bool = None, description: str = None, is_announcement_only: bool = None) -> Room:
        """
        Creates a room. The authenticated user is automatically added as a member of the room. See the Memberships
        API to learn how to add more people to the room.
        To create a 1:1 room, use the Create Messages endpoint to send a message directly to another person by using
        the toPersonId or toPersonEmail parameters.
        Bots are not able to create and classify a room. A bot may update a space classification after a person of
        the same owning organization joined the space as the first human user.
        A space can only be put into announcement mode when it is locked.

        :param title: A user-friendly name for the room.
        :type title: str
        :param team_id: The ID for the team with which this room is associated.
        :type team_id: str
        :param classification_id: The classificationId for the room.
        :type classification_id: str
        :param is_locked: Set the space as locked/moderated and the creator becomes a moderator
        :type is_locked: bool
        :param is_public: The room is public and therefore discoverable within the org. Anyone can find and join that
            room. When true the description must be filled in.
        :type is_public: bool
        :param description: The description of the space.
        :type description: str
        :param is_announcement_only: Sets the space into announcement Mode.
        :type is_announcement_only: bool
        """
        body = {}
        if title is not None:
            body['title'] = title
        if team_id is not None:
            body['teamId'] = team_id
        if classification_id is not None:
            body['classificationId'] = classification_id
        if is_locked is not None:
            body['isLocked'] = is_locked
        if is_public is not None:
            body['isPublic'] = is_public
        if description is not None:
            body['description'] = description
        if is_announcement_only is not None:
            body['isAnnouncementOnly'] = is_announcement_only
        url = self.ep()
        data = await super().post(url=url, json=body)
        return Room.parse_obj(data)

    async def details(self, room_id: str) -> Room:
        """
        Shows details for a room, by ID.
        The title of the room for 1:1 rooms will be the display name of the other person.
        Specify the room ID in the roomId parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        """
        url = self.ep(f'{room_id}')
        data = await super().get(url=url)
        return Room.parse_obj(data)

    async def meeting_details(self, room_id: str) -> GetRoomMeetingDetailsResponse:
        """
        Shows Webex meeting details for a room such as the SIP address, meeting URL, toll-free and toll dial-in numbers.
        Specify the room ID in the roomId parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        """
        url = self.ep(f'{room_id}/meetingInfo')
        data = await super().get(url=url)
        return GetRoomMeetingDetailsResponse.parse_obj(data)

    async def update(self, update: Room) -> Room:
        """
        Updates details for a room
        A space can only be put into announcement mode when it is locked.

        :update: update to apply. ID and title have to be set. Only can update:

            * title: str: A user-friendly name for the room.
            * classification_id: str: The classificationId for the room.
            * team_id: str: The teamId to which this space should be assigned. Only unowned spaces can be assigned
              to a team. Assignment between teams is unsupported.
            * is_locked: bool: Set the space as locked/moderated and the creator becomes a moderator
            * is_announcement_only: bool: Sets the space into announcement mode or clears the anouncement Mode (false)
            * is_read_only: bool: A compliance officer can set a direct room as read-only, which will disallow any
              new information exchanges in this space, while maintaining historical data.
        """
        update: Room
        data = update.json(include={'title', 'classification_id', 'team_id', 'is_locked', 'is_announcement_only',
                                    'is_read_only'})
        if update.id is None:
            raise ValueError('ID has to be set')
        url = self.ep(f'{update.id}')
        data = await super().put(url=url, data=data)
        return Room.parse_obj(data)

    async def delete(self, room_id: str):
        """
        Deletes a room, by ID. Deleted rooms cannot be recovered.
        As a security measure to prevent accidental deletion, when a non moderator deletes the room they are removed
        from the room instead.
        Deleting a room that is part of a team will archive the room instead.
        Specify the room ID in the roomId parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        """
        url = self.ep(f'{room_id}')
        await super().delete(url=url)
        return


class AsTeamMembershipsApi(AsApiChild, base='team/memberships'):
    """
    Team Memberships represent a person's relationship to a team. Use this API to list members of any team that you're
    in or create memberships to invite someone to a team. Team memberships can also be updated to make someone a
    moderator or deleted to remove them from the team.
    Just like in the Webex app, you must be a member of the team in order to list its memberships or invite people.
    """

    def list_gen(self, team_id: str, **params) -> AsyncGenerator[TeamMembership, None, None]:
        """
        Lists all team memberships for a given team, specified by the teamId query parameter.
        Use query parameters to filter the response.

        :param team_id: List memberships for a team, by ID.
        :type team_id: str
        """
        if team_id is not None:
            params['teamId'] = team_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=TeamMembership, params=params)

    async def list(self, team_id: str, **params) -> List[TeamMembership]:
        """
        Lists all team memberships for a given team, specified by the teamId query parameter.
        Use query parameters to filter the response.

        :param team_id: List memberships for a team, by ID.
        :type team_id: str
        """
        if team_id is not None:
            params['teamId'] = team_id
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=TeamMembership, params=params)]

    async def create(self, team_id: str, person_id: str = None, person_email: str = None,
               is_moderator: bool = None) -> TeamMembership:
        """
        Add someone to a team by Person ID or email address, optionally making them a moderator.

        :param team_id: The team ID.
        :type team_id: str
        :param person_id: The person ID.
        :type person_id: str
        :param person_email: The email address of the person.
        :type person_email: str
        :param is_moderator: Whether or not the participant is a team moderator.
        :type is_moderator: bool
        """
        body = {}
        if team_id is not None:
            body['teamId'] = team_id
        if person_id is not None:
            body['personId'] = person_id
        if person_email is not None:
            body['personEmail'] = person_email
        if is_moderator is not None:
            body['isModerator'] = is_moderator
        url = self.ep()
        data = await super().post(url=url, json=body)
        return TeamMembership.parse_obj(data)

    async def details(self, membership_id: str) -> TeamMembership:
        """
        Shows details for a team membership, by ID.
        Specify the team membership ID in the membershipId URI parameter.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str
        """
        url = self.ep(f'{membership_id}')
        data = await super().get(url=url)
        return TeamMembership.parse_obj(data)

    async def membership(self, membership_id: str, is_moderator: bool) -> TeamMembership:
        """
        Updates a team membership, by ID.
        Specify the team membership ID in the membershipId URI parameter.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str
        :param is_moderator: Whether or not the participant is a team moderator.
        :type is_moderator: bool
        """
        body = {'isModerator': is_moderator}
        url = self.ep(f'{membership_id}')
        data = await super().put(url=url, json=body)
        return TeamMembership.parse_obj(data)

    async def delete(self, membership_id: str):
        """
        Deletes a team membership, by ID.
        Specify the team membership ID in the membershipId URI parameter.
        The team membership for the last moderator of a team may not be deleted; promote another user to team moderator
        first.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str
        """
        url = self.ep(f'{membership_id}')
        await super().delete(url=url)
        return


class AsTeamsApi(AsApiChild, base='teams'):
    """
    Teams are groups of people with a set of rooms that are visible to all members of that team. This API is used to
    manage the teams themselves. Teams are created and deleted with this API. You can also update a team to change its
    name, for example.
    To manage people in a team see the Team Memberships API.
    To manage team rooms see the Rooms API.
    """

    def list_gen(self) -> AsyncGenerator[Team, None, None]:
        """
        Lists teams to which the authenticated user belongs.
        """
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Team)

    async def list(self) -> List[Team]:
        """
        Lists teams to which the authenticated user belongs.
        """
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=Team)]

    async def create(self, name: str) -> Team:
        """
        Creates a team.
        The authenticated user is automatically added as a member of the team. See the Team Memberships API to learn
        how to add more people to the team.

        :param name: A user-friendly name for the team.
        :type name: str
        """
        body = {}
        if name is not None:
            body['name'] = name
        url = self.ep()
        data = await super().post(url=url, json=body)
        return Team.parse_obj(data)

    async def details(self, team_id: str) -> Team:
        """
        Shows details for a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        """
        url = self.ep(f'{team_id}')
        data = await super().get(url=url)
        return Team.parse_obj(data)

    async def update(self, team_id: str, name: str) -> Team:
        """
        Updates details for a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        :param name: A user-friendly name for the team.
        :type name: str
        """
        body = {'name': name}
        url = self.ep(f'{team_id}')
        data = await super().put(url=url, json=body)
        return Team.parse_obj(data)

    async def delete(self, team_id: str):
        """
        Deletes a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        """
        url = self.ep(f'{team_id}')
        await super().delete(url=url)
        return


class AsAccessCodesApi(AsApiChild, base='telephony/config/locations'):
    """
    Access codes API
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific feature endpoint like
        /v1/telephony/config/locations/{locationId}/outgoingPermission/accessCodes}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/outgoingPermission/accessCodes{path}')
        return ep

    async def read(self, location_id: str, org_id: str = None) -> list[AuthCode]:
        """
        Get Location Access Code

        Retrieve access codes details for a customer location.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Retrieving access codes details requires a full, user or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.


        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        :return: list of :class:`wxc_sdk.common.CallPark`
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        data = await self.get(url, params=params)
        return parse_obj_as(list[AuthCode], data['accessCodes'])

    async def create(self, location_id: str, access_codes: list[AuthCode], org_id: str = None) -> list[AuthCode]:
        """
        Create access code in location

        :param location_id: Add new access code for this location.
        :type location_id: str
        :param access_codes: Access code details
        :type access_codes: list of :class:`wxc_sdk.common.AuthCode`
        :param org_id: Add new access code for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = {'accessCodes': [json.loads(ac.json()) for ac in access_codes]}
        await self.post(url, json=body, params=params)

    async def delete_codes(self, location_id: str, access_codes: list[Union[str, AuthCode]],
                     org_id: str = None) -> list[AuthCode]:
        """
        Delete Access Code Location

        Deletes the access code details for a particular location for a customer.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Modifying the access code location details requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Deletes the access code details for this location.
        :type location_id: str
        :param access_codes: access codes to delete
        :type access_codes: list of :class:`wxc_sdk.common.AuthCode` or str
        :param org_id: Delete access codes from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = {'deleteCodes': [ac.code if isinstance(ac, AuthCode) else ac
                                for ac in access_codes]}
        await self.put(url, json=body, params=params)


class AsForwardingApi:
    """
    API for forwarding settings on call queues, hunt groups, and auto attendants
    """

    def __init__(self, session: AsRestSession, feature_selector: FeatureSelector):
        self._session = session
        self._feature = feature_selector

    def _endpoint(self, location_id: str, feature_id: str, path: str = None):
        """

        :meta private:
        :param location_id:
        :param feature_id:
        :param path:
        :return:
        """
        path = path and f'/{path}' or ''
        ep = self._session.ep(path=f'telephony/config/locations/{location_id}/{self._feature.value}/'
                                   f'{feature_id}/callForwarding{path}')
        return ep

    async def settings(self, location_id: str, feature_id: str, org_id: str = None) -> CallForwarding:
        """
        Retrieve Call Forwarding settings for the designated feature including the list of call
        forwarding rules.

        :param location_id: Location in which this feature exists.
        :type location_id: str
        :param feature_id: Retrieve the call forwarding settings for this entity
        :type feature_id: str
        :param org_id: Retrieve call forwarding settings from this organization.
        :type org_id: str
        :return: call forwarding settings
        :rtype: class:`CallForwarding`
        """
        params = org_id and {'orgId': org_id} or {}
        url = self._endpoint(location_id=location_id, feature_id=feature_id)
        data = await self._session.rest_get(url=url, params=params)
        result = CallForwarding.parse_obj(data['callForwarding'])
        return result

    async def update(self, location_id: str, feature_id: str,
               forwarding: CallForwarding, org_id: str = None):
        """
        Update Call Forwarding Settings for a feature

        Update Call Forwarding settings for the designated feature.

        Updating call forwarding settings for a feature requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this feature exists.
        :type location_id: str
        :param feature_id: Update call forwarding settings for this feature.
        :type feature_id: str
        :param forwarding: Forwarding settings
        :type forwarding: :class:`CallForwarding`
        :param org_id: Update feature forwarding settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or {}
        url = self._endpoint(location_id=location_id, feature_id=feature_id)
        body = forwarding.dict()

        # update only has 'id' and 'enabled' in rules
        # determine names of ForwardingRule fields to remove
        to_pop = [field
                  for field in ForwardingRule.__fields__
                  if field not in {'id', 'enabled'}]
        for rule in body['rules']:
            rule: Dict
            for field in to_pop:
                rule.pop(field, None)
        body = {'callForwarding': body}
        await self._session.rest_put(url=url, json=body, params=params)

    async def create_call_forwarding_rule(self, location_id: str, feature_id: str,
                                    forwarding_rule: ForwardingRuleDetails, org_id: str = None) -> str:
        """
        Create a Selective Call Forwarding Rule feature

        A selective call forwarding rule for feature to be forwarded or not
        forwarded to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available feature's call
        forwarding settings.
        :param location_id: Location in which the call queue exists.
        :type location_id: str
        :param feature_id: Create the rule for this feature
        :type feature_id: str
        :param forwarding_rule: details of rule to be created
        :type forwarding_rule: :class:`ForwardingRuleDetails`
        :param org_id: Create the feature forwarding rule for this organization.
        :type org_id: str
        :return: forwarding rule id
        :rtype; str
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path='selectiveRules')
        body = forwarding_rule.dict()
        params = org_id and {'orgId': org_id} or None
        data = await self._session.rest_post(url=url, json=body, params=params)
        return data['id']

    async def call_forwarding_rule(self, location_id: str, feature_id: str, rule_id: str,
                             org_id: str = None) -> ForwardingRuleDetails:
        """
        Retrieve a Selective Call Forwarding Rule's settings for the designated Call Queue.

        A selective call forwarding rule for feature allows calls to be forwarded or not forwarded
        to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the feature's call
        forwarding settings.
        :param location_id: Location in which the feature exists.
        :type location_id: stre
        :param feature_id: Retrieve setting for a rule for this feature.
        :type feature_id: str
        :param rule_id: feature rule you are retrieving settings for.
        :type rule_id: str
        :param org_id: Retrieve feature forwarding settings from this organization.
        :type org_id: str
        :return: call forwarding rule details
        :rtype: :class:`ForwardingRuleDetails`
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules/{rule_id}')
        params = org_id and {'orgId': org_id} or None
        data = await self._session.rest_get(url=url, params=params)
        result = ForwardingRuleDetails.parse_obj(data)
        return result

    async def update_call_forwarding_rule(self, location_id: str, feature_id: str, rule_id: str,
                                    forwarding_rule: ForwardingRuleDetails, org_id: str = None) -> str:
        """
        Update a Selective Call Forwarding Rule's settings for the designated feature.

        A selective call forwarding rule for feature allows calls to be forwarded or not forwarded
        to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the feature's call
        forwarding settings.

        NOTE: The Call Forwarding Rule ID will change upon modification of the Call Forwarding Rule name.

        :param location_id: Location in which the feature exists.
        :type location_id: str
        :param feature_id: Update settings for a rule for this feature.
        :type feature_id: str
        :param rule_id: feature you are updating settings for.
        :type rule_id: str
        :param forwarding_rule: forwarding rule details for update
        :type forwarding_rule: :class:`ForwardingRuleDetails`
        :param org_id: Update feature rule settings for this organization.
        :type org_id: str
        :return: new call forwarding rule id
        :rtype: str
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules/{rule_id}')
        params = org_id and {'orgId': org_id} or None
        body = forwarding_rule.dict()
        data = await self._session.rest_put(url=url, params=params, json=body)
        return data['id']

    async def delete_call_forwarding_rule(self, location_id: str, feature_id: str, rule_id: str, org_id: str = None):
        """
        Delete a Selective Call Forwarding Rule for the designated feature.

        A selective call forwarding rule for a feature allows calls to be forwarded or not forwarded
        to the designated number, based on the defined criteria.

        Note that the list of existing call forward rules is available in the feature's call
        forwarding
        settings.
        """
        url = self._endpoint(location_id=location_id, feature_id=feature_id, path=f'selectiveRules/{rule_id}')
        params = org_id and {'orgId': org_id} or None
        await self._session.delete(url=url, params=params)


class AsAutoAttendantApi(AsApiChild, base='telephony/config/autoAttendants'):
    """
    Auto attendant API
    """
    forwarding: AsForwardingApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.forwarding = AsForwardingApi(session=session, feature_selector=FeatureSelector.auto_attendants)

    def _endpoint(self, *, location_id: str = None, auto_attendant_id: str = None) -> str:
        """
        auto attendant specific feature endpoint like /v1/telephony/config/locations/{locationId}/autoAttendants/{
        auto_attendant_id}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param auto_attendant_id: auto attendant id
        :type auto_attendant_id: str
        :return: full endpoint
        :rtype: str
        """
        if location_id is None:
            return self.session.ep('telephony/config/autoAttendants')
        else:
            ep = self.session.ep(f'telephony/config/locations/{location_id}/autoAttendants')
            if auto_attendant_id:
                ep = f'{ep}/{auto_attendant_id}'
            return ep

    def list_gen(self, org_id: str = None, location_id: str = None, name: str = None,
             phone_number: str = None, **params) -> AsyncGenerator[AutoAttendant, None, None]:
        """
        Read the List of Auto Attendants
        List all Auto Attendants for the organization.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List auto attendants for this organization.
        :type org_id: str
        :param location_id: Return the list of auto attendants for this location.
        :type location_id: str
        :param name: Only return auto attendants with the matching name.
        :type name: str
        :param phone_number: Only return auto attendants with the matching phone number.
        :type phone_number: str
        :return: yields :class:`AutoAttendant` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=AutoAttendant, params=params, item_key='autoAttendants')

    async def list(self, org_id: str = None, location_id: str = None, name: str = None,
             phone_number: str = None, **params) -> List[AutoAttendant]:
        """
        Read the List of Auto Attendants
        List all Auto Attendants for the organization.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List auto attendants for this organization.
        :type org_id: str
        :param location_id: Return the list of auto attendants for this location.
        :type location_id: str
        :param name: Only return auto attendants with the matching name.
        :type name: str
        :param phone_number: Only return auto attendants with the matching phone number.
        :type phone_number: str
        :return: yields :class:`AutoAttendant` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=AutoAttendant, params=params, item_key='autoAttendants')]

    async def by_name(self, name: str, location_id: str = None, org_id: str = None) -> Optional[AutoAttendant]:
        """
        Get auto attendant info by name

        :param location_id:
        :param name:
        :param org_id:
        :return:
        """
        return next((hg for hg in await self.list(name=name, location_id=location_id, org_id=org_id)
                     if hg.name == name), None)

    async def details(self, location_id: str, auto_attendant_id: str, org_id: str = None) -> AutoAttendant:
        """
        Get Details for an Auto Attendant
        Retrieve an Auto Attendant details.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Retrieving an auto attendant details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve an auto attendant details in this location.
        :type location_id: str
        :param auto_attendant_id: Retrieve the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Retrieve auto attendant details from this organization.
        :type org_id: str
        :return: auto attendant details
        :rtype: :class:`AutoAttendant`
        """
        url = self._endpoint(location_id=location_id, auto_attendant_id=auto_attendant_id)
        params = org_id and {'orgId': org_id} or None
        return AutoAttendant.parse_obj(await self.get(url, params=params))

    async def create(self, location_id: str, settings: AutoAttendant, org_id: str = None) -> str:
        """
        Create an Auto Attendant
        Create new Auto Attendant for the given location.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Creating an auto attendant requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Create the auto attendant for this location.
        :type location_id: str
        :param settings: auto attendant settings for new auto attendant
        :type settings: :class:`AutoAttendant`
        :param org_id: Create the auto attendant for this organization.
        :type org_id: str
        :return: ID of the newly created auto attendant.
        :rtype: str
        """
        data = settings.create_or_update()
        url = self._endpoint(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.post(url, data=data, params=params)
        return data['id']

    async def update(self, location_id: str, auto_attendant_id: str, settings: AutoAttendant, org_id: str = None):
        """
        Update an Auto Attendant
        Update the designated Auto Attendant.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Updating an auto attendant requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this auto attendant exists.
        :type location_id: str
        :param auto_attendant_id: Update an auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param settings: auto attendant settings for the update
        :type settings: :class:`AutoAttendant`
        :param org_id: Create the auto attendant for this organization.
        :type org_id: str
        """
        data = settings.create_or_update()
        url = self._endpoint(location_id=location_id, auto_attendant_id=auto_attendant_id)
        params = org_id and {'orgId': org_id} or None
        await self.put(url, data=data, params=params)

    async def delete_auto_attendant(self, location_id: str, auto_attendant_id: str, org_id: str = None):
        """
        elete the designated Auto Attendant.

        Auto attendants play customized prompts and provide callers with menu options for routing their calls through
        your system.

        Deleting an auto attendant requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete an auto attendant.
        :type location_id: str
        :param auto_attendant_id: Delete the auto attendant with the matching ID.
        :type auto_attendant_id: str
        :param org_id: Delete the auto attendant from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, auto_attendant_id=auto_attendant_id)
        params = org_id and {'orgId': org_id} or None
        await self.delete(url, params=params)


class AsCallParkApi(AsApiChild, base='telephony/config/callParks'):
    """
    Call Park API
    """

    def _endpoint(self, *, location_id: str, callpark_id: str = None, path: str = None) -> str:
        """
        call park specific feature endpoint like /v1/telephony/config/locations/{locationId}/callParks/{callpark_id}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param callpark_id: call park id
        :type callpark_id: str
        :param path: addtl. path
        :type path: str
        :return: full endpoint
        :rtype: str
        """
        call_park_id = callpark_id and f'/{callpark_id}' or ''
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/callParks{call_park_id}{path}')
        return ep

    def list_gen(self, location_id: str, order: Literal['ASC', 'DSC'] = None, name: str = None,
             org_id: str = None, **params) -> AsyncGenerator[CallPark, None, None]:
        """
        Read the List of Call Parks

        List all Call Parks for the organization.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Return the list of call parks for this location.
        :type location_id: str
        :param order: Sort the list of call parks by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call parks that contains the given name. The maximum length is 80.
        :type name: str
        :param org_id: List call parks for this organization.
        :type org_id: str
        :return: yields :class:`CallPark` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i > 1 and v is not None and k != 'params')
        url = self._endpoint(location_id=location_id)
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CallPark, params=params, item_key='callParks')

    async def list(self, location_id: str, order: Literal['ASC', 'DSC'] = None, name: str = None,
             org_id: str = None, **params) -> List[CallPark]:
        """
        Read the List of Call Parks

        List all Call Parks for the organization.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Return the list of call parks for this location.
        :type location_id: str
        :param order: Sort the list of call parks by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call parks that contains the given name. The maximum length is 80.
        :type name: str
        :param org_id: List call parks for this organization.
        :type org_id: str
        :return: yields :class:`CallPark` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i > 1 and v is not None and k != 'params')
        url = self._endpoint(location_id=location_id)
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=CallPark, params=params, item_key='callParks')]

    async def create(self, location_id: str, settings: CallPark, org_id: str = None) -> str:
        """
        Create a Call Park

        Create new Call Parks for the given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Creating a call park requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Create the call park for this location.
        :type location_id: str
        :param settings: settings for new call park
        :type settings: :class:`CallPark`
        :param org_id: Create the call park for this organization.
        :return: ID of the newly created call park.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = settings.create_or_update()
        data = await self.post(url, data=body, params=params)
        return data['id']

    async def delete_callpark(self, location_id: str, callpark_id: str, org_id: str = None):
        """
        Delete a Call Park

        Delete the designated Call Park.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Deleting a call park requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Location from which to delete a call park.
        :type location_id: str
        :param callpark_id: Delete the call park with the matching ID.
        :type callpark_id: str
        :param org_id: Delete the call park from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, callpark_id=callpark_id)
        params = org_id and {'orgId': org_id} or None
        await self.delete(url, params=params)

    async def details(self, location_id: str, callpark_id: str, org_id: str = None) -> CallPark:
        """
        Get Details for a Call Park

        Retrieve Call Park details.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving call park details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: Retrieve settings for a call park in this location.
        :type location_id: str
        :param callpark_id: Retrieve settings for a call park with the matching ID.
        :type callpark_id: str
        :param org_id: Retrieve call park settings from this organization.
        :type org_id: str
        :return: call park info
        :rtype: :class:`CallPark`
        """
        url = self._endpoint(location_id=location_id, callpark_id=callpark_id)
        params = org_id and {'orgId': org_id} or None
        return CallPark.parse_obj(await self.get(url, params=params))

    async def update(self, location_id: str, callpark_id: str, settings: CallPark, org_id: str = None) -> str:
        """
        Update a Call Park

        Update the designated Call Park.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Updating a call park requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Park ID will change upon modification of the Call Park name.

        :param location_id: RLocation in which this call park exists.
        :type location_id: str
        :param callpark_id: Update settings for a call park with the matching ID.
        :type callpark_id: str
        :param settings: updates
        :type settings: :class:`CallPark`
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, callpark_id=callpark_id)
        body = settings.create_or_update()
        data = await self.put(url, data=body, params=params)
        return data['id']

    def available_agents_gen(self, location_id: str, call_park_name: str = None, name: str = None, phone_number: str = None,
                         order: str = None, org_id: str = None) -> AsyncGenerator[PersonPlaceAgent, None, None]:
        """
        Get available agents from Call Parks
        Retrieve available agents from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available agents from call parks requires a full or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_park_name: Only return available agents from call parks with the matching name.
        :type call_park_name: str
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, number and extension.
            The maximum supported sort order value is 3.
        :type order: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :return: yields :class:`PersonPlaceCallPark` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableUsers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=PersonPlaceAgent, params=params, item_key='agents')

    async def available_agents(self, location_id: str, call_park_name: str = None, name: str = None, phone_number: str = None,
                         order: str = None, org_id: str = None) -> List[PersonPlaceAgent]:
        """
        Get available agents from Call Parks
        Retrieve available agents from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available agents from call parks requires a full or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_park_name: Only return available agents from call parks with the matching name.
        :type call_park_name: str
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, number and extension.
            The maximum supported sort order value is 3.
        :type order: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :return: yields :class:`PersonPlaceCallPark` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableUsers')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=PersonPlaceAgent, params=params, item_key='agents')]

    def available_recalls_gen(self, location_id: str, name: str = None, order: str = None,
                          org_id: str = None) -> AsyncGenerator[AvailableRecallHuntGroup, None, None]:
        """
        Get available recall hunt groups from Call Parks

        Retrieve available recall hunt groups from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available recall hunt groups from call parks requires a full or read-only administrator auth
        token with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available recall hunt groups for this location.
        :type location_id: str
        :param name: Only return available recall hunt groups with the matching name.
        :type name: str
        :param order: Order the available recall hunt groups according to the designated fields. Available sort
            fields: lname.
        :param order: str
        :param org_id: Return the available recall hunt groups for this organization.
        :type org_id: str
        :return: yields :class:`AvailableRecallHuntGroup` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableRecallHuntGroups')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=AvailableRecallHuntGroup,
                                              params=params, item_key='huntGroups')

    async def available_recalls(self, location_id: str, name: str = None, order: str = None,
                          org_id: str = None) -> List[AvailableRecallHuntGroup]:
        """
        Get available recall hunt groups from Call Parks

        Retrieve available recall hunt groups from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving available recall hunt groups from call parks requires a full or read-only administrator auth
        token with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available recall hunt groups for this location.
        :type location_id: str
        :param name: Only return available recall hunt groups with the matching name.
        :type name: str
        :param order: Order the available recall hunt groups according to the designated fields. Available sort
            fields: lname.
        :param order: str
        :param org_id: Return the available recall hunt groups for this organization.
        :type org_id: str
        :return: yields :class:`AvailableRecallHuntGroup` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableRecallHuntGroups')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=AvailableRecallHuntGroup,
                                              params=params, item_key='huntGroups')]

    async def call_park_settings(self, location_id: str, org_id: str = None) -> LocationCallParkSettings:
        """
        Get Call Park Settings

        Retrieve Call Park Settings from call parks for a given location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Retrieving settings from call parks requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Return the call park settings for this location.
        :type location_id: str
        :param org_id: Return the call park settings for this organization.
        :type org_id: str
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, path='settings')
        return LocationCallParkSettings.parse_obj(await self.get(url, params=params))

    async def update_call_park_settings(self, location_id: str, settings: LocationCallParkSettings, org_id: str = None):
        """
        Update Call Park settings

        Update Call Park settings for the designated location.

        Call Park allows call recipients to place a call on hold so that it can be retrieved from another device.

        Updating call park settings requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location for which call park settings will be updated.
        :type location_id: str
        :param settings: update settings
        :type settings: :class:`LocationCallParkSettings`
        :param org_id: Update call park settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, path='settings')
        body = settings.update()
        await self.put(url, params=params, data=body)


class AsCallPickupApi(AsApiChild, base='telephony/config/callPickups'):
    """
    Call Pickup API
    """

    def _endpoint(self, *, location_id: str, pickup_id: str = None, path: str = None) -> str:
        """
        call park specific feature endpoint like /v1/telephony/config/locations/{locationId}/callPickups/{pickup_id}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param pickup_id: call pickup id
        :type pickup_id: str
        :param path: addtl. path
        :type path: str
        :return: full endpoint
        :rtype: str
        """
        pickup_id = pickup_id and f'/{pickup_id}' or ''
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/callPickups{pickup_id}{path}')
        return ep

    def list_gen(self, location_id: str, order: Literal['ASC', 'DSC'] = None, name: str = None,
             org_id: str = None, **params) -> AsyncGenerator[CallPickup, None, None]:
        """
        Read the List of Call Pickups

        List all Call Pickups for the organization.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving this list requires a full, user, or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Return the list of call pickups for this location.
        :type location_id: str
        :param order: Sort the list of call pickups by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call pickups that contains the given name. The maximum length is 80.
        :type name: str
        :param org_id: List call pickups for this organization.
        :type org_id: str
        :return: yields :class:`CallPickup` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i > 1 and v is not None and k != 'params')
        url = self._endpoint(location_id=location_id)
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CallPickup, params=params, item_key='callPickups')

    async def list(self, location_id: str, order: Literal['ASC', 'DSC'] = None, name: str = None,
             org_id: str = None, **params) -> List[CallPickup]:
        """
        Read the List of Call Pickups

        List all Call Pickups for the organization.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving this list requires a full, user, or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Return the list of call pickups for this location.
        :type location_id: str
        :param order: Sort the list of call pickups by name, either ASC or DSC. Default is ASC.
        :type order: str
        :param name: Return the list of call pickups that contains the given name. The maximum length is 80.
        :type name: str
        :param org_id: List call pickups for this organization.
        :type org_id: str
        :return: yields :class:`CallPickup` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i > 1 and v is not None and k != 'params')
        url = self._endpoint(location_id=location_id)
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=CallPickup, params=params, item_key='callPickups')]

    async def create(self, location_id: str, settings: CallPickup, org_id: str = None) -> str:
        """
        Create a Call Pickup

        Create new Call Pickups for the given location.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Creating a call pickup requires a full or user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Create the call pickup for this location.
        :type location_id: str
        :param settings: settings for new call pickup
        :type settings: :class:`CallPickup`
        :param org_id: Create the call pickup for this organization.
        :return: ID of the newly created call pickup.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = settings.create_or_update()
        data = await self.post(url, data=body, params=params)
        return data['id']

    async def delete_pickup(self, location_id: str, pickup_id: str, org_id: str = None):
        """
        Delete a Call Pickup

        Delete the designated Call Pickup.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Deleting a call pickup requires a full or user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location from which to delete a call pickup.
        :type location_id: str
        :param pickup_id: Delete the call pickup with the matching ID.
        :type pickup_id: str
        :param org_id: Delete the call pickup from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, pickup_id=pickup_id)
        params = org_id and {'orgId': org_id} or None
        await self.delete(url, params=params)

    async def details(self, location_id: str, pickup_id: str, org_id: str = None) -> CallPickup:
        """
        Get Details for a Call Pickup

        Retrieve Call Pickup details.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving call pickup details requires a full, user, or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Retrieve settings for a call pickup in this location.
        :type location_id: str
        :param pickup_id: Retrieve settings for a call pickup with the matching ID.
        :type pickup_id: str
        :param org_id: Retrieve call pickup settings from this organization.
        :type org_id: str
        :return: call pickup info
        :rtype: :class:`CallPickup`
        """
        url = self._endpoint(location_id=location_id, pickup_id=pickup_id)
        params = org_id and {'orgId': org_id} or None
        return CallPickup.parse_obj(await self.get(url, params=params))

    async def update(self, location_id: str, pickup_id: str, settings: CallPickup, org_id: str = None) -> str:
        """
        Update a Call Pickup

        Update the designated Call Pickup.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Updating a call pickup requires a full or user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        NOTE: The Call Pickup ID will change upon modification of the Call Pickup name.

        :param location_id: Location in which this call pickup exists.
        :type location_id: str
        :param pickup_id: Update settings for a call pickup with the matching ID.
        :type pickup_id: str
        :param settings: updates
        :type settings: :class:`CallPickup`
        :param org_id: Update call pickup settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, pickup_id=pickup_id)
        body = settings.create_or_update()
        data = await self.put(url, data=body, params=params)
        return data['id']

    def available_agents_gen(self, location_id: str, call_pickup_name: str = None, name: str = None,
                         phone_number: str = None, order: str = None,
                         org_id: str = None) -> AsyncGenerator[PersonPlaceAgent, None, None]:
        """
        Get available agents from Call Pickups
        Retrieve available agents from call pickups for a given location.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving available agents from call pickups requires a full, user, or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_pickup_name: Only return available agents from call pickups with the matching name.
        :type call_pickup_name: str
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, number and extension.
            The maximum supported sort order value is 3.
        :type order: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :return: yields :class:`PersonPlaceCallPark` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableUsers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=PersonPlaceAgent, params=params, item_key='agents')

    async def available_agents(self, location_id: str, call_pickup_name: str = None, name: str = None,
                         phone_number: str = None, order: str = None,
                         org_id: str = None) -> List[PersonPlaceAgent]:
        """
        Get available agents from Call Pickups
        Retrieve available agents from call pickups for a given location.

        Call Pickup enables a user(agent) to answer any ringing line within their pickup group.

        Retrieving available agents from call pickups requires a full, user, or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param location_id: Return the available agents for this location.
        :type location_id: str
        :param call_pickup_name: Only return available agents from call pickups with the matching name.
        :type call_pickup_name: str
        :param name: Only return available agents with the matching name.
        :type name: str
        :param phone_number: Only return available agents with the matching primary number.
        :type phone_number: str
        :param order: Order the available agents according to the designated fields. Up to three vertical bar (|)
            separated sort order fields may be specified. Available sort fields: fname, lname, number and extension.
            The maximum supported sort order value is 3.
        :type order: str
        :param org_id: Return the available agents for this organization.
        :type org_id: str
        :return: yields :class:`PersonPlaceCallPark` objects
        """
        params = {to_camel(k): v for i, (k, v) in enumerate(locals().items())
                  if i > 1 and v is not None}
        url = self._endpoint(location_id=location_id, path='availableUsers')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=PersonPlaceAgent, params=params, item_key='agents')]


class AsAnnouncementApi:
    """
    API for call queue Announcements
    """

    def __init__(self, *, session: AsRestSession):
        self._session = session

    def _endpoint(self, location_id: str, queue_id: str, path: str = None):
        """

        :meta private:
        :param location_id:
        :param queue_id:
        :param path:
        :return:
        """
        path = path and f'/{path}' or ''
        ep = self._session.ep(path=f'telephony/config/locations/{location_id}/queues/{queue_id}/announcements{path}')
        return ep

    def list_gen(self, location_id: str, queue_id: str, org_id: str = None) -> AsyncGenerator[Announcement]:
        """

        :param location_id:
        :param queue_id:
        :param org_id:
        :return:
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = org_id and {'orgId': org_id} or dict()
        # noinspection PyTypeChecker
        return self._session.follow_pagination(url=url, model=Announcement, params=params)

    async def list(self, location_id: str, queue_id: str, org_id: str = None) -> List[Announcement]:
        """

        :param location_id:
        :param queue_id:
        :param org_id:
        :return:
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = org_id and {'orgId': org_id} or dict()
        # noinspection PyTypeChecker
        return [o async for o in self._session.follow_pagination(url=url, model=Announcement, params=params)]

    async def delete_announcement(self, location_id: str, queue_id: str, file_name: str, org_id: str = None):
        """

        :param location_id:
        :type location_id: str
        :param queue_id:
        :type queue_id: str
        :param file_name:
        :type file_name: str
        :param org_id:
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id, path=file_name)
        params = org_id and {'orgId': org_id} or None
        await self._session.delete(url=url, params=params)


class AsCQPolicyApi:
    _session: AsRestSession

    def _ep(self, location_id: str, queue_id: str, path: str):
        return self._session.ep(f'telephony/config/locations/{location_id}/queues/{queue_id}/{path}')

    def __init__(self, session: AsRestSession):
        self._session = session

    async def holiday_service_details(self, location_id: str, queue_id: str, org_id: str = None) -> HolidayService:
        """
        Retrieve Call Queue Holiday Service details.

        Configure the call queue to route calls differently during the holidays.

        Retrieving call queue holiday service details requires a full or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str
        :return: Call Queue Holiday Service details
        :rtype: HolidayService
        """
        url = self._ep(location_id, queue_id, 'holidayService')
        params = org_id and {'orgId': org_id} or None
        data = await self._session.rest_get(url=url, params=params)
        return HolidayService.parse_obj(data)

    async def holiday_service_update(self, location_id: str, queue_id: str, update: HolidayService, org_id: str = None):
        """
        Update the designated Call Queue Holiday Service.

        Configure the call queue to route calls differently during the holidays.

        Updating a call queue holiday service requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param update: holiday service settings.
        :type update: HolidayService
        :param org_id: Update call queue settings from this organisation.
        :type org_id: str
        """
        url = self._ep(location_id, queue_id, 'holidayService')
        params = org_id and {'orgId': org_id} or None
        body = update.json(exclude={'holiday_schedules'})
        await self._session.rest_put(url=url, params=params, data=body)

    async def night_service_detail(self, location_id: str, queue_id: str, org_id: str = None) -> NightService:
        """
        Retrieve Call Queue Night service details.

        Configure the call queue to route calls differently during the hours when the queue is not in service. This
        is determined by a schedule that defines the business hours of the queue.

        Retrieving call queue details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue night service with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue night service settings from this organisation
        :type org_id: str
        :return: Call Queue Night service details
        :rtype: NightService
        """
        url = self._ep(location_id, queue_id, 'nightService')
        params = org_id and {'orgId': org_id} or None
        data = await self._session.rest_get(url=url, params=params)
        return NightService.parse_obj(data)

    async def night_service_update(self, location_id: str, queue_id: str, update: NightService, org_id: str = None):
        """
        Update Call Queue Night Service details.

        Configure the call queue to route calls differently during the hours when the queue is not in service. This
        is determined by a schedule that defines the business hours of the queue.

        Retrieving call queue night service details requires a full or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: update settings for a call queue in this location.
        :type location_id: str
        :param queue_id: update settings for the call queue night service with this identifier.
        :type queue_id: str
        :param update: new night service settings
        :type update: NightService
        :param org_id: update call queue night service settings from this organisation.
        :type org_id: str
        """
        url = self._ep(location_id, queue_id, 'nightService')
        params = org_id and {'orgId': org_id} or None
        body = update.json(exclude={'business_hours_schedules'})
        await self._session.rest_put(url=url, params=params, data=body)

    async def stranded_calls_details(self, location_id: str, queue_id: str, org_id: str = None) -> StrandedCalls:
        """
        Allow admin to view default/configured Stranded Calls settings.

        Stranded-All agents logoff Policy: If the last agent staffing a queue “unjoins” the queue or signs out,
        then all calls in the queue become stranded. Stranded-Unavailable Policy: This policy allows for the
        configuration of the processing of calls that are in a staffed queue when all agents are unavailable.

        Retrieving call queue Stranded Calls details requires a full or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location.
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str
        :return: Stranded Calls settings
        :rtype: StrandedCalls
        """
        url = self._ep(location_id, queue_id, 'strandedCalls')
        params = org_id and {'orgId': org_id} or None
        data = await self._session.rest_get(url=url, params=params)
        return StrandedCalls.parse_obj(data)

    async def stranded_calls_update(self, location_id: str, queue_id: str, update: StrandedCalls, org_id: str = None):
        """
        Update the designated Call Stranded Calls Service.

        Allow admin to modify configured Stranded Calls settings.

        Updating a call queue stranded calls requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param update: Call Stranded Calls settings
        :type update: StrandedCalls
        :param org_id: Update call queue settings from this organisation.
        :type org_id: str
        """
        url = self._ep(location_id, queue_id, 'strandedCalls')
        params = org_id and {'orgId': org_id} or None
        await self._session.rest_put(url=url, params=params, data=update.json())

    async def forced_forward_details(self, location_id: str, queue_id: str, org_id: str = None) -> ForcedForward:
        """
        Retrieve Call Queue policy Forced Forward details.

        This policy allows calls to be temporarily diverted to a configured destination.

        Retrieving call queue Forced Forward details requires a full or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Location in which this call queue exists.
        :param queue_id: Retrieve setting for the call queue with the matching ID.
        :param org_id: Retrieve call queue settings from this organisation.
        :return: Call Queue policy Forced Forward details.
        :rtype: ForcedForward
        """
        url = self._ep(location_id, queue_id, 'forcedForward')
        params = org_id and {'orgId': org_id} or None
        data = await self._session.rest_get(url=url, params=params)
        return ForcedForward.parse_obj(data)

    async def forced_forward_update(self, location_id: str, queue_id: str, update: ForcedForward, org_id: str = None):
        """
        Update the designated Forced Forward Service.

        If the option is enabled, then incoming calls to the queue are forwarded to the configured destination. Calls
        that are already in the queue remain queued. The policy can be configured to play an announcement prior to
        proceeding with the forward.

        Updating a call queue Forced Forward service requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param update: new call queue Forced Forward settings
        :type update: ForcedForward
        :param org_id: Update call queue settings from this organisation.
        :type org_id: str
        """
        url = self._ep(location_id, queue_id, 'forcedForward')
        params = org_id and {'orgId': org_id} or None
        await self._session.rest_put(url=url, params=params, data=update.json())


class AsCallQueueApi:
    """
    Call Queue APÍ
    """
    forwarding: AsForwardingApi
    announcement: AsAnnouncementApi
    policy: AsCQPolicyApi

    def __init__(self, session: AsRestSession):
        self._session = session
        self.forwarding = AsForwardingApi(session=session, feature_selector=FeatureSelector.queues)
        self.announcement = AsAnnouncementApi(session=session)
        self.policy = AsCQPolicyApi(session=session)

    def _endpoint(self, *, location_id: str = None, queue_id: str = None):
        """
        Helper to get URL for API endpoints

        :meta private:
        :param location_id:
        :param queue_id:
        :return:
        """
        if location_id is None:
            return self._session.ep('telephony/config/queues')
        else:
            ep = self._session.ep(f'telephony/config/locations/{location_id}/queues')
            if queue_id:
                ep = f'{ep}/{queue_id}'
            return ep

    @staticmethod
    def update_or_create(*, queue: CallQueue) -> str:
        """
        Get JSON for update or create

        :param queue:
        :return:
        :meta private:
        """
        return queue.json(
            exclude={'id': True,
                     'location_name': True,
                     'location_id': True,
                     'toll_free_number': True,
                     'language': True,
                     'agents':
                         {'__all__':
                              {'first_name': True,
                               'last_name': True,
                               'user_type': True,
                               'extension': True,
                               'phone_number': True}},
                     'alternate_number_settings':
                         {'alternate_numbers':
                              {'__all__':
                                   {'toll_free_number': True}}},
                     'queue_settings':
                         {'overflow':
                              {'is_transfer_number_set': True}}})

    def list_gen(self, location_id: str = None, name: str = None,
             org_id: str = None, **params) -> AsyncGenerator[CallQueue, None, None]:
        """
        Read the List of Call Queues
        List all Call Queues for the organization.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Only return call queues with matching location ID.
        :type location_id: str
        :param name: Only return call queues with the matching name.
        :type name: str
        :param org_id: List call queues for this organization
        :type org_id: str
        :param params: dict of additional parameters passed directly to endpoint
        :type params: dict
        :return: yields :class:`CallQueue` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self._session.follow_pagination(url=url, model=CallQueue, params=params)

    async def list(self, location_id: str = None, name: str = None,
             org_id: str = None, **params) -> List[CallQueue]:
        """
        Read the List of Call Queues
        List all Call Queues for the organization.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Only return call queues with matching location ID.
        :type location_id: str
        :param name: Only return call queues with the matching name.
        :type name: str
        :param org_id: List call queues for this organization
        :type org_id: str
        :param params: dict of additional parameters passed directly to endpoint
        :type params: dict
        :return: yields :class:`CallQueue` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return [o async for o in self._session.follow_pagination(url=url, model=CallQueue, params=params)]

    async def by_name(self, name: str, location_id: str = None, org_id: str = None) -> Optional[CallQueue]:
        """
        Get queue info by name

        :param location_id:
        :param name:
        :param org_id:
        :return:
        """
        return next((cq for cq in await self.list(location_id=location_id, org_id=org_id, name=name)
                     if cq.name == name), None)

    async def create(self, location_id: str, settings: CallQueue, org_id: str = None) -> str:
        """
        Create a Call Queue
        Create new Call Queues for the given location.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Creating a call queue requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Create the call queue for this location.
        :type location_id: str
        :param settings: parameters for queue creation.
        :type settings: :class:`CallQueue`
        :param org_id: Create the call queue for this organization.
        :type org_id: str
        :return: queue id
        :rtype: str

        Example:

            .. code-block:: python

                settings = CallQueue(name=new_name,
                                     extension=extension,
                                     call_policies=CallQueueCallPolicies.default(),
                                     queue_settings=QueueSettings.default(queue_size=10),
                                     agents=[Agent(agent_id=user.person_id) for user in members])

                # create new queue
                queue_id = api.telephony.callqueue.create(location_id=target_location.location_id,
                                                          settings=settings)

        """
        params = org_id and {'orgId': org_id} or {}
        cq_data = settings.create_or_update()
        url = self._endpoint(location_id=location_id)
        data = await self._session.rest_post(url, data=cq_data, params=params)
        return data['id']

    async def delete_queue(self, location_id: str, queue_id: str, org_id: str = None):
        """
        Delete a Call Queue
        Delete the designated Call Queue.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Deleting a call queue requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a call queue.
        :type location_id: str
        :param queue_id: Delete the call queue with the matching ID.
        :type queue_id: str
        :param org_id: Delete the call queue from this organization.
        :type org_id: str
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = org_id and {'orgId': org_id} or None
        await self._session.rest_delete(url=url, params=params)

    async def details(self, location_id: str, queue_id: str, org_id: str = None) -> CallQueue:
        """
        Get Details for a Call Queue
        Retrieve Call Queue details.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned anvinternal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Retrieving call queue details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a call queue in this location
        :type location_id: str
        :param queue_id: Retrieve settings for the call queue with this identifier.
        :type queue_id: str
        :param org_id: Retrieve call queue settings from this organization.
        :type org_id: str
        :return: call queue details
        :rtype: :class:`CallQueue`
        """
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        params = {'orgId': org_id} if org_id is not None else {}
        data = await self._session.rest_get(url, params=params)
        result = CallQueue.parse_obj(data)
        result.location_id = location_id
        # noinspection PyTypeChecker
        return result

    async def update(self, location_id: str, queue_id: str, update: CallQueue, org_id: str = None):
        """
        Update a Call Queue

        Update the designated Call Queue.

        Call queues temporarily hold calls in the cloud when all agents, which can be users or agents, assigned to
        receive calls from the queue are unavailable. Queued calls are routed to an available agent when not on an
        active call. Each call queue is assigned a Lead Number, which is a telephone number outside callers can dial
        to reach users assigned to the call queue. Call queues are also assigned an internal extension, which can be
        dialed internally to reach users assigned to the call queue.

        Updating a call queue requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this call queue exists.
        :type location_id: str
        :param queue_id: Update setting for the call queue with the matching ID.
        :type queue_id: str
        :param update: updates
        :type update: :class:`CallQueue`
        :param org_id: Update call queue settings from this organization.

        Examples:

        .. code-block::

            api = WebexSimpleApi()

            # shortcut
            cq = api.telephony.callqueue

            # disable a call queue
            update = CallQueue(enabled=False)
            cq.update(location_id=...,
                      queue_id=...,
                      update=update)

            # set the call routing policy to SIMULTANEOUS
            update = CallQueue(call_policies=CallPolicies(policy=Policy.simultaneous))
            cq.update(location_id=...,
                      queue_id=...,
                      update=update)
            # don't bounce calls after the set number of rings.
            update = CallQueue(
                call_policies=CallPolicies(
                    call_bounce=CallBounce(
                        enabled=False)))
            cq.update(location_id=...,
                      queue_id=...,
                      update=update)

        Alternatively you can also read call queue details, update them in place and then call update().

        .. code-block::

            details = cq.details(location_id=...,
                                 queue_id=...)
            details.call_policies.call_bounce.agent_unavailable_enabled=False
            details.call_policies.call_bounce.on_hold_enabled=False
            cq.update(location_id=...,
                      queue_id=...,
                      update=details)

        """
        params = org_id and {'orgId': org_id} or None
        if location_id is None or queue_id is None:
            raise ValueError('location_id and queue_id cannot be None')
        cq_data = update.create_or_update()
        url = self._endpoint(location_id=location_id, queue_id=queue_id)
        await self._session.rest_put(url=url, data=cq_data, params=params)


class AsCallparkExtensionApi(AsApiChild, base='telephony'):
    """
    Call Park Extension API
    """

    def _endpoint(self, *, location_id: str = None, cpe_id: str = None) -> str:
        """
        call park extension specific feature endpoint like
        /v1/telephony/config/locations/{locationId}/callParkExtensions/{cpe_id}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param cpe_id: call park extension id
        :type cpe_id: str
        :return: full endpoint
        :rtype: str
        """
        if location_id is None:
            return self.session.ep('telephony/config/callParkExtensions')
        else:
            ep = self.session.ep(f'telephony/config/locations/{location_id}/callParkExtensions')
            if cpe_id:
                ep = f'{ep}/{cpe_id}'
            return ep

    def list_gen(self, extension: str = None, name: str = None, location_id: str = None,
             location_name: str = None, order: str = None, org_id: str = None,
             **params) -> AsyncGenerator[CallParkExtension, None, None]:
        """
        Read the List of Call Park Extensions

        List all Call Park Extensions for the organization.

        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call
        Park service for holding parked calls.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param extension: Only return call park extensions with the matching extension.
        :type extension: str
        :param name: Only return call park extensions with the matching name.
        :type name: str
        :param location_id: Only return call park extensions with matching location ID.
        :type location_id: str
        :param location_name: Only return call park extensions with matching location name.
        :type location_name: str
        :param order: Order the available agents according to the designated fields. Available sort fields: groupName,
            callParkExtension, callParkExtensionName, callParkExtensionExternalId.
        :type order: str
        :param org_id: List call park extensions for this organization.
        :type org_id: str
        :param params: additional parameters
        :return: yields :class:`wxc_sdk.common.CallParkExtension` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CallParkExtension, params=params)

    async def list(self, extension: str = None, name: str = None, location_id: str = None,
             location_name: str = None, order: str = None, org_id: str = None,
             **params) -> List[CallParkExtension]:
        """
        Read the List of Call Park Extensions

        List all Call Park Extensions for the organization.

        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call
        Park service for holding parked calls.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param extension: Only return call park extensions with the matching extension.
        :type extension: str
        :param name: Only return call park extensions with the matching name.
        :type name: str
        :param location_id: Only return call park extensions with matching location ID.
        :type location_id: str
        :param location_name: Only return call park extensions with matching location name.
        :type location_name: str
        :param order: Order the available agents according to the designated fields. Available sort fields: groupName,
            callParkExtension, callParkExtensionName, callParkExtensionExternalId.
        :type order: str
        :param org_id: List call park extensions for this organization.
        :type org_id: str
        :param params: additional parameters
        :return: yields :class:`wxc_sdk.common.CallParkExtension` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=CallParkExtension, params=params)]

    async def details(self, location_id: str, cpe_id: str, org_id: str = None) -> CallParkExtension:
        """
        Get Details for a Call Park Extension

        Retrieve Call Park Extension details.

        The Call Park service, enabled for all users by default, allows a user to park a call against an available
        user's extension or to a Call Park Extension. Call Park Extensions are extensions defined within the Call
        Park service for holding parked calls.

        Retrieving call park extension details requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve details for a call park extension in this location.
        :type location_id: str
        :param cpe_id: Retrieve details for a call park extension with the matching ID.
        :type cpe_id: str
        :param org_id: Retrieve call park extension details from this organization
        :type org_id: str
        :return: call park extension details
        :rtype: :class:`wxc_sdk.common.CallParkExtension` instance (only name and extension are set)
        """
        url = self._endpoint(location_id=location_id, cpe_id=cpe_id)
        params = org_id and {'orgId': org_id} or {}
        data = await self.get(url, params=params)
        return CallParkExtension.parse_obj(data)

    async def create(self, location_id: str, name: str, extension: str, org_id: str = None, ) -> str:
        """
        Create new Call Park Extensions for the given location.
        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.
        Creating a call park extension requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Create the call park extension for this location.
        :type location_id: str
        :param name: Name for the call park extension. The maximum length is 30.
        :type name: str
        :param extension: Unique extension which will be assigned to call park extension. The minimum length is 2,
            maximum length is 6.
        :type extension: str
        :param org_id: Create the call park extension for this organization.
        :type org_id: str
        :return: id of the new call park extension
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {'name': name, 'extension': extension}
        url = self._endpoint(location_id=location_id)
        data = await super().post(url=url, params=params, json=body)
        return data["id"]

    async def delete(self, location_id: str, cpe_id: str, org_id: str = None):
        """
        Delete the designated Call Park Extension.
        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.
        Deleting a call park extension requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a call park extension.
        :type location_id: str
        :param cpe_id: Delete the call park extension with the matching ID.
        :type cpe_id: str
        :param org_id: Delete the call park extension from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self._endpoint(location_id=location_id, cpe_id=cpe_id)

        await super().delete(url=url, params=params)
        return

    async def update(self, location_id: str, cpe_id: str, name: str = None, extension: str = None, org_id: str = None):
        """
        Update the designated Call Park Extension.
        Call Park Extension enables a call recipient to park a call to an extension, so someone else within the same
        Organization can retrieve the parked call by dialing that extension. Call Park Extensions can be added as
        monitored lines by users' Cisco phones, so users can park and retrieve calls by pressing the associated phone
        line key.
        Updating a call park extension requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location in which this call park extension exists.
        :type location_id: str
        :param cpe_id: Update a call park extension with the matching ID.
        :type cpe_id: str
        :param name: Name for the call park extension. The maximum length is 30.
        :type name: str
        :param extension: Unique extension which will be assigned to call park extension. The minimum length is 2,
            maximum length is 6.
        :type extension: str
        :param org_id: Update a call park extension from this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = {}
        if name is not None:
            body['name'] = name
        if extension is not None:
            body['extension'] = extension
        url = self._endpoint(location_id=location_id, cpe_id=cpe_id)
        await super().put(url=url, params=params, json=body)
        return


class AsCallsApi(AsApiChild, base='telephony/calls'):

    async def dial(self, destination: str) -> DialResponse:
        """
        Initiate an outbound call to a specified destination. This is also commonly referred to as Click to Call or
        Click to Dial. Alerts on all the devices belonging to the user. When the user answers on one of these alerting
        devices, an outbound call is placed from that device to the destination.

        :param destination: The destination to be dialed. The destination can be digits or a URI. Some examples for
            destination include: 1234, 2223334444, +12223334444, \*73, tel:+12223334444, user@company.domain,
            sip:user@company.domain
        :type destination: str
        :return: Call id and call session id
        """
        ep = self.ep('dial')
        data = await self.post(ep, json={'destination': destination})
        return DialResponse.parse_obj(data)

    async def answer(self, call_id: str):
        """
        Answer an incoming call on the user's primary device.

        :param call_id: The call identifier of the call to be answered.
        :type call_id: str
        """
        ep = self.ep('answer')
        await self.post(ep, json={'callId': call_id})

    async def reject(self, call_id: str, action: RejectAction = None):
        """
        Reject an unanswered incoming call.

        :param call_id: The call identifier of the call to be rejected.
        :type call_id: str
        :param action: The rejection action to apply to the call. The busy action is applied if no specific action is
            provided.
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('reject')
        await self.post(ep, json=data)

    async def hangup(self, call_id: str):
        """
        Hangup a call. If used on an unanswered incoming call, the call is rejected and sent to busy.

        :param call_id: The call identifier of the call to hangup.
        :type call_id: str
        """
        ep = self.ep('hangup')
        await self.post(ep, json={'callId': call_id})

    async def hold(self, call_id: str):
        """
        Hold a connected call.

        :param call_id: The call identifier of the call to hold.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('hold')
        await self.post(ep, json=data)

    async def resume(self, call_id: str):
        """
        Resume a held call.

        :param call_id: The call identifier of the call to resume.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('resume')
        await self.post(ep, json=data)

    async def divert(self, call_id: str, destination: str = None, to_voicemail: bool = None):
        """
        Divert a call to a destination or a user's voicemail. This is also commonly referred to as Blind Transfer

        :param call_id: The call identifier of the call to divert.
        :type call_id: str
        :param destination: The destination to divert the call to. If toVoicemail is false, destination is required.
            The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444,
            +12223334444, \*73, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type destination: str
        :param to_voicemail: If set to true, the call is diverted to voicemail. If no destination is specified, the
            call is diverted to the user's own voicemail. If a destination is specified, the call is diverted to the
            specified user's voicemail.
        :type to_voicemail: bool
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('divert')
        await self.post(ep, json=data)

    async def transfer(self, call_id1: str = None, call_id2: str = None, destination: str = None):
        """
        Transfer two calls together. Unanswered incoming calls cannot be transferred but can be diverted using the
        divert API. If the user has only two calls and wants to transfer them together, the callId1 and callId2
        parameters are optional and when not provided the calls are automatically selected and transferred. If the
        user has more than two calls and wants to transfer two of them together, the callId1 and callId2 parameters
        are mandatory to specify which calls are being transferred. These are also commonly referred to as Attended
        Transfer, Consultative Transfer, or Supervised Transfer and will return a 204 response. If the user wants to
        transfer one call to a new destination but only when the destination responds, the callId1 and destination
        parameters are mandatory to specify the call being transferred and the destination. This is referred to as a
        Mute Transfer and is similar to the divert API with the difference of waiting for the destination to respond
        prior to transferring the call. If the destination does not respond, the call is not transferred. This will
        return a 201 response.

        :param call_id1: The call identifier of the first call to transfer. This parameter is mandatory if either
            call_id2 or destination is provided.
        :type call_id1: str
        :param call_id2: The call identifier of the first call to transfer. This parameter is mandatory if either
            callId2 or destination is provided.
        :type call_id1: str
        :param destination: The destination to be transferred to. The destination can be digits or a URI. Some
            examples for destination include: 1234, 2223334444,
            +12223334444, \*73, tel:+12223334444, user@company.domain, sip:user@company.domain.
            This parameter is mandatory if call_id1 is provided and call_id2 is not provided.
        :type destination: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('transfer')
        await self.post(ep, json=data)

    async def park(self, call_id: str, destination: str = None, is_group_park: bool = None) -> ParkedAgainst:
        """
        Park a connected call. The number field in the response can be used as the destination for the retrieve
        command to retrieve the parked call.

        :param call_id: The call identifier of the call to park.
        :type call_id: str
        :param destination: Identifies where the call is to be parked. If not provided, the call is parked against the
            parking user.
            The destination can be digits or a URI. Some examples for destination include: 1234, 2223334444,
            +12223334444, \*73, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type destination: str
        :param is_group_park: If set to true, the call is parked against an automatically selected member of the
            user's call park group and the destination parameter is ignored.
        :type is_group_park: bool
        :return: The details of where the call has been parked.
        :rtype: :class:`ParkedAgainst`
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('park')
        data = await self.post(ep, json=data)
        return ParkedAgainst.parse_obj(data)

    async def retrieve(self, destination: str) -> CallInfo:
        """
        :param destination: Identifies where the call is parked. The number field from the park command response can
            be used as the destination for the retrieve command. If not provided, the call parked against the
            retrieving user is retrieved. The destination can be digits or a URI. Some examples for destination
            include: 1234, 2223334444, +12223334444, \*73, tel:+12223334444, user@company.domain,
            sip:user@company.domain
        :return: call id and call session id of retreived call
        :rtype: :class:`CallInfo`
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('retrieve')
        data = await self.post(ep, json=data)
        return CallInfo.parse_obj(data)

    async def start_recording(self, call_id: str):
        """
        Start recording a call. Use of this API is only valid when the user's call recording mode is set to "On Demand".

        :param call_id: The call identifier of the call to start recording.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('startRecording')
        await self.post(ep, json=data)

    async def stop_recording(self, call_id: str):
        """
        Stop recording a call. Use of this API is only valid when a call is being recorded and the user's call
        recording mode is set to "On Demand".

        :param call_id: The call identifier of the call to stop recording.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('stopRecording')
        await self.post(ep, json=data)

    async def pause_recording(self, call_id: str):
        """
        Pause recording on a call. Use of this API is only valid when a call is being recorded and the user's call
        recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param call_id: The call identifier of the call to pause recording.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('pauseRecording')
        await self.post(ep, json=data)

    async def resume_recording(self, call_id: str):
        """
        Resume recording a call. Use of this API is only valid when a call's recording is paused and the user's call
        recording mode is set to "On Demand" or "Always with Pause/Resume".

        :param call_id: The call identifier of the call to resume recording.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('resumeRecording')
        await self.post(ep, json=data)

    async def transmit_dtmf(self, call_id: str, dtmf: str):
        """
        Transmit DTMF digits to a call.

        :param call_id: The call identifier of the call to hold.
        :type call_id: str
        :param dtmf: The DTMF digits to transmit. Each digit must be part of the following set: [0, 1, 2, 3, 4, 5, 6,
            7, 8, 9, \*, #, A, B, C, D]. A comma "," may be included to indicate a pause between digits. For the value
            “1,234”, the DTMF 1 digit is initially sent. After a pause, the DTMF 2, 3, and 4 digits are sent
            successively.
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('transmitDtmf')
        await self.post(ep, json=data)

    async def push(self, call_id: str):
        """
        Pushes a call from the assistant to the executive the call is associated with. Use of this API is only valid
        when the assistant’s call is associated with an executive.

        :param call_id: The call identifier of the call to push.
        :type call_id: str
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('push')
        await self.post(ep, json=data)

    async def pickup(self, target: str) -> CallInfo:
        """
        Picks up an incoming call to another user. A new call is initiated to perform the pickup in a similar manner
        to the dial command. When target is not present, the API pickups up a call from the user’s call pickup group.
        When target is present, the API pickups an incoming call from the specified target user.

        :param target: Identifies the user to pickup an incoming call from. If not provided, an incoming call to the
            user’s call pickup group is picked up. The target can be digits or a URI. Some examples for target
            include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type target: str
        :return: call info of picked up call
        :rtype: :class:`CallInfo`
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('pickup')
        data = await self.post(ep, json=data)
        return CallInfo.parse_obj(data)

    async def barge_in(self, target: str):
        """
        Barge-in on another user’s answered call. A new call is initiated to perform the barge-in in a similar manner
        to the dial command.

        :param target: Identifies the user to barge-in on. The target can be digits or a URI. Some examples for target
            include: 1234, 2223334444, +12223334444, tel:+12223334444, user@company.domain, sip:user@company.domain
        :type target: str
        :return: call info of picked up call
        :rtype: :class:`CallInfo`
        """
        data = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                if i and v is not None}
        ep = self.ep('bargeIn')
        data = await self.post(ep, json=data)
        return CallInfo.parse_obj(data)

    def list_calls_gen(self) -> AsyncGenerator[TelephonyCall, None, None]:
        """
        Get the list of details for all active calls associated with the user.

        :return: yield :class:`TelephonyCall`
        """
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=TelephonyCall)

    async def list_calls(self) -> List[TelephonyCall]:
        """
        Get the list of details for all active calls associated with the user.

        :return: yield :class:`TelephonyCall`
        """
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=TelephonyCall)]

    async def call_details(self, call_id: str) -> TelephonyCall:
        """
        Get the details of the specified active call for the user.

        :param call_id: The call identifier of the call.
        :type call_id: str
        :return: call details
        :rtype: :class:`TelephonyCall`
        """
        ep = self.ep(call_id)
        data = await self.get(ep)
        return TelephonyCall.parse_obj(data)

    def call_history_gen(self, history_type: Union[str, HistoryType] = None) -> AsyncGenerator[CallHistoryRecord, None, None]:
        """
        List Call History
        Get the list of call history records for the user. A maximum of 20 call history records per type (placed,
        missed, received) are returned.

        :param history_type: The type of call history records to retrieve. If not specified, then all call history
            records are retrieved.
            Possible values: placed, missed, received
        :type history_type: HistoryType or str
        :return: yields :class:`CallHistoryRecord` objects
        """
        history_type = history_type and HistoryType.history_type_or_str(history_type)
        params = history_type and {'type': history_type.value} or None
        url = self.ep('history')
        return self.session.follow_pagination(url=url, model=CallHistoryRecord, params=params)

    async def call_history(self, history_type: Union[str, HistoryType] = None) -> List[CallHistoryRecord]:
        """
        List Call History
        Get the list of call history records for the user. A maximum of 20 call history records per type (placed,
        missed, received) are returned.

        :param history_type: The type of call history records to retrieve. If not specified, then all call history
            records are retrieved.
            Possible values: placed, missed, received
        :type history_type: HistoryType or str
        :return: yields :class:`CallHistoryRecord` objects
        """
        history_type = history_type and HistoryType.history_type_or_str(history_type)
        params = history_type and {'type': history_type.value} or None
        url = self.ep('history')
        return [o async for o in self.session.follow_pagination(url=url, model=CallHistoryRecord, params=params)]


class AsHuntGroupApi(AsApiChild, base='telephony/config/huntGroups'):
    """
    Hunt Group API
    """
    forwarding: AsForwardingApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.forwarding = AsForwardingApi(session=session, feature_selector=FeatureSelector.huntgroups)

    def _endpoint(self, *, location_id: str = None, huntgroup_id: str = None) -> str:
        """
        hunt group specific feature endpoint like /v1/telephony/config/locations/{locationId}/huntGroups/{huntGroupId}

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param huntgroup_id: schedule id
        :type huntgroup_id: str
        :return: full endpoint
        :rtype: str
        """
        if location_id is None:
            return self.session.ep('telephony/config/huntGroups')
        else:
            ep = self.session.ep(f'telephony/config/locations/{location_id}/huntGroups')
            if huntgroup_id:
                ep = f'{ep}/{huntgroup_id}'
            return ep

    def list_gen(self, org_id: str = None, location_id: str = None, name: str = None,
             phone_number: str = None, **params) -> AsyncGenerator[HuntGroup, None, None]:
        """
        Read the List of Hunt Groups

        List all calling Hunt Groups for the organization.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List hunt groups for this organization.
        :param location_id: Only return hunt groups with matching location ID.
        :param name: Only return hunt groups with the matching name.
        :param phone_number: Only return hunt groups with the matching primary phone number or extension.
        :return: yields :class:`HuntGroup` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=HuntGroup, params=params)

    async def list(self, org_id: str = None, location_id: str = None, name: str = None,
             phone_number: str = None, **params) -> List[HuntGroup]:
        """
        Read the List of Hunt Groups

        List all calling Hunt Groups for the organization.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: List hunt groups for this organization.
        :param location_id: Only return hunt groups with matching location ID.
        :param name: Only return hunt groups with the matching name.
        :param phone_number: Only return hunt groups with the matching primary phone number or extension.
        :return: yields :class:`HuntGroup` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=HuntGroup, params=params)]

    async def by_name(self, name: str, location_id: str = None, org_id: str = None) -> Optional[HuntGroup]:
        """
        Get hunt group info by name
        :param location_id:
        :param name:
        :param org_id:
        :return:
        """
        return next((hg for hg in await self.list(name=name, location_id=location_id, org_id=org_id)
                     if hg.name == name), None)

    async def create(self, location_id: str, settings: HuntGroup, org_id: str = None) -> str:
        """
        Create a Hunt Group

        Create new Hunt Groups for the given location.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Creating a hunt group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the hunt group for the given location.
        :type location_id: str
        :param settings: hunt group details
        :type settings: :class:`HuntGroup`
        :param org_id: Create the hunt group for this organization.
        :type org_id: str
        :return: ID of the newly created hunt group.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or {}
        settings.call_policies = settings.call_policies or HGCallPolicies().default()
        data = settings.create_or_update()
        url = self._endpoint(location_id=location_id)
        data = await self.post(url, data=data, params=params)
        return data['id']

    async def delete_huntgroup(self, location_id: str, huntgroup_id: str, org_id: str = None):
        """
        Delete a Hunt Group

        Delete the designated Hunt Group.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Deleting a hunt group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a hunt group.
        :type location_id: str
        :param huntgroup_id: Delete the hunt group with the matching ID.
        :type huntgroup_id: str
        :param org_id: Delete the hunt group with the matching ID.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, huntgroup_id=huntgroup_id)
        await self.delete(url, params=params)

    async def details(self, location_id: str, huntgroup_id: str, org_id: str = None) -> HuntGroup:
        """
        Get Details for a Hunt Group

        Retrieve Hunt Group details.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Retrieving hunt group details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Retrieve settings for a hunt group in this location.
        :type location_id: str
        :param huntgroup_id: Retrieve settings for the hunt group with this identifier.
        :type huntgroup_id: str
        :param org_id: Retrieve hunt group settings from this organization.
        :type org_id: str
        :return: hunt group details
        """
        url = self._endpoint(location_id=location_id, huntgroup_id=huntgroup_id)
        params = org_id and {'orgId': org_id} or {}
        data = await self.get(url, params=params)
        result = HuntGroup.parse_obj(data)
        return result

    async def update(self, location_id: str, huntgroup_id: str, update: HuntGroup,
               org_id: str = None):
        """
        Update a Hunt Group

        Update the designated Hunt Group.

        Hunt groups can route incoming calls to a group of people or workspaces. You can even configure a pattern to
        route to a whole group.

        Updating a hunt group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Update the hunt group for this location.
        :type location_id: str
        :param huntgroup_id: Update setting for the hunt group with the matching ID.
        :type huntgroup_id: str
        :param update: hunt group settings
        :type update: :class:`HuntGroup`
        :param org_id: Update hunt group settings from this organization.
        """
        params = org_id and {'orgId': org_id} or None
        data = update.create_or_update()
        url = self._endpoint(location_id=location_id, huntgroup_id=huntgroup_id)
        await self.put(url, data=data, params=params)


class AsManageNumbersJobsApi(AsApiChild, base='telephony/config/jobs/numbers'):
    """
    API for jobs to manage numbers
    """

    def list_jobs_gen(self, org_id: str = None, **params) -> AsyncGenerator[NumberJob, None, None]:
        """
        Lists all Manage Numbers jobs for the given organization in order of most recent one to oldest one
        irrespective of its status.
        The public API only supports initiating jobs which move numbers between locations.
        Via Control Hub they can initiate both the move and delete, so this listing can show both.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Retrieve list of Manage Number jobs for this organization.
        :type org_id: str
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('manageNumbers')
        return self.session.follow_pagination(url=url, model=NumberJob, params=params)

    async def list_jobs(self, org_id: str = None, **params) -> List[NumberJob]:
        """
        Lists all Manage Numbers jobs for the given organization in order of most recent one to oldest one
        irrespective of its status.
        The public API only supports initiating jobs which move numbers between locations.
        Via Control Hub they can initiate both the move and delete, so this listing can show both.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param org_id: Retrieve list of Manage Number jobs for this organization.
        :type org_id: str
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('manageNumbers')
        return [o async for o in self.session.follow_pagination(url=url, model=NumberJob, params=params)]

    async def initiate_job(self, operation: str, target_location_id: str,
                     number_list: list[NumberItem]) -> NumberJob:
        """
        Starts the numbers move from one location to another location. Although jobs can do both MOVE and DELETE
        actions internally, only MOVE is supported publicly.
        In order to move a number,
        For example, you can move from Cisco PSTN to Cisco PSTN, but you cannot move from Cisco PSTN to a location
        with Cloud Connected PSTN.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param operation: Indicates the kind of operation to be carried out. 
        :type operation: str
        :param target_location_id: The target location within organization where the unassigned numbers will be moved
            from the source location.
        :type target_location_id: str
        :param number_list: Indicates the numbers to be moved from source to target locations.
        :type number_list: list[NumberItem]
        """
        body = InitiateMoveNumberJobsBody(operation=operation,
                                          target_location_id=target_location_id,
                                          number_list=number_list)
        url = self.ep('manageNumbers')
        data = await super().post(url=url, data=body.json())
        return NumberJob.parse_obj(data)

    async def job_status(self, job_id: str = None) -> NumberJob:
        """
        Returns the status and other details of the job.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param job_id: Retrieve job details for this jobId.
        :type job_id: str
        """
        url = self.ep(f'manageNumbers/{job_id}')
        data = await super().get(url=url)
        return NumberJob.parse_obj(data)

    async def pause_job(self, job_id: str = None, org_id: str = None):
        """
        Pause the running Manage Numbers Job. A paused job can be resumed or abandoned.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param job_id: Pause the Manage Numbers job for this jobId.
        :type job_id: str
        :param org_id: Pause the Manage Numbers job for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'manageNumbers/{job_id}/actions/pause/invoke')
        await super().post(url=url, params=params)
        return

    async def resume_job(self, job_id: str = None, org_id: str = None):
        """
        Resume the paused Manage Numbers Job. A paused job can be resumed or abandoned.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param job_id: Resume the Manage Numbers job for this jobId.
        :type job_id: str
        :param org_id: Resume the Manage Numbers job for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'manageNumbers/{job_id}/actions/resume/invoke')
        await super().post(url=url, params=params)
        return

    async def abandon_job(self, job_id: str = None, org_id: str = None):
        """
        Abandon the Manage Numbers Job.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param job_id: Abandon the Manage Numbers job for this jobId.
        :type job_id: str
        :param org_id: Abandon the Manage Numbers job for this organization.
        :type org_id: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'manageNumbers/{job_id}/actions/abandon/invoke')
        await super().post(url=url, params=params)
        return

    def list_job_errors_gen(self, job_id: str = None, org_id: str = None,
                        **params) -> AsyncGenerator[ManageNumberErrorItem, None, None]:
        """
        Lists all error details of Manage Numbers job. This will not list any errors if exitCode is COMPLETED. If the
        status is COMPLETED_WITH_ERRORS then this lists the cause of failures.
        List of possible Errors:
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param job_id: Retrieve the error details for this jobId.
        :type job_id: str
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'manageNumbers/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ManageNumberErrorItem, params=params)

    async def list_job_errors(self, job_id: str = None, org_id: str = None,
                        **params) -> List[ManageNumberErrorItem]:
        """
        Lists all error details of Manage Numbers job. This will not list any errors if exitCode is COMPLETED. If the
        status is COMPLETED_WITH_ERRORS then this lists the cause of failures.
        List of possible Errors:
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param job_id: Retrieve the error details for this jobId.
        :type job_id: str
        :param org_id: Retrieve list of jobs for this organization.
        :type org_id: str
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'manageNumbers/{job_id}/errors')
        return [o async for o in self.session.follow_pagination(url=url, model=ManageNumberErrorItem, params=params)]


class AsJobsApi(AsApiChild, base='telephony/config/jobs'):
    """
    Jobs API
    """
    #: API for device settings jobs
    device_settings: AsDeviceSettingsJobsApi
    #: API for manage numbers jobs
    manage_numbers: AsManageNumbersJobsApi

    def __init__(self, *, session: AsRestSession):
        super().__init__(session=session)
        self.device_settings = AsDeviceSettingsJobsApi(session=session)
        self.manage_numbers = AsManageNumbersJobsApi(session=session)


class AsLocationInterceptApi(AsApiChild, base='telephony/config/locations'):
    """
    API for location's call intercept settings
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific
        telephony/config/locations/{locationId}/intercept

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/intercept{path}')
        return ep

    async def read(self, location_id: str, org_id: str = None) -> InterceptSetting:
        """
        Get Location Intercept

        Retrieve intercept location details for a customer location.

        Intercept incoming or outgoing calls for persons in your organization. If this is enabled, calls are either
        routed to a designated number the person chooses, or to the person's voicemail.

        Retrieving intercept location details requires a full, user or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve intercept details for this location.
        :type location_id: str
        :param org_id: Retrieve intercept location details for a customer location.
        :type org_id: str
        :return: user's call intercept settings
        :rtype: :class:`wxc_sdk.person_settings.call_intercept.InterceptSetting`
        """
        ep = self._endpoint(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        return InterceptSetting.parse_obj(await self.get(ep, params=params))

    async def configure(self, location_id: str, settings: InterceptSetting, org_id: str = None):
        """
        Put Location Intercept

        Modifies the intercept location details for a customer location.

        Intercept incoming or outgoing calls for users in your organization. If this is enabled, calls are either
        routed to a designated number the user chooses, or to the user's voicemail.

        Modifying the intercept location details requires a full, user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Unique identifier for the person.
        :type location_id: str
        :param settings: new intercept settings
        :type settings: InterceptSetting
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners)
            may use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        """
        ep = self._endpoint(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = settings.json()
        await self.put(ep, params=params, data=data)


class AsOrganisationVoicemailSettingsAPI(AsApiChild, base='telephony/config/voicemail/settings'):
    """
    API for Organisation voicemail settings
    """

    async def read(self, org_id: str = None) -> OrganisationVoicemailSettings:
        """
        Get Voicemail Settings

        Retrieve the organization's voicemail settings.

        Organizational voicemail settings determines what voicemail features a person can configure and automatic
        message expiration.

        Retrieving organization's voicemail settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param org_id: Retrieve voicemail settings for this organization.
        :type org_id: str
        :return: VM settings
        :rtype: OrganisationVoicemailSettings
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        return OrganisationVoicemailSettings.parse_obj(await self.get(url, params=params))

    async def update(self, settings: OrganisationVoicemailSettings, org_id: str = None):
        """
        Update the organization's voicemail settings.

        Organizational voicemail settings determines what voicemail features a person can configure and automatic
        message expiration.

        Updating organization's voicemail settings requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param settings: new settings
        :type settings: OrganisationVoicemailSettings
        :param org_id: Update voicemail settings for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = settings.json()
        await self.put(url, data=data, params=params)


class AsPagingApi(AsApiChild, base='telephony/config'):

    def _endpoint(self, *, location_id: str = None, paging_id: str = None) -> str:
        """
        endpoint for paging group operation

        :meta private:
        :param location_id:
        :type location_id: str
        :param paging_id:
        :type paging_id: str
        """
        if location_id is None:
            return super().ep('paging')
        paging_id = paging_id and f'/{paging_id}' or ''
        return super().ep(f'locations/{location_id}/paging{paging_id}')

    def list_gen(self, location_id: str = None, name: str = None, phone_number: str = None,
             org_id: str = None, **params) -> AsyncGenerator[Paging, None, None]:
        """
        Read the List of Paging Groups
        List all Paging Groups for the organization.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return only paging groups with matching location ID. Default is all locations
        :type location_id: str
        :param name: Return only paging groups with the matching name.
        :type name: str
        :param phone_number: Return only paging groups with matching primary phone number or extension.
        :type phone_number: str
        :param org_id: List paging groups for this organization.
        :type org_id: str
        :return: generator of class:`Paging` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=Paging, params=params, item_key='locationPaging')
        pass

    async def list(self, location_id: str = None, name: str = None, phone_number: str = None,
             org_id: str = None, **params) -> List[Paging]:
        """
        Read the List of Paging Groups
        List all Paging Groups for the organization.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return only paging groups with matching location ID. Default is all locations
        :type location_id: str
        :param name: Return only paging groups with the matching name.
        :type name: str
        :param phone_number: Return only paging groups with matching primary phone number or extension.
        :type phone_number: str
        :param org_id: List paging groups for this organization.
        :type org_id: str
        :return: generator of class:`Paging` objects
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and v is not None and k != 'params')
        url = self._endpoint()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=Paging, params=params, item_key='locationPaging')]
        pass

    async def create(self, location_id: str, settings: Paging, org_id: str = None) -> str:
        """
        Create a new Paging Group
        Create a new Paging Group for the given location.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Creating a paging group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Create the paging group for this location.
        :type location_id: str
        :param settings: new paging group
        :type settings: Paging
        :param org_id: Create the paging group for this organization.
        :type org_id: str
        :return: ID of the newly created paging group.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        if settings.originators and settings.originator_caller_id_enabled is None:
            raise TypeError('originator_caller_id_enabled required if originators are provided')
        url = self._endpoint(location_id=location_id)
        data = settings.create_or_update()
        data = await self.post(url, data=data, params=params)
        return data['id']

    async def delete_paging(self, location_id: str, paging_id: str, org_id: str = None):
        """
        Delete a Paging Group
        Delete the designated Paging Group.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Deleting a paging group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a paging group.
        :type location_id: str
        :param paging_id: Delete the paging group with the matching ID.
        :param org_id: Delete the paging group from this organization.
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, paging_id=paging_id)
        await self.delete(url, params=params)

    async def details(self, location_id: str, paging_id: str, org_id: str = None) -> Paging:
        """
        Get Details for a Paging Group
        Retrieve Paging Group details.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Retrieving paging group details requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.
        :param location_id: Retrieve settings for a paging group in this location.
        :param paging_id: Retrieve settings for the paging group with this identifier.
        :param org_id: Retrieve paging group settings from this organization.
        :return: :class:`Paging` object
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, paging_id=paging_id)
        return Paging.parse_obj(await self.get(url, params=params))

    async def update(self, location_id: str, update: Paging, paging_id: str, org_id: str = None):
        """
        Update the designated Paging Group.

        Group Paging allows a person to place a one-way call or group page to up to 75 people and/or workspaces by
        dialing a number or extension assigned to a specific paging group. The Group Paging service makes a
        simultaneous call to all the assigned targets.

        Updating a paging group requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param location_id: Update settings for a paging group in this location.
        :type location_id: str
        :param update: update parameters
        :type update: Paging
        :param paging_id: Update settings for the paging group with this identifier.
        :type paging_id: str
        :param org_id: Update paging group settings from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, paging_id=paging_id)
        data = update.create_or_update()
        await self.put(url, data=data, params=params)


class AsDialPlanApi(AsApiChild, base='telephony/config/premisePstn/dialPlans'):

    def list_gen(self, dial_plan_name: str = None, route_group_name: str = None, trunk_name: str = None,
             order: str = None, org_id: str = None, **params) -> AsyncGenerator[DialPlan, None, None]:
        """
        List all Dial Plans for the organization.

        Dial plans route calls to on-premises destinations by use of the trunks or route groups with which the dial
        plan is associated. Multiple dial patterns can be defined as part of your dial plan. Dial plans are configured
        globally for an enterprise and apply to all users, regardless of location.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_name: Return the list of dial plans matching the dial plan name.
        :type dial_plan_name: str
        :param route_group_name: Return the list of dial plans matching the route group name.
        :type route_group_name: str
        :param trunk_name: Return the list of dial plans matching the trunk name.
        :type trunk_name: str
        :param order: Order the dial plans according to the designated fields. Available sort fields: name, routeName,
            routeType. Sort order is ascending by default
        :type order: str
        :param org_id: List dial plans for this organization.
        :type org_id: str
        :return:
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i and v is not None and p != 'params')
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=DialPlan, params=params, item_key='dialPlans')

    async def list(self, dial_plan_name: str = None, route_group_name: str = None, trunk_name: str = None,
             order: str = None, org_id: str = None, **params) -> List[DialPlan]:
        """
        List all Dial Plans for the organization.

        Dial plans route calls to on-premises destinations by use of the trunks or route groups with which the dial
        plan is associated. Multiple dial patterns can be defined as part of your dial plan. Dial plans are configured
        globally for an enterprise and apply to all users, regardless of location.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_name: Return the list of dial plans matching the dial plan name.
        :type dial_plan_name: str
        :param route_group_name: Return the list of dial plans matching the route group name.
        :type route_group_name: str
        :param trunk_name: Return the list of dial plans matching the trunk name.
        :type trunk_name: str
        :param order: Order the dial plans according to the designated fields. Available sort fields: name, routeName,
            routeType. Sort order is ascending by default
        :type order: str
        :param org_id: List dial plans for this organization.
        :type org_id: str
        :return:
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i and v is not None and p != 'params')
        url = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=DialPlan, params=params, item_key='dialPlans')]

    async def create(self, name: str, route_id: str, route_type: RouteType, dial_patterns: List[str] = None,
               org_id: str = None) -> CreateResponse:
        """
        Create a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Creating a dial plan requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param name: A unique name for the dial plan.
        :type name: str
        :param route_id: ID of route type associated with the dial plan.
        :type route_id: str
        :param route_type: Route Type associated with the dial plan.
        :type route_type: :class:`wxc_sdk.common.RouteType`
        :param dial_patterns: An Array of dial patterns
        :type dial_patterns: list[str]
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :return: result of dial plan creation
        :rtype: :class:`CreateResponse`
        """
        url = self.ep()
        params = org_id and {'orgId': org_id} or None
        body = {
            'name': name,
            'routeId': route_id,
            'routeType': route_type.value if isinstance(route_type, RouteType) else route_type,
            'dialPatterns': dial_patterns or []
        }
        data = await self.post(url=url, params=params, json=body)
        return CreateResponse.parse_obj(data)

    async def details(self, dial_plan_id: str, org_id: str = None) -> DialPlan:
        """
        Get a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Retrieving a dial plan requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_id: ID of the dial plan.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        :return: dial plan details
        :rtype: :class:`DialPlan`
        """
        url = self.ep(dial_plan_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url=url, params=params)
        dp: DialPlan = DialPlan.parse_obj(data)
        dp.dial_plan_id = dial_plan_id
        return dp

    async def update(self, update: DialPlan, org_id: str = None):
        """
        Modify a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Modifying a dial plan requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param update: DialPlan objects with updated settings. Only name, route_id and route_type are considered. All
            three need to be set
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        url = self.ep(update.dial_plan_id)
        params = org_id and {'orgId': org_id} or None
        body = update.json(include={'name', 'route_id', 'route_type'})
        await self.put(url=url, params=params, data=body)

    async def delete_dial_plan(self, dial_plan_id: str, org_id: str = None):
        """
        Delete a Dial Plan for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Deleting a dial plan requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param dial_plan_id: ID of the dial plan.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        url = self.ep(dial_plan_id)
        params = org_id and {'orgId': org_id} or None
        await self.delete(url=url, params=params)

    def patterns_gen(self, dial_plan_id: str, org_id: str = None,
                 dial_pattern: str = None, **params) -> AsyncGenerator[str, None, None]:
        """
        List all Dial Patterns for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_id: ID of the dial plan.
        :type dial_plan_id: str
        :param org_id: List dial patterns associated with a dial plan.
        :type org_id: str
        :param dial_pattern: An enterprise dial pattern is represented by a sequence of digits (1-9), followed by
            optional wildcard characters. Valid wildcard characters are ! (matches any sequence of digits) and
            X (matches a single digit, 0-9).
            The ! wildcard can only occur once at the end and only in an E.164 pattern
        :return: list of patterns
        :rtype: list[str]
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i > 1 and v is not None and p != 'params')
        url = self.ep(f'{dial_plan_id}/dialPatterns')

        return self.session.follow_pagination(url=url, params=params, item_key='dialPatterns')

    async def patterns(self, dial_plan_id: str, org_id: str = None,
                 dial_pattern: str = None, **params) -> List[str]:
        """
        List all Dial Patterns for the organization.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param dial_plan_id: ID of the dial plan.
        :type dial_plan_id: str
        :param org_id: List dial patterns associated with a dial plan.
        :type org_id: str
        :param dial_pattern: An enterprise dial pattern is represented by a sequence of digits (1-9), followed by
            optional wildcard characters. Valid wildcard characters are ! (matches any sequence of digits) and
            X (matches a single digit, 0-9).
            The ! wildcard can only occur once at the end and only in an E.164 pattern
        :return: list of patterns
        :rtype: list[str]
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i > 1 and v is not None and p != 'params')
        url = self.ep(f'{dial_plan_id}/dialPatterns')

        return [o async for o in self.session.follow_pagination(url=url, params=params, item_key='dialPatterns')]

    async def modify_patterns(self, dial_plan_id: str, dial_patterns: List[PatternAndAction], org_id: str = None):
        """
        Modify dial patterns for the Dial Plan.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Modifying a dial pattern requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param dial_plan_id: ID of the dial plan being modified.
        :type dial_plan_id: str
        :param dial_patterns: Array of dial patterns to add or delete. Dial Pattern that is not present in the
            request is not modified.
        :type dial_patterns: :class:`PatternAndAction`
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        url = self.ep(f'{dial_plan_id}/dialPatterns')
        params = org_id and {'orgId': org_id} or None

        class Body(ApiModel):
            dial_patterns: list[PatternAndAction]

        body = Body(dial_patterns=dial_patterns).json()
        await self.put(url=url, params=params, data=body)

    async def delete_all_patterns(self, dial_plan_id: str, org_id: str = None):
        """
        Delete all dial patterns from the Dial Plan.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Deleting dial pattern requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param dial_plan_id: ID of the dial plan being modified.
        :type dial_plan_id: str
        :param org_id: Organization to which dial plan belongs.
        :type org_id: str
        """
        url = self.ep(f'{dial_plan_id}/dialPatterns')
        params = org_id and {'orgId': org_id} or None
        body = {'deleteAllDialPatterns': True}
        await self.put(url=url, params=params, json=body)


class AsRouteGroupApi(AsApiChild, base='telephony/config/premisePstn/routeGroups'):
    """
    API for everything route groups
    """

    def list_gen(self, name: str = None, order: str = None,
             org_id: str = None, **params) -> AsyncGenerator[RouteGroup, None, None]:
        """
        List all Route Groups for an organization. A Route Group is a group of trunks that allows further scale and
        redundancy with the connection to the premises.

        Retrieving this route group list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of route groups matching the route group name.
        :type name: st
        :param order: Order the route groups according to designated fields. Available sort orders: asc, desc.
        :type order: str
        :param org_id: List route groups for this organization.
        :type org_id: str
        :return: generator of :class:`RouteGroup` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params, model=RouteGroup)

    async def list(self, name: str = None, order: str = None,
             org_id: str = None, **params) -> List[RouteGroup]:
        """
        List all Route Groups for an organization. A Route Group is a group of trunks that allows further scale and
        redundancy with the connection to the premises.

        Retrieving this route group list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of route groups matching the route group name.
        :type name: st
        :param order: Order the route groups according to designated fields. Available sort orders: asc, desc.
        :type order: str
        :param org_id: List route groups for this organization.
        :type org_id: str
        :return: generator of :class:`RouteGroup` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, params=params, model=RouteGroup)]

    async def create(self, route_group: RouteGroup, org_id: str = None) -> str:
        """
        Creates a Route Group for the organization.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Creating a Route Group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param route_group: settings for new route group. name and local_gateways need to be set. For each LGW
            id and priority need to be set.
            Example:

            .. code-block:: python

                rg = RouteGroup(name=rg_name,
                        local_gateways=[RGTrunk(trunk_id=trunk.trunk_id,
                                                priority=1)])
                rg_id = api.telephony.prem_pstn.route_group.create(route_group=rg)
        :type route_group: :class:`RouteGroup`
        :param org_id:
        :type org_id: str
        :return: id of new route group
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        body = route_group.json(include={'name': True,
                                         'local_gateways': {'__all__': {'trunk_id', 'priority'}}})
        url = self.ep()
        data = await self.post(url=url, params=params, data=body)
        return data['id']

    async def details(self, rg_id: str, org_id: str = None) -> RouteGroup:
        """
        Reads a Route Group for the organization based on id.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Reading a Route Group requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route Group for which details are being requested.
        :type rg_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :return: route group details
        :rtype: :class:`RouteGroup`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rg_id)
        data = await self.get(url=url, params=params)
        return RouteGroup.parse_obj(data)

    async def update(self, rg_id: str, update: RouteGroup, org_id: str = None):
        """
        Modifies an existing Route Group for an organization based on id.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Modifying a Route Group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rg_id: route group to be modified
        :type rg_id: str
        :param update: new settings
        :type update: :class:`RouteGroup`
        :param org_id: Organization of the Route Group.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        body = update.json(include={'name': True,
                                    'local_gateways': {'__all__': {'trunk_id', 'priority'}}})
        url = self.ep(rg_id)
        data = await self.post(url=url, params=params, data=body)
        await self.put(url=url, params=params, data=data)

    async def delete_route_group(self, rg_id: str, org_id: str = None):
        """
        Remove a Route Group from an Organization based on id.

        A Route Group is a collection of trunks that allows further scale and redundancy with the connection to the
        premises. Route groups can include up to 10 trunks from different locations.

        Removing a Route Group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rg_id: Route Group to be deleted
        :type rg_id: str
        :param org_id: Organization of the Route Group.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rg_id)
        await self.delete(url=url, params=params)

    async def usage(self, rg_id: str, org_id: str = None) -> RouteGroupUsage:
        """
        List the number of "Call to" on-premises Extensions, Dial Plans, PSTN Connections, and Route Lists used by a
        specific Route Group. Users within Call to Extension locations are registered to a PBX which allows you to
        route unknown extensions (calling number length of 2-6 digits) to the PBX using an existing Trunk or Route
        Group. PSTN Connections may be cisco PSTN, cloud-connected PSTN, or premises-based PSTN (local gateway).
        Dial Plans allow you to route calls to on-premises extensions via your trunk or route group. Route Lists are
        a list of numbers that can be reached via a route group. It can be used to provide cloud PSTN connectivity to
        Webex Calling Dedicated Instance.

        Retrieving usage information requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :type rg_id: str
        :param org_id: Organization associated with specific route group
        :type org_id: str
        :return: usage information
        :rtype: :class:`RouteGroupUsage`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{rg_id}/usage')
        data = await self.get(url=url, params=params)
        return RouteGroupUsage.parse_obj(data)

    def usage_call_to_extension_gen(self, rg_id: str, org_id: str = None, **params) -> AsyncGenerator[IdAndName, None, None]:
        """
        List "Call to" on-premises Extension Locations for a specific route group. Users within these locations are
        registered to a PBX which allows you to route unknown extensions (calling number length of 2-6 digits) to
        the PBX using an existing trunk or route group.

        Retrieving this location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageCallToExtension')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    async def usage_call_to_extension(self, rg_id: str, org_id: str = None, **params) -> List[IdAndName]:
        """
        List "Call to" on-premises Extension Locations for a specific route group. Users within these locations are
        registered to a PBX which allows you to route unknown extensions (calling number length of 2-6 digits) to
        the PBX using an existing trunk or route group.

        Retrieving this location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageCallToExtension')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params)]

    def usage_dial_plan_gen(self, rg_id: str, org_id: str = None, **params) -> AsyncGenerator[IdAndName, None, None]:
        """
        List Dial Plan Locations for a specific route group.

        Dial Plans allow you to route calls to on-premises destinations by use of trunks or route groups. They are
        configured globally for an enterprise and apply to all users, regardless of location. A Dial Plan also
        specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Retrieving this location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageDialPlan')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    async def usage_dial_plan(self, rg_id: str, org_id: str = None, **params) -> List[IdAndName]:
        """
        List Dial Plan Locations for a specific route group.

        Dial Plans allow you to route calls to on-premises destinations by use of trunks or route groups. They are
        configured globally for an enterprise and apply to all users, regardless of location. A Dial Plan also
        specifies the routing choice (trunk or route group) for calls that match any of its dial patterns.
        Specific dial patterns can be defined as part of your dial plan.

        Retrieving this location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageDialPlan')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params)]

    def usage_location_pstn_gen(self, rg_id: str, org_id: str = None, **params) -> AsyncGenerator[IdAndName, None, None]:
        """
        List PSTN Connection Locations for a specific route group. This solution lets you configure users to use Cloud
        PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this Location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usagePstnConnection')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    async def usage_location_pstn(self, rg_id: str, org_id: str = None, **params) -> List[IdAndName]:
        """
        List PSTN Connection Locations for a specific route group. This solution lets you configure users to use Cloud
        PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this Location list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usagePstnConnection')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params)]

    def usage_route_lists_gen(self, rg_id: str, org_id: str = None, **params) -> AsyncGenerator[UsageRouteLists, None, None]:
        """
        List Route Lists for a specific route group. Route Lists are a list of numbers that can be reached via a
        Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.

        Retrieving this list of Route Lists requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageRouteList')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=UsageRouteLists, params=params)

    async def usage_route_lists(self, rg_id: str, org_id: str = None, **params) -> List[UsageRouteLists]:
        """
        List Route Lists for a specific route group. Route Lists are a list of numbers that can be reached via a
        Route Group. It can be used to provide cloud PSTN connectivity to Webex Calling Dedicated Instance.

        Retrieving this list of Route Lists requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rg_id: Route group requested for information.
        :param org_id: Organization associated with specific route group.
        :return: generator of instances
        :rtype: :class:`wxc_sdk.common.IdAndName`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'rg_id', 'params'})
        url = self.ep(f'{rg_id}/usageRouteList')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=UsageRouteLists, params=params)]


class AsRouteListApi(AsApiChild, base='telephony/config/premisePstn/routeLists'):
    """
    API for everything route lists
    """

    def list_gen(self, name: list[str] = None, location_id: list[str] = None, order: str = None,
             org_id: str = None, **params) -> AsyncGenerator[RouteList, None, None]:
        """
        List all Route Lists for the organization.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving the Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of Route List matching the route list name.
        :type name: str
        :param location_id: Return the list of Route Lists matching the location id.
        :type location_id: str
        :param order: Order the Route List according to the designated fields.Available sort fields: name, locationId.
            Sort order is ascending by default
        :type order: str
        :param org_id: List all Route List for this organization.
        :type org_id: str
        :return: generator yielding :class:`RouteList` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params, model=RouteList)

    async def list(self, name: list[str] = None, location_id: list[str] = None, order: str = None,
             org_id: str = None, **params) -> List[RouteList]:
        """
        List all Route Lists for the organization.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving the Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of Route List matching the route list name.
        :type name: str
        :param location_id: Return the list of Route Lists matching the location id.
        :type location_id: str
        :param order: Order the Route List according to the designated fields.Available sort fields: name, locationId.
            Sort order is ascending by default
        :type order: str
        :param org_id: List all Route List for this organization.
        :type org_id: str
        :return: generator yielding :class:`RouteList` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, params=params, model=RouteList)]

    async def create(self, name: str, location_id: str, rg_id: str, org_id: str = None) -> str:
        """
        Create a Route List for the organization.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Creating a Route List requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param name: Name of the Route List
        :type name: str
        :param location_id: Location associated with the Route List.
        :type location_id: str
        :param rg_id: UUID of the route group associated with Route List.
        :type rg_id: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: ID of the newly route list created.
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        body = {'name': name,
                'locationId': location_id,
                'routeGroupId': rg_id}
        url = self.ep()
        data = await self.post(url=url, params=params, json=body)
        return data['id']

    async def details(self, rl_id: str, org_id: str = None) -> RouteListDetail:
        """
        Get Route List Details.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param rl_id: ID of the Route List.
        :type rl_id: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: route list details
        :rtype: :class:`RouteListDetail`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rl_id)
        data = await self.get(url=url, params=params)
        return RouteListDetail.parse_obj(data)

    async def update(self, rl_id: str, name: str, rg_id: str, org_id: str = None):
        """
        Modify the details for a Route List.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: ID of the Route List.
        :type rl_id: str
        :param name: Route List new name.
        :type name: str
        :param rg_id: New route group id.
        :type rg_id: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        body = {'name': name,
                'routeGroupId': rg_id}
        url = self.ep(rl_id)
        await self.put(url=url, params=params, json=body)

    async def delete_route_list(self, rl_id: str, org_id: str = None):
        """
        Delete Route List for a Customer

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Deleting a Route List requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: ID of the Route List.
        :type rl_id: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(rl_id)
        await self.delete(url=url, params=params)

    def numbers_gen(self, rl_id: str, order: str = None, number: str = None,
                org_id: str = None, **params) -> AsyncGenerator[str, None, None]:
        """
        Get numbers assigned to a Route List

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: ID of the Route List.
        :type rl_id: str
        :param order: Order the Route Lists according to number.
        :type order: str
        :param number: Number assigned to the route list.
        :type number: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: generator yielding str
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params', 'rl_id'})
        url = self.ep(f'{rl_id}/numbers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params)

    async def numbers(self, rl_id: str, order: str = None, number: str = None,
                org_id: str = None, **params) -> List[str]:
        """
        Get numbers assigned to a Route List

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: ID of the Route List.
        :type rl_id: str
        :param order: Order the Route Lists according to number.
        :type order: str
        :param number: Number assigned to the route list.
        :type number: str
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: generator yielding str
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params', 'rl_id'})
        url = self.ep(f'{rl_id}/numbers')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, params=params)]

    async def update_numbers(self, rl_id: str, numbers: List[NumberAndAction],
                       org_id: str = None) -> List[UpdateNumbersResponse]:
        """
        Modify numbers for a specific Route List of a Customer.

        A Route List is a list of numbers that can be reached via a Route Group. It can be used to provide cloud PSTN
        connectivity to Webex Calling Dedicated Instance.

        Retrieving a Route List requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param rl_id: ID of the Route List.
        :type rl_id: str
        :param numbers: Array of the numbers to be deleted/added.
        :type numbers: list[:class:`NumberAndAction`]
        :param org_id: Organization to which Route List belongs.
        :type org_id: str
        :return: list of update number status
        :rtype: list[:class:`UpdateNumbersResponse`]
        """
        url = self.ep(f'{rl_id}/numbers')
        params = org_id and {'orgId': org_id} or None

        class Body(ApiModel):
            numbers: list[NumberAndAction]

        body = Body(numbers=numbers).json()
        data = await self.put(url=url, params=params, data=body)
        if data:
            return parse_obj_as(list[UpdateNumbersResponse], data['numberStatus'])
        else:
            return []

    async def delete_all_numbers(self, rl_id: str, org_id: str = None):
        url = self.ep(f'{rl_id}/numbers')
        params = org_id and {'orgId': org_id} or None
        body = {'deleteAllNumbers': True}
        await self.put(url=url, params=params, json=body)


class AsTrunkApi(AsApiChild, base='telephony/config/premisePstn/trunks'):
    """
    API for everything trunks
    """

    def list_gen(self, name: str = None, location_name: str = None, trunk_type: str = None, order: str = None,
             org_id: str = None, **params) -> AsyncGenerator[Trunk, None, None]:
        """
        List all Trunks for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        ebex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of trunks matching the local gateway names.
        :type name: str
        :param location_name: Return the list of trunks matching the location names.
        :type location_name: str
        :param trunk_type: Return the list of trunks matching the trunk type.
        :type trunk_type: str
        :param order: Order the trunks according to the designated fields. Available sort fields: name, locationName.
            Sort order is ascending by default
        :type order: str
        :param org_id:
        :type org_id: str
        :return: generator of Trunk instances
        :rtype: :class:`Trunk`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, params=params, model=Trunk, item_key='trunks')

    async def list(self, name: str = None, location_name: str = None, trunk_type: str = None, order: str = None,
             org_id: str = None, **params) -> List[Trunk]:
        """
        List all Trunks for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        ebex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param name: Return the list of trunks matching the local gateway names.
        :type name: str
        :param location_name: Return the list of trunks matching the location names.
        :type location_name: str
        :param trunk_type: Return the list of trunks matching the trunk type.
        :type trunk_type: str
        :param order: Order the trunks according to the designated fields. Available sort fields: name, locationName.
            Sort order is ascending by default
        :type order: str
        :param org_id:
        :type org_id: str
        :return: generator of Trunk instances
        :rtype: :class:`Trunk`
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if v is not None and p not in {'self', 'params'})
        url = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, params=params, model=Trunk, item_key='trunks')]

    async def create(self, name: str, location_id: str, password: str, trunk_type: TrunkType = TrunkType.registering,
               dual_identity_support_enabled: bool = None, device_type: TrunkDeviceType = None, address: str = None,
               domain: str = None, port: int = None, max_concurrent_calls: int = None, org_id: str = None) -> str:
        """
        Create a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Creating a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param name: A unique name for the trunk.
        :type name: str
        :param location_id: ID of location associated with the trunk.
        :type location_id: str
        :param password: A password to use on the trunk.
        :type password: str
        :param trunk_type: Trunk Type associated with the trunk.
        :type trunk_type: :class:`TrunkType`
        :param dual_identity_support_enabled: Dual Identity Support setting impacts the handling of the From header
            and P-Asserted-Identity header when sending an initial SIP INVITE to the trunk for an outbound call.
        :type dual_identity_support_enabled: bool
        :param device_type: Device type associated with trunk.
        :type device_type: :class:`TrunkDeviceType`
        :param address: FQDN or SRV address. Required to create a static certificate-based trunk.
        :type address: str
        :param domain: Domain name. Required to create a static certificate based trunk.
        :type domain: str
        :param port: FQDN port. Required to create a static certificate-based trunk.
        :type port: int
        :param max_concurrent_calls: Max Concurrent call. Required to create a static certificate based trunk.
        :type max_concurrent_calls: int
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id of new trunk
        :rtype: str
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'org_id'} and v is not None}
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = await self.post(url=url, params=params, json=body)
        return data['id']

    async def details(self, trunk_id: str, org_id: str = None) -> TrunkDetail:
        """
        Get a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving a trunk requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: trunk details
        :rtype: :class:`TrunkDetail`
        """
        url = self.ep(trunk_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url=url, params=params)
        return TrunkDetail.parse_obj(data)

    async def update(self, trunk_id: str, name: str, location_id: str, password: str, trunk_type: TrunkType,
               dual_identity_support_enabled: bool = None, max_concurrent_calls: int = None, org_id: str = None):
        """
        Modify a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Modifying a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param trunk_id:
        :type name: str
        :param location_id: ID of location associated with the trunk.
        :type location_id: str
        :param password: A password to use on the trunk.
        :type password: str
        :param trunk_type: Trunk Type associated with the trunk.
        :type trunk_type: :class:`TrunkType`
        :param dual_identity_support_enabled: Dual Identity Support setting impacts the handling of the From header
            and P-Asserted-Identity header when sending an initial SIP INVITE to the trunk for an outbound call.
        :type dual_identity_support_enabled: bool
        :param max_concurrent_calls: Max Concurrent call. Required to create a static certificate based trunk.
        :type max_concurrent_calls: int
        :param org_id: Organization to which trunk belongs.
        :type org_id: str:return:
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'org_id'} and v is not None}
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        await self.put(url=url, params=params, json=body)

    async def delete_trunk(self, trunk_id: str, org_id: str = None):
        """
        Delete a Trunk for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Deleting a trunk requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        """
        url = self.ep(trunk_id)
        params = org_id and {'orgId': org_id} or None
        await self.delete(url=url, params=params)

    async def trunk_types(self, org_id: str = None) -> List[TrunkTypeWithDeviceType]:
        """
        List all TrunkTypes with DeviceTypes for the organization.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy. Trunk Types are Registering
        or Certificate Based and are configured in CallManager.

        Retrieving trunk types requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id:
        :return: trunk types
        :rtype: list[:class:`TrunkTypeWithDeviceType`]
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep('trunkTypes')
        data = await self.get(url=ep, params=params)
        return parse_obj_as(list[TrunkTypeWithDeviceType], data['trunkTypes'])

    async def usage(self, trunk_id: str, org_id: str = None) -> TrunkUsage:
        """
        Get Local Gateway Usage Count

        A trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: usage counts
        :rtype: :class:`TrunkUsage`
        """
        url = self.ep(f'{trunk_id}/usage')
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url=url, params=params)
        return TrunkUsage.parse_obj(data)

    def usage_dial_plan_gen(self, trunk_id: str, org_id: str = None) -> AsyncGenerator[IdAndName, None, None]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usageDialPlan')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    async def usage_dial_plan(self, trunk_id: str, org_id: str = None) -> List[IdAndName]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usageDialPlan')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params)]

    def usage_location_pstn_gen(self, trunk_id: str, org_id: str = None) -> AsyncGenerator[IdAndName, None, None]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with
        a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks
        that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usagePstnConnection')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    async def usage_location_pstn(self, trunk_id: str, org_id: str = None) -> List[IdAndName]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with
        a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks
        that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usagePstnConnection')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params)]

    def usage_route_group_gen(self, trunk_id: str, org_id: str = None) -> AsyncGenerator[IdAndName, None, None]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usageRouteGroup')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=IdAndName, params=params)

    async def usage_route_group(self, trunk_id: str, org_id: str = None) -> List[IdAndName]:
        """
        Get Local Gateway Dial Plan Usage for a Trunk.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Retrieving this information requires a full administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param trunk_id: ID of the trunk.
        :type trunk_id: str
        :param org_id: Organization to which trunk belongs.
        :type org_id: str
        :return: id and name objects
        """
        params = {to_camel(p): v for p, v in locals().items()
                  if v is not None and p not in {'self', 'trunk_id'}}
        url = self.ep(f'{trunk_id}/usageRouteGroup')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params)]

    async def validate_fqdn_and_domain(self, address: str, domain: str, port: int = None, org_id: str = None):
        """
        Validate Local Gateway FQDN and Domain for the organization trunks.

        A Trunk is a connection between Webex Calling and the premises, which terminates on the premises with a local
        gateway or other supported device. The trunk can be assigned to a Route Group - a group of trunks that allow
        Webex Calling to distribute calls over multiple trunks or to provide redundancy.

        Validating Local Gateway FQDN and Domain requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param address: FQDN or SRV address of the trunk.
        :type address: str
        :param domain: Domain name of the trunk.
        :type domain: str
        :param port: FQDN port of the trunk
        :type port: int
        :param org_id: Organization to which trunk types belongs.
        :type org_id: str
        """
        body = {p: v for p, v in locals().items()
                if p not in {'self', 'org_id'} and v is not None}
        url = self.ep('actions/fqdnValidation/invoke')
        params = org_id and {'orgId': org_id} or None
        await self.post(url=url, params=params, json=body)

    # TODO: are we missing a usage for trunks used for calls to unknown extensions??


class AsPremisePstnApi(AsApiChild, base='telephony/config/premisePstn'):
    """
    Premises PSTN API
    """
    #: dial plan configuration
    dial_plan: AsDialPlanApi
    #: trunk configuration
    trunk: AsTrunkApi
    #: route group configuration
    route_group: AsRouteGroupApi
    #: route list configuration
    route_list: AsRouteListApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.dial_plan = AsDialPlanApi(session=session)
        self.trunk = AsTrunkApi(session=session)
        self.route_group = AsRouteGroupApi(session=session)
        self.route_list = AsRouteListApi(session=session)

    async def validate_pattern(self, dial_patterns: Union[str, List[str]], org_id: str = None) -> DialPatternValidationResult:
        """
        Validate a Dial Pattern.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Validating a dial pattern requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param dial_patterns: Array of dial patterns.
        :type dial_patterns: list[str] or str
        :param org_id: Organization to which dial plan belongs.
        :return: validation result
        :rtype: :class:`DialPatternValidationResult`
        """
        if isinstance(dial_patterns, str):
            dial_patterns = [dial_patterns]

        url = self.ep('actions/validateDialPatterns/invoke')
        params = org_id and {'orgId': org_id} or None
        body = {'dialPatterns': dial_patterns}
        data = await self.post(url=url, params=params, json=body)
        return DialPatternValidationResult.parse_obj(data)


class AsPrivateNetworkConnectApi(AsApiChild, base='telephony/config/locations'):
    """
    API for location private network connect API settings
    """

    async def read(self, location_id: str, org_id: str = None) -> NetworkConnectionType:
        """
        Get Private Network Connect

        Retrieve the location's network connection type.

        Network Connection Type determines if the location's network connection is public or private.

        Retrieving location's network connection type requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve network connection type for this location.
        :type location_id: str
        :param org_id: Retrieve network connection type for this organization.
        :type org_id: str
        :return: location PNC settings
        :rtype: NetworkConnectionType
        """
        params = org_id and {'orgId': org_id} or None
        url = self.session.ep(f'telephony/config/locations/{location_id}/privateNetworkConnect')
        data = await self.get(url, params=params)
        return parse_obj_as(NetworkConnectionType, data['networkConnectionType'])

    async def update(self, location_id: str, connection_type: NetworkConnectionType, org_id: str = None):
        """
        Get Private Network Connect

        Retrieve the location's network connection type.

        Network Connection Type determines if the location's network connection is public or private.

        Retrieving location's network connection type requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Update network connection type for this location.
        :type location_id: str
        :param connection_type: Network Connection Type for the location.
        :type connection_type: NetworkConnectionType
        :param org_id: Update network connection type for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.session.ep(f'telephony/config/locations/{location_id}/privateNetworkConnect')
        body = {'networkConnectionType': connection_type.value}
        await self.put(url, json=body, params=params)


class AsTelephonyDevicesApi(AsApiChild, base='telephony/config/devices'):
    """
    Telephony devices API
    """

    async def members(self, device_id: str, org_id: str = None) -> DeviceMembersResponse:
        """
        Get Device Members

        Get the list of all the members of the device including primary and secondary users.

        A device member can be either a person or a workspace. An admin can access the list of member details, modify
        member details and search for available members on a device.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Retrieves the list of all members of the device in this Organization.
        :type org_id: str
        :return: Device model, line count, and members
        :rtype: DeviceMembersResponse
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{device_id}/members')
        data = await self.get(url=url, params=params)
        return DeviceMembersResponse.parse_obj(data)

    async def update_members(self, device_id: str, members: Optional[list[Union[DeviceMember, AvailableMember]]],
                       org_id: str = None):
        """
        Modify member details on the device.

        A device member can be either a person or a workspace. An admin can access the list of member details,
        modify member details and search for available members on a device.

        Modifying members on the device requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param members: New member details for the device. If the member's list is missing then all the users are
            removed except the primary user.
        :type members: list[Union[DeviceMember, AvailableMember]
        :param org_id: Modify members on the device in this organization.
        :type org_id: str
        """
        members_for_update = []
        for member in members:
            if isinstance(member, AvailableMember):
                member = DeviceMember.from_available(member)
            else:
                member = member.copy(deep=True)
            members_for_update.append(member)

        if members_for_update:
            # now assign port indices
            port = 1
            for member in members_for_update:
                member.port = port
                port += member.line_weight

        # create body
        if members_for_update:
            members = ','.join(m.json(include={'member_id', 'port', 't38_fax_compression_enabled', 'primary_owner',
                                               'line_type', 'line_weight', 'hotline_enabled', 'hotline_destination',
                                               'allow_call_decline_enabled'})
                               for m in members_for_update)
            body = f'{{"members": [{members}]}}'
        else:
            body = None

        url = self.ep(f'{device_id}/members')
        params = org_id and {'orgId': org_id} or None
        await self.put(url=url, data=body, params=params)

    def available_members_gen(self, device_id: str, location_id: str, member_name: str = None, phone_number: str = None,
                          extension: str = None, org_id: str = None,
                          **params) -> AsyncGenerator[AvailableMember, None, None]:
        """
        Search members that can be assigned to the device.

        A device member can be either a person or a workspace. A admin can access the list of member details,
        modify member details and search for available members on a device.

        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param location_id: Search (Contains) based on number.
        :type location_id: str
        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param extension: Search (Contains) based on extension.
        :type extension: str
        :param org_id: Retrieves the list of available members on the device in this Organization.
        :type org_id: str
        :return: list of available members
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if p not in {'self', 'params', 'device_id'} and v is not None)
        url = self.ep(f'{device_id}/availableMembers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=AvailableMember, params=params, item_key='members')

    async def available_members(self, device_id: str, location_id: str, member_name: str = None, phone_number: str = None,
                          extension: str = None, org_id: str = None,
                          **params) -> List[AvailableMember]:
        """
        Search members that can be assigned to the device.

        A device member can be either a person or a workspace. A admin can access the list of member details,
        modify member details and search for available members on a device.

        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param location_id: Search (Contains) based on number.
        :type location_id: str
        :param member_name: Search (Contains) numbers based on member name.
        :type member_name: str
        :param phone_number: Search (Contains) based on number.
        :type phone_number: str
        :param extension: Search (Contains) based on extension.
        :type extension: str
        :param org_id: Retrieves the list of available members on the device in this Organization.
        :type org_id: str
        :return: list of available members
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if p not in {'self', 'params', 'device_id'} and v is not None)
        url = self.ep(f'{device_id}/availableMembers')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=AvailableMember, params=params, item_key='members')]

    async def apply_changes(self, device_id: str, org_id: str = None):
        """
        Apply Changes for a specific device

        Issues request to the device to download and apply changes to the configuration.

        Applying changes for a specific device requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.
        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param org_id: Apply changes for a device in this Organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{device_id}/actions/applyChanges/invoke')
        await self.post(url=url, params=params)

    async def device_settings(self, device_id: str, device_model: str, org_id: str = None) -> DeviceCustomization:
        """
        Get override settings for a device.

        Device settings lists all the applicable settings for an MPP and an ATA devices at the device level. An admin
        can also modify the settings. DECT devices do not support settings at the device level.

        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param device_model: Model type of the device.
        :type device_model: str
        :param org_id: Settings on the device in this organization.
        :type org_id: str
        :return: Device settings
        :rtype: DeviceCustomization
        """
        params = {'model': device_model}
        if org_id:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}/settings')
        data = await self.get(url=url, params=params)
        return DeviceCustomization.parse_obj(data)

    async def update_device_settings(self, device_id: str, device_model: str, customization: DeviceCustomization,
                               org_id: str = None):
        """
        Modify override settings for a device.

        Device settings list all the applicable settings for an MPP and an ATA devices at the device level. Admins
        can also modify the settings. NOTE: DECT devices do not support settings at the device level.

        Updating settings on the device requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param device_id: Unique identifier for the device.
        :type device_id: str
        :param device_model: Device model name.
        :type device_model: str
        :param customization: Indicates the customization object of the device settings.
        :type customization: DeviceCustomization
        :param org_id: Organization in which the device resides..
        :type org_id: str

        Example :

            .. code-block:: python

                # target_device is a TelephonyDevice object
                target_device: TelephonyDevice

                # get device level settings
                settings = api.telephony.devices.device_settings(device_id=target_device.device_id,
                                                                 device_model=target_device.model)

                # update settings (display name format) and enable device level customization
                settings.customizations.mpp.display_name_format = DisplayNameSelection.person_last_then_first_name
                settings.custom_enabled = True

                # update the device level settings
                api.telephony.devices.update_device_settings(device_id=target_device.device_id,
                                                             device_model=target_device.model,
                                                             customization=settings)

                # apply changes to device
                api.telephony.devices.apply_changes(device_id=target_device.device_id)

        """
        params = {'model': device_model}
        if org_id:
            params['orgId'] = org_id
        url = self.ep(f'{device_id}/settings')
        body = customization.json(include={'customizations', 'custom_enabled'})
        await self.put(url=url, params=params, data=body)

    async def dect_devices(self, org_id: str = None) -> list[DectDevice]:
        """
        Read the DECT device type list

        Get DECT device type list with base stations and line ports supported count. This is a static list.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id:
        :return:
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep('dects/supportedDevices')
        data = await self.get(url=url, params=params)
        return parse_obj_as(list[DectDevice], data['devices'])

    async def validate_macs(self, macs: list[str], org_id: str = None) -> MACValidationResponse:
        """
        Validate a list of MAC addresses.

        Validating this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param macs: MAC addresses to be validated.
        :type macs: list[str]
        :param org_id: Validate the mac address(es) for this organization.
        :type org_id: str
        :return: validation response
        :rtype: :class:`MACValidationResponse`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep('actions/validateMacs/invoke')
        data = await self.post(url=url, params=params, json={'macs': macs})
        return MACValidationResponse.parse_obj(data)


class AsInternalDialingApi(AsApiChild, base='telephony/config/locations'):
    """
    Internal dialing settings for location
    """

    def url(self, location_id: str) -> str:
        return super().ep(f'{location_id}/internalDialing')

    async def read(self, location_id: str, org_id: str = None) -> InternalDialing:
        """
        Get current configuration for routing unknown extensions to the Premises as internal calls

        If some users in a location are registered to a PBX, retrieve the setting to route unknown extensions (digits
        that match the extension length) to the PBX.

        Retrieving the internal dialing configuration requires a full or read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: location for which internal calling configuration is being requested
        :type location_id: str
        :param org_id:
        :type org_id: str
        :return: settings
        :rtype: :class:`InternalDialing`
        """
        url = self.url(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url=url, params=params)
        return InternalDialing.parse_obj(data)

    async def update(self, location_id: str, update: InternalDialing, org_id: str = None):
        """
        Modify current configuration for routing unknown extensions to the Premises as internal calls

        If some users in a location are registered to a PBX, enable the setting to route unknown extensions (digits
        that match the extension length) to the PBX.

        Editing the internal dialing configuration requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: location for which internal calling configuration is being requested
        :type location_id: str
        :param update: new settings
        :type update: :class:`InternalDialing`
        :param org_id:
        :type org_id: str
        """
        url = self.url(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = update.json(exclude_none=False)
        await self.put(url=url, params=params, data=data)


class AsLocationMoHApi(AsApiChild, base='telephony/config/locations'):
    """
    Access codes API
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific feature endpoint like
        /v1/telephony/config/locations/{locationId}/musicOnHold

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/musicOnHold{path}')
        return ep

    async def read(self, location_id: str, org_id: str = None) -> LocationMoHSetting:
        """
        Get Music On Hold

        Retrieve the location's music on hold settings.

        Location's music on hold settings allows you to play music when a call is placed on hold or parked.

        Retrieving location's music on hold settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        :return: MoH settings
        :rtype: :class:`LocationMoHSetting`
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        data = await self.get(url, params=params)
        return LocationMoHSetting.parse_obj(data)

    async def update(self, location_id: str, settings: LocationMoHSetting, org_id: str = None) -> LocationMoHSetting:
        """
        Get Music On Hold

        Retrieve the location's music on hold settings.

        Location's music on hold settings allows you to play music when a call is placed on hold or parked.

        Retrieving location's music on hold settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param settings: new settings
        :type settings: :class:`LocationMoHSetting`
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        :return: list of :class:`wxc_sdk.common.CallPark`
        """
        params = org_id and {'orgId': org_id} or None
        data = settings.json()
        url = self._endpoint(location_id=location_id)
        await self.put(url, params=params, data=data)

    async def create(self, location_id: str, access_codes: list[AuthCode], org_id: str = None) -> list[AuthCode]:
        """

        :param location_id: Add new access code for this location.
        :type location_id: str
        :param access_codes: Access code details
        :type access_codes: list of :class:`wxc_sdk.common.AuthCode`
        :param org_id: Add new access code for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = {'accessCodes': [json.loads(ac.json()) for ac in access_codes]}
        await self.post(url, json=body, params=params)

    async def delete_codes(self, location_id: str, access_codes: list[Union[str, AuthCode]],
                     org_id: str = None) -> list[AuthCode]:
        """
        Delete Access Code Location

        Deletes the access code details for a particular location for a customer.

        Use Access Codes to bypass the set permissions for all persons/workspaces at this location.

        Modifying the access code location details requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Deletes the access code details for this location.
        :type location_id: str
        :param access_codes: access codes to delete
        :type access_codes: list of :class:`wxc_sdk.common.AuthCode` or str
        :param org_id: Delete access codes from this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = {'deleteCodes': [ac.code if isinstance(ac, AuthCode) else ac
                                for ac in access_codes]}
        await self.put(url, json=body, params=params)


class AsLocationNumbersApi(AsApiChild, base='telephony/config/locations'):
    def _url(self, location_id: str, path: str = None):
        path = path and f'/{path}' or ''
        return self.ep(f'{location_id}/numbers{path}')

    async def add(self, location_id: str, phone_numbers: list[str], state: NumberState = NumberState.inactive,
            org_id: str = None):
        """
        Adds specified set of phone numbers to a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Adding a phone number to a location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: LocationId to which numbers should be added.
        :type location_id: str
        :param phone_numbers: List of phone numbers that need to be added.
        :type phone_numbers: list[str]
        :param state: State of the phone numbers.
        :type state: :class:`wxc_sdk.common.NumberState`
        :param org_id: Organization to manage
        :type org_id: str
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = {'phoneNumbers': phone_numbers,
                'state': state}
        await self.post(url=url, params=params, json=body)

    async def activate(self, location_id: str, phone_numbers: list[str], org_id: str = None):
        """
        Activate the specified set of phone numbers in a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features.
        Phone numbers must follow E.164 format for all countries, except for the United States, which can also
        follow the National format. Active phone numbers are in service.

        Activating a phone number in a location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: LocationId in which numbers should be activated.
        :type location_id: str
        :param phone_numbers: List of phone numbers to be activated.
        :type phone_numbers: list[str]
        :param org_id: Organization to manage
        :type org_id: str
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = {'phoneNumbers': phone_numbers}
        await self.put(url=url, params=params, json=body)

    async def remove(self, location_id: str, phone_numbers: list[str], org_id: str = None):
        """
        Remove the specified set of phone numbers from a location for an organization.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Removing a phone number from a location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: LocationId from which numbers should be removed.
        :type location_id: str
        :param phone_numbers: List of phone numbers to be removed.
        :type phone_numbers: list[str]
        :param org_id: Organization to manage
        :type org_id: str
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = {'phoneNumbers': phone_numbers}
        await self.delete(url=url, params=params, json=body)


class AsLocationVoicemailSettingsApi(AsApiChild, base='telephony/config/locations'):
    """
    location voicemail settings API, for now only enable/disable Vm transcription
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific
        telephony/config/locations/{locationId}/voicemail

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/voicemail{path}')
        return ep

    async def read(self, location_id: str, org_id: str = None) -> LocationVoiceMailSettings:
        """
        Get Location Voicemail

        Retrieve voicemail settings for a specific location.

        Location's voicemail settings allows you to enable voicemail transcription for a specific location.

        Retrieving location's voicemail settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.


        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        :return: location voicemail settings
        :rtype: :class:`LocationVoiceMailSettings`
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        data = await self.get(url, params=params)
        return LocationVoiceMailSettings.parse_obj(data)

    async def update(self, location_id: str, settings: LocationVoiceMailSettings, org_id: str = None):
        """
        Get Location Voicemail

        Retrieve voicemail settings for a specific location.

        Location's voicemail settings allows you to enable voicemail transcription for a specific location.

        Retrieving location's voicemail settings requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.


        :param location_id: Retrieve access codes details for this location.
        :type location_id: str
        :param settings: new settings
        :type settings: :class:`LocationVoiceMailSettings`
        :param org_id: Retrieve access codes details for a customer location in this organization
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        body = settings.json()
        await self.put(url, params=params, data=body)


class AsTelephonyLocationApi(AsApiChild, base='telephony/config/locations'):
    #: call intercept settings
    intercept: AsLocationInterceptApi
    #: internal dialing settings
    internal_dialing: AsInternalDialingApi
    #: moh settings
    moh: AsLocationMoHApi
    #: number settings
    number: AsLocationNumbersApi
    #: Location VM settings (only enable/disable transcription for now)
    voicemail: AsLocationVoicemailSettingsApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.intercept = AsLocationInterceptApi(session=session)
        self.internal_dialing = AsInternalDialingApi(session=session)
        self.moh = AsLocationMoHApi(session=session)
        self.number = AsLocationNumbersApi(session=session)
        self.voicemail = AsLocationVoicemailSettingsApi(session=session)

    async def generate_password(self, location_id: str, generate: list[str] = None, org_id: str = None):
        """
        Generates an example password using the effective password settings for the location. If you don't specify
        anything in the generate field or don't provide a request body, then you will receive a SIP password by default.

        It's used while creating a trunk and shouldn't be used anywhere else.

        Generating an example password requires a full or write-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location for which example password has to be generated.
        :type location_id: str
        :param generate: password settings array.
        :type generate: list[str]
        :param org_id: Organization to which location belongs.
        :type org_id: str
        :return: new password
        :rtype: str
        """
        params = org_id and {'orgId': org_id} or None
        body = generate and {'generate': generate} or {}
        url = self.ep(f'{location_id}/actions/generatePassword/invoke')
        data = await self.post(url=url, params=params, json=body)
        return data['exampleSipPassword']

    async def validate_extensions(self, location_id: str, extensions: list[str],
                            org_id: str = None) -> ValidateExtensionsResponse:
        """
        Validate extensions for a specific location.

        Validating extensions requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Validate extensions for this location.
        :type location_id: str
        :param extensions: Array of extensions that will be validated.
        :type extensions: list[str]
        :param org_id: Validate extensions for this organization.
        :type org_id: str
        :return: Validation result
        :rtype: :class:`wxc_sdk.common.ValidateExtensionsResponse`
        """
        url = self.ep(f'{location_id}/actions/validateExtensions/invoke')
        body = {'extensions': extensions}
        params = org_id and {'orgId': org_id} or None
        data = await self.post(url=url, params=params, json=body)
        return ValidateExtensionsResponse.parse_obj(data)

    async def details(self, location_id: str, org_id: str = None) -> TelephonyLocation:
        """
        Shows Webex Calling details for a location, by ID.

        Specify the location ID in the locationId parameter in the URI.

        Searching and viewing location in your organization requires an administrator auth token with
        the spark-admin:telephony_config_read scope.

        :param location_id: Retrieve Webex Calling location attributes for this location.
        :type location_id: str
        :param org_id: Retrieve Webex Calling location attributes for this organization.
        :type org_id: str
        :return: Webex Calling details for location
        :rtype: :class:`TelephonyLocation`
        """
        params = org_id and {'orgId': org_id}
        url = self.ep(location_id)
        data = await self.get(url=url, params=params)
        return TelephonyLocation.parse_obj(data)

    async def update(self, location_id: str, settings: TelephonyLocation, org_id: str = None):
        """
        Update Webex Calling details for a location, by ID.

        Specify the location ID in the locationId parameter in the URI.

        Modifying the connection via API is only supported for the local PSTN types of TRUNK and ROUTE_GROUP.

        Updating a location in your organization requires an administrator auth token with
        the spark-admin:telephony_config_write scope.

        Example :

            .. code-block:: python

                api.telephony.location.update(location_id=location_id,
                                              settings=TelephonyLocation(
                                                  calling_line_id=CallingLineId(
                                                      phone_number=tn),
                                                  routing_prefix=routing_prefix,
                                                  outside_dial_digit='9'))

        :param location_id: Updating Webex Calling location attributes for this location.
        :type location_id: str
        :param settings: settings to update
        :type settings: :class:`TelephonyLocation`
        :param org_id: Updating Webex Calling location attributes for this organization.
        :type org_id: str
        :return:
        """
        data = settings.json(exclude={'location_id', 'user_limit', 'default_domain'})
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id)
        await self.put(url=url, data=data, params=params)

    async def change_announcement_language(self, location_id: str, language_code: str, agent_enabled: bool = None,
                                     service_enabled: bool = None, org_id: str = None):
        """
        Change Announcement Language

        Change announcement language for the given location.

        Change announcement language for current people/workspaces and/or existing feature configurations. This does
        not change the default announcement language which is applied to new users/workspaces and new feature
        configurations.

        Changing announcement language for the given location requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Change announcement language for this location.
        :type location_id: str
        :param language_code: Language code.
        :type language_code: str
        :param agent_enabled: Set to true to change announcement language for existing people and workspaces.
        :type agent_enabled: bool
        :param service_enabled: Set to true to change announcement language for existing feature configurations.
        :type service_enabled: bool
        :param org_id: Change announcement language for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        body = {'announcementLanguageCode': language_code}
        if agent_enabled is not None:
            body['agentEnabled'] = agent_enabled
        if service_enabled is not None:
            body['serviceEnabled'] = service_enabled
        url = self.session.ep(f'{location_id}/actions/modifyAnnouncementLanguage/invoke')
        await self.put(url, json=body, params=params)

    async def device_settings(self, location_id: str, org_id: str = None) -> DeviceCustomization:
        """
        Get device override settings for a location.

        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param location_id: Unique identifier for the location
        :type location_id: str
        :param org_id: Settings on the device in this organization
        :type org_id: str
        :return: device customization response
        :rtype: DeviceCustomization
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(f'{location_id}/devices/settings')
        data = await self.get(url=url, params=params)
        return DeviceCustomization.parse_obj(data)


class AsVoiceMessagingApi(AsApiChild, base='telephony/voiceMessages'):
    """
    Voice Messaging APIs provide support for handling voicemail and message waiting indicators in Webex Calling.  The
    APIs are limited to user access (no admin access), and all GET commands require the spark:calls_read scope, while
    the other commands require the spark:calls_write scope.
    """

    async def summary(self) -> MessageSummary:
        """
        Get a summary of the voicemail messages for the user.
        """
        url = self.ep('summary')
        data = await super().get(url=url)
        return MessageSummary.parse_obj(data)

    def list_gen(self, **params) -> AsyncGenerator[VoiceMessageDetails, None, None]:
        """
        Get the list of all voicemail messages for the user.
        """
        url = self.ep()
        return self.session.follow_pagination(url=url, model=VoiceMessageDetails, params=params)

    async def list(self, **params) -> List[VoiceMessageDetails]:
        """
        Get the list of all voicemail messages for the user.
        """
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=VoiceMessageDetails, params=params)]

    async def delete(self, message_id: str):
        """
        Delete a specfic voicemail message for the user.

        :param message_id: The message identifer of the voicemail message to delete
        :type message_id: str
        """
        url = self.ep(f'{message_id}')
        await super().delete(url=url)
        return

    async def mark_as_read(self, message_id: str):
        """
        Update the voicemail message(s) as read for the user.
        If the messageId is provided, then only mark that message as read.  Otherwise, all messages for the user are
        marked as read.

        :param message_id: The voicemail message identifier of the message to mark as read.  If the messageId is not
            provided, then all voicemail messages for the user are marked as read.
        :type message_id: str
        """
        body = {'messageId': message_id}
        url = self.ep('markAsRead')
        await super().post(url=url, json=body)
        return

    async def mark_as_unread(self, message_id: str):
        """
        Update the voicemail message(s) as unread for the user.
        If the messageId is provided, then only mark that message as unread.  Otherwise, all messages for the user are
        marked as unread.

        :param message_id: The voicemail message identifier of the message to mark as unread.  If the messageId is not
            provided, then all voicemail messages for the user are marked as unread.
        :type message_id: str
        """
        body = {'messageId': message_id}
        url = self.ep('markAsUnread')
        await super().post(url=url, json=body)
        return


class AsVoicePortalApi(AsApiChild, base='telephony/config/locations'):
    """
    location voice portal API
    """

    def _endpoint(self, *, location_id: str, path: str = None) -> str:
        """
        location specific
        telephony/config/locations/{locationId}/voicePortal

        :meta private:
        :param location_id: Unique identifier for the location.
        :type location_id: str
        :param path: additional path
        :type: path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        ep = self.session.ep(f'telephony/config/locations/{location_id}/voicePortal{path}')
        return ep

    async def read(self, location_id: str, org_id: str = None) -> VoicePortalSettings:
        """

        :param location_id: Location to which the voice portal belongs.
        :type location_id: str
        :param org_id: Organization to which the voice portal belongs.
        :type org_id: str
        :return: location voice portal settings
        :rtype: VoicePortalSettings
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        return VoicePortalSettings.parse_obj(await self.get(url, params=params))

    async def update(self, location_id: str, settings: VoicePortalSettings, passcode: str = None, org_id: str = None):
        """
        Update VoicePortal

        Update Voice portal information for the location.

        Voice portals provide an interactive voice response (IVR) system so administrators can manage auto attendant
        announcements.

        Updating voice portal information for organization and/or rules requires a full administrator auth token with
        a scope of spark-admin:telephony_config_write.

        :param location_id: Location to which the voice portal belongs.
        :type location_id: str
        :param settings: new settings
        :type settings: VoicePortalSettings
        :param passcode: new passcode
        :type passcode: str
        :param org_id: Organization to which the voice portal belongs.
        :type org_id: str
        """
        data = json.loads(settings.json(exclude={'portal_id': True,
                                                 'language': True}))
        if passcode is not None:
            data['passcode'] = {'newPasscode': passcode,
                                'confirmPasscode': passcode}
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id)
        await self.put(url, params=params, json=data)

    async def passcode_rules(self, location_id: str, org_id: str = None) -> PasscodeRules:
        """
        Get VoicePortal Passcode Rule

        Retrieve the voice portal passcode rule for a location.

        Voice portals provide an interactive voice response (IVR) system so administrators can manage auto attendant
        announcements

        Retrieving the voice portal passcode rule requires a full read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve voice portal passcode rules for this location.
        :type location_id: str
        :param org_id: Retrieve voice portal passcode rules for this organization.
        :type org_id: str
        :return: passcode rules
        :rtype: PasscodeRules
        """
        params = org_id and {'orgId': org_id} or None
        url = self._endpoint(location_id=location_id, path='passcodeRules')
        return PasscodeRules.parse_obj(await self.get(url, params=params))


class AsVoicemailGroupsApi(AsApiChild, base='telephony/config/voicemailGroups'):
    """
    API for voicemail groups
    """

    def ep(self, location_id: str = None, path: str = None):
        """
        :param location_id:
        :param path:
        :return:
        """
        path = path and f'/{path}' or ''
        if location_id is None:
            return super().ep(path)
        return self.session.ep(f'telephony/config/locations/{location_id}/voicemailGroups{path}')

    def list_gen(self, location_id: str = None, name: str = None, phone_number: str = None,
             org_id: str = None, **params) -> AsyncGenerator[VoicemailGroup, None, None]:
        """
        List the voicemail group information for the organization.

        You can create a shared voicemail box and inbound fax box to assign to users or call routing features like an
        auto attendant, call queue, or hunt group.

        Retrieving voicemail Group for the organization requires a full read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Location to which the voicemail group belongs.
        :type location_id: str
        :param name: Search (Contains) based on voicemail group name
        :type name: str
        :param phone_number: Search (Contains) based on number or extension
        :type phone_number: str
        :param org_id: Organization to which the voicemail group belongs.
        :type org_id: str
        :return: yields ::class::`VoicemailGroup` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items() if p not in {'self', 'params'} and v is not None)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=VoicemailGroup, params=params, item_key='voicemailGroups')

    async def list(self, location_id: str = None, name: str = None, phone_number: str = None,
             org_id: str = None, **params) -> List[VoicemailGroup]:
        """
        List the voicemail group information for the organization.

        You can create a shared voicemail box and inbound fax box to assign to users or call routing features like an
        auto attendant, call queue, or hunt group.

        Retrieving voicemail Group for the organization requires a full read-only administrator auth token with a
        scope of spark-admin:telephony_config_read.

        :param location_id: Location to which the voicemail group belongs.
        :type location_id: str
        :param name: Search (Contains) based on voicemail group name
        :type name: str
        :param phone_number: Search (Contains) based on number or extension
        :type phone_number: str
        :param org_id: Organization to which the voicemail group belongs.
        :type org_id: str
        :return: yields ::class::`VoicemailGroup` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items() if p not in {'self', 'params'} and v is not None)
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=VoicemailGroup, params=params, item_key='voicemailGroups')]

    async def details(self, location_id: str, voicemail_group_id: str, org_id: str = None) -> VoicemailGroupDetail:
        """
        Retrieve voicemail group details for a location.

        Manage your voicemail group settings for a specific location, like when you want your voicemail to be active,
        message storage settings, and how you would like to be notified of new voicemail messages.

        Retrieving voicemail group details requires a full, user or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: Retrieve voicemail group details for this location.
        :type location_id: str
        :param voicemail_group_id: Retrieve voicemail group details for this voicemail group ID.
        :type voicemail_group_id: str
        :param org_id: Retrieve voicemail group details for a customer location.
        :type org_id: str
        :return: Voicemail group settings
        :type: :class:`VoicemailGroupDetail`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id, voicemail_group_id)
        data = await self.get(url=url, params=params)
        return VoicemailGroupDetail.parse_obj(data)

    async def update(self, location_id: str, voicemail_group_id: str, settings: VoicemailGroupDetail, org_id: str = None):
        """
        Modifies the voicemail group location details for a particular location for a customer.

        Manage your voicemail settings, like when you want your voicemail to be active, message storage settings, and
        how you would like to be notified of new voicemail messages.

        Modifying the voicemail group location details requires a full, user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Modifies the voicemail group details for this location.
        :type location_id: str
        :param voicemail_group_id: Modifies the voicemail group details for this voicemail group ID.
        :type voicemail_group_id: str
        :param settings: New settings
        :type settings: :class:`VoicemailGroupDetail`
        :param org_id: Modifies the voicemail group details for a customer location.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id, voicemail_group_id)
        body = settings.json_for_update()
        await self.put(url=url, data=body, params=params)

    async def create(self, location_id: str, settings: VoicemailGroupDetail, org_id: str = None) -> str:
        """
        Create new voicemail group for the given location for a customer.

        Voicemail group can be created for given location for a customer.

        Creating voicemail group for the given location requires a full or user administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Create new voice mail group for this location.
        :type location_id: str
        :param settings: settings for new voicemail group
            Example:

            .. code-block:: python

                settings = VoicemailGroupDetail.create(
                                        name=vmg_name, extension=extension,
                                        first_name='first', last_name='last',
                                        passcode=740384)
                vmg_id = api.telephony.voicemail_groups.create(location_id=location_id,
                                                               settings=settings)

        :type settings: :class:`VoicemailGroupDetail`
        :param org_id: Create new voice mail group for this organization.
        :type org_id: str
        :return: UUID of the newly created voice mail group.
        :rtype: str
        """
        body = settings.json_for_create()
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id)
        data = await self.post(url=url, data=body, params=params)
        return data['id']

    async def delete(self, location_id: str, voicemail_group_id: str, org_id: str = None):
        """
        Delete the designated voicemail group.

        Deleting a voicemail group requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Location from which to delete a voicemail group.
        :type location_id: str
        :param voicemail_group_id: Delete the voicemail group with the matching ID.
        :type voicemail_group_id: str
        :param org_id: Delete the voicemail group from this organization.
        :type org_id: str
        """
        url = self.ep(location_id, voicemail_group_id)
        await super().delete(url=url)


class AsVoicemailRulesApi(AsApiChild, base='telephony/config/voicemail/rules'):
    """
    API for voicemail rules settings
    """

    async def read(self, org_id: str = None) -> VoiceMailRules:
        """
        Get Voicemail Rules

        Retrieve the organization's voicemail rules.

        Organizational voicemail rules specify the default passcode requirements.

        Retrieving the organization's voicemail rules requires a full, user or read-only administrator auth token with
        a scope of spark-admin:telephony_config_read.

        :param org_id: Retrieve voicemail settings for this organization.
        :type org_id: str
        :return: VM settings
        :rtype: OrganisationVoicemailSettings
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        return VoiceMailRules.parse_obj(await self.get(url, params=params))

    async def update(self, settings: VoiceMailRules, org_id: str = None):
        """
        Update Voicemail Rules

        Update the organization's default voicemail passcode and/or rules.

        Organizational voicemail rules specify the default passcode requirements.

        If you choose to set default passcode for new people added to your organization, communicate to your people
        what that passcode is, and that it must be reset before they can access their voicemail. If this feature is
        not turned on, each new person must initially set their own passcode.

        Updating organization's voicemail passcode and/or rules requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param settings: new settings
        :type settings: VoiceMailRules
        :param org_id: Update voicemail rules for this organization.
        :type org_id: str
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = settings.json(exclude={'default_voicemail_pin_rules': True})
        await self.put(url, params=params, data=data)


class AsTelephonyApi(AsApiChild, base='telephony/config'):
    """
    The telephony settings (features) API.
    """
    #: access or authentication codes
    access_codes: AsAccessCodesApi
    auto_attendant: AsAutoAttendantApi
    #: location call intercept settings
    call_intercept: AsLocationInterceptApi
    calls: AsCallsApi
    callpark: AsCallParkApi
    callpark_extension: AsCallparkExtensionApi
    callqueue: AsCallQueueApi
    #: WxC device operations
    devices: AsTelephonyDevicesApi
    huntgroup: AsHuntGroupApi
    jobs: AsJobsApi
    #: location specific settings
    location: AsTelephonyLocationApi
    #: organisation voicemail settings
    organisation_voicemail: AsOrganisationVoicemailSettingsAPI
    paging: AsPagingApi
    permissions_out: AsOutgoingPermissionsApi
    pickup: AsCallPickupApi
    prem_pstn: AsPremisePstnApi
    pnc: AsPrivateNetworkConnectApi
    schedules: AsScheduleApi
    # location voicemail groups
    voicemail_groups: AsVoicemailGroupsApi
    voicemail_rules: AsVoicemailRulesApi
    voice_messaging: AsVoiceMessagingApi
    voiceportal: AsVoicePortalApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.access_codes = AsAccessCodesApi(session=session)
        self.auto_attendant = AsAutoAttendantApi(session=session)
        self.call_intercept = AsLocationInterceptApi(session=session)
        self.calls = AsCallsApi(session=session)
        self.callpark = AsCallParkApi(session=session)
        self.callpark_extension = AsCallparkExtensionApi(session=session)
        self.callqueue = AsCallQueueApi(session=session)
        self.devices = AsTelephonyDevicesApi(session=session)
        self.huntgroup = AsHuntGroupApi(session=session)
        self.jobs = AsJobsApi(session=session)
        self.location = AsTelephonyLocationApi(session=session)
        self.organisation_voicemail = AsOrganisationVoicemailSettingsAPI(session=session)
        self.paging = AsPagingApi(session=session)
        self.permissions_out = AsOutgoingPermissionsApi(session=session, locations=True)
        self.pickup = AsCallPickupApi(session=session)
        self.pnc = AsPrivateNetworkConnectApi(session=session)
        self.prem_pstn = AsPremisePstnApi(session=session)
        self.schedules = AsScheduleApi(session=session, base=ScheduleApiBase.locations)
        self.voicemail_groups = AsVoicemailGroupsApi(session=session)
        self.voicemail_rules = AsVoicemailRulesApi(session=session)
        self.voice_messaging = AsVoiceMessagingApi(session=session)
        self.voiceportal = AsVoicePortalApi(session=session)

    def phone_numbers_gen(self, location_id: str = None, phone_number: str = None, available: bool = None,
                      order: str = None,
                      owner_name: str = None, owner_id: str = None, owner_type: OwnerType = None,
                      extension: str = None, number_type: NumberType = None,
                      phone_number_type: NumberListPhoneNumberType = None,
                      state: NumberState = None, toll_free_numbers: bool = None,
                      org_id: str = None, **params) -> AsyncGenerator[NumberListPhoneNumber, None, None]:
        """
        Get Phone Numbers for an Organization with given criteria.

        List all the phone numbers for the given organization along with the status and owner (if any).

        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return the list of phone numbers for this location within the given organization.
        :type location_id: str
        :param phone_number: Search for this phone number.
        :type phone_number: str
        :param available: Search among the available phone numbers. This parameter cannot be used along with owner_type
            parameter when set to true.
        :type available: bool
        :param order: Sort the list of phone numbers based on the following:lastName,dn,extension. Default sort will
            be based on number and extension in an Ascending order
        :type order: str
        :param owner_name: Return the list of phone numbers that is owned by given owner name. Maximum length is 255.
        :type owner_name: str
        :param owner_id: Returns only the matched number/extension entries assigned to the feature with specified
            uuid/broadsoftId.
        :type owner_id: str
        :param owner_type: Returns the list of phone numbers that are of given owner_type.
        :type owner_type: OwnerType
        :param extension: Returns the list of PSTN phone numbers with given extension.
        :type extension: str
        :param number_type: Returns the filtered list of PSTN phone numbers that contains given type of numbers.
            This parameter cannot be used along with available or state.
        :type number_type: NumberType
        :param phone_number_type: Returns the filtered list of PSTN phone numbers that are of given phoneNumberType.
        :type phone_number_type: NumberListPhoneNumberType
        :param state: Returns the list of PSTN phone numbers with matching state.
        :type state: NumberState
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: yields :class:`NumberListPhoneNumber` instances
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i and v is not None and p != 'params')
        for param, value in params.items():
            if isinstance(value, bool):
                value = 'true' if value else 'false'
                params[param] = value
            elif isinstance(value, Enum):
                value = value.value
                params[param] = value
        url = self.ep(path='numbers')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=NumberListPhoneNumber, params=params,
                                              item_key='phoneNumbers')

    async def phone_numbers(self, location_id: str = None, phone_number: str = None, available: bool = None,
                      order: str = None,
                      owner_name: str = None, owner_id: str = None, owner_type: OwnerType = None,
                      extension: str = None, number_type: NumberType = None,
                      phone_number_type: NumberListPhoneNumberType = None,
                      state: NumberState = None, toll_free_numbers: bool = None,
                      org_id: str = None, **params) -> List[NumberListPhoneNumber]:
        """
        Get Phone Numbers for an Organization with given criteria.

        List all the phone numbers for the given organization along with the status and owner (if any).

        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.

        Retrieving this list requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return the list of phone numbers for this location within the given organization.
        :type location_id: str
        :param phone_number: Search for this phone number.
        :type phone_number: str
        :param available: Search among the available phone numbers. This parameter cannot be used along with owner_type
            parameter when set to true.
        :type available: bool
        :param order: Sort the list of phone numbers based on the following:lastName,dn,extension. Default sort will
            be based on number and extension in an Ascending order
        :type order: str
        :param owner_name: Return the list of phone numbers that is owned by given owner name. Maximum length is 255.
        :type owner_name: str
        :param owner_id: Returns only the matched number/extension entries assigned to the feature with specified
            uuid/broadsoftId.
        :type owner_id: str
        :param owner_type: Returns the list of phone numbers that are of given owner_type.
        :type owner_type: OwnerType
        :param extension: Returns the list of PSTN phone numbers with given extension.
        :type extension: str
        :param number_type: Returns the filtered list of PSTN phone numbers that contains given type of numbers.
            This parameter cannot be used along with available or state.
        :type number_type: NumberType
        :param phone_number_type: Returns the filtered list of PSTN phone numbers that are of given phoneNumberType.
        :type phone_number_type: NumberListPhoneNumberType
        :param state: Returns the list of PSTN phone numbers with matching state.
        :type state: NumberState
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
        :param org_id: List numbers for this organization.
        :type org_id: str
        :return: yields :class:`NumberListPhoneNumber` instances
        """
        params.update((to_camel(p), v) for i, (p, v) in enumerate(locals().items())
                      if i and v is not None and p != 'params')
        for param, value in params.items():
            if isinstance(value, bool):
                value = 'true' if value else 'false'
                params[param] = value
            elif isinstance(value, Enum):
                value = value.value
                params[param] = value
        url = self.ep(path='numbers')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=NumberListPhoneNumber, params=params,
                                              item_key='phoneNumbers')]

    async def phone_number_details(self, org_id: str = None) -> NumberDetails:
        """
        get summary (counts) of phone numbers

        :param org_id: detaild for numbers in this organization.
        :type org_id: str
        :return: phone number details
        :rtype: :class:`NumberDetails`
        """
        params = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                  if i and v is not None}
        params['details'] = 'true'
        params['max'] = 1
        url = self.ep(path='numbers')
        data = await self.get(url, params=params)
        return NumberDetails.parse_obj(data['count'])

    async def validate_extensions(self, extensions: list[str]) -> ValidateExtensionsResponse:
        """
        Validate the List of Extensions

        Validate the List of Extensions. Retrieving this list requires a full or read-only administrator auth token
        with a scope of spark-admin:telephony_config_read.

        :param extensions: Array of Strings of ID of Extensions.
        :type extensions: list[str]
        :return: validation response
        :rtype: :class:`wxc_sdk.common.ValidateExtensionsResponse`
        """
        url = self.ep(path='actions/validateExtensions/invoke')
        data = await self.post(url, json={'extensions': extensions})
        return ValidateExtensionsResponse.parse_obj(data)

    async def validate_phone_numbers(self, phone_numbers: list[str], org_id: str = None) -> ValidatePhoneNumbersResponse:
        """
        Validate the list of phone numbers in an organization. Each phone number's availability is indicated in the
        response.

        Each location has a set of phone numbers that can be assigned to people, workspaces, or features. Phone numbers
        must follow E.164 format for all countries, except for the United States, which can also follow the National
        format. Active phone numbers are in service.

        Validating a phone number in an organization requires a full administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param phone_numbers: List of phone numbers to be validated.
        :type phone_numbers: list[str]
        :param org_id: Organization of the Route Group.
        :type org_id: str
        :return: validation result
        :rtype: :class:`wxc_sdk.common.ValidatePhoneNumbersResponse`
        """
        url = self.ep('actions/validateNumbers/invoke')
        body = {'phoneNumbers': phone_numbers}
        params = org_id and {'orgId': org_id} or None
        data = await self.post(url=url, params=params, json=body)
        return ValidatePhoneNumbersResponse.parse_obj(data)

    async def ucm_profiles(self, org_id: str = None) -> list[UCMProfile]:
        """
        Read the List of UC Manager Profiles

        List all calling UC Manager Profiles for the organization.

        UC Manager Profiles are applicable if your organization uses Jabber in Team Messaging mode or Calling in
        Webex Teams (Unified CM).

        The UC Manager Profile has an organization-wide default and may be overridden for individual persons, although
        currently only setting at a user level is supported by Webex APIs.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:people_read as this API is designed to be used in conjunction with calling behavior at the
        user level.

        :param org_id: List manager profiles in this organization.
        :type org_id: str
        :return: list of :class:`UCMProfile`
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(path='callingProfiles')
        data = await self.get(url, params=params)
        return parse_obj_as(list[UCMProfile], data['callingProfiles'])

    def route_choices_gen(self, route_group_name: str = None, trunk_name: str = None, order: str = None,
                      org_id: str = None) -> AsyncGenerator[RouteIdentity, None, None]:
        """
        List all Routes for the organization.

        Trunk and Route Group qualify as Route. Trunks and Route Groups provide you the ability to configure Webex
        Calling to manage calls between Webex Calling hosted users and premises PBX(s) users. This solution lets you
        configure users to use Cloud PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param route_group_name: Return the list of route identities matching the route group name.
        :param trunk_name: Return the list of route identities matching the trunk name.
        :param order: Order the route identities according to the designated fields.
            Available sort fields: routeName, routeType.
        :param org_id: List route identities for this organization.
        :return:
        """
        params = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                  if i and v is not None}
        url = self.ep('routeChoices')
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=RouteIdentity, params=params, item_key='routeIdentities')

    async def route_choices(self, route_group_name: str = None, trunk_name: str = None, order: str = None,
                      org_id: str = None) -> List[RouteIdentity]:
        """
        List all Routes for the organization.

        Trunk and Route Group qualify as Route. Trunks and Route Groups provide you the ability to configure Webex
        Calling to manage calls between Webex Calling hosted users and premises PBX(s) users. This solution lets you
        configure users to use Cloud PSTN (CCP or Cisco PSTN) or Premises-based PSTN.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param route_group_name: Return the list of route identities matching the route group name.
        :param trunk_name: Return the list of route identities matching the trunk name.
        :param order: Order the route identities according to the designated fields.
            Available sort fields: routeName, routeType.
        :param org_id: List route identities for this organization.
        :return:
        """
        params = {to_camel(p): v for i, (p, v) in enumerate(locals().items())
                  if i and v is not None}
        url = self.ep('routeChoices')
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=url, model=RouteIdentity, params=params, item_key='routeIdentities')]

    async def test_call_routing(self, originator_id: str, originator_type: OriginatorType, destination: str,
                          originator_number: str = None, org_id: str = None) -> TestCallRoutingResult:
        """
        Validates that an incoming call can be routed.

        Dial plans route calls to on-premises destinations by use of trunks or route groups. They are configured
        globally for an enterprise and apply to all users, regardless of location. A dial plan also specifies the
        routing choice (trunk or route group) for calls that match any of its dial patterns. Specific dial patterns
        can be defined as part of your dial plan.

        Test call routing requires a full or write-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param originator_id: This element is used to identify the originating party. It can be user UUID or trunk UUID.
        :type originator_id: str
        :param originator_type:
        :type originator_type: :class:`OriginatorType`
        :param destination: This element specifies called party. It can be any dialable string, for example, an
            ESN number, E.164 number, hosted user DN, extension, extension with location code, URL, FAC code.
        :type destination: str
        :param originator_number: Only used when originatorType is TRUNK. This element could be a phone number or URI.
        :type originator_number: str
        :param org_id: Organization in which we are validating a call routing.
        :type org_id: str
        :return: call routing test result
        :rtype: :class:`TestCallRoutingResult`
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'org_id'} and v is not None}
        params = org_id and {'orgId': org_id} or None
        url = self.ep('actions/testCallRouting/invoke')
        data = await self.post(url=url, params=params, json=body)
        return TestCallRoutingResult.parse_obj(data)

    async def supported_devices(self, org_id: str = None) -> list[SupportedDevice]:
        """
        Gets the list of supported devices for an organization location.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List supported devices for an organization
        :return: List of supported devices
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep('supportedDevices')
        data = await self.get(url=url, params=params)
        return parse_obj_as(list[SupportedDevice], data['devices'])

    async def device_settings(self, org_id: str = None) -> DeviceCustomization:
        """
        Get device override settings for an organization.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List supported devices for an organization location.
        :type org_id: str
        :return: device customization response
        :rtype: DeviceCustomization
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep('devices/settings')
        data = await self.get(url=url, params=params)
        return DeviceCustomization.parse_obj(data)


class AsWebhookApi(AsApiChild, base='webhooks'):
    """
    API for webhook management
    """

    def list_gen(self) -> AsyncGenerator[Webhook, None, None]:
        """
        List all of your webhooks.

        :return: yields webhooks
        """
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Webhook)

    async def list(self) -> List[Webhook]:
        """
        List all of your webhooks.

        :return: yields webhooks
        """
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=Webhook)]

    async def create(self, name: str, target_url: str, resource: WebhookResource, event: WebhookEventType, filter: str = None,
               secret: str = None,
               owned_by: str = None) -> Webhook:
        """
        Creates a webhook.

        :param name: A user-friendly name for the webhook.
        :param target_url: The URL that receives POST requests for each event.
        :param resource: The resource type for the webhook. Creating a webhook requires 'read' scope on the resource
            the webhook is for.
        :param event: The event type for the webhook.
        :param filter: The filter that defines the webhook scope.
        :param secret: The secret used to generate payload signature.
        :param owned_by: Specified when creating an org/admin level webhook. Supported for meetings, recordings and
            meetingParticipants resources for now.

        :return: the new webhook
        """
        params = {to_camel(param): value for i, (param, value) in enumerate(locals().items())
                  if i and value is not None}
        body = json.loads(WebhookCreate(**params).json())
        ep = self.ep()
        data = await self.post(ep, json=body)
        result = Webhook.parse_obj(data)
        return result

    async def details(self, webhook_id: str) -> Webhook:
        """
        Get Webhook Details
        Shows details for a webhook, by ID.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :return: Webhook details
        """
        url = self.ep(webhook_id)
        return Webhook.parse_obj(await self.get(url))

    async def update(self, webhook_id: str, update: Webhook) -> Webhook:
        """
        Updates a webhook, by ID. You cannot use this call to deactivate a webhook, only to activate a webhook that
        was auto deactivated. The fields that can be updated are name, targetURL, secret and status. All other fields,
        if supplied, are ignored.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :param update: The webhook update
        :type update: Webhook
        :return: updated :class:`Webhook` object
        """
        url = self.ep(webhook_id)
        webhook_data = update.json(include={'name', 'target_url', 'secret', 'owned_by', 'status'})
        return Webhook.parse_obj(await self.put(url, data=webhook_data))

    async def webhook_delete(self, webhook_id: str):
        """
        Deletes a webhook, by ID.

        :param webhook_id: The unique identifier for the webhook.
        :type webhook_id: str
        :return: None
        """
        ep = self.ep(f'{webhook_id}')
        await self.delete(ep)


class AsWorkspaceLocationFloorApi(AsApiChild, base='workspaceLocations'):
    # noinspection PyMethodOverriding
    def ep(self, location_id: str, floor_id: str = None):
        path = f'{location_id}/floors'
        if floor_id:
            path = f'{path}/{floor_id}'
        return super().ep(path=path)

    def list_gen(self, location_id: str, org_id: str = None) -> AsyncGenerator[WorkspaceLocationFloor, None, None]:
        """

        :param location_id:
        :param org_id:
        :return:
        """
        url = self.ep(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        return self.session.follow_pagination(url=url, model=WorkspaceLocationFloor, params=params, item_key='items')

    async def list(self, location_id: str, org_id: str = None) -> List[WorkspaceLocationFloor]:
        """

        :param location_id:
        :param org_id:
        :return:
        """
        url = self.ep(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        return [o async for o in self.session.follow_pagination(url=url, model=WorkspaceLocationFloor, params=params, item_key='items')]

    async def create(self, location_id: str, floor_number: int, display_name: str = None,
               org_id: str = None) -> WorkspaceLocationFloor:
        """
        Create a Workspace Location Floor

        Create a new floor in the given location. The displayName parameter is optional, and omitting it will result
        in the creation of a floor without that value set.

        :param location_id: A unique identifier for the location.
        :param floor_number:
        :param display_name:
        :type location_id: str
        :param org_id:
        :type org_id: str
        :return: new workspace location floor
        :rtype: WorkspaceLocationFloor
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'location_id', 'org_id'} and v is not None}
        url = self.ep(location_id=location_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.post(url=url, params=params, json=body)
        return WorkspaceLocationFloor.parse_obj(data)

    async def details(self, location_id: str, floor_id: str, org_id: str = None) -> WorkspaceLocationFloor:
        """
        Get a Workspace Location Floor Details

        Shows details for a floor, by ID. Specify the floor ID in the floorId parameter in the URI.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :param org_id:
        :type org_id: str
        :return: workspace location floor details
        :rtype: WorkspaceLocationFloor
        """
        url = self.ep(location_id=location_id, floor_id=floor_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url=url, params=params)
        return WorkspaceLocationFloor.parse_obj(data)

    async def update(self, location_id: str, floor_id: str, settings: WorkspaceLocationFloor,
               org_id: str = None) -> WorkspaceLocationFloor:
        """
        Updates details for a floor, by ID. Specify the floor ID in the floorId parameter in the URI. Include all
        details for the floor that are present in a Get Workspace Location Floor Details. Not including the optional
        displayName field will result in the field no longer being defined for the floor.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :param settings: new settings
        :type settings: WorkspaceLocationFloor
        :param org_id:
        :type org_id: str
        :return: updated workspace location floor
        """
        data = settings.json(exclude_none=True, exclude_unset=True, exclude={'id', 'location_id'})
        url = self.ep(location_id=location_id, floor_id=floor_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.put(url=url, data=data, params=params)
        return WorkspaceLocationFloor.parse_obj(data)

    async def delete(self, location_id: str, floor_id: str, org_id: str = None):
        """
        Delete a Workspace Location Floor
        Deletes a floor, by ID.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :param org_id:
        :type org_id: str
        """
        url = self.ep(location_id=location_id, floor_id=floor_id)
        params = org_id and {'orgId': org_id} or None
        await super().delete(url=url, params=params)


class AsWorkspaceLocationApi(AsApiChild, base='workspaceLocations'):
    #: Workspace location floor API :class:`AsWorkspaceLocationFloorApi`
    floors: AsWorkspaceLocationFloorApi

    def __init__(self, *, session: AsRestSession, base: str = None):
        super().__init__(session=session, base=base)
        self.floors = AsWorkspaceLocationFloorApi(session=session)

    def ep(self, location_id: str = None):
        return super().ep(path=location_id)

    def list_gen(self, display_name: str = None, address: str = None, country_code: str = None, city_name: str = None,
             org_id: str = None, **params) -> AsyncGenerator[WorkspaceLocation, None, None]:
        """
        List workspace locations

        :param display_name: Location display name.
        :type display_name: str
        :param address: Location address
        :type address: str
        :param country_code: Location country code (ISO 3166-1).
        :type country_code: str
        :param city_name: Location city name.
        :type city_name: str
        :param org_id: Organization id
        :type org_id: str
        :param params: addtl. parameters
        :return: generator of :class:`WorkspaceLocation` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if p not in {'self', 'params'} and v is not None)
        url = self.ep()
        return self.session.follow_pagination(url=url, model=WorkspaceLocation, params=params, item_key='items')

    async def list(self, display_name: str = None, address: str = None, country_code: str = None, city_name: str = None,
             org_id: str = None, **params) -> List[WorkspaceLocation]:
        """
        List workspace locations

        :param display_name: Location display name.
        :type display_name: str
        :param address: Location address
        :type address: str
        :param country_code: Location country code (ISO 3166-1).
        :type country_code: str
        :param city_name: Location city name.
        :type city_name: str
        :param org_id: Organization id
        :type org_id: str
        :param params: addtl. parameters
        :return: generator of :class:`WorkspaceLocation` instances
        """
        params.update((to_camel(p), v) for p, v in locals().items()
                      if p not in {'self', 'params'} and v is not None)
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=WorkspaceLocation, params=params, item_key='items')]

    async def create(self, display_name: str, address: str, country_code: str, latitude: float, longitude: float,
               city_name: str = None, notes: str = None, org_id: str = None) -> WorkspaceLocation:
        """
        Create a location. The cityName and notes parameters are optional, and omitting them will result in the
        creation of a location without these values set.

        :param display_name: A friendly name for the location.
        :param address: The location address.
        :param country_code: The location country code (ISO 3166-1).
        :param latitude: The location latitude.
        :param longitude: The location longitude.
        :param city_name: The location city name.
        :param notes: Notes associated to the location.
        :param org_id:
        :return: created workspace location
        :rtype: WorkspaceLocation
        """
        body = {to_camel(p): v for p, v in locals().items()
                if p not in {'self', 'org_id'} and v is not None}
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = await self.post(url=url, json=body, params=params)
        return WorkspaceLocation.parse_obj(data)

    async def details(self, location_id: str, org_id: str = None) -> WorkspaceLocation:
        """
        Get a Workspace Location Details
        Shows details for a location, by ID. Specify the location ID in the locationId parameter in the URI.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param org_id:
        :type org_id: str
        :return: Workspace location details
        :rtype: WorkspaceLocation
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id=location_id)
        data = await self.get(url=url, params=params)
        return WorkspaceLocation.parse_obj(data)

    async def update(self, location_id: str, settings: WorkspaceLocation, org_id: str = None):
        """
        Update a Workspace Location
        Updates details for a location, by ID. Specify the location ID in the locationId parameter in the URI.
        Include all details for the location that are present in a Get Workspace Location Details. Not including the
        optional cityName or notes fields (setting them to None) will result in the fields no longer being defined for
        the location.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param settings: new settings
        :type settings: WorkspaceLocation
        :param org_id:
        :type org_id: str
        :return: updated workspace location
        :rtype: WorkspaceLocation
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id=location_id)
        body = settings.json(exclude_none=True, exclude_unset=True, exclude={'id'})
        data = await self.put(url=url, data=body, params=params)
        return WorkspaceLocation.parse_obj(data)

    async def delete(self, location_id: str, org_id: str = None):
        """
        Delete a Workspace Location
        Deletes a location, by ID. The workspaces associated to that location will no longer have a location, but a new
        location can be reassigned to them.
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id=location_id)
        await super().delete(url=url, params=params)


class AsWorkspaceNumbersApi(AsApiChild, base='workspaces'):

    # noinspection PyMethodOverriding
    def ep(self, workspace_id: str, path: str = None):
        """
        :meta private:
        """
        path = path and '/path' or ''
        return super().ep(path=f'{workspace_id}/features/numbers/{path}')

    async def read(self, workspace_id: str, org_id: str = None) -> WorkSpaceNumbers:
        """
        List the PSTN phone numbers associated with a specific workspace, by ID, within the organization. Also shows
        the location and Organization associated with the workspace.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:workspaces_read.

        :param workspace_id: List numbers for this workspace.
        :type workspace_id: str
        :param org_id: List numbers for a workspace within this organization.
        :type org_id: str
        :return: Workspace numbers
        :rtype: WorkSpaceNumbers
        """
        params = org_id and {'org_id': org_id} or None
        url = self.ep(workspace_id=workspace_id)
        data = await self.get(url=url, params=params)
        return parse_obj_as(WorkSpaceNumbers, data)


@dataclass(init=False)
class AsWorkspaceSettingsApi(AsApiChild, base='workspaces'):
    """
    API for all workspace settings.

    Most of the workspace settings are equivalent to corresponding user settings. For these settings the attributes of
    this class are instances of the respective user settings APIs. When calling endpoints of these APIs workspace IDs
    need to be passed to the ``person_id`` parameter of the called function.
    """
    call_intercept: AsCallInterceptApi
    call_waiting: AsCallWaitingApi
    caller_id: AsCallerIdApi
    forwarding: AsPersonForwardingApi
    monitoring: AsMonitoringApi
    numbers: AsWorkspaceNumbersApi
    permissions_in: AsIncomingPermissionsApi
    permissions_out: AsOutgoingPermissionsApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.call_intercept = AsCallInterceptApi(session=session, workspaces=True)
        self.call_waiting = AsCallWaitingApi(session=session, workspaces=True)
        self.caller_id = AsCallerIdApi(session=session, workspaces=True)
        self.forwarding = AsPersonForwardingApi(session=session, workspaces=True)
        self.monitoring = AsMonitoringApi(session=session, workspaces=True)
        self.numbers = AsWorkspaceNumbersApi(session=session)
        self.permissions_in = AsIncomingPermissionsApi(session=session, workspaces=True)
        self.permissions_out = AsOutgoingPermissionsApi(session=session, workspaces=True)


class AsWorkspacesApi(AsApiChild, base='workspaces'):
    """
    Workspaces API

    Workspaces represent where people work, such as conference rooms, meeting spaces, lobbies, and lunch rooms. Devices
    may be associated with workspaces.

    Viewing the list of workspaces in an organization requires an administrator auth token with
    the spark-admin:workspaces_read scope. Adding, updating, or deleting workspaces in an organization requires an
    administrator auth token with the spark-admin:workspaces_write scope.

    The Workspaces API can also be used by partner administrators acting as administrators of a different organization
    than their own. In those cases an orgId value must be supplied, as indicated in the reference documentation for
    the relevant endpoints.
    """

    def list_gen(self, workspace_location_id: str = None, floor_id: str = None, display_name: str = None,
             capacity: int = None,
             workspace_type: WorkSpaceType = None, calling: CallingType = None, calendar: CalendarType = None,
             org_id: str = None, **params) -> AsyncGenerator[Workspace, None, None]:
        """
        List Workspaces

        List workspaces. Use query parameters to filter the response. The orgId parameter can only be used by admin
        users of another organization (such as partners). The workspaceLocationId, floorId, capacity and type fields
        will only be present for workspaces that have a value set for them. The special values notSet (for filtering
        on category) and -1 (for filtering on capacity) can be used to filter for workspaces without a type and/or
        capacity.

        :param workspace_location_id: Location associated with the workspace
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param display_name: List workspaces by display name.
        :type display_name: str
        :param capacity: List workspaces with the given capacity. Must be -1 or higher. A value of -1 lists workspaces
            with no capacity set.
        :type capacity: int
        :param workspace_type: List workspaces by type.
        :type workspace_type: :class:`WorkSpaceType`
        :param calling: List workspaces by calling type.
        :type calling: :class:`CallingType`
        :param calendar: List workspaces by calendar type.
        :type calendar: :class:`CalendarType`
        :param org_id: List workspaces in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: generator of :class:`Workspace` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        if workspace_type is not None:
            params.pop('workspaceType')
            params['type'] = workspace_type
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Workspace, params=params)

    async def list(self, workspace_location_id: str = None, floor_id: str = None, display_name: str = None,
             capacity: int = None,
             workspace_type: WorkSpaceType = None, calling: CallingType = None, calendar: CalendarType = None,
             org_id: str = None, **params) -> List[Workspace]:
        """
        List Workspaces

        List workspaces. Use query parameters to filter the response. The orgId parameter can only be used by admin
        users of another organization (such as partners). The workspaceLocationId, floorId, capacity and type fields
        will only be present for workspaces that have a value set for them. The special values notSet (for filtering
        on category) and -1 (for filtering on capacity) can be used to filter for workspaces without a type and/or
        capacity.

        :param workspace_location_id: Location associated with the workspace
        :type workspace_location_id: str
        :param floor_id: Floor associated with the workspace.
        :type floor_id: str
        :param display_name: List workspaces by display name.
        :type display_name: str
        :param capacity: List workspaces with the given capacity. Must be -1 or higher. A value of -1 lists workspaces
            with no capacity set.
        :type capacity: int
        :param workspace_type: List workspaces by type.
        :type workspace_type: :class:`WorkSpaceType`
        :param calling: List workspaces by calling type.
        :type calling: :class:`CallingType`
        :param calendar: List workspaces by calendar type.
        :type calendar: :class:`CalendarType`
        :param org_id: List workspaces in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: generator of :class:`Workspace` instances
        """
        params.update((to_camel(k), v)
                      for i, (k, v) in enumerate(locals().items())
                      if i and k != 'params' and v is not None)
        if workspace_type is not None:
            params.pop('workspaceType')
            params['type'] = workspace_type
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=Workspace, params=params)]

    async def create(self, settings: Workspace, org_id: str = None):
        """
        Create a Workspace

        Create a workspace. The workspaceLocationId, floorId, capacity, type and notes parameters are optional, and
        omitting them will result in the creation of a workspace without these values set, or set to their default.
        A workspaceLocationId must be provided when the floorId is set. Calendar and calling can also be set for a
        new workspace. Omitting them will default to free calling and no calendaring. The orgId parameter can only be
        used by admin users of another organization (such as partners).

        :param settings: settings for new Workspace
        :type settings: :class:`Workspace`
        :param org_id: OrgId associated with the workspace. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: new workspace
        :rtype: :class:`Workspace`
        """
        if org_id:
            settings.org_id = org_id
        data = settings.update_or_create()
        url = self.ep()
        data = await self.post(url, data=data)
        return Workspace.parse_obj(data)

    async def details(self, workspace_id) -> Workspace:
        """
        Get Workspace Details

        Shows details for a workspace, by ID. The workspaceLocationId, floorId, capacity, type and notes fields will
        only be present if they have been set for the workspace.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :return: workspace details
        :rtype: :class:`Workspace`
        """
        url = self.ep(workspace_id)
        return Workspace.parse_obj(await self.get(url))

    async def update(self, workspace_id, settings: Workspace) -> Workspace:
        """
        Update a Workspace

        Updates details for a workspace, by ID. Specify the workspace ID in the workspaceId parameter in the URI.
        Include all details for the workspace that are present in a GET request for the workspace details. Not
        including the optional capacity, type or notes fields will result in the fields no longer being defined
        for the workspace. A workspaceLocationId must be provided when the floorId is set. The workspaceLocationId,
        floorId, calendar and calling fields do not change when omitted from the update request. Updating the
        calling parameter is not supported.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        :param settings: new workspace settings
        :type settings: :class:`Workspace`
        :return: updated workspace
        :rtype: :class:`Workspace`
        """
        url = self.ep(workspace_id)
        j_data = settings.update_or_create(for_update=True)
        data = await self.put(url, data=j_data)
        return Workspace.parse_obj(data)

    async def delete_workspace(self, workspace_id):
        """
        Delete a Workspace

        Deletes a workspace, by ID. Will also delete all devices associated with the workspace. Any deleted devices
        will need to be reactivated.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str
        """
        url = self.ep(workspace_id)
        await self.delete(url)


@dataclass(init=False)
class AsWebexSimpleApi:
    """
    The main API object
    """

    #: Attachment actions API :class:`AsAttachmentActionsApi`
    attachment_actions: AsAttachmentActionsApi
    #: CDR API :class:`AsDetailedCDRApi`
    cdr: AsDetailedCDRApi
    #: devices API :class:`AsDevicesApi`
    devices: AsDevicesApi
    #: events API; :class:`AsEventsApi`
    events: AsEventsApi
    #: groups API :class:`AsGroupsApi`
    groups: AsGroupsApi
    #: Licenses API :class:`AsLicensesApi`
    licenses: AsLicensesApi
    #: Location API :class:`AsLocationsApi`
    locations: AsLocationsApi
    #: membership API :class:`AsMembershipApi`
    membership: AsMembershipApi
    #: Messages API :class:`AsMessagesApi`
    messages: AsMessagesApi
    #: organization settings API
    organizations: AsOrganizationApi
    #: Person settings API :class:`AsPersonSettingsApi`
    person_settings: AsPersonSettingsApi
    #: People API :class:`AsPeopleApi`
    people: AsPeopleApi
    #: Reports API :class:`AsReportsApi`
    reports: AsReportsApi
    #: Rooms API :class:`AsRoomsApi`
    rooms: AsRoomsApi
    #: Room tabs API :class:`AsRoomTabsApi`
    room_tabs: AsRoomTabsApi
    #: Teams API :class:`AsTeamsApi`
    teams: AsTeamsApi
    #: Team memberships API :class:`AsTeamMembershipsApi`
    team_memberships: AsTeamMembershipsApi
    #: Telephony (features) API :class:`AsTelephonyApi`
    telephony: AsTelephonyApi
    #: Webhooks API :class:`AsWebhookApi`
    webhook: AsWebhookApi
    #: Workspaces API :class:`AsWorkspacesApi`
    workspaces: AsWorkspacesApi
    #: Workspace locations API; :class:`AsWorkspaceLocationApi`
    workspace_locations: AsWorkspaceLocationApi
    #: Workspace setting API :class:`AsWorkspaceSettingsApi`
    workspace_settings: AsWorkspaceSettingsApi
    #: :class:`AsRestSession` used for all API requests
    session: AsRestSession

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

        session = AsRestSession(tokens=tokens, concurrent_requests=concurrent_requests)
        self.attachment_actions = AsAttachmentActionsApi(session=session)
        self.cdr = AsDetailedCDRApi(session=session)
        self.devices = AsDevicesApi(session=session)
        self.events = AsEventsApi(session=session)
        self.groups = AsGroupsApi(session=session)
        self.licenses = AsLicensesApi(session=session)
        self.locations = AsLocationsApi(session=session)
        self.membership = AsMembershipApi(session=session)
        self.messages = AsMessagesApi(session=session)
        self.organizations = AsOrganizationApi(session=session)
        self.person_settings = AsPersonSettingsApi(session=session)
        self.people = AsPeopleApi(session=session)
        self.reports = AsReportsApi(session=session)
        self.rooms = AsRoomsApi(session=session)
        self.room_tabs = AsRoomTabsApi(session=session)
        self.teams = AsTeamsApi(session=session)
        self.team_memberships = AsTeamMembershipsApi(session=session)
        self.telephony = AsTelephonyApi(session=session)
        self.webhook = AsWebhookApi(session=session)
        self.workspaces = AsWorkspacesApi(session=session)
        self.workspace_locations = AsWorkspaceLocationApi(session=session)
        self.workspace_settings = AsWorkspaceSettingsApi(session=session)
        self.session = session

    @property
    def access_token(self) -> str:
        """
        access token used for all requests

        :return: access token
        :rtype: str
        """
        return self.session.access_token

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
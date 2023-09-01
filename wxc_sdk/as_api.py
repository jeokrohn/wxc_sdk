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
from dateutil.parser import isoparse
from enum import Enum
from io import BufferedReader
from typing import Union, Dict, Optional, Literal, List

from aiohttp import FormData
from pydantic import TypeAdapter

from wxc_sdk.all_types import *
from wxc_sdk.as_rest import AsRestSession
from wxc_sdk.base import to_camel, StrOrDict, dt_iso_str, enum_str
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
CALLING_DATA_TIMEOUT_PROTECTION = False


__all__ = ['AsAccessCodesApi', 'AsAgentCallerIdApi', 'AsAnnouncementApi', 'AsAnnouncementsRepositoryApi',
           'AsApiChild', 'AsAppServicesApi', 'AsAttachmentActionsApi', 'AsAutoAttendantApi', 'AsBargeApi',
           'AsCQPolicyApi', 'AsCallInterceptApi', 'AsCallParkApi', 'AsCallPickupApi', 'AsCallQueueApi',
           'AsCallRecordingApi', 'AsCallWaitingApi', 'AsCallerIdApi', 'AsCallingBehaviorApi',
           'AsCallparkExtensionApi', 'AsCallsApi', 'AsDetailedCDRApi', 'AsDeviceSettingsJobsApi', 'AsDevicesApi',
           'AsDialPlanApi', 'AsDndApi', 'AsEventsApi', 'AsExecAssistantApi', 'AsForwardingApi', 'AsGroupsApi',
           'AsHotelingApi', 'AsHuntGroupApi', 'AsIncomingPermissionsApi', 'AsInternalDialingApi', 'AsJobsApi',
           'AsLicensesApi', 'AsLocationInterceptApi', 'AsLocationMoHApi', 'AsLocationNumbersApi',
           'AsLocationVoicemailSettingsApi', 'AsLocationsApi', 'AsManageNumbersJobsApi', 'AsMeetingChatsApi',
           'AsMeetingClosedCaptionsApi', 'AsMeetingInviteesApi', 'AsMeetingParticipantsApi',
           'AsMeetingPreferencesApi', 'AsMeetingQandAApi', 'AsMeetingQualitiesApi', 'AsMeetingTranscriptsApi',
           'AsMeetingsApi', 'AsMembershipApi', 'AsMessagesApi', 'AsMonitoringApi', 'AsNumbersApi',
           'AsOrganisationVoicemailSettingsAPI', 'AsOrganizationApi', 'AsOutgoingPermissionsApi', 'AsPagingApi',
           'AsPeopleApi', 'AsPersonForwardingApi', 'AsPersonSettingsApi', 'AsPersonSettingsApiChild',
           'AsPreferredAnswerApi', 'AsPremisePstnApi', 'AsPrivacyApi', 'AsPrivateNetworkConnectApi',
           'AsPushToTalkApi', 'AsReceptionistApi', 'AsReceptionistContactsDirectoryApi', 'AsReportsApi',
           'AsRestSession', 'AsRoomTabsApi', 'AsRoomsApi', 'AsRouteGroupApi', 'AsRouteListApi', 'AsScheduleApi',
           'AsTeamMembershipsApi', 'AsTeamsApi', 'AsTelephonyApi', 'AsTelephonyDevicesApi', 'AsTelephonyLocationApi',
           'AsTransferNumbersApi', 'AsTrunkApi', 'AsVirtualLinesApi', 'AsVoiceMessagingApi', 'AsVoicePortalApi',
           'AsVoicemailApi', 'AsVoicemailGroupsApi', 'AsVoicemailRulesApi', 'AsWebexSimpleApi', 'AsWebhookApi',
           'AsWorkspaceDevicesApi', 'AsWorkspaceLocationApi', 'AsWorkspaceLocationFloorApi', 'AsWorkspaceNumbersApi',
           'AsWorkspaceSettingsApi', 'AsWorkspacesApi']


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
        return AttachmentAction.model_validate(data)


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

    def get_cdr_history_gen(self, start_time: Union[str, datetime] = None, end_time: Union[datetime, str] = None,
                        locations: list[str] = None, **params) -> AsyncGenerator[CDR, None, None]:
        """
        Provides Webex Calling Detailed Call History data for your organization.

        Results can be filtered with the startTime, endTime and locations request parameters. The startTime and endTime
        parameters specify the start and end of the time period for the Detailed Call History reports you wish to
        collect.
        The API will return all reports that were created between startTime and endTime.

        :param start_time: Time of the first report you wish to collect. (report time is the time the call finished).
            Can be a datetime object or an ISO-8601 datetime string to be
            parsed by :meth:`dateutil.parser.isoparse`.

            Note: The specified time must be between 5 minutes ago and 48 hours ago.
        :type start_time: Union[str, datetime]
        :param end_time: Time of the last report you wish to collect. Note: The specified time should be earlier than
            startTime and no earlier than 48 hours ago. Can be a datetime object or an ISO-8601 datetime string to be
            parsed by :meth:`dateutil.parser.isoparse`.
        :type end_time: Union[str, datetime]
        :param locations: Names of the location (as shown in Control Hub). Up to 10 comma-separated locations can be
            provided. Allows you to query reports by location.
        :type locations: list[str]
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

        def guess_datetime(dt: Union[datetime, str]) -> datetime:
            if isinstance(dt, str):
                r = isoparse(dt)
            else:
                r = dt_iso_str(dt)
            return r

        params['startTime'] = guess_datetime(start_time)
        params['endTime'] = guess_datetime(end_time)
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=url, model=CDR, params=params, item_key='items')

    async def get_cdr_history(self, start_time: Union[str, datetime] = None, end_time: Union[datetime, str] = None,
                        locations: list[str] = None, **params) -> List[CDR]:
        """
        Provides Webex Calling Detailed Call History data for your organization.

        Results can be filtered with the startTime, endTime and locations request parameters. The startTime and endTime
        parameters specify the start and end of the time period for the Detailed Call History reports you wish to
        collect.
        The API will return all reports that were created between startTime and endTime.

        :param start_time: Time of the first report you wish to collect. (report time is the time the call finished).
            Can be a datetime object or an ISO-8601 datetime string to be
            parsed by :meth:`dateutil.parser.isoparse`.

            Note: The specified time must be between 5 minutes ago and 48 hours ago.
        :type start_time: Union[str, datetime]
        :param end_time: Time of the last report you wish to collect. Note: The specified time should be earlier than
            startTime and no earlier than 48 hours ago. Can be a datetime object or an ISO-8601 datetime string to be
            parsed by :meth:`dateutil.parser.isoparse`.
        :type end_time: Union[str, datetime]
        :param locations: Names of the location (as shown in Control Hub). Up to 10 comma-separated locations can be
            provided. Allows you to query reports by location.
        :type locations: list[str]
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

        def guess_datetime(dt: Union[datetime, str]) -> datetime:
            if isinstance(dt, str):
                r = isoparse(dt)
            else:
                r = dt_iso_str(dt)
            return r

        params['startTime'] = guess_datetime(start_time)
        params['endTime'] = guess_datetime(end_time)
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
            body['customizations'] = json.loads(customization.customizations.model_dump_json())
        data = await self.post(url=url, params=params, json=body)
        return StartJobResponse.model_validate(data)

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
        return StartJobResponse.model_validate(data)

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
    Devices represent cloud-registered Webex RoomOS devices or IP Phones. Devices may be associated with Workspaces
    or People.

    The following scopes are required for performing the specified actions:

    Searching and viewing details for devices requires an auth token with the spark:devices_read scope.

    Updating or deleting your devices requires an auth token with the spark:devices_write scope.

    Viewing the list of all devices in an organization requires an administrator auth token with
    the spark-admin:devices_read scope.

    Adding, updating, or deleting all devices in an organization requires an administrator auth token with
    the spark-admin:devices_write scope.

    Generating an activation code requires an auth token with the identity:placeonetimepassword_create scope.
    """

    #: device jobs Api
    settings_jobs: AsDeviceSettingsJobsApi

    def __init__(self, *, session: AsRestSession):
        super().__init__(session=session)
        self.settings_jobs = AsDeviceSettingsJobsApi(session=session)

    def list_gen(self, person_id: str = None, workspace_id: str = None, workspace_location_id: str = None,
             display_name: str = None, product: str = None,
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
        :param workspace_location_id: List devices by workspace location ID.
        :type workspace_location_id: str
        :param display_name: List devices with this display name.
        :type display_name: str
        :param product: List devices with this product name.
        :type product: str
        :param product_type: List devices with this type. Possible values: roomdesk, phone, accessory, webexgo, unknown
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
        pt = params.pop('productType', None)
        if pt is not None:
            params['type'] = pt
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Device, params=params, item_key='items')

    async def list(self, person_id: str = None, workspace_id: str = None, workspace_location_id: str = None,
             display_name: str = None, product: str = None,
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
        :param workspace_location_id: List devices by workspace location ID.
        :type workspace_location_id: str
        :param display_name: List devices with this display name.
        :type display_name: str
        :param product: List devices with this product name.
        :type product: str
        :param product_type: List devices with this type. Possible values: roomdesk, phone, accessory, webexgo, unknown
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
        pt = params.pop('productType', None)
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
        return Device.model_validate(data)

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
        return Device.model_validate(data)

    async def activation_code(self, workspace_id: str = None, person_id: str = None, model: str = None,
                        org_id: str = None) -> ActivationCodeResponse:
        """
        Create a Device Activation Code

        Generate an activation code for a device in a specific workspace by workspaceId. Currently, activation codes
        may only be generated for shared workspaces--personal mode is not supported.

        :param workspace_id: The ID of the workspace where the device will be activated.
        :type workspace_id: str
        :param person_id: The ID of the person who will own the device once activated.
        :type person_id: str
        :param model: The model of the device being created.
        :type model: str
        :param org_id: The organization associated with the activation code generated.
        :type org_id: str
        :rtype: ActivationCodeResponse
        """
        params = org_id and {'orgId': org_id} or None
        body = {}
        if workspace_id is not None:
            body['workspaceId'] = workspace_id
        if person_id is not None:
            body['personId'] = person_id
        if model is not None:
            body['model'] = model
        url = self.ep('activationCode')
        data = await self.post(url=url, json=body, params=params)
        return ActivationCodeResponse.model_validate(data)

    async def create_by_mac_address(self, mac: str, workspace_id: str = None, person_id: str = None,
                              model: str = None, password: str = None, org_id: str = None) -> Device:
        """
        Create a phone by it's MAC address in a specific workspace or for a person.
        Specify the mac, model and either workspaceId or personId.

        :param mac: The MAC address of the device being created.
        :type mac: str
        :param workspace_id: The ID of the workspace where the device will be activated.
        :type workspace_id: str
        :param person_id: The ID of the person who will own the device once activated.
        :type person_id: str
        :param model: The model of the device being created.
        :type model: str
        :param password: SIP password to be configured for the phone, only required with third party devices.
        :type password: str
        :param org_id: The organization associated with the device.
        :type org_id: str
        :return: created device information
        :rtype: Device
        """
        params = org_id and {'orgId': org_id} or None
        body = {'mac': mac}
        if workspace_id is not None:
            body['workspaceId'] = workspace_id
        if person_id is not None:
            body['personId'] = person_id
        if model is not None:
            body['model'] = model
        if password is not None:
            body.password = password
        url = self.ep()
        data = await super().post(url=url, json=body, params=params)
        return Device.model_validate(data)


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
        return ComplianceEvent.model_validate(data)


class AsGroupsApi(AsApiChild, base='groups'):
    """
    Groups contain a collection of members in Webex. A member represents a Webex user. A group is used to assign
    templates and settings to the set of members contained in a group. To create and manage a group, including adding
    and removing members from a group, an auth token containing the identity:groups_rw is required. Searching and
    viewing members of a group requires an auth token with a scope of identity:groups_read.
    To learn more about managing people to use as members in the /groups API please refer to the People API.
    """

    def list_gen(self, include_members: bool = None, attributes: str = None, sort_by: str = None,
             sort_order: str = None, list_filter: str = None, org_id: str = None,
             **params) -> AsyncGenerator[Group, None, None]:
        """
        List groups in your organization.

        :param include_members: Include members in list response
        :type include_members: bool
        :param attributes: comma separated list of attributes to return
        :type attributes: str
        :param sort_by: attribute to sort by
        :type sort_by: str
        :param sort_order: sort order, ascending or descending
        :type sort_order: str
        :param org_id: List groups in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param list_filter: Searches the group by displayName with an operator and a value. The available operators
            are eq (equal) and sw (starts with). Only displayName can be used to filter results.
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
        List groups in your organization.

        :param include_members: Include members in list response
        :type include_members: bool
        :param attributes: comma separated list of attributes to return
        :type attributes: str
        :param sort_by: attribute to sort by
        :type sort_by: str
        :param sort_order: sort order, ascending or descending
        :type sort_order: str
        :param org_id: List groups in this organization. Only admin users of another organization (such as partners)
            may use this parameter.
        :type org_id: str
        :param list_filter: Searches the group by displayName with an operator and a value. The available operators
            are eq (equal) and sw (starts with). Only displayName can be used to filter results.
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
        body = settings.model_dump_json(exclude={'group_id': True,
                                                 'members': {'__all__': {'member_type': True,
                                                                         'display_name': True,
                                                                         'operation': True}},
                                                 'created': True,
                                                 'last_modified': True})
        data = await self.post(url, data=body)
        return Group.model_validate(data)

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
        return Group.model_validate(data)

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
            body = settings.model_dump_json(exclude={'group_id': True,
                                                     'members': {'__all__': {'member_type': True,
                                                                             'display_name': True}},
                                                     'created': True,
                                                     'last_modified': True})
        else:
            body = 'purgeAllValues:{"attributes":["members"]}'
        data = await self.patch(url, data=body)
        return Group.model_validate(data)

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
        return License.model_validate(await self.get(ep))


class AsLocationsApi(AsApiChild, base='locations'):
    """
    Location API

    Locations allow you to organize users and workspaces based on a physical location. You can configure both calling
    and workspace management functions into the same location. You can also create and inspect locations in Webex
    Control Hub. See Locations on Control Hub for more information.

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

    async def details(self, location_id: str, org_id: str = None) -> Location:
        """
        Shows details for a location, by ID.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param org_id: Get location common attributes for this organization.
        :type org_id: str

        :return: location details
        :rtype: :class:`Location`
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep(location_id)
        return Location.model_validate(await self.get(ep, params=params))

    async def create(self, name: str, time_zone: str, preferred_language: str, announcement_language: str, address1: str,
               city: str, state: str, postal_code: str, country: str, address2: str = None, org_id: str = None) -> str:
        """
        Create a new Location for a given organization. Only an admin in the organization can create a new Location.

        Creating a location in your organization requires an administrator auth token with
        the spark-admin:locations_write.

        Partners may specify orgId query parameter to create location in managed organization.

        The following body parameters are required to create a new location: name, timeZone, preferredLanguage,
        address, announcementLanguage.


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
        # TODO: this is broken see conversation in "Implementation - Locations as a Common Construct"
        if (tz := body.pop('timeZone', None)) is not None:
            body['timezone'] = tz
        body['address'] = address
        params = org_id and {'orgId': org_id} or None
        url = self.ep()
        data = await self.post(url=url, json=body, params=params)
        # TODO: doc issue, looks like this endpoint returns location details, but the doc only mentions "id"
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
        settings_copy = settings.model_copy(deep=True)
        if settings_copy.address and not settings_copy.address.address2:
            settings_copy.address.address2 = None

        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id)

        # TODO: this is broken see conversation in "Implementation - Locations as a Common Construct"
        data = json.loads(settings_copy.model_dump_json(exclude={'location_id', 'org_id'}, exclude_none=False, exclude_unset=True))
        data['timezone'] = data.pop('timeZone', None)
        await self.put(url=url, json=data, params=params)

        # data = settings_copy.json(exclude={'location_id', 'org_id'}, exclude_none=False, exclude_unset=True)
        # await self.put(url=url, data=data, params=params)

    async def list_floors(self, location_id: str) -> List[Floor]:
        """
        List location floors.
        Requires an administrator auth token with the spark-admin:locations_read scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str

        documentation: https://developer.webex.com/docs/api/v1/locations/list-location-floors
        """
        url = self.ep(f'{location_id}/floors')
        data = await super().get(url=url)
        return TypeAdapter(list[Floor]).validate_python(data["items"])

    async def create_floor(self, location_id: str, floor_number: int, display_name: str = None) -> Floor:
        """
        Create a new floor in the given location. The displayName parameter is optional, and omitting it will result in
        the creation of a floor without that value set.
        Requires an administrator auth token with the spark-admin:locations_write scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_number: The floor number.
        :type floor_number: int
        :param display_name: The floor display name.
        :type display_name: str

        documentation: https://developer.webex.com/docs/api/v1/locations/create-a-location-floor
        """
        body = CreateLocationFloorBody()
        if floor_number is not None:
            body.floor_number = floor_number
        if display_name is not None:
            body.display_name = display_name
        url = self.ep(f'{location_id}/floors')
        data = await super().post(url=url, data=body.model_dump_json())
        return Floor.model_validate(data)

    async def floor_details(self, location_id: str, floor_id: str) -> Floor:
        """
        Shows details for a floor, by ID. Specify the floor ID in the floorId parameter in the URI.
        Requires an administrator auth token with the spark-admin:locations_read scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str

        documentation: https://developer.webex.com/docs/api/v1/locations/get-location-floor-details
        """
        url = self.ep(f'{location_id}/floors/{floor_id}')
        data = await super().get(url=url)
        return Floor.model_validate(data)

    async def update_floor(self, location_id: str, floor_id: str, floor_number: int, display_name: str = None) -> Floor:
        """
        Updates details for a floor, by ID. Specify the floor ID in the floorId parameter in the URI. Include all
        details for the floor returned by a previous call to Get Location Floor Details. Omitting the optional
        displayName field will result in that field no longer being defined for the floor.
        Requires an administrator auth token with the spark-admin:locations_write scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str
        :param floor_number: The floor number.
        :type floor_number: int
        :param display_name: The floor display name.
        :type display_name: str

        documentation: https://developer.webex.com/docs/api/v1/locations/update-a-location-floor
        """
        body = CreateLocationFloorBody()
        if floor_number is not None:
            body.floor_number = floor_number
        if display_name is not None:
            body.display_name = display_name
        url = self.ep(f'{location_id}/floors/{floor_id}')
        data = await super().put(url=url, data=body.model_dump_json())
        return Floor.model_validate(data)

    async def delete_floor(self, location_id: str, floor_id: str):
        """
        Deletes a floor, by ID.
        Requires an administrator auth token with the spark-admin:locations_write scope.

        :param location_id: A unique identifier for the location.
        :type location_id: str
        :param floor_id: A unique identifier for the floor.
        :type floor_id: str

        documentation: https://developer.webex.com/docs/api/v1/locations/delete-a-location-floor
        """
        url = self.ep(f'{location_id}/floors/{floor_id}')
        await super().delete(url=url)
        return


class AsMeetingChatsApi(AsApiChild, base='meetings/postMeetingChats'):
    """
    Chats are content captured in a meeting when chat messages are sent between the participants within a meeting. This feature allows a Compliance Officer to access the in-meeting chat content.
    The Compliance Officer can use the Meeting Chats API to retrieve the chats of a meeting and to delete all chats associated with a meeting. private chats are text messages between two people. group chats are for larger breakout spaces. Meeting chats are different from room messages in that there is no catch-up propagation. For example, if a user joins a meeting late only, chat messages that are created from then on, will be propagated to this user. To understand which user saw which message if they joined late, you have to query the meetingParticipants REST resource for the joined/left times and compare to the meetingsChat chatTime field.
    The Webex meetings chat functionality and API endpoint described here is "upon-request" and not enabled by default. If you need it enabled for your org, or if you need help, please contact the Webex Developer Support team at devsupport@webex.com.
    """

    def list_gen(self, meeting_id: str, offset: int = None, **params) -> AsyncGenerator[ChatObject, None, None]:
        """
        Lists the meeting chats of a finished meeting instance specified by meetingId. You can set a maximum number of chats to return.
        Use this operation to list the chats of a finished meeting instance when they are ready. Please note that only meeting instances in state ended are supported for meetingId. Meeting series, scheduled meetings and in-progress meeting instances are not supported.

        :param meeting_id: A unique identifier for the meeting instance to which the chats belong. The meeting ID of a scheduled personal room meeting is not supported.
        :type meeting_id: str
        :param offset: Offset from the first result that you want to fetch.
        :type offset: int
        """
        params['meetingId'] = meeting_id
        if offset is not None:
            params['offset'] = offset
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ChatObject, params=params)

    async def list(self, meeting_id: str, offset: int = None, **params) -> List[ChatObject]:
        """
        Lists the meeting chats of a finished meeting instance specified by meetingId. You can set a maximum number of chats to return.
        Use this operation to list the chats of a finished meeting instance when they are ready. Please note that only meeting instances in state ended are supported for meetingId. Meeting series, scheduled meetings and in-progress meeting instances are not supported.

        :param meeting_id: A unique identifier for the meeting instance to which the chats belong. The meeting ID of a scheduled personal room meeting is not supported.
        :type meeting_id: str
        :param offset: Offset from the first result that you want to fetch.
        :type offset: int
        """
        params['meetingId'] = meeting_id
        if offset is not None:
            params['offset'] = offset
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=ChatObject, params=params)]

    async def delete(self, meeting_id: str):
        """
        Deletes the meeting chats of a finished meeting instance specified by meetingId.
        Use this operation to delete the chats of a finished meeting instance when they are ready. Please note that only meeting instances in state ended are supported for meetingId. Meeting series, scheduled meetings and in-progress meeting instances are not supported.

        :param meeting_id: A unique identifier for the meeting instance to which the chats belong. Meeting IDs of a scheduled personal room meeting are not supported.
        :type meeting_id: str
        """
        params = {}
        params['meetingId'] = meeting_id
        url = self.ep()
        await super().delete(url=url, params=params)
        return


class AsMeetingClosedCaptionsApi(AsApiChild, base='meetingClosedCaptions'):
    """
    Meeting Closed Captions APIs are enabled upon request, and are not available by default. Please contact the Webex
    Developer Support team at devsupport@webex.com if you would like to enable this feature for your organization.
    Meeting closed captions are the automatic transcriptions of what is being said during a meeting in real-time.
    Closed captions appear after being enabled during a meeting and can be translated to a participant's language.
    A closed caption snippet is a short text snippet from a meeting closed caption which was spoken by a particular
    participant in the meeting. A meeting's closed captions consists of many snippets.
    The Closed Captions API manages meeting closed captions and snippets. You can list meeting closed captions, as well
    as list and download snippets. Closed captions can be retrieved in either Web Video Text Tracks (VTT) or plain text
    (TXT) format via the download links provided by the vttDownloadLink and txtDownloadlink response properties,
    respectively.
    Refer to the Meetings API Scopes section of Meetings Overview guide for the scopes required for each API.
    Notes:
    Currently, closed caption APIs are only supported for the Compliance Officer role.
    Closed captions will be available 15 minutes after the meeting is finished.
    """

    def list_gen(self, meeting_id: str, **params) -> AsyncGenerator[ClosedCaption, None, None]:
        """
        Lists closed captions of a finished meeting instance specified by meetingId.

        :param meeting_id: Unique identifier for the meeting instance which the closed captions belong to. This
            parameter only applies to ended meeting instnaces. It does not apply to meeting series, scheduled meetings
            or scheduled personal room meetings.
        :type meeting_id: str
        """
        params['meetingId'] = meeting_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ClosedCaption, params=params)

    async def list(self, meeting_id: str, **params) -> List[ClosedCaption]:
        """
        Lists closed captions of a finished meeting instance specified by meetingId.

        :param meeting_id: Unique identifier for the meeting instance which the closed captions belong to. This
            parameter only applies to ended meeting instnaces. It does not apply to meeting series, scheduled meetings
            or scheduled personal room meetings.
        :type meeting_id: str
        """
        params['meetingId'] = meeting_id
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=ClosedCaption, params=params)]

    def list_snippets_gen(self, closed_caption_id: str, meeting_id: str, **params) -> AsyncGenerator[CCSnippet, None, None]:
        """
        Lists snippets of a meeting closed caption specified by closedCaptionId.

        :param closed_caption_id: Unique identifier for the meeting closed caption which the snippets belong to.
        :type closed_caption_id: str
        :param meeting_id: Unique identifier for the meeting instance which the closed caption snippets belong to. This
            parameter only applies to ended meeting instances. It does not apply to meeting series, scheduled meetings
            or scheduled personal room meetings.
        :type meeting_id: str
        """
        params['meetingId'] = meeting_id
        url = self.ep(f'{closed_caption_id}/snippets')
        return self.session.follow_pagination(url=url, model=CCSnippet, params=params)

    async def list_snippets(self, closed_caption_id: str, meeting_id: str, **params) -> List[CCSnippet]:
        """
        Lists snippets of a meeting closed caption specified by closedCaptionId.

        :param closed_caption_id: Unique identifier for the meeting closed caption which the snippets belong to.
        :type closed_caption_id: str
        :param meeting_id: Unique identifier for the meeting instance which the closed caption snippets belong to. This
            parameter only applies to ended meeting instances. It does not apply to meeting series, scheduled meetings
            or scheduled personal room meetings.
        :type meeting_id: str
        """
        params['meetingId'] = meeting_id
        url = self.ep(f'{closed_caption_id}/snippets')
        return [o async for o in self.session.follow_pagination(url=url, model=CCSnippet, params=params)]

    async def download_snippets(self, closed_caption_id: str, meeting_id: str, format: str = None):
        """
        Download meeting closed caption snippets from the meeting closed caption specified by closedCaptionId formatted
        either as a Video Text Track (.vtt) file or plain text (.txt) file.

        :param closed_caption_id: Unique identifier for the meeting closed caption.
        :type closed_caption_id: str
        :param meeting_id: Unique identifier for the meeting instance which the closed caption snippets belong to. This
            parameter only applies to meeting instances in the ended state. It does not apply to meeting series,
            scheduled meetings or scheduled personal room meetings.
        :type meeting_id: str
        :param format: Format for the downloaded meeting closed caption snippets. Possible values: vtt, txt
        :type format: str
        """
        # TODO: verify return and adapt
        params = {}
        params['meetingId'] = meeting_id
        if format is not None:
            params['format'] = format
        url = self.ep(f'{closed_caption_id}/download')
        await super().get(url=url, params=params)
        return


class AsMeetingInviteesApi(AsApiChild, base='meetingInvitees'):
    """
    This API manages invitees' relationships to a meeting.
    You can use the Meeting Invitees API to list, create, update, and delete invitees.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    """

    def list_gen(self, meeting_id: str, host_email: str = None, panelist: bool = None,
             **params) -> AsyncGenerator[Invitee, None, None]:
        """
        Lists meeting invitees for a meeting with a specified meetingId. You can set a maximum number of invitees to
        return. This operation can be used for meeting series, scheduled meetings, and ended or ongoing meeting
        instance objects. If the specified meetingId is for a meeting series, the invitees for the series will be
        listed; if the meetingId is for a scheduled meeting, the invitees for the particular scheduled meeting will
        be listed; if the meetingId is for an ended or ongoing meeting instance, the invitees for the particular
        meeting instance will be listed. See the Webex Meetings guide for more information about the types of
        meetings. The list returned is sorted in ascending order by email address. Long result sets are split into
        pages.

        :param meeting_id: Unique identifier for the meeting for which invitees are being requested. The meeting
            can be a meeting series, a scheduled meeting, or a meeting instance which has ended or is ongoing. The
            meeting ID of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or
            application calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of
            a user in a site they manage and the API will return meeting invitees that are hosted by that user.
        :type host_email: str
        :param panelist: Filter invitees or attendees for webinars only. If true,
            returns invitees. If false, returns attendees. If null, returns both invitees and attendees.
        :type panelist: bool
        """
        params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if panelist is not None:
            params['panelist'] = str(panelist).lower()
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Invitee, params=params)

    async def list(self, meeting_id: str, host_email: str = None, panelist: bool = None,
             **params) -> List[Invitee]:
        """
        Lists meeting invitees for a meeting with a specified meetingId. You can set a maximum number of invitees to
        return. This operation can be used for meeting series, scheduled meetings, and ended or ongoing meeting
        instance objects. If the specified meetingId is for a meeting series, the invitees for the series will be
        listed; if the meetingId is for a scheduled meeting, the invitees for the particular scheduled meeting will
        be listed; if the meetingId is for an ended or ongoing meeting instance, the invitees for the particular
        meeting instance will be listed. See the Webex Meetings guide for more information about the types of
        meetings. The list returned is sorted in ascending order by email address. Long result sets are split into
        pages.

        :param meeting_id: Unique identifier for the meeting for which invitees are being requested. The meeting
            can be a meeting series, a scheduled meeting, or a meeting instance which has ended or is ongoing. The
            meeting ID of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or
            application calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of
            a user in a site they manage and the API will return meeting invitees that are hosted by that user.
        :type host_email: str
        :param panelist: Filter invitees or attendees for webinars only. If true,
            returns invitees. If false, returns attendees. If null, returns both invitees and attendees.
        :type panelist: bool
        """
        params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if panelist is not None:
            params['panelist'] = str(panelist).lower()
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=Invitee, params=params)]

    async def create_invitee(self, email: str, meeting_id: str, display_name: str = None, co_host: bool = None,
                       send_email: bool = None, panelist: bool = None, host_email: str = None) -> Invitee:
        """
        Invite a person to attend a meeting.
        Identify the invitee in the request body, by email address.

        :param email: Email address for meeting invitee.
        :type email: str
        :param meeting_id: Unique identifier for the meeting to which a person is being invited. This attribute only
            applies to meeting series and scheduled meeting. If it's a meeting series, the meeting invitee is invited
            to the entire meeting series; if it's a scheduled meeting, the meeting invitee is invited to this individual
            scheduled meeting. It doesn't apply to an ended or ongoing meeting instance. The meeting ID of a scheduled
            personal room meeting is not supported for this API.
        :type meeting_id: str

        :param display_name: Display name for meeting invitee. The maximum length of displayName is 128
            characters. In Webex App, if the email has been associated with an existing Webex account, the display
            name associated with the Webex account will be used; otherwise, the email will be used as displayName. In
            Webex site, if displayName is specified, it will show displayName. If displayName is not specified,
            and the email has been associated with an existing Webex account, the display name associated with the
            Webex account will be used; otherwise, the email will be used as displayName. Please note that if the
            invitee has an existing Webex account, the displayName shown in the meeting will be the displayName
            associated with the Webex account; otherwise, displayName shown in the meeting will be the displayName
            which is specified by the invitee who does not have a Webex account.

        :type display_name: str
        :param co_host: Whether or not invitee is a designated alternate host for the meeting. See Add Alternate
            Hosts for Cisco Webex Meetings for more details.
        :type co_host: bool
        :param send_email: If true, send an email to the invitee.
        :type send_email: bool
        :param panelist: If true, the invitee is a designated panelist for the event meeting.
        :type panelist: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email of
            a user in a site they manage to be the meeting host.
        :type host_email: str
        """
        body = CreateMeetingInviteeBody()
        if email is not None:
            body.email = email
        if meeting_id is not None:
            body.meeting_id = meeting_id
        if display_name is not None:
            body.display_name = display_name
        if co_host is not None:
            body.co_host = co_host
        if send_email is not None:
            body.send_email = send_email
        if panelist is not None:
            body.panelist = panelist
        if host_email is not None:
            body.host_email = host_email
        url = self.ep()
        data = await super().post(url=url, data=body.model_dump_json())
        return Invitee.model_validate(data)

    async def create_invitees(self, meeting_id: str, items: List[CreateInviteesItem],
                        host_email: str = None) -> List[Invitee]:
        """
        Invite people to attend a meeting in bulk.
        Identify each invitee by the email address of each item in the items of the request body.
        Each invitee should have a unique email.
        This API limits the maximum size of items in the request body to 100.

        :param meeting_id: Unique identifier for the meeting to which the people are being invited. This attribute
            only applies to meeting series and scheduled meetings. If it's a meeting series, the meeting invitees are
            invited to the entire meeting series; if it's a scheduled meeting, the meeting invitees are invited to this
            individual scheduled meeting. It doesn't apply to an ended or ongoing meeting instance. The meeting ID of a
            scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email of
            a user in a site they manage to be the meeting host.
        :type host_email: str
        :param items: Meeting invitees to be inserted.
        :type items: CreateInviteesItem
        """
        body = CreateMeetingInviteesBody()
        if meeting_id is not None:
            body.meeting_id = meeting_id
        if host_email is not None:
            body.host_email = host_email
        if items is not None:
            body.items = items
        url = self.ep('bulkInsert')
        data = await super().post(url=url, data=body.model_dump_json())
        return data["items"]

    async def invitee_details(self, meeting_invitee_id: str, host_email: str = None) -> Invitee:
        """
        Retrieve details for a meeting invitee identified by a meetingInviteeId in the URI.

        :param meeting_invitee_id: Unique identifier for the invitee whose details are being requested.
        :type meeting_invitee_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will return details for a meeting invitee that is hosted by that user.
        :type host_email: str
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_invitee_id}')
        data = await super().get(url=url, params=params)
        return Invitee.model_validate(data)

    async def update(self, meeting_invitee_id: str, email: str, display_name: str = None, co_host: bool = None,
               send_email: bool = None, panelist: bool = None, host_email: str = None) -> Invitee:
        """
        Update details for a meeting invitee identified by a meetingInviteeId in the URI.

        :param meeting_invitee_id: Unique identifier for the invitee to be updated. This parameter only applies to an
            invitee to a meeting series or a scheduled meeting. It doesn't apply to an invitee to an ended or ongoing
            meeting instance.
        :type meeting_invitee_id: str
        :param email: Email address for meeting invitee.
        :type email: str
        :param display_name: Display name for meeting invitee. The maximum length of displayName is 128 characters.
            In Webex App, if the email has been associated with an existing Webex account, the display name associated
            with the Webex account will be used; otherwise, the email will be used as displayName. In Webex site,
            if displayName is specified, it will show displayName. If displayName is not specified, and the email has
            been associated with an existing Webex account, the display name associated with the Webex account will be
            used; otherwise, the email will be used as displayName.
            Please note that if the invitee has an existing Webex account, the displayName shown in the meeting will
            be the displayName associated with the Webex account; otherwise, displayName shown in the meeting will be
            the displayName which is specified by the invitee who does not have a Webex account.
        :type display_name: str
        :param co_host: Whether or not invitee is a designated alternate host for the meeting. See Add Alternate
            Hosts for Cisco Webex Meetings for more details.
        :type co_host: bool
        :param send_email: If true, send an email to the invitee.
        :type send_email: bool
        :param panelist: If true, the invitee is a designated panelist for the event meeting.
        :type panelist: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin on-behalf-of scopes. When used, the admin may specify the email of
            a user in a site they manage to be the meeting host.
        :type host_email: str
        """
        body = UpdateMeetingInviteeBody()
        if email is not None:
            body.email = email
        if display_name is not None:
            body.display_name = display_name
        if co_host is not None:
            body.co_host = co_host
        if send_email is not None:
            body.send_email = send_email
        if panelist is not None:
            body.panelist = panelist
        if host_email is not None:
            body.host_email = host_email
        url = self.ep(f'{meeting_invitee_id}')
        data = await super().put(url=url, data=body.model_dump_json())
        return Invitee.model_validate(data)

    async def delete(self, meeting_invitee_id: str, host_email: str = None, send_email: bool = None):
        """
        Removes a meeting invitee identified by a meetingInviteeId specified in the URI. The deleted meeting invitee
        cannot be recovered.
        If the meeting invitee is associated with a meeting series, the invitee will be removed from the entire
        meeting series. If the invitee is associated with a scheduled meeting, the invitee will be removed from only
        that scheduled meeting.

        :param meeting_invitee_id: Unique identifier for the invitee to be removed. This parameter only applies to an
            invitee to a meeting series or a scheduled meeting. It doesn't apply to an invitee to an ended or ongoing
            meeting instance.
        :type meeting_invitee_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin on-behalf-of scopes. If set, the admin may specify the email of a user in a
            site they manage and the API will delete a meeting invitee that is hosted by that user.
        :type host_email: str
        :param send_email: If true, send an email to the invitee.
        :type send_email: bool
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if send_email is not None:
            params['sendEmail'] = str(send_email).lower()
        url = self.ep(f'{meeting_invitee_id}')
        await super().delete(url=url, params=params)
        return


class AsMeetingParticipantsApi(AsApiChild, base='meetingParticipants'):
    """
    This API manages meeting participants.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    """

    def list_participants_gen(self, meeting_id: str, host_email: str = None, join_time_from: str = None,
                          join_time_to: str = None, **params) -> AsyncGenerator[Participant, None, None]:
        """
        List all participants in a live or post meeting. The meetingId parameter is required, which is the unique
        identifier for the meeting.
        The authenticated user calling this API must either have an Administrator role with the
        meeting:admin_participants_read scope, or be the meeting host.

        :param meeting_id: The unique identifier for the meeting. Please note that currently meeting ID of a scheduled
            personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :param join_time_from: The time participants join a meeting starts from the specified date and time (inclusive)
            in any ISO 8601 compliant format. If joinTimeFrom is not specified, it equals joinTimeTo minus 7 days.
        :type join_time_from: str
        :param join_time_to: The time participants join a meeting before the specified date and time (exclusive) in any
            ISO 8601 compliant format. If joinTimeTo is not specified, it equals joinTimeFrom plus 7 days. The interval
            between joinTimeFrom and joinTimeTo must be within 90 days.
        :type join_time_to: str
        """
        params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if join_time_from is not None:
            params['joinTimeFrom'] = join_time_from
        if join_time_to is not None:
            params['joinTimeTo'] = join_time_to
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Participant, params=params)

    async def list_participants(self, meeting_id: str, host_email: str = None, join_time_from: str = None,
                          join_time_to: str = None, **params) -> List[Participant]:
        """
        List all participants in a live or post meeting. The meetingId parameter is required, which is the unique
        identifier for the meeting.
        The authenticated user calling this API must either have an Administrator role with the
        meeting:admin_participants_read scope, or be the meeting host.

        :param meeting_id: The unique identifier for the meeting. Please note that currently meeting ID of a scheduled
            personal room meeting is not supported for this API.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :param join_time_from: The time participants join a meeting starts from the specified date and time (inclusive)
            in any ISO 8601 compliant format. If joinTimeFrom is not specified, it equals joinTimeTo minus 7 days.
        :type join_time_from: str
        :param join_time_to: The time participants join a meeting before the specified date and time (exclusive) in any
            ISO 8601 compliant format. If joinTimeTo is not specified, it equals joinTimeFrom plus 7 days. The interval
            between joinTimeFrom and joinTimeTo must be within 90 days.
        :type join_time_to: str
        """
        params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if join_time_from is not None:
            params['joinTimeFrom'] = join_time_from
        if join_time_to is not None:
            params['joinTimeTo'] = join_time_to
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=Participant, params=params)]

    async def query_participants_with_email(self, meeting_id: str, max: int = None, host_email: str = None,
                                      join_time_from: str = None, join_time_to: str = None,
                                      emails: list[str] = None) -> list[Participant]:
        """
        Query participants in a live meeting, or after the meeting, using participant's email. The meetingId parameter
        is the unique identifier for the meeting and is required.
        The authenticated user calling this API must either have an Administrator role with the
        meeting:admin_participants_read scope, or be the meeting host.

        :param meeting_id: The unique identifier for the meeting.
        :type meeting_id: str
        :param max: Limit the maximum number of participants in the response, up to 1000.
        :type max: int
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        :param join_time_from: The time participants join a meeting starts from the specified date and time (inclusive)
            in any ISO 8601 compliant format. If joinTimeFrom is not specified, it equals joinTimeTo minus 7 days.
        :type join_time_from: str
        :param join_time_to: The time participants join a meeting before the specified date and time (exclusive) in any
            ISO 8601 compliant format. If joinTimeTo is not specified, it equals joinTimeFrom plus 7 days. The interval
            between joinTimeFrom and joinTimeTo must be within 90 days.
        :type join_time_to: str
        :param emails: Participants email list Possible values: a@example.com
        :type emails: List[str]
        """
        params = {}
        params['meetingId'] = meeting_id
        if max is not None:
            params['max'] = max
        if host_email is not None:
            params['hostEmail'] = host_email
        if join_time_from is not None:
            params['joinTimeFrom'] = join_time_from
        if join_time_to is not None:
            params['joinTimeTo'] = join_time_to
        body = QueryMeetingParticipantsWithEmailBody()
        if emails is not None:
            body.emails = emails
        url = self.ep('query')
        data = await super().post(url=url, params=params, data=body.model_dump_json())
        # TODO: this is wrong -> fix code generation
        return data["items"]

    async def participant_details(self, participant_id: str, host_email: str = None) -> Participant:
        """
        Get a meeting participant details of a live or post meeting. The participantId is required to identify the
        meeting and the participant.
        The authenticated user calling this API must either have an Administrator role with the
        meeting:admin_participants_read scope, or be the meeting host.

        :param participant_id: The unique identifier for the meeting and the participant.
        :type participant_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes, the admin may specify the email of a user in a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{participant_id}')
        data = await super().get(url=url, params=params)
        return Participant.model_validate(data)

    async def update_participant(self, participant_id: str, muted: bool = None, admit: bool = None,
                           expel: bool = None) -> UpdateParticipantResponse:
        """
        To mute, un-mute, expel, or admit a participant in a live meeting. The participantId is required to identify
        the meeting and the participant.
        Notes:

        :param participant_id: The unique identifier for the meeting and the participant.
        :type participant_id: str
        :param muted: The value is true or false, and means to mute or unmute the audio of a participant.
        :type muted: bool
        :param admit: The value can be true or false. The value of true is to admit a participant to the meeting if the
            participant is in the lobby, No-Op if the participant is not in the lobby or when the value is set to
            false.
        :type admit: bool
        :param expel: The attribute is exclusive and its value can be true or false. The value of true means that the
            participant will be expelled from the meeting, the value of false means No-Op.
        :type expel: bool
        """
        body = UpdateParticipantBody()
        if muted is not None:
            body.muted = muted
        if admit is not None:
            body.admit = admit
        if expel is not None:
            body.expel = expel
        url = self.ep(f'{participant_id}')
        data = await super().put(url=url, data=body.model_dump_json())
        return UpdateParticipantResponse.model_validate(data)

    async def admit_participants(self, participant_ids: List[str] = None):
        """
        To admit participants into a live meeting in bulk.
        This API limits the maximum size of items in the request body to 100.
        Each participantId of items in the request body should have the same prefix of meetingId.

        :param participant_ids: The ID that identifies the meeting participant.
        :type participant_ids: List[str]
        """
        body = AdmitParticipantsBody()
        if participant_ids is not None:
            body.items = participant_ids
        url = self.ep('admit')
        await super().post(url=url, data=body.model_dump_json())
        return


class AsMeetingPreferencesApi(AsApiChild, base='meetingPreferences'):
    """
    This API manages a user's meeting preferences, including Personal Meeting Room settings, video and audio settings,
    meeting scheduling options, and site settings.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    """

    async def details(self, user_email: str = None, site_url: str = None) -> MeetingPreferenceDetails:
        """
        Retrieves meeting preferences for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the required admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details of the meeting preferences for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep()
        data = await super().get(url=url, params=params)
        return MeetingPreferenceDetails.model_validate(data)

    async def personal_meeting_room_options(self, user_email: str = None, site_url: str = None) -> PersonalMeetingRoomOptions:
        """
        Retrieves the Personal Meeting Room options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will return details of the Personal Meeting Room options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('personalMeetingRoom')
        data = await super().get(url=url, params=params)
        return PersonalMeetingRoomOptions.model_validate(data)

    async def update_personal_meeting_room_options(self, topic: str, host_pin: str, enabled_auto_lock: bool,
                                             auto_lock_minutes: int, enabled_notify_host: bool, support_co_host: bool,
                                             co_hosts: CoHost, user_email: str = None, site_url: str = None,
                                             support_anyone_as_co_host: bool = None,
                                             allow_first_user_to_be_co_host: bool = None,
                                             allow_authenticated_devices: bool = None) -> PersonalMeetingRoomOptions:
        """
        Update a single meeting

        :param topic: Personal Meeting Room topic to be updated.
        :type topic: str
        :param host_pin: Updated PIN for joining the room as host. The host PIN must be digits of a predefined length,
            e.g. 4 digits. It cannot contain sequential digits, such as 1234 or 4321, or repeated digits of the
            predefined length, such as 1111. The predefined length for host PIN can be viewed in user's My Personal
            Room page and it can only be changed by site administrator.
        :type host_pin: str
        :param enabled_auto_lock: Update for option to automatically lock the Personal Room a number of minutes after a
            meeting starts. When a room is locked, invitees cannot enter until the owner admits them. The period after
            which the meeting is locked is defined by autoLockMinutes.
        :type enabled_auto_lock: bool
        :param auto_lock_minutes: Updated number of minutes after which the Personal Room is locked if enabledAutoLock
            is enabled. Valid options are 0, 5, 10, 15 and 20.
        :type auto_lock_minutes: int
        :param enabled_notify_host: Update for flag to enable notifying the owner of a Personal Room when someone
            enters the Personal Room lobby while the owner is not in the room.
        :type enabled_notify_host: bool
        :param support_co_host: Update for flag allowing other invitees to host a meetingCoHost in the Personal Room
            without the owner.
        :type support_co_host: bool
        :param co_hosts: Updated array defining cohosts for the room if both supportAnyoneAsCoHost and
            allowFirstUserToBeCoHost are false
        :type co_hosts: CoHost
        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update Personal Meeting Room options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        :param support_anyone_as_co_host: Whether or not to allow any attendee with a host account on the target site
            to become a cohost when joining the Personal Room. The target site is user's preferred site.
        :type support_anyone_as_co_host: bool
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee with a host account on the
            target site to become a cohost when joining the Personal Room. The target site is user's preferred site.
        :type allow_first_user_to_be_co_host: bool
        :param allow_authenticated_devices: Whether or not to allow authenticated video devices in the user's
            organization to start or join the meeting without a prompt.
        :type allow_authenticated_devices: bool
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        body = UpdatePersonalMeetingRoomOptionsBody()
        if topic is not None:
            body.topic = topic
        if host_pin is not None:
            body.host_pin = host_pin
        if enabled_auto_lock is not None:
            body.enabled_auto_lock = enabled_auto_lock
        if auto_lock_minutes is not None:
            body.auto_lock_minutes = auto_lock_minutes
        if enabled_notify_host is not None:
            body.enabled_notify_host = enabled_notify_host
        if support_co_host is not None:
            body.support_co_host = support_co_host
        if co_hosts is not None:
            body.co_hosts = co_hosts
        if support_anyone_as_co_host is not None:
            body.support_anyone_as_co_host = support_anyone_as_co_host
        if allow_first_user_to_be_co_host is not None:
            body.allow_first_user_to_be_co_host = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body.allow_authenticated_devices = allow_authenticated_devices
        url = self.ep('personalMeetingRoom')
        data = await super().put(url=url, params=params, data=body.model_dump_json())
        return PersonalMeetingRoomOptions.model_validate(data)

    async def audio_options(self, user_email: str = None, site_url: str = None) -> Audio:
        """
        Retrieves audio options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will return details of the audio options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('audio')
        data = await super().get(url=url, params=params)
        return Audio.model_validate(data)

    async def update_audio_options(self, user_email: str = None, site_url: str = None,
                             default_audio_type: DefaultAudioType = None, other_teleconference_description: str = None,
                             enabled_global_call_in: bool = None, enabled_toll_free: bool = None,
                             enabled_auto_connection: bool = None, audio_pin: str = None,
                             office_number: OfficeNumber = None, mobile_number: OfficeNumber = None) -> Audio:
        """
        Updates audio options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update audio options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved
            from /meetingPreferences/sites.
        :type site_url: str
        :param default_audio_type: Default audio type. This attribute can be modified with the with the Update Audio
            Options API.
        :type default_audio_type: DefaultAudioType
        :param other_teleconference_description: Phone number and other information for the teleconference provider to
            be used, along with instructions for invitees. This attribute can be modified with the with the Update
            Audio Options API.
        :type other_teleconference_description: str
        :param enabled_global_call_in: Flag to enable/disable global call ins. Note: If the site does not support
            global call-ins, you cannot set this option. This attribute can be modified with the with the Update Audio
            Options API.
        :type enabled_global_call_in: bool
        :param enabled_toll_free: Flag to enable/disable call-ins from toll-free numbers. Note: If the site does not
            support calls from toll-free numbers, you cannot set this option. This attribute can be modified with the
            with the Update Audio Options API.
        :type enabled_toll_free: bool
        :param enabled_auto_connection: Flag to enable/disable automatically connecting to audio using a computer. The
            meeting host can enable/disable this option. When this option is set to true, the user is automatically
            connected to audio via a computer when they start or join a Webex Meetings meeting on a desktop. This
            attribute can be modified with the Update Audio Options API.
        :type enabled_auto_connection: bool
        :param audio_pin: PIN to provide a secondary level of authentication for calls where the host is using the
            phone and may need to invite additional invitees. It must be exactly 4 digits. It cannot contain sequential
            digits, such as 1234 or 4321, or repeat a digit 4 times, such as 1111. This attribute can be modified with
            the with the Update Audio Options API.
        :type audio_pin: str
        :param office_number: Office phone number. We recommend that phone numbers be specified to facilitate
            connecting via audio. This attribute can be modified with the with the Update Audio Options API.
        :type office_number: OfficeNumber
        :param mobile_number: Mobile phone number. We recommend that phone numbers be specified to facilitate
            connecting via audio. This attribute can be modified with the with the Update Audio Options API.
        :type mobile_number: OfficeNumber
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        body = Audio()
        if default_audio_type is not None:
            body.default_audio_type = default_audio_type
        if other_teleconference_description is not None:
            body.other_teleconference_description = other_teleconference_description
        if enabled_global_call_in is not None:
            body.enabled_global_call_in = enabled_global_call_in
        if enabled_toll_free is not None:
            body.enabled_toll_free = enabled_toll_free
        if enabled_auto_connection is not None:
            body.enabled_auto_connection = enabled_auto_connection
        if audio_pin is not None:
            body.audio_pin = audio_pin
        if office_number is not None:
            body.office_number = office_number
        if mobile_number is not None:
            body.mobile_number = mobile_number
        url = self.ep('audio')
        data = await super().put(url=url, params=params, data=body.model_dump_json())
        return Audio.model_validate(data)

    async def video_options(self, user_email: str = None, site_url: str = None) -> list[VideoDevice]:
        """
        Retrieves video options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will return details of the video options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved using Get Site List.
        :type site_url: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('video')
        data = await super().get(url=url, params=params)
        return TypeAdapter(list[VideoDevice]).validate_python(data["videoDevices"])

    async def update_video_options(self, video_devices: VideoDevice, user_email: str = None,
                             site_url: str = None) -> list[VideoDevice]:
        """
        Updates video options for the authenticated user.

        :param video_devices: Array of video devices. If the array is not empty, one device and no more than one
            devices must be set as default device.
        :type video_devices: VideoDevice
        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update video options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        body = VideoOptions()
        if video_devices is not None:
            body.video_devices = video_devices
        url = self.ep('video')
        data = await super().put(url=url, params=params, data=body.model_dump_json())
        return TypeAdapter(list[VideoDevice]).validate_python(data["videoDevices"])

    async def scheduling_options(self, user_email: str = None, site_url: str = None) -> SchedulingOptions:
        """
        Retrieves scheduling options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will return details of the scheduling options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('schedulingOptions')
        data = await super().get(url=url, params=params)
        return SchedulingOptions.model_validate(data)

    async def update_scheduling_options(self, user_email: str = None, site_url: str = None,
                                  enabled_join_before_host: bool = None, join_before_host_minutes: int = None,
                                  enabled_auto_share_recording: bool = None,
                                  enabled_webex_assistant_by_default: bool = None) -> SchedulingOptions:
        """
        Updates scheduling options for the authenticated user.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update scheduling options for that user.
        :type user_email: str
        :param site_url: URL of the Webex site to query. For individual use, if siteUrl is not specified, the query
            will use the default site of the user. For admin use, if siteUrl is not specified, the query will use the
            default site for the admin's authorization token used to make the call. In the case where the user belongs
            to a site different than the admin’s default site, the admin can set the site to query using the siteUrl
            parameter. All available Webex sites and default site of a user can be retrieved from
            /meetingPreferences/sites.
        :type site_url: str
        :param enabled_join_before_host: Flag to enable/disable Join Before Host. The period during which invitees can
            join before the start time is defined by autoLockMinutes. This attribute can be modified with the Update
            Scheduling Options API. Note: This feature is only effective if the site supports the Join Before Host
            feature. This attribute can be modified with the Update Scheduling Options API.
        :type enabled_join_before_host: bool
        :param join_before_host_minutes: Number of minutes before the start time that an invitee can join a meeting if
            enabledJoinBeforeHost is true. Valid options are 0, 5, 10 and 15. This attribute can be modified with the
            Update Scheduling Options API.
        :type join_before_host_minutes: int
        :param enabled_auto_share_recording: Flag to enable/disable the automatic sharing of the meeting recording with
            invitees when it is available. This attribute can be modified with the Update Scheduling Options API.
        :type enabled_auto_share_recording: bool
        :param enabled_webex_assistant_by_default: Flag to automatically enable Webex Assistant whenever you start a
            meeting. This attribute can be modified with the Update Scheduling Options API.
        :type enabled_webex_assistant_by_default: bool
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        if site_url is not None:
            params['siteUrl'] = site_url
        body = SchedulingOptions()
        if enabled_join_before_host is not None:
            body.enabled_join_before_host = enabled_join_before_host
        if join_before_host_minutes is not None:
            body.join_before_host_minutes = join_before_host_minutes
        if enabled_auto_share_recording is not None:
            body.enabled_auto_share_recording = enabled_auto_share_recording
        if enabled_webex_assistant_by_default is not None:
            body.enabled_webex_assistant_by_default = enabled_webex_assistant_by_default
        url = self.ep('schedulingOptions')
        data = await super().put(url=url, params=params, data=body.model_dump_json())
        return SchedulingOptions.model_validate(data)

    async def site_list(self, user_email: str = None) -> list[MeetingsSite]:
        """
        Retrieves the list of Webex sites that the authenticated user is set up to use.

        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user and the API will
            return the list of Webex sites for that user.
        :type user_email: str
        """
        params = {}
        if user_email is not None:
            params['userEmail'] = user_email
        url = self.ep('sites')
        data = await super().get(url=url, params=params)
        return TypeAdapter(list[MeetingsSite]).validate_python(data["sites"])

    async def update_default_site(self, default_site: bool, site_url: str, user_email: str = None) -> MeetingsSite:
        """
        Updates the default site for the authenticated user.

        :param default_site: Whether or not to change user's default site. Note: defaultSite should be set to true for
            the user's single default site
        :type default_site: bool
        :param site_url: Access URL for the site.
        :type site_url: str
        :param user_email: Email address for the user. This parameter is only used if the user or application calling
            the API has the admin-level scopes. If set, the admin may specify the email of a user in a site they manage
            and the API will update default site for that user.
        :type user_email: str
        """
        params = {}
        params['defaultSite'] = str(default_site).lower()
        if user_email is not None:
            params['userEmail'] = user_email
        body = UpdateDefaultSiteBody()
        if site_url is not None:
            body.site_url = site_url
        url = self.ep('sites')
        data = await super().put(url=url, params=params, data=body.model_dump_json())
        return MeetingsSite.model_validate(data)


class AsMeetingQandAApi(AsApiChild, base='meetings/q_and_a'):
    """
    During a Question and Answer (Q&A) session, attendees can pose questions to hosts, co-hosts, and presenters, who
    can answer and moderate those questions. You use the Meeting Q&A API to retrieve the questions and the answers in a
    meeting.
    Currently, these APIs are available to users with one of the meeting host, admin or Compliance Officer roles.
    The features and APIs described here are available upon-request and is not enabled by default. If would like this
    feature enabled for your organization please contact the Webex Developer Support team at devsupport@webex.com.
    """

    def list_gen(self, meeting_id: str, **params) -> AsyncGenerator[QAObject, None, None]:
        """
        Lists questions and answers from a meeting, when ready.
        Notes:

        :param meeting_id: A unique identifier for the meeting instance which the Q&A belongs to.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-q-and-a/list-meeting-q-and-a
        """
        params['meetingId'] = meeting_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=QAObject, params=params)

    async def list(self, meeting_id: str, **params) -> List[QAObject]:
        """
        Lists questions and answers from a meeting, when ready.
        Notes:

        :param meeting_id: A unique identifier for the meeting instance which the Q&A belongs to.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-q-and-a/list-meeting-q-and-a
        """
        params['meetingId'] = meeting_id
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=QAObject, params=params)]

    def list_answers_gen(self, question_id: str, meeting_id: str,
                     **params) -> AsyncGenerator[AnswerObject, None, None]:
        """
        Lists the answers to a specific question asked in a meeting.

        :param question_id: The ID of a question.
        :type question_id: str
        :param meeting_id: A unique identifier for the meeting instance which the Q&A belongs to.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-q-and-a/list-answers-of-a-question
        """
        params['meetingId'] = meeting_id
        url = self.ep(f'{question_id}/answers')
        return self.session.follow_pagination(url=url, model=AnswerObject, params=params)

    async def list_answers(self, question_id: str, meeting_id: str,
                     **params) -> List[AnswerObject]:
        """
        Lists the answers to a specific question asked in a meeting.

        :param question_id: The ID of a question.
        :type question_id: str
        :param meeting_id: A unique identifier for the meeting instance which the Q&A belongs to.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-q-and-a/list-answers-of-a-question
        """
        params['meetingId'] = meeting_id
        url = self.ep(f'{question_id}/answers')
        return [o async for o in self.session.follow_pagination(url=url, model=AnswerObject, params=params)]


class AsMeetingQualitiesApi(AsApiChild, base=''):
    """
    To retrieve quality information, you must use an administrator token with the analytics:read_all scope. The
    authenticated user must be a read-only or full administrator of the organization to which the meeting belongs and
    must not be an external administrator.
    To use this endpoint, the org needs to be licensed for the Webex Pro Pack.
    For CI-Native site, no additional settings are required.
    For CI-linked site, the admin must also be set as the Full/ReadOnly Site Admin of the site.
    A minimum Webex and Teams client version is required. For details, see Troubleshooting Help Doc.
    Quality information is available 10 minutes after a meeting has started and may be retrieved for up to 7 days.
    A rate limit of 1 API call every 5 minutes for the same meeting instance ID applies.
    """

    def meeting_qualities_gen(self, meeting_id: str, offset: int = None,
                          **params) -> AsyncGenerator[MediaSessionQuality, None, None]:
        """
        Get quality data for a meeting, by meetingId. Only organization administrators can retrieve meeting quality
        data.

        :param meeting_id: Unique identifier for the specific meeting instance. Note: The meetingId can be obtained via
            the Meeting List API when meetingType=meeting. The id attribute in the Meeting List Response is what is
            needed, for example, e5dba9613a9d455aa49f6ffdafb6e7db_I_191395283063545470.
        :type meeting_id: str
        :param offset: Offset from the first result that you want to fetch.
        :type offset: int

        documentation: https://developer.webex.com/docs/api/v1/meeting-qualities/get-meeting-qualities
        """
        params['meetingId'] = meeting_id
        if offset is not None:
            params['offset'] = offset
        url = self.ep('https://analytics.webexapis.com/v1/meeting/qualities')
        return self.session.follow_pagination(url=url, model=MediaSessionQuality, params=params)

    async def meeting_qualities(self, meeting_id: str, offset: int = None,
                          **params) -> List[MediaSessionQuality]:
        """
        Get quality data for a meeting, by meetingId. Only organization administrators can retrieve meeting quality
        data.

        :param meeting_id: Unique identifier for the specific meeting instance. Note: The meetingId can be obtained via
            the Meeting List API when meetingType=meeting. The id attribute in the Meeting List Response is what is
            needed, for example, e5dba9613a9d455aa49f6ffdafb6e7db_I_191395283063545470.
        :type meeting_id: str
        :param offset: Offset from the first result that you want to fetch.
        :type offset: int

        documentation: https://developer.webex.com/docs/api/v1/meeting-qualities/get-meeting-qualities
        """
        params['meetingId'] = meeting_id
        if offset is not None:
            params['offset'] = offset
        url = self.ep('https://analytics.webexapis.com/v1/meeting/qualities')
        return [o async for o in self.session.follow_pagination(url=url, model=MediaSessionQuality, params=params)]


class AsMeetingTranscriptsApi(AsApiChild, base=''):
    """
    Not supported for Webex for Government (FedRAMP)
    A meeting transcript is the automatic transcription of a meeting's recordings by our industry-leading
    speech-to-text engine to capture of what was discussed and decided during the meeting, in text form.
    A transcript snippet is a short text snippet from a meeting transcript which was spoken by a particular participant
    in the meeting. A meeting transcript consists of many snippets.
    This API manages meeting transcripts and snippets. You can use the Transcript API to list meeting transcripts,
    list, get and update transcript snippets. Transcripts may be retrieved via download link defined by vttDownloadLink
    or txtDownloadlink in the response body.
    Refer to the Meetings API Scopes section of Meetings Overview for scopes required for each API.
    NOTE:
    """

    def list_gen(self, meeting_id: str = None, host_email: str = None, site_url: str = None, from_: str = None,
             to_: str = None, **params) -> AsyncGenerator[Transcript, None, None]:
        """
        Lists available transcripts of an ended meeting instance.
        Use this operation to list transcripts of an ended meeting instance when they are ready. Please note that only
        meeting instances in state ended are supported for meetingId. Meeting series, scheduled meetings and
        in-progress meeting instances are not supported.

        :param meeting_id: Unique identifier for the meeting instance to which the transcript belongs. Please note that
            currently the meeting ID of a scheduled personal room meeting is not supported for this API. If meetingId
            is not specified, the operation returns an array of transcripts for all meetings of the current user.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user. If meetingId is not
            specified, it can not support hostEmail.
        :type host_email: str
        :param site_url: URL of the Webex site from which the API lists transcripts. If not specified, the API lists
            transcripts from user's preferred site. All available Webex sites and the preferred site of the user can be
            retrieved by the Get Site List API.
        :type site_url: str
        :param from_: Starting date and time (inclusive) for transcripts to return, in any ISO 8601 compliant format.
            from cannot be after to.
        :type from_: str
        :param to_: Ending date and time (exclusive) for List transcripts to return, in any ISO 8601 compliant format.
            to cannot be before from.
        :type to_: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/list-meeting-transcripts
        """
        if meeting_id is not None:
            params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        url = self.ep('meetingTranscripts')
        return self.session.follow_pagination(url=url, model=Transcript, params=params)

    async def list(self, meeting_id: str = None, host_email: str = None, site_url: str = None, from_: str = None,
             to_: str = None, **params) -> List[Transcript]:
        """
        Lists available transcripts of an ended meeting instance.
        Use this operation to list transcripts of an ended meeting instance when they are ready. Please note that only
        meeting instances in state ended are supported for meetingId. Meeting series, scheduled meetings and
        in-progress meeting instances are not supported.

        :param meeting_id: Unique identifier for the meeting instance to which the transcript belongs. Please note that
            currently the meeting ID of a scheduled personal room meeting is not supported for this API. If meetingId
            is not specified, the operation returns an array of transcripts for all meetings of the current user.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user. If meetingId is not
            specified, it can not support hostEmail.
        :type host_email: str
        :param site_url: URL of the Webex site from which the API lists transcripts. If not specified, the API lists
            transcripts from user's preferred site. All available Webex sites and the preferred site of the user can be
            retrieved by the Get Site List API.
        :type site_url: str
        :param from_: Starting date and time (inclusive) for transcripts to return, in any ISO 8601 compliant format.
            from cannot be after to.
        :type from_: str
        :param to_: Ending date and time (exclusive) for List transcripts to return, in any ISO 8601 compliant format.
            to cannot be before from.
        :type to_: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/list-meeting-transcripts
        """
        if meeting_id is not None:
            params['meetingId'] = meeting_id
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        url = self.ep('meetingTranscripts')
        return [o async for o in self.session.follow_pagination(url=url, model=Transcript, params=params)]

    def list_compliance_officer_gen(self, site_url: str, from_: str = None, to_: str = None,
                                **params) -> AsyncGenerator[Transcript, None, None]:
        """
        Lists available or deleted transcripts of an ended meeting instance for a specific site.
        The returned list is sorted in descending order by the date and time that the transcript was created.

        :param site_url: URL of the Webex site from which the API lists transcripts.
        :type site_url: str
        :param from_: Starting date and time (inclusive) for transcripts to return, in any ISO 8601 compliant format.
            from cannot be after to.
        :type from_: str
        :param to_: Ending date and time (exclusive) for List transcripts to return, in any ISO 8601 compliant format.
            to cannot be before from.
        :type to_: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/list-meeting-transcripts-for
        -compliance-officer
        """
        params['siteUrl'] = site_url
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        url = self.ep('admin/meetingTranscripts')
        return self.session.follow_pagination(url=url, model=Transcript, params=params)

    async def list_compliance_officer(self, site_url: str, from_: str = None, to_: str = None,
                                **params) -> List[Transcript]:
        """
        Lists available or deleted transcripts of an ended meeting instance for a specific site.
        The returned list is sorted in descending order by the date and time that the transcript was created.

        :param site_url: URL of the Webex site from which the API lists transcripts.
        :type site_url: str
        :param from_: Starting date and time (inclusive) for transcripts to return, in any ISO 8601 compliant format.
            from cannot be after to.
        :type from_: str
        :param to_: Ending date and time (exclusive) for List transcripts to return, in any ISO 8601 compliant format.
            to cannot be before from.
        :type to_: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/list-meeting-transcripts-for
        -compliance-officer
        """
        params['siteUrl'] = site_url
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        url = self.ep('admin/meetingTranscripts')
        return [o async for o in self.session.follow_pagination(url=url, model=Transcript, params=params)]

    async def download(self, transcript_id: str, format: str = None, host_email: str = None):
        """
        Download a meeting transcript from the meeting transcript specified by transcriptId.

        :param transcript_id: Unique identifier for the meeting transcript.
        :type transcript_id: str
        :param format: Format for the downloaded meeting transcript. Possible values: vtt, txt
        :type format: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/download-a-meeting-transcript
        """
        params = {}
        if format is not None:
            params['format'] = format
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'meetingTranscripts/{transcript_id}/download')
        await super().get(url=url, params=params)
        # TODO: fix. Find out what the actual return type is

    def list_snippets_gen(self, transcript_id: str, **params) -> AsyncGenerator[TranscriptSnippet, None, None]:
        """
        Lists snippets of a meeting transcript specified by transcriptId.
        Use this operation to list snippets of a meeting transcript when they are ready.

        :param transcript_id: Unique identifier for the meeting transcript to which the snippets belong.
        :type transcript_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/list-snippets-of-a-meeting-transcript
        """
        url = self.ep(f'meetingTranscripts/{transcript_id}/snippets')
        return self.session.follow_pagination(url=url, model=TranscriptSnippet, params=params)

    async def list_snippets(self, transcript_id: str, **params) -> List[TranscriptSnippet]:
        """
        Lists snippets of a meeting transcript specified by transcriptId.
        Use this operation to list snippets of a meeting transcript when they are ready.

        :param transcript_id: Unique identifier for the meeting transcript to which the snippets belong.
        :type transcript_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/list-snippets-of-a-meeting-transcript
        """
        url = self.ep(f'meetingTranscripts/{transcript_id}/snippets')
        return [o async for o in self.session.follow_pagination(url=url, model=TranscriptSnippet, params=params)]

    async def snippet_detail(self, transcript_id: str, snippet_id: str) -> TranscriptSnippet:
        """
        Retrieves details for a transcript snippet specified by snippetId from the meeting transcript specified by
        transcriptId.

        :param transcript_id: Unique identifier for the meeting transcript to which the requested snippet belongs.
        :type transcript_id: str
        :param snippet_id: Unique identifier for the snippet being requested.
        :type snippet_id: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/get-a-transcript-snippet
        """
        url = self.ep(f'meetingTranscripts/{transcript_id}/snippets/{snippet_id}')
        data = await super().get(url=url)
        return TranscriptSnippet.model_validate(data)

    async def update_snippet(self, transcript_id: str, snippet_id: str, text: str, reason: str = None) -> TranscriptSnippet:
        """
        Updates details for a transcript snippet specified by snippetId from the meeting transcript specified by
        transcriptId.

        :param transcript_id: Unique identifier for the meeting transcript to which the snippet to be updated belongs.
        :type transcript_id: str
        :param snippet_id: Unique identifier for the snippet being updated.
        :type snippet_id: str
        :param text: Text for the snippet.
        :type text: str
        :param reason: Reason for snippet update; only required for Compliance Officers.
        :type reason: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/update-a-transcript-snippet
        """
        body = UpdateTranscriptSnippetBody()
        if text is not None:
            body.text = text
        if reason is not None:
            body.reason = reason
        url = self.ep(f'meetingTranscripts/{transcript_id}/snippets/{snippet_id}')
        data = await super().put(url=url, data=body.model_dump_json())
        return TranscriptSnippet.model_validate(data)

    async def delete(self, transcript_id: str, reason: str = None, comment: str = None):
        """
        Removes a transcript with a specified transcript ID. The deleted transcript cannot be recovered. If a
        Compliance Officer deletes another user's transcript, the transcript will be inaccessible to regular users
        (host, attendees), but will be still available to the Compliance Officer.

        :param transcript_id: Unique identifier for the meeting transcript.
        :type transcript_id: str
        :param reason: Reason for deleting a transcript. Only required when a Compliance Officer is operating on
            another user's transcript.
        :type reason: str
        :param comment: Explanation for deleting a transcript. The comment can be a maximum of 255 characters long.
        :type comment: str

        documentation: https://developer.webex.com/docs/api/v1/meeting-transcripts/delete-a-transcript
        """
        body = DeleteTranscriptBody()
        if reason is not None:
            body.reason = reason
        if comment is not None:
            body.comment = comment
        url = self.ep(f'meetingTranscripts/{transcript_id}')
        await super().delete(url=url, data=body.model_dump_json())
        return


class AsMeetingsApi(AsApiChild, base='meetings'):
    """
    Meetings API
    """
    #: meeting chats API
    chats: AsMeetingChatsApi
    #: closed captions API
    closed_captions: AsMeetingClosedCaptionsApi
    #: meeting invitees API
    invitees: AsMeetingInviteesApi
    #: meeting participants API
    participants: AsMeetingParticipantsApi
    #: preferences API
    preferences: AsMeetingPreferencesApi
    #: Q and A API
    qanda: AsMeetingQandAApi
    #: qualities API
    qualities: AsMeetingQualitiesApi
    #: transcripts
    transcripts: AsMeetingTranscriptsApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.chats = AsMeetingChatsApi(session=session)
        self.closed_captions = AsMeetingClosedCaptionsApi(session=session)
        self.invitees = AsMeetingInviteesApi(session=session)
        self.participants = AsMeetingParticipantsApi(session=session)
        self.preferences = AsMeetingPreferencesApi(session=session)
        self.qanda = AsMeetingQandAApi(session=session)
        self.qualities = AsMeetingQualitiesApi(session=session)
        self.transcripts = AsMeetingTranscriptsApi(session=session)

    async def create(self, title: str = None, agenda: str = None, password: str = None, start: str = None, end: str = None,
               timezone: str = None, recurrence: str = None, enabled_auto_record_meeting: bool = None,
               allow_any_user_to_be_co_host: bool = None, enabled_join_before_host: bool = None,
               enable_connect_audio_before_host: bool = None, join_before_host_minutes: int = None,
               exclude_password: bool = None, public_meeting: bool = None, reminder_time: int = None,
               unlocked_meeting_join_security: UnlockedMeetingJoinSecurity = None, session_type_id: int = None,
               enabled_webcast_view: bool = None, panelist_password: str = None, enable_automatic_lock: bool = None,
               automatic_lock_minutes: int = None, allow_first_user_to_be_co_host: bool = None,
               allow_authenticated_devices: bool = None, send_email: bool = None, host_email: str = None,
               site_url: str = None, meeting_options: MeetingOptions = None,
               attendee_privileges: AttendeePrivileges = None, integration_tags: List[str] = None,
               enabled_breakout_sessions: bool = None, tracking_codes: TrackingCodeItem = None,
               audio_connection_options: AudioConnectionOptions = None, adhoc: bool = None, room_id: str = None,
               template_id: str = None, scheduled_type: ScheduledType = None,
               invitees: InviteeForCreateMeeting = None, registration: Registration = None,
               simultaneous_interpretation: SimultaneousInterpretation = None,
               breakout_sessions: BreakoutSession = None) -> Meeting:
        """
        Creates a new meeting. Regular users can schedule up to 100 meetings in 24 hours and admin users up to 3000.

        :param title: Meeting title. The title can be a maximum of 128 characters long.
        :type title: str
        :param agenda: Meeting agenda. The agenda can be a maximum of 1300 characters long.
        :type agenda: str
        :param password: Meeting password. Must conform to the site's password complexity settings. Read password
            management for details.
        :type password: str
        :param start: Date and time for the start of meeting in any ISO 8601 compliant format. start cannot be before
            current date and time or after end. Duration between start and end cannot be shorter than 10 minutes or
            longer than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating
            date and time for a meeting. Please note that when a meeting is being updated, start of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, if start is within the same minute as the
            current time, start will be adjusted to the upcoming minute; otherwise, start will be adjusted with seconds
            and milliseconds stripped off. For instance, if the current time is 2022-03-01T10:32:16.657+08:00, start of
            2022-03-01T10:32:28.076+08:00 or 2022-03-01T10:32:41+08:00 will be adjusted to 2022-03-01T10:33:00+08:00,
            and start of 2022-03-01T11:32:28.076+08:00 or 2022-03-01T11:32:41+08:00 will be adjusted to
            2022-03-01T11:32:00+08:00.
        :type start: str
        :param end: Date and time for the end of meeting in any ISO 8601 compliant format. end cannot be before current
            date and time or before start. Duration between start and end cannot be shorter than 10 minutes or longer
            than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating date
            and time for a meeting. Please note that when a meeting is being updated, end of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, end will be adjusted with seconds and
            milliseconds stripped off. For instance, end of 2022-03-01T11:52:28.076+08:00 or 2022-03-01T11:52:41+08:00
            will be adjusted to 2022-03-01T11:52:00+08:00.
        :type end: str
        :param timezone: Time zone in which the meeting was originally scheduled (conforming with the IANA time zone
            database).
        :type timezone: str
        :param recurrence: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring
            meeting series, not to a meeting series with only one scheduled meeting. Multiple days or dates for monthly
            or yearly recurrence rule are not supported, only the first day or date specified is taken. For example,
            "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported
            as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
        :type recurrence: str
        :param enabled_auto_record_meeting: Whether or not meeting is recorded automatically.
        :type enabled_auto_record_meeting: bool
        :param allow_any_user_to_be_co_host: Whether or not to allow any attendee with a host account on the target
            site to become a cohost when joining the meeting. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_any_user_to_be_co_host: bool
        :param enabled_join_before_host: Whether or not to allow any attendee to join the meeting before the host joins
            the meeting.
        :type enabled_join_before_host: bool
        :param enable_connect_audio_before_host: Whether or not to allow any attendee to connect audio in the meeting
            before the host joins the meeting. This attribute is only applicable if the enabledJoinBeforeHost attribute
            is set to true.
        :type enable_connect_audio_before_host: bool
        :param join_before_host_minutes: The number of minutes an attendee can join the meeting before the meeting
            start time and the host joins. This attribute is only applicable if the enabledJoinBeforeHost attribute is
            set to true. Valid options are 0, 5, 10 and 15. Default is 0 if not specified.
        :type join_before_host_minutes: int
        :param exclude_password: Whether or not to exclude the meeting password from the email invitation.
        :type exclude_password: bool
        :param public_meeting: Whether or not to allow the meeting to be listed on the public calendar.
        :type public_meeting: bool
        :param reminder_time: The number of minutes before the meeting begins, that an email reminder is sent to the
            host.
        :type reminder_time: int
        :param unlocked_meeting_join_security: Specifies how the people who aren't on the invite can join the unlocked
            meeting.
        :type unlocked_meeting_join_security: UnlockedMeetingJoinSecurity
        :param session_type_id: Unique identifier for a meeting session type for the user. This attribute is required
            while scheduling webinar meeting. All available meeting session types enabled for the user can be retrieved
            by List Meeting Session Types API.
        :type session_type_id: int
        :param enabled_webcast_view: Whether or not webcast view is enabled.
        :type enabled_webcast_view: bool
        :param panelist_password: Password for panelists of a webinar meeting. Must conform to the site's password
            complexity settings. Read password management for details. If not specified, a random password conforming
            to the site's password rules will be generated automatically.
        :type panelist_password: str
        :param enable_automatic_lock: Whether or not to automatically lock the meeting after it starts.
        :type enable_automatic_lock: bool
        :param automatic_lock_minutes: The number of minutes after the meeting begins, for automatically locking it.
        :type automatic_lock_minutes: int
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee of the meeting with a host
            account on the target site to become a cohost. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_first_user_to_be_co_host: bool
        :param allow_authenticated_devices: Whether or not to allow authenticated video devices in the meeting's
            organization to start or join the meeting without a prompt.
        :type allow_authenticated_devices: bool
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin-level scopes. When used, the admin may specify the email of a
            user in a site they manage to be the meeting host.
        :type host_email: str
        :param site_url: URL of the Webex site which the meeting is updated on. If not specified, the meeting is
            created on user's preferred site. All available Webex sites and preferred site of the user can be retrieved
            by Get Site List API.
        :type site_url: str
        :param meeting_options: Meeting Options.
        :type meeting_options: MeetingOptions
        :param attendee_privileges: Attendee Privileges.
        :type attendee_privileges: AttendeePrivileges
        :param integration_tags: External keys created by an integration application in its own domain, for example
            Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries meetings
            by a key in its own domain. The maximum size of integrationTags is 3 and each item of integrationTags can
            be a maximum of 64 characters long. Please note that an empty or null integrationTags will delete all
            existing integration tags for the meeting implicitly. Developer can update integration tags for a
            meetingSeries but he cannot update it for a scheduledMeeting or a meeting instance.
        :type integration_tags: List[str]
        :param enabled_breakout_sessions: Whether or not breakout sessions are enabled. If the value of
            enabledBreakoutSessions is false, users can not set breakout sessions. If the value of
            enabledBreakoutSessions is true, users can update breakout sessions using the Update Breakout Sessions API.
            Updating breakout sessions are not supported by this API.
        :type enabled_breakout_sessions: bool
        :param tracking_codes: Tracking codes information. All available tracking codes and their options for the
            specified site can be retrieved by List Meeting Tracking Codes API. If an optional tracking code is missing
            from the trackingCodes array and there's a default option for this tracking code, the default option is
            assigned automatically. If the inputMode of a tracking code is select, its value must be one of the
            site-level options or the user-level value. Tracking code is not supported for a personal room meeting or
            an ad-hoc space meeting.
        :type tracking_codes: TrackingCodeItem
        :param audio_connection_options: Audio connection options.
        :type audio_connection_options: AudioConnectionOptions
        :param adhoc: Whether or not to create an ad-hoc meeting for the room specified by roomId. When true, roomId is
            required.
        :type adhoc: bool
        :param room_id: Unique identifier for the Webex space which the meeting is to be associated with. It can be
            retrieved by List Rooms. roomId is required when adhoc is true. When roomId is specified, the parameter
            hostEmail will be ignored.
        :type room_id: str
        :param template_id: Unique identifier for meeting template. Please note that start and end are optional when
            templateId is specified. The list of meeting templates that is available for the authenticated user can be
            retrieved from List Meeting Templates. This parameter is ignored for an ad-hoc meeting.
        :type template_id: str
        :param scheduled_type: When set as an attribute in a POST request body, specifies whether it's a regular
            meeting, a webinar, or a meeting scheduled in the user's personal room. If not specified, it's a regular
            meeting by default. The default value for an ad-hoc meeting is meeting and the user's input value will be
            ignored.
        :type scheduled_type: ScheduledType
        :param invitees: Invitees for meeting. The maximum size of invitees is 1000. If roomId is specified and
            invitees is missing, all the members in the space are invited implicitly. If both roomId and invitees are
            specified, only those in the invitees list are invited. coHost for each invitee is true by default if
            roomId is specified when creating a meeting, and anyone in the invitee list that is not qualified to be a
            cohost will be invited as a non-cohost invitee. The user's input value will be ignored for an ad-hoc
            meeting and the the members of the room specified by roomId except "me" will be used by default.
        :type invitees: InviteeForCreateMeeting
        :param registration: Meeting registration. When this option is enabled, meeting invitees must register personal
            information to join the meeting. Meeting invitees will receive an email with a registration link for the
            registration. When the registration form has been submitted and approved, an email with a real meeting link
            will be received. By clicking that link the meeting invitee can join the meeting. Please note that meeting
            registration does not apply to a meeting when it's a recurring meeting with a recurrence field or no
            password, or the Join Before Host option is enabled for the meeting. See Register for a Meeting in Cisco
            Webex Meetings for details. This parameter is ignored for an ad-hoc meeting.
        :type registration: Registration
        :param simultaneous_interpretation: Simultaneous interpretation information for a meeting.
        :type simultaneous_interpretation: SimultaneousInterpretation
        :param breakout_sessions: Breakout sessions are smaller groups that are split off from the main meeting or
            webinar. They allow a subset of participants to collaborate and share ideas over audio and video. Use
            breakout sessions for workshops, classrooms, or for when you need a moment to talk privately with a few
            participants outside of the main session. Please note that maximum number of breakout sessions in a meeting
            or webinar is 100. In webinars, if hosts preassign attendees to breakout sessions, the role of attendee
            will be changed to panelist. Breakout session is not supported for a meeting with simultaneous
            interpretation.
        :type breakout_sessions: BreakoutSession

        documentation: https://developer.webex.com/docs/api/v1/meetings/create-a-meeting
        """
        body = CreateMeetingBody()
        if title is not None:
            body.title = title
        if agenda is not None:
            body.agenda = agenda
        if password is not None:
            body.password = password
        if start is not None:
            body.start = start
        if end is not None:
            body.end = end
        if timezone is not None:
            body.timezone = timezone
        if recurrence is not None:
            body.recurrence = recurrence
        if enabled_auto_record_meeting is not None:
            body.enabled_auto_record_meeting = enabled_auto_record_meeting
        if allow_any_user_to_be_co_host is not None:
            body.allow_any_user_to_be_co_host = allow_any_user_to_be_co_host
        if enabled_join_before_host is not None:
            body.enabled_join_before_host = enabled_join_before_host
        if enable_connect_audio_before_host is not None:
            body.enable_connect_audio_before_host = enable_connect_audio_before_host
        if join_before_host_minutes is not None:
            body.join_before_host_minutes = join_before_host_minutes
        if exclude_password is not None:
            body.exclude_password = exclude_password
        if public_meeting is not None:
            body.public_meeting = public_meeting
        if reminder_time is not None:
            body.reminder_time = reminder_time
        if unlocked_meeting_join_security is not None:
            body.unlocked_meeting_join_security = unlocked_meeting_join_security
        if session_type_id is not None:
            body.session_type_id = session_type_id
        if enabled_webcast_view is not None:
            body.enabled_webcast_view = enabled_webcast_view
        if panelist_password is not None:
            body.panelist_password = panelist_password
        if enable_automatic_lock is not None:
            body.enable_automatic_lock = enable_automatic_lock
        if automatic_lock_minutes is not None:
            body.automatic_lock_minutes = automatic_lock_minutes
        if allow_first_user_to_be_co_host is not None:
            body.allow_first_user_to_be_co_host = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body.allow_authenticated_devices = allow_authenticated_devices
        if send_email is not None:
            body.send_email = send_email
        if host_email is not None:
            body.host_email = host_email
        if site_url is not None:
            body.site_url = site_url
        if meeting_options is not None:
            body.meeting_options = meeting_options
        if attendee_privileges is not None:
            body.attendee_privileges = attendee_privileges
        if integration_tags is not None:
            body.integration_tags = integration_tags
        if enabled_breakout_sessions is not None:
            body.enabled_breakout_sessions = enabled_breakout_sessions
        if tracking_codes is not None:
            body.tracking_codes = tracking_codes
        if audio_connection_options is not None:
            body.audio_connection_options = audio_connection_options
        if adhoc is not None:
            body.adhoc = adhoc
        if room_id is not None:
            body.room_id = room_id
        if template_id is not None:
            body.template_id = template_id
        if scheduled_type is not None:
            body.scheduled_type = scheduled_type
        if invitees is not None:
            body.invitees = invitees
        if registration is not None:
            body.registration = registration
        if simultaneous_interpretation is not None:
            body.simultaneous_interpretation = simultaneous_interpretation
        if breakout_sessions is not None:
            body.breakout_sessions = breakout_sessions
        url = self.ep()
        data = await super().post(url=url, data=body.model_dump_json())
        return Meeting.model_validate(data)

    async def get(self, meeting_id: str, current: bool = None, host_email: str = None) -> Meeting:
        """
        Retrieves details for a meeting with a specified meeting ID.

        :param meeting_id: Unique identifier for the meeting being requested.
        :type meeting_id: str
        :param current: Whether or not to retrieve only the current scheduled meeting of the meeting series, i.e. the
            meeting ready to join or start or the upcoming meeting of the meeting series. If it's true, return details
            for the current scheduled meeting of the series, i.e. the scheduled meeting ready to join or start or the
            upcoming scheduled meeting of the meeting series. If it's false or not specified, return details for the
            entire meeting series. This parameter only applies to meeting series.
        :type current: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for a meeting that is hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting
        """
        params = {}
        if current is not None:
            params['current'] = str(current).lower()
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep(f'{meeting_id}')
        data = await super().get(url=url, params=params)
        return Meeting.model_validate(data)

    def list_gen(self, meeting_number: str = None, web_link: str = None, room_id: str = None, meeting_type: str = None,
             state: str = None, scheduled_type: str = None, current: bool = None, from_: str = None, to_: str = None,
             host_email: str = None, site_url: str = None, integration_tag: str = None,
             **params) -> AsyncGenerator[Meeting, None, None]:
        """
        Retrieves details for meetings with a specified meeting number, web link, meeting type, etc. Please note that
        there are various products in the Webex Suite such as Meetings and Events. Currently, only meetings of the
        Meetings product are supported by this API, meetings of others in the suite are not supported. Ad-hoc meetings
        created by Create a Meeting with adhoc of true and a roomId will not be listed, but the ended and ongoing
        ad-hoc meeting instances will be listed.

        :param meeting_number: Meeting number for the meeting objects being requested. meetingNumber, webLink and
            roomId are mutually exclusive. If it's an exceptional meeting from a meeting series, the exceptional
            meeting instead of the primary meeting series is returned.
        :type meeting_number: str
        :param web_link: URL encoded link to information page for the meeting objects being requested. meetingNumber,
            webLink and roomId are mutually exclusive.
        :type web_link: str
        :param room_id: Associated Webex space ID for the meeting objects being requested. meetingNumber, webLink and
            roomId are mutually exclusive.
        :type room_id: str
        :param meeting_type: Meeting type for the meeting objects being requested. This parameter will be ignored if
            meetingNumber, webLink or roomId is specified. Possible values: meetingSeries, scheduledMeeting, meeting
        :type meeting_type: str
        :param state: Meeting state for the meeting objects being requested. If not specified, return meetings of all
            states. This parameter will be ignored if meetingNumber, webLink or roomId is specified. Details of an
            ended meeting will only be available 15 minutes after the meeting has ended. inProgress meetings are not
            fully supported. The API will try to return details of an inProgress meeting 15 minutes after the meeting
            starts. However, it may take longer depending on the traffic. See the Webex Meetings guide for more
            information about the states of meetings. Possible values: active, scheduled, ready, lobby, inProgress,
            ended, missed, expired
        :type state: str
        :param scheduled_type: Scheduled type for the meeting objects being requested. Possible values: meeting,
            webinar, personalRoomMeeting
        :type scheduled_type: str
        :param current: Flag identifying to retrieve the current scheduled meeting of the meeting series or the entire
            meeting series. This parameter only applies to scenarios where meetingNumber is specified and the meeting
            is not an exceptional meeting from a meeting series. If it's true, return the scheduled meeting of the
            meeting series which is ready to join or start or the upcoming scheduled meeting of the meeting series; if
            it's false, return the entire meeting series.
        :type current: bool
        :param from_: Start date and time (inclusive) in any ISO 8601 compliant format for the meeting objects being
            requested. from cannot be after to. This parameter will be ignored if meetingNumber, webLink or roomId is
            specified.
        :type from_: str
        :param to_: End date and time (exclusive) in any ISO 8601 compliant format for the meeting objects being
            requested. to cannot be before from. This parameter will be ignored if meetingNumber, webLink or roomId is
            specified.
        :type to_: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for meetings that are hosted by that user.
        :type host_email: str
        :param site_url: URL of the Webex site which the API lists meetings from. If not specified, the API lists
            meetings from user's all sites. All available Webex sites of the user can be retrieved by Get Site List
            API.
        :type site_url: str
        :param integration_tag: External key created by an integration application. This parameter is used by the
            integration application to query meetings by a key in its own domain such as a Zendesk ticket ID, a Jira
            ID, a Salesforce Opportunity ID, etc.
        :type integration_tag: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meetings
        """
        if meeting_number is not None:
            params['meetingNumber'] = meeting_number
        if web_link is not None:
            params['webLink'] = web_link
        if room_id is not None:
            params['roomId'] = room_id
        if meeting_type is not None:
            params['meetingType'] = meeting_type
        if state is not None:
            params['state'] = state
        if scheduled_type is not None:
            params['scheduledType'] = scheduled_type
        if current is not None:
            params['current'] = current
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        if integration_tag is not None:
            params['integrationTag'] = integration_tag
        url = self.ep()
        return self.session.follow_pagination(url=url, model=Meeting, params=params)

    async def list(self, meeting_number: str = None, web_link: str = None, room_id: str = None, meeting_type: str = None,
             state: str = None, scheduled_type: str = None, current: bool = None, from_: str = None, to_: str = None,
             host_email: str = None, site_url: str = None, integration_tag: str = None,
             **params) -> List[Meeting]:
        """
        Retrieves details for meetings with a specified meeting number, web link, meeting type, etc. Please note that
        there are various products in the Webex Suite such as Meetings and Events. Currently, only meetings of the
        Meetings product are supported by this API, meetings of others in the suite are not supported. Ad-hoc meetings
        created by Create a Meeting with adhoc of true and a roomId will not be listed, but the ended and ongoing
        ad-hoc meeting instances will be listed.

        :param meeting_number: Meeting number for the meeting objects being requested. meetingNumber, webLink and
            roomId are mutually exclusive. If it's an exceptional meeting from a meeting series, the exceptional
            meeting instead of the primary meeting series is returned.
        :type meeting_number: str
        :param web_link: URL encoded link to information page for the meeting objects being requested. meetingNumber,
            webLink and roomId are mutually exclusive.
        :type web_link: str
        :param room_id: Associated Webex space ID for the meeting objects being requested. meetingNumber, webLink and
            roomId are mutually exclusive.
        :type room_id: str
        :param meeting_type: Meeting type for the meeting objects being requested. This parameter will be ignored if
            meetingNumber, webLink or roomId is specified. Possible values: meetingSeries, scheduledMeeting, meeting
        :type meeting_type: str
        :param state: Meeting state for the meeting objects being requested. If not specified, return meetings of all
            states. This parameter will be ignored if meetingNumber, webLink or roomId is specified. Details of an
            ended meeting will only be available 15 minutes after the meeting has ended. inProgress meetings are not
            fully supported. The API will try to return details of an inProgress meeting 15 minutes after the meeting
            starts. However, it may take longer depending on the traffic. See the Webex Meetings guide for more
            information about the states of meetings. Possible values: active, scheduled, ready, lobby, inProgress,
            ended, missed, expired
        :type state: str
        :param scheduled_type: Scheduled type for the meeting objects being requested. Possible values: meeting,
            webinar, personalRoomMeeting
        :type scheduled_type: str
        :param current: Flag identifying to retrieve the current scheduled meeting of the meeting series or the entire
            meeting series. This parameter only applies to scenarios where meetingNumber is specified and the meeting
            is not an exceptional meeting from a meeting series. If it's true, return the scheduled meeting of the
            meeting series which is ready to join or start or the upcoming scheduled meeting of the meeting series; if
            it's false, return the entire meeting series.
        :type current: bool
        :param from_: Start date and time (inclusive) in any ISO 8601 compliant format for the meeting objects being
            requested. from cannot be after to. This parameter will be ignored if meetingNumber, webLink or roomId is
            specified.
        :type from_: str
        :param to_: End date and time (exclusive) in any ISO 8601 compliant format for the meeting objects being
            requested. to cannot be before from. This parameter will be ignored if meetingNumber, webLink or roomId is
            specified.
        :type to_: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return details for meetings that are hosted by that user.
        :type host_email: str
        :param site_url: URL of the Webex site which the API lists meetings from. If not specified, the API lists
            meetings from user's all sites. All available Webex sites of the user can be retrieved by Get Site List
            API.
        :type site_url: str
        :param integration_tag: External key created by an integration application. This parameter is used by the
            integration application to query meetings by a key in its own domain such as a Zendesk ticket ID, a Jira
            ID, a Salesforce Opportunity ID, etc.
        :type integration_tag: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meetings
        """
        if meeting_number is not None:
            params['meetingNumber'] = meeting_number
        if web_link is not None:
            params['webLink'] = web_link
        if room_id is not None:
            params['roomId'] = room_id
        if meeting_type is not None:
            params['meetingType'] = meeting_type
        if state is not None:
            params['state'] = state
        if scheduled_type is not None:
            params['scheduledType'] = scheduled_type
        if current is not None:
            params['current'] = current
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        if host_email is not None:
            params['hostEmail'] = host_email
        if site_url is not None:
            params['siteUrl'] = site_url
        if integration_tag is not None:
            params['integrationTag'] = integration_tag
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=Meeting, params=params)]

    def list_of_series_gen(self, meeting_series_id: str, from_: str = None, to_: str = None, meeting_type: str = None,
                       state: str = None, is_modified: bool = None, host_email: str = None,
                       **params) -> AsyncGenerator[ScheduledMeeting, None, None]:
        """
        Lists scheduled meeting and meeting instances of a meeting series identified by meetingSeriesId. Scheduled
        meetings of an ad-hoc meeting created by Create a Meeting with adhoc of true and a roomId will not be listed,
        but the ended and ongoing meeting instances of it will be listed.
        Each scheduled meeting or meeting instance of a meeting series has its own start, end, etc. Thus, for example,
        when a daily meeting has been scheduled from 2019-04-01 to 2019-04-10, there are 10 scheduled meeting instances
        in this series, one instance for each day, and each one has its own attributes. When a scheduled meeting has
        been started and ended or is happening, there are even more ended or in-progress meeting instances.
        Use this operation to list scheduled meeting and meeting instances of a meeting series within a specific date
        range.
        Long result sets are split into pages.
        trackingCodes is not supported for ended meeting instances.

        :param meeting_series_id: Unique identifier for the meeting series. Please note that currently meeting ID of a
            scheduled personal room meeting is not supported for this API.
        :type meeting_series_id: str
        :param from_: Start date and time (inclusive) for the range for which meetings are to be returned in any ISO
            8601 compliant format. from cannot be after to.
        :type from_: str
        :param to_: End date and time (exclusive) for the range for which meetings are to be returned in any ISO 8601
            compliant format. to cannot be before from.
        :type to_: str
        :param meeting_type: Meeting type for the meeting objects being requested. If not specified, return meetings of
            all types. Possible values: scheduledMeeting, meeting
        :type meeting_type: str
        :param state: Meeting state for the meetings being requested. If not specified, return meetings of all states.
            Details of an ended meeting will only be available 15 minutes after the meeting has ended. inProgress
            meetings are not fully supported. The API will try to return details of an inProgress meeting 15 minutes
            after the meeting starts. However, it may take longer depending on the traffic. See the Webex Meetings
            guide for more information about the states of meetings. Possible values: scheduled, ready, lobby,
            inProgress, ended, missed
        :type state: str
        :param is_modified: Flag identifying whether or not only to retrieve scheduled meeting instances which have
            been modified. This parameter only applies to scheduled meetings. If it's true, only return modified
            scheduled meetings; if it's false, only return unmodified scheduled meetings; if not specified, all
            scheduled meetings will be returned.
        :type is_modified: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return meetings that are hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meetings-of-a-meeting-series
        """
        params['meetingSeriesId'] = meeting_series_id
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        if meeting_type is not None:
            params['meetingType'] = meeting_type
        if state is not None:
            params['state'] = state
        if is_modified is not None:
            params['isModified'] = is_modified
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ScheduledMeeting, params=params)

    async def list_of_series(self, meeting_series_id: str, from_: str = None, to_: str = None, meeting_type: str = None,
                       state: str = None, is_modified: bool = None, host_email: str = None,
                       **params) -> List[ScheduledMeeting]:
        """
        Lists scheduled meeting and meeting instances of a meeting series identified by meetingSeriesId. Scheduled
        meetings of an ad-hoc meeting created by Create a Meeting with adhoc of true and a roomId will not be listed,
        but the ended and ongoing meeting instances of it will be listed.
        Each scheduled meeting or meeting instance of a meeting series has its own start, end, etc. Thus, for example,
        when a daily meeting has been scheduled from 2019-04-01 to 2019-04-10, there are 10 scheduled meeting instances
        in this series, one instance for each day, and each one has its own attributes. When a scheduled meeting has
        been started and ended or is happening, there are even more ended or in-progress meeting instances.
        Use this operation to list scheduled meeting and meeting instances of a meeting series within a specific date
        range.
        Long result sets are split into pages.
        trackingCodes is not supported for ended meeting instances.

        :param meeting_series_id: Unique identifier for the meeting series. Please note that currently meeting ID of a
            scheduled personal room meeting is not supported for this API.
        :type meeting_series_id: str
        :param from_: Start date and time (inclusive) for the range for which meetings are to be returned in any ISO
            8601 compliant format. from cannot be after to.
        :type from_: str
        :param to_: End date and time (exclusive) for the range for which meetings are to be returned in any ISO 8601
            compliant format. to cannot be before from.
        :type to_: str
        :param meeting_type: Meeting type for the meeting objects being requested. If not specified, return meetings of
            all types. Possible values: scheduledMeeting, meeting
        :type meeting_type: str
        :param state: Meeting state for the meetings being requested. If not specified, return meetings of all states.
            Details of an ended meeting will only be available 15 minutes after the meeting has ended. inProgress
            meetings are not fully supported. The API will try to return details of an inProgress meeting 15 minutes
            after the meeting starts. However, it may take longer depending on the traffic. See the Webex Meetings
            guide for more information about the states of meetings. Possible values: scheduled, ready, lobby,
            inProgress, ended, missed
        :type state: str
        :param is_modified: Flag identifying whether or not only to retrieve scheduled meeting instances which have
            been modified. This parameter only applies to scheduled meetings. If it's true, only return modified
            scheduled meetings; if it's false, only return unmodified scheduled meetings; if not specified, all
            scheduled meetings will be returned.
        :type is_modified: bool
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will return meetings that are hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meetings-of-a-meeting-series
        """
        params['meetingSeriesId'] = meeting_series_id
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        if meeting_type is not None:
            params['meetingType'] = meeting_type
        if state is not None:
            params['state'] = state
        if is_modified is not None:
            params['isModified'] = is_modified
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=ScheduledMeeting, params=params)]

    async def patch(self, meeting_id: str, title: str = None, agenda: str = None, password: str = None, start: str = None,
              end: str = None, timezone: str = None, recurrence: str = None, enabled_auto_record_meeting: bool = None,
              allow_any_user_to_be_co_host: bool = None, enabled_join_before_host: bool = None,
              enable_connect_audio_before_host: bool = None, join_before_host_minutes: int = None,
              exclude_password: bool = None, public_meeting: bool = None, reminder_time: int = None,
              unlocked_meeting_join_security: UnlockedMeetingJoinSecurity = None, session_type_id: int = None,
              enabled_webcast_view: bool = None, panelist_password: str = None, enable_automatic_lock: bool = None,
              automatic_lock_minutes: int = None, allow_first_user_to_be_co_host: bool = None,
              allow_authenticated_devices: bool = None, send_email: bool = None, host_email: str = None,
              site_url: str = None, meeting_options: MeetingOptions = None,
              attendee_privileges: AttendeePrivileges = None, integration_tags: List[str] = None,
              enabled_breakout_sessions: bool = None, tracking_codes: TrackingCodeItem = None,
              audio_connection_options: AudioConnectionOptions = None) -> PatchMeetingResponse:
        """
        Updates details for a meeting with a specified meeting ID. This operation applies to meeting series and
        scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Ad-hoc meetings created by
        Create a Meeting with adhoc of true and a roomId cannot be updated.

        :param meeting_id: Unique identifier for the meeting to be updated. This parameter applies to meeting series
            and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Please note that
            currently meeting ID of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param title: Meeting title. The title can be a maximum of 128 characters long.
        :type title: str
        :param agenda: Meeting agenda. The agenda can be a maximum of 1300 characters long.
        :type agenda: str
        :param password: Meeting password. Must conform to the site's password complexity settings. Read password
            management for details.
        :type password: str
        :param start: Date and time for the start of meeting in any ISO 8601 compliant format. start cannot be before
            current date and time or after end. Duration between start and end cannot be shorter than 10 minutes or
            longer than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating
            date and time for a meeting. Please note that when a meeting is being updated, start of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, if start is within the same minute as the
            current time, start will be adjusted to the upcoming minute; otherwise, start will be adjusted with seconds
            and milliseconds stripped off. For instance, if the current time is 2022-03-01T10:32:16.657+08:00, start of
            2022-03-01T10:32:28.076+08:00 or 2022-03-01T10:32:41+08:00 will be adjusted to 2022-03-01T10:33:00+08:00,
            and start of 2022-03-01T11:32:28.076+08:00 or 2022-03-01T11:32:41+08:00 will be adjusted to
            2022-03-01T11:32:00+08:00.
        :type start: str
        :param end: Date and time for the end of meeting in any ISO 8601 compliant format. end cannot be before current
            date and time or before start. Duration between start and end cannot be shorter than 10 minutes or longer
            than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating date
            and time for a meeting. Please note that when a meeting is being updated, end of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, end will be adjusted with seconds and
            milliseconds stripped off. For instance, end of 2022-03-01T11:52:28.076+08:00 or 2022-03-01T11:52:41+08:00
            will be adjusted to 2022-03-01T11:52:00+08:00.
        :type end: str
        :param timezone: Time zone in which the meeting was originally scheduled (conforming with the IANA time zone
            database).
        :type timezone: str
        :param recurrence: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring
            meeting series, not to a meeting series with only one scheduled meeting. Multiple days or dates for monthly
            or yearly recurrence rule are not supported, only the first day or date specified is taken. For example,
            "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported
            as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
        :type recurrence: str
        :param enabled_auto_record_meeting: Whether or not meeting is recorded automatically.
        :type enabled_auto_record_meeting: bool
        :param allow_any_user_to_be_co_host: Whether or not to allow any attendee with a host account on the target
            site to become a cohost when joining the meeting. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_any_user_to_be_co_host: bool
        :param enabled_join_before_host: Whether or not to allow any attendee to join the meeting before the host joins
            the meeting.
        :type enabled_join_before_host: bool
        :param enable_connect_audio_before_host: Whether or not to allow any attendee to connect audio in the meeting
            before the host joins the meeting. This attribute is only applicable if the enabledJoinBeforeHost attribute
            is set to true.
        :type enable_connect_audio_before_host: bool
        :param join_before_host_minutes: The number of minutes an attendee can join the meeting before the meeting
            start time and the host joins. This attribute is only applicable if the enabledJoinBeforeHost attribute is
            set to true. Valid options are 0, 5, 10 and 15. Default is 0 if not specified.
        :type join_before_host_minutes: int
        :param exclude_password: Whether or not to exclude the meeting password from the email invitation.
        :type exclude_password: bool
        :param public_meeting: Whether or not to allow the meeting to be listed on the public calendar.
        :type public_meeting: bool
        :param reminder_time: The number of minutes before the meeting begins, that an email reminder is sent to the
            host.
        :type reminder_time: int
        :param unlocked_meeting_join_security: Specifies how the people who aren't on the invite can join the unlocked
            meeting.
        :type unlocked_meeting_join_security: UnlockedMeetingJoinSecurity
        :param session_type_id: Unique identifier for a meeting session type for the user. This attribute is required
            while scheduling webinar meeting. All available meeting session types enabled for the user can be retrieved
            by List Meeting Session Types API.
        :type session_type_id: int
        :param enabled_webcast_view: Whether or not webcast view is enabled.
        :type enabled_webcast_view: bool
        :param panelist_password: Password for panelists of a webinar meeting. Must conform to the site's password
            complexity settings. Read password management for details. If not specified, a random password conforming
            to the site's password rules will be generated automatically.
        :type panelist_password: str
        :param enable_automatic_lock: Whether or not to automatically lock the meeting after it starts.
        :type enable_automatic_lock: bool
        :param automatic_lock_minutes: The number of minutes after the meeting begins, for automatically locking it.
        :type automatic_lock_minutes: int
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee of the meeting with a host
            account on the target site to become a cohost. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_first_user_to_be_co_host: bool
        :param allow_authenticated_devices: Whether or not to allow authenticated video devices in the meeting's
            organization to start or join the meeting without a prompt.
        :type allow_authenticated_devices: bool
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin-level scopes. When used, the admin may specify the email of a
            user in a site they manage to be the meeting host.
        :type host_email: str
        :param site_url: URL of the Webex site which the meeting is updated on. If not specified, the meeting is
            created on user's preferred site. All available Webex sites and preferred site of the user can be retrieved
            by Get Site List API.
        :type site_url: str
        :param meeting_options: Meeting Options.
        :type meeting_options: MeetingOptions
        :param attendee_privileges: Attendee Privileges.
        :type attendee_privileges: AttendeePrivileges
        :param integration_tags: External keys created by an integration application in its own domain, for example
            Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries meetings
            by a key in its own domain. The maximum size of integrationTags is 3 and each item of integrationTags can
            be a maximum of 64 characters long. Please note that an empty or null integrationTags will delete all
            existing integration tags for the meeting implicitly. Developer can update integration tags for a
            meetingSeries but he cannot update it for a scheduledMeeting or a meeting instance.
        :type integration_tags: List[str]
        :param enabled_breakout_sessions: Whether or not breakout sessions are enabled. If the value of
            enabledBreakoutSessions is false, users can not set breakout sessions. If the value of
            enabledBreakoutSessions is true, users can update breakout sessions using the Update Breakout Sessions API.
            Updating breakout sessions are not supported by this API.
        :type enabled_breakout_sessions: bool
        :param tracking_codes: Tracking codes information. All available tracking codes and their options for the
            specified site can be retrieved by List Meeting Tracking Codes API. If an optional tracking code is missing
            from the trackingCodes array and there's a default option for this tracking code, the default option is
            assigned automatically. If the inputMode of a tracking code is select, its value must be one of the
            site-level options or the user-level value. Tracking code is not supported for a personal room meeting or
            an ad-hoc space meeting.
        :type tracking_codes: TrackingCodeItem
        :param audio_connection_options: Audio connection options.
        :type audio_connection_options: AudioConnectionOptions

        documentation: https://developer.webex.com/docs/api/v1/meetings/patch-a-meeting
        """
        body = PatchMeetingBody()
        if title is not None:
            body.title = title
        if agenda is not None:
            body.agenda = agenda
        if password is not None:
            body.password = password
        if start is not None:
            body.start = start
        if end is not None:
            body.end = end
        if timezone is not None:
            body.timezone = timezone
        if recurrence is not None:
            body.recurrence = recurrence
        if enabled_auto_record_meeting is not None:
            body.enabled_auto_record_meeting = enabled_auto_record_meeting
        if allow_any_user_to_be_co_host is not None:
            body.allow_any_user_to_be_co_host = allow_any_user_to_be_co_host
        if enabled_join_before_host is not None:
            body.enabled_join_before_host = enabled_join_before_host
        if enable_connect_audio_before_host is not None:
            body.enable_connect_audio_before_host = enable_connect_audio_before_host
        if join_before_host_minutes is not None:
            body.join_before_host_minutes = join_before_host_minutes
        if exclude_password is not None:
            body.exclude_password = exclude_password
        if public_meeting is not None:
            body.public_meeting = public_meeting
        if reminder_time is not None:
            body.reminder_time = reminder_time
        if unlocked_meeting_join_security is not None:
            body.unlocked_meeting_join_security = unlocked_meeting_join_security
        if session_type_id is not None:
            body.session_type_id = session_type_id
        if enabled_webcast_view is not None:
            body.enabled_webcast_view = enabled_webcast_view
        if panelist_password is not None:
            body.panelist_password = panelist_password
        if enable_automatic_lock is not None:
            body.enable_automatic_lock = enable_automatic_lock
        if automatic_lock_minutes is not None:
            body.automatic_lock_minutes = automatic_lock_minutes
        if allow_first_user_to_be_co_host is not None:
            body.allow_first_user_to_be_co_host = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body.allow_authenticated_devices = allow_authenticated_devices
        if send_email is not None:
            body.send_email = send_email
        if host_email is not None:
            body.host_email = host_email
        if site_url is not None:
            body.site_url = site_url
        if meeting_options is not None:
            body.meeting_options = meeting_options
        if attendee_privileges is not None:
            body.attendee_privileges = attendee_privileges
        if integration_tags is not None:
            body.integration_tags = integration_tags
        if enabled_breakout_sessions is not None:
            body.enabled_breakout_sessions = enabled_breakout_sessions
        if tracking_codes is not None:
            body.tracking_codes = tracking_codes
        if audio_connection_options is not None:
            body.audio_connection_options = audio_connection_options
        url = self.ep(f'{meeting_id}')
        data = await super().patch(url=url, data=body.model_dump_json())
        return PatchMeetingResponse.model_validate(data)

    async def update(self, meeting_id: str, title: str = None, agenda: str = None, password: str = None, start: str = None,
               end: str = None, timezone: str = None, recurrence: str = None, enabled_auto_record_meeting: bool = None,
               allow_any_user_to_be_co_host: bool = None, enabled_join_before_host: bool = None,
               enable_connect_audio_before_host: bool = None, join_before_host_minutes: int = None,
               exclude_password: bool = None, public_meeting: bool = None, reminder_time: int = None,
               unlocked_meeting_join_security: UnlockedMeetingJoinSecurity = None, session_type_id: int = None,
               enabled_webcast_view: bool = None, panelist_password: str = None, enable_automatic_lock: bool = None,
               automatic_lock_minutes: int = None, allow_first_user_to_be_co_host: bool = None,
               allow_authenticated_devices: bool = None, send_email: bool = None, host_email: str = None,
               site_url: str = None, meeting_options: MeetingOptions = None,
               attendee_privileges: AttendeePrivileges = None, integration_tags: List[str] = None,
               enabled_breakout_sessions: bool = None, tracking_codes: TrackingCodeItem = None,
               audio_connection_options: AudioConnectionOptions = None) -> PatchMeetingResponse:
        """
        Updates details for a meeting with a specified meeting ID. This operation applies to meeting series and
        scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Ad-hoc meetings created by
        Create a Meeting with adhoc of true and a roomId cannot be updated.

        :param meeting_id: Unique identifier for the meeting to be updated. This parameter applies to meeting series
            and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Please note that
            currently meeting ID of a scheduled personal room meeting is not supported for this API.
        :type meeting_id: str
        :param title: Meeting title. The title can be a maximum of 128 characters long.
        :type title: str
        :param agenda: Meeting agenda. The agenda can be a maximum of 1300 characters long.
        :type agenda: str
        :param password: Meeting password. Must conform to the site's password complexity settings. Read password
            management for details.
        :type password: str
        :param start: Date and time for the start of meeting in any ISO 8601 compliant format. start cannot be before
            current date and time or after end. Duration between start and end cannot be shorter than 10 minutes or
            longer than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating
            date and time for a meeting. Please note that when a meeting is being updated, start of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, if start is within the same minute as the
            current time, start will be adjusted to the upcoming minute; otherwise, start will be adjusted with seconds
            and milliseconds stripped off. For instance, if the current time is 2022-03-01T10:32:16.657+08:00, start of
            2022-03-01T10:32:28.076+08:00 or 2022-03-01T10:32:41+08:00 will be adjusted to 2022-03-01T10:33:00+08:00,
            and start of 2022-03-01T11:32:28.076+08:00 or 2022-03-01T11:32:41+08:00 will be adjusted to
            2022-03-01T11:32:00+08:00.
        :type start: str
        :param end: Date and time for the end of meeting in any ISO 8601 compliant format. end cannot be before current
            date and time or before start. Duration between start and end cannot be shorter than 10 minutes or longer
            than 24 hours. Refer to the Webex Meetings guide for more information about restrictions on updating date
            and time for a meeting. Please note that when a meeting is being updated, end of the meeting will be
            accurate to minutes, not seconds or milliseconds. Therefore, end will be adjusted with seconds and
            milliseconds stripped off. For instance, end of 2022-03-01T11:52:28.076+08:00 or 2022-03-01T11:52:41+08:00
            will be adjusted to 2022-03-01T11:52:00+08:00.
        :type end: str
        :param timezone: Time zone in which the meeting was originally scheduled (conforming with the IANA time zone
            database).
        :type timezone: str
        :param recurrence: Meeting series recurrence rule (conforming with RFC 2445). Applies only to a recurring
            meeting series, not to a meeting series with only one scheduled meeting. Multiple days or dates for monthly
            or yearly recurrence rule are not supported, only the first day or date specified is taken. For example,
            "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10,11,12" is not supported and it will be partially supported
            as "FREQ=MONTHLY;INTERVAL=1;COUNT=10;BYMONTHDAY=10".
        :type recurrence: str
        :param enabled_auto_record_meeting: Whether or not meeting is recorded automatically.
        :type enabled_auto_record_meeting: bool
        :param allow_any_user_to_be_co_host: Whether or not to allow any attendee with a host account on the target
            site to become a cohost when joining the meeting. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_any_user_to_be_co_host: bool
        :param enabled_join_before_host: Whether or not to allow any attendee to join the meeting before the host joins
            the meeting.
        :type enabled_join_before_host: bool
        :param enable_connect_audio_before_host: Whether or not to allow any attendee to connect audio in the meeting
            before the host joins the meeting. This attribute is only applicable if the enabledJoinBeforeHost attribute
            is set to true.
        :type enable_connect_audio_before_host: bool
        :param join_before_host_minutes: The number of minutes an attendee can join the meeting before the meeting
            start time and the host joins. This attribute is only applicable if the enabledJoinBeforeHost attribute is
            set to true. Valid options are 0, 5, 10 and 15. Default is 0 if not specified.
        :type join_before_host_minutes: int
        :param exclude_password: Whether or not to exclude the meeting password from the email invitation.
        :type exclude_password: bool
        :param public_meeting: Whether or not to allow the meeting to be listed on the public calendar.
        :type public_meeting: bool
        :param reminder_time: The number of minutes before the meeting begins, that an email reminder is sent to the
            host.
        :type reminder_time: int
        :param unlocked_meeting_join_security: Specifies how the people who aren't on the invite can join the unlocked
            meeting.
        :type unlocked_meeting_join_security: UnlockedMeetingJoinSecurity
        :param session_type_id: Unique identifier for a meeting session type for the user. This attribute is required
            while scheduling webinar meeting. All available meeting session types enabled for the user can be retrieved
            by List Meeting Session Types API.
        :type session_type_id: int
        :param enabled_webcast_view: Whether or not webcast view is enabled.
        :type enabled_webcast_view: bool
        :param panelist_password: Password for panelists of a webinar meeting. Must conform to the site's password
            complexity settings. Read password management for details. If not specified, a random password conforming
            to the site's password rules will be generated automatically.
        :type panelist_password: str
        :param enable_automatic_lock: Whether or not to automatically lock the meeting after it starts.
        :type enable_automatic_lock: bool
        :param automatic_lock_minutes: The number of minutes after the meeting begins, for automatically locking it.
        :type automatic_lock_minutes: int
        :param allow_first_user_to_be_co_host: Whether or not to allow the first attendee of the meeting with a host
            account on the target site to become a cohost. The target site is specified by siteUrl parameter when
            creating the meeting; if not specified, it's user's preferred site.
        :type allow_first_user_to_be_co_host: bool
        :param allow_authenticated_devices: Whether or not to allow authenticated video devices in the meeting's
            organization to start or join the meeting without a prompt.
        :type allow_authenticated_devices: bool
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool
        :param host_email: Email address for the meeting host. This attribute should only be set if the user or
            application calling the API has the admin-level scopes. When used, the admin may specify the email of a
            user in a site they manage to be the meeting host.
        :type host_email: str
        :param site_url: URL of the Webex site which the meeting is updated on. If not specified, the meeting is
            created on user's preferred site. All available Webex sites and preferred site of the user can be retrieved
            by Get Site List API.
        :type site_url: str
        :param meeting_options: Meeting Options.
        :type meeting_options: MeetingOptions
        :param attendee_privileges: Attendee Privileges.
        :type attendee_privileges: AttendeePrivileges
        :param integration_tags: External keys created by an integration application in its own domain, for example
            Zendesk ticket IDs, Jira IDs, Salesforce Opportunity IDs, etc. The integration application queries meetings
            by a key in its own domain. The maximum size of integrationTags is 3 and each item of integrationTags can
            be a maximum of 64 characters long. Please note that an empty or null integrationTags will delete all
            existing integration tags for the meeting implicitly. Developer can update integration tags for a
            meetingSeries but he cannot update it for a scheduledMeeting or a meeting instance.
        :type integration_tags: List[str]
        :param enabled_breakout_sessions: Whether or not breakout sessions are enabled. If the value of
            enabledBreakoutSessions is false, users can not set breakout sessions. If the value of
            enabledBreakoutSessions is true, users can update breakout sessions using the Update Breakout Sessions API.
            Updating breakout sessions are not supported by this API.
        :type enabled_breakout_sessions: bool
        :param tracking_codes: Tracking codes information. All available tracking codes and their options for the
            specified site can be retrieved by List Meeting Tracking Codes API. If an optional tracking code is missing
            from the trackingCodes array and there's a default option for this tracking code, the default option is
            assigned automatically. If the inputMode of a tracking code is select, its value must be one of the
            site-level options or the user-level value. Tracking code is not supported for a personal room meeting or
            an ad-hoc space meeting.
        :type tracking_codes: TrackingCodeItem
        :param audio_connection_options: Audio connection options.
        :type audio_connection_options: AudioConnectionOptions

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-a-meeting
        """
        body = PatchMeetingBody()
        if title is not None:
            body.title = title
        if agenda is not None:
            body.agenda = agenda
        if password is not None:
            body.password = password
        if start is not None:
            body.start = start
        if end is not None:
            body.end = end
        if timezone is not None:
            body.timezone = timezone
        if recurrence is not None:
            body.recurrence = recurrence
        if enabled_auto_record_meeting is not None:
            body.enabled_auto_record_meeting = enabled_auto_record_meeting
        if allow_any_user_to_be_co_host is not None:
            body.allow_any_user_to_be_co_host = allow_any_user_to_be_co_host
        if enabled_join_before_host is not None:
            body.enabled_join_before_host = enabled_join_before_host
        if enable_connect_audio_before_host is not None:
            body.enable_connect_audio_before_host = enable_connect_audio_before_host
        if join_before_host_minutes is not None:
            body.join_before_host_minutes = join_before_host_minutes
        if exclude_password is not None:
            body.exclude_password = exclude_password
        if public_meeting is not None:
            body.public_meeting = public_meeting
        if reminder_time is not None:
            body.reminder_time = reminder_time
        if unlocked_meeting_join_security is not None:
            body.unlocked_meeting_join_security = unlocked_meeting_join_security
        if session_type_id is not None:
            body.session_type_id = session_type_id
        if enabled_webcast_view is not None:
            body.enabled_webcast_view = enabled_webcast_view
        if panelist_password is not None:
            body.panelist_password = panelist_password
        if enable_automatic_lock is not None:
            body.enable_automatic_lock = enable_automatic_lock
        if automatic_lock_minutes is not None:
            body.automatic_lock_minutes = automatic_lock_minutes
        if allow_first_user_to_be_co_host is not None:
            body.allow_first_user_to_be_co_host = allow_first_user_to_be_co_host
        if allow_authenticated_devices is not None:
            body.allow_authenticated_devices = allow_authenticated_devices
        if send_email is not None:
            body.send_email = send_email
        if host_email is not None:
            body.host_email = host_email
        if site_url is not None:
            body.site_url = site_url
        if meeting_options is not None:
            body.meeting_options = meeting_options
        if attendee_privileges is not None:
            body.attendee_privileges = attendee_privileges
        if integration_tags is not None:
            body.integration_tags = integration_tags
        if enabled_breakout_sessions is not None:
            body.enabled_breakout_sessions = enabled_breakout_sessions
        if tracking_codes is not None:
            body.tracking_codes = tracking_codes
        if audio_connection_options is not None:
            body.audio_connection_options = audio_connection_options
        url = self.ep(f'{meeting_id}')
        data = await super().put(url=url, data=body.model_dump_json())
        return PatchMeetingResponse.model_validate(data)

    async def delete(self, meeting_id: str, host_email: str = None, send_email: bool = None):
        """
        Deletes a meeting with a specified meeting ID. The deleted meeting cannot be recovered. This operation applies
        to meeting series and scheduled meetings. It doesn't apply to ended or in-progress meeting instances. Ad-hoc
        meetings created by Create a Meeting with adhoc of true and a roomId cannot be deleted.

        :param meeting_id: Unique identifier for the meeting to be deleted. This parameter applies to meeting series
            and scheduled meetings. It doesn't apply to ended or in-progress meeting instances.
        :type meeting_id: str
        :param host_email: Email address for the meeting host. This parameter is only used if the user or application
            calling the API has the admin-level scopes. If set, the admin may specify the email of a user in a site
            they manage and the API will delete a meeting that is hosted by that user.
        :type host_email: str
        :param send_email: Whether or not to send emails to host and invitees. It is an optional field and default
            value is true.
        :type send_email: bool

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-a-meeting
        """
        params = {}
        if host_email is not None:
            params['hostEmail'] = host_email
        if send_email is not None:
            params['sendEmail'] = send_email
        url = self.ep(f'{meeting_id}')
        await super().delete(url=url, params=params)
        return

    async def join(self, meeting_id: str = None, meeting_number: str = None, web_link: str = None, join_directly: bool = None,
             email: str = None, display_name: str = None, password: str = None,
             expiration_minutes: int = None) -> JoinMeetingResponse:
        """
        Retrieves a meeting join link for a meeting with a specified meetingId, meetingNumber, or webLink that allows
        users to join the meeting directly without logging in and entering a password.

        :param meeting_id: Unique identifier for the meeting. This parameter applies to meeting series and scheduled
            meetings. It doesn't apply to ended or in-progress meeting instances. Please note that currently meeting ID
            of a scheduled personal room meeting is also supported for this API.
        :type meeting_id: str
        :param meeting_number: Meeting number. Applies to meeting series, scheduled meeting, and meeting instances, but
            not to meeting instances which have ended.
        :type meeting_number: str
        :param web_link: Link to a meeting information page where the meeting client is launched if the meeting is
            ready to start or join.
        :type web_link: str
        :param join_directly: Whether or not to redirect to joinLink. It is an optional field and default value is
            true.
        :type join_directly: bool
        :param email: Email address of meeting participant. If the user is a guest issuer, email is required.
        :type email: str
        :param display_name: Display name of meeting participant. The maximum length of displayName is 128 characters.
            If the user is a guest issuer, displayName is required.
        :type display_name: str
        :param password: It's required when the meeting is protected by a password and the current user is not
            privileged to view it if they are not a host, cohost or invitee of the meeting.
        :type password: str
        :param expiration_minutes: Expiration duration of joinLink in minutes. Must be between 1 and 60.
        :type expiration_minutes: int

        documentation: https://developer.webex.com/docs/api/v1/meetings/join-a-meeting
        """
        body = JoinMeetingBody()
        if meeting_id is not None:
            body.meeting_id = meeting_id
        if meeting_number is not None:
            body.meeting_number = meeting_number
        if web_link is not None:
            body.web_link = web_link
        if join_directly is not None:
            body.join_directly = join_directly
        if email is not None:
            body.email = email
        if display_name is not None:
            body.display_name = display_name
        if password is not None:
            body.password = password
        if expiration_minutes is not None:
            body.expiration_minutes = expiration_minutes
        url = self.ep('join')
        data = await super().post(url=url, data=body.model_dump_json())
        return JoinMeetingResponse.model_validate(data)

    async def update_simultaneous_interpretation(self, meeting_id: str, enabled: bool,
                                           interpreters:
                                           InterpreterForSimultaneousInterpretation =
                                           None) -> SimultaneousInterpretation:
        """
        Updates simultaneous interpretation options of a meeting with a specified meeting ID. This operation applies to
        meeting series and scheduled meetings. It doesn't apply to ended or in-progress meeting instances.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param enabled: Whether or not simultaneous interpretation is enabled.
        :type enabled: bool
        :param interpreters: Interpreters for meeting.
        :type interpreters: InterpreterForSimultaneousInterpretation

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-meeting-simultaneous-interpretation
        """
        body = SimultaneousInterpretation()
        if enabled is not None:
            body.enabled = enabled
        if interpreters is not None:
            body.interpreters = interpreters
        url = self.ep(f'{meeting_id}/simultaneousInterpretation')
        data = await super().put(url=url, data=body.model_dump_json())
        return SimultaneousInterpretation.model_validate(data)

    async def survey(self, meeting_id: str) -> GetMeetingSurveyResponse:
        """
        Retrieves details for a meeting survey identified by meetingId.

        :param meeting_id: Unique identifier for the meeting. Please note that only the meeting ID of a scheduled
            webinar is supported for this API.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-survey
        """
        url = self.ep(f'{meeting_id}/survey')
        data = await super().get(url=url)
        return GetMeetingSurveyResponse.model_validate(data)

    def list_survey_results_gen(self, meeting_id: str, meeting_start_time_from: str = None,
                            meeting_start_time_to: str = None, **params) -> AsyncGenerator[SurveyResult, None, None]:
        """
        Retrieves results for a meeting survey identified by meetingId.

        :param meeting_id: Unique identifier for the meeting. Please note that only the meeting ID of a scheduled
            webinar is supported for this API.
        :type meeting_id: str
        :param meeting_start_time_from: Start date and time (inclusive) in any ISO 8601 compliant format for the
            meeting objects being requested. meetingStartTimeFrom cannot be after meetingStartTimeTo. This parameter
            will be ignored if meetingId is the unique identifier for the specific meeting instance. When meetingId is
            not the unique identifier for the specific meeting instance, the meetingStartTimeFrom, if not specified,
            equals meetingStartTimeTo minus 1 month; if meetingStartTimeTo is also not specified, the default value for
            meetingStartTimeFrom is 1 month before the current date and time.
        :type meeting_start_time_from: str
        :param meeting_start_time_to: End date and time (exclusive) in any ISO 8601 compliant format for the meeting
            objects being requested. meetingStartTimeTo cannot be prior to meetingStartTimeFrom. This parameter will be
            ignored if meetingId is the unique identifier for the specific meeting instance. When meetingId is not the
            unique identifier for the specific meeting instance, if meetingStartTimeFrom is also not specified, the
            default value for meetingStartTimeTo is the current date and time;For example,if meetingStartTimeFrom is a
            month ago, the default value for meetingStartTimeTo is 1 month after meetingStartTimeFrom.Otherwise it is
            the current date and time.
        :type meeting_start_time_to: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-survey-results
        """
        if meeting_start_time_from is not None:
            params['meetingStartTimeFrom'] = meeting_start_time_from
        if meeting_start_time_to is not None:
            params['meetingStartTimeTo'] = meeting_start_time_to
        url = self.ep(f'{meeting_id}/surveyResults')
        return self.session.follow_pagination(url=url, model=SurveyResult, params=params)

    async def list_survey_results(self, meeting_id: str, meeting_start_time_from: str = None,
                            meeting_start_time_to: str = None, **params) -> List[SurveyResult]:
        """
        Retrieves results for a meeting survey identified by meetingId.

        :param meeting_id: Unique identifier for the meeting. Please note that only the meeting ID of a scheduled
            webinar is supported for this API.
        :type meeting_id: str
        :param meeting_start_time_from: Start date and time (inclusive) in any ISO 8601 compliant format for the
            meeting objects being requested. meetingStartTimeFrom cannot be after meetingStartTimeTo. This parameter
            will be ignored if meetingId is the unique identifier for the specific meeting instance. When meetingId is
            not the unique identifier for the specific meeting instance, the meetingStartTimeFrom, if not specified,
            equals meetingStartTimeTo minus 1 month; if meetingStartTimeTo is also not specified, the default value for
            meetingStartTimeFrom is 1 month before the current date and time.
        :type meeting_start_time_from: str
        :param meeting_start_time_to: End date and time (exclusive) in any ISO 8601 compliant format for the meeting
            objects being requested. meetingStartTimeTo cannot be prior to meetingStartTimeFrom. This parameter will be
            ignored if meetingId is the unique identifier for the specific meeting instance. When meetingId is not the
            unique identifier for the specific meeting instance, if meetingStartTimeFrom is also not specified, the
            default value for meetingStartTimeTo is the current date and time;For example,if meetingStartTimeFrom is a
            month ago, the default value for meetingStartTimeTo is 1 month after meetingStartTimeFrom.Otherwise it is
            the current date and time.
        :type meeting_start_time_to: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-survey-results
        """
        if meeting_start_time_from is not None:
            params['meetingStartTimeFrom'] = meeting_start_time_from
        if meeting_start_time_to is not None:
            params['meetingStartTimeTo'] = meeting_start_time_to
        url = self.ep(f'{meeting_id}/surveyResults')
        return [o async for o in self.session.follow_pagination(url=url, model=SurveyResult, params=params)]

    def list_tracking_codes_gen(self, service: str, site_url: str = None,
                            host_email: str = None) -> AsyncGenerator[TrackingCode, None, None]:
        """
        Lists tracking codes on a site by a meeting host. The result indicates which tracking codes and what options
        can be used to create or update a meeting on the specified site.

        :param service: Service for schedule or sign-up pages.
        :type service: str
        :param site_url: URL of the Webex site which the API retrieves the tracking code from. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and preferred
            sites of a user can be retrieved by Get Site List API.
        :type site_url: str
        :param host_email: Email address for the meeting host. This parameter is only used if a user or application
            calling the API has the admin-level scopes. The admin may specify the email of a user on a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-tracking-codes
        """
        params = {}
        params['service'] = service
        if site_url is not None:
            params['siteUrl'] = site_url
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep('trackingCodes')
        return self.session.follow_pagination(url=url, model=TrackingCode, params=params)

    async def list_tracking_codes(self, service: str, site_url: str = None,
                            host_email: str = None) -> List[TrackingCode]:
        """
        Lists tracking codes on a site by a meeting host. The result indicates which tracking codes and what options
        can be used to create or update a meeting on the specified site.

        :param service: Service for schedule or sign-up pages.
        :type service: str
        :param site_url: URL of the Webex site which the API retrieves the tracking code from. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and preferred
            sites of a user can be retrieved by Get Site List API.
        :type site_url: str
        :param host_email: Email address for the meeting host. This parameter is only used if a user or application
            calling the API has the admin-level scopes. The admin may specify the email of a user on a site they manage
            and the API will return meeting participants of the meetings that are hosted by that user.
        :type host_email: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-tracking-codes
        """
        params = {}
        params['service'] = service
        if site_url is not None:
            params['siteUrl'] = site_url
        if host_email is not None:
            params['hostEmail'] = host_email
        url = self.ep('trackingCodes')
        return [o async for o in self.session.follow_pagination(url=url, model=TrackingCode, params=params)]


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
        return Membership.model_validate(data)

    async def details(self, membership_id: str) -> Membership:
        """
        Get details for a membership by ID.
        Specify the membership ID in the membershipId URI parameter.

        :param membership_id: The unique identifier for the membership.
        :type membership_id: str
        """
        url = self.ep(f'{membership_id}')
        data = await super().get(url=url)
        return Membership.model_validate(data)

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
        data = update.model_dump_json(include={'is_moderator', 'is_room_hidden'})
        if update.id is None:
            raise ValueError('ID has to be set')
        url = self.ep(f'{update.id}')
        data = await super().put(url=url, data=data)
        return Membership.model_validate(data)

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
               text: str = None, markdown: str = None, html: str = None, files: List[str] = None,
               attachments: List[Union[dict, MessageAttachment]] = None) -> Message:
        """
        Post a plain text, rich text or html message, and optionally, a file attachment, to a room.

        The files parameter is an array, which accepts multiple values to allow for future expansion, but currently
        only one file may be included with the message. File previews are only rendered for attachments of 1MB or less.

        html formatting is limited to the following markup h1,h2,h3,ul,ol,u,i,b and links.

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
        :param html: The message, in HTML format. The maximum message length is 7439 bytes.
        :type html: str
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
        if html is not None:
            body['html'] = html
        if attachments is not None:
            body['attachments'] = [a.model_dump(by_alias=True) if isinstance(a, MessageAttachment) else a
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
        return Message.model_validate(data)

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
                * html: str: The message, in HTML format. The maximum message length is 7439 bytes.
        """
        data = message.model_dump_json(include={'room_id', 'text', 'markdown', 'html'})
        if not message.id:
            raise ValueError('ID has to be set')
        url = self.ep(f'{message.id}')
        data = await super().put(url=url, data=data)
        return Message.model_validate(data)

    async def details(self, message_id: str) -> Message:
        """
        Show details for a message, by message ID.
        Specify the message ID in the messageId parameter in the URI.

        :param message_id: The unique identifier for the message.
        :type message_id: str
        """
        url = self.ep(f'{message_id}')
        data = await super().get(url=url)
        return Message.model_validate(data)

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
    async def list(self, calling_data: bool = None) -> list[Organization]:
        """
        List all organizations visible by your account. The results will not be paginated.

        :param calling_data: Include XSI endpoint values in the response (if applicable) for the organization.
            Default: false
        :type calling_data: bool
        :return: list of Organizations
        """
        params = calling_data and {'callingData': 'true'} or None
        data = await self.get(url=self.ep(), params=params)
        return TypeAdapter(list[Organization]).validate_python(data['items'])

    async def details(self, org_id: str, calling_data: bool = None) -> Organization:
        """
        Get Organization Details

        Shows details for an organization, by ID.

        :param org_id: The unique identifier for the organization.
        :type org_id: str
        :param calling_data: Include XSI endpoint values in the response (if applicable) for the organization.
            Default: false
        :type calling_data: bool
        :return: org details
        :rtype: :class:`Organization`
        """
        url = self.ep(org_id)
        params = calling_data and {'callingData': 'true'} or None
        data = await self.get(url=url, params=params)
        return Organization.model_validate(data)

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
             roles: str = None, calling_data: bool = None, location_id: str = None,
             **params) -> AsyncGenerator[Person, None, None]:
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

        Lookup by roles is only supported for Admin users for the people within the same org.

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
        :param roles: List of roleIds separated by commas.
        :type roles: str
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
            if CALLING_DATA_TIMEOUT_PROTECTION:
                params['max'] = params.get('max', MAX_USERS_WITH_CALLING_DATA)
        id_list = params.pop('idList', None)
        if id_list:
            params['id'] = ','.join(id_list)
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Person, params=params)

    async def list(self, email: str = None, display_name: str = None, id_list: list[str] = None, org_id: str = None,
             roles: str = None, calling_data: bool = None, location_id: str = None,
             **params) -> List[Person]:
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

        Lookup by roles is only supported for Admin users for the people within the same org.

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
        :param roles: List of roleIds separated by commas.
        :type roles: str
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
            if CALLING_DATA_TIMEOUT_PROTECTION:
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
        data = settings.model_dump_json(exclude={'person_id': True,
                                                 'created': True,
                                                 'last_modified': True,
                                                 'timezone': True,
                                                 'last_activity': True,
                                                 'sip_addresses': True,
                                                 'status': True,
                                                 'invite_pending': True,
                                                 'login_enabled': True,
                                                 'person_type': True})
        return Person.model_validate(await self.post(url, data=data, params=params))

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
        return Person.model_validate(await self.get(ep, params=params))

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
        data = person.model_dump_json(exclude={'created': True,
                                               'last_modified': True,
                                               'timezone': True,
                                               'last_activity': True,
                                               'sip_addresses': True,
                                               'status': True,
                                               'invite_pending': True,
                                               'login_enabled': True,
                                               'person_type': True})
        ep = self.ep(path=person.person_id)
        return Person.model_validate(await self.put(url=ep, data=data, params=params))

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
        result = Person.model_validate(data)
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
        return QueueCallerId.model_validate(data)

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
        return AppServicesSettings.model_validate(data)

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
        data = settings.model_dump_json(include={'ring_devices_for_click_to_dial_calls_enabled': True,
                                                 'ring_devices_for_group_page_enabled': True,
                                                 'ring_devices_for_call_park_enabled': True,
                                                 'desktop_client_enabled': True,
                                                 'tablet_client_enabled': True,
                                                 'mobile_client_enabled': True,
                                                 'browser_client_enabled': True})
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
        return BargeSettings.model_validate(await self.get(ep, params=params))

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
        await self.put(ep, params=params, data=barge_settings.model_dump_json())


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
        return InterceptSetting.model_validate(await self.get(ep, params=params))

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
        data = json.loads(intercept.model_dump_json())
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
        else:
            must_close = False
            # an existing reader
            if not upload_as:
                raise ValueError('upload_as is required')
        encoder = MultipartEncoder({'file': (upload_as, content, 'audio/wav')})
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
        return CallRecordingSetting.model_validate(await self.get(ep, params=params))

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
        data = json.loads(recording.model_dump_json())
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
        return CallerId.model_validate(await self.get(ep, params=params))

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
        data = settings.model_dump_json(exclude_unset=True, include={'selected': True,
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
        return CallingBehavior.model_validate(data)

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
        data = settings.model_dump_json(exclude_none=False, exclude={'effective_behavior_type'}, exclude_unset=True)
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
        return DND.model_validate(await self.get(ep, params=params))

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
        await self.put(ep, params=params, data=dnd_settings.model_dump_json())


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
        h: _Helper = _Helper.model_validate(data)
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
        data = h.model_dump_json()
        await self.put(ep, params=params, data=data)


class AsHotelingApi(AsPersonSettingsApiChild):
    """
    API for person's hoteling settings
    """

    # TODO: this seems to be wrong. For workspace devices methods exist with complete coverage for all hoteling settings

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
        return IncomingPermissions.model_validate(await self.get(ep, params=params))

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
        await self.put(ep, params=params, data=settings.model_dump_json())


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
        return Monitoring.model_validate(data)

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

    async def read(self, person_id: str, prefer_e164_format: bool = None, org_id: str = None) -> PersonNumbers:
        """
        Get a person's phone numbers including alternate numbers.

        A person can have one or more phone numbers and/or extensions via which they can be called.

        This API requires a full or user administrator auth token with
        the spark-admin:people_read scope.

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param prefer_e164_format: Return phone numbers in E.164 format.
        :type prefer_e164_format: bool
        :param org_id: Person is in this organization. Only admin users of another organization (such as partners) may
            use this parameter as the default is the same organization as the token used to access API.
        :type org_id: str
        :return: Alternate numbers of the user
        :rtype: :class:`PersonNumbers`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if prefer_e164_format is not None:
            params['preferE164Format'] = str(prefer_e164_format).lower()
        ep = self.f_ep(person_id=person_id)
        return PersonNumbers.model_validate(await self.get(ep, params=params))

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
        body = update.model_dump_json()
        await self.put(url=url, params=params, data=body)


class AsAccessCodesApi(AsPersonSettingsApiChild):
    """
    API for workspace's outgoing permission access codes
    """
    feature = 'outgoingPermission/accessCodes'

    async def read(self, workspace_id: str, org_id: str = None) -> list[AuthCode]:
        """
        Retrieve Access codes for a Workspace.

        Access codes are used to bypass permissions.

        This API requires a full or read-only administrator auth token with a scope of spark-admin:workspaces_read or
        a user auth token with spark:workspaces_read scope can be used to read workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        :return: list of access codes
        :rtype: list of :class:`AuthCode`
        """
        url = self.f_ep(person_id=workspace_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.get(url, params=params)
        return TypeAdapter(list[AuthCode]).validate_python(data['accessCodes'])

    async def delete_codes(self, workspace_id: str, access_codes: list[Union[str, AuthCode]], org_id: str = None):
        """
        Modify Access codes for a workspace.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a
        user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param access_codes: authorization codes to remove
        :type access_codes: list[str]
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        """
        url = self.f_ep(person_id=workspace_id)
        params = org_id and {'orgId': org_id} or None
        body = {'deleteCodes': [ac.code if isinstance(ac, AuthCode) else ac
                                for ac in access_codes]}
        await self.put(url, params=params, json=body)

    async def create(self, workspace_id: str, code: str, description: str, org_id: str = None):
        """
        Create new Access codes for the given workspace.

        Access codes are used to bypass permissions.

        This API requires a full or user administrator auth token with the spark-admin:workspaces_write scope or a
        user auth token with spark:workspaces_write scope can be used to update workspace settings.

        :param workspace_id: Unique identifier for the workspace.
        :type workspace_id: str
        :param code: Indicates an access code.
        :type code: str
        :param description: Indicates the description of the access code.
        :type description: str
        :param org_id: ID of the organization within which the workspace resides. Only admin users of another
            organization (such as partners) may use this parameter as the default is the same organization as the token
            used to access API.
        :type org_id: str
        """
        url = self.f_ep(person_id=workspace_id)
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
        return AutoTransferNumbers.model_validate(data)

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
        body = settings.model_dump_json()
        await self.put(url, params=params, data=body)


class AsOutgoingPermissionsApi(AsPersonSettingsApiChild):
    """
    API for person's outgoing permissions settings

    also used for workspace and location outgoing permissions
    """
    #: Only available for workspaces and locations
    transfer_numbers: AsTransferNumbersApi
    #: Only available for workspaces
    access_codes: AsAccessCodesApi

    feature = 'outgoingPermission'

    def __init__(self, *, session: AsRestSession,
                 workspaces: bool = False, locations: bool = False):
        super().__init__(session=session, workspaces=workspaces, locations=locations)
        if workspaces:
            # auto transfer numbers API seems to only exist for workspaces
            self.transfer_numbers = AsTransferNumbersApi(session=session,
                                                       workspaces=True)
            self.access_codes = AsAccessCodesApi(session=session, workspaces=True)
        elif locations:
            self.transfer_numbers = AsTransferNumbersApi(session=session,
                                                       locations=True)
            self.access_codes = None
        else:
            self.transfer_numbers = None
            self.access_codes = None

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
        return OutgoingPermissions.model_validate(await self.get(ep, params=params))

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
        await self.put(ep, params=params, data=settings.model_dump_json(drop_call_types=drop_call_types))


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
        return PersonForwardingSetting.model_validate(await self.get(ep, params=params))

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
        data = forwarding.model_dump_json(
            exclude={'call_forwarding':
                         {'no_answer':
                              {'system_max_number_of_rings': True}}})
        await self.put(ep, params=params, data=data)


class AsPreferredAnswerApi(AsApiChild, base='telephony/config/people'):

    # noinspection PyMethodOverriding
    def ep(self, person_id: str) -> str:
        """
        :meta private:
        """
        return super().ep(f'{person_id}/preferredAnswerEndpoint')

    async def read(self, person_id: str, org_id: str = None) -> PreferredAnswerResponse:
        """
        Get Preferred Answer Endpoint
        Get the person's preferred answer endpoint (if any) and the list of endpoints available for selection. These
        endpoints can be used by the following Call Control API's that allow the person to specify an endpointId to
        use for the call:

        /v1/telephony/calls/dial

        /v1/telephony/calls/retrieve

        /v1/telephony/calls/pickup

        /v1/telephony/calls/barge-in

        /v1/telephony/calls/answer

        This API requires spark:telephony_config_read or spark-admin:telephony_config_read scope.

        :param person_id: A unique identifier for the person.
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access
            API.
        :return: person's preferred answer endpoint settings
        :rtype: PreferredAnswerResponse
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep(person_id=person_id)
        return PreferredAnswerResponse.model_validate(await self.get(ep, params=params))

    async def modify(self, person_id: str, preferred_answer_endpoint_id: str, org_id: str = None):
        """
        Modify Preferred Answer Endpoint
        Sets or clears the person’s preferred answer endpoint. To clear the preferred answer endpoint the p
        preferred_answer_endpoint_id parameter must be set to None.
        This API requires spark:telephony_config_write or spark-admin:telephony_config_write scope.

        :param person_id: A unique identifier for the person.
        :param preferred_answer_endpoint_id: Person’s preferred answer endpoint.
        :param org_id: ID of the organization in which the person resides. Only admin users of another organization
            (such as partners) may use this parameter as the default is the same organization as the token used to
            access
            API.
        """
        params = org_id and {'orgId': org_id} or None
        ep = self.ep(person_id=person_id)
        await self.put(ep, params=params, json={'preferredAnswerEndpointId': preferred_answer_endpoint_id})


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
        return Privacy.model_validate(data)

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
        data = json.loads(settings.model_dump_json())
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
        return PushToTalkSettings.model_validate(await self.get(ep, params=params))

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
            body_settings = settings.model_copy(deep=True)
            members = [m.member_id if isinstance(m, MonitoredMember) else m
                       for m in settings.members]
            body_settings.members = members
        else:
            body_settings = settings
        body = body_settings.model_dump_json(exclude_none=False,
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
        return ReceptionistSettings.model_validate(data)

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
        data = json.loads(settings.model_dump_json())
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
        result = Schedule.model_validate(data)
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
        result = Event.model_validate(data)
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
        data = event.model_dump_json(exclude={'event_id'})
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
        event_data = event.model_dump_json(exclude={'event_id'})
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
        return VoicemailSettings.model_validate(await self.get(url, params=params))

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
        data = settings.model_dump_json(exclude={'send_busy_calls': {'greeting_uploaded': True},
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
        encoder = MultipartEncoder({'file': (upload_as, content, 'audio/wav')})
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
    #: Preferred answer endpoint settings
    preferred_answer: AsPreferredAnswerApi
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
        self.preferred_answer = AsPreferredAnswerApi(session=session)
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
        return PersonDevicesResponse.model_validate(data)


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
        result = TypeAdapter(list[ReportTemplate]).validate_python(data['items'])
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
        result = Report.model_validate(data['items'][0])
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
        return RoomTab.model_validate(data)

    async def tab_details(self, tab_id: str) -> RoomTab:
        """
        Get details for a Room Tab with the specified room tab ID.

        :param tab_id: The unique identifier for the Room Tab.
        :type tab_id: str
        """
        url = self.ep(f'{tab_id}')
        data = await super().get(url=url)
        return RoomTab.model_validate(data)

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
        return RoomTab.model_validate(data)

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
            params['type'] = enum_str(type_)
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
            params['type'] = enum_str(type_)
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
        Bots are not able to create and simultaneously classify a room. A bot may update a space classification after
        a person of the same owning organization joined the space as the first human user.

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
        return Room.model_validate(data)

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
        return Room.model_validate(data)

    async def meeting_details(self, room_id: str) -> GetRoomMeetingDetailsResponse:
        """
        Shows Webex meeting details for a room such as the SIP address, meeting URL, toll-free and toll dial-in numbers.
        Specify the room ID in the roomId parameter in the URI.

        :param room_id: The unique identifier for the room.
        :type room_id: str
        """
        url = self.ep(f'{room_id}/meetingInfo')
        data = await super().get(url=url)
        return GetRoomMeetingDetailsResponse.model_validate(data)

    async def update(self, update: Room) -> Room:
        """
        Updates details for a room, by ID.

        Specify the room ID in the roomId parameter in the URI.

        A space can only be put into announcement mode when it is locked.

        Any space participant or compliance officer can convert a space from public to private. Only a compliance
        officer can convert a space from private to public and only if the space is classified with the lowest
        category (usually public), and the space has a description.

        To remove a description please use a space character   by itself.

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
        data = update.model_dump_json(include={'title', 'classification_id', 'team_id', 'is_locked',
                                               'is_announcement_only', 'is_read_only'})
        if update.id is None:
            raise ValueError('ID has to be set')
        url = self.ep(f'{update.id}')
        data = await super().put(url=url, data=data)
        return Room.model_validate(data)

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
        return TeamMembership.model_validate(data)

    async def details(self, membership_id: str) -> TeamMembership:
        """
        Shows details for a team membership, by ID.
        Specify the team membership ID in the membershipId URI parameter.

        :param membership_id: The unique identifier for the team membership.
        :type membership_id: str
        """
        url = self.ep(f'{membership_id}')
        data = await super().get(url=url)
        return TeamMembership.model_validate(data)

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
        return TeamMembership.model_validate(data)

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
        return Team.model_validate(data)

    async def details(self, team_id: str) -> Team:
        """
        Shows details for a team, by ID.
        Specify the team ID in the teamId parameter in the URI.

        :param team_id: The unique identifier for the team.
        :type team_id: str
        """
        url = self.ep(f'{team_id}')
        data = await super().get(url=url)
        return Team.model_validate(data)

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
        return Team.model_validate(data)

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


class AsAnnouncementsRepositoryApi(AsApiChild, base='telephony/config'):
    """
    Not supported for Webex for Government (FedRAMP)

    Features: Announcement Repository support reading and writing of Webex Calling Announcement Repository settings for
    a specific organization.

    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    spark-admin:telephony_config_read.
    Modifying these organization settings requires a full administrator auth token with a scope
    of spark-admin:telephony_config_write.

    A partner administrator can retrieve or change settings in a customer's organization using the optional orgId query
    parameter.
    """

    def list_gen(self, location_id: str = None, order: str = None, file_name: str = None, file_type: str = None,
             media_file_type: str = None, name: str = None, org_id: str = None,
             **params) -> AsyncGenerator[RepoAnnouncement, None, None]:
        """
        Fetch a list of binary announcement greetings at an organization as well as location level.
        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return the list of enterprise or Location announcement files. Without this parameter, the
            Enterprise level announcements are returned. Possible values: all, locations,
            Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
        :type location_id: str
        :param order: Sort the list according to fileName or fileSize. The default sort will be in Ascending order.
        :type order: str
        :param file_name: Return the list of announcements with the given fileName.
        :type file_name: str
        :param file_type: Return the list of announcement files for this fileType.
        :type file_type: str
        :param media_file_type: Return the list of announcement files for this mediaFileType.
        :type media_file_type: str
        :param name: Return the list of announcement files for this announcement label.
        :type name: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str
        :return: yields :class:`RepoAnnouncement` objects

        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if order is not None:
            params['order'] = order
        if file_name is not None:
            params['fileName'] = file_name
        if file_type is not None:
            params['fileType'] = file_type
        if media_file_type is not None:
            params['mediaFileType'] = media_file_type
        if name is not None:
            params['name'] = name
        url = self.ep('announcements')
        return self.session.follow_pagination(url=url, model=RepoAnnouncement, item_key='announcements',
                                              params=params)

    async def list(self, location_id: str = None, order: str = None, file_name: str = None, file_type: str = None,
             media_file_type: str = None, name: str = None, org_id: str = None,
             **params) -> List[RepoAnnouncement]:
        """
        Fetch a list of binary announcement greetings at an organization as well as location level.
        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Return the list of enterprise or Location announcement files. Without this parameter, the
            Enterprise level announcements are returned. Possible values: all, locations,
            Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzMxMTYx
        :type location_id: str
        :param order: Sort the list according to fileName or fileSize. The default sort will be in Ascending order.
        :type order: str
        :param file_name: Return the list of announcements with the given fileName.
        :type file_name: str
        :param file_type: Return the list of announcement files for this fileType.
        :type file_type: str
        :param media_file_type: Return the list of announcement files for this mediaFileType.
        :type media_file_type: str
        :param name: Return the list of announcement files for this announcement label.
        :type name: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str
        :return: yields :class:`RepoAnnouncement` objects

        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if order is not None:
            params['order'] = order
        if file_name is not None:
            params['fileName'] = file_name
        if file_type is not None:
            params['fileType'] = file_type
        if media_file_type is not None:
            params['mediaFileType'] = media_file_type
        if name is not None:
            params['name'] = name
        url = self.ep('announcements')
        return [o async for o in self.session.follow_pagination(url=url, model=RepoAnnouncement, item_key='announcements',
                                              params=params)]

    async def _upload_or_modify(self, *, url, name, file, upload_as, params, is_upload) -> dict:
        if isinstance(file, str):
            upload_as = upload_as or os.path.basename(file)
            file = open(file, mode='rb')
            must_close = True
        else:
            must_close = False
            # an existing reader
            if not upload_as:
                raise ValueError('upload_as is required')
        encoder = MultipartEncoder({'name': name, 'file': (upload_as, file, 'audio/wav')})
        if is_upload:
            meth = super().post
        else:
            meth = super().put
        try:
            data = await meth(url, data=encoder, headers={'Content-Type': encoder.content_type},
                        params=params)
        finally:
            if must_close:
                file.close()
        return data
        

    async def upload_announcement(self, name: str, file: Union[BufferedReader, str], upload_as: str = None,
                            location_id: str = None,
                            org_id: str = None) -> str:
        params = org_id and {'orgId': org_id} or None
        if location_id is None:
            url = self.ep('announcements')
        else:
            url = self.ep(f'locations/{location_id}/announcements')
        data = await self._upload_or_modify(url=url, name=name, file=file, upload_as=upload_as, params=params,
                                      is_upload=True)
        return data["id"]

        

    async def usage(self, location_id: str = None, org_id: str = None) -> RepositoryUsage:
        """
        Retrieves repository usage for announcements for an organization.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Unique identifier of a location
        :type location_id: str
        :param org_id: Create an announcement in this organization.
        :type org_id: str

        """
        params = org_id and {'orgId': org_id} or None
        if location_id is None:
            url = self.ep('announcements/usage')
        else:
            url = self.ep(f'locations/{location_id}/announcements/usage')
        data = await super().get(url=url, params=params)
        return RepositoryUsage.model_validate(data)

    async def details(self, announcement_id: str, location_id: str = None, org_id: str = None) -> RepoAnnouncement:
        """
        Fetch details of a binary announcement greeting by its ID at an organization level.
        An admin can upload a file at an organization level. This file will be uploaded to the announcement repository.
        This API requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        :param location_id: Unique identifier of a location
        :type location_id: str
        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param org_id: Get details of an announcement in this organization.
        :type org_id: str

        """
        params = org_id and {'orgId': org_id} or None
        if location_id is None:
            url = self.ep(f'announcements/{announcement_id}')
        else:
            url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        data = await super().get(url=url, params=params)
        return RepoAnnouncement.model_validate(data)

    async def delete(self, announcement_id: str, location_id: str = None, org_id: str = None):
        """
        Delete an announcement greeting.
        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.

        :param announcement_id: Unique identifier of an announcement.
        :type announcement_id: str
        :param location_id: Unique identifier of a location where announcement is being deleted.
        :type location_id: str
        :param org_id: Delete an announcement in this organization.
        :type org_id: str

        """
        params = org_id and {'orgId': org_id} or None

        if location_id is None:
            url = self.ep(f'announcements/{announcement_id}')
        else:
            url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        await super().delete(url=url, params=params)

    async def modify(self, announcement_id: str, name: str, file: Union[BufferedReader, str],
               upload_as: str = None, location_id: str = None, org_id: str = None):
        params = org_id and {'orgId': org_id} or None
        if location_id is None:
            url = self.ep(f'announcements/{announcement_id}')
        else:
            url = self.ep(f'locations/{location_id}/announcements/{announcement_id}')
        data = await self._upload_or_modify(url=url, name=name, file=file, upload_as=upload_as, params=params,
                                      is_upload=False)
        return data["id"]

        


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
        result = CallForwarding.model_validate(data['callForwarding'])
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

        body = {'callForwarding': json.loads(forwarding.model_dump_json(exclude={'rules': {'__all__': {'calls_from',
                                                                                                       'forward_to',
                                                                                                       'calls_to',
                                                                                                       'name'}}}))}
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
        params = org_id and {'orgId': org_id} or None
        body = forwarding_rule.model_dump_json()
        data = await self._session.rest_post(url=url, data=body, params=params)
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
        result = ForwardingRuleDetails.model_validate(data)
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
        body = forwarding_rule.model_dump_json(exclude={'id'})
        data = await self._session.rest_put(url=url, params=params, data=body)
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
        await self._session.rest_delete(url=url, params=params)


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
        return AutoAttendant.model_validate(await self.get(url, params=params))

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
        return CallPark.model_validate(await self.get(url, params=params))

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
        return LocationCallParkSettings.model_validate(await self.get(url, params=params))

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
        return CallPickup.model_validate(await self.get(url, params=params))

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
        return HolidayService.model_validate(data)

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
        body = update.model_dump_json(exclude={'holiday_schedules'})
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
        return NightService.model_validate(data)

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
        body = update.model_dump_json(exclude={'business_hours_schedules'})
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
        return StrandedCalls.model_validate(data)

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
        await self._session.rest_put(url=url, params=params, data=update.model_dump_json())

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
        return ForcedForward.model_validate(data)

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
        await self._session.rest_put(url=url, params=params, data=update.model_dump_json())


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

        :meta private:
        :param queue:
        :return:
        """
        return queue.model_dump_json(
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
        result = CallQueue.model_validate(data)
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
        return CallParkExtension.model_validate(data)

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
        return DialResponse.model_validate(data)

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
        return ParkedAgainst.model_validate(data)

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
        return CallInfo.model_validate(data)

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
        return CallInfo.model_validate(data)

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
        return CallInfo.model_validate(data)

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
        return TelephonyCall.model_validate(data)

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
        result = HuntGroup.model_validate(data)
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
        data = await super().post(url=url, data=body.model_dump_json())
        return NumberJob.model_validate(data)

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
        return NumberJob.model_validate(data)

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
        return InterceptSetting.model_validate(await self.get(ep, params=params))

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
        data = settings.model_dump_json()
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
        return OrganisationVoicemailSettings.model_validate(await self.get(url, params=params))

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
        data = settings.model_dump_json()
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
        return Paging.model_validate(await self.get(url, params=params))

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
        return CreateResponse.model_validate(data)

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
        dp: DialPlan = DialPlan.model_validate(data)
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
        body = update.model_dump_json(include={'name', 'route_id', 'route_type'})
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

        body = Body(dial_patterns=dial_patterns).model_dump_json()
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
        body = route_group.model_dump_json(include={'name': True,
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
        return RouteGroup.model_validate(data)

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
        body = update.model_dump_json(include={'name': True,
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
        return RouteGroupUsage.model_validate(data)

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
        return RouteListDetail.model_validate(data)

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

        body = Body(numbers=numbers).model_dump_json()
        data = await self.put(url=url, params=params, data=body)
        if data:
            return TypeAdapter(list[UpdateNumbersResponse]).validate_python(data['numberStatus'])
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
        return TrunkDetail.model_validate(data)

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
        return TypeAdapter(list[TrunkTypeWithDeviceType]).validate_python(data['trunkTypes'])

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
        return TrunkUsage.model_validate(data)

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
        return DialPatternValidationResult.model_validate(data)


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
        return TypeAdapter(NetworkConnectionType).validate_python(data['networkConnectionType'])

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
        return DeviceMembersResponse.model_validate(data)

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
                member = member.model_copy(deep=True)
            members_for_update.append(member)

        if members_for_update:
            # now assign port indices
            port = 1
            for member in members_for_update:
                member.port = port
                port += member.line_weight

        # create body
        if members_for_update:
            members = ','.join(m.model_dump_json(include={'member_id', 'port', 't38_fax_compression_enabled',
                                                          'primary_owner', 'line_type', 'line_weight', 'line_label',
                                                          'hotline_enabled', 'hotline_destination',
                                                          'allow_call_decline_enabled'})
                               for m in members_for_update)
            body = f'{{"members": [{members}]}}'
        else:
            body = None

        url = self.ep(f'{device_id}/members')
        params = org_id and {'orgId': org_id} or None
        await self.put(url=url, data=body, params=params)

    def available_members_gen(self, device_id: str, location_id: str = None, member_name: str = None,
                          phone_number: str = None, extension: str = None, org_id: str = None,
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

    async def available_members(self, device_id: str, location_id: str = None, member_name: str = None,
                          phone_number: str = None, extension: str = None, org_id: str = None,
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
        return DeviceCustomization.model_validate(data)

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
        body = customization.model_dump_json(include={'customizations', 'custom_enabled'})
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
        return TypeAdapter(list[DectDevice]).validate_python(data['devices'])

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
        return MACValidationResponse.model_validate(data)


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
        return InternalDialing.model_validate(data)

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
        data = update.model_dump_json(exclude_none=False)
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
        return LocationMoHSetting.model_validate(data)

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
        data = settings.model_dump_json()
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
        body = {'accessCodes': [json.loads(ac.model_dump_json()) for ac in access_codes]}
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
        return LocationVoiceMailSettings.model_validate(data)

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
        body = settings.model_dump_json()
        await self.put(url, params=params, data=body)


class AsReceptionistContactsDirectoryApi(AsApiChild, base='telephony/config/locations'):
    """
    Webex Calling Location Receptionist Contacts supports creation of directories and assigning custom groups of
    users to directories for a location within an organization.

    Receptionist Contact Directories are named custom groups of users.

    Viewing these read-only directories requires a full or read-only administrator auth token with a scope of
    spark-admin:telephony_config_read, as the current set of APIs is designed to provide supplemental information for
    administrators utilizing People Webex Calling APIs.

    Modifying these directories requires a full administrator auth token with a scope
    of spark-admin:telephony_config_write.

    A partner administrator can retrieve or change settings in a customer's organization using the optional OrgId
    query parameter.

    """

    # TODO: create test cases
    # TODO: really no details call and no way to update a directory?

    def _url(self, location_id: str):
        return self.ep(f'{location_id}/receptionistContacts/directories')

    async def create(self, location_id: str, name: str, contacts: list[str], org_id: str = None) -> str:
        """
        Creates a new Receptionist Contact Directory for a location.

        Receptionist Contact Directories can be used to create named directories of users.

        Adding a directory requires a full or write-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Add a Receptionist Contact Directory to this location.
        :type location_id: str
        :param name: Receptionist Contact Directory name.
        :type name: str
        :param contacts: Array of user or workspace ids assigned to this Receptionist Contact Directory
        :type contacts: list[str]
        :param org_id: Add a Receptionist Contact Directory to this organization.
        :type org_id: str
        :return: Receptionist Contact Directory ID.
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        body = {'name': name,
                'contacts': [{'personId': contact} for contact in contacts]}
        data = await self.post(url=url, params=params, json=body)
        return data['id']

    def list_gen(self, location_id: str, org_id: str = None) -> AsyncGenerator[IdAndName, None, None]:
        """
        List all Receptionist Contact Directories for a location.

        Receptionist Contact Directories can be used to create named directories of users.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: List Receptionist Contact Directories for this location.
        :type location_id: str
        :param org_id: List Receptionist Contact Directories for this organization.
        :type org_id: str
        :return: Yields IdAndName instances
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        return self.session.follow_pagination(url=url, model=IdAndName, params=params, item_key='directories')

    async def list(self, location_id: str, org_id: str = None) -> List[IdAndName]:
        """
        List all Receptionist Contact Directories for a location.

        Receptionist Contact Directories can be used to create named directories of users.

        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param location_id: List Receptionist Contact Directories for this location.
        :type location_id: str
        :param org_id: List Receptionist Contact Directories for this organization.
        :type org_id: str
        :return: Yields IdAndName instances
        """
        url = self._url(location_id)
        params = org_id and {'orgId': org_id} or None
        return [o async for o in self.session.follow_pagination(url=url, model=IdAndName, params=params, item_key='directories')]

    async def delete(self, location_id: str, directory_id: str, org_id: str = None):
        """
        Delete a Receptionist Contact Directory from a location.

        Receptionist Contact Directories can be used to create named directories of users.

        Deleting a directory requires a full or write-only administrator auth token with a scope
        of spark-admin:telephony_config_write.

        :param location_id: Delete a Receptionist Contact Directory from this location.
        :param directory_id: ID of directory to delete.
        :param org_id: Delete a Receptionist Contact Directory from this organization.
        """
        url = f'{self._url(location_id)}/{directory_id}'
        params = org_id and {'orgId': org_id} or None
        await super().delete(url=url, params=params)


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
    #: Receptionist contacts directories
    receptionist_contacts_directory: AsReceptionistContactsDirectoryApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.intercept = AsLocationInterceptApi(session=session)
        self.internal_dialing = AsInternalDialingApi(session=session)
        self.moh = AsLocationMoHApi(session=session)
        self.number = AsLocationNumbersApi(session=session)
        self.voicemail = AsLocationVoicemailSettingsApi(session=session)
        self.receptionist_contacts_directory = AsReceptionistContactsDirectoryApi(session=session)

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
        return ValidateExtensionsResponse.model_validate(data)

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
        return TelephonyLocation.model_validate(data)

    async def enable_for_calling(self, location: Location, org_id: str = None) -> str:
        """
        Enable a location by adding it to Webex Calling. This add Webex Calling support to a location created
        using the POST /v1/locations API.

        Locations are used to support calling features which can be defined at the location level.

        This API requires a full administrator auth token with a scope of spark-admin:telephony_config_write.
        :return: A unique identifier for the location.
        :rtype: str
        """
        params = org_id and {'orgId': org_id}
        url = self.ep()
        body = location.model_dump_json()
        data = await self.post(url=url, data=body, params=params)
        return data['id']

    def list_gen(self, name: str = None, order: str = None, org_id: str = None) -> AsyncGenerator[TelephonyLocation, None, None]:
        """
        Lists Webex Calling locations for an organization with Webex Calling details.

        Searching and viewing locations with Webex Calling details in your organization require an administrator auth
        token with the spark-admin:telephony_config_read scope.
        :param name: List locations whose name contains this string.
        :type name: str
        :param order: Sort the list of locations based on name, either asc or desc.
        :type order: str
        :param org_id: List locations for this organization.
        :type org_id: str
        :return: generator of :class:`TelephonyLocation` instances
        """
        params = {to_camel(k): v
                  for k, v in locals().items()
                  if k != 'self' and v is not None}
        url = self.ep()
        return self.session.follow_pagination(url=url, model=TelephonyLocation, params=params, item_key='locations')

    async def list(self, name: str = None, order: str = None, org_id: str = None) -> List[TelephonyLocation]:
        """
        Lists Webex Calling locations for an organization with Webex Calling details.

        Searching and viewing locations with Webex Calling details in your organization require an administrator auth
        token with the spark-admin:telephony_config_read scope.
        :param name: List locations whose name contains this string.
        :type name: str
        :param order: Sort the list of locations based on name, either asc or desc.
        :type order: str
        :param org_id: List locations for this organization.
        :type org_id: str
        :return: generator of :class:`TelephonyLocation` instances
        """
        params = {to_camel(k): v
                  for k, v in locals().items()
                  if k != 'self' and v is not None}
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=TelephonyLocation, params=params, item_key='locations')]

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
        data = settings.model_dump_json(exclude={'location_id', 'name', 'user_limit', 'default_domain',
                                                 'subscription_status', 'e911_setup_required'})
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
        return DeviceCustomization.model_validate(data)


class AsVirtualLinesApi(AsApiChild, base='telephony/config/virtualLines'):
    def list_gen(self, org_id: str = None, location_id: list[str] = None,
             id: list[str] = None, owner_name: list[str] = None, phone_number: list[str] = None,
             location_name: list[str] = None, order: list[str] = None, has_device_assigned: bool = None,
             has_extension_assigned: bool = None, has_dn_assigned: bool = None,
             **params) -> AsyncGenerator[VirtualLine, None, None]:
        """
        List all Virtual Lines for the organization.
        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.
        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List virtual lines for this organization.
        :type org_id: str
        :param location_id: Return the list of virtual lines matching these location ids. Example for multiple values -
            ?locationId=locId1&locationId=locId2.
        :type location_id: List[str]
        :param id: Return the list of virtual lines matching these virtualLineIds.
        :type id: List[str]
        :param owner_name: Return the list of virtual lines matching these owner names.
        :type owner_name: List[str]
        :param phone_number: Return the list of virtual lines matching these phone numbers.
        :type phone_number: List[str]
        :param location_name: Return the list of virtual lines matching the location names.
        :type location_name: List[str]
        :param order: Return the list of virtual lines based on the order. Default sort will be in an Ascending order.
            Maximum 3 orders allowed at a time.
        :type order: List[str]
        :param has_device_assigned: If true, includes only virtual lines with devices assigned. When not explicitly
            specified, the default includes both virtual lines with devices assigned and not assigned.
        :type has_device_assigned: bool
        :param has_extension_assigned: If true, includes only virtual lines with an extension assigned. When not
            explicitly specified, the default includes both virtual lines with extension assigned and not assigned.
        :type has_extension_assigned: bool
        :param has_dn_assigned: If true, includes only virtual lines with an assigned directory number, also known as a
            Dn. When not explicitly specified, the default includes both virtual lines with a Dn assigned and not
            assigned.
        :type has_dn_assigned: bool
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if id is not None:
            params['id'] = id
        if owner_name is not None:
            params['ownerName'] = owner_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if location_name is not None:
            params['locationName'] = location_name
        if order is not None:
            params['order'] = order
        if has_device_assigned is not None:
            params['hasDeviceAssigned'] = has_device_assigned
        if has_extension_assigned is not None:
            params['hasExtensionAssigned'] = has_extension_assigned
        if has_dn_assigned is not None:
            params['hasDnAssigned'] = has_dn_assigned
        url = self.ep()
        return self.session.follow_pagination(url=url, model=VirtualLine, params=params, item_key='virtualLines')

    async def list(self, org_id: str = None, location_id: list[str] = None,
             id: list[str] = None, owner_name: list[str] = None, phone_number: list[str] = None,
             location_name: list[str] = None, order: list[str] = None, has_device_assigned: bool = None,
             has_extension_assigned: bool = None, has_dn_assigned: bool = None,
             **params) -> List[VirtualLine]:
        """
        List all Virtual Lines for the organization.
        Virtual line is a capability in Webex Calling that allows administrators to configure multiple lines to Webex
        Calling users.
        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

        :param org_id: List virtual lines for this organization.
        :type org_id: str
        :param location_id: Return the list of virtual lines matching these location ids. Example for multiple values -
            ?locationId=locId1&locationId=locId2.
        :type location_id: List[str]
        :param id: Return the list of virtual lines matching these virtualLineIds.
        :type id: List[str]
        :param owner_name: Return the list of virtual lines matching these owner names.
        :type owner_name: List[str]
        :param phone_number: Return the list of virtual lines matching these phone numbers.
        :type phone_number: List[str]
        :param location_name: Return the list of virtual lines matching the location names.
        :type location_name: List[str]
        :param order: Return the list of virtual lines based on the order. Default sort will be in an Ascending order.
            Maximum 3 orders allowed at a time.
        :type order: List[str]
        :param has_device_assigned: If true, includes only virtual lines with devices assigned. When not explicitly
            specified, the default includes both virtual lines with devices assigned and not assigned.
        :type has_device_assigned: bool
        :param has_extension_assigned: If true, includes only virtual lines with an extension assigned. When not
            explicitly specified, the default includes both virtual lines with extension assigned and not assigned.
        :type has_extension_assigned: bool
        :param has_dn_assigned: If true, includes only virtual lines with an assigned directory number, also known as a
            Dn. When not explicitly specified, the default includes both virtual lines with a Dn assigned and not
            assigned.
        :type has_dn_assigned: bool
        """
        if org_id is not None:
            params['orgId'] = org_id
        if location_id is not None:
            params['locationId'] = location_id
        if id is not None:
            params['id'] = id
        if owner_name is not None:
            params['ownerName'] = owner_name
        if phone_number is not None:
            params['phoneNumber'] = phone_number
        if location_name is not None:
            params['locationName'] = location_name
        if order is not None:
            params['order'] = order
        if has_device_assigned is not None:
            params['hasDeviceAssigned'] = has_device_assigned
        if has_extension_assigned is not None:
            params['hasExtensionAssigned'] = has_extension_assigned
        if has_dn_assigned is not None:
            params['hasDnAssigned'] = has_dn_assigned
        url = self.ep()
        return [o async for o in self.session.follow_pagination(url=url, model=VirtualLine, params=params, item_key='virtualLines')]


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
        return MessageSummary.model_validate(data)

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
        return VoicePortalSettings.model_validate(await self.get(url, params=params))

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
        data = json.loads(settings.model_dump_json(exclude={'portal_id': True,
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
        return PasscodeRules.model_validate(await self.get(url, params=params))


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
        return VoicemailGroupDetail.model_validate(data)

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
        return VoiceMailRules.model_validate(await self.get(url, params=params))

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
        data = settings.model_dump_json(exclude={'default_voicemail_pin_rules': True})
        await self.put(url, params=params, data=data)


class AsTelephonyApi(AsApiChild, base='telephony/config'):
    """
    The telephony settings (features) API.
    """
    #: access or authentication codes
    access_codes: AsAccessCodesApi
    announcements_repo: AsAnnouncementsRepositoryApi
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
    locations: AsTelephonyLocationApi
    #: organisation voicemail settings
    organisation_voicemail: AsOrganisationVoicemailSettingsAPI
    paging: AsPagingApi
    permissions_out: AsOutgoingPermissionsApi
    pickup: AsCallPickupApi
    prem_pstn: AsPremisePstnApi
    pnc: AsPrivateNetworkConnectApi
    schedules: AsScheduleApi
    virtual_lines: AsVirtualLinesApi
    # location voicemail groups
    voicemail_groups: AsVoicemailGroupsApi
    voicemail_rules: AsVoicemailRulesApi
    voice_messaging: AsVoiceMessagingApi
    voiceportal: AsVoicePortalApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.access_codes = AsAccessCodesApi(session=session)
        self.announcements_repo = AsAnnouncementsRepositoryApi(session=session)
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
        self.locations = self.location
        self.organisation_voicemail = AsOrganisationVoicemailSettingsAPI(session=session)
        self.paging = AsPagingApi(session=session)
        self.permissions_out = AsOutgoingPermissionsApi(session=session, locations=True)
        self.pickup = AsCallPickupApi(session=session)
        self.pnc = AsPrivateNetworkConnectApi(session=session)
        self.prem_pstn = AsPremisePstnApi(session=session)
        self.schedules = AsScheduleApi(session=session, base=ScheduleApiBase.locations)
        self.virtual_lines = AsVirtualLinesApi(session=session)
        self.voicemail_groups = AsVoicemailGroupsApi(session=session)
        self.voicemail_rules = AsVoicemailRulesApi(session=session)
        self.voice_messaging = AsVoiceMessagingApi(session=session)
        self.voiceportal = AsVoicePortalApi(session=session)

    def phone_numbers_gen(self, location_id: str = None, phone_number: str = None, available: bool = None,
                      order: str = None,
                      owner_name: str = None, owner_id: str = None, owner_type: OwnerType = None,
                      extension: str = None, number_type: NumberType = None,
                      phone_number_type: NumberListPhoneNumberType = None,
                      state: NumberState = None, details: bool = None, toll_free_numbers: bool = None,
                      restricted_non_geo_numbers: bool = None,
                      org_id: str = None, **params) -> AsyncGenerator[NumberListPhoneNumber, None, None]:
        """
        Get Phone Numbers for an Organization with given criteria.

        List all the phone numbers for the given organization along with the status and owner (if any).

        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.
        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

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
        :param details: Returns the overall count of the PSTN phone numbers along with other details for given
            organization.
        :type details: bool
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
        :param restricted_non_geo_numbers: Returns the list of restricted non geographical numbers.
        :type restricted_non_geo_numbers: bool
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
                      state: NumberState = None, details: bool = None, toll_free_numbers: bool = None,
                      restricted_non_geo_numbers: bool = None,
                      org_id: str = None, **params) -> List[NumberListPhoneNumber]:
        """
        Get Phone Numbers for an Organization with given criteria.

        List all the phone numbers for the given organization along with the status and owner (if any).

        PSTN phone numbers are associated with a specific location and can be active/inactive and assigned/unassigned.
        The owner is the person, workspace, or feature to which the number is assigned.
        Retrieving this list requires a full or read-only administrator auth token with a scope
        of spark-admin:telephony_config_read.

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
        :param details: Returns the overall count of the PSTN phone numbers along with other details for given
            organization.
        :type details: bool
        :param toll_free_numbers: Returns the list of toll free phone numbers.
        :type toll_free_numbers: bool
        :param restricted_non_geo_numbers: Returns the list of restricted non geographical numbers.
        :type restricted_non_geo_numbers: bool
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
        return NumberDetails.model_validate(data['count'])

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
        return ValidateExtensionsResponse.model_validate(data)

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
        return ValidatePhoneNumbersResponse.model_validate(data)

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
        return TypeAdapter(list[UCMProfile]).validate_python(data['callingProfiles'])

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
        return TestCallRoutingResult.model_validate(data)

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
        return TypeAdapter(list[SupportedDevice]).validate_python(data['devices'])

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
        return DeviceCustomization.model_validate(data)

    async def read_list_of_announcement_languages(self) -> list[AnnouncementLanguage]:
        """
        List all languages supported by Webex Calling for announcements and voice prompts.
        Retrieving announcement languages requires a full or read-only administrator auth token with a scope of
        spark-admin:telephony_config_read.

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/read-the-list-of-announcement-languages
        """
        url = self.ep('announcementLanguages')
        data = await super().get(url=url)
        return TypeAdapter(list[AnnouncementLanguage]).validate_python(data["languages"])


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
        body = json.loads(WebhookCreate(**params).model_dump_json())
        ep = self.ep()
        data = await self.post(ep, json=body)
        result = Webhook.model_validate(data)
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
        return Webhook.model_validate(await self.get(url))

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
        webhook_data = update.model_dump_json(include={'name', 'target_url', 'secret', 'owned_by', 'status'})
        return Webhook.model_validate(await self.put(url, data=webhook_data))

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
        return WorkspaceLocationFloor.model_validate(data)

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
        return WorkspaceLocationFloor.model_validate(data)

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
        data = settings.model_dump_json(exclude_none=True, exclude_unset=True, exclude={'id', 'location_id'})
        url = self.ep(location_id=location_id, floor_id=floor_id)
        params = org_id and {'orgId': org_id} or None
        data = await self.put(url=url, data=data, params=params)
        return WorkspaceLocationFloor.model_validate(data)

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
        return WorkspaceLocation.model_validate(data)

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
        return WorkspaceLocation.model_validate(data)

    async def update(self, location_id: str, settings: WorkspaceLocation, org_id: str = None) -> WorkspaceLocation:
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
        body = settings.model_dump_json(exclude_none=True, exclude_unset=True, exclude={'id'})
        data = await self.put(url=url, data=body, params=params)
        return WorkspaceLocation.model_validate(data)

    async def delete(self, location_id: str, org_id: str = None):
        """
        Delete a Workspace Location
        Deletes a location, by ID. The workspaces associated to that location will no longer have a location, but a new
        location can be reassigned to them.
        """
        params = org_id and {'orgId': org_id} or None
        url = self.ep(location_id=location_id)
        await super().delete(url=url, params=params)


class AsWorkspaceDevicesApi(AsApiChild, base='telephony/config/workspaces'):
    def list_gen(self, workspace_id: str, org_id: str = None) -> AsyncGenerator[TelephonyDevice, None, None]:
        """
        Get all devices for a workspace.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param workspace_id: ID of the workspace for which to retrieve devices.
        :type workspace_id: str
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-workspace-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/devices')
        return self.session.follow_pagination(url=url, model=TelephonyDevice, params=params, item_key='devices')

    async def list(self, workspace_id: str, org_id: str = None) -> List[TelephonyDevice]:
        """
        Get all devices for a workspace.
        This requires a full or read-only administrator auth token with a scope of spark-admin:telephony_config_read.

        :param workspace_id: ID of the workspace for which to retrieve devices.
        :type workspace_id: str
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/get-workspace-devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/devices')
        return [o async for o in self.session.follow_pagination(url=url, model=TelephonyDevice, params=params, item_key='devices')]

    async def modify_hoteling(self, workspace_id: str, hoteling: Hoteling, org_id: str = None):
        """
        Modify devices for a workspace.
        Modifying devices for a workspace requires a full administrator auth token with a scope of
        spark-admin:telephony_config_write.

        :param workspace_id: ID of the workspace for which to modify devices.
        :type workspace_id: str
        :param hoteling: hoteling settings
        :type hoteling: Hoteling
        :param org_id: Organization to which the workspace belongs.
        :type org_id: str

        documentation: https://developer.webex.com/docs/api/v1/webex-calling-organization-settings/modify-workspace
        -devices
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'{workspace_id}/devices')
        await super().put(url=url, params=params, data=hoteling.model_dump_json())


class AsWorkspaceNumbersApi(AsApiChild, base='workspaces'):

    # noinspection PyMethodOverriding
    def ep(self, workspace_id: str, path: str = None):
        """

        :meta private:
        """
        path = path and '/path' or ''
        return super().ep(path=f'{workspace_id}/features/numbers/{path}')

    async def read(self, workspace_id: str, org_id: str = None) -> WorkspaceNumbers:
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
        :rtype: WorkspaceNumbers
        """
        params = org_id and {'org_id': org_id} or None
        url = self.ep(workspace_id=workspace_id)
        data = await self.get(url=url, params=params)
        return TypeAdapter(WorkspaceNumbers).validate_python(data)


@dataclass(init=False)
class AsWorkspaceSettingsApi(AsApiChild, base='workspaces'):
    """
    API for all workspace settings.

    Most of the workspace settings are equivalent to corresponding user settings. For these settings the attributes of
    this class are instances of the respective user settings APIs. When calling endpoints of these APIs workspace IDs
    need to be passed to the ``person_id`` parameter of the called function.
    """
    forwarding: AsPersonForwardingApi
    call_waiting: AsCallWaitingApi
    caller_id: AsCallerIdApi
    monitoring: AsMonitoringApi
    numbers: AsWorkspaceNumbersApi
    permissions_in: AsIncomingPermissionsApi
    permissions_out: AsOutgoingPermissionsApi
    devices: AsWorkspaceDevicesApi
    call_intercept: AsCallInterceptApi

    def __init__(self, session: AsRestSession):
        super().__init__(session=session)
        self.forwarding = AsPersonForwardingApi(session=session, workspaces=True)
        self.call_waiting = AsCallWaitingApi(session=session, workspaces=True)
        self.caller_id = AsCallerIdApi(session=session, workspaces=True)
        self.monitoring = AsMonitoringApi(session=session, workspaces=True)
        self.numbers = AsWorkspaceNumbersApi(session=session)
        self.permissions_in = AsIncomingPermissionsApi(session=session, workspaces=True)
        self.permissions_out = AsOutgoingPermissionsApi(session=session, workspaces=True)
        self.devices = AsWorkspaceDevicesApi(session=session)
        self.call_intercept = AsCallInterceptApi(session=session, workspaces=True)


class AsWorkspacesApi(AsApiChild, base='workspaces'):
    """
    Workspaces API

    Workspaces represent where people work, such as conference rooms, meeting spaces, lobbies, and lunch rooms. Devices
    may be associated with workspaces.
    Viewing the list of workspaces in an organization requires an administrator auth token with the
    spark-admin:workspaces_read scope. Adding, updating, or deleting workspaces in an organization requires an
    administrator auth token with the spark-admin:workspaces_write scope.
    The Workspaces API can also be used by partner administrators acting as administrators of a different organization
    than their own. In those cases an orgId value must be supplied, as indicated in the reference documentation for the
    relevant endpoints.
    """

    def list_gen(self, workspace_location_id: str = None, floor_id: str = None, display_name: str = None,
             capacity: int = None,
             workspace_type: WorkSpaceType = None, calling: CallingType = None,
             supported_devices: WorkspaceSupportedDevices = None, calendar: CalendarType = None,
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
        :param workspace_type: List workspaces by type. Possible values: notSet, focus, huddle, meetingRoom, open,
            desk, other
        :type workspace_type: :class:`WorkSpaceType`
        :param calling: List workspaces by calling type. Possible values: freeCalling, hybridCalling, webexCalling,
            webexEdgeForDevices, thirdPartySipCalling, none
        :type calling: :class:`CallingType`
        :param supported_devices: List workspaces by supported devices. Possible values: collaborationDevices, phones
        :type supported_devices: str

        :param calendar: List workspaces by calendar type. Possible values: none, google, microsoft
        :type calendar: :class:`CalendarType`
        :param org_id: List workspaces in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: generator of :class:`Workspace` instances
        """
        params.update((to_camel(k), enum_str(v))
                      for k, v in locals().items()
                      if k not in {'self', 'params', 'enum_str'} and v is not None)
        if workspace_type is not None:
            params.pop('workspaceType')
            params['type'] = workspace_type
        ep = self.ep()
        # noinspection PyTypeChecker
        return self.session.follow_pagination(url=ep, model=Workspace, params=params)

    async def list(self, workspace_location_id: str = None, floor_id: str = None, display_name: str = None,
             capacity: int = None,
             workspace_type: WorkSpaceType = None, calling: CallingType = None,
             supported_devices: WorkspaceSupportedDevices = None, calendar: CalendarType = None,
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
        :param workspace_type: List workspaces by type. Possible values: notSet, focus, huddle, meetingRoom, open,
            desk, other
        :type workspace_type: :class:`WorkSpaceType`
        :param calling: List workspaces by calling type. Possible values: freeCalling, hybridCalling, webexCalling,
            webexEdgeForDevices, thirdPartySipCalling, none
        :type calling: :class:`CallingType`
        :param supported_devices: List workspaces by supported devices. Possible values: collaborationDevices, phones
        :type supported_devices: str

        :param calendar: List workspaces by calendar type. Possible values: none, google, microsoft
        :type calendar: :class:`CalendarType`
        :param org_id: List workspaces in this organization. Only admin users of another organization
            (such as partners) may use this parameter.
        :type org_id: str
        :return: generator of :class:`Workspace` instances
        """
        params.update((to_camel(k), enum_str(v))
                      for k, v in locals().items()
                      if k not in {'self', 'params', 'enum_str'} and v is not None)
        if workspace_type is not None:
            params.pop('workspaceType')
            params['type'] = workspace_type
        ep = self.ep()
        # noinspection PyTypeChecker
        return [o async for o in self.session.follow_pagination(url=ep, model=Workspace, params=params)]

    async def create(self, settings: Workspace, org_id: str = None):
        """
        Create a Workspace

        The workspaceLocationId, floorId, capacity, type, notes and hotdeskingStatus parameters are optional,
        and omitting them will result in the creation of a workspace without these values set, or set to their
        default. A workspaceLocationId must be provided when the floorId is set. Calendar and calling can also be set
        for a new workspace. Omitting them will default to free calling and no calendaring. The orgId parameter can
        only be used by admin users of another organization (such as partners).

        Information for Webex Calling fields may be found here: locations and available numbers.

        The locationId and supportedDevices fields cannot be changed once configured.

        When creating a webexCalling workspace, a locationId and either a phoneNumber or extension or both is required.

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
        return Workspace.model_validate(data)

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
        return Workspace.model_validate(await self.get(url))

    async def update(self, workspace_id, settings: Workspace) -> Workspace:
        """
        Updates details for a workspace by ID.

        Specify the workspace ID in the workspaceId parameter in the URI. Include all details for the workspace that
        are present in a GET request for the workspace details. Not including the optional capacity, type or notes
        fields will result in the fields no longer being defined for the workspace. A workspaceLocationId must be
        provided when the floorId is set. The workspaceLocationId, floorId, supportedDevices, calendar and calling
        fields do not change when omitted from the update request.

        Information for Webex Calling fields may be found here: locations and available numbers.

        Updating the calling parameter is only supported if the existing calling type is freeCalling, none,
        thirdPartySipCalling or webexCalling.

        Updating the calling parameter to none, thirdPartySipCalling or webexCalling is not supported if the
        workspace contains any devices.

        The locationId and supportedDevices fields cannot be changed once configured.

        When updating webexCalling information, a locationId and either a phoneNumber or extension or both is required.

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
        return Workspace.model_validate(data)

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

    async def capabilities(self, workspace_id: str) -> CapabilityMap:
        """
        Shows the capabilities for a workspace by ID.
        Returns a set of capabilities, including whether or not the capability is supported by any device in the
        workspace, and if the capability is configured (enabled). For example for a specific capability like
        occupancyDetection, the API will return if the capability is supported and/or configured such that occupancy
        detection data will flow from the workspace (device) to the cloud. Specify the workspace ID in the workspaceId
        parameter in the URI.

        :param workspace_id: A unique identifier for the workspace.
        :type workspace_id: str

        """
        url = self.ep(f'{workspace_id}/capabilities')
        data = await super().get(url=url)
        return CapabilityMap.model_validate(data["capabilities"])


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
    #: meetings API :class:`AsMeetingsApi`
    meetings: AsMeetingsApi
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

    def __init__(self, *, tokens: Union[str, Tokens] = None, concurrent_requests: int = 10, retry_429: bool = True):
        """

        :param tokens: token to be used by the API. Can be a :class:`tokens.Tokens` instance, a string or None. If
            None then an access token is expected in the WEBEX_ACCESS_TOKEN environment variable.
        :param concurrent_requests: number of concurrent requests when using multi-threading
        :type concurrent_requests: int
        :param retry_429: automatically retry for 429 throttling response
        :type retry_429: bool
        """
        if isinstance(tokens, str):
            tokens = Tokens(access_token=tokens)
        elif tokens is None:
            tokens = os.getenv('WEBEX_ACCESS_TOKEN')
            if tokens is None:
                raise ValueError('if no access token is passed, then a valid access token has to be present in '
                                 'WEBEX_ACCESS_TOKEN environment variable')
            tokens = Tokens(access_token=tokens)

        session = AsRestSession(tokens=tokens, concurrent_requests=concurrent_requests, retry_429=retry_429)
        self.attachment_actions = AsAttachmentActionsApi(session=session)
        self.cdr = AsDetailedCDRApi(session=session)
        self.devices = AsDevicesApi(session=session)
        self.events = AsEventsApi(session=session)
        self.groups = AsGroupsApi(session=session)
        self.licenses = AsLicensesApi(session=session)
        self.locations = AsLocationsApi(session=session)
        self.meetings = AsMeetingsApi(session=session)
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
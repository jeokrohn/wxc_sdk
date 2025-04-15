from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['CallRecordingJobStatus', 'CallRecordingLocationVendorsResponse', 'CallRecordingVendorUsersResponse',
           'CallRecordingVendors', 'CallRecordingVendorsList', 'CountObject', 'ErrorMessageObject', 'ErrorObject',
           'FailureBehavior', 'FeaturesCallRecordingApi', 'GetCallRecordingObject',
           'GetCallRecordingObjectOrganization', 'GetCallRecordingTermsOfServiceObject',
           'GetComplianceAnnouncementObject', 'GetOrgComplianceAnnouncementObject', 'ItemObject',
           'JobExecutionStatusObject', 'LatestExecutionStatus', 'MemberType', 'Members', 'Regions',
           'StepExecutionStatusesObject', 'UserLicenseType', 'Vendor']


class GetCallRecordingObjectOrganization(ApiModel):
    #: A unique identifier for the organization.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9lNTEzMTg1Zi01YTJmLTQ0OTUtYjM1Yi03MDY3YmY3Y2U0OGU
    id: Optional[str] = None
    #: A unique name for the organization.
    #: example: Alaska Cisco Organization
    name: Optional[str] = None


class GetCallRecordingObject(ApiModel):
    #: Details of the organization.
    organization: Optional[GetCallRecordingObjectOrganization] = None
    #: Whether or not the call recording is enabled.
    #: example: True
    enabled: Optional[bool] = None
    #: A unique identifier for the vendor.
    #: example: Y2lzY29zcGFyazovL3VzL1JFQ09SRElOR19WRU5ET1IvNTNkYzRjODctODQwOC00ODgyLTk1NzAtZGNhMmJjZGI5Mjgw
    vendor_id: Optional[str] = None
    #: A unique name for the vendor.
    #: example: Dubber
    vendor_name: Optional[str] = None
    #: Url where can be found terms of service for the vendor.
    #: 
    #: **NOTE**: This is expected to be empty for webex recording platform.
    #: example: https://www.dubber.net/terms
    terms_of_service_url: Optional[str] = None


class GetCallRecordingTermsOfServiceObject(ApiModel):
    #: A unique identifier for the vendor.
    #: example: Y2lzY29zcGFyazovL3VzL1JFQ09SRElOR19WRU5ET1IvNTNkYzRjODctODQwOC00ODgyLTk1NzAtZGNhMmJjZGI5Mjgw
    vendor_id: Optional[str] = None
    #: A unique name for the vendor.
    #: example: Dubber
    vendor_name: Optional[str] = None
    #: Whether or not the call recording terms of service are enabled.
    #: example: True
    terms_of_service_enabled: Optional[bool] = None
    #: Url where can be found terms of service for the vendor.
    #: 
    #: **NOTE**: This is expected to be empty for webex recording platform.
    #: example: https://www.dubber.net/terms
    terms_of_service_url: Optional[str] = None


class GetComplianceAnnouncementObject(ApiModel):
    #: Flag to indicate whether the call recording START/STOP announcement is played to an inbound caller.
    #: example: True
    inbound_pstncalls_enabled: Optional[bool] = Field(alias='inboundPSTNCallsEnabled', default=None)
    #: Flag to indicate whether to use the customer level compliance announcement default settings.
    #: example: True
    use_org_settings_enabled: Optional[bool] = None
    #: Flag to indicate whether the call recording START/STOP announcement is played to an outbound caller.
    outbound_pstncalls_enabled: Optional[bool] = Field(alias='outboundPSTNCallsEnabled', default=None)
    #: Flag to indicate whether compliance announcement is played after a specified delay in seconds.
    outbound_pstncalls_delay_enabled: Optional[bool] = Field(alias='outboundPSTNCallsDelayEnabled', default=None)
    #: Number of seconds to wait before playing the compliance announcement.
    #: example: 10
    delay_in_seconds: Optional[int] = None


class GetOrgComplianceAnnouncementObject(ApiModel):
    #: Flag to indicate whether the call recording START/STOP announcement is played to an inbound caller.
    #: example: True
    inbound_pstncalls_enabled: Optional[bool] = Field(alias='inboundPSTNCallsEnabled', default=None)
    #: Flag to indicate whether the call recording START/STOP announcement is played to an outbound caller.
    outbound_pstncalls_enabled: Optional[bool] = Field(alias='outboundPSTNCallsEnabled', default=None)
    #: Flag to indicate whether compliance announcement is played after a specified delay in seconds.
    outbound_pstncalls_delay_enabled: Optional[bool] = Field(alias='outboundPSTNCallsDelayEnabled', default=None)
    #: Number of seconds to wait before playing the compliance announcement.
    #: example: 10
    delay_in_seconds: Optional[int] = None


class Regions(ApiModel):
    #: Two character region code.
    #: example: US
    code: Optional[str] = None
    #: Name of the region.
    #: example: United States
    name: Optional[str] = None
    #: Enabled by default.
    default_enabled: Optional[bool] = None


class MemberType(str, Enum):
    #: Member is a person.
    people = 'PEOPLE'
    #: Member is a workspace.
    place = 'PLACE'
    #: Member is a virtual line.
    virtual_line = 'VIRTUAL_LINE'


class UserLicenseType(str, Enum):
    #: License type is webex calling standard user.
    basic_user = 'BASIC_USER'
    #: License type is webex calling professional user.
    professional_user = 'PROFESSIONAL_USER'
    #: License type is webex calling common area workspace.
    workspace = 'WORKSPACE'
    #: License type is webex calling professional workspace.
    professional_workspace = 'PROFESSIONAL_WORKSPACE'
    #: License type is webex calling virtual profile.
    virtual_profile = 'VIRTUAL_PROFILE'


class Members(ApiModel):
    #: Unique identifier of the member.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1BMQUNFL2U2OTczZDgyLWM1NTUtNDMwOC05NGU3LWI3ZWU2MjczY2YyMg
    id: Optional[str] = None
    #: Last name of the member.
    #: example: jones
    last_name: Optional[str] = None
    #: First name of the member.
    #: example: Vickor
    first_name: Optional[str] = None
    #: Type of member.
    #: example: PEOPLE
    type: Optional[MemberType] = None
    #: License type of the member.
    #: example: PROFESSIONAL_USER
    license_type: Optional[UserLicenseType] = None


class CallRecordingVendorUsersResponse(ApiModel):
    #: Call recording vendor ID.
    #: example: Y2lzY29zcGFyazovL3VzL1JFQ09SRElOR19WRU5ET1IvMGE0MjY3NTQtYTQ3MC00YzJkLThiYTAtZmJjNjc3M2E4YTdj
    vendor_id: Optional[str] = None
    #: Contains member details
    members: Optional[list[Members]] = None


class FailureBehavior(str, Enum):
    #: Failure behavior will make sure that the call proceeds without announcement.
    proceed_with_call_no_announcement = 'PROCEED_WITH_CALL_NO_ANNOUNCEMENT'
    #: Failure behavior will make sure that the call proceeds with an announcement.
    proceed_call_with_announcement = 'PROCEED_CALL_WITH_ANNOUNCEMENT'
    #: Failure behavior will make sure that the call ends with an announcement.
    end_call_with_announcement = 'END_CALL_WITH_ANNOUNCEMENT'


class Vendor(ApiModel):
    #: Unique identifier of a vendor.
    #: example: Y2lzY29zcGFyazovL3VzL1JFQ09SRElOR19WRU5ET1IvZmVjYjYzNGUtYzMyZS00ZWJmLThlYzMtMmVhYjk3Y2IyNjNk
    id: Optional[str] = None
    #: Name of a call recording vendor.
    #: example: Dubber
    name: Optional[str] = None
    #: Describing some vendor info.
    #: example: This is the Dubber instance for the US region.
    description: Optional[str] = None
    #: Users can be migrated.
    #: example: True
    migrate_user_creation_enabled: Optional[bool] = None
    #: Login URL of the vendor.
    #: example: https://wxc-us.dubber.net/login?sso=webex
    login_url: Optional[str] = None
    #: URL to vendor's terms of service.
    #: example: https://www.dubber.net/terms
    terms_of_service_url: Optional[str] = None


class CallRecordingLocationVendorsResponse(ApiModel):
    #: Default call recording is enabled.
    #: example: True
    org_default_enabled: Optional[bool] = None
    #: Unique identifier of a vendor.
    #: example: Y2lzY29zcGFyazovL3VzL1JFQ09SRElOR19WRU5ET1IvMGE0MjY3NTQtYTQ3MC00YzJkLThiYTAtZmJjNjc3M2E4YTdj
    org_default_vendor_id: Optional[str] = None
    #: Name of the call recording vendor.
    #: example: Webex
    org_default_vendor_name: Optional[str] = None
    #: Unique identifier of a vendor.
    #: example: Y2lzY29zcGFyazovL3VzL1JFQ09SRElOR19WRU5ET1IvMGE0MjY3NTQtYTQ3MC00YzJkLThiYTAtZmJjNjc3M2E4YTdj
    default_vendor_id: Optional[str] = None
    #: Name of the call recording vendor.
    #: example: Webex
    default_vendor_name: Optional[str] = None
    #: List of available vendors and their details.
    vendors: Optional[list[Vendor]] = None
    #: Region-based storage is enabled.
    #: example: True
    org_storage_region_enabled: Optional[bool] = None
    #: Org level two character Region code.
    #: example: US
    org_storage_region: Optional[str] = None
    #: Location level character Region code.
    #: example: US
    storage_region: Optional[str] = None
    #: Failure behavior is enabled.
    #: example: True
    org_failure_behavior_enabled: Optional[bool] = None
    #: Type of org-level failure behavior.
    #: example: PROCEED_WITH_CALL_NO_ANNOUNCEMENT
    org_failure_behavior: Optional[FailureBehavior] = None
    #: Type of location level failure behavior.
    #: example: PROCEED_WITH_CALL_NO_ANNOUNCEMENT
    failure_behavior: Optional[FailureBehavior] = None


class StepExecutionStatusesObject(ApiModel):
    #: Unique identifier that identifies each step in a job.
    #: example: 1998857
    id: Optional[int] = None
    #: Step execution start time in UTC format.
    #: example: 2024-03-13T03:58:36.886Z
    start_time: Optional[datetime] = None
    #: Step execution end time in UTC format.
    #: example: 2024-03-13T03:58:48.471Z
    end_time: Optional[datetime] = None
    #: Last updated time for a step in UTC format.
    #: example: 2024-03-13T03:58:48.472Z
    last_updated: Optional[datetime] = None
    #: Displays the status of a step.
    #: example: COMPLETED
    status_message: Optional[str] = None
    #: Exit Code for a step.
    #: example: COMPLETED
    exit_code: Optional[str] = None
    #: Name of different steps the job goes through.
    #: example: managecallrecordingproviderGetUserThatNeedCallRecProviderUpdate
    name: Optional[str] = None
    #: Time lapsed since the step execution started.
    #: example: PT11.585S
    time_elapsed: Optional[str] = None


class JobExecutionStatusObject(ApiModel):
    #: Unique identifier that identifies each instance of the job.
    #: example: 436272
    id: Optional[int] = None
    #: Step execution start time in UTC format.
    #: example: 2024-03-13T14:57:04.678Z
    start_time: Optional[datetime] = None
    #: Step execution end time in UTC format.
    #: example: 2024-03-13T14:57:04.678Z
    end_time: Optional[datetime] = None
    #: Last updated time (in UTC format) post one of the step execution completion.
    #: example: 2024-03-13T14:57:04.678Z
    last_updated: Optional[datetime] = None
    #: Displays status for overall steps that are part of the job.
    #: example: STARTING
    status_message: Optional[str] = None
    #: Exit Code for a job.
    #: example: UNKNOWN
    exit_code: Optional[str] = None
    #: Job creation time in UTC format.
    #: example: 2024-03-13T14:57:04.678Z
    created_time: Optional[datetime] = None
    #: Time lapsed since the job execution started.
    #: example: PT0S
    time_elapsed: Optional[str] = None
    #: Status of each step within a job.
    step_execution_statuses: Optional[list[StepExecutionStatusesObject]] = None


class LatestExecutionStatus(str, Enum):
    #: Job has started.
    starting = 'STARTING'
    #: Job is in progress.
    started = 'STARTED'
    #: Job has been completed.
    completed = 'COMPLETED'
    #: Job has failed.
    failed = 'FAILED'


class CountObject(ApiModel):
    #: Total number of locations.
    total_number_of_locations: Optional[int] = None
    #: Total number of users.
    #: example: 6
    total_number_of_users: Optional[int] = None
    #: Failed number of users.
    failed_users: Optional[int] = None
    #: Updated number of users.
    #: example: 6
    updated_users: Optional[int] = None


class CallRecordingJobStatus(ApiModel):
    #: Name of the job.
    #: example: managecallrecordingprovider
    name: Optional[str] = None
    #: Unique identifier of the job.
    #: example: Y2lzY29zcGFyazovL3VzL0pPQl9JRC8wNjZkOTQzNC1kODEyLTQzODItODVhMC00MjBlOTFlODg3ZTY
    id: Optional[str] = None
    #: Unique identifier to track the flow of HTTP requests.
    #: example: ADMINBATCHCLIENT_a02c7b0c-4d28-4e98-b47b-0a135a4b287f_0
    tracking_id: Optional[str] = None
    #: Unique identifier of the user who has run the job.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODA2NzZhZC0yNjRlLTRmMWMtYmIwYS1jMWZiNmQ0ODlmZTI
    source_user_id: Optional[str] = None
    #: Unique identifier of the customer who has run the job.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNDEyODExZi0xMWI4LTQ2YTAtYWExNS1lZmEwMjRjODI5ODM
    source_customer_id: Optional[str] = None
    #: Unique identifier of the customer for which the job was run.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNDEyODExZi0xMWI4LTQ2YTAtYWExNS1lZmEwMjRjODI5ODM
    target_customer_id: Optional[str] = None
    #: Unique identifier to identify the instance of the job.
    #: example: 637210
    instance_id: Optional[int] = None
    #: Displays the most recent step's execution status. Contains execution statuses of all the steps involved in the
    #: execution of the job.
    job_execution_status: Optional[list[JobExecutionStatusObject]] = None
    #: Most recent status of the job at the time of invocation.
    #: example: COMPLETED
    latest_execution_status: Optional[LatestExecutionStatus] = None
    #: Unique identifier of a location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzlmZTFmZDllLTlkM2QtNDUxZi04MDEwLTMwY2U1ZjRlNTYyNQ
    location_id: Optional[str] = None
    #: Unique identifier of a vendor.
    #: example: Y2lzY29zcGFyazovL3VzL1JFQ09SRElOR19WRU5ET1IvZmYzNzMzOTYtMGVmMC00N2NiLTk5NzEtNzg0MDI5YzZjMTQ3
    vendor_id: Optional[str] = None
    #: Job statistics.
    counts: Optional[CountObject] = None


class ErrorMessageObject(ApiModel):
    #: Error message.
    #: example: POST failed: HTTP/1.1 404 Not Found
    description: Optional[str] = None
    code: Optional[str] = None
    #: Error messages describing the location ID in which the error occurs. For a move operation, this is the target
    #: location ID.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzlmZTFmZDllLTlkM2QtNDUxZi04MDEwLTMwY2U1ZjRlNTYyNQ
    location_id: Optional[str] = None


class ErrorObject(ApiModel):
    #: HTTP error code.
    #: example: 500
    key: Optional[str] = None
    #: Message string with further error information.
    message: Optional[list[ErrorMessageObject]] = None


class ItemObject(ApiModel):
    #: Index of error number.
    item_number: Optional[int] = None
    #: Unique identifier (UUID) of the error.
    #: example: 5d320be1-e28c-420a-8935-1a54c7826eb4
    item: Optional[str] = None
    #: Contains error details.
    error: Optional[ErrorObject] = None
    #: Unique tracking ID of the request.
    #: example: ADMINBATCHCLIENT_2830be24-766e-4a2a-be36-d289eb890322_0_3
    tracking_id: Optional[str] = None


class CallRecordingVendors(ApiModel):
    #: List of call recording vendors.
    items: Optional[list[Vendor]] = None


class CallRecordingVendorsList(ApiModel):
    #: Unique identifier of the vendor.
    vendor_id: Optional[str] = None
    #: Name of the vendor.
    vendor_name: Optional[str] = None
    #: List of call recording vendors
    vendors: Optional[CallRecordingVendors] = None
    #: Call recording storage region. Only applicable for Webex as a vendor and isn't used for other vendors.
    storage_region: Optional[str] = None
    #: Call recording failure behavior.
    failure_behavior: Optional[FailureBehavior] = None


class FeaturesCallRecordingApi(ApiChild, base='telephony/config'):
    """
    Features: Call Recording
    
    Not supported for Webex for Government (FedRAMP).
    
    
    
    Features: Call Recording supports reading and writing of Webex Calling Call Recording settings for a specific
    organization and also a location in an organization.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def get_call_recording_settings(self, org_id: str = None) -> GetCallRecordingObject:
        """
        Get Call Recording Settings

        Retrieve call recording settings for the organization.

        The Call Recording feature enables authorized agents to record any active call that Webex Contact Center
        manages.

        Retrieving call recording settings requires a full or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve call recording settings from this organization.
        :type org_id: str
        :rtype: :class:`GetCallRecordingObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording')
        data = super().get(url, params=params)
        r = GetCallRecordingObject.model_validate(data)
        return r

    def update_call_recording_settings(self, enabled: bool, org_id: str = None):
        """
        Update Call Recording Settings

        Update call recording settings for the organization.

        The Call Recording feature enables authorized agents to record any active call that Webex Contact Center
        manages.

        Updating call recording settings requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        **NOTE**: This API is for Cisco partners only.

        :param enabled: Whether or not the call recording is enabled.
        :type enabled: bool
        :param org_id: Retrieve call recording settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['enabled'] = enabled
        url = self.ep('callRecording')
        super().put(url, params=params, json=body)

    def get_call_recording_terms_of_service_settings(self, vendor_id: str,
                                                     org_id: str = None) -> GetCallRecordingTermsOfServiceObject:
        """
        Get Call Recording Terms Of Service Settings

        Retrieve call recording terms of service settings for the organization.

        The Call Recording feature enables authorized agents to record any active call that Webex Contact Center
        manages.

        Retrieving call recording terms of service settings requires a full or read-only administrator or location
        administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param vendor_id: Retrieve call recording terms of service details for the given vendor.
        :type vendor_id: str
        :param org_id: Retrieve call recording terms of service details from this organization.
        :type org_id: str
        :rtype: :class:`GetCallRecordingTermsOfServiceObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'callRecording/vendors/{vendor_id}/termsOfService')
        data = super().get(url, params=params)
        r = GetCallRecordingTermsOfServiceObject.model_validate(data)
        return r

    def update_call_recording_terms_of_service_settings(self, vendor_id: str, terms_of_service_enabled: bool,
                                                        org_id: str = None):
        """
        Update Call Recording Terms Of Service Settings

        Update call recording terms of service settings for the given vendor.

        The Call Recording feature enables authorized agents to record any active call that Webex Contact Center
        manages.

        Updating call recording terms of service settings requires a full administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param vendor_id: Update call recording terms of service settings for the given vendor.
        :type vendor_id: str
        :param terms_of_service_enabled: Whether or not the call recording terms of service are enabled.
        :type terms_of_service_enabled: bool
        :param org_id: Update call recording terms of service settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['termsOfServiceEnabled'] = terms_of_service_enabled
        url = self.ep(f'callRecording/vendors/{vendor_id}/termsOfService')
        super().put(url, params=params, json=body)

    def get_details_for_the_organization_compliance_announcement_setting(self,
                                                                         org_id: str = None) -> GetOrgComplianceAnnouncementObject:
        """
        Get details for the organization Compliance Announcement Setting

        Retrieve the organization compliance announcement settings.

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Retrieving organization compliance announcement setting requires a full or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve compliance announcement setting from this organization.
        :type org_id: str
        :rtype: :class:`GetOrgComplianceAnnouncementObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording/complianceAnnouncement')
        data = super().get(url, params=params)
        r = GetOrgComplianceAnnouncementObject.model_validate(data)
        return r

    def update_the_organization_compliance_announcement(self, inbound_pstncalls_enabled: bool = None,
                                                        outbound_pstncalls_enabled: bool = None,
                                                        outbound_pstncalls_delay_enabled: bool = None,
                                                        delay_in_seconds: int = None, org_id: str = None):
        """
        Update the organization compliance announcement.

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Updating the organization compliance announcement requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param inbound_pstncalls_enabled: Flag to indicate whether the call recording START/STOP announcement is played
            to an inbound caller.
        :type inbound_pstncalls_enabled: bool
        :param outbound_pstncalls_enabled: Flag to indicate whether the call recording START/STOP announcement is
            played to an outbound caller.
        :type outbound_pstncalls_enabled: bool
        :param outbound_pstncalls_delay_enabled: Flag to indicate whether compliance announcement is played after a
            specified delay in seconds.
        :type outbound_pstncalls_delay_enabled: bool
        :param delay_in_seconds: Number of seconds to wait before playing the compliance announcement.
        :type delay_in_seconds: int
        :param org_id: Update the compliance announcement setting from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if inbound_pstncalls_enabled is not None:
            body['inboundPSTNCallsEnabled'] = inbound_pstncalls_enabled
        if outbound_pstncalls_enabled is not None:
            body['outboundPSTNCallsEnabled'] = outbound_pstncalls_enabled
        if outbound_pstncalls_delay_enabled is not None:
            body['outboundPSTNCallsDelayEnabled'] = outbound_pstncalls_delay_enabled
        if delay_in_seconds is not None:
            body['delayInSeconds'] = delay_in_seconds
        url = self.ep('callRecording/complianceAnnouncement')
        super().put(url, params=params, json=body)

    def get_details_for_the_location_compliance_announcement_setting(self, location_id: str,
                                                                     org_id: str = None) -> GetComplianceAnnouncementObject:
        """
        Get details for the Location Compliance Announcement Setting

        Retrieve the location compliance announcement settings.

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Retrieving location compliance announcement setting requires a full or read-only administrator auth token with
        a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve compliance announcement settings for this location.
        :type location_id: str
        :param org_id: Retrieve compliance announcement setting from this organization.
        :type org_id: str
        :rtype: :class:`GetComplianceAnnouncementObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callRecording/complianceAnnouncement')
        data = super().get(url, params=params)
        r = GetComplianceAnnouncementObject.model_validate(data)
        return r

    def update_the_location_compliance_announcement(self, location_id: str, inbound_pstncalls_enabled: bool = None,
                                                    use_org_settings_enabled: bool = None,
                                                    outbound_pstncalls_enabled: bool = None,
                                                    outbound_pstncalls_delay_enabled: bool = None,
                                                    delay_in_seconds: int = None, org_id: str = None):
        """
        Update the location compliance announcement.

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Updating the location compliance announcement requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Update the compliance announcement settings for this location.
        :type location_id: str
        :param inbound_pstncalls_enabled: Flag to indicate whether the Call Recording START/STOP announcement is played
            to an inbound caller.
        :type inbound_pstncalls_enabled: bool
        :param use_org_settings_enabled: Flag to indicate whether to use the customer level compliance announcement
            default settings.
        :type use_org_settings_enabled: bool
        :param outbound_pstncalls_enabled: Flag to indicate whether the Call Recording START/STOP announcement is
            played to an outbound caller.
        :type outbound_pstncalls_enabled: bool
        :param outbound_pstncalls_delay_enabled: Flag to indicate whether compliance announcement is played after a
            specified delay in seconds.
        :type outbound_pstncalls_delay_enabled: bool
        :param delay_in_seconds: Number of seconds to wait before playing the compliance announcement.
        :type delay_in_seconds: int
        :param org_id: Update the compliance announcement setting from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if inbound_pstncalls_enabled is not None:
            body['inboundPSTNCallsEnabled'] = inbound_pstncalls_enabled
        if use_org_settings_enabled is not None:
            body['useOrgSettingsEnabled'] = use_org_settings_enabled
        if outbound_pstncalls_enabled is not None:
            body['outboundPSTNCallsEnabled'] = outbound_pstncalls_enabled
        if outbound_pstncalls_delay_enabled is not None:
            body['outboundPSTNCallsDelayEnabled'] = outbound_pstncalls_delay_enabled
        if delay_in_seconds is not None:
            body['delayInSeconds'] = delay_in_seconds
        url = self.ep(f'locations/{location_id}/callRecording/complianceAnnouncement')
        super().put(url, params=params, json=body)

    def get_call_recording_regions(self, org_id: str = None) -> list[Regions]:
        """
        Get Call Recording Regions

        Retrieve all the call recording regions that are available for an organization.

        The Call Recording feature supports multiple third-party call recording providers, or vendors, to capture and
        manage call recordings. An organization is configured with an overall provider, but locations can be
        configured to use a different vendor than the overall organization default.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve call recording regions for this organization.
        :type org_id: str
        :rtype: list[Regions]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording/regions')
        data = super().get(url, params=params)
        r = TypeAdapter(list[Regions]).validate_python(data['regions'])
        return r

    def get_call_recording_vendor_users(self, max_: int = None, start: int = None, standard_user_only: bool = None,
                                        org_id: str = None) -> CallRecordingVendorUsersResponse:
        """
        Get Call Recording Vendor Users

        Retrieve call recording vendor users of an organization. This API is used to get the list of users who are
        assigned to the default call-recording vendor of the organization.

        The Call Recording feature supports multiple third-party call recording providers, or vendors, to capture and
        manage call recordings. An organization is configured with an overall provider, but locations can be
        configured to use a different vendor than the overall organization default.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param max_: Limit the number of vendor users returned to this maximum count. The default is 2000.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching objects. The default is 0.
        :type start: int
        :param standard_user_only: If true, results only include Webex Calling standard users.
        :type standard_user_only: bool
        :param org_id: Retrieve call recording vendor users for this organization.
        :type org_id: str
        :rtype: :class:`CallRecordingVendorUsersResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if max_ is not None:
            params['max'] = max_
        if start is not None:
            params['start'] = start
        if standard_user_only is not None:
            params['standardUserOnly'] = str(standard_user_only).lower()
        url = self.ep('callRecording/vendorUsers')
        data = super().get(url, params=params)
        r = CallRecordingVendorUsersResponse.model_validate(data)
        return r

    def set_call_recording_vendor_for_a_location(self, location_id: str, id: str = None,
                                                 org_default_enabled: bool = None, storage_region: str = None,
                                                 org_storage_region_enabled: bool = None,
                                                 failure_behavior: FailureBehavior = None,
                                                 org_failure_behavior_enabled: bool = None,
                                                 org_id: str = None) -> str:
        """
        Set Call Recording Vendor for a Location

        Assign a call recording vendor to a location of an organization. Response will be `204` if the changes can be
        applied immediatley otherwise `200` with a job ID is returned.

        The Call Recording feature supports multiple third-party call recording providers, or vendors, to capture and
        manage call recordings. An organization is configured with an overall provider, but locations can be
        configured to use a different vendor than the overall organization default.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_write`.

        :param location_id: Update the call recording vendor for this location
        :type location_id: str
        :param id: Unique identifier of the call recording vendor.
        :type id: str
        :param org_default_enabled: Vendor is enabled by default.
        :type org_default_enabled: bool
        :param storage_region: Regions where call recordings are stored.
        :type storage_region: str
        :param org_storage_region_enabled: Region-based call recording storage is enabled.
        :type org_storage_region_enabled: bool
        :param failure_behavior: Type of failure behavior.
        :type failure_behavior: FailureBehavior
        :param org_failure_behavior_enabled: Failure behavior is enabled.
        :type org_failure_behavior_enabled: bool
        :param org_id: Update the call recording vendor for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if id is not None:
            body['id'] = id
        if org_default_enabled is not None:
            body['orgDefaultEnabled'] = org_default_enabled
        if storage_region is not None:
            body['storageRegion'] = storage_region
        if org_storage_region_enabled is not None:
            body['orgStorageRegionEnabled'] = org_storage_region_enabled
        if failure_behavior is not None:
            body['failureBehavior'] = enum_str(failure_behavior)
        if org_failure_behavior_enabled is not None:
            body['orgFailureBehaviorEnabled'] = org_failure_behavior_enabled
        url = self.ep(f'locations/{location_id}/callRecording/vendor')
        data = super().put(url, params=params, json=body)
        r = data['jobId']
        return r

    def get_location_call_recording_vendors(self, location_id: str,
                                            org_id: str = None) -> CallRecordingLocationVendorsResponse:
        """
        Get Location Call Recording Vendors

        Retrieve details of the call recording vendor that the location is assigned and also a list of vendors.

        The Call Recording feature supports multiple third-party call recording providers, or vendors, to capture and
        manage call recordings. An organization is configured with an overall provider, but locations can be
        configured to use a different vendor than the overall organization default.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve vendor details for this location.
        :type location_id: str
        :param org_id: Retrieve vendor details for this organization.
        :type org_id: str
        :rtype: :class:`CallRecordingLocationVendorsResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callRecording/vendors')
        data = super().get(url, params=params)
        r = CallRecordingLocationVendorsResponse.model_validate(data)
        return r

    def get_call_recording_vendor_users_for_a_location(self, location_id: str, max_: int = None, start: int = None,
                                                       standard_user_only: bool = None,
                                                       org_id: str = None) -> CallRecordingVendorUsersResponse:
        """
        Get Call Recording Vendor Users for a Location

        Retrieve call recording vendor users of a location. This API is used to get the list of users assigned to the
        call recording vendor of the location.

        The Call Recording feature supports multiple third-party call recording providers, or vendors, to capture and
        manage call recordings. An organization is configured with an overall provider, but locations can be
        configured to use a different vendor than the overall organization default.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param location_id: Retrieve vendor users for this location.
        :type location_id: str
        :param max_: Limit the number of vendor users returned to this maximum count. The default is 2000.
        :type max_: int
        :param start: Start at the zero-based offset in the list of matching objects. The default is 0.
        :type start: int
        :param standard_user_only: If true, results only include Webex Calling standard users.
        :type standard_user_only: bool
        :param org_id: Retrieve vendor users for this organization.
        :type org_id: str
        :rtype: :class:`CallRecordingVendorUsersResponse`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        if max_ is not None:
            params['max'] = max_
        if start is not None:
            params['start'] = start
        if standard_user_only is not None:
            params['standardUserOnly'] = str(standard_user_only).lower()
        url = self.ep(f'locations/{location_id}/callRecording/vendorUsers')
        data = super().get(url, params=params)
        r = CallRecordingVendorUsersResponse.model_validate(data)
        return r

    def list_call_recording_jobs(self, org_id: str = None, **params) -> Generator[CallRecordingJobStatus, None, None]:
        """
        List Call Recording Jobs

        Get the list of all call recording jobs in an organization.

        The Call Recording feature supports multiple third-party call recording providers, or vendors, to capture and
        manage call recordings. An organization is configured with an overall provider, but locations can be
        configured to use a different vendor than the overall organization default.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: List call recording jobs in this organization.
        :type org_id: str
        :return: Generator yielding :class:`CallRecordingJobStatus` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('jobs/callRecording')
        return self.session.follow_pagination(url=url, model=CallRecordingJobStatus, item_key='items', params=params)

    def get_the_job_status_of_a_call_recording_job(self, job_id: str, org_id: str = None) -> CallRecordingJobStatus:
        """
        Get the Job Status of a Call Recording Job

        Get the details of a call recording job by its job ID.

        The Call Recording feature supports multiple third-party call recording providers, or vendors, to capture and
        manage call recordings. An organization is configured with an overall provider, but locations can be
        configured to use a different vendor than the overall organization default.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job status for this `jobId`.
        :type job_id: str
        :param org_id: Retrieve job status in this organization.
        :type org_id: str
        :rtype: :class:`CallRecordingJobStatus`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/callRecording/{job_id}')
        data = super().get(url, params=params)
        r = CallRecordingJobStatus.model_validate(data)
        return r

    def get_job_errors_for_a_call_recording_job(self, job_id: str, org_id: str = None,
                                                **params) -> Generator[ItemObject, None, None]:
        """
        Get Job Errors for a Call Recording Job

        Get errors for a call recording job in an organization.

        The Call Recording feature supports multiple third-party call recording providers, or vendors, to capture and
        manage call recordings. An organization is configured with an overall provider, but locations can be
        configured to use a different vendor than the overall organization default.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param job_id: Retrieve job errors for this job.
        :type job_id: str
        :param org_id: Retrieve job errors for a call recording job in this organization.
        :type org_id: str
        :return: Generator yielding :class:`ItemObject` instances
        """
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'jobs/callRecording/{job_id}/errors')
        return self.session.follow_pagination(url=url, model=ItemObject, item_key='items', params=params)

    def get_organization_call_recording_vendors(self, org_id: str = None) -> CallRecordingVendorsList:
        """
        Get Organization Call Recording Vendors

        Returns what the current vendor is as well as a list of all the available vendors.

        The Call Recording feature supports multiple third-party call recording providers, or vendors, to capture and
        manage call recordings. An organization is configured with an overall provider, but locations can be
        configured to use a different vendor than the overall organization default.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve call recording settings from this organization.
        :type org_id: str
        :rtype: :class:`CallRecordingVendorsList`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording/vendors')
        data = super().get(url, params=params)
        r = CallRecordingVendorsList.model_validate(data)
        return r

    def set_organization_call_recording_vendor(self, vendor_id: str, storage_region: str = None,
                                               failure_behavior: FailureBehavior = None, org_id: str = None) -> str:
        """
        Set Organization Call Recording Vendor

        Returns a Job ID that you can use to get the status of the job.

        The Call Recording feature supports multiple third-party call recording providers, or vendors, to capture and
        manage call recordings. An organization is configured with an overall provider, but locations can be
        configured to use a different vendor than the overall organization default.

        Requires a full administrator auth token with a scope of `spark-admin:telephony_config_write`,
        `spark-admin:telephony_config_read`, and `spark-admin:people_write`.

        :param vendor_id: Unique identifier of the vendor.
        :type vendor_id: str
        :param storage_region: Call recording storage region. Only applicable for Webex as a vendor and isn't used for
            other vendors.
        :type storage_region: str
        :param failure_behavior: Call recording failure behavior.
        :type failure_behavior: FailureBehavior
        :param org_id: Modify call recording settings from this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['vendorId'] = vendor_id
        if storage_region is not None:
            body['storageRegion'] = storage_region
        if failure_behavior is not None:
            body['failureBehavior'] = enum_str(failure_behavior)
        url = self.ep('callRecording/vendor')
        data = super().put(url, params=params, json=body)
        r = data['jobId']
        return r

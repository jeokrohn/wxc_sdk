from collections.abc import Generator
from typing import Any, Optional

from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.common import AnnAudioFile, IdAndName, UserLicenseType, UserType
from wxc_sdk.person_settings.call_recording import BaseCallRecordingAnnouncement, CallRecordingAnnouncement

__all__ = [
    'CallRecordingInfo',
    'CallRecordingTermsOfService',
    'OrgComplianceAnnouncement',
    'LocationComplianceAnnouncement',
    'CallRecordingRegion',
    'RecordingUser',
    'FailureBehavior',
    'RecordingVendor',
    'CallRecordingVendors',
    'CallRecordingLocationVendors',
    'CallRecordingSettingsApi',
]


class CallRecordingInfo(ApiModel):
    #: Details of the organization.
    organization: Optional[IdAndName] = None
    #: Whether or not the call recording is enabled.
    enabled: Optional[bool] = None
    #: A unique identifier for the vendor.
    vendor_id: Optional[str] = None
    #: A unique name for the vendor.
    vendor_name: Optional[str] = None
    #: Url where can be found terms of service for the vendor.
    #:
    #: **NOTE**: This is expected to be empty for Webex Recording Platform.
    terms_of_service_url: Optional[str] = None


class CallRecordingTermsOfService(ApiModel):
    #: A unique identifier for the vendor.
    vendor_id: Optional[str] = None
    #: A unique name for the vendor.
    vendor_name: Optional[str] = None
    #: Whether or not the call recording terms of service are enabled.
    terms_of_service_enabled: Optional[bool] = None
    #: Url where can be found terms of service for the vendor.
    #:
    #: **NOTE**: This is expected to be empty for Webex Recording Platform.
    terms_of_service_url: Optional[str] = None


class BaseComplianceAnnouncement(ApiModel):
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an inbound caller.
    inbound_pstncalls_enabled: Optional[bool] = Field(alias='inboundPSTNCallsEnabled', default=None)
    #: Flag to indicate whether the Call Recording START/STOP announcement is played to an outbound caller.
    outbound_pstncalls_enabled: Optional[bool] = Field(alias='outboundPSTNCallsEnabled', default=None)
    #: Flag to indicate whether compliance announcement is played after a specified delay in seconds.
    outbound_pstncalls_delay_enabled: Optional[bool] = Field(alias='outboundPSTNCallsDelayEnabled', default=None)
    #: Number of seconds to wait before playing the compliance announcement.
    delay_in_seconds: Optional[int] = None


class OrgComplianceAnnouncement(BaseComplianceAnnouncement):
    #: Flag to indicate whether to use the custom compliance announcement. If true it uses the organization's custom
    #: compliance announcement file, and if false default compliance announcement used.
    use_custom_announcement_enabled: Optional[bool] = None
    #: The custom audio announcement file to be played.
    audio_announcement_file: Optional[AnnAudioFile] = None

    def update(self) -> dict[str, Any]:
        data = self.model_dump(mode='json', by_alias=True, exclude_none=True, exclude={'audio_announcement_file'})
        if self.use_custom_announcement_enabled:
            if (af := self.audio_announcement_file) is None or af.id is None:
                raise ValueError('audio announcement file id is required')
            data['audioAnnouncementFileId'] = af.id
        return data


class LocationComplianceAnnouncement(BaseComplianceAnnouncement):
    #: Flag to indicate whether to use the customer level compliance announcement default settings.
    use_org_settings_enabled: Optional[bool] = None
    #: Flag to indicate whether to use the organization level custom compliance announcement. If this flag is set to
    #: true, takes the organization's announcement setting. If this flag is set to false, takes the location's custom
    #: announcement.
    use_org_level_announcement_enabled: Optional[bool] = None
    #: Custom compliance announcement settings.
    custom_compliance_announcement: Optional[CallRecordingAnnouncement] = None

    def update(self) -> dict[str, Any]:
        """
        Data for update

        :meta private:
        """
        data = self.model_dump(mode='json', by_alias=True, exclude={'custom_compliance_announcement'})
        if (ola := self.use_org_level_announcement_enabled) is not None and not ola:
            if (
                (cca := self.custom_compliance_announcement) is None
                or (af := cca.audio_announcement_file) is None
                or af.id is None
            ):
                raise ValueError(
                    'custom compliance announcement is required and audio announcement file id is required'
                )
            data['customComplianceAnnouncement'] = {'type': cca.type, 'audioAnnouncementFileId': af.id}
        return data


class CallRecordingRegion(ApiModel):
    #: Two character region code.
    code: Optional[str] = None
    #: Name of the region.
    name: Optional[str] = None
    #: Enabled by default.
    default_enabled: Optional[bool] = None


class RecordingUser(ApiModel):
    #: Unique identifier of the member.
    id: Optional[str] = None
    #: Last name of the member.
    last_name: Optional[str] = None
    #: First name of the member.
    first_name: Optional[str] = None
    #: Type of member.
    type: Optional[UserType] = None
    #: License type of the member.
    license_type: Optional[UserLicenseType] = None


class FailureBehavior(str, Enum):
    #: Failure behavior will make sure that the call proceeds without announcement.
    proceed_with_call_no_announcement = 'PROCEED_WITH_CALL_NO_ANNOUNCEMENT'
    #: Failure behavior will make sure that the call proceeds with an announcement.
    proceed_call_with_announcement = 'PROCEED_CALL_WITH_ANNOUNCEMENT'
    #: Failure behavior will make sure that the call ends with an announcement.
    end_call_with_announcement = 'END_CALL_WITH_ANNOUNCEMENT'


class RecordingVendor(ApiModel):
    #: Unique identifier of a vendor.
    id: Optional[str] = None
    #: Name of a call recording vendor.
    name: Optional[str] = None
    #: Describing some vendor info.
    description: Optional[str] = None
    #: Users can be migrated.
    migrate_user_creation_enabled: Optional[bool] = None
    #: Login URL of the vendor.
    login_url: Optional[str] = None
    #: URL to vendor's terms of service.
    terms_of_service_url: Optional[str] = None


class CallRecordingVendors(ApiModel):
    #: Unique identifier of the vendor.
    vendor_id: Optional[str] = None
    #: Name of the vendor.
    vendor_name: Optional[str] = None
    #: List of call recording vendors
    vendors: Optional[list[RecordingVendor]] = None
    #: Call recording storage region. Only applicable for Webex as a vendor and isn't used for other vendors.
    storage_region: Optional[str] = None
    #: Call recording failure behavior.
    failure_behavior: Optional[FailureBehavior] = None


class CallRecordingLocationVendors(ApiModel):
    #: Default call recording is enabled.
    org_default_enabled: Optional[bool] = None
    #: Unique identifier of a vendor.
    org_default_vendor_id: Optional[str] = None
    #: Name of the call recording vendor.
    org_default_vendor_name: Optional[str] = None
    #: Unique identifier of a vendor.
    default_vendor_id: Optional[str] = None
    #: Name of the call recording vendor.
    default_vendor_name: Optional[str] = None
    #: List of available vendors and their details.
    vendors: Optional[list[RecordingVendor]] = None
    #: Region-based storage is enabled.
    org_storage_region_enabled: Optional[bool] = None
    #: Org level two character Region code.
    org_storage_region: Optional[str] = None
    #: Location level character Region code.
    storage_region: Optional[str] = None
    #: Failure behavior is enabled.
    org_failure_behavior_enabled: Optional[bool] = None
    #: Type of org-level failure behavior.
    org_failure_behavior: Optional[FailureBehavior] = None
    #: Type of location level failure behavior.
    failure_behavior: Optional[FailureBehavior] = None


class CallRecordingSettingsApi(ApiChild, base='telephony/config'):
    """
    Features:  Call Recording

    Not supported for Webex for Government (FedRAMP)

    Features: Call Recording supports reading and writing of Webex Calling Call Recording settings for a specific
    organization.

    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.

    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.

    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read(self, org_id: str = None) -> CallRecordingInfo:
        """
        Get Call Recording Settings

        Retrieve call recording settings for the organization.

        The Call Recording feature enables authorized agents to record any active call that Webex Contact Center
        manages.

        Retrieving call recording settings requires a full or read-only administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve call recording settings from this organization.
        :type org_id: str
        :rtype: :class:`CallRecordingInfo`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording')
        data = super().get(url, params=params)
        r = CallRecordingInfo.model_validate(data)
        return r

    def update(self, enabled: bool, org_id: str = None):
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

    def read_terms_of_service(self, vendor_id: str, org_id: str = None) -> CallRecordingTermsOfService:
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
        :rtype: :class:`CallRecordingTermsOfService`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'callRecording/vendors/{vendor_id}/termsOfService')
        data = super().get(url, params=params)
        r = CallRecordingTermsOfService.model_validate(data)
        return r

    def update_terms_of_service(self, vendor_id: str, enabled: bool, org_id: str = None):
        """
        Update Call Recording Terms Of Service Settings

        Update call recording terms of service settings for the given vendor.

        The Call Recording feature enables authorized agents to record any active call that Webex Contact Center
        manages.

        Updating call recording terms of service settings requires a full administrator or location administrator auth
        token with a scope of `spark-admin:telephony_config_write`.

        :param vendor_id: Update call recording terms of service settings for the given vendor.
        :type vendor_id: str
        :param enabled: Whether or not the call recording terms of service are enabled.
        :type enabled: bool
        :param org_id: Update call recording terms of service settings from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['termsOfServiceEnabled'] = enabled
        url = self.ep(f'callRecording/vendors/{vendor_id}/termsOfService')
        super().put(url, params=params, json=body)

    def read_org_call_recording_announcement(self, org_id: str = None) -> BaseCallRecordingAnnouncement:
        """
        Get Organization Call Recording Announcement Settings

        Retrieve the organization call recording announcements setting.

        The call recording Announcement feature interacts with the Call Recording feature, specifically with the
        playback of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the
        PSTN party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Retrieving organization compliance announcement setting requires a full or read-only administrator auth token
        with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve call recording announcements setting from this organization.
        :type org_id: str
        :rtype: :class:`CallRecordingAnnouncements`
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording/announcements')
        data = super().get(url, params=params)
        r = BaseCallRecordingAnnouncement.model_validate(data)
        return r

    def update_org_call_recording_announcement(
        self, settings: BaseCallRecordingAnnouncement, org_id: str = None
    ) -> None:
        """
        Update Organization Call Recording Announcement Settings.

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Updating the organization compliance announcement requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param settings: Update compliance announcement settings for this organization.
        :type settings: BaseCallRecordingAnnouncement
        :param org_id: Update the call recording announcements setting from this organization.
        :type org_id: str
        :rtype: None
        """
        params: dict[str, Any] = dict()
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.update()
        url = self.ep('callRecording/announcements')
        super().put(url, params=params, json=body)

    def read_org_compliance_announcement(self, org_id: str = None) -> OrgComplianceAnnouncement:
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
        :rtype: :class:`OrgComplianceAnnouncement`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording/complianceAnnouncement')
        data = super().get(url, params=params)
        r = OrgComplianceAnnouncement.model_validate(data)
        return r

    def update_org_compliance_announcement(
        self,
        settings: OrgComplianceAnnouncement,
        org_id: str = None,
    ):
        """
        Update the organization compliance announcement.

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Updating the organization compliance announcement requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param settings: new settings
        :type settings: OrgComplianceAnnouncement
        :param org_id: Update the compliance announcement setting from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.update()
        url = self.ep('callRecording/complianceAnnouncement')
        super().put(url, params=params, json=body)

    def read_location_compliance_announcement(
        self, location_id: str, org_id: str = None
    ) -> LocationComplianceAnnouncement:
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
        :rtype: :class:`LocationComplianceAnnouncement`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callRecording/complianceAnnouncement')
        data = super().get(url, params=params)
        r = LocationComplianceAnnouncement.model_validate(data)
        return r

    def update_location_compliance_announcement(
        self,
        location_id: str,
        settings: LocationComplianceAnnouncement,
        org_id: str = None,
    ) -> None:
        """
        Update the location compliance announcement.

        The Compliance Announcement feature interacts with the Call Recording feature, specifically with the playback
        of the start/stop announcement. When the compliance announcement is played to the PSTN party, and the PSTN
        party is connected to a party with call recording enabled, then the start/stop announcement is inhibited.

        Updating the location compliance announcement requires a full administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param location_id: Update the compliance announcement settings for this location.
        :type location_id: str
        :param settings: new settings
        :type settings: LocationComplianceAnnouncement
        :param org_id: Update the compliance announcement setting from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = settings.update()
        url = self.ep(f'locations/{location_id}/callRecording/complianceAnnouncement')
        super().put(url, params=params, json=body)

    def get_call_recording_regions(self, org_id: str = None) -> list[CallRecordingRegion]:
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
        r = TypeAdapter(list[CallRecordingRegion]).validate_python(data['regions'])
        return r

    def list_org_users(
        self, standard_user_only: bool = None, org_id: str = None, **params
    ) -> Generator[RecordingUser, None, None]:
        """
        Get Call Recording Vendor Users

        Retrieve call recording vendor users of an organization. This API is used to get the list of users who are
        assigned to the default call-recording vendor of the organization.

        The Call Recording feature supports multiple third-party call recording providers, or vendors, to capture and
        manage call recordings. An organization is configured with an overall provider, but locations can be
        configured to use a different vendor than the overall organization default.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param standard_user_only: If true, results only include Webex Calling standard users.
        :type standard_user_only: bool
        :param org_id: Retrieve call recording vendor users for this organization.
        :type org_id: str
        """
        if org_id is not None:
            params['orgId'] = org_id
        if standard_user_only is not None:
            params['standardUserOnly'] = str(standard_user_only).lower()
        url = self.ep('callRecording/vendorUsers')
        return self.session.follow_pagination(url=url, model=RecordingUser, params=params, item_key='members')

    def set_location_vendor(
        self,
        location_id: str,
        id: str = None,
        org_default_enabled: bool = None,
        storage_region: str = None,
        org_storage_region_enabled: bool = None,
        failure_behavior: FailureBehavior = None,
        org_failure_behavior_enabled: bool = None,
        org_id: str = None,
    ) -> str:
        """
        Set Call Recording Vendor for a Location

        Assign a call recording vendor to a location of an organization. Response will be `204` if the changes can be
        applied immediately otherwise `200` with a job ID is returned.

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
        body: dict[str, Any] = dict()
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

    def get_location_vendors(self, location_id: str, org_id: str = None) -> CallRecordingLocationVendors:
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
        :rtype: :class:`CallRecordingLocationVendors`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/callRecording/vendors')
        data = super().get(url, params=params)
        r = CallRecordingLocationVendors.model_validate(data)
        return r

    def list_location_users(
        self,
        location_id: str,
        max_: int = None,
        start: int = None,
        standard_user_only: bool = None,
        org_id: str = None,
        **params,
    ) -> Generator[RecordingUser, None, None]:
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
        """
        if org_id is not None:
            params['orgId'] = org_id
        if max_ is not None:
            params['max'] = max_
        if start is not None:
            params['start'] = start
        if standard_user_only is not None:
            params['standardUserOnly'] = str(standard_user_only).lower()
        url = self.ep(f'locations/{location_id}/callRecording/vendorUsers')
        return self.session.follow_pagination(url=url, model=RecordingUser, params=params, item_key='members')

    def get_org_vendors(self, org_id: str = None) -> CallRecordingVendors:
        """
        Get Organization Call Recording Vendors

        Returns what the current vendor is as well as a list of all the available vendors.

        The Call Recording feature supports multiple third-party call recording providers, or vendors, to capture and
        manage call recordings. An organization is configured with an overall provider, but locations can be
        configured to use a different vendor than the overall organization default.

        Requires a full or read-only administrator auth token with a scope of `spark-admin:telephony_config_read`.

        :param org_id: Retrieve call recording settings from this organization.
        :type org_id: str
        :rtype: :class:`CallRecordingVendors`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('callRecording/vendors')
        data = super().get(url, params=params)
        r = CallRecordingVendors.model_validate(data)
        return r

    def set_org_vendor(
        self, vendor_id: str, storage_region: str = None, failure_behavior: FailureBehavior = None, org_id: str = None
    ) -> str:
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

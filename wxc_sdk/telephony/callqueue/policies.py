"""
Call Queue policy settings
"""
from dataclasses import dataclass
from typing import Optional

from pydantic import Field

from ...base import ApiModel
from ...base import SafeEnum as Enum
from ...common import Greeting, AnnAudioFile
from ...rest import RestSession

__all__ = ['CPActionType', 'ScheduleLevel', 'CQHolidaySchedule', 'HolidayService', 'AnnouncementMode', 'NightService',
           'StrandedCalls', 'ForcedForward', 'CQPolicyApi']


class CPActionType(str, Enum):
    """
    Specifies call processing action type.
    """
    #: The caller hears a fast-busy tone.
    busy = 'BUSY'
    #: Transfers the call to number specified in transferPhoneNumber.
    transfer = 'TRANSFER'


class ScheduleLevel(str, Enum):
    """
    Specifies whether the schedule mentioned in holidayScheduleName is org or location specific.
    (Must be from holidaySchedules list)
    """
    #: Specifies this Schedule is configured across location.
    location = 'LOCATION'
    #: Specifies this Schedule is configured across organisation.
    organization = 'ORGANIZATION'


class CQHolidaySchedule(ApiModel):
    """
    pre-configured holiday schedule
    """
    #: Name of the schedule configured for a holiday service.
    schedule_name: str
    #: Specifies whether the schedule mentioned in scheduleName is org or location specific.
    schedule_level: ScheduleLevel


class HolidayService(ApiModel):
    """
    Call Queue Holiday Service details
    """
    #: Whether or not the call queue holiday service routing policy is enabled.
    holiday_service_enabled: bool
    #: Specifies call processing action type.
    action: Optional[CPActionType]
    #: Specifies whether the schedule mentioned in holidayScheduleName is org or location specific.
    #: (Must be from holidaySchedules list)
    holiday_schedule_level: Optional[ScheduleLevel]
    #: Name of the schedule configured for a holiday service as one of from holidaySchedules list.
    holiday_schedule_name: Optional[str]
    #: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
    transfer_phone_number: Optional[str]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: bool
    #: Specifies what type of announcement to be played.
    audio_message_selection: Optional[Greeting]
    #: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
    audio_files: Optional[list[AnnAudioFile]]
    #: Lists the pre-configured holiday schedules.
    holiday_schedules: list[CQHolidaySchedule] = Field(default_factory=list)


class AnnouncementMode(str, Enum):
    """
    Specifies the type of announcements to played.
    """
    #: Plays announcement as per audioMessageSelection.
    normal = 'NORMAL'
    #: Plays announcement as per manualAudioMessageSelection.
    manual = 'MANUAL'


class NightService(ApiModel):
    """
    Call Queue Night service details
    """
    #: Whether or not the call queue night service routing policy is enabled.
    night_service_enabled: bool
    #: Specifies call processing action type.
    action: Optional[CPActionType]
    #: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
    transfer_phone_number: Optional[str]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: bool
    #: Specifies the type of announcements to played.
    announcement_mode: Optional[AnnouncementMode]
    #: Specifies what type of announcement to be played.
    audio_message_selection: Optional[Greeting]
    #: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
    audio_files: Optional[list[AnnAudioFile]]
    #: Name of the schedule configured for a night service as one of from businessHourSchedules list.
    business_hours_name: Optional[str]
    #: Specifies whether the above mentioned schedule is org or location specific.
    #: (Must be from businessHourSchedules list).
    business_hours_level: Optional[ScheduleLevel]
    #: Lists the pre-configured business hour schedules.
    business_hour_schedules: list[CQHolidaySchedule] = Field(default_factory=list)
    #: Force night service regardless of business hour schedule.
    force_night_service_enabled: Optional[bool]
    #: Specifies what type of announcement to be played when announcementMode is MANUAL.
    manual_audio_message_selection: Optional[Greeting]
    #: List Of Audio Files.
    manual_audio_files: Optional[list[AnnAudioFile]]


class StrandedCallsAction(str, Enum):
    """
    Specifies call processing action type for stranded calls
    """
    #: Call remains in the queue.
    none = 'NONE'
    #: The caller hears a fast-busy tone.
    busy = 'BUSY'
    #: Transfers the call to number specified in transferPhoneNumber.
    transfer = 'TRANSFER'
    #: Calls are handled according to the Night Service configuration. If the Night Service action is set to none,
    #: then this is equivalent to this policy being set to none (that is, calls remain in the queue).
    night_service = 'NIGHT_SERVICE'
    #: Calls are removed from the queue and are provided with ringing until the caller releases the call. The
    #: ringback tone played to the caller is localized according to the country code of the caller.
    ringing = 'RINGING'
    #: Calls are removed from the queue and are provided with an announcement that is played in a loop until the
    # caller releases the call.
    announcement = 'ANNOUNCEMENT'


class StrandedCalls(ApiModel):
    """
    Call Queue Holiday Service details
    """
    #: Specifies call processing action type.
    action: Optional[StrandedCallsAction]
    #: Call gets transferred to this number when action is set to TRANSFER. This can also be an extension.
    transfer_phone_number: Optional[str]
    audio_message_selection: Optional[Greeting]
    #: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
    audio_files: Optional[list[AnnAudioFile]]


class ForcedForward(ApiModel):
    """
    Call Queue policy Forced Forward details
    """
    #: Whether or not the call queue forced forward routing policy setting is enabled.
    forced_forward_enabled: bool
    #: All incoming calls are forwarded to this number. This can also be an extension.
    transfer_phone_number: Optional[str]
    #: Specifies if an announcement plays to callers before applying the action.
    play_announcement_before_enabled: Optional[bool]
    #: Specifies what type of announcement to be played.
    audio_message_selection: Optional[Greeting]
    #: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
    audio_files: Optional[list[AnnAudioFile]]


@dataclass(init=False)
class CQPolicyApi:
    _session: RestSession

    def _ep(self, location_id: str, queue_id: str, path: str):
        return self._session.ep(f'telephony/config/locations/{location_id}/queues/{queue_id}/{path}')

    def __init__(self, session: RestSession):
        self._session = session

    def holiday_service_details(self, location_id: str, queue_id: str, org_id: str = None) -> HolidayService:
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
        data = self._session.rest_get(url=url, params=params)
        return HolidayService.parse_obj(data)

    def holiday_service_update(self, location_id: str, queue_id: str, update: HolidayService, org_id: str = None):
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
        self._session.rest_put(url=url, params=params, data=body)

    def night_service_detail(self, location_id: str, queue_id: str, org_id: str = None) -> NightService:
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
        data = self._session.rest_get(url=url, params=params)
        return NightService.parse_obj(data)

    def night_service_update(self, location_id: str, queue_id: str, update: NightService, org_id: str = None):
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
        self._session.rest_put(url=url, params=params, data=body)

    def stranded_calls_details(self, location_id: str, queue_id: str, org_id: str = None) -> StrandedCalls:
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
        data = self._session.rest_get(url=url, params=params)
        return StrandedCalls.parse_obj(data)

    def stranded_calls_update(self, location_id: str, queue_id: str, update: StrandedCalls, org_id: str = None):
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
        self._session.rest_put(url=url, params=params, data=update.json())

    def forced_forward_details(self, location_id: str, queue_id: str, org_id: str = None) -> ForcedForward:
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
        data = self._session.rest_get(url=url, params=params)
        return ForcedForward.parse_obj(data)

    def forced_forward_update(self, location_id: str, queue_id: str, update: ForcedForward, org_id: str = None):
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
        self._session.rest_put(url=url, params=params, data=update.json())

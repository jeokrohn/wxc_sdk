from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['GetMeetingConfigurationCommonSettingObject',
           'GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions',
           'GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsEntryAndExitTone',
           'GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsTelephonySupport',
           'GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions',
           'GetMeetingConfigurationCommonSettingObjectSecurityOptions',
           'GetMeetingConfigurationCommonSettingObjectSecurityOptionsPasswordCriteria',
           'GetMeetingConfigurationCommonSettingObjectSiteOptions',
           'GetMeetingConfigurationCommonSettingObjectTelephonyConfig', 'SiteApi']


class GetMeetingConfigurationCommonSettingObjectSiteOptions(ApiModel):
    #: Allow hosts to change their Personal Room URLs.
    allow_custom_personal_room_url: Optional[bool] = Field(alias='allowCustomPersonalRoomURL', default=None)


class GetMeetingConfigurationCommonSettingObjectTelephonyConfig(ApiModel):
    #: Whether call-in teleconferencing for sessions was enabled.
    allow_call_in: Optional[bool] = None
    #: Whether call-back teleconferencing for sessions was enabled.
    allow_call_back: Optional[bool] = None
    #: Whether other teleconferencing for sessions was enabled.
    allow_other_teleconf: Optional[bool] = None
    #: Whether toll-free call-in teleconferencing was enabled.
    allow_toll_free_callin: Optional[bool] = None
    #: Whether international call-in teleconferencing was enabled.
    allow_international_callin: Optional[bool] = None
    #: Whether international call-back teleconferencing was enabled.
    allow_international_callback: Optional[bool] = None
    #: Whether Voice Over IP functionality using the attendee computer's speakers and microphones was enabled.
    vo_ip: Optional[bool] = Field(alias='VoIP', default=None)


class GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsEntryAndExitTone(str, Enum):
    #: No tone.
    no_tone = 'NoTone'
    #: Beep.
    beep = 'Beep'
    #: Announce name.
    announce_name = 'AnnounceName'


class GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsTelephonySupport(str, Enum):
    #: None.
    none_ = 'None'
    #: Webex teleconferencing.
    webex_teleconferencing = 'WebexTeleconferencing'
    #: Other Teleconferencing.
    other = 'Other'


class GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions(ApiModel):
    #: Determines if a sound is made when someone enters or exits.
    #: example: Beep
    entry_and_exit_tone: Optional[GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsEntryAndExitTone] = None
    #: Specifies whether or not joining teleconference without pressing 1 is checked by default.
    join_teleconf_not_press1: Optional[bool] = None
    #: Specifies the type of teleconference support for meetings.
    #: example: WebexTeleconferencing
    telephony_support: Optional[GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptionsTelephonySupport] = None
    #: Specifies whether toll-free call-in is available.
    toll_free: Optional[bool] = None
    #: Denotes if VoIP protocols are being used.
    vo_ip: Optional[bool] = Field(alias='VoIP', default=None)


class GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions(ApiModel):
    #: Determines if email reminders are to be sent out.
    email_reminders: Optional[bool] = None


class GetMeetingConfigurationCommonSettingObjectSecurityOptionsPasswordCriteria(ApiModel):
    #: Determines if a password requires mixed case.
    mixed_case: Optional[bool] = None
    #: Sets the minimum password length.
    #: example: 8
    min_length: Optional[int] = None
    #: Sets the minimum number of numeric characters in the password.
    #: example: 2
    min_numeric: Optional[int] = None
    #: Sets the minimum number of alphabetical characters in the password.
    #: example: 4
    min_alpha: Optional[int] = None
    #: Sets the minimum number of special characters in the password.
    #: example: 1
    min_special: Optional[int] = None
    #: Do not allow dynamic web page text for meeting passwords (like site name, host's name, username, meeting topic).
    disallow_dynamic_web_text: Optional[bool] = None
    #: Specifies if passwords from the `disallowValues` list are to be allowed.
    disallow_list: Optional[bool] = None
    #: Sets password values that are not allowed.
    disallow_values: Optional[list[str]] = None


class GetMeetingConfigurationCommonSettingObjectSecurityOptions(ApiModel):
    #: Allow attendees or panelists to join before the host.
    join_before_host: Optional[bool] = None
    #: Allows attendees or panelists to join the teleconference before the host.
    audio_before_host: Optional[bool] = None
    #: Allows first attendee or panelist as the presenter.
    first_attendee_as_presenter: Optional[bool] = None
    #: Specifies that all meetings must be unlisted.
    unlist_all_meetings: Optional[bool] = None
    #: Determines if a user must login before getting site access.
    require_login_before_access: Optional[bool] = None
    #: Allow screen capture (Android devices only).
    allow_mobile_screen_capture: Optional[bool] = None
    #: Determines if strict passwords are required for meetings.
    require_strong_password: Optional[bool] = None
    #: Criteria of a strong password.
    password_criteria: Optional[GetMeetingConfigurationCommonSettingObjectSecurityOptionsPasswordCriteria] = None


class GetMeetingConfigurationCommonSettingObject(ApiModel):
    #: Site Options on Webex Administration.
    site_options: Optional[GetMeetingConfigurationCommonSettingObjectSiteOptions] = None
    #: Telephony Configuration on WebEx Super Admin (These options are read-only, unable to update by Update Common
    #: Settings API).
    telephony_config: Optional[GetMeetingConfigurationCommonSettingObjectTelephonyConfig] = None
    #: Default Scheduler Options on Webex Administration (These options are applied to the site as defaults, but
    #: individual users can change them).
    default_scheduler_options: Optional[GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions] = None
    #: Schedule Meeting Options on Webex Administration.
    schedule_meeting_options: Optional[GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions] = None
    #: Security Options on Webex Administration.
    security_options: Optional[GetMeetingConfigurationCommonSettingObjectSecurityOptions] = None


class SiteApi(ApiChild, base='admin/meeting/config/commonSettings'):
    """
    Site
    
    This chapter provides descriptions of the Webex RESTful APIs for the site service, which contains operations like
    querying and updating common meeting configuration settings.
    
    Samples are given for the outbound request messages and expected server response messages. The API calls available
    as part of the Site service are listed below.
    
    You can see the elements that constitute the respective RESTful schema in a separate section below.
    """

    def get_meeting_common_settings_configuration(self,
                                                  site_url: str = None) -> GetMeetingConfigurationCommonSettingObject:
        """
        Get Meeting Common Settings Configuration

        Site administrators can use this API to get a list of functions, options, and privileges that are configured
        for their Webex service sites.

        * If `siteUrl` is specified, common settings of the meeting's configuration of the specified site will be
        queried; otherwise, the API will query from the site administrator's preferred site. All available Webex sites
        and preferred site of the user can be retrieved by `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        :param site_url: URL of the Webex site which the API queries common settings of the meeting's configuration
            from. If not specified, the API will query from the site administrator's preferred site. All available
            Webex sites and the preferred site of the user can be retrieved by the `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :rtype: :class:`GetMeetingConfigurationCommonSettingObject`
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep()
        data = super().get(url, params=params)
        r = GetMeetingConfigurationCommonSettingObject.model_validate(data)
        return r

    def update_meeting_common_settings_configuration(self,
                                                     site_options: GetMeetingConfigurationCommonSettingObjectSiteOptions,
                                                     default_scheduler_options: GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions,
                                                     schedule_meeting_options: GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions,
                                                     security_options: GetMeetingConfigurationCommonSettingObjectSecurityOptions) -> GetMeetingConfigurationCommonSettingObject:
        """
        Update Meeting Common Settings Configuration

        Site administrators can use this API to update the option of features, options and privileges that are
        configured for their WebEx service sites.

        :param site_options: Site Options on Webex Administration.
        :type site_options: GetMeetingConfigurationCommonSettingObjectSiteOptions
        :param default_scheduler_options: Default Scheduler Options on Webex Administration (These options are applied
            to the site as defaults, but individual users can change them).
        :type default_scheduler_options: GetMeetingConfigurationCommonSettingObjectDefaultSchedulerOptions
        :param schedule_meeting_options: Schedule Meeting Options on Webex Administration.
        :type schedule_meeting_options: GetMeetingConfigurationCommonSettingObjectScheduleMeetingOptions
        :param security_options: Security Options on Webex Administration.
        :type security_options: GetMeetingConfigurationCommonSettingObjectSecurityOptions
        :rtype: :class:`GetMeetingConfigurationCommonSettingObject`
        """
        body = dict()
        body['siteOptions'] = site_options.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['defaultSchedulerOptions'] = default_scheduler_options.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['scheduleMeetingOptions'] = schedule_meeting_options.model_dump(mode='json', by_alias=True, exclude_none=True)
        body['securityOptions'] = security_options.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep()
        data = super().patch(url, json=body)
        r = GetMeetingConfigurationCommonSettingObject.model_validate(data)
        return r

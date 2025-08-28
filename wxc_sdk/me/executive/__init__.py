from typing import Optional

from pydantic import TypeAdapter, Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum
from wxc_sdk.common import IdAndName, PrimaryOrSecondary
from wxc_sdk.common.schedules import ScheduleType
from wxc_sdk.common.selective import SelectiveFrom

__all__ = ['ExecAlertingMode', 'ExecAlertRolloverAction', 'ExecAlertClidNameMode', 'ExecAlertClidPhoneNumberMode',
           'ExecAlert', 'ExecOrAssistant', 'AssignedAssistants', 'AssistantSettings',
           'ExecCallFilterType', 'ExecCallFilteringCriteriaItem', 'ExecCallFiltering',
           'ExecCallFilteringScheduleLevel', 'ExecCallFilteringToNumber', 'ExecCallFilteringCriteria',
           'ExecScreeningAlertType', 'ExecScreening', 'MeExecutiveApi']


class ExecAlertingMode(str, Enum):
    #: Alerts assistants one at a time in the defined order.
    sequential = 'SEQUENTIAL'
    #: Alerts all assistants at the same time.
    simultaneous = 'SIMULTANEOUS'


class ExecAlertRolloverAction(str, Enum):
    voice_messaging = 'VOICE_MESSAGING'
    no_answer_processing = 'NO_ANSWER_PROCESSING'
    forward = 'FORWARD'


class ExecAlertClidNameMode(str, Enum):
    #: Display executive name followed by caller name.
    executive_originator = 'EXECUTIVE_ORIGINATOR'
    #: Display caller name followed by executive name.
    originator_executive = 'ORIGINATOR_EXECUTIVE'
    #: Display only executive name.
    executive = 'EXECUTIVE'
    #: Display only caller name.
    originator = 'ORIGINATOR'
    #: Display a custom name.
    custom = 'CUSTOM'


class ExecAlertClidPhoneNumberMode(str, Enum):
    #: Display executive's phone number.
    executive = 'EXECUTIVE'
    #: Display caller's phone number.
    originator = 'ORIGINATOR'
    #: Display a custom phone number.
    custom = 'CUSTOM'


class ExecAlert(ApiModel):
    #: * `SEQUENTIAL` - Alerts assistants one at a time in the defined order.
    alerting_mode: Optional[ExecAlertingMode] = None
    #: Number of rings before alerting the next assistant when in sequential mode.
    next_assistant_number_of_rings: Optional[int] = None
    #: Controls whether the rollover timer (`rolloverWaitTimeInSecs`) is enabled. When set to `true`, rollover will
    #: trigger after the timer expires, even if assistants are still available. When `false`, rollover only occurs
    #: when no assistants remain.
    rollover_enabled: Optional[bool] = None
    #: Specifies what happens when rollover is triggered:
    #: - VOICE_MESSAGING: Send to Voicemail—A voicemail is sent to the executive.
    #: - FORWARD: Forward—Calls are forwarded to a specified number.
    #: - NO_ANSWER_PROCESSING: Do nothing—No action is taken.
    #: Rollover is always triggered when no assistants remain for a filtered call. If the rollover timer is enabled,
    #: rollover can also be triggered when the timer expires, even if assistants are still available.
    rollover_action: Optional[ExecAlertRolloverAction] = None
    #: Phone number to forward calls to when rollover action is set to FORWARD.
    rollover_forward_to_phone_number: Optional[str] = None
    #: Time in seconds to wait before applying the rollover action.
    rollover_wait_time_in_secs: Optional[int] = None
    #: * `EXECUTIVE_ORIGINATOR` - Display executive name followed by caller name.
    clid_name_mode: Optional[ExecAlertClidNameMode] = None
    #: Custom caller ID name to display (deprecated).
    custom_clidname: Optional[str] = Field(alias='customCLIDName', default=None)
    #: Custom caller ID name in Unicode format.
    custom_clidname_in_unicode: Optional[str] = Field(alias='customCLIDNameInUnicode', default=None)
    #: * `EXECUTIVE` - Display executive's phone number.
    clid_phone_number_mode: Optional[ExecAlertClidPhoneNumberMode] = None
    #: Custom caller ID phone number to display.
    custom_clidphone_number: Optional[str] = Field(alias='customCLIDPhoneNumber', default=None)

    def update(self) -> dict:
        """
        data for update()

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_unset=True)


class ExecOrAssistant(ApiModel):
    #: Unique identifier of the assistant.
    id: Optional[str] = None
    #: First name of the assistant.
    first_name: Optional[str] = None
    #: Last name of the assistant.
    last_name: Optional[str] = None
    #: Direct number of the assistant.
    direct_number: Optional[str] = None
    #: Extension number of the assistant.
    extension: Optional[str] = None
    #: If `true`, the assistant can opt in to the executive assistant pool.
    opt_in_enabled: Optional[bool] = None
    location: Optional[IdAndName] = None


class AssignedAssistants(ApiModel):
    #: If `true`, the user can opt in or out of the executive assistant pool.
    allow_opt_in_out_enabled: Optional[bool] = None
    #: List of assigned executive assistants.
    assistants: Optional[list[ExecOrAssistant]] = None

    def update(self) -> dict:
        """
        data for update()

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_unset=True,
                               include={'allow_opt_in_out_enabled': True,
                                        'assistants': {'__all__': {'id': True}}})


class AssistantSettings(ApiModel):
    #: If `true`, the executive assistant forwards filtered calls to the forward to phone number.
    forward_filtered_calls_enabled: Optional[bool] = None
    #: Phone number to forward calls to.
    forward_to_phone_number: Optional[str] = None
    #: List of assigned executives.
    executives: Optional[list[ExecOrAssistant]] = None

    def update(self) -> dict:
        """
        data for update()

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_unset=True,
                               include={'forward_filtered_calls_enabled': True,
                                        'forward_to_phone_number': True,
                                        'executives': {'__all__': {'id': True, 'opt_in_enabled': True}}})


class ExecCallFilterType(str, Enum):
    #: Choose this option to ensure only specific calls are sent to the executive assistant.
    custom_call_filters = 'CUSTOM_CALL_FILTERS'
    #: Choose this option to send both internal and external calls to the executive assistant.
    all_calls = 'ALL_CALLS'
    #: Choose this option to send all the internal calls to the executive assistant.
    all_internal_calls = 'ALL_INTERNAL_CALLS'
    #: Choose this option to send all the external calls to the executive assistant.
    all_external_calls = 'ALL_EXTERNAL_CALLS'


class ExecCallFilteringCriteriaItem(ApiModel):
    #: Unique identifier for the filter criteria.
    id: Optional[str] = None
    #: Name of the criteria.
    filter_name: Optional[str] = None
    source: Optional[SelectiveFrom] = None
    #: Controls whether this filter criteria is active. When `true`, the criteria is evaluated for incoming calls. When
    #: `false`, the criteria is completely ignored and has no effect on call filtering.
    activation_enabled: Optional[bool] = None
    #: Controls the action when this criteria matches a call. When `true`, matching calls are filtered (blocked). When
    #: `false`, matching calls are allowed through and take precedence over other filtering criteria, creating
    #: exceptions to let specific calls through.
    filter_enabled: Optional[bool] = None


class ExecCallFiltering(ApiModel):
    #: Indicates if executive call filtering is enabled.
    enabled: Optional[bool] = None
    filter_type: Optional[ExecCallFilterType] = None
    #: List of call filtering criteria configured for executive call filtering.
    criteria: Optional[list[ExecCallFilteringCriteriaItem]] = None

    def update(self) -> dict:
        """
        data for update()

        :meta private:
        """
        data = self.model_dump(mode='json', by_alias=True, exclude_unset=True,
                               include={'enabled': True,
                                        'filter_type': True,
                                        'criteria': {'__all__': {'id': True,
                                                                 'activation_enabled': True}}})
        criteria = data.pop('criteria', None)
        if criteria is not None:
            data['criteriaActivation'] = criteria
        return data


class ExecCallFilteringScheduleLevel(str, Enum):
    #: The schedule applies to the individual user.
    people = 'PEOPLE'
    #: The schedule applies at the account level, potentially affecting multiple users.
    location = 'LOCATION'


class ExecCallFilteringToNumber(ApiModel):
    type: Optional[PrimaryOrSecondary] = None
    #: The phone number to call.
    phone_number: Optional[str] = None


class ExecCallFilteringCriteria(ApiModel):
    #: Unique identifier for the filter criteria.
    id: Optional[str] = None
    #: Name of the criteria.
    filter_name: Optional[str] = None
    #: Name of the schedule associated with this criteria.
    schedule_name: Optional[str] = None
    #: * `holidays` - The schedule is based on specific times.
    schedule_type: Optional[ScheduleType] = None
    #: * `PEOPLE` - The schedule applies to the individual user.
    schedule_level: Optional[ExecCallFilteringScheduleLevel] = None
    #: * `ANY_PHONE_NUMBER` - The criteria applies to any phone number.
    calls_from: Optional[SelectiveFrom] = None
    #: Indicates if the criteria applies to anonymous callers.
    anonymous_callers_enabled: Optional[bool] = None
    #: Indicates if the criteria applies to unavailable callers.
    unavailable_callers_enabled: Optional[bool] = None
    #: List of phone numbers that this filtering criteria applies to.
    phone_numbers: Optional[list[str]] = None
    #: Controls the action when this criteria matches a call. When `true`, matching calls are filtered (blocked). When
    #: `false`, matching calls are allowed through and take precedence over other filtering criteria, creating
    #: exceptions to let specific calls through.
    filter_enabled: Optional[bool] = None
    #: List of phone numbers to route calls to when this criteria matches.
    calls_to_numbers: Optional[list[ExecCallFilteringToNumber]] = None

    def create(self) -> dict:
        """
        data for create()

        :meta private:
        """
        return self.model_dump(mode='json', by_alias=True, exclude_unset=True,
                               exclude={'id': True})

    def update(self) -> dict:
        """
        data for update()

        :meta private:
        """
        return self.create()


class ExecScreeningAlertType(str, Enum):
    #: No audible alert is provided for executive screening.
    silent = 'SILENT'
    #: A short ring (splash) is used as an alert for executive screening.
    ring_splash = 'RING_SPLASH'


class ExecScreening(ApiModel):
    #: Indicates if executive screening is enabled.
    enabled: Optional[bool] = None
    alert_type: Optional[ExecScreeningAlertType] = None
    #: Indicates if alerts are enabled for Single Number Reach locations.
    alert_anywhere_location_enabled: Optional[bool] = None
    #: Indicates if alerts are enabled for Webex Go locations.
    alert_mobility_location_enabled: Optional[bool] = None
    #: Indicates if alerts are enabled for Shared Call Appearance locations.
    alert_shared_call_appearance_location_enabled: Optional[bool] = None


class MeExecutiveApi(ApiChild, base='telephony/config/people/me'):
    def alert_settings(self) -> ExecAlert:
        """
        Get User Executive Alert Settings

        Get executive alert settings for the authenticated user.

        Executive Alert settings in Webex allow you to control how calls are routed to executive assistants, including
        alerting mode, rollover options, and caller ID presentation. You can configure settings such as sequential or
        simultaneous alerting, and specify what happens when calls aren't answered.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`ExecAlert`
        """
        url = self.ep('settings/executive/alert')
        data = super().get(url)
        r = ExecAlert.model_validate(data)
        return r

    def update_alert_settings(self, settings: ExecAlert):
        """
        Modify User Executive Alert Settings

        Update executive alert settings for the authenticated user.

        Executive Alert settings in Webex allow you to control how calls are routed to executive assistants, including
        alerting mode, rollover options, and caller ID presentation. You can configure settings such as sequential or
        simultaneous alerting, and specify what happens when calls aren't answered.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: Alert settings
        :type settings: ExecAlert
        """
        body = settings.update()
        url = self.ep('settings/executive/alert')
        super().put(url, json=body)

    def assigned_assistants(self) -> AssignedAssistants:
        """
        Get My Executive Assigned Assistants

        Get list of assigned executive assistants for an authenticated user.

        As an executive, you can add assistants to your executive pool to manage calls for you. You can set when and
        which types of calls they can handle. Assistants can opt in when needed or opt out when not required.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`AssignedAssistants`
        """
        url = self.ep('settings/executive/assignedAssistants')
        data = super().get(url)
        r = AssignedAssistants.model_validate(data)
        return r

    def update_assigned_assistants(self, assigned_assistants: AssignedAssistants):
        """
        Update My Executive Assigned Assistants

        Update assigned executive assistants for the authenticated user.

        As an executive, you can add assistants to your executive pool to manage calls for you. You can set when and
        which types of calls they can handle. Assistants can opt in when needed or opt out when not required.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param assigned_assistants: Assigned Assistants
        :type assigned_assistants: AssignedAssistants
        :rtype: None
        """
        body = assigned_assistants.update()
        if assigned_assistants.assistants:
            body['assistantIds'] = [a.id for a in assigned_assistants.assistants]
            body.pop('assistants')
        url = self.ep('settings/executive/assignedAssistants')
        super().put(url, json=body)

    def executive_assistant_settings(self) -> AssistantSettings:
        """
        Get My Executive Assistant Settings

        Get settings for an executive assistant.

        Executive assistants can make, answer, intercept, and route calls appropriately on behalf of their executive.
        Assistants can also set the call forwarding destination, and join or leave an executive’s pool.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`AssistantSettings`
        """
        url = self.ep('settings/executive/assistant')
        data = super().get(url)
        r = AssistantSettings.model_validate(data)
        return r

    def update_executive_assistant_settings(self, assistant_settings: AssistantSettings):
        """
        Update My Executive Assistant Settings

        Update Settings for an executive assistant.

        Executive assistants can make, answer, intercept, and route calls appropriately on behalf of their executive.
        Assistants can also set the call forwarding destination, and join or leave an executive’s pool.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param assistant_settings: My Executive Assistant Settings
        :type assistant_settings: AssistantSettings
        """
        body = assistant_settings.update()
        url = self.ep('settings/executive/assistant')
        super().put(url, json=body)

    def executive_available_assistants(self) -> list[ExecOrAssistant]:
        """
        Get My Executive Available Assistants

        Get a list of available executive assistants for the authenticated user.

        As an executive, you can add assistants to your executive pool to manage calls for you. You can set when and
        which types of calls they can handle. Assistants can opt in when needed or opt out when not required.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: list[ExecOrAssistant]
        """
        url = self.ep('settings/executive/availableAssistants')
        data = super().get(url)
        r = TypeAdapter(list[ExecOrAssistant]).validate_python(data['assistants'])
        return r

    def executive_call_filtering_settings(self) -> ExecCallFiltering:
        """
        Get User Executive Call Filtering Settings

        Get executive call filtering settings for the authenticated user.

        Executive Call Filtering in Webex allows you to control which calls are allowed to reach the executive
        assistant based on custom criteria, such as specific phone numbers or call types. You can enable or disable
        call filtering and configure filter rules to manage incoming calls.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`ExecCallFiltering`
        """
        url = self.ep('settings/executive/callFiltering')
        data = super().get(url)
        r = ExecCallFiltering.model_validate(data)
        return r

    def update_executive_call_filtering_settings(self, settings: ExecCallFiltering):
        """
        Update User Executive Call Filtering Settings

        Update executive call filtering settings for the authenticated user.

        Executive Call Filtering in Webex allows you to control which calls are allowed to reach the executive
        assistant based on custom criteria, such as specific phone numbers or call types. You can enable or disable
        call filtering and configure filter rules to manage incoming calls.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: Call Filtering Settings
        :type settings: ExecCallFiltering
        """
        body = settings.update()
        url = self.ep('settings/executive/callFiltering')
        super().put(url, json=body)

    def create_call_filtering_criteria(self, settings: ExecCallFilteringCriteria) -> str:
        """
        Create User Executive Call Filtering Criteria

        Create a new executive call filtering criteria for the authenticated user.

        Executive Call Filtering Criteria in Webex allows you to define detailed filter rules for incoming calls. This
        API creates a new filter rule with the specified configuration, including schedule, phone numbers, and call
        routing preferences.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: Call Filtering Settings
        :type settings: ExecCallFilteringCriteria
        """
        body = settings.create()
        url = self.ep('settings/executive/callFiltering/criteria')
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_call_filtering_criteria(self, id: str):
        """
        Delete User Executive Call Filtering Criteria

        Delete a specific executive call filtering criteria for the authenticated user.

        Executive Call Filtering Criteria in Webex allows you to manage detailed filter rules for incoming calls. This
        API removes a specific filter rule by its unique identifier.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the executive call filtering criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL2RHVnpkRjltYVd4MFpYST0`.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'settings/executive/callFiltering/criteria/{id}')
        super().delete(url)

    def call_filtering_criteria(self, id: str) -> ExecCallFilteringCriteria:
        """
        Get User Executive Call Filtering Criteria Settings

        Get executive call filtering criteria settings for the authenticated user.

        Executive Call Filtering Criteria in Webex allows you to retrieve detailed configuration for a specific filter
        rule. This includes schedule settings, phone number filters, and call routing preferences for executive call
        filtering.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :param id: The `id` parameter specifies the unique identifier for the executive call filtering criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL2RHVnpkRjltYVd4MFpYST0`.
        :type id: str
        :rtype: :class:`ExecCallFilteringCriteria`
        """
        url = self.ep(f'settings/executive/callFiltering/criteria/{id}')
        data = super().get(url)
        r = ExecCallFilteringCriteria.model_validate(data)
        return r

    def update_call_filtering_criteria(self, id: str, settings: ExecCallFilteringCriteria) -> str:
        """
        Update User Executive Call Filtering Criteria Settings

        Update executive call filtering criteria settings for the authenticated user.

        Executive Call Filtering Criteria in Webex allows you to modify detailed configuration for a specific filter
        rule. This includes updating schedule settings, phone number filters, and call routing preferences for
        executive call filtering.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param id: The `id` parameter specifies the unique identifier for the executive call filtering criteria.
            Example: `Y2lzY29zcGFyazovL3VzL0NSSVRFUklBL2RHVnpkRjltYVd4MFpYST0`.
        :type id: str
        :param settings: Call Filtering Settings
        :type settings: ExecCallFilteringCriteria
        :rtype: str
        """
        body = settings.update()
        url = self.ep(f'settings/executive/callFiltering/criteria/{id}')
        data = super().put(url, json=body)
        r = data['id']
        return r

    def screening_settings(self) -> ExecScreening:
        """
        Get User Executive Screening Settings

        Get executive screening settings for the authenticated user.

        Executive Screening in Webex allows you to manage how incoming calls are screened and alerted based on your
        preferences. You can enable or disable executive screening and configure alert types and locations for
        notifications.

        This API requires a user auth token with a scope of `spark:telephony_config_read`.

        :rtype: :class:`ExecScreening`
        """
        url = self.ep('settings/executive/screening')
        data = super().get(url)
        r = ExecScreening.model_validate(data)
        return r

    def update_screening_settings(self, settings: ExecScreening):
        """
        Modify User Executive Screening Settings

        Update executive screening settings for the authenticated user.

        Executive Screening in Webex allows you to manage how incoming calls are screened and alerted based on your
        preferences. You can enable or disable executive screening and configure alert types and locations for
        notifications.

        This API requires a user auth token with a scope of `spark:telephony_config_write`.

        :param settings: Screening Settings
        :type settings: ExecScreening

        """
        body = settings.model_dump(mode='json', by_alias=True, exclude_unset=True)
        url = self.ep('settings/executive/screening')
        super().put(url, json=body)

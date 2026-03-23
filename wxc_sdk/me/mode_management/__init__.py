from typing import Optional

from pydantic import TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.common.schedules import ScheduleLevel
from wxc_sdk.person_settings.mode_management import ExceptionType, ModeManagementFeature
from wxc_sdk.telephony.forwarding import ForwardToSelection
from wxc_sdk.telephony.operating_modes import (
    DifferentHoursDaily,
    OperatingModeHoliday,
    OperatingModeSchedule,
    SameHoursDaily,
)

__all__ = [
    'MeModeManagementApi',
    'FeatureDetail',
    'FeatureMode',
    'FeatureModeForwardTo',
    'OperatingModeDetail',
    'OperatingModeForwardTo',
]


class FeatureModeForwardTo(ApiModel):
    selection: Optional[ForwardToSelection] = None
    #: Phone number to forward to when selection is FORWARD_TO_SPECIFIED_NUMBER.
    phone_number: Optional[str] = None
    #: Whether to send to voicemail when selection is FORWARD_TO_SPECIFIED_NUMBER.
    send_to_voicemail_enabled: Optional[bool] = None
    #: Default phone number when selection is FORWARD_TO_DEFAULT_NUMBER. This field is not present if the mode's
    #: default is to not forward.
    default_phone_number: Optional[str] = None
    #: Whether default is to send to voicemail
    default_send_to_voicemail_enabled: Optional[bool] = None


class FeatureMode(ApiModel):
    #: Unique identifier for the operating mode.
    id: Optional[str] = None
    #: Display name of the operating mode.
    name: Optional[str] = None
    type: Optional[OperatingModeSchedule] = None
    level: Optional[ScheduleLevel] = None
    #: Whether this mode is enabled for normal operation.
    normal_operation_enabled: Optional[bool] = None
    #: Forwarding configuration for this mode
    forward_to: Optional[FeatureModeForwardTo] = None


class FeatureDetail(ApiModel):
    #: Whether mode based forwarding is enabled for the feature
    mode_based_forwarding_enabled: Optional[bool] = None
    #: Timezone for the feature
    timezone: Optional[str] = None
    #: Phone number of the feature
    phone_number: Optional[str] = None
    #: Extension of the feature
    extension: Optional[str] = None
    #: Unique identifier for the current operating mode.
    current_operating_mode_id: Optional[str] = None
    #: The current operating mode's end time in 12-hour format showing hour and minute only (no date information). This
    #: field's presence and meaning depends on the operational state:
    #:  * Present during normal operation with the time at which the next mode change will occur.
    #:  * Not present for Manual Switch Back exceptions.
    #:  * For Automatic Switch Back (Early Start) exceptions it is when the exception ends and the feature automatically
    #:    reverts to normal operation which is the mode's configured start time.
    #:  * For Automatic Switch Back (Extension) exceptions it is when the exception ends and the feature automatically
    #:    reverts to normal operation which is the mode's configured end time when the exception started plus the
    #:    extension time.
    #:  * For Automatic Switch Back (Standard) exceptions it is when the exception ends and the feature automatically
    #:    reverts to normal operation which is the mode's configured end time.
    current_operating_mode_end_time: Optional[str] = None
    #: Forward destination for current operating mode
    current_operating_mode_forward_destination: Optional[str] = None
    #: Type of exception indicating how the feature will switch back from the current mode. This field is not present
    #: when the feature is in normal operation.
    exception_type: Optional[ExceptionType] = None
    #: Array of operating modes configured for this feature
    modes: Optional[list[FeatureMode]] = None


class OperatingModeForwardTo(ApiModel):
    #: Whether call forwarding is enabled
    enabled: Optional[bool] = None
    #: Forwarding destination phone number
    destination: Optional[str] = None
    #: Whether to send to voicemail
    send_to_voicemail_enabled: Optional[bool] = None


class OperatingModeDetail(ApiModel):
    #: Unique identifier for the operating mode.
    operating_mode_id: Optional[str] = None
    #: Display name of the operating mode.
    name: Optional[str] = None
    type: Optional[OperatingModeSchedule] = None
    level: Optional[ScheduleLevel] = None
    #: Location name
    location_name: Optional[str] = None
    #: Schedule configuration when same hours apply for weekdays and weekends
    same_hours_daily: Optional[SameHoursDaily] = None
    #: Schedule configuration when different hours apply for each day
    different_hours_daily: Optional[DifferentHoursDaily] = None
    #: Array of holiday schedule events
    holidays: Optional[list[OperatingModeHoliday]] = None
    #: Call forwarding configuration for this operating mode
    forward_to: Optional[OperatingModeForwardTo] = None


class MeModeManagementApi(ApiChild, base='telephony/config/people/me'):
    def get_features(self) -> list[ModeManagementFeature]:
        """
        Get Mode Management Features

        Retrieves a list of all mode management features (Auto Attendants, Call Queues, and Hunt Groups) for which the
        authenticated user has been designated as a mode manager. This API returns basic information about each
        feature including its ID, name, and type.

        Mode Management allows designated managers to switch features between different operational configurations
        based on time schedules or manual triggers. This is useful for managing business hours, holidays, and
        emergency scenarios.

        This API requires a user auth token with the `spark:telephony_config_read` scope. The authenticated user must
        be configured as a mode manager for at least one feature to receive results.

        :rtype: list[ModeManagementFeature]
        """
        url = self.ep('settings/modeManagement/features')
        data = super().get(url)
        r = TypeAdapter(list[ModeManagementFeature]).validate_python(data['features'])
        return r

    def switch_mode_multiple_features(self, feature_ids: list[str], operating_mode_name: str):
        """
        Switch Mode for Multiple Features

        Switches the operating mode for multiple features simultaneously by specifying a common mode name. This API
        accepts a list of feature IDs and sets all of them to the specified operating mode, provided that mode exists
        for all features.

        This bulk operation is particularly useful for coordinating operational changes across an organization, such as
        activating holiday modes, emergency procedures, or after-hours configurations across multiple Auto Attendants,
        Call Queues, and Hunt Groups at once.

        This API requires a user auth token with the `spark:telephony_config_write` scope. The authenticated user must
        be a mode manager for all specified features.

        :param feature_ids: List of feature IDs to switch mode
        :type feature_ids: list[str]
        :param operating_mode_name: Name of the common operating mode to be set as current operating mode
        :type operating_mode_name: str
        :rtype: None
        """
        body = dict()
        body['featureIds'] = feature_ids
        body['operatingModeName'] = operating_mode_name
        url = self.ep('settings/modeManagement/features/actions/switchMode/invoke')
        super().post(url, json=body)

    def get_common_modes(self, feature_ids: list[str]) -> list[str]:
        """
        Get Common Modes

        Retrieves a list of common operating mode names that are shared across multiple specified features. This API
        accepts a list of feature IDs and returns only the mode names that exist in all of the specified features,
        allowing managers to switch multiple features to the same mode simultaneously.

        Common modes are useful when you need to coordinate operational changes across multiple features. For example,
        switching an entire office to "Holiday" mode across all Auto Attendants and Call Queues at once.

        This API requires a user auth token with the `spark:telephony_config_read` scope. The authenticated user must
        be a mode manager for the specified features.

        :param feature_ids: List of feature IDs (comma-separated) for auto attendants, call queues, or hunt groups
        :type feature_ids: list[str]
        :rtype: list[str]
        """
        params = {}
        params['featureIds'] = ','.join(feature_ids)
        url = self.ep('settings/modeManagement/features/commonModes')
        data = super().get(url, params=params)
        r = data['commonModeNames']
        return r

    def feature_get(self, feature_id: str) -> FeatureDetail:
        """
        Get Mode Management Feature

        Retrieves detailed information about a specific mode management feature including its current operating mode
        and exception status. This API provides the feature's ID, name, type, current operating mode ID, and whether
        it is currently in an exception mode.

        Exception mode indicates that the feature has been manually switched to a different mode than what its schedule
        dictates. This information is critical for mode managers to understand the current state of their features.

        This API requires a user auth token with the `spark:telephony_config_read` scope. The authenticated user must
        be a mode manager for the specified feature.

        :param feature_id: Unique identifier for the feature.
        :type feature_id: str
        :rtype: :class:`FeatureDetail`
        """
        url = self.ep(f'settings/modeManagement/features/{feature_id}')
        data = super().get(url)
        r = FeatureDetail.model_validate(data)
        return r

    def extend_mode(self, feature_id: str, operating_mode_id: str, extension_time: int = None):
        """
        Extend Current Operating Mode Duration

        Extends the duration of the current operating mode by adding additional time before it expires or reverts to
        scheduled operation. This API allows managers to prolong a temporary mode change without having to switch
        modes again.

        Extension time can be specified in 30-minute increments up to 720 minutes (12 hours). If no extension time is
        provided, the mode is extended with a manual switchback exception, meaning it will remain active until
        manually changed.

        This API requires a user auth token with the `spark:telephony_config_write` scope. The authenticated user must
        be a mode manager for the specified feature.

        :param feature_id: Unique identifier for the feature.
        :type feature_id: str
        :param operating_mode_id: Unique identifier for the operating mode for which the extension is being configured.
        :type operating_mode_id: str
        :param extension_time: Extension time in minutes (must be multiple of 30). If not sent, mode is extended with
            manual switch back exception
        :type extension_time: int
        :rtype: None
        """
        body = dict()
        body['operatingModeId'] = operating_mode_id
        if extension_time is not None:
            body['extensionTime'] = extension_time
        url = self.ep(f'settings/modeManagement/features/{feature_id}/actions/extendMode/invoke')
        super().post(url, json=body)

    def switch_mode_for_feature(
        self, feature_id: str, operating_mode_id: str, is_manual_switchback_enabled: bool = None
    ):
        """
        Switch Mode for Single Feature

        Switches the operating mode for a single feature to a specified mode, either temporarily or with manual
        switchback. This API creates an exception to the feature's normal scheduled operation, allowing managers to
        manually control the feature's behavior.

        You can configure whether the mode switch is temporary (automatically reverts based on schedule) or requires
        manual switchback. This is useful for handling unexpected situations like emergency closures, special events,
        or unscheduled breaks.

        This API requires a user auth token with the `spark:telephony_config_write` scope. The authenticated user must
        be a mode manager for the specified feature.

        :param feature_id: Unique identifier for the feature.
        :type feature_id: str
        :param operating_mode_id: Operating mode ID to switch to
        :type operating_mode_id: str
        :param is_manual_switchback_enabled: Determines if switch back will be manual (if true) or automatic (if false
            or omitted from request)
        :type is_manual_switchback_enabled: bool
        :rtype: None
        """
        body = dict()
        body['operatingModeId'] = operating_mode_id
        if is_manual_switchback_enabled is not None:
            body['isManualSwitchbackEnabled'] = is_manual_switchback_enabled
        url = self.ep(f'settings/modeManagement/features/{feature_id}/actions/switchMode/invoke')
        super().post(url, json=body)

    def switch_to_normal_operation(self, feature_id: str):
        """
        Switch to Normal Operation

        Switches the feature back to its normal scheduled operation mode, removing any manual exceptions or overrides
        that may be active. This returns the feature to operating according to its configured time schedules.

        This operation is useful when a temporary manual mode change (exception) is no longer needed and you want to
        restore automatic schedule-based operation. It effectively cancels any active manual mode switches.

        This API requires a user auth token with the `spark:telephony_config_write` scope. The authenticated user must
        be a mode manager for the specified feature.

        :param feature_id: Unique identifier for the feature.
        :type feature_id: str
        :rtype: None
        """
        url = self.ep(f'settings/modeManagement/features/{feature_id}/actions/switchToNormalOperation/invoke')
        super().post(url)

    def get_operating_mode(self, feature_id: str, mode_id: str) -> OperatingModeDetail:
        """
        Get Operating Mode

        Retrieves detailed information about a specific operating mode for a feature, including the mode's ID and name.
        This API allows managers to get the details of any operating mode configured for a feature.

        Operating modes define different configurations for how a feature behaves (e.g., business hours routing vs.
        after-hours routing). Each mode has a unique ID and a descriptive name that helps managers identify its
        purpose.

        This API requires a user auth token with the `spark:telephony_config_read` scope. The authenticated user must
        be a mode manager for the specified feature.

        :param feature_id: Unique identifier for the feature.
        :type feature_id: str
        :param mode_id: Unique identifier for the operating mode.
        :type mode_id: str
        :rtype: :class:`OperatingModeDetail`
        """
        url = self.ep(f'settings/modeManagement/features/{feature_id}/modes/{mode_id}')
        data = super().get(url)
        r = OperatingModeDetail.model_validate(data)
        return r

    def get_normal_operation_mode(self, feature_id: str) -> str:
        """
        Get Normal Operation Mode

        Retrieves the current normal operating mode that the feature is scheduled to be in based on its time schedules.
        This represents the mode the feature would be in if no manual exceptions or overrides were active.

        The normal operation mode is determined by the feature's configured schedules and may differ from the actual
        current operating mode if a manual exception has been applied. This API helps managers understand what the
        scheduled behavior is versus the actual current state.

        This API requires a user auth token with the `spark:telephony_config_read` scope. The authenticated user must
        be a mode manager for the specified feature.

        :param feature_id: Unique identifier for the feature.
        :type feature_id: str
        :rtype: str
        """
        url = self.ep(f'settings/modeManagement/features/{feature_id}/normalOperationMode')
        data = super().get(url)
        r = data['operatingModeId']
        return r

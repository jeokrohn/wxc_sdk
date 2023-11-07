from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CreateOrUpdateTrackingCodeObject', 'GetTrackingCodeForUserObject', 'GetTrackingCodeItemForUserObject',
            'GetTrackingCodeObject', 'GetTrackingCodeObjectHostProfileCode', 'GetTrackingCodeObjectInputMode',
            'GetTrackingCodesObject', 'OptionsForTrackingCodeObject', 'ScheduleStartCodeObject',
            'ScheduleStartCodeObjectService', 'ScheduleStartCodeObjectType', 'UpdateTrackingCodeForUserObject',
            'UpdateTrackingCodeItemForUserObject']


class OptionsForTrackingCodeObject(ApiModel):
    #: The value of a tracking code option.
    value: Optional[str] = None
    #: Whether or not the option is the default option of a tracking code.
    default_value: Optional[bool] = None


class GetTrackingCodeObjectInputMode(str, Enum):
    #: Text input.
    text = 'text'
    #: Drop down list which requires `options`.
    select = 'select'
    #: Both text input and select from list.
    editable_select = 'editableSelect'
    #: An input method is only available for the host profile and sign-up pages.
    host_profile_select = 'hostProfileSelect'
    none_ = 'none'


class GetTrackingCodeObjectHostProfileCode(str, Enum):
    #: Available to be chosen but not compulsory.
    optional = 'optional'
    #: Officially compulsory.
    required = 'required'
    #: The value is set by admin.
    admin_set = 'adminSet'
    #: The value cannot be used.
    not_used = 'notUsed'
    none_ = 'none'


class ScheduleStartCodeObjectService(str, Enum):
    #: Tracking codes apply to all services.
    all = 'All'
    #: Users can set tracking codes when scheduling a meeting.
    meeting_center = 'MeetingCenter'
    #: Users can set tracking codes when scheduling an event.
    event_center = 'EventCenter'
    #: Users can set tracking codes when scheduling a training session.
    training_center = 'TrainingCenter'
    #: Users can set tracking codes when scheduling a support meeting.
    support_center = 'SupportCenter'
    none_ = 'none'


class ScheduleStartCodeObjectType(str, Enum):
    #: Available to be chosen but not compulsory.
    optional = 'optional'
    #: Officially compulsory.
    required = 'required'
    #: The value is set by admin. This value only applies when `hostProfileCode` is `adminSet`.
    admin_set = 'adminSet'
    #: The value cannot be used.
    not_used = 'notUsed'
    #: This value only applies to the service of `All`. When the type of `All` for a tracking code is `notApplicable`,
    #: there are different types for different services. For example, `required` for `MeetingCenter`, `optional` for
    #: `EventCenter` and `notUsed` for others.
    not_applicable = 'notApplicable'
    none_ = 'none'


class ScheduleStartCodeObject(ApiModel):
    #: Service for schedule or sign up pages
    service: Optional[ScheduleStartCodeObjectService] = None
    #: Type for meeting scheduler or meeting start pages.
    type: Optional[ScheduleStartCodeObjectType] = None


class GetTrackingCodeObject(ApiModel):
    #: Unique identifier for tracking code.
    #: example: 1
    id: Optional[datetime] = None
    #: Name for tracking code.
    #: example: Department
    name: Optional[str] = None
    #: Site URL for the tracking code.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: Tracking code option list.
    options: Optional[list[OptionsForTrackingCodeObject]] = None
    #: An option for how an admin user can provide a code value.
    input_mode: Optional[GetTrackingCodeObjectInputMode] = None
    #: Type for the host profile.
    host_profile_code: Optional[GetTrackingCodeObjectHostProfileCode] = None
    #: Specify how tracking codes are used for each service on the meeting scheduler or meeting start pages.
    schedule_start_codes: Optional[list[ScheduleStartCodeObject]] = None


class GetTrackingCodesObject(ApiModel):
    #: Tracking codes information.
    items: Optional[list[GetTrackingCodeObject]] = None


class CreateOrUpdateTrackingCodeObject(ApiModel):
    #: Name for tracking code. The name cannot be empty and the maximum size is 120 characters.
    #: example: Department
    name: Optional[str] = None
    #: Site URL for the tracking code.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: Tracking code option list. The maximum size of `options` is 500.
    options: Optional[list[OptionsForTrackingCodeObject]] = None
    #: Select an option for how users can provide a code value. Please note that if users set `inputMode` as
    #: `hostProfileSelect`, `scheduleStartCode` should be `null`, which means `hostProfileSelect` only applies to
    #: "Host Profile".
    input_mode: Optional[GetTrackingCodeObjectInputMode] = None
    #: Type for the host profile.
    host_profile_code: Optional[GetTrackingCodeObjectHostProfileCode] = None
    #: Specify how tracking codes are used for each service on the meeting scheduler or meeting start pages. The
    #: maximum size of `scheduleStartCodes` is 5.
    schedule_start_codes: Optional[list[ScheduleStartCodeObject]] = None


class GetTrackingCodeItemForUserObject(ApiModel):
    #: Unique identifier for tracking code.
    #: example: 1
    id: Optional[datetime] = None
    #: Name for tracking code.
    #: example: Department
    name: Optional[str] = None
    #: Value for tracking code.
    value: Optional[str] = None


class GetTrackingCodeForUserObject(ApiModel):
    #: Site URL for the tracking code.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: Unique identifier for the user.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xOGJiOWNjMC0zMWM2LTQ3MzYtYmE4OC0wMDk5ZmQzNDNmODE
    person_id: Optional[str] = None
    #: Email address for the user.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Tracking code information.
    tracking_codes: Optional[list[GetTrackingCodeItemForUserObject]] = None


class UpdateTrackingCodeItemForUserObject(ApiModel):
    #: Name for tracking code. The name cannot be empty and the maximum size is 120 characters.
    #: example: Department
    name: Optional[str] = None
    #: Value for tracking code. `value` cannot be empty and the maximum size is 120 characters.
    value: Optional[str] = None


class UpdateTrackingCodeForUserObject(ApiModel):
    #: Site URL for the tracking code.
    #: example: example.webex.com
    site_url: Optional[str] = None
    #: Unique identifier for the user. At least one parameter of `personId` or `email` is required. `personId` must
    #: precede `email` if both are specified.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xOGJiOWNjMC0zMWM2LTQ3MzYtYmE4OC0wMDk5ZmQzNDNmODE
    person_id: Optional[str] = None
    #: Email address for the user. At least one parameter of `personId` or `email` is required. `personId` must precede
    #: `email` if both are specified.
    #: example: john.andersen@example.com
    email: Optional[str] = None
    #: Tracking code information for updates.
    tracking_codes: Optional[list[UpdateTrackingCodeItemForUserObject]] = None


class TrackingCodesApi(ApiChild, base='admin/meeting'):
    """
    Tracking Codes
    
    Tracking codes are alphanumeric codes that identify categories of users on a Webex site. With tracking codes, you
    can analyze usage by various groups within an organization.
    
    The authenticated user calling this API must have an Administrator role with the `meeting:admin_schedule_write` and
    `meeting:admin_schedule_read` scopes.
    """
    ...
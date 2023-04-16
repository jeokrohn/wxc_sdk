from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['CreateTrackingCodeBody', 'GetTrackingCodeItemForUserObject', 'GetTrackingCodeObject',
           'GetUserTrackingCodesResponse', 'HostProfileCode', 'InputMode', 'ListTrackingCodesResponse',
           'OptionsForTrackingCodeObject', 'ScheduleStartCodeObject', 'Service', 'TrackingCodesApi', 'Type',
           'UpdateTrackingCodeItemForUserObject']


class OptionsForTrackingCodeObject(ApiModel):
    #: The value of a tracking code option.
    value: Optional[str]
    #: Whether or not the option is the default option of a tracking code.
    default_value: Optional[bool]


class InputMode(str, Enum):
    #: Text input.
    text = 'text'
    #: Drop down list which requires options.
    select = 'select'
    #: Both text input and select from list.
    editable_select = 'editableSelect'
    #: An input method is only available for the host profile and sign-up pages.
    host_profile_select = 'hostProfileSelect'


class HostProfileCode(str, Enum):
    #: Available to be chosen but not compulsory.
    optional = 'optional'
    #: Officially compulsory.
    required = 'required'
    #: The value is set by admin.
    admin_set = 'adminSet'
    #: The value cannot be used.
    not_used = 'notUsed'


class Service(str, Enum):
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


class Type(HostProfileCode):
    #: This value only applies to the service of All. When the type of All for a tracking code is notApplicable, there
    #: are different types for different services. For example, required for MeetingCenter, optional for EventCenter
    #: and notUsed for others.
    not_applicable = 'notApplicable'


class ScheduleStartCodeObject(ApiModel):
    #: Service for schedule or sign up pages
    service: Optional[Service]
    #: Type for meeting scheduler or meeting start pages.
    type: Optional[Type]


class GetTrackingCodeObject(ApiModel):
    #: Unique identifier for tracking code.
    id: Optional[str]
    #: Name for tracking code.
    name: Optional[str]
    #: Site URL for the tracking code.
    site_url: Optional[str]
    #: Tracking code option list.
    options: Optional[list[OptionsForTrackingCodeObject]]
    #: An option for how an admin user can provide a code value.
    input_mode: Optional[InputMode]
    #: Type for the host profile.
    host_profile_code: Optional[HostProfileCode]
    #: Specify how tracking codes are used for each service on the meeting scheduler or meeting start pages.
    schedule_start_codes: Optional[list[ScheduleStartCodeObject]]


class CreateTrackingCodeBody(ApiModel):
    #: Name for tracking code. The name cannot be empty and the maximum size is 120 characters.
    name: Optional[str]
    #: Site URL for the tracking code.
    site_url: Optional[str]
    #: Tracking code option list. The maximum size of options is 500.
    options: Optional[list[OptionsForTrackingCodeObject]]
    #: Select an option for how users can provide a code value. Please note that if users set inputMode as
    #: hostProfileSelect, scheduleStartCode should be null, which means hostProfileSelect only applies to "Host
    #: Profile".
    input_mode: Optional[InputMode]
    #: Type for the host profile.
    host_profile_code: Optional[HostProfileCode]
    #: Specify how tracking codes are used for each service on the meeting scheduler or meeting start pages. The
    #: maximum size of scheduleStartCodes is 5.
    schedule_start_codes: Optional[list[ScheduleStartCodeObject]]


class UpdateTrackingCodeItemForUserObject(ApiModel):
    #: Name for tracking code. The name cannot be empty and the maximum size is 120 characters.
    name: Optional[str]
    #: Value for tracking code. value cannot be empty and the maximum size is 120 characters.
    value: Optional[str]


class GetTrackingCodeItemForUserObject(UpdateTrackingCodeItemForUserObject):
    #: Unique identifier for tracking code.
    id: Optional[str]


class GetUserTrackingCodesResponse(ApiModel):
    #: Site URL for the tracking code.
    site_url: Optional[str]
    #: Unique identifier for the user.
    person_id: Optional[str]
    #: Email address for the user.
    email: Optional[str]
    #: Tracking code information.
    tracking_codes: Optional[list[GetTrackingCodeItemForUserObject]]


class ListTrackingCodesResponse(ApiModel):
    #: Tracking codes information.
    items: Optional[list[GetTrackingCodeObject]]


class UpdateUserTrackingCodesBody(ApiModel):
    #: Site URL for the tracking code.
    site_url: Optional[str]
    #: Unique identifier for the user. At least one parameter of personId or email is required. personId must precede
    #: email if both are specified.
    person_id: Optional[str]
    #: Email address for the user. At least one parameter of personId or email is required. personId must precede email
    #: if both are specified.
    email: Optional[str]
    #: Tracking code information for updates.
    tracking_codes: Optional[list[UpdateTrackingCodeItemForUserObject]]


class TrackingCodesApi(ApiChild, base=''):
    """
    Tracking codes are alphanumeric codes that identify categories of users on a Webex site. With tracking codes, you
    can analyze usage by various groups within an organization.
    The authenticated user calling this API must have an Administrator role with the meeting:admin_schedule_write and
    meeting:admin_schedule_read scopes.
    """

    def list_codes(self, site_url: str = None) -> list[GetTrackingCodeObject]:
        """
        Lists tracking codes on a site by an admin user.

        :param site_url: URL of the Webex site which the API retrieves the tracking code from. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and preferred
            sites of a user can be retrieved by the Get Site List API.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/list-tracking-codes
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('https: //webexapis.com/v1/admin/meeting/config/trackingCodes')
        data = super().get(url=url, params=params)
        return parse_obj_as(list[GetTrackingCodeObject], data["items"])

    def code(self, tracking_code_id: str, site_url: str = None) -> GetTrackingCodeObject:
        """
        Retrieves details for a tracking code by an admin user.

        :param tracking_code_id: Unique identifier for the tracking code whose details are being requested.
        :type tracking_code_id: str
        :param site_url: URL of the Webex site which the API retrieves the tracking code from. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and the preferred
            sites of a user can be retrieved by the Get Site List API.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/get-a-tracking-code
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep(f'https: //webexapis.com/v1/admin/meeting/config/trackingCodes/{tracking_code_id}')
        data = super().get(url=url, params=params)
        return GetTrackingCodeObject.parse_obj(data)

    def create_code(self, name: str, site_url: str, options: OptionsForTrackingCodeObject, input_mode: InputMode, host_profile_code: HostProfileCode, schedule_start_codes: ScheduleStartCodeObject) -> GetTrackingCodeObject:
        """
        Create a new tracking code by an admin user.

        :param name: Name for tracking code. The name cannot be empty and the maximum size is 120 characters.
        :type name: str
        :param site_url: Site URL for the tracking code.
        :type site_url: str
        :param options: Tracking code option list. The maximum size of options is 500.
        :type options: OptionsForTrackingCodeObject
        :param input_mode: Select an option for how users can provide a code value. Please note that if users set
            inputMode as hostProfileSelect, scheduleStartCode should be null, which means hostProfileSelect only
            applies to "Host Profile".
        :type input_mode: InputMode
        :param host_profile_code: Type for the host profile.
        :type host_profile_code: HostProfileCode
        :param schedule_start_codes: Specify how tracking codes are used for each service on the meeting scheduler or
            meeting start pages. The maximum size of scheduleStartCodes is 5.
        :type schedule_start_codes: ScheduleStartCodeObject

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/create-a-tracking-code
        """
        body = CreateTrackingCodeBody()
        if name is not None:
            body.name = name
        if site_url is not None:
            body.site_url = site_url
        if options is not None:
            body.options = options
        if input_mode is not None:
            body.input_mode = input_mode
        if host_profile_code is not None:
            body.host_profile_code = host_profile_code
        if schedule_start_codes is not None:
            body.schedule_start_codes = schedule_start_codes
        url = self.ep('https: //webexapis.com/v1/admin/meeting/config/trackingCodes')
        data = super().post(url=url, data=body.json())
        return GetTrackingCodeObject.parse_obj(data)

    def update_code(self, name: str, site_url: str, options: OptionsForTrackingCodeObject, input_mode: InputMode, host_profile_code: HostProfileCode, schedule_start_codes: ScheduleStartCodeObject) -> GetTrackingCodeObject:
        """
        Updates details for a tracking code by an admin user.

        :param name: Name for tracking code. The name cannot be empty and the maximum size is 120 characters.
        :type name: str
        :param site_url: Site URL for the tracking code.
        :type site_url: str
        :param options: Tracking code option list. The maximum size of options is 500.
        :type options: OptionsForTrackingCodeObject
        :param input_mode: Select an option for how users can provide a code value. Please note that if users set
            inputMode as hostProfileSelect, scheduleStartCode should be null, which means hostProfileSelect only
            applies to "Host Profile".
        :type input_mode: InputMode
        :param host_profile_code: Type for the host profile.
        :type host_profile_code: HostProfileCode
        :param schedule_start_codes: Specify how tracking codes are used for each service on the meeting scheduler or
            meeting start pages. The maximum size of scheduleStartCodes is 5.
        :type schedule_start_codes: ScheduleStartCodeObject

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/update-a-tracking-code
        """
        body = CreateTrackingCodeBody()
        if name is not None:
            body.name = name
        if site_url is not None:
            body.site_url = site_url
        if options is not None:
            body.options = options
        if input_mode is not None:
            body.input_mode = input_mode
        if host_profile_code is not None:
            body.host_profile_code = host_profile_code
        if schedule_start_codes is not None:
            body.schedule_start_codes = schedule_start_codes
        url = self.ep('https: //webexapis.com/v1/admin/meeting/config/trackingCodes/{trackingCodeId}')
        data = super().put(url=url, data=body.json())
        return GetTrackingCodeObject.parse_obj(data)

    def delete_code(self, tracking_code_id: str, site_url: str):
        """
        Deletes a tracking code by an admin user.

        :param tracking_code_id: Unique identifier for the tracking code to be deleted.
        :type tracking_code_id: str
        :param site_url: URL of the Webex site from which the API deletes the tracking code. All available Webex sites
            and preferred sites of a user can be retrieved by the Get Site List API.
        :type site_url: str

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/delete-a-tracking-code
        """
        params = {}
        params['siteUrl'] = site_url
        url = self.ep(f'https: //webexapis.com/v1/admin/meeting/config/trackingCodes/{tracking_code_id}')
        super().delete(url=url, params=params)
        return

    def user_codes(self, site_url: str = None, person_id: str = None) -> GetUserTrackingCodesResponse:
        """
        Lists user's tracking codes by an admin user.

        :param site_url: URL of the Webex site from which the API retrieves the tracking code. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and preferred
            sites of a user can be retrieved by the Get Site List API.
        :type site_url: str
        :param person_id: Unique identifier for the user whose tracking codes are being retrieved. The admin user can
            specify the personId of a user on a site they manage and the API returns details for the user's tracking
            codes. At least one parameter of personId or email is required.
        :type person_id: str

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/get-user-tracking-codes
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        if person_id is not None:
            params['personId'] = person_id
        url = self.ep('https: //webexapis.com/v1/admin/meeting/userconfig/trackingCodes')
        data = super().get(url=url, params=params)
        return GetUserTrackingCodesResponse.parse_obj(data)

    def update_user_codes(self, site_url: str, person_id: str = None, email: str = None, tracking_codes: UpdateTrackingCodeItemForUserObject = None) -> GetUserTrackingCodesResponse:
        """
        Updates tracking codes for a specified user by an admin user.

        :param site_url: Site URL for the tracking code.
        :type site_url: str
        :param person_id: Unique identifier for the user. At least one parameter of personId or email is required.
            personId must precede email if both are specified.
        :type person_id: str
        :param email: Email address for the user. At least one parameter of personId or email is required. personId
            must precede email if both are specified.
        :type email: str
        :param tracking_codes: Tracking code information for updates.
        :type tracking_codes: UpdateTrackingCodeItemForUserObject

        documentation: https://developer.webex.com/docs/api/v1/tracking-codes/update-user-tracking-codes
        """
        body = UpdateUserTrackingCodesBody()
        if site_url is not None:
            body.site_url = site_url
        if person_id is not None:
            body.person_id = person_id
        if email is not None:
            body.email = email
        if tracking_codes is not None:
            body.tracking_codes = tracking_codes
        url = self.ep('https: //webexapis.com/v1/admin/meeting/userconfig/trackingCodes')
        data = super().put(url=url, data=body.json())
        return GetUserTrackingCodesResponse.parse_obj(data)

from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['GetTrackingCodeForUserObject', 'GetTrackingCodeItemForUserObject', 'GetTrackingCodeObject',
           'GetTrackingCodeObjectHostProfileCode', 'GetTrackingCodeObjectInputMode', 'OptionsForTrackingCodeObject',
           'ScheduleStartCodeObject', 'ScheduleStartCodeObjectService', 'ScheduleStartCodeObjectType',
           'TrackingCodesApi', 'UpdateTrackingCodeItemForUserObject']


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


class GetTrackingCodeObjectHostProfileCode(str, Enum):
    #: Available to be chosen but not compulsory.
    optional = 'optional'
    #: Officially compulsory.
    required = 'required'
    #: The value is set by admin.
    admin_set = 'adminSet'
    #: The value cannot be used.
    not_used = 'notUsed'


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


class ScheduleStartCodeObject(ApiModel):
    #: Service for schedule or sign up pages
    service: Optional[ScheduleStartCodeObjectService] = None
    #: Type for meeting scheduler or meeting start pages.
    type: Optional[ScheduleStartCodeObjectType] = None


class GetTrackingCodeObject(ApiModel):
    #: Unique identifier for tracking code.
    #: example: 1
    id: Optional[str] = None
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


class GetTrackingCodeItemForUserObject(ApiModel):
    #: Unique identifier for tracking code.
    #: example: 1
    id: Optional[str] = None
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


class TrackingCodesApi(ApiChild, base='admin/meeting'):
    """
    Tracking Codes
    
    Tracking codes are alphanumeric codes that identify categories of users on a Webex site. With tracking codes, you
    can analyze usage by various groups within an organization.
    
    The authenticated user calling this API must have an Administrator role with the `meeting:admin_schedule_write` and
    `meeting:admin_schedule_read` scopes.
    """

    def list_tracking_codes(self, site_url: str = None) -> list[GetTrackingCodeObject]:
        """
        List Tracking Codes

        Lists tracking codes on a site by an admin user.

        * If `siteUrl` is specified, tracking codes of the specified site will be listed; otherwise, tracking codes of
        the user's preferred site will be listed. All available Webex sites and the preferred sites of a user can be
        retrieved by the `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        * Admins can switch any Control Hub managed site from using classic tracking codes to mapped tracking codes in
        Control Hub. This is a one-time irreversible operation. Once the tracking codes are mapped to custom or user
        profile attributes, the response returns the mapped tracking codes.

        :param site_url: URL of the Webex site which the API retrieves the tracking code from. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and preferred
            sites of a user can be retrieved by the `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :rtype: list[GetTrackingCodeObject]
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep('config/trackingCodes')
        data = super().get(url, params=params)
        r = TypeAdapter(list[GetTrackingCodeObject]).validate_python(data['items'])
        return r

    def get_a_tracking_code(self, tracking_code_id: str, site_url: str = None) -> GetTrackingCodeObject:
        """
        Get a Tracking Code

        Retrieves details for a tracking code by an admin user.

        * If `siteUrl` is specified, the tracking code is retrieved from the specified site; otherwise, the tracking
        code is retrieved from the user's preferred site. All available Webex sites and the preferred sites of a user
        can be retrieved by the `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        * Admins can switch any Control Hub managed site from using classic tracking codes to mapped tracking codes in
        Control Hub, this is a one-time irreversible operation. Once the tracking codes are mapped to custom or user
        profile attributes, the response returns details for a mapped tracking code.

        :param tracking_code_id: Unique identifier for the tracking code whose details are being requested.
        :type tracking_code_id: str
        :param site_url: URL of the Webex site which the API retrieves the tracking code from. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and the
            preferred sites of a user can be retrieved by the `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :rtype: :class:`GetTrackingCodeObject`
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        url = self.ep(f'config/trackingCodes/{tracking_code_id}')
        data = super().get(url, params=params)
        r = GetTrackingCodeObject.model_validate(data)
        return r

    def create_a_tracking_code(self, name: str, site_url: str, options: list[OptionsForTrackingCodeObject],
                               input_mode: GetTrackingCodeObjectInputMode,
                               host_profile_code: GetTrackingCodeObjectHostProfileCode,
                               schedule_start_codes: list[ScheduleStartCodeObject]) -> GetTrackingCodeObject:
        """
        Create a Tracking Code

        Create a new tracking code by an admin user.

        * The `siteUrl` is required. The operation creates a tracking code for the specified site. All or a user's
        available Webex sites can be retrieved by the `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        * The `inputMode` of `hostProfileSelect` is only available for a host profile and sign-up pages and does not
        apply to the meeting scheduler page or the meeting start page. The value for `scheduleStartCodes` must be
        `null` or the value for all services must be `notUsed` when the `inputMode` is `hostProfileSelect`.

        * The `hostProfileCode` of `required` is only allowed for a Site Admin managed site, and not for a Control Hub
        managed site.

        * When the `hostProfileCode` is `adminSet`, only `adminSet`, `notUsed`, and `notApplicable` are available for
        the types of `scheduleStartCodes`. When the `hostProfileCode` is not `adminSet`, only `optional`, `required`,
        `notUsed`, and `notApplicable` are available for `scheduleStartCodes`.

        * If the type of the `All` service has a value other than `notApplicable`, and another service, e.g.
        `EventCenter`, is missing from the `scheduleStartCodes`, then the type of this missing `EventCenter` service
        shares the same type as the `All` service. If the type of `All` service has a value other than
        `notApplicable`, and another service, e.g. `EventCenter`, has a type, then the type specified should be the
        same as the `All` service.

        * If the `All` service is missing from the `scheduleStartCodes`, any of the other four services, e.g.
        `EventCenter`, have a default type of `notUsed` if it is also missing from the `scheduleStartCodes`.

        * Admins can switch any Control Hub managed site from using classic tracking codes to mapped tracking codes in
        Control Hub, this is a one-time irreversible operation. Once the tracking codes are mapped to custom or user
        profile attributes, they cannot create tracking codes when the mapping process is in progress or the mapping
        process is completed.

        :param name: Name for tracking code. The name cannot be empty and the maximum size is 120 characters.
        :type name: str
        :param site_url: Site URL for the tracking code.
        :type site_url: str
        :param options: Tracking code option list. The maximum size of `options` is 500.
        :type options: list[OptionsForTrackingCodeObject]
        :param input_mode: Select an option for how users can provide a code value. Please note that if users set
            `inputMode` as `hostProfileSelect`, `scheduleStartCode` should be `null`, which means `hostProfileSelect`
            only applies to "Host Profile".
        :type input_mode: GetTrackingCodeObjectInputMode
        :param host_profile_code: Type for the host profile.
        :type host_profile_code: GetTrackingCodeObjectHostProfileCode
        :param schedule_start_codes: Specify how tracking codes are used for each service on the meeting scheduler or
            meeting start pages. The maximum size of `scheduleStartCodes` is 5.
        :type schedule_start_codes: list[ScheduleStartCodeObject]
        :rtype: :class:`GetTrackingCodeObject`
        """
        body = dict()
        body['name'] = name
        body['siteUrl'] = site_url
        body['options'] = TypeAdapter(list[OptionsForTrackingCodeObject]).dump_python(options, mode='json', by_alias=True, exclude_none=True)
        body['inputMode'] = enum_str(input_mode)
        body['hostProfileCode'] = enum_str(host_profile_code)
        body['scheduleStartCodes'] = TypeAdapter(list[ScheduleStartCodeObject]).dump_python(schedule_start_codes, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('config/trackingCodes')
        data = super().post(url, json=body)
        r = GetTrackingCodeObject.model_validate(data)
        return r

    def update_a_tracking_code(self, name: str, site_url: str, options: list[OptionsForTrackingCodeObject],
                               input_mode: GetTrackingCodeObjectInputMode,
                               host_profile_code: GetTrackingCodeObjectHostProfileCode,
                               schedule_start_codes: list[ScheduleStartCodeObject]) -> GetTrackingCodeObject:
        """
        Update a Tracking Code

        Updates details for a tracking code by an admin user.

        * The `siteUrl` is required. The operation updates a tracking code for the specified site. All of a user's
        available Webex sites can be retrieved by the `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        * The `inputMode` of `hostProfileSelect` is only available for the host profile and sign-up pages and it
        doesn't apply to the meeting scheduler page or meeting start page. Therefore, `scheduleStartCodes` must be
        `null` or type of all services must be `notUsed` when the `inputMode` is `hostProfileSelect`.

        * Currently, the `hostProfileCode` of `required` is only allowed for a Site Admin managed site, and not allowed
        for a Control Hub managed site.

        * When the `hostProfileCode` is `adminSet`, only `adminSet`, `notUsed` and `notApplicable` are available for
        the types of `scheduleStartCodes`. When the `hostProfileCode` is not `adminSet`, only `optional`, `required`,
        `notUsed` and `notApplicable` are available for types of `scheduleStartCodes`.

        * If the type of the `All` service has a value other than `notApplicable`, and another service, e.g.
        `EventCenter`, is missing from the `scheduleStartCodes`, then the type of this missing `EventCenter` service
        shares the same type as the `All` service silently. If the type of `All` service has a value other than
        `notApplicable`, and another service, e.g. `EventCenter`, has a type, then the type specified should be the
        same as the `All` service.

        * If the `All` service is missing from the `scheduleStartCodes`, any of the other four services, e.g.
        `EventCenter`, has a default type of `notUsed` if that service is also missing from the `scheduleStartCodes`.

        * Admins can switch any Control Hub managed site from using classic tracking codes to mapped tracking codes in
        Control Hub, this is a one-time irreversible operation. Once the tracking codes are mapped to custom or user
        profile attributes, they cannot update tracking codes when the mapping process is in progress or the mapping
        process is completed.

        :param name: Name for tracking code. The name cannot be empty and the maximum size is 120 characters.
        :type name: str
        :param site_url: Site URL for the tracking code.
        :type site_url: str
        :param options: Tracking code option list. The maximum size of `options` is 500.
        :type options: list[OptionsForTrackingCodeObject]
        :param input_mode: Select an option for how users can provide a code value. Please note that if users set
            `inputMode` as `hostProfileSelect`, `scheduleStartCode` should be `null`, which means `hostProfileSelect`
            only applies to "Host Profile".
        :type input_mode: GetTrackingCodeObjectInputMode
        :param host_profile_code: Type for the host profile.
        :type host_profile_code: GetTrackingCodeObjectHostProfileCode
        :param schedule_start_codes: Specify how tracking codes are used for each service on the meeting scheduler or
            meeting start pages. The maximum size of `scheduleStartCodes` is 5.
        :type schedule_start_codes: list[ScheduleStartCodeObject]
        :rtype: :class:`GetTrackingCodeObject`
        """
        body = dict()
        body['name'] = name
        body['siteUrl'] = site_url
        body['options'] = TypeAdapter(list[OptionsForTrackingCodeObject]).dump_python(options, mode='json', by_alias=True, exclude_none=True)
        body['inputMode'] = enum_str(input_mode)
        body['hostProfileCode'] = enum_str(host_profile_code)
        body['scheduleStartCodes'] = TypeAdapter(list[ScheduleStartCodeObject]).dump_python(schedule_start_codes, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('config/trackingCodes/{trackingCodeId}')
        data = super().put(url, json=body)
        r = GetTrackingCodeObject.model_validate(data)
        return r

    def delete_a_tracking_code(self, tracking_code_id: str, site_url: str):
        """
        Delete a Tracking Code

        Deletes a tracking code by an admin user.

        * The `siteUrl` is required. The operation deletes a tracking code for the specified site. All of a user's
        available Webex sites can be retrieved by the `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.

        * Admins can switch any Control Hub managed site from using classic tracking codes to mapped tracking codes in
        Control Hub, this is a one-time irreversible operation. Once the tracking codes are mapped to custom or user
        profile attributes, they cannot delete tracking codes when the mapping process is in progress or the mapping
        process is completed.

        :param tracking_code_id: Unique identifier for the tracking code to be deleted.
        :type tracking_code_id: str
        :param site_url: URL of the Webex site from which the API deletes the tracking code. All available Webex sites
            and preferred sites of a user can be retrieved by the `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :rtype: None
        """
        params = {}
        params['siteUrl'] = site_url
        url = self.ep(f'config/trackingCodes/{tracking_code_id}')
        super().delete(url, params=params)

    def get_user_tracking_codes(self, site_url: str = None, person_id: str = None) -> GetTrackingCodeForUserObject:
        """
        Get User Tracking Codes

        Lists user's tracking codes by an admin user.

        * At least one parameter, either `personId`, or `email` is required. `personId` must come before `email` if
        both are specified. Please note that `email` is specified in the request header.

        * If `siteUrl` is specified, the tracking codes of the specified site will be listed; otherwise, the tracking
        codes of a user's preferred site are listed. All available Webex sites and preferred sites of a user can be
        retrieved by the `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API. Please note that the user here is the admin user who invokes the API, not
        the user specified by `personId` or email.

        * Admins can switch any Control Hub managed site from using classic tracking codes to mapped tracking codes in
        Control Hub, this is a one-time irreversible operation. Once the tracking codes are mapped to custom or user
        profile attributes, the response returns the user's mapped tracking codes.

        #### Request Header

        * `email`: Email address for the user whose tracking codes are being retrieved. The admin users can specify the
        email of a user on a site they manage and the API returns details for the user's tracking codes. At least one
        parameter of `personId` or `email` is required.

        :param site_url: URL of the Webex site from which the API retrieves the tracking code. If not specified, the
            API retrieves the tracking code from the user's preferred site. All available Webex sites and preferred
            sites of a user can be retrieved by the `Get Site List
            <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API.
        :type site_url: str
        :param person_id: Unique identifier for the user whose tracking codes are being retrieved. The admin user can
            specify the `personId` of a user on a site they manage and the API returns details for the user's tracking
            codes. At least one parameter of `personId` or `email` is required.
        :type person_id: str
        :rtype: :class:`GetTrackingCodeForUserObject`
        """
        params = {}
        if site_url is not None:
            params['siteUrl'] = site_url
        if person_id is not None:
            params['personId'] = person_id
        url = self.ep('userconfig/trackingCodes')
        data = super().get(url, params=params)
        r = GetTrackingCodeForUserObject.model_validate(data)
        return r

    def update_user_tracking_codes(self, site_url: str, tracking_codes: list[UpdateTrackingCodeItemForUserObject],
                                   person_id: str = None, email: str = None) -> GetTrackingCodeForUserObject:
        """
        Update User Tracking Codes

        Updates tracking codes for a specified user by an admin user.

        * The `siteUrl` is required. The operation updates a user's tracking code on the specified site. All a user's
        available Webex sites can be retrieved by the `Get Site List
        <https://developer.webex.com/docs/api/v1/meeting-preferences/get-site-list>`_ API. Please note that the user here is the admin
        user who invokes the API, not the user specified by `personId` or `email`.

        * A name that is not found in the site-level tracking codes cannot be set for a user's tracking codes. All
        available site-level tracking codes for a site can be retrieved by the `List Tracking Codes
        <https://developer.webex.com/docs/api/v1/tracking-codes/list-tracking-codes>`_ API.

        * If the `inputMode` of a user's tracking code is `select` or `hostProfileSelect`, its value must be one of the
        site-level options of that tracking code. All available site-level tracking codes for a site can be retrieved
        by the `List Tracking Codes
        <https://developer.webex.com/docs/api/v1/tracking-codes/list-tracking-codes>`_ API.

        * Admins can switch any Control Hub managed site from using classic tracking codes to mapped tracking codes in
        Control Hub, this is a one-time irreversible operation. Once the tracking codes are mapped to custom or user
        profile attributes, they cannot update user's tracking codes when the mapping process is in progress or the
        mapping process is completed.

        :param site_url: Site URL for the tracking code.
        :type site_url: str
        :param tracking_codes: Tracking code information for updates.
        :type tracking_codes: list[UpdateTrackingCodeItemForUserObject]
        :param person_id: Unique identifier for the user. At least one parameter of `personId` or `email` is required.
            `personId` must precede `email` if both are specified.
        :type person_id: str
        :param email: Email address for the user. At least one parameter of `personId` or `email` is required.
            `personId` must precede `email` if both are specified.
        :type email: str
        :rtype: :class:`GetTrackingCodeForUserObject`
        """
        body = dict()
        body['siteUrl'] = site_url
        if person_id is not None:
            body['personId'] = person_id
        if email is not None:
            body['email'] = email
        body['trackingCodes'] = TypeAdapter(list[UpdateTrackingCodeItemForUserObject]).dump_python(tracking_codes, mode='json', by_alias=True, exclude_none=True)
        url = self.ep('userconfig/trackingCodes')
        data = super().put(url, json=body)
        r = GetTrackingCodeForUserObject.model_validate(data)
        return r

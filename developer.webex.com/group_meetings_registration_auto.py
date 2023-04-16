from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['Api', 'Condition', 'CustomizedQuestionForCreateMeeting', 'CustomizedQuestionForGetMeeting',
           'GetRegistrationFormFormeetingResponse', 'Question', 'Result', 'Rules1', 'StandardRegistrationApproveRule',
           'Type']


class Type(str, Enum):
    #: Single line text box.
    single_line_text_box = 'singleLineTextBox'
    #: Multiple line text box.
    multi_line_text_box = 'multiLineTextBox'
    #: Check box which requires options.
    checkbox = 'checkbox'
    #: Drop down list box which requires options.
    dropdown_list = 'dropdownList'
    #: Single radio button which requires options.
    radio_buttons = 'radioButtons'


class Condition(str, Enum):
    #: The content of the answer contains the value.
    contains = 'contains'
    #: The content of the answer does not contain the value
    not_contains = 'notContains'
    #: The content of the answer begins with the value.
    begins_with = 'beginsWith'
    #: The content of the answer ends with the value.
    ends_with = 'endsWith'
    #: The content of the answer is the same as the value.
    equals = 'equals'
    #: The content of the answer is not the same as the value.
    not_equals = 'notEquals'


class Result(str, Enum):
    #: If the user's registration value meets the criteria, the registration form will be automatically approved.
    approve = 'approve'
    #: If the user's registration value meets the criteria, the registration form will be automatically rejected.
    reject = 'reject'


class Rules1(ApiModel):
    #: Judgment expression for approval rules.
    condition: Optional[Condition]
    #: The keyword for the approval rule. If the rule matches the keyword, the corresponding action will be executed.
    value: Optional[str]
    #: The automatic approval result for the approval rule.
    result: Optional[Result]
    #: Whether to check the case of values.
    match_case: Optional[bool]


class CustomizedQuestionForCreateMeeting(ApiModel):
    #: Title of the customized question.
    question: Optional[str]
    #: Whether or not the customized question is required to be answered by participants.
    required: Optional[bool]
    #: Type of the question being asked.
    type: Optional[Type]
    #: The maximum length of a string that can be entered by the user, ranging from 0 to 999. Only required by
    #: singleLineTextBox and multiLineTextBox.
    max_length: Optional[int]
    #: The content of options. Required if the question type is one of checkbox, dropdownList, or radioButtons.
    #: The content of the option.
    options: Optional[list[object]]
    #: The automatic approval rules for customized questions.
    rules: Optional[list[Rules1]]


class CustomizedQuestionForGetMeeting(CustomizedQuestionForCreateMeeting):
    #: Unique identifier for the question.
    id: Optional[int]


class Question(str, Enum):
    #: If the value is lastName, this approval rule applies to the standard question of "Last Name".
    last_name = 'lastName'
    #: If the value is email, this approval rule applies to the standard question of "Email".
    email = 'email'
    #: If the value is jobTitle, this approval rule applies to the standard question of "Job Title".
    job_title = 'jobTitle'
    #: If the value is companyName, this approval rule applies to the standard question of "Company Name".
    company_name = 'companyName'
    #: If the value is address1, this approval rule applies to the standard question of "Address 1".
    address1 = 'address1'
    #: If the value is address2, this approval rule applies to the standard question of "Address 2".
    address2 = 'address2'
    #: If the value is city, this approval rule applies to the standard question of "City".
    city = 'city'
    #: If the value is state, this approval rule applies to the standard question of "State".
    state = 'state'
    #: If the value is zipCode, this approval rule applies to the standard question of "Zip/Post Code".
    zip_code = 'zipCode'
    #: If the value is countryRegion, this approval rule applies to the standard question of "Country Region".
    country_region = 'countryRegion'
    #: If the value is workPhone, this approval rule applies to the standard question of "Work Phone".
    work_phone = 'workPhone'
    #: If the value is fax, this approval rule applies to the standard question of "Fax".
    fax = 'fax'


class StandardRegistrationApproveRule(Rules1):
    #: Name for standard question.
    question: Optional[Question]
    #: The priority number of the approval rule. Approval rules for standard questions and custom questions need to be
    #: ordered together.
    order: Optional[int]


class GetRegistrationFormFormeetingResponse(ApiModel):
    #: Whether or not a registrant's first name is required for meeting registration. This option must always be true.
    require_first_name: Optional[bool]
    #: Whether or not a registrant's last name is required for meeting registration. This option must always be true.
    require_last_name: Optional[bool]
    #: Whether or not a registrant's email is required for meeting registration. This option must always be true.
    require_email: Optional[bool]
    #: Whether or not a registrant's job title is shown or required for meeting registration.
    require_job_title: Optional[bool]
    #: Whether or not a registrant's company name is shown or required for meeting registration.
    require_company_name: Optional[bool]
    #: Whether or not a registrant's first address field is shown or required for meeting registration.
    require_address1: Optional[bool]
    #: Whether or not a registrant's second address field is shown or required for meeting registration.
    require_address2: Optional[bool]
    #: Whether or not a registrant's city is shown or required for meeting registration.
    require_city: Optional[bool]
    #: Whether or not a registrant's state is shown or required for meeting registration.
    require_state: Optional[bool]
    #: Whether or not a registrant's postal code is shown or required for meeting registration.
    require_zip_code: Optional[bool]
    #: Whether or not a registrant's country or region is shown or required for meeting registration.
    require_country_region: Optional[bool]
    #: Whether or not a registrant's work phone number is shown or required for meeting registration.
    require_work_phone: Optional[bool]
    #: Whether or not a registrant's fax number is shown or required for meeting registration.
    require_fax: Optional[bool]
    #: Customized questions for meeting registration.
    customized_questions: Optional[list[CustomizedQuestionForGetMeeting]]
    #: The approval rules for standard questions.
    rules: Optional[list[StandardRegistrationApproveRule]]


class UpdateMeetingRegistrationFormBody(ApiModel):
    host_email: Optional[str]
    #: Whether or not a registrant's first name is required for meeting registration. This option must always be true.
    require_first_name: Optional[bool]
    #: Whether or not a registrant's last name is required for meeting registration. This option must always be true.
    require_last_name: Optional[bool]
    #: Whether or not a registrant's email is required for meeting registration. This option must always be true.
    require_email: Optional[bool]
    #: Whether or not a registrant's job title is shown or required for meeting registration.
    require_job_title: Optional[bool]
    #: Whether or not a registrant's company name is shown or required for meeting registration.
    require_company_name: Optional[bool]
    #: Whether or not a registrant's first address field is shown or required for meeting registration.
    require_address1: Optional[bool]
    #: Whether or not a registrant's second address field is shown or required for meeting registration.
    require_address2: Optional[bool]
    #: Whether or not a registrant's city is shown or required for meeting registration.
    require_city: Optional[bool]
    #: Whether or not a registrant's state is shown or required for meeting registration.
    require_state: Optional[bool]
    #: Whether or not a registrant's postal code is shown or required for meeting registration.
    require_zip_code: Optional[bool]
    #: Whether or not a registrant's country or region is shown or required for meeting registration.
    require_country_region: Optional[bool]
    #: Whether or not a registrant's work phone number is shown or required for meeting registration.
    require_work_phone: Optional[bool]
    #: Whether or not a registrant's fax number is shown or required for meeting registration.
    require_fax: Optional[bool]
    #: The maximum number of meeting registrations. Only applies to meetings. Webinars use a default value of 10000. If
    #: the maximum capacity of attendees for a webinar is less than 10000, e.g. 3000, then at most 3000 registrants can
    #: join this webinar.
    max_register_num: Optional[int]
    #: Customized questions for meeting registration.
    customized_questions: Optional[list[CustomizedQuestionForCreateMeeting]]
    #: The approval rule for standard questions.
    rules: Optional[list[StandardRegistrationApproveRule]]


class Api(ApiChild, base='meetings/'):
    """

    """

    def form_formeeting(self, meeting_id: str) -> GetRegistrationFormFormeetingResponse:
        """
        Get a meeting's registration form to understand which fields are required.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-registration-form-for-a-meeting
        """
        url = self.ep(f'{meeting_id}/registration')
        data = super().get(url=url)
        return GetRegistrationFormFormeetingResponse.parse_obj(data)

    def update_meeting_form(self, meeting_id: str, host_email: str = None, require_first_name: bool = None, require_last_name: bool = None, require_email: bool = None, require_job_title: bool = None, require_company_name: bool = None, require_address1: bool = None, require_address2: bool = None, require_city: bool = None, require_state: bool = None, require_zip_code: bool = None, require_country_region: bool = None, require_work_phone: bool = None, require_fax: bool = None, max_register_num: int = None, customized_questions: CustomizedQuestionForCreateMeeting = None, rules: StandardRegistrationApproveRule = None) -> GetRegistrationFormFormeetingResponse:
        """
        Enable or update a registration form for a meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting or an occurrence meeting.
        :type meeting_id: str
        :param host_email: 
        :type host_email: str
        :param require_first_name: Whether or not a registrant's first name is required for meeting registration. This
            option must always be true.
        :type require_first_name: bool
        :param require_last_name: Whether or not a registrant's last name is required for meeting registration. This
            option must always be true.
        :type require_last_name: bool
        :param require_email: Whether or not a registrant's email is required for meeting registration. This option
            must always be true.
        :type require_email: bool
        :param require_job_title: Whether or not a registrant's job title is shown or required for meeting
            registration.
        :type require_job_title: bool
        :param require_company_name: Whether or not a registrant's company name is shown or required for meeting
            registration.
        :type require_company_name: bool
        :param require_address1: Whether or not a registrant's first address field is shown or required for meeting
            registration.
        :type require_address1: bool
        :param require_address2: Whether or not a registrant's second address field is shown or required for meeting
            registration.
        :type require_address2: bool
        :param require_city: Whether or not a registrant's city is shown or required for meeting registration.
        :type require_city: bool
        :param require_state: Whether or not a registrant's state is shown or required for meeting registration.
        :type require_state: bool
        :param require_zip_code: Whether or not a registrant's postal code is shown or required for meeting
            registration.
        :type require_zip_code: bool
        :param require_country_region: Whether or not a registrant's country or region is shown or required for meeting
            registration.
        :type require_country_region: bool
        :param require_work_phone: Whether or not a registrant's work phone number is shown or required for meeting
            registration.
        :type require_work_phone: bool
        :param require_fax: Whether or not a registrant's fax number is shown or required for meeting registration.
        :type require_fax: bool
        :param max_register_num: The maximum number of meeting registrations. Only applies to meetings. Webinars use a
            default value of 10000. If the maximum capacity of attendees for a webinar is less than 10000, e.g. 3000,
            then at most 3000 registrants can join this webinar.
        :type max_register_num: int
        :param customized_questions: Customized questions for meeting registration.
        :type customized_questions: CustomizedQuestionForCreateMeeting
        :param rules: The approval rule for standard questions.
        :type rules: StandardRegistrationApproveRule

        documentation: https://developer.webex.com/docs/api/v1/meetings/update-meeting-registration-form
        """
        body = UpdateMeetingRegistrationFormBody()
        if host_email is not None:
            body.host_email = host_email
        if require_first_name is not None:
            body.require_first_name = require_first_name
        if require_last_name is not None:
            body.require_last_name = require_last_name
        if require_email is not None:
            body.require_email = require_email
        if require_job_title is not None:
            body.require_job_title = require_job_title
        if require_company_name is not None:
            body.require_company_name = require_company_name
        if require_address1 is not None:
            body.require_address1 = require_address1
        if require_address2 is not None:
            body.require_address2 = require_address2
        if require_city is not None:
            body.require_city = require_city
        if require_state is not None:
            body.require_state = require_state
        if require_zip_code is not None:
            body.require_zip_code = require_zip_code
        if require_country_region is not None:
            body.require_country_region = require_country_region
        if require_work_phone is not None:
            body.require_work_phone = require_work_phone
        if require_fax is not None:
            body.require_fax = require_fax
        if max_register_num is not None:
            body.max_register_num = max_register_num
        if customized_questions is not None:
            body.customized_questions = customized_questions
        if rules is not None:
            body.rules = rules
        url = self.ep(f'{meeting_id}/registration')
        data = super().put(url=url, data=body.json())
        return GetRegistrationFormFormeetingResponse.parse_obj(data)

    def delete_meeting_form(self, meeting_id: str):
        """
        Disable the registration form for a meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting or an occurrence meeting.
        :type meeting_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-meeting-registration-form
        """
        url = self.ep(f'{meeting_id}/registration')
        super().delete(url=url)
        return


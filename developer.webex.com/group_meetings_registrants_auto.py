from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['AnswerForCustomizedQuestion', 'Api', 'BatchRegisterMeetingRegistrantsResponse', 'CustomizedRegistrant',
           'GetmeetingRegistrantsDetailInformationResponse', 'ListMeetingRegistrantsResponse', 'OrderBy', 'OrderType',
           'QueryMeetingRegistrantsResponse', 'RegisterMeetingRegistrantBody', 'RegisterMeetingRegistrantResponse',
           'Status']


class AnswerForCustomizedQuestion(ApiModel):
    #: Unique identifier for the option.
    option_id: Optional[int]
    #: The content of the answer or the option for this question.
    answer: Optional[str]


class CustomizedRegistrant(ApiModel):
    #: Unique identifier for the customized questions retrieved from the registration form.
    question_id: Optional[int]
    #: The answers for customized questions. If the question type is checkbox, more than one answer can be set.
    answers: Optional[list[AnswerForCustomizedQuestion]]


class Status(str, Enum):
    #: Registrant has been approved.
    approved = 'approved'
    #: Registrant is in a pending list waiting for host or cohost approval.
    pending = 'pending'
    #: Registrant has been rejected by the host or cohost.
    rejected = 'rejected'


class GetmeetingRegistrantsDetailInformationResponse(ApiModel):
    #: New registrant's ID.
    registrant_id: Optional[str]
    #: New registrant's status.
    status: Optional[Status]
    #: Registrant's first name.
    first_name: Optional[str]
    #: Registrant's last name.
    last_name: Optional[str]
    #: Registrant's email.
    email: Optional[str]
    #: Registrant's job title.
    job_title: Optional[str]
    #: Registrant's company.
    company_name: Optional[str]
    #: Registrant's first address line.
    address1: Optional[str]
    #: Registrant's second address line.
    address2: Optional[str]
    #: Registrant's city name.
    city: Optional[str]
    #: Registrant's state.
    state: Optional[str]
    #: Registrant's postal code.
    zip_code: Optional[int]
    #: Registrant's country or region.
    country_region: Optional[str]
    #: Registrant's work phone number.
    work_phone: Optional[str]
    #: Registrant's FAX number.
    fax: Optional[str]
    #: Registrant's registration time.
    registration_time: Optional[str]
    #: Registrant's answers for customized questions, Registration options define whether or not this is required.
    customized_questions: Optional[list[CustomizedRegistrant]]
    #: Registrant's source id.The sourceId is from Create Invitation Sources API.
    source_id: Optional[str]


class RegisterMeetingRegistrantBody(ApiModel):
    #: The registrant's first name.
    first_name: Optional[str]
    #: The registrant's last name. (Required)
    last_name: Optional[str]
    #: The registrant's email.
    email: Optional[str]
    #: If true send email to the registrant. Default: true.
    send_email: Optional[bool]
    #: The registrant's job title. Registration options define whether or not this is required.
    job_title: Optional[str]
    #: The registrant's company. Registration options define whether or not this is required.
    company_name: Optional[str]
    #: The registrant's first address line. Registration options define whether or not this is required.
    address1: Optional[str]
    #: The registrant's second address line. Registration options define whether or not this is required.
    address2: Optional[str]
    #: The registrant's city name. Registration options define whether or not this is required.
    city: Optional[str]
    #: The registrant's state. Registration options define whether or not this is required.
    state: Optional[str]
    #: The registrant's postal code. Registration options define whether or not this is required.
    zip_code: Optional[int]
    #: The America is not a country or a specific region. Registration options define whether or not this is required.
    country_region: Optional[str]
    #: The registrant's work phone number. Registration options define whether or not this is required.
    work_phone: Optional[str]
    #: The registrant's FAX number. Registration options define whether or not this is required.
    fax: Optional[str]
    #: The registrant's answers for customized questions. Registration options define whether or not this is required.
    customized_questions: Optional[list[CustomizedRegistrant]]


class RegisterMeetingRegistrantResponse(ApiModel):
    #: New registrant's ID.
    id: Optional[str]
    #: New registrant's status.
    status: Optional[Status]
    #: Registrant's first name.
    first_name: Optional[str]
    #: Registrant's last name.
    last_name: Optional[str]
    #: Registrant's email.
    email: Optional[str]
    #: Registrant's job title.
    job_title: Optional[str]
    #: Registrant's company.
    company_name: Optional[str]
    #: Registrant's first address line.
    address1: Optional[str]
    #: Registrant's second address line.
    address2: Optional[str]
    #: Registrant's city name.
    city: Optional[str]
    #: Registrant's state.
    state: Optional[str]
    #: Registrant's postal code.
    zip_code: Optional[int]
    #: Registrant's country or region.
    country_region: Optional[str]
    #: Registrant's work phone number.
    work_phone: Optional[str]
    #: Registrant's FAX number.
    fax: Optional[str]
    #: Registrant's registration time.
    registration_time: Optional[str]
    #: Registrant's answers for customized questions, Registration options define whether or not this is required.
    customized_questions: Optional[list[CustomizedRegistrant]]


class OrderType(str, Enum):
    desc = 'DESC'
    asc = 'ASC'


class OrderBy(str, Enum):
    #: Registrant's first name.
    first_name = 'firstName'
    #: Registrant's last name.
    last_name = 'lastName'
    #: Registrant's status.
    status = 'status'
    #: registrant's email.
    email = 'email'


class ListMeetingRegistrantsResponse(ApiModel):
    #: Registrants array.
    items: Optional[list[GetmeetingRegistrantsDetailInformationResponse]]


class BatchUpdateMeetingRegistrantsStatusBody(ApiModel):
    #: If true send email to registrants. Default: true.
    send_email: Optional[bool]
    #: Registrants array.
    #: Registrant ID.
    registrants: Optional[list[Registrants]]


class BatchRegisterMeetingRegistrantsBody(ApiModel):
    #: Registrants array.
    items: Optional[list[RegisterMeetingRegistrantBody]]


class BatchRegisterMeetingRegistrantsResponse(ApiModel):
    items: Optional[list[RegisterMeetingRegistrantResponse]]


class QueryMeetingRegistrantsBody(ApiModel):
    #: Registrant's status.
    status: Optional[Status]
    #: Sort order for the registrants.
    order_type: Optional[OrderType]
    #: Registrant ordering field. Ordered by registrationTime by default.
    order_by: Optional[OrderBy]
    #: List of registrant email addresses.
    #: Possible values: bob@example.com
    emails: Optional[list[str]]


class QueryMeetingRegistrantsResponse(ApiModel):
    #: Registrants array.
    items: Optional[list[GetmeetingRegistrantsDetailInformationResponse]]


class Api(ApiChild, base='meetings/'):
    """

    """

    def register_registrant(self, meeting_id: str, first_name: str, last_name: str, email: str, send_email: bool = None, job_title: str = None, company_name: str = None, address1: str = None, address2: str = None, city: str = None, state: str = None, zip_code: int = None, country_region: str = None, work_phone: str = None, fax: str = None, customized_questions: CustomizedRegistrant = None) -> RegisterMeetingRegistrantResponse:
        """
        Register a new registrant for a meeting.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param first_name: The registrant's first name.
        :type first_name: str
        :param last_name: The registrant's last name. (Required)
        :type last_name: str
        :param email: The registrant's email.
        :type email: str
        :param send_email: If true send email to the registrant. Default: true.
        :type send_email: bool
        :param job_title: The registrant's job title. Registration options define whether or not this is required.
        :type job_title: str
        :param company_name: The registrant's company. Registration options define whether or not this is required.
        :type company_name: str
        :param address1: The registrant's first address line. Registration options define whether or not this is
            required.
        :type address1: str
        :param address2: The registrant's second address line. Registration options define whether or not this is
            required.
        :type address2: str
        :param city: The registrant's city name. Registration options define whether or not this is required.
        :type city: str
        :param state: The registrant's state. Registration options define whether or not this is required.
        :type state: str
        :param zip_code: The registrant's postal code. Registration options define whether or not this is required.
        :type zip_code: int
        :param country_region: The America is not a country or a specific region. Registration options define whether
            or not this is required.
        :type country_region: str
        :param work_phone: The registrant's work phone number. Registration options define whether or not this is
            required.
        :type work_phone: str
        :param fax: The registrant's FAX number. Registration options define whether or not this is required.
        :type fax: str
        :param customized_questions: The registrant's answers for customized questions. Registration options define
            whether or not this is required.
        :type customized_questions: CustomizedRegistrant

        documentation: https://developer.webex.com/docs/api/v1/meetings/register-a-meeting-registrant
        """
        body = RegisterMeetingRegistrantBody()
        if first_name is not None:
            body.first_name = first_name
        if last_name is not None:
            body.last_name = last_name
        if email is not None:
            body.email = email
        if send_email is not None:
            body.send_email = send_email
        if job_title is not None:
            body.job_title = job_title
        if company_name is not None:
            body.company_name = company_name
        if address1 is not None:
            body.address1 = address1
        if address2 is not None:
            body.address2 = address2
        if city is not None:
            body.city = city
        if state is not None:
            body.state = state
        if zip_code is not None:
            body.zip_code = zip_code
        if country_region is not None:
            body.country_region = country_region
        if work_phone is not None:
            body.work_phone = work_phone
        if fax is not None:
            body.fax = fax
        if customized_questions is not None:
            body.customized_questions = customized_questions
        url = self.ep(f'{meeting_id}/registrants')
        data = super().post(url=url, data=body.json())
        return RegisterMeetingRegistrantResponse.parse_obj(data)

    def getmeeting_registrants_detail_information(self, meeting_id: str, registrant_id: str) -> GetmeetingRegistrantsDetailInformationResponse:
        """
        Retrieves details for a meeting registrant with a specified registrant Id.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param registrant_id: Unique identifier for the registrant
        :type registrant_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/get-a-meeting-registrant's-detail-information
        """
        url = self.ep(f'{meeting_id}/registrants/{registrant_id}')
        data = super().get(url=url)
        return GetmeetingRegistrantsDetailInformationResponse.parse_obj(data)

    def list_registrants(self, meeting_id: str, email: str = None, register_time_from: str = None, register_time_to: str = None, **params) -> Generator[GetmeetingRegistrantsDetailInformationResponse, None, None]:
        """
        Meeting's host and cohost can retrieve the list of registrants for a meeting with a specified meeting Id.

        :param meeting_id: Unique identifier for the meeting.
        :type meeting_id: str
        :param email: Registrant's email to filter registrants.
        :type email: str
        :param register_time_from: The time registrants register a meeting starts from the specified date and time
            (inclusive) in any ISO 8601 compliant format. If registerTimeFrom is not specified, it equals
            registerTimeTo minus 7 days.
        :type register_time_from: str
        :param register_time_to: The time registrants register a meeting before the specified date and time (exclusive)
            in any ISO 8601 compliant format. If registerTimeTo is not specified, it equals registerTimeFrom plus 7
            days. The interval between registerTimeFrom and registerTimeTo must be within 90 days.
        :type register_time_to: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/list-meeting-registrants
        """
        if email is not None:
            params['email'] = email
        if register_time_from is not None:
            params['registerTimeFrom'] = register_time_from
        if register_time_to is not None:
            params['registerTimeTo'] = register_time_to
        url = self.ep(f'{meeting_id}/registrants')
        return self.session.follow_pagination(url=url, model=GetmeetingRegistrantsDetailInformationResponse, params=params)

    def batch_update_registrants_status(self, meeting_id: str, status_op_type: str, send_email: bool = None, registrants: List[Registrants] = None):
        """
        Meeting's host or cohost can update the set of registrants for a meeting. cancel means the registrant(s) will
        be moved back to the registration list. bulkDelete means the registrant(s) will be deleted.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param status_op_type: Update registrant's status. Possible values: approve, reject, cancel, bulkDelete
        :type status_op_type: str
        :param send_email: If true send email to registrants. Default: true.
        :type send_email: bool
        :param registrants: Registrants array. Registrant ID.
        :type registrants: List[Registrants]

        documentation: https://developer.webex.com/docs/api/v1/meetings/batch-update-meeting-registrants-status
        """
        body = BatchUpdateMeetingRegistrantsStatusBody()
        if send_email is not None:
            body.send_email = send_email
        if registrants is not None:
            body.registrants = registrants
        url = self.ep(f'{meeting_id}/registrants/{status_op_type}')
        super().post(url=url, data=body.json())
        return

    def delete_registrant(self, meeting_id: str, registrant_id: str):
        """
        Meeting's host or cohost can delete a registrant with a specified registrant ID.

        :param meeting_id: Unique identifier for the meeting. Does not support meeting IDs for a scheduled personal
            room meeting.
        :type meeting_id: str
        :param registrant_id: Unique identifier for the registrant.
        :type registrant_id: str

        documentation: https://developer.webex.com/docs/api/v1/meetings/delete-a-meeting-registrant
        """
        url = self.ep(f'{meeting_id}/registrants/{registrant_id}')
        super().delete(url=url)
        return

    def batch_register_registrants(self, meeting_id: str, items: RegisterMeetingRegistrantBody = None) -> list[RegisterMeetingRegistrantResponse]:
        """
        Bulk register new registrants for a meeting.

        :param meeting_id: Unique identifier for the meeting.
        :type meeting_id: str
        :param items: Registrants array.
        :type items: RegisterMeetingRegistrantBody

        documentation: https://developer.webex.com/docs/api/v1/meetings/batch-register-meeting-registrants
        """
        body = BatchRegisterMeetingRegistrantsBody()
        if items is not None:
            body.items = items
        url = self.ep(f'{meeting_id}/registrants/bulkInsert')
        data = super().post(url=url, data=body.json())
        return parse_obj_as(list[RegisterMeetingRegistrantResponse], data["items"])

    def query_registrants(self, meeting_id: str, emails: List[str], status: Status = None, order_type: OrderType = None, order_by: OrderBy = None, **params) -> Generator[GetmeetingRegistrantsDetailInformationResponse, None, None]:
        """
        Meeting's host and cohost can query the list of registrants for a meeting with a specified meeting ID and
        registrants email.

        :param meeting_id: Unique identifier for the meeting.
        :type meeting_id: str
        :param emails: List of registrant email addresses. Possible values: bob@example.com
        :type emails: List[str]
        :param status: Registrant's status.
        :type status: Status
        :param order_type: Sort order for the registrants.
        :type order_type: OrderType
        :param order_by: Registrant ordering field. Ordered by registrationTime by default.
        :type order_by: OrderBy

        documentation: https://developer.webex.com/docs/api/v1/meetings/query-meeting-registrants
        """
        body = QueryMeetingRegistrantsBody()
        if emails is not None:
            body.emails = emails
        if status is not None:
            body.status = status
        if order_type is not None:
            body.order_type = order_type
        if order_by is not None:
            body.order_by = order_by
        url = self.ep(f'{meeting_id}/registrants/query')
        return self.session.follow_pagination(url=url, model=GetmeetingRegistrantsDetailInformationResponse, params=params, data=body.json())


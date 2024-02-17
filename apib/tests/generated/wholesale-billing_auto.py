from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['ListReport', 'ListReportStatus', 'ListReportType', 'ListWholesaleBillingReportsSortBy', 'Report',
           'ReportError', 'ReportId', 'WholesaleBillingReportsApi']


class ListReportStatus(str, Enum):
    #: Report generation is in progress.
    in_progress = 'IN_PROGRESS'
    #: Report generation is complete.
    completed = 'COMPLETED'
    #: Report generation failed.
    failed = 'FAILED'


class ListReportType(str, Enum):
    user = 'USER'
    customer = 'CUSTOMER'
    partner = 'PARTNER'


class ListReport(ApiModel):
    #: A unique report id that corresponds to a billing report.
    #: example: 'Y2lzY29zcGFyazovL3VzL0JJTExJTkdfUkVQT1JULzViOGQ1MThhLThmMDAtNDUxYi1hNDA2LWVhZjQ5YjRhN2ZhOA'
    id: Optional[str] = None
    #: Billing report startDate.
    #: example: 2021-05-21
    billing_start_date: Optional[datetime] = None
    #: Billing report endDate.
    #: example: 2021-05-30
    billing_end_date: Optional[datetime] = None
    #: The status of the billing report
    #: example: COMPLETED
    status: Optional[ListReportStatus] = None
    #: Billing Report Type.
    #: example: PARTNER
    type: Optional[ListReportType] = None


class ReportError(ApiModel):
    #: An error code that identifies the reason for the error.
    #: example: 2024
    code: Optional[int] = None
    #: A textual representation of the error code.
    #: example: Billing Report not found.
    description: Optional[str] = None


class Report(ApiModel):
    #: A unique report ID that corresponds to a billing report.
    #: example: 'Y2lzY29zcGFyazovL3VzL0JJTExJTkdfUkVQT1JULzViOGQ1MThhLThmMDAtNDUxYi1hNDA2LWVhZjQ5YjRhN2ZhOA'
    id: Optional[str] = None
    #: Billing report `startDate`.
    #: example: 2021-05-21
    billing_start_date: Optional[datetime] = None
    #: Billing report `endDate`.
    #: example: 2021-05-30
    billing_end_date: Optional[datetime] = None
    #: Billing Report Type
    #: example: PARTNER
    type: Optional[ListReportType] = None
    #: The date and time the report was generated.
    #: example: 2021-06-16T12:40:33.109Z
    created: Optional[datetime] = None
    #: The person ID of the partner administrator who created the report.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wYWNkMzg3NS00ZTEyLTRkNzctYjk4MS1lMzg5ZmQ4ODQ2YzA
    created_by: Optional[str] = None
    #: The status of the billing report.
    #: example: COMPLETED
    status: Optional[ListReportStatus] = None
    #: The URL for partners to download the billing report.
    #: example: https://billing-reports-int-us-east-1.webexcontent.com/a366de9b-3204-4140-8181-25808d360e36/WHOLESALE/340177d1-7f25-41e1-a39f-ad63ec1103a5.csv?Expires=1624978489&Signature=Syp3vrVeMx4P6MeMtm8e1bQaeAdHFe-c7NeHERWh5-qJGLZ1T8Dvl2ee-M8OsFf~z6Yepz94e2Hh1HDVailD0Uryl8SgiM~jl0cBh7L0PmSe~i9oFA0eJ0MulkqGSMVf7ZHhxY55xYMgIBZIERkWm3CqQNDg5BS4EaXapKfOnmFegf36OokCM63m5uOK8-csk08IkZhwo2Z0l1JMtuWYEaLh4dgMHoe~xgH3YmDSSCWInFYaEifUAfgi2YAYS6nP9Zq4BTliBq62XBaehOE1gBrhy4RdwD-3WSs2oD-BdpoRpuGzo3FZzDLVEvd0S2D6gTcHljOHodQKxe-u0BXPWQ__&Key-Pair-Id=APKAJADAKLCI2FW2U32Q
    temp_download_url: Optional[str] = Field(alias='tempDownloadURL', default=None)
    #: List of errors that occurred during report generation.
    #: 
    #: **Note:**
    #: 
    #: * This list captures errors that occurred during asynchronous or background report generation, after the request
    #: has been accepted and a `202 OK` response is returned.
    errors: Optional[list[ReportError]] = None


class ReportId(ApiModel):
    #: A unique report ID that corresponds to a billing report.
    #: example: 'Y2lzY29zcGFyazovL3VzL0JJTExJTkdfUkVQT1JULzViOGQ1MThhLThmMDAtNDUxYi1hNDA2LWVhZjQ5YjRhN2ZhOA'
    id: Optional[str] = None
    #: Billing report startDate.
    #: example: 2021-05-21
    billing_start_date: Optional[datetime] = None
    #: Billing report endDate.
    #: example: 2021-05-30
    billing_end_date: Optional[datetime] = None
    #: Billing Report Type
    #: example: PARTNER
    type: Optional[ListReportType] = None


class ListWholesaleBillingReportsSortBy(str, Enum):
    id = 'id'
    billing_start_date = 'billingStartDate'
    billing_end_date = 'billingEndDate'
    status = 'status'


class WholesaleBillingReportsApi(ApiChild, base='wholesale/billing/reports'):
    """
    Wholesale Billing Reports
    
    The Wholesale Billing Report APIs are targeted at Service Providers who sign up for the Webex for Wholesale
    solution. These APIs provide customer and user breakdown reports to the service providers or partners. Service
    providers can use these reports to reconcile their monthly invoices.
    
    Viewing Webex for Wholesale billing reports information requires a partner administrator auth token with the
    `spark-admin:wholesale_billing_reports_read` scope. Creating, Deleting billing reports require a partner
    administrator auth token with the `spark-admin:wholesale_billing_reports_write` scope.
    
    Each Webex Developer Sandbox for Webex Wholesale use is limited to a maximum
    of 10 account users for validation and test purposes only. Cisco may from time
    to time audit Webex Developer Sandbox accounts and reserves the right to
    remove users in excess of 10 account users, or terminate the Webex Developer
    Sandbox environment for any Developer resource misuse. To learn more about the
    error codes used in Wholesale billing reports API, see the [API Error
    codes](/docs/api/guides/webex-for-wholesale#api-error-codes) guides.
    
    """

    def list_wholesale_billing_reports(self, billing_start_date: Union[str, datetime] = None,
                                       billing_end_date: Union[str, datetime] = None,
                                       sort_by: ListWholesaleBillingReportsSortBy = None, type: ListReportType = None,
                                       status: ListReportStatus = None, sub_partner_org_id: str = None,
                                       **params) -> Generator[ListReport, None, None]:
        """
        List Wholesale Billing Reports

        Search for associated wholesale billing reconciliation reports.

        :param billing_start_date: Only include billing reports having this billing `startDate`.
        :type billing_start_date: Union[str, datetime]
        :param billing_end_date: Only include billing reports having this billing `endDate`.
        :type billing_end_date: Union[str, datetime]
        :param sort_by: Sort the reports.
        :type sort_by: ListWholesaleBillingReportsSortBy
        :param type: Only include reports of this type.
        :type type: ListReportType
        :param status: The status of the billing report
        :type status: ListReportStatus
        :param sub_partner_org_id: The Organization ID of the sub partner on Cisco Webex.
        :type sub_partner_org_id: str
        :return: Generator yielding :class:`ListReport` instances
        """
        if billing_start_date is not None:
            if isinstance(billing_start_date, str):
                billing_start_date = isoparse(billing_start_date)
            billing_start_date = dt_iso_str(billing_start_date)
            params['billingStartDate'] = billing_start_date
        if billing_end_date is not None:
            if isinstance(billing_end_date, str):
                billing_end_date = isoparse(billing_end_date)
            billing_end_date = dt_iso_str(billing_end_date)
            params['billingEndDate'] = billing_end_date
        if sort_by is not None:
            params['sortBy'] = sort_by
        if type is not None:
            params['type'] = type
        if status is not None:
            params['status'] = status
        if sub_partner_org_id is not None:
            params['subPartnerOrgId'] = sub_partner_org_id
        url = self.ep()
        return self.session.follow_pagination(url=url, model=ListReport, item_key='items', params=params)

    def get_a_wholesale_billing_report(self, id: str) -> Report:
        """
        Get a Wholesale Billing Report

        Retrieve a specific wholesale billing reconciliation report.

        :param id: A unique identifier for the report being requested.
        :type id: str
        :rtype: :class:`Report`
        """
        url = self.ep(f'{id}')
        data = super().get(url)
        r = Report.model_validate(data)
        return r

    def create_a_wholesale_billing_report(self, billing_start_date: Union[str, datetime], billing_end_date: Union[str,
                                          datetime], type: str = None, sub_partner_org_id: str = None) -> ReportId:
        """
        Create a Wholesale Billing Report

        Generate a wholesale billing reconciliation report.

        :param billing_start_date: The `startDate` (`YYYY-MM-DD`) for which the partner requests the billing report.
        :type billing_start_date: Union[str, datetime]
        :param billing_end_date: The `endDate` (`YYYY-MM-DD`) for which the partner requests the billing report.
        :type billing_end_date: Union[str, datetime]
        :param type: Create report of the given type, `PARTNER`, `CUSTOMER`, or `USER`. Default: `PARTNER`.
        :type type: str
        :param sub_partner_org_id: The Organization ID of the sub partner on Cisco Webex.
        :type sub_partner_org_id: str
        :rtype: :class:`ReportId`
        """
        body = dict()
        body['billingStartDate'] = billing_start_date
        body['billingEndDate'] = billing_end_date
        if type is not None:
            body['type'] = type
        if sub_partner_org_id is not None:
            body['subPartnerOrgId'] = sub_partner_org_id
        url = self.ep()
        data = super().post(url, json=body)
        r = ReportId.model_validate(data)
        return r

    def delete_a_wholesale_billing_report(self, id: str):
        """
        Delete a Wholesale Billing Report

        Delete a monthly reconciliation report by report ID.

        :param id: A unique report ID that corresponds to a billing report.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'{id}')
        super().delete(url)

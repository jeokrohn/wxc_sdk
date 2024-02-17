from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BroadWorksBillingReportsApi', 'ListReport', 'Report', 'ReportError', 'ReportStatus']


class ReportError(ApiModel):
    #: The error code itself.
    #: example: 2024
    code: Optional[int] = None
    #: A textual representation of the error code.
    #: example: Billing Report not found.
    description: Optional[str] = None


class ReportStatus(str, Enum):
    #: Report generation is in progress.
    in_progress = 'IN_PROGRESS'
    #: Report generation is complete.
    completed = 'COMPLETED'
    #: Report generation failed.
    failed = 'FAILED'


class Report(ApiModel):
    #: A unique report ID that corresponds to a billing report.
    #: example: 'Y2lzY29zcGFyazovL3VzL0JJTExJTkdfUkVQT1JULzViOGQ1MThhLThmMDAtNDUxYi1hNDA2LWVhZjQ5YjRhN2ZhOA'
    id: Optional[str] = None
    #: The year and month (`YYYY-MM`) for which the billing report was generated.
    #: example: 2021-05
    billing_period: Optional[datetime] = None
    #: The status of the billing report.
    #: example: IN_PROGRESS
    status: Optional[ReportStatus] = None
    #: The date and time the report was generated.
    #: example: 2021-06-16T12:40:33.109Z
    created: Optional[datetime] = None
    #: The person ID of the partner administrator who created the report.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wYWNkMzg3NS00ZTEyLTRkNzctYjk4MS1lMzg5ZmQ4ODQ2YzA
    created_by: Optional[str] = None
    #: The URL for partners to download the billing report.
    #: example: https://billing-reports-int-example.webexcontent.com/a366de9b-3204-4140-8181-25808d360e36/2021/06/16/340177d1-7f25-41e1-a39f-ad63ec1103a5.csv?Expires=1624978489&Signature=Syp3vrVeMx4P6MeMtm8e1bQaeAdHFe-c7NeHERWh5-qJGLZ1T8Dvl2ee-M8OsFf~z6Yepz94e2Hh1HDVailD0Uryl8SgiM~jl0cBh7L0PmSe~i9oFA0eJ0MulkqGSMVf7ZHhxY55xYMgIBZIERkWm3CqQNDg5BS4EaXapKfOnmFegf36OokCM63m5uOK8-csk08IkZhwo2Z0l1JMtuWYEaLh4dgMHoe~xgH3YmDSSCWInFYaEifUAfgi2YAYS6nP9Zq4BTliBq62XBaehOE1gBrhy4RdwD-3WSs2oD-BdpoRpuGzo3FZzDLVEvd0S2D6gTcHljOHodQKxe-u0BXPWQ__&Key-Pair-Id=APKAJADAKLCI2FW2U32Q
    temp_download_url: Optional[str] = Field(alias='tempDownloadURL', default=None)
    #: List of errors that occurred during report generation.
    #: 
    #: **Note:**
    #: 
    #: * Captures errors that occurred during asynchronous or background report generation, after the request has been
    #: accepted and a `202 OK` response is returned.
    errors: Optional[list[ReportError]] = None


class ListReport(ApiModel):
    #: A unique report ID that corresponds to a billing report.
    #: example: 'Y2lzY29zcGFyazovL3VzL0JJTExJTkdfUkVQT1JULzViOGQ1MThhLThmMDAtNDUxYi1hNDA2LWVhZjQ5YjRhN2ZhOA'
    id: Optional[str] = None
    #: The year and month (`YYYY-MM`) for which the billing report was generated.
    #: example: 2021-05
    billing_period: Optional[datetime] = None
    #: The status of the billing report.
    #: example: IN_PROGRESS
    status: Optional[ReportStatus] = None


class BroadWorksBillingReportsApi(ApiChild, base='broadworks/billing/reports'):
    """
    BroadWorks Billing Reports
    
    These are a set of APIs that are specifically targeted at BroadWorks Service Providers who sign up to the Webex for
    BroadWorks solution. These APIs helps Service Providers to generate monthly billing reports with user billing data.
    Service Providers can use these reports to reconcile their monthly invoice. Please note
    these APIs require a functional BroadWorks system configured for Webex for BroadWorks. Read more about using this
    API
    at https://www.cisco.com/go/WebexBroadworksAPI.
    
    Viewing Webex for BroadWorks billing reports information requires a partner administrator auth token with
    `spark-admin:broadworks_billing_reports_read` scope. Creating, Deleting billing reports require a partner
    administrator auth token with `spark-admin:broadworks_billing_reports_write` scope.
    """

    def list_broad_works_billing_reports(self, before: Union[str, datetime] = None, after: Union[str, datetime] = None,
                                         sort_by: str = None) -> list[ListReport]:
        """
        List BroadWorks Billing Reports

        Search for reports. There are a number of filter options which can be combined in a single request.

        :param before: Only include billing reports created before this date.
        :type before: Union[str, datetime]
        :param after: Only include billing reports created after this date.
        :type after: Union[str, datetime]
        :param sort_by: Sort the reports.

        + Members:
        + id
        + status
        + billingPeriod
        :type sort_by: str
        :rtype: list[ListReport]
        """
        params = {}
        if before is not None:
            if isinstance(before, str):
                before = isoparse(before)
            before = dt_iso_str(before)
            params['before'] = before
        if after is not None:
            if isinstance(after, str):
                after = isoparse(after)
            after = dt_iso_str(after)
            params['after'] = after
        if sort_by is not None:
            params['sortBy'] = sort_by
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[ListReport]).validate_python(data['items'])
        return r

    def get_a_broad_works_billing_report(self, id: str) -> Report:
        """
        Get a BroadWorks Billing Report

        Retrieve a specific billing reconciliation report.

        :param id: A unique identifier for the report in request.
        :type id: str
        :rtype: :class:`Report`
        """
        url = self.ep(f'{id}')
        data = super().get(url)
        r = Report.model_validate(data)
        return r

    def create_a_broad_works_billing_report(self, billing_period: Union[str, datetime]) -> str:
        """
        Create a BroadWorks Billing Report

        Generate a monthly reconciliation report.

        :param billing_period: The year and month (`YYYY-MM`) for which the billing report is to be generated.
        :type billing_period: Union[str, datetime]
        :rtype: str
        """
        body = dict()
        body['billingPeriod'] = billing_period
        url = self.ep()
        data = super().post(url, json=body)
        r = data['id']
        return r

    def delete_a_broad_works_billing_report(self, id: str):
        """
        Delete a BroadWorks Billing Report

        Delete a monthly reconciliation report using a report ID.

        :param id: A unique report ID that corresponds to a billing report.
        :type id: str
        :rtype: None
        """
        url = self.ep(f'{id}')
        super().delete(url)

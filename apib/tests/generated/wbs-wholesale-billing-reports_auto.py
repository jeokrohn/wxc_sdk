from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ListReport', 'ListWholesaleBillingReportsSortBy', 'Report', 'ReportError', 'ReportId', 'ReportIdType', 'ReportStatus', 'WholesaleBillingReportsListResponse']


class ReportError(ApiModel):
    #: An error code that identifies the reason for the error.
    #: example: 2024.0
    code: Optional[int] = None
    #: A textual representation of the error code.
    #: example: Billing Report not found.
    description: Optional[str] = None


class ReportIdType(str, Enum):
    user = 'USER'
    customer = 'CUSTOMER'
    partner = 'PARTNER'


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
    type: Optional[ReportIdType] = None


class ReportStatus(str, Enum):
    #: Report generation is in progress
    in_progress = 'IN_PROGRESS'
    #: Report generation is complete
    completed = 'COMPLETED'
    #: Report generation failed
    failed = 'FAILED'


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
    type: Optional[ReportIdType] = None
    #: The date and time the report was generated.
    #: example: 2021-06-16T12:40:33.109Z
    created: Optional[datetime] = None
    #: The person ID of the partner administrator who created the report.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wYWNkMzg3NS00ZTEyLTRkNzctYjk4MS1lMzg5ZmQ4ODQ2YzA
    created_by: Optional[str] = None
    #: The status of the billing report.
    #: example: COMPLETED
    status: Optional[ReportStatus] = None
    #: The URL for partners to download the billing report.
    #: example: https://billing-reports-int-us-east-1.webexcontent.com/a366de9b-3204-4140-8181-25808d360e36/WHOLESALE/340177d1-7f25-41e1-a39f-ad63ec1103a5.csv?Expires=1624978489&Signature=Syp3vrVeMx4P6MeMtm8e1bQaeAdHFe-c7NeHERWh5-qJGLZ1T8Dvl2ee-M8OsFf~z6Yepz94e2Hh1HDVailD0Uryl8SgiM~jl0cBh7L0PmSe~i9oFA0eJ0MulkqGSMVf7ZHhxY55xYMgIBZIERkWm3CqQNDg5BS4EaXapKfOnmFegf36OokCM63m5uOK8-csk08IkZhwo2Z0l1JMtuWYEaLh4dgMHoe~xgH3YmDSSCWInFYaEifUAfgi2YAYS6nP9Zq4BTliBq62XBaehOE1gBrhy4RdwD-3WSs2oD-BdpoRpuGzo3FZzDLVEvd0S2D6gTcHljOHodQKxe-u0BXPWQ__&Key-Pair-Id=APKAJADAKLCI2FW2U32Q
    temp_download_url: Optional[str] = Field(alias='tempDownloadURL', default=None)
    #: List of errors that occurred during report generation.
    #: **Note:**
    #: * This list captures errors that occurred during asynchronous or background report generation, after the request has been accepted and a `202 OK` response is returned.
    errors: Optional[list[ReportError]] = None


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
    status: Optional[ReportStatus] = None
    #: Billing Report Type.
    #: example: PARTNER
    type: Optional[ReportIdType] = None


class WholesaleBillingReportsListResponse(ApiModel):
    #: An array of report objects.
    items: Optional[list[ListReport]] = None


class ListWholesaleBillingReportsSortBy(str, Enum):
    id = 'id'
    billing_start_date = 'billingStartDate'
    billing_end_date = 'billingEndDate'
    status = 'status'

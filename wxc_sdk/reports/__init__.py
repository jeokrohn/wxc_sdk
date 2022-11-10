"""
Reports API
"""
import csv
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from pydantic import Field, parse_obj_as, root_validator

from ..api_child import ApiChild
from ..base import ApiModel, to_camel

__all__ = ['ValidationRules', 'ReportTemplate', 'Report', 'ReportsApi', 'CallingCDR']


class ValidationRules(ApiModel):
    #: Field on which validation rule is applied
    field: Optional[str]
    #: Whether the above field is required
    required: Optional[str]


class ReportTemplate(ApiModel):
    #: Unique identifier representing a report.
    id: Optional[int] = Field(alias='Id')
    #: Name of the template.
    title: Optional[str]
    #: The service to which the report belongs.
    service: Optional[str]
    #: Maximum date range for reports belonging to this template.
    max_days: Optional[int]
    start_date: Optional[date]
    end_date: Optional[date]
    #: Generated reports belong to which field.
    identifier: Optional[str]
    #: an array of validation rules
    validations: Optional[list[ValidationRules]]


class Report(ApiModel):
    #: Unique identifier for the report.
    id: Optional[str] = Field(alias='Id')
    #: Name of the template to which this report belongs.
    title: Optional[str]
    #: The service to which the report belongs.
    service: Optional[str]
    #: The data in this report belongs to dates greater than or equal to this.
    start_date: Optional[date]
    #: The data in this report belongs to dates smaller than or equal to this.
    end_date: Optional[date]
    #: The site to which this report belongs to. This only exists if the report belongs to service Webex.
    site_list: Optional[str]
    #: Time of creation for this report.
    created: Optional[datetime]
    #: The person who created the report.
    created_by: Optional[str]
    #: Whether this report was scheduled from API or Control Hub.
    schedule_from: Optional[str]
    #: Completion status of this report.
    status: Optional[str]
    download_domain: Optional[str]
    #: The link from which the report can be downloaded.
    download_url: Optional[str] = Field(alias='downloadURL')


class CallingCDR(ApiModel):
    """
    Records in a Calling Detailed Call History report
    """

    @root_validator(pre=True)
    def remove_na(cls, values):
        """
        Some report fields are marked 'NA'. We want to treat them as null

        :meta private:
        """
        return {k: v for k, v in values.items()
                if v != 'NA'}

    start_time: Optional[datetime] = Field(alias='Start time')
    answer_time: Optional[datetime] = Field(alias='Answer time')
    duration: Optional[int] = Field(alias='Duration')
    calling_number: Optional[str] = Field(alias='Calling number')
    called_number: Optional[str] = Field(alias='Called number')
    user: Optional[str] = Field(alias='User')
    calling_line_id: Optional[str] = Field(alias='Calling line ID')
    called_line_id: Optional[str] = Field(alias='Called line ID')
    correlation_id: Optional[str] = Field(alias='Correlation ID')
    location: Optional[str] = Field(alias='Location')
    inbound_trunk: Optional[str] = Field(alias='Inbound trunk')
    outbound_trunk: Optional[str] = Field(alias='Outbound trunk')
    route_group: Optional[str] = Field(alias='Route group')
    direction: Optional[str] = Field(alias='Direction')
    call_type: Optional[str] = Field(alias='Call type')
    client_type: Optional[str] = Field(alias='Client type')
    client_version: Optional[str] = Field(alias='Client version')
    sub_client_type: Optional[str] = Field(alias='Sub client type')
    os_type: Optional[str] = Field(alias='OS type')
    device_mac: Optional[str] = Field(alias='Device Mac')
    answered: Optional[bool] = Field(alias='Answered')
    international_country: Optional[str] = Field(alias='International Country')
    original_reason: Optional[str] = Field(alias='Original reason')
    related_reason: Optional[str] = Field(alias='Related reason')
    redirect_reason: Optional[str] = Field(alias='Redirect reason')
    site_main_number: Optional[str] = Field(alias='Site main number')
    site_timezone: Optional[int] = Field(alias='Site timezone')
    user_type: Optional[str] = Field(alias='User type')
    call_id: Optional[str] = Field(alias='Call ID')
    user_uuid: Optional[str] = Field(alias='User UUID')
    org_uuid: Optional[str] = Field(alias='Org UUID')
    report_id: Optional[str] = Field(alias='Report ID')
    department_id: Optional[str] = Field(alias='Department ID')
    site_uuid: Optional[str] = Field(alias='Site UUID')
    releasing_party: Optional[str] = Field(alias='Releasing party')
    redirecting_number: Optional[str] = Field(alias='Redirecting number')
    transfer_related_call_ID: Optional[str] = Field(alias='Transfer related call ID')
    dialed_digits: Optional[str] = Field(alias='Dialed digits')
    authorization_code: Optional[str] = Field(alias='Authorization code')

    @classmethod
    def from_dicts(cls, dicts: Iterable[dict]) -> Generator['CallingCDR', None, None]:
        """
        Yield :class:`CallingCDR` instances from dicts

        :param dicts: iterable with the dicts to yield CDRs from
        :return: yields :class:`CallingCDR` instances

        Example:

            .. code-block:: python

                # download call history report from Webex
                cdrs = list(CallingCDR.from_dicts(api.reports.download(url=url)))

        """
        for record in dicts:
            yield cls.parse_obj(record)


@dataclass(init=False)
class ReportsApi(ApiChild, base='devices'):
    """
    Report templates are available for use with the Reports API.

    To access this endpoint, you must use an administrator token with the analytics:read_all scope. The authenticated
    user must be a read-only or full administrator of the organization to which the report belongs.

    To use this endpoint the organization needs to be licensed for Pro Pack for Control Hub.

    Reports available via Webex Control Hub may be generated and downloaded via the Reports API. To access this API,
    the authenticated user must be a read-only or full administrator of the organization to which the report belongs.

    """

    def list_templates(self) -> list[ReportTemplate]:
        """
        List all the available report templates that can be generated.

        CSV (comma separated value) reports for Webex services are only supported for organizations based in the
        North American region. Organizations based in other regions will return blank CSV files for any Webex reports.

        :return: list of report templates
        :rtype: list[ReportTemplate]
        """
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "Template Attributes" is actually "items"
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "validations"/"validations" is actually "validations"
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "id" is actually "Id"
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "startDate", "endDate" not documented
        url = self.session.ep('report/templates')
        data = self.get(url=url)
        result = parse_obj_as(list[ReportTemplate], data['items'])
        return result

    def list(self, report_id: str = None, service: str = None, template_id: str = None, from_date: date = None,
             to_date: date = None) -> Generator[Report, None, None]:
        """
        Lists all reports. Use query parameters to filter the response. The parameters are optional. However,
        from and to parameters should be provided together.

        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param report_id: List reports by ID.
        :param service: List reports which use this service.
        :param template_id: List reports with this report template ID.
        :param from_date: List reports that were created on or after this date.
        :param to_date: List reports that were created before this date.
        :return: yields :class:`Report` instances
        """
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "Report Attributes" is actually "items"
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   missing attribute: downloadDomain
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "id" is actually "Id"
        # TODO: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates, documentation bug
        #   "scheduledFrom" is actually "scheduleFrom"

        params = {to_camel(k.split('_')[0] if k.endswith('date') else k): v for k, v in locals().items()
                  if k not in {'self', 'from_date', 'to_date'} and v is not None}
        if from_date:
            params['from'] = from_date.strftime('%Y-%m-%d')
        if to_date:
            params['to'] = to_date.strftime('%Y-%m-%d')

        url = self.session.ep('reports')
        return self.session.follow_pagination(url=url, params=params, model=Report, item_key='items')

    def create(self, template_id: int, start_date: date = None, end_date: date = None, site_list: str = None) -> str:
        """
        Create a new report. For each templateId, there are a set of validation rules that need to be followed. For
        example, for templates belonging to Webex, the user needs to provide siteUrl. These validation rules can be
        retrieved via the Report Templates API.

        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param template_id: Unique ID representing valid report templates.
        :type template_id: int
        :param start_date: Data in the report will be from this date onwards.
        :type start_date: date
        :param end_date: Data in the report will be until this date.
        :type end_date: date
        :param site_list: Sites belonging to user's organization. This attribute is needed for site-based templates.
        :type site_list: str
        :return: The unique identifier for the report.
        :rtype: str
        """
        # TODO: https://developer.webex.com/docs/api/v1/reports/create-a-report, documentation bug
        #   result actually is something like: {'items': {'Id': 'Y2...lMg'}}
        body = {'templateId': template_id}
        if start_date:
            body['startDate'] = start_date.strftime('%Y-%m-%d')
        if end_date:
            body['endDate'] = end_date.strftime('%Y-%m-%d')
        if site_list:
            body['siteList'] = site_list
        url = self.session.ep('reports')
        data = self.post(url=url, json=body)
        result = data['items']['Id']
        return result

    def details(self, report_id: str) -> Report:
        """
        Shows details for a report, by report ID.

        Specify the report ID in the reportId parameter in the URI.

        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param report_id: The unique identifier for the report.
        :type report_id: str
        :return: report details
        :rtype: Report
        """
        # TODO: https://developer.webex.com/docs/api/v1/reports/create-a-report, documentation bug
        #   result actually is something like: {'items': [{'title': 'Engagement Report', 'service': 'Webex Calling',
        #   'startDate': '2021-12-14', 'endDate': '2022-01-13', 'siteList': '', 'created': '2022-01-14 11:16:59',
        #   'createdBy': 'Y2lz..GM', 'scheduleFrom': 'api', 'status': 'done', 'downloadDomain':
        #   'https://reportdownload-a.webex.com/',  'downloadURL':
        #   'https://reportdownload-a.webex.com/api?reportId=Y2lz3ZA',  'Id': 'Y23ZA'}], 'numberOfReports': 1}
        url = self.session.ep(f'reports/{report_id}')
        data = self.get(url=url)
        result = Report.parse_obj(data['items'][0])
        return result

    def delete(self, report_id: str):
        """
        Remove a report from the system.

        Specify the report ID in the reportId parameter in the URI

        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param report_id: The unique identifier for the report.
        :type report_id: str
        """
        url = self.session.ep(f'reports/{report_id}')
        super().delete(url=url)

    def download(self, url: str) -> Generator[dict, None, None]:
        """
        Download a report from the given URL and yield the rows as dicts

        :param url: download URL
        :type url: str
        :return: yields dicts
        """
        '''async
    async def download(self, url: str) -> List[dict]:
        """
        Download a report from the given URL and yield the rows as dicts

        :param url: download URL
        :type url: str
        :return: list of dicts (one per row)
        :rtype: list[dict]
        """
        headers = {'Authorization': f'Bearer {self.session.access_token}'}
        async with self.session.get(url=url, headers=headers) as r:
            r.raise_for_status()
            lines = [line.decode(encoding='utf-8-sig') async for line in r.content]
            reader = csv.DictReader(lines)
            return list(reader)

        '''
        headers = {'Authorization': f'Bearer {self.session.access_token}'}
        with self.session.get(url=url, stream=True, headers=headers) as r:
            r.raise_for_status()
            lines = (line.decode(encoding='utf-8-sig') for line in r.iter_lines())
            reader = csv.DictReader(lines)
            yield from reader

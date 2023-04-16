from collections.abc import Generator

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, enum_str
from wxc_sdk.base import SafeEnum as Enum
from typing import List, Optional
from pydantic import Field, parse_obj_as


__all__ = ['CreateReportResponse', 'ListReportTemplatesResponse', 'ListReportsResponse', 'Report',
           'ReportTemplatesApi', 'ReportsApi', 'Template', 'ValidationRules', 'ValidationRulesCollection']


class ValidationRules(ApiModel):
    #: Field on which validation rule is applied
    field: Optional[str]
    #: Whether the above field is required
    required: Optional[str]


class ValidationRulesCollection(ApiModel):
    #: An array of validation rules
    validations: Optional[list[ValidationRules]]


class Template(ApiModel):
    #: Unique identifier representing a report.
    id: Optional[str]
    #: Name of the template.
    title: Optional[str]
    #: The service to which the report belongs.
    service: Optional[str]
    #: Maximum date range for reports belonging to this template.
    max_days: Optional[int]
    #: Generated reports belong to which field.
    identifier: Optional[str]
    validations: Optional[ValidationRulesCollection]


class ListReportTemplatesResponse(ApiModel):
    #: An array of template object
    template_attributes: Optional[list[Template]] = Field(alias='Template Attributes')


class ReportTemplatesApi(ApiChild, base='report/templates'):
    """
    Report templates are available for use with the Reports API.
    To access this endpoint, you must use an administrator token with the analytics:read_all scope. The authenticated
    user must be a read-only or full administrator of the organization to which the report belongs.
    To use this endpoint the organization needs to be licensed for Pro Pack for Control Hub.
    For more information about Report Templates, see the Admin API guide.
    """

    def list_report_templates(self) -> list[Template]:
        """
        List all the available report templates that can be generated.
        CSV (comma separated value) reports for Webex services are only supported for organizations based in the North
        American region. Organizations based in other regions will return blank CSV files for any Webex reports.

        documentation: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates
        """
        url = self.ep()
        data = super().get(url=url)
        return parse_obj_as(list[Template], data["Template Attributes"])

class Report(ApiModel):
    #: Unique identifier for the report.
    id: Optional[str]
    #: Name of the template to which this report belongs.
    title: Optional[str]
    #: The service to which the report belongs.
    service: Optional[str]
    #: The data in this report belongs to dates greater than or equal to this.
    start_date: Optional[str]
    #: The data in this report belongs to dates smaller than or equal to this.
    end_date: Optional[str]
    #: The site to which this report belongs to. This only exists if the report belongs to service Webex.
    site_list: Optional[str]
    #: Time of creation for this report.
    created: Optional[str]
    #: The person who created the report.
    created_by: Optional[str]
    #: Whether this report was scheduled from API or Control Hub.
    scheduled_from: Optional[str]
    #: Completion status of this report.
    status: Optional[str]
    #: The link from which the report can be downloaded.
    download_url: Optional[str]


class ListReportsResponse(ApiModel):
    #: An array of report objects.
    report_attributes: Optional[list[Report]] = Field(alias='Report Attributes')


class CreateReportBody(ApiModel):
    #: Unique ID representing valid report templates.
    template_id: Optional[int]
    #: Data in the report will be from this date onwards.
    start_date: Optional[str]
    #: Data in the report will be until this date.
    end_date: Optional[str]
    #: Sites belonging to user's organization. This attribute is needed for site-based templates.
    site_list: Optional[str]


class CreateReportResponse(ApiModel):
    #: The unique identifier for the report.
    id: Optional[str]


class ReportsApi(ApiChild, base='reports'):
    """
    To access these endpoints, you must use an administrator token with the analytics:read_all scope. The authenticated
    user must be a read-only or full administrator of the organization to which the report belongs.
    To use this endpoint the org needs to be licensed for the Pro Pack.
    Reports available via Webex Control Hub may be generated and downloaded via the Reports API. To access this API,
    the authenticated user must be a read-only or full administrator of the organization to which the report belongs.
    For more information about Reports, see the Admin API guide.
    """

    def list(self, report_id: str = None, service: str = None, template_id: int = None, from_: str = None, to_: str = None) -> list[Report]:
        """
        Lists all reports. Use query parameters to filter the response. The parameters are optional. However, from and
        to parameters should be provided together.
        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param report_id: List reports by ID.
        :type report_id: str
        :param service: List reports which use this service.
        :type service: str
        :param template_id: List reports with this report template ID.
        :type template_id: int
        :param from_: List reports that were created on or after this date.
        :type from_: str
        :param to_: List reports that were created before this date.
        :type to_: str

        documentation: https://developer.webex.com/docs/api/v1/reports/list-reports
        """
        params = {}
        if report_id is not None:
            params['reportId'] = report_id
        if service is not None:
            params['service'] = service
        if template_id is not None:
            params['templateId'] = template_id
        if from_ is not None:
            params['from'] = from_
        if to_ is not None:
            params['to'] = to_
        url = self.ep()
        data = super().get(url=url, params=params)
        return parse_obj_as(list[Report], data["Report Attributes"])

    def create(self, template_id: int, start_date: str = None, end_date: str = None, site_list: str = None) -> str:
        """
        Create a new report. For each templateId, there are a set of validation rules that need to be followed. For
        example, for templates belonging to Webex, the user needs to provide siteUrl. These validation rules can be
        retrieved via the Report Templates API.
        The 'templateId' parameter is a number. However, it is a limitation of developer.webex.com platform that it is
        passed as a string when you try to test the API from here.
        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param template_id: Unique ID representing valid report templates.
        :type template_id: int
        :param start_date: Data in the report will be from this date onwards.
        :type start_date: str
        :param end_date: Data in the report will be until this date.
        :type end_date: str
        :param site_list: Sites belonging to user's organization. This attribute is needed for site-based templates.
        :type site_list: str

        documentation: https://developer.webex.com/docs/api/v1/reports/create-a-report
        """
        body = CreateReportBody()
        if template_id is not None:
            body.template_id = template_id
        if start_date is not None:
            body.start_date = start_date
        if end_date is not None:
            body.end_date = end_date
        if site_list is not None:
            body.site_list = site_list
        url = self.ep()
        data = super().post(url=url, data=body.json())
        return data["id"]

    def details(self, report_id: str) -> Report:
        """
        Shows details for a report, by report ID.
        Specify the report ID in the reportId parameter in the URI.
        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param report_id: The unique identifier for the report.
        :type report_id: str

        documentation: https://developer.webex.com/docs/api/v1/reports/get-report-details
        """
        url = self.ep(f'{report_id}')
        data = super().get(url=url)
        return Report.parse_obj(data)

    def delete(self, report_id: str):
        """
        Remove a report from the system.
        Specify the report ID in the reportId parameter in the URI
        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param report_id: The unique identifier for the report.
        :type report_id: str

        documentation: https://developer.webex.com/docs/api/v1/reports/delete-a-report
        """
        url = self.ep(f'{report_id}')
        super().delete(url=url)
        return

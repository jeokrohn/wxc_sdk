from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['Report', 'ReportsApi']


class Report(ApiModel):
    #: Unique identifier for the report.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mYzhjMWFhMS00OTM5LTQ2NjEtODAwMy1hYWE0MzFmZWM0ZmE
    id: Optional[str] = None
    #: Name of the template to which this report belongs.
    #: example: Bots Activity
    title: Optional[str] = None
    #: The service to which the report belongs.
    #: example: Teams
    service: Optional[str] = None
    #: The data in this report belongs to dates greater than or equal to this.
    #: example: 2020-02-23
    start_date: Optional[datetime] = None
    #: The data in this report belongs to dates smaller than or equal to this.
    #: example: 2020-03-24
    end_date: Optional[datetime] = None
    #: The site to which this report belongs to. This only exists if the report belongs to service `Webex`.
    #: example: cisco.webex.com
    site_list: Optional[str] = None
    #: Time of creation for this report.
    #: example: 2020-03-24 17:13:39
    created: Optional[datetime] = None
    #: The person who created the report.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mYzhjMWFhMS00OTM5LTQ2NjEtODAwMy1hYWE0MzFmZWM0ZmE
    created_by: Optional[str] = None
    #: Whether this report was scheduled from API or Control Hub.
    #: example: API
    scheduled_from: Optional[str] = None
    #: Completion status of this report.
    #: example: done
    status: Optional[str] = None
    #: The link from which the report can be downloaded.
    #: example: https://downloadservicebts.webex.com/api?reportId=Y2lzY29zcGFyazovL3VzL1JFUE9SVC9hZDBkMjA1NzVkYTA0NWE0OGZhZDQ3ZDk3NGFiNDFmMg
    download_url: Optional[str] = Field(alias='downloadURL', default=None)


class ReportsApi(ApiChild, base='reports'):
    """
    Reports
    
    To access these endpoints, you must use an administrator token with the `analytics:read_all` `scope
    <https://developer.webex.com/docs/integrations#scopes>`_. The
    authenticated user must be a read-only or full administrator of the organization to which the report belongs.
    
    To use this endpoint the org needs to be licensed for the Pro Pack.
    
    Reports available via `Webex Control Hub
    <https://admin.webex.com>`_ may be generated and downloaded via the Reports API. To access this API,
    the authenticated user must be a read-only or full administrator of the organization to which the report belongs.
    
    For more information about Reports, see the `Admin API
    <https://developer.webex.com/docs/admin#reports-api>`_ guide.
    """

    def list_reports(self, report_id: str = None, service: str = None, template_id: int = None, from_: Union[str,
                     datetime] = None, to_: Union[str, datetime] = None) -> list[Report]:
        """
        List Reports

        Lists all reports. Use query parameters to filter the response. The parameters are optional. However, `from`
        and `to` parameters should be provided together.

        **Notes**:
        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        Reports are usually provided in zip format. A Content-header `application/zip` or `application/octet-stream`
        does indicate the zip format. There is usually no .zip file extension.

        :param report_id: List reports by ID.
        :type report_id: str
        :param service: List reports which use this service.
        :type service: str
        :param template_id: List reports with this report template ID.
        :type template_id: int
        :param from_: List reports that were created on or after this date.
        :type from_: Union[str, datetime]
        :param to_: List reports that were created before this date.
        :type to_: Union[str, datetime]
        :rtype: list[Report]
        """
        params = {}
        if report_id is not None:
            params['reportId'] = report_id
        if service is not None:
            params['service'] = service
        if template_id is not None:
            params['templateId'] = template_id
        if from_ is not None:
            if isinstance(from_, str):
                from_ = isoparse(from_)
            from_ = dt_iso_str(from_)
            params['from'] = from_
        if to_ is not None:
            if isinstance(to_, str):
                to_ = isoparse(to_)
            to_ = dt_iso_str(to_)
            params['to'] = to_
        url = self.ep()
        data = super().get(url, params=params)
        r = TypeAdapter(list[Report]).validate_python(data['Report Attributes'])
        return r

    def create_a_report(self, template_id: str, start_date: Union[str, datetime] = None, end_date: Union[str,
                        datetime] = None, site_list: str = None) -> str:
        """
        Create a Report

        Create a new report. For each `templateId`, there are a set of validation rules that need to be followed. For
        example, for templates belonging to Webex, the user needs to provide `siteUrl`. These validation rules can be
        retrieved via the `Report Templates API
        <https://developer.webex.com/docs/api/v1/report-templates>`_.

        The 'templateId' parameter is a number. However, it is a limitation of developer.webex.com platform that it is
        passed as a string when you try to test the API from here.

        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param template_id: Unique ID representing valid report templates.
        :type template_id: str
        :param start_date: Data in the report will be from this date onwards.
        :type start_date: Union[str, datetime]
        :param end_date: Data in the report will be until this date.
        :type end_date: Union[str, datetime]
        :param site_list: Sites belonging to user's organization. This attribute is needed for site-based templates.
        :type site_list: str
        :rtype: str
        """
        body = dict()
        body['templateId'] = template_id
        if start_date is not None:
            body['startDate'] = start_date
        if end_date is not None:
            body['endDate'] = end_date
        if site_list is not None:
            body['siteList'] = site_list
        url = self.ep()
        data = super().post(url, json=body)
        r = data['id']
        return r

    def get_report_details(self, report_id: str) -> Report:
        """
        Get Report Details

        Shows details for a report, by report ID.

        Specify the report ID in the `reportId` parameter in the URI.

        **Notes**:
        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        Reports are usually provided in zip format. A Content-header `application/zip` or `application/octet-stream`
        does indicate the zip     format. There is usually no .zip file extension.

        :param report_id: The unique identifier for the report.
        :type report_id: str
        :rtype: :class:`Report`
        """
        url = self.ep(f'{report_id}')
        data = super().get(url)
        r = Report.model_validate(data)
        return r

    def delete_a_report(self, report_id: str):
        """
        Delete a Report

        Remove a report from the system.

        Specify the report ID in the `reportId` parameter in the URI

        CSV reports for Teams services are only supported for organizations based in the North American region.
        Organizations based in a different region will return blank CSV files for any Teams reports.

        :param report_id: The unique identifier for the report.
        :type report_id: str
        :rtype: None
        """
        url = self.ep(f'{report_id}')
        super().delete(url)

from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel


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


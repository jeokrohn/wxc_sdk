from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Report', 'ReportCollectionResponse']


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


class ReportCollectionResponse(ApiModel):
    #: An array of report objects.
    report attributes: Optional[list[Report]] = Field(alias='Report Attributes', default=None)

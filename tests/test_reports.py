"""
unit tests for reports
"""
import csv
import io
import json
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta

from tests.base import TestCaseWithLog
from wxc_sdk.reports import CallingCDR, Report


class TestReports(TestCaseWithLog):

    @staticmethod
    def print_reports(details: list[Report]):
        for detail in details:
            print(f'created {detail.created.isoformat()} start {detail.start_date.isoformat()} '
                  f'end {detail.end_date.isoformat()} service "{detail.service}" title "{detail.title}" status "'
                  f'{detail.status}"')

    def test_001_templates(self):
        templates = self.api.reports.list_templates()
        print(f'Got {len(templates)} templates')

    def test_002_list(self):
        reports = list(self.api.reports.list())
        print(f'Got {len(reports)} reports')
        self.print_reports(reports)

    def test_003_list_with_dates(self):
        all_reports = list(self.api.reports.list())
        from_date = min(r.created.date() for r in all_reports)
        to_date = max(r.created.date() for r in all_reports) + timedelta(days=1)
        reports = list(self.api.reports.list(from_date=from_date, to_date=to_date))
        all_reports.sort(key=lambda r: r.created)
        reports.sort(key=lambda r: r.created)
        self.print_reports(reports)
        self.assertEqual(all_reports, reports)

    def test_004_list_webex_calling(self):
        all_reports = list(self.api.reports.list())
        reports = list(self.api.reports.list(service='Webex Calling'))
        all_reports.sort(key=lambda r: r.created)
        reports.sort(key=lambda r: r.created)
        self.print_reports(reports)
        self.assertEqual(all_reports, reports)

    def test_005_all_details(self):
        """
        details for all reports
        """
        all_reports = list(self.api.reports.list())
        # get details for all reports
        with ThreadPoolExecutor() as pool:
            details = list(pool.map(lambda r: self.api.reports.details(r.id), all_reports))
        print(f'got details for {len(details)} reports')
        details: list[Report]
        details.sort(key=lambda r: r.created)
        self.print_reports(details)

    def test_006_create_cdr(self):
        """
        Create a new CDR report
        """
        templates = self.api.reports.list_templates()
        cdr_template = next(t for t in templates if t.title == 'Calling Detailed Call History')
        today = date.today()
        end_date = today - timedelta(days=1)
        start_date = end_date - timedelta(days=cdr_template.max_days - 1)
        report_id = self.api.reports.create(template_id=cdr_template.id, start_date=start_date, end_date=end_date)
        details = self.api.reports.details(report_id=report_id)
        print('created report')
        print(json.dumps(json.loads(details.model_dump_json()), indent=2))

    def test_007_download_latest_cdr(self):
        """
        download CDRs of latest CDR history
        """

        all_reports = [r for r in self.api.reports.list() if r.title == 'Calling Detailed Call History' and
                       r.status == 'done']
        all_reports.sort(key=lambda r: r.created, reverse=True)
        if not all_reports:
            self.skipTest('No CDR reports')
        latest = all_reports[0]
        details = self.api.reports.details(report_id=latest.id)
        url = latest.download_url
        cdrs = list(CallingCDR.from_dicts(self.api.reports.download(url=url)))
        if not cdrs:
            self.skipTest('No CDRs')
        print(f'CDR report, start {details.start_date.isoformat()}, end {details.end_date.isoformat()}, '
              f'created {details.created.isoformat()}')
        print(f'{len(cdrs)} records, 1st call {min(r.start_time for r in cdrs).isoformat()}, '
              f'last call {max(r.start_time for r in cdrs).isoformat()}')

    @TestCaseWithLog.async_test
    async def test_008_async_download(self):
        all_reports = [r async for r in self.async_api.reports.list_gen()
                       if r.title == 'Calling Detailed Call History' and r.status == 'done']
        all_reports.sort(key=lambda r: r.created, reverse=True)
        if not all_reports:
            self.skipTest('No CDR reports')
        latest = all_reports[0]
        details = await self.async_api.reports.details(report_id=latest.id)
        url = details.download_url
        with self.assertRaises(NotImplementedError):
            cdrs = list(CallingCDR.from_dicts(await self.async_api.reports.download(url=url)))
            print(f'CDR report, start {details.start_date.isoformat()}, end {details.end_date.isoformat()}, '
                  f'created {details.created.isoformat()}')
            print(f'{len(cdrs)} records, 1st call {min(r.start_time for r in cdrs).isoformat()}, '
                  f'last call {max(r.start_time for r in cdrs).isoformat()}')


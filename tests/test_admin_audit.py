from datetime import datetime, timedelta
from operator import attrgetter

from inflection import underscore

from tests.base import TestCaseWithLog


class TestAdminAudit(TestCaseWithLog):
    def test_event_categories(self):
        categories = list(self.api.admin_audit.list_event_categories())
        print(f'Got {len(categories)} categories')
        print('\n'.join(categories))

    def test_list_events(self):
        org_id = self.api.people.me().org_id
        from_ = datetime.utcnow() - timedelta(days=364)
        to_ = datetime.utcnow()
        events = list(self.api.admin_audit.list_events(org_id=org_id, from_=from_, to_=to_))
        events.sort(key=attrgetter('created'))
        print(f'Got {len(events)} events')
        extras = dict()
        for event in events:
            data = event.data
            print(f'{event.created}: {data.action_text}')
            extra = data.model_extra

            if not extra:
                continue
            for k, v in extra.items():
                extras[k] = v.__class__.__name__
        if extras:
            print('add these attributes to class AuditEventData ')
            for k in sorted(extras):
                print(f'{underscore(k)}: Optional[Any] = None')
        self.assertTrue(not extras)


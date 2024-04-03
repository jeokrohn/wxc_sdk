from tests.base import TestCaseWithLog


class TestStatus(TestCaseWithLog):
    def test_001_test_status_summary(self):
        api = self.api.status
        summary = api.summary()

    def test_002_test_status(self):
        api = self.api.status
        status = api.status()

    def test_003_test_components(self):
        api = self.api.status
        components = api.components()
        print(f'got {len(components)} components')

    def test_004_test_unresolved_incidents(self):
        api = self.api.status
        incidents = api.unresolved_incidents()
        print(f'got {len(incidents)} unresolved incidents')

    def test_005_all_incidents(self):
        api = self.api.status
        incidents = api.all_incidents()
        print(f'got {len(incidents)} incidents')

    def test_006_upcoming_scheduled_maintenances(self):
        api = self.api.status
        maintenances = api.upcoming_scheduled_maintenances()
        print(f'got {len(maintenances)} upcoming scheduled maintenances')
        print('\n'.join(m.name for m in maintenances))

    def test_007_active_scheduled_maintenances(self):
        api = self.api.status
        maintenances = api.active_scheduled_maintenances()
        print(f'got {len(maintenances)} active scheduled maintenances')
        print('\n'.join(m.name for m in maintenances))

    def test_008_all_scheduled_maintenances(self):
        api = self.api.status
        maintenances = api.all_scheduled_maintenances()
        print(f'got {len(maintenances)} scheduled maintenances')
        print('\n'.join(m.name for m in maintenances))


from tests.base import TestCaseWithLog


class TestRouteChoices(TestCaseWithLog):
    # TODO: additional tests for various parameters
    def test_001_get_choices(self):
        """
        get all route choices
        :return:
        """
        route_choices = list(self.api.telephony.route_choices())
        print(f'Got {len(route_choices)} route choices')
        print('\n'.join(f'{rc.route_type:>11}: {rc.name}' for rc in route_choices))

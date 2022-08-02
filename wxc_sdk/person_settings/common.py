from ..api_child import ApiChild
from ..rest import RestSession

__all__ = ['PersonSettingsApiChild']


class PersonSettingsApiChild(ApiChild, base=''):
    """
    Base class for all classes implementing person settings APIs
    """

    feature = None

    def __init__(self, *, session: RestSession,
                 workspaces: bool = False, locations: bool = False):
        self.feature_prefix = '/features/'
        if workspaces:
            self.selector = 'workspaces'
        elif locations:
            self.selector = 'telephony/config/locations'
            self.feature_prefix = '/'
        else:
            self.selector = 'people'
        super().__init__(session=session, base=self.selector)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(base='')
        if cls.feature is None:
            raise TypeError('feature has to be defined')

    def f_ep(self, *, person_id: str, path: str = None) -> str:
        """
        person specific feature endpoint like v1/people/{uid}/features/....

        :param person_id: Unique identifier for the person.
        :type person_id: str
        :param path: path in the endpoint after the feature base URL
        :type path: str
        :return: full endpoint
        :rtype: str
        """
        path = path and f'/{path}' or ''
        return self.session.ep(f'{self.selector}/{person_id}{self.feature_prefix}{self.feature}{path}')

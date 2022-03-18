from ..api_child import ApiChild

__all__ = ['PersonSettingsApiChild']


class PersonSettingsApiChild(ApiChild, base='people'):
    """
    API for all user level settings
    """

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
        return self.session.ep(f'people/{person_id}/features{path}')

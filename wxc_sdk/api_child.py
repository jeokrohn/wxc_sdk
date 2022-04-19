from dataclasses import dataclass

from .base import StrOrDict
from .rest import RestSession

__all__ = ['ApiChild']


@dataclass(init=False)
class ApiChild:
    """
    Base class for child APIs of :class:`WebexSimpleApi`
    """
    session: RestSession

    def __init__(self, *, session: RestSession, base: str = None):
        #: REST session
        self.session = session
        if base:
            self.base = base

    def __init_subclass__(cls, base: str):
        """
        Subclass registration hook. Each APIChild has a specific endpoint prefix which we gather at subclass
        registration time-

        :param base: APIChild specific URL path
        """
        super().__init_subclass__()
        # save endpoint prefix
        cls.base = base

    def ep(self, path: str = None):
        """
        endpoint URL for given path

        :param path: path after APIChild subclass specific endpoint URI prefix
        :type path: str
        :return: endpoint URL
        :rtype: str
        """
        path = path and f'/{path}' or ''
        return self.session.ep(f'{self.base}{path}')

    def get(self, *args, **kwargs) -> StrOrDict:
        """
        GET request

        :param args:
        :param kwargs:
        :return:
        """
        return self.session.rest_get(*args, **kwargs)

    def post(self, *args, **kwargs) -> StrOrDict:
        """
        POST request

        :param args:
        :param kwargs:
        :return:
        """
        return self.session.rest_post(*args, **kwargs)

    def put(self, *args, **kwargs) -> StrOrDict:
        """
        PUT request

        :param args:
        :param kwargs:
        :return:
        """
        return self.session.rest_put(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        """
        DELETE request

        :param args:
        :param kwargs:
        """
        self.session.rest_delete(*args, **kwargs)

    def patch(self, *args, **kwargs) -> StrOrDict:
        """
        PATCH request

        :param args:
        :param kwargs:
        """
        return self.session.rest_patch(*args, **kwargs)

from wxc_sdk.api_child import ApiChild


class ScimApiChild(ApiChild, base='identity/scim'):

    def ep(self, path: str = None):
        """
        endpoint URL for given path

        :meta private:
        :param path: path after APIChild subclass specific endpoint URI prefix
        :type path: str
        :return: endpoint URL
        :rtype: str
        """
        path = path and f'/{path}' or ''
        return f'https://webexapis.com/{self.base}{path}'

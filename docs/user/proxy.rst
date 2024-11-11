Using proxies
=============


WebexSimpleApi
--------------

:class:`WebexSimpleApi <wxc_sdk.WebexSimpleApi>` can be used with with proxies by passing the URL of the proxy in the
`proxy_url` parameter when instantiating the API object:

.. code-block:: Python

    from wxc_sdk import WebexSimpleApi

    with WebexSimpleApi(access_token='your_access_token',
                        proxy_url='http://your.proxy.url:port') as api:
        # now can use the connection object for you code
        users = list(api.people.list())
    ...

The proxy will then be used for all HTTPS requests initiated by the API object.

If the proxy requires authentication, then the credentials can be included in the `proxy_url` parameter in this format:

    http://username:password@proxyserver:port

:class:`WebexSimpleApi <wxc_sdk.WebexSimpleApi>` in addition to the optional `proxy_url` parameter also accepts the
optional `verify` parameter. Both, `proxy_url` and `verify` are used to set the
:attr:`proxies <requests.Session.proxies>` and :attr:`verify <requests.Session.verify>` attributes of the
:class:`requests.Session` baseclass of the :attr:`RestSession <wxc_sdk.WebexSimpleApi.session>` object that is used
for all HTTPS requests by the api object.

For more advanced use cases the :attr:`RestSession <wxc_sdk.WebexSimpleApi.session>` object of the api object can be
accessed and updated directly.

AsWebexSimpleApi
----------------

Also the asyncio variant :class:`AsWebexSimpleApi <wxc_sdk.as_api.AsWebexSimpleApi>` can be used with with proxies by
passing the URL of the proxy in the `proxy_url` parameter when instantiating the API object:

.. code-block:: Python

    from wxc_sdk.as_api import AsWebexSimpleApi

    async with As WebexSimpleApi(access_token='your_access_token',
                                 proxy_url='http://your.proxy.url:port') as api:
        # now can use the connection object for you code
        users = await api.people.list()

The proxy will then be used for all HTTPS requests initiated by the API object.

If the proxy requires authentication, then the credentials can be included in the `proxy_url` parameter in this format:

    http://username:password@proxyserver:port

:class:`AsWebexSimpleApi <wxc_sdk.as_api.AsWebexSimpleApi>` uses an
:attr:`AsRestSession <wxc_sdk.as_api.AsWebexSimpleApi.session>` object that is based on :class:`aiohttp.ClientSession`
for all requests. Proxy parameters are not directly supported by :class:`aiohttp.ClientSession` but can be passed as
arguments when calling the :meth:`aiohttp.ClientSession.request` method. The
:class:`AsRestSession <wxc_sdk.as_rest.AsRestSession>`
constructor in addition to `proxy_url` also accepts the `ssl` parameter which is passed to each call of the
:meth:`aiohttp.ClientSession.request` method.

For further customization additional parameters given to the
:class:`AsWebexSimpleApi <wxc_sdk.as_api.AsWebexSimpleApi>` constructor are passed to the
:class:`AsRestSession <wxc_sdk.as_rest.AsRestSession>` constructor of the
:attr:`AsWebexSimpleApi.session <wxc_sdk.as_api.AsWebexSimpleApi.session>` attribute .

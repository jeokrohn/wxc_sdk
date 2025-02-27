Logging to HAR files
=====================

If needed you can log all REST requests and responses to HAR files. This can be useful for debugging or for creating
test cases. Here is an example of how to use the :class:`HarWriter <wxc_sdk.har_writer.HarWriter>` class:

.. code-block:: Python

    from wxc_sdk import WebexSimpleApi
    from wxc_sdk.har_writer import HarWriter

    with WebexSimpleApi() as api:
        with HarWriter(api=api, path='har_file.har') as har_writer:
            # now can use the connection object for you code
            users = list(api.people.list())
        # the HAR file will be written when the HarRecorder object is closed


The HAR file will contain all requests and responses in the format defined by the `HTTP Archive (HAR) format`. The
resulting HAR  file can be viewed with any HAR viewer, e.g. the `HAR Viewer` browser extension.

The HAR writer can also be used with the `asyncio` variant of the SDK:

.. code-block:: Python

    import asyncio
    from wxc_sdk.as_api import AsWebexSimpleApi
    from wxc_sdk.har_writer import HarWriter

    async def main():
        async with AsWebexSimpleApi() as api:
            with HarWriter(api=api, path='har_file.har') as har_writer:
                # now can use the connection object for you code
                users = await api.people.list()
            # the HAR file will be written when the HarRecorder object is closed

    if __name__ == '__main__':
        asyncio.run(main())

Another use case of the HAR writer is to record the REST requests and responses to memory only and
then use the recorded data in test cases. This can be done by not passing a `path` attribute when creating the
:class:`HarWriter <wxc_sdk.har_writer.HarWriter>` instance. The recorded data can then be accessed through the
:attr:`har <wxc_sdk.har_writer.HarWriter.har>` attribute of the :class:`HarWriter <wxc_sdk.har_writer.HarWriter>`
instance.
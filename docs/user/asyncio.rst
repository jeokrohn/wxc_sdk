Using `asyncio`
===============

Async version of the SDK
------------------------

With :class:`wxc_sdk.as_api.AsWebexSimpleApi` the SDK offers an asyncio variant based on asyncio/aiohttp. This
variant is automatically generated based off the source of the synchronous API and offers async variants of the
endpoints using the same datastructures as the synchronous API.

Here is an example of how to use the asyncio SDK:

.. literalinclude:: ../../examples/calling_users_async.py
    :language: Python

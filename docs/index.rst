.. currentmodule:: wxc_sdk
.. highlight:: python
   :linenothreshold: 5

=======
wxc_sdk
=======

A simple SDK to work with `Webex APIs <https://developer.webex.com>`_, special focus on Webex Calling specific API
endpoints.

----------------------------------------------

This is how easy it is to use the SDK. The example code list all calling enabled users within the org.

.. literalinclude:: ../examples/calling_users.py
    :language: Python

Installation
------------

Installing and upgrading wxc_sdk is easy:

**Install via PIP**

.. code-block:: bash

    $ pip install wxc-sdk

**Upgrade to the latest version**

.. code-block:: bash

    $ pip install wxc-sdk --upgrade

Documentation
-------------

Documentation is available at:
http://wxc_sdk.readthedocs.io

Examples
--------

Sample scripts are available in the examples_ folder.

Also the test cases in the tests_ folder can serve as examples of how to use the SDK.

.. _examples: https://github.com/jeokrohn/wxc_sdk/tree/master/examples
.. _tests: https://github.com/jeokrohn/wxc_sdk/tree/master/tests

Datatypes
---------

Datatypes are defined in the respective subpackages and submodules and have to be imported from there explicitly:

.. code-block::

   from wxc_sdk.people import Person
   from wxc_sdk.person_settings.barge import BargeSettings

To allow to abstract from the subpackage and submodule structure any datatype can also be imported from
``wxc_sdk.all_types`` directly:

.. code-block::

   from wxc_sdk.all_types import Person, BargeSettings

All ``wxc_sdk`` data types can also be imported at once:

.. code-block::

   from wxc_sdk.all_types import *

Async version of the SDK (experimental)
---------------------------------------

With :class:`wxc_sdk.as_api.AsWebexSimpleApi` the SDK offers an async variant based on asyncio/aiohttp. This variant is
automatically generated based off the source of the synchronous API and offers async variants of the endpoints using the
same datastructures as the synchronous API.

Here is an example of how to use the async SDK:

.. literalinclude:: ../examples/calling_users_async.py
    :language: Python

Reference
---------

.. toctree::
   :maxdepth: 4

   apidoc/wxc_sdk.rst
   changes.rst
   rest_debug.rst
   examples.rst
   method_ref.rst


---------

Indices and tables
==================
* :ref:`genindex`
* :ref:`search`

.. currentmodule:: wxc_sdk
.. highlight:: python
   :linenothreshold: 5

=======
wxc_sdk
=======

A simple SDK to work with `Webex APIs <https://developer.webex.com>`_, special focus on Webex Calling specific API
endpoints.

.. this is the main left side TOC
.. toctree::
    :maxdepth: 1
    :hidden:

    user/installation
    user/asyncio
    user/proxy
    user/examples
    user/rest_debug
    user/har_writer
    user/changes
    user/method_ref
    apidoc/wxc_sdk


----------------------------------------------

This is how easy it is to use the SDK. The example code list all calling enabled users within the org.

.. literalinclude:: ../examples/calling_users.py
    :language: Python

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

---------

Indices and tables
==================
* :ref:`genindex`
* :ref:`search`

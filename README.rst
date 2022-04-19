=======
wxc_sdk
=======

A simple SDK to work with `Webex APIs <https://developer.webex.com>`_, special focus on Webex Calling specific API
endpoints.

----------------------------------------------

This is how easy it is to use the SDK. The example code list all calling enabled users within the org.

.. code-block:: Python

    from wxc_sdk import WebexSimpleApi

    api = WebexSimpleApi()

    # if a user is enabled for calling, then the location_id attribute is set
    calling_users = [user for user in api.people.list(calling_data=True)
                     if user.location_id]
    print(f'{len(calling_users)} users:')
    print('\n'.join(user.display_name for user in calling_users))


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

.. _examples: https://github.com/jeokrohn/wxc_sdk/tree/master/examples



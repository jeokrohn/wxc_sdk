Examples
========

Code examples can be found in the `examples directory on GitHub`_

Also take a look at the unit tests in the `tests directory`_.

Get all calling users
---------------------

Source: |calling_users.py|_

.. |calling_users.py| replace:: ``calling_users.py``


.. literalinclude:: ../examples/calling_users.py
    :linenos:

Default call forwarding settings for all users
----------------------------------------------

This example start with the list of all calling users and then calls
:meth:`wxc_sdk.person_settings.forwarding.PersonForwardingApi.configure` for each user. To speed up things a
``ThreadPoolExecutor`` is used and all update operations are scheduled for execution by the thread pool.

Source: |reset_call_forwarding.py|_

.. |reset_call_forwarding.py| replace:: ``reset_call_forwarding.py``

.. literalinclude:: ../examples/reset_call_forwarding.py
    :linenos:

Modify number of rings configuration for users read from CSV
------------------------------------------------------------

Here we read a bunch of user email addresses from a CSV. The CSV as an ERROR column and we only want to consider
users without errors.

For all these users a VM setting is updated and the results are written to a CSV for further processing.

Source: |modify_voicemail.py|_

.. |modify_voicemail.py| replace:: ``modify_voicemail.py``

.. literalinclude:: ../examples/modify_voicemail.py
    :linenos:


Holiday schedule w/ US national holidays for all US locations
-------------------------------------------------------------

This example uses the Calendarific API at https://calendarific.com/ to get a list of national US holidays and creates
a "``National Holidays``" holiday schedule for all US locations with all these national holidays.

A rudimentary API implementation in |calendarific.py|_ is used for the requests to https://calendarific.com/.
Calendarific APIs require all requests to be authenticated using an API key. You can `sign up for a free account`_ to get
a free API account key which then is read from environment variable ``CALENDARIFIC_KEY``.

.. |calendarific.py| replace:: ``calendarific.py``

Source: |us_holidays.py|_

.. |us_holidays.py| replace:: ``us_holidays.py``

.. literalinclude:: ../examples/us_holidays.py
    :linenos:


Persist tokens and obtain new tokens interactively
--------------------------------------------------

A typical problem specifically when creating CLI scripts is how to obtain valid access tokens for the API operations.
If your code wants to invoke Webex REST APIs on behalf of a user then an integration is needed. The concepts of
integrations are explained at the `"Integrations" page on developer.cisco.com`_.

This example code shows how an OAUth Grant flow for an integration can be initiated from a script by using the Python
`webbrowser module`_ and calling the ``open()`` method with the authorization URL of a given integration to open that
URL in the system web browser. The user can then authenticate and grant access to the integration. In the last
step of a successful authorization flow the web browser is redirected to the ``redirect_url`` of the
integration.

The example code starts a primitive web server serving GET requests to ``http://localhost:6001/redirect``.
This URL has to be the redirect URL of the integration you create under `My Webex Apps on developer.webex.com`_.

The sample script reads the integration parameters from environment variables (``TOKEN_INTEGRATION_CLIENT_ID``,
``TOKEN_INTEGRATION_CLIENT_SECRET``, ``TOKEN_INTEGRATION_CLIENT_SCOPES``). These variables can also be defined in
``get_tokens.env`` in the current directory:

.. literalinclude:: ../examples/get_tokens.env (sample)

The sample code persists the tokens in ``get_tokens.yml`` in the current directory. On startup the sample code tries
to read tokens from that file. If needed a new access token is obtained using the refresh token.

An OAuth flow is only initiated if no (valid) tokens could be read from ``get_tokens.yml``

Source: |get_tokens.py|_

.. |get_tokens.py| replace:: ``get_tokens.py``

.. literalinclude:: ../examples/get_tokens.py
    :linenos:


.. _examples directory on GitHub: https://github.com/jeokrohn/wxc_sdk/tree/master/examples
.. _"Integrations" page on developer.cisco.com: https://developer.webex.com/docs/integrations

.. _get_tokens.py: https://github.com/jeokrohn/wxc_sdk/blob/master/examples/get_tokens.py
.. _calling_users.py: https://github.com/jeokrohn/wxc_sdk/blob/master/examples/calling_users.py
.. _us_holidays.py: https://github.com/jeokrohn/wxc_sdk/blob/master/examples/us_holidays.py
.. _calendarific.py: https://github.com/jeokrohn/wxc_sdk/blob/master/examples/calendarific.py
.. _reset_call_forwarding.py: https://github.com/jeokrohn/wxc_sdk/blob/master/examples/reset_call_forwarding.py
.. _modify_voicemail.py: https://github.com/jeokrohn/wxc_sdk/blob/master/examples/modify_voicemail.py

.. _webbrowser module: https://docs.python.org/3/library/webbrowser.html
.. _My Webex Apps on developer.webex.com: https://developer.webex.com/my-apps

.. _tests directory: https://github.com/jeokrohn/wxc_sdk/tree/master/tests

.. _sign up for a free account: https://calendarific.com/signup




Logging of REST requests
========================

Detailed logging of REST requests and responses is available through the ``wxc_sdk.rest`` logger.
The logging level has ot be set to ``logging.DEBUG`` to enable REST logging.

Access tokens are masked in the generated logs.

Example output (IDs truncated to protect the innocent):

    ::

        2022-03-25 06:11:36,098 MainThread Request 200[OK]: GET https://webexapis.com/v1/telephony/config/locations/Y2l...k5NA/queues/Y2lzY2..TI5dA
          User-Agent: python-requests/2.27.1
          Accept-Encoding: gzip, deflate
          Accept: */*
          Connection: keep-alive
          authorization: Bearer ***
          content-type: application/json;charset=utf-8
          TrackingID: SIMPLE_eac8a6d5-9b81-4fc7-b184-a80c78dd6315
         Response
          Date: Fri, 25 Mar 2022 06:11:35 GMT
          Content-Type: application/json
          Transfer-Encoding: chunked
          Connection: keep-alive
          cache-control: no-cache, no-store, no-cache, no-store
          via: 1.1 linkerd, 1.1 linkerd, 1.1 linkerd, 1.1 linkerd
          content-encoding: gzip
          trackingid: SIMPLE_eac8a6d5-9b81-4fc7-b184-a80c78dd6315, SIMPLE_eac8a6d5-9b81-4fc7-b184-a80c78dd6315
          server: Redacted
          vary: accept-encoding
          strict-transport-security: max-age=63072000; includeSubDomains; preload
          ---response body ---
          {
            "id": "Y2lzY29...WTI5dA",
            "name": "cq_003",
            "enabled": true,
            "language": "English",
            "languageCode": "en_us",
            "firstName": ".",
            "lastName": "cq_003",
            "timeZone": "America/Los_Angeles",
            "extension": "8003",
            "alternateNumberSettings": {
              "distinctiveRingEnabled": true,
              "alternateNumbers": []
          .....

REST logging is used extensively in the `test cases`_. Check the implementation of the TestCaseWithLog_ class.
This base class for test cases sets up REST logging to a dedicated log file for each test case.

.. _TestCaseWithLog: https://github.com/jeokrohn/wxc_sdk/blob/4b9f9131a39f4a543af865e2b456e7ff0731bce2/tests/base.py#L270-L311
.. _test cases: https://github.com/jeokrohn/wxc_sdk/tree/master/tests

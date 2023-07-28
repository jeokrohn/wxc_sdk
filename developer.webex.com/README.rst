Trying to auto-create a reference of APIs by scraping developer.webex.com
-------------------------------------------------------------------------

Install ChromeDriver
=======================

https://chromedriver.chromium.org/getting-started

* Download webdriver version matching Chrome from https://chromedriver.chromium.org/downloads

    .. image:: developer.webex.com/README_rst/chrome_version.png
        :width: 200
* unzip
* move driver to directory in path

  | ``% sudo mv chromedriver /usr/local/bin``
  | ``% which chromedriver``
  | ``/usr/local/bin/chromedriver``

* check webdriver

  | ``% python``
  | ``>>> from selenium import webdriver``
  | ``>>> driver = webdriver.Chrome()``
  | ``>>> driver.get("http://selenium.dev")``
  | ``>>> driver.quit()``

  If error message pops up ...

  .. image:: developer.webex.com/README_rst/chromedriver.security.png
        :width: 200

  ... trust the webdriver binary by lifting the quarantine:

  | ``% xattr -d com.apple.quarantine /usr/local/bin/chromedriver``

Get Google Chrome for testing
=============================

* Download from: https://googlechromelabs.github.io/chrome-for-testing/

* remove extended attribute that prohibits Chrome from starting

  | ``xattr -cr 'Google Chrome for Testing.app'``






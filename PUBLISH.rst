# Steps to publish a new release

* review pyproject.toml for outdated packages
    * update constraints as needed
* poetry update
* run "script/test lint" and review/fix
* set version number in pyproject.toml
* set version number in wxc_sdk.__init__
* set version number in tests/test_wxc_sdk.py
* update docs/changes.rst, prepare commit message
* run "script/build"
* check API changes based on information scraped from developer.webex.com
* run all tests and check results
* review TODOs: did we miss anything
* run "script/build"
* commit changes, don't push
* tag commit with version number: e.g. "1.5.0"
* push to GitHub: MAKE SURE TO PUSH TAGS!

* poetry publish
* review read the docs
* build docs for last tag on readthedocs; under "Versions"
* review pypi
* review GitHub

# Steps to publish a new release

* create branch for new release
* review pyproject.toml for outdated packages
    * update constraints as needed
* poetry update
* run "script/test lint" and review/fix
* set version number in pyproject.toml
* set version number in wxc_sdk.__init__
* set version number in tests/test_wxc_sdk.py
* set version number in docs/conf.py
* update docs/changes.rst, prepare commit message
* shelve all changes that should not be part of the build
* run "script/build"
* check API changes based on information scraped from developer.webex.com
* run all tests and check results
* review TODOs: did we miss anything
* run "script/build"
* commit changes, don't push
* merge branch
* tag commit with version number: e.g. "1.5.0"
* push to GitHub: MAKE SURE TO PUSH TAGS!

* poetry publish
* review read the docs: especially check build logs for errors
* build docs for last tag on readthedocs; under "Versions"
* review pypi
* review GitHub

* unshelve changes that were not part of the build

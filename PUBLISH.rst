# Steps to publish a new release

* create branch for new release
* review pyproject.toml for outdated packages
    * update constraints as needed
* uv lock --upgrade
* uv sync
* run "script/test lint" and review/fix
* update docs/user/changes.rst
* shelve all changes that should not be part of the build
* run all tests and check results
* review TODOs: did we miss anything
* commit changes, don't push
* merge branch
* run "uv run cz bump" and review
* chech changelog, tag, commit
* git push --follow-tags
* review read the docs: especially check build logs for errors
* readthedocs: set new default version
* build docs for last tag on readthedocs; under "Versions"
* review pypi
* review GitHub
* unshelve changes that were not part of the build



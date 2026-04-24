# Steps to publish a new release

* create branch for new release
* review pyproject.toml for outdated packages
    * update constraints as needed
* uv lock --upgrade
* uv sync
* run "script/test lint" and review/fix
* update docs/user/changes.rst based on "uv run cz bump --dry-run"
* shelve all changes that should not be part of the build
* run all tests and check results
* review TODOs: did we miss anything
* commit changes, don't push
* merge branch
* run "uv run cz bump --dry-run" and check version bump
* add new version tag to docs/user/changes.rst and commit change
* run "uv run cz bump" and review
* check changelog, tag, commit
* build: make package
* uv publish
* git push --tags
* review read the docs: especially check build logs for errors
* readthedocs: set new default version
* review pypi
* review GitHub
* unshelve changes that were not part of the build



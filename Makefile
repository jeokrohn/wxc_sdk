# Makefile for project build automation
# Copyright (c) 2026 Johannes Krohn <jkrohn@cisco.com>
# License: MIT

.PHONY: all package docs types async methref apib oas clean rst

# Default target builds everything
all: clean types methref async docs package

clean:
	@echo "==> Cleaning previous build artifacts"
	script/clean

types:
	@echo "==> Creating types.py"
	script/all_types.py

methref:
	@echo "==> Creating method_ref.rst"
	script/method_ref.py

async:
	@echo "==> Creating as_api.py"
	script/async_gen.py

rst:
	@echo "==> Building RST files"
	uv run sphinx-apidoc -o docs/apidoc -f -e -M wxc_sdk 'wxc_sdk/all_types.py'

docs:
	@echo "==> Building the Docs"
	uv run make -C docs clean
	rm -f docs/apidoc/*.rst
	uv run sphinx-apidoc -o docs/apidoc -f -e -M wxc_sdk 'wxc_sdk/all_types.py'
	uv run make -C docs html

package:
	@echo "==> Building the Source Distribution package"
	rm -rf dist/
	uv build

oas:
	@echo "==> Creating Python sources from OAS files"
	script/oas2py.py --cleanup
	script/oas2py.py --with-examples

apib:
	@echo "==> Creating Python sources from APIB files"
	script/apib2py.py "*.apib" --exclude "attachment-actions|meeting-preferences" --with-examples